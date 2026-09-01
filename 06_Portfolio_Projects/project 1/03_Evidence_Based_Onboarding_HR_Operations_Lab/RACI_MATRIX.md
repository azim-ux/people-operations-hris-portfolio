# RACI Matrix

## Purpose

This matrix prevents work from becoming “owned by HR” in the abstract. Each activity has exactly one **Accountable (A)** role. **Responsible (R)** performs the work, **Consulted (C)** provides required input, and **Informed (I)** receives the outcome.

Role codes: **HR** HR Operations; **HM** Hiring Manager; **IT** IT Administrator; **BY** Buddy; **EE** Employee/Newcomer; **FN** Finance/Payroll; **SO** Safety/Quality Owner; **HRIS** HRIS Administrator.

`AR` means the same role is both accountable and responsible. `—` means no formal involvement. Accountability can be delegated only through an approved temporary-delegation record.

| ID | Activity / decision | HR | HM | IT | BY | EE | FN | SO | HRIS | Evidence of completion |
|---|---|---|---|---|---|---|---|---|---|---|
| RACI-01 | Validate approved hire, mandatory master data, candidate consent, and BGV route | AR | C | — | — | I | C | — | C | Validation log and BGV case reference |
| RACI-02 | Create Employee master in Draft | AR | I | — | — | I | I | — | C | Employee ID and audit entry |
| RACI-03 | Approve department, designation, grade, and manager assignment | R | A | — | — | I | C | — | C | Approved position reference |
| RACI-04 | Select and launch onboarding template | AR | C | I | I | I | — | C | C | Template version and launch event |
| RACI-05 | Prepare 30/60/90 role charter and outcomes | C | AR | — | C | C | — | C | — | Accepted role charter |
| RACI-06 | Nominate, brief, and confirm buddy | I | AR | — | R | I | — | — | — | Buddy acceptance and backup |
| RACI-07 | Request business application and data access | C | AR | C | — | I | C | C | C | Approved access request |
| RACI-08 | Approve application/data access by control owner | I | A | C | — | I | R | R | C | Approval evidence by system/domain |
| RACI-09 | Provision device, account, MFA, and approved groups | I | I | AR | — | I | — | — | C | Provisioning and access-test log |
| RACI-10 | Validate Day-1 readiness gate and exceptions | AR | R | R | I | I | — | C | C | Readiness check and owners |
| RACI-11 | Deliver safety, security, confidentiality, and quality essentials | C | I | R | — | R | — | AR | I | Completion attestations |
| RACI-12 | Conduct role and decision-rights orientation | C | AR | — | I | R | — | C | I | Role charter acknowledgment |
| RACI-13 | Complete buddy introduction and stakeholder map | I | C | — | AR | R | — | — | — | Stakeholder map reference |
| RACI-14 | Deliver supervised first work sample and feedback | I | AR | — | C | R | — | C | — | Work sample and feedback evidence |
| RACI-15 | Conduct Day 30 role-clarity review and sign-off | C | A | — | C | R | — | — | R | Score, sign-off, and action log |
| RACI-16 | Conduct Day 60 task-mastery and social-support review | C | A | I | C | R | — | C | R | Review evidence and actions |
| RACI-17 | Conduct Day 90 overall adjustment review | R | A | I | C | R | — | C | C | Overall score and decision |
| RACI-18 | Approve supported onboarding extension | R | A | I | I | C | — | C | C | Reason, support, owner, next date |
| RACI-19 | Monitor SLA exceptions and coordinate escalations | AR | R | R | I | I | I | R | C | Escalation log and ageing |
| RACI-20 | Assign approved leave policy and verify allocation | AR | I | — | — | I | C | — | C | Policy assignment and allocation IDs |
| RACI-21 | Reconcile onboarding access at Day 30/60 | C | A | R | — | I | C | C | C | Access reconciliation report |
| RACI-22 | Authorize separation and confirmed last working date | R | A | I | — | I | C | — | I | Approved separation case |
| RACI-23 | Complete knowledge and work handover | I | A | — | — | R | — | C | I | Accepted handover record |
| RACI-24 | Revoke logical/physical access and recover IT assets | I | C | AR | — | I | — | C | C | Revocation and asset evidence |
| RACI-25 | Complete final settlement, employee-status closure, and retention routing | A | I | I | — | I | R | — | C | Approved settlement and closed record |

