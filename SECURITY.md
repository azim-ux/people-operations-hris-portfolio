# Security and privacy

This repository is a static portfolio using synthetic demonstration data. Its RBAC and governance documents describe a reference model; the site is not a production HR system and must not hold real employee records or credentials.

Public content may include the portfolio author's professional name, education and LinkedIn profile. Personal contact details, government identifiers, CV/application working files, employment documents, source evidence and credentials do not belong in the repository, including its history.

Before publishing, run `python3 scripts/security_gate.py` and the applicable project tests. The gate checks tracked paths, selected credential/PII patterns, PDF text/metadata, and executable script sources. Image pixels, arbitrary encoded data and historic commits need separate review. A passing gate is not a guarantee that all private data has been found.

Frontend scripts and generated styles are served locally from pinned packages. See [dependency notices and rebuild instructions](THIRD_PARTY_NOTICES.md).

Use a GitHub noreply email for commits and enable GitHub's email-privacy protection in account settings. Deleting a file in a new commit does not erase older history. Rotate exposed credentials before attempting historical cleanup, and coordinate any history rewrite with other clones and pull requests.

Do not paste secrets or personal details into a public issue. Use GitHub's private vulnerability reporting when it is available, or contact the maintainer privately through the professional profile linked from the portfolio.
