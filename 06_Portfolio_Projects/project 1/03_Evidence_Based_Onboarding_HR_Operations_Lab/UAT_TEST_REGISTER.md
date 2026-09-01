# UAT Test Register

## 1. Test approach

This register demonstrates how APD would validate a Frappe HR–modeled configuration before production. The results below are **synthetic execution results from the design scenario**, not evidence that a live Frappe instance was tested. Each case uses synthetic IDs and no real personal data.

### Entry Criteria

- Approved process, RACI, RBAC, master-data catalogue, and template version are available.
- A segregated UAT environment has representative synthetic configuration and integrations.
- Test users exist for HR, Hiring Manager, IT, Buddy, Employee, Finance, Safety/Quality, and HRIS roles.
- Notification capture, audit logs, reset scripts, and defect tracking are operational.
- Tester and business owner agree expected results and severity rules.

### Exit Criteria

- All 14 planned cases have an evidenced result.
- All Severity 1 and Severity 2 defects are fixed and retested successfully.
- At least 95% of non-critical cases pass, with accepted workarounds for any lower-severity residual defect.
- Permission-negative tests pass; a failed denial test is never waived for release.
- HR Operations, HRIS, IT Security, and the process owner sign the release decision.

## 2. Defect Severity

| Severity | Definition | Release treatment |
|---|---|---|
| S1 Critical | Unauthorized sensitive access, data corruption/loss, or inability to revoke critical access | Immediate stop; release blocked |
| S2 High | Payroll/leave error, failed mandatory workflow, wrong population access, or material audit failure | Release blocked until retest passes |
| S3 Medium | Non-critical function incorrect with a controlled workaround | Owner/date required; risk acceptance required |
| S4 Low | Cosmetic, wording, or minor usability issue without control impact | May be scheduled after release |

## 3. Test cases

### UAT-001 — Create a valid employee master

**Objective:** Verify that HR can create a complete employee record using controlled organizational values.

**Preconditions:** HR test user; approved position; Department, Designation, Grade, Company, and Manager masters active.

**Actions:**

1. Sign in as HR Operations.
2. Create employee `APD-UAT-001` with approved work name, joining date, company, department, designation, grade, and reports-to.
3. Save in Draft, review the generated audit entry, then submit/activate through the approved workflow.
4. Search by employee ID and open the record.

**Expected outcome:** A unique employee ID is created; controlled values resolve correctly; unauthorized fields remain masked; actor/time/status transitions appear in audit history.

**Actual result:** Record created once, retrieved by ID, and audit history showed Draft → Active with the HR test actor.

**Status:** PASS

### UAT-002 — Reject missing and invalid mandatory data

**Objective:** Confirm validation prevents incomplete or inconsistent employee records.

**Preconditions:** HR test user; `INVALID-DEPT` is not an active Department.

**Actions:**

1. Start a new employee record without a joining date or manager.
2. Attempt to save.
3. Add the missing fields but set Department to `INVALID-DEPT` through an import/API test.
4. Attempt to submit.

**Expected outcome:** Save/submit is blocked with clear field-specific errors; no active Employee or orphan onboarding record is created.

**Actual result:** UI validation blocked missing values; API validation rejected the inactive department; no employee ID was committed.

**Status:** PASS

### UAT-003 — Select the correct onboarding template

**Objective:** Verify department/grade rules select the approved template and version.

**Preconditions:** Active templates for Engineering APD-G1 and APD-G4; employee `APD-UAT-003` is Engineering APD-G4.

**Actions:**

1. Open the employee lifecycle action as HR.
2. Create Employee Onboarding for `APD-UAT-003`.
3. Run the template-selection rule.
4. Review department, grade, version, and activity list before submit.

**Expected outcome:** `APD-ONB-ENG-G4-v1.0` is selected; APD-G1 content is not selected; the chosen version is retained on the transaction.

**Actual result:** The G4 Engineering template and correct version were selected; the tester confirmed lead/manager controls were present.

**Status:** PASS

### UAT-004 — Generate owned activities with due offsets

**Objective:** Confirm onboarding submission creates complete, non-duplicate activities.

**Preconditions:** UAT-003 onboarding record is ready to submit; all role assignees active.

**Actions:**

1. Submit the onboarding record.
2. Count generated activities and inspect phase, assigned role, start offset, duration/SLA, and dependency.
3. submit the same action again using a retry simulation.
4. Compare task IDs and counts.

