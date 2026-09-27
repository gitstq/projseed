""".gitignore merge / dedupe / negation-aware utilities.

Design goals:
- Never destroy existing user content.
- Dedupe patterns that are already present (exact line match, after strip).
- Preserve negation patterns (leading "!") as their own canonical key, so a
  negation line is never dropped just because an ignore line exists.
- Append new content under a clearly labelled section header so it is easy to
  review and remove. If the section header already exists in the file, no
  duplicate header is added; only genuinely new patterns are appended.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Set


def _canonical(line: str) -> str:
    """Canonical form of a gitignore line for dedupe comparison.

    We keep the leading "!" meaningful: "!foo" and "foo" are two different
    rules, so they are compared verbatim (after whitespace strip).
    """
    return line.strip()


def existing_patterns(text: str) -> Set[str]:
    """Return the set of non-comment, non-blank canonical lines in text."""
    found: Set[str] = set()
    for raw in text.splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        found.add(s)
    return found


_SECTION_RE = re.compile(r"^#\s*---\s*projseed:\s*([A-Za-z0-9_-]+)\s*---\s*$")


def _existing_sections(text: str) -> Set[str]:
    found: Set[str] = set()
    for raw in text.splitlines():
        m = _SECTION_RE.match(raw.strip())
        if m:
            found.add(m.group(1))
    return found


def merge_into(existing_text: str, section_name: str, new_patterns: Iterable[str]) -> str:
    """Append ``new_patterns`` to ``existing_text`` idempotently.

    - Lines already present (canonical match) are skipped.
    - A labelled header comment is inserted the first time a section is seen.
      Re-running the same section never creates a duplicate header; only
      genuinely new patterns are appended.
    - If ``existing_text`` is empty, a fresh file body is produced.
    """
    have = existing_patterns(existing_text)
    sections_have = _existing_sections(existing_text)
    section_seen_before = section_name in sections_have

    additions: List[str] = []
    for raw in new_patterns:
        s = raw.strip()
        if not s:
            continue
        if s.startswith("#"):
            # If this section was already written, its header comment is
            # already in the file — don't duplicate it.
            if section_seen_before:
                continue
            additions.append(s)
            continue
        if s in have:
            continue
        additions.append(s)
        have.add(s)  # also dedupe within the incoming batch

    if not additions:
        return existing_text

    if section_seen_before:
        # No new header; just append the new patterns at the end.
        block = "\n".join(additions) + "\n"
    else:
        header = f"# --- projseed: {section_name} ---"
        block = header + "\n" + "\n".join(additions) + "\n"

    if not existing_text.strip():
        return block
    if existing_text.endswith("\n"):
        return existing_text + block
    return existing_text + "\n" + block
