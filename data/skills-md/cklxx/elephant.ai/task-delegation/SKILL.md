---
name: task-delegation
description: 跨 Agent 任务委派 — 将子任务分发给 Codex/Claude/Gemini CLI 执行。
triggers:
  intent_patterns:
    - "delegate|委派|分发|子任务|subtask|dispatch|后台执行"
  context_signals:
    keywords: ["delegate", "委派", "codex", "claude", "dispatch"]
  confidence_threshold: 0.7
priority: 7
requires_tools: [bash]
max_tokens: 200
cooldown: 120
---

# task-delegation

跨 Agent 任务分发：将子任务委派给外部 CLI agent 执行。

## 调用

```bash
python3 skills/task-delegation/run.py dispatch --agent codex --task 'fix the bug in main.go'
python3 skills/task-delegation/run.py list
```
