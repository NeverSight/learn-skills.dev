---
name: use-task-gateway
description: '用于其他 App 接入 XGENT Task Gateway 完成异步任务，或排查鉴权、提交、幂等、进度与结果回收；需要时对齐 VM 执行器和 workflow 动作面。不用于网关自身开发发布或通用异步架构咨询。'
when_to_use: "用户会说「接异步任务网关」「任务重复提交了」「进度和结果查不到」时。"
---

# use-task-gateway

让调用方 App 形成可恢复的闭环：业务执行记录 → 提交任务 → 保存 task_id → 查询进度 → 消费终态结果。普通 App 默认走 Portal HTTP 租户面；任务由已注册服务的节点反向领取，网关不直接执行 payload 中的命令。

## 先确定接入边界

从调用方仓库查找 manifest、门户鉴权/换票封装、后端配置、业务 run/job/step 模型，以及目标服务的 payload 契约。复用其语言和已有 HTTP 客户端，不要求调用方使用 Rust，也不要求克隆网关源码。

先确认四项：实际 Gateway 基址、用户态或后台服务态、真实服务名、执行器所需输入。缺部署信息时先完成可配置的客户端与业务接线；仅在真实联调依赖该信息时索取，不能猜测生产地址、凭据或服务名。

| 当前工作 | 按需读取 |
| --- | --- |
| 用户代表调用、后台 SA、manifest 与换票排错 | [references/authentication.md](references/authentication.md) |
| HTTP 提交、持久化、幂等、状态、取消、回调、重试 | [references/task-api.md](references/task-api.md) |
| 新接 VM/CLI/API 执行能力、SSH 部署能力确认、任务一直 pending 或领取后失败 | [references/workers.md](references/workers.md) |
| 明确接入 workflow 引擎动作目录、placement/lease 或运行中止 | [references/workflow-actions.md](references/workflow-actions.md)；先核验引擎专用身份 |

实施普通 App 接入时读取前两份；已有执行服务时不用改节点部署。

## 接入面与凭据

| 调用方 | 接口及凭据 |
| --- | --- |
| 普通 Portal App 后端 | `https://<portal-host>/svc/task-gateway` + TDT；提交用 `task_gateway.submit`，发现/查询用 `task_gateway.read` |
| workflow 引擎专用动作调用 | 同 HTTP 基址下 `/workflow/v1/*`；仅 `kind=service`、`azp=workflow`、`task_gateway.workflow_actions` 同时满足 |
| 已明确采用原生 gRPC 的平台客户端 | 独立 gRPC 地址 + 网关 API Key（可叠加 mTLS），只可提交公开的平台服务；不得用来绕开租户 HTTP 授权 |
| VM 上的 `xgent-agent` | 独立 gRPC NodeService + Node Token；该 token 不用于 App 提交 |

`API_BASE_URL` 若指向内部 `portal-api`，只用于门户 API，不能直接拼 `/svc/task-gateway`。容器内直连 Gateway HTTP 地址仅采用部署配置已明确的地址。`:8081` 是内部支撑面，不是任务 API。旧 HTTP API-Key、admin-ui 和任务 SSE 路由已退场。

原生 gRPC 是独立协议：请求 payload 为 JSON 编码字符串，状态为 protobuf 枚举，任务不进入 Portal 租户可见集，且没有 HTTP 提交幂等契约。若用户明确选用它，依据目标部署的 `proto/src/gateway.proto` 和凭据约束接入，不套用本文 HTTP 重试策略。

## 调用方实施要点

1. **先有业务记录，再有网络提交。** 校验本 App 的租户、用户和业务对象权限；保存 run/step/attempt、目标服务、不可变提交体和幂等键。HTTP 成功取到 task_id 后立即关联保存。业务接口可返回“已受理”和本 App 的 run ID，后台继续查询。
2. **选择正确身份。** 用户发起的代表调用走用户换票；无用户上下文的后台任务走已授权 SA。长任务恢复需明确后续如何获得合法令牌；不能静默将用户授权失败改为高权限服务态执行。
3. **处理两层成败。** HTTP 非 2xx 或信封 `ok !== true` 均为 API 调用失败。`ok:true` 的提交响应仅表示受理；只有任务 `state=completed` 才表示执行成功。
4. **可恢复等待。** 后台按 task_id 轮询，进程重启后继续。使用有上限的退避、抖动和观察期限；等待超时返回“仍可查询”，保留任务关联。`partial_result` 是累积文本，每次替换；`result` 可为任意 JSON 值、字符串或 null。终态入库及后续业务动作按 run/attempt 幂等，避免并发观察者或重复通知多次消费结果。
5. **区分重传和重做。** 提交结果不确定时，在相同租户和来源归因下重用原 key 与原请求。预算耗尽后保留可恢复记录，不无界重试；不要换 key 规避冲突。明确决定重做已失败的业务执行才建立新 attempt；网关去重不保证执行副作用恰好一次。
6. **保留业务权限。** Gateway 详情和取消目前只按租户校验；同租户其他用户/来源 App 的任务不会自动被隔离。任何 task_id 都先经本 App 的业务记录授权，再向网关查询或取消；不以“能读到任务”判定访问权。

普通任务请求采用 `snake_case`；workflow 动作面采用另一套 `camelCase` 契约。不要把 `taskId/submissionKey/placement/abortIfRunning` 填进普通 `/v1/tasks` 并期待生效。普通面只能取消 pending，停止等待也不代表远端执行已停止。

## 验证与交付

按改动范围验证可观察结果：成功与执行失败；HTTP 200 + `ok:false`；提交已受理但客户端丢失响应后的同 key 恢复；进程重启恢复查询；JSON/文本结果；累积输出不重复；等待超时及 pending 取消/运行中取消拒绝。验证本 App 拦截同租户越权访问，而不只验证网关跨租户隔离。

可用本地 HTTP fixture 覆盖调用方契约；真实闭环应确认任务被目标执行器领取且结果被 App 消费。没有凭据或节点时，明确记录未验证部分，不用 mock 结果声称真实联调成功。仅在任务授权范围内发起测试任务；缺服务/容器时请求已有环境协助，不擅自安装或启动基础设施。

交付调用方代码/配置与实际验证结果，指出仍需的平台授权、服务/节点或凭据配置。仅咨询时解释需要的接线，不强制创建文档、部署机器或修改网关。

## 契约维护依据

本包任务接入契约以 `xgent-ai-task-gateway` 提交 `5e90da9` 为基线（2026-10-16 核对）；SSH 接入说明已核对 `aeca179`（1.9.3，2026-10-17）。可整目录移到其他 App 使用。引用的源码路径是维护线索，不是运行依赖。若能访问更新源码，优先核对 `gateway/src/portal/{gate,tasks,routes,onboarding}.rs`、`gateway/src/portal/workflow_actions/`、`gateway/src/agent/config.rs` 和 `proto/src/gateway.proto`；其次参考 `docs/API.md`、`docs/portal-app-contract.md`、`docs/PORTAL-APP-INTEGRATION.md`。部署可能落后于源码，需通过目标环境验证能力。
