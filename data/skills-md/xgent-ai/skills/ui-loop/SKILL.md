---
name: ui-loop
description: "用于页面设计、重设计或视觉打磨的自检迭代；不用于只读评审、仅找参考、解释提示词或后端任务。以获奖作品为基准，逐项检查并修补，直到所有维度无可见改进。"
when_to_use: "用户会说「这个页面再打磨一下」「和获奖作品比还差什么」「按视觉标准逐项过一遍」时。"
---

# UI Loop

按以下 Prompt DSL 执行：

```text
::OBJECTIVE{site_design|pri:OVERRIDE_ALL}
  target: build page to award-tier visual standard
  ACCEPT: no visible improvement remaining across all CHECK dimensions
  BENCHMARK: Awwwards | Webby Awards | FWA winning entries

::CHECK{typography|standard:award_tier}
::CHECK{whitespace|standard:award_tier}
::CHECK{visual_hierarchy|standard:award_tier}
::CHECK{color|standard:award_tier}
::CHECK{motion|standard:award_tier}
::CHECK{micro_interaction|standard:award_tier}
::CHECK{responsive|standard:award_tier}
::CHECK{originality|standard:award_tier}

::LOOP{self_review|trigger:on_completion}
  [READ] current page against CHECK list
  [COMPARE] each dimension to BENCHMARK entries
  [IF] gap found => [PATCH] then re-enter LOOP
  [IF] no gap => [Ω]
```
