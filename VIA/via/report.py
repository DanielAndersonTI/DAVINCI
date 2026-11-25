"""Laudo emission in JSON and Markdown."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .graph import GraphData
from .io.loader import Architecture, CanonicalArchitecture
from .metrics import finding_counts
from .rules.automatic import Finding


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_laudo(
    system: str,
    llm: str,
    config: str,
    execution: str,
    execution_id: str,
    architecture: Architecture,
    canonical: CanonicalArchitecture,
    graph: GraphData,
    findings: list[Finding],
    metrics: dict[str, float | None],
    metrics_status: dict[str, str],
    requirements_count: int,
    d07_mode: str,
    yaml_sha256: str,
    generated_at: str | None = None,
) -> dict:
    return {
        "versao_via": "1.0.0",
        "sistema": system,
        "execucao": {
            "configuracao": config,
            "modelo": llm,
            "modelo_versao": None,
            "rodada": int(execution) if str(execution).isdigit() else execution,
            "execution_id": execution_id,
            "commit_davinci": None,
            "temperatura": None,
            "max_tokens": None,
        },
        "entrada": {
            "requisitos": requirements_count,
            "servicos": len(canonical.services),
            "arestas": len(graph.edges),
            "yaml_sha256": yaml_sha256,
            "schema": architecture.schema,
            "duplicatas_normalizadas": canonical.duplicate_names,
        },
        "achados": [finding.to_dict() for finding in findings],
        "descartados": [],
        "metricas": {
            key: (round(value, 6) if isinstance(value, float) else value)
            for key, value in metrics.items()
        },
        "metricas_status": metrics_status,
        "contagens": finding_counts(findings),
        "d07_status": "not_applicable" if d07_mode != "auto" else "computed",
        "avisos": architecture.warnings + canonical.warnings,
        "gerado_em": generated_at or now_iso(),
    }


def write_json(path: Path, laudo: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(laudo, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _metric(value: float | None) -> str:
    if value is None:
        return "n/d"
    return f"{value:.4f}"


def write_markdown(path: Path, laudo: dict) -> None:
    execution = laudo["execucao"]
    lines = [
        f"# Laudo VIA — {laudo['sistema']}",
        "",
        f"**Modelo:** {execution['modelo']}  ",
        f"**Configuracao:** {execution['configuracao']}  ",
        f"**Rodada:** {execution['rodada']}  ",
        f"**Execucao:** `{execution['execution_id']}`",
        "",
        "## Entrada",
        "",
        "| Item | Valor |",
        "|---|---:|",
        f"| Requisitos | {laudo['entrada']['requisitos']} |",
        f"| Servicos | {laudo['entrada']['servicos']} |",
        f"| Arestas | {laudo['entrada']['arestas']} |",
        f"| Schema | {laudo['entrada']['schema']} |",
        "",
        "## Metricas",
        "",
        "| Metrica | Valor | Status |",
        "|---|---:|---|",
    ]
    for key, value in laudo["metricas"].items():
        status = laudo["metricas_status"].get(key, "")
        lines.append(f"| {key} | {_metric(value)} | {status} |")
    lines.extend(["", "## Achados", ""])
    if laudo["achados"]:
        lines.extend(
            [
                "| ID | Codigo | Severidade | Elementos | Evidencia |",
                "|---|---|---|---|---|",
            ]
        )
        for finding in laudo["achados"]:
            elements = ", ".join(finding["elementos"]) or "artefato inteiro"
            evidence = finding["evidencia"].replace("|", "/")
            lines.append(
                f"| {finding['id']} | {finding['codigo']} | {finding['severidade']} | {elements} | {evidence} |"
            )
    else:
        lines.append("Nenhum achado automatico.")
    if laudo.get("avisos"):
        lines.extend(["", "## Avisos", ""])
        for warning in laudo["avisos"]:
            lines.append(f"- {warning}")
    lines.extend(
        [
            "",
            "## Notas",
            "",
            f"- D07: {laudo['d07_status']}.",
            "- Metricas semanticas (D01, D02, D08, D09) nao executadas nesta versao.",
            "- O VIA mede integridade interna, nao qualidade global da arquitetura.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
