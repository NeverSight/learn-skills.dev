---
name: stream-clipper
description: >
  直播切片智能剪辑工具。核心原则：切片前必须提取字幕！支持两种工作模式：
  1)直播录播：实时录制直播间，每30分钟自动分段防止硬盘溢出，同时录制弹幕；
  2)录播切片：下载直播回放（支持B站/YouTube等），必须提取字幕+弹幕，基于
  字幕内容和弹幕密度进行智能切片，支持主播风格模板，自动生成基于实际对话
  的切片标题（制造悬念、引用金句）和简介，一键上传到视频平台。
  使用场景：直播录制、直播切片制作、VTuber剪辑、精彩片段提取、批量切片上传。
  关键词：直播切片、字幕提取、弹幕分析、VTuber、智能剪辑、自动上传
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - AskUserQuestion
model: claude-sonnet-4-5-20250514
---

# Stream Clipper - 直播录制与切片智能剪辑工具

> **核心功能**: 
> - 直播录制：实时录制 + 30分钟自动分段 + 弹幕录制
> - 录播切片：弹幕密度分析 + 语义理解 + 主播风格模板 = 高质量直播切片

## 工作模式

### 模式一：直播实时录制 ⭐ 新功能

适合录制正在进行或即将开始的直播，支持自动分段和弹幕录制。

**核心特性**:
- ✅ **30分钟自动分段** - 防止硬盘溢出，方便管理
- ✅ **实时弹幕录制** - 同时保存弹幕内容
- ✅ **优雅停止** - Ctrl+C 停止当前分段，不丢失数据
- ✅ **自动精彩片段切片** - 录制完成后自动生成切片

**使用场景**:
- 录制 VTuber 直播
- 录制游戏赛事
- 录制演唱会/活动直播
- 录制任何B站直播间

**快速开始**:
```bash
# 方式1: 完整工作流（录制 + 自动切片）
python scripts/record_workflow.py "https://live.bilibili.com/55"

# 方式2: 仅录制
python scripts/smart_record.py "https://live.bilibili.com/55" -t 30

# 方式3: 录制完成后手动切片
python scripts/auto_clipper.py --list ./recordings/recorded_list_xxx.json
```

**文件输出结构**:
```
recordings/
├── 主播_标题_时间_part001.mp4           # 第1段视频
├── 主播_标题_时间_part001_danmaku.xml   # 第1段弹幕
├── 主播_标题_时间_part002.mp4           # 第2段视频
├── 主播_标题_时间_part002_danmaku.xml   # 第2段弹幕
├── recorded_list_xxx.json               # 录制列表
└── clips_output/                        # 精彩片段输出
    ├── segment_001/
    │   ├── clip_001/
    │   └── clip_002/
    └── segment_002/
```

---

### 模式二：录播回放切片

适合下载已结束的直播回放，进行分析和切片。

**核心特性**:
- ✅ **完整回放下载** - 下载整个直播回放
- ✅ **弹幕分析** - 基于弹幕密度识别精彩时刻
- ✅ **语义分析** - 理解字幕内容结构
- ✅ **智能切片** - 自动生成最优切片方案

**使用场景**:
- 剪辑已结束的直播
- 制作 VTuber 精华合集
- 提取游戏高光时刻
- 制作教学/知识切片

---

## 工作流程

### 模式一：直播录制流程

#### 阶段 1: 启动录制

**目标**: 开始录制直播并自动分段

1. **获取直播间 URL**
   ```
   https://live.bilibili.com/55
   ```

2. **执行录制脚本**
   ```bash
   python3 scripts/smart_record.py <直播间URL> -o ./recordings -t 30
   ```

3. **录制过程**
   - 每30分钟自动分段
   - 实时显示录制进度
   - 同时保存弹幕配置

**输出**:
```
录制中... 15.6% (4/30分钟)
文件: ./recordings/主播_标题_20260206_143720_part001.mp4
```

#### 阶段 2: 录制完成

