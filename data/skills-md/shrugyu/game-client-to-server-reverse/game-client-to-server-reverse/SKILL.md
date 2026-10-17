---
name: game-client-to-server-reverse
description: 从游戏客户端（安装包/APK/IPA/EXE 或 dump.cs、lua、usmap、抓包等）反推服务端协议并复现可部署服务端。含阅读路径分派、原理层(primer：三要素/数据包协议/协议表/热更源码)、四阶段路线图(workflow-roadmap：静态分析→建工具+登录链→重定向→补包循环→清单迭代)、11 种反推方法选择器（含内联服务端路线）、接口清单提取器（tools/）、协议规格模板(protocol.spec.yaml)、wire 级定点改写（不等 schema 齐就能跑）、客户端地址来源清查、三轴状态与验收体系、发布运维清单、进度清单(TRACKER.md)、登录链条与功能清单模板。覆盖：账号登录注册、房间匹配、战斗、掉落物资、抽卡、充值与邮件、部署(本地/服务器/Termux/Windows)、客户端对接、闭环验证；并支持 Unity(IL2CPP/Mono/Lua)、Unreal(UE4/UE5)、Cocos2d-x/Cocos Creator(JS/Lua 热更)、C#、AS3、Java、JS 等客户端；含进服后的 Live 运营手册；并含「内联服务端」路线（客户端进程内合成响应、运行时对象合成与字段发现、平台 SDK 登录态复用与目录服/区服两段准入）。
license: 仅限自研 / 已授权 / 离线单机目标用于互操作性研究与本地化部署；不得用于未授权破坏性测试或商业化他人资产（边界详见 README.md）
compatibility: 需要 Python 3.10+（pip 可装 flask / PyYAML / aiosqlite）；参考服务端可在本机、Termux、WSL2 或 Windows PowerShell 运行；联网可选（查资料、下载工具时）。跨平台：android / ios / windows / linux。
metadata:
  version: "2.0"
  platforms: "android, ios, windows, linux"
  spec: 遵循 Agent Skills 规范（name 与父目录名一致；SKILL.md < 500 行；references 按需加载）
---

# 游戏客户端 → 离线本地化 Skill

> **定位**：把「只有客户端」的游戏，还原出「服务端协议 + 本地离线服务端」，并让原版客户端**本地离线运行**。
> **适用**：互操作性研究、本地离线化 / 离线版建模、协议文档化、安全评估、游戏存档研究。
> **边界**：仅用于自研、已授权或离线/单机目标。禁止未授权破坏性测试与商业化他人资产。

> **版本 v2.0**（完整变更历史见 `README.md`）。2.0 较 1.x 新增：**原理层** `primer.md`、**四阶段路线图**
> `workflow-roadmap.md`、**反推对象地图** `server-architecture-basics.md`、**重定向落点（含 Xposed/LSPatch 模块）**、
> 复活 / 本地离线项目合集、登录链/功能清单模板、全库去除 emoji、跨模型阅读优化，并对 SKILL.md 大幅瘦身。

---

##  阅读协议（任何模型通用：GLM / DeepSeek / Claude / …）

> 本包 = 1 份长文档（`SKILL.md`）+ 37 篇 `references/` + `templates/` + `tools/` + 参考实现 `server/`。
> **不要一次读完**——会耗尽上下文，结果在没读完的地方开始猜。
> **注意：多数模型不会自动加载 references，必须显式打开文件。**
> **先读 `references/usage-policy.md`（使用守则与限制）——确认用途合规、不越界，再动手。**

**标准三步（照做即可）**：
```
1. 先读完本文件 §0（方法选择 + 铁律 + 工作流 + 补包循环）—— 必读核心
2. 打开 references/reading-path.md → 按你的任务类型拿到 3~5 个文件的阅读顺序
3. 按顺序打开并读完那些文件 → 再动手
收工前：打开 references/reading-path.md §2，过一遍「收工前检查」
```

