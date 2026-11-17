---
name: synesthesia-mapper
description: "把图像确定性地映射为音乐和视觉乐谱，生成 MIDI、WAV、PNG/SVG 乐谱、映射 JSON 与同步 HTML 预览。用于用户提出图像转声音、颜色作曲、视觉音乐、共感艺术、图片生成 MIDI/WAV、动态海报前期声音草图、视觉乐谱或跨感官映射时；支持 PNG、JPG、JPEG、WebP 等常见图片。第一版聚焦图像转声音，不要声称已经支持音频转视觉。"
---

# 共感谱 Synesthesia Mapper

把图像的空间、颜色、亮度与纹理翻译成受调式和节拍约束的音乐事件。同一输入、预设、参数与种子必须得到相同结果；将它描述为艺术映射系统，不要声称它读取了图像的“真实声音”或模拟医学意义上的联觉。

## 工作流

1. 确认输入为一张可读取的图片。保留原图，不覆盖源文件。
2. 运行能力检测：

```bash
python scripts/capability_check.py
```

缺少 Pillow 或 NumPy 时，明确报告缺失项并停止生成。环境没有命令执行或文件写入能力时，只能设计映射方案；不要声称已经生成 MIDI、WAV 或乐谱文件。

3. 选择预设：
   - `prism`：默认。平衡颜色、空间和纹理，适合大多数摄影与插画。
   - `grain`：增强纹理与短音，适合颗粒、拼贴和高细节图像。
   - `orbit`：径向扫描与小调音阶，适合中心构图、圆形和放射结构。
4. 运行生成器。未给出音乐偏好时，直接使用 `prism`，不要为了根音或 BPM 阻塞任务：

```bash
python scripts/synesthesia_mapper.py image-to-sound INPUT \
  --output-dir OUTPUT \
  --preset prism \
  --title "作品标题"
```

5. 读取 `validation.json`。只有 `status` 为 `pass`，且 MIDI、WAV 与乐谱校验均通过时，才报告生成完成。
6. 交付 `interactive-preview.html` 作为首选入口，并列出 MIDI、WAV、PNG/SVG 乐谱和 `mapping.json`。

## 参数选择

在用户明确要求时覆盖预设：

```bash
python scripts/synesthesia_mapper.py image-to-sound INPUT --output-dir OUTPUT \
  --preset prism --scan horizontal --root D --scale pentatonic \
  --bpm 92 --bars 8 --density 0.58 --smoothness 1.0 --seed 42
```

- `--scan horizontal|radial`：横向叙事画面用 `horizontal`；中心或放射构图用 `radial`。
- `--scale pentatonic|major|minor|dorian|chromatic`：默认优先五声音阶；实验性需求再用 chromatic。
- `--density 0..1`：控制每个时间片的最大音符数和触发阈值。复杂图片从 `0.45–0.65` 开始。
- `--smoothness 0.5..1.8`：控制延音；不是图像模糊参数。
- `--bars` 与 `--steps-per-bar`：共同决定扫描时间分辨率。先增加 bars，再增加 steps，避免音符过密。
- `--min-midi` 与 `--max-midi`：限制音域；人声或乐器编配需求应主动设置。

读取 [references/mapping-system.md](references/mapping-system.md) 处理映射解释、调式与扫描路径选择。读取 [references/output-and-validation.md](references/output-and-validation.md) 处理文件交付、校验和环境限制。

## 输出解释

- `synesthesia.mid`：可继续在 Ableton Live、Logic Pro、Cubase、FL Studio 等软件中编曲。
- `synesthesia.wav`：内置轻量合成器渲染的试听，不代表最终音色设计。
- `visual-score.png` / `visual-score.svg`：适合展示、打印和继续排版的视觉乐谱。
- `interactive-preview.html`：图片扫描线、声音和音符同步的交互预览。
- `mapping.json`：完整参数与逐音符来源，可用于复现和二次开发。
- `validation.json`：文件完整性、音频格式和最大复音数等检查结果。

## 质量判断

- 先保证音乐性，再追求像素级直译。默认量化到调式，不把每个像素变成一个音符。
- 音符过多时降低 `density`；过于平淡时增加 bars 或改用 `grain`，不要直接使用 chromatic 补密度。
- 径向扫描的时间对应角度，音高对应半径；不要把它解释成画面中的上下位置。
- 把 WAV 称为“基础合成试听”。专业成片应使用 MIDI 更换音源、混音和母带。
- 说明当前版本只实现图像转声音。收到声音转视觉请求时，可以设计映射方案，但不要伪造 MP4、粒子或字形动画输出。