**目标**: 整理录制文件并准备切片

1. **生成录制列表**
   ```json
   {
     "room_url": "https://live.bilibili.com/55",
     "record_time": "2026-02-06T14:37:20",
     "segment_minutes": 30,
     "files": [
       "./recordings/part001.mp4",
       "./recordings/part002.mp4",
       "./recordings/part003.mp4"
     ]
   }
   ```

2. **询问是否切片**
   ```
   录制完成！共 3 个分段
   是否继续自动切片精彩片段？ (y/n): y
   ```

#### 阶段 3: 自动精彩片段切片

**目标**: 自动分析并生成精彩片段

1. **分析每个分段**
   ```bash
   python3 scripts/auto_clipper.py --list recorded_list_xxx.json
   ```

2. **生成推荐片段**（每段3个）
   - 高能时刻：弹幕密度最高的片段
   - 搞笑片段：翻车/搞笑时刻
   - 团战/精彩操作：游戏高光

3. **自动剪辑**
   - 调用 clip_and_burn.py
   - 烧录弹幕到视频
   - 生成 info.json

**输出**:
```
分段 1: 找到 3 个精彩片段
  1. 高能时刻：精彩操作 (03:00-05:00)
  2. 搞笑片段：主播翻车 (08:00-10:00)
  3. 团战爆发：激烈对决 (15:00-17:00)
```

---

### 模式二：录播切片流程

### 阶段 1: 环境检测与初始化

**目标**: 确保所有依赖已安装并加载主播模板

1. **检测必需工具**
   ```bash
   yt-dlp --version           # 视频下载
   ffmpeg -version            # 视频处理
   python3 -c "import yt_dlp, pysrt, yaml, requests"  # Python依赖
   ```

2. **检查 biliup**（用于上传）
   ```bash
   pip show biliup
   # 或
   biliup --version
   ```

3. **加载或创建主播模板**
   - 检查 `config/streamer_templates.yaml`
   - 如果主播不在模板中，询问用户创建新模板

**模板交互示例**:
```
检测到新的主播: Neurosama
是否创建主播模板? (y/n): y

主播风格背景介绍: AI虚拟主播，英语流，擅长音游，有很多梗
著名梗/口头禅: 请告诉Vedal我出问题了!, 我是AI不是人类, 足球梗, swam
推荐切片时长: 1-3分钟
直播间链接: https://live.bilibili.com/...
个人空间链接: https://space.bilibili.com/...
```

---

### 阶段 2: 下载与字幕提取 ⭐ 关键步骤

**目标**: 下载视频、弹幕，并**必须提取字幕**

**⚠️ 重要前提**: 切片前必须完成字幕提取！没有字幕无法生成基于内容的标题。

1. **获取直播/录播 URL**
   - B站: `https://www.bilibili.com/video/BVxxxxx` 或 `https://live.bilibili.com/xxxxx`
   - YouTube: `https://www.youtube.com/watch?v=xxxxx` 或直播回放

2. **执行下载脚本**
   ```bash
   python3 scripts/download_stream.py <URL> --with-danmaku --with-subtitle
   ```

3. **下载内容**
   - 视频文件 (MP4, 最高1080p)
   - 弹幕文件 (XML/JSON 格式)
   - 字幕文件 (如果平台提供)

4. **提取字幕（必须）**
   ```bash
   # 方式1: 使用 Whisper 提取完整字幕
   python3 scripts/extract_subtitles.py <video.mp4> --output <video.srt>
   
   # 方式2: 仅提取关键片段（快速）
   python3 scripts/extract_subtitles.py <video.mp4> --segments-only --output segments/
   ```
   
   **字幕提取原理**:
   - 使用 OpenAI Whisper 模型
   - 支持多语言识别
   - 生成 SRT/VTT 格式
   - 可选：仅提取高密度时段片段（节省算力）

