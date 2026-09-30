---
name: prd-architect
description: >
  PRD 架构师 / 需求文档起草：当用户要把一个产品想法、需求草稿、脑暴结果或功能说明整理成 PRD 时使用。
  可用中文唤起：“帮我写 PRD”“帮我选 PRD 模板”“把这个需求整理成 PRD”“判断该用轻量 PRD 还是标准 PRD”
  “补一张可编辑 Draw.io 核心流程图”“PRD 里加架构图”。
  会在 PRD-lite、PRD-standard、PRD-ai-native 中选择一个模板资产按需加载，并在需要时加载 mockup handoff、
  Draw.io 图示或开发 handoff 附录；页面型 PRD 默认联动生成项目 UI 对齐的 HTML、关键截图和正文证据。
  不用于直接编码、单纯画 UI，或评审一份已经写好的 PRD。
---

# PRD 架构师（prd-architect）

## 中文速查

- 中文名：PRD 架构师 / 需求文档起草
- 英文稳定名：`prd-architect`
- 你可以这样叫我：`帮我写 PRD`、`帮我选 PRD 模板`、`把这个需求整理成 PRD`、`这个需求该用哪种 PRD`、`PRD 里补 Draw.io 流程图`
- 适合：需求还在成型，需要判断 PRD 类型、当前成熟度、模板资产和后续 UI / handoff 承接
- 不适合：已有完整 PRD 要评审时改用 `prd-review`；只要正式 UI mockup 时改用 `ui-mockup-desktop-workbench`；直接编码不触发

## Overview

这个 Skill 负责把产品想法组织成结构匹配的 PRD。它不是固定展开重型模板，而是：

1. 先判断上游输入是否足够成熟。
2. 再选择 `PRD-lite / PRD-standard / PRD-ai-native` 其中一个模板资产。
3. 只加载本轮需要的附加资产；页面型 PRD 自动激活 mockup handoff 和 UI 证据链。
4. 以“短背景 + 功能模块”为正文主干，把目标态 UI 和功能逻辑放在同一个模块内。
5. 只有复杂链路才生成 Draw.io，不为简单需求补装饰性流程图。
6. 生成文件时尽量运行 PRD shape 自检，避免把初版 PRD 写成实现方案。
7. 每份 PRD 都在标题后维护一张版本记录表，让首次创建和后续迭代可追溯。

## Upstream Boundaries

不要把所有输入都直接写成 PRD。先判断上游是否已经成熟：

- 问题、用户、目标或判断标准还不清楚：先转 `ai-collaboration-calibration` 做问题校准。
- 问题已确认，但具体方案、架构、计划或产品决策需要压力测试：先转 `grill-me`。
- PRD 中存在重大产品、技术、商业或平台选择，且缺少证据：先转 `decision-research`。
- 已有 PRD/handoff 只是要判断能否交付开发：转 `prd-review`，由它给 readiness verdict。
- PRD 和 UI 规范都已确认，用户要正式桌面端多状态页面 mockup：转 `ui-mockup-desktop-workbench`。

`prd-architect` 可以根据上游输出起草或修订 PRD，但不自我批准 `Ready for writing-plans`。

## Responsibilities

这个 Skill 负责：

1. 判断需求复杂度和当前成熟度。
2. 判断是否属于 AI-native 需求。
3. 选择并加载一个 PRD 模板资产。
4. 按需加载 mockup、Draw.io 或 handoff 资产。
5. 组织 PRD 正文、待确认项和下一步建议。
6. 在生成到文件时运行可用的确定性检查。
7. 当 PRD 包含用户可见界面时，编排 `ui-mockup-desktop-workbench`，在同一交付中完成 HTML、关键截图和正文回填。
8. 新建 PRD 时初始化 `V1.0`，修订时读取现有版本历史并记录本轮实际修改点。

它不负责：

- 直接决定 UI 视觉细节。
- 把 standalone HTML 当成生产代码；正式视觉实现由 `ui-mockup-desktop-workbench` 负责，但本 Skill 负责触发、收口和验证这条交付链。
- 直接开始编码。
- 把核心规则外包给单独 guide 再让用户自己跳转理解。
- 在用户只要“初版 PRD”时展开接口字段、TypeScript、JSON schema、adapter 或 metadata 结构。

## Workflow

