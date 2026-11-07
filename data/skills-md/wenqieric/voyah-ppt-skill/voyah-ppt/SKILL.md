---
name: voyah-ppt
description: 基于岚图汽车（VOYAH）2025 官方 PPT 模板生成内部汇报材料。任何时候用户要做「岚图内部汇报」「项目汇报」「月度复盘」「周报 PPT」「述职报告」「培训材料」「岚图 PPT」「公司模板 PPT」「VOYAH PPT」，或者明示/暗示需要符合岚图品牌视觉规范的演示文稿时，立即使用此 skill。它会克隆官方模板的封面、目录、章节页、正文页、封底版式，保留母版字体（华康金刚黑、等线）、企业 Logo、密级标记和品牌色，输出可在 PowerPoint 中二次编辑且能切换版式的 .pptx 文件。
---

# voyah-ppt

## Overview

把用户的汇报需求（主题、要点、目录、数据）转成一份**完全符合岚图汽车 2025 官方 PPT 模板**的演示文稿。技术上委托给底层 `python-pptx`，通过克隆 `assets/voyah-master.pptx` 中现成的 5 个 slideLayout 来生成每一页，保证字体、Logo、配色、密级标记和母版结构 100% 与公司规范一致。

## 为什么这样做（设计原理）

直接复用模板里现成的 `slideLayout` 作为每页底板，而不是凭空画一张图再转 pptx——原因有三：

1. **品牌一致性**：母版里嵌入了「华康金刚黑」「等线 Light」字体声明、企业 Logo（image1.png 等）、密级标记、深浅两套色板。HTML 渲染再转 pptx 的方案会丢掉这些。
2. **可编辑性**：输出文件在 PowerPoint 里能切换版式、编辑文字，团队成员能直接接手二次修改。
3. **轻量**：纯 XML 操作，没有 Puppeteer/Chromium 依赖，几百 KB 内存即可。

## 工作流程

### 第 0 步：确认环境

需要 Python 3.9+ 和 `python-pptx`。检查并按需安装：

```bash
python3 -c "import pptx; print(pptx.__version__)" 2>/dev/null || pip3 install --user python-pptx
```

如果上一步报错且系统 pip 受 PEP 668 限制，改用：

```bash
python3 -m venv /tmp/voyah-ppt-venv && /tmp/voyah-ppt-venv/bin/pip install python-pptx
# 后续 build_pptx.py 用 /tmp/voyah-ppt-venv/bin/python 执行
```

### 第 1 步：理解需求 → 生成 content.md

读 `references/content-rules.md`，把用户的需求整理成结构化的 `output/content.md`：

- 抽取：主题、汇报人/部门、章节划分、每章要点
- 决定页数策略：**≤ 5 页正文时跳过目录和章节页**（避免冗余），> 5 页时正常包含目录和章节分隔页
- 整理为「封面 → (目录) → (章节1 → 正文…) → (章节2 → 正文…) → … → 封底」的纲要

### 第 2 步：生成 slides.json

读 `references/template-matching.md` 和 `references/content-variants.md`，把 content.md 翻译成 `output/slides.json`。

每条记录的格式：

```json
{
  "kind": "cover | contents | section | content | thanks",
  "variant": "（仅 content 类型需要：bullet-list / paragraph / text-image / two-columns / cards / big-number / code-block）",
  "slots": { ... }
}
```

完整示例见 `references/slides-example.json`，复制后改字段即可。

### 第 3 步：构建 PPTX

```bash
mkdir -p output
python3 SKILL_DIR/scripts/build_pptx.py \
  --master SKILL_DIR/assets/voyah-master.pptx \
  --slides output/slides.json \
  --out output/presentation.pptx
```

把 `SKILL_DIR` 替换为本 skill 的真实绝对路径。

### 第 4 步：自检（必须执行）

**每次生成后都必须跑自检**，检查布局异常：

```bash
python3 SKILL_DIR/scripts/inspect_pptx.py \
  --pptx output/presentation.pptx \
  --report output/inspect-report.md
```

自检脚本会检查：
- shape 是否越界
- shape 之间是否重叠
- 文本框是否溢出
- 标题字数是否超标
- 目录页空 shape 是否清理干净
- 密级标记是否正确

**如果报告里有警告**，回到第 2 步修改 slides.json（通常是标题太长、要点太多），然后重新构建。

### 第 5 步：交付并告知用户

```bash
cat output/inspect-report.md
ls -lh output/presentation.pptx
```

告诉用户：文件位置、总页数、结构概要（"封面 + N 个章节 + 封底"）。如果自检报告有问题，一并告知需要修改的地方。

