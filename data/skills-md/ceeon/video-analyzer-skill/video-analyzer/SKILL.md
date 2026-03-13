---
name: video-analyzer
description: 视频内容分析。当用户提到"分析视频"、"视频分析"、"看看这个视频"、"这个视频讲了什么"、"视频笔记"、"总结视频"时触发。支持 B站、YouTube 等平台链接和本地视频文件。
---

<!--
input: 视频 URL 或本地文件路径
output: 视频内容的详细分析笔记（含时间戳）
pos: 核心 skill，视频理解能力
-->

# 视频内容分析

下载视频 → 压缩 → Files API 上传 → Responses API 分析。一次 API 调用出完整结果。

## 依赖

- `yt-dlp`（brew install yt-dlp）
- `ffmpeg`（brew install ffmpeg）

## 步骤

### 1. 读取配置

```bash
# 从 ~/.claude/skills/video-analyzer/config/secrets.md 读取
API_KEY="your-api-key-here"
API_URL="https://ark.cn-beijing.volces.com/api/v3/responses"
MODEL="doubao-seed-2-0-pro-260215"
```

### 2. 获取视频

**本地文件**：直接用。

**在线视频**（B站/YouTube 等）：
```bash
yt-dlp -f "bv*+ba/b" -o "/tmp/video-analyzer-%(id)s.%(ext)s" --no-playlist "URL"
```

B站高清需要 Cookie：
```bash
yt-dlp --cookies-from-browser chrome -f "bv*+ba/b" -o "/tmp/video-analyzer-%(id)s.%(ext)s" --no-playlist "URL"
```

### 3. 压缩（超过 100MB 时）

```bash
ffmpeg -i "输入文件" -vf "scale='min(720,iw)':-2" -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 64k -y /tmp/video-analyzer-compressed.mp4
```

实测效果：327MB → 74MB。如果还大，加 `-crf 32` 或 `-t 600` 截前 10 分钟。

### 4. 上传 Files API

```bash
curl -s https://ark.cn-beijing.volces.com/api/v3/files \
  -H "Authorization: Bearer $API_KEY" \
  -F "purpose=user_data" \
  -F "file=@/tmp/video-analyzer-compressed.mp4"
```

返回 `{"id": "file-xxx", "status": "processing"}`，提取 `id` 即 file_id。

### 5. 等待文件处理完成

文件上传后状态为 `processing`，必须等处理完才能调用分析。

| 文件大小 | 等待时间 |
|---------|---------|
| < 30MB | sleep 15 |
| 30-100MB | sleep 45 |
| > 100MB | sleep 60，或轮询状态 |

如果调用分析返回 `OperationDenied.InvalidState` 说明还没处理完，再等 15 秒重试。

### 6. 调用 Responses API

```bash
curl -s "$API_URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "'"$MODEL"'",
    "input": [{
      "role": "user",
      "content": [
        {"type": "input_video", "file_id": "'"$FILE_ID"'"},
        {"type": "input_text", "text": "提示词"}
      ]
    }]
  }'
```

**关键**：用 `"file_id"` 字段引用视频，不要用 `"video_url"` 传 file_id（会报 `invalid scheme`）。

### 7. 默认提示词

```
你是一个视频内容分析助手。请按时间线详细梳理视频内容，要求：
1. 标注准确的时间戳 [mm:ss]
2. 提取所有关键信息：讲解的知识点、出现的文字、图表、公式、人物动作、场景变化
3. 生成结构化的内容笔记
请用中文详细回答。
```

用户可指定侧重点（"重点分析代码"、"提取公式"、"总结观点"），融入 prompt。

### 8. 解析响应

响应 `output` 数组包含两类：
- `"type": "reasoning"` — 模型思考过程（忽略）
- `"type": "message"` — 最终结果，取 `content[].text`

```python
for item in result["output"]:
    if item["type"] == "message":
        for c in item["content"]:
            if c["type"] == "output_text":
                print(c["text"])
```

### 9. 清理

```bash
rm -f /tmp/video-analyzer-*
```

### 10. 输出格式

拿到原始分析后，根据用户意图决定输出详细程度：
- 用户说"分析视频"、"视频笔记" → 直接输出完整笔记
- 用户说"简单描述"、"讲了什么" → 用自己的话精简概括，不贴原文

## 踩坑记录

| 问题 | 原因 | 解决 |
|------|------|------|
| `invalid scheme` | 用 `video_url` 传了 file_id | 改用 `file_id` 字段 |
| `OperationDenied.InvalidState` | 文件还在 processing | 多等一会儿再调用 |
| 429 RequestBurstTooFast | base64 直传请求体太大触发突发保护 | 改用 Files API 上传，不要用 base64 |
| `input_file` 报 not pdf | `input_file` 类型只支持 PDF | 视频用 `input_video` + `file_id` |
| yt-dlp 下载 480p | B站高清需登录 | 加 `--cookies-from-browser chrome` |
