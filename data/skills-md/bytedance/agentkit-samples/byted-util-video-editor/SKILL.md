---
name: byted-util-video-editor
description: 视频编辑器，在需要视频后期制作、多个视频文件合成、视频添加音频轨道、合并多个音频文件、视频生成并烧录字幕场景时，使用该技能。
version: 1.0.0
license: Apache-2.0
---

# Video Editor - 视频编辑器

## 适用场景

当需要进行视频后期处理时使用此技能，包括：

- **合并多个视频**：将多个分镜视频合成一个完整视频
- **添加音频**：为视频添加旁白、背景音乐等音频轨道
- **合并音频**：将多个音频文件按时间轴合并成一个完整音频
- **生成字幕**：生成 SRT 格式的字幕文件
- **烧录字幕**：将字幕硬编码到视频中
- **视频制作**：短视频、宣传片、教学视频的后期合成

## 功能特性

### 1. 合并多个视频

- 支持 2+ 个视频文件拼接
- 自动处理视频编码和格式转换
- 保持原始视频质量
- **自动保留原始视频的背景音乐**

### 2. 添加音频轨道

- 支持添加旁白配音
- 支持添加背景音乐
- 可调节音频音量（0.0-2.0 倍）
- 可调节原始视频背景音乐音量（0.0-2.0 倍）
- 背景音乐和对白音频自动混合

### 3. 合并多个音频

- 支持将多个音频文件按时间轴合并成一个完整音频
- 每个音频可以指定自己的开始时间（秒）
- 使用 amix 滤镜平滑混合音频

### 4. 生成字幕

- 支持生成标准 SRT 格式字幕文件
- 支持多段字幕，每段有独立的开始/结束时间
- UTF-8 编码，支持中文字幕

### 5. 烧录字幕

- 将 SRT 字幕硬编码到视频中
- 需要 ffmpeg 编译时包含 libass（subtitles 滤镜）支持
- 如当前环境不支持，可使用其他视频编辑工具（如剪映等）烧录字幕

### 6. 灵活的操作模式

- **merge 模式**：合并多个视频（可同时添加音频）
- **add-audio 模式**：为现有视频添加音频
- **merge-audios 模式**：合并多个音频文件
- **generate-srt 模式**：生成 SRT 字幕文件
- **burn-subtitles 模式**：烧录字幕到视频

## 系统要求

### 安装 ffmpeg

**Ubuntu/Debian：**

```bash
sudo apt install ffmpeg
```

**macOS：**

```bash
brew install ffmpeg
```

**验证安装：**

```bash
ffmpeg -version
```

## 使用步骤

### 模式 1：合并多个视频

**基本用法：**

```bash
python scripts/video_editor.py output.mp4 --videos video1.mp4 video2.mp4 video3.mp4
```

**带音频合并：**

```bash
python scripts/video_editor.py output.mp4 --videos v1.mp4 v2.mp4 v3.mp4 --audio narration.mp3
```

**调整音频音量：**

```bash
# 对白音频音量为 0.8 倍（降低 20%）
python scripts/video_editor.py output.mp4 --videos v1.mp4 v2.mp4 --audio dialogue.mp3 --volume 0.8

# 对白音频音量为 1.5 倍（提高 50%）
python scripts/video_editor.py output.mp4 --videos v1.mp4 v2.mp4 --audio dialogue.mp3 --volume 1.5

# 同时调整背景音乐音量为 0.5 倍
python scripts/video_editor.py output.mp4 --videos v1.mp4 v2.mp4 --audio dialogue.mp3 --volume 0.8 --bg-volume 0.5
```

### 模式 2：为现有视频添加音频

**基本用法：**

```bash
python scripts/video_editor.py output.mp4 --video input.mp4 --audio narration.mp3 --mode add-audio
```

**调节音量：**

```bash
python scripts/video_editor.py output.mp4 --video input.mp4 --audio background.mp3 --volume 0.5 --mode add-audio
```

### 模式 3：合并多个音频文件

**基本用法：**

```bash
python scripts/video_editor.py output.mp3 --audios audio1.mp3,audio2.mp3 --start-times 0,5 --mode merge-audios
```

**参数说明：**

- `--audios`：要合并的音频文件列表，用逗号分隔
- `--start-times`：每个音频的开始时间（秒），用逗号分隔
- 两个列表的长度必须相同

### 模式 4：生成 SRT 字幕文件

**基本用法：**

```bash
python scripts/video_editor.py output.srt --subtitles '[{"text":"你好","start_time":0,"end_time":2},{"text":"世界","start_time":2.5,"end_time":5}]' --mode generate-srt
```

**参数说明：**

- `--subtitles`：JSON 格式的字幕数据，每个字幕包含：
  - `text`：字幕文字
  - `start_time`：开始时间（秒）
  - `end_time`：结束时间（秒）

### 模式 5：烧录字幕到视频

**基本用法：**

