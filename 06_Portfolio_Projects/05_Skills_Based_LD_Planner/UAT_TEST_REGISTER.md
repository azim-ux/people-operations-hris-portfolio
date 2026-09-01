# UAT Test Register

## Execution protocol

Run tests with synthetic accounts in a non-production environment. For each case capture release, tester role, date, input fixture, expected result, actual result, evidence reference, severity, and disposition. A Critical or High defect blocks release; Medium requires owner and due date; Low may be accepted by the product owner.

### UAT-001 — Ontology version acceptance

**Role:** Skill Owner. **Action:** Submit a valid competency version with provenance, behavior definition, target, and assessment standard. **Expected:** Approval gate opens; approved version becomes selectable only on its effective date; prior records retain their historical version.

### UAT-002 — Inactive competency rejection

**Role:** L&D Analyst. **Action:** Attempt to create an IDP against an inactive competency. **Expected:** Save is blocked with a clear reason; no LMS event is emitted; attempt is audit-logged.

### UAT-003 — IDP activation gate

**Role:** Manager. **Action:** Activate a plan without employee acknowledgement, mentor, or planned hours. **Expected:** Status remains unapproved and missing requirements are identified without losing entered data.

### UAT-004 — 30/60/90 milestone lifecycle

**Role:** Employee and Manager. **Action:** Record evidence through all three milestones. **Expected:** Events remain ordered and timestamped; closure is unavailable until the 90-day evidence decision is recorded.

### UAT-005 — Mentor conflict prevention

**Role:** L&D Analyst. **Action:** Assign the plan owner as their own mentor. **Expected:** Validation rejects the relationship and suggests a different eligible mentor.

### UAT-006 — LMS idempotent retry

**Role:** Integration Service. **Action:** Resend the same assignment event with its correlation ID. **Expected:** One assignment exists; the duplicate is acknowledged and logged without a second learner record.

### UAT-007 — Completion does not set mastery

**Role:** LMS Administrator. **Action:** Post course completion. **Expected:** Completion updates, while Level 2, Level 3, and mastery remain unchanged until their evidence workflows succeed.

### UAT-008 — Assessment and rubric version

**Role:** Assessor. **Action:** Submit a Level 2 result with an active rubric version. **Expected:** Result is accepted with scorer, evidence type, and rubric version; an unknown version is quarantined.

### UAT-009 — Nine-box calculation

**Role:** Talent Partner. **Action:** Enter all nine combinations of performance and potential scores. **Expected:** Categories exactly match the published lookup, including High/High → Star Talent and Low/Low → Priority Support.

### UAT-010 — Employee challenge workflow

**Role:** Employee. **Action:** Challenge a skill result or nine-box evidence record. **Expected:** Review status is visible; downstream irreversible use is frozen; reviewer and final reason are recorded.

### UAT-011 — RBAC denial and audit

**Role:** Mentor. **Action:** Request a non-assigned employee profile and organization export. **Expected:** Both are denied; permitted assigned-plan feedback remains available; denials are security logged.

### UAT-012 — Dashboard filters and pagination

**Role:** L&D Analyst. **Action:** Combine search, department, grade, and nine-box filters; switch between 25 and 50 rows; page forward and back. **Expected:** counts, page bounds, empty-state message, and restored first page are correct.

### UAT-013 — Drawer sanitization and keyboard use

**Role:** Accessibility Tester. **Action:** Open an IDP from the table using keyboard navigation and inject encoded markup into a test text field. **Expected:** drawer content is rendered as text, focus moves predictably, Escape closes it, and reduced-motion preference is honored.

### UAT-014 — KPI and embedded-data reconciliation

**Role:** Data Steward. **Action:** Compare CSV records, embedded JSON, and dashboard KPIs. **Expected:** 20 competencies, 70 employees, 70 plans, 58 Active, 14 Star Talent, 81.4% mastery, current 3.64, target 4.12, and -0.48 mean gap reconcile exactly.

## Release evidence

Release approval requires all 14 cases executed, automated controls green, no unresolved Critical/High defects, privacy and accessibility review complete, and named owners for accepted residual risk.
