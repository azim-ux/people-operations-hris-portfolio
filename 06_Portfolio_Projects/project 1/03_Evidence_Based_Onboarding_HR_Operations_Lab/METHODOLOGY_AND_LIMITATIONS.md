# Methodology and Limitations

## 1. Project method

The lab follows a traceable design sequence:

1. Review organizational-socialization evidence and identify operational constructs.
2. Translate constructs into phase gates, owned activities, evidence, and escalation rules.
3. Map the lifecycle to Frappe HR concepts without claiming an installed production system.
4. Define RACI and RBAC separately so accountability does not imply unrestricted data access.
5. Create synthetic employee/task extracts that exercise normal, in-progress, extended, and escalated paths.
6. Specify UAT cases for functions, negative validation, permissions, analytics, leave, and separation.
7. Calculate operational indicators from declared formulas and expose them through a static dashboard.
8. Document limitations, fairness risks, and implementation dependencies.

## 2. Synthetic data generation

All entities were authored specifically for this project. No source dataset, real employee file, public profile, resume, or proprietary HR record was sampled.

### Employee records

- Twenty unique IDs follow `APD-2026-001` through `APD-2026-020`.
- Joining dates span Q1, Q2, Q3, and Q4 of the synthetic 2026 scenario.
- Five department codes and five grades are represented.
- Names are fictional labels used for interface testing. Any resemblance to a real person is coincidental.
- Manager and buddy IDs are synthetic role-directory references, not people in the 20-row cohort.
- Three employee records contain one open escalation each and are marked `Escalated` with supported extension enabled.
- Adjustment scores are bounded synthetic observations selected to exercise department, status, and detail views.

### Task records

- Sixty IDs follow `TASK-001` through `TASK-060`.
- Every employee has exactly three analytical task records: a Day-1 readiness verification, a Day 30 role-clarity sign-off, and one sampled phase-specific operational activity.
- Each row links to one valid employee ID and contains an owner role, SLA, actual elapsed hours, arithmetic variance, status, and escalation flag.
- The task extract is a controlled analytics sample, not the complete activity library in the onboarding template.
- Six tasks contain historical or open positive variance. Three are closed historical delays and three are open escalation-required blockers.

### Scenario-time note

The rows are a synthetic lifecycle replay used to test a complete dashboard, not a claim that every score existed on the joining date or on August 31, 2026. Joining dates anchor four quarterly cohorts; status and scores represent the lab’s modeled review state. A live implementation would enforce “as-of” dates and show unavailable future milestones as null rather than populate them for interface testing.

## 3. Reproducible KPI definitions

### 3.1 Day-1 Readiness Rate

For employee (i), let (D_i) be `Day1_Readiness_Score` on a 0–100 scale.

`Day-1 Readiness Rate = Σ D_i / employee record count`

The 20 scores sum to 1,868. Therefore:

`1,868 / 20 = 93.4%`

Target: greater than 95%. The metric is a mean readiness score, not the percentage of employees with every item complete.

### 3.2 Task SLA Adherence

For task (j):

- `Variance_Hours = Actual_Hours − SLA_Hours`
- `Positive_Delay_Hours = max(Variance_Hours, 0)`

`Task SLA Adherence = [1 − Σ Positive_Delay_Hours / Σ SLA_Hours] × 100`

Across 60 task rows:

- Total SLA commitment = 15,840 hours
- Total positive delay = 1,821.6 hours
- `1 − (1,821.6 / 15,840) = 0.885`
- Result = **88.5%**

Target: greater than 90%. This variance-weighted index penalizes the magnitude of delay. It is not the simple proportion of completed-within-SLA tasks and should not be compared to an organization that uses a different denominator.

### 3.3 Average Time-to-Role-Clarity

Select the 20 task rows whose `Task_Name` is exactly `Day 30 Role Clarity Sign-off`.

`Average days = Σ (Actual_Hours / 24) / 20`

The elapsed times total 484 days, so `484 / 20 = 24.2 days`.

Target: less than 30 calendar days. The metric indicates process elapsed time to a documented conversation; it is not proof that ambiguity is permanently resolved or that productivity was achieved.

### 3.4 Active Onboarding Cohort

`Active Onboarding Cohort = count of employee records in the selected lab cohort = 20`

“Active” means included in the dashboard’s selected simulation cohort. Workflow status is separately displayed as Completed, In Progress, or Escalated.

### 3.5 Open Escalations & Blockers

`Open Escalations = Σ Escalations_Count = 3`

This matches the three task rows with `Escalation_Required = Yes`. Historical delayed tasks with `Escalation_Required = No` contribute to SLA delay but not to the open escalation count.

