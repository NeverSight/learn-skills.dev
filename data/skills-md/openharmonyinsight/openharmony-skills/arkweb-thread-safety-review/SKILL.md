---
name: arkweb-thread-safety-review
description: Must use when scanning or reviewing OpenHarmony ArkWeb/Chromium C++ single files for thread-safety violations involving PostTask, BindOnce, base::Unretained(this), WeakPtr, scoped_refptr, mojo::Connector, GPU/Audio/DrDC threads, NDK/UI callbacks, NWeb, WebContents, Profile, BrowserContext, NavigationController. Enforces false-positive control and outputs strict JSON schema violations for standard_rule1-standard_rule10 only.
---

# ArkWeb 线程安全代码审计技能

## 概述

本 Skill 用于 ArkWeb/Chromium C++ 单文件线程安全审计，只报告本文 10 条标准规则中的明确违规。核心目标不是枚举可疑 API，而是判断当前文件是否同时给出线程/sequence、异步边界、对象归属和生命周期证据。

## 审查前判断

- 确认文件类型和审查范围是否属于 ArkWeb/Chromium C++ 单文件审计。
- 先判断函数或回调可能运行的线程/sequence，尤其是 UI、IO、GPU、Audio、DrDC、IPC 或外部回调线程。
- 对异步任务先确认执行路径和对象生命周期，再判断裸 `this`、`base::Unretained(this)` 或跨线程持有风险。
- 对 UI 线程对象、NWeb 对象、GPU/Audio 资源和 `mojo::Connector`，先确认访问线程和对象归属线程是否一致。
- 只有能指出明确对象、线程路径、异步边界或生命周期证据时，才报告 violation。

## 审查决策路径

1. 识别触发点：优先搜索异步边界、线程切换、mojo/IPC、外部回调、UI/GPU/Audio/NWeb 对象访问和 `scoped_refptr` 跨线程传递。
2. 判断执行线程：从 `CurrentlyOn`、task runner、`CEF_POST_TASK`、BrowserThread、mojo receiver/connector 绑定位置和函数命名推断当前 sequence；无法推断时不直接报违规。
3. 判断对象归属：确认被访问对象是否要求 UI、GPU、Audio、DrDC 或创建线程使用。
4. 判断生命周期：异步任务中只有裸 `this`、`base::Unretained(this)`、跨线程 `scoped_refptr` 且当前文件看不到 owner、取消机制或 `WeakPtr` 保障时才报告。
5. 选择规则：同一证据只归入最具体的 standard_rule；不要重复报多个泛化规则。

## 扫描执行顺序

搜索触发点 -> 建立线程/sequence 证据 -> 确认对象归属和生命周期 -> 套用规则矩阵 -> 仅读取命中规则的示例 -> 必要时读取 team_mapping -> 输出完整 JSON。

## 证据强度与规则选择

- 强证据：当前文件同时出现明确触发点、线程或异步边界、受约束对象、缺失的转发/生命周期保障，可报告 violation。
- 弱证据：只能看到可疑 API 或对象，但当前文件无法确认执行线程、owner 生命周期或跨线程路径，不报告 violation。
- 禁止报告：同步立即调用、仅同一 sequence 内复制 `scoped_refptr`、WebContents/Profile 等对象只被转换为 ID 后跨线程传递、已有 `WeakPtr`/取消机制/明确 owner 覆盖异步任务。
- 报告前自检：每条 violation 必须能回答对象是什么、当前线程/sequence 是什么、异步或跨线程边界在哪里、缺失了什么保障、当前文件哪一行提供证据。
- 规则重叠时选择更具体规则：`mojo::Connector` 跨线程优先 rule7，GPU mojo 线程错误优先 rule2，`compositor_gpu_thread_` 优先 rule3，NWeb/BrowserContext/NavigationController 优先 rule5，通用 Chromium UI 对象访问归 rule6，异步裸 `this` 生命周期归 rule1，跨线程引用计数对象归 rule10。
- 冲突示例：GPU mojo 回调里跨线程使用 `mojo::Connector` 时，若证据核心是 connector sequence-affinity 被破坏，报 rule7；若证据核心是 IPC 回调直接处理 GPU 资源，报 rule2。
- 冲突示例：同一异步任务既捕获裸 `this` 又持有 `scoped_refptr<T>` 时，裸 `this` 的 UAF 证据报 rule1；只有跨线程引用计数/析构模型不安全时才另报 rule10，避免同一根因重复上报。
- 三条以上规则重叠时，按“对象特有线程约束 > 资源线程约束 > 通用生命周期/引用计数”的顺序选择根因；同一代码片段只报告当前文件证据完整支撑的最具体规则。
- 复杂重叠示例：IPC 回调中既触碰 GPU 资源、又使用 `mojo::Connector`、又捕获裸 `this` 时，若当前文件只证明 GPU 资源错线程，报 rule2；只有同时证明 connector 创建/使用 sequence 不一致时才另报 rule7；只有证明异步回调可能晚于对象销毁时才另报 rule1。

