# UAE Workforce Planning and Total Rewards Command Centre

An interview-ready, privacy-safe HR portfolio case for **Gulf Horizon Services LLC (fictional)**. The company, employees, salaries, recruitment activity and scenarios are entirely fictional.

## Business question

How should leadership allocate its people budget to balance retention, fair pay, recruitment demand and planned growth?

## Deliverables

- `dashboard.html` — standalone interactive executive dashboard
- `index.html` — identical GitHub Pages entry point
- `employee_records.csv` — 650 synthetic employee records
- `salary_bands.csv` — 24 hypothetical salary bands
- `monthly_workforce.csv` — 24 months of departmental movements and payroll
- `recruitment_funnel.csv` — synthetic requisition funnel and cost data
- `workforce_scenarios.csv` — baseline, retention and growth scenarios
- `LINKEDIN_CASE_STUDY.md` — source for the LinkedIn document PDF
- `LINKEDIN_POST.md` and `CV_PROJECT_ENTRY.md` — publication-ready copy
- `Mohammad_Azimuddin_UAE_HR_Analytics_Case_Study.pdf` — four-page LinkedIn document
- `LinkedIn_Case_Study_Cover.png` — optional cover preview derived from page one
- supporting requirements, methodology, executive memo, Power BI guide, interview guide and release checklist

## Reproduce

```bash
python3 98_Maintenance/generate_uae_workforce_project.py
python3 -m unittest 98_Maintenance/tests/test_generate_uae_workforce_project.py
```

Open `dashboard.html` directly in a browser. Import the CSV files into Excel or Power BI to recreate the model.

For public release, complete every gate in `PUBLICATION_CHECKLIST.md`, generate the
case-study PDF, and follow `GITHUB_PUBLISHING_GUIDE.md`.

## Ethical boundary

Never describe this as employer data, UAE salary-survey evidence, production Oracle HCM experience, predictive modelling or a guaranteed business result.
