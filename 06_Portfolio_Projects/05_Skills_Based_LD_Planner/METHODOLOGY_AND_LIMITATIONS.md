# Methodology and Limitations

## Scenario construction

This is a wholly synthetic portfolio case for a 70-person precision-manufacturing organization. It was designed backwards from a governed decision brief, then constrained so every displayed KPI can be recomputed from the distributed CSVs.

## Dataset generation

### Competencies

Twenty local competencies were mapped to O*NET 31.0 occupation codes. Target and current values were constructed on a 1–5 scale so their exact means are 4.12 and 3.64. `Mean_Gap` is current minus target, producing -0.48 overall. Assessment standards were assigned by construct, ranging from work samples and simulations to document audits and structured rubrics.

### Employee skill profiles

Seventy sequential pseudonymous records were allocated across Engineering (24), Quality (16), Supply Chain (16), and People & Culture (14). Grades G1–G5 recur deterministically. The three mastery components sum to exactly three times each row's overall mastery, and the portfolio mean is exactly 81.4%.

Performance and potential use integers 1–3. The nine-box label is a fixed lookup, enabling deterministic validation. Category counts total 70 and include 14 Star Talent records. Employee skill gaps use a balanced repeating series whose exact mean is -0.48.

### Development plans

Every employee has one IDP and a different in-scope mentor. Fifty-eight are Active and 12 Completed. Level 1 scores repeat a balanced sequence averaging 4.6; Level 2 scores average 88.6%. Level 3 uses Verified/Pending workflow states. Level 4 repeats the governed cohort statement to preserve the analytic grain rather than invent employee-level attribution.

## Computed measures

| Measure | Formula |
|---|---|
| Overall mastery | Mean of `Overall_Mastery_Percent` across filtered employees |
| Competency gap | `Current_Workforce_Proficiency - Target_Proficiency_Baseline` |
| Active IDPs | Count where `Plan_Status = Active` |
| Star cohort | Count where `9_Box_Category = Star Talent` |
| L1 | Mean of `Kirkpatrick_L1_Reaction_Score` |
| L2 | Mean of `Kirkpatrick_L2_Learning_Percent` |

## Limitations

- The sample is a small cohort of 70 and was constructed, not observed.
- Results are descriptive and do not estimate uncertainty or population parameters.
- The Level 4 relationship is not causal; yield, scrap, and savings may reflect many concurrent factors.
- Mastery is a synthetic index, not a validated assessment score.
- O*NET codes provide provenance but do not replace local job analysis.
- Nine-box potential is especially vulnerable to opportunity, visibility, and manager-judgement bias.
- Protected attributes are absent, so group fairness cannot be assessed.
- The repeated one-plan-per-person structure is convenient for demonstration and less complex than production history.
- External content delivery means styling and charts may not load offline; the data table and narrative remain in the document.

## Production validation plan

Use subject-matter-expert review, employee consultation, behaviorally anchored rubrics, assessor training, accessible alternatives, and a documented pilot. Evaluate inter-rater agreement, test/retest stability where relevant, criterion relationships, missingness, subgroup outcomes where lawful, and decision consequences. Pre-register Level 4 outcomes and comparison logic. Keep a change log and rerun reconciliation after every release.

## Ethical use

The tool should support development conversations, resource prioritization, and program evaluation. It should not rank human worth, infer protected traits, automate adverse action, or present cohort outcomes as proof about an individual. Employees need meaningful explanation, access, correction, and challenge routes.
