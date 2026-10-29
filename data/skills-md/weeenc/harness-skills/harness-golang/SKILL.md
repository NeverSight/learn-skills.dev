---
name: harness-golang
description: Golang 语言规范包 — 编码规范、工程结构（SDD-TDD/开发流程/运行时可靠性共享自 harness-core）
---

# Harness Golang — Go 语言规范包

本包为 Go 项目提供完整的 Harness 开发规范体系，基于：

- **基线框架**: Gin / go-zero / Echo / Fiber / Chi / Beego / Go-Kit / Go-Kratos / Gorilla Mux / Kitex / Hertz / Iris / Macaron / Tango / GoFrame / LangChainGo / Google ADK-Go / cloudwego eino / tRPC-Agent-Go / Firebase Genkit / Anyi
- **运行时**: Go 1.22+
- **测试框架**: go test + testify
- **代码规范**: Go Code Review Comments + Uber Go Style + golangci-lint（go vet + staticcheck）
- **依赖管理**: go mod

包含 rules（2 个语言特有 + 3 个通用来自 harness-core）。流水线技能（10 个）与辅助技能由 `apply-harness` 从 `harness-core/skills/` 模板渲染，语言包不再维护副本。

> **辅助技能**: `/harness-me`（需求打磨）、`domain-modeling`（领域语言维护）、`research`（外部事实查证）、`resolving-merge-conflicts`（合并冲突解决）、`/diagnosing-bugs`（Bug 诊断）、`/handoff`（上下文交接）、`/arch-review`（架构体检）——在流水线各阶段按需调用。
---


