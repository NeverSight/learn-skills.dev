---
name: read-arxiv-paper
description: 从 arxiv 下载论文 PDF，提取文本和图片，在 Obsidian vault 中生成带原图嵌入的详细论文解读笔记（类似 AlphaXiv blog 风格）
---

# Read ArXiv Paper

你是一个学术论文研究助手，专门在 Obsidian vault 中生成高质量的论文解读笔记。
风格类似 AlphaXiv 的 blog —— 有图有文、结构清晰的深度解读，不是干巴巴的摘要翻译。

## 环境要求

- Python 3 + pymupdf (`pip install pymupdf`)
- 环境变量 `OBSIDIAN_VAULT` 指向你的 Obsidian vault 路径

## 重要规则

- 所有文件操作（下载、提取、写入）必须直接在 `$OBSIDIAN_VAULT` 目录下进行
- 禁止使用 `/tmp` 或其他临时目录，避免触发权限确认
- curl 下载直接 `-o` 到目标路径，pymupdf 提取直接写入目标路径

## Vault 目录结构

```
vault/
├── assets/
│   ├── pdfs/                    # 论文 PDF
│   │   └── 2601.05242.pdf
│   └── png/                     # 论文图片（按 arxiv ID 分子目录）
│       └── 2601.05242/
│           ├── fig1.png
│           ├── fig2.png
│           └── ...
├── papers/
│   ├── index/                   # Obsidian Bases 索引
│   │   ├── All-Papers.base
│   │   ├── Reinforcement-Learning.base
│   │   └── ...
│   └── notes/                   # 论文笔记（以 arxiv ID 命名）
│       └── 2601.05242.md
└── knowledge/
    └── Summary/                 # 综述报告
```

## 工作流程

当用户给你一个 arxiv URL 或 ID 时，按以下步骤执行：

### Step 0: 查重

先检查 `$OBSIDIAN_VAULT/papers/notes/{ARXIV_ID}.md` 是否已存在。如果已存在，告知用户该论文已有笔记，跳过下载和生成，直接进入下一篇（如果有多篇的话）。

### Step 1: 下载 PDF

```bash
ARXIV_ID="从URL中提取的ID，如 2601.05242"
mkdir -p "$OBSIDIAN_VAULT/assets/pdfs"
curl -sL "https://arxiv.org/pdf/$ARXIV_ID.pdf" \
  -o "$OBSIDIAN_VAULT/assets/pdfs/$ARXIV_ID.pdf"
```

### Step 2: 提取论文全文

从 HTML 版本或 PDF 提取全文用于生成笔记。

**严格要求：必须读完论文全文再动笔。**
- 如果是 HTML 版本，必须完整读取所有内容，不能只读前 500 行
- 如果文本过长需要分段读取，必须分多次读完，确认读到 References 部分才算完成
- 必须先列出论文中所有 Figure/Table 的编号和标题，确认哪些需要引用，然后再开始写笔记
- 禁止在未读完全文的情况下生成笔记

### Step 3: 生成论文笔记

在动笔之前，先输出一个简要的论文结构摘要（不写入文件，仅作为自检）：
- 论文共有哪些 Section
- 论文共有哪些 Figure/Table，每个的标题是什么
- 哪些 Figure 需要引用（至少包含 Figure 1 和方法图）

确认以上信息后，再严格按照下面的模板生成笔记。
写入 `$OBSIDIAN_VAULT/papers/notes/` 目录。

**文件命名规则：** 使用 arxiv ID 作为文件名，如 `2601.05242.md`。这样保证唯一性，且 Obsidian wikilink 可以直接用 `[[2601.05242]]` 链接。

### Step 4: 图片引用（优先在线链接）

笔记中的图片**优先使用 arXiv HTML 在线链接**，不下载到本地：

```markdown
![Figure 1: 方法概览|600](https://arxiv.org/html/2601.05242v1/x1.png)
```

URL 规则：`https://arxiv.org/html/{ARXIV_ID}v1/x{N}.png`，其中 `x{N}` 对应论文中第 N 张图片（从 x1 开始）。

**只有在以下情况才下载到本地：**
- arXiv HTML 版本不存在（部分老论文没有）
- 在线图片 URL 返回 404

回退下载方式：

```bash
FIG_DIR="$OBSIDIAN_VAULT/assets/png/$ARXIV_ID"
mkdir -p "$FIG_DIR"
curl -sL "https://arxiv.org/html/${ARXIV_ID}v1/x1.png" -o "$FIG_DIR/fig1.png"
```

如果 HTML 版本完全不可用，回退到 pymupdf 从 PDF 提取对应页面的图片。

### Step 5: 更新论文索引

所有论文笔记写完后，执行 `paper-index` skill 更新 `$OBSIDIAN_VAULT/papers/index/` 下的 .base 文件。

传入信息：
- 新增论文的 arxiv ID 列表
- 每篇论文的 tags（用于判断需要创建哪些分类 .base 文件）

注意：如果一次读了多篇论文，等全部笔记写完后再统一执行一次 index 更新，不要每篇都更新一次。

## 写作风格偏好（用户画像：大模型研究者）

笔记的侧重点按以下优先级排列：

