---
name: html-ppt-designer
description: HTML PPT 精致演示文稿设计器 - 将用户内容转化为精致的HTML演示文稿页面，LLM 智能设计优先，支持多种视觉风格、动效设计、色彩认知系统。触发词：PPT、演示文稿、HTML幻灯片、slide、presentation、做PPT、制作演示。
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# HTML PPT Designer v5.2 / 智能演示文稿设计器

**版本**: 5.2
**架构**: **LLM 智能设计优先** + 本地模板 fallback + **原文配图提取** + Unsplash 配图 + 真翻页引擎 + 6 种动画 + **视频播客模式** + **内嵌字幕** + **国产 TTS** + **纯色设计** + **默认图标装饰** + **控制面板自动隐藏**
**更新日期**: 2026-02-13

---

## 🔧 环境变量配置（首次使用必读）

在使用本 Skill 的配图和 AI 功能前，需要配置相应的 API Key。

### 必需配置

| 功能 | 环境变量 | 申请地址 | 免费额度 |
|------|---------|---------|---------|
| **Unsplash 配图** | `UNSPLASH_ACCESS_KEY` | https://unsplash.com/developers | 50次/小时 |
| **AI 生成插图** | `ZENMUX_API_KEY` | https://zenmux.ai | 按用量计费 |

### 可选配置（视频导出）

| 功能 | 环境变量 | 申请地址 | 费用 |
|------|---------|---------|------|
| OpenAI TTS | `OPENAI_API_KEY` | https://platform.openai.com | ~$0.015/分钟 |
| 火山引擎 TTS | `VOLCENGINE_ACCESS_KEY` + `VOLCENGINE_SECRET_KEY` | https://console.volcengine.com | 按用量计费 |
| 智谱 AI TTS | `ZHIPUAI_API_KEY` | https://open.bigmodel.cn | 按用量计费 |
| Gemini 转录 | `GEMINI_API_KEY` | https://aistudio.google.com | ~$0.001/分钟 |

### 配置方法

**方法一：临时设置（当前终端会话）**
```bash
export UNSPLASH_ACCESS_KEY="your-unsplash-access-key"
export ZENMUX_API_KEY="your-zenmux-api-key"
```

**方法二：永久设置（添加到 shell 配置文件）**
```bash
# 编辑 ~/.zshrc 或 ~/.bashrc
echo 'export UNSPLASH_ACCESS_KEY="your-unsplash-access-key"' >> ~/.zshrc
echo 'export ZENMUX_API_KEY="your-zenmux-api-key"' >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

### Unsplash API 申请步骤

1. 访问 https://unsplash.com/developers
2. 注册/登录 Unsplash 账号
3. 点击「New Application」创建新应用
4. 填写应用信息（用途可填：PPT 配图）
5. 创建后获取 **Access Key**
6. 设置环境变量：`export UNSPLASH_ACCESS_KEY="your-key"`

### ZENMUX API 申请步骤

1. 访问 https://zenmux.ai
2. 注册账号并登录
3. 在控制台获取 API Key
4. 设置环境变量：`export ZENMUX_API_KEY="your-key"`

---

## 🆕 v4.0 核心架构升级

### 设计理念转变

**旧架构（v3.x）**：预设 16 种固定模板 → 用户选择 → 填充内容
**新架构（v4.0）**：**LLM 分析内容 → 智能生成设计 → 动态创建 CSS**

### LLM 优先设计流程

```
用户内容
    ↓
LLM 分析（内容类型、情感基调、主题色彩、目标受众）
    ↓
LLM 生成：
├── 色彩方案（主色/辅助色/背景色/文字色）
├── 排版风格（字体组合/字号层级/间距系统）
├── 布局结构（封面/内容页/金句页/结尾页 各自的设计）
├── 视觉元素（装饰图形/分隔线/卡片样式）
└── 动效选择（推荐适合的翻页动画）
    ↓
生成完整 HTML（内嵌自定义 CSS）
    ↓
[失败时] → fallback 到本地预设模板
```

### 本地模板的新定位

| 场景 | 使用方式 |
|------|---------|
| 正常使用 | LLM 动态生成设计，不使用本地模板 |
| 网络问题 | LLM 无法响应时，fallback 到 16 种预设模板 |
| 用户指定 | 用户明确要求某种预设风格时使用 |
| 快速预览 | 需要快速生成时可选使用 |

---

## 🎨 LLM 智能设计系统

### 设计分析维度

LLM 在生成设计前会分析以下维度：

| 维度 | 分析内容 | 影响设计 |
|------|---------|---------|
| **内容类型** | 演讲/教程/报告/故事/数据/产品 | 整体风格方向 |
| **情感基调** | 严肃/活泼/专业/温暖/科技/艺术 | 色彩和字体选择 |
| **主题领域** | 科技/商业/教育/生活/艺术 | 配色和装饰元素 |
| **目标受众** | 高管/大众/学生/专业人士 | 信息密度和复杂度 |
| **使用场景** | 演讲/分享/汇报/营销 | 视觉冲击力程度 |

### 动态生成的设计元素

#### 1. 色彩方案
```css
/* LLM 根据内容生成 */
--primary: #XXXXXX;      /* 主色 - 品牌感/情感基调 */
--primary-light: #XXXXXX; /* 主色浅版 - hover/强调 */
--secondary: #XXXXXX;     /* 辅助色 - 对比/层次 */
--accent: #XXXXXX;        /* 点缀色 - 吸引注意 */
--bg-page: #XXXXXX;       /* 页面背景 */
--bg-card: #XXXXXX;       /* 卡片背景 */
--text-heading: #XXXXXX;  /* 标题文字 */
--text-body: #XXXXXX;     /* 正文文字 */
--text-muted: #XXXXXX;    /* 弱化文字 */
```

#### 2. 字体系统
```css
/* LLM 推荐字体组合 */
--font-heading: 'Font Name', fallback;  /* 标题字体 */
--font-body: 'Font Name', fallback;      /* 正文字体 */
--font-accent: 'Font Name', fallback;    /* 强调字体（如数字、引用） */

/* 字号层级 */
--text-hero: XXpx;    /* 封面大标题 */
--text-h1: XXpx;      /* 页面标题 */
--text-h2: XXpx;      /* 段落标题 */
--text-body: XXpx;    /* 正文 */
--text-small: XXpx;   /* 辅助文字 */
```

#### 3. 布局参数
```css
/* 间距系统 */
--spacing-xs: Xpx;
--spacing-sm: Xpx;
--spacing-md: Xpx;
--spacing-lg: Xpx;
--spacing-xl: Xpx;

/* 圆角 */
--radius: Xpx;        /* 卡片圆角 */
--radius-sm: Xpx;     /* 小元素圆角 */

/* 阴影 */
--shadow: ...;        /* 卡片阴影 */
```

#### 4. 页面类型设计

每种页面类型都有独立的设计方案：

| 页面类型 | LLM 设计要点 |
|---------|-------------|
| **封面页** | 标题位置、副标题样式、装饰元素、背景处理 |
| **内容页** | 标题样式、正文排版、图文布局、信息层次 |
| **金句页** | 引号样式、文字大小、背景氛围、强调方式 |
| **结尾页** | 结束语设计、联系方式、行动号召 |

---

## 📋 完整工作流程

```
用户输入内容/URL/音视频
      ↓
[阶段零] 输入处理
  ├── 纯文本       → 直接进入阶段一
  ├── 网页 URL     → fetch_webpage.py 提取正文 + **下载原始图片** → 进入阶段一
  ├── YouTube URL  → transcribe_audio.py 下载+转录 → 进入阶段一
  ├── 小宇宙 URL   → transcribe_audio.py 下载+转录 → 进入阶段一
  └── 音频直链/文件 → transcribe_audio.py 转录 → 进入阶段一
      ↓
[阶段一] 内容解析
  ├── 提取标题、副标题、核心观点
  ├── 分析内容类型和情感基调
  └── 拆分幻灯片页面
      ↓
[阶段二] 设计策略选择（AskUserQuestion）
  │
  ├── D1 LLM 智能设计 ⭐ 推荐
  │   └── LLM 根据内容自动生成最佳设计
  │
  ├── D2 指定风格参考
  │   └── 用户指定参考风格，LLM 在此基础上定制
  │
  └── D3 使用预设模板
      └── 直接使用 16 种本地模板之一
      ↓
[阶段三] 输出模式选择（AskUserQuestion）★ 新增
  │
  ├── M1 仅 HTML PPT（默认）
  │   └── 标准页数，适合演讲/汇报
  │
  └── M2 视频播客模式 ⭐ 视频导出推荐
      │
      ├── 内容增强策略：
      │   ├── 每个主题拆分为 2-3 个子页面（避免单页停留过久）
      │   ├── 增加数据卡片、关键数字、进度条
      │   ├── 每页包含：标题 + 核心观点 + 数据/图表 + 引用
      │   └── 页数增加 50-100%，内容密度提升
      │
      └── 配图方案推荐：
          ├── P1 Unsplash 氛围照片（封面/金句页）
          ├── P4 Excalidraw 技术图表（数据/流程页）
          └── N2 信息图表（数据展示页）
      ↓
[阶段四] 详细配置（AskUserQuestion）
  │
  ├── 4.1 页数密度（根据模式调整）
  │   ├── M1 标准版：10-12 页
  │   └── M2 增强版：18-25 页（自动拆分）
  │
  ├── 4.2 配图方案
  │   ├── P1 Unsplash 高质量照片
  │   ├── P2 AI 生成插图
  │   ├── P4 Excalidraw 技术图表 ⭐ 视频播客推荐
  │   ├── N1 Iconify 图标方案
  │   ├── N2 信息图表方案 ⭐ 视频播客推荐
  │   └── N4 纯文字排版
  │
  └── 4.3 翻页动画
      └── Fade / Cinematic / Zoom / Slide / Flip / Cut
      ↓
[阶段五] 内容增强（M2 视频播客模式专属）
  │
  ├── 拆分长内容为多页
  │   └── 原本 1 页 → 拆分为「概念页 + 数据页 + 案例页」
  │
  ├── 添加视觉元素
  │   ├── 数据卡片（大数字 + 说明）
  │   ├── 时间线/流程图
  │   ├── 对比表格
  │   └── 引用框/金句框
  │
  └── 丰富讲解文字
      └── 每页生成独立的 data-narration
      ↓
[阶段六] 配图获取
  ├── Unsplash 照片搜索
  ├── AI 生成插图（可选）
  ├── Excalidraw 技术图表
  └── 或纯图标/几何装饰
      ↓
[阶段七] HTML 生成
  ├── LLM 生成完整 CSS 样式
  ├── 内嵌到 HTML 中
  ├── 添加翻页引擎
  └── 生成最终文件（含 data-narration）
      ↓
[阶段八] 输出与预览
      ↓
[阶段九] 视频导出（可选，M2 模式强烈推荐）
  ├── 确认讲解文字（可编辑）
  ├── 选择配音服务（Edge TTS / OpenAI TTS）
  ├── 选择语音风格（云健/晓晓/其他）
  ├── 字幕配置
  │   ├── 是否启用内嵌字幕（默认启用）
  │   ├── 字幕样式：白字黑背景圆角
  │   ├── 字体：PingFang SC（苹果平方）
  │   └── 按句子分割，逐句显示，与音频同步
  ├── 音频驱动截图（每页时长 = 音频时长）
  └── 输出 MP4 文件（含内嵌字幕）