### 1. Intake

先从用户输入和可发现项目上下文提炼：

- 需求描述、目标用户、当前问题、成功标准。
- 已知边界、非目标、待确认点。
- 是否涉及既有界面、截图、HTML mockup 或正式 UI mockup。
- 已有页面资产属于现状参考、与本期目标一致的目标稿，还是已经过期/结构不匹配的旧原型。
- 是否涉及 AI 协作、模型生成、推荐、记忆、人工确认或人工接管。
- 是否明确要求开发 handoff、接口字段、协议 schema 或实现计划。
- 是否会发布到钉钉或其他在线文档；若会发布，默认按“发布版正文”组织，不把本地路径当成正文信息。

如果输入缺失，可以基于明确假设先出第一版；不要把缺失业务判断伪装成已确认事实。

### 2. Select Template Asset

读取 `references/template-selection.md`，选择且只选择一个模板：

- `references/templates/prd-lite.md`
- `references/templates/prd-standard.md`
- `references/templates/prd-ai-native.md`

不要同时加载三份模板来拼接章节。选中模板后，按模板内的“章节启用条件”和“禁止内容”写正文。

### 2A. Initialize Or Revise Version History

读取 `references/prd-versioning.md`，并把版本记录作为 PRD 的固定顶部内容：

1. 新建 PRD 时，在标题后、其他 H2 章节前创建 `版本记录` 表，初始版本为 `V1.0`，日期为当前工作时区当天，修改内容为 `首次创建`。
2. 修订已有 PRD 时，先读取当前版本表再改正文；不能覆盖、删除或复用已有版本行。
3. 用户明确给出目标版本时使用该版本；否则普通功能、交互、文案或规则迭代默认把小版本 `+0.1`。
4. 产品目标、交付范围、核心信息架构或核心流程发生实质变化时升级主版本，并把小版本归零。
5. 最新版本放在第一行，用 1-3 个具体修改点说明本轮变化；禁止只写“更新 PRD”“优化文档”等空泛内容。
6. 仅重试发布、回读钉钉、重拍同内容截图、调整格式或修正不改变产品含义的错别字时，不新增版本。

### 3. Activate Optional Assets

只在触发条件满足时加载附加资产：

| 资产 | 何时加载 |
| --- | --- |
| `references/mockup-handoff.md` | PRD 涉及任何用户可见页面、弹窗、面板、按钮、表单或状态提示；即使用户没有单独要求 HTML 也要加载 |
| `references/mockup-evidence-manifest.md` | 页面型 PRD 需要解析真实 UI 来源、生成 HTML/截图并验证证据新鲜度 |
| `references/product-delivery-manifest.md` | 用户要求建立/更新 Product Delivery Package，或下游 Review/Publisher 要消费 Manifest |
| `references/drawio-templates.md` | 用户明确要求正式图示，或链路跨多角色/系统、含关键判断或回流、异步恢复，或达到 6 个及以上相互依赖步骤 |
| `references/handoff-appendix.md` | 用户明确要求开发 handoff、字段定义、协议、接口、adapter、metadata 或实现计划前置材料 |
| `references/prd-shape-gates.md` | 需要自检 PRD 是否过重、过技术化、章节误激活或待确认项处理不当 |

### 3A. Detect UI-bearing PRDs

只要本期定义了用户可见的页面、弹窗、抽屉、表单、卡片、导航、按钮、空态、错误态、确认态或成功态，就把它判定为页面型 PRD。页面型 PRD 的默认交付不是单一 Markdown，而是：

`PRD + 项目 UI 对齐 HTML/preview + 关键状态截图 + PRD 对应章节内嵌截图`

执行规则：

1. 用户不需要再次说“生成 HTML”或“补截图”；页面型判断本身就是触发条件。
2. 先定位真实项目、app/路由、组件、样式 token、图标和相邻页面状态，再调用 `ui-mockup-desktop-workbench`。
3. 默认选择 `visual-handoff`，在 PRD 产物目录生成独立 HTML，不修改生产前端；只有用户明确要求项目内 preview 或真实实现承接时才选择 `project-native-preview`。
4. 讨论中 PRD 可以生成“目标态草稿” HTML，但必须把未决内容标成假设；只有阻断性的页面信息架构或状态决策未关闭时才跳过。
5. 至少截取每个实质变化页面的默认态；PRD 明确定义的关键拦截、失败、确认或成功态按关键状态覆盖需要补图。
6. 截图直接插入它解释的功能或状态章节，不在文末集中堆放。
7. standalone HTML 必须明确标记为视觉交付参考，不得声称它是生产代码。
8. 只有用户明确要求纯文本、需求完全无界面、阻断性页面决策未关闭、或真实项目不可访问且无法形成有证据的静态复刻时可以跳过。最终说明要写清原因、受影响页面和待补动作。

