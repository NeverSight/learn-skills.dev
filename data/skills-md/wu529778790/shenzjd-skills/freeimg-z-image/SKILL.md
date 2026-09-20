---
name: freeimg-z-image
description: "Generate AI images from text prompts via the free z-image-turbo model (Gitee AI serverless API, ~100 free 2K images/day with a free token). One-time setup stores the token locally; then generate PNG images in any size (multiple of 8), with negative prompts and step control. Companion web app with 18000+ prompt library and 12 preset styles: https://freeimg.shenzjd.com. Use for generating, drawing, or creating images (icons, covers, illustrations, posters). Keywords: image generation, text-to-image, AI image, z-image, z-image-turbo, Gitee AI, free image, 画图, 生成图片, 文生图, AI 绘画, 免费图片生成, freeimg-z-image."
---

# FreeImg Z-Image — 免费 AI 图片生成

把一句话提示词变成 2K 高清图片：底层调用 Gitee AI Serverless API 的
`z-image-turbo` 模型（8 步极速生成），每天约 100 张免费额度，只需一个
免费令牌。不依赖任何付费服务。

**可视化网页版**：[freeimg.shenzjd.com](https://freeimg.shenzjd.com) ——
不想写提示词时直接用网页版：内置 **18000+ 精选提示词库**、**12 种预设
风格**（公众号封面 / 小红书封面 / 知识卡片 / 海报 / 3D 卡通 / 中国风等）、
7 种尺寸比例、历史记录与图床上传。Skill 负责让 AI 在对话里直接出图，
网页版负责人工精修与逛提示词库，两者共用同一款令牌。

## When to Use

- User asks to generate / draw / create an image (icon, cover, illustration, poster, avatar)
- User mentions 文生图 / 画图 / 生成图片 / AI 绘画 / 生成头像 / 生成封面
- User wants quick AI images without paid API keys (z-image-turbo is free)

**When NOT to Use:**
- User wants to *edit* an existing image (this skill is text-to-image only) — for 垫图/图生图 use the `freeimg-hunyuan` skill
- User explicitly needs the Hunyuan/混元 model or the WeChat 小程序成长计划 free quota — use the `freeimg-hunyuan` skill
- User explicitly needs another model (DALL·E, Midjourney, Flux…) — use the corresponding skill/API
- No network access or Gitee AI is unreachable

## Core Pattern

### Step 0: 首次使用 — 配置免费令牌

令牌获取（免费，三步，详见 [freeimg.shenzjd.com](https://freeimg.shenzjd.com) 页面教程）：
登录 [ai.gitee.com/serverless-api](https://ai.gitee.com/serverless-api) →
任意模型详情页点「在线体验」→「API」→「添加令牌」→ 复制。

脚本按以下优先级读取令牌（**不要把令牌写进仓库、日志或对话输出**）：

1. 环境变量 `GITEE_AI_API_KEY`
2. 本地配置文件 `~/.freeimg-z-image/config.env`（内容一行：`GITEE_AI_API_KEY=xxxx`）

都没有时脚本会打印上面的获取引导并退出；AI 应引导用户完成 Step 0，
把令牌写入 `~/.freeimg-z-image/config.env`（`chmod 600`），只需一次。

### Step 1: 生成图片

```bash
scripts/generate.mjs --prompt "提示词" --out 输出.png \
  [--width 1024] [--height 1024] [--steps 8] [--negative "负向提示词"]
```

- `--width/--height`：必须为 **8 的倍数**；常用组合见 Quick Reference
- `--steps`：默认 8（turbo 模型推荐值，越高越慢）
- `--negative`：不传时默认 `文字,字母,水印,签名,模糊`
- 接口偶发 502，脚本已内置 2 次退避重试；仍失败则换时间再试

### Step 2: 交付

- 生成后**先查看图片**（Read 工具）确认质量，再交给用户；不满意就换提示词重新生成，不要把废图丢给用户
- 需要小尺寸（如 App 头像 144×144）时用 `sips -Z 144 原图 --out 小图.png`（macOS）或 ImageMagick `convert -resize` 缩放
- 提示词用中文即可，模型中文理解良好；结构：`风格 + 主体 + 细节 + 构图 + 无文字无水印`

## Quick Reference

| 需求 | 参数 | 用途 |
| ---- | ---- | ---- |
| 1:1 方图 | `--width 1024 --height 1024`（高清用 2048×2048） | 头像、图标、知识卡片 |
| 4:3 横图 | `--width 2048 --height 1536` | 公众号封面（900×383 可后期裁） |
| 3:4 竖图 | `--width 1536 --height 2048` | 小红书封面 |
| 16:9 宽图 | `--width 2048 --height 1152` | PPT 配图、banner |

提示词模板：

```
{风格，如 扁平卡通插画/3D 渲染/水彩}：{主体与细节}，{构图，如 居中特写、四周留裁剪余量}，{用途，如 App 图标、缩小时仍清晰}，无文字，无水印
```

环境变量：`GITEE_AI_API_KEY`（令牌）、`FREEIMG_Z_IMAGE_CONFIG`（自定义配置文件路径）。

## Common Mistakes

- **把令牌提交进仓库**：令牌等同免费额度账号，只放 `~/.freeimg-z-image/config.env` 或环境变量；`.env` 文件一律 `.gitignore`
- **尺寸不是 8 的倍数**：如 1000×1000 会被接口拒绝或静默取整，用 1024/1536/2048
- **图里带乱码文字**：z-image 对文字渲染不稳定，需要文字时后期用设计工具加，提示词里声明「无文字」
- **生成后不检查就交付**：模型偶尔产出畸形手部/构图偏移，必须先 Read 查看再给用户
- **额度耗尽还在重试**：单日约 100 张免费额度，报 429/403 时提示用户明天再试或换令牌
