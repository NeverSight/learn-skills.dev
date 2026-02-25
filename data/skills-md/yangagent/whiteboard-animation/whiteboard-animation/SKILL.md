---
name: whiteboard-animation
description: 从图片生成白板手绘动画视频。将任意彩色图片转换为包含线稿绘制和上色两个阶段的动画，带手部覆盖效果，输出 H.264 MP4 视频。当用户说"把图片做成白板动画"、"白板动画"，或使用 /whiteboard 时触发。
---

# 白板手绘动画生成器

从输入图片生成白板手绘动画视频，动画分为两个阶段：
1. **线稿绘制** — 手持笔在白板上逐步画出黑白线稿
2. **上色** — 手持笔沿内容轮廓逐步涂上彩色，还原为原图

## 工作流

### 第一步：准备环境

先用 `--check` 检测环境是否就绪：

```bash
python <skill目录>/scripts/setup_env.py --check
```

- 如果成功（退出码 0）：最后一行输出 `PYTHON_PATH=<路径>`，**捕获该路径用于后续步骤**，直接跳到第二步
- 如果失败（退出码 1）：运行完整安装：

```bash
python <skill目录>/scripts/setup_env.py
```

安装脚本会自动创建 `.venv` 虚拟环境并安装缺失依赖（`opencv-python`、`numpy`、`av`），最后一行同样输出 `PYTHON_PATH=<路径>`。

### 第二步：确认输入图片

从用户请求中获取图片路径，确认文件存在。支持格式：PNG、JPG、JPEG、BMP、TIFF。

白色或浅色背景的图片效果最佳。

### 第三步：确定参数

收集可选参数，所有参数都有合理的默认值：

| 参数 | 标志 | 默认值 | 说明 |
|------|------|--------|------|
| 图片路径 | 位置参数（必填） | -- | 输入的彩色图片路径 |
| 输出目录 | `--output-dir` | `./output` | 视频输出目录 |
| 时长 | `--duration` | `10` | 视频总时长（秒），生成的视频会精确匹配该时长 |
| 无手部 | `--no-hand` | 默认显示手 | 禁用手部覆盖效果 |

### 第四步：运行生成脚本

使用第一步获取的 `PYTHON_PATH` 运行生成脚本：

```bash
<PYTHON_PATH> <skill目录>/scripts/generate_whiteboard.py <图片路径> [--output-dir <目录>] [--duration <秒>] [--no-hand]
```

示例：

```bash
<PYTHON_PATH> <skill目录>/scripts/generate_whiteboard.py /path/to/photo.png --output-dir ./output --duration 20
```

### 第五步：返回结果

脚本会将最终视频路径打印到 stdout，将该路径告知用户。输出文件命名格式：`vid_YYYYMMDD_HHMMSS_h264.mp4`。

## 故障排除

- **`ModuleNotFoundError`**：重新运行 `setup_env.py` 确保依赖完整安装。
- **输出全黑/无内容**：输入图片可能太暗，建议使用浅色背景的图片。
- **输出文件过大**：减小 `--duration` 值以缩短视频时长。
- **虚拟环境创建失败**：确认系统已安装 Python 3.8+，且 `python3` 命令可用。
