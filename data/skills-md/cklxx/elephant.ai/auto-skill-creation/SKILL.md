---
name: auto-skill-creation
description: 自动创建技能并将重复流程沉淀为技能，支持使用 Codex/Claude 等外部代理执行任务并生成技能文件。
triggers:
  intent_patterns:
    - "create skill|创建技能|新技能|auto skill|沉淀技能|skill creation"
  context_signals:
    keywords: ["skill", "技能", "create", "创建", "沉淀", "auto"]
  confidence_threshold: 0.6
priority: 7
requires_tools: [bash]
max_tokens: 200
cooldown: 60
---

# auto-skill-creation

Automatically create new skills from repeated task patterns by dispatching to external agents (Codex/Claude), collecting results, and generating compliant skill directory structures. All task dispatch, status monitoring, and file generation logic are handled by run.py.

## 调用

```bash
python3 skills/auto-skill-creation/run.py create --skill_name my-new-skill --description 'What the skill does' --agent_type codex
```
