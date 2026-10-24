---
name: make-dsh-plugin
description: >
  当用户要为 DeepSeek Harness（dsh）开发插件、或搭一个垂直 Agent 产品时使用本
  skill。先给 dsh 的概念地图（一切皆插件；profile / bundle / plugin / agent
  preset / skill 五种装配单位；宿主树与 per-Agent 树），再引导三种活：加一个
  工具或界面、发一个新的 Agent 模式（preset）、用「工具 → preset → UI + 新
  profile」从零搭垂直 Agent。覆盖形态选择（bundle 组合层 / 纯 cordis / 纯
  skill 包 / MCP）、npm 包与 Cordis entry、client half 与设置页、安装与验证
  纪律、UI 风格、多语言、README 与发布规范、门禁与决策记录。
license: MIT
metadata:
  author: vlln
  version: "5.3.1"
requires:
  bins:
    - dsh
---

# 创建 dsh 插件

dsh（DeepSeek Harness）是 agent harness——一个 Cordis 运行时加一套内置能力
（工具、会话、设置、Web GUI）。**插件就是给它加能力的 npm 包**：注册工具 / 服务 /
事件 / 命令 / prompt，或者往 Web GUI 里加界面。插件经 **web profile** 安装，
用户用 `dsh plugin --profile web add <包>` 装卸、在官方 Plugins 页查看与配置。

**代码插件的分发形态有两种**，选型只看是否需要"组合层"（判据见 Step 0）：
**bundle**——声明 `dsh.bundle.patch`，自带一层组合 patch（多行 insert/config/disabled
随包分发）；**纯 cordis**——单个 Cordis 插件包，装完在 profile 的 `cordis.patch.yml`
里写一行 insert。两者都能带 client half（`dsh.client`）往 Web GUI 加界面。
**纯 skill 包**（无代码）走文件系统发现根，不属于这两类。注意：**bundle 是分发单位，
plugin 是功能单位**——同一个包可以只当其一，也可以两者兼任（见
[01-concepts.md](references/01-concepts.md) L1）。

**本 skill 的路线**：Step 0 选形态 → Step 1 仓库布局 → Step 2 manifest → Step 2b 图标 →
Step 3 Node half → Step 4 client half（可选）→ Step 5 安装与验证 → Step 5b 交付检查与发布
（发布可选）→ Step 6 README 与开发规范。**要从零搭一个垂直 Agent，先读
[03-vertical-agent-recipe.md](references/03-vertical-agent-recipe.md) 的三步法。**

**权威契约内嵌在本 skill 的 `references/`，按主题编号取用**（`01` 概念 · `02` 装配 · `03` 配方 ·
`04` 契约 · `05` bundle · `06` UI · `07` 设置 · `08` i18n · `09` 纪律 · `10` 验证 ·
`11` 发布 · `12` 生态 · `13` 证据池 · `14` Desktop）——**不必线性读**，按第 2 节的边界地图取一篇即可；
开发不需要任何仓库文档（`06-ui-style.md` 是查阅型手册，按章查）。

## 0. 30 秒版（够开工）

**一切皆插件**：插件声明自己提供的服务与 `inject` 依赖，Cordis 牵线并管理生命周期。
在此之上只有五种装配单位：

| 你会听到 | 单位 | 落点 | 一句话 |
|---|---|---|---|
| 运行方式（web / headless） | **profile** | `$DSH_HOME/profiles/<name>/` | 装哪些 bundle + 用户 patch；也是**安装与解析边界** |
| 插件包 / 一组插件 | **bundle** | `dsh.bundle.patch`（可为数组） | 可复用的 patch 层，可只分发别人的行 |
| 插件 / 组件 | **plugin** | npm 包 + Cordis entry | 功能零件：工具 / 服务 / 命令 / 事件 / UI |
| 模式（标准 / 极简 / 创造） | **agent preset** | `preset-<id>` 行 | 每个 Agent 的**工具 + 人设 + 技能**组合 |
| 技能 | **skill 包** | `.dsh/skills` 等发现根 | 无代码，不进 profile 装配 |

**两棵树**——本 skill 里所有"该放哪"的判断都来自这里：

- **宿主树**：一个进程一棵，由 profile 层栈决定。模型路由、Agent 循环、会话、设置、
  沙箱/审批、**工具注册表本体**都在这里，**所有 preset 共享**。
- **Agent 树**：每个会话按选中的 preset 分出一棵隔离子树，装 persona、instructions、
  工具行、技能——**只有该 Agent 看得见**。

一句话记住：**profile 决定装了什么，preset 决定 Agent 看得见什么。** preset 不拥有模型与
Agent 循环（那是宿主）；权限预设是第三件事。展开见 [01-concepts.md](references/01-concepts.md)。

## 1. 先选一条路线（不必线性读）

每一步**只需要读一个文件**；读完就能动手，细节留到碰到时再展开。

