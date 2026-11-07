---
name: team
description: Start a temporary agent team for collaborative work. Keep the main agent focused on user interaction, coordination, monitoring, and final integration while delegating independent work to teammates whenever feasible. Use proactively when a task can be split across independent files, modules, or concerns. Also trigger when the user asks to work on multiple things at once, speed up a large task, or mentions "팀", "병렬", "parallel", "동시에", "나눠서".
argument-hint: "[병렬로 처리할 작업 설명]"
allowed-tools: Agent, ListAgents, SendMessage, TaskCreate, TaskUpdate, TaskList, TaskGet, TaskStop, Bash(git status:*), Bash(git diff:*), Bash(rg:*)
---

# Agent Team Mode

병렬 작업을 위한 에이전트 팀을 만들고 관리한다.

Input: $ARGUMENTS

## 런타임

팀을 만들거나 지우는 도구는 없다. 세션에는 **암묵적 팀 하나**만 있고, teammate 는 `Agent` 도구로 만든다.

| 하고 싶은 것 | 방법 |
|---|---|
| teammate 생성 | `Agent` 에 `name` 지정. pane 배치는 `teammateMode` 설정(`tmux`/`iterm2`)이 처리한다 |
| 현재 팀원·상태 확인 | `ListAgents` — 각 행이 busy/idle 을 알려준다 |
| 브리핑·재배정 | `SendMessage({to: "<name>", message: ...})` |
| 완료된 teammate 재사용 | 같은 이름으로 `SendMessage` — 이전 transcript 에서 이어서 깨어난다 |
| teammate 종료 | `TaskStop({task_id: "<name>"})` |
| 작업 추적 | `TaskCreate` / `TaskUpdate`(`owner` 로 배정) / `TaskList` / `TaskGet` |

- `Agent` 의 `team_name` 은 deprecated(무시됨) — 넘기지 않는다.
- 서브에이전트는 기본 백그라운드로 돌고 완료 시 알림이 온다. `run_in_background` 를 명시하지 않는다 — 이 파라미터는 버전/컨텍스트에 따라 제공되지 않으며, 없는데 넘기면 호출이 거부된다.
- teammate 메시지는 자동으로 전달된다. 인박스를 폴링하지 않는다.

## 작업 방침

- **재사용 우선.** `ListAgents` 에 idle 이거나 완료된 teammate 가 있으면 `SendMessage` 로 재브리핑한다. 새로 만들 때는 왜 재사용하지 않는지 응답에 한 줄 밝힌다(역할 불일치, ownership 충돌, 독립 판단 필요 등).
- **메인은 위임에 집중.** 메인의 기본 역할은 사용자 응답, 조율, 모니터링, 최종 통합이다. 파일을 수정하는 요청이면 크기와 무관하게 위임이 기본값 — "간단해 보여서 직접 처리"는 허용하지 않는다. 메인이 직접 맡는 경우는 아래로 한정한다.
  - 한두 문장으로 끝나는 답변, 상태 보고, ownership/backlog 조정
  - teammate 배정 전에 필요한 짧은 탐색이나 범위 정리
  - 실패·충돌·의존성 변경으로 backlog 를 재계획하거나 부분 통합할 때
  - 모든 subtask 가 끝난 뒤의 최종 통합/검증
  - 사용자가 메인 직접 처리를 명시한 경우
- 사용자가 병렬을 명시하지 않아도 독립 subtask 로 나뉘면 팀 사용을 먼저 검토한다. 반대로 "혼자 처리", "팀 쓰지 마", "서브에이전트 쓰지 마" 라고 하면 그 요청이 우선이다.
- 단일 파일 작은 수정이나, 의존성이 강해 병렬화가 오히려 위험한 작업에는 팀을 쓰지 않는다.
- 팀은 **현재 top-level 요청 단위의 임시 팀**이다. 사용자가 "팀 유지", "keep alive", "다음 작업에도 재사용" 을 명시한 경우에만 요청 종료 후 유지한다.

## 실행 절차

### 1. 분해

팀을 만들기 전에 어떻게 나눌지 먼저 정한다. 잘못된 분해가 충돌과 재작업의 원인이므로 이 단계가 가장 중요하다.

| 전략 | 적합한 상황 | 예시 |
|---|---|---|
| 파일/모듈 기준 | 서로 다른 파일을 독립적으로 수정 | API 리팩토링 → routes, controllers, middleware |
| 관심사 기준 | 같은 코드를 다른 관점에서 분석 | 코드 리뷰 → security, performance, test-coverage |
| 파이프라인 기준 | 순차 단계를 병렬 준비 | 배포 준비 → lint 수정 + 테스트 작성 + 문서 업데이트 |

배정 전에 소유권 표를 만든다. 컬럼은 `subtask`, `teammate`, `edit scope`, `no-touch scope`, `done criteria`, `status`(queued / running / done / blocked), `depends on`.

- 같은 파일을 두 명 이상이 수정하면 git 충돌이 난다. 소유권이 겹치거나 불명확하면 배정 전에 메인이 범위를 조정한다.
- 작업량을 균등하게 나눈다. 한 명이 파일 10개, 다른 한 명이 1개면 비효율적이다.
- `teammate` 가 비어 있는 항목은 backlog 로 본다. 메인이 맡는 항목은 `main` 으로 표시하고 직접 처리하는 이유를 남긴다.
- 인자가 비어 있으면 무엇을 병렬화할지 사용자에게 묻는다.

### 2. 배정

subtask 마다 순서대로:

1. `TaskCreate` 로 작업을 만든다
2. `ListAgents` 로 재사용 가능한 teammate 를 찾는다 — 있으면 `SendMessage` 로 새 브리프를 보낸다
3. 없거나 역할상 재사용이 부적절할 때만 `Agent` 로 새로 만든다 (`name` 필수)
4. `TaskUpdate` 로 `owner` 를 해당 teammate name 으로 배정한다

teammate 는 현재 대화 이력을 전혀 공유하지 않는다. 방금 합류한 동료에게 브리핑하듯 아래 구조로 쓴다. 컨텍스트가 부족하면 엉뚱한 방향으로 작업하거나 되묻느라 시간을 버린다.

```text
역할:
목표:            무엇을, 왜
담당 범위:       파일/디렉터리 경로 명시
수정 금지:
필수 사전 확인:  CLAUDE/AGENTS/README/CONTRIBUTING, 관련 issue/PR/설계 문서, 해당 skill 명세
컨벤션:
완료 조건:       어떤 상태가 되면 완료인지
이전 작업 맥락은 무시:   재사용 teammate 인 경우
완료 보고 형식:
```

재사용 teammate 에게는 **이전 작업 맥락을 폐기하고 현재 브리프 기준으로 시작하라**고 명시한다. 이름 변경이 지원되지 않으면 task owner 와 브리프, 최종 보고에 현재 역할명이 드러나게 한다.

### 3. 연속 스케줄링

선행 작업에 의존해 바로 시작할 수 없는 subtask 는 backlog 에 둔다. batch 전체가 끝날 때까지 기다리지 않는다 — 하나가 완료되면 변경 파일, 실패 여부, ownership 충돌 가능성만 짧게 확인한 뒤 backlog 에서 의존성 없는 다음 subtask 를 즉시 `SendMessage` 로 배정한다.

`TaskList`/`TaskGet` 으로 주기적으로 확인해 idle teammate 가 queued subtask 를 두고 놀지 않게 한다. idle teammate 와 queued subtask 가 동시에 있는데 배정하지 않는 것은 예외 상황이므로 충돌·의존성·실패 같은 구체적 이유를 사용자에게 설명한다.

작업 중 들어온 사용자 추가 요청도 backlog 의 새 subtask 로 취급한다. 메인이 직접 처리했으면 위임하지 않은 이유를 응답에 한 줄 명시한다.

선행 subtask 결과가 후속 입력이면 결과 요약과 변경 파일을 `SendMessage` 에 담아 전달한다. 충돌 위험이 있으면 후속을 시작하지 말고 메인이 먼저 통합 판단을 한다.

