---
name: yunxiao-devops
description: 阿里云云效 DevOps 平台集成技能。提供代码管理、流水线、项目管理、组织管理、制品仓库、应用交付、测试管理等完整 DevOps 能力。当用户需要与云效平台交互时使用，包括：(1) 代码仓库操作（分支、文件、合并请求）(2) 流水线创建和运行 (3) 项目和工作项管理 (4) 组织成员管理 (5) 制品仓库查询 (6) 应用部署和发布 (7) 测试用例管理。触发词：云效、Codeup、Flow、Projex、AppStack、DevOps。
---

# 云效 DevOps 技能

本技能提供与阿里云云效平台交互的完整能力，包含 156 个工具。

## 前置条件

```bash
export YUNXIAO_ACCESS_TOKEN="your-personal-access-token"
```

**重要**: 需要告知用户在全局设定此 token！当 API 请求失败时，提示用户获取令牌。

获取令牌：云效控制台 → 个人设置 → 个人访问令牌

## 核心原则：优先使用 CLI 查询

**在查阅 references 文档之前，必须优先使用 CLI 帮助命令！**

CLI 位置：`scripts/yunxiao-cli/index.mjs`

### 快速查询命令

```bash
# 查看帮助
node scripts/yunxiao-cli/index.mjs --help

# 列出所有工具
node scripts/yunxiao-cli/index.mjs list

# 按类别筛选 (base/code/org/project/pipeline/packages/appstack/test)
node scripts/yunxiao-cli/index.mjs list --category=pipeline

# 搜索工具
node scripts/yunxiao-cli/index.mjs search branch

# 查看工具详情（包含完整参数说明）
node scripts/yunxiao-cli/index.mjs tool create_branch
```

### 调用工具

```bash
# 调用工具（使用完整的 MCP 业务逻辑）
node scripts/yunxiao-cli/index.mjs call get_current_organization_info

# 带参数调用
node scripts/yunxiao-cli/index.mjs call create_branch '{"organizationId":"xxx","repositoryId":"yyy","branch":"feature/new"}'

# 直接调用 API
node scripts/yunxiao-cli/index.mjs api GET /oapi/v1/organization/current
node scripts/yunxiao-cli/index.mjs api POST /endpoint --data '{"key":"value"}'
```

## 查询流程

1. **先用 CLI 查询** → `list`、`search`、`tool` 命令获取工具信息
2. **CLI 信息不足时** → 查阅 references/ 目录下的详细文档
3. **执行操作** → 使用 `call` 命令（推荐）或 `api` 命令

## 功能模块参考

仅当 CLI 查询信息不足时查阅：

| 模块 | 参考文档 |
|------|----------|
| 代码管理 | [code-management.md](references/code-management.md) |
| 流水线 | [pipeline.md](references/pipeline.md) |
| 项目管理 | [project-management.md](references/project-management.md) |
| 组织管理 | [organization.md](references/organization.md) |
| 制品仓库 | [packages.md](references/packages.md) |
| 应用交付 | [appstack.md](references/appstack.md) |
| 测试管理 | [test-management.md](references/test-management.md) |

## API 基础信息

- **基础 URL**: `https://openapi-rdc.aliyuncs.com`
- **认证**: Header `x-yunxiao-token: <token>`

