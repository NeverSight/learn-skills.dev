---
name: bilibili-subtitle-downloader
description: 下载 Bilibili 视频字幕，将其进行分块以供 LLM（大语言模型）处理，并生成高质量的总结。当用户提供 Bilibili BV 号或 URL，并希望获取视频内容的总结、核心要点或详细的分解时使用。
---

# Bilibili 字幕下载器技能

此技能通过使用专用的 Python 脚本和子智能体 (sub-agent) 编排，自动化提取和总结 Bilibili 视频字幕的流程。

## 工作流程

1.  **提取字幕**: 运行自带的脚本来下载并分块字幕。普通视频，均为 BV 号开头
    ```bash
    python3 skills/bilibili-subtitle-downloader/scripts/download_and_chunk.py <BV_ID>
    ```
    * **登录检查**: 如果脚本输出 `QR_CODE_READY:<PATH>`，它将等待用户扫描二维码。您应该将此图像发送给用户。
    * **保存 Cookie**: 成功登录后，脚本会自动将 Cookie 保存到 `~/.openclaw/workspace/bilibili_cookie.txt`。

2.  **处理输出**: 解析脚本输出的 `RESULT_JSON`，以获取分块文件列表。分块文件命名格式：
    * 普通视频 (BV号): `bili_temp/<BV_ID>/<BV_ID>_chunk_0.txt`
    * 课程剧集 (EP号): `bili_temp/<EP_ID>/chunk_0.txt`

## Bilibili 课程 (Cheese) 工作流程

1.  **提取课程/剧集信息**: 使用课程专属脚本获取元数据和字幕。课程或者视频，往往由 SS 或者 EP 开头
    ```bash
    python3 skills/bilibili-subtitle-downloader/scripts/cheese_downloader.py <SS_ID or EP_ID>
    ```
    * **登录**: 脚本将生成一个 `bilibili_login_qr.png`。扫描它以登录。
    * **SS_ID 模式**: 如果提供 SS_ID（如 `ss123`），脚本将打印课程信息和所有剧集列表，需要使用具体的 EP_ID 来获取字幕。
    * **EP_ID 模式**: 如果提供 EP_ID（如 `ep456`），脚本将下载字幕并切分保存到 `bili_temp/ep456/` 目录，输出 `RESULT_JSON`。

## 子智能体指令

在生成用于总结的子智能体时，请使用以下提示词 (prompt) 模式：

> 请阅读以下 Bilibili 视频字幕分块，并提供全面、准确的总结。 
> 
> **要求：**
> - 捕获所有关键的技术细节、具体的数据点和逻辑步骤。
> - 使用标题保持清晰的结构。
> - 明确主旨和可执行的要点。
> - 风格：专业、信息丰富且详细。
>
> **字幕文件：** [PATH_TO_CHUNK]

## 资源

- **脚本**: `scripts/download_and_chunk.py` - 处理 Bilibili API 交互和基于 Token 的安全分块。