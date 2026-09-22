---
name: smart-learn
description: 独立学习技能，基于费曼学习法的五步闭环。触发方式：输入 /smart-learn 主题，或说"教我XX"、"帮我系统学习XX"。每学完一步自动同步更新 Word 文档 + Mermaid 思维导图。
context: inline
---

# Smart Learn — 增量内联学习技能

基于费曼学习法五步闭环。纯 Markdown 零依赖可用；可选 `pip install python-docx` 获得 Word 文档功能。每一步学习成果同步更新到 **Word 文档** + **Mermaid 思维导图**，全程实时生长。

## 触发

- `/smart-learn 主题名`
- "教我 Kubernetes 网络模型"
- "帮我系统学习 DDD"
- 任何表达出"想系统掌握一个复杂主题"的意图

### 不触发

- 简单定义（"X是什么"）
- 信息查询（"帮我查一下X"）
- 内容总结（"总结这篇文章"）

## 核心原则

1. **禁止使用 Agent 工具** — 所有步骤由主对话直接执行
2. **每步可见** — 输出实时展示，用户确认后进入下一步
3. **自然对话** — 不用弹窗确认，用户用自然语言回应即可
4. **零外部依赖（核心）** — Markdown 学习 + 存储不依赖任何第三方包
5. **三格式持久化** — .md（知识库笔记，始终生成） + .docx（Word文档，可选） + Mermaid 思维导图（零依赖，始终生成）

---

## 初始化（Word 文档 + 思维导图）

学习开始前，同时初始化 Word 文档和 Mermaid 思维导图。Word 失败不影响核心流程；思维导图零依赖始终可用。

```bash
# 思维导图（零依赖，始终生成）
python .claude/skills/smart-learn/mindmap_utils.py init \
  --topic "主题名" \
  --output-dir "knowledge_store"

# Word 文档（可选，需 python-docx）
python .claude/skills/smart-learn/docx_utils.py init \
  --topic "主题名" \
  --output-dir "knowledge_store"
```

- 记录 `MINDMAP_FILE` 和 `MINDMAP_DATA` 路径，后续每步同步更新
- 如果 docx init 返回 `"status": "no_docx"` → 告知用户可 `pip install python-docx`，继续执行
- **智能入口检测**：初始化时按以下顺序检查已学记录，以**非阻塞提示**方式告知用户（不中断流程，用户无需回应即可继续）：
  1. 检查 `knowledge_store/{主题slug}_checkpoint.json` → 存在 = 有未完成学习
  2. 检查 `knowledge_store/{主题}.md` 或 `knowledge_store/{主题}_学习笔记.docx` → 存在 = 已学完
  3. 检查 `knowledge_store/` 下文件名含关键词的笔记 → 存在 = 有相关知识

  根据检测结果，在初始化日志中附带提示（不阻塞，不等用户选择）：
  - **有未完成学习** → 告知"💡 检测到未完成的学习（步骤N/5）。输入 `继续` 可续学，或正常开始全新学习"
  - **已学完该主题** → 告知"💡 你已学过「{主题}」。需要复习时随时输入 `/smart-review {主题}`"
  - **有相关主题笔记** → 告知"💡 检测到相关笔记「{主题}」，步骤4将自动关联"
  - **无任何记录** → 正常开始
  - 用户如果回应"继续上次" → 跳转到对应步骤恢复
  - 用户如果回应"复习" → 切换到复习流程
  - **用户不回应 → 不阻塞，直接进入步骤1**
  - 每完成一步 → 更新 checkpoint（`{"topic":"...", "last_step": N, "mindmap_data":"...", "docx_path":"..."}`）

---

## 五步工作流

每一步的核心输出格式保持不变。Word 写入是每步末尾的附加操作。

---

## 步骤0：前置评估（可选，仅在用户表明已有基础时触发）

**触发条件**：用户说"我已经了解XX部分"、"XX我比较熟"、"跳过基础直接讲进阶"等。

**不触发**：用户直接说"/smart-learn 主题"不带任何基础说明 → 跳过步骤0，正常从步骤1开始。

**执行**：
1. 仍然先执行步骤1生成完整概念地图（确保知识结构完整）
2. 概念地图展示给用户后，额外询问："你对哪些概念已经比较熟悉？"
3. 用户可多选或描述（如"1、2、3 我熟 / 前三个入门的基本都会"）
4. 为每个概念打上用户掌握度标记：
   - 🟢 熟悉 → 步骤2 只讲核心思想+一句话（跳过完整五维），步骤3 只出 1 道边界层题
   - 🟡 了解 → 步骤2 正常讲但可精简，步骤3 正常出题
   - 🔴 新手 → 步骤2 完整五维，步骤3 从最合适层出题
