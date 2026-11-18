---
name: ay-write
description: Write or revise Chinese and English prose. Use when authoring articles, Q&A, guides, stories, speeches, social content, or consumer handoffs for approved/implemented APIs and messages; 中文写作、面试题库、公众号、小红书、视频文案、口播、改稿、去 AI 味、联调文档、客户端升级说明. Exclude contract design, conversations, mock interviews, interview sourcing, UI copy, layout-only work, and assistant-reply shortening.
---

# AY Write

## Approval contract

<!-- ay-contract:start -->
- Read the full request and investigate discoverable facts before asking the user.
- Treat review, diagnosis, explanation, and planning as read-only unless the user also requests change.
- Treat a precise instruction as approval when target, observable result, and acceptance boundary are clear.
- A broad outcome authorizes investigation, not file or artifact changes based on choices the agent must invent.
- For a materially underspecified change, present one recommended proposal and wait for approval.
- After approval, execute autonomously inside the approved boundary; do not ask about ordinary implementation details.
- Reopen approval only when new evidence changes behavior, architecture, data contracts, dependencies, scope, risk, cost, rollback, or external actions.
- Perform external actions only when the request or approved proposal includes them. Confirm the exact target before an irreversible action.
- Preserve unrelated and user-authored work. Verify the real requested outcome before claiming completion.
<!-- ay-contract:end -->

## Writing

Deliver the requested text directly. Include drafting notes, alternatives, or editing rationale only on request. Respect the reader, voice, form, and length.

Cut throat-clearing, previews of the next sentence, and summaries that repeat the answer. Add background or examples to resolve a specific gap. Stop once the reader can understand or act.

Read the shortened passage in order. Restore any missing reason, unclear subject, or condition detached from its action. Keep connected thoughts in flowing prose. Preserve facts, uncertainty, literals, and source boundaries. Verify factual claims against primary sources. Label hypothetical examples. Only requested fiction may invent events.

## By task

- Q&A and FAQ: answer each question directly. Preserve follow-ups and version conditions. Make entries independently readable.
- Explanations and selection articles: lead with the answer and decisive conditions. Explain mechanisms in understanding order. Include tradeoffs that affect the choice.
- Technical deep dives: use [deep-dive-articles.md](references/deep-dive-articles.md) for question-driven sections, running examples, pinned sources, worked numbers, and hand-written SVG diagrams.
- Tutorials: give prerequisites, actions, observable checks, and relevant failure conditions. Writing instructions does not authorize execution.
- Reference: organize for lookup with stable terms.
- Integration handoffs: document established contracts using [integration-docs.md](references/integration-docs.md).
- Stories and speeches: preserve viewpoint, pacing, and voice.
- Social and video: use [social-writing.md](references/social-writing.md) for platform and timing.

For rewrites and factual explanations, read [clear-prose.md](references/clear-prose.md). For other technical writing, read [technical-articles.md](references/technical-articles.md).

## Delivery

Full explanatory articles include opening and module images. Use [visuals.md](references/visuals.md) for cinematic realism and the bundled cast. Deep dives use the SVG style above. Honor requested styles and text-only scope.

Verify coverage, facts, links, assets, and layout. Report unavailable images. AI review cannot prove reader comprehension or recall. Publishing, paid tools, dependencies, and skill edits require separate authorization.
