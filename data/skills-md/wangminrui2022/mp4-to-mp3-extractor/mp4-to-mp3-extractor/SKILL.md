---
name: mp4-to-mp3-extractor
description: |-
  批量将指定目录下的 .mp4 视频文件提取为 .mp3 音频文件。
  脚本会自动管理其 Python 虚拟环境并保持文件夹结构。
metadata:
  openclaw:
    requires:
      bins:
        - ffmpeg
        - python
---

# MP4 to MP3 Extractor Skill

## 执行步骤
1. **解析目录**: 识别用户的源目录（如 `D:\Videos`）。
2. **默认目标**: 若用户未指定输出路径，默认设为 `[源目录]_audio`。
3. **调用命令**:  使用以下兼容性命令来启动脚本，它会优先尝试 python3，若失败则尝试 python，脚本会自动处理虚拟环境的创建和切换。
   ```bash
   (python3 ./skills/mp4-to-mp3-extractor/scripts/extract.py "<源目录>" "<目标目录>") || (python ./skills/mp4-to-mp3-extractor/scripts/extract.py "<源目录>" "<目标目录>")