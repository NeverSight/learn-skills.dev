---
name: experience-lwc-widget-assess
description: "Assess whether a specific Lightning web component can serve its user's purpose as an HXL declarative widget. Use for LWC-to-widget feasibility, portability audits, and candidate screening; use experience-lwc-widget-migrate when the user wants the widget built."
metadata:
  version: "1.0"
  domains: ["Experience", "Platform", "Agentforce"]
  minApiVersion: "68.0"
  relatedSkills:
    - "experience-lwc-widget-migrate"
    - "platform-widget-generate"
---

# Assess LWC to widget fit

Answer two questions for each LWC: **Can the current behavior be represented?** If not, **would a feasible widget still accomplish the user's goal?** Assess only; do not create metadata. A widget is its own declarative artifact, distinct from a Lightning Type. Its body renders supplied data with discovered tiles, bindings, formulas, and supported actions. It cannot run arbitrary LWC code, fetch after render, or retain reactive client state.

## Evidence and decision

1. Read the component's JS/TS, template, metadata, and relevant child components. State the user's goal in one sentence. Trace each visible value to its source and identify interactions essential to that goal. An `@api` property proves external input, **not** that an invocable action returns it. A user's explicit statement about action output is evidence for a feasibility assessment; verify the actual action contract and Lightning Type/renderer wiring before claiming a working migration.
2. Map the **job** of each rendered element and action to the target surface. `platform-widget-generate` explains the discovery procedure; the actual `discoverUiComponents` response and `getUiComponentSchemas` results establish available blocks and attributes. Read its `references/widget-formulas.md` only when a transformation matters. Record the target channel from evidence rather than assuming a fixed channel or tile count. Without discovery, a documented pattern can support a **provisional candidate**, but absence from examples does not prove a block is unavailable. Use `review` when that uncertainty determines the verdict; never invent a tile, action, input submission mechanism, or formula.
3. Check all dimensions, even after a failure: rendering vocabulary; retained state, imperative effects, and actions; data origin; and transformations. A bounded snapshot or pre-shaped collection can sometimes move into the invocable action's output. Inspect the action implementation before asserting that it can. A formula's scalar `MIN`/`MAX`, date, or regex support does not imply collection sorting or aggregation. Input forms require evidence that the current tiles can collect values **and** pass those values to an action; `sendMessage` alone does not prove that.
4. Judge the current LWC and a proposed widget separately. A link or `sendMessage` may preserve an intent without preserving the original interaction, if the agent can actually perform the requested work with the required context. A carousel may become a product list; an order builder whose purpose is choosing quantities may not. Treat that change as a rebuild. For the widget candidate, consider a **specified proposed IA contract** when setting `rendersAsWidget`; state the contract change explicitly. If feasibility or purpose remains unresolved, use `review`, not a forced yes/no verdict.

Use these outcomes:

| Outcome | Meaning |
|---|---|
| `asIsVerdict: port-declarative` | Current visible behavior and data contract can be represented. |
| `asIsVerdict: needs-IA-contract-change` | Only a bounded output or pre-shaping change is needed. |
| `asIsVerdict: not-portable` | Some current behavior or visual has no verified equivalent. |
| `asIsVerdict: review` | Evidence cannot establish the current fit. |
| `asDisplayWidget.verdict: viable` | A verified or clearly identified candidate serves the goal, possibly after a stated contract change or rebuild. |
| `asDisplayWidget.verdict: pointless` | It can render but loses the user's goal. |
| `asDisplayWidget.verdict: blocked` | The proposed display/action cannot be represented. |
| `asDisplayWidget.verdict: review` | Capability, data provenance, or purpose is unresolved. |

List **every material blocker** in the report with its gate and evidence, citing a source location or concrete behavior. Gate names are `role`, `rendering vocabulary`, `behavior/interactivity`, `data source`, and `transformation`. Do not stop at the first failed dimension. `contractChange.shapeToAdd` names only fields or pre-shaped values the action could plausibly return; never invent a payload. A viable adaptation may need a contract change even when the current LWC is `not-portable`. If a proposed widget changes the UX, set `isRebuild: true` and name the lost interaction in the report. Mark uncertain conclusions low confidence and explain what would resolve them.

## Output

Produce two artifacts. When an output location is given, write them as `verdict.json` and `report.md`.

**Verdict** — the machine-readable decision that `experience-lwc-widget-migrate` gates on. One JSON object per component; for a folder, an array. Keep exactly these fields:

```json
{
  "component": "caseDetailsPanel",
  "role": "renderer",
  "asIsVerdict": "port-declarative",
  "contractChange": {"suggested": false, "shapeToAdd": []},
  "asDisplayWidget": {"verdict": "viable", "rendersAsWidget": true, "stillServesPurpose": true, "isRebuild": false},
  "needsHumanReview": false
}
```

`role` is `renderer`, `input`, or `interactive`. `stillServesPurpose` is boolean or `"unknown"`; `rendersAsWidget` is boolean or `null` when capability is unresolved. For `viable`, both are true. For `pointless`, rendering is true and purpose false. For `blocked`, rendering is false and purpose is `"unknown"`. For `review`, keep unresolved fields unknown/null. Set `needsHumanReview: true` for either `review` verdict or unknown purpose. Suggest a contract change only when a value the widget displays is **not** already in the action's output (for example, it is fetched after render). Data already in the payload needs no contract change, even when the LWC is `not-portable` or the widget is a rebuild. Any suggested contract change needs a nonempty `shapeToAdd`; `needs-IA-contract-change` requires such a suggestion. `port-declarative` has no contract change.

**Report** — the human-review document. For a folder, one section per component. Use this structure:

```markdown
# <component>: <one-line conclusion>

**Verdict:** <asIsVerdict> → <asDisplayWidget.verdict> (rebuild or not) · **Confidence:** high | low · **Needs human review:** yes | no

## Why
The user's goal, what maps cleanly, and what decides the verdict.

## Blockers
Each material blocker: gate, signal, evidence. "None" for `port-declarative`.

## Suggested contract change
Each field to add and why it must move into the action output. Omit when none is suggested.

## What the widget keeps / drops
Kept actions and dropped or replaced interactions.

## Open questions
What would resolve any low-confidence conclusion.
```
