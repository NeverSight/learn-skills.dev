---
name: dreamina-prompt-image2image
description: Use when the user wants to edit an existing image with 即梦 (Dreamina/Jimeng) models 4.0+ via style transfer (风格迁移), background replacement (背景替换), detail enhancement (细节增强), color adjustment (色彩调整), element add/remove (元素添加移除), season/time change (季节时间变换), restoration (修复), outfit change (换装), creative transformation (创意变形), or multi-reference compositing (多图合成); mentions "图生图", "image2image", "编辑图片", "换背景", "改风格", "修图", "把这张图变成"; or supplies a reference image and asks to transform it. Uses a Keep/Change framework that declares what stays and what transforms, with 10 edit categories, 30 annotated examples, and I2I-specific templates.
license: Complete terms in LICENSE.txt
---

# dreamina-prompt-image2image — 即梦图生图提示词

Craft image-to-image edit prompts for 即梦 Dreamina models 4.0+.

## When to use this skill

Use this skill when the user:
- Provides a reference image and wants to modify it ("把这张图改成...")
- Asks to change an image's style, background, colors, or details
- Wants to add or remove elements from an existing image
- Mentions keywords: 图生图, image2image, 编辑图片, 换背景, 改风格, 修图, 风格迁移, 背景替换
- Describes a transformation applied TO an existing image (not creating from scratch)

Do NOT use this skill for:
- Creating images from text only (no reference image) → use dreamina-prompt-text2image
- CLI execution → use dreamina-cli-image2image
- Video prompts → use dreamina-prompt-text2video or dreamina-prompt-image2video

## Core Methodology

The image-to-image prompt formula is fundamentally different from text-to-image:

```
[保留什么] + [改变什么] + [新元素/新风格描述] + [光影/色彩协调] + [画质要求]
```

**The Keep/Change Principle**: An I2I prompt must explicitly state what to KEEP and what to CHANGE. Failing to specify the "keep" list leads to edit cascading — the model changes elements you never intended to touch.

### Key difference from text-to-image

| | Text-to-Image | Image-to-Image |
|---|---|---|
| Input | Text only | Reference image(s) + edit instruction |
| Core task | Create from scratch | Transform while preserving |
| Prompt focus | Complete scene description | Keep vs. Change separation |
| Critical component | Subject + Scene + Style | KEEP list (what stays) + CHANGE list (what transforms) |
| Reference | Optional style reference | Required — the source image IS the starting point |
| Model requirement | 3.0+ | 4.0+ only |

## How to use this skill

### Step 1: Identify the edit category

| Category | What User Wants | Example File |
|----------|----------------|--------------|
| 风格迁移 | Change art style while keeping content | `examples/style-transfer.md` |
| 背景替换 | Replace background, keep foreground | `examples/background-replace.md` |
| 细节增强 | Improve quality, sharpness, texture | `examples/detail-enhance.md` |
| 色彩调整 | Change color palette, tone, mood | `examples/color-adjust.md` |
| 元素编辑 | Add or remove specific objects/elements | `examples/element-edit.md` |
| 季节/时间 | Change season or time of day | `examples/season-time.md` |
| 修复/复原 | Restore damaged/old photos | `examples/restoration.md` |
| 创意变形 | Whimsical/fantasy transformations | `examples/creative-transform.md` |
| 换装/服装 | Change clothing while keeping person | `examples/outfit-change.md` |
| 多图合成 | Combine elements from multiple images | `examples/multi-reference.md` |

### Step 2: Load reference materials

**Load the matched example file** from `examples/` for category-specific patterns.

**Load `references/usecase-library.md`** for detailed edit templates and the keep/change pattern for each use case.

**Load `references/word-library.md`** for transformation verbs, edit-specific modifiers, and coordination vocabulary.

**For general descriptive vocabulary** (facial features, clothing, scenes, styles, lighting, composition), cross-reference the text2image skill's `word-library.md` — it covers 12 major categories with 60+ subcategories not duplicated here.

### Step 3: Build the prompt with the Keep/Change framework

1. **KEEP list** (保留): What must remain unchanged? Be specific — enumerate the elements: "保持人物面部特征、姿势、服装颜色不变"
2. **CHANGE instruction** (改变): What specifically should transform? "将背景替换为..." "将风格转换为..."
3. **NEW description** (新元素): Describe what the result should look like AFTER the change
4. **Coordination** (协调): How should old and new elements blend? "调整光线使新旧元素自然融合""保持整体色调统一"
5. **Quality** (画质): Resolution and output specs

### Step 4: Apply I2I-specific writing rules

1. **Keep list first** — explicitly state what stays unchanged before describing changes
2. **Be specific about what changes** — "将纯色背景替换为阳光明媚的海滩" not "换个背景"
3. **Describe the blend** — new elements must look like they BELONG in the scene: "确保新背景的光线方向与原图人物身上的光影一致"
4. **Coordinate colors** — "新背景的色调与人物服装的暖色调保持协调"
5. **Multi-reference: assign roles** — "图一保留人物姿势，图二作为背景风格参考，图三作为服装材质参考"