| 路线 | 顺序 |
|---|---|
| **A 加一个工具 / 命令 / 面板** | [04](references/04-plugin-contract.md) →（有 UI）[06](references/06-ui-style.md) → [10](references/10-install-and-verify.md) |
| **B 发一个新的模式（preset）** | [02](references/02-profile-and-preset.md) §2 → [03](references/03-vertical-agent-recipe.md) 第 2 步 → 新开会话验证 |
| **C 从零搭一个垂直 Agent** | [03](references/03-vertical-agent-recipe.md) 全文 → [04](references/04-plugin-contract.md) / [05](references/05-bundle-plugins.md) 写包 → [06](references/06-ui-style.md) 做 UI → [10](references/10-install-and-verify.md) 装 |
| **D 发布与被发现** | [11](references/11-publish.md) 交付/发布 → [12](references/12-ecosystem.md) 市场与社区 |
| **E 装不上 / 行为怪** | [10](references/10-install-and-verify.md) 排查 → [13](references/13-gotchas.md) 对症状 |
| **F 理解 dsh 机制** | [01](references/01-concepts.md) 概念 → [02](references/02-profile-and-preset.md) 装配 |
| **G 在 Desktop 上装 / 调** | [14](references/14-desktop.md)（应用内插件页、版本跟应用走、DevTools） |

## 2. 边界地图（一个问题 = 一个文件）

每个 reference 开头都有同样的「本文件回答 / 不回答」框；这里是一张总表。

| # | 文件 | 回答什么 | 不回答 → 去 |
|---|---|---|---|
| 01 | [concepts](references/01-concepts.md) | 为什么分层、五种单位、两棵树、生命周期、术语 | 命令与字段 → 02；搭产品 → 03 |
| 02 | [profile-and-preset](references/02-profile-and-preset.md) | profile 目录/层栈/解析；preset 声明/选择/分发/覆盖 | 从零搭产品 → 03；entry 字段 → 04 |
| 03 | [recipe](references/03-vertical-agent-recipe.md) | 三步法、每步检查点、常见返工 | 字段细节 → 02 / 04；UI 规格 → 06 |
| 04 | [plugin-contract](references/04-plugin-contract.md) | `dsh` 字段、entry、client、skill、MCP 契约 | 打包 → 05；安装验证 → 10 |
| 05 | [bundle-plugins](references/05-bundle-plugins.md) | bundle 形态、patch 数组、依赖解析、Git 安装 | preset → 02；市场 → 12 |
| 06 | [ui-style](references/06-ui-style.md) * | token / 控件 / 落位 / 视觉自检 | 设置面 → 07；文案 → 08 |
| 07 | [settings-panel](references/07-settings-panel.md) | `Config` + 配置卡片契约与验证 | UI 视觉 → 06；字典 → 08 |
| 08 | [i18n](references/08-i18n.md) | 客户端字典 / 包元数据 / 宿主文案 | 设置面 → 07 |
| 09 | [dev-conventions](references/09-dev-conventions.md) | 11 条纪律 + 门禁 / 决策 / 兼容性 | 证据 → 13；操作 → 10 |
| 10 | [install-and-verify](references/10-install-and-verify.md) | 安装、验证、负控、图标验收、排查 | 发布 → 11；纪律 → 09 |
| 11 | [publish](references/11-publish.md) | 交付清单、description / topics | 市场社区 → 12；验证 → 10 |
| 12 | [ecosystem](references/12-ecosystem.md) | 市场索引机制、社区入口、生态目录与工具、参考实现 | 发布纪律 → 11 |
| 13 | [gotchas](references/13-gotchas.md) | 实测坑与症状 | 纪律 → 09；验证 → 10 |
| 14 | [desktop](references/14-desktop.md) | Desktop 的安装归属 / 版本 / 调试 / 恢复 | 通用安装验证 → 10；UI → 06 |
| 15 | [product-boundaries](references/15-product-boundaries.md) | 产品边界：数据放哪、向 agent 暴露什么、工具面还是 skill+命令、面板与会话的关系 | 字段与契约 → 04；验证 → 10 |

## 3. Step → 文件

| Step | 本步只读 | 产出 |
|---|---|---|
| 0 选形态 | 01 / 02（做内容型插件再加 15） | 形态 + 安装通道（三判据） |
| 1 仓库布局 | 04 | 目录骨架 |
| 2 manifest | 04（+05 打包时） | `package.json` + patch |
| 2b 图标 | 10（图标节） | `icon.svg` + 真实加载验证 |
| 3 Node half | 04 | entry + 工具/服务 |
| 4 client half | 06（+04/07/08） | client bundle + UI |
| 5 安装验证 | 10（+02 通道） | 装上 + 真调一次 |
| 5b 交付发布 | 11（+12 推广） | 清单过 + 发布 |
| 6 README / 规范 | 09（+11） | README + 门禁 |

## 4. 纪律（11 条，动手前扫一眼）

逐条有反例与细节指针（[09-dev-conventions.md](references/09-dev-conventions.md)）；违反其中任何一条
都会在真实装载时暴露，且大多**不会在 mock 单测里暴露**。

