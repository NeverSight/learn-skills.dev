---
name: generate-sls-sop
description: 将 SLS project 或输入目录转换为结构化的 overview.md SOP 文档。当用户提供 SLS project 名称、要求生成日志分析 SOP、从 index/dashboard 生成文档、或提到 generate-sls-sop 时触发。
compatibility: Python 3, aliyun CLI >= v3.0.308, network access
license: MIT
---

# Generate SLS SOP

> **路径变量**：`<project_dir>` project 级目录（如 `.input/my-project/`） · `<logstore_dir>` = `<project_dir>/<logstore_name>/`

支持两种输入方式：
1. **SLS Project 名称**：自动通过 `aliyun` CLI 获取 index/dashboard 数据，然后生成 SOP
2. **本地目录**（输入目录）：直接从已有数据目录生成 SOP

> **输入目录结构**（fetch 脚本输出 / 手动准备均可）：
> ```
> <logstore_dir>/
> ├── index.json              # 必需：logstore 索引配置
> ├── dashboards/             # 资源目录：关联的仪表盘 JSON
> │   └── *.json
> ├── alerts/                 # 资源目录：关联的告警规则 JSON
> │   └── *.json
> ├── scheduled_sqls/         # 资源目录：关联的定时 SQL JSON
> │   └── *.json
> └── saved_searches/         # 资源目录：关联的快速查询 JSON
>     └── *.json
> ```
> 合法目录需包含 `index.json`（由 `fetch_sls_data.py` 生成）。

## 执行约定

> ⚠️ **必须**在 workspace 根目录执行，禁止cd到 skill 目录。违反此约定将导致相对路径解析失败。

## 前置条件

- 当输入为 SLS project 名称时，需要 `aliyun` CLI **>= v3.0.308** 已安装并完成鉴权配置（`aliyun sls` 子命令在 v3.0.308 引入）
  - 安装参考：https://github.com/aliyun/aliyun-cli
  - **版本验证**：执行 `aliyun version`，确认版本号 >= 3.0.308
  - **鉴权验证**：执行 `aliyun configure list`，确认存在已配置 AccessKey 的 profile；若无任何 profile，提示用户先运行 `aliyun configure` 配置 AccessKey ID/Secret 和 Region
- 执行 fetch 或 validate_queries 时，须在**非沙箱环境**中运行（沙箱会限制系统证书链访问，导致 TLS 失败）

## 工作流程

**检查清单**（执行时勾选）：

- [ ] Step 0：恢复检测（`--resume-check` -> 按 action 路由）

**Phase A**（project 级准备，全局一次性执行）：

> Steps 1-3 针对整个 project 执行一次，一次性处理所有 logstore。

- [ ] Step 1：定位数据源（SLS fetch / 本地 / 关键词搜索）
- [ ] Step 2：`prepare_project.py` 批量预处理
- [ ] Step 3：批量过滤 + 确认输出路径 ← 全局检查点，完成前不进入 Phase B

**Phase B**（per-logstore 生成）：

对每个 logstore（`<logstore_dir>`）执行：
- [ ] `update_status.py <project_dir> --mark-in-progress <logstore>`
- [ ] Step 4：参考文档提取（条件执行）
- [ ] Step 5：生成字段说明
- [ ] Step 6：精选查询
- [ ] Step 7：归一化模板
- [ ] Step 8：验证查询（可选）
- [ ] Step 9：清理 + 标注
- [ ] Step 10：渲染片段 + 报告
- [ ] Step 11：组装输出
- [ ] `update_status.py <project_dir> --mark-completed <logstore>`

**Phase C**（全局索引更新）：
- [ ] Step 12：全局更新索引

**Phase D**（审计，可选）：
- [ ] Step 13：审计

### 数据文件参考

`<project_dir>/project_summary.json`：Step 2 输出 → Step 3 输入。
`<project_dir>/selected_logstores.json`：Step 3 脚本输出 → Phase B / Step 12 输入。

`<logstore_dir>/` 下的工作文件：

