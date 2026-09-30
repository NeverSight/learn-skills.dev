---
name: prd-review
description: >
  PRD 评审 / 需求评审：当用户已有 PRD 初稿、handoff、需求文档或产品方案，需要从 PM、研发、测试视角找缺口、
  冲突、不可实现点和不可测试点时使用。可用中文唤起：“帮我审 PRD”“从研发和测试视角挑问题”
  “这个需求文档能不能交付开发”“帮我给 PRD 出修改草案”“检查 PRD 图示是否缺失或不可编辑”。
  不用于凭空生成 PRD 初稿、直接写代码，或对 PRD 背后的成熟方案做一问一答压力测试；方案压测用 grill-me。
---

# PRD 评审（prd-review）

## 中文速查

- 中文名：PRD 评审 / 需求评审
- 英文稳定名：`prd-review`
- 你可以这样叫我：`帮我审 PRD`、`从研发测试视角挑问题`、`这个需求文档能不能交付开发`、`帮我补一版修订草案`、`检查 PRD 图示是否可编辑`
- 适合：已经有 PRD/handoff，需要发现阻断项、重要缺口、用户结果不可验证、工程无法落地的地方
- 不适合：从零写 PRD，改用 `prd-architect`；PRD 背后的方案可行性压测改用 `grill-me`；只做语言润色时不需要触发

## Overview

这个 Skill 评审的是 PRD / handoff artifact 是否能支撑交付。默认输出结构化 review report、按严重程度排序的 findings、可回填的 revision draft，以及 `Implementation-Plan Readiness` verdict。

它不是 PRD 生成器，也不是一问一答方案压力测试器：

- 没有 PRD 或只有模糊想法：转 `prd-architect` 或 `ai-collaboration-calibration`。
- 关心“这个方案本身会不会失败”：转 `grill-me`。
- 要把 ready PRD 拆 GitHub issues：转 `prd-to-issues`。
- 要文件级开发计划：转 Superpowers `writing-plans`。

## Loop Extension

当用户明确需要“多轮评审”“关闭阻断项”“继续上一轮 review”“判断是否能进 writing-plans”“跟踪修订状态”或“把 PRD 收敛到可交付开发计划”时，读取 `references/prd-readiness-loop-contract.md`。

不要因为用户只是要求一次普通 PRD review 就创建状态文件；只有需要多轮收敛、可恢复状态或 readiness tracking 时才启用 Loop contract。

## Inputs

优先读取：

- `handoff` 文档：功能背景、目标用户、范围、风险与已确认事实。
- `PRD` 初稿：当前结构、已写事实、隐含假设、缺口和冲突。

可选补充：

- 本轮关注视角或维度。
- 用户明确担心的问题。
- 相关 UI、架构图、历史评审意见。
- `docs/templates-local/` override；如存在，应按 local override 理解正文结构。

如果输入不完整：

1. 明确哪些结论来自 handoff，哪些来自 PRD 当前写法，哪些是 review 推断。
2. 无法下结论的地方输出待确认问题，不强行补脑。
3. 输入还不足以 review 时，建议先回到 `prd-architect`。

## Workflow

1. **Establish scope**
   - 记录 PRD / handoff 来源、本轮 review 目标、事实与假设边界。
   - 判断是否应转 `prd-architect`、`grill-me`、`prd-to-issues` 或 `writing-plans`。

2. **Load review assets**
   - 默认读取 `references/review-lenses.md` 和 `references/severity-rules.md`。
   - 当需要输出完整 report 或 revision draft 时读取 `references/output-contract.md`。
   - 当用户问“能不能交付开发 / 能不能进 writing-plans”时读取 `references/implementation-plan-readiness.md`。
   - 当 PRD 包含或应包含流程图、架构图、系统关系图、AI 协作链路图时读取 `references/diagram-review.md`。
   - 当 PRD 看起来过重、过技术化或模板章节误激活时读取 `references/prd-shape-gates.md`。

3. **Review the PRD**
   - 至少从 PM、研发、测试三个视角 review。
   - 合并重复问题，不要按角色输出三份重复报告。
   - findings 必须包含：严重程度、视角、位置、问题、影响、建议改法。
   - 图示相关结论必须区分：文本要求缺失、文件实际校验失败、未能验证。

4. **Run deterministic checks when possible**
   - 有本地 PRD 文件且疑似过技术化时运行：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native>
