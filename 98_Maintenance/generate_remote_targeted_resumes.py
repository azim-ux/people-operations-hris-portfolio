#!/usr/bin/env python3
"""Generate evidence-controlled, role-specific remote-job resume packages."""

from __future__ import annotations

import csv
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "07_Remote_Job_Applications" / "2026-07-30"
ORACLE_BADGE_URL = "https://catalog-education.oracle.com/ords/certview/sharebadge?id=EEB81659F197DAB703AB626ABED829FF6C2A0DDF27309D9C4D3690D71D2CE7A2"

CONTACT = {
    "name": "MOHAMMAD AZIMUDDIN",
    "location": "Aligarh, Uttar Pradesh, India · Available for remote work",
    "linkedin": "linkedin.com/in/md-azimuddin-34b088174",
    "linkedin_url": "https://www.linkedin.com/in/md-azimuddin-34b088174",
}

MYTVS_HR_OPS = {
    "title": "HR Operations",
    "org": "myTVS · Aligarh, India",
    "dates": "July 2025 – Present",
    "bullets": [
        "Continued with myTVS in HR Operations after completing a Human Resources internship from 26 May to 16 July 2025.",
        "Handle day-to-day HR operations for a small-company workforce of approximately 70 employees, coordinating routine HR administration, employee communication, and management follow-ups.",
        "Maintain HR documentation and organise employee information with attention to accuracy, confidentiality, and timely retrieval.",
        "Work independently in a lean environment, prioritising recurring HR requirements and following actions through to completion.",
    ],
}

SURE = {
    "title": "Consultant, SURE Program",
    "org": "Aligarh Muslim University × C. T. Bauer College of Business, University of Houston",
    "dates": "August 2024 – October 2024",
    "bullets": [
        "Participated as a Consultant in a 12-week MSME-focused programme.",
        "Learned a structured process for preparing business plans and organising business information.",
        "Worked in a collaborative academic setting involving AMU and the University of Houston.",
    ],
}

FILMSAAZ = {
    "title": "Intern, Filmsaaz 2023",
    "org": "University Film Club, Aligarh Muslim University · Aligarh, India",
    "dates": "March 2023 – April 2023",
    "bullets": [
        "Recruited as an intern for the 13th Filmsaaz International Short Film Festival.",
        "Contributed as a member of the festival team in a university event environment.",
    ],
}

EDUCATION = [
    {
        "title": "Master of Human Resource Management (MHRM)",
        "org": "Aligarh Muslim University",
        "dates": "2024 – 2026",
        "detail": "",
    },
    {
        "title": "Bachelor of Arts in Economics",
        "org": "Aligarh Muslim University",
        "dates": "2021 – 2024",
        "detail": "CGPA: 7.4/10",
    },
]

LEARNING = {
    "oracle": "Oracle Fusion Cloud Applications HCM Process Essentials Certified – Rel 1 — Oracle, August 2026",
    "performance": "Performance Management System — IIM Bangalore / SWAYAM, 2024 (90.4%)",
    "excel": "HR Analytics Using Excel — Dayananda Sagar Institutions / SWAYAM, 2024 (78.8%)",
    "uci": "Human Resources Analytics — University of California, Irvine, 2023",
    "vitara": "VITARA-HRMx — IMF/edX",
    "powerbi": "AI-Enhanced Power BI three-day workshop — Aligarh Muslim University, October 2024",
}


def learning_keys(job: dict) -> list[str]:
    """Place the verified Oracle HCM credential first without duplicating it."""
    return ["oracle", *[key for key in job["learning"] if key != "oracle"]]

AI_TOOLS = (
    "Hands-on use of Claude, ChatGPT Codex, and Visual Studio Code for research, "
    "drafting, information organisation, and output review"
)

LINKEDIN_FORMAT = (
    "LinkedIn currently recommends Microsoft Word or PDF below 2 MB. This package "
    "uses a one-page, text-extractable PDF below that limit."
)
GREENHOUSE_FORMAT = (
    "Greenhouse accepts DOC, DOCX, PDF, RTF, and TXT uploads up to 100 MB. Submit "
    "the PDF; use the TXT copy only for manual form fields."
)
PDF_FORMAT = (
    "Submit the one-page, text-extractable PDF. A plain-text copy is included for "
    "application fields and ATS verification."
)


