---
name: setup-james-skills
description: Create or reconcile a repository's root AGENTS.md references to the tech-preferences, engineering-principles and verifiable-trust skills. Use when asked to set up, refresh or validate James's personal engineering guidance; preserve existing instructions and make repeat runs idempotent.
license: Apache-2.0
metadata:
  author: jamespegg
  version: "1.1.0"
---

# Setup James Skills

Reconcile **only the current repository's root `AGENTS.md`** so coding agents can discover:

- `tech-preferences` — preferred, experimental and avoided technologies;
- `engineering-principles` — design for local reasoning;
- `verifiable-trust` — independent verification and bounded AI autonomy.

This is a **mutating setup skill**. Explicit invocation authorises a bounded `AGENTS.md` change, not cross-repo changes, skill installation, or unrelated refactoring.

## Reconciliation procedure

1. Determine the repository root and read `AGENTS.md` if it exists. Inspect existing references and documented project exceptions; preserve repository-specific instructions and unrelated content.
2. Check whether all three skills are installed/discoverable in the current agent environment. Report missing skills; **do not claim installation or install silently**. References may still be written to assist future setup.
3. Find the exact marker pair `<!-- james-skills:start -->` and `<!-- james-skills:end -->`. If both appear *exactly once* in the right order, replace **only the contents of that managed block** with the canonical block below if needed. If markers are incomplete, duplicated or malformed, preserve the file and report the ambiguity rather than guessing.
4. If no managed block exists, find any equivalent existing personal-guidance section. Update that section in place where this is unambiguous to avoid duplication. Otherwise append the canonical block separated by blank lines; create root `AGENTS.md` if absent.
5. Keep all unrelated instructions untouched; avoid whole-file reformatting. Follow repository line-ending conventions and ensure a final newline.
6. Re-read and diff the result. Confirm exactly one managed block and each of the three skill references once **within the block**, with the instruction to read their full contents before implementation and pass that requirement to workers. Re-running must make no changes. Report whether created/updated/already correct, and any unavailable skills.

## Canonical managed block

Copy the following exact block, including markers:

```markdown
<!-- james-skills:start -->
## Personal engineering guidance

These skills are **standing constraints**, not alternatives to Matt Pocock's workflow. **Before implementing or changing code** (including through `/implement`, `/implement-spec`, `/tdd` or direct implementation), read the full installed content of all three:

- **`tech-preferences`** — Preferred technologies, exclusions and rules for existing architecture decisions.
- **`engineering-principles`** — Local reasoning, cohesive capabilities, clear boundaries and explicit dependencies.
- **`verifiable-trust`** — Independent verification, bounded authority and recoverability.

Apply their guidance throughout implementation and review. **Skill availability or a reference here does not mean the agent has read the skill.** Read each once per task, not at every test cycle; for trivial documentation-only work, apply guidance proportionately.

When delegating implementation, explicitly require each worker to read and apply these skills in its own context. Don't assume the parent's loaded skill content is inherited. If a skill is unavailable, say so rather than silently proceeding as if it were applied.

Documented project decisions take precedence over generic defaults. Flag meaningful deviations **before implementing**, recommend an approach and ask before changing established technology. When James chooses to retain a deviation, record the decision and don't reopen it without a request or material new evidence.

Source: [jamespegg/skills](https://github.com/jamespegg/skills).
<!-- james-skills:end -->
```

## Boundaries

- Keep references concise; don't copy skill bodies into `AGENTS.md`. The skills repository is authoritative for their content.
- Preserve project policies, existing decisions, nested `AGENTS.md` files, application code, workflows and dependencies.
- Modify only the repository explicitly in scope. Don't overwrite a documented choice to exclude these references without discussing the conflict.
- A mention in `AGENTS.md` does not itself install, load or guarantee invocation of a skill. Be transparent if the agent environment lacks skill discovery.