| # | 纪律 | 为什么 |
|---|---|---|
| 1 | 官方包 `dependencies` / `peerDependencies` / `devDependencies` 三处留空 | 官方包自带整条 peer 闭包，声明必 ERESOLVE（[13-gotchas.md](references/13-gotchas.md) 1） |
| 2 | 插件必须装进 profile 树内 | 树外解析不到官方包 ⇒ **整棵 profile 起不来**（[13-gotchas.md](references/13-gotchas.md) 6） |
| 3 | 启停覆盖写 profile 层，不写进 bundle 包内 | 产品层不该承载用户偏好（[13-gotchas.md](references/13-gotchas.md) 1b） |
| 4 | 覆盖某行必须重述整块 `config` | patch 是整行替换，不是深合并 |
| 5 | `config.id` 是身份，发布后不改；行 id 用 `preset-<id>` | 老会话按 id 恢复，改了就拒绝恢复 |
| 6 | 改动按改动面取**最窄**证据，并先做负控 | "干净日志"只有在故意弄坏会响亮报错时才算证据（[10-install-and-verify.md](references/10-install-and-verify.md)） |
| 7 | boot 干净 ≠ 功能可用：真调一次工具/命令 | 服务惰性读取，服务名写错在 boot 期看不见 |
| 8 | 资产从安装包解析，不读 profile / preset 目录 | preset 没有自己的目录（[02-profile-and-preset.md](references/02-profile-and-preset.md) §2.6） |
| 9 | 机制带版本号；渠道 / 社区 / 生态现状**只进 12**（时效数据），并写"是什么/怎么用"而不是"最新/N 个" | 无日期的时效断言会烂掉；实测记录不会 |
| 10 | README 只写使用者内容；工程备忘录进 `AGENTS.local.md` / `docs/` | 读者不对，关键信息会被淹掉（Step 6） |
| 11 | 开发实例 = 独立进程 + **持久的私有 `DSH_HOME`**（`~/.dsh-<插件>`，建一次、复用、不删）+ **固定端口**（只挑一次、存进 home、永远复用，避开 3080）；**永不指向 `~/.dsh`**；URL + 测试点交给**用户手动测试** | 每次新建 home 会丢会话；每次换端口会让旧 URL 全部失效（用户以为进程死了）；复用真实 home 会与主 GUI 抢写会话日志（[10-install-and-verify.md](references/10-install-and-verify.md)「本地开发实例」） |

## 何时使用

- 用户想为 dsh 开发新插件（工具、skill 包、MCP server、事件监听、服务、
  命令、prompt、浏览器 UI）。
- 用户要 bundle 插件 / 纯 cordis 插件的脚手架 / 示例 / 模板。
- 用户要**新增一个 Agent 模式（preset）**，或把一套工具 + 提示词做成**垂直
  Agent 产品**（读 [03-vertical-agent-recipe.md](references/03-vertical-agent-recipe.md)）。
- 用户要安装 / 分发 / 升级插件，或理解 profile 层栈与重启边界（读
  [02-profile-and-preset.md](references/02-profile-and-preset.md)）。
- 插件挂载失败且原因是 entry 契约或安装通道。

## Step 0：选择插件形态

按插件分发什么选官方路径。`dsh` 字段 strict——能力面声明：

| 需求 | 官方路径 | 安装通道 | 起点 |
|---|---|---|---|
| 纯 skill 包（无代码） | skill 走**文件系统发现根**（`dsh.skills` 字段在当前基线无消费方，见 [04-plugin-contract.md](references/04-plugin-contract.md)） | 复制/链接进发现根（`<项目>/.dsh/skills`、`.agents/skills`、`$DSH_HOME/skills`、`~/.agents/skills`） | Step 2（skills） |
| MCP server | **不是包 manifest 字段**：CLI 随附 `@deepseek-ai/dsh-mcp-client` 供 **patch 层**使用，默认禁用（每条服务器命令是 agent 沙箱之外的受信任可执行代码） | patch 层 config | `apps/cli/reference/README.md` |
| Node 工具 / 事件 / 服务 | npm 包 + Cordis entry（`main`） | profile insert 行 | Step 3 |
| Node + 浏览器 UI | npm 包 + Cordis entry + `dsh.client` | bundle | Step 3 + 4 |
| 带组合层（多行 insert/config/disabled 随包分发） | npm 包 + `dsh.bundle` | bundle 层栈 | 读 `references/05-bundle-plugins.md` |
| **新的 Agent 模式（preset：工具/人设/技能组合）** | npm 包 + `dsh.bundle`，patch 里 insert `preset-<id>` 行 | bundle（`patch` 可为数组） | 读 `references/02-profile-and-preset.md` §2 |

按三个判据选形态，**按顺序问**：

**判据 A —— 有代码吗？**
纯 skill（无代码）走文件系统发现根；MCP server 是 **patch 层配置**，不是包 manifest 字段；
其余都是 npm 包 + Cordis entry。

**判据 B —— 需要组合层吗？** 看包是否声明 `dsh.bundle.patch`。
声明 = 一层组合 patch（多行 insert/config/disabled，`patch` 可为数组）→
`dsh plugin --profile web add` 进层栈；无声明 = 单个 Cordis 插件 → profile
`cordis.patch.yml` 写一行 insert。

**先问一句：是原型还是产品？** 只给本机用、还在试形态 → 直接用产品内的**创造模式**（`cordis` preset）做 bundle 并 `install_bundle`（见 [05-bundle-plugins.md](references/05-bundle-plugins.md)「创造模式」）；要分发、要维护、要给别人装 → 按下面判据走仓库路径。

**判据 C —— 给谁用？** 只给宿主加服务 / 界面 → **Host 行**即可；要影响 **Agent 看见什么**
（工具、人设、技能）→ 落在 **preset 行**（web 的内置工具行就是按模式拆开的）。
装完不等于新模式出现：**新增模式 = 新增一条 `preset-<id>` 声明行**。

