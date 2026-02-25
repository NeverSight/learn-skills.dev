---
name: download-openapi
description: "Download remote OpenAPI JSON to local file via aptx-ft. Use when user asks to fetch swagger/openapi from URL, save spec to openapi.json, or prepare local input for later model/service generation."
---

# 下载 OpenAPI JSON

使用底层命令，不包含本地脚本包装。

## 前置条件

在目标项目安装 aptx 包，并确保可执行 `aptx-ft`：

```bash
pnpm add -D @aptx/frontend-tk-cli
```

## 执行步骤

1. 选择输出文件路径（建议 `./openapi.json`）。
2. 执行下载命令。
3. 下载成功后，把该文件路径交给其他技能（如模型生成、请求框架生成）。

```bash
pnpm exec aptx-ft input download --url <url> --output <file>
```

可选（未使用 pnpm 时）：

```bash
npx aptx-ft input download --url <url> --output <file>
```

示例：

```bash
pnpm exec aptx-ft input download --url https://api.example.com/swagger.json --output ./openapi.json
```

## 输出

- 本地 OpenAPI JSON 文件（例如 `./openapi.json`）。

## 边界

本 skill 仅处理 OpenAPI JSON 格式的下载：
- 不支持 YAML 格式的 OpenAPI 规范
- 不处理需要认证的 URL（如需要 Bearer Token）
- 不处理自定义请求头
- 下载后不自动验证 OpenAPI 规范的有效性（仅验证 JSON 语法）

如需上述功能，请手动下载后使用其他工具处理。
