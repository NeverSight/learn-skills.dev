---
name: model-selector
description: 根据用户的视频需求(场景、时长、音频、语言、平台限制、预算、是否需要本地部署/角色一致性等),从 16 个主流 AI 视频模型(12 商业 + 4 开源)中推荐最匹配的 1-3 个,并解释为什么。覆盖商业:Seedance 2.0、HappyHorse 1.0、Kling 3.0、Sora 2、Veo 3.1、**Gemini Omni**(2026-05 新)、Runway Gen-4.5/Aleph、Pika 2.5、Hailuo 02、Hunyuan Video 1.5、Wan 2.7、即梦 AI;开源:LTX-Video 0.9.7、Mochi 1、CogVideoX 5B、Higgsfield Soul。用于"用哪个 AI 视频模型好"、"Sora 还是 Kling"、"国内有什么模型"、"哪个免费"、"哪个支持中文"、"哪个能编辑已有视频"、"哪个能本地部署"、"哪个角色一致性最强"等触发场景。
---

# model-selector

15 个主流 AI 视频模型(11 商业 + 4 开源)的"购物顾问"。问用户 3-4 个关键问题,给出推荐 + 理由。

## 何时不用此 skill

- 用户已经确定要用某个模型 → 用对应的 `<model>-prompter` skill
- 用户问"提示词怎么写" → 用 `seedance-prompter` / `kling-prompter` / `happyhorse-prompter`
- 用户的提示词不工作 → 用 `seedance-debugger`

## 11 模型能力速查矩阵

| 模型 | 中文 | 音频 | 物理 | 编辑 | 时长 | 开源 | 国内可用 | 主战场 |
|---|---|---|---|---|---|---|---|---|
| **Seedance 2.0** | ★★★ | — | ★★★ | — | 15s | — | ✓ | 电影叙事 |
| **HappyHorse 1.0** | ★★★ | ★★ | ★★ | — | 15s（默认 5s） | — | ✓ | ASMR / 短片 |
| **Kling 3.0** | ★★★★★ | ★★★★ | ★★★★ | ✓ | 2m | — | ✓ | 中文剧情 / 图生视频 |
| **Sora 2** | ★★ | ★★★★ | ★★★★★ | — | 25s (Pro) | — | △ | 电影艺术片 |
| **Veo 3.1** | ★★ | ★★★★★ | ★★★ | — | 148s chained | — | △ | 多人对话 |
| **Gemini Omni** ⭐NEW | ★★ | ★★★ | ★★★ | ★★★★★ | 待定 | — | △ | **迭代编辑 / 文字渲染 / 跨模态** |
| **Runway Gen-4** | ★★★ | — | ★★★ | ★★★★★ | 30s | — | ✓ | **视频编辑** |
| **Pika 2.5** | ★★ | ★ | ★★ | — | 25s | — | ✓ | **创意特效** |
| **Hailuo 02** | ★★★ | — | ★★★★★ | — | 10s | — | ✓ | 物理动作 |
| **Hunyuan 1.5** | ★★★★ | — | ★★★ | ✓ | 10s | ★★★★★ | ✓ | **开源 / LoRA** |
| **Wan 2.7** | ★★★ | ★★★★★ | ★★★ | ✓ | 15s | — | ✓ | **数字人 lip-sync** |
| **即梦 3.0** | ★★★★★ | ★★ | ★★★ | — | 15s | — | ✓ | **中文 + 剪映集成** |

## 工作流程

### 步骤 1：问 3-4 个关键问题

不要全部问，挑最影响结果的 3-4 个：

| 维度 | 问题 |
|---|---|
| 时长 | "需要多长？5 秒 / 10 秒 / 15 秒以上？" |
| 音频 | "要原生音频吗？只要环境音 / 要对白 / 要 BGM / 不要" |
| 语言 | "是中文场景还是英文场景？" |
| 编辑性质 | "全新生成还是编辑已有视频？" |
| 平台限制 | "国内可用 / 国际可用 / 本地部署？" |
| 用途 | "短视频爆款 / 影视级 / 商业广告 / 个人创作？" |

### 步骤 2：按决策树推荐

