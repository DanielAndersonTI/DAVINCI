"""Static figures for the VIA quick-check report.

Light surface, one hue per job, thin marks and selective labels. The figures
are built with matplotlib so the report and the slides can reuse the same PNGs.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
BLUE = "#2a78d6"
ORANGE = "#eb6834"
SEQUENTIAL = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

CONFIG_ORDER = ["C0", "C1", "C2", "C3", "C4"]
MODEL_ORDER = ["Claude", "DeepSeek", "Gemini"]

PLAIN_LABELS = {
    "D03": "Serviço isolado",
    "D04": "Ciclo entre serviços",
    "D05": "Ligação não resolvida",
    "D06": "Auto-dependência",
    "D07": "Divergência de dependências",
    "D11": "Interface subespecificada",
    "D12": "Sem termo de autenticação",
}


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "font.family": "sans-serif",
            "font.sans-serif": ["Segoe UI", "DejaVu Sans", "Arial"],
            "font.size": 10,
            "axes.titlesize": 13,
            "axes.titleweight": "semibold",
            "axes.titlecolor": INK,
            "axes.labelsize": 10,
            "axes.labelcolor": INK_SECONDARY,
            "xtick.color": INK_MUTED,
            "ytick.color": INK_SECONDARY,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.edgecolor": BASELINE,
            "axes.linewidth": 0.8,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "legend.frameon": False,
            "legend.fontsize": 9,
        }
    )


def _pt(value: float, digits: int = 2) -> str:
    text = f"{value:.{digits}f}"
    return text.replace(".", ",")


def _finish(ax, grid_axis: str = "x") -> None:
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def fig_prevalencia(
    prevalencia: list[dict],
    out: Path,
    label_map: dict[str, str] | None = None,
    exclude: tuple[str, ...] = (),
    title: str = "Prevalência dos códigos automáticos",
    subtitle: str = "356 artefatos. Azul: regras estruturais. Laranja: higiene lexical (D12).",
    xlabel: str = "artefatos com ao menos um achado",
) -> None:
    rows = [row for row in prevalencia if row["codigo"] not in exclude]
    rows.sort(key=lambda row: float(row["share_artefatos"]))
    label_map = label_map or {}
    labels = [label_map.get(row["codigo"], row["codigo"]) for row in rows]
    values = [float(row["share_artefatos"]) * 100 for row in rows]
    colors = [ORANGE if row["codigo"] == "D12" else BLUE for row in rows]

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    bars = ax.barh(labels, values, height=0.55, color=colors, edgecolor=SURFACE, linewidth=1.5)
    for bar, value in zip(bars, values):
        ax.text(
            value + 1.5,
            bar.get_y() + bar.get_height() / 2,
            f"{_pt(value, 1)}%",
            va="center",
            ha="left",
            color=INK_SECONDARY,
            fontsize=9,
        )
    ax.set_xlim(0, 108)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0", "25", "50", "75", "100%"])
    ax.set_xlabel(xlabel)
    _finish(ax, "x")
    ax.set_title(title, loc="left", pad=18)
    ax.text(
        0,
        1.03,
        subtitle,
        transform=ax.transAxes,
        color=INK_SECONDARY,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


def slide_prevalence(prevalencia: list[dict], out: Path) -> None:
    """Prevalence figure for the five-slide deck.

    Uses plain-language labels. Leaves out D07 and D11: D07 does not apply to
    this corpus, and the YAML generator writes exactly one endpoint per service,
    so D11 carries no variation from the model and would mislead an audience
    that does not know the rule codes.
    """
    _style()
    fig_prevalencia(
        prevalencia,
        out,
        label_map=PLAIN_LABELS,
        exclude=("D07", "D11", "D12"),
        title="Falhas mais frequentes por artefato",
        subtitle="356 artefatos. Quatro tipos de falha estrutural no grafo declarado.",
        xlabel="artefatos com ao menos uma ocorrência",
    )


def fig_forest(per_system: list[dict], out: Path) -> None:
    rows = [
        row
        for row in per_system
        if row["metric"] == "structural_defect_rate" and row["rho"]
    ]
    rows.sort(key=lambda row: float(row["rho"]))
    systems = [row["system"] for row in rows]
    rho = [float(row["rho"]) for row in rows]
    low = [float(row["ci_low"]) for row in rows]
    high = [float(row["ci_high"]) for row in rows]
    positions = np.arange(len(rows))
    median = float(np.median(rho))
    negative = sum(1 for value in rho if value < 0)

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for y, left, right, point in zip(positions, low, high, rho):
        ax.plot([left, right], [y, y], color=BASELINE, linewidth=2.0, solid_capstyle="round", zorder=1)
        ax.plot([point], [y], marker="o", markersize=8, color=BLUE, markeredgecolor=SURFACE, markeredgewidth=2, zorder=2)
        ax.text(1.02, y, f"{point:+.2f}".replace(".", ","), transform=ax.get_yaxis_transform(),
                va="center", ha="left", color=INK_SECONDARY, fontsize=9)
    ax.axvline(0, color=BASELINE, linewidth=1.0, zorder=0)
    ax.set_yticks(positions)
    ax.set_yticklabels(systems)
    ax.set_xlim(-1, 1)
    ax.set_xticks([-1, -0.5, 0, 0.5, 1])
    ax.set_xticklabels(["−1", "−0,5", "0", "0,5", "1"])
    ax.set_xlabel("correlação de postos entre F1 das interações e defeitos estruturais por serviço")
    _finish(ax, "x")
    ax.set_title("F1 não acompanha a integridade estrutural", loc="left", pad=28)
    ax.text(
        0,
        1.06,
        f"Por sistema, com intervalo de confiança de 95% por reamostragem. Mediana {_pt(median, 2).replace('-', '−')}; "
        f"{negative} de {len(rho)} sistemas negativos.",
        transform=ax.transAxes,
        color=INK_SECONDARY,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


def fig_heatmap(por_celula: list[dict], out: Path) -> None:
    # ``por_celula`` has one row per system x model x config. The heatmap shows
    # the model x config mean, weighted by the number of artifacts in each system
    # cell, so one system cannot dominate a column.
    totals: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in por_celula:
        totals[(row["llm"], row["config"])].append(
            (float(row["defect_rate"]), int(row["n"]))
        )
    values = np.array(
        [
            [
                sum(value * n for value, n in totals[(model, config)])
                / sum(n for _value, n in totals[(model, config)])
                for config in CONFIG_ORDER
            ]
            for model in MODEL_ORDER
        ]
    )
    cmap = LinearSegmentedColormap.from_list("via_blue", SEQUENTIAL)
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    image = ax.imshow(values, cmap=cmap, aspect="auto", vmin=values.min() - 0.02, vmax=values.max() + 0.02)
    for row in range(values.shape[0]):
        for column in range(values.shape[1]):
            value = values[row, column]
            normalized = (value - image.norm.vmin) / (image.norm.vmax - image.norm.vmin)
            color = "#ffffff" if normalized > 0.55 else INK
            ax.text(column, row, _pt(value, 3), ha="center", va="center", color=color, fontsize=10)
    ax.set_xticks(np.arange(len(CONFIG_ORDER)))
    ax.set_xticklabels(CONFIG_ORDER)
    ax.set_yticks(np.arange(len(MODEL_ORDER)))
    ax.set_yticklabels(MODEL_ORDER)
    ax.set_xticks(np.arange(-0.5, len(CONFIG_ORDER), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(MODEL_ORDER), 1), minor=True)
    ax.grid(which="minor", color=SURFACE, linewidth=3)
    ax.tick_params(which="both", length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    colorbar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.02)
    colorbar.set_label("defeitos por serviço", color=INK_SECONDARY, fontsize=9)
    colorbar.outline.set_visible(False)
    colorbar.ax.tick_params(labelsize=8, length=0, colors=INK_MUTED)
    ax.set_title("Taxa média de defeitos por modelo e configuração", loc="left", pad=22)
    ax.text(
        0,
        1.04,
        "Célula é a média das execuções; Claude/C4 tem 2 artefatos por sistema, as demais 3.",
        transform=ax.transAxes,
        color=INK_SECONDARY,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


def fig_endpoints(merged: list[dict], out: Path) -> None:
    groups: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for record in merged:
        row = record["resumo"]
        if row["llm"] not in ("Gemini", "DeepSeek"):
            continue
        value = record["resumo"].get("endpoints_per_responsibility", "")
        if value in ("", None):
            continue
        groups[row["system"]][row["llm"]].append(float(value))
    systems = sorted(
        groups,
        key=lambda system: (
            np.mean(groups[system].get("Gemini", [np.nan]))
            - np.mean(groups[system].get("DeepSeek", [np.nan]))
        ),
    )
    gemini = [np.mean(groups[system]["Gemini"]) for system in systems]
    deepseek = [np.mean(groups[system]["DeepSeek"]) for system in systems]
    positions = np.arange(len(systems))

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for y, left, right in zip(positions, deepseek, gemini):
        ax.plot([left, right], [y, y], color=BASELINE, linewidth=2.0, solid_capstyle="round", zorder=1)
    ax.scatter(deepseek, positions, s=64, color=ORANGE, edgecolor=SURFACE, linewidth=2, zorder=2, label="DeepSeek")
    ax.scatter(gemini, positions, s=64, color=BLUE, edgecolor=SURFACE, linewidth=2, zorder=3, label="Gemini")
    for y, left, right in zip(positions, deepseek, gemini):
        ax.text(1.02, y, f"{right - left:+.3f}".replace(".", ","), transform=ax.get_yaxis_transform(),
                va="center", ha="left", color=INK_SECONDARY, fontsize=9)
    ax.set_yticks(positions)
    ax.set_yticklabels(systems)
    ax.set_xlabel("endpoints sugeridos por responsabilidade")
    ax.set_xlim(0, max(gemini + deepseek) * 1.28)
    _finish(ax, "x")
    ax.legend(loc="lower right", handletextpad=0.4, borderpad=0.2)
    ax.set_title("Gemini propõe mais endpoints por responsabilidade", loc="left", pad=28)
    ax.text(
        0,
        1.06,
        "Média por sistema. Diferença média +0,088 (IC 95% 0,062–0,115); 8 de 8 sistemas acima.",
        transform=ax.transAxes,
        color=INK_SECONDARY,
        fontsize=9,
    )
    fig.tight_layout()
    fig.savefig(out, dpi=200, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


def make_figures(
    merged: list[dict],
    prevalencia: list[dict],
    per_system: list[dict],
    por_celula: list[dict],
    out_dir: Path,
) -> None:
    _style()
    out_dir.mkdir(parents=True, exist_ok=True)
    fig_prevalencia(prevalencia, out_dir / "fig1_prevalence.png")
    fig_forest(per_system, out_dir / "fig2_forest_f1_defects.png")
    fig_heatmap(por_celula, out_dir / "fig3_heatmap_model_config.png")
    fig_endpoints(merged, out_dir / "fig4_endpoints_model.png")
