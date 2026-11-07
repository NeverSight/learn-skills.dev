---
name: happyhorse-prompter
description: 生成符合 HappyHorse 1.0 严格规则的紧凑提示词（30-55 词），主体先行 + 明确镜头技术 + 音频激活路径（with X audible / speaking English at natural pace）。可选加入"8s 时序节拍"结构。用于"用 HappyHorse 生成视频"、"做个 3-15 秒短片"、"要原生带音频的视频"、"ASMR 视频提示词"等触发场景。
---

# happyhorse-prompter

HappyHorse 1.0（阿里巴巴 Kling 团队）的核心差异：**原生音视频联合生成 + 严格按字数执行**。这个 skill 帮你产出符合它脾气的紧凑提示词。

## 何时不用此 skill

- 需要 10-15 秒长视频 / 多镜头切换 → 用 [seedance-prompter](../seedance-prompter/) 或 [seedance-storyboard](../seedance-storyboard/)
- 复杂叙事 / 多主体 → 用 Seedance
- 已有提示词调不出来 → 还在 HappyHorse 范围内的话可以让我帮看，否则用 [seedance-debugger](../seedance-debugger/)

## 五大黄金规则

详见 [methodology/02-进阶公式.md](../../methodology/02-进阶公式.md)。

### 规则 1：主体先行，动作其后

- ❌ `Walking through a forest, a woman...`
- ✅ `A woman in hiking gear walking through a forest...`

### 规则 2：明确指定镜头技术

HappyHorse 对"特写""广角"的理解非常精确，**不要留给模型猜测**。

### 规则 3：提示词长度控制在 30-55 词

- 过短（<30 词） → 输出模糊
- 过长（>60 词） → 模型忽略后半段

写完数一下英文单词数。

### 规则 4：物理效果加运动描述词

头发、水、布料、烟雾、火焰：加 `slow motion`、`motion blur` 或 `fluid dynamics`

### 规则 5：明确指定音频内容

**音频激活路径**（这是 HappyHorse 区别于 Seedance 的核心能力）：

- `with rain on leaves audible` → 雨打树叶声
- `with engine roar audible` → 引擎轰鸣声
- `speaking English at a natural pace` → 自然英语对话
- `speaking Korean at a measured pace` → 韩语对话
- `with ambient coffee shop chatter audible` → 咖啡馆环境音
- `with the pour sound audible` → 倒水/液体声
- `with faint crackling sound audible` → 火苗噼啪声
- `with hoofbeats audible` → 马蹄声
- `with drone motor whine audible` → 无人机马达声
- `complete silence` / `near silence with faint wind audible` → 纯静或环境底噪

**不写音频提示** = 模型可能不生成音频或乱生成。**主动写**。

## 工作流程

### 步骤 1：判断要不要时序节拍

如果用户的需求包含**时间结构**（如"先静止 2 秒，然后画面渐显"、"前 3 秒做 A，后 5 秒做 B"），用 CrePal 时序节拍写法：

```
8s duration. First 2s: black. Slow fade reveals: [画面 A]...
```

否则直接写 30-55 词紧凑版。

### 步骤 2：按公式拼接

```
[主体（明确特征）] [动作（具体）] [场景] [镜头大小+运动] [光影] [音频路径] [质量/风格].
```

英文写。

### 步骤 3：数词

- 复制到一个字数统计工具或心算 → 严格 30-55 词
- 超过 55 词：删形容词（不删核心要素），保留主体/镜头/音频路径
- 少于 30 词：补充镜头大小或音频细节

### 步骤 4：输出格式

```markdown
## 生成的提示词

\`\`\`
[完整提示词]
\`\`\`

**词数**：N · **时长建议**：N-Ns · **比例**：[X:Y]
**音频路径**：[突出说明用了什么音频提示]
**可调点**：[换音频/换镜头/换光影都可以怎么改]
```

## ⚠️ 时长写法硬规则(每次必查)

