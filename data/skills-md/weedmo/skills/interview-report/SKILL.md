---
name: interview-report
description: "Renders matt-auto's decision log (question → decision → rationale, per pipeline stage) into the run's live decision-graph page: stages in order, each decision an editable node the user can rewrite or flag and export as <slug>.edits.json for matt-auto to rework from, plus ticket waves, review and PR lanes while the run executes. Owns the view and writes <slug>.data.json; build (render.py) and delivery (deliver.py) come from the shared `$loop-report` skill. Called by matt-auto after loading the confirmed design and before its final report — never standalone."
---

# Interview Report (decision graph)

Turn the decision log matt-auto's delegate produced — question, decision, one-line rationale,
stage by stage — into a graph a person reads in under a minute and can *push back on*. The raw
log is a transcript nobody scrolls; since the user opted out of live confirms, the graph is their
steering wheel: a node they disagree with, they edit or flag and export for matt-auto.

## When this runs

Only inside matt-auto's pipeline:

1. After loading the confirmed spec — a read-only `design` stage, interview skipped,
   and execution stages pending. This is not a design approval gate.
2. On every board update once tickets exist, and before the final report —
   regenerate over the full execution log; include `outcome` only after verified
   implementation and independent review (and shipping when requested).

Never off a standalone `$grill-me` / `$grill-with-docs` session: the report is about delegate
decisions.

## Input

matt-auto's decision log: ordered `{question, decision, rationale}` per stage, which were
escalated to the real user, each stage's status (done / in progress / pending / skipped, with
why); once the run executes, the ticket DAG, wave plan, ticket states, and review / PR state.

## Output

`docs/agents/matt-auto-log/<slug>.data.json` (the decision log's `<slug>`) and from it
`docs/agents/matt-auto-log/<slug>.html`, one self-contained page; regeneration rewrites both.

## Build and deliver

This skill owns the *view* — `assets/view.html` and its checks in `assets/validate.py`; the page
shell, build, and delivery are **`$loop-report`**'s:

1. Write the data JSON (format below) to `docs/agents/matt-auto-log/<slug>.data.json`.
2. Build, then deliver, as matt-auto asked (probe or publish):

   ```
   python3 <loop-report's dir>/assets/render.py \
     --data docs/agents/matt-auto-log/<slug>.data.json \
     --out  docs/agents/matt-auto-log/<slug>.html \
     --view <this skill's dir>/assets/view.html
   python3 <loop-report's dir>/assets/deliver.py publish --page docs/agents/matt-auto-log/<slug>.html
   ```

   `<this skill's dir>` holds this SKILL.md; `<loop-report's dir>` is listed in loop-report's
   SKILL.md. `render.py` validates (common keys, then `validate.py`: stage keys, unique decision
   ids, ticket statuses and blockers, wave modes and `why`, `outcome` only with `review`). A
   probe is `deliver.py probe --page …`.

Delivery is `deliver.py`'s alone — never hand-splice the page or edit the view's CSS/JS; relay
its one-line answer to matt-auto verbatim. If `$loop-report` is missing, say
`loop-report unavailable — weed-harness 4.x required` once; the decision log on disk is then the
only report, and matt-auto's board must say so.

### Data format

Common keys (`title`, `slug`, `generated`, `summary`, `progress`, `outcome`) follow loop-report's
contract. The view's own keys:

```json
{
  "stages": [
    {
      "id": "interview",
      "name": "인터뷰",
      "skill": "grill-with-docs",
      "status": "done",
      "note": "",
      "decisions": [
        {
          "id": "interview-1",
          "question": "restated plainly",
          "before": "prior policy or de-facto behavior, or null",
          "change": "new",
          "decision": "the after-state",
          "rationale": "One-line rationale",
          "escalated": false
        }
      ]
    }
  ]
}
```

- `stages` in the order the pipeline ran them. Use matt-auto's execution stages (Load design, Size work,
  Spec reference, Tickets, Execution plan, Implement, Review, Ship); drop stages that never applied — except skipped ones,
  which stay visible with `"status": "skipped"` and a `note` saying why (`"autonomous"`, `"confirmed spec"`).
- `status`: `done` / `in-progress` / `pending` / `skipped`. Optional explicit `percent`; else done
  is 100, pending 0, an in-progress implement stage follows its tickets.