### 3B. Resolve The UI Baseline

生成视觉产物前必须先把 UI 来源解析为唯一、可追溯的基线。不要仅凭目录名包含 `latest`、更新时间较新或页面名称相似就自行选择前端项目。

按以下顺序处理：

1. 用户已给出明确前端仓库、app、路由或组件时，读取并验证它确实承载目标页面。
2. 用户没有给路径时，可以在已授权的 workspace 和会话上下文中发现候选仓库；只有存在唯一且能由路由、组件或产品标识证明的候选时才直接采用。
3. 存在多个候选、找不到目标页面或无法证明仓库身份时，停止生成 HTML，向用户问一个简短的来源确认问题。PRD 文案可以继续，但视觉证据状态必须标为 `source_resolution_required`。
4. 用户确认没有可访问的真实前端后，优先请其提供当前页面截图、参考 HTML 或 UI 规范。允许从这些证据提取颜色、字体、间距、圆角、密度、导航结构和组件形态，但来源必须记为 `screenshot` 或 `reference-html`，并明确“截图推断，不代表生产组件已验证”。
5. 既没有真实前端，也没有截图、参考 HTML 或 UI 规范时，不生成声称项目对齐的高保真 HTML；说明缺少什么证据以及用户补充后从哪个状态继续。

来源强度从高到低为：`frontend-repo > design-system > reference-html > screenshot`。低强度来源可以支撑视觉草稿，但不能升级为“生产对齐”结论。

### 3C. Durable UI Evidence Workflow

页面证据链按轻量、可恢复状态机执行：

`source_resolution_required -> source_resolved -> mockup_built -> screenshots_fresh -> prd_embedded -> verified`

这类似 Temporal 的 durable workflow 思路，但默认不引入 Temporal 服务依赖。使用 `mockup-evidence.json` 保存 checkpoint 和 provenance，使用确定性脚本验证状态迁移：

- UI 基线变化会使 `mockup_built` 及其后状态失效。
- HTML 内容变化会使 `screenshots_fresh`、`prd_embedded` 和 `verified` 失效。
- 截图变化或丢失会使 `prd_embedded` 和 `verified` 失效。
- PRD 修改后必须重新记录并验证正文图片引用。
- 不允许仅凭“文件存在”恢复到完成态；必须重新计算 commit/hash 并通过门禁。

读取 `references/mockup-evidence-manifest.md`，按其中命令捕获和验证 evidence manifest。截图时间早于 HTML 时必须失败并要求重拍；不要通过触碰文件时间或重新保存旧图绕过。

### 3D. Product Delivery Package Mode

用户明确要求 Product Delivery Package、提供 `product-delivery-manifest.yaml`，或交付目标包含完整 Package Review/发布时，读取 `references/product-delivery-manifest.md`。

1. 把 Manifest 作为输入和产物索引，不把它当第二份 PRD；已有 Manifest 时先读取再修改 Maker 分区。
2. 显式记录 `ui_requirement.required`。只要本期存在用户可见 surface 就是 `true`；只有 `reason: no_user_visible_surface` 才能为 `false`。前端不可访问、浏览器失败或时间不足都不能改成无 UI。
3. Maker 只写 Package identity、revision、UI applicability、sources、decisions 和 PRD artifact。不要写 `review`、`approvals` 或 `release`，也不要把本 Skill 的 shape check 当独立 Review。
4. 页面型 Package 交给 UI Skill 补齐 HTML/preview、Action Contract、截图、baseline 和 anchor；无页面 Package 不为满足形式伪造 HTML 或截图。
5. 运行 `scripts/validate_product_delivery_manifest.py` 计算当前 input fingerprint 和最早恢复节点。校验成功最多把 Maker 交付推进到 `review_pending`，不能自行产生 `package_ready`。

