---
name: feishu-send-file
description: Send files, images, and audio messages via Feishu Lark API using the mandatory two-step process. Use when needing to send files, images, or voice messages to Feishu users or groups. This skill enforces the required workflow - first upload to get file_key, image_key, or audio_key, then send message with the key. Supports file API for documents, image API for pictures, and file API with audio type for voice messages.
---

# 飞书文件/图片发送 Skill

## 快速开始

### 1. 配置文件

**复制示例配置文件：**

```bash
cd ~/.openclaw/workspace/skills/feishu-send-file
cp config.json.example config.json
# 使用你喜欢的编辑器修改 config.json
```

**填入你的配置：**

```json
{
  "app_id": "cli_xxxxxxxxxxxxxxxx",
  "app_secret": "your_app_secret_here",
  "receive_id": "ou_xxxxxxxxxxxxxxxx",
  "message_mode": "send"
}
```

**配置说明：**
| 字段 | 说明 | 示例 |
|------|------|------|
| `app_id` | 飞书应用ID | `cli_xxxxxxxxxxxxxxxx` |
| `app_secret` | 飞书应用密钥 | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `receive_id` | 接收人Open ID | `ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `message_mode` | 消息模式：`send` = 直接发送 | `send` |

**⚠️ 重要**：本脚本**只支持发送模式** (`send`)，不支持回复模式 (`reply`)，避免消息被标记为回复。

**安全提示：**
- `config.json` 已被添加到 `.gitignore`，不会意外提交到 Git
- 建议使用环境变量方式，避免在文件中存储凭证

### 2. 发送消息

```bash
cd ~/.openclaw/workspace/skills/feishu-send-file

# 发送文本
./scripts/send-message.sh text "你好主人！"

# 发送 Markdown 卡片
./scripts/send-message.sh card "**加粗** 和 *斜体*"

# 发送图片
./scripts/send-message.sh image "/path/to/photo.png"

# 发送语音（opus格式）
./scripts/send-message.sh audio "/path/to/voice.opus"

# 发送视频
./scripts/send-message.sh video "/path/to/video.mp4"

# 发送文件
./scripts/send-message.sh file "/path/to/document.pdf"
```

### 3. 环境变量方式（推荐）

使用环境变量临时覆盖配置文件：

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_RECEIVE_ID="ou_xxx"

./scripts/send-message.sh text "消息内容"
```

**优先级：环境变量 > 配置文件**

---

## ⚠️ CRITICAL: OpenClaw 自动回复陷阱

### 问题描述

**OpenClaw 的消息回复机制会自动将响应关联到用户消息，导致变成「回复」而不是「发送」！**

即使你用 `curl` 调用 API，如果最后通过 OpenClaw 的 normal 回复输出，系统仍可能标记为 `has_reply_context: true`。

### 解决方案：使用独立脚本

**必须** 使用提供的独立脚本 `send-message.sh`，它完全绕过 OpenClaw 的回复机制：

```bash
# ✅ 正确：使用独立脚本（绕过 OpenClaw 回复）
./scripts/send-message.sh text "你好主人！"
./scripts/send-message.sh image "/path/to/image.png"
./scripts/send-message.sh audio "/path/to/voice.opus"
```

**不要** 这样做：
```bash
# ❌ 错误：即使 curl 成功，最后通过 OpenClaw 回复输出，仍会变成「回复」
curl -X POST ...
echo "发送成功"  # 这行输出会被 OpenClaw 标记为回复
```

---

## ⚠️ 重要警告

### 1. 发送消息 vs 回复消息

**必须使用「发送消息」API，不要混用「回复消息」API**

| 用途 | API | URL | 说明 |
|------|-----|-----|------|
| **✅ 发送消息** | 发送消息 | `POST /im/v1/messages` | 本技能使用，直接发送消息 |
| **❌ 回复消息** | 回复消息 | `POST /im/v1/messages/:message_id/reply` | **不使用**，用于回复指定消息 |

**正确的发送消息 URL：**
```bash
POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id
```

**错误的回复消息 URL：**
```bash
# 不要用这个！
POST https://open.feishu.cn/open-apis/im/v1/messages/:message_id/reply
```

### 2. 必须使用两步流程

**飞书发送文件/图片必须使用两步流程，一步都不能少！**

❌ 错误方式：直接通过 message API 发送文件路径
✅ 正确方式：先上传获取 `file_key`/`image_key`，再用 key 发送消息

## 三种API的区别

