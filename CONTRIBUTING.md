# Contributing a skill

## Format

A skill is a directory under [`skills/`](skills/) (community submissions —
[`examples/`](examples/) holds the one starter example bundled with this
repo, kept separate so it's obviously not itself a community submission)
containing exactly one `SKILL.md`:

```markdown
---
name: your-skill-name
description: One sentence — what question or task this helps with
tags: [relevant, search, terms]
version: 1.0
---

## When to use this
...
```

- `name` should match the directory name.
- `description` is what gets matched against a user's question during
  retrieval — write it as the kind of question someone would actually ask,
  not a category label.
- The frontmatter is a **restricted YAML subset**: `key: value`, quoted
  strings, and lists of strings (inline `[a, b]` or block `- a`/`- b`).
  Nothing else parses — no nested maps, no anchors. See the root
  [README](README.md) for why.

## The one non-negotiable rule

**No executable files, anywhere in the skill's directory.** No `.py`,
`.pyw`, `.pyc`, `.sh`, `.bash`, `.zsh`, `.ps1`, `.bat`, `.cmd`, `.exe`,
`.dll`, `.so`, or `.dylib`. A PR adding one will fail
[the validation workflow](.github/workflows/validate.yml) automatically —
this isn't a style preference, it's a hard trust boundary, since a skill
installed by someone else goes straight into their agent's prompt.

Python shown *inside* `SKILL.md` as an illustrative snippet is fine and
expected — that's the whole point of a skill. What's not allowed is a
separate file that could actually run.

## What makes a good skill

Compare a skill that just restates general advice ("check for outliers
before analyzing the data") against one with actual teeth. The two examples
this registry ships —
[`examples/outlier-detection/`](examples/outlier-detection/) here, and the
built-in
[`cohort-analysis`](https://github.com/Wizard-AIA/Wizard-w2/blob/master/backend/skills/cohort-analysis/SKILL.md)
and
[`data-quality-triage`](https://github.com/Wizard-AIA/Wizard-w2/blob/master/backend/skills/data-quality-triage/SKILL.md)
skills Wizard ships with — all follow the same shape:

1. **Name the specific mistakes people actually make**, not general
   principles. "Averaging down a column mixes a mature cohort with an
   immature one" is useful; "be careful with missing data" is not.
2. **Give runnable code snippets**, with placeholder column names called out
   explicitly as placeholders.
3. **End with a "what to report" section** — the concrete things a correct
   answer needs to state (a window size, a denominator, an exclusion count),
   not just "explain your findings."

A skill that's just a restatement of a textbook chapter won't retrieve any
better than the manager model already reasons on its own — the value is in
the specific, hard-won detail.

## Submitting

1. Fork this repo.
2. Add `skills/<your-skill-name>/SKILL.md`.
3. Open a PR. The validation workflow checks the frontmatter parses and that
   no executable file is present.
4. A maintainer reviews for the "actual teeth" bar above, not just format
   validity — a skill can pass validation and still not be a good fit for
   the registry.

## License

By submitting, you agree your skill is licensed under this repo's
[BSD 3-Clause license](LICENSE), unless your `SKILL.md` states otherwise.
