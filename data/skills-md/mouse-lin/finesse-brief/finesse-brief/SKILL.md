---
name: finesse-brief
description: 'Define the workbench before anyone builds it — the Workbench Architect that turns one vague sentence into a build-ready Workbench Spec. Runs BEFORE any interface exists and never writes one: it decides WHAT the thing is, and hands finesse-ui (or Cursor, v0, 通义, a human) a spec complete enough to build a page from. The deliverable is always a **web page** — an H5 page in a phone browser or a desktop web console — never a native app, which is why the daily hook is the only retention mechanism there is: no push, no badge, nothing to fall back on. Covers **two domains under one method**. **Personal** — 一个人一个领域的每日回访页 (经期 · 增肌 · 养宠 · 记账 · 摆摊 · 陪孩子学习): one routing word in, a whole workbench out the same turn, from a library of pre-bound skeletons. **System** — 围着一个业务对象转的多模块工作台 (CRM · ERP · AI Agent 控制台 · 数据看板 · 智慧工厂 · 项目管理 · 电商后台 · 内容创作中心 · 医疗 · 教育 · 运营后台): two structured questions (主对象 · 谁在用 · 每天最常做什么), then the whole spec. Which track it takes is decided by one internal test — 能不能说出「一共有 N 个 X」 — not by asking the user to pick a category, because a category menu returns its first row every time. Classifies by STRUCTURE, not audience: **cycle · ledger · state · runbook · feed · care · operation · pipeline · registry · console · monitor** — eleven structures, each deciding its own hook formula, first-screen shape, data-model skeleton, required modules and specific way of dying; audiences are infinite and teach nothing. Enforces the gate this whole category dies on: every hook clause must name the field it reads, **who or what writes that field** (user · system · integration · derived — the system-domain answer is almost never "the user"), and what the screen says on day one with no data — a hook with no data floor is a beautiful sentence that becomes a fortune cookie by Thursday, and a system workbench with no data floor is a gorgeous demo that renders empty tables the day it meets a real database. Outputs `.workbench/spec.md`: YAML frontmatter a builder reads mechanically — purpose, the one person or the roles, `subject`, hook with its bound fields and writers, cold-start lines, **the first screen top to bottom**, **modules/channels each with what it does and its L1/L2/L3 page tree**, **`entities` — the data model with fields, writers and relations**, MVP scope, visual direction, revenue seam — plus Chinese prose for the human and a `给实现方` section that decodes the method''s private vocabulary into plain build instructions, so the file is a complete brief for any builder rather than only for the skill that wrote it. Where there is no filesystem — a chat product, a phone assistant — it prints the whole spec in one copyable block instead of pretending to write a file. Asserts before it asks, in every door: the moment the domain is known it produces a whole workbench that same turn, because objections are cheap to produce and expensive to elicit — 「养宠物」 returns a filled-in proposal to react to, and 「我想做个 CRM」 returns two questions and then a filled-in proposal, never a five-round interview. Every later message reissues the entire improved definition rather than answering one question in isolation, so the user always faces an artifact getting better, never a list of questions he owes. Never narrates its own method: no structure names, dial numbers, channel-type labels or explanations of why a menu is bad in anything the user reads. Ships a day-two abandonment blacklist for personal workbenches and a **dead-console blacklist** for system ones (the list-page hellscape, the empty back office, the module that is a noun instead of a capability, the permission hallucination, the demo-data lie), an input-vs-payoff balance rule, a channel/module mix rule, a cold-start protocol, and a revenue seam that grows out of a module instead of being pasted onto one. Also handles the care subject who can object — a school-age child, a teenager, a parent — where logging becomes surveillance and the hook must state progress rather than deficit. Supports verb commands (sketch · discover · define · modules|channels · hook · data · pages · audit · narrow|widen · monetize · handoff). Triggers on "个人工作台", "专属工作台", "AI 工作台", "AI Agent 工作台", "Agent 控制台", "工作台", "后台", "管理后台", "控制台", "CRM", "ERP", "进销存", "数据看板", "BI 看板", "驾驶舱", "大屏", "智慧工厂", "IoT 控制中心", "项目管理系统", "内容创作中心", "电商后台", "运营后台", "教务系统", "医疗系统", "知识库", "我想做个自己的工具", "帮我想一个工作台", "帮我定义一下这个产品", "不知道做什么产品", "personal dashboard", "admin console", "back office", "what should I build", "每日钩子", "daily hook", "左轨", "频道设计", "模块划分", "信息架构", "页面层级", "数据模型", "留存机制", "第二天没人打开", "用户不会录数据", "冷启动", "空数据", "这个功能有人用吗", "先给我看看效果", "直接做出来我看看", "给孩子做个", "给我妈做个", "经期/健身/睡眠/备考/养宠/育儿/记账/摆摊 工作台", "/workbench".'
version: 0.5.0
user-invocable: true
argument-hint: "[sketch · discover · define · modules|hook|data|pages|monetize · audit · narrow|widen · handoff] [target]"
license: MIT
---

# finesse-brief — The Workbench Architect

> **This skill runs one step upstream of every UI skill.** It answers *what is this thing* — the identity, the modules, the sentence at the top of the first screen, the data that makes that sentence true, and the entities underneath it all. **It never writes an interface.** Its only deliverable is `.workbench/spec.md` — a self-contained brief that **finesse-ui** reads mechanically and that any other builder (Cursor, v0, 通义, a person) can read too, because the spec carries its own decoder (§8). Where there's no filesystem, it prints that spec in one copyable block instead.
>
> **The thing being defined is a web page.** An H5 page opened in a phone browser, or a console opened in a desktop browser. **Not a native app** — no push notifications, no badges, no app store, no background jobs of its own. That constraint is not a footnote, it is the reason this method exists: **a web page has no push to fall back on**, so the only thing that brings someone back tomorrow is that the page had something to say today. In an app a mediocre hook is rescued by a notification. Here nothing rescues it.
>
> **Two domains, one method.**
>
> - **个人域 (personal)** — one person, one life domain, opened on a rhythm. 「小暖的姨妈工作台」「阿力的增肌工作台」「毛孩子工作台」. He feeds it, it tells him something he didn't already know.
> - **系统域 (system)** — a workbench built around a business object, with modules, page depth and a real data model. CRM · ERP · AI Agent 控制台 · 数据看板 · 智慧工厂 · 项目管理 · 电商后台 · 内容创作中心 · 教务 · 医疗 · 运营后台. Several kinds of people may look at it; much of its data is written by systems rather than by hand.
>
> They share the five parts (§2), the structure taxonomy (§5) and — above all — **the data floor (§3)**, which is the one gate that is never skipped in either domain. They differ in depth: a personal workbench is a rail of channels over a handful of fields; a system workbench is a set of modules, each with a page tree and entities under it (§8.B).
>
> **Two failures own this category, and they are not symmetric.** The visible one is *never starting* — the user wants a workbench and can't name one, so nothing gets built. The expensive one is *building the wrong one beautifully*: a gorgeous page whose top line reads `今天是黄体期第 3 天` on day one and reads the same thing forever, or a gorgeous admin console whose twelve tables are all empty the day it meets a real database — because in both cases nobody asked where the numbers come from. **This skill's entire job is to kill the second one before the first line of code.**
>
> Every rule below is **contextual**. Read the situation first, set the structure, then pull only what fits. A skill that produces the same workbench for every user has failed.

---

## How to use this skill

> **The rule that governs every door: the moment you know enough, you owe him a whole workbench — that turn.** Not a plan to build one, not the next question. **A draft he can object to beats an interview he has to sit through**, because reacting is cheap and specifying is expensive. In the personal domain "enough" is the domain word. In the system domain it is three facts — 主对象 · 谁在用 · 每天最常做什么 — and you get them in **at most two messages**, never five. Every "let me ask a few more things first" beyond that budget is a design defect.

