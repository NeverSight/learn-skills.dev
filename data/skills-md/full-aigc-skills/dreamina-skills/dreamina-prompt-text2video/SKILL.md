---
name: dreamina-prompt-text2video
description: Use when the user wants to write, refine, or optimize a video-generation prompt for 即梦 (Dreamina/Jimeng) video models (视频3.0 Pro, Doubao Seedance 2.0, Seedance 1.5/1.0, 智能多帧); mentions 文生视频, text2video, 视频提示词, 运镜, camera movement, 生成一段...的视频, 帮我写个视频; describes a scene they want as a video; or supplies a rough scene description. Covers 12 scenario categories with 35 annotated examples, adds explicit motion description and camera direction beyond image prompts, and includes a motion/camera word library plus 7 basic and 6 advanced compound camera techniques with emotional effect mappings.
license: Complete terms in LICENSE.txt
---

# dreamina-prompt-text2video — 即梦文生视频提示词

Craft production-ready text-to-video prompts for 即梦 Dreamina video models (视频3.0 Pro, Doubao Seedance 2.0, Seedance 1.5, Seedance 1.0, 智能多帧).

## When to use this skill

Use this skill when the user:
- Asks you to write a video generation prompt ("帮我写个视频提示词")
- Describes a scene they want as a moving image / video
- Wants to refine or optimize an existing video prompt
- Mentions keywords like: 文生视频, text2video, 视频生成, 视频提示词, 运镜, camera movement, Seedance
- Asks about how to describe motion, camera work, or temporal progression in a prompt

Do NOT use this skill for:
- Executing CLI commands to generate videos → use dreamina-cli-text2video
- Writing image-to-video prompts → use dreamina-prompt-image2video
- Writing text-to-image prompts → use dreamina-prompt-text2image

## Model Version Guide

即梦 has multiple video model lines. The core writing approach differs by model:

| Model | Formula | Key Difference |
|-------|---------|----------------|
| **视频3.0 / 3.0 Pro** | 主体 + 动作 + 场景 + 镜头 + 风格 + (情绪演绎) + (照明) | 自然语言自由书写; 支持切镜和创意特效 |
| **Doubao Seedance 2.0 系列** | 主体 + 动作/运动 + 空间背景/光影/风格 + 镜头调度/音效 | 支持T2V/I2V/R2V/V2V; 原生音频+视频联合生成; 多模态参考(图片/音频/视频); 支持文字生成(广告语/字幕/气泡台词); 支持视频编辑(元素增删改/延长/轨道补齐) |
| **Seedance 1.5 Pro** | 主体 + 动作 + 场景 + 镜头 + 风格 | 更快的生成速度 |
| **Seedance 1.0 Pro / Pro Fast** | 主体 + 动作 + 场景 + 镜头 + 风格 | Pro Fast: 极致速度 |
| **图生视频 (I2V)** | 动作 + 镜头 + (情绪/照明) | 由图像提供主体+场景, 提示词只控制动态 |
| **智能多帧** | [多帧图像] + [每帧时长] + [运镜提示词] | 多图驱动一镜到底; 上传2-10帧; 每帧1-6s |

## Core Methodology

The video prompt formula extends the image formula with two critical dimensions: **motion** and **camera**.

**For 视频3.0/3.0 Pro 文生视频:**
```
主体 + 动作 + 场景 + 镜头 + 风格 + (情绪演绎) + (照明)
```

**For 图生视频 (image-to-video):**
```
动作 + 镜头 + (情绪/照明)
```

**For Doubao Seedance 2.0 系列 文生视频:**
```
主体 + 动作/运动 + 空间背景/光影/风格 + 镜头调度/音效
```

The key difference from text-to-image prompting:
- **Motion is mandatory**: a video without motion is just a still image
- **Camera adds storytelling**: how the camera moves determines the viewer's emotional experience
- **Duration shapes pacing**: a 5-second clip needs different action density than a 10-second clip
- **For 视频3.0 Pro specifically**: 自然语言自由书写, 核心思路是"直观表达出你想要的效果"
- **For Doubao Seedance 2.0**: 支持多模态参考(图片/音频/视频), 可在提示词中用"图片1""图片2"指代参考素材

## How to use this skill

### Step 1: Identify video scenario category
→ Load `rules/video-category-table.md` to match user's request to the right category and example file

### Step 2: Load reference materials

**Load video vocabulary — choose by what you need:**

| 需要什么 | 加载文件 |
|----------|----------|
| 人物动作、自然动态、动物动态、机械运动 | `video-words/motion.md` |
| 场景环境、视频画质、视频风格、氛围情绪、节奏描述 | `video-words/scene-style.md` |

**Load camera movement references — choose by complexity:**

| 需要什么 | 加载文件 |
|----------|----------|
| 推拉摇移跟升降 | `camera-basic.md` |
| 环绕、一镜到底、希区柯克、运镜情感映射 | `camera-advanced.md` |

