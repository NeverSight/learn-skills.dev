---
name: stata-sep
description: Use when performing Stata analysis via Stata-MCP tools, including do file generation, execution, result analysis, or managing ado packages.
---

# Stata-sep（基于 Stata-MCP）

## 核心思路
- 目标：在 Claude Code 等 MCP 客户端中，把 Stata-MCP 的全部工具（工具列表见下文）和 agent/评估用法包装成可复用流程，减少提示词负担。
- 输出优先级：先给高层决策与最小可运行路径，再按需展开到具体工具调用/样例（渐进披露）。
- 安全默认：仅使用绝对路径；写/改文件或运行 do 前明确路径；安装 ado 包需用户确认。

## 快速起步（最小可用链路）
1) 环境探测：`uvx stata-mcp --usable`；若 `stata_cli` 失败，设置环境变量 `stata_cli` 为 Stata 可执行绝对路径（macOS 如 `/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp`，Windows 如 `C:\\Program Files\\Stata18\\StataSE.exe`）。可选 `documents_path`。  
2) 将 MCP server 加入客户端（示例 config JSON 已放 `references/usage.md`）。默认工作根：`~/Documents/stata-mcp-folder/`，自动包含 `stata-mcp-log/`、`stata-mcp-dofile/`、`stata-mcp-result/`、`stata-mcp-tmp/`。  
3) 最小流水线：
   - `write_dofile` 写入完整 do，必要时先调用 `results_doc_path` 生成输出目录。
   - `stata_do` 运行 do，返回日志路径与内容。
   - `read_file` 查看日志或结果。
   - 若需数据概览，先用 `get_data_info`（支持 .dta/.csv）。

## 工具地图（全量覆盖）
- `help(cmd)`（Unix only）：返回 Stata help。用于快速查语法。  
- `write_dofile(content, encoding?, strict_mode?)`：把 Stata 代码写入新 do，返回绝对路径。建议在顶部 `use` 数据并设置 `local output_path`（来自 `results_doc_path`）。
- `append_dofile(original_dofile_path, content, encoding?)`：在现有 do 基础上追加，或新建副本；返回新 do 路径。
- `stata_do(dofile_path, log_file_name?, is_read_log=True)`：执行 do，返回 `log_file_path` 和可选 `log_content`。  
- `read_file(file_path, encoding="utf-8")`：读取任意文本文件内容。  
- `get_data_info(data_path, vars_list?, encoding="utf-8")`：对 .dta/.csv 生成描述性统计，结果写入 tmp 目录并返回概要。  
- `ado_package_install(package, source="ssc"|"github"|"net", is_replace=True, package_source_from=None)`（Unix only）：安装 ado；首次使用需确认。  
- `load_figure(figure_path)`：载入 png/jpg，便于回显图形。  
- `mk_dir(path)`：安全创建目录。  
- Prompts：`stata_assistant_role(lang?)`、`stata_analysis_strategy(lang?)`、`results_doc_path()` 生成输出目录。

## 推荐工作流（逐层展开）
1) 数据理解：`get_data_info` → 选择变量/样本 → 形成 do 草稿。  
2) do 生成：
   - 快速试验用 `write_dofile`；增量修改用 `append_dofile`。
   - 需要表格输出时先 `results_doc_path`，在 do 里 `local output_path "<返回路径>"`，配合 `outreg2`/`esttab`。
3) 执行与回溯：`stata_do` → 如失败查看 `log_content` 或用 `read_file` 重读；必要时追加 do 并重跑。  
4) 包依赖：缺少命令时，用 `ado_package_install("  ,")` 安装；完成后复跑。  
5) 产出：用 `load_figure` 回显图形，用 `read_file` 回显表格/日志。

## Agent 模式与评估
- Agent：`uvx stata-mcp --agent` 或直接 `stata-mcp --agent`，修改示例任务位于 `stata-mcp/source/agent_examples/openai/main.py`（`model_instructions` 与 `task_message`）。
- 作为工具：`StataAgent.as_tool()` 示例见 `source/docs/Usages/agent_as/agent_as_tool.md`。
- 评估：流程与样例问答在 `source/docs/Usages/Evaluation.md`；可据此自定义评测集合。

## 参考资料（按需加载）
- `references/usage.md`：客户端配置、环境变量、最小命令速查。绝对路径：`/Users/lingguiwang/Skill-Seekers/Github/stata-sep/references/usage.md`。
- `references/tools.md`：各工具参数与返回字段、常见坑。绝对路径：`/Users/lingguiwang/Skill-Seekers/Github/stata-sep/references/tools.md`。
- `references/usage_full.md`：官方 Usage 详版（中英混排）。
- `references/advanced.md`：高级用法（传输方式、定制路径等）。
- `references/questions.md`：常见问题汇总。
- `references/evaluation.md`：评估流程与示例问答生成方法。
- `references/agent_as_tool.md`：将 Stata-Agent 作为工具嵌入其他 agent 的示例。
- `assets/config.json`：最小配置模板，可直接拷贝调整绝对路径与环境变量。
- `assets/agent_examples/`：可直接复制的 agent 示例代码（OpenAI/prompt 生成）。

## 注意事项
- 所有路径使用绝对路径；Windows 需转义反斜杠。
- 运行/写入前确认目标目录，避免覆盖用户文件。
- 安装 ado、创建目录等潜在改动操作需先向用户确认。
