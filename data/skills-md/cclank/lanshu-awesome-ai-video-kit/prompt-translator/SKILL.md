---
name: prompt-translator
description: 把一条 AI 视频提示词从源模型(如 Sora 2)的写法风格转换为目标模型(如 Kling 3.0 / Wan 2.7 / Veo 3.1 等)的最佳实践写法。基于 110 条 10 场景 × 11 模型对照基准数据(prompts/data/cross-model-matrix.json),不是凭直觉重写,而是查表式 in-context learning。10 场景:产品 / 双人对话 / 物理动作 / 图生视频 / 多人会议 / 恐怖 / 自然延时 / 抽象 / 武侠 / 萌宠。用于"Sora 已 EOL 帮我把这条提示词改成 Veo"、"我有 Kling 提示词想跑 Wan"、"跨模型 A/B 测试"、"把英文 prompt 优化成 Kling 中文版"等触发场景。
---

# prompt-translator

跨模型提示词转换器。**关键差异**:不是凭 AI 直觉重写,而是**查 110 条对照基准做 in-context learning**。

## 何时不用此 skill

- 用户从零开始写一条新提示词(不是转换) → 用 `seedance-prompter` / `kling-prompter` / `happyhorse-prompter` 或 `model-selector`
- 用户问"用哪个模型好" → 用 `model-selector`
- 已有提示词出问题但不换模型 → 用 `seedance-debugger`

## 核心数据资产

**[`prompts/data/cross-model-matrix.json`](../../prompts/data/cross-model-matrix.json)** — 这就是 translator 的"训练数据":

- **10 个核心场景**:产品广告 / 情感重逢 / 滑板动作 / 图生视频 / 多人会议 / 恐怖悬疑 / 自然延时 / 抽象艺术 / 武侠决斗 / 萌宠爆款
- **每个场景 × 11 模型 = 110 条对照 prompt**,每条严格遵循对应模型的官方公式
- 这构成"同一场景在 11 模型上的最佳写法对照",**就是 translator 的查找表**

## 工作流程

### 步骤 1:接收输入

最少需要:
- **源模型** (如 Sora 2 / Kling 3.0 / Wan 2.7)
- **源 prompt** (用户的现有提示词)
- **目标模型** (用户想转到哪个)

可选:
- 转换偏好(更简洁 / 更详细 / 保留中文)

### 步骤 2:分析源 prompt 的语义内容

提取**核心场景元素**(与具体写法风格无关的):
- 主体(subject):是谁/什么
- 场景(scene):在哪/什么环境
- 动作(motion):发生了什么时序事件
- 情绪(mood):整体氛围
- 镜头(camera):怎么拍
- 音频(audio):需要什么声音
- 对白(dialogue):有无台词
- 风格(style):视觉锚点

这一步是**剥离风格,提取语义**。把 Sora 的 `Style: → Cinematography: → Actions:` 分层结构里的实际内容,抽象成"核心场景描述"。

### 步骤 3:查 110 条基准对照表找最相似场景

读取 [`prompts/data/cross-model-matrix.json`](../../prompts/data/cross-model-matrix.json),在 10 个场景里找**与用户输入最相似的 1-2 个场景**:

| 用户输入像... | 参考场景 |
|---|---|
| 产品旋转 / 静态主体特写 | scene-1-perfume |
| 双人对白 / 情感叙事 | scene-2-reunion |
| 户外动作 / 物理运动 | scene-3-kickflip |
| 图生视频(有参考图) | scene-4-i2v-cafe |
| 多人对话 / 室内会议 | scene-5-meeting |
| 恐怖悬疑 / 慢推进氛围 | scene-6-horror-balloon |
| 自然延时 / 无人景观 | scene-7-mountain-sunrise |
| 抽象艺术 / 流体特效 | scene-8-liquid-metal |
| 武侠 / 中式打斗 | scene-9-wuxia-duel |
| 萌宠 / 病毒短视频 | scene-10-surfing-dog |

### 步骤 4:基于相似场景的对照模式,做转换

**在 prompt 里给 Claude 这样的 few-shot 模板**:

```
我要把这条 [源模型] 的 prompt 转换成 [目标模型] 的最佳写法。

【参考对照】下面是一个相似场景在两个模型上的对照写法:

[源模型 in scene-N]:
{基准数据中该场景在源模型上的 prompt}

[目标模型 in scene-N]:
{基准数据中该场景在目标模型上的 prompt}

注意观察:
- 字段标签的变化 (e.g. "Cinematography:" → "Camera:" → "镜头:")
- 段落结构的变化 (e.g. 分层 → 5 层 → Entity+Scene+Motion+Sound)
- 措辞密度的变化 (e.g. 100 词 → 30 词 → 中文短句)
- 音频处理的变化 (e.g. "Background Sound:" → "Audio:" → "Sound:")

【用户的源 prompt】
{源 prompt}

【请输出】基于上面对照模式,将用户 prompt 转换为目标模型最佳写法。保留所有语义内容,仅调整结构/标签/措辞。
```

