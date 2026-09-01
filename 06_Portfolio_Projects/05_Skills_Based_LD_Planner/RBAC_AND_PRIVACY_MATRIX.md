# RBAC and Privacy Matrix

## Privacy stance

The lab uses synthetic names and pseudonymous identifiers. A production design should follow least privilege, purpose limitation, data minimization, accuracy, retention control, and human review. India deployment would require a documented assessment against the Digital Personal Data Protection Act (DPDP) and applicable rules; this portfolio is not legal advice.

## Access matrix

| Role | Own IDP | Team skill detail | Organization aggregate | Assessment evidence | Nine-box input | Export | Admin |
|---|---|---|---|---|---|---|---|
| Employee | Read/comment | No | Read | Own evidence | Own outcome explanation | Own record | No |
| Manager | Read/update | Direct reports | Read | Job-relevant summary | Propose for direct reports | Controlled team extract | No |
| Mentor | Assigned plan only | No | No | Practice feedback only | No | No | No |
| L&D analyst | Read/update workflow | Approved scope | Read | Scored evidence summary | Read after calibration | Pseudonymous extract | Limited |
| Skill owner | Competency-linked | Aggregated | Read | Calibration sample | No | Aggregated | Ontology only |
| Data steward | Integrity access | Pseudonymous | Read | Metadata, not narrative | Distribution only | Governed | Data controls |
| Business owner | No | Aggregated | Read | No | Aggregated | Approved aggregate | No |
| System administrator | No business need | No business need | Operational only | No content by default | No | No | Technical configuration |

## Data classification

| Data | Classification | Analytics grain | Default retention |
|---|---|---|---|
| Employee identifier | Confidential | Pseudonymous row | Employment plus approved operational window |
| Skill assessment | Confidential | Individual with restricted access | Review after purpose closes |
| Manager observation | Highly restricted | Summary only in analytics | Short, policy-defined window |
| Nine-box inputs | Highly restricted | Individual in calibration; aggregate elsewhere | Annual review plus challenge window |
| Learning completion | Confidential | Individual | Policy-defined learning record period |
| Cohort business result | Internal | Cohort/process | Financial and operational policy |
| Audit log | Restricted | Event | Security and accountability policy |

The precise production retention schedule must be approved by legal, security, HR, records management, and employee-relations stakeholders. Retention is a limit, not a default instruction to keep every field until the maximum date.

## Control requirements

- **Purpose limitation:** do not reuse development evidence for discipline, surveillance, or unrelated model training without a new lawful basis and transparent review.
- **Minimization:** dashboards receive identifiers and governed scores, not raw narrative evidence.
- **Transparency:** employees can see data meaning, source, use, retention, and challenge route.
- **Accuracy:** disputed records carry a review status and are excluded from irreversible decisions.
- **Separation:** fairness-review attributes, when lawfully collected, remain outside routine manager views.
- **Export control:** watermark, log, scope, and expire extracts; disable broad download by default.
- **Human review:** no automated adverse employment action from mastery or nine-box category.

## Lifecycle

1. Collect only fields tied to a documented L&D purpose.
2. Validate source, consent or other lawful basis where required, and access need.
3. Use within role scope and record material changes.
4. Review access quarterly and on role change.
5. Archive or delete when the purpose and challenge window close.
6. Preserve only records under an approved legal hold.

## Incident and rights handling

Access requests, correction, withdrawal, grievance, and deletion requests follow authenticated workflows with response tracking. Suspected exposure triggers containment, evidence preservation, impact assessment, required notification review, credential rotation, and post-incident control improvement. Employees must not be penalized for exercising a privacy or challenge right.
