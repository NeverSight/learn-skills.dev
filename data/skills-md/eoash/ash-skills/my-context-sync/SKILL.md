---
name: my-context-sync
description: 나의 컨텍스트 싱크. Slack, Notion, Gmail, Google Calendar, ClickUp, GitHub에서 정보를 수집하고 하나의 문서로 정리한다. "싱크", "sync", "정보 수집", "컨텍스트 싱크" 요청에 사용.
triggers:
  - "싱크"
  - "sync"
  - "정보 수집"
  - "컨텍스트 싱크"

# 연결 상태 (2026-02-19 기준)
# ✅ MCP 연결됨: Slack (Connectors), Notion (npx @notionhq/notion-mcp-server), ClickUp (Connectors)
# ✅ subagent 권한: Slack + ClickUp "Always allow" 설정 완료 → 병렬 수집 가능
# ✅ 스크립트 연결됨: Gmail, Google Calendar (google_token.json 저장 완료)
# ✅ 스크립트 연결됨: GitHub (GITHUB_PERSONAL_ACCESS_TOKEN은 .claude.json mcpServers에서 읽음)
---

# My Context Sync

흩어진 정보를 한곳에 모아 정리하는 스킬.

Slack, Notion, Gmail, Google Calendar, ClickUp, GitHub에서 최근 정보를 수집하고,
하나의 마크다운 문서로 통합한다.

## 소스 정의

### 소스 1: Slack

| 항목 | 값 |
|------|-----|
| MCP 도구 | `mcp__claude_ai_Slack__slack_read_channel` |
| 수집 범위 | 최근 7일 |

수집할 채널 목록:

```yaml
channels:
  - name: "general"          # 전체 공지
  - name: "team-operation"   # 팀 운영
  - name: "random"           # 자유 채널
```

수집 방법:
```
각 채널에 대해 mcp__claude_ai_Slack__slack_read_channel 호출.
채널명과 메시지 개수(limit)를 전달한다.

mcp__claude_ai_Slack__slack_read_channel(channel="general", limit=50)
```

추출할 정보:
- 중요 공지사항
- 의사결정 사항 ("확정", "결정", "합의" 키워드)
- 나에게 멘션된 메시지
- 답장이 필요한 질문

---

### 소스 2: Gmail

| 항목 | 값 |
|------|-----|
| 실행 방법 | Python 스크립트 (Gmail API) |
| 수집 범위 | 최근 7일, 받은편지함 |

수집 방법:
```bash
uv run python .claude/skills/my-context-sync/scripts/gmail_fetch.py --days 7
```

추출할 정보:
- 안 읽은 이메일 수
- 중요 발신자 이메일 요약
- 회신이 필요한 이메일
- 일정 초대 (캘린더 연동)

---

### 소스 3: Google Calendar

| 항목 | 값 |
|------|-----|
| 실행 방법 | Python 스크립트 (Google Calendar API) |
| 수집 범위 | 오늘 ~ 7일 후 |

수집 방법:
```bash
uv run python .claude/skills/my-context-sync/scripts/calendar_fetch.py --days 7
```

추출할 정보:
- 오늘의 일정
- 이번 주 주요 미팅
- 준비가 필요한 미팅 (발표, 외부 미팅 등)
- 일정 충돌 여부

---

### 소스 4: Notion

| 항목 | 값 |
|------|-----|
| MCP 도구 | Notion MCP (`mcp__notion__API-post-search`) |
| 수집 범위 | 최근 업데이트된 페이지 및 태스크 |

수집 방법:
```
mcp__notion__API-post-search 호출로 최근 수정된 페이지를 조회한다.

mcp__notion__API-post-search(
  sort={"direction": "descending", "timestamp": "last_edited_time"},
  page_size=20
)
```

추출할 정보:
- 진행 중인 태스크
- 기한이 임박한 항목
- 최근 업데이트된 페이지

---

### 소스 5: ClickUp

| 항목 | 값 |
|------|-----|
| MCP 도구 | `mcp__claude_ai_ClickUp__clickup_search` |
| 수집 범위 | 나에게 할당된 태스크 |

수집 방법:
```
mcp__claude_ai_ClickUp__clickup_search 호출.
진행 중이거나 기한 임박한 태스크를 조회한다.

mcp__claude_ai_ClickUp__clickup_search(query="", assignee="me", status="in progress")
```

추출할 정보:
- 진행 중인 태스크
- 기한 임박 태스크 (3일 이내)
- 최근 댓글이 달린 태스크
- 차단된(blocked) 태스크

