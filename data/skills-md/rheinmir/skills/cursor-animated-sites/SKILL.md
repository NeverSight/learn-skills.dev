---
name: cursor-animated-sites
description: Build an interactive "cursor-animated walkthrough" page on top of the /docs-site-macos glass theme — a narrow LEFT step-list + wide RIGHT animated folder-tree where an arrow cursor sits in the gutter at the start of each line and moves controller→file per step, files TYPE IN like a transcript exactly when they are created (absent before), nodes are colored BY ROLE (source/read vs dest/write vs pass vs verdict) with text tags, each step has its own accent, there is a manual "step" mode and an auto-play mode, and a caption under the frame narrates the current frame. Use for explaining install→runtime lifecycles, sequences, data-flow, or any "how it works, step by step" walkthrough where the viewer must SEE which file each action touches. Hooks /docs-site-macos for the base glass design system.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: cursor-animated-sites

Build a **single-file, self-contained HTML** walkthrough that animates a cursor over a folder
tree, step by step. It is a LAYER on top of **`/docs-site-macos`** — reuse that skill's glass
design system (background plane, glass tiers, scrollbar, fonts, ripple, output path
`llmwiki/html/DDMMYY-<slug>.html`, auto-host). This skill ADDS the interactive walkthrough.

> Inherit docs-site-macos's **Accessibility & Document Head** section too — `<meta viewport>` + `<title>`/`description`, inline favicon, `:focus-visible` ring on the ⏮/⏭/▶ controls, and the global `prefers-reduced-motion` guard (rule 11 already skips the walkthrough animation; the guard also stills the cursor/typewriter). Do NOT ship the page without viewport meta or its responsive grid breaks on mobile.

## WHAT

### Purpose và context
- **Purpose:** build a single-file, self-contained HTML walkthrough (layer on `/docs-site-macos`) where a gutter cursor moves controller→file step by step, files type in when created, nodes are colored by role, with manual step and auto-play modes and a per-frame caption.
- **Trigger (when to use):**
  - Explaining a **lifecycle** (install → configure → run), a **sequence**, or a **data-flow**.
  - Any "how does X work, step by step" where the viewer needs to SEE *which file each action reads/writes* and *in what order*.
  - Trigger words: "hoạt họa", "con trỏ chạy", "life cycle", "từng bước", "transcript", "minh hoạ cây thư mục", "/cursor-animated-sites".
- **Non-goals:** does not redefine the glass design system (background plane, glass tiers, scrollbar, fonts, ripple, output path, auto-host) — reuse `/docs-site-macos`; this skill only ADDS the interactive walkthrough.

### Mental model
`STEPS[] (ph · sp · h · d · flow · chain · role · marks · leak · verdict) + tree rows (data-born) → prep (accent per step, visibility by born) → animate (caption transcript = master clock, born rows type in, cursor visits chain in order, role colors + seq badges) → rest = full final frame`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | lifecycle/sequence to explain | có | real order of steps + which files each step reads/writes |
| In | folder tree (files + actors) | có | each file has a birth step |
| Out | `llmwiki/html/DDMMYY-<slug>.html` | có | single file, docs-site-macos base, auto-hosted |
| Out | draft output report + index + log | có | OKF YAML frontmatter |

