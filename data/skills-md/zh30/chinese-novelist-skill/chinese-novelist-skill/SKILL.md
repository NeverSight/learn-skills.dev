---
name: chinese-novelist-skill
description: Use when the user wants to plan, write, continue, revise, or export a Chinese novel, web novel, serialized story, chapter outline, character bible, or chapter draft in Chinese. Also use when user wants to export novel as EPUB or check chapter word count.
---

# Chinese Novelist

## Version

- **Version**: `0.6.1`
- **Version Date**: `2026-03-09`
- **Compatibility**: standard Markdown skill loaders that support `name` and `description` frontmatter
- **Previous Versions**: see [CHANGELOG.md](CHANGELOG.md)

## Overview

为中文长篇小说和网文创作提供一套可持续执行的工作流：先稳住设定与大纲，再按章节推进，持续维护人物状态、悬念台账和文风质量，避免写到后面失控、注水或前后打架。

## When to Use

- 用户要从零开始写中文小说、网文、长篇故事、连载故事
- 用户已有设定，想补大纲、人物档案、世界观、章节规划
- 用户要续写已有章节，要求前后连贯
- 用户要重写某章，增强钩子、节奏、对白、人物张力或减少 AI 味
- 用户要将小说导出为 EPUB 电子书（如"帮我导出 epub"、"把这本书导出为电子书"）
- 用户要检查章节字数（如"帮我看看这章多少字"）

## Default Working Mode

先判断用户要的交付深度，再选最轻的有效模式：

1. `策划模式`：只做题材定位、故事引擎、大纲、人物、世界观、伏笔台账
2. `试写模式`：策划完成后，只写首章或样章
3. `连载模式`：按章推进，每次交付 1 章或少量连续章节
4. `完稿模式`：只有在用户明确要求整本初稿时，才连续写完整部长篇

如果用户没有说清楚：
- 新项目默认 `策划模式`
- 已有章节的项目默认 `连载模式`

## Intake

只补问真正缺失的关键信息，优先补齐以下 6 项：

- 题材 / 子类型
- 一句话 premise 或核心冲突
- 主角身份、最大欲望、致命缺陷
- 目标读者、文风关键词、禁忌
- 叙事视角（第一人称 / 第三人称 / 群像）
- 篇幅目标与交付模式

如果用户只给了模糊想法，不要空泛追问；应给出具体备选并推荐更稳的方案。

## Required Files

在 `novels/<书名>/` 内创建或更新：

- `00-大纲.md` → 使用 [outline-template.md](references/outline-template.md)
- `01-人物档案.md` → 使用 [character-template.md](references/character-template.md)
- `02-世界观与伏笔.md` → 使用 [story-bible-template.md](references/story-bible-template.md)
- `第XX章-标题.md` → 使用 [chapter-template.md](references/chapter-template.md)

## Planning Rules

开始批量写章节前，至少锁定以下内容：

- `logline`
- 主线冲突、对抗力量、利害关系
- 主角外部目标与内在成长弧线
- 结局类型与兑现方式
- 采用的结构模板（参见 [plot-structures.md](references/plot-structures.md)）
- 逐章功能分配
- 未回收悬念、伏笔、时间线、关系状态

除非用户明确要求跳过规划，否则不要直接写完全书。即使用户要求“直接开写”，也先产出一页精简总纲再动笔。

## Chapter Loop

每写一章都按这个循环执行：

1. 读取 `00-大纲.md`、最近章节摘要、`02-世界观与伏笔.md`
2. 明确 `本章目标 / 阻碍 / 转折 / 结尾钩子`
3. 先拆 3-6 个场景，再落正文
4. 开头前 20% 必须尽快进入冲突，参考 [chapter-guide.md](references/chapter-guide.md)
   - 如果在写首章，额外参考 [opening-design.md](references/opening-design.md)
5. 对话、扩写、连贯性、结尾钩子分别参考：
   - [dialogue-writing.md](references/dialogue-writing.md)
   - [content-expansion.md](references/content-expansion.md)
   - [consistency.md](references/consistency.md)
   - [hook-techniques.md](references/hook-techniques.md)
   - [scene-design.md](references/scene-design.md)
   - [style-polishing.md](references/style-polishing.md)
6. 长章节交付前，运行：
   - `python3 scripts/check_chapter_wordcount.py <章节文件路径>`
7. 交付前用 [quality-checklist.md](references/quality-checklist.md) 自查
8. 回写章节摘要、人物状态、伏笔状态与章节进度

## Export

当用户要求导出 EPUB 时：

1. 确认小说目录路径（用户已提供或在 novels/ 下查找）
2. 运行导出脚本：
   ```bash
   python3 scripts/generate_epub.py <小说目录路径>
   ```
