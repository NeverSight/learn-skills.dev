---
name: observability-and-instrumentation
description: 给代码埋点，让生产行为可见、可诊断。在添加日志、指标、tracing 或告警时使用。在构建任何会跑在生产环境的功能、而你需要证据证明它能工作时使用。在生产问题被上报、但仅凭现有数据说不清发生了什么时使用。
---

# 可观测性与埋点

## 概览

无法观测的代码，就无法运维。可观测性是指：借助代码发出的 telemetry，从外部回答“系统正在做什么、为什么”。埋点不是上线后的附加项——它和功能代码一起写，就像测试一样。如果一个功能在没有 telemetry 的情况下发布，第一个用户上报的 bug 就变成了考古，而不是查询。

## 何时使用

- 构建任何会跑在生产环境的功能
- 添加新的服务、endpoint、后台 job 或外部集成
- 一次生产事故的诊断花了太久（"we couldn't tell what happened"）
- 建立或评审告警规则
- 评审一个新增 I/O、重试、队列或跨服务调用的 PR

**不适用于：**
- 诊断正在发生的故障——用 `debugging-and-error-recovery` skill（可观测性正是让这个 skill 下次跑得快的东西）
- 对已测量出的慢做 profiling 和优化——用 `performance-optimization` skill
- 发布日的监控 checklist 和回滚触发器——见 `shipping-and-launch` skill；本 skill 覆盖的是喂养它们的那层埋点

## 流程

### 1. 先定义“能工作”，再埋点

没有问题支撑的 telemetry 就是噪音。在添加任何埋点之前，写下 on-call 工程师针对这个功能会问的 2–4 个问题：

```
FEATURE: checkout payment retry
QUESTIONS ON-CALL WILL ASK:
1. What fraction of payments succeed on first attempt vs after retry?
2. When a payment fails permanently, why? (provider error? timeout? validation?)
3. Is the payment provider slower than usual?
→ Every signal below must help answer one of these.
```

如果你说不出这些问题，你就还没准备好埋点——你会把一切写进日志，然后什么也学不到。

### 2. 为每个问题选对信号

| 信号 | 回答什么 | 成本特征 | 例子 |
|---|---|---|---|
| **结构化日志** | “这个具体案例里发生了什么？” | 按事件计；随流量增长 | 带 provider 错误码的 `payment_failed` |
| **指标** | “聚合来看，多频繁 / 多快？” | 每个 series 固定；查询便宜 | provider 调用的 p99 延迟 |
| **Trace** | “时间花在了跨服务的哪一段？” | 按请求计；通常采样 | 一次慢 checkout，按 hop 拆开看 |

经验法则：指标告诉你**出了**什么问题，trace 告诉你问题在**哪里**，日志告诉你**为什么**。

### 3. 结构化日志

记录事件，不是散文。每一行日志都是一个 JSON object，带有稳定的事件名和机器可读的字段：

```typescript
// BAD: string interpolation — unqueryable, inconsistent
logger.info(`Payment ${id} failed for user ${userId} after ${n} retries`);

// GOOD: stable event name + structured fields
logger.warn({
  event: 'payment_failed',
  paymentId: id,
  provider: 'stripe',
  errorCode: err.code,
  attempt: n,
}, 'payment failed');
```

**日志级别——用得体一致：**

| 级别 | 含义 | On-call 的动作 |
|---|---|---|
| `error` | 不变量被打破；可能有人需要采取行动 | 调查 |
| `warn` | 降级但已处理（重试成功、用了 fallback） | 留意趋势 |
| `info` | 重要的业务事件（下单完成、job 结束） | 无 |
| `debug` | 诊断细节 | 生产环境默认关闭 |

**Correlation ID 是强制的。** 在系统边界生成（或接受）一个 request ID，并把它附加到每一行日志、每个 span 和每次对外调用上。没有它，你无法从交错的日志里重建出单个请求：

```typescript
// Express: child logger per request, ID propagated downstream
app.use((req, res, next) => {
  req.id = req.headers['x-request-id'] ?? crypto.randomUUID();
  req.log = logger.child({ requestId: req.id });
  res.setHeader('x-request-id', req.id);
  next();
});
```

**当多个入口点写同一份日志时，给日志标出入口点。** Correlation ID 标识一次运行，但说不出是哪条代码路径发起了它。同一个 job 被 scheduler、replay endpoint 和手动 CLI 运行各触发一次，会在同一个 sink 里产出可以互相顶替的行，于是行的归属只能靠排除法——交叉阅读 scheduler 的历史、进程表、部署日志——而这套论证只在外层那些记录恰好还存在时才成立。在运行启动的地方、紧挨着 correlation ID 给入口点打标记，并让两个字段以同样的方式传播：

