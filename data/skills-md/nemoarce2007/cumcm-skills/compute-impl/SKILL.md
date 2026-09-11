---
name: compute-impl
description: 把已建立的 CUMCM 模型写成可运行、可复现代码并导出论文要用的数表。在模型已推导、用户说「写代码」「求解」「跑一下」时使用。不要在模型未定义时让模型自己编题。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N7
---

# compute-impl

推荐目录见 CONTEXT.md。原则：先有模型，再写代码。

## 何时使用

必须使用：`model_built`；要数值结果。

禁止使用：用 AI 直接“给一个合理最优值”；修改 raw；把不可复现的笔记本截图当唯一证据。

## 循环

目标：入口脚本退出码 0；`results/` 中数字与将写入论文的数字一致。

`max_rounds`: 6

## 步骤

1. 参数进 `configs/config.yaml`（或 `.m` 常量区）。`np.random.seed` 或 `rng` 固定，写入 `code.seed`。
2. 每问一个 `scripts/run_problemN.py`，复用 `src/`。
3. 必须：中文注释写「为什么」；至少在陷阱处写踩坑注释；异常要抛到日志，不要静默吃掉。
4. 图先出正确数据，美化交给 `chart-style`。
5. 写 `results/logs/run.md`：环境、耗时、收敛信息。
6. 更新 `README` 式 `scripts/README.md`：如何一键跑。

## 验收

- [ ] 相对路径，无用户主目录绝对路径
- [ ] 固定种子
- [ ] 论文将引用的每个关键数字能在 `results/tables/` 找到
- [ ] 优化问题约束在代码里有对应（不得漏约束）
- [ ] 预测问题不得用未来信息训练（无泄漏）

## 输出

`problems[].results`、`code.*`。`status=solved`。

## 下一跳

`model-validate`。