5. **重要**：即使是"熟悉"的概念，仍要写入 Markdown 笔记和思维导图（确保笔记完整性），只是在对话中加速讲解。Word 文档中标注 `[已掌握]`。

**约束**：
- 步骤0 是可选加速器，不改变五步闭环结构
- 用户标记为"熟悉"的概念 ≠ 不学，只是讲得更快、题更少
- 如果用户发现"熟悉"的概念实际不熟（步骤3答错），自动降级为 🔴 并完整补充

1. 调用 WebSearch 搜索该主题的最新资料（中文优先，确保准确性和及时性）
2. 读取 `templates/1-concept-map.md` 按模板执行
3. 将主题拆解为 5~8 个子概念，按学习依赖排序，标注难度

**固定输出格式**：
```
## 📊 概念地图：{主题}

1. {概念名}（{难度}）→ {一句话解决什么问题}
   ↓
2. {概念名}（{难度}）→ {一句话解决什么问题}
   ↓
...
```

输出后等待用户回应：
- "继续" / "OK" → 进入步骤2
- "调整XX" → 修改概念地图 → 重新输出 → **重新执行 mindmap 和 Word 同步（覆盖更新）** → 重新询问确认

**→ 保存检查点**（中断恢复用）：
```bash
python -c "import json; json.dump({'topic':'{主题}','last_step':1}, open('knowledge_store/{主题slug}_checkpoint.json','w'))"
```

**→ 同步到思维导图**（始终执行）：
```bash
python .claude/skills/smart-learn/mindmap_utils.py update \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" --step 1 \
  --concepts '[{"name":"概念1","difficulty":"入门","purpose":"解决问题X"}, ...]'
```
执行后告知用户：`🧠 思维导图已更新：knowledge_store/{主题}_思维导图.md`

**→ 写入 Word**（如果 DOCX_PATH 存在）：
```bash
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" --step 1 --title "概念地图" \
  --content-file /tmp/smart-learn-step1.md
```
执行后告知用户：`📄 Word 文档已更新：knowledge_store/{主题}_学习笔记.docx`

---

### 步骤 2：费曼解释

读取 `templates/2-feynman.md` 按模板执行。对步骤1中的每个概念，逐一用五维框架解释。

**每个概念的固定输出结构**：
```markdown
### {序号}. {概念名}

**为什么需要？** → {背景与动机，旧方案有什么问题}
**核心思想** → {一句话说清本质}
**类比理解** → {日常场景类比，完全非技术领域}
**示例** → {最小可运行的代码/真实场景}
**一句话** → {离开后能记住的那句}
```

**每个概念的执行顺序（严格遵守，不可跳过任何一步）**：

```
1. 输出该概念的五维解释
        ↓
2. ⚡ 执行 mindmap 同步命令（必须实际运行 Bash，不可只声明）
        ↓
3. ⚡ 将解释内容写入临时文件，执行 Word 写入命令（必须实际运行 Bash）
        ↓
4. 告知用户文件已更新（显示路径）
        ↓
5. 询问用户：继续 / 修改 / 换类比 / 提问
```

**用户回应后的处理**：

| 用户回应 | 处理方式 |
|---------|---------|
| "继续" / "下一个" | 已完成同步，直接讲下一个概念 |
| "修改XX部分" | 按反馈调整解释 → 重新执行步骤 1→2→3→4→5（mindmap 覆盖更新，Word 以 `{概念名}（修正）` 追加修订版） |
| "换一个类比" / "没懂" | 用不同类比重讲，用户确认后执行步骤 2→3→4→5 |
| 任意提问 | 针对性解答，确认后继续 |

**→ 同步到思维导图**（每概念确认后必须执行）：
```bash
python .claude/skills/smart-learn/mindmap_utils.py update \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" --step 2 \
  --concept "{概念名}" --core "{核心思想摘要}" --analogy "{类比关键词}"
```
执行后告知用户：`🧠 已同步到思维导图：knowledge_store/{主题}_思维导图.md`