| 类型 | 上传API | 消息类型 | 返回key | 适用场景 |
|------|---------|----------|---------|----------|
| **图片** | `/im/v1/images` | `image` | `image_key` | jpg/png/gif等图片 |
| **文件** | `/im/v1/files` | `file` | `file_key` | 文档、压缩包等 |
| **语音** | `/im/v1/files` | `audio`/`file` | `file_key` | opus/mp3音频 |
| **视频** | `/im/v1/files` | `media` | `file_key` | mp4视频 |
| **表情包** | `/im/v1/images` | `image` | `image_key` | png/gif表情包 |

## 图片发送流程

### 第一步：上传图片获取 image_key

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@/path/to/image.jpg"
```

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "image_key": "img_v3_02ve_xxxx-xxxx-xxxx-xxxx"
  }
}
```

**关键点：**
- `image_type` 必须是 `message`
- `image` 使用 `@` 符号指定本地图片路径
- 保存返回的 `image_key`，下一步要用

### 第二步：发送图片消息

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxxxxx",
    "msg_type": "image",
    "content": "{\"image_key\":\"img_v3_02ve_xxxx-xxxx-xxxx-xxxx\"}"
  }'
```

## 文件发送流程

### 第一步：上传文件获取 file_key

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=stream" \
  -F "file_name=文件名.md" \
  -F "file=@/path/to/file"
```

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "file_key": "file_v3_00ve_xxxx-xxxx-xxxx-xxxx"
  }
}
```

**关键点：**
- `file_type` 必须是 `stream`
- `file_name` 必须包含扩展名
- `file` 使用 `@` 符号指定本地文件路径

### 第二步：发送文件消息

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxxxxx",
    "msg_type": "file",
    "content": "{\"file_key\":\"file_v3_00ve_xxxx-xxxx-xxxx-xxxx\"}"
  }'
```

## 完整参数说明

### 获取 tenant_access_token

所有API调用都需要先获取令牌：

```bash
curl -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "cli_xxxxx",
    "app_secret": "xxxxx"
  }'
```

### receive_id_type 选项

| 类型 | 说明 | 示例 |
|------|------|------|
| `open_id` | 用户的唯一标识（推荐） | `ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `user_id` | 用户ID | `user_xxxxx` |
| `union_id` | 统一ID | `on_xxxxx` |
| `email` | 邮箱 | `user@company.com` |
| `chat_id` | 群聊ID | `oc_xxxxx` |

## 使用脚本自动发送

本skill包含自动化脚本：

### 发送图片
```bash
./scripts/send-image.sh <app_id> <app_secret> <receive_id> <image_path>
```

### 发送文件
```bash
./scripts/send-file.sh <app_id> <app_secret> <receive_id> <file_path>
```

### 发送语音
```bash
./scripts/send-audio.sh <app_id> <app_secret> <receive_id> <audio_path>
```

### 环境变量方式
```bash
export FEISHU_APP_ID="cli_xxxxx"
export FEISHU_APP_SECRET="xxxxx"
./scripts/send-image.sh "" "" "ou_xxxxx" "/path/to/image.jpg"
./scripts/send-file.sh "" "" "ou_xxxxx" "/path/to/file.pdf"
./scripts/send-audio.sh "" "" "ou_xxxxx" "/path/to/voice.opus"
```

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| `field validation failed` | 缺少 `receive_id_type` | URL必须加 `?receive_id_type=open_id` |
| `invalid file_key` | file_key格式错误或已过期 | 重新上传文件获取新key |
| `invalid image_key` | image_key格式错误或已过期 | 重新上传图片获取新key |
| `permission denied` | 应用没有权限 | 检查应用权限设置 |
| `user not found` | receive_id错误 | 确认ID类型和值正确 |

## 快速判断：用图片API还是文件API？

- **图片API** (`/im/v1/images`): jpg, jpeg, png, gif, bmp, webp 等图片格式
- **文件API** (`/im/v1/files`): pdf, doc, docx, xls, xlsx, zip, 等其他所有文件
- **语音API** (`/im/v1/files`): opus, mp3 等音频格式

## 语音消息发送流程

飞书语音消息使用文件上传 API，但有一些特殊要求：

### 音频格式要求

| 格式 | file_type | msg_type | 说明 |
|------|-----------|----------|------|
| `opus` | `opus` | `audio` | 最佳格式，直接播放 |
| `mp3` | `opus` | `file` | 兼容发送，作为文件 |

### 发送语音消息

#### 方式一：使用脚本（推荐）

```bash
# 环境变量方式
export FEISHU_APP_ID="cli_xxxxx"
export FEISHU_APP_SECRET="xxxxx"

# 发送语音
./scripts/send-audio.sh "" "" "ou_xxxxx" "/path/to/voice.opus"
```

#### 方式二：手动 curl

**第一步：上传音频获取 file_key**

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file_name=voice.opus" \
  -F "file=@/path/to/voice.opus"
```

