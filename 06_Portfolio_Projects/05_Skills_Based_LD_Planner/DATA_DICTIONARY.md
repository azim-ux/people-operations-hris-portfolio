# Data Dictionary

## Common conventions

- Files use UTF-8 CSV with one header row.
- Identifiers are stable synthetic keys and must not be recycled.
- Percent fields contain numeric values without the percent sign.
- Proficiency values use the governed 1–5 scale.
- Dates are described in milestones rather than stored as person-linked calendar dates in this compact lab.
- Empty values are not used in the supplied datasets.

## `synthetic_competencies.csv`

| Field | Type | Rule / meaning |
|---|---|---|
| Competency_ID | string | Unique `COMP-001`…`COMP-020` |
| ONET_Code | string | O*NET occupation-code provenance anchor |
| Competency_Name | string | Local governed label |
| Department | enum | Engineering, Quality, Supply Chain, People & Culture, or Enterprise |
| Category | enum | Technical, Digital, Compliance, or Leadership |
| Target_Proficiency_Baseline | decimal | Required average on 1–5 scale |
| Current_Workforce_Proficiency | decimal | Synthetic observed average on 1–5 scale |
| Mean_Gap | decimal | Current minus target |
| Assessment_Standard | string | Required evidence method |

## `synthetic_employees_skills.csv`

| Field | Type | Rule / meaning |
|---|---|---|
| Employee_ID | string | Unique `APD-2026-001`…`APD-2026-070` |
| Synthetic_Name | string | Clearly artificial display name |
| Department | enum | Four operating departments |
| Grade | enum | G1, G2, G3, G4, or G5 |
| Performance_Score | integer | 1 Low, 2 Moderate, 3 High |
| Potential_Score | integer | 1 Low, 2 Moderate, 3 High |
| 9_Box_Category | enum | Deterministic performance/potential lookup |
| Technical_Mastery_Percent | decimal | Constructed technical component |
| Compliance_Mastery_Percent | decimal | Constructed compliance component |
| Leadership_Mastery_Percent | decimal | Constructed leadership component |
| Overall_Mastery_Percent | decimal | Exact mean of three component fields |
| Mean_Skill_Gap | decimal | Synthetic employee-level proficiency gap |

## `synthetic_development_plans.csv`

| Field | Type | Rule / meaning |
|---|---|---|
| Plan_ID | string | Unique `IDP-2026-001`…`IDP-2026-070` |
| Employee_ID | foreign key | Must exist in employee file |
| Plan_Status | enum | Active or Completed |
| Target_Competency_ID | foreign key | Must exist in competency file |
| Development_Action | string | Primary practice design |
| Milestone_30_Days | string | Baseline and contract evidence |
| Milestone_60_Days | string | Applied practice and feedback evidence |
| Milestone_90_Days | string | Reassessment and transfer evidence |
| Mentor_Employee_ID | foreign key | Existing employee and not plan owner |
| Planned_Training_Hours | integer | Approved time allocation |
| Kirkpatrick_L1_Reaction_Score | decimal | Reaction score, 1.0–5.0 |
| Kirkpatrick_L2_Learning_Percent | decimal | Learning evidence, 0–100 |
| Kirkpatrick_L3_Behavior_Status | enum | Verified or Pending |
| Kirkpatrick_L4_Result_Measure | string | Governed cohort result statement |

## Join paths

`development_plans.Employee_ID → employees.Employee_ID`, `development_plans.Mentor_Employee_ID → employees.Employee_ID`, and `development_plans.Target_Competency_ID → competencies.Competency_ID`.

## Validation rules

Reject duplicate keys, orphan references, self-mentoring relationships, values outside the published scale, unrecognized enumerations, a component mean that differs from overall mastery, and a gap that differs from current minus target. Publication also requires exact source-to-embedded-data reconciliation.
