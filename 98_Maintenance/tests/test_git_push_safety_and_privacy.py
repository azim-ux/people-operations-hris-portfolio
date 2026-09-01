#!/usr/bin/env python3
"""Pre-push privacy, Git hygiene, and public-link acceptance tests.

The workspace root is not required to be an initialized Git repository. When it
is not, the suite creates an isolated temporary repository to prove that the
root ignore policy prevents representative confidential files from appearing in
``git status --porcelain``. Any live Git repository found inside the workspace
is audited directly for tracked, staged, and historically committed private
paths.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
ROOT_GITIGNORE = ROOT / ".gitignore"

PUBLIC_ROOTS = (
    ROOT / "06_Portfolio_Projects",
    ROOT / "98_Maintenance",
)
PUBLIC_SINGLE_FILES = (ROOT / "00_START_HERE.md",)

REQUIRED_ROOT_IGNORE_RULES = {
    ".DS_Store",
    ".DS_Store?",
    "._*",
    ".Spotlight-V100",
    ".Trashes",
    "ehthumbs.db",
    "Thumbs.db",
    ".obsidian/",
    "*.canvas",
    "graphify-out/",
    ".claude/",
    ".gstack/",
    "tmp/",
    "*.log",
    "08_Employment_Exit_Documents/",
    "01_Source_Evidence/",
    "99_Archive/",
    "09_Obsidian_Hub/",
    "07_Remote_Job_Applications/",
    "02_CV_Library/",
    "*.docx",
    "*.pdf",
    "*.zip",
    "*.tar.gz",
    "!06_Portfolio_Projects/**/*.pdf",
    "!06_Portfolio_Projects/**/slides.html",
}

REQUIRED_LIVE_REPO_IGNORE_RULES = {
    ".DS_Store",
    "Thumbs.db",
    ".obsidian/",
    "*.canvas",
    "graphify-out/",
    ".claude/",
    ".gstack/",
    "tmp/",
    "*.log",
    "*.docx",
}

FORBIDDEN_COMPONENTS = {
    "01_Source_Evidence",
    "08_Employment_Exit_Documents",
    "99_Archive",
    "09_Obsidian_Hub",
    "07_Remote_Job_Applications",
    ".obsidian",
    ".claude",
    ".gstack",
    "tmp",
    "graphify-out",
}
FORBIDDEN_FILENAMES = {".DS_Store", "Thumbs.db", "Untitled.canvas"}
FORBIDDEN_SUFFIXES = (".docx", ".zip", ".tar.gz", ".tmp", ".log")

SYNTHETIC_EMAIL_DOMAINS = {"apexprecision.test", "example.com"}
EMAIL_RE = re.compile(
    r"(?i)\b[A-Z0-9._%+-]{2,}@((?:[A-Z0-9-]{2,}\.)+[A-Z]{2,})\b"
)
PII_PATTERNS = {
    "Indian mobile number": re.compile(r"(?<!\d)[6-9]\d{9}(?!\d)"),
    "Aadhaar number": re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}\b"),
    "PAN number": re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b"),
    "passport number": re.compile(r"\b[A-Z][1-9]\d{6}\b"),
    "Emirates ID": re.compile(r"\b784[ -]?\d{4}[ -]?\d{7}[ -]?\d\b"),
}
LOCAL_PATH_RE = re.compile(
    r"(?i)(?:/" + "Users" + r"/[A-Za-z0-9._-]+(?:/[^\s'\"<>)]*)?"
    r"|[A-Z]:\\" + "Users" + r"\\[A-Za-z0-9._-]+(?:\\[^\s'\"<>)]*)?)"
)

TEXT_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".svg",
    ".txt",
    ".yaml",
    ".yml",
}


def _run(command: list[str], cwd: Path, *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=cwd,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _git_repository_roots() -> list[Path]:
    roots: list[Path] = []
    for current, directories, _files in os.walk(ROOT):
        current_path = Path(current)
        if ".git" in directories:
            roots.append(current_path)
            directories.remove(".git")
        directories[:] = [
            name
            for name in directories
            if name not in {".obsidian", ".claude", ".gstack", "graphify-out", "tmp"}
        ]
    return sorted(set(roots))


def _is_forbidden_repository_path(raw_path: str) -> bool:
    normalized = raw_path.replace("\\", "/").lstrip("./")
    path = Path(normalized)
    if any(part in FORBIDDEN_COMPONENTS for part in path.parts):
        return True
    if path.name in FORBIDDEN_FILENAMES or path.suffix == ".canvas":
        return True
    return normalized.lower().endswith(FORBIDDEN_SUFFIXES)


def _iter_public_files() -> list[Path]:
    files: set[Path] = set()
    for public_root in PUBLIC_ROOTS:
        if not public_root.exists():
            continue
        for candidate in public_root.rglob("*"):
            if not candidate.is_file():
                continue
            relative = candidate.relative_to(ROOT)
            if any(part in FORBIDDEN_COMPONENTS for part in relative.parts):
                continue
            if ".git" in relative.parts or "__pycache__" in relative.parts:
                continue
            if candidate.name in FORBIDDEN_FILENAMES:
                continue
            files.add(candidate)
    files.update(path for path in PUBLIC_SINGLE_FILES if path.is_file())
    return sorted(files)


def _extract_searchable_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        converter = shutil.which("pdftotext")
        if converter is None:
            raise AssertionError("pdftotext is required to privacy-scan public PDF content")
        result = _run([converter, "-layout", str(path), "-"], ROOT)
        if result.returncode != 0:
            raise AssertionError(f"Unable to extract text from public PDF: {path.relative_to(ROOT)}")
        return result.stdout.decode("utf-8", errors="replace")

    data = path.read_bytes()
    if path.suffix.lower() in TEXT_SUFFIXES:
        return data.decode("utf-8", errors="replace")
    # Binary compression streams produce random byte sequences that resemble
    # emails or identifiers. Scan only printable metadata-like runs instead.
    printable_runs = re.findall(rb"[\x20-\x7e]{4,}", data)
    return "\n".join(run.decode("ascii", errors="ignore") for run in printable_runs)


def _redacted_location(path: Path, text: str, match: re.Match[str]) -> str:
    line = text.count("\n", 0, match.start()) + 1
    return f"{path.relative_to(ROOT)}:{line}"


class _LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag in {"a", "area", "link"} and attributes.get("href"):
            self.targets.append(attributes["href"] or "")
        if tag in {"img", "script", "source", "video", "audio", "iframe"} and attributes.get("src"):
            self.targets.append(attributes["src"] or "")


MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\((<[^>]+>|[^)\s]+)(?:\s+['\"][^)]*['\"])?\)")


def _document_targets(path: Path, text: str) -> list[str]:
    if path.suffix.lower() == ".html":
        parser = _LinkCollector()
        parser.feed(text)
        return parser.targets
    if path.suffix.lower() == ".md":
        return [match.group(1).strip("<>") for match in MARKDOWN_LINK_RE.finditer(text)]
    return []


def _resolve_relative_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if not target or target.startswith(("#", "//")):
        return None
    split = urlsplit(target)
    if split.scheme or split.netloc or not split.path or split.path.startswith("/"):
        return None
    decoded = unquote(split.path)
    if any(token in decoded for token in ("{{", "}}", "${", "<%")):
        return None
    return (source.parent / decoded).resolve()


class GitPushSafetyAndPrivacyTests(unittest.TestCase):
    maxDiff = None

    def test_01_root_gitignore_enforces_private_public_boundary(self) -> None:
        self.assertTrue(ROOT_GITIGNORE.is_file(), ".gitignore is missing at the workspace root")
        rules = {
            line.strip()
            for line in ROOT_GITIGNORE.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertFalse(
            REQUIRED_ROOT_IGNORE_RULES - rules,
            f"Missing required root .gitignore rules: {sorted(REQUIRED_ROOT_IGNORE_RULES - rules)}",
        )

    def test_02_simulated_and_live_git_status_exclude_private_assets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="portfolio-git-safety-") as temp_directory:
            simulation = Path(temp_directory)
            shutil.copy2(ROOT_GITIGNORE, simulation / ".gitignore")
            init = _run(["git", "init", "--quiet"], simulation)
            self.assertEqual(init.returncode, 0, init.stderr.decode(errors="replace"))

            private_samples = (
                "01_Source_Evidence/degree.pdf",
                "08_Employment_Exit_Documents/salary-slip.pdf",
                "99_Archive/draft.zip",
                "09_Obsidian_Hub/notes.md",
                "07_Remote_Job_Applications/tracker.csv",
                "02_CV_Library/01_UAE/resume.html",
                "02_CV_Library/01_UAE/resume.pdf",
                ".obsidian/workspace.json",
                ".claude/settings.local.json",
                ".gstack/security-report.json",
                "tmp/runtime.log",
                "graphify-out/graph.html",
                "Untitled.canvas",
                "CipherBridge_Employment_Agreement_private.docx",
                ".DS_Store",
            )
            for relative in private_samples:
                sample = simulation / relative
                sample.parent.mkdir(parents=True, exist_ok=True)
                sample.write_text("private", encoding="utf-8")

            public_samples = (
                "06_Portfolio_Projects/04_Structured_Hiring_and_ATS_Lab/deck.pdf",
                "06_Portfolio_Projects/04_Structured_Hiring_and_ATS_Lab/slides.html",
                "98_Maintenance/tests/privacy_test.py",
                "00_START_HERE.md",
            )
            for relative in public_samples:
                sample = simulation / relative
                sample.parent.mkdir(parents=True, exist_ok=True)
                sample.write_text("public", encoding="utf-8")

            status = _run(["git", "status", "--porcelain=v1", "--untracked-files=all"], simulation)
            self.assertEqual(status.returncode, 0, status.stderr.decode(errors="replace"))
            status_text = status.stdout.decode("utf-8", errors="replace")
            for private_path in private_samples:
                self.assertNotIn(private_path, status_text, f"Private sample is visible to Git: {private_path}")
            for public_path in public_samples:
                self.assertIn(public_path, status_text, f"Public sample is unexpectedly ignored: {public_path}")

        repository_roots = _git_repository_roots()
        for repository in repository_roots:
            relative_repository = repository.relative_to(ROOT)
            local_ignore = repository / ".gitignore"
            self.assertTrue(local_ignore.is_file(), f"Live Git repository lacks .gitignore: {relative_repository}")
            local_rules = {
                line.strip()
                for line in local_ignore.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            }
            self.assertFalse(
                REQUIRED_LIVE_REPO_IGNORE_RULES - local_rules,
                f"Live repository {relative_repository} lacks local privacy rules: "
                f"{sorted(REQUIRED_LIVE_REPO_IGNORE_RULES - local_rules)}",
            )

            tracked = _run(["git", "ls-files", "-z"], repository)
            self.assertEqual(tracked.returncode, 0, tracked.stderr.decode(errors="replace"))
            tracked_paths = [item.decode("utf-8", errors="replace") for item in tracked.stdout.split(b"\0") if item]
            self.assertFalse(
                [path for path in tracked_paths if _is_forbidden_repository_path(path)],
                f"Private paths are tracked in {relative_repository}",
            )
            if repository == ROOT:
                self.assertFalse(
                    [path for path in tracked_paths if path == "02_CV_Library" or path.startswith("02_CV_Library/")],
                    "The local-only CV library is tracked in the public root repository",
                )

            status = _run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], repository)
            self.assertEqual(status.returncode, 0, status.stderr.decode(errors="replace"))
            status_entries = [item.decode("utf-8", errors="replace") for item in status.stdout.split(b"\0") if item]
            status_paths = [entry[3:] if len(entry) > 3 else entry for entry in status_entries]
            self.assertFalse(
                [path for path in status_paths if _is_forbidden_repository_path(path)],
                f"Private paths are staged or visible in Git status for {relative_repository}",
            )

            history = _run(["git", "log", "--all", "--pretty=format:", "--name-only", "-z"], repository)
            self.assertEqual(history.returncode, 0, history.stderr.decode(errors="replace"))
            history_paths = [item.decode("utf-8", errors="replace").strip() for item in history.stdout.split(b"\0") if item.strip()]
            self.assertFalse(
                [path for path in history_paths if _is_forbidden_repository_path(path)],
                f"Private paths exist in Git history for {relative_repository}",
            )

    def test_03_public_assets_contain_no_pii_local_paths_or_real_email_addresses(self) -> None:
        findings: list[str] = []
        local_username = Path.home().name
        username_re = re.compile(rf"(?i)(?<![A-Za-z0-9]){re.escape(local_username)}(?![A-Za-z0-9])")

        for path in _iter_public_files():
            text = _extract_searchable_text(path)
            for label, pattern in PII_PATTERNS.items():
                for match in pattern.finditer(text):
                    findings.append(f"{label} at {_redacted_location(path, text, match)}")
            for match in LOCAL_PATH_RE.finditer(text):
                findings.append(f"local machine path at {_redacted_location(path, text, match)}")
            for match in username_re.finditer(text):
                findings.append(f"local username at {_redacted_location(path, text, match)}")
            for match in EMAIL_RE.finditer(text):
                if match.group(1).lower() not in SYNTHETIC_EMAIL_DOMAINS:
                    findings.append(f"non-synthetic email at {_redacted_location(path, text, match)}")

        self.assertFalse(findings, "Public-scope privacy findings:\n" + "\n".join(findings))

    def test_04_public_relative_links_resolve_inside_publishable_scope(self) -> None:
        findings: list[str] = []
        public_roots = tuple(path.resolve() for path in PUBLIC_ROOTS)
        public_single_files = {path.resolve() for path in PUBLIC_SINGLE_FILES}
        root_worktree = _run(["git", "rev-parse", "--is-inside-work-tree"], ROOT)
        tracked_public_paths: set[str] | None = None
        if root_worktree.returncode == 0 and root_worktree.stdout.strip() == b"true":
            tracked = _run(["git", "ls-files", "-z"], ROOT)
            self.assertEqual(tracked.returncode, 0, tracked.stderr.decode(errors="replace"))
            tracked_public_paths = {
                item.decode("utf-8", errors="replace")
                for item in tracked.stdout.split(b"\0")
                if item
            }

        for source in _iter_public_files():
            if source.suffix.lower() not in {".html", ".md"}:
                continue
            text = _extract_searchable_text(source)
            for raw_target in _document_targets(source, text):
                target = _resolve_relative_target(source, raw_target)
                if target is None:
                    continue
                location = source.relative_to(ROOT)
                try:
                    target.relative_to(ROOT)
                except ValueError:
                    findings.append(f"{location}: link escapes the workspace: {raw_target}")
                    continue
                if not target.exists():
                    findings.append(f"{location}: broken relative link: {raw_target}")
                    continue
                target_in_public_scope = target in public_single_files or any(
                    target == public_root or public_root in target.parents for public_root in public_roots
                )
                if not target_in_public_scope:
                    findings.append(f"{location}: link leaves public scope: {raw_target}")
                    continue
                relative_target = target.relative_to(ROOT)
                if _is_forbidden_repository_path(relative_target.as_posix()):
                    findings.append(f"{location}: link targets ignored/private asset: {raw_target}")
                if target.suffix.lower() == ".pdf" and "06_Portfolio_Projects" not in relative_target.parts:
                    findings.append(f"{location}: link targets globally ignored PDF: {raw_target}")
                if (
                    tracked_public_paths is not None
                    and target.is_file()
                    and relative_target.as_posix() not in tracked_public_paths
                ):
                    findings.append(f"{location}: link target is not tracked by root Git: {raw_target}")

        self.assertFalse(findings, "Unsafe or broken public links:\n" + "\n".join(sorted(set(findings))))


if __name__ == "__main__":
    unittest.main(verbosity=2)
