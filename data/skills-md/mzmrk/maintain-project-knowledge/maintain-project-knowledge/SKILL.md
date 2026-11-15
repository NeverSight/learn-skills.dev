---
name: maintain-project-knowledge
description: Maintain compact, source-linked project memory under docs/. Use before and after changes to code, configuration, schemas, data, tooling, deployment, or workflows; when durable decisions, invariants, failure modes, or recurring traps are discovered; or when project documentation needs review, consolidation, or correction. Read the complete core memory in a fresh context, map structural changes to existing architecture, update affected knowledge, verify it against authoritative source and tests, and report when documentation impact is none.
---

# Maintain Project Knowledge

Keep accurate, compact memory that helps future agents understand the project, avoid known mistakes, and locate
authoritative source without repeating investigation.

## Boundaries

- "Primary task" means the work the user currently requested. During documentation maintenance, read any repository
  file needed as evidence, but write only under `docs/` and, when its workflow applies, the root `README.md`.
  Documentation maintenance triggered by this skill does not itself authorize other changes; separately authorized
  primary-task changes are unaffected.
- Keep the root `README.md` outside project memory, technical authority, validator scope, and the core word budget.
- Do not change code, tests, configuration, repository policy, generated artifacts, or other files solely as a
  documentation safeguard. Report the needed safeguard unless the primary task authorizes it.
- Write Markdown in English, preserving exact identifiers or source text when translation would be wrong.

## Workflow

### 1. Load the complete core

Inspect `git status --short`, relevant staged and unstaged diffs, and relevant untracked files; preserve unrelated user
changes. Inventory every `docs/**/*.md` file except Markdown under `docs/references/` and `docs/evidence/`, record line
and word counts, and read each one to confirmed EOF. `docs/README.md` is the index, not a substitute for the complete
read. If `docs/` does not exist, treat the core as empty; create `docs/README.md` only when durable knowledge must be
recorded. From the repository root, when `docs/` exists, inventory it with:

```bash
find docs -type f -name '*.md' ! -path 'docs/references/*' ! -path 'docs/evidence/*' -print | sort
find docs -type f -name '*.md' ! -path 'docs/references/*' ! -path 'docs/evidence/*' -print0 | sort -z | xargs -0 -r wc -l -w
```

Read all core documents of at most 240 lines concurrently in one bounded orchestration call, using one labeled
`sed -n '1,240p' -- <path>` command per file and an output budget of at least twice their aggregate word count. Page each
longer document separately in 240-line ranges; it must not serialize qualifying reads. Check every result and exit status.
Confirm that the final requested range reaches the recorded line count. If output is missing or truncated, resume
sequentially from the last confirmed line. Summaries, indexes, hashes, searches, or redirected output do not count as
reading the content.

Use this complete read as the context baseline. Reload it after context compaction, inventory or ownership changes,
cross-topic work, or uncertain external edits; otherwise re-read only changed or implicated documents. Read a reference
only when its indexed condition applies or while auditing references. Inspect evidence only for a claim that links to it.

### 2. Map behavior and resolve uncertainty

**Map architecture.** Before changes affecting behavior or structure, identify relevant owners, contracts, state and data
flows, dependency direction, lifecycle or persistence, and test seams as applicable. Keep existing boundaries when their
responsibilities fit; adjust them within the task’s scope when a concrete ownership problem warrants it. Add, split,
combine, or remove modules and abstractions to clarify responsibilities or contracts, weighing their benefits against
added indirection. Keep behavior easy to find and follow. Check affected producers and consumers; avoid adding unrelated
responsibilities to coordinators. Keep the investigation proportional to the task.

**Trace authoritative behavior.** Trace affected behavior through active implementation, callers, schemas, configuration,
scripts, persistence, tests, and generated contracts. Confirm plausible files are active through imports, registration,
or references. Resolve conflicts in this order:

1. Executable code, schemas, migrations, configuration, and package scripts.
2. Tests and validators demonstrating supported behavior.
3. Generated contracts, for inspection only.
4. Documentation.

Treat tests as evidence, not automatic documentation triggers. Record a test change only when it establishes or changes a
durable behavior, invariant, boundary, failure mode, or supported workflow; ignore refactors, fixtures, and coverage-only
changes. Separate implemented behavior from intended policy and current limitations from deliberate design. Claim intent
only with evidence.

**Resolve material uncertainty.** Investigate proportionately. Resolve local, reversible choices through project patterns
and engineering judgment. Ask the minimum focused questions when unresolved alternatives would materially affect the
intended outcome, scope, public behavior or contracts, security or privacy, compatibility, cost, or an irreversible
outcome. If the choice is delegated, use the best-supported option within task authority and disclose material assumptions.
Otherwise, if clarification remains unavailable, report the material choice as blocked and continue only independent work.

### 3. Maintain durable memory

Record only project-specific knowledge that is durable, non-obvious, and useful to future work: product behavior, domain
invariants, ownership, runtime and persistence flows, contracts across clients, services, data, generated artifacts, and
deployment, security, privacy, authorization, migration, backup and recovery constraints, active and inactive paths,
material failure modes, operational requirements, costly recurring traps, and decisions maintainers may revisit.

Exclude inventories, exhaustive fields or endpoints, dependency lists, obvious mechanics, temporary state, debugging
history, resolved incidents, speculation, and secrets. Link to clear source instead of copying recoverable detail. When no
durable knowledge changed, leave `docs/` untouched and report `Documentation impact: none` after verification.

Give every substantive claim one canonical owner. Update behavior, rationale, workflow, limitation, and source links
together; other documents may link briefly without maintaining a duplicate. Replace stale text rather than appending
corrections or chronology. Remove obsolete claims, resolved warnings, and duplication encountered in affected topics.
Add a document only when no existing owner remains clear, link every core document from `docs/README.md`, and update
links and ownership descriptions in `docs/README.md` when responsibilities change. Use relative links and kebab-case for
new filenames; do not rename existing files only for style.

