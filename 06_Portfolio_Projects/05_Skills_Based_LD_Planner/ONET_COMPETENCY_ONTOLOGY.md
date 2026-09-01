# O*NET Competency Ontology

## Purpose

The ontology gives the L&D planner a controlled vocabulary for capability demand. It contains 20 competencies mapped to O*NET 31.0 occupation codes, then localized for a synthetic precision-manufacturing context. O*NET source data are available under CC BY 4.0; local wording and proficiency design are scenario-specific transformations.

## Structure

Each competency has:

- a stable local identifier (`COMP-001` through `COMP-020`);
- an O*NET occupation-code provenance anchor;
- a human-readable local name;
- a department or enterprise scope;
- a category: Technical, Digital, Compliance, or Leadership;
- a target proficiency baseline and current workforce average;
- a computed gap (`current - target`);
- an assessment standard that defines the expected form of evidence.

## Proficiency scale

| Level | Operational meaning | Minimum evidence |
|---:|---|---|
| 1 | Awareness | Explains core terms with support |
| 2 | Guided application | Completes a bounded task with coaching |
| 3 | Independent application | Performs recurring work to standard |
| 4 | Advanced application | Handles variance and coaches peers |
| 5 | Enterprise expertise | Designs standards and resolves novel risk |

Targets are role-demand baselines, not ratings of personal worth. A negative gap prioritizes development; it is not a performance sanction.

## Governance workflow

1. Skill owner proposes a change with operational rationale and affected roles.
2. Role incumbents and assessors review observable behaviors and evidence methods.
3. Data steward checks identifiers, formula integrity, and downstream mappings.
4. L&D governance approves the version and effective date.
5. LMS administrator stages the update, tests mappings, and records the release.
6. Dashboard owner refreshes data only after the approval gate succeeds.

## Version control

The version control policy uses semantic ontology releases such as `1.0.0`. Increment the major version for proficiency-scale or identifier-breaking change; the minor version for new competencies or material behavior changes; and the patch version for clarification that does not alter scoring. Store effective date, source O*NET release, approver, reason, affected roles, and migration notes in the audit log.

## Local-validation checklist

- Does each competency describe observable work rather than a personality preference?
- Does its scope avoid duplicating another competency?
- Can two trained assessors distinguish levels 1–5?
- Is the selected assessment standard feasible and accessible?
- Is the target level necessary for the work and not merely aspirational?
- Are role mappings and learning resources current?
- Can employees see, understand, and challenge the evidence?

## Current portfolio

The synthetic ontology spans five Engineering capabilities, four Quality capabilities, four Supply Chain capabilities, four People & Culture capabilities, and three enterprise capabilities. The workforce averages reconcile to current 3.64, target 4.12, and mean gap -0.48 across all 20 competencies.

## Licensing note

O*NET attribution: this product includes information from O*NET Web Services or the O*NET Database by the U.S. Department of Labor, Employment and Training Administration, used under CC BY 4.0. The local competency labels and synthetic values are the portfolio author's transformations and do not imply endorsement by the U.S. Department of Labor.
