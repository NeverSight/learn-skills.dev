---
name: video-editor
description: "粗剪现成 MP4、MOV、MKV 视频：压缩停顿、识别口误重讲与废案，导出新视频、剪辑计划和审计报告。用户要求自动粗剪、压缩口播节奏或导出剪辑时间线时使用。不用于 Screen Studio 原生工程（交给 screen-studio-editor），不生成字幕（交给 oil-subtitle）。"
---

# Video Editor

压缩停顿、识别口误废案，生成可复核的剪辑计划，再导出新视频。语音转文字由 ASR 完成，语义判断由调用这个 Skill 的 Agent 根据带时间戳的转录亲自完成；两步都可能出错，正式使用前需要检查报告与接缝听感。

后续字幕生成交给 `oil-subtitle`。

---

## 目标

适合以人声讲解为主的视频；会议、音乐和依赖长停顿的演示需要逐段复核。
1. **压缩停顿**：以能量检测和 VAD 确认无声，统一使用 300ms 的连续无声门限，保留约 180ms 气口。底层探测窗口是 250ms，只负责找候选；只有实际无声超过 300ms 才会剪。ASR 时间戳用于对齐和说明，落在确认无声区里不会自动阻止剪辑；只有纯 ASR 词间距候选才使用文字保护。
2. **识别口误废案**：按子句切分并滑窗分析；引用必须覆盖完整删除话术，替代话术必须在最终计划中保留。
3. **收尾安全检查**：语义删减仍须避开保留词和替代话术；音频已确认的停顿可以覆盖不精确的 ASR 时间戳，不能再被同一条 ASR 保护规则拦回。
4. **减轻接缝杂音**：波形吸附只允许缩小删除区间；正常编码在各段首尾施加 15ms `afade`，不保证所有接缝听感相同。
5. **安全导出**：默认重编码，禁止覆盖源片；`--fast-copy` 仅用于近似预览，可能保留额外内容，不应用淡化。

---

## 外部服务与语义判断边界

只有语音转文字需要 DashScope API Key，先读[API Key 配置与业务读取](references/api-key-setup.md)。本 Skill 的 ASR 后端固定为百炼 `bailian`；语义判断不调用外部模型或模型接口，Agent 读取本地转录上下文后，自己写出语义删减计划。已有安全配置直接复用，缺少时由用户亲自填写固定页面，不在聊天或命令参数中传 Key。

---

## 环境与配置

### 1. 基础依赖

- `ffmpeg`、`ffprobe`：安装后放入系统 PATH；macOS 也支持 `/opt/homebrew/bin/`。
- DashScope API Key（仅用于 ASR）。优先使用 `bl` CLI 的 `fun-asr`，未安装 bl 时使用 SDK 的 `paraformer-realtime-v2`。
- Python 3.10+；macOS / Linux 首次运行 `bash setup.sh`，Windows 首次运行 `PowerShell -ExecutionPolicy Bypass -File .\setup.ps1`，两者都会创建虚拟环境并安装依赖。钥匙串配置与读取另需 Node.js 22.18+，详见凭据说明。
- macOS / Linux 使用 `bash <SKILL_DIR>/scripts/run.sh ...`；Windows PowerShell 使用 `<SKILL_DIR>\scripts\run.ps1 ...`。

### 2. Agent 语义判断配置

配置文件路径：`~/.config/video-editor/config.json`（可选，不存在时使用默认值）：

```json
{
  "asr_backend": "bailian",
  "semantic_planner": "calling-agent",
  "semantic_max_local_cleanup_ms": 2500.0,
  "pause_threshold_ms": 300.0,
  "sentence_threshold_ms": 300.0,
  "min_pause_ms": 180.0,
  "crossfade_ms": 15.0
}
```

- `semantic_planner` 固定为 `calling-agent`，表示语义判断由当前调用 Skill 的 Agent 完成，不读取模型地址、不保存模型 Key。
- `asr_backend` 固定为 `bailian`，视频 Skill 不安装或调用本地 Whisper；需要本地 ASR 时使用 `screen-studio-editor` 的显式 `local` 模式。
- `semantic_max_local_cleanup_ms` 是局部口误的安全上限，超过 2.5 秒的 `delivery_cleanup` 或 `self_correction` 默认拒绝。
- `scripts/run.sh` 和 `scripts/run.ps1` 按当前平台选择虚拟环境入口：只为 ASR 复用环境变量或已有 bl 配置，缺少时通过凭据组件从系统库注入。普通配置 JSON 不保存 Key。

---

## 工作流

### 1. 默认智能剪辑（推荐）

对源视频进行完整分析并导出剪辑后的新视频。语义删减分成两步，避免把一个外部模型偷偷当成“自动裁判”：

```bash
bash scripts/run.sh cut /path/to/video.mp4
```

Windows PowerShell：

```powershell
.\scripts\run.ps1 cut C:\path\to\video.mp4
```

第一次运行会完成 ASR、VAD 和停顿分析，并生成 `semantic_context.json`。调用 Skill 的 Agent 读取这个文件，按其中的 JSON 规则判断口误，写出同目录的 `semantic_plan.json`，然后继续运行：

```bash
bash scripts/run.sh cut /path/to/video.mp4 --semantic-plan /path/to/.video.mp4_work/semantic_plan.json -o /path/to/video_edited.mp4
```