```bash
python scripts/video_editor.py output_with_subs.mp4 --video input.mp4 --subtitle subs.srt --mode burn-subtitles
```

**注意：**

- 字幕样式参数已预留，但实际效果取决于 ffmpeg 的 subtitles 滤镜配置
- 如当前环境不支持 subtitles 滤镜，建议：
  1. 使用专业视频编辑软件（Final Cut Pro、Premiere、剪映等）
  2. 使用在线视频工具（如 Kapwing、Clideo 等）

## 参数说明

| 参数              | 说明                                                                   | 示例                                                                  |
| ----------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `output`          | 输出文件路径                                                           | `final_video.mp4`                                                     |
| `--videos`        | 要合并的视频文件列表（2+ 个）                                          | `--videos v1.mp4 v2.mp4 v3.mp4`                                       |
| `--video`         | 单个视频文件（add-audio 或 burn-subtitles 模式）                       | `--video input.mp4`                                                   |
| `--audio`         | 单个音频文件（旁白、对白等）                                           | `--audio narration.mp3`                                               |
| `--audios`        | 要合并的音频文件列表（逗号分隔）                                       | `--audios a1.mp3,a2.mp3`                                              |
| `--start-times`   | 每个音频的开始时间（逗号分隔，秒）                                     | `--start-times 0,5`                                                   |
| `--volume`        | 对白音频音量（0.0-2.0，默认 1.0）                                      | `--volume 0.8`                                                        |
| `--bg-volume`     | 背景音乐音量（0.0-2.0，默认 1.0）                                      | `--bg-volume 0.5`                                                     |
| `--subtitles`     | 字幕数据（JSON 格式，generate-srt 模式）                               | `--subtitles '[{\"text\":\"你好\",\"start_time\":0,\"end_time\":2}]'` |
| `--subtitle`      | SRT 字幕文件路径（burn-subtitles 模式）                                | `--subtitle subs.srt`                                                 |
| `--font-name`     | 字幕字体名称                                                           | `--font-name "Arial"`                                                 |
| `--font-size`     | 字幕字体大小                                                           | `--font-size 24`                                                      |
| `--font-color`    | 字幕字体颜色                                                           | `--font-color "&H00FFFFFF"`                                           |
| `--outline-color` | 字幕边框颜色                                                           | `--outline-color "&H00000000"`                                        |
| `--outline`       | 字幕边框宽度                                                           | `--outline 2`                                                         |
| `--shadow`        | 字幕阴影深度                                                           | `--shadow 0`                                                          |
| `--alignment`     | 字幕对齐方式                                                           | `--alignment 2`                                                       |
| `--mode`          | 操作模式：merge、add-audio、merge-audios、generate-srt、burn-subtitles | `--mode generate-srt`                                                 |

## 实际示例

### 示例 1：AI 短剧合成

假设有 3 个分镜视频：

- `shot1.mp4`（5秒）
- `shot2.mp4`（10秒）
- `shot3.mp4`（10秒）

**合成无旁白版本：**

```bash
python scripts/video_editor.py drama_no_audio.mp4 --videos shot1.mp4 shot2.mp4 shot3.mp4
```

**合成带旁白版本：**

```bash
python scripts/video_editor.py drama_with_audio.mp4 --videos shot1.mp4 shot2.mp4 shot3.mp4 --audio narration.mp3
```

### 示例 2：添加背景音乐

为现有视频添加背景音乐，降低音量：

```bash
python scripts/video_editor.py video_with_music.mp4 --video original.mp4 --audio bgm.mp3 --volume 0.4 --mode add-audio
```

### 示例 3：合并多个对白音频

假设有 3 个对白音频文件，分别在不同时间点播放：

- `line1.mp3`（在 0 秒开始）
- `line2.mp3`（在 5 秒开始）
- `line3.mp3`（在 12 秒开始）

**合并成一个完整音频：**

```bash
python scripts/video_editor.py full_narration.mp3 --audios line1.mp3,line2.mp3,line3.mp3 --start-times 0,5,12 --mode merge-audios
```

### 示例 4：生成 SRT 字幕文件

假设有两段对白：

- "你好世界"（0-2 秒）
- "欢迎来到漫剧"（2.5-5 秒）

\*\*生成字幕文件：

```bash
python scripts/video_editor.py drama_subs.srt --subtitles '[{"text":"你好世界","start_time":0,"end_time":2},{"text":"欢迎来到漫剧","start_time":2.5,"end_time":5}]' --mode generate-srt
```

### 示例 5：烧录字幕到视频

**使用默认样式烧录：**

```bash
python scripts/video_editor.py drama_with_subs.mp4 --video drama.mp4 --subtitle drama_subs.srt --mode burn-subtitles
```

**注意：** 如环境不支持烧录功能，请直接使用生成的 SRT 字幕文件，配合剪映、Final Cut Pro 等视频编辑软件完成字幕烧录！
