---
name: wot-ui-cli
description: 使用、调试或维护 @wot-ui/cli 与 open-wot 仓库。适用于 wot CLI 命令、Agent/MCP 接入、doctor/usage/lint、组件知识查询、客户端 adapter、离线数据提取、构建测试、发布包检查和仓库开发；如果任务是直接编写 wd-* 组件页面或解释组件 API，应改用 wot-ui-v2 skill。
---

# Wot UI CLI

处理 `@wot-ui/cli`、MCP、Agent 接入和 open-wot 仓库维护任务时，基于当前源码、`package.json` 和 README 行事，不根据旧文档猜测命令。

## 路由

- CLI、MCP、Agent、数据提取或仓库开发：使用本 Skill。
- 组件选型、页面代码、props、主题和组件问题：使用 `wot-ui-v2` Skill。
- 通过 CLI 查询组件知识时，保留 CLI 使用语境；需要生成组件代码时再切换到 `wot-ui-v2`。

## 工作流

1. 先查看 `README.md`、`package.json#scripts` 和相关源码。
2. 修改 CLI、MCP、prompt、数据结构或 Skill 后，同步测试与 README。
3. 写配置前先运行 `--dry-run`，使用隔离 `--cwd`，不要修改真实用户配置。
4. 修改命令输出后，至少运行一个真实源码或构建产物命令。
5. 提交前运行 `pnpm lint && pnpm typecheck && pnpm test && pnpm build`。

## 命令分组

组件知识：

```bash
wot list [keyword]
wot info <component>
wot doc <component>
wot demo <component> [name]
wot token [component]
wot changelog [versionOrComponent] [component]
```

项目分析：

```bash
wot doctor [dir]
wot usage [dir]
wot lint [dir]
```

Agent 接入：

```bash
wot agent list
wot agent init --client cursor
wot agent status --client cursor
wot agent doctor --client cursor
wot agent remove --client cursor
wot agent init --client all
```

MCP 管理：

```bash
wot mcp
wot mcp serve
wot mcp list
wot mcp init --client cursor
wot mcp status --client cursor
wot mcp doctor --client cursor
wot mcp remove --client cursor
wot mcp print --client cursor
```

查询命令支持 `--version` 和 `--format text|json|markdown`。Agent/MCP 管理命令支持的具体选项以 `--help` 和源码为准；写操作优先使用 `--dry-run`。

## 仓库开发

```bash
pnpm install
pnpm dev
pnpm exec tsx src/index.ts list
pnpm build
node dist/index.mjs list
```

更新离线数据：

```bash
pnpm sync:clone
pnpm extract:clone
pnpm sync --wot-dir ../wot-ui
pnpm extract --wot-dir ../wot-ui --output data/v2.0.4.json
```

发布包检查：

```bash
pnpm build
pnpm compress
pnpm exec publint
npm pack --dry-run --json
```

## MCP 注意事项

- `wot mcp` 使用 stdio，终端无普通输出通常正常。
- `doctor` 验证配置和真实 handshake；部分客户端还会检查注册状态。
- `--client all` 在 project scope 处理六个支持客户端。
- 保留已有 Server、JSONC 注释、非托管 TOML 和用户 Instructions。

## 参考

需要完整命令矩阵、目录职责、验证要求、数据与发布流程时，读取 [references/overview.md](./references/overview.md)。
