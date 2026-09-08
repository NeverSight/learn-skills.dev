---
name: tk-eli5
description: "[user/auto] 초보자가 이해할 수 있는 그림 중심의 self-contained HTML 설명 자료를 만듭니다. 텍스트 재설명, 비교 prototype, 기존 페이지 편집에는 사용하지 않습니다."
disable-model-invocation: false
argument-hint: "<topic and optional output path>"
metadata:
  tigerkit:
    kind: hybrid
    origin: anthropics/claude-plugins-community
    relationship: adapted
    upstream-skill: eli5
---

# Visual ELI5 Explainer

Create one picture-first HTML artifact that lets a newcomer grasp the topic's core flow at a glance.
Use it for an explicit `$tk-eli5` invocation or a request for an HTML explanation with a big picture and little text.

## Boundaries

- A text-only simplification of the immediately preceding explanation is ordinary host/model capability; stop with `NotApplicable`.
- An executable comparison of two or more UI/logic alternatives belongs to `tk-prototype`; stop with `NotApplicable`.
- Do not apply this skill to a general prose explanation, code walkthrough, or edit of an existing HTML/page; stop with `NotApplicable`.
- If the topic is missing or ambiguous, output exactly `Unverifiable` and create no file.

## Workflow

1. Confirm one clear topic and any user-specified output path. Without a path, use
   `eli5-<topic-slug>.html` in the current working directory; if it exists, choose a new path
   with a numeric suffix. Never overwrite an existing file without explicit approval.
2. Normally divide a simple core mental model into about `3–5` scenes and one consistent analogy. Use fewer or more
   scenes when that materially improves comprehension or preserves a required caveat; scene count is a design signal,
   not a correctness gate. For topics where
   freshness or expert facts matter, verify available evidence first; simplification must not
   discard accuracy or required warnings.
3. Create one self-contained HTML file. Inline CSS and SVG/CSS visuals; add no external asset,
   font, framework, dependency, build step, or network request.
4. Use large visuals, short headings, and aim for at most about `35` words of explanation per scene. Exceed that target
   only when splitting or deleting text would make the explanation inaccurate or less understandable. Preserve
   semantic HTML, sufficient contrast, accessible SVG titles, non-color-only distinctions, and
   `prefers-reduced-motion` by default.
5. Verify that the HTML opens directly offline and contains a coherent scene sequence, inline visuals, and the
   AI-authorship footer. Do not start a server or automatically open a browser.

End the HTML with this exact sentence:

```text
🤖 본 설명 자료는 AI가 작성했습니다.
```

## Completion and Output

Return `Pass` only when the designated HTML exists, opens without installation or network access,
and explains the topic's core flow through a big picture and little text. Never report a generation failure as success.

Return only this one line to the user:

```text
<path> — 초보자용 그림 중심 HTML 설명 자료.
```

## Source

Adapted the big-picture, low-text HTML artifact and `/eli5 <topic>` behavior from
`anthropics/claude-plugins-community` `eli5` v1.0.0, commit
`863e70dc7cff21a2facc749e40a7ecd1a5d19833`. TigerKit adds offline self-contained output,
skill boundaries, verification, collision-free paths, accessibility, and authorship disclosure.
The original copyright and MIT notice are in repository `NOTICE.md`.
