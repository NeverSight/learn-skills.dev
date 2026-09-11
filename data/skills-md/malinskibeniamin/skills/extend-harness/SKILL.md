---
name: extend-harness
description: Extend and debug the frontend-skills hook harness, rules, severity tiers, and analytics.
disable-model-invocation: true
---

Edit source manifests/libraries, never generated configs. [REFERENCE.md](REFERENCE.md) owns severities, options, parser contracts, debugging.

## Add rule

1. Prefer Biome/Ultracite; hooks are for cross-element/file, workflow, or agent behavior.
2. Copy a neighboring `.claude/hooks/checks/*.lib.sh`: one `run_*` function plus thin `.claude/hooks/*.sh` wrapper.
3. Register in `skill-manifest.json`, usually `PostToolUse.Edit|Write`.
4. Add focused `evals/` fixture; capture RED then GREEN.
5. Regenerate and test:

```bash
bash scripts/generate-hook-configs.sh --apply
echo '{"hook_event_name":"PostToolUse","tool_name":"Edit","tool_input":{"file_path":"/tmp/x.ts"}}' | bash .claude/hooks/my-check.sh
```

Use `hook_warn` for style, `hook_block` correctness, `hook_block_strict` security, `hook_info` observation. Prefer skill-scoped hooks for one vertical.

## Implementation

- Permission-filtered/async entries use manifest objects; retain stdin guards because Codex drops Claude-only filters.
- Provable structure belongs in Biome/AST; ambiguous judgment in review, not multiline grep.
- Sync toolchain bans with `hooks/frontend-skills.rules`.

## Audit/debug

`/hook-audit --all` for latency/firing/zero-fire; `HOOK_DEBUG=1 HOOKS_FAIL_CLOSED=1 claude` for missing hooks; `claude --safe-mode` to isolate customization. `/doctor` latency is a P95 budget failure.

## Done

Manifest owns matcher; executable script sources `_hook-lib.sh`, parses stdin, filters paths, documents escape; fixture proves RED -> GREEN; generator `--check` and `bash evals/run.sh` pass.
