---
created: 2026-01-24
updated: 2026-02-22
version: 2.0.0
name: token-log
description: Log token usage for a specific phase of story workflow. Called automatically by workflow commands after completing a phase. Writes to the storyTokenUsage table via kb_log_tokens MCP tool.
kb_tools:
  - kb_log_tokens
---

# /token-log - Log Phase Token Usage

## Usage

```
/token-log STORY-XXX phase-name [input-tokens] [output-tokens]
```

## Arguments

- `STORY-XXX` — story ID (e.g., STORY-001, WRKF-1021)
- `phase-name` — standardized phase name (see table below)
- `input-tokens` — (optional) input token count
- `output-tokens` — (optional) output token count

If tokens are not provided, prompt the user to estimate from `/cost` output.

## Standardized Phase Names

| Phase Name | Command |
|------------|---------|
| `pm-generate` | `/pm-generate-story` |
| `pm-fix` | `/pm-fix-story` |
| `elaboration` | `/elab-story` |
| `dev-setup` | Phase 0 of `/dev-implement-story` |
| `dev-planning` | Phase 1 of `/dev-implement-story` |
| `dev-implementation` | Phase 2 of `/dev-implement-story` |
| `dev-verification` | Phase 3 of `/dev-implement-story` |
| `dev-documentation` | Phase 4 of `/dev-implement-story` |
| `code-review` | `/dev-code-review` |
| `dev-fix` | `/dev-fix-story` |
| `qa-verify` | `/qa-verify-story` |

## Task

1. Call `kb_log_tokens` MCP tool with the provided arguments:

```javascript
kb_log_tokens({
  story_id: "STORY-XXX",
  phase: "phase-name",
  input_tokens: {input-tokens},
  output_tokens: {output-tokens}
})
```

2. Report success with summary

## Output

After logging, report the result from `kb_log_tokens`:

```
Token logged for STORY-XXX:
  Phase: phase-name
  Input: XX,XXX | Output: XX,XXX | Total: XX,XXX
```

## Error Handling

If `kb_log_tokens` returns an error:
- Report the error message
- Suggest checking that the KB MCP server is running

If phase-name is not in the standard list:
- Allow it but warn: "Non-standard phase name: 'custom-name'"

## Examples

```bash
/token-log WRKF-1021 pm-generate 15000 5000
# → Logs 15k input, 5k output for pm-generate phase

/token-log WRKF-1021 elaboration 20000 2000
# → Logs 20k input, 2k output for elaboration phase
# → Cumulative now 42,000

/token-log WRKF-1021 dev-implementation 80000 37000
# → Logs 80k input, 37k output for dev-implementation
# → Cumulative now 159,000
```
