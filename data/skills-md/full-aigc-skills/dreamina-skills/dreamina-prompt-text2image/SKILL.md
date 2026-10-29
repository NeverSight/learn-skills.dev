---
name: dreamina-prompt-text2image
description: Use when the user wants to write, refine, optimize, or translate an image-generation prompt for 即梦 (Dreamina/Jimeng) — mentions "提示词", "文生图", "text2image", "文字成图", "AI绘画", "AI生图", "prompt", "帮我写一个...的画面", "生成一张...的图片", "写一个...的提示词"; describes an image they want; or supplies a rough description to turn into a production-ready prompt. Covers 35 scenario categories with 115+ annotated examples, a word library across 60+ thematic subcategories, and complete color references (159 Chinese traditional colors, the 384-color Forbidden City palette, Pantone, RAL).
license: Complete terms in LICENSE.txt
---

# dreamina-prompt-text2image — 即梦文生图提示词

Craft production-ready text-to-image prompts for 即梦 (Jimeng/Dreamina) models.

## When to use this skill

Use this skill when the user:
- Asks you to write an image generation prompt ("帮我写个提示词")
- Describes an image they want and needs it turned into a proper prompt
- Wants to refine, optimize, or translate an existing prompt
- Mentions keywords like: 提示词, 文生图, text2image, AI绘画, AI生图, prompt, 文字成图
- Asks about how to describe a specific visual scene, style, or effect

Do NOT use this skill for:
- Executing CLI commands to generate images → use dreamina-cli-text2image
- Writing video prompts → use dreamina-prompt-text2video
- Image-to-image editing prompts → use dreamina-prompt-image2image

## Core Methodology

The prompt formula is a reasoning framework — not a rigid template. Apply it flexibly:

```
[主体/人物] + [场景/背景] + [动作/姿态] + [风格/艺术类型] + [光线/色彩] + [构图/视角] + [画质/细节]
```

Each component is optional. Select and weight components based on the scenario:
- **Portrait**: emphasize subject, expression, clothing, lighting, composition
- **Landscape**: emphasize environment, time/weather, color palette, atmosphere
- **Product**: emphasize object details, material, background, lighting setup
- **Abstract/Artistic**: emphasize style, color scheme, texture, mood

## How to use this skill

### Step 1: Identify scenario category
→ Load `rules/category-table.md` to match user's request to the right category and example file

### Step 2: Load reference materials

**Load the relevant vocabulary files from `word-library/` based on what you need — never load the whole library:**

| 你需要的 | 加载文件 |
|----------|----------|
| 人物/面部/体型/发型/表情/妆容/服装/配饰 | `word-library/subject.md` |
| 场景/环境/天气/时间/季节/地域 | `word-library/scene.md` |
| 摄影/绘画/设计/数字/民族风格 | `word-library/style.md` |
| 材质/肌理（金属/木材/石材/织物/玻璃） | `word-library/material.md` |
| 动作/姿态/动态/手势 | `word-library/motion.md` |
| 道具/器物/乐器/武器/科技/食物 | `word-library/props.md` |
| 光线/光影/光效/照明 | `word-library/lighting.md` |
| 构图/视角/景深/镜头 | `word-library/composition.md` |
| 画质/质感/通感词 | `word-library/quality.md` |
| 氛围/情绪/意境 | `word-library/atmosphere.md` |
| 抽象/概念/视觉隐喻 | `word-library/abstract.md` |
| 自然元素（花卉/树木/动物） | `word-library/nature.md` |

**Load color references — choose by what the user says:**

| 用户提到 | 加载文件 |
|----------|----------|
| 中国色、传统色、胭脂、桃红、月白、黛色、中国红、故宫色、国风配色 | `color-library/chinese-traditional.md` |
| Pantone、潘通、流行色、年度色、国际流行 | `color-library/pantone.md` |
| RAL、劳尔色卡、工业色、国际标准色 | `color-library/ral.md` |
| 莫兰迪、配色方案、色彩搭配、电影色调、高级灰、低饱和 | `color-library/modern-schemes.md` |
| 用户提到具体颜色但没说体系 | 从最相关的文件加载 |

