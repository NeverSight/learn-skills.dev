---
name: zhy-wechat-publish
description: Use when publishing HTML articles to WeChat Official Account drafts, especially when you need cover upload, automatic cover generation, body image rewriting, CSS-variable compatibility, or draft metadata like author and comment settings.
argument-hint: [html-file-path]
---

# 微信公众号草稿箱发布技能

本技能用于将文章发布到微信公众号草稿箱。脚本仅依赖 Node.js 内置模块；自动封面生成步骤会复用现有 `bun` 生图脚本。

## 前置条件

1. `Node.js >= 16`
2. 若要自动生成封面，还需本机可用 `bun`
3. 技能目录下 `.env` 至少包含：

```env
WECHAT_APP_ID=你的公众号AppID
WECHAT_APP_SECRET=你的公众号AppSecret
WECHAT_DEFAULT_THUMB_MEDIA_ID=默认封面图media_id（可选）
WECHAT_DEFAULT_AUTHOR=AI源来如此（可选）
```

4. 运行机器公网 IP 已加入公众号后台 IP 白名单
5. 自动生成封面时，需保证 `zhy-article-illustrator` 的生图环境可用

## 安装说明

本 skill 适合与 `npx skills add ... --skill zhy-wechat-publish` 一起安装到 OpenCode、Claude Code 等支持 `SKILL.md` 的 agent 工具中。

安装后请在本地 skill 目录手动创建 `.env`，不要将真实凭据提交回仓库。

## 脚本清单

脚本位于 `scripts/`：

| 脚本 | 用途 |
|---|---|
| `wechat_draft.js` | 上传正文到公众号草稿箱 |
| `upload_image.js` | 上传本地封面图到永久素材库，获取 `media_id` |
| `publish_with_cover.js` | 读取文章、生成封面、上传封面并推送草稿 |

## 核心能力

- 自动处理正文 CSS 变量兼容
- 自动将正文图片上传到微信正文图片接口并替换 URL
- 自动将 `ul/ol` 降级为微信公众号编辑态更稳定的段落列表
- 支持默认作者、评论开关、仅粉丝评论设置
- 支持从文章内容生成单张公众号封面，并自动上传为 `thumb_media_id`

## 工作流

### 方式一：已准备好 HTML 与封面 media_id

```bash
node scripts/wechat_draft.js --title "文章标题" --file "post.html" --author "AI源来如此" --thumb "MEDIA_ID" --need-open-comment "1" --only-fans-can-comment "1"
```

参数说明：

| 参数 | 必填 | 说明 |
|---|---|---|
| `--title` | 是 | 文章标题 |
| `--file` | 是 | HTML 正文文件路径 |
| `--author` | 否 | 作者，不传时默认 `WECHAT_DEFAULT_AUTHOR` 或 `AI源来如此` |
| `--digest` | 否 | 摘要 |
| `--thumb` | 否 | 封面 `media_id`，不传时读取 `.env` 默认值 |
| `--source-url` | 否 | 原文链接 |
| `--need-open-comment` | 否 | 是否开启评论，默认 `1` |
| `--only-fans-can-comment` | 否 | 是否仅粉丝可评论，默认 `1` |

### 方式二：自动生成封面并发布

当你已有文章源文件，以及最终用于上传的 HTML 文件时，可直接运行：

```bash
node scripts/publish_with_cover.js --article "article.md" --html "post.html" --author "AI源来如此" --source-url "https://example.com"
```

该脚本会自动完成：

1. 读取文章内容并提取标题/摘要
2. 调用 `zhy-article-illustrator/scripts/image-gen.ts` 生成单张 16:9 封面图
3. 调用 `upload_image.js --json` 上传封面，获得 `thumb_media_id`
4. 调用 `wechat_draft.js` 推送草稿，并自动带上：
   - `author`
   - `thumb_media_id`
   - `need_open_comment=1`
   - `only_fans_can_comment=1`

可选参数：

| 参数 | 说明 |
|---|---|
| `--article` | 原始文章文件，推荐 Markdown，也可 HTML |
| `--html` | 最终上传到公众号的 HTML 文件 |
| `--title` | 显式覆盖标题 |
| `--author` | 显式覆盖作者 |
| `--cover-output` | 自定义封面输出路径 |
| `--cover-ar` | 封面宽高比，默认 `16:9` |
| `--source-url` | 原文链接 |
| `--need-open-comment` | 是否开启评论，默认 `1` |
| `--only-fans-can-comment` | 是否仅粉丝可评论，默认 `1` |

## 正文兼容说明

发布前，`wechat_draft.js` 会自动处理：

1. `var(--xxx)` CSS 变量展开
2. 微信 section 背景样式兼容
3. 首个 `h1` 去除，避免与标题重复
4. 正文图片上传到 `cgi-bin/media/uploadimg`
5. 原生列表转换为普通段落列表

## 错误排查

- `[40013] invalid appid`：检查 `.env` 中 `WECHAT_APP_ID`
- `[40164] invalid ip... not in whitelist`：将报错 IP 加入微信后台白名单
- `[40007] invalid media_id`：封面素材无效，重新上传封面图
- `缺少 Xiaomi/Gemini/OpenAI API Key`：自动封面生成所需生图配置缺失
- 正文图片不显示：检查原图路径/URL 是否可访问，以及 `media/uploadimg` 是否成功

## 快速示例

```bash
# 已有 HTML，直接发草稿
node scripts/wechat_draft.js --title "技术周报" --file "post.html"

# 自动生封面并发布
node scripts/publish_with_cover.js --article "article.md" --html "post.html"

# 上传封面图并把 media_id 回写 .env
node scripts/upload_image.js "cover.png" --write-env --json
```