JOBS = [
    {
        "order": 1,
        "slug": "01_Everis_People_Operations_Specialist",
        "company": "Everis",
        "role": "People Operations Specialist",
        "url": "https://jobs.ashbyhq.com/everis/8fd7e6fa-edab-4c8e-8955-5b310afe80b9/",
        "platform": "Ashby",
        "format": PDF_FORMAT,
        "fit": "Strongest fit",
        "status": "Apply now",
        "headline": "PEOPLE OPERATIONS | HR ADMINISTRATION | AI-ASSISTED DOCUMENTATION",
        "summary": (
            "HR Operations professional with approximately one year of post-internship experience supporting "
            "day-to-day people administration for a small workforce of about 70 employees. Pursuing an MHRM "
            "with a B.A. in Economics; experienced in organising HR documentation, coordinating routine "
            "employee communication and management follow-ups, and handling confidential information. "
            "Hands-on user of Claude, ChatGPT Codex, and Visual Studio Code for structured research, drafting, "
            "information organisation, and output review."
        ),
        "skills": [
            "Day-to-day HR operations and administration",
            "Employee communication and management follow-up",
            "HR documentation and confidential information handling",
            "Recruitment and selection exposure",
            "Structured documentation and information organisation",
            "Microsoft Excel, Word, and PowerPoint",
            "AI-assisted research, drafting, and output review",
            "Independent prioritisation and follow-through",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["performance", "excel", "uci", "vitara"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Everis is a new acquisition-and-operations company founded by experienced remote-technology "
            "operators. The role prioritises reliability, documentation, internal systems, HR records, "
            "coordination, confidentiality, and practical use of AI rather than a fixed number of years."
        ),
        "gaps": [
            "No verified ownership of onboarding/offboarding, payroll, leave systems, or HRIS.",
            "No quantified hiring or process-improvement results.",
            "The role will attract unusually strong applicants because direct experience is not mandatory and pay is high.",
        ],
        "keywords": [
            "People Operations", "HR administration", "HR documentation", "recruitment coordination",
            "employee records", "onboarding support", "training materials", "AI tools", "remote operations",
            "confidential information", "SOPs", "organisation",
        ],
        "pitch": (
            "I have approximately one year of post-internship HR Operations experience at myTVS, supporting "
            "day-to-day people administration for a workforce of about 70 employees. The lean environment has "
            "required careful documentation, independent prioritisation, clear employee communication, "
            "confidentiality, and dependable follow-through. Alongside my MHRM, I use Claude, ChatGPT Codex, "
            "and VS Code for structured research, drafting, organisation, and output review. This combination "
            "matches Everis's need for a reliable early-career operator who can learn systems quickly."
        ),
    },
    {
        "order": 12,
        "slug": "02_Unloq_Revenue_Operations_Coordinator",
        "company": "Unloq",
        "role": "Revenue Operations Coordinator",
        "url": "https://in.linkedin.com/jobs/view/revenue-operations-coordinator-at-unloq%C2%AE-4442467036",
        "platform": "LinkedIn",
        "format": LINKEDIN_FORMAT,
        "fit": "Relevant operations foundation; no commercial systems experience",
        "status": "Closed on LinkedIn; retain for repost or direct outreach",
        "headline": "REVENUE OPERATIONS | AI-ASSISTED RESEARCH | PROCESS DOCUMENTATION",
        "summary": (
            "Operations-focused MHRM candidate with a B.A. in Economics and approximately one year of "
            "post-internship HR Operations experience in a lean, 70-person organisation. Brings disciplined "
            "follow-up, documentation, employee and management communication, business-plan learning, and "
            "hands-on use of Claude, ChatGPT Codex, and Visual Studio Code for research, drafting, information "
            "organisation, and output review. Interested in transferring this operating discipline into "
            "Revenue Operations."
        ),
        "skills": [
            "Structured trackers, documentation, and information organisation",
            "Management follow-up and action closure",
            "AI-assisted research, drafting, and output review",
            "Microsoft Excel, Word, and PowerPoint",
            "Economics foundation and business-plan preparation",
            "Professional written communication",
            "Independent prioritisation in a lean environment",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "powerbi", "performance", "uci"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Unloq builds AI systems for high-stakes business use. The coordinator role is the operating "
            "backbone between founders, sales, marketing, agencies, and prospects. It explicitly values a "
            "recent graduate with placement experience, strong writing, persistent follow-up, and "
            "demonstrable use of frontier AI coding and chat tools."
        ),
        "gaps": [
            "No verified Salesforce, HubSpot, CRM administration, SDR, outbound-agency, or sales-pipeline experience.",
            "No evidence-backed revenue metrics or commercial quota work.",
            "The application should include a small, truthful work sample demonstrating organised AI-assisted research.",
        ],
        "keywords": [
            "Revenue Operations", "pipeline", "CRM data quality", "lead qualification", "sales support",
            "commercial operations", "AI tools", "prompt and context", "professional writing", "follow-up",
            "reporting", "process discipline",
        ],
        "pitch": (
            "My background combines approximately one year in HR Operations, an MHRM, Economics, structured "
            "business-plan learning, and hands-on use of Claude, ChatGPT Codex, and VS Code. Working in a lean "
            "company has developed disciplined tracking, clear communication, management follow-up, and "
            "independent prioritisation. I have not administered a production CRM and would not overstate "
            "that experience, but I offer an operations foundation and fast tool learning relevant to a "
            "Revenue Operations coordinator role."
        ),
    },
    {
        "order": 5,
        "slug": "03_Meridial_Business_Management_AI_Trainer",
        "company": "Meridial",
        "role": "Business and Management Specialist – Freelance AI Trainer",
        "url": "https://job-boards.greenhouse.io/agency/jobs/4784908101",
        "platform": "Greenhouse",
        "format": GREENHOUSE_FORMAT,
        "fit": "Strong academic fit",
        "status": "Apply now; contract work",
        "headline": "BUSINESS & MANAGEMENT AI EVALUATION | HRM | ECONOMICS",
        "summary": (
            "Business and management-focused MHRM candidate with a B.A. in Economics and approximately one "
            "year of post-internship HR Operations experience in a 70-person organisation. Combines practical "
            "exposure to day-to-day organisational operations with performance-management, HR analytics, and "
            "business-plan learning. Brings critical reading, structured reasoning, clear written explanation, "
            "and hands-on use of Claude and ChatGPT Codex for research and output review."
        ),
        "skills": [
            "Management principles and organisational performance coursework",
            "Economics foundation and business reasoning",
            "HR analytics and performance-management coursework",
            "Business-plan preparation process",
            "Critical reading and structured written explanation",
            "AI-assisted research and output review",
            "Microsoft Excel, Word, and PowerPoint",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["performance", "excel", "uci", "vitara", "powerbi"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "This project evaluates whether AI can reason about business operations, management, "
            "organisational behaviour, strategy, and practical decisions. The listing explicitly welcomes "
            "entry-level candidates with business, management, or economics foundations and emphasises "
            "clear explanations of reasoning."
        ),
        "gaps": [
            "No verified professional AI-training employment or formal model-evaluation role.",
            "No published business research or documented consulting outcomes.",
            "Contract rate and task availability are variable; the advertised ceiling should not be treated as expected earnings.",
        ],
        "keywords": [
            "business management", "organisational behaviour", "business operations", "strategy",
            "decision-making", "AI evaluation", "structured feedback", "logical consistency",
            "management scenarios", "economics", "critical reasoning",
        ],
        "pitch": (
            "My MHRM and Economics background gives me a strong base for evaluating management, "
            "organisational behaviour, performance, and business-decision scenarios. Approximately one year "
            "in myTVS HR Operations adds practical context from supporting a lean organisation of about 70 "
            "employees, while the SURE Program developed structured business-plan thinking. I also use Claude "
            "and ChatGPT Codex for research, drafting, organisation, and careful output review. I would bring "
            "transparent reasoning, practical business context, and a willingness to document uncertainty."
        ),
    },
    {
        "order": 2,
        "slug": "04_Yodo1_People_Operations_Coordinator",
        "company": "Yodo1",
        "role": "People Operations Coordinator",
        "url": "https://careers.yodo1.com/jobs/7664931-people-operations-coordinator",
        "platform": "Teamtailor",
        "format": PDF_FORMAT,
        "fit": "Strong relevant fit",
        "status": "Apply now",
        "headline": "PEOPLE OPERATIONS | EMPLOYEE EXPERIENCE | AI-ASSISTED DOCUMENTATION",
        "summary": (
            "People Operations candidate with approximately one year of post-internship HR Operations "
            "experience supporting a small workforce of about 70 employees. Pursuing an MHRM with a B.A. "
            "in Economics; brings day-to-day HR administration, employee communication, management follow-up, "
            "documentation, confidentiality, and independent prioritisation. Uses Claude, ChatGPT Codex, and "
            "Visual Studio Code for structured research, drafting, information organisation, and output review."
        ),
        "skills": [
            "Day-to-day People and HR operations",
            "Employee communication and management follow-up",
            "HR documentation and organised employee information",
            "Recruitment and selection exposure",
            "HR analytics and report-interpretation coursework",
            "AI-assisted research, drafting, and output review",
            "Microsoft Excel, Word, and PowerPoint",
            "Confidentiality, prioritisation, and follow-through",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "performance", "uci", "powerbi"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Yodo1 is a global mobile-games company designed around work from anywhere. The role supports "
            "onboarding, People data, internal documentation, reporting, process improvement, and practical "
            "AI use. Its culture signals impact, curiosity, ownership, precise communication, and comfort "
            "with distributed teams."
        ),
        "gaps": [
            "No verified ownership of onboarding systems, ATS updates, People data, or Notion workspaces.",
            "Experience is from a small local organisation rather than a distributed technology company.",
            "Potential Beijing-hours overlap should be confirmed before accepting the role.",
        ],
        "keywords": [
            "People Operations", "onboarding", "employee experience", "People data", "documentation",
            "Talent Operations", "HR operations", "AI efficiency", "process improvement", "remote team",
            "attention to detail", "ownership",
        ],
        "pitch": (
            "I have approximately one year of post-internship HR Operations experience supporting a "
            "70-person organisation, where lean staffing required independent prioritisation, employee "
            "communication, management follow-up, confidentiality, and organised HR documentation. Yodo1's "
            "focus on People systems, process improvement, ownership, and practical AI use matches my next "
            "step. I also use Claude, ChatGPT Codex, and VS Code for structured drafting, organisation, and "
            "output review, while remaining ready to learn Yodo1's specific tools."
        ),
    },
    {
        "order": 7,
        "slug": "05_ElevenLabs_Talent_Operations",
        "company": "ElevenLabs",
        "role": "Talent Operations",
        "url": "https://jobs.ashbyhq.com/elevenlabs/abc4a773-7529-497d-90e0-ff60dbf7b14e",
        "platform": "Ashby",
        "format": PDF_FORMAT,
        "fit": "High-value stretch",
        "status": "Apply after top four",
        "headline": "TALENT OPERATIONS | RECRUITMENT SUPPORT | AI-ASSISTED WORKFLOWS",
        "summary": (
            "MHRM candidate with approximately one year of post-internship HR Operations experience, "
            "recruitment-and-selection exposure, and a B.A. in Economics. Combines independent follow-through, "
            "structured HR documentation, employee communication, HR analytics coursework, and hands-on use "
            "of Claude, ChatGPT Codex, and Visual Studio Code. Interested in building accurate, scalable, "
            "candidate-focused Talent Operations processes in a global AI company."
        ),
        "skills": [
            "Recruitment and selection exposure",
            "Talent-process documentation and information organisation",
            "Candidate-experience and employee-engagement awareness",
            "HR analytics and performance-management coursework",
            "AI-assisted research, drafting, and output review",
            "Microsoft Excel, Word, and PowerPoint",
            "Communication, teamwork, and critical thinking",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "uci", "performance", "powerbi"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "ElevenLabs is a fast-scaling voice-AI company. Its Talent Operations role values previous "
            "Talent exposure, strong project organisation, rapid adoption of recruiting systems, data and "
            "dashboard thinking, process automation, and the ability to code or use AI-assisted coding tools."
        ),
        "gaps": [
            "No verified ATS administration, Ashby experience, recruiting metrics, or production automation.",
            "Hands-on Codex/VS Code use should not be described as software-development employment.",
            "Competition will include candidates with direct high-growth technology recruiting experience.",
        ],
        "keywords": [
            "Talent Operations", "recruiting operations", "candidate experience", "ATS", "Ashby",
            "process improvement", "automation", "data", "dashboards", "project management",
            "stakeholder management", "AI-assisted coding",
        ],
        "pitch": (
            "I bring approximately one year of HR Operations experience in a lean 70-person organisation, "
            "alongside recruitment-and-selection exposure, an MHRM, and HR analytics coursework. The role "
            "has developed careful coordination, documentation, employee communication, and follow-through. "
            "I use Claude, ChatGPT Codex, and VS Code for structured research, drafting, organisation, and "
            "output review. I have not administered Ashby or built production recruiting automations, but I "
            "offer relevant Talent-function exposure and a strong base for mastering those systems."
        ),
    },
    {
        "order": 8,
        "slug": "06_Meridial_Investment_AI_Trainer",
        "company": "Meridial",
        "role": "Investment Specialist – Freelance AI Trainer",
        "url": "https://job-boards.greenhouse.io/agency/jobs/4784904101",
        "platform": "Greenhouse",
        "format": GREENHOUSE_FORMAT,
        "fit": "Moderate academic fit",
        "status": "Apply after business-management role",
        "headline": "ECONOMICS & BUSINESS AI EVALUATION | STRUCTURED ANALYSIS",
        "summary": (
            "Economics graduate pursuing a Master of Human Resource Management, with structured "
            "business-plan learning, approximately one year of HR Operations experience, and coursework in "
            "analytics and performance measurement. Brings critical reading, logical analysis, clear written "
            "explanation, and hands-on use of Claude and ChatGPT Codex for research, drafting, information "
            "organisation, and output review. Interested in evaluating the clarity and consistency of "
            "AI-generated investment and market reasoning."
        ),
        "skills": [
            "Economics foundation and analytical reasoning",
            "Business-plan preparation process",
            "Performance measurement and analytics coursework",
            "Critical reading and structured written explanation",
            "AI-assisted research and output review",
            "Microsoft Excel, Word, and PowerPoint",
            "Careful interpretation of evidence and limitations",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "performance", "uci", "powerbi"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "This project tests AI reasoning across investments, financial markets, portfolio concepts, "
            "valuation, risk, and macroeconomic influences. It accepts entry-level applicants with "
            "economics, finance, accounting, or business foundations, but candidates with direct finance "
            "expertise will be stronger."
        ),
        "gaps": [
            "No verified professional investing, valuation, financial modelling, brokerage, or portfolio-management experience.",
            "No finance-specific certification or documented investment work sample.",
            "Apply as an economics-and-business reasoning candidate, not as an investment professional.",
        ],
        "keywords": [
            "economics", "investment reasoning", "financial markets", "risk", "portfolio concepts",
            "macroeconomic influences", "AI evaluation", "structured feedback", "analytical reasoning",
            "logical consistency", "business",
        ],
        "pitch": (
            "My strongest qualification for this project is a B.A. in Economics supported by structured "
            "business-plan learning, analytics coursework, and careful written reasoning. I use Claude and "
            "ChatGPT Codex for research, drafting, organisation, and output review, while checking claims "
            "rather than accepting model output uncritically. I do not have professional portfolio-management "
            "or brokerage experience and would not represent myself as an investment practitioner. I would "
            "contribute as an entry-level economics and business evaluator who documents logic, uncertainty, "
            "and limitations clearly."
        ),
    },
    {
        "order": 9,
        "slug": "07_Weave_TrueLark_AI_Trainer",
        "company": "Weave / TrueLark",
        "role": "AI Trainer",
        "url": "https://jobs.ashbyhq.com/weave/15e0f8bd-ad1e-47ec-9001-e3c72e8bea4e",
        "platform": "Ashby",
        "format": PDF_FORMAT,
        "fit": "Experience-gap stretch",
        "status": "Apply selectively",
        "headline": "AI RESPONSE REVIEW | WRITTEN QUALITY | CUSTOMER-EXPERIENCE MINDSET",
        "summary": (
            "MHRM candidate with a B.A. in Economics, approximately one year of HR Operations experience, "
            "and hands-on use of Claude and ChatGPT Codex for research, drafting, information organisation, "
            "and output review. Brings employee-communication experience, clear writing, careful attention "
            "to detail, analytical coursework, and an interest in improving the accuracy, tone, and "
            "usefulness of AI-supported customer interactions."
        ),
        "skills": [
            "AI-assisted drafting and output review",
            "Clear written communication and information organisation",
            "Customer- and employee-experience awareness",
            "Attention to detail and critical thinking",
            "HR analytics and performance-management coursework",
            "Microsoft Excel, Word, and PowerPoint",
            "Teamwork, professional conduct, and learning agility",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["powerbi", "excel", "uci", "performance"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "TrueLark, operating within Weave, applies conversational AI to customer interactions. The AI "
            "Trainer reviews responses, documents feedback, creates natural conversational content, and "
            "helps decide when human escalation is appropriate. The role requests two to three years in AI "
            "training, customer care, chat management, or related work and requires India night/weekend flexibility."
        ),
        "gaps": [
            "No verified professional AI-training, customer-care, or chat-management experience.",
            "No Postman experience is supported by current evidence.",
            "The required two to three years makes this a genuine stretch application.",
        ],
        "keywords": [
            "AI Trainer", "response review", "customer feedback", "conversational content",
            "AI versus human escalation", "quality", "written communication", "customer experience",
            "continuous improvement", "attention to detail",
        ],
        "pitch": (
            "I bring an MHRM and Economics foundation, approximately one year of HR Operations experience, "
            "employee communication, analytics coursework, and hands-on use of Claude and ChatGPT Codex for "
            "research, drafting, organisation, and output review. I am interested in whether AI responses are "
            "clear, appropriate, useful, and ready for customer use or human escalation. I do not yet have "
            "two years of professional AI-training or chat-management experience, but I offer disciplined "
            "written review, attention to detail, and practical experience handling people-related communication."
        ),
    },
    {
        "order": 6,
        "slug": "08_Rwazi_Executive_Assistant_CEO_Office",
        "company": "Rwazi",
        "role": "Executive Assistant, CEO Office",
        "url": "https://jobs.ashbyhq.com/rwazi/376d13e5-5035-496f-9cdf-5bf548670768/",
        "platform": "Ashby",
        "format": PDF_FORMAT,
        "fit": "Analytical-background stretch",
        "status": "Apply after core roles",
        "headline": "EXECUTIVE OPERATIONS | RESEARCH | STRUCTURED DOCUMENTATION",
        "summary": (
            "MHRM candidate and Economics graduate with approximately one year of HR Operations experience "
            "in a lean, 70-person organisation. Brings management follow-up, confidential information "
            "handling, careful documentation, clear writing, independent prioritisation, and structured "
            "business-plan learning. Uses Claude, ChatGPT Codex, and Visual Studio Code for research, drafting, "
            "information organisation, and output review."
        ),
        "skills": [
            "Structured writing and document preparation",
            "Research, synthesis, and information organisation",
            "Business-plan preparation process",
            "Microsoft Word, Excel, and PowerPoint",
            "AI-assisted research, drafting, and output review",
            "Professional discretion and confidential-information awareness",
            "Communication, teamwork, and critical thinking",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["performance", "excel", "uci", "vitara"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Rwazi describes an AI-native, high-velocity environment. The CEO-office role prioritises "
            "structured notes, action tracking, planning cadence, board and executive materials, research, "
            "discretion, and low-ego support. It prefers former founder/operator experience or a strong "
            "analytical background."
        ),
        "gaps": [
            "No verified executive-calendar, inbox, board-deck, travel, or CEO-support experience.",
            "No professional consulting, finance, founder, or executive-operations role.",
            "Use the Economics and business-plan background as the analytical bridge; do not overstate executive support.",
        ],
        "keywords": [
            "Executive Assistant", "CEO Office", "executive operations", "documentation",
            "meeting notes", "action items", "planning cadence", "research", "synthesis",
            "follow-through", "discretion", "analytical reasoning",
        ],
        "pitch": (
            "My background combines approximately one year of HR Operations in a lean organisation, Economics, "
            "an MHRM, and structured business-plan learning. The role has required management follow-up, "
            "confidentiality, clear documentation, independent prioritisation, and dependable action closure. "
            "I also use Claude, ChatGPT Codex, and VS Code for research, drafting, organisation, and output "
            "review. I have not supported a CEO or board, but I offer an analytical foundation and practical "
            "experience operating in a disciplined support function."
        ),
    },
    {
        "order": 4,
        "slug": "09_VertoFX_People_Operations_Coordinator",
        "company": "VertoFX",
        "role": "People Operations Coordinator",
        "url": "https://wellfound.com/jobs/3890180-people-operations-coordinator",
        "platform": "Wellfound",
        "format": PDF_FORMAT,
        "fit": "Strong experience match; systems and location gaps",
        "status": "Apply now; confirm Pune workspace expectations",
        "headline": "PEOPLE OPERATIONS | HR DOCUMENTATION | EMPLOYEE EXPERIENCE",
        "summary": (
            "HR Operations professional with approximately one year of post-internship experience supporting "
            "a workforce of about 70 employees. Pursuing an MHRM with a B.A. in Economics; brings day-to-day "
            "HR administration, employee communication, management follow-up, organised documentation, "
            "confidentiality, and independent prioritisation. Ready to transfer this small-company ownership "
            "mindset into a fast-moving fintech People Operations environment."
        ),
        "skills": [
            "HR documentation and employee-experience exposure",
            "Recruitment and selection exposure",
            "Employee engagement and performance-evaluation exposure",
            "Information organisation and confidential-information awareness",
            "Microsoft Excel, Word, and PowerPoint",
            "HR analytics coursework",
            "AI-assisted research, drafting, and output review",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "performance", "uci", "vitara"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "VertoFX is a global cross-border payments company. The role covers employee lifecycle support, "
            "background checks, HRMS administration, benefits, internal engagement, facilities, and "
            "employee queries. The listing describes WFH flexibility but also substantial Pune workspace "
            "responsibilities, so fully remote eligibility must be confirmed."
        ),
        "gaps": [
            "No verified HRMS experience with HiBob, GreytHR, BambooHR, Keka, Darwinbox, or similar systems.",
            "No verified benefits, background-check, facilities, contract, or lifecycle-process ownership.",
            "The role may require presence in Pune despite being indexed as remote-friendly.",
        ],
        "keywords": [
            "People Operations", "employee lifecycle", "onboarding", "offboarding", "HRMS",
            "background checks", "employee engagement", "benefits", "internal communication",
            "employee queries", "documentation", "startup",
        ],
        "pitch": (
            "I have approximately one year of post-internship HR Operations experience supporting a "
            "70-person organisation, with responsibility for routine HR administration, employee communication, "
            "management follow-up, and organised documentation. That lean environment developed ownership, "
            "confidentiality, and independent prioritisation. I have not administered HiBob or another "
            "production HRMS, so I would approach that as an immediate learning priority while contributing "
            "a practical HR Operations foundation."
        ),
    },
    {
        "order": 10,
        "slug": "10_AlphaSense_People_Operations_Coordinator_Global",
        "company": "AlphaSense",
        "role": "People Operations Coordinator – Global",
        "url": "https://job-boards.greenhouse.io/alphasenseindia/jobs/" + "86324" + "53002",
        "platform": "Greenhouse",
        "format": GREENHOUSE_FORMAT,
        "fit": "Hard-requirement gap",
        "status": "Do not misstate Workday answer",
        "headline": "PEOPLE OPERATIONS | HR DOCUMENTATION | GLOBAL-SUPPORT INTEREST",
        "summary": (
            "MHRM candidate with a B.A. in Economics and approximately one year of post-internship HR "
            "Operations experience supporting a 70-person workforce. Brings day-to-day HR administration, "
            "employee communication, management follow-up, organised documentation, confidentiality, and "
            "HR analytics coursework. Interested in transferring this foundation into structured global "
            "employee-lifecycle and shared-services operations."
        ),
        "skills": [
            "HR documentation and confidential-information awareness",
            "Recruitment and selection exposure",
            "Employee engagement and performance-evaluation exposure",
            "Microsoft Excel, Word, and PowerPoint",
            "HR analytics and performance-management coursework",
            "Structured information organisation",
            "AI-assisted research, drafting, and output review",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "performance", "uci", "vitara"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "AlphaSense is an AI-driven market-intelligence company serving global enterprises. The role "
            "supports People tickets, onboarding/offboarding transactions, HCM data, compliance reporting, "
            "files, requisitions, and global People programmes. Its application explicitly asks whether the "
            "candidate has at least one year of Workday employee-lifecycle experience."
        ),
        "gaps": [
            "No verified Workday experience; answer the screening question truthfully.",
            "No verified Jira/ticketing-platform, HCM, payroll-provider, mobility-tool, or global HR support experience.",
            "The explicit one-year Workday question may automatically screen out the application.",
        ],
        "keywords": [
            "People Operations", "employee lifecycle", "Workday", "HCM", "Jira", "ticketing",
            "onboarding", "offboarding", "employee data", "compliance reporting", "global HR",
            "confidential information",
        ],
        "pitch": (
            "I have approximately one year of HR Operations experience supporting a 70-person organisation, "
            "with day-to-day administration, employee communication, management follow-up, confidentiality, "
            "and organised documentation. I am interested in developing this foundation in global People "
            "Operations. I do not have one year of Workday or Jira experience and would answer the screening "
            "question honestly. If equivalent HR Operations experience can be considered, I offer a practical "
            "base and strong commitment to learning global HCM and shared-services processes."
        ),
    },
    {
        "order": 3,
        "slug": "11_Ivy_Mobility_HR_Operations_Associate",
        "company": "Ivy Mobility",
        "role": "HR Operations – Associate",
        "url": "https://wellfound.com/jobs/3962571-hr-operations-associate-sr-associate",
        "platform": "Wellfound",
        "format": PDF_FORMAT,
        "fit": "Strong one-year experience match; HRMS gap",
        "status": "Apply as Associate, not Senior Associate",
        "headline": "HR OPERATIONS | DOCUMENTATION | EMPLOYEE-DATA ACCURACY",
        "summary": (
            "HR Operations professional with approximately one year of post-internship experience supporting "
            "a workforce of about 70 employees. Pursuing an MHRM with a B.A. in Economics; brings routine HR "
            "administration, employee communication, management follow-up, organised documentation, "
            "confidentiality, and independent prioritisation. Supported by Excel-based HR analytics and "
            "performance-management coursework."
        ),
        "skills": [
            "HR documentation and records awareness",
            "Recruitment and selection exposure",
            "Employee engagement and performance-evaluation exposure",
            "Microsoft Excel, Word, and PowerPoint",
            "HR analytics and reporting coursework",
            "Process orientation and attention to detail",
            "Communication, teamwork, and critical thinking",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "performance", "uci", "vitara"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Ivy Mobility provides enterprise SaaS and mobile solutions. The HR Operations role covers "
            "employee lifecycle transactions, letters, records, benefits, Darwinbox, reporting, organisation "
            "structures, compliance, and contract-workforce administration. Chennai is the first location "
            "preference and remote India the second."
        ),
        "gaps": [
            "No verified Darwinbox/HRMS, benefits, mediclaim, statutory-compliance, or contract-workforce experience.",
            "The candidate now meets the advertised one-year experience threshold but not the role's full systems scope.",
            "Apply only to the Associate level and do not use the Senior Associate title.",
        ],
        "keywords": [
            "HR Operations", "employee lifecycle", "HR documentation", "employee records",
            "Darwinbox", "HRMS", "MIS reporting", "benefits", "compliance", "data accuracy",
            "onboarding", "offboarding",
        ],
        "pitch": (
            "I have approximately one year of post-internship HR Operations experience supporting a workforce "
            "of about 70 employees and am applying specifically at the Associate level. My experience includes "
            "routine HR administration, employee communication, management follow-up, confidentiality, and "
            "organised documentation. I have not administered Darwinbox, benefits, or statutory processes and "
            "would not claim otherwise; I bring the advertised experience duration and a practical base for "
            "learning Ivy Mobility's structured lifecycle and HRMS environment."
        ),
    },
    {
        "order": 11,
        "slug": "12_Safeguard_Global_Revenue_Operations_Coordinator",
        "company": "Safeguard Global",
        "role": "Revenue Operations Coordinator – 6-Month Fixed Term",
        "url": "https://safeguardglobal.wd3.myworkdayjobs.com/en-US/External_Careers/job/Revenue-Operations-Coordinator---6-Months-Fixed-Term_R-106223",
        "platform": "Workday",
        "format": PDF_FORMAT,
        "fit": "Major experience and systems gap",
        "status": "Low-priority stretch",
        "headline": "REVENUE OPERATIONS | EXCEL-BASED ANALYSIS | BUSINESS REPORTING",
        "summary": (
            "Economics graduate pursuing an MHRM, with approximately one year of HR Operations experience, "
            "Excel-based HR analytics coursework, and structured business-plan learning. Brings analytical "
            "thinking, management follow-up, careful information organisation, Microsoft Office skills, clear "
            "written communication, and hands-on use of AI tools for research and output review. Interested "
            "in developing revenue-reporting, planning, and operational-analysis capability."
        ),
        "skills": [
            "Microsoft Excel-based analytics coursework",
            "Economics foundation and analytical reasoning",
            "Business-plan preparation process",
            "Structured information organisation and reporting interest",
            "Microsoft Word and PowerPoint",
            "AI-assisted research, drafting, and output review",
            "Communication, teamwork, and critical thinking",
        ],
        "experience": [MYTVS_HR_OPS, SURE],
        "learning": ["excel", "powerbi", "performance", "uci"],
        "tools": AI_TOOLS,
        "company_analysis": (
            "Safeguard Global provides global employment, payroll, and workforce services. This fixed-term "
            "role handles sales-performance reporting, Excel and Salesforce analysis, dashboards, sales "
            "compensation, forecasting, planning, data quality, and senior-stakeholder requests. It requests "
            "two to five years plus advanced Excel and basic Salesforce."
        ),
        "gaps": [
            "Approximately one year of HR Operations does not meet the requested two to five years in data analysis, finance, or reporting.",
            "No advanced Excel, Salesforce, sales compensation, forecasting, quota, or territory-planning evidence.",
            "This resume deliberately says Excel-based coursework rather than advanced proficiency.",
        ],
        "keywords": [
            "Revenue Operations", "sales performance", "reporting", "Excel", "Salesforce",
            "dashboards", "forecasting", "sales compensation", "planning", "data quality",
            "business analysis", "stakeholder communication",
        ],
        "pitch": (
            "My background combines approximately one year of HR Operations, Economics, an MHRM, Excel-based "
            "HR analytics coursework, and structured business-plan learning. The role has developed management "
            "follow-up, documentation, and independent prioritisation, but I do not have the requested two "
            "years in data analysis, Salesforce, or advanced Excel evidence. I would not misrepresent those "
            "gaps; I offer operational discipline, analytical foundations, and a strong willingness to develop "
            "the technical reporting requirements during a fixed-term assignment."
        ),
    },
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def resume_html(job: dict) -> str:
    exp_html = []
    for item in job["experience"]:
        bullets = "".join(f"<li>{esc(b)}</li>" for b in item["bullets"])
        exp_html.append(
            f"""
<div class="entry">
  <div class="entry-head"><strong>{esc(item['title'])}</strong><span>{esc(item['dates'])}</span></div>
  <div class="sub">{esc(item['org'])}</div>
  <ul>{bullets}</ul>
</div>"""
        )

    edu_html = []
    for item in EDUCATION:
        detail = f" · {esc(item['detail'])}" if item["detail"] else ""
        edu_html.append(
            f"""
<div class="entry compact">
  <div class="entry-head"><strong>{esc(item['title'])}</strong><span>{esc(item['dates'])}</span></div>
  <div class="sub">{esc(item['org'])}{detail}</div>
</div>"""
        )

    skills = " · ".join(esc(x) for x in job["skills"])
    learning = "".join(
        (
            f'<li><a href="{esc(ORACLE_BADGE_URL)}">{esc(LEARNING[x])}</a> '
            f'<a href="{esc(ORACLE_BADGE_URL)}">[Verify]</a></li>'
            if x == "oracle"
            else f"<li>{esc(LEARNING[x])}</li>"
        )
        for x in learning_keys(job)
    )

    return f"""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(CONTACT['name'].title())} — {esc(job['company'])} — {esc(job['role'])}</title>
<style type="text/css">
  @page {{ size: A4; margin: 9.5mm 12mm; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0 auto; max-width: 186mm; color: #17202b; font: 9.25pt/1.28 Arial, Helvetica, sans-serif; }}
  .header {{ text-align: center; border-bottom: 1.8px solid #254f70; padding-bottom: 5px; }}
  h1 {{ margin: 0; color: #173a56; font-size: 20.5pt; letter-spacing: .35px; }}
  .headline {{ margin: 2px 0; color: #315f7e; font-size: 9.2pt; font-weight: 700; }}
  .target {{ margin: 1px 0 3px; font-size: 8.3pt; font-weight: 700; }}
  .contact {{ font-size: 8.1pt; }}
  a {{ color: inherit; text-decoration: none; }}
  h2 {{ margin: 7px 0 3px; padding-bottom: 1.5px; border-bottom: .7px solid #7791a4; color: #173a56; font-size: 10.5pt; letter-spacing: .25px; }}
  p {{ margin: 2px 0; }}
  ul {{ margin: 2px 0 3px 15px; padding: 0; }}
  li {{ margin: 1.1px 0; }}
  .skills {{ font-size: 8.9pt; line-height: 1.3; }}
  .entry {{ break-inside: avoid; margin-bottom: 3.5px; }}
  .entry.compact {{ margin-bottom: 2px; }}
  .entry-head {{ display: flex; justify-content: space-between; gap: 10px; }}
  .entry-head span {{ white-space: nowrap; }}
  .sub {{ color: #425367; font-size: 8.6pt; }}
  .tools {{ font-size: 8.8pt; }}
</style>
</head>
<body>
<div class="header">
  <h1>{esc(CONTACT['name'])}</h1>
  <div class="headline">{esc(job['headline'])}</div>
  <div class="target">TARGET POSITION: {esc(job['role'].upper())} · {esc(job['company'].upper())}</div>
  <div class="contact">
    {esc(CONTACT['location'])} · Contact via LinkedIn<br>
    <a href="{esc(CONTACT['linkedin_url'])}">{esc(CONTACT['linkedin'])}</a>
  </div>
</div>
<h2>PROFESSIONAL PROFILE</h2>
<p>{esc(job['summary'])}</p>
<h2>ROLE-RELEVANT CAPABILITIES</h2>
<p class="skills">{skills}</p>
<h2>EXPERIENCE</h2>
{''.join(exp_html)}
<h2>EDUCATION</h2>
{''.join(edu_html)}
<h2>SELECTED LEARNING</h2>
<ul>{learning}</ul>
<h2>TOOLS &amp; DIGITAL WORKFLOW</h2>
<p class="tools">{esc(job['tools'])}. Microsoft Excel, Word, and PowerPoint; introductory Power BI workshop exposure.</p>
</body>
</html>
"""


def html_to_text(source: str) -> str:
    source = re.sub(r"<style.*?</style>", "", source, flags=re.S)
    source = re.sub(r"<br\s*/?>", "\n", source, flags=re.I)
    source = re.sub(r"</(h1|h2|p|li|div|section|header|footer)>", "\n", source, flags=re.I)
    source = re.sub(r"<li>", "• ", source, flags=re.I)
    source = re.sub(r"<[^>]+>", "", source)
    source = html.unescape(source)
    lines = [re.sub(r"\s+", " ", line).strip() for line in source.splitlines()]
    return "\n".join(line for line in lines if line) + "\n"


def application_notes(job: dict) -> str:
    gaps = "\n".join(f"- {x}" for x in job["gaps"])
    keywords = ", ".join(job["keywords"])
    availability = (
        "Closed: LinkedIn currently states that this vacancy is no longer accepting applications. "
        "Retain the resume for a repost or truthful direct outreach; do not submit through the expired link."
        if job["company"] == "Unloq"
        else "Open when rechecked on 30 July 2026: the application page still displayed an Apply action."
    )
    return f"""# {job['company']} — {job['role']}

Prepared: 30 July 2026

## Live role

- Application page: {job['url']}
- Platform: {job['platform']}
- Fit assessment: {job['fit']}
- Recommended status: {job['status']}
- Availability check: {availability}

## Resume format

{job['format']}

The resume is intentionally:

- one A4 page;
- single-column in reading order;
- free of a photo, date of birth, nationality, marital status, graphics, skill bars, and tables;
- selectable and text-extractable;
- customised to the exact company and role title.

## Company and role analysis

{job['company_analysis']}

## Evidence gaps that must not be hidden

{gaps}

## ATS and recruiter language addressed

{keywords}

Keywords that are not supported by evidence may appear in this analysis, but they are not presented in
the resume as completed professional experience.

## Suggested application introduction

{job['pitch']}

## Before submitting

- [ ] Re-open the live vacancy and confirm it is still accepting applications.
- [ ] Check that the target company and role in the PDF match the application.
- [ ] Answer experience, location, shift, HRIS, ATS, CRM, and work-authorisation questions truthfully.
- [ ] Do not add Workday, Jira, Salesforce, Darwinbox, HiBob, Postman, ATS ownership, onboarding ownership,
      advanced Excel, professional AI training, or quantified achievements without evidence.
- [ ] Ensure the final signed myTVS documents support the HR Operations title, July 2025 start month,
      approximately 70-employee context, and the core duties shown in the resume.
- [ ] Review the final PDF after upload; some platforms generate their own preview.
- [ ] Keep a copy of every answer submitted.

## Optional portfolio item

The local synthetic HR analytics dashboard may be added only after the candidate independently reviews,
reproduces, and can explain its calculations, synthetic-data label, and non-causality limitation.
"""


def master_readme() -> str:
    rows = "\n".join(
        f"{j['order']}. **{j['company']} — {j['role']}**  \n"
        f"   Folder: `{j['slug']}` · {j['fit']} · {j['status']}"
        for j in sorted(JOBS, key=lambda x: x["order"])
    )
    return f"""# Remote Job Application Pack

Prepared: 30 July 2026

This folder contains 12 company- and role-specific resume packages built from the verified fact sheet
and the candidate's employment update of 30 July 2026.
Each package contains:

- an ATS-focused HTML reference file;
- a one-page upload-ready PDF produced from the same structured role data;
- a plain-text resume for ATS checks and manual form fields;
- application notes covering company fit, keywords, evidence gaps, and a suggested introduction.

## Start here

- Open `00_Ready_to_Upload/README.md` for the eleven live-role PDFs in priority order, current application
  links, and role-specific screening cautions.
- `99_Closed_or_Hold` contains the Unloq version because that listing is no longer accepting applications.

## Recommended order

{rows}

## Submission rule

Use only the PDF inside the matching company folder. Never reuse a company-labelled resume for another
employer. The text copy is not the primary visual resume.

## Evidence controls

- The MHRM is shown as 2024–2026 without claiming that a final degree or transcript has already been issued.
- The candidate directly stated that, after the internship ending 16 July 2025, he continued in HR
  Operations at myTVS for approximately one year and supported a workforce of about 70 employees.
- The resumes use `HR Operations · July 2025–Present` pending the signed experience/service certificate.
- myTVS duties are limited to the candidate-confirmed operating context and conservative core activities:
  routine HR administration, employee communication, management follow-up, documentation, confidentiality,
  independent prioritisation, and follow-through.
- AI tools are described only as hands-on use based on the candidate's direct statement.
- HRIS, ATS, CRM, payroll, Workday, Jira, Darwinbox, HiBob, Salesforce, advanced Excel, professional AI
  training, and quantified outcomes are not claimed.
- The synthetic analytics project is excluded from the resumes pending independent candidate review.

## Platform-format research

- LinkedIn recommends Microsoft Word or PDF below 2 MB:
  https://www.linkedin.com/help/linkedin/answer/a510363
- Greenhouse accepts DOC, DOCX, PDF, RTF, and TXT up to 100 MB. See the
  Greenhouse support article referenced in the private research pack.
- The generated PDF is the common submission format used across all 12 target platforms.
"""


def write_outputs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "README.md").write_text(master_readme(), encoding="utf-8")

    matrix_path = OUT / "00_Target_Job_Matrix.csv"
    with matrix_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            ["Priority", "Company", "Role", "Platform", "Fit", "Status", "Application URL", "Folder"]
        )
        for job in sorted(JOBS, key=lambda x: x["order"]):
            writer.writerow(
                [
                    job["order"], job["company"], job["role"], job["platform"], job["fit"],
                    job["status"], job["url"], job["slug"],
                ]
            )

    for job in JOBS:
        folder = OUT / job["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        base = f"Mohammad_Azimuddin_{job['company'].replace(' / ', '_').replace(' ', '_')}_{job['role']}"
        base = re.sub(r"[^A-Za-z0-9_-]+", "_", base).strip("_")
        html_path = folder / f"{base}_Resume.html"
        text_path = folder / f"{base}_Resume.txt"
        notes_path = folder / "APPLICATION_NOTES.md"
        source = resume_html(job)
        html_path.write_text(source, encoding="utf-8")
        text_path.write_text(html_to_text(source), encoding="utf-8")
        notes_path.write_text(application_notes(job), encoding="utf-8")


if __name__ == "__main__":
    write_outputs()
    print(f"Generated {len(JOBS)} targeted resume packages under {OUT}")