```
<logstore_dir>/
  ├── skill_options.json                 # Step 1 写入，多步骤读取
  ├── parsed/                            # 中间数据
  │   ├── fields.json                    # Step 2：原始字段（保留）
  │   ├── queries.json                   # Step 2：已去重（不可变，id: q0, q1...）
  │   ├── prepare_summary.json           # Step 2：统计
  │   ├── reference_queries.json         # Step 4（条件，id: r0, r1...）
  │   ├── field_annotations.json         # Step 5 LLM
  │   ├── query_selection.json           # Step 6 LLM
  │   ├── query_pipeline.json            # Step 6 脚本 → Step 7 归一化(+pre_cleaned_query) → Step 8c 更新
  │   ├── query_validation.json           # Step 8a 脚本 → Step 8b 写回 pass/error
  │   ├── query_validation_LLM.json      # Step 8a 脚本（条件） → LLM 处理 → Step 8b 写回
  │   ├── query_annotations.json         # Step 9 LLM
  │   └── query_report.md                # Step 10 脚本
  └── fragments/                         # 组装片段
      ├── datasource.md                  # Step 2（不可变）
      ├── fields_table.md                # Step 5 脚本渲染（render_fields.py）
      ├── queries_selected.md            # Step 10（selected 或 extra 非空时）
      ├── queries_extra.md               # Step 10（条件）
      └── common_values.md               # Step 10 脚本（合并 reference 查询值，空时不生成）
```

`queries.json` 中每个 query 包含 `source_type` 字段（`"dashboard"`、`"alert"`、`"scheduled_sql"`、`"saved_search"`）和 `logstore` 字段，用于精选、分类和 Step 3 推断时参考。

---

### Step 0: 恢复检测

**LLM**：从用户输入推断 `<project_dir>`（SLS project 名称 → `.input/<project>/`；本地路径 → 直接使用或取父目录；关键词 → 搜索 workspace）。若无法确定或目录不存在，直接跳到 Step 1。

**脚本**：运行恢复检测：

```bash
python3 scripts/update_status.py <project_dir> --resume-check
```

输出示例：

```json
{
  "action": "resume_phase_b",
  "summary": {
    "total": 100,
    "pending": 68,
    "in_progress": 2,
    "completed": 27,
    "failed": 3
  },
  "pending_logstores": ["logstore_c", "logstore_d", "..."],
  "in_progress_logstores": ["logstore_a", "logstore_b"],
  "failed_logstores": [
    {"name": "logstore_x", "failed_step": 6}
  ]
}
```

根据 `action` 字段跳转到对应阶段，`action` 含义：
- `"first_run"` -- 无 selected_logstores.json -> 正常执行 Step 1
- `"resume_phase_b"` -- 有 pending/in_progress -> 跳到 Phase B
- `"all_completed"` -- 全部 completed -> 跳到 Phase C（Step 12）

**LLM**：向用户报告 summary 中的进度，按 action 路由到对应步骤。

### Step 1: 定位数据源

用户输入四种形式，按优先级匹配：

1. **SLS Project 名称**：用户提供 project（可选附带 logstore 名称）→ 继续本步骤
2. **本地路径（project 目录）**：验证目录下存在 logstore 子目录 → 跳到 Step 2
3. **本地路径（logstore 目录）**：验证目录结构（含 `index.json` 和至少一个资源子目录）→ 推断 project_dir = 父目录，logstore = 目录名 → Step 2 时使用 `--logstores=<logstore_name>`
4. **关键词**：在 workspace 中搜索匹配的目录（包含 `index.json`）→ 找到后跳到 Step 2

---

**以下仅 SLS Project 输入时执行。**

确认 `aliyun` CLI 可用：

1. 执行 `aliyun version`，确认版本 >= 3.0.308；若版本过低或未安装，提示用户升级/安装
2. 执行 `aliyun configure list`，确认存在已配置 AccessKey 的 profile；若无任何 profile，提示用户先运行 `aliyun configure` 配置 AccessKey ID/Secret 和 Region

**确定参数**：

- **仅 project**：不传 `--logstores`，fetch 自动处理所有有关联资源的 logstore（internal logstore 已自动过滤）
- **project + logstore(s)**：传 `--logstores=<ls1,ls2,...>`，仅 fetch 用户指定的 logstore

**执行 fetch**（须在非沙箱环境运行）：

```bash
python3 scripts/fetch_sls_data.py <project> .input/<project>/ \
  [--logstores=<ls1,ls2,...>] \
  > /tmp/sls_fetch_summary_<project>.json \
  2>/tmp/sls_fetch_err_<project>.log
```

> 参数和输出格式详见 [fetch_sls_data.py](scripts/fetch_sls_data.py) 顶部 docstring。

**结果检查**：读取 `/tmp/sls_fetch_summary_<project>.json`，检查 `errors` 是否为空。非空则检查具体错误（常见：API 鉴权失败、dashboard 不存在）。

**数据摘要**：展示 stdout 中的 `data_summary.md` 内容，向用户报告数据过滤流。

**fetch 后处理**：根据 summary 中 `logstores_processed` 展示各 logstore 关联资源数量。检查 `warnings` 中有无 "No index config" 提示——这些 logstore 会在 Step 2 被自动跳过（无 `index.json`）。

**用户选项持久化**（解析用户指令，调用脚本批量写入 `skill_options.json`）：

