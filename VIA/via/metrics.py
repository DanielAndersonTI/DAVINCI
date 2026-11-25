"""Derived metrics and small statistical helpers.

The nine metrics follow Section 6 of the VIA specification. Metrics that need
semantic adjudication are returned as ``None`` with an explicit status, never
as a fabricated number.
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np

from .graph import GraphData
from .io.loader import CanonicalArchitecture
from .rules.automatic import Finding, automatic_counts


def gini(values: list[int]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    total = sum(ordered)
    if total == 0:
        return 0.0
    size = len(ordered)
    cumulative = sum((index + 1) * value for index, value in enumerate(ordered))
    return (2 * cumulative) / (size * total) - (size + 1) / size


def jaccard(left: set, right: set) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 1.0
    return len(left & right) / len(union)


def spearman(x: list[float], y: list[float]) -> float | None:
    pairs = [
        (float(a), float(b))
        for a, b in zip(x, y)
        if a is not None and b is not None and not math.isnan(float(a)) and not math.isnan(float(b))
    ]
    if len(pairs) < 3:
        return None
    xs = _average_ranks([pair[0] for pair in pairs])
    ys = _average_ranks([pair[1] for pair in pairs])
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((a - mean_x) * (b - mean_y) for a, b in zip(xs, ys))
    denominator = math.sqrt(
        sum((a - mean_x) ** 2 for a in xs) * sum((b - mean_y) ** 2 for b in ys)
    )
    if denominator == 0:
        return None
    return numerator / denominator


def _average_ranks(values: list[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda index: values[index])
    ranks = [0.0] * len(values)
    position = 0
    while position < len(order):
        end = position
        while end + 1 < len(order) and values[order[end + 1]] == values[order[position]]:
            end += 1
        average = (position + end) / 2 + 1
        for index in order[position : end + 1]:
            ranks[index] = average
        position = end + 1
    return ranks


def bootstrap_spearman(
    x: list[float], y: list[float], n_boot: int = 10000, seed: int = 42
) -> tuple[float | None, float | None, float | None]:
    pairs = [
        (float(a), float(b))
        for a, b in zip(x, y)
        if a is not None and b is not None and not math.isnan(float(a)) and not math.isnan(float(b))
    ]
    if len(pairs) < 4:
        return None, None, None
    point = spearman([pair[0] for pair in pairs], [pair[1] for pair in pairs])
    if point is None:
        return None, None, None
    rng = np.random.default_rng(seed)
    values = np.asarray(pairs, dtype=float)
    estimates: list[float] = []
    for _ in range(n_boot):
        sample = values[rng.integers(0, len(values), len(values))]
        estimate = spearman(sample[:, 0].tolist(), sample[:, 1].tolist())
        if estimate is not None:
            estimates.append(estimate)
    if not estimates:
        return point, None, None
    low, high = np.percentile(estimates, [2.5, 97.5])
    return point, float(low), float(high)


def bootstrap_mean(
    values: list[float], n_boot: int = 10000, seed: int = 42
) -> tuple[float | None, float | None, float | None]:
    clean = [float(value) for value in values if value is not None and not math.isnan(float(value))]
    if not clean:
        return None, None, None
    point = sum(clean) / len(clean)
    if len(clean) < 2:
        return point, None, None
    rng = np.random.default_rng(seed)
    array = np.asarray(clean, dtype=float)
    estimates = [
        float(sample.mean()) for sample in (array[rng.integers(0, len(array), len(array))] for _ in range(n_boot))
    ]
    low, high = np.percentile(estimates, [2.5, 97.5])
    return point, float(low), float(high)


def bootstrap_difference(
    left: list[float], right: list[float], n_boot: int = 10000, seed: int = 42
) -> tuple[float | None, float | None, float | None]:
    left_clean = [float(value) for value in left if value is not None and not math.isnan(float(value))]
    right_clean = [float(value) for value in right if value is not None and not math.isnan(float(value))]
    if not left_clean or not right_clean:
        return None, None, None
    point = sum(left_clean) / len(left_clean) - sum(right_clean) / len(right_clean)
    rng = np.random.default_rng(seed)
    left_array = np.asarray(left_clean, dtype=float)
    right_array = np.asarray(right_clean, dtype=float)
    estimates = []
    for _ in range(n_boot):
        sample_left = left_array[rng.integers(0, len(left_array), len(left_array))]
        sample_right = right_array[rng.integers(0, len(right_array), len(right_array))]
        estimates.append(float(sample_left.mean() - sample_right.mean()))
    low, high = np.percentile(estimates, [2.5, 97.5])
    return point, float(low), float(high)


def compute_metrics(
    canonical: CanonicalArchitecture,
    graph: GraphData,
    findings: list[Finding],
    requirements_count: int,
    d07_mode: str = "auto",
    stability_services: float | None = None,
    stability_edges: float | None = None,
) -> tuple[dict[str, float | None], dict[str, str]]:
    counts = automatic_counts(findings)
    service_count = len(graph.declared)
    edge_count = len(graph.edges)
    responsibilities = [len(service.responsibilities) for service in canonical.services.values()]
    total_responsibilities = sum(responsibilities)
    total_endpoints = sum(len(service.endpoints) for service in canonical.services.values())

    included_codes = ["D03", "D04", "D05", "D06", "D11", "D12"]
    if d07_mode == "auto":
        included_codes.append("D07")
    defect_count = sum(counts.get(code, 0) for code in included_codes)

    metrics: dict[str, float | None] = {
        "cobertura_requisitos": None,
        "precisao_servicos": None,
        "densidade_ciclos": (counts.get("D04", 0) / service_count) if service_count else None,
        "consistencia_interna": (
            1 - counts.get("D07", 0) / edge_count
            if d07_mode == "auto" and edge_count
            else None
        ),
        "conflitos_de_posse": None,
        "gini_granularidade": gini(responsibilities),
        "endpoints_por_responsabilidade": (
            total_endpoints / total_responsibilities if total_responsibilities else None
        ),
        "estabilidade_jaccard_servicos": stability_services,
        "estabilidade_jaccard_arestas": stability_edges,
        "taxa_defeitos_por_servico": (defect_count / service_count) if service_count else None,
    }
    status = {
        "cobertura_requisitos": "semiautomatico_nao_executado",
        "precisao_servicos": "semiautomatico_nao_executado",
        "densidade_ciclos": "calculado",
        "consistencia_interna": (
            "calculado" if d07_mode == "auto" and edge_count else "d07_nao_aplicavel"
        ),
        "conflitos_de_posse": "semiautomatico_nao_executado",
        "gini_granularidade": "calculado",
        "endpoints_por_responsabilidade": (
            "calculado" if total_responsibilities else "sem_responsabilidades"
        ),
        "estabilidade_jaccard_servicos": (
            "calculado" if stability_services is not None else "celula_sem_par"
        ),
        "estabilidade_jaccard_arestas": (
            "calculado" if stability_edges is not None else "celula_sem_par"
        ),
        "taxa_defeitos_por_servico": "calculado",
    }
    return metrics, status


def finding_counts(findings: list[Finding]) -> dict[str, int]:
    counts = Counter(
        finding.codigo for finding in findings if finding.subtipo != "ciclo2"
    )
    return dict(sorted(counts.items()))
