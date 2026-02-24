---
name: connector
description: 스마일게이트 업무 도구(Slack, Jira, Confluence, BISKIT, API Docs)를 Claude Code에 연결하는 설정 가이드. 비개발자도 따라할 수 있도록 단계별로 안내한다. "커넥터", "connector", "MCP 설정", "jira 연결", "confluence 연결", "slack 연결", "biskit 연결", "비스킷 연결", "apidocs 연결", "api docs 연결" 요청에 사용.
triggers:
  - "커넥터"
  - "connector"
  - "커넥터 설정"
  - "MCP 설정"
  - "jira 연결"
  - "confluence 연결"
  - "slack 연결"
  - "biskit 연결"
  - "비스킷 연결"
  - "biskit mcp"
  - "apidocs 연결"
  - "api docs 연결"
  - "apidocs mcp"
  - "스마일게이트 커넥터"
---

# Smilegate Connector

스마일게이트 업무 도구를 Claude Code에 연결하는 설정 스킬.
비개발자도 따라할 수 있도록 단계별로 안내한다.

## 연결 대상

| 서비스 | 연결 방식 | 난이도 |
|--------|----------|--------|
| Slack | Connectors (클릭만) | 쉬움 |
| Jira | MCP (토큰 발급 필요) | 보통 |
| Confluence | MCP (토큰 발급 필요) | 보통 |
| BISKIT | MCP (토큰 발급 필요) | 보통 |
| API Docs | MCP (인증 불필요, 클릭만) | 쉬움 |

## 실행 흐름

이 스킬이 트리거되면 아래 순서로 진행한다.

**링크 출력 규칙**: 모든 URL은 코드 블록 밖에서 마크다운 링크 형식 `[텍스트](URL)` 으로 표시한다. 코드 블록 안에 URL을 절대 넣지 않는다. 코드 블록 안의 URL은 클릭이 불가능하고 줄바꿈이 발생할 수 있다. 단, JSON 설정 예시의 URL 값은 설정값이므로 코드 블록 안에 표기한다.

### Phase 0: 현재 연결 상태 진단

스킬 시작 시 먼저 현재 연결 상태를 진단한다.

확인 방법:
1. ToolSearch로 `+slack read` 검색 → Slack 도구 존재 여부 확인
2. ToolSearch로 `+jira test` 검색 → Jira MCP 존재 여부 확인. 도구가 있으면 `mcp__jira__test_jira_connection()` 호출로 실제 연결 확인
3. ToolSearch로 `+confluence test` 검색 → Confluence MCP 존재 여부 확인. 도구가 있으면 `mcp__confluence__test_confluence_connection()` 호출로 실제 연결 확인
4. ToolSearch로 `+biskit check_auth` 검색 → BISKIT MCP 존재 여부 확인. 도구가 있으면 `mcp__biskit-report-mcp__check_auth_status()` 호출로 실제 연결 확인
5. ToolSearch로 `+apidocs search` 검색 → API Docs MCP 존재 여부 확인. 도구가 있으면 연결됨 (인증 불필요이므로 도구 존재 = 연결 성공)

진단 결과를 테이블로 보여준다:

| 서비스 | 상태 |
|--------|------|
| Slack | ✅ 연결됨 / ❌ 미연결 |
| Jira | ✅ 연결됨 / ⚠️ 재연결 필요 (토큰 만료 등) / ❌ 미연결 |
| Confluence | ✅ 연결됨 / ⚠️ 재연결 필요 / ❌ 미연결 |
| BISKIT | ✅ 연결됨 / ⚠️ 재연결 필요 / ❌ 미연결 |
| API Docs | ✅ 연결됨 / ❌ 미연결 |

- ✅ 연결됨: 도구 존재 + 연결 테스트 성공
- ⚠️ 재연결 필요: 도구는 존재하지만 연결 테스트 실패 (토큰 만료, 토큰 오류 등)
- ❌ 미연결: 도구 자체가 없음 (MCP 설정 없음)
- API Docs는 인증이 불필요하므로 ✅(연결됨)과 ❌(미연결) 두 가지 상태만 존재한다.

이미 연결된 서비스(✅)는 건너뛴다. ⚠️ 또는 ❌ 상태의 서비스만 설정을 진행한다.
모두 ✅이면 "모든 서비스가 연결되어 있습니다!"를 출력하고 기본 사용법을 안내한 뒤 종료한다.