**Load model-version-specific references:**

| 版本 | 关键词 | 官方 Model ID | 加载文件 |
|------|--------|--------------|----------|
| **2.1** | 2.1 | — | `references/jimeng-2.1-prompt-guide.md` |
| **3.0** | 3.0 | — | `references/3.0/vocabulary-core.md` + `references/jimeng-3.0-prompt-guide.md` + `references/jimeng-3.0-word-library.md`。如需风格→额外 `references/3.0/vocabulary-styles.md`；如需材质→额外 `references/3.0/vocabulary-materials.md` |
| **3.1** | 3.1 | — | `references/jimeng-3.1-prompt-guide.md` |
| **4.0** | 4.0 | `doubao-seedream-4-0-250828` | `references/jimeng-4.0-prompt-guide.md` |
| **4.1** | 4.1 | — | `references/jimeng-4.1-prompt-guide.md` |
| **4.5** | 4.5 | `doubao-seedream-4-5-251128` | `references/jimeng-4.5-prompt-guide.md` |
| **5.0** | 5.0, Seedream, 联网 | `doubao-seedream-5-0-260128` (also `doubao-seedream-5-0-lite-260128`) | `references/seedream-5.0-prompt-guide.md` |
| **未指定** | — | — | 默认 `references/jimeng-3.0-vocabulary.md` |

### Step 3: Build the prompt
→ Load `rules/core-methodology.md` for component-by-component guidance

### Step 4: Apply writing rules
→ Load `rules/writing-rules.md` for all 10 writing rules

### Step 5: Validate
→ Load `rules/validation-checklist.md` and run through all checks

## Gotchas

1. **即梦 ignores negations** — "不要红色" is interpreted as "红色". Always rewrite as positive descriptions
2. **Character consistency is limited** — 即梦 cannot reliably maintain the same face across multiple generations. Avoid promising identical characters
3. **Aspect ratio drives composition** — a prompt written for 16:9 will compose differently than the same prompt at 9:16. Always confirm the intended aspect ratio
4. **Style keywords can dominate** — strong style keywords (cyberpunk, 水墨, Pixar) can override other elements. Place them carefully in the prompt order
5. **Prompt language** — 即梦 works best with Chinese prompts. If the user provides English, translate and adapt rather than directly using it
6. **⚠️ Never write hex color values into prompts** — The model treats `#ff2121`, `#9d2933` etc. as literal text to render in the image, NOT as color instructions. Always use Chinese color names only: "大红", "胭脂", "桃红" — never "大红 #ff2121" or any form with hex codes
7. **Color library is for YOUR reference only** — Load `color-library/chinese-traditional.md` to FIND the right color name to write into the prompt. Do NOT copy hex codes into the output prompt text

## Available Resources

| Resource | Description | When to Load |
|----------|-------------|--------------|
| `rules/category-table.md` | 35 scenario categories + example mapping | Step 1 |
| `rules/core-methodology.md` | Component-by-component build guide + presentation | Step 3 |
| `rules/writing-rules.md` | 9 prompt writing rules | Step 4 |
| `rules/validation-checklist.md` | 8-point pre-submission checklist | Step 5 |
| `word-library/*.md` | 12 thematic vocabulary files | Based on prompt component needed |
| `color-library/chinese-traditional.md` | 中国色9大色系159色 | User mentions 中国色/传统色/胭脂 |
| `color-library/pantone.md` | Pantone常用色系 | User mentions Pantone/潘通 |
| `color-library/ral.md` | RAL Classic+RAL Design | User mentions RAL/劳尔 |
| `color-library/modern-schemes.md` | 莫兰迪+配色方案+电影色调 | User mentions 莫兰迪/配色 |
| `references/gugong-384-colors.md` | 384 colors × 24 solar terms | Poetic/seasonal colors |
| `references/jimeng-*.md` | Version-specific guides | Based on user's model version |
| `references/3.0/*.md` | 3.0 core/styles/materials | When using 3.0 model |
| `references/618-ecommerce-poster-examples.md` | 抖音商城 618 好东西大会 14 组官方电商海报示例 | ⭐ 用户写电商促销海报、618 主题海报、带货类提示词时加载（被动引用，无需告知用户） |
| `examples/*.md` | 35 scenario-specific examples | After identifying category |

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user wants to write, refine, optimize, or translate an image-generation prompt for 即梦 (Dreamina/Jimeng) — mentions "提示词", "文生图", "text2image", "文字成图", "AI绘画", "AI生图", "prompt", "帮我写一个...的画面", "生成一张...的图片", "写一个...的提示词"; describes an image they want; or supplies a rough description to turn into a production-ready prompt. Covers 35 scenario categories with 115+ annotated examples, a word library across 60+ thematic subcategories, and complete color references (159 Chinese traditional colors, the 384-color Forbidden City palette, Pantone, RAL).。

