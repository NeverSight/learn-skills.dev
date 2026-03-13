---
name: git-review
description: 分析指定时间范围内的 git 提交，生成工作复盘报告。触发词：复盘、review commits、git回顾、今天做了什么、工作总结、daily review、retrospective
allowed-tools: Bash
disable-model-invocation: true
---

# Git Review — 工作复盘工具

分析当前 git 仓库指定时间范围内的所有 commits，生成结构化的工作复盘报告。适用于代码、文档、设计、调研等任何 git 管理的内容。

## When to Use

当用户请求以下操作时触发：
- "复盘一下" / "今天做了什么" / "工作总结"
- "review commits" / "git 回顾" / "daily review"
- "这周干了什么" / "最近3天的工作" / "retrospective"
- 任何涉及回顾 git 提交历史并进行分析的请求

## Phase 0: 解析输入 — 确定时间范围

根据用户输入确定分析的时间范围：

**默认值**：昨天 22:00 到当前时间（覆盖跨午夜的工作段）

**自然语言映射**：
| 用户输入 | --after | --before |
|---------|---------|----------|
| 今天 / today | 今天 00:00 | now |
| 昨天 / yesterday | 昨天 00:00 | 昨天 23:59 |
| 这周 / this week | 本周一 00:00 | now |
| 最近N天 / last N days | N天前 00:00 | now |
| 具体日期 (如 2月20日) | 该日 00:00 | 该日 23:59 |
| 日期范围 (如 2/20-2/23) | 起始日 00:00 | 结束日 23:59 |
| 默认（无指定） | 昨天 22:00 | now |

使用 `date` 命令计算具体时间戳，转换为 git log 可用的格式（如 `2026-02-22T22:00:00`）。

## Phase 1: 数据采集

**前置检查**：先运行 `git rev-parse --is-inside-work-tree` 确认当前目录是 git 仓库。如果不是，告知用户并停止。

**拉取最新代码**：运行 `git pull` 确保分析基于最新的提交历史。如果拉取失败（网络问题、冲突等），忽略错误继续后续步骤，不要重试。

顺序执行以下 5 条命令（本地操作，无需并行）：

### 1. 完整提交记录

```bash
git log --after="{after}" --before="{before}" --format="%H|%an|%ai|%s|%b|||" --name-status
```

如果结果为空，**必须立即停止所有后续步骤**。不要尝试扩大时间范围、不要查找最近的提交、不要自行调整参数继续分析。只需：
1. 告知用户该时间范围内无提交
2. 展示最近 5 条提交的时间，帮助用户选择合适的范围
3. 建议用户指定时间范围（如"复盘昨天"、"复盘 2/22"、"最近3天"）
4. 等待用户下一步指示

### 2. 提交统计

```bash
git log --after="{after}" --before="{before}" --stat --format="%H %s"
```

### 3. 时间段整体变更统计

```bash
git diff --stat $(git log --after="{after}" --before="{before}" --format="%H" | tail -1)^..$(git log --after="{after}" --before="{before}" --format="%H" | head -1)
```

如果只有一条提交，使用 `git show --stat {hash}` 替代。

### 4. 分支信息

```bash
git branch -a --sort=-committerdate | head -20
```

### 5. 当前未完成工作

```bash
git status --short && echo "---STASH---" && git stash list
```

### 6. 当日个人记录（可选）

检查仓库是否有 `notes/daily_notes/` 目录及对应的每日记录文件（命名格式：`{YEAR}H{1|2}-daily-notes.md`，如 `2026H1-daily-notes.md`）：

```bash
find notes/daily_notes -name "*-daily-notes.md" 2>/dev/null | head -5
```

如果找到文件，提取时间范围内所有涉及日期的记录块。对于每个目标日期（格式 `YYYY-MM-DD`），执行：

```bash
# 提取该日期的记录块（从日期标题到下一个日期标题前）
awk '/^### {YYYY-MM-DD}/{f=1;next} /^### [0-9]{4}-[0-9]{2}-[0-9]{2}/{f=0} f' notes/daily_notes/{FILE}
```

如果文件不存在、或指定日期无记录，跳过此步骤，不影响后续分析。

## Phase 2: 七维度分析

基于采集到的数据，逐一完成以下分析。

### 维度 0: 当日记录（如有）

**仅当 Phase 1 步骤 6 采集到记录时执行此维度。**

