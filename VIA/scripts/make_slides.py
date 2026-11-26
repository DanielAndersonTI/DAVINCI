"""Build the five-slide deck for the ISE workshop.

Numbers are read from the analysis CSVs so the slides stay tied to the verdicts.
Run from the VIA directory:

    python scripts/make_slides.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu

BASE = Path(__file__).resolve().parents[1]
REL = BASE / "reports"
OUT = REL / "Slides-2026-11-27.pptx"
ASSETS = REL / "slides-assets"

sys.path.insert(0, str(BASE))
from via.figures import slide_prevalence  # noqa: E402

SURFACE = RGBColor(0xFC, 0xFC, 0xFB)
INK = RGBColor(0x0B, 0x0B, 0x0B)
SECONDARY = RGBColor(0x52, 0x51, 0x4E)
MUTED = RGBColor(0x89, 0x87, 0x81)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
BLUE_LIGHT = RGBColor(0xE8, 0xF1, 0xFC)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
RULE = RGBColor(0xE1, 0xE0, 0xD9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

FONT = "Segoe UI"
WIDTH = Inches(13.333)
HEIGHT = Inches(7.5)
MARGIN = Inches(0.7)


def read_csv(name: str) -> list[dict[str, str]]:
    with (REL / "quick-check-v1" / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def pt(value: str | float, digits: int = 2, sign: bool = False) -> str:
    number = float(value)
    text = f"{number:+.{digits}f}" if sign else f"{number:.{digits}f}"
    return text.replace(".", ",")


def add_slide(prs: Presentation) -> object:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = SURFACE
    return slide


def add_rule(slide, top: float, left: float = 0.7, width: float = 11.93, color=RULE) -> None:
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Emu(9525))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def add_text(
    slide,
    text: str,
    left: float,
    top: float,
    width: float,
    height: float,
    size: int = 18,
    color=INK,
    bold: bool = False,
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.TOP,
    italic: bool = False,
    spacing: float = 1.0,
):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = 0
    frame.margin_right = 0
    frame.margin_top = 0
    frame.margin_bottom = 0
    frame.vertical_anchor = anchor
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    paragraph.line_spacing = spacing
    run = paragraph.add_run()
    run.text = text
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return box


def add_title(slide, title: str, subtitle: str = "", number: int | None = None) -> None:
    add_text(slide, title, 0.7, 0.5, 11.9, 0.9, size=30, bold=True)
    if subtitle:
        add_text(slide, subtitle, 0.7, 1.33, 11.9, 0.62, size=15, color=SECONDARY)
    add_rule(slide, 2.02)
    if number is not None:
        add_text(slide, f"{number}/5", 12.15, 7.05, 0.5, 0.3, size=10, color=MUTED, align=PP_ALIGN.RIGHT)


def add_bullets(slide, items: list[tuple[str, str]], left: float, top: float, width: float, height: float) -> None:
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    frame = box.text_frame
    frame.word_wrap = True
    frame.margin_left = 0
    frame.margin_right = 0
    frame.margin_top = 0
    frame.margin_bottom = 0
    for index, (headline, detail) in enumerate(items):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.space_after = Pt(14 if detail else 6)
        run = paragraph.add_run()
        run.text = headline
        run.font.name = FONT
        run.font.size = Pt(20)
        run.font.bold = True
        run.font.color.rgb = INK
        if detail:
            detail_paragraph = frame.add_paragraph()
            detail_paragraph.space_after = Pt(16)
            run = detail_paragraph.add_run()
            run.text = detail
            run.font.name = FONT
            run.font.size = Pt(14)
            run.font.color.rgb = SECONDARY


def add_callout(slide, headline: str, detail: str, left: float, top: float, width: float, height: float, accent=BLUE) -> None:
    shape = slide.shapes.add_shape(5, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = BLUE_LIGHT
    shape.line.fill.background()
    bar = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(0.06), Inches(height))
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent
    bar.line.fill.background()
    add_text(slide, headline, left + 0.22, top + 0.16, width - 0.4, 0.5, size=18, bold=True, color=INK)
    add_text(slide, detail, left + 0.22, top + 0.68, width - 0.4, height - 0.8, size=13, color=SECONDARY)


def add_figure(slide, path: Path, left: float, top: float, width: float) -> None:
    slide.shapes.add_picture(str(path), Inches(left), Inches(top), width=Inches(width))


def add_table(slide, rows: list[list[str]], left: float, top: float, width: float, height: float, highlight: set[tuple[int, int]] | None = None) -> None:
    shape = slide.shapes.add_table(len(rows), len(rows[0]), Inches(left), Inches(top), Inches(width), Inches(height))
    table = shape.table
    highlight = highlight or set()
    for row_index, row in enumerate(rows):
        for column_index, value in enumerate(row):
            cell = table.cell(row_index, column_index)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if row_index == 0:
                cell.fill.fore_color.rgb = BLUE
            elif (row_index, column_index) in highlight:
                cell.fill.fore_color.rgb = BLUE_LIGHT
            else:
                cell.fill.fore_color.rgb = WHITE
            frame = cell.text_frame
            frame.word_wrap = True
            paragraph = frame.paragraphs[0]
            paragraph.alignment = PP_ALIGN.LEFT if column_index == 0 else PP_ALIGN.CENTER
            run = paragraph.add_run()
            run.text = value
            run.font.name = FONT
            run.font.size = Pt(14)
            run.font.bold = row_index == 0
            run.font.color.rgb = WHITE if row_index == 0 else INK


def add_notes(slide, text: str) -> None:
    slide.notes_slide.notes_text_frame.text = text


def build() -> None:
    prevalencia_rows = read_csv("prevalence.csv")
    prevalencia = {row["codigo"]: row for row in prevalencia_rows}
    modelos = {row["llm"]: row for row in read_csv("by_model.csv")}
    configs = {row["config"]: row for row in read_csv("by_config.csv")}
    contrastes = {row["hipotese"]: row for row in read_csv("contrasts.csv")}
    exploratorios = {row["codigo"]: row for row in read_csv("exploratory_contrasts.csv")}

    ASSETS.mkdir(parents=True, exist_ok=True)
    figure_prevalence = ASSETS / "fig1_prevalence_plain.png"
    slide_prevalence(prevalencia_rows, figure_prevalence)

    prs = Presentation()
    prs.slide_width = WIDTH
    prs.slide_height = HEIGHT

    # Slide 1 -----------------------------------------------------------------
    slide = add_slide(prs)
    add_text(slide, "Integridade arquitetural", 0.7, 1.15, 11.5, 0.9, size=44, bold=True)
    add_text(slide, "além do F1", 0.7, 1.95, 11.5, 0.9, size=44, bold=True, color=BLUE)
    add_text(
        slide,
        "O que 356 decomposições automáticas revelam sobre a qualidade das ligações entre serviços",
        0.7,
        3.05,
        10.8,
        0.8,
        size=20,
        color=SECONDARY,
    )
    add_text(
        slide,
        "Oito sistemas Java foram decompostos em microserviços por três modelos de linguagem, em cinco configurações de pipeline.",
        0.7,
        3.85,
        11.2,
        0.6,
        size=14,
        color=MUTED,
    )
    add_rule(slide, 4.7, color=BLUE)
    add_text(slide, "Daniel Anderson · Computação · UFCG", 0.7, 4.95, 8.0, 0.4, size=15, color=INK)
    add_text(slide, "Workshop ISE · 27 de novembro de 2026", 0.7, 5.35, 8.0, 0.4, size=13, color=MUTED)
    add_text(slide, "356 artefatos   ·   8 sistemas   ·   3 modelos   ·   5 configurações", 0.7, 6.4, 11.5, 0.4, size=12, color=MUTED)
    add_notes(
        slide,
        "45 s. O F1 é a métrica padrão para comparar uma decomposição com a referência. Ele mede a concordância das ligações. "
        "A pergunta desta apresentação é o que fica de fora quando o grafo é internamente inconsistente.",
    )

    # Slide 2 -----------------------------------------------------------------
    slide = add_slide(prs)
    add_title(
        slide,
        "O F1 mede fidelidade. Não mede integridade.",
        "O F1 compara as ligações propostas com as da referência. Ele não verifica se o conjunto faz sentido.",
        2,
    )
    add_bullets(
        slide,
        [
            (
                "Ciclos entre serviços",
                f"{pt(float(prevalencia['D04']['share_artefatos']) * 100, 1)}% dos artefatos têm ao menos um ciclo. "
                "Um serviço depende de outro que, direta ou indiretamente, depende do primeiro.",
            ),
            (
                "Ligação não resolvida",
                f"{pt(float(prevalencia['D05']['share_artefatos']) * 100, 1)}% dos artefatos citam um serviço que não existe. "
                f"São {prevalencia['D05']['achados']} ligações em {prevalencia['D05']['artefatos_com_achado']} artefatos.",
            ),
            (
                "Serviço isolado",
                f"{pt(float(prevalencia['D03']['share_artefatos']) * 100, 1)}% dos artefatos declaram um serviço que não conversa com ninguém.",
            ),
        ],
        0.7,
        2.35,
        4.9,
        3.5,
    )
    add_figure(slide, figure_prevalence, 5.7, 2.3, 6.9)
    add_text(
        slide,
        "Um ciclo pode coincidir com a referência e continuar sendo um ciclo.",
        0.7,
        6.35,
        11.8,
        0.45,
        size=19,
        bold=True,
        color=BLUE,
    )
    add_notes(
        slide,
        "60 s. Setenta e seis por cento dos artefatos têm ao menos um ciclo. Dez por cento citam um serviço inexistente, 89 ligações ao todo. "
        "Onze e meio por cento declaram um serviço sem nenhuma ligação. O F1 conta ligações certas e erradas; ele não julga a consistência do conjunto.",
    )

    # Slide 3 -----------------------------------------------------------------
    slide = add_slide(prs)
    add_title(
        slide,
        "F1 alto não garante arquitetura íntegra",
        "Correlação de postos entre F1 de interação e defeitos estruturais por serviço, dentro de cada sistema.",
        3,
    )
    add_figure(slide, REL / "quick-check-v1" / "figures" / "fig2_forest_f1_defects.png", 0.5, 2.15, 7.45)
    add_callout(
        slide,
        "Bootstrap: 5.000 reamostragens",
        "Sorteamos sistemas inteiros, com reposição, e refazemos a correlação a cada sorteio. "
        "Artefatos do mesmo sistema não são independentes, por isso o sorteio é por sistema.",
        8.2,
        2.2,
        4.45,
        1.62,
    )
    add_callout(
        slide,
        "O que ele conclui",
        "Mediana −0,08; intervalo −0,55 a 0,08. O intervalo atravessa o zero: os dados não sustentam "
        "uma relação consistente. Cinco sistemas têm sinal negativo; três, positivo.",
        8.2,
        3.95,
        4.45,
        1.55,
    )
    add_callout(
        slide,
        "Mesmo F1, outra integridade",
        f"Claude e DeepSeek empatam no F1, {pt(modelos['Claude']['f1_inter'], 3)} contra {pt(modelos['DeepSeek']['f1_inter'], 3)}. "
        f"Claude tem {pt(abs(float(exploratorios['E3']['efeito'])), 3)} menos defeitos estruturais por serviço.",
        8.2,
        5.62,
        4.45,
        1.35,
        accent=ORANGE,
    )
    add_notes(
        slide,
        "65 s. Se o F1 ordenasse a integridade, a correlação seria negativa em todos os sistemas. Não é. "
        "A mediana é -0,08, com intervalo de -0,55 a 0,08. O bootstrap refaz o cálculo em 5.000 sorteios de sistemas inteiros. "
        "Intervalo que atravessa o zero quer dizer que não há relação estável. AcmeAir chega a -0,87; JPetStore a +0,40. "
        "O contraste mais direto é Claude contra DeepSeek: F1 igual, integridade diferente.",
    )

    # Slide 4 -----------------------------------------------------------------
    slide = add_slide(prs)
    add_title(
        slide,
        "Nenhum modelo domina todas as dimensões",
        "Médias por modelo. O F1 e a integridade estrutural apontam para lados diferentes.",
        4,
    )
    rows = [["Modelo", "F1 de interação", "Defeitos por serviço", "Ciclos por serviço"]]
    for model in ("Claude", "DeepSeek", "Gemini"):
        row = modelos[model]
        rows.append(
            [
                model,
                pt(row["f1_inter"], 3),
                pt(row["structural_defect_rate"], 3),
                pt(row["cycle_density"], 3),
            ]
        )
    add_table(slide, rows, 0.7, 2.2, 11.95, 2.0, highlight={(1, 2), (2, 2), (3, 1)})
    add_callout(
        slide,
        "Claude e DeepSeek empatam no F1",
        f"{pt(modelos['Claude']['f1_inter'], 3)} contra {pt(modelos['DeepSeek']['f1_inter'], 3)}. "
        f"A integridade separa: {pt(modelos['Claude']['structural_defect_rate'], 3)} contra "
        f"{pt(modelos['DeepSeek']['structural_defect_rate'], 3)} defeitos por serviço.",
        0.7,
        4.55,
        5.8,
        1.55,
    )
    add_callout(
        slide,
        "O pipeline completo ajuda em parte",
        f"{pt(configs['C1']['structural_defect_rate'], 3)} contra {pt(configs['C0']['structural_defect_rate'], 3)} "
        "defeitos por serviço do agente único. A densidade de ciclos quase não muda: menos "
        f"{pt(abs(float(contrastes['H2']['efeito'])), 3)}.",
        6.85,
        4.55,
        5.8,
        1.55,
        accent=ORANGE,
    )
    add_text(
        slide,
        "Média de 116 a 120 artefatos por modelo. Limite: oito sistemas e regras heurísticas.",
        0.7,
        6.45,
        11.8,
        0.35,
        size=11,
        color=MUTED,
    )
    add_notes(
        slide,
        "60 s. Gemini tem o maior F1, 0,877, e taxa estrutural intermediária, 0,232. Claude e DeepSeek empatam no F1, 0,831 e 0,829, "
        "mas Claude tem 0,140 defeitos por serviço contra 0,266 de DeepSeek. Nenhum modelo vence nas duas dimensões. "
        "O pipeline completo melhora a estrutura, 0,176 contra 0,247 do agente único, e o ganho vem de menos ligações não resolvidas, não de menos ciclos.",
    )

    # Slide 5 -----------------------------------------------------------------
    slide = add_slide(prs)
    add_title(slide, "O verificador como portão de qualidade", "Determinístico, rastreável e sem modelo de linguagem nas regras.", 5)
    cards = [
        ("Mede", "Ciclos, ligações que não resolvem, serviços isolados e auto-dependências."),
        ("Aponta", "Serviço, ligação e ciclo exatos. O reparo deixa de ser reescrita às cegas."),
        ("Decide", "Severidade e prevalência por artefato. Roda em integração contínua porque é determinístico."),
    ]
    for index, (headline, detail) in enumerate(cards):
        left = 0.7 + index * 4.05
        shape = slide.shapes.add_shape(5, Inches(left), Inches(2.45), Inches(3.75), Inches(2.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = BLUE_LIGHT
        shape.line.fill.background()
        add_text(slide, headline, left + 0.25, 2.7, 3.2, 0.5, size=22, bold=True, color=BLUE)
        add_text(slide, detail, left + 0.25, 3.25, 3.2, 1.15, size=14, color=SECONDARY)
    add_text(slide, "Próximo passo: validar as regras com arquitetos e medir se o laudo melhora a reparação.", 0.7, 5.3, 11.8, 0.55, size=20, bold=True)
    add_text(
        slide,
        "O verificador não substitui o F1. Ele acrescenta o que o F1 não mede: a consistência interna do grafo declarado.",
        0.7,
        6.05,
        11.8,
        0.55,
        size=15,
        color=SECONDARY,
    )
    add_text(
        slide,
        "Limite: oito sistemas, regras heurísticas e validação humana pendente.",
        0.7,
        6.85,
        11.8,
        0.3,
        size=11,
        color=MUTED,
    )
    add_notes(
        slide,
        "60 s. A contribuição prática é um portão que reprova ciclos, ligações quebradas e serviços isolados antes da revisão humana. "
        "O laudo diz onde está o problema, então o reparo é direcionado. O limite é claro: oito sistemas, regras heurísticas e nenhuma validação com arquitetos. "
        "O próximo passo é medir se o laudo melhora a reparação.",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"slides: {OUT}")


if __name__ == "__main__":
    build()
