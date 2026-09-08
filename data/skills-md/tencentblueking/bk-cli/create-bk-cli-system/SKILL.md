---
name: create-bk-cli-system
description: 当需要为 bk-cli 扩展 system 能力时使用：无论是新增顶层 system、给已有 system 增加 action、还是为大 system 增加一层 subsystem，都应先使用此技能。技能会先检查目标 system/subsystem 是否已存在，遇到多模块 API 列表时先让用户在扁平 action 与一层 subsystem 两种命令形态中选择，再复用共享的 YAML/Go 选型、注册、测试和文档约定。
---

# 扩展 bk-cli System

## 使用目标

这个技能统一覆盖两类工作：

- 新增一个顶层 system 命令
- 给已有 system 新增一个或多个 action
- 给已有 system 新增一层 subsystem，并在 subsystem 下新增 YAML 或 Go actions

本技能同时提供创建/扩展 system 时必查的共享契约摘要；详细规则以 `docs/design.md` 为准。先判断 system 是否已存在，再决定走哪条分支；不要先写代码再回头补注册或补结构。

## 推荐读取顺序

1. 先读 `AGENTS.md` 和 `docs/design.md`，确认仓库边界与设计基线。
2. 再读本技能中的“扩展 system 必查摘要”，确认扩展 system 时最容易踩坑的共享规则；详细契约一律回到 `docs/design.md`。
3. 最后按本技能的分支流程判断是“新建 system”还是“给已有 system 增加 action”。

## 第零步：先判断是否需要 subsystem

如果用户的需求、OpenAPI 列表、资源 tags 或业务描述天然分成多个模块，先暂停实现，给用户两个选项：

1. **扁平 action**：继续使用 `bk-cli <system> <action>`，通过 action 名区分模块，例如 `get_pipeline_build_list`。
2. **一层 subsystem**：使用 `bk-cli <system> <subsystem> <action>`，例如 `bk-cli devops pipeline get_build_list`、`bk-cli devops codecc get_task_detail`、`bk-cli devops stream trigger`。

当前只允许一层 subsystem，不允许 `bk-cli <system> <subsystem> <sub_subsystem> <action>`。如果用户需要更深层级，停止实现并给出公共契约变更 proposal 建议。

## 第一步：先判断 system 是否已存在

按下面顺序检查：

1. 阅读 `AGENTS.md`、`docs/design.md`，并先通读本技能后面的“扩展 system 必查摘要”
2. 查看 `cmd/system/register.go`，确认 `systemCatalog()` 的注册方式
3. 检查以下文件是否已经存在：
   - `cmd/system/<system>.go`
   - `cmd/system/<system>/spec.go`
   - `cmd/system/<system>/actions.yaml`
   - `cmd/system/<system>/<subsystem>/spec.go`
   - `cmd/system/<system>/<subsystem>/actions.yaml`
4. 搜索 `new<System>SystemSpec()` 或 `NewSystemSpec()`，确认该 system 是否已接入 catalog

判断结果：

- **system 不存在**：先创建 system，再按需要补 YAML actions、Go-implemented actions、测试和文档
- **system 已存在**：只新增 action，按 action 粒度决定用 YAML 还是 Go，不要为了一个 Go action 迁移已有 YAML actions
- **system 已存在但 subsystem 不存在**：按“分支 C：新增 subsystem”创建 subsystem，再按 action 粒度决定 YAML 或 Go

## 扩展 system 必查摘要

文档分层以 `AGENTS.md` 为准；详细共享契约以 `docs/design.md` 为准。生成 system/action 时，至少先确认：

