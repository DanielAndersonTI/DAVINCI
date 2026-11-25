import json

from via.graph import build_graph
from via.io.loader import Architecture, Service, canonicalize
from via.metrics import compute_metrics
from via.report import build_laudo
from via.rules.automatic import evaluate


def build() -> dict:
    architecture = Architecture(
        system="Demo",
        services=[
            Service("A", ["one", "two"], ["B"], ["/a"]),
            Service("B", ["three"], ["A"], ["/b"]),
            Service("C", ["four"], [], ["/c"]),
        ],
        interactions=[("A", "B"), ("B", "A")],
        raw_text="Authentication required.",
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
        stability_services=0.8,
        stability_edges=0.6,
    )
    return build_laudo(
        system="Demo",
        llm="Gemini",
        config="C1",
        execution="1",
        execution_id="20260101_000000_000000",
        architecture=architecture,
        canonical=canonical,
        graph=graph,
        findings=findings,
        metrics=metrics,
        metrics_status=status,
        requirements_count=10,
        d07_mode="not_applicable",
        yaml_sha256="abc",
        generated_at="2026-11-24T00:00:00+00:00",
    )


def test_laudo_is_byte_identical_except_the_date() -> None:
    first = json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True)
    second = json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True)
    assert first == second


def test_date_is_the_only_nondeterministic_field() -> None:
    first = build()
    second = build()
    first["gerado_em"] = "different"
    assert first != second
    first["gerado_em"] = second["gerado_em"]
    assert first == second
