---
name: spring-processor
description: 在 Spring 工程中按 Processor + Context + Handler 模式编排多步骤业务操作，把长流程拆成有序 Handler，并用 Context 传递步骤间的中间结果。当需要新增或改造包含多个可独立描述步骤的写操作，或调整已有 Processor 流程的步骤与顺序时使用。
---

# Spring Processor 编排

## 适用场景

### 目标

把包含多个可独立描述步骤的业务操作交给统一的 `Processor` + `Context` + `Handler` 编排：
每个步骤一个 `Handler`，步骤间数据经 `Context` 字段传递，
调用方只负责构造入参、触发编排、取回响应。

### 适用

- 写操作包含多个可独立描述的步骤时，统一使用该模式编排。
- 新增多步骤业务操作（创建、更新、删除、上传等），每步都能单独说明条件、输入、过程和输出。
- 把已有 Service 中流程冗长、职责混杂的方法改造成 `Context` + `Handler` 链。
- 为已有 `Context` 增加、拆分或重排步骤。
- 仓库尚无框架代码时，按模板创建 `Processor`、`Context`、`Handler` 三件套。

### 不适用

- 单步、没有编排价值的简单增删改查：直接写 Service 方法。
- 第三方 REST 接口封装与远程调用：使用 `spring-openfeign-client`。
- 只修缺陷且不涉及步骤拆分。
- 修改已存在的 `Processor`、`Context`、`Handler` 框架类本身，除非用户明确要求。

## 前置条件

### 必要输入

- 目标业务操作：它做什么，以及它的请求与响应类型。
- 步骤划分：每步做什么、依赖哪些中间结果。用户只给需求描述时，按
  「校验 → 加工或判权 → 落库 → 派生处理 → 组装响应」的通用顺序起草，并在交付时列出推断结果请其确认。
- 框架位置：仓库中 `Processor`、`Context`、`Handler` 的所在包。

### 必要环境

- Java + Spring Boot 工程，`Processor` 已作为 Spring Bean 可注入。
- 目标模块的 `processor` 包在组件扫描范围内，Handler 以 `@Service` 注册。
- 能读取同模块既有的 `Context` 与 `Handler`，作为命名与顺序风格的参照。

### 参考文件

- 编写 `Context` 与 `Handler` 前必须读取
  [references/pattern-template.md](references/pattern-template.md)：
  框架三件套源码、`Context` 与 `Handler` 骨架模板、目录结构、命名与顺序约定。
- 第一次做编排，或对文件划分、调用链、条件步骤有疑问时，读取
  [references/examples.md](references/examples.md)：一个从请求类型到调用方写全的三步注册流程示例，含并发唯一性与密码存储边界。
- 规则以本文件与模板文件为准；示例只做演示，不单独承载规则。示例中的业务、安全算法与类型签名不得自动套用到目标项目。

### 信息缺失处理

- 未指定目标模块或包路径：跟随被改造方法所在模块，沿用同模块既有包结构。
- 仓库不存在框架三件套：参考模板创建 `Processor`、`Context`、`Handler` 后再编排，
  并在交付说明中写明创建位置。
- 步骤划分、事务边界或权限点无法确定：先实现可确定部分，把不确定项列为待确认，
  不臆造业务规则。

## 执行步骤

### 步骤 1：确认框架与既有用法

- 操作：
  - 定位 `Processor`、`Context`、`Handler`，确认 `Processor` 可注入、所在包在扫描范围内。
  - 通读同模块至少一个既有 `Context` 及其全部 Handler，
    记录包结构、命名后缀、顺序常量取值习惯与 Lombok 注解用法。
  - 读取 [references/pattern-template.md](references/pattern-template.md)；
    首次编排或需要参照完整文件划分时，同时读取 [references/examples.md](references/examples.md)。
- 完成标志：
  - 能说出目标模块的包路径、命名规则与顺序常量取值习惯。
  - 框架可用，或已确认需要先按模板创建。

### 步骤 2：设计步骤序列并编写 Context

- 操作：
  - 把操作拆成有序步骤，每步明确「条件、输入、过程、输出」。
  - 每个步骤一个 `public static final int` 顺序常量，按执行顺序声明，
    并在 Javadoc 中写明条件、输入、过程、输出以及 `@see` 实现类。
  - 顺序值步长 10（10、20、30…），需要插队时取中间值（如 5、15），不复用已有取值。
  - 跨步骤共享的中间结果声明为 `Context` 字段；整体入参与最终响应由
    `Context<请求类型, 响应类型>` 的泛型承载。
  - 步骤之间没有数据依赖时不要新建字段；无额外字段时不需要 Lombok 注解。
- 完成标志：
  - 每个步骤都有唯一顺序常量、完整的步骤 Javadoc 与对应实现类名。
  - `Context` 字段只包含需要跨 Handler 传递的数据，没有冗余字段。

### 步骤 3：实现 Handler

- 操作：
  - 每个步骤一个类，`implements Handler<XxxContext>`，
    注册为 Spring Bean 并标注 `@Order(XxxContext.步骤常量)`；依赖注入方式沿用模块既有风格。
  - `handle` 内从 `context.getIn()` 读入参、读写 `Context` 字段；
    不重复加载上一步已载入的数据。
  - 仅当该步骤确实有条件时才重写 `shouldHandle`，条件判断只读 `Context`。
  - 产出业务响应的那一步调用 `context.setOut(...)`。
  - 业务失败使用项目统一业务异常（示例以 `BizException` 表示）；类名后缀跟随同包既有风格。