三者都按目标运行时的配置协调 / HMR 能力**实测生效情况**，不预设必须重启。
带 UI 的独立插件两类皆可（自渲染 client 在 bundle 里照常工作）——选型看是否需要组合层，而非 UI 形态。

## Step 1：仓库布局

`my-plugin/` 根即 npm 包（bundle 形态包根 = 仓库根）：

```
my-plugin/
├── package.json            # name/version + main/exports + icon + dsh.bundle/dsh.client
├── icon.svg                # 必需：Plugins 页的插件标识（非功能截图）
├── cordis.patch.yml        # dsh.bundle 声明的组合层（insert 挂载自身）
├── index.mjs               # Node half 入口：完整 Cordis 插件（main/exports["."]）
├── client/  lib/client.js  # client bundle 源码 / 构建产物（dsh.client 通道）
└── scripts/                # 门禁 + 生成器（可选）
```

## Step 2：`package.json` + 能力面

按 `references/05-bundle-plugins.md` 与 `references/04-plugin-contract.md` 的模板。
关键决策：

- `dsh.bundle.patch` → `cordis.patch.yml`（组合层，含 `- insert: - id: <自身> name: <包名>`）
- `dsh.client` 声明（platform web）+ `exports["./client"]`（有 client half 时）
- `main`/`exports["."]` 指向 Cordis entry（`name`/`inject`/`Config`/`apply`）
- `dependencies`/`peerDependencies`/`devDependencies` **三处都留空**——官方包由挂载环境注入（理由与本地 link 配方见 [13-gotchas.md](references/13-gotchas.md) 1）；唯一例外是 schema 要用 dsh 的 fork
  `@deepseek-ai/schemastery`（公共 `schemastery` 没有 `.volatile()`），装成普通 `dependencies`
- `inject` 声明 `ctx.get` 用到的全部服务（`webServer`/`jobs` 等）。**严格注入两个方向都会出事**：
  - **声明了但宿主没有**（名字写错、或该服务已被新 rc 移除）→ 条目**永久 pending**，
    boot 日志只有一行 `warning: 1 entry did not activate`，该插件的功能与 UI 一起消失；
  - **用到了却没声明** → apply 开头即抛 `cannot get property without inject`。
  两种都**照不出来于 mock ctx 单测**——必须真启动一次 profile 才算验证过（Step 5）
- 服务名与槽名以**当前基线**为准逐条核实：官方会跨 rc 改名（[13-gotchas.md](references/13-gotchas.md) 7、8）
- **包显示元数据**（Plugins 页里的标题与一句话描述）：`locale/en.json` + `locale/zh.json` 的
  `meta.title` / `meta.description`，并把 `"./locale/*.json"` 同时加进 `exports` 与 `files`
  ——少了 `files` 发布出去就丢（写法与回退链见 [08-i18n.md](references/08-i18n.md) §2）

### Skill 包（`dsh.skills`）与 MCP server（`dsh.mcpServers`）

声明写法（`dsh.skills` 相对路径列表 / `dsh.mcpServers` 的 server-id → 启动
配置映射）与 SKILL.md 写法规范（frontmatter / 正文模式 / <500 行，遵循
make-skill）见 `references/04-plugin-contract.md` 对应小节——不要发明竞争格式。

## Step 2b：绘制插件图标（必做）

每个 npm 插件都要绘制并验证 Plugins 页图标，包括没有 client half 的插件；
仅走文件系统发现的纯 skill 包不适用。**这是交付要求，不是运行时必填字段**。

- 先看几个**已发布插件的图标**（官方 Plugins 页里的、或你自己别的插件），按其简洁风格绘制
  能表达本插件功能的 SVG。观测样式是 **36×36 透明画布、主体约在 8..28、少量蓝/青渐变**，
  不是硬 API；不要照搬别的插件身份。用户指定的标记优先，例如 autofork 的 `⑂` 仅是该插件
  的标记，需画成路径/几何形状，不把它变成所有插件的模板。
- 使用显式填色/描边；SVG 作为 `<img>` **不继承宿主 `currentColor`**。
  不用字体字形、外链资源或脚本；不要把 README 功能截图当作插件图标。
- 在 **`package.json` 顶层**写 `"icon": "./icon.svg"`，**不是 `dsh.icon`**；图标限 **SVG / PNG / JPEG / WebP、≤ 256 KiB**，路径相对 manifest 且 realpath 后必须仍在包内；
  `files` 打包白名单包含图标，并保留 `exports["./package.json"] = "./package.json"`。
- 完成前读 [10-install-and-verify.md](references/10-install-and-verify.md)「插件图标：机械验证与视觉验收」，
  验证打包结果、真实 Plugins 图片加载，**并实际查看渲染图像**；只证明文件存在不算完成。

## Step 3：Node half——Cordis entry

`index.mjs` 导出完整 Cordis 插件（`name`/`inject`/`apply`）。用 `defineTool`
注册工具；服务/事件/命令/prompt 是完整 Cordis，无需声明。依赖解析是官方
运行时的职责（`@deepseek-ai/*`、`cordis`——profile pnpm 闭包注入，勿声明）。
在 `ctx.effect()`/`ctx.on()` 内注册，disable 时清理。

