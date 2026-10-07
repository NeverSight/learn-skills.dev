---
name: phaser4-game-ad-integration
description: "Phaser 4 + Capacitor 移动项目通过 AppLovin 官方 MAX Cordova 原生插件接入聚合广告时使用；指导 iOS/Android 插件集成、Banner、插页与激励视频、多广告位静默预加载、广告位独立加载重试、视频不可用提示与隐私验收，不用于 Phaser Web 或小游戏广告实现。"
---

# Phaser 4 AppLovin MAX 广告接入

## 适用范围与硬边界

本 Skill 只处理 Phaser 4 + TypeScript/Vite + Capacitor 移动项目的 Banner、插页与激励视频广告能力，聚合层固定使用 AppLovin MAX，接入实现固定使用 AppLovin 官方维护的 `cordova-plugin-applovin-max`，由 Capacitor 的 Cordova 兼容层加载。项目只在 TypeScript 侧建立业务门面和官方插件 API 适配，不自建 Android/iOS 广告插件，也不直接集成 MAX 原生 SDK。所有已配置广告位都必须独立维护状态并在后台静默预加载；全屏展示和 Banner 显隐触发只读取现有状态并立即返回，不在触发路径临时加载。每个广告位独立维护加载失败计数、retry deadline 和至多一个重试 timer，但使用相同分类、退避、暂停和恢复规则。开始任何设计、实施或审查前，必须先读取唯一细则合同 [AppLovin MAX 接入合同](references/applovin-max-contract.md)，并以其中的状态、时序、失败和合规规则为准。

