---
name: adapt-materal-enums
description: "Materal-specific enum adaptation workflow: fetch enum values from provider API, let LLM fill suggested_name, then apply patch with aptx-ft to generate final TypeScript models. Use only when Materal naming rules are required."
---

# Materal Framework 枚举适配器（专用）

使用底层命令，不包含本地脚本包装。

## 前置条件

在目标项目安装 aptx 包，并确保可执行 `aptx-ft`：

```bash
pnpm add -D @aptx/frontend-tk-cli
```

## 强约束流程

1. 必须先从接口拉取枚举数据并生成 patch。
2. 必须由 LLM 根据 `comment` 回填有语义的 `suggested_name`，不允许保留 `Value1/Value2` 风格命名。
3. 仅在 `suggested_name` 已完整回填后执行 apply 生成模型。
4. 生产环境在 apply 成功后必须删除中间产物：`enum-patch.json`、`enum-patch.translated.json`。

## 使用方法

```bash
# 1) 拉取 Materal 枚举 patch（关闭自动命名，交给 LLM）
pnpm exec aptx-ft -i <spec-file> materal enum-patch --base-url <base-url> --output ./tmp/enum-patch.json --naming-strategy none

# 2) 让 LLM 填充 patch 中每个 item 的 suggested_name
# 约定：根据 comment 翻译成语义化 PascalCase 名称，保留 value/comment 语义

# 3) 应用翻译后的 patch（要求 suggested_name 非空）
pnpm exec aptx-ft -i <spec-file> model enum-apply --patch ./tmp/enum-patch.translated.json --output ./generated/models --style module --conflict-policy patch-first

# 4) 生产环境清理中间产物（必须）
# macOS / Linux
rm -f ./tmp/enum-patch.json ./tmp/enum-patch.translated.json

# PowerShell
Remove-Item ./tmp/enum-patch.json, ./tmp/enum-patch.translated.json -ErrorAction SilentlyContinue
```

可选（未使用 pnpm 时）：

```bash
npx aptx-ft -i <spec-file> materal enum-patch --base-url <base-url> --output ./tmp/enum-patch.json --naming-strategy none
npx aptx-ft -i <spec-file> model enum-apply --patch ./tmp/enum-patch.translated.json --output ./generated/models --style module --conflict-policy patch-first
```

## 高级参数

`materal:enum-patch` 命令支持以下可选参数：

- `--max-retries <n>`：网络请求失败时的最大重试次数，默认值 3
- `--timeout-ms <ms>`：单次请求的超时时间（毫秒），默认值 10000（10秒）

示例（自定义超时和重试）：

```bash
pnpm exec aptx-ft -i <spec-file> materal enum-patch --base-url <base-url> --output ./tmp/enum-patch.json --naming-strategy none --max-retries 5 --timeout-ms 30000
```

## 输出

- `enum-patch.json`：来自接口的枚举补丁，成员字段为 `value` / `suggested_name` / `comment`（Materal 默认映射：`Key -> value`，`Value -> comment`）。
- `enum-patch.translated.json`：LLM 回填后的补丁。
- 最终模型目录：包含适配后的 enum 声明。

apply 成功后必须清理上述两个中间文件，仅保留最终模型输出。

## 边界

本 skill 仅用于 Materal 专用适配。  
通用 OpenAPI 项目请使用 `generate-artifacts` 或 `generate-models`。