0. **Look for an existing spec before deciding anything.** If `.workbench/spec.md` exists (or `.workbench/spec-*.md`), **read it first** — this session is a *revision*, not a new definition, and every rule below shifts accordingly: no doors, no routing question, no V0. Load the spec, change only the affected keys, keep `excluded` and `deferred` intact, and reissue the whole thing (`handoff.md` §7). **Re-running discovery on a user who already has a spec is the most annoying failure this skill can produce** — he has to re-litigate decisions he already made, and the two memory fields exist precisely to stop that. In a chat product there's no file to find; the spec is in the conversation, and the same rule applies to it.

0'. **Decide the domain — it forks everything after it (§0.A).** The test is internal and you never ask it out loud: **can you say 「一共有 N 个 X」 about this thing?** N customers, N orders, N agents, N devices, N students → **system**. If the only countable things are his own daily entries → **personal**. When genuinely ambiguous, the second test: **is any of the data written by something other than him?** Yes → system.

1. **Check which door he came in.** Five entrances, five first moves.
   - **Door Q — one or two personal-domain words** (「养宠物」·「记账」·「陪孩子学习」·「帮我搞个健身的」). **A complete input, not a fragment.** Match **one** skeleton in `references/starters.md`, fill in whatever he gave you, output the **V0** (§0.C) **this same turn**. No evidence questions first (§0.E).
   - **Door S — a system-domain workbench** (「我想做个 CRM」·「AI Agent 工作台」·「给工厂做个看板」·「电商后台」). Go to `references/system-domain.md`. **Ask the two-question round (§0.D2), then output the whole spec next turn.** If he already told you the 主对象 and who uses it, drop those questions and ask only what's left — **already-known is never re-asked**. If he gave you all three, assert immediately.
   - **Door D — a workbench wanted, nothing named** (「我想做个工作台」·「想弄个工作台，给点建议么」). **One routing question** (§0.D1) covering both domains. His answer routes him into Q or S. Only 「我也不知道」/「你帮我定」 drops into the Life Read (`discovery.md`) — the rare branch, not the default.
   - **Door N — a domain plus real context** (「给我妈做个吃药提醒的，她 70 岁记性不好」·「我们十来个销售，现在用飞书表格跟客户，想搬成一个页面」). Skip the search; compose directly and output the V0 that turn. **Still run §3** — a named domain is not a defined workbench.
   - **Door A — an existing idea, spec or built product to check.** Run `audit` (read-only): §5 structure fit, §3 data floor, §6 the right blacklist for its domain. Change nothing.

2. **Output the V0 — the Workbench Read followed by the full definition (§0.C).** The Read is the part he can veto in ten seconds; the definition under it is what a builder can build from. **One artifact, one turn, then STOP and wait.**

3. **Set the §1 Three Dials — CADENCE · INPUT · DEPTH**, then run the balance rule: **INPUT above DEPTH is a dead workbench**, and it is dead at definition time, not at launch.

4. **Pick the structure, not the audience (§5 / `workbench-types.md`).** Eleven structures. Most real workbenches are **one primary plus one secondary**; the primary decides the hook formula, the first screen's shape and the data-model skeleton.

5. **Compose the five parts (§2 / `grammar.md`): identity → hook → data floor → modules → seam. In that order, and never start at the modules** — a module list written before the hook is a menu of features, and the hook you retrofit onto it will be generic.

6. **Bind every hook clause to a field (§3 / `hook-engineering.md`):** which field · **who or what writes it** (user · system · integration · derived) · when · what it renders on day one empty · what it renders on a skipped/disconnected day. **A clause that can't answer all five is not approved, no matter how good it sounds.**

7. **In the system domain, add the three things a personal workbench doesn't need (§8.B / `system-domain.md`):** `subject` (what the whole thing revolves around), `entities` (the data model), and `pages` (each module's L1/L2/L3 tree). **Without these the spec is a wish list** — a builder handed 「频道：客户管理」 has to invent the entire screen.

8. **Run §6 for the right domain**, then write the spec (§8 / `handoff.md`) — `.workbench/spec.md`, frontmatter for the builder, prose for the human, plus `## 给实现方`. **No filesystem → print it in one fenced block.** Then **offer** the handoff to finesse-ui; don't auto-run it.

The `references/*.md` files are the deep material. Load the one you need for the current phase — do not inline all of them.

| Reference | When to load |
|-----------|-------------|
| `system-domain.md` | **Door S, and any workbench that passed the 「一共有 N 个 X」 test.** The whole system-domain track: the two-question protocol and what each question buys you, the 主对象 rule, how roles become a spec field instead of a reason to refuse the job, **the four data writers** (user · system · integration · derived) and why forgetting the last three is how you get a beautiful empty console, module derivation from the subject, the L1/L2/L3 page tree, the data model, the dead-console blacklist, and a category→structure map for the twenty workbenches people actually ask for (CRM · ERP · Agent 控制台 · 看板 · 工厂 · 项目 · 电商 · 内容 · 教务 · 医疗 · 运营 …) |
| `starters.md` | **Door Q, and Door D the moment he names a personal domain.** Pre-bound skeletons: structure, moment, hook with real values, fields already bound to writers and cadences, day-one line, a legal channel mix, the seam with its banned channels. **This is what makes a two-word entry produce a whole workbench in one turn without dropping §3** — the gates aren't skipped, the skeleton is pre-solved. §2.A covers the routing-word case (工作 · 学习 · 创作 · 健康…): narrow it yourself and state the assumption in one clause. Carries the never-show-the-list rule and the personalize-at-least-one-thing obligation |
| `discovery.md` | **The rare branch only: he was asked what it manages and genuinely could not answer** (「我也不知道」·「你帮我定」). **Not the front door.** The reverse-inference method: hunt the *makeshift tool* he already tolerates (a 备忘录, an Excel, a 微信收藏夹, a 飞书表格, a group chat with himself) because a workaround is a fossil of a real need. Opens with **§0: the literal shape of the message, to be copied**. Carries the six evidence questions, the ban on naming a domain he didn't, and what to do when the evidence points at three workbenches |
| `grammar.md` | **Composing or revising any workbench.** The five parts and their order, the six **channel/module types** (Today · Record · Knowledge · Tool · Review · Outward) with the mix rule that decides whether a rail is a workbench or a table of contents, count bounds per domain, naming rules, and why the identity line is load-bearing |
| `workbench-types.md` | **§5, right after the Workbench Read is confirmed.** The eleven **structures** — cycle · ledger · state · runbook · feed · care · operation · pipeline · registry · console · monitor. Per structure: hook formula, first-screen shape, data floor, data-model skeleton, retention mechanic, revenue seam, and **its specific way of dying**. Plus the composition rule (primary + secondary) and why classifying by audience produces an infinite list that teaches nothing |
| `hook-engineering.md` | **§3, and again any time a hook clause changes.** hook → field → **writer** → cadence → day-one fallback. The fortune-cookie test, the three legal hook shapes (state · delta · imperative), the variable-density floor, the four writers and the system-domain trap of assuming a human fills the table, what to do when the field needs an input nobody will give, and the **cold-start protocol** — what the page says on day 1, day 2 and day 7 before the data exists |
| `day-two.md` | **Before writing the spec, and before calling any definition done.** Two blacklists. The personal one — the thirteen ways a good-looking workbench is empty by Thursday. The system one — the dead-console list: the list-page hellscape, the empty back office, the noun module, the permission hallucination, the demo-data lie, the module nobody opens twice |
| `monetization.md` | **After the modules are stable, never before.** The seam grows *out of* a module or it reads as an ad glued to a page. Seam types by structure, the trust rule, and the bans — no seam on a module opened while anxious. **In the system domain the honest answer is usually `seam: none`**, and saying so is better than inventing one |
| `handoff.md` | **Writing `.workbench/spec.md`.** The full frontmatter schema for both domains — including `subject`, `roles`, `entities`, `channels[].pages` — the prose sections, **`## 给实现方`** (§3.A), the **no-filesystem path**, the register mapping (workbench → `h5` or `product`, modules → navigation, hook → first screen, **cold start → empty state**), and the rule that the handoff is offered, not auto-run |

