# Oracle HCM Credential — CV Update QA Report

Date: 9 August 2026

## Change implemented

The following verified credential was placed first in the certification/applied-learning section of every reusable, non-archived CV:

> Oracle Fusion Cloud Applications HCM Process Essentials Certified – Rel 1 — Oracle, August 2026

The credential is presented as foundational HCM process certification. No CV claims Oracle production configuration, implementation, administration, payroll-specialist or consulting experience.

The public verification URL was supplied by the candidate and independently checked on 9 August 2026. Oracle returned HTTP 200 and the page matched Mohammad Azimuddin, the exact credential title, Oracle as issuer and 9 August 2026 as the issued date:

`https://catalog-education.oracle.com/ords/certview/sharebadge?id=EEB81659F197DAB703AB626ABED829FF6C2A0DDF27309D9C4D3690D71D2CE7A2`

The URL is embedded behind a concise `[Verify]` label so it remains clickable without placing the long address in the visible CV layout.

## Scope

- Six active country/role CVs in `02_CV_Library`, with matching HTML and PDF versions.
- Three upload-ready PDFs in `05_Ready_to_Use_Application_Pack`.
- Twelve role packages and their upload/hold copies under `07_Remote_Job_Applications/2026-07-30`.
- Twelve role packages and their priority/conditional/expired copies under `07_Remote_Job_Applications/2026-07-31_High_Paying_Early_Career`.
- Nine current role packages under `07_Remote_Job_Applications/2026-08-05_Current_High_Paying_Remote`, including their HTML, TXT, PDF, DOCX and upload-ready copies.
- Reusable generation logic in `generate_corrected_portfolio.py`, `generate_remote_targeted_resumes.py`, `render_remote_targeted_resumes_pdf.py` and `generate_aug_05_targeted_remote_cvs.py`.

The immutable original CV, `99_Archive`, retired CVs and pre-correction snapshots were intentionally not changed.

## Validation results

| Check | Result |
|---|---:|
| HTML/TXT CV files inspected | 72 |
| HTML/TXT files containing the credential | 72 |
| HTML CV files containing the badge hyperlink | 39 of 39 |
| PDF CV files inspected | 77 |
| PDFs containing extractable credential text | 77 |
| PDFs containing the clickable badge link | 77 of 77 |
| PDFs remaining one A4 page | 77 |
| DOCX CV files inspected | 18 |
| DOCX files containing the credential | 18 |
| DOCX files containing the clickable badge link | 18 of 18 |
| Unique DOCX originals rendered through Microsoft Word | 9 |
| Word-rendered DOCX originals remaining one A4 page | 9 |
| Word-rendered DOCX PDFs retaining the badge link | 9 of 9 |
| Ready-to-upload DOCX copies matching their originals | 9 of 9 |
| Python generation/render scripts passing syntax compilation | 6 of 6 |

Representative visual inspection covered a master UAE HR CV, a dense Revenue Operations CV, a Graduate HR Generalist CV, an Everis People Operations PDF, a QuantumLoopAI Operations PDF and a Word-rendered Everis DOCX. No clipping, overlap, broken section, awkward page break or illegible credential line was found.

## Final status

Passed. The updated reusable CV set is application-ready subject to the existing evidence warnings and the normal requirement to recheck each vacancy before submission.
