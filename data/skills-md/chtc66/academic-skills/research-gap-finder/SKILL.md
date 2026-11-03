---
name: research-gap-finder
description: analyze topic coverage, bottlenecks, controversies, and plausible research gaps when the input includes a research topic, a set of papers, or the user's early ideas and the user needs a grounded gap analysis, problem framing, small entry points, or experiment hypotheses without forced novelty claims.
---

# Research Gap Finder

用这个 skill 分析一个研究主题的已有覆盖、瓶颈、争议点和潜在 research gap。目标是帮助用户识别真正值得切入的问题，而不是硬造创新点。

## 工作流

1. 先概括主题和当前输入覆盖范围。
2. 参考 `references/problem_framing_template.md` 把问题边界说清楚。
3. 参考 `references/gap_analysis_template.md` 分析已有覆盖、瓶颈、争议点和潜在 gap。
4. 输出小问题切入建议、可验证实验思路和风险提示。

## 输入处理规则

- 接收研究主题、若干论文、用户已有想法或问题设想。
- 如果论文覆盖很少，先输出“当前只是初步 gap 讨论”，不要直接下创新结论。
- 如果用户已有想法，先判断它更像真正 gap、工程机会、评测缺口，还是阅读不足导致的表面空白。

## 输出规则

- 默认输出：
  - 主题概括
  - 已有工作覆盖面
  - 常见方法路线
  - 当前瓶颈
  - 争议点
  - research gap
  - 可切入的小问题
  - 潜在实验验证思路
  - 风险提示
- 每个 gap 都尽量说明它为什么尚未被充分覆盖。
- 明确区分“真正的 gap”和“只是文献读得还不够”。

## 证据与表述约束

- 不要为了给用户灵感而硬造创新点。
- 不要把“还没人做到”作为默认前提。
- 当输入不足时，把 gap 改写成“待进一步核实的潜在切入点”。

## 何时读引用文件

- 始终读取 `references/gap_analysis_template.md`。
- 在需要重新定义问题边界或收敛切入角度时读取 `references/problem_framing_template.md`。