- context 表示独立 BlueKing 部署目标，不是 API Gateway stage；详细 context 规则以 `docs/design.md` 为准。
- `--stage`、timeout、tenant、`--header` 的优先级不要自己重写；涉及这些行为时回查 `docs/design.md`。
- 即使用户用 `--header` 覆盖 `X-Bkapi-Authorization`，`--dry-run` / `--verbose` 仍必须脱敏展示认证内容。
- YAML action 必须显式声明 `authConfig`；`resourcePermissionRequired: true` 必须同时设置 `appVerifiedRequired: true`。
- YAML `params` 只支持 `in: path`、`in: query` 和帮助用途的 `in: header`；不要声明 `in: body`。
- YAML action 统一获得共享输入：`--stage`、`--body '<json>'`、重复的 `--header 'Key:Value'`；保留 flag 名冲突时应跳过 action 并给出 warning。
- 如果 OpenAPI request body 很复杂、需要 Agent 或调用方自行构造完整 JSON，不要强行把 body 字段拆成 command flags；继续使用共享 `--body '<json>'`，请求体示例放进 `examples`，并在 YAML action 中配置 `body_schema`。如果 OpenAPI 标记 request body 为 required，同时配置 `body_required: true`。默认 help 按 `Usage`、`Examples`、schema 查看提示的顺序展示，完整 schema 通过 `bk-cli <system> [subsystem] <action> -h --body-schema` 查看。
- 路径占位符值会按单个 URL path segment 转义，不能依赖它注入 `/` 或 `?`。
- Go-implemented action 要通过 `systemcmd.ResolveRuntime(deps)` 和 `systemcmd.ExecuteRequest(...)` 或 `syslib.ExecuteRequest(...)` 走共享执行路径，不要绕过 runtime / output / credential 逻辑。
- 当 Go-implemented action 同时支持命名 flags 和原始 `--body` 时，把 `--body` 视为显式覆盖。

### command group 形态

一个 command group 可以是以下形态之一：

- **YAML-driven**：所有 action 由 `actions.yaml` 定义
- **Go-implemented**：所有 action 由 Go 代码实现
- **mixed**：同时保留 YAML actions 和 Go-implemented actions
- **group-only**：父 system 只作为分组，下面挂 subsystem
- **parent actions + subsystems**：父 system 有自己的 actions，同时下面挂 subsystem

一个 action 的实现方式只看它自己的复杂度，不看别的 action 已经用什么。

同一 parent 下的直接子命令名必须唯一。父 system 的 action 名不能和 subsystem 名冲突。

### action 选型规则

优先选择满足需求的最简单实现。

优先用 YAML，当且仅当下面条件都满足：

- 本质上只是 `cli args -> 一次 API 调用`
- 不需要本地编排逻辑
- 不需要本地专属 flags, API 请求参数直接转换成 flags
- 不需要定制返回结构
- 即使有 request body，只要调用方可以通过 `--body` 直接提供完整 JSON，且 `examples` / `body_schema` 足以指导 Agent 构造 body，也优先保持 YAML-driven

必须用 Go-implemented action，只要满足任一条件：

- 需要本地校验、分支、编排或分页聚合
- 需要零次、一次或多次 API 调用
- 需要本地专属 flags，例如 `--bk_biz_id`、`--fields`、`--limit`, 封装/处理/编排后再作为请求参数
- 需要请求前由 CLI 根据命名 flags 合成 body，或需要对 body 字段做本地专属校验/默认值处理
- 需要请求后用 `mutate` 或手工 envelope 调整返回

### YAML body schema / example 规则

`body_schema` 用于“body 很复杂，但 action 本身仍然只是一次 API 调用”的场景。典型例子是 OpenAPI 的 request body 有大量嵌套字段、数组或对象，Agent 需要根据 schema 自行构造完整 JSON。

规则：