### 4. Write PRD

输出必须做到：

1. 标题后的第一个 H2 章节必须是 `版本记录`，并符合 `references/prd-versioning.md`。
2. 背景只说明当前问题、主要影响和为什么现在处理，最多 200 字；能更短说清就不要凑字数，调研过程和长期愿景不进入正文。
3. 用一句话写清“本期只解决什么”，并只保留最容易误解的非目标。
4. 不单列“用户场景、入口与触发、页面结构、核心对象、交互逻辑”作为默认章节；把这些信息放进对应功能模块。
5. 每个功能模块先说明一句话目的；页面型模块紧接目标态 UI 截图，再用短表写条件/状态、用户动作、系统行为和 UI 反馈。
6. 状态名称相近但主体或作用域不同，补“主体、判定时点、影响范围、用途”，不要用一个模糊状态承载多种规则。
7. 同一规则只写一次；跨两个及以上模块的规则才进入“跨模块规则”。
8. 如果涉及既有前端页面，先定位真实项目、真实路由和真实组件，再写页面稿。
9. 如果只是产品初版，不在正文写 TypeScript interface、JSON schema、endpoint、adapter、metadata 或 capability 字段；明确要求 handoff 时才放入开发附录。
10. 页面型 PRD 无论是否已有 HTML/mock，都要在本轮完成目标态 HTML、关键状态截图和正文回填。已有旧原型与新 PRD 不一致时先更新原型，不把旧截图冒充目标稿。
11. 若用户准备把 PRD 发到钉钉，正文默认不输出“关联产物”聚合区和“待确认事项”章节；待确认项只保留在本地草稿、最终说明或明确标注的发布前检查清单中。

### 5. Diagram Mode

正式流程图统一使用 Draw.io。用户明确要求图示时直接启用；用户未要求时，只有复杂度门槛成立才启用。

执行规则：

1. 先检查用户是否明确要求正式图示；明确要求时无条件启用。只有用户未要求时，才判断是否跨多个角色/系统、存在关键判断或回流、包含异步等待/恢复，或达到 6 个及以上相互依赖步骤；都不满足才省略整个流程图章节。
2. 需要图时判断它要回答的问题：系统是什么、链路怎么跑、还是人和 AI 如何协作。
3. 读取 `references/drawio-templates.md`，选择 `architecture` 或 `flow` 布局；不要先画 Mermaid / ASCII 再重复画正式图。
4. 生成可编辑 `.drawio` 源文件；如果 PRD 需要 Markdown 可预览，优先交付包含 Draw.io 数据的 `*.drawio.svg`。
5. 在 PRD 的“核心流程”处引用图示，并说明它支撑哪些功能模块。
6. 对 `.drawio` 源文件运行 `python3 scripts/validate_drawio.py <path>`。
7. 如果验证工具不可用，必须在最终说明里标记“图示可编辑性未验证”。

### 6. Mockup Handoff

当需求发生在既有产品页面上，优先读取 `references/mockup-handoff.md`。PRD 中应写清：

- 页面范围、触发入口、关键状态、用户可见反馈。
- 需要截图、静态 HTML mockup、真实页面截图，还是转交正式 UI mockup。
- mockup 展示哪个状态：默认态、拦截态、确认态、失败态或成功态。
- 截图应该插入哪个 PRD 功能模块；同一 mock 可以复用，但不要在底部“关联产物”集中堆图。

页面型 PRD 执行页面证据门禁：

1. 先判断原型与本期 PRD 的页面、模块和状态是否一致。
2. 没有目标态原型时，调用 `ui-mockup-desktop-workbench` 新建；已有且一致时实际打开或渲染。至少截取每个实质变化页面的默认态，关键失败态、空态、确认态或成功态按需补图。
3. 将每张截图直接嵌入它解释的功能/页面/状态章节，图片下说明状态和验证重点。本地附录里的 HTML/PNG 路径不能替代正文截图。
4. 仅代表现状的截图要标注“现状参考”；与本期结构不一致的旧原型要先更新，或转 `ui-mockup-desktop-workbench` 的 `structure-only` mode，不能作为目标态证据。
5. 只有 3A 节规定的跳过条件成立时可以跳过；原型不可运行时先尝试安全修复或重新生成，不把“当前没有 HTML”当作跳过理由。

