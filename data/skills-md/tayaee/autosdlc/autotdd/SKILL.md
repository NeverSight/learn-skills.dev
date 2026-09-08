---
name: autotdd
description: Fully-automatic mode — runs tdd2 then aacpd for each issue, one issue completely finished (implement+verify+merge+push+deploy) before the next starts, never batching, never prompting mid-run. With no issue numbers, lists everything left in issues/ and asks once whether to run through all of it. Optionally runs each issue in its own throwaway git worktree (the `worktree` keyword) for isolation — still one issue at a time, each merged into main immediately before the next starts. Use when the user says "/autotdd", "autotdd #", or gives a list/range of issue numbers to fully implement and ship unattended.
---

# autotdd — tdd2, then code-quality-gate, then aacpd, per issue, fully automatic

The name is literal: **tdd** (via `tdd2`), followed by **code-quality-gate**
(project-wide quality verification), and **auto**mating everything after it
(`aacpd`: archive, commit, push, deploy). Pure orchestration:
no script of its own. It composes `tdd2` (implementation + lightweight targeted
tests, stops at `git add`), `code-quality-gate` (comprehensive quality gate),
and `aacpd` (archive+commit+push+deploy), run sequentially for each issue number.

**= implement (tdd2 + git add) + code-quality-gate + merge (archive+commit+push) + deploy to dev**

## Stream conventions

파일명 규약의 단일 정본은 `docs/spec/spec-issue-filenames.md`다. 요약:

- **Stream IDs**: `issue-<N>` and `autofix-<N>`. Bare-number arguments
  (e.g., `autotdd 22`) default to the `issue` stream.
- **문법(v3)**: `<stream>-<N>[-<slug>][__<마커>].md` — 마커는 닫힌
  리터럴 집합(`code-review-by-<llms>` / `refix-plan` / `agent-stats` /
  `must-fix-by-<llms>` / `tech-debt-by-<llms>` / `analysis-required` /
  `STATE-manual` / `STATE-agent-failed`).
- **판정 규칙**: 마커가 없거나 `must-fix-by-`/`analysis-required`만
  있으면 pending("remaining issues" 대상). 그 외 마커가 하나라도 있으면
  제외 — `code-review-by-`/`refix-plan`/`agent-stats`는 산출물,
  `tech-debt-by-`/`STATE-manual`/`STATE-agent-failed`는 파킹. 번호는
  정규식 `^(issue|autofix)-([0-9]+)`로 추출한다.
- **analysis-required 게이트**: pending이지만 원인 분석·계획이 없는
  raw 보고(`create-tickets.py` 자동 생성) — 아래 "analysis-required
  게이트" 절 참조.
- **예약 슬러그 가드**: 태그 없는 파일이 구(v1) 규약 구조에 해당하면
  (패턴 표는 spec 문서) 목록에 넣지 말고 "harness-project의
  `upgrade-issue-filenames.sh`를 실행하라"는 안내와 함께 중단한다.
- **Worktree branch name** (worktree mode): `<stream>-<N>` (e.g.,
  `autofix-3` for an autofix-stream issue) — 슬러그·태그는 브랜치명에
  포함하지 않는다.

## How this package relates to plain `/tdd`

Once Matt Pocock's `tdd` skill and this package are both installed,
`tdd2` is what `/tdd` *means* in a repo that tracks work as local
`issues/issue-#.md` files — it's the same red→green→refactor
discipline, just pointed at that local-file SDLC instead of a bare
prompt. `/tdd # + /aacpd #` and `/tdd2 # + /aacpd #` do the same thing;
saying `tdd2` is just unambiguous about which flavor you mean. All
three of `/tdd`, `/tdd2`, and `/aacpd` can stop and ask the user
something. `/autotdd` is the odd one out: it chains `tdd2` and `aacpd`
per issue and is built to run **unattended** — see "The one rule that
matters" below for exactly what that rules out.

## Dependency check — run this first, every invocation

`tdd2` depends on Matt Pocock's `tdd` skill for the actual
red→green→refactor discipline (`tdd2` just wraps it with the
local-file issue SDLC). Before doing anything else — before listing
issues, before the "run through all N?" prompt, before touching any
issue — confirm `tdd` is actually available:

```bash
[ -f ~/.claude/skills/tdd/SKILL.md ] || [ -f "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/tdd/SKILL.md" ]
```

(Or check it against the Available Skills listing already in context —
either way of confirming is fine.)

- **Found** → proceed normally.
- **Not found** → stop immediately and tell the user:

  > Matt Pocock's `tdd` skill isn't installed (checked
  > `~/.claude/skills/tdd/` and `.claude/skills/tdd/` in this repo —
  > neither exists), and `tdd2` depends on it. This package doesn't
  > know where you originally got it from, so it can't hand you an
  > install command — but you already have several of its sibling
  > skills installed (`ask-matt`, `grill-me`, `to-tickets`, `to-spec`,
  > `code-review`, `implement`, etc., all under `~/.claude/skills/`):
  > install `tdd` from wherever those came from, the same way, so it
  > ends up at `~/.claude/skills/tdd/SKILL.md` (or
  > `.claude/skills/tdd/SKILL.md` if you're installing it per-project
  > instead of globally). Re-run `autotdd` once it's there.

  Do **not** guess a GitHub URL or invent an install command — if none
  of `tdd`'s sibling skills are present either to point at, just report
  that `tdd` is missing and required, and stop.

## UI dependency check — run when target issues touch UI files

After the `tdd` dependency check passes, and once the target issue list
is known (after the user confirms for the no-number case, or immediately
for the explicit-number case), apply `tdd2`'s **UI-touching test** to
every target issue file — the single definition lives in `tdd2`'s step 1:
references to `templates/`/`.html`/`.css`/`.js` *plus* at least one
user-visible browser behaviour in the requirements; an extension match
alone doesn't count.

If **no UI-touching issues** are in the target list → skip this check
entirely and proceed to the per-issue loop.

If **any UI-touching issue** is found:

1. **Check the `agent-browser` skill** — look for it the same way as
   `tdd`:

   ```bash
   [ -f ~/.claude/skills/agent-browser/SKILL.md ] || \
   [ -f "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/agent-browser/SKILL.md" ]
   ```

   Or confirm against the Available Skills listing already in context —
   either method is fine.

2. **Found** → proceed to the per-issue loop. `tdd2`'s step 10 will use
   it for automated browser verification.

3. **Not found** → install it. Unlike the `tdd` dependency (whose
   origin this package doesn't know, so it never guesses an install
   command), `agent-browser` has a known pinned source, so installing
   it unattended is fine — always from exactly this source, never from
   a search result:

   ```bash
   npx skills add vercel-labs/agent-browser -g -y
   ```

4. Re-confirm that `agent-browser/SKILL.md` exists. If the installation
   failed for any reason → **stop and report**. Do not proceed with
   UI-touching issues without browser verification capability.

## analysis-required 게이트 — run after the UI dependency check, before the loop

`create-tickets.py`가 로그 스캔으로 자동 등록한 이슈
(`issue-<N>-<slug>__analysis-required.md`)는 원인 분석도 수정 계획도
없는 raw 에러 보고다. `issues/`(아카이브 제외) 전체에서 이 파일이
하나라도 있으면, 스코프(명시 번호든 no-number든)와 무관하게 루프
진입 전에 **한 번만** 확인한다:

```bash
ls issues/*__analysis-required*.md 2>/dev/null
```

- **없음** → 건너뛰고 다음 단계로.
- **하나 이상 있음** → 사용자에게 물어본다: "분석되지 않은 raw 이슈
  N개가 있습니다(`__analysis-required`). 자동 진행 전에
  `grill-with-docs`를 먼저 돌려서 원인 분석·수정 계획을 채울까요?"
  - **예** → `grill-with-docs` 스킬을 해당 파일들에 대해 실행해 분석·
    계획을 채운 뒤(사람이 결과를 반영해 `__analysis-required` 마커를
    제거하는 것은 별도 단계 — 이 스킬이 자동으로 리네이밍하지 않는다),
    다음 단계로 진행.
  - **아니오** → `__analysis-required` 파일들은 이번 실행 스코프에서
    제외하고 나머지 정상 pending 이슈만 진행. 침묵 제외 금지 — 몇 건을
    건너뛰는지 보고한다.

이것도 dependency check처럼 "질문"이지만 **루프 시작 전**에만 발생 —
"The one rule that matters"가 금지하는 mid-run 프롬프트가 아니다.