**Expected outcome:** One activity set is created; every required activity has an owner and due rule; retry is idempotent and creates no duplicates.

**Actual result:** The expected activity set was created once; retry returned the existing transaction and task count remained unchanged.

**Status:** PASS

### UAT-005 — Deliver role-scoped notifications

**Objective:** Verify reminders and escalation messages reach the correct recipients without sensitive content.

**Preconditions:** Notification capture enabled; a task due in 24 hours and an overdue test task exist.

**Actions:**

1. Run the scheduled notification job.
2. Inspect employee, task owner, manager, and HR capture mailboxes.
3. Review message subject/body and links.
4. Repeat the job in the same notification window.

**Expected outcome:** Due reminder reaches the owner; overdue escalation reaches owner/manager/HR according to rule; messages contain employee ID and secure link but no restricted field values; duplicates are suppressed.

**Actual result:** Correct recipients and safe content were observed; the second run did not create duplicate messages.

**Status:** PASS

### UAT-006 — Enforce employee self-service scope

**Objective:** Confirm an employee can see their own onboarding plan but not another employee’s record.

**Preconditions:** Employee test users A and B with separate onboarding records.

**Actions:**

1. Sign in as Employee A and open the own-plan link.
2. Update an assigned acknowledgment.
3. Replace the record ID in the URL/API request with Employee B’s ID.
4. Attempt list, report, and export access.

**Expected outcome:** Employee A can read/update only permitted own fields; direct-object, list, report, and export attempts for Employee B are denied and logged.

**Actual result:** Own action succeeded; all cross-record requests returned access denied and created security log entries.

**Status:** PASS

### UAT-007 — Enforce HR population and restricted-field controls

**Objective:** Verify normal HR access and masked restricted fields.

**Preconditions:** Standard HR Operations user and separately approved restricted-case user.

**Actions:**

1. Sign in as standard HR and open an assigned employee.
2. Review core work fields and onboarding scores.
3. Attempt to open health/accommodation case content and export bank fields.
4. Repeat the restricted-case access with the authorized specialist user.

**Expected outcome:** Standard HR can perform assigned lifecycle work but cannot view case content or export bank data; authorized specialist access works within scope and is logged.

**Actual result:** Standard access was denied for restricted content/export; specialist access succeeded and generated a privileged-view log.

**Status:** PASS

### UAT-008 — Prevent IT access to HR adjustment data

**Objective:** Confirm IT can provision access without seeing adjustment scores or private HR fields.

**Preconditions:** IT test user assigned an access task for `APD-UAT-008`.

**Actions:**

1. Sign in as IT and open the assigned task.
2. Record device and account evidence.
3. Attempt to open employee adjustment scores, bank fields, and an HR report URL/API endpoint.
4. Complete the IT task.

**Expected outcome:** IT sees only necessary identity/work/access fields; restricted requests are denied; task completion is allowed and audited.

**Actual result:** Provisioning evidence saved; three restricted requests were denied; task completed with a valid audit trail.

**Status:** PASS

### UAT-009 — Limit manager access to direct reports

**Objective:** Verify manager record scope and approval controls.

**Preconditions:** Manager M1 has direct report A; employee B reports to M2.

**Actions:**

1. Sign in as M1 and open A’s onboarding record.
2. Record a manager checkpoint and approve the role-clarity sign-off.
3. Attempt to open B’s record directly and through dashboard filter/export.
4. Attempt to view A’s bank and health-detail fields.

**Expected outcome:** M1 can act on A within workflow; B and restricted employee fields are inaccessible; denied attempts are logged.

**Actual result:** Direct-report workflow succeeded; cross-manager and restricted-field requests were denied and logged.

**Status:** PASS

### UAT-010 — Constrain buddy permissions and expiry

**Objective:** Verify buddy access contains only navigation-support information and expires.

**Preconditions:** Buddy assigned to Employee A; test clock supports movement beyond closure + 7 days.

**Actions:**

1. Sign in as Buddy and open the buddy task.
2. Record introduction and stakeholder-map completion.
3. Attempt to view scores, manager feedback, compensation, and another newcomer.
4. Close onboarding, advance the test clock eight days, and retry the buddy link.

**Expected outcome:** Buddy can update assigned support tasks only; restricted/cross-record access is denied; access expires after the defined grace period.

**Actual result:** Support task update succeeded; restricted requests were denied; expired link returned access denied after the clock change.

**Status:** PASS