**上下文很少时**（只能读 1~2 篇），按此优先级取：
`SKILL §0` → `reading-path.md` → `wire-level-patching.md` → `closure-verification.md` → `client-address-sources.md`

> 一句话：**SKILL.md 是导航，references 是正文**。先读导航，再按需读正文。

---

## 阅读地图：三条主线，先认清自己在哪条

> 这个包讲三件事。**先确认自己卡在哪条主线，再去读对应文件**，不要混着读。

| 主线 | 回答的问题 | 先读 | 关键产物 |
|------|-----------|------|---------|
| **A. 原理** | 「到底在反推什么？」 | `references/primer.md`、`references/server-architecture-basics.md` | （认知：三要素 / 协议表 / 热更源码 / 反推对象地图） |
| **B. 路线** | 「先做什么、后做什么、在哪验收？」 | `references/workflow-roadmap.md` | `login-chain.md`、进度 |
| **C. 方法** | 「用哪个手段取证？」 | `references/methods.md` | 选定方法 → `project-profile.yaml` |
| **D. 规格** | 「怎么把结论固定下来？」 | `references/protocol-spec.md` | `protocol.spec.yaml`（唯一事实来源） |

**一句话**：A 讲「找什么」，B 讲「什么顺序」，C 讲「怎么找」，D 讲「怎么记」。

- **新手 / 第一次接触某客户端** → 先读 A（`primer.md` + `server-architecture-basics.md`），再看 B。
- **知道自己要干什么、只是缺手法** → 直接看 C（`methods.md`）+ §0.0。
- **已经拿到证据、要落盘** → 直接看 D（`protocol-spec.md`）。

---

## 0. 本 Skill 的定位：通用适配器，不是固定方案

**核心认知（先读三遍）**：

> 这个 skill 里附带的任何代码（`server/`、`templates/`、`examples/`）都只是**参考实现**，
> **不是**对某个游戏的答案。每个游戏的引擎、传输、封装、加密、序列化、消息号、字段布局
> **都不一样**。AI 必须先**读取用户实际给的项目**，产出**协议规格（Protocol Spec）**，
> 再据此**生成或改造**服务端。

### 0.0 第一步：选对方法 （最容易做错的一步）

> **方法选错 = 后面全白干。** 完整方法论见 `references/methods.md`。

**先回答 3 个问题**：

1. **有什么？** `PKG`(只有安装包) / `CAP`(抓包) / `SRC`(源码或反编译产物) /
   `RUN`(能运行) / `DBG`(能注入) / `MANIP`(能改客户端或代理) / `REF`(有同类实现)
2. **要什么？** `DOC`(只要文档) / `FLOW`(跑通主流程) / `FULL`(完整服务端) / `PATCH`(改客户端)
3. **什么约束？** 客户端保护 / 时间 / 权限

**十一种方法速览**（详见 `methods.md`）：

| 代号 | 方法 | 何时用 |
|------|------|--------|
| M1 | 白盒源码法 | 有 `SRC` → **首选** |
| M2 | 黑盒抓包法 | 有 `CAP` → 通用 |
| M3 | 灰盒 Hook 法 | 有 `RUN`+`DBG` → 破加密 |
| M4 | 辅助 Artifact 法 | 有 `.proto`/`.usmap`/SDK → 一步到位 |
| M5 | 代理透传+逐接口替换 | 有 `CAP`+`MANIP` → **最稳落地** |
| M6 | 差分探测法 | 定字段 |
| M7 | 回放/录像法 | 有录像 → 战斗协议 |
| M8 | 已知实现移植法 | 有 `REF` → 抄作业 |
| M9 | 自环法 | 起桩看客户端要什么 |
| M10 | 穷举校验法 | 兜底（优先 M3） |
| M11 | 内联服务端法 | 有 `RUN`+`DBG`/`MANIP` 且可单机化 → **不起外部服务端** |

**默认路线**（不知选什么就用它）：
```
M1/M4（有源码就抄）→ M2+M3（拿明文）→ M6（定字段）→ M9（跑通连接）
→ M5（透传+逐接口替换）→ 闭环验证
```

