---
name: sketch-image-prompt
description: Transforms article content or summaries into minimalist hand-drawn style JSON prompts for AI image generation tools. Use this skill whenever the user wants to create any kind of visual from text content — including banners, article illustrations, inline diagrams, infographics, or concept visuals. Trigger on requests like "turn this into a visual", "create an image prompt", "make an illustration for this", "generate a diagram from this article", "I need a sketch for this section", or any request combining content analysis with image/visual prompt generation. Always use this skill when the user provides text content and wants an AI-ready image prompt output.
---

# Sketch Image Prompt

将文字内容转化为极简手绘风格图像提示词，供 Midjourney、Stable Diffusion 等 AI 绘图工具直接使用。

## 工作流程

### 第一步：询问尺寸比例

用户提供内容后，**必须先询问尺寸比例**，再进行分析：

> "请问这张图的尺寸比例是？
>
> 横屏：
> - **16:9** — 横向展示 / Twitter / 社交媒体
> - **5:2** — 博客头图 / 宽幅横图
> - **21:9** — 微信公众号封面 / 超宽幅
> - **4:3** — 通用横图 / 演示文稿
> - **1:1** — 方形 / Instagram / 头像配图
>
> 竖屏：
> - **9:16** — 手机全屏 / Story / 竖版海报
> - **2:5** — 竖版长图 / 手机壁纸
> - **9:21** — 竖版超长图 / 手机长截图
> - **3:4** — 竖版通用图 / 小红书"

### 第二步：内部分析（不输出给用户）

在脑中完成以下分析，**不要输出这个过程**：

- 提炼核心主题（1个最核心的概念）
- 筛选关键元素（只选 **3-5个**，宁少勿多）
- 识别元素关系（流程 / 对比 / 层级 / 循环 / 并列）
- 判断情感基调 → 推断配色
- 根据比例选择最优布局

**配色参考：**

| 主题类型 | 背景色建议 |
|---------|-----------|
| 技术/开发 | 薄荷绿系 `#D4F1D4`、`#E3F2FD` |
| 商业/金融 | 米黄/浅桃系 `#F5E6D3`、`#FFDAB9` |
| 创意/设计 | 淡紫/淡粉系 `#E6E6FA`、`#FFE4E1` |
| 教育/知识 | 浅黄/薄荷系 `#FFF9E3`、`#D4F1D4` |
| 通用/中性 | 温暖米色系 `#F5E6D3` |

**布局参考：**

| 比例 | 布局方向 | 元素上限 |
|------|---------|---------|
| 16:9 | 水平流程（左→右） | 5个 |
| 5:2  | 水平延展 | 5-6个 |
| 21:9 | 水平极宽，辐射或简洁流程 | 4个 |
| 4:3  | 水平/方形过渡 | 5个 |
| 1:1  | 居中对称，辐射型 | 4个 |
| 9:16 | 垂直堆叠（上→下） | 5个 |
| 2:5  | 垂直延展 | 5-6个 |
| 9:21 | 垂直极长，分层结构 | 6个 |
| 3:4  | 垂直/方形过渡 | 5个 |

竖屏时：横屏「左→右」流程改为「上→下」，横向对比改为纵向对比。

### 第三步：输出给用户

**只输出以下两部分，不输出其他任何内容：**

```
[一行设计摘要：背景色 + 构图类型 + 元素数量，例如：薄荷绿背景，水平三步流程，3个元素]

[final_prompt 正文]
```

---

## Final Prompt 规范

### 必须包含的内容

1. **比例参数**（根据工具格式）
   - Midjourney：结尾加 `--ar 16:9`（或对应比例）
   - 通用描述：开头写 `16:9 horizontal composition` 或 `9:16 vertical composition`
   - 默认同时写通用描述 + Midjourney 参数，兼容两种工具

2. **视觉风格**（固定不变）：
   - `minimalist hand-drawn illustration`
   - `bold marker illustration, chunky brush-pen style`
   - `very thick black outlines, heavy stroke weight, bold chunky lines like a childrenΓÇÖs book illustration`

3. **笔触质感**（必须详细描述）：
   - `dry brush texture with tiny gaps in ink coverage`
   - `organic slightly rough edges`
   - `natural line weight variation but always heavy and bold`
   - `imperfect circles and slightly wobbly lines`
   - `warm handmade feel, NOT perfect vector lines, NOT thin lines — bold chunky strokes only`

4. **配色**：背景色（含色号）+ `black #000000` 主色 + 强调色（如有）

5. **构图与元素**：布局方式 + 每个元素的视觉描述 + 连接方式

6. **简洁性关键词**：
   - `minimalist`, `extremely simple`, `clean`, `uncluttered`
   - `generous whitespace`, `only 3-5 elements total`
   - `minimal text`, `1-3 words per label`

7. **排版**：`rounded handwritten-style font, casual and friendly`

### Final Prompt 模板结构

```
[比例] [构图类型] composition. [背景色描述]. Only [N] elements: [元素1描述], [元素2描述], [元素3描述]. [连接方式描述]. Bold marker illustration, chunky brush-pen style, very thick black outlines with heavy stroke weight — like a fat-tipped marker, bold chunky lines. Dry brush texture with tiny gaps in ink coverage, organic slightly rough edges, natural line weight variation, imperfect circles and slightly wobbly lines, warm handmade feel — NOT perfect vector lines. [配色描述]. Minimal text labels only: [标签列表]. Generous whitespace, clean and uncluttered, flat illustration with no shadows or gradients, rounded handwritten-style font. --ar [X:Y]
```

## 语言规则

- 设计摘要跟随用户语言
- `final_prompt` **始终使用英文**
