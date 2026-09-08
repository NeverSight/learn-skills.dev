---
name: autotddreviewfix
description: Multi-model implementation → review → synthesis → re-fix loop, fully unattended per issue. Use when the user says "/autotddreviewfix", "autotddreviewfix #", or gives issue numbers (e.g., `autotddreviewfix 21 22 23 minimax sonnet`). One issue fully finished before the next starts; reviewers within an issue run in parallel. Coupled to harness-project wrappers at /home/user1/git/harness-project/.local/bin/.
---

# autotddreviewfix — multi-model review loop, unattended

Implements a 4-step cycle for each issue number, fully unattended:

1. **Coder MVP** — execution session runs `/autotdd <N>` inline
2. **Reviewers N** — N models (parallel) each write a code review file. If no reviewers are specified, it defaults to a self-review (using a subagent in a new context).
3. **Planner** — execution session synthesizes reviews into a fix plan inline, using the `to-tickets` skill
4. **Coder re-fix** — execution session runs the plan inline using `/autotdd`, and archives review files

Issues run **sequentially**. Reviewers within an issue run **in parallel**.
The coder steps (Step 1 and Step 4), the planner step (Step 3), and re-fix are all handled inline by the executing session.
Pure orchestration — no secrets are held by this skill (see "Coupling to harness-project" below).

## Coupling to harness-project

This skill calls model wrappers that live in `/home/user1/git/harness-project/.local/bin/`.
The wrapper binaries are named `<name>-cli.sh` (where `<name>` is the base model name like `sonnet`, `minimax`, `qwen`, `gemini`, `fable`, `deepseek`, `haiku`, `opus`).

Before starting the run, all specified reviewers must be validated: check if `/home/user1/git/harness-project/.local/bin/<name>-cli.sh` exists and is executable. If any of them are missing or not executable, abort the entire run immediately.

## Argument parsing

Arguments are parsed by positional tokens, categorised by shape (order does not matter):

- **Integer tokens**: Issue numbers (at least one is required, otherwise abort).
- **`worktree`**: Isolation keyword.
- **Other tokens**: Reviewer model names (base names, e.g., `minimax`, `sonnet`).

If no reviewer names are specified, the run defaults to a **self-review**.
Note: The old options (model, coder, reviewers, and planner with double dashes) are completely removed. There is no backward compatibility.

Examples:

- `autotddreviewfix 21` — Runs issue 21 with self-review.
- `autotddreviewfix 21 22 23 minimax sonnet` — Runs issues 21, 22, and 23 sequentially. Reviewers are minimax and sonnet (running in parallel).
- `autotddreviewfix 21 22 23 worktree minimax` — Runs issues 21, 22, and 23 in worktree isolation mode, with minimax as the reviewer.

## cwd validation

Run from inside the target repo (any subdirectory). Verify:

1. `cwd` contains `.git/`
2. `issues/issue-<N>.md` (or the unique tag-less `issues/issue-<N>-<slug>.md` — see `docs/spec/spec-issue-filenames.md`) exists for every requested issue number

If any check fails, abort with a clear message. Same pattern as `/autodev`.

## Per-issue flow

For each issue `N`, in order. Each step's "done check" is file-based — skip the step if the file already exists with non-empty content.

### Step 1 — Coder MVP (skip if done)

**Done check**: `regression-tests/verify-issue-N.sh` exists AND `issues/issue-N.md` has the `## 구현 결과` placeholder replaced with real content (the `(미정)` marker absent).

If not done:
1. **시작 HEAD 기록**: `git rev-parse HEAD`를 `<시작HEAD>`로 기록한다
   (Step 2의 리뷰 대상 범위 산출용).
2. The execution session runs `/autotdd <N>` inline (or `/autotdd <N>
   worktree` if the `worktree` keyword was provided). Wait for it to
   complete.

**리뷰 대상 범위 산출** (Step 1 완료 직후, Step 2 주입용):

- 커밋 범위: `<시작HEAD>..HEAD`
- 변경 파일 목록: `git diff --name-only <시작HEAD>..HEAD`
- worktree 모드: 병합 후 **main 기준**으로 동일하게 산출한다.
- Step 1을 skip한 재실행(멱등 재개)이라 `<시작HEAD>`가 없으면: 커밋
  메시지의 `issue-N:` prefix 관행으로 해당 커밋들을 **역추적**해 같은
  정보를 산출한다.
