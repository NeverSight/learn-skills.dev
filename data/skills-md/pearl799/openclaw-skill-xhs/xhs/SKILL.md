---
name: xhs
description: 小红书自动化 — 用 exec 工具运行脚本来登录、发布、爬热点、AI 生成图文。所有操作必须通过 exec 工具执行 uv run 命令，不要用 browser 工具。
homepage: https://github.com/pearl799/xhs-toolkit
metadata:
  {
    "openclaw":
      {
        "emoji": "📕",
        "requires": { "bins": ["uv"], "env": ["XHS_TOOLKIT_DIR", "IMAGE_API_KEY", "IMAGE_BASE_URL", "IMAGE_MODEL"] },
        "primaryEnv": "XHS_TOOLKIT_DIR",
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# 小红书自动化 (XHS)

**重要：所有小红书操作必须使用 exec 工具执行以下命令，不要用 browser 工具打开网页。**

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `XHS_TOOLKIT_DIR` | 是 | xhs-toolkit 项目路径（`git clone https://github.com/pearl799/xhs-toolkit`） |
| `IMAGE_API_KEY` | 是 | 图片生成 API Key（任意 OpenAI 兼容的图片生成服务） |
| `IMAGE_BASE_URL` | 是 | 图片生成 API Base URL（例如 `https://openrouter.ai/api/v1/chat/completions`） |
| `IMAGE_MODEL` | 是 | 图片生成模型名称（例如 `google/gemini-3-pro-image-preview`） |
| `OPENCLAW_GATEWAY_TOKEN` | 否 | OpenClaw Gateway token（文案生成用，如果 gateway 开了 auth） |
| `XHS_DATA_DIR` | 否 | 数据目录，默认 `~/.openclaw/skills/xhs/data` |

## 命令

检查登录状态：

```bash
uv run --project $XHS_TOOLKIT_DIR {baseDir}/scripts/xhs_status.py
```

登录小红书（用户说"登录小红书"/"xhs login"时）：

```bash
uv run --project $XHS_TOOLKIT_DIR {baseDir}/scripts/xhs_auth.py
```

会在 Mac 桌面打开 Chrome，告知用户去扫码。

发布笔记（用户说"发小红书"/"发布笔记"时）：

```bash
uv run --project $XHS_TOOLKIT_DIR {baseDir}/scripts/xhs_publish.py --title "标题" --content "正文" --images "/path/1.png,/path/2.png" --topics "话题1,话题2"
```

发布前先用 xhs_status.py 检查登录。--images 必须是本地文件路径，1-9 张。--dry-run 可验证不发布。

爬取热点（用户说"小红书热点"/"trending"/"今天什么热门"时）：

```bash
uv run --project $XHS_TOOLKIT_DIR {baseDir}/scripts/xhs_trending.py --category "综合" --limit 20
```

支持 --keyword "AI" 搜索。分类：综合/时尚/美食/旅行/美妆/科技/健身/宠物/家居/教育。

AI 生成内容（用户说"生成小红书"/"帮我生成"时）：

```bash
uv run --project $XHS_TOOLKIT_DIR {baseDir}/scripts/xhs_generate_content.py --topic "主题" --style "干货分享" --image-count 4
```

生成文案+配图。生成后发给用户预览，确认后再调 xhs_publish.py 发布。

全自动流水线（用户说"自动发布"/"全自动"时）：

```bash
uv run --project $XHS_TOOLKIT_DIR {baseDir}/scripts/xhs_auto_pipeline.py --mode preview
```

热点→选题→生成→预览/发布。--mode auto 直接发布。

所有脚本输出 JSON，解析 status 字段判断结果。MEDIA: 行表示附件图片。

## 注意事项

- 每个命令只需调用一次，等待结果即可，不要重复执行
- 脚本输出的 JSON 是给你解析用的，转述关键信息给用户即可，不要原样转发
- 生成内容后，把标题、正文、话题发给用户预览，图片用 MEDIA 行的路径作为附件
- 不要在一次回复中发送多条消息，合并为一条