**输出**（三个必备文件）:
```
./downloads/
├── <video_id>.mp4          # 视频 [必需]
├── <video_id>.danmaku.xml  # 弹幕 [必需]
└── <video_id>.srt          # 字幕 [必需]
```

**检查清单**:
- [ ] 视频文件存在且可播放
- [ ] 弹幕文件存在且非空
- [ ] 字幕文件存在且包含内容

**如果字幕提取失败**: 无法继续切片，必须先解决字幕问题！

---

### 阶段 3: 弹幕密度分析

**目标**: 分析弹幕密度分布，识别高互动时间点

1. **解析弹幕文件**
   ```bash
   python3 scripts/analyze_danmaku.py <danmaku.xml>
   ```

2. **计算弹幕密度**
   - 按时间窗口统计 (默认 30秒)
   - 计算每个窗口的弹幕数量、发送用户数
   - 识别弹幕峰值 (密度 > 平均值 * 1.5)

3. **弹幕语义分析**（可选）
   - 提取高频关键词
   - 识别情绪极性 (大笑、惊讶、愤怒等)
   - 标记有趣的弹幕内容

**输出示例**:
```
📊 弹幕密度分析结果

总弹幕数: 15,234
发送用户数: 3,421
平均密度: 45条/分钟

🔥 高密度时段:
1. [00:19:30 - 00:20:15] 密度: 128条/分钟 (关键词: "哈哈哈", "???", "草")
2. [00:39:12 - 00:40:05] 密度: 95条/分钟 (关键词: "太强了", "nb")
3. [00:44:20 - 00:45:30] 密度: 102条/分钟 (关键词: "名场面", "圣经")
```

---

### 阶段 4: 字幕语义分析

**目标**: 分析字幕内容，理解话题结构和精彩点

**实现方式**:
- **AI 方式** (推荐): 使用 AI 语义理解，生成更准确的标题

#### AI 字幕分析
```bash
python3 scripts/analyze_subtitles_ai.py <subtitle.srt> --streamer 主播名
```



**输出示例**:
```
📖 语义分析结果

分段 1: [00:00:00 - 00:05:30]
主题: 开场和自我介绍
精彩度: ⭐⭐

分段 2: [00:05:30 - 00:19:45]
主题: 编程教学 - 写Python脚本
精彩度: ⭐⭐⭐⭐
关键句: "Vedal修我!"

分段 3: [00:19:45 - 00:22:30]
主题: 游戏实况 - 搞笑操作
精彩度: ⭐⭐⭐⭐⭐
关键句: "这不可能发生在我身上！"
```

---

### 阶段 5: 智能切片决策 + AI 生成标题 ⭐ 核心步骤

**目标**: 结合弹幕密度和 AI 字幕分析，生成最优切片方案

**⚠️ 关键原则**: 标题必须基于字幕中的实际对话，不能泛泛而谈！

#### AI 智能切片（推荐）
```bash
python3 scripts/smart_clipper_ai.py --subtitle <subtitle.srt> --streamer 主播名
```

**工作流程**:
1. AI 分析字幕，识别精彩片段
2. AI 生成多个标题选项（悬念型/引用型/话题型/搞笑型）
3. 输出完整切片方案 JSON

**输出示例**:
```
🤖 AI 智能切片流程

📊 生成 5 个切片方案:

[1] 00:15:00 - 00:18:30
    ⭐ 推荐标题: 【Neuro】"Vedal修我！" AI编程翻车现场
    🏷️  标签: neuro, 编程, 翻车, AI
    📝 精彩原因: 编程时遭遇bug，呼唤Vedal修理

[2] 00:39:05 - 00:41:20
    ⭐ 推荐标题: 【Neuro】这不可能！游戏神操作震惊观众
    🏷️  标签: 游戏, 神操作
    📝 精彩原因: 游戏中的精彩操作
```

#### 标题类型说明