### 步骤 5:输出格式

#### ⚠️ 目标格式硬约束(每次必查)

**无论源 prompt 是 prose 还是带标签,目标 prompt 必须严格遵循目标模型在 `cross-model-matrix.json` 里的标签格式**。不要 prose 化输出。

| 目标模型 | 必带标签 / 结构 | 反例(LLM 容易犯) |
|---|---|---|
| Kling 3.0 | `Scene:` / `Characters:` / `Action:` / `Camera:` / `Audio & Style:` / `Negative:` | ❌ 一段 prose 把 5 层揉进自然语言 |
| Sora 2 | `Style:` / `Cinematography:` / `Actions:`(- beats)/ `Background Sound:` / `Dialogue:` | ❌ 合并成单段描述 |
| Veo 3.1 | 8 元素 + `Dialogue:` / `Audio:` 双标记 | ❌ 漏 Dialogue/Audio 显式标签 |
| Wan 2.7 | `Entity:` / `Scene:` / `Motion:` / `Sound:` 四段 | ❌ 揉成一段 |
| Seedance 2.0 | 8 要素 prose 单段(主体+动作+场景+光+相机+风格+音频+约束) | ✓ 这家就是 prose |
| HappyHorse 1.0 | 紧凑 prose 30-55 词;明确时序时 `Ns duration.` 开头 | ❌ 把时长埋在中段 |
| Hailuo 02 | 克制简洁 prose,1-3 句 | ❌ 堆砌过长 |
| Pika 2.5 | 单一焦点 prose,`Negative:` 必带 `no morphing` | ❌ 多主体堆叠 |
| Runway Gen-4.5 | prose + Aleph 编辑动词(`recolor / add / remove`) | ❌ 描述静态而非编辑动作 |
| Hunyuan / LTX / Mochi / CogVideoX | 详细 prose,单段 | — |
| 即梦 / Jimeng | 8 维度公式(同 Seedance) | ❌ 漏维度 |

**自检清单**(输出前必过):
1. [ ] 目标 prompt 有没有上表对应的标签/结构?
2. [ ] 数据库 `cross-model-matrix.json` 中该模型该场景的 prompt 长什么样?我的输出格式跟它一致吗?
3. [ ] 如果不一致,**重写**,不要凑合。

#### 输出模板

```markdown
## 转换结果

**源模型**: [Sora 2] · **目标模型**: [Kling 3.0]
**参考场景**: [scene-N-xxx · 用户输入最像哪个对照场景]

\`\`\`
[转换后的目标模型 prompt — 必须带上表对应标签]
\`\`\`

## 转换映射(供检查)

| 源结构 | 目标结构 | 注释 |
|---|---|---|
| Style: ... | Scene: + Audio & Style: | Sora 单一 Style 段拆成 Kling 的环境+风格混合 |
| Cinematography: ... | Camera: | 字段重命名 |
| Actions: - beat - beat | Action: 流畅描述 | 按 beats 列表合并成自然语言 |
| Background Sound: ... | Audio & Style: | 合并进风格段 |
| (无角色对白栏) | (保留对白嵌入 Action) | Kling 5 层不单独分对白 |

## 注意事项

- ⚠️ [目标模型] 与 [源模型] 在 [某能力] 上有差异:[具体说明,例如 "Kling 中文比 Sora 强,可考虑改成中文版本"]
- 💡 推荐参数:[根据目标模型给出宽高比/时长/分辨率建议]
- 🔄 如果效果不理想,试试:[备选转换方向,如再转 Veo 用多人对话能力]
```

## 实战示例

### 例 1:用户给一条 Sora 2 提示词,想转成 Kling 3.0

**输入**:
> 源模型:Sora 2
> 源 prompt:
> ```
> Style: 1970s romantic drama, 35mm film with warm halation, slight handheld micro-shake.
> A park bench at golden hour in late autumn. Two men in their early 30s.
> Cinematography: Medium-wide, slow dolly-in. 40mm lens, shallow focus.
> Actions:
> - A sits down hesitantly
> - A (low, hesitant): "It's been a long time."
> - B turns, eyes widening
> - B (warm): "Too long. I almost didn't recognize you."
> - Both share a quiet laugh
> Background Sound: Soft piano, ambient park, no music swell.
> ```
> 目标模型:Kling 3.0

**步骤 2-3**:识别这是 scene-2-reunion(情感对话)场景。