**→ 写入 Word**（每概念确认后必须执行）：
```bash
# 先将该概念的完整 Markdown 解释写入临时文件
cat > /tmp/smart-learn-step2-concept.md << 'EOF'
### {序号}. {概念名}

**为什么需要？**
{解释内容}
...
EOF
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" --step 2 --title "{序号}. {概念名}" \
  --content-file /tmp/smart-learn-step2-concept.md
```
执行后告知用户：`📄 已写入 Word：knowledge_store/{主题}_学习笔记.docx`

全部概念讲完后，用 3~5 句话串联串讲，然后进入步骤3。

**禁止**：
- 用未解释的术语解释另一个术语
- 从定义开始（必须从"为什么需要"开始）
- 类比用另一个技术概念
- **声明"已同步"但未实际执行 Bash 命令**（这是最严重的执行错误）

---

### 步骤 3：递进式自测

读取 `templates/3-self-test.md` 按模板执行。为每个概念出 1 道题，从三层中选最合适的一层：

| 层次 | 考察目标 | 适合什么概念 |
|------|---------|------------|
| 理解层 | 改变条件问变化 | 核心机制类（如缓存策略） |
| 应用层 | 新场景设计方案 | 工程实践类（如API设计） |
| 边界层 | 什么时候失效 | 理论约束类（如CAP定理） |

**每题的执行顺序（严格遵守）**：

```
1. 出题，等待用户回答
        ↓
2. 给出点评 + 参考答案 + 掌握度
        ↓
3. ⚡ 如果是 ❌ 薄弱 → 执行 mindmap 标记命令
        ↓
4. ⚡ 执行 Word 写入命令（含题目+回答+点评+参考答案）
        ↓
5. 告知用户文件已更新
        ↓
6. 出下一道题（或汇总）
```

**逐个提问**，每次只出一道题。用户回答后给出：
- **点评**：具体评价哪里好、哪里不足
- **参考答案**：一个高质量的示范回答
- **掌握度**：✅ 已掌握 / ⚠️ 部分掌握 / ❌ 薄弱

全部完成后汇总薄弱点，询问用户：
- "继续" → 进入步骤4
- "回顾薄弱概念" → 对每个 ❌ 薄弱概念：
  1. 用不同的类比重新解释该概念（不重复步骤2的原版）
  2. 出一道新的同类层级的题目
  3. 用户回答后点评
  4. 直到掌握度变为 ✅/⚠️ 或用户说"先继续"
  5. 更新思维导图移除该概念的 ⚠️ 标记（如果已掌握）
  6. **薄弱概念回顾的每一步也要同步到 Word（追加"回顾修正"记录）**

**→ 同步到思维导图**（每题点评后，❌ 薄弱则必须执行）：
```bash
python .claude/skills/smart-learn/mindmap_utils.py update \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" --step 3 \
  --concept "{概念名}" --weak "{薄弱原因摘要}"
```
执行后告知用户：`🧠 {概念名} 已标记薄弱点到思维导图`

**→ 写入 Word**（每题点评后必须执行）：
```bash
cat > /tmp/smart-learn-step3-q.md << 'EOF'
**问题**：{题目}
**你的回答**：{用户回答摘要}
**点评**：{点评}
**参考答案**：{参考答案}
**掌握度**：{✅/⚠️/❌}
EOF
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" --step 3 --title "{概念名} — 自测" \
  --content-file /tmp/smart-learn-step3-q.md
```
执行后告知用户：`📄 自测记录已写入 Word`

---

### 步骤 4：关联内化

读取 `templates/4-association.md` 按模板执行。

1. 用 Glob 检查 `knowledge_store/` 下已有的学习笔记
2. 如果有相关主题，做四维对比：
   - 解决的是同一个问题吗？
   - 哪些经验可以直接迁移？
   - 新概念有什么独特性？
   - 知识地图中位置关系？
3. 如果没有，告知"这是该领域的第一个知识节点"
4. 输出文本版知识网络图

**步骤4的执行顺序（严格遵守）**：

```
1. 检索并输出知识网络图
        ↓
2. ⚡ 对每个关联主题执行 mindmap 关联命令
        ↓
3. ⚡ 执行 Word 写入命令（含对比表格和网络图）
        ↓
4. 告知用户文件已更新
        ↓
5. 询问用户：继续 / 补充关联
```

用户回应：
- "继续" → 进入步骤5
- "补充关联" → 用户提出更多关联角度 → 追加分析 → 重新执行步骤 2→3→4（mindmap 自动去重，Word 追加新关联）

