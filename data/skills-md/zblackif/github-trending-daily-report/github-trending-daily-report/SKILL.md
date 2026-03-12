---
name: github-trending-daily-report
description: Generate deep analysis reports for GitHub Trending repositories, providing insights on trending popularity, technical implementations, frameworks, and potential application directions. Use when user needs automated daily GitHub Trending analysis, reports on trending repositories with technical deep dives, insights into emerging technology trends, or daily scheduled reports for monitoring GitHub ecosystem changes.
---

# GitHub Trending Daily Report — 深度分析报告生成指南

生成高质量的 GitHub Trending 深度分析报告，包括每个项目的技术架构分析、核心特性、潜在应用方向，以及整体技术趋势总结和投资建议。

**质量目标**: 最终报告应达到 1000-1500 行，每个项目 80-100 行深度分析。参考 `github-trending-report-2026-02-08.md` 作为输出质量标准。

---

## 工作流程概览

本报告生成分为5个步骤：

| 步骤 | 执行者 | 描述 |
|------|--------|------|
| Step 1 | Python 脚本 | 抓取 GitHub Trending 数据并富化（README、元数据、依赖信息） |
| Step 2 | Python 脚本 | 生成动态骨架报告（含占位标记） |
| Step 3 | **Claude** | **核心步骤**：为每个项目填写深度技术分析 |
| Step 4 | **Claude** | 生成动态趋势总结、投资建议、风险分析 |
| Step 5 | **Claude** | 质量检查与最终输出 |

---

## Step 1: 抓取并富化 Trending 数据

运行数据抓取脚本：

```bash
cd /Users/bytedance/github-trending-report
python3 fetch_trending.py
```

如果有 GitHub Token（推荐，提高 API 限额）：

```bash
python3 fetch_trending.py --github-token "$GITHUB_TOKEN"
```

**验证**: 检查生成的 `trending-data-YYYY-MM-DD.json` 文件：
- 确认包含 10-20 个仓库数据
- 确认大部分仓库有 `readme_content` 字段（富化成功）
- 确认有 `metadata` 字段（包含 topics、license、forks 等）

**如果富化失败**: 某些仓库可能没有 `readme_content`，在 Step 3 中需要通过 WebFetch 手动补充。

**输出**: `trending-data-YYYY-MM-DD.json`

---

## Step 2: 生成骨架报告

```bash
python3 generate_report.py
```

**验证**: 检查生成的 `github-trending-report-YYYY-MM-DD.md`：
- 包含动态生成的概览表（所有仓库，含许可证列）
- 包含基于 topics 自动分类的技术领域分布
- 每个项目有 `<!-- DEEP_ANALYSIS: ... -->` 占位标记
- 趋势总结部分有占位标记

**输出**: `github-trending-report-YYYY-MM-DD.md`（骨架版本）

---

## Step 3: 深度技术分析（核心步骤）

这是最关键的步骤。需要读取骨架报告和 JSON 数据，为每个项目生成深度分析内容。

### 3.1 数据准备

1. 读取 `trending-data-YYYY-MM-DD.json` 获取每个项目的完整数据
2. 读取 `github-trending-report-YYYY-MM-DD.md` 获取骨架报告
3. 对于 JSON 中缺少 `readme_content` 的项目，使用 WebFetch 访问：
   - `https://github.com/{owner}/{repo}` — 仓库主页
   - `https://raw.githubusercontent.com/{owner}/{repo}/main/README.md` — README 原文
   - 项目 homepage（如果 metadata 中有）

### 3.2 执行摘要补充

替换 `<!-- DEEP_ANALYSIS: executive_summary_intro -->` 占位符，补充1-2句概括性描述：

**格式要求**：
```
这些项目涵盖了{领域1}、{领域2}、{领域3}等多个技术领域，反映了当前{特征描述}的技术发展热点趋势。
```

### 3.3 技术领域分布分析

