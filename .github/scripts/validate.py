#!/usr/bin/env python3
"""Validate the vibesec skill structure.

Catches the mistakes that break the skill silently:
- SKILL.md frontmatter that doesn't parse as YAML (the inline-colon gotcha)
- duplicate check IDs across checklists
- detection table pointing at a checks/ file that doesn't exist
- a checks/ file that exists but is never registered in SKILL.md
"""

import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "vibesec" / "SKILL.md"
CHECKS = ROOT / "skills" / "vibesec" / "checks"

errors = []

# 1. Frontmatter parses as YAML and has the required fields
skill_text = SKILL.read_text()
fm_match = re.match(r"^---\n(.*?)\n---\n", skill_text, re.S)
if not fm_match:
    errors.append("SKILL.md: missing YAML frontmatter block")
else:
    try:
        fm = yaml.safe_load(fm_match.group(1))
        for field in ("name", "description"):
            if not isinstance(fm.get(field), str) or not fm[field].strip():
                errors.append(f"SKILL.md frontmatter: missing or empty '{field}'")
    except yaml.YAMLError as exc:
        errors.append(f"SKILL.md frontmatter: YAML parse error: {exc}")

# 2. Check IDs are unique across all checklists
ID_RE = re.compile(r"^### ([A-Z]{1,2}-[CHML]\d+)\.")
seen = {}
for path in sorted(CHECKS.glob("*.md")):
    if path.name == "_template.md":
        continue
    for lineno, line in enumerate(path.read_text().splitlines(), 1):
        match = ID_RE.match(line)
        if match:
            check_id = match.group(1)
            if check_id in seen:
                errors.append(
                    f"{path.name}:{lineno}: duplicate check ID {check_id} "
                    f"(first seen at {seen[check_id]})"
                )
            seen[check_id] = f"{path.name}:{lineno}"
if not seen:
    errors.append("no check IDs found in checks/*.md — heading format changed?")

# 3. Every checks/ file referenced from SKILL.md exists
referenced = set(re.findall(r"`checks/([a-zA-Z0-9_-]+\.md)`", skill_text))
for name in sorted(referenced):
    if not (CHECKS / name).exists():
        errors.append(f"SKILL.md references checks/{name} which does not exist")

# 4. Every checks/ file (except the template) is registered in SKILL.md
for path in sorted(CHECKS.glob("*.md")):
    if path.name != "_template.md" and path.name not in referenced:
        errors.append(
            f"checks/{path.name} is not referenced in SKILL.md — "
            f"add it to the detection table"
        )

if errors:
    print("FAIL:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(
    f"OK: frontmatter valid, {len(seen)} unique check IDs, "
    f"{len(referenced)} checklists registered and present"
)
