---
name: using-jev
description: "Use the jev CLI when a script, pipeline, CI job, or agent workflow needs a fast typed semantic judgment instead of generated text: routing or classifying text to predefined labels, yes/no gating with calibrated probability, rating along ordered levels, ranking candidate texts, or checking a condition that would otherwise require a fragile prompt-and-parse step. Also use whenever the user mentions Jev, TypeSafe, System One, calibrated judgments, or semantic gates in automation. Do not use it for text generation, multi-step reasoning, or open-ended questions."
compatibility: "Requires the jev CLI, network access to the TypeSafe API, and an API key configured by the user with jev login. The caller's shell tool must support invoking the CLI."
---

# Using Jev for typed judgments

Jev is a decision model, not a text generator: you send a `state` (any text or JSON) plus typed `questions`, and it returns calibrated probabilities and typed answers that code can branch on. The `jev` CLI turns that into shell primitives: stable JSON on stdout, human diagnostics on stderr, and exit codes that encode outcomes.

The CLI pins the model to `jev-latest`.

## When to reach for it

Use `jev` when ordinary code needs common sense: a gate ("is this diff destructive?"), a router ("which team handles this issue?"), a ranker ("which of these docs matches the error?"), or a verifier ("does this summary match the source?"). Keep counting, arithmetic, lookups, and execution in code; ask Jev only for the semantic judgment. Do not use it to write prose, reason through multi-step problems, or answer open-ended questions — use a generational model for those.

## Exit codes are the contract

| Code | Meaning |
|---|---|
| `0` | Requests succeeded (this does not mean a judgment was "yes") |
| `1` | Usage or infrastructure error, including an assertion that cannot be evaluated |
| `2` | Batch partially succeeded (`jev map`) |
| `3` | An assertion evaluated to false |
| `130` | Interrupted |

"Cannot be evaluated" is deliberately an error, not a false: a path typo in `--assert` must block loudly rather than silently pass a gate.

## Commands

| Command | Purpose |
|---|---|
| `jev noul "Q?" [--true D] [--false D]` | One yes/no probability. Answer id is `q`. |
| `jev choice "Q?" --opt KEY=DESC ...` | Pick one option. Answer id is `q`. |
| `jev score "Q?" --level LOW --level HIGH ...` | Rate on ordered levels. Answer id is `q`. |
| `jev ask [PATH\|-] [--preset NAME]` | One full request (state + questions). |
| `jev map [PATH\|-] --in FILE` | Concurrent batch; JSONL in, JSONL out. |
| `jev presets list / show NAME / validate` | Manage request templates; no API calls. |

State comes from `--state TEXT`, `--state @PATH` (JSON files stay structured), or stdin. Every judging command accepts `--assert EXPR` to turn answers into exit code 0 or 3.

```sh
echo "$LINE" | jev noul "Does this log line indicate an OOM kill?" \
    --assert 'answers.q.noul >= 0.8'

jev score "How current is this dependency documentation?" \
    --level "Matches the API" --level "Minor drift" --level "Badly outdated" \
    --state @README.md
```

Assertions support `and`/`or`/`not`, parentheses, comparisons (`==`, `!=`, `<=`, `>=`, `<`, `>`), `in [list]`, and paths into the response envelope, including bracketed keys for level descriptions: `answers.risk.probabilities["needs human review"] >= 0.25`. Only comparisons produce booleans; there is no arithmetic — pipe through `jq` for weighted sums.

## Presets

A preset is a committed, reviewable automation asset: a JSON file in `./.jev/presets/` (repository, wins on collisions) or the user config directory. It is a request plus three reserved keys that never reach the API:

```json
{
  "description": "Gate releases on destructive-diff detection",
  "params": {"diff": "the pull request diff"},
  "state": {"diff": "{{diff}}"},
  "questions": {
    "destructive": {"type": "noul", "instructions": "Does this diff perform destructive changes?", "criteria": {"true": "Drops data, rewrites history, or force-pushes", "false": "Ordinary additive or editable changes"}}
  },
  "assert": "answers.destructive.noul <= 0.5"
}
```

`{{name}}` placeholders must fill an entire field value; pass values with `--param NAME=VALUE` or `--param NAME=@PATH` (JSON files inject as subtrees). `jev presets validate` checks structure, question shapes, and assertion syntax offline before anything costs tokens.

```sh
jev ask --preset review-gate --param diff=@pr.diff
# Explicit --assert replaces the preset default.
```

## Batches

`jev map` evaluates one template over many inputs concurrently:

```sh
jev map --preset triage --in issues.jsonl --out triaged.jsonl --concurrency 8
```

`--each state` (default) makes each JSONL line the request state; `--each text` wraps plain lines as strings; `--each request` treats each line as a complete request body — generate those with `jq` when questions must vary per row. Templates for `--each state`/`--each text` normally omit `state` entirely, since each line replaces it. Rows stream out in completion order, each tagged with its input `index`. A failed row fails alone (`{"ok":false,"error":{"kind":"api"|"network"|"usage","message":"..."}}`) and the run exits `2`. With `--out FILE` and `--resume`, a rerun skips rows that already completed `ok` — this is checkpointing, not caching; the CLI itself never memoizes results.

## Writing good questions

- Put the judgment in `instructions`; define answers in `criteria`. Question ids never reach the model.
- One narrow judgment per question. Split independent dimensions; ask independent questions together in one request — they run in parallel.
- Give complete state: the text plus any identities, policies, or facts needed to judge. Do not include irrelevant material.
- Write edge cases into criteria literally. For deletion gates, frame toward the worst case (delete only when clearly bad); when several labels may apply, use one noul per label.
- Scores need concrete, self-standing level descriptions, ordered lowest first.
- For choices, include a no-match option when nothing may fit; check that candidates actually cover the possible answers.
- Thresholds are policy: pick them for the consequences of each side, and validate on your own data. Confidence measures distribution concentration, not correctness.

## Availability and authentication

Invoke directly; the CLI prints actionable errors. Authentication comes from the `JEV_API_KEY` environment variable when set (common in CI and containers), otherwise from credentials stored by `jev login`. If authentication fails, ask the user to run `jev login` in their own terminal. Never ask them to paste an API key into the conversation. Rate limits (roughly 20 requests/second) are handled with retries and backoff; keep `--concurrency` at or below 8.
