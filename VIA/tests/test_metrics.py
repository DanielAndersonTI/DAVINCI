import math

from via.graph import build_graph
from via.io.loader import Architecture, Service, canonicalize
from via.metrics import (
    bootstrap_mean,
    bootstrap_spearman,
    compute_metrics,
    gini,
    jaccard,
    spearman,
)
from via.rules.automatic import evaluate


def make_architecture(services: list[dict], interactions=None, raw_text="authentication") -> Architecture:
    return Architecture(
        system="Demo",
        services=[
            Service(
                name=item["name"],
                responsibilities=item.get("responsibilities", []),
                dependencies=item.get("dependencies", []),
                endpoints=item.get("endpoints", []),
            )
            for item in services
        ],
        interactions=interactions or [],
        raw_text=raw_text,
    )


def test_gini_balanced_is_zero() -> None:
    assert gini([1, 1, 1, 1]) == 0.0


def test_gini_known_value() -> None:
    assert math.isclose(gini([1, 1, 1, 9]), 0.5, rel_tol=1e-9)


def test_gini_empty_is_zero() -> None:
    assert gini([]) == 0.0


def test_jaccard() -> None:
    assert math.isclose(jaccard({"a", "b"}, {"b", "c"}), 1 / 3)
    assert jaccard(set(), set()) == 1.0
    assert jaccard({"a"}, {"b"}) == 0.0


def test_spearman_perfect() -> None:
    assert math.isclose(spearman([1, 2, 3], [2, 4, 6]), 1.0, rel_tol=1e-9)


def test_spearman_requires_three_points() -> None:
    assert spearman([1, 2], [2, 4]) is None


def test_bootstrap_spearman_perfect_interval() -> None:
    point, low, high = bootstrap_spearman([1, 2, 3, 4, 5], [2, 4, 6, 8, 10], n_boot=200, seed=1)
    assert point == 1.0
    assert low is not None and high is not None
    assert low <= point <= high


def test_bootstrap_mean() -> None:
    point, low, high = bootstrap_mean([1, 2, 3, 4], n_boot=200, seed=1)
    assert point == 2.5
    assert low <= point <= high


def test_compute_metrics_excludes_d07_when_not_applicable() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "responsibilities": ["a"], "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "responsibilities": ["b"], "dependencies": ["A"], "endpoints": ["/b"]},
            {"name": "C", "responsibilities": ["c"], "dependencies": [], "endpoints": ["/c"]},
        ],
        interactions=[("A", "B"), ("B", "A")],
    )
    canonical = canonicalize(architecture, {})
    graph = build_graph(canonical)
    findings = evaluate(canonical, graph, d07_mode="not_applicable", raw_text=architecture.raw_text)
    metrics, status = compute_metrics(
        canonical,
        graph,
        findings,
        requirements_count=10,
        d07_mode="not_applicable",
        stability_services=0.5,
        stability_edges=0.25,
    )
    assert metrics["densidade_ciclos"] == 1 / 3
    assert metrics["taxa_defeitos_por_servico"] == 2 / 3
    assert metrics["consistencia_interna"] is None
    assert status["consistencia_interna"] == "d07_nao_aplicavel"
    assert metrics["gini_granularidade"] == 0.0
    assert metrics["endpoints_por_responsabilidade"] == 1.0
    assert metrics["estabilidade_jaccard_servicos"] == 0.5
    assert metrics["estabilidade_jaccard_arestas"] == 0.25
    assert metrics["cobertura_requisitos"] is None
    assert metrics["precisao_servicos"] is None
    assert metrics["conflitos_de_posse"] is None
