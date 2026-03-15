---
name: brainstorm
description: |
  当需要探索方案、头脑风暴、创意思维时自动使用此 Skill。

  触发场景：
  - 不知道怎么设计
  - 需要多种方案对比
  - 架构讨论与功能规划
  - 业务扩展方向探索
  - 模块划分决策

  触发词：头脑风暴、方案、怎么设计、有什么办法、创意、讨论、探索、想法、建议、怎么做、如何实现、有哪些方式、能不能做、可以实现吗
---

# 头脑风暴框架

## 本项目技术约束（方案边界）

### 已集成技术

| 层面 | 技术 | 说明 |
|------|------|------|
| **框架** | Spring Boot 3.5.9 | 核心框架 |
| **ORM** | MyBatis-Plus 3.5.16 | 数据持久层 |
| **缓存** | Redis + Redisson（Caffeine 本地缓存）| 分布式+本地缓存 |
| **消息** | Redis Streams | 轻量消息队列 |
| **定时** | SnailJob + @Scheduled | 分布式定时任务 |
| **认证** | Sa-Token 1.44.0 | 权限与认证 |
| **实时** | WebSocket + SSE | 实时推送 |
| **存储** | AWS S3 SDK | MinIO 兼容 |
| **加密** | AES/RSA | 字段级加密 |
| **短信** | SMS4j | 多平台短信 |
| **邮件** | Spring Mail | 邮件发送 |
| **登录** | JustAuth | OAuth2（30+ 平台） |
| **Excel** | FastExcel | 导入导出 |

### 需自行扩展的技术

| 技术 | 场景 |
|------|------|
| **RocketMQ** | 高吞吐消息队列、分布式事务 |
| **MQTT** | IoT 设备通信（mica-mqtt） |
| **LangChain4j** | AI 大模型集成 |
| **支付模块** | 微信/支付宝（IJPay 等） |

### 可复用 Common 模块（24个）

```
核心: core, web, security, log, doc, bom
数据: mybatis, redis, json, encrypt, sensitive, oss, excel
认证: satoken, tenant, social
通信: mail, sms, websocket, sse
业务: job(SnailJob), idempotent, ratelimiter, translation
```

---

## 决策维度（必须考虑）

| 维度 | 关键问题 | 实现要点 |
|------|---------|---------|
| **三层架构** | 如何分层？ | Controller -> Service -> Mapper（无 DAO 层） |
| **模块归属** | 属于哪个模块？ | sys/demo/wf（标准）或 b/m/iot/crm（业务） |
| **多租户** | 需要隔离？ | Entity 继承 TenantEntity，自动 SQL 过滤 |
| **多端** | 哪些端需要？ | 同一套 API，按需扩展前端 |
| **多数据库** | 要兼容多库？ | SQL 脚本同步 MySQL/Oracle/PG/SQLServer |

### 方案评估矩阵

```markdown
| 方案 | 复用度(25%) | 多端(20%) | 多租户(20%) | 多数据库(15%) | 开发量(20%) | 总分 |
|------|-------------|-----------|-------------|---------------|-------------|------|
| 方案A | ? | ? | ? | ? | ? | ? |
| 方案B | ? | ? | ? | ? | ? | ? |

评分说明：1-10分，分数越高越好
- 开发量：分数越高=工作量越少
```

---

## 方案探索模板

### 问题定义

```markdown
- **是什么**: [功能描述]
- **模块归属**: base / mall / crm / iot / 新模块
- **端支持**: PC端 / 移动端 / 两者
- **租户**: 需要隔离 / 系统级
- **数据库**: MySQL only / 多库兼容
```

### 可复用资源盘点

```markdown
| 资源 | 类型 | 复用程度 |
|------|------|---------|
| ruoyi-common-xxx | 模块 | 完全/部分/参考 |
| 现有 Xxx 功能 | 代码 | 参考模式 |
```

### 方案对比（至少2个）