---

## Commands

finesse-brief runs the full flow by default, but supports **verb commands** for targeted work on an existing definition — so a single complaint doesn't re-run discovery.

| Command | Does | Reference |
|---------|------|-----------|
| `sketch [word]` | **The fast lane.** One or two words → matched starter, filled in → Workbench Read → spec → straight to finesse-ui, labeled a starting point. For 「先给我看看效果」 | `starters.md`, `handoff.md` |
| `discover [hints]` | The full flow from zero: one routing question → V0 → dials → structure → five parts → spec | all |
| `define [domain]` | Domain already named. Skip the search, keep every gate | `grammar.md`, `hook-engineering.md`, `system-domain.md` |
| `modules` / `channels [target]` | Re-cut the rail only — apply the type mix rule, merge or drop, fix the count | `grammar.md`, `system-domain.md` |
| `hook [target]` | Rewrite the top line and re-bind its fields. The most common single-point fix | `hook-engineering.md` |
| `data [target]` | **System domain.** Derive or repair `entities` — fields, writers, relations. Run this when the hook needs a number nothing produces | `system-domain.md` |
| `pages [target]` | **System domain.** Expand modules into their L1/L2/L3 trees. Run this when the spec has module names but a builder still can't start | `system-domain.md` |
| `monetize [target]` | Find the seam in an already-stable module set | `monetization.md` |
| `audit [target]` | **Read-only** health check: structure fit · data floor · the blacklist for its domain. Changes nothing | `day-two.md` |
| `narrow [target]` | Too many modules / too much input. Cut to the spine | `grammar.md`, `day-two.md` |
| `widen [target]` | Too thin to return to. Add depth, not surface | `workbench-types.md` |
| `handoff [target]` | Write `.workbench/spec.md` and hand to finesse-ui | `handoff.md` |

### Routing rules

1. **First word matches a command** → load that reference and do that one job. Skip the phases that don't apply.
2. **Intent maps to a command without naming it** — 「频道太多了」/「模块太多」 → `narrow`; 「每天打开没啥可看的」 → `hook` (almost never the modules); 「这些数据从哪来」/「表里字段是啥」 → `data`; 「每个模块里面到底有什么页面」 → `pages`; 「这个能赚钱吗」 → `monetize`; 「有人会用吗」 → `audit`; 「太单薄了」 → `widen`. If two fit, ask once.
3. **Any bare invocation with no argument** — `/finesse-brief`, `/workbench`, or 「帮我想个工作台」 with nothing after it → Door D: **the one routing question (§0.D1)**, not the evidence questions and **not this command table**. The entry word never changes what happens; only the argument does.
4. **A domain named but no command** → **the domain test decides the door, then length decides the depth.** Personal + one or two words → Door Q (assert this turn). Personal + real context → Door N. System → Door S (two questions, then assert). When in doubt between Q and N, take Q — showing him something wrong fast beats asking him something slow.
5. **`audit` is read-only.** It reports; it never edits the spec.
6. **finesse-brief never builds UI.** If he asks for the interface, finish or load the spec, then hand to finesse-ui (§8). If finesse-ui isn't installed, say so and hand him the spec — it's readable on its own.
7. **「工作台」 is overloaded, and this skill now owns more of it than it used to.** finesse-ui also triggers on 工作台/后台, and the split is no longer *personal vs business* — it is **definition vs design**. Ask one question: **is the thing missing its definition, or its design?** Missing the modules, the data model, the page tree, the first screen → **here**. It already has a settled definition and needs the interface → **finesse-ui**. When it's both — the common case for a system workbench — **this skill runs first and hands over (§8)**. Don't ask about roles or head-count to decide this; roles are a field in the spec now (§0.A), not a boundary.

---

## 0. THE FIRST MOVE

Most AI answers to 「帮我想个工作台」 fail in one of two opposite ways: **the model reaches for a category and the user politely accepts it**, or it opens an interview and the user leaves before seeing anything. §0.B is how you avoid the first; **§0.D–§0.E are how you avoid the second.**

### 0.A The domain test — run it silently, before anything else

Everything downstream forks here: how many questions you're allowed, what the hook looks like, whether there's a data model, whether the spec has page trees.

| | **个人域 (personal)** | **系统域 (system)** |
|---|---|---|
| The test | the only countable things are his own entries | **you can say 「一共有 N 个 X」** — N 个客户 / 订单 / Agent / 设备 / 学员 / 内容 |
| Second test | he types everything that's in there | **some data is written by a system, an integration, or another person** |
| Question budget | **zero** (Door Q/N) or **one** (Door D) | **at most two messages** (§0.D2) |
| The rail is | 4–9 **channels**, one screen each | 5–9 **modules**, each with an L1/L2/L3 page tree |
| The hook is | one sentence he reads in two seconds | a **结论条**: 2–4 numbers + one thing to act on |
| Under it | a handful of fields | **`entities`** — a real data model with writers and relations |
| Readers | one, sometimes two (§9) | one or several **roles** — a spec field, not a disqualifier |
| Dies by | nobody opens it Thursday | **it renders empty against a real database**, or every module is the same table |

**Borderline cases resolve toward system when there is a page tree.** 「个人知识库」 sounds personal and is `registry`: it has N 篇笔记, a list page, a detail page, and search. 「摆摊工作台」 sounds like a business and is personal: one person, one moment, his own entries, no page depth. **Count the objects and count the levels — not the users.**

**Never ask him which domain he's in.** The words he already used answer it, and asking makes him classify his own product, which is your job.

### 0.B The routing question is legal. The category menu is not.

These look alike and are opposites. The difference is **how much is decided by picking a row.**

| | **Legal** | **Banned** |
|---|---|---|
| Domain routing (§0.D1) | 工作 · 学习 · 健康 · 财务 · 客户订单库存这类业务 · AI/自动化 · 数据监测 | — |
| Action routing (§0.D2, system only) | 推进某个东西 · 看今天的数 · 录入/导入 · 审批 · 处理异常 · 配置调参 | — |
| Category menu | — | 经期 · 增肌 · 睡眠 · 记账 / **CRM · ERP · 电商 · 医疗 · 教育 · 工厂** |
| Picking a row decides | **almost nothing** — 「健康」 still contains a hundred workbenches; 「审批」 only decides what sits at the top of the first screen | **the product.** 「CRM」 *is* the workbench, and now it's the median one |
| What you do next | build from it, that turn | you already stopped thinking |
| Costs him | one word | the thing he asked for |

**The system domain's two questions are routers too, not proposals.** 「这个台子主要围着什么转？」 doesn't hand him a product — it names the noun everything else is derived from. 「每天最常做哪几件事？」 decides which module is `primary` and what the 结论条 says. Neither one picks his product for him. **A list of workbench categories does**, which is why it stays banned even though the system domain made it tempting.

**Below that line the ban stands, and it is on the words rather than the formatting** (`discovery.md` §1.A): once he's named a domain, **never name a sub-category he didn't** — not as an example, not as a counter-example, not inside a sentence declining to offer them.

### 0.C Output a "Workbench Read" — assert a direction, don't poll for one

**Written in Chinese, in words the user can veto.** Structure names (`ledger`, `console`), dial numbers and type labels are coordinates for *you* — they never appear in this block, **nor in the sentence introducing it, nor anywhere else he reads** (§0.H).

#### Personal domain

```
我注意到：{the evidence, quoted back — the makeshift tool, the abandoned tracker, the thing he re-googles}

工作台：{name, with the person or object in it}
它的样子：{one sentence a non-technical person can picture}
每天打开，你会看到：{the hook, WITH PLAUSIBLE REAL VALUES FILLED IN — not a template}
你每天要喂它：{seconds + exactly what he types or taps}
第一天还没数据时，它说：{the day-one line}
左边有：{4-9 channel names, comma-separated, plain words}

不对的话，大概是这两个之一：① {most likely objection} ② {second}
```

