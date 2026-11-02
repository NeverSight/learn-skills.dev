---
name: use-llm-gateway
description: '用于其他 App、SDK 或编码工具接入 XGENT LLM Gateway 的统一 /v1 调用面，或迁移旧调用、排查凭证、幂等及媒体任务恢复。不用于网关自身开发发布或通用提示词优化。'
when_to_use: "用户会说「接一下大模型网关」「换掉旧的模型调用」「媒体任务丢了怎么恢复」时。"
---

# use-llm-gateway

把模型调用接进调用方已有的业务流程：选对模型与凭证，发送原生请求，保存调用键和任务关联，正确处理未知结果与产物回收。本包面向**统一 `/v1` 版本**；源码或本 skill 的存在不证明目标环境已经升级。

## 先确定调用方上下文

读取当前 App 的 HTTP/SDK 封装、配置、manifest、鉴权与业务 job/run/attempt 模型。复用其语言、客户端和配置约定，不要求克隆门户源码或新建一套任务系统。

先确定实际网关服务根地址、租户、可用凭证、所需能力和目标环境版本。缺部署资料时可先完成可配置的客户端与本地契约测试；真实联调前再索取缺项，不猜生产地址、模型或凭证，也不因新接口404静默回退旧调用面。

| 当前工作 | 按需读取 |
| --- | --- |
| 签服务令牌、选模型、构造请求、解析成功体 | [references/api.md](references/api.md) |
| 幂等、丢回包、超时、任务查询/取消/ACK、计费判定 | [references/recovery.md](references/recovery.md) |
| 从旧媒体、推理、审核或服务调用台账迁移 | [references/recovery.md 的迁移对照](references/recovery.md#旧调用迁移) |

实现调用读取第一份；涉及非流式生成、后台任务、重试或迁移时同时读取第二份。普通文本调用不必加载全部媒体细节。

## 两种凭证，一张调用面

| 身份 | 公共调用方式 |
| --- | --- |
| API Key：`xuak_` 或仍有效的 `xgw_` | `Authorization: Bearer <key>`；按这把 Key 隔离 |
| 绑定调用 App 的服务令牌 | 同一 Bearer 头；票为 `kind=service` 且有非空 `azp`，按 App 隔离 |
| 用户 TDT，包括用户 Token Exchange 产物 | **不能调用公共 `/v1`**，返回401；不能因用户点击了生成就把用户票直接传给网关 |

用户触发的 App 后端生成仍须先验证本 App 的用户/租户/业务权限，再使用已授权的 API Key 或 App 服务令牌。`X-Actor-User-Id` 可记录已验证的发起用户，但不授予权限；鉴权失败不自动切换到更宽身份。

GET 使用 `llm_gateway.read`，生成POST、取消、ACK、封存及DELETE使用 `llm_gateway.write`。API Key 的网关write资格兼具读；服务令牌按实际scope校验。不要把SA密钥或共享API Key打进前端bundle。

**协议分界**：`/v1/*` 返回原生JSON、字节或SSE，失败用真实HTTP状态；`GET /api/v1/models` 仍是带TDT的管理信封 `{ok,data}`。公共调用直接使用服务端HTTP/适配的SDK，不经过门户iframe的 `callService` / postMessage代理。

## 实施时保留这些事实

1. **先保存执行意图，再提交。** 对需要恢复的非流式调用，在业务attempt中持久化凭证主体、逻辑模型、不可变请求及 `Idempotency-Key`。同一意图重传保持原键、原内容、标记与策略；新的一次业务执行才用新键。流式调用不能带键。
2. **HTTP成功不等于业务完成。** 202是任务受理；语音成功可能直接是音频字节；审核的review/unsupported不是放行。先按状态和Content-Type分派，再解析对应成功体，不能统一取 `response.data.data`。
3. **超时后恢复原调用。** 保存成功头 `X-Gateway-Task-Id`、202的id，或错误的 `details.taskId`。504 TASK_RUNNING后查同一任务，不再POST生成。仅有键时先回读 `/v1/calls`；没有免费终局证据时不自动换键重做。
4. **资源归属不随token字符串猜测。** 查询、下载、取消和ACK使用同租户、同主体。同App的新服务令牌可续查；另一把API Key或另一App不能读旧资源，不能靠actor、标记或taskId跨主体恢复。
5. **媒体先归档再ACK。** 用返回的 `asset_key` 取网关自持字节，校验并可靠写入调用方存储后再ACK。`/v1/...` 资源路径相对**网关服务根目录**，拼接时保留 `/svc/llm-gateway` 前缀；不能直接当公开图片地址，也不向供应商地址转发网关Bearer。
6. **限制自动重试。** 尊重 `x-should-retry:false`；接管SDK对写请求的默认重试，避免HTTP状态触发重复付费。后台查询可有退避与观察期限；期限到达保留可恢复关联，停止本轮等待，不制造新的生成。

## 验证与交付

按改动覆盖实际行为：所用能力成功与原生错误、用户票拒绝、跨主体拒绝、同键重放/不同请求冲突、丢回包恢复；媒体补充202、504同任务恢复、查询失败重试、终态失败/取消、下载后ACK与410。若接入审核，验证不可用或不支持时不会当作allow。

本地HTTP fixture可验证调用方行为；真实联调只在任务授权的环境和费用范围内进行。没有凭证或目标版本未升级时，明确未验证部分，不把mock成功写成供应商实测，也不为完成接入擅自部署网关、改门户授权或切换旧接口。

交付当前App的代码/配置与实际验证结果，说明仍需的平台安装、scope、模型或版本条件。纯查询时解释接线即可，不强制落文档、执行调用或改基础设施。

## 契约维护依据

本包按门户调用面统一实现 `17104d5e` 核对，可整目录导出给其他App。若可访问该版本源码，维护线索是 `docs/llm-gateway-service-calls.md`、`docs/llm-gateway-models-contract.md`、`docs/内容安全审核接入指引.md` 以及 `apps/llm-gateway-server/src/{lib/caller.ts,routes/gateway-ext.ts,routes/generation.ts}`；这些不是使用本包的运行依赖。目标部署的实际版本和能力需单独确认。
