---
name: start
description: First-time onboarding — asks where you are, then guides you to the right workflow. No assumptions.
license: MIT
phase_automation:
  auto_proceed_default: false
  user_override_command: "/manual"
  phases:
    - phase: "Phase 1: Detect State"
      auto_conditions:
        - condition_type: "file_exists"
          target: ".opencode/project-context.md"
          action_if_met: "skip"
          notification: "✅ 配置文件已存在，自动跳过状态检测"
          fallback_action: "proceed_manual"

    - phase: "Phase 2: Team Structure Detection"
      auto_conditions:
        - condition_type: "config_has_key"
          config_file: ".opencode/project-context.md"
          key: "Team Structure"
          action_if_met: "skip"
          notification: "✅ 团队结构已配置，跳过此阶段"

    - phase: "Phase 2.5: MCP Integration Check"
      auto_conditions:
        - condition_type: "config_has_key"
          config_file: ".opencode/project-context.md"
          key: "MCP Status"
          action_if_met: "skip"
          notification: "✅ MCP 状态已记录，跳过此阶段"

    - phase: "Phase 3: Project Stage Check"
      auto_conditions:
        - condition_type: "config_has_key"
          config_file: ".opencode/project-context.md"
          key: "Project Stage"
          action_if_met: "skip"
          notification: "✅ 项目阶段已设置，跳过此阶段"
---

# Guided Onboarding Skill

Entry point for new users. Detects project state and team structure, routes to the right skill.

---

## ⚠️ EXECUTION RULES

1. **ONE PHASE PER TURN** — Execute only one phase, then STOP and wait
2. **NEVER SKIP AHEAD** — Do not proceed to next phase without user response
3. **IF TOOL FAILS** — Skip that check and continue with available info
4. **ALWAYS END WITH A QUESTION** — Never end a turn without asking user something

---

## Phase 1: Detect State (Silent)

**ACTION**: Try to read these files (skip if not found):
- `.opencode/project-context.md` → **Team, project & MCP info already collected?**
- `.opencode/mcp.json` → **MCP servers configured?**
- `.opencode/docs/technical-preferences.md` → Engine configured?
- `design/gdd/game-concept.md` → Game concept exists?
- Check `src/` directory → Source code exists?

**IF `project-context.md` EXISTS**:
- Read team structure, project stage, and MCP status from it
- Skip Phase 2, Phase 2.5, and Phase 3 (already answered)
- Jump directly to Phase 4 with stored values

**IF `mcp.json` EXISTS with enabled servers**:
- Note MCP configuration status for Phase 4 routing suggestions

**STOP**: After detection, proceed to Phase 2 (if config missing) or Phase 4 (if config exists).

---

## Phase 2: Team Structure Detection

**IF config already has team structure**:
- Skip this phase, use stored value

**ELSE, ASK**:
```
你的团队结构是什么？

A) 单人独立开发 — 只有我一个
B) 2人小队 — 我+队友（程序/美术/策划）
C) 3人小队 — 我作为队长，有队友支持
D) 更大团队 — 4人及以上
```

**AFTER user answers**:
1. **WRITE to `.opencode/project-context.md`**:
   ```markdown
   ## Team Structure
   - **Type**: [用户选择的选项]
   - **My Role**: [如果是B/C，询问队长角色]
   ```
2. **STOP**: Wait for user's answer before writing.

---

## Phase 2.5: MCP Integration Check (Optional)

**IF config already has MCP status**:
- Skip this phase, use stored value

**ELSE, ASK**:
```
你是否需要配置 MCP 服务器来增强开发能力？

可选服务器：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• PixelLab   — AI 像素艺术生成（角色、瓦片、物体）
• ElevenLabs — AI 音频/语音生成（音效、配音、音乐）
• Godot MCP  — Godot 项目控制（创建场景、运行项目）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A) 立即配置 — 我会提供设置指南
B) 稍后配置 — 下次启动时再提醒我
C) 暂不需要 — 保存选择，以后不再询问
D) 跳过此步骤 — 暂不决定，下次继续询问

详细配置指南：`.opencode/docs/mcp-setup-guide.md`
```

**AFTER user answers**:
1. **IF A (立即配置)**:
   - Show brief setup guide reference
   - ASK which servers to enable: "你想启用哪些服务器？"
   - Provide links: PixelLab (https://pixellab.ai/dashboard), ElevenLabs (https://elevenlabs.io)
   - APPEND MCP status to `project-context.md`

2. **IF B (稍后配置)**:
   - Write `Status: pending` to `project-context.md`
   - Say "好的，下次启动时会再次提醒你"

3. **IF C (暂不需要)**:
   - Write `Status: declined` to `project-context.md`
   - Say "已记录你的选择，以后不再询问。你可以随时查阅 `.opencode/docs/mcp-setup-guide.md`"

4. **IF D (跳过)**:
   - Do NOT write anything (will ask again next session)
   - Say "好的，我们继续"

5. **STOP**: Wait for user response before proceeding to Phase 3

---

## Phase 3: Project Stage Check

**IF config already has project stage**:
- Skip this phase, use stored value

**ELSE, ASK**:
```
你目前处于哪个阶段？

A) 还没有想法 — 我想从头探索游戏概念
B) 有模糊想法 — 我有个大致的主题或类型
C) 概念已清晰 — 我知道核心玩法，但还没文档化
D) 已有工作成果 — 我已经有设计文档、原型或代码
```

**AFTER user answers**:
1. **APPEND to `.opencode/project-context.md`**:
   ```markdown
   ## Project Stage
   - **Current Stage**: [用户选择的选项]
   - **Last Updated**: [当前日期]
   ```
2. **STOP**: Wait for user's answer before writing.

**IF MCP servers are enabled**:
```
💡 MCP 增强提示：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PixelLab 启用时:
  → /art-coordinator 可自动生成像素资产
  → /prototype-mode 可快速创建角色动画

ElevenLabs 启用时:
  → /prototype-mode 可生成音效原型
  → 音频资产请求流程集成 AI 音效生成

Godot MCP 启用时:
  → /godot-specialist 可直接操作场景文件
  → 自动创建节点、加载贴图、运行项目验证
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 4: Route Based on Team + Stage

### Single Developer (单人)

| Stage | Recommend | Next Steps |
|-------|-----------|------------|
| 没有想法 | `/brainstorm` | 探索概念 |
| 模糊想法 | `/brainstorm "idea"` | 发展想法 |
| 概念清晰 | `/setup-engine` → `/sprint-plan` | 开始开发 |
| 已有成果 | `/code-review` 或 `/design-review` | 检查质量 |

### 2-3 Person Team (小队队长)

| Stage | Recommend | Additional Skills |
|-------|-----------|-------------------|
| 没有想法 | `/brainstorm` | 团队讨论概念 |
| 模糊想法 | `/brainstorm` → `/game-designer` | 定义系统 |
| 概念清晰 | `/setup-engine` → `/art-coordinator` | 美术协调 |
| 已有成果 | `/producer` → `/sprint-plan` | 团队进度 |

### Team Lead Tools

**如果用户选择了B或C（小队）**:
```
作为小队队长，你可以使用：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
管理:     /producer, /sprint-plan
技术:     /godot-specialist, /code-review
设计:     /design-review, /game-designer
美术协调: /art-coordinator (NEW!)
原型:     /prototype-mode (NEW!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 5: Hand Off

Once user confirms their next action:

**TELL USER**:
```
✅ 项目信息已保存到 `.opencode/project-context.md`
下次会话将自动读取，无需重复回答。
```

**TELL USER (新内容)**:
```
📌 下次新会话时，使用 `/resume` 快速恢复上下文，无需重新走完整流程。
```

**IF MCP was configured**:
```
📌 MCP 配置状态：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
已启用服务器: [列出用户启用的服务器]
配置文件: .opencode/mcp.json
详细指南: .opencode/docs/mcp-setup-guide.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**IF MCP was declined**:
- Do not show MCP status message

**For single developer**:
- Suggest the primary skill and let them invoke it

**For team lead (2-3 people)**:
- Suggest primary skill + mention team-specific tools
- **IF有美术队友**: 特别推荐 `/art-coordinator`
- **IF需要快速验证**: 推荐 `/prototype-mode`
- **IF MCP enabled**: Highlight MCP-enhanced workflow

**DO NOT invoke other skills automatically.** Let the user invoke them.

---

## Team Lead Workflow

### Weekly Cycle (推荐)

```
周一: /sprint-plan review → 检查进度
周三: /art-coordinator → 美术同步  
周五: /producer → 周总结
```

### New Feature Flow

```
/design-review → 验证设计
    ↓
/art-coordinator → 请求美术资产
    ↓
/godot-specialist → 技术实现
    ↓
/code-review → 质量检查
```

---

## Error Handling

| Error | Fallback |
|-------|----------|
| Cannot read files | Assume project is empty, proceed to Phase 2 |
| `project-context.md` incomplete | Ask only missing sections, preserve existing |
| User gives unclear answer | Ask clarifying question, do NOT guess |
| User wants to skip onboarding | Say "好的，你可以随时使用 `/help` 查看可用命令" and stop |

---

## Persistent Config File

**Location**: `.opencode/project-context.md`

**Purpose**: Store team structure, project stage, platform info to avoid re-asking on new sessions.

**Created by**: `/start` skill (Phase 2 & 3)

**Updated by**: `/setup-engine` (engine info), `/brainstorm` (vision), other skills

**快速恢复**: `/resume` skill 可在新会话中自动读取此文件，无需重复 `/start` 流程。

**Template**: `.opencode/docs/templates/project-context-template.md`

---

## Quick Reference

### 单人开发者

| 状态 | 首选 Skill |
|------|------------|
| 新会话恢复 | `/resume` |
| 没想法 | `/brainstorm` |
| 有想法 | `/brainstorm "idea"` |
| 概念清晰 | `/setup-engine` |
| 已有代码 | `/code-review` |

### 小队队长 (2-3人)

| 状态 | 首选 Skill | 额外工具 |
|------|------------|----------|
| 新会话恢复 | `/resume` | — |
| 没想法 | `/brainstorm` | 团队讨论 |
| 概念清晰 | `/setup-engine` | `/art-coordinator` |
| 已有成果 | `/producer` | `/sprint-plan` |
| 需美术 | `/art-coordinator` | 资产请求模板 |
| 快速验证 | `/prototype-mode` | 一次性代码模式 |