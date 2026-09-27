"""Tech-stack detection and missing-meta-file reporting."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Tuple

# Ecosystem -> list of sentinel files/dirs that strongly suggest it is in use.
ECO_SYSTEM_MARKERS: Dict[str, List[str]] = {
    "python": ["pyproject.toml", "setup.py", "setup.cfg", "requirements.txt", "Pipfile"],
    "node": ["package.json", "yarn.lock", "pnpm-lock.yaml"],
    "go": ["go.mod", "go.sum"],
    "rust": ["Cargo.toml", "Cargo.lock"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle"],
    "docker": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
}

# Meta files a healthy repo usually has. Relative to project root.
EXPECTED_META: List[Tuple[str, str]] = [
    (".gitignore", "add general"),
    ("LICENSE", "license mit"),
    ("README.md", "readme"),
    (".editorconfig", "editorconfig"),
    ("CONTRIBUTING.md", "contributing"),
    ("CHANGELOG.md", "changelog"),
    (".github/ISSUE_TEMPLATE/bug_report.yml", "issue-templates"),
    ("PULL_REQUEST_TEMPLATE.md", "issue-templates"),
]


def detect_ecosystems(root: Path) -> List[str]:
    """Return the sorted list of ecosystems detected under ``root``."""
    found: List[str] = []
    for eco, markers in ECO_SYSTEM_MARKERS.items():
        for m in markers:
            if (root / m).exists():
                found.append(eco)
                break
    return sorted(set(found))


def missing_meta(root: Path) -> List[Tuple[str, str]]:
    """Return the list of (relative_path, subcommand) tuples for missing meta files."""
    out: List[Tuple[str, str]] = []
    for rel, sub in EXPECTED_META:
        if not (root / rel).exists():
            out.append((rel, sub))
    return out
