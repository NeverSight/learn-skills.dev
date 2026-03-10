---
name: wechat-studio
description: 微信公众号内容创作全流程工具，支持 Markdown 主题排版、Dan Koe 风格写作、AI 去痕、图片上传、图文草稿和小绿书发布。Use this skill when the user asks about WeChat Official Account publishing, converting Markdown to WeChat HTML, uploading images to WeChat, creating drafts, writing in Dan Koe style, or removing AI writing traces (humanize). Also trigger when the user mentions 微信排版, 公众号发文, 公众号格式, 文章排版成微信格式, 微信图文, 小绿书, or any WeChat content workflow — even if they don't explicitly say "wechat-studio".
---

# WeChat Studio

微信公众号内容创作全流程工具：Markdown 排版、写作助手、AI 去痕、图片上传、草稿发布。

## 路径解析（重要）

本 skill 的脚本位于 SKILL.md 所在目录下。执行任何脚本之前，**必须**先确定本文件的实际路径，并以此推导脚本目录。

**规则：** 以下文档中所有 `$SKILL_DIR` 占位符应替换为本 SKILL.md 文件所在的目录路径。

例如：如果本文件位于 `/Users/xxx/Desktop/AI/skills/wechat-studio/SKILL.md`，则 `$SKILL_DIR` = `/Users/xxx/Desktop/AI/skills/wechat-studio`。

```bash
SKILL_DIR="<本 SKILL.md 文件所在目录的绝对路径>"
```

---

## 功能一：Markdown → 微信 HTML

`convert.mjs` 直接将 Markdown 渲染为带主题样式的微信公众号 HTML，无需 AI 参与。

```bash
# 输出到文件
node "$SKILL_DIR/scripts/convert.mjs" -i article.md -t autumn-warm -o article.html

# 输出到 stdout
node "$SKILL_DIR/scripts/convert.mjs" -i article.md -t spring-fresh
```

图片会自动替换为 `<!-- IMG:0 -->`、`<!-- IMG:1 -->` 占位符，按 Markdown 中出现顺序编号。

**可用主题:**
| 主题 | 说明 |
|------|------|
| `autumn-warm` | 秋日暖光，橙色调，温暖治愈（默认） |
| `spring-fresh` | 春日清新，绿色调，清爽明快 |
| `ocean-calm` | 海洋静谧，蓝色调，沉稳专业 |
| `custom` | 自定义主题，使用 AI 提示词渲染（`type: ai`） |

---

## 功能二：风格写作（Dan Koe）

**触发条件：** 用户提到"用 Dan Koe 风格写"、"帮我写一篇文章"、"写一篇关于…的文章"

读取 `$SKILL_DIR/references/dan-koe-writing.md` 获取完整写作规范，按其中的结构和语气要求生成文章。更详细的模板和金句库见 `$SKILL_DIR/writers/dan-koe.yaml`。

---

## 功能三：图片上传

### 上传本地图片

```bash
# 单张
node "$SKILL_DIR/scripts/upload-image.mjs" /path/to/image.jpg

# 批量（JSON 文件，内容为路径字符串数组）
node "$SKILL_DIR/scripts/upload-image.mjs" --json images.json

# 批量并将结果写入文件（供 replace-images.mjs / publish.mjs 使用）
node "$SKILL_DIR/scripts/upload-image.mjs" --json images.json --output upload-result.json

# 强制重新上传（跳过缓存）
node "$SKILL_DIR/scripts/upload-image.mjs" --json images.json --no-cache
```

batch JSON 格式（`images.json`）：
```json
["images/photo1.jpg", "images/photo2.png", "images/photo3.webp"]
```

选项：
- `--json <file>`：从 JSON 文件读取路径列表进行批量上传
- `--output <file>`：将批量上传结果写入 JSON 文件（可供后续 replace-images.mjs 使用）
- `--no-cache`：跳过缓存，强制重新上传

单张输出：
```json
{ "success": true, "media_id": "xxx", "wechat_url": "https://mmbiz..." }
```

批量输出（JSON 数组）：
```json
[
  { "file": "img1.jpg", "success": true, "media_id": "xxx", "wechat_url": "https://mmbiz..." },
  { "file": "img2.png", "success": true, "media_id": "yyy", "wechat_url": "https://mmbiz..." }
]
```