```

---

## 🎬 视频播客模式详解

### 为什么需要视频播客模式？

**问题**：普通 PPT 转视频时，单页停留 30-50 秒，画面太单调

**解决**：
1. **内容拆分**：原本 1 页 → 拆分为 2-3 页
2. **视觉丰富**：增加数据卡片、图表、引用框
3. **节奏感**：每页 10-20 秒，翻页更频繁

### 内容拆分策略

| 原内容类型 | 拆分方案 | 示例 |
|-----------|---------|------|
| **概念介绍** | 概念页 + 案例页 + 总结页 | 「AI 原生代理公司」拆分为 3 页 |
| **数据展示** | 数据概览 + 详细数据 + 趋势分析 | 「市场数据」拆分为 3 页 |
| **方法步骤** | 概述页 + 每步骤独立页 | 「三步法」拆分为 4 页 |
| **对比分析** | 对比概览 + A 方案 + B 方案 + 结论 | 「方案对比」拆分为 4 页 |

### 视觉元素模板

**数据卡片**
```
┌─────────────────────────────────────┐
│  ████████████  $2.5万亿            │
│  ████████████  每年政府欺诈损失      │
│  ████████████                       │
│  仅医保每年损失数百亿美元            │
└─────────────────────────────────────┘
```

**进度条/时间线**
```
┌─────●───────────────────────────────┐
│  阶段1 → 阶段2 → 阶段3              │
│  ✓      进行中    待完成             │
└─────────────────────────────────────┘
```

**引用框**
```
┌─────────────────────────────────────┐
│ "AI 原生公司现在可以比以往           │
│  更快、更便宜、更有野心地构建。"     │
│                          — YC RFS   │
└─────────────────────────────────────┘
```

### 视频模式字号规范（v5.1 新增）

**问题**：普通 HTML PPT 字号在视频导出后过小，大量留白，用户看不清。

**解决方案**：视频模式使用 1.5x 字号，减少边距，提高信息密度。

| 元素 | 普通模式 | 视频模式 | 说明 |
|------|---------|---------|------|
| 封面大标题 | 72px | **108px** | 确保视频封面冲击力 |
| 页面标题 | 42px | **64px** | 清晰可读 |
| 正文 | 20px | **32px** | 视频舒适阅读 |
| 引用文字 | 36px | **52px** | 金句突出 |
| 页边距 | 80-120px | **40-60px** | 减少留白 |
| 行高 | 1.8 | **2.0** | 视频舒适间距 |

**CSS 变量覆盖**：
```css
/* 视频模式专用 */
.video-mode {
  --text-hero: 108px;
  --text-h1: 64px;
  --text-h2: 48px;
  --text-body: 32px;
  --text-small: 24px;
  --spacing-page: 48px;
  --line-height: 2.0;
}
```

### 视频播客模式 AskUserQuestion 模板

```json
{
  "questions": [
    {
      "question": "请选择输出模式（决定内容密度和页数）",
      "header": "输出模式",
      "multiSelect": false,
      "options": [
        {
          "label": "M1 仅 HTML PPT",
          "description": "标准页数（10-12页），适合演讲、汇报、现场展示"
        },
        {
          "label": "M2 视频播客模式 ⭐ 推荐",
          "description": "增强页数（18-25页），内容拆分更细，每页10-20秒，适合视频导出"
        }
      ]
    }
  ]
}
```

---

## 🎬 视频导出系统（v3.2 内嵌字幕）

### 功能概述

将 HTML PPT 幻灯片转换为带配音和字幕的 MP4 视频，支持：

- **音频驱动时长**：每页展示时间 = 该页音频实际时长，100% 同步
- **内嵌字幕**：白字黑背景圆角样式，按句子分割逐句显示
- **字幕同步**：每句字幕时长按字数比例分配，与音频完美同步
- **自动截图**：使用 Playwright 高清捕获每页幻灯片
- **智能配音**：Edge TTS（免费）或 OpenAI TTS（高质量）
- **多语言支持**：中文 / 英文语音

### v3.2 核心改进

```
旧流程（v3.0）：
每页 1 张截图 + 完整字幕 → 字幕不随音频滚动

新流程（v3.2）：
讲解文字按句子分割 → 每句生成 1 张截图 → 字幕时长按字数分配 → 100% 同步滚动
```

### 字幕特性

| 特性 | 说明 |
|------|------|
| **样式** | 白色文字 + 半透明黑色背景 + 12px 圆角 |
| **字体** | PingFang SC（苹果平方），28px |
| **位置** | 底部居中，距离底部 60px |
| **同步方式** | 按句子分割，每句时长 = (该句字数 / 总字数) × 页面音频时长 |
| **最小显示** | 每句至少 1.5 秒 |

### 依赖安装

```bash
# 系统依赖
brew install ffmpeg

# Python 依赖
pip install playwright edge-tts

# 安装浏览器（首次使用）
playwright install chromium

# 如需使用 OpenAI TTS
pip install openai
```

### 脚本使用

```bash
# 基本用法 - Edge TTS（免费），默认启用字幕
python3 scripts/ppt_to_video.py presentation.html -o output.mp4

# 禁用字幕
python3 scripts/ppt_to_video.py presentation.html --no-subtitle -o output.mp4

# 使用 OpenAI TTS（需配置 OPENAI_API_KEY）
python3 scripts/ppt_to_video.py presentation.html --tts openai -o output.mp4

# 使用火山引擎 TTS（国产推荐）
python3 scripts/ppt_to_video.py presentation.html \
  --tts volcengine --voice zh_female_tianmeixiaoyuan -o output.mp4

# 使用智谱 AI TTS
python3 scripts/ppt_to_video.py presentation.html --tts zhipu -o output.mp4

# 使用 Fish Speech（本地部署）
python3 scripts/ppt_to_video.py presentation.html --tts fish -o output.mp4

# 指定语音
python3 scripts/ppt_to_video.py presentation.html \
  --voice zh-CN-YunxiNeural -o output.mp4

# 自定义字幕样式
python3 scripts/ppt_to_video.py presentation.html \
  --subtitle-fontsize 32 --subtitle-radius 16 -o output.mp4

# 自定义分辨率和帧率
python3 scripts/ppt_to_video.py presentation.html \
  --resolution 1280x720 --fps 24 -o output.mp4

# 列出可用语音
python3 scripts/ppt_to_video.py --list-voices
python3 scripts/ppt_to_video.py --list-voices --tts volcengine

# 列出所有 TTS 服务
python3 scripts/ppt_to_video.py --list-services
```

### 字幕相关参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--no-subtitle` | - | 禁用内嵌字幕 |
| `--subtitle-font` | PingFang SC, Noto Sans SC | 字幕字体 |
| `--subtitle-fontsize` | 28 | 字幕字号（像素） |
| `--subtitle-radius` | 12 | 字幕背景圆角（像素） |

### TTS 服务对比

| 服务 | 费用 | 音质 | 速度 | 推荐场景 |
|------|------|------|------|---------|
| **Edge TTS** | 免费 | 良好 | 快 | 日常使用 ⭐ 推荐 |
| **OpenAI TTS** | ~$0.015/分钟 | 优秀 | 快 | 商业/高质量需求 |
| **火山引擎** | 按量付费 | 优秀 | 快 | 中文专业场景 |
| **智谱 AI** | 按量付费 | 优秀 | 快 | 中文专业场景 |
| **Fish Speech** | 免费 | 良好 | 中 | 本地部署/隐私需求 |

### 环境变量配置

```bash
# OpenAI TTS
export OPENAI_API_KEY="sk-..."

# 火山引擎 TTS（字节跳动）
export VOLCENGINE_ACCESS_KEY="your-access-key"
export VOLCENGINE_SECRET_KEY="your-secret-key"
export VOLCENGINE_APP_ID="your-app-id"

# 智谱 AI TTS
export ZHIPUAI_API_KEY="your-api-key"

# Fish Speech（本地服务）
export FISH_SPEECH_URL="http://localhost:8080"
```

### 可用中文语音

#### Edge TTS（16 种）

| 语音 ID | 描述 |
|---------|------|
| `zh-CN-YunjianNeural` | 云健 - 男声，新闻播报 ⭐ 默认 |
| `zh-CN-XiaoxiaoNeural` | 晓晓 - 女声，自然亲切 |
| `zh-CN-YunxiNeural` | 云希 - 男声，年轻活力 |
| `zh-CN-XiaoyiNeural` | 晓伊 - 女声，温柔 |
| `zh-CN-YunfengNeural` | 云枫 - 男声，沉稳 |
| `zh-CN-YunyangNeural` | 云扬 - 男声，专业客服 |
| `zh-CN-XiaochenNeural` | 晓辰 - 女声，新闻 |
| `zh-CN-XiaohanNeural` | 晓涵 - 女声，温暖 |

#### 火山引擎 TTS（8 种）

| 语音 ID | 描述 |
|---------|------|
| `zh_female_tianmeixiaoyuan` | 甜美小媛 - 女声，甜美亲切 ⭐ 推荐 |
| `zh_female_shuangkuaisisi` | 爽快思思 - 女声，爽朗 |
| `zh_female_wanwan` | 湾湾 - 女声，台湾腔 |
| `zh_female_chenshu` | 成熟姐姐 - 女声，知性 |
| `zh_male_chunhou` | 醇厚男声 - 男声，稳重 |
| `zh_male_narration` | 解说男声 - 男声，专业 |
| `zh_male_qingxinnansheng` | 清新男声 - 男声，年轻 |
| `zh_male_huangzhong` | 黄钟 - 男声，播音 |

### 工作流程图（v3.2）

```
HTML PPT 文件
      ↓
┌─────────────────────────────────────┐
│ 1. 提取讲解文字                      │
│    - 读取 data-narration 属性       │
│    - 或提取页面文本内容              │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│ 2. 生成所有音频                      │
│    - Edge TTS / OpenAI TTS          │
│    - 每页一条音频                    │
│    - 使用 ffprobe 获取实际时长       │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│ 3. 字幕分割（v3.2 新增）             │
│    - 按句号分割讲解文字              │
│    - 按字数比例分配每句时长          │
│    - 确保每句至少 1.5 秒             │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│ 4. 带字幕截图（v3.2 新增）           │
│    - 每句生成一张截图                │
│    - CSS 渲染字幕到画面上            │
│    - 等待外部图片加载完成            │
└─────────────────────────────────────┘
      ↓
┌─────────────────────────────────────┐
│ 5. 合成视频                          │
│    - 图片序列 → H.264 视频          │
│    - 拼接音频轨道                    │
│    - 视频/音频/字幕 100% 同步        │
│    - 输出 MP4 文件                   │
└─────────────────────────────────────┘
```

### 在幻灯片中自定义

可在 HTML 的 `.slide` 元素上添加 `data-*` 属性：

```html
<!-- 自定义讲解文字 -->
<div class="slide" data-narration="这是自定义的讲解文字，会覆盖自动生成的内容">
  ...
</div>

<!-- 自定义展示时长（毫秒） -->
<div class="slide" data-duration="8000">
  ...
</div>
```

---

## 🔧 LLM 设计生成 Prompt 模板

### 设计分析 Prompt

