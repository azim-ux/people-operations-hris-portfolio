#!/usr/bin/env python3
"""Generate a reproducible UAE workforce-planning and total-rewards portfolio."""

from __future__ import annotations

import csv
import json
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "06_Portfolio_Projects/02_UAE_Workforce_Planning_and_Total_Rewards"
SEED = 20260828
AS_OF_DATE = date(2026, 7, 31)
COMPANY = "Gulf Horizon Services LLC (fictional)"
TOTAL_EMPLOYEE_RECORDS = 650
ACTIVE_EMPLOYEE_RECORDS = 538

DEPARTMENTS = [
    "Operations",
    "Sales",
    "Customer Experience",
    "Technology",
    "Finance",
    "People & Culture",
]
DEPARTMENT_WEIGHTS = [29, 19, 18, 15, 10, 9]
JOB_FAMILY_BY_DEPARTMENT = {
    "Operations": "Operations",
    "Sales": "Commercial",
    "Customer Experience": "Customer Experience",
    "Technology": "Technology",
    "Finance": "Finance",
    "People & Culture": "People & Culture",
}
JOB_LEVELS = ["L1", "L2", "L3", "L4"]
LEVEL_WEIGHTS = [42, 32, 20, 6]
LOCATIONS = ["Dubai", "Abu Dhabi", "Sharjah"]
LOCATION_WEIGHTS = [61, 27, 12]

EMPLOYEE_FIELDS = [
    "Employee_ID",
    "Department",
    "Job_Family",
    "Job_Level",
    "Location",
    "Gender",
    "Workforce_Category",
    "Employment_Type",
    "Hire_Date",
    "Exit_Date",
    "Employment_Status",
    "Monthly_Salary_AED",
    "Band_Mid_AED",
    "Compa_Ratio",
    "Performance_Rating",
    "Engagement_Score",
    "Training_Hours_YTD",
    "Absence_Days_YTD",
    "Critical_Role",
    "Regrettable_Exit",
]


def _choose(rng: random.Random, values: list[str], weights: list[int]) -> str:
    return rng.choices(values, weights=weights, k=1)[0]


def _month_keys() -> list[str]:
    keys = []
    year, month = 2024, 8
    for _ in range(24):
        keys.append(f"{year:04d}-{month:02d}")
        month += 1
        if month == 13:
            month = 1
            year += 1
    return keys


def _random_date(rng: random.Random, start: date, end: date) -> date:
    return start + timedelta(days=rng.randint(0, (end - start).days))


def _aed(value: float) -> str:
    return f"AED {value:,.0f}"


def compa_ratio(salary: float, midpoint: float) -> float:
    """Return salary divided by salary-band midpoint."""
    return round(salary / midpoint, 3) if midpoint else 0.0


def turnover_rate(leavers: int, average_headcount: float) -> float:
    """Return a percentage using average headcount as the denominator."""
    return round(leavers * 100 / average_headcount, 1) if average_headcount else 0.0


def create_salary_bands() -> list[dict[str, object]]:
    """Create hypothetical monthly AED salary bands for portfolio practice."""
    family_base = {
        "Operations": 7_200,
        "Commercial": 8_200,
        "Customer Experience": 6_800,
        "Technology": 11_500,
        "Finance": 9_200,
        "People & Culture": 8_400,
    }
    level_factor = {"L1": 1.0, "L2": 1.55, "L3": 2.35, "L4": 3.55}
    rows = []
    for family, base in family_base.items():
        for level in JOB_LEVELS:
            midpoint = round(base * level_factor[level] / 100) * 100
            rows.append(
                {
                    "Job_Family": family,
                    "Job_Level": level,
                    "Band_Min_AED": round(midpoint * 0.80 / 100) * 100,
                    "Band_Mid_AED": midpoint,
                    "Band_Max_AED": round(midpoint * 1.20 / 100) * 100,
                    "Benchmark_Status": "Hypothetical portfolio assumption",
                }
            )
    return rows


