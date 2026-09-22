---
name: eli
description: "Explain a topic at a chosen reader level: 5살 / 입문 / 실무 (eli 5 / 20 / 30). Use when the user types /eli <age> <topic>, or asks to explain something \"like I'm N\", \"N살한테 설명하듯\", or wants a picture explainer with adjustable depth."
argument-hint: "[5|입문|실무] <주제>"
---

# eli

Explain `$ARGUMENTS` as an HTML artifact. The first token is the level; the rest is the topic.
Levels are named by reader, not age. Numbers are shortcuts for typing:

| token | tab label | reader |
|---|---|---|
| `5`, `5살` | 5살 | someone hearing the topic for the first time |
| `20`, `입문` | 입문 | someone who started learning it |
| `30`, `실무` | 실무 | someone who uses it at work |

If no level is given, build **all three as tabs** on one page, 5살 selected by default. Several tokens (`5 20 30`) also means tabs. A single token means one panel (the template hides the tab bar).
Never show "20살", "30살", or "(실무)" in the page. Tab labels are exactly `5살`, `입문`, `실무`.

The one-line lead under each tab is a summary of the topic at that level (e.g. 5살: "책을 많이 읽고 다음 말을 맞히는 친구"), never a description of the format or of these rules.

Always: big pictures (inline SVG or CSS shapes), one idea per card, Korean by default, headings as noun phrases, body lines ending in `~함 / ~됨 / ~임`.

## Workflow (4 tool calls, no browser MCP)

The design system (palette, type, tabs, cards, tiles, bars, stepper, simulator, glossary, code) already lives in `templates/template.html` inside this skill's directory. Do not write CSS or tab/stepper JS. Loading `artifact-design` is not needed: the template is the design pass.

1. Write **only the content** to `<scratchpad>/eli-<topic>-sections.html`: one `<section data-tab="입문">` per level (add `data-default` to the tab that opens first). Inside: `<p class="lead">`, optional `<p class="note">`, then `<div class="cards">` of `<article class="card">`. Topic-specific `<script>` blocks (simulators) go at the end of the same file; the builder moves them after the shared script, where `window.eli` is available.
2. Run `python3 ${CLAUDE_SKILL_DIR}/scripts/eli_build.py <sections> --title "<주제 명사구>" --out <scratchpad>/eli-<topic>.html` (`${CLAUDE_SKILL_DIR}` is the directory containing this SKILL.md). Needs `playwright` and `pillow` with Chromium installed; without them, pass `--no-verify` and skip to step 4 after reading the built page yourself. It assembles the page, opens it in headless Chromium (about 6 seconds), screenshots every tab (with every step of every stepper appended below) plus a dark-theme sheet, and prints DOM warnings: SVG text over 12 chars, `text-anchor` not middle, text within 20 viewBox units of an edge, content overflowing a card, forbidden strings, console errors.
3. Read the printed `shots/tab-*.png` once each (tall pages are cut into side-by-side columns) and `dark.png` once. Fix every warning and anything clipped, overlapped, or wrapped mid-word in the sections file. Then rebuild with `--tabs <탭,탭>` naming only the tabs you edited: the DOM check still covers every tab, but only those screenshots are written and the dark sheet is skipped. Read only those shots. Do not publish with warnings.
4. Publish `eli-<topic>.html` with the Artifact tool. Favicon: 🖍️ for 5살, 📘 for 입문, 🧭 for 실무, 🎚️ for a tabbed page. If there is no Artifact tool (e.g. Codex), stop here and give the user the path of the built HTML file to open in a browser.

### Markup the template understands

| piece | markup |
|---|---|
| card | `<article class="card"><div class="fig">picture + <p>caption</p></div><div class="body"><h3>제목</h3>…<ul><li>…함</li></ul></div></article>` |
| term (입문/실무) | `<div class="term"><b>한글</b><i>English</i><span>뜻</span></div>` right under `<h3>` |
| token tiles | `<div class="tiles"><span class="tile">조각</span><span class="tile hi">방금 고른 것</span><span class="tile q">?</span><span class="tile ghost">흐림</span></div>`; several rows: wrap in `<div class="rows">` |
| bars | `<div class="bars"><span class="lbl">이름</span><div class="bar pick"><i style="width:41%"></i></div><span class="val">0.41</span>…</div>` (`pick` yellow, `cut` grey, `mono` neutral) |
| flow | `<div class="flow"><div class="box">입력<small>설명</small></div><span class="arrow">→</span><div class="box acc">핵심</div><div class="box bad">틀린 것</div></div>` |
| step widget | `<div class="stepper"><div class="step"><div class="stage">그림</div><p class="cap"><b>1 이름</b> : 한 줄</p></div>…</div>` — buttons and dots are added by the template |
| step widget over a box row (preferred) | `<div class="stepper" data-pipe="분해,맥락,생성,검증,기록" data-back="4>3"><div class="step"><p class="cap"><b>1 분해</b> : 한 줄</p></div>…</div>` — no `.stage` needed; step i gets the box row with box i highlighted, `data-back="4>3"` draws a dashed return arrow on step 4 |
| box row | `<div class="pipe" data-boxes="입력,처리,출력" data-hi="2" data-back="3>2"></div>` — SVG drawn by the template, `data-hi` is 1-based, `data-back` optional |
| grid of cells | `<div class="grid" data-cells="이해\|어떻게 답을 만드나,활용\|어떻게 시키나,평가\|맞는지 보나,책임\|누가 책임지나" data-cols="2" data-hi="3"></div>` — `제목\|부제` per cell, `data-hi` optional |
| simulator | `<div class="sim"><div class="knobs"><label>온도 <output id="tOut">0.8</output><input type="range" id="temp" …></label><div class="stat" id="stat"></div></div><div class="bars" id="simBars"></div></div>` + your `<script>` using `eli.softmax(logits, T)` and `eli.bars([{label, pct, val, cls}])` |
| glossary | `<div class="tablewrap"><table><thead><tr><th>뜻</th><th>입문 탭 비유</th><th>영어</th></tr></thead><tbody><tr><td>…</td><td class="an">…</td><td class="en">…</td></tr></tbody></table></div>` |
| code / terminal replay | `<div class="pre-wrap"><pre><code>…</code></pre></div>`; inside `<pre>`: `<span class="you">` what you type, `<span class="edit">` the part you edit, `<span class="dim">`, `<span class="err">` |
| two columns | `<div class="two"><div><h4 class="ok">쓰기 좋음</h4><ul>…</ul></div><div><h4 class="no">피해야 함</h4><ul>…</ul></div></div>` |
| before / after | `<div class="ba"><div><h4>전</h4>…</div><div><h4>후</h4>…</div></div>` |
| context bar | `<div class="ctx"><span style="flex:2;background:var(--accent)">이름</span>…</div><div class="ctx-legend"><span>…</span></div>` |