解析用户指令中的可选参数：
- `output_format`：用户提及"生成 SKILL"、"SKILL 格式"、"技能文档"等 → 加 `--output-format SKILL`；否则默认 `--output-format SOP`
- `validate_queries`：用户提及"验证 query"、"检查 query"等 → 加 `--validate-queries`
- `reference_source`：
  - **用户指定参考目录**：加 `--reference-dir <path>`（脚本按文件名自动匹配）
  - **用户显式指定 logstore + 文档**：加 `--reference <logstore>=<file>`

```bash
python3 scripts/save_options.py <project_dir> \
  [--output-format SOP|SKILL] \
  [--validate-queries] \
  [--reference-dir <path>] \
  [--reference <logstore>=<file> ...]
```

> 脚本为每个 logstore 写入 `skill_options.json`，确保后续步骤能独立读取用户选项。
>
> **注意**：`save_options.py` 不需要 `--logstores` 参数——它通过检查 `index.json` 自动识别有效 logstore（即 Step 1 fetch 阶段已处理的 logstore）。

### Step 2: 批量预处理

一次调用处理整个 project 下所有有效 logstore：

```bash
python3 scripts/prepare_project.py <project_dir> \
  > /tmp/sls_prepare_summary_<project>.json 2>/tmp/sls_prepare_err_<project>.log
```

> 自动处理 `<project_dir>` 下所有有效 logstore（纯本地解析，执行很快）。
> 参数和输出格式详见 [prepare_project.py](scripts/prepare_project.py) 顶部 docstring。

**结果检查**：读取 `<project_dir>/project_summary.json`，检查 `errors` 是否为空。

### Step 3: 名称简化 + 确认输出路径

> 全局检查点（Phase A 收尾），处理完成前不进入 Phase B。

对所有 logstore 执行名称简化、去重，并确认输出路径。Read [naming_rules.md](rules/naming_rules.md)，严格按规则执行。

输入：`<project_dir>/project_summary.json`（Step 2 输出）
输出：`<project_dir>/selected_logstores.json` + 各确认 logstore 的 `skill_options.json` 追加 `output_path`

---

> **Phase B 开始**
>
> 运行 `python3 scripts/update_status.py <project_dir> --resume-check` 获取当前状态：
> - `pending_logstores`: 未开始 → 启动新任务
> - `in_progress_logstores`: 处理中（可能是其他 agent 正在执行，或上次中断）→ 勿重复启动
> - `failed_logstores`: 失败 → 需人工介入
>
> **执行方式**（按平台能力选择）：
> - **并行**（平台支持多任务/子代理）：为每个 logstore 启动独立任务，各自执行 Steps 4-11
>   - **限流防护**：同时运行的 agent 数量不超过 8 个
> - **串行**（单 logstore 或平台不支持并行）：逐个 logstore 执行 Steps 4-11
>
> **禁止**跨 logstore 交替执行（如先做所有 Step 5 再做所有 Step 6），以免上下文污染。
>
> **进度监控**：定期运行 `--resume-check` 刷新状态。
>
> **结束条件**：当 `pending_logstores` 和 `in_progress_logstores` 均为空时，Phase B 完成，进入 Phase C。
>
> ---
>
> 以下 Steps 4-11 在当前 logstore（`<logstore_dir>`）上下文中执行。
>
> **Step 级检查点**：每个 step 完成后标记进度，支持中断后从上次完成位置恢复。

**检测恢复点**：`python3 scripts/update_status.py <project_dir> --step-resume-check <logstore>`

输出示例：`{"resume_from": 8}`

按 `resume_from` 跳转到对应步骤；若为 4 则从头开始；若为 12 则已完成。

**标记进行中**：`python3 scripts/update_status.py <project_dir> --mark-in-progress <logstore>`

### Step 4: 参考文档提取

> 条件步骤：仅当 `skill_options.json` 中含 `reference_source` 字段时执行，否则跳过。

Read [reference_extract.md](rules/reference_extract.md)，严格按规则执行。

输入：`skill_options.json` 中 `reference_source` 指定的参考文档
输出：`parsed/reference_queries.json`（与 `queries.json` 相同 schema，id 前缀 `r`）

### Step 5: 生成字段说明

为每个字段生成简短中文描述。Read [field_desc.md](rules/field_desc.md)，严格按规则执行。

输入：`parsed/fields.json`（Step 2 生成的字段列表）
输出：`fragments/fields_table.md`

### Step 6: 精选查询

> LLM 负责语义选择，脚本负责数据组装。

Read [query_select.md](rules/query_select.md)，严格按规则执行。

输入：`parsed/queries.json`（Step 2） + `parsed/reference_queries.json`（Step 4，如存在）
输出：`parsed/query_pipeline.json`（完整 pipeline，后续步骤的数据源）

