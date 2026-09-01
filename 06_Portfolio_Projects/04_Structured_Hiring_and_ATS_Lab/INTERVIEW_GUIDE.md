# Interview Guide: Defending the Project

## 60-second overview

“I designed an enterprise structured-hiring and ATS control model for Apex Precision Dynamics, a fictional manufacturer. It handles 4,000 synthetic applicants across five requisition families, with 986 knockout progressions, 500 assessed finalists, and 120 hires. The system combines a work sample, four-competency BARS interview, and job-knowledge test using a 40/40/20 composite. I also designed idempotent batch screening, human-review routing, score locking, a 48-hour SLA, adverse-impact and Chi-square monitoring, RBAC, retention and erasure workflows, 14 UAT cases, and paginated dashboards. Candidate 0013 is the control: impression was 4.60 but governed composite was 3.92, so the +0.68 gap triggered evidence review rather than an intuitive override.”

## Architecture questions

### Why did you build this as a system rather than only an analytics dashboard?

Hiring quality depends on how evidence is created, who can see it, when it can change, and how a decision is approved. A dashboard can expose outcomes but cannot by itself prevent demographic access, inconsistent questions, late feedback, or score changes. I started with job and data contracts, then designed workflow, permissions, evidence, tests, and reporting around them.

### What are the six ATS stages?

Requisition authorization; application and blind eligibility screen; standardized phone screen and shortlist; work sample and structured assessment; calibration, decision, and offer; then hire transfer, closure, and retention. Each stage has entry criteria, required evidence, owners, and exit controls.

### Why OpenCATS?

OpenCATS provides a recognizable open-source ATS context for a portfolio architecture. I kept the design platform-neutral because real field names, permissions, APIs, and extension points must be validated against the deployed version. The value of the work is the control model and testable requirements, not an unsupported claim that a particular configuration is already production-ready.

### How would you implement score locking?

I would separate draft and submitted states. On submit, the service validates all competencies, writes an immutable version with assessor and timestamp, and denies update permissions. A correction creates a new version referencing the old one, with reason and approver. Peer scores become readable only when the release condition is met.

### How would you make automated knockout safe at 4,000-candidate volume?

I would restrict rules to approved minimum job criteria, version every rule, keep demographic and source fields out of inputs, route missing or ambiguous evidence to human review, and provide a candidate correction route. The worker needs idempotency keys, state validation, bounded batches, retry and dead-letter handling, a kill switch, rollback, and post-batch count reconciliation. Automation can apply a rule consistently; it cannot decide whether the rule is valid.

## Selection-science questions

### Why a structured interview?

Structure improves comparability: job-related questions, consistent core prompts, behaviorally anchored evaluation, trained assessors, evidence notes, and independent scoring. The Sackett et al. revision also warns me not to exaggerate coefficients. The `.42` value in the lab is an external design prior, not a locally proven APD effect.

### What is BARS?

A Behaviorally Anchored Rating Scale describes observable performance at defined levels. In this project, each of four competencies has anchors from 1 to 5. The benefit is shared scoring language; the limitation is that anchors still depend on good job analysis, probing, rater training, and accessibility.

### Why those four competencies?

They cover problem solving and quality, stakeholder conflict, process improvement, and adaptability with ethical governance. Those domains fit all three roles at different technical depths. A production version would use job-analysis evidence to confirm relevance and could vary questions or weighting by role while retaining controlled versions.

### Why 40/40/20?

Work samples and structured interviews receive equal largest weights because they offer complementary job behavior and similar supplied validity priors. Job knowledge adds role-specific evidence with a smaller weight. I would not claim those weights are optimal; any real change requires local evidence, fairness review, and validation.

### How do you calculate candidate 013?

`0.40 × 4.00 + 0.40 × 3.80 + 0.20 × 4.00 = 3.92`. The subjective impression was `4.60`, so the bias-variance gap was `4.60 − 3.92 = +0.68`. The impression has zero decision weight. The gap asks the panel to identify missing job evidence; it is not proof of bias by itself.

### Why not simply use the highest composite?

The candidate must first pass required safety, ethics, and job-critical gates. Then the composite supports ranking. Accessibility, test security, data quality, adverse impact, and evidence integrity must also be sound. A mathematically high score cannot cure an invalid assessment process.

### Explain Taylor–Russell in plain language.

It estimates how the expected proportion of successful hires changes with the current success rate, the fraction of candidates selected, and a locally supported validity coefficient. I presented a sensitivity framework because this synthetic cohort has no outcome criterion and cannot supply a defensible composite validity.

## Fairness questions

### How is the 0.87 adverse-impact ratio calculated?

The Reference Group progression rate is `624/2,400 = 26.000%`. The Focal Group rate is `362/1,600 = 22.625%`. Dividing `22.625% by 26.000%` gives approximately `0.870`, displayed as `0.87`. It is above the 0.80 rule-of-thumb threshold.

### Does 0.87 mean the process is fair?

