from via.graph import build_graph
from via.io.loader import Architecture, Service, canonicalize
from via.rules.automatic import automatic_counts, evaluate


def make_architecture(
    services: list[dict],
    interactions: list[tuple[str, str]] | None = None,
    raw_text: str = "authentication required",
) -> Architecture:
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


def findings_for(architecture: Architecture, mode: str = "auto"):
    canonical = canonicalize(architecture, {})
    graph = build_graph(canonical)
    return evaluate(canonical, graph, d07_mode=mode, raw_text=architecture.raw_text)


def codes(findings) -> list[str]:
    return [finding.codigo for finding in findings]


def test_clean_architecture_has_no_findings() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "responsibilities": ["one", "two"], "dependencies": ["B"], "endpoints": ["/a", "/b"]},
            {"name": "B", "responsibilities": ["three"], "dependencies": [], "endpoints": ["/c"]},
        ],
        interactions=[("A", "B")],
        raw_text="Authentication is required.",
    )
    assert findings_for(architecture) == []


def test_d03_isolated_service() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": [], "endpoints": ["/b"]},
            {"name": "C", "dependencies": [], "endpoints": ["/c"]},
        ],
        interactions=[("A", "B")],
    )
    findings = findings_for(architecture)
    assert [finding.elementos for finding in findings if finding.codigo == "D03"] == [["C"]]


def test_d04_two_node_cycle_and_subtype() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": ["A"], "endpoints": ["/b"]},
        ],
        interactions=[("A", "B"), ("B", "A")],
    )
    findings = findings_for(architecture)
    d04 = [finding for finding in findings if finding.codigo == "D04"]
    assert len([finding for finding in d04 if finding.subtipo is None]) == 1
    assert len([finding for finding in d04 if finding.subtipo == "ciclo2"]) == 1
    assert automatic_counts(findings)["D04"] == 1


def test_d04_three_node_cycle_has_no_two_cycle_subtype() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": ["C"], "endpoints": ["/b"]},
            {"name": "C", "dependencies": ["A"], "endpoints": ["/c"]},
        ],
        interactions=[],
    )
    findings = findings_for(architecture)
    d04 = [finding for finding in findings if finding.codigo == "D04"]
    assert len(d04) == 1
    assert d04[0].subtipo is None
    assert len(d04[0].elementos) == 3


def test_d05_dangling_dependency_keeps_original_name() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["Database"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": [], "endpoints": ["/b"]},
        ],
        interactions=[("A", "B")],
    )
    findings = findings_for(architecture)
    d05 = [finding for finding in findings if finding.codigo == "D05"]
    assert len(d05) == 1
    assert d05[0].elementos == ["A", "Database"]
    assert "Database" in d05[0].evidencia


def test_d06_self_dependency() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["A"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": [], "endpoints": ["/b"]},
        ],
        interactions=[("A", "B")],
    )
    findings = findings_for(architecture)
    assert [finding.elementos for finding in findings if finding.codigo == "D06"] == [["A"]]


def test_d07_symmetric_difference() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": [], "endpoints": ["/b"]},
            {"name": "C", "dependencies": [], "endpoints": ["/c"]},
        ],
        interactions=[("B", "C")],
    )
    findings = findings_for(architecture)
    d07 = [finding for finding in findings if finding.codigo == "D07"]
    assert len(d07) == 2
    assert all(finding.confirmado for finding in d07)


def test_d07_not_applicable_marks_findings_unconfirmed() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": [], "endpoints": ["/b"]},
            {"name": "C", "dependencies": [], "endpoints": ["/c"]},
        ],
        interactions=[("B", "C")],
    )
    findings = findings_for(architecture, mode="not_applicable")
    d07 = [finding for finding in findings if finding.codigo == "D07"]
    assert d07
    assert all(not finding.confirmado for finding in d07)
    assert all(finding.nota for finding in d07)


def test_d11_generic_interface() -> None:
    architecture = make_architecture(
        [
            {
                "name": "A",
                "responsibilities": ["one", "two", "three", "four"],
                "dependencies": ["B"],
                "endpoints": ["/a"],
            },
            {"name": "B", "responsibilities": ["five"], "dependencies": [], "endpoints": ["/b"]},
        ],
        interactions=[("A", "B")],
    )
    findings = findings_for(architecture)
    assert [finding.elementos for finding in findings if finding.codigo == "D11"] == [["A"]]


def test_d11_ratio_of_exactly_half_is_not_a_finding() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "responsibilities": ["one", "two"], "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "responsibilities": ["three"], "dependencies": [], "endpoints": ["/b"]},
        ],
        interactions=[("A", "B")],
    )
    assert "D11" not in codes(findings_for(architecture))


def test_d11_ratio_below_half_is_a_finding_without_many_responsibilities() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "responsibilities": ["one", "two", "three"], "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "responsibilities": ["four"], "dependencies": [], "endpoints": ["/b"]},
        ],
        interactions=[("A", "B")],
    )
    d11 = [finding for finding in findings_for(architecture) if finding.codigo == "D11"]
    assert [finding.elementos for finding in d11] == [["A"]]
    assert "1 endpoint(s) para 3 responsabilidade(s)" in d11[0].evidencia


def test_d11_flags_service_without_endpoint() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "responsibilities": ["one", "two"], "dependencies": ["B"], "endpoints": []},
            {"name": "B", "responsibilities": ["three"], "dependencies": [], "endpoints": ["/b"]},
        ],
        interactions=[("A", "B")],
    )
    assert [finding.elementos for finding in findings_for(architecture) if finding.codigo == "D11"] == [["A"]]


def test_d12_absent_authentication() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": [], "endpoints": ["/b"]},
        ],
        interactions=[("A", "B")],
        raw_text="No security terms here.",
    )
    findings = findings_for(architecture)
    assert [finding.codigo for finding in findings if finding.codigo == "D12"] == ["D12"]


def test_d12_present_authentication_is_not_a_finding() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": [], "endpoints": ["/b"]},
        ],
        interactions=[("A", "B")],
        raw_text="The authentication service validates credentials.",
    )
    assert "D12" not in codes(findings_for(architecture))


def test_finding_ids_are_stable() -> None:
    architecture = make_architecture(
        [
            {"name": "A", "dependencies": ["B"], "endpoints": ["/a"]},
            {"name": "B", "dependencies": ["A"], "endpoints": ["/b"]},
            {"name": "C", "dependencies": [], "endpoints": ["/c"]},
        ],
        interactions=[("A", "B"), ("B", "A")],
    )
    first = [finding.to_dict() for finding in findings_for(architecture)]
    second = [finding.to_dict() for finding in findings_for(architecture)]
    assert first == second
    assert [item["id"] for item in first if item["codigo"] == "D03"] == ["D03-001"]