**检查点**：entry 可解析；工具已注册；inject 声明完整；**在真实 profile 里启动过一次**
（boot 不报 `plugin tree failed to load`）——缺 `inject`、服务名写错这类问题只有真启动才暴露。

## Step 4：Client half（可选）——自渲染

带 UI 的插件声明 `dsh.client`（platform web）+ `exports["./client"]`，client
bundle 经 `__ModuleLoader__.load({id, factory})` 注册（factory 返回
`{name, apply}`，由 client 内核挂载时调用 `apply(ctx)`）。自渲染 DOM 逻辑
放 `apply` 内——**与填官方 hole 正交**（自渲染跑 bundle 照常，参考实现 `vlln/whale-girl`）。

`dsh.client` 的其余字段：`inject`（声明消费的其他 client 模块）、**`external`**
（声明本行消费的 client 包，client-modules 用它排模块图顺序；**不得声明自己**——同包自引用会抛
`a row must not declare its own package in dsh.client.external`）。client 包用共享构建形态：
extends `tsconfig.base.client.json` + 共享 tsdown preset（`packages/client/tsdown.client.ts`）。

构建：esbuild/tsdown CJS 输出 + 外层 `window.__ModuleLoader__.load` 包装（对齐
官方 preset 的 banner/footer 模式）。

**画 UI 之前先读 `references/06-ui-style.md`**：官方 `docs/web-styling.md` 与 `docs/ui-radius.md`
规定了样式归属与圆角标准，那份 reference 把它们翻成插件作者可照抄的形式——三/四层 token、
配色速查、圆角按角色选档、字体阶梯、阴影与浮层材质、焦点与滚动条，以及**可直接复用的官方控件
目录（逐组件 props / 几何 / token / 选型判据）**、**`/` 菜单命令行的行外观（label / icon）**（含宿主命令没有官方
入口时的贴面做法、label 的搜索键作用与降级契约，§10.7）。两条最常被违反的：插件**不写死颜色、不定义自己的
深色主题**；**库里有控件就不要抄第二份**（这是硬约定，不是偏好）。

**UI 文案先分流再动手**：浏览器 UI 的文案走**客户端字典**（`ctx.locale.register(ns, { zh, en })` +
slot 注册项的 `locale` 座位拿 `t`），Plugins 页的插件标题/描述走 `locale/*.json`，
宿主产生的用户可见文本官方自身留英文（要本地化读 `locale` 设置命名空间的 `preference`）——
判据表、键的写法（点分小写）、改造清单与验证见 [08-i18n.md](references/08-i18n.md)。
**模型可见文本（tool/schema description）不是 UI 文案**，不要翻译。

**填官方设置面（可选）**：Node half 导出 `Config` schema 声明命名空间（= 条目 id），
client half 把配置页注册进 Plugins 页的槽（自有 bundle 用 `plugins.bundle.config`，
key = 包名）；live 字段标 `.volatile()`，保存即生效、不重挂载。完整契约
（槽选择、读写语义、四处同名不变量、验证步骤）见
`references/07-settings-panel.md`；实测参考实现 `vlln/whale-girl` 的配置卡片。

**检查点**：`__DSH_BOOT__` 含 client 行；`/plugins/<id>/client.js` 200；无
`loaded without registering` 报错。

## Step 5：安装与验证

安装通道（写法细则见 `references/10-install-and-verify.md` 与
`references/05-bundle-plugins.md`）：

- **bundle**：`dsh plugin --profile web add <包路径/git 源/npm 包/tarball>`——声明 `dsh.bundle`
  的包；安装后的生效检查见下述引用，不预设必须重启。
- **纯 cordis**：`dsh plugin --profile web add <包>` 装依赖 + profile
  `cordis.patch.yml` insert 行；启用配置热协调时可实时挂载。
- **四条包渠道**（官方 [publish 文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/develop/basic/publish.md)）；市场索引是**发现渠道**，不托管包（[12-ecosystem.md](references/12-ecosystem.md)）：
  ① 产物入库 + git 源（真一行）② `prepare` 脚本 + 用户为该包放行 `allowBuilds`
  ③ npm 预构建 ④ `pnpm pack` 出的 tarball（`dsh plugin --profile web add ./x-0.1.0.tgz`）。
  ②的授权语义是**允许该包在安装时于用户机器上执行代码**（不在 agent 沙箱内）——安装说明里要写明并建议钉 commit。

**写安装说明时必须给出用户可直接复制的命令**；验证按改动面与挂载失败排查见 `references/10-install-and-verify.md`。

**开发与每次改动后都起独立实例验证**（用户 2026-10 定调）：新 `DSH_HOME`（默认不碰 `~/.dsh`）
+ `dsh web --port 0`，URL 与测试点交给**用户手动测试**——不复用用户 GUI（默认 3080）与真实
`~/.dsh`；交接前先确认插件真挂上了（**URL 能打开 ≠ 插件在**，见 [10-install-and-verify.md](references/10-install-and-verify.md)「本地开发实例」）。

**三条硬规矩**（该文件详述，这里先记住结论）：

1. **boot 干净 ≠ 功能可用**——依赖解析失败、服务名写错在 boot 期看不见（服务惰性读取），
   **必须真调一次工具/命令**；
