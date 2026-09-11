---
name: 4drawio
description: "数学建模非数据型图示绘制阶段。根据 ANALYSIS_MODELING_REPORT.md、RESULTS_REPORT.md 和已有 figures/ 生成技术路线图、子问题求解流程图、模型结构图、数据处理流程图等 DrawIO 图，并导出论文可引用 PDF。"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, WebSearch, WebFetch
---

# DrawIO 非数据图示绘制

本 skill 承接 `3coding-visual`。它只负责论文中的**非数据型图示**，例如论文整体示意图、技术路线图、求解流程图、模型结构图、数据处理流程图、变量关系图、指标体系图等。整体布局参考 `sci-box/scibox-diagram` 的五带路线、三栏研究框架和横版任务流水线思路，但节点与结论必须来自当前题目。

版式选择和连线约束详见 `references/scibox-integration.md`。插件已内置
`resources/scibox-diagram/`：其中包含来自 `jihe520/sci-box` 的四套可复现模板、Draw.io
XML 生成脚本、预览/导出脚本、静态布局检查器及模板说明。优先复用这些资源，再按当前题目
替换内容；不要把示例中的研究结论或模拟数据当作本题证据。

## 数学建模规范参考

如需领域判断，读取 `../mathmodel-references/math_modeling_norms.md` 中的“图表与可视化”和“非数据图工具选择”小节。该文件只作为规范知识库，不要求为了凑数量生成额外图示。

## 阶段边界

- 本阶段负责：DrawIO 源文件、非数据图 PDF、图示生成记录。
- 本阶段不负责：折线图、柱状图、散点图、热力图、箱线图、雷达图等数据图。这些由 `3coding-visual` 生成。
- 本阶段不重跑模型、不修改 `code/`，不改写 `reports/RESULTS_REPORT.md` 的数值结论。

## 必须产出

在当前工作目录创建或更新：

```text
figures/
  fig_roadmap.drawio
  fig_roadmap.pdf
  fig_flow_q1.drawio
  fig_flow_q1.pdf
  ...
reports/DRAWIO_REPORT.md
```

如果某类图不需要生成，必须在 `reports/DRAWIO_REPORT.md` 中说明原因。竞赛论文通常至少需要一张 `fig_roadmap` 技术路线图。

全国赛论文必须生成一张论文整体示意图（可与 `fig_roadmap` 合并，但用途和 caption 要明确），将题目、数据、各问题、模型/算法、验证和最终决策串成可追溯的信息流。

读取这些文件的目的不是提取数据作图，而是理解论文方法、章节结构、子问题关系和已有图表，避免重复。

## 工作流程

### Step 1: 盘点已有图表和需求

先读取以下文件（存在则读取）：`reports/ANALYSIS_MODELING_REPORT.md`、`reports/RESULTS_REPORT.md`、`figures/` 目录列表。

然后从前序文档提取非数据图需求，输出一个清单：

```text
DRAWIO PLAN CHECKLIST:
[ ] fig_roadmap      技术路线图，放在问题重述/绪论
[ ] fig_paper_overview 论文整体示意图，放在问题重述/总体方法
[ ] fig_flow_q1      问题一求解流程图
[ ] fig_flow_q2      问题二求解流程图
[ ] fig_flow_q3      问题三求解流程图
[ ] fig_pipeline     数据处理流程图
[ ] fig_model        模型结构/变量关系图
```

清单不是固定模板，要根据题目实际删减或增补。不要为了凑图生成无意义图示。

### Step 2: 判定图类型

常见图示选择：

