---
name: skill-router
description: >-
  Always-on request orchestrator: analyze every user task from multiple angles,
  pick the best skill lane, and split large work across parallel agents. Use at
  the start of ANY user request (simple or complex); when routing skills; when
  the user mentions router, توجيه, تحليل الطلب, تقسيم المهام, router-feedback,
  or روتر-تعليق.
license: MIT
compatibility: Cursor, Claude Code, Antigravity, Codex, Gemini CLI, OpenCode, Copilot
metadata:
  author: SaleemNijim
  version: "3.1.1"
  self-learning: corrections-only
---

# Skill Router

Orchestrator for every request: **think → analyze → route → (split if needed) → execute**.

Works with any Agent Skills–compatible harness (Cursor, Claude Code, Antigravity, Codex, Gemini CLI, OpenCode, and similar). Not a passive lane picker — force a multi-angle read before coding or answering, even when the ask looks trivial.

Learns only from **routing corrections**, never from ordinary turns. Learned instincts are trigger examples (same shape as [registry.md](registry.md)), not token-overlap math. A correction **must** run `scripts/learn.py --correct` in the same turn; if it is not saved, Phase 4 failed. Hard instincts promote to GitHub only via `--promote-pr` (a review PR — never a push to `main`).

## Mandatory flow (every turn)

### Phase 0 — Multi-angle analysis (always, before tools)

Do this silently (or as a short internal checklist). Do **not** skip for "simple" tasks.

For the user request, answer:

1. **Surface ask** — What did they literally ask for?
2. **Hidden goals** — What outcome do they actually need? (shipping, data, UX, ownership, speed)
3. **Blind spots** — Angles they may not have considered (data integrity, auth/RLS, env mismatch, rollback, i18n/RTL, empty states, verification, cost/time, side effects on other apps)
4. **Risks** — What can go wrong if we do the naive thing?
5. **Success proof** — How will we know it worked? (query, screenshot, URL, test)
6. **Scope** — One agent enough, or split?

If a critical decision is ambiguous, ask **one** sharp question (with your recommended answer). Otherwise proceed.

Optional short user-facing lead-in (1–3 lines) when non-trivial:
`تحليل: … · مخاطر: … · تحقق: …`

Do **not** write a log on ordinary turns.

### Phase 1 — Route

Follow this order. Stop at the first match.

1. User names a skill/plugin → use it (Phase 0 still brief).
2. `stop router` / `بدون موجّه` / `نفّذ مباشرة` → skip auto-routing (one-line risk check only for the last).
3. If `.skill-router/overrides.md` exists in the **project root**, read it. If an instinct's examples resemble this request, use that lane + primary.
4. Else classify from [registry.md](registry.md).
5. Else `general`, or one clarifying question.

Then:

- Activate **at most one primary** and **one optional helper**.
- Read those skill files when needed; do **not** load excluded skills/rules.
- Prefer no skill over the wrong skill.
- Edited file stack → only stack-matched language rules.

Match instincts the same way you match registry triggers (resemblance to examples). **Do not** compute Jaccard / overlap scores in your head.

### Phase 2 — Split (when warranted)

Split into **2–4 parallel agents** when **any** of these is true:

- Independent workstreams (e.g. DB seed + UI + deploy config)
- Exploration of 2+ separate code areas with no shared write lock
- Research / audit / review that can fan out
- Estimated effort > ~15 minutes of sequential tool use
- Multiple apps / packages in a monorepo affected

**Do not split** when:

