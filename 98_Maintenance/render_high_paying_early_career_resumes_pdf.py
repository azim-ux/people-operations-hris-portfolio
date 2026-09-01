#!/usr/bin/env python3
"""Render and package the 31 July 2026 high-paying early-career CV set."""

from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "98_Maintenance" / "generate_high_paying_early_career_resumes.py"
BASE_RENDERER = ROOT / "98_Maintenance" / "render_remote_targeted_resumes_pdf.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def destination_name(job: dict) -> str:
    role = job["slug"].split("_", 1)[1]
    return f"{job['order']:02d}_{role}.pdf"


def write_package_readme(source, directory: Path, category: str) -> None:
    jobs = [job for job in source.JOBS if job["category"] == category]
    if category == "priority":
        heading = "Ready to Upload"
        intro = "Upload only the PDF matching the employer and role. Re-open the live vacancy immediately before applying."
    elif category == "conditional":
        heading = "Conditional or Gap"
        intro = (
            "These CVs are technically prepared but should not be submitted until the documented eligibility, "
            "location, or mandatory-skill condition is resolved."
        )
    else:
        heading = "Expired or Closed"
        intro = (
            "These CVs are preserved for reference only. Do not submit them unless the employer republishes "
            "the vacancy and the new requirements are checked."
        )
    rows = []
    for job in sorted(jobs, key=lambda item: item["order"]):
        filename = destination_name(job)
        rows.append(
            f"| {job['order']} | {job['company']} | {job['role']} | "
            f"[PDF]({filename}) | [Apply]({job['url']}) | {job['status']} |"
        )
    text = f"""# {heading}

Prepared: 31 July 2026

{intro}

| Priority | Company | Role | CV | Application | Submission status |
|---:|---|---|---|---|---|
{chr(10).join(rows)}

Every CV is one-page, A4, text-extractable, and evidence-controlled. No CV can guarantee shortlisting.
The myTVS title and dates must match the final signed experience/service certificate.
"""
    (directory / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    source = load_module(SOURCE, "high_paying_early_career")
    renderer = load_module(BASE_RENDERER, "base_pdf_renderer")
    renderer.OUT = source.OUT

    ready = source.OUT / "00_Ready_to_Upload"
    expired = source.OUT / "98_Expired_or_Closed"
    conditional = source.OUT / "99_Conditional_or_Gap"
    ready.mkdir(parents=True, exist_ok=True)
    expired.mkdir(parents=True, exist_ok=True)
    conditional.mkdir(parents=True, exist_ok=True)

    results = []
    for job in source.JOBS:
        rendered = renderer.render_job(source, job)
        if job["category"] == "priority":
            target_dir = ready
        elif job["category"] == "conditional":
            target_dir = conditional
        else:
            target_dir = expired
        packaged = target_dir / destination_name(job)
        shutil.copy2(rendered, packaged)
        results.append((rendered, packaged))
        print(f"{job['company']}: {rendered.name} -> {packaged.name}")

    write_package_readme(source, ready, "priority")
    write_package_readme(source, expired, "expired")
    write_package_readme(source, conditional, "conditional")
    print(f"Rendered and packaged {len(results)} CVs under {source.OUT}")


if __name__ == "__main__":
    main()