```

   - PRD 明确是开发 handoff 时加 `--allow-handoff`。
   - 评审发布版时加 `--publish-ready`；该模式会同时要求有效的顶部版本记录。只评审版本历史时可加 `--require-version-history`。
   - 有 `.drawio` 源文件时运行：

```bash
python3 scripts/validate_drawio.py <path>
```

   - 脚本 warning 是 review 证据，不自动等同于阻断；结合 PRD 阶段和用户目标判断。

   - 输入包含 `product-delivery-manifest.yaml` 时，先运行 canonical Manifest validator，再评审整个 Package；validator 只证明确定性结构，不替代 Reviewer 判断。

5. **Produce repair-ready output**
   - Findings 按严重程度排序。
   - 必须给 revision draft：最小可替换章节、段落、可验证结果/边界/异常清单三者至少一种。
   - 必须列 open questions。
   - 必须给 `Implementation-Plan Readiness` verdict：`Ready for writing-plans`、`Ready with assumptions` 或 `Not ready`。

### Product Delivery Package Verdict

Package Review 与普通 PRD readiness 并存但不可混用。输入包含 Product Delivery Manifest 时，先确认本轮是拆分前 Review 还是完整 Package 最终 Review：

1. 拆分前 Review 读取 PRD、适用 UI artifact、Action Contract、截图、anchor 和 baseline；最终 Review 还必须读取版本计划、issue drafts 和 coverage matrix。不要对未读取的 revision 给 verdict。
2. 验证 `reviewer_identity` 与当前 Review 覆盖的全部 artifact `producer_identity` 不同，且 `maker_identities` 没有遗漏生产者；Reviewer 不修改被评审 artifact。
3. 只输出一条适用阶段的 verdict：`ready` 或 `changes_requested`，并包含且只包含 `content`、`artifacts`、`publish` 三项 `passed/failed` 检查。
4. 拆分前 `ready` 必须绑定 validator 返回的当前 `pre_split_input_fingerprint` 并写入 `pre_split_review`；最终 `ready` 必须绑定当前 `package_input_fingerprint` 并写入 `review`。两者都要求三项检查全部通过，`Ready with assumptions` 不能产生 Package readiness 或发布授权。
5. findings 记录 severity、证据来源、责任节点、受影响对象和最小重跑 scope；输入变化后旧 verdict 立即 stale。
6. Reviewer 只写本阶段对应的 `pre_split_review` 或 `review` 分区。Human approval 与 DingTalk release 仍由各自角色负责。

## Writing Rules

- Findings 先于 summary。
- 同一个问题合并成一条，再标注受影响视角。
- 修订草案优先最小可替换块，不默认重写整篇。
- 不把缺失业务判断伪装成已确认需求。
- 不为了显得完整而强行添加与当前阶段无关的大段章节。
- 不声称图文件合格，除非已经运行相应验证或明确说明验证限制。

## Resource Guide

- `references/review-lenses.md`：PM / 研发 / 测试 / 可选角色视角。
- `references/severity-rules.md`：阻断、重要、优化的判定规则。
- `references/output-contract.md`：默认 review report 结构、revision draft 和 writing rules。
- `references/implementation-plan-readiness.md`：进入 `writing-plans` 前的 readiness verdict。
- `references/diagram-review.md`：Draw.io / SVG / PNG / Mermaid 图示评审。
- `references/drawio-templates.md`：需要判断图示布局、节点数、颜色或 XML 模板时读取。
- `references/prd-shape-gates.md`：阶段混淆、过早技术化、模板章节误激活。
- `references/prd-readiness-loop-contract.md`：多轮 review / revision / re-review 状态化合约。
- `scripts/check_prd_shape.py`：PRD 形状和过技术化 warning。
- `scripts/check_prd_version_history.py`：与 `prd-architect` 保持一致的版本历史校验器。
- `scripts/validate_drawio.py`：Draw.io XML 基础结构验证。

## Definition of Done

- handoff 和 PRD 的边界已经分开。
- findings 有严重程度排序，且证据来源清楚。
- 修订草案可直接回填。
- 推断和事实没有混写。
- 图示和 PRD shape 的验证状态已说明。
- 已明确 `Implementation-Plan Readiness`。

## Evaluation

Smoke prompts:

- `帮我审这份 PRD，从 PM、研发、测试视角找阻断项。`
- `这个需求文档能不能交付开发？给我 readiness verdict。`
- `帮我 review 这份 AI-native PRD，重点看人工确认和失败回退。`
- `检查这份 PRD 图示是否缺失或不可编辑。`

Non-trigger prompts:

- `帮我写一个 PRD。`
- `拷问这个方案会不会失败。`
- `把这个 ready PRD 拆成 GitHub issues。`
- `只润色这段 PRD 文案。`

Capability checks:

- 输出 findings、revision draft、open questions 和 readiness verdict。
- 结论区分 handoff facts、PRD text 和 reviewer inference。
- 图示检查区分正式 `*.drawio.svg`、`src/*.drawio`、普通 `.svg`、PNG 和 Mermaid。
- 过技术化产品稿会建议把 schema / metadata / adapter 移到开发 handoff 附录。
