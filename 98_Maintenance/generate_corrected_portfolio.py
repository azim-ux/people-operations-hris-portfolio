#!/usr/bin/env python3
"""Generate the active, evidence-controlled career portfolio.

The factual content in this file is intentionally conservative. Update the
verified fact register before adding any new claim to a CV or application.
"""

from __future__ import annotations

import csv
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPDATED = "9 August 2026"
ORACLE_BADGE_URL = "https://catalog-education.oracle.com/ords/certview/sharebadge?id=EEB81659F197DAB703AB626ABED829FF6C2A0DDF27309D9C4D3690D71D2CE7A2"


def write(relative_path: str, content: str) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def page(title: str, subtitle: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
  @page {{ size: A4; margin: 14mm; }}
  * {{ box-sizing: border-box; }}
  body {{ max-width: 190mm; margin: 0 auto; color: #172033; font: 10.5pt/1.48 Arial, sans-serif; }}
  h1 {{ margin: 0; color: #17365d; font-size: 23pt; }}
  h2 {{ margin: 22px 0 8px; padding-bottom: 4px; border-bottom: 2px solid #2d6a91; color: #17365d; font-size: 14pt; }}
  h3 {{ margin: 15px 0 4px; color: #224f70; font-size: 11.5pt; }}
  p {{ margin: 6px 0; }}
  ul, ol {{ margin: 6px 0 10px 22px; padding: 0; }}
  li {{ margin: 4px 0; }}
  a {{ color: #185f8d; }}
  table {{ width: 100%; border-collapse: collapse; margin: 9px 0 14px; }}
  th, td {{ border: 1px solid #c7d0da; padding: 7px; vertical-align: top; text-align: left; }}
  th {{ background: #eaf1f6; color: #17365d; }}
  .subtitle {{ color: #526171; margin: 3px 0 14px; }}
  .decision {{ padding: 12px 14px; border-left: 5px solid #26734d; background: #eef8f2; }}
  .warning {{ padding: 10px 13px; border-left: 5px solid #b66a00; background: #fff6e8; }}
  .danger {{ padding: 10px 13px; border-left: 5px solid #a12828; background: #fff0f0; }}
  .note {{ padding: 10px 13px; border-left: 5px solid #2d6a91; background: #edf5fa; }}
  .small {{ color: #596777; font-size: 9pt; }}
  code {{ background: #f2f4f6; padding: 1px 4px; }}
  @media print {{ a {{ color: inherit; text-decoration: none; }} h2, h3 {{ break-after: avoid; }} table, .decision, .warning, .danger, .note {{ break-inside: avoid; }} }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<p class="subtitle">{html.escape(subtitle)} · Verified/updated {UPDATED}</p>
{body}
</body>
</html>"""


PROFILE = {
    "name": "Mohammad Azimuddin",
    "linkedin": "https://www.linkedin.com/in/md-azimuddin-34b088174",
    "location": "Aligarh, Uttar Pradesh, India",
}


EXPERIENCE = [
    {
        "role": "Human Resources Intern",
        "organisation": "TVS Automobile Solutions Pvt. Ltd. (myTVS)",
        "place": "Aligarh, Uttar Pradesh, India",
        "dates": "26 May 2025 – 16 July 2025",
        "bullets": [
            "Completed a seven-week internship in a corporate human resources environment.",
            "Developed practical understanding of recruitment and selection, employee engagement, performance evaluation, and HR documentation, as recorded in the completion certificate.",
            "Demonstrated professional conduct and commitment throughout the internship period.",
        ],
    },
    {
        "role": "Consultant, SURE Program",
        "organisation": "Department of Commerce, AMU × C. T. Bauer College of Business, University of Houston",
        "place": "Aligarh, Uttar Pradesh, India",
        "dates": "August 2024 – October 2024",
        "bullets": [
            "Participated as a Consultant in the 12-week SURE Program.",
            "Learned the structured process of preparing business plans in an MSME-focused consulting programme.",
            "Worked in a collaborative academic setting involving AMU and the University of Houston.",
        ],
    },
    {
        "role": "Intern, Filmsaaz 2023",
        "organisation": "University Film Club, Aligarh Muslim University",
        "place": "Aligarh, Uttar Pradesh, India",
        "dates": "March 2023 – April 2023",
        "bullets": [
            "Recruited as an intern for the 13th Filmsaaz International Short Film Festival.",
            "Contributed as a member of the festival team in a university event environment.",
        ],
    },
]


EDUCATION = [
    (
        "Master of Human Resource Management (MHRM)",
        "Aligarh Muslim University",
        "2024 – 2026",
        "Degree title follows the official AMU 2024–25 admissions guide.",
    ),
    (
        "Bachelor of Arts (B.A.) in Economics",
        "Aligarh Muslim University",
        "2021 – 2024",
        "CGPA: 7.4/10",
    ),
]


CERTIFICATIONS = [
    "Oracle Fusion Cloud Applications HCM Process Essentials Certified – Rel 1 — Oracle, August 2026",
    "Performance Management System — IIM Bangalore / SWAYAM, 2024 (90.4%)",
    "HR Analytics Using Excel — Dayananda Sagar Institutions / SWAYAM, 2024 (78.8%)",
    "Human Resources Analytics — University of California, Irvine, 2023",
    "VITARA-HRMx: Virtual Training to Advance Revenue Administration – Human Resource Management — IMF/edX",
    "AI-Enhanced Power BI three-day workshop — Department of Commerce, Aligarh Muslim University, October 2024",
]


INVOLVEMENT = [
    "Hospitality Committee Volunteer — Spectrum 2K25, Aligarh Muslim University, 19 April 2025",
    "Participant — Insurance and Entrepreneurship Conclave, 13–14 March 2023",
    "Certificate of Appreciation — Aaghaz NGO awareness and mental-health camp",
]


CV_VARIANTS = {
    "02_CV_Library/01_UAE/01_General_HR/Mohammad_Azimuddin_UAE_HR_General.html": {
        "headline": "EARLY-CAREER HR PROFESSIONAL | HR OPERATIONS | RECRUITMENT SUPPORT",
        "market": "UAE",
        "summary": (
            "Early-career human resources professional completing a Master of Human Resource Management "
            "at Aligarh Muslim University in 2026, with a B.A. in Economics and a seven-week HR internship "
            "at TVS Automobile Solutions. Internship learning covered recruitment and selection, employee "
            "engagement, performance evaluation, and HR documentation. Additional applied learning includes "
            "performance management, HR analytics using Excel, and an AI-enhanced Power BI workshop. Seeking "
            "an entry-level HR operations, coordinator, recruitment-support, or people-reporting opportunity "
            "and open to employer-sponsored relocation to the UAE."
        ),
        "skills": [
            "HR foundations: recruitment and selection, employee engagement, performance evaluation, HR documentation",
            "Tools: Microsoft Excel, Microsoft PowerPoint, Microsoft Word; introductory Power BI workshop exposure",
            "Analytics learning: HR analytics coursework, data interpretation, reporting fundamentals",
            "Professional: communication, teamwork, critical thinking, business-plan preparation",
        ],
        "status": "Recommended general UAE version",
    },
    "02_CV_Library/01_UAE/02_HR_Coordinator/Mohammad_Azimuddin_UAE_HR_Coordinator.html": {
        "headline": "HR COORDINATOR | HR OPERATIONS | EMPLOYEE SUPPORT",
        "market": "UAE",
        "summary": (
            "Early-career HR professional completing an MHRM at Aligarh Muslim University, with documented "
            "internship exposure to recruitment and selection, employee engagement, performance evaluation, "
            "and HR documentation at TVS Automobile Solutions. Brings a B.A. in Economics, strong communication "
            "and teamwork, and applied learning in performance management and HR analytics. Seeking an entry-level "
            "HR Coordinator or HR Operations role and open to employer-sponsored relocation to the UAE."
        ),
        "skills": [
            "HR coordination foundations: recruitment support, employee engagement, HR documentation",
            "Performance-management concepts and professional communication",
            "Microsoft Excel, Word, and PowerPoint; introductory Power BI workshop exposure",
            "Organisation, teamwork, critical thinking, and stakeholder communication",
        ],
        "status": "Primary targeted version",
    },
    "02_CV_Library/01_UAE/03_HR_Analyst/Mohammad_Azimuddin_UAE_HR_Analyst.html": {
        "headline": "JUNIOR HR ANALYST | HR REPORTING | PEOPLE ANALYTICS SUPPORT",
        "market": "UAE",
        "summary": (
            "MHRM candidate and Economics graduate seeking a junior HR reporting or people-analytics support role. "
            "Completed assessed courses in Performance Management System (90.4%) and HR Analytics Using Excel "
            "(78.8%), plus a three-day AI-enhanced Power BI workshop. Corporate HR internship exposure at TVS "
            "Automobile Solutions covered recruitment and selection, engagement, performance evaluation, and "
            "documentation. Ready to develop deeper dashboard, HRIS, and workforce-reporting capability on the job."
        ),
        "skills": [
            "HR analytics coursework, performance-management concepts, data interpretation",
            "Microsoft Excel and Microsoft Office; introductory Power BI workshop exposure",
            "Economics foundation, critical thinking, written and verbal communication",
            "HR documentation, recruitment and engagement exposure",
        ],
        "status": "Use only after independently reproducing and explaining the synthetic dashboard project",
    },
    "02_CV_Library/01_UAE/04_Compensation_and_Benefits/Mohammad_Azimuddin_UAE_CB_Analyst.html": {
        "headline": "JUNIOR COMPENSATION & BENEFITS SUPPORT | HR OPERATIONS",
        "market": "UAE",
        "summary": (
            "MHRM candidate and Economics graduate interested in entry-level compensation, benefits, and HR "
            "operations support. Academic strengths include economics, performance management, and HR analytics "
            "using Excel. A seven-week HR internship at TVS Automobile Solutions provided exposure to performance "
            "evaluation and HR documentation. Seeking a supervised junior role in which to build practical payroll, "
            "reward, job-evaluation, and market-pricing experience."
        ),
        "skills": [
            "Economics and quantitative reasoning; performance-management coursework",
            "HR analytics using Excel; Microsoft Office; introductory Power BI workshop exposure",
            "HR documentation and performance-evaluation exposure",
            "Communication, critical thinking, accuracy, and willingness to learn",
        ],
        "status": "Stretch version—do not claim payroll or market-pricing experience",
    },
    "02_CV_Library/02_India/01_General_HR/Mohammad_Azimuddin_India_HR_General.html": {
        "headline": "HR EXECUTIVE | HR OPERATIONS | TALENT ACQUISITION SUPPORT",
        "market": "India",
        "summary": (
            "Early-career HR professional completing a Master of Human Resource Management at Aligarh Muslim "
            "University in 2026, with a B.A. in Economics and corporate HR internship exposure at TVS Automobile "
            "Solutions. Learning covered recruitment and selection, employee engagement, performance evaluation, "
            "and HR documentation. Additional coursework includes performance management, HR analytics using Excel, "
            "and Power BI fundamentals. Seeking an entry-level HR Executive, HR Operations, recruitment-support, "
            "or junior people-reporting position in India."
        ),
        "skills": [
            "Recruitment and selection, employee engagement, performance evaluation, HR documentation",
            "Microsoft Excel, Word, and PowerPoint; introductory Power BI workshop exposure",
            "HR analytics and performance-management coursework",
            "Communication, teamwork, critical thinking, and business-plan preparation",
        ],
        "status": "Primary India version",
    },
    "02_CV_Library/03_Saudi_Arabia/01_General_HR/Mohammad_Azimuddin_Saudi_HR_General.html": {
        "headline": "EARLY-CAREER HR PROFESSIONAL | HR OPERATIONS | RECRUITMENT SUPPORT",
        "market": "Saudi Arabia",
        "summary": (
            "Early-career HR professional completing an MHRM at Aligarh Muslim University, with a B.A. in Economics "
            "and a seven-week HR internship at TVS Automobile Solutions. Documented learning exposure includes "
            "recruitment and selection, employee engagement, performance evaluation, and HR documentation. Seeking "
            "an entry-level HR operations or coordinator opportunity that is explicitly open to international "
            "applicants, and open to employer-sponsored relocation to Saudi Arabia."
        ),
        "skills": [
            "HR foundations: recruitment and selection, engagement, performance evaluation, documentation",
            "Microsoft Excel, Word, and PowerPoint; introductory Power BI workshop exposure",
            "HR analytics and performance-management coursework",
            "Communication, teamwork, critical thinking, and cross-institution collaboration",
        ],
        "status": "Opportunistic version—only for roles open to international applicants",
    },
}


def cv_html(config: dict[str, object]) -> str:
    skills = "".join(f"<li>{html.escape(item)}</li>" for item in config["skills"])
    experience = []
    for item in EXPERIENCE:
        bullets = "".join(f"<li>{html.escape(bullet)}</li>" for bullet in item["bullets"])
        experience.append(
            f"""<div class="entry">
<div class="row"><strong>{html.escape(item['role'])}</strong><span>{html.escape(item['dates'])}</span></div>
<div class="sub">{html.escape(item['organisation'])} · {html.escape(item['place'])}</div>
<ul>{bullets}</ul>
</div>"""
        )
    education = "".join(
        f"""<div class="entry"><div class="row"><strong>{html.escape(degree)}</strong><span>{html.escape(dates)}</span></div>
<div class="sub">{html.escape(institution)} · {html.escape(note)}</div></div>"""
        for degree, institution, dates, note in EDUCATION
    )
    certifications = "".join(
        (
            f'<li><a href="{html.escape(ORACLE_BADGE_URL, quote=True)}">{html.escape(item)}</a> '
            f'<a href="{html.escape(ORACLE_BADGE_URL, quote=True)}">[Verify]</a></li>'
            if item.startswith("Oracle Fusion Cloud Applications HCM Process Essentials Certified")
            else f"<li>{html.escape(item)}</li>"
        )
        for item in CERTIFICATIONS
    )
    involvement = "".join(f"<li>{html.escape(item)}</li>" for item in INVOLVEMENT)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{PROFILE['name']} — {config['headline']}</title>
<style>
  @page {{ size: A4; margin: 11mm 13mm; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0 auto; max-width: 184mm; color: #182331; font: 9.5pt/1.34 Arial, Helvetica, sans-serif; }}
  .header {{ text-align: center; border-bottom: 2px solid #244f70; padding-bottom: 7px; }}
  h1 {{ margin: 0; color: #173a56; font-size: 22pt; letter-spacing: .4px; }}
  .headline {{ margin: 3px 0; color: #315f7e; font-weight: 700; font-size: 10pt; }}
  .contact {{ font-size: 8.8pt; }}
  a {{ color: inherit; text-decoration: none; }}
  h2 {{ margin: 11px 0 5px; padding-bottom: 2px; border-bottom: 1px solid #66869e; color: #173a56; font-size: 11.5pt; letter-spacing: .3px; }}
  p {{ margin: 3px 0; }}
  ul {{ margin: 3px 0 5px 17px; padding: 0; }}
  li {{ margin: 1.8px 0; }}
  .row {{ display: flex; justify-content: space-between; gap: 12px; }}
  .row span {{ white-space: nowrap; }}
  .sub {{ color: #435466; font-size: 9pt; }}
  .entry {{ break-inside: avoid; margin: 0 0 6px; }}
  .status {{ margin-top: 9px; color: #5a6875; font-size: 8pt; text-align: center; }}
  @media print {{ .status {{ display: none; }} }}
</style>
</head>
<body>
<div class="header">
  <h1>MOHAMMAD AZIMUDDIN</h1>
  <div class="headline">{html.escape(str(config['headline']))}</div>
  <div class="contact">
    {html.escape(PROFILE['location'])} · Contact via LinkedIn<br>
    <a href="{PROFILE['linkedin']}">linkedin.com/in/md-azimuddin-34b088174</a> · Target market: {html.escape(str(config['market']))}
  </div>
</div>
<h2>PROFESSIONAL SUMMARY</h2>
<p>{html.escape(str(config['summary']))}</p>
<h2>CORE SKILLS</h2>
<ul>{skills}</ul>
<h2>EXPERIENCE</h2>
{''.join(experience)}
<h2>EDUCATION</h2>
{education}
<h2>SELECTED CERTIFICATIONS & APPLIED LEARNING</h2>
<ul>{certifications}</ul>
<h2>ADDITIONAL INVOLVEMENT</h2>
<ul>{involvement}</ul>
<p class="status">{html.escape(str(config['status']))} · Evidence-controlled edition · Updated {UPDATED}</p>
</body>
</html>"""


def generate_cvs() -> None:
    for output, config in CV_VARIANTS.items():
        write(output, cv_html(config))


def generate_verified_profile() -> None:
    write(
        "01_Source_Evidence/00_Verified_Profile/VERIFIED_FACT_SHEET.md",
        f"""# Verified Fact Sheet

Updated: {UPDATED}

This is the controlling source for CVs, cover letters, emails, LinkedIn updates, and interview preparation. A claim may be added to an application only when its evidence status permits it.

## Identity and contact

- Name: Mohammad Azimuddin
- Location: Aligarh, Uttar Pradesh, India
- LinkedIn: https://www.linkedin.com/in/md-azimuddin-34b088174

## Education

- Master of Human Resource Management (MHRM), Aligarh Muslim University, 2024–2026
  - The official AMU 2024–25 admissions guide lists this programme as MHRM, not MBA.
- Bachelor of Arts in Economics, Aligarh Muslim University, 2021–2024
  - CGPA: 7.4/10

## Directly supported professional experience

- Human Resources Intern, TVS Automobile Solutions Pvt. Ltd., 26 May–16 July 2025
  - Certificate supports learning exposure to recruitment and selection, employee engagement, performance evaluation, and HR documentation.
  - It does not establish ownership of hiring pipelines, onboarding, retention programmes, HR compliance, KPI reporting, or quantified outcomes.
- Consultant, 12-week SURE Program, August–October 2024
  - Joint programme involving AMU and the C. T. Bauer College of Business, University of Houston.
  - Certificate supports participation as a Consultant and learning the business-plan preparation process.
- Intern, Filmsaaz 2023, March–April 2023
  - Selection letter confirms recruitment as an intern for the 13th Filmsaaz festival.

## Selected certifications and learning

- Oracle Fusion Cloud Applications HCM Process Essentials Certified – Rel 1, Oracle, issued 9 August 2026 (`1Z0-1162-1`)
  - Public verification: {ORACLE_BADGE_URL}
  - Supports foundational HCM process knowledge; does not establish production configuration or implementation experience.
- Performance Management System, IIM Bangalore / SWAYAM, 90.4%, 2024
- HR Analytics Using Excel, Dayananda Sagar Institutions / SWAYAM, 78.8%, 2024
- Human Resources Analytics, University of California, Irvine, 2023
- VITARA-HRMx, IMF/edX
- Three-day AI-Enhanced Power BI workshop, AMU, October 2024

## Safe skill wording

- Microsoft Excel, Word, and PowerPoint
- Introductory Power BI workshop exposure
- HR analytics and performance-management coursework
- Recruitment and selection, employee engagement, performance evaluation, and HR documentation exposure
- Communication, teamwork, and critical thinking

## Candidate preferences

- Open to entry-level HR roles in India.
- Open to employer-sponsored relocation for suitable UAE opportunities.
- Saudi applications should be limited to roles explicitly open to international applicants.

## Portfolio project

- A reproducible descriptive HR analytics project using 120 synthetic employee records is stored under `06_Portfolio_Projects`.
- It includes a CSV dataset, dashboard, data dictionary, methodology, limitations, and suggested Power BI measures.
- Add it to a CV only after independently reviewing, reproducing, and explaining the analysis.

## Claims excluded until evidence is added

- MBA degree title
- SHRM-CP Candidate or scheduled-exam status
- Advanced Excel, Power Query, INDEX-MATCH, predictive analytics, or advanced Power BI proficiency
- HRIS, payroll, salary-band design, market pricing, attrition forecasting, or HR ROI experience
- Detailed recruitment, onboarding, retention, compliance, or KPI ownership at TVS
- Passport validity, driving-licence conversion eligibility, visa status, notice date, Arabic ability
- Marital status or religion
- Any invented performance metric, response rate, salary premium, or guaranteed career outcome
""",
    )

    rows = [
        ["Degree title", "Master of Human Resource Management (MHRM)", "A", "Original CV; official AMU 2024–25 admissions guide", "Use"],
        ["MHRM dates", "2024–2026", "A", "Original CV; LinkedIn education capture", "Use"],
        ["BA Economics", "2021–2024; CGPA 7.4/10", "A", "Original CV; LinkedIn education capture", "Use"],
        ["TVS role and dates", "HR Intern; 26 May–16 July 2025", "A", "TVS internship certificate", "Use"],
        ["TVS learning areas", "Recruitment and selection; engagement; performance evaluation; HR documentation", "A", "TVS internship certificate", "Use as exposure/learning"],
        ["TVS detailed duties", "Sourcing, screening, onboarding, KPI tracking, retention, compliance", "C", "No supporting local evidence", "Exclude"],
        ["SURE role and dates", "Consultant; August–October 2024; 12 weeks", "A", "SURE certificate", "Use"],
        ["SURE focus", "Learning business-plan preparation", "A", "SURE certificate", "Use"],
        ["SURE competitive selection/market entry", "Competitive selection; faculty boards; market-entry frameworks", "C", "No supporting local evidence", "Exclude"],
        ["Filmsaaz", "Recruited as intern for 13th Filmsaaz 2023", "A", "Selection letter", "Use"],
        ["Power BI", "Attended three-day AI-enhanced Power BI workshop", "A", "Workshop certificate", "Use as workshop exposure"],
        ["Advanced analytics", "Predictive models, attrition forecasts, dashboards, HR ROI", "C", "No work sample or evidence", "Exclude"],
        ["Performance Management", "IIM Bangalore/SWAYAM; 90.4%", "A", "Certificate capture", "Use"],
        ["HR Analytics Using Excel", "Dayananda Sagar/SWAYAM; 78.8%", "A", "Certificate capture", "Use"],
        ["VITARA-HRMx", "Completed IMF/edX course", "A", "Certificate capture", "Use exact course wording"],
        ["IMF-certified HR professional", "Professional certification implication", "C", "Course completion is not a professional HR designation", "Exclude"],
        ["SHRM-CP Candidate", "Candidate/exam scheduled", "C", "No ATT, accepted application, or booking evidence", "Exclude"],
        ["Driving licence conversion", "Indian licence directly convertible in UAE/KSA", "C", "India absent from current Dubai RTA direct-exchange list", "Exclude"],
        ["Passport/visa/notice", "Valid passport; visa status; September availability", "C", "No supporting document supplied", "Exclude"],
        ["Religion/marital status", "Muslim; single", "C", "Sensitive and unnecessary; religion was inferred", "Exclude"],
        ["Language ability", "Hindi/Urdu/Arabic levels", "C", "No verified proficiency statement supplied", "Exclude until confirmed"],
        ["Salary expectation", "AED 7,500–11,000 likely first offer", "C", "Uncited screenshot; current market aggregates are lower", "Do not present as forecast"],
        ["Synthetic HR analytics project", "Descriptive dashboard using 120 clearly labelled fictional records", "A", "Local reproducible project files", "Use only after independently reproducing and explaining"],
        ["Oracle HCM Process Essentials", "Oracle Fusion Cloud Applications HCM Process Essentials Certified – Rel 1; issued 9 August 2026; exam 1Z0-1162-1", "A", f"Oracle eCertificate supplied and public badge verified at {ORACLE_BADGE_URL}", "Use exact title; foundational process credential only—not production implementation/configuration experience"],
    ]
    path = ROOT / "01_Source_Evidence/00_Verified_Profile/CLAIM_EVIDENCE_REGISTER.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Claim", "Approved Wording or Description", "Evidence Grade", "Evidence", "Decision"])
        writer.writerows(rows)


def generate_research() -> None:
    roles_body = """
<div class="decision"><strong>Recommended positioning:</strong> lead with HR operations and coordination. Add junior HR reporting as a secondary track after producing a genuine work sample.</div>
<h2>Role priority</h2>
<table>
<tr><th>Priority</th><th>Roles</th><th>Why</th><th>Condition</th></tr>
<tr><td>Primary</td><td>HR Coordinator, HR Executive, HR Operations Assistant, Recruitment Coordinator</td><td>Closest match to documented internship exposure and communication strengths</td><td>Use evidence-controlled Coordinator or General CV</td></tr>
<tr><td>Secondary</td><td>Junior HR Analyst, People Reporting Assistant, HR MIS Trainee</td><td>Economics degree and assessed HR analytics learning are relevant</td><td>Attach or link a genuine Excel/Power BI portfolio project</td></tr>
<tr><td>Stretch</td><td>Junior C&amp;B Support, HRIS Assistant, Payroll Assistant</td><td>Relevant academic foundation, but no practical payroll, HRIS, reward, or job-evaluation evidence</td><td>Apply only where training is provided; do not claim prior hands-on experience</td></tr>
<tr><td>Not yet suitable</td><td>HR Business Partner, HR Manager, Senior Analyst, Total Rewards Analyst</td><td>These normally require deeper operational ownership and employment-law judgement</td><td>Reassess after substantial full-time HR experience</td></tr>
</table>
<h2>Defensible strengths</h2>
<ul>
<li>MHRM plus B.A. Economics creates a useful people-and-quantitative foundation.</li>
<li>TVS provides real corporate HR exposure, although the internship was seven weeks and should not be overstated.</li>
<li>Performance Management System (90.4%) and HR Analytics Using Excel (78.8%) provide assessed learning evidence.</li>
<li>SURE adds structured business-plan and cross-institution collaboration exposure.</li>
<li>Communication, teamwork, and critical thinking recur across the source material.</li>
</ul>
<h2>Current gaps</h2>
<ul>
<li>No substantial full-time HR experience or verified ownership of HR processes.</li>
<li>No demonstrated HR dashboard, HRIS, payroll, compensation, or workforce-planning work sample.</li>
<li>No verified advanced Excel or advanced Power BI proficiency.</li>
<li>No documented UAE or Saudi employment-law experience.</li>
</ul>
<h2>Evidence-building plan</h2>
<ol>
<li>Reproduce and extend the included synthetic HR dashboard in Excel or Power BI. Verify every measure against the CSV and explain the data dictionary, calculations, and limitations.</li>
<li>Practise Excel tables, XLOOKUP or INDEX/MATCH, SUMIFS, PivotTables, charts, data validation, and Power Query; claim each only after demonstrating it.</li>
<li>Seek India-based HR operations, recruitment coordination, HR MIS, or payroll-support work that creates verifiable scope.</li>
<li>Record actual volumes and outcomes only when they can be confirmed by records or a supervisor.</li>
</ol>
<div class="note"><strong>Economics remains useful.</strong> The MHRM does not erase the B.A. Economics. It supports HR analytics, workforce reporting, reward fundamentals, and evidence-based people decisions.</div>
"""
    write(
        "03_Career_Research/01_Role_Strategy/Roles_to_Apply_and_Strengths.html",
        page("Role Strategy and Evidence-Building Plan", "Evidence-controlled recommendations for Mohammad Azimuddin", roles_body),
    )

    country_body = """
<div class="decision"><strong>Decision:</strong> use India as the highest-probability route to substantial experience, run a focused UAE search in parallel, and treat Saudi Arabia as an opportunistic market only when a vacancy explicitly accepts international applicants.</div>
<h2>Why the strategy changed</h2>
<p>The earlier UAE-versus-Saudi score used unsupported precision, omitted India, treated sensitive personal characteristics as employability signals, and assumed megaproject demand for fresh international HR graduates. Those assumptions have been removed.</p>
<table>
<tr><th>Market</th><th>Near-term fit</th><th>Main advantage</th><th>Main constraint</th></tr>
<tr><td>India</td><td>Primary</td><td>No relocation or sponsorship barrier; best chance to accumulate verifiable HR scope</td><td>Starting compensation may be lower than Gulf aspirations</td></tr>
<tr><td>UAE</td><td>Parallel selective search</td><td>Large, diverse private sector and relevant coordinator/operations roles</td><td>Remote fresher applications face strong competition and sponsorship friction</td></tr>
<tr><td>Saudi Arabia</td><td>Opportunistic only</td><td>Large transformation programmes and employers with international workforces</td><td>Expanding Saudization and sector localisation reduce entry-level expatriate opportunities</td></tr>
</table>
<h2>Practical application allocation</h2>
<ul>
<li><strong>India:</strong> prioritise live HR operations, recruitment coordination, HR MIS, and trainee roles that offer real process ownership.</li>
<li><strong>UAE:</strong> apply to clearly advertised entry-level roles, recruiter portals, graduate/trainee programmes open to international candidates, and referrals.</li>
<li><strong>Saudi Arabia:</strong> apply only where nationality requirements and sponsorship terms are explicit and compatible.</li>
</ul>
<h2>Salary expectations</h2>
<p>Do not use AED 7,500–11,000 as an expected first-offer range. As a market reference—not a guarantee—Indeed reported an average Dubai HR Coordinator salary of AED 3,928 per month from 191 reported salaries on 10 July 2026. Individual offers vary by employer, role scope, experience, and benefits.</p>
<h2>Decision rules</h2>
<ol>
<li>Judge a role by duties, learning, manager quality, legal sponsorship, and total package—not title alone.</li>
<li>Never describe religion, name, or inferred cultural identity as an employment advantage.</li>
<li>Never claim guaranteed callbacks, savings, promotion speed, or certification salary premiums.</li>
<li>Reassess the market after 12 months of substantial verified HR experience.</li>
</ol>
<h2>Current sources</h2>
<ul>
<li><a href="https://www.hrsd.gov.sa/en/ministry/about-ministry/about-us/ministry-sectors/767512/767566">Saudi HRSD Saudization Agency</a></li>
<li><a href="https://www.hrsd.gov.sa/ur/node/5579002">Saudi HRSD: new Nitaqat phase from 2026</a></li>
<li><a href="https://ae.indeed.com/career/human-resources-coordinator/salaries/Dubai">Indeed Dubai HR Coordinator salary snapshot</a></li>
</ul>
"""
    write(
        "03_Career_Research/02_Country_Strategy/Country_Selection_Analysis.html",
        page("Country Strategy: India, UAE, and Saudi Arabia", "Risk-adjusted early-career plan", country_body),
    )

    benchmark_body = """
<div class="decision"><strong>Recommended CV standard:</strong> one or two pages, single column, text-based PDF, reverse chronological, minimal personal data, and evidence-controlled wording.</div>
<h2>What is genuinely useful</h2>
<ul>
<li>Use a simple hierarchy, standard headings, readable type, and selectable text.</li>
<li>Put name, phone, email, LinkedIn, and current location at the top.</li>
<li>Tailor the summary and skills to the actual vacancy without inventing experience.</li>
<li>Use exact degree and employer names and consistent dates.</li>
<li>Use metrics only when they can be verified.</li>
</ul>
<h2>Claims removed from the old benchmark</h2>
<ul>
<li>There is no substantiated government “MOHRE-compliant CV template” in the cited material.</li>
<li>A photo is not required for an ATS CV and can introduce bias. Add one only when a legitimate employer explicitly requests it.</li>
<li>Nationality, religion, marital status, passport details, driving licence, date of birth, and visa claims are not default CV requirements.</li>
<li>There is no reliable basis here for precise Arabic-language salary premiums or universal certification premiums.</li>
<li>SHRM/CIPD is not required by every Dubai HR Coordinator vacancy.</li>
</ul>
<h2>ATS checklist</h2>
<ol>
<li>Use a text PDF exported directly from the HTML source.</li>
<li>Avoid tables, text boxes, icons used as text, headers/footers containing critical information, and multi-column layouts.</li>
<li>Copy only truthful keywords that match demonstrated knowledge or experience.</li>
<li>Open the PDF, copy its text into a plain-text editor, and confirm the reading order.</li>
<li>Use a clear filename: <code>Mohammad_Azimuddin_UAE_HR_Coordinator_Company_YYYY-MM-DD.pdf</code>.</li>
</ol>
<h2>Driving-licence correction</h2>
<p>India is absent from Dubai RTA's current list for direct licence exchange. Do not state “UAE conversion eligible.” If driving is relevant, verify the exact process with RTA at the time of application.</p>
<h2>Sources</h2>
<ul>
<li><a href="https://www.rta.ae/wps/portal/rta/ae/home/rta-services/service-details?serviceId=121">Dubai RTA licence-exchange service, updated 3 July 2026</a></li>
<li><a href="https://u.ae/en/information-and-services/jobs/employment-in-the-private-sector/working-hours">Official UAE private-sector working-hours guidance</a></li>
</ul>
"""
    write(
        "03_Career_Research/03_CV_Benchmarks/Dubai_HR_CV_Benchmark.html",
        page("Evidence-Controlled UAE HR CV Benchmark", "Practical ATS and credibility standard", benchmark_body),
    )

    shrm_body = """
<div class="decision"><strong>Current exam facts:</strong> SHRM-CP has 134 questions and four hours total, including 3 hours 40 minutes of testing. Do not present a raw “70% passing mark.”</div>
<h2>Exam structure</h2>
<table>
<tr><th>Item</th><th>Current official information</th></tr>
<tr><td>Total questions</td><td>134: 80 knowledge items and 54 situational-judgment items</td></tr>
<tr><td>Field-test items</td><td>24 unscored items mixed into the exam</td></tr>
<tr><td>Time</td><td>Four hours including 3 hours 40 minutes of testing</td></tr>
<tr><td>Delivery</td><td>Computer-based, in person at an authorised Prometric centre</td></tr>
<tr><td>Scoring</td><td>Scaled score; passing candidates receive 200. Do not convert this to an unofficial raw percentage.</td></tr>
</table>
<h2>Candidate-status rule</h2>
<div class="warning">Do not put “SHRM-CP Candidate” or an exam window on the CV until SHRM accepts the application and issues an Authorization to Test letter. “Planning to pursue SHRM-CP” belongs in private planning notes, not credentials.</div>
<h2>Study plan</h2>
<ol>
<li>Read the current SHRM BASK and map weak areas.</li>
<li>Study HR knowledge and behavioural competencies together.</li>
<li>Practise situational-judgment questions by identifying the strategic, ethical, and policy-consistent response.</li>
<li>Complete timed mixed sets, review every incorrect answer, and maintain an error log.</li>
<li>Use full-length practice only after topic foundations are stable.</li>
</ol>
<h2>Current 2026 window and fees</h2>
<p>For the 1 December 2026–15 February 2027 testing window, early-bird applications run 3 June–31 August 2026 and standard applications 1 September–24 December 2026. Current student pricing is USD 150/250 early bird for member/nonmember and USD 199/299 standard, subject to eligibility and checkout conditions.</p>
<h2>Official sources</h2>
<ul>
<li><a href="https://www.shrm.org/credentials/certification/shrm-cp">SHRM-CP format</a></li>
<li><a href="https://www.shrm.org/in/credentials/certification/exam-options-fees">SHRM exam windows and fees</a></li>
<li><a href="https://www.shrm.org/credentials/certification/eligibility-criteria">SHRM eligibility criteria</a></li>
</ul>
"""
    write(
        "03_Career_Research/04_Certification_Plans/SHRM_CP_Syllabus_and_Practice.html",
        page("SHRM-CP Exam Facts and Preparation Plan", "Corrected current guidance", shrm_body),
    )

    comparison_body = """
<div class="decision"><strong>Recommendation:</strong> consider SHRM-CP first only if the exam fits the budget and near-term target roles. Revisit CIPD Level 5 after meaningful HR experience or when a specific employer/market values it.</div>
<h2>Corrected comparison</h2>
<table>
<tr><th>Factor</th><th>SHRM-CP</th><th>CIPD Level 5 Associate Diploma</th></tr>
<tr><td>Type</td><td>Professional certification examination</td><td>Structured qualification delivered through approved study centres</td></tr>
<tr><td>Best fit now</td><td>Early-career HR learner if eligible and prepared</td><td>Better when the learner can connect assignments to practical people-management work</td></tr>
<tr><td>Duration</td><td>Self-directed preparation varies</td><td>Typically 12–16 months</td></tr>
<tr><td>Current cost reference</td><td>2026 student exam fee: USD 150/250 early bird member/nonmember; USD 199/299 standard</td><td>Provider-dependent; CIPD reports a typical UK range of £1,600–£3,600</td></tr>
<tr><td>Current CV wording</td><td>Do not claim candidate status before SHRM acceptance/ATT</td><td>Do not claim enrolment before formal registration</td></tr>
</table>
<h2>Decision sequence</h2>
<ol>
<li>Confirm current SHRM student eligibility and total checkout cost.</li>
<li>Take SHRM-CP only if preparation will not displace job-search and experience-building work.</li>
<li>Do not buy expensive preparation packages automatically; compare official materials and lower-cost practice options.</li>
<li>Revisit CIPD after obtaining substantial HR experience or a clear employer requirement.</li>
</ol>
<h2>Claims removed</h2>
<ul>
<li>Outdated 160-question SHRM format</li>
<li>Separate application fee added on top of prices that already include it</li>
<li>Unsupported salary premiums and guaranteed employer recognition</li>
<li>Overstated total SHRM cost estimates</li>
<li>Shortened CIPD completion timeline</li>
</ul>
<h2>Official sources</h2>
<ul>
<li><a href="https://www.shrm.org/in/credentials/certification/exam-options-fees">SHRM options and fees</a></li>
<li><a href="https://www.cipd.org/uk/learning/qualifications/associate/associate-diploma-in-people-management/">CIPD Level 5 qualification</a></li>
<li><a href="https://www.cipd.org/en/learning/support-for-students/currently-studying/costs-funding/">CIPD costs and funding</a></li>
</ul>
"""
    write(
        "03_Career_Research/04_Certification_Plans/SHRM_vs_CIPD_Action_Plan.html",
        page("SHRM-CP vs CIPD Level 5: Corrected Action Plan", "Cost- and evidence-aware comparison", comparison_body),
    )


def generate_toolkit() -> None:
    checklist_body = """
<div class="decision"><strong>Rule:</strong> every application must be truthful, vacancy-specific, and recorded. Tailoring means selecting relevant verified facts—not adding unsupported keywords.</div>
<h2>Before applying</h2>
<ol>
<li>Confirm the vacancy is current on the employer's official careers site or a reputable platform.</li>
<li>Check location, nationality restrictions, experience, sponsorship, and required tools.</li>
<li>Select the closest active CV: General, Coordinator, Analyst, C&amp;B, India, or Saudi.</li>
<li>Verify every CV statement against the Verified Fact Sheet and Claim Evidence Register.</li>
<li>Change only the headline, summary, skill ordering, and emphasis supported by evidence.</li>
</ol>
<h2>Document checks</h2>
<ul>
<li>Correct degree: Master of Human Resource Management (MHRM).</li>
<li>No SHRM candidate claim unless an ATT exists.</li>
<li>No passport, religion, marital status, licence-conversion, invented language, salary, or visa claim.</li>
<li>PDF is text-selectable, no more than two pages, and uses a clear filename.</li>
<li>Employer and role names match the vacancy exactly.</li>
</ul>
<h2>After applying</h2>
<ol>
<li>Record the application immediately in the tracker.</li>
<li>Save the vacancy URL and submitted CV filename.</li>
<li>Set one appropriate follow-up date; do not repeatedly message the same contact.</li>
<li>Record responses and outcomes so future decisions use actual data.</li>
</ol>
<div class="warning"><strong>Fraud safety:</strong> never pay a recruiter for a job offer, and do not send passport, Aadhaar, banking details, OTPs, or payment before independently verifying the employer and contractual need.</div>
"""
    write(
        "04_Application_Toolkit/01_Per_Application_Checklist.html",
        page("Per-Application Quality Checklist", "Evidence-controlled application workflow", checklist_body),
    )

    cover_body = """
<div class="note"><strong>Target length:</strong> 180–260 words. Replace every bracketed field and remove any sentence that is not relevant to the vacancy.</div>
<h2>Template</h2>
<p>[Date]</p>
<p>Dear [Hiring Manager Name / Hiring Team],</p>
<p>I am applying for the <strong>[exact role title]</strong> position at <strong>[company]</strong>. I am completing a Master of Human Resource Management at Aligarh Muslim University in 2026 and hold a B.A. in Economics.</p>
<p>During a seven-week Human Resources internship with TVS Automobile Solutions, I developed practical understanding of recruitment and selection, employee engagement, performance evaluation, and HR documentation. I also participated as a Consultant in the 12-week SURE Program, focused on the business-plan preparation process in a collaborative AMU–University of Houston setting.</p>
<p>For this role, I would bring <strong>[choose two or three verified strengths from the vacancy: HR documentation / communication / Excel / performance-management learning / HR analytics coursework]</strong>. My assessed learning includes Performance Management System through IIM Bangalore/SWAYAM (90.4%) and HR Analytics Using Excel through Dayananda Sagar Institutions/SWAYAM (78.8%).</p>
<p>I am particularly interested in <strong>[specific, researched reason related to the employer or role]</strong>. I would welcome the opportunity to discuss how my early-career HR foundation, economics background, and willingness to learn could support your team.</p>
<p>Thank you for your consideration.</p>
<p>Sincerely,<br>Mohammad Azimuddin<br>linkedin.com/in/md-azimuddin-34b088174</p>
<h2>Do not add</h2>
<ul>
<li>Unsupported advanced-tool claims, invented metrics, or generic praise.</li>
<li>SHRM-CP candidate status without formal acceptance.</li>
<li>Personal information unrelated to the job.</li>
</ul>
"""
    write(
        "04_Application_Toolkit/02_Cover_Letter_Template.html",
        page("Evidence-Controlled Cover Letter Template", "Concise and vacancy-specific", cover_body),
    )

    targets_body = """
<div class="decision"><strong>Channel priority:</strong> current vacancy → official careers page → referral → reputable recruiter/agency portal → carefully verified direct email.</div>
<h2>Target role families</h2>
<ul>
<li>HR Coordinator, HR Assistant, HR Administrator, HR Operations Assistant</li>
<li>Recruitment Coordinator, Talent Acquisition Assistant, Recruitment Administrator</li>
<li>Junior HR Analyst, HR MIS Trainee, People Reporting Assistant—after creating a work sample</li>
<li>Graduate or trainee programmes explicitly open to international applicants</li>
</ul>
<h2>Employer categories</h2>
<table>
<tr><th>Category</th><th>Examples to research</th><th>Best route</th></tr>
<tr><td>Aviation and logistics</td><td>Emirates Group, dnata, major logistics operators</td><td>Official careers portals</td></tr>
<tr><td>Retail and diversified groups</td><td>Majid Al Futtaim, Al-Futtaim, Landmark Group</td><td>Official portals and referrals</td></tr>
<tr><td>Hospitality</td><td>Jumeirah, Marriott, Hilton, Accor and established hotel groups</td><td>Brand careers portals; verify the property and vacancy</td></tr>
<tr><td>Education</td><td>Established school and higher-education groups</td><td>Official school/group careers pages</td></tr>
<tr><td>Recruitment agencies</td><td>Established UAE agencies with verifiable domains and staff profiles</td><td>Agency portal and one relevant consultant</td></tr>
</table>
<h2>Search routine</h2>
<ol>
<li>Search official career pages and reputable platforms using the exact role families above.</li>
<li>Apply within the vacancy window and save the URL.</li>
<li>Check whether the posting accepts candidates outside the UAE.</li>
<li>Use one relevant recruiter contact rather than mass-emailing multiple people at the same firm.</li>
<li>Measure results from the tracker; do not rely on invented funnel percentages.</li>
</ol>
<div class="warning">This is a target-company research list, not evidence of current vacancies. Verify each vacancy on the day of application.</div>
"""
    write(
        "04_Application_Toolkit/03_Dubai_Target_Companies.html",
        page("UAE Target Employers and Search Channels", "Vacancy-first job-search strategy", targets_body),
    )

    quality_body = """
<div class="decision"><strong>Live DNS result on 27 July 2026:</strong> the active list contained 67 addresses. Sixty-two domains had MX records, four domains had no DNS, and one domain had an A record but no MX. DNS does not verify an individual mailbox.</div>
<h2>Quarantined from the active list</h2>
<table>
<tr><th>Address</th><th>Result</th><th>Action</th></tr>
<tr><td>contact.one@example.com</td><td>Synthetic example</td><td>Do not send</td></tr>
<tr><td>contact.two@example.com</td><td>Synthetic example</td><td>Do not send</td></tr>
<tr><td>contact.three@example.com</td><td>Synthetic example</td><td>Do not send</td></tr>
<tr><td>contact.four@example.com</td><td>Synthetic example</td><td>Do not send</td></tr>
<tr><td>contact.five@example.com</td><td>Synthetic example</td><td>Do not send</td></tr>
</table>
<h2>What MX does and does not prove</h2>
<ul>
<li>MX means the domain is configured to receive email.</li>
<li>It does not prove the named mailbox exists, belongs to the stated employee, or welcomes unsolicited CVs.</li>
<li>Personal/free-email addresses are risk signals requiring verification, not automatic proof of fraud.</li>
<li>Generic finance or information addresses should not receive a CV unless the employer specifically instructs applicants to use them.</li>
</ul>
<h2>Safe contact workflow</h2>
<ol>
<li>Find the vacancy or employer's official careers page first.</li>
<li>Confirm the domain and recruiter identity independently.</li>
<li>Use one relevant contact, a short personalised message, and the role-specific PDF.</li>
<li>Record the actual send date and source.</li>
<li>Never pay fees or send identity/banking documents at the prospecting stage.</li>
</ol>
"""
    write(
        "04_Application_Toolkit/04_Email_List_Quality_Analysis.html",
        page("Email Contact Quality and Safety Audit", "Corrected counts and live domain status", quality_body),
    )

    archived_list = ROOT / "99_Archive/03_Pre_Correction_Snapshot_2026-07-27/04_Application_Toolkit/05_Dubai_HR_Contact_List.txt"
    source = archived_list.read_text(encoding="utf-8")
    active_block = source.split("REMOVED (9)", 1)[0]
    addresses = sorted(
        set(
            address.lower()
            for address in re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", active_block, flags=re.I)
        )
    )
    no_dns_domains = {"example.com"}
    a_only_domains: set[str] = set()
    active = [a for a in addresses if a.rsplit("@", 1)[1] not in no_dns_domains | a_only_domains]
    quarantined = [a for a in addresses if a not in active]
    contact_text = [
        "UAE HR PROSPECT CONTACT LIST — DOMAIN-CHECKED, MAILBOXES UNVERIFIED",
        f"Updated: {UPDATED}",
        "",
        f"ACTIVE PROSPECTS: {len(active)} addresses with domain MX records",
        "IMPORTANT: MX status does not prove that the individual mailbox exists or accepts CVs.",
        "Use only after checking a current vacancy, official website, and recipient relevance.",
        "",
    ]
    contact_text.extend(f"{index:02d}. {address}" for index, address in enumerate(active, start=1))
    contact_text.extend(
        [
            "",
            "QUARANTINED — DO NOT SEND WITHOUT NEW VERIFICATION",
            *[f"- {address}" for address in quarantined],
            "",
            "SAFETY",
            "- Never pay a recruiter or employer to obtain an offer.",
            "- Do not send passport, Aadhaar, bank details, OTPs, or payment at the prospecting stage.",
            "- A free-email address is a reason for additional verification, not automatic proof of fraud.",
        ]
    )
    write("04_Application_Toolkit/05_Dubai_HR_Contact_List.txt", "\n".join(contact_text))

    validation_path = ROOT / "04_Application_Toolkit/08_Contact_Domain_Validation.csv"
    with validation_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Email", "Domain_Status_2026-07-27", "Mailbox_Verified", "Recommended_Action"])
        for address in addresses:
            domain = address.rsplit("@", 1)[1]
            if domain in no_dns_domains:
                writer.writerow([address, "NO_DNS", "No", "Do not send"])
            elif domain in a_only_domains:
                writer.writerow([address, "A_ONLY_NO_MX", "No", "Verify through official website"])
            else:
                writer.writerow([address, "MX", "No", "Use only after vacancy and recipient verification"])

    email_body = """
<div class="note"><strong>Use only after identifying a suitable current role or legitimate talent-pool route.</strong> Keep the message under approximately 130 words.</div>
<h2>Template</h2>
<p><strong>Subject:</strong> Application: [Exact Role Title] — Mohammad Azimuddin</p>
<p>Dear [Name / Hiring Team],</p>
<p>I am applying for the [exact role title] opportunity at [company]. I am completing a Master of Human Resource Management at Aligarh Muslim University in 2026 and have corporate HR internship exposure at TVS Automobile Solutions covering recruitment and selection, employee engagement, performance evaluation, and HR documentation.</p>
<p>[One sentence connecting a verified strength to a requirement in the vacancy.]</p>
<p>I have attached my role-specific CV for consideration. I would welcome the opportunity to discuss how my early-career HR foundation and willingness to learn could support your team.</p>
<p>Kind regards,<br>Mohammad Azimuddin<br>linkedin.com/in/md-azimuddin-34b088174</p>
<h2>Sending rules</h2>
<ul>
<li>Do not use a blanket “Sunday UAE workday” rule; employer schedules vary.</li>
<li>Do not attach certificates, passport, or identity documents to a cold email.</li>
<li>Do not email multiple people at the same organisation simultaneously.</li>
</ul>
"""
    write(
        "04_Application_Toolkit/06_Cold_Email_Template.html",
        page("Vacancy-Specific Email Template", "Short, factual, and respectful", email_body),
    )

    write(
        "04_Application_Toolkit/07_Application_Tracker.csv",
        "Application_ID,Date_Applied,Employer,Role,Location,Job_URL,Source,CV_Version,Cover_Letter,Contact_Name,Contact_Email,Status,Follow_Up_Date,Last_Action,Notes",
    )


def generate_public_pack_text() -> None:
    write(
        "05_Ready_to_Use_Application_Pack/README.md",
        """# Ready-to-Use Application Pack

This folder contains the safest application documents after factual correction.

## Recommended use

- UAE HR Coordinator CV: primary UAE role-specific version
- UAE HR General CV: broader UAE HR operations version
- India HR General CV: primary India version
- Cover letter and email templates: replace every bracketed field

Always rename the chosen CV with the employer and application date before sending. Do not share the full workspace; share only the relevant PDF and tailored message.
""",
    )
    write(
        "05_Ready_to_Use_Application_Pack/Cover_Letter_Template.txt",
        """[Date]

Dear [Hiring Manager Name / Hiring Team],

I am applying for the [exact role title] position at [company]. I am completing a Master of Human Resource Management at Aligarh Muslim University in 2026 and hold a B.A. in Economics.

During a seven-week Human Resources internship with TVS Automobile Solutions, I developed practical understanding of recruitment and selection, employee engagement, performance evaluation, and HR documentation. I also participated as a Consultant in the 12-week SURE Program, focused on the business-plan preparation process in a collaborative AMU–University of Houston setting.

For this role, I would bring [two or three verified strengths connected to the vacancy]. I am particularly interested in [specific researched reason related to the employer or role].

I would welcome the opportunity to discuss how my early-career HR foundation, economics background, and willingness to learn could support your team.

Sincerely,
Mohammad Azimuddin
linkedin.com/in/md-azimuddin-34b088174
""",
    )
    write(
        "05_Ready_to_Use_Application_Pack/Email_Template.txt",
        """Subject: Application: [Exact Role Title] — Mohammad Azimuddin

Dear [Name / Hiring Team],

I am applying for the [exact role title] opportunity at [company]. I am completing a Master of Human Resource Management at Aligarh Muslim University in 2026 and have corporate HR internship exposure at TVS Automobile Solutions covering recruitment and selection, employee engagement, performance evaluation, and HR documentation.

[One sentence connecting a verified strength to a requirement in the vacancy.]

I have attached my role-specific CV for consideration. I would welcome the opportunity to discuss how my early-career HR foundation and willingness to learn could support your team.

Kind regards,
Mohammad Azimuddin
linkedin.com/in/md-azimuddin-34b088174
""",
    )


def main() -> None:
    generate_verified_profile()
    generate_cvs()
    generate_research()
    generate_toolkit()
    generate_public_pack_text()
    print("Corrected portfolio source files generated.")


if __name__ == "__main__":
    main()
