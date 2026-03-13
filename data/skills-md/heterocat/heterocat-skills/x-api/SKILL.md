---
name: x-api
description: "使用 X (Twitter) API v2 获取和发布推文、媒体、用户信息等数据。用于：获取指定用户的最新推文、搜索推文、获取用户信息、发布纯文本/带图片/带视频的推文。获取操作需要 X_BEARER_TOKEN，发布操作需要 OAuth 1.0a 四件套：X_API_KEY、X_API_SECRET、X_ACCESS_TOKEN、X_ACCESS_TOKEN_SECRET。当用户需要获取或发布 Twitter/X 上的推文、上传媒体文件（图片/视频）时触发。"
---

# X (Twitter) API

使用 X API v2 获取和发布推文、媒体、用户信息。

## 前置要求

### 只读操作（获取推文、搜索、用户信息）
```bash
export X_BEARER_TOKEN="你的 Bearer Token"
```

### 发布推文（OAuth 1.0a）
```bash
export X_API_KEY="你的 Consumer Key"
export X_API_SECRET="你的 Consumer Secret"
export X_ACCESS_TOKEN="你的 Access Token"
export X_ACCESS_TOKEN_SECRET="你的 Access Token Secret"
```

## 可用功能

### 1. 获取用户最新推文

使用 `get_user_tweets.py` 脚本获取指定用户的最新推文。

**用法**:
```bash
python scripts/get_user_tweets.py <username> [max_results]
```

**参数**:
- `username` (string): 用户名（不含 @）
- `max_results` (number, 可选): 返回推文数量，默认 5，最大 100

**示例**:
```bash
python scripts/get_user_tweets.py cheerselflin 5
```

**输出格式** (2026-02-28优化):
```
# 1. 2026-02-27 20:33

> I'll stick to being a dog mom thanks 🐶 https://t.co/sPRYAnTGwO

视频: https://video.twimg.com/amplify_video/.../xxx.mp4
预览图: https://pbs.twimg.com/amplify_video_thumb/.../xxx.jpg

❤️793 🔄13 💬39 🔁1
```

格式说明：
- 标题：`# 序号. YYYY-MM-DD HH:MM`
- 推文内容：`> 引用块` 展示原文
- 媒体：`图片: https://...` / `视频: https://...` / `预览图: https://...`
- 统计：`❤️likes 🔄RTs 💬回复 🔁quotes`
- 无 Markdown 图像语法 `![alt](url)`（飞书/飞书文档不渲染）
- 无代码块

### 2. 搜索推文

使用 `search_tweets.py` 脚本搜索公开推文。

**用法**:
```bash
python scripts/search_tweets.py "<query>" [max_results]
```

**参数**:
- `query` (string): 搜索查询（支持 X 搜索语法，如 "from:username"、"#hashtag"）
- `max_results` (number, 可选): 返回推文数量，默认 10，最大 100

**示例**:
```bash
python scripts/search_tweets.py "from:cheerselflin" 5
```

### 3. 获取用户信息

使用 `get_user_info.py` 脚本获取用户详细信息。

**用法**:
```bash
python scripts/get_user_info.py <username>
```

**示例**:
```bash
python scripts/get_user_info.py cheerselflin
```

### 4. 发布推文

使用 `post_tweet.py` 脚本发布推文。

**用法**:
```bash
python scripts/post_tweet.py "推文内容"
```

**参数**:
- `text` (string): 推文内容，最多 280 字符

**环境变量要求**:
发布推文需要 OAuth 1.0a 认证（用户上下文）：
- `X_API_KEY` - API Key (Consumer Key)
- `X_API_SECRET` - API Secret (Consumer Secret)
- `X_ACCESS_TOKEN` - Access Token
- `X_ACCESS_TOKEN_SECRET` - Access Token Secret

**如何获取 OAuth 凭证**:
1. 前往 [X Developer Portal](https://developer.x.com/en/portal/dashboard)
2. 进入你的项目/应用 → "Keys and Tokens"
3. 生成 "Access Token and Secret"（需要有 Write 权限）
4. 如果应用权限变更过，需要重新生成 Access Token

**示例**:
```bash
# 发布纯文本推文
python scripts/post_tweet.py "Hello, X!"

# 发布带图片的推文
python scripts/post_tweet.py "Check out this photo!" --media ./photo.jpg

# 发布带多张图片的推文（最多4张）
python scripts/post_tweet.py "Multiple images" -m ./img1.jpg -m ./img2.jpg -m ./img3.jpg

# 使用已上传的 media_id
python scripts/post_tweet.py "Using media id" --media-id 1234567890
```

### 5. 上传媒体文件

使用 `upload_media.py` 脚本上传图片或视频（供后续发推文使用）。

**用法**:
```bash
python scripts/upload_media.py <文件路径>
```

**支持的格式**: JPG, PNG, GIF, WEBP, MP4, MOV

**示例**:
```bash
python scripts/upload_media.py ./my-image.png
```

**返回**: Media ID，可用于 `post_tweet.py --media-id`

## 技能组合 Workflow

### 生成视频并发布到 X

结合 `generate-video` skill 和 `x-api` skill：

```bash
# 1. 生成视频（使用豆包视频生成）
cd .claude/skills/generate-video/scripts
python text_to_video.py "可爱猫咪在阳光下打盹" -t 5 -r 1:1

# 2. 上传视频到 X
cd .claude/skills/x-api/scripts
python upload_media.py /path/to/video.mp4

# 3. 获取 Media ID 后发布推文
python post_tweet.py "🐱 AI生成的视频" --media-id <MEDIA_ID>
```

## 脚本文件

| 脚本 | 功能 | 认证方式 |
|-----|------|---------|
| `get_user_tweets.py` | 获取用户推文 | Bearer Token |
| `search_tweets.py` | 搜索推文 | Bearer Token |
| `get_user_info.py` | 获取用户信息 | Bearer Token |
| `post_tweet.py` | 发布推文 | OAuth 1.0a |
| `upload_media.py` | 上传媒体文件 | OAuth 1.0a |

## 错误处理

### 只读操作错误
- `401` - 认证失败，检查 Bearer Token
- `403` - 超出请求限制
- `404` - 用户不存在
- `429` - 请求过于频繁，需要等待重置

### 发布推文错误
- `401` - OAuth 认证失败，检查 API Key/Secret 和 Access Token
- `403` - 权限不足，确保应用有 "Read and Write" 权限且 Token 已刷新
- `429` - 请求过于频繁或日推数限制

## 注意事项

1. **请求限制**: X API v2 有速率限制
2. **数据保留**: `search/recent` 仅返回最近 7 天的推文
3. **认证方式**:
   - 只读操作：Bearer Token（应用上下文）
   - 发布推文：OAuth 1.0a（用户上下文）
4. **发布权限**: 发布推文需要应用在 X Developer Portal 中启用 "Read and Write" 权限，且 Access Token 需要重新生成以应用新权限

## 参考文档

- [X API v2 文档](https://docs.x.com/x-api/introduction)
