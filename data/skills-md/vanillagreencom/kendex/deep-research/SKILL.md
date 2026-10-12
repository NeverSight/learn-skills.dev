---
name: deep-research
description: "Load for research tasks, architectural investigations, and vendor, library, or technology comparisons."
summary: "Exa-powered deep research that produces an evidence-backed findings.md report."
license: MIT
user-invocable: true
argument-hint: "report [query] --output findings.md"
dependencies:
  required: [code-quality]
  optional: [decider]
metadata:
  author: vanillagreen
  source: kendex
  repository: "https://github.com/vanillagreencom/kendex"
  bugs: "https://github.com/vanillagreencom/kendex/issues"
tags: [research]
---

<!-- kendex:project-instructions:start -->
## Project Instructions

<!-- kendex:shared-instructions:start -->
Problems with a kendex-owned skill go through `kendex report`; check ownership in the file first.
<!-- kendex:shared-instructions:end -->
<!-- kendex:project-instructions:end -->

# Deep Research

In Pi with the `web_research` tool active, use that tool, passing `outputPath` when creating a report. In every other harness, run `scripts/deep-research` with `EXA_API_KEY` set.

## Rules

- Exa is the research source. Substitute a general web search only when Exa is unavailable and the user approves the fallback.
- Write `findings.md` to the path the caller requested, exactly. Given no path, write it to `tmp/plans/<slug>-research.md`, never under a tracked `docs/` path; the full rule is `agents/planner.md` § Plan Artifacts. The report reaches other sessions as an attachment on its tracker issue.
- Research on building against another system is held to [code-quality § Over-Engineering](../code-quality/SKILL.md#over-engineering).
- Cite sources for material claims. Provider payloads go in the sidecar JSON (`findings.raw.json` beside the report by default), never inline. Sanitize evidence excerpts: source-page headings must not render as headings.
- Once the report and its sidecar exist, run `validate` and stop. No local reproduction, benchmarks, tests, code inspection, or implementation unless the caller asked for it.
- A missing `EXA_API_KEY` fails with setup instructions. Set it on this package's Customize tab in the kendex app, or by hand in the project's private env file — `.env.local` unless `KENDEX_ENV_FILE` names another. The value may be a key or a 1Password `op://vault/item/field` reference when the `op` CLI is installed and signed in.
- Every mode uses the same findings sections. Record mode and source counts in `## Research Metadata`.

## Running

```bash
.agents/skills/deep-research/scripts/deep-research report "question" --mode standard --output path/to/findings.md
.agents/skills/deep-research/scripts/deep-research report --query-file prompt.txt --context-glob 'context-*.md' --mode full --output findings.md
.agents/skills/deep-research/scripts/deep-research json "question" --output raw.json
.agents/skills/deep-research/scripts/deep-research validate findings.md findings.raw.json
.agents/skills/deep-research/scripts/deep-research doctor
```

`deep-research help` lists every flag. Exa `/search` caps the settings behind them: `numResults` 1-100, `text.maxCharacters` 1-10000, `additionalQueries` at most 10.

| Mode | Exa type | Results | Text cap | Timeout | Synthesis |
|---|---|---:|---:|---:|---|
| `lite` | `deep-lite` | 15 | 10k chars/result | 5 min | Not requested, evidence brief only |
| `standard` | `deep-reasoning` | 50 | 10k chars/result | 10 min | Requested via `outputSchema` |
| `full` | `deep-reasoning` | 100 | 10k chars/result | 30 min | Requested, per query |

`standard` is the default; `lite` for fast spikes, `full` for strategic or high-risk decisions. `--type`, `--num-results`, and `--text-max-characters` override a mode's defaults.

`--additional-query` (repeatable) reaches Exa as `additionalQueries` within the single request under `lite` and `standard`, and as one request per query with URLs deduped across responses under `full`.

`--include-domain` is a hard host filter, not a quality filter: `--include-domain github.com` admits every repo on it and excludes everything else. Name authoritative projects and organizations in the query text for quality; audit the returned source list either way.

## Validation

```bash
.agents/skills/deep-research/scripts/deep-research validate path/to/findings.md path/to/findings.raw.json
```

Prints `{ok, errors, warnings, mode, synthesis, queryCount}`; exits 0 when there are no errors. Checks structure only: required sections present, sidecar parses, query-expansion metadata self-consistent, synthesized answer present for modes that requested one.

Read for these yourself:

- Claims the cited sources contradict. Spot-check material numbers against the sidecar source text.
- Off-topic sources that share an acronym or name with the subject.
- Recommendations with no claim-level support in Evidence and Sources.
- Results generalized past what the source established.

## Findings format

`templates/findings.md` carries exactly the sections `validate` requires, in order. `Key Findings` holds distinct claims, not a restatement of the summary.