## 不确定证据分流

- 缺少创建/绑定线程证据：对 `mojo::Connector`、NWeb、Audio、GPU/DrDC 对象不报告跨线程违规，因为无法证明对象归属线程。
- 缺少 task runner 归属：只看到 `PostTask` 但看不到目标 runner 对应 UI/GPU/Audio/DrDC 时，不把它当作已修复或已违规；继续寻找 `CurrentlyOn`、`RunsTasksInCurrentSequence`、BrowserThread 或命名证据，找不到则不报。
- 缺少 owner 生命周期：异步回调捕获对象但当前文件看不到销毁路径、取消机制或 owner 关系时，只在裸 `this`/`base::Unretained(this)` 与异步边界同时成立时报告；否则不扩展到非标准生命周期问题。
- 缺少被管理对象类型：只看到 `scoped_refptr<T>` 变量但看不到 `T` 的引用计数基类、析构 sequence 或跨线程使用路径时，不报告 rule10。

## 判无违规前复核

在输出空 `violations` 前，至少复核当前文件是否遗漏以下证据：
- 构造函数、`Init*`、`Start*`、`Bind*`、`BindReceiver` 中的 sequence、task runner、receiver 或 connector 绑定点。
- 成员 `*_task_runner_`、`receiver_`、`connector_`、`weak_factory_` 的初始化位置、使用线程和销毁/取消路径。
- 回调是否经过 `On*`、`Did*`、`Notify*`、`Run*`、`Create*On*Thread` 等 helper 二次转发，导致真实执行线程隐藏在同文件其他函数中。
- 对象销毁、`InvalidateWeakPtrs`、取消任务、owner 持有关系是否在当前文件可见；仍无证据时保持空违规，不输出猜测字段。

## 误报控制

- 不得仅凭“缺少线程检查”或“可能多线程调用”报告违规。
- 不得把同步调用误判为异步生命周期问题。
- 证据不足以确认违规时，不报告 violation；需要跨文件才能确认的风险，也应以当前文件可见证据为准。
- 不属于本文 10 条标准规则的问题，不得作为 violation 输出。
- 最终审查结果只能输出 JSON，不得输出 Markdown、解释性文字或代码围栏。

## 绝不报告边界

- rule1：只看到 `base::Unretained(this)`，但回调同步立即执行、对象生命周期由当前文件可见 owner 覆盖、或已经使用 `WeakPtr`/取消机制时，不报告；否则会把性能优化或同步绑定误判成 UAF。
- rule5/rule6：只跨线程传递 frame tree node id、process id、routing id、URL、字符串、配置快照等值类型，不报告 UI 对象跨线程访问；这些值脱离 UI 对象生命周期，不等同于跨线程解引用。
- rule7：只看到 `mojo::Connector` 成员声明或同一 sequence 内使用，无法确认创建和使用 sequence 不一致时，不报告；`mojo::Connector` 的风险来自 sequence-affinity 被破坏，可能导致 DCHECK、消息乱序或竞态崩溃，而不是类型本身。
- rule8：只看到 Audio 方法名，无法确认当前入口来自非 Audio 线程、或已通过 audio task runner 投递时，不报告；Audio 生命周期方法名常被封装，必须有入口线程证据。
- rule10：`scoped_refptr<T>` 本身不是违规；只有 `T` 的引用计数、析构 sequence 或方法访问模型不支持跨线程，且当前文件存在跨线程持有/传递证据时才报告；否则会把正常引用计数生命周期管理误判为跨线程内存风险。

## 辅助材料

`examples/` 保存按标准规则拆分的 good/bad 自包含示例。

示例读取规则：
- MANDATORY READ：命中某条标准规则的关键代码模式并准备判断是否报告时，必须读取该规则对应的 bad 示例；需要确认边界或修复方式时，再读取对应 good 示例。
- 需要区分误报边界时，优先读取 bad 示例，再对照 good 示例。
- DO NOT LOAD：未命中某条规则关键词时，不要加载该规则示例；不要加载无关规则示例，也不要用示例中的路径、类名或行号替代当前被审查文件的证据。

