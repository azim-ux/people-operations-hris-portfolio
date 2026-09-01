"""Tests for the UAE workforce planning and total rewards portfolio project."""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "98_Maintenance/generate_uae_workforce_project.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("uae_workforce_generator", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load generator from {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WorkforceProjectUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()

    def setUp(self):
        self.bands = self.generator.create_salary_bands()
        self.employees = self.generator.create_employee_records(self.bands)
        self.monthly = self.generator.create_monthly_workforce()
        self.requisitions = self.generator.create_requisitions()

    def test_salary_bands_are_unique_and_ordered(self):
        keys = {(row["Job_Family"], row["Job_Level"]) for row in self.bands}
        self.assertEqual(len(keys), len(self.bands))
        self.assertGreaterEqual(len(self.bands), 20)
        for row in self.bands:
            self.assertLess(row["Band_Min_AED"], row["Band_Mid_AED"])
            self.assertLess(row["Band_Mid_AED"], row["Band_Max_AED"])

    def test_employee_records_are_deterministic_private_and_relationally_valid(self):
        repeated = self.generator.create_employee_records(self.bands)
        self.assertEqual(self.employees, repeated)
        self.assertEqual(len(self.employees), 650)
        self.assertEqual(len({row["Employee_ID"] for row in self.employees}), 650)

        forbidden_fields = {"Name", "Email", "Phone", "Address", "Passport_Number"}
        self.assertTrue(forbidden_fields.isdisjoint(self.employees[0]))

        band_lookup = {
            (row["Job_Family"], row["Job_Level"]): row for row in self.bands
        }
        statuses = {row["Employment_Status"] for row in self.employees}
        self.assertEqual(statuses, {"Active", "Exited"})
        self.assertGreater(sum(row["Employment_Status"] == "Active" for row in self.employees), 450)
        self.assertGreater(sum(row["Employment_Status"] == "Exited" for row in self.employees), 50)

        for row in self.employees:
            band = band_lookup[(row["Job_Family"], row["Job_Level"])]
            self.assertGreaterEqual(row["Monthly_Salary_AED"], band["Band_Min_AED"])
            self.assertLessEqual(row["Monthly_Salary_AED"], band["Band_Max_AED"])
            if row["Employment_Status"] == "Active":
                self.assertEqual(row["Exit_Date"], "")
            else:
                self.assertNotEqual(row["Exit_Date"], "")

    def test_monthly_workforce_balances_and_rolls_forward(self):
        self.assertEqual(len(self.monthly), 24 * 6)
        by_department = defaultdict(list)
        for row in self.monthly:
            self.assertEqual(
                row["Closing_Headcount"],
                row["Opening_Headcount"] + row["Hires"] - row["Exits"],
            )
            self.assertGreater(row["Payroll_Cost_AED"], 0)
            self.assertGreater(row["Payroll_Budget_AED"], 0)
            by_department[row["Department"]].append(row)

        self.assertEqual(len(by_department), 6)
        for rows in by_department.values():
            rows.sort(key=lambda row: row["Month"])
            for previous, current in zip(rows, rows[1:]):
                self.assertEqual(previous["Closing_Headcount"], current["Opening_Headcount"])

        latest_month = max(row["Month"] for row in self.monthly)
        latest_closing_headcount = sum(
            row["Closing_Headcount"] for row in self.monthly if row["Month"] == latest_month
        )
        active_employee_records = sum(
            row["Employment_Status"] == "Active" for row in self.employees
        )
        self.assertEqual(latest_closing_headcount, active_employee_records)

    def test_recruitment_funnel_is_monotonic_and_costed(self):
        self.assertGreaterEqual(len(self.requisitions), 40)
        for row in self.requisitions:
            self.assertGreaterEqual(row["Applications"], row["Screened"])
            self.assertGreaterEqual(row["Screened"], row["Interviewed"])
            self.assertGreaterEqual(row["Interviewed"], row["Offers"])
            self.assertGreaterEqual(row["Offers"], row["Hires"])
            self.assertGreaterEqual(row["Recruitment_Cost_AED"], 0)
            if row["Status"] == "Closed":
                self.assertGreater(row["Time_to_Fill_Days"], 0)

    def test_metric_helpers_use_defensible_denominators(self):
        self.assertEqual(self.generator.compa_ratio(9_000, 10_000), 0.9)
        self.assertEqual(self.generator.compa_ratio(9_000, 0), 0.0)
        self.assertEqual(self.generator.turnover_rate(24, 200), 12.0)
        self.assertEqual(self.generator.turnover_rate(1, 0), 0.0)

    def test_scenarios_disclose_assumptions_and_change_decision_outputs(self):
        summary = self.generator.calculate_summary(
            self.employees, self.monthly, self.requisitions, self.bands
        )
        scenarios = self.generator.build_scenarios(summary)
        names = {row["Scenario"] for row in scenarios}
        self.assertEqual(names, {"Baseline", "Targeted Retention", "Growth-First"})

        lookup = {row["Scenario"]: row for row in scenarios}
        self.assertLess(
            lookup["Targeted Retention"]["Expected_Exits"],
            lookup["Baseline"]["Expected_Exits"],
        )
        for row in scenarios:
            self.assertTrue(row["Assumption"])
            self.assertGreater(row["Projected_People_Cost_AED"], 0)

    def test_validator_reports_duplicate_ids_and_broken_funnel(self):
        duplicate_employees = self.employees + [dict(self.employees[0])]
        broken_requisitions = [dict(row) for row in self.requisitions]
        broken_requisitions[0]["Offers"] = broken_requisitions[0]["Interviewed"] + 1
        errors = self.generator.validate_project_data(
            self.bands, duplicate_employees, self.monthly, broken_requisitions
        )
        self.assertTrue(any("duplicate employee" in error.lower() for error in errors))
        self.assertTrue(any("funnel" in error.lower() for error in errors))


class WorkforceProjectIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generator = load_generator()

    def test_main_generates_complete_portfolio_package(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            result = self.generator.main(project)

            expected_files = {
                "employee_records.csv",
                "salary_bands.csv",
                "monthly_workforce.csv",
                "recruitment_funnel.csv",
                "workforce_scenarios.csv",
                "dashboard.html",
                "index.html",
                "README.md",
                "REQUIREMENTS.md",
                "DATA_DICTIONARY.md",
                "METHODOLOGY_AND_LIMITATIONS.md",
                "EXECUTIVE_DECISION_MEMO.md",
                "POWER_BI_BUILD_GUIDE.md",
                "INTERVIEW_GUIDE.md",
                "LINKEDIN_POST.md",
                "CV_PROJECT_ENTRY.md",
                "LINKEDIN_CASE_STUDY.md",
                "PUBLICATION_CHECKLIST.md",
                "GITHUB_PUBLISHING_GUIDE.md",
            }
            self.assertEqual(expected_files, {path.name for path in project.iterdir()})
            self.assertEqual(result["employee_records"], 650)

            with (project / "employee_records.csv").open(
                "r", encoding="utf-8", newline=""
            ) as handle:
                employee_rows = list(csv.DictReader(handle))
            self.assertEqual(len(employee_rows), 650)
            self.assertIn("Monthly_Salary_AED", employee_rows[0])

            dashboard = (project / "dashboard.html").read_text(encoding="utf-8")
            self.assertIn("UAE Workforce Planning & Total Rewards", dashboard)
            self.assertIn("Entirely synthetic", dashboard)
            self.assertIn('id="scenario-select"', dashboard)
            self.assertIn('data-section="rewards"', dashboard)
            self.assertIn('data-section="recruitment"', dashboard)
            self.assertIn("Projected people cost", dashboard)
            self.assertEqual(
                (project / "dashboard.html").read_bytes(),
                (project / "index.html").read_bytes(),
            )

            memo = (project / "EXECUTIVE_DECISION_MEMO.md").read_text(encoding="utf-8")
            self.assertIn("Decision requested", memo)
            self.assertIn("Targeted Retention", memo)
            self.assertIn("not a forecast", memo)

            linkedin_post = (project / "LINKEDIN_POST.md").read_text(encoding="utf-8")
            self.assertIn("650 synthetic employee records", linkedin_post)
            self.assertIn("24 months", linkedin_post)
            self.assertIn("entirely synthetic", linkedin_post.lower())
            self.assertIn("#PeopleAnalytics", linkedin_post)
            for banned_phrase in (
                "game-changer",
                "rapidly evolving landscape",
                "excited to announce my journey",
            ):
                self.assertNotIn(banned_phrase, linkedin_post.lower())

            cv_entry = (project / "CV_PROJECT_ENTRY.md").read_text(encoding="utf-8")
            self.assertIn("Independent Portfolio Project", cv_entry)
            self.assertIn("Power BI-ready", cv_entry)
            self.assertIn("Entirely synthetic", cv_entry)
            self.assertNotIn("production Oracle HCM", cv_entry)
            self.assertNotIn("predictive model", cv_entry.lower())

            case_study = (project / "LINKEDIN_CASE_STUDY.md").read_text(encoding="utf-8")
            for heading in (
                "# UAE Workforce Planning and Total Rewards",
                "## Business question",
                "## Dataset and controls",
                "## Descriptive findings",
                "## Scenario comparison",
                "## Recommendation",
                "## Limitations",
            ):
                self.assertIn(heading, case_study)
            self.assertIn("11.0%", case_study)
            self.assertIn("AED 464,400", case_study)

            checklist = (project / "PUBLICATION_CHECKLIST.md").read_text(encoding="utf-8")
            self.assertIn("538", checklist)
            self.assertIn("57", checklist)
            self.assertIn("516.2", checklist)
            self.assertIn("11.0%", checklist)
            self.assertIn("public portfolio URL", checklist)
            self.assertIn("Do not publish", checklist)

            publishing_guide = (project / "GITHUB_PUBLISHING_GUIDE.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("GitHub Pages", publishing_guide)
            self.assertIn("index.html", publishing_guide)

    def test_generation_is_byte_for_byte_reproducible(self):
        with tempfile.TemporaryDirectory() as first_directory, tempfile.TemporaryDirectory() as second_directory:
            first = Path(first_directory)
            second = Path(second_directory)
            self.generator.main(first)
            self.generator.main(second)

            for name in (
                "employee_records.csv",
                "monthly_workforce.csv",
                "dashboard.html",
                "index.html",
                "LINKEDIN_POST.md",
                "CV_PROJECT_ENTRY.md",
                "LINKEDIN_CASE_STUDY.md",
            ):
                first_hash = hashlib.sha256((first / name).read_bytes()).hexdigest()
                second_hash = hashlib.sha256((second / name).read_bytes()).hexdigest()
                self.assertEqual(first_hash, second_hash)


if __name__ == "__main__":
    unittest.main()
