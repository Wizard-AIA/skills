#!/usr/bin/env python3
"""Validates every skill under skills/ and examples/ against the same rule
Wizard's own loader enforces (backend/src/core/skills/loader.py's
EXECUTABLE_SUFFIXES / offending_names) — reimplemented standalone here since
this repo has no dependency on the backend package. Two implementations of
a security boundary is two chances for them to stop agreeing, so keep this
list in sync with the source of truth by hand.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

EXECUTABLE_SUFFIXES = frozenset(
    {".py", ".pyw", ".pyc", ".sh", ".bash", ".zsh", ".ps1", ".bat", ".cmd", ".exe", ".dll", ".so", ".dylib"}
)

FRONTMATTER_FENCE = "---"
KEY_LINE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(?P<value>.*)$")
REQUIRED_KEYS = {"name", "description"}


def offending_files(skill_dir: Path) -> list[Path]:
    return [p for p in skill_dir.rglob("*") if p.is_file() and p.suffix.lower() in EXECUTABLE_SUFFIXES]


def check_frontmatter(skill_md: Path) -> list[str]:
    errors: list[str] = []
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_FENCE:
        return [f"{skill_md}: must start with a '{FRONTMATTER_FENCE}' frontmatter fence"]

    found_keys: set[str] = set()
    closed = False
    for line in lines[1:]:
        if line.strip() == FRONTMATTER_FENCE:
            closed = True
            break
        match = KEY_LINE.match(line)
        if match:
            found_keys.add(match.group("key"))
    if not closed:
        errors.append(f"{skill_md}: frontmatter block is never closed with '{FRONTMATTER_FENCE}'")

    missing = REQUIRED_KEYS - found_keys
    if missing:
        errors.append(f"{skill_md}: missing required frontmatter key(s): {', '.join(sorted(missing))}")
    return errors


def main() -> int:
    roots = [Path("skills"), Path("examples")]
    skill_dirs = [d for root in roots if root.is_dir() for d in root.iterdir() if d.is_dir()]

    if not skill_dirs:
        print("No skill directories found — nothing to validate.")
        return 0

    errors: list[str] = []
    for skill_dir in skill_dirs:
        bad_files = offending_files(skill_dir)
        if bad_files:
            names = ", ".join(str(p.relative_to(skill_dir)) for p in bad_files)
            errors.append(f"{skill_dir}: contains executable file(s) not allowed in a skill: {names}")

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill_dir}: missing SKILL.md")
            continue
        errors.extend(check_frontmatter(skill_md))

    if errors:
        print("Skill validation failed:\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"All {len(skill_dirs)} skill(s) passed validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
