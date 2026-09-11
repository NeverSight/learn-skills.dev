---
name: academic-voice
description: 压缩 CUMCM 论文套话、补上证据与取舍，不改变公式与数值。在初稿已成、用户说「去 AI 味」「降重」「润色」时使用。不要把检测软件百分比当作目标。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N11
---

# academic-voice

写法：[references/voice.md](references/voice.md)。

## 何时使用

必须使用：`paper_drafted`；用户要润色或觉得像模板。

禁止使用：尚未有结果；为降重改公式或换标准模型名；故意加错别字。

## 循环

目标：每个结论段能指向图/表/式/日志；删掉无信息量的对称三段论。

`max_rounds`: 3

## 步骤

1. 标空泛句（“具有重要意义”“较好的鲁棒性”“性能优越、结论可靠”“提供理论依据和决策参考”且无数字）。
2. 用 results 里的观察重写：数据在前，解释在后。
3. 补取舍：为什么不是 why_not 里的模型；参数从哪来。
4. 允许保留失败尝试与异常点。不要编造未发生的调试故事；没有就写真实取舍。
5. 句式不要连续三段同一主语开场。不要为禁词表而损害逻辑词。

## 验收

- [ ] 技术含义与数字未变（抽 5 个关键数核对）
- [ ] 无新文献（除非用户提供真实条目）
- [ ] 空泛句清单清零或标为人工待补
- [ ] 未把“AI 率 0”写入状态作为成功

## 输出

更新 `paper.path`。`status=voice_checked`。

## 下一跳

`award-review`。