- Phaser Web、浏览器预览和小游戏不直接调用 MAX，也不加载原生广告 SDK；广告能力在这些运行目标上必须是明确的 `unsupported`/no-op，调用后立即返回并继续游戏。
- iOS 与 Android 只使用 AppLovin 官方 `cordova-plugin-applovin-max`。实施前必须按[官方 Cordova 集成文档](https://support.applovin.com/en/max/cordova/overview/integration)和[官方仓库](https://github.com/AppLovin/AppLovin-MAX-Cordova)核对插件版本、Capacitor Cordova 兼容层、Android Gradle 与 iOS 包管理器；不兼容时阻断并报告，不回退到社区插件、自建 Capacitor 原生插件或业务代码直连 MAX SDK。
- 本 Skill 不替项目自动配置 MAX 控制台、广告网络账号、商店元数据或发布渠道。SDK key 与 ad unit ID 按环境从受控构建配置注入官方插件适配层，不手写进业务源码、示例、日志或提交记录；广告网络账号凭证与 Ad Review key 不得进入 Web 代码或公开产物。
- 广告只在自然中断点尝试展示；调用方永不等待广告加载、网络请求或展示完成。不可展示时必须按广告位当前状态立即返回结果，不得阻塞场景切换、输入、主循环或结算流程。后台加载、加载失败和重试保持静默，不弹 Toast。
- 视频广告位在用户触发展示但当前不可用，或官方插件接受展示后回调 `displayFailed` 时，通过统一 UI 层弹出一次“视频广告暂不可用，请稍后再试”Toast；不得由插件适配层直接操作 Phaser UI，也不得因重复回调重复提示。
- Banner 初始化后创建为隐藏状态并静默加载，只有已 ready 且布局安全时才能立即显示；未 ready 时保持隐藏并立即返回，不弹 Toast、不占用错误高度、不等待加载。Banner 不使用视频 Toast 或全屏仲裁。

## 全局控制接入

[`$phaser4-game-workflow-control`](../phaser4-game-workflow-control/SKILL.md) 是唯一的全局状态、风险门、任务范围和证据控制面。本领域可以在当前 Work Item、冻结的 Implementation Package、A 等级与路径范围内提出方案、审查现状并实施；所有计划、变更、测试证据和阻断项必须回到控制面登记和复核。任务内调整接口、路径或验证范围时同步更新 Work Item，不另建平行状态机。

涉及外部写入、付费、真实设备、商店提交、发布或不可逆操作的 A4-A6 动作，必须按对象取得控制面明确批准；本 Skill 不代为批准、执行或推送这些动作，也不自动发起真机运行验收。普通本地文档、桥接代码和单元测试按当前任务授权执行。

## 交付流程

1. 读取当前 Work Item、项目 TDD/依赖能力档、Capacitor 平台状态及官方插件安装状态；按 [AppLovin MAX 接入合同](references/applovin-max-contract.md)登记范围、非目标、公开接口、状态所有权、生命周期和失败边界。广告属于可选商业能力，不能把它作为 Phaser Web 核心循环的运行前置。
2. 提交最小模块提议：Web/小游戏 no-op、AppLovin 官方 Cordova 插件、共享 TypeScript 业务门面与插件 API 适配器、测试替身。核对官方插件发布版本、许可证、Android/iOS 支持、Capacitor 兼容方式、回调语义和隐私能力；不得提出社区插件或自建原生桥作为备用实现。
3. 冻结插件适配契约：`initialize`、`preload(slotId)`、`tryShow(context)`、`setBannerVisibility(slotId, visible)`、`isReady(slotId)` 均为非阻塞调用并返回结构化结果；适配器把官方插件的 callback/event API 归一化为该契约。初始化失败进入 `failed`，瞬时失败只能通过显式初始化重试入口恢复，且不能与加载重试混用。服务初始化幂等，每个广告位只有一个业务状态所有者，原生格式对象由官方插件内部管理。初始化成功后立即静默预加载全部启用广告位；每个广告位的加载失败由自己的重试 timer 调度，独立保存计数与 deadline，并应用同一套 `2/4/8/16/32/64 秒`退避、抖动、去重、后台/离线暂停和恢复规则。一个广告位取消、重排或触发重试不得改变其他广告位的 timer。
4. 将 MAX 控制台、官方插件及其原生依赖、Capacitor Cordova 兼容配置、隐私/CMP/ATT、广告位配置和遥测分别登记责任人。固定聚合渠道为 AppLovin、Google AdMob、Mintegral、Pangle、Unity Ads、DT Exchange（Fyber）和 Verve（PubNative/HyBid）；插件、MAX SDK 与 adapter 的版本组合以官方插件和官方渠道文档当前声明的兼容范围为准，不在 Skill 或业务代码中写死版本号，也不绕过插件重复引入 MAX SDK。
5. 在自然中断点调用 `tryShow`；调用只读取指定广告位快照，绝不触发前台加载。匹配的激励视频 `hidden` 回调到达后，广告服务使用单调时钟记录 30 秒插页保护截止时间；保护期内的插页 `tryShow` 必须立即返回 `rewarded-interstitial-delay`，不得调用 MAX show、创建冷却 timer 或弹不可用 Toast。保护期结束后，只要目标广告位 ready、所有 gates open、自然中断条件成立且全屏展示仲裁空闲，就可以发起展示。未 ready、正在展示、隐私未决、网络不可用或平台不支持都立即返回并继续游戏；视频广告不可用或展示失败时，由统一 UI 层消费结构化结果/事件并显示一次不可用 Toast。激励只由匹配的 `rewarded` 回调异步发放且保持幂等；隐藏或展示失败后继续静默预加载。
6. Banner 使用原生广告视图，按安全区和实际自适应尺寸放置；业务只控制显隐，不自行创建刷新 timer。隐藏、切后台或页面不允许广告时暂停刷新，恢复显示时按合同恢复；不得覆盖游戏按钮、手势区、系统安全区或把空白占位当成已加载广告。
7. 先完成静态审查、TypeScript/原生编译和状态机单测，再在已授权的目标环境运行平台集成测试。使用 MAX Test Mode 与 Mediation Debugger 按渠道和格式分别核验，检查 `app-ads.txt`、iOS SKAdNetwork、Google CMP/TCF 及 ATT；不以单一网络或单一格式成功冒充全部通过。
8. 将候选 diff、接口契约、平台日志（脱敏）、失败重试轨迹和验证结果提交给 `$phaser4-game-workflow-control`；把未执行的外部配置、真机、实时广告和发布步骤列为明确未覆盖项。

## 最低公开契约

共享门面至少提供以下语义，具体参数命名可按目标项目惯例落地，但不能改变返回时序：

```ts
initialize(config): Promise<InitResult> // 只确认桥接请求受理/初始化状态，不等待广告加载
retryInitialize(): Promise<InitResult>  // 仅显式重试初始化，不与 load 重试共用语义
preload(slotId): Promise<PreloadResult> // 只发起或复用指定广告位的后台加载，不等待网络结果
isReady(slotId): ReadyResult            // 读取指定广告位缓存状态，不触发加载
tryShow(context): Promise<ShowResult>   // 只读状态；ready 时发起展示，否则立即返回
setBannerVisibility(slotId, visible): Promise<BannerVisibilityResult> // 只读状态并立即显隐
```

结果至少包含稳定的 `ok`、`code`、`platform`、`phase`、`gates` 和必要的 `retryScheduled` 字段；插页因激励视频后的 30 秒保护期被跳过时返回 `rewarded-interstitial-delay` 和 `interstitialDelayRemainingMs`。业务调用方只传环境、能力开关和业务 `slotId`；官方插件适配器按环境解析 SDK key 与 MAX ad unit ID，并仅在插件 API 边界使用。不得把插件原始异常、设备 ID、广告网络账号凭证或完整 waterfall 凭证透传到业务层。`tryShow` 返回“已请求展示”不等于已展示成功。

`InitResult`、`PreloadResult`、`ReadyResult`、`ShowResult` 及 `NativeAdEvent` 的最小字段、隐私 gate/结果码、`instanceGeneration`/`showRequestId` 关联和重复事件幂等规则统一以[接入合同](references/applovin-max-contract.md)为准。

## 交付审查清单

- 平台边界：Web/小游戏调用为 no-op；Android/iOS 仅通过 AppLovin 官方 Cordova 插件调用 MAX，未引入社区插件、自建原生广告插件或直接 SDK 接入；宿主页面生命周期、Activity/ViewController 和前后台切换已明确。
- 生命周期：初始化幂等；每个已配置广告位持有业务 phase、加载计数、retry deadline 和至多一个加载重试 timer，格式匹配的原生对象由官方插件管理；广告服务额外持有激励视频结束后的 30 秒插页保护截止时间，但不为此创建 timer。所有广告位只共享全屏展示仲裁和该跨格式保护状态等服务级门，不共享加载重试 timer；实例重建递增 `instanceGeneration`，展示请求生成唯一 `showRequestId`；成功初始化立刻静默预加载全部启用广告位，重复调用不会并发请求。
- 原生门：Activity/ViewController provider、前台状态、网络连通性、privacy readiness 和 fullscreen arbiter 属于原生服务依赖；`phase` 只表示广告资源/展示阶段，门状态独立计算，不混入 Phaser 场景状态。
- 节奏：插页只在自然中断点展示；匹配的激励视频 `hidden` 事件从其单调时间戳起阻断插页 30 秒，保护期只阻断插页，不阻断 Banner、激励视频、后台预加载或奖励结算。保护期内立即静默返回剩余毫秒数，过期后无需 timer 唤醒即可恢复判定；`hidden` 与 `displayFailed` 都会触发对应广告位的后台预加载。
- 失败恢复：每个广告位使用独立加载重试 timer，并遵循同一套错误分类与退避公式；计数、deadline、timer 引用和 in-flight 标记均按广告位隔离，同一广告位只允许一个待执行 timer。后台或离线时分别暂停，恢复后每个到期广告位最多恢复一次；展示失败独立记录并重新预加载，不进入另一套重试逻辑。
- 用户反馈：后台加载、重试和状态变化保持静默；视频广告展示触发在立即判定不可用或异步 `displayFailed` 时只显示一次本地化不可用 Toast，重复/迟到回调不会重复提示；`rewarded-interstitial-delay` 是预期节奏控制，不显示不可用 Toast。
- Banner：原生视图默认隐藏，ready 后才显示；显隐不触发临时 load，失败保持隐藏且无 Toast；尺寸基于平台当前自适应 Banner 结果和安全区，布局不遮挡游戏交互；刷新只有一个所有者，禁止 JS/Phaser 自建刷新 timer。
- 合规与安全：CMP/TCF、MAX 隐私标志、iOS ATT、SKAdNetwork、Google 要求和目标地区规则均有责任人和证据；SDK key 与广告位来自受控的分环境构建配置并仅供官方插件适配器使用，账号凭证与 Ad Review key 不进入 Web 层，遥测脱敏。
- 验证：每个固定网络均在测试模式或 Mediation Debugger 中单独确认 adapter、加载、展示和官方插件失败回调；检查 MAX waterfall、`app-ads.txt` 和发布前平台清单。单测还要覆盖官方插件广告事件永不返回时，结算通过 fire-and-forget 仍继续，以及适配器 Promise 只等待本地受理/拒绝、不等待广告事件。

本仓库本次只交付 Skill 指导文件，不新增运行时代码、脚本、SDK 依赖或外部配置。