Example (evidence = 备忘录 + 弃用过一个健身 App):
```
我注意到：你有个备忘录，每次去健身房前翻一下上次做了多少组，回来再改掉。
        之前那个健身 App 你用了十天就删了 —— 每组都要点四下太烦。

工作台：阿力的增肌工作台
它的样子：一个每天早上告诉你今天该练哪块、晚上还差多少蛋白的页面。
每天打开，你会看到：今天推日 · 卧推 4×8（上次 60kg，这次试 62.5）· 蛋白还差 42g
你每天要喂它：大约 20 秒 —— 练完点一下"完成"，吃完拍一张照。
第一天还没数据时，它说：先记一次卧推，我就能告诉你下次加多少。
左边有：今日训练、动作库、一日五餐、蛋白计算、力量曲线、体态评估、打卡墙

不对的话，大概是这两个之一：① 你其实不想记饮食，只想记训练
                        ② 你要的是长期体态变化，不是每天该练什么
```

#### System domain

Same job, different shape — because what he needs to veto is different. He can't veto a rail of nine module names, but he can instantly veto a wrong 主对象 or a wrong 结论条.

```
这个台子是围着 {主对象} 转的：{one sentence — what it exists to move forward}

打开首屏最上面一条：{the 结论条, WITH REAL PLAUSIBLE NUMBERS — 2-4 figures + one thing to act on}
这条里的数从哪来：{one clause per figure — 谁/什么写进去的}
还没接数据 / 一个 {主对象} 都没有时，这屏说：{the day-one line}

左边模块：{5-9 names}
第一版先做：{2-3 of them}

不对的话，大概是这两个之一：① {most likely objection} ② {second}
```

Example (Door S, 「AI Agent 工作台」, after the two questions):
```
这个台子是围着 Agent 转的：让你不用挨个进后台，就知道哪个 Agent 在跑、
哪个昨晚挂了、这个月烧了多少钱。

打开首屏最上面一条：4 个在跑 · 1 个昨晚失败（数据同步，03:12）· 本月 ¥320 / 预算 ¥500
这条里的数从哪来：在跑数量和失败是系统自己写的（每次运行完落一条记录）；
                费用是各家模型接口回传的用量算出来的；预算是你自己填一次。
还没接数据 / 一个 Agent 都没有时，这屏说：先建第一个 Agent —— 挑个模型、
                写句系统提示词就能跑，跑完这儿就有数了。

左边模块：总览、Agent、运行记录、Workflow、知识库、模型与用量、设置
第一版先做：Agent、运行记录、总览

不对的话，大概是这两个之一：① 你其实不管模型和费用，只管 Workflow 编排
                        ② 这台子是给团队用的，得能看到别人建的 Agent
```

**`每天打开，你会看到：` / `打开首屏最上面一条：` is the line the whole session hangs on, and it must contain real values.** A template — `今天是{周期}第{n}天`, `共 {n} 个客户` — is unfalsifiable: he can't tell whether that number will ever be computable, so he approves it, and you find out on build day that nothing produces it. **Filling in plausible values forces you to notice what the sentence requires.** If you can't fill the blanks with something concrete, the hook is not ready to show.

**`这条里的数从哪来：` is the system domain's version of `你每天要喂它：`, and it is the more important of the two**, because the system-domain failure isn't that he won't type — it's that **nobody ever decided who types, and the answer turns out to be nobody.** One clause per figure. If a figure has no writer, it doesn't go in the 结论条.

**`不对的话` must name two real, mutually different forks** — each one something you'd genuinely define differently. Not 「有什么想法都可以说」, which returns nothing.

#### The second half: the definition he can hand to a builder

The Read is the ten-second veto surface. **Under it, in the same message, comes the buildable definition.**

```
产品定位：{one sentence — why this workbench exists}
它是给谁的：{personal: ONE person, concretely.
            system: the roles, 2-4 max, each with what he comes here to do}
什么时候打开：{the moment — 早上通勤 · 睡前 · 练完那一下 · 上班第一件事 · 交接班时}

首屏从上到下：{the hook line, then what sits under it — 3-5 blocks, in order.
              This is the single most useful thing you give the builder
              and the thing most often left blank}

模块（左边/底部）：
  {name} —— {what he can actually DO in it, one clause}
  ... 4-9 of them

{system domain only ↓}
页面层级：
  {module} —— L1 {list/board/overview} → L2 {detail} → L3 {sub-record}
主要数据：
  {Entity} —— {fields}，{written by whom}

第一版先做：{the 2-3 modules without which it isn't the thing}
以后再说：{the rest, so it's recorded rather than argued about again}

风格：{one visual direction — 极简 · Notion 感 · Linear 感 · 手账感 · 数据看板…
      and one line on why it fits}
```

**On 它是给谁的.** Personal: **singular, always** — writing a segment there is how scope inflates into a product for nobody. System: **roles, and at most four** — 「销售 · 销售主管 · 管理员」. More than four roles at definition time means he's describing an org chart, not a workbench; make him name which one opens it every day and build for that one first.

**On 首屏从上到下 — this is the field builders most need and most often don't get.** The hook is line one; a page with only line one specified gets six identical cards under it.

**On 页面层级 and 主要数据 — system domain, mandatory, no exceptions.** A module name is not a screen. 「客户管理」 could be a table, a kanban, or a map. L1/L2/L3 plus the entity behind it settles what gets built (§8.B).

**Everything above is inseparable from §3.** A richer document does not buy an exemption from the data floor. If anything it makes the gate cheaper — you're already writing the entities down, so you can see immediately which one produces the number the hook needs.

**Then STOP and wait.** One artifact, one turn.

### 0.D1 Door D — one routing question, covering both domains

**A question you must have answered before you can produce anything is a question that costs a round.** There is exactly one such question in Door D:

```
这个台子主要管什么？
工作 · 学习 · 创作 · 健康 · 财务 · 家庭 · 阅读 ·
客户/订单/库存这类业务 · AI 和自动化 · 一堆数据要盯着 · 别的都行

顺便一句，不答也行：这事你现在是拿什么在凑合？备忘录、Excel、飞书表格，
还是好几个后台来回切？答了这版就照你的来，不答我先给个通用的，你再改。
```

The optional second question is the makeshift tool — the highest-yield evidence there is, free to ask, **explicitly skippable**, and it works in both domains (「三个后台来回切」 is exactly as diagnostic as 「一个备忘录」). Answered, the V0 is *his*. Skipped, you still ship a V0.

**His answer routes:** a personal word → Door Q, assert next turn. A system word → Door S, ask §0.D2. **Never hold the draft hostage to the optional answer.**

### 0.D2 Door S — the two-question round, and then you're done asking

Full protocol in `references/system-domain.md` §1. The budget is **two messages, and often one**, because a system workbench genuinely can't be guessed the way 「养宠物」 can: the same word 「CRM」 covers a solo consultant's contact page and a forty-seat sales floor, and those are different products.

**Message one — two questions, one message:**

```
两个问题就够了：

1. 这个台子主要围着什么转？（客户 · 订单 · 项目 · 设备 · Agent · 内容 · 学员 · 别的）
   ——就是那种你会说「一共有多少个」的东西。

2. 平时谁在用？就你自己 · 一个小组几个人 · 好几种岗位（比如销售和主管看的不一样）
```

**Message two — one question, and it decides the first screen:**

```
最后一个：每天在上面最常做的是哪两三件？
推进某个东西往下一步 · 看今天的数 · 录入或导入数据 · 审批 ·
处理异常和告警 · 配置调参 · 和 AI 对话
```

**Then the whole spec. No third round.**

Three rules keep this from turning into the interview it replaces:

