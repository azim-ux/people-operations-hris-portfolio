#!/usr/bin/env python3
"""Build the Obsidian navigation and reference layer for the career workspace."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "09_Obsidian_Hub"
UPDATED = "2026-08-05"

SOURCE_SECTIONS = [
    "01_Source_Evidence",
    "02_CV_Library",
    "03_Career_Research",
    "04_Application_Toolkit",
    "05_Ready_to_Use_Application_Pack",
    "06_Portfolio_Projects",
    "07_Remote_Job_Applications",
    "08_Employment_Exit_Documents",
    "98_Maintenance",
    "99_Archive",
]


def wikilink(path: str, label: str | None = None) -> str:
    return f"[[{path}|{label or Path(path).name}]]"


def mdlink(note_path: Path, target: Path, label: str | None = None) -> str:
    relative = target.relative_to(ROOT).as_posix()
    encoded = quote(relative, safe="/._-~")
    return f"[{label or target.name}](/" + encoded + ")"


def note(title: str, note_type: str, tags: list[str], body: str, status: str = "current", aliases: list[str] | None = None) -> str:
    frontmatter = [
        "---",
        f'title: "{title}"',
        f"type: {note_type}",
        f"status: {status}",
        f"updated: {UPDATED}",
        "tags: " + json.dumps(tags, ensure_ascii=False),
    ]
    if aliases:
        frontmatter.append("aliases: " + json.dumps(aliases, ensure_ascii=False))
    frontmatter.extend(["---", "", f"# {title}", "", body.strip(), ""])
    return "\n".join(frontmatter)


def write(relative: str, content: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


def section_files(section: str) -> list[Path]:
    base = ROOT / section
    return sorted(p for p in base.rglob("*") if p.is_file() and not p.name.startswith(".DS_Store"))


def directory_listing(section: str, intro: str) -> str:
    files = section_files(section)
    rows = [intro, "", f"**Files indexed:** {len(files)}", ""]
    current_parent: Path | None = None
    for path in files:
        parent = path.parent.relative_to(ROOT)
        if parent != current_parent:
            rows.extend([f"## `{parent.as_posix()}`", ""])
            current_parent = parent
        relative = path.relative_to(ROOT).as_posix()
        flag = " — temporary/lock file; do not rely on it" if path.name.startswith("~$") else ""
        rows.append(f"- {wikilink(relative, path.name)} · {format_size(path.stat().st_size)}{flag}")
    return "\n".join(rows)


def current_job_table() -> str:
    pack = ROOT / "07_Remote_Job_Applications" / "2026-07-31_High_Paying_Early_Career"
    matrix = pack / "00_Target_Job_Matrix.csv"
    rows = [
        "| # | Category | Company | Role | Fit/status | Files | Application |",
        "|---:|---|---|---|---|---|---|",
    ]
    with matrix.open(newline="", encoding="utf-8-sig") as handle:
        for item in csv.DictReader(handle):
            number = int(item["Priority"])
            folder = pack / item["Folder"]
            notes = folder / "APPLICATION_NOTES.md"
            pdfs = sorted(folder.glob("*_Resume.pdf"))
            file_links = [wikilink(notes.relative_to(ROOT).as_posix(), "notes")]
            if pdfs:
                file_links.append(wikilink(pdfs[0].relative_to(ROOT).as_posix(), "CV"))
            rows.append(
                f"| {number} | {item['Category']} | {item['Company']} | {item['Role']} | "
                f"{item['Status']} | {' · '.join(file_links)} | [open]({item['Application URL']}) |"
            )
    return "\n".join(rows)


def full_catalog() -> str:
    body = [
        "This catalog is generated from the filesystem. Use `Cmd+F` inside this note or Obsidian's global search.",
        "",
    ]
    total = 0
    for section in SOURCE_SECTIONS:
        files = section_files(section)
        total += len(files)
        body.extend([f"## {section} ({len(files)} files)", ""])
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            body.append(f"- {wikilink(relative, relative)} · {format_size(path.stat().st_size)}")
        body.append("")
    body.insert(2, f"**Total indexed source files:** {total}\n")
    return "\n".join(body)


def main() -> None:
    for relative in [
        "09_Obsidian_Hub/01_Profile",
        "09_Obsidian_Hub/02_Career_Strategy",
        "09_Obsidian_Hub/03_Applications",
        "09_Obsidian_Hub/04_Employment",
        "09_Obsidian_Hub/05_Portfolio_and_AI",
        "09_Obsidian_Hub/06_Conversation_Summaries",
        "09_Obsidian_Hub/07_File_Maps",
        "09_Obsidian_Hub/90_Inbox",
        "09_Obsidian_Hub/91_Attachments",
        "09_Obsidian_Hub/92_Templates",
        "09_Obsidian_Hub/99_System",
        ".obsidian",
    ]:
        (ROOT / relative).mkdir(parents=True, exist_ok=True)

    write(
        "09_Obsidian_Hub/00_HOME.md",
        note(
            "Career Knowledge Home",
            "dashboard",
            ["hub", "career", "navigation"],
            """
> [!important] System of record
> Start with the [[01_Source_Evidence/00_Verified_Profile/VERIFIED_FACT_SHEET|Verified Fact Sheet]]. It controls what may be claimed in applications. This vault is a navigation and summary layer; source evidence remains authoritative.

## Today

- **Profile status:** approximately one year of candidate-confirmed post-internship HR Operations at myTVS; signed employer confirmation is still pending.
- **Primary positioning:** HR Operations, People Operations, HR Coordinator, and operations-heavy early-career roles.
- **Current application state:** no submission should be recorded without a confirmation page or email.
- **Time-sensitive material:** remote vacancies were last checked on 31 July 2026 and must be rechecked before use.

## Main workspaces

Open [[09_Obsidian_Hub/Career_Map.canvas|Visual Career Map]] for a one-screen overview of how the hubs connect.

