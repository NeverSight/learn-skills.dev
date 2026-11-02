---
name: brainstorm
description: Explore game ideas from scratch using professional frameworks — MDA, player psychology, verb-first design. Develops vague concepts into formalized game concepts.
license: MIT
phase_automation:
  auto_proceed_default: false
  user_override_command: "/manual"
  phases:
    - phase: "Phase 1: Initial Context"
      auto_conditions:
        - condition_type: "game_type_detected"
          action_if_met: "proceed"
          notification: "🎮 检测到游戏类型，自动进入问卷..."
          target_phase: "Phase 2.5"

    - phase: "Phase 7: Save"
      auto_conditions:
        - condition_type: "save_success"
          action_if_met: "proceed"
          notification: "✅ 游戏概念已保存！启动玩家评估..."
          trigger_on_approval: true

    - phase: "Phase 8: Player Evaluation"
      auto_conditions:
        - condition_type: "user_approved"
          action_if_met: "invoke_skill"
          skill: "player-evaluator"
          notification: "🚀 自动启动 player-evaluator..."
          trigger_on_approval: true
---

# Brainstorm Skill

Guided ideation using professional game design frameworks. Develops vague concepts into formal game concept documents.

---

## ⚠️ EXECUTION RULES

1. **ONE PHASE PER TURN** — Execute only one phase, then STOP and wait for user
2. **ASK BEFORE WRITING** — Never write files without explicit approval
3. **KEEP IT CONVERSATIONAL** — This is a dialogue, not a form
4. **IF USER WANTS TO SKIP** — Jump to Phase 6 (Output) with what we have

---

## Phase 1: Initial Context

**ASK ONE QUESTION** based on invocation:

| Invocation | Action |
|------------|--------|
| `/brainstorm` | Ask: "你想做什么类型的游戏？有什么特别的感受想给玩家吗？" |
| `/brainstorm "idea"` | Ask: "'[idea]' 这个想法里，最让你兴奋的是什么？" |
| `/brainstorm open` | Ask: "告诉我你最近玩过且喜欢的游戏，我们一起分析为什么它吸引你。" |

**STOP**: Wait for user response. Do NOT proceed until answered.

---

## Phase 2: Core Concept Discovery

Based on user's answer, explore **ONE** of these areas (user's choice):

### Option A: Player Experience
- "你希望玩家感受到什么？" (e.g., 紧张、成就感、探索欲)
- "玩家会做什么动作？" (core verbs: 探索、战斗、建造...)

### Option B: Theme & Setting
- "游戏发生在什么世界？" (奇幻、科幻、现代...)
- "你想要什么风格？" (严肃、轻松、黑暗、希望...)

### Option C: Core Loop
- "玩家会重复做什么？"
- "什么让他们想再来一次？"

**STOP**: Ask user which area to explore, or if they want to proceed to structure.

---

## Phase 2.5: Game-Type Questionnaire (NEW)

**IF game type identified** (from Phase 1 or 2), load corresponding questionnaire:

| Game Type | Questionnaire File |
|-----------|-------------------|
| Tower Defense | `.opencode/docs/questionnaires/tower-defense.md` |
| Roguelike / Roguelite | `.opencode/docs/questionnaires/roguelike.md` |
| ARPG / Action RPG | `.opencode/docs/questionnaires/arpg.md` |
| Platformer | `.opencode/docs/questionnaires/platformer.md` |
| Puzzle | `.opencode/docs/questionnaires/puzzle.md` |

**ASK**: "I detected this is a [game type]. Let me ask some specific questions for this type..."

**READ**: Load questionnaire file based on detected game type

**STOP**: Complete questionnaire questions, then proceed to Phase 3.

**IF game type unclear or mixed**:
- **ASK**: "Your concept involves multiple genres. Which is the primary focus?"
- Proceed with primary type's questionnaire, note secondary influences

### How to Detect Game Type

Keywords to watch for:

| Type | Keywords |
|------|----------|
| Tower Defense | "tower", "waves", "defense", "strategic placement" |
| Roguelike | "permadeath", "procedural", "run-based", "meta progression" |
| ARPG | "action combat", "skills", "equipment", "real-time" |
| Platformer | "jump", "platforms", "gravity", "side-scrolling" |
| Puzzle | "solve", "logic", "match", "brain teaser" |

---

## Phase 3: Structure the Concept

Use **ONE** framework to organize (ask user which):

### MDA Analysis (Quick)
| Layer | Question | Your Concept |
|-------|----------|--------------|
| Aesthetics | 玩家感受什么？ | |
| Dynamics | 产生什么行为？ | |
| Mechanics | 需要什么规则？ | |

### Design Pillars (3 max)
Define 2-3 foundational principles:
1. [Pillar 1] — e.g., "策略深度而非反应速度"
2. [Pillar 2] — e.g., "有意义的选择"
3. [Pillar 3] — e.g., "涌现式叙事"

**STOP**: Show the structure, ask "这个框架符合你的想法吗？需要调整吗？"

