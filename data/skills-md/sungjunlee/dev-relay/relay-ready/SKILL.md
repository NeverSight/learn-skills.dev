---
name: relay-ready
argument-hint: "[task description or readiness handoff candidate]"
description: Verify a task is ready to relay — judge readiness on clarity, granularity, and verifiability, then ask bounded questions when the task is too ambiguous to plan.
compatibility: Requires git and Node.js 18+.
metadata:
  related-skills: "relay, relay-plan, relay-dispatch, relay-review"
  keywords: "relay-ready, ready to relay, readiness gate, task readiness, 릴레이 준비, 준비도, 검증, 완료 기준"
---
## Inputs
- Env: optional `RELAY_SKILL_ROOT` defaults to `skills`.
- Files: `/tmp/relay-ready-contract.json` with request, handoff, leaf, and Done Criteria fields; generated request artifacts under `~/.relay/requests/<repo-slug>/`.
- Sibling scripts: `${RELAY_SKILL_ROOT:-skills}/relay-ready/scripts/persist-request.js`, `${RELAY_SKILL_ROOT:-skills}/relay-dispatch/scripts/dispatch.js`.

# Relay Ready

## Use when

- `/relay` cannot safely bypass straight to planning
- The request is ambiguous, too broad, or may need multiple ordered leaves
- No stable Done Criteria or review anchor exists yet

## Do not use when

- Authoring rubrics or dispatch prompts — use `relay-plan`
- Delegating implementation work — use `relay-dispatch`
- Reviewing executor output — use `relay-review`
- Landing a reviewed GitHub change — use `relay-merge`

## Readiness Judgment

No script scores readiness. Judge the request yourself against these factors,
reading only text outside fenced code blocks — a fenced example is not a signal.

- **Clarity** is low when any of these hold: a vague verb (`improve`, `enhance`,
  `clean up`, `polish`); no explicit target (no file path, no `function()`); a
  body under roughly 200 characters. It is high only when an explicit target and
  an observable end state both appear in the opening paragraph.
- **Granularity** is low when any of these hold: a top-level `and` joining two
  action clauses in the opening line; a multi-verb opener spanning more than one
  subsystem; three or more bullets across two or more modules, ignoring
  `Non-goals`, `Out of scope`, and `Tests` sections. It is high when one action
  verb acts on one subsystem.
- **Verifiability** is low when subjective wording (`feels`, `good`, `smoother`,
  `nicer`) carries the criteria, or a Done/Acceptance Criteria heading exists but
  its section states nothing observable. It is high when the text names a test
  path, a quoted log line, a file or diff target, or a numeric threshold.
- **Task shape** measures decomposition pressure. Signals: four or more criteria
  group headings or eight or more criteria bullets; sprint, epic, milestone,
  foundation, roadmap, or initiative scope language; three or more distinct
  subsystems; a multi-stage journey (flow, journey, or end-to-end wording plus
  three or more stages such as signup, onboarding, review, export); a product
  surface mixed with platform foundation terms. Two or more signals — or six or
  more criteria groups, eight or more bullets, or four or more subsystems — is a
  **strong** shape.
- **Risk** is high when `migration`, `drop`, `delete`, `schema`, `auth`,
  `secret`, or `prod` appears outside fenced code.

Route on that judgment:

- **Ready** — a Done/Acceptance Criteria heading, an observable assertion inside
  that section, no high-risk keyword, single-leaf granularity, and no strong task
  shape. Proceed to `relay-plan`.
- **needs_split** — a strong task shape. Take the proposal-first shaping route
  below before any dispatch; only an explicit operator override skips it.
- **Escalate** — high risk together with any low dimension. Confirm scope with
  the operator instead of dispatching.
- **Otherwise** — ask bounded questions until one of the routes above holds.

An accepted relay-ready handoff supersedes the issue's own acceptance criteria
only when the bundle's source identity matches the task in hand: the issue
number or issue URL recorded under `source`, or, when neither was recorded, the
`request_id` the operator was given. Before treating an issue body as ready,
check `~/.relay/requests/<repo-slug>/` for such a bundle and use it as the
source of truth. A newer bundle for a different issue is irrelevant — never let
it override the current issue's criteria.

## Output Contract

Persist one immutable completed bundle under `~/.relay/requests/<repo-slug>/<request-id>/` (request
frontmatter, raw request, handoff(s), Done Criteria snapshot(s), and a last completion marker). Field-by-field schema with input
requirements plus persisted request and handoff artifact definitions: see
[`scripts/request-contract.schema.json`](scripts/request-contract.schema.json). `persist-request.js`
validates the input contract on every persistence call; `$defs.RequestArtifact` and
`$defs.HandoffArtifact` document generated frontmatter for downstream consumers.

## Persistence Step

Write a JSON contract file with:
- `source.kind`
- `request_text`
- either `handoff` for single-leaf or `handoffs[]` for multi-leaf
- per leaf: `leaf_id`, `title`, `goal`, `order`
- per leaf: `done_criteria_markdown`
- optional per leaf: `depends_on`, `in_scope`, `out_of_scope`, `assumptions`, `escalation_conditions`

Persist it with:

```bash
node "${RELAY_SKILL_ROOT:-skills}/relay-ready/scripts/persist-request.js" --repo . --contract-file /tmp/relay-ready-contract.json --json
```

Readiness is optional, but if supplied, all readiness dimensions are required; see schema enum domains.

## Decomposition Boundary

Scripts only validate and persist handoffs; they do not infer semantic leaf boundaries. The task-shape factors above detect decomposition pressure, not the correct leaves. When the shape is strong, use AI proposal-first shaping to decide whether the request is one high-risk leaf or multiple ordered leaves, then persist the accepted shape. Detailed operator contract and oversized product-foundation example: [`references/decomposition-contract.md`](references/decomposition-contract.md).

Proposal, clarification, answer, and edit state stays in the conversation. Do not
persist mutable intake state or a readiness event journal. Call `persist-request.js`
once the accepted leaf shape is final. A completed bundle is immutable and an
incomplete bundle fails closed for operator inspection.

## Downstream Handoff

After persistence succeeds:
1. use `relay-ready/<leaf-id>.md` as the source-of-truth input for `relay-plan`
2. dispatch with:

```bash
node "${RELAY_SKILL_ROOT:-skills}/relay-dispatch/scripts/dispatch.js" . \
  -b <branch> \
  --prompt-file <dispatch-prompt-path> \
  --rubric-file <rubric-path-from-relay-plan> \
  --done-criteria-file <done-criteria-path>
```

3. for multi-leaf requests, dispatch leaves in `decomposition.leaf_order`, respecting `depends_on`
4. let dispatch freeze that file into the new run's immutable Done Criteria contract

Do not create a second lifecycle. The readiness gate stops once the relay-ready contract is persisted.
