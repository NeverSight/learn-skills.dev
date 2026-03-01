---
name: storyboard-generator
description: 根据用户描述的故事内容，润色故事线并拆分为分镜脚本，批量生成风格一致的故事板插图。提供8种视觉风格选择，基于故事类型推荐最佳风格。调用Gemini API生成图片，保存到Obsidian图片目录。触发词："分镜故事"、"故事板"、"做个分镜"、"创建故事板"、"storyboard"、"画个故事"。
---

# 分镜故事板生成器

根据用户描述润色故事线，拆分为分镜脚本，批量生成风格一致的故事板插图。

## 工作流程

### Phase 1: 故事润色与分镜拆分

1. **接收故事** - 获取用户描述的故事内容（文字、大纲、或灵感片段）
2. **润色故事线** - 补充叙事细节，梳理情感弧线，输出结构化故事概要：
   ```
   故事概要：一句话概括
   情感弧线：[起点] → [转折] → [结局]
   ```
3. **拆分分镜** - 将故事拆为 6-10 个关键帧，每帧包含：
   - 场景标题
   - 镜头类型（远景/中景/近景/特写等）
   - 画面描述（人物动作、环境、光线）
   - 情绪基调
   - 对白/文字（如有）
4. **展示分镜脚本** - 以表格形式展示，等待用户确认或调整

展示格式：
```
## 分镜脚本

| # | 场景 | 镜头 | 画面描述 | 情绪 |
|---|------|------|---------|------|
| 1 | 开场 | 远景 | xxx | 平静 |
| 2 | 引入 | 中景 | xxx | 好奇 |
| ... |
```

### Phase 2: 风格选择

分镜脚本确认后，展示 8 种视觉风格（读取 references/visual-styles.md）：

| # | 风格 | 一句话特征 | 适用故事 |
|---|------|----------|---------|
| 1 | 赛博朋克漫画 | 霓虹+暗色调+高对比 | 科技/AI/未来 |
| 2 | 吉卜力水彩 | 柔和水彩+温暖光影 | 日常/温馨/成长 |
| 3 | 美式扁平插画 | 矢量几何+明快配色 | 产品/商业/教育 |
| 4 | 电影分镜手稿 | 黑白素描+镜头标注 | 视频脚本/广告 |
| 5 | 像素艺术 | 复古16-bit游戏风 | 游戏/趣味/极客 |
| 6 | 中国风水墨 | 水墨晕染+诗意留白 | 传统/哲理/东方 |
| 7 | 清线漫画 | 均匀粗线+扁平上色 | 冒险/幽默/IP |
| 8 | 写实概念艺术 | 电影级数字绘画 | 史诗/科幻/奇幻 |

根据故事类型和情感调性，**推荐 1-2 种最适合的风格并说明理由**，等待用户选择。

### Phase 3: 生成提示词

用户选定风格后，为每个分镜帧生成提示词。

每个提示词结构（读取 references/visual-styles.md 获取风格前缀和镜头语言）：
1. **风格前缀** - 选定风格的标准描述
2. **镜头指令** - 如 "Wide establishing shot" / "Close-up"
3. **画面叙述** - 用完整语句描述场景内容（人物、动作、环境、光线、氛围）
4. **情绪指令** - 明确画面传递的情感
5. **一致性锚定** - `IMPORTANT: This is panel [N] of [TOTAL] in a storyboard sequence. Maintain exact same art style, color palette, character design, and visual consistency with all other panels. Same character must look identical across all panels.`
6. **中文指令**（如需）- `ALL text, signs, and dialogue in the image MUST be in Chinese (Simplified Chinese). Technical terms may remain in English.`

展示提示词概要表，等待确认：
```
## 提示词概要

| # | 场景 | 镜头 | 风格 | 核心画面 |
|---|------|------|------|---------|
| 1 | 开场 | 远景 | 赛博朋克 | 城市天际线... |
| ... |

确认后开始生成（共 N 帧）
```

### Phase 4: 批量生成

确认后逐帧调用脚本生成：

```bash
python3 scripts/generate_image.py \
  --prompt "提示词" \
  --output "/Users/ugreen/Documents/obsidian/09image/MMDD-故事名-storyboard/01-场景名.png" \
  --api-key "AIzaSyDvvGGRbH4Os3Er0dYi0kE_AzE3_2b_Az8" \
  --api-url "https://generativelanguage.googleapis.com" \
  --model "gemini-3-pro-image-preview" \
  --aspect-ratio "16:9" \
  --resolution "2K"
```

**注意事项**:
- 故事板默认 **16:9 横版**
- 分辨率默认 **2K**
- MMDD 为当天日期
- 文件命名：`01-场景简称.png`、`02-场景简称.png`...
- 每帧间隔 2-3 秒避免限流
- 失败帧记录并继续，最后汇报
- **关键**: 角色外观描述在所有帧中保持一致（发型、服装、体型）

### Phase 5: 展示与迭代

1. 生成完成后，按顺序列出所有帧路径
2. 询问用户：
   - "整体故事节奏是否满意？"
   - "需要重新生成某一帧吗？"
   - "需要增加/删除某个场景吗？"
   - "角色一致性是否满意？"
3. 迭代：调整提示词重新生成指定帧

## 保存路径规范

```
/Users/ugreen/Documents/obsidian/09image/MMDD-故事名-storyboard/
├── 01-开场-远景.png
├── 02-引入-中景.png
├── 03-转折-近景.png
├── 04-发展A-中景.png
├── 05-发展B-全景.png
├── 06-高潮-特写.png
├── 07-结局-远景.png
└── storyboard-script.md  (可选：保存分镜脚本文档)
```

## API 配置

| 配置项 | 值 |
|-------|---|
| API URL | `https://generativelanguage.googleapis.com` |
| API Key | `AIzaSyDvvGGRbH4Os3Er0dYi0kE_AzE3_2b_Az8` |
| Model | `gemini-3-pro-image-preview` |
| 默认比例 | 16:9（故事板横版） |
| 默认分辨率 | 2K |

## 镜头语言速查

| 镜头 | 英文 | 用途 |
|------|------|------|
| 远景 | Wide Shot | 开场、环境交代 |
| 全景 | Full Shot | 人物全身+环境 |
| 中景 | Medium Shot | 对话、日常互动 |
| 近景 | Close-up | 表情、情感 |
| 特写 | Extreme Close-up | 关键道具、细节 |
| 俯拍 | Bird's Eye | 全局、渺小感 |
| 仰拍 | Low Angle | 权威、震撼 |

## 常见用法

| 用户说 | 操作 |
|-------|-----|
| "帮我画个故事分镜" | 收集故事 → 润色 → 拆分镜 → 选风格 → 生成 |
| "这个故事做成故事板" | 同上 |
| "用赛博朋克风画这个故事" | 跳过风格选择，直接用指定风格 |
| "第3帧不好，重新生成" | 调整提示词重新生成单帧 |
| "加一帧过渡镜头" | 在指定位置插入新分镜帧 |