| Area | Open | Use it for |
|---|---|---|
| Profile and evidence | [[09_Obsidian_Hub/01_Profile/00_Profile_Hub|Profile Hub]] | Verified facts, timeline, learning and evidence gaps |
| Career direction | [[09_Obsidian_Hub/02_Career_Strategy/00_Career_Strategy_Hub|Career Strategy Hub]] | Roles, countries, international routes and priorities |
| Applications | [[09_Obsidian_Hub/03_Applications/00_Application_Command_Center|Application Command Center]] | CV selection, job status, answers and submission blockers |
| myTVS employment | [[09_Obsidian_Hub/04_Employment/00_Employment_Hub|Employment Hub]] | Exit documents, signatures and verification gaps |
| Portfolio and AI | [[09_Obsidian_Hub/05_Portfolio_and_AI/00_Portfolio_and_AI_Hub|Portfolio & AI Hub]] | AI evidence and the synthetic analytics project |
| Conversation record | [[09_Obsidian_Hub/06_Conversation_Summaries/00_Conversation_Hub|Conversation Hub]] | Decisions, previous questions and reusable responses |
| Files | [[09_Obsidian_Hub/07_File_Maps/00_File_System_Map|File System Map]] | Find any source file by purpose or folder |

## Fast actions

- Apply for a role: [[09_Obsidian_Hub/03_Applications/01_CV_Selection_Guide|choose the correct CV]] → [[09_Obsidian_Hub/03_Applications/02_Active_Remote_Jobs|check role status]] → [[04_Application_Toolkit/01_Per_Application_Checklist.html|run the checklist]] → record it in [[04_Application_Toolkit/07_Application_Tracker.csv|the tracker]].
- Add a new fact: use [[09_Obsidian_Hub/92_Templates/New_Evidence_Record|New Evidence Record]] and update the claim register before changing any CV.
- Prepare the exit: open [[09_Obsidian_Hub/04_Employment/01_myTVS_Exit_Checklist|myTVS Exit Checklist]].
- Find anything: open [[09_Obsidian_Hub/07_File_Maps/09_Full_File_Catalog|Full File Catalog]] or press `Cmd+Shift+F`.

## Reliability legend

- **Verified / Grade A:** supported by official records or certificates.
- **Candidate-confirmed / Grade B:** usable only with cautious wording; independent evidence is still needed.
- **Excluded / Grade C:** do not use until evidence is added.
- **Date-sensitive:** recheck the official source before acting.
""",
            aliases=["Home", "Dashboard", "Career Hub"],
        ),
    )

    write(
        "09_Obsidian_Hub/01_Profile/00_Profile_Hub.md",
        note(
            "Profile Hub",
            "hub",
            ["hub", "profile", "evidence"],
            """
## Essential references

- [[09_Obsidian_Hub/01_Profile/01_Profile_Snapshot|Profile Snapshot]] — concise current profile.
- [[09_Obsidian_Hub/01_Profile/02_Experience_Timeline|Experience Timeline]] — dated education and work history.
- [[09_Obsidian_Hub/01_Profile/03_Education_and_Learning|Education & Learning]] — degrees, scores and safe wording.
- [[09_Obsidian_Hub/01_Profile/04_Evidence_Gaps_and_Excluded_Claims|Evidence Gaps & Excluded Claims]] — facts that must not be overstated.
- [[01_Source_Evidence/00_Verified_Profile/VERIFIED_FACT_SHEET|Verified Fact Sheet]] — controlling narrative source.
- [[01_Source_Evidence/00_Verified_Profile/CLAIM_EVIDENCE_REGISTER.csv|Claim Evidence Register]] — claim-by-claim decision log.

