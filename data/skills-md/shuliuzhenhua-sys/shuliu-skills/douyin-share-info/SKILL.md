---
name: douyin-share-info
description: 通过抖音分享链接调用 TikHub Douyin Web API 获取作品基础信息，并固定提取封面、音频、视频下载地址（均取第一个 url_list）。当用户提到“抖音分享链接解析”“根据分享链接取视频信息/封面/音频/播放地址”时使用。
---

# 抖音分享链接基础信息

通过 TikHub 的 Douyin Web 接口，根据分享链接提取作品基础信息。

## Script Directory

**Important**: All scripts are located in the `scripts/` subdirectory of this skill.

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/main.ts`
3. Replace all `${SKILL_DIR}` in this document with the actual path

## Usage

```bash
# 输出结构化 JSON（推荐）
npx -y bun ${SKILL_DIR}/scripts/main.ts \
  --share-url "https://v.douyin.com/xxxxxx/" \
  --json

# 同时保存原始响应
npx -y bun ${SKILL_DIR}/scripts/main.ts \
  --share-url "https://v.douyin.com/xxxxxx/" \
  --json \
  --raw out/raw.json
```

## Options

- `--share-url <url>`, `--url <url>`: 抖音分享链接（必填）
- `--raw <path>`: 保存 TikHub 原始响应 JSON 到文件
- `--json`: JSON 输出（默认开启，兼容现有习惯）
- `-h`, `--help`: 显示帮助

## Env

- `TIKHUB_API_KEY`（必填）
- `TIKHUB_BASE_URL`（可选，默认 `https://api.tikhub.io`）

请求头使用：`Authorization: Bearer $TIKHUB_API_KEY`

## Fixed Extraction Rules

- 封面：`data.aweme_detail.video.origin_cover.url_list[0]`
- 音频：`data.aweme_detail.music.play_url.url_list[0]`
- 视频：按数组顺序遍历 `data.aweme_detail.video.bit_rate[*].play_addr.url_list[0]`，取第一个可用地址

## Output

输出字段：
- `share_url`
- `aweme_id`
- `desc`
- `author`（`uid`、`sec_uid`、`unique_id`、`nickname`）
- `cover_url`（按规则取第一个）
- `audio_url`（按规则取第一个）
- `video_url`（按规则取第一个）
- `video_url_first_available`（按数组顺序遇到的第一个可用链接）
- `video_quality_selected`（命中的清晰度标签）
- `video_bit_rate_count`
- `api`（`code`、`message`、`request_id`）
