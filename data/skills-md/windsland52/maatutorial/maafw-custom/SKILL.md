---
name: maafw-custom
description: 编写、注册与调试 MaaFramework Custom 识别/动作——何时上 Custom 的判据、宿主与注册路径、binding 实现与注册、参数解析与校验、复用 pipeline 节点、Agent 子进程模式与工程规范。Use when implementing MaaFW custom recognition or action logic, deciding registration path for your host, registering customs, parsing custom_action_param/custom_recognition_param, reusing pipeline nodes inside custom code, or setting up the agent child process mode.
---

# MaaFW Custom 开发

Pipeline 表达不了的逻辑用 Custom 补齐：读外部状态、跨节点数据传递、动态计数、复杂判定、自定义识别算法。binding 类签名与 context API **不凭记忆写**，一律路由 [MaaLLMWiki](https://github.com/Windsland52/MaaLLMWiki) 的 bindings / native-api 索引（版本锁定、引用回源；已安装 `maallmwiki` skill 时由其承载完整路由流程）。

## 硬护栏

1. **能 pipeline 不 custom**（默认方向，由成本非对称决定而非偏好）：
    - **为什么偏 pipeline**：custom 节点的**外层**仍受引擎调度与观测——next 候选顺序（先命中先执行）、`max_hit`、`on_error`、focus、option 的 pipeline_override 照常生效，`run_task` 起的子流程也由引擎执行。失去自动约束的是**回调内部**——内部循环 / 等待 / 网络 IO 不展开为节点图，节点 `timeout` 打不断阻塞中的回调，耗时、取消、重试、内部状态全靠自己管，对工具链只剩日志。
    - **一律 pipeline**：视觉可判定的等待 / 点击 / 滑动 / 找字 / 循环 / 分支——循环 = next 环 + 出口 + max_hit（固定次数重复用 `repeat` / `repeat_delay` / `repeat_wait_freezes`，v5.3+），分支 = next 顺序 + 遮蔽。
    - **才上 Custom**：依赖画面外运行时数据（文件、网络、进程状态、时间）的读取或以其为判据的控制流；识别 / 动作字段表达不了的判定；外部调用。
    - **字段表达力的两条硬边界**（实证项目 custom 存量的大头就在这）：
        - And / Or 是**布尔组合**——无数值比较、无跨节点算术（数值比较、多节点数值表达式是 custom 的地盘）；组合期唯一数据流是 box：`box_index` 选输出、`sub_name` 传 filtered box 作 ROI、Or 取命中者 box；
        - `max_hit` 只会递增，pipeline 字段**读不到也清不掉**命中计数——custom 内可用 `get_hit_count` / `clear_hit_count`（作用域：当前任务与其 `run_task` 子任务共享）；跨节点"数据"仍无字段通道——`anchor` 是节点名变量（写 / 清 / 引用三态），不是数据存储。
    - **该转 custom 的反信号**：为表达一段逻辑开始堆克隆节点、节点图膨胀难读、开始需要运行时改参数或计数（override / 状态类标准件频繁登场）——继续拆不如转。
    - 判据拿不准先回 `maafw-pipeline` 试拆节点。
2. **失败要显式，且分清三种语义**：
    - CustomRecognition 返回未命中 = 本候选不命中——轮询继续试后面的候选，整轮全未命中等宿主节点 `timeout` 后走**宿主的** on_error（不是立即触发）；
    - CustomAction 返回失败 = 走**动作所在节点**的 on_error；实现异常不吞、显式失败返回——静默假成功是排障噩梦；
    - binding 侧**空返回值语义**要查再写（样例：Python 动作 `run` 返回 None 等价成功、识别 `analyze` 返回 None 等价未命中——漏写 return 在动作侧就是静默假成功；以 binding 路由为准）；
    - 直调 `context.run_recognition()` 只返回识别结果，错误分支由调用方自理。
3. **注册名逐字符一致**：注册名（装饰器或注册表中的字符串）与 pipeline 节点引用完全一致，区分大小写。**改名时同步所有注册点**——装饰器/注册表、pipeline 引用（先改 pipeline 用法再改注册）、有 Schema 基建则含 enum；custom 代码内的节点名引用（`run_task` / `run_recognition` / `run_action` 的 entry、`override_next` 的目标）也在同步面——**调用即失败**（返回值要判），不是静默失联；素材路径同样在同步面，但框架不替你报错——自定义代码读图必须自查加载结果（空图即失败），漏改多表现为静默空转（引用点全表见 maafw-pipeline 的 naming.md）。
4. **签名路由**：`analyze` / `run` 的参数结构、context API 随 binding 版本演进，以路由结果为准，本文样例仅作形态示意；不依赖框架未承诺的钩子（如 stop / 中断回调——有没有、叫什么以路由结果为准）。框架**不会主动打断回调**——长循环自查停止条件、外部 IO 设超时、资源清理用 finally / RAII 等该语言机制。
    - **Context 能力面**（上了 custom 之后有哪些杠杆；名字以 binding 路由为准）：`run_task` / `run_recognition` / `run_action`（按节点跑，识别与动作配对）；`run_recognition_direct` / `run_action_direct`（不建节点直接用引擎算法）；`wait_freezes`（引擎等画面静止，内部自截图）；`override_pipeline` / `override_next` / `override_image`（补丁三件）；`get_node_data`（读当前有效节点定义，含补丁）；`set_anchor` / `get_anchor`（锚点读写）；`get_hit_count` / `clear_hit_count`（计数读清）；`get_tasker`（取 controller / resource——截图链的前提）；`clone`（分叉 context）。
5. **状态最小化**：custom 内尽量无状态；确需跨调用记忆（如"仅首次执行"哨兵）要注明生命周期——agent 进程存活期间类状态跨任务共享，任务重入会带着上次的值。

## 工作流

1. **定宿主与注册路径**（先于一切实现决策）：能不能进程内注册由**谁拥有主程序**决定——细则、agent 段接线与架构见 references/agent-mode.md。
2. **判型**：
    - 自定义识别算法 → `CustomRecognition`（`analyze` 返回命中 box）；
    - 外部调用 / 复杂动作 → `CustomAction`（`run` 返回成功失败）；
    - 横切钩子（全局检查、失败引导）→ sink 通道而非散进 action（细则见 patterns.md「事件监听」）。

    特例不与上列并列：非标设备控制走 `CustomController`——按**控制器**接入而非注册（子类 + 工厂构造后 bind 给 Tasker），且仅掌控宿主进程时可行，agent 子进程内框架不提供控制器创建（见 agent-mode.md 的 agent 能力面）。
3. **最小注册闭环**：先接最小节点（DoNothing + 日志）跑通"注册 → pipeline 引用 → 被调到"，再填实现。
4. **建文件与实现**：
    - 按业务能力分文件，与 resource 的模块目录对齐（文件形态随语言惯用法，判据见 references/patterns.md「模块边界」）；
    - 通用可复用件进共享件目录；注册进唯一的注册点（装饰器或集中注册表）；
    - 参数从 pipeline 的 `custom_action_param` / `custom_recognition_param`（JSON）进入，经解析工具函数做类型 / 必填 / 默认值处理与运行时校验后使用，不裸取字段；实现自带行为契约文档（docstring / 注释等该语言惯例）——写清预期行为与参数语义。
5. **复用而非重写**：
    - custom 内需要识别 / 动作时优先引用既有 pipeline 节点——`context.run_recognition("<节点名>", image)` 直接跑某节点的识别；
    - 图像来源按用途：识别回调判定本次画面用 `argv.image`；动作后要新画面经既有 controller 主动截图**等完成后再取图**（样例形态 `context.tasker.controller.post_screencap().wait().get()`，名字以 binding 路由为准）；`cached_image` 属 controller、是最近一次已完成截图的缓存、**不会自己刷新**——时效可接受才用；
    - 识别 → 操作 → 再识别法则在 custom 内同样成立（见 maafw-pipeline 的 flow-patterns）。
6. **失败、取消与状态作用域**：失败三语义见硬护栏 2；长循环与外部 IO 的取消策略见硬护栏 4；跨调用状态的生命周期注明（硬护栏 5）；override 补丁写明对象、作用域与生命周期（见 patterns.md「状态与作用域」）。
7. **验证**：日志带节点名 + 入参摘要 + 结果摘要（这是排错唯一线索）；单元验证后转 `maafw-debug` 单节点流程与端到端。

## 审查清单

- 判据：这个逻辑真的 pipeline 表达不了吗？有没有把流程控制藏进 custom（回调内部不展开为节点图）？
- 命名能自解释：注册名与 pipeline 节点命名风格对齐（惯例 PascalCase），项目内统一。
- 参数底线：入口运行时校验——类型 / 必填 / 默认值 / 错误行为明确；有 Schema 基建的项目同步 enum 与注册名，并确认校验入口真的覆盖（建文件本身不产生校验）。
- 失败路径：三种失败语义分清；没有裸 `except: pass`；空返回值的 binding 语义核对过。
- 阻塞与取消：长循环有停止检查、外部 IO 有超时、清理有 finally / RAII 等机制。
- 注册点：改名改删时，pipeline 用法 → 注册点 → （有 Schema 则含 enum）→ custom 代码内节点名引用与素材路径，全部同步。

## 深入阅读（按需）

- [references/patterns.md](references/patterns.md) — Custom 实现决策指南：注册与加载、模块边界、参数契约、Pipeline 复用、状态作用域、失败取消、事件监听、验证
- [references/agent-mode.md](references/agent-mode.md) — Agent 子进程模式：启动到退出的阶段职责、连接标识符、PI_* 容错、双日志、宿主与隔离决策
