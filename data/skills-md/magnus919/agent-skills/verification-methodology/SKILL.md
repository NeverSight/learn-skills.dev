---
name: verification-methodology
description: Verify work against explicit criteria using direct, source-faithful evidence, reproducible checks, and clear verdicts. Use before declaring an artifact, implementation, or claim complete; do not use for exploratory research without pass/fail criteria.
license: MIT
compatibility: No runtime dependency.
metadata:
  source_repo: https://github.com/magnus919/hermes-profiles
  source_commit: 867a555
---


# Verification Methodology

Pass/fail assessment against pre-defined criteria.

## The Verification Protocol

1. **Receive** — restate the artifact, claim, or implementation being verified and the decision it will support.
2. **Assess criteria** — convert requirements into observable pass/fail conditions; identify what would disprove each claim.
3. **Investigate** — collect direct, reproducible evidence from the source named by the request and record commands, source locations, or source URLs. Own this collection when the source is accessible: do not ask the user to relay evidence you can retrieve yourself. Ask only for access you genuinely lack.
4. **Decide** — mark each criterion passed, failed, blocked, or not applicable. Do not convert missing evidence into a pass.
   - When verification is split across lanes, no lane's PASS is the gate verdict. Wait for every required lane and reconcile conflicts before synthesis.
   - A later source-fidelity BLOCK supersedes an earlier prose, rendering, or checklist PASS for the same artifact hash. Immediately label earlier PASS packets as superseded so downstream workers cannot mistake them for the current verdict.
   - Pattern scans and internal consistency cannot substitute for checking factual transformations against the named primary source or source dossier.
5. **Report** — use the verdict template to distinguish verified facts, assumptions, and remaining work.

Stop when every criterion has direct evidence or an explicit blocked/not-applicable verdict. Escalate when the criterion is ambiguous, evidence conflicts, or the required access is unavailable.

## Source Fidelity

Treat the requested or configured local service as part of the verification criterion, not as an interchangeable topic label.

1. Load the matching skill and use its documented executable or service path before adjacent integrations, generic web search, or public project sources.
2. Use the path resolved by the skill itself. A missing global `PATH` entry does not prove that a bundled executable is unavailable.
3. If the direct source fails, report the attempted command or endpoint and its exact failure. Do not silently substitute evidence from another source.
4. Use a substitute only when the user requests broader context or explicitly accepts the fallback. Label substitute evidence as secondary and do not present it as the requested source's state.

Example: for “What’s new on Jellyfin?” in an environment with a configured Jellyfin skill and bundled CLI, query that server through the bundled CLI first. Home Assistant entities and public Jellyfin project activity answer different questions.

## When not to use

Do not use this skill for open-ended exploration that has no artifact, claim, decision, or observable completion criterion. Use a research or discovery skill first, then return here when there is something falsifiable to verify.

## Related Skills

- [playwright](../playwright/SKILL.md) — browser-based E2E checks as a verification instrument: authoring and running specs against the real UI boundary.
- [documents](../documents/SKILL.md) — producing verification reports or evidence packets as PDF/Word/Excel/PowerPoint deliverables.

## Reference Files

| Reference | When to load |
|-----------|-------------|
| `references/criteria-assessment.md` | You need to evaluate whether work meets completion criteria |
| `references/evidence-standards.md` | You need to judge whether evidence supports the claims made |
| `references/magnus919-refine-to-ship-gate.md` | You are running the Magnus919 Refine-to-Ship verifier gate — 12 criteria, editorial change verification, output structure |
| `references/verdict-template.md` | You need to produce a structured pass/fail/hold verdict |

## Magnus919 Refine-to-Ship Gate Criteria

12 criteria for the verifier profile. Each criterion maps to an observable, reproducible check.

### All 12 Criteria

| # | Criterion | How to Verify |
|---|-----------|---------------|
| 1 | **Dash scan** — zero em dash (U+2014), en dash (U+2013), horizontal bar (U+2015), or visible prose double-hyphen | `search_files` for `[\u2014\u2013\u2015]` and `\-\-`. Double-hyphens in YAML frontmatter delimiters are OK. |
| 2 | **Fact-check** — all methodology claims map to source; no fabricated numbers, chronology, or universal claims | Cross-reference article claims to source document sections. Search for `\d+%`, `percent`, `average of`, `illustrative`. Search for `research proves`, `studies demonstrate`. |
| 3 | **Voice-check** — Magnus fingerprint: conversational first-person, contractions, "But" pivots (not formal transitions), colons over semicolons, no consultant cadence | Search for `Furthermore`, `Moreover`, `Nevertheless`, `Consequently`, `Therefore`, `not only.*but also`, triplet parallelism. Count colons vs semicolons (should skew heavily toward colons). |
| 4 | **Oxford commas, spelling, grammar** — American English, Oxford commas in series, no spelling errors | Manual read of series. Check for consistent formatting. |
| 5 | **No formulaic AI closing** — zero "In conclusion", "To summarize", "In this article", generic motivational advice | `search_files` for `In conclusion`, `Ultimately,`, `To summarize`, `In this article`, `In this post`. |
| 6 | **Methodology-first** — personal frame ≤ ~10% of article; rest is methodology | Count paragraphs in frame vs body. |
| 7 | **Human stake integrated** — cognitive burden, expertise formation, transferred work, anti-surveillance, accountable authority | Verify dedicated section or dispersed coverage of all dimensions. |
| 8 | **Privacy/anonymization** — zero company identifiers, role titles, named people, source filename, proprietary domain examples | `search_files` for company name, product names, domain-specific terminology from source. |
| 9 | **Frontmatter** — title, slug, date, byline correct and value-identical to specification | `read_file` lines 1–11. |
| 10 | **Links resolve** — each distinct URL appears once at first meaningful mention; all return 200 | `curl -s -o /dev/null -w "%{http_code}"` each URL. Verify link text is at first meaningful mention. |
| 11 | **Hugo build + routes** — build exit 0; new route returns 200; old take-home-title route returns 404 | `hugo --quiet && echo EXIT:$?`. `curl` both routes. |
| 12 | **No duplicate source bundle** — single directory, single `index.md`; no stale `*take-home*` directories | `ls` the page bundle directory. `find` in content/posts for duplicate slug patterns. |

### Parent-Requested Editorial Changes

When the parent profile specifies editorial changes during gate recovery, verify each one is present before proceeding with the full criteria scan:

| Change Type | Verification Method |
|-------------|-------------------|
| Fabricated illustrative numbers removed | `search_files` for `\d+%`, `percent`, `PRs? per`, `average of` → zero hits |
| Tense correction | `search_files` for the exact parent-specified phrase |
| Closing replacement | `search_files` for the first and last sentence of the parent-specified closing |

### Verdict Rules

- **PASS:** All 12 criteria met. Produce 00-index.md, 01-summary/verdict.md, 02-analysis/per-criteria-results.md.
- **BLOCK:** Any criterion fails. Produce gap-details.md with specific fix instructions. See `verifier-gate-recovery` skill for remediation patterns.

### Output Structure

```
/private/tmp/verifier-gate/<slug>-refine/
  00-index.md              — verdict, links to artifacts
  01-summary/verdict.md    — per-criterion pass/fail table
  02-analysis/
    per-criteria-results.md  — detailed evidence per criterion
    gap-details.md           — only if BLOCK, with remediation instructions
```

## Portability

This skill is intentionally host-neutral. Use your agent's normal mechanisms to load the references, templates, and scripts listed here. Do not assume a particular profile system, task orchestrator, memory service, or response-handoff format.