---

## Phase 4: Scope Check

Present scope options:

| Scope | Team | Duration | Features |
|-------|------|----------|----------|
| **Jam** | Solo | 48h-1w | 1-2 core mechanics |
| **Small** | Solo/2-3 | 1-6mo | 3-5 systems |
| **Medium** | 3-10 | 6-18mo | Multiple systems |

**ASK**: "你的项目规模目标是什么？"

**STOP**: Wait for user's scope decision.

---

## Phase 5: Engine Recommendation

Based on concept, suggest engine:

| Concept Type | Recommendation |
|--------------|----------------|
| 2D game | Godot 4 (excellent 2D support) |
| 2D/3D mix | Godot 4 or Unity |
| AAA 3D | Unreal 5 |
| Mobile cross-platform | Unity |

**ASK**: "你倾向哪个引擎？"

**STOP**: Wait for user's engine preference.

---

## Phase 6: Generate Output

Present the **Game Concept Document** for approval:

```markdown
# [Game Title]

## Elevator Pitch
[1-2 sentence description]

## Design Pillars
1. [Pillar 1]
2. [Pillar 2]
3. [Pillar 3] (optional)

## Core Loop
1. [Action]
2. [Reward]
3. [Progression]

## Target Player
[Player persona description]

## Key Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

## Scope
[Size and timeline estimate]

## Recommended Engine
[Engine] — [Reasoning]

## Next Steps
1. /setup-engine [engine]
2. Design core systems
3. Prototype core mechanic
```

**ASK**: "我可以把这个保存到 `design/gdd/game-concept.md` 吗？"

**STOP**: Wait for explicit approval.

---

## Phase 7: Save (Only After Approval)

**IF USER APPROVES**:
- Create directory if needed: `design/gdd/`
- Write file: `design/gdd/game-concept.md`
- Say: "✅ 已保存到 design/gdd/game-concept.md"
- **NEW**: 自动触发 Phase 8 (玩家评估)

**IF USER WANTS CHANGES**:
- Make changes, re-present, ask for approval again

**STOP**: After saving or if user declines.

---

## Phase 8: Player Evaluation (NEW)

> **自动触发**: Phase 7 保存成功后自动执行

### Step 1: 询问是否评估

**ASK**:
```
游戏概念已保存！是否从玩家视角评估这个概念？

A) 是，启动玩家评估 (推荐)
B) 跳过，稍后再评估
C) 手动选择评估视角

评估将:
- 从多个玩家视角评估游戏概念
- 识别有趣性、参与度、学习曲线等问题
- 提供具体的改进建议
```

**STOP**: Wait for user's choice.

### Step 2: 调用 Player Evaluator Skill

**IF user selects A or C**:

```
正在启动 player-evaluator skill...
```

**EXECUTE**: `/player-evaluator`

**该 skill 将**:
1. 读取 `design/gdd/game-concept.md`
2. 自动选择 4-6 个玩家视角 (基于目标玩家)
3. 并发启动多个评估任务
4. 生成评估报告到 `design/gdd/player-evaluation-report.md`

### Step 3: 处理评估结果

**AFTER player-evaluator completes**:

**READ**: `design/gdd/player-evaluation-report.md`

**PRESENT摘要**:
```
评估完成！

**整体评分**: [X]/5
**首要优点**: [Top strength]
**首要担忧**: [Top concern]

**关键改进建议**:
1. [建议1]
2. [建议2]
3. [建议3]

选择:
A) 查看完整报告
B) 讨论如何改进
C) 继续下一步 (setup-engine)
```

**STOP**: Wait for user's choice.

### Step 4: 可选 - 迭代改进

**IF user wants to improve**:

- 使用 `/game-designer` 实施改进建议
- 重新运行 `/player-evaluator` 验证
- 更新 `game-concept.md`

**STOP**: After user is satisfied or wants to continue.

---

## Error Handling

| Error | Fallback |
|-------|----------|
| User gives very short answers | Ask follow-up questions, don't assume |
| User seems confused by frameworks | Skip framework, just summarize what they said |
| User wants to quit | Say "好的，你可以随时继续。想保存目前的想法吗？" |
| Cannot create directory | Ask user to create `design/gdd/` manually, then retry |
| Player evaluator fails | Report error, offer to skip or retry |
| No game-concept.md found | Skip Phase 8, proceed to next step |

---

## Quick Reference

| Phase | Purpose | End With |
|-------|---------|----------|
| 1. Context | Understand starting point | User's initial idea |
| 2. Discovery | Explore core elements | User's choice of focus |
| 2.5. Questionnaire | Game-type specifics | Completed type questions |
| 3. Structure | Apply framework | User's approval of structure |
| 4. Scope | Set realistic goals | User's scope decision |
| 5. Engine | Technology choice | User's engine preference |
| 6. Output | Generate document | User's approval to save |
| 7. Save | Write file | Confirmation |
| 8. Evaluation | Player perspective review | Evaluation report |