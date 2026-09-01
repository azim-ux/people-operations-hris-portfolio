import csv
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "06_Portfolio_Projects" / "05_Skills_Based_LD_Planner"

EXPECTED_FILES = {
    "synthetic_competencies.csv",
    "synthetic_employees_skills.csv",
    "synthetic_development_plans.csv",
    "README.md",
    "RESEARCH_FOUNDATION.md",
    "ONET_COMPETENCY_ONTOLOGY.md",
    "KIRKPATRICK_EVALUATION_MODEL.md",
    "IDP_FRAMEWORK_AND_RACI.md",
    "NINE_BOX_TALENT_MATRIX.md",
    "LMS_WORKFLOW_AND_INTEGRATION.md",
    "RBAC_AND_PRIVACY_MATRIX.md",
    "UAT_TEST_REGISTER.md",
    "METHODOLOGY_AND_LIMITATIONS.md",
    "DATA_DICTIONARY.md",
    "CV_PROJECT_ENTRY.md",
    "LINKEDIN_POST.md",
    "INTERVIEW_GUIDE.md",
    "dashboard.html",
    "index.html",
    "slides.html",
}

COMPETENCY_HEADERS = [
    "Competency_ID", "ONET_Code", "Competency_Name", "Department", "Category",
    "Target_Proficiency_Baseline", "Current_Workforce_Proficiency", "Mean_Gap",
    "Assessment_Standard",
]

EMPLOYEE_HEADERS = [
    "Employee_ID", "Synthetic_Name", "Department", "Grade", "Performance_Score",
    "Potential_Score", "9_Box_Category", "Technical_Mastery_Percent",
    "Compliance_Mastery_Percent", "Leadership_Mastery_Percent",
    "Overall_Mastery_Percent", "Mean_Skill_Gap",
]

PLAN_HEADERS = [
    "Plan_ID", "Employee_ID", "Plan_Status", "Target_Competency_ID",
    "Development_Action", "Milestone_30_Days", "Milestone_60_Days",
    "Milestone_90_Days", "Mentor_Employee_ID", "Planned_Training_Hours",
    "Kirkpatrick_L1_Reaction_Score", "Kirkpatrick_L2_Learning_Percent",
    "Kirkpatrick_L3_Behavior_Status", "Kirkpatrick_L4_Result_Measure",
]


def read_csv(name):
    with (PROJECT / name).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


