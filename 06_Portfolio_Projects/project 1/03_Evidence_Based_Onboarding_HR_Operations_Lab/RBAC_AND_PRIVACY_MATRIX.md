# RBAC and Privacy Matrix

## 1. Scope and principles

This design applies role-based access control to the APD employee lifecycle. It is intended to demonstrate privacy-aware configuration, not to provide legal advice or claim compliance certification.

The control model is aligned at a design-principle level with GDPR Article 5 concepts—lawfulness/fairness/transparency, purpose limitation, data minimization, accuracy, storage limitation, and integrity/confidentiality—and with the Digital Personal Data Protection Act, 2023 concepts of lawful purpose, notice/consent where applicable, data accuracy, security safeguards, data-principal rights, and erasure when retention is no longer required. Local counsel and APD’s Data Fiduciary/Controller governance would determine the actual lawful basis, notices, exemptions, retention, and response procedures.

Core rules:

- Deny by default; grant the minimum record, field, action, and duration needed.
- Separate business approval from technical provisioning.
- Restrict special/sensitive categories and free text more tightly than operational metadata.
- Log viewing/export of restricted datasets and all privileged changes.
- Never expose passwords, authentication secrets, bank data, identity-document images, medical data, or investigation notes in onboarding tasks or analytics.
- Require human review for decisions; adjustment scores cannot trigger an adverse action automatically.

## 2. Object-level permission matrix

Legend: **C** create, **R** read, **U** update, **A** approve/submit, **X** export, **—** no access. Scope qualifications are mandatory.

| Object / function | HR | HM | IT | BY | EE | FN | SO | HRIS |
|---|---|---|---|---|---|---|---|---|
| Employee master: core work fields | CRUA, assigned population | R, direct reports | R, ID/name/status/work location only | R, assigned newcomer name/work contact only | R, own record | R, payroll-critical subset | R, name/ID/role for assigned training | CRUX, privileged and logged |
| Employee master: identity documents | CRU, authorized specialists | — | — | — | R, own submitted record where policy permits | — | — | Technical administration only; content access exceptional and logged |
| Bank, tax, and payroll fields | R, limited authorized specialists | — | — | — | R, own masked values; controlled update request | CRUA, assigned population | — | Technical administration only; masked by default |
| Health, disability, accommodation | R, need-to-know case specialists | Functional limitation/action only, not diagnosis | Required technical adjustment only | — | R, own case/decision where appropriate | — | Required safety adjustment only | No routine content access |
| Onboarding record | CRUA, assigned population | RU, direct reports | R/U assigned IT activities | R/U assigned buddy activities only | R/U own assigned activities | R/U assigned finance activities | R/U assigned safety/quality activities | CRUX, privileged and logged |
| Adjustment scores | CRU, assigned population | RU, direct reports | — | — | R, own scores and agreed actions | — | R only where required for safety/quality support | R/X approved aggregate; row access logged |
| Buddy support activity | R, completion and exception only | R, completion and exception only | — | RU, assigned activity | R, own activity | — | — | Configuration and audit metadata |
| Access request | R/U coordination | CRA, direct reports | RU implementation; no business approval | — | R, own request status | A, finance-domain access only | A, quality/safety-domain access only | C/R configuration; privileged access separately approved |
| Leave policy assignment/allocation | CRAU, authorized specialists | R, direct-report balance summary only | — | — | R, own entitlement | R, payroll-relevant result | — | CRUX configuration and audit |
| Separation record | CRAU, assigned population | RU, direct reports | R/U assigned revocation/assets | — | R/U own assigned handover/acknowledgment | R/U/A financial components | R/U assigned clearance | CRUX, privileged and logged |
| Full-and-final components | R, lifecycle fields only | R, approved manager inputs only | R, asset result only | — | R, own approved statement | C/R/U/A/X, segregation of duties enforced | — | Technical administration only |
| Analytics dashboard | R/X approved aggregate and controlled row view | R, direct-report or approved aggregate | R, IT task aggregate; no adjustment scores | — | R, own record if deployed to self-service | R, operational aggregate excluding scores | R, training aggregate | R/X approved administrative view |
| Permission and role configuration | — | — | Technical infrastructure roles only | — | — | — | — | CRUA, maker-checker and time-bound elevation |

`X` never grants unrestricted download. Export requires purpose, population, fields, recipient, retention date, and an audit event.

## 3. Field classification and handling

| Classification | Examples | Storage / display control | Sharing rule |
|---|---|---|---|
| Public organizational | Department names, generic grade definitions, role templates | Approved knowledge repository | May be shared internally; external publication requires owner review |
| Internal operational | Employee ID, work name, designation, manager, task status | HRIS with authenticated role scope | Need-to-know operational sharing |
| Confidential HR | Adjustment scores, extension reason, leave allocation, separation status | Field-level permission, encryption, access log | HR/manager/employee scope as defined; no buddy or broad reporting access |
| Restricted identity/financial | Government ID, bank/tax data, compensation components | Dedicated encrypted fields; masked UI; restricted export | Authorized HR/Finance only for defined purpose |
| Restricted case/special category | Health/accommodation, grievance, investigation, harassment reports | Separate case system or highly restricted module; do not copy to task notes | Named case team only; disclose action requirements without diagnosis |
| Security secret | Passwords, tokens, recovery codes, private keys | Approved identity/secrets system, never HRIS task text | Never transmitted through onboarding tasks or general email |