- 不要为复杂 body 字段生成大量 command flags；否则 help 会膨胀，调用契约也容易和 OpenAPI 漂移。
- YAML action 只把 `path` / `query` 参数转成 flags；body 继续通过共享 `--body '<json>'` 输入。
- `body_schema` 放精简后的 JSON schema 或字段结构说明；可直接作为 `--body` 起点的 JSON 示例放在 action `examples` 中，避免和示例重复维护。
- 如果 OpenAPI request body 是 required，配置 `body_required: true`；这样执行时缺少 `--body` 会在本地失败，不会把空 body 发送到上游。
- 默认 `bk-cli <system> [subsystem] <action> --help` 必须先展示 `Usage` 和 `Examples`，再展示 schema 查看提示；`body_schema` 必须能通过 `bk-cli <system> [subsystem] <action> -h --body-schema` 看到。系统专属 `skills/*/SKILL.md` 只能放常用示例，不能作为唯一的 body 结构来源。
- `--body-schema` 是 help modifier，不是执行参数；不带 `-h` 单独使用时必须快速失败，不能进入认证或请求执行路径。
- 只有当用户明确需要更友好的本地 flags、CLI 需要合成 body、或需要本地校验复杂字段时，才把该 action 单独做成 Go-implemented wrapper。

### 核心类型

#### `systemcmd.SystemSpec`

```go
type SystemSpec struct {
    Name              string
    Description       string
    YAMLFile          string
    RegisterGoActions RegisterGoActionsFunc
    Subsystems        []SystemSpec
}
```

#### `systemcmd.BuildDeps`

```go
type BuildDeps struct {
    GetContext func() string
    IsDryRun   func() bool
    IsVerbose  func() bool
    WarnWriter io.Writer
}
```

#### `syslib.RequestSpec`

Go-implemented action 用它描述单次请求。常用字段：

- `GatewayName`
- `Method`
- `Path`
- `ParamsJSON`
- `BodyJSON`
- `Headers`
- `Stage`
- `Timeout`
- `AuthConfig`

`AuthConfig` 必须显式设置，使用 `&syslib.AuthConfig{...}`。

### 共享 helper 地图

#### 运行时与请求执行

| Helper | 用途 |
|--------|------|
| `systemcmd.ResolveRuntime(deps)` | 在 `RunE` 开头统一解析 context、dry-run、verbose、insecure |
| `systemcmd.ExecuteRequest(cmd, runtime, actionName, spec, mutate)` | 单次请求 action 的标准执行路径 |
| `syslib.ExecuteRequest(runtime, spec)` | 多次请求编排、分页聚合 |
| `systemcmd.EnsureEnvelope(actionName, env)` | 防御空 envelope |

#### flags、校验与序列化

| Helper | 用途 |
|--------|------|
| `systemcmd.AddCommonRequestFlags(cmd, &stage, &body, &headers)` | 注册 `--stage`、`--body`、`--header` |
| `systemcmd.AddCommonRequestFlagsWithoutBody(cmd, &stage, &headers)` | 注册 `--stage`、`--header` |
| `systemcmd.MarshalJSON(payload)` | 统一序列化 body |
| `systemcmd.ValidatePositiveIntFlag(...)` | 校验必填正整数 |
| `systemcmd.ValidatePositiveIntFlagIfChanged(...)` | 校验可选正整数 |
| `systemcmd.ValidateNonNegativeIntFlag(...)` | 校验非负整数 |
| `systemcmd.ValidateNonEmptyStringFlag(...)` | 校验非空字符串 |
| `systemcmd.ParseJSONObjectFlag(flagName, raw)` | 解析 JSON object 类型 flag |

#### 测试 helper

| Helper | 用途 |
|--------|------|
| `testutil.BuildDeps(dryRun bool)` | 构造测试依赖 |
| `testutil.SetupTestContext(baseURL string)` | 创建默认 context 与凭据 |
| `testutil.CaptureCommandStdout(fn)` | 捕获 stdout |
| `testutil.BuildYAMLActionCmd(...)` | 构造 YAML action 测试命令 |

不要自己重复实现这些共享能力。

## 分支 A：system 不存在，先创建 system

### 必须新增或更新的文件

始终需要：

| 文件 | 用途 |
|------|------|
| `cmd/system/<system>.go` | 薄包装，调用 `<system>.NewSystemSpec()` |
| `cmd/system/<system>/spec.go` | `NewSystemSpec()` 实现 |
| `cmd/system/register.go` | 在 `systemCatalog()` 中注册 |

按需新增：

| 文件 | 条件 |
|------|------|
| `cmd/system/<system>/actions.yaml` | 该 system 需要 YAML actions |
| `cmd/system/<system>/<action>.go` | 该 system 需要 Go-implemented actions |
| `cmd/system/<system>/common.go` | 多个 Go actions 共享逻辑 |
| `cmd/system/<system>/<system>_suite_test.go` | 该 system 有 Ginkgo 测试 |
| `skills/bk-cli-<system>/SKILL.md` | 新增公开 system 时必须补齐，且内容用中文 |

### 薄包装模板

```go
package system

import <system>system "github.com/TencentBlueKing/bk-cli/cmd/system/<system>"

func new<System>SystemSpec() SystemSpec {
    return <system>system.NewSystemSpec()
}
```

### `spec.go` 模板

#### YAML-driven

```go
func NewSystemSpec() systemcmd.SystemSpec {
    return systemcmd.SystemSpec{
        Name:        "<system>",
        Description: "<system> system commands",
        YAMLFile:    "<system>/actions.yaml",
    }
}
```

#### Go-implemented

```go
func NewSystemSpec() systemcmd.SystemSpec {
    return systemcmd.SystemSpec{
        Name:        "<system>",
        Description: "<system> system commands",
        RegisterGoActions: func(parent *cobra.Command, deps systemcmd.BuildDeps) error {
            parent.AddCommand(newSomeActionCmd(deps))
            return nil
        },
    }
}
```

#### mixed

```go
func NewSystemSpec() systemcmd.SystemSpec {
    return systemcmd.SystemSpec{
        Name:        "<system>",
        Description: "<system> system commands",
        YAMLFile:    "<system>/actions.yaml",
        RegisterGoActions: func(parent *cobra.Command, deps systemcmd.BuildDeps) error {
            builders := []func(systemcmd.BuildDeps) *cobra.Command{
                newActionOneCmd,
                newActionTwoCmd,
            }
            for _, build := range builders {
                parent.AddCommand(build(deps))
            }
            return nil
        },
    }
}
```

### 注册与 embed 约束

在 `cmd/system/register.go` 的 `systemCatalog()` 中加入新 system。

如果用了 YAML，文件必须放在 `cmd/system/<system>/actions.yaml`，因为仓库依赖 `//go:embed */actions.yaml` 自动嵌入。

### `common.go` 建议

多个 Go-implemented actions 共享逻辑时，把下面内容放进 `common.go`：

- 网关名常量
- 共享类型
- body builder
- 共享校验函数
- factory function

### Ginkgo suite

该 system 只要出现测试文件，就补 suite 文件：

```go
package <system>_test

import (
    "testing"

    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"
)

func TestSuite(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "<System> Suite")
}
```

## 分支 B：system 已存在，新增 action

### YAML action 工作流

YAML 文件位置固定为：

`cmd/system/<system>/actions.yaml`

如果 `SystemSpec.YAMLFile` 已配置，只需要在 `actions` 列表中追加 action，不需要额外 Go wiring。

#### YAML 顶层结构

```yaml
name: <system>
gateway_name: bk-<upstream>
description: "System description"
actions:
  - ...
```

#### YAML action 字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | action 命令名 |
| `description` | 是 | Cobra Short |
| `method` | 是 | HTTP 方法 |
| `path` | 是 | API 路径，可带 `{param}` |
| `timeout` | 否 | 覆盖 context timeout，例如 `30s` |
| `authConfig` | 是 | 认证配置 |
| `params` | 否 | 参数列表 |
| `examples` | 否 | 命令示例 |
| `body_schema` | 否 | 复杂 request body 的 schema 或字段结构说明；通过 `-h --body-schema` 帮助 Agent 构造 `--body` |
| `body_required` | 否 | 执行时是否要求非空 `--body`；OpenAPI requestBody.required=true 时应设置为 true |

#### `authConfig`

