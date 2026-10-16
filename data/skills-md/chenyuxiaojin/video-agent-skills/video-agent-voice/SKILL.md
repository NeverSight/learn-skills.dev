---
name: video-agent-voice
description: >
  视频团队的配音师。将逐字稿转为语音和字幕，支持 MiniMax Speech-02（中文首选，全球#1）、
  Edge-TTS（免费）、ElevenLabs（英文）、自录音四种模式。
  MiniMax 支持 10 秒声音克隆，中文 WER 仅 2.25%。
  能读取分镜表的情绪标注，生成带语速和情感控制的配音，
  以及供自录音参考的配音指导表。
  当收到"生成语音""处理音频""我录好音了"时触发，
  或由制片人（producer）调度时自动触发。
---

# video-agent-voice（配音师）

## 职责边界

- ✅ 将逐字稿转为语音文件
- ✅ 生成精确时间戳的字幕文件
- ✅ 根据分镜表的情绪标注调整语速和情感
- ✅ 为自录音模式生成配音指导表
- ❌ 修改逐字稿内容（编剧负责）
- ❌ 设计画面（分镜师负责）

## 输入 → 输出

- 输入：`script.md` + `storyboard.md`（可选，用于情绪标注）
- 输出：
  - `audio/voiceover.mp3`
  - `audio/subtitles.srt`
  - `audio/voice-direction.md`（配音指导表）

## 引擎选择

| 引擎 | 成本 | 中文质量 | 情绪控制 | 适用场景 |
|------|------|---------|----------|----------|
| MiniMax Speech-02 | 低 | 最高（全球#1） | emotion 参数 + 停顿标记 | 正式发布（中文首选） |
| Edge-TTS | 免费 | 中等 | SSML 语速/音调 | 快速测试、草稿 |
| ElevenLabs | 高 | 差（WER 16%） | Prompt 情感描述 | 英文视频 |
| 自录音 | 免费 | 最高 | 完全自控 | 追求最佳效果 |

- 默认使用 **MiniMax Speech-02**（中文质量全球第一，价格仅 ElevenLabs 的 1/4）
- 如果 project.json 中指定 `tts_engine: edge`，使用 Edge-TTS（免费草稿）
- 如果指定 `tts_engine: elevenlabs`，使用 ElevenLabs API（仅适合英文）
- 如果指定 `tts_engine: manual`，跳过语音生成，仅生成字幕模板和配音指导表

### MiniMax 声音克隆（可选）

支持用 10 秒录音克隆自己的声音，克隆后可反复使用：

```bash
python scripts/minimax_tts.py clone <你的录音.mp3> --voice-id myvoice001
```

克隆语音 7 天不使用会被自动删除，需重新克隆。克隆价格：9.9 元/次。

## 执行步骤

### 步骤 1：提取纯文本

```bash
python scripts/extract_plain_text.py <project>/script.md <project>/script-plain.txt
```

过滤规则（从 script.md 中去除非朗读内容）：
- 去除 `> 场景提示：...` 行
- 去除 `【出处：...】` 行
- 去除 Markdown 标题行（`## 案例一：...`）
- 去除元数据行（`> 逐字稿 | 目标时长：...`）
- 去除分隔线（`---`）
- 保留所有正文段落（这些是要朗读的内容）

### 步骤 2：生成情绪节奏映射

如果存在 `storyboard.md`，读取每个镜头的情绪/节奏标注，生成情绪映射：

```bash
python scripts/build_emotion_map.py <project>/storyboard.md <project>/script-plain.txt <project>/audio/emotion-map.json
```

输出 `emotion-map.json`：