```
是编辑已有视频？
├── Yes → Runway Aleph（独家）
└── No → 继续
    ├── 要数字人/真人对口型？
    │   └── Yes → Wan 2.7（业界最准）
    ├── 要多人对话+精确配乐？
    │   └── Yes → Veo 3.1
    ├── 中文剧情/中式美学？
    │   └── Yes → 即梦 3.0（创作者） / Kling 3.0（开发者 API）
    ├── 极致物理感（水/火/动作）？
    │   └── Yes → Hailuo 02 > Sora 2
    ├── 创意爆款特效（变身/融化）？
    │   └── Yes → Pika 2.5（Pikaffects）
    ├── 本地部署/开源/LoRA 训练？
    │   └── Yes → Hunyuan 1.5
    ├── 极致电影质感/艺术片？
    │   └── Yes → Sora 2 > Runway Gen-4
    ├── 5/10/15 秒紧凑短片 + 环境音？
    │   └── Yes → HappyHorse 1.0
    └── 复杂多镜头叙事？
        └── Yes → Seedance 2.0 / Kling 智能分镜
```

### 步骤 3：输出格式

```markdown
## 推荐模型

**最佳选择**：[模型名]
**理由**：[2-3 句话说明为什么]
**对应 skill**：[skills/xxx-prompter] （如果有）
**对应方法论**：[methodology/NN-xxx-公式.md]
**官方平台**：[链接]

**备选**：[模型名]
**为什么备选**：[一句话]

## 你的需求 → 我的判断

| 你的需求 | 对应能力 | 评级 |
|---|---|---|
| [需求 1] | [模型支持情况] | ★★★★★ |
| ... | ... | ... |
```

## 实战示例

### 例 1：用户问"我想做中文短剧"

**澄清问题**：
1. 短剧时长？10 秒以内的片段还是 1-2 分钟完整故事？
2. 要原生音频（角色对话）吗？
3. 偏向写实 / 古风 / 现代都市哪种？

**用户答**：单个片段 10 秒，要有对话，现代都市。

**输出**：

> **最佳选择**：**Kling 3.0**
> **理由**：中文理解业界并列第一（与即梦），原生音频支持角色定向发声，最长 15 秒单段，5 层进阶公式天然适合剧情。
>
> **对应 skill**：[skills/kling-prompter](../kling-prompter/SKILL.md)
> **对应方法论**：[methodology/09-kling-公式.md](../../methodology/09-kling-公式.md)
> **官方平台**：[klingai.com](https://klingai.com)
>
> **备选**：**Wan 2.7**（如果对话很多且需要数字人感强）/ **即梦 3.0**（如果在剪映里直接做后期）

---

### 例 2：用户问"我有一段视频想改个风格，比如变水彩动画"

**判断**：编辑已有视频 → 直接推荐 Runway Aleph。

**输出**：

> **最佳选择**：**Runway Aleph**
> **理由**：编辑已有视频是 Aleph 的独家能力（其他 10 个模型都做不到）。`re-style` 动词专门用于风格转换，能保持原始运动和时序不变。
>
> **示例 prompt**：
> ```
> Re-style this clip as a hand-painted watercolor animation. Soft brush textures, flowing edges, warm palette. Preserve all motion and timing exactly.
> ```
>
> **对应方法论**：[methodology/13-六大模型公式速查.md#1-runway-gen-4--aleph](../../methodology/13-六大模型公式速查.md)
> **官方平台**：[Runway](https://runwayml.com)
>
> **备选**：没有真正可替代的。如果非要，Hunyuan 视频也能改一些（开源），但不是 native 编辑能力。

---

### 例 3：用户问"我自己想搭一个本地视频生成，预算有限"

**澄清问题**：
1. GPU 配置如何？（24GB / 12GB / 8GB）
2. 主要用途？（个人玩 / 自训 LoRA / 商业）

**用户答**：RTX 4090 24GB，想自训 LoRA。

**输出**：

> **最佳选择**：**Hunyuan Video 1.5**（8.3B 版本）
> **理由**：开源最强、24GB 显存可跑、原生支持 LoRA 训练、社区活跃（ComfyUI 完整工作流支持）。
>
> **推荐参数**：`Q5_K_M GGUF + 30 steps + dpmpp_2m_sde + sgm_uniform + cfg 6.0`
> **官方资源**：
> - GitHub: [Tencent-Hunyuan/HunyuanVideo-1.5](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5)
> - HuggingFace: [tencent/HunyuanVideo-1.5](https://huggingface.co/tencent/HunyuanVideo-1.5)
> - ComfyUI 教程: [docs.comfy.org](https://docs.comfy.org/tutorials/video/hunyuan/hunyuan-video)
>
> **备选**：CogVideoX（智谱开源）/ LTX Video（Lightricks 实时）— 这两个未纳入本仓库主目录，但同属开源阵营。

## 参考

- 11 模型能力对比详表：[methodology/13-六大模型公式速查.md](../../methodology/13-六大模型公式速查.md)
- 五大模型公式对照：[methodology/10-跨模型对比.md](../../methodology/10-跨模型对比.md)
- 官方资源汇总：[RESOURCES.md](../../RESOURCES.md)