### Step 7: 归一化模板

运行归一化脚本，将所有模板语法统一为 `<var;default>` / `<var>` 格式，并生成 `pre_cleaned_query`（剥离 `;default`）：

```bash
python3 scripts/normalize_templates.py <logstore_dir>
```

> 纯脚本执行，无需 LLM。

输入：`parsed/query_pipeline.json`（Step 6 输出）
输出：`parsed/query_pipeline.json`（更新：每条 query 增加 `normalized_query` 和 `pre_cleaned_query`）

> `pre_cleaned_query` = `normalized_query` 中的 `<var;default>` 自动剥离为 `<var>`，供 Step 9 LLM 审视。

**记录步骤成功**：`python3 scripts/update_status.py <project_dir> --mark-step <logstore> --step 7`

### Step 8: 验证查询（可选）

> 仅当 `skill_options.json` 中 `validate_queries` 为 true 时执行，否则跳过。

对 pipeline 中的查询进行语法验证，移除失败项并递补。Read [query_verify.md](rules/query_verify.md)，严格按规则执行。

输入：`parsed/query_pipeline.json`（Step 7 输出，含 `normalized_query`）
输出：`parsed/query_pipeline.json`（更新：移除失败项、递补、添加 `validation` 统计）

### Step 9: 清理 + 标注

> 必须由 LLM 直接处理，不得编写脚本代替。

Read [query_format.md](rules/query_format.md)，严格按规则执行。

输入：`parsed/query_pipeline.json`（Step 7/8 输出）
输出：`parsed/query_annotations.json`（独立注解文件，仅含 id/title/category/cleaned_query）

### Step 10: 渲染片段 + 报告

运行渲染脚本：

```bash
python3 scripts/render_queries.py <logstore_dir>
```

脚本读取 `parsed/query_pipeline.json` + `parsed/query_annotations.json`，合并后生成：
- `fragments/queries_selected.md`（selected 或 extra 非空时）
- `fragments/queries_extra.md`（extra 非空时）
- `parsed/query_report.md`（必须）

> 脚本还读取 `parsed/prepare_summary.json`、`parsed/reference_queries.json`（如存在）和 `parsed/query_validation.json` + `parsed/query_validation_LLM.json`（如存在）用于报告。
> 此步骤为纯脚本执行，无需 LLM。

**记录步骤成功**：`python3 scripts/update_status.py <project_dir> --mark-step <logstore> --step 10`

### Step 11: 组装输出

参考 `<logstore_dir>/fragments/queries_selected.md`（查询分类）和 `fragments/fields_table.md`（字段构成），生成：

- **name**：简短可读名（语义翻译优先，如 `xxx_audit_log` → "审计日志（xxx_audit_log）"；无法翻译时用原名）
- **description**：一句话功能定位，从查询分类和字段推断所属系统与用途，禁止直接罗列分类名或套用通用模板

运行组装脚本：

```bash
python3 scripts/assemble_overview.py <logstore_dir> \
  --name "..." --description "..."
```

> 组装结果写入 `skill_options.json` 中 `output_path` 指定的路径。

**记录步骤成功**：`python3 scripts/update_status.py <project_dir> --mark-step <logstore> --step 11`

**记录处理完成**：`python3 scripts/update_status.py <project_dir> --mark-completed <logstore>`

> **Phase B 结束**：返回处理下一个 pending logstore，或进入 Phase C。

### Step 12: 全局更新索引

> 全局一次性执行（Phase C）。

从最深层目录向上逐级更新或新建索引文件。Read [index_rules.md](rules/index_rules.md)，严格按规则执行。

输入：`<project_dir>/selected_logstores.json`（含所有已确认 logstore 的 output_path 和 output_root）
输出：各级目录的索引文件（已有则更新，不存在则按模板新建）

**Phase C 完成**：提示用户 SOP 生成已完成，询问是否需要进行质量审计（Phase D，可选，建议新会话执行）。

---

> **Phase D 开始**（可选，建议新会话）：仅在用户显式请求审计或 Phase C 完成后用户确认需要质量审查时执行。审计强烈建议在独立会话中执行，以获得客观视角，避免生成阶段的上下文偏见。

### Step 13: 审计

> 可选步骤，用于审计 LLM 生成内容的语义质量。

Read [audit_rules.md](rules/audit_rules.md)，严格按规则执行。

输入：`<project_dir>/selected_logstores.json`（已完成的 logstore 列表）
输出：`<project_dir>/_audit/`（审计计划、per-logstore 结果、汇总报告）

---

## 故障排查

见 [troubleshooting.md](rules/troubleshooting.md)。
