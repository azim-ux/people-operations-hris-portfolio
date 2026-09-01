#!/usr/bin/env python3
"""Render the structured remote-job resumes as one-page, upload-ready PDFs."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

from fpdf import FPDF


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "98_Maintenance" / "generate_remote_targeted_resumes.py"
OUT = ROOT / "07_Remote_Job_Applications" / "2026-07-30"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ITALIC = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"

BLUE = (23, 58, 86)
MID_BLUE = (49, 95, 126)
GREY = (66, 83, 103)
DARK = (23, 32, 43)


def load_source():
    spec = importlib.util.spec_from_file_location("remote_resumes", SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ResumePDF(FPDF):
    def __init__(self, title: str):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(15.5, 9.0, 15.5)
        self.set_auto_page_break(False)
        self.add_font("ArialLocal", "", FONT_REGULAR)
        self.add_font("ArialLocal", "B", FONT_BOLD)
        self.add_font("ArialLocal", "I", FONT_ITALIC)
        self.set_title(title)
        self.set_author("Mohammad Azimuddin")
        self.set_creator("Evidence-controlled targeted resume generator")
        self.set_subject("Targeted remote-job resume")
        self.add_page()

    def font(self, style="", size=9.0, color=DARK):
        self.set_font("ArialLocal", style, size)
        self.set_text_color(*color)

    def section(self, title: str):
        self.ln(1.0)
        self.font("B", 9.8, BLUE)
        self.cell(0, 4.45, title.upper(), new_x="LMARGIN", new_y="NEXT")
        y = self.get_y() - 0.7
        self.set_draw_color(119, 145, 164)
        self.set_line_width(0.18)
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(0.2)

    def paragraph(self, text: str, size=9.0, line=4.0, color=DARK):
        self.font("", size, color)
        self.multi_cell(0, line, text, new_x="LMARGIN", new_y="NEXT")

    def linked_learning(self, module, job, size=8.15, line=3.65):
        """Render ATS-readable learning text and attach the public Oracle badge URL."""
        keys = (
            module.learning_keys(job)
            if hasattr(module, "learning_keys")
            else ["oracle", *[key for key in job["learning"] if key != "oracle"]]
        )
        self.set_x(self.l_margin)
        for index, key in enumerate(keys):
            if index:
                self.font("", size, DARK)
                self.write(line, " · ")
            link = module.ORACLE_BADGE_URL if key == "oracle" else ""
            self.font("", size, DARK)
            self.write(line, module.LEARNING[key], link=link)
            if key == "oracle":
                self.font("U", size, MID_BLUE)
                self.write(line, " [Verify]", link=link)
        self.ln(line)

    def compact_center_links(self, segments):
        """segments: sequence of (text, link-or-empty)."""
        self.font("", 7.75, DARK)
        widths = [self.get_string_width(text) for text, _ in segments]
        total = sum(widths)
        self.set_x((self.w - total) / 2)
        for (text, link), width in zip(segments, widths):
            self.cell(width, 3.2, text, link=link or "")
        self.ln(3.4)

    def experience_entry(self, item):
        self.font("B", 9.35, DARK)
        y = self.get_y()
        self.cell(0, 3.95, item["title"])
        self.font("", 8.55, DARK)
        date_w = self.get_string_width(item["dates"])
        self.set_xy(self.w - self.r_margin - date_w, y)
        self.cell(date_w, 3.95, item["dates"], align="R", new_x="LMARGIN", new_y="NEXT")
        self.font("", 8.25, GREY)
        self.multi_cell(0, 3.55, item["org"], new_x="LMARGIN", new_y="NEXT")

        self.set_text_color(*DARK)
        for bullet in item["bullets"]:
            self.font("", 8.65, DARK)
            self.set_x(self.l_margin + 1.2)
            self.cell(3.0, 3.75, "•")
            self.multi_cell(
                self.w - self.r_margin - (self.l_margin + 4.2),
                3.75,
                bullet,
                new_x="LMARGIN",
                new_y="NEXT",
            )
        self.ln(0.35)

    def education_entry(self, item):
        self.font("B", 9.5, DARK)
        y = self.get_y()
        self.cell(0, 4.15, item["title"])
        self.font("", 8.8, DARK)
        date_w = self.get_string_width(item["dates"])
        self.set_xy(self.w - self.r_margin - date_w, y)
        self.cell(date_w, 4.15, item["dates"], align="R", new_x="LMARGIN", new_y="NEXT")
        detail = f" · {item['detail']}" if item["detail"] else ""
        self.font("", 8.55, GREY)
        self.cell(0, 3.85, f"{item['org']}{detail}", new_x="LMARGIN", new_y="NEXT")


def filename_for(job: dict) -> str:
    base = f"Mohammad_Azimuddin_{job['company'].replace(' / ', '_').replace(' ', '_')}_{job['role']}"
    base = re.sub(r"[^A-Za-z0-9_-]+", "_", base).strip("_")
    return f"{base}_Resume.pdf"


def render_job(module, job: dict) -> Path:
    title = f"Mohammad Azimuddin — {job['company']} — {job['role']}"
    pdf = ResumePDF(title)

    pdf.font("B", 20.0, BLUE)
    pdf.cell(0, 7.0, module.CONTACT["name"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.font("B", 9.1, MID_BLUE)
    pdf.cell(0, 3.8, job["headline"], align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.font("B", 7.7, DARK)
    pdf.cell(
        0,
        3.5,
        f"TARGET POSITION: {job['role'].upper()} · {job['company'].upper()}",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.compact_center_links(
        [
            (module.CONTACT["location"] + " · Contact via LinkedIn", ""),
        ]
    )
    pdf.compact_center_links(
        [(module.CONTACT["linkedin"], module.CONTACT["linkedin_url"])]
    )
    pdf.set_draw_color(37, 79, 112)
    pdf.set_line_width(0.55)
    pdf.line(pdf.l_margin, pdf.get_y() + 0.5, pdf.w - pdf.r_margin, pdf.get_y() + 0.5)
    pdf.ln(1.2)

    pdf.section("Professional Summary")
    pdf.paragraph(job["summary"], size=9.25, line=4.05)

    pdf.section("Core Skills")
    pdf.paragraph(" · ".join(job["skills"]), size=8.55, line=3.75)

    pdf.section("Experience")
    for item in job["experience"]:
        pdf.experience_entry(item)

    if job.get("projects"):
        pdf.section("Selected Project")
        for item in job["projects"]:
            pdf.experience_entry(item)

    pdf.section("Education")
    for item in module.EDUCATION:
        pdf.education_entry(item)

    pdf.section("Certifications & Applied Learning")
    pdf.linked_learning(module, job, size=8.15, line=3.65)

    pdf.section("Technical Skills")
    technical = job.get("technical") or (
        f"{job['tools']}. Microsoft Excel, Word, and PowerPoint; "
        "introductory Power BI workshop exposure."
    )
    pdf.paragraph(technical, size=8.3, line=3.7)

    if pdf.page_no() != 1:
        raise RuntimeError(f"{job['company']} rendered to {pdf.page_no()} pages")
    if pdf.get_y() > 289:
        raise RuntimeError(
            f"{job['company']} content reached {pdf.get_y():.1f} mm; reduce content before delivery"
        )

    folder = OUT / job["slug"]
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / filename_for(job)
    pdf.output(output)
    return output


def main():
    module = load_source()
    results = []
    for job in module.JOBS:
        path = render_job(module, job)
        results.append(path)
        print(f"{job['company']}: {path.name}")
    print(f"Rendered {len(results)} PDFs.")


if __name__ == "__main__":
    main()
