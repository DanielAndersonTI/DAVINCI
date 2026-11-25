"""Corpus manifest and the Claude C2 execution-id repair.

The data.csv produced by the previous experiment has 360 rows. Seven
execution ids are duplicated and one is empty, all in Claude/C2. The three
runs of each system are present in ``result/`` and can be ordered
chronologically by the timestamp embedded in the directory name. The repair
records the original id, the resolved id and the evidence, and never modifies
``data.csv`` or any artifact.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from .loader import (
    SchemaError,
    find_result_dir,
    load_architecture,
    normalize_key,
    sha256_file,
)


@dataclass
class RowMapping:
    row_index: int
    row: dict[str, str]
    original_id: str
    resolved_id: str
    method: str
    run_dir: Path | None
    note: str = ""
    f1_row_serv: str = ""
    f1_row_inter: str = ""
    f1_summary_serv: str = ""
    f1_summary_inter: str = ""


def _number(value: str) -> float | None:
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _summary_f1(run_dir: Path) -> tuple[float | None, float | None]:
    path = run_dir / "sumario.json"
    if not path.exists():
        return None, None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        metrics = payload.get("metricas") or {}
        if not isinstance(metrics, dict):
            return None, None
        service = (metrics.get("consolidada") or {}).get("f1_score")
        interaction = (metrics.get("consolidada_inter") or {}).get("f1_score")
        return (
            float(service) if service is not None else None,
            float(interaction) if interaction is not None else None,
        )
    except (OSError, ValueError, TypeError, json.JSONDecodeError, AttributeError):
        return None, None


def _matches(row: dict[str, str], run_dir: Path) -> bool:
    row_service = _number(row.get("f1_serv", ""))
    row_interaction = _number(row.get("f1_inter", ""))
    summary_service, summary_interaction = _summary_f1(run_dir)
    if row_service is not None and summary_service is not None:
        if abs(row_service - summary_service) > 1e-4:
            return False
    if row_interaction is not None and summary_interaction is not None:
        if abs(row_interaction - summary_interaction) > 1e-4:
            return False
    return True


def _mapping_method(run_dir: Path | None, original: str, resolved: str) -> str:
    if run_dir is None:
        return "unresolved"
    if original and original == resolved:
        return "original_id"
    return "claude_c2_repair"


def _repair_shifted(
    rows: list[dict[str, str]],
    row_indices: list[int],
    result_root: Path,
    prefixes: tuple[str, ...],
    method_prefix: str,
) -> list[RowMapping]:
    """Assign the three runs of a shifted cell in chronological order.

    Claude/C2 and Claude/C4 were written with execution ids shifted by one
    system. The three directories are still present; their names carry the run
    timestamp. The summary F1 is used as a cross-check; when it disagrees, an
    unclaimed directory with matching F1 is searched before giving up.
    """
    if not row_indices:
        return []
    system = rows[row_indices[0]]["system"]
    try:
        result_dir = find_result_dir(result_root, system)
    except FileNotFoundError:
        return [
            RowMapping(
                row_index=index,
                row=rows[index],
                original_id=rows[index]["execution_id"],
                resolved_id="",
                method="unresolved",
                run_dir=None,
                note="result directory not found",
            )
            for index in row_indices
        ]

    candidates = sorted(
        [
            path
            for path in result_dir.glob("run_*")
            if any(path.name.startswith(prefix) for prefix in prefixes)
        ],
        key=lambda path: path.name,
    )
    ordered_rows = sorted(row_indices, key=lambda index: int(rows[index]["execution"] or 0))
    mappings: list[RowMapping] = []
    used: set[Path] = set()

    for position, index in enumerate(ordered_rows):
        row = rows[index]
        resolved_dir: Path | None = None
        method = ""
        note = ""
        if position < len(candidates) and candidates[position] not in used:
            candidate = candidates[position]
            if _matches(row, candidate):
                resolved_dir = candidate
                method = f"{method_prefix}_chronological"
            else:
                note = "cronologia nao confere com sumario"
        if resolved_dir is None:
            for candidate in sorted(result_dir.glob("run_*"), key=lambda path: path.name):
                if candidate in used:
                    continue
                if _matches(row, candidate):
                    resolved_dir = candidate
                    method = f"{method_prefix}_f1_match"
                    break
        if resolved_dir is None:
            original = row["execution_id"]
            if original:
                candidate = result_dir / f"run_{original}"
                if candidate.is_dir() and candidate not in used:
                    resolved_dir = candidate
                    method = "original_id"
        if resolved_dir is not None:
            used.add(resolved_dir)
        original = row["execution_id"]
        resolved = resolved_dir.name[4:] if resolved_dir is not None else ""
        summary_service, summary_interaction = (
            _summary_f1(resolved_dir) if resolved_dir is not None else (None, None)
        )
        mappings.append(
            RowMapping(
                row_index=index,
                row=row,
                original_id=original,
                resolved_id=resolved,
                method=method or "unresolved",
                run_dir=resolved_dir,
                note=note,
                f1_row_serv=row.get("f1_serv", ""),
                f1_row_inter=row.get("f1_inter", ""),
                f1_summary_serv="" if summary_service is None else f"{summary_service}",
                f1_summary_inter="" if summary_interaction is None else f"{summary_interaction}",
            )
        )
    return mappings


def resolve_rows(
    rows: list[dict[str, str]], result_root: Path
) -> list[RowMapping]:
    """Resolve every data.csv row to one run directory."""
    mappings: list[RowMapping | None] = [None] * len(rows)
    shifted: dict[tuple[str, str], dict[str, list[int]]] = {}
    for index, row in enumerate(rows):
        key = (row.get("llm", ""), row.get("config", ""))
        if key in {("Claude", "C2"), ("Claude", "C4")}:
            shifted.setdefault(key, {}).setdefault(row["system"], []).append(index)
            continue
        original = row.get("execution_id", "")
        run_dir = None
        method = "unresolved"
        if original:
            try:
                result_dir = find_result_dir(result_root, row["system"])
                candidate = result_dir / f"run_{original}"
                if candidate.is_dir():
                    run_dir = candidate
                    method = "original_id"
            except FileNotFoundError:
                run_dir = None
            if run_dir is None:
                # A few runs of 7ep were written under result/7ed, a folder
                # typo from the previous experiment. A unique global match is
                # accepted and recorded; no artifact is moved.
                hits = sorted(result_root.glob(f"*/result_generalized_fewshot/run_{original}"))
                if len(hits) == 1:
                    run_dir = hits[0]
                    method = "global_id_fallback"
        mappings[index] = RowMapping(
            row_index=index,
            row=row,
            original_id=original,
            resolved_id=original if run_dir is not None else "",
            method=method,
            run_dir=run_dir,
        )

    for (llm, config), systems in shifted.items():
        prefixes = (
            ("run_20260916_235", "run_20260917_00")
            if config == "C2"
            else ("run_20260923_20",)
        )
        for _system, indices in systems.items():
            repaired = _repair_shifted(
                rows,
                indices,
                result_root,
                prefixes=prefixes,
                method_prefix=f"claude_{config.lower()}",
            )
            for mapping in repaired:
                mappings[mapping.row_index] = mapping

    return [mapping for mapping in mappings if mapping is not None]


def build_manifest(
    data_csv: Path,
    result_root: Path,
    manifest_path: Path,
    mapping_path: Path,
) -> list[RowMapping]:
    with data_csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    mappings = resolve_rows(rows, result_root)

    manifest_rows: list[dict[str, str]] = []
    fix_rows: list[dict[str, str]] = []
    for mapping in mappings:
        row = mapping.row
        run_dir = mapping.run_dir
        yaml_path = run_dir / "especificacao_arquitetural.yaml" if run_dir else None
        status = "included"
        reason = ""
        yaml_sha = ""
        services = ""
        interactions = ""
        yaml_status = ""
        if run_dir is None:
            status, reason = "excluded", "run directory not resolved"
        elif not yaml_path.exists():
            status, reason = "excluded", "architecture YAML missing"
        elif yaml_path.stat().st_size == 0:
            status, reason, yaml_status = "excluded", "empty architecture YAML", "empty"
        else:
            yaml_sha = sha256_file(yaml_path)
            try:
                architecture = load_architecture(yaml_path, row["system"])
            except SchemaError as error:
                status, reason, yaml_status = "excluded", f"schema error: {error}", "invalid"
            else:
                services = str(len(architecture.services))
                interactions = str(len(architecture.interactions))
                yaml_status = "valid"
                if len(architecture.services) < 2:
                    status, reason = "excluded", "fewer than two services"
        manifest_rows.append(
            {
                "row_index": str(mapping.row_index),
                "system": row["system"],
                "llm": row["llm"],
                "config": row["config"],
                "execution": row["execution"],
                "execution_id_original": mapping.original_id,
                "execution_id_resolved": mapping.resolved_id,
                "mapping_method": mapping.method,
                "run_dir": "" if run_dir is None else str(run_dir),
                "yaml_path": "" if yaml_path is None else str(yaml_path),
                "yaml_sha256": yaml_sha,
                "yaml_status": yaml_status,
                "services": services,
                "interactions": interactions,
                "status": status,
                "reason": reason,
            }
        )
        if mapping.method != "original_id" or mapping.original_id != mapping.resolved_id:
            fix_rows.append(
                {
                    "row_index": str(mapping.row_index),
                    "system": row["system"],
                    "llm": row["llm"],
                    "config": row["config"],
                    "execution": row["execution"],
                    "original_id": mapping.original_id,
                    "resolved_id": mapping.resolved_id,
                    "method": mapping.method,
                    "note": mapping.note,
                    "f1_row_serv": mapping.f1_row_serv,
                    "f1_summary_serv": mapping.f1_summary_serv,
                    "f1_row_inter": mapping.f1_row_inter,
                    "f1_summary_inter": mapping.f1_summary_inter,
                }
            )

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(manifest_rows[0].keys()) if manifest_rows else []
    with manifest_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(manifest_rows)

    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    fix_fields = list(fix_rows[0].keys()) if fix_rows else [
        "row_index", "system", "llm", "config", "execution", "original_id",
        "resolved_id", "method", "note", "f1_row_serv", "f1_summary_serv",
        "f1_row_inter", "f1_summary_inter",
    ]
    with mapping_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fix_fields)
        writer.writeheader()
        writer.writerows(fix_rows)
    return mappings


def build_corpus_lock(
    manifest_path: Path,
    data_csv: Path,
    lock_path: Path,
) -> dict:
    with manifest_path.open(encoding="utf-8", newline="") as handle:
        manifest = list(csv.DictReader(handle))
    included = [row for row in manifest if row["status"] == "included"]
    excluded = [row for row in manifest if row["status"] != "included"]
    reasons: dict[str, int] = {}
    for row in excluded:
        reasons[row["reason"]] = reasons.get(row["reason"], 0) + 1
    lock = {
        "corpus_version": "v1",
        "via_version": "1.0.0",
        "data_csv": str(data_csv),
        "data_csv_sha256": sha256_file(data_csv),
        "manifest_sha256": sha256_file(manifest_path),
        "n_rows": len(manifest),
        "n_included": len(included),
        "n_excluded": len(excluded),
        "excluded_by_reason": dict(sorted(reasons.items())),
        "systems": sorted({row["system"] for row in manifest}),
        "models": sorted({row["llm"] for row in manifest}),
        "configs": sorted({row["config"] for row in manifest}),
        "generated_on": "2026-11-24",
    }
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(
        json.dumps(lock, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return lock
