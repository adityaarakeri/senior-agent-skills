#!/usr/bin/env python3
"""Validate repository structure without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

REQUIRED_FILES = (
    "README.md",
    "RUNBOOK.md",
    "AGENTS.md",
    "install.sh",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/pull_request_template.md",
    ".github/workflows/validate.yml",
)

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()

    if not lines or lines[0] != "---":
        return {}, [f"{path.relative_to(ROOT)}: missing opening frontmatter delimiter"]

    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, [f"{path.relative_to(ROOT)}: missing closing frontmatter delimiter"]

    values: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        if ":" not in line:
            errors.append(
                f"{path.relative_to(ROOT)}:{line_number}: invalid frontmatter entry"
            )
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()

    return values, errors


def validate_skills() -> tuple[list[str], int]:
    errors: list[str] = []
    skill_dirs = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())

    if not skill_dirs:
        return ["skills/: no skill directories found"], 0

    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
            continue

        frontmatter, parse_errors = parse_frontmatter(skill_file)
        errors.extend(parse_errors)

        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")
        if name != skill_dir.name:
            errors.append(
                f"{skill_file.relative_to(ROOT)}: name '{name}' must match "
                f"folder '{skill_dir.name}'"
            )
        if not description:
            errors.append(f"{skill_file.relative_to(ROOT)}: description is required")

    return errors, len(skill_dirs)


def validate_required_files() -> list[str]:
    return [
        f"{relative}: required file is missing"
        for relative in REQUIRED_FILES
        if not (ROOT / relative).is_file()
    ]


def validate_markdown_links() -> tuple[list[str], int]:
    errors: list[str] = []
    checked = 0

    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK.finditer(text):
            target = match.group(1).strip().strip("<>")
            if (
                not target
                or target.startswith(("#", "http://", "https://", "mailto:"))
            ):
                continue

            relative_target = unquote(target.split("#", 1)[0])
            resolved = (path.parent / relative_target).resolve()
            checked += 1
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(ROOT)}: broken local link '{target}'"
                )

    return errors, checked


def main() -> int:
    errors = validate_required_files()
    skill_errors, skill_count = validate_skills()
    link_errors, link_count = validate_markdown_links()
    errors.extend(skill_errors)
    errors.extend(link_errors)

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        f"Repository validation passed: {skill_count} skills and "
        f"{link_count} local Markdown links checked."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