- 完整展示该日期的个人记录原文（保留缩进和 checkbox 状态）
- 标注各条目状态：`[x]` 已完成 / `[ ]` 未完成 / `[-]` 无对应 commit
- 与 git commits 交叉比对：
  - 记录中 `[x]` 项是否能在提交中找到对应 commit？
  - 有哪些 commit 未在记录中提及（可能是临时修复或额外工作）？
  - 有哪些记录中计划的事项没有对应 commit（未完成或待明天继续）？

### 维度 1: 工作总结

- 将 commits 按逻辑主题分组（而非简单按时间排列）
- 用叙述式语言总结每组工作内容，说明做了什么、为什么做
- 附上提交时间线表格：`| 时间 | Hash (短) | 提交信息 |`

### 维度 2: 变更类型分布

按文件后缀和路径将变更分为以下类型，统计各类文件数和行数变更：

| 类型 | 匹配规则 |
|------|---------|
| 代码 | `.go`, `.py`, `.js`, `.ts`, `.java`, `.rs`, `.c`, `.cpp`, `.swift`, `.kt` 等 |
| 测试 | 路径含 `test`/`spec`/`_test`，或文件名含 `test`/`spec` |
| 文档 | `.md`, `.txt`, `.rst`, `.adoc`, `.doc` |
| 配置 | `.yaml`, `.yml`, `.json`, `.toml`, `.ini`, `.env`, `Dockerfile`, `Makefile` |
| 设计/调研 | 路径含 `design`/`research`/`rfc`/`proposal`/`audit`/`review` |
| 依赖 | `go.mod`, `go.sum`, `package.json`, `package-lock.json`, `requirements.txt`, `Cargo.toml`, `Gemfile` |
| 其他 | 以上都不匹配的文件 |

输出分类表格和饼图式占比。

### 维度 3: 工作节奏

- 绘制提交时间线（用文本表示，如每小时一格）
- 识别 Flow Session：连续提交间隔 < 30 分钟视为同一 session
- 统计：首次提交时间、末次提交时间、总跨度、session 数、最长 session、最长间隔
- 如果只有 1 条提交，跳过节奏分析，仅记录提交时间

### 维度 4: 提交实践评估

对提交习惯进行 1-5 分评分：

| 评估项 | 5分标准 | 1分标准 |
|--------|--------|--------|
| Message 质量 | 清晰描述 what + why | 模糊或无意义 (如 "update", "fix") |
| 粒度 (Granularity) | 每次提交是独立的逻辑单元 | 巨型提交混合多个不相关改动 |
| Conventional Commits | 遵循 `type(scope): description` | 无任何规范 |

给出每项的评分、好的示例（来自实际提交）和可改进的示例。

### 维度 5: 技术决策识别

扫描变更内容，识别以下类型的技术决策：
- **新依赖引入**：依赖文件的新增项
- **架构变更**：新目录结构、新模块、接口变更
- **重构**：大量文件重命名/移动、函数签名变更
- **安全相关**：涉及 auth、token、secret、permission 的改动
- **API 变更**：路由、端点、schema 的修改

每项列出具体 commit 和影响评估。如果没有识别到技术决策，简要说明。

### 维度 6: 完成度检查

以 checklist 格式检查：
- [ ] 是否有未提交的改动（`git status`）
- [ ] 是否有 stash 中的暂存工作
- [ ] 新增代码中是否包含 `TODO`/`FIXME`/`HACK`/`XXX` 注释
- [ ] 新增代码文件是否有配套测试文件（检查同名 `_test` 文件是否存在）

对每项给出 Pass/Warning/Info 标记和具体内容。

### 维度 7: 改进建议

基于以上 6 个维度的分析结果，给出 3-5 条可操作的改进建议。每条建议需要：
- 引用具体的分析数据作为证据
- 提出明确的行动项
- 说明预期效果

## Phase 3: 输出报告