```typescript
// One helper for every entry point: the run's own logger carries both fields.
// `entryPoint`, not `source` — ECS reserves `source.*` for network fields.
export const runLog = (entryPoint: 'scheduler' | 'replay_endpoint' | 'cli', runId: string) =>
  logger.child({ entryPoint, requestId: runId });

// scheduler tick        -> runLog('scheduler', crypto.randomUUID())
// POST /jobs/:id/replay -> runLog('replay_endpoint', req.id)
// CLI invocation        -> runLog('cli', process.env.RUN_ID ?? crypto.randomUUID())
```

这两个字段必须和 correlation ID 跨越同样的边界——队列 metadata、HTTP header——否则 worker 只能重新推断入口点、靠猜。一个仅仅与某个入口点存在相关性的字段只是一个线索，不是归因：任何能触发这个 job 的东西都能复现它。

**绝不记录 secret、token、密码或完整 PII。** 这是来自 `security-and-hardening` skill 的一条硬性规则——telemetry pipeline 是一条经典的数据泄露路径。按 allowlist 记录字段；不要整包记录 request body。

### 4. 指标

对 request-driven 的服务，在每个 endpoint 和每个外部依赖上埋 **RED**：**R**ate（请求/秒）、**E**rrors（失败率）、**D**uration（延迟 histogram，不是平均值）。对资源（队列、连接池、主机），用 **USE**：**U**tilization、**S**aturation、**E**rrors。

和 tracing 一样，厂商中立的路径是 OpenTelemetry metrics API（与第 5 步相同的 SDK 和 context）。下面的例子用的是 Prometheus 的 `prom-client`——一个常见的后端选择，不是唯一的选择；RED/USE 和 cardinality 规则两种路径下完全相同。

```typescript
import { Histogram } from 'prom-client';

const httpDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route', 'status_class'],  // '2xx', not '200'
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
});
```

**Cardinality 就是那个故障模式。** 每一个唯一的 label 组合都是一条独立的 time series。Label 必须来自小而固定的集合（route template、status class、provider 名）。绝不要用 user ID、原始 URL、错误消息或其他无界值做 label——那些属于日志和 trace。

```
OK as label:    route="/api/tasks/:id"   status_class="5xx"   provider="stripe"
NEVER a label:  user_id, email, request_id, full URL, error message text
```

永不追踪平均值，永远追踪百分位：平均值会藏起那 1% 体验极差的用户。用 histogram，读 p50/p95/p99。

### 5. 分布式 tracing

用 OpenTelemetry——它是厂商中立的标准，而 auto-instrumentation 以近乎零代码覆盖 HTTP、gRPC 和常见 DB client：

```typescript
// tracing.ts — must be imported before anything else
import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  serviceName: 'checkout-service',
  instrumentations: [getNodeAutoInstrumentations()],
});
sdk.start();
```

只在有意义的内部工作单元周围（例如 `applyDiscounts`、`chargeProvider`）添加手动 span，并附上 on-call 会用来过滤的 attributes。让 context 跨越每一个 async 边界传播——HTTP header、队列消息 metadata——否则 trace 会在断点处死掉。默认以低比例做 head-based 采样；如果你的后端支持 tail sampling，对错误保留 100%。

### 6. 告警

对**用户能感受到的症状**告警，不是对原因：

```
SYMPTOM (page-worthy):           CAUSE (dashboard, not a page):
error rate > 1% for 5 min        CPU at 85%
p99 latency > 2s                 one pod restarted
queue age > 10 min               disk at 70%
```

基于原因的告警会在什么都没出错时开火，并错过你没预测到的故障。基于症状的告警恰好在用户受到伤害时开火，无论原因是什么。

对你创建的每条告警的规则：

1. **它必须可行动。** 如果响应是“忽略它，它会自愈”，删掉这条告警。
2. **它链接到一个 runbook**——哪怕只有三行：它意味着什么、第一个该跑的查询、升级路径。
3. **它有一个阈值和持续时间**，依据是 SLO 或历史数据，不是拍脑袋。
4. 只用两个严重级别：**page**（面向用户，立即行动）和 **ticket**（降级，本周内行动）。第三档会变成噪音，教会人们无视一切。

#### 编写 Runbook

上面第 2 条规则要求每条告警都链接到一个 runbook。Runbook 的职责是回答三个问题，并且不需要读者动脑：正在发生什么、先检查什么、如果这解决不了该找谁。存放在 `docs/runbooks/`，以告警命名。