| 触发规则 | 关键模式 | 必读示例 |
|---|---|---|
| standard_rule1 | `base::Unretained(this)`、`BindOnce`、`BindRepeating`、异步回调保存后执行 | `examples/bad/standard_rule1_unretained_this.md`；必要时对照 `examples/good/standard_rule1_unretained_this.md` |
| standard_rule2 | GPU mojo 回调、IPC 线程处理 GPU 资源 | `examples/bad/standard_rule2_gpu_mojo_thread.md`；必要时对照 `examples/good/standard_rule2_gpu_mojo_thread.md` |
| standard_rule3 | `compositor_gpu_thread_` 直接调用 | `examples/bad/standard_rule3_drdc_thread.md`；必要时对照 `examples/good/standard_rule3_drdc_thread.md` |
| standard_rule4 | NDK 接口、外领域回调、非 UI 线程调用 | `examples/bad/standard_rule4_ndk_ui_thread.md`；必要时对照 `examples/good/standard_rule4_ndk_ui_thread.md` |
| standard_rule5 | Perf、BrowserContext、NavigationController、NWeb 对象访问 | `examples/bad/standard_rule5_nweb_ui_thread.md`；必要时对照 `examples/good/standard_rule5_nweb_ui_thread.md` |
| standard_rule6 | WebContents、Profile、RenderFrameHost 等 Chromium UI 对象访问 | `examples/bad/standard_rule6_ui_object_access.md`；必要时对照 `examples/good/standard_rule6_ui_object_access.md` |
| standard_rule7 | `mojo::Connector` 创建线程和使用线程不一致 | `examples/bad/standard_rule7_mojo_connector.md`；必要时对照 `examples/good/standard_rule7_mojo_connector.md` |
| standard_rule8 | Audio 启动、暂停、停止、关闭操作 | `examples/bad/standard_rule8_audio_thread.md`；必要时对照 `examples/good/standard_rule8_audio_thread.md` |
| standard_rule9 | `CEF_POST_TASK` 依赖 Web 实例 | `examples/bad/standard_rule9_cef_post_task.md`；必要时对照 `examples/good/standard_rule9_cef_post_task.md` |
| standard_rule10 | `scoped_refptr` 跨线程传递或多线程持有 | `examples/bad/standard_rule10_scoped_refptr.md`；必要时对照 `examples/good/standard_rule10_scoped_refptr.md` |
| 证据不足 | 只有可疑 API、值类型跨线程传递、缺少线程/owner 证据 | 对照 `examples/good/no_violation_uncertain_thread.md` 和 `examples/good/no_violation_id_transfer.md` |

## 规则判定矩阵

| 规则 | 触发证据 | 必要报告证据 | 不报告条件 |
|---|---|---|---|
| standard_rule1 | `PostTask`、delay、ThreadPool、mojo/IPC、NDK 或外部回调中绑定裸 `this`/`base::Unretained(this)` | 当前文件看不到 `WeakPtr`、取消机制、owner 生命周期覆盖，且回调可能在对象销毁后执行 | 同步立即执行、生命周期证据充分、已使用 `WeakPtr` 或取消机制 |
| standard_rule2 | GPU mojo 回调、IPC 线程收到 GPU 操作 | GPU 资源或 GPU 接口在 IPC/当前回调线程直接使用，未投递到 GPU 线程 | 只转发参数、不触碰 GPU 资源，或已投递到目标 GPU task runner |
| standard_rule3 | `compositor_gpu_thread_` 成员调用 | 调用发生在 UI/IPC/非 DrDC 入口，且未通过 DrDC task runner 转发 | 当前代码已经在 DrDC task runner 上执行 |
| standard_rule4 | NDK 接口、外领域交互回调、应用侧回调入口 | 当前入口不是 UI 线程，仍直接调用 NDK/外部回调 | 已检查 UI 线程或已 `PostTask` 到 UI 线程 |
| standard_rule5 | Perf、BrowserContext、NavigationController、NWeb 对象访问 | 当前入口不是 UI 线程，直接读写这些 UI 归属对象 | 只传递 ID/值快照，或访问已经转发到 UI 线程 |
| standard_rule6 | WebContents、Profile、RenderFrameHost、RenderProcessHost 等 Chromium UI 对象 | 非 UI 线程直接解引用或调用对象方法 | 只跨线程传递稳定 ID/弱引用 token，或回到 UI 线程再访问 |
| standard_rule7 | `mojo::Connector` 创建、绑定、`Accept`、`Close`、发送消息 | 当前文件同时显示创建/绑定 sequence 与使用 sequence 不一致 | 只有声明、同 sequence 使用，或缺少创建线程证据 |
| standard_rule8 | Audio start/pause/stop/close、音频回调入口、audio task runner | 非 Audio 线程直接执行音频生命周期操作 | 已通过 audio task runner 投递，或入口可确认在 Audio 线程 |
| standard_rule9 | `CEF_POST_TASK` 投递依赖 Web 实例的任务 | 投递前未检查对应 Web 实例已创建/仍可用，当前文件存在初始化竞态 | 投递前已有实例检查或任务不依赖 Web 实例 |
| standard_rule10 | `scoped_refptr<T>` 跨线程传递、多线程持有、异步任务捕获 | 必须确认 `T` 的引用计数基类和对象访问路径是否线程安全；`base::RefCounted` 对象不得跨线程持有/释放 | 仅同 sequence 内复制，或 `T` 明确使用 `base::RefCountedThreadSafe` 并支持跨线程访问 |