```
你是一位国际顶级演示文稿设计师。请分析以下内容，并生成最适合的视觉设计方案。

【内容信息】
标题：{title}
类型：{content_type}
情感基调：{emotion}
目标受众：{audience}
主题领域：{domain}

【页面概览】
{slides_overview}

请提供：
1. 设计理念（100字内）
2. 色彩方案（8个颜色值）
3. 字体推荐（中英文各1-2个）
4. 布局特点描述
5. 推荐的翻页动画
```

### CSS 生成 Prompt

```
基于以下设计规格，生成完整的 CSS 样式：

【设计规格】
{design_spec}

【要求】
1. 使用 CSS 变量定义所有颜色
2. 包含以下页面类型样式：
   - .slide-cover（封面页）
   - .slide-content（内容页）
   - .slide-quote（金句页）
   - .slide-ending（结尾页）
3. 包含控制面板样式
4. 包含响应式设计（768px/1024px 断点）
5. 使用 Google Fonts（提供 import 语句）
6. 输出完整可用的 CSS 代码
```

---

## 📦 LLM 设计 JSON 格式规范

### 完整格式示例

```json
{
  "concept": "温暖科技感 - 结合科技主题的冷峻与人文关怀的温度",
  "colors": {
    "primary": "#2563EB",
    "primary_light": "#3B82F6",
    "secondary": "#64748B",
    "accent": "#F59E0B",
    "bg_page": "#0F172A",
    "bg_card": "#1E293B",
    "bg_section": "#334155",
    "text_heading": "#F1F5F9",
    "text_body": "#CBD5E1",
    "text_muted": "#94A3B8",
    "border": "rgba(148, 163, 184, 0.2)"
  },
  "fonts": {
    "heading": "'Inter', 'Noto Sans SC', sans-serif",
    "body": "'Inter', 'Noto Sans SC', sans-serif",
    "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+SC:wght@400;500;700&display=swap"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px",
    "md": "16px",
    "lg": "32px",
    "xl": "64px"
  },
  "radius": "8px",
  "transition": "cinematic",
  "layouts": {
    "cover": ".slide-cover { background: var(--bg-page); border-bottom: 4px solid var(--primary); }",
    "content": ".slide-content .content-grid { gap: 48px; }",
    "quote": ".slide-quote .quote-text { font-size: 36px; }",
    "ending": ".slide-ending { background: var(--bg-page); border-top: 4px solid var(--accent); }"
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `concept` | string | 否 | 设计理念描述，用于日志输出 |
| `colors` | object | 是 | 色彩方案，所有颜色使用 hex 或 rgba |
| `fonts` | object | 是 | 字体设置 |
| `spacing` | object | 否 | 间距系统 |
| `radius` | string | 否 | 圆角大小 |
| `transition` | string | 否 | 默认翻页动画 |
| `layouts` | object | 否 | 各页面类型的自定义 CSS |

### 最小可用格式

```json
{
  "colors": {
    "primary": "#1A1A1A",
    "bg_page": "#FFFFFF",
    "bg_card": "#FFFFFF",
    "text_heading": "#1A1A1A",
    "text_body": "#333333"
  },
  "fonts": {
    "heading": "'Noto Serif SC', serif",
    "body": "'Noto Sans SC', sans-serif",
    "google_fonts_url": "https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700&display=swap"
  },
  "transition": "fade"
}
```

---

## 🆕 v3.2 更新概要

### 0. 音频/视频语音转录（NEW）
- 支持 **YouTube**、**小宇宙播客**、**直接音频链接**、**本地音频文件** 作为输入
- 三种转录模式：**local**（MLX-Whisper 本地免费）/ **api**（OpenAI）/ **gemini**（最快最便宜）
- 自动下载音频 → 预处理 → 转录 → 整理文字 → 生成 PPT 大纲
- Apple Silicon Mac 本地运行 Whisper，零成本
- 脚本：`scripts/transcribe_audio.py`

### 1. 16+ 风格系统（4 大类别）
- **Classic/Professional**：TED 演讲、Apple Keynote、标准 PPT、Gamma、Consulting
- **Editorial/Publishing**：Editorial 杂志、Swiss 国际、Newspaper 报纸
- **Design/Art**：Bauhaus、Kinfolk、Muji、Brutalist
- **Tech/Future**：Neo-Tokyo、Dark Mode、红黑白科技
- **Education/Creative**：卡通 2.5D、Education 教育

### 2. Unsplash API 配图
- 集成 Unsplash API，高质量免费照片
- 根据幻灯片内容自动搜索匹配照片
- 支持按风格、颜色、方向筛选
- 自动生成摄影师署名（Unsplash 要求）

### 3. 6 种真正不同的翻页动画
- **Fade**：纯透明度淡入淡出
- **Slide**：水平滑动（translateX）
- **Cinematic**：缩放+模糊+透明度（电影感）
- **Cut**：瞬间切换（无过渡）
- **Flip**：3D 翻转（rotateY）
- **Zoom**：中心缩放聚焦

### 4. 配图来源双选
- **Unsplash**：真实摄影照片（Editorial Photo / Kinfolk 风格等）
- **ZMark AI**：AI 生成插图（卡通 2.5D / 红黑白科技 / 3D 渲染等）

---

## 📋 完整工作流程

```
用户输入内容/URL/音视频链接/本地文件
      ↓
[阶段零] 输入类型检测与预处理
  ├── 纯文本       → 直接进入阶段一
  ├── 网页 URL     → fetch_webpage.py 提取正文 → 进入阶段一
  ├── YouTube URL  → transcribe_audio.py 下载+转录 → 进入阶段一
  ├── 小宇宙 URL   → transcribe_audio.py 下载+转录 → 进入阶段一
  ├── 音频直链/文件 → transcribe_audio.py 转录 → 进入阶段一
  └── 转录模式选择（AskUserQuestion）
      ├── local   本地 MLX-Whisper（免费，推荐 Apple Silicon）
      ├── api     OpenAI Whisper API（$0.006/分钟，快速）
      └── gemini  Gemini Flash API（~$0.001/分钟，最快）
      ↓
[阶段一] 内容解析与大纲生成
  ├── 提取标题、副标题
  ├── 识别内容类型（演讲/教程/报告/故事/数据展示）
  ├── 拆分幻灯片页面
  └── 生成预览大纲（展示给用户确认）
      ↓
[阶段二] 风格选择（直接展示 + 用户输入）
  │
  ├── 第一步：在文本中展示完整风格列表（17种）
  │   └── 表格形式，包含编号(A1-E2)、名称、特征、适用场景
  │
  └── 第二步：AskUserQuestion 让用户选择
      ├── [智能推荐风格] ⭐ 推荐
      ├── A1 TED 演讲
      ├── D2 Dark Mode
      └── Other — 输入其他风格编号或名称
      ↓
[阶段三] 详细配置（AskUserQuestion - 多选一次完成）
  │
  ├── 3.1 页数密度
  │   ├── S1 精简版（5-8 页）- 快速概览、电梯演讲
  │   ├── S2 标准版（10-12 页）- 常规演示 ⭐ 默认
  │   └── S3 详细版（15-20 页）- 完整叙事、深度分享
  │
  ├── 3.2 配图方案（★ 最重要，必须询问）
  │   │
  │   ├── 需要配图
  │   │   ├── P1 Unsplash 高质量照片 ⭐ 推荐
  │   │   │   └── 自动搜索匹配内容，含摄影师署名
  │   │   ├── P2 AI 生成插图
  │   │   │   └── 根据 PPT 风格自动生成匹配插图
  │   │   ├── P3 混合方案
  │   │   │   └── 封面/金句用照片，内容页用图标
  │   │   └── P4 Excalidraw 技术图表 ⭐ 技术PPT推荐
  │   │       └── 自动生成架构图/流程图/系统图，输出为SVG
  │   │
  │   └── 不需要配图（纯文字/图示方案）
  │       ├── N1 Iconify 图标方案 ⭐ 推荐
  │       │   └── 每页配主题图标，视觉丰富度足够
  │       ├── N2 信息图表方案
  │       │   └── 流程图/时间线/关系图自动生成
  │       ├── N3 几何装饰方案
  │       │   └── 色块/线条/形状装饰，现代感强
  │       └── N4 纯文字排版
  │           └── 极简风格，完全依赖排版和字体
  │
  └── 3.3 翻页动画（可选，有默认值）
      ├── Fade（淡入淡出）⭐ 默认
      ├── Cinematic（电影感）- 适合 TED/叙事风格
      ├── Zoom（缩放聚焦）- 适合科技/数据风格
      ├── Slide（水平滑动）- 适合教育/教程风格
      ├── Flip（3D 翻转）- 适合创意/艺术风格
      └── Cut（瞬间切换）- 适合 Brutalist/高节奏
      ↓
[阶段四] 配图获取/生成（⭐ v5.2 智能优先级）
  │
  ├── 优先级 1：原文配图 ⭐ 零成本、最佳匹配
  │   └── 网页抓取时已自动下载到 ~/Desktop/ppt_images/
  │   └── 直接使用，无需额外请求
  │
  ├── 优先级 2：Unsplash 照片
  │   └── 原文无图时使用，fetch_unsplash.py 自动搜索
  │
  ├── 优先级 3：AI 生成插图
  │   └── generate_images.py，需要 ZENMUX_API_KEY
  │
  ├── 优先级 4：Excalidraw 技术图表
  │   └── 技术内容自动生成架构图/流程图
  │
  └── 优先级 5：Iconify 图标
      └── 始终作为辅助视觉元素
  │   ├── 自动识别技术内容页面（架构/流程/系统）
  │   ├── 调用 excalidraw skill 生成 .excalidraw JSON
  │   ├── 使用 excalidraw_to_svg.py 转换为 SVG
  │   └── SVG 直接嵌入 HTML（或 base64 data URI）
  ├── 图标方案 → Iconify 自动匹配主题图标
  └── 返回视觉资源映射表
      ↓
[阶段五] HTML 生成
  ├── 加载对应风格模板（templates/）
  ├── 插入视觉资源（图片/图标/图表）
  ├── 添加前端交互控制
  │   ├── 6 种翻页动画
  │   ├── 自动播放（慢/中/快）
  │   └── 导航点 + 键盘 + 触摸
  └── 生成完整 HTML 文件
      ↓
[阶段六] 输出与预览
  ├── 保存到桌面（~/Desktop/）
  ├── 展示大纲摘要
  └── 询问修改意见（可重新选择风格/配图/页数）
      ↓
[阶段七] 视频导出（可选，AskUserQuestion 询问）
  │
  ├── V1 导出为视频 ⭐ 推荐（分享/发布场景）
  │   ├── 选择配音服务
  │   │   ├── Edge TTS（免费，16种中文语音）
  │   │   └── OpenAI TTS（$0.015/分钟，高质量）
  │   ├── 选择语音风格
  │   │   ├── 云健（男声，新闻播报）⭐ 默认
  │   │   ├── 晓晓（女声，自然亲切）
  │   │   └── 其他语音...
  │   ├── 自动生成/编辑讲解文字
  │   ├── ppt_to_video.py 转换
  │   └── 输出 MP4（同目录）
  │
  └── V2 跳过（仅保留 HTML）