### 下载在线图片并上传

```bash
# 单张
node "$SKILL_DIR/scripts/download-upload.mjs" "https://example.com/image.png"

# 批量（JSON 文件，内容为 URL 字符串数组）
node "$SKILL_DIR/scripts/download-upload.mjs" --json urls.json

# 批量并将结果写入文件
node "$SKILL_DIR/scripts/download-upload.mjs" --json urls.json --output upload-result.json

# 强制重新上传
node "$SKILL_DIR/scripts/download-upload.mjs" --json urls.json --no-cache
```

图片会自动压缩（超过 5MB 时）再上传。相同内容的图片会命中本地缓存，跳过重复上传。

缓存文件位于 `~/.config/wechat-studio/upload-cache.json`，以文件 MD5 为 key。

### 替换 HTML 占位符

上传完成后，用 `replace-images.mjs` 将 HTML 中的 `<!-- IMG:N -->` 自动替换为对应的微信图片 `<img>` 标签：

```bash
node "$SKILL_DIR/scripts/replace-images.mjs" \
  --html article.html \
  --result upload-result.json \
  --output article-final.html
```

选项：
- `--html`：输入 HTML 文件路径
- `--result`：上传结果 JSON 文件（由 `--output` 参数生成）
- `--output`：输出 HTML 文件路径（不指定则输出到 stdout）

占位符 `<!-- IMG:0 -->` 对应结果数组第 0 项，`<!-- IMG:1 -->` 对应第 1 项，以此类推。

---

## 功能四：创建图文草稿

**Step 1: 准备草稿 JSON 文件**（`draft.json`）

```json
{
  "articles": [{
    "title": "文章标题",
    "content": "<p>完整 HTML 内容（已替换图片 URL）</p>",
    "thumb_media_id": "封面图的素材 ID",
    "author": "作者名",
    "digest": "文章摘要，最多 120 字",
    "need_open_comment": 0,
    "only_fans_can_comment": 0
  }]
}
```

**Step 2: 创建草稿**

```bash
node "$SKILL_DIR/scripts/create-draft.mjs" draft.json
```

输出：
```json
{ "success": true, "media_id": "草稿的 media_id" }
```

---

## 功能五：创建小绿书（图片帖）

```bash
# 指定本地图片
node "$SKILL_DIR/scripts/create-image-post.mjs" \
  -t "标题" -c "描述文字" --images photo1.jpg,photo2.jpg

# 从 Markdown 文件提取图片
node "$SKILL_DIR/scripts/create-image-post.mjs" \
  -t "标题" -m article.md

# 预览（不实际创建）
node "$SKILL_DIR/scripts/create-image-post.mjs" \
  -t "标题" --images photo1.jpg --dry-run
```

输出：
```json
{ "success": true, "media_id": "xxx", "image_count": 2, "uploaded_ids": ["id1", "id2"] }
```

---

## 功能六：AI 去痕（Humanizer-zh）

**触发条件：** 用户提到"去除 AI 痕迹"、"让文章更自然"、"humanize"

读取 `$SKILL_DIR/references/humanizer-zh.md` 获取完整的 22 种 AI 写作模式和 5 条核心去痕规则，按其中的规范处理文本并输出质量评分。

---

## 功能七：Server Mode（远程代理）

当本地机器无法直连微信 API（如没有固定 IP 白名单）时，可以在远程服务器上部署 `proxy-server.mjs`，本地客户端通过 HTTP 调用远程服务器的 API。

### 服务端部署

```bash
# 在有微信 API 白名单的服务器上启动
node "$SKILL_DIR/scripts/proxy-server.mjs" --port 8080 --secret your-proxy-secret

# 或通过环境变量
PROXY_PORT=8080 PROXY_SECRET=your-proxy-secret node "$SKILL_DIR/scripts/proxy-server.mjs"
```

服务端暴露以下接口（均为 POST，需 `X-Proxy-Secret` 请求头认证）：
- `/api/access-token` — 获取 Access Token
- `/api/upload-material` — 上传图片素材（multipart/form-data）
- `/api/create-draft` — 创建图文草稿（JSON）

### 客户端配置

配置 proxy 后，所有上传/草稿脚本自动走远程服务器，无需修改调用方式。

