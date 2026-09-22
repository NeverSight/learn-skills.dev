---
name: ohos-req-review-ppt-gen
description: Use when converting an OpenHarmony requirement document, spec, or design proposal into an OpenHarmony review slide deck (需求评审 / 需求变更评审 / 设计评审 PPTX) — produces the fixed OpenHarmony-branded review-deck structure (OH logo on every page) with architecture/flow diagrams and field tables. Triggers on "需求评审PPT", "需求变更评审", "把需求文档转成评审PPT", "spec转评审PPT", "requirement/spec to review deck". NOT for arbitrary or generic slide decks unrelated to OpenHarmony requirement/design review.
metadata:
  author: openharmony
  scope: common
  stage: requirements
  domain: review
  capability: ppt-gen
  version: 0.1.0
  status: trial
  tags:
    - pptx
    - requirement-review
    - deck-generation
---

# OpenHarmony Requirement-Review PPTX Deck Generation

## Overview

Build clean, consistent 16:9 PowerPoint decks by calling a ready-made helper
library — **you supply only content; the library owns all coordinates, colors,
fonts, spacing, and arrow-drawing.**

**Core principle:** Never compute slide geometry or restyle shapes by hand.
Import `deckbuilder.Deck` and call its slide methods. Building raw `python-pptx`
shapes from scratch is the #1 cause of broken layouts, overlapping boxes,
text-only "diagrams", and wrong imports. Don't do it.

## Fastest path — 需求评审 in ONE call (start here)

If the task is an OpenHarmony **需求变更评审 / 需求评审** deck (the common case),
do NOT hand-assemble slides and do NOT choose builders yourself. Fill one plain
`spec` dict and make a single call — the library owns the page order, which builder
each page uses, and every fixed table shape (5 影响对象 rows, 8 风险 rows, 11 交付
columns). This is the most reliable path and removes the top mistake (picking the
wrong builder, e.g. four cards for the 价值 page).

```python
from deckbuilder import Deck
Deck().requirement_review_deck(spec).save("requirement_change_review.pptx")
```

- **Copy `examples/requirement_review_oneshot.py`**, replace the `<placeholders>`,
  keep the structure, run it. That's the whole job.
- Every field is optional — anything you leave out renders as **待评估 / TBD**, never
  fabricated. List those TBD fields back to the user.
- `spec["design"]` may be one dict (one 设计方案 page) or a list of dicts (multiple,
  auto-paged). `spec["delivery"]["items"]` is one row per 子需求; the 合计 row is
  summed for you.
- The 8 fixed pages, in order: 封面 · 需求价值描述 · 需求设计方案 · 需求变更背景 ·
  需求变更影响性分析 · 版本交付计划 · 兼容性分析 · 风险评估.

The full `spec` shape is documented in the `requirement_review_deck` docstring and in
`examples/requirement_review_oneshot.py`. Everything below is the **manual / advanced
mode** — the individual builders, for non-review decks or one-off custom pages.

### Page → builder map (do not deviate)

For 需求评审 pages, each page has exactly ONE correct builder. Never use
`content_slide` / `banded_slide` for the 价值 or 设计 pages — that produces the
"four boxes" / rainbow-bars result. (The library will `warnings.warn` if you do.)

| Page | Builder | Never use |
|------|---------|-----------|
| 需求价值描述 | `value_slide` (左文右图) | ❌ `content_slide` (四格) |
| 需求设计方案 | `design_slide` + `diagram=` (左文右图+框图) | ❌ `content_slide` / bullet list |
| 需求变更背景 / 影响性分析 / 兼容性 / 风险 | `table_slide` | ❌ `banded_slide` (彩色横条) |
| 版本交付计划 | `table_slide` (11 列) | ❌ 手写列宽/字号 |


## When to Use

- Converting an OpenHarmony **requirement document / spec / design proposal** into a
  review deck — this is the primary trigger
- **需求评审 / 需求变更评审 / 设计评审** decks (OH-branded, fixed structure)
- Feature-proposal decks that follow the OH review flow
- Such decks needing an **architecture / data-flow diagram** (real boxes + arrows)
  or comparison / breakdown **tables**

When NOT to use: **generic or non-OpenHarmony slide decks** (this skill always
stamps the OpenHarmony logo and imposes the OH review structure — it is not a
general-purpose PPT maker); editing an existing `.pptx` the user already has (open it
with `python-pptx` directly); or when the user wants Markdown/PDF instead.