2. **先做负控**——装一份故意弄坏的副本，确认日志会响亮报错；只有负控响过，"干净日志"
   才算证据；
3. **mock ctx 单测不能替代真实装载**——它不施加严格注入门禁，缺 `inject` 的启动即崩
   照不出来。

**零依赖包的安装说明只给 git 源**：本地目录装在 profile 树外解析不到官方包（[13-gotchas.md](references/13-gotchas.md) 6），只用于开发自测且要先 link SDK。

## Step 5b：交付检查与发布

做完插件先过 **交付检查清单**（与是否公开无关），再决定要不要公开分发：

- [ ] 入口 / `dsh.bundle.patch` / insert 行与包名同源；依赖三字段为空
- [ ] 图标已绘制并**实际看过**渲染结果（Step 2b）
- [ ] 带 UI 时过了 [06-ui-style.md](references/06-ui-style.md) 的交付前视觉自检
- [ ] 安装冒烟含一次**真实工具/命令调用**，且做过负控；改动已在**独立实例**（新 `DSH_HOME` + `--port 0`）里跑过，URL + 测试点已交给用户手动测试
- [ ] README 只含使用者内容 + `## 兼容性` 节 + `## 插件管理` 节

完整清单与公开发布（description / topics）见 [11-publish.md](references/11-publish.md)；
市场、社区与曝光渠道见 [12-ecosystem.md](references/12-ecosystem.md)。

## Step 6：开发规范

可维护的插件遵循 `references/09-dev-conventions.md` 的纪律：门禁（自证测试）、
每个非平凡改动的决策记录、生成物不手改、首次环境行为沉淀为环境事实。

**README 规范**（make-skill spec + 用户 2026-09 定调）——**骨架直接抄 [templates/README.md](templates/README.md)**，按注释删块、替换占位符。高星插件的四个可吸收写法：

- **头部**：社媒预览图 + 语言互链 + 徽章（npm / stars / dsh 版本），可选但很吃第一眼；
- **安装先 GUI 后 CLI**：有 Plugins 页入口就先写「Plugins → 添加插件」，再给 CLI 与升级命令，并写清"装不上时"的典型症状；
- **"用起来"用面×截图×问题表**：每个界面/页签/命令一节，配一张图 + 一张「它回答什么问题」的表（多状态分开截图，不拼图）；
- **安全与数据**单独一节：权限、外发、凭据放哪（有网络/执行/写文件时必写）；
- **宿主矩阵**：web / 官方 Desktop 分开写（安装互不相通），跨大版本给"宿主 × 插件版本"对应表；
- **装好之后怎么确认** + **卸载命令**：各 2–3 行，比让用户猜省事；
- **dsh 生态徽章**（可选）：awesome-dsh-plugin、dsh-plugin.org `listed`、dshfind、Hub——**被收录后才放**。

**README 的读者是「用这个插件的人」，不是维护者。** 一条内容留不留，就看
"用户拿它做决定"吗（装不装、怎么配、会不会踩坑）——只有"改这个插件的人"才用得
上的，一律移走。README 变成工程备忘录是**最常见的跑偏**：信息都真、都重要，但
读者不对，真正需要的那几句被淹掉（反例：某插件 README 602 行，安装节在第 573 行）。

- **写**：这是什么（一句话方案）；**为什么需要它**（动机——要解决的具体问题、用户
  当前不得不忍受什么、这个方案把什么交给了工具）；怎么装（含"装完要重启"这类生效
  条件）；用起来是什么样（用户可见的行为——界面多了什么、列表里的名字长什么样、
  注入行怎么呈现）；能力面表格；参数与环境变量；**已知限制**（用户会撞上的边界、
  安全注意事项）；`## 插件管理` 固定节；许可。
- **动机要写"用户视角的痛"**，不是设计目标：用"你现在必须怎样、代价是什么"说话，
  并**讲清与相邻方案的区别**（官方能力 / 同类插件，谁发起、用户要做什么）——
  这是使用者判断"要不要装"的主要依据。
- **边界要诚实**：说清它**不解决什么**（例如"某种等待是问题本身的性质"）。只写
  好处的 README 在真实使用里会被立刻发现，代价比少写一段大。
- **不写**（工程备忘录）：内部事件/API 挂钩点、实现范围与机制表、验证证据与测试
  计数、E2E 台怎么跑、设计取舍的来由、踩坑与事故复盘、与官方包内部的契约。
  它们写到**别处**——仓库本地 `AGENTS.local.md`（不入库）、代码注释，或仓库内
  单独的 `docs/engineering-notes.md`；README 只在安装节留**一句**指针。
- **能力面**用表格：每个能力面一个表、每项一行一句话；人扫描表格决定用什么，
  细节留在各项自身文件。
- 自检：README 超过 ~200 行基本已经跑偏，逐段问一遍"这段的读者是谁"。

**`## 兼容性` 节（必含，随每次更新核对）**：用户装之前只有这一节能回答"我这版 dsh 能不能用"。
写**实测过的 dsh 版本 + 验证日期**，并承认没测过的边界；不写"latest / 要求最新版"这类会立刻过期的断言
（上游一个月走几千 commit）。取版本号：`dsh --version`，或官方仓库 tag `dsh-v<版本>`。