For a recurring trap, identify the smallest enforceable safeguard—a type or schema constraint, focused test, validator,
fail-fast check, or clearer boundary. Implement it only within primary-task authority; otherwise report it. Document only
the residual invariant, limitation, or action—not incident chronology or blame—and remove the warning when enforcement
makes it obsolete. While reviewing the documentation workflow, report a cheap existing validator missing from relevant
CI; change CI only when authorized.

### 4. Maintain the public README conditionally

Treat the root `README.md` as concise onboarding for first-time human visitors. Do not load it with routine core memory.
Review it when a change affects public purpose, audience, status, URLs, installation, first use, requirements, supported
platforms, major capabilities or limitations, external services or data, privacy, security, support, contribution,
licensing, or attribution. Skip it when none of those claims can be affected.

During an authorized change or build task, update affected README claims in the same change unless the user excludes
human-facing documentation. During read-only work, report contradictions without editing them. Make the opening state:

1. What the project does and who it serves.
2. The fastest useful action: open, install, run, import, or download.
3. Any status or limitation that could change the visitor's decision.

Then include only the shortest working usage path, meaningful capabilities, essential requirements and limitations, and
relevant help, contribution, license, or attribution links. Adapt to the project type; require neither fixed headings nor
empty sections. Aim for at most 800 words and consolidate above 1,000 unless it is deliberately the primary user
documentation. Remove internal architecture, implementation rationale, exhaustive inventories, operations, and detail
better owned elsewhere. Link to useful human-facing detail, including under `docs/`, while keeping onboarding
self-contained.

Verify README claims against active source, configuration, tests, deployment, package scripts, licenses, and linked files.
Run its quick start or a safe equivalent when practical. Check links, informative-image alt text, rendered Markdown, and
prefer relative links for repository files. Report changes or unresolved contradictions.

## Memory layout

Core memory is Markdown under `docs/` except `docs/references/` and `docs/evidence/`. Keep it at or below 6,000 words;
at 5,500, warn and consolidate. Before adding words, remove stale or duplicated claims, recoverable mechanics, and detail
that source links can replace.

Use `docs/references/` only when necessary knowledge still cannot fit after consolidation and can be checked against
current authoritative sources. Move the narrowest specialist detail first; core retains the actionable conclusion, why it
matters, and the exact read condition. Never offload product scope, active behavior, ownership, security or privacy
boundaries, routine operations, or costly traps merely to meet the limit.

Keep references one level below `docs/references/`, forbid reference-to-reference dependencies, and list each under
`## Specialized references` in `docs/README.md` with a concrete read condition. Begin each reference with:

```markdown
> Non-authoritative reference.
> Core owner: [Document](../owning-document.md)
> Verify against:
> - `path/to/authoritative-source`
> Review when:
> - Concrete invalidation condition
```

Before relying on a reference, verify relevant claims against every declared source. Update or remove stale material in
the same task; if verification is impossible, treat it as uncertain. Inspect a reference when its owner or source changes.
Adding, removing, or renaming one requires reloading the complete core, reading every reference to EOF, and checking each
index entry, core owner, declared source and review condition, and the prohibition on reference dependencies. Verify
affected claims against their declared sources.

Use `docs/evidence/` only for small raw artifacts whose exact form matters, such as images, captures, exact responses, or
binary samples. Evidence is optional and non-authoritative. Link every file from the core or reference document explaining
what it supports and when to inspect it; an inventory alone is insufficient. Prefer reference Markdown when explanation
matters more than exact form. Verify evidence-derived claims against current source or label them as observations. Remove
orphaned or superseded evidence. Never store secrets, dependencies, build output, large reproducible downloads, or
temporary debugging artifacts there.

## Verify and finish

1. Re-read every changed document and README to confirmed EOF when changed.
2. Derive removed or renamed terms, paths, commands, data sources, and contracts from the diff. Search `docs/` for their
   old forms, contradictions, duplicate ownership, and stale terminology; re-read implicated surroundings.
3. Recheck claims against the authority order above. Run relevant safe tests or documented verification commands when
   practical and report important omissions. State prerequisites and working directories for commands. Give risky
   procedures verification and recovery guidance; do not execute destructive, production, or expensive commands merely
   to test prose.
4. Do not edit generated artifacts directly, including contracts, schemas, declarations, or documentation. When the
   primary task authorizes a change, inspect the generated output and modify its generator instead.
5. From the host repository root, run Node on `scripts/validate-docs.mjs` beside this `SKILL.md`, not an assumed host
   `./scripts/` path. Run `git diff --check`; review the final diff for unrelated churn, secrets, stale warnings, and
   unjustified growth.
6. Do not stage or commit unrelated changes. Follow commit authorization and message rules from the primary task or
   repository workflow. Unless commits are prohibited, include documentation in its primary-task commit and commit each
   discrete, completed, and verified change. When no message format is specified, use
   `area[,area2,area3]: intention of change and why it was done (what changed)` with at most three areas. Areas name primary
   product or system concerns, not every file category. Omit `docs`, `tests`, and generated output when they only support
   another change; use `docs` only for documentation-only commits and `tests` only when testing behavior or infrastructure
   is itself the change.
7. Report documents added, updated, consolidated, moved, or removed and why. Report observed skill contradictions,
   incorrect or ambiguous rules, unnecessary restrictions, poor task fit, repetition, or material time, context, or
   correctness costs, even when the task succeeds. Name the concrete impact and a specific improvement; do not invent
   criticism or placeholders.