**步骤 4**:读基准数据中 scene-2-reunion 的 sora-2 和 kling-3.0 对照,提取转换模式。

**输出**:
```markdown
## 转换结果

**源模型**: Sora 2 · **目标模型**: Kling 3.0
**参考场景**: scene-2-reunion(情感双人对话)

\`\`\`
Scene: A park bench at golden hour in late autumn, amber sunlight filtering through bare branches, fall leaves drifting through the frame.
Characters: Character A (early 30s, hesitant) and Character B (early 30s, expressive).
Action: A walks up and sits down beside B with visible hesitation. A says: "It's been a long time." B turns slowly, eyes widening with recognition, replies warmly: "Too long. I almost didn't recognize you." They share a quiet laugh that breaks the tension.
Camera: Slow push-in on A as he speaks, over-the-shoulder cut to B's reaction, ending on a held wide two-shot.
Audio & Style: Soft solo piano underscore building gently, ambient park sounds (distant kids playing, leaves rustling), warm cinematic teal-and-amber grade, 1970s romantic drama with 35mm halation aesthetic, naturalistic dialogue delivery.
\`\`\`

## 转换映射

| Sora 2 | Kling 3.0 | 注释 |
|---|---|---|
| Style: ... | (合并到 Audio & Style:) | Kling 5 层把 Style 嵌在最后一层 |
| Cinematography: 段 | Camera: | 字段重命名,Kling 更简洁 |
| Actions: beats + dialogue 嵌入 | Action: 自然语言 + 嵌入对白 | Kling 5 层 Action 段直接含对白,不像 Sora 用 beats 列表 |
| Background Sound: | (合并到 Audio & Style:) | Kling 把音频与视觉风格放一段 |
| (无 Characters: 段) | Characters: 显式列角色 | Kling 5 层强制要求 Characters: 段 |

## 注意事项

- ✅ Kling 5 层结构能很好承接 Sora 的所有内容
- 💡 推荐参数:16:9 / 10s / 1080p
- 🌐 Kling 中文理解优于 Sora,如果场景偏中式可把对白和场景描述改成中文(Kling 中文是业界并列第一)
- 🔄 如果想要更强的音画对白同步,再转 Veo 3.1(原生音频最强)
```

### 例 2:用户的 Wan 2.7 提示词转 Hailuo 02

(同样的查表流程,参考 scene-5-meeting 或最相似场景的 wan-2.5 ↔ hailuo-02 对照行)

### 例 3:用户的 Kling 中文 prompt 转回 Pika 简洁英文

(参考 scene-1-perfume 或最相似场景的 kling-3.0 ↔ pika-2.5 对照行,**强调 Pika 的"单一焦点 / no morphing"约束**)

## 局限性 — 必须诚实告知

⚠️ **本 skill 是基于 110 条公式对照数据的查表式转换,不是基于实测视频效果的端到端优化**。

**做不到**:
- 无法保证转换后的 prompt 在目标模型上实际生成的视频质量
- 无法预测目标模型的特殊脾气(模型频繁迭代)
- 无法替你做最终的 A/B 测试 — 这必须实际跑

**能做到**:
- 把源 prompt 重新组织成符合目标模型公式的结构
- 保留所有语义内容(主体/场景/动作/音频/风格)
- 指出关键的字段映射和风格差异
- 给出推荐参数和后续优化方向

**最佳实践**:把转换结果作为"起草稿",在目标平台实测后微调。如果发现某条转换效果稳定,欢迎 PR 加到 [`cross-model-matrix.json`](../../prompts/data/cross-model-matrix.json) 作为新场景的对照样本(详见 [CONTRIBUTING.md](../../CONTRIBUTING.md))。

## 路线图(等数据更扎实再做)

| 版本 | 增强 |
|---|---|
| v1(当前) | 110 条对照查表 + 5 步流程 |
| v2 | 加 5 场景扩到 165 条对照 |
| v3 | 加每条对照的实测视频链接(由社区贡献) |
| v4 | 加自动 A/B 评估(同 prompt 在多模型实测后的 ELO 评分驱动) |

## 资源

- 基准数据:[`prompts/data/cross-model-matrix.json`](../../prompts/data/cross-model-matrix.json)
- 数据说明:[`prompts/cross-model/README.md`](../../prompts/cross-model/README.md)
- Web 查询界面:[`tools/cross-model/index.html`](../../tools/cross-model/index.html)
- 各模型公式:[`methodology/`](../../methodology/) 13 篇 SOP
- 跨模型对比:[`methodology/10-跨模型对比.md`](../../methodology/10-跨模型对比.md) + [`methodology/13-六大模型公式速查.md`](../../methodology/13-六大模型公式速查.md)