- 역추적도 실패하면 폴백: 범위 없이 리뷰어에게 맡기지 말고, 이슈 파일과
  회귀 스크립트 경로만이라도 명시하며 범위 산출이 실패했다는 사실을
  프롬프트에 밝힌다 (**침묵 금지**).

### Step 2 — Reviewers (parallel, skip done ones)

파일명 규약의 단일 정본은 `docs/spec/spec-issue-filenames.md`다.

**Done check** (per reviewer `X`): `issues/issue-N__code-review-by-<X>.md` exists and is non-empty (where `<X>` is the base model name, or `self` for self-review — `-by-` 값은 항상 래퍼 base명이며 버전명은 쓰지 않는다).

#### 리뷰어 프롬프트 — 5부 구조 (외부 래퍼·셀프 리뷰 공통)

실행 세션이 아래 5부를 조립해 하나의 프롬프트로 전달한다. 목적은 추측
리뷰의 구조적 차단 — 리뷰 사이클은 티켓 수백 개에 걸쳐 반복되므로 한
번에 다 찾을 필요가 없고, 확실한 것만 잡는 게 중요하다.

**① 환경 사실**:
- 대상 리포의 Python 버전을 `.python-version`에서, 없으면
  `pyproject.toml`의 `requires-python`에서 읽어 프롬프트에 명시한다.
  준수 수준 판정: 버전이 3.12 미만이면 그 버전 준수를 요구하고, 3.12
  초과면 언어 준수 수준을 3.12로 캡한다. (둘 다 없으면 "버전 정보 없음
  — 문법 세대 지적 금지"라고 명시.)
- "이 코드는 이미 code-quality-gate(ruff+pyright+pytest+회귀 스크립트 등)를 통과한 상태"임을
  알린다.

**② 리뷰 범위**: 기계가 못 잡는 것만 — 로직 오류, 스펙(이슈 요구사항)
불일치, 보안(OWASP Top 10 렌즈), 동시성·경계조건. **ruff/pyright가 잡는
스타일·타입 지적은 보고 금지** (파이프라인의 다른 단계 몫).

**③ 증거 계약**: finding마다 필수 3요소 —
- `파일:라인` + 실제 **코드 인용**
- 문제가 재현되는 구체 **실패 시나리오** (입력/상태 → 잘못된 결과)
- **확인 방법** (실행·재현 절차)

그리고 명시: "확인하지 못한 것은 쓰지 마라. 리뷰 사이클은 반복되므로
이번에 다 찾을 필요 없다 — **누락보다 오판이 비싸다**."

**④ 구조화 finding 포맷**: **자유 산문 금지** — finding당 고정 필드
(파일:라인 / 코드 인용 / 실패 시나리오 / 확인 방법 / 심각도 제안
`must-fix`|`tech-debt`)를 표 또는 고정 섹션으로 강제. Step 3 플래너가
기계적으로 판정할 수 있는 형태여야 한다.

**⑤ 리뷰 대상 범위** (Step 1에서 산출한 값을 주입):
- 이슈 파일 경로 (`issues/issue-<N>*.md`) — **스펙 대조**용
- **커밋 범위**와 **변경 파일 목록**
- **회귀 스크립트** 경로 (`regression-tests/verify-issue-<N>.sh`)
- 지시: "리뷰 대상은 이 범위다. **범위 밖** 코드는 이 변경과의 직접
  상호작용(**호출부**·피호출부)이 문제일 때만 언급하라."

공통 유지 지시: 본문 첫 줄에 자기 모델명(버전 포함)을 기입.

#### 실행

For each undone reviewer, launch (모든 `log-cost.sh` 호출은 Windows에서 `.bat`/`.ps1` 동일 인자로 대체 가능 — `bin/log-cost.py`를 감싼다):
- **External Reviewers**: For each reviewer `<X>`, before launching call
  `log-cost.sh --script-id <X> <repo-path> issue-<N> "review-start"` — `<X>`
  자체가 곧 정확한 model 식별자이므로 별도 판단 없이 그대로 쓴다. Then
  launch in parallel:
  ```bash
  /home/user1/git/harness-project/.local/bin/<X>-cli.sh -p "<위 4부 구조로 조립한 프롬프트 — 산출 파일: issues/issue-<N>__code-review-by-<X>.md>"
  ```
  When that reviewer's launch returns, call
  `log-cost.sh --script-id <X> <repo-path> issue-<N> "review-end"`(같은
  `<X>`). 리뷰어별로 개별 start/end 쌍 — N명이면 `cost_details`에
  2N항목.
- **Self-Review**: If no reviewers were specified, before launching call
  `log-cost.sh --script-id <base명> <repo-path> issue-<N> "review-start"` —
  `<base명>`은 **Step 1에서 이미 확정된 `coders.<base명>` 키와 정확히 같은 값**(오케스트레이팅 세션 자신을
  가리킴). 새로 판단하지 말고 그 값을 그대로 재사용한다. Then launch a
  subagent in a new context (do not review inline in the same
  conversation) to write: `issues/issue-N__code-review-by-self.md`.
  셀프 리뷰 서브에이전트의 프롬프트에도 위 4부 구조를 동일하게 적용한다 (모델명 첫 줄 기입 포함).
  서브에이전트가 반환하면 같은 `<base명>`으로
  `log-cost.sh --script-id <base명> <repo-path> issue-<N> "review-end"`를
  호출한다.

Failure of one reviewer does NOT stop the others (continue-with-partial). When all parallel launches return, verify each output file exists and is non-empty. Note any failures for step 3.

### Step 3 — Planner (skip if done)

**Done check**: `issues/issue-N__refix-plan.md` exists and is non-empty.

If not done, first call `log-cost.sh --script-id <base명> <repo-path> issue-<N> "refix-plan-start"` — `<base명>`은 Step 1/Step 2
self-review와 **정확히 같은 값**(오케스트레이팅 세션 자신, 이 단계는
외부 wrapper 없이 실행 세션이 직접 수행하므로 Step 2 self-review와
동일한 base명을 그대로 재사용한다). 그 다음, the execution session
runs inline, in this order:

1. **수집**: Read all available review files matching
   `issues/issue-N__code-review-by-*.md`.
2. **형식 게이트**: finding에 증거 3요소(파일:라인+코드 인용 / 실패
   시나리오 / 확인 방법)가 하나라도 없으면 내용 불문 기계적으로
   `reject` (사유: "증거 미비"). 근거 제시 책임은 리뷰어에게 있다.
3. **분류**: 게이트 통과 finding을 `must-fix` / `tech-debt` /
   `reject`로 분류 (v3 개정 — 구 `good-to-fix` 용어는 `tech-debt`로
   전면 개명).
4. **실질 재검증 (must-fix 한정)**: must-fix 승격 후보는 인용된
   파일:라인을 직접 열어 ① **인용이 실재**하고 ② **주장이 성립**하는지
   확인한 뒤에만 승격한다. 확인 실패 → 근거를 남기고 reject 또는
   tech-debt로 강등 (사유: "재검증 실패"). tech-debt는 파킹되어
   사람 눈을 거치므로 재검증을 생략한다. (비용 비대칭: must-fix 1건은
   무인 `/autotdd` 풀사이클을 발동하므로 오판 비용이 재검증 비용보다
   크다.)
5. **파생 이슈 생성** (`to-tickets` 스킬 활용, 파일명은 규약 v3 + issue-48):
   - **파일명**: 정규화·override·suffix·다중 리뷰어 정렬은 결정성을 위해
     helper `bin/derive_fixing_slug.py`에 위임한다. SKILL.md prose는
     호출 시점·인자만 명시. helper API·CLI 상세는 `bin/derive_fixing_slug.py`
     docstring 참조.
   - **슬러그 도출**: `python bin/derive_fixing_slug.py slug --max-len 50`
     (stdin에 finding 본문) → stdout이 `<finding-slug>`. override 우선,
     자동 추출 fallback.
   - **BY 정렬**: `python bin/derive_fixing_slug.py by --names "<csv>"`
     → stdout이 `<r1>-<r2>-...` (알파벳 정렬, `self` 규칙 적용).
   - **충돌 검사**: `python bin/derive_fixing_slug.py suffix
     --existing "<기존 슬러그 csv>" --slug "<신규>"` → 충돌 시 `-2`,
     `-3` suffix 부여.
   - **파일명 조립** (helper `build_filename(new_n, slug, reviewers,
     tech_debt)` 또는 SKILL.md prose inline):
     - must-fix → `issue-<신번호>-<finding-slug>__must-fix-by-<r1>-<r2>-...md`
     - tech-debt → `issue-<신번호>-<finding-slug>__tech-debt-by-<r1>-<r2>-...md`
   - **원본 이슈 번호는 v3부터 파일명에 넣지 않는다** — 계보(원본 이슈
     번호, 출처 리뷰 파일명, finding 인용, 재검증 결과)는 본문에만
     기록한다.
   - **적용 시점**: 본 v3 개정 이후 생성되는 모든 파생 이슈부터.
     개정 이전 archived 파일(v1 `issue-127-fixing-123.md`, v2
     `__STATE-later__BY-...md` 등)은 **불변** (spec 문서 "레거시 불변" +
     "관행·문법 아님" 섹션의 "레거시 호환" 항목).
   - **중복 finding 규칙** (issue-44): 복수 리뷰어가 같은 결함을 독립
     발견해 승격된 경우 — 파생 이슈는 **1개만** 생성한다(계보에 복수
     리뷰 파일 인용). stats의 must_fix/tech_debt 카운트는 **발견한
     리뷰어 전원**에게 각각 +1. 최초 발견자 개념은 두지 않는다(병렬
     실행이므로 무의미). by 값은 발견한 리뷰어 전원의 base명을 helper
     `by` subcommand로 알파벳 정렬한 결과(예: `__must-fix-by-gemini-qwen-sonnet`).
   - 채번: issues/ + issues/archive/ 전체에서 **최대 번호 + 1** (번호
     재사용 금지). 생성 직전 기존 번호를 재확인한다.
   - 본문 **계보** 필수: 원본 이슈 번호, 출처 리뷰 파일명, 해당 finding
     인용, 재검증 결과.
6. **refix-plan 산출**: `issues/issue-N__refix-plan.md` — 리뷰어별
   finding 수, 분류 결과, reject 사유("증거 미비"/"재검증 실패" 구분),
   생성된 파생 이슈 목록. (Step 3의 done check가 이 파일 기준.)
7. **agent-stats JSON 병합 기록** (issue-43 스코어보드 CLI의 기초 자료):
   같은 판정 데이터를, tdd2가 이미 만들어 둔
   `issues/issue-N__agent-stats.json`(기존 `issue`/`started`/
   `coders` 필드 보존)에 병합 기록한다. 추가하는 필수 필드 —
   `reviewers`(리뷰어 base명 key별: `model` / `findings` /
   `gate_rejected` / `verify_rejected` / `must_fix` / `tech_debt`),
   `derived_by_reviewers`(생성된 파생 이슈 파일명 목록). `.json`은 `.md`
   열거에 걸리지 않으므로 파이프라인에 중립 — 집계는 CLI 몫, 여기서는
   기록만.
   - `reviewers` 각 항목의 `model` 필드는 해당 리뷰 파일
     (`issues/issue-N__code-review-by-<X>.md`) **첫 줄의 버전
     포함 모델명**을 그대로 전사한다. 키는 base명 유지(스코어보드 집계
     단위 불변). 첫 줄에서 모델명을 얻지 못하면 `"unknown"`을 기록한다
     (**침묵 금지** — 필드 누락 금지). 래퍼 뒤 모델이 업그레이드되어도
     stats 한 줄에 전후 이력이 섞이지 않게 한다 (issue-44).
8. **`coders.<base명>.review_outcome` 병합**: 위와 **같은 write 호출**로
   (파일이 하나이므로 별도 read-modify-write가 아니다), 같은
   `issues/issue-N__agent-stats.json`의 `coders.<base명>.review_outcome`을
   채워 넣는다.
   - 키 `<base명>`은 기존 `coders`의 키(tdd2가 생성한 키)를 그대로 사용하며, 새 coder를 추가하지 않는다.
   - `review_outcome` 스키마 (`ts`는 tdd2와 동일한 타임스탬프 규약 —
     로컬 타임존 오프셋 포함, UTC `Z` 금지):
     ```json
     "review_outcome": {
       "ts": "<ISO8601, 로컬 오프셋 포함>",
       "findings_received": <이 리뷰어로부터 받은 총 finding 수>,
       "must_fix_count": <이 리뷰어의 finding 중 실질 재검증을 통과해 파생 이슈로 생성된 must-fix 수>,
       "tech_debt_count": <이 리뷰어의 finding 중 tech-debt 분류 수>,
       "refix_plans_written": <이 이슈 사이클에서 플래너가 refix-plan을 작성했으면 1, 리뷰 파일이 없어 작성하지 못했으면 0>
     }
     ```
   - 만약 리뷰 파일이 하나도 없어 refix-plan 자체를 작성하지 못하는 예외 상황인 경우, `review_outcome.refix_plans_written = 0`과 함께 나머지 수치 필드들을 모두 `0`으로 채워 기록한다.
9. **cost_details 계측 — "refix-plan-end"**: 위 7·8번 write 직후,
   `log-cost.sh --script-id <base명> <repo-path> issue-<N> "refix-plan-end"`를
   호출한다(이 단계 시작 시 쓴 "refix-plan-start"와 정확히 같은
   `<base명>`).

If any reviewer files are missing (from failed reviewers in Step 2), prepend a note in the planning context: "Note: The reviewer file for <failed-reviewer> was unavailable. Synthesize from the surviving files."

### Step 4 — Coder re-fix (skip if done)

**Done check**: every review/refix-plan/agent-stats output file for this
issue (`issue-N__code-review-by-*.md`, `issue-N__refix-plan.md`,
`issue-N__agent-stats.json`) has been moved to
`issues/archive/<YYYY>/<MM>/<DD>/` — 파일명 그대로, `git mv`로.

If not done:
The execution session runs:
- **cost_details 계측 — "refix-start"**: 파생 이슈 처리를 시작하기 전,
  `log-cost.sh --script-id <base명> <repo-path> issue-<N> "refix-start"`를
  호출한다(`<base명>`은 이 이슈의 `agent-stats.json`의 `coders` 키 —
  Step 1의 coder와 정확히 동일한 값, 새로 판단하지 않는다). Step 4
  전체를 감싸는 **한 쌍만** 원본 이슈에 남긴다 — 파생 이슈가 여러 개여도
  각 파생 이슈 자신의 mvp 비용은 그 이슈 자신의 `agent-stats.json`에
  tdd2가 별도로 기록하므로 여기서 중복 계측하지 않는다.
- Step 3가 생성한 파생 이슈 중 **pending인 것만**
  (`issues/issue-*__must-fix-by-*.md`) `/autotdd`로 처리한다 (passing
  `worktree` if the original run specified `worktree`).
  `__tech-debt-by-*` 파킹 파생 이슈는 **건드리지 않는다** — 사람이
  `__tech-debt-by-<...>` 마커를 파일명에서 지워 승격할 때까지 대기.
- **cost_details 계측 — "refix-end"**: 파생 이슈 처리가 전부 끝난
  직후, `log-cost.sh --script-id <base명> <repo-path> issue-<N> "refix-end"`를
  호출한다(같은 `<base명>`, "refix-start"와 짝을 이룸).
- 이 이슈의 산출물(code-review들, refix-plan, agent-stats.json)은
  별도로 `git mv`하지 않는다 — 이 이슈에 대해 `aacp`
  (`.claude/skills/aacpd/aacp.sh`)를 호출하면 `issue-N.md`와 함께
  자동으로 아카이브된다(agent-stats.json은 그 과정에서
  `archived`/`duration`도 함께 채워짐 — issue-47).

## Failure policy

- **Issue-level fail-fast**: if step 1 (MVP) fails, skip all remaining steps for that issue and move to next. If step 3 (planner) or step 4 (re-fix) fails, skip remaining and move to next.
- **Step-level continue-with-partial**: in step 2, if some reviewers fail, continue with the survivors and pass that info to the planner so it can account for missing inputs.

When continuing past failures, log the failure clearly in the final summary, but don't abort the overall run unless the failure is structural (e.g., wrapper not found, cwd invalid).

## Idempotency

Every step's "done check" is file-based. Re-running `autotddreviewfix N` after a partial run will skip already-finished steps and resume from where it left off. To force re-do, `rm` the relevant output file(s) first.

## Multi-issue behavior

Issues are processed strictly sequentially: `autotddreviewfix 21 22 23` finishes 21 fully (all 4 steps), then 22, then 23. Within each issue, reviewers run in parallel.

## Output / report

After all issues complete (or fail), emit a summary table:

| Issue | MVP | Reviews | Plan | Re-fix | Status |
|---|---|---|---|---|---|
| 21 | ✓ | 3/3 | ✓ | ✓ | DONE |
| 22 | ✓ | 2/3 (gemini failed) | ✓ (partial input) | ✓ | DONE |
| 23 | ✗ (coder timeout) | — | — | — | FAILED |

## Forbidden

- Do NOT make this SKILL.md hold secrets. All API keys live in the wrappers.
- Do NOT skip the done-check — re-running is the whole point of unattended.
- Do NOT run reviewers serially when they could be parallel (wall time matters).
- Do NOT commit/push/merge to autotdd or harness-project as part of this skill's flow. The coder's own `/autotdd` calls handle that for the issue repo. This skill only manipulates `issues/issue-*.md` files in cwd.