> **另有一条主干分叉**：目标可单机化 + 客户端能注入/能改 → 走 **M11 内联服务端**（`inline-server.md`），
> 传输 / 封装 / 加密层**不必还原**。先判分叉，再选方法。

> 注意: 现实中都是**组合使用**（如 M1+M6+M5）。
> 选定后记进 `project-profile.yaml` 的 `method` 段；发现更好路径可**中途切换**。

### 0.1 五条铁律

1. **证据驱动，不臆测**：所有结论必须来自用户项目里的实际证据（dump.cs / lua / 抓包 / SDK / 资源文件 / 客户端行为）。
   没有证据 → 标注为「假设」并写进 Spec 的 `unresolved` 列表。
2. **先产出规格，再产出代码**：中间必须有一个**语言无关的协议规格文件**
   （见 `references/protocol-spec.md` 与 `schema/protocol.spec.yaml`）。
   代码是从规格派生出来的，换游戏 = 换规格，不是重写一堆散代码。
3. **闭环验证**：服务端必须能让**原版客户端**跑通到某个状态（握手/登录/进场景），否则推断就是错的。
4. **不把「能跑」当成「跑通」**：端口在 listen、自环脚本报 `OK`、日志打了 [x]，
   **都不是**闭环证据。宣布成功前必须逐条排除假阳性 →
   **见 `references/closure-verification.md`**（接手别人项目时尤其必读）。
   内联路线另有一套判据：**界面截图不算**，要看网络 / 状态层的完成点 → `inline-server.md` §6。
5. **三件事分开记**：「服务端实现了」「自动测试覆盖了」「客户端验收了」。
   用一个状态列会掩盖后两项 → **见 `references/verification-and-status.md`**。
   不支持的输入要 **fail closed**，不要猜一个值。

### 0.2 双证据链

任何字段结论 = **流量证据**（抓包里字节变化） + **代码证据**（客户端里的结构体/序列化代码）。
单侧只算假设。

### 0.3 四层剥离（先分层，再解字段）

不要一上来抠某个字节。先弄清
`传输层 → 封装层 → 加密/压缩层 → 序列化层`，每层剥离后再看内容。

### 0.4 自适应工作流（本 skill 的主干）

> **输入可能是零**：如果用户只给了一个安装包（apk/ipa/exe），先走
> `references/from-installer.md` 的**自举流水线**把证据造出来，再进入下面的步骤。

```
[第0步] 读取输入
   ├─ 只有安装包 ? ──▶ references/from-installer.md
   │    解包 → 判引擎/语言 → 自产 dump.cs/dll/lua/资源 → 抓包 → 动态 dump
   └─ 已有 dump/lua/抓包 ? ──▶ 直接进第1步
        ↓
[第0.5步] 建立工作区契约 → 在项目根放 AGENTS.md（边界/目录分区/验证命令）  ← templates/AGENTS.md
        ↓
[第1步] 产出「项目档案 project-profile」              ← references/adaptation.md
   扫描目录/文件，识别引擎、语言、网络库、资源格式、已知工具产物
        ↓
[第2步] 证据清点 → 证据清单 evidence-inventory
   每条证据：来源、类型、能得出什么结论、置信度
        ↓
[第3步] 决策引擎 → 逐层决策（引擎/传输/封装/加密/序列化/架构）  ← references/decision-tree.md
   每个决策点都有"若…则…"的分支，禁止默认套用参考实现
        ↓
[第4步] 产出协议规格 protocol.spec.yaml                     ← references/protocol-spec.md
   语言无关，含 opcodes / frames / crypto / serialize / state_machine / client / subsystems
        ↓
[第5步] 由规格生成/改造服务端（多语言参考）                   ← references/codegen.md
   选一个最贴近目标协议的语言；参考实现只提供"套路"，不提供"答案"
        ↓
[第6步] 平台部署（端游/手游/服务器）                         ← §14
        ↓
[第7步] 客户端对接 + 闭环验证                                 ← §8/§9
```

