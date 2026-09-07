#!/usr/bin/env python3
"""Fail closed on private release files, credential patterns and remote scripts.

This is a publication regression gate, not a complete vulnerability scanner.
It prints categories and locations without printing matched private values.
"""
import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PARTS = {
    '01_Source_Evidence', '02_CV_Library', '07_Remote_Job_Applications',
    '08_Employment_Exit_Documents', '99_Archive', '.gstack', '.codex',
    '.claude', '.agents', 'node_modules', '__pycache__',
}
PRIVATE_SUFFIXES = {'.pem', '.key', '.p12', '.pfx', '.kdbx', '.keychain-db', '.docx', '.bundle', '.bak'}
PRIVATE_PREFIXES = ('Internal_Storage_Audit', 'Restored_Images_and_Study_Materials', 'Latest_CV', 'Career_Launch')
EMAIL = re.compile(r'\b[A-Z0-9._%+-]+@((?:[A-Z0-9-]+\.)+[A-Z]{2,})\b', re.I)
ALLOWED_EMAIL_DOMAINS = {'example.com', 'example.org', 'example.net', 'users.noreply.github.com', 'github.com'}
PATTERNS = {
    'private key': re.compile('-----BEGIN ' + r'(?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'GitHub token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9_]{30,}|github_pat_[A-Za-z0-9_]{40,})\b'),
    'AWS access key': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'local home path': re.compile('/' + r'Users/[A-Za-z0-9_.-]+/|[A-Z]:\\Users\\', re.I),
    'phone-like number': re.compile(r'(?<![A-Za-z0-9])[6-9]\d{9}(?![A-Za-z0-9])'),
    'PAN-like identifier': re.compile(r'\b[A-Z]{5}\d{4}[A-Z]\b'),
}


def path_findings(relative):
    p = Path(relative)
    findings = []
    if (set(p.parts) & PRIVATE_PARTS or p.suffix.lower() in PRIVATE_SUFFIXES
            or any(part.startswith(PRIVATE_PREFIXES) for part in p.parts)
            or (p.name.startswith('.env') and p.name != '.env.example')
            or p.name in {'.DS_Store', 'Thumbs.db'}):
        findings.append('private or generated release file')
    if p.parts[:1] == ('98_Maintenance',) and (
        any(word in p.name for word in ('resume', 'remote_cv', 'exit_pack', 'obsidian'))
        or p.name == 'generate_corrected_portfolio.py' or p.name.startswith('QA_REPORT_')):
        findings.append('personal career workflow')
    return findings


def text_findings(text, check_identity=True):
    findings = []
    for label, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            findings.append((label, text.count('\n', 0, match.start()) + 1))
    if check_identity:
        for match in EMAIL.finditer(text):
            domain = match.group(1).lower()
            if domain not in ALLOWED_EMAIL_DOMAINS and not domain.endswith(('.test', '.example')):
                findings.append(('non-example email', text.count('\n', 0, match.start()) + 1))
    return findings


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'script' and values.get('src'):
            self.sources.append(values['src'])


def script_findings(text, source, root):
    parser = Scripts()
    parser.feed(text)
    findings = []
    for raw in parser.sources:
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or raw.startswith('//'):
            findings.append('external executable script')
            continue
        target = (source.parent / unquote(parsed.path)).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            findings.append('missing or out-of-repository script')
    return findings


def scan(root=ROOT):
    paths = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root).decode().split('\0')
    findings = []
    for name in filter(None, paths):
        p = root / name
        findings.extend((name, 0, label) for label in path_findings(name))
        if p.is_symlink():
            findings.append((name, 0, 'tracked symlink')); continue
        if not p.is_file():
            findings.append((name, 0, 'tracked file unavailable')); continue
        try:
            if p.suffix.lower() == '.pdf':
                text = subprocess.check_output(['pdftotext', '-layout', str(p), '-'], stderr=subprocess.DEVNULL).decode(errors='replace')
                text += subprocess.check_output(['pdfinfo', str(p)], stderr=subprocess.DEVNULL).decode(errors='replace')
            elif p.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
                continue  # Image pixels require a separate visual/metadata review.
            else:
                data = p.read_bytes()
                if b'\0' in data:
                    findings.append((name, 0, 'unexpected binary')); continue
                text = data.decode(errors='replace')
            findings.extend((name, line, label) for label, line in text_findings(text, 'vendor' not in p.parts))
            if p.suffix.lower() == '.html':
                findings.extend((name, 0, label) for label in script_findings(text, p, root))
        except (OSError, subprocess.SubprocessError):
            findings.append((name, 0, 'could not inspect file or PDF tooling unavailable'))
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    findings = scan(args.root.resolve())
    for name, line, label in findings:
        print(f'{name}:{line}: {label}')
    print(f'{"FAIL" if findings else "PASS"}: public release security gate ({len(findings)} findings)')
    return int(bool(findings))


if __name__ == '__main__':
    sys.exit(main())
