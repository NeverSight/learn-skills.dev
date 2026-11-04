---
name: codeguard-security-api
description: 审查和设计接口鉴权、数据权限、文件上传与 apikey/timestamp/signature 防重放机制；当用户编写或审查 API、Shiro/Spring Security 注解、多租户过滤、文件上传，或询问越权/接口安全时使用。
license: Apache-2.0
compatibility: 需要接口路由、鉴权链、数据范围与部署边界上下文；不会导出、上传或记录真实凭据和个人数据。
---

# 接口安全规范（越权 · 数据权限 · 文件上传 · 签名）

依据：PartMe.AI 开发规范「接口安全规范」。两大类常见漏洞：**越权绕过**、**文件上传漏洞**。

## 一、功能权限检查（防越权）

### 登录控制
- 单设备登录、登录环境检测、登录异常检测

### 接口鉴权注解（按框架选用，AI 写接口必须带）

**Shiro：**
```java
@RequiresAuthentication                    // 已认证
@RequiresUser                              // 已登录（含 rememberMe）
@RequiresGuest                             // 游客
@RequiresPermissions("sys:user:view")      // 单权限
@RequiresPermissions({"a", "b"}, logical = Logical.OR)   // 多权限任一
@RequiresRoles("admin")                    // 角色
```

**Spring Security：**
```java
@PreAuthorize("isAuthenticated()")
@PreAuthorize("hasAuthority('sys:user:view')")
@PreAuthorize("hasAnyAuthority('a','b')")
@PreAuthorize("hasRole('ADMIN')")
@PreAuthorize("hasAnyRole('ADMIN','OPS')")
```

AI 行为：写新增/修改/删除/查询接口时，若项目已用上述框架，**必须**补鉴权注解；缺失即提示。

## 二、数据权限检查（防越权取数）

- 请求参数检查：增删改查接口对数据归属参数做校验，
  如 `@RequiresDataPermissions`（校验学校代码等字段）+ `DataScopeProvider` 本地校验
- 返回数据过滤：按角色/用户设置数据访问范围，查询时动态追加筛选条件

AI 行为：写查询接口时注意 tenantId / shopId / 数据归属字段的过滤；禁止返回全表无过滤数据。

## 三、文件上传检查（三层控制）

| 层 | 控制项 |
|---|---|
| 前端 | 上传前回调校验：格式白名单（xls/doc/pdf/zip 等）+ 大小（如 ≤50MB） |
| 后端 | 基于 JSR303 Bean Validation 扩展注解（如 `@FileNotEmpty`）：非空、扩展名白名单、最大尺寸（如 ≤100MB）、MIME 类型检测 |
| 运维 | Nginx `client_max_body_size` 限制请求体（默认约 2MB，按需调整并 reload） |

风险：不限类型/大小/路径/文件名 → 攻击者传后门拿 WebShell。文件名存储须重命名（UUID），禁止用户可控路径拼接。

## 四、接口签名机制（延伸）

对外暴露的敏感接口采用 **apikey + timestamp + signature**：

1. 客户端：`signature = HMAC(secret, apikey + timestamp + body)`
2. 服务端：校验 apikey 有效 → timestamp 在窗口内（防重放）→ 重算 signature 比对
3. 建议窗口 ±5 分钟 + nonce 缓存防重放

## 五、AI 自查清单（写接口时逐项过）

- [ ] 有鉴权注解（或网关层已统一鉴权）
- [ ] 涉及数据归属的查询有数据权限过滤
- [ ] 文件上传有：白名单 + 大小限制 + 重命名存储
- [ ] 对外接口有签名/防重放
- [ ] 敏感返回字段已脱敏（见数据安全技能）

## 不适用范围（什么时候不该用）

- 主要问题是静态代码风格、依赖 CVE 或数据库加密，应交给对应专用技能。
- 仅根据控制器注解就要求证明“无越权”；还需跟踪服务、查询和缓存路径。
- 需要使用真实凭据或生产个人数据进行测试。

## 标准 Workflow

### Step 1：建立资产和信任边界

列出身份来源、网关、服务、数据库、对象归属、外部调用方和文件存储。

### Step 2：跟踪请求路径

从 route 到 controller/service/query/response 逐层核对认证、功能权限和对象层授权。

### Step 3：检查输入与上传

确认 schema、大小、内容类型、文件头、重命名、存储路径、执行权限和杀毒/隔离策略。

### Step 4：验证失败路径

覆盖未登录、低权限、跨租户、重放、超大文件、伪造 MIME 和非所有者资源。

### Step 5：输出修复与测试证据

为每个发现列出信任边界、可利用前置、最小修复、阴性测试和剩余风险。

## Rules

1. tenant/user/role 等归属信息不能直接信任客户端参数。
2. 认证通过不等于对象层授权通过。
3. 签名比对必须常量时间，timestamp 与 nonce 都必须验证。
4. 文件扩展名不是可信类型证据。

## Gotchas

1. **查询后内存过滤可泄露侧信道**：应尽量在数据源层限定范围。
2. **批量接口易漏掉单条对象授权**：需对每个 ID 验证归属。
3. **缓存 key 可造成跨租户泄露**：必须包含受信的租户维度。
4. **文件内容与 MIME 可不一致**：需检查 magic bytes 和安全解析。
5. **反向代理限制不能取代应用层验证**。
6. **仅依靠时间戳不能防止窗口内重放**：还需 nonce/idempotency key。

## 按需加载资源

- 决策和交接读取 `references/rules/decision-contract.md` 与 `references/operations/evidence-playbook.md`。
- 只打开 `examples/` 中匹配当前资产的示例。