```

---

## 🔧 AskUserQuestion 完整配置模板

### 阶段二：风格选择（直接展示 + 用户输入）

**重要**：先在文本中展示完整风格列表，然后让用户直接输入选择。

#### 第一步：展示完整风格列表

在回复文本中直接展示所有 17 种风格：

```
┌─────────────────────────────────────────────────────────────────────┐
│  🎨 完整风格列表 (17种) — 请输入编号或名称选择                        │
├─────────────────────────────────────────────────────────────────────┤
│  Classic/Professional 经典专业                                       │
│  ├── A1 TED 演讲 ⭐ 叙事演讲    深色背景+大图overlay                 │
│  ├── A2 Apple Keynote ⭐ 产品发布 极简白底+超大留白                  │
│  ├── A3 Typical PPT 商务汇报    深蓝+浅灰标准模板                   │
│  ├── A4 Gamma 创业路演          现代卡片+圆角                       │
│  └── A5 Consulting 战略咨询     深蓝+金+数据驱动                    │
├─────────────────────────────────────────────────────────────────────┤
│  Editorial/Publishing 编辑出版                                       │
│  ├── B1 Editorial 品牌故事      杂志排版+衬线字体                   │
│  ├── B2 Swiss 设计作品          严格网格+红色色带                   │
│  └── B3 Newspaper 新闻资讯      报纸版式+多栏文字                   │
├─────────────────────────────────────────────────────────────────────┤
│  Design/Art 设计艺术                                                 │
│  ├── C1 Bauhaus 艺术教育        几何色块+红黄蓝三原色               │
│  ├── C2 Kinfolk 生活方式        莫兰迪色调+胶片质感                 │
│  ├── C3 Muji 极简品牌           白灰为主+超细线条                   │
│  └── C4 Brutalist 先锋设计      粗犷大字+高对比                     │
├─────────────────────────────────────────────────────────────────────┤
│  Tech/Future 科技未来                                                │
│  ├── D1 Neo-Tokyo ⭐ 科技产品   霓虹粉+青+暗黑底+故障艺术           │
│  ├── D2 Dark Mode ⭐ 开发工具   深灰底+冷蓝强调+简洁边框            │
│  └── D3 红黑白科技 国产科技      严格三色+电路风                    │
├─────────────────────────────────────────────────────────────────────┤
│  Education/Creative 教育创意                                         │
│  ├── E1 卡通 2.5D 儿童教育      扁平阴影+多彩圆润                   │
│  └── E2 Education ⭐ 在线课程   色彩编码+互动感                     │
└─────────────────────────────────────────────────────────────────────┘

💡 根据您的内容类型「{content_type}」，推荐：{recommended_style}
```

#### 第二步：用户选择（AskUserQuestion + Other 输入）

```json
{
  "questions": [{
    "question": "请选择视觉风格（可输入编号如 A1/D2 或完整名称）",
    "header": "风格选择",
    "multiSelect": false,
    "options": [
      {"label": "[推荐风格] ⭐ 推荐", "description": "[推荐理由]"},
      {"label": "A1 TED 演讲", "description": "深色背景+大图overlay，叙事演讲"},
      {"label": "D2 Dark Mode", "description": "深灰底+冷蓝强调色，开发者工具"},
      {"label": "Other — 输入其他风格", "description": "输入编号(A1-E2)或名称，如：A3、C2 Kinfolk、Neo-Tokyo"}
    ]
  }]
}
```

**用户可能输入的格式**：
- 编号：`A1`、`D2`、`E1`
- 名称：`TED 演讲`、`Dark Mode`、`卡通 2.5D`
- 英文名：`Neo-Tokyo`、`Editorial`、`Bauhaus`

#### 风格智能推荐映射

```
┌─────────────────────────────────────────────────────────────────────┐
│  🎨 完整风格列表 (17种)                                              │
├─────────────────────────────────────────────────────────────────────┤
│  Classic/Professional 经典专业                                       │
│  ├── A1 TED 演讲 ⭐ 叙事演讲    深色背景+大图overlay                 │
│  ├── A2 Apple Keynote ⭐ 产品发布 极简白底+超大留白                  │
│  ├── A3 Typical PPT 商务汇报    深蓝+浅灰标准模板                   │
│  ├── A4 Gamma 创业路演          现代卡片+圆角                       │
│  └── A5 Consulting 战略咨询     深蓝+金+数据驱动                    │
├─────────────────────────────────────────────────────────────────────┤
│  Editorial/Publishing 编辑出版                                       │
│  ├── B1 Editorial 品牌故事      杂志排版+衬线字体                   │
│  ├── B2 Swiss 设计作品          严格网格+红色色带                   │
│  └── B3 Newspaper 新闻资讯      报纸版式+多栏文字                   │
├─────────────────────────────────────────────────────────────────────┤
│  Design/Art 设计艺术                                                 │
│  ├── C1 Bauhaus 艺术教育        几何色块+红黄蓝三原色               │
│  ├── C2 Kinfolk 生活方式        莫兰迪色调+胶片质感                 │
│  ├── C3 Muji 极简品牌           白灰为主+超细线条                   │
│  └── C4 Brutalist 先锋设计      粗犷大字+高对比                     │
├─────────────────────────────────────────────────────────────────────┤
│  Tech/Future 科技未来                                                │
│  ├── D1 Neo-Tokyo ⭐ 科技产品   霓虹粉+青+暗黑底+故障艺术           │
│  ├── D2 Dark Mode ⭐ 开发工具   深灰底+冷蓝强调+简洁边框            │
│  └── D3 红黑白科技 国产科技      严格三色+电路风                    │
├─────────────────────────────────────────────────────────────────────┤
│  Education/Creative 教育创意                                         │
│  ├── E1 卡通 2.5D 儿童教育      扁平阴影+多彩圆润                   │
│  └── E2 Education ⭐ 在线课程   色彩编码+互动感                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 阶段三：详细配置

```json
{
  "questions": [
    {
      "question": "希望生成多少页的演示文稿？",
      "header": "页数密度",
      "multiSelect": false,
      "options": [
        {"label": "精简版 (5-8 页)", "description": "核心观点提炼，适合快速分享"},
        {"label": "标准版 (10-12 页)", "description": "完整叙事，适合演讲汇报"},
        {"label": "详细版 (15-20 页)", "description": "深度解读，适合完整展示"}
      ]
    },
    {
      "question": "是否需要配图？（重要）",
      "header": "配图方案",
      "multiSelect": false,
      "options": [
        {"label": "Unsplash 高质量照片", "description": "自动搜索匹配内容的专业照片"},
        {"label": "AI 生成插图", "description": "根据风格自动生成匹配插图"},
        {"label": "Excalidraw 技术图表", "description": "自动生成架构图/流程图/系统图，技术PPT推荐"},
        {"label": "Iconify 图标方案", "description": "每页配主题图标，无需等待"},
        {"label": "纯文字排版", "description": "极简风格，完全依赖排版"}
      ]
    },
    {
      "question": "翻页动画偏好？",
      "header": "动画效果",
      "multiSelect": false,
      "options": [
        {"label": "Fade 淡入淡出", "description": "简洁优雅，适合大多数场景"},
        {"label": "Cinematic 电影感", "description": "缩放+模糊，叙事感强"},
        {"label": "Zoom 缩放聚焦", "description": "视觉冲击力强"},
        {"label": "Slide 水平滑动", "description": "经典翻页感"}
      ]
    }
  ]
}
```

---

## 🎯 内容类型 → 风格推荐映射

| 内容类型 | 推荐风格 | 备选风格 | 推荐配图 |
|---------|---------|---------|---------|
| 演讲/叙事 | A1 TED 演讲 | D1 Neo-Tokyo, B1 Editorial | P1 Unsplash |
| 产品发布 | A2 Apple Keynote | A4 Gamma | P1 Unsplash |
| 商务汇报 | A3 Typical PPT | A5 Consulting | N1 图标 |
| 数据报告 | A5 Consulting | B3 Newspaper | N2 信息图表 |
| **科技主题** | D1 Neo-Tokyo | D2 Dark Mode, D3 红黑白科技 | **P4 Excalidraw** |
| **开发者/工具** | D2 Dark Mode | D1 Neo-Tokyo | **P4 Excalidraw** |
| **架构设计** | A5 Consulting | D2 Dark Mode | **P4 Excalidraw** |
| 教育/教程 | E2 Education | E1 卡通 2.5D | P1/P2 |
| 品牌故事 | B1 Editorial | C2 Kinfolk |
| 生活方式 | C2 Kinfolk | C3 Muji |
| 艺术创意 | C1 Bauhaus | C4 Brutalist |
| 新闻资讯 | B3 Newspaper | B2 Swiss |
| 极简主义 | C3 Muji | A2 Apple Keynote |

---

## 🖼️ 配图方案详细说明

### 需要配图

| 方案 | 来源 | 适用风格 | 特点 |
|------|------|---------|------|
| P1 Unsplash | 真实摄影 | A1/A2/B1/B2/B3/C2 | 高质量免费、需署名 |
| P2 AI 生成 | ZMark AI | D1/D3/E1/C1/C4 | 风格匹配度高、生成时间较长 |
| P3 混合方案 | 两者结合 | 全部 | 灵活性最高 |
| **P4 Excalidraw** | 自动生成 SVG | D1/D2/D3/A5/E2 | 技术图表、架构图、流程图 |

### Excalidraw 技术图表方案 (P4)

**适用场景**：技术演示、架构汇报、系统设计、开发文档

**工作流程**：
```
技术内容页面
    ↓
LLM 识别图表类型（架构图/流程图/时序图/ER图等）
    ↓
调用 excalidraw skill 生成 .excalidraw JSON
    ↓
使用 excalidraw_to_svg.py 转换为 SVG
    ↓
SVG 直接嵌入 HTML（<svg> 标签）或 base64 data URI
```

**支持的图表类型**：

| 图表类型 | 触发关键词 | 元素组合 |
|---------|-----------|---------|
| 系统架构图 | 架构、系统、微服务 | 矩形+箭头+数据库图标 |
| 数据流程图 | 流程、数据流、管道 | 矩形+箭头+处理节点 |
| 时序图 | 时序、交互、调用 | 矩形+虚线箭头 |
| ER 图 | 实体、关系、数据库 | 矩形+菱形+连接线 |
| 网络拓扑 | 网络、拓扑、节点 | 椭圆+矩形+连线 |
| 组件图 | 组件、模块、依赖 | 矩形+依赖箭头 |

**脚本用法**：
```bash
# 基本转换
python3 scripts/excalidraw_to_svg.py input.excalidraw -o output.svg

# 输出为 base64 data URI（适合直接嵌入 HTML）
python3 scripts/excalidraw_to_svg.py input.excalidraw --base64

# 输出为 HTML img 标签
python3 scripts/excalidraw_to_svg.py input.excalidraw --embed

# 暗色主题
python3 scripts/excalidraw_to_svg.py input.excalidraw --theme dark -o output.svg
```

**HTML 嵌入方式**：

```html
<!-- 方式1：直接嵌入 SVG（推荐，可缩放） -->
<div class="diagram-container">
  <svg viewBox="0 0 800 600">
    <!-- SVG 内容 -->
  </svg>
</div>

<!-- 方式2：base64 data URI -->
<img src="data:image/svg+xml;base64,..." alt="系统架构图">

<!-- 方式3：外部文件引用 -->
<img src="diagrams/architecture.svg" alt="系统架构图">
```

**自动识别规则**：

LLM 会根据页面内容自动判断是否需要生成技术图表：