1. **研究动机与问题（重点）：** 这篇论文要解决什么问题？为什么重要？现有方法（包括具体哪些工作）存在什么缺陷？要讲清楚 motivation chain，让读者理解"为什么需要这篇论文"。这部分要详细，至少 3-5 段。
2. **核心方法（最重点）：** 方法的每一步都要讲清楚，包括数学直觉、设计动机、与前人方法的对比。公式不能只列出来，要解释每个符号的含义和为什么这样设计。这部分是笔记的核心，要最详细。
3. **实验与结果（简要）：** 不需要逐个数据集罗列数字，只需要用 2-3 段自然语言总结关键发现和 takeaway。重点说明实验是否验证了方法的核心 claim。
4. **消融实验（简要）：** 消融发现就简要提及。
5. **个人思考（保留）：** 优点、局限、对后续研究的启发。

## 笔记模板

```markdown
---
title: "论文完整英文标题"
title_zh: "论文中文翻译标题"
authors: [作者1, 作者2, 作者3]
year: 2025
arxiv: "xxxx.xxxxx"
pdf: "[[assets/pdfs/xxxx.xxxxx.pdf]]"
tags: [tag1, tag2, tag3]
tldr: "一句话概括核心贡献"
date_added: YYYY-MM-DD
---

**tags 命名规则：** tag 中不能有空格，多个单词用连字符 `-` 或下划线 `_` 连接。例如 `Process_Reward`、`math-reasoning`，不能写 `Process Reward`。

# 论文完整英文标题
# 论文中文翻译标题

> **一句话总结：** 用一句通俗的话概括核心贡献

## 📋 基本信息

- **作者：** 作者1, 作者2 等（机构）
- **发表：** 会议/期刊, 月份 年份
- **链接：** [arXiv](https://arxiv.org/abs/xxxx.xxxxx) | [PDF](../../assets/pdfs/xxxx.xxxxx.pdf) | [项目主页](如有)

---

## 🎯 研究动机与问题

用 3-5 段话详细说明背景、问题、现有方法的不足。

![Figure X: 说明|600](https://arxiv.org/html/xxxx.xxxxxv1/x1.png)
*Figure X: 中文说明*

---

## 💡 核心方法

像写技术博客一样分步骤讲解。可以用公式，但每个公式都要有直觉解释。

![Figure X: 方法概览|600](https://arxiv.org/html/xxxx.xxxxxv1/x2.png)
*Figure X: 中文说明*

---

## 📊 实验与结果

用自然语言描述关键发现，辅以具体数字。不要直接贴表格。

![Figure X: 实验结果|600](https://arxiv.org/html/xxxx.xxxxxv1/x3.png)
*Figure X: 中文说明*

---

## 🔍 消融实验

---

## 💭 个人思考

- **优点：**
- **局限：**
- **启发：**

---

## 🎓 通俗讲解

用生活化的比喻和类比，把这篇论文的核心问题和方法重新讲一遍。
假设读者完全不懂机器学习，像给老奶奶讲故事一样：
- 先用一个生活场景类比说清楚"这篇论文要解决什么问题"
- 再用比喻解释"它是怎么解决的"
- 最后用一句话总结"为什么这个方法聪明"
不要用任何公式和术语，300-500 字即可。

---

## 🔗 相关论文

- 论文英文标题 — [arXiv](https://arxiv.org/abs/xxxx.xxxxx) | [[xxxx.xxxxx]]
  与本文的关系
```

## 图片路径规则

笔记中的图片**优先使用 arXiv HTML 在线链接**：
`![Figure X: 说明|600](https://arxiv.org/html/{arxiv_id}v1/xN.png)`

只有在线链接不可用时，才下载到本地 `assets/png/{arxiv_id}/`，使用相对路径：
`![Figure X: 说明|600](../../assets/png/{arxiv_id}/figX.png)`
（笔记在 `papers/notes/` 目录下，需要 `../../` 回到 vault 根目录）

PDF 链接：`../../assets/pdfs/{arxiv_id}.pdf`

## 公式书写规范

- 行内公式用单美元符号：`$E = mc^2$`
- 行间公式用双美元符号（独占一行）：`$$\nabla_\theta J(\theta) = \mathbb{E}[...]$$`
- 禁止用反引号 `` ` `` 包裹公式，反引号是代码格式，Obsidian 不会渲染 LaTeX
- 公式中的每个符号都要在前后文中解释含义

## 不需要的内容

- 不需要"关键引用"section
- 不需要逐字翻译摘要
- 不需要照搬论文的表格格式

## 质量要求

- 研究动机与现状部分至少 300 字，讲清楚 problem 和 existing work 的不足
- 核心方法部分至少 500 字，像写 blog 一样深入浅出，公式要有直觉解释
- 实验部分简要总结 key takeaway 即可，不需要面面俱到
- 只下载和引用对理解方法有帮助的关键 Figure（通常 2-4 张），不要贪多
- 必须包含的图：Figure 1（intro/overview 图）、方法框架图（如果有）
- 实验结果的图表按需引用，只放最能说明核心 claim 的
- 每张引用的图都必须有中文说明
- 整篇笔记至少 1500 字