## 5 种页面类型（kind）

逐条说明触发场景和必填槽位。详细的模板适配规则在 `references/template-matching.md`，**遇到要决定某页用什么版式时务必读它**。

| kind | 何时使用 | 必填 slots |
|---|---|---|
| `cover` | 每份 PPT 的第 1 页，自带岚图 Logo 和密级标记 | title, subtitle |
| `contents` | 章节数 2–5 时的整体目录（**最多 5 章**，模板限制） | chapters[] |
| `section` | 每个章节开始的过渡分隔页，左下角带 01/02/03 编号 | chapterNumber, title |
| `content` | 正文页，必须配一个 `variant` 指明排版方式 | title + variant 各自的字段 |
| `thanks` | 最后一页，自带「感谢聆听 / Thanks」+ 公司信息 | （无，保留模板默认即可） |

## 10 种正文 variant

| variant | 适用 |
|---|---|
| `bullet-list` | 要点罗列。最常用，几乎所有正文页的默认选项 |
| `paragraph` | 背景介绍、问题陈述、需要完整说明的段落 |
| `text-image` | 左文右图，展示截图、产品图、流程图 |
| `two-columns` | 同质双栏并列（特性、组成） |
| `cards` | 3–4 个并列要点（优势点、功能特性、流程阶段） |
| `big-number` | 突出单个核心数据（一个大数字 + 解释） |
| `data-highlight` | 并列 3 个 KPI/指标（深青底面板） |
| `timeline` | 流程/步骤/阶段/时间线（横向 3 步） |
| `comparison` | A vs B 强对比（主色 vs 中性） |
| `code-block` | 代码片段或表格（技术类汇报常用） |

详细字段定义见 `references/content-variants.md`。

## 文件结构

```
voyah-ppt/
├── SKILL.md                       # 本文件
├── assets/
│   └── voyah-master.pptx          # 官方 PPT 模板（作为基底）
├── references/
│   ├── content-rules.md           # 内容生成规则
│   ├── template-matching.md       # 5 种 kind 的判定规则
│   ├── content-variants.md        # 10 种正文 variant 的字段
│   └── slides-example.json        # 完整 slides.json 示例
├── scripts/
│   ├── build_pptx.py              # 核心：克隆 layout + 注入内容
│   └── inspect_pptx.py            # 自检：检查布局异常
└── evals/
    └── evals.json                 # 测试用例
```

## 断点续作

- 如果 `output/content.md` 已存在且用户没说"重新写大纲"，跳到第 2 步
- 如果 `output/slides.json` 已存在且用户只是想"重新生成 PPT"，跳到第 3 步
- `build_pptx.py` 是幂等的，重复运行覆盖输出文件

## 模板的硬约束（必须遵守）

这些约束写死在公司模板里，违反就会变形或溢出：

1. **封面主标题 ≤ 14 字**（单行 36pt）——标题独占封面主标题位，副标题不再同行。**v3 起不缩字号**，超长会被硬性截断并告警，应从源头精简。
2. **正文标题 ≤ 18 字**——正文标题位高度有限。**不缩字号**，超长截断+告警。
3. **章节标题 ≤ 16 字**——章节分隔页 40pt 大字，过长拥挤。
4. **目录页最多 5 个章节**——模板里只有 5 个章节位。如果用户要 6 个章节，拆成两层或与用户沟通缩减。空位会在构建时自动删除，不留空白。
5. **section 章节编号建议 01–09**——模板字体是 2 位数样式，"10" 也能塞下但不美观。
6. **密级标记保留默认**——封面右上角"核心商密/普通商密/工作秘密/内部信息"由模板提供，不主动修改；如用户明确要求改密级，在 cover 的 slot 里传 `confidentiality: "core|normal|work|internal"`。
7. **不要尝试改字体**——华康金刚黑/等线已在母版声明，强行覆盖会让没装这两个字体的同事看到乱码。
8. **配色统一岚图青 #406A70**——版式已内置品牌色板，不要自行指定颜色。

## 当 LLM 拿不准时该怎么办

- **某段内容用哪个 variant 合适？** → 读 `references/template-matching.md` 的"判定流程图"
- **slot 字段叫什么名字？** → 看 `references/slides-example.json` 里同 kind/variant 的示例
- **章节数 6 个怎么办？** → 反问用户："模板目录最多支持 5 章，是合并为 4-5 章，还是放弃目录页？"
- **build_pptx.py 报"slot 未找到"？** → 说明 slides.json 字段名拼错了，参照 references 修正
