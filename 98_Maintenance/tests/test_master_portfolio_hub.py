import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
HUB = ROOT / "06_Portfolio_Projects"

DELIVERABLES = ["index.html", "README.md", "MASTER_CV_PROJECTS_SNIPPET.md"]

PROJECTS = [
    {
        "id": "talent-acquisition",
        "directory": "04_Structured_Hiring_and_ATS_Lab",
        "title": "Structured Hiring & ATS Architecture Lab",
        "domain": "Talent Acquisition Operations & Psychometrics",
        "metrics": {
            "conversion": "3.0%",
            "hires": "120",
            "time_to_fill": "28.5d",
            "sla": "91.8%",
            "adverse_impact_ratio": "0.87",
        },
        "links": {
            "project": "04_Structured_Hiring_and_ATS_Lab/index.html",
            "slides": "04_Structured_Hiring_and_ATS_Lab/slides.html",
        },
    },
    {
        "id": "onboarding",
        "directory": "project%201/03_Evidence_Based_Onboarding_HR_Operations_Lab",
        "title": "Evidence-Based 90-Day Onboarding & HR Ops Lab",
        "domain": "Employee Onboarding, HRIS Workflow & Socialization",
        "metrics": {
            "day_1_readiness": "93.4%",
            "task_sla": "88.5%",
            "role_clarity": "24.2 days",
            "active_cohort": "20",
            "open_escalations": "3",
        },
        "links": {
            "project": "project%201/03_Evidence_Based_Onboarding_HR_Operations_Lab/index.html",
            "slides": "project%201/03_Evidence_Based_Onboarding_HR_Operations_Lab/slides.html",
        },
    },
    {
        "id": "talent-development",
        "directory": "05_Skills_Based_LD_Planner",
        "title": "Skills-Based L&D Planner & Talent Growth Engine",
        "domain": "Talent Development, Competency Modeling & Training ROI",
        "metrics": {
            "mastery": "81.4%",
            "active_idps": "58",
            "star_talent": "14",
            "yield_gain": "+24.6%",
            "scrap_reduction": "-18.2%",
            "quarterly_savings": "₹4.8 Lakhs",
        },
        "links": {
            "project": "05_Skills_Based_LD_Planner/index.html",
            "slides": "05_Skills_Based_LD_Planner/slides.html",
        },
    },
]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return
        attributes = dict(attrs)
        if "href" in attributes:
            self.links.append(attributes)


def load_html():
    return (HUB / "index.html").read_text(encoding="utf-8")


def embedded_portfolio_data(html):
    match = re.search(
        r'<script id="portfolio-data" type="application/json">(.*?)</script>',
        html,
        flags=re.DOTALL,
    )
    if not match:
        return None
    return json.loads(match.group(1))