## Two ways to invoke it

### `/autotdd <numbers>` — scope given, runs immediately

No confirmation — the numbers are the scope. Go straight to the loop
below.

### `/autotdd` — no numbers, scope is implicit

1. List every issue still in `issues/` (not yet archived) — everything,
   regardless of state: not started, in-progress, or already
   pending-deploy. 산출물·파킹 마커가 붙은 파일은 제외하되,
   `__must-fix-by-`/`__analysis-required`는 pending이므로 **포함**한다
   (판정 규칙은 Stream conventions / spec 문서 참조).

   ```bash
   ls issues/issue-*.md 2>/dev/null | \
     grep -Ev '__(code-review-by-|refix-plan|agent-stats|tech-debt-by-|STATE-manual|STATE-agent-failed)'
   ```

2. Show the list, ask **once**: "run through all N of these in order?"
3. Yes → build the ordered issue-number list from that listing and
   enter the fully-automatic loop below. No further questions from
   this point on.
4. No → stop; don't guess a partial scope.

This is the *only* prompt `autotdd` ever shows (aside from the
dependency check above, which isn't really a prompt — it's a hard stop
if `tdd` is missing, not a question). Once the run starts (whichever
way it started), it does not ask anything else — see "The one rule
that matters" below for what that means concretely.

## Optional `worktree` keyword — isolation, not concurrency

Both invocation forms above accept an extra `worktree` keyword
anywhere in the input (`autotdd worktree 100 101 102`, `autotdd 100
101 102 worktree`, or bare `autotdd worktree` for the no-number case).
Strip it out before applying the number-parsing rules below — it is
never a number and never counts as scope.

**"Worktree" means isolation, not concurrency.** Issues are still
processed one at a time, in order, exactly like the default loop —
`worktree` only changes *where* each issue's `tdd2`/`aacpd` pair runs
(a throwaway sibling checkout instead of the directory you're standing
in). The payoff: your current checkout stays untouched while the run
is in progress, so you can inspect `main` mid-run, or point a separate
`autotdd` invocation at a different set of issue numbers, without the
two colliding.

No `worktree` keyword → default per-issue loop (below). `worktree`
present → see "Worktree mode" instead, further down.

## Parsing an explicit issue list

| Input | Meaning |
|---|---|
| `autotdd 100` | issue 100 |
| `autotdd 100 101 102` | issues 100, 101, 102 |
| `autotdd 100, 101, 102` | issues 100, 101, 102 |
| `autotdd 100 to 110` | issues 100–110 inclusive |
| `autotdd 100 ~ 110` | issues 100–110 inclusive |
| `autotdd worktree 100 101 102` | issues 100, 101, 102, worktree mode |
| `autotdd 100 to 110 worktree` | issues 100–110 inclusive, worktree mode |

Rule: strip the `worktree` keyword first (see above) if present, then
extract all numbers from what's left. If there are exactly two and
they're joined by `to` or `~`, expand to the inclusive range. Otherwise
treat every extracted number as a listed issue, in the order given.

## The one rule that matters