| 图类型 | 文件名建议 | 适用场景 |
| --- | --- | --- |
| 技术路线图 | `fig_roadmap` | 展示整体解题路线、章节逻辑、方法串联 |
| 子问题求解流程图 | `fig_flow_q1`, `fig_flow_q2` | 展示单个子问题的输入、判断、算法、输出 |
| 数据处理流程图 | `fig_pipeline` | 展示数据清洗、特征构造、建模输入 |
| 模型结构图 | `fig_model` | 展示模块关系、变量关系、模型层次 |
| 指标体系图 | `fig_index_system` | 展示目标层、准则层、指标层 |
| 决策树/规则图 | `fig_decision_tree` | 展示分类规则、设备选择、策略分支 |
| 论文整体示意图 | `fig_paper_overview` | 展示题目—数据—逐题模型—验证—决策的全局信息流 |

重要算法的图示选择：

| 论证负荷 | 选择 | 判据 |
| --- | --- | --- |
| 步骤、分支、迭代或停止条件复杂 | 算法流程框图 | 读者需要沿输入—处理—判断—输出复现求解过程 |
| 变量耦合、反馈、因果或模块作用复杂 | 算法概念/机制图 | 读者需要理解“为什么有效”及变量如何传递 |
| 过程和机理都承担不可替代的解释任务 | 两者都要 | 两图信息非重复，并在正文分别引用 |
| 以上均不成立 | 只保留文字/公式 | 不为了凑图制造低信息密度图示 |

不要用 DrawIO 画这些图：

- 结果对比柱状图
- 预测误差曲线
- 灵敏度曲线
- 相关性热力图
- 分布图和箱线图

### Complex Draw.io MCP routing (run before Step 3)

Keep this skill as the owner of the non-data-diagram stage and `reports/DRAWIO_REPORT.md`. Route
the actual creation or edit to `using-drawio-mcp` and set `drawio_mcp_required: true` when the
figure has more than eight nodes, at least two decisions or a feedback loop, at least two lanes or
nested groups, a multi-layer architecture, specialized editable geometry, any existing `.drawio`
edit, or an explicit Draw.io MCP requirement.

Match all visible labels to the paper language. Chinese figures use Chinese labels and `是`/`否`;
English figures use English labels and `Yes`/`No`. For existing files, require the page-safe
`list_pages -> get_page -> set_page` workflow owned by `using-drawio-mcp`.

If `drawio` is absent from `codex mcp list`, restore the official stdio service before drawing:

```powershell
codex mcp add drawio -- "<npx-path>" --yes @drawio/mcp
codex mcp get drawio
```

Do not silently replace a required editable diagram with a bitmap. If installation or startup
fails, record the fallback state and keep the figure non-promotable until MCP is restored or a
human accepts the documented fallback.

When MCP is unavailable or still fails visual QA after three attempts, record:

- legal `.drawio` and XML fallbacks marked `UNVERIFIED_MCP_FALLBACK`;
- a rendered Mermaid or TikZ placeholder plus its source;
- `paper/issues/drawio-mcp/<figure_id>/issue.md` and an `OPEN` or `BLOCKING` entry in
  `paper/issues/issue_register.md`;
- the same state, paths, attempts, and recovery action in `reports/DRAWIO_REPORT.md`.

`PLACEHOLDER`, `AWAITING_SAVE`, and `UNVERIFIED_MCP_FALLBACK` are drafting states only. Never
report them as final, and never allow them through G5 or G6.

### Step 3: 生成 DrawIO 源文件

### sci-box 模板资源路径

按版式选择后，从以下插件内路径读取对应说明、示例 JSON 和脚本：

```text
skills/4drawio/resources/scibox-diagram/
  assets/<template-id>/example.json
  references/<template-id>.md
  scripts/<template-id>.py
```

四个模板脚本分别为 `roadmap_5band.py`、`framework_3col.py`、`stageflow_3col.py` 和
`taskflow_land.py`。先复制并修改 `example.json`，再运行脚本生成 `.drawio`；生成后运行
`scripts/check_layout.py`，需要浏览器预览时运行 `scripts/preview_html.py`。若需导出 PNG/PDF，
运行 `scripts/export_figure.py` 并保留可编辑 `.drawio` 源文件。资源中的 Tabler 图标受 MIT
许可保护，使用时保留 `resources/scibox-diagram/ATTRIBUTION.md` 及其许可证文件。