> [!warning] Current employment evidence
> The post-internship myTVS role is candidate-confirmed, not yet independently established by signed company records. Use the exact conservative wording in the fact sheet.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/01_Profile/01_Profile_Snapshot.md",
        note(
            "Profile Snapshot",
            "profile",
            ["profile", "evidence", "current"],
            """
## Identity

- **Name:** Mohammad Azimuddin
- **Location:** Aligarh, Uttar Pradesh, India
- **LinkedIn:** <https://www.linkedin.com/in/md-azimuddin-34b088174>

## Professional summary

Early-career HR Operations professional with approximately one year of candidate-confirmed post-internship experience supporting routine HR administration for a small organisation of about 70 employees. Safe strengths are employee communication, management follow-up, documentation, confidentiality, independent prioritisation and follow-through. The strongest target roles are HR Operations, People Operations, HR Coordinator and administration-heavy operations roles.

## Education

- Master of Human Resource Management (MHRM), Aligarh Muslim University, 2024–2026 — completion/final result must not be claimed until documented.
- B.A. Economics, Aligarh Muslim University, 2021–2024 — CGPA 7.4/10.

## Safe digital skills

- Microsoft Excel, Word and PowerPoint.
- Introductory Power BI workshop exposure.
- Hands-on use of Claude, ChatGPT Codex and Visual Studio Code for research, drafting, information organisation and output review.

## Current goals

- Build a well-paid early-career role outside India, with Australia, the UK and Europe as preferred long-term destinations.
- Consider legitimate remote work and employer-sponsored international routes.
- Remain flexible about job function while preserving truthful applications and realistic eligibility.

## Controlling links

- [[01_Source_Evidence/00_Verified_Profile/VERIFIED_FACT_SHEET|Verified facts]]
- [[01_Source_Evidence/00_Verified_Profile/CLAIM_EVIDENCE_REGISTER.csv|Evidence register]]
- [[09_Obsidian_Hub/04_Employment/01_myTVS_Exit_Checklist|myTVS evidence plan]]
""",
        ),
    )

    write(
        "09_Obsidian_Hub/01_Profile/02_Experience_Timeline.md",
        note(
            "Experience Timeline",
            "timeline",
            ["profile", "experience", "timeline"],
            """
| Period | Activity | Evidence status | Safe description |
|---|---|---|---|
| 2021–2024 | B.A. Economics, AMU | Verified | Graduated with CGPA 7.4/10 |
| Mar–Apr 2023 | Filmsaaz 2023 intern | Verified | Selected as an intern for the 13th Filmsaaz festival |
| Aug–Oct 2024 | SURE Program consultant | Verified | Participated in a 12-week AMU–University of Houston programme and learned the business-plan preparation process |
| 2024–2026 | MHRM, AMU | Programme/dates verified; final completion not documented | State that the programme is being pursued or give dates without claiming issue of the final degree |
| 26 May–16 Jul 2025 | HR Intern, TVS Automobile Solutions Pvt. Ltd. | Verified | Exposure to recruitment and selection, employee engagement, performance evaluation and HR documentation |
| Jul 2025–present | HR Operations, myTVS | Candidate-confirmed; signed proof pending | Routine HR administration, employee communication, management follow-up, documentation, confidentiality and independent prioritisation for about 70 employees |

## Important distinction

The internship certificate uses `TVS Automobile Solutions Pvt. Ltd.` while the candidate identifies the subsequent small employer as `myTVS`. Signed separation and service documents must resolve the exact legal/trading name, designation, dates and employment type before background verification.

See [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/README|exit-document instructions]].
""",
        ),
    )

    write(
        "09_Obsidian_Hub/01_Profile/03_Education_and_Learning.md",
        note(
            "Education and Learning",
            "reference",
            ["profile", "education", "certifications"],
            """
## Degrees

| Programme | Institution | Result/status | Application wording |
|---|---|---|---|
| Master of Human Resource Management | Aligarh Muslim University | 2024–2026; final result not documented | `MHRM, Aligarh Muslim University, 2024–2026` or `pursuing an MHRM` |
| B.A. Economics | Aligarh Muslim University | CGPA 7.4/10, 2021–2024 | May be stated exactly |

## Selected learning

- Performance Management System — IIM Bangalore / SWAYAM, 90.4%, 2024.
- HR Analytics Using Excel — Dayananda Sagar Institutions / SWAYAM, 78.8%, 2024.
- Human Resources Analytics — University of California, Irvine, 2023.
- VITARA-HRMx — IMF/edX.
- Three-day AI-Enhanced Power BI workshop — AMU, October 2024.

## Application-ready four-sentence answer

> I earned a Bachelor of Arts in Economics from Aligarh Muslim University with a CGPA of 7.4/10. I am also pursuing a Master of Human Resource Management at the same university (2024–2026), with the final result not yet issued. My additional academic achievements include scoring 90.4% in IIM Bangalore's Performance Management course and 78.8% in HR Analytics Using Excel. I have not claimed any formal university honors or awards because none are currently documented in my records.

""",
        ),
    )

    write(
        "09_Obsidian_Hub/01_Profile/04_Evidence_Gaps_and_Excluded_Claims.md",
        note(
            "Evidence Gaps and Excluded Claims",
            "control",
            ["evidence", "risk", "claims"],
            """
## Pending primary evidence

- Exact registered/trading employer name for current myTVS employment.
- Exact post-internship start date, designation, department and employment type.
- Salary, cash-payment history, last working day and notice period.
- Manager-verified responsibilities and achievements.
- MHRM completion/final result.
- Language proficiency, nationality, passport, visa and work-authorisation details.

## Do not claim without new evidence

- MBA title; the programme is MHRM.
- SHRM-CP candidate or scheduled-exam status.
- Advanced Excel, advanced Power BI, Power Query, predictive analytics or coding proficiency.
- HRIS, payroll, ATS, CRM, compliance, onboarding, KPI, benefits or compensation ownership.
- SQL, Python, Tableau, BigQuery, Looker, Zendesk or comparable platforms.
- Professional AI employment, prompt-engineering expertise, workflow automation or software engineering.
- Invented metrics, percentages, salary premiums or guaranteed outcomes.
- Religion, marital status, Arabic ability, visa status or driving-licence conversion.

## Update rule

Add evidence to `01_Source_Evidence`, update [[01_Source_Evidence/00_Verified_Profile/CLAIM_EVIDENCE_REGISTER.csv|the claim register]], then update the fact sheet and regenerate every affected CV. Never introduce a new claim in only one resume.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/02_Career_Strategy/00_Career_Strategy_Hub.md",
        note(
            "Career Strategy Hub",
            "hub",
            ["hub", "career-strategy", "international"],
            """
- [[09_Obsidian_Hub/02_Career_Strategy/01_Role_Strategy|Role Strategy]]
- [[09_Obsidian_Hub/02_Career_Strategy/02_Country_and_Mobility_Strategy|Country & Mobility Strategy]]
- [[09_Obsidian_Hub/02_Career_Strategy/03_Action_Plan|Career Action Plan]]
- [[03_Career_Research/README|Evidence-controlled research library]]

> [!note] Strategy versus evidence
> Country and job-market guidance changes. Treat research as decision support, not as proof of eligibility, salary or visa entitlement.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/02_Career_Strategy/01_Role_Strategy.md",
        note(
            "Role Strategy",
            "strategy",
            ["career-strategy", "roles", "hr"],
            """
## Priority order

1. **HR Operations / People Operations / HR Coordinator** — best match to current evidence.
2. **Operations Associate / administrative coordination** — strong transferable documentation and follow-through fit.
3. **Graduate customer success or sales development** — possible stretch where employers accept transferable communication and learning ability.
4. **Business/management AI evaluation** — academic fit; usually contractor work with uncertain hours.
5. **Economics/investment AI evaluation** — possible only with strong preparation in investment fundamentals.
6. **HR or junior data analytics** — pursue after independently reproducing the portfolio and gaining evidenced SQL/Excel/Power BI capability.

## HR versus economics conclusion

HR is the stronger immediate employment profile because it combines an MHRM, a verified HR internship and candidate-confirmed HR Operations experience. Economics remains valuable as a supporting analytical foundation and a secondary route into business research, AI evaluation and later analytics roles.

## Roles currently too weak to claim directly

- Payroll, rewards, compensation design, HRIS administration or HR compliance ownership.
- Data analyst roles requiring SQL, Python and Tableau from day one.
- SaaS helpdesk roles requiring one year of written customer support.
- SEO/link-building roles requiring placements, publisher relationships and specialist tools.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/02_Career_Strategy/02_Country_and_Mobility_Strategy.md",
        note(
            "Country and Mobility Strategy",
            "strategy",
            ["career-strategy", "countries", "mobility"],
            """
## Stated preference

The long-term goal is employment in Australia, the UK or Europe, and the candidate is open to jobs outside the core HR profile, including lower-paid entry routes when lawful and realistic.

## Practical interpretation

- **Australia:** usually requires a lawful work-right route first; direct overseas sponsorship for a fresher or generic minimum-wage role is difficult. Education, skilled migration or later employer sponsorship may be more realistic after stronger experience and English evidence.
- **United Kingdom:** entry-level sponsorship is limited and employers must meet sponsorship and salary rules. Minimum-wage willingness does not by itself create visa eligibility.
- **Europe:** requirements vary by country; English-speaking roles are competitive and local-language ability often matters. Target employers that explicitly sponsor or hire internationally.
- **UAE:** easier geographic access than Western markets but a tourist-visa job search carries financial and legal risk. Verified experience and applying from India first are safer.
- **Remote work:** a useful income and experience route, but country eligibility, contractor status and payment reliability must be verified.

## IELTS

IELTS can prove English proficiency for education, migration or employers that request it; it does not itself create work authorisation or guarantee a job. Prepare for the specific Academic or General Training test required by the intended route.

## Before spending money

Recheck official immigration rules, employer sponsorship status, role eligibility, total relocation costs and refund policies. Use the dated country research in [[03_Career_Research/02_Country_Strategy/Country_Selection_Analysis.pdf|Country Selection Analysis]] as background only.
""",
            status="date-sensitive",
        ),
    )

    write(
        "09_Obsidian_Hub/02_Career_Strategy/03_Action_Plan.md",
        note(
            "Career Action Plan",
            "plan",
            ["career-strategy", "action-plan"],
            """
## Immediate — documentation

- [ ] Complete and secure signed myTVS exit and service documents.
- [ ] Add documentary proof of MHRM completion when available.
- [ ] Confirm languages, nationality, work rights, notice period and earliest start date.
- [ ] Keep evidence scans and application files backed up.

## Next 30 days — applications

- [ ] Recheck every remote vacancy before using its CV.
- [ ] Apply first to HR Operations, People Operations and coordination roles that accept India-based applicants.
- [ ] Record every submission in [[04_Application_Toolkit/07_Application_Tracker.csv|Application Tracker]].
- [ ] Save the exact submitted CV with employer and date in the filename.
- [ ] Build direct employer/referral applications before mass cold outreach.

## Next 60–90 days — employability

- [ ] Reproduce and explain the synthetic HR analytics project independently.
- [ ] Build evidenced Excel and Power BI work samples; add SQL only after practical projects.
- [ ] Create a small public portfolio or GitHub repository only after reviewing all content.
- [ ] Prepare interview stories using Situation–Task–Action–Result without inventing metrics.
- [ ] Research one concrete lawful route for Australia, the UK or a selected European country.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/03_Applications/00_Application_Command_Center.md",
        note(
            "Application Command Center",
            "dashboard",
            ["hub", "applications", "jobs"],
            """
> [!warning] Current status
> No application is considered submitted without a confirmation page or email. The latest remote-job research was checked on 31 July 2026 and is now date-sensitive.

## Apply in this order

1. [[09_Obsidian_Hub/03_Applications/02_Active_Remote_Jobs|Check whether the role is still open and eligible]].
2. [[09_Obsidian_Hub/03_Applications/01_CV_Selection_Guide|Choose the exact matching CV]].
3. Open the role's `APPLICATION_NOTES.md` and resolve every warning.
4. Run [[04_Application_Toolkit/01_Per_Application_Checklist.html|the per-application checklist]].
5. Submit through the official employer platform.
6. Record the confirmation in [[04_Application_Toolkit/07_Application_Tracker.csv|the tracker]].

## Current resources

- [[07_Remote_Job_Applications/2026-07-31_High_Paying_Early_Career/README|Latest 12-role pack]]
- [[07_Remote_Job_Applications/2026-07-31_High_Paying_Early_Career/APPLICATION_SUBMISSION_STATUS_2026-07-31|Submission blockers]]
- [[07_Remote_Job_Applications/2026-07-31_High_Paying_Early_Career/00_Target_Job_Matrix.csv|Target matrix]]
- [[05_Ready_to_Use_Application_Pack/README|General UAE and India application pack]]
- [[09_Obsidian_Hub/06_Conversation_Summaries/03_Reusable_Application_Answers|Reusable answer drafts]]

## Non-negotiable controls

- Never use one employer's targeted CV for another employer.
- Never answer `Yes` to an unsupported skill or experience requirement.
- Canonical narrative answers must be written by the candidate without AI-generated wording.
- Do not submit expired or location-ineligible vacancies.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/03_Applications/01_CV_Selection_Guide.md",
        note(
            "CV Selection Guide",
            "guide",
            ["applications", "cv", "ats"],
            """
| Situation | Use |
|---|---|
| Exact employer appears in a dated remote pack | Use only that employer-and-role PDF from its ready folder |
| UAE HR Coordinator | [[05_Ready_to_Use_Application_Pack/01_Mohammad_Azimuddin_UAE_HR_Coordinator.pdf|UAE HR Coordinator CV]] |
| General UAE HR Operations | [[05_Ready_to_Use_Application_Pack/02_Mohammad_Azimuddin_UAE_HR_General.pdf|UAE General HR CV]] |
| General India HR | [[05_Ready_to_Use_Application_Pack/03_Mohammad_Azimuddin_India_HR_General.pdf|India General HR CV]] |
| Analytics role | Use the HR Analyst CV only after reproducing the portfolio and meeting the job's actual technical requirements |
| Saudi role | Use the Saudi CV only when the vacancy explicitly accepts international applicants |

## Filename rule

`Mohammad_Azimuddin_[Market]_[Role]_[Employer]_[YYYY-MM-DD].pdf`

## Before upload

- Confirm title and dates match signed myTVS documents.
- Recheck contact details, role name, employer name and country eligibility.
- Confirm one A4 page, selectable text and no unsupported claims.
- Keep the submitted copy unchanged for future reference.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/03_Applications/02_Active_Remote_Jobs.md",
        note(
            "Active Remote Jobs",
            "job-index",
            ["applications", "remote-jobs", "date-sensitive"],
            """
> [!danger] Recheck required
> The table reflects research completed on 31 July 2026, not a guarantee that a vacancy remains open on 5 August 2026. Open the official page immediately before applying.

""" + current_job_table() + """

## Category meaning

- `priority` — CV prepared and fit considered worth applying, subject to a fresh vacancy/eligibility check.
- `conditional` — resolve the documented skill, experience or country condition first.
- `expired` — retain for reference only; do not submit to the closed listing.
""",
            status="date-sensitive",
        ),
    )

    write(
        "09_Obsidian_Hub/03_Applications/03_Submission_Blockers.md",
        note(
            "Submission Blockers",
            "control",
            ["applications", "blockers", "privacy"],
            """
## Candidate information still required

- Exact legal first and last name split.
- Nationality and work authorisation.
- Voluntary demographic selections or `Prefer not to say`.
- Verified language proficiency.
- High-school mathematics and native-language marks/relative standing.
- International-travel willingness and visa/vaccination constraints.
- Contractor acceptance, equipment/internet and minimum hourly rate.
- Notice period and earliest start date.

## Technical blockers

- Interactive browser control is required for uploads, account sign-in, CAPTCHA and final submission.
- Confirmation pages or emails must be retained.
- Never share passwords, OTPs, bank information or identity-document numbers in chat.

## Employer-specific blockers

- Canonical requires candidate-authored answers and rejects AI-generated content.
- Jobgether requires one year of written support experience, currently not evidenced.
- Superwork lists an unsupported SQL/Python/Tableau stack.
- Prox and Allara require confirmation that India is eligible.
- Anchorial's researched listing expired.

Full source: [[07_Remote_Job_Applications/2026-07-31_High_Paying_Early_Career/APPLICATION_SUBMISSION_STATUS_2026-07-31|Application Submission Status]].
""",
        ),
    )

    write(
        "09_Obsidian_Hub/04_Employment/00_Employment_Hub.md",
        note(
            "Employment Hub",
            "hub",
            ["hub", "employment", "mytvs"],
            """
- [[09_Obsidian_Hub/04_Employment/01_myTVS_Exit_Checklist|myTVS Exit Checklist]]
- [[09_Obsidian_Hub/04_Employment/02_Employment_Evidence_Status|Employment Evidence Status]]
- [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/README|Exit-pack instructions]]
- [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/DOCUMENT_COMPLETION_CHECKLIST.csv|Document completion tracker]]

> [!important]
> Because Mohammad has been acting in HR, an independent manager or authorised signatory must verify and issue his employment documents. Drafts are not company records until reviewed, dated and signed.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/04_Employment/01_myTVS_Exit_Checklist.md",
        note(
            "myTVS Exit Checklist",
            "checklist",
            ["employment", "mytvs", "exit-documents"],
            """
## Complete first

- [ ] [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/00_Field_Completion_and_Verification_Sheet.docx|Field Completion & Verification Sheet]]
- [ ] Confirm legal/trading employer name, employee ID, designation, department and employment type.
- [ ] Confirm exact start date, resignation date, notice requirement and accepted last working day.
- [ ] Reconcile month-wise cash salary against attendance/wage records and actual payment dates.
- [ ] Identify the reporting manager, authorised signatory and background-verification contact.

## Issue in sequence

1. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/01_Resignation_Letter.docx|Resignation Letter]]
2. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/02_Resignation_Acceptance_and_Last_Working_Day.docx|Acceptance & Last Working Day]]
3. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/03_Post_Internship_Employment_Status_Confirmation.docx|Employment Status Confirmation]]
4. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/09_Handover_and_No_Dues_Record.docx|Handover & No Dues]]
5. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/08_Full_and_Final_Settlement_Statement.docx|Full & Final Settlement]]
6. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/04_Experience_and_Service_Certificate.docx|Experience & Service Certificate]]
7. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/05_Relieving_Letter.docx|Relieving Letter]]
8. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/06_Employment_Salary_and_Cash_Payment_Certificate.docx|Salary & Cash Payment Certificate]]
9. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/10_Manager_Recommendation_and_Reference.docx|Manager Recommendation]]
10. [[08_Employment_Exit_Documents/MyTVS_Exit_Pack_2026/11_Separation_Documents_Issuance_and_Receipt.docx|Issuance & Receipt Record]]

