---
name: product-spec
description: 管理产品功能规范——功能清单、交互逻辑、以及 Flyway 式版本化的新增与变更记录，产出可直接喂给 Claude Design、v0、Figma Make、Lovable 等 AI 设计工具的规范文件。规范落 products/specs/<产品线>/，V 链（V1__baseline、V2__xxx）记录演进，合成的 CURRENT.md 是喂设计工具的唯一入口。在用户说「建产品功能规范」「写功能规格」「记录这次产品变更」「生成给设计工具的规范」「同步 CURRENT.md」「product-spec」时使用，也用于新产品线初始化规范、或规范与实现漂移需要核对时。
argument-hint: "[init | add <title> | sync | check | export --tool <v0|figma-make|claude-design|lovable>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# product-spec

管理一份**产品功能规范**：产品有哪些功能、每个页面怎么交互、以及每次演进改了什么。产出物的第一读者是 AI 设计工具（Claude Design / v0 / Figma Make / Lovable），第二读者才是人。Reply in Chinese.

## Codex Adapter

In Codex, translate this wrapper instead of rewriting it:

- `$ARGUMENTS` = text after the command name.
- `AskUserQuestion`: only map to `request_user_input` if your Codex build truly renders an interactive picker; otherwise print each option's content in your reply, list choices as a numbered Markdown list, and **stop and wait** for the user's text reply. Never self-answer a prompt the user never saw.
- Claude tool names are intent labels; use equivalent Codex tools.

---

## 为什么是「V 链 + 合成快照」双轨

产品规范有两个互相打架的诉求：

- **追溯**——「关联应用这列什么时候改叫关联空间的、为什么」，要的是**增量链**
- **喂设计工具**——要的是**当前全量态**

纯 Flyway 增量链只满足前者。当前态得靠脑内重放 V1→Vn，人能做，设计工具做不了：把 V1 和 V2 一起丢给 v0，它会照着 V1 里那个已被 V2 改名的字段画。反过来，每个 V 都存全量则 diff 全是噪音，追溯等于没有。

所以两轨并行，各司其职：

| 轨 | 文件 | 谁写 | 谁读 |
|---|---|---|---|
| 增量链 | `V1__baseline.md`、`Vn__<slug>.md` | 人 + skill 访谈 | 人、审计、追溯 |
| 当前态 | `CURRENT.md` | **只有 `sync` 能写** | AI 设计工具 |

这条分离抄自 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 的 `specs/` + `changes/`。

## 目录约定

```
products/specs/
├── README.md                 # 格式说明 + 给设计工具的使用说明
├── console/                  # 一个产品线一套 V 链，独立编号
│   ├── CURRENT.md            # ← generated，勿手改
│   ├── V1__baseline.md
│   └── V2__data_space.md
└── portal/
    ├── CURRENT.md
    └── V1__baseline.md
```

完整格式定义（frontmatter、定位符语法、章节清单）见 `references/spec-format.md`。可直接抄的骨架见 `references/templates.md`。

## 不可协商的六条纪律

体系烂掉都是从破这几条开始的：

1. **`CURRENT.md` 只能由 `sync` 写。** 手改它等于让两轨脱钩，下次 `sync` 会静默覆盖掉你的修改。要改内容就发新 V 文件。
2. **`status: active` 的 V 文件不回改。** 改了等于改历史，追溯就废了。改需求就发下一个 V。只有 `draft` 可以随便改。
3. **定位符必须能在前序 V 链里解析到。** 解析不到就**报错并停下**问用户，绝不猜。猜错会在 `CURRENT.md` 里留下一个幽灵页面，而且没人会发现。
4. **只写「是什么 / 怎么交互」，不写像素、色值、字号、间距。** 视觉层归 `products/design/`（若项目有 `tokens.css` / `DESIGN.md` 就指向它）。规范里出现 `#0066FF` 或 `padding: 16px` 一律删掉。
5. **对外文案以项目 CLAUDE.md 为准。** 内部代号、内部服务名不得出现在规范正文里——它会被设计工具原样画进界面。
6. **写完必须 `sync`。** `add` 子命令自带这一步，别跳过。

## 子命令路由

解析 `$ARGUMENTS` 第一个词：

| 参数 | 动作 |
|---|---|
| `init` | 初始化规范体系 |
| `add <title>` | 新增一个 V 变更文件 |
| `sync` | 重放 V 链，生成/更新 `CURRENT.md` |
| `check` | 一致性与漂移检查 |
| `export --tool <name>` | 按工具方言导出 prompt 包 |
| 空 | 先跑 `check`，把结果和可用子命令一起报给用户，让他挑 |

多产品线时，若 `$ARGUMENTS` 没点名产品线且目录下不止一个，用 AskUserQuestion 让用户选，别默认第一个。

---

## init

**前置**：若 `products/specs/<产品线>/V1__baseline.md` 已存在，停下告诉用户已初始化，改用 `add`。

