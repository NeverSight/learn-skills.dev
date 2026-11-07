---
name: seedance-prompter
description: 把用户的自然语言视频需求转换为符合 Doubao Seedance 2.0 进阶公式的提示词（8 要素：精准主体+动作细节+场景环境+光影色调+镜头运镜+视觉风格+画质+约束条件）。用于"帮我写一个 Seedance 提示词"、"生成视频提示词"、"做个产品广告视频"、"用 Seedance 生成 XX"等触发场景。如果用户没明确说 Seedance，但描述的是单一镜头的复杂叙事/多主体/电影感视频，也优先用此 skill。
---

# seedance-prompter

把用户的"我想要什么样的视频"转换成 Seedance 2.0 能理解的工程级指令。

## 何时不用此 skill

- 用户描述的是 **5/10/15 秒紧凑短片** 或 **要原生带音频** → 用 [happyhorse-prompter](../happyhorse-prompter/)
- 用户已有提示词但效果不对 → 用 [seedance-debugger](../seedance-debugger/)
- 剧情复杂需要多镜头切换 → 用 [seedance-storyboard](../seedance-storyboard/)

## 核心方法论：进阶公式

```
精准主体 + 动作细节 + 场景环境 + 光影色调 + 镜头运镜 + 视觉风格 + 画质 + 约束条件
```

详见 [methodology/02-进阶公式.md](../../methodology/02-进阶公式.md)。

## 工作流程

### 步骤 1：澄清需求（必要时）

如果用户只给了一两句话（"做个香水广告"），先问清楚以下要素中至少 3 项（不要问全部，挑最影响结果的）：

| 要素 | 示例问题 |
|---|---|
| 主体 | "香水瓶什么样？玻璃透明还是磨砂？" |
| 动作 | "瓶子是静止展示还是旋转/喷雾？" |
| 场景 | "实景还是纯色背景？什么色？" |
| 光影 | "硬光戏剧感还是柔光高级感？" |
| 镜头 | "特写质感优先还是中景展示整瓶？" |
| 风格 | "电影感 / 商业广告 / 极简 / 复古？" |
| 时长/比例 | "竖屏短视频 / 横屏 / 多长？" |

**例外**：如果用户说"随便""快"或给了参考图，直接生成一版给他改。

### 步骤 2：按 8 要素填充

写英文（Seedance 对英文响应更好），但用户的核心元素用原文保留（人物名字、品牌名、专有名词）。

**模板骨架**：

```
[Subject with 2-3 stable identifying features].
[Action with specific body parts + speed/intensity].
[Scene/environment].
[Light source + time of day + color tone].
[Camera size + movement + angle].
[Visual style + film grain/aesthetic anchor].
[Quality: cinematic / 4K / photorealistic].
[Negative: avoid ...; no watermark; no logo; preserve face stability].
```

### 步骤 3：检查避免错误

提交前自查：

- [ ] 提示词 50-200 词之间？
- [ ] 一个镜头只指定 1 种运镜方式（不要同时推+拉+摇）？
- [ ] 没有矛盾词（如 `8mm` + `4K`、`slow motion` + `high speed`）？
- [ ] 有约束条件（至少 `no watermark, no logo`）？
- [ ] 多主体场景已用标签区分（"警察"/"小偷"）？

### 步骤 4：输出格式

给用户一份完整的提示词，加 3 个说明：

```markdown
## 生成的提示词

\`\`\`
[完整提示词]
\`\`\`

**推荐参数**：宽高比 [X:Y] · 时长 [N 秒] · 分辨率 1080p
**关键技巧**：[1-2 句说明这条提示词的设计思路]
**可调点**：[告诉用户可以怎么改 — 比如换光影/换风格/换镜头]
```

## 实战示例

**用户输入**："给我做个咖啡的广告"

**澄清问题**（一次性问，不超过 3 个）：
1. 镜头视角偏好 — 极特写质感（油花/蒸汽）还是中景实景（咖啡馆桌面）？
2. 情绪基调 — 温暖（晨间/木质） 还是 高端（黑底/聚光）？
3. 投放渠道 — 竖屏抖音 / 横屏电视 / 正方形 IG？

**用户答**：极特写、温暖、竖屏。

**输出**：

```
Extreme close-up of rich cream being poured into a freshly brewed dark espresso in slow motion, creating a mesmerizing vortex pattern across the crema surface. Wisps of steam rise softly from the cup. Warm tungsten side-light highlights the contrast between cream and coffee, casting soft amber reflections on the ceramic edge. The camera slowly pulls back from macro to medium shot, revealing a styled wooden café table with a sprig of cinnamon and a folded linen napkin. Commercial quality, appetizing warm color grading, 4K, shallow depth of field, photorealistic liquid dynamics. No text overlays, no watermark, no logo.
```

**推荐参数**：9:16 · 8 秒 · 1080p
**关键技巧**：单镜头单运镜（仅 pull back），用极特写 → 中景的尺度变化制造戏剧性，slow motion + 温暖色调强化食欲。
**可调点**：把 `tungsten side-light` 换成 `morning window light` 可改成晨间感；加 `with pour sound audible` 提示音频路径（注意：Seedance 2.0 需独立处理音频）。

## 参考资源

- 进阶公式：[methodology/02-进阶公式.md](../../methodology/02-进阶公式.md)
- **Masterclass(10 YouTube 教学综合)**：[methodology/15-seedance-masterclass.md](../../methodology/15-seedance-masterclass.md) ⭐ 9 要素公式 / Timeline Prompting / 5 种爆款 / VFX 技巧 / 8 个模板
- 运镜词典：[methodology/05-运镜词典.md](../../methodology/05-运镜词典.md)
- 约束词清单：[methodology/06-约束词清单.md](../../methodology/06-约束词清单.md)
- 117 条实测提示词：[prompts/seedance/README.md](../../prompts/seedance/README.md)

## 质量后缀(每条 prompt 都加)

> 来源:[Masterclass §1](../../methodology/15-seedance-masterclass.md) — *The ULTIMATE Seedance 2.0 Prompting Guide*

```
4K, ultra HD, rich detail, sharp clarity, cinematic textures, stable picture.
Maintaining face and clothing consistency without distortion or high detail.
Generate the video without subtitles.
```
