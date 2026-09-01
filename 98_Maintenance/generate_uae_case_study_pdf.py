#!/usr/bin/env python3
"""Render the UAE HR analytics case-study Markdown as a polished PDF."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


NAVY = "#112A46"
TEAL = "#0D8A87"
PALE_TEAL = "#EAF7F6"
PALE_BLUE = "#EEF4FA"
INK = "#233447"
MUTED = "#60758B"
LINE = "#CBD7E3"


def clean_text(value: str) -> str:
    """Use ReportLab-safe punctuation while preserving the document meaning."""
    return (
        value.replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
        .replace("\u00d7", "x")
        .replace("\u00b7", " | ")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )


def inline_markup(value: str) -> str:
    escaped = html.escape(clean_text(value.strip()))
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<font name='Courier'>\1</font>", escaped)
    return escaped


def split_table(lines: list[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def parse_metadata(lines: list[str]) -> dict[str, str]:
    metadata = {
        "title": "UAE Workforce Planning and Total Rewards",
        "author": "Mohammad Azimuddin",
        "date": "August 2026",
    }
    if lines and lines[0].startswith("# "):
        metadata["title"] = lines[0][2:].strip()
    for line in lines[:12]:
        if line.startswith("**Author:**"):
            metadata["author"] = line.removeprefix("**Author:**").strip()
        elif line.startswith("**Date:**"):
            metadata["date"] = line.removeprefix("**Date:**").strip()
    return metadata


def build_pdf(source: Path, output: Path) -> None:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            PageBreak,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError as exc:
        raise SystemExit(
            "ReportLab is required. Install it with: uv pip install reportlab"
        ) from exc

    lines = source.read_text(encoding="utf-8").splitlines()
    metadata = parse_metadata(lines)
    output.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=13.5,
        textColor=colors.HexColor(INK),
        spaceAfter=7,
    )
    body_small = ParagraphStyle(
        "BodySmall",
        parent=body,
        fontSize=8.4,
        leading=11.4,
        textColor=colors.HexColor(MUTED),
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15.5,
        leading=19,
        textColor=colors.HexColor(NAVY),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True,
    )
    subsection_style = ParagraphStyle(
        "Subsection",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor(TEAL),
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        parent=body,
        leftIndent=13,
        firstLineIndent=-8,
        bulletIndent=1,
        spaceAfter=4.5,
    )
    number_style = ParagraphStyle(
        "Number",
        parent=body,
        leftIndent=16,
        firstLineIndent=-11,
        bulletIndent=0,
        spaceAfter=4.5,
    )
    quote_style = ParagraphStyle(
        "Quote",
        parent=body_small,
        leftIndent=9,
        rightIndent=9,
        borderColor=colors.HexColor(TEAL),
        borderWidth=0,
        borderPadding=8,
        backColor=colors.HexColor(PALE_TEAL),
        textColor=colors.HexColor(INK),
        spaceAfter=10,
    )

    def first_page(canvas, _doc):
        canvas.saveState()
        width, height = A4
        canvas.setFillColor(colors.HexColor(NAVY))
        canvas.rect(0, 0, width, height, stroke=0, fill=1)
        canvas.setFillColor(colors.HexColor(TEAL))
        canvas.rect(0, height - 8 * mm, width, 8 * mm, stroke=0, fill=1)
        canvas.restoreState()

    def later_pages(canvas, current_doc):
        canvas.saveState()
        width, height = A4
        canvas.setStrokeColor(colors.HexColor(LINE))
        canvas.setLineWidth(0.5)
        canvas.line(20 * mm, height - 15 * mm, width - 20 * mm, height - 15 * mm)
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.setFillColor(colors.HexColor(NAVY))
        canvas.drawString(
            20 * mm,
            height - 11.5 * mm,
            "UAE WORKFORCE PLANNING | SYNTHETIC CASE STUDY",
        )
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor(MUTED))
        canvas.drawRightString(
            width - 20 * mm,
            11 * mm,
            f"MOHAMMAD AZIMUDDIN  |  {current_doc.page}",
        )
        canvas.restoreState()

    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=21 * mm,
        bottomMargin=18 * mm,
        title=clean_text(metadata["title"]),
        author=clean_text(metadata["author"]),
        subject="Independent synthetic HR analytics portfolio case study",
    )

    cover_eyebrow = ParagraphStyle(
        "CoverEyebrow",
        parent=body,
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#75D6D1"),
        alignment=TA_LEFT,
    )
    cover_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=31,
        leading=35,
        textColor=colors.white,
        alignment=TA_LEFT,
        spaceAfter=12,
    )
    cover_subtitle = ParagraphStyle(
        "CoverSubtitle",
        parent=body,
        fontSize=14,
        leading=20,
        textColor=colors.HexColor("#D9E7F3"),
        spaceAfter=24,
    )
    cover_meta = ParagraphStyle(
        "CoverMeta",
        parent=body,
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#D9E7F3"),
    )
    cover_note = ParagraphStyle(
        "CoverNote",
        parent=body,
        fontSize=9.5,
        leading=14,
        textColor=colors.white,
        borderColor=colors.HexColor("#3A5A76"),
        borderWidth=0.8,
        borderPadding=10,
        backColor=colors.HexColor("#193955"),
    )

    story = [
        Spacer(1, 28 * mm),
        Paragraph("INDEPENDENT HR ANALYTICS PORTFOLIO CASE", cover_eyebrow),
        Spacer(1, 5 * mm),
        Paragraph(inline_markup(metadata["title"]), cover_title),
        Paragraph(
            "A decision-focused case connecting workforce planning, total rewards, recruitment, and scenario modelling.",
            cover_subtitle,
        ),
        Spacer(1, 8 * mm),
        Paragraph(
            f"<b>{inline_markup(metadata['author'])}</b><br/>{inline_markup(metadata['date'])}",
            cover_meta,
        ),
        Spacer(1, 27 * mm),
        Paragraph(
            "<b>SYNTHETIC DATA DISCLOSURE</b><br/>All company, employee, salary, recruitment, and scenario data in this document is fictional. Results demonstrate an analytical process, not employer outcomes or UAE market benchmarks.",
            cover_note,
        ),
        PageBreak(),
    ]

    body_start = next(
        (index for index, line in enumerate(lines) if line.startswith("## Business question")),
        0,
    )
    content = lines[body_start:]
    index = 0
    paragraph_buffer: list[str] = []

    def flush_paragraph() -> None:
        if paragraph_buffer:
            text = " ".join(part.strip() for part in paragraph_buffer)
            if text.startswith("These findings are descriptive."):
                story.append(PageBreak())
                story.append(Paragraph(inline_markup(text), quote_style))
            else:
                story.append(Paragraph(inline_markup(text), body))
            paragraph_buffer.clear()

    while index < len(content):
        line = content[index].rstrip()

        if not line:
            flush_paragraph()
            index += 1
            continue

        if line.startswith("## "):
            flush_paragraph()
            heading = line[3:].strip()
            if heading == "Recommendation":
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(heading), section_style))
            index += 1
            continue

        if line.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[4:]), subsection_style))
            index += 1
            continue

        if line.startswith("> "):
            flush_paragraph()
            story.append(Paragraph(inline_markup(line[2:]), quote_style))
            index += 1
            continue

        if line.startswith("|"):
            flush_paragraph()
            table_lines = []
            while index < len(content) and content[index].strip().startswith("|"):
                table_lines.append(content[index].strip())
                index += 1
            rows = split_table(table_lines)
            if rows:
                column_count = len(rows[0])
                if column_count == 2:
                    widths = [102 * mm, 48 * mm]
                elif column_count == 5:
                    widths = [42 * mm, 25 * mm, 30 * mm, 34 * mm, 29 * mm]
                else:
                    widths = [160 * mm / column_count] * column_count

                header_style = ParagraphStyle(
                    "TableHeader",
                    parent=body_small,
                    fontName="Helvetica-Bold",
                    textColor=colors.white,
                    alignment=TA_LEFT,
                )
                table_data = [
                    [
                        Paragraph(
                            inline_markup(cell),
                            body_small if row_number else header_style,
                        )
                        for cell in row
                    ]
                    for row_number, row in enumerate(rows)
                ]
                table = Table(
                    table_data,
                    colWidths=widths,
                    repeatRows=1,
                    hAlign="LEFT",
                )
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 6),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                            ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor(LINE)),
                            (
                                "ROWBACKGROUNDS",
                                (0, 1),
                                (-1, -1),
                                [colors.white, colors.HexColor(PALE_BLUE)],
                            ),
                        ]
                    )
                )
                story.extend([table, Spacer(1, 5 * mm)])
            continue

        bullet_match = re.match(r"^-\s+(.+)$", line)
        number_match = re.match(r"^(\d+)\.\s+(.+)$", line)
        if bullet_match:
            flush_paragraph()
            story.append(
                Paragraph(
                    inline_markup(bullet_match.group(1)),
                    bullet_style,
                    bulletText="-",
                )
            )
            index += 1
            continue
        if number_match:
            flush_paragraph()
            story.append(
                Paragraph(
                    inline_markup(number_match.group(2)),
                    number_style,
                    bulletText=f"{number_match.group(1)}.",
                )
            )
            index += 1
            continue

        paragraph_buffer.append(line)
        index += 1

    flush_paragraph()
    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Case-study Markdown source")
    parser.add_argument("output", type=Path, help="Output PDF path")
    args = parser.parse_args()
    build_pdf(args.source.resolve(), args.output.resolve())
    print(args.output.resolve())


if __name__ == "__main__":
    main()