def create_employee_records(
    salary_bands: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Create 650 deterministic and privacy-safe employee records."""
    rng = random.Random(SEED + 1)
    band_lookup = {
        (str(row["Job_Family"]), str(row["Job_Level"])): row
        for row in salary_bands
    }
    exited_ids = set(
        rng.sample(
            range(1, TOTAL_EMPLOYEE_RECORDS + 1),
            TOTAL_EMPLOYEE_RECORDS - ACTIVE_EMPLOYEE_RECORDS,
        )
    )
    rows = []
    for index in range(1, TOTAL_EMPLOYEE_RECORDS + 1):
        department = _choose(rng, DEPARTMENTS, DEPARTMENT_WEIGHTS)
        family = JOB_FAMILY_BY_DEPARTMENT[department]
        level = _choose(rng, JOB_LEVELS, LEVEL_WEIGHTS)
        band = band_lookup[(family, level)]
        midpoint = int(band["Band_Mid_AED"])

        is_exited = index in exited_ids
        if is_exited:
            exit_date = _random_date(rng, date(2024, 8, 1), AS_OF_DATE)
            latest_hire = exit_date - timedelta(days=120)
            hire_date = _random_date(rng, date(2017, 1, 1), latest_hire)
            status = "Exited"
        else:
            exit_date = None
            hire_date = _random_date(rng, date(2016, 1, 1), date(2026, 6, 30))
            status = "Active"

        tenure_years = ((exit_date or AS_OF_DATE) - hire_date).days / 365.25
        tenure_adjustment = min(0.09, tenure_years * 0.008)
        salary_position = max(0.81, min(1.18, rng.gauss(0.94 + tenure_adjustment, 0.075)))
        salary = round(midpoint * salary_position / 100) * 100
        salary = max(int(band["Band_Min_AED"]), min(int(band["Band_Max_AED"]), salary))

        performance = min(5, max(1, round(rng.gauss(3.4, 0.8))))
        engagement = min(96, max(35, round(rng.gauss(73, 11) + (performance - 3) * 2)))
        training = max(0, round(rng.gauss(26, 13)))
        absence = max(0, round(rng.gauss(6, 3) + max(0, 68 - engagement) / 10))
        gender = _choose(rng, ["Woman", "Man"], [46, 54])
        workforce_category = _choose(rng, ["UAE National", "International"], [18, 82])
        employment_type = _choose(rng, ["Permanent", "Fixed-term"], [88, 12])
        critical_role = "Yes" if rng.random() < (0.22 if level in {"L3", "L4"} else 0.09) else "No"
        regrettable = ""
        if is_exited:
            regrettable = "Yes" if performance >= 4 or critical_role == "Yes" else "No"

        rows.append(
            {
                "Employee_ID": f"UAE-SYN-{index:04d}",
                "Department": department,
                "Job_Family": family,
                "Job_Level": level,
                "Location": _choose(rng, LOCATIONS, LOCATION_WEIGHTS),
                "Gender": gender,
                "Workforce_Category": workforce_category,
                "Employment_Type": employment_type,
                "Hire_Date": hire_date.isoformat(),
                "Exit_Date": exit_date.isoformat() if exit_date else "",
                "Employment_Status": status,
                "Monthly_Salary_AED": salary,
                "Band_Mid_AED": midpoint,
                "Compa_Ratio": compa_ratio(salary, midpoint),
                "Performance_Rating": performance,
                "Engagement_Score": engagement,
                "Training_Hours_YTD": training,
                "Absence_Days_YTD": absence,
                "Critical_Role": critical_role,
                "Regrettable_Exit": regrettable,
            }
        )
    return rows


def create_monthly_workforce() -> list[dict[str, object]]:
    """Create a balanced 24-month departmental workforce movement table."""
    rng = random.Random(SEED + 2)
    opening = {
        "Operations": 142,
        "Sales": 92,
        "Customer Experience": 86,
        "Technology": 72,
        "Finance": 48,
        "People & Culture": 41,
    }
    average_salary = {
        "Operations": 10_200,
        "Sales": 12_400,
        "Customer Experience": 9_300,
        "Technology": 17_800,
        "Finance": 14_200,
        "People & Culture": 13_100,
    }
    rows = []
    for month_index, month in enumerate(_month_keys()):
        for department in DEPARTMENTS:
            start = opening[department]
            exits = max(0, round(start * rng.uniform(0.004, 0.017)))
            growth_bias = 1 if month_index >= 12 and department in {"Operations", "Technology"} else 0
            hires = max(0, exits + rng.choice([-1, 0, 0, 1, 1]) + growth_bias)
            close = start + hires - exits
            salary_drift = 1 + month_index * 0.0025
            payroll = round(close * average_salary[department] * salary_drift / 100) * 100
            budget_variance = rng.uniform(-0.022, 0.035)
            budget = round(payroll * (1 + budget_variance) / 100) * 100
            rows.append(
                {
                    "Month": month,
                    "Department": department,
                    "Opening_Headcount": start,
                    "Hires": hires,
                    "Exits": exits,
                    "Closing_Headcount": close,
                    "Payroll_Cost_AED": payroll,
                    "Payroll_Budget_AED": budget,
                }
            )
            opening[department] = close

    latest_month = _month_keys()[-1]
    latest_rows = [row for row in rows if row["Month"] == latest_month]
    closing_difference = sum(int(row["Closing_Headcount"]) for row in latest_rows) - ACTIVE_EMPLOYEE_RECORDS
    if closing_difference:
        adjustment = next(row for row in latest_rows if row["Department"] == "Operations")
        if closing_difference > 0:
            adjustment["Exits"] = int(adjustment["Exits"]) + closing_difference
            adjustment["Closing_Headcount"] = int(adjustment["Closing_Headcount"]) - closing_difference
        else:
            adjustment["Hires"] = int(adjustment["Hires"]) - closing_difference
            adjustment["Closing_Headcount"] = int(adjustment["Closing_Headcount"]) - closing_difference
        prior_payroll = int(adjustment["Payroll_Cost_AED"])
        budget_ratio = int(adjustment["Payroll_Budget_AED"]) / prior_payroll
        revised_payroll = round(
            int(adjustment["Closing_Headcount"])
            * average_salary["Operations"]
            * (1 + 23 * 0.0025)
            / 100
        ) * 100
        adjustment["Payroll_Cost_AED"] = revised_payroll
        adjustment["Payroll_Budget_AED"] = round(revised_payroll * budget_ratio / 100) * 100
    return rows


def create_requisitions() -> list[dict[str, object]]:
    """Create a deterministic recruitment funnel with open and closed roles."""
    rng = random.Random(SEED + 3)
    month_starts = [date(int(key[:4]), int(key[5:]), 1) for key in _month_keys()]
    rows = []
    for index in range(1, 49):
        department = _choose(rng, DEPARTMENTS, DEPARTMENT_WEIGHTS)
        family = JOB_FAMILY_BY_DEPARTMENT[department]
        level = _choose(rng, JOB_LEVELS, [40, 34, 21, 5])
        start = month_starts[(index - 1) % len(month_starts)] + timedelta(days=rng.randint(0, 20))
        is_open = index > 42
        applications = rng.randint(35, 190)
        screened = rng.randint(max(8, round(applications * 0.20)), max(9, round(applications * 0.48)))
        interviewed = rng.randint(max(4, round(screened * 0.32)), max(5, round(screened * 0.65)))
        offers = rng.randint(1, max(1, min(interviewed, round(interviewed * 0.35))))
        if is_open:
            hires = rng.randint(0, min(offers, 1))
            status = "Open"
            close_date = ""
            time_to_fill = 0
        else:
            hires = rng.randint(1, min(offers, 3))
            status = "Closed"
            time_to_fill = rng.randint(24, 83)
            close_date = (start + timedelta(days=time_to_fill)).isoformat()
        cost = round((2_200 + applications * 12 + interviewed * 180 + hires * 1_200) / 100) * 100
        rows.append(
            {
                "Requisition_ID": f"REQ-SYN-{index:03d}",
                "Department": department,
                "Job_Family": family,
                "Job_Level": level,
                "Open_Date": start.isoformat(),
                "Close_Date": close_date,
                "Status": status,
                "Applications": applications,
                "Screened": screened,
                "Interviewed": interviewed,
                "Offers": offers,
                "Hires": hires,
                "Time_to_Fill_Days": time_to_fill,
                "Recruitment_Cost_AED": cost,
            }
        )
    return rows


def _department_metrics(employees: list[dict[str, object]]) -> list[dict[str, object]]:
    active = [row for row in employees if row["Employment_Status"] == "Active"]
    rows = []
    for department in DEPARTMENTS:
        subset = [row for row in active if row["Department"] == department]
        women = [row for row in subset if row["Gender"] == "Woman"]
        men = [row for row in subset if row["Gender"] == "Man"]
        women_salary = mean(float(row["Monthly_Salary_AED"]) for row in women) if women else 0
        men_salary = mean(float(row["Monthly_Salary_AED"]) for row in men) if men else 0
        raw_gap = (men_salary - women_salary) * 100 / men_salary if men_salary else 0
        rows.append(
            {
                "Department": department,
                "Active_Headcount": len(subset),
                "Average_Compa_Ratio": round(mean(float(row["Compa_Ratio"]) for row in subset), 3),
                "Below_090_Compa": sum(float(row["Compa_Ratio"]) < 0.90 for row in subset),
                "Average_Engagement": round(mean(int(row["Engagement_Score"]) for row in subset), 1),
                "Raw_Gender_Pay_Gap_Pct": round(raw_gap, 1),
            }
        )
    return rows


def calculate_summary(
    employees: list[dict[str, object]],
    monthly_workforce: list[dict[str, object]],
    requisitions: list[dict[str, object]],
    salary_bands: list[dict[str, object]],
) -> dict[str, object]:
    """Calculate the documented executive-level portfolio metrics."""
    del salary_bands  # bands are validated separately; employee rows carry the midpoint.
    active = [row for row in employees if row["Employment_Status"] == "Active"]
    trailing_start = date(2025, 8, 1)
    trailing_exits = [
        row
        for row in employees
        if row["Exit_Date"] and trailing_start <= date.fromisoformat(str(row["Exit_Date"])) <= AS_OF_DATE
    ]

    month_totals: dict[str, int] = defaultdict(int)
    for row in monthly_workforce:
        if str(row["Month"]) >= "2025-08":
            month_totals[str(row["Month"])] += int(row["Closing_Headcount"])
    average_headcount = mean(month_totals.values()) if month_totals else 0
    current_payroll_monthly = sum(int(row["Monthly_Salary_AED"]) for row in active)
    low_compa = [row for row in active if float(row["Compa_Ratio"]) < 0.90]
    annual_salary_correction = sum(
        max(0, round(float(row["Band_Mid_AED"]) * 0.90 - int(row["Monthly_Salary_AED"]))) * 12
        for row in low_compa
    )

    women = [row for row in active if row["Gender"] == "Woman"]
    men = [row for row in active if row["Gender"] == "Man"]
    women_average = mean(int(row["Monthly_Salary_AED"]) for row in women)
    men_average = mean(int(row["Monthly_Salary_AED"]) for row in men)
    raw_gap = (men_average - women_average) * 100 / men_average if men_average else 0

    closed = [row for row in requisitions if row["Status"] == "Closed"]
    total_offers = sum(int(row["Offers"]) for row in closed)
    total_hires = sum(int(row["Hires"]) for row in closed)
    average_annual_salary = current_payroll_monthly * 12 / len(active)
    replacement_cost_per_exit = average_annual_salary * 0.30

    return {
        "as_of_date": AS_OF_DATE.isoformat(),
        "active_headcount": len(active),
        "trailing_12_exits": len(trailing_exits),
        "average_headcount_12m": round(average_headcount, 1),
        "turnover_rate_pct": turnover_rate(len(trailing_exits), average_headcount),
        "annual_payroll_aed": current_payroll_monthly * 12,
        "average_annual_salary_aed": round(average_annual_salary),
        "employees_below_090_compa": len(low_compa),
        "annual_salary_correction_aed": round(annual_salary_correction),
        "raw_gender_pay_gap_pct": round(raw_gap, 1),
        "closed_requisitions": len(closed),
        "total_hires": total_hires,
        "offer_acceptance_rate_pct": round(total_hires * 100 / total_offers, 1) if total_offers else 0.0,
        "average_time_to_fill_days": round(mean(int(row["Time_to_Fill_Days"]) for row in closed), 1),
        "recruitment_cost_aed": sum(int(row["Recruitment_Cost_AED"]) for row in closed),
        "replacement_cost_per_exit_aed": round(replacement_cost_per_exit),
        "trailing_12_replacement_cost_aed": round(replacement_cost_per_exit * len(trailing_exits)),
        "department_metrics": _department_metrics(employees),
    }


def build_scenarios(summary: dict[str, object]) -> list[dict[str, object]]:
    """Create transparent, assumption-led planning scenarios, not forecasts."""
    current_headcount = int(summary["active_headcount"])
    expected_exits = max(1, round(current_headcount * float(summary["turnover_rate_pct"]) / 100))
    replacement_cost = int(summary["replacement_cost_per_exit_aed"])
    annual_payroll = int(summary["annual_payroll_aed"])
    average_salary = int(summary["average_annual_salary_aed"])
    correction_cost = int(summary["annual_salary_correction_aed"])

    targeted_exits = max(1, round(expected_exits * 0.85))
    avoided_exits = expected_exits - targeted_exits
    manager_program = 300_000
    baseline_growth = 36
    growth_first_hires = 72

    return [
        {
            "Scenario": "Baseline",
            "Expected_Exits": expected_exits,
            "Growth_Hires": baseline_growth,
            "Total_Hires_Required": expected_exits + baseline_growth,
            "Intervention_Cost_AED": 0,
            "Projected_People_Cost_AED": annual_payroll + expected_exits * replacement_cost + baseline_growth * average_salary // 2,
            "Avoided_Replacement_Cost_AED": 0,
            "Year_End_Headcount": current_headcount + baseline_growth,
            "Assumption": "Current turnover rate continues; 36 net-growth hires join evenly through the year.",
        },
        {
            "Scenario": "Targeted Retention",
            "Expected_Exits": targeted_exits,
            "Growth_Hires": baseline_growth,
            "Total_Hires_Required": targeted_exits + baseline_growth,
            "Intervention_Cost_AED": correction_cost + manager_program,
            "Projected_People_Cost_AED": annual_payroll + correction_cost + manager_program + targeted_exits * replacement_cost + baseline_growth * average_salary // 2,
            "Avoided_Replacement_Cost_AED": avoided_exits * replacement_cost,
            "Year_End_Headcount": current_headcount + baseline_growth,
            "Assumption": "Selected pay corrections plus manager support are modelled with a 15% reduction in exits; this is a testable assumption, not a causal forecast.",
        },
        {
            "Scenario": "Growth-First",
            "Expected_Exits": expected_exits,
            "Growth_Hires": growth_first_hires,
            "Total_Hires_Required": expected_exits + growth_first_hires,
            "Intervention_Cost_AED": 180_000,
            "Projected_People_Cost_AED": annual_payroll + 180_000 + expected_exits * replacement_cost + growth_first_hires * average_salary // 2,
            "Avoided_Replacement_Cost_AED": 0,
            "Year_End_Headcount": current_headcount + growth_first_hires,
            "Assumption": "72 net-growth hires join evenly through the year; turnover remains unchanged and recruiting capacity receives AED 180,000.",
        },
    ]


def validate_project_data(
    salary_bands: list[dict[str, object]],
    employees: list[dict[str, object]],
    monthly_workforce: list[dict[str, object]],
    requisitions: list[dict[str, object]],
) -> list[str]:
    """Return human-readable integrity errors; an empty list means valid."""
    errors = []
    employee_ids = [str(row["Employee_ID"]) for row in employees]
    if len(employee_ids) != len(set(employee_ids)):
        errors.append("Duplicate employee IDs detected.")

    band_lookup = {
        (str(row["Job_Family"]), str(row["Job_Level"])): row for row in salary_bands
    }
    if len(band_lookup) != len(salary_bands):
        errors.append("Duplicate salary-band keys detected.")
    for row in employees:
        key = (str(row["Job_Family"]), str(row["Job_Level"]))
        band = band_lookup.get(key)
        if not band:
            errors.append(f"Employee {row['Employee_ID']} has no salary band.")
            continue
        salary = int(row["Monthly_Salary_AED"])
        if not int(band["Band_Min_AED"]) <= salary <= int(band["Band_Max_AED"]):
            errors.append(f"Employee {row['Employee_ID']} is outside the assigned band.")
        if row["Employment_Status"] == "Active" and row["Exit_Date"]:
            errors.append(f"Active employee {row['Employee_ID']} has an exit date.")
        if row["Employment_Status"] == "Exited" and not row["Exit_Date"]:
            errors.append(f"Exited employee {row['Employee_ID']} lacks an exit date.")

    by_department: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in monthly_workforce:
        if int(row["Closing_Headcount"]) != int(row["Opening_Headcount"]) + int(row["Hires"]) - int(row["Exits"]):
            errors.append(f"Monthly balance failed for {row['Department']} in {row['Month']}.")
        by_department[str(row["Department"])].append(row)
    for department, rows in by_department.items():
        ordered = sorted(rows, key=lambda row: str(row["Month"]))
        for previous, current in zip(ordered, ordered[1:]):
            if int(previous["Closing_Headcount"]) != int(current["Opening_Headcount"]):
                errors.append(f"Monthly roll-forward failed for {department}.")

    if monthly_workforce:
        latest_month = max(str(row["Month"]) for row in monthly_workforce)
        latest_closing = sum(
            int(row["Closing_Headcount"])
            for row in monthly_workforce
            if str(row["Month"]) == latest_month
        )
        active_records = sum(row["Employment_Status"] == "Active" for row in employees)
        if latest_closing != active_records:
            errors.append("Latest monthly closing headcount does not match active employee records.")

    for row in requisitions:
        stages = [int(row[name]) for name in ("Applications", "Screened", "Interviewed", "Offers", "Hires")]
        if any(left < right for left, right in zip(stages, stages[1:])):
            errors.append(f"Recruitment funnel is invalid for {row['Requisition_ID']}.")
    return errors


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _bar_rows(metrics: list[dict[str, object]], key: str, suffix: str = "") -> str:
    maximum = max(float(row[key]) for row in metrics) or 1
    return "".join(
        f'<div class="bar-row"><span>{row["Department"]}</span><div class="track"><i style="width:{float(row[key]) * 100 / maximum:.1f}%"></i></div><strong>{float(row[key]):.1f}{suffix}</strong></div>'
        for row in metrics
    )


def render_dashboard(summary: dict[str, object], scenarios: list[dict[str, object]]) -> str:
    """Render a dependency-free dashboard with section and scenario controls."""
    metrics = list(summary["department_metrics"])
    reward_rows = "".join(
        f"<tr><td>{row['Department']}</td><td>{row['Active_Headcount']}</td><td>{float(row['Average_Compa_Ratio']):.3f}</td><td>{row['Below_090_Compa']}</td><td>{float(row['Raw_Gender_Pay_Gap_Pct']):.1f}%</td></tr>"
        for row in metrics
    )
    scenario_options = "".join(
        f'<option value="{index}">{row["Scenario"]}</option>' for index, row in enumerate(scenarios)
    )
    scenario_json = json.dumps(scenarios, ensure_ascii=False, separators=(",", ":"))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UAE Workforce Planning &amp; Total Rewards Command Centre</title>
<style>
:root{{--ink:#172033;--muted:#657087;--navy:#14324a;--teal:#008b87;--sand:#f5efe4;--line:#dbe2e8;--paper:#fff;--bg:#eef3f5;--amber:#b66a00}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,Arial,sans-serif}}button,select{{font:inherit}}
.shell{{max-width:1220px;margin:0 auto;padding:24px}}header{{background:linear-gradient(125deg,var(--navy),#1e5b69);color:white;border-radius:18px;padding:30px;box-shadow:0 15px 35px #14324a24}}
.eyebrow{{margin:0 0 5px;color:#9fe2d9;font-size:12px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}}h1{{margin:0;font-size:clamp(28px,4vw,43px);line-height:1.08}}header p{{max-width:760px;margin:12px 0 0;color:#d9e9ed}}
.notice{{margin:16px 0;padding:13px 16px;border-left:5px solid var(--amber);background:#fff8e8;border-radius:8px}}nav{{display:flex;gap:8px;overflow:auto;padding:4px 0 16px}}nav button{{border:1px solid var(--line);background:white;color:var(--navy);padding:9px 14px;border-radius:999px;cursor:pointer;white-space:nowrap}}nav button.active{{background:var(--navy);color:white}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:13px;margin-bottom:16px}}.card,.panel{{background:var(--paper);border:1px solid var(--line);border-radius:14px;box-shadow:0 4px 14px #19344c0b}}.card{{padding:18px}}.value{{font-size:29px;font-weight:800;color:var(--teal)}}.label{{color:var(--muted);font-size:13px}}.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.panel{{padding:21px;margin-bottom:16px}}h2{{margin:0 0 14px;color:var(--navy);font-size:20px}}h3{{color:var(--navy)}}
.bar-row{{display:grid;grid-template-columns:145px 1fr 55px;gap:9px;align-items:center;margin:11px 0}}.track{{height:11px;background:#e5ecef;border-radius:8px;overflow:hidden}}.track i{{display:block;height:100%;background:linear-gradient(90deg,var(--teal),#5dbab1);border-radius:8px}}table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border-bottom:1px solid var(--line);text-align:left}}th{{background:#eef5f5;color:var(--navy);font-size:12px;text-transform:uppercase;letter-spacing:.04em}}.table-wrap{{overflow:auto}}
.section{{display:none}}.section.active{{display:block}}.scenario-control{{display:flex;gap:12px;align-items:center;flex-wrap:wrap}}select{{min-width:220px;padding:10px;border:1px solid var(--line);border-radius:9px;background:white}}.scenario-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:16px}}.assumption{{background:var(--sand);padding:15px;border-radius:10px}}.small{{color:var(--muted);font-size:13px}}footer{{color:var(--muted);font-size:12px;padding:10px 2px 30px}}
@media(max-width:850px){{.kpis,.grid,.scenario-grid{{grid-template-columns:1fr 1fr}}}}@media(max-width:560px){{.shell{{padding:12px}}.kpis,.grid,.scenario-grid{{grid-template-columns:1fr}}.bar-row{{grid-template-columns:115px 1fr 48px}}}}
@media print{{nav{{display:none}}.section{{display:block!important}}body{{background:white}}.shell{{max-width:none}}}}
</style>
</head>
<body><main class="shell">
<header><p class="eyebrow">Executive people decision support</p><h1>UAE Workforce Planning & Total Rewards</h1><p>{COMPANY} · Portfolio case study · Data as of {summary['as_of_date']}</p></header>
<div class="notice"><strong>Entirely synthetic:</strong> no real employee, employer, salary-survey or HRIS data is used. Results demonstrate analytical method; scenario assumptions are not forecasts or employment recommendations.</div>
<nav aria-label="Dashboard sections"><button class="active" data-target="overview">Overview</button><button data-target="rewards">Total rewards</button><button data-target="recruitment">Recruitment</button><button data-target="scenarios">Scenarios</button><button data-target="governance">Governance</button></nav>

<section class="section active" data-section="overview">
<div class="kpis"><div class="card"><div class="value">{summary['active_headcount']}</div><div class="label">Active synthetic headcount</div></div><div class="card"><div class="value">{float(summary['turnover_rate_pct']):.1f}%</div><div class="label">Trailing 12-month turnover</div></div><div class="card"><div class="value">{_aed(float(summary['annual_payroll_aed']))}</div><div class="label">Annualized base payroll</div></div><div class="card"><div class="value">{summary['employees_below_090_compa']}</div><div class="label">Employees below 0.90 compa-ratio</div></div></div>
<div class="grid"><div class="panel"><h2>Active headcount by department</h2>{_bar_rows(metrics,'Active_Headcount')}</div><div class="panel"><h2>Average engagement by department</h2>{_bar_rows(metrics,'Average_Engagement')}</div></div>
<div class="panel"><h2>Management question</h2><p>Should leadership continue the baseline plan, invest selectively in retention and manager capability, or prioritise accelerated growth? Use the scenario section to compare people cost, exits, hiring demand and year-end headcount.</p></div>
</section>

<section class="section" data-section="rewards"><div class="kpis"><div class="card"><div class="value">{float(mean(float(row['Average_Compa_Ratio']) for row in metrics)):.3f}</div><div class="label">Average departmental compa-ratio</div></div><div class="card"><div class="value">{_aed(float(summary['annual_salary_correction_aed']))}</div><div class="label">Illustrative annual correction to 0.90</div></div><div class="card"><div class="value">{float(summary['raw_gender_pay_gap_pct']):.1f}%</div><div class="label">Raw, unadjusted gender pay gap</div></div><div class="card"><div class="value">24</div><div class="label">Hypothetical salary bands</div></div></div><div class="panel"><h2>Reward indicators by department</h2><div class="table-wrap"><table><thead><tr><th>Department</th><th>HC</th><th>Avg compa</th><th>Below 0.90</th><th>Raw pay gap</th></tr></thead><tbody>{reward_rows}</tbody></table></div><p class="small">The raw gap does not control for level, tenure, job family, performance or location and is not evidence of discrimination. It is a prompt for deeper, governed analysis.</p></div></section>

<section class="section" data-section="recruitment"><div class="kpis"><div class="card"><div class="value">{summary['closed_requisitions']}</div><div class="label">Closed requisitions</div></div><div class="card"><div class="value">{summary['total_hires']}</div><div class="label">Recorded hires</div></div><div class="card"><div class="value">{float(summary['offer_acceptance_rate_pct']):.1f}%</div><div class="label">Offer acceptance rate</div></div><div class="card"><div class="value">{float(summary['average_time_to_fill_days']):.1f}</div><div class="label">Average time-to-fill days</div></div></div><div class="grid"><div class="panel"><h2>Recruitment cost</h2><div class="value">{_aed(float(summary['recruitment_cost_aed']))}</div><p>Aggregate cost recorded for closed synthetic requisitions.</p></div><div class="panel"><h2>Replacement-cost assumption</h2><div class="value">{_aed(float(summary['replacement_cost_per_exit_aed']))}</div><p>Thirty percent of average annual salary per exit. Replace this assumption when a credible internal cost model is available.</p></div></div></section>

<section class="section" data-section="scenarios"><div class="panel"><h2>Workforce scenario comparison</h2><div class="scenario-control"><label for="scenario-select"><strong>Select scenario</strong></label><select id="scenario-select">{scenario_options}</select></div><div class="scenario-grid"><div class="card"><div class="value" id="scenario-exits"></div><div class="label">Expected exits</div></div><div class="card"><div class="value" id="scenario-hires"></div><div class="label">Total hires required</div></div><div class="card"><div class="value" id="scenario-cost"></div><div class="label">Projected people cost</div></div><div class="card"><div class="value" id="scenario-headcount"></div><div class="label">Year-end headcount</div></div></div><h3>Assumption</h3><p class="assumption" id="scenario-assumption"></p><p class="small">Scenario values support discussion. They are not a promise of savings, attrition reduction or future performance.</p></div></section>

<section class="section" data-section="governance"><div class="grid"><div class="panel"><h2>Data-quality controls</h2><ul><li>Unique synthetic employee and requisition IDs</li><li>Salary-band foreign-key and range checks</li><li>Monthly opening-to-closing headcount reconciliation</li><li>Recruitment-funnel monotonicity checks</li><li>Status and exit-date consistency checks</li></ul></div><div class="panel"><h2>Responsible-use boundaries</h2><ul><li>Aggregate protected characteristics only</li><li>Never use this data for individual employment decisions</li><li>Do not present hypothetical bands as UAE market benchmarks</li><li>Do not infer causation from descriptive patterns</li><li>Validate assumptions with Finance, Legal and business leaders</li></ul></div></div></section>
<footer>Generated reproducibly with Python standard library · Fixed seed {SEED} · See methodology, data dictionary and Power BI build guide.</footer>
</main>
<script>
const scenarios={scenario_json};
const money=new Intl.NumberFormat('en-AE',{{style:'currency',currency:'AED',maximumFractionDigits:0}});
function showScenario(index){{const s=scenarios[index];document.getElementById('scenario-exits').textContent=s.Expected_Exits;document.getElementById('scenario-hires').textContent=s.Total_Hires_Required;document.getElementById('scenario-cost').textContent=money.format(s.Projected_People_Cost_AED);document.getElementById('scenario-headcount').textContent=s.Year_End_Headcount;document.getElementById('scenario-assumption').textContent=s.Assumption;}}
document.getElementById('scenario-select').addEventListener('change',event=>showScenario(Number(event.target.value)));
document.querySelectorAll('nav button').forEach(button=>button.addEventListener('click',()=>{{document.querySelectorAll('nav button').forEach(item=>item.classList.remove('active'));document.querySelectorAll('.section').forEach(section=>section.classList.remove('active'));button.classList.add('active');document.querySelector(`[data-section="${{button.dataset.target}}"]`).classList.add('active');}}));
showScenario(0);
</script></body></html>"""


def _write_docs(project: Path, summary: dict[str, object], scenarios: list[dict[str, object]]) -> None:
    scenario_lookup = {str(row["Scenario"]): row for row in scenarios}
    targeted = scenario_lookup["Targeted Retention"]
    baseline = scenario_lookup["Baseline"]
    (project / "README.md").write_text(
        f"""# UAE Workforce Planning and Total Rewards Command Centre

An interview-ready, privacy-safe HR portfolio case for **{COMPANY}**. The company, employees, salaries, recruitment activity and scenarios are entirely fictional.

## Business question

How should leadership allocate its people budget to balance retention, fair pay, recruitment demand and planned growth?

## Deliverables

- `dashboard.html` — standalone interactive executive dashboard
- `index.html` — identical GitHub Pages entry point
- `employee_records.csv` — 650 synthetic employee records
- `salary_bands.csv` — 24 hypothetical salary bands
- `monthly_workforce.csv` — 24 months of departmental movements and payroll
- `recruitment_funnel.csv` — synthetic requisition funnel and cost data
- `workforce_scenarios.csv` — baseline, retention and growth scenarios
- `LINKEDIN_CASE_STUDY.md` — source for the LinkedIn document PDF
- `LINKEDIN_POST.md` and `CV_PROJECT_ENTRY.md` — publication-ready copy
- `Mohammad_Azimuddin_UAE_HR_Analytics_Case_Study.pdf` — four-page LinkedIn document
- `LinkedIn_Case_Study_Cover.png` — optional cover preview derived from page one
- supporting requirements, methodology, executive memo, Power BI guide, interview guide and release checklist

## Reproduce

```bash
python3 98_Maintenance/generate_uae_workforce_project.py
python3 -m unittest 98_Maintenance/tests/test_generate_uae_workforce_project.py
```

Open `dashboard.html` directly in a browser. Import the CSV files into Excel or Power BI to recreate the model.

For public release, complete every gate in `PUBLICATION_CHECKLIST.md`, generate the
case-study PDF, and follow `GITHUB_PUBLISHING_GUIDE.md`.

## Ethical boundary

Never describe this as employer data, UAE salary-survey evidence, production Oracle HCM experience, predictive modelling or a guaranteed business result.
""",
        encoding="utf-8",
    )
    (project / "REQUIREMENTS.md").write_text(
        """# Project Requirements

## User journeys

1. As an HR analyst, I can reconcile workforce movement and report defensible people metrics.
2. As a rewards analyst, I can compare salaries with hypothetical bands and identify review populations.
3. As a talent-acquisition partner, I can diagnose funnel conversion, time-to-fill and recruitment cost.
4. As an HRBP, I can compare transparent workforce scenarios and communicate a recommendation.
5. As an interviewer, I can trace every dashboard number to a documented formula and source field.

## Functional requirements

- Deterministic synthetic data; no real names, contact details or employer records.
- CSV outputs compatible with Excel, Power Query and Power BI.
- Automated ID, relationship, balance, range, status and funnel tests.
- Dashboard sections for workforce, rewards, recruitment, scenarios and governance.
- Scenario assumptions displayed beside results.
- Clear separation between descriptive findings, assumptions and recommendations.

## Software

- Required: Python 3.9+ and a modern browser.
- Recommended: Excel or another spreadsheet tool.
- Optional: Power BI Desktop on Windows, or Windows through a VM/remote machine when working from macOS.
- No paid API, HRIS account, salary survey or personal employee data is required.

## Acceptance criteria

- All automated tests pass.
- Generation is byte-for-byte reproducible.
- Dashboard works without an internet connection.
- Candidate can reproduce the core metrics and explain limitations without reading a script.
""",
        encoding="utf-8",
    )
    (project / "DATA_DICTIONARY.md").write_text(
        """# Data Dictionary

## employee_records.csv

| Field | Meaning |
|---|---|
| Employee_ID | Synthetic unique key beginning `UAE-SYN-` |
| Department / Job_Family / Job_Level | Fictional organization and job architecture |
| Location | Dubai, Abu Dhabi or Sharjah |
| Gender / Workforce_Category | Synthetic attributes used only for aggregate learning |
| Hire_Date / Exit_Date / Employment_Status | Synthetic employment timeline |
| Monthly_Salary_AED | Fictional monthly base salary in AED |
| Band_Mid_AED / Compa_Ratio | Hypothetical midpoint and salary divided by midpoint |
| Performance_Rating | Generated 1–5 rating |
| Engagement_Score | Generated 0–100 score |
| Training_Hours_YTD / Absence_Days_YTD | Generated YTD activity |
| Critical_Role / Regrettable_Exit | Synthetic planning flags; not an individual decision model |

## salary_bands.csv

One hypothetical minimum, midpoint and maximum for each Job_Family × Job_Level combination. These are not UAE market benchmarks.

## monthly_workforce.csv

One row per Month × Department with opening headcount, hires, exits, closing headcount, payroll cost and payroll budget. `Closing = Opening + Hires − Exits`.

## recruitment_funnel.csv

One row per requisition with dates, status, funnel stages, time-to-fill and fictional recruitment cost.

## workforce_scenarios.csv

Three assumption-led planning cases with exits, hiring, intervention cost, projected people cost, avoided replacement cost and year-end headcount.
""",
        encoding="utf-8",
    )
    (project / "METHODOLOGY_AND_LIMITATIONS.md").write_text(
        f"""# Methodology and Limitations

## Method

1. Generate deterministic fictional records using fixed seed `{SEED}`.
2. Validate unique keys, salary-band relationships, employee status, monthly headcount roll-forward and recruitment-funnel order.
3. Calculate trailing-12-month turnover using average monthly closing headcount.
4. Calculate compa-ratio as monthly salary divided by the hypothetical band midpoint.
5. Calculate the raw gender pay gap from group-average monthly salary.
6. Compare three explicitly documented workforce scenarios.

## Important limitations

- The figures are designed for learning and are not representative of any employer or the UAE labour market.
- The raw pay gap is unadjusted. It does not control for job level, family, tenure, location, performance or other legitimate variables and cannot establish discrimination.
- Descriptive relationships do not establish causes of attrition, performance or engagement.
- The targeted-retention scenario assumes a 15% exit reduction for comparison. No historical experiment supports that assumption.
- Replacement cost is modelled as 30% of average annual salary. A real analysis would use Finance-approved internal cost components.
- The model excludes allowances, bonus, benefits, visa costs, end-of-service benefits, tax, currency changes and accounting timing.
- Protected attributes must never be used to automate individual employment decisions.
""",
        encoding="utf-8",
    )
    (project / "EXECUTIVE_DECISION_MEMO.md").write_text(
        f"""# Executive Decision Memo

**To:** Fictional Executive Committee  
**From:** People Analytics Portfolio Analyst  
**Subject:** 2027 workforce plan — retention versus accelerated growth  
**Data date:** {summary['as_of_date']}

## Decision requested

Approve a controlled review of the **Targeted Retention** scenario before committing to accelerated growth hiring.

## Evidence from the synthetic case

- Active headcount: **{summary['active_headcount']}**.
- Trailing-12-month turnover: **{float(summary['turnover_rate_pct']):.1f}%**, using average closing headcount.
- Employees below 0.90 compa-ratio: **{summary['employees_below_090_compa']}**.
- Illustrative annual cost to lift that population to 0.90: **{_aed(float(summary['annual_salary_correction_aed']))}**.
- Baseline hiring requirement: **{baseline['Total_Hires_Required']}**; targeted-retention requirement: **{targeted['Total_Hires_Required']}**.
- Modelled avoided replacement cost under targeted retention: **{_aed(float(targeted['Avoided_Replacement_Cost_AED']))}**.

## Recommendation

Run a 90-day validation phase: review low compa-ratio cases by job architecture, diagnose exit reasons, confirm replacement-cost inputs with Finance, and define manager-support measures. Proceed only if governed analysis supports the assumed retention opportunity.

## Risks and controls

- Do not apply a uniform pay increase without checking role, level, performance and internal equity.
- Do not treat the raw pay gap as proof of inequity or discrimination.
- Monitor regrettable exits, offer acceptance, time-to-fill and employee listening indicators.
- Recalculate the business case with actual, authorized organizational data.

This memo demonstrates a decision process. The scenario is **not a forecast**, guarantee or recommendation for a real employer.
""",
        encoding="utf-8",
    )
    (project / "POWER_BI_BUILD_GUIDE.md").write_text(
        """# Power BI Build Guide

## Model

1. Import all five CSV files with **Get Data → Text/CSV**.
2. Set dates, whole numbers, decimal numbers and currency types explicitly.
3. In both employee records and salary bands, create `Job_Band_Key = Job_Family & "|" & Job_Level`; relate the tables on that key.
4. Keep monthly workforce, recruitment funnel and scenarios as separate fact tables.
5. Create a calendar table covering August 2024 through July 2026.

## Core measures

```text
Active Headcount =
CALCULATE(DISTINCTCOUNT(Employees[Employee_ID]), Employees[Employment_Status] = "Active")

Leavers =
CALCULATE(DISTINCTCOUNT(Employees[Employee_ID]), Employees[Employment_Status] = "Exited")

Turnover Rate =
DIVIDE([Trailing 12M Leavers], [Average Monthly Headcount])

Average Compa Ratio =
AVERAGE(Employees[Compa_Ratio])

Offer Acceptance Rate =
DIVIDE(SUM(Recruitment[Hires]), SUM(Recruitment[Offers]))

Average Time to Fill =
CALCULATE(AVERAGE(Recruitment[Time_to_Fill_Days]), Recruitment[Status] = "Closed")

Payroll Variance =
SUM(MonthlyWorkforce[Payroll_Cost_AED]) - SUM(MonthlyWorkforce[Payroll_Budget_AED])
```

## Pages

1. Executive overview
2. Workforce movement and turnover
3. Total rewards and aggregate equity indicators
4. Recruitment funnel and cost
5. Scenario comparison and assumptions
6. Data quality and governance

Reconcile each measure against the CSVs before changing the design.
""",
        encoding="utf-8",
    )
    (project / "INTERVIEW_GUIDE.md").write_text(
        """# Interview Guide

## 60-second introduction

“I built a synthetic UAE workforce-planning case to practise connecting HR data with management decisions. I created and validated employee, salary-band, workforce-movement and recruitment tables; calculated turnover, compa-ratio and hiring metrics; and compared three transparent budget scenarios. The data is fictional, and I clearly separate descriptive findings from assumptions.”

## Questions you must be able to answer

1. Why is average headcount a better turnover denominator than ending headcount alone?
2. What does a compa-ratio below 0.90 mean, and what does it not prove?
3. Why is the displayed gender pay gap described as raw and unadjusted?
4. How do you reconcile monthly opening and closing headcount?
5. What costs are missing from the replacement-cost model?
6. Why is the 15% retention improvement an assumption rather than a prediction?
7. What HRIS modules or files could supply each table in a real organization?
8. What privacy and access controls would real employee data require?

## Demonstration checklist

- Recalculate one KPI in Excel without referring to the dashboard.
- Explain one data-quality test.
- Compare two scenarios in business language.
- State at least three limitations before the interviewer asks.
- Never claim production Power BI, Oracle HCM implementation or predictive-analytics experience from this project alone.
""",
        encoding="utf-8",
    )


def _write_publication_docs(
    project: Path,
    summary: dict[str, object],
    scenarios: list[dict[str, object]],
) -> None:
    """Write source-first LinkedIn, CV, case-study, and publishing materials."""
    scenario_lookup = {str(row["Scenario"]): row for row in scenarios}
    baseline = scenario_lookup["Baseline"]
    targeted = scenario_lookup["Targeted Retention"]
    growth = scenario_lookup["Growth-First"]
    targeted_premium = int(targeted["Projected_People_Cost_AED"]) - int(
        baseline["Projected_People_Cost_AED"]
    )

    (project / "LINKEDIN_POST.md").write_text(
        f"""# LinkedIn Post

**Publish only after completing `PUBLICATION_CHECKLIST.md`. Replace the link placeholder before posting.**

I built an independent HR analytics portfolio case around a practical management decision:

**Should a fictional UAE company continue its baseline workforce plan, invest selectively in retention, or prioritise faster growth?**

The project uses:

- 650 synthetic employee records
- 24 hypothetical salary bands
- 24 months of workforce movement and payroll data
- 48 synthetic recruitment requisitions
- three transparent workforce scenarios

The descriptive model reports an 11.0% trailing-12-month turnover rate, 81 active employees below a 0.90 compa-ratio, a 43.3% offer-acceptance rate, and an average time-to-fill of 56.8 days.

I then translated those measures into an executive dashboard and decision memo. The Targeted Retention scenario lowers modelled exits from {baseline['Expected_Exits']} to {targeted['Expected_Exits']}, but it costs {_aed(targeted_premium)} more than the baseline. That is why the recommendation is a controlled 90-day validation phase, not an immediate company-wide intervention.

The project is entirely synthetic. It does not use employer records or salary-survey data, and its assumptions are not forecasts. I built it to practise workforce planning, total-rewards analysis, recruitment metrics, data-quality controls, scenario modelling, and executive communication.

Case-study PDF and interactive dashboard: **[add public portfolio URL]**

#PeopleAnalytics #HRAnalytics #WorkforcePlanning #TotalRewards

## Suggested document title

UAE Workforce Planning & Total Rewards: An Independent Synthetic HR Analytics Case

## Alt text for the dashboard image

Executive HR analytics dashboard for a fictional UAE company showing synthetic headcount, turnover, payroll, rewards, recruitment, and workforce-scenario metrics. No real employee or employer data is used.
""",
        encoding="utf-8",
    )

    (project / "CV_PROJECT_ENTRY.md").write_text(
        f"""# CV and LinkedIn Project Entry

**Status:** Ready for insertion only after every ownership gate in `PUBLICATION_CHECKLIST.md` is checked.

## CV version — recommended

**UAE Workforce Planning & Total Rewards Command Centre** | Independent Portfolio Project | August 2026

- Created a privacy-safe HR decision case using 650 synthetic employee records, 24 hypothetical salary bands, 24 months of workforce movements, and 48 recruitment requisitions; reconciled {summary['active_headcount']} active records across the employee and monthly-workforce tables.
- Analysed synthetic turnover ({float(summary['turnover_rate_pct']):.1f}%), compa-ratio review population ({summary['employees_below_090_compa']} below 0.90), recruitment conversion, time-to-fill, payroll, and three assumption-led workforce scenarios.
- Produced a Power BI-ready data model, standalone executive dashboard, data dictionary, decision memo, and automated integrity tests while documenting non-causality, pay-equity, privacy, and forecasting limitations.

**Disclosure:** Entirely synthetic independent learning project; not employer work or UAE salary-benchmark evidence.

## One-line CV version — when space is limited

**Independent HR Analytics Project:** Built a Power BI-ready synthetic workforce-planning and total-rewards case covering {summary['active_headcount']} active records, {float(summary['turnover_rate_pct']):.1f}% modelled turnover, recruitment metrics, compensation indicators, scenario analysis, and data-quality controls.

## LinkedIn Projects section

**Project name:** UAE Workforce Planning & Total Rewards Command Centre  
**Date:** August 2026  
**Associated with:** Independent project  
**Project URL:** [add public portfolio URL]  
**Description:** Developed a privacy-safe, reproducible HR analytics case using synthetic employee, salary-band, workforce-movement, payroll, and recruitment data. Compared baseline, targeted-retention, and growth-first scenarios through an interactive dashboard and executive decision memo. All figures are fictional and assumptions are explicitly documented.

## Safe skills to associate after reproduction

HR Analytics · Workforce Planning · HR Metrics · Total Rewards Concepts · Data Quality · Microsoft Excel · Data Storytelling
""",
        encoding="utf-8",
    )

    (project / "LINKEDIN_CASE_STUDY.md").write_text(
        f"""# UAE Workforce Planning and Total Rewards

**An independent synthetic HR analytics case study**  
**Author:** Mohammad Azimuddin  
**Date:** August 2026

> This case uses entirely fictional company, employee, salary, recruitment, and scenario data. It demonstrates an analytical process, not employer results or UAE market benchmarks.

## Business question

How should a fictional UAE services company allocate its people budget to balance retention, fair-pay review, recruitment demand, and planned growth?

The analysis compares three choices:

1. Continue the current baseline.
2. Invest selectively in pay corrections and manager support.
3. Accelerate growth hiring while accepting unchanged turnover.

## Dataset and controls

| Component | Synthetic scope |
|---|---:|
| Employee records | 650 |
| Active employee records | {summary['active_headcount']} |
| Hypothetical salary bands | 24 |
| Workforce history | 24 months × 6 departments |
| Recruitment requisitions | 48 |
| Workforce scenarios | 3 |

The data package includes unique-ID checks, salary-band relationship checks, monthly opening-to-closing headcount reconciliation, recruitment-funnel checks, and status/exit-date validation. The July closing headcount reconciles to {summary['active_headcount']} active employee records.

## Descriptive findings

### Workforce

- Trailing-12-month exits: **{summary['trailing_12_exits']}**.
- Average monthly closing headcount: **{float(summary['average_headcount_12m']):.1f}**.
- Turnover: **{float(summary['turnover_rate_pct']):.1f}%**.
- Annualised synthetic base payroll: **{_aed(float(summary['annual_payroll_aed']))}**.

### Total rewards

- Active records below a 0.90 compa-ratio: **{summary['employees_below_090_compa']}**.
- Illustrative annual correction to 0.90: **{_aed(float(summary['annual_salary_correction_aed']))}**.
- The displayed gender pay gap is raw and unadjusted. It cannot establish unfair treatment or discrimination.

### Recruitment

- Closed requisitions: **{summary['closed_requisitions']}**.
- Offer-acceptance rate: **{float(summary['offer_acceptance_rate_pct']):.1f}%**.
- Average time-to-fill: **{float(summary['average_time_to_fill_days']):.1f} days**.

These findings are descriptive. They identify questions for investigation; they do not establish why employees leave or how a real workforce would respond.

## Scenario comparison

| Scenario | Expected exits | Total hires required | Projected people cost | Year-end headcount |
|---|---:|---:|---:|---:|
| Baseline | {baseline['Expected_Exits']} | {baseline['Total_Hires_Required']} | {_aed(float(baseline['Projected_People_Cost_AED']))} | {baseline['Year_End_Headcount']} |
| Targeted Retention | {targeted['Expected_Exits']} | {targeted['Total_Hires_Required']} | {_aed(float(targeted['Projected_People_Cost_AED']))} | {targeted['Year_End_Headcount']} |
| Growth-First | {growth['Expected_Exits']} | {growth['Total_Hires_Required']} | {_aed(float(growth['Projected_People_Cost_AED']))} | {growth['Year_End_Headcount']} |

The Targeted Retention scenario assumes a 15% reduction in exits. It reduces required hires by {int(baseline['Total_Hires_Required']) - int(targeted['Total_Hires_Required'])}, but its projected people cost is {_aed(targeted_premium)} above baseline because the intervention costs more than the modelled avoided replacement cost.

## Recommendation

Do not approve a broad intervention from this dashboard alone. Run a controlled 90-day validation phase:

1. Review low compa-ratio cases within consistent job families and levels.
2. Validate exit reasons and regrettable-exit definitions.
3. Replace the 30% replacement-cost assumption with Finance-approved inputs.
4. Define a limited manager-support pilot and success measures.
5. Recalculate the scenario before any wider decision.

## Limitations

- All records and results are synthetic.
- Salary bands are hypothetical and are not UAE labour-market benchmarks.
- The raw pay gap does not control for level, tenure, job family, performance, or location.
- The model excludes allowances, incentives, benefits, visa costs, end-of-service benefits, and accounting timing.
- The 15% retention effect and 30% replacement-cost factor are assumptions, not forecasts.
- Protected characteristics must never drive individual employment decisions.

## What this project demonstrates

Workforce-movement reconciliation · HR metric definition · compa-ratio interpretation · recruitment-funnel analysis · assumption-led scenario modelling · data-quality controls · ethical limitation writing · executive data storytelling

**Interactive dashboard:** the public link belongs in the LinkedIn post and CV entry after hosting.
""",
        encoding="utf-8",
    )

    (project / "PUBLICATION_CHECKLIST.md").write_text(
        f"""# Publication and Ownership Checklist

## Status

**Do not publish or add this project to an active CV until every required box below is checked by Mohammad Azimuddin.**

## Calculation ownership

- [ ] I can filter the employee table and reproduce **{summary['active_headcount']} active records**.
- [ ] I can identify **{summary['trailing_12_exits']} trailing-12-month exits**.
- [ ] I can reproduce **{float(summary['average_headcount_12m']):.1f} average monthly headcount** from the monthly workforce table.
- [ ] I can calculate **{summary['trailing_12_exits']} ÷ {float(summary['average_headcount_12m']):.1f} = {float(summary['turnover_rate_pct']):.1f}% turnover** and explain the denominator.
- [ ] I can explain compa-ratio and why a value below 0.90 is a review flag, not proof of underpayment.
- [ ] I can explain why the raw pay gap is not an adjusted pay-equity study.
- [ ] I can reconcile July monthly closing headcount to the active employee table.

## Scenario ownership

- [ ] I can explain the Baseline, Targeted Retention, and Growth-First assumptions.
- [ ] I can explain why the Targeted Retention scenario costs more than Baseline despite fewer exits.
- [ ] I can state clearly that the 15% exit reduction and 30% replacement-cost factor are assumptions.
- [ ] I can explain why the recommendation is a 90-day validation phase rather than an immediate intervention.

## Public-release checks

- [ ] I replaced every `[add public portfolio URL]` placeholder after hosting.
- [ ] The public portfolio URL opens successfully in a signed-out browser.
- [ ] The case-study PDF contains no placeholder, broken link, or real employee information.
- [ ] I uploaded the PDF to LinkedIn as a document and used the prepared post copy.
- [ ] I added the project to the LinkedIn Projects section with the synthetic-data disclosure.
- [ ] I added the recommended project entry only to the relevant HR Analyst or C&B CV.

## Claims I will not make

- Real-employer business impact or savings
- UAE market-pricing or salary-survey expertise
- Advanced Power BI proficiency before independently recreating the model
- Live HRIS configuration or implementation experience
- Causal or future-outcome claims from the synthetic scenarios

When every required box is complete, change the status at the top to `PUBLICATION CLEARED — owner verified` and record the date.
""",
        encoding="utf-8",
    )

    (project / "GITHUB_PUBLISHING_GUIDE.md").write_text(
        """# GitHub Pages Publishing Guide

The project folder is structured as a standalone static portfolio repository. `index.html` is the GitHub Pages entry point and works without a server or external JavaScript library.

## Before uploading

1. Complete `PUBLICATION_CHECKLIST.md`.
2. Confirm `Mohammad_Azimuddin_UAE_HR_Analytics_Case_Study.pdf` opens and has four pages.
3. Confirm every file is synthetic and contains no private employer data.
4. Keep the disclosure near the top of `README.md` and the dashboard.

## Suggested repository

Repository name: `uae-workforce-analytics-portfolio`

Upload this project folder as the repository root. Do not upload unrelated CV, employment, contact-list, or source-evidence folders from the larger workspace.

## Enable GitHub Pages

1. Open the repository’s **Settings**.
2. Select **Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Choose the `main` branch and `/ (root)` folder.
5. Save and wait for the public URL.
6. Open the URL in a signed-out browser and test all dashboard sections and scenarios.

## Finish the publication package

Replace `[add public portfolio URL]` in `LINKEDIN_POST.md` and `CV_PROJECT_ENTRY.md`. The PDF is intentionally link-free so the same document can remain valid if the hosting URL changes.

Never upload the entire career workspace. Only this self-contained synthetic project folder is intended for public hosting.
""",
        encoding="utf-8",
    )


def main(project: Path = PROJECT) -> dict[str, int]:
    """Generate and validate every portfolio deliverable."""
    project.mkdir(parents=True, exist_ok=True)
    bands = create_salary_bands()
    employees = create_employee_records(bands)
    monthly = create_monthly_workforce()
    requisitions = create_requisitions()
    errors = validate_project_data(bands, employees, monthly, requisitions)
    if errors:
        raise ValueError("Project validation failed:\n- " + "\n- ".join(errors))

    summary = calculate_summary(employees, monthly, requisitions, bands)
    scenarios = build_scenarios(summary)
    _write_csv(project / "employee_records.csv", employees)
    _write_csv(project / "salary_bands.csv", bands)
    _write_csv(project / "monthly_workforce.csv", monthly)
    _write_csv(project / "recruitment_funnel.csv", requisitions)
    _write_csv(project / "workforce_scenarios.csv", scenarios)
    dashboard_html = render_dashboard(summary, scenarios)
    (project / "dashboard.html").write_text(dashboard_html, encoding="utf-8")
    (project / "index.html").write_text(dashboard_html, encoding="utf-8")
    _write_docs(project, summary, scenarios)
    _write_publication_docs(project, summary, scenarios)
    result = {
        "employee_records": len(employees),
        "salary_bands": len(bands),
        "monthly_workforce_rows": len(monthly),
        "requisitions": len(requisitions),
        "scenarios": len(scenarios),
    }
    print(
        "Generated UAE workforce portfolio: "
        + ", ".join(f"{name}={count}" for name, count in result.items())
    )
    return result


if __name__ == "__main__":
    main()
