import csv
import json
import re
import unittest
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "06_Portfolio_Projects" / "04_Structured_Hiring_and_ATS_Lab"

EXPECTED_FILES = {
    "synthetic_requisitions.csv",
    "synthetic_candidates.csv",
    "synthetic_interviews.csv",
    "README.md",
    "RESEARCH_FOUNDATION.md",
    "REQUISITIONS_AND_ROLES.md",
    "STRUCTURED_INTERVIEW_RUBRICS.md",
    "ATS_WORKFLOW_AND_RACI.md",
    "SELECTION_VALIDITY_MODEL.md",
    "COMPLIANCE_AND_FAIRNESS_MATRIX.md",
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

REQUISITION_HEADERS = [
    "Requisition_ID", "Job_Title", "Department", "Grade", "Hiring_Manager_ID",
    "Target_Headcount", "Open_Date", "Close_Date", "Days_to_Fill", "Status",
    "Sourcing_Channel_Primary", "Total_Applicants", "Shortlisted", "Interviewed",
    "Offered", "Hired",
]

CANDIDATE_HEADERS = [
    "Candidate_ID", "Full_Name", "Gender", "Demographic_Cohort", "Requisition_ID",
    "Applied_Date", "Source_Channel", "Current_Stage", "Disposition_Reason",
    "Resume_Screen_Score", "Phone_Screen_Score", "Work_Sample_Score",
    "Structured_Interview_Score", "Job_Knowledge_Score", "Composite_Score",
    "Subjective_Impression_Score", "Bias_Variance_Gap", "Offer_Extended",
    "Offer_Accepted", "Hired_Date",
]

INTERVIEW_HEADERS = [
    "Interview_ID", "Candidate_ID", "Requisition_ID", "Stage_Name", "Interviewer_ID",
    "Interviewer_Role", "Scheduled_Date", "Feedback_Submitted_Date", "Turnaround_Hours",
    "SLA_Met", "BARS_Score_1", "BARS_Score_2", "BARS_Score_3", "BARS_Score_4",
    "Mean_BARS_Score", "Notes_Summary",
]


def read_csv(name):
    with (PROJECT / name).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


class StructuredHiringATSLabAcceptanceTests(unittest.TestCase):
    def test_01_exact_file_inventory(self):
        self.assertTrue(PROJECT.is_dir(), f"Missing project directory: {PROJECT}")
        actual = {path.name for path in PROJECT.iterdir() if path.is_file()}
        self.assertEqual(EXPECTED_FILES, actual)

    def test_02_schemas_identity_sequences_and_referential_integrity(self):
        req_headers, requisitions = read_csv("synthetic_requisitions.csv")
        cand_headers, candidates = read_csv("synthetic_candidates.csv")
        int_headers, interviews = read_csv("synthetic_interviews.csv")
        self.assertEqual(REQUISITION_HEADERS, req_headers)
        self.assertEqual(CANDIDATE_HEADERS, cand_headers)
        self.assertEqual(INTERVIEW_HEADERS, int_headers)
        self.assertEqual(5, len(requisitions))
        self.assertEqual(4_000, len(candidates))
        self.assertEqual(2_000, len(interviews))
        self.assertEqual(
            [f"CAND-2026-{number:04d}" for number in range(1, 4_001)],
            [row["Candidate_ID"] for row in candidates],
        )
        self.assertEqual(
            [f"INT-2026-{number:04d}" for number in range(1, 2_001)],
            [row["Interview_ID"] for row in interviews],
        )
        requisition_ids = {row["Requisition_ID"] for row in requisitions}
        candidate_ids = {row["Candidate_ID"] for row in candidates}
        self.assertTrue(all(row["Requisition_ID"] in requisition_ids for row in candidates))
        self.assertTrue(all(row["Requisition_ID"] in requisition_ids for row in interviews))
        self.assertTrue(all(row["Candidate_ID"] in candidate_ids for row in interviews))
        candidate_req = {row["Candidate_ID"]: row["Requisition_ID"] for row in candidates}
        self.assertTrue(
            all(candidate_req[row["Candidate_ID"]] == row["Requisition_ID"] for row in interviews)
        )

    def test_03_reconciled_governed_kpis(self):
        _, requisitions = read_csv("synthetic_requisitions.csv")
        _, candidates = read_csv("synthetic_candidates.csv")
        _, interviews = read_csv("synthetic_interviews.csv")
        hired = [row for row in candidates if row["Current_Stage"] == "Hired"]
        self.assertEqual(120, len(hired))
        conversion = Decimal(len(hired)) / Decimal(len(candidates)) * Decimal("100")
        self.assertEqual(Decimal("3.00"), conversion)
        expected_requisitions = {
            "REQ-2026-ENG-G4": (800, 10, Decimal("34.0")),
            "REQ-2026-ENG-G1": (1600, 60, Decimal("22.0")),
            "REQ-2026-QUA-G3": (600, 15, Decimal("30.0")),
            "REQ-2026-PNC-G2": (400, 10, Decimal("26.0")),
            "REQ-2026-SCM-G2": (600, 25, Decimal("30.5")),
        }
        self.assertEqual(expected_requisitions, {
            row["Requisition_ID"]: (
                int(row["Total_Applicants"]), int(row["Hired"]), Decimal(row["Days_to_Fill"])
            )
            for row in requisitions
        })
        for requisition_id, (applicants, req_hires, _) in expected_requisitions.items():
            self.assertEqual(applicants, sum(row["Requisition_ID"] == requisition_id for row in candidates))
            self.assertEqual(req_hires, sum(
                row["Requisition_ID"] == requisition_id and row["Current_Stage"] == "Hired"
                for row in candidates
            ))
        mean_time_to_fill = sum(Decimal(row["Days_to_Fill"]) for row in requisitions) / Decimal(5)
        self.assertEqual(Decimal("28.5"), mean_time_to_fill)
        on_time = [row for row in interviews if row["SLA_Met"] == "Yes"]
        late = [row for row in interviews if row["SLA_Met"] == "No"]
        self.assertEqual(1_836, len(on_time))
        self.assertEqual(164, len(late))
        self.assertTrue(all(Decimal(row["Turnaround_Hours"]) <= 48 for row in on_time))
        self.assertTrue(all(Decimal(row["Turnaround_Hours"]) > 48 for row in late))
        sla_rate = Decimal(len(on_time)) / Decimal(len(interviews)) * Decimal("100")
        self.assertEqual(Decimal("91.800"), sla_rate)
        reference = [row for row in candidates if row["Demographic_Cohort"] == "Reference Group"]
        focal = [row for row in candidates if row["Demographic_Cohort"] == "Focal Group"]
        self.assertEqual((2_400, 1_600), (len(reference), len(focal)))
        self.assertEqual((624, 362), (
            sum(row["Phone_Screen_Score"] != "" for row in reference),
            sum(row["Phone_Screen_Score"] != "" for row in focal),
        ))
        air = (Decimal(362) / Decimal(1600)) / (Decimal(624) / Decimal(2400))
        self.assertEqual(Decimal("0.87"), air.quantize(Decimal("0.01")))

    def test_04_scoring_math_and_bias_control_case(self):
        _, candidates = read_csv("synthetic_candidates.csv")
        scored = [row for row in candidates if row["Composite_Score"]]
        self.assertEqual(500, len(scored))
        for row in scored:
            expected = (
                Decimal("0.40") * Decimal(row["Work_Sample_Score"])
                + Decimal("0.40") * Decimal(row["Structured_Interview_Score"])
                + Decimal("0.20") * Decimal(row["Job_Knowledge_Score"])
            ).quantize(Decimal("0.01"))
            self.assertEqual(expected, Decimal(row["Composite_Score"]), row["Candidate_ID"])
            gap = (Decimal(row["Subjective_Impression_Score"]) - expected).quantize(Decimal("0.01"))
            self.assertEqual(gap, Decimal(row["Bias_Variance_Gap"]), row["Candidate_ID"])
        interview_counts = {}
        _, interviews = read_csv("synthetic_interviews.csv")
        for interview in interviews:
            interview_counts[interview["Candidate_ID"]] = interview_counts.get(interview["Candidate_ID"], 0) + 1
        self.assertEqual({row["Candidate_ID"] for row in scored}, set(interview_counts))
        self.assertEqual({4}, set(interview_counts.values()))
        control = next(row for row in candidates if row["Candidate_ID"] == "CAND-2026-0013")
        self.assertEqual("4.60", control["Subjective_Impression_Score"])
        self.assertEqual("3.92", control["Composite_Score"])
        self.assertEqual("0.68", control["Bias_Variance_Gap"])
        self.assertNotEqual("Hired", control["Current_Stage"])

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
            self.assertTrue(domains <= {"apexprecision.test", "example.com"}, (path.name, domains))
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
        for token in ["Sackett", "2022", "Schmidt", "Hunter", "1998", "Campion", "1997", "non-causal"]:
            self.assertIn(token, research)
        for token in ["4,000", "statistical power", "large-sample"]:
            self.assertIn(token, research)
        rubric = (PROJECT / "STRUCTURED_INTERVIEW_RUBRICS.md").read_text(encoding="utf-8")
        for competency in [
            "Technical Problem Solving & Quality Mindset",
            "Stakeholder Collaboration & Conflict Resolution",
            "Process Optimization & Continuous Improvement",
            "Adaptability & Ethical Governance",
        ]:
            self.assertIn(competency, rubric)
        for anchor in ["1 — Unsatisfactory", "3 — Proficient", "5 — Role Model"]:
            self.assertGreaterEqual(rubric.count(anchor), 4)
        raci = (PROJECT / "ATS_WORKFLOW_AND_RACI.md").read_text(encoding="utf-8")
        self.assertEqual(20, len(re.findall(r"^\| RACI-\d{2} \|", raci, flags=re.MULTILINE)))
        for token in ["24-hour reminder", "48-hour deadline", "72-hour hold"]:
            self.assertIn(token, raci)
        uat = (PROJECT / "UAT_TEST_REGISTER.md").read_text(encoding="utf-8")
        self.assertEqual(
            [f"UAT-{number:03d}" for number in range(1, 15)],
            re.findall(r"^### (UAT-\d{3})\b", uat, flags=re.MULTILINE),
        )
        privacy = (PROJECT / "RBAC_AND_PRIVACY_MATRIX.md").read_text(encoding="utf-8")
        for token in ["180 days", "Right to be Forgotten", "DPDP", "least privilege"]:
            self.assertIn(token, privacy)
        selection = (PROJECT / "SELECTION_VALIDITY_MODEL.md").read_text(encoding="utf-8")
        for token in ["Taylor–Russell", "Brogden–Cronbach–Gleser", "120"]:
            self.assertIn(token, selection)
        fairness = (PROJECT / "COMPLIANCE_AND_FAIRNESS_MATRIX.md").read_text(encoding="utf-8")
        for token in ["Chi-square", "624 / 2,400", "362 / 1,600"]:
            self.assertIn(token, fairness)

    def test_07_html_embeds_source_identical_json_and_required_ui(self):
        _, requisitions = read_csv("synthetic_requisitions.csv")
        _, candidates = read_csv("synthetic_candidates.csv")
        _, interviews = read_csv("synthetic_interviews.csv")
        for filename in ["index.html", "dashboard.html"]:
            html = (PROJECT / filename).read_text(encoding="utf-8")
            self.assertIn("https://cdn.tailwindcss.com", html)
            self.assertIn("https://cdn.jsdelivr.net/npm/chart.js", html)
            for value in ["4,000", "3.0%", "28.5d", "91.8%", "0.87"]:
                self.assertIn(value, html)
            for element_id in [
                "candidate-search", "requisition-filter", "stage-filter", "status-filter",
                "pipeline-table-body", "scorecard-drawer", "close-scorecard", "funnel-chart",
                "bias-chart", "sla-chart", "fairness-chart", "page-size", "previous-page",
                "next-page", "page-indicator",
            ]:
                self.assertIn(f'id="{element_id}"', html, (filename, element_id))
            embedded = {}
            for key in ["requisitions", "candidates", "interviews"]:
                match = re.search(
                    rf'<script id="{key}-data" type="application/json">(.*?)</script>',
                    html,
                    flags=re.DOTALL,
                )
                self.assertIsNotNone(match, (filename, key))
                embedded[key] = json.loads(match.group(1))
            self.assertEqual(requisitions, embedded["requisitions"])
            self.assertEqual(candidates, embedded["candidates"])
            self.assertEqual(interviews, embedded["interviews"])
            self.assertIn("prefers-reduced-motion", html)
            self.assertIn("requestAnimationFrame", html)
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
        for token in ["4,000", "120", "3.0%", "28.5d", "91.8%", "0.87"]:
            self.assertIn(token, html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
