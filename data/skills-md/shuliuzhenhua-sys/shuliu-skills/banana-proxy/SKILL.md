---
name: banana-proxy
description: Gemini image generation via Banana proxy endpoint.
---

# Banana Proxy Image Generation

通过 Banana 代理端点调用 Gemini 生图。

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/main.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

## Usage

```bash
# 基础生图
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "A cat" --image out.png

# 指定比例与质量
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "portrait" --image out.png --ar 3:4 --quality 2k

# 使用参考图
npx -y bun ${SKILL_DIR}/scripts/main.ts --prompt "replace subject" --ref a.png b.png --image out.png

# 批量并行生图（JSONL）
npx -y bun ${SKILL_DIR}/scripts/main.ts --batch jobs.jsonl --concurrency 4
```

## Options

- `--prompt <text>`, `-p`: 提示词
- `--promptfiles <files...>`: 从文件读取提示词
- `--image <path>`: 输出路径（必填）
- `--batch <file>`: 批量任务文件（`.json` 数组或 `.jsonl` 每行一个 JSON）
- `--concurrency <n>`: 并行数（仅 `--batch` 模式生效，默认 `4`）
- `--model <id>`, `-m`: 模型（默认 `gemini-3-pro-image-preview`）
- `--ar <ratio>`: 比例，如 `1:1`、`3:4`、`16:9`
- `--quality normal|2k`: 质量（默认 `2k`）
- `--imageSize 1K|2K|4K`: 生成尺寸等级
- `--ref <files...>`: 参考图
- `--json`: JSON 输出

## Batch 文件格式

JSONL 每行示例：

```json
{"prompt":"A cat in watercolor style","image":"out/cat.png","ar":"1:1"}
{"prompt":"A cyberpunk city at night","image":"out/city.png","quality":"2k","imageSize":"2K"}
```

字段说明：
- `prompt` 或 `promptFile`（二选一）
- `image`（必填）
- 可选：`model`、`ar`、`quality`、`imageSize`、`ref`（字符串数组）

## Fixed Config

- Base URL: `https://lnapi.com`
- Primary API Key: `LNAPI_KEY`（必填）
