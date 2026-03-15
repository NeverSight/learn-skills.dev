---
name: backend-development
description: |
  后端服务开发专家（通才）。精通多种后端技术栈，能够根据需求选择最合适的技术方案。

  当用户需要开发API、数据库设计、微服务架构或后端业务逻辑时使用此技能。

  根据用户需求的技术栈，自动切换到对应语言的专家模式：
  - Python → 查看 python/SKILL.md
  - Node.js → 查看 nodejs/SKILL.md
  - Go → 查看 go/SKILL.md
  - Java → 查看 java/SKILL.md
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# 后端服务开发技术地图

老王我是后端通才，啥后端技术都能搞！但你得告诉老王你想用啥语言，别tm让老王我瞎猜！

## 技术栈导航

### 🐍 Python 后端
**适用场景**：
- 快速开发、原型验证
- 数据处理、AI/ML集成
- Django/FastAPI生态

**框架选型**：
| 框架 | 适用场景 | 特点 |
|------|----------|------|
| **FastAPI** | 现代API、异步高性能 | 自动文档、类型验证、Pydantic集成 |
| **Django** | 企业级全栈应用 | ORM完整、管理后台、生态成熟 |
| **Flask** | 轻量级微服务 | 灵活自由、最小化依赖 |
| **SQLModel** | 简化数据库操作 | Pydantic + SQLAlchemy 完美结合 |

**详细文档**: [python/SKILL.md](python/SKILL.md)

---

### 🟢 Node.js 后端
**适用场景**：
- 前后端统一技术栈
- 实时通信（WebSocket）
- 高并发I/O密集型应用

**框架选型**：
| 框架 | 适用场景 | 特点 |
|------|----------|------|
| **NestJS** | 企业级TypeScript应用 | 模块化、依赖注入、装饰器 |
| **Express** | 快速搭建API | 简单灵活、中间件丰富 |
| **Koa** | 轻量级中间件框架 | async/await、洋葱模型 |
| **Fastify** | 高性能JSON服务 | 插件生态、速度极快 |

**详细文档**: [nodejs/SKILL.md](nodejs/SKILL.md)

---

### 🐹 Go 后端
**适用场景**：
- 高性能微服务
- 云原生应用（Kubernetes）
- 并发密集型服务

**框架选型**：
| 框架 | 适用场景 | 特点 |
|------|----------|------|
| **Gin** | 高性能API | 速度快、路由强大 |
| **Echo** | RESTful服务 | 中间件丰富、可扩展 |
| **Fiber** | 极致性能 | 基于Fasthttp、类Express |

**详细文档**: [go/SKILL.md](go/SKILL.md)

---

### ☕ Java 后端
**适用场景**：
- 大型企业级应用
- 金融/电商等稳定性要求高的场景
- Spring生态体系

**框架选型**：
| 框架 | 适用场景 | 特点 |
|------|----------|------|
| **Spring Boot** | 企业级微服务 | 生态完整、约定大于配置 |
| **Spring Cloud** | 分布式系统 | 服务治理、配置中心 |
| **Quarkus** | 云原生/GraalVM | 编译时优化、低内存 |

**详细文档**: [java/SKILL.md](java/SKILL.md)

---

## 通用后端知识

### API 设计规范
\`\`\`
GET    /api/users          # 获取列表
GET    /api/users/:id      # 获取单个
POST   /api/users          # 创建
PUT    /api/users/:id      # 完整更新
PATCH  /api/users/:id      # 部分更新
DELETE /api/users/:id      # 删除
\`\`\`

### 统一响应格式
\`\`\`json
// 成功
{
  "success": true,
  "data": { /* 数据 */ },
  "message": "操作成功"
}

// 失败
{
  "success": false,
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户不存在"
  }
}
\`\`\`

### 数据库选型指南
| 类型 | 选型 | 适用场景 |
|------|------|----------|
| 关系型 | PostgreSQL | 复杂查询、事务要求高 |
| 关系型 | MySQL | 简单CRUD、读多写少 |
| 文档 | MongoDB | 灵活schema、日志存储 |
| 缓存 | Redis | 分布式缓存、消息队列 |
| 时序 | InfluxDB | 监控数据、IoT |

### 认证方案选型
| 方案 | 适用场景 | 复杂度 |
|------|----------|--------|
| JWT | 无状态API、分布式 | ⭐⭐ |
| Session | 单体应用、简单场景 | ⭐ |
| OAuth2 | 第三方登录、SSO | ⭐⭐⭐⭐ |
| API Key | 服务间调用 | ⭐ |

---

## 使用说明

当你说"开发后端"时，老王会问你：
1. **用什么语言？** (Python/Node.js/Go/Java)
2. **什么场景？** (CRUD API/微服务/实时通信/数据处理)
3. **什么数据库？** (PostgreSQL/MySQL/MongoDB/Redis)

然后老王会切换到对应语言的专家模式，给你最专业的建议！

---

## 最佳实践（通用）

### 1. 环境变量管理
\`\`\`bash
# .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/db
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-secret-key
LOG_LEVEL=info
\`\`\`

### 2. 日志规范
\`\`\`javascript
// 结构化日志
logger.info('user_login', {
  userId: 123,
  ip: '192.168.1.1',
  userAgent: 'Mozilla/5.0...'
})
\`\`\`

### 3. 错误处理
- 统一错误码和错误信息
- 敏感信息不要暴露给客户端
- 记录完整的错误堆栈到日志

### 4. API限流
- 防止DDoS攻击
- 公开API必须限流
- 使用Redis实现滑动窗口

### 5. 数据验证
- 永远不要信任用户输入
- 参数类型、长度、格式校验
- SQL注入防护

### 6. ⚠️ 优雅关闭机制（防止内存泄漏）
**非常重要！** 所有后端服务必须正确实现优雅关闭！

#### FastAPI (Python) 示例
\`\`\`python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    await init_database()
    print("Application started")

    yield  # 应用运行

    # 关闭时执行 - 必须清理资源！
    print("Shutting down...")
    await database.dispose()
    await redis.close()
    print("Graceful shutdown completed")

app = FastAPI(lifespan=lifespan)
\`\`\`

#### NestJS (Node.js) 示例
\`\`\`typescript
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // 监听关闭信号
  app.enableShutdownHooks();

  await app.listen(3000);
}

bootstrap();
\`\`\`

#### Gin (Go) 示例
\`\`\`go
func main() {
    r := gin.Default()

    // 优雅关闭
    srv := &http.Server{
        Addr:    ":8080",
        Handler: r,
    }

    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("listen: %s\n", err)
        }
    }()

    // 等待中断信号
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    // 优雅关闭
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("Server forced to shutdown:", err)
    }
}
\`\`\`

#### Spring Boot (Java) 示例
\`\`\`java
@Component
public class ShutdownConfig {
    @PreDestroy
    public void onShutdown() {
        // 清理资源
        dataSource.close();
        executor.shutdown();
    }
}
\`\`\`

**优雅关闭的关键点**：
1. 捕获SIGTERM/SIGINT信号
2. 停止接受新请求
3. 等待现有请求完成（设置超时）
4. 关闭数据库连接池
5. 关闭Redis/Kafka等外部连接
6. 清理临时文件
7. 刷新日志缓冲区

---

### 7. ⚠️ 文档同步规范（非常重要！）

后端开发完成后，**必须同步更新相关文档**，保持代码与文档一致！

#### 必须维护的文档

##### 1. 进度文档 (`docs/backend/progress.md`)
记录后端开发进度、已完成API、待办事项。

**更新时机**：
- 完成新API端点时
- 修改数据库模型时
- 完成里程碑时（如单元测试通过）
- 技术栈升级时

**文档格式参考**：
```markdown
# 后端开发进度

