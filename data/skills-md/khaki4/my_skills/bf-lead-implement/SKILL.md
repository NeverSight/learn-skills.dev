---
name: bf-lead-implement
description: Monitor 패턴으로 에픽 내 모든 Story의 구현을 조율한다. 모든 난이도의 Story를 agent에게 위임하고, sprint-status.yaml은 Lead만 갱신한다.
---

# Lead Implement (Monitor Pattern)

## Overview

에픽 내 모든 Story의 TDD 구현을 조율하는 Lead 스킬이다. **모든 난이도의 Story를 agent에게 위임**하고 Lead는 코드를 직접 만지지 않는다. sprint-status.yaml은 이 Lead만 갱신한다 (단일 쓰기 지점).

## When to Use

- `bf-lead-orchestrate`가 에픽 루프에서 스폰
- 직접 호출하지 않는다.

## Prerequisites

- Story 파일: `docs/stories/{TICKET}-story-*.md` (현재 에픽 소속)
- `docs/sprint-status.yaml`
- `docs/conventions.md` (있으면)
- 수정 재실행인 경우: `docs/reviews/{EPIC-ID}-modification.md` (사람의 수정 지시)

## Error Handling

- S/M Story agent 스폰 실패: 1회 재시도 후에도 실패 시 해당 Story를 stuck으로 처리 (`status: in_progress` 설정 후 stuck.md에 "agent spawn failed" 기록, `ralph_stuck: true` 설정). Done 신호에서 `"done (stuck: {STORY-ID})"` 목록에 포함하여 orchestrate가 `skipped`로 처리
- L/XL Story Sub-Lead 스폰 실패: 단독 Sonnet agent로 fallback (S/M과 동일 방식)
- sprint-status.yaml 쓰기 실패: CLAUDE.md의 Read-yq-Verify Recover 절차를 따른다 (git checkout → 1회 재시도 → 실패 시 orchestrate에 `"error: sprint-status update failed"` 보고)

## Instructions

### 1. 초기 로딩

**yq 전제조건 체크** (최초 1회):
```bash
command -v yq >/dev/null 2>&1 || { echo "❌ yq not installed. Install: brew install yq"; exit 1; }
```

- 현재 에픽에 속한 모든 Story 문서를 읽는다.
- `docs/conventions.md`를 읽는다.
- 수정 재실행인 경우: `modification.md`를 읽어 수정 지시와 대상 Story를 확인한다.
- `docs/sprint-status.yaml`을 읽어서 각 Story의 난이도와 상태를 확인한다.
  - `status: done`인 Story는 건너뛴다.
  - `status: todo` 또는 `in_progress`인 Story만 대상으로 한다.

### 1b. Convention 섹션 필터링

conventions.md를 읽은 후, 각 Story에 전달할 관련 섹션을 결정한다.

**Core 섹션 (항상 포함):**
아키텍처, 네이밍, 테스트, 코드 스타일

**Concern-area 섹션 (Story 파일 경로 기반 필터링):**

| Story 파일 경로 패턴 | 포함 섹션 |
|---|---|
| `src/components/`, `src/pages/`, `src/views/`, `src/layouts/`, `src/hooks/`, `*.tsx`, `*.vue`, `*.svelte`, `app/` (Next.js) | UI 패턴 |
| `src/api/`, `src/routes/`, `src/controllers/`, `src/middleware/`, `routes/`, `controllers/`, `server/` | API 패턴 |
| `src/models/`, `src/entities/`, `src/repositories/`, `prisma/`, `migrations/`, `src/db/`, `drizzle/` | DB 패턴 |
| `src/auth/`, `src/security/`, `src/guards/`, `middleware/auth*` | 보안 패턴 |
| `Dockerfile`, `.github/`, `docker-compose*`, `infra/`, `deploy/`, `.env*` | 인프라 패턴 |

**필터링 규칙:**
1. conventions.md에 concern-area 섹션이 없으면 전체 내용을 그대로 전달한다 (하위 호환).
2. Story의 Technical Notes에 변경 대상 파일이 없으면 전체 내용을 전달한다 (안전 fallback).
3. 매칭되는 concern-area 섹션이 있으면, Core 섹션 + 매칭 concern-area 섹션만 추출하여 인라인으로 전달한다.
4. 각 `##` 헤딩부터 다음 `##` 헤딩 전까지를 하나의 섹션으로 취급한다.

**인라인 전달 형식:**
```
[Project Conventions]
아래는 이 Story에 관련된 프로젝트 컨벤션이다. 전체 컨벤션은 Epic 리뷰 시 Convention Guard가 검사한다.

{추출된 섹션 내용}

[Library Reference]
아래는 이 Story 구현에 참고할 라이브러리 API 레퍼런스이다. 프로젝트 컨벤션과 충돌 시 컨벤션을 우선한다.

### {라이브러리명}
{context7에서 조회한 관련 API 문서 발췌}

### {라이브러리명2}
{context7에서 조회한 관련 API 문서 발췌}

(Library Reference는 1c에서 조회. 조회 결과가 없으면 [Library Reference] 섹션 전체를 생략한다)
```

### 1c. Library Reference 조회

conventions.md 필터링 후, 각 Story에 전달할 라이브러리 레퍼런스를 준비한다.

**라이브러리 추출:**
1. Story의 Technical Notes에서 "주요 라이브러리" 항목을 확인한다.
2. 라이브러리가 명시되어 있으면, Story당 **최대 3개**까지 context7로 조회한다.
3. 라이브러리가 명시되어 있지 않으면 이 단계를 건너뛴다.

**context7 조회 절차 (라이브러리당):**
1. `resolve-library-id`로 library ID를 확인한다.
2. `query-docs`로 Story의 AC에 관련된 API 문서를 조회한다.
   - query는 Story의 AC를 기반으로 구성한다 (예: "form validation with zod schema", "server actions with next.js app router")
   - 범용적인 query보다 Story AC에 특화된 query가 효과적이다.
3. 조회 결과에서 **해당 Story AC에 직접 관련된 API/패턴만** 추출한다 (전체 문서 전달 금지).

**Fallback:**
- `resolve-library-id` 실패 (라이브러리 미발견): 해당 라이브러리는 건너뛴다.
- `query-docs` 실패 또는 빈 결과: 해당 라이브러리는 건너뛴다.
- context7 MCP 서버 연결 불가: 전체 단계를 건너뛰고 conventions만 전달한다.
- 모든 fallback은 정상 동작이다. Library Reference는 보충 자료이지 필수 전제조건이 아니다.

### 2. 모델 (orchestrate가 결정)

이 Lead의 모델은 `bf-lead-orchestrate`가 스폰 시 지정한다:
- 에픽 내 L/XL Story 포함 시 Opus
- S/M만이면 Sonnet

### 3. Story Agent 스폰

모든 난이도의 Story를 agent에게 위임한다. Lead는 코드를 직접 만지지 않는다.

#### S/M Story → 단독 Agent (Sonnet)

- Story당 1개의 Sonnet agent를 스폰한다.
- `.ralph-progress/{STORY-ID}.json`이 존재하면 초기 retry_count/approaches_count를 해당 파일에서 읽어 전달한다 (이전 중단 복구 시).
- Agent에게 전달하는 정보:
  - Story 문서 내용 (AC, Technical Notes)
  - conventions 관련 섹션 (1b에서 필터링한 인라인 텍스트)
  - library reference (1c에서 조회한 인라인 텍스트, 있으면)
  - 수정 재실행인 경우: modification.md의 해당 Story 수정 지시 원문
  - Ralph Loop 지침 (아래 "Story Agent용 Ralph Loop 지침" 참조)
  - 기존 retry_count/approaches_count (있으면 — 이전 중단에서 복구된 값)
  - **"sprint-status.yaml을 수정하지 말 것"**
  - **"`"done"` + commit hash + retry_count + approaches_count 또는 `"stuck"` + stuck.md + retry_count + approaches_count로 보고할 것"**

<HARD-GATE>
Story agent는 sprint-status.yaml을 절대 읽거나 수정하지 않는다. 모든 상태 업데이트는 Lead가 "done"/"stuck" 신호를 수신한 후 수행한다. "상태만 빨리 기록하겠다"는 단일 쓰기 지점 원칙을 파괴하는 합리화이다.
</HARD-GATE>

#### L Story → Sub-Lead (Opus) + Implementers (Sonnet)

- Story당 1개의 Opus sub-lead를 스폰한다.
- Sub-lead에게 전달하는 정보:
  - Story 문서 내용
  - conventions 관련 섹션 (1b에서 필터링한 인라인 텍스트)
  - library reference (1c에서 조회한 인라인 텍스트, 있으면)
  - 수정 지시 (있으면)
  - "Sonnet implementer를 스폰하여 구현을 진행하라"
  - "쟁점 해소 프로토콜에 따라 조율하라" (아래 참조)
  - Ralph Loop 지침
  - **"sprint-status.yaml을 수정하지 말 것"**
  - **"`"done"` + commit hash + retry_count + approaches_count 또는 `"stuck"` + stuck.md + retry_count + approaches_count로 보고할 것"**

#### XL Story → Sub-Lead (Opus) + 3+ Teammates

- Story당 1개의 Opus sub-lead를 스폰한다.
- Sub-lead에게 전달하는 정보:
  - Story 문서 내용
  - conventions 관련 섹션 (1b에서 필터링한 인라인 텍스트)
  - library reference (1c에서 조회한 인라인 텍스트, 있으면)
  - 수정 지시 (있으면)
  - "3+ teammates를 스폰하여 구현, 통합, 리뷰 역할을 분담하라"
  - "discourse로 설계 검증 후 구현을 진행하라"
  - "쟁점 해소 프로토콜에 따라 조율하라"
  - Ralph Loop 지침
  - **"sprint-status.yaml을 수정하지 말 것"**
  - **"`"done"` + commit hash + retry_count + approaches_count 또는 `"stuck"` + stuck.md + retry_count + approaches_count로 보고할 것"**

### 4. 병렬 실행 규칙

**디폴트는 병렬이다.** Story 문서의 Technical Notes에서 변경 대상 파일을 확인하고, 아래 순차 조건에 해당하지 않으면 하나의 응답에서 여러 Task tool call을 동시에 보내 병렬 스폰한다.

**순차 실행 조건** (이 조건에 해당할 때만 순차):
- 파일 겹침: 두 Story의 Target files에 동일 파일이 존재
- Dependencies 명시: Story 문서에 다른 Story에 대한 의존성이 명시됨
- 공유 파일 충돌: 아래 파일을 변경하는 Story는 "겹침"으로 간주
  - Lock 파일: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Gemfile.lock`, `poetry.lock`, `go.sum`
  - 공유 설정: `tsconfig.json`, `webpack.config.*`, `vite.config.*`, `.env.*`
  - 자동 생성 파일: `schema.prisma` → `@prisma/client`, DB migration 파일
- Story agent가 lock 파일을 변경해야 하는 경우 (새 의존성 설치 등): 해당 Story를 병렬 그룹에서 분리하여 단독 또는 순차 실행

### 5. 모니터링 루프

sprint-status.yaml 갱신은 CLAUDE.md의 **Read-yq-Verify** 프로토콜을 따른다.

각 Story agent로부터 완료 신호를 수신한다:

**"done" + commit hash 수신 시:**
- sprint-status.yaml 업데이트 (Lead가 직접, `yq -i` 명령어 사용):
  ```bash
  yq -i '
    .<TICKET>.<EPIC>.<STORY>.status = "done" |
    .<TICKET>.<EPIC>.<STORY>.tdd = "done" |
    .<TICKET>.<EPIC>.<STORY>.model_used = "sonnet" |
    .<TICKET>.<EPIC>.<STORY>.ralph_retries = 1 |
    .<TICKET>.<EPIC>.<STORY>.ralph_approaches = 0 |
    .<TICKET>.<EPIC>.<STORY>.ralph_stuck = false
  ' docs/sprint-status.yaml
  ```
  - `model_used`: 실제 사용된 모델 전략 (`"sonnet"` / `"opus-lead"` / `"opus-lead+3"`)
  - `ralph_retries`: agent가 보고한 재시도 횟수
  - `ralph_approaches`: agent가 보고한 접근 전환 횟수

**"stuck" + stuck.md 수신 시:**
- sprint-status.yaml 업데이트:
  ```bash
  yq -i '
    .<TICKET>.<EPIC>.<STORY>.ralph_stuck = true |
    .<TICKET>.<EPIC>.<STORY>.ralph_retries = 3 |
    .<TICKET>.<EPIC>.<STORY>.ralph_approaches = 2
  ' docs/sprint-status.yaml
  ```
- stuck.md를 `docs/reviews/{STORY-ID}-stuck.md`에 저장한다.
- **git commit하지 않는다** — docs/ 산출물은 Phase 4 Archive에서 일괄 커밋한다.
- **다른 Story들은 계속 진행한다** (stuck Story가 있어도 나머지를 중단하지 않음).
- **stuck Story의 `status`는 변경하지 않는다** — orchestrate가 자동 판단 시 `skipped`로 변경한다.

모든 Story가 완료(done 또는 stuck)될 때까지 대기한다.

### 6. Done 신호

모든 Story 완료 후 orchestrate에 보고한다:

**stuck Story 없음:**
- `"done"` + sprint-status.yaml 경로

**stuck Story 있음:**
- `"done (stuck: {STORY-ID}, {STORY-ID})"` + sprint-status.yaml 경로 + stuck.md 경로들

종료 (컨텍스트 소멸).

---

## Story Agent용 Ralph Loop 지침

Story agent에게 전달할 TDD 지침이다. Agent는 이 지침을 그대로 따른다.

### TDD 사이클

<HARD-GATE>
구현 코드를 작성하기 전에 반드시 테스트를 먼저 작성하고 Red(실패)를 확인해야 한다. 테스트와 구현을 동시에 작성하는 것은 TDD 위반이다. "간단하니까 같이 작성해도 된다"는 이 게이트를 우회하는 전형적인 합리화이다.
</HARD-GATE>

1. **단위 테스트 작성** (AC 기반)
2. **Red 확인**: 테스트 실행 → 실패 확인
   - 예상대로 실패하지 않으면 테스트 코드 수정
3. **구현**
4. **Green 확인**: 테스트 재실행 → 통과 확인
   - 실패하면 아래 가드레일에 따라 재시도
5. **리팩토링** (필요 시, Green 유지 확인)
6. **git commit**: `[{TICKET}] {간단한 설명}`
   - **`docs/` 하위 파일은 커밋에 포함하지 않는다** (sprint-status.yaml, story 문서 등 모두 제외)
7. **Lead에 done 보고**: `"done"` + commit hash + `retry_count` + `approaches_count`

### Ralph Loop 가드레일

**a) 최대 재시도 횟수: 5회**
- Green 검증 실패 → 구현 수정 → 재실행을 최대 5회까지 반복한다.
- `retry_count`를 0부터 시작하여 매 실패마다 1 증가.

**b) 반복 실패 감지 (Stuck Detection)**
- 매 실패 시 에러 메시지의 핵심 내용(에러 타입 + 발생 파일)을 기록한다.
- 직전 시도와 동일한 근본 원인의 에러가 연속 2회 발생하면, 접근 방식을 전환한다:
  1. 테스트 코드의 기대값이 잘못되었는지 재검토
  2. AC 해석이 올바른지 Story 파일 재확인
  3. 구현 전략을 근본적으로 변경 (다른 알고리즘/패턴 적용)
- `approaches_count`를 0부터 시작하여 전환 시마다 1 증가.

**c) 진행 상태 파일 기록 (크래시 복구용)**
- 매 재시도 후 `.ralph-progress/{STORY-ID}.json`에 현재 상태를 기록한다:
  ```json
  {
    "retry_count": 2,
    "approaches_count": 1,
    "last_error_type": "TypeError",
    "last_error_file": "src/auth/login.ts"
  }
  ```
- 이 파일은 에이전트 크래시 후 bf-resume이 재개할 때 Ralph Loop 카운트를 복원하는 데 사용된다.
- Story 완료("done") 또는 stuck 보고 후 해당 파일을 삭제한다.
- **sprint-status.yaml은 여전히 수정하지 않는다** — 이 파일은 ralph-progress 전용이다.

**d) 한도 초과 시 → "stuck" 보고**
- `retry_count >= 5`에 도달하면 루프를 즉시 중단한다.
- **stuck.md를 작성한다:**

```markdown
# Stuck 보고서: {STORY-ID}

