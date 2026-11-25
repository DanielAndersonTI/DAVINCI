import csv
import json
from pathlib import Path

from via.analysis import (
    _holm,
    _metric,
    _paired_units,
    _sign_flip_p,
    prevalence,
    run_analysis,
)


def record(system: str, llm: str, config: str, execution: int, services: int = 4, **codes) -> dict:
    resumo = {
        "system": system,
        "llm": llm,
        "config": config,
        "execution": str(execution),
        "services": str(services),
        "d03": str(codes.get("d03", 0)),
        "d04": str(codes.get("d04", 0)),
        "d05": str(codes.get("d05", 0)),
        "d06": str(codes.get("d06", 0)),
        "d07": "0",
        "d11": str(codes.get("d11", 0)),
        "d12": str(codes.get("d12", 0)),
        "defect_rate": str(codes.get("defect_rate", 1.0)),
        "cycle_density": str(codes.get("cycle_density", 0.0)),
        "gini": str(codes.get("gini", 0.0)),
        "endpoints_per_responsibility": str(codes.get("endpoints_per_responsibility", 0.2)),
        "stability_edges": str(codes.get("stability_edges", 0.5)),
    }
    data = {"system": system, "llm": llm, "config": config, "execution": str(execution), "f1_inter": str(codes.get("f1_inter", 0.8))}
    return {"resumo": resumo, "data": data}


def test_structural_rate_uses_only_d03_to_d06() -> None:
    merged = [record("S", "Claude", "C1", 1, services=4, d03=1, d04=1, d11=4, d12=1)]
    assert _metric(merged[0], "structural_defect_rate") == 0.5


def test_prevalence_counts_each_artifact_once() -> None:
    merged = [
        record("S", "Claude", "C1", 1, d04=2),
        record("S", "Claude", "C1", 2, d04=1),
        record("S", "Claude", "C1", 3, d04=0),
    ]
    rows = {row["codigo"]: row for row in prevalence(merged)}
    assert rows["D04"]["achados"] == 3
    assert rows["D04"]["artefatos_com_achado"] == 2
    assert rows["D04"]["share_artefatos"] == "0.666667"


def test_paired_units_requires_both_groups() -> None:
    merged = [
        record("S", "Claude", "C1", 1, cycle_density=0.2),
        record("S", "Claude", "C0", 1, cycle_density=0.4),
        record("S", "Gemini", "C1", 1, cycle_density=0.3),
    ]
    units = _paired_units(merged, ("system", "llm"), "config", "C1", "C0", "cycle_density")
    assert units == [(0.2, 0.4)]


def test_holm_is_monotone_and_capped() -> None:
    adjusted = _holm([0.01, 0.04, 0.03])
    assert adjusted == [0.03, 0.06, 0.06]


def test_sign_flip_detects_consistent_shift() -> None:
    differences = [0.2, 0.3, 0.25, 0.15, 0.22, 0.28]
    p_value = _sign_flip_p(differences, n_perm=500, seed=7)
    assert p_value is not None
    assert p_value < 0.05


def write_inputs(tmp_path: Path, merged: list[dict]) -> tuple[Path, Path]:
    resumo_path = tmp_path / "summary.csv"
    data_path = tmp_path / "data.csv"
    with resumo_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(merged[0]["resumo"]))
        writer.writeheader()
        writer.writerows(record["resumo"] for record in merged)
    with data_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(merged[0]["data"]))
        writer.writeheader()
        writer.writerows(record["data"] for record in merged)
    return resumo_path, data_path


def test_run_analysis_writes_the_expected_tables(tmp_path: Path) -> None:
    merged = []
    for system in ("A", "B"):
        for index, execution in enumerate((1, 2, 3, 4), 1):
            merged.append(
                record(
                    system,
                    "Gemini" if index % 2 else "DeepSeek",
                    "C1" if index <= 2 else "C0",
                    execution,
                    services=4,
                    d04=index % 3,
                    d11=4 - index % 2,
                    structural_defect_rate=index / 10,
                    f1_inter=0.7 + index / 100,
                )
            )
    resumo_path, data_path = write_inputs(tmp_path, merged)
    out = tmp_path / "out"
    overview = run_analysis(resumo_path, data_path, out, n_boot=50, seed=3)
    assert overview["n_artefatos"] == 8
    for name in (
        "prevalence.csv",
        "by_model.csv",
        "by_config.csv",
        "by_system.csv",
        "by_cell.csv",
        "correlations.csv",
        "pooled_correlations.csv",
        "contrasts.csv",
        "exploratory_contrasts.csv",
        "overview.json",
    ):
        assert (out / name).exists(), name
    with (out / "contrasts.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["hipotese"] for row in rows] == ["H1", "H2", "H3"]
    assert json.loads((out / "overview.json").read_text(encoding="utf-8"))["n_artefatos"] == 8