---

### 소스 6: GitHub

| 항목 | 값 |
|------|-----|
| 실행 방법 | Python 스크립트 (GitHub REST API) |
| 수집 범위 | 최근 7일, 내 활동 |

수집 방법:
```bash
GITHUB_PERSONAL_ACCESS_TOKEN=<token> python C:/Users/ash/.claude/skills/my-context-sync/scripts/github_fetch.py --days 7
```

토큰 위치: `.claude.json` → `mcpServers.github.env.GITHUB_PERSONAL_ACCESS_TOKEN`

추출할 정보:
- 열린 PR (리뷰 요청 포함)
- 내가 관여한 이슈
- 최근 커밋 내역
- 머지된 PR

---

## 실행 흐름

이 스킬이 트리거되면 아래 순서로 실행한다.

### 1단계: 병렬 수집

7개 소스를 **동시에** 수집한다. 서로 의존성이 없으므로 병렬 실행이 가능하다.

```
수집 시작
  ├── [소스 1] Slack 채널 메시지 수집         ─┐
  ├── [소스 2] Gmail 이메일 수집               │
  ├── [소스 3] Google Calendar 일정 수집       ├── 병렬 실행
  ├── [소스 4] Notion 페이지/태스크 수집       │
  ├── [소스 5] ClickUp 태스크 수집             │
  └── [소스 6] GitHub 활동 수집               ─┘
수집 완료
```

각 소스 수집은 subagent(Task 도구)로 실행한다:

```
Task(description="Slack 수집",    prompt="general, team-operation, random 채널에서 최근 7일 메시지를 수집하라")
Task(description="Gmail 수집",    prompt="gmail_fetch.py를 실행하여 최근 7일 이메일을 수집하라")
Task(description="Calendar 수집", prompt="calendar_fetch.py를 실행하여 7일간 일정을 수집하라")
Task(description="Notion 수집",   prompt="최근 수정된 페이지와 진행 중 태스크를 수집하라")
Task(description="ClickUp 수집",  prompt="나에게 할당된 진행 중 및 기한 임박 태스크를 수집하라")
Task(description="GitHub 수집",   prompt="github_fetch.py를 실행하여 최근 7일 활동을 수집하라")
```

### 2단계: 결과 통합

수집된 정보를 하나의 문서로 합친다.

통합 규칙:
- 소스별 섹션으로 구분
- 각 섹션에서 "하이라이트" (중요 항목 3개 이내)를 선별
- 액션 아이템을 문서 하단에 모아서 정리
- 수집 실패한 소스는 "수집 실패" 표시와 함께 사유 기록

### 3단계: 문서 저장

결과 파일을 저장한다.

```
저장 위치: .claude/skills/my-context-sync/sync/YYYY-MM-DD-context-sync.md
```

### 4단계: 리포트

실행 결과를 사용자에게 보고한다.

```
싱크 완료!

수집 결과:
  Slack:           3개 채널, 47개 메시지
  Gmail:           12개 이메일 (안 읽음 5개)
  Calendar:        8개 일정
  Notion:          15개 페이지
  ClickUp:         7개 태스크
  GitHub:          4개 PR, 12개 커밋

하이라이트 3건:
  1. [Slack] #team-operation: 배포 일정 확정
  2. [Gmail] 파트너사 계약서 회신 필요
  3. [GitHub] PR #42 리뷰 요청 대기 중

액션 아이템:
  - [ ] 파트너사 계약서 회신
  - [ ] GitHub PR #42 리뷰
  - [ ] ClickUp 기한 초과 태스크 처리

파일 저장: .claude/skills/my-context-sync/sync/2026-02-19-context-sync.md
```

## 출력 포맷

<!-- Block 4에서 "Markdown 파일만" 선택됨 (2026-02-19) -->
출력 방식: **Markdown 파일** — `sync/YYYY-MM-DD-context-sync.md`에 저장

저장 경로: `.claude/skills/my-context-sync/sync/YYYY-MM-DD-context-sync.md`

저장되는 마크다운 파일의 구조:

```markdown
# Context Sync - YYYY-MM-DD

> 자동 수집 시각: HH:MM

## 하이라이트

- **[소스]** 내용
- **[소스]** 내용
- **[소스]** 내용

## Slack
...

## Gmail
...

## Google Calendar
...

## Notion
...

## ClickUp
...

## GitHub
...

## 액션 아이템

- [ ] 항목 1
- [ ] 항목 2
```
