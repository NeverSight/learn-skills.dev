---
id: research-idea-convergence
name: Research Idea Convergence
version: 1.0.0
description: |-
  Generates 2-4 candidate research directions from survey results, presents them with pros/cons for user selection, and converges to a publishable angle.
stages: ["ideation"]
tools: ["read_file", "search_project", "write_file"]
summary: |-
  Interactive research direction selection. Reads survey reports and gap analysis, generates 2-4 candidate research directions with pros/cons/feasibility, and waits for user selection before writing the final publishable angle.
primaryIntent: ideation
intents: ["ideation", "research"]
capabilities: ["research-planning"]
domains: ["academic"]
keywords: ["research-idea-convergence", "idea selection", "research direction", "publishable angle", "candidate", "convergence", "interactive", "ideation"]
source: builtin
status: verified
resourceFlags:
  hasReferences: false
  hasScripts: false
  hasTemplates: true
  hasAssets: false
  referenceCount: 0
  scriptCount: 0
  templateCount: 1
  assetCount: 0
  optionalScripts: false
---

# Research Idea Convergence

## Canonical Summary

Interactive research direction selection for academic projects. Generates multiple candidate research directions from survey/literature results, presents them with structured comparison for user selection, then converges to a final publishable angle.

## Trigger Rules

Use this skill when:
- The project enters the **ideation** stage after completing the survey stage
- The user asks about research direction, publishable angle, or idea selection
- The current task involves generating or selecting a research direction

**Do NOT use this skill when:**
- The user has already decided on a specific research direction and just wants to refine it
- The project is still in the survey stage (use survey skills instead)

## Execution Contract

- Resolve every relative path from this skill directory first.
- Do not write generated artifacts back into the skill directory; save them inside the active project workspace.
- **Never skip the user selection checkpoint** — this is the core purpose of this skill.

## Working Rules

1. Read existing survey outputs before generating candidates.
2. Generate **2-4 candidate directions**, no more, no fewer.
3. Each candidate must be concrete enough to evaluate (not vague platitudes).
4. **[USER_CHECKPOINT]** — Always stop and wait for user selection. Never auto-select.
5. Only after user confirmation, write the final direction to output files.

## Step-by-step Instructions

### Step 1 — Read Survey Context

Read all available survey outputs to understand the research landscape:

| File | Purpose |
|------|---------|
| `.pipeline/docs/research_brief.json` | Research topic, goal, target venue |
| `.viewerleaf/research/Survey/reports/*.md` | Literature screening, gap summary |
| `.pipeline/tasks/tasks.json` | Current task states and progress |

Extract:
- **Research domain** and specific problem area
- **Key gaps** identified in the literature
- **Strong baselines** that exist (traditional and learning-based)
- **Available datasets / experimental platforms**
- **Target venue** constraints (if specified)

### Step 2 — Generate Candidate Directions

Produce **2-4 candidate research directions**. For each candidate, provide:

```markdown
## 候选方向 N：[方向名称]

**核心思路：** [1-2 句技术路线和创新点]

**研究问题：** [具体要回答的科学问题]

**方法概要：**
- [关键技术 1]
- [关键技术 2]
- ...

**对标基线：**
- [需要对比的已有方法 1]
- [需要对比的已有方法 2]

**目标刊物：** [适合投稿的会议/期刊]

**✅ 优势：**
- [优势 1]
- [优势 2]

**⚠️ 风险：**
- [风险 1]
- [风险 2]

**可行性评分：** ⭐⭐⭐⭐☆ (x/5)
- 实验资源: x/5
- 时间可控: x/5
- 技术难度: x/5
- 发表潜力: x/5
```

### Candidate Generation Principles

1. **差异化** — 候选方向之间应有明显区别（不同技术路线、不同创新角度、不同应用场景）
2. **可比性** — 使用统一的评估维度，方便用户横向对比
3. **务实性** — 考虑用户的实际资源（本科 vs 硕博、实验周期、计算资源）
4. **梯度风险** — 包含保守稳妥的方向和激进创新的方向，让用户在风险与收益之间选择

### Step 3 — Present Comparison Table

在列出所有候选方向后，给出一个汇总对比表：

```markdown
## 📊 候选方向对比

| 维度 | 方向 1 | 方向 2 | 方向 3 |
|------|--------|--------|--------|
| 创新性 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 可行性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 发表潜力 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 实验周期 | 2 周 | 4 周 | 6 周 |
| 推荐度 | 🟡 稳妥 | 🟢 推荐 | 🔴 激进 |
```

### Step 4 — USER CHECKPOINT ⛔

> **[USER_CHECKPOINT] — 必须在此处停下，等待用户回复。**
>
> 向用户提问：
> 1. 你倾向于哪个方向？
> 2. 是否需要组合某些方向的元素？
> 3. 有没有你自己的想法想要加入？
> 4. 对某个方向的风险有没有顾虑？
>
> **绝对不要跳过这一步。不要替用户做选择。**

等用户明确选择后，再进入 Step 5。

### Step 5 — Converge and Write

用户确认后：

1. **写入 publishable_angle.md**
   ```
   路径: .viewerleaf/research/Ideation/publishable_angle.md
   ```
   包含：选定方向的完整描述、用户的修改意见（如有）、对标基线、预期贡献

2. **更新 research_brief.json**
   ```
   路径: .pipeline/docs/research_brief.json
   ```
   更新 `briefGoal` 和 `stageNotes.ideation`

3. **更新 tasks.json**
   ```
   路径: .pipeline/tasks/tasks.json
   ```
   标记 ideation 任务完成，触发下一阶段任务

4. **记录选择理由**
   在 `publishable_angle.md` 末尾附加：
   ```markdown
   ## 选择记录
   - 候选方向数：N 个
   - 用户选择：方向 X [+ 用户修改内容]
   - 选择理由：[用户给出的理由或综合分析]
   - 弃选方向：方向 Y (原因)、方向 Z (原因)
   ```

## Output Templates

### publishable_angle.md

Use `templates/publishable_angle.template.md`:

```markdown
# Publishable Angle

## 研究方向
[选定方向名称]

## 核心创新点
[1-2 句话概括]

## 研究问题
[具体要回答的科学问题]

## 方法概要
- ...

## 对标基线
- ...

## 预期贡献
- ...

## 目标刊物
[期刊/会议名称]

## 选择记录
- 候选方向数：N 个
- 用户选择：方向 X
- 选择理由：...
```

## Integration with Other Skills

| Upstream | This Skill | Downstream |
|----------|-----------|------------|
| `research-literature-trace` (survey reports) | → 读取 gap/baseline 信息 | |
| `research-pipeline-planner` (brief) | → 读取研究主题和目标 | |
| | 生成候选 → 用户选择 → 写入 | → `inno-idea-eval` (评审选中方向) |
| | | → `inno-experiment-dev` (实验设计) |

## Notes for LLMs

1. **核心原则**：这个 skill 的价值在于**交互**，不在于生成。生成候选只是手段，让用户做出知情选择才是目的。
2. **不要跳过 USER_CHECKPOINT**：即使用户看起来已经有偏好，也要完整展示所有候选并明确收集确认。
3. **不要过度推荐**：可以标注"推荐"但不要暗示只有一个正确答案。每个方向都有其适用场景。
4. **尊重用户原有思路**：如果用户已有初步想法，把它作为候选之一纳入对比，而不是忽略。
5. **差异化很重要**：不要生成几个只有微小差别的方向，那等于没给选择。技术路线、创新角度、目标场景应有明显区分。
