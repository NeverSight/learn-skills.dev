---
name: review
description: Review GitHub PRs and track improvements as tasks. Use when user asks to review a PR, check a pull request, says "PR 리뷰해줘", "PR 봐줘", or provides a GitHub PR URL or number. Delegates both the review judgment and comment writing to the `reviewer` agent (run in the background).
argument-hint: "[PR 번호 | PR URL]"
allowed-tools: Agent, Bash(gh:*), Read, TaskCreate, TaskUpdate, TaskList, TaskGet
model: sonnet
effort: low
---

# PR Review

GitHub Pull Request를 리뷰하고, 발견된 개선사항을 task로 관리한다. task로 다루는 이유는 리뷰 결과가 한 번 보고 사라지지 않고 "1번 완료" 같은 후속 지시로 진행 상황을 추적하기 위함이다.

Input: $ARGUMENTS

## 인자 파싱 규칙

- 인자 없음: `gh pr list --limit 20`으로 열린 PR 목록을 표시하고 리뷰할 PR을 선택하게 한다. 사용자가 본인 PR만 보고 싶다고 하면 `--author "@me"`를 추가한다.
- 숫자(예: `108`): 해당 PR을 바로 리뷰한다
- URL(예: `https://github.com/.../pull/108`): URL에서 PR 번호를 추출하여 리뷰한다

## 역할 분담 원칙

리뷰 관련 처리(PR 리뷰 판단, 코멘트 달기 등)는 **항상 별도 에이전트가 담당**한다. 시점·상황과 무관하게 메인 에이전트는 리뷰 관련 실제 작업을 직접 수행하지 않으며, **언제나 사용자 인터랙션에 집중**한다.

- **메인 에이전트**(직접 수행): 인자 파싱, PR 선택, 에이전트 입력 준비, 사용자 확인, 에이전트 디스패치, 결과 보고, task 등록/상태 관리, 승인(approve) 제출(아래 "PR 승인 처리"). 그 외 리뷰 관련 판단·작성은 직접 하지 않는다.
- **별도 에이전트**(항상 위임, 둘 다 `reviewer` 에이전트로 디스패치):
  - PR 리뷰 판단 → `reviewer` 에이전트 (아래 "PR 리뷰")
  - 코멘트 작성 → `reviewer` 에이전트 (아래 "코멘트 요청 처리")
- 위임은 **`Agent` 도구(새 스폰) 또는 `SendMessage`(idle 에이전트 재사용)로** 한다. 서브에이전트는 기본적으로 백그라운드로 돌고 완료 시 알림이 오므로 `run_in_background` 를 명시하지 않는다 — 이 파라미터는 버전/컨텍스트에 따라 제공되지 않으며, 없는데 넘기면 호출이 거부된다. 메인은 호출 직후 사용자 입력 대기/처리로 돌아가고, 완료 알림이 오면 후처리(결과 보고, task 등록/완료)만 진행한다.
- **같은 PR 의 후속 위임은 새 스폰 대신 idle 에이전트에 이어서 시킨다.** 리뷰를 끝낸 `reviewer` 가 `idleReason: available` 알림을 보냈으면, 그 PR 의 후속 작업(수정 커밋 재검증, 코멘트 본문 구성, 재리뷰)은 `SendMessage` 로 그 에이전트에 보낸다 — diff·base 대조·기존 finding·오탐 목록을 이미 갖고 있어 재수집 비용이 없고 판단이 일관된다. 새 `Agent` 스폰은 기존 에이전트가 없거나 종료됐을 때, 또는 여러 코멘트 본문을 동시에 병렬 구성할 때만.
- **GitHub 에 실제 반영하는 제출성 명령(approve, 코멘트 POST/PATCH)은 메인이 실행한다.** 서브에이전트 세션은 사용자에게 권한 프롬프트를 띄울 수 없어 권한 classifier 가 External System Writes 로 차단한다(실측: 2026-08-07 approve, 2026-09-15 comments POST). `reviewer` 에는 판단·라인 검증·본문 구성까지만 맡긴다.
- 사용자 확인이 필요한 단계(코멘트 작성 승인 등)는 메인이 직접 수행하고 에이전트에 위임하지 않는다.

## 실행 절차

### 작업 환경 보존

메인은 입력 준비에 `gh`만 쓰고 작업트리/브랜치를 건드리지 않는다. 에이전트 쪽 규칙(checkout 금지, 격리 worktree, 임시 파일 위치)은 `reviewer` 정의가 단일 출처다.

### 사전 컨텍스트 수집

리뷰 전에 아래를 먼저 확인한다. 기존 의견을 모르고 리뷰하면 같은 지적을 반복하거나 이미 합의된 방향과 충돌하는 의견을 낼 수 있다.

1. `gh pr view <number> --comments`로 PR 본문과 일반 코멘트를 본다
2. `gh api repos/{owner}/{repo}/pulls/<number>/comments`로 라인 단위 리뷰 코멘트를 본다
3. 이미 다른 리뷰어가 지적한 사항은 리뷰에서 중복 제기하지 않고, 필요 시 "기존 코멘트와 동일 의견" 정도로만 언급한다

### PR 리뷰

리뷰 판단은 **항상 `reviewer` 에이전트에게 위임**한다. 메인은 리뷰 판단을 직접 하지 않고 입력 준비와 결과 후처리만 담당하며, 위임 후에는 사용자 입력에 계속 반응한다.

1. `gh pr view <number>`로 PR 상세 정보(제목, 본문, baseRefName)를 확인한다
2. `gh pr diff <number>`로 변경 내용을 가져온다
3. 변경 규모가 매우 크면(파일 수가 많거나 핵심 모듈 포함) 핵심 파일 우선이라는 가이드를 함께 전달한다. lock 파일이나 generated 코드는 빠르게 훑도록 지시한다.
4. **`Agent` 도구로 `reviewer` 서브에이전트(`subagent_type: ysoftman-claude-kit:reviewer`)를 1개 디스패치**한다(백그라운드가 기본). 변경이 커도 분할하지 않는다. 같은 PR 의 재리뷰·후속 커밋 검증은 새 스폰 대신 idle `reviewer` 에 `SendMessage`(위 역할 분담 원칙). 호출 직후 메인은 사용자 입력 대기/처리로 돌아간다(리뷰 완료를 동기적으로 기다리지 않는다). prompt에 다음을 포함:
   - PR 번호와 제목
   - 변경된 diff 전체
   - PR 본문/설명 (의도 컨텍스트)
   - **base 브랜치(baseRefName)와 head SHA** — `reviewer`가 PR 무관 여부를 base 대조로 판정하는 데 쓴다
   - 사전 컨텍스트 수집 단계에서 확인한 기존 코멘트 (중복 지적 방지)
   - 프로젝트 컨벤션(CLAUDE.md 규칙: bun/rg/fd/biome/rumdl 등) 위반 여부도 체크 항목에 포함
   - 사용자가 "꼼꼼히"/"전체" 리뷰를 요청한 경우에만 "🟢 포함"을 prompt 에 명시한다. 보고 기준(실패 시나리오, verdict, 검증 게이트, 8개 상한)은 `reviewer` 정의가 담당하므로 반복하지 않는다.
5. 서브에이전트 완료 알림이 오면 반환된 리뷰 결과(🔴 높음 / 🟡 중간 + `확정`/`추정` verdict + PR 변경 영향이 아닌 것만 `[PR 무관]`으로 표시된 findings)를 받는다.
6. 받은 결과 본문은 사용자에게 그대로 표시하고, 아래 "코멘트 요청 처리"의 게시 기준을 충족하는 항목(확정 🔴, 추정 🔴, 확정 🟡)을 한 줄로 짚어 준 뒤 "개선사항 task 등록"을 진행한다

### 개선사항 task 등록

같은 PR을 다시 리뷰하는 경우, 기존 task를 일괄 삭제하지 않는다. 사용자가 이미 "완료/스킵" 처리한 항목까지 리셋되면 진행 상태 추적이 끊기기 때문이다. 다음과 같이 병합한다:

1. `TaskList`로 기존 task를 가져와 subject로 매칭한다
2. 이번 리뷰에도 동일한 항목이 남아 있으면 기존 task를 그대로 둔다(상태 보존)
3. 이번 리뷰에서 새로 발견한 항목만 `TaskCreate`로 추가한다(번호는 기존과 충돌하지 않게 이어 부여)
4. 변경/삭제로 더 이상 해당 없는 기존 task는 `TaskUpdate status=skipped`로 처리한다(삭제하지 않고 흔적을 남긴다)

리뷰에서 발견된 개선사항을 TaskCreate로 등록한다. **🔴/🟡 상세 finding 만 등록**하고, 🟢(꼼꼼히 리뷰에서만 나옴)와 상한 초과 요약분(`그 외 🟡 N건`)은 등록하지 않는다. 우선순위와 verdict 는 **`reviewer`가 분류한 값을 그대로 반영**한다. 분류 기준의 단일 출처는 `reviewer` 에이전트 정의(Methodology)이며, 스킬은 기준을 중복 기술하지 않는다.

- subject 형식: `#번호 우선순위 · verdict — 제목` — PR 변경에서 비롯된 항목은 마커 없이 표기한다. PR 변경 영향이 아닌 항목만 verdict 뒤에 `[PR 무관]`을 붙인다.
  - 예: `#1 🔴 높음 · 확정 — retry 루프에서 context 취소 확인 누락`
  - 예: `#2 🟡 중간 · 추정 [PR 무관] — 기존 add() 락 부재 (이 PR과 무관, 참고용)`
- description에 실패 시나리오, 근거(`file:line`), 개선 방안을 기술한다. `[PR 무관]`이면 base 대조로 확인된 "기존부터 존재" 근거도 함께 적는다.
- **`[PR 무관]` task는 이 PR의 머지 조건이 아니다.** PR 코멘트로 다는 것보다 별도 이슈/추후 처리가 적절하므로, 사용자에게 보고할 때 이를 구분해 안내한다(예: "PR 무관 항목은 참고용이며 이 PR에서 고칠 필요는 없습니다").

### 상태 업데이트

리뷰 결과는 task로 추적하므로 **별도의 표는 출력하지 않는다**. 진행 상황은 task 목록으로 확인한다.

- 사용자가 "1번 완료", "2번 스킵" 등으로 지시하면 해당 Task를 `TaskUpdate`로 상태 변경만 한다(completed / skipped 등).
- 상태 변경 후에는 어떤 task를 어떤 상태로 바꿨는지 한 줄로 간단히 확인해 준다(표 재출력 없음).

### PR 승인 처리

사용자가 승인(approve)을 지시하면 **메인이 직접** `gh pr review <number> --approve`를 실행한다. 서브에이전트에 위임하지 않는다 — 서브에이전트 세션은 사용자에게 권한 프롬프트를 띄울 수 없어 권한 classifier가 외부 반영 동작을 차단한다(실측: 2026-08-07 approve 위임 실패). approve 제출은 리뷰 판단이 아니라 기계적 제출이므로 역할 분담 원칙의 위임 대상이 아니다.

- body는 붙이지 않는다(외부에 보이는 본문은 사용자 확인을 거친 것만 게시).
- 제출 후 `gh pr view <number> --json reviewDecision`으로 APPROVED를 확인해 보고한다.
- 머지는 CLAUDE.md 절대 규칙대로 수행하지 않고 웹 UI에서 진행하도록 안내한다.

### 코멘트 요청 처리

사용자가 특정 이슈에 대해 PR 코멘트를 요청하면, **실제 코멘트 작성은 `reviewer` 에이전트에게 위임**한다. 메인은 코멘트 작성에 묶여 있지 않고 사용자 입력을 계속 대기/처리할 수 있어야 한다.

#### 메인 에이전트의 역할

1. 코멘트 대상(이슈/task 번호, 파일, 라인)을 정한다. 코멘트 본문은 메인이 새로 작성하는 것이 아니라 **`reviewer`가 낸 finding(문제/권장 + suggestion 코드)을 그대로 코멘트 본문으로 구성**한다(메인은 리뷰 내용을 직접 작성하지 않는다 — 역할 분담 원칙). 게시 기준과 접두어는 **심각도 × verdict** 로 정한다:
   - 확정 🔴 → `issue (blocking):` 접두어로 게시
   - 추정 🔴 → `question:` 접두어, 단정하지 않는 질문 문장으로 게시
   - 확정 🟡 → `suggestion (non-blocking):` 접두어로 게시 후보 (🟡 정의가 실발생/자기 계약 위반으로 좁혀져 있어 suggestion 유무는 형식만 결정)
   - 추정 🟡 → task 로만 추적, 사용자가 지정할 때만 `question:` 으로 게시
   사용자가 항목을 직접 지정하면 기준과 무관하게 그 항목을 진행한다(접두어는 verdict 에 맞춰 붙인다).
2. **코멘트 작성 전 사용자에게 내용을 확인받는다.** 작성된 코멘트는 다른 협업자에게 즉시 보이므로 되돌리기 비용이 크다. 이 확인 단계는 메인이 직접 수행한다(서브에이전트에게 위임하지 않는다).
3. 사용자가 승인하면 **`reviewer` 에 라인 검증과 최종 본문 구성을 넘긴다** — idle `reviewer` 가 있으면 `SendMessage`, 없으면 `Agent` 스폰(백그라운드가 기본). **게시(POST)는 넘기지 않는다** — 서브에이전트는 권한 차단으로 실패한다(역할 분담 원칙). 호출 직후 메인은 즉시 사용자 입력 대기/처리로 돌아간다.
4. `reviewer` 가 검증된 `path`/`line`(또는 `start_line`/`line`)/`side` 와 본문 파일 경로를 반환하면 **메인이 게시**한다:

   ```bash
   gh api repos/{owner}/{repo}/pulls/<n>/comments -F body=@<file> -F commit_id=<headSha> \
     -F path=<path> -F line=<line> -F side=RIGHT [-F start_line=<start> -F start_side=RIGHT]
   ```

   대문자 `-F body=@<file>` 만 사용한다(소문자 `-f` 는 `@file` 을 펼치지 않아 경로 문자열이 게시됨 — 실측 사고 2026-09-14). 게시 후 응답 `.body` 첫 줄을 승인 본문과 대조하고, 불일치면 같은 id 에 `-X PATCH -F body=@<file>` 로 정정한다. `reviewer` 가 승인 본문을 보정했으면(라인 번호 정정, suggestion 생략 등) 보정 요지를 한 줄로 알리고 게시한다 — **지적 내용 자체가 바뀐 경우에만** 게시 전 재확인을 받는다. 결과(코멘트 URL 또는 실패 사유)를 사용자에게 간단히 보고하고, 실패 시 재시도 여부를 확인한다.
5. **코멘트가 특정 task(개선사항)에 대응하고 작성이 성공하면, 해당 Task를 `TaskUpdate status=completed`로 변경**한다. 코멘트 작성이 실패했으면 task 상태는 그대로 둔다(성공한 코멘트만 완료 처리).
6. 여러 코멘트를 한 번에 요청받으면, 본문 구성을 독립 서브에이전트로 동시에 디스패치한다. 각 서브에이전트가 반환할 때마다 메인이 개별 게시하고 대응 task를 완료 처리한다(전체가 끝날 때까지 기다리지 않는다).

#### `reviewer`에 전달할 prompt 내용

- PR 번호와 repo(owner/repo)
- 코멘트 대상 파일 경로, line 또는 `start_line`/`line` 범위
- 승인된 코멘트 본문(`reviewer` finding 기반)과 접두어(`issue (blocking):` / `question:` / `suggestion (non-blocking):`)
- suggestion 적용 시 대체 코드

본문 구성의 구체 규칙(suggestion 우선, line 검증, checkout 금지, 본문 파일·반환 형식 등)은 **`reviewer` 에이전트 정의(`kit` 플러그인의 `agents/reviewer.md`)의 "코멘트 작성 위임" 섹션을 단일 출처**로 한다. 게시 명령과 게시 후 검증은 위 4번(메인 담당)이 단일 출처다. 스킬은 구성 규칙을 중복 기술하지 않으며, 위 입력만 전달하면 `reviewer`가 자신의 규칙대로 처리한다.

## 사용 예시

- `/review` — 열린 PR 목록 표시 후 선택
- `/review 108` — PR #108 바로 리뷰
