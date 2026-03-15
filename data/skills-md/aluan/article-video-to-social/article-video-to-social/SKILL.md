---
name: article-video-to-social
description: Convert Bilibili videos or WeChat articles into social media content. Transcribe videos, extract article text, summarize and rewrite in platform-specific style, then publish via social-push-skill. Use when user asks to convert B站视频/公众号文章 to social media posts.
license: MIT
metadata:
  author: aluan
  version: 1.0.3
  requires:
    - yt-dlp
    - ffmpeg
    - faster-whisper
    - pandoc
    - social-push-skill
---

# 文章视频转社交媒体

## Overview
将 B 站视频或微信公众号文章转为文字 → 总结提炼 → 按目标平台风格重写 → 通过 social-push-skill 发布到社交媒体。

## Progress Feedback（进度反馈规则）

每个步骤完成后，必须立即向用户输出对应的进度反馈，格式如下：

| 步骤完成事件 | 反馈消息 |
|---|---|
| 公众号文章获取完毕 | `✅ 公众号文章获取成功` |
| B站视频转写完毕 | `✅ 视频内容转写成功` |
| 洗稿重写完毕 | `✅ 洗稿成功` |
| 发布到微博完毕 | `✅ 发布到微博成功` |
| 发布到小红书完毕 | `✅ 发布到小红书成功` |
| 发布到微信公众号完毕 | `✅ 发布到微信公众号成功` |

若步骤失败，输出 `❌ <步骤名> 失败：<简短原因>`，然后尝试降级方案或提示用户。

---

## Workflow (follow in order)

0. **Pre-flight：清理残留进程**（每次 workflow 开始前必做）
   ```bash
   agent-browser close 2>/dev/null || true
   ```
   此步骤确保上一次 agent-browser 进程已退出，避免出现 `Target page ... closed` 或 `--profile ignored` 报错。
   静默执行，无需向用户反馈。

1. **获取原始内容**
   - **B站视频**：
     - 先告知用户：`⏳ 正在获取视频内容，若无字幕将启动 Whisper 转写，预计 3-10 分钟，请稍候...`
      执行本 skill 目录下的 `scripts/transcribe_bili_tiny.py`（脚本与本 SKILL.md 在同一目录，执行前确认其绝对路径）：
     ```bash
     python3 <本SKILL.md所在目录>/scripts/transcribe_bili_tiny.py <BV_ID或URL> /tmp/transcript.txt
     ```
     脚本会优先尝试下载B站字幕（含自动生成字幕），获取不到字幕时自动回退到 faster-whisper 语音转写。
     **脚本执行过程中会输出详细进度信息，包括：**
     - 字幕下载尝试状态
     - 音频下载进度
     - Whisper 模型加载状态
     - 转录进度百分比（每处理 10 个片段更新一次）

     **你必须将脚本输出的所有进度信息实时转发给用户**，让用户了解当前处理状态。

     转写完成后，打开文件检查并修正明显识别错误。
     **完成后输出**：`✅ 视频内容转写成功`

   - **微信公众号文章**：
     - 有链接：
       1. 先告知用户：`⏳ 正在打开页面，请稍候...`
       2. 打开并等待加载：
          ```bash
          agent-browser open <URL>
          agent-browser wait --load networkidle
          ```
       3. 获取标题和正文（用 `#js_content` 定位微信正文容器，避免抓到全页 UI 噪音）：
          ```bash
          agent-browser get title
          agent-browser snapshot -s "#js_content" > /tmp/article.txt
          ```
       4. 若 `#js_content` 为空（少数模板不同），降级用：
          ```bash
          agent-browser snapshot -s ".rich_media_content" > /tmp/article.txt
          ```
       5. 若仍不完整，提示用户复制粘贴
     - 无链接：让用户直接粘贴全文或关键段落
     - 清理广告、版权声明、二维码等非正文内容（snapshot 输出的是 a11y 文本树，图片会显示为 `img "图片"`，可忽略）
     - **完成后输出**：`✅ 公众号文章获取成功`

2. **内容处理**
   - **洗稿重写**：参考 `assets/rewrite_prompt.md` 进行专业的内容重写
   - **格式优化**：根据目标平台调整展示格式
   - **完成后输出**：`✅ 洗稿成功`

3. **发布到社交平台**
   - 使用 [social-push-skill](https://github.com/aluan/social-push-skill) 发布
   - 支持平台：小红书、微博、微信公众号等（根据 social-push-skill 配置）
   - 发布前向用户确认内容
   - 用户确认后，如果用户没有指定发布平台，默认就发布到支持的所有平台(小红书、微博、微信公众号等)，如果用户指定了发布平台，就只发布到指定的平台。

   **发布流程**（按顺序执行）：
   - **内容渲染和复制**：
     - 将 markdown 转换为适合社交媒体的纯文本格式并复制到剪切板：
       ```bash
       # 使用 pandoc 转换为纯文本（保留段落结构）
       pandoc -f markdown -t plain --wrap=none /path/to/content.md | pbcopy
       ```
     - 输出提示：`✅ 内容已复制到剪切板`
   - **发布到平台**：
     - 调用 social-push-skill 发布到目标平台
     - 发布后根据平台返回结果输出对应反馈：
       - 成功：`✅ 发布到<平台>成功`
       - 失败：`❌ 发布到<平台>失败：<简短原因>`

## Rules
- 避免大段原文照搬，必须重组与提炼
- 尊重各平台内容规范，避免敏感词和违规内容
- 出现违禁词语时的处理方式：直接停止发布，同时提示用户内容可能违规。
- 保留原文核心观点，深度挖掘投资价值

## References
- 详细流程：`references/workflow.md`
- 发布工具：[social-push-skill](https://github.com/aluan/social-push-skill)

## Resources
- `scripts/transcribe_bili_tiny.py`（与本 SKILL.md 同目录）：使用 faster-whisper medium 转写 B 站视频
- `assets/rewrite_prompt.md`：专业的洗稿重写提示词
- `references/workflow.md`：详细工作流程说明