1. **勘察取证**（先看再问，能从代码推断的别浪费用户的话）：
   - 高保真原型图片：`products/design/`、`products/design/screenshots/`
   - 前端路由与页面：`src/pages/`、`src/routes/`、路由表文件
   - 导航结构：找 `Shell`/`Layout`/`Sidebar`/`nav` 定义，它通常直接给出分组 → 菜单 → 页面 id 的完整树
   - 后端 API 与枚举：Controller 路径、枚举类的中文映射（术语表的来源）
   - 项目 CLAUDE.md：对外称谓、锁定决策、UI 约定

2. **访谈**（只问推断不了的，一次 AskUserQuestion 问完）：
   - 产品线怎么划分（若原型里已能看出 console/portal 之类的分裂，把推断结果作为选项给他确认，而不是开放提问）
   - 每条产品线的目标用户与角色
   - 有没有「明确不做」的东西（这条最值钱，见下）

3. **产出**：
   - `products/specs/README.md`（格式说明 + 使用说明，抄 `references/templates.md` 的 README 骨架）
   - 每条产品线一个目录 + `V1__baseline.md`
   - 跑 `sync` 生成各自的 `CURRENT.md`

4. **V1 起草原则**：
   - 页面 id **沿用原型/代码里已有的 id**（如 `apps`、`complianceStats`），别自创一套，否则定位符和实现对不上
   - 从原型能读出来的（字段、列、按钮、弹层）直接写实；读不出来的（前置条件、错误态、极值）**标 `<!-- TODO: 待确认 -->` 而不是编**
   - 起草完把所有 TODO 列给用户，一轮问清楚

## add \<title\>

1. 定位产品线，扫目录取当前最大版本号 N，新文件是 `V{N+1}__<slug>.md`。slug 从 title 生成：小写、下划线分词、只留 ASCII，如「数据空间架构重构」→ `data_space`（中文标题由用户给或你提议，让他确认）。
2. 读 `CURRENT.md` 拿当前态——**这是填变更清单的依据**，不要去读一堆 V 文件自己重放。
3. 访谈驱动填**变更摘要**和**变更清单**表。每行必须齐三样：操作（`ADD`/`MODIFY`/`MOVE`/`RENAME`/`REMOVE`）、定位符、一句话说明。
4. 逐条验证定位符能在 `CURRENT.md` 里解析到（`ADD` 除外，`ADD` 的定位符必须**不**存在）。解析失败停下问，别猜。
5. 新增页面用六小节模板全量写；修改页面只写 delta，每条注明替换哪一小节。
6. 写 `status: draft`。用户确认后改 `active`。
7. **跑 `sync`**。

## sync

算法与边界条件见 `references/synthesis.md`。要点：

1. 按版本号升序读齐该产品线所有 `status: active` 的 V 文件（`draft` 也纳入，但在 `CURRENT.md` frontmatter 里标 `includes_draft: true` 提醒当前态未定稿）。
2. 以 `V1__baseline.md` 为初始态，逐个 V 应用其变更清单。
3. 写 `CURRENT.md`：generated 警示注释 + frontmatter（`synthesized_from`、`generated`、`generator`）+ 「给 AI 设计工具的上下文块」+ baseline 的七章结构。
4. 每个页面节末尾加一行溯源：`> 来源：V1 → V2（改名）`。
5. 报告：合成了哪些 V、多少页面、多少条变更、有无未解析的定位符。

## check

只读，不改任何文件。逐项报 ✅/⚠️/❌：

| 检查 | 判据 |
|---|---|
| 目录存在 | `products/specs/` 有没有、有没有 V 文件。空则提示先 `init`，**不要报错崩掉** |
| 版本连续 | 版本号无重复、无跳号；文件名 `V{n}__` 与 frontmatter `version` 一致 |
| 快照新鲜 | `CURRENT.md` 的 `synthesized_from` 覆盖了目录里所有 V 文件 |
| 快照未被手改 | `CURRENT.md` mtime 晚于最近一次 `generated`，或 generated 注释/frontmatter 缺失 → 疑似手改 |
| 定位符可解析 | 每个 V 的变更清单定位符在其前序态里存在（`ADD` 反之） |
| 悬空引用 | 被 `REMOVE` 的目标是否仍被后续 V 或流程/术语章节引用 |
| 视觉污染 | 规范正文里出现十六进制色值、`px`、字号、`font-family` → 违反纪律 4 |
| 文案泄漏 | 出现项目 CLAUDE.md 标记为「不得对外」的内部代号 |

发现问题给出**具体修法**，不要只报「有问题」。用户要求修时才动手。

## export --tool \<name\>

按目标工具的方言裁剪 `CURRENT.md`，产出可直接粘贴的 prompt 包。各工具吃什么、不吃什么见 `references/tool-dialects.md`。

产出写到 `products/specs/<产品线>/.export/<tool>-<page-or-all>.md`（`.export/` 是临时产物，建议进 `.gitignore`），并把路径报给用户。

## 与其他 skill 的关系

- 写出来的 Markdown 走 `doc-writing-best-practices`（中西文混排、标题层级、表格取舍）
- 页面交互约定要与 `ui-ux-best-practices` 一致——表单校验时机、弹层状态重置、破坏性操作确认、分页与格式。**冲突时以那个 skill 为准**，规范不该自造一套交互通则
- 视觉层（色值、字体、间距、组件圆角）不归本 skill，归项目的 `DESIGN.md` / `tokens.css`