### 4. 재사용 금지 조건

idle 로 보여도 아래에서는 재사용하지 않는다.

- 직전 작업 **자체가** 실패했고(잘못된 수정, 반복 오류, 지시 불이행) 원인이 정리되지 않은 경우. 단 실패 원인이 작업과 무관한 외부 요인(세션/사용량 한도, 일시적 네트워크·MCP 오류, 런타임 중단)이고 해소가 확인되면 재브리핑 후 재사용 가능하다
- 전문 agent 성격이 크게 달라 이전 시스템/역할 지침이 방해될 수 있는 경우
- 보안 검토, 최종 리뷰처럼 독립 판단이 중요해 이전 맥락 오염이 위험한 경우
- 같은 파일 또는 같은 ownership 범위를 다른 teammate 가 수정 중인 경우
- top-level 요청이 바뀌었고 사용자가 팀 유지를 명시하지 않은 경우
- 사용자가 새 agent 사용, 단독 처리, 또는 팀 비사용을 명시한 경우

### 5. 통합

teammate 는 작업 종료 시 아래 형식으로 보고해야 한다.

```text
상태: done / blocked / failed
변경 파일:
실행한 검증:
남은 리스크:
메인 통합 시 주의점:
```

- 보고를 받으면 **브리프의 모든 항목이 채워졌는지 대조**하고, 누락이 있으면 같은 teammate 에게 잔여 항목만 다시 배정한다.
- 완료 알림만 오고 보고가 없으면 `git diff`/`rg` 로 **실제 파일 상태를 직접 확인**한 뒤 미착수면 재요청한다.
- 최종 보고 전에 `git status`/`git diff` 로 변경 범위를 확인하고 ownership 충돌, 중복 수정, 누락된 후속 작업을 점검한다. 코드가 바뀌었으면 관련 lint/format/test 결과 또는 실행하지 못한 이유를 함께 보고한다.

### 6. 정리

현재 요청의 queued/running subtask 가 모두 끝나면 진행 중 task 가 없는지 확인한 뒤 `TaskStop({task_id: "<name>"})` 으로 teammate 를 종료한다. 진행 중 작업이 있으면 종료하지 않고 대상 teammate 와 남은 작업을 먼저 보고한다.

정리 시점은 대화 흐름을 보고 판단한다. 요청이 끝났어도 **같은 작업 영역의 후속 요청이 올 가능성이 있으면** 그 맥락을 가진 teammate 는 남겨두는 편이 재사용 가치가 높다. 작업 영역이 종료됐거나 사용자가 다른 주제로 넘어갔거나 대화가 마무리된 것으로 보이면 기본값대로 정리한다 — keep-alive 요청이 없는 팀을 무한정 유지하지 않는다.

## 팀 구성 패턴

| 작업 | 구성 |
|---|---|
| 코드 리뷰 (3) | security(취약점·auth·secrets) / quality(복잡도·중복·네이밍·에러 처리) / test-coverage |
| 리팩토링 (모듈 수만큼) | teammate 당 독립 모듈. 모듈 간 인터페이스가 바뀌면 명세를 먼저 합의해 브리프에 넣는다 |
| 기능 개발 (3~4) | backend(API/로직) / frontend(UI) / tester (+ docs 선택) |
| 분석·조사 (2~3) | 같은 코드베이스를 다른 관점에서 보고 메인이 종합한다 |

## 문제 상황

| 상황 | 대응 |
|---|---|
| teammate 작업 실패 | 새로 만들지 말고 `SendMessage` 로 추가 컨텍스트를 주거나 범위를 좁힌다 |
| 파일 충돌 | 한쪽을 먼저 완료시킨 뒤 다른 쪽에 변경된 상태를 `SendMessage` 로 알린다 |
| 작업 간 의존성 발견 | 선행 완료 후 결과와 필요한 정보를 `SendMessage` 로 전달한다 |
| 응답 없음 | `ListAgents` 로 상태 확인 → busy 면 대기, 목록에 없으면 같은 이름으로 `SendMessage`(transcript 에서 재개) |
