---
name: make-app-observability
description: Use when creating, integrating, reviewing, or debugging a Make App's default Trace ID chain, traceparent and X-Log-Id propagation, safe correlated logs, or @qfei-design/make-app-observability error notices. Every new Make App includes this baseline even when the user does not mention observability. Covers direct-gateway and Service-fronted Apps and AI transports when present. Does not own authentication, Service route design, AI protocol, tracing backend/exporter deployment, runtime packaging, or page layout.
metadata:
  version: 0.1.1
---

# make-app-observability

所有新建 Make App 默认接入 Trace ID。存量 App 的本次任务涉及业务请求、AI transport、错误出口或发布门禁时，应核对相关 Trace 链路并补齐缺失环节；无关改动只报告发现的缺失，不擅自扩大本次任务范围。Trace ID 的默认范围是 App 的业务请求及其错误出口，包括启用时的 AI JSON、SSE 和二进制传输。静态资源和 OAuth 回调不属于 UI 业务请求适配器的范围。

## 主责与边界

本 Skill 负责跨 UI、可选 Service 和 Make Gateway 的 Trace ID 生成、传递、关联日志、错误分类与统一展示。`@qfei-design/make-app-observability` 提供错误呈现模型及 React 组件；它不会发请求、创建 Span、传 Header、记录日志或配置导出器。不能把安装该包等同于完成 Trace 链路，也不能把仅有 Trace ID 关联宣称为已接入集中式 Trace 后端。

- 认证请求与 cookie/session 机制交给 `make-app-auth`；在其共享已认证请求适配器中注入追踪 Header，不另写裸请求或浏览器 token 逻辑。
- Service 路由、UI-Service 业务合同和 Make adapter 交给 `make-app-service`；本 Skill 定义跨这些边界的 Trace 不变量。
- AI 路由、流式事件和取消语义交给 `make-ai-assistant`；其已认证 JSON、SSE、二进制传输沿用同一追踪合同。
- 发布脚本和交付门禁交给 `make-app-runtime`；该 Skill 调用本 Skill 的审计器。
- 页面布局与错误出口的位置交给 `makeui`；错误卡片和 Trace ID 展示规则由公共包负责。

## 默认接入流程

1. 判定 App 的请求拓扑：UI 直连 Make Gateway，或 `UI -> Service -> Make Gateway`。两种拓扑都必须经过一个共享、已认证的 UI 请求适配器。
2. 在 UI 的每次业务请求开始时创建有效的 W3C Trace 上下文，保存本次 128-bit 非零 Trace ID。请求 Header 同时写入 `traceparent` 和等于其中 trace-id 的 `X-Log-Id`；同一次请求的成功或失败使用创建时保存的 ID，重试作为新的网络尝试重新创建并保留对应 ID。不要通过 URL query 传 Trace 信息。
3. Service-fronted App 在请求入口校验入站 Header，缺失或非法时生成安全 Trace ID；所有响应返回 `X-Log-Id`。向 Make Gateway 转发时只使用已校验且一致的追踪 Header，Service 安全日志带同一个 `traceId`。直连模式则由共享 UI 适配器把 Header 送到 Gateway。
4. 统一错误出口区分 HTTP 非 2xx、网络异常和 HTTP 2xx 业务码异常。收到响应时在 Span 记录实际 HTTP 状态码；业务码失败和 HTTP 非 2xx 标记为错误，网络异常不虚构状态码。使用公共包的 `MakeAppErrorNotice`；只有 HTTP 和网络错误显示可复制的 Trace ID。失败时优先保留本次请求创建的 ID，避免无响应的网络错误丢失关联信息。
5. 当 App 使用 AI transport 时，JSON、SSE、文件和二进制请求也发送这两个 Header；HTTP 非 2xx 即使有响应体也要标记 Span 为错误。不能恢复通过 `__traceparent` 等 query 参数传递 Trace 的旧做法。
6. 先补行为测试，再运行 `scripts/audit-trace-contract.mjs` 和 App 原有测试。审计是源代码接线检查，不能代替真实请求的端到端断言。

## 按需阅读

| 工作 | 读取 |
| --- | --- |
| 安装公共包、公开入口、错误卡片与移动端全局出口 | `references/package-integration.md` |
| UI、Service、Gateway 和 AI 的 Trace 链路及安全边界 | `references/trace-chain.md` |
| 行为测试、静态审计、发布检查和排障 | `references/testing-and-audit.md` |

安装或升级时，先从目标 App 已安装包的 `package.ai.json` 读取 `readOrder`，按声明顺序阅读公开文档；不要从包内 `src` 或 `dist` 深层导入，也不要把本 Skill 写的示例当成高于目标安装版本的公开 API。

## 交付条件

- 新建 Make App 的项目级发布检查包含 `trace:audit`；发布前同时通过适用的行为测试和审计。已有 App 使用自身的兼容运行时及发布命令，不为接入追踪强制迁移包管理器。
- 审计命令：`node skills/make-app-observability/scripts/audit-trace-contract.mjs <project-root> --mode auto`。复制到 App 项目本地的脚本才可写入项目 `package.json`，不要引用开发者机器上的 Skill 绝对路径。
- 不记录或传给 UI `Authorization`、Cookie、token、业务请求正文、AI 提示词或原始内部错误。日志只写安全的路由、方法、状态、错误类别及 `traceId`。