### 7. Publish-ready PRD Mode

当用户明确提到“上传钉钉 / 发到钉钉文档 / 发布给开发看 / 线上 PRD”时，把 PRD 当作发布版写：

1. 标题后的版本表记录当前版本、日期和本轮具体修改点；更新线上 PRD 前必须先完成版本递增。
2. 文档信息表只放功能名、状态、模块等可读信息，不放本地 mock URL、`.html`、`.png` 或 `dingtalk-assets` 路径；当前版本只以顶部版本记录表为准，不维护第二套版本字段。
3. 页面或 mock 截图应嵌入对应章节，例如输入框状态放在输入框章节、任务卡状态放在任务卡章节、取消逻辑放在取消章节。
4. “待确认事项”默认不进入发布版正文；确需保留时，改写成“发布前仍需确认”，并在最终说明中提示不要直接上传。
5. “关联产物”默认不作为发布版正文模块；本地草稿可以保留，但要标记为 `本地草稿，不上传钉钉正文`。
6. 如果 PRD 后续交给 `dingtalk-prd-publisher`，最终说明提醒它需要校验版本表、做钉钉回读和浏览器可见性验证。

### 8. Self-check

如果本轮把 PRD 写入 Markdown 文件，尽量运行：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native>
```

当用户明确要求开发 handoff 时增加：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> --allow-handoff
```

当用户说明 PRD 要上传钉钉或发布到在线文档时增加：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> --publish-ready
```

页面型 PRD 的完成态必须同时检查正文截图、本轮 HTML 和 evidence manifest：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> \
  --require-mockup-evidence --require-mockup-artifact <mockup.html> \
  --require-current-mockup-evidence --mockup-manifest <mockup-evidence.json>
```

该门禁会检查每个功能模块是否各自包含目标态图片和功能逻辑，并验证本地图片引用是否真实存在；只放在背景、“本地草稿附录”或“关联产物”中的图片不算完成。脚本会从文档信息自动识别成熟度；非常规格式可用 `--maturity draft|discussing|confirmed` 显式指定。发布版应先完成本地证据检查，再由发布流程上传或重写图片引用。

