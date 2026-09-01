import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PORTFOLIO = ROOT / "06_Portfolio_Projects"

PROJECTS = [
    {
        "directory": PORTFOLIO / "04_Structured_Hiring_and_ATS_Lab",
        "pdf": "Structured_Hiring_and_ATS_Architecture_Mobile_Case_Study.pdf",
        "dashboard": "index.html",
    },
    {
        "directory": PORTFOLIO / "project 1" / "03_Evidence_Based_Onboarding_HR_Operations_Lab",
        "pdf": "Evidence_Based_Onboarding_HR_Operations_Mobile_Case_Study.pdf",
        "dashboard": "index.html",
    },
    {
        "directory": PORTFOLIO / "05_Skills_Based_LD_Planner",
        "pdf": "Skills_Based_LD_Planner_Mobile_Case_Study.pdf",
        "dashboard": "index.html",
    },
]


class MobilePortfolioExperienceTests(unittest.TestCase):
    def test_mobile_sources_are_five_page_tall_portrait_documents(self):
        stylesheet = (PORTFOLIO / "mobile-case-study.css").read_text(encoding="utf-8")
        for token in [
            "@page { size: 148mm 254mm; margin: 0; }",
            "@media screen and (max-width: 640px)",
            "min-height: 100svh",
            "font-size: 14pt",
        ]:
            self.assertIn(token, stylesheet)

        for project in PROJECTS:
            source = (project["directory"] / "mobile-case-study.html").read_text(encoding="utf-8")
            self.assertIn('name="viewport" content="width=device-width, initial-scale=1"', source)
            self.assertEqual(5, len(re.findall(r'<section class="page">', source)))
            self.assertIn("Phone edition", source)
            self.assertIn("Open interactive dashboard", source)

    def test_mobile_pdfs_are_five_page_tall_portrait_files(self):
        for project in PROJECTS:
            pdf = project["directory"] / project["pdf"]
            self.assertTrue(pdf.is_file(), pdf)
            result = subprocess.run(
                ["pdfinfo", str(pdf)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Pages:           5", result.stdout)
            size = re.search(r"Page size:\s+([\d.]+) x ([\d.]+) pts", result.stdout)
            self.assertIsNotNone(size, result.stdout)
            width, height = map(float, size.groups())
            self.assertLess(width, height)
            self.assertGreaterEqual(width, 410)
            self.assertLessEqual(width, 430)
            self.assertGreaterEqual(height, 715)
            self.assertLessEqual(height, 725)

    def test_dashboards_expose_phone_pdfs_and_touch_sized_controls(self):
        hub = (PORTFOLIO / "index.html").read_text(encoding="utf-8")
        self.assertIn("project-actions", hub)
        self.assertIn("min-height:44px", hub)

        for project in PROJECTS:
            dashboard = (project["directory"] / project["dashboard"]).read_text(encoding="utf-8")
            self.assertIn(project["pdf"], dashboard)
            self.assertIn('target="_blank"', dashboard)
            self.assertRegex(dashboard, r"min-height:\s*44px")
            self.assertRegex(dashboard, r"-webkit-overflow-scrolling:\s*touch")


if __name__ == "__main__":
    unittest.main(verbosity=2)
