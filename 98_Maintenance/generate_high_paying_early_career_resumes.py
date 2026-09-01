#!/usr/bin/env python3
"""Generate evidence-controlled CV packages for the 31 July 2026 remote-job shortlist."""

from __future__ import annotations

import copy
import csv
import importlib.util
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_SOURCE = ROOT / "98_Maintenance" / "generate_remote_targeted_resumes.py"
OUT = ROOT / "07_Remote_Job_Applications" / "2026-07-31_High_Paying_Early_Career"


def load_base():
    spec = importlib.util.spec_from_file_location("base_remote_resumes", BASE_SOURCE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {BASE_SOURCE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_base()
CONTACT = BASE.CONTACT
MYTVS_HR_OPS = BASE.MYTVS_HR_OPS
SURE = BASE.SURE
EDUCATION = BASE.EDUCATION
LEARNING = BASE.LEARNING
ORACLE_BADGE_URL = BASE.ORACLE_BADGE_URL
AI_TOOLS = BASE.AI_TOOLS

PDF_FORMAT = (
    "Submit the one-page, text-extractable PDF. Retain the TXT copy for manual application "
    "fields and the HTML copy only as a reference."
)
GREENHOUSE_FORMAT = (
    "Greenhouse accepts PDF and common document formats. Submit the one-page PDF and recheck "
    "the generated preview before completing the application."
)


def existing_job(company: str, role: str) -> dict:
    for job in BASE.JOBS:
        if job["company"] == company and job["role"] == role:
            return copy.deepcopy(job)
    raise KeyError(f"Existing job not found: {company} — {role}")


EVERIS = existing_job("Everis", "People Operations Specialist")
EVERIS.update(
    order=1,
    slug="01_Everis_People_Operations_Specialist",
    category="priority",
    status="Priority application — India expressly eligible",
)

MERIDIAL_BUSINESS = existing_job(
    "Meridial", "Business and Management Specialist – Freelance AI Trainer"
)
MERIDIAL_BUSINESS.update(
    order=6,
    slug="06_Meridial_Business_Management_AI_Trainer",
    category="priority",
    status="Priority contract application — hours and rate are not guaranteed",
)

MERIDIAL_INVESTMENT = existing_job(
    "Meridial", "Investment Specialist – Freelance AI Trainer"
)
MERIDIAL_INVESTMENT.update(
    order=7,
    slug="07_Meridial_Investment_AI_Trainer",
    category="priority",
    status="Selective contract application — prepare investment fundamentals",
)


JOBS = [
    EVERIS,
    {
        "order": 2,
        "slug": "02_Canonical_Graduate_HR_Generalist_APAC",
        "category": "priority",
        "company": "Canonical",
        "role": "Graduate HR Generalist – APAC",
        "url": "https://canonical.com/careers/5253092/graduate-hr-generalist-apac-remote",
        "platform": "Canonical Careers",
        "format": PDF_FORMAT,
        "fit": "Excellent early-career HR fit; global-HR systems gap",
        "status": "Priority application — APAC remote",
        "headline": "HR OPERATIONS | EMPLOYEE SUPPORT | ACCURATE DOCUMENTATION",
        "summary": (
            "Early-career HR Operations professional with approximately one year of post-internship "
            "experience supporting day-to-day people administration for a small workforce of about 70 "
            "employees. Pursuing an MHRM with a B.A. in Economics; brings employee communication, management "
            "follow-up, organised HR documentation, confidentiality, independent prioritisation, and a strong "
            "learning orientation suited to a distributed international People team."
        ),
        "skills": [
            "Day-to-day HR operations and employee support",
            "HR documentation and organised employee information",
            "Employee communication and management follow-up",
            "Recruitment, engagement, and performance-management exposure",
            "Confidential information handling and accuracy",
            "Microsoft Excel, Word, and PowerPoint",
            "Independent prioritisation and adaptability",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["performance", "excel", "uci", "vitara"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Canonical's APAC graduate role supports employee questions, HRIS records, new hires, benefits, "
            "payroll inputs, file audits, global projects, and process improvement. The selection criteria "
            "emphasise academic achievement, HR internship exposure, accuracy, communication, integrity, "
            "independence, adaptability, and willingness to travel."
        ),
        "gaps": [
            "No verified HRIS, payroll, benefits, purchase-order, GDPR, or global employee-lifecycle ownership.",
            "The application requires evidence for school and university performance; use only official marks.",
            "The signed myTVS experience/service certificate must support the title and dates used in the CV.",
        ],
        "keywords": [
            "HR operations", "employee support", "HR documentation", "confidential data", "accuracy",
            "global HR", "employee files", "process improvement", "prioritisation", "adaptability",
        ],
        "pitch": (
            "Approximately one year in a lean HR Operations environment has developed my employee "
            "communication, documentation, confidentiality, management follow-up, and independent "
            "prioritisation. My MHRM studies and HR analytics and performance-management learning provide a "
            "strong base for developing into Canonical's global HR processes and systems."
        ),
        "special_instruction": (
            "Canonical requires application responses in the candidate's own words. Do not paste AI-generated "
            "answers into the application form."
        ),
    },
    {
        "order": 3,
        "slug": "03_Outcapped_Operations_Associate",
        "category": "priority",
        "company": "Outcapped",
        "role": "Operations Associate",
        "url": "https://jobs.ashbyhq.com/outcapped/a13c3ae7-c78c-4526-bc96-07a4848f5a8c/",
        "platform": "Ashby",
        "format": PDF_FORMAT,
        "fit": "One-year threshold met; tooling and time-zone stretch",
        "status": "Priority stretch — work-from-anywhere role",
        "headline": "OPERATIONS | ADMINISTRATION | DOCUMENTATION & FOLLOW-THROUGH",
        "summary": (
            "Early-career operations professional with approximately one year of post-internship HR "
            "Operations experience in a lean organisation of about 70 employees. Brings careful "
            "documentation, information organisation, recurring administrative coordination, management "
            "follow-up, confidentiality, and independent prioritisation. Uses Claude, ChatGPT Codex, and "
            "Visual Studio Code for structured research, drafting, organisation, and output review."
        ),
        "skills": [
            "Administrative and day-to-day operations support",
            "Documentation and information organisation",
            "Accuracy, confidentiality, and detail review",
            "Management follow-up and action completion",
            "Independent prioritisation in a lean environment",
            "Microsoft Excel, Word, and PowerPoint",
            "AI-assisted research, drafting, and output review",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "performance", "uci", "powerbi"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Outcapped supports mission-driven startups with hands-on back-office operations. It asks for "
            "one to three years in operations or administration, exposure to operational areas such as "
            "documentation or admin, strong English, attention to detail, reliable follow-through, and "
            "comfort learning tools. Selection includes a work test and paid two-month trial."
        ),
        "gaps": [
            "No verified professional use of Notion, Google Workspace, Slack, Airtable, Zapier, or Make.",
            "No verified finance operations, client delivery, no-code automation, or startup-agency experience.",
            "The advertised CEST and Pacific overlap may require an unusually long split working day from India.",
        ],
        "keywords": [
            "operations associate", "administration", "documentation", "quality assurance", "organisation",
            "follow-through", "process improvement", "remote operations", "AI tools", "owner thinking",
        ],
        "pitch": (
            "My lean-company HR Operations experience aligns with Outcapped's need for reliable administrative "
            "execution, accurate documentation, organisation, and follow-through. I have not used its named "
            "startup tools professionally, but I am comfortable learning software independently and can "
            "demonstrate careful execution in the practical work test."
        ),
        "special_instruction": (
            "Confirm that the combined CEST and Pacific-time overlap is sustainable before entering the work trial."
        ),
    },
    {
        "order": 4,
        "slug": "04_Canonical_Graduate_Customer_Success_Manager",
        "category": "priority",
        "company": "Canonical",
        "role": "Graduate Customer Success Manager",
        "url": "https://canonical.com/careers/6103331",
        "platform": "Canonical Careers",
        "format": PDF_FORMAT,
        "fit": "Graduate eligibility met; customer-success and Linux knowledge gap",
        "status": "Priority stretch — worldwide remote",
        "headline": "CUSTOMER SUCCESS | DOCUMENTATION | EMPATHETIC FOLLOW-THROUGH",
        "summary": (
            "Early-career operations professional with approximately one year of post-internship HR "
            "Operations experience involving routine employee communication, management follow-up, organised "
            "documentation, confidentiality, and independent prioritisation. Pursuing an MHRM with a B.A. in "
            "Economics and hands-on experience using modern AI tools for research, drafting, information "
            "organisation, and output review. Interested in developing a career in technology customer success."
        ),
        "skills": [
            "Employee communication and issue follow-up",
            "Empathetic, professional communication",
            "Documentation and information organisation",
            "Problem-solving and critical thinking",
            "Microsoft Excel, Word, and PowerPoint",
            "AI-assisted research, drafting, and output review",
            "Independent learning and cross-functional teamwork",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "uci", "performance", "powerbi"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Canonical's worldwide graduate CSM role supports tickets, documentation, onboarding materials, "
            "digital campaigns, product adoption, feedback, risk identification, and customer portfolios. It "
            "explicitly accepts recent graduates or candidates with no more than two years of work experience."
        ),
        "gaps": [
            "No verified external customer portfolio, ticketing, SaaS onboarding, retention, or churn experience.",
            "No verified Ubuntu, Linux, cloud-infrastructure, or Canonical-product knowledge.",
            "The application asks the candidate to explain Canonical's products and interest in customer success.",
        ],
        "keywords": [
            "customer success", "customer support", "documentation", "onboarding", "product adoption",
            "feedback", "risk identification", "technology", "organisation", "empathy",
        ],
        "pitch": (
            "My current experience is internal HR Operations rather than formal customer success, but it has "
            "developed empathetic communication, structured follow-up, careful documentation, and independent "
            "problem-solving. I would combine that foundation with focused learning of Ubuntu and Canonical's "
            "product portfolio."
        ),
        "special_instruction": (
            "Canonical requires application responses in the candidate's own words. Independently study Ubuntu "
            "Pro, MAAS, Landscape, OpenStack, Ceph, and Kubernetes before answering."
        ),
    },
    {
        "order": 5,
        "slug": "05_Canonical_Graduate_Sales_Development_Representative",
        "category": "priority",
        "company": "Canonical",
        "role": "Graduate Sales Development Representative",
        "url": "https://job-boards.greenhouse.io/canonical/jobs/5915299",
        "platform": "Greenhouse",
        "format": GREENHOUSE_FORMAT,
        "fit": "Strong graduate foundation; no sales pipeline experience",
        "status": "Priority stretch — worldwide remote",
        "headline": "BUSINESS DEVELOPMENT | RESEARCH | COMMUNICATION & FOLLOW-UP",
        "summary": (
            "MHRM candidate and Economics graduate with approximately one year of HR Operations experience in "
            "a lean, 70-person organisation. Brings structured research, professional communication, management "
            "follow-up, business-plan learning, critical thinking, and hands-on use of Claude, ChatGPT Codex, "
            "and Visual Studio Code. Interested in building a technology sales career through disciplined "
            "prospecting, continuous learning, and evidence-based business conversations."
        ),
        "skills": [
            "Business research and information synthesis",
            "Professional communication and structured follow-up",
            "Economics foundation and business reasoning",
            "Business-plan preparation process",
            "Microsoft Excel, Word, and PowerPoint",
            "AI-assisted research, drafting, and output review",
            "Curiosity, persistence, and continuous learning",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "performance", "powerbi", "uci"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Canonical's graduate SDR role handles inbound enquiries, outbound campaigns, prospect research, "
            "market trends, lead records, meetings, and collaboration with sales and marketing. It prioritises "
            "academic performance, interest in business and technology, communication, persistence, curiosity, "
            "and problem-solving rather than prior sales tenure."
        ),
        "gaps": [
            "No verified cold calling, prospecting, CRM, lead generation, quota, pipeline, or technology-sales experience.",
            "No verified Linux, cloud, or Canonical-product knowledge.",
            "The application requires candidate-authored examples of technology interest, problem-solving, and leadership.",
        ],
        "keywords": [
            "sales development", "business development", "prospect research", "market research",
            "inbound enquiries", "outbound campaigns", "communication", "persistence", "technology",
        ],
        "pitch": (
            "My Economics, MHRM, business-plan learning, operations experience, and AI-tool familiarity give me "
            "a foundation for understanding business problems and communicating clearly. I do not claim prior "
            "sales pipeline ownership, but I can bring disciplined research, persistence, and willingness to "
            "learn Canonical's products and sales process."
        ),
        "special_instruction": (
            "Canonical prohibits AI-generated application answers. Write every required example independently "
            "and support academic claims with official marks."
        ),
    },
    MERIDIAL_BUSINESS,
    MERIDIAL_INVESTMENT,
    {
        "order": 8,
        "slug": "08_Anchorial_Link_Building_Executive",
        "category": "expired",
        "company": "Anchorial",
        "role": "Link Building Executive",
        "url": "https://in.linkedin.com/jobs/view/link-building-executive-remote-at-anchorial-4440201324",
        "platform": "LinkedIn / email application",
        "format": PDF_FORMAT,
        "fit": "Transferable research and AI-tool fit; direct SEO gap",
        "status": "Closed — LinkedIn listing expired on 31 July 2026",
        "headline": "RESEARCH | WRITTEN OUTREACH | AI-ASSISTED INFORMATION REVIEW",
        "summary": (
            "Early-career operations professional with approximately one year of experience in a lean "
            "organisation, combining structured information organisation, routine professional communication, "
            "management follow-up, confidentiality, and independent prioritisation. Pursuing an MHRM with a "
            "B.A. in Economics and hands-on use of Claude, ChatGPT Codex, and Visual Studio Code for research, "
            "drafting, organisation, and output review. Interested in developing white-hat SaaS outreach and SEO."
        ),
        "skills": [
            "Structured online research and information organisation",
            "Professional written communication",
            "Consistent follow-up and action tracking",
            "Critical thinking and quality awareness",
            "Microsoft Excel, Word, and PowerPoint",
            "Claude, ChatGPT Codex, and VS Code",
            "Independent learning in a remote environment",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "performance", "powerbi", "uci"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Anchorial's India-remote role researches and qualifies publishers, conducts personalised editor "
            "outreach, negotiates placements, evaluates article fit, maintains campaigns, and builds publisher "
            "relationships. Freshers are welcome if they demonstrate strong writing and genuine SEO interest. "
            "The process includes a one-week paid trial."
        ),
        "gaps": [
            "No verified SEO, link-building, cold-email, publisher-relations, or placement-negotiation experience.",
            "No verified Ahrefs, Semrush, n8n, Snov.io, Monday.com, or Claude API experience.",
            "The email application asks for an original cold-email example; it must be written and defended by the candidate.",
        ],
        "keywords": [
            "link building", "publisher research", "editor outreach", "written English", "SEO",
            "SaaS", "AI search", "relationship building", "campaign organisation", "Claude",
        ],
        "pitch": (
            "My current experience has developed structured research, careful information handling, clear "
            "communication, and persistent follow-up. Although I have not yet worked in SEO or publisher "
            "outreach, I am comfortable using modern AI tools thoughtfully and am prepared to demonstrate my "
            "writing and research ability in Anchorial's paid trial."
        ),
        "special_instruction": (
            "Do not apply through the expired LinkedIn listing. Retain this CV only in case Anchorial republishes "
            "the role. Any future application must use a candidate-written cold-email example and must not claim "
            "links or placements that do not exist."
        ),
    },
    {
        "order": 9,
        "slug": "09_Prox_Agent_Evals_Specialist",
        "category": "conditional",
        "company": "Prox",
        "role": "Agent Evals Specialist – Knowledge Graph Review",
        "url": "https://jobs.ashbyhq.com/prox/c0c1c269-c761-48d1-a2ad-da3ee36d08ba/",
        "platform": "Ashby",
        "format": PDF_FORMAT,
        "fit": "Assessment-based AI stretch; India eligibility not explicit",
        "status": "Conditional — confirm India eligibility",
        "headline": "AI OUTPUT REVIEW | CRITICAL READING | STRUCTURED FEEDBACK",
        "summary": (
            "MHRM candidate and Economics graduate with approximately one year of HR Operations experience, "
            "careful documentation habits, critical-thinking coursework, and hands-on use of Claude, ChatGPT "
            "Codex, and Visual Studio Code for research, drafting, information organisation, and output review. "
            "Brings patience with detailed material, attention to accuracy, and clear written explanation for "
            "an entry-level AI evaluation environment."
        ),
        "skills": [
            "Critical reading and structured reasoning",
            "AI-assisted output review",
            "Document comparison and information organisation",
            "Clear written explanation and critical thinking",
            "Accuracy, consistency, and confidentiality awareness",
            "Microsoft Excel, Word, and PowerPoint",
            "Independent task prioritisation",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "uci", "performance", "powerbi"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Prox's evaluator compares technical source documents with AI-agent outputs, scores accuracy and "
            "coverage, and writes specific feedback. Prior AI-training work is preferred, not mandatory. Every "
            "applicant receives the same short practical prescreen, but the listing does not expressly name "
            "India as an eligible location."
        ),
        "gaps": [
            "No verified professional AI evaluation, annotation, technical writing, QA, or knowledge-graph experience.",
            "No verified Markdown expertise or sustained review of dense technical documents.",
            "India eligibility and contractor/payment setup are not stated clearly on the vacancy page.",
        ],
        "keywords": [
            "AI evaluation", "agent evals", "knowledge graph", "accuracy", "coverage", "structured feedback",
            "technical documents", "quality review", "critical reading", "consistency",
        ],
        "pitch": (
            "I offer critical thinking, careful documentation, hands-on LLM use, and experience organising "
            "confidential information accurately. I would rely on the standard prescreen to demonstrate my "
            "ability rather than claim prior professional AI-evaluation experience."
        ),
        "special_instruction": "Confirm that Prox can engage and pay an India-based worker before completing unpaid steps.",
    },
    {
        "order": 10,
        "slug": "10_Allara_Onboarding_Payer_Operations_Coordinator",
        "category": "conditional",
        "company": "Allara",
        "role": "Onboarding Payer Operations Coordinator",
        "url": "https://jobs.ashbyhq.com/allarahealth/71d49ac6-4375-402a-84d0-a63412cdb7ca/",
        "platform": "Ashby",
        "format": PDF_FORMAT,
        "fit": "Operations foundation; healthcare and location uncertainty",
        "status": "Conditional — confirm India is accepted",
        "headline": "OPERATIONS COORDINATION | DOCUMENT ACCURACY | CONFIDENTIALITY",
        "summary": (
            "Early-career HR Operations professional with approximately one year of post-internship experience "
            "supporting administration for about 70 employees. Brings accurate document organisation, "
            "confidential information handling, routine communication, management follow-up, independent "
            "prioritisation, and willingness to learn structured workflows. Pursuing an MHRM with a B.A. in "
            "Economics and interested in transferring these skills to healthcare operations."
        ),
        "skills": [
            "Document management and information accuracy",
            "Confidential information handling",
            "Routine operations coordination and follow-up",
            "Employee communication and escalation awareness",
            "Independent prioritisation and workflow learning",
            "Microsoft Excel, Word, and PowerPoint",
            "AI-assisted research, drafting, and output review",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "performance", "uci", "vitara"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Allara's entry-level coordinator handles provider enrolment, licensing, credentialing, onboarding "
            "documents, data accuracy, status updates, escalation, and SOP learning. The description says "
            "internationally remote and welcomes recent graduates, but the vacancy metadata identifies the "
            "Philippines, creating an India-eligibility conflict."
        ),
        "gaps": [
            "No verified healthcare administration, payer enrolment, provider credentialing, licensing, or onboarding experience.",
            "No CAQH, Verifiable, Airtable, or healthcare-compliance experience.",
            "The listing's location metadata conflicts with its internationally remote wording.",
        ],
        "keywords": [
            "payer operations", "provider enrolment", "credentialing", "licensing", "onboarding",
            "data accuracy", "document management", "status tracking", "escalation", "SOPs",
        ],
        "pitch": (
            "My HR Operations background provides transferable documentation, confidentiality, communication, "
            "and follow-up skills. I do not have healthcare credentialing experience, but I am comfortable "
            "learning structured processes and escalating exceptions rather than overstating domain expertise."
        ),
        "special_instruction": "Proceed only if India appears as an accepted country in the application form.",
    },
    {
        "order": 11,
        "slug": "11_Superwork_Data_Analyst_Fresher",
        "category": "conditional",
        "company": "Superwork",
        "role": "Data Analyst Fresher",
        "url": "https://jobs.pyjamahr.com/superwork/data-analyst-fresher-2",
        "platform": "PyjamaHR",
        "format": PDF_FORMAT,
        "fit": "Education aligns; mandatory technical stack not evidenced",
        "status": "Conditional — build technical portfolio first",
        "headline": "ENTRY-LEVEL DATA ANALYTICS | ECONOMICS | EXCEL COURSEWORK",
        "summary": (
            "Economics graduate pursuing an MHRM, with Excel-based HR analytics coursework, introductory "
            "Power BI workshop exposure, and approximately one year of HR Operations experience maintaining "
            "organised employee information in a 70-person environment. Brings analytical reasoning, attention "
            "to data accuracy, Microsoft Office capability, structured business-plan learning, and a strong "
            "interest in developing practical data-analysis skills."
        ),
        "skills": [
            "Economics foundation and analytical reasoning",
            "Excel-based HR analytics coursework",
            "Introductory Power BI workshop exposure",
            "Information accuracy and organisation",
            "Business-plan preparation process",
            "Microsoft Excel, Word, and PowerPoint",
            "Critical thinking and output review",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "powerbi", "uci", "performance"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "The remote India fresher listing accepts zero to two years but names SQL, Excel, Python, Tableau, "
            "Power BI, data cleaning, visualisation, and basic statistics as must-have skills. The candidate's "
            "current evidence supports only Excel-based coursework and introductory Power BI exposure."
        ),
        "gaps": [
            "No verified SQL, Python, Tableau, BigQuery, Looker, Git, or data-warehouse experience.",
            "No independently reviewed analytics portfolio or production dashboard evidence.",
            "The listed technical requirements make immediate shortlisting unlikely despite fresher eligibility.",
        ],
        "keywords": [
            "data analyst", "Excel", "Power BI", "data accuracy", "reporting", "dashboards",
            "economics", "statistics", "data cleaning", "visualisation",
        ],
        "pitch": (
            "My Economics degree, Excel-based HR analytics coursework, introductory Power BI workshop, and "
            "information-accuracy experience provide a foundation for data analytics. I would not claim the "
            "mandatory SQL, Python, or Tableau skills until I have completed and can explain relevant projects."
        ),
        "special_instruction": (
            "Do not submit until at least one independently reproducible SQL/Excel/Power BI project has been "
            "completed; answer every technical screening question truthfully."
        ),
    },
    {
        "order": 12,
        "slug": "12_Jobgether_Customer_Support_Agent_SaaS_Helpdesk",
        "category": "conditional",
        "company": "Jobgether",
        "role": "Customer Support Agent – SaaS Helpdesk",
        "url": "https://jobs.lever.co/jobgether/8083c98a-05ae-450a-8df4-4b88f29a879c",
        "platform": "Lever",
        "format": PDF_FORMAT,
        "fit": "Communication foundation; mandatory written-support gap",
        "status": "Conditional — one-year email-support requirement is unmet",
        "headline": "CUSTOMER SUPPORT TRANSITION | DOCUMENTATION | PROBLEM-SOLVING",
        "summary": (
            "Early-career HR Operations professional with approximately one year of experience involving "
            "routine employee communication, management follow-up, accurate documentation, confidentiality, "
            "and independent prioritisation. Pursuing an MHRM with a B.A. in Economics and hands-on use of "
            "Claude, ChatGPT Codex, and Visual Studio Code for research, drafting, organisation, and output "
            "review. Interested in transferring these strengths into technology customer support."
        ),
        "skills": [
            "Professional employee communication and follow-up",
            "Documentation and information organisation",
            "Problem-solving and critical thinking",
            "Confidential information handling",
            "Independent learning from written information",
            "Microsoft Excel, Word, and PowerPoint",
            "AI-assisted research, drafting, and output review",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "uci", "performance", "powerbi"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Jobgether is advertising an unnamed partner's India-remote SaaS helpdesk position. The role "
            "handles written support, technical troubleshooting, help articles, ticket queues, escalation, "
            "privacy, and collaboration. It explicitly requires at least one year of email or comparable "
            "written customer-support experience."
        ),
        "gaps": [
            "No verified one-year email customer-support or written helpdesk experience.",
            "No verified Zendesk, ticketing, SaaS troubleshooting, email-security, spam, or phishing support experience.",
            "The underlying partner company is not identified in the listing.",
        ],
        "keywords": [
            "customer support", "SaaS helpdesk", "written communication", "technical troubleshooting",
            "documentation", "help articles", "ticketing", "privacy", "escalation", "problem-solving",
        ],
        "pitch": (
            "My HR Operations experience offers transferable communication, documentation, confidentiality, "
            "and follow-up skills, but it is not equivalent to one year of email helpdesk support. I would "
            "apply only if the employer is willing to consider adjacent operational communication experience."
        ),
        "special_instruction": (
            "Do not answer Yes to the one-year email-support requirement unless separately documented experience exists."
        ),
    },
]


def filename_stem(job: dict) -> str:
    base = f"Mohammad_Azimuddin_{job['company']}_{job['role']}"
    return re.sub(r"[^A-Za-z0-9_-]+", "_", base).strip("_")


def application_notes(job: dict) -> str:
    gaps = "\n".join(f"- {item}" for item in job["gaps"])
    keywords = ", ".join(job["keywords"])
    special = job.get("special_instruction", "No additional role-specific instruction.")
    return f"""# {job['company']} — {job['role']}

Prepared: 31 July 2026

## Live vacancy

- Application page: {job['url']}
- Platform: {job['platform']}
- Category: {job['category'].title()}
- Fit assessment: {job['fit']}
- Recommended status: {job['status']}
- Availability: The application action was visible when rechecked on 31 July 2026. Recheck immediately before submission.

## CV design

{job['format']}

The CV is one A4 page, single-column, text-extractable, and targeted to the exact company and role.
It contains no photo, date of birth, nationality, marital status, graphics, skill bars, or unsupported metrics.

## Role analysis

{job['company_analysis']}

## Evidence gaps

{gaps}

## ATS language researched

{keywords}

Unsupported keywords are documented here for gap analysis but are not presented in the CV as completed
professional experience.

## Suggested truthful positioning

{job['pitch']}

## Critical instruction

{special}

## Before submission

- [ ] Confirm the listing is still open and accepts applicants based in India.
- [ ] Upload only the PDF labelled for this exact employer and role.
- [ ] Ensure signed myTVS documents support `HR Operations · July 2025–Present`.
- [ ] Answer all experience, location, shift, software, salary, and work-authorisation questions truthfully.
- [ ] Do not add HRIS, payroll, onboarding ownership, ATS, CRM, SQL, Python, Tableau, advanced Excel,
      professional AI training, SEO placements, helpdesk tickets, or quantified results without evidence.
- [ ] Review the platform-generated preview and retain a copy of every submitted answer.
"""


def master_readme() -> str:
    rows = "\n".join(
        f"{job['order']}. **{job['company']} — {job['role']}**  \n"
        f"   `{job['slug']}` · {job['fit']} · {job['status']}"
        for job in sorted(JOBS, key=lambda item: item["order"])
    )
    return f"""# High-Paying Remote Early-Career Application Pack

Prepared: 31 July 2026

This is a separate 12-role pack based on the latest vacancy research and the candidate-confirmed
approximately one year of post-internship HR Operations experience at myTVS.

## Contents

- Seven currently actionable priority-role CVs
- Four conditional-role CVs retained with explicit evidence or location warnings
- One closed-role CV preserved in case the employer republishes the vacancy
- One ATS-focused HTML reference and plain-text copy per role
- One role-analysis and submission-control file per role
- A priority-ordered target matrix
- A documented build and evidence audit in `QA_REPORT_2026-07-31.md`

After PDF rendering, use `00_Ready_to_Upload` for priority applications and
`99_Conditional_or_Gap` only after resolving the documented condition.
`98_Expired_or_Closed` is reference material and must not be submitted to the expired vacancy.

## Recommended order

{rows}

## Evidence controls

- Employment is shown as `HR Operations · myTVS · July 2025–Present`, pending the signed
  experience/service certificate.
- Duties remain limited to candidate-confirmed HR administration, employee communication,
  management follow-up, documentation, confidentiality, independent prioritisation, and follow-through.
- No HRIS, payroll, ATS, CRM, SQL, Python, Tableau, advanced Excel, SEO placement, helpdesk-ticket,
  professional AI-training, or quantified achievement claim has been invented.
- MHRM is shown as 2024–2026 without claiming that the final degree has already been issued.

## Important

Targeting improves relevance; it cannot guarantee a shortlist or offer. Vacancy availability,
country eligibility, contractor hours, and advertised compensation can change without notice.

The Anchorial LinkedIn vacancy redirected to an expired-job page when checked again on
31 July 2026. Do not submit that CV unless Anchorial republishes the role.
"""


def write_outputs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "README.md").write_text(master_readme(), encoding="utf-8")

    with (OUT / "00_Target_Job_Matrix.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "Priority", "Category", "Company", "Role", "Platform", "Fit", "Status",
                "Application URL", "Folder",
            ]
        )
        for job in sorted(JOBS, key=lambda item: item["order"]):
            writer.writerow(
                [
                    job["order"], job["category"], job["company"], job["role"], job["platform"],
                    job["fit"], job["status"], job["url"], job["slug"],
                ]
            )

    for job in JOBS:
        folder = OUT / job["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        stem = filename_stem(job)
        html_source = BASE.resume_html(job)
        (folder / f"{stem}_CV.html").write_text(html_source, encoding="utf-8")
        (folder / f"{stem}_CV.txt").write_text(BASE.html_to_text(html_source), encoding="utf-8")
        (folder / "APPLICATION_NOTES.md").write_text(application_notes(job), encoding="utf-8")

    print(f"Generated {len(JOBS)} targeted CV packages under {OUT}")


if __name__ == "__main__":
    write_outputs()
