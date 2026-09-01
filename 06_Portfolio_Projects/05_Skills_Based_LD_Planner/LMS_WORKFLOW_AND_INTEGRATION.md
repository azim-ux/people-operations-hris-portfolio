# LMS Workflow and Integration

## Why this artifact exists

The build specification names 19 deliverables while requiring an exact 20-file inventory. This workflow document is the twentieth governance artifact: it closes the operational gap between approved IDPs, learning assignment, evidence return, and dashboard refresh.

## System boundary

The planner is the decision-support layer; the LMS is the learning-delivery and completion system; the assessment service owns scored evidence; the HRIS owns worker and organization references; the data layer reconciles approved records. None of these systems should silently overwrite another system of record.

## Event flow

1. Manager and employee submit an IDP.
2. L&D applies the approval gate: competency, action, time, mentor, and evidence plan must be complete.
3. The integration maps `Employee_ID`, `Target_Competency_ID`, learning object, due date, and correlation ID.
4. LMS stages the assignment and returns a status without changing mastery.
5. Completion returns as a learning event; it does not set Level 2 or Level 3.
6. Assessment evidence updates Level 2 after validation.
7. Manager observation updates Level 3 through a controlled workflow.
8. Business-owner data updates Level 4 only at the agreed cohort grain.
9. Data steward reconciles counts and releases the dashboard refresh.

## Minimum integration contract

| Field | Direction | Required control |
|---|---|---|
| Correlation ID | Planner → LMS → planner | Idempotent across retries |
| Employee ID | HRIS → planner/LMS | Pseudonymous in analytics extracts |
| Competency ID/version | Ontology → all systems | Reject inactive versions |
| Learning object ID/version | LMS → planner | Preserve historical version |
| Assignment status | LMS → planner | Enumerated state and event time |
| Completion event | LMS → assessment layer | Never equated to mastery |
| Assessment result | Assessment → planner | Evidence type, scorer, and rubric version |
| Error code | Either direction | Human-readable remediation and retry class |

## Failure handling

- Use idempotency keys so retries do not duplicate assignments.
- Quarantine unknown employee, competency, and learning-object references.
- Route recoverable failures to bounded retry; route definition failures to human review.
- Record actor, source, event time, received time, old value, new value, and reason in the audit log.
- Reconcile assigned, active, completed, and rejected counts after every batch.
- Provide rollback to the last approved release when mapping or ontology defects are found.

## Approval gate

No assignment is sent until employee acknowledgement, manager approval, active competency version, accessible learning option, planned hours, and due date are present. Bulk assignment also needs L&D approval and a capacity check.

## Security and privacy

Use service identities with narrow scopes, encryption in transit and at rest, secret rotation, signed events where available, and environment separation. Do not export manager notes, protected attributes, or raw assessment artifacts into the dashboard. Logs should use controlled identifiers and follow retention policy.

## Service targets

| Control | Target |
|---|---:|
| Assignment acknowledgement | Within 15 minutes |
| Event freshness in analytics | Within 24 hours |
| Referential exceptions | Zero at release |
| Duplicate assignments | Zero after idempotency reconciliation |
| Failed-event review | Each business day |

## Release checklist

Validate schema, version mappings, one-record and bulk paths, duplicate retry, inactive competency, inaccessible content, withdrawn employee, late event, rollback, reconciliation, and access logging before production enablement.