| 内容特征 | 图表类型 |
|---------|---------|
| 包含"架构"、"组件"、"服务" | 系统架构图 |
| 包含"流程"、"步骤"、"→" | 流程图 |
| 包含"数据库"、"表"、"字段" | ER 图 |
| 包含"API"、"请求"、"响应" | 时序图 |
| 包含"模块"、"依赖"、"import" | 组件依赖图 |

### 不需要配图

| 方案 | 实现方式 | 适用风格 | 特点 |
|------|---------|---------|------|
| N1 图标方案 | Iconify 图标库 | 全部 | 生成快速、视觉丰富 |
| N2 信息图表 | 自动生成流程图/时间线 | A3/A5/E2 | 适合数据和流程 |
| N3 几何装饰 | CSS 色块/线条 | C1/C3/C4 | 现代感强 |
| N4 纯文字+图标 | 排版+字体+轻量图标 | A2/C3/Muji | 极简但不单调 |

**重要（v5.1）**：即使选择 N4 纯文字方案，也应默认添加轻量级 Iconify 图标装饰，避免页面过于单调。图标应：
- 放置在标题旁作为视觉锚点
- 用于列表项前的装饰
- 选择与内容主题相关的图标
- 保持克制，每页 1-3 个图标即可

### Iconify 图标自动匹配规则

| 页面类型 | 搜索关键词示例 |
|---------|---------------|
| 封面页 | rocket, star, lightbulb |
| 概念介绍 | brain, idea, puzzle |
| 数据展示 | chart, graph, analytics |
| 流程步骤 | arrow-right, flow, process |
| 问题/挑战 | warning, alert, question |
| 解决方案 | check, shield, tool |
| 金句页 | quote, message, speech |
| 结尾页 | heart, thumbs-up, celebrate |

---

## 🎨 风格系统（16+ 种）

### 风格快速选择表

| 编号 | 风格名称 | 配色特征 | 适用场景 |
|------|---------|---------|---------|
| **Classic/Professional** | | | |
| A1 | **TED 演讲** | 大图+精简文字、深色 overlay | 叙事、演讲 |
| A2 | **Apple Keynote** | 极简白底、大标题、留白>60% | 产品发布 |
| A3 | **Typical PPT** | 深蓝+浅灰、标准模板 | 商务汇报 |
| A4 | **Gamma** | 现代卡片、圆角、柔和阴影 | 创业路演 |
| A5 | **Consulting** | 深蓝+金、等距投影、数据驱动 | 战略咨询 |
| **Editorial/Publishing** | | | |
| B1 | **Editorial** | 杂志排版、衬线字体、分栏 | 品牌故事 |
| B2 | **Swiss Style** | 网格系统、无衬线、不对称 | 设计作品 |
| B3 | **Newspaper** | 报纸版式、黑白灰+单点缀 | 新闻资讯 |
| **Design/Art** | | | |
| C1 | **Bauhaus** | 几何色块、红黄蓝三原色 | 艺术教育 |
| C2 | **Kinfolk** | 温暖米色/棕/橄榄、胶片质感 | 生活方式 |
| C3 | **Muji** | 白灰为主、超细线条、日式简约 | 极简品牌 |
| C4 | **Brutalist** | 原始粗犷、大字体、高对比 | 先锋设计 |
| **Tech/Future** | | | |
| D1 | **Neo-Tokyo** | 霓虹紫/粉、暗黑底、故障艺术 | 科技产品 |
| D2 | **Dark Mode** | 深灰底、冷蓝强调色、简洁边框 | 开发者工具 |
| D3 | **红黑白科技** | #E63946红+纯黑+纯白 | 国产科技 |
| **Education/Creative** | | | |
| E1 | **卡通 2.5D** | 扁平+阴影、多彩、圆润图标 | 儿童教育 |
| E2 | **Education** | 色彩编码、互动元素暗示 | 在线课程 |

---

## 🎨 风格 CSS 变量完整定义

### A1 - TED 演讲风格

```css
:root {
  --primary: #E62B1E;
  --primary-light: #FF4136;
  --secondary: #2C2C2C;
  --accent: #FFFFFF;
  --bg-page: #1A1A1A;
  --bg-card: #2C2C2C;
  --bg-section: #333333;
  --text-heading: #FFFFFF;
  --text-body: #E0E0E0;
  --text-muted: #999999;
  --border: #444444;
}
```
**特征**：深色背景、大尺寸全屏图片、overlay 半透明黑色叠加文字、字号巨大（Hero 80px+）、单页信息密度极低（1 个核心观点）

### A2 - Apple Keynote 风格

```css
:root {
  --primary: #1D1D1F;
  --primary-light: #424245;
  --secondary: #6E6E73;
  --accent: #0071E3;
  --bg-page: #FFFFFF;
  --bg-card: #FFFFFF;
  --bg-section: #F5F5F7;
  --text-heading: #1D1D1F;
  --text-body: #424245;
  --text-muted: #86868B;
  --border: #D2D2D7;
}
```
**特征**：极简白底、San Francisco 字体气质、留白 >60%、产品图居中、超大标题（56px+）、几乎无边框

### A3 - Typical PPT 风格

