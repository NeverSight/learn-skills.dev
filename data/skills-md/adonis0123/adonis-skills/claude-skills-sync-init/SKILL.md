---
name: claude-skills-sync-init
description: Bootstrap Claude skill-sync automation in any repository. Use when users ask to set up `.agents/skills` to `.claude/skills` syncing, generate `skills:sync:*` scripts, inject package.json scripts/postinstall hooks, or initialize this sync workflow in a new or existing project.
---

# Claude Skills Sync Init

在目标项目中初始化 skills 同步能力时，使用本 Skill。

## Overview

目标是在目标仓库自动落地以下能力：

1. 生成 `scripts/sync-llm-skills.ts`，支持 `--source`、`--targets`、`--dry-run`。
2. 注入 `scripts.skills:sync:llm` 命令。
3. 自动确保 `devDependencies.is-ci` 存在（缺失时自动写入）。
4. 以幂等方式合并 `postinstall`，默认注入 `is-ci` CI guard。
5. 同步目标仅为 `.claude/skills`。
6. 同步过程采用原子切换，避免复制失败时清空目标目录。
7. 自动确保目标仓库 `.gitignore` 包含 `/.claude/skills`。

## Execution Flow

1. 收集上下文
- 确认目标仓库根目录（存在 `package.json`）。
- 确认源目录是否仍使用 `.agents/skills`（默认值）。
- 确认目标目录为 `.claude/skills`（默认且唯一目标）。

2. 执行自动落地脚本
- 在目标仓库执行：
```bash
node /path/to/claude-skills-sync-init/scripts/bootstrap-sync-skills.mjs --project /path/to/target-repo
```
- 可选参数：
  - `--script-name`（默认 `skills:sync:llm`）
  - `--script-path`（默认 `scripts/sync-llm-skills.ts`）
  - `--skip-postinstall`（跳过 postinstall 注入）
- `--script-name` 仅允许字符集 `[A-Za-z0-9:._-]+`，非法值必须失败退出。

3. 运行同步命令验证
- 默认验证：
```bash
pnpm run skills:sync:llm -- --dry-run
```
- 显式指定目标（可选）：
```bash
pnpm run skills:sync:llm -- --targets=claude
```

4. 输出变更摘要
- 列出新增/更新文件：
  - `scripts/sync-llm-skills.ts`
  - `package.json`
  - `.gitignore`
- 说明 `is-ci` 依赖处理结果（新增或已存在）。
- 说明 postinstall 合并结果（新建、追加、或已存在跳过），并标注 CI guard 是否生效。
- 说明 `.gitignore` 的 `/.claude/skills` 忽略规则处理结果（新增或已存在）。
- 附上验证命令与执行结果。

## Resources

- 自动落地脚本：`scripts/bootstrap-sync-skills.mjs`
- 同步脚本模板：`assets/templates/sync-llm-skills.ts`
- 集成检查清单：`references/integration-checklist.md`

## Guardrails

1. 仅在目标仓库根目录执行（必须可读写 `package.json`）。
2. 保持幂等：重复执行不得重复注入命令或 postinstall 片段。
3. 不覆盖已有 postinstall 逻辑，只做追加合并。
4. 源目录不存在时必须失败并返回非零退出码。
5. postinstall 去重必须做完整命令/完整脚本调用匹配，不能使用宽松子串匹配。
6. 同步实现必须优先复制到临时目录，再切换目标目录，并在失败时尝试回滚。
7. 若目标仓库缺少 `is-ci`，必须自动写入 `devDependencies.is-ci`，再注入 CI guard 命令。