> **可选分叉（M11 内联服务端）**：若目标可单机化且客户端能注入 / 能改，可跳过传输与加密层的还原，
> 直接在客户端进程内合成响应 → `references/inline-server.md`。

**换个视角看同一件事——四阶段路线（见 `references/workflow-roadmap.md`）**：
```
阶段0 静态分析（清点线索） → 阶段1 建工具+登录链文档 → 阶段2 重定向（让请求到达本地离线服务端）
→ 阶段3 补包循环（上游→下游，客户端能走到下一步才算通） → 阶段4 功能清单迭代
```
> §0.4 是"**按产物**推进的流水线"，四阶段是"**按顺序+验收**推进的路线图"，两者是同一件事的两种记法。
> 不确定从哪下手时，先看 `workflow-roadmap.md` 的全景图。

### 0.4b 补包循环 （进游戏阶段的核心工作模式）

> 这是**"让客户端一步步前进"的唯一主线**。四阶段的**阶段 3** 就是它。
> 前两步（静态分析、重定向）都只是为它铺路。

**方向：从【登录链最上游】往下游补回包**

```
① 先回【服务器列表】     ← 地址来自这里
② 再回【登录握手】       ← 鉴权 / token / hash
③ 最后补【游戏需要的数据】← 角色 / 背包 / 任务 / VIP / 签到 …
```

**通过标准：每补一块，以「客户端能走到下一步」为准**

> 不是"服务端没报错"，而是**客户端真的前进了一步**（界面前进 / 状态推进）。
> —— 这是铁律 4「不把『能跑』当『跑通』」在补包阶段的落地。

**出错怎么查：对照报错 + 两侧日志**

拿 `客户端报错`、`网络日志`、`服务端日志` **三边对齐**，判断属于哪一种：

| 症状 | 大概率原因 |
|------|-----------|
| 客户端没反应 / 静默断开 | **格式错了**（帧 / 字节序 / 字段布局 + 长度） |
| 明确报错 / 空指针 | **数据缺失**（少字段、空子消息被省略） |
| 走到了下一步但还是不对 | **逻辑根本没有写**（该给的条件数据没给） |

**里程碑：能进入游戏主场景 = 成功一大半。**

之后**工作流程就只有这一条路线**——不断让用户测试工作区目标，循环：

```
测试 →（看日志）→ 定位 →（改）→ 修改 → 再测试   ↺
```

**收尾：整理【功能清单文档】放到工作区，反复迭代直到基本完善** → `templates/function-checklist.md`。

> 详细版（含三边对齐的排错顺序、假阳性排查）：`references/workflow-roadmap.md` §阶段 3~4。

### 0.5 参考实现的正确用法

