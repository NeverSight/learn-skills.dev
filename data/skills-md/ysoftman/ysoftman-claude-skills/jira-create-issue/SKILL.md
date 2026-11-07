---
name: jira-create-issue
description: Create or edit Jira issues on boards the user has access to. Use this skill whenever the user asks to create, add, file, open, write, or edit a Jira issue/ticket/task, mentions `/jira-create-issue`, `jira 이슈 생성`, `지라 이슈 만들어`, `이슈 수정`, or asks to "티켓 올려줘", even when the project or issue key is not stated explicitly — the skill will infer the project from conversation context or present accessible boards for the user to pick. Always trigger this over generic jira lookup when the intent is to create or modify an issue.
allowed-tools: mcp__atlassian__getAccessibleAtlassianResources, mcp__atlassian__getVisibleJiraProjects, mcp__atlassian__getJiraProjectIssueTypesMetadata, mcp__atlassian__createJiraIssue, mcp__atlassian__editJiraIssue, mcp__atlassian__getJiraIssue, mcp__atlassian__getTransitionsForJiraIssue, mcp__atlassian__transitionJiraIssue, Bash(git rev-parse:*), Bash(pwd), Bash(basename:*)
model: sonnet
effort: low
---

# Jira Create / Edit Issue

사용자의 발화나 대화 맥락으로부터 Jira 이슈를 생성하거나 수정한다. 제목은 영어, 본문은 한국어를 기본으로 하며, 생성/수정 전에 반드시 미리보기를 보여주고 사용자 확인을 받는다.

## 핵심 원칙

- **제목은 영어**, **본문은 한국어**. 제목은 `[ProjectName] English summary` 형식.
- **미리보기 → 확인 → 실행** 순서를 지킨다. 사용자의 "네/진행/OK" 류 확정 응답 없이는 API를 호출하지 않는다.
- 프로젝트를 확신할 수 없을 때 추측하지 말고 사용자에게 접근 가능한 프로젝트 목록을 보여주고 선택받는다.
- 누락된 정보(본문, 이슈 유형 등)는 합리적으로 채우되, 미리보기에서 드러나게 표시해 사용자가 교정할 수 있게 한다.

## 워크플로우

### 1. 의도 파악

먼저 "생성"인지 "수정"인지 판별한다.

- 수정: 발화에 이슈 키(`PROJ-123` 형태)가 있거나 "수정/업데이트/바꿔"가 포함된 경우
- 생성: 그 외 (기본값)

### 2. Cloud ID 확보

`getAccessibleAtlassianResources`로 Cloud ID를 조회한다. 실패 시 사용자에게 Atlassian MCP 서버 연결 상태를 확인해 달라고 안내하고 중단한다.

### 3. 프로젝트 결정

우선순위에 따라 프로젝트를 결정한다.

1. 사용자가 발화에 프로젝트 키·이름을 직접 준 경우 → 그대로 사용
2. 이슈 키에서 추출할 수 있으면 → 그 프로젝트
3. 최근 대화 맥락에 단일 프로젝트가 뚜렷이 언급된 경우 → 그것을 **제안**하되 미리보기에서 사용자에게 확인 받는다
4. 그 외 → `getVisibleJiraProjects`로 목록을 가져와 **번호와 함께** 보여주고 선택받는다

목록을 표시할 때는 각 프로젝트의 **보드 URL**도 함께 보여준다. URL 형식은 `https://<site>.atlassian.net/jira/software/projects/<KEY>/boards` (site 는 `getAccessibleAtlassianResources` 응답의 `url`에서 추출).

목록 표시 예:

```text
접근 가능한 프로젝트:
  1. Backend Platform (BP)  — https://<site>.atlassian.net/jira/software/projects/BP/boards
  2. Data Pipeline (DP)     — https://<site>.atlassian.net/jira/software/projects/DP/boards
  3. Mobile App (MA)        — https://<site>.atlassian.net/jira/software/projects/MA/boards
어느 프로젝트에 생성할까요?
```

### 4. 제목 생성

형식: `[RepoName] English summary`

- `RepoName`은 **현재 작업 중인 저장소/디렉터리 이름**이다. Jira 프로젝트 이름이 아니다.
  - `git rev-parse --show-toplevel` 의 basename 을 우선 사용한다.
  - git 저장소가 아니면 `pwd` 의 basename 을 사용한다.
  - 사용자가 발화에서 저장소/모듈 이름을 명시한 경우 그것을 우선한다.
- 영어 요약은 발화/맥락에서 추출해 **동사로 시작**하고 60자 이내로 간결하게 쓴다. (`Add`, `Fix`, `Investigate`, `Refactor`, `Deploy` 등)
- 사용자가 제목을 직접 제공했으면 그대로 존중하되, 한국어로 주면 영어로 번역하고 대괄호 접두사를 붙인다.

#### 예시

| 발화 / 컨텍스트 | 제목 |
|---|---|
| `repo=api-server`, "로그인 에러 수정 이슈 만들어줘" | `[api-server] Fix login error` |
| `repo=payments`, "결제 모듈 리팩토링 태스크 추가" | `[payments] Refactor payment module` |
| `repo=mobile-app`, "iOS 앱 크래시 조사" | `[mobile-app] Investigate iOS app crash` |

### 5. 본문 작성