```markdown
### 方案 A: 最大复用（优先考虑）
- **复用**: [列出模块/代码]
- **新开发**: [列出新写部分]
- **优缺点**: [简述]

### 方案 B: 适度扩展
- **复用**: [列出模块/代码]
- **新开发**: [列出新写部分]
- **优缺点**: [简述]
```

### 推荐方案

```markdown
**推荐**: 方案 [X]
**理由**: [1-3条]
**实施步骤**:
1. [ ] 数据库设计 -> database-ops
2. [ ] 后端开发 -> crud-development
3. [ ] 测试验证
**风险点**: [风险] -> [应对策略]
```

---

## 典型场景速查

### 新增业务管理模块

```
需求示例：优惠券管理

模块归属 -> mall（商城相关）
功能拆解 -> 模板管理 / 发放 / 使用 / 统计
可复用 -> Ad模块(CRUD模板) + redis(分布式锁) + SnailJob(过期作废) + 字典(类型/状态)
表设计 -> m_coupon_template, m_coupon_record
```

### 接入第三方服务

```
可复用 -> encrypt(密钥存储) + redis(结果缓存) + Platform(配置存储)
实现 -> 接口+实现类（策略模式支持扩展）
注意 -> 密钥加密 + @RateLimiter频率限制 + 失败降级
```

### 实时通信

```
WebSocket(双向,已集成) ✅ 首选 | SSE(单向推送,已集成) | 轮询(不推荐)
消息类型 -> 广播(全连接) / 点对点(特定用户) / 组播(群组) / 主题订阅
可复用 -> websocket模块 + redis(在线状态/多实例同步)
```

### 数据统计报表

```
方案选择 -> 小数据(<100万):实时查询 | 中数据:预计算+缓存(推荐) | 大数据:分析引擎
可复用 -> FastExcel(导出) + SnailJob(预计算) + redis(结果缓存)
```

### AI 功能集成

```
需自行引入 LangChain4j Maven 依赖
可复用 -> SSE(流式响应) + redis(会话上下文)
模型推荐 -> DeepSeek(国产便宜) / ChatGPT / Claude
需开发 -> ChatSession表 + ChatMessage表 + AiService + 模型配置
```

---

## 常见问题快速决策

| 问题 | 推荐 | 原因 |
|------|------|------|
| 新功能放哪个模块？ | 看业务相关性 | base=基础、mall=商城、crm=客户、iot=设备 |
| WebSocket vs SSE？ | WebSocket | 双向通信、已有封装 |
| RocketMQ vs Redis？ | Redis 优先 | Streams 简单场景够用 |
| 要支持多数据库？ | 是 | 项目标准，SQL 脚本同步 4 库 |
| 要支持多租户？ | 业务数据要 | TenantEntity 自动隔离 |
| 定时任务用什么？ | 简单->@Scheduled，复杂->SnailJob | 按复杂度选 |
| 文件上传？ | AWS S3 SDK | 已集成、MinIO 兼容 |
| 敏感数据？ | @EncryptField | ruoyi-common-encrypt |
| 防重复提交？ | @RepeatSubmit | ruoyi-common-idempotent |
| 接口限流？ | @RateLimiter | ruoyi-common-ratelimiter |
| 分布式锁？ | Redisson | 已集成 |

---

## Skill 联动路径

```
brainstorm（本 Skill）
    |-- 需要建表 -> database-ops
    |-- 需要后端开发 -> crud-development
    |-- 需要定时任务 -> scheduled-jobs
    |-- 需要安全认证 -> security-guard
    |-- 需要数据权限 -> data-permission
    |-- 需要异常处理 -> error-handler
    |-- 需要技术对比 -> tech-decision
    |-- 需要代码规范 -> code-patterns
```

| 头脑风暴结论 | 下一步 Skill | 触发方式 |
|-------------|-------------|---------|
| 需要新建业务模块 | crud-development | "帮我开发 xxx 模块" |
| 需要数据库设计 | database-ops | "帮我设计 xxx 表" |
| 需要安全认证 | security-guard | "怎么控制权限访问" |
| 需要技术对比 | tech-decision | "Redis 还是本地缓存好" |
