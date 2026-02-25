---
name: piracy-handler
description: 盗版检测与后置处理编排器。Use when wechat-search-collector 综合页任务完成后，需要基于 capture_results 进行盗版检测、创建子任务、写入 webhook 计划，或在子任务终态后执行 webhook dispatch/reconcile。支持 sqlite/supabase 二选一作为 capture_results 数据源。
---

# Piracy Handler

执行目录：`~/.agents/skills/piracy-handler/`

## 1) 主流程

### A. 综合页后置（推荐）

```bash
npx tsx scripts/piracy_detect.ts --task-ids <TASK_ID[,TASK_ID2,...]> --data-source <sqlite|supabase>
npx tsx scripts/piracy_create_subtasks.ts --input <DETECT_JSON_PATH>
npx tsx scripts/upsert_webhook_plan.ts --source detect --input <DETECT_JSON_PATH>
```

### B. 一条命令全流程（兼容入口）

```bash
npx tsx scripts/piracy_pipeline.ts --task-ids <TASK_ID_1,TASK_ID_2,...>
```

说明：`piracy_pipeline.ts` 保留为兼容壳，内部复用 detect runner + create/upsert。
默认会按 `--task-app com.tencent.mm --task-date Today` 扫描；`--task-app/--task-date` 均支持 CSV 多值（例如 `--task-date Today,Yesterday`）。
当 `--task-date` 提供多个值时，处理顺序按输入优先级依次进行（如 `Today` 优先于 `Yesterday`）。`--task-ids` 与 `--task-app/--task-date` 互斥。

### C. webhook 触发与补偿

```bash
npx tsx scripts/webhook.ts --mode single --task-id <TASK_ID> --data-source <sqlite|supabase>
npx tsx scripts/webhook.ts --mode reconcile --date <YYYY-MM-DD> --data-source <sqlite|supabase>
```

## 2) 职责边界

- `capture_results` 读取：支持 `sqlite|supabase`
- 任务表读取/子任务创建：当前仍走飞书任务表（`TASK_BITABLE_URL`）
- 剧单元数据：当前仍走飞书剧目表（`DRAMA_BITABLE_URL`）
- webhook 计划读写：当前仍走飞书 webhook 表（`WEBHOOK_BITABLE_URL`）

## 3) 关键脚本

- `scripts/piracy_detect.ts`
作用：按 TaskID（或从飞书筛选）生成 detect.json；支持 sqlite/supabase 数据源；检测仅纳入 `status=success` 的综合页任务结果，ratio 采用 `>=` 阈值判定。
- `scripts/piracy_create_subtasks.ts`
作用：基于 detect.json 创建子任务（个人页/合集/锚点）。
- `scripts/upsert_webhook_plan.ts`
作用：webhook plan 唯一入口；支持 `--source detect`（从 detect.json 产出计划）与 `--source plan`（通用计划输入）。
去重键为 `BizType + Date + GroupID`，按目标键精确查询历史记录，避免大表场景下重复创建。
- `scripts/webhook.ts`
作用：webhook 统一入口；`--mode single` 用于单 group 触发，`--mode reconcile` 用于按日期批量补偿。
- `scripts/dedupe_webhook_plans.ts`
作用：一次性清理 webhook 计划表中的历史重复记录（默认执行删除，`--dry-run` 仅预览）。
运行约束：需确保 `WEBHOOK_USE_VIEW` 关闭，避免视图过滤导致清理不完整。

## 4) 公共模块（重构后）

- `scripts/shared/lib.ts`
通用工具函数、时间/解析、以及 task-manager/webhook-upsert 子进程桥接。
- `scripts/shared/cli.ts`
通用 CLI 参数解析辅助（`limit`、正整数等）。
- `scripts/data/result_source.ts`
统一 `capture_results` 读取接口（sqlite/supabase）。
- `scripts/data/result_source_cli.ts`
统一 `--data-source/--sqlite-path/--table/--page-size/--timeout-ms` 解析。
- `scripts/detect/task_units.ts`
统一任务分组逻辑：`--task-ids` 与 `--task-app/--task-date` 互斥；缺省时按飞书筛选条件分组。
- `scripts/detect/core.ts`
detect 聚合/阈值/summary 核心逻辑。
- `scripts/detect/runner.ts`
统一 detect 执行与输出路径策略。
- `scripts/webhook/lib.ts`
webhook 计划读取、状态聚合、dispatch/reconcile 核心逻辑。

目录结构速览：`scripts/README.md`

## 5) 环境变量

| 变量 | 用途 |
|---|---|
| `FEISHU_APP_ID` / `FEISHU_APP_SECRET` | 飞书应用凭证 |
| `TASK_BITABLE_URL` | 任务状态表 |
| `DRAMA_BITABLE_URL` | 剧单元信息表（detect 仍依赖） |
| `WEBHOOK_BITABLE_URL` | webhook 计划表 |
| `CRAWLER_SERVICE_BASE_URL` | webhook 推送与豁免检查服务 |
| `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` | `--data-source supabase` 时读取 `capture_results` |
| `SUPABASE_RESULT_TABLE` | Supabase 结果表名（默认 `capture_results`） |
| `TRACKING_STORAGE_DB_PATH` | sqlite 模式默认数据库路径 |

## 6) 参考文档

- 详细命令、参数与样例：`references/commands.md`
- webhook ready 语义：组内任务需全部为 `success|error`（`failed` 不视为 ready）。
