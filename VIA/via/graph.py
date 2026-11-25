"""Directed graph view of an architecture."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from .io.loader import CanonicalArchitecture


@dataclass
class GraphData:
    declared: set[str]
    dependencies: set[tuple[str, str]]
    interactions: set[tuple[str, str]]
    edges: set[tuple[str, str]]
    graph: nx.DiGraph

    def degree(self, node: str) -> int:
        return int(self.graph.in_degree(node)) + int(self.graph.out_degree(node))

    def in_degree(self, node: str) -> int:
        return int(self.graph.in_degree(node))

    def out_degree(self, node: str) -> int:
        return int(self.graph.out_degree(node))

    def components(self) -> list[list[str]]:
        components = [
            sorted(component)
            for component in nx.strongly_connected_components(self.graph)
            if len(component) >= 2
        ]
        return sorted(components, key=lambda item: tuple(item))

    def mutual_pairs(self) -> list[tuple[str, str]]:
        pairs: set[tuple[str, str]] = set()
        for source, target in self.edges:
            if source != target and (target, source) in self.edges:
                pairs.add(tuple(sorted((source, target))))
        return sorted(pairs)


def build_graph(canonical: CanonicalArchitecture) -> GraphData:
    """Build the graph from dependencies and interactions.

    Endpoints that do not resolve to a declared service remain as nodes so the
    graph keeps the edge for D05. D03 only checks declared services, so an
    unresolved target never becomes a service.
    """
    graph = nx.DiGraph()
    declared = set(canonical.declared)
    edges = set(canonical.dependencies) | set(canonical.interactions)
    graph.add_nodes_from(sorted(declared))
    for source, target in sorted(edges):
        graph.add_edge(source, target)
    return GraphData(
        declared=declared,
        dependencies=set(canonical.dependencies),
        interactions=set(canonical.interactions),
        edges=edges,
        graph=graph,
    )