### Rules và capabilities
Hard-won rules (distilled — do NOT relearn these). These are corrections from real use. Violating them makes the page confusing:
- RULE-01 (MUST): **Cursor lives in the LEFT GUTTER, never over content.** It is a small right-pointing arrow at `x = rowLeft − ~22px`, moving mostly vertically. A mouse-pointer glyph placed *on* the row covers the text and reads as clutter. → use `▶`-style arrow in the gutter. **Smooth motion:** `left` and `top` MUST share the same duration + easing (e.g. `.5s cubic-bezier(.45,.05,.2,1)`) — mismatched timings (e.g. left .32s, top .5s) make diagonal moves jerk because x lands before y. Add `will-change:left,top`.
- RULE-02 (MUST): **Number every visited node (inline seq badge).** When paused, the viewer must still read the order ①②③. A moving cursor alone is unreadable when frozen.
- RULE-03 (MUST): **Default at rest = the FULL final frame of the step, not the empty first frame.** On load show the complete frame (all nodes hit, caption full). Never show an empty "frame 0" with nothing on it.
- RULE-04 (MUST): **Files do not exist until created.** Before a file's "born" step it is `display:none` (absent from the tree — NOT faded/ghost). It appears (types in) exactly at the step that creates it. The tree fills up over time. Keep an explicit empty "before install" step so the empty state is actually visible.
- RULE-05 (MUST): **Appear like a TRANSCRIPT, not copy-paste pop.** New file rows reveal with a clip typewriter; the caption streams char-by-char. The transcript is the master clock — the frame advances *at the transcript's speed*, not a fixed timer.
- RULE-06 (MUST): **Go SLOW.** Reading speed beats motion. ~30ms/char, long dwell at end of frame. People give up if it rushes.
- RULE-07 (MUST): **Color by ROLE inside a step, not one color for everything.** The biggest confusion: copy-FROM (source) and copy-TO (dest) tinted the same → you can't tell direction. Source = blue "đọc", dest = teal "ghi/tạo", pass = grey, deny = red, ok = green, leak = amber. Put a **text tag** on the row too.
- RULE-08 (MUST): **Per-STEP accent goes on the LEFT list + caption chip only** (so steps are distinguishable in the list) — the RIGHT nodes use ROLE colors. Two color systems, two jobs; don't mix them on the same element.
- RULE-09 (MUST): **The caption under the frame must NOT duplicate the left bar.** Left = compact nav (label + title only). Right caption = the detailed description + flow for the current frame. Full duplication makes people dismiss both as redundant.
- RULE-10 (MUST): **Left column is narrow; the animation gets the space.** `grid-template-columns: minmax(190px,.5fr) 1.5fr`.
- RULE-11 (MUST): **Two modes:** "Tự bước" (⏭ plays one frame's transcript then STOPS) and "Tự chạy" (auto-advance, slow). Default = paused/manual. Respect `prefers-reduced-motion` (skip animation, show full frames).
- RULE-12 (MUST): **Captions = plain language, never jargon/caveman.** Each frame's caption (`d`) must read as full sentences for someone OUTSIDE the project. Expand every term on first use: a "hook" → "the move the runtime makes before each action"; "R1/R2" → the rule in actual words ("the rule that forbids writing to raw/"); "exit 2 / exit 0" → "code 2 = BLOCK / code 0 = PASS"; "assertion" → "a check that says the result must be X"; "layer=repo" → "the check that runs at commit/PR time, on the changed files". Say what is READ vs WRITTEN and WHY. A terse symbol caption like "PreToolUse → LÕI → R1 → exit 2" reads as cryptic and viewers skip it — write the sentence; let the short `flow` line carry the shorthand. (Longer `d` ⇒ lower the per-char type speed, ~18ms, so it doesn't drag.)
- Capabilities: read the `/docs-site-macos` skill; write one HTML file + draft/index/log; run a local HTML parse check and open the page via the auto-host server.

### Failure boundaries
- Page without viewport meta → responsive grid breaks on mobile: **failed**, do not ship.
- HTML parse check raises → **failed**, fix before hosting.
- A frame unreadable when paused (no seq badges, empty frame 0, caption duplicating the left bar) → **failed** against RULE-02/03/09, fix and re-click through.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | effect | docs-site-macos conventions | Generate base page | glass base at `llmwiki/html/DDMMYY-<slug>.html` | — |
| W02 | effect | base page | Replace body with hero + controls + lifecycle + legend | structure | — |
| W03 | judgment | real file list | Author tree rows with `data-born` + seqslot, actor chips | tree | — |
| W04 | judgment | lifecycle | Author `STEPS[]` with empty "before" step first, roles, verdict/leak/marks | data | — |
| W05 | effect | Reference engine | Drop in engine JS + CSS deltas; default paused/static | working page | — |
| W06 | deterministic | page | Validate: HTML parse + click ⏭ through every step while paused | every frame readable | not readable → fix, repeat W06 |

Chi tiết từng bước (nguồn chân lý cho W01–W06):

1. Generate the base page with **`/docs-site-macos`** conventions (glass CSS, fonts, scrollbar, background plane, output to `llmwiki/html/DDMMYY-<slug>.html`, auto-host).
2. Replace the body with the `hero + controls + .lifecycle(left steps / right tree-pane) + legend` structure above.
3. Author the folder tree: one `.trow id="f-*" data-born="…"` per file, each starting with `<span class="seqslot"></span>`; actor chips in `.controllers` likewise.
4. Author `STEPS[]`: order them as a real lifecycle, include an explicit **empty "before" step** first; tag each node's `role` (src/dst); add `verdict`/`leak`/`marks` where relevant.
5. Drop in the engine JS + CSS deltas. Default to paused/static; ⏭ steps, ▶ auto-plays slowly.
6. Validate: `python3 -c "import html.parser; html.parser.HTMLParser().feed(open(F).read())"`; open via the auto-host server; click ⏭ through every step and check each frame reads clearly when *paused*.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | `prefers-reduced-motion: reduce` | skip animation, show full frames (RULE-11) | — | W06 |
| B02 | user_optional | viewer presses ▶ "Tự chạy" | auto-advance slowly; ⏭ plays one frame then stops | default = paused/manual | W06 |

