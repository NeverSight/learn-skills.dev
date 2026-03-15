---
name: skill-writer
description: Claude Code skill 设计和编写助手。仅通过 /skill-writer 命令手动触发，不自动激活。负责分析需求合理性、边界情况、降级兼容处理，最终生成规范的 SKILL.md 文件。
version: 1.0.0
author: snailuu
allowed-tools: Read, Write, Glob, Bash
---

# Skill Writer

Read `~/.claude/skills/skill-writer/AGENTS.md` before proceeding.

---

## 重要：工具调用规则

**必须直接使用 Bash 工具执行 shell 命令，绝对不要使用 Task 工具。**

## Phase 1 — Analyze and Score

```bash
ls ~/.claude/skills/
```

Analyze the requirement. Output a completeness score immediately using the
scoring template in AGENTS.md § Appendix B.

---

## Phase 2 — Iterate

After each user response, update the score and ask only the highest-impact
unanswered questions.

Advance to Phase 3 when score ≥ 85, or user says "够了" / "直接写".

---

## Phase 3 — Present Draft

Show the complete SKILL.md content in a code block.
Use the template from AGENTS.md § Appendix C.

Note any fields filled with defaults. Ask: **"是否需要修改？没问题就写入文件。"**

---

## Phase 4 — Write and Validate

```bash
mkdir -p ~/.claude/skills/<skill-name>
```

Write the file with the Write tool. Then validate:

```bash
bash ~/.claude/skills/skill-writer/scripts/validate.sh ~/.claude/skills/<skill-name>
```

Report the validation result to the user.