## 规则等级

规则等级用于标识违规风险优先级，不影响是否报告 violation。所有 violation 仍必须满足本文的明确证据要求。

| 等级 | 标准规则ID | 报告策略 |
|---|---|---|
| P1 | standard_rule1, standard_rule2, standard_rule3, standard_rule6, standard_rule7, standard_rule10 | 优先报告和修复；通常涉及 UAF、跨线程 UI/GPU/DrDC/mojo sequence 破坏或引用计数竞争 |
| P2 | standard_rule4, standard_rule5, standard_rule8, standard_rule9 | 正常报告；通常涉及 UI/Audio 线程契约、NWeb/BrowserContext 访问约束或 Web 实例生命周期前置条件 |

**报告要求**：
- 所有 violation 必须带 `rule_level` 字段，并与上表保持一致。
- 不得仅凭“缺少线程检查”“可能多线程调用”报告，必须指出明确对象、跨线程路径或生命周期证据。

## 标准规则索引

以“规则判定矩阵”为主规则源；本节只提供 `rule_id` 和 `rule_name`，避免与矩阵产生漂移。

| rule_id | rule_name |
|---|---|
| standard_rule1 | 异步任务裸 this 生命周期约束 |
| standard_rule2 | GPU mojo 任务线程约束 |
| standard_rule3 | compositor_gpu_thread_ DrDC 线程约束 |
| standard_rule4 | NDK 接口与外领域回调 UI 线程约束 |
| standard_rule5 | NWeb 相关对象 UI 线程约束 |
| standard_rule6 | Chromium UI 线程对象访问约束 |
| standard_rule7 | mojo::Connector 跨线程约束 |
| standard_rule8 | Audio 操作 Audio 线程约束 |
| standard_rule9 | CEF_POST_TASK Web 实例创建约束 |
| standard_rule10 | scoped_refptr 线程安全约束 |

## 模块责任划分

优先按代码所属功能模块和文件路径选择团队；若规则与多个团队相关，以直接拥有被访问对象或接口的团队为准。当前文件无法可靠判断时，选择最接近的功能团队，并在 `issue` 中写明依据，不要因为归属不确定新增非标准规则。

输出 violation 时必须填写 `team`。若无法从路径、对象或接口直接确定团队，必须读取 `references/team_mapping.md`；仍无法判断时填最接近团队，并在 `issue` 中说明依据。

## 评审输出格式

本 Skill 专注于**单文件扫描**。

输出仅采用 JSON，便于工具链解析和结果汇总。

### 格式约束（必须严格遵守）

1. **只输出 JSON**，禁止添加 Markdown、解释性文字、代码围栏或额外章节。
2. **违规规则必须来自本文档定义的标准规则**。
3. **必须附上规则编号**：`rule_id` 使用 `standard_rule<N>`，`rule_name` 使用对应标准规则名称。
4. **必须附上规则等级**：每条违规必须按“规则等级”表输出 `rule_level`。
5. **无违规时也必须输出完整 JSON 结构**，`violations` 数组为空。
6. **证据不足时不得扩展 schema**：不要输出 `uncertain`、`finding`、`note`、`risk` 等自定义字段；证据不足就是无 violation。
7. **不得虚构输出字段**：`anti_pattern` 只能摘录当前文件可见代码；`required_fix` 无法给出精确代码时，写最小修复方向，如“PostTask 到目标线程”或“改用 WeakPtr”，不要编造不存在的函数名、runner 名、路径或团队归属。
8. **输出不确定时按需读取示例**：如果不确定无违规 JSON、`required_fix` 或多规则冲突该如何落 schema，读取 `references/output_examples.md`。

### JSON 格式

```json
{
  "scan_info": {
    "file_path": "<文件绝对路径>",
    "skill": "arkweb-thread-safety-review"
  },
  "summary": {
    "total_violations": 0,
    "by_rule": {
      "<规则编号>": <数量>
    },
    "by_team": {
      "<团队名称>": <数量>
    }
  },
  "violations": [
    {
      "id": 1,
      "rule_id": "<规则编号，如 standard_rule1>",
      "rule_name": "<规则名称>",
      "rule_level": "<规则等级，如 P2>",
      "location": {
        "file": "<文件名>",
        "line": <行号>,
        "function": "<函数名>"
      },
      "issue": "<问题描述>",
      "anti_pattern": "<违规代码片段>",
      "required_fix": "<最小修复方向或当前文件可见的修复片段>",
      "impact": "<违反后果>",
      "team": "<责任团队>"
    }
  ]
}
```

**无违规时**：`violations` 数组为空 `[]`，`summary.total_violations` 为 0，`by_rule` 和 `by_team` 为空对象 `{}`。
