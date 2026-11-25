"""Canonical loading for VIA.

The loader accepts the two YAML schemas found in the DAVINCI corpus (English
and Portuguese keys), drops the empty dependency strings produced by the
generator, and applies the same name normalization used by the F1 scorer.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


class SchemaError(ValueError):
    """Raised when an artifact cannot be read as an architecture."""


@dataclass
class Service:
    name: str
    responsibilities: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    endpoints: list[str] = field(default_factory=list)


@dataclass
class Architecture:
    system: str
    services: list[Service]
    interactions: list[tuple[str, str]]
    source_path: Path | None = None
    schema: str = "en"
    warnings: list[str] = field(default_factory=list)
    raw_text: str = ""


@dataclass
class CanonicalArchitecture:
    """Services and edges with normalized names.

    ``declared`` is the set of canonical service names. ``dependencies`` and
    ``interactions`` keep the canonical endpoints, including names that do not
    resolve to a declared service, because D05 must report them.
    """

    services: dict[str, Service]
    declared: set[str]
    dependencies: set[tuple[str, str]]
    interactions: set[tuple[str, str]]
    duplicate_names: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _as_list(value: Any) -> list[str]:
    """Coerce a YAML value to a list of non-empty strings.

    A scalar string is treated as one item. The generator sometimes writes an
    empty string inside a list; those entries are dropped here so they cannot
    become a fake service or a dangling dependency.
    """
    if value is None:
        return []
    if isinstance(value, str):
        raw = [value]
    elif isinstance(value, (list, tuple, set)):
        raw = list(value)
    else:
        raw = [value]
    result: list[str] = []
    for item in raw:
        text = _text(item)
        if text:
            result.append(text)
    return result


def _pick(mapping: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_key(name: str) -> str:
    """Normalize a system or folder name for case and punctuation insensitive match."""
    return re.sub(r"[\s_-]+", "", str(name).strip().lower())


SYSTEM_FOLDERS = {
    "7ep": "7ep",
    "acmeair": "acmeair",
    "cargo-tracker": "cargo-tracker",
    "daytrader7": "daytrader7",
    "jokul": "jokul",
    "jpetstore": "jpetstore",
    "pet-clinic": "pet-clinic",
    "tntconcept": "TNTConcept",
}


def find_input_dir(inputs_root: Path, system: str) -> Path:
    wanted = normalize_key(system)
    for folder in sorted(inputs_root.iterdir()):
        if folder.is_dir() and normalize_key(folder.name) == wanted:
            return folder
    raise FileNotFoundError(f"input folder not found for system {system!r}")


def find_result_dir(result_root: Path, system: str) -> Path:
    wanted = normalize_key(system)
    candidates = [
        folder
        for folder in sorted(result_root.iterdir())
        if folder.is_dir() and normalize_key(folder.name) == wanted
    ]
    if not candidates:
        raise FileNotFoundError(f"result folder not found for system {system!r}")

    def run_count(folder: Path) -> int:
        base = folder / "result_generalized_fewshot"
        return len(list(base.glob("run_*"))) if base.is_dir() else -1

    # The corpus has duplicate folders such as ``cargo-tracker`` and
    # ``cargo tracker``. The canonical one is the one with the most runs.
    candidates.sort(key=lambda folder: (-run_count(folder), folder.name))
    for folder in candidates:
        if (folder / "result_generalized_fewshot").is_dir():
            return folder / "result_generalized_fewshot"
    return candidates[0] / "result_generalized_fewshot"


def load_normalization(system_dir: Path) -> tuple[dict[str, str], list[str]]:
    """Read ``name_normalization_map.txt`` if it exists.

    The file format is ``source -> target``. Missing files are not an error;
    the corpus has folders without a map.
    """
    path = system_dir / "name_normalization_map.txt"
    if not path.exists():
        return {}, [f"normalization map missing: {path}"]
    mapping: dict[str, str] = {}
    warnings: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text or text.startswith("#") or "->" not in text:
            continue
        source, target = text.split("->", 1)
        source = source.strip()
        target = target.strip()
        if source and target:
            mapping[source.lower()] = target
    return mapping, warnings


def canonical_name(name: str, mapping: dict[str, str]) -> str:
    value = re.sub(r"\s+", " ", str(name).strip())
    for _ in range(3):
        replacement = mapping.get(value.lower())
        if not replacement or replacement == value:
            break
        value = replacement
    return value


def load_requirements(system_dir: Path) -> tuple[list[dict[str, str]], list[str]]:
    """Read requirements and assign stable synthetic identifiers.

    Only bullet lines are requirements. The corpus files also contain blank
    separators and a few observations at the end; those are kept out of the
    count and reported as warnings.
    """
    path = system_dir / "requirements.txt"
    if not path.exists():
        raise FileNotFoundError(f"requirements not found: {path}")
    requirements: list[dict[str, str]] = []
    warnings: list[str] = []
    skipped = 0
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        text = line.strip()
        if not text:
            continue
        if not text.startswith("- "):
            skipped += 1
            continue
        body = text[2:].strip()
        if not body:
            continue
        match = re.match(r"^(R\d{2,})\s*[-:]?\s+(.+)$", body)
        if match:
            identifier, body = match.group(1), match.group(2).strip()
        else:
            identifier = f"R{len(requirements) + 1:02d}"
        requirements.append({"id": identifier, "texto": body, "linha": str(line_number)})
    if skipped:
        warnings.append(f"{skipped} non-bullet lines ignored in requirements")
    return requirements, warnings


def _interactions(doc: dict[str, Any]) -> tuple[list[tuple[str, str]], list[str]]:
    raw = _pick(doc, ("interactions", "interacoes")) or []
    if not isinstance(raw, list):
        return [], ["interactions is not a list"]
    result: list[tuple[str, str]] = []
    warnings: list[str] = []
    for item in raw:
        source = target = ""
        if isinstance(item, dict):
            source = _text(
                _pick(item, ("from", "de", "origem", "source", "origem_servico"))
            )
            target = _text(
                _pick(item, ("to", "para", "destino", "target", "destino_servico"))
            )
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            source, target = _text(item[0]), _text(item[1])
        else:
            warnings.append(f"unrecognized interaction entry: {item!r}")
            continue
        if source and target:
            result.append((source, target))
    return result, warnings


def load_architecture(path: Path, system: str) -> Architecture:
    """Load one architecture YAML file."""
    if not path.exists():
        raise SchemaError(f"artifact not found: {path}")
    raw_text = path.read_text(encoding="utf-8")
    if not raw_text.strip():
        raise SchemaError("empty artifact")
    try:
        doc = yaml.safe_load(raw_text)
    except yaml.YAMLError as error:
        raise SchemaError(f"invalid YAML: {error}") from error
    if not isinstance(doc, dict):
        raise SchemaError("top level is not a mapping")

    if "services" in doc:
        schema = "en"
    elif "servicos" in doc:
        schema = "pt"
    else:
        raise SchemaError("missing services/servicos key")

    raw_services = doc.get("services") or doc.get("servicos") or []
    if not isinstance(raw_services, list):
        raise SchemaError("services is not a list")
    if not raw_services:
        raise SchemaError("empty services list")

    services: list[Service] = []
    warnings: list[str] = []
    for index, item in enumerate(raw_services):
        if not isinstance(item, dict):
            warnings.append(f"service {index} is not a mapping")
            continue
        name = _text(_pick(item, ("name", "nome")))
        if not name:
            warnings.append(f"service {index} has no name")
            continue
        services.append(
            Service(
                name=name,
                responsibilities=_as_list(
                    _pick(item, ("responsibilities", "responsabilidades"))
                ),
                dependencies=_as_list(_pick(item, ("dependencies", "dependencias"))),
                endpoints=_as_list(
                    _pick(
                        item,
                        ("suggested_endpoints", "endpoints_sugeridos", "endpoints"),
                    )
                ),
            )
        )

    if not services:
        raise SchemaError("no service with a name")

    interactions, interaction_warnings = _interactions(doc)
    warnings.extend(interaction_warnings)
    return Architecture(
        system=system,
        services=services,
        interactions=interactions,
        source_path=path,
        schema=schema,
        warnings=warnings,
        raw_text=raw_text,
    )


def canonicalize(
    architecture: Architecture, mapping: dict[str, str]
) -> CanonicalArchitecture:
    """Apply normalization to services, dependencies and interactions.

    Duplicate canonical names are merged into the first occurrence; the laudo
    records the collision. The corpus has none after normalization, but a
    future input may.
    """
    services: dict[str, Service] = {}
    duplicates: list[str] = []
    warnings: list[str] = []
    for service in architecture.services:
        name = canonical_name(service.name, mapping)
        if name in services:
            duplicates.append(name)
            first = services[name]
            first.responsibilities.extend(service.responsibilities)
            first.dependencies.extend(service.dependencies)
            first.endpoints.extend(service.endpoints)
            continue
        services[name] = Service(
            name=name,
            responsibilities=list(service.responsibilities),
            dependencies=[canonical_name(item, mapping) for item in service.dependencies],
            endpoints=list(service.endpoints),
        )
    declared = set(services)
    dependencies = {
        (name, target)
        for name, service in services.items()
        for target in service.dependencies
    }
    interactions = {
        (canonical_name(source, mapping), canonical_name(target, mapping))
        for source, target in architecture.interactions
    }
    return CanonicalArchitecture(
        services=services,
        declared=declared,
        dependencies=dependencies,
        interactions=interactions,
        duplicate_names=sorted(set(duplicates)),
        warnings=warnings,
    )


def strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char))
