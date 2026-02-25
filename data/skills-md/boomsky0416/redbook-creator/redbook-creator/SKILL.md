---
name: redbook-creator
description: "Use this skill when the user wants to create Xiaohongshu (小红书/RedBook) posts. Trigger phrases: 小红书创作, create redbook, 小红书, 红书, 笔记创作, 帖子创作. The user will provide images, videos, or text content. This skill analyzes the content, searches for trending Xiaohongshu posts as reference, generates post title and copy, auto-edits videos (merge, subtitles, BGM, narration), attempts auto-upload to Xiaohongshu creator platform, and generates a local preview HTML file."
alwaysApply: false
---

# 小红书创作助手 (RedBook Creator)

帮助用户基于提供的素材（图片/视频/文字）创作小红书爆款帖子，支持自动视频剪辑、字幕、BGM 和 AI 解说。

---

## 依赖工具

本 skill 依赖以下工具，使用前需确认可用：

| 工具 | 用途 | 检查命令 |
|------|------|----------|
| ffmpeg/ffprobe | 视频剪辑/合并/字幕 | `which ffmpeg` |
| edge-tts | AI 语音合成（自然男声/女声） | `python3 -m edge_tts --version` |
| selenium | 自动上传小红书 | `python3 -c "import selenium"` |

**缺失依赖自动安装**：如果 edge-tts 或 selenium 未安装，使用 `pip3 install edge-tts selenium` 安装。

---

## 完整工作流程

当用户触发此 skill 时，严格按以下步骤执行：

### 第一步：素材收集与分析

1. **接收素材**：用户会提供图片、视频或文字内容
2. **分析素材**：
   - 图片：使用 Read 工具查看图片，识别主题、场景、物品、氛围
   - 视频：用 ffprobe 获取视频信息，用 ffmpeg 提取关键帧，再用 Read 工具查看关键帧图片来分析内容
   - 文字：提取核心主题、关键词、情感倾向
3. **确定创作方向**：基于素材确定内容类别（美食、旅行、穿搭、美妆、家居、数码、健身、萌宠、学习、职场等）

### 第二步：爆款参考研究

使用 WebSearch 搜索小红书相关爆款内容：

```
搜索策略：
1. 搜索 "小红书 [主题关键词] 爆款笔记"
2. 搜索 "小红书 [类别] 热门标题"
3. 搜索 "小红书 [主题] 文案模板"
4. 分析搜索结果中的标题模式、文案风格、emoji 使用、标签策略
```

### 第三步：创作帖子内容

#### 标题创作规则（生成 3-5 个备选标题）：
- 字数控制在 **10-20 字**
- 必须包含 **emoji**（至少 2 个）
- 使用以下爆款标题公式之一：
  - 数字型：「5个xxx让你xxx」「xxx的10种方式」
  - 反问型：「为什么xxx都在xxx？」「你还在xxx吗？」
  - 惊叹型：「绝了！xxx竟然xxx」「天花板级别的xxx」
  - 对比型：「xxx vs xxx，结果xxx」
  - 干货型：「xxx保姆级教程」「一文搞懂xxx」
  - 种草型：「人生建议：一定要试试xxx」「后悔没早知道的xxx」
  - 情绪型：「救命！xxx也太xxx了吧」「哭死，xxx居然xxx」

#### 文案创作规则：
- **开头**（黄金 2 行）：用 emoji + 吸引力语句抓住注意力
- **正文**：
  - 每段 2-3 行，段间用 emoji 分隔
  - 使用口语化表达，加入「姐妹们」「家人们」「宝子们」等亲切称呼
  - 适当使用感叹句和反问句增加互动感
  - 干货内容用序号或 emoji 列表呈现
  - 总字数 **200-800 字**（根据内容类型调整）
- **结尾**：引导互动（点赞/收藏/关注/评论）
- **标签**：生成 5-10 个相关标签，格式为 `#标签名`
- **话题**：推荐 2-3 个小红书热门话题

#### 文案格式模板：
```
[emoji] [吸引力开头]

[emoji] [正文段落1]

[emoji] [正文段落2]

[emoji] [正文段落3]
...

[互动引导语句]

---
[#标签1 #标签2 #标签3 ...]
```

