---
name: create-agent
description: >
  Claude Code Agent를 생성합니다.
  에이전트 생성, AGENT.md 작성, 새 에이전트 만들기 요청 시 활성화.
---

# Agent 생성

Claude Code Agent를 생성하는 가이드입니다.

## 필수 요소

| 필드 | 설명 | 제약 |
|------|------|------|
| `name` | 에이전트 식별자 | 소문자/하이픈만, 하이픈 시작·연속 불가 |
| `description` | 역할 + 위임 조건 + "Use proactively" | Claude 위임 판단 기준 |

## description 작성 패턴

Claude는 description을 읽고 위임 여부를 판단한다. **What(무엇을 하는지)** + **When(언제 사용하는지)** 모두 포함해야 한다.

```yaml
description: >
  [역할/전문 영역 - What]
  [언제 위임할지 조건 - When]
  Use proactively when/after [트리거 조건].
```

**좋은 예:**
```yaml
description: >
  코드 리뷰 전문가. 품질, 보안, 유지보수성 검토.
  코드 작성/수정 후 사전에 사용.
  Use proactively after code changes.
```

**나쁜 예:**
```yaml
description: 코드를 검토합니다.  # What만 있고 When 없음 → 위임 시점 판단 불가
```

## 생성 단계

### 1단계: 파일 생성

**단일 파일** (간단한 에이전트):

```bash
touch .claude/agents/{name}.md
```

**폴더 구조** (references가 필요한 경우):

```bash
mkdir -p .claude/agents/{name}/references
```

### 2단계: AGENT.md 작성

```yaml
---
name: agent-name
description: >
  역할과 전문 영역 설명.
  언제 위임할지 조건 명시.
  Use proactively when [조건].
tools: Read, Grep, Glob, Bash
---

당신은 [역할] 전문가입니다.

## 호출 시 수행 단계

1. 단계 1
2. 단계 2
3. 단계 3

## 출력 형식

[결과물 형식 정의]
```

## 선택 필드

| 필드 | 용도 | 예시 |
|------|------|------|
| `tools` | 허용 도구 (생략 시 전체 상속) | `Read, Grep, Glob, Bash` |
| `disallowedTools` | 거부 도구 | `Write, Edit` |
| `model` | 모델 선택 | `haiku`, `sonnet`, `opus`, `inherit` |
| `permissionMode` | 권한 모드 | `default`, `acceptEdits`, `dontAsk` |
| `maxTurns` | 최대 에이전틱 턴 수 | `10` |
| `skills` | 시작 시 주입할 스킬 | `[api-conventions, error-handling]` |
| `hooks` | 라이프사이클 훅 | `{PreToolUse: [...]}` |
| `mcpServers` | 사용할 MCP 서버 | `{server-name: {command: "..."}}` |
| `memory` | 영속 메모리 스코프 | `user`, `project`, `local` |

## 도구 제한 패턴

| 패턴 | tools | disallowedTools |
|------|-------|-----------------|
| 읽기 전용 | `Read, Grep, Glob, Bash` | `Write, Edit` |
| 수정 가능 | `Read, Edit, Write, Grep, Glob, Bash` | - |
| 최소 권한 | `Read, Grep, Glob` | - |
| 스폰 제어 | `Task(worker, researcher), Read, Bash` | - |
| 스폰 불가 | `Read, Bash` (Task 생략) | - |

## 모델 선택 가이드

| 모델 | 사용 시점 |
|------|----------|
| `haiku` | 빠른 탐색, 간단한 검색 |
| `sonnet` | 분석, 리뷰, 균형 잡힌 작업 |
| `opus` | 복잡한 추론, 아키텍처 결정 |
| `inherit` | 메인 대화와 동일 (기본값) |

## 체크리스트

```
□ name이 소문자/하이픈만 사용하는가?
□ description이 역할 + 위임 조건을 명확히 설명하는가?
□ description에 "Use proactively" 패턴이 있는가?
□ 필요한 도구만 tools에 명시되었는가?
□ 읽기 전용이면 disallowedTools에 Write, Edit이 있는가?
□ 시스템 프롬프트가 역할과 단계를 명확히 정의하는가?
```

## 상세 가이드

- [Frontmatter 스키마](references/schema.md)
- [템플릿 모음](references/templates.md)