- One file / one bug / one clarifying answer
- Steps are strictly sequential (B needs A's output)
- User said `بدون موجّه` / `stop router` / named a single skill only

#### How to split

1. Write a one-line goal + acceptance check per subtask.
2. Launch independent subagents in **parallel** (whatever your harness supports: Task tool, subagents, worktrees, etc.).
3. Keep the parent as integrator: merge results, resolve conflicts, run the success proof from Phase 0.
4. Each subagent gets: goal, paths, constraints, "do not touch X", and what to return.

### Phase 3 — Execute under the lane

Complete the work. Verify against Phase 0 success proof before claiming done.

---

## Self-learning (corrections only)

### When to record (Phase 4)

Record **only** when this turn corrects routing. Signals:

| Signal | Example | `feedback` |
|--------|---------|------------|
| Command | `router-feedback wrong-lane debug` | `wrong-lane` |
| Command | `router-feedback wrong-primary ponytail` | `wrong-primary` |
| Command | `router-feedback ok` | `ok` (log only; does not create an instinct) |
| Natural language | «المسار غلط، هذا debug» / «ليش فتحت frontend-design» | `wrong-lane` or `wrong-primary` |
| Named skill after a miss | «استخدم ponytail» when another primary was chosen | `wrong-primary` |
| Override + lane hint | `بدون موجّه، أصلحه كـ debug` | `wrong-lane` if a prior route this session was wrong |

Arabic aliases: `روتر-تعليق خطأ-مسار <lane>` · `روتر-تعليق خطأ-سكيل <skill>` · `روتر-تعليق صحيح`.

If the original misrouted request is in this session, use **that** text as `--input` (not the correction sentence).

**Mandatory:** on any correction signal above, you **must** run `scripts/learn.py --correct` in **this turn** (cwd = the project repo, or `SKILL_ROUTER_ROOT`), then continue the user's work on the correct lane. Mentioning the command is not enough. If the CLI does not print `correction saved` / `✅ تعليق محفوظ`, Phase 4 failed — stop and run it before doing anything else.

### How to record

Prefer the CLI (it appends JSONL and rebuilds instincts immediately):

```bash
python scripts/learn.py --correct \
  --input "<first 80 chars of the misrouted user request>" \
  --wrong-lane <lane-you-chose> \
  --correct-lane <lane-they-wanted> \
  --correct-primary <skill-or-omit> \
  --source natural
```

`--source` is `natural`, `command`, or `named-skill`. Run from the **project repo** (the script walks up to `.git`). Confirm with `✅ تعليق محفوظ` (or the CLI's `correction saved`).

If Python is unavailable, append one JSONL row to `.skill-router/routing.log.jsonl` then run `--ingest` later:

```json
{ "row_type": "correction", "id": "<uuid>", "ts": "<ISO8601 with ms>", "input_summary": "<original request>", "wrong_lane": "<lane>", "wrong_primary": "<skill or null>", "correct_lane": "<lane>", "correct_primary": "<skill or none>", "feedback": "wrong-lane", "source": "natural" }
```

Never edit existing log rows. Never write a `decision` row. Never patch [registry.md](registry.md) on `main`.

### What the learner writes (Phase 5)

`scripts/learn.py --ingest` (already run by `--correct`) rebuilds `.skill-router/overrides.md`:

- **1** similar correction → **narrow** example (applies next turn)
- **3** similar (Jaccard ≥ 0.5 on tokens) → **soft** instinct; keywords = **intersection** of samples
- **5** similar → **hard** instinct; still does **not** edit `registry.md` on this branch

Dissimilar corrections that share only a lane pair stay **separate** instincts.

Optional: `python scripts/learn.py --propose-registry` prints Must-NOT suggestions.

When **5** similar corrections exist, `python scripts/learn.py --promote-pr` opens a GitHub PR (`instincts/YYYY-MM-DD-<id>`) that adds the Must-NOT example to [registry.md](registry.md) and a case to `tests/routing-cases.md`. Requires `gh`. **Never merge. Never `git push origin main`.** Set `SKILL_ROUTER_PROMOTE_ROOT` to the skill-router git clone if the installed skill is not the repo.

### Feedback quick-reference

```
router-feedback wrong-lane debug
router-feedback wrong-primary systematic-debugging
router-feedback ok

python scripts/learn.py --report
python scripts/learn.py --ingest --dry-run
python scripts/learn.py --export > instincts.json
python scripts/learn.py --import instincts.json
python scripts/learn.py --propose-registry
python scripts/learn.py --promote-pr
python scripts/learn.py --promote-pr --dry-run
python scripts/learn.py --reset --yes
```

---

## Examples

### 1 — RLS bug
```
Request: "عندي bug في الـ RLS policy"
→ Phase 0: tenant isolation / anon vs service role / which table; proof = failing query then passing query
→ Lane: debug
→ Primary: systematic-debugging
→ Helper: karpathy-guidelines
→ Split: no — one failing policy path
```

### 2 — Arabic landing page
```
Request: "صمّملي صفحة هبوط"
→ Phase 0: brand-first hero, RTL, one CTA; proof = desktop+mobile screenshot
→ Lane: design-ui
→ Primary: frontend-design
→ Helper: ponytail
→ Split: no (unless copy research is separate)
```

### 3 — Multi-app migrate
```
Request: "Migrate Supabase and update delivery + admin + driver"
→ Phase 0: data ownership, env keys, rollback; proof = catalogs load on each app
→ Lane: orchestrate
→ Primary: Phase 2 split (db / each app / verify)
→ Helper: handoff if context is long
→ Split: yes — 2–4 agents with "do not touch" boundaries
```

### 4 — Override
```
Request: "نفّذ مباشرة: زِد الـ timeout إلى 30s"
→ Phase 0: one-line risk (timeouts hide hung deps) — skip grilling
→ Lane: implement (direct)
→ Primary: none / stack only
→ Helper: —
→ Split: no
```

### 5 — False-positive trap
```
Request: "fix the CSS bug on the homepage hero"
→ Phase 0: broken layout vs redesign ask; proof = repro then fixed screenshot
→ Lane: debug (NOT design-ui)
→ Primary: systematic-debugging
→ Helper: karpathy-guidelines
→ Split: no
```

### 6 — Correction becomes next-turn instinct
```
Turn A: "fix the CSS bug on the homepage hero" was routed to design-ui
User: "المسار غلط، هذا debug"
→ Phase 4: --correct --input "fix the CSS bug on the homepage hero" --wrong-lane design-ui --correct-lane debug
→ Phase 5: narrow instinct written to .skill-router/overrides.md
Turn B: same phrasing → debug (instinct), not design-ui
"صمّملي صفحة هبوط" → still design-ui
```

### 7 — Gated UI control is implement, not design-ui
```
Request: "زر PDF في الواجهة العربية. نفس قيد الاعتماد. TDD."
→ Phase 0: export gated by approval, not a visual redesign; proof = failing test then passing test
→ Lane: implement (NOT design-ui)
→ Primary: stack-matched coding skill/rule if needed
→ Helper: tdd-workflow
→ Split: no
```

## Caps

- Max 1 primary skill + 1 helper (skills)
- Max 4 parallel subagents per split wave
- Never activate registry **conflict pairs**
- Missing named skill → next best in-lane primary, or one short question
- Log corrections only; never auto-edit `registry.md` on `main` (promotion is a PR)

## Priority when ambiguous

1. User names a skill/plugin → honor it (still run Phase 0 analysis)
2. `stop router` / `بدون موجّه` / `نفّذ مباشرة`
3. Project `.skill-router/overrides.md` instincts (hard, then soft, then narrow)
4. Clear registry triggers → that lane
5. Edited file stack → only stack-matched language rules
6. Else `general`, or one clarifying question

## always-on policy

- Keep a thin always-on rule that points at this skill (see harness adapters under `adapters/`)
- Heavy domain rules off unless the lane selects them
- Language packs only for the edited stack
- Learned instincts are project-local (`.skill-router/`). Promote across projects with `--export` / `--import`. Promote into the published registry only via `--promote-pr` (human-merged PR).

## User override

- Named skill / plugin → use it
- `stop router` / `بدون موجّه` → skip routing + split for that turn (still think briefly)
- `نفّذ مباشرة` → skip long analysis; keep one-line risk check only
- `router-feedback` / `روتر-تعليق` / natural correction → Phase 4 + `--correct` **in this turn** (not a normal lane). If unsaved, the task failed.

## Customization

Edit [registry.md](registry.md) to map lanes to skills installed in **your** environment.

## Maintainer note

When adding a skill to a project: append one registry row (triggers, primary, helper, excludes). Keep always-on rules thin; detail lives here. Learned false-positives belong in `overrides.md` until a human merges a `--promote-pr` into the registry Must-NOT column.