### Step 5: Validate against checklist

Run through the [Validation Checklist](#validation-checklist). Every item must pass before presenting the prompt to the user.

### Step 6: Present the result

Always present: KEEP list + CHANGE instruction + complete prompt + model version (4.0+) + aspect ratio recommendation + optional alternative approaches.

## Writing Rules for Image-to-Image

### Rule 1: Keep list is mandatory

- ✗ "把背景换成海滩" → risk: model might also change the person
- ✓ "保持人物、姿势、服装不变。将纯色背景替换为阳光明媚的海滩，调整光线方向使人物光影与海滩环境光一致"

### Rule 2: The more you keep, the more you must list

For subtle edits (color tweak, detail enhancement), the keep list should be longer than the change instruction. The default behavior of I2I models is to "improve" everything — you must constrain it.

### Rule 3: Describe the coordination between old and new

The most common I2I failure is new elements looking "pasted on." Always add a coordination instruction:
- "确保新背景的光影方向与人物一致"
- "保持整体色调的协调统一"
- "新元素的材质与场景中的光照自然融合"

### Rule 4: Multi-reference images need role assignment

When using 2+ reference images, clearly assign each one's role:
- "图一：保留主体姿势和面部"
- "图二：作为背景风格参考"
- "图三：服装材质和颜色参考"

### Rule 5: Match output resolution to input

即梦 4.0 supports up to 4K. If the input is 2K, specify 2K or 4K output. Don't upscale a low-res input to 4K — quality degrades.

### Rule 6: Reference quality matters

模糊/杂乱的参考图会导致 AI 误判。If the user's reference image is low quality, recommend they use a clearer image or expect reduced quality.

## Validation Checklist

- [ ] KEEP list explicitly stated (what stays unchanged)
- [ ] CHANGE instruction is specific (not vague)
- [ ] NEW element description is complete
- [ ] Coordination/blend instruction included
- [ ] Aspect ratio recommendation matches content type
- [ ] Model version noted (must be 4.0+)
- [ ] For multi-reference: each image's role is assigned
- [ ] No conflicting instructions (e.g., "change the background" + "keep the scene identical")

## Gotchas

1. **Edit cascading is the #1 failure mode** — without explicit keep constraints, I2I models tend to "improve" everything. Always write a keep list
2. **Background/foreground separation can fail** — complex edges (hair, fur, transparent objects) may blend with the new background. Warn users about this limitation
3. **Multi-reference requires role clarity** — up to 6-10 images supported, but each must have a clear, distinct role. "Combine these two images" without specifying WHICH elements from EACH will produce unpredictable results
4. **Local editing is not supported** — 即梦 I2I works on the entire image. You cannot edit "only the left corner." All edits are global
5. **Model 4.0+ only** — I2I does not work with models 3.0-3.1. Always confirm model version
6. **Resolution matching** — 4.0 supports 2K/4K. Upscaling a low-res input degrades quality
7. **Style strength is controlled by prompt detail** — more detailed style description = stronger style application. Less detail = subtle effect

## Available Resources

| Resource | Description | When to Load |
|----------|-------------|--------------|
| `references/usecase-library.md` | 10 use case templates with keep/change patterns | When building any I2I prompt — loaded by default |
| `references/word-library.md` | Transformation verbs, edit modifiers, coordination vocabulary | When building any I2I prompt — loaded by default |
| `examples/style-transfer.md` | 风格迁移 examples | User wants to change art style |
| `examples/background-replace.md` | 背景替换 examples | User wants to change/replace background |
| `examples/detail-enhance.md` | 细节增强 examples | User wants higher quality, sharper details |
| `examples/color-adjust.md` | 色彩调整 examples | User wants to change color palette/tone |
| `examples/element-edit.md` | 元素添加/移除 examples | User wants to add or remove objects |
| `examples/season-time.md` | 季节/时间变换 examples | User wants different season or time of day |
| `examples/restoration.md` | 修复/复原 examples | User has damaged or old photos |
| `examples/creative-transform.md` | 创意变形 examples | User wants whimsical/fantasy transformations |
| `examples/outfit-change.md` | 换装/服装替换 examples | User wants to change clothing on a person |
| `examples/multi-reference.md` | 多图合成 examples | User has multiple reference images |

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user wants to edit an existing image with 即梦 (Dreamina/Jimeng) models 4.0+ via style transfer (风格迁移), background replacement (背景替换), detail enhancement (细节增强), color adjustment (色彩调整), element add/remove (元素添加移除), season/time change (季节时间变换), restoration (修复), outfit change (换装), creative transformation (创意变形), or multi-reference compositing (多图合成); mentions "图生图", "image2image", "编辑图片", "换背景", "改风格", "修图", "把这张图变成"; or supplies a reference image and asks to transform it. Uses a Keep/Change framework that declares what stays and what transforms, with 10 edit categories, 30 annotated examples, and I2I-specific templates.。

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
