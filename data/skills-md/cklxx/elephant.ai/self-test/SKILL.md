---
name: self-test
description: 自主运行 Lark 场景测试套件，分析失败，按修复分级自动迭代修复。
triggers:
  intent_patterns:
    - "self.?test|自测|场景测试|scenario.?test|run.?test|测试套件"
  context_signals:
    keywords: ["test", "scenario", "lark", "测试", "自测"]
  confidence_threshold: 0.7
priority: 7
requires_tools: [bash]
max_tokens: 200
cooldown: 120
---

# self-test

Run the Lark scenario test suite, analyze failures by root cause (test_drift, prompt_issue, tool_bug, etc.), apply tiered auto-fixes (up to 3 rounds), and generate a structured report. All test execution, failure analysis, and iterative repair logic are handled by run.py.

## 调用

```bash
python3 skills/self-test/run.py run
```
