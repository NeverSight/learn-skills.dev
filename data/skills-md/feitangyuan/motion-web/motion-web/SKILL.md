---
name: motion-web
description: "Design and build motion-first creative websites — page design (structure, type scale, palette, spacing) plus interaction choreography: scroll animation, Framer Motion, GSAP, and light 3D via Three.js/R3F. Use for animated landing pages, creative portfolios, product showcases, WebGL-lite scenes, and motion audits. Also use when tuning interaction handfeel (手感差/太生硬/不跟手), replicating motion from a video or URL reference (复刻), building 3D depth from flat image assets (伪3D/抠图), diagnosing dead scroll-timeline stretches, mixing scene audio, auditing discoverability (点不开/没人会发现), building headless verification probes, or fixing a page that moves well but looks generated (不好看/像AI做的/没设计感). Equally for building a whole site from nothing (从0到1做个网页/落地页/官网/作品集): stack choice, sections and copy, components (导航/hero/表单/卡片/定价表), and production polish (favicon/OG/404/空状态/暗色模式). Not for dashboards, admin UI, or full 3D scene generation."
---

# motion-web

Motion-first creative web. The skill handles all phases: reference → concept → spec → build → audit.

**This skill builds whole web pages.** Motion is what makes them good; it is not the whole job. A
request with no motion in it at all — "做个落地页", "帮我把这个官网做出来" — is still this skill, and the
deliverable is a finished site: stack, tokens, sections, copy, components, states, meta, deploy.

**Priority order — 1 and 2 are co-equal:**
1. Motion concept and interaction choreography
2. **Page design** — structure, type scale, palette, spacing rhythm, the thing it looks like before anything moves
3. **The page as a built artifact** — sections and their copy, the component vocabulary, the token layer,
   the states off the happy path (`page-blueprints.md`, `components.md`, `project-setup.md`, `production-polish.md`)
4. Light 3D or canvas only when it strengthens the page
5. Performance, accessibility, reduced-motion fallbacks

**A great mechanic on a default-looking page is a failed page.** Motion is the *advantage*, not the
excuse. The most common failure of this skill is shipping one clever interaction glued onto a layout
nobody designed — if the page would embarrass you with the motion switched off, it is not done, and
no amount of spring tuning fixes it. Design is not step 2 in time; it is a second thing that must also
be true at the end. → `references/page-design.md`, `references/design-slop.md`

This *is* a design-and-build skill for one class of site: creative and marketing web — landing pages,
product pages, portfolios, studio sites, campaigns, editorial, light docs. It builds them end to end.
It is **not** a dashboard / admin / data-dense app-UI skill, and not a full 3D-scene generator
(those route to `3d-scene-studio`). A creative page containing app-shaped fragments — a pricing table, a
sign-in, a console screenshot — is in scope; a logged-in product interface is not.

---

## Agentic Intent Detection (CRITICAL — Read This First)

**The user will often say very little. Detect their intent from minimal input and act autonomously.**

### Signal → Intent Map

| What the user sends | Detected intent | What to do |
|---|---|---|
| "做个网页" / "做个落地页/官网/作品集" with a topic, no reference | `full-build` | **The whole site, not a mechanic.** [page-blueprints.md](./references/page-blueprints.md) → [project-setup.md](./references/project-setup.md) → [page-design.md](./references/page-design.md) → build → [components.md](./references/components.md) → [production-polish.md](./references/production-polish.md) |
| "这页要放什么" / "该有哪些 section" / "信息架构" / "文案怎么写" | `blueprint` | [page-blueprints.md](./references/page-blueprints.md) — pick a spine, write real copy, mark every invented fact |
| "导航" / "按钮" / "表单" / "卡片" / "footer" / "FAQ" / "定价表" / "弹窗" / "组件" | `component` | [components.md](./references/components.md) — the dialect table first, then the state matrix. A component without its states is not done |
| "用什么技术栈" / "Astro 还是 Next" / "怎么起项目" / "design token" / "字体" / "部署" | `setup` | [project-setup.md](./references/project-setup.md) — page ladder ≠ motion ladder; start at rung 0 and climb |
| "像 demo 不像成品" / "OG 预览是空的" / "没有 favicon" / "404" / "空状态" / "暗色模式" / "表单没校验" | `polish` | [production-polish.md](./references/production-polish.md) — all of it is checkable; run §9 rather than estimating |
| A bare URL (no other text) | `url-drop` | Open it and deconstruct it (Replicate Mode steps 1–2), then ask: rebuild this, or use it as the reference for something of theirs? |
| A URL + "做个网页" or "参考这个" | `replicate → build` | Deconstruct the URL first (Replicate Mode), then propose a motion concept for the user's own content |
| 参考 + "复刻出来并收录成 case" / "存进 skill" / "做成案例" | `case-authoring` | [cases/AUTHORING.md](./cases/AUTHORING.md) — Phase 0 gate first: strip the images out of the reference; if nothing survives, settle the assets **before** building, not after |
| A URL + "复刻" / "做一个类似的" / "参考这个做" | `replicate` | **Deconstruct → map to patterns → build immediately.** |
| A URL to a paper/article/blog | `doc-drop` | Read it, name the techniques with extractable values, build from one if asked (Document / Article Drop below) |
| A vague brief ("做个很酷的网页" / "做个 portfolio") | `freeform-build` | Orchestrate via [composition-guide.md](./references/composition-guide.md) → choose style+arc independently |
| A topic only ("做一个关于 AI 的落地页") | `spec → build` | Orchestrate via [composition-guide.md](./references/composition-guide.md) → propose visual direction, build immediately |
| A detailed brief with references | `spec → build` | Write MOTION_SPEC.md → get approval → build |
| "审查" / "有什么问题" / "gap" | `audit` | Inspect existing work for motion/perf/accessibility gaps — **including the still frame**, per [design-slop.md](./references/design-slop.md) |
| "不好看" / "太丑" / "像 AI 做的" / "没设计感" / "普通" | `design-audit` | Screenshot with motion **off** and run the gates in [design-slop.md](./references/design-slop.md). Do not tune springs — the complaint is about the still frame |
| "版式" / "排版" / "字太小" / "留白" / "结构" / "section 都长一样" | `design` | [page-design.md](./references/page-design.md) — macrostructure, type scale, spacing rhythm, measured against current award winners |
| "加上…" on existing page | `incremental-build` | Extend current implementation with new motion |
| A **video** reference (Pinterest/Dribbble/X clip) | `video-ref` | **STOP — run the Video Reference Protocol below before writing any code** |
| "手感差" / "太生硬" / "不跟手" / "四平八稳" on existing motion | `handfeel-tune` | Audit against [handfeel.md](./references/handfeel.md) — springs, velocity coupling, secondary motion |
| "跟手但总差一点" / "一抖一抖" / 手感随帧率变 on anything that **follows** (camera, cursor, rail, tooltip) | `handfeel-tune` | Not §1's spring — [handfeel.md](./references/handfeel.md) §7: `1-exp(-k·dt)`, the `speed/k` lead term, and never correcting after the filter |
| "能不能不用 GSAP" / 只是个入场或视差 / 想要更轻 | `build` | Check rung **1.5** first — native `animation-timeline` / `animation-trigger` / `sibling-index()` → [build-mode.md](./references/build-mode.md) ladder + [pattern-recipes.md](./references/pattern-recipes.md) #16. Firefox gets the static end-state |
| 素材是一个**真实存在的地方**（实拍/扫描），要走进去 | `build` | Rung **5.5** — 3D Gaussian splats before models → [build-mode.md](./references/build-mode.md) ladder |
| 卡片/图片要**弯折**、旗帜、翻页、把截图钉进立体面、"skew 不够用" | `warp` | Corner-pin homography → [pattern-recipes.md](./references/pattern-recipes.md) #17. **Guard every quad and clamp edge tilt to `asin(h/w)`** — an unguarded quad paints a screen-sized block with no error |
| "点不开" / "只有一个能点" / "没人会发现" / "看不到" on existing motion | `affordance-audit` | **Do not touch hit-test code first.** Audit against [affordance.md](./references/affordance.md) — the mechanism is usually fine; the invitation is missing or expired |
| A pile of **image assets** + "做成一个 3D 场景" / "要有纵深" / "camera 要能走进去" | `image-plane-3d` | **Do not reach for models.** Build the scene from flat planes in a real perspective camera → [image-plane-3d.md](./references/image-plane-3d.md) (ladder rung 5) |
| "有拼接感" / "没融进去" / "像贴上去的" on a rendered scene | `image-plane-3d` | Measure before touching art: mean `R−B` and luminance per asset batch, contact shadows present → [image-plane-3d.md](./references/image-plane-3d.md) §6–7 |
| "这个该用什么画" / "DOM 还是 canvas" / 页面只会输出 div 和系统字体 / 参考明显不是 DOM 能做的 | `render-layer` | **先定层再定机制** → [render-layer.md](./references/render-layer.md) §1。层是一个声明，写进 case README，由 `verify_case.py --layer` 核对 |
| 手绘 / 墨线 / 描边风的 3D，"像画出来的不像渲出来的"，boil / 抖线 / 纸纹 | `ink-render` | [render-layer.md](./references/render-layer.md) §3 — 深度不连续描边（法线折痕关掉）、静态 warp 与动态 boil 分离、boil 时钟 11Hz 对 60fps 渲染 |
| Raw plates / renders that still need cutting out, "抠图", "素材怎么进场景", "图糊了" | `asset-pipeline` | Key against the image's **own** background, crop to the alpha bbox, script the metadata, print the per-element resolution budget → [image-asset-pipeline.md](./references/image-asset-pipeline.md) |
| Any headless check; a number disagrees with what you see; "怎么验" | `verify` | Build the probe surface first — pinnable clocks, `__seek`, `__hold`, state exits — then measure → [verification-harness.md](./references/verification-harness.md) |
| "这一段什么都没发生" / "节奏不好" / "一堆字一下就出来了" on a scroll timeline | `timeline-audit` | Lay every track against one scroll axis; dead beats are coinciding plateaus, not one slow layer → [timeline-orchestration.md](./references/timeline-orchestration.md) |
| Long scroll scene with many assets; "卡", "加载慢", "内存爆了", hundreds of plates | `scene-streaming` | Activate by screen window, slice big uploads, yield inside the scan, dispose completely → [scene-streaming.md](./references/scene-streaming.md) |
| Anything with sound — BGM, ambience, interaction SFX, "音效太少", "氛围音听不清但也别吵" | `scene-audio` | Three buses (bgm / hand / world), per-act curves, discrete events over a louder bed → [scene-audio.md](./references/scene-audio.md) |