**环境变量：**
```bash
export WECHAT_PROXY_URL=http://your-server:8080
export WECHAT_PROXY_SECRET=your-proxy-secret
```

**配置文件：**
```yaml
proxy:
  url: http://your-server:8080
  secret: your-proxy-secret
```

---

## 配置

需要微信凭证才能使用上传/草稿功能（convert、写作、去痕无需凭证）。

**方式一：环境变量**

```bash
export WECHAT_APP_ID=your_appid
export WECHAT_SECRET=your_secret
```

**方式二：配置文件**（按优先级从高到低）

```
./wechat-studio.yaml                    # 项目本地（最高优先级）
~/.wechat-studio.yaml                   # 用户目录
~/.config/wechat-studio/config.yaml    # 全局配置
```

```yaml
wechat:
  appid: your_appid
  secret: your_secret

# 图片压缩选项（可选）
compress_images: true       # 是否自动压缩，默认 true
max_image_width: 1920       # 最大宽度（px），默认 1920
max_image_size: 5242880     # 最大文件大小（字节），默认 5MB
http_timeout: 30            # HTTP 超时（秒），默认 30

# 远程代理（可选，见功能七）
proxy:
  url: http://your-server:8080
  secret: your-proxy-secret
```

---

## 典型工作流

### 发布一篇 Markdown 文章

**方式一：一键发布（推荐）**
```bash
# 1. 批量上传文章图片，结果写入 JSON
node "$SKILL_DIR/scripts/upload-image.mjs" --json images.json --output upload-result.json
# 2. 一键：Markdown → 渲染 → 替换图片 → 最终 HTML
node "$SKILL_DIR/scripts/publish.mjs" -i article.md -r upload-result.json -t autumn-warm -o article-final.html
# 3. 上传封面图
node "$SKILL_DIR/scripts/upload-image.mjs" cover.jpg
# 4. 创建草稿（准备 draft.json，填入 article-final.html 内容和封面 media_id）
node "$SKILL_DIR/scripts/create-draft.mjs" draft.json
```

**方式二：分步操作**
```bash
# 1. Markdown → HTML（直接渲染，无需 AI）
node "$SKILL_DIR/scripts/convert.mjs" -i article.md -t autumn-warm -o article.html
# 2. 批量上传文章图片，结果写入 JSON
node "$SKILL_DIR/scripts/upload-image.mjs" --json images.json --output upload-result.json
# 3. 自动替换 HTML 中的占位符
node "$SKILL_DIR/scripts/replace-images.mjs" \
  --html article.html \
  --result upload-result.json \
  --output article-final.html
# 4. 上传封面图
node "$SKILL_DIR/scripts/upload-image.mjs" cover.jpg
# 5. 创建草稿（准备 draft.json，填入 article-final.html 内容和封面 media_id）
node "$SKILL_DIR/scripts/create-draft.mjs" draft.json
```

### 发布小绿书

```bash
node "$SKILL_DIR/scripts/create-image-post.mjs" \
  -t "九月摄影精选" -c "光影记录日常" \
  --images sep01.jpg,sep02.jpg,sep03.jpg
```

---

## File Structure

```
scripts/
  convert.mjs           # Markdown → 微信 HTML（代码渲染，无需 AI）
  upload-image.mjs      # 上传本地图片到微信
  download-upload.mjs   # 下载在线图片并上传
  replace-images.mjs    # 替换 HTML 中的 <!-- IMG:N --> 占位符
  publish.mjs           # 一键：Markdown → 替换图片 → 最终 HTML
  create-draft.mjs      # 创建图文草稿
  create-image-post.mjs # 创建小绿书
  proxy-server.mjs      # 微信 API 远程代理服务器（Server Mode）
lib/
  args.mjs              # CLI 参数解析工具
  config.mjs            # 配置加载（env > YAML > 默认值）
  wechat.mjs            # 微信 API（token、上传、草稿、远程代理）
  image.mjs             # 图片压缩（sharp）
  renderer.mjs          # 基于 marked 的微信 HTML 渲染器
  replace.mjs           # HTML 占位符替换逻辑
  theme.mjs             # 主题 YAML 加载
themes/                 # 主题 YAML 文件
writers/                # 写作风格 YAML 文件
references/             # 参考文档（写作指南、去痕规则）
```
