---
name: cli-self-check
version: 1.0.0
description: "检测新合并到 te-cli 的 CLI 功能是否合理。从命令注册、业务域↔skill 配对、skill 文档覆盖、skill 内部一致性、用户文档同步、工程健壮性六个维度扫描，定位会导致命令加载失败、AI agent 读空文档瞎猜参数、用户文档滞后等问题。当合并了新命令域/命令、新增或修改 skill、做发版前自检、或需要评估 CLI 功能完整性时使用。"
---

# cli-self-check

te-cli 的「新功能合理性」自检 skill。把一次人工 code review 中反复用到的结构化检查固化成可重复执行的脚本 + 判读规则。

## 何时用

- 合并了新的命令域（`src/commands/te-*`）或新命令
- 新增 / 修改了 `skills/` 下的 skill
- 发版前自检、或评估某分支 CLI 功能是否「做完整了」

## 怎么跑

```bash
# 全量扫描（推荐发版前用）
node self-check/scan.mjs

# 只看相对某分支的变更域（推荐合并/提 PR 后用，聚焦本次改动）
node self-check/scan.mjs --since master

# 机器可读，便于接 CI
node self-check/scan.mjs --json
```

退出码：存在 **P1** 时返回 `1`，否则 `0`，可直接用于 CI 卡口。

> 脚本是纯 Node、零新依赖、只读不改仓库。判读和修复由你（agent）依据下方规则完成——脚本负责「发现」，你负责「确认 + 修」。

## 六个检测维度

| 维度 | 名称 | 查什么 | 漏了会怎样 |
|------|------|--------|-----------|
| **D1** | 命令注册 | 新域是否在 `src/index.ts` 注册；MCP service 是否注册了 mapping | 命令根本不加载；`buildMcpUrl` 运行时抛错 |
| **D2** | 域↔skill 配对 | 每个业务域是否有对应 skill；工具命令不应有 skill | agent 不知道怎么用新命令 |
| **D3** | skill 文档覆盖 | 命令 ↔ `references/*.md` 是否一一对应 | agent 缺命令文档，被迫猜参数 |
| **D4** | skill 内部一致性 | CRITICAL 规则「+cmd→cmd.md」是否与真实文件名相符；SKILL.md 内链接是否失效 | agent 按规则去读文档却读空，瞎猜 ID/参数 |
| **D5** | 文档同步 | README（中/英）是否覆盖所有 service；版本号 vs CHANGELOG | 用户照 README 用，以为新功能不存在 |
| **D6** | 工程健壮性 | 每个域是否有 verify 脚本；是否接入 `tsc --noEmit` | 回归无自动拦截；类型错误只在 build 暴露 |

## 严重度与处理原则

- **🔴 P1（阻断）**：会导致命令加载失败、或 agent 行为出错（读空文档→瞎猜）。**必须改**，CI 应卡。
- **🟡 P2（面向用户/agent 的明显偏差）**：文档缺失/滞后、失效链接。发版前应改。
- **🟢 P3（工程健壮性）**：verify/typecheck 缺口，风格不统一。择期补，不阻断发版。
- **ℹ️ info**：符合约定的确认项（如工具命令无 skill），无需处理。

## 各维度判读 + 修复指引

### D1 命令注册
- **「域未在 src/index.ts 注册」**：在 `src/index.ts` 的 `loadCommands()`（业务域）或 `registerXxxCommand()`（工具命令）补上 `import('./commands/<dir>/index.js')`。
- **「MCP service 未注册 mapping」**：在仍使用 MCP transport 的域 `index.ts` 顶部调 `registerMcpMappings({ '<service>': { componentName, mappingPath } })`（参考 `te-community/index.ts`）。Analysis 域只允许 Capability Gateway，不应注册 MCP mapping。
- 注意区分两种 "service"：commander 分组名（如 `engage`）≠ MCP 路由 key（如 `engage_config`）。脚本只检查后者，且只提取**字面量**传参；变量传参不报（宁可漏报不误报）。

### D2 域↔skill 配对
- 约定：**业务域配 skill，工具命令（交互式/运维）不配**。`sync`、`model`、`auth`、`config`、`api` 无 skill 是正确的。
- 若新增业务域，需在 `scan.mjs` 顶部 `DOMAIN_TO_SKILL` 里登记映射；新增工具命令登记到 `TOOL_DIRS`。**漏登记会被报 P2**，提醒你补映射或确认归类。

### D3 skill 文档覆盖
- 判定用「归一化 + 包含」匹配，能识别 `create-team.md` 覆盖 `+create`，所以这里报的是**真·缺文档**。
- 修法：在对应 skill 的 `references/` 补 `.md`，并在 SKILL.md 命令清单里挂上链接。
- 采用「分组/内联文档」策略的 skill（`ae-dataops`、`ae-kb`）在 `GROUPED_DOC_SKILLS` 中豁免逐命令检查——若新 skill 也走这种策略，加进去。

### D4 skill 内部一致性（最易出 P1）
- **规则矛盾**：SKILL.md 顶部若写「reference filename equals the command name（+cmd → references/cmd.md）」，则**每个命令都必须有严格同名文件**。若 `+list` 的文档叫 `list-teams.md`，agent 会去读不存在的 `list.md`。
  - **两种修法**（择一）：① 把文件重命名为与命令严格同名（`list.md`）——推荐，规则最自洽；② 改写顶部规则为「以下方命令清单中的链接为准」，删掉「filename = command name」的断言。
- **失效链接**：SKILL.md 里 `references/xxx.md` 指向的文件不存在——补文件或修链接。

### D5 文档同步
- 新域/新命令要同步进 `README.md` 和 `README.zh.md` 的命令表。
- 发版时版本号要在 CHANGELOG.md 有对应条目。

### D6 工程健壮性
- 新域建议补一个 `scripts/verify-te-<domain>.mjs`（参考现有 `verify-te-analysis-tools.mjs`：遍历命令源码并校验注册、flag、description 和文档契约），并在 `package.json` 加 `verify:<domain>` 脚本。
- 建议加 `"typecheck": "tsc --noEmit"`，把类型检查从 build 前移。

## 维护脚本

`scan.mjs` 顶部有可调配置，新增模块时按需更新：
- `DOMAIN_TO_SKILL`：业务域目录 → skill 名映射
- `COMMAND_SKILL_OVERRIDES`：同一命令域内由 overlay skill 负责的命令路径 → skill 名映射
- `TOOL_DIRS`：工具命令目录（豁免 skill 检查）
- `GROUPED_DOC_SKILLS`：走分组/内联文档策略的 skill（豁免逐命令 reference 检查）

判读哲学：**脚本只报「值得人看一眼」的线索，确认与修复由 agent 结合源码做**。新增检测维度时，优先保证零误报——一个假 P1 比漏报更伤工具可信度。