按以下 HTML 格式输出最终报告。使用内联 CSS 确保在浏览器和飞书中均可良好显示：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Git 工作复盘 — {repo} {date}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; max-width: 860px; margin: 0 auto; padding: 20px; color: #1a1a1a; background: #f8f9fa; }
  .report { background: #fff; border-radius: 12px; padding: 32px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }
  h1 { font-size: 24px; border-bottom: 3px solid #0d7377; padding-bottom: 12px; margin-bottom: 4px; }
  h2 { font-size: 17px; color: #0d7377; margin-top: 28px; border-left: 4px solid #0d7377; padding-left: 10px; }
  h3 { font-size: 14px; color: #444; margin-top: 14px; }
  .meta { color: #666; font-size: 13px; margin-bottom: 16px; }
  .summary { background: #e0f7f7; border-radius: 8px; padding: 16px; font-size: 15px; margin: 16px 0; }
  .summary ol { margin: 8px 0 0 0; padding-left: 20px; }
  .summary li { margin: 4px 0; }
  table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 14px; }
  th { background: #f1f3f4; text-align: left; padding: 10px 12px; font-weight: 600; border-bottom: 2px solid #ddd; }
  td { padding: 8px 12px; border-bottom: 1px solid #eee; vertical-align: top; }
  tr:hover td { background: #f8f9fa; }
  .mono { font-family: "SFMono-Regular", Consolas, monospace; font-size: 12px; color: #555; }
  .tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; }
  .tag-pass { background: #e8f5e9; color: #2e7d32; }
  .tag-warn { background: #fff3e0; color: #e65100; }
  .tag-info { background: #f5f5f5; color: #616161; }
  .timeline { font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; background: #f8f9fa; padding: 12px 16px; border-radius: 6px; overflow-x: auto; white-space: pre; }
  .stars { color: #f5a623; letter-spacing: 2px; }
  .suggestion { background: #f3f8ff; border-left: 3px solid #0d7377; padding: 10px 14px; margin: 8px 0; border-radius: 0 6px 6px 0; }
  .suggestion strong { display: block; margin-bottom: 4px; }
  .checklist { list-style: none; padding: 0; }
  .checklist li { padding: 6px 0; border-bottom: 1px solid #f0f0f0; font-size: 14px; }
  ul, ol { padding-left: 20px; }
  li { margin: 5px 0; line-height: 1.6; }
  code { background: #f1f3f4; padding: 1px 5px; border-radius: 3px; font-size: 12px; font-family: "SFMono-Regular", Consolas, monospace; }
  .daily-notes { background: #fafafa; border: 1px solid #e8e8e8; border-radius: 8px; padding: 14px 18px; font-size: 13px; white-space: pre-wrap; font-family: inherit; line-height: 1.7; }
  .daily-notes .done { color: #2e7d32; }
  .daily-notes .pending { color: #888; }
  .match-table td:first-child { width: 60px; text-align: center; }
</style>
</head>
<body>
<div class="report">

<h1>Git 工作复盘</h1>
<div class="meta">{时间范围} | 仓库: <strong>{repo}</strong> | {提交数} commits | {文件变更数} files changed | <span style="color:#2e7d32">+{新增行}</span> <span style="color:#c62828">-{删除行}</span></div>

<!-- 仅当存在当日记录时输出此 section，否则完全省略 -->
<h2>0. 当日记录</h2>
<div class="daily-notes">{当日个人记录原文，保留原始缩进和 checkbox}</div>
<h3>计划 vs 实际对比</h3>
<table class="match-table">
  <tr><th>状态</th><th>记录条目</th><th>对应 Commit</th></tr>
  <tr><td><span class="tag tag-pass">✓ 已提交</span></td><td>...</td><td class="mono">abc1234</td></tr>
  <tr><td><span class="tag tag-warn">○ 未提交</span></td><td>...</td><td>—</td></tr>
  <tr><td><span class="tag tag-info">+ 额外</span></td><td>记录未提及的 commit</td><td class="mono">def5678</td></tr>
</table>

<div class="summary">
<strong>核心发现</strong>
<ol>
  <li>...</li>
  <li>...</li>
  <li>...</li>
</ol>
</div>

<h2>1. 工作总结</h2>
<p>{叙述式总结：按逻辑主题分组说明做了什么、为什么做}</p>

<h3>提交时间线</h3>
<table>
  <tr><th>时间</th><th>Hash</th><th>提交信息</th></tr>
  <tr><td>HH:MM</td><td class="mono">abc1234</td><td>...</td></tr>
</table>

<h2>2. 变更类型分布</h2>
<table>
  <tr><th>类型</th><th>文件数</th><th>占比</th><th>增删行数</th></tr>
  <tr><td>代码</td><td>...</td><td>...%</td><td>+... -...</td></tr>
  <tr><td>测试</td><td>...</td><td>...%</td><td>+... -...</td></tr>
  <tr><td>文档</td><td>...</td><td>...%</td><td>+... -...</td></tr>
  <tr><td>配置</td><td>...</td><td>...%</td><td>+... -...</td></tr>
  <tr><td>其他</td><td>...</td><td>...%</td><td>+... -...</td></tr>
</table>
<p>{分析说明}</p>

<h2>3. 工作节奏</h2>
<table>
  <tr><th>指标</th><th>数值</th></tr>
  <tr><td>首次提交</td><td>...</td></tr>
  <tr><td>末次提交</td><td>...</td></tr>
  <tr><td>总跨度</td><td>...</td></tr>
  <tr><td>Flow Sessions</td><td>... 个</td></tr>
  <tr><td>最长 Session</td><td>...</td></tr>
  <tr><td>最长间隔</td><td>...</td></tr>
</table>
<div class="timeline">{时间线可视化，用 ASCII 字符表示，如每格代表一小时}</div>

<h2>4. 提交实践评估</h2>
<table>
  <tr><th>评估项</th><th>评分</th><th>说明</th></tr>
  <tr><td>Message 质量</td><td><span class="stars">★★★★☆</span></td><td>...</td></tr>
  <tr><td>提交粒度</td><td><span class="stars">★★★☆☆</span></td><td>...</td></tr>
  <tr><td>Conventional Commits</td><td><span class="stars">★★★★★</span></td><td>...</td></tr>
</table>
<p><strong>好的示例:</strong> <code>feat(auth): add JWT refresh token rotation</code></p>
<p><strong>可改进:</strong> <code>fix</code> → 改为 <code>fix(module): describe what was fixed</code></p>

<h2>5. 技术决策</h2>
<ul>
  <li><strong>新依赖引入</strong>: ... (<code>abc1234</code>)</li>
  <li><strong>架构变更</strong>: ... (<code>def5678</code>)</li>
</ul>

<h2>6. 完成度检查</h2>
<ul class="checklist">
  <li><span class="tag tag-pass">Pass</span> &nbsp;未提交改动: 工作区干净</li>
  <li><span class="tag tag-warn">Warning</span> &nbsp;Stash 暂存: ...</li>
  <li><span class="tag tag-info">Info</span> &nbsp;TODO/FIXME: ...</li>
  <li><span class="tag tag-pass">Pass</span> &nbsp;测试配套: ...</li>
</ul>

<h2>7. 改进建议</h2>
<div class="suggestion"><strong>1. {建议标题}</strong>{具体内容}（证据：{引用分析数据}）</div>
<div class="suggestion"><strong>2. {建议标题}</strong>...</div>
<div class="suggestion"><strong>3. {建议标题}</strong>...</div>

</div>
</body>
</html>
```

**HTML 填写规则：**
- 将模板中的占位符替换为实际数据，删除注释
- 星级评分用 `★` (实心) 和 `☆` (空心) 表示，5分=`★★★★★`
- 完成度标签：Pass=`tag-pass`（绿），Warning=`tag-warn`（橙），Info=`tag-info`（灰）
- 时间线可视化用等宽字符绘制，每格代表一小时，有提交的格用 `█`，无提交用 `·`
- 确保 HTML 完整，可直接在浏览器中打开

将报告保存为 `git-review-{date}.html` 到当前工作目录的 `output/` 子目录（如无则使用当前目录），其中 `{date}` 为当天日期（如 `2026-02-23`）。

保存 HTML 后，使用 Chrome headless 转换为 PDF：

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf="$(pwd)/output/git-review-{date}.pdf" \
  --no-pdf-header-footer \
  "file://$(pwd)/output/git-review-{date}.html"
```

> 如果 Chrome 不可用，使用备选方案：`npx -y md-to-pdf "$(pwd)/output/git-review-{date}.html"`

最终输出两份文件：
- `output/git-review-{date}.html` — HTML 版本
- `output/git-review-{date}.pdf` — PDF 版本（用于飞书发送）

## Edge Cases

- **无当日记录**：`notes/daily_notes/` 不存在或指定日期无匹配标题，跳过维度 0 和报告 section 0，其余维度不受影响
- **多日范围含多天记录**：依次提取各天记录块，在报告中合并展示，按日期倒序
- **无提交**：Phase 1 第 1 步检测到空结果后，**立即终止流程**——展示最近 5 条提交时间供参考，提示用户重新指定范围。禁止自行扩大时间范围或继续后续 Phase
- **单条提交**：正常生成报告，但跳过维度 3（工作节奏）的 session 分析，简化为仅记录提交时间
- **非 git 仓库**：Phase 1 前置检查失败，提示用户当前目录不是 git 仓库
- **二进制文件**：仅在文件列表中标注为二进制，跳过行数统计，不尝试 diff 分析
- **超大时间范围（>100 commits）**：正常分析，但在维度 1 中按主题分组时做更高层次的归纳，避免报告过长
