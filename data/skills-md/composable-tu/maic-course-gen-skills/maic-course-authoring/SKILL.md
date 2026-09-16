---
name: maic-course-authoring
title: "MAIC 课件自主编写"
description: 用外部 Agent 依据原始材料自主编写 OpenMAIC 课件，并打包成可直接导入的 .maic.zip。适用于"帮我做一份关于 X 的课件/幻灯片/互动课堂""把这份材料变成一节课""生成 MAIC 课件""做成 .maic.zip"这类请求。内容全部由 Agent 依据用户上传的原始材料亲自撰写，不调用 OpenMAIC 内部生成流水线；版式复用上游的「克隆已有页面、只改文字」机制，结构由上游 JSON Schema 把关。不覆盖纯聊天、只要 PPTX 文件、或只问 OpenMAIC 用法的问题。
---

# MAIC 课件自主编写

你负责**亲自撰写**一份 OpenMAIC 课件，依据是用户提供的原始材料。

## 最高优先级规则

**在动手写任何内容之前，先读 [`references/grounding.md`](references/grounding.md)。**

它说明了为什么本 Skill 必须自己承担保真责任，以及四条不可违反的硬规则。
本仓库选择让 Agent 全程依据原文撰写。因此**保真是你的责任，不是工具的责任**：
工具能帮你读到原文、能校验结构，但「这句话是否真的来自材料」只有你能回答。

一句话总结：**每个事实性断言都必须能回指到材料原文。找不到出处的，要么删掉，
要么明确标注为补充知识。**

## 核心工作流

完整步骤见 [`references/workflow.md`](references/workflow.md)。骨架：

```text
0. 材料入库   material_list → material_read → material_search 抽查
1. 规划       从材料提炼单元 → 定页面清单（每项都指向材料出处）
2. 逐页写作   回原文取片段 → 按版式写 → draft_validate（一页一校验）
3. 成稿校验   数字逐字核对 → draft_validate 整份 → 走自检清单
4. 打包交付   course_pack_maic_zip → 交付并说明材料覆盖情况
```

**逐页校验，不要攒到最后。** 错误在大纲层是廉价的，在讲解稿层是昂贵的。

## 按需加载参考文档

不要一次读完所有参考。按当前任务加载：

| 你现在要做的事 | 读这个 |
| --- | --- |
| 任何写作之前的必读 | [`grounding.md`](references/grounding.md) —— 保真规则（**最高优先级**） |
| 完整流程与门禁 | [`workflow.md`](references/workflow.md) |
| 搞清文档结构、字段在哪、zip 与文档如何映射 | [`structure.md`](references/structure.md) |
| 打包、媒体引用、导入侧行为 | [`maic-zip.md`](references/maic-zip.md) |
| **不知道某个类型要哪些字段** | 先调 `dsl_schema_get`（权威必需字段表），再看索引 |
| 全部 25 个上游技能的路由 | [`skills/INDEX.md`](references/skills/INDEX.md) |
| 写幻灯片画布与十种元素 | [`slide-dsl`](references/skills/agent-runtime/slide-dsl/SKILL.md) —— 完整字段手册 |
| 版式、字号、对齐、留白、富文本陷阱 | [`slide-craft`](references/skills/agent-runtime/slide-craft/SKILL.md) —— 设计法则 |
| 复用已有页面的版式，不重画 | [`page-clone`](references/skills/agent-runtime/page-clone/SKILL.md)、[`style-clone`](references/skills/agent-runtime/style-clone/SKILL.md) |
| 写测验题 | [`quiz.md`](references/skills/agent-runtime/stage-dsl/references/quiz.md) |
| 写交互式内容（HTML 或 widget） | [`widget.md`](references/skills/agent-runtime/stage-dsl/references/widget.md) |
| 写 PBL 项目 | [`pbl.md`](references/skills/agent-runtime/stage-dsl/references/pbl.md) |
| 写讲解词、聚光灯、白板等播放动作 | [`actions.md`](references/skills/agent-runtime/stage-dsl/references/actions.md) |
| 课程级的 stage / scene 骨架 | [`stage-dsl`](references/skills/agent-runtime/stage-dsl/SKILL.md) |
| 规划讲什么（系列课 / 单节课 / 螺旋式 / UbD） | 见索引「三、决定讲什么」 |
| 决定怎么讲（讲授 / 工作坊 / 费曼 / SEL） | 见索引「四、决定怎么讲」 |
| 材料里的事实相互冲突 | [`fact-check`](references/skills/agent-runtime/fact-check/SKILL.md) |

