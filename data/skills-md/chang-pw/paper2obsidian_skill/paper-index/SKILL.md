---
name: paper-index
description: 使用 Obsidian Bases 维护论文数据库，自动生成和更新 .base 文件实现动态分类视图
---

# Paper Index

使用 Obsidian Bases（.base 文件）维护论文数据库索引。Bases 是 Obsidian 1.9+ 的原生功能，能从笔记 frontmatter 自动生成数据库视图，无需手动维护表格。

## 触发条件

当用户要求"更新索引"、"整理论文"、"生成论文列表"时加载此 skill。
也会在 read-arxiv-paper skill 完成后自动执行。

## 前置要求

- Obsidian 1.9+ （内置 Bases 功能）
- 论文笔记的 frontmatter 必须包含以下字段：title, title_zh, authors, year, arxiv, pdf, tags, tldr, date_added

## 目录结构

```
vault/
├── papers/
│   ├── index/                   # .base 文件存放目录
│   │   ├── All-Papers.base      # 总库
│   │   ├── Reinforcement-Learning.base  # 分类库
│   │   ├── Reasoning.base       # 分类库
│   │   └── ...
│   └── notes/                   # 论文笔记
│       ├── 2402.03300.md
│       └── ...
```

## 工作流程

### Step 1: 扫描论文笔记

读取 `$OBSIDIAN_VAULT/papers/notes/` 下所有 `.md` 文件的 frontmatter，提取 tags 字段。

### Step 2: 确定分类

收集所有论文的 tags，按以下规则映射为分类（中文名）：

- `reinforcement-learning`, `GRPO`, `PPO`, `RLHF`, `DAPO`, `Dr-GRPO` → **Reinforcement-Learning**
- `alignment`, `DPO`, `preference` → **Alignment**
- `attention`, `transformer`, `architecture` → **Architecture**
- `math-reasoning`, `reasoning`, `chain-of-thought` → **Reasoning**
- `data`, `pretraining`, `scaling` → **Pretraining**
- `distillation`, `knowledge-distillation` → **Distillation**
- `video`, `video-generation`, `video-distillation` → **Video-Generation**

一篇论文可以属于多个分类（只要 tags 匹配多个分类规则）。
遇到无法归类的新 tag 时，自行创建合理的英文分类名。

tags 中不能有空格，多个单词用连字符 `-` 或下划线 `_` 连接。

### Step 3: 检查已有 .base 文件

检查 `$OBSIDIAN_VAULT/papers/index/` 目录下已有的 .base 文件。

### Step 4: 生成/更新 .base 文件

**总库（All-Papers.base）：** 如果不存在则创建，已存在则不覆盖。

```yaml
filters:
  and:
    - file.inFolder("papers/notes")
    - 'file.ext == "md"'

properties:
  title:
    displayName: "Title"
  title_zh:
    displayName: "中文名"
  tldr:
    displayName: "TLDR"
  tags:
    displayName: "标签"

views:
  - type: table
    name: "All Papers"
    order:
      - file.name
      - title_zh
      - title
      - tldr
      - tags
    groupBy:
      property: year
      direction: DESC
```

**分类库（{Category-Name}.base）：** 对每个分类，如果对应的 .base 文件不存在则创建。filter 条件使用 `tags.contains("tag-name")` 匹配。如果一个分类对应多个 tag，用 `or` 组合：

```yaml
filters:
  and:
    - file.inFolder("papers/notes")
    - 'file.ext == "md"'
    - or:
        - 'tags.contains("reinforcement-learning")'
        - 'tags.contains("GRPO")'
        - 'tags.contains("PPO")'

properties:
  title:
    displayName: "Title"
  title_zh:
    displayName: "中文名"
  tldr:
    displayName: "TLDR"
  tags:
    displayName: "标签"

views:
  - type: table
    name: "Category-Name"
    order:
      - file.name
      - title_zh
      - title
      - tldr
      - tags
    groupBy:
      property: year
      direction: DESC
```

## 重要规则

- .base 文件使用 YAML 格式，不是 Markdown
- 已存在的 .base 文件不要覆盖（用户可能手动调整过视图配置）
- 只创建新分类对应的 .base 文件
- 分类名使用英文，如 "Reinforcement-Learning"、"Reasoning"
- filter 中的 tag 必须与论文 frontmatter 中的 tags 完全匹配（区分大小写）
