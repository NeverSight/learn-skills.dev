---
name: logo-batch-generator
description: 批量生成品牌Logo。支持两种入口：(1)用户描述品牌/用途后批量生成10个Logo变体 (2)用户上传参考图片后分析并生成Logo。提供7种主流风格选择。调用Gemini API生成，保存到Obsidian图片目录。触发词："生成Logo"、"设计Logo"、"做个Logo"、"批量Logo"、"帮我设计一个标志"。
---

# Logo 批量生成器

根据品牌描述或参考图片，批量生成 10 个专业 Logo 变体，支持 7 种主流风格。

## 两种入口模式

### 模式 A：文字描述入口

用户描述品牌名、用途、风格偏好 → 生成 Logo。

### 模式 B：图片参考入口

用户上传参考图片 → 分析图片元素 → 询问需求 → 生成 Logo。

## 工作流程

### Phase 1: 需求收集

**模式 A（文字描述）**:
1. 收集品牌信息：品牌名（中文/英文）、行业/用途、核心理念
2. 展示 7 种风格选项（读取 references/logo-styles.md），简明介绍每种风格特点
3. 根据品牌属性推荐 1-2 种最适合的风格，说明理由
4. 等待用户选择风格

**模式 B（图片参考）**:
1. 分析用户上传的图片，提取：
   - 图形元素（形状/图标/符号）
   - 色彩方案（主色/辅色）
   - 排版风格（字体类型/排列）
   - 最接近的风格类型
   - 情感调性
2. 展示分析结果，询问用户意图：
   - "想要类似风格的 Logo？"
   - "想保留某些元素并改进？"
   - "想要完全不同方向的 Logo？"
3. 展示风格选项并推荐
4. 等待用户选择

### Phase 2: 生成提示词

选定风格后，为品牌生成 10 个 Logo 变体的提示词：

**变体策略**（读取 references/logo-styles.md 获取模板）:
- 变体 1-2：主风格，不同构图（图标居中 / 图文左右排列）
- 变体 3-4：主风格，不同配色方案（浅色/深色/对比色）
- 变体 5-6：主风格，不同图标/符号变化
- 变体 7-8：相近风格交叉（如极简+线条混合）
- 变体 9-10：额外探索方向（用户可指定）

每个提示词结构：
1. 风格描述（来自选定风格的模板前缀）
2. 品牌具体描述（名称、行业、理念）
3. 构图/配色的具体变化
4. 基础指令：`Professional logo design. Pure white background. High contrast. Scalable vector-style quality. No watermark, no mockup, no background texture.`
5. 中文指令（若 Logo 含中文）：`ALL text in the logo MUST use Chinese characters with clean professional Chinese typography. Technical terms and brand abbreviations may remain in English.`

展示所有 10 个提示词概要，等待用户确认：
```
## Logo 提示词概要

| # | 变体方向 | 风格 | 配色 | 简述 |
|---|---------|------|------|------|
| 1 | 主风格-构图A | 极简扁平 | 蓝色 | 几何图标居中... |
| 2 | 主风格-构图B | 极简扁平 | 蓝色 | 图文横排... |
| ... |

确认后开始生成（共 10 张 Logo）
```

### Phase 3: 批量生成

确认后逐个调用脚本生成：

```bash
python3 scripts/generate_image.py \
  --prompt "提示词" \
  --output "/Users/ugreen/Documents/obsidian/09image/MMDD-品牌名-logo/01-变体描述.png" \
  --api-key "AIzaSyDvvGGRbH4Os3Er0dYi0kE_AzE3_2b_Az8" \
  --api-url "https://generativelanguage.googleapis.com" \
  --model "gemini-3-pro-image-preview" \
  --aspect-ratio "1:1" \
  --resolution "2K"
```

**注意事项**:
- Logo 默认使用 **1:1 正方形** 比例
- 分辨率默认 **2K**
- MMDD 为当天日期
- 品牌名取简短英文/拼音（如 spaceai、mylogo）
- 文件命名：`01-风格-变体.png`（如 `01-flat-icon-center.png`）
- 每张间隔 2-3 秒避免限流
- 失败的图继续下一张，最后汇报

### Phase 4: 展示与迭代

1. 生成完成后，列出所有成功的 Logo 路径
2. 询问用户：
   - "哪几个方向最喜欢？"
   - "需要基于某个方向继续迭代吗？"
   - "需要调整配色/形状/文字吗？"
3. 若用户要求迭代，基于选中的 Logo 调整提示词重新生成

## 保存路径规范

```
/Users/ugreen/Documents/obsidian/09image/MMDD-品牌名-logo/
├── 01-flat-icon-center.png
├── 02-flat-text-horizontal.png
├── 03-flat-dark-theme.png
├── 04-flat-gradient-accent.png
├── 05-flat-alt-symbol.png
├── 06-flat-abstract-shape.png
├── 07-lineart-monoline.png
├── 08-lineart-detail.png
├── 09-explore-badge.png
└── 10-explore-gradient.png
```

## API 配置

| 配置项 | 值 |
|-------|---|
| API URL | `https://generativelanguage.googleapis.com` |
| API Key | `AIzaSyDvvGGRbH4Os3Er0dYi0kE_AzE3_2b_Az8` |
| Model | `gemini-3-pro-image-preview` |
| 默认比例 | 1:1（正方形） |
| 默认分辨率 | 2K |

## 7 种可选风格速览

| # | 风格 | 一句话特征 | 适用场景 |
|---|------|----------|---------|
| 1 | 极简扁平 | 几何+纯色，干净利落 | 科技、SaaS、互联网 |
| 2 | 线条艺术 | 单线条，优雅精致 | 工作室、设计品牌 |
| 3 | 字母标志 | 首字母创意变形 | 企业、个人品牌 |
| 4 | 徽章印章 | 圆形边框，复古仪式感 | 社区、播客、教育 |
| 5 | 吉祥物图标 | 角色化，记忆点强 | 游戏、教育、社交 |
| 6 | 渐变现代 | 丰富渐变，科技感强 | AI 产品、App、金融科技 |
| 7 | 手写书法 | 手写体，温暖有温度 | 博客、餐饮、手作 |

详细风格模板和配色参考见 references/logo-styles.md。

## 常见用法

| 用户说 | 操作 |
|-------|-----|
| "帮我设计一个 Logo" | 模式A：收集描述 → 推荐风格 → 生成 |
| "做个 Logo，科技风" | 模式A：直接推荐极简/渐变风格 |
| "参考这张图做 Logo" | 模式B：分析图片 → 询问意图 → 生成 |
| "我喜欢第3个，再做几个类似的" | 迭代：基于选中方向扩展生成 |
| "把第5个改成蓝色" | 迭代：调整配色重新生成 |