## Safeguards

- Do not sign blank documents or acknowledge money before receipt.
- Do not backdate documents or invent wage records.
- Use actual issue dates, approved letterhead and an authorised signature.
- Retain colour scans and the transmitting email for every final document.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/04_Employment/02_Employment_Evidence_Status.md",
        note(
            "Employment Evidence Status",
            "evidence-status",
            ["employment", "evidence", "verification"],
            """
| Claim | Current status | Next evidence |
|---|---|---|
| HR internship, 26 May–16 Jul 2025 | Verified by certificate | Preserve original certificate |
| Post-internship HR Operations from Jul 2025 | Candidate-confirmed | Signed status confirmation and experience certificate |
| Approximately 70 employees | Candidate-confirmed context | Manager confirmation if used in background verification |
| Routine administration, communication, follow-up and documentation | Candidate-confirmed safe duties | Signed responsibilities or manager reference |
| Cash salary | Candidate-confirmed | Wage register, attendance, receipts and signed salary certificate |
| Exact designation/employment type | Unverified | Approved company record |
| Last working day | Not fixed in evidence | Resignation acceptance and relieving letter |

The signed documents must reconcile the current-employer name `myTVS` with the internship certificate's `TVS Automobile Solutions Pvt. Ltd.` wording.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/05_Portfolio_and_AI/00_Portfolio_and_AI_Hub.md",
        note(
            "Portfolio and AI Hub",
            "hub",
            ["hub", "portfolio", "ai"],
            """
- [[09_Obsidian_Hub/05_Portfolio_and_AI/01_AI_Capability_Evidence|AI Capability Evidence]]
- [[09_Obsidian_Hub/05_Portfolio_and_AI/02_HR_Analytics_Project|HR Analytics Project]]
- [[06_Portfolio_Projects/README|Portfolio source folder]]

The safe positioning is practical tool use for research, drafting, information organisation and output review—not professional AI employment, software engineering or expert prompt engineering.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/05_Portfolio_and_AI/01_AI_Capability_Evidence.md",
        note(
            "AI Capability Evidence",
            "portfolio-note",
            ["ai", "skills", "portfolio"],
            """
## Verified-safe wording

`Hands-on use of Claude, ChatGPT Codex, and Visual Studio Code for research, drafting, information organisation, and output review.`

## Strongest current AI-assisted work product

An evidence-controlled career application system that:

- Organises academic, certification and employment records into a verified fact sheet.
- Separates verified, candidate-confirmed and excluded claims.
- Maintains employer-specific CVs, application notes, status controls and QA reports.
- Checks PDFs for A4 page size, text extraction, embedded fonts and unsupported keywords.
- Preserves archived versions instead of silently overwriting submitted or retired documents.

Tools used: Claude, ChatGPT Codex and VS Code. The value is not merely generating text; it is creating an auditable workflow that reduces fabricated claims and makes future applications faster to prepare and verify.

## Boundaries

Do not describe this as professional AI training, autonomous workflow development, prompt-engineering expertise or software-engineering employment unless further evidence and independent capability are demonstrated.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/05_Portfolio_and_AI/02_HR_Analytics_Project.md",
        note(
            "HR Analytics Project",
            "portfolio-note",
            ["portfolio", "hr-analytics", "power-bi"],
            """
## Project

The workspace contains a descriptive HR analytics project using 120 synthetic employee records. It includes a privacy-safe CSV, dashboard, data dictionary, methodology, limitations and suggested Power BI measures.

## Open the files

- [[06_Portfolio_Projects/01_Synthetic_HR_Analytics_Dashboard/README|Project README]]
- [[06_Portfolio_Projects/01_Synthetic_HR_Analytics_Dashboard/dashboard.html|Dashboard]]
- [[06_Portfolio_Projects/01_Synthetic_HR_Analytics_Dashboard/synthetic_hr_data.csv|Dataset]]
- [[06_Portfolio_Projects/01_Synthetic_HR_Analytics_Dashboard/DATA_DICTIONARY|Data dictionary]]
- [[06_Portfolio_Projects/01_Synthetic_HR_Analytics_Dashboard/ANALYSIS_NOTES|Analysis notes]]

> [!warning] Portfolio gate
> Do not cite this project in an application until you can independently reproduce its calculations, explain every measure and distinguish descriptive association from causation.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/06_Conversation_Summaries/00_Conversation_Hub.md",
        note(
            "Conversation Hub",
            "hub",
            ["hub", "conversation", "decisions"],
            """
- [[09_Obsidian_Hub/06_Conversation_Summaries/01_Master_Conversation_Summary|Master Conversation Summary]]
- [[09_Obsidian_Hub/06_Conversation_Summaries/02_Decision_Log|Decision Log]]
- [[09_Obsidian_Hub/06_Conversation_Summaries/03_Reusable_Application_Answers|Reusable Application Answers]]

This is a structured synthesis of the available conversation context and resulting files, not a verbatim chat export. When a conversation statement conflicts with source evidence, the Verified Fact Sheet wins.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/06_Conversation_Summaries/01_Master_Conversation_Summary.md",
        note(
            "Master Conversation Summary",
            "conversation-summary",
            ["conversation", "history", "career"],
            """
## 1. File analysis and correction

The career folder was deeply reviewed, reorganised into numbered sections and corrected to remove unsupported claims, outdated research, duplicate CVs and unreliable application records. A Verified Fact Sheet and Claim Evidence Register became the controlling sources. Earlier material was preserved in `99_Archive` rather than deleted.

## 2. International career exploration

The conversation examined India salary expectations, Dubai walk-in interviews, UAE experience requirements, UK and Australia eligibility, Europe, IELTS and minimum-wage willingness. The consistent conclusion was that willingness to accept low pay does not remove visa/work-authorisation barriers; verified experience, English evidence and employer sponsorship matter more. Australia, the UK and Europe remain preferred long-term destinations, while UAE and remote work were considered possible intermediate routes.

## 3. HR versus economics profile

HR Operations was selected as the strongest immediate profile because the MHRM, internship and candidate-confirmed myTVS experience align. Economics remains useful for analytical reasoning, business/management AI evaluation, investment-related preparation and possible future data roles. Technical data jobs remain conditional until practical SQL/Excel/Power BI evidence exists.

## 4. AI employability

The candidate reported hands-on experience with Claude, ChatGPT Codex and VS Code. The safe CV wording is limited to research, drafting, information organisation and output review. The most defensible AI-assisted work product is the evidence-controlled application system now contained in this workspace.

## 5. myTVS experience and exit

The candidate clarified that the current employer should be called myTVS, a small organisation of roughly 70 employees, and that post-internship HR Operations continued for approximately one year. Because wages were paid in cash and the candidate was handling HR, a complete exit-document pack was drafted for independent manager verification and signature. The exact employer name, designation, dates, salary and last working day remain evidence priorities.

## 6. Remote-job research and tailored CVs

Two dated remote-job packs were produced. The latest contains 12 role-specific CV packages: seven priority, four conditional and one expired at the last check. Each role has a PDF, HTML, TXT file and application notes, with separate QA and submission-control documents.

## 7. Attempted application submission

The user authorised applications to all researched jobs, but no application was recorded as submitted because interactive browser control, CAPTCHA handling and candidate-only declarations were unavailable. Canonical explicitly requires responses in the candidate's own words and disqualifies AI-generated narrative answers. Missing legal-name split, nationality, languages, school grades, travel consent, work rights, notice and contractor choices were documented.

## 8. Recent application-answer preparation

Drafts were prepared for education/results, evidence of ability, Everis motivation and an AI-project description. These are stored in [[09_Obsidian_Hub/06_Conversation_Summaries/03_Reusable_Application_Answers|Reusable Application Answers]] and must be reviewed for truth and employer-specific AI policies before use.

## Current unresolved items

- Signed myTVS experience and exit records.
- MHRM completion evidence.
- Personal application declarations and Canonical candidate-authored narratives.
- Fresh status checks for remote vacancies.
- Independent reproduction of the HR analytics portfolio.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/06_Conversation_Summaries/02_Decision_Log.md",
        note(
            "Decision Log",
            "decision-log",
            ["decisions", "history", "governance"],
            """
| Date | Decision | Reason |
|---|---|---|
| 27 Jul 2026 | Make the fact sheet and evidence register controlling | Prevent unsupported or inconsistent CV claims |
| 27 Jul 2026 | Archive old variants rather than delete them | Preserve provenance and recoverability |
| 30 Jul 2026 | Treat post-internship myTVS work as candidate-confirmed pending signatures | The candidate reported the work, but independent company evidence is outstanding |
| 30 Jul 2026 | Position HR Operations as the primary immediate domain | Strongest combination of study and early experience |
| 30 Jul 2026 | Require independent manager approval of the candidate's exit documents | The candidate should not be both preparer and company issuer |
| 31 Jul 2026 | Separate remote roles into priority, conditional and expired | Prevent blind applications to ineligible or closed roles |
| 31 Jul 2026 | Record no job as submitted without confirmation | Avoid false tracker history |
| 31 Jul 2026 | Do not generate Canonical candidate narratives for submission | Canonical prohibits AI-generated application answers |
| 5 Aug 2026 | Make the complete workspace the Obsidian vault | All source files remain searchable without duplication or relocation |
""",
        ),
    )

    write(
        "09_Obsidian_Hub/06_Conversation_Summaries/03_Reusable_Application_Answers.md",
        note(
            "Reusable Application Answers",
            "answer-bank",
            ["applications", "answers", "drafts"],
            """
> [!warning] Review before use
> These are evidence-controlled drafts, not universal answers. Adapt them to the exact form and do not paste them where an employer requires unaided candidate-authored wording. Canonical explicitly prohibits AI-generated answers.

## University study and results — four sentences

> I earned a Bachelor of Arts in Economics from Aligarh Muslim University with a CGPA of 7.4/10. I am also pursuing a Master of Human Resource Management at the same university (2024–2026), with the final result not yet issued. My additional academic achievements include scoring 90.4% in IIM Bangalore's Performance Management course and 78.8% in HR Analytics Using Excel. I have not claimed any formal university honors or awards because none are currently documented in my records.

## Evidence of ability

> My main achievement was progressing from an HR internship into an ongoing HR Operations role at myTVS, where I independently support routine HR administration, employee communication, management follow-ups, and confidential documentation for approximately 70 employees. Academically, I scored 90.4% in IIM Bangalore's Performance Management course and 78.8% in HR Analytics Using Excel. I also participated as a consultant in the 12-week SURE Program involving Aligarh Muslim University and the University of Houston, where I learned a structured approach to business-plan preparation and information analysis.

## Why Everis — four sentences

> I am applying because Everis's People Operations role closely matches my HR administration experience and offers an opportunity to contribute within a remote, international environment. At myTVS, I have supported routine HR operations for approximately 70 employees, including documentation, employee communication, confidential information handling, and management follow-ups. This experience has strengthened my ability to follow procedures, organise information accurately, prioritise recurring requirements independently, and complete actions reliably without constant supervision. My MHRM studies, Economics background, and careful use of digital and AI tools would also help me learn Everis's processes quickly and communicate effectively in a distributed team.

## Most impressive AI-assisted work

> The most impressive thing I have built with AI is an evidence-controlled career application system, although it is not publicly hosted yet. Using Claude, ChatGPT Codex, and VS Code, I organised scattered academic, certification, and employment records into a verified fact sheet, then produced 12 role-specific, ATS-friendly CV packages with application notes, job trackers, and quality checks. The unusual part was designing a verification process that separated documented facts from unverified claims and checked every PDF for one-page A4 formatting, text extraction, correct targeting, and unsupported keywords instead of simply asking AI for generic resumes. It was worth the effort because it gave me a reusable workflow that makes applications faster and more relevant without sacrificing accuracy or honesty.
""",
            status="draft",
        ),
    )

    write(
        "09_Obsidian_Hub/07_File_Maps/00_File_System_Map.md",
        note(
            "File System Map",
            "file-map",
            ["hub", "files", "navigation"],
            """
## Folder architecture

```text
00_START_HERE.md                         legacy root guide
01_Source_Evidence                       factual source of truth
02_CV_Library                            active market/role CV variants
03_Career_Research                       dated strategy and benchmark reports
04_Application_Toolkit                   checklists, templates, contacts, tracker
05_Ready_to_Use_Application_Pack         safest general-use PDFs
06_Portfolio_Projects                    reproducible work samples
07_Remote_Job_Applications               dated vacancy-specific application packs
08_Employment_Exit_Documents             myTVS separation drafts and controls
09_Obsidian_Hub                          navigation, summaries and templates
98_Maintenance                           generators and QA records
99_Archive                               retired and pre-correction material
```

## Open an index

- [[09_Obsidian_Hub/07_File_Maps/01_Source_Evidence_Index|Source Evidence]]
- [[09_Obsidian_Hub/07_File_Maps/02_CV_Library_Index|CV Library]]
- [[09_Obsidian_Hub/07_File_Maps/03_Career_Research_Index|Career Research]]
- [[09_Obsidian_Hub/07_File_Maps/04_Application_Toolkit_Index|Application Toolkit]]
- [[09_Obsidian_Hub/07_File_Maps/05_Portfolio_Index|Portfolio Projects]]
- [[09_Obsidian_Hub/07_File_Maps/06_Remote_Applications_Index|Remote Applications]]
- [[09_Obsidian_Hub/07_File_Maps/07_Exit_Documents_Index|Exit Documents]]
- [[09_Obsidian_Hub/07_File_Maps/08_Maintenance_and_Archive_Index|Maintenance & Archive]]
- [[09_Obsidian_Hub/07_File_Maps/09_Full_File_Catalog|Full File Catalog]]

## Search shortcuts

- `Cmd+O` — quick-open a note or file by name.
- `Cmd+Shift+F` — search the full vault.
- Search `path:01_Source_Evidence` for evidence only.
- Search `path:07_Remote_Job_Applications APPLICATION_NOTES` for role notes.
- Search `path:99_Archive` only when tracing older versions.
- Search `tag:#applications` or `tag:#evidence` for hub notes.
""",
        ),
    )

    index_specs = [
        ("01_Source_Evidence_Index", "Source Evidence Index", "01_Source_Evidence", "Primary and secondary records controlling factual claims."),
        ("02_CV_Library_Index", "CV Library Index", "02_CV_Library", "Active country- and role-specific CV source/PDF pairs."),
        ("03_Career_Research_Index", "Career Research Index", "03_Career_Research", "Dated role, country, CV-benchmark and certification research."),
        ("04_Application_Toolkit_Index", "Application Toolkit Index", "04_Application_Toolkit", "Checklists, templates, contact research and the application tracker."),
        ("05_Portfolio_Index", "Portfolio Index", "06_Portfolio_Projects", "Portfolio projects that require independent reproduction before application use."),
        ("06_Remote_Applications_Index", "Remote Applications Index", "07_Remote_Job_Applications", "Dated company-specific application packs; newest does not automatically mean still open."),
        ("07_Exit_Documents_Index", "Exit Documents Index", "08_Employment_Exit_Documents", "Editable myTVS separation drafts and their QA/control files."),
    ]
    for filename, title, section, intro in index_specs:
        write(
            f"09_Obsidian_Hub/07_File_Maps/{filename}.md",
            note(title, "file-index", ["files", "index", section.lower()], directory_listing(section, intro)),
        )

    maintenance_body = directory_listing("98_Maintenance", "Generators and QA records. Run only after reviewing their documented scope.")
    maintenance_body += "\n\n---\n\n" + directory_listing("99_Archive", "Retired and pre-correction material. Do not use for new applications.")
    write(
        "09_Obsidian_Hub/07_File_Maps/08_Maintenance_and_Archive_Index.md",
        note("Maintenance and Archive Index", "file-index", ["files", "maintenance", "archive"], maintenance_body),
    )
    write(
        "09_Obsidian_Hub/07_File_Maps/09_Full_File_Catalog.md",
        note("Full File Catalog", "file-catalog", ["files", "catalog", "search"], full_catalog()),
    )

    write(
        "09_Obsidian_Hub/92_Templates/New_Job_Application.md",
        """---
type: job-application
status: researching
company:
role:
location:
work_mode:
source_url:
date_found: {{date}}
date_checked: {{date}}
deadline:
cv_used:
tags: [applications, job]
---

# {{title}}

## Eligibility

- [ ] Location/country eligible
- [ ] Work authorisation or sponsorship understood
- [ ] Mandatory experience met truthfully
- [ ] Mandatory tools met truthfully

## Evidence match

**Strong matches:**

**Gaps:**

**Claims requiring proof:**

## Submission

- [ ] Tailored CV selected
- [ ] Application answers reviewed
- [ ] Submitted
- [ ] Confirmation saved
- [ ] Tracker updated

## Follow-up

- Submission date:
- Confirmation/reference:
- Follow-up date:
- Outcome:
""",
    )
    write(
        "09_Obsidian_Hub/92_Templates/New_Evidence_Record.md",
        """---
type: evidence-record
status: unreviewed
date_added: {{date}}
claim:
evidence_grade:
source_file:
tags: [evidence, review-needed]
---

# {{title}}

## Proposed claim

## Exact source wording

## What the evidence supports

## What it does not support

## Approved application wording

## Required updates

- [ ] Source file stored in `01_Source_Evidence`
- [ ] Claim Evidence Register updated
- [ ] Verified Fact Sheet updated
- [ ] Affected CVs regenerated and checked
""",
    )
    write(
        "09_Obsidian_Hub/92_Templates/Conversation_Summary.md",
        """---
type: conversation-summary
status: current
date: {{date}}
tags: [conversation, decisions]
---

# {{title}}

## User objective

## Facts confirmed

## Decisions made

## Files created or changed

## Open questions

## Next actions
""",
    )
    write("09_Obsidian_Hub/90_Inbox/README.md", "# Inbox\n\nCapture new notes here, then move them to the correct hub after review.\n")
    write("09_Obsidian_Hub/91_Attachments/README.md", "# Attachments\n\nNew Obsidian note attachments are stored here. Primary evidence must be moved to `01_Source_Evidence` and registered before use.\n")

    write(
        "09_Obsidian_Hub/99_System/Vault_Guide.md",
        note(
            "Vault Guide",
            "system-guide",
            ["obsidian", "system", "navigation"],
            """
## Scope

The vault root is resolved from the generator location. The hub is the curated navigation layer; numbered folders retain their local workflow roles without embedding a machine-specific workspace name.

## Naming

- Numbered folders define workflow order.
- Hub notes start with `00`.
- Dated job packs use `YYYY-MM-DD`.
- Submitted CVs must include market, role, employer and submission date.
- Use the Inbox only for uncategorised notes.

## Updating the vault

Run `python3 98_Maintenance/build_obsidian_career_vault.py` after adding, moving or renaming source files. The script refreshes generated indexes and the full catalog; it does not move or delete source evidence.

## Obsidian use

- Quick Switcher: `Cmd+O`
- Command Palette: `Cmd+P`
- Global Search: `Cmd+Shift+F`
- Backlinks reveal which summaries reference a source.
- Tags classify the curated notes; folder paths classify the source files.
""",
        ),
    )
    write(
        "09_Obsidian_Hub/99_System/Change_Log.md",
        note(
            "Vault Change Log",
            "change-log",
            ["obsidian", "changes", "system"],
            """
## 5 August 2026

- Made the existing career workspace the Obsidian vault without moving source files.
- Added the `09_Obsidian_Hub` dashboard and functional hubs.
- Added verified-profile, strategy, application, employment, AI and conversation summaries.
- Added per-section indexes and a generated full file catalog.
- Added job, evidence and conversation templates.
- Configured core Obsidian navigation, templates and attachment locations.
- Registered the career workspace as a new Obsidian vault and opened its dashboard.
- Backed up the previous Obsidian vault registry under `99_Archive/02_System_Metadata`.
- Preserved all existing source, archive and user-named files.
""",
        ),
    )

    write(
        "09_Obsidian_Hub/README.md",
        """# Obsidian Career Hub

Open [[09_Obsidian_Hub/00_HOME|Career Knowledge Home]].
For a visual overview, open [[09_Obsidian_Hub/Career_Map.canvas|Career Map]].

This folder is the curated navigation and summary layer for the complete career workspace. The workspace root is the Obsidian vault so all existing PDFs, images, Word files, CSVs, HTML documents and Markdown notes remain searchable without duplication.
""",
    )

    obsidian = ROOT / ".obsidian"
    (obsidian / "snippets").mkdir(parents=True, exist_ok=True)
    (obsidian / "app.json").write_text(
        json.dumps(
            {
                "alwaysUpdateLinks": True,
                "attachmentFolderPath": "09_Obsidian_Hub/91_Attachments",
                "newFileLocation": "folder",
                "newFileFolderPath": "09_Obsidian_Hub/90_Inbox",
                "showUnsupportedFiles": True,
                "showInlineTitle": True,
                "useMarkdownLinks": False,
                "userIgnoreFilters": ["99_Archive/03_Pre_Correction_Snapshot_2026-07-27/", "~$", ".DS_Store"],
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    (obsidian / "core-plugins.json").write_text(
        json.dumps(
            {
                "file-explorer": True,
                "global-search": True,
                "switcher": True,
                "graph": True,
                "backlink": True,
                "outgoing-link": True,
                "tag-pane": True,
                "properties": True,
                "page-preview": True,
                "templates": True,
                "note-composer": True,
                "command-palette": True,
                "bookmarks": True,
                "outline": True,
                "word-count": True,
                "file-recovery": True,
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    (obsidian / "templates.json").write_text(
        json.dumps({"folder": "09_Obsidian_Hub/92_Templates"}, indent=2) + "\n",
        encoding="utf-8",
    )
    (obsidian / "appearance.json").write_text(
        json.dumps({"baseFontSize": 16, "showViewHeader": True, "enabledCssSnippets": ["career-vault"]}, indent=2) + "\n",
        encoding="utf-8",
    )
    (obsidian / "snippets" / "career-vault.css").write_text(
        """/* Small readability improvements for the career dashboard. */
.workspace-leaf-content[data-type="markdown"] .markdown-preview-view h1 { color: var(--color-accent); }
.markdown-rendered table { width: 100%; }
.markdown-rendered .callout[data-callout="important"] { --callout-color: 35, 98, 150; }
""",
        encoding="utf-8",
    )

    print(f"Built Obsidian career vault at {ROOT}")
    print(f"Dashboard: {HUB / '00_HOME.md'}")


if __name__ == "__main__":
    main()
