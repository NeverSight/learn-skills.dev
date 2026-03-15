---
name: capture
description: 启动屏幕截图工具。当用户要求截图、录屏、捕获屏幕内容时使用。
allowed-tools: Bash(source .venv/bin/activate *)
---

启动屏幕区域定时截图工具。

执行以下命令：

```bash
source .venv/bin/activate && python pipeline.py capture --save-dir output/captures --interval $0
```

- `$0` 是截图间隔（毫秒），默认 500
- 这会打开一个 GUI 窗口

告知用户操作步骤：
1. 点击 "Select Area" 选择屏幕上要截图的区域
2. 点击 "Start Capture" 开始定时截图
3. 播放视频，等截图完成
4. 点击 "Stop Capture" 停止，关闭窗口

截图保存在 `output/captures/` 目录。