- **`design` stage — first on every run**: `id: "design"`,
  `name: "확정 설계"`, `status: "done"`, `note` the spec path (its artifact URL when the
  spec has one). Its decisions
  keep the spec's own ids (`D1`, `D2`…) and carry `source: "matt-design"` (legacy specs: `"design-map"`) plus `before` /
  `change` (`null` / `"new"` unless the spec names a prior state). The view renders a sourced
  decision **read-only** — 설계에서 확정 badge, no edit box, no flag — so it never appears in
  `<slug>.edits.json`; `validate.py` refuses a sourced decision without `change`.
- Decision `id`s stay stable across regenerations (stage prefix + ordinal) — edits key on them.
- `escalated: true` marks decisions the real user answered directly; highlighted.
- **`before` / `change` — the before → after view on every decision.** `before` is the prior
  state — a documented policy or the code's de-facto behavior — or `null` when nothing existed
  (rendered *"없음 — 정해진 바 없었음"*). `change` classifies the move as a badge, visible even when
  collapsed: `"new"` (신규), `"redirect"` (방향 전환 — a prior direction changed), `"keep"` (유지 — a
  prior policy examined and confirmed). `decision` is always the after-state. Fill these whenever
  the log knows the before-state; a decision without `change` falls back to a single-line node —
  the degraded form, not a choice.
- **`progress` + `tickets` — the live board, from the ticket stage until the run ends.** They
  render *진행 상황* above everything: run-wide percentage, elapsed and remaining time, the flow —
  **waves as columns left to right, each ticket a node in its wave** — and a red blocker box for
  anything stuck. The decision graph stays below a 결정 검토 disclosure; the reader's
  expansion choice sticks. Before ticket planning, the initial confirmed-design
  render may omit `tickets` and `plan`. Once planned, every run, including a
  one-ticket run, carries `tickets`, `plan`, and `progress` through verification
  and review. Set `state: "done"` only when execution's completion checks pass.

```json
"tickets": [
  { "id": "T3", "title": "결과 패널 렌더링", "status": "blocked",
    "blockedBy": [], "gates": { "met": 3, "total": 5 },
    "route": "matt-deep",
    "worker": { "model": "fable", "effort": "high",
                "dispatchId": "dispatch-7f2", "worktree": "matt-auto/T3" },
    "estimateMin": 25,
    "blocker": { "reason": "gate", "detail": "G4 스냅샷 테스트 실패 — 기대 +504/−175, 수신 +504/−134" },
    "note": "선택 — 막히지 않았을 때의 한 줄" }
]
```

  - Ticket `status`: `done` / `in-progress` / `blocked` / `pending` / `skipped`. `blockedBy` lists
    the ticket ids it waits on — a DAG edge, not a blocker. The board **draws** them: the column
    says when a ticket runs, the edge says why it waits. `validate.py` refuses an unknown id; an
    edge into a collapsed wave is not drawn.
  - **`blocker` is required on every `blocked` ticket**: `reason` is one of `gate` / `escalation`
    / `ci` / `conflict` / `dependency` / `worker` / `review` / `other`; `detail` is the checkable
    fact — the unmet gate id with expected-vs-actual, the failing check, the open question.
    "막혔습니다" with no detail is the failure this panel exists to prevent.
  - `gates` counts the ticket's verification commands: `total` the commands the ticket names,
    `met` how many passed on the coordinator's own last run. Omit when the ticket names none.
  - **Who does the work shows on the node**: `route` is the routed agent; `worker` the model and
    effort it resolved to plus, for an Orca worker, `dispatchId` and `worktree`. Fill both — a
    route alone half-answers "어떤 티켓을 어떤 서브에이전트가 어떤 모델로".

- **`plan` — how the run intends to execute the tickets**, an ordered wave graph. Fill it right
  after the ticket DAG and keep it through the run — waves stay put as tickets change status.

```json
"plan": {
  "concurrency": 2,
  "placement": "local",
  "note": "선택 — 계획 전체에 대한 한 줄",
  "waves": [
    { "id": "W1", "mode": "parallel", "why": "서로 다른 파일만 건드려 충돌 위험이 없다",
      "tickets": ["T1", "T2"] },
    { "id": "W2", "mode": "sequential", "why": "같은 섹션을 고쳐 순차로 둔다",
      "tickets": ["T5"] }
  ]
}
```

  - `mode` is `parallel` or `sequential`; `why` is one Korean line on what made it so — file
    overlap, risk, dependency. `validate.py` refuses a wave without `why`.
  - `concurrency` = workers at once; `placement` = `local` or the environment name.
  - Waves render **left to right** with each wave's duration (parallel: slowest ticket;
    sequential: the sum). With no `plan` the page derives columns from `blockedBy` levels.
