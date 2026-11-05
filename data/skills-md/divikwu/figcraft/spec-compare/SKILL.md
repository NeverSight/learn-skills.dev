---
name: spec-compare
description: "Compare DTCG design token spec against Figma Library variables. Use when: compare/diff/check + tokens/spec/DTCG + Figma/variables/library, or when auditing token drift between code and Figma."
---

# Spec Compare — DTCG vs Figma Token Diff

Compare a DTCG (W3C Design Token Community Group) JSON spec against Figma Library variables. Categorizes differences and recommends sync actions. Pairs with `token-sync` for the actual sync step.

## Skill Boundaries

- Use this skill to **compare and audit** token differences between DTCG spec and Figma.
- If the task is **syncing tokens to Figma**, switch to [token-sync](../token-sync/SKILL.md).
- If the task is **exporting Figma variables to DTCG**, use `reverse_sync_tokens` directly after `load_toolset("tokens")`.
- If the task is **creating variables from scratch**, switch to [figcraft-generate-library](../figcraft-generate-library/SKILL.md).

## Workflow

### Step 1: Connect and Get File Path

```
ping                                          → verify plugin connection
```

**If `ping` fails (plugin not connected):** STOP. Do not fall back to other MCP servers. Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.

Ask the user for the DTCG JSON file path (e.g., `tokens/design-tokens.json`).

### Step 2: Load Token Tools

```
load_toolset("tokens")                        → enable DTCG token tools
```

### Step 3: Preview Tokens

```
list_tokens(filePath: "...")                   → parse and preview DTCG tokens
```

Optional: filter by type (e.g., `type: "color"`) to focus on specific token categories.

### Step 4: Diff Against Figma

```
diff_tokens(filePath: "...", collectionName: "...")  → compare DTCG vs Figma variables
```

Returns tokens categorized as:
- ✅ In-sync — values match between DTCG and Figma
- ⬆️ DTCG-ahead — DTCG has newer/different values
- ⬇️ Figma-ahead — Figma has values not in DTCG
- ❌ Missing — tokens exist in one side but not the other

### Step 5: Report and Recommend

Present a structured diff report:

```
📊 Token Comparison:
- In-sync: X tokens
- DTCG-ahead: Y tokens (DTCG has updates)
- Figma-ahead: Z tokens (Figma has updates)
- Missing in Figma: N tokens
- Missing in DTCG: M tokens
```

Recommend actions for each category:
- DTCG-ahead → `sync_tokens` to push DTCG values to Figma
- Figma-ahead → `reverse_sync_tokens` to export Figma values to DTCG, or update DTCG manually
- Missing in Figma → `sync_tokens` to create new variables
- Missing in DTCG → add to DTCG spec or remove from Figma

### Step 6: Offer Sync

Ask the user if they want to sync to resolve differences. If yes, hand off to the `token-sync` workflow.

## Integration

```
spec-compare → token-sync
(audit)        (sync)
```

Run spec-compare first to understand the gap, then token-sync to resolve it.
