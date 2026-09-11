---
name: ask-cumcm
description: 按用户当前意图路由到本仓库某一个技能。在用户不知道用哪个 CUMCM 技能、问“下一步做什么”、或同时提出多个建模任务时使用。不拆题、不写论文、不写代码。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: user
  graph-node: R1
disable-model-invocation: true
---

# ask-cumcm

路由器。读完 [AGENTS.md](../../AGENTS.md) 技能表后输出一个推荐，然后停止。

## 何时使用

必须使用：用户说「用哪个技能」「现在该做什么」「帮我看看这套 skills」。

禁止使用：用户已经点名某个 skill；用户要直接改论文/代码——改去对应模型技能。不要为了“全面”推荐 `contest-run`。

## 循环

目标：给出恰好一个主推荐 skill，以及 0–2 个不要用的 skill。

`max_rounds`: 1（本技能不迭代）

## 步骤

1. 把用户原话映射到 AGENTS.md 表的「用户说了什么」。
2. 若赛题工作区没有 `contest-state.json` 且任务超过「问一句规则」→ 主推荐必须是 `setup-cumcm-skills`。
3. 若任务覆盖读题到提交中的 ≥3 个阶段 → `contest-run`。
4. 否则推荐覆盖该阶段的那个模型技能。
5. 输出格式固定如下，不要追加建模内容。

```
推荐: <skill-name>
原因: <一句，引用用户原话中的触发词>
不要用: <skill-name> — <原因>
状态: <若能读到 contest-state.json 则写 status，否则 uninitialized>
```

## 验收

- [ ] 恰好一个 `推荐:`
- [ ] `推荐` 是本仓库已有目录名
- [ ] 没有输出公式、代码或论文段落

## 输出

不写 `contest-state.json`。

## 下一跳

停。等用户显式调用推荐技能。
