---
name: yao-positioning-skill
description: "Generate evidence-aware positioning reports for personal IPs, courses, products, services, brands, or companies by combining positioning theory, course-marketing analysis, user intent, competitor research, market demand, and verifiable advantages. Use when users ask for 定位、差异化分析、优势分析、心智定位、品类定位、竞品定位研究、定位报告或再定位建议. Do not use for slogan-only copywriting, generic marketing ideas, standalone market research without a positioning recommendation, or brand knowledge-base construction."
metadata:
  author: Yao Team
---

# 定位分析与报告

## Owned Job

- 为个人、课程、产品、服务或品牌生成定位报告。
- 研究五类竞争参照。
- 比较 2 至 3 套方案并推荐或降级。

## Workflow

1. 按 `references/intake-and-readiness-gate.md` 接受问答、附件或 URL，整理符合 `templates/intake-brief.schema.json` 的 `intake-brief.json`，运行 `python3 scripts/validate-intake.py intake-brief.json`。
2. 仅当校验返回 `intake_ready` 才开始检索；否则停止并使用返回的缺失项与示例，每轮追问 1 至 3 个问题。开始前回显对象、目的、范围、已收资料、自述项和待核验项。
3. 选择 `local`、`standard` 或 `deep` 研究模式。需要当前竞品、价格或市场事实时必须联网核验。
4. 读取 `references/theory-system.md`。个人 IP 或课程任务再读 `references/course-marketing-method.md`。
5. 按 `references/ai-workflow.md` 建立主张清单、竞争集合、研究计划和证据台账。
6. 按 `references/source-credibility-policy.md` 区分事实、自述、推断、假设和建议；来源必须通过权威性、主张适配、直接性、时效性、独立性和市场适配检查。
7. 按 `references/competitor-research-method.md` 研究竞争与心智位置。禁止把“未发现公开证据”写成“不存在”。
8. 按 `references/demand-and-differentiation-method.md` 分析需求、市场空位和 D6 优势，执行否决规则。
9. 通过诊断与推荐门槛后生成 2 至 3 套定位方案并压力测试，只推荐一套；不通过时只输出初步观察和补证计划。
10. 按 `references/plain-language-positioning-method.md` 生成通俗的心智快照，再进入可视化报告。
11. 先生成符合 `templates/report-data.schema.json` 的 JSON，再运行 `python3 scripts/validate-report-data.py positioning-report-data.json`。
12. 校验通过后运行 `python3 scripts/render-report.py positioning-report-data.json --out positioning-report`。
13. 运行 `python3 scripts/review-report.py positioning-report`，修复语义、图表、移动端、打印和跨格式回归；不得通过删证据或升级置信度消除警告。
14. 按 `references/report-contract.md` 核对 HTML、JSON、Markdown 的结论、指标和引用一致性。模板或图表变更再按 `references/report-review-method.md` 执行三视口与 A4 PDF 栅格化审校。

## Downgrade Rules

- 研究就绪门槛未通过：只补信息，不检索竞品、不生成方案。
- 诊断门槛未通过：只输出初步观察和补证计划。
- 无法访问外部资料且用户未提供竞品：进入本地证据模式，输出补证清单。
- 没有用户需求证据：不得宣称市场空位。
- 没有可证明优势：输出能力建设建议，不制造差异化标签。
- 涉及第一、唯一、领先或效果承诺：要求独立证据和合规审查。

## Output Contract

默认交付：

- `positioning-report.html`：离线可视化决策报告。
- `positioning-report-data.json`：唯一结构化事实源。
- `positioning-report.md`：无脚本降级版与审计记录。

先用一页心智快照说清结论，再提供需求、竞争、优势、方案、行动、风险、证据和验证计划。个人 IP 或课程增加四层一致性，课程再增加行动路径、4P 与课程机制。缺失数据展示“证据不足”，不得伪造图表或总分。

交付前 `review-report.py` 必须通过。来源时效和证据警告可保留，但必须在报告和审校结果中可见；零警告交付使用 `--strict`。

## Reference Map

- 理论：`references/theory-system.md`、`references/plain-language-positioning-method.md`、`references/course-marketing-method.md`
- 执行：`references/intake-and-readiness-gate.md`、`references/ai-workflow.md`
- 研究：`references/source-credibility-policy.md`、`references/competitor-research-method.md`
- 分析：`references/demand-and-differentiation-method.md`
- 交付：`references/report-contract.md`、`references/report-review-method.md`、`references/html-report-spec.md`、`references/metric-dictionary.md`
- 渲染资产：`assets/report-template.html`、`assets/echarts.min.js`
- 系统说明：`reports/positioning-skill-system-overview-2026-07-16/index.html`
- 分发净化：`scripts/sanitize-package.py`（仅在重建 ZIP 后执行）
