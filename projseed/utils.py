"""Shared helpers: idempotent file writes, small console utilities."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional


class WriteResult:
    OUT_OF_SCOPE = "out-of-scope"  # noqa: E741 - kept for readability
    SKIPPED = "skipped"
    WRITTEN = "written"
    OVERWRITTEN = "overwritten"


def write_file(
    path: Path,
    content: str,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> str:
    """Write ``content`` to ``path`` idempotently.

    Returns one of the WriteResult constants.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return WriteResult.SKIPPED
    if dry_run:
        return WriteResult.WRITTEN
    path.write_text(content, encoding="utf-8")
    if path.exists() and force:
        return WriteResult.OVERWRITTEN
    return WriteResult.WRITTEN


def info(msg: str) -> None:
    print(f"  • {msg}")


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def skip(msg: str) -> None:
    print(f"  - {msg} (exists, use --force to overwrite)")


def warn(msg: str) -> None:
    print(f"  ! {msg}", file=sys.stderr)


def ask_default(prompt: str, default: str) -> str:
    """Prompt the user; on EOF / non-interactive, return ``default``."""
    if not sys.stdin.isatty():
        return default
    try:
        raw = input(f"{prompt} [{default}]: ").strip()
    except EOFError:
        return default
    return raw or default


def ask_choice(prompt: str, choices: list, default: Optional[str] = None) -> str:
    """Prompt for one of ``choices``; returns the chosen value."""
    if not sys.stdin.isatty():
        if default is not None:
            return default
        return choices[0]
    hint = "/".join(choices)
    while True:
        try:
            raw = input(f"{prompt} ({hint})").strip().lower()
        except EOFError:
            return default if default is not None else choices[0]
        if not raw and default is not None:
            return default
        if raw in choices:
            return raw
        print(f"    please choose one of: {hint}")


def git_user_identity() -> str:
    """Best-effort guess of the copyright holder name from git config."""
    import subprocess

    for cmd in (
        ["git", "config", "user.name"],
        ["git", "config", "user.login"],
    ):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, text=True)
            name = out.strip()
            if name:
                return name
        except Exception:
            continue
    return os.environ.get("USER", "anonymous")
