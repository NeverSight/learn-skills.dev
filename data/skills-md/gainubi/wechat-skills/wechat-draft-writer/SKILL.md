---
name: wechat-draft-writer
description: 公众号初稿写作技能。用于在选题和大纲已确认后，基于参考资料、语音底稿和文风 DNA 生成一版高保真初稿。适用于正文写作阶段，不负责选题、大纲和标题决策。
---

# Wechat Draft Writer

## Overview
在结构已确认的前提下，把参考资料和语音底稿转成符合作者文风的公众号初稿。

## Workflow
1. Require confirmed outline, reference materials, voice transcript draft, Style DNA card, and article goal.
2. 如果用户还没有个人 Style DNA，先调用 `wechat-style-profiler` 生成。
3. 将个人 Style DNA 复制到 `wechat-draft-writer/references/author-style-dna.md`。
4. 在开写前明确声明当前使用的 Style DNA 文件或作者画像名称。
5. Digest source material, separating hard facts from personal观点、原话和待验证信息。
6. 为每个 section 生成内部写作 brief，不对外输出新的大纲版本。
7. 按 section 写出 `Draft v1`，执行 `references/draft-dna-enforcement.md` 的硬约束。
8. 跑 `references/draft-quality-checklist.md` 自检。
9. 返回初稿、文风贴合说明、风险点和可修正建议。

## Output Contract
1. `Style DNA In Use`
2. `Draft v1`
3. `Style Adherence Notes`
4. `DNA Compliance Report`
5. `Weak Sections And Fix Suggestions`
6. `Optional Alternative Lead`

## Guardrails
- Avoid inventing facts; mark any uncertain claim with `[待补充证据]`.
- Distinguish source types explicitly: `参考资料` facts vs `语音底稿` personal expression.
- Keep paragraph granularity suitable for WeChat mobile reading.
- Preserve the user's habitual rhetorical devices from the Style DNA card.
- If no personal Style DNA is provided, hand off to `wechat-style-profiler` first.
- Prefer loading DNA from `wechat-draft-writer/references/author-style-dna.md`.
- The default DNA template is only a temporary fallback for demo/testing, not for final publish drafts.
- Must explicitly tell the user which DNA file or author profile is being used before presenting the draft.
- Keep paragraph length within 1-3 sentences unless explicitly requested.
- Do not use em dashes.
- If hard-fail pattern is detected, rewrite before returning output.
- If outline is not confirmed, hand off to `wechat-topic-outline-planner` instead of drafting.