**时长信息有 2 个去处,二选一,不能同时,也不能放错位置**:

| 用户场景 | 时长去处 | 写法 |
|---|---|---|
| 用户只说"做个 X 视频"(无明确时序) | **只放在外部元数据** | prompt 内**不写**时长;`**时长建议**:5-7s` 放在末尾元数据行 |
| 用户明确说"前 N 秒...然后..."(有时序节拍) | **放 prompt 最前面作时序锚点** | `Ns duration, first Ns: black. [content]` 这种结构 |

**反例**(❌ 不要这样写):
```
晨光透过咖啡店玻璃门...温暖琥珀色调,16:9,5 秒。  ← 把时长埋在 prompt 中段/末尾
```

**正例 A**(✓ 无明确时序 — prose 不带时长):
```
晨光透过咖啡店玻璃门,木质门牌"OPEN"翻转...
(门铃叮当声 + 咖啡机蒸汽嘶嘶声)
```
然后元数据行写:`**时长建议**:5s`

**正例 B**(✓ 有明确时序 — 时长前置):
```
5s duration. 晨光透过咖啡店玻璃门,木质门牌"OPEN"翻转...
```

**自检清单**(输出前必过):
1. [ ] prompt 内部是否出现"N 秒" / "Ns" / "持续 N 秒"等时长描述?
2. [ ] 如果出现,它是不是在最开头作为时序锚点?
3. [ ] 如果不在最开头,**搬到外部元数据行**,prompt 内删掉。

## 实战示例

**用户输入**:"做个雨夜街头吉他手的视频"

**判断**：6-8 秒紧凑场景，需要带音频（吉他声+雨声）→ 不需要时序节拍，用紧凑模板。

**输出**：

```
A guitar player busking on a rain-slicked city street at night, medium shot, neon reflections on wet pavement, rain falling softly, with acoustic guitar sound audible, warm tungsten light from shop windows.
```

**词数**：30 · **时长建议**：6-8s · **比例**：16:9
**音频路径**：`with acoustic guitar sound audible` 激活原生吉他音轨；环境雨声不写也会带（因为画面就是雨）。
**可调点**：把 `warm tungsten light from shop windows` 换成 `harsh sodium streetlight only` 改成冷峻感；加 `with light rain on awning audible` 强化雨声层次。

---

**用户输入**："想要 8 秒，前 2 秒黑屏，然后慢慢揭示一片山谷"

**判断**：明确的时间结构 → 用时序节拍模板。

**输出**：

```
8s duration, first 2s: black. Slow fade reveals: wide shot, mountain valley at dawn, low mist between pine trees, single dirt road leading into the scene, no people. Camera very slowly pushes forward on a dolly. Soft blue-gold light on the horizon. Quiet, cinematic, high production value.
```

**词数**：48 · **时长建议**：8s · **比例**：16:9
**音频路径**：未指定 → HappyHorse 默认匹配晨间风声底噪；可加 `with distant birdsong audible` 进一步强化。
**可调点**：把 `dirt road` 换成 `wooden cabin in distance` 增加视觉锚点；`blue-gold light` 改 `pink-orange` 调更暖。

## 图转视频（已有参考图）的正确姿势

当有参考图时，**不要重复描述图中已有的内容**，专注于描述变化：

| ✅ 应该写 | ❌ 不要写 |
|---|---|
| `walks toward camera` / `head turns left` | 重复图中已有的服装颜色 |
| `slow push-in` / `lateral tracking right` | 重复图中已有的构图 |
| `hair drifts` / `fabric ripples` / `steam rises` | 重复图中已有的主体外观 |

## 参考资源

- 进阶公式：[methodology/02-进阶公式.md](../../methodology/02-进阶公式.md)
- 运镜词典：[methodology/05-运镜词典.md](../../methodology/05-运镜词典.md)
- 57 条实测提示词：[prompts/happyhorse/README.md](../../prompts/happyhorse/README.md)
