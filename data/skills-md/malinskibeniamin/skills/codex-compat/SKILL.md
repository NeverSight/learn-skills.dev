---
name: codex-compat
description: Generate Codex hooks.json and AGENTS.md parity surfaces from the Claude hook manifest.
disable-model-invocation: true
---

Codex supports Claude-style `SessionStart`, `SubagentStart`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `UserPromptSubmit`, `SubagentStop`, and `Stop` hooks. Claude-only events (`FileChanged`, `WorktreeCreate`, `SessionEnd`, `PostToolUseFailure`) use a safe Stop-batch fallback or are dropped. Tool matchers cover Bash, MCP, `apply_patch`, and `Edit|Write`; map edit hooks direct when possible. Use `/read-the-damn-docs` for current behavior and `/plan-arbiter` for ambiguous mappings.

## Creates

- `.codex/hooks.json`: supported direct hooks.
- `.codex/hooks/codex-batch-check.sh`: fallback-only checks.
- `.codex/rules/frontend-skills.rules`: execpolicy floor.
- Root `AGENTS.md` + `CLAUDE.md`: shared rules.
- compatibility matrix: `direct|direct with shim|fallback only|unsupported`.

## Steps

1. Classify every `.claude/settings.json` hook with [REFERENCE.md](REFERENCE.md).
2. Generate `.codex/hooks.json`: lifecycle events direct; Bash/Edit|Write/`apply_patch`/`mcp__.*` pre/post direct; PermissionRequest direct only when scripts accept Codex payloads; omit/document unsafe unsupported cases.
3. Copy `scripts/codex-batch-check.sh` only when fallback is required; make executable.
4. Copy `hooks/frontend-skills.rules` to `.codex/rules/`.
5. Generate AGENTS/CLAUDE from the reference template.
6. Set `[features] hooks = true` in `config.toml`; run `/hooks` and trust definitions again after changes. CI uses managed hooks or `--dangerously-bypass-hook-trust`. Optional `notify = ["bash", "<repo>/.claude/hooks/codex-notify.sh"]`.

## Verify

- Direct source `Edit|Write` PostToolUse hooks exist; batch checker exists only for fallback.
- Rules copy is byte-identical; hooks active/trusted, not pending.
- Root AGENTS/CLAUDE exist; `.claude/settings.json` unchanged.