`slide-dsl`（约 900 行）是最长也最密的一份。**只在你确实要写新元素类型时读它**；
字段清单以 `dsl_schema_get` 为准——本格式的 schema 是闭合的，未定义字段会被直接报出来。

## 硬规则

1. **无材料不写作。** 用户忘传附件时停下来问，不要用先验知识硬编。
2. **每个事实有出处。** 数字、公式、专有名词、日期、引文逐字核对。
3. **宁可留白不填空。** 页数服从材料容量，不为凑篇幅灌水。
4. **不要逐字重画版式。** 先把一页做好，之后用 `scene_clone` 复制版式、只换文字；
   写最小必需字段，再用 `draft_normalize` 让上游补默认值与可派生的几何。
5. **字段清单以 `dsl_schema_get` 为准。** 那是从上游 schema 运行时推导的权威表。
6. **一页一校验。** 每页写完立即 `draft_validate`，修完再下一页。
7. **不使用内部生成器。** 不要调用 OpenMAIC 的 `generate_scene` 之类能力；
   内容由你写。生成器只接管版式渲染，不接管内容。
8. **不写占位符 `src`。** 非 `http`/`data`/`blob` 的 `src` 会永远显示骨架屏。
9. **结构契约是闭合的。** 元素与动作都拒绝未定义字段，且不能改动 `id`/`type`。
   `draft_validate` 是结构闸门，**它抓不到教学法问题**——那是你的责任。
10. **文件写错不报错。** `manifest.json` 在导入侧只有三处校验（见 `maic-zip.md`），
    所以本地校验是不可省的。
11. **交付时如实说明。** 哪些材料被覆盖、哪些没覆盖、哪些解析失败，都要讲清楚。
12. **id 全篇唯一。** 元素 / 动作 / 题目 id 重复会让渲染层报重复 key。
    同一页调用两次同一个版式函数最容易撞 id。交付前跑 `scene_normalize_ids`。
13. **结构过了还要看版式。** 越界、文本溢出、元素压盖，schema 都不查。
    每页写完跑 `draft_layout`。

## MCP 工具

工具定义见 [`mcp/README.md`](mcp/README.md)。十个工具：

| 工具 | 用途 |
| --- | --- |
| `material_list` / `material_read` / `material_search` | 读原始材料（保真的根） |
| `dsl_schema_get` | 取结构契约、权威必需字段表与 `DSL_VERSION` |
| `draft_validate` | 结构校验 + **id 唯一性** + 引用完整性（**硬闸门**） |
| `draft_normalize` | 让上游补元素默认值、派生可派生的几何 |
| `draft_layout` | 版式检查：越界 / 文本溢出 / 折行 / 元素压盖 |
| `scene_clone` | 复制已有页面的版式，只改写文字槽位（自动处理 id） |
| `scene_normalize_ids` | 全篇 id 归一：加页前缀并去重，同步改写 spotlight 引用 |
| `course_pack_maic_zip` | 打出 `.maic.zip` |

`material_*` 需要一个材料目录。启动 MCP 时通过环境变量设定：

```bash
MAIC_MATERIALS_DIR=/path/to/source-docs node mcp/server.mjs
```

未配置时材料工具会返回明确错误——遇到这种情况提醒用户配置，
不要跳过材料步骤继续写作。

## 许可证与出处

`references/skills/` 下的全部内容（25 个技能包，53 个文件）原样取自
[THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC)（MIT 许可），
是该项目为 Agent 编写的课件领域知识库，质量很高，不应重写。
`references/skills/INDEX.md` 是本仓库新增的路由索引。

其余文件为本次新增。完整的归属与同步方式见仓库根目录
[`NOTICE.md`](../../NOTICE.md) 与 [`LICENSE-openmaic`](../../LICENSE-openmaic)。

当前基线 `@openmaic/dsl@0.11.1`，`DSL_VERSION = 0.3.0`。
