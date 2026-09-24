---
name: 100x-exaggerate
description: Design exaggeration techniques and contrast pairings for a TikTok/UGC
  script draft, each anchored to a literal script quote and capped by a market/hat-level
  calibration ceiling so it doesn't tip into looking fake. Use when the user asks to
  "帮这条脚本加点夸张", "这里怎么做反差", "这段有点平，怎么更抓人", "加个前后对比",
  "make this script more dramatic", "add a before/after contrast", "how do I exaggerate
  this without it looking fake", or gives a script and wants exaggeration/contrast
  beats designed for it.
metadata:
  author: 100x
  version: "1.2.0"
---

# 100x-exaggerate

## 一句话定位
输入一段脚本/文案纯文本，输出"怎么夸张"（夸张技法+强度）+ "怎么反差"（反差类型+两端
锚点），每条都逐字回指脚本原句，强度按市场+帽度天花板校准。属于 100x 体系 L2 创意生成层，
对应"3.3 夸张/反差"这一步。

## 何时触发
用户说：
- "帮这条脚本加点夸张" / "这里怎么做反差" / "这段有点平，怎么更抓人" / "加个前后对比"
- "这条脚本的钩子不够冲击" / "怎么让这句话听起来更夸张但别太假"
- "make this script more dramatic" / "add a before/after contrast" / "how do I
  exaggerate this without it looking fake" / "what's the contrast angle here"
- 或直接给一段脚本文案，要求"设计夸张点和反差点" / "design exaggeration and contrast
  beats for this"

## 输入
最小输入（类别 A，硬性必填）：`source_script`——完整脚本/文案纯文本。本 skill **不接
视频文件**，只吃文本（与 `100x-persona` 同一约束）。

软性补充（类别 B，缺失走三级降级，见 `workflow.md` Phase 1）：`hat_level`
（`blackhat`/`grayhat`/`whitehat`）+ `market`（自由文本，如"美区"/"US"/"西语区"/
"通用"）。两者都缺失时，`hat_level` 内联推断为 `grayhat`，`market` 按保守默认处理
（`emotion_reaction_hyperbole` 技法按美区市场对待），不追问用户，`meta.warnings`
如实记录推断过程——详见 `axioms.md` 公理 3、`workflow.md` Phase 1。

上游可选产出（类别 C）：本 skill **不声明任何依赖上游 skill 产出的字段**——如果用户
已跑过 `100x-persona`/`100x-search-query` 并附带产出，可在 `rationale` 里顺带引用，
但 `schema.json` 完全不含 `persona_ref`/`scene_ref` 一类的跨 skill 引用字段，比
`100x-persona` 的可选 `segment_ref` 更彻底解耦。

## 输出
结构见 `schema.json`：`ExaggerationContrastBundle` = `source_script`（原文回显）+
`meta`（`hat_level`/`market`/校准说明/`warnings`）+ `exaggeration_beats[]`（夸张点，
每条含 `technique` 闭集枚举 + `label_cn` + `intensity` + 逐字锚点）+ `contrast_beats[]`
（反差点，每条含 `contrast_type` 闭集枚举 + `label_cn` + 两端逐字锚点）。可选再渲染
一张人类可读的 Markdown 摘要（夸张点列表 + 反差点列表）。

## 核心约束（4 条公理，详见 `axioms.md`）
1. 夸张手法（5 种）与反差类型（4 种）必须选自闭集枚举，不许自创新词——枚举本身取自
   创意桥段词典的 L1 桥段/画面类型 + 参考语料信号频次，不是拍脑袋定的
2. 每条夸张点/反差点的锚点必须是脚本原句的逐字子串，不许编造——与 `100x-persona`
   证据引文公理同一机制
3. 夸张强度受市场+帽度天花板校准，不是越夸张越好——直接吸收词典-06 自带的美区市场
   夸张强度校准提醒（具体措辞不逐字引用，见 `axioms.md` 公理 3），但**这条限制只对
   `emotion_reaction_hyperbole`（情绪反应夸张）这一个技法生效**，不笼统限制其余 4 种
   技法（已知局限：天花板表本身的三档数值化是本次原创判断，只在英西两个市场的保健品
   类目语料上验证过；`meta.market` 命中美区的判定目前是分段后做整段精确匹配，不做真正
   的中英文分词，识别不了"美国市场"这类别名嵌在更长复合词、且前后没有任何分隔符的写法
   ——v1.1 已修正一个更严重的反向问题：分段前的整串子串匹配曾对 `Russia`/`Australia`/
   `Belarus`/"南美国家"这类与美区无关的市场字符串产生假阳性；v1.2 又修正了另一个方向
   的问题：v1.1 的分段符号不含连字符`-`/`&`，导致"美区-通用"/"US & Canada"这类用连字符
   或`&`组合多个市场值的写法被漏判为不命中美区，市场天花板被静默放开，现已把`-`/`&`
   也纳入分段符号——但"完全无分隔符的复合词"这一类仍未解决，见 `axioms.md` 公理 3、
   TODO）
