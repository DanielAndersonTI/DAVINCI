"""Analysis of the VIA laudos against the previous experiment metrics.

The unit of analysis is the artifact. Correlations are computed within each
system; the pooled estimate is a cluster bootstrap over systems, reported as
descriptive because eight systems cannot support a strong pooled claim.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

from .metrics import bootstrap_spearman, spearman
from .rules.automatic import FAMILY, SEVERITY

CODES = ("D03", "D04", "D05", "D06", "D07", "D11", "D12")
CORE_METRICS = (
    "structural_defect_rate",
    "defect_rate",
    "cycle_density",
    "gini",
    "endpoints_per_responsibility",
    "stability_edges",
    "d11_share",
)


def _float(value) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _mean(values: list[float]) -> float | None:
    clean = [value for value in values if value is not None]
    if not clean:
        return None
    return sum(clean) / len(clean)


def _fmt(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fields is None:
        fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def load_rows(resumo_path: Path, data_csv: Path) -> tuple[list[dict], list[dict], int]:
    with resumo_path.open(encoding="utf-8", newline="") as handle:
        resumo = list(csv.DictReader(handle))
    with data_csv.open(encoding="utf-8-sig", newline="") as handle:
        data = list(csv.DictReader(handle))
    index = {
        (row["system"], row["llm"], row["config"], row["execution"]): row
        for row in data
    }
    merged = []
    missing = 0
    for row in resumo:
        key = (row["system"], row["llm"], row["config"], row["execution"])
        metrics_row = index.get(key)
        if metrics_row is None:
            missing += 1
            continue
        merged.append({"resumo": row, "data": metrics_row})
    return merged, data, missing


def _metric(record: dict, name: str) -> float | None:
    row = record["resumo"]
    if name == "d11_share":
        services = _float(row.get("services")) or 0
        return (_float(row.get("d11")) or 0) / services if services else None
    if name == "structural_defect_rate":
        services = _float(row.get("services")) or 0
        if not services:
            return None
        structural = sum(
            int(_float(row.get(code.lower())) or 0)
            for code in ("D03", "D04", "D05", "D06")
        )
        return structural / services
    if name == "f1_inter":
        return _f1(record)
    return _float(row.get(name))


def _f1(record: dict, column: str = "f1_inter") -> float | None:
    return _float(record["data"].get(column))


def prevalence(merged: list[dict]) -> list[dict]:
    total_services = sum(_float(record["resumo"]["services"]) or 0 for record in merged)
    rows = []
    for code in CODES:
        total = sum(int(_float(record["resumo"][code.lower()]) or 0) for record in merged)
        artifacts = sum(1 for record in merged if (int(_float(record["resumo"][code.lower()]) or 0) > 0))
        rows.append(
            {
                "codigo": code,
                "familia": FAMILY[code],
                "severidade": SEVERITY[code],
                "achados": total,
                "artefatos_com_achado": artifacts,
                "n": len(merged),
                "share_artefatos": _fmt(artifacts / len(merged) if merged else None),
                "media_por_artefato": _fmt(total / len(merged) if merged else None),
                "media_por_servico": _fmt(total / total_services if total_services else None),
            }
        )
    return rows


def group_table(merged: list[dict], key: str) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for record in merged:
        groups[record["resumo"][key]].append(record)
    rows = []
    for value in sorted(groups):
        group = groups[value]
        f1_values = [_f1(record) for record in group]
        rows.append(
            {
                key: value,
                "n": len(group),
                "structural_defect_rate": _fmt(
                    _mean([_metric(record, "structural_defect_rate") for record in group])
                ),
                "defect_rate": _fmt(_mean([_metric(record, "defect_rate") for record in group])),
                "cycle_density": _fmt(_mean([_metric(record, "cycle_density") for record in group])),
                "gini": _fmt(_mean([_metric(record, "gini") for record in group])),
                "endpoints_per_responsibility": _fmt(
                    _mean([_metric(record, "endpoints_per_responsibility") for record in group])
                ),
                "d11_share": _fmt(_mean([_metric(record, "d11_share") for record in group])),
                "stability_edges": _fmt(_mean([_metric(record, "stability_edges") for record in group])),
                "f1_inter": _fmt(_mean(f1_values)),
            }
        )
    return rows


def cell_table(merged: list[dict]) -> list[dict]:
    groups: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for record in merged:
        row = record["resumo"]
        groups[(row["system"], row["llm"], row["config"])].append(record)
    rows = []
    for (system, llm, config) in sorted(groups):
        group = groups[(system, llm, config)]
        rows.append(
            {
                "system": system,
                "llm": llm,
                "config": config,
                "n": len(group),
                "structural_defect_rate": _fmt(
                    _mean([_metric(record, "structural_defect_rate") for record in group])
                ),
                "defect_rate": _fmt(_mean([_metric(record, "defect_rate") for record in group])),
                "cycle_density": _fmt(_mean([_metric(record, "cycle_density") for record in group])),
                "endpoints_per_responsibility": _fmt(
                    _mean([_metric(record, "endpoints_per_responsibility") for record in group])
                ),
                "gini": _fmt(_mean([_metric(record, "gini") for record in group])),
                "f1_inter": _fmt(_mean([_f1(record) for record in group])),
            }
        )
    return rows


def correlations(merged: list[dict], n_boot: int, seed: int) -> list[dict]:
    systems = sorted({record["resumo"]["system"] for record in merged})
    rows = []
    for system in systems:
        group = [record for record in merged if record["resumo"]["system"] == system]
        for metric in CORE_METRICS:
            pairs = [
                (_metric(record, metric), _f1(record))
                for record in group
                if _metric(record, metric) is not None and _f1(record) is not None
            ]
            if len(pairs) < 4:
                continue
            point, low, high = bootstrap_spearman(
                [pair[0] for pair in pairs],
                [pair[1] for pair in pairs],
                n_boot=n_boot,
                seed=seed,
            )
            rows.append(
                {
                    "scope": "system",
                    "system": system,
                    "metric": metric,
                    "n": len(pairs),
                    "rho": _fmt(point),
                    "ci_low": _fmt(low),
                    "ci_high": _fmt(high),
                }
            )

    for metric in CORE_METRICS:
        pairs = [
            (_metric(record, metric), _f1(record))
            for record in merged
            if _metric(record, metric) is not None and _f1(record) is not None
        ]
        if len(pairs) < 4:
            continue
        point, low, high = bootstrap_spearman(
            [pair[0] for pair in pairs],
            [pair[1] for pair in pairs],
            n_boot=n_boot,
            seed=seed,
        )
        rows.append(
            {
                "scope": "pooled_naive",
                "system": "todos",
                "metric": metric,
                "n": len(pairs),
                "rho": _fmt(point),
                "ci_low": _fmt(low),
                "ci_high": _fmt(high),
            }
        )
    return rows


def cluster_bootstrap_spearman(merged: list[dict], metric: str, n_boot: int, seed: int) -> tuple:
    systems = sorted({record["resumo"]["system"] for record in merged})
    by_system = {
        system: [
            (_metric(record, metric), _f1(record))
            for record in merged
            if record["resumo"]["system"] == system
            and _metric(record, metric) is not None
            and _f1(record) is not None
        ]
        for system in systems
    }
    all_pairs = [pair for system in systems for pair in by_system[system]]
    point = spearman([pair[0] for pair in all_pairs], [pair[1] for pair in all_pairs])
    if point is None:
        return None, None, None
    rng = random.Random(seed)
    estimates = []
    for _ in range(n_boot):
        sample = []
        for _ in systems:
            chosen = rng.choice(systems)
            sample.extend(by_system[chosen])
        estimate = spearman([pair[0] for pair in sample], [pair[1] for pair in sample])
        if estimate is not None:
            estimates.append(estimate)
    if not estimates:
        return point, None, None
    estimates.sort()
    low = estimates[int(0.025 * len(estimates))]
    high = estimates[min(len(estimates) - 1, int(0.975 * len(estimates)))]
    return point, low, high


def _paired_units(
    merged: list[dict],
    unit_keys: tuple[str, ...],
    group_key: str,
    left: str,
    right: str,
    metric: str,
) -> list[tuple[float, float]]:
    groups: dict[tuple, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for record in merged:
        row = record["resumo"]
        group = row[group_key]
        if group not in (left, right):
            continue
        key = tuple(row[item] for item in unit_keys)
        value = _metric(record, metric)
        if value is not None:
            groups[key][group].append(value)
    units = []
    for key in sorted(groups):
        values = groups[key]
        if values.get(left) and values.get(right):
            units.append((_mean(values[left]), _mean(values[right])))
    return units


def _sign_flip_p(differences: list[float], n_perm: int, seed: int) -> float | None:
    if not differences:
        return None
    observed = abs(sum(differences) / len(differences))
    rng = random.Random(seed)
    hits = 0
    for _ in range(n_perm):
        permuted = [
            value if rng.random() < 0.5 else -value for value in differences
        ]
        if abs(sum(permuted) / len(permuted)) >= observed - 1e-12:
            hits += 1
    return (hits + 1) / (n_perm + 1)


def _holm(pvalues: list[float | None]) -> list[float | None]:
    indexed = [(value, index) for index, value in enumerate(pvalues) if value is not None]
    if not indexed:
        return [None] * len(pvalues)
    indexed.sort()
    adjusted: list[float | None] = [None] * len(pvalues)
    previous = 0.0
    total = len(indexed)
    for rank, (value, index) in enumerate(indexed):
        candidate = min(1.0, (total - rank) * value)
        previous = max(previous, candidate)
        adjusted[index] = previous
    return adjusted


def _bootstrap_median(values: list[float], n_boot: int, seed: int) -> tuple:
    if not values:
        return None, None, None
    point = sorted(values)[len(values) // 2]
    rng = random.Random(seed)
    estimates = []
    for _ in range(n_boot):
        sample = [rng.choice(values) for _ in values]
        sample.sort()
        estimates.append(sample[len(sample) // 2])
    estimates.sort()
    return point, estimates[int(0.025 * len(estimates))], estimates[int(0.975 * len(estimates))]


def _permutation_median_rho(
    merged: list[dict], metric: str, n_perm: int, seed: int
) -> float | None:
    """Permute F1 within each system and recompute the median rho.

    The permutation keeps the system-level composition and the marginal
    distributions, and breaks only the pairing between quality metric and F1.
    """
    systems = sorted({record["resumo"]["system"] for record in merged})
    by_system: dict[str, list[tuple[float, float]]] = {}
    for system in systems:
        pairs = [
            (_metric(record, metric), _f1(record))
            for record in merged
            if record["resumo"]["system"] == system
            and _metric(record, metric) is not None
            and _f1(record) is not None
        ]
        if pairs:
            by_system[system] = pairs
    if not by_system:
        return None
    observed_values = []
    for pairs in by_system.values():
        value = spearman([pair[0] for pair in pairs], [pair[1] for pair in pairs])
        if value is not None:
            observed_values.append(value)
    if not observed_values:
        return None
    observed_values.sort()
    observed = observed_values[len(observed_values) // 2]
    rng = random.Random(seed)
    hits = 0
    for _ in range(n_perm):
        permuted = []
        for pairs in by_system.values():
            xs = [pair[0] for pair in pairs]
            ys = [pair[1] for pair in pairs]
            rng.shuffle(ys)
            value = spearman(xs, ys)
            if value is not None:
                permuted.append(value)
        if not permuted:
            continue
        permuted.sort()
        if abs(permuted[len(permuted) // 2]) >= abs(observed) - 1e-12:
            hits += 1
    return (hits + 1) / (n_perm + 1)


def contrasts(merged: list[dict], per_system: list[dict], n_boot: int, seed: int) -> list[dict]:
    rows = []

    # H1: within-system association between F1 of interactions and structural
    # defect rate (D03-D06 per service). D11 and D12 are left out because D11 is
    # saturated and D12 is lexical hygiene, not architectural integrity.
    h1_values = [
        float(row["rho"])
        for row in per_system
        if row["metric"] == "structural_defect_rate" and row["rho"] not in ("", None)
    ]
    point, low, high = _bootstrap_median(h1_values, n_boot, seed)
    p_raw = _permutation_median_rho(merged, "structural_defect_rate", n_boot, seed + 4)
    negative = sum(1 for value in h1_values if value < 0)
    rows.append(
        {
            "hipotese": "H1",
            "comparacao": "rho(F1_inter, defeitos estruturais por serviço) por sistema, mediana",
            "efeito": _fmt(point),
            "ci_low": _fmt(low),
            "ci_high": _fmt(high),
            "p_raw": _fmt(p_raw),
            "p_holm": "",
            "n_unidades": len(h1_values),
            "detalhe": f"{negative} de {len(h1_values)} sistemas com rho negativo; D03-D06, sem D11/D12",
        }
    )

    # H2: cycle density, C1 minus C0, paired by system and model.
    units = _paired_units(
        merged, ("system", "llm"), "config", "C1", "C0", "cycle_density"
    )
    differences = [left - right for left, right in units]
    point = _mean(differences)
    low, high = _bootstrap_mean_difference(differences, n_boot, seed)
    p_raw = _sign_flip_p(differences, n_boot, seed + 1)
    rows.append(
        {
            "hipotese": "H2",
            "comparacao": "densidade de ciclos C1 - C0",
            "efeito": _fmt(point),
            "ci_low": _fmt(low),
            "ci_high": _fmt(high),
            "p_raw": _fmt(p_raw),
            "p_holm": "",
            "n_unidades": len(units),
            "detalhe": "unidade: sistema x modelo, media das 3 execucoes",
        }
    )

    # H3: endpoint ratio, Gemini minus DeepSeek, paired by system and config.
    units = _paired_units(
        merged,
        ("system", "config"),
        "llm",
        "Gemini",
        "DeepSeek",
        "endpoints_per_responsibility",
    )
    differences = [left - right for left, right in units]
    point = _mean(differences)
    low, high = _bootstrap_mean_difference(differences, n_boot, seed + 2)
    p_raw = _sign_flip_p(differences, n_boot, seed + 3)
    rows.append(
        {
            "hipotese": "H3",
            "comparacao": "endpoints por responsabilidade Gemini - DeepSeek",
            "efeito": _fmt(point),
            "ci_low": _fmt(low),
            "ci_high": _fmt(high),
            "p_raw": _fmt(p_raw),
            "p_holm": "",
            "n_unidades": len(units),
            "detalhe": "unidade: sistema x configuracao, media das 3 execucoes",
        }
    )

    adjusted = _holm([_float(row["p_raw"]) for row in rows])
    for row, value in zip(rows, adjusted):
        row["p_holm"] = _fmt(value)
    return rows


def _bootstrap_mean_difference(differences: list[float], n_boot: int, seed: int) -> tuple:
    if not differences:
        return None, None
    rng = random.Random(seed)
    estimates = []
    for _ in range(n_boot):
        sample = [rng.choice(differences) for _ in differences]
        estimates.append(sum(sample) / len(sample))
    estimates.sort()
    return estimates[int(0.025 * len(estimates))], estimates[int(0.975 * len(estimates))]


def exploratory_contrasts(merged: list[dict], n_boot: int, seed: int) -> list[dict]:
    """Post-hoc contrasts kept separate from the three focal hypotheses.

    They are labelled exploratory and carry raw p-values only. Two of them test
    the construct argument directly: models or configurations with the same F1
    can differ in structural defect rate.
    """
    specs = [
        ("E1", "C1 - C0, defeitos estruturais", ("system", "llm"), "config", "C1", "C0", "structural_defect_rate"),
        ("E2", "C1 - C0, F1_inter", ("system", "llm"), "config", "C1", "C0", "f1_inter"),
        ("E3", "Claude - DeepSeek, defeitos estruturais", ("system", "config"), "llm", "Claude", "DeepSeek", "structural_defect_rate"),
        ("E4", "Claude - DeepSeek, F1_inter", ("system", "config"), "llm", "Claude", "DeepSeek", "f1_inter"),
        ("E5", "Claude - Gemini, defeitos estruturais", ("system", "config"), "llm", "Claude", "Gemini", "structural_defect_rate"),
        ("E6", "Claude - Gemini, F1_inter", ("system", "config"), "llm", "Claude", "Gemini", "f1_inter"),
        ("E7", "Gemini - DeepSeek, defeitos estruturais", ("system", "config"), "llm", "Gemini", "DeepSeek", "structural_defect_rate"),
        ("E8", "Gemini - DeepSeek, F1_inter", ("system", "config"), "llm", "Gemini", "DeepSeek", "f1_inter"),
    ]
    rows = []
    for position, (identifier, label, unit_keys, group_key, left, right, metric) in enumerate(specs):
        units = _paired_units(merged, unit_keys, group_key, left, right, metric)
        differences = [first - second for first, second in units]
        point = _mean(differences)
        low, high = _bootstrap_mean_difference(differences, n_boot, seed + 20 + position * 3)
        p_raw = _sign_flip_p(differences, n_boot, seed + 21 + position * 3)
        unit_label = "sistema x modelo" if "llm" in unit_keys else "sistema x configuracao"
        rows.append(
            {
                "codigo": identifier,
                "comparacao": label,
                "efeito": _fmt(point),
                "ci_low": _fmt(low),
                "ci_high": _fmt(high),
                "p_raw": _fmt(p_raw),
                "n_unidades": len(units),
                "detalhe": f"exploratorio; p bruto; unidade: {unit_label}",
            }
        )
    return rows


def _markdown_tables(out_dir: Path, tables: dict[str, list[dict]]) -> None:
    lines = ["# Tabelas do quick-check VIA", ""]
    for title, rows in tables.items():
        lines.extend([f"## {title}", ""])
        if not rows:
            lines.extend(["Sem dados.", ""])
            continue
        fields = list(rows[0].keys())
        lines.append("| " + " | ".join(fields) + " |")
        lines.append("|" + "|".join("---" for _ in fields) + "|")
        for row in rows:
            lines.append("| " + " | ".join(str(row.get(field, "")) for field in fields) + " |")
        lines.append("")
    (out_dir / "tables.md").write_text("\n".join(lines), encoding="utf-8")


def run_analysis(
    resumo_path: Path,
    data_csv: Path,
    out_dir: Path,
    n_boot: int = 10000,
    seed: int = 42,
) -> dict:
    merged, data, missing = load_rows(resumo_path, data_csv)
    if not merged:
        raise RuntimeError("no laudo matched data.csv")
    out_dir.mkdir(parents=True, exist_ok=True)
    tables_dir = out_dir / "tables"
    figures_dir = out_dir / "figures"
    tables_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    prevalencia = prevalence(merged)
    por_modelo = group_table(merged, "llm")
    por_config = group_table(merged, "config")
    por_sistema = group_table(merged, "system")
    por_celula = cell_table(merged)
    correlacoes = correlations(merged, n_boot=min(n_boot, 5000), seed=seed)
    per_system = [row for row in correlacoes if row["scope"] == "system"]

    pooled_rows = []
    for metric in CORE_METRICS:
        point, low, high = cluster_bootstrap_spearman(
            merged, metric, n_boot=min(n_boot, 5000), seed=seed
        )
        pooled_rows.append(
            {
                "metric": metric,
                "rho": _fmt(point),
                "ci_low": _fmt(low),
                "ci_high": _fmt(high),
                "n": len(merged),
                "scope": "pooled_cluster",
            }
        )
    contrastes = contrasts(merged, per_system, n_boot=min(n_boot, 5000), seed=seed)
    exploratorios = exploratory_contrasts(merged, n_boot=min(n_boot, 5000), seed=seed)

    write_csv(out_dir / "prevalence.csv", prevalencia)
    write_csv(out_dir / "by_model.csv", por_modelo)
    write_csv(out_dir / "by_config.csv", por_config)
    write_csv(out_dir / "by_system.csv", por_sistema)
    write_csv(out_dir / "by_cell.csv", por_celula)
    write_csv(out_dir / "correlations.csv", correlacoes)
    write_csv(out_dir / "pooled_correlations.csv", pooled_rows)
    write_csv(out_dir / "contrasts.csv", contrastes)
    write_csv(out_dir / "exploratory_contrasts.csv", exploratorios)

    overview = {
        "n_artefatos": len(merged),
        "n_data_csv": len(data),
        "n_sem_par": missing,
        "sistemas": sorted({record["resumo"]["system"] for record in merged}),
        "modelos": sorted({record["resumo"]["llm"] for record in merged}),
        "configuracoes": sorted({record["resumo"]["config"] for record in merged}),
        "celulas": len({(record["resumo"]["system"], record["resumo"]["llm"], record["resumo"]["config"]) for record in merged}),
    }
    (out_dir / "overview.json").write_text(
        json.dumps(overview, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _markdown_tables(
        out_dir,
        {
            "Prevalencia por codigo": prevalencia,
            "Por modelo": por_modelo,
            "Por configuracao": por_config,
            "Por sistema": por_sistema,
            "Correlacoes por sistema": per_system,
            "Correlacoes agrupadas": pooled_rows,
            "Contrastes focais": contrastes,
            "Contrastes exploratorios": exploratorios,
        },
    )
    try:
        from .figures import make_figures

        make_figures(merged, prevalencia, per_system, por_celula, figures_dir)
    except Exception as error:  # noqa: BLE001 - figures are not allowed to break tables
        print(f"figures skipped: {error}")

    print(json.dumps(overview, ensure_ascii=False, indent=2))
    print(f"tables: {tables_dir}")
    print(f"figures: {figures_dir}")
    return overview
