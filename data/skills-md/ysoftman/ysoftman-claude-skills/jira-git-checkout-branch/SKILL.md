---
name: jira-git-checkout-branch
description: Pick one of the user's In Progress Jira issues and create/checkout a git branch named after it. Use when the user says things like "jira 이슈로 브랜치 만들어", "내 지라 이슈 기반으로 브랜치 파줘", "jira issue branch", or `/jira-git-checkout-branch`. If the working tree is dirty, asks the user whether to proceed; halts if the Atlassian MCP server is not available.
allowed-tools: mcp__atlassian__getAccessibleAtlassianResources, mcp__atlassian__searchJiraIssuesUsingJql, Bash(git:*)
model: sonnet
effort: low
---

# Jira → Git Checkout Branch

현재 사용자에게 할당된 Jira "In Progress" 이슈 중 하나를 골라, 해당 이슈 키로 시작하는 git 브랜치를 생성하고 체크아웃한다.

## 핵심 원칙

- **실행 전 안전 점검을 먼저** 한다: MCP 미연결 상태에서는 브랜치를 만들지 않는다. dirty working tree 인 경우 사용자에게 진행 여부를 묻고, 허용했을 때만 진행한다.
- 브랜치 이름은 **이슈 키로 시작**하고, **영어 소문자 + 하이픈**으로만 구성한다 (ASCII only).
- 브랜치 이름은 **최대 50자**, 단어 경계에서 자른다 (단어를 중간에 자르지 않는다).
- 브랜치를 만들기 전에 **사용자에게 이름을 미리 보여주고 확인**을 받는다.

## 워크플로우

### Step 1. 작업 디렉터리 상태 확인

`git status --porcelain` 을 실행한다.

- 출력이 비어 있으면 정상. 다음 단계로 진행한다.
- 출력이 비어 있지 않으면 변경된 파일 목록을 보여주고 **사용자에게 그대로 진행할지 묻는다**. 변경사항을 자동으로 stash/commit 하지 않는다.

확인 메시지 예:

```text
작업 디렉터리에 커밋되지 않은 변경사항이 있습니다.
이 상태로 새 브랜치를 생성/체크아웃하면 변경사항이 새 브랜치로 함께 옮겨집니다.

변경된 파일 목록:
- A  staged.txt   (staged)
- ?? untracked.txt (untracked)

그대로 진행할까요? (y/N)
```

- `y`/`Y`: 다음 단계로 진행한다.
- 그 외(엔터 포함): 중단하고, 변경사항을 커밋/stash 한 뒤 다시 시도하라고 안내한다.

### Step 2. Atlassian MCP 가용성 확인

`mcp__atlassian__*` 도구가 사용 가능한지 확인한다. deferred tool 목록에 있으면 `ToolSearch`로 `getAccessibleAtlassianResources`, `searchJiraIssuesUsingJql` 스키마를 로드한다.

MCP 서버에 접근할 수 없으면 **즉시 중단**한다.

```text
Atlassian(Jira) MCP 서버가 연결되어 있지 않아 이슈를 조회할 수 없습니다.
MCP 설정을 확인한 뒤 다시 시도하세요.
```

### Step 3. Cloud ID 조회

`getAccessibleAtlassianResources` 를 호출해 Cloud ID와 사이트 URL(`https://<site>.atlassian.net`)을 가져온다.

### Step 4. 이슈 검색

`searchJiraIssuesUsingJql` 로 다음 JQL을 실행한다. 현재 사용자는 JQL `currentUser()`가 자동으로 해석하므로 별도의 accountId 조회가 필요 없다.

```jql
assignee = currentUser() AND status = "In Progress" ORDER BY updated DESC
```

- fields: `summary, status, issuetype, updated, priority`
- maxResults: 20

결과가 0건이면 사용자에게 In Progress 이슈가 없음을 알리고 JQL을 조정할지 (예: status 조건 확장) 묻는다.

### Step 5. 번호가 매겨진 이슈 목록 표시

각 이슈 키는 `https://<site>.atlassian.net/browse/<KEY>` URL 로 마크다운 링크를 건다.