- **Estimates.** `progress.startedAt` (ISO) drives 경과; each ticket's `estimateMin` (plus
  `startedAt` once begun, `actualMin` once done) drives the rest. The page computes — never
  pre-compute — the overall percent (estimate-weighted, in-progress counted by elapsed/estimate,
  capped at 90%), 남은 예상, and 완료 예정 시각. **`estimateMin` is the run's own guess, labeled
  예상** — never present it as measurement, never back-fill it to move a bar.
- **Ticket detail — the modal.** A node is a summary; clicking opens the ticket. Specifics go
  here: `acceptance` (criteria as written), `steps` (티켓 읽기 → `$implement` → 게이트 재검증 →
  머지백, each `{ name, status, note }`), `gateList` (`{ id, text, status: met|unmet|manual,
  check, expect, actual }` — `CHECK:` and expected-vs-actual make an unmet gate actionable),
  `files`, `commits`. All optional.
- **`review` and `pr` — the tail of the flow.** `review` renders a 리뷰 lane (one node per
  dimension with its finding count); `pr` a PR lane (number, `branch → base`, check rows, babysit
  cycles, link) at the right end.

```json
"review": { "status": "in-progress", "skill": "code-review", "note": "…",
  "passes": [ { "id": "r1", "name": "정확성", "status": "done", "findings": 2, "note": "…" } ] },
"pr": { "number": 128, "url": "https://…", "base": "dev", "branch": "matt-auto/x",
  "status": "in-progress", "cycles": 2, "note": "…",
  "checks": [ { "name": "CI", "status": "failed", "detail": "unit: 2 failing" },
              { "name": "리뷰어", "status": "pending", "detail": "변경 요청 1건" },
              { "name": "머지 가능", "status": "ok", "detail": "충돌 없음" } ] }
```

  - Check `status`: `ok` / `done` / `failed` / `pending`; `detail` is the measured fact, never a
    guess. Omit `pr` on a run that opens no PR.
- **Long runs**: beyond three waves the page collapses finished ones itself, so publish a long
  plan in full.
- **`outcome`** follows loop-report's contract (files from `git diff --numstat` against matt-auto's
  baseline; `docs/agents/matt-auto-log/**` and `.unlazy/**` left out). Last regeneration only,
  with `progress.state: "done"` **and the `review` block** — matt-auto always runs its review
  pass, one-ticket runs included, and `validate.py` refuses an `outcome` without it.

### Writing the summary and decision text

**Always write the graph's content in Korean** — `title`, `summary`, stage `name`s and `note`s,
every `question` / `decision` / `rationale`; ids and JSON structure stay English. Write for a
teammate with zero context a week later: every `question`/`decision` pair stands alone —
translate ("X를 하기로 했다, 왜냐하면 Y"), don't paste the transcript line.

## The edits round-trip

The user can rewrite a decision, flag a node with a comment, and click **수정 내보내기**, which
produces `<slug>.edits.json` to save into `docs/agents/matt-auto-log/`. matt-auto checks for it
at every invocation and treats each entry as a change request — that logic is matt-auto's (its
Decision-graph report section). This skill's only obligations: stable decision ids and the view's
export format.

## Red flags

- Raw Q&A log pasted into the JSON unedited → the point is translation.
- Graph content in English → only ids and structure stay English.
- Decision ids changed on regeneration → orphans saved and exported edits.
- `outcome` on the initial confirmed-design generation → nothing has been built yet.
- A `blocked` ticket with vague `blocker.detail` ("실패함", "확인 필요") → it must be actionable
  without a terminal.
- `state` left at `running` on the final regeneration, or `progress.updated` typed from memory →
  the page polls forever, or "N분 전 갱신" lies.
- A wave without `why`, or estimates invented to move the bar → the plan panel becomes decoration.
- The file anywhere but `docs/agents/matt-auto-log/<slug>.html` → matt-auto and the round-trip
  assume it.
- Run outside matt-auto, off a bare grilling session → out of scope.
