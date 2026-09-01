import csv
import json
import re
import subprocess
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = (
    ROOT
    / "06_Portfolio_Projects"
    / "project 1"
    / "03_Evidence_Based_Onboarding_HR_Operations_Lab"
)

EXPECTED_FILES = {
    ".gitignore",
    "LICENSE",
    "README.md",
    "RESEARCH_FOUNDATION.md",
    "ORGANIZATION_AND_ROLES.md",
    "ONBOARDING_TEMPLATES_30_60_90.md",
    "RACI_MATRIX.md",
    "RBAC_AND_PRIVACY_MATRIX.md",
    "UAT_TEST_REGISTER.md",
    "METHODOLOGY_AND_LIMITATIONS.md",
    "DATA_DICTIONARY.md",
    "synthetic_onboarding_records.csv",
    "synthetic_onboarding_tasks.csv",
    "index.html",
    "slides.html",
    "mobile-case-study.html",
    "Evidence_Based_Onboarding_HR_Operations_Case_Study.pdf",
    "Evidence_Based_Onboarding_HR_Operations_Mobile_Case_Study.pdf",
}

INTERNAL_FILES = {
    "CV_PROJECT_ENTRY.md",
    "INTERVIEW_GUIDE.md",
    "FINAL_LINKEDIN_ANNOUNCEMENT.md",
    "LAUNCH_READY_KIT.md",
    "LINKEDIN_POST.md",
    "PUBLICATION_AND_DEMO_GUIDE.md",
    "SLIDE_DECK_CASE_STUDY.md",
    "export_pdf.sh",
    "dashboard.html",
}

RECORD_HEADERS = [
    "Employee_ID", "Full_Name", "Department", "Designation", "Grade", "Joining_Date",
    "Onboarding_Status", "Manager_ID", "Buddy_ID", "Day1_Readiness_Score",
    "Day30_Role_Clarity_Score", "Day30_Task_Mastery_Score",
    "Day60_Social_Acceptance_Score", "Day90_Overall_Adjustment_Score",
    "Escalations_Count", "Extended_Onboarding_Flag",
]

TASK_HEADERS = [
    "Task_ID", "Employee_ID", "Phase", "Task_Name", "Assigned_Role",
    "SLA_Hours", "Actual_Hours", "Variance_Hours", "Status", "Escalation_Required",
]


def read_csv(name):
    with (PROJECT / name).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


