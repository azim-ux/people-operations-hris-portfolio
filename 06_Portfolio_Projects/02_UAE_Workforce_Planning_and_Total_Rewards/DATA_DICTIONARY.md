# Data Dictionary

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