class SkillsBasedLDPlannerAcceptanceTests(unittest.TestCase):
    def test_01_exact_file_inventory(self):
        self.assertTrue(PROJECT.is_dir(), f"Missing project directory: {PROJECT}")
        actual = {path.name for path in PROJECT.iterdir() if path.is_file()}
        self.assertEqual(EXPECTED_FILES, actual)

    def test_02_schemas_identity_sequences_and_referential_integrity(self):
        competency_headers, competencies = read_csv("synthetic_competencies.csv")
        employee_headers, employees = read_csv("synthetic_employees_skills.csv")
        plan_headers, plans = read_csv("synthetic_development_plans.csv")
        self.assertEqual(COMPETENCY_HEADERS, competency_headers)
        self.assertEqual(EMPLOYEE_HEADERS, employee_headers)
        self.assertEqual(PLAN_HEADERS, plan_headers)
        self.assertEqual((20, 70, 70), (len(competencies), len(employees), len(plans)))
        self.assertEqual(
            [f"COMP-{number:03d}" for number in range(1, 21)],
            [row["Competency_ID"] for row in competencies],
        )
        self.assertEqual(
            [f"APD-2026-{number:03d}" for number in range(1, 71)],
            [row["Employee_ID"] for row in employees],
        )
        self.assertEqual(
            [f"IDP-2026-{number:03d}" for number in range(1, 71)],
            [row["Plan_ID"] for row in plans],
        )
        employee_ids = {row["Employee_ID"] for row in employees}
        competency_ids = {row["Competency_ID"] for row in competencies}
        self.assertTrue(all(row["Employee_ID"] in employee_ids for row in plans))
        self.assertTrue(all(row["Mentor_Employee_ID"] in employee_ids for row in plans))
        self.assertTrue(all(row["Target_Competency_ID"] in competency_ids for row in plans))
        self.assertTrue(all(row["Employee_ID"] != row["Mentor_Employee_ID"] for row in plans))

    def test_03_reconciled_governed_kpis(self):
        _, competencies = read_csv("synthetic_competencies.csv")
        _, employees = read_csv("synthetic_employees_skills.csv")
        _, plans = read_csv("synthetic_development_plans.csv")
        mean_mastery = sum(Decimal(row["Overall_Mastery_Percent"]) for row in employees) / Decimal(70)
        mean_gap = sum(Decimal(row["Mean_Skill_Gap"]) for row in employees) / Decimal(70)
        self.assertEqual(Decimal("81.4"), mean_mastery)
        self.assertEqual(Decimal("-0.48"), mean_gap)
        self.assertEqual(58, sum(row["Plan_Status"] == "Active" for row in plans))
        self.assertEqual(14, sum(row["9_Box_Category"] == "Star Talent" for row in employees))
        self.assertEqual(
            {"Engineering", "Quality", "Supply Chain", "People & Culture"},
            {row["Department"] for row in employees},
        )
        self.assertEqual({"G1", "G2", "G3", "G4", "G5"}, {row["Grade"] for row in employees})
        self.assertEqual(
            Decimal("4.12"),
            sum(Decimal(row["Target_Proficiency_Baseline"]) for row in competencies) / Decimal(20),
        )
        self.assertEqual(
            Decimal("3.64"),
            sum(Decimal(row["Current_Workforce_Proficiency"]) for row in competencies) / Decimal(20),
        )
        self.assertEqual(
            Decimal("-0.48"),
            sum(Decimal(row["Mean_Gap"]) for row in competencies) / Decimal(20),
        )
        self.assertEqual(
            Decimal("4.6"),
            sum(Decimal(row["Kirkpatrick_L1_Reaction_Score"]) for row in plans) / Decimal(70),
        )
        self.assertEqual(
            Decimal("88.6"),
            sum(Decimal(row["Kirkpatrick_L2_Learning_Percent"]) for row in plans) / Decimal(70),
        )
        for row in employees:
            component_mean = (
                Decimal(row["Technical_Mastery_Percent"])
                + Decimal(row["Compliance_Mastery_Percent"])
                + Decimal(row["Leadership_Mastery_Percent"])
            ) / Decimal(3)
            self.assertEqual(Decimal(row["Overall_Mastery_Percent"]), component_mean)

    def test_04_nine_box_classification_is_reproducible(self):
        _, employees = read_csv("synthetic_employees_skills.csv")
        labels = {1: "Low", 2: "Moderate", 3: "High"}
        expected_categories = {
            ("High", "High"): "Star Talent",
            ("Moderate", "High"): "High Potential",
            ("Low", "High"): "Emerging Potential",
            ("High", "Moderate"): "High Performer",
            ("Moderate", "Moderate"): "Core Contributor",
            ("Low", "Moderate"): "Development Focus",
            ("High", "Low"): "Trusted Professional",
            ("Moderate", "Low"): "Effective Contributor",
            ("Low", "Low"): "Priority Support",
        }
        for row in employees:
            key = (labels[int(row["Performance_Score"])], labels[int(row["Potential_Score"])])
            self.assertEqual(expected_categories[key], row["9_Box_Category"], row["Employee_ID"])

    def test_05_privacy_linter_and_completeness(self):
        email_pattern = re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", re.IGNORECASE)
        mobile_pattern = re.compile(r"(?<!\d)[6-9]\d{9}(?!\d)")
        aadhaar_pattern = re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b")
        pan_pattern = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")
        passport_pattern = re.compile(r"\b[A-Z][1-9]\d{6}\b")
        forbidden_content = re.compile(
            r"\b(TODO|TBD|lorem ipsum|insert here|add more here|placeholder)\b", re.IGNORECASE
        )
        for path in PROJECT.iterdir():
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            domains = {match.group(1).lower() for match in email_pattern.finditer(text)}
            self.assertTrue(domains <= {"example.com"}, (path.name, domains))
            self.assertIsNone(mobile_pattern.search(text), path.name)
            self.assertIsNone(aadhaar_pattern.search(text), path.name)
            self.assertIsNone(pan_pattern.search(text), path.name)
            self.assertIsNone(passport_pattern.search(text), path.name)
            self.assertNotIn("/" + "Users" + "/", text, path.name)
            self.assertNotIn("C:\\" + "Users" + "\\", text, path.name)
            if path.suffix in {".md", ".html"}:
                self.assertIsNone(forbidden_content.search(text), path.name)

    def test_06_documentation_controls_and_traceability(self):
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        for filename in EXPECTED_FILES - {"README.md"}:
            self.assertIn(f"]({filename})", readme, filename)
        research = (PROJECT / "RESEARCH_FOUNDATION.md").read_text(encoding="utf-8")
        for token in ["O*NET 31.0", "August 2026", "Sanchez", "Levine", "non-causal"]:
            self.assertIn(token, research)
        ontology = (PROJECT / "ONET_COMPETENCY_ONTOLOGY.md").read_text(encoding="utf-8")
        for token in ["CC BY 4.0", "20 competencies", "version control"]:
            self.assertIn(token, ontology)
        kirkpatrick = (PROJECT / "KIRKPATRICK_EVALUATION_MODEL.md").read_text(encoding="utf-8")
        for token in ["Level 1 — Reaction", "Level 2 — Learning", "Level 3 — Behavior", "Level 4 — Results"]:
            self.assertIn(token, kirkpatrick)
        raci = (PROJECT / "IDP_FRAMEWORK_AND_RACI.md").read_text(encoding="utf-8")
        self.assertEqual(20, len(re.findall(r"^\| RACI-\d{2} \|", raci, flags=re.MULTILINE)))
        uat = (PROJECT / "UAT_TEST_REGISTER.md").read_text(encoding="utf-8")
        self.assertEqual(
            [f"UAT-{number:03d}" for number in range(1, 15)],
            re.findall(r"^### (UAT-\d{3})\b", uat, flags=re.MULTILINE),
        )
        privacy = (PROJECT / "RBAC_AND_PRIVACY_MATRIX.md").read_text(encoding="utf-8")
        for token in ["least privilege", "DPDP", "purpose limitation", "retention"]:
            self.assertIn(token, privacy)
        method = (PROJECT / "METHODOLOGY_AND_LIMITATIONS.md").read_text(encoding="utf-8")
        for token in ["synthetic", "descriptive", "not causal", "small cohort"]:
            self.assertIn(token, method)
        lms = (PROJECT / "LMS_WORKFLOW_AND_INTEGRATION.md").read_text(encoding="utf-8")
        for token in ["LMS", "approval gate", "audit log", "rollback"]:
            self.assertIn(token, lms)

    def test_07_html_embeds_source_identical_json_and_required_ui(self):
        _, competencies = read_csv("synthetic_competencies.csv")
        _, employees = read_csv("synthetic_employees_skills.csv")
        _, plans = read_csv("synthetic_development_plans.csv")
        for filename in ["index.html", "dashboard.html"]:
            html = (PROJECT / filename).read_text(encoding="utf-8")
            self.assertIn("https://cdn.tailwindcss.com", html)
            self.assertIn("https://cdn.jsdelivr.net/npm/chart.js", html)
            for value in ["81.4%", "58", "14", "+24.6%", "-18.2%", "₹4.8 lakhs", "-0.48"]:
                self.assertIn(value, html, (filename, value))
            for element_id in [
                "nine-box-grid", "box-star-talent", "onet-gap-chart", "kirkpatrick-bars",
                "employee-search", "department-filter", "grade-filter", "ninebox-filter",
                "employee-table-body", "idp-drawer", "close-idp", "page-size",
                "previous-page", "next-page", "page-indicator",
            ]:
                self.assertIn(f'id="{element_id}"', html, (filename, element_id))
            embedded = {}
            for key in ["competencies", "employees", "plans"]:
                match = re.search(
                    rf'<script id="{key}-data" type="application/json">(.*?)</script>',
                    html,
                    flags=re.DOTALL,
                )
                self.assertIsNotNone(match, (filename, key))
                embedded[key] = json.loads(match.group(1))
            self.assertEqual(competencies, embedded["competencies"])
            self.assertEqual(employees, embedded["employees"])
            self.assertEqual(plans, embedded["plans"])
            for token in ["escapeHtml", "prefers-reduced-motion", "requestAnimationFrame"]:
                self.assertIn(token, html)
            self.assertRegex(html, r'<option value="25"[^>]*>25 rows</option>')
            self.assertRegex(html, r'<option value="50"[^>]*>50 rows</option>')
            self.assertNotIn("eval(", html)
            self.assertNotIn("document.write", html)

    def test_08_slide_deck_is_five_slide_keyboard_and_print_ready(self):
        html = (PROJECT / "slides.html").read_text(encoding="utf-8")
        self.assertEqual(5, len(re.findall(r'<section\s+class="[^"]*\bslide\b', html)))
        for number in range(1, 6):
            self.assertIn(f'id="slide-{number}"', html)
        for token in ["ArrowLeft", "ArrowRight", "progress-bar", "slide-counter", "@media print"]:
            self.assertIn(token, html)
        for token in ["70", "81.4%", "58", "14", "+24.6%", "-18.2%", "₹4.8 lakhs"]:
            self.assertIn(token, html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