每张图一个 `.drawio` 文件，放在 `figures/`。

DrawIO 内容要求：

- 文字语言与论文语言一致。
- 节点文字短，必要时双行，不堆长句。
- 同类节点样式统一。
- 箭头方向清晰，避免交叉。
- 先排版后连线：固定列基线和层级，优先正交折线、共享母线和分区泳道；禁止无语义的斜穿线、回头线和节点重叠。
- 整体示意图优先使用五带路线图、三栏研究框架或横版任务流水线；不为“好看”增加无论证节点。
- 重要算法按解释负荷自主选择算法流程框图、算法概念/机制图或两者组合：流程图表达步骤与判断，概念图表达变量、模块、反馈和作用机理；只有两类信息都不可替代时才同时生成，不能用同一张只改标题的图冒充两类图。
- 图中不写大段解释，解释留给论文正文。
- 不使用装饰性阴影和过度渐变。

生成大 XML 时，分段写入，避免截断。示例：

```bash
mkdir -p figures
cat << 'XMLEOF' > figures/fig_roadmap.drawio
<mxfile>
  <diagram name="Page-1">
    <mxGraphModel>
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- nodes and edges -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
XMLEOF
```

### Step 4: 导出 PDF

优先用可用的 DrawIO 命令导出 PDF：

```bash
DRAWIO_BIN="$(command -v drawio 2>/dev/null || command -v draw.io 2>/dev/null || command -v draw.io.exe 2>/dev/null || true)"
if [ -n "$DRAWIO_BIN" ]; then
  "$DRAWIO_BIN" --export --format pdf --crop --output figures/fig_roadmap.pdf figures/fig_roadmap.drawio
else
  echo "DrawIO command not found; keep .drawio source and record export failure."
fi
```

如果无法导出 PDF，保留 `.drawio`，在 `reports/DRAWIO_REPORT.md` 记录失败原因和建议导出命令。

### Step 5: 自检和修复

每张图必须检查：

- `.drawio` 文件非空。
- 若导出成功，`.pdf` 文件非空。
- 节点没有明显重叠。
- 箭头不穿过核心节点。
- 多分支、多汇流和反馈均有明确入口/出口，连线不交叉、不重叠；必要时改用母线、泳道或分层页面。
- 论文整体示意图覆盖题目、数据、每个子问题、模型/算法、验证和决策；重要算法至少有一种与其解释负荷匹配的算法图示，必要时再补充另一种。
- 字号、颜色、边框风格一致。
- 文件名和图意一致。
- 没有与 `3coding-visual` 的数据图重复。

发现问题要修 `.drawio` 并重新导出，不要只在报告里解释。

### Step 6: 写生成记录

创建 `reports/DRAWIO_REPORT.md`，至少包含：

```markdown
# DrawIO 图示生成报告

## 图示清单
| 文件 | 类型 | 来源依据 | 用途 | 状态 |
| --- | --- | --- | --- | --- |

## 未生成图示及原因

## 导出与自检记录

## 给论文阶段的嵌入建议
```

嵌入建议只说明每张图适合放入哪个章节和建议 caption，不生成 `*_typst_includes.typ`。最终的图表插入代码（Typst 的 `#figure(image(...), caption: [...])` 或 LaTeX 的 `\begin{figure}...\end{figure}`）由 `5writing` 根据论文结构和所选引擎决定。

## 质量要求

- 图示服务论文论证，不为装饰而画。
- 每张图必须能对应到`reports/ANALYSIS_MODELING_REPORT.md` 中的真实方法。
- 数据型图表不得在本阶段重复生成。
- 论文阶段引用的非数据图都应有 `.drawio` 源文件和 PDF，或者在 `reports/DRAWIO_REPORT.md` 说明导出失败。
- 导出前检查目标版面下最小字号不低于中文六号（约 7.5 pt）；矢量优先，位图分辨率须足以保证缩印清晰，不把 300 dpi 当作唯一合格线。