```
## 兼容性

| dsh 版本 | 状态 |
|---|---|
| `0.2.0-rc.2` | ✅ 已验证（2026-10-15） |
| 其它版本 | ⚠️ 未验证——升级 dsh 后若 <用户可见症状>，多半是 <一行原因> |
```

- **与 `peerDependencies` 同源**：声明了官方 peer 范围（见 [05-bundle-plugins.md](references/05-bundle-plugins.md)）
  的插件，README 写的"已验证基线"必须是那个范围的**下限**（例：peer `^0.2.0-rc.2` ⇄ README 写
  `0.2.0-rc.2`）——两处不一致时用户会照 README 装上却被宿主预检整行禁用。多支持线插件
  按 [DSH-better-sidebar](https://github.com/vlln/DSH-better-sidebar) 的"按你的 dsh 版本选插件版本"
  表写（每行：dsh 范围 / 安装命令 / 插件版本）；`workspace:^` 这类"跟随运行时"的 peer 不该配一张版本表。
- **每次更新插件后同步核对本节**：改了机制挂钩点、client 契约或设置面就重新实测，把新基线
  与日期写进来（旧版本行保留或改标"未验证"，不要留着假断言）；纯文案/内部重构不动它。
- 这一节只放**面向用户**的结论（能用/不能用、症状）；验证过程与证据仍归
  `AGENTS.local.md` / `docs/engineering-notes.md`。

**标题格式**（强制）：
- `<h1 align="center">插件名</h1>`——**居中**；用仓库/插件名（如
  `whale-girl`、`loop`），**不加 npm 前缀**（不要写 `@vlln/dsh-loop`
  或 `@scope/name` 作为标题）。
- 标题下加 `<p align="center">` 一句话价值主张（是什么 + 主要收益）+ 可选
  徽章（badgen：license/format）。

**图片要求**（若有 UI 或可演示的行为）：README 应含至少一张功能图片——
状态/界面/效果截图或 gif。Agent 在验证环境截取或提示人工截取后放入
`docs/` 并引用；图片路径相对仓库内（如 `docs/preview/*.gif`），md-links
可解析。纯 CLI 工具无 UI 可豁免，但 README 应有可演示的示例输出。

**能力面表格**：

- **Skills**（恒有）：`| Skill | 作用 |`——每个 SKILL.md 一行。
- **MCP servers**（若含 `dsh.mcpServers`）：`| MCP | 说明 |`——每个
  server 一行（名称 + 暴露什么）。
- **Tools**（若注册工具）：`| 工具 | 说明 |`——每个 `defineTool` 注册一行。

适用于任何带 skills/MCP/tools 的仓库。

**推荐管理章节**（README 固定含一节，向用户推荐插件管理方式）：插件装/卸/启停用官方 CLI
与官方 Plugins 页，不要在 README 里引导用户手改 profile 配置：

```
## 插件管理

装/卸/启停用官方 CLI：`dsh plugin --profile web add|remove <包>`；已装插件在**侧边栏 Plugins 页**
里查看与配置——每个插件自己的配置页挂在那个包页上（Settings 里的「插件」只是只读清单，改不了配置）。
```

每个按本 skill 产出的插件 README 都带此节（安装说清通道与重启条件即可）。

**进入迭代期时读 `references/09-dev-conventions.md`**。

## 坑（Gotchas）

高频坑（官方包不可单独安装、ESM 缓存、严格注入、宿主 CSS 覆盖、entry 契约
失败时机等）见 [13-gotchas.md](references/13-gotchas.md)（唯一清单）；**先读它再动手**。
手册索引见上文 §2；参考实现（`whale-girl` / `dsh-loop` / 薄控制台）见 [12-ecosystem.md](references/12-ecosystem.md) §E。

## 版本与权威来源

**机制契约的版本权威是官方文档**（随基线更新，优先于本 skill 的复述；发现冲突时以官方为准并回来更新本 skill）。
⚠️ 但**官方文档与源码 checkout 跟的是 master，可能领先于用户实际安装的 rc**——两者冲突时以**安装的运行时**为准，并把差异与版本号写回来（实例见 [13-gotchas.md](references/13-gotchas.md) 9）。

| 主题 | 官方位置（`deepseek-ai/deepseek-harness` 仓库内） |
|---|---|
| 插件配置 / 打包 / 安装 / 发布 | `docs/user/develop/basic/config.md`、`basic/publish.md`、`basic/tool.md` |
| 插件生命周期（服务 / 事件） | `docs/user/develop/framework/*` |
| 运行时元数据、动态 Cordis | `docs/user/develop/practice/dynamic-cordis.md` |
| 新增包 / 设置卡 | `docs/cookbook/adding-a-package.md`、`adding-a-settings-card.md` |
| 层优先级 / flag / profile 机制 | `apps/cli/reference/README.md`（本 skill 的整理见 [02-profile-and-preset.md](references/02-profile-and-preset.md)） |
| Web UI 样式（token / 圆角 / 控件目录） | `docs/web-styling.md`、`docs/ui-radius.md`、`packages/client/ui-theme/src/styles/*`、`packages/client/ui-primitives/README.md` |
| 子系统地图 | `docs/subsystems/*.md`（extensions / skills / web-client / tools …） |
| **产品内造插件（创造模式）** | `@deepseek-ai/dsh-agent-preset/skills/`：`cordis-plugin-development`（写插件/页面/设置卡）、`editing-cordis-compositions`（写/改 preset）、`cordis-composition-reference`（patch 方言与可装包清单）、`agent-experience`（工具描述与上下文加载）——**只在该 preset 挂载**，内容随运行时版本 |
| 插件市场 / 发现 | `docs/user/guide/plugin-market.md`（本 skill 的整理见 [12-ecosystem.md](references/12-ecosystem.md)） |

**权威优先级**：安装的运行时（`lib/types` + 创造模式里那四份 skills）→ 官方 docs → 本 skill 的整理。
本 skill **不复制**这四份 skills 的模板与流程：它们随安装发布、天然对版；本 skill 负责仓库化、分发、
验证与纪律（分工表见 [05-bundle-plugins.md](references/05-bundle-plugins.md)「创造模式」）。名字与路径
以安装包 `@deepseek-ai/dsh-agent-preset/skills/` 为准，跨版本可能改名。

### 溯源：一条事实该去哪儿核

**每个 `references/*.md` 开头都写明「来源」**（官方文档路径 / 实测基线 / 本 skill 自定），新增 reference 照此办理；
读 reference 时先看那一行，就知道该不该信它、以及冲突时去哪儿找权威。

核查次序固定为 **安装的运行时 → 该版本的源码 tag → master**：

1. **安装的运行时**（最权威，本 skill 的口径基准）：官方 client 包随 CLI 一起装，**编译后的组件 CSS 与 token 表都在里面**：

   ```sh
   D=$(dirname "$(dirname "$(readlink -f "$(command -v dsh)")")")/node_modules/@deepseek-ai
   grep -o -- '--dsw-radius-[a-z]*: *[^;}]*' "$D/dsh-client-ui-theme/lib/client.js" | sort -u  # token 实际值
   ls "$D/dsh-client-ui-primitives/lib"/*.module.css                                            # 组件的真实样式
   ```

   （`readlink -f` 不可用的老系统：换成 `realpath "$(command -v dsh)"`，或直接看
   `ls -l "$(command -v dsh)"` 的指向手动拼出 `D`。）

   浏览器里还能读**当前生效值**——DevTools 控制台：
   `getComputedStyle(document.body).getPropertyValue('--dsw-alias-bg-base')`。
2. **该版本的源码**（props / JSDoc 这类编译产物里没有的东西）：官方 tag `dsh-v<版本>`——
   `git show dsh-v0.2.0-rc.2:<路径>`（先 `git fetch --tags origin`），或
   `https://raw.githubusercontent.com/deepseek-ai/deepseek-harness/dsh-v0.2.0-rc.2/<路径>`。
   版本号先取现场值（`dsh --version`）。
3. **master**：只在判断"官方接下来往哪走"时看；**不要拿它当插件的行为依据**（[13-gotchas.md](references/13-gotchas.md) 9）。

**本 skill 保留两类官方文档不写的内容**：

1. **发布与生态纪律**——发布检查清单、仓库 description/topics 规则、README 读者规则、门禁与决策记录、安装说明纪律（Step 5b / Step 6）；
2. **实测坑与验证纪律**——`references/13-gotchas.md`（踩出来的领域事实）与 `references/10-install-and-verify.md`（含"负控"这类方法论）。

**新增会话页签前先读** [13-gotchas.md](references/13-gotchas.md) 12：`conversation.view` 各页签**共用**
会话内容区，外壳的左右拖动**宽度手柄**会跟着出现在你的页签上（`[data-width-handle]`，
两条 `col-resize` 竖线）——用「给视图挂稳定 data 属性 + `:has([data-…-view]) [data-width-handle]{display:none}`」隐藏它。

**事实带基线**：本 skill 的实测事实标注核实时的 dsh 版本——插件机制面（04–08、10）按 **0.2.0-rc.2** 核，
其中服务名 / manifest 字段 / CLI flags / locale 与 settings API 已在 **0.2.1-rc.1** 抽查（记录见项目 README）；
preset / profile 两层装配按 **0.2.1-rc.1** 核（[02-profile-and-preset.md](references/02-profile-and-preset.md)）。
其余细节（UI token 数值、槽位几何、0.1.5 时段实例）仍是 0.2.0-rc.2 标注。冲突时以**安装的运行时**为准。

**相邻能力**（本 skill 不展开，需要时读官方文档）：bundle 行可自带 CLI
（`inject = ['cmdlineArgs']` + `parseCmdline`，启动器把同一份不可变参数快照交给每个插件）；
**extensions 子系统**（agent 定义带版本的 Cordis 包并运行其 host 与浏览器两半，`tool-cordis`
查询运行时元数据）；**dynamic Cordis**（运行时写插件）。**profile 与 agent preset 不在此列**——
两层装配、层栈、会话如何选模式见 [02-profile-and-preset.md](references/02-profile-and-preset.md)。

**升级既有插件跨 rc 时**：服务名、槽名、manifest 字段与平台模块导出名都会改，且**旧名字不报错**
（症状是 client 条目永久 pending、Node 侧静默失效）——先读 [13-gotchas.md](references/13-gotchas.md) 7、8、10
的改名清单再动手。