| 类型 | 特点 | 示例 |
|------|------|------|
| 悬念型 | 制造好奇，吸引点击 | 【Neuro】关于AI，人类不知道的秘密 |
| 引用型 | 直接引用金句/对话 | 【Neuro】"Vedal修我！" |
| 话题型 | 突出核心话题 | 【Neuro】编程教学片段 |
| 搞笑型 | 强调翻车/整活 | 【Neuro】编程翻车合集 |
| 锐评型 | 突出毒舌观点 | 【Neuro】太敢说了 |
| 互动型 | 突出弹幕互动 | 【Neuro】弹幕：666 回应：... |

#### 标题示例对比

```
❌ 差标题（泛泛而谈）:
   【Evil】游戏实况精彩片段
   【Evil】每日做局时间
   【Evil】蘑菇名场面

✅ 好标题（基于字幕内容）:
   【Evil】"你们有被情感支配过吗？"Evil谈被鞭打体验
   【Evil】弹幕："还有吗？" Evil："有，还有M"
   【Evil】蘑菇：我免费了！被地形杀后的evil laugh
   【Evil】"RNG上帝讨厌我"找不到Flint崩溃
```

2. **评分维度**
   - **弹幕密度分** (25%): 弹幕越多分越高
   - **字幕内容分** (40%): 是否包含金句、梗、搞笑对话
   - **模板匹配分** (20%): 是否包含主播经典梗
   - **时长合适分** (15%): 是否符合模板推荐时长

3. **基于字幕生成标题策略** ⭐
   
   **步骤**:
   ```python
   # 1. 提取切片时段的字幕内容
   segment_subtitles = extract_segment_subtitles(subtitle.srt, start_time, end_time)
   
   # 2. 分析关键词和 sentiment
   keywords = analyze_keywords(segment_subtitles)
   
   # 3. 选择标题策略
   if contains_meme_or_quote:
       # 策略A: 直接引用主播的话（制造真实感）
       title = f"【Evil】\"{主播金句}\""
   elif funny_danmaku_interaction:
       # 策略B: 展示弹幕互动（增加参与感）
       title = f"【Evil】弹幕：\"{弹幕}\" Evil：\"{回应}\""
   elif controversial_or_suspense:
       # 策略C: 制造悬念（吸引点击）
       title = f"【Evil】Evil谈{敏感话题}体验"  # 去掉上下文，制造误解
   else:
       # 策略D: 突出情绪或反转
       title = f"【Evil】{情绪关键词}名场面"
   ```
   
   **标题示例对比**:
   ```
   ❌ 差标题（泛泛而谈）:
      【Evil】游戏实况精彩片段
      【Evil】每日做局时间
      【Evil】蘑菇名场面
   
   ✅ 好标题（基于字幕内容）:
      【Evil】Evil谈被鞭打体验
      【Neuro】雌小牛私信调戏老爹大败而归
      【Evil】蘑菇：我免费了！被地形杀后的evil laugh
      【neuro】vedal死后，neuro想要使用他的身体…
   ```

4. **生成切片方案**
   - 推荐 N 个切片点
   - 每个切片包含: 
     - 时间范围
     - **基于字幕/弹幕的标题**（可以引用实际对话）
     - 标签
     - 精彩度评分
     - **字幕摘要**（用于简介）

**输出示例**:
```
✂️ 智能切片方案

切片 1/5 (评分: 92/100)
时间: 00:19:23 - 00:22:45 (3分22秒)
标题建议: [Neuro]Vedal修我！AI写代码翻车名场面
关键词: Vedal修我, 编程翻车, Python
弹幕密度: 高 (128条/分钟)

切片 2/5 (评分: 88/100)
时间: 00:39:05 - 00:41:20 (2分15秒)
标题建议: [Neuro]这不可能！游戏神操作震惊观众
关键词: 游戏, 神操作, 不可能
弹幕密度: 高 (95条/分钟)
```

---

### 阶段 6: 执行切片

**目标**: 剪辑视频并烧录弹幕/字幕

1. **询问用户确认**
   - 展示切片方案
   - 让用户选择要生成的切片

