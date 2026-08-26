#!/usr/bin/env python3
"""Builds a centralized registry.json index from all SKILL.md files under skills/."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

FRONTMATTER_FENCE = "---"
KEY_LINE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(?P<value>.*)$")


def parse_frontmatter(skill_md: Path) -> dict:
    content = skill_md.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_FENCE:
        return {}

    meta: dict = {}
    body_start = 0
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == FRONTMATTER_FENCE:
            body_start = idx + 1
            break
        match = KEY_LINE.match(line)
        if match:
            k = match.group("key")
            v = match.group("value").strip()
            if v.startswith("[") and v.endswith("]"):
                # Parse list of tags
                meta[k] = [t.strip().strip("'\"") for t in v[1:-1].split(",") if t.strip()]
            else:
                meta[k] = v.strip("'\"")

    body_text = "\n".join(lines[body_start:])
    meta["chars"] = len(body_text)
    meta["words"] = len(body_text.split())
    meta["path"] = str(skill_md.parent.relative_to(skill_md.parent.parent.parent))
    return meta


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent.parent
    skills_dir = repo_root / "skills"
    
    registry: dict[str, dict] = {}
    for skill_path in sorted(skills_dir.glob("*/SKILL.md")):
        meta = parse_frontmatter(skill_path)
        if "name" in meta:
            registry[meta["name"]] = meta

    out_file = repo_root / "registry.json"
    out_file.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Compiled {len(registry)} skills into {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
