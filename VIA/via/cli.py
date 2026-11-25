"""Command line interface for the VIA verifier.

Run from the ``VIA`` directory so that the package is importable:

    python -m via manifest --data ..\\Report-and-Dates\\...\\data.csv ...
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from .graph import build_graph
from .io.loader import (
    canonicalize,
    find_input_dir,
    load_architecture,
    load_normalization,
    load_requirements,
    sha256_file,
)
from .io.manifest import build_corpus_lock, build_manifest
from .metrics import compute_metrics, jaccard
from .report import build_laudo, write_json, write_markdown
from .rules.automatic import evaluate

DEFAULT_D07_MODE = "not_applicable"


def _safe(value: str) -> str:
    return "".join(char if char.isalnum() or char in "-_." else "_" for char in value)


def _read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def command_manifest(args: argparse.Namespace) -> None:
    mappings = build_manifest(
        data_csv=Path(args.data),
        result_root=Path(args.result),
        manifest_path=Path(args.manifest),
        mapping_path=Path(args.mapping),
    )
    lock = build_corpus_lock(
        manifest_path=Path(args.manifest),
        data_csv=Path(args.data),
        lock_path=Path(args.lock),
    )
    print(json.dumps(lock, ensure_ascii=False, indent=2))
    print(f"manifest: {args.manifest}")
    print(f"mapping:  {args.mapping}")
    print(f"lock:     {args.lock}")
    print(f"rows: {len(mappings)}")


def _evaluate_one(
    row: dict[str, str],
    inputs_root: Path,
    d07_mode: str,
    generated_at: str | None,
):
    system = row["system"]
    yaml_path = Path(row["yaml_path"])
    input_dir = find_input_dir(inputs_root, system)
    requirements, requirement_warnings = load_requirements(input_dir)
    mapping, normalization_warnings = load_normalization(input_dir)
    architecture = load_architecture(yaml_path, system)
    architecture.warnings.extend(requirement_warnings)
    architecture.warnings.extend(normalization_warnings)
    canonical = canonicalize(architecture, mapping)
    graph = build_graph(canonical)
    findings = evaluate(canonical, graph, d07_mode=d07_mode, raw_text=architecture.raw_text)
    metrics, metrics_status = compute_metrics(
        canonical,
        graph,
        findings,
        requirements_count=len(requirements),
        d07_mode=d07_mode,
    )
    return {
        "row": row,
        "architecture": architecture,
        "canonical": canonical,
        "graph": graph,
        "findings": findings,
        "metrics": metrics,
        "metrics_status": metrics_status,
        "requirements": len(requirements),
        "generated_at": generated_at,
        "yaml_sha256": sha256_file(yaml_path),
    }


def _stability(records: list[dict]) -> None:
    """Fill each record with the mean Jaccard against the other runs of its cell."""
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for record in records:
        row = record["row"]
        groups[(row["system"], row["llm"], row["config"])].append(record)
    for group in groups.values():
        for record in group:
            service_values: list[float] = []
            edge_values: list[float] = []
            for other in group:
                if other is record:
                    continue
                service_values.append(
                    jaccard(
                        set(record["canonical"].services),
                        set(other["canonical"].services),
                    )
                )
                edge_values.append(jaccard(record["graph"].edges, other["graph"].edges))
            if service_values:
                record["metrics"]["estabilidade_jaccard_servicos"] = sum(service_values) / len(service_values)
                record["metrics_status"]["estabilidade_jaccard_servicos"] = "calculado"
            if edge_values:
                record["metrics"]["estabilidade_jaccard_arestas"] = sum(edge_values) / len(edge_values)
                record["metrics_status"]["estabilidade_jaccard_arestas"] = "calculado"


def _resumo_row(record: dict) -> dict[str, str]:
    row = record["row"]
    counts = {code: 0 for code in ("D03", "D04", "D05", "D06", "D07", "D11", "D12")}
    ciclo2 = 0
    for finding in record["findings"]:
        if finding.subtipo == "ciclo2":
            ciclo2 += 1
            continue
        counts[finding.codigo] = counts.get(finding.codigo, 0) + 1
    metrics = record["metrics"]
    return {
        "system": row["system"],
        "llm": row["llm"],
        "config": row["config"],
        "execution": row["execution"],
        "execution_id": row["execution_id_resolved"],
        "requirements": str(record["requirements"]),
        "services": str(len(record["canonical"].services)),
        "edges": str(len(record["graph"].edges)),
        "d03": str(counts["D03"]),
        "d04": str(counts["D04"]),
        "d05": str(counts["D05"]),
        "d06": str(counts["D06"]),
        "d07": str(counts["D07"]),
        "d11": str(counts["D11"]),
        "d12": str(counts["D12"]),
        "d04_ciclo2": str(ciclo2),
        "total_findings": str(sum(counts.values())),
        "defect_rate": "" if metrics["taxa_defeitos_por_servico"] is None else f"{metrics['taxa_defeitos_por_servico']:.6f}",
        "cycle_density": "" if metrics["densidade_ciclos"] is None else f"{metrics['densidade_ciclos']:.6f}",
        "consistency": "" if metrics["consistencia_interna"] is None else f"{metrics['consistencia_interna']:.6f}",
        "gini": "" if metrics["gini_granularidade"] is None else f"{metrics['gini_granularidade']:.6f}",
        "endpoints_per_responsibility": "" if metrics["endpoints_por_responsabilidade"] is None else f"{metrics['endpoints_por_responsabilidade']:.6f}",
        "stability_services": "" if metrics["estabilidade_jaccard_servicos"] is None else f"{metrics['estabilidade_jaccard_servicos']:.6f}",
        "stability_edges": "" if metrics["estabilidade_jaccard_arestas"] is None else f"{metrics['estabilidade_jaccard_arestas']:.6f}",
        "yaml_sha256": record["yaml_sha256"],
    }


def command_quick_check(args: argparse.Namespace) -> None:
    manifest = [
        row for row in _read_manifest(Path(args.manifest)) if row["status"] == "included"
    ]
    if args.limit:
        manifest = manifest[: args.limit]
    records = []
    for row in manifest:
        try:
            records.append(
                _evaluate_one(
                    row,
                    inputs_root=Path(args.inputs),
                    d07_mode=args.d07_mode,
                    generated_at=args.generated_at,
                )
            )
        except Exception as error:  # noqa: BLE001 - the manifest already filtered schema
            print(f"ERROR {row['system']} {row['llm']} {row['config']} {row['execution']}: {error}")
            raise
    _stability(records)
    records.sort(
        key=lambda record: (
            record["row"]["system"],
            record["row"]["llm"],
            record["row"]["config"],
            int(record["row"]["execution"]),
        )
    )
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    resumo_rows = []
    for record in records:
        row = record["row"]
        laudo = build_laudo(
            system=row["system"],
            llm=row["llm"],
            config=row["config"],
            execution=row["execution"],
            execution_id=row["execution_id_resolved"],
            architecture=record["architecture"],
            canonical=record["canonical"],
            graph=record["graph"],
            findings=record["findings"],
            metrics=record["metrics"],
            metrics_status=record["metrics_status"],
            requirements_count=record["requirements"],
            d07_mode=args.d07_mode,
            yaml_sha256=record["yaml_sha256"],
            generated_at=record["generated_at"],
        )
        target = (
            out_root
            / _safe(row["system"])
            / _safe(row["llm"])
            / _safe(row["config"])
            / f"run_{_safe(row['execution'])}.json"
        )
        write_json(target, laudo)
        write_markdown(target.with_suffix(".md"), laudo)
        resumo_rows.append(_resumo_row(record))

    resumo_path = Path(args.resumo)
    resumo_path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(resumo_rows[0].keys()) if resumo_rows else []
    with resumo_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(resumo_rows)
    print(f"laudos: {len(records)}")
    print(f"resumo: {resumo_path}")


def command_report(args: argparse.Namespace) -> None:
    from .analysis import run_analysis

    run_analysis(
        resumo_path=Path(args.resumo),
        data_csv=Path(args.data),
        out_dir=Path(args.out),
        n_boot=args.n_boot,
        seed=args.seed,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="via", description="VIA verifier")
    subparsers = parser.add_subparsers(dest="command", required=True)

    manifest = subparsers.add_parser("manifest", help="scan the corpus and resolve run directories")
    manifest.add_argument("--data", required=True)
    manifest.add_argument("--result", required=True)
    manifest.add_argument("--manifest", required=True)
    manifest.add_argument("--mapping", required=True)
    manifest.add_argument("--lock", required=True)
    manifest.set_defaults(func=command_manifest)

    quick = subparsers.add_parser("quick-check", help="run the automatic rules over the manifest")
    quick.add_argument("--manifest", required=True)
    quick.add_argument("--inputs", required=True)
    quick.add_argument("--out", required=True)
    quick.add_argument("--resumo", required=True)
    quick.add_argument("--d07-mode", choices=("auto", "not_applicable"), default=DEFAULT_D07_MODE)
    quick.add_argument("--limit", type=int, default=0)
    quick.add_argument("--generated-at", default=None)
    quick.set_defaults(func=command_quick_check)

    report = subparsers.add_parser("report", help="analyse the laudos and write tables and figures")
    report.add_argument("--resumo", required=True)
    report.add_argument("--data", required=True)
    report.add_argument("--out", required=True)
    report.add_argument("--n-boot", type=int, default=10000)
    report.add_argument("--seed", type=int, default=42)
    report.set_defaults(func=command_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
