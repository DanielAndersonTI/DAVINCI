from pathlib import Path

import pytest

from via.io.loader import (
    SchemaError,
    canonicalize,
    canonical_name,
    load_architecture,
    load_requirements,
)


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_load_english_schema_drops_empty_dependencies(tmp_path: Path) -> None:
    path = write(
        tmp_path / "a.yaml",
        """
services:
  - name: "A Service"
    responsibilities: ["do a"]
    dependencies: ["", "B Service"]
    suggested_endpoints: ["/a"]
  - name: "B Service"
    responsibilities: ["do b"]
    dependencies: []
    suggested_endpoints: ["/b"]
interactions:
  - from: "A Service"
    to: "B Service"
""",
    )
    architecture = load_architecture(path, "Demo")
    assert architecture.schema == "en"
    assert [service.name for service in architecture.services] == ["A Service", "B Service"]
    assert architecture.services[0].dependencies == ["B Service"]
    assert architecture.interactions == [("A Service", "B Service")]


def test_load_portuguese_schema(tmp_path: Path) -> None:
    path = write(
        tmp_path / "b.yaml",
        """
servicos:
  - nome: "Servico A"
    responsabilidades: ["fazer a"]
    dependencias: ["Servico B"]
    endpoints_sugeridos: ["/a"]
  - nome: "Servico B"
    responsabilidades: ["fazer b"]
    dependencias: []
    endpoints_sugeridos: ["/b"]
interacoes:
  - de: "Servico A"
    para: "Servico B"
""",
    )
    architecture = load_architecture(path, "Demo")
    assert architecture.schema == "pt"
    assert len(architecture.services) == 2
    assert architecture.interactions == [("Servico A", "Servico B")]


def test_empty_artifact_raises(tmp_path: Path) -> None:
    path = write(tmp_path / "empty.yaml", "")
    with pytest.raises(SchemaError, match="empty"):
        load_architecture(path, "Demo")


def test_missing_services_raises(tmp_path: Path) -> None:
    path = write(tmp_path / "bad.yaml", "foo: bar\n")
    with pytest.raises(SchemaError, match="missing services"):
        load_architecture(path, "Demo")


def test_normalization_is_transitive_and_case_insensitive() -> None:
    mapping = {"book service": "Book Catalog Service"}
    assert canonical_name("BOOK SERVICE", mapping) == "Book Catalog Service"
    assert canonical_name("Book Catalog Service", mapping) == "Book Catalog Service"


def test_canonicalize_merges_duplicate_names(tmp_path: Path) -> None:
    path = write(
        tmp_path / "c.yaml",
        """
services:
  - name: "Book Service"
    responsibilities: ["one"]
    dependencies: []
    suggested_endpoints: []
  - name: "Book Catalog Service"
    responsibilities: ["two"]
    dependencies: []
    suggested_endpoints: []
""",
    )
    architecture = load_architecture(path, "Demo")
    canonical = canonicalize(architecture, {"book service": "Book Catalog Service"})
    assert canonical.declared == {"Book Catalog Service"}
    assert canonical.duplicate_names == ["Book Catalog Service"]
    assert canonical.services["Book Catalog Service"].responsibilities == ["one", "two"]


def test_requirements_use_only_bullets_and_stable_ids(tmp_path: Path) -> None:
    path = write(
        tmp_path / "requirements.txt",
        """
- The system must do A.
- The system must do B.

A note that is not a requirement.
- R07 The system must do C.
""",
    )
    requirements, warnings = load_requirements(tmp_path)
    assert [item["id"] for item in requirements] == ["R01", "R02", "R07"]
    assert [item["texto"] for item in requirements] == [
        "The system must do A.",
        "The system must do B.",
        "The system must do C.",
    ]
    assert warnings == ["1 non-bullet lines ignored in requirements"]