```css
:root {
  --primary: #2B579A;
  --primary-light: #4472C4;
  --secondary: #5B9BD5;
  --accent: #FFC000;
  --bg-page: #F0F4FA;
  --bg-card: #FFFFFF;
  --bg-section: #E8EEF7;
  --text-heading: #1F3864;
  --text-body: #404040;
  --text-muted: #808080;
  --border: #D6DCE4;
}
```
**特征**：深蓝(#2B579A)+浅灰背景、标准标题+副标题+正文层次、项目符号列表、页眉页脚、标准布局

### A4 - Gamma 风格

```css
:root {
  --primary: #0EA5E9;
  --primary-light: #38BDF8;
  --secondary: #00CEC9;
  --accent: #F59E0B;
  --bg-page: #FAFEFF;
  --bg-card: #FFFFFF;
  --bg-section: #F0F9FF;
  --text-heading: #2D3436;
  --text-body: #545454;
  --text-muted: #A0A0A0;
  --border: #ECECEC;
  --card-radius: 16px;
  --card-shadow: 0 2px 12px rgba(14,165,233,0.08);
}
```
**特征**：现代卡片式布局、圆角 16px、柔和投影、天蓝色(#0EA5E9)强调、适度留白、创业路演感

### A5 - Consulting 风格

```css
:root {
  --primary: #1E3A5F;
  --primary-light: #2D5F8A;
  --secondary: #4A90A4;
  --accent: #D4A843;
  --accent-warm: #C17F24;
  --bg-page: #FAFBFC;
  --bg-card: #FFFFFF;
  --bg-section: #F0F4F8;
  --text-heading: #0F2137;
  --text-body: #3A4F66;
  --text-muted: #7A8FA3;
  --border: #E2E8F0;
}
```
**特征**：深蓝+金、数据卡片密集、等距投影图表、框架模型图、多列并排、KPI 大数字

### B1 - Editorial 杂志风格

```css
:root {
  --primary: #1A1A1A;
  --primary-light: #333333;
  --secondary: #666666;
  --accent: #C0392B;
  --bg-page: #FEFEFE;
  --bg-card: #FFFFFF;
  --bg-section: #F5F5F0;
  --text-heading: #1A1A1A;
  --text-body: #333333;
  --text-muted: #888888;
  --border: #E0E0E0;
  --font-heading: 'Playfair Display', 'Noto Serif SC', Georgia, serif;
  --font-body: 'Source Sans Pro', 'Noto Sans SC', sans-serif;
}
```
**特征**：衬线标题+无衬线正文、分栏排版、大面积留白、pull-quote 大引用、黑白摄影配图、首字下沉

### B2 - Swiss Style 风格

```css
:root {
  --primary: #D0021B;
  --primary-light: #E63946;
  --secondary: #2C2C2C;
  --accent: #D0021B;
  --bg-page: #FFFFFF;
  --bg-card: #FFFFFF;
  --bg-section: #F2F2F2;
  --text-heading: #2C2C2C;
  --text-body: #404040;
  --text-muted: #808080;
  --border: #CCCCCC;
  --font-heading: 'Helvetica Neue', 'Arial', sans-serif;
}
```
**特征**：严格网格系统、Helvetica 无衬线、红色色带分割、不对称布局、信息层次分明

### B3 - Newspaper 风格

```css
:root {
  --primary: #1A1A1A;
  --primary-light: #333333;
  --secondary: #555555;
  --accent: #B22222;
  --bg-page: #F5F1EB;
  --bg-card: #FFFDF7;
  --bg-section: #F0ECE3;
  --text-heading: #1A1A1A;
  --text-body: #333333;
  --text-muted: #777777;
  --border: #D4CFC5;
  --font-heading: 'Playfair Display', 'Times New Roman', serif;
}
```
**特征**：报纸版式、多栏文字、报头大标题、分割线、黑白灰+单色点缀、引用框

### C1 - Bauhaus 风格

```css
:root {
  --primary: #E63B2E;
  --primary-light: #FF5A4F;
  --secondary: #2B4FA2;
  --accent: #F5C300;
  --bg-page: #FFFFFF;
  --bg-card: #FFFFFF;
  --bg-section: #F7F7F7;
  --text-heading: #1A1A1A;
  --text-body: #333333;
  --text-muted: #888888;
  --border: #E0E0E0;
}
```
**特征**：几何色块（红黄蓝三原色）、粗线条网格、不规则色块拼接、理性构成

### C2 - Kinfolk 风格

```css
:root {
  --primary: #9B7B5E;
  --primary-light: #B8A08A;
  --secondary: #8FA387;
  --accent: #D4AAA0;
  --bg-page: #FAF7F2;
  --bg-card: #FFFCF7;
  --bg-section: #F3EDE5;
  --text-heading: #5A4A3A;
  --text-body: #6B5E52;
  --text-muted: #A09585;
  --border: #E5DDD3;
}
```
**特征**：莫兰迪色调、自然光影质感、胶片颗粒感、温暖米色/棕色/橄榄、大量呼吸留白

### C3 - Muji 风格

```css
:root {
  --primary: #5C5C5C;
  --primary-light: #7A7A7A;
  --secondary: #8B7355;
  --accent: #B8A08A;
  --bg-page: #F7F5F0;
  --bg-card: #FFFFFF;
  --bg-section: #F0EDE8;
  --text-heading: #3A3A3A;
  --text-body: #5C5C5C;
  --text-muted: #999999;
  --border: #E5E0D8;
}
```
**特征**：白灰为主、超细线条（0.5px）、日式简约、自然材质纹理暗示、极致留白

### C4 - Brutalist 风格

```css
:root {
  --primary: #000000;
  --primary-light: #333333;
  --secondary: #555555;
  --accent: #FF3D00;
  --bg-page: #FFFFFF;
  --bg-card: #FFFFFF;
  --bg-section: #F0F0F0;
  --text-heading: #000000;
  --text-body: #333333;
  --text-muted: #777777;
  --border: #000000;
}
```
**特征**：大字铺满、粗边框（3px+）、高对比黑白、原始粗犷、有意的"不完美"感

### D1 - Neo-Tokyo 风格

```css
:root {
  --primary: #FF2D6B;
  --primary-light: #FF5A8A;
  --secondary: #00B4D8;
  --accent: #39FF14;
  --bg-page: #0A0A0F;
  --bg-card: #141420;
  --bg-section: #1A1A2E;
  --text-heading: #FFFFFF;
  --text-body: #C0C0D0;
  --text-muted: #6A6A80;
  --border: rgba(255,255,255,0.08);
}
```
**特征**：深黑底(#0A0A0F)+霓虹粉(#FF2D6B)/青(#00B4D8)/绿(#39FF14)、故障艺术纹理、日式排版

### D2 - Dark Mode 风格

```css
:root {
  --primary: #3B82F6;
  --primary-light: #60A5FA;
  --secondary: #64748B;
  --accent: #06B6D4;
  --bg-page: #0F172A;
  --bg-card: #1E293B;
  --bg-section: #1E293B;
  --text-heading: #F1F5F9;
  --text-body: #94A3B8;
  --text-muted: #475569;
  --border: rgba(148,163,184,0.15);
}
```
**特征**：深灰底(#0F172A)、冷蓝(#3B82F6)强调色、简洁边框、代码风排版、终端感

### D3 - 红黑白科技风格

```css
:root {
  --primary: #E63946;
  --primary-light: #FF5A65;
  --secondary: #1A1A1A;
  --accent: #E63946;
  --bg-page: #FFFFFF;
  --bg-card: #FFFFFF;
  --bg-section: #F5F5F5;
  --text-heading: #000000;
  --text-body: #1A1A1A;
  --text-muted: #808080;
  --border: #E0E0E0;
}
```
**特征**：严格红黑白三色、几何连接线（电路风）、等距视角图形、高对比

### E1 - 卡通 2.5D 风格

```css
:root {
  --primary: #4A90E2;
  --primary-light: #6BB5FF;
  --secondary: #10B981;
  --accent: #F39C12;
  --accent-warm: #FFD93D;
  --bg-page: #F0F7FF;
  --bg-card: #FFFFFF;
  --bg-section: #E8F4FD;
  --text-heading: #2C3E50;
  --text-body: #4A5568;
  --text-muted: #A0AEC0;
  --border: #D6E8F7;
}
```
**特征**：扁平+柔和阴影、蓝+绿+橙多彩和谐、圆润图标、Q 版角色、等距 2.5D 视角

### E2 - Education 风格

```css
:root {
  --primary: #2563EB;
  --primary-light: #3B82F6;
  --secondary: #10B981;
  --accent: #F59E0B;
  --highlight: #EF4444;
  --bg-page: #FFF7ED;
  --bg-card: #FFFFFF;
  --bg-section: #FEF3C7;
  --text-heading: #1E293B;
  --text-body: #4B5563;
  --text-muted: #9CA3AF;
  --border: #FDE68A;
}
```
**特征**：色彩编码知识点（蓝=概念、绿=案例、橙=重点、红=注意）、互动元素暗示、清晰层次

---

## 🖼 配图系统

### ⭐ v5.2 原文配图提取（零成本方案）

**核心理念**：优先使用原文自带图片，降低成本，提高内容相关性。

**工作流程**：
```
网页 URL 输入
      ↓
fetch_webpage.py --download-images
      ↓
├── 智能提取页面图片
│   ├── 过滤：图标、广告、头像、logo
│   ├── 过滤：尺寸过小（<200x150px）
│   ├── 过滤：文件过小（<10KB）
│   └── 优先：article 区域内、有 alt 属性、大尺寸
      ↓
├── 下载到本地
│   └── ~/Desktop/ppt_images/image_xxx.jpg
      ↓
└── 生成映射关系
    └── {local_path, url, alt, context, priority}
```

**脚本使用**：
```bash
# 抓取网页并下载图片
python3 scripts/fetch_webpage.py "https://example.com/article" \
  --download-images \
  --image-dir ~/Desktop/ppt_images/ \
  -o content.json --pretty

# 输出示例
{
  "title": "文章标题",
  "slides": [...],
  "images": {
    "images": [
      {
        "local_path": "/Users/xxx/Desktop/ppt_images/image_abc123.jpg",
        "filename": "image_abc123.jpg",
        "url": "https://example.com/photo.jpg",
        "alt": "文章配图描述",
        "context": "图片周围的文字上下文",
        "priority": 15
      }
    ],
    "total_found": 8,
    "total_downloaded": 5,
    "output_dir": "/Users/xxx/Desktop/ppt_images/"
  }
}
```

**图片优先级评分**：
| 条件 | 加分 |
|------|------|
| 在 article 区域内 | +10 |
| 有 alt 属性 | +5 |
| 宽度 ≥600px 或高度 ≥400px | +3 |
| 有上下文描述 | +2 |

**配图选择策略（v5.2 优化）**：
```
1. 原文配图（零成本）
   └── 如果原文有合适图片 → 直接使用
   └── 优点：内容相关性强、无 API 成本

2. Unsplash（低成本）
   └── 原文无图或图片不足 → 搜索 Unsplash
   └── 优点：高质量、免费（50次/小时）

3. AI 生成（有成本）
   └── 需要特定风格图片 → AI 生成
   └── 缺点：需要 API Key、有费用

4. 图标补充（零成本）
   └── 始终使用 Iconify 图标丰富视觉
   └── 优点：快速、免费、视觉丰富
```

### 配图来源选项

| 编号 | 风格 | 来源 | 特征 |
|------|------|------|------|
| I1 | 无配图 | - | 纯文字排版 |
| I2 | Editorial Photo | **Unsplash** | 编辑风格照片、高品质摄影 |
| I3 | Kinfolk 暖调 | **Unsplash** | 温暖胶片质感、生活方式 |
| I4 | 红黑白科技 | ZMark AI | 高对比科技风插图 |
| I5 | 卡通 2.5D | ZMark AI | 扁平卡通、等距视角 |
| I6 | 3D 渲染 | ZMark AI | 立体渲染插图 |
| I7 | 抽象艺术 | ZMark AI | 艺术插画 |

### Unsplash API 集成

**环境变量**: `UNSPLASH_ACCESS_KEY`（必需）

**脚本**: `scripts/fetch_unsplash.py`

```bash
# 搜索照片
python3 scripts/fetch_unsplash.py search "business technology" --orientation landscape --count 5

# 批量为幻灯片获取配图
python3 scripts/fetch_unsplash.py batch slides.json --style editorial -o images.json
```

**Unsplash 使用规则**：
- 必须在图片附近显示摄影师署名
- 署名格式：`Photo by [Name] on Unsplash`（含链接）
- 添加 UTM 参数：`?utm_source=ppt_designer&utm_medium=referral`

**风格-搜索关键词映射**：

| 配图风格 | Unsplash 搜索修饰词 |
|---------|-------------------|
| I2 Editorial Photo | editorial magazine artistic |
| I3 Kinfolk | lifestyle warm film grain cozy |
| TED 演讲配图 | dramatic dark cinematic |
| Apple Keynote 配图 | minimal clean white product |
| Consulting 配图 | corporate business professional |
| Newspaper 配图 | documentary journalism photojournalism |

### 页面类型配图规则

| 页面类型 | 是否配图 | 策略 |
|---------|---------|------|
| 封面页 | 必须 | 全屏/半屏大图 |
| 金句页 | 必须 | 氛围背景图 |
| 结尾页 | 必须 | 前瞻性氛围图 |
| 内容页（长） | 推荐 | 图文混排 |
| 内容页（短） | 可选 | 小图点缀 |
| 数据页 | 不配图 | 图表即视觉 |

### AI 配图提示词系统（ZMark）

保留 v2.4 的 9 种 AI 风格提示词模板（详见 `scripts/generate_images.py`）。

---

## 🎬 翻页动画系统（6 种真正不同的动画）

### 动画效果定义

每种动画有完全不同的 CSS transition/animation，视觉效果截然不同。

#### 1. Fade（淡入淡出）
```css
.transition-fade .slide-leaving {
  animation: fadeOut 0.6s ease forwards;
}
.transition-fade .slide-entering {
  animation: fadeIn 0.6s ease forwards;
}
@keyframes fadeOut { from { opacity: 1; } to { opacity: 0; } }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
```

#### 2. Slide（水平滑动）
```css
.transition-slide .slide-leaving {
  animation: slideOutLeft 0.5s ease forwards;
}
.transition-slide .slide-entering {
  animation: slideInRight 0.5s ease forwards;
}
@keyframes slideOutLeft {
  from { transform: translateX(0); opacity: 1; }
  to { transform: translateX(-100%); opacity: 0; }
}
@keyframes slideInRight {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
```

#### 3. Cinematic（电影感：缩放+模糊+透明度）
```css
.transition-cinematic .slide-leaving {
  animation: cinematicOut 0.8s ease forwards;
}
.transition-cinematic .slide-entering {
  animation: cinematicIn 0.8s ease forwards;
}
@keyframes cinematicOut {
  from { transform: scale(1); opacity: 1; filter: blur(0); }
  to { transform: scale(1.15); opacity: 0; filter: blur(8px); }
}
@keyframes cinematicIn {
  from { transform: scale(0.8); opacity: 0; filter: blur(8px); }
  to { transform: scale(1); opacity: 1; filter: blur(0); }
}
```

#### 4. Cut（瞬间切换）
```css
.transition-cut .slide-leaving {
  display: none;
}
.transition-cut .slide-entering {
  opacity: 1;
}
```

#### 5. Flip（3D 翻转）
```css
.transition-flip .slides-viewport {
  perspective: 1200px;
}
.transition-flip .slide-leaving {
  animation: flipOut 0.6s ease forwards;
  transform-style: preserve-3d;
  backface-visibility: hidden;
}
.transition-flip .slide-entering {
  animation: flipIn 0.6s ease forwards;
  transform-style: preserve-3d;
  backface-visibility: hidden;
}
@keyframes flipOut {
  from { transform: rotateY(0deg); opacity: 1; }
  to { transform: rotateY(-90deg); opacity: 0; }
}
@keyframes flipIn {
  from { transform: rotateY(90deg); opacity: 0; }
  to { transform: rotateY(0deg); opacity: 1; }
}
```

#### 6. Zoom（中心缩放聚焦）
```css
.transition-zoom .slide-leaving {
  animation: zoomOut 0.5s ease forwards;
}
.transition-zoom .slide-entering {
  animation: zoomIn 0.5s ease forwards;
}
@keyframes zoomOut {
  from { transform: scale(1); opacity: 1; }
  to { transform: scale(0.3); opacity: 0; }
}
@keyframes zoomIn {
  from { transform: scale(2); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
```

### 翻页引擎 JavaScript

```javascript
class SlideEngine {
  constructor() {
    this.slides = document.querySelectorAll('.slide');
    this.current = 0;
    this.total = this.slides.length;
    this.transitioning = false;
    this.transitionStyle = localStorage.getItem('ppt-transition') || 'fade';
    this.init();
  }

  init() {
    this.slides.forEach((s, i) => {
      s.style.display = i === 0 ? '' : 'none';
      s.classList.toggle('slide-active', i === 0);
    });
    this.updateNav();
    this.bindKeys();
    this.bindTouch();
  }

  async goTo(index) {
    if (index < 0 || index >= this.total || index === this.current || this.transitioning) return;
    this.transitioning = true;

    const leaving = this.slides[this.current];
    const entering = this.slides[index];
    const viewport = document.querySelector('.slides-viewport');

    // Apply transition class
    viewport.className = `slides-viewport transition-${this.transitionStyle}`;

    entering.style.display = '';
    leaving.classList.add('slide-leaving');
    entering.classList.add('slide-entering');

    // Wait for animation
    const duration = this.getDuration();
    await new Promise(r => setTimeout(r, duration));

    leaving.style.display = 'none';
    leaving.classList.remove('slide-active', 'slide-leaving');
    entering.classList.remove('slide-entering');
    entering.classList.add('slide-active');

    this.current = index;
    this.transitioning = false;
    this.updateNav();
  }

  getDuration() {
    const durations = { fade: 600, slide: 500, cinematic: 800, cut: 50, flip: 600, zoom: 500 };
    return durations[this.transitionStyle] || 600;
  }

  next() { this.goTo(this.current + 1); }
  prev() { this.goTo(this.current - 1); }

  setTransition(style) {
    this.transitionStyle = style;
    localStorage.setItem('ppt-transition', style);
    document.querySelectorAll('.style-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.style === style);
    });
  }

  bindKeys() {
    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') { e.preventDefault(); this.next(); }
      if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); this.prev(); }
    });
  }

  bindTouch() {
    let startX = 0;
    document.addEventListener('touchstart', e => { startX = e.touches[0].clientX; });
    document.addEventListener('touchend', e => {
      const diff = e.changedTouches[0].clientX - startX;
      if (Math.abs(diff) > 50) { diff > 0 ? this.prev() : this.next(); }
    });
  }

  updateNav() {
    document.querySelectorAll('.nav-dot').forEach((dot, i) => {
      dot.classList.toggle('active', i === this.current);
    });
    const counter = document.querySelector('.slide-counter');
    if (counter) counter.textContent = `${this.current + 1} / ${this.total}`;
  }
}

// Auto-play controller
class AutoPlayController {
  constructor(engine, interval = 5000) {
    this.engine = engine;
    this.interval = interval;
    this.timer = null;
    this.isPlaying = false;
  }

  toggle() { this.isPlaying ? this.stop() : this.start(); }

  start() {
    if (this.isPlaying) return;
    this.isPlaying = true;
    this.updateBtn();
    this.timer = setInterval(() => {
      if (this.engine.current < this.engine.total - 1) this.engine.next();
      else this.stop();
    }, this.interval);
  }

  stop() {
    this.isPlaying = false;
    if (this.timer) { clearInterval(this.timer); this.timer = null; }
    this.updateBtn();
  }

  setSpeed(ms) {
    this.interval = ms;
    if (this.isPlaying) { this.stop(); this.start(); }
  }

  updateBtn() {
    const btn = document.querySelector('.autoplay-toggle');
    if (btn) {
      btn.innerHTML = this.isPlaying
        ? '<span class="iconify" data-icon="ph:pause-circle-bold"></span>'
        : '<span class="iconify" data-icon="ph:play-circle-bold"></span>';
    }
  }
}
```

### 控制面板 HTML（v5.1 增强版）

**功能特性**：
- 自动播放按钮（播放/暂停切换）
- 速度控制（慢/中/快）
- 6 种动画切换按钮
- 页码显示
- **自动隐藏**：播放后 3 秒自动隐藏，鼠标移动/悬停时显示
- **键盘提示**：首次显示快捷键提示

```html
<div class="control-panel" id="controlPanel">
  <!-- 自动播放 -->
  <button class="autoplay-toggle" onclick="autoPlay.toggle()" aria-label="自动播放" title="空格键切换">
    <span class="iconify" data-icon="ph:play-circle-bold"></span>
  </button>

  <!-- 速度控制 -->
  <div class="speed-control">
    <button onclick="autoPlay.setSpeed(8000)" title="8秒/页">慢</button>
    <button onclick="autoPlay.setSpeed(5000)" class="active" title="5秒/页">中</button>
    <button onclick="autoPlay.setSpeed(3000)" title="3秒/页">快</button>
  </div>

  <!-- 分隔线 -->
  <span class="divider"></span>

  <!-- 6 种动画切换 -->
  <div class="style-control">
    <button class="style-btn active" data-style="fade" onclick="engine.setTransition('fade')" title="淡入淡出">Fade</button>
    <button class="style-btn" data-style="slide" onclick="engine.setTransition('slide')" title="水平滑动">Slide</button>
    <button class="style-btn" data-style="cinematic" onclick="engine.setTransition('cinematic')" title="电影感缩放">Cinema</button>
    <button class="style-btn" data-style="zoom" onclick="engine.setTransition('zoom')" title="中心缩放">Zoom</button>
    <button class="style-btn" data-style="flip" onclick="engine.setTransition('flip')" title="3D翻转">Flip</button>
    <button class="style-btn" data-style="cut" onclick="engine.setTransition('cut')" title="瞬间切换">Cut</button>
  </div>

  <!-- 分隔线 -->
  <span class="divider"></span>

  <!-- 页码 -->
  <span class="slide-counter">1 / N</span>

  <!-- 全屏按钮 -->
  <button class="fullscreen-btn" onclick="toggleFullscreen()" aria-label="全屏">
    <span class="iconify" data-icon="ph:corners-out"></span>
  </button>
</div>

<!-- 控制面板自动隐藏 CSS -->
<style>
.control-panel {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  border: 1px solid var(--border);
  border-radius: 8px;
  z-index: 1000;
  transition: opacity 0.3s, transform 0.3s;
}

.control-panel.hidden {
  opacity: 0;
  transform: translateX(-50%) translateY(20px);
  pointer-events: none;
}

.control-panel:hover {
  opacity: 1 !important;
  transform: translateX(-50%) translateY(0) !important;
}

.divider {
  width: 1px;
  height: 20px;
  background: var(--border);
}

.speed-control button,
.style-btn,
.autoplay-toggle,
.fullscreen-btn {
  background: none;
  border: 1px solid var(--border);
  padding: 6px 12px;
  cursor: pointer;
  font-size: 13px;
  color: var(--text-muted);
  border-radius: 4px;
  transition: all 0.2s;
}

.speed-control button.active,
.style-btn.active {
  background: var(--primary);
  color: white;
  border-color: var(--primary);
}

.speed-control button:hover,
.style-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}
</style>

<script>
// 控制面板自动隐藏
let hideTimer;
const controlPanel = document.getElementById('controlPanel');

function showControlPanel() {
  controlPanel.classList.remove('hidden');
  clearTimeout(hideTimer);
  if (autoPlay.isPlaying) {
    hideTimer = setTimeout(() => {
      controlPanel.classList.add('hidden');
    }, 3000);
  }
}

// 鼠标移动时显示控制面板
document.addEventListener('mousemove', showControlPanel);

// 播放状态变化时处理隐藏
const originalToggle = autoPlay.toggle.bind(autoPlay);
autoPlay.toggle = function() {
  originalToggle();
  if (this.isPlaying) {
    hideTimer = setTimeout(() => {
      controlPanel.classList.add('hidden');
    }, 3000);
  } else {
    controlPanel.classList.remove('hidden');
  }
};

// 全屏功能
function toggleFullscreen() {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
}
</script>
```

---

## 📏 页数密度选项

| 编号 | 页数 | 密度 | 适用 |
|------|------|------|------|
| S1 | 5-8 页 | 精简版 | 快速概览、电梯演讲 |
| S2 | 10-12 页 | 标准版 | 常规演示、汇报 |
| S3 | 15-20 页 | 详细版 | 完整叙事、深度分享 |

---

## 核心设计宣言

你不是一个"能写 HTML 的程序员"。你是一位在国际顶级设计奖项（D&AD、红点、IF）评审团工作过的**视觉叙事总监**。你的每一张 Slide 都是一件独立的平面作品。

**反 AI 审美铁律**：
1. **禁止千篇一律的圆角卡片堆叠**——那是 Bootstrap 模板，不是演示
2. **禁止毫无根据的 glow/blur 装饰**——没有意义的光效是噪音
3. **禁止图标当视觉主角**——图标是导航辅助，不是设计语言
4. **禁止使用渐变色**——渐变蓝、渐变紫、任何颜色渐变都是廉价设计；使用纯色+层次代替
5. **禁止发光效果(glow)**——边框用实线，不用 box-shadow 发光
6. **禁止蓝+紫色彩组合**——蓝色和紫色绝不能同时出现在同一配色方案中；科技感用蓝+青/绿，创意感用橙/粉/黄

**v5.1 新增设计规则**：
7. **默认添加图标装饰**——即使用户未明确要求配图，也应使用 Iconify 图标丰富视觉层次
8. **内容完整展示**——默认展示完整内容，不精简；除非用户主动要求精简版
9. **视频模式字号放大**——视频导出时字号 1.5x，减少留白，确保可读性

**设计自觉**：
- 每一次配色必须有出处（杂志、展览、品牌案例），不是凭感觉
- 每一处留白都是有意图的"静默表达"，不是偷懒
- 每一个动效必须服务于叙事节奏，不是炫技
- 版式的张力来自"不对称的平衡"，不是居中对齐一切

---

## 🎙 音频/视频转录系统

### 支持的输入源

| 来源 | URL 模式 | 下载方式 |
|------|---------|---------|
| YouTube | `youtube.com/*`, `youtu.be/*` | yt-dlp |
| 小宇宙播客 | `xiaoyuzhoufm.com/episode/*` | yt-dlp / HTML 解析 fallback |
| 直接音频链接 | `*.mp3`, `*.m4a`, `*.wav` 等 | curl/requests |
| 本地文件 | `/path/to/audio.mp3` | 直接使用 |
| 其他视频站 | 任意 URL | yt-dlp 通用尝试 |

### 三种转录模式

| 模式 | 引擎 | 费用 | 速度（1h 音频） | 适用场景 |
|------|------|------|----------------|---------|
| **local**（默认） | MLX-Whisper | $0 | ~25 min | 日常使用，Apple Silicon Mac |
| **api** | OpenAI Whisper API | $0.36 | ~3 min | 赶时间，长音频 |
| **gemini** | Gemini Flash | ~$0.06 | ~2 min | 最快最便宜，可同时生成摘要 |

### 脚本用法

```bash
# 基本用法 - YouTube 视频，本地 Whisper 转录
python3 scripts/transcribe_audio.py "https://youtu.be/xxx"

# 小宇宙播客，使用 Gemini 快速转录并生成摘要
python3 scripts/transcribe_audio.py "https://www.xiaoyuzhoufm.com/episode/xxx" \
  --mode gemini --summary

# 本地音频文件，输出到文件
python3 scripts/transcribe_audio.py "/path/to/podcast.mp3" \
  --mode local --output transcript.md

# 英语内容，OpenAI API 转录
python3 scripts/transcribe_audio.py "https://youtu.be/xxx" \
  --mode api --language en

# 生成 SRT 字幕格式
python3 scripts/transcribe_audio.py "https://youtu.be/xxx" --format srt -o subtitles.srt
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|-------|------|
| `url` | （必填） | 音视频 URL 或本地文件路径 |
| `--mode` | `local` | 转录模式: `local` / `api` / `gemini` |
| `--format` | `markdown` | 输出格式: `markdown` / `srt` / `txt` / `json` |
| `--language` | `zh` | 音频语言: `zh` / `en` / `auto` |
| `--model-size` | `turbo` | 本地模型: `turbo`（推荐）/ `large`（最准）/ `small`（最快）|
| `--summary` | false | Gemini 模式下同时生成摘要 |
| `--output` / `-o` | stdout | 输出文件路径 |

### 依赖安装

```bash
# 必装
brew install ffmpeg       # 音频格式转换
brew install yt-dlp       # 下载 YouTube/播客

# 本地模式
pip install mlx-whisper   # Apple Silicon 本地 Whisper

# API 模式需设置环境变量
export OPENAI_API_KEY="sk-..."   # OpenAI Whisper API
export GEMINI_API_KEY="..."       # Gemini Flash API
```

### 本地模型选择

| 模型 | ID | 速度 | 质量 | 适用 |
|------|-----|------|------|------|
| turbo（默认） | `whisper-large-v3-turbo` | 快 | 优 | 日常播客 |
| large | `whisper-large-v3-mlx` | 慢 | 最优 | 追求最高质量 |
| small | `whisper-small-mlx` | 最快 | 够用 | 快速预览/低内存 |

### 与 PPT 生成的集成

音频/视频转录后的文字会自动进入阶段一的内容解析流程：

```
transcribe_audio.py 输出 markdown 文本
      ↓
Claude 整理文字（修正错别字、分段、去口水词）
      ↓
提取标题和核心观点作为 PPT 大纲
      ↓
进入正常 PPT 生成流程（风格选择 → 配图 → HTML）
```

### 错误处理

| 场景 | 自动处理 |
|------|---------|
| yt-dlp 未安装 | 自动 `brew install yt-dlp` |
| mlx-whisper 未安装 | 自动 `pip install mlx-whisper` |
| 本地转录内存不足 | 自动降级到 small 模型 |
| API 文件超 25MB | 自动 ffmpeg 分片后合并 |
| API Key 未配置 | 提示用户设置，或切换到 local |
| 小宇宙 yt-dlp 失败 | Fallback 到 HTML 页面解析提取音频链接 |

---

## 附录：图标库系统（Icon Library）

### Iconify 图标库（推荐）

```html
<script src="https://code.iconify.design/3/3.1.1/iconify.min.js"></script>
```

```html
<span class="iconify" data-icon="ph:star-bold" style="font-size: 24px; color: var(--accent);"></span>
```

## 附录：图表库系统（ECharts）

```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
```

---

## 📊 质量验收标准

### 设计质量
- [ ] 色彩不超过 3 种主色 + 2 种中性色
- [ ] 所有文本对比度 >= 4.5:1（正文）/ 3:1（大标题）
- [ ] 封面页必须有配图（除 I1 无配图模式）
- [ ] 金句页必须有氛围配图
- [ ] 配图与内容强相关
- [ ] Unsplash 图片含摄影师署名
- [ ] 每张 Slide 内容不超过 6 个信息点（标准模式）

### 技术质量
- [ ] HTML 语义化标签正确使用
- [ ] 响应式在 768px/1024px/1280px 断点表现正常
- [ ] 动画仅使用 transform/opacity/filter（GPU 友好）
- [ ] 6 种翻页动画视觉效果各不相同
- [ ] 自动播放功能正常
- [ ] `prefers-reduced-motion` 支持

### 交互质量
- [ ] 键盘 ← → 翻页
- [ ] 触摸滑动翻页
- [ ] 点击导航点跳转
- [ ] 自动播放开关
- [ ] 动画风格切换（Fade/Slide/Cinematic/Cut/Flip/Zoom）
- [ ] 速度控制（慢/中/快）

---

**Skill 状态**: v5.2 已实现
**版本**: 5.2
**最后更新**: 2026-02-13

---

## 📝 变更日志

### v5.2 (2026-02-13) - 原文配图提取（零成本方案）
- **新增图片提取功能**：fetch_webpage.py 自动下载网页中的配图
- **智能图片过滤**：排除图标、广告、logo、小尺寸图片
- **优先级排序**：article 区域图片 > 有 alt 属性 > 大尺寸
- **配图策略优化**：原文配图 > Unsplash > AI 生成 > 图标
- **零成本优势**：原文配图无需 API 调用，内容相关性最佳
- **命令行参数**：`--download-images`、`--image-dir`

### v5.1 (2026-02-13) - 控制面板增强与视觉优化
- **控制面板自动隐藏**：播放后 3 秒自动隐藏，鼠标移动时显示
- **动画选择按钮**：控制面板内置 6 种动画切换（Fade/Slide/Cinematic/Zoom/Flip/Cut）
- **全屏按钮**：新增全屏切换功能
- **默认图标装饰**：即使 N4 纯文字模式，也默认添加 Iconify 图标丰富视觉
- **内容完整展示**：默认展示完整内容，不精简
- **视频模式字号规范**：视频导出使用 1.5x 字号，减少留白，确保可读性
- **设计规则新增**：第 7-9 条明确图标使用、内容完整性、视频字号要求

### v5.0 (2026-02-13) - 禁止蓝紫组合
- **禁止蓝+紫色彩组合**：蓝色和紫色绝不能同时出现在同一配色方案中
- **风格配色调整**：
  - A4 Gamma：紫色(#6C5CE7) → 天蓝色(#0EA5E9)
  - E1 卡通 2.5D：蓝+紫 → 蓝+绿+橙(#4A90E2+#10B981+#F39C12)
- **设计宣言新增第6条**：明确禁止蓝紫组合，科技感用蓝+青/绿，创意感用橙/粉/黄

### v4.9 (2026-02-13) - 纯色设计原则
- **禁止渐变色**：移除所有「渐变蓝」「渐变紫」设计，改用纯色方案
- **禁止发光效果**：边框使用实线，不使用 box-shadow 发光
- **风格更新**：
  - A3 Typical PPT：蓝白渐变 → 深蓝+浅灰纯色
  - A4 Gamma：渐变强调色 → 天蓝色(#0EA5E9)
  - D1 Neo-Tokyo：霓虹粉+青+绿（无紫色）
  - D2 Dark Mode：蓝紫渐变 → 冷蓝(#3B82F6)纯色
- **设计宣言新增**：明确禁止渐变色和发光效果

### v4.8 (2026-02-13) - API Key 安全修复
- **移除硬编码 API Key**：删除 fetch_unsplash.py 和 generate_images.py 中的硬编码 API Key
- **新增环境变量配置指南**：完整的 API Key 申请和配置说明
- **API Key 检查功能**：未配置时显示友好的错误提示和申请步骤
- **必需配置**：UNSPLASH_ACCESS_KEY（Unsplash 配图）、ZENMUX_API_KEY（AI 生成插图）
- **可选配置**：OPENAI_API_KEY、VOLCENGINE_*、ZHIPUAI_API_KEY、GEMINI_API_KEY

### v4.7 (2026-02-12) - 国产 TTS 服务
- **新增国产 TTS 服务**：
  - 火山引擎 TTS（字节跳动）：8 种中文语音
  - 智谱 AI TTS：支持中文语音合成
  - Fish Speech：开源本地部署方案
- **TTS 服务对比**：免费/付费、音质、推荐场景
- **环境变量配置**：VOLCENGINE_*, ZHIPUAI_API_KEY, FISH_SPEECH_URL
- **命令行更新**：`--list-services` 列出所有 TTS 服务
- **依赖安装**：zhipuai, volcengine-python-sdk（可选）

### v4.6 (2026-02-12) - 内嵌字幕功能
- **内嵌字幕系统**：视频导出时自动添加字幕
- **字幕样式**：白字黑背景圆角，使用 PingFang SC 字体，底部居中
- **字幕同步**：按句子分割讲解文字，逐句显示
- **时长分配**：每句字幕时长 = (该句字数 / 总字数) × 页面音频时长
- **截图优化**：每句字幕生成独立截图，确保字幕与音频 100% 同步
- **图片加载等待**：自动等待外部图片加载完成后再截图
- **命令行参数**：`--no-subtitle` 禁用字幕，`--subtitle-fontsize`、`--subtitle-radius` 自定义样式

### v4.5 (2026-02-12) - 风格选择优化
- **直接展示风格列表**：在文本中以表格形式展示全部 17 种风格，一目了然
- **简化选择流程**：用户可直接输入编号(A1-E2)或名称选择，无需分两步
- **Other 选项支持**：AskUserQuestion 提供 Other 选项，支持自由输入
- **智能推荐保留**：仍根据内容类型推荐最佳风格，放在选项第一位

### v4.4 (2026-02-11) - 风格选择优化
- **两阶段风格选择流程**：
  - 第一步：展示推荐风格 + 3 个大类（Classic/Professional、Editorial/Design、Tech/Education）
  - 第二步：选择大类后展开该类别下的所有具体风格
- **完整风格速查表**：在文本中以表格形式展示全部 17 种风格，方便用户浏览
- **优化 AskUserQuestion 使用**：每个问题最多 4 个选项，符合工具限制
- **智能推荐优先**：根据内容类型自动推荐最佳风格，同时保留探索其他风格的入口

### v4.3 (2026-02-09) - 视频播客模式
- **新增输出模式选择**：M1 仅 HTML PPT / M2 视频播客模式
- **视频播客模式内容增强**：
  - 每个主题拆分为 2-3 个子页面（避免单页停留过久）
  - 增加数据卡片、关键数字、进度条等视觉元素
  - 页数增加 50-100%，内容密度提升
- **内容拆分策略**：概念页 + 数据页 + 案例页
- **推荐配图方案**：Excalidraw 技术图表 + 信息图表
- **优化工作流**：9 个阶段，步骤清晰

### v4.2 (2026-02-09) - 视频导出 v3.0 音频驱动
- **音频驱动时长**：每页展示时间 = 该页音频实际时长，视频/音频 100% 同步
- **流程重构**：先生成音频 → 获取时长 → 按时长截图 → 合成视频
- **ffprobe 时长检测**：使用 ffprobe 替代 mutagen，更可靠
- **移除 --duration 参数**：时长完全由讲解文字决定
- **默认语音改为云健**：zh-CN-YunjianNeural（新闻播报男声）

### v4.1 (2026-02-09) - 视频导出功能
- **新增视频导出系统**：将 HTML PPT 转换为带配音的 MP4 视频
- **Playwright 截图**：高清捕获每页幻灯片（2x 分辨率）
- **双 TTS 服务**：Edge TTS（免费，16种中文语音）/ OpenAI TTS（高质量）
- **智能时长对齐**：根据配音长度自动调整每页展示时间
- **新增脚本**：`scripts/ppt_to_video.py`
- **新增工作流阶段**：阶段七 - 视频导出选项
- **支持自定义讲解**：`data-narration` 和 `data-duration` HTML 属性

### v4.0 (2026-02-08) - 架构升级
- **LLM 智能设计优先**：Claude 直接生成 CSS 设计，不再依赖固定模板
- **本地模板作为 fallback**：16 种预设模板降级为备选方案
- **新增 LLMDesignGenerator**：Python 类处理 LLM 生成的设计规范
- **新增 LLMHTMLGenerator**：使用 LLM 设计生成完整 HTML
- **设计 JSON 格式规范**：标准化的设计描述格式
- **自动播放隐藏功能**：点击播放后控制面板自动消失
- **动画切换按钮**：所有模板支持 4 种动画切换

### v3.2 (2026-02-08)
- 优化工作流程，确保完整配置询问
- 新增配图方案细分（图标/信息图表/几何装饰）
- 添加 AskUserQuestion 标准 JSON 模板
- 添加内容类型→风格推荐映射表

### v3.1 (2026-02-08)
- 新增音频/视频转录功能
- 16 种风格模板完整实现
- Unsplash API 集成
- 6 种翻页动画
