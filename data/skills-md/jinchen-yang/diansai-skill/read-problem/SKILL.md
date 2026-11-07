---
name: read-problem
description: 解析当年比赛题目（读题/审题）。当用户把官方题目 PDF/文本放进 inputs/problem/ 并要"读题""审题""解析题目""提取题目要求/限制条款"时使用。产出结构化 design/problem.yaml（限制条款、要求功能、评分、场地、计时），作为后续方案/选材的唯一需求来源。
---

# read-problem —— 读题/审题（流水线入口 ①）

**lane**: lead  ·  **needs: multimodal**（解析 PDF/图片 → **只在 lead/Claude 会话跑**；队友 lane 直接用产出的 problem.yaml）

这是整条流水线的**真正入口**。每年题目规定都不同，一切从读懂当年题目开始——**尤其先看「限制条款」**（如允不允许用摄像头，直接决定 K230 上不上）。

## 步骤

1. **定位题目**：在 `inputs/problem/` 找当年题目文件（PDF/文本/图片）。没有就提醒用户投喂，停。
2. **读全文**：用 Read 读题目（PDF 多模态直接读）。逐条抠：基础要求、发挥部分、评分、场地尺寸/标记、时间限制、器件/重量/尺寸限制。
3. **查 KB 作背景**（用 Read，不复制）：
   - `kb/01-赛事概况与赛制流程.md` —— 赛制、限制条款的常见形态、评分惯例。
   - `kb/02-历年小车与控制类赛题.md` —— 对照历年同类题型，识别"这是哪一类"（送药/追踪/循迹/双车/识别）。
4. **抽成结构**，写 `design/problem.yaml`（schema 见下）。**限制条款单列、最显眼。**
5. **标注模糊点**：题目没写清、或需要现场确认的（场地材质、起停判定、是否允许外部供电等），放进 `ambiguities`，**提请用户确认**——这是轻人工门，别替用户拍板硬约束。
6. 更新 `STATUS.md`：阶段 → ②；lead 段标"题目已解析，待 /plan-solution"。

## design/problem.yaml schema

```yaml
title:               # 题目名
year:                # 年份/届
category:            # 送药 | 追踪 | 循迹 | 双车 | 识别 | 其他（对照 KB02）
source:              # inputs/problem/<文件名>
restrictions:        # ★ 限制条款——最先看、最关键
  camera_allowed:    # true | false | unknown（决定 K230）
  power:             # 供电限制（如禁外接电源/电压上限）
  size_weight:       # 尺寸/重量限制
  parts:             # 指定/禁用器件
  other: []
required_functions:  # 要实现的功能
  - {id: F1, desc: , level: basic|advanced, points: }
scoring:             # 评分细则
  - {item: , points: }
arena: {desc: , dimensions: , track: , markings: }
timing: {run_limit: , notes: }
constraints: []      # 其他硬约束
ambiguities:         # 需人工确认（不要自己默认）
  - {q: , why: }
```

## 注意

- **不要发明题目没写的东西**；题目没明确的进 `ambiguities`，别填默认值（默认值正是赛场翻车点）。
- 限制条款里 `camera_allowed=false` 时，要在产出里**显著提示**：本届不能上 K230，方案需走纯灰度/电磁，后续 `plan-solution` 据此选。
- 产出是给 `plan-solution`/`select-parts` 用的**机器可读需求**，写清楚、可签字。
