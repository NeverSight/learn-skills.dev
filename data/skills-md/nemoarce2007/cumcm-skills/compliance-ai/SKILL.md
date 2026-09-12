---
name: compliance-ai
description: 按 2026 年 CUMCM 官方规定撰写 AI 工具使用声明与「AI工具使用详情.pdf」要点，并核对匿名与支撑包清单。在终审通过前后、用户说「AI 声明」「支撑材料」「能不能交」时使用。
license: MIT
metadata:
  author: cumcm-skills
  version: "0.1.0"
  invocation: model
  graph-node: N13
---

# compliance-ai

原文要点：[references/official.md](references/official.md)。

## 何时使用

必须使用：准备提交；需要声明或详情 PDF；自查发现无声明。

禁止使用：教用户隐瞒 AI；把未核验的核心建模写成“仅润色”。

## 循环

目标：声明二选一正确；若使用过 AI，`support/AI工具使用详情.md`（导出 PDF）含官方四项。

`max_rounds`: 2

## 步骤

1. 根据真实使用填写 `ai_use.used`。用过任何大模型/代码助手都算使用。
2. 未使用：论文参考文献前写：「本参赛队在竞赛过程中未使用任何 AI 工具。」
3. 使用：写：「本参赛队在竞赛过程中使用了 AI 工具，主要用于【简要用途】，详细使用情况见支撑材料。」
4. 详情稿必须含：工具名与版本；目的和环节；提示方式与过程（可附典型交互，**不要粘贴未公开赛题全文到将公开的仓库**）；采纳、修改、核验情况（语言润色除外也要说明核验了数字）。
5. 支撑包：源程序、自查数据、大表、详情 PDF。RAR/ZIP 规划 ≤20MB。附录列出文件清单。
6. 电子论文 ≤20MB，首页摘要。

## 验收

- [ ] 声明与 `ai_use.used` 一致
- [ ] 使用了 AI 则详情四项齐全
- [ ] 未建议虚假“未使用”
- [ ] 身份信息扫描通过

## 输出

`ai_use.*`。全绿 `status=compliance_ready`，用户确认打包后可标 `shippable`。

## 下一跳

停止。交人做最后点击提交。竞赛期间不要往公开 GitHub 推送赛题。
