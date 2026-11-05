---
name: diagram
description: Create, repair, and calibrate ToDiagram custom-format diagrams (.todiagram) for end users, including system architecture maps, process/flow diagrams, schema normalization, and readability-driven grouping/splitting. Use when users ask for ToDiagram JSON generation, invalid payload fixes, architecture/flow modeling, simplification/detail tuning of existing diagrams, or stable file-based diagram output.
---

# Diagram

## Mission
Generate human-readable `.todiagram` JSON that is valid for ToDiagram's custom schema and optimized for fast visual comprehension.

## Mode Router
1. `schema-build`: user asks to create/fix `.todiagram` structure or convert notes into valid nodes/edges.
2. `system-architecture`: user asks for platform/service/component topology.
3. `flow-diagram`: user asks for workflow, journey, runbook, or decision flow.
4. `detail-calibration`: user asks to simplify, enrich, or split dense diagrams.

If a request spans multiple modes, run in this order:
1. schema-build
2. system-architecture or flow-diagram
3. detail-calibration
4. final schema validation

## Global Output Contract
- Default to file-first output for stability:
  create a `.todiagram` file and return its path.
- Only return inline JSON when the user explicitly asks for inline output.
- Use canonical raw `.todiagram` keys: `nodes`, `edges`, `direction`, `id`, `label`, `from`, `to`, `imageUrl`, `iconUrl`, `custom_theme`, `fields`.
- Put node display data inside the `fields` object. Direct properties on the node are deprecated by the schema.
- Never combine `imageUrl` with `fields` on the same node — `imageUrl` replaces row rendering.
- Include `imageUrl` and `iconUrl` only when used; omit the keys entirely otherwise.
- Include node-level `nodes` only for true containers with real children.
- Restrict `direction` to `RIGHT`, `LEFT`, `UP`, or `DOWN` (`UP`, not `TOP`).
- Keep IDs globally unique; ensure every edge endpoint resolves to an existing ID.
- Prefer Iconify specs (`logos:*`, `fa7-solid:*`, short forms like `fa:gear`) for icons; use external URL icons only if the user explicitly requests them.
- When the exact Iconify slug is unknown, look it up via `curl -fsSL 'https://api.iconify.design/search?query=<term>&limit=10'` (optionally `&prefix=logos`) and pick a slug from the returned `icons` array. Use the ToDiagram MCP icon-search tool when available.
- Apply per-node theming via `custom_theme` (`NODE`, `EDGE`, `TEXT` groups) — see schema contract for full key list.

## File Output Policy
- If user provides a target path/name, write there.
- If user does not provide one, derive a short kebab-case filename from the diagram's topic or subject
  (e.g., "system architecture" → `system-architecture.todiagram`, "user onboarding flow" → `user-onboarding-flow.todiagram`, "AWS infrastructure" → `aws-infrastructure.todiagram`).
  Write to the current working directory.
- For multi-diagram outputs, use stable descriptive names:
  `overview.todiagram`, `domain-<name>.todiagram`, `flow-<name>.todiagram`.
- After writing, run:
  `python scripts/validate_todiagram_schema.py <file>.todiagram`

## Core Workflow
1. Identify audience and decision intent.
2. Select mode and detail tier (overview, working, deep-dive).
3. Draft container hierarchy first, then leaf nodes, then edges.
4. Add concise labels and only high-signal metadata.
5. Validate with [`references/authoring-checklist.md`](references/authoring-checklist.md) and run:
   `python scripts/validate_todiagram_schema.py <file>.todiagram`
6. If overloaded, split using [`references/split-strategies.md`](references/split-strategies.md) while preserving shared IDs/names.

## Mode Playbooks

### 1) Schema Build
Read [`references/schema-contract.md`](references/schema-contract.md) first.

Use this scaffold unless the user provides a different envelope:

```json
{
  "direction": "RIGHT",
  "nodes": [],
  "edges": []
}
```

Rules:
- Add `configuration` only when key mappings deviate from defaults.
- Normalize payloads to canonical keys (`children` → `nodes`, `source`/`target` → `from`/`to`).
- Move deprecated direct node properties into the `fields` object.
- If a node has both `imageUrl` and `fields`, drop one — they cannot coexist.

### 2) System Architecture
Read:
- [`references/grouping-playbook.md`](references/grouping-playbook.md)
- [`references/architecture-patterns.md`](references/architecture-patterns.md)

Rules:
- Prefer 2-3 hierarchy levels.
- Keep most containers within 3-8 children.
- Connect leaf-to-leaf interactions by default.
- Keep overview diagrams metadata-light.

### 3) Flow Diagrams
Read:
- [`references/flow-patterns.md`](references/flow-patterns.md)
- [`references/labeling-guide.md`](references/labeling-guide.md)

Rules:
- Build happy path first, then branches/failures/retries.
- Keep one dominant direction per diagram.
- Keep edge labels short (1-3 words) and meaningful.

### 4) Detail Calibration
Read:
- [`references/complexity-budgets.md`](references/complexity-budgets.md)
- [`references/split-strategies.md`](references/split-strategies.md)

Rules:
- Choose a detail tier before generating.
- If above budget, split by domain, lifecycle, environment, or audience.
- Keep cross-diagram naming and shared IDs consistent.

## Example Intents
- "Create a high-level SaaS architecture in ToDiagram." -> `system-architecture` + overview tier.
- "Fix this invalid ToDiagram JSON." -> `schema-build`.
- "Turn this incident runbook into a readable flow." -> `flow-diagram` (+ `detail-calibration` if dense).

## Troubleshooting
- Invalid payload shape: normalize keys and flatten wrappers first.
- Diagram too noisy: remove low-signal metadata and split into focused views.
- Diagram too abstract: add 1-2 critical metadata properties on key leaves.
- Unclear relationships: add concise protocol/action/outcome edge labels.
- Schema validation dependency error: install `jsonschema` via
  `python3 -m pip install --user jsonschema`.

## References
- Schema contract: [`references/schema-contract.md`](references/schema-contract.md)
- Authoring checklist: [`references/authoring-checklist.md`](references/authoring-checklist.md)
- Architecture patterns: [`references/architecture-patterns.md`](references/architecture-patterns.md)
- Grouping playbook: [`references/grouping-playbook.md`](references/grouping-playbook.md)
- Flow patterns: [`references/flow-patterns.md`](references/flow-patterns.md)
- Labeling guide: [`references/labeling-guide.md`](references/labeling-guide.md)
- Complexity budgets: [`references/complexity-budgets.md`](references/complexity-budgets.md)
- Split strategies: [`references/split-strategies.md`](references/split-strategies.md)

## Scripts
- Canonical + schema validator:
  [`scripts/validate_todiagram_schema.py`](scripts/validate_todiagram_schema.py)