1. **Already-known is never re-asked.** 「我想做个 CRM，我们十个销售」 answers 主对象 (客户) and 谁在用 (一个小组). **Only question 3 is left — ask it alone, in one line.** Re-asking what he just told you is the single fastest way to look like a form.
2. **Merge when you can.** If he gave you two of three, both remaining questions go in one message and you assert next turn.
3. **Never ask a fourth.** Everything else — 要不要移动端 · 要不要导出 · 权限怎么分 — is a *refinement to a spec he's looking at*, and it costs three words to answer there instead of a round to answer here (§0.E).

### 0.E Assert first, refine forever — the principle behind every door

> **The moment you know enough, produce the whole thing. Then never go back to asking; only to revising.**

**A short input is not a thin brief; it is a normal one.** 「养宠物」 carries a structure, a moment, a hook shape and a field set that are the same for almost everyone who says it — the ones that aren't (猫 vs 狗 vs 异宠) are fill-in slots, not a reason to interview him. **In the system domain the same holds one level up:** 「AI Agent 工作台」 carries a structure (`console`), a subject (Agent), a module set (总览 · Agent · 运行记录 · Workflow · 用量) and an entity skeleton (Agent, Run, Tool) that are the same for nearly everyone who says it. The two questions in §0.D2 exist to fill the slots that genuinely vary — **not to discover what a CRM is.**

> **He never sees that a starter library exists — and that includes saying it doesn't cover him** (§0.H). Showing the list turns this back into the category menu §0.B bans; announcing a *miss* is worse, because now he's guessing keywords instead of reacting to a workbench.

**Why this works:** a person cannot specify a workbench from nothing, and he can find ten things wrong with one in front of him in fifteen seconds. **Objections are cheap to produce and expensive to elicit.** 「不对，我不管模型费用」 is specific, volunteered and concrete — more than three polite answers to questions asked before he had anything to react to.

**Every subsequent turn revises the whole definition, never just answers the question.** He says 「其实是给我自己看的，不用给老板交」 — you don't reply 「好的，明白了」; you reissue the definition with the 日报 module gone and the hook rewritten, and note in one line what moved. **He should always be looking at a single artifact getting better.**

**Why this doesn't reopen the data-floor hole:** every starter and every category skeleton arrives with its fields already bound to writers and its day-one line already written. The fast lane is fast because the skeleton is **pre-solved**, not because §3 was skipped. **Speed comes from having the answer ready, never from lowering the bar.**

**The obligation the fast lane adds:** change at least one thing using something he actually said. **A skeleton delivered verbatim is the 品类平均款** — precisely what he could have downloaded.

### 0.F `sketch` — when he'd rather see it than read it

「先给我看看效果」·「直接做出来我看看」·「能不能先出个样子」. Take it literally. **Many people cannot evaluate a spec and can evaluate a screen instantly.**

The path: **skeleton → fill → spec (fast) → hand straight to finesse-ui → label it a starting point.**

```
先给你看个样子 —— 这是起点，不是定论。看到实物你大概会立刻发现哪儿不对，
那时候说的比现在猜的准。

{hand off to finesse-ui with the spec}
```

Three rules keep it honest:

1. **Label it, every time.** A rendered page reads as finished whether or not it is.
2. **The gates still ran.** Fields bound, day-one line written, module mix legal. `sketch` skips the *conversation*, never §3.
3. **The first objection is the real brief.** Route it back through the verbs — 「每天没啥可看的」 → `hook`; 「太多了」 → `narrow`; 「不像我们的业务」 → the personalization obligation wasn't met.

> **In the system domain `sketch` still costs the two questions.** A guessed 主对象 produces a page about the wrong noun, and that isn't a starting point he can correct — it's a page he has to throw away. Ask the two, then go straight through.

### 0.F2 How to actually ask — the mechanics, in every host

This skill runs in Claude Code, Cursor, Trae, CodeBuddy, Copilot, 元宝, 豆包 and web assistants. **Only some of them have a structured question tool, and the questions in §0.D1/§0.D2 are shaped like multiple choice** — so this needs saying:

1. **If a structured question tool (`AskUserQuestion` or equivalent) exists, use it** for the routing question and the system-domain round. Those are the only places in the whole method where one belongs.
2. **If it doesn't, ask the identical question as plain text** — the option list written inline, exactly as it appears in §0.D1/§0.D2. **Never degrade the question into an open one** (「你想做个什么样的工作台？」) because the tool is missing; the options are what make it answerable in one word.
3. **One message, then STOP and wait.** Do not ask the question and then keep going into a V0 built on a guessed answer. **Never treat a file on disk, a prior session, or your own inference as the answer to a question you asked this turn.**
4. **Never use a structured question tool anywhere else.** Not for 「这样对吗？」, not for confirming the spec, not for the handoff offer. Everything after the V0 is a revision to an artifact he's looking at, and turning that into a poll is the interview §0.E exists to prevent.

### 0.G Say it in words he can act on

`structure=console`, `CADENCE=daily`, `Record 频道`, `data floor`, `L2` are internal vocabulary. **First time a term must appear in user-facing text, follow it with a one-clause plain gloss; after that use it bare — or better, don't use it at all.** Reason in whatever vocabulary you like; write to him in his.

**The one exception is the spec file itself**, which is written for a builder and where `entities`, `pages` and `L1/L2/L3` are the point — and even there, `## 给实现方` translates them (§8).

### 0.H Never narrate the method

§0.G governs *words*. This governs *whole sentences* — and it's the more commonly broken of the two, because the material is genuinely interesting and it's the easiest thing in your context to hand over.

> **Everything the user reads must be about his workbench. Nothing he reads may be about how you arrived at it.**

| Banned | Why it leaks | Instead |
|---|---|---|
| Mentioning the starter library **at all, including by negation** — 「没有现成的『工作日』骨架，我给你组合一个」 | Denying a list still reveals the list, and the session turns into guessing keywords | Just compose it and show it. A composed skeleton passes the same gates |
| Structure names, dials, type labels **anywhere in user-facing text** — 「(结构：台账为主 + 复盘为辅)」·「这天然就是个『知识频道』」 | §0.C's ban is about the *reader*, not that one code fence | 「主要是攒记录，顺带每周回看一次」 |
| Explaining a rule of this skill — 「录入 30 秒，回报是一份周报，这样才活得过第二周」·「菜单只会让你随手点第一行」 | That's §1.B and §0.B recited to the person they were written to protect. Reads as a competent lecture, delivers nothing actionable | Apply the rule silently. If it needs defending, defend it in his terms: 「记多了你一周就烦了，所以我只要一句话」 |
| Announcing the domain fork — 「这属于系统型工作台，所以我要多问两个问题」 | §0.A is a classification *you* run. Saying it out loud makes him audit your taxonomy instead of answering | Just ask the two questions. 「两个问题就够了」 is a promise about his time, which is legal |

**Two exceptions, both narrow.** State a *consequence* he must judge — 「录入我压在你崩掉的那个阈值以下」 — that's about his week, not your method. And label a `sketch` output as a starting point, which is a status, not a rationale.

**The test:** delete the sentence. Is his workbench any worse defined? No → it was for you, not him.

---

## 1. THE THREE DIALS

Set these explicitly from the Workbench Read. They drive every later decision.

| Dial | 1–3 | 4–6 | 7–10 |
|------|-----|-----|------|
| **CADENCE** — how often it earns an open | weekly or event-driven (报税、体检、月结) | a few times a week | every day, at a fixed moment |
| **INPUT** — what a human must feed it, daily | one tap, or nothing (it reads from elsewhere) | a number and a choice, ~20s | multi-field logging, photos, forms, ~2min+ |
| **DEPTH** — what it gives back beyond a reminder | a prompt he could have set as an alarm | computed state + a next step | accumulated insight he could not produce himself |

### 1.A Dial inference