class MasterPortfolioHubAcceptanceTests(unittest.TestCase):
    def test_01_deliverables_and_project_entry_points_exist(self):
        for filename in DELIVERABLES:
            self.assertTrue((HUB / filename).is_file(), filename)
        for project in PROJECTS:
            project_dir = HUB / unquote(project["directory"])
            self.assertTrue((project_dir / "index.html").is_file(), project["directory"])
            self.assertTrue((project_dir / "slides.html").is_file(), project["directory"])

    def test_02_hub_links_every_project_and_slide_deck(self):
        html = load_html()
        readme = (HUB / "README.md").read_text(encoding="utf-8")
        for project in PROJECTS:
            page = project["links"]["project"]
            slides = project["links"]["slides"]
            self.assertIn(f'href="{page}"', html, page)
            self.assertIn(f'href="{slides}"', html, slides)
            self.assertIn(f']({page})', readme, page)
            self.assertIn(f']({slides})', readme, slides)

    def test_03_embedded_metadata_matches_governed_metrics(self):
        html = load_html()
        data = embedded_portfolio_data(html)
        self.assertIsNotNone(data)
        self.assertEqual("Mohammad Azimuddin", data["candidate"]["name"])
        self.assertEqual(
            "Oracle Fusion Cloud Applications HCM Process Essentials Certified – Rel 1 (1Z0-1162-1)",
            data["candidate"]["certification"],
        )
        self.assertEqual(PROJECTS, data["projects"])
        for project in PROJECTS:
            for value in project["metrics"].values():
                self.assertIn(value, html, (project["id"], value))

    def test_04_profile_credentials_stack_and_architecture_are_present(self):
        html = load_html()
        for token in [
            "Mohammad Azimuddin",
            "Master of Human Resource Management",
            "Aligarh Muslim University",
            "Oracle Fusion Cloud HCM",
            "1Z0-1162-1",
            "Open to India &amp; UAE relocation",
            "Frappe HR",
            "OpenCATS",
            "O*NET 31.0",
            "Chart.js",
            "Python",
            "SQL",
        ]:
            self.assertIn(token, html)
        for element_id in [
            "project-ats",
            "project-onboarding",
            "project-ld",
            "lifecycle-map",
            "stage-talent-acquisition",
            "stage-onboarding",
            "stage-talent-development",
            "architecture-detail",
        ]:
            self.assertIn(f'id="{element_id}"', html, element_id)
        self.assertIn("https://cdn.tailwindcss.com", html)
        self.assertRegex(html, r"https://(?:unpkg\.com|cdn\.jsdelivr\.net)/.+lucide")
        self.assertIn("lucide.createIcons", html)
        self.assertIn('href="#main-content"', html)
        self.assertIn("prefers-reduced-motion", html)
        self.assertLess(html.index('id="stage-talent-acquisition"'), html.index('id="stage-onboarding"'))
        self.assertLess(html.index('id="stage-onboarding"'), html.index('id="stage-talent-development"'))

    def test_05_public_contact_and_cv_links_are_safe_and_complete(self):
        parser = LinkParser()
        parser.feed(load_html())
        hrefs = [link["href"] for link in parser.links]
        self.assertTrue(any(href.startswith("https://www.linkedin.com/") for href in hrefs))
        self.assertTrue(any(href.startswith("https://github.com/") for href in hrefs))
        self.assertEqual(0, sum(href.startswith("mailto:") for href in hrefs))
        cv_links = [link for link in parser.links if link.get("data-link") == "cv-download"]
        self.assertEqual(1, len(cv_links))
        self.assertNotIn("download", cv_links[0])
        cv_path = HUB / unquote(urlsplit(cv_links[0]["href"]).path)
        self.assertTrue(cv_path.resolve().is_relative_to(ROOT.resolve()))
        self.assertTrue(cv_path.is_file(), cv_path)
        self.assertTrue(cv_path.resolve().is_relative_to((ROOT / "02_CV_Library").resolve()))
        self.assertEqual(".html", cv_path.suffix.lower())
        for link in parser.links:
            href = link["href"]
            if href.startswith(("https://", "mailto:")):
                if href.startswith("https://"):
                    self.assertEqual("_blank", link.get("target"), href)
                    rel_tokens = set(link.get("rel", "").split())
                    self.assertTrue({"noopener", "noreferrer"} <= rel_tokens, href)

    def test_06_all_relative_html_and_markdown_links_resolve(self):
        html = load_html()
        parser = LinkParser()
        parser.feed(html)
        for link in parser.links:
            href = link["href"]
            if href.startswith(("https://", "mailto:", "#")):
                continue
            parts = urlsplit(href)
            target = HUB / unquote(parts.path)
            self.assertTrue(target.is_file(), href)
        readme = (HUB / "README.md").read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", readme):
            if target.startswith(("https://", "mailto:", "#")):
                continue
            path = HUB / unquote(urlsplit(target).path)
            self.assertTrue(path.is_file(), target)

    def test_07_privacy_and_content_linter(self):
        phone_patterns = [
            re.compile(r"(?<!\d)(?:\+?91[-\s]?)?[6-9](?:[\s-]?\d){9}(?!\d)"),
            re.compile(r"(?<!\d)(?:\+?971[-\s]?)?5(?:[\s-]?\d){8}(?!\d)"),
        ]
        sensitive_patterns = [
            re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b"),
            re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
            re.compile(r"\b[A-Z][1-9]\d{6}\b"),
        ]
        unfinished = re.compile(
            r"\b(TODO|TBD|lorem ipsum|insert here|add more here|placeholder)\b",
            re.IGNORECASE,
        )
        email_pattern = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
        for filename in DELIVERABLES:
            text = (HUB / filename).read_text(encoding="utf-8")
            self.assertNotIn("/" + "Users" + "/", text, filename)
            self.assertNotIn("C:\\" + "Users" + "\\", text, filename)
            self.assertNotIn("file://", text, filename)
            for pattern in phone_patterns + sensitive_patterns:
                self.assertIsNone(pattern.search(text), filename)
            self.assertFalse(email_pattern.search(text), filename)
            self.assertIsNone(unfinished.search(text), filename)

    def test_08_readme_and_cv_snippet_are_decision_ready(self):
        readme = (HUB / "README.md").read_text(encoding="utf-8")
        snippet = (HUB / "MASTER_CV_PROJECTS_SNIPPET.md").read_text(encoding="utf-8")
        for token in [
            "Executive Portfolio Index",
            "Employee Lifecycle Architecture",
            "KPI Summary",
            "Reproduction",
            "synthetic",
            "non-causal",
        ]:
            self.assertIn(token, readme)
        for token in [
            "India",
            "UAE",
            "Oracle Fusion Cloud HCM",
            "OpenCATS",
            "Frappe HR",
            "O*NET 31.0",
            "4,000",
            "81.4%",
            "93.4%",
            "synthetic",
        ]:
            self.assertIn(token, snippet)
        self.assertGreaterEqual(len(re.findall(r"^- ", snippet, flags=re.MULTILINE)), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