class OnboardingLabAcceptanceTests(unittest.TestCase):
    def test_exact_project_inventory(self):
        self.assertTrue(PROJECT.is_dir(), f"Missing project directory: {PROJECT}")
        actual = {path.name for path in PROJECT.iterdir() if path.is_file()}
        self.assertEqual(EXPECTED_FILES, actual)

    def test_records_contract_and_reconciled_kpis(self):
        headers, records = read_csv("synthetic_onboarding_records.csv")
        self.assertEqual(RECORD_HEADERS, headers)
        self.assertEqual(20, len(records))
        self.assertEqual([f"APD-2026-{i:03d}" for i in range(1, 21)], [r["Employee_ID"] for r in records])
        self.assertEqual(20, len({r["Employee_ID"] for r in records}))
        self.assertEqual(
            {"Engineering", "Quality", "Supply Chain", "Finance", "People & Culture"},
            {r["Department"] for r in records},
        )
        self.assertEqual({"APD-G1", "APD-G2", "APD-G3", "APD-G4", "APD-G5"}, {r["Grade"] for r in records})
        self.assertEqual({"Completed", "In Progress", "Escalated"}, {r["Onboarding_Status"] for r in records})
        self.assertEqual({"Yes", "No"}, {r["Extended_Onboarding_Flag"] for r in records})
        score_columns = [
            "Day30_Role_Clarity_Score", "Day30_Task_Mastery_Score",
            "Day60_Social_Acceptance_Score", "Day90_Overall_Adjustment_Score",
        ]
        for row in records:
            self.assertGreaterEqual(float(row["Day1_Readiness_Score"]), 0)
            self.assertLessEqual(float(row["Day1_Readiness_Score"]), 100)
            for column in score_columns:
                self.assertGreaterEqual(float(row[column]), 1.0)
                self.assertLessEqual(float(row[column]), 5.0)
        day1 = sum(Decimal(r["Day1_Readiness_Score"]) for r in records) / Decimal(len(records))
        self.assertEqual(Decimal("93.4"), day1)
        self.assertEqual(3, sum(int(r["Escalations_Count"]) for r in records))
        quarters = {(int(r["Joining_Date"][5:7]) - 1) // 3 + 1 for r in records}
        self.assertEqual({1, 2, 3, 4}, quarters)

    def test_tasks_contract_referential_integrity_and_reconciled_kpis(self):
        _, records = read_csv("synthetic_onboarding_records.csv")
        headers, tasks = read_csv("synthetic_onboarding_tasks.csv")
        self.assertEqual(TASK_HEADERS, headers)
        self.assertEqual(60, len(tasks))
        self.assertEqual([f"TASK-{i:03d}" for i in range(1, 61)], [t["Task_ID"] for t in tasks])
        employee_ids = {r["Employee_ID"] for r in records}
        self.assertTrue(all(t["Employee_ID"] in employee_ids for t in tasks))
        self.assertEqual({3}, {sum(t["Employee_ID"] == eid for t in tasks) for eid in employee_ids})
        self.assertTrue({"Preboarding", "Day 1", "Week 1", "Month 1", "Month 2", "Month 3"}.issubset({t["Phase"] for t in tasks}))
        self.assertTrue({"HR", "HM", "IT", "BY", "EE"}.issubset({t["Assigned_Role"] for t in tasks}))
        for task in tasks:
            expected = Decimal(task["Actual_Hours"]) - Decimal(task["SLA_Hours"])
            self.assertEqual(expected, Decimal(task["Variance_Hours"]))
        total_sla = sum(Decimal(t["SLA_Hours"]) for t in tasks)
        positive_delay = sum(max(Decimal("0"), Decimal(t["Variance_Hours"])) for t in tasks)
        sla_index = (Decimal("1") - positive_delay / total_sla) * Decimal("100")
        self.assertEqual(Decimal("88.500"), sla_index.quantize(Decimal("0.001")))
        role_clarity = [t for t in tasks if t["Task_Name"] == "Day 30 Role Clarity Sign-off"]
        self.assertEqual(20, len(role_clarity))
        average_days = sum(Decimal(t["Actual_Hours"]) / Decimal("24") for t in role_clarity) / Decimal("20")
        self.assertEqual(Decimal("24.2"), average_days)

    def test_documents_are_complete_and_cross_linked(self):
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        for filename in EXPECTED_FILES - {"README.md", ".gitignore"}:
            self.assertIn(f"]({filename})", readme, filename)
        research = (PROJECT / "RESEARCH_FOUNDATION.md").read_text(encoding="utf-8")
        for identifier in [
            "10.1037/0021-9010.92.3.707",
            "10.1177/01492063241277168",
            "10.1016/j.jvb.2006.12.004",
            "github.com/18F/onboarding-documents",
            "docs.frappe.io/hr/employee-onboarding",
        ]:
            self.assertIn(identifier, research)
        self.assertRegex(research.lower(), r"not caus|cannot establish caus")
        org = (PROJECT / "ORGANIZATION_AND_ROLES.md").read_text(encoding="utf-8")
        for headcount in ["Engineering & Operations | 26", "Quality Assurance | 12", "Supply Chain | 11", "Finance | 9", "People & Culture | 12"]:
            self.assertIn(headcount, org)
        self.assertIn("**Total** | **70**", org)
        raci = (PROJECT / "RACI_MATRIX.md").read_text(encoding="utf-8")
        self.assertEqual(25, len(re.findall(r"^\| RACI-\d{2} \|", raci, flags=re.MULTILINE)))
        uat = (PROJECT / "UAT_TEST_REGISTER.md").read_text(encoding="utf-8")
        self.assertEqual([f"UAT-{i:03d}" for i in range(1, 15)], re.findall(r"^### (UAT-\d{3})\b", uat, flags=re.MULTILINE))
        self.assertIn("Defect Severity", uat)
        self.assertIn("Entry Criteria", uat)
        self.assertIn("Exit Criteria", uat)
    def test_dashboard_embeds_csv_source_data_and_accessible_controls(self):
        html = (PROJECT / "index.html").read_text(encoding="utf-8")
        self.assertIn("https://cdn.tailwindcss.com", html)
        self.assertIn("https://cdn.jsdelivr.net/npm/chart.js", html)
        self.assertIn("93.4%", html)
        self.assertIn("88.5%", html)
        self.assertIn("24.2", html)
        self.assertIn("20", html)
        self.assertIn("3", html)
        for element_id in [
            "employee-search", "department-filter", "status-filter", "grade-filter",
            "records-table-body", "detail-dialog", "socialization-chart", "sla-role-chart",
            "milestone-chart", "delay-chart",
        ]:
            self.assertIn(f'id="{element_id}"', html)
        self.assertIn('aria-label="Search onboarding records"', html)
        self.assertIn("prefers-reduced-motion", html)
        self.assertNotIn("document.write", html)
        self.assertNotIn("eval(", html)
        records_match = re.search(r'<script id="records-data" type="application/json">(.*?)</script>', html, re.DOTALL)
        tasks_match = re.search(r'<script id="tasks-data" type="application/json">(.*?)</script>', html, re.DOTALL)
        self.assertIsNotNone(records_match)
        self.assertIsNotNone(tasks_match)
        embedded_records = json.loads(records_match.group(1))
        embedded_tasks = json.loads(tasks_match.group(1))
        _, csv_records = read_csv("synthetic_onboarding_records.csv")
        _, csv_tasks = read_csv("synthetic_onboarding_tasks.csv")
        self.assertEqual(csv_records, embedded_records)
        self.assertEqual(csv_tasks, embedded_tasks)
        forbidden = re.compile(r"\b(TODO|TBD|lorem ipsum|insert here|placeholder)\b", re.IGNORECASE)
        for filename in EXPECTED_FILES:
            if filename.endswith((".md", ".html")):
                self.assertIsNone(forbidden.search((PROJECT / filename).read_text(encoding="utf-8")), filename)

    def test_enterprise_dashboard_actions_and_quick_filters(self):
        html = (PROJECT / "index.html").read_text(encoding="utf-8")
        for token in [
            "Plus+Jakarta+Sans", "family=Inter", "backdrop-filter: blur(12px)",
            'id="export-cohort"', 'id="print-report"', 'id="reset-filters"',
            'id="quick-filter-all"', 'id="quick-filter-escalated"',
            'id="quick-filter-progress"', 'id="quick-filter-completed"',
            "All Cohort", "Action Needed", "Fully Completed",
            "URL.createObjectURL", "text/csv;charset=utf-8", "window.print()",
            "@media print", "Chart.defaults.plugins.tooltip",
        ]:
            self.assertIn(token, html)
        for color in ["#10b981", "#36d6c4", "#f43f5e"]:
            self.assertIn(color, html)

    def test_slide_deck_is_exactly_five_print_safe_slides(self):
        html = (PROJECT / "slides.html").read_text(encoding="utf-8")
        self.assertEqual(5, len(re.findall(r'<section\s+class="[^"]*\bslide\b', html)))
        for slide_number in range(1, 6):
            self.assertIn(f'id="slide-{slide_number}"', html)
        for token in [
            "HR OPERATIONS LAB · A BETTER WAY TO ONBOARD",
            "How to Build a Great 90-Day Onboarding System",
            "A practical HR system that helps new hires learn fast, feel welcome, and succeed from Day 1.",
            "Clear Checklists", "No IT Delays", "Friendly Buddy System", "Live Dashboard",
            "THE CHALLENGE", "Why Most Onboarding Fails (And How We Fix It)",
            "The Old Way", "Laptops, emails, and logins arrive days late",
            "Managers forget to hold weekly 1-on-1 check-ins",
            "New hires feel lost, confused, and unsupported",
            "Good people quit within their first 3 months",
            "Our Way", "Everything set up and ready before Day 1",
            "A dedicated friendly buddy from your first week",
            "Clear 30, 60, and 90-day goals with your manager",
            "Continuous support so nobody gets left behind",
            "THE 4-STEP FRAMEWORK", "The 4 Keys to Helping New Hires Succeed",
            "Clear Goals", "Doing the Work", "Feeling Welcome", "Big Picture",
            "I know exactly what my job is and what success looks like.",
            "I can do my daily tasks on my own with confidence.",
            "I have a helpful buddy, great teammates, and feel at home.",
            "I understand our company's mission and where we are heading.",
            "Before Day 1", "Day 1 Welcome", "Week 1 Basics",
            "Month 1 Goals", "Month 2 Practice", "Month 3 Confirmation",
            "WHO DOES WHAT", "Clear Roles &amp; Built-In Quality Checks",
            "HR Team", "Manager", "IT Team", "Peer Buddy",
            "Fast Help", "Data Privacy", "14 System Tests",
            "LIVE RESULTS", "Real-Time Tracking: The Live Dashboard",
            "93.4%", "88.5%", "24 Days", "20 Hires", "3 Flags",
            "Ready on Day 1", "On-Time Tasks", "To Clear Goals",
            "Tracked in 2026 Cohort", "Solved Early",
            "Explore the live interactive dashboard",
            "https://azim-ux.github.io/evidence-based-onboarding-lab/",
            "linear-gradient(135deg, #ffffff 30%, #36d6c4 75%, #6596ff 100%)",
            "-webkit-background-clip: text", "-webkit-text-fill-color: transparent",
            "font-size: clamp(0.85rem, 1.1vw, 1.05rem);",
            "font-size: clamp(2.2rem, 4.5vw, 3.8rem);",
            "font-size: clamp(1.15rem, 1.6vw, 1.5rem);",
            "font-size: clamp(0.95rem, 1.3vw, 1.25rem);",
            "font-size: clamp(0.85rem, 1.05vw, 1.05rem);",
            "font-size: clamp(2.2rem, 4vw, 3.8rem);",
            "font-size: clamp(0.9rem, 1.15vw, 1.1rem);",
            "#e2e8f0", "#cbd5e1", "IntersectionObserver",
            "touchstart", "wheel", "ArrowRight", "ArrowLeft",
            "@media print", "@page { size: 16in 9in; margin: 0; }",
            "page-break-after", "print-color-adjust: exact",
            "height: 100vh", "height: 100dvh", "overflow: hidden",
            "max-height: 700px", "max-height: 600px", "max-height: 500px",
            "prefers-reduced-motion",
        ]:
            self.assertIn(token, html)

        for declaration in re.findall(r"font-size:\s*([^;]+)", html):
            value = declaration.strip()
            match = re.match(r"clamp\(\s*([0-9.]+)(px|rem|em)", value)
            if not match:
                match = re.match(r"([0-9.]+)(px|rem|em)$", value)
            if match:
                amount = float(match.group(1))
                pixels = amount if match.group(2) == "px" else amount * 16
                self.assertGreaterEqual(
                    pixels,
                    13.6,
                    f"Micro-text is not allowed: font-size: {declaration}",
                )

        pdf_path = PROJECT / "Evidence_Based_Onboarding_HR_Operations_Case_Study.pdf"
        self.assertTrue(pdf_path.read_bytes().startswith(b"%PDF-"))
        self.assertGreater(pdf_path.stat().st_size, 100_000)
        pdf_metadata = subprocess.run(
            ["pdfinfo", str(pdf_path)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertRegex(pdf_metadata, r"(?m)^Pages:\s+5$")
        self.assertRegex(pdf_metadata, r"(?m)^Page size:\s+1152 x 648 pts")

    def test_public_release_license_and_portfolio_hub(self):
        license_text = (PROJECT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(license_text.startswith("MIT License\n"))
        self.assertIn("Copyright (c) 2026 Mohammad Azimuddin", license_text)
        self.assertIn("THE SOFTWARE IS PROVIDED \"AS IS\"", license_text)
        hub = (ROOT / "06_Portfolio_Projects" / "README.md").read_text(encoding="utf-8")
        project_names = [
            "03_Evidence_Based_Onboarding_HR_Operations_Lab",
            "02_UAE_Workforce_Planning_and_Total_Rewards",
            "01_Synthetic_HR_Analytics_Dashboard",
        ]
        for project_name in project_names:
            self.assertIn(project_name, hub)
        self.assertLess(hub.index(project_names[0]), hub.index(project_names[1]))
        self.assertLess(hub.index(project_names[1]), hub.index(project_names[2]))

    def test_enterprise_leadership_governance_and_employee_experience_controls(self):
        raci = (PROJECT / "RACI_MATRIX.md").read_text(encoding="utf-8")
        for token in [
            "Level 1", "> 24 hours", "Task Owner", "Hiring Manager",
            "Level 2", "> 48 hours", "HR Operations Specialist", "daily stand-up",
            "Level 3", "> 72 hours", "Head of HR Operations",
            "Day-1 badge/system access hold", "emergency task reassignment",
            "Standard BGV", "7 business days", "Fast-Track BGV", "3 business days",
        ]:
            self.assertIn(token, raci)

        onboarding = (PROJECT / "ONBOARDING_TEMPLATES_30_60_90.md").read_text(encoding="utf-8")
        for token in [
            "T-10 Days", "Buddy welcome message", "T-5 Days",
            "courier dispatch tracking number", "T-2 Days", "What to Expect on Day 1",
            "dress code", "arrival time", "parking/security badge instructions",
            "OKR clarity", "resource roadblocks", "workload calibration", "buddy feedback",
            "APD-2026-015", "APD-2026-018", "APD-2026-020",
            "Bi-weekly HRBP coaching", "weekly milestone targets", "Day 120",
            "confidential", "buddy reassignment",
        ]:
            self.assertIn(token, onboarding)

    def test_enterprise_architecture_and_segmented_onboarding_are_documented(self):
        org = (PROJECT / "ORGANIZATION_AND_ROLES.md").read_text(encoding="utf-8")
        for token in [
            "```mermaid", "flowchart LR", "Applicant Tracking System (ATS)",
            "JSON Webhook", "Frappe HR / Employee Master", "SCIM / REST API",
            "Identity Provider / Active Directory", "Okta", "Azure AD",
            "Auto-Provision", "Google Workspace", "ERP", "Slack",
            "Plant/Technician Roles (G5)", "EHS", "physical badge", "machine clearance",
            "Desk/Engineering Roles (G1–G4)", "cloud repositories", "IDE access",
            "remote-work compliance", "not the APD-G5 employee grade",
        ]:
            self.assertIn(token, org)

    def test_four_pillar_instrument_and_reconciled_cost_model_are_documented(self):
        exact_items = [
            'I have a clear understanding of the goals, priorities, and performance expectations for my role.',
            'I can independently execute my daily operating procedures without frequent supervisor intervention.',
            'I feel welcomed, supported by my buddy, and psychologically safe within my immediate team.',
            "I understand how my department's goals align with APD's strategic mission and governance policies.",
        ]
        for filename in ["RESEARCH_FOUNDATION.md", "DATA_DICTIONARY.md"]:
            document = (PROJECT / filename).read_text(encoding="utf-8")
            for item in exact_items:
                self.assertIn(item, document)
            self.assertGreaterEqual(document.count("[1–5]"), 4)
            self.assertIn("project-authored", document)
            self.assertIn("Cost of 3-Day Workstation Delay", document)
            self.assertIn("$1,250/day", document)
            self.assertIn("~$2,450", document)
            self.assertIn("cannot be reconciled", document)
            self.assertIn("$4,903.85", document)

    def test_internal_career_and_launch_assets_are_absent(self):
        actual = {path.name for path in PROJECT.iterdir() if path.is_file()}
        self.assertTrue(INTERNAL_FILES.isdisjoint(actual))

    def test_readme_lists_only_the_public_release_artifacts(self):
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        for filename in EXPECTED_FILES - {"README.md", ".gitignore"}:
            self.assertIn(f"]({filename})", readme, filename)
        for filename in INTERNAL_FILES:
            self.assertNotIn(filename, readme)

    def test_standalone_publication_entrypoint_and_ignore_rules(self):
        self.assertEqual(
            ".DS_Store\n"
            ".DS_Store?\n"
            "._*\n"
            ".Spotlight-V100\n"
            ".Trashes\n"
            "ehthumbs.db\n"
            "Thumbs.db\n"
            "__pycache__/\n"
            "*.pyc\n"
            "*.tmp\n"
            "*.log\n"
            "*.canvas\n"
            "*.docx\n"
            ".env*\n"
            "graphify-out/\n"
            ".obsidian/\n"
            ".claude/\n"
            ".gstack/\n"
            "tmp/\n"
            ".vscode/\n"
            ".idea/\n",
            (PROJECT / ".gitignore").read_text(encoding="utf-8"),
        )
        readme = (PROJECT / "README.md").read_text(encoding="utf-8")
        for token in [
            "https://azim-ux.github.io/evidence-based-onboarding-lab/",
            "https://azim-ux.github.io/evidence-based-onboarding-lab/slides.html",
        ]:
            self.assertIn(token, readme)
        for path in PROJECT.iterdir():
            if path.suffix in {".md", ".html"}:
                content = path.read_text(encoding="utf-8")
                self.assertNotIn("YOUR_GITHUB_USERNAME", content, path.name)


if __name__ == "__main__":
    unittest.main()