### Validation và stopping
Deterministic: HTML parse check. Needs eyes: click ⏭ through every step and confirm each frame reads clearly when *paused*. Stop when every frame passes; then write the output report.

### Examples
- **Positive:** "làm trang hoạt họa life cycle cài harness" → STEPS starts with empty "before install", step 1 cursor visits `c-install → f-policy → f-cli`, `f-policy` types in teal "ghi/tạo"; paused frame shows ①②③ badges and full caption.
- **Boundary/failure:** source and dest rows both tinted the step accent → viewer cannot tell copy direction → violates RULE-07/08; switch right-pane nodes to ROLE colors (src blue "đọc", dst teal "ghi/tạo") with text tags.

### Reference — Page structure
```
hero (title + 1-line how-to-read)
controls: ⏮  ⏭ Bước tiếp  ▶ Tự chạy   <hint>   <phase chip>   <n / N>
.lifecycle (grid: narrow left | wide right)
 ├─ .steps  (LEFT) — compact cards: <span class=sp>label</span><h3>title</h3>   (NO paragraph)
 └─ .tree-pane (RIGHT, sticky glass)
      ├─ chrome dots + title
      ├─ .controllers — actor chips (installer / agent / git / CI), each with a .seqslot
      ├─ .tree — rows with id=f-*, data-born="<step|−1 pre-exist|99 never>", leading .seqslot
      ├─ .frame-cap — fcNum / fcSp / fcH / fcD(streams) / fcFlow   (the per-frame caption)
      ├─ .cursor — gutter arrow (fill=currentColor)
      └─ .verdict + .leak — floating tags on the RIGHT side near the active row
legend: đọc(blue) · ghi(teal) · cho qua(green) · chặn(red) · lọt(amber)
```

### Reference — STEP data model
```js
const STEPS = [
  { ph:'install'|'run',           // phase (left chip text)
    sp:'CÀI · B0',                // short label
    h:'Đặt lõi vào repo',         // title (left + caption)
    d:'... mô tả đầy đủ ...',     // detailed narration → ONLY in right caption, streams
    flow:'installer → policy.yaml', // 1-line data-flow summary
    chain:['c-install','f-policy','f-cli'],  // node ids the cursor visits IN ORDER
    role:{'f-policy':'dst','f-cli':'dst'},   // per-node role: 'src'|'dst' (pass/actor inferred)
    marks:{'f-x':'warn','f-y':'deny'},       // optional: override role on specific nodes
    leak:'f-wiki',                            // optional: node that "leaked" (amber tag)
    verdict:{kind:'deny'|'ok'|'neutral', text:'exit 2 · CHẶN'} },  // optional: end badge
];
```
`data-born` on each file row: the step index at which it is created (`-1` = pre-existing vendor file, `99` = never created e.g. a blocked write attempt). Files with `born === cur` type in this step; `born < cur` already present; otherwise hidden.