## 4. Record-scope rules

- Hiring Managers see current direct reports and approved pending joiners; dotted-line access requires separate authorization.
- Buddies see only the assigned newcomer’s business name, work contact, start logistics, and buddy tasks. Buddy access expires at workflow closure plus seven days.
- IT sees fields required to bind the correct account/device and implement approved groups; it does not see adjustment scores, pay, or case details.
- Finance sees payroll and settlement fields for assigned entities; it does not see buddy notes or adjustment scores.
- Employees see their own agreed onboarding plan, tasks, scores, and actions, subject to a governed process for legally privileged or third-party information.
- HRIS administrators use named privileged accounts, MFA, just-in-time elevation where available, and a separate standard account for normal work.

## 5. Joiner–mover–leaver access control

### Joiner

1. Manager requests role access with business purpose.
2. Application/data owner approves the scope.
3. IT stages access and activates it at the approved start event.
4. HR confirms identity-to-account binding without receiving credentials.
5. Manager and IT reconcile temporary/elevated access at Day 30 and Day 60.

### Mover

1. New-role access and incompatible old-role access are analyzed together.
2. New access follows owner approval; old access is removed at the effective event.
3. Temporary overlap requires a reason, risk owner, and expiry.
4. A post-move access review confirms no orphaned approvals or segregation-of-duties conflict.

### Leaver

1. HR provides the approved event time; risk may require earlier suspension through the incident process.
2. IT revokes interactive login, sessions, tokens, groups, delegated access, remote access, and physical access.
3. Managers reassign owned records, workflows, mailboxes, approvals, and shared resources without browsing private content indiscriminately.
4. A control report confirms completion and exceptions. Exceptions need an owner and expiry.

## 6. Audit logging requirements

The production design should log:

- Authentication success/failure, MFA events, privileged elevation, and session revocation
- Create/read/export/update/approve actions on restricted HR objects where technically feasible
- Old value, new value, actor, time, reason, and approval for master-data and workflow changes
- Permission/role changes and changes to report visibility
- Bulk download, API extraction, and scheduled-report delivery
- Template version, activity generation, notification delivery, status transitions, and evidence-reference changes
- Deletion, anonymization, legal hold, and retention-disposition events

Logs must be tamper-resistant, time-synchronized, access-restricted, monitored for anomalous behavior, and retained under an approved schedule. Log content should avoid duplicating sensitive field values.

## 7. Retention schedule for the simulation design

The periods below are proposed controls requiring legal/policy approval before real use.

| Record | Proposed trigger and period | Disposition | Owner |
|---|---|---|---|
| Preboarding records for withdrawn/no-show hire | Withdrawal/no-show + 180 days, unless a dispute hold applies | Delete or irreversibly de-identify | HR Operations |
| Onboarding task metadata and sign-offs | Workflow closure + 3 years | Delete task detail; retain approved aggregate where justified | HR Operations |
| Adjustment pulse scores and extension actions | Workflow closure + 2 years | Delete or de-identify; never move into unrestricted personnel notes | People governance owner |
| Access requests and provisioning/revocation evidence | Access closure + 3 years or security policy period | Secure deletion after hold check | IT Security |
| Safety/quality training attestations | Per applicable regulatory/quality schedule | Archive then dispose under controlled process | Safety/Quality owner |
| Leave allocation and payroll/settlement records | Per employment, tax, and accounting requirements | Controlled archival and deletion | HR/Finance |
| UAT evidence and defect records | Release retirement + 3 years | Delete after audit/hold review | HRIS owner |
| Aggregated, irreversibly de-identified metrics | While purpose remains valid; annual review | Delete when no longer useful | Analytics owner |

Retention is suspended by a documented legal hold, investigation hold, or statutory requirement. A hold must be scoped, approved, reviewed, and released; it is not a reason for indefinite blanket retention.

## 8. Rights and correction workflow

1. Route access, correction, grievance, nomination, or erasure requests to the approved privacy channel.
2. Verify identity proportionately without collecting excessive new data.
3. Search the systems and processors in scope; preserve third-party rights and legal restrictions.
4. Correct source data first, then propagate to authorized downstream copies.
5. Record decision, rationale, response date, approver, and any refusal/appeal route.
6. Do not alter audit history silently; append a correction event.

## 9. Quarterly access review

- HR certifies HR-role membership and population scope.
- Managers certify direct-report and pending-joiner visibility.
- System/data owners certify privileged and domain access.
- HRIS reviews dormant accounts, shared accounts, conflicting roles, exports, and time-bound grants.
- IT tests a sample of joiner, mover, and leaver events against approval and revocation evidence.
- Unresolved high-risk exceptions block release or trigger immediate remediation.
