# Evidence-Based 90-Day Onboarding & HR Operations Lab

> **Portfolio simulation:** every person, identifier, organization detail, event, score, and operational result in this repository is synthetic. The project is a design demonstration, not a live HR system, legal opinion, or record of an actual employer.

## Executive summary

This lab designs an auditable employee lifecycle for **Apex Precision Dynamics Ltd. (APD)**, a fictional 70-person precision-manufacturing organization operating in India. It converts organizational-socialization research into a controlled 90-day onboarding process, maps that process to open-source Frappe HR concepts, assigns accountable owners through RACI, limits access through role-based controls, tests expected behavior through UAT, and reports synthetic operational outcomes in a standalone dashboard.

The portfolio addresses a practical HR Operations problem: onboarding often exists as a loose checklist, while HRIS records, owner handoffs, evidence, privacy, and escalation controls remain disconnected. The lab joins those elements into one governed operating model.

## Live portfolio

- [Live dashboard](https://azim-ux.github.io/evidence-based-onboarding-lab/)
- [Live five-slide case study](https://azim-ux.github.io/evidence-based-onboarding-lab/slides.html)
- [GitHub repository](https://github.com/azim-ux/evidence-based-onboarding-lab)

## What this project demonstrates

- Research translation: Bauer et al. (2007, 2025) and Saks et al. (2007) are translated into controls for role clarity, task mastery, social acceptance, and organizational understanding.
- Process design: the 18F open onboarding checklist pattern is adapted into Preboarding, Day 1, Week 1, Month 1, Month 2, and Month 3 gates.
- HRIS thinking: Employee, Department, Designation, Grade, Employee Onboarding Template, Task/Assignment, Leave Policy Assignment, and Employee Separation are mapped to Frappe HR concepts.
- Operating governance: 25 activities have RACI ownership; RBAC defines least-privilege access, sensitive fields, and retention controls.
- Quality assurance: 14 UAT cases cover the happy path, negative tests, permissions, notifications, leave allocation, reporting, and separation.
- Analytics: 20 synthetic onboarding records and 60 synthetic tasks reproduce five governed KPIs and four operational visualizations.

## Synthetic organization and scenario

APD has 70 active employees across Engineering & Operations, Quality Assurance, Supply Chain, Finance, and People & Culture. The analytics sample represents 20 synthetic joiners spread across four 2026 quarterly cohorts. The sample is deliberately constructed for process testing and portfolio demonstration; it is not representative of any population or labour-market benchmark.

The dashboard reports a simulated year-end control snapshot:

| KPI | Result | Target | Calculation |
|---|---:|---:|---|
| Day-1 Readiness Rate | 93.4% | >95% | Mean of 20 employee readiness percentages |
| Task SLA Adherence | 88.5% | >90% | `1 − total positive variance hours / total SLA hours` |
| Average Time-to-Role-Clarity | 24.2 days | <30 days | Mean elapsed hours for 20 Day 30 role-clarity sign-offs ÷ 24 |
| Active Onboarding Cohort | 20 | Monitor capacity | Count of employee onboarding records in the simulation |
| Open Escalations & Blockers | 3 | 0 | Sum of open employee escalation counts; matches three task-level escalation flags |

“Task SLA Adherence” is a variance-weighted operational index, not a simple percentage of tasks completed before deadline. Its definition is fixed here and in the methodology so that the displayed result is reproducible.

## Evidence and design logic

The operating model uses four adjustment pillars:

1. **Role Clarity** — documented outcomes, decision rights, manager checkpoints, and a Day 30 sign-off.
2. **Task Mastery** — SOP practice, supervised delivery, competence evidence, and progressive independence.
3. **Social Acceptance** — buddy contact, stakeholder introductions, team participation, and psychological-safety check-ins.
4. **Cultural / Organizational Understanding** — values-in-action examples, governance routes, strategy context, and organizational navigation.

Research supports associations between proximal newcomer adjustment and outcomes such as job attitudes, intentions to quit, and performance. This portfolio does **not** claim that its checklist causes retention or productivity. It also does not infer one-year retention from a 90-day synthetic snapshot.

## Repository guide

| Artifact | Purpose |
|---|---|
| [Interactive dashboard](index.html) | Primary GitHub Pages entry point and standalone analytics interface |
| [Five-slide case study](slides.html) | Responsive presentation with keyboard navigation and five-page print output |
| [Downloadable PDF deck](Evidence_Based_Onboarding_HR_Operations_Case_Study.pdf) | Five-page case-study document for offline review |
| [Responsive phone case-study source](mobile-case-study.html) | Mobile-first HTML source used to produce the portrait edition |
| [Phone-friendly portrait PDF](Evidence_Based_Onboarding_HR_Operations_Mobile_Case_Study.pdf) | Five-page, A5-width tall edition sized for comfortable fit-to-width reading on phones |
| [Research foundation](RESEARCH_FOUNDATION.md) | Evidence review, research-to-control mapping, caveats, and bibliography |
| [Organization and roles](ORGANIZATION_AND_ROLES.md) | APD structure, grade architecture, Frappe mapping, and lifecycle flows |
| [30-60-90 templates](ONBOARDING_TEMPLATES_30_60_90.md) | Phase gates, templates, checklists, evidence, and offboarding workflow |
| [RACI matrix](RACI_MATRIX.md) | Accountability for 25 onboarding and separation activities |
| [RBAC and privacy matrix](RBAC_AND_PRIVACY_MATRIX.md) | Least-privilege permissions, sensitive-field handling, and audit controls |
| [UAT test register](UAT_TEST_REGISTER.md) | Fourteen executable acceptance tests and defect governance |
| [Methodology and limitations](METHODOLOGY_AND_LIMITATIONS.md) | Data generation, formula logic, assumptions, ethics, and limitations |
| [Data dictionary](DATA_DICTIONARY.md) | Field-level definitions and quality rules for both CSVs |
| [Synthetic onboarding records](synthetic_onboarding_records.csv) | Twenty employee-level onboarding records |
| [Synthetic onboarding tasks](synthetic_onboarding_tasks.csv) | Sixty task-level SLA records |
| [MIT license](LICENSE) | Terms for reuse, modification, and distribution |

## How to review the project

1. Open [index.html](index.html) in a modern browser. Internet access is required only for the Tailwind CSS and Chart.js CDNs.
2. Review the five KPIs, then compare departments in the socialization radar and task owners in the SLA chart.
3. Search or filter the employee register and open a row’s “View details” action to inspect milestone progress.
4. Trace the metric definitions to [METHODOLOGY_AND_LIMITATIONS.md](METHODOLOGY_AND_LIMITATIONS.md) and the raw records to the two CSV files.
5. Review [UAT_TEST_REGISTER.md](UAT_TEST_REGISTER.md) to see how the proposed configuration would be validated before release.
6. Open [slides.html](slides.html) for the five-slide recruiter case study, use Left/Right arrows to navigate, download the ready-made [PDF deck](Evidence_Based_Onboarding_HR_Operations_Case_Study.pdf), or use the [phone-friendly portrait edition](Evidence_Based_Onboarding_HR_Operations_Mobile_Case_Study.pdf).

No installation, build process, backend, credentials, or proprietary software is required. The dashboard reads embedded copies of the same synthetic CSV rows so it continues to work when opened directly from the filesystem.

## Audit trail and control conventions

- IDs are stable, unique, sequential, and non-identifying.
- Employee-to-task relationships are enforced through `Employee_ID`.
- Every task records an owner role, SLA, actual elapsed time, variance, status, and escalation flag.
- Process evidence is described as a record reference or approval event; this repository stores no identity documents.
- Manager and buddy IDs are synthetic role-directory identifiers, not additional employee records.
- Extended onboarding is a support decision, not a performance label or disciplinary outcome.
- Dashboard scores are descriptive operational indicators. Small department samples are never used for ranking, automated employment decisions, or causal inference.

## HRIS implementation boundary

This is a **Frappe HR–modeled design**, not a configured production instance and not a claim of certification in Frappe HR, Oracle HCM, SAP SuccessFactors, Workday, or any other platform. A real implementation would require local policy validation, security review, environment configuration, data migration, integration testing, change management, and formal approval by accountable business owners.

## Intended portfolio use

This work is suitable for HR Operations, HRIS, People Analytics, onboarding, employee-experience, and HR transformation discussions. The strongest interview narrative is the control chain: research principle → process gate → system object → accountable role → test case → metric → escalation decision.

## License and attribution

Original project content is released under the [MIT License](LICENSE). External theories, documentation, and open-source frameworks remain subject to their respective copyrights and licenses and are cited in [RESEARCH_FOUNDATION.md](RESEARCH_FOUNDATION.md). No external codebase or employer dataset has been copied into this project.