## Setup (do this first)

```bash
python3 -c "import pptx" 2>/dev/null || pip install python-pptx
```

The library file `deckbuilder.py` lives in this skill's **`scripts/`** directory,
alongside `oh_logo.png` (the OpenHarmony logo). Copy **both** (keep them together)
next to your build script, or add the `scripts/` dir to `sys.path` —
`deckbuilder.py` auto-finds the logo in its own directory, so the two files must
stay side by side. Then write ONE script that imports it and calls slide methods in
order, e.g.:

```python
import os, sys
sys.path.insert(0, os.path.join("<skill-dir>", "scripts"))
from deckbuilder import Deck
```

### Visual style (built in — do not re-implement)

The library renders a **light theme with a red accent** ("red ink"): titles are
**near-black ink** (subdued, not a loud color), a single **red** accent carries each
page's **conclusion** and primary path, structure is **soft neutral grey**, **blue**
is used for value-page body text and table headers, and **amber** is reserved for
change points. Every choice below is automatic, you never set colors or coordinates:

- **The conclusion is the highlight, not the title.** Each page's 32pt title is calm
  near-black ink (`primary`); the eye is drawn instead to the `takeaway` conclusion
  line, rendered in **red** (`accent`) right under the title. The red accent also draws
  the title underline and primary data-flow arrows.
  **Everything else — secondary arrows, grid, connector bars, box borders — is soft
  grey** (`grey`). **Do NOT give cards/sections different accent colors** — that
  produces a rainbow ("不纯粹") deck. Leave `accent` unset (defaults to red).
- **Reserve hue changes for real meaning only:** `red` (a muted brick-red) for an
  actual risk/blocker; the built-in `★变更` change box (a light-amber fill with an
  amber badge, drawn for you when you pass `"change": True`). `green` (the logo
  green) exists but is rarely needed — don't sprinkle colors to "add color".
- **Cover & headers.** Cover has a thin red spine; each content page is a 32pt
  Microsoft YaHei **ink** title on white with a thin red underline and the page
  number top-right.
- **OpenHarmony logo, bottom-left of every page** (cover included) — added
  automatically from `oh_logo.png`. If the file is missing it's silently skipped.
- **Diagrams are real drawing boxes** — rounded rectangles joined by arrows.
- **Tables** — **slate-blue header** (`C6D7EC`) with black bold text, white body, and
  **black solid grid lines**; fonts follow the value/design page standard (header
  **15pt bold**, body **13.5pt**). Light-red total row when `highlight_last=True`.
  All drawn for you.

## The Only API You Need

```python
from deckbuilder import Deck

deck = Deck()                    # 16:9; font defaults to "Microsoft YaHei"

# ── EASIEST: whole 需求评审 deck in one call (see "Fastest path" above) ──
deck.requirement_review_deck(spec)   # spec = dict; fixed 8-page 需求变更评审

# ── or assemble pages manually (advanced / non-review decks) ──
# NOTE: every content slide below REQUIRES takeaway="结论：…" (the page's one-line
# conclusion) — pass it as a keyword. Omitting it raises ValueError. Only cover()
# takes no takeaway.
deck.cover(title, subtitle=None, meta_lines=[...])
deck.content_slide(title, cards, takeaway="结论：…", subtitle=None)
deck.banded_slide(title, sections, takeaway="结论：…", subtitle=None)
deck.bullets_slide(title, bullets, takeaway="结论：…", subtitle=None)
deck.table_slide(title, headers, rows, takeaway="结论：…", col_widths=None, highlight_last=False)
deck.flow_slide(title, stages, takeaway="结论：…", note=None, lane_label=None)
deck.layered_diagram_slide(title, layers, takeaway="结论：…", connect=None, note=None)
deck.architecture_slide(title, nodes, edges, takeaway="结论：…", note=None)
# Two-column pages (左文右图) — title is 28pt bold YaHei; takeaway is OPTIONAL here:
deck.value_slide(title="需求价值描述", background=[...], features=[...], scope=[...], image=None)
deck.design_slide(title="需求设计方案", design=[...], changes=[...], extra=None, image=None)
deck.save("output.pptx")
```

**Every page leads with its conclusion — `takeaway` is REQUIRED.** Pass
`takeaway="结论：…"` (one short sentence) to every content slide — it renders as a bold
red line with a red kicker right under the (subdued ink) title, so the
reviewer's eye lands on the point before the detail.
The title stays the topic label (`五、兼容性分析`); the `takeaway` carries the verdict
(`不改变公开 API 行为，应用无需适配`). Write an assertion, not a restatement of the
title. `subtitle` (small grey) still exists for neutral scope notes; if both are
given, `takeaway` wins the slot. **`takeaway` is mandatory: a content slide built
without it raises `ValueError` and the deck will not save.** There is no way to ship a
page without its 突出重点 — write the one-line verdict for every slide.

Page numbers auto-increment (cover is excluded). Header band, accent colors, and
spacing are automatic. **Colors are passed by name string** — `"accent"` (red)
and `"grey"` (soft grey) cover almost everything; `"red"` for a genuine risk;
`"green"`, `"orange"`, `"primary"` exist but are rarely the right call. **Default to
omitting `accent` (or using `"accent"`)** so the deck stays one coordinated family —
don't vary it per card just to add color.

### Quick reference — what each method takes

| Method | Key argument shape |
|--------|--------------------|
| `requirement_review_deck` | `spec={...}` — whole 8-page 需求变更评审 in one call. **Preferred for review decks.** Missing fields → 待评估/TBD. See `examples/requirement_review_oneshot.py` |
| `cover` | strings + `meta_lines=["Team", "2026-06-23"]` |
| `content_slide` | `cards=[{"title","bullets":[...]}]` (1–6 auto-grid). **Per-card `accent` is ignored — all cards render in one family** (no rainbow). For 需求变更评审 4–7 use `table_slide`, not this |
| `banded_slide` | same `sections=[{"title","bullets"}]` shape, rendered as full-width horizontal bars stacked top→bottom. **Per-section `accent` is ignored — all bars are one color.** Avoid for 需求变更评审 4–7 (use `table_slide`); the colored 横条 it used to make were the #1 "不纯粹" complaint |
| `bullets_slide` | `bullets=["text", {"text","level":1,"accent","bold"}]` |
| `table_slide` | `headers=[...]`, `rows=[[...],[...]]`, `highlight_last=True` for totals. `col_widths` are relative weights — auto-scaled to fit, never overflow |
| `flow_slide` | `stages=[{"title","lines":[...],"change":True}]` → 1 row, auto arrows |
| `layered_diagram_slide` | `layers=[{"label","nodes":[{"title","lines","change"}]}]` + optional `connect` |
| `architecture_slide` | `nodes=[{"id","title","lines","row","col","change"}]`, `edges=[{"from","to","label","dir":"f"/"both","accent"}]` — labeled directional connectors for high-level module interaction |
| `value_slide` | `background=[...]`, `features=[...]`, `scope=[...]`, `image=None`. Two-column 需求价值描述 page (see below). `takeaway` optional |
| `design_slide` | `design=[...]`, `changes=[...]`, `extra=[{"heading","lines"}]`, `image=None`. Two-column 需求设计方案 page (see below). `takeaway` optional |

## 需求价值描述 / 需求设计方案 — the two-column pages (左文右图)

Two dedicated builders for the standard 需求评审 value + design pages. **Title is
Microsoft YaHei, bold, 28pt** (auto-shrinks only if absurdly long). Left column =
stacked sections; **right column = a scene/architecture image** (pass `image=`) or,
if omitted, a labeled placeholder card telling the user where to paste one.
Typography is fixed and built in — section heading **15pt bold**, body **13.5pt,
not bold**. `takeaway=` is OPTIONAL on these two pages (they lead with their sections,
not a one-line verdict).

### `value_slide` — 需求价值描述 (3 sections)

```python
deck.value_slide(
    title="需求价值描述",
    background=["…"],   # 段一「背景」    — body BLUE 13.5pt
    features=["…"],     # 段二「特性及价值点」— body BLUE 13.5pt
    scope=["…"],        # 段三「需求收益（影响）范围」— body BLUE 13.5pt
    image="scene.png",  # 右侧场景图（可选，缺省显示占位卡）
)
```

- **段一「背景」** — 蓝色正文。需求由来 / 现状问题。
- **段二「特性及价值点」** — 蓝色正文。**明确需求价值所在**，参考：用户痛点、需求功能点、
  范围、用户场景、所带来的价值。toD 内容需明确**开发者适用范围**、明确**开发者完成后达成的
  结果**；能力提升需求不能脱离业务（除能力目标外，需能力提供后的**业务目标**、**能力开放范围**）；
  **可量化目标**：用户活跃数、好评率、新增用户留存等；**产品范围**：1+8+N 涉及的产品。
