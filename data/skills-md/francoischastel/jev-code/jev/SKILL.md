---
name: jev
description: >-
  Use Jev, TypeSafe's System One classifier, whenever a coding task needs a classifier under
  the hood: labelling or routing many items (issues, files, log lines, test failures, commits,
  messages), yes/no checks with a calibrated probability (does this diff touch auth, is this
  claim supported by the log, is this failure flaky), scoring on ordered levels (severity,
  priority, quality), or ranking candidates by relevance (which file answers this question).
  Prefer it over eyeballing long lists, brittle regex heuristics, or one frontier-model call
  per item. Tools: jev_classify, jev_check, jev_score, jev_rank, jev_ask (MCP or native),
  with the `jev-code` CLI as a bash fallback. Also use when the user's own application needs
  a classifier, router, guardrail, or verifier built on TypeSafe's API or SDKs. Needs
  TYPESAFE_API_KEY.
license: MIT
compatibility: Requires Node.js 20+ and the TYPESAFE_API_KEY environment variable. Tools come from the jev-code MCP server, the Pi extension, or the jev-code CLI.
metadata:
  author: FrancoisChastel
  source: https://github.com/FrancoisChastel/jev-code
  version: "0.1.0"
---

# Jev: a classifier for coding agents

Jev is a decision model, not a text model. Give it evidence and typed questions; it returns
typed answers with calibrated probabilities in roughly 70 to 500 ms, for a fraction of a cent.
It never writes prose, so there is nothing to parse and the answer is always one of the options
you supplied. Use it for the narrow judgments inside a task while you keep control of the
workflow.

The live TypeSafe docs are the source of truth for the model, the primitives, and worked
examples: start at https://docs.typesafe.ai/llms.txt and append `.md` to any page path. This
skill gives direction; read the docs when a detail matters.

## When to reach for Jev

Reach for it when you notice yourself about to:

- Label, route, group, or triage more than a handful of items by hand.
- Write a regex or keyword heuristic to decide something semantic ("is this a flaky test?").
- Skim a long list of files, docs, or search hits to find the few that matter.
- Assert something you have not verified ("tests pass", "this is backwards compatible").
- Rate severity, priority, or quality consistently across many items.

Typical moments in a coding session: triaging CI failures, labelling a backlog of issues or
TODOs, deciding which of 40 files to open for a question, checking a PR description against
its diff, screening fetched pages for prompt injection, ordering findings by severity.

## When not to

- The answer is prose, code, or a free-form value: Jev only picks among options you give it.
- A single item where you already have the evidence in front of you and the call is obvious.
- Exact facts a lookup or a test can settle: run the test, do not ask a model.
- Anything you could not decide yourself in a second with the right context in view. Split
  such judgments into smaller questions, or reason about them yourself.

## Tools at a glance

| Tool | Use when | Returns |
| --- | --- | --- |
| `jev_classify` | Many items, one label each from your classes | label, probabilities, margin, `decision: auto\|review` per item |
| `jev_check` | Yes/no questions about one piece of evidence | probability and `verdict: yes\|no\|uncertain` per check |
| `jev_score` | Many items on one ordered scale (severity, priority) | score, nearest level, confidence, decision per item |
| `jev_rank` | Which candidates answer a question | relevance per candidate, sorted, plus `any_relevant` |
| `jev_ask` | Anything else: mixed question types over one state | raw typed answers |

If the `jev_*` tools are not in your tool list, use the CLI from bash: `jev-code classify
--input payload.json` and friends take the same JSON. See [references/cli.md](references/cli.md).
If `jev-code` is missing too, tell the user to run `npx -y @francoischastel/jev-code setup`.

## Workflow

1. **Frame the judgment.** Decide what your code (or you) will do with each answer. Pick the
   tool whose output maps directly onto that action: a Choice onto branches, a check onto an
   `if`, a score onto a threshold, a rank onto "open these".
2. **Gather raw evidence.** Pass the actual text: the diff, the log excerpt, the issue body,
   the file excerpt. Never pass your own summary or conclusion; a conclusion in the state
   biases the answer toward itself, and the confidence then means nothing.
3. **Write complete questions and classes.** Ids are for you; the model sees only
   `instructions`, `classes`, and `levels`. Say what belongs, what does not, and how
   neighbouring classes differ. Add a catch-all (`other`, `unclear`) when an item might fit
   nothing. Reference named parts of the state with backticks: `` `diff` ``, `` `items.m1` ``.
4. **Batch.** Send every item, or every question about the same evidence, in one call. All
   questions run in parallel; extra ones cost tokens, not time. Limits per call: 64 items,
   250 classes, 64 checks, 250 candidates, about 120K characters in total. Split larger sets.
5. **Act on the decision, not just the label.** `decision: auto` and `verdict: yes|no` are safe
   to act on at the default thresholds. Look at `review` and `uncertain` results yourself, or
   ask the user. Raise thresholds when a wrong answer is costly; lower them when it is cheap.
6. **Report honestly.** Tell the user what Jev decided and what you reviewed, e.g. "Jev labelled
   38 failures: 31 auto-accepted, 7 I checked by hand (5 flaky, 2 real)."

## Writing good questions and classes

- One narrow judgment per question. "Is this failure caused by a timeout?" is good; "analyse
  this failure and decide what to do" is not. Split multi-factor judgments and combine in code.
- Phrase yes/no checks so that a high probability means yes, and name the condition to test,
  not the conclusion you expect.
- Class descriptions decide borderline cases. Prefer "`bug`: existing behaviour is wrong or
  crashes; not a request for something new" over "`bug`: bugs".
- Score levels must describe concrete situations, lowest first, each standing on its own.
- A yes/no probability near 0.5 means undecided, not "medium". Use a score for degrees.
- Confidence summarises how peaked the distribution is, not whether the workflow is correct.

More detail and worked examples: [references/question-design.md](references/question-design.md).

## Recipes

Ready-made payloads for common coding-agent jobs (CI triage, issue labelling, file selection,
PR-claim verification, injection screening, severity ranking):
[references/recipes.md](references/recipes.md). Exact input and output shapes for every tool:
[references/tools.md](references/tools.md).

## When the user's code needs Jev

If the application itself needs a decision Jev can make (support routing, moderation, document
classification, ranking, verification), prototype the questions with `jev_ask` or the CLI, then
build it with the official Python or JavaScript SDK, not by shelling out to `jev-code`. Patterns,
cookbook links, judgment design, and SDK snippets, adapted from TypeSafe's own skill:
[references/building-with-typesafe.md](references/building-with-typesafe.md).

## Limits, cost, and safety

- Text only, English strongest; each item is truncated at 4000 characters (`truncated: true`
  in the result). Send excerpts that contain the deciding evidence.
- Every result includes `usage` (tokens) and `model`. Mention cost only if the user asks.
- Jev is calibrated, not infallible: typed output guarantees the interface, not the truth.
  Keep destructive actions behind your own confirmation, whatever the confidence.
- The API key is read from `TYPESAFE_API_KEY`. Never print it, and never paste it into chat.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Tool call fails with "TYPESAFE_API_KEY is not set" | Ask the user to export the key (console.typesafe.ai/keys) and restart the agent, or re-run `jev-code setup`. |
| "Request is N characters, above the budget" | Split items into batches, or shorten texts to the deciding excerpt. |
| Many `review` results | Sharpen class descriptions, add a catch-all, or pass more context. |
| `status: invalid_response` on an item | The API answered in an unexpected shape; retry once, then report it. |
| `jev-code: command not found` | `npx -y @francoischastel/jev-code doctor` works without a global install. |