## Rules

- 先读后写：先确认当前状态与真实能力，再执行会改变外部状态的动作。
- 权限最小化：只使用完成当前步骤所需的文件、工具、账户与网络范围。
- 证据优先：运行结果、资源 ID、版本、哈希或测试输出缺失时，明确标记为 `NOT_VERIFIED`。
- 幂等优先：保留请求标识与阶段状态；结果不明确时先查询，不进行盲目重试。
- 隐私安全：日志、示例、回执和错误信息不得包含 token、cookie、密钥或个人敏感数据。

## Workflow

### Step 1：澄清意图

确认本技能是否匹配目标；若只是相邻需求，交给更精确的技能。
### Step 2：执行预检

校验输入、模型/工具能力、输出路径、预算上限和审批状态；任一关键条件未知时停止在只读阶段。
### Step 3：形成计划

列出将调用的工具、会改变的对象、成功标准以及失败后的安全退出方式。
### Step 4：执行动作

按一次批准执行并记录请求标识；模糊结果先查询而不是重提；每个外部调用均保留可关联的状态或回执。
### Step 5：验证交付

验证产物存在性、格式、哈希/标识、成本状态和质量门禁，并把事实、推断和未验证项分开陈述。

## Validation checklist

- [ ] 技能触发条件与用户意图一致，没有把相邻任务误路由到本技能。
- [ ] 输入、目标对象、版本和输出位置均已明确，且没有使用猜测值替代必填值。
- [ ] 所有写入、付费、发布或不可逆动作都在用户授权范围内。
- [ ] 结果已用独立检查验证；仅有“命令成功”或“文件存在”不算完整验收。
- [ ] 输出包含实际证据、失败/跳过项、剩余风险和可执行的下一步。

## Gotchas

1. **把计划当结果**：文档或提示词不等于真实执行；必须标明实际运行层级。
2. **错误重试**：超时或响应丢失可能已经产生远端状态，先查询再决定是否重试。
3. **隐式扩大范围**：批量、全量、发布、覆盖和付费不是普通读写的自然延伸。
4. **版本漂移**：引用外部资源时记录版本、tag 或提交；不要把可变分支当发布证据。
5. **证据过期**：缓存、旧截图和历史测试不能证明当前环境；在交付前刷新关键证据。

## 不适用与边界

付费、发布、覆盖、上传或外部写入必须使用当前任务的显式授权；不自动扩大次数和预算。 如果请求需要别的技能，不复制其正文；按技能名称进行交接，并保留当前任务上下文。

## Progressive disclosure

- 需要确定输入/输出、状态和授权点时，读取 `references/workflow-contract.md`。
- 需要交付前自检时，读取 `references/validation-checklist.md`。
- 遇到超时、部分成功或恢复场景时，读取 `references/error-recovery.md`。
- 首次运行、拒绝越权和失败恢复分别参考 `examples/happy-path.md`、`examples/boundary-refusal.md`、`examples/failure-recovery.md`。
