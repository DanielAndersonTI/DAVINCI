import csv
import json
from pathlib import Path

from via.io.manifest import build_corpus_lock, build_manifest, resolve_rows


def make_run(root: Path, name: str, services: int = 2, empty: bool = False) -> Path:
    run = root / "TestSystem" / "result_generalized_fewshot" / name
    run.mkdir(parents=True, exist_ok=True)
    (run / "sumario.json").write_text(
        json.dumps(
            {
                "metricas": {
                    "consolidada": {"f1_score": 0.9},
                    "consolidada_inter": {"f1_score": 0.8},
                }
            }
        ),
        encoding="utf-8",
    )
    yaml_path = run / "especificacao_arquitetural.yaml"
    if empty:
        yaml_path.write_text("", encoding="utf-8")
    else:
        body = ["services:"]
        for index in range(services):
            body.extend(
                [
                    f'  - name: "S{index}"',
                    "    responsibilities:",
                    f'      - "do {index}"',
                    "    dependencies: []",
                    "    suggested_endpoints:",
                    f'      - "/s{index}"',
                ]
            )
        yaml_path.write_text("\n".join(body) + "\n", encoding="utf-8")
    return run


def write_data(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["system", "llm", "config", "execution", "execution_id", "f1_serv", "f1_inter"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_claude_c2_duplicate_ids_are_resolved_chronologically(tmp_path: Path) -> None:
    result = tmp_path / "result"
    first = "20260916_235000_000001"
    second = "20260917_000000_000002"
    third = "20260917_001000_000003"
    make_run(result, f"run_{first}")
    make_run(result, f"run_{second}")
    make_run(result, f"run_{third}")
    rows = [
        {"system": "TestSystem", "llm": "Claude", "config": "C2", "execution": "1", "execution_id": first, "f1_serv": "0.9", "f1_inter": "0.8"},
        {"system": "TestSystem", "llm": "Claude", "config": "C2", "execution": "2", "execution_id": second, "f1_serv": "0.9", "f1_inter": "0.8"},
        {"system": "TestSystem", "llm": "Claude", "config": "C2", "execution": "3", "execution_id": second, "f1_serv": "0.9", "f1_inter": "0.8"},
    ]
    mappings = resolve_rows(rows, result)
    assert [mapping.resolved_id for mapping in mappings] == [first, second, third]
    assert all(mapping.method == "claude_c2_chronological" for mapping in mappings)


def test_empty_yaml_is_excluded_without_deleting_it(tmp_path: Path) -> None:
    result = tmp_path / "result"
    first = "20260916_235000_000001"
    second = "20260917_000000_000002"
    third = "20260917_001000_000003"
    make_run(result, f"run_{first}", services=2)
    make_run(result, f"run_{second}", empty=True)
    make_run(result, f"run_{third}", services=2)
    data = tmp_path / "data.csv"
    rows = [
        {"system": "TestSystem", "llm": "Claude", "config": "C2", "execution": "1", "execution_id": first, "f1_serv": "0.9", "f1_inter": "0.8"},
        {"system": "TestSystem", "llm": "Claude", "config": "C2", "execution": "2", "execution_id": second, "f1_serv": "0.9", "f1_inter": "0.8"},
        {"system": "TestSystem", "llm": "Claude", "config": "C2", "execution": "3", "execution_id": third, "f1_serv": "0.9", "f1_inter": "0.8"},
    ]
    write_data(data, rows)
    manifest = tmp_path / "manifest.csv"
    mapping = tmp_path / "mapping.csv"
    build_manifest(data, result, manifest, mapping)
    with manifest.open(encoding="utf-8", newline="") as handle:
        entries = list(csv.DictReader(handle))
    assert [entry["status"] for entry in entries] == ["included", "excluded", "included"]
    assert entries[1]["reason"] == "empty architecture YAML"
    assert (result / "TestSystem" / "result_generalized_fewshot" / f"run_{second}" / "especificacao_arquitetural.yaml").exists()
    lock = build_corpus_lock(manifest, data, tmp_path / "corpus.json")
    assert lock["n_included"] == 2
    assert lock["n_excluded"] == 1
    assert lock["excluded_by_reason"] == {"empty architecture YAML": 1}
