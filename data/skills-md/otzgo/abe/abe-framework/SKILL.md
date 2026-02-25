---
name: abe-framework
description: ABE 框架完整开发技能集，提供现代化 Go HTTP RESTful API 应用开发的全套解决方案。核心功能包括：模块化引擎架构、标准化控制器路由注册、全局和路由级中间件系统、依赖注入容器（支持全局和请求级作用域）、多语言国际化（i18n）支持、基于 JWT 和 Casbin 的访问控制体系、异步事件总线机制、高性能协程池管理、可扩展插件机制、配置管理系统（支持多层配置优先级）、GORM 数据库集成、结构化日志系统、表单验证框架、定时任务调度（Cron）、CORS 跨域支持等。适用于构建企业级 Web 服务、微服务架构应用、API 网关、后台管理系统等场景。框架采用松耦合设计，支持 UseCase 业务逻辑模式，提供完善的错误处理机制和性能监控能力，帮助企业快速构建稳定、可维护的分布式应用系统。
---

# ABE Framework 开发指南

## 框架概述

ABE (API Builder Engine) 是一个现代化的 Go 语言 HTTP RESTful API 开发框架，整合了主流开源组件，提供开箱即用的企业级解决方案。

### 核心特性
- **模块化架构**：基于依赖注入实现松耦合设计
- **路由和控制器**：标准化的控制器模式和路由注册机制  
- **中间件管理**：灵活的全局和路由级中间件系统
- **国际化支持**：内置多语言 i18n 支持
- **权限控制**：集成 Casbin 访问控制
- **事件驱动**：基于 Watermill 的异步事件总线
- **协程池管理**：高效的并发任务处理
- **插件机制**：可扩展的插件系统

## 快速开始

### 1. 初始化引擎
```go
package main

import "github.com/otzgo/abe"

func main() {
    // 创建引擎实例
    engine := abe.NewEngine()
    
    // 配置和注册组件
    // ...
    
    // 启动服务
    engine.Run(abe.WithBasePath("/api/v1"))
}
```

### 2. 核心概念
- **Engine**：应用主容器，协调所有组件
- **Controller**：业务逻辑控制器，实现标准化接口
- **Middleware**：HTTP 中间件，处理横切关注点
- **UseCase**：业务用例模式，封装具体业务逻辑
- **Plugin**：可插拔扩展模块

## 开发流程

当你需要开发 ABE 应用时，请按以下顺序查阅相关文档：

1. **引擎核心功能** - 了解 Engine 实例创建和服务获取
2. **控制器开发** - 学习标准化控制器设计和路由注册
3. **中间件系统** - 掌握中间件开发和使用技巧
4. **依赖注入** - 理解容器管理和依赖注入模式
5. **插件机制** - 扩展框架功能的插件开发

## 最佳实践

### 项目结构建议
```
project/
├── cmd/app/           # 应用入口
├── internal/
│   ├── controllers/   # 控制器层
│   ├── usecases/      # 业务用例层
│   ├── dtos/          # 数据传输对象
│   └── models/        # 数据模型
├── configs/           # 配置文件
└── docs/              # 文档
```

### 代码组织原则
- 控制器只负责路由注册和参数处理
- 业务逻辑放在 UseCase 中
- 依赖通过构造函数注入
- 使用标准化的错误处理和响应格式

## 详细参考资料

请查看以下参考文档获取更详细的信息：

### 核心功能
- [引擎核心功能详解](references/engine-core.md) - Engine 实例管理、服务获取器、生命周期管理
- [控制器开发指南](references/controllers.md) - Controller 接口实现、路由注册、RESTful 设计
- [依赖注入容器](references/dependency-injection.md) - 全局和请求级依赖注入、UseCase 模式

### 系统集成
- [配置管理系统](references/configuration.md) - 多层配置、环境变量、命令行参数
- [数据库集成](references/database.md) - GORM 使用、模型定义、查询优化
- [日志系统使用](references/logging.md) - 结构化日志、上下文管理、性能监控

### 功能特性
- [中间件系统使用](references/middlewares.md) - 全局中间件、路由级中间件、自定义中间件开发
- [CORS 中间件配置](references/cors.md) - 跨域资源共享、安全配置、常见问题
- [表单验证系统](references/validation.md) - 数据验证、多语言支持、自定义规则
- [多语言国际化](references/i18n.md) - 翻译文件、语言切换、模板使用

### 安全与运维
- [访问控制机制](references/access-control.md) - JWT 认证、Casbin 权限、中间件使用
- [事件驱动系统](references/events.md) - 消息发布订阅、异步处理、事件总线
- [定时任务调度](references/cron.md) - Cron 表达式、任务管理、监控告警
- [插件机制详解](references/plugins.md) - 插件接口、生命周期钩子、插件开发示例

### 协程与性能
- [协程池管理](references/goroutine-pool.md) - 性能优化、资源管理、任务调度