4. 反差两端必须有真实落差，不许同一句话充当两端——直接对应词典-06 Type D 画面对
   "两端要有可感知落差"这一核心要求的机器化（具体措辞不逐字引用，见 `axioms.md`
   公理 4）（已知局限：只能拦"字面完全相同"，拦不住"语义重复但字面不同"的更隐蔽
   退化，与 `100x-persona` 公理 3 TODO 同一类天花板，见 `axioms.md` 公理 4）

## 三阶段流程
详见 `workflow.md`：Phase 1 接收+校验（类别 A/B，`hat_level`/`market` 三级降级确定
天花板）→ Phase 2（候选句标注 → 技法/反差类型分配 → 强度定档 → 逐条自检 → 批量自检）
→ Phase 3 输出（组装 JSON，公理 1-4 全过）+ 用户触发的返工（L1 单条 / L2 校准调整，
**校准调整只能通过明确改变 `hat_level`/`market` 来放宽天花板，不能仅凭"再夸张点"
这句话就无视天花板拉高强度**）。

## 独立调用保证
类别 A（`source_script`）缺失 → 固定拒绝话术追问，不代猜、不接视频文件替代。类别 B
（`hat_level`/`market`）缺失走三级降级（两者都给→直接用；只给一个→内联推断另一个；
都缺→推断为 grayhat+保守市场默认），**不追问**，全程记录在 `meta.warnings`。类别 C
（上游 skill 产出）不存在硬依赖字段，**绝不要求用户先跑其他 skill**。

## 禁用词
让我 / 希望 / 或许 / 大概 / 可能 / 也许 / 让我们；AI 客服味（as an AI / I'd be happy to /
feel free to）；不编造脚本原文没有的效果/数字/权威背书/认证/见证；不写死任何客户品类
词典；不为了凑数量堆砌 `exaggeration_beats`/`contrast_beats`；不为了显得"更专业"给
`authority_absolutism_hyperbole` 技法编造脚本没有的机构/认证名称（本 skill 只负责
**标注**脚本里已有的宣称属于哪种技法，不负责**替脚本编造**新的宣称——合规判断同样
不是本 skill 职责，沿用词典-06 反复强调的同一边界：桥段只做客观事实描述，合规审核
留给编导发布前人工把关（具体措辞不逐字引用），见 `workflow.md` Phase 1）。

## 路由（推荐，非强依赖）
- 已有夸张/反差点，想找对应视觉参考图 → 搜索关键词类 skill（`100x-search-query`，
  若已建）
- 想把夸张/反差点转成具体人物+场景的镜头设计 → 人物场景类 skill（`100x-persona`，
  若已建）
- 想把夸张/反差点转成 AI 视频生成提示词 → 提示词组装类 skill（若已建）
- 想回入口重新分诊 → 100x 体系总入口（若已建）

以上均为"产出后按需推荐"，不是前置依赖；对应 skill 尚未建好时不影响本 skill 独立工作。

## 出厂自检
运行 `node scripts/validate.js --selftest` 验证。`schema.json` 声明的结构层
约束（`required`/`additionalProperties`/`enum`/`pattern`/`minLength`/`minItems` 等）
由 `scripts/validate.js` 内的 **ajv**（真实 JSON Schema draft-07 验证器，`package.json`
声明的 devDependency，先 `npm install` 再跑，ajv 8.x 接线抄 `100x-search-query`，
不是 `100x-persona` 早期用过的 ajv6 写法）实际执行，不是手写字段枚举。公理 2（逐字
子串锚定）、公理 3（市场帽度天花板查表）、公理 4（反差非退化）是三类跨字段/跨条目
聚合规则，vanilla JSON Schema 结构上表达不出来，由 `scripts/validate.js` 里的手写代码
补上：
```
npm install                                                   # 首次使用先装 ajv
node scripts/validate.js <bundle.json> [bundle2.json ...]   # 校验产出
node scripts/validate.js --selftest                          # 跑内置回归用例
```

## 来源
本 skill 是基于《创意画面桥段词典》（v3.3）+ 《脚本结构公式库·A-G七型与效果公式》 +
《实战案例精解·四套标杆脚本》 + 参考语料频次统计的方法论构建。三阶段流程骨架参照
标准生成与校验结构，`scripts/validate.js` 的 ajv 校验执行结构层约束。逐条判据出处、
字段设计出处、哪些是原创判断，见 `sources.md`。
