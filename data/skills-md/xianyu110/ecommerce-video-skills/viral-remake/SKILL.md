---
name: viral-remake
description: "爆款拆解复刻：把抖音/TikTok 爆款带货视频（链接、转写或口述结构）拆成 8 维结构与 5-beat 节拍，再映射到你的商品，输出拆解表 + 3 个复刻角度 + 可渲染 storyboard.json。Use when the user says 爆款, 拆解, 复刻, 对标, 仿拍, viral remake, breakdown, swipe file, copy structure, 竞品视频, remake a TikTok/Douyin product video, or wants to replicate a viral ecommerce short's structure with their own product."
---

# 爆款拆解复刻 · Viral Remake

丢一条爆款带货视频（链接 / 转写 / 口述结构），**拆出可复用骨架**，再换成你的商品，直接出能喂给 `ffmpeg-auto-assemble` 的 `storyboard.json`。

复刻的是 **结构与节奏**，不是画面、配乐或台词原文。

> Part of [ecommerce-video-skills](https://github.com/xianyu110/ecommerce-video-skills)

## 一句话用法（给 agent）

```text
用 viral-remake 拆这条抖音爆款，换成我的保温杯复刻一条 15 秒分镜
```

## 输入 Inputs

| 字段 | 说明 |
|---|---|
| 爆款来源 | 视频链接 **或** 用户粘贴的转写 **或** 用户口述的节拍/结构（agent **不下载/不爬** 付费墙内容；没有成片时就按转写/口述拆） |
| 目标商品 | 品名、人群、场景、**用户确认过的真实卖点**（数字/效果只能用这些） |
| 平台 | 抖音 / TikTok Shop / 视频号 / 小红书 / Reels … |
| 时长目标 | 默认 15s；可指定 30s / 60s |
| 可用素材 | 商品图 / 场景图 / 实拍片段文件名（没有就标 TODO） |

## 步骤 Steps

1. **收集输入**：确认平台、时长、目标卖点；若只有链接且看不了成片，请用户贴转写或口述 5-beat。
2. **拆解 8 维**（见下表）：钩子类型、前 3 秒画面、节拍时间轴、情绪温度、花字/字幕节奏、证明方式、CTA 形态、可复用 vs 不可复用。
3. **标红不可复用**：品牌专属梗、版权素材（成片画面/配乐/原台词）、无法证明的数据/认证/销量 → 一律不可复用，复刻时替换或删除。
4. **映射到目标商品**：只保留可复用骨架；每个数字/效果改成用户确认过的真实卖点；钩子可交给 `hook-3s-script` 细化。
5. **出 3 个复刻角度**（见下）：保守同构 / 同构换钩子 / 同构换证明；与用户确认选 1 个。
6. **输出**：Markdown 拆解表 + 所选角度的 `storyboard.json`（字段对齐 `assemble.py`）。
7. **合规自检**（Checklist）→ 接入流水线渲染。

## 拆解 8 维 · 8-dimension breakdown

| # | 维度 | 记什么 | 示例（虚构爆款 → AURA 演示） |
|---|---|---|---|
| 1 | 钩子类型 | 痛点提问 / 反差 / 结果先行 / 数字 / 场景…（见 `hook-3s-script`） | 痛点提问：「冰水不到中午就温了？」 |
| 2 | 前 3 秒画面 | 第一帧是什么、有没有商品、有没有花字 | 户外手持杯特写 + 花字弹出 |
| 3 | 节拍时间轴 | **5-beat**：Hook → Problem → Solution → Proof → CTA（可合并镜） | 0–3 / 3–5 / 5–8 / 8–13 / 13–15 |
| 4 | 情绪温度 | 吐槽 / 安利 / 冷静测评 / 紧迫感 / 轻松 | 前半吐槽，后半安利 |
| 5 | 花字/字幕节奏 | 关键词何时弹出、是否分句、高亮词 | 每镜 1 个高亮词，CTA 单独大花字 |
| 6 | 证明方式 | 演示 / 对比 / 细节特写 / 使用场景 / 口播数字 | 倒冰块演示保冰；拧盖演示不漏 |
| 7 | CTA 形态 | 点链接 / 搜同款 / 评论区 / 关注 | 「想要同款，点下方链接」 |
| 8 | 可复用 vs 不可复用 | 骨架✅；品牌梗❌；版权画面/配乐/原台词❌；未证实数据❌ | 「XX 明星同款」❌；「24h 保冰」仅用户测过才✅ |

### 5-beat 节拍（默认 15s）

```text
Hook (0–3s)      → 停住划走：场景 + 痛点 / 反差
Problem (3–5s)   → 放大痛点或旧方案失败（可与 Hook 合并）
Solution (5–8s)  → 产品亮相 + 一句话是什么
Proof (8–13s)    → 1–2 个可被看见的证明（演示/对比/细节）
CTA (13–15s+)    → 行动号召 + 贴纸；min ≥ 3s 方便点
```

## 映射规则 · Map to your product

- **只替换可复用骨架**：节拍、情绪弧线、证明类型、花字节奏可以留；台词、画面、品牌梗全部重写。
- **数字 / 效果**：必须来自用户确认的卖点清单；源视频里的「10 万好评 / 实验室级 / 第一」等 → 删除或改成可证明的说法。
- **证明方式优先可视化**：能演就不要只靠口播数字（倒水、拧盖、前后对比）。
- **缺图**：标 `TODO`，建议交给姊妹仓库 [ecommerce-image-skills](https://github.com/xianyu110/ecommerce-image-skills) 或 [gptimage2.asia](https://gptimage2.asia/) 出图，再回填路径。

## 三个复刻角度 · 3 remake angles

| 角度 | 怎么做 | 适合 |
|---|---|---|
| **A 保守同构** | 5-beat、钩子类型、证明方式都对齐源结构，只换商品与真实卖点 | 想要最接近「爆款手感」 |
| **B 同构换钩子** | 节拍与证明不变，钩子换成另一类型（可跑 `hook-3s-script` 出 6–10 版再选） | 同品类已经有人仿拍过同钩子 |
| **C 同构换证明** | 节拍与钩子不变，证明从「口播数字」改成「演示/对比」或反过来 | 你有实拍素材但卖点数字测不全 |

每个角度给：一句话差异说明 + 推荐理由；用户选定后再写完整 `storyboard.json`。

## 输出模板 · Output templates

### 1) Markdown 拆解表

```markdown
## 爆款拆解 · {源视频一句话 / 口述}

| 维度 | 源视频 | 可复用？ | 映射到 {目标商品} |
|---|---|---|---|
| 钩子类型 | … | ✅/❌ | … |
| 前 3 秒画面 | … | ✅骨架 / ❌画面 | … |
| 5-beat | Hook→…→CTA | ✅ | … |
| 情绪温度 | … | ✅ | … |
| 花字节奏 | … | ✅ | … |
| 证明方式 | … | ✅类型 / ❌具体数据 | … |
| CTA | … | ✅ | … |
| 不可复用清单 | 品牌梗、原配乐、未证实销量… | ❌ | 已删除/替换 |

### 复刻角度
- A 保守同构：…
- B 同构换钩子：…
- C 同构换证明：…
**选用：{A/B/C}**
```

### 2) storyboard.json（字段对齐 assemble.py）

```json
{
  "title": "{商品} · 爆款复刻 {时长}s（演示）",
  "voice": "zh-CN-YunxiNeural",
  "rate": "+12%",
  "bgm": "auto",
  "tag": "{品牌} · 复刻演示",
  "shots": [
    {"image": "assets/lifestyle.webp", "motion": "punch", "transition": "slideup",
     "line": "钩子台词（≤18字）", "sub": "钩子**关键词**", "title": "花字≤10字"},
    {"image": "assets/white-bg.webp", "motion": "zoom_in", "transition": "fade",
     "line": "产品亮相", "sub": "换这只 **{品牌}** 试试"},
    {"image": "assets/proof.webp", "fit": "blur", "motion": "pan_down", "transition": "slideleft",
     "line": "证明一台词（真实卖点）", "sub": "卖点|**证明**", "title": "短花字"},
    {"image": "assets/scene.webp", "motion": "zoom_out", "transition": "fade",
     "line": "场景/卖点二", "sub": "场景 **关键词**"},
    {"image": "assets/end-card.png", "motion": "zoom_in", "min": 3.0,
     "line": "想要同款，点下方链接看看。", "sub": "", "cta": "点击下方链接 ›"}
  ]
}
```

常用字段：`image` / `video` / `motion` / `line` / `sub` / `title` / `cta` / `min` / `fit` / `transition` / `line_en` / `sub_en` / `title_en` / `cta_en`。细节见 `ffmpeg-auto-assemble`。

## 提示词模板 Prompt template

```text
你是电商短视频编导。按 viral-remake skill 拆解并复刻：
爆款来源：{链接 / 转写 / 口述 5-beat}
目标商品：{…}；真实卖点（不得编造）：{…}
平台：{抖音}；时长：{15s}；可用素材：{文件名列表}
要求：
1) 输出 8 维拆解表，标出可复用 vs 不可复用；
2) 给出 A 保守同构 / B 同构换钩子 / C 同构换证明 三个角度；
3) 按用户选定的角度输出 storyboard.json（字段含 image/motion/line/sub/title/cta/min/fit）；
4) 禁止绝对化用语；禁止贬低具名竞品；禁止编造销量/评分；复刻结构与节奏，不抄画面/配乐/台词原文。
```

## 接入流水线

```text
爆款链接/转写 ──► viral-remake ──► 拆解表 + 3 角度 + storyboard.json
                      │
                      ├─► hook-3s-script（可选：细化/替换钩子）
                      ├─► 缺图 → ecommerce-image-skills / gptimage2.asia
                      ▼
              ffmpeg-auto-assemble ──► MP4
                      │
              cover-title-ab / platform-spec-export / multilingual-dubbing
```

渲染示例：

```bash
python scripts/assemble.py examples/viral-remake-demo/storyboard.json -o out/remake.mp4
```

## 合规 Compliance（必须）

- 禁止：最、第一、顶级、国家级、100%、根治、以及无法证明的销量/评分/认证。
- 禁止贬低**具名**竞品；对比用「普通款 / 之前那只」。
- 禁止编造测过的时长、温度、泄漏等数据；演示卖点必须用户确认可拍到。
- 版权：不复制源视频画面、配乐、花字原句、口播原文；只迁移结构、节拍、证明类型。
- 平台广告与带货标识规则以官方最新说明为准。

## 检查清单 Checklist

- [ ] 8 维拆解齐全；不可复用项已标红并在复刻中删除/替换
- [ ] 5-beat 完整（可合并镜，但 Hook 与 CTA 都在）
- [ ] 给出 3 个角度且用户已选定（或默认 A 并注明）
- [ ] 所有数字/效果来自用户确认卖点；无绝对化、无贬低具名竞品
- [ ] `storyboard.json` 字段可被 `assemble.py` 消费；`python -m json.tool` 通过
- [ ] 缺素材镜头标了 TODO；未抄源视频画面/配乐/台词

## 常见问题与修复 Failure fixes

| 问题 | 修复 |
|---|---|
| 只有链接、看不到成片 | 请用户贴转写或口述 5-beat；不要假装已看过 |
| 复刻后仍像抄袭 | 重写全部台词与花字；换证明素材；钩子改类型（走角度 B） |
| 卖点数字来自源视频 | 删掉或换成用户测过的；改用可视化演示 |
| storyboard 渲染缺图 | 路径改相对 `storyboard.json`；或先出图再填 |
| 钩子不够劲 | 把第 1 镜交给 `hook-3s-script` 出 6–10 版再嵌回 |
| 想直接仿画面运镜 | 拒绝复制；只保留「特写→演示→场景」这类结构词，具体镜头重写 |
