---
name: prose-critique-zh
description: 审阅和改写普通中文文章、日常文本、散文、文学艺术评论和叙事片段。Use when the user says a Chinese passage has AI 味、翻译腔、太抽象、太端着、动作拆太细、意象不落地、句子不自然, or asks to polish, critique, rewrite, humanize, or tighten Chinese prose without changing its basic meaning.
---

# Prose Critique Zh

审改中文文本时，先读 `references/ERROR_INDEX.md`，再按命中的错误类型用文本搜索工具检索 `references/CORRECTIONS.md` 中的对应样本；不要把 `CORRECTIONS.md` 全量加入上下文。

## Workflow

1. 判断文本类型：日常表达、散文叙事、评论说明、文学艺术文本。保留原文本的用途和语气，不把所有文本都改成同一种“干净文风”。
2. 用 `ERROR_INDEX.md` 找AI味类型。优先识别句式、动作、意象、文气和口号感；不要机械套所有规则。
3. 用文本搜索工具在 `CORRECTIONS.md` 中定位同类样本。只打开命中的错误类型和相邻例子，不整篇读取或搬运。
4. 如果用户要“审稿”或“哪里怪”，先指出最影响阅读的一两处，再给改法。
5. 如果用户要“直接改”，给出改写后的正文；必要时在正文后用一两句话说明关键改动。

## Editing Principles

- 具体不是越细越好。自然动作不要拆成姿势标注。
- 意象必须落地。写信、桌子、雨、刀、屋子，就要让它们和人物、动作、语境有关。
- 少用“不是……而是……”“重点不在……而在……”这类聪明转折。能正面说清，就直接说。
- 不要用漂亮抽象句替代具体威胁、具体触感或具体关系。
- 不要为了去 AI 味，把文章削成口号或金句。文学文本允许有节奏、停顿和余味。
- 修改时尽量保留作者原来的观察角度。只修坏味，不替作者重写成另一篇文章。

## Output

普通改写任务：直接给改写后的文本。

审阅任务：按“问题 -> 原因 -> 修改建议”简洁说明，必要时给局部改写。

沉淀规则任务：先判断是否已有错误类型可以容纳；只有反复出现、现有类型覆盖不了的问题，才建议新增到 reference。