설정이 필요한 서비스(⚠️/❌)가 있으면 AskUserQuestion으로 설정할 서비스를 선택받는다:
- question: "어떤 서비스를 설정할까요? (여러 개 선택 가능)"
- options: ⚠️/❌ 상태의 서비스만 동적으로 표시
  - {label: "Slack", description: "Slack 채널 읽기/검색 (클릭 몇 번이면 끝)"}
  - {label: "Jira", description: "Jira 이슈 조회/생성/관리 (토큰 발급 필요)"}
  - {label: "Jira ⚠️ 재연결", description: "토큰 만료 또는 오류 — 토큰을 다시 발급받아 연결합니다"}
  - {label: "Confluence", description: "Wiki 페이지 조회/검색 (토큰 발급 필요)"}
  - {label: "Confluence ⚠️ 재연결", description: "토큰 만료 또는 오류 — 토큰을 다시 발급받아 연결합니다"}
  - {label: "BISKIT", description: "게임 데이터 리포트 조회 (토큰 발급 필요)"}
  - {label: "BISKIT ⚠️ 재연결", description: "토큰 만료 또는 오류 — 토큰을 다시 발급받아 연결합니다"}
  - {label: "API Docs", description: "SGP API 명세 검색 (인증 불필요, 바로 설치)"}
- multiSelect: true
- 해당 상태의 서비스만 옵션에 표시한다 (예: Jira가 ❌이면 "Jira"만, ⚠️이면 "Jira ⚠️ 재연결"만)

#### 분기 흐름

선택 결과에 따라 아래와 같이 진행한다:
- **Slack만 선택** → Phase 1 → Phase 5
- **API Docs만 선택** → Phase 2 → Phase 5
- **MCP 서비스만 선택** (Jira/Confluence/BISKIT) → Phase 3 → Phase 5
- **API Docs + MCP 서비스 선택** → Phase 2 → Phase 3 → Phase 5
- **Slack + API Docs 선택** → Phase 1 → Phase 2 → Phase 5
- **Slack + MCP 서비스 선택** → Phase 1 → Phase 3 → Phase 5
- **Slack + API Docs + MCP 서비스 선택** → Phase 1 → Phase 2 → Phase 3 → Phase 5

### Phase 1: Slack 연결 (Connectors)

Slack 설정 가이드에 따라 진행한다. → [references/slack.md](references/slack.md)

완료 확인 후:
- 연결 성공 시:
  - API Docs를 선택했으면 Phase 2로 이동한다.
  - MCP 서비스(Jira/Confluence/BISKIT)를 선택했으면 Phase 3으로 이동한다.
  - API Docs도 MCP 서비스도 선택하지 않았으면 Phase 5로 이동한다.
- 연결 실패 시: Slack 가이드의 트러블슈팅 진행 → 진전 없으면 Phase 4(이슈 등록) → Phase 5로 이동한다.

### Phase 2: API Docs 연결 (인증 불필요)

API Docs 설정 가이드에 따라 진행한다. → [references/apidocs.md](references/apidocs.md)

완료 후:
- MCP 서비스(Jira/Confluence/BISKIT)를 선택했으면 Phase 3으로 이동한다 (재시작은 Phase 3 이후에 한 번만).
- MCP 서비스를 선택하지 않았으면 재시작 안내 후 Phase 5로 이동한다.

### Phase 3: MCP 연결 (Jira / Confluence / BISKIT)

> ⚠️ Jira, Confluence, BISKIT MCP는 **사내망 또는 VPN 연결이 필요**합니다. 연결 상태를 먼저 확인해주세요.

**핵심 원칙**: 선택한 MCP 서비스(Jira/Confluence/BISKIT)를 모두 한 번에 설정하고, **재시작은 딱 한 번**만 한다. (API Docs는 Phase 2에서 이미 처리되었으므로 여기서는 다루지 않는다.)

토큰 발급 → 전체 입력 → 설정 파일 일괄 저장 → 재시작 → 연결 테스트 순서로 진행한다.

#### Step 1: 선택한 서비스의 토큰 발급 안내 (모두 출력)

선택한 서비스에 해당하는 토큰 발급 안내를 **한 번에 모두** 출력한다.
사용자가 브라우저에서 여러 탭을 열어 한꺼번에 발급받을 수 있도록 안내한다.

각 서비스의 상세 토큰 발급 절차는 해당 가이드를 참조한다:
- Jira 선택 시 → [references/jira.md](references/jira.md)
- Confluence 선택 시 → [references/confluence.md](references/confluence.md)
- BISKIT 선택 시 → [references/biskit.md](references/biskit.md)

#### Step 2: 토큰 전체 입력 (선택한 서비스 모두)

토큰 발급 안내 직후, AskUserQuestion으로 필요한 정보를 순서대로 입력받는다.
**재시작 전에 선택한 모든 서비스의 토큰을 한 번에 입력받는다.**