**Never ask the user what mode to use.** Detect it. Proceed. Only stop if the brief is truly ambiguous between two very different outputs (e.g., spec vs. immediately building).

---

## Video Reference Protocol (硬规则 — 不许猜)

**Trigger: the reference is a video you cannot actually watch** — Pinterest pin, Dribbble shot, X clip, 站外短链. A title or text description is NOT motion information.

0. **Read the thread before you conclude there is no live page.** The author almost always posts the
   URL in a reply, and the replies also tell you whether the piece is even a web page. Measured
   2026-09-02: a previous session declared seven video references URL-less and spent its Phase 1 on
   frame measurement; **all seven had live sites, posted by the authors themselves**, and three of
   four clips in one post turned out to be Jitter / Figma Motion / Rive renders with no web
   implementation at all (`cases/AUTHORING.md` Phase 1). `safe-x tweet <url> --json`, then resolve
   every `t.co` link in the replies.
1. **Never build motion from a guess.** If all you extracted is a title/description, you know the *topic*, not the *motion*. Building anyway burns a full iteration — this is a documented failure mode (2026-07-06, seafood hero: guessed "orbit", actual was a rising diagonal; two rebuilds).
2. **Ask for 2–3 keyframes immediately.** One sentence: "这个视频我打不开，截 2-3 帧关键画面（入场/中间/离场）发我"。
3. **State the trajectory as explicit geometry before coding**, and get confirmation:
   - Anchor points: where the element enters / crests / exits (corners, thirds)
   - Attitude: rotation follows path tangent / stays constant / lags behind
   - Secondary reactions: what else moves (background shapes, lines, text) and how
   - Example: "右下入场 → 中心 → 左上离场的上升对角线，鱼头恒定朝左上" — wrong guesses die here, not in code
4. Only then map to pattern-recipes / handfeel.md and build.

A single screenshot follows the same rule: one frame gives pose, not trajectory. If the *path* matters, ask for more frames.

---

## Replicate Mode (复刻模式)

When the user sends a URL with "复刻" / "做一个类似的" / "能不能做这种效果" — deconstruct it, then build. There is no storage step; the deliverable is the page.

### Replicate Execution Path

1. **Open the page and read it as three layers**, with whatever browser tooling is available (Claude
   Preview, `browser-use`, Playwright): the **stack** (library, easing, keyframes, CSS variables — the
   bundle names them), the **scroll choreography** (which element is pinned over which band, rails and
   their px distance, parallax rates, scrubbed properties, entrance points — sample ~9 scroll positions
   and diff `getBoundingClientRect` plus computed styles between them), and the **WebGL layer** (program
   count, draw calls, custom uniform names; wrap `getContext` before page scripts run if you need the
   shader sources). Two scripts cover the measurable halves: `scripts/measure_structure.py <url>` for
   the static page (sections, nav, buttons, token scales, media, meta, mobile overflow) and
   `scripts/measure_churn.py <url>` for how much of the page actually moves under a real wheel.
   **The URL must be the work itself**, never a gallery listing (`awwwards.com/sites/<slug>`): a
   listing page hands you the gallery's own chrome, and six different winners come back with the same
   library, the same keyframes and the same font.
2. **Deconstruct** — state what you found, and quote the numbers rather than impressions:
   - "GSAP 3.12 + ScrollTrigger + Lenis；`.home-animate__wrapper` 在 0.25–0.50 被 pin 住，
     期间 `.icon` 横移 +1545px，出场是 0.25/0.38/0.62 三段 stagger"
   - "背景是原生 WebGL2，14 个 program、944 draw calls，uniform 里有 bloomStrength/blurTexture1-5
     和 cloudCoverage/cloudDensity —— 是 UnrealBloom + 体积云"

   **Never report "用了 WebGL" off a context alone** — an unsized 300×150 context with no linked
   program is Modernizr-style capability detection, not a scene. Count linked programs and draw calls.
3. **Map to pattern-recipes** — find the closest recipe in `references/pattern-recipes.md`
4. **Fill the gap** — what the reference uses that we don't have in recipes, write from scratch based on extracted values
5. **Build immediately** — scaffold the page, run it, verify visually
6. **Report** — "复刻了 [site] 的核心动效，用了 [X] 实现 [Y]，和原版差异是 [Z]"

### Replicate ≠ Copy

- **Do**: Recreate the interaction pattern, motion character, timing feel
- **Don't**: Copy proprietary brand colors, exact copy text, identifiable product UI
- **Do**: Adapt the technique to the user's own content and palette
- Note in the report what was adapted vs. what was faithful to the original

---

## Freeform Build Mode (When User Gives Zero Direction)

When the user says "做个网页" / "随便做" / "自己想一个主题" or gives a simple vague topic (e.g. "做一个AI agent平台落地页"), this is an invitation to be creative.
**Do NOT default to a generic template, do NOT use rigid 1-to-1 routing mapping, and do NOT ask clarification questions.**

### Freeform Action Path (Runtime Creative Loop — 创造发生在执行中，不在文档里)

The user should NEVER need to supply a reference. But novelty also does NOT come
from reading these docs — docs are constraints and physics, not answers.
Novelty comes from **fresh inputs sampled at runtime + a build-test-kill loop
where you are your own critic**. Execute:

1. **Sample the present** (runtime input, not memory): open this month's
   Awwwards SOTD / Godly / SiteInspire listings and look at 3–5 of the winning
   pages themselves — the work, never the gallery page. You're not copying;
   you're locating the current frontier so you can land past it. 2 minutes.
   Look at **structure and type scale**, not only the effect — that is the half
   that decides whether the page reads as current (`page-design.md` §1).
2. **Invent 3 candidate mechanics** from the topic's own physics via the
   generative operators (composition-guide §5). Kill any candidate that
   resembles the graveyard OR anything you just saw in step 1.
3. **Sketch before committing**: build the signature interaction as a minimal
   single-file prototype (one div, one rAF loop, fake content, <15 min).
   Not the page — just the mechanic.
4. **Test it on yourself**: run it and drive it with the currently available
   browser tooling — Claude Preview (`preview_start` → `preview_eval`/`preview_click` →
   `preview_screenshot`) first, `browser-use` as fallback — mouse sweeps, wheel
   flicks, screenshots at extremes, then look at the evidence. Ask:
   会不会玩 10 秒就腻? 截两帧给人看,能不能猜出交互规则? If it fails — mutate the
   operator or pick the next candidate. Do not ask the user to be your eyes.
