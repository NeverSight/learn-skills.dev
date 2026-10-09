---
name: wedding-flow-poster-lite
description: Use when a user provides messy wedding workflow notes, voice-transcribed ceremony text, or an execution rundown and wants a clean wedding flow poster.
---

# Wedding Flow Poster Lite

## Overview
Turn messy wedding notes into a **poster-ready flow**, ask the user to confirm it, then render the confirmed content through the bundled deterministic renderer.

Core contract:

**clean to poster content → confirm → serialize confirmed data → run bundled renderer → return PNG**

This Skill is not a wedding brief, execution sheet, meeting summary, or planning document.

## Stage 1 — Produce a poster-ready clean draft
Read only the user-provided text/files. Extract only information that can appear on the Lite poster:

- couple names;
- wedding date;
- optional event label only when explicitly supplied;
- start time;
- venue;
- ordered wedding flow item names;
- optional After Party items only when explicitly supplied.

Clean fillers, duplicate wording, obvious speech-to-text noise, punctuation, and overly long phrases. Preserve facts and order. Do not invent missing steps or times.

### Content clarity
The first response must be **short, visual, and poster-oriented**, not exhaustive.

For flow items:
- one visible event per line;
- target 2–10 Chinese characters; maximum 16;
- use concise labels such as `新郎入场`, `新人告白`, `交换戒指`, `父母登场`;
- silently remove backstage details: microphone handoffs, door opening, reminders, prop retrieval, stage positions, clothing, music, guest counts, mood notes, preparation lists, staffing, and similar execution notes;
- never use semicolon-heavy multi-action lines or long parentheses;
- if a detail does not change the visible event name, omit it;
- if ambiguity changes the actual visible event, use the safest generic label or mark only that event for confirmation.

Do **not** create extra sections such as `来宾信息`, `婚礼想法`, `音乐`, `开场白方向`, `婚礼需要准备`, `伴郎伴娘分工`, or `执行备注`.

### Required Stage-1 response shape

```text
新人：测试新郎 & 测试新娘
日期：2026.10.18
时间：11:08
地点：示例酒店

婚礼流程
1. 主持人开场
2. 新郎入场
3. 新娘入场
4. 新人告白
5. 交换戒指
6. 父母登场
7. 父亲致辞
8. 合影

请确认以上文字、信息和顺序是否正确。需要修改直接告诉我；确认无误后告诉我“生成海报”。
```

Omit unknown optional metadata instead of inventing it.

Show the **complete cleaned poster draft** and wait. Do not render before explicit confirmation, even if the first message says “直接生成”. If the user changes anything, show the complete updated poster draft and wait for confirmation again.

## Stage 2 — Use only the bundled renderer
After the user confirms the latest cleaned draft, serialize the confirmed content to JSON. Example:

```json
{
  "coupleNames": "测试新郎 & 测试新娘",
  "date": "2026.10.18",
  "eventLabel": "婚礼晚宴",
  "venue": "示例酒店",
  "startTime": "11:08",
  "title": "婚礼流程",
  "items": ["主持人开场", "新郎入场", "新娘入场"],
  "afterPartyTitle": "AFTER PARTY",
  "afterPartyItems": ["新人合唱", "默契挑战"]
}
```

Optional fields (`eventLabel`, `afterPartyItems`) must be omitted when the user did not provide them. Never invent them.

### Renderer ownership — hard rule
Do **not** hand-write a new poster HTML/CSS file in Chat, Work, or another agent environment. Do **not** improvise layout order.

Always invoke the bundled renderer:

```bash
python scripts/render_poster.py confirmed.json output.png
```

The bundled renderer is the single source of truth for:
- vertical order;
- typography hierarchy;
- spacing;
- background/text layer separation;
- overflow fitting;
- final composition.

This rule exists to prevent environments from reversing the design, placing `婚礼流程` at the bottom, or inventing a different layout.

### Hard visual order
When fields exist, visual order must remain **top → bottom**:

```text
新人姓名
日期
可选婚礼类型
地点
短分隔线
开始时间
婚礼流程
短分隔线
流程正文（严格按确认顺序）
可选 AFTER PARTY
短分隔线
After Party 正文（严格按确认顺序）
```

Never reverse it. Never use `column-reverse`, CSS `order`, bottom anchoring, or any equivalent mechanism.

## Layout spec v1.1
The detailed executable reference is `references/layout-spec.md`. Core rules:

- 1080×1920, 9:16;
- X=540 px center axis;
- typography visible region targets about Y=252→1687 (≈74.7% height);
- top whitespace ≈12%–14%; bottom ≈11%–13%;
- logical safe width ≈57%; typical actual longest line ≈36%–40%;
- body reference 28 px;
- couple names 53 px ≈ body×1.9;
- main title 33 px ≈ body×1.18;
- AFTER PARTY 31 px ≈ body×1.11;
- Chinese body step ≈50 px / line-height rhythm ≈1.75–1.8;
- After Party step ≈52 px / rhythm ≈1.8–1.9;
- font size and spacing must change together;
- 50×2 px short dividers;
- primary `#3B3029`, accent `#9B4C2E`;
- accent only for `&`, section titles, and short dividers;
- preferred serif stack: Noto Serif CJK SC / Source Han Serif SC / Songti SC / STSong.

If the content is too tall, proportionally scale the **whole typography system** while preserving hierarchy and order. Never solve overflow by reversing, bottom-anchoring, or shrinking only body text.

## Layer pipeline
The renderer must keep layers separate:

1. confirmed structured content;
2. HTML/CSS real-text rendering;
3. transparent PNG typography layer;
4. bundled warm-white paper background layer;
5. pixel-level alpha composite;
6. final 1080×1920 PNG;
7. check order and bounds before returning.

Never send background + text back through an image-generation model.

## Output
Return the final PNG as an accessible attachment/link. Do not expose a temporary path as the only delivery method.

## Never do
- Never turn the source into a comprehensive wedding brief.
- Never render execution instructions inside flow items.
- Never invent missing facts, event labels, After Party items, steps, or times.
- Never skip the confirmation gate.
- Never hand-author a replacement poster layout instead of using the renderer.
- Never reverse the top-to-bottom order.
- Never offer background/font/theme choices in Lite.
- Never use production Poster Workspace services, secrets, or customer data.
