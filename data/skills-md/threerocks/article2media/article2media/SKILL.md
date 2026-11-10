---
name: article2media
description: 把文章或视频一键做成中文视觉内容的总入口：按推荐组合把 10 个可单独使用的能力串起来——文章抓取、视频转文字、改写（总结）、全文翻译、长图、卡片（小红书 3:4 / 4:5 / 1:1 / 9:16）、公众号排版、口播视频、白板论证、漫画。常用组合：原文→改写→长图（默认）、原文→改写→小红书卡片、原文→公众号排版、原文→总结→公众号、外文→翻译→公众号、原文长图 / 原文卡片（一字不改）、视频→逐字稿→改写→长图或卡片、一稿多发（长图 + 小红书 + 公众号）、文章→口播视频。输入：X/Twitter 长文与线程、网页、微信公众号、本地 Markdown、粘贴的正文；抖音、YouTube、B 站链接、本地视频/音频、.srt/.vtt。21 套主题，不指定时按内容选。Use when the user gives an article, URL, long post, video link or file and wants it turned into 总结图, 长图, 知识卡片, 小红书图文, 公众号排版, 口播视频, 原文排版, 白板, 漫画 — or wants several of them, or names a combo (一键、组合、全套、一稿多发) — e.g. "把这篇文章做成图/小红书/公众号/视频", "把这个抖音视频做成小红书", "翻译成中文发公众号".
argument-hint: <url|视频链接|文件|粘贴的正文> [组合名] [-f 原文|-w 白板|-c 漫画] [--ratio 3:4|4:5|1:1|9:16 或 小红书/IG] [公众号] [视频] [--style 主题名|all] [--illustrate] [--verify]
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/engine/scripts/doctor.mjs), Bash(node ${CLAUDE_SKILL_DIR}/../article-fetch/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../video-transcript/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../article-rewrite/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../article-translate/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../long-image/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../image-cards/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../wechat-layout/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../explainer-video/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../logic-whiteboard/scripts/*), Bash(node ${CLAUDE_SKILL_DIR}/../article-comic/scripts/*)
version: "2.0.1"
---

# article2media：推荐组合

article2media 由 10 个能力组成，**每个都是独立的 skill**，可以单独用，也可以按任意顺序组装。本 skill 是总入口：听懂用户要什么，选一个组合，依次调用各个能力，最后统一交付。本目录的 `engine/` 是所有能力共用的脚本、主题和版式。

参数：`$ARGUMENTS`

## 能力

| skill | 能力 | 输入 → 产出 |
|---|---|---|
| `article-fetch` | 文章抓取 | X 长文 / 网页 / 公众号 / 本地文件 → `article.md` |
| `video-transcript` | 视频转文字 | 抖音、YouTube、B 站、本地音视频、.srt/.vtt → `article.md`（逐字稿） |
| `article-rewrite` | 改写（总结） | `article.md` → `content.json`（改写稿），可导出 `rewrite.md` |
| `article-translate` | 全文翻译 | `article.md` → `article.zh.md`（不删减，逐块对应） |
| `long-image` | 长图 | `content.json` → 杂志长图；`article.md` → 原文长图 |
| `image-cards` | 卡片 | `content.json` → 总结卡片；`article.md` → 原文卡片（3:4 / 4:5 / 1:1 / 9:16） |
| `wechat-layout` | 公众号排版 | 文章（原文、译文或 `rewrite.md`）→ 可粘贴的图文 + 封面 |
| `explainer-video` | 口播视频 | 文章（可参考 `content.json`）→ 1080×1920 竖屏讲解视频 |
| `logic-whiteboard` | 白板论证 | `article.md` → 把推理摊成纵向主干的长图 |
| `article-comic` | 漫画 | `article.md` → 黑白漫画 + 3:4 卡片（需要出图能力） |

能力之间只通过工作目录里的文件交接；交接文件、"原文还是改写"的默认判断、怎么调用别的能力，都在 `references/pipeline.md`。**开始前先读它。**

## 推荐组合

| 组合 | 用户通常这么说 | 链路 |
|---|---|---|
| **总结长图**（默认） | 做成图、长图、总结图 | 取原文 → 改写 → 长图 |
| **小红书总结** | 做成小红书、卡片、3:4、IG | 取原文 → 改写 → 卡片 |
| **公众号排版** | 排成公众号、公众号排版 | 取原文 → 公众号排版 |
| **公众号总结** | 总结成一篇公众号 | 取原文 → 改写 → 导出 `rewrite.md` → 公众号排版 |
| **外文搬运** | 翻译成中文发公众号 | 取原文 → 翻译 → 公众号排版 |
| **原文长图** | 原文排版、全文长图、一字不改、`-f` | 取原文 → 长图（原文） |
| **原文卡片** | 全文做成小红书卡片、原文卡片 | 取原文 →（外文先翻译）→ 卡片（原文） |
| **视频转图文** | 这个视频做成长图 / 小红书 | 视频转文字 → 改写 → 长图或卡片 |
| **视频转文字** | 视频转文字、逐字稿 | 视频转文字（交付 `article.md`） |
| **一稿多发** | 长图、小红书、公众号都要 | 取原文 → 改写一次 → 长图 + 卡片 + 公众号（`rewrite.md`） |
| **文章转口播** | 做成视频、口播、视频号 | 取原文 → 口播视频 |
| **白板 / 漫画** | 论证图、`-w`；漫画、四格、`-c` | 取原文 → 白板 / 漫画 |

- **取原文**：文章用 `article-fetch`，视频用 `video-transcript`；用户直接粘贴正文时，自己写 `article.md`（见 pipeline.md 第 1 节）。
- 用户可以点名组合（`/article2media 小红书总结 <链接>`），也可以自己组装（"先翻译，再出原文卡片""改写后只要 1:1"），按用户说的顺序调用即可，表里没有的组合同样成立。
- 用户没点名组合时，按 pipeline.md 第 2 节的默认表判断原文还是改写，再从上表挑最接近的组合。**输入和输出分开判断**：给视频只说明原文是视频，产出仍按用户说的定。
- 以前的参数照样有效：`-f` = 原文长图，`-w` = 白板，`-c` = 漫画，`--ratio` / 平台名 = 卡片，"公众号" = 公众号排版，"视频" = 口播视频；`--style`、`--illustrate`、`--verify`、`--pages`、`--lang` 交给对应的能力。

## 流程

1. **环境检查**（本会话第一次）：`node ${CLAUDE_SKILL_DIR}/engine/scripts/doctor.mjs`。失败时把修复建议转告用户，然后停下。
2. **定组合**：不需要先跟用户确认，除非 pipeline.md 第 2 节说要问。
3. **依次调用能力**：按 pipeline.md 第 3 节调用每个 skill，照它的 SKILL.md 做完、检查通过（✗ 全部修完），再进入下一步。所有能力用同一个工作目录。
4. **一份改写稿多处用**：一稿多发时只改写一次；同一篇已有 `content.json` 时不要重写，只补新版式需要的字段。
5. **交付**：把每个能力的交付项合在一起说，按产物分组：
   - 每个产物的绝对路径；
   - 走了哪条组合（例如"原文 → 改写 → 3:4 卡片"）；
   - 用了哪个主题（你选的就一句话说明理由），以及怎么换主题、换版式；
   - 卡片贴出发帖文案，公众号贴出标题、摘要和封面路径；
   - 需要用户留意的地方：未核对的数字、抓取不全的段落、识别可能出错的专有名词、翻译检查的提示。