| 字段 | 必填 | 说明 |
|------|------|------|
| `appVerifiedRequired` | 是 | 是否需要应用认证 |
| `userVerifiedRequired` | 是 | 是否需要用户认证 |
| `resourcePermissionRequired` | 是 | 是否需要资源权限校验 |

约束：

- `resourcePermissionRequired: true` 时，`appVerifiedRequired` 也必须为 `true`
- 如果 app/user 都不需要，CLI 不会生成 `X-Bkapi-Authorization`
- 即使用户用 `--header` 覆盖认证头，dry-run / verbose 也必须继续脱敏展示认证内容

#### `params`

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 参数名，也是 flag 名 |
| `in` | 是 | `path`、`query` 或 `header` |
| `type` | 是 | `string`、`bool`、`int` |
| `description` | 否 | 帮助文本 |
| `required` | 否 | 是否必填 |
| `default` | 否 | 默认值 |

规则：

- `path` 与 `query` 会生成 CLI flags
- `header` 仅用于帮助文本，不生成独立 flag
- 不要写 `in: body`
- action 额外共享 `--stage`、`--body '<json>'` 和重复的 `--header 'Key:Value'`；有 `body_schema` 时额外支持 help modifier `--body-schema`；有 `body_required: true` 时 `--body` 是执行必填项
- param 名不能与保留 flag 冲突：`body`、`body-schema`、`header`、`stage`、`help`、`context`、`dry-run`、`format`、`verbose`、`insecure`
- 同一 action 内 path 和 query param 名不能重复

### Go-implemented action 工作流

#### 需要修改的文件

| 文件 | 用途 |
|------|------|
| `cmd/system/<system>/<action>.go` | action 构造函数 |
| `cmd/system/<system>/spec.go` | 注册新 action |
| `cmd/system/<system>/<action>_test.go` | action 测试 |
| `cmd/system/<system>/common.go` | 共享逻辑，可选 |

#### 构造函数模板

```go
func newSomeActionCmd(deps systemcmd.BuildDeps) *cobra.Command {
    var (
        bizID   int
        stage   string
        body    string
        headers []string
    )

    cmd := &cobra.Command{
        Use:   "some_action",
        Short: "Short description",
        RunE: func(cmd *cobra.Command, args []string) error {
            runtime, err := systemcmd.ResolveRuntime(deps)
            if err != nil {
                return err
            }

            if err := systemcmd.ValidatePositiveIntFlag("bk_biz_id", bizID); err != nil {
                return err
            }

            bodyJSON, err := buildSomeBody(body, bizID)
            if err != nil {
                return err
            }

            return systemcmd.ExecuteRequest(cmd, runtime, "some_action", syslib.RequestSpec{
                GatewayName: gatewayName,
                Method:      "POST",
                Path:        "/api/v3/some/path/",
                BodyJSON:    bodyJSON,
                Headers:     headers,
                Stage:       stage,
                AuthConfig: &syslib.AuthConfig{
                    AppVerifiedRequired:        true,
                    UserVerifiedRequired:       true,
                    ResourcePermissionRequired: false,
                },
            }, nil)
        },
    }

    cmd.Flags().IntVar(&bizID, "bk_biz_id", 0, "Business ID")
    systemcmd.AddCommonRequestFlags(cmd, &stage, &body, &headers)
    return cmd
}
```

#### body 合成模式

优先使用 `bodyOverride` 守卫：

```go
func buildSomeBody(bodyOverride string, bizID int) (string, error) {
    if bodyOverride != "" {
        return bodyOverride, nil
    }
    if err := systemcmd.ValidatePositiveIntFlag("bk_biz_id", bizID); err != nil {
        return "", err
    }
    return systemcmd.MarshalJSON(map[string]any{
        "bk_biz_id": bizID,
    })
}
```

#### mutate 回调

需要在 stdout 前调整 envelope 时，传入 `mutate`：