**响应示例：**
```json
{
  "code": 0,
  "data": {
    "file_key": "file_v3_00ve_xxxx-xxxx-xxxx-xxxx"
  }
}
```

**第二步：发送语音消息**

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxxxx",
    "msg_type": "audio",
    "content": "{\"file_key\":\"file_v3_00ve_xxxx-xxxx-xxxx-xxxx\"}"
  }'
```

**关键点：**
- `file_type` 设置为 `opus`（推荐）或 `stream`
- `msg_type` 设置为 `audio` 显示为语音消息，或 `file` 显示为文件
- 音频文件建议为 opus 格式，兼容性最好

### 音频格式转换

如果手头是 mp3 格式，可以使用 ffmpeg 转换：

```bash
# mp3 转 opus
ffmpeg -i input.mp3 -c:a libopus -b:a 32k output.opus

# 或者直接用 mp3 发送（作为文件类型）
# file_type=stream, msg_type=file
```

---

## 视频消息发送流程 ⭐

飞书视频消息使用 `media` 消息类型，支持 mp4 格式。

### 视频格式要求

| 参数 | 要求 |
|------|------|
| 格式 | mp4 |
| 大小 | 最大 500MB |
| 上传 API | `/im/v1/files` |
| file_type | `mp4` |

### 发送视频

#### 使用脚本

```bash
export FEISHU_APP_ID="cli_xxxxx"
export FEISHU_APP_SECRET="xxxxx"

# 发送视频（可选封面图）
./scripts/send-video.sh "" "" "ou_xxxxx" "/path/to/video.mp4" "/path/to/thumb.jpg"
```

#### 手动 curl

**第一步：上传视频**

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=mp4" \
  -F "file=@/path/to/video.mp4"
```

**第二步：发送视频**

```bash
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxxxx",
    "msg_type": "media",
    "content": "{\"file_key\":\"file_v3_00ve_xxxx\",\"image_key\":\"img_v3_02ve_xxxx\"}"
  }'
```

**注意**：视频消息可包含封面图 `image_key`（可选）

---

## 表情包发送流程 ⭐

飞书表情包本质上是图片消息，但可以显示为可收藏的表情样式。

### 表情包类型

| 类型 | 说明 | 方法 |
|------|------|------|
| Emoji 字符 | 😸🎉🐱 等 | 直接发送文本消息 |
| 图片表情 | png/gif 图片 | 发送图片消息 |

### 发送表情包

#### 方式一：Emoji 字符（最简单）

```bash
# 发送包含 emoji 的文本
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxxxx",
    "msg_type": "text",
    "content": "{\"text\":\"😸🎉🐱👍\"}"
  }'
```

#### 方式二：使用脚本发送图片表情

```bash
export FEISHU_APP_ID="cli_xxxxx"
export FEISHU_APP_SECRET="xxxxx"

# 发送图片作为表情包
./scripts/send-sticker.sh "" "" "ou_xxxxx" "/path/to/sticker.png"
```

#### 方式三：手动 curl 发送图片表情

```bash
# 上传表情图片
curl -X POST "https://open.feishu.cn/open-apis/im/v1/images" \
  -H "Authorization: Bearer $TOKEN" \
  -F "image_type=message" \
  -F "image=@/path/to/sticker.png"

# 发送图片（显示为表情样式）
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_xxxxx",
    "msg_type": "image",
    "content": "{\"image_key\":\"img_v3_02ve_xxxx\"}"
  }'
```

---

## 检查清单

发送前确认：

- [ ] 已获取 `tenant_access_token`
- [ ] 已判断使用图片API还是文件API
- [ ] 已上传并获取 `image_key` 或 `file_key`
- [ ] URL包含 `?receive_id_type=xxx`
- [ ] `msg_type` 设置正确（image/file/audio/media）
- [ ] `content` 包含正确的 key
- [ ] `receive_id` 与 `receive_id_type` 匹配

### 各类型消息检查表

| 消息类型 | file_type | msg_type | 需要 Key |
|----------|-----------|----------|----------|
| 图片 | - | `image` | `image_key` |
| 文件 | `stream` | `file` | `file_key` |
| 语音 | `opus` | `audio` | `file_key` |
| 视频 | `mp4` | `media` | `file_key` (+ 可选 `image_key`) |
| 表情包 | - | `image` | `image_key` |

## 参考文档

- 上传图片API: https://open.feishu.cn/document/server-docs/im-v1/image/create
- 上传文件API: https://open.feishu.cn/document/server-docs/im-v1/file/create
- 发送消息API: https://open.feishu.cn/document/server-docs/im-v1/message/create
- 完整消息类型指南: `MESSAGE_TYPES.md`
