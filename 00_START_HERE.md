# Mohammad Azimuddin — Public HR Technology Portfolio

This is the public, privacy-audited entry point for Mohammad Azimuddin’s HR operations and HR technology portfolio. It contains synthetic work samples and automated integrity checks. No phone number, government identifier, source-evidence scan, employment document, CV library, private application record, or machine-specific path belongs in the public release.

## Start here

1. Open the [Master People Operations & HRIS Portfolio](06_Portfolio_Projects/index.html).
2. Read the [portfolio architecture and reproduction guide](06_Portfolio_Projects/README.md).
3. Run the [maintenance test suite](98_Maintenance/README.md) before publishing.

## Featured employee-lifecycle labs

- [Structured Hiring & ATS Architecture Lab](06_Portfolio_Projects/04_Structured_Hiring_and_ATS_Lab/index.html)
- [Evidence-Based 90-Day Onboarding & HR Operations Lab](06_Portfolio_Projects/project%201/03_Evidence_Based_Onboarding_HR_Operations_Lab/index.html)
- [Skills-Based L&D Planner & Talent Growth Engine](06_Portfolio_Projects/05_Skills_Based_LD_Planner/index.html)

Each lab uses synthetic data and documents its methodology, governance controls, limitations, interactive experience, and executive presentation.

## Public repository map

```text
00_START_HERE.md
06_Portfolio_Projects/  Interactive HR technology labs and master hub
98_Maintenance/         Generators, QA records, and automated safety tests
```

Everything outside this public map is local working material and is excluded by the repository ignore policy.

## Pre-push verification

Run from the repository root:

```bash
python3 "98_Maintenance/tests/test_git_push_safety_and_privacy.py"
```

The gate checks the ignore boundary, live Git indexes and history when present, public-scope PII, local paths, non-synthetic email addresses, and relative-link integrity.

## Profile boundary

- Master of Human Resource Management (MHRM), Aligarh Muslim University, 2024–2026
- B.A. in Economics, Aligarh Muslim University
- Oracle Fusion Cloud Applications HCM Process Essentials Certified – Rel 1 (`1Z0-1162-1`)
- Target roles: HR Operations, People Operations, junior HRIS, Talent Acquisition Operations, and L&D coordination
- Professional contact: [LinkedIn](https://www.linkedin.com/in/md-azimuddin-34b088174)

Portfolio metrics are governed synthetic results, not claims about production employers or real employees.