```json
[
  {
    "segment": 1,
    "text": "你有没有想过一个问题：为什么你学了那么多时间管理方法...",
    "mood": "焦虑、快切",
    "pace": "fast",
    "ssml_rate": "+15%",
    "ssml_pitch": "+5%",
    "elevenlabs_style": "urgent, slightly anxious",
    "direction_note": "语速偏快，带一点焦虑感，像在追问观众"
  },
  {
    "segment": 5,
    "text": "Cal Newport 在《Deep Work》这本书里提出了一个概念...",
    "mood": "权威、可信",
    "pace": "normal",
    "ssml_rate": "+0%",
    "ssml_pitch": "-3%",
    "elevenlabs_style": "calm, authoritative",
    "direction_note": "语速正常，声音沉稳，引用专家时要有权威感"
  },
  {
    "segment": 12,
    "text": "一天 8 小时，真正能用来做深度工作的时间，可能连 2 小时都不到",
    "mood": "震惊、冲击",
    "pace": "slow_then_pause",
    "ssml_rate": "-10%",
    "ssml_pitch": "+0%",
    "elevenlabs_style": "dramatic pause, emphasis on the number",
    "direction_note": "说到'2 小时'之前稍微停顿，然后重音落在这个数字上，让观众感受冲击"
  }
]
```

情绪到语速的映射规则：

| 情绪关键词 | 语速 | SSML rate | 说明 |
|-----------|------|-----------|------|
| 焦虑、压迫、快切 | fast | +15% ~ +20% | 制造紧迫感 |
| 冲击、震惊、醒悟 | slow_then_pause | -10% ~ -15% | 关键信息前放慢，制造冲击 |
| 权威、可信、平稳 | normal | +0% | 沉稳叙述 |
| 共鸣、温暖、日常 | slightly_slow | -5% | 贴近观众，像聊天 |
| 希望、力量、行动 | slightly_fast | +5% ~ +10% | 带动情绪，收束有力 |
| 讽刺、荒诞、反差 | normal | +0% | 语气平淡反而更讽刺 |
| 悬念、期待 | slow | -10% | 吊胃口 |

如果没有 storyboard.md，则跳过此步骤，所有段落使用默认语速。

### 步骤 3：生成配音指导表

无论使用哪种引擎模式，都生成 `audio/voice-direction.md`：

```markdown
# 配音指导表 — 视频标题

> 总时长目标：约 8 分钟 | 总字数：约 1800 字

## 开头（0:00-0:30）

**语速：快** | **情绪：焦虑、追问**

> 你有没有想过一个问题：为什么你学了那么多时间管理方法，下载了那么多效率工具，看了那么多生产力视频，你还是觉得时间不够用？

🎯 配音要点：像在追问观众，语速偏快，带一点焦虑感

---

**语速：慢，停顿** | **情绪：悬念、权威**

> 今天我想告诉你一个反直觉的事实——生产力的公式里，其实只有一个变量。

🎯 配音要点："反直觉"之前微微停顿，"只有一个变量"放慢、加重

---

## 案例一：忙碌不等于生产力（0:30-2:30）

**语速：正常** | **情绪：权威、沉稳**

> Cal Newport 在《Deep Work》这本书里提出了一个概念，叫做"忙碌即生产力"谬误。

🎯 配音要点：引用专家时声音沉稳，语速正常，体现可信度

...
```

这份指导表有三个用途：
- 自录音模式下，你照着这个读，知道每段该用什么情绪
- TTS 模式下，作为质量对照：检查 AI 配音是否达到了指导表的要求
- 团队协作时，可以直接发给外包配音演员

### 步骤 4：生成语音

#### 模式 A：自录音（manual）

1. 导出 `script-plain.txt` + `voice-direction.md`
2. 等待用户上传 `audio/voiceover.mp3`
3. 使用 Whisper 生成 `subtitles.srt`

#### 模式 B1：Edge-TTS（免费）

```bash
python scripts/edge_tts_generate.py \
  <project>/script-plain.txt \
  <project>/audio \
  --voice zh-CN-YunxiNeural \
  --emotion-map <project>/audio/emotion-map.json
```

Edge-TTS 情绪控制方式：
- 读取 emotion-map.json
- 将纯文本转为 SSML 格式
- 对每个段落应用对应的 `<prosody rate="..." pitch="...">` 标签
- Edge-TTS 同时生成音频和字幕，无需 Whisper

