---
name: golang-testing
description: Go testing patterns including table-driven tests, subtests, benchmarks, fuzzing, and test coverage. Follows TDD methodology with idiomatic Go practices.
metadata:
  author: caijiatao
  version: "2026.2.24"
  source: https://go.dev/doc/tutorial/add-a-test
  language: zh
  tags: [testing, tdd, benchmarks, fuzzing, coverage]
  category: testing
---

# Go 测试模式

用于编写可靠、可维护测试的完整 Go 测试模式，遵循 TDD 方法论。

## 何时启用

- 编写新的 Go 函数或方法
- 为现有代码增加测试覆盖率
- 为性能关键代码建立基准测试
- 实现输入验证的模糊测试
- 在 Go 项目中遵循 TDD 工作流程

## 测试模式

| 模式 | 描述 | 参考 |
|------|------|------|
| **TDD 方法论** | RED-GREEN-REFACTOR 循环 | [test-tdd](references/test-tdd.md) |
| **表格驱动测试** | Go 测试的标准模式 | [test-table-driven](references/test-table-driven.md) |
| **子测试与并行** | 组织相关测试，并行执行 | [test-subtests](references/test-subtests.md) |
| **接口 Mock** | 使用接口进行依赖注入和 mock | [test-mocking](references/test-mocking.md) |
| **基准测试** | 性能测试和内存分析 | [test-benchmarks](references/test-benchmarks.md) |
| **模糊测试** | 随机输入测试以发现边界情况 | [test-fuzzing](references/test-fuzzing.md) |
| **测试覆盖率** | 分析代码覆盖情况 | [test-coverage](references/test-coverage.md) |

## Go 的 TDD 工作流程

```
RED     → 先写失败的测试
GREEN   → 编写最少代码使测试通过
REFACTOR → 在保持测试绿色的同时改善代码
REPEAT  → 继续下一个需求
```

## 快速参考

### 基本测试
```go
func TestAdd(t *testing.T) {
    got := Add(2, 3)
    want := 5
    if got != want {
        t.Errorf("Add(2, 3) = %d; want %d", got, want)
    }
}
```

### 表格驱动测试
```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got := Add(tt.a, tt.b)
            if got != tt.expected {
                t.Errorf("got %d; want %d", got, tt.expected)
            }
        })
    }
}
```

### 子测试与并行
```go
func TestParallel(t *testing.T) {
    tests := []struct{ name string }{
        {"test1"}, {"test2"}, {"test3"},
    }

    for _, tt := range tests {
        tt := tt
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // 并行执行
            // 测试代码...
        })
    }
}
```

### 基准测试
```go
func BenchmarkProcess(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Process()
    }
}
```

## 测试命令

```bash
# 执行所有测试
go test ./...

# 执行带覆盖率的测试
go test -coverprofile=coverage.out ./...

# 执行带竞态检测的测试
go test -race ./...

# 执行基准测试
go test -bench=. -benchmem ./...

# 执行模糊测试
go test -fuzz=FuzzParseJSON -fuzztime=30s ./...
```

## 最佳实践

### 应该做的
- 先写测试（TDD）
- 使用表格驱动测试以获得完整覆盖
- 测试行为，而非实现
- 在辅助函数中使用 `t.Helper()`
- 对独立测试使用 `t.Parallel()`
- 用 `t.Cleanup()` 清理资源
- 使用描述情境的有意义测试名称

### 不应该做的
- 不要直接测试私有函数（通过公开 API 测试）
- 不要在测试中使用 `time.Sleep()`（使用 channels 或条件）
- 不要忽略不稳定测试（修复或移除它们）
- 不要 mock 所有东西（可能时偏好集成测试）
- 不要跳过错误路径测试

## 覆盖率目标

| 代码类型 | 目标 |
|-----------|------|
| 关键业务逻辑 | 100% |
| 公开 API | 90%+ |
| 一般代码 | 80%+ |
| 生成的代码 | 排除 |

## 资源

- [Go Testing](https://go.dev/doc/tutorial/add-a-test)
- [Effective Go - Testing](https://go.dev/doc/effective_go#testing)
- [TableDrivenTests](https://github.com/golang/go/wiki/TableDrivenTests)
