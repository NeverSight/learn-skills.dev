---
name: tailwindcss-next-init
description: Initialize Tailwind CSS v4 and Iconify for Next.js App Router projects with script-driven templates. Use when you need a fast setup or migration with consistent style-entry conventions.
metadata:
  author: adonis
---

# Tailwindcss Next Init

## 概览

用本 skill 为目标仓库生成 Tailwind v4 初始化骨架，并给出可复制的依赖安装命令、布局导入检查结果、`@source` 与 `@reference` 使用建议。
优先运行脚本完成标准化输出，避免手工遗漏。

## 标准流程

1. 识别目标项目结构。
- 检查 `<project-root>/package.json` 是否存在。
- 检查 `src/app/layout.tsx` 或 `app/layout.tsx` 是否存在。
- 检查 `src/styles/` 与 `styles/` 目录状态。

2. 先做 dry-run 预览。
- 运行：
```bash
python3 scripts/init_tailwind_v4.py --project-root /abs/path/to/project --dry-run
```
- 先确认将创建/覆盖的文件，再决定是否执行真实写入。

3. 执行初始化写入。
- 默认最小模板：
```bash
python3 scripts/init_tailwind_v4.py --project-root /abs/path/to/project
```
- 贴近本仓库模板：
```bash
python3 scripts/init_tailwind_v4.py --project-root /abs/path/to/project --preset project-like
```
- 已有文件需覆盖时显式加 `--force`。

4. 处理依赖安装。
- 按脚本输出的包管理器命令安装依赖（脚本只生成命令，不直接执行安装）。
- 默认图标策略是 `--icons all`，安装 `lucide/mdi/tabler` 三套图标集。

5. 检查导入与扫描边界。
- 若脚本提示缺少全局样式导入，在目标 `layout.tsx` 增加：
```ts
import "@/styles/globals.css";
import "@/styles/custom.css";
```
- 若类名来自 `node_modules` 或扫描盲区，按提示在 `tailwind-core.css` 增加 `@source`。

6. 进行项目验证。
- 至少执行一次构建链路检查（如 `pnpm typecheck`、`pnpm dev`）。
- 确认页面样式生效、Iconify 图标类可渲染。

## 脚本参数契约

`scripts/init_tailwind_v4.py` 支持以下参数：
- `--project-root <path>`：目标项目根目录（必填）
- `--preset minimal|project-like`：模板风格，默认 `minimal`
- `--icons all|lucide|none`：图标策略，默认 `all`
- `--package-manager auto|pnpm|npm|yarn|bun`：包管理器，默认 `auto`
- `--dry-run`：仅预览，不写文件
- `--force`：覆盖已存在文件

## 资源说明

- `references/repo-tailwind-audit.md`
  - 记录当前仓库 Tailwind 链路与历史演进，供“项目同款”策略参考。
- `references/tailwind-v4-best-practices.md`
  - 记录 Tailwind v4 / Next.js / Iconify 的最佳实践与官方链接。
- `assets/templates/minimal/*`
  - 通用最小模板，适合跨项目快速落地。模板源文件使用 `.tpl` 后缀。
- `assets/templates/project-like/*`
  - 贴近本仓库风格，包含 safe-area、reduced-motion、theme token bridge。模板源文件使用 `.tpl` 后缀。
  - `project-like` 模板中的 `@layer ... antd ...` 为仓库同款特化项；非 Ant Design 项目可按需移除该 layer。

模板后缀约定：
- 模板源：`*.tpl`
- 目标产物：`src/styles/*.css` 或 `styles/*.css`（脚本自动判定）
- `init_tailwind_v4.py` 严格读取 `.tpl`，不会回退读取 `.css` 模板。

## 输出约束

执行本 skill 时，始终输出：
1. 目标项目识别结果（layout、styles、package manager）
2. 将写入/已写入文件列表
3. 依赖安装命令（按所选包管理器）
4. `@source` 与 `@reference` 的建议片段
5. 验证清单（至少 3 条可执行检查项）
