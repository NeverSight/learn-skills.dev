---
name: code-review
description: 编码完成后的多维度代码审查，覆盖 SOLID 架构、安全性、代码质量、边界条件与清理计划，输出结构化审查报告。
triggers:
  intent_patterns:
    - "review|审查|code review|CR|代码审查|review code"
  context_signals:
    keywords: ["review", "审查", "CR", "code review", "代码质量", "merge"]
  confidence_threshold: 0.6
priority: 9
requires_tools: [bash]
max_tokens: 200
cooldown: 60
---

# code-review

Run a multi-dimensional code review (SOLID architecture, security, quality, edge cases, cleanup) on the current diff and output a structured report with severity levels (P0-P3). All review checklists, workflow steps, and report generation are handled by run.py.

## 调用

```bash
python3 skills/code-review/run.py review
```