工作流程：
1. **音频提取与声学校准**：提取 16kHz WAV 音频，自适应计算能量分布分位数与底噪；自动静音阈值设有 `-30.5 dB` 下限，避免低电平空白片段因少量孤立峰值被误当成有声。
2. **高精度 ASR 字级识别**：调用已选择的 ASR，检查转录格式与字时间戳；缺失时停止。
3. **自适应停顿检测与证据标注**：结合 Silero VAD 与句尾标点感知切分死寂停顿；ASR 负责时间对齐和复核提示，不会否决已经由音频确认的无声区。
4. **Agent 语义口误规划**：按子句标点切分为原子片段，生成带时间戳的本地上下文；由当前 Agent 阅读上下文，依据“宁可漏删，不要误删”的规则写出 `semantic_plan.json`，程序只负责校验编号、原话覆盖、替代冲突和安全时长。
5. **切点波形极小值吸附**：只在删除区间内微调，随后重新检查保留文字。
6. **平台编码与微淡化**：macOS 采用 `h264_videotoolbox`，Windows / Linux 使用 `libx264`，每段保留切片首尾施加 15ms `afade`。部分 Windows FFmpeg 版本不再提供 `filter_complex_script`，程序会自动改用文件参数读取滤镜图，必要时再以内联滤镜图兜底。
7. **生成 Markdown 审计报告**：记录实际配置，分别标明计划时长、导出状态和实测时长。

### Agent 写 `semantic_plan.json` 的规则

Agent 只根据 `semantic_context.json` 里的文字和时间戳判断，不重新听猜，也不把“有停顿”直接当成废话。每个删减都要能回答三个问题：前一句为什么是废案、后一句是否真的重述或纠正、删掉后句子是否仍然完整。

计划文件最小格式如下：

```json
{
  "source": "复制 semantic_context.json 里的 source",
  "edits": [
    {
      "remove_start_id": "U0007",
      "remove_end_id": "U0007",
      "cut_until_id": "U0008",
      "replacement_ids": ["U0012"],
      "removed_quote": "不对，重新说。",
      "replacement_quote": "点击右边的导出按钮。",
      "category": "explicit_restart",
      "confidence": "high",
      "reason": "后面明确重述同一条操作，前一句被说停并放弃。"
    }
  ]
}
```

`removed_quote` 必须覆盖完整的待删原话；`replacement_ids` 只能指向真正重述或纠正的片段。没有明确证据就返回空的 `edits`，不要为了让视频更紧凑而扩大删除范围。程序还会拒绝低置信度候选、替代片段被同时删除的候选，以及超过 2.5 秒的局部口误候选。

---

### 2. 预览分析与试运行（Dry-run）

若只想生成上下文、先让 Agent 判断而不实际渲染大视频：

```bash
bash scripts/run.sh cut /path/to/video.mp4
```

- 在源文件旁的 `.<name>.<ext>_work/` 生成 `semantic_context.json`；Agent 写完 `semantic_plan.json` 并再次运行带 `--semantic-plan` 的命令后，才会生成 `<name>_edit_plan.json` 和 `<name>_edit_report.md`。
- `semantic_context.json` 包含原子片段、停顿标记和逐窗口提示；它只供 Agent 阅读，不上传视频。
- 报告中包含：原始时长、预计时长、压缩比例、每一处口误删减区间、原话、订正保留话术与删减理由。

---

### 3. 近似流拷贝预览（Fast-copy）

仅用于接受关键帧边界偏差的快速预览。报告记录实测时长与计划偏差；需要准确删除口误时使用默认重编码：

```bash
bash scripts/run.sh cut /path/to/video.mp4 --semantic-plan /path/to/.video.mp4_work/semantic_plan.json --fast-copy -o /path/to/video_fast.mp4
```

---

### 4. 离线复核与重新渲染（Review / Re-render）

读取已有计划，不调用模型或读取 Key。需要调整时，编辑计划中的 `kept_intervals`（源视频毫秒坐标），再 render；报告的实际保留区间会同步更新，原话与理由仍来自分析阶段：

```bash
bash scripts/run.sh review /path/to/video.mp4
bash scripts/run.sh render /path/to/video.mp4 -o /path/to/video_edited.mp4
```

更换源视频后必须重新分析。已有成片默认不覆盖，明确需要替换时加 `--overwrite`；该选项也不能覆盖源片。分析失败可直接重试，相同源文件的有效音频和转录会复用，原有成功计划不会被失败结果替换。

---

## 输出规范

1. **剪辑后视频**：
   - 命名：默认在源文件同目录下生成 `<name>_edited.<ext>`，或由 `-o` 指定。
   - 编码：默认 H.264 与 192k AAC 重编码，不缩放画面；重编码有损，帧边界存在量化误差。临时导出经轨道与时长检查后才写入目标文件。
2. **审计报告**：
   - 保存在源文件旁的 `.<name>.<ext>_work/<name>_edit_report.md`。
   - 提供 Markdown 表格，清晰记录各处删减的前后文与删减理由。

---

## 资源导航

- `references/api-key-setup.md`: API Key 安全配置、环境绑定与凭据读取规范。
- `scripts/run.sh` / `scripts/run.ps1`: 按平台选择虚拟环境与凭据入口。
- `scripts/video_editor.py`: 分析、离线复核与按计划渲染。
- `scripts/audio_extractor.py`: 音频提取与声学能量分析。
- `scripts/transcriber.py`: 阿里百炼 ASR 转录模块（支持 `bl` CLI 与 SDK）。
- `scripts/silence_detector.py`: 自适应静音检测、VAD 与字保护算法。
- `scripts/semantic_planner.py`: 子句原子化切分、Agent 提示构造和语义计划校验；不发起任何模型请求。
- `scripts/video_assembler.py`: 平台编码、Windows FFmpeg 滤镜参数兼容、15ms 音频微淡化与报告生成。
- `tests/`: 基础算法与业务回归测试。维护时运行 `.venv/bin/python3 -m unittest discover -s tests -v`，覆盖源片保护、缓存失效、ASR 格式、缺少 Agent 计划、替代冲突和实际渲染；不得以基础函数测试通过代替完整流程验证。
