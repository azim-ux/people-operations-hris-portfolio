# Power BI Build Guide

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
