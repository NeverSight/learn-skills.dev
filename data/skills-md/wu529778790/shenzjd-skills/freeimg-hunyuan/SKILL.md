---
name: freeimg-hunyuan
description: "Generate AI images (text-to-image and image-to-image with reference) via Tencent Hunyuan 3.0 — completely FREE: claim the WeChat 小程序成长计划 incentive resource pack (10万张 free AI images + 10亿 Token, 6-month validity) and the quota burns on your own CloudBase env, no payment ever. One-time setup stores Tencent Cloud credentials locally (full illustrated tutorial on the companion web app https://freeimg.shenzjd.com/hunyuan); then generate images (upstream returns JPEG) in 4 fixed sizes with prompt revise control and optional watermark. Use when the user wants Hunyuan/混元 model, WeChat ecosystem image generation, or image-to-image with a reference image. For free no-setup generation prefer the freeimg-z-image skill (z-image-turbo). Keywords: hunyuan, 混元, 混元生图, 腾讯云, CloudBase, 云开发, text-to-image, image-to-image, 垫图, 图生图, 文生图, 小程序成长计划, 激励任务, 免费, 免费生图, 10万张, freeimg-hunyuan."
---

# FreeImg Hunyuan — 腾讯混元生图（免费 10 万张额度）

调用腾讯云混元 3.0 生图模型（走 CloudBase AI 网关），支持**文生图**与**垫图
（图生图）**。**完全免费，不花一分钱**：额度来自微信「小程序成长计划」激励
资源包——**10 万张 AI 生图 + 10 亿 Token**，全行业开发者免费领取，6 个月有效，
额度烧在你自己云开发环境的资源包上。

**可视化网页版 + 图文教程**：[freeimg.shenzjd.com/hunyuan](https://freeimg.shenzjd.com/hunyuan) ——
网页里有**从领取资源包、创建密钥到出图的完整备注教程**（Step 0 卡片式引导），
不想配本地环境时在网页上填密钥即用，两者共用同一套腾讯云凭据。

## When to Use

- User 明确要混元 / Hunyuan / 腾讯云出图，或需要**垫图**（参考图改图）
- User 走微信小程序生态、想用「小程序成长计划」激励资源包的**10 万张免费生图额度**
- User 已配置过腾讯云密钥并要求继续用混元

**When NOT to Use:**
- User 只想免费快速出图、零配置 → 用 `freeimg-z-image` skill（z-image-turbo，免注册免领取）
- User 不愿花几分钟领取免费资源包（虽然不领也不产生费用，但没有资源包时按量计费）

## Core Pattern

### Step 0: 首次使用 — 免费领取资源包并配置凭据

额度领取（**免费，全行业开发者可领**；网页版有同款图文教程卡片）：

1. **领激励资源包**：微信公众平台「行业能力 → 小程序成长计划」领取资源包
   （**10 万张 AI 生图 + 10 亿 Token，6 个月有效**），点「去使用」创建一个
   云开发环境，记下**环境 ID**——资源包就绑定在这个环境上
2. **建密钥**：腾讯云控制台
   [访问管理 → API 密钥管理](https://console.cloud.tencent.com/cam/capi)
   「新建密钥」，复制 SecretId 与 SecretKey
3. **写配置**（只需一次，**不要把密钥写进仓库、日志或对话输出**）：

   ```bash
   mkdir -p ~/.freeimg-hunyuan && printf "TCB_ENV_ID=你的环境ID\nTCB_SECRET_ID=你的SecretId\nTCB_SECRET_KEY=你的SecretKey\n" > ~/.freeimg-hunyuan/config.env && chmod 600 ~/.freeimg-hunyuan/config.env
   ```

脚本按以下优先级读取凭据：环境变量 `TCB_ENV_ID` / `TCB_SECRET_ID` /
`TCB_SECRET_KEY` → 配置文件 `~/.freeimg-hunyuan/config.env`。都没有时打印上述引导退出。

依赖说明：脚本用官方 `@cloudbase/node-sdk`（网关鉴权是自定义签名，不自行复刻），
首次运行自动装到 `~/.freeimg-hunyuan/sdk`（需本机有 node + npm，十几秒），之后复用。

### Step 1: 生成图片

```bash
# 文生图
scripts/generate.mjs --prompt "提示词" --out 输出.jpg [--size 1024x1024] [--no-revise] [--footnote "品牌名"]
# 垫图（图生图）：--image 接图片路径、base64 或 data URL
scripts/generate.mjs --prompt "提示词" --image 垫图.jpg --out 输出.jpg
```

- `--size`：只支持 `1024x1024` / `1280x720` / `720x1280` / `2048x512`
  （上游限制：宽高 [512,2048] 且面积 ≤ 1024x1024）
- `--no-revise`：关闭模型自动润色提示词（默认开启）
- `--footnote`：右下角水印文字 ≤16 字符；默认单个空格=无水印
  （去水印的合规责任在使用方）
- 提示词上限 4000 字，中文即可
- 429/5xx 已内置 2 秒重试一次；仍失败按错误提示处理

### Step 2: 交付

- 生成后**先查看图片**（Read 工具）确认质量再交给用户；不满意换提示词重生成
- 返回的图片 URL 是签名地址会过期，脚本已立即下载落盘，只交付本地文件
- 垫图模式提示词写「保持构图，把 ×× 换成 ××」这类改图指令效果更好

## Quick Reference

| 需求 | 参数 | 用途 |
| ---- | ---- | ---- |
| 1:1 方图 | `--size 1024x1024` | 头像、图标、知识卡片 |
| 16:9 横图 | `--size 1280x720` | PPT 配图、banner |
| 9:16 竖图 | `--size 720x1280` | 手机海报、小红书 |
| 4:1 超宽 | `--size 2048x512` | 公众号头图、横幅 |

环境变量：`TCB_ENV_ID`、`TCB_SECRET_ID`、`TCB_SECRET_KEY`（凭据）、
`FREEIMG_HUNYUAN_CONFIG`（自定义配置文件路径）、`FREEIMG_HUNYUAN_SDK_DIR`（自定义 SDK 安装目录）。

## Common Mistakes

- **把密钥提交进仓库或贴进对话**：SecretId/SecretKey 等同账号权限，只放
  `~/.freeimg-hunyuan/config.env`（`chmod 600`）或环境变量
- **用不支持的尺寸**：如 1536x2048 会被拒绝，只能四选一（见 Quick Reference）
- **422 还在重试**：422 是提示词触发内容审核，同样内容重发必然再失败，改措辞
- **没有资源包直接生成**：会按量计费产生费用；引导用户先免费领取「小程序成长计划」激励资源包（10 万张生图额度）并绑定所用环境
- **环境 ID 填错**：资源包绑定在领取时创建的那个环境，凭据对应的环境必须有资源包
- **以为输出是 PNG**：混元上游下发的是 **JPEG**，脚本按原样落盘，扩展名由 `--out` 决定——
  用 `.png` 会得到「名字是 png、内容是 jpeg」的文件，交付前缀名一律写 `.jpg`
- **生成后不检查就交付**：先 Read 查看再给用户
