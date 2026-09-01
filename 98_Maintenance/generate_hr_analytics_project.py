#!/usr/bin/env python3
"""Create a reproducible, privacy-safe HR analytics portfolio project."""

from __future__ import annotations

import csv
import random
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "06_Portfolio_Projects/01_Synthetic_HR_Analytics_Dashboard"
RNG = random.Random(20260727)

DEPARTMENTS = ["Sales", "Operations", "Customer Support", "Finance", "Human Resources", "Technology"]
DEPARTMENT_WEIGHTS = [23, 25, 18, 11, 9, 14]
LOCATIONS = ["Aligarh", "Delhi NCR", "Bengaluru", "Mumbai", "Hyderabad"]
LOCATION_WEIGHTS = [16, 27, 22, 18, 17]
LEVELS = ["Entry", "Associate", "Specialist", "Manager"]
LEVEL_WEIGHTS = [34, 35, 23, 8]
BASE_SALARY = {"Entry": 30000, "Associate": 47000, "Specialist": 68000, "Manager": 98000}
DEPARTMENT_FACTOR = {
    "Sales": 1.02,
    "Operations": 0.98,
    "Customer Support": 0.91,
    "Finance": 1.08,
    "Human Resources": 1.00,
    "Technology": 1.19,
}


def pick(values: list[str], weights: list[int]) -> str:
    return RNG.choices(values, weights=weights, k=1)[0]


def create_rows() -> list[dict[str, object]]:
    rows = []
    for index in range(1, 121):
        department = pick(DEPARTMENTS, DEPARTMENT_WEIGHTS)
        location = pick(LOCATIONS, LOCATION_WEIGHTS)
        level = pick(LEVELS, LEVEL_WEIGHTS)
        tenure = round(min(12.0, max(0.2, RNG.gammavariate(1.8, 1.7))), 1)
        performance = min(5, max(1, round(RNG.gauss(3.4, 0.75))))
        engagement = min(96, max(38, round(RNG.gauss(72, 11) + (performance - 3) * 2)))
        training = max(0, round(RNG.gauss(24, 12)))
        absence = max(0, round(RNG.gauss(7, 4) + (70 - engagement) / 11))
        salary_noise = RNG.uniform(0.88, 1.14)
        salary = round(BASE_SALARY[level] * DEPARTMENT_FACTOR[department] * salary_noise / 500) * 500

        attrition_probability = 0.07
        if tenure < 1.5:
            attrition_probability += 0.10
        if engagement < 65:
            attrition_probability += 0.14
        if absence > 11:
            attrition_probability += 0.06
        if department in {"Sales", "Customer Support"}:
            attrition_probability += 0.04
        attrition = "Yes" if RNG.random() < min(attrition_probability, 0.48) else "No"

        rows.append(
            {
                "Employee_ID": f"SYN-{index:03d}",
                "Department": department,
                "Location": location,
                "Job_Level": level,
                "Tenure_Years": tenure,
                "Performance_Rating": performance,
                "Engagement_Score": engagement,
                "Training_Hours_YTD": training,
                "Absence_Days_YTD": absence,
                "Monthly_Salary_INR": salary,
                "Attrition": attrition,
            }
        )
    return rows


def percent(part: int, total: int) -> float:
    return round(part * 100 / total, 1) if total else 0.0


def bar(label: str, value: float, maximum: float, suffix: str = "") -> str:
    width = 0 if maximum == 0 else value * 100 / maximum
    return (
        f'<div class="bar-row"><span>{label}</span><div class="track">'
        f'<div class="bar" style="width:{width:.1f}%"></div></div><strong>{value:.1f}{suffix}</strong></div>'
    )


