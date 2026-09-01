# Data Dictionary

## 1. File standards

Both files contain synthetic portfolio data only. They use UTF-8 encoding, comma delimiters, a single header row, ISO 8601 dates (`YYYY-MM-DD`), period decimals, and no formulas. IDs are case-sensitive and immutable.

## 2. `synthetic_onboarding_records.csv`

Grain: one row per synthetic onboarding employee record. Primary key: `Employee_ID`.

| Field | Type / format | Allowed values or rule | Meaning and control |
|---|---|---|---|
| Employee_ID | Text, `APD-2026-NNN` | Unique, nonblank; 001–020 in this file | Synthetic lifecycle identifier; never reused |
| Full_Name | Text | Nonblank synthetic label | Interface-test display name; not a real identity |
| Department | Categorical text | Engineering; Quality; Supply Chain; Finance; People & Culture | Analytics code mapped to the formal department in the organization document |
| Designation | Text | Active approved synthetic job title | Role title at joining |
| Grade | Categorical text | APD-G1; APD-G2; APD-G3; APD-G4; APD-G5 | Five-band synthetic grade architecture |
| Joining_Date | Date | Valid 2026 ISO date | Scenario anchor; sample spans all four quarters |
| Onboarding_Status | Categorical text | Completed; In Progress; Escalated | Latest workflow state in the simulation |
| Manager_ID | Text, `APD-MGR-*` | Nonblank synthetic role-directory ID | Reporting manager reference; not part of the 20-row employee sample |
| Buddy_ID | Text, `APD-BDY-*` | Nonblank synthetic role-directory ID | Assigned buddy reference; access is time-bound |
| Day1_Readiness_Score | Decimal percentage | 0–100 inclusive | Composite operational readiness score; file mean is 93.4 |
| Day30_Role_Clarity_Score | Decimal rating | 1.0–5.0 inclusive | Anchored Day 30 understanding of outcomes, standards, boundaries, and escalation routes |
| Day30_Task_Mastery_Score | Decimal rating | 1.0–5.0 inclusive | Anchored evidence of early task proficiency and appropriate independence |
| Day60_Social_Acceptance_Score | Decimal rating | 1.0–5.0 inclusive | Anchored access to support, integration, and psychological safety |
| Day90_Overall_Adjustment_Score | Decimal rating | 1.0–5.0 inclusive | Synthetic holistic review, not a performance rating or automated decision input |
| Escalations_Count | Nonnegative integer | 0 or 1 in this file | Number of open onboarding blockers at snapshot; total equals 3 |
| Extended_Onboarding_Flag | Boolean text | Yes; No | Whether a time-bound supported extension is active |

### Record validation rules

- `Onboarding_Status = Escalated` requires `Escalations_Count > 0` and `Extended_Onboarding_Flag = Yes` in this design.
- `Escalations_Count = 0` must align with no open task escalation for that employee.
- Department, Grade, Status, and Flag reject unapproved variants or extra whitespace.
- The dashboard culture dimension is calculated; it is not a hidden source column.

## 3. `synthetic_onboarding_tasks.csv`

Grain: one row per synthetic analytical task. Primary key: `Task_ID`. Foreign key: `Employee_ID` → onboarding records.

| Field | Type / format | Allowed values or rule | Meaning and control |
|---|---|---|---|
| Task_ID | Text, `TASK-NNN` | Unique, nonblank; 001–060 | Stable analytical task identifier |
| Employee_ID | Text | Must exist in employee file | Join to the employee onboarding record |
| Phase | Categorical text | Preboarding; Day 1; Week 1; Month 1; Month 2; Month 3; Offboarding | Lifecycle stage; Offboarding is permitted by schema but not present in this onboarding sample |
| Task_Name | Text | Nonblank controlled activity name | Human-readable task/control; exact role-clarity name supports KPI selection |
| Assigned_Role | Categorical text | HR; HM; IT; BY; EE | Responsible role: HR Operations, Hiring Manager, IT, Buddy, or Employee |
| SLA_Hours | Positive decimal | >0 | Committed elapsed-hour allowance for the analytical control |
| Actual_Hours | Nonnegative decimal | ≥0 | Synthetic elapsed hours to result/snapshot |
| Variance_Hours | Decimal | Must equal `Actual_Hours − SLA_Hours` | Negative = within allowance; positive = delayed |
| Status | Categorical text | Completed; In Progress; Overdue | Task state at synthetic snapshot |
| Escalation_Required | Boolean text | Yes; No | Whether the task is an open escalation; exactly three Yes rows |

### Task validation rules