- **段三「需求收益（影响）范围」** — 蓝色正文。描述特性的**使用范围、地区、具体产品**，
  **重点关注特性通用性**，不允许仅为单个产品做特性（硬件依赖除外）。
- **右半部分贴场景图**展示该特性的价值。

### `design_slide` — 需求设计方案 (左文右图，可多页)

```python
deck.design_slide(
    title="需求设计方案",
    design=["…"],    # 1、设计方案：设计重点（交互模块及如何达成需求的规格等）
    changes=["…"],   # 2、变更点及影响（见下）
    extra=[{"heading": "三、UI 示意", "lines": ["…"]},
           {"heading": "四、裁剪说明", "lines": ["…"]}],   # 可选追加段落
    image="arch.png",   # 右侧架构图（可选）
)
```

- **1、设计方案** — 输出设计方案设计重点，如交互模块及如何达成需求的规格等。
- **2、体现变更点及影响** — 包括但不限于：数据结构变更、外部接口变更、外部依赖分析、
  性能功耗评估、影响用户体验的关键 KPI 等。
- **设计方案可以有多种，可多页输出** —— 每个方案各调用一次 `design_slide`（自动翻页）。
- **如涉及 UI，需具体示意图** —— 把示意图作为 `image=` 贴在右侧，或在 `extra` 里加「UI 示意」段。
- **如裁剪已上线需求，需需求方意见** —— 在 `extra` 里加一段说明。
- **右边可贴架构图补充展示**（`image=`）。

## Architecture diagrams (the part models get wrong)

A design/system slide MUST be a real diagram — boxes connected by arrows — not a
bullet list. Three builders, all auto-layout and auto-draw arrows. Pick by intent:

- **`flow_slide`** — one left-to-right pipeline (data flow through stages).
- **`layered_diagram_slide`** — stacked planes (e.g. control plane over data plane).
- **`architecture_slide`** — **high-level module interaction**: how a subsystem
  touches its peers. Use this for the "系统级架构 / 对 OpenHarmony 整体影响" slide.
  Labeled, directional connectors say WHAT each link is and WHICH way it flows —
  far clearer than uniform arrows. See the requirement-review template for the
  canonical OH-module example.

**Simple pipeline** — one left-to-right flow. Mark changed components with
`"change": True` (renders a light-amber box with an amber `★变更` badge + border):

```python
deck.flow_slide("System Design — Data Flow", [
    {"title": "HID device",   "lines": ["USB / BT"]},
    {"title": "normalize",    "lines": ["resolve binding"], "change": True},
    {"title": "windows mgr",  "lines": ["hit test, isolate state"], "change": True},
    {"title": "UDS dispatch",  "lines": ["consistent ids"]},
], takeaway="结论：变更集中在 normalize 与窗口命中两处",
   note=["normalize resolves the binding before coordinate calc.",
         "Light-amber ★变更 boxes are the change points."])
```

**Layered diagram** — stacked planes (e.g. control plane over data plane). Each
layer is a row; `connect` draws vertical arrows between nodes by `[layer, node]`
index:

```python
deck.layered_diagram_slide("System Design — Framework", [
    {"label": "control", "nodes": [
        {"title": "Service (SA)", "lines": ["bind request"]},
        {"title": "BindHelper",   "lines": ["runtime state", "inner API"], "change": True}]},
    {"label": "data", "nodes": [
        {"title": "device",    "lines": ["event"]},
        {"title": "normalize", "lines": ["resolve"], "change": True},
        {"title": "dispatch",  "lines": ["consistent"]}]},
], connect=[[[0, 1], [1, 1]]],   # BindHelper → normalize (down arrow)
   takeaway="结论：BindHelper 变更下沉到 normalize 阶段",
   note="Helper feeds the normalize stage.")
```

## Requirement-CHANGE-review decks (需求变更评审) — use the fixed template

**Prefer the one-call path (`deck.requirement_review_deck(spec)` — see "Fastest path"
at the top).** It builds this exact 8-page structure for you, so you can skip the
manual builder choices below. The rest of this section documents what each page
contains — useful for filling the `spec`, or for building pages by hand when you need
a variation.