| 参考物 | 是什么 | 怎么用 |
|--------|--------|--------|
| `references/primer.md` | **原理层**：三要素（配置/协议/代码）、数据包协议本质、协议号与协议表、热更源码、双证据链 | **第一次接触某客户端时先读**，避免"不知道在找什么" |
| `references/workflow-roadmap.md` | **四阶段路线总纲**（静态分析→建工具+登录链→重定向→补包循环→清单迭代）+ 四层重定向表 | **动手前看全景图**；它把 §0.4 与 M1~M11 串成一条有验收的线 |
| `references/server-architecture-basics.md` | **反推对象地图（逆向视角）**：你在还原哪几类服、网关留下的隐藏层、从包里认 Protobuf/KCP、同步模型决定"要还原多少逻辑" | **判断"你在反推哪几类服、去哪找证据"时读**；避免在网关层迷路 |
| `server/` | 长连接二进制协议的参考实现（Python） | **只借鉴分层结构与套路**，协议参数全部按 Spec 改 |
| `templates/mock_server.py` | 极简单文件桩 | 逆向早期快速验证用 |
| `examples/*.md` | 不同游戏类型的**推演示例** | 看"给定这类证据会怎么决策"，不要照搬结论 |
| `references/cases.md` | **两个真实成功的服务端项目**（Go / Node） | 看真实项目的子系统与取舍，校准自己的方案 |
| `references/client-languages.md` | 各客户端语言的反编译与打补丁 | 先判语言，再选工具 |
| `references/cocos2d.md` | **Cocos2d-x / Cocos Creator 深潜**（.jsc/.lua 解包 / 自加密 HTTP-RPC / 多端口 / 热更 / 语言表还原 / **§H2 进服后的 Live 运营**：note 双层包裹、客户端本地存档合并、双表版本差异、自愈设计、部署纪律） | 目标是 cocos 客户端时必读（另见 `examples/E-cocos2dx-http-js.md` §8 Live 运营阶段） |
| `references/live-ops.md` | **Live 运营手册**（进服后 30+ 子系统按投诉频率排序的补全次序 / 契约反推法 / 自愈设计 / 双表差异处置） | **进服之后**读，与 cocos2d.md §H2 互补、引擎无关 |
| `references/from-installer.md` | **零输入自举**：只有安装包怎么自产证据 | 最常见的入口，必读 |
| `references/reading-path.md` | **最小必读路径**（按任务类型给 3~5 个文件的阅读顺序） | **打开 skill 的第一件事** |
| `references/methods.md` | **10 种反推方法 + 选择矩阵** | **动手前先看**（§0.0） |
| `references/closure-verification.md` | **闭环验证 6 类假阳性 + 检查表** | **宣布"成功"前必看**；接手别人项目时第一条 |
| `references/engineering-practices.md` | **实机跑通项目的工程范式**（fixture 回放 / 具名完成点 / 证据分档 / ADR） | **动手前定策略**；配套 `templates/adr-*.md`、`templates/e2e-*.md` |
| `references/wire-level-patching.md` | **实现层核心**：不依赖 protobuf 运行时的 wire 级定点改写 | **写服务端之前必读**；决定"先跑起来还是先凑 schema" |
| `references/client-address-sources.md` | **客户端地址来源清查**（六类来源 + 落点策略 + 重签后果） | **改包/对接客户端之前必读**；解决"改了 URL 还连官方" |
| `references/verification-and-status.md` | **三轴状态 + 可达性分类 + 测试门禁** | 写 TRACKER / 宣称完成之前必读 |
| `references/release-and-ops.md` | **发布、部署与运营**（配置冻结 / 端口族 / CDN / 备份） | 跑通之后要交付时看 |
| `references/case-il2cpp-ecdh.md` | 真实案例：Unity IL2CPP + ECDH 登录服（进行中） | 看"分层结论怎么写 + 卡点怎么复核" |
| `references/repack-rename.md` | 改包名 / 重打包 / 签名 / 包名派生密钥 | 想产独立安装包时看 |
| `references/inline-server.md` | **内联服务端**：在客户端进程内合成响应（门面三类入口 / 回调投递纪律 / 延迟派发 / 双通路 / 内联版验收与假阳性） | **能注入且要单机化时先读这个** —— 它决定你要不要起外部服务端 |
| `references/runtime-object-synthesis.md` | **运行时对象合成与字段发现**（对象级 schema 自举 / dump 循环 / 填值纪律 / 对象级→wire 级切换） | 走内联路线时必读；也可用来先拿一份可信字段清单 |
| `references/platform-sdk-and-admission.md` | **平台 SDK 登录态复用 + 目录服→区服两段准入** | 大厂手游（第三方平台账号 SDK）登录卡点时读 |
| `references/case-il2cpp-inline.md` | 真实案例：Unity IL2CPP + 平台 SDK 的内联服务端 | 看「不起服务端」这条路怎么走、哪些结论已被证伪 |
| `schema/*.yaml` | 规格/档案模板 | 直接复制填，作为 AI 的中间产物 |
| `extensions/` | **后续拓展（可选）**，不影响核心运行 | 跑通之后再考虑，见 §19 |