替换每个领域的 `<!-- DEEP_ANALYSIS: domain_analysis -->` 占位符。

**格式模板**：
```markdown
该领域项目总星标数超过{total_stars}，{一句话总结该领域特征}：
- **{子分类1}：** {具体描述，引用项目名}
- **{子分类2}：** {具体描述，引用项目名}
- **{子分类3}：** {具体描述，引用项目名}
```

### 3.4 单个项目深度分析

这是报告的核心。对每个项目，替换三个占位符区域。

#### 3.4.1 技术原理与实现

替换 `<!-- DEEP_ANALYSIS: technical_principles -->`

**输出格式**：
```markdown
{项目名}是{一句话定位描述，说明它是什么、解决什么问题}。

**核心技术架构：**

1. **{架构组件/技术要点1}**
   - {从 README 中提取的具体技术细节}
   - {使用的框架、库或设计模式}
   - {实现方式或工作原理}

2. **{架构组件/技术要点2}**
   - {具体细节}
   - {具体细节}
   - {具体细节}

3. **{架构组件/技术要点3}**
   - ...

4. **{架构组件/技术要点4}**
   - ...

5. **{架构组件/技术要点5}**（如有足够信息）
   - ...
```

**质量要求**：
- 4-5 个编号要点，每个要点有粗体标题
- 每个要点下 2-3 个具体子项（用 `-` 列表）
- 技术细节必须来自 README 实际内容，如具体的 SDK 名称、API 设计、架构模式
- 如果 README 提到了具体的技术栈（如 "基于 Anthropic Claude Agent SDK"），必须引用
- 如果有工作流程（如 "四阶段工作流"），需要详细描述每个阶段

#### 3.4.2 核心特性

替换 `<!-- DEEP_ANALYSIS: core_features -->`

**输出格式**：
```markdown
**1. {特性名称}**
   - {特性的具体描述}
   - {实现方式或用户价值}
   - {相关的技术指标或性能数据}

**2. {特性名称}**
   - ...

**3. {特性名称}**
   - ...

**4. {特性名称}**
   - ...

**5. {特性名称}**
   - ...

**6. {特性名称}**（如有足够信息）
   - ...
```

**质量要求**：
- 5-6 个编号特性，每个有粗体标题
- 特性名称必须来自项目 README 中实际描述的功能
- 每个特性下 2-3 个子项
- 如有性能数据或 benchmark（如 "2x faster"、"70% less VRAM"），必须引用
- 不可使用通用的泛泛描述如"高性能"、"易用性"，必须具体化

#### 3.4.3 潜在应用方向

替换 `<!-- DEEP_ANALYSIS: potential_applications -->`

**输出格式**：
```markdown
**1. {应用领域}**
   - {具体应用场景1}：{详细描述}
   - {具体应用场景2}：{详细描述}
   - {商业机会或市场前景}

**2. {应用领域}**
   - ...

**3. {应用领域}**
   - ...

**4. {应用领域}**
   - ...

**5. {应用领域}**
   - ...
```

**质量要求**：
- 5 个编号应用方向，每个有粗体标题
- 每个方向下 3 个具体子项
- 应用场景必须与项目实际能力匹配（如 AI 安全工具不应推荐用于金融分析）
- 包含行业应用、技术集成场景、商业化方向
- 子项格式："场景名：详细描述"

---

## Step 4: 趋势总结与洞察

在所有单个项目分析完成后，生成报告末尾的趋势总结部分。

### 4.1 技术趋势

替换 `<!-- DEEP_ANALYSIS: technology_trends -->`

**输出格式**：
```markdown
1. **{趋势标题}**
   - {解释性描述，引用具体项目名如 "以{项目A}和{项目B}为代表"}
   - {趋势的深层原因或影响}

2. **{趋势标题}**
   - ...

3. **{趋势标题}**
   - ...

4. **{趋势标题}**
   - ...

5. **{趋势标题}**
   - ...
```