### UAT-011 — Assign leave policy and create allocation

**Objective:** Confirm an approved leave policy assignment generates the correct entitlement record.

**Preconditions:** Active employee, approved 2026 leave period, APD standard leave policy, HR test user.

**Actions:**

1. Create a Leave Policy Assignment using “Joining Date” as the effective basis.
2. Save and submit.
3. Open generated Leave Allocation records.
4. Attempt a duplicate overlapping assignment.

**Expected outcome:** Effective dates derive from joining date; correct allocation records are created once; overlapping duplicate is prevented or routed for explicit exception approval.

**Actual result:** Allocation dates and types matched the policy; the overlapping assignment was blocked with a conflict message.

**Status:** PASS

### UAT-012 — Reproduce dashboard metrics and filters

**Objective:** Confirm extracts and formulas reproduce governed results without hidden row loss.

**Preconditions:** Load the 20 employee and 60 task synthetic records; approved metric dictionary available.

**Actions:**

1. Refresh the extract/report.
2. Recalculate Day-1 mean, SLA index, role-clarity time, cohort count, and escalation count.
3. Filter by each department, status, and grade; clear filters.
4. Open a detail record and trace it to three task rows.

**Expected outcome:** Results equal 93.4%, 88.5%, 24.2 days, 20, and 3; filters preserve valid totals and each employee joins to exactly three tasks.

**Actual result:** All five metrics reproduced; no orphan/duplicate IDs were found; filters and row-to-task trace behaved as expected.

**Status:** PASS

### UAT-013 — Generate complete separation activities

**Objective:** Verify separation launch creates mandatory activities, owners, and timing.

**Preconditions:** Active test employee with device, application access, leave balance, and an approval delegation.

**Actions:**

1. Record an approved last working date and launch the standard separation template.
2. Inspect knowledge transfer, asset return, access revocation, finance, HR closure, and delegated-approval tasks.
3. Compare task owners and event times with the approved template.
4. Attempt closure while one mandatory task remains open.

**Expected outcome:** All mandatory activities are generated and closure is blocked until completion or approved exception.

**Actual result:** Asset, access, finance, and HR tasks were generated, but the delegated-approval reassignment activity was absent. Closure was blocked by other mandatory tasks, yet the missing control requires correction.

**Status:** FAIL — DEF-UAT-013, S2 High

### UAT-014 — Revoke leaver access and verify sessions

**Objective:** Confirm the leaver event revokes all approved access channels and produces evidence.

**Preconditions:** Test employee has directory account, HR self-service, VPN, one API token, physical access, and an active browser session.

**Actions:**

1. Trigger revocation at the approved test event time.
2. Attempt new login to each service.
3. Reuse the existing browser session and API token.
4. Review the revocation control report and exception queue.

**Expected outcome:** New and existing access is denied across all channels; tokens/sessions are invalidated; report contains evidence or a named exception for every entitlement.

**Actual result:** Directory, VPN, HR self-service, API token, and physical access were revoked, but the existing HR self-service browser session remained usable for seven minutes and did not appear as an exception.

**Status:** FAIL — DEF-UAT-014, S1 Critical

## 4. Defect register and release decision

| Defect | Severity | Root-cause hypothesis | Required remediation | Owner | Retest requirement |
|---|---|---|---|---|---|
| DEF-UAT-013 | S2 High | Separation template dependency map omitted delegated-approval ownership | Add reassignment activity, migration check for existing cases, and template-version test | HRIS | Repeat UAT-013 plus regression on standard/manager templates |
| DEF-UAT-014 | S1 Critical | Identity connector disables account but session-revocation endpoint is not called/monitored | Invoke session invalidation, capture response, alert on failure, and add reconciliation | IT Security | Repeat UAT-014 for interactive, mobile, API, and federated sessions |

**Synthetic UAT decision:** **NO-GO**. Twelve of fourteen cases passed (85.7%), but one S1 and one S2 defect remain open. Release is blocked until both fixes pass retest and permission/security regression tests remain successful.

## 5. Evidence pack checklist

- Test data manifest and reset confirmation
- Screenshots or exported audit events with restricted values masked
- Notification captures with recipient and duplicate-control evidence
- Permission-denial logs for employee, manager, buddy, IT, and HR negative tests
- Metric reconciliation worksheet or automated test output
- Defect history, fix reference, retest result, and business sign-off
- Final release decision with environment, configuration version, date, and approvers