3. 可选参数：
   - `--author <作者名>` 覆盖大纲中的作者
   - `-o <输出路径>` 指定输出文件位置
   - `--lang en` 导出英文版（需要先通过翻译功能生成 `en/` 目录）
4. 告诉用户生成的 EPUB 文件路径

## Quality Bar

每章至少满足：

- 本章发生了不能删除的变化
- 回应、升级或偏转至少一条已有悬念
- 结尾钩子强度与全书位置匹配
- 人物通过动作、选择、对白被展示，而不是只被描述
- 避免空泛形容词堆砌、抽象情绪总结、整段均匀句式和过度书面腔
- 每个章节至少包含若干有任务的场景，而不是流水账拼接

## Completion

在 `完稿模式` 收尾时，必须额外检查：

- 主线悬念是否回收
- 主角弧线是否完成
- 设定规则是否前后一致
- 是否存在遗失角色、断裂线索、无兑现伏笔
- 是否需要留下续作钩子；只有用户要时才保留
- 终稿收尾方式参考 [ending-design.md](references/ending-design.md)

## Translation

当用户要求翻译成英文时执行：

### 执行流程

**第一步：准备阶段**
1. 确认小说目录和翻译范围（全本 / 部分章节）
2. 读取上下文文件：
   - `00-大纲.md` → 书名、作者、类型、简介
   - `01-人物档案.md` → 人物信息
   - `02-世界观与伏笔.md` → 世界观要点

**第二步：生成术语表**
3. 分析小说内容，提取需要统一的术语：
   - 角色人名及拼音
   - 修炼体系/境界名称
   - 武器、法宝、门派名称
   - 中文特有词汇（功夫、气功、灵气等）
   - 量词和时间表达

**第三步：并行翻译**
4. 将章节分成多个批次（每批 2-3 章，相邻章节在同一批次）
5. 为每个批次创建一个 subagent，并行翻译
6. 每个 subagent 携带：小说信息 + 术语表 + 翻译规则

**第四步：最终校对**
7. 所有翻译完成后，派一个 subagent 做全局校对：
   - 检查术语一致性
   - 检查人名一致性
   - 检查剧情衔接
   - 修正发现的问题

**第五步：保存结果**
8. 汇总所有翻译结果，写入 `en/` 目录：
   - `Chapter-001.md`, `Chapter-002.md` 等

### 术语表格式

```
## 统一术语表（必须严格遵守）

### 人物名称
- [角色名] → [Pinyin]
- 张三 → Zhang San
- 李四 → Li Si

### 修炼体系
- 筑基 → Foundation Building
- 金丹 → Golden Core
- 元婴 → Nascent Soul
- 灵气 → Spiritual Energy
- 真气 → True Qi

### 门派与武器
- [门派名] → [Pinyin or English]
- 青云门 → Qingyun Sect
- 太极剑 → Taiji Sword

### 中文特有表达
- 盏茶 → the time it takes to drink a cup of tea
- 片刻 → a moment
- 一盏茶时间 → the time needed to finish a cup of tea
```

### Subagent 翻译提示词

```
# 翻译任务

你是专业的小说翻译专家。请将以下中文小说章节翻译为流畅的英文。

## 小说信息
- 书名：[书名]
- 作者：[作者]
- 类型：[类型]
- 简介：[简介]

## 人物（必须使用以下统一译名）
[人物档案要点]

## 世界观
[世界观与伏笔要点]

## 统一术语表（必须严格遵守）
[术语表内容]

## 翻译规则
1. 保持故事的叙事节奏和情感张力
2. 角色名字必须使用上面的统一译名
3. 术语必须使用统一术语表中的翻译
4. 使用现代英语，避免生硬的直译
5. 对话自然流畅，符合人物性格
6. 翻译后的章节保存为 Markdown 格式

## 待翻译章节（同一批次，情节连贯）
[章节1: 标题]
[章节1内容]

[章节2: 标题]
[章节2内容]

## 输出要求
为每个章节创建 Markdown 文件，文件名格式：Chapter-XXX.md
文件内容格式：
## 章节标题

## Body

翻译正文...
```

### 校对 subagent 提示词

```
# 翻译校对任务

请检查以下所有翻译章节，确保一致性：

## 统一术语表
[术语表内容]

## 翻译规则
1. 所有角色名字是否统一
2. 所有术语翻译是否一致
3. 连续章节的剧情是否衔接顺畅
4. 语气和风格是否统一

## 待检查章节
[所有已翻译的章节内容]

## 输出
列出发现的问题及修正建议。如果没有问题，回复"校对通过"。
```
```

### 英文版导出

英文版也支持 EPUB 导出：
```bash
python3 scripts/generate_epub.py <小说目录路径> --lang en
```