### 第四步：视频自动剪辑（如有视频素材）

当用户提供视频素材时，自动执行以下剪辑流程：

#### 4.1 视频合并

当有多个视频时，自动合并为一个视频：

```bash
# 1. 统一规格：所有视频转为 720x1280（小红书竖屏），30fps，libx264
ffmpeg -y -i input.mp4 \
  -vf "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -preset fast -crf 20 -r 30 \
  -c:a aac -ar 44100 -ac 1 -b:a 128k \
  -map 0:v:0 -map 0:a:0 \
  normalized.mp4

# 2. 使用 xfade 渐变过渡合并（0.5秒过渡）
ffmpeg -y -i v1_norm.mp4 -i v2_norm.mp4 \
  -filter_complex "\
    [0:v][1:v]xfade=transition=fade:duration=0.5:offset=<v1时长-0.5>[vout];\
    [0:a][1:a]acrossfade=d=0.5[aout]" \
  -map "[vout]" -map "[aout]" \
  -c:v libx264 -preset fast -crf 20 -c:a aac -b:a 128k \
  merged.mp4
```

**注意事项**：
- 如果视频有旋转元数据（如 iPhone MOV），ffmpeg 会自动处理旋转
- offset 值 = 第一个视频时长 - 过渡时长
- 多个视频按顺序两两合并

#### 4.2 AI 解说旁白

根据视频内容创作 3-5 段解说词，使用 edge-tts 生成自然语音：

```bash
# 生成解说音频（使用微软 YunxiNeural 年轻男声）
python3 -m edge_tts --voice zh-CN-YunxiNeural --rate="+5%" \
  --text "解说文字" \
  --write-media segment.mp3
```

**可用中文语音**：

| 语音ID | 风格 | 适用场景 |
|--------|------|----------|
| zh-CN-YunxiNeural | 年轻男声，自然活力 | 健身、科技、日常vlog（默认首选） |
| zh-CN-YunjianNeural | 成熟男声，沉稳大气 | 知识分享、商务 |
| zh-CN-YunyangNeural | 播音男声，专业 | 新闻播报风格 |
| zh-CN-XiaoxiaoNeural | 年轻女声，甜美 | 美妆、穿搭、美食 |
| zh-CN-XiaoyiNeural | 活泼女声 | 萌宠、生活分享 |

**解说词创作要求**：
- 分 3-5 个片段，每段对应视频的一个阶段
- 语气自然口语化，像朋友聊天
- 每段 10-25 字，不要太长
- 留出呼吸间隔

**解说词时间轴安排**：
- 根据视频总时长均匀分配
- 每段解说之间留 2-3 秒间隔
- 使用 ffmpeg adelay 精确控制每段开始时间

```bash
# 合并解说片段（控制时间点）
ffmpeg -y \
  -i s1.mp3 -i s2.mp3 -i s3.mp3 \
  -filter_complex "\
    [0]adelay=<ms1>|<ms1>[d1];\
    [1]adelay=<ms2>|<ms2>[d2];\
    [2]adelay=<ms3>|<ms3>[d3];\
    [d1][d2][d3]amix=inputs=3:duration=longest:normalize=0,\
    apad=whole_dur=<总时长>,atrim=0:<总时长>[out]" \
  -map "[out]" -c:a pcm_s16le -ar 44100 -ac 1 \
  narration.wav
```

#### 4.3 BGM 背景音乐

使用 Python 生成匹配内容风格的 BGM 节拍：

```bash
python3 ~/.claude/skills/redbook-creator/scripts/generate_bgm.py \
  --style <风格> \
  --duration <秒数> \
  --bpm <节拍> \
  --output bgm.wav
```

**BGM 风格选项**（根据内容类别自动选择，也可询问用户）：

| 风格 | BPM | 适用类别 |
|------|-----|----------|
| energetic | 128 | 健身、运动、挑战 |
| chill | 90 | 日常、穿搭、家居 |
| upbeat | 110 | 美食、旅行、种草 |
| emotional | 75 | 故事、情感、回忆 |

#### 4.4 字幕叠加