When the user asks for a 需求变更评审 / requirement-change-review deck, or gives a
page-by-page brief (需求价值 → 需求设计方案 → 需求变更背景 → 需求变更影响性分析 →
版本交付计划 → 兼容性分析 → 风险评估), **follow the 8-page structure** in
[requirement-review-template.md](references/requirement-review-template.md) instead of inventing
an outline. `examples/requirement_review_example.py` is a complete, generic fill-in deck.

The fixed page order (cover counts as page 1):

1. **封面** — `cover`
2. **需求价值描述** — `value_slide` (左文右图, unchanged)
3. **需求设计方案** — `design_slide` (左文右图 + 右侧框图, unchanged; 可多页)
4. **需求变更背景** — `table_slide`: ① 需裁剪/变更的需求说明（原始需求/编号、特性概述与影响、使用场景，重点 2C/2D 价值与影响）；② 原始被接纳时的决策纪要（SIG 评审通过记录）
5. **需求变更影响性分析** — `table_slide`, **5 行**: 北向应用开发者／南向开发者／分布式设备／系统开发者（跨子系统依赖）／设备使用者
6. **版本交付计划** — `table_slide`, **11 列**横向计划表：承接领域／承接类型(IR/SR)／主要需求内容／落地版本／设计者／代码行数／是否涉及API／端到端工作量(500行≈1人月)／领域PM／管道是否满足／工作量是否由领域PM审核OK。**把需求拆解成多个子需求，一行一个、逐行呈现工作量**，末行用 `highlight_last=True` 合计
7. **兼容性分析** — `table_slide`: 是否涉及应用兼容性；兼容性包括（机制/权限/API行为/其它）；兼容性方案；应用适配方案和计划
8. **风险评估** — `table_slide`, **固定 2 列 8 行** checklist

What this page reliably gets wrong (the top two are the most-reported):

- **Pages 4–8 must be `table_slide`, never `banded_slide` / `content_slide`.** The
  bar/card builders tempt you to color each section differently → multi-colored 横条
  ("不纯粹"). Build them as field tables (页 4/5/7/8 两列 分项｜内容；页 6 为 11 列宽表).
  (The engine also forces those builders to one color now, but tables are the right
  layout here.)
- **Every `table_slide` page must pass `takeaway="结论：…"`** — a topic title over a
  table with no conclusion has no 突出重点. This is enforced: a slide without
  `takeaway` raises `ValueError`, so the deck will not build until every page has its
  verdict. (`value_slide` / `design_slide` take `takeaway` optionally.)
- **Keep pages 2–3 (价值/设计) as the two-column 左文右图 builders** — do NOT convert
  them to tables. Page 3's right column is a real **框图** (`diagram=` layers or
  `image=`), never a bullet list.
- **Page 5 has exactly 5 影响对象 rows, in order**: 北向应用开发者 → 南向开发者 →
  分布式设备 → 系统开发者（跨子系统/部件依赖）→ 设备使用者（性能/功耗/功能/体验）.
- **Page 6 版本交付计划 is a fixed 11-列 wide table** — 把需求拆解成多个子需求，一行一个、
  逐行呈现工作量，末行 `highlight_last=True` 合计；表头/正文字号随列数自动收缩，不要手设字号
  或写死列宽英寸；`col_widths` 传相对权重。
- **Page 8 is a fixed 2×8 checklist** — these 8 rows, in order: 对性能/功耗/RAM/ROM
  是否有影响；是否存在其他依赖关系；是否有安全风险；是否涉及合法/合规问题；是否涉及外部
  承诺；是否开源；是否涉及 AI；隐私风险特性识别. Answer each with 是/否/待评估 + 一句话。
- **Mark absent fields `待评估 / TBD`** (需求编号、SIG 决策纪要、落地版本、设计者、代码行数、
  端到端工作量、领域PM、适用地区/产品、外部承诺、合规/安全结论) and list them back to the
  user — never fabricate them.

## Workflow

1. Install python-pptx if missing; make `scripts/deckbuilder.py` importable (add the
   `scripts/` dir to `sys.path`, keeping `oh_logo.png` alongside it).
2. If the source is a spec/doc, read it and pull the real content per slide.
   Don't invent technical facts; if a number (e.g. effort) isn't given, label it
   an estimate or use `TBD`.
