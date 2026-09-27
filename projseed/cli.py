"""projseed command-line interface.

Subcommands
-----------
init              Generate a full meta-file skeleton for a new project.
add               Append ecosystem patterns to an existing .gitignore.
license           Write a LICENSE file.
readme            Write a README.md skeleton.
editorconfig      Write an .editorconfig.
contributing      Write a CONTRIBUTING.md.
changelog         Write a CHANGELOG.md (Keep a Changelog format).
issue-templates   Write GitHub issue / PR templates.
detect            Probe the current directory and report missing meta files.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence

from . import templates
from .detect import detect_ecosystems, missing_meta
from .gitignore import merge_into
from .utils import (
    WriteResult,
    ask_choice,
    ask_default,
    git_user_identity,
    info,
    ok,
    skip,
    warn,
    write_file,
)

__version__ = "1.0.0"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_gitignore(root: Path) -> str:
    p = root / ".gitignore"
    if p.exists():
        return p.read_text(encoding="utf-8")
    return ""


def _write_gitignore_for_ecosystems(
    root: Path, ecosystems: List[str], *, force: bool, dry_run: bool
) -> None:
    existing = _load_gitignore(root)
    new_text = existing
    for eco in ecosystems:
        patterns = templates.GITIGNORE_PRESETS.get(eco)
        if patterns is None:
            warn(f"unknown ecosystem: {eco} (skipped)")
            continue
        new_text = merge_into(new_text, eco, patterns)

    if new_text == existing:
        print(f"  - .gitignore: already up to date ({', '.join(ecosystems)})")
        return

    # .gitignore is a *merge* target: we never destroy user content, we only
    # append deduplicated presets. So unlike README/LICENSE etc., we always
    # write the merged text back (the merge itself is the safety mechanism).
    path = root / ".gitignore"
    if dry_run:
        ok(f".gitignore ({', '.join(ecosystems)}) [dry-run]")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_text, encoding="utf-8")
    ok(f".gitignore ({', '.join(ecosystems)})")


# ---------------------------------------------------------------------------
# Subcommand implementations
# ---------------------------------------------------------------------------

def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.out_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)

    holder = args.holder or git_user_identity()
    year = args.year or datetime.now().year
    project = args.project or root.name

    if args.ecosystems:
        ecosystems = list(args.ecosystems)
    elif args.non_interactive:
        ecosystems = ["general"]
    else:
        print("Which ecosystems does this project target?")
        print("  options: " + ", ".join(sorted(templates.GITIGNORE_PRESETS)))
        raw = input("  comma-separated [general,python]: ").strip()
        ecosystems = [e.strip() for e in raw.split(",") if e.strip()] or ["general"]

    if args.license:
        lic = args.license
    elif args.non_interactive:
        lic = "mit"
    else:
        lic = ask_choice(
            "Which license?",
            list(templates.LICENSE_BUILDERS.keys()),
            default="mit",
        )

    if lic not in templates.LICENSE_BUILDERS:
        warn(f"unknown license: {lic}")
        return 2

    info(f"project:   {project}")
    info(f"holder:    {holder}")
    info(f"year:      {year}")
    info(f"ecosystem: {', '.join(ecosystems)}")
    info(f"license:   {lic}")

    # 1. .gitignore
    _write_gitignore_for_ecosystems(root, ecosystems, force=args.force, dry_run=args.dry_run)

    # 2. LICENSE
    lic_text = templates.LICENSE_BUILDERS[lic](holder, year)
    r = write_file(root / "LICENSE", lic_text, force=args.force, dry_run=args.dry_run)
    if r == WriteResult.SKIPPED:
        skip("LICENSE")
    else:
        ok(f"LICENSE ({lic})")

    # 3. README
    r = write_file(
        root / "README.md",
        templates.readme_skeleton(project, holder, year),
        force=args.force,
        dry_run=args.dry_run,
    )
    if r == WriteResult.SKIPPED:
        skip("README.md")
    else:
        ok("README.md skeleton")

    # 4. .editorconfig
    r = write_file(
        root / ".editorconfig",
        templates.EDITORCONFIG,
        force=args.force,
        dry_run=args.dry_run,
    )
    if r == WriteResult.SKIPPED:
        skip(".editorconfig")
    else:
        ok(".editorconfig")

    # 5. CONTRIBUTING
    r = write_file(
        root / "CONTRIBUTING.md",
        templates.contributing_skeleton(project),
        force=args.force,
        dry_run=args.dry_run,
    )
    if r == WriteResult.SKIPPED:
        skip("CONTRIBUTING.md")
    else:
        ok("CONTRIBUTING.md")

    # 6. CHANGELOG
    r = write_file(
        root / "CHANGELOG.md",
        templates.changelog_skeleton(holder, year),
        force=args.force,
        dry_run=args.dry_run,
    )
    if r == WriteResult.SKIPPED:
        skip("CHANGELOG.md")
    else:
        ok("CHANGELOG.md")

    # 7. issue / PR templates
    cmd_issue_templates(args)

    ok(f"done. files are under {root}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    root = Path(args.out_dir).resolve()
    _write_gitignore_for_ecosystems(
        root, list(args.ecosystems), force=args.force, dry_run=args.dry_run
    )
    return 0


def cmd_license(args: argparse.Namespace) -> int:
    root = Path(args.out_dir).resolve()
    holder = args.holder or git_user_identity()
    year = args.year or datetime.now().year
    lic = args.license
    if lic not in templates.LICENSE_BUILDERS:
        warn(f"unknown license: {lic}. choose from {list(templates.LICENSE_BUILDERS)}")
        return 2
    text = templates.LICENSE_BUILDERS[lic](holder, year)
    r = write_file(root / "LICENSE", text, force=args.force, dry_run=args.dry_run)
    if r == WriteResult.SKIPPED:
        skip("LICENSE")
    else:
        ok(f"LICENSE ({lic}, holder={holder}, year={year})")
    return 0


def cmd_readme(args: argparse.Namespace) -> int:
    root = Path(args.out_dir).resolve()
    holder = args.holder or git_user_identity()
    year = args.year or datetime.now().year
    project = args.project or root.name
    text = templates.readme_skeleton(project, holder, year)
    r = write_file(root / "README.md", text, force=args.force, dry_run=args.dry_run)
    if r == WriteResult.SKIPPED:
        skip("README.md")
    else:
        ok("README.md skeleton")
    return 0


def cmd_editorconfig(args: argparse.Namespace) -> int:
    root = Path(args.out_dir).resolve()
    r = write_file(
        root / ".editorconfig",
        templates.EDITORCONFIG,
        force=args.force,
        dry_run=args.dry_run,
    )
    if r == WriteResult.SKIPPED:
        skip(".editorconfig")
    else:
        ok(".editorconfig")
    return 0


def cmd_contributing(args: argparse.Namespace) -> int:
    root = Path(args.out_dir).resolve()
    project = args.project or root.name
    r = write_file(
        root / "CONTRIBUTING.md",
        templates.contributing_skeleton(project),
        force=args.force,
        dry_run=args.dry_run,
    )
    if r == WriteResult.SKIPPED:
        skip("CONTRIBUTING.md")
    else:
        ok("CONTRIBUTING.md")
    return 0


def cmd_changelog(args: argparse.Namespace) -> int:
    root = Path(args.out_dir).resolve()
    holder = args.holder or git_user_identity()
    year = args.year or datetime.now().year
    r = write_file(
        root / "CHANGELOG.md",
        templates.changelog_skeleton(holder, year),
        force=args.force,
        dry_run=args.dry_run,
    )
    if r == WriteResult.SKIPPED:
        skip("CHANGELOG.md")
    else:
        ok("CHANGELOG.md")
    return 0


def cmd_issue_templates(args: argparse.Namespace) -> int:
    root = Path(args.out_dir).resolve()
    files = {
        ".github/ISSUE_TEMPLATE/bug_report.yml": templates.BUG_REPORT_YML,
        ".github/ISSUE_TEMPLATE/feature_request.yml": templates.FEATURE_REQUEST_YML,
        "PULL_REQUEST_TEMPLATE.md": templates.PR_TEMPLATE,
    }
    for rel, body in files.items():
        p = root / rel
        r = write_file(p, body, force=args.force, dry_run=args.dry_run)
        if r == WriteResult.SKIPPED:
            skip(rel)
        else:
            ok(rel)
    return 0


def cmd_detect(args: argparse.Namespace) -> int:
    root = Path(args.out_dir).resolve()
    ecos = detect_ecosystems(root)
    print(f"project root: {root}")
    if ecos:
        print("detected ecosystems: " + ", ".join(ecos))
    else:
        print("detected ecosystems: (none)")
    missing = missing_meta(root)
    if not missing:
        ok("all expected meta files are present.")
        return 0
    print("missing meta files:")
    for rel, sub in missing:
        print(f"  - {rel}   (run: projseed {sub})")
    return 1


# ---------------------------------------------------------------------------
# Argparse wiring
# ---------------------------------------------------------------------------

def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--out-dir", default=".", help="project root (default: current dir)")
    p.add_argument("--force", action="store_true", help="overwrite existing files")
    p.add_argument("--dry-run", action="store_true", help="show what would be written")
    p.add_argument("--holder", help="copyright holder name (defaults to git user.name)")
    p.add_argument("--year", type=int, help="copyright year (defaults to current year)")
    p.add_argument("--project", help="project name used in README / CONTRIBUTING")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="projseed",
        description="Zero-dependency CLI that scaffolds the meta files a repo needs.",
    )
    parser.add_argument("--version", action="version", version=f"projseed {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="generate the full meta-file skeleton")
    p_init.add_argument(
        "ecosystems",
        nargs="*",
        help="ecosystem presets, e.g. python node go rust java docker general",
    )
    p_init.add_argument("--license", help="license template: mit|isc|bsd-2|apache-2.0")
    p_init.add_argument(
        "--non-interactive",
        action="store_true",
        help="never prompt; use flags or sensible defaults",
    )
    _add_common(p_init)
    p_init.set_defaults(func=cmd_init)

    p_add = sub.add_parser("add", help="append ecosystem patterns to .gitignore")
    p_add.add_argument("ecosystems", nargs="+", help="preset names to append")
    _add_common(p_add)
    p_add.set_defaults(func=cmd_add)

    p_lic = sub.add_parser("license", help="write a LICENSE file")
    p_lic.add_argument("license", help="mit|isc|bsd-2|apache-2.0")
    _add_common(p_lic)
    p_lic.set_defaults(func=cmd_license)

    p_readme = sub.add_parser("readme", help="write a README.md skeleton")
    _add_common(p_readme)
    p_readme.set_defaults(func=cmd_readme)

    p_ec = sub.add_parser("editorconfig", help="write an .editorconfig")
    _add_common(p_ec)
    p_ec.set_defaults(func=cmd_editorconfig)

    p_c = sub.add_parser("contributing", help="write a CONTRIBUTING.md")
    _add_common(p_c)
    p_c.set_defaults(func=cmd_contributing)

    p_cl = sub.add_parser("changelog", help="write a CHANGELOG.md")
    _add_common(p_cl)
    p_cl.set_defaults(func=cmd_changelog)

    p_it = sub.add_parser("issue-templates", help="write GitHub issue / PR templates")
    _add_common(p_it)
    p_it.set_defaults(func=cmd_issue_templates)

    p_det = sub.add_parser("detect", help="probe the current dir and report missing meta")
    _add_common(p_det)
    p_det.set_defaults(func=cmd_detect)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except KeyboardInterrupt:
        warn("interrupted")
        return 130


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