> 注意: 反例：直接把 `server/config/config.yaml` 的 `opcode_size=2` 拿去套一个 1 字节消息号的游戏 —— 必错。
> 正确做法：Spec 里写明 `opcode_size: 1`，再改代码。

### 0.6 启动阶段的两把钥匙 

> 来自实机跑通到「主界面」的真实项目范式，详见 `references/engineering-practices.md`。
> **先读这两条，能少走几周弯路。**

**钥匙一：fixture 回放（抓包 → 原样重放 + 定点改写）**

启动时客户端要一次性吃下几十个字段的嵌套状态（角色/背包/任务/VIP/签到…），
纯靠反推字段拼几乎必卡在某个页面。更快的路径：

```
原版客户端连原版服务器 → 抓一次完整启动序列 → 落成 fixture（含方向/消息号/seq/flag/原始 body）
→ 本地服务端按【原始顺序】重放 → 未知字段【原样保留】，只对已确认字段做 wire-level 定点改写
```

**具体怎么实现**（不引入 protobuf 运行时的字段遍历 + splice 替换）
→ **`references/wire-level-patching.md`**（含帧 codec、字段遍历器、
`patch_varint/bytes/string`、"空子消息也要保留"等实测经验）

> 注意: 两个红线：① 不要用「缺字段的伪造对象」代替真实启动数据；
> ② 一个账号的 fixture 带着它的 UID/角色数据，**不能直接发给别的账号**。

**钥匙二：具名「完成点」做验收**

不要写「登录成功」。要写**客户端上的一个可观察状态**，例如：
「收到启动结束消息后进入**主界面**，**不是只保持 TCP 连接**」。
再补一次**强制停止 + 重启 + 重连**，确认状态仍在。

配合使用：`templates/e2e-evidence-template.md`（帧序表 + 主动解释帧长差异 + 重连快照）、
`templates/adr-template.md`（写清「当前不做的事情」与回滚条件）。

---

## 1. 输入分类与预处理

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 2. 阶段一：侦察与引擎识别

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 3. 阶段二：流量获取

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 4. 阶段三：协议分层识别

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 5. 阶段四：客户端静态分析（分引擎）

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 6. 阶段五：字段语义推断

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 7. 阶段六：服务端建模与实现

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 8. 阶段七：部署（本地 / 服务器 / 容器）

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 9. 阶段八：验证与回滚

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 10. 输出物清单（交付模板）

> 详细步骤（命令 / 工具 / 判断 / 常见坑）见 `references/phases-detail.md`。

## 11. 常见坑（速记）

> **完整清单见 `references/closure-verification.md` §附「高频常见坑速查」**。这里只留最要记住的几条：

- **改包顺序**：先"不改包 + 端口劫持"跑通协议，**最后**才改包（动手前读 ）。
- **raw deflate ≠ 加密**：先在 `decision-tree.md §4.0` 做 30 秒快筛，别在错误的加密假设上耗数小时。
- **别把"能跑"当"跑通"**：端口在听 / 自环 OK / 日志打勾都不是闭环证据（铁律 4）。
- **只跑通登录不算完**：状态机未闭环，客户端进场景即崩。

---

## 12. 工具速查

| 用途 | 工具 |
|------|------|
| Unity IL2CPP dump | Il2CppDumper / Il2CppInspector / r2unity |
| Unity Mono | dnSpy / ILSpy |
| Lua 反编译 | unluac / luadec |
| 反汇编 | IDA Pro / Ghidra / Hopper |
| 动态 | Frida / x64dbg / lldb |
| UE 资源 | FModel / UnrealPak / umodel / AesFinder |
| UE SDK/mapping | Dumper-7 / UE4SS / usmap dumper |
| 抓包 | mitmproxy / Charles / Wireshark / tcpdump |
| 协议试解 | protoc --decode_raw / binwalk / ent |
| **接口清单提取** | `tools/extract_interfaces.py`（本 skill 自带） |
| **so 结构 / 依赖 / 符号** | `readelf -d`（NEEDED）、`readelf --dyn-syms --wide`（**FUNC + OBJECT 都要看**）、`strings -a`（找硬编码常量） |
| **APK 编辑 / 资源 / 重打包 / 签名** | MT 管理器（含 MCP：`http://127.0.0.1:8787/mcp`，可 dex/资源/构建/签名一条龙）、apktool、apksigner |
| **ZIP 原样复制重打包** | 本 skill `tools/` 的 repack 脚本（2GB 包秒级，只替换目标条目） |
| **动态调试 / 内存** | Frida、`/proc/<pid>/maps`（看加载了哪些 so） |