**最小可用 runbook（三行）：**

```markdown
# Runbook: High Error Rate on /api/tasks
**Means:** DB connection pool likely exhausted, or a bad deploy.
**First check:** `SELECT count(*) FROM pg_stat_activity WHERE backend_type = 'client backend';`
  — if count > pool limit, see Step 2. (Swap in the equivalent for your database.)
**Escalate to:** #db-oncall or engineering on-call rotation.
```

**什么时候值得在三行之上扩充：** 只有当第一个检查本身不足以做判断时，才添加步骤。一份覆盖三个最常见原因的五步 runbook，好过一份覆盖所有边缘情况、然后被人跳着扫的二十步文档。

**让 runbook 保持时新。** 把更新 runbook 作为关闭每一次用过它的事故的一部分——过期的 runbook 会建立起虚假的信心。如果某一步是错的或缺失的，在把事故标记为 resolved 之前就修好它。

### 7. 验证 telemetry 本身

埋点是代码；它会错。在宣布完工之前，触发那些路径，去看实际的输出：

- 在 staging 人为制造一个错误 → 用 `requestId` 在日志里找到它，确认字段是结构化的（不是 `[object Object]`）
- 发送测试流量 → 确认 metric series 以预期的 label 和合理的数值出现
- 在 tracing UI 里跟随一个请求跨服务 → 没有断裂的 span
- 每条新告警开火一次（临时调低阈值）→ 确认它到达正确的 channel，runbook 链接可用

## 常见合理化借口

| 合理化借口 | 现实 |
|---|---|
| "等它能工作了我再加日志" | “等之后”会变成“等第一次事故之后”，而那是发现自己是瞎子的最昂贵的时刻。边构建边埋点。 |
| "日志越多 = 越可观测" | 非结构化的噪音让事故处理更慢而不是更快。三个可查询的事件胜过三百行散文。 |
| "console.log 目前够用" | 非结构化的输出没法过滤、关联或告警。结构化 logger 只需要一次性多花五分钟。 |
| "等出了问题我们看 dashboard 就行" | 没有定义过问题的 dashboard 会把除了答案以外的一切都展示给你。从 on-call 的问题出发。 |
| "凡是不重要的都告警，以后再调" | 吵闹的 pager 会教会人们无视它。调优永远不会发生；被错过的真实 page 会发生。 |
| "把 User ID 做成 metric label 调试更方便" | 它同时也会让你的 metrics 后端轰然倒下。高 cardinality 的查找属于日志和 trace。 |
| "我们才两个服务，tracing 是杀鸡用牛刀" | 两个服务已经意味着日志回答不了的跨服务延迟问题。Auto-instrumentation 让这个成本微不足道。 |

## 危险信号

- 一个带重试、队列或外部调用的功能 PR，却没有新增任何 telemetry
- 用字符串插值而不是结构化字段拼出来的日志行
- 没有 correlation/request ID——每一行日志都是孤儿
- 一条日志流同时被 scheduler、webhook 和手动运行写入，却没有任何字段能说明这行是谁产生的
- 用 user ID、原始 URL 或错误消息文本做 label 的指标（cardinality 炸弹）
- 延迟只用平均值追踪，没有百分位
- 每天开火、被人确认却毫无动作的告警
- 在面向用户的错误率无人监控的同时，对原因（CPU、内存）的告警却在 page 真人
- 日志里出现 secret、token 或完整的 request body
- 把一个生产功能健康的证据寄托在 "It works on my machine" 上

## 验证

给一个功能埋点之后，确认：

- [ ] 这个功能的 on-call 问题已被写下来，且每个信号都对应其中一问
- [ ] 所有日志输出都是结构化的（JSON），有稳定的事件名，每行都带 correlation ID
- [ ] 每个被多个入口点写入的日志 sink 都带一个入口点字段：在运行启动处设置、随 correlation ID 一起传播，而不是在下游推断
- [ ] 任何一行日志里没有 secret、token 或未脱敏的 PII（抽查实际输出）
- [ ] 每个新 endpoint 和每个外部依赖都有 RED 指标，label 集合有界
- [ ] 延迟是 histogram；p95/p99 可查询
- [ ] 单个请求可以在 tracing UI 里端到端跟踪，没有断裂的 span
- [ ] 每条新告警都基于症状、有 runbook 链接，并且被试发过一次
- [ ] 在 staging 人为制造的故障，仅凭 telemetry 就能定位，不需要读源码

这份清单的速览版本（含发布前埋点 gate）见 `../../references/observability-checklist.md`。
