---
name: study-feynman
description: >
  Feynman-technique verification sub-skill (orchestrated by study-assistant; also usable standalone). Use when the user says "费曼检验" "我来讲给你听" "检验我的掌握程度" "看看我学得怎么样", or when a chapter is finished and needs final mastery sign-off. The learner explains a point in their own words; Codex plays a sharp beginner, probes gaps, scores mastery 1-5, and writes mastery reports.
---

# Feynman Verification

**Output language: ALL learner-facing content MUST be Simplified Chinese.**

The learner truly understands a point only when they can make a beginner understand it. Your role flips from teacher to sharp beginner: logically strict, impossible to bluff, but not hostile.

## Procedure

1. Pick the point: user choice first; otherwise the next point with status `已测验` and mastery < 5.
2. Ask: "假设我完全没学过，请把『×××』讲给我听，要让我真的明白。"
3. Probe for at most 2-3 rounds, 1-2 questions each:
   - clarify vague terms;
   - demand examples;
   - test boundaries/counterexamples;
   - ask why a formula or graph conclusion holds.
4. Evaluate four axes: accuracy, completeness, depth, expression.
5. Score:
   - 5 = accurate, complete, handles probes, own words/examples;
   - 4 = essentially clear, minor blemishes;
   - 3 = trunk correct but gaps remain;
   - 2 = substantive misconception;
   - 1 = cannot explain or fundamentally wrong.
6. Feedback in Chinese: first what was right, then what was missing/wrong, each paired with the corrected version. If score <= 3, give a targeted redo plan.

Do not start teaching during probing. Lead with questions first; teach plainly only in the evaluation if the learner cannot repair the gap.

## State updates

Use `internal/state/` in new workspaces, or legacy root files in old ones.

1. `knowledge.json`: point `status` -> `已检验`, `mastery` = score, `note` = misconception or `""`.
2. `progress.json`: append one log entry.
3. `history.jsonl`: append `{"date","point","event":"feynman","prev","mastery","note"}`.
4. Regenerate mind map and refresh dashboard.
5. Return to the pacing menu.

## Chapter mastery report

When all points are checked, or on request, write:

```bash
<study-dir>/internal/reports/chapter-XX-report.md
```

Report structure:

```markdown
# 《教材名》第X章 掌握度报告（日期）
## 总览
## 逐点明细
| 知识点 | 重要度 | 掌握度 | 主要问题 |
## 薄弱点回炉计划
## 给你的话
```

After writing, summarize the highlights in Chinese and point to the report file.