### Reference — Core JS (the engine — reproduce faithfully)
```js
const PAL=[{c:'#0a84ff',bg:'rgba(10,132,255,.12)'},{c:'#30b0c7',bg:'rgba(48,176,199,.13)'},
  {c:'#5856d6',bg:'rgba(88,86,214,.12)'},{c:'#34c759',bg:'rgba(52,199,89,.14)'},
  {c:'#ff9500',bg:'rgba(255,149,0,.15)'},{c:'#ff2d55',bg:'rgba(255,45,85,.12)'}];      // màu mỗi step
const ROLEINFO={src:{c:'#0a84ff',t:'đọc',cls:'r-src'}, dst:{c:'#30b0c7',t:'ghi/tạo',cls:'r-dst'},
  pass:{c:'#9aa3b2',t:'',cls:'r-pass'}, actor:{c:'#9aa3b2',t:'',cls:'r-pass'},
  neutral:{c:'#0a84ff',t:'',cls:'r-pass'}, deny:{c:'#e0264b',t:'chặn',cls:'deny'},
  ok:{c:'#34c759',t:'cho qua',cls:'ok'}, warn:{c:'#f0902a',t:'lọt',cls:'warn'},
  attempt:{c:'#e0264b',t:'',cls:'deny'}};

let cur=0, auto=false, timers=[];
const clear=()=>{timers.forEach(clearTimeout);timers=[]};
// con trỏ ở GUTTER trái (x = rowLeft − 22), y = giữa dòng
const at=id=>{const el=document.getElementById(id),pr=pane.getBoundingClientRect(),r=el.getBoundingClientRect();
  return {gx:Math.max(2,r.left-pr.left-22), y:r.top-pr.top+r.height/2, el};};
// hiện nếu pre-existing(-1) hoặc đã tạo ở bước TRƯỚC (b<i); born===i sẽ "gõ" ra trong bước này
function applyVis(i){document.querySelectorAll('.trow[data-born]').forEach(e=>{
  const b=+e.dataset.born; e.classList.toggle('notyet', !((b===-1)||(b!==99&&b<i)));});}

function prep(){ const s=STEPS[cur];
  /* left active card, prog, phase, caption (fcNum/fcSp/fcH/fcD=full/fcFlow) */
  const a=PAL[cur%PAL.length], rs=document.documentElement.style;
  rs.setProperty('--ac',a.c); rs.setProperty('--acbg',a.bg);          // accent PER-STEP (trái + chip)
  document.querySelectorAll('.trow,.chip').forEach(e=>e.classList.remove('hit','deny','ok','warn','attempt','born-now','r-src','r-dst','r-pass'));
  document.querySelectorAll('.rtag').forEach(t=>t.remove());
  document.querySelectorAll('.seqslot').forEach(s2=>{s2.textContent='';s2.className='seqslot';});
  applyVis(cur); return s; }

function paint(idx,s){ const id=s.chain[idx], last=idx===s.chain.length-1, vk=s.verdict?.kind||'';
  const el=document.getElementById(id); el.classList.remove('notyet'); const p=at(id);
  let role = id==='f-raw' ? 'attempt'
    : (s.marks&&s.marks[id]) || (last&&vk) || (s.role&&s.role[id]) || (id.indexOf('c-')===0?'actor':'pass');
  const ri=ROLEINFO[role]||ROLEINFO.pass;
  el.classList.add('hit'); if(ri.cls)el.classList.add(ri.cls); if(id==='f-raw')el.classList.add('attempt');
  const slot=el.querySelector('.seqslot'); if(slot){slot.textContent=idx+1; slot.className='seqslot on '+(ri.cls||'');}
  if(ri.t && id.indexOf('c-')!==0){const tag=document.createElement('span');tag.className='rtag '+ri.cls;tag.textContent=ri.t;el.appendChild(tag);}
  cursor.style.left=p.gx+'px'; cursor.style.top=(p.y-9)+'px'; cursor.style.color=ri.c;   // cursor đổi màu theo vai trò
  /* leak tag + verdict tag positioned on the RIGHT side near p.y */ }

function revealBorn(i){document.querySelectorAll('.trow[data-born]').forEach(e=>{if(+e.dataset.born===i)e.classList.remove('notyet');});}
function typeRow(e,dur){e.classList.remove('notyet'); if(dur<=0)return; e.style.setProperty('--td',dur+'ms');
  e.classList.add('typing'); timers.push(setTimeout(()=>e.classList.remove('typing'),dur+40));}
function typeText(el,txt,per){el.textContent='';el.classList.add('streaming');let i=0;
  const tick=()=>{el.textContent=txt.slice(0,i); i++<txt.length?timers.push(setTimeout(tick,per)):el.classList.remove('streaming');};tick();}

function full(){const s=prep(); revealBorn(cur); s.chain.forEach((id,idx)=>paint(idx,s));}   // TĨNH = frame đầy đủ
function animate(){const s=prep();
  if(reduce){revealBorn(cur); s.chain.forEach((id,idx)=>paint(idx,s)); return;}
  const per=30, capDur=Math.max(1600, s.d.length*per);          // transcript = đồng hồ; CHẬM
  typeText(document.getElementById('fcD'), s.d, per);
  const born=[...document.querySelectorAll('.trow[data-born]')].filter(e=>+e.dataset.born===cur);
  let bt=400; const slot=born.length?(capDur*0.55)/born.length:0;
  born.forEach(e=>{timers.push(setTimeout(()=>typeRow(e,Math.min(slot*0.8,700)),bt)); bt+=slot;});
  const n=Math.max(1,s.chain.length);
  s.chain.forEach((id,idx)=>timers.push(setTimeout(()=>paint(idx,s), 300+Math.round(idx*(capDur-300)/n))));
  if(auto) timers.push(setTimeout(()=>step(cur+1), capDur+2200));   // CHỈ tự sang khi auto
}
function step(i){clear(); cur=(i+STEPS.length)%STEPS.length; animate();}   // Tự bước: gõ 1 frame rồi dừng
// prev/next: auto=false; step(±1).  play: auto=!auto; auto?step(cur):full().
// LOAD: requestAnimationFrame(()=>setTimeout(()=>{cur=0;full();},200));   // mặc định TĨNH frame đầy đủ
```