No. Four-fifths is a screening rule, not a legal safe harbor or proof of equal treatment. The larger sample improves detection but does not validate the rule, accessibility, criterion, or job-family aggregation. I show counts, rates, requisition strata, and significance context so the headline KPI cannot hide risk.

### Why can four-fifths pass while Chi-square is significant?

They answer different questions. Four-fifths compares the size of two selection rates against a practical 0.80 threshold. Chi-square tests whether cohort and progression are independent and becomes more sensitive as sample size grows. In this synthetic table, AIR is 0.87 while Pearson Chi-square is about 5.89 with an illustrative p-value near .015. Neither result alone establishes discrimination, fairness, or job relevance.

### What exactly does knockout progression mean in the dataset?

It is the Stage 2 event in which an applicant passes the versioned minimum-requirement rule and receives a phone-screen score. Exactly 986 candidates progress: 624 Reference and 362 Focal. Of those, 500 complete the work sample and structured assessment. The event definition is fixed so analysts do not mix “passed knockout,” “fully assessed,” and “hired.”

### Should assessors see demographic data to improve fairness?

No. Individual decisions should use job evidence. A restricted compliance role monitors aggregated subgroup outcomes separately. If a pattern appears, the response is to inspect job relevance and process controls, not to alter an individual score because of cohort membership.

## Data and KPI questions

### How did you reconcile time to fill?

The five requisitions are 34.0, 22.0, 30.0, 26.0, and 30.5 days. Their arithmetic mean is `142.5 / 5 = 28.5 days`.

### How did you reconcile the feedback SLA?

There are 2,000 evaluation events. Exactly 1,836 are at or below 48 hours and 164 are above it. `1,836/2,000 = 91.8%`.

### Why are there 2,000 interview records for 500 finalists?

Each finalist has four controlled events: work-sample review, structured interview A, structured interview B, and calibration. The file is an evaluation-event ledger, not a claim that 2,000 distinct candidates had interviews.

### How do the embedded dashboards stay consistent with CSV?

Both pages contain three JSON script blocks whose records match the CSV strings field for field. The acceptance test parses the JSON and compares it with Python’s CSV reader. A source change that is not propagated causes the suite to fail.

## Privacy and governance questions

### What is the key privacy design decision?

Separation. Identity, assessment evidence, demographic monitoring, and administration are different permission surfaces. Hiring roles cannot read demographic cohorts, and no export can combine individual scores with cohort values.

### Why 180 days for rejected résumés?

It is a synthetic APD minimization policy, not a universal legal requirement. It provides a concrete deletion trigger while allowing a bounded period for operational queries. Real deployment would reconcile jurisdictional recordkeeping, legal claims, consent, and processor obligations.

### Walk through an erasure request.

Verify identity proportionately; record scope and jurisdiction; discover live, indexed, exported, processor, and backup copies; assess lawful exceptions; obtain approval; delete or irreversibly de-identify; collect processor evidence; communicate the outcome; retain only the minimum request audit.

### What happens when feedback is late?

At 24 hours the assessor receives a reminder. At 48 hours an SLA breach is logged and the candidate cannot advance on incomplete evidence. At 72 hours the requisition enters a decision hold until a recovery owner is assigned.

## Testing questions

### What does the automated suite verify?

Exact 20-file inventory; schemas; sequential IDs; foreign keys; 5/4,000/2,000 counts; 120 hires by requisition; 500 scored finalists with four events each; scoring formulas; the +0.68 control; time-to-fill, conversion, SLA, and AIR arithmetic; privacy controls; source-identical embedded JSON; pagination requirements; and exactly five keyboard/print-ready slides.

### What would you test next in a real implementation?

Authorization at the API and database layers, concurrent score submissions, audit-log immutability, notification retries, deletion across processors and backups, accessible keyboard and screen-reader flows, export controls, performance at realistic volume, disaster recovery, and statistical monitoring by assessment version and assessor.

## Limitations and improvement questions

### What is the biggest limitation?

There is no local criterion evidence. The data is synthetic, so the project demonstrates architecture and arithmetic, not predictive success. The next research step would be a privacy-reviewed criterion study with independent performance measures, adequate sample size, reliability analysis, and predeclared fairness monitoring.

### What would you improve first?

I would add an accessible assessment-delivery prototype and a formal content-validity trace from job tasks to every prompt and scoring key. Then I would test API-level RBAC and immutable score history in a real OpenCATS extension environment.

### What did this project demonstrate about your work style?

I can translate research and policy into data definitions, workflow states, permissions, operating ownership, user-facing analytics, and executable acceptance criteria. I also separate what the evidence supports from what still requires validation.

## Questions to ask the interviewer

1. Where does unstructured judgment enter your current hiring workflow?
2. How are assessment versions, score changes, and exceptions audited today?
3. Who owns interviewer feedback SLAs and fairness monitoring?
4. Can selection decision-makers access demographic monitoring data?
5. What outcome criterion would be credible enough for a local validation study?