**质量要求**：
- 5 个编号趋势
- 每个趋势必须引用至少 2 个当天实际项目名称作为佐证
- 趋势必须从当天实际项目中归纳总结，不可使用预设固定内容
- 每个趋势 2 个解释性子项

### 4.2 投资建议

替换 `<!-- DEEP_ANALYSIS: high_priority_investment -->` 和 `<!-- DEEP_ANALYSIS: medium_priority_investment -->`

**输出格式**（高优先级示例）：
```markdown
**1. {方向名称}**
- **投资逻辑**：{为什么这个方向值得关注，数据支撑}
- **重点关注**：{具体项目名称}（{今日星标数} stars today）
- **投资建议**：{具体的行动建议}

**2. {方向名称}**
- ...
```

**质量要求**：
- 高优先级 2-3 个方向，中优先级 2-3 个方向
- 每个方向引用具体项目和数据
- 投资逻辑必须有数据支撑（stars 增长、社区活跃度等）

### 4.3 风险分析

替换 `<!-- DEEP_ANALYSIS: risk_analysis -->`

**输出格式**：
```markdown
#### 技术风险
- {具体风险点1，引用相关项目}
- {具体风险点2}

#### 市场风险
- {具体风险点1}
- {具体风险点2}

#### 安全合规风险
- {具体风险点1，如许可证问题}
- {具体风险点2}

#### 社区维护风险
- {具体风险点1，如维护者数量、活跃度}
- {具体风险点2}
```

**质量要求**：
- 4 个维度，每个维度 2-3 个具体要点
- 风险点必须针对当天实际项目，不可泛泛而谈
- 引用具体数据（如 forks 数、issue 数、许可证类型）

---

## Step 5: 质量检查

最终输出前，执行以下检查：

### 检查清单

- [ ] **无占位标记残留**：报告中不应有 `<!-- DEEP_ANALYSIS:` 标记
- [ ] **无方括号指令残留**：报告中不应有 `[请基于...` 等指令文本
- [ ] **所有项目完整**：每个项目都有"技术原理与实现"、"核心特性"、"潜在应用方向"三个完整部分
- [ ] **趋势引用真实项目**：趋势总结中引用的项目名称都是当天数据中实际存在的
- [ ] **中文一致性**：全文使用中文，技术术语可保留英文原文
- [ ] **格式正确**：Markdown 格式正确，表格对齐，列表缩进一致
- [ ] **报告行数**：目标 1000-1500 行（12 个项目的情况下）
- [ ] **README 摘要折叠**：每个项目的 `<details>` 标签中包含 README 摘要供参考

### 保存最终报告

将最终完成的报告内容覆盖保存到 `github-trending-report-YYYY-MM-DD.md`。

---

## 快速执行命令

完整的自动化流程（Step 1 + Step 2）：

```bash
cd /Users/bytedance/github-trending-report
./run_report.sh
```

之后手动执行 Step 3-5（Claude 深度分析）完成报告。

---

## Scheduling for Daily Execution

Use cron to schedule daily 9 AM execution:

```bash
# Edit crontab
crontab -e

# Add daily 9 AM cron job
0 9 * * * cd /Users/bytedance/github-trending-report && ./run_report.sh >> logs/report.log 2>&1
```

The `run_report.sh` script executes Steps 1 and 2. Use the skill afterwards for Steps 3-5.

---

## Resources

### scripts/

- `fetch_trending.py`: Fetches GitHub trending HTML + enriches with GitHub API metadata, README, and manifest
- `generate_report.py`: Generates dynamic skeleton report with placeholder markers for Claude
- `run_report.sh`: Shell script to execute the data pipeline (Steps 1+2)

### 输出文件

- `trending-data-YYYY-MM-DD.json`: 富化的趋势数据（含 README、metadata、manifest）
- `github-trending-report-YYYY-MM-DD.md`: 最终深度分析报告
