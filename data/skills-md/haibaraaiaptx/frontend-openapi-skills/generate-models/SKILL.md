---
name: generate-models
description: "Generate TypeScript models (interfaces/enums) from OpenAPI via aptx-ft. Use when user only needs model layer output, schema typing, or selective model generation; do not use for framework-specific enum adaptation."
---

# 生成 TypeScript 模型（通用技能）

使用底层命令，不包含本地脚本包装。

## 前置条件

在目标项目安装 aptx 包，并确保可执行 `aptx-ft`：

```bash
pnpm add -D @aptx/frontend-tk-cli
```

## 项目类型参数建议（执行前必须确认）

先判断项目类型，再给出建议参数；必须等待用户确认最终参数后再执行命令。

### 单项目（应用代码在 `src/`）

- 推荐输出：`--output ./src/models`
- 推荐风格：`--style module`
- 按需限制模型：`--name <Schema>`

示例：

```bash
pnpm exec aptx-ft -i ./openapi.json model gen --output ./src/models --style module
```

### Monorepo（共享模型包）

- 推荐输出：`--output ./packages/models/src`
- 推荐风格：`--style module`
- 如只想增量生成，使用 `--name` 限制范围

示例：

```bash
pnpm exec aptx-ft -i ./openapi.json model gen --output ./packages/models/src --style module
```

## 执行步骤

1. 准备输入（本地文件或 URL）。
2. 询问用户关键参数并确认：
   - **输出目录**：推荐 `./src/models`（单项目）或 `./packages/models/src`（Monorepo）
   - **生成风格**（必问）：
     - `module`（默认）：生成 ES Module 格式，每个类型独立 export，适合现代前端项目
     - `declaration`：生成单一声明文件，适合需要全局类型声明或兼容旧项目的场景
   - **选择性生成**（可选）：如只需部分模型，使用 `--name` 指定（可多次使用）
3. 向用户展示完整命令并确认后执行。
4. 执行命令并返回生成结果。

```bash
pnpm exec aptx-ft -i <spec-file-or-url> model gen --output <output-dir> --style <module|declaration>
```

> 注意：`--style` 默认值为 `module`，如需 `declaration` 风格需显式指定。

示例：

```bash
# 使用默认 module 风格
pnpm exec aptx-ft -i ./openapi.json model gen --output ./generated/models

# 显式指定 module 风格
pnpm exec aptx-ft -i ./openapi.json model gen --output ./generated/models --style module

# 使用 declaration 风格（单一声明文件）
pnpm exec aptx-ft -i ./openapi.json model gen --output ./generated/models --style declaration

# 选择性生成特定模型
pnpm exec aptx-ft -i ./openapi.json model gen --output ./generated/models --name User --name Role
```

可选（未使用 pnpm 时）：

```bash
npx aptx-ft -i ./openapi.json model gen --output ./generated/models --style module
```

## 输出

- TypeScript 模型文件（interface/enum）。
- 不包含请求层代码。

## 边界

- 需要同时生成模型与请求框架时，使用 `generate-artifacts`。
- 需要 Materal 专用枚举适配时，使用 `adapt-materal-enums`。