| # | Issue Key | Summary | Priority | Updated |
|---|-----------|---------|----------|---------|
| 1 | [PROJ-123](https://<site>.atlassian.net/browse/PROJ-123) | Fix login error on mobile | Medium | 2026-04-13 |

출력 후 `생성할 브랜치의 번호를 입력하세요.` 로 안내한다.

### Step 6. 사용자 선택

사용자가 번호를 입력하면 해당 이슈를 선택한다. 범위를 벗어나면 다시 요청한다.

### Step 7. 브랜치 이름 생성

포맷: `<ISSUE-KEY>-<kebab-case-summary>`

규칙:

1. `<ISSUE-KEY>` 는 원본 대소문자를 유지한다 (예: `PROJ-123`, `FOO-7`).
2. summary는 다음 순서로 가공한다.
   1. 한국어 등 비ASCII summary는 **영어로 간결하게 번역**한다. 의미를 보존하되 필요 없는 세부(예: 제공자 목록 전체)는 버리고 동사 구문 위주로 3~6단어로 압축한다.
      - 예: "CI 파이프라인에서 자바스크립트 테스트가 타임아웃되는 문제 수정" → `fix ci js test timeout`
   2. 모두 **lowercase** 로 바꾼다.
   3. 공백과 특수문자(영숫자/하이픈 외)는 하이픈으로 바꾸고, 연속 하이픈을 하나로 합친다. 양끝 하이픈은 제거한다.
   4. 숫자 안의 `.`(버전 등)도 하이픈으로 바꾼다 (예: `1.5.4` → `1-5-4`).
3. 전체 길이가 **50자를 넘으면** 단어 경계에서 잘라 50자 이하로 맞춘다. 절대로 단어 중간에서 자르지 않는다.
4. ASCII 범위만 허용한다. 남은 비ASCII 문자는 제거하거나 번역한다.

예시:

| Issue | Summary | 생성된 브랜치명 |
|---|---|---|
| `PROJ-123` | Release 1.5.4 - modernize stack and upgrade dependencies | `PROJ-123-release-1-5-4-modernize-stack-and-upgrade` (50자) |
| `PROJ-7` | Add OAuth2 login flow with Google GitHub LinkedIn Apple Microsoft Facebook providers ... | `PROJ-7-add-oauth2-login-flow` (28자) |
| `XYZ-456` | CI 파이프라인에서 자바스크립트 테스트가 타임아웃되는 문제 수정 | `XYZ-456-fix-ci-js-test-timeout` (31자) |

### Step 8. 사용자 확인 후 브랜치 생성

제안한 이름을 보여주고 확인을 받는다.

```text
이 이름으로 브랜치를 생성할까요? (Y/n, 또는 수정할 이름 입력)
> XYZ-456-fix-ci-js-test-timeout
```

- `Y`/`y`/엔터: 진행.
- `n`: 중단.
- 임의 문자열: 그 문자열을 브랜치명으로 사용한다(단, 규칙 1~4를 다시 검증하고 위반하면 사용자에게 알린다).

확인되면:

1. `git rev-parse --verify --quiet <branch>` 로 이미 존재하는지 검사한다.
   - exit 0 (이미 존재): 사용자에게 기존 브랜치로 체크아웃할지 묻는다.
   - exit 1 (없음): 다음 단계로.
2. `git checkout -b <branch>` 로 새 브랜치를 만들고 체크아웃한다.
3. `git status` 로 현재 브랜치와 작업 트리 상태를 확인하고 사용자에게 알린다.

```text
브랜치 `XYZ-456-fix-ci-js-test-timeout`이 생성되었고, 현재 해당 브랜치에 체크아웃된 상태입니다.
```

## 엣지 케이스

- **현재 디렉터리가 git 저장소가 아님**: `git rev-parse --is-inside-work-tree` 가 실패하면 사용자에게 알리고 중단한다.
- **In Progress 이슈 0건**: 사용자에게 알리고 다른 상태(예: `To Do`, `In Review`)도 포함할지 묻는다.
- **이슈 summary가 비어 있음**: 이슈 키만으로 브랜치를 만든다 (`<ISSUE-KEY>-no-summary` 같은 placeholder는 쓰지 않는다).
- **브랜치 생성 후 사용자가 취소를 원함**: `git checkout -` 로 이전 브랜치로 돌아가는 방법을 안내한다 (명령을 자동 실행하지 않음).

## 왜 이렇게 하는가

- dirty working tree 상태에서 브랜치를 만들면 변경사항이 새 브랜치로 끌려와서 예상과 다르게 섞일 수 있다. 그래서 자동으로 진행하지 않고 사용자에게 확인을 받는다 — 의도적으로 작업 중 변경을 새 브랜치로 가져가려는 경우도 있기 때문에 강제 중단 대신 명시적 동의를 받는 방식으로 보호한다.
- 브랜치 이름을 이슈 키로 시작시키면 PR/커밋 로그에서 이슈 추적이 쉬워지고, CI에서 키 추출 규칙도 단순해진다.
- 50자 제한은 터미널 프롬프트/PR UI에서 잘리지 않고 표시되는 실용적인 상한이다. 단어 경계에서 자르는 것은 가독성을 위해서다.
- 미리보기 후 확인을 강제하는 이유: 브랜치명은 리모트에 push 되면 남고, 이름만 바꾸는 작업도 협업 맥락에선 성가시기 때문이다.