- Every employee appears exactly three times in this 60-row analytical sample.
- The exact task name `Day 30 Role Clarity Sign-off` occurs once per employee.
- `Escalation_Required = Yes` requires `Status = Overdue`.
- A positive variance may be historical and resolved when Status is Completed and Escalation_Required is No.
- Decimal arithmetic must preserve `309.6` and `357.6`; binary floating display should be rounded for presentation only.

## 4. Four-pillar pulse instrument definitions

These are **project-authored** employee-experience items informed by organizational-socialization constructs, not reproduced or validated Bauer scale items. All use [1–5] Likert responses: 1 = Strongly disagree, 2 = Disagree, 3 = Neither agree nor disagree, 4 = Agree, and 5 = Strongly agree. Missing or declined responses remain null and are excluded from means.

| Instrument item | Exact wording and scale | Data-contract treatment |
|---|---|---|
| Role Clarity (Day 30) | “I have a clear understanding of the goals, priorities, and performance expectations for my role.” [1–5] | Maps to `Day30_Role_Clarity_Score` |
| Task Mastery (Day 60) | “I can independently execute my daily operating procedures without frequent supervisor intervention.” [1–5] | Future implementation field `Day60_Task_Mastery_Score`; current `Day30_Task_Mastery_Score` remains the earlier synthetic checkpoint and is not relabeled |
| Social Acceptance (Day 60) | “I feel welcomed, supported by my buddy, and psychologically safe within my immediate team.” [1–5] | Maps to `Day60_Social_Acceptance_Score`; follow-up separates the three concepts when support is needed |
| Organizational Understanding (Day 90) | “I understand how my department's goals align with APD's strategic mission and governance policies.” [1–5] | Future implementation field `Day90_Organizational_Understanding_Score`; it is not interchangeable with `Day90_Overall_Adjustment_Score` |

The future fields are design definitions only and are not added to either CSV, preserving the published data contract. Survey responses are conversation inputs, not automated probation, performance, or termination rules.

## 5. Derived measures

| Measure | Source | Formula |
|---|---|---|
| Day-1 Readiness Rate | employee file | Mean `Day1_Readiness_Score` |
| Task SLA Adherence | task file | `[1 − Σ max(Variance_Hours,0) / Σ SLA_Hours] × 100` |
| Average Time-to-Role-Clarity | task file | Mean `Actual_Hours / 24` where Task_Name exactly matches the role-clarity sign-off |
| Active Onboarding Cohort | employee file | Row count in selected lab cohort |
| Open Escalations & Blockers | employee/task files | Sum employee escalation count; control-check against count of task escalation Yes |
| Culture / Organizational Understanding proxy | employee file | Per-employee mean of role clarity, task mastery, and social acceptance; then department mean |
| Phase completion | task file | Completed tasks ÷ all sampled tasks in each phase |
| Delay ageing | task file | Count positive-variance category tasks in 0–48, 49–168, >168 hour buckets |

## 6. Commercial friction scenario fields

The leadership brief supplied this scenario expression:

`Cost of 3-Day Workstation Delay = (Annual Salary ÷ 260 Working Days) × 3 Idle Days + Lost Project Velocity ($1,250/day proxy) = ~$2,450 per delayed technical hire.`

The result is **unreconciled**: three days at `$1,250/day` already equal `$3,750`, so `~$2,450` cannot be reconciled with the supplied formula and a positive annual salary. Under a fully synthetic `$100,000` salary assumption, the reconciled calculation is `($100,000 ÷ 260 × 3) + ($1,250 × 3) = $4,903.85`.

| Scenario input / output | Type | Definition |
|---|---|---|
| `Annual_Salary_Assumption` | Currency | Scenario-only annual salary; not present in the CSVs and not an APD observation |
| `Working_Days_Assumption` | Integer | 260 for this illustration; must be versioned for a real organization |
| `Idle_Days` | Nonnegative decimal | Workstation-delay duration; three in the example |
| `Velocity_Proxy_Per_Day` | Currency | Scenario-only opportunity-cost proxy; `$1,250/day` in the supplied brief |
| `Estimated_Delay_Cost` | Currency | `(Annual Salary ÷ Working Days × Idle Days) + (Velocity Proxy Per Day × Idle Days)` |

The value is a sensitivity-analysis prompt, not booked cost, realized savings, an employee productivity rating, or a market benchmark.

## 7. Privacy classification

The CSVs contain internal operational fields and fictional display names. They intentionally exclude date of birth, home address, phone, personal email, government identifiers, bank/tax data, compensation, health/accommodation information, leave detail, grievances, investigations, protected characteristics, passwords, and free-text case notes.

If adapted to real data, replace names with governed pseudonymous IDs for analytics, enforce purpose/role scope, set an approved retention date, suppress small groups, and complete privacy/security review before export.
