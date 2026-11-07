---
name: sdlc-plan
description: >-
  Capture a new product change as a one-page intent.md: problem, outcome,
  acceptance scenarios, steps. Use for a new capability or product change, after
  exploration and before building. Bounded fixes go to sdlc-fix.
license: MIT
metadata:
  author: acourtiol
  version: "3.0"
---

# sdlc-plan

Write `intent/<slug>/intent.md` from the user's idea, in their words. One page. It is both the agreement and the checklist you will be held to.

## Triage

- A feasibility question is a spike: answer it, no intent.
- A bug, tweak, or small behavior change in an existing flow is `sdlc-fix`, no intent.
- Anything that changes what the product does is an intent. Pick the tier and write it in the frontmatter:
  - **change**: ordinary feature. One intent file, then build.
  - **critical**: consequential (migration on populated tables, auth, secrets, privacy or PII, destructive or irreversible operations, LLM prompts or gates that change generated content or approval, external sends, scraping policy). Adds a `## Spec` section to the same file and a stricter review (a missing independent reviewer blocks).
  - Both tiers get a fresh-context `sdlc-verify` after apply.
  - When unsure, take critical.

## Rules that matter

- Preserve requested outcomes. Explicit automation, named providers or integrations, and requested data coverage are requirements. A manual fallback or follow-up does not satisfy them, and nothing the user asked for moves to Out of scope without their explicit agreement.
- Do not add scope. A new screen, mandatory input, acknowledgement or gate is a product decision: trace it to something the user asked for, or present the tradeoff and let them decide.
- Size to the user: one person, one deployment. No speculative settings or extension points.
- Critical `## Spec` settles only decisions that are expensive to get wrong, citing the code you read: contracts and their callers; data and migration (additive, never edit an applied migration, how the upgrade is proven on a disposable database seeded with the previous state); persisted state after failure, retry and reload; provider errors grounded in real adapters or version-matched docs; auth, secrets, PII and what leaves the machine; rollout and rollback; open decisions, each answered by the user or a default they accept. Do not restate Acceptance.
- Acceptance covers the boundaries where defects hide: for stateful, async or external-provider outcomes add the denied, expired, failed, retried and reload cases.
- Challenge by confidence. High means: outcome and constraints explicit, current source supports the approach, contracts and failure modes have evidence, no open assumption. Then go on. Otherwise give one fresh read-only reviewer the strongest open assumption, check its citations, record what changed. Never re-challenge settled decisions.
- A broad request is split: name the first independently useful, complete delivery and write that intent. Keep the rest as a list in Out of scope or a later intent.

## Steps

1. Read the repo's instructions and `intent/*/` to see work in flight. Read code before asking anything code can answer.
2. Interview until concrete: what cannot be done today, evidence it is real (or `not checked`), who is affected, what better looks like, constraints, out of scope. One question at a time, only when the answer changes what gets built; otherwise state your assumption and go.
3. Read the code the change will touch and write `## Approach` from it: the paths that change, what is reused, what is deliberately not built, and each decision taken with its reason. The user catches over-building here, before it is built; the autonomous run uses these paths to find overlap between intents.
4. Pick a kebab-case slug not already used in `intent/`. Create `intent/<slug>/intent.md` from the template below.
5. Show the path and a short summary. The user accepts or corrects. On acceptance set `status: accepted` and commit the file. Material changes to outcome or acceptance later set it back to `draft` until re-accepted.
6. Next: `sdlc-apply`. One acceptance covers the intent and, for critical, its Spec.

## Template

```markdown
---
status: draft   # draft | accepted
tier: change    # change | critical
slug: example-slug
---

# Intent: short name

## Problem
What cannot be done today, and who feels it. Evidence it is real, or `not checked`.

## Outcome
What better looks like, observable, in the user's words. Keep short decisive quotes.

## Acceptance
- WHEN <trigger> THEN <observable result>. One line each, each checkable. Quote limits and enum values exactly.

## Approach
Paths that change. What is reused. What is deliberately not built. Decisions taken, one line each with the reason. 8 lines or fewer.

## Out of scope
Only what the user agreed to leave out.

## Steps
- [ ] First coherent slice. check: how you will know it works
- [ ] ...

## Spec (critical only)
Contracts and callers. Data and migration. Failure and retry. Security and privacy. Rollout and rollback. Open decisions.

## Result
Filled at the end: one line per Acceptance item (PASS/FAIL, evidence), plus anything not checked.
```