본문은 **한국어**로 작성한다. 사용자가 직접 제공한 내용이 있으면 우선 사용한다. 없으면 대화 맥락에서 추출해 아래 섹션 중 해당되는 것만 채운다.

```text
## 배경
<왜 이 이슈가 필요한지>

## 작업 내용
- <해야 할 일 1>
- <해야 할 일 2>
```

맥락이 부족해 본문을 비우는 게 나은 경우, 본문을 "TBD" 한 줄로 두고 미리보기에서 사용자가 채울 수 있게 안내한다. 추측으로 본문을 부풀리지 않는다.

### 6. 이슈 유형 결정

`getJiraProjectIssueTypesMetadata`로 해당 프로젝트의 이슈 유형을 가져온다. 발화에서 단서("버그", "태스크", "스토리")가 있으면 매핑하고, 없으면 **Task**를 기본값으로 제안한다. 미리보기에 표시해 사용자가 바꿀 수 있게 한다.

### 7. 미리보기 출력

생성 직전에 미리보기를 **어시스턴트 응답(마크다운)으로 직접 출력**한다. `printf`나 Bash 도구로 출력하지 않는다 — 도구 출력으로 들어가면 사용자가 ctrl+o로 전문을 펼쳐야만 보이기 때문이다. 아래 형식으로 응답 본문에 그대로 쓴다:

```text
**📋 Jira 이슈 미리보기**

- **프로젝트**: Backend Platform (BP) — https://<site>.atlassian.net/jira/software/projects/BP/boards
- **이슈 유형**: Task
- **제목**: [Backend Platform] Fix login error
- **생성 후 상태**: In Progress (자동 전이)

> ## 배경
> 사용자가 특정 조건에서 로그인 시 500 에러를 받고 있음.
>
> ## 작업 내용
> - 에러 로그 수집
> - 재현 경로 확인
> - 원인 수정
```

그 뒤 "이대로 생성할까요? (네 / 수정할 내용 입력)" 안내문을 이어서 표시한다.

사용자가 "네"라고 하면 생성한다. 수정 요청이 오면 반영 후 다시 미리보기를 출력한다.

### 8. 생성 실행

`createJiraIssue`를 호출한다. 생성 직후 **In Progress 상태로 전이**한다(기본 상태 규칙).

1. `getTransitionsForJiraIssue`로 사용 가능한 전이 목록을 가져온다.
2. 이름이 `In Progress`(대소문자 무시) 또는 한글로 `진행 중`/`진행중`에 해당하는 전이를 찾는다.
3. `transitionJiraIssue`로 해당 전이 ID를 적용한다.
4. 전이 실패 시 이슈는 생성된 상태로 두고, 전이 실패 사유를 그대로 전달한다.

성공하면 이슈 키·상태·URL을 짧게 알려준다.

```text
생성됨: PROJ-123 (상태: 진행 중) — https://<your-site>.atlassian.net/browse/PROJ-123
```

실패 시 에러 메시지를 있는 그대로 보여주고 원인을 짧게 해석해 준다(예: 필드 누락, 권한 부족).

## 수정 (Edit) 플로우

1. 이슈 키를 확보한다. 없으면 사용자에게 묻는다.
2. `getJiraIssue`로 현재 상태를 읽고 요약해서 보여준다.
3. 변경할 필드(제목/본문/이슈 유형 등)를 결정한다.
4. **변경 전 → 변경 후** 미리보기를 **어시스턴트 응답(마크다운)으로 직접 출력**한다. `printf`나 Bash 도구를 쓰지 않는다(ctrl+o 없이 화면에 바로 보이도록):

```text
**✏️ 수정 미리보기 (BP-482)**

- **제목**
  - 변경 전: [Backend Platform] Fix login error
  - 변경 후: [Backend Platform] Fix login 500 error on mobile
- **본문**: (변경 없음)
```

그 뒤 "이대로 수정할까요? (네 / 추가 수정)" 안내문을 이어서 표시한다.

5. 확인되면 `editJiraIssue`로 적용한다.

## 엣지 케이스

- **MCP 연결 실패**: Atlassian MCP 서버 연결 상태를 확인해 달라고 안내하고 중단한다.
- **프로젝트 접근 권한 없음**: `getVisibleJiraProjects` 결과가 비면 그 사실을 알리고 관리자 문의를 안내한다.
- **사용자가 본문을 비워달라고 요청**: 그대로 존중하고 본문을 빈 값 또는 "TBD"로 둔다.
- **영어 요약이 어색해 보일 때**: 미리보기를 보여주고 사용자가 영어 제목을 직접 제시하면 덮어쓴다.
- **이슈 유형 메타 조회 실패**: Task로 시도하되 실패 메시지를 그대로 전달한다.

## 왜 이렇게 하는가

- 제목을 영어로 통일하면 Jira 검색/알림에서 읽기 쉽고, 다국적 팀과 이력 공유가 쉽다.
- 본문은 한국어로 두어 한국어 사용자가 쓰는 시간을 줄인다.
- 미리보기 후 확인을 강제하는 이유: Jira 이슈는 생성되면 알림이 팀에 퍼지고 지우기도 애매하므로 되돌리기 비용이 높다.
- 프로젝트 추론을 느슨히 하지 않는 이유: 잘못된 프로젝트에 티켓이 들어가면 담당자가 놓치기 쉽고, 이관 작업이 성가시다.