```go
return systemcmd.ExecuteRequest(cmd, runtime, "demo_action", spec,
    func(env *output.Envelope) error {
        if env.DryRun {
            env.Data = map[string]any{"received": localData}
            return nil
        }
        env.Data = map[string]any{
            "received": localData,
            "upstream": env.Data,
        }
        return nil
    })
```

#### 无共享 `--body` 的 action

如果 action 自己管理 body 语义：

1. 使用 `systemcmd.AddCommonRequestFlagsWithoutBody`
2. 自己声明本地 `--body` flag
3. `RequestSpec.BodyJSON` 由本地逻辑决定

#### factory 模式

多个 action 共享同一套 flag/request 结构时，把公共部分收进 `common.go`，用 spec struct + factory function 生成命令，避免复制粘贴。

#### 多次请求编排

需要分页聚合或多次调用时：

1. 用 `syslib.ExecuteRequest(runtime, spec)` 发每次请求
2. 用 `systemcmd.EnsureEnvelope(actionName, result.Envelope)` 校验结果
3. 手工聚合数据
4. 手工构造最终 envelope

#### 在 `spec.go` 中挂载

```go
builders := []func(systemcmd.BuildDeps) *cobra.Command{
    newExistingActionCmd,
    newSomeActionCmd,
}
for _, build := range builders {
    parent.AddCommand(build(deps))
}
```

## 分支 C：system 已存在，新增一层 subsystem

### 必须新增或更新的文件

| 文件 | 用途 |
|------|------|
| `cmd/system/<system>/spec.go` | 在 `SystemSpec.Subsystems` 中注册 subsystem |
| `cmd/system/<system>/<subsystem>/spec.go` | `NewSystemSpec()` 实现，描述 subsystem 自己的 YAML/Go actions |
| `cmd/system/<system>/<subsystem>/actions.yaml` | 该 subsystem 需要 YAML actions 时使用 |
| `cmd/system/<system>/<subsystem>/<action>.go` | 该 subsystem 需要 Go-implemented actions 时使用 |
| `cmd/system/<system>/<subsystem>/common.go` | 多个 Go actions 共享逻辑，可选 |
| `cmd/system/<system>/<subsystem>/<subsystem>_suite_test.go` | 该 subsystem 有测试时必须存在 |

### subsystem `spec.go` 模板

```go
package <subsystem>

import (
    "github.com/spf13/cobra"

    systemcmd "github.com/TencentBlueKing/bk-cli/internal/systemcmd"
)

func NewSystemSpec() systemcmd.SystemSpec {
    return systemcmd.SystemSpec{
        Name:        "<subsystem>",
        Description: "<subsystem> commands",
        YAMLFile:    "<system>/<subsystem>/actions.yaml",
        RegisterGoActions: func(parent *cobra.Command, deps systemcmd.BuildDeps) error {
            parent.AddCommand(newSomeActionCmd(deps))
            return nil
        },
    }
}
```

### parent system 注册模板

```go
func NewSystemSpec() systemcmd.SystemSpec {
    return systemcmd.SystemSpec{
        Name:        "<system>",
        Description: "<system> commands",
        YAMLFile:    "<system>/actions.yaml",
        RegisterGoActions: func(parent *cobra.Command, deps systemcmd.BuildDeps) error {
            parent.AddCommand(newParentActionCmd(deps))
            return nil
        },
        Subsystems: []systemcmd.SystemSpec{
            <subsystem>.NewSystemSpec(),
        },
    }
}
```

父 system 的 `YAMLFile` 和 `RegisterGoActions` 都是可选的。不要为了挂 subsystem 创建无意义的父 action。

### subsystem YAML 顶层结构

```yaml
name: <subsystem>
gateway_name: <subsystem-gateway-name>
description: "<subsystem> commands"
actions:
  - name: <action>
```

subsystem YAML 的 `gateway_name` 必须独立声明，不从父 system 继承。

## 测试与文档要求

至少补充或更新：