3. Write the build script:
   - **需求评审 deck →** copy `examples/requirement_review_oneshot.py`, fill `spec`,
     `deck.requirement_review_deck(spec)` → `deck.save()`. One call, done.
   - **Other decks →** `Deck()` → one method call per slide → `deck.save()`.
4. Wrap the build in `warnings.catch_warnings(record=True)` so any
   `table_slide` content-overflow warning is captured, not just printed and
   lost — see **Verification** below.
5. Run it. Then **verify** (next section). Report the output path + slide count.

## Verification before claiming done

Always run this after building — it confirms the file opens, no
`table_slide` overflowed its content, and nothing overflows the canvas:

```python
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    # ... build the deck here (or re-import/re-run the build script) ...
    table_warnings = [str(x.message) for x in w if "table" in str(x.message)]

from pptx import Presentation
p = Presentation("output.pptx"); W, H = p.slide_width, p.slide_height
bad = 0
for i, s in enumerate(p.slides):
    for sh in s.shapes:
        if sh.left is None: continue
        if sh.left < 0 or sh.top < 0 or sh.left+sh.width > W+2000 or sh.top+sh.height > H+2000:
            bad += 1; print("overflow on slide", i+1)
print("slides:", len(p.slides._sldIdLst), "overflow:", bad,
      "table warnings:", len(table_warnings))
# both overflow == 0 AND table_warnings == [] must hold
```

No renderer (LibreOffice) is needed; the bounds check is the smoke test. It
catches SHAPE-level overflow (a table/box positioned or sized past the
canvas edge). `table_slide()` now sizes each row to the actual measured
wrapped-text height of its cells (not a flat row-count average), and leaves
the table at its true (taller) height instead of force-compressing it when
content doesn't fit — so a table with genuinely too much text pushes its
shape past `BODY_BOTTOM` and IS caught by the check above, rather than
silently shrinking rows until text is visually clipped. If `table_slide()`
cannot fit the content even at its minimum font size, it also raises a
Python `UserWarning` naming the table — treat that warning as a build
failure and split the rows across multiple `table_slide()` calls or shorten
the cell text.

**`takeaway` is enforced — the build fails without it.** A content slide built
without `takeaway="结论：…"` raises `ValueError` naming the slide, so a deck that saves
successfully already has a conclusion on every page. If your script errors with
`slide '…' was built without takeaway=`, add the one-line verdict to that slide and
rerun — do not work around it.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hand-assembling a 需求评审 deck page by page (and picking a wrong builder) | Use `deck.requirement_review_deck(spec)` — one call, fixed 8 pages |
| 价值/设计页做成 `content_slide` 四格 / bullet 列表 | 用 `value_slide` / `design_slide`（左文右图；设计页右侧传 `diagram=`）— the library warns if you don't |
| Building shapes with raw `python-pptx` and hand-picked inches | Use `Deck` methods; they place everything for you |
| `from pptx.dgm...` / guessing import paths | The library already imports correctly — just `from deckbuilder import Deck` |
| Design slide is a bullet list, not a diagram | Use `flow_slide` or `layered_diagram_slide` |
| Passing `RGBColor(...)` everywhere | Pass color **names**; default to `"accent"`/`"grey"`, names map to the palette |
| Giving every card/section a different `accent` (rainbow 横条) | Don't — per-card/section colors are ignored by design; for 需求变更评审 4–7 use `table_slide` |
| Pages 4–8 as colored `banded_slide` bars | Use `table_slide` (分项｜内容 / 计划宽表) — the bars invite the "不纯粹" rainbow |
| Pages with no point — just a topic title over a table | Give every content slide a `takeaway="结论：…"` one-liner; it's required — a slide without it raises `ValueError` |
| Cramming 8+ cards on one slide | Max 6 per `content_slide`; split across slides |
| Putting >8 rows in one table at full font | The library auto-shrinks; still split very long tables |
| Claiming done without running it | Run the script + the overflow check, report path & slide count |

## Real-World Impact

This skill was distilled from building OpenHarmony 需求变更评审 decks (cover, 需求价值
描述, 需求设计方案, 需求变更背景, 需求变更影响性分析, 兼容性分析, 风险评估). The
两-column 价值/设计 pages carry a real 框图 on the right, and the change-review pages
(4–7) are clean 分项｜内容 field tables — both reproducible in a few lines via
`value_slide` / `design_slide` / `table_slide`.
