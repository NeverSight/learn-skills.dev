---
name: write-guide
description: Write or change a skill, reference doc or golden path in this repo so it agrees with the concept graph and is linked to it. Use when adding or editing any SKILL.md, reference/*.md or golden path, and after adding or changing a concept so the docs that cover it are updated too. Pairs with the add-concept skill, which covers the concept files themselves.
---

# Write a guide against the concept graph

This repo has two kinds of content that must agree:

- **Concepts** (`plugins/runpod/skills/runpod-usage/concepts/*.yaml`) hold exact facts as
  rules, each citing a public source. They are the source of truth for *what is true*.
- **Guides** (every `SKILL.md`, `reference/*.md` and golden path) explain, teach and
  demonstrate. They are the source of truth for *how to do it*.

A guide states facts that the concept rules support, and links to the concepts it covers.
A concept is covered by at least one guide. `pnpm check:guides` enforces both links.

## Writing or changing a guide

1. **Find the concepts it touches** before writing (run these in `ontology/tools/`):

   ```bash
   pnpm build:sqlite
   pnpm query tree "<concept>"      # the concept, its children and the guides that cover them
   pnpm query search "<question>"   # the rules that answer a question
   pnpm query concept "<name>"      # every rule on one concept, with evidence
   ```

2. **Write from the rules.** Every factual claim (a limit, a default, a state, what an action
   does, what exists) must match a rule. Explain it in your own words and add the *how*: the
   commands, order, pitfalls and verification.
   - If the guide needs a fact that no rule has, **add the rule first** with the
     `add-concept` skill, citing the spec, the public docs or a live probe. Then write the
     guide.
   - If a rule is wrong or out of date, fix the rule (and its evidence) in the same change.
   - Never let a guide and a rule say different things. If you find a disagreement, the
     public source decides which one changes.

3. **Declare the links.**

   | Guide | Where | Example |
   |---|---|---|
   | `SKILL.md` | `metadata.concepts` in the frontmatter | `concepts: [pod, network-volume]` |
   | Reference doc | a `concepts:` line in frontmatter at the top | `---`<br>`concepts: [runpod-secret]`<br>`---` |
   | Golden path | `lanes`, `mcp` and `concepts` in frontmatter | see `plugins/runpod/skills/runpod/golden-paths/README.md` |

   List the concepts the guide actually explains or uses, not every word it mentions.
   `pnpm build:bundle --suggest` lists the concepts each golden path names, as candidates.
   A reference doc that a rule already cites as evidence is linked automatically, but list
   its concepts anyway when it covers more than the citing rules.

4. **Point to the rules** when a doc is the main explanation of a concept. End it with a short
   "Exact rules" section with a Markdown link to each concept file (from a reference doc the
   target is `../concepts/<id>.yaml`).

5. **Route it.** A new reference doc gets a row in its skill's `SKILL.md` table. A new golden
   path gets rows in the router's table and `golden-paths/README.md`.

## After adding or changing a concept

1. `pnpm check:guides` fails if the new concept has no guide. Extend an existing doc or write
   a new one, following the steps above.
2. Find the guides that already cover it and check they still agree with the rules:

   ```bash
   pnpm query tree "<concept>"                    # guides linked to it
   grep -rln "<name or alias>" ../../plugins/     # guides that mention it without a link
   ```

3. When a rule cites a skill file as evidence and you change that file, re-read the rule:
   `grep -rn "<path>" ../../plugins/runpod/skills/runpod-usage/concepts/`.

## Style

Follow `plugins/runpod/skills/runpod-usage/concepts/README.md` → "Writing style" and the
repo conventions in `AGENTS.md`: plain present tense, "Runpod", code identifiers in
backticks, no "currently" or "not yet", and positive claims over claims that something is
missing (a missing capability needs the spec or docs as evidence, and CLI absence claims are
checked by `hooks/check_cli_absence_claims.py`).

## Check

```bash
cd ontology/tools
pnpm format && pnpm validate --strict && pnpm check:guides && pnpm test
cd ../.. && python3 hooks/check_links.py && python3 hooks/check_runpod_branding.py
```

`check:guides` must report no errors, and the build line "concepts with a guide" must stay at
every concept.