**→ 同步到思维导图**（每个关联主题必须执行）：
```bash
python .claude/skills/smart-learn/mindmap_utils.py update \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" --step 4 \
  --assoc-target "{关联主题名}" --assoc-relation "{一句话关系}"
```
执行后告知用户：`🧠 知识关联已添加到思维导图`

**→ 写入 Word**（必须执行）：
```bash
cat > /tmp/smart-learn-step4.md << 'EOF'
{关联分析的对比表格和网络图内容}
EOF
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" --step 4 --title "关联内化" \
  --content-file /tmp/smart-learn-step4.md
```
执行后告知用户：`📄 关联分析已写入 Word`

---

### 步骤 5：巩固总结并保存

读取 `templates/5-summary.md` 按模板执行。

**输出精华笔记**（≤500 字）：
```markdown
## 🎯 核心公式
{一句"懂了就懂了80%"的话}

## 🔑 三个关键点
1. {洞察一}
2. {洞察二}
3. {洞察三}

## ⚠️ 薄弱点
- **{具体薄弱点}**：{为什么容易搞混} → {正确理解}（首次标记：{今天日期}）

## 🏗️ 一句话类比
{日常场景一句话总结}

## 🏷️ 关键词
`{k1}` `{k2}` `{k3}` `{k4}` `{k5}`
```

输出精华笔记后等待用户回应：
- "保存" → 写入所有文件（见下方持久化步骤）
- "修改XX" → 调整对应部分 → 重新输出完整精华笔记 → 重新询问确认（确认后一次性写入所有文件）

**持久化**（用户确认后执行）：
1. **必做**：将完整五步报告写入 `knowledge_store/{主题slug}.md`
2. **必做**：最终化思维导图：
```bash
python .claude/skills/smart-learn/mindmap_utils.py finalize \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" \
  --summary "{核心公式}" \
  --weak-points "{薄弱点1; 薄弱点2}" \
  --keywords "{k1, k2, k3, k4, k5}"
```
3. **可选**：最终化 Word 文档：
```bash
python .claude/skills/smart-learn/docx_utils.py finalize \
  --file "{DOCX_PATH}" \
  --summary "{核心公式}" \
  --weak-points "{薄弱点1; 薄弱点2}" \
  --keywords "{k1, k2, k3, k4, k5}"
```

最后以可点击路径告知用户全部产出物位置：
- 📝 Markdown 笔记：`knowledge_store/{主题slug}.md`
- 🧠 思维导图：`knowledge_store/{主题}_思维导图.md`（Mermaid 格式，GitHub/VSCode 原生渲染）
- 📄 Word 文档：`knowledge_store/{主题}_学习笔记.docx`（如有）
- ⚠️ 薄弱点列表：（逐一列出）

**→ 清理临时文件和检查点**（学习完成）：
```bash
rm -f /tmp/smart-learn-step*.md /tmp/smart-learn-concept*.md
rm -f knowledge_store/{主题slug}_checkpoint.json
```

---

## 同步更新流程图

```
/smart-learn 主题
     │
     ├─ 初始化 ──→ 🧠 创建空白思维导图 + 📄 创建 Word（可选）
     │
     ├─ 步骤1 ──→ 🧠 写入概念节点 + 📄 写入概念地图
     │
     ├─ 步骤2 ──→ 🧠 每概念追加核心思想/类比 + 📄 写入解释
     │
     ├─ 步骤3 ──→ 🧠 标记薄弱点 ⚠️ + 📄 写入问答记录
     │
     ├─ 步骤4 ──→ 🧠 追加知识关联 🔗 + 📄 写入对比分析
     │
     └─ 步骤5 ──→ 🧠 最终化思维导图 + 📄 最终化 Word + 📝 Markdown
```

---

## 知识连续性

- 学习前检查 `knowledge_store/` 目录已有笔记
- 发现关键词匹配的旧笔记时，主动在步骤4做关联
- 所有笔记（.md + .docx + 思维导图.md）保存到同一目录，形成累积知识库

## 模板与工具

| 文件 | 用途 | 依赖 |
|------|------|------|
| `templates/1-concept-map.md` | 概念地图模板 | 无 |
| `templates/2-feynman.md` | 费曼解释模板 | 无 |
| `templates/3-self-test.md` | 递进式自测模板 | 无 |
| `templates/4-association.md` | 关联内化模板 | 无 |
| `templates/5-summary.md` | 巩固总结模板 | 无 |
| `mindmap_utils.py` | Mermaid 思维导图同步生成 | **零依赖** |
| `docx_utils.py` | Word 文档增量生成 | python-docx（可选） |