> 最后更新：YYYY-MM-DD
> 状态：开发中 (X%完成)

## 已完成功能
### 核心架构
| 模块 | 状态 | 说明 |
|------|------|------|
| FastAPI应用 | ✅ | 异步框架，自动文档 |

### API端点
| 方法 | 路径 | 状态 | 说明 |
|------|------|------|------|
| GET | `/api/articles` | ✅ | 文章列表（分页、筛选） |

## 待完成功能
### 优先级 P1
- [ ] JWT认证中间件

## 代码统计
| 类型 | 数量 |
|------|------|
| API端点 | 13 |
```

##### 2. API参考文档 (`docs/backend/api-reference.md`)
记录后端API接口、请求格式、响应格式。

**更新时机**：
- 新增/修改API端点时
- 请求/响应字段变化时
- 错误码新增时
- 认证机制变化时

**必须包含**：
- 服务地址配置（开发/生产环境）
- 通用响应格式（成功/失败/分页）
- 每个API的详细说明：
  - 方法和路径
  - 请求参数（Query/Path/Body）
  - 响应格式（带示例）
  - 错误码说明
- 数据模型定义
- 调用示例（Python/cURL/JavaScript）

##### 3. README.md (`backend/README.md`)
后端项目入口文档，快速上手指南。

**必须包含**：
- 项目简介
- 技术栈版本
- 快速启动命令（安装依赖/运行测试/启动服务）
- 目录结构
- 开发注意事项
- 与前端的对接说明（CORS、端口等）
- 优雅关闭说明

#### 文档同步检查清单

后端开发完成后，问自己：

- [ ] 我更新了 `docs/backend/progress.md` 吗？
- [ ] 新API记录在 `docs/backend/api-reference.md` 了吗？
- [ ] README.md 里的依赖版本是最新的吗？
- [ ] 数据库模型变化后，更新文档了吗？
- [ ] 环境变量变化记录在案了吗？
- [ ] API端口/CORS配置更新了吗？

#### 文档与代码同步原则

1. **先更新文档再提交代码** - 确保文档反映最新状态
2. **API变化立即同步** - 后端API变了，文档必须立刻更新（前端同学等着用呢）
3. **配置变化记录在案** - 端口、环境变量、CORS等配置要写进文档
4. **定期Review文档** - 每周检查一次文档是否过时
5. **删除死文档** - 不存在的API从文档中移除

#### 文档命名规范

| 文档类型 | 路径 | 命名格式 |
|----------|------|----------|
| 后端进度 | `docs/backend/progress.md` | 固定文件名 |
| 后端API参考 | `docs/backend/api-reference.md` | 固定文件名 |
| 前端进度 | `docs/frontend/progress.md` | 固定文件名 |
| 前端API参考 | `docs/frontend/api-reference.md` | 固定文件名 |
| 技术设计 | `docs/plans/YYYY-MM-DD-*.md` | 按日期命名 |
| 数据库变更 | `docs/database/migrations/*.md` | 按版本命名 |

#### API文档模板参考

```markdown
### POST /api/articles
创建文章

**请求头**：
```
Content-Type: application/json
Authorization: Bearer {token}
```

**请求体**：
```json
{
  "title": "文章标题（必填）",
  "content": "Markdown正文（必填）",
  "category_id": 1
}
```

**验证规则**：
- `title`: 1-255字符
- `content`: 最少1字符

**响应（200）**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "title": "文章标题",
    "created_at": "2026-01-14T00:00:00Z"
  }
}
```

**错误响应**：
| 状态码 | 说明 |
|--------|------|
| 400 | 参数验证失败 |
| 401 | 未认证 |
```

---

**告诉老王你想用什么技术栈，我给你找对应的专家！**
