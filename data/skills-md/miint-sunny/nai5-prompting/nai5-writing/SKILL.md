---
name: nai5-writing
description: Use when the user needs general NovelAI prompt syntax, field or preset guidance, wording for a settled ordinary illustration, or an exact edit or correction to existing prompt text.
---

Copyright (C) 2026 Miint-Sunny · GPL-3.0-only。项目与公开来源：[nai5-prompting](https://github.com/Miint-Sunny/nai5-prompting)。完整许可见 [LICENSE](LICENSE)，贡献范围见 [NOTICE](NOTICE)。

# 通用提示词写法与精确改词

承接用户已定内容，按 [写法契约](references/conventions.md#writing-conventions) 选择本次终点；共同语法、预设、用户事实与原串保护只在此确立。普通完整画面再读 [普通写法](references/illustration.md)，用户限定了修改范围（一处或多处）时按 [精确修改](references/conventions.md#writing-exact-edit) 处理：范围外字符不动，连带改动只列不改，范围不清先问。技术问题按需读 [共享依据](references/sources.md) 的对应节；历史依据仅在用户明确要求核对时读取。

漫画或四格的逐格编译由已启用的 `nai5-comic-writing` 补充，已定衣物片段及服装表达由已启用的 `nai5-costume-writing` 补充；当前任务需要时才读取，不默认全载。使用完整稿时直接读对应同名章节，无需另装技能。只有核心而缺少所需补充时，完成现有规则能支持的部分，说明专项规则尚未载入，不把普通模板当作已完成的专项交付。

转换时把已定对象和属性组织为词组，把持物、接触、遮挡、前后远近写成关系句；完整外貌按角色类型放入对应字段。保留已定剧情、镜头、服装与文字；缺少创作决定时只指出具体缺口，按本次需要接相应构思任务，现稿充分则直接交付，已有确认不再索要。完整字段、衣物片段和局改的范围分别遵循当前契约；不因某个示例或领域默认重写用户锁定内容。

交完整提示词时，按[定稿装配](references/conventions.md#writing-final-assembly)从待交付文本依次核对对象与姿势词组、当前绘色、主串结尾和 UC；缺项补在所属字段，沿用项对照来源。检查完成后交可复制文本，检查过程不额外写进提示词。

此入口交文本。没有真实写入工具时，用户要求填工作台也只能拿到可填写内容，并如实说明未写入；纯文字修改不声称已执行设置或验证成图。
