---
name: leeforge-templates
description: |
  leeforge/templates 项目的开发助手，掌握垂直切片模块开发、架构概念、配置参考和部署流程。
  触发条件：
  (1) 为 templates 项目新增业务模块（如"新增 order 模块"、"创建 comment 模块"）
  (2) 询问 templates 项目的架构原理（如"请求生命周期"、"Module 和 Plugin 的区别"）
  (3) 询问 templates 的配置（如"多租户怎么配置"、"JWT 参数在哪里改"）
  (4) 询问 templates 的部署（如"怎么构建镜像"、"remote-deploy 做了什么"）
  (5) 关键词包含：leeforge templates、垂直切片、NewPostModule、bootstrap/app.go、ModuleFactory
---

# Leeforge Templates 开发助手

## 项目定位

`leeforge/templates` 是基于 Leeforge Core 框架的 Gin HTTP 服务模板，用于快速搭建具备多租户/OU 权限的业务服务。

**技术栈**：Go 1.25+ / Gin / Chi（Core 管理）/ Ent ORM / PostgreSQL / Redis

## 新增业务模块（7 步）

> 详细代码模板见 `references/module-guide.md`

| 步骤 | 操作 | 文件 |
|------|------|------|
| 1 | 定义 Ent Schema | `ent/schema/<name>.go` |
| 2 | 运行代码生成 | `make generate` |
| 3 | 定义 DTO + 错误 | `modules/<name>/dto.go` |
| 4 | 实现 Service | `modules/<name>/service.go` |
| 5 | 实现 Handler（含 Swagger 注解） | `modules/<name>/handler.go` |
| 6 | 实现 Module（路由注册） | `modules/<name>/module.go` |
| 7 | 注册到 bootstrap | `bootstrap/app.go` → `ModuleFactories` |

注册后运行 `make swagger` 更新 Swagger 文档，`make dev` 启动服务验证。

## 参考文件导航

| 文件 | 内容 | 何时加载 |
|------|------|----------|
| `references/module-guide.md` | 7步详细指南 + 完整代码模板 | 新增/修改业务模块时 |
| `references/architecture.md` | 三层模型、请求生命周期、路由、认证上下文 | 解释架构原理时 |
| `references/config.md` | 所有 yaml 配置字段说明 | 回答配置问题时 |
| `references/deployment.md` | Docker 构建、部署配置、remote-deploy 流程 | 回答部署问题时 |
