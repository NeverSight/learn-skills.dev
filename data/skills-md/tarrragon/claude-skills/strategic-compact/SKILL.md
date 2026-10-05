---
name: strategic-compact
description: "策略性 Context 壓縮工具 - 在邏輯邊界建議手動 /compact，避免 auto-compaction 在不恰當時機打斷工作流。Use for: (1) 探索階段完成、即將進入實作時, (2) 完成一個 Milestone 後要開始下一個 Phase, (3) 長時間 debug 後恢復正常開發, (4) 大量工具呼叫後 Context 開始擁擠時。Use when: 用戶詢問何時應該 /compact、擔心 Context 被截斷、完成重要里程碑後想要清空無關 Context 時。"
metadata:
  version: 1.0.0
---

# Strategic Compact Skill

Suggests manual `/compact` at strategic points in your workflow rather than relying on arbitrary auto-compaction.

## Why Strategic Compaction?

Auto-compaction triggers at arbitrary points:

- Often mid-task, losing important context
- No awareness of logical task boundaries
- Can interrupt complex multi-step operations

Strategic compaction at logical boundaries:

- **After exploration, before execution** - Compact research context, keep implementation plan
- **After completing a milestone** - Fresh start for next phase
- **Before major context shifts** - Clear exploration context before different task

## How It Works

The `suggest-compact.py` script runs on PreToolUse (Edit/Write) and:

1. **Tracks tool calls** - Counts tool invocations in session
2. **Threshold detection** - Suggests at configurable threshold (default: 50 calls)
3. **Periodic reminders** - Reminds every 25 calls after threshold

## Hook Setup

Add to your `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "tool == \"Edit\" || tool == \"Write\"",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/skills/strategic-compact/suggest-compact.py"
          }
        ]
      }
    ]
  }
}
```

## Configuration

Environment variables:

- `COMPACT_THRESHOLD` - Tool calls before first suggestion (default: 50)

## Best Practices

1. **Compact after planning** - Once plan is finalized, compact to start fresh
2. **Compact after debugging** - Clear error-resolution context before continuing
3. **Don't compact mid-implementation** - Preserve context for related changes
4. **Read the suggestion** - The hook tells you _when_, you decide _if_

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Token optimization section
- Memory persistence hooks - For state that survives compaction

---

版本紀錄在同目錄的 `CHANGELOG.md`。