def create_dashboard(rows: list[dict[str, object]]) -> str:
    total = len(rows)
    attrition_count = sum(row["Attrition"] == "Yes" for row in rows)
    avg_engagement = sum(int(row["Engagement_Score"]) for row in rows) / total
    avg_performance = sum(int(row["Performance_Rating"]) for row in rows) / total
    avg_training = sum(int(row["Training_Hours_YTD"]) for row in rows) / total

    department_rows: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        department_rows[str(row["Department"])].append(row)

    department_stats = []
    for department in DEPARTMENTS:
        subset = department_rows[department]
        leavers = sum(row["Attrition"] == "Yes" for row in subset)
        engagement = sum(int(row["Engagement_Score"]) for row in subset) / len(subset)
        department_stats.append((department, len(subset), percent(leavers, len(subset)), engagement))

    max_headcount = max(item[1] for item in department_stats)
    max_attrition = max(item[2] for item in department_stats)
    headcount_bars = "".join(bar(name, count, max_headcount) for name, count, _, _ in department_stats)
    attrition_bars = "".join(bar(name, rate, max_attrition, "%") for name, _, rate, _ in department_stats)

    table_rows = "".join(
        f"<tr><td>{name}</td><td>{count}</td><td>{rate:.1f}%</td><td>{engagement:.1f}</td></tr>"
        for name, count, rate, engagement in department_stats
    )

    tenure_bands = {"Under 1.5 years": [], "1.5–3 years": [], "Over 3 years": []}
    for row in rows:
        tenure = float(row["Tenure_Years"])
        if tenure < 1.5:
            tenure_bands["Under 1.5 years"].append(row)
        elif tenure <= 3:
            tenure_bands["1.5–3 years"].append(row)
        else:
            tenure_bands["Over 3 years"].append(row)
    tenure_rows = "".join(
        f"<tr><td>{name}</td><td>{len(subset)}</td><td>{percent(sum(row['Attrition'] == 'Yes' for row in subset), len(subset)):.1f}%</td></tr>"
        for name, subset in tenure_bands.items()
    )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Synthetic HR Workforce Dashboard</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: #f2f5f8; color: #172438; font: 15px/1.45 Arial, sans-serif; }}
  .dashboard {{ max-width: 1180px; margin: 28px auto; padding: 0 20px 34px; }}
  .dash-header {{ padding: 24px 28px; border-radius: 12px; background: #173a56; color: white; }}
  h1 {{ margin: 0; font-size: 30px; }}
  .dash-header p {{ margin: 7px 0 0; color: #d7e5ef; }}
  h2 {{ margin: 0 0 13px; color: #173a56; font-size: 20px; }}
  .warning {{ margin: 18px 0; padding: 13px 16px; border-left: 5px solid #b66a00; background: #fff5e6; }}
  .kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 18px 0; }}
  .card, .panel {{ border: 1px solid #d8e0e7; border-radius: 10px; background: white; box-shadow: 0 2px 7px #173a5612; }}
  .card {{ padding: 18px; }}
  .card .value {{ color: #195b84; font-size: 29px; font-weight: 700; }}
  .card .label {{ color: #607080; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .panel {{ margin-bottom: 16px; padding: 20px; }}
  .bar-row {{ display: grid; grid-template-columns: 128px 1fr 54px; align-items: center; gap: 10px; margin: 9px 0; }}
  .track {{ height: 12px; overflow: hidden; border-radius: 8px; background: #e5ebf0; }}
  .bar {{ height: 100%; border-radius: 8px; background: #2c779f; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ padding: 9px; border-bottom: 1px solid #dde4ea; text-align: left; }}
  th {{ color: #173a56; background: #edf3f7; }}
  ul {{ margin: 7px 0 0 19px; padding: 0; }}
  li {{ margin: 5px 0; }}
  .small {{ color: #657585; font-size: 13px; }}
  @media (max-width: 800px) {{ .kpis, .grid {{ grid-template-columns: 1fr; }} }}
  @media print {{ body {{ background: white; }} .dashboard {{ margin: 0; max-width: none; }} .card, .panel {{ box-shadow: none; }} }}
</style>
</head>
<body>
<div class="dashboard">
<div class="dash-header">
  <h1>Synthetic HR Workforce Dashboard</h1>
  <p>Descriptive portfolio project · 120 fictional employee records · Generated 27 July 2026</p>
</div>
<div class="warning"><strong>Privacy and interpretation:</strong> this dataset is entirely synthetic. It contains no real employees and supports descriptive practice only. The generated relationships are not causal and must not be used for employment decisions.</div>
<div class="kpis">
  <div class="card"><div class="value">{total}</div><div class="label">Synthetic headcount</div></div>
  <div class="card"><div class="value">{percent(attrition_count, total):.1f}%</div><div class="label">Generated attrition rate</div></div>
  <div class="card"><div class="value">{avg_engagement:.1f}</div><div class="label">Average engagement / 100</div></div>
  <div class="card"><div class="value">{avg_training:.1f}</div><div class="label">Average training hours YTD</div></div>
</div>
<div class="grid">
  <div class="panel"><h2>Headcount by department</h2>{headcount_bars}</div>
  <div class="panel"><h2>Generated attrition rate by department</h2>{attrition_bars}</div>
</div>
<div class="panel">
  <h2>Department summary</h2>
  <table><thead><tr><th>Department</th><th>Headcount</th><th>Attrition</th><th>Avg engagement</th></tr></thead><tbody>{table_rows}</tbody></table>
</div>
<div class="grid">
  <div class="panel">
    <h2>Tenure comparison</h2>
    <table><thead><tr><th>Tenure band</th><th>Headcount</th><th>Attrition</th></tr></thead><tbody>{tenure_rows}</tbody></table>
  </div>
  <div class="panel">
    <h2>Interpretation checklist</h2>
    <ul>
      <li>Start with data quality and field definitions.</li>
      <li>Compare rates as well as counts.</li>
      <li>Do not infer causation from descriptive patterns.</li>
      <li>Do not use protected characteristics for individual decisions.</li>
      <li>Validate findings with qualitative and operational context.</li>
    </ul>
  </div>
</div>
<div class="panel">
  <h2>Project scope</h2>
  <p>This work sample demonstrates a reproducible descriptive workflow: synthetic data creation, CSV preparation, KPI definition, department and tenure aggregation, visual reporting, and limitations documentation.</p>
  <p class="small">Average performance in the synthetic dataset: {avg_performance:.2f}/5. See the accompanying data dictionary, analysis notes, and source CSV.</p>
</div>
</div>
</body>
</html>"""


def write_docs(rows: list[dict[str, object]]) -> None:
    total = len(rows)
    attrition_count = sum(row["Attrition"] == "Yes" for row in rows)
    department_counts = Counter(str(row["Department"]) for row in rows)
    department_leavers = Counter(str(row["Department"]) for row in rows if row["Attrition"] == "Yes")
    highest_department = max(
        DEPARTMENTS,
        key=lambda name: department_leavers[name] / department_counts[name],
    )

    (PROJECT / "README.md").write_text(
        """# Synthetic HR Analytics Dashboard

This is a privacy-safe portfolio project built from 120 fictional employee records. It demonstrates descriptive HR reporting without claiming real employer experience.

## Files

- `synthetic_hr_data.csv` — Excel/Power BI-compatible source data
- `dashboard.html` — standalone dashboard with no external dependency
- `DATA_DICTIONARY.md` — field definitions
- `ANALYSIS_NOTES.md` — methodology, findings, limitations, and interview prompts

## How to use

1. Open `dashboard.html` in a browser.
2. Review the calculations against the CSV.
3. Import the CSV into Excel or Power BI and recreate the measures and charts.
4. Do not place this project on a CV until you can independently explain and reproduce it.

## Ethical boundary

The dataset is synthetic. Never describe it as employer data, a production HRIS export, or evidence of predictive modelling.
""",
        encoding="utf-8",
    )
    (PROJECT / "DATA_DICTIONARY.md").write_text(
        """# Data Dictionary

| Field | Type | Definition |
|---|---|---|
| Employee_ID | Text | Fictional unique identifier beginning `SYN-` |
| Department | Category | Fictional organisational department |
| Location | Category | Fictional work location |
| Job_Level | Category | Entry, Associate, Specialist, or Manager |
| Tenure_Years | Decimal | Generated years of service |
| Performance_Rating | Integer | Generated rating from 1 to 5 |
| Engagement_Score | Integer | Generated score from 0 to 100 |
| Training_Hours_YTD | Integer | Generated year-to-date learning hours |
| Absence_Days_YTD | Integer | Generated year-to-date absence days |
| Monthly_Salary_INR | Integer | Fictional monthly salary for practice |
| Attrition | Yes/No | Generated leaver indicator |

All values are synthetic and must not be interpreted as a real labour-market benchmark.
""",
        encoding="utf-8",
    )
    (PROJECT / "ANALYSIS_NOTES.md").write_text(
        f"""# Analysis Notes

## Reproducible headline metrics

- Synthetic records: {total}
- Generated leavers: {attrition_count}
- Generated attrition rate: {percent(attrition_count, total):.1f}%
- Highest generated department attrition rate: {highest_department}

## Method

1. Generated a deterministic fictional workforce with a fixed random seed.
2. Validated unique IDs and allowed category values.
3. Calculated headcount, leaver count, attrition rate, average engagement, average performance, and average training hours.
4. Compared department and tenure groups using counts and rates.
5. Documented synthetic-data and non-causality limitations.

## Interpretation

The dashboard is descriptive. Differences are intentionally generated for learning and do not prove that engagement, absence, tenure, department, or any other field causes attrition.

## Suggested Power BI measures

```text
Headcount = DISTINCTCOUNT(HR[Employee_ID])
Leavers = CALCULATE([Headcount], HR[Attrition] = "Yes")
Attrition Rate = DIVIDE([Leavers], [Headcount])
Average Engagement = AVERAGE(HR[Engagement_Score])
Average Training Hours = AVERAGE(HR[Training_Hours_YTD])
```

## Interview preparation

Be ready to explain:

- why rate denominators matter;
- why synthetic data was used;
- why descriptive association is not causation;
- how missing values, duplicates, and inconsistent categories would be checked;
- what additional business context would be required before recommending action.
""",
        encoding="utf-8",
    )


def main() -> None:
    PROJECT.mkdir(parents=True, exist_ok=True)
    rows = create_rows()
    csv_path = PROJECT / "synthetic_hr_data.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (PROJECT / "dashboard.html").write_text(create_dashboard(rows), encoding="utf-8")
    write_docs(rows)
    print(f"Generated {len(rows)} synthetic records and dashboard.")


if __name__ == "__main__":
    main()