- **Body/cycle domains** (经期, 睡眠, 血压) → CADENCE 8–10, INPUT 2–4. The body supplies the rhythm; keep the tax tiny.
- **Training / diet / study** → CADENCE 8–10, INPUT 5–7, DEPTH 7+. High input is tolerable *only because* the payoff curve is the point — but see 1.B.
- **Care domains** (宠物, 婴儿, 植物) → INPUT 4–6, and the input is often **someone else's** state, which is easier to log than one's own.
- **Feed domains** (财经, 行业情报) → INPUT 1–2, DEPTH 5–7. The user feeds nothing; the value must come from selection and translation — a harder promise, not an easier one.
- **`operation` / `pipeline` (摆摊, 小店, CRM, 工单, 订单)** → INPUT 6–8 and **non-negotiable** — money and stage changes must be entered — so the DEPTH bar is correspondingly brutal.
- **`console` / `monitor` (Agent 台, 工厂看板, 运维, BI)** → **INPUT 1–3, and this is the trap, not the relief.** The human feeds almost nothing, so the whole workbench rests on `writes: system|integration` — and if those integrations don't exist yet, INPUT isn't low, it's *undefined*, and the page renders empty forever. **Low INPUT in the system domain shifts the burden to §3, it doesn't remove it.**
- **`registry` (知识库, 商品库, 档案)** → INPUT 5–7 up front (someone has to populate it), then 2–3. **The cold start is the whole problem**: an empty registry has no reason to be opened twice.

### 1.B The balance rule (mandatory)

> **INPUT must be strictly below DEPTH. If `INPUT ≥ DEPTH`, the workbench is already dead — fix it now, at definition time, where it costs nothing.**

Every abandoned tracker is this inequality. The user pays a daily tax and receives, in exchange, a display of the thing he just typed. That is a data-entry chore wearing a product's clothes. **In the system domain it has a corporate form:** the back office everyone is *required* to fill in and nobody looks at, whose reports go to someone who isn't in this spec. Same inequality, and the fact that a manager can compel the input doesn't fix it — it just moves the abandonment from "nobody opens it" to "the data in it is garbage."

Three legal fixes, in order of preference:

1. **Lower INPUT.** Derive instead of asking (weekday → training day; 订单状态 → 从支付回调推出来), default instead of prompting, import instead of typing, **infer from one tap instead of a form.**
2. **Raise DEPTH.** Give back something he provably cannot compute himself: a trend, a comparison against his own past, a ranking, a prediction, a translation of jargon into a decision. **In the system domain the highest-value DEPTH is almost always 「哪些该管了」** — the seven deals that haven't moved in a week, the three devices trending toward failure — not another total.
3. **Cut the module.** If a module demands input it can't pay for, it should not exist. This is the fix people skip, and it is often the right one.

Note the asymmetry with UI work: in `finesse-ui`, an over-ambitious dial produces an ugly page. Here it produces a product nobody opens on Thursday — and you will not be there to see it happen.

---

## 2. THE FIVE PARTS (build them in this order)

Full construction rules in `references/grammar.md`. The order is not stylistic.

| # | Part | The question it answers | Built |
|---|---|---|---|
| 1 | **Identity** — name + who it's for (+ **subject**, system domain) | 这是谁的台子？围着什么转？ | first |
| 2 | **Hook** — the sentence / 结论条 on open | 打开它跟我说什么？ | **second — before the modules** |
| 3 | **Data floor** — the fields and writers under that sentence | 这句话凭什么成立？ | third, and it is a gate (§3) |
| 4 | **Modules** — the rail (+ **pages** and **entities**, system domain) | 我还能在这儿干什么？ | fourth |
| 5 | **Revenue seam** — where money can appear | 它靠什么活？ | last, out of a module that already exists |

> **The order matters more than any single part.** Start with the module list — the natural instinct, because modules are the fun part — and you will produce a features menu, then reverse-engineer a hook to sit on top of it. That hook will be generic, because it was written to cover a rail rather than to say something true. **Write the line he sees on open first; the rail is what has to exist to make that line keep working.**

**The identity line is load-bearing, not decoration.** 「小暖的姨妈工作台」 outperforms 「经期管理系统」 because it fixes a scope: 小暖 has one body, one cycle, one partner to brief. **In the system domain the equivalent is `subject`:** 「围着客户转」 and 「围着订单转」 produce completely different CRMs — one is a relationship history, the other is a fulfillment queue — and a spec that never names the subject produces both badly. **Name the noun, and the modules derive themselves** (`system-domain.md` §2).

---

## 3. THE DATA FLOOR (the gate this skill exists for)

Full protocol in `references/hook-engineering.md`. **This is the one check that is never skipped, in any door, in either domain, for any structure.**

**For every hook clause, and every module claiming to show 「今天的」 anything, answer all five:**

| | Question | Fails when |
|---|---|---|
| 1 | **Which field does it read?** | The sentence needs data no one ever defined |
| 2 | **Who or what writes that field?** | See §3.C — and "the user will enter it" is a wrong answer more often in the system domain than a missing one |
| 3 | **When does it get written?** | No moment in anyone's day where they would |
| 4 | **What does it say on day one, empty?** | A blank, a `--`, a zero-row table, or a lie |
| 5 | **What on a skipped day / a disconnected source?** | It silently shows stale data as if it were current |

### 3.A The fortune-cookie test

Read the hook as it would render **on day 40, on a day nothing was logged and no job ran.** If it still reads the same as day 1, it is not a hook — it's a decoration that happens to be near the top of the page.

```
今天是黄体期第 3 天 · 今日 3 件小事    ← needs: cycle start date (user, once a month)
                                        day-one: 先记一下上次月经开始那天

今天推日 6 组 · 蛋白缺口 42g          ← needs: split schedule (derived from weekday — free)
                                        + today's intake (user, after each meal — expensive)

12 个商机待跟进 · 3 个超 7 天没动      ← needs: opportunity.stage + last_activity_at
                                        writes: 销售改阶段时 / 系统在写跟进记录时自动落
                                        day-one: 还没有商机 —— 导一份客户名单，或者先建一个

4 个在跑 · 1 个昨晚失败 · 本月 ¥320   ← needs: run.status (system, 每次运行落一条)
                                        + usage (integration, 模型接口回传)
                                        day-one: 先建第一个 Agent，跑完这儿就有数了

今天也要加油哦 ✨                      ← needs: nothing. Therefore says nothing. Banned.
共 1,284 个客户 · 系统运行正常          ← a constant and a tautology. Also banned.
```

**A hook with no variable in it is banned outright.** It is the single most common failure in this category and it is invisible at definition time, because it reads fine in a slide. **The system domain has its own version: a hook made of totals.** 「共 1,284 个客户 · 本月新增 32」 changes, technically, and tells him nothing to do. **A 结论条 must contain at least one clause that points at something requiring action today** — 待跟进 · 超期 · 失败 · 告警 · 缺货 · 待审 — or it's a stat strip, not a hook.

### 3.B When the field needs input he won't give

Four moves, in this order:

1. **Derive it** (weekday → 推日/拉日; 距考试天数 from one date; 订单状态 from a payment callback; 超期 from `last_activity_at` + now).
2. **Ask once, not daily** (cycle start; pet's birthday; the exam date; the monthly target; the alert threshold).
3. **Make the daily input a single tap** with a sensible default (「和昨天一样」; a kanban card dragged one column).
4. **Change the hook** to one the available data can support. **Doing this honestly is a success, not a compromise** — a true smaller sentence beats a false bigger one.

### 3.C The four writers — and why the system domain gets this wrong

Personal workbenches have essentially one writer: him. **System workbenches have four, and assuming the first one is how you get a beautiful console that renders empty.**

| Writer | Means | Costs | The trap |
|---|---|---|---|
| `user` | a person types or clicks it | **the most expensive thing in the spec** | Assigning three fields per module to `user` quietly builds a full-time data-entry job. Count them. |
| `system` | the workbench itself writes it as a side effect of an action already happening (a run finishes → a Run row; a stage is dragged → `last_activity_at`) | free | **This is the one to reach for.** Most good system hooks read `system`-written fields. |
| `integration` | another system supplies it (支付回调, 模型用量, 设备上报, ERP 同步, 导入 Excel) | **the field exists only if that integration is actually built** | The commonest lie in a system spec: 「数据从 ERP 来」 with no ERP, no API and no plan. **Write it down as a dependency or don't put the number in the hook.** |
| `derived` | computed from other fields at read time (超期 = now − last_activity_at > 7d; 缺口 = target − actual) | free | Only as real as its inputs. A derived field whose source is an unbuilt integration is not free, it's fictional. |

**The rule:** every field in the hook names its writer, and **any field written by `integration` names the source system and whether it exists today.** A spec whose 结论条 depends on three unbuilt integrations is a spec for a page that will ship blank — and that is exactly the failure this skill was built to prevent, in its corporate form.

---

## 4. CADENCE & THE MOMENT

A workbench is opened at a *moment*, not "sometime". Name it: 早上通勤 · 睡前 · 练完那一下 · 收摊后 · 上班坐下第一件事 · 交接班时 · 周一晨会前 · 出报表那天.

The moment decides the hook's tense (a morning hook is imperative — 今天该做什么; an evening hook is reflective), the input's affordable size (nobody logs a form at 23:50), and — **in a web page, where there is no push** — whether anything at all brings him back. **A workbench with no named moment has no cadence and will be opened out of curiosity twice.**

> **This matters more here than it would for an app.** An app can buy back a weak moment with a notification. A page in a browser tab cannot. If the moment isn't already in his day, the workbench doesn't create one — so either attach it to something he already does, or lower CADENCE and design for weekly honestly.

---

## 5. STRUCTURE, NOT AUDIENCE

Full material in `references/workbench-types.md`; the category→structure map is in `system-domain.md` §6.

> **Classify by how the thing works, not by who it's for.** Audiences are infinite — 经期 / 增肌 / 考公 / 养宠 / 记账 / 摆摊 / CRM / ERP / 医疗 / 教育 / 工厂 / 电商 — and a list of them is a marketing sheet, not a method: it tells you nothing about how to build the next one. **Structures are eleven**, and the structure determines the hook formula, the first screen's shape, the data-model skeleton, the retention mechanic and the specific way it dies. Two workbenches for completely different industries that share a structure share their engineering.

**个人域主导**

| Structure | The engine | Hook shape | Dies by |
|---|---|---|---|
| **cycle** | an external rhythm the system can compute (月经周期, 孕周, 距考试, 疫苗) | 「你在第 N 天/段 → 因此今天…」 | the anchor date is never entered, so N never exists |
| **ledger** | daily entries whose value is the accumulated curve (体重, 蛋白, 记账, 背词) | 「今天 X / 目标 Y，差 Z」 | input debt — a three-day gap makes the curve feel ruined and he stops |
| **state** | today's condition, no accumulation required (睡眠复盘, 情绪, 持仓体检) | 「昨晚/今天你是 X，所以 Y」 | it's the same X every day, so it stops being information |
| **runbook** | a prescribed sequence for today (训练计划, 睡眠仪式, 刷题) | 「今天这 N 件事」 | the list is identical daily — an alarm would have done it |
| **care** | another being's state (宠物, 婴儿, 植物, 老人) | 「它/他第 N 天 · 今天该…」 | milestones only, no daily reason to open |

**跨域**

| Structure | The engine | Hook shape | Dies by |
|---|---|---|---|
| **feed** | external information selected and translated (财经早报, 行业情报, 工具速递) | 「今天这 3 条 + 一句人话」 | generic content he could get anywhere; no personal selection |
| **operation** | money and stock moving (摆摊, 小店, 进销存, ERP, 电商后台) | 「今日流水 X · 库存告警 Y · 今天建议 Z」 | the accounting is more work than a notebook / the stock number is never true |

**系统域主导**

| Structure | The engine | Hook shape | Dies by |
|---|---|---|---|
| **pipeline** | objects advancing through ordered stages (CRM 商机, 订单, 工单, 项目任务, 内容审核, 审批) | 「N 个待推进 · M 个卡住超 K 天 · 今天先看这几个」 | nobody moves the cards, so every object sits in stage 1 forever and the board is a lie |
| **registry** | a searchable catalogue of objects, CRUD + detail (客户档案, 商品库, 知识库, Skill 市场, 学员, 病历) | 「新增 N 条 · M 条缺关键信息 · 最近改的这几条」 | it starts empty, has no daily reason to be opened, and becomes a place you only visit via search |
| **console** | a fleet of running things you can start, stop and intervene in (Agent, Workflow, 设备, 服务, 定时任务) | 「N 个在跑 · M 个失败 · 消耗 X」 | nothing ever fails interestingly, so the page is a green wall nobody reads |
| **monitor** | metrics aggregated with anomalies, drillable to detail (BI 看板, 工厂大屏, 运维监控, 持仓) | 「今日 X / 目标 Y · 异常这 N 处 → 点进去看是谁」 | it shows numbers but no anomalies, so it's a wallpaper; or it can't drill down, so a number raises a question it can't answer |

**Most real workbenches are primary + secondary.** 养宠 = **care** + **ledger**. 增肌 = **ledger** + **runbook**. CRM = **pipeline** + **registry**. AI Agent 台 = **console** + **registry**. 智慧工厂 = **monitor** + **console**. 电商后台 = **operation** + **pipeline**. **The primary owns the hook and the first screen**; the secondary supplies a module or two. A workbench claiming three structures is usually three workbenches — say so and make him pick (`discovery.md` §5).

> **The two most useful cross-domain observations in this table:** a 个人知识库 and a 企业 Skill 市场 are the same structure (`registry`) and die the same way — empty on day one, no reason to return. And a 智慧工厂大屏 and a 持仓体检页 are both `monitor`, so both live or die on **whether they surface anomalies rather than totals**. That's what classifying by structure buys you.

---

## 6. THE BLACKLIST — run the one for your domain

Before writing any spec, scan `references/day-two.md`.

### 6.A Personal — the day-two list

- **The fortune-cookie hook** — no variable, or a variable nothing produces (§3). The #1 killer.
- **The encyclopedia rail** — more than a third of channels are Knowledge type. That's a 百科, and nobody opens a 百科 daily.
- **Input debt** — `INPUT ≥ DEPTH` (§1.B), or three separate channels each demanding daily logging.
- **No Review channel** — nothing ever says 「你已经坚持 14 天」. Accumulation with no moment of return is just chores.
- **The fake Today** — a 「今日 X」 channel whose content is identical every day.
- **The blank cold start** — day one is `--`, so he never reaches day two.
- **Ten-plus channels** — a rail nobody can hold in his head becomes a menu he stops reading.
- **The pasted-on revenue seam** — a shop tab unrelated to any channel, or a product pushed on a channel he opened while in pain.
- **A moment that doesn't exist in his actual day.**
- **The system that has users** — 「XX 管理系统」 with roles bolted onto a personal workbench. (Two *readers* is not this — §9.)
- **It became a supervision tool** — a `care` workbench whose subject can object, whose hook reports deficits and whose record is kept about him rather than shown to him.

### 6.B System — the dead-console list

- **The demo-data lie** — the spec's hook shows `12 个待跟进`, and no field in the spec produces 12. The system-domain form of the fortune cookie, and the most expensive failure here (§3.C). **Detect it by rendering the first screen with an empty database.**
- **The list-page hellscape** — every module's L1 is the same table with a search box and pagination. Nine modules, nine identical screens, no screen anywhere that says a *conclusion*. **Fix: the primary module's L1 is a board, a curve or a triage list, not a table** — and the 结论条 is not optional.
- **The empty back office** — no seed data, no import path, no first-object flow. `registry` and `pipeline` both die here. **Every system spec needs `cold_start.day_1` to name a concrete first action** (导入一份名单 · 建第一个 Agent · 录一个客户), not a description of the empty state.
- **The noun module** — 「客户管理」「订单管理」「系统管理」. A noun plus 管理 is not a capability; it is the absence of a decision. **Every module's `does` must contain a verb someone performs.**
- **The permission hallucination** — three roles in the spec, and every role sees exactly the same screens. Either the roles differ in what they see or do (write it down, per module), or **there is one role and you should say so**.
- **The unbuilt integration** — the hook depends on data from 「ERP」「支付系统」「设备上报」 that has no API, no owner and no date. **Name it as a dependency in the spec or take the number out of the hook** (§3.C).
- **The orphan module** — a module with no relation to `subject`. In a CRM built around 客户, a 「公司公告」 module is somebody else's product. Cut it or fork it.
- **The three-level page tree with nothing at L3** — depth invented for symmetry. If a module has no genuine sub-record, it stops at L2 and that's correct.
- **Roles as an org chart** — more than four roles at definition time. He's describing a company, not a workbench. **Name the one who opens it daily and build for him first.**
- **Everything is `primary`** — nine modules of equal weight is the visual form of never having decided what matters.

---

## 7. THE REVENUE SEAM

Full material in `references/monetization.md`. Two rules that hold everywhere:

1. **The seam grows out of an existing module or it doesn't exist.** 暖宫贴 belongs on 疼痛急救 because that module is already about relief; a standalone 商城 tab is an ad. If you cannot name the module the seam attaches to, there is no seam yet — **and that's fine, say so.**
2. **Never monetize the module he opened while anxious or in pain.** 疼痛急救 during cramps, 宠物医院 at 2am, 情绪 on a bad day. Highest conversion, highest damage, and the damage is to the daily habit the whole workbench depends on.

> **In the system domain, `seam: none` is usually the correct answer** and writing one anyway is a defect. A CRM's revenue model is that someone paid for the CRM; a factory dashboard's is that it prevents downtime. Inventing an in-page 增值服务 for an internal tool produces the enterprise version of the pasted-on shop tab. The exception is a workbench that is itself the product for outside users — then the seam is a plan (席位 · 用量 · 模块解锁), it belongs in the spec's `seam` as one line, and it still must attach to a module.

---

## 8. HANDOFF — write the spec, then stop

Full schema in `references/handoff.md`. When the definition is confirmed, produce **`.workbench/spec.md`**.

### 8.A Both domains

YAML frontmatter — `purpose`, `user` (or `roles`), `surface`, `structure`, `moment`, `dials`, `hook` **with each clause's bound field and writer**, `cold_start` (day_1 / day_2 / day_7 / re_entry), **`home` — the first screen top to bottom**, `channels` with types, weights and **`does`**, **`mvp`/`later`**, **`visual`**, `seam`, `excluded`, `deferred`. Then Chinese prose for the human (who it's for, the evidence, one ordinary day end to end, why these modules, what was left out and why), and a closing **`## 给实现方`** section (`handoff.md` §3.A) that translates this method's private enums into plain build instructions.

