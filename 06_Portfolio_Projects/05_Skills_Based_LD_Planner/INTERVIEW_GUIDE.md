# Interview Guide

## 30-second summary

I built a static, privacy-safe L&D planning product that links a 20-skill governed ontology to 70 employee skill profiles, 70 individual development plans, a transparent nine-box review, and Kirkpatrick-aligned evidence. The focus is not course administration; it is traceable decisions, credible measurement, and an operating model managers could actually use.

## Two-minute walkthrough

1. Start with the KPI strip: mastery is 81.4%, 58 plans are Active, and the mean current-to-target gap is -0.48.
2. Use the nine-box matrix to show transparent classification and filter the roster; highlight that it is a conversation aid with a challenge route.
3. Show the O*NET-linked competency comparison: current 3.64 versus target 4.12 across 20 locally validated competencies.
4. Open an employee IDP to connect skill need, action, 30/60/90-day milestones, mentor, time, and L1–L4 evidence.
5. End with the Level 4 boundary: the operational figures are governed cohort associations, not individual or causal claims.

## Likely questions and strong answers

### Why O*NET?

It gives a maintained, licensed provenance layer and reduces blank-page taxonomy design. I did not copy it as a local truth: the project maps occupation codes to local competency wording, assessment standards, targets, owners, and version controls. Production use still needs role-incumbent and subject-matter-expert validation.

### How is mastery calculated?

Each synthetic employee has technical, compliance, and leadership mastery components. Their arithmetic mean equals the stored overall value on every row, and the workforce mean is exactly 81.4%. In production I would replace the constructed values with rubric-aligned evidence and publish reliability/validity findings where appropriate.

### What is the skill gap?

At competency level it is current proficiency minus target proficiency. The means are 3.64 and 4.12, so the governed average gap is -0.48. Negative indicates development demand; it should not be read as a disciplinary score.

### Why use a nine-box at all?

It can create a common calibration language, but it carries serious judgement and opportunity-bias risks. I made the logic explicit—three-point performance crossed with three-point potential—and added evidence, calibration, access, and challenge controls. I would not allow an automated adverse action from the category.

### Why does completion not equal mastery?

Completion only establishes exposure. Kirkpatrick Level 2 needs aligned learning evidence; Level 3 needs behavior on the job; Level 4 needs governed results. The LMS workflow deliberately prevents a completion event from silently setting those fields.

### Can you claim the training improved yield?

No. The +24.6% yield, -18.2% scrap, and ₹4.8 lakhs savings are a synthetic cohort scenario. The project labels them non-causal. A production evaluation would predefine the result, outcome window, confounder log, and a defensible comparison design.

### How did you assure data quality?

I wrote eight acceptance controls before the implementation. They check exact files, schemas, sequential IDs, foreign keys, mentor conflicts, KPI arithmetic, nine-box mapping, privacy patterns, documentation traceability, source-identical embedded JSON, and slide behavior.

### What would you build next?

I would validate behavior anchors with local experts, add rubric-versioned assessment events, introduce historical IDP and ontology tables, implement authenticated row-level access, test accessibility with assistive technology, and design an evaluation with a comparison strategy.

## Tradeoffs to acknowledge

- Static HTML makes the portfolio portable but is not an authorization boundary.
- The dataset is deliberately small and fully synthetic.
- One plan per employee simplifies explanation but omits plan history.
- O*NET occupation codes are provenance anchors, not local validity evidence.
- Nine-box potential requires especially careful governance.

## Questions to ask the interviewer

- How are skills defined, owned, and retired in your organization?
- Where does learning evidence live today, and who trusts it?
- What manager behavior most limits transfer after training?
- Which business result would be valuable enough to evaluate rigorously?
- How can employees access and challenge talent or skill data?
- What decision should the dashboard make easier next quarter?
