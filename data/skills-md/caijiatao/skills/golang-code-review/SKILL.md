---
name: golang-code-review
description: "基于《Golang 工匠》的 Go 代码综合审查器，涵盖命名、结构体、函数、接口设计和错误处理五大方面。Use when reviewing Go code to ensure it follows best practices and idiomatic patterns."
metadata:
  author: caijiatao
  version: "2026.2.24"
  source: https://github.com/xxjwxc/uber_go_guide_cn
  language: zh
  tags: [code-review, 命名, 结构体, 函数, 接口, 错误处理]
  category: review
---

# Golang Code Reviewer

基于《Golang 工匠》的 Go 代码综合审查器，涵盖命名、结构体、函数、接口设计和错误处理五大方面。

## 触发时机

当用户请求以下任务时触发：
- "审查代码" / "review code"
- "检查 Go 代码" / "check go code"
- 编写、审查或重构 Go 代码时

## 审查领域

| 领域 | 描述 | 参考 |
|-----|------|------|
| **命名规范** | 包名、变量名、函数名、常量名、接口名检查 | [review-naming](references/review-naming.md) |
| **结构体设计** | 字段顺序、嵌入使用、构造函数、自定义类型 | [review-structs](references/review-structs.md) |
| **函数设计** | 职责单一性、参数设计、返回值设计 | [review-functions](references/review-functions.md) |
| **接口设计** | 接口大小、定义位置、组合、空接口使用 | [review-interfaces](references/review-interfaces.md) |
| **错误处理** | 错误创建、包装、判断、信息设计 | [review-errors](references/review-errors.md) |

## 审查流程

1. 检查命名规范（包名、变量名、函数名、常量名、接口名）
2. 检查结构体设计（字段顺序、嵌入使用、构造函数）
3. 检查函数设计（职责单一性、参数、返回值）
4. 检查接口设计（接口大小、定义位置、组合）
5. 检查错误处理（错误创建、判断、信息设计）
6. 提供具体的改进建议

## 输出格式

**直接使用 Edit 工具修改代码**，将不规范的代码改为符合 Go 最佳实践的代码。

- 不符合规范的命名 → 直接改为正确命名
- 结构体字段顺序混乱 → 直接调整字段顺序
- 函数参数过多 → 直接改为使用结构体
- 函数职责过多 → 直接拆分为多个函数
- 接口过大 → 直接拆分为小接口
- 错误处理不当 → 直接改为正确的错误处理

## 核心原则

1. 发现问题直接改为正确版本
2. 一次审查完成所有相关修改
3. 修改后代码应该直接可以运行
4. 保持建设性，专注于改进建议

## 资源来源

- [Uber Go Style Guide (Chinese)](https://github.com/xxjwxc/uber_go_guide_cn)
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