SSML 示例：

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">
  <voice name="zh-CN-YunxiNeural">
    <prosody rate="+15%" pitch="+5%">
      你有没有想过一个问题：为什么你学了那么多时间管理方法，
      下载了那么多效率工具，看了那么多生产力视频，
      你还是觉得时间不够用？
    </prosody>
    <break time="500ms"/>
    <prosody rate="-10%" pitch="-3%">
      今天我想告诉你一个反直觉的事实。
    </prosody>
    <break time="300ms"/>
    <prosody rate="-10%" pitch="-3%">
      生产力的公式里，其实只有一个变量。
    </prosody>
  </voice>
</speak>
```

默认语音选项：
- 男声：`zh-CN-YunxiNeural`
- 女声：`zh-CN-XiaoxiaoNeural`

#### 模式 B2：MiniMax Speech-02（高质量，中文首选）

```bash
python scripts/minimax_tts.py \
  <project>/script-plain.txt \
  <project>/audio \
  --voice <voice_id> \
  --emotion auto
```

MiniMax 情绪控制方式：
- 模型：`speech-02-hd`（最高质量）或 `speech-02-turbo`（更快）
- emotion 参数：`auto`（自动）/ `happy` / `sad` / `calm`
- 文本内停顿标记：`<#0.5#>` 表示停顿 0.5 秒
- 长文本自动分段（每段不超过 8000 字符），多段用 ffmpeg 合并
- 合并后使用 Whisper 生成精确字幕
- 支持克隆语音：先用 `clone` 命令克隆，再用克隆的 voice_id 生成

#### 模式 B3：ElevenLabs（仅英文视频）

```bash
python scripts/elevenlabs_tts.py \
  <project>/script-plain.txt \
  <project>/audio \
  --voice-id [voice_id] \
  --emotion-map <project>/audio/emotion-map.json
```

ElevenLabs 情绪控制方式：
- 模型：`eleven_multilingual_v2`
- 读取 emotion-map.json
- 将每个段落的 `elevenlabs_style` 作为 style prompt 传入
- 长文本分段（每段不超过 5000 字符），按段落情绪分别生成
- 多段用 ffmpeg 合并
- 合并后使用 Whisper 生成精确字幕
- ⚠️ 注意：ElevenLabs 中文 WER 高达 16%，不建议用于中文视频

### 步骤 5：校验输出

- [ ] `audio/voiceover.mp3` 存在且可播放
- [ ] `audio/subtitles.srt` 存在且格式正确
- [ ] `audio/voice-direction.md` 已生成
- [ ] 字幕总条数与逐字稿段落数大致匹配
- [ ] 字幕每条不超过 2 行，每行不超过 20 个中文字符
- [ ] 音频总时长在目标时长 ±15% 以内
- [ ] 无明显断句错误或不自然的停顿

## 字幕分段规则

- 每条字幕不超过 2 行
- 每行不超过 20 个中文字符
- 按自然语句断句，避免在词语中间断开
- 标点符号保留在行尾

## API 配置

| 环境变量 | 用途 |
|----------|------|
| MINIMAX_API_KEY | MiniMax 语音生成（模式 B2，推荐） |
| MINIMAX_GROUP_ID | MiniMax 声音克隆（仅克隆时需要） |
| ELEVENLABS_API_KEY | ElevenLabs 语音生成（模式 B3，仅英文） |

## 依赖

| 依赖 | 用途 | 必需 |
|------|------|------|
| edge-tts | Edge-TTS 语音生成 | 模式 B1 |
| whisper | 语音转字幕 | 模式 A / B2 |
| ffmpeg / ffprobe | 音频合并与时长检测 | 是 |

## 脚本文件

- `scripts/extract_plain_text.py` — 从 script.md 提取纯文本（更新过滤规则）
- `scripts/build_emotion_map.py` — 从分镜表生成情绪节奏映射
- `scripts/minimax_tts.py` — MiniMax Speech-02 语音生成 + 声音克隆（中文首选）
- `scripts/edge_tts_generate.py` — Edge-TTS 语音+字幕生成（支持 SSML 情绪控制）
- `scripts/elevenlabs_tts.py` — ElevenLabs 语音生成（仅英文，支持 style prompt）
- `scripts/generate_subtitles.py` — Whisper 字幕生成
