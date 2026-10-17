---
name: nai5-reverse-prompt
description: Use when the user sends an image and wants a ready-to-use NovelAI V5 prompt reverse-engineered from it, or only one part of it (composition, lighting, colors, outfit, appearance, pose, expression, scene, relationships, or on-image text). Not for merely describing what an image shows.
---

Copyright (C) 2026 Miint-Sunny · GPL-3.0-only。项目与公开来源：[nai5-prompting](https://github.com/Miint-Sunny/nai5-prompting)。完整许可见 [LICENSE](LICENSE)，贡献范围见 [NOTICE](NOTICE)。

# 照图反推提示词

读 [照图反推](references/reverse.md)，照用户发来的图写一版能直接用的 NAI V5 提示词，或只推用户要的那一部分。本包只管看图、取舍和写到哪。语法、字段、质量尾与 UC 依赖已启用的 `nai5-writing`：读取其 `references/conventions.md` 的“写法规范与交付边界”“精确修改与保行为”“用户事实、原串与本次可见范围”“字段职责：先选画面类型”“将定稿组装为完整提示词”“完整导出的质量词与 UC”，再按本次需要读普通写法。图是漫画或分格时，另接 `nai5-comic-writing`。

画师串、画风、质量词、UC 和负权重都不从画面推；角色不凭长相认，不用 tagger 的结果；普通插画和多人图不给界面的角色位置。手部写清入画方向和接触位置，遮挡只描述实际可见部分；看不清的部位说明具体缺口并留空。回复里分开标原文、用户给的和推测。

独立包不附通用规则，也不会自动安装核心。核心不可用或规则未取得时，交现有资料能支持的内容并说明缺少哪些规则，不编造规范或假称已读。

此入口交文本。没有真实写入工具时，用户要求填工作台也只能拿到可填写内容，并如实说明未写入。