## 4. Visualization calculations

### Socialization radar

Department values are arithmetic means of employee scores:

- Role Clarity = `Day30_Role_Clarity_Score`
- Task Mastery = `Day30_Task_Mastery_Score`
- Social Acceptance = `Day60_Social_Acceptance_Score`
- Culture / Organizational Understanding proxy = arithmetic mean of those three scores for each employee

The proxy is disclosed because the fixed employee CSV does not contain a separate culture field. It must not be interpreted as value conformity, belonging diagnosis, or a validated fit scale.

### SLA performance by owner role

For each of HR, IT, Hiring Manager (`HM`), and Buddy (`BY`), apply the same variance-weighted formula to tasks assigned to that role. The displayed role index is bounded to 0–100 so accumulated delay cannot create a negative percentage. Employee-owned tasks are excluded from this owner comparison but remain in the overall KPI.

### Milestone stage progress

For each ordered phase—Preboarding, Day 1, Week 1, Month 1, Month 2, Month 3—the dashboard calculates:

`Phase completion % = Completed tasks in phase / all sampled tasks in phase × 100`

This is stage progress, not a person-level survival funnel. Different phases have different sample sizes because the 60-row task file is an analytical sample.

### Delay and ageing categories

Only task names containing IT Provisioning, Manager Feedback, or Document Verification are classified. Positive variance is counted in three ageing buckets:

- 0–48 hours
- 49–168 hours
- More than 168 hours

Rows without positive variance are not counted as delays. “IT Provisioning Remediation” maps to IT Provisioning by keyword.

## 5. Data-quality controls

- Exact headers and controlled values are defined in [DATA_DICTIONARY.md](DATA_DICTIONARY.md).
- IDs must be unique and nonblank.
- Every task employee ID must exist in the employee file.
- Scores must remain within their declared ranges.
- `Variance_Hours` must equal actual minus SLA, including decimals.
- Escalation count and task escalation flags must reconcile at the portfolio snapshot level.
- CSV files use UTF-8, comma delimiter, one header row, and no formulas/macros.
- Dashboard JSON is tested against the CSV rows to prevent drift.

## 6. Research interpretation

The design uses meta-analytic evidence to choose constructs worth observing. It does not reproduce study effect sizes, validated survey instruments, or causal identification. Associations reported in prior literature can be influenced by selection, measurement, study design, job type, labour market, management quality, and other contextual factors.

This lab therefore avoids the claims “onboarding increased retention,” “reduced time-to-productivity,” or “improved job satisfaction.” It has no comparison group, pre-period, randomized intervention, validated satisfaction measure, objective productivity measure, or one-year retention outcome.

## 7. Limitations

1. **Synthetic sample:** results describe constructed records and have no external validity.
2. **Small groups:** department averages use few records; apparent differences are not statistically meaningful.
3. **Selected task sample:** three tasks per employee do not represent the full onboarding workload.
4. **Operational score design:** the 1–5 values are anchored for demonstration but are not a validated psychometric instrument.
5. **Culture proxy:** a calculated proxy cannot replace a dedicated, validated organizational-understanding measure.
6. **Static interface:** the HTML dashboard has no authentication, backend, row-level security, workflow engine, or persistent updates.
7. **CDN dependency:** Tailwind CSS and Chart.js require internet access; source data and text still reside in the local file.
8. **HRIS abstraction:** Frappe HR objects are mapped conceptually; exact fields, permissions, and behavior vary by version/configuration.
9. **Legal localization:** privacy, employment, tax, safety, recordkeeping, consultation, and accessibility duties require jurisdiction-specific review.
10. **No production assurance:** UAT results are scripted synthetic outcomes. A real deployment needs environment evidence and formal sign-off.

## 8. Ethical safeguards

- Do not use onboarding scores as automated hiring, confirmation, promotion, pay, discipline, or termination inputs.
- Discuss low scores with the employee and investigate system, role, access, workload, manager, or team barriers.
- Avoid demographic inference and protected-class comparisons in small samples.
- Provide a correction route and meaningful explanation of measures.
- Keep narrative case details outside general task records and analytical extracts.
- Report aggregates only where group sizes and context protect confidentiality.
- Review measures for differential impact, gaming, response pressure, and unintended manager surveillance.

## 9. Production-readiness work still required

A real implementation would require configuration in a segregated environment, data-protection impact assessment where appropriate, records-of-processing updates, security threat modeling, integration design, migration reconciliation, notification/content approval, accessibility testing, performance testing, backup/recovery testing, operating procedures, user training, change communications, support model, cutover plan, and post-launch control monitoring.
