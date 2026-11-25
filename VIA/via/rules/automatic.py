"""Automatic VIA rules, D03 to D07 and D10 to D12.

D10 is a descriptive metric, not a finding, so it lives in ``metrics.py``.
D07 is computed but can be marked not applicable when the serialization
derives interactions from dependencies, as in the DAVINCI corpus.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field

from ..graph import GraphData
from ..io.loader import CanonicalArchitecture, strip_accents

SEVERITY = {
    "D03": "baixa",
    "D04": "alta",
    "D05": "alta",
    "D06": "media",
    "D07": "media",
    "D11": "media",
    "D12": "baixa",
}

FAMILY = {
    "D03": "completude",
    "D04": "coerencia",
    "D05": "coerencia",
    "D06": "coerencia",
    "D07": "coerencia",
    "D11": "interface",
    "D12": "interface",
}

REPAIRABLE_BY_REMOVAL = {
    "D03": False,
    "D04": False,
    "D05": False,
    "D06": True,
    "D07": False,
    "D11": False,
    "D12": False,
}

AUTH_TERMS = (
    "autentica",
    "authentic",
    "autoriza",
    "authoriz",
    "login",
    "token",
    "credencial",
    "credential",
    "password",
    "senha",
    "session",
    "sessao",
)


@dataclass
class Finding:
    codigo: str
    elementos: list[str]
    evidencia: str
    subtipo: str | None = None
    valor: float | None = None
    confirmado: bool = True
    nota: str = ""
    identificador: str = ""

    @property
    def severidade(self) -> str:
        return SEVERITY[self.codigo]

    @property
    def familia(self) -> str:
        return FAMILY[self.codigo]

    @property
    def reparavel_por_remocao(self) -> bool:
        return REPAIRABLE_BY_REMOVAL[self.codigo]

    def to_dict(self) -> dict:
        value = {
            "id": self.identificador,
            "codigo": self.codigo,
            "severidade": self.severidade,
            "familia": self.familia,
            "elementos": self.elementos,
            "evidencia": self.evidencia,
            "origem": "automatica",
            "confirmado": self.confirmado,
            "reparavel_por_remocao": self.reparavel_por_remocao,
        }
        if self.subtipo:
            value["subtipo"] = self.subtipo
        if self.valor is not None:
            value["valor"] = round(float(self.valor), 6)
        if self.nota:
            value["nota"] = self.nota
        return value


def _add(findings: list[Finding], codigo: str, elementos: list[str], evidencia: str, **kwargs) -> None:
    findings.append(Finding(codigo=codigo, elementos=elementos, evidencia=evidencia, **kwargs))


def evaluate(
    canonical: CanonicalArchitecture,
    graph: GraphData,
    d07_mode: str = "auto",
    raw_text: str = "",
) -> list[Finding]:
    """Run the automatic rules in a fixed order.

    The order is part of the contract: it makes finding identifiers stable
    across runs.
    """
    findings: list[Finding] = []

    # D03: isolated service. Degree counts every declared edge, including a
    # dangling target, because the service still participates in a relation.
    for name in sorted(graph.declared):
        if graph.degree(name) == 0:
            _add(
                findings,
                "D03",
                [name],
                "grau de entrada 0 e grau de saida 0",
            )

    # D04: strongly connected components of size two or more. A two-node cycle
    # is also reported as a subtype because it is the most severe form.
    for component in graph.components():
        _add(
            findings,
            "D04",
            component,
            f"componente fortemente conexa com {len(component)} servicos",
        )
    for pair in graph.mutual_pairs():
        _add(
            findings,
            "D04",
            list(pair),
            f"{pair[0]} -> {pair[1]}; {pair[1]} -> {pair[0]}",
            subtipo="ciclo2",
        )

    # D05: endpoint that does not resolve to a declared service.
    for source, target in sorted(graph.edges):
        missing = []
        if source not in graph.declared:
            missing.append(source)
        if target not in graph.declared:
            missing.append(target)
        if missing:
            _add(
                findings,
                "D05",
                [source, target],
                "nome nao resolvido: " + ", ".join(missing),
            )

    # D06: self-dependency, one finding per node even if both a dependency and
    # an interaction repeat the edge.
    self_loops = sorted({source for source, target in graph.edges if source == target})
    for name in self_loops:
        _add(findings, "D06", [name], f"{name} -> {name}")

    # D07: symmetric difference between unordered dependency and interaction
    # pairs. In DAVINCI the interactions are derived from dependencies, so the
    # caller may mark this rule not applicable.
    dependency_pairs = {tuple(sorted(edge)) for edge in graph.dependencies}
    interaction_pairs = {tuple(sorted(edge)) for edge in graph.interactions}
    for pair in sorted(dependency_pairs ^ interaction_pairs):
        only_dependency = pair in dependency_pairs
        origin = "dependencia" if only_dependency else "interacao"
        _add(
            findings,
            "D07",
            list(pair),
            f"par presente apenas na lista de {origin}",
            confirmado=(d07_mode == "auto"),
            nota="" if d07_mode == "auto" else "interacoes derivadas das dependencias no corpus",
        )

    # D11: generic interface, endpoint-to-responsibility ratio.
    for name, service in sorted(canonical.services.items()):
        responsibilities = len(service.responsibilities)
        endpoints = len(service.endpoints)
        ratio = endpoints / max(1, responsibilities)
        if ratio < 0.5 or (responsibilities > 3 and endpoints == 1):
            _add(
                findings,
                "D11",
                [name],
                f"{endpoints} endpoint(s) para {responsibilities} responsabilidade(s)",
                valor=ratio,
            )

    # D12: no lexical mention of authentication or authorization anywhere.
    text = strip_accents(raw_text.lower())
    if not any(term in text for term in AUTH_TERMS):
        _add(
            findings,
            "D12",
            [],
            "nenhuma mencao a autenticacao ou autorizacao no artefato",
        )

    counters: dict[str, int] = defaultdict(int)
    for finding in findings:
        counters[finding.codigo] += 1
        finding.identificador = f"{finding.codigo}-{counters[finding.codigo]:03d}"
    return findings


def automatic_counts(findings: list[Finding]) -> dict[str, int]:
    """Count findings by code, excluding the D04 two-cycle subtype.

    The subtype is evidence for the D04 component, not a second defect.
    """
    counts: dict[str, int] = defaultdict(int)
    for finding in findings:
        if finding.subtipo == "ciclo2":
            continue
        counts[finding.codigo] += 1
    return dict(counts)
