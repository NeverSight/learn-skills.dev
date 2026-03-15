---
name: banana-image
description: |
  AI 图片生成技能。使用 Gemini API 生成高质量产品图、海报、缩略图等（最高 4K 分辨率）。

  触发场景：
  - 需要生成产品宣传图片、电商展示图
  - 需要创建海报、Banner、社交媒体配图
  - 需要 AI 生成或编辑高清图片
  - 需要批量生成图片变体

  触发词：生成图片、AI图片、产品图、海报、缩略图、4K、高清、制作图片、/image、图片编辑

  【不触发】纯文本任务、代码生成、不涉及图片的设计讨论。
  【先问什么】若缺少：图片描述、分辨率偏好、宽高比，先提问补齐。
---

# Banana Image - AI 图片生成

基于 Gemini API 的独立图片生成技能，支持 4K 输出、双模型选择、图片编辑。

## 环境要求

```bash
# 设置 API Key（必需）
export GEMINI_API_KEY="your-api-key"

# 安装依赖（首次使用）
cd .claude/skills/banana-image/scripts && npm install
```

## 快速命令

```bash
# 快速生成（Flash 模型）
npx tsx .claude/skills/banana-image/scripts/banana_image_exec.ts \
  -p "可爱的柴犬在公园玩耍" -m flash

# 4K 高质量生成（Pro 模型）
npx tsx .claude/skills/banana-image/scripts/banana_image_exec.ts \
  -p "专业产品照片：iPhone 手机壳" -m pro -r 4K -a 4:5
```

## 模型选择

| 模型      | 速度 | 分辨率  | 适用场景                     |
| --------- | ---- | ------- | ---------------------------- |
| **Flash** | 2-3s | ≤1024px | 快速草图、迭代、原型         |
| **Pro**   | 5-8s | ≤4K     | 最终交付、营销素材、专业作品 |

**自动选择规则**：

- 包含 "快速"、"草图"、"draft" → Flash
- 包含 "4K"、"专业"、"高质量" → Pro（默认）

## 参数说明

```bash
npx tsx banana_image_exec.ts --help

Options:
  --prompt, -p <text>      图片描述（必需）
  --model, -m <type>       模型选择: flash | pro (默认: pro)
  --aspect-ratio, -a <r>   宽高比: 1:1, 16:9, 9:16, 4:3, 3:2, 21:9 等
  --resolution, -r <res>   分辨率: 1K, 2K, 4K (默认: Pro=4K, Flash=1K)
  --negative, -n <text>    排除内容描述
  --output, -o <dir>       输出目录 (默认: ./images)
  --grounding, -g          启用 Google Search 锚定 (仅 Pro)
  --input, -i <path>       输入图片路径（编辑模式）
  --system, -s <text>      系统指令
  --count, -c <num>        生成数量 (1-4)
```

## 工作流

### 1. 简单生成

```bash
npx tsx .claude/skills/banana-image/scripts/banana_image_exec.ts \
  -p "A cute shiba inu playing in the park" \
  -m pro
```

### 2. 带参数生成

```bash
# 16:9 横版海报，启用 Google 搜索锚定
npx tsx .claude/skills/banana-image/scripts/banana_image_exec.ts \
  -p "2024年科技大会宣传海报" \
  -m pro -r 4K -a 16:9 -g
```

### 3. 图片编辑

```bash
# 修改现有图片
npx tsx .claude/skills/banana-image/scripts/banana_image_exec.ts \
  -p "将背景改为黄昏海滩" \
  -i /path/to/original.png
```

### 4. 批量生成

```bash
# 生成多张变体
npx tsx .claude/skills/banana-image/scripts/banana_image_exec.ts \
  -p "产品照片：无线耳机" \
  -m pro -c 4
```

## 输出格式

脚本输出 JSON 格式结果：

```json
{
  "success": true,
  "images": [
    {
      "path": "./images/banana_pro_2024-01-01T12-00-00_abc123.png",
      "model": "gemini-3-pro-image-preview",
      "prompt": "可爱的柴犬"
    }
  ],
  "metadata": {
    "model": "gemini-3-pro-image-preview",
    "aspectRatio": "1:1",
    "resolution": "4K",
    "duration": 5234
  }
}
```

## 宽高比映射

| 用途         | 宽高比 | 关键词                        |
| ------------ | ------ | ----------------------------- |
| 社交媒体方图 | 1:1    | "方形"、"Instagram"           |
| 横版海报     | 16:9   | "横版"、"YouTube"、"桌面壁纸" |
| 竖版海报     | 9:16   | "竖版"、"手机壁纸"、"Story"   |
| 产品图       | 4:5    | "产品"、"电商"                |
| 电影海报     | 2:3    | "海报"、"电影"                |
| 超宽屏       | 21:9   | "超宽"、"Banner"              |

## 模板系统

读取预定义模板生成图片：

```bash
# 列出可用模板
python .claude/skills/banana-image/scripts/apply_template.py list

# 应用产品图模板
python .claude/skills/banana-image/scripts/apply_template.py apply product \
  -v '{"product": "wireless earbuds"}'
```

模板输出可直接传递给 `banana_image_exec.ts`。

## 错误处理

| 错误                    | 原因           | 解决方案                      |
| ----------------------- | -------------- | ----------------------------- |
| GEMINI_API_KEY not set  | 未设置 API Key | `export GEMINI_API_KEY="..."` |
| Content filtered        | 内容安全过滤   | 调整描述，避免敏感词          |
| Invalid aspect ratio    | 不支持的宽高比 | 使用支持的宽高比              |
| Image generation failed | API 调用失败   | 检查网络和 API 配额           |

## 参考文档

- [高级用法](references/advanced-usage.md) - 批量生成、图片编辑、参数优化
