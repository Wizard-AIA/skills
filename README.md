# Wizard Skills

A community registry of `SKILL.md` files for
[Wizard](https://github.com/Wizard-AIA/Wizard-w2) — reusable analytical
know-how the agent can retrieve, cite, and consult mid-analysis.

Install from this registry into your own Wizard install with:

```bash
python backend/main.py skills add Wizard-AIA/skills
```

(from a Wizard checkout). This walks every skill found in the repository and
lets you confirm each one individually before it's installed — pass `--yes`
to skip the per-skill confirmation. See
[Installing a Skill from GitHub](https://wizard-aia.github.io/docs/guides/installing-a-skill/)
for what that flow actually does before anything reaches the agent.

## What a skill is

A `SKILL.md` file: YAML frontmatter, then Markdown instructions.

```markdown
---
name: outlier-detection
description: Choosing a detection method that matches the data's actual distribution
tags: [outliers, anomaly-detection, statistics]
version: 1.0
---

## When to use this
...
```

The frontmatter is parsed by a **restricted YAML subset** — `key: value`,
quoted strings, and inline or block lists of strings. Nothing else: no
anchors, no aliases, no nested maps, no arbitrary types. This isn't a
missing feature, it's the whole point — Milestone 6 of Wizard's evolution
spec parses this frontmatter on files fetched from repositories the
maintainer doesn't control, and a parser that can only ever produce strings
and lists of strings can't be talked into constructing anything else.

## The one hard rule: no executable code

A skill directory may not contain a `.py`, `.pyw`, `.pyc`, `.sh`, `.bash`,
`.zsh`, `.ps1`, `.bat`, `.cmd`, `.exe`, `.dll`, `.so`, `.dylib`, or similar
file. This is enforced by both the installer (checked from the file listing,
before a single byte of content is fetched) and the loader (checked again on
load) — refused outright, naming the offending file, not silently stripped.

Any Python shown *inside* a skill's Markdown body is illustrative text only.
The only way anything derived from it ever executes is Wizard's own worker
model writing fresh code that then passes the same static guard and sandbox
as any other generated code — a skill file itself never runs.

This matters especially here: a skill installed from this registry is
untrusted text that goes straight into the manager model's prompt. If a
skill could carry code, a malicious one could try to make itself
self-propagating. It can't, by construction.

## Submitting a skill

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Examples

- [`examples/outlier-detection/`](examples/outlier-detection/) — a starter
  example in this repo, showing the format end to end.
- Wizard ships two more built in:
  [`cohort-analysis`](https://github.com/Wizard-AIA/Wizard-w2/blob/master/backend/skills/cohort-analysis/SKILL.md)
  and
  [`data-quality-triage`](https://github.com/Wizard-AIA/Wizard-w2/blob/master/backend/skills/data-quality-triage/SKILL.md) —
  read those for the level of specificity a good skill aims for: concrete
  code snippets, named failure modes, and an explicit "what to report"
  section, not general advice.

## License

Submissions to this registry are accepted under the same
[BSD 3-Clause license](LICENSE) as the core project, unless a submission
states otherwise in its own `SKILL.md`.
