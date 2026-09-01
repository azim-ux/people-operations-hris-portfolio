import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "generate_uae_case_study_pdf.py"
MODULE_SPEC = importlib.util.spec_from_file_location("generate_uae_case_study_pdf", MODULE_PATH)
pdf_builder = importlib.util.module_from_spec(MODULE_SPEC)
assert MODULE_SPEC and MODULE_SPEC.loader
MODULE_SPEC.loader.exec_module(pdf_builder)


class CaseStudyPdfBuilderTests(unittest.TestCase):
    def test_clean_text_normalizes_unsupported_punctuation(self):
        self.assertEqual(
            pdf_builder.clean_text("retention—growth × 6 · controls"),
            "retention-growth x 6  |  controls",
        )

    def test_inline_markup_converts_bold_without_leaking_markdown(self):
        rendered = pdf_builder.inline_markup("**Turnover:** 11.0%")
        self.assertEqual(rendered, "<b>Turnover:</b> 11.0%")
        self.assertNotIn("**", rendered)

    def test_split_table_removes_alignment_row(self):
        rows = pdf_builder.split_table(
            ["| Metric | Value |", "|---|---:|", "| Turnover | 11.0% |"]
        )
        self.assertEqual(rows, [["Metric", "Value"], ["Turnover", "11.0%"]])

    def test_metadata_removes_markdown_markers(self):
        metadata = pdf_builder.parse_metadata(
            [
                "# UAE Workforce Planning and Total Rewards",
                "**Author:** Mohammad Azimuddin",
                "**Date:** August 2026",
            ]
        )
        self.assertEqual(metadata["author"], "Mohammad Azimuddin")
        self.assertEqual(metadata["date"], "August 2026")

    @unittest.skipUnless(importlib.util.find_spec("reportlab"), "ReportLab not installed")
    def test_build_pdf_creates_valid_pdf_without_placeholders(self):
        source_text = """# UAE Workforce Planning and Total Rewards

**Author:** Mohammad Azimuddin
**Date:** August 2026

## Business question

How should leaders allocate a synthetic people budget?

## Dataset and controls

| Component | Synthetic scope |
|---|---:|
| Employee records | 650 |

## Descriptive findings

These findings are descriptive. They are not employer outcomes.

## Scenario comparison

| Scenario | Expected exits | Total hires required | Projected people cost | Year-end headcount |
|---|---:|---:|---:|---:|
| Baseline | 59 | 95 | AED 88,588,663 | 574 |

## Recommendation

Run a 90-day validation phase.

## Limitations

- All results are synthetic.
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "case.md"
            output = root / "case.pdf"
            source.write_text(source_text, encoding="utf-8")
            pdf_builder.build_pdf(source, output)
            self.assertTrue(output.read_bytes().startswith(b"%PDF"))
            self.assertGreater(output.stat().st_size, 5_000)


if __name__ == "__main__":
    unittest.main()