---

## 13. 使用本 Skill 的 AI 行为契约（必读）

> 完整行为契约（强制产物 / 硬性禁止 / 缺信息做法 / 决策可追溯 / 终点定义 / 回滚）见 `references/ai-contract.md`。
>
> **使用守则与限制（允许 / 禁止用途 + 硬性约束 + 自检清单）见 `references/usage-policy.md`——每次动手前先读。**

## 14. 运行环境与工具链（端游 / 手游）

服务端代码同一套，差别只在**运行平台 + 保活 + 客户端对接** → 详见 `references/termux.md`（手游/Android）、`references/windows.md`（端游/Windows）。

**环境选择**：
```
只用 Python+SQLite      → Termux / 裸 Windows
要 AES 或大量 Linux 工具 → Termux+proot Ubuntu / WSL2
要长期对外在线           → 云服务器(Ubuntu + deploy.sh) / Windows NSSM
仅本机自测              → 直接跑，客户端连 127.0.0.1
```
> 注意: **保活**是最容易翻车的点：Termux 要 `termux-wake-lock` + 关电池优化；Windows 用**服务/计划任务**，别用前台窗口。
> 脚本：`server/start_termux.sh`、`server/deploy/start_windows.bat`。

---

## 15. 充值 / 邮件 / 道具奖励发放

> 客户端连的是**我们自己的服务端**，第三方支付 SDK 不存在 → **下单直接判成功并发放**（"点击购买即成功"）。
> 参考实现：`logic/handlers/pay.py` / `mail.py`；商品表 `store/models.py: PAY_PRODUCTS`（键 = 客户端真实 product_id）。

- **两条路径**（`game.pay_grant_mode`）：`direct` 货币直接进角色 ／ `mail` 发附件邮件自助领取；`pay_auto_success:true` 跳过真实校验。
- **协议**：`PAY_PRODUCT_LIST 0x0501/2`、`PAY 0x0503/4`、`MAIL_{LIST,READ,CLAIM} 0x0401~0x0406`、`MAIL_NEW_NTF 0x0407`。
- **踩过的坑**：① 邮件推送必须在 PayRes **之后**发（否则被当成充值回包）；② 领取/已读/删除共用结构但**必须用各自 opcode**；③ `order_no UNIQUE` 保**幂等**；④ 发放全在服务端。
- **边界**：仅自建/离线/已授权；不接真实支付渠道、不伪造凭证。

---

## 16. 账号体系与接口还原

> 目标：**官方客户端**用**我们自己注册的账号**登录我们的服务端。方法论 → `references/account.md`。

- **账号从哪来**：A 客户端内注册 ／ **B 独立注册网站**（写同一 DB，客户端只登录；模板 → `templates/register-site/`）／ C 脚本批量建号。
- **注意: 最大的坑——密码预处理**：客户端常先 `MD5(pwd+salt)` 再发包，**必须复刻其哈希**，否则注册的密码登不上。找法：读登录函数 / 抓两次包看密文是否固定；落 Spec 的 `account.password_hash/salt/client_side_hashing`。
- **接口替换**：优先**改配置 / hosts**，不动二进制；有服务器列表就返回我们自己的地址（→ §8.6、`client-address-sources.md`）。
- **典型链路**：`版本/公告 → 登录(账号+密文) → token → 服务器列表 → 带 token 连游戏服(TCP)`。
- 账号接口逐条登记进 `TRACKER.md`。