**Load reference guides:**
- `references/jimeng-video-3.0-guide.md` — when user mentions 视频3.0/3.0 Pro
- `references/smart-multi-frame-guide.md` — when user mentions 智能多帧/多帧/一镜到底

**For color descriptions**, cross-reference text2image's `color-library/chinese-traditional.md` or `gugong-384-colors.md`.

### Step 3: Build the prompt
→ Load `rules/video-core-methodology.md` for component-by-component build guide + presentation format

### Step 4: Apply video writing rules
→ Load `rules/video-writing-rules.md` for all 10 rules (motion, camera, duration, light, model-matching, differentiation, action layers)

### Step 5: Validate
→ Load `rules/video-validation-checklist.md` and run through all checks

### Step 6 (User assessment): Evaluate prompt output
When the user provides an existing prompt output and asks for evaluation ("评估""检测命中率""看看优化方向"):
→ Load `references/evaluation-framework.md` for the systematic 6-dimension assessment methodology

## Gotchas

1. **Action must be explicit** — 即梦 cannot infer motion from static description. "一个人在街上" = static shot
2. **Complex interactions fail** — multi-person interactions + camera movement = distortion risk
3. **Chinese camera terms work better** — "镜头缓缓推近" > "dolly in slowly"
4. **Seedance quality/speed tradeoff** — seedance2.0 = highest quality/slowest; fast = faster/lower quality
5. **Duration-to-action matching** — 5s with 3-stage action = rushed. Match complexity to time
6. **First-time web authorization** — some models require browser auth before first use
7. **Character consistency not guaranteed** — same face across segments not reliable
8. **Camera + complex motion = risk** — prioritize one over the other
9. **Model-prompt mismatch is the #1 output killer (Rule 8)** — long descriptive prose → 视频3.0 Pro; structured short sentences → Seedance 2.0. Mismatching causes detail loss and poor generation. **This is the single most common error in real usage.**
10. **Action layer count by model (Rule 10)** — Seedance 2.0 can't handle 4+ action layers reliably. Cap at 3. 视频3.0 Pro can handle 4-5.
11. **Multi-scheme differentiation is non-optional (Rule 9)** — When providing 2+ alternatives, verify visual distinction. At least 2 dimensions must differ (运镜/动作密度/景别/节奏/场景). Similar schemes waste user's time.
12. **Light must change, not just exist (Rule 5)** — "洒入" is a static snapshot. Use "缓缓流动""逐渐变亮""光影移动" to encode time passage.
13. **⚠️ Never write hex color codes in video prompts** — Same as image prompts: `#RRGGBB` values get rendered as text in the video frames, NOT as color instructions. Use Chinese color names only

## Available Resources

| Resource | Description | When to Load |
|----------|-------------|--------------|
| `rules/video-category-table.md` | 12 video scenario categories | Step 1 |
| `rules/video-core-methodology.md` | Component-by-component build guide | Step 3 |
| `rules/video-writing-rules.md` | 10 video-specific writing rules | Step 4 |
| `rules/video-validation-checklist.md` | 基础+进阶+多方案校验清单 | Step 5 |
| `video-words/motion.md` | Motion vocabulary library | When writing motion descriptions |
| `video-words/scene-style.md` | Scene/style/vocabulary library | When describing scenes |
| `camera-basic.md` | 7 basic camera movements | Basic camera work needed |
| `camera-advanced.md` | 7 compound moves + emotion mapping | Advanced camera work |
| `references/jimeng-video-3.0-guide.md` | 视频3.0/3.0 Pro: 8 dimensions | User mentions 视频3.0 |
| `references/smart-multi-frame-guide.md` | 智能多帧: 多图一镜到底 | User mentions 智能多帧/多帧 |
| `references/evaluation-framework.md` | 6维评估框架: 词库命中率/规则遵从度/公式完整性/模型匹配/区分度/校验 | User asks to assess/evaluate skill output |

<!-- QUALITY_BASELINE_V1 -->
## When to use（什么时候使用）

当用户需要 **在明确输入、预算和交付约束后执行生成或写入操作** 时加载本技能。先从请求中提取目标、输入、约束、交付格式和验收标准；描述摘要为：Use when the user wants to write, refine, or optimize a video-generation prompt for 即梦 (Dreamina/Jimeng) video models (视频3.0 Pro, Doubao Seedance 2.0, Seedance 1.5/1.0, 智能多帧); mentions 文生视频, text2video, 视频提示词, 运镜, camera movement, 生成一段...的视频, 帮我写个视频; describes a scene they want as a video; or supplies a rough scene description. Covers 12 scenario categories with 35 annotated examples, adds explicit motion description and camera direction beyond image prompts, and includes a motion/camera word library plus 7 basic and 6 advanced compound camera techniques with emotional effect mappings.。

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
