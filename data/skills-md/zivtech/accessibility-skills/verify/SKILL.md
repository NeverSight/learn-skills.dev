---
name: verify
description: "How to verify changes in this prompt-only repo: reproduce committed evidence-harness recipes from scratch, don't re-run CI. Covers the evals/results/* harness pattern."
---

# Verifying changes in accessibility-skills

This is a prompt-only repo — most diffs are docs/skill text with no runtime surface (SKIP those).
The exception is **committed evidence harnesses** under `evals/results/<tool>/harness/`: each carries
a README whose central claim is a reproduction recipe with expected output. Verify those by
executing the recipe as a fresh consumer, never by re-running in the directory where the artifacts
were authored.

Recipe that works:

1. `mktemp -d` under the session scratchpad; follow the harness README's commands **verbatim**,
   copying any story/test artifacts from the **committed repo paths** (drift between scratchpad
   and archive is exactly what this catches).
2. Compare the run's resolved dependency versions against the README's as-run table — report drift
   even when results hold.
3. Probe beyond the happy path: extract any code snippet quoted in `.claude/skills/*/SKILL.md`
   verbatim (sed the fenced block) and run it standalone — doc snippets rot independently of
   archives. Reproduce any "measured" behavioral claims (e.g., the virtual-screen-reader
   missing-stop log-leak) in the fresh environment.

Gotchas: the user-level npm guard `min-release-age=7` blocks packages younger than 7 days — init
tools fail with a message naming the compliant pin; use that pin, never bypass the guard. Playwright
Chromium is cached machine-wide (`~/Library/Caches/ms-playwright`), so browser-mode Vitest runs need
no download. Skill mirrors (`.claude/skills/` and `.agents/skills/`) must stay identical — diff the
edited sections as part of any verification touching them.