将解说词作为字幕烧录到视频上：

```bash
python3 ~/.claude/skills/redbook-creator/scripts/burn_subtitles.py \
  --video merged.mp4 \
  --subtitles "时间1|文字1,时间2|文字2,..." \
  --style xiaohongshu \
  --output subtitled.mp4
```

**字幕样式（小红书风格）**：
- 字体：PingFang SC Bold（macOS 自带）
- 大小：42px
- 颜色：白色，黑色描边（2px）
- 位置：底部居中，距底 15%
- 可选：添加半透明黑色背景条

#### 4.5 最终音频混合

将原始音频、BGM、解说合并：

```bash
ffmpeg -y \
  -i subtitled.mp4 \
  -i bgm.wav \
  -i narration.wav \
  -filter_complex "\
    [0:a]volume=0.2[orig];\
    [1:a]volume=0.15[bgm];\
    [2:a]volume=1.6[narr];\
    [orig][bgm][narr]amix=inputs=3:duration=shortest:normalize=0[aout]" \
  -map 0:v -map "[aout]" \
  -c:v copy -c:a aac -b:a 192k \
  -shortest \
  final.mp4
```

**音量参考**：
- 原始环境音：20%（保留真实感）
- BGM：15%（不抢解说）
- 解说旁白：160%（清晰突出）

### 第五步：上传到小红书创作者平台

**默认行为：自动尝试上传**

使用 Bash 工具运行上传脚本：

```bash
# 先清理之前的 Chrome 会话
pkill -f chromedriver 2>/dev/null
pkill -f "redbook-chrome-profile" 2>/dev/null
sleep 2

python3 ~/.claude/skills/redbook-creator/scripts/upload_redbook.py \
  --title "帖子标题" \
  --content "帖子文案" \
  --tags "标签1,标签2,标签3" \
  --media "最终视频路径"
```

**上传脚本特性**：
- 使用持久化 Chrome 配置（`~/.claude/redbook-chrome-profile`），登录一次后续免登录
- 自动轮询等待登录（无需命令行交互）
- 通过 JavaScript 注入填写标题和正文（支持 emoji）
- 浏览器保持打开（detach），用户确认后手动点击发布
- 如自动上传失败，自动输出手动上传指引

**如果自动上传失败**，输出手动指引：

```
📱 手动上传指引：

方式一：网页端
1. 打开 https://creator.xiaohongshu.com
2. 登录你的小红书账号
3. 点击「发布笔记」
4. 上传视频/图片素材
5. 粘贴标题和文案
6. 添加标签和话题
7. 点击发布

方式二：手机端
1. 打开小红书 App
2. 点击底部「+」号
3. 选择素材 → 粘贴文案 → 发布
```

同时将标题和文案以方便复制的格式输出到终端。

### 第六步：生成本地预览 HTML

使用预览脚本生成 HTML 预览文件：

```bash
python3 ~/.claude/skills/redbook-creator/scripts/generate_preview.py \
  --title "帖子标题" \
  --content "帖子文案（完整带emoji和标签）" \
  --media "最终视频或图片路径" \
  --output "./redbook_preview_YYYYMMDD_HHMMSS.html"
```

生成完成后用 `open` 命令在浏览器中打开预览。

---

## 输出清单

每次创作完成后，确保输出以下内容：

1. **备选标题**（3-5 个）+ 推荐标题
2. **完整文案**（含 emoji、标签、话题）
3. **剪辑后视频**（合并+字幕+BGM+解说）
4. **上传结果**（自动上传成功/手动上传指引）
5. **本地预览文件路径**（HTML 文件）

---

## 注意事项

- 文案风格需要符合小红书平台调性：真实、有温度、种草感
- 避免过度营销感，保持真实分享的语气
- emoji 使用要自然，不堆砌
- 标签选择兼顾热门标签和精准长尾标签
- 如果素材不足，主动向用户询问补充信息
- 所有生成的文件保存在当前工作目录
- 视频输出统一 720x1280 竖屏格式（小红书最佳比例）
- 解说语音默认使用 YunxiNeural 男声，可根据用户偏好切换
- BGM 风格根据内容类别自动匹配，也可询问用户偏好