5. **Design the page — as a separate act, before the mechanic goes into it.**
   Not "pick a palette and start coding". Three outputs, in order:
   (a) the **blueprint and the real copy** → `references/page-blueprints.md` — which
   sections exist and what they actually say; (b) the **macrostructure, type scale
   and spacing rhythm** → `references/page-design.md`, with concrete values in
   `data/visual-bank.json`; (c) the **token layer and scales** →
   `references/project-setup.md` §2–§5. The mechanic then gets placed *into* a page
   that already works, which is the opposite order from the one that produces
   「一个破动效贴在没设计的页面上」.
6. **Build it**, components and their state matrices from `references/components.md`,
   springs from `references/motion-tokens.md`, full-page linkage per handfeel.md.
7. **Design gate — run this before you show anything.** Screenshot the page with
   **all motion disabled** (`prefers-reduced-motion`, or comment out the mechanic)
   and judge that still frame on its own:
   - Would this still frame place on Awwwards with zero animation? If the honest
     answer is "no, it's a centred headline and three cards", the design is not done.
   - Run the slop gates in `references/design-slop.md`. Any hit = revise, not ship.
   - Only then ask the motion questions: 会不会玩 10 秒就腻? 截两帧能不能猜出交互规则?
   A page that passes step 4 and fails this one is the documented failure mode this
   loop exists to prevent — step 4 only ever tested the mechanic.
8. **Finish it**: `references/production-polish.md` — head, OG, favicon, 404, the
   states off the happy path, and the ten manual checks in §9. A page that stops
   before this is a demo, not a deliverable.
9. **Bury the mechanic**: append one line to the graveyard (composition-guide)
   so it can never be reused — the loop stays forced-fresh.

Pitch to the user only if two surviving candidates are genuinely different
directions; otherwise just build the best one and explain the metaphor after.

---

## Document / Article Drop

If the user drops a paper, article or design blog: read it, name the 2–3 techniques in it that carry
extractable values (library, easing, timing, a shader idea, a layout rule), and ask one question —
build from one of them now, or keep going with the brief? If they say build, the most distinctive
pattern becomes the page's primary motion concept and goes through the same Build Order as everything
else. Nothing is stored; a technique that mattered goes into `pattern-recipes.md` after it has shipped.

---

## Modes (for explicit user direction)

- `spec`: turn a brief + references into a buildable `MOTION_SPEC.md`
- `build`: implement an approved motion-first web experience
- `audit`: inspect an existing motion-heavy page or implementation for gaps
- `design-audit`: the complaint is about how it *looks*, not how it moves — judge the still frame first
- `replicate`: deconstruct a reference page in numbers, then rebuild the pattern on the user's content
- `freeform-build`: user gives no direction → make creative choices independently
- `full-build`: build a whole site 0→1 — blueprint + copy, stack + tokens, design, components, motion, polish
- `blueprint`: decide what sections a page needs and write their copy
- `component`: design/build a specific component with its full state matrix
- `setup`: pick the page stack, scaffold the project, lay the token/type/font layer
- `polish`: the finishing pass — meta, OG, 404, off-happy-path states, dark mode, pre-ship checks

---

## Build Order (Always Follow This)

0. **Pick the page stack** → `references/project-setup.md` §1 — one HTML file / Vite / Astro / Next. This is a
   *different ladder* from the motion one; do not let either pick the other. Start at rung 0.
0.5 Pick the motion stack rung → `references/build-mode.md` **Tech Stack Decision Ladder** — lowest rung that reaches the goal; never default to R3F because the reference "looks 3D", and never default to *models* because the scene needs depth (rung 5 builds the whole scene out of images)
1. **Pick the blueprint and write the copy** → `references/page-blueprints.md` — which sections exist, in
   what order, and the real words in them. Layout is a response to real text; placeholder copy means the
   page has not been designed. Then pick arc type → `references/choreography-arc.md`
2. **Design the page** → `references/page-design.md` — macrostructure, type scale, palette, spacing
   rhythm. Concrete values in `data/visual-bank.json`. This is a real step with its own output, not a
   line item: decide what the page looks like **with the motion switched off**, and be willing to
   defend that still frame on its own
2.5 **Lay the token layer and the scales** → `references/project-setup.md` §2–§5 — three-level tokens,
   fluid type scale with a real jump, space scale, fonts with metric overrides, `@layer` order. Doing this
   after components exist means editing every component.
3. Pick motion tokens → `references/motion-tokens.md` (duration, easing, spring)
3.5 **Build the component vocabulary** → `references/components.md` — pick the dialect (creative vs product,
   the two are measurably different systems), then give every interactive component its full state matrix.
   A missing `:focus-visible`, error or empty state is the most common "像 demo" cause.
4. Check pattern library → `references/pattern-recipes.md` for reusable implementations
5. **If the scene is built from image assets, run the asset pipeline before the runtime** → `references/image-asset-pipeline.md`. Cutouts, scripted metadata, per-element resolution budget. No amount of shader work fixes an asset that was keyed against the wrong background or is being enlarged 0.83×. Decide the **topology** at the same time (camera moves vs world moves → `image-plane-3d.md` §12) and, if it is long, the **streaming policy** → `references/scene-streaming.md`
6. Implement per → `references/build-mode.md`, **building the probe surface as you go** → `references/verification-harness.md` §1 (retrofitting `__seek` / `__hold` / pinnable clocks costs more than building them)
7. For a multi-track scroll timeline, lay the tracks out horizontally → `references/timeline-orchestration.md`; if the page has sound → `references/scene-audio.md`
8. For anything interactive that isn't an obvious button: mark the invitation per → `references/affordance.md`
9. **Run the design gate before the motion gate** → `references/design-slop.md`. Screenshot with all
   motion disabled and judge that frame first; a page that only works while moving has not been designed
10. **Finish it** → `references/production-polish.md` — head/OG/favicon, 404, the states off the happy path,
    dark-mode decision, and the ten manual checks in §9. Skipping this is what makes a good page read as a demo
11. Verify desktop + mobile + reduced-motion + **the affordance checklist and its numeric oracles**

**Mandatory pre-flight — not optional, not a suggestion:** before writing a single line of GSAP, Framer Motion, or Three.js/R3F code, open the matching framework section in `references/build-mode.md` (Framework-Specific Rules) and the `Failure Patterns to Avoid` table. Do this even if you're confident you remember the pattern — the table exists specifically because remembered patterns silently regress (e.g. GSAP `.from()` without `gsap.context()`/`.revert()` under React StrictMode). Skipping this step and reinventing a fix that's already documented there is a process failure, not a stylistic choice.

---

## Load Only What You Need