## 재시도 횟수: {retry_count}/5
## 접근 전환 횟수: {approaches_count}

## 시도한 접근 방식
1. {접근 1} — {에러 요약}
2. {접근 2} — {에러 요약}

## 마지막 에러
{전체 에러 출력}

## 변경된 파일
{변경 파일 목록}
```

- `.ralph-progress/{STORY-ID}.json` 삭제
- Lead에 보고: `"stuck"` + stuck.md 경로
- `retry_count`, `approaches_count`를 함께 보고한다.

### 쟁점 해소 프로토콜 (L/XL Story의 Sub-Lead/Teammates에 적용)

1. **Teammates 직접 대화**: `SendMessage`로 직접 challenge/agree/보완
   - 합의됨 → Sub-Lead에 결론만 보고
2. **미합의 시 Sub-Lead 중재**: 프로젝트 방향성(conventions.md) 기준으로 판단
   - Sub-Lead 결정으로 확정
3. **그래도 미합의 → 버린다 (기록)**: 더 이상 토큰을 쓰지 않음

### Agent Teams 실패 시 Fallback (L/XL)

- Task tool 에러 (agent 생성 실패): 단독 Sonnet agent로 fallback (S/M과 동일 방식)
- Teammate 10분 이상 무응답: 해당 teammate 제외하고 나머지로 진행
- 프로세스 비정상 종료: 단독 Sonnet agent로 fallback

## Output Format

- sprint-status.yaml 업데이트 (이 Lead가 구현 단계의 유일한 쓰기 지점)
- `"done"` 또는 `"done (stuck)"` 신호를 orchestrate에 전달
