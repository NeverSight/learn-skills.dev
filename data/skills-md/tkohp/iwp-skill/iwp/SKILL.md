---
name: iwp
description: IWP（创新工作平台）MCP 客户端：调用 IWP 后端课题任务与周报工具，OAuth 2.1 授权。触发词：列出我的任务、创建任务、课题任务、周报、提交周报、根据任务生成周报、MCP 工具。
metadata:
  version: "1.1.1"
---

# iwp skill - 路由器入口

## 这是什么

iwp skill 是 IWP（创新工作平台）MCP server 的标准 OAuth 2.1 PKCE 客户端：浏览器授权只见事务 ID，凭证只经 OAuth 授权流程获取，任何位置都不粘贴 refresh_token。

- **工具事实来源是 MCP `tools/list`**：本 skill 只描述场景与工作流，不维护硬编码工具清单——数量与参数以实时发现为准

## 路由表（先读这里，再按路由执行）

| 用户想做什么 | 路由 | 类型 | 参考文件 |
|--------------|------|------|---------|
| 列任务 / 建任务 / 改任务 / 删任务 / 分配 / 任务日志 / 找课题 | **tasks** | 业务 | `references/tasks/README.md` |
| 写周报 / 提交周报 / 查周报 / **根据本周课题任务自动生成周报** | **reports** | 业务 | `references/reports/README.md` |
| 列出所有 MCP 工具 / 调一个路由未覆盖的工具 / 查某工具参数 schema | **free-mode** | 业务 | `references/free-mode/README.md` |
| 更新 iwp 技能本身（非业务数据） | **update** | 维护 | `references/_shared/update-flow.md` |
| 首次使用 / 配置 MCP 地址 / 安装依赖 | **setup** | 维护 | `references/_shared/setup-flow.md` |

所有路由**平权**：无主流程与兜底之分，free-mode 的通配透传是路由模式而非层级兜底。

路由命中后：**读对应参考文件 → 按其工作流执行**。

## 授权铁律（每次调工具前）

任何路由、任何工具调用之前，按顺序完成两道检查：

0. **事前检查**（会话首次调用前执行一次）：`python scripts/preflight.py` 确认依赖与 `.env` 配置就绪；有缺失时按 `references/_shared/setup-flow.md` 引导用户完成配置（检查分流、创建 `.env`、可达性探测的唯一事实来源）
1. **授权检查**：`python cli.py auth status` 返回 `authorized: true` 即有效。无效或缺失时，按 `references/_shared/auth-flow.md` 执行三方 OAuth 流程（**授权前必读**：授权流程、端口占用、超时与 state 校验的唯一事实来源，本文不重复其步骤）

## 调用约定

所有工具调用走统一 CLI 入口：技能根目录 `cli.py`（内部路径基于 SKILL_DIR 解析，cwd 无关；文档示例约定 `cd` 到技能目录后执行）。

- **透传**：`python cli.py call <工具名> --args '<JSON 对象>'`；参数含中文或复杂结构时改用 `--args-file <file.json>`（bash 内联 JSON 会被转码，禁止内联中文参数）
- **高频场景**：`python cli.py tasks list --mine --all`（自动翻页 + 状态标签）；`python cli.py auth status|start|finish|invalidate`
- **schema 优先**：调用示例仅示意，参数以 `python cli.py tools` 输出的 inputSchema 为准（工具事实来源仍是 MCP `tools/list`）→ `references/_shared/tool-discovery.md`
- **输出契约**：stdout 永远是 ASCII-safe JSON（任何管道编码下无损不乱码）；需要中文可读的大段结果加 `--out file.json`（UTF-8 文件，用读文件工具查看）。成功 `{"ok":true,...}` 退出码 0；失败 `{"ok":false,"error":{kind,message,hint}}` 退出码 1；用法错误退出码 2
- 错误翻译 → `references/_shared/failure-modes.md`；输出渲染 → `references/_shared/output-format.md`
- 连接/协商诊断：`python cli.py selfcheck`
- **写操作完整预览**：任何写操作（create / update / delete / assign / 写日志 / 周报创建与提交，含 free-mode 透传的写工具）执行前，按 `references/_shared/write-preview.md` 生成全字段完整预览并经用户确认，执行后回读核验

## 相关文档

- `references/tasks/README.md` / `references/reports/README.md` / `references/free-mode/README.md` - 业务路由场景提示词；`references/_shared/update-flow.md` - update 路由工作流
- `references/_shared/` - 授权工作流 / 工具发现（schema 优先）/ 错误码翻译 / 输出格式
- `cli.py` - 统一 CLI 入口（透传 call / tools / auth / tasks list / selfcheck；输出契约见 SKILL.md 调用约定）
- `skill_config.py` + `scripts/`（auth / client / token_store / swagger_meta）- 纯基础设施（cli.py 的内部依赖,agent 不直接调用）