Use `pipe`, `grid`, and `data-pipe` steppers for every picture that is boxes with labels; write inline SVG only for pictures those cannot draw (a parrot, a scale, a timeline). Never repeat the same SVG with one box recolored: that is a `data-pipe` stepper.

Colors inside SVG: use `var(--accent)`, `var(--hi)`, `var(--hi-ink)`, `var(--surface)`, `var(--line)`, `var(--ink)`, `var(--muted)`, `var(--bad)` so dark theme works. SVG text: `text-anchor="middle"`, `font-family="IBM Plex Sans KR, sans-serif"`, at most 12 Korean characters, 20+ viewBox units from every edge. Commands, code, and paths never go in SVG text; put them in `<pre><code>` under the picture.

Edge margins that pass the check on the first build (font-size 13–16): a top label needs `y ≥ 36`; a bottom label needs `y ≤ height − 28`; a side label needs `x` at least `글자 수 × 8 + 20` from the left or right edge. A label under a shape sits at least 12 units below the shape's lowest point (tails, stands, shadows included). When in doubt, add 20 to the viewBox height rather than squeezing the label up.

## Age levels

| level | reader | analogy | terms | mechanism | cards |
|---|---|---|---|---|---|
| 5살 | non-developer, no background | everyday objects only | none | none, only "what it does" | 4–5 |
| 입문 | beginner, junior | everyday objects + one real step | 1 per card, `한글(English) : 뜻` | one real step per card | 6–8 |
| 실무 | working developer | optional, only if it clarifies | as needed, defined on first use | real flow, trade-offs, failure modes, where it breaks in practice | 6–8 |

Other numbers map to the nearest level (5–12 → 5살, 13–25 → 입문, 26+ → 실무).

## Topic kind decides the order (all levels, strictest at 실무)

Classify the topic first. When unsure, treat it as a tool.

| kind | examples | order of cards |
|---|---|---|
| concept | hash, branch, DNS, cache | definition => mechanism => example |
| tool / command | rebase -i, grep, docker run, a CLI flag | **the pain without it** (show the actual mess: a log, an error, a screen) => the command => screen before/after => when not to use |
| procedure / workflow | PR flow, deploy, onboarding | step list => input and output of each step => where people get stuck |

Rules for tools:
- Never open a tool card with a definition. Open with "이게 없으면 이렇게 됨" and show the real artifact (ugly `git log`, the error text, the manual repetition).
- If the tool has a screen, write it as a terminal replay: what you type => what appears => the part you edit (highlighted) => the result. A simulator is optional and comes after the replay, never instead of it.
- Tie back to the lower levels' analogy in one line (e.g. "사진 4장 중 3장은 실수 수정 => 1장에 겹쳐 붙이기").

## 실무 specifics

- Start with `<p class="note">5살, 입문 탭을 먼저 보면 좋음</p>` when the page has lower levels; never assume the reader skipped nothing.
- Every term the 입문 level did not define gets a `한글(English) : 뜻` on first use (cherry-pick, upstream, merge-base, reflog ...).
- Glossary card comes AFTER the flow/mechanism widget, never before it, titled `용어 : 위 흐름에 나온 것`. Each row: plain Korean first, the 입문-level analogy in the middle column, the English term last. No row may introduce a second unexplained term.
- The definition card uses no acronym the reader has not met. Spell out what the protocol/tool fixes in three plain clauses; the formal names go in the glossary.
- Open with the one-sentence definition, then the mechanism diagram.
- If the mechanism is step-based, use the step widget (one change per step, a caption per step) instead of a static before/after.
- If the topic has a mode where the user edits something and sees a result (interactive rebase, config flags, query plans), build a small simulator: inputs on the left, live result on the right, plain JS, no libraries.
- Include: when to use / when not to, common mistakes, one concrete command or code snippet if applicable.
- Numbers carry sources in parentheses: `약 20% (자체 집계, 2026년 6월)`.
- No motivational filler. A working developer reads it in 3 minutes.

## Output

Publish with the Artifact tool. Title is the topic as a noun phrase (same string as `--title`).