所有新建或修订 PRD 都增加版本历史门禁；`--publish-ready` 会自动启用同一检查：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> --require-version-history
```

检查失败不等于不能交付，但最终说明必须解释哪些 warning 是故意保留的，哪些需要修订。

## Revision Input Contract

当用户提供 `prd-review` findings、revision draft、open blockers 或 readiness status 时，可以进入修订模式：

1. 先识别本轮 patch scope：只修 blocker、补可验证结果、补异常、补图示，还是重组章节。
2. 读取当前版本记录，判断本轮是普通小版本还是产品范围/核心流程变化触发的主版本。
3. 把 review finding 分成事实缺口、表达缺口、可验证性缺口、图示缺口和待确认决策。
4. 只改能从输入中支撑的内容；缺失业务判断写成待确认项。
5. 在正文修改完成后，把本轮实际修改点作为一行新记录置顶；若只是格式或发布重试，不新增版本。
6. 输出最小可替换章节或段落，不默认重写整份 PRD。
7. 修订后建议回到 `prd-review` 做 readiness re-check；readiness verdict 不由本 Skill 给出。

## Downstream Handoff

只有 PRD 满足以下条件，才建议进入 superpowers `writing-plans`：

- 目标用户、问题、范围边界和非目标已经明确。
- 主流程、关键状态、输入输出、异常或人工接管点已经写清。
- 关键动作的系统行为、用户可见反馈、失败结果和恢复方式已经写清，并可被测试、人工检查或通过具体 artifact 验证。
- 阻断性待确认项已经关闭；若仍有假设，必须明确写成 implementation plan 的前置假设。

如果不满足这些条件，下一步应继续深化 PRD、补 handoff 或做 `prd-review`。

## Definition of Done

完成标准是：

- 已选定且只加载一个 PRD 类型模板。
- 标题后的首个 H2 是有效的版本记录表；新建文档从 `V1.0` 开始，修订文档保留历史、最新置顶且修改内容具体。
- 当前状态明确，正文成熟度与状态一致。
- 背景不超过 200 字且不为凑字数扩写，正文以功能模块为主，没有模板填空式的用户场景或重复章节。
- 页面型模块的目标态 UI 与功能逻辑就近呈现；同一规则没有跨背景、流程、模块和其他章节重复。
- 只有复杂度门槛成立或用户明确要求时才生成 Draw.io；简单需求没有装饰性流程图。
- 待确认项和假设没有混在一起。
- mockup / 图示 / handoff 附加资产只在需要时启用。
- 页面型 PRD 已在同一交付中生成项目 UI 对齐的 HTML/preview，关键状态已实际截图并嵌入对应功能章节；旧原型不匹配时已更新或明确停止使用。
- 页面型 PRD 已解析并记录唯一 UI 基线；来源不明确时已询问用户，没有真实前端时才使用用户确认的截图或参考 HTML，并标注证据强度。
- `mockup-evidence.json` 已记录基线 commit/hash、HTML hash、截图来源 hash 和 PRD hash；当前文件通过新鲜度门禁，HTML 更新后的旧截图不能继续充当完成证据。
- 无截图只允许发生在明确的跳过条件下，且原因和待补状态已说明；HTML 路径或截图计划本身不算页面证据。
- 涉及发布到钉钉或在线文档时，本地 mock 链接、截图路径、关联产物和待确认项没有污染发布版正文。
- 如果本轮生成 Draw.io 图示，`.drawio` 已验证或验证限制已明确说明。
- 如果本轮写入 PRD 文件，已运行 `check_prd_shape.py` 或说明未运行原因。
- 下一步建议不会把草稿误推成定稿。

## Evaluation

Smoke prompts:

- 单点改动，是否只加载 `PRD-lite` 并保持 5 分钟可读。
- 常规跨状态功能，是否加载 `PRD-standard`，以功能模块承载目标态 UI 和逻辑，不生成独立用户场景章节。
- AI 协作需求，是否加载 `PRD-ai-native`，把人工动作、AI 动作、系统反馈和回退写进对应模块。
- 简单页面改动是否省略流程图；复杂多角色回流链路是否生成并验证 Draw.io。
- `帮我写一个 PRD，并补一张可编辑 Draw.io 核心流程图。`
- `回答后下一步行动建议 PRD 初版`，应输出产品规则和 UX 行为，不输出实现 schema。
- `这份 PRD 后面要上传钉钉，mock 截图直接放到对应模块里。`，应启用发布版正文规则，不输出本地 mock 链接、关联产物聚合区或待确认事项正文。
- `基于已有 HTML mockup 起草多页面 PRD，并把关键页面截图放到对应功能章节。`，应先校验原型与目标结构是否一致；一致则实际生成截图并内嵌，不一致则更新原型或明确停止把旧原型当目标稿。
- `基于真实项目写一个新增审批抽屉的 PRD。`，即使用户没有说 HTML，也应在同一交付中生成 UI 对齐 HTML、关键状态截图并回填对应章节。
- `工作区里有两个可能的前端仓库，但我没说用哪个。`，应先问一个来源确认问题，不自行选择名称带 `latest` 的目录。
- `我们没有可访问的前端项目，我只给你一张现有页面截图。`，应把截图作为低置信视觉基线，提取可观察规范并记录 hash，不声称已验证生产组件。
- `HTML 刚更新过，但目录里已有上一版截图。`，必须让截图失效并重拍，不能因图片文件存在而通过。
- `写一个完全没有用户界面的 API 限流策略 PRD。`，不应生成 HTML 或截图。

Non-trigger prompts:

- 直接让它改代码。
- 只让它画正式 UI mockup。
- 只做目录治理。
- 已有 PRD 要找问题，应转 `prd-review`。

Resources:

- `references/template-selection.md`
- `references/prd-versioning.md`
- `references/templates/prd-lite.md`
- `references/templates/prd-standard.md`
- `references/templates/prd-ai-native.md`
- `references/mockup-handoff.md`
- `references/mockup-evidence-manifest.md`
- `references/product-delivery-manifest.md`
- `references/drawio-templates.md`
- `references/handoff-appendix.md`
- `references/prd-shape-gates.md`
- `scripts/check_prd_shape.py`
- `scripts/check_prd_version_history.py`
- `scripts/capture_mockup_evidence.py`
- `scripts/validate_product_delivery_manifest.py`
- `scripts/validate_drawio.py`
