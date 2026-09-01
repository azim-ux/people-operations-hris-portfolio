# Kirkpatrick Evaluation Model

## Evaluation contract

The planner uses all four Kirkpatrick levels as separate evidence questions. Completion is not treated as learning, learning is not treated as behavior, and behavior is not treated as business impact.

### Level 1 — Reaction

**Question:** Did participants find the experience relevant, usable, and supportive of the target behavior?

**Field:** `Kirkpatrick_L1_Reaction_Score`, 1.0–5.0. The synthetic portfolio mean is 4.6. A production instrument would also track response rate and item-level distribution; the dashboard's 92% satisfaction marker is a communication KPI rather than a reconstructed response count.

### Level 2 — Learning

**Question:** What knowledge, skill, attitude, confidence, or commitment changed?

**Field:** `Kirkpatrick_L2_Learning_Percent`, 0–100. The synthetic portfolio mean is 88.6%. Preferred evidence is a scored work sample or scenario aligned to the competency standard, with pre/post or mastery-threshold logic defined before launch.

### Level 3 — Behavior

**Question:** Is the critical behavior used on the job under normal conditions?

**Field:** `Kirkpatrick_L3_Behavior_Status`, either Verified or Pending in this lab. Verification requires manager or trained-observer evidence after an agreed transfer window. The 81.4% mastery KPI is an aggregate skill signal and is not a direct count of verified behavior records.

### Level 4 — Results

**Question:** Did the intended operational outcomes move?

**Field:** `Kirkpatrick_L4_Result_Measure`. The governed synthetic cohort outcome is +24.6% yield, -18.2% scrap, and ₹4.8 lakhs savings. These figures are a portfolio scenario and remain non-causal without a defensible counterfactual.

## Measurement plan

| Level | Owner | Timing | Evidence | Escalation trigger |
|---|---|---|---|---|
| L1 | L&D analyst | Within 24 hours | Short relevance/usability pulse | Mean below 4.0 or low response |
| L2 | Assessor | Before and after learning | Aligned work sample or simulation | Mastery below agreed standard |
| L3 | Manager and mentor | 30–90 days | Observation, work artifact, quality record | Transfer blocked or evidence absent |
| L4 | Business owner | Agreed outcome window | Governed operational metric | Definition drift or competing intervention |

## Leading and lagging indicators

Leading indicators include attendance, practice completion, feedback cycles, and critical-behavior opportunity. Lagging indicators include yield, scrap, rework, cycle time, safety, and savings. The system should show both so a weak result can be investigated instead of automatically blamed on the learning program.

## Attribution safeguards

- Define the result and calculation owner before the program begins.
- Record process, staffing, product-mix, equipment, and policy changes during the outcome window.
- Use a comparison group, staggered rollout, interrupted time series, or another locally defensible design where feasible.
- Report uncertainty and missing data.
- Keep individual skill evidence separate from financial attribution.
- Never infer L4 from favorable L1 responses.

## Review cadence

Managers review milestones monthly; L&D reviews L1/L2 quarterly; skill owners review L3 evidence quarterly; business owners review L4 on the metric's natural operational cadence. Any metric-definition change creates a new version and breaks comparability unless a documented bridge is approved.
