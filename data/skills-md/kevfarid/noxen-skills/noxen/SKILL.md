---
name: noxen
description: >
  Use when the user asks for an overview of how the current codebase is
  built, wants to be onboarded to a repo, or asks something like "explain
  how this app works", "summarize the architecture", "walk me through this
  codebase", or "what conventions does this app use". This is the Noxen
  orchestrator — it runs every other Noxen skill's detection logic against
  the current repo and returns one consolidated summary in the
  conversation. It never writes files. For depth on a single topic once
  the overview is done, defer to that topic's own skill instead of
  re-running this one.
metadata:
  version: 1.0
  collection: noxen
---

# Noxen — App Overview (orchestrator)

Meta-skill on top of the rest of the **Noxen** collection. Every other skill in
this repo answers "how should I build X" or "where does X go" for one topic.
This one answers "how does THIS app currently do X", across every topic Noxen
covers, in a single pass.

**Output contract: ephemeral only.** This skill never creates or edits a file
in the target repo. It investigates, then replies in the conversation (plain
markdown, or an Artifact if the user wants something shareable). If the user
wants a persistent, repo-local version of this summary, that's a different
request — write it as its own reference skill for that repo instead (see how
`topcars-architecture-reference`-style skills are built), don't repurpose
this one for that.

**Describe, don't grade.** For every topic, report what the repo actually
does — file paths, real snippets, the pattern in use. Do not compare it
against what that topic's own Noxen skill prescribes, and do not flag
deviations as problems. A repo using Formik where the `forms` skill defaults
to React Hook Form is not a finding here — it's just what `forms` says in
its own section.

**Always all topics, no skipping.** Produce a section for every topic listed
below, in order, even when the repo doesn't use it. When a topic doesn't
apply, say so in one line ("No data tables in this codebase") and move on —
don't omit the heading.

## Process

1. **Check for the Next.js complement first.** Look for `next.config.*` and
   an `app/` (or `pages/`) router directory. If present, load
   `nextjs/app-router` before anything else — it changes how `architecture`
   and `react-patterns` apply (routing, Server vs. Client Components, data
   fetching). Note the delta, don't re-derive it from scratch.

2. **Walk the base topics in this fixed order** (matches the dependency
   chain in this repo's README — each topic's own skill documents its
   detection signals in more depth than this file repeats):

   1. `architecture` — folder structure, feature modules, service/adapter layers, naming
   2. `ui-architecture` — where app-wide shared components/hooks/utils live (which of its scenarios matches)
   3. `react-patterns` — component/hook/effect conventions actually in use
   4. `typescript` — strictness level, `interface` vs `type`, discriminated unions, runtime validation
   5. `forms` — which library, which schema validator, the pattern connecting them
   6. `data-fetching` — which server-state library, cache/invalidation conventions
   7. `data-table` — which table/grid library, if any
   8. `state-management` — which global client-state library, if any, and what actually lives in it
   9. `modals` — which modal system, how a modal is triggered from multiple places
   10. `styling` — which styling approach (Tailwind/CSS Modules/vanilla-extract/styled-components/...)
   11. `plugin-pattern` — any registry-style pluggable UI (look for the SDUI-adjacent pattern of `type → Component` maps)
   12. `code-constraints` — file size limits, one-component-per-file, comment style, actually enforced how (lint rule vs. convention only)
   13. `http-layer` — HTTP client(s), interceptor pipeline, where case conversion happens
   14. `auth-flow` — login/OTP/session flow, where the token lives, client vs. server token source
   15. `sdui` — any backend-driven list of typed sections, and how the type→component registry is built

3. **If the Next.js complement applies**, also cover, as sub-sections under
   a `Next.js specifics` heading at the end:
   - `nextjs/screen-config` — declarative page layout / screens-as-modals, if present
   - `nextjs/i18n` — translation strategy
   - `nextjs/feature-flags` — flag system, if present

4. **For each topic**, investigate before writing:
   - Load that topic's `SKILL.md` (and only the specific `references/*.md`
     that match what you find) as the lens for what to look for — don't
     load every reference file of every skill up front, that's most of
     this collection's content and won't fit.
   - Grep/read the actual repo for that topic's signals (config files,
     folder names, import patterns, a representative real file).
   - Write 2-5 sentences or a short bullet list: what's actually there,
     with real file paths and, where it clarifies more than prose, a short
     real snippet. This is an overview, not the deep-dive — if the user
     wants more on one topic after seeing the summary, point them at that
     topic's own skill rather than expanding inline.

5. **Large repos**: investigating 15+ topics can be a lot of tool output to
   carry at once. If context is a concern, fan investigation out across
   forks (one per topic or small topic cluster) and assemble their findings
   into the final summary yourself — the summary you hand back to the user
   is still one consolidated pass, the parallelism is just an execution
   detail.

## Output shape

A single markdown reply (or Artifact, if the user asks for something to
keep/share), structured as:

```
# <Repo name> — Architecture overview

## Next.js  (only if applicable, otherwise omit this one section, not the others)
...

## Architecture
...

## UI architecture
...

## React patterns
...

[... one section per base topic above, in order ...]

## Next.js specifics  (only if applicable)
...
```

Keep the whole thing scannable — this replaces reading 15 skills' worth of
detection checklists by hand, not the individual skills themselves.
