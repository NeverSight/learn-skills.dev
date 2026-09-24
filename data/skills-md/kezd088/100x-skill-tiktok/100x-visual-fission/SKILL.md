---
name: 100x-visual-fission
description: Fission a locked person/scene/product reference into a media-fission
  prompt matrix (single-frame / head-tail / head-mid-tail / multi-day frame structures
  x VTP's fixed camera/lighting/color-grading presets), with one fixed negative
  prompt constant. Use when the user asks to "帮我裂变这条视觉参考", "这个产品出几个变体",
  "生成裂变提示词矩阵", "媒介裂变", "视觉裂变", "fission this reference", "generate
  prompt variants for this product", "multiply this reference image into variants",
  or gives reversed person/scene reference material (or a plain-text description of
  it) plus a product brief and wants a VTP-style constants/variables template
  fissioned across frame structures and camera presets.
metadata:
  author: 100x
  version: "1.1.0"
---

# 100x-visual-fission

## 一句话定位
输入 ≥2 条同系列人物/场景参考（反推 JSON 或文字降级描述）+ 产品文案，输出锁定人物/场景/
产品身份的媒介裂变提示词矩阵：单帧/首尾/首中尾/数日见效四选一媒介结构 × VTP 原版 A/B/C
机位预设，附固定负面词常量。属于 100x 体系 L2 创意生成层，对应"5 视觉裂变"这一步。

## 何时触发
用户说：
- "帮我裂变这条视觉参考" / "这个产品出几个变体" / "生成裂变提示词矩阵" / "媒介裂变" / "视觉裂变"
- "fission this reference" / "generate prompt variants for this product" /
  "multiply this reference image into variants"
- 或直接给一组已反推的人物/场景 JSON（或文字描述）+ 产品文案，要求出一套裂变提示词

## 输入
最小输入（类别 A，硬性必填，两项都要）：`references[]`——**至少 2 条**同系列的人物/场景
参考材料，可以是已完成的 VTP 反推 JSON（`vtp_prompts_01/02` schema），也可以是没有真实
参考图时的文字描述降级（需在产出的 `source_material_note` 里如实标注）；`product_brief`——
产品名+品类+效果叙事文本。少于 2 条参考无法做"提取共性"（分不清哪些在变），会被拒绝，
详见 `workflow.md` Phase 1 类别 A 校验。

软性补充（类别 B，缺失走默认值，见 `workflow.md`）：`aspect_ratios_wanted`（默认
`["9:16"]`）、`variant_count`（默认 2，这是 VTP 04 步用户自由指定的参数，不是本 skill
的结构性判据）。

上游可选产出（类别 C，缺失静默跳过，不阻塞，也绝不要求用户先跑别的 skill）：
`100x-persona` 产出的 `PersonaSceneBundle`（若已存在，直接复用其身份锚点，跳过反推）。

## 输出
结构见 `schema.json`：`constants`（人物/场景/产品三锚点）+ `variables`（VTP 03 步的
共性/变量提取）+ `media_plan`（四选一媒介结构 + 帧计划）+ `prompt_sets`（VTP 04 步生成
的 N 组提示词）+ `fission_variants`（VTP 06 步机位裂变，每帧至少一条）+ `negative_prompt`
（VTP 07 步固定常量）+ `meta`。可选再渲染一张人类可读 Markdown 摘要（媒介结构 + 帧列表 +
每帧对应裂变条目）。

## 核心约束（4 条公理，详见 `axioms.md`）
1. 人物/场景/产品三锚点是定量，必须逐字出现在每一个裂变分支里（子串包含检查是大小写
   不敏感的字面匹配，不是语义等价判断——两段用词不同但描述同一个人的文字，或恰好共享
   同一句泛泛套话的两件不同产品，都可能让这条检查产生假阴性/假阳性，见 `axioms.md` 公理1）
2. **媒介裂变轴（单帧/首尾/首中尾/数日见效）叠加在 VTP 原版机位/灯光/调色三档轴之上，
   不是替换**——这是本 skill 与 VTP 原设计的核心差异点（已知局限：媒介结构判定要求
   `multi_day` 分支的理由必须引用一个数字，但机器验证不了这个数字是否忠实反映输入叙事，
   见 `axioms.md` 公理 2 TODO）
3. 每一帧计划必须真的被至少一条裂变产物渲染出来，裂变产物引用的来源必须真实存在——
   规划了却没渲染，或渲染了却指向不存在的规划，都判 FAIL
4. 每条落地提示词固定负面词常量 + 真实感兜底后缀，不得把不可视化/夸大宣称原句抄进画面
   描述（已知局限：不可视化宣称关键词表目前只在保健品类目的英语+西语真实语料上验证过，
   跨更多品类大概率需要扩表，见 `axioms.md` 公理 4 TODO）

## 三阶段流程
详见 `workflow.md`：Phase 1 接收+校验（类别 A/B/C + 不可视化宣称预检测）→ Phase 2（VTP
七步骨架：01/02 反推或降级 → 03 提取共性 → **媒介结构判定（本 skill 新增）** → 04 生成
N 组提示词 → 06 机位裂变 → 07 固定负面词 → 逐条自检）→ Phase 3 用户触发的返工（L1 单条 /
L2 单帧或结构级 / L3 全体）。

## 独立调用保证
类别 A 缺失（`references[]` 少于 2 条，或 `product_brief` 拿不到）→ 固定拒绝话术追问，
不代猜、不拿一条参考硬凑成"2 条"。类别 B 缺失走默认值 + `meta.warnings` 提示。类别 C
（`100x-persona` 产出）缺失静默跳过，**绝不要求用户先跑 `100x-persona`**。

## 禁用词
让我 / 希望 / 或许 / 大概 / 可能 / 也许 / 让我们；AI 客服味（as an AI / I'd be happy to /
feel free to）；无效美学词 attractive/beautiful/stunning/serene/pristine/elegant/
cinematic/professional/studio/flawless（VTP 反棚拍偏见的直接延伸）；不把不可视化/夸大
宣称（"clinically proven"/"cellular health"/"guarantee"等）原句抄进画面描述（公理 4）；
不编造 `references[]`/`product_brief` 里没有的事实；不发明具体品牌/客户名称；
`negative_prompt` 固定常量不可由用户或返工流程改写。

## 路由（推荐，非强依赖）
- 还没有参考图、想先找视觉参考 → 搜索关键词类 skill（`100x-search-query`，若已建）
- 还没定人物/场景、只有一段脚本文案 → 人设/场景类 skill（`100x-persona`，若已建，产出
  可直接喂给本 skill 的类别 C）
- 想把裂变结果转成正式分镜脚本/时间轴 → 分镜类 skill（若已建）
- 想回入口重新分诊 → 100x 体系总入口（若已建）

以上均为"产出后按需推荐"，不是前置依赖；对应 skill 尚未建好时不影响本 skill 独立工作。

## 出厂自检
运行 `node scripts/validate.js --selftest` 验证。公理 2/3/4 里的跨条目
聚合规则（帧数组长度、帧顺序、引用完整性、零孤儿、负面词跨分支一致、不可视化宣称扫描）
`schema.json`（vanilla JSON Schema）表达不出来，真正执行判定的是 `scripts/validate.js`：
```
npm install                                                   # 首次使用先装 ajv
node scripts/validate.js <bundle.json> [bundle2.json ...]     # 校验产出
node scripts/validate.js --selftest                           # 跑内置回归用例（16 项）
```

## 来源
本 skill 方法论骨架是 VTP（Visual Template Proliferator）七步流水线的方法论改写：
《反推方法论·四类反推与VTP七步》 + 反推 schema（人物/场景） +
提取共性/生成变体/翻译/裂变 prompt + 方法论文档里的
07 负面词常量。"媒介裂变"（单帧/首尾/首中尾/数日见效四选一媒介
结构轴，叠加在 VTP 原版机位/灯光/调色轴之上）是本 skill 的原创扩展，不是 VTP 原设计
就有的层次，具体差异点见 `axioms.md` 开篇与公理 2。逐文件改写点、原创判断披露、语料实测
记录见 `sources.md`。