---

## 17. 房间 / 战斗 / 掉落（核心玩法）

> **没有战斗和掉落，游戏就不成立。** 方法论 → `references/combat.md`、`references/drops.md`；
> 参考实现 → `server/app/logic/rooms.py`、`loot.py`、`handlers/{room,battle,drop}.py`。

- **关系**：`大厅/场景 → 房间(匹配/组队) → 战斗(回合/实时) → 结算 → 掉落(掷骰) → 背包/邮件`。
- **房间**：创建→加入/退出→准备→房主开始→战斗→回等待；必备**槽位上限、房主权限、全准备才开、房主退出移交、空房回收**。
- **战斗（铁律：结算在服务端）**：客户端只发意图；回合制=服务端算结果并广播，实时=服务端定权威状态。必备回合推进/伤害/超时判负/异常退出；结束广播 `BATTLE_RESULT_NTF`。
- **掉落**：`table_id → {rolls, entries:[{item_id, count[min,max], rate}]}`（从客户端配置表反推）；**服务端掷骰**；背包满 → **自动转邮件补发**。
- **协议**：房间 `0x0601~0x060B`、战斗 `0x0701~0x0704`、掉落/背包 `0x0801~0x0805`（详表见 `server/app/proto/opcodes.py`）。
- **经济系统复用**：抽卡(`references/gacha.md`) / 商店 / 背包 **共用同一套「随机→结算→入库」**，不要写两套。

---

## 18. 快速上手（AI 第一次拿到项目的动作序列）

```
[第 0 步 · 最重要] 选对方法
  · 回答 3 个问题：有什么 / 要什么 / 什么约束
  · 对照 references/methods.md §4/§5 选定方法 → 记进 project-profile.yaml 的 method 段
  · 默认路线：M1/M4 → M2+M3 → M6 → M9 → M5

[如果只有安装包]
  0. 走 references/from-installer.md：解包 → 判引擎/语言 → 自产证据 → 抓包
     （详见该文件第 9 节的 10 项动作清单）

[通用主流程]
  1. 列目录 → 跑 references/adaptation.md 的探测命令
  2. 填 out/project-profile.yaml（包括 needs 清单）
  3. 逐条记录证据 → out/evidence-inventory.md
  4. 走 references/decision-tree.md → 填 out/protocol.spec.yaml
     （含 client / subsystems 两段）
  5. 检查 protocol-spec.md 的「Spec 完成度清单」
  5.5 账号/接口：读 references/account.md → 在 TRACKER.md 登记接口清单
  6. 按 references/codegen.md 选语言 + 改造/新建服务端
  7. 增量验证（连接→登录→…）→ 回填置信度
  8. 部署（§14）+ 客户端对接（§8）→ 闭环
```

看 `examples/` 里的三个推演，理解"同样流程、不同结论"。

---

## 19. 后续拓展（可选，不影响核心运行）

> **判断标准**：去掉它，游戏还能不能正常玩？**能 → 它就是拓展**（放 `extensions/`），**不写进核心流程**。

| 拓展 | 文件 | 一句话 |
|------|------|--------|
| **服务端人机（假玩家）** | `extensions/bots.md` | 多人副本凑不齐人时用 AI 自动补位 |
| **反推人机机制** | `extensions/bot-reverse.md` | 无参考项时从客户端获取信息反推它的人机实现 |
**人机为什么是拓展**：单人游戏完全不需要；多人缺人只损体验、**服务端本身能跑**；参考实现默认 `auto_fill: 0`（不生成假玩家）。
**用法**（跑通后再做）：核心链路先通 → 确认是否"必须多人" → `bot-reverse.md` 反推机制写进 Spec → `bots.md` 实现 → 调试（`bots spawn/clear/difficulty`）→ 原版客户端验收。


> 注意: 拓展**不参与**核心验收（§13 的强制产物与闭环）。没做拓展 ≠ 交付不完整。
> 不要因为拓展没做就认为交付不完整；也不要把它塞进核心流程。