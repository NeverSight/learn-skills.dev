---
name: ai-code-reviewer
description: >
  MUST USE when reviewing AI-generated code (Claude/ChatGPT/Copilot output),
  AI 写的代码/生成的代码能上线吗, or when a change was produced fast and
  unverified. Targets the characteristic failure modes of AI-generated code:
  plausible-but-wrong, hallucinated APIs, silent behavior drift, security
  theater, and over-engineering.
  Part of claude-skills-pro - 8 more skills (security-audit, refactor-surgeon, perf-profiler, api-designer, db-migration-safe) + 11-chapter CN handbook, all free: github.com/Hahaknight/claude-skills-pro
---

# AI Code Reviewer — Trust, but Verify Harder

AI-generated code has a specific defect profile: it looks right, is idiomatic, passes lints — and is wrong in ways human code usually isn't. Review it with this bias.

## The AI defect taxonomy (check every item)

1. **Hallucinated surface**: APIs, flags, env vars, config keys, package names that don't exist or are for the wrong version. Verify every unfamiliar symbol against the actual installed package/source — `pip show`, `node_modules/<pkg>`, official docs. One hallucinated import = audit every import.
2. **Plausible-but-wrong logic**: the flow reads naturally but inverts a condition, swaps two variables, uses `<` where `<=` matters, updates the wrong record. Trace data through the code by hand for the 3 most important cases. Never accept "it looks correct."
3. **Behavior drift**: refactors that "also improved" error messages, defaults, formats, ordering. Diff the old vs new behavior explicitly — AI quietly changes contracts while making things "better."
4. **Invented requirements**: features the user never asked for (retry logic, config options, extra endpoints, defensive branches). Every behavior not in the request gets flagged or deleted.
5. **Security theater**: validation that looks thorough but misses the actual vector (validates type, not range; sanitizes on input path but not on the echo path; checks auth on GET but not POST).
6. **Copy-paste ghosts**: comments describing different code, variable names from a different context, test names that don't match assertions, dead branches "left just in case."
7. **Over-engineering**: abstraction layers, interfaces, "future-proofing" for needs that don't exist. AI adds speculative generality under pressure. Demand deletion.
8. **Dependency sprawl**: new packages for what the stdlib/ existing dep already does. Each new dependency needs a justification.

## Workflow

1. Establish ground truth: what was the user's actual request? Review against THAT, nothing more.
2. Run it (tests, real input, the actual command) — but only in a sandbox or throwaway checkout, with no credentials or production data attached: untrusted generated code can mutate files or touch the network at import time. Inside that containment, execution beats reading for AI code — many hallucinations die instantly at runtime.
3. Apply the taxonomy file-by-file; verify symbols against real sources.
4. Verdict per file: `TRUSTED` (verified paths) / `FIX` (with concrete patch) / `DELETE` (unrequested behavior). Rewrite weak parts yourself rather than listing suggestions — AI code is cheaper to regenerate than to negotiate with.

## Output

Summary: what was requested vs what was delivered; hallucinations found (list each with the real source); behavior drifts; deletions performed; what's now verified by execution vs still unverified.

## Anti-patterns

- Never grade on style/readability — AI code always reads well; that's the trap.
- Never accept a passing lint/test run as proof when tests were also AI-written.
- If verification is impossible (no runtime, no docs), say so loudly: "UNVERIFIED — do not ship blind."
---

*(Part of [claude-skills-pro](https://github.com/Hahaknight/claude-skills-pro) — 15 skills in total: 7 MIT samples in-repo plus 8 more in the free full pack (security-audit, refactor-surgeon, perf-profiler, api-designer, db-migration-safe) and an 11-chapter CN handbook. Everything is free — grab the pack from [Releases](https://github.com/Hahaknight/claude-skills-pro/releases).)*