- 完成标志：
  - 每个步骤都有实现类，`@Order` 引用 `Context` 常量而非字面量。
  - 每个 Handler 的泛型参数就是该 `Context` 类本身；确认组件扫描和泛型匹配能发现全部预期 Handler，不以零 Handler 或缺步骤的空流程报告成功。

### 步骤 4：改造调用方

- 操作：
  - Service 注入 `Processor`，方法体为：
    `new XxxContext()` → `context.setIn(请求)` → `processor.process(context)` → 检查必需响应非空 → 返回响应。
  - 入参不是单一 DTO 时，在 `process` 前直接设置 `Context` 字段。
  - 多步数据库写入需要原子性时，在 Service 调用入口划定 `@Transactional` 边界；Handler 通常不各自开启事务。不要未经设计把外部调用纳入数据库事务。
- 完成标志：
  - Service 方法只负责构造 Context、触发流程、检查并返回结果，业务步骤已拆入 Handler。
  - 原方法中的流程代码已移除，没有留下重复实现。

### 步骤 5：验收并输出

- 操作：
  - 逐条核对「验收标准」。
  - 命名、顺序常量、`@Order` 引用、有响应流程未写入 `out`、泛型写错等可直接修正的问题，
    修正后重新核对。
  - 步骤划分、事务边界、权限点等业务歧义列入待确认，不自行决定。
- 完成标志：
  - 适用的验收项全部通过，或已明确列出未确认项与阻断原因。

## 约束

### 编排规则

- 一个 Handler 只做一步，不在 Handler 内调用另一个 Handler。
- 步骤间数据只经 `Context` 字段传递，不引入新的 `ThreadLocal`、静态变量或隐式全局状态来传递中间结果。
- Handler 不返回响应，也不在 Service 之外解析流程结果。
- 顺序只由 `@Order` 决定，不依赖 Spring Bean 的发现顺序。
- 已存在的步骤常量与顺序值保持不变；插入新步骤使用空闲值，不重排既有取值。

### 修改范围

- 不修改已存在的 `Processor`、`Context`、`Handler` 框架类，除非用户明确要求。
- 不重构与本次操作无关的既有步骤、Service 方法或包结构。
- 只新增或修改完成该操作所需的文件，不删除无关代码。
- 不主动运行构建、测试或启动应用；用户要求运行而环境不具备时，说明未验证。

### 异常处理

- `Context` 与 Handler 已存在且用户只要求增加步骤：只新增常量与 Handler，
  不重建 `Context`、不调整已有顺序值。
- 框架三件套缺失：参考模板创建；创建位置无法确定或创建受阻时停止并报告。
- 步骤划分存在歧义：先实现可确定部分，列出待确认项，不编造业务规则。
- 无法可靠继续时停止，说明失败步骤、已完成内容及影响，不把部分完成报告为全部成功。

## 输出与验收

### 交付内容

- 按包路径列出每个新增或修改的 Java 文件及其完整内容。
- 附一张步骤表：顺序常量 → 顺序值 → Handler 类 → 执行条件。
- 说明未编译、未运行验证的部分，以及列出的待确认项。

### 验收标准

- 每个 Handler 的泛型参数是传给 `processor.process()` 的那个 `Context` 类本身。
- 每个 Handler 都是 Spring Bean，并标注 `@Order(XxxContext.常量)`；依赖注入与 Bean 注解沿用目标模块风格，顺序值唯一、无字面量魔数。
- `Context` 的步骤常量按执行顺序声明，Javadoc 写明条件、输入、过程、输出并指向实现类。
- 有响应的流程由 `context.setOut()` 产出，Service 在取回响应前检查非空；同时通过启动检查或测试确认预期 Handler 全部注册。无响应流程按其响应类型契约处理。
- 需要原子性的多步数据库写入由 Service 调用入口管理事务；Handler 不擅自开启独立事务，外部副作用边界已明确。
- 步骤间流转的中间结果只存放在 `Context` 字段中。
- 未改动框架类，也未改动无关既有步骤的顺序值。

## 示例

完整代码见 [references/examples.md](references/examples.md)：含请求类型、`Context`、三个 Handler 与调用方的三步注册流程。以下另列条件步骤的通用边界场景。

### 多步骤写操作的编排

场景：

> 给业务模块加一个注册写操作：校验用户名是否存在、生成随机盐并计算 SM3 摘要、入库、返回用户 ID。

关键预期行为：

- `Context` 按执行顺序声明三个步骤常量（10、20、30），每步一段四段式 Javadoc。
- 每个步骤一个 `Handler<RegisterContext>`：校验用户名、处理密码、入库。
- 密码步骤把盐值与密码摘要写入 `Context`，入库步骤直接取用，不重复计算。
- 入库并产出响应的那一步调用 `context.setOut(new RegisterResp(userId))`。
- Service 的 `register` 方法只负责设置入参、调用 `process`、检查响应非空并返回；该多步入库场景需要原子性时，在方法上标注 `@Transactional`。
- 若作为 SM3 密码存储方案使用，先核对项目安全要求；交付时给出步骤表，并说明未编译验证。完整代码及唯一约束、密码存储注意事项见 [references/examples.md](references/examples.md)。

### 条件步骤的边界场景

场景：

> 现有多步骤流程中有一个派生处理，只在请求包含目标值时执行。

关键预期行为：

- 先确认这个处理确实是可选步骤，且跳过后后续必需步骤仍然成立。
- 在 `Context` 上追加空闲顺序常量，不改动已有步骤取值。
- `shouldHandle` 只根据 `Context` 中已有数据作纯判断；外部调用放在 `handle`。
- 如果跳过会导致关键结果缺失，应让前序步骤校验并失败，而不是静默跳过。
