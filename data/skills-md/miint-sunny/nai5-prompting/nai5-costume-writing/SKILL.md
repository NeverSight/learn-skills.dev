---
name: nai5-costume-writing
description: Use when the user wants prompt wording for a settled outfit, a clothing-only fragment, clothing in a complete image prompt, or a targeted correction to clothing prompt text.
---

Copyright (C) 2026 Miint-Sunny · GPL-3.0-only。项目与公开来源：[nai5-prompting](https://github.com/Miint-Sunny/nai5-prompting)。完整许可见 [LICENSE](LICENSE)，贡献范围见 [NOTICE](NOTICE)。

# 服装写法补充

用于把已定服装转成衣物片段、放入完整画面，或精确修改现有衣物词句。本包补充服装表达，依赖已启用的 `nai5-writing`：读取其 `references/conventions.md` 的“写法规范与交付边界”“精确修改与保行为”“用户事实、原串与本次可见范围”，语法、字段和实际预设按本次需要选读。已读取且仍适用的规则直接沿用，不重复加载整包。

读 [服装表达](references/costume.md) 的相关部分。把颜色、材质、长度和装饰放在它们所属的部件旁；内外覆盖、单侧滑落和携带方向用短关系句写清。只要衣物片段就交该片段，明确不带角色时省略角色信息；完整画面则接核心的字段与质量 UC，不让片段默认截断请求。服装进入已定漫画时，漫画字段由已启用的 `nai5-comic-writing` 补充。保留用户部件、位置、数量、材质、印字与冻结原串，局改只动当前范围，已有服装不重新设计。

完整稿中可直接按同名章节阅读；独立包不附通用规则，也不会自动安装核心。核心或本题所需补充不可用时，交现有资料能支持的内容并说明哪些规则尚未载入，不编造规范或假称已读。术语来源按需查核心的 `references/sources.md` 中“查询依据”，未实际查询的词不称已验证。

此入口交文本。没有真实写入工具时，用户要求填工作台也只能拿到可填写内容，并如实说明未写入；纯文字修改不声称已执行设置或验证成图。
