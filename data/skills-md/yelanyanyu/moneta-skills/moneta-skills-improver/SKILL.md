---
name: moneta-skills-improver
description: 当用户已经确认 Moneta 的风格规则、纠错压缩方案或流程变化，需要把反馈反哺到 word-disclosure、phrase-disclosure、write-review 等 Moneta skills 时使用。它把纠错样本整理和 skills 优化合并成一个用户可理解的改进动作。
---

# Moneta Skills Improver

改进 Moneta skills，不把内部细节交给用户。

## 影响范围

这个 skill 的工作对象是本仓库的 Moneta skills 文件和 reference 文件。可以修改：

- 目标技能入口文件：`skills/<skill-name>/SKILL.md`，例如 `skills/word-disclosure/SKILL.md`、`skills/moneta-critique/SKILL.md`、`skills/ask-yanyu/SKILL.md`。
- 目标技能参考文件：`skills/<skill-name>/references/*.md`，例如 `skills/word-disclosure/references/ERROR_INDEX.md`、`STYLE.md`、`CORRECTIONS.md`、`SOURCES.md`。
- 当反馈影响入口路由时，可以修改 `skills/ask-yanyu/SKILL.md`；当反馈影响改进流程本身时，可以修改 `skills/moneta-skills-improver/SKILL.md`。

不要把普通文章个案直接扩展成全局规则；先看目标技能的错误索引和现有纠错类型。

先把用户确认过的反馈分成四类：旧规则的新例子、当前文章个案、重复样本、新规则。分类时优先归入已有问题类型；不要因为一个坏句多了一个表面特征，就新建规则。

新增规则的门槛要高。只有当问题足够典型、可能反复出现，并且现有规则或纠错样本确实覆盖不了时，才创建新规则。否则，把它写进已有错误类型的例子、修改方案或当前文章个案里。

然后自行判断应该改哪里：

- 纠错样本太长或重复：压缩、合并，必要时归档。
- 问题来自流程：改目标 skill 的流程。
- 问题来自风格：改风格或纠错 reference。
- 问题来自来源搜索：改来源 reference。
- 问题只是已有风格问题的一个新表现：补到现有 CORRECTIONS 类型下，不新增 STYLE 条目。

压缩 CORRECTIONS 短例时，优先把同类坏句合并到一个错误类型下，用“例子 -> 问题 -> 修正后”的嵌套列表。只有涉及完整剧情、来源上下文或人物动机断裂的样本，才保留展开段落。

整理 CORRECTIONS 的例子标题时，不要写单词名、文本类型或规则结论。标题只补充坏例语境，概括坏例正在写什么，可以适当引申文本处境；不要提前写出问题、修正方向或规则结论。例如写“对灰心泥沼故事的描写与介绍”，不要写“对故事改写语言边界的处理”。

压缩或删除用户给过的样本前，先给用户看提案并等确认。

改完后只汇报用户关心的内容：吸收了哪条反馈、改进了哪些 Moneta skills、哪些反馈没有写入长期规则。用户确认稳定后，提醒 commit；需要同步到其他环境时提醒 push。