## Preboarding third-party BGV SLA overlay

Background verification (BGV) is a vendor-supported sub-process within `RACI-01`, monitored through `RACI-10` and escalated through `RACI-19`. The vendor is not added as an internal RACI role: HR remains accountable for case initiation, consent, status monitoring, and evidence routing, while the provider performs the contracted checks.

| Preboarding item | Turnaround commitment | Clock start and stop | Internal ownership | Completion evidence |
|---|---|---|---|---|
| Standard BGV | 7 business days | Starts when the provider accepts a complete, consented case; pauses only for a documented candidate-information dependency | HR Operations Specialist responsible; Head of HR Operations accountable for the vendor control | Provider status, completion date, exception reason, and restricted report reference |
| Fast-Track BGV | 3 business days | Starts on approved fast-track acceptance; requires a joining-date risk or business-critical rationale and budget approval | HR Operations Specialist responsible; Hiring Manager consulted; Head of HR Operations accountable | Fast-track approval, provider status, completion date, exception reason, and restricted report reference |

The general task record stores only status and a restricted evidence reference. It must not contain identity-document images, raw screening results, or adverse-action narrative. A vendor delay is not automatically attributed to the candidate and does not by itself authorize an employment decision.

## Tiered SLA escalation protocol

The overdue clock starts at the task’s approved due timestamp. Automation evaluates open tasks hourly, records each notification in the escalation log, and sends a level only once unless the owner or due date changes through an approved record.

| Level | Automated trigger | Routing and mandatory action | Closure evidence |
|---|---|---|---|
| Level 1 | Delay > 24 hours | Automated system notification to the Task Owner, with CC to the Hiring Manager; owner records cause, next action, and recovery time | Notification event and acknowledged recovery plan |
| Level 2 | Delay > 48 hours | Escalation alert to the HR Operations Specialist and mandatory daily stand-up flag until a recovery owner is confirmed | Escalation event, stand-up flag, owner, and target time |
| Level 3 | Delay > 72 hours | Direct escalation to the Head of HR Operations; apply a Day-1 badge/system access hold where the unresolved item creates an identity, safety, or unauthorized-access risk; authorize emergency task reassignment | Leadership decision, scoped hold or exception, reassignment, and resolution evidence |

The Day-1 badge/system access hold is a risk control, not a blanket employment hold. It applies only to the affected physical or logical access. HR and the Hiring Manager must provide a safe alternative work plan where possible, and the newcomer must not lose pay or be penalized for an internal or vendor-owned delay.

## Control interpretation

- `RACI-08` uses the Hiring Manager as accountable for ensuring that every requested access item has the correct domain-owner approval; Finance and Safety/Quality are responsible only for the systems/data they control. IT implements but does not grant itself business authorization.
- `RACI-15` to `RACI-17` keep the Hiring Manager accountable for employment-context judgments while the employee contributes evidence and HR maintains process integrity.
- `RACI-20` separates policy administration from financial consultation and HRIS configuration.
- `RACI-25` makes HR accountable for lifecycle closure while Finance remains responsible for financial settlement calculations and approval according to delegated authority.

## Escalation and delegation rules

1. Safety, harassment, retaliation, unauthorized access, and identity/payment risks bypass routine cadence and follow the approved incident route.
2. An accountable owner may name a temporary delegate only with scope, start/end time, reason, and approver recorded.
3. A responsible role cannot mark an approval complete on behalf of the accountable role unless the delegation control is active.
4. Any activity overdue by more than its approved tolerance must have an owner, next action, and target time; a status change alone does not resolve the exception.
5. RACI defines process ownership, not data access. Permissions remain governed by [RBAC_AND_PRIVACY_MATRIX.md](RBAC_AND_PRIVACY_MATRIX.md).
