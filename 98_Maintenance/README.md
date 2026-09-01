# Portfolio Maintenance and Release Safety

This directory contains deterministic portfolio generators, QA records, and automated acceptance tests. Public release checks are designed to fail on private Git exposure, PII, machine-specific paths, unsafe email domains, inconsistent governed metrics, and broken links.

## Required pre-push gate

Run from the repository root:

```bash
python3 "98_Maintenance/tests/test_git_push_safety_and_privacy.py"
```

The gate validates:

- root and live-repository ignore policies;
- simulated and live Git status, tracked files, and available history;
- public HTML, Markdown, source data, scripts, images, and PDF text;
- phone, national-ID, local-path, email-domain, and secret patterns; and
- relative links that must remain inside the approved public scope.

## Portfolio acceptance tests

```bash
python3 -m unittest discover -s "98_Maintenance/tests" -p "test_*.py" -v
```

Generators must never embed personal contact values or absolute workstation paths. Resolve workspace paths from the script location, keep public datasets synthetic, and use LinkedIn or approved non-routable example domains for contact demonstrations.