> ⚠️ Never run all the `tdd2`s first and all the `aacpd`s after. Each
> issue must be **fully finished** — `tdd2 #` immediately followed by
> `code-quality-gate`, then `aacpd #` — before touching the next issue number. And within a run,
> **never prompt** — not per-issue, not for UI verification (see the
> exception noted in `tdd2`'s step 10), not for anything. The single
> upfront "run through all N?" question (no-number case only) and the
> dependency check above are the entire interactive/blocking surface of
> this skill.

> **Note on UI verification:** `tdd2`'s step 10 auto-triggers for any
> UI-touching issue (per the test in `tdd2`'s step 1), even without an
> explicit `### UI 검증` section. The pre-loop check above installs
> the `agent-browser` skill (`vercel-labs/agent-browser`) when it's
> missing, so an unattended run only stops on UI verification if that
> installation fails — or if the browser verification itself fails.

> **Note on worktree mode:** the identical rule applies — one issue
> fully finished (through its `git merge --ff-only` into `main`) before
> the next one starts. Worktree mode (below) only changes where each
> iteration's `tdd2` + `code-quality-gate` + `aacpd` trio physically runs; it never changes this
> one-at-a-time, no-batching ordering.

`autotdd 1 2 3` is:

```
tdd2 1 → code-quality-gate 1 → aacpd 1 → tdd2 2 → code-quality-gate 2 → aacpd 2 → tdd2 3 → code-quality-gate 3 → aacpd 3
```

**not**

```
tdd2 1 → tdd2 2 → tdd2 3 → aacpd 1 → aacpd 2 → aacpd 3
```

Why: once an issue is pushed and deployed to dev, it's a clean
checkpoint — a mid-batch failure has an unambiguous boundary between
what's live and what's untouched. Stacking implementations first
destroys that boundary.

## Phase 2: `code-quality-gate` 규약 및 탐색 알고리즘

`tdd2`가 이슈 단위의 구현과 경량 검사(해당 이슈 단위 테스트 + `verify-issue-#.sh`)를 마치고 `git add`한 직후, 전체 프로젝트 품질을 보장하기 위해 `code-quality-gate`를 실행한다.

1. **탐색 디렉터리 순서**:
   - `.` (프로젝트 루트) ➔ `bin/` ➔ `scripts/`
2. **실행 우선순위 규칙**:
   - **1순위 (Unified Quality Gate)**:
     - `code-quality-gate.sh` (또는 `.bat`, `.ps1`)가 `.` ➔ `bin/` ➔ `scripts/` 중 발견되면, **해당 스크립트 하나만 실행**하고 개별 스크립트 탐색은 생략한다.
   - **2순위 (Discovered Individual Checkers)**:
     - `code-quality-gate.sh`가 없는 경우, 아래 개별 품질 검증 스크립트들을 발견되는 대로 차례로 수행한다:
       - `run-ruff.sh`
       - `run-pyright.sh`
       - `run-pytest.sh` (또는 `run-unit-tests.sh`)
       - `run-regression-tests.sh`
       - `run-pyright-full.sh`
       - 기타 `run-*.sh` (pip-audit, gitleaks, semgrep 등 프로젝트에 존재하는 품질 스크립트)
     - 각 스크립트 역시 `.` ➔ `bin/` ➔ `scripts/` 순서로 탐색하여 가장 먼저 발견된 것을 실행한다. 프로젝트 내에 없으면 autosdlc 번들 기본 스크립트(`bin/run-*.sh`)를 fallback으로 실행한다.

## Per-issue loop (default — no worktree)

For each issue `#` in the target list, **resolve its file first**
(`issues/issue-#.md`, or the unique tag-less `issues/issue-#-<slug>.md`
— see the spec in Stream conventions), then **check its state** —
don't redo finished work:

```bash
f=$(ls "issues/issue-${n}.md" issues/issue-${n}-*.md 2>/dev/null | grep -v '__' | head -1)
grep -q '\*\*구현 완료 일시\*\*: *(미정)' "$f"
```

- Placeholder still `(미정)` (not implemented, or in-progress) →
  `tdd2 #`, then `code-quality-gate`, then `aacpd #`.
- Already filled in (implemented earlier, never merged — e.g. a prior
  `tdd2` run that stopped short of `aacpd`) → `code-quality-gate`, then `aacpd #`.

```
for # in <target list>:
    if no tag-less issues/issue-#*.md resolves (rule above):
        warn and skip #, continue to next
    if 구현 결과 already filled in:
        code-quality-gate   ← comprehensive quality gate (. -> bin/ -> scripts/)
        aacpd #             ← archive + commit + push + deploy --env dev
    else:
        tdd2 #              ← implement + verify acceptance criteria + git add (stops there)
        code-quality-gate   ← comprehensive quality gate (. -> bin/ -> scripts/)
        aacpd #             ← archive + commit + push + deploy --env dev
    # is done only once the applicable step(s) above have completed
```

- **Any failure stops the whole run immediately** — a non-zero verify,
  a failed commit/push/deploy, a UI-verification step that needed a
  human and `agent-browser` wasn't available, anything. Report which
  issue failed and at which step; do not proceed to the remaining
  issues.
- On success, report the full list of completed issue numbers.

## Worktree mode

Triggered by the `worktree` keyword (see above). Same target-issue
list, same one-at-a-time ordering, same "check state first" rule as
the default loop — only the mechanics of each iteration differ.
Neither `tdd2` nor `aacpd` are modified for this: they run completely
unmodified, just with their cwd inside a throwaway worktree instead of
the repo you're standing in.

Naming convention, resolved once per issue from the repo root
(`git rev-parse --show-toplevel`):

| | Value |
|---|---|
| Worktree path | `../<repo-name>-issue-<#>` (sibling of the repo, not inside it) |
| Branch | `issue-<#>` |

For each issue `#` in the target list:

1. **Check state first**, on `main`, same test as the default loop
   (`구현 완료 일시` still `(미정)`?). If it's already filled in
   (implemented earlier but never archived — nothing to isolate) → run
   `aacpd #` directly on `main`, no worktree involved, then move on to
   the next `#`.
2. Otherwise, from `main` at its current tip:

   ```bash
   git worktree add ../<repo-name>-issue-<#> -b issue-<#>
   ```

3. Inside that worktree: `tdd2 #`, then `aacpd #` — unmodified, exactly
   as the default loop runs them. `aacpd`'s own commit, push, and
   `deploy --env dev` all happen on the `issue-<#>` branch here; that's
   fine, because step 2 guarantees `issue-<#>` never diverges from
   `main` except by this one issue's commit(s) — so whatever gets
   deployed is byte-identical to what `main` will contain after step 4.
4. Back on `main`:

   ```bash
   git merge --ff-only issue-<#>
   ```

   - **Succeeds** → go to step 5.
   - **Fails** (only possible if `main` moved for some reason since
     step 2) → attempt recovery, once:
     1. `git -C ../<repo-name>-issue-<#> rebase main`
     2. **Rebase hits conflicts** → attempt one AI-assisted resolution:
        run, once, in that worktree:

        ```bash
        claude --model sonnet -p "Resolve the git rebase conflicts in this worktree. Conflicted files: $(git diff --name-only --diff-filter=U). Resolve them preserving both sides' intent, stage the resolved files, and run 'git rebase --continue'. Do not skip or abort the rebase."
        ```

        - Resolved (rebase completes with no conflict markers left) →
          **re-run the same verification this issue already passed
          once** (`aacpd`'s five-check Python gate if `pyproject.toml`
          exists at the repo root, otherwise whatever `tdd2` steps 5–9
          used) inside the worktree.
          - Passes → retry `git merge --ff-only issue-<#>` on `main`,
            go to step 5. Note in the final report that this issue
            needed an AI-assisted rebase resolution.
          - Fails → **stop the whole run** (see below), and still note
            that the AI-assisted resolution was attempted.
        - Not resolved (still conflicted, or `claude` itself failed) →
          **stop the whole run** (see below), noting the attempt and
          its failure.
     3. No conflicts on rebase but still not fast-forwardable, or any
        other unexpected git failure → **stop the whole run** (see
        below).
5. `git push origin main`
6. Clean up — **only after a successful merge**:

   ```bash
   git branch -d issue-<#>
   git push origin --delete issue-<#>
   git worktree remove ../<repo-name>-issue-<#>
   ```

7. Move to the next `#`.

Result: `main`'s history stays linear — no merge commits, nothing to
distinguish this from having worked directly on `main` the whole time.
This is deliberate: it's a direct fix for the old failure mode where
several issues only showed up as a single combined integration at the
end — every issue now lands on `main`, via its own `git push origin
main`, immediately after it finishes and before the next one starts.

### Stopping the whole run (worktree mode)

Same rule as the default loop's "any failure stops the whole run
immediately" — extended with one difference: **do not clean up the
failing issue's worktree or branch.** Leave `../<repo-name>-issue-<#>`
and its `issue-<#>` branch exactly as they are — don't delete, don't
force anything — and report:

- Which issue failed and at which step (rebase conflict / AI-resolve
  attempted and its outcome / post-resolve re-verification failure /
  other).
- The worktree path and branch name, so the user can go inspect and
  resolve it by hand.
- Which issues before it already completed and merged into `main`
  (those stay merged — same "clean checkpoint" reasoning as the
  default loop).

Always state explicitly in the report whether an AI-assisted rebase
resolution was attempted and whether it succeeded — even when the run
as a whole completes successfully. It's a silent step by default and
the user should know it fired.