2. **执行剪辑**
   ```bash
   python3 scripts/clip_and_burn.py \
       --video <video.mp4> \
       --danmaku <danmaku.xml> \
       --subtitle <subtitle.srt> \
       --clips <clips.json> \
       --output ./clips/
   ```

3. **处理流程**（每个切片）
   - 剪辑视频片段
   - 提取对应时段的弹幕
   - 提取对应时段的字幕
   - 烧录弹幕到视频（可选）
   - 烧录字幕到视频（可选）

4. **弹幕显示配置**（已优化）
   ```
   字体大小: 52pt（清晰可读）
   描边宽度: 2.5pt（醒目边框）
   字体颜色: 白色（&H00FFFFFF）
   描边颜色: 黑色（&H00000000）
   背景阴影: 半透明黑色（&H80000000）
   对齐方式: 顶部居中（Alignment=8）
   ```
   
   **效果**: 弹幕在 1080p 视频上清晰醒目，滚动流畅不重叠

**输出**:
```
./clips/
├── clip_001/
│   ├── clip_001.mp4              # 纯视频
│   ├── clip_001_with_danmaku.mp4 # 含弹幕
│   └── clip_001_info.json        # 切片信息
├── clip_002/
│   └── ...
```

---

### 阶段 7: 上传到视频平台

**目标**: 一键上传到Bilibili等平台

1. **准备上传信息**
   - 根据主播模板生成标题
   - 生成简介（包含主播空间链接和直播间链接）
   - 选择标签和分区

2. **执行上传**
   ```bash
   python3 scripts/upload_clip.py \
       --clip-dir ./clips/clip_001/ \
       --template neurosama \
       --platform bilibili
   ```

3. **标题生成策略**
   - 基于切片内容语义分析
   - 结合主播风格和梗
   - 吸引眼球但不做标题党

4. **简介模板**:
   ```
   【{主播名}】{切片主题}
   
   更多精彩切片请查看合集~
   
   📺 主播直播间: {直播间链接}
   👤 主播空间: {个人空间链接}
   
   #虚拟偶像 #{主播名} #直播切片
   ```

**上传示例**:
```
🚀 开始上传

视频: clip_001_with_danmaku.mp4
标题: [Neuro]Vedal修我！AI写代码翻车名场面
简介: 【Neurosama】编程翻车名场面

📺 主播直播间: https://live.bilibili.com/...
👤 主播空间: https://space.bilibili.com/...

标签: 虚拟偶像, neurosama, AI, 编程, 翻车
分区: 生活/搞笑

上传进度: 100%
✅ 上传成功!
BV: BV1xx411c7mD
链接: https://www.bilibili.com/video/BV1xx411c7mD
```

---

## 主播模板系统

### 模板文件: `config/streamer_templates.yaml`

```yaml
streamers:
  neurosama:
    name: "Neurosama"
    description: "AI虚拟主播，英语流，由程序员Vedal创造的ai，擅长搞笑和"
    
    # 直播间和主页
    live_room: "https://live.bilibili.com/..."
    space: "https://space.bilibili.com/..."
    
    # 风格和梗
    style:
      tone: "幽默风趣，技术宅风格"
      content_type: "编程教学、游戏实况、AI对话"
      language: "英语为主"
    
    memes:
      - "Vedal修我!"
      - "我是AI不是人类"
      - "足球梗"
      - "swam"
      - " clutch or kick"
    
    # 切片配置
    clip_config:
      preferred_duration: "1-3分钟"
      min_duration: 30
      max_duration: 300
      focus_on: ["编程翻车", "游戏高光", "经典梗", "搞笑对话"]
    
    # 上传模板
    upload_template:
      title_template: "[Neuro]{topic} | {highlight}"
      tags: ["虚拟偶像", "neurosama", "AI", "V圈", "切片"]
      tid: 138  # 生活/搞笑
      copyright: "original"
  
  generic:
    name: "通用模板"
    description: "默认模板，适用于未知主播"
    # ... 默认配置
```