**`home` and `channels[].does` are why the file can be built from rather than only read.** `hook` fixes the first line; without `home` the builder invents what sits under it, and a module with a name but no capability leaves its whole screen to guesswork.

### 8.B System domain adds three fields, and they are not optional

| Field | Why the spec is unbuildable without it |
|---|---|
| **`subject`** | The noun everything revolves around. Two CRMs — one around 客户, one around 订单 — have different first screens, different modules and different entities. One word, and it derives half the spec (`system-domain.md` §2) |
| **`entities`** | The data model: each entity's fields, **each field's writer** (§3.C), and the relations between them. **This is the field that makes the hook's numbers real.** A builder without it invents a schema, and the schema it invents won't produce the 结论条 |
| **`channels[].pages`** | Each module's L1 → L2 → L3 tree, with what each level shows and what can be done there. **A module name is not a screen.** Without this the builder renders nine identical tables — blacklist item 2 (§6.B) |

```yaml
subject: Agent
roles:
  - { name: 开发者, opens_daily: true, does: 建 Agent、看昨晚跑得怎么样、调提示词 }
entities:
  - name: Agent
    fields: [id, name, status, model, system_prompt, created_at]
    written_by: { name: user, status: system, model: user, created_at: system }
    relations: [Agent 1-n Run]
channels:
  - name: Agent
    type: today
    weight: primary
    does: 建 Agent、启停、改提示词、看每个跑得怎么样
    pages:
      - { level: L1, shows: Agent 卡片列表 + 状态筛选, actions: [新建, 启停, 复制] }
      - { level: L2, shows: 配置 + 最近 10 次运行 + 本月用量, actions: [编辑, 试运行] }
      - { level: L3, shows: 单次运行的逐步日志和输入输出, actions: [重跑, 导出] }
```

**Write `## 给实现方` every time.** finesse-ui knows the vocabulary; Cursor, v0, 通义 and a human contractor do not, and the decoder table lives in `handoff.md`, which does not travel with the spec. Without it the builder renders six identical tabs and a greeting strip, and nothing in the file says otherwise.

**No filesystem? Print the whole spec in one fenced block** and say in one line that it can be copied to any builder (`handoff.md` §1.A). Most people running this skill are in a chat product, and their handoff is a paste, not a path. **Never claim to have written a file you didn't.**

The mapping finesse-ui reads (this stays here; the spec carries §3.A instead):

| Spec field | Becomes, in finesse-ui |
|---|---|
| `surface: phone` / `desktop` | register `h5` (a page in a phone browser) / `product` (a page in a desktop browser) |
| `channels[]` | the navigation — bottom bar or sidebar; count drives the shell choice |
| `channels[].pages` | the routes, and the depth the shell must support |
| `hook` | the first screen, above everything |
| `entities` | the tables, the forms, the columns, the filters |
| `cold_start` | **the empty state** — and finesse-ui treats an empty state as a real image slot |
| `structure.primary` | the dominant display: cycle → calendar · ledger → curve · pipeline → board · registry → list+detail · console → fleet cards · monitor → figures+drilldown · operation → figures |

> **Writing the spec is the end of this skill's job. Building is a separate yes.** Offer the handoff in one line and wait — the user may want to sit with the definition, take it elsewhere, or build it himself.

---

## 9. OUT OF SCOPE

finesse-brief defines **what a workbench is** — personal or system — and stops at the definition. Hand off when the work is:

- **the interface** → finesse-ui (that's the designed handoff, §8);
- **the engineering** — storage, sync, auth implementation, model choice, deployment, how the integration actually gets built. **The spec names an integration as a dependency (§3.C); it does not design it.**
- **a real multi-tenant commercial product** — 计费、租户隔离、合规、SLA、销售流程、路线图. **Roles are in scope; a company's product strategy is not.** The line: this skill defines one workbench thoroughly. It does not do product management for a SaaS business.
- **clinical, financial or legal substance.** This skill decides that a 妇科科普 or 持仓体检 or 用药提醒 module should exist and what it must show. **It does not supply the medical, financial or legal content, and it must not invent it** — a module containing a plausible-sounding fabrication is worse than no module. Name it, then say plainly where real content has to come from.

**Two things that used to be out of scope and no longer are.** *Multiple roles* — 「销售看自己的，主管看全组」 is now `roles` plus per-module differences, not a refusal. *Enterprise categories* — CRM, ERP, 工厂, 医疗, 教育 are `pipeline`/`operation`/`monitor`/`registry` workbenches and are handled by the system track. What still isn't in scope is the *business* around them.

**And one boundary that hasn't moved.** A 妈妈给孩子做的学习工作台 has two people looking at it and stays **personal**: one owner, one domain, one moment, one hook, no page tree, nobody logging in as a *type*. **Two readers of one surface is a writing problem** — the same sentence must be true and kind for both (`hook-engineering.md` §7) — not an architecture problem. When the second reader has a will of his own (a school-age child, an aging parent), the extra rules live in `workbench-types.md` §6.A.