각 서비스의 토큰 입력 AskUserQuestion 스펙은 해당 가이드를 참조한다:
- 사용자 ID 질문 (Jira/Confluence 중 하나라도 선택한 경우):
  - question: "사용자 ID를 입력해주세요 (Jira/Confluence 공통, 예: hyuntkim)"
  - options: [
      {label: "직접 입력하기", description: "사용자 ID를 입력하세요"},
      {label: "잘 모르겠어요", description: "Jira 또는 Confluence에 로그인할 때 사용하는 ID입니다"}
    ]
  - "잘 모르겠어요" 선택 시: [Jira 프로필 페이지](https://jira.smilegate.net/secure/ViewProfile.jspa) 또는 [Confluence 프로필 페이지](https://wiki.smilegate.net/users/viewmyprofile.action)에서 사용자 이름을 확인할 수 있다고 안내한 뒤, 다시 입력을 요청한다.
- Jira 토큰 입력 → [references/jira.md](references/jira.md)
- Confluence 토큰 입력 → [references/confluence.md](references/confluence.md)
- BISKIT 토큰 입력 → [references/biskit.md](references/biskit.md)

**중요**: 토큰은 민감정보이므로 대화 내용에 그대로 노출하지 않는다.
입력받은 토큰 값의 앞뒤 공백과 줄바꿈을 제거(trim)한 뒤 설정 파일에 저장한다.
대화에서는 마스킹하여 표시한다.

#### Step 3: 설정 파일 일괄 업데이트

Read 도구로 설정 파일을 읽고, `mcpServers` 객체에 **선택한 서비스를 한번에** 추가(신규) 또는 덮어쓰기(재연결)한다.
각 서비스의 MCP 설정 JSON은 해당 가이드를 참조한다:
- Jira → [references/jira.md](references/jira.md)
- Confluence → [references/confluence.md](references/confluence.md)
- BISKIT → [references/biskit.md](references/biskit.md)

추가 후 사용자에게 재시작을 안내한다:

설정 파일의 mcpServers에 {설정한 서비스 목록} 설정이 모두 추가되었습니다!

이제 **Claude Code를 한 번 재시작**하면 모든 서비스가 동시에 연결됩니다:

- **Mac / Linux**: `Ctrl+D` → 터미널에서 `claude` 실행
- **Windows**: `exit` 입력 → 터미널에서 `claude` 실행

재시작 후 `/resume` 을 입력하면 **직전 대화를 이어서** 진행할 수 있습니다.

#### Step 4: 재시작 후 연결 테스트 (선택한 서비스 모두)

사용자가 재시작을 완료했다고 (또는 `/resume`으로 돌아왔다고) 알려주면, 선택한 서비스를 **모두** 테스트한다.
각 서비스의 연결 테스트 방법은 해당 가이드를 참조한다:
- Jira → [references/jira.md](references/jira.md)
- Confluence → [references/confluence.md](references/confluence.md)
- BISKIT → [references/biskit.md](references/biskit.md)
- API Docs (Phase 2에서 설치한 경우) → [references/apidocs.md](references/apidocs.md)

연결 실패 시 트러블슈팅 → [references/troubleshoot.md](references/troubleshoot.md)

### Phase 4: 미해결 이슈 등록

트러블슈팅이 진전 없이 막혀있을 때 GitHub 이슈 등록을 제안한다. → [references/troubleshoot.md](references/troubleshoot.md)

이후 Phase 5로 진행한다. (이슈 등록 여부와 관계없이 완료 리포트는 출력)

### Phase 5: 완료 리포트

모든 설정이 끝나면 최종 상태를 요약한다.

**실제 설정한 서비스만** 표시하고, 연결 테스트 결과에 따라 ✅(성공)/❌(실패)를 표시한다.

출력 형식 (코드 블록 없이 마크다운으로):

**스마일게이트 커넥터 설정 완료!**

연결 상태: (설정한 서비스만 표시)
- {서비스명}: ✅ 연결됨 또는 ❌ 연결 실패

기본 사용법: (연결 성공한 서비스만 표시)

서비스별 예시 문구:
- **Slack**: "Slack에서 #general 채널 최근 메시지 보여줘", "Slack에서 '배포' 관련 메시지 검색해줘"
- **Jira**: "나한테 할당된 Jira 이슈 보여줘", "PROJ-123 이슈 상태 알려줘"
- **Confluence**: "최근 업데이트된 Wiki 페이지 보여줘", "'프로젝트 계획' 관련 문서 검색해줘"
- **BISKIT**: "카제나 어제 DAU 알려줘", "에픽세븐 이번 주 매출은?"
- **API Docs**: "결제 관련 API 명세 찾아줘", "사용자 인증 API 스펙 알려줘"

연결 실패한 서비스가 있으면 트러블슈팅 안내를 함께 표시한다.

> 팁: 토큰이 만료되면 "커넥터 설정해줘" 한 마디로 이 스킬을 다시 실행할 수 있습니다.

## MCP 설정 위치

MCP는 항상 **전역 설정 파일**에 추가한다. OS마다 경로가 다르다:

| OS | 설정 파일 경로 |
|------|------|
| Mac / Linux | `~/.claude.json` |
| Windows | `%USERPROFILE%\.claude.json` (예: `C:\Users\hyuntkim\.claude.json`) |

> 전역 설정 파일에 저장하면 모든 프로젝트에서 사용할 수 있다.
> Git 저장소 밖에 있으므로 토큰이 실수로 커밋될 위험이 없다.