### Reference — Essential CSS deltas (beyond docs-site-macos)
```css
.lifecycle{display:grid;grid-template-columns:minmax(190px,.5fr) 1.5fr;gap:22px;align-items:start}
.steps{max-height:74vh;overflow-y:auto} .step{opacity:.62} .step.active{opacity:1;border-left:3px solid var(--ac)}
.tree-pane{position:sticky;top:18px} .trow{display:flex;align-items:center;white-space:pre;border-radius:8px;padding:5px 8px}
.seqslot{display:inline-flex;align-items:center;justify-content:center;width:17px;height:17px;margin-right:8px;border-radius:50%;font-size:10px;font-weight:800;background:transparent;color:transparent;border:1px solid rgba(30,90,170,.1)}
.seqslot.r-src{background:#0a84ff;color:#fff;border-color:transparent}
.seqslot.r-dst{background:#30b0c7;color:#fff;border-color:transparent}
.seqslot.r-pass{background:#9aa3b2;color:#fff;border-color:transparent}
.trow.hit.r-src{background:rgba(10,132,255,.13);box-shadow:inset 0 0 0 1px #0a84ff}
.trow.hit.r-dst{background:rgba(48,176,199,.17);box-shadow:inset 0 0 0 1px #30b0c7}
.trow.hit.r-pass{background:rgba(140,150,165,.12);box-shadow:inset 0 0 0 1px rgba(120,130,145,.5)}
.rtag{margin-left:9px;font-size:10px;font-weight:700;padding:1px 8px;border-radius:11px}
.rtag.r-src{background:rgba(10,132,255,.14);color:#0a84ff} .rtag.r-dst{background:rgba(48,176,199,.2);color:#1d7d8c}
.trow.notyet{display:none}                              /* CHƯA tạo → ẩn hẳn (không mờ) */
.trow.typing{overflow:hidden;animation:typeline var(--td,500ms) steps(30) both}
@keyframes typeline{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
.cursor{position:absolute;z-index:7;will-change:left,top;color:var(--ac);
  transition:left .5s cubic-bezier(.45,.05,.2,1),top .5s cubic-bezier(.45,.05,.2,1),color .3s ease}  /* MƯỢT: left+top CÙNG duration+easing, đừng lệch */
.cursor svg path{fill:currentColor}                     /* arrow color = currentColor (set per role) */
.fc-sp{background:var(--acbg);color:var(--ac)}          /* caption chip = per-step accent */
```

### Delivery — Output Report
Write a `propose` draft to `llmwiki/wiki/sources/draft/DDMMYY-<ten>.md`, append to `wiki/index.md` + `wiki/log.md`.
Dùng **YAML frontmatter** (chuẩn OKF v0.1 — KHÔNG dùng bold `**Type:**`, sẽ fail OKF):
```markdown
---
type: draft
title: DDMMYY-<ten>
status: proposed
tags: [cursor-animated-sites, output-report]
timestamp: YYYY-MM-DD
---

# DDMMYY-<ten>

## What
<một câu — trang này dựng/quyết định cái gì>

## Files
| File | Action |
|------|--------|
| `llmwiki/html/DDMMYY-<ten>.html` | created |

## Origin
- **Draft:** `wiki/sources/draft/DDMMYY-<ten>.md`
- **Commit:** _(verify-before-commit điền)_
```

## Origin
- Distilled by `/orca-eval` from the session that built `llmwiki/html/250626-harness-lifecycle.html`.
- Base theme: `/docs-site-macos` (`~/.claude/skills/docs-site-macos/SKILL.md`).