- `cmd/system/register_test.go`：system 注册行为
- `cmd/system/<system>/<action>_test.go`：Go-implemented action 测试
- `cmd/system/<system>/<subsystem>/<action>_test.go`：subsystem Go-implemented action 测试
- `cmd/system/<system>/<system>_suite_test.go`：该 system 有测试时必须存在
- `cmd/system/<system>/<subsystem>/<subsystem>_suite_test.go`：该 subsystem 有测试时必须存在

如果新增公开 system，同步更新：

- `AGENTS.md`
- `README.md`
- `README_EN.md`
- `tests/integration/AGENTS.md`
- `skills/bk-cli-<system>/SKILL.md`

如果只是改动已有命令或参数，也要同步更新 `AGENTS.md`、`README.md`、`README_EN.md`、`tests/integration/AGENTS.md` 和相关 skill。

如果变更影响公开 system 的可见行为，补充或更新：

- `tests/integration/cases/system/<system>/` 下的 YAML 集成用例
- `tests/integration/mock_api/app.py`（仅当 `httpbin` 不够表达该行为时）

## 最终检查清单

1. 先确认目标 system 是否已存在，再选分支
2. `cmd/system/<system>.go` 与 `cmd/system/<system>/spec.go` 都存在
3. `SystemSpec.Name`、YAML 顶层 `name`、注册项三者一致
4. `cmd/system/register.go` 的 `systemCatalog()` 已包含目标 system
5. YAML 文件路径是 `cmd/system/<system>/actions.yaml`
6. YAML action 都有完整 `authConfig`
7. Go-implemented action 使用 `systemcmd.ResolveRuntime`
8. Go-implemented action 使用 `systemcmd.ExecuteRequest` 或 `syslib.ExecuteRequest`
9. 共享 flags、校验、JSON 解析优先复用 `systemcmd` helper
10. 测试优先复用 `cmd/system/testutil`
11. 公开 system 已补 `skills/bk-cli-<system>/SKILL.md`
12. 相关 system 的集成用例已在 `tests/integration/cases/system/<system>/` 补齐或确认无需变更
13. 如集成用例作者约定有变化，已更新 `tests/integration/AGENTS.md`
14. 如果新增 subsystem，确认只使用一层 subsystem
15. 如果新增 subsystem，确认 subsystem action 路径是 `cmd/system/<system>/<subsystem>/...`
16. 如果新增 subsystem，确认 subsystem YAML 顶层 `name` 是 `<subsystem>`，并且独立声明 `gateway_name`
17. 确认父 system 的 action 名没有和 subsystem 名冲突
18. 完成后执行：

```bash
make fmt
make lint
make test
make build
make test-integration SCENARIO=<SCENARIO_ID>
```

## 排障顺序

1. 先确认 context 与凭据是否正确。
2. 再确认 stage、tenant、timeout、header、body 是否符合前面的必查摘要；细节以 `docs/design.md` 为准。
3. 使用 `--dry-run` 查看最终请求构造。
4. 仍有问题时，再回到具体 system 技能或 `docs/design.md` 深挖。

## 常见错误

- 没先判断 system 是否已存在，结果重复创建结构
- 只写 `actions.yaml`，却没有补 `cmd/system/<system>.go` 与 `spec.go`
- 忘了把 system 加到 `systemCatalog()`
- YAML 文件不在 `cmd/system/<system>/actions.yaml`
- YAML action 缺少 `authConfig`
- 在 YAML `params` 中写 `in: body`
- Go-implemented action 绕过 `ResolveRuntime` 或 `ExecuteRequest`
- 在 system 目录里重复定义测试 helper
- 新增公开 system 却没补 `skills/bk-cli-<system>/SKILL.md`
- 导入别名没用 `syslib` / `systemcmd`
- 用户给出的 API 列表已经按 pipeline/codecc/stream 这类模块划分，agent 没先让用户选择扁平 action 还是 subsystem
- subsystem YAML 写成了父 system 的 `name`
- subsystem YAML 试图省略 `gateway_name` 并继承父 system
- 创建了多层 subsystem
- 父 system action 和 subsystem 使用了同一个命令名
