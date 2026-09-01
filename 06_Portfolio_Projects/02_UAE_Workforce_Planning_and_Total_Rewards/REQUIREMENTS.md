# Project Requirements

## User journeys

1. As an HR analyst, I can reconcile workforce movement and report defensible people metrics.
2. As a rewards analyst, I can compare salaries with hypothetical bands and identify review populations.
3. As a talent-acquisition partner, I can diagnose funnel conversion, time-to-fill and recruitment cost.
4. As an HRBP, I can compare transparent workforce scenarios and communicate a recommendation.
5. As an interviewer, I can trace every dashboard number to a documented formula and source field.

## Functional requirements

- Deterministic synthetic data; no real names, contact details or employer records.
- CSV outputs compatible with Excel, Power Query and Power BI.
- Automated ID, relationship, balance, range, status and funnel tests.
- Dashboard sections for workforce, rewards, recruitment, scenarios and governance.
- Scenario assumptions displayed beside results.
- Clear separation between descriptive findings, assumptions and recommendations.

## Software

- Required: Python 3.9+ and a modern browser.
- Recommended: Excel or another spreadsheet tool.
- Optional: Power BI Desktop on Windows, or Windows through a VM/remote machine when working from macOS.
- No paid API, HRIS account, salary survey or personal employee data is required.

## Acceptance criteria

- All automated tests pass.
- Generation is byte-for-byte reproducible.
- Dashboard works without an internet connection.
- Candidate can reproduce the core metrics and explain limitations without reading a script.
