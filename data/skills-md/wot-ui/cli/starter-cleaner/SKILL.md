---
name: starter-cleaner
description: 将 wot-starter v2 模板精简为最小可开发状态，移除文档、演示分包、生成文件和 monorepo 配置，并同步清理相关 Vite 与 package.json 配置。用户要求“清理模板”“移除示例”“生成最小模板”“精简 wot-starter v2”时使用。
---

# Starter Cleaner

使用随技能提供的确定性脚本清理 `wot-starter` v2，保留基础页面、Wot UI、`uni-echarts` 和 `echarts` 能力。

## 执行流程

1. 在项目根目录运行 `git status --short`，确认并告知用户未提交改动会被保留，但待清理目录中的改动会随目录一起删除。
2. 如果用户尚未明确要求执行清理，先说明这是破坏性操作并取得确认。
3. 先预览清理计划：

   ```sh
   node .agents/skills/starter-cleaner/scripts/clean.js --dry-run
   ```

4. 确认目标是 `wot-starter` v2 后执行。脚本会删除旧的 `src/pages.json`，然后受控运行 `pnpm dev:h5`，等新的最小 `src/pages.json` 生成后退出 dev server：

   ```sh
   node .agents/skills/starter-cleaner/scripts/clean.js
   ```

5. 执行 `pnpm install --lockfile-only` 更新锁文件，再运行 `pnpm type-check` 和 `pnpm lint`。如果依赖不可用，至少检查 `git diff --check` 和清理后的 diff，并将未运行的验证明确告知用户。

## 清理范围

脚本执行以下操作，且支持重复运行：

- 删除 `docs/`、`src/subPages/`、`src/subEcharts/`、`src/subAsyncEcharts/`。
- 删除旧的 `src/pages.json`，再通过 `pnpm dev:h5` 触发 `vite-plugin-uni-pages` 重新生成最小页面配置。
- 删除 `pnpm-workspace.yaml`，将项目从文档 workspace 恢复为单包项目。
- 从 `vite.config.ts` 的 `UniHelperPages` 配置中移除上述三个示例分包入口。
- 从 `package.json` 中移除 `docs:*` 与 `lint:docs` 脚本。
- 保留 `uni-echarts`、`echarts` 依赖和相关 Vite 配置，方便业务继续使用图表。

## 安全约束

- 不直接拼接或扩展删除路径；仅使用脚本内的固定清单。
- 不在非 `wot-starter` v2 项目中运行。仅在用户明确确认目标项目后使用 `--force` 跳过项目身份检查。
- 不用 `--force` 绕过未提交改动提示；该参数只用于项目身份检查。
