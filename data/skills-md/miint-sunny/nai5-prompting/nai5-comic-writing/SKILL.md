---
name: nai5-comic-writing
description: Use when the user wants NovelAI prompt text for a settled comic or four-panel storyboard, asks for ready-to-use comic or four-panel prompts directly without a storyboard review, wants a page or panel export, or wants a targeted correction to existing comic prompt text.
---

Copyright (C) 2026 Miint-Sunny · GPL-3.0-only。项目与公开来源：[nai5-prompting](https://github.com/Miint-Sunny/nai5-prompting)。完整许可见 [LICENSE](LICENSE)，贡献范围见 [NOTICE](NOTICE)。

# 漫画写法补充

用于把已定漫画、四格或指定画格转成提示词，以及对现有漫画词句做局部修订。本包补充漫画表达，依赖已启用的 `nai5-writing`：读取其 `references/conventions.md` 的“写法规范与交付边界”“精确修改与保行为”“用户事实、原串与本次可见范围”，再按本次需要取语法、完整字段与质量 UC 章节。已读取且仍适用的规则直接沿用，不重复加载整包。

读 [漫画编译](references/comics.md) 的相关部分，按实际生成单元去重身份，用位置和大小定位各格，再把该格可见的人物、持物、接触与文字写入对应框；仅在当前分镜的字段编排或拆框写法不清楚时，查 [漫画示例](references/comic-examples.md) 对应段；示例不用于补人物、题材或剧情。分镜、读向、格数、服饰和冻结文字沿用现稿，只改指定格时不重做导演或扩成整页。共同规则与实际预设仍由核心确定，示例不替代它们。

这是先导演、后写词的转换阶段。完整新故事仍未审阅时先由 `nai5-comic-storyboard` 交完整三部分；用户说「直接给词」「只要提示词」「不用分镜」这类话而手里没有分镜时，本包在同一轮先给一份逐格简稿（一格一行，格数按本次内容定）并标明是本次补的，再给完整导出，自己补的分镜不称「已定」「现稿」或「已确认」；已有定稿、已有确认、按本次要求落实明确修改后，或明确跳过审阅时直接转换，不增加确认轮次；范围外的连带改动仍按核心的精确修改规则先列出、不擅自改。完整导出按页或已定生成单元给简短版式说明，再分别给主串、全部 `Character N:` 与实际 `UC:` 的可复制代码块，默认在代码块外逐框给格位和格内站位，并说明 AI's Choice → Custom 的手动定位步骤；用户明确省略设置说明或另有定位方式时按其要求处理，后页不写“同上”，也不重贴已审导演稿；交付前按 [漫画导出前核对](references/comics.md#comic-adapter.s08) 过一遍。只改指定格或词句时仅交相应替换。

完整稿中可直接按上述章节名阅读；独立包不附通用规则，也不会自动安装核心。核心不可用或规则未取得时，交现有资料能支持的内容并说明缺少哪些规则，不编造规范或假称已读。技术问题查核心 `references/sources.md` 的对应节；历史依据仅在用户明确要求核对时读取；普通写法只在本题确实涉及对应表达时选读。

此入口交文本。没有真实写入工具时，用户要求填工作台也只能拿到可填写内容，并如实说明未写入；纯文字修改不声称已执行设置或验证成图。