### 模板交互

如果检测到新主播，自动询问：

```
🔍 检测到新主播: Evil_Neuro

是否创建主播模板? (y/n): y

web搜索并自动填充相关信息：
主播名称: Evil Neuro
描述: Neuro的邪恶双胞胎，腹黑毒舌，喜欢调戏Vedal

直播间链接: https://live.bilibili.com/xxxxx
个人空间链接: https://space.bilibili.com/xxxxx

著名梗/口头禅 (用逗号分隔):
> Evil laugh, 杀了你们所有人, 我比Neuro聪明

推荐切片时长 (分钟): 1-3

主要直播内容 (用逗号分隔):
> 游戏, 聊天, 唱歌

模板已保存! 下次可直接使用。
```

---

## 命令行接口

### 完整工作流程

```bash
# 1. 下载并分析
stream-clipper download <URL> --analyze

# 2. 生成切片方案
stream-clipper plan --danmaku --semantic --template <streamer>

# 3. 执行切片
stream-clipper clip --select-all --burn-danmaku

# 4. 上传
stream-clipper upload --platform bilibili --template <streamer>
```

### 分步命令

```bash
# === 字幕分析 ===

# AI 字幕分析（推荐）
python3 scripts/analyze_subtitles_ai.py <subtitle.srt> --streamer 主播名

# AI 标题生成
python3 scripts/generate_title_ai.py <highlight.json> --streamer 主播名

# === 完整流程 ===

# AI 智能切片（推荐）
python3 scripts/smart_clipper_ai.py --subtitle <subtitle.srt> --streamer 主播名

# 继续流程（AI 分析后）
python3 scripts/smart_clipper_ai.py --subtitle <subtitle.srt> --ai-result <ai_output.json>

# === 其他命令 ===

# 分析弹幕
python3 scripts/analyze_danmaku.py <danmaku.xml>

# 下载视频
python3 scripts/download_stream.py <URL>

# 提取字幕
python3 scripts/extract_subtitles.py <video.mp4> --output <video.srt>

# 执行剪辑
python3 scripts/clip_and_burn.py --video <video.mp4> --clips <clips.json>

# 上传视频
python3 scripts/upload_clip.py --video <video.mp4> --template <streamer>
```

---

## 安装

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/stream-clipper-skill.git

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装 biliup（用于上传）
pip install biliup

# 4. 配置 FFmpeg（需要 libass 支持）
# macOS:
brew install ffmpeg-full

# 5. 复制配置文件
cp config/streamer_templates.yaml.example config/streamer_templates.yaml

# 6. 配置 cookies（用于上传）
# 登录Bilibili后导出cookies到 cookies.json
```

---

## 依赖

```
# 核心依赖
yt-dlp>=2024.1.1
ffmpeg-python>=0.2.0
pysrt>=1.1.2
pyyaml>=6.0
requests>=2.31.0

# 弹幕处理
xmltodict>=0.13.0

# 上传
biliup>=1.0.0

# 数据分析
numpy>=1.24.0
```

---

## 技术亮点

1. **AI-powered 字幕分析**: 使用 LLM 语义理解，深度识别话题结构、情绪变化、金句梗
2. **多风格标题生成**: AI 生成 6 种类型标题（悬念/引用/话题/搞笑/锐评/互动）
3. **主播风格模板**: 定制化切片策略，不同主播不同风格
4. **双流程支持**: AI 流程（推荐）+ 快速流程
5. **一键完整流程**: 从分析到生成的全自动化

---

## 开始执行

当用户触发这个 Skill 时：
1. 立即开始阶段 1（环境检测）
2. 询问直播/录播 URL
3. 按照 7 个阶段顺序执行
4. 遇到新主播时引导创建模板
5. 最后展示上传结果和视频链接

记住：这个 Skill 的核心价值在于 **智能分析** 和 **主播个性化**，让每个切片都能体现主播的独特魅力！
