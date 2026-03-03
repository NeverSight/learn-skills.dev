---
name: soul-self-evolution
description: SOUL 自演进技能 — 在不可变段保护下更新可演进人格/协作策略并支持回滚。
triggers:
  intent_patterns:
    - "soul|人格更新|self evolve|自我优化|更新协作风格"
  context_signals:
    keywords: ["SOUL", "persona", "habit", "collaboration"]
  confidence_threshold: 0.7
priority: 9
requires_tools: [read_file, write_file]
max_tokens: 320
cooldown: 300
capabilities: [self_evolve_soul, policy_self_adjust]
governance_level: critical
activation_mode: semi_auto
depends_on_skills: [meta-orchestrator]
produces_events:
  - workflow.skill.meta.soul_updated
  - workflow.skill.meta.rollback_applied
requires_approval: false
---

# soul-self-evolution

对 `SOUL.md` 或 `docs/reference/SOUL.md` 进行受控更新：
- 只允许改动可演进段
- 记录 checkpoint
- 支持一键回滚

## 调用

```bash
python3 skills/soul-self-evolution/run.py '{"action":"apply","path":"docs/reference/SOUL.md","changes":[{"section":"## Collaboration Preferences","content":"- Keep updates concise."}]}'
python3 skills/soul-self-evolution/run.py '{"action":"list_checkpoints"}'
```