| Mode | Read these references |
|---|---|
| `spec` | motion-spec.md + baseline-ui.md + choreography-arc.md |
| **every build, without exception** | **page-design.md + design-slop.md** — the still frame is half the deliverable |
| a brief in a case's class, or you need its mechanism | the case's `README.md` first (it has the 可以照搬/不许照搬 split), then its `index.html` |
| **every 0→1 site build** | **page-blueprints.md + project-setup.md + components.md + production-polish.md** — sections & copy, stack & tokens, component states, the finish |
| `full-build` / "做个网页" with no reference | page-blueprints.md + project-setup.md + page-design.md + design-slop.md + composition-guide.md + components.md + production-polish.md |
| `blueprint` / "该有哪些 section" / 信息架构 / 文案 | page-blueprints.md + page-design.md §1 |
| `component` / 导航 / 表单 / 卡片 / footer / 弹窗 | components.md + baseline-ui.md + (affordance.md if it isn't an obvious button) |
| `setup` / 技术栈 / token / 字体 / 部署 | project-setup.md (+ build-mode.md ladder for the *motion* stack) |
| `polish` / 像 demo / OG / favicon / 404 / 空状态 / 暗色模式 | production-polish.md + baseline-ui.md |
| `build` | build-mode.md + motion-tokens.md + pattern-recipes.md + (light-3d.md if canvas/WebGL) |
| `image-plane-3d` / scene built from image assets / "有拼接感" | image-asset-pipeline.md + image-plane-3d.md + light-3d.md + verification-harness.md + (scene-streaming.md if it's long; affordance.md if anything in the scene is clickable) |
| `scene-streaming` / 长滚动大场景 / 卡 / 加载慢 | scene-streaming.md + image-asset-pipeline.md §6, §9 |
| `asset-pipeline` / 抠图 / 素材元数据 / 图糊了 | image-asset-pipeline.md (+ image-plane-3d.md §2 for how the runtime consumes it) |
| `verify` / building any oracle / a metric disagrees with the eye | verification-harness.md + affordance.md §9 |
| `timeline-audit` / scroll-driven多拍编排 / "这一段什么都没发生" | timeline-orchestration.md + choreography-arc.md |
| `scene-audio` / BGM / 环境音 / 交互音效 | scene-audio.md + verification-harness.md §3 |
| `freeform-build` | page-design.md + design-slop.md + composition-guide.md + choreography-arc.md + visual-bank.json + motion-tokens.md + pattern-recipes.md |
| `audit` | build-mode.md + motion-tokens.md |
| `handfeel-tune` / "不跟手" complaints | handfeel.md + motion-tokens.md |
| `affordance-audit` / "点不开" / "发现不了" complaints | affordance.md + handfeel.md |
| `video-ref` | (protocol above) then handfeel.md + pattern-recipes.md |
| `replicate` / `url-drop` | pattern-recipes.md + handfeel.md + page-design.md + design-slop.md |
| portfolio/personal site | page-blueprints.md (the portfolio blueprint) + components.md |

---

## Core Rules

- Motion is the main design material, not the final polish layer.
- **Anything that follows something else is not a spring problem.** Cameras, cursors, rails and tooltips
  must arrive and stop. Steady-state lag behind a moving target is `speed / k` — arithmetic, not a tuning
  failure — and a correction written after the filter gets undone next frame (`handfeel.md` §7).
- **「飘」 is a stillness ratio, not an easing curve.** Easing changes how fast the source is read; it never
  changes how often a new state appears. Measure the fraction of near-identical adjacent frames before
  touching a curve (`timeline-orchestration.md` §11).
- **Climb the ladder from rung 1.5, not rung 4.** A reveal, a parallax band, a stagger and a scroll-spy nav
  are now native CSS; author the finished state first and put the timeline behind `@supports`, because
  Firefox implements none of it (`build-mode.md` ladder, `pattern-recipes.md` #16).
- **Buildable ≠ findable.** An interaction is not done when it works; it is done when a first-time visitor
  discovers it without being told. Every interactive element that isn't an obvious button owes an answer to
  the three questions in `references/affordance.md` §1.
- **The test has to encode the user's complaint, not your model of it.** If the user says "I can't open it"
  and your check says "it opens", you are measuring a different thing — go find their question first.
- **Decide what number would prove it, then print that number.** Screenshots are expensive and settle
  nothing. Coverage sweep, handoff size error, safe-area containment, window-vs-dwell — all one headless
  run (`references/affordance.md` §9).
- **A general quality score is worse than no test.** Every oracle must encode one stated complaint; the
  aesthetic verdict stays with a human looking at the thing (`verification-harness.md` §0).
- **Assets before runtime.** In an image-built scene the metadata is a build artifact, never a hand-edit —
  if you are nudging a `baseline` to make something sit right, the bug is upstream (`image-asset-pipeline.md`).
- **A dead beat is several layers' flat sections landing together**, not one slow layer. Read a scroll
  schedule horizontally (`timeline-orchestration.md` §1).
- **The deliverable is a page, not a mechanic.** A brief with no motion in it is still this skill, and the
  job is a finished site — sections with real copy, a component vocabulary with its states, a token layer,
  meta and a 404. Handing back one beautiful interaction and a template around it is the failure this
  skill's whole design half exists to prevent.
- **The two component dialects are measurably different systems.** Creative pages: median **1** distinct
  radius, **0** shadowed elements, 37 % uppercase buttons, no nav CTA, a 2-column footer. Product pages:
  median **8** radii, ~18 shadowed elements, 1 % uppercase, 2 nav CTAs, a 5-column 35-link footer
  (n=32, `components.md` §1). Pick one and be consistent — building a creative page out of product
  components *is* the "像 AI 做的" complaint.
- **A component without its states is not built.** hover / `:focus-visible` / active / disabled / loading /
  error / empty / success. The missing state is almost always the one the user notices
  (`components.md` §2).
- **Copy before layout.** Layout is a response to real text length; a page laid out around placeholder
  copy has to be redone. If the user supplied no facts, write the draft and mark every invented slot
  `[…]` — never invent proof (`page-blueprints.md` §4, `design-slop.md` A8).
- **Award-winning is not well-built.** In the same 32-site run, 2 of 18 award sites had horizontal
  overflow at 390px, 5 had no `<h1>`, and only 37 % of their images reserved a box. Copy their design
  language; do not copy their hygiene (`production-polish.md`).
- **A projective transform has a legality condition, and violating it fails silently.** Corner-pin
  (`matrix3d`) only behaves while the destination quad stays convex — past that the homography flips
  through infinity and paints a screen-sized block with no console error. Guard the quad *and* clamp
  edge tilt to `asin(h/w)`; the guard alone is a visible snap (`pattern-recipes.md` #17).
- **From `cases/`: take the mechanism, never the skin.** The source ships in full because re-deriving a
  solver is waste — but palette, type values, grid, section order and copy belong to that case. A page
  that is a case with the logo swapped is the failure mode, not the shortcut.
- **A probe that bypasses the event handlers tests a path nobody takes.** One case passed
  every probe-driven check — landing error 0.0000°, all slots reachable, both ends clamped — while
  being completely dead to a real scroll wheel. Every oracle must drive at least one **real** gesture,
  and `verify_case.py` now does this on every page.
- **Placeholder geometry passes every oracle and still looks like nothing.** Grey gradient rectangles
  standing in for photographs clear the type-ratio, dead-beat and state-matrix checks and still read
  as a technique diagram. No metric detects it and none should be invented — decide whether the
  artwork exists **before** the build, not after (`cases/AUTHORING.md` Phase 0).
- **An oracle that pins its input and settles has not tested the page anyone uses.** Every assertion
  in `--strings` originally ran against a frozen clock; unpinned, a drifting endpoint or a body that
  never stops sloshing is invisible to all of them. Whatever your mechanic is driven by, add a pass
  that lets it run free. (And when a live readout looks alarming, check the loop is running first —
  a hidden browser tab suspends `requestAnimationFrame`, and a frozen sim reports plausible,
  completely wrong numbers: `cases/string-clock` 踩过的坑 #7.)
- **An inline style declaration outranks every rule in the stylesheet, including `:hover`.** A stack order written as `el.style.zIndex` silently kills `.thing:hover{z-index:…}` — the hover still *looks* live because its colour change comes from the same rule that did win, so the promotion is dead and nothing reports it. Ship per-element state as a custom property
  (`el.style.setProperty('--z', n)`) and let the rules read it.
- **Never build from a summary of a reference you could open yourself.** A previous session compressed a video into one sentence for a hand-off; building from that sentence produced a resizable window the reference does not have, an eased entrance it does not have, and a scrolling marquee that measures 0 px of movement per frame. The clip was on disk the whole time. A contact sheet gives pose; only the frames give **trajectory, cadence and stillness**
 .
- **An oracle threshold comes from a measurement or from a design requirement you can state — never from taste.** A "no clumping" band of nearest-neighbour CV [0.08, 0.40] looked principled and the reference itself scored 0.507: it places at random and lets cards overlap hard. The real contract was elsewhere — **z-order is arrival order, so the newest card is never buried** — and that one is worth asserting.
- **Decide what the page is *drawn with* before you decide what it does.** Seven cases shipped as DOM + CSS on the system font stack while every reference was something else; nothing in the skill ever asked the question, so every brief resolved to divs by default. The layer is a declaration in the case README, and `verify_case.py --layer` checks it (`references/render-layer.md` §1, `cases/ink-crowd`).
- **Some numbers only exist in the source.** The 11 Hz boil clock that decides whether a frame reads as drawn is invisible to frame-differencing: sub-pixel displacement under camera motion, 95 % of frames differ, autocorrelation flat. Measuring pixels would have produced a confident wrong answer. Fetch the bundle and read it (`cases/ink-crowd` §1).
- **"Take the feel, not the layout" means taking the motion first.** A build that lifted a reference's palette and grain and shipped a static page passed every gate in the floor: the page looked right and did nothing. Characterise the reference's motion in numbers before touching the design — per-layer velocity and how much of the time anything is moving — and assert liveness with no input.
- **Whole-frame correlation cannot measure a multi-layer scene.** Layers moving at different rates, some in opposition, cancel to a median shift of zero. Track one colour or feature mask per layer instead.
- **Check a tiled texture's period against every repeating dimension near it.** A 128 px noise tile over an 11-band strip on a 1440 px canvas (130.9 px per band) beats into vertical streaks — the one artefact film grain never has. Writing noise into the pixels avoids the whole class.
- **A pointer that aims into a 3D scene must intersect the plane the *content* sits on, not the ground.** Figures are 1.75 units tall; a ray aimed at a body and intersected with `y = 0` lands far behind it, and near the horizon it runs away entirely. The symptom is not "slightly off" — it is a mechanic that works in one screen band and is completely deaf everywhere else, while its own counter still reports activity (`cases/ink-crowd` §4, `verify_case.py --follow`).
- **Two answers to "pin a screen", and they exclude each other.** Hijack the wheel and translate a rail: you can compute any progress you like, and `position:sticky` will never fire because the ancestor is transformed, so every pinned child must be parked by hand. Leave scroll alone and stack `sticky; top:0; height:100vh` screens: pinning is free, and progress has to be read back out of the document as `(scrollY - offsetTop) / innerHeight`. Pick before laying anything out; retrofitting either onto the other is a rewrite (`cases/wheel-rail` §2, `cases/press-stack` §2).
- **A sticky stack of one-viewport screens has no dwell at all.** Each screen is fully visible at exactly one scroll position, so every animation inside it plays in the half already being covered, and scrolling reads as dead. `margin-bottom: 100vh` on each screen buys a viewport of dwell without changing its box. Then progress splits: content uses `(scrollY - top) / vh` while the screen is whole, and only exit effects use `(scrollY - top - vh) / vh` (`cases/press-stack` §2).
- **Read the layout in the oracle; never assume it.** `--stack` hardcoded "one screen per viewport" and reported 1 of 8 pinned the moment the layout gained a dwell — a green-to-red flip caused entirely by the check, not the page. Section positions come from the probe (`cases/press-stack` §3).
- **A sticky stack eats the bottom of the screen first.** The next screen rides up from below, so anything anchored with `margin-top:auto` is the first thing covered. A headline, a giant numeral and a section rule all disappeared on the first build for this one reason. Content belongs in the upper two thirds (`cases/press-stack` §2).
- **Album covers are drawable; people are not.** Sleeves are a colour field, two shapes and a line of type; a record is concentric grooves plus two narrow specular arcs — a wide wash across the disc reads as a gold plate. Both are better generated than faked with a grey rectangle. A portrait or a hand is neither: leave the slot out and redesign around it rather than stacking primitives into a figure (`cases/press-stack` §4).
- **Density is a device, and the underlay is where it comes from.** A page can carry every motion mechanism the reference has and still read thin: 184 elements against the reference's 584. The gap was not more copy — it was the technical-drawing underlay the reference puts beneath everything: a hairline grid, act rules, range markers. Twenty elements, each of which draws itself and tracks the pointer, and the same screens stop looking like a wireframe of the reference (`cases/wheel-rail` §3).
- **A reference clip on disk outranks the live site.** Built from headless screenshots of `blink.trade`, this case reproduced the palette, the type and the scroll device and still got "the fuzzy round thing never changes". The clip showed the signature element is a radar sweep — a hand turning over a dotted ring, trailing a soft wedge that closes and clears in 0.92 s. A still frame cannot represent the one thing that made the page. **If a clip exists, watch it before building, even when the live site is reachable** (`cases/wheel-rail` §2b — and this is the second time it cost a rebuild).
- **Input-driven and ambient are not alternatives.** The correction "interaction motion means motion the mouse produces" is about what is *missing*, never a licence to strip the ambient layer. The reference runs both: wheel and pointer drive the layout and every reveal, and the sweep turns regardless. Assert both — churn under real input, and liveness with no input at all (`verify_case.py --rail`).
- **A rail that translates is not choreography.** A hijacked wheel moving a rail while every child element holds still is a scrollbar in costume — and it passed four `--rail` assertions before anyone looked at it. Measure how many elements actually change under real wheel input: the reference moves 64 %, the rejected build moved 13 %. Assert the churn, and assert that some elements are caught *mid*-transition, or a page that snaps between states satisfies the count and still reads as a slideshow (`cases/wheel-rail` §3).
- **Split the text or the page has nothing to animate.** The reference wraps every word in an inline-block span — 296 of them — at `translateY(8px)` / `opacity 0` with `transition-duration: 0s`, i.e. written per frame rather than handed to CSS. That single decision is most of the 64 %. Writing the values yourself is also what makes the reveal scrub backwards when the wheel reverses (`cases/wheel-rail` §2).
- **A scroll-mapped reveal on something already on screen resolves to "finished" on frame 1.** The hero diagram's draw-on never once played, because its section's `top` is 0 at rest so the progress clamps to 1 immediately. Anything visible at rest needs its own load clock; only what starts below the fold can be mapped to scroll (`cases/wheel-rail` §2).
- **Interaction motion means motion the mouse produces.** Wheel and pointer, nothing else. A page that drifts, breathes and dissolves on its own clock while the mouse sits still is a screensaver, and it will satisfy a "add motion" brief while failing the actual request. Ask which input drives it before building (`cases/wheel-rail` §0).
- **A probe that reads back what the code wrote cannot tell you what the screen shows.** An oracle asserting a hard cut read `el.style.opacity` — the inline value the loop sets — and reported a perfect flipbook for a copy with `transition: opacity 250ms` added, because a transition interpolates *between* inline values and the inline read jumps straight to the target. `getComputedStyle` catches it at 19 of 60 samples mid-transition. This is the probe-only lesson one layer down: the first version tests intent, not rendering (`cases/toy-flipbook` §5 #2).
- **A low-probability effect needs a driver that clears its threshold, or the assertion was never run.** A desk-toy kick fires only above `|v| > 2.2` and then wins a 6 % roll; a pointer sweep peaks at exactly 2.2, so the leg reported 0/5 and could not distinguish a broken mechanism from a test that never triggered. Drive it with something that overshoots, and **print the peak and fail if it never cleared the threshold** — a leg that did not run must say so rather than pass or fail silently (`cases/toy-flipbook` §5 #3).
- **A comment can promise what the code has never once done.** `s.v = s.v < -30 ? -s.v * 0.35 : 0` sat under a comment reading "bounce, then rest" in shipped code; `s.v` is positive while falling, so the branch never ran and every toy stopped dead on contact. It looked fine — you only miss a bounce if you know it was meant to be there. Assert the *consequence* (the squash) rather than the movement, and the dead branch surfaces immediately (`cases/toy-flipbook` §5 #1).
- **`file://` refuses a CSS mask and allows an `<img>`, so a page can be half-lit and look almost right.** `mask-image: url(img/x.webp)` is a CORS fetch from origin `null`; the photograph loads, the lighting silently does not, and three console lines are the only evidence. Inline the mask as a `data:` URI and leave the display image external — a mask carries alpha only, so 320 px and flat RGB is ~4 KB against 75 KB for the photo it clips.
- **An oracle's baseline must be measured still, never waited out — a fixed settle time let a copy with the pointer force set to ZERO pass every assertion.** `verify_case.py` fires one real wheel in its own smoke test; on a page that turns a wheel into a decaying impulse, a hard-coded 2.6 s settle landed *inside* the 2.7 s decay, so the page was still drifting on its own and every later displacement was credited to the pointer. Poll the probe until motion is under threshold, and fail if it never settles. A settle time that is long enough today stops being long enough the moment someone adds an entrance (`cases/char-curtain` §5 #1).
- **A ratio dominated by structure cannot test the force that produced it.** An anisotropic pointer push (x at full, y at 0.35) looked testable as "is horizontal displacement much larger than vertical" — 7.9× on the real case. A copy with the bias set to 1.0 measured **8.8×**, higher, because the vertical links absorb y motion by sliding nodes along the string. Assert the structural claim the code actually makes instead: poking one column must leave a distant column alone (`cases/char-curtain` §5 #2).
- **A rate limit computed once per frame is not a rate limit.** The budget was read before a loop over nine emitters and passed in as a flag, so all nine could fire on the same frame: a stated cap of 4 measured 6 and allowed 9. Re-read the budget inside the loop *and* guard again at the moment of the push. The overshoot is invisible by eye, which is why only an oracle finds it (`cases/lyre-crows` §5 #1).
- **An assertion can match a string the page is structurally unable to produce.** A check for the full replacement sentence failed against a perfectly working page, because the tail holds a fixed node count and anything longer is truncated. Assert that state *changed* — against a snapshot taken before the interaction — rather than that it changed into one exact value (`cases/lyre-crows` §5 #2).
- **A pure-canvas page is invisible to the floor's input check, and that is a finding about the page, not the check.** The change signature is scrollY plus computed styles plus `innerText`; canvas pixels are in none of them. A demo that is one `<canvas>` can be full of motion and still fail "a real wheel event changed nothing" — and a visitor who has not moved yet, or anyone using a screen reader, gets exactly as little as the checker does. A small live readout in the DOM fixes both at once (`cases/char-curtain` §5 #3).
- **One flaky fetch in a hundred runs is enough to make a whole suite untrustworthy, and a CDN font is the usual culprit.** Two cases kept a Google Fonts `<link>` because substituting a lookalike face would have changed the design rather than ported it — sound reasoning, wrong conclusion. A full-suite run went red once on `console/page errors`; twelve deliberate re-runs were clean. An intermittent failure nobody can reproduce is worse than a consistent one, because the first thing anyone does with it is stop trusting the suite. Keep the real faces and remove the network instead: fetch the OFL originals, subset each to the characters its own page renders (65.8 → 40.9 KB for a variable serif), inline them.
- **Prove an oracle by breaking the case.** `--rail`'s hijack assertion passed a copy with `preventDefault()` deleted, because `overflow:hidden` already pinned `scrollY`. The check was vacuous and would have stayed vacuous forever. Run every new oracle against a deliberately broken copy of its own case before filing it (`cases/wheel-rail` §3).
- **`position:sticky` does not fire inside a transformed ancestor.** Any pinned element inside a hijacked rail has to be parked by hand against the rail offset. This is not a bug to debug — it is the spec (`cases/wheel-rail` §2).
- **A post-process pass ships with a debug channel or it is undebuggable.** "The heads render as black blobs" sent me into the capsule mesh; one look at the raw colour buffer showed shadows above the figures, i.e. an inverted camera basis. Expose raw colour / linear depth / edge magnitude from the first frame you write (`cases/ink-crowd` §4).
- **Stillness is a spec.** 444 of 504 frames of that reference have zero changed pixels; its whole motion budget is *when things appear*. If a page's character is staccato, the assertion is `document.getAnimations()` empty and rects bit-identical between events — not an easing curve.
- **A stylesheet that fails to parse does not error — it recovers, and recovery eats the next block.**
  One `*/` written inside a banner comment closed it early and the parser consumed the following
  `:root{}` as that garbage rule's body: 23 tokens undefined, `background: var(--ground)` invalid at
  computed-value time, the whole `font:` shorthand dropped to Times 16px — and the page passed every
  check in `verify_case.py` (`cases/string-clock`, 踩过的坑 #1). Never write `*/` inside a comment;
  the floor now fails on any referenced-but-undefined custom property and on a transparent body.
- **A colour is not an `<image>`, so it takes the whole declaration down with it.**
  `background-image: <gradient>, #eae3d3` is invalid and drops in full — the ground simply never
  paints, with nothing logged. Colours belong in `background-color`, layered under the gradient.
- **A scripted edit that matches nothing reports success.** Two `str.replace` calls in one session
  silently changed no bytes because the pattern had drifted from the file. Assert the file actually
  changed after every scripted edit, or the next check is measuring the old page.
- **A percentage inside a transform resolves against the element's own box, never the container.**
  `translateY(-40%)` on a 64px numeral is 26px, not 40% of the dial — and a token used as *both* a
  width and a transform argument (`--dial: min(74vh, 100%, 760px)`) resolves differently in the two
  places, so it can be correct at one breakpoint and wrong at another from one declaration.
- **A discrete control is driven by committing a state, not by an impulse.** A wheel notch on a
  detented dial means "next slot", not "add velocity": a mouse reports `deltaY` 120 and a trackpad
  600+, and a spring pulling back the whole time makes the actual travel unpredictable. And never
  `preventDefault()` a wheel unconditionally — hand it back at the control's ends or the page cannot
  scroll.
- Do not let motion hide weak hierarchy, unreadable text, or missing content.
- **The still frame is half the deliverable.** Screenshot with motion disabled and be willing to defend
  that frame on its own. "不好看 / 像 AI 做的" is almost never a motion-tuning problem — going to the
  springs first is the documented wrong move (`design-slop.md`).
- **Design the page before the mechanic goes into it.** Macrostructure, type scale and palette are an
  act with their own output, not a clause inside the build step. Placing a mechanic into a page that
  already works is the opposite order from decorating a template, and it is the order that works.
- Extract real motion values when possible: trigger, duration, easing, stagger, transform, media, library, reduced-motion behavior.
- Treat X posts, videos, and screenshots as topic information only until the real page is inspected (Video Reference Protocol).
- Light 3D belongs here only when it is part of a web page: hero scenes, product staging, shader planes, scroll cameras, spatial cards, or WebGL-lite atmosphere.
- **A shader is required only when the picture has to change at runtime.** If the viewer only moves
  *through* the picture, a whole scene can be unlit `MeshBasicMaterial` planes — SBS *The Boat* ships
  zero `ShaderMaterial`, zero custom blending, zero `renderOrder` across 117 app modules
  (`image-plane-3d.md` §14). Decide which one you are building before writing the first material.
- **Depth does not require geometry.** A `PerspectiveCamera` doesn't care whether the thing at `(x,y,z)` is a
  mesh or a textured plane — it foreshortens, occludes, sorts and projects either way. Before proposing models,
  ask what actually has to *rotate*; if the answer is "nothing, the camera just moves", the whole scene can be
  flat images (`references/image-plane-3d.md`). What separates it from collage is measurement, not art.
- Full 3D scenes, game-like environments, generated models, physics-heavy scenes, and material/light pipelines → route to `3d-scene-studio` — after ruling out rung 5.
- Use `MOTION_SPEC.md` as the build contract for complex builds. Skip it for quick freeform builds.
- Implementation is not done until desktop, mobile, reduced-motion, performance, and build/type-check are verified.
- **R3F & DOM Sync**: If WebGL canvas is in background (`pointer-events: none`), `state.pointer` dies. Use global `window.addEventListener('pointermove')` for NDC coordinates.
- **Parallax vs Unproject**: If tracking DOM elements to WebGL meshes, `Vector3.unproject(camera)` will conflict with a moving Parallax camera. Unproject using a separate static dummy camera.
- **Scroll Morphing**: Do not use CSS `clip-path` on Canvas. Keep Canvas `100vw/100vh`, track transparent DOM placeholders via `getBoundingClientRect()`, and lerp mesh position/scale. Use Shader SDFs for rounded corners instead of real geometry.

---

## Data

- `data/visual-bank.json` — the static-first visual design library: 7 palette archetypes, 5 typography
  systems, 5 layout grids, each with concrete values (`clamp()` scales, letter-spacing, grid CSS).
  `page-design.md` and `design-slop.md` A4 point here. Pick one archetype and commit; do not blend two.
- The measured numbers quoted in `components.md` §1, `page-blueprints.md`, `production-polish.md` and
  `page-design.md` §2 come from a 2026-08 headless run over 32 sites (18 award-winning creative, 14
  product-marketing) with `scripts/measure_structure.py` at 1440×900 and 390×844. The summaries live in
  those files; the per-site records are not part of this release. Re-run the script on a fresh set of
  URLs when you need a current baseline.

---

## Cases

`cases/` ships **working, verified source** — unlike a technical-breakdown-only library, the whole page
is there and it runs. That makes one rule load-bearing:

> **机制层照搬，皮层一律不许照搬。**
> The **mechanism** — solvers, math, guards, probe surfaces, the `@supports` authoring order — is
> engineering, not an aesthetic signature. Lift it verbatim; re-deriving a homography by hand is waste.
> The **skin** — palette, type values, grid, section order, copy, the invented brand — is the case's
> own identity. Reusing it produces a page that is recognisably this case wearing a different logo,
> which is the exact template behaviour the rest of this skill exists to prevent.

Each case's `index.html` marks the boundary in a comment banner, and its `README.md` has the split as
two explicit lists (可以照搬 / 不许照搬) plus the reasoning behind every skin decision — **that**
reasoning is what transfers, not the values.

| Case | Teaches | Stack |
|---|---|---|
| `cases/string-clock/` | **soft body, exact endpoint** — clock hands as slack elastic strings pinned at both ends, a stiff tip spring so the readout stays true while the stroke lies, `Rods` shipped as the degenerate case, and the dialect finding (product controls on a creative canvas) | single HTML file, rAF |
| `cases/ink-crowd/` | **the ink render layer** — hand-written WebGL2 (no framework, no CDN): 620 instanced capsules into an MRT + depth target, then a fullscreen pass that draws the line from **depth discontinuity only** (interior creases off). Two noises, one static per figure and one on an **11 Hz boil clock** against a 60 fps render. Shadow disc and void are the same primitive. Binary palette, inlined variable font | single HTML file, WebGL2, rAF |
| `cases/press-stack/` | **the sticky stack** — the opposite answer to `wheel-rail`: native scroll left alone, nine screens each `position:sticky;top:0;height:100vh` so the next rides over the last. Progress is read back out of the document (`(scrollY - offsetTop) / innerHeight`), not accumulated. Type wipe lights words `0.22 → 1` in reading order. Every sleeve and record is **drawn on a canvas**, no bitmaps | single HTML file, DOM + Canvas 2D, rAF |
| `cases/wheel-rail/` | **input-driven choreography** — nothing plays on a timer. `wheel` is hijacked `{passive:false}` and eased into a translated rail (`window.scrollY` stays 0); the pointer drives three planes at a 7× depth ratio; labelled nodes are pinned to their curves by `getPointAtLength`; act 4's curve field is parked by hand because `position:sticky` cannot fire inside a transformed ancestor | single HTML file, DOM + inline SVG, rAF |
| `cases/toy-flipbook/` | **rotation in depth without a renderer** — four curated pre-rendered yaw frames, hard-cut by `Math.round` of a spring with no transition anywhere, on a **held 11 Hz jitter clock** against a 60 fps render. One normalised driver feeds every layer its own gain, including opposite signs on the two lines of a single headline | single HTML file, rAF |
| `cases/char-curtain/` | **a cloth that is a set of strings, not a mesh** — 576 glyphs on 24 Verlet columns with **zero horizontal links**, which is the only reason a pointer parts it instead of denting it. Sprung anchors rather than pinned ones, bouncing by reflecting `oldX`, and speed mapped to colour *and* alpha so a still frame shows where the ripple is | single HTML file, Canvas 2D, rAF |
| `cases/lyre-crows/` | **a causal ecology instead of a timeline** — strum a string, a word is released, a steering crow hunts it down and **rewrites its own tail with what it caught**. Rate limiting at the source and unconditional decay on the product are what keep the loop from becoming noise; steering clamps the *force*, not the velocity, which is what gives a turn a radius | single HTML file, Canvas 2D, rAF |

Every case passes the same acceptance floor and prints it in its README: no console errors, zero
horizontal overflow at 320/375/414/768/1440, one `<h1>`, `lang` set, display ÷ body ≥ 4×, ≥ 3 distinct
section shapes, **no referenced custom property left undefined**, a body that paints its own ground,
and **nothing stuck hidden under reduced-motion**. The single-screen hero (`toy-flipbook`) runs with
`--min-shapes 1`, which is an exemption for a hero demo and **not** for anything that is
actually a page. Each case adds a domain oracle. `--beats` and `--detent` are kept without a
case: both need the page to expose their probe contract, so they are patterns to build
against, not checks you can point at an arbitrary page:

| Flag | Asserts | Used by |
|---|---|---|
| `--beats` | sweeps the scroll axis, normalises each track by its own range, and reports the **longest run where no track moved** — the operational definition of a dead beat | no case — needs `__probe.seek/tracks` |
| `--detent` | released at 36 positions, a snapping control lands ≤ 0.02° off a slot, settles, reaches every slot, and clamps at both ends | no case — needs the detent probe |
| `--strings` | two assertions that **pull against each other**: every hand's tip is ≤ 1.5° off the true angle, *and* every hand still sags ≥ 1.12× its chord — plus a **real-pointer** fling at 12/60/240 px per step that may not stretch past 3.2× or leave the box, and a **free-running** pass with the clock unpinned | string-clock |
| `--stack` | the sticky contract: every screen must pin at `top: 0` **while `window.scrollY` keeps advancing** (the inverse of `--rail`, which requires it to stay at 0), ≥3 distinct grounds, and a type wipe that both **shows a gradient** at some moment and **never drops below 0.12** — a page that lights everything at once passes the second test, a page that fades from zero passes the first, and only the reference's device passes both. Also fails any element that pulls a bitmap | press-stack |
| `--rail` | **element churn, idle liveness, plus** the wheel hijack: with the mouse completely still for 1.5 s at least 2 elements must still be changing, because a page whose every motion waits for input is a still image until someone touches it. Then: across a real eight-burst wheel run at least 35 % of elements must change `transform`, `opacity` or `stroke-dashoffset`, and at least 4 must be caught **part-way** through a transition. The first assertion catches a rail that translates while every child holds still; the second catches states that snap. Also, as before, the wheel is hijacked and the pointer carries depth: a real wheel must move a rail while `window.scrollY` stays 0 **and the wheel event is cancelled** (`overflow:hidden` pins `scrollY` on its own but still overscrolls), the rail must be measurably behind target one frame later and settled a second later, and a corner-to-corner pointer sweep must move the far plane at least 1.5× the near one | wheel-rail |
| `--layer <dom\|svg\|canvas2d\|webgl>` | asserts the render layer the README declares, by probing live canvas contexts and inline SVG shape counts rather than trusting the prose — a case claiming `webgl` while shipping divs fails. Implies the **web-font gate**: 0 `@font-face` and no font preload is a fail, because the system stack is the generated-page tell no other gate catches (`--draws-own-type` for a page that draws its own letterforms) | ink-crowd |
| `--follow` | pointer-led motion: aims at five points across the canvas — including bare ground — and requires the crowd **centroid to close on the aim from every one of them**. A follow counter that ticks is not evidence anything walked; a mechanic that works in one band and is deaf everywhere else passes every other check | ink-crowd |
| `--flipbook` | two assertions that **pull against each other**: across a 60-sample real pointer sweep every frame is either fully lit or fully off (a crossfade fails this) *and* the sweep visits every frame in order without skipping (a control that snaps to the end pose fails this). Plus: the jitter re-rolls between 4 and 25 Hz, and a wheel spin past the kick threshold both lifts desk toys off the table and squashes them on landing — **the leg prints its peak drive and fails if it never cleared the threshold**, so an untriggered test cannot pass silently | toy-flipbook |
| `--curtain` | two assertions that **pull against each other**: a real pointer sweep must move the median column ≥ 6px sideways, *and* poking one column must leave the far side of the cloth moving < 20 % as much. A dead cloth fails the first; a sheet with horizontal links passes the first and fails the second. Plus: no link deviates > 35 % from rest length, and every anchor returns within 2px of its peg. **The baseline is polled until the cloth is measurably still rather than waited out** — see the lesson above | char-curtain |
| `--lyre` | two assertions that **pull against each other**: fourteen real strum sweeps must release words, *and* the count aloft must never exceed the page's stated cap while being abused. A decorative instrument passes the cap; an unlimited emitter floods (the broken copy reached 440). Plus: with prey aloft a crow must enter a hunting state and close ≥ 30 % of its gap, and a counted capture must **change that crow's tail** and leave the caught word in it | lyre-crows |

A new case is not a case until `verify_case.py` passes on it.

**Building one — read [cases/AUTHORING.md](./cases/AUTHORING.md) first.** It is the procedure for
参考 → 复刻 → 收录: the intake gate (does the reference survive having its images stripped?), the
measurement scripts, the four classification decisions, the build rules, the oracle, and what a
README owes — 设计系统 + 动效系统 + 判据 + 可照搬/不许照搬 + 踩过的坑.

**Read a case when**: the user's brief is in its class, you need the mechanism, or you want a worked
example of a doc's rules actually applied. **Do not** open one to "start from" — start from
`page-blueprints.md` and pull the mechanism in.

---

## Reference Files

| File | Contains |
|---|---|
| `references/choreography-arc.md` | 5 page-level arc types with motion tokens |
| `references/motion-tokens.md` | **Duration scale, easing dictionary, spring config cheatsheet, stagger patterns, transform budget** |
| `references/pattern-recipes.md` | **ready-to-use motion pattern implementations (Vanilla + Framer + GSAP)** — count them, don't trust a number written here. Includes #17 corner-pin warp (真形变，不是 skew) and #18 the Verlet card chain built on it |
| `references/affordance.md` | **能点 ≠ 看得出能点：the invitation audit, window-vs-dwell, painted-bbox marks, down-records/up-decides, numeric oracles, the invisible handoff** |
| `references/handfeel.md` | **Interaction handfeel: underdamped springs, velocity tilt, wheel momentum guard, jelly wobble, fake lighting on flat images — plus §7 the *following* half (frame-rate-independent `exp(-k·dt)`, the `speed/k` steady-state lag and its lead term, why a correction after the filter hunts, acceleration-driven critical damping) and §8 screen shake** |
| `references/build-mode.md` | Implementation rules, performance rules, verification checklist |
| `references/page-design.md` | **动效页怎么设计：macrostructure 选择、给动效让位的版式、测量自当前获奖站的字号阶梯与配色规模、滚动叙事的分段、移动端降级** |
| `references/design-slop.md` | **动效页专属的 AI 味闸门：关掉动效看静帧、默认 hero、三栏特性卡、紫色渐变、装饰代替设计、统一 hover 抬升、全页 fade-up、首屏烧光预算** |
| `references/page-blueprints.md` | **这页到底放什么：the section vocabulary, 7 blueprints (product / portfolio / studio / campaign / editorial / index / docs), ordering logic, what each section owes in real copy, information architecture, and the measured section-count & shape-variety numbers** |
| `references/components.md` | **组件级 craft：the two measurably different component dialects (creative vs product — radius, shadow, uppercase, nav CTA, footer scale), the state matrix every component owes, and nav / hero / button / tag / card / media / form / accordion / dialog / index / proof / footer** |
| `references/project-setup.md` | **工程 0→1：the page stack ladder (one HTML file → Vite → Astro → Next), the three-level token layer + Tailwind v4 `@theme`, fluid type & space scales with the clamp() formula, font loading with metric overrides, `@layer` order, file layout, images, budget & deploy** |
| `references/production-polish.md` | **从能跑到成品：the full head block, OG images, 404, the states off the happy path, dark mode without a flash, the small "finished" details, machine-readable structure, analytics, and ten manual pre-ship checks** |
| `references/baseline-ui.md` | Accessibility and usability floor (focus, touch targets, hover-free mobile) — the *floor*, not the design |
| `references/motion-spec.md` | MOTION_SPEC.md template and entry field definitions |
| `references/composition-guide.md` | **How to orchestrate custom designs and motion without rigid templates** |
| `references/shaders-spec.md` | **WebGL GLSL shaders, simplex noise, rendering optimization — and §6 the silent failures: int-vs-float literals killing a program, missing tonemapping/colorspace includes, `DepthTexture` filtering, distance falloff for high-frequency detail, spatially-coherent instanced wind** |
| `references/tactile-texture.md` | **SVG viscous filters, CSS Houdini, OffscreenCanvas, and canvas grain patterns** |
| `references/image-asset-pipeline.md` | **图片资产怎么造出来：keying against the image's own background, the `coverage` gate, bbox crop, line-art alpha, scripted `cx/baseline`, the crown anchor nobody records, per-element resolution budget, texture density vs serving distance, provenance** |
| `references/scene-streaming.md` | **大场景怎么装得下：screen-window activation, cooperative scanning, throttled DOM mutation, full disposal, sliced texture upload, audio streamed by audibility** |
| `references/verification-harness.md` | **判据台架：the probe contract (`__seek`/`__hold`/pinnable clocks/state exits), on-off differencing, why teleport and screen-diff lie, determinism as a precondition, sampling rate, the ruler's resolution floor — and why a composite quality score is worse than no test** |
| `references/timeline-orchestration.md` | **多轨滚动时间轴：read the schedule horizontally, one easing layer, weight by what the eye reads, one window one event, velocity-zero keyframes, the apparatus outliving its content, the money frame, threshold-map histograms** |
| `references/scene-audio.md` | **场景声音：three buses (bgm/hand/world), per-act LUFS curves, ducking, discrete events over a louder bed, why a continuous quantity reads as ambience, the REST oracle, filters eating 20 dB** |
| `references/image-plane-3d.md` | **图片资产做出真纵深：flat cutouts as planes in a real perspective camera — asset metadata contract, long lens, silhouette interlock, hand-sorted transparency, analytic contact shadows, the colour-temperature cure for 「拼接感」** |
| `references/light-3d.md` | Three.js/R3F/canvas integration rules + DOM-over-a-moving-scene |

---

## Scripts

```bash
# ── MEASURE STRUCTURE (the static-page half: sections, components, tokens, polish) ─
# Answers "how is it built as a page": sections, nav, buttons, token scales, forms, media, meta, mobile overflow.
python3 scripts/measure_structure.py https://example.com
python3 scripts/measure_structure.py --urls-file urls.txt --out data/structure-bank.json
# Skips URLs already present in the out file, so a killed run resumes.

# ── DECONSTRUCT A VIDEO REFERENCE (no URL to open) ────────────────────────────
# measure_structure needs a loadable page. A clip has none.
python3 scripts/measure_frames.py sheet   ref.mp4        # contact sheet — ALWAYS look first
python3 scripts/measure_frames.py palette ref.mp4 -t 8   # ground %, accents, mid-grey scale
python3 scripts/measure_frames.py bands   ref.mp4 -t 8   # control heights/widths off the pixels
python3 scripts/measure_frames.py trace   ref.mp4 --color red   # arc/chord per frame
python3 scripts/measure_frames.py grounds ref.mp4               # section changes + which way the new screen arrives
python3 scripts/measure_frames.py wipe    ref.mp4 --from 7.9 --to 10.1 --dark
#   ^ the schedule of a per-word reveal, and the one number a still frame cannot give
#     you: whether unlit type is hidden (0.00) or merely dimmed (side-b: 0.22).

# ── VERIFY A CASE / ANY BUILT PAGE ────────────────────────────────────────────
# The acceptance floor every case's README claims. Re-runnable, so the claim can't rot.
python3 scripts/verify_case.py cases/string-clock/index.html --strings  # exact tip, sagging body
python3 scripts/verify_case.py cases/ink-crowd/index.html    --layer webgl --follow  # declared layer + pointer-led crowd
python3 scripts/verify_case.py cases/wheel-rail/index.html   --rail   # hijacked wheel + depth + churn
python3 scripts/verify_case.py cases/press-stack/index.html  --stack  # sticky dwell + type wipe + drawn art
python3 scripts/verify_case.py cases/toy-flipbook/index.html --min-shapes 1 --flipbook  # hard cut AND continuous scrub
python3 scripts/verify_case.py cases/char-curtain/index.html  --min-shapes 1 --curtain   # parts AND stays independent
python3 scripts/verify_case.py cases/lyre-crows/index.html    --min-shapes 1 --lyre      # releases AND stays limited
python3 scripts/verify_case.py http://localhost:5173                   # works on a dev server too

# ── DOES ANYTHING ACTUALLY MOVE? ──────────────────────────────────────────────
# The check that caught what every oracle above missed twice: a page with all the
# right mechanisms that reads as dead. Drives a REAL wheel; scrollTo teleports
# past the arriving-and-leaving window where the motion lives.
python3 scripts/measure_churn.py https://a-reference.com         # characterise it first
python3 scripts/measure_churn.py cases/foo/index.html --against https://a-reference.com

# ── SHIP REAL TYPE, NOT THE SYSTEM STACK ──────────────────────────────────────
# 0 @font-face is the loudest generated-page tell (render-layer.md §2).
python3 scripts/subset_fonts.py list
python3 scripts/subset_fonts.py pack --out /tmp/faces.css \
    Grot=Inter-Variable Ital=InstrumentSerif-Italic Mono=IBMPlexMono-Regular
```

**Self-check** (run after editing `scripts/` or any case, or when the user asks to 体检 this skill):

```bash
cd ~/.claude/skills/motion-web
python3 -c "import json;json.load(open('data/visual-bank.json'))" && echo "json OK"
python3 -m py_compile scripts/*.py && echo "syntax OK"
# then the seven verify_case.py lines above — every one must print VERDICT: PASS
```

**zsh does not split variables.** `flags="--layer webgl"; verify "$f" $flags` passes the whole string
as one argument and argparse reports `unrecognized arguments`. Write the flags out, or use `${=flags}`.

---

## Output Contracts

**For spec work**: output a concise `MOTION_SPEC.md` from the template in `references/motion-spec.md`.

**For freeform build**: skip the spec. Build immediately. After completion, tell the user:
- The concept name and why you chose it
- The arc type and how it shapes the page rhythm
- The 3 most important motion decisions made
- What to verify (reduced-motion, mobile, FPS)

**For a `full-build`**: report the blueprint chosen and why, the page stack rung, the component dialect
(creative vs product), the motion concept, **every factual slot you had to invent, listed explicitly**, and
the results of `production-polish.md` §9 — which checks passed and which you could not run.

**For any build**: verify locally before reporting done. Run build/type-check if applicable. Report what changed, what was verified, and any remaining risk.
