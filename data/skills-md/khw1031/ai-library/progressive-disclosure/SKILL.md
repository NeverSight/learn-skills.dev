---
name: progressive-disclosure
description: >
  LLM 컨텍스트 윈도우를 효율적으로 사용하는 3단계 정보 로드 원칙.
  Skills, Agents, Prompts 작성 시 참조.
  SKILL.md, AGENT.md 작성, 프롬프트 설계, 컨텍스트 최적화 시 활성화.
---

# Progressive Disclosure 원칙

> 정보를 필요한 시점에 필요한 만큼만 로드하여 컨텍스트 윈도우를 효율적으로 사용합니다.

## 왜 필요한가

LLM의 컨텍스트 윈도우는 제한된 자원입니다. 모든 정보를 한 번에 로드하면:
- 핵심 내용이 희석됨
- 관련 없는 정보로 성능 저하
- 토큰 비용 증가

Progressive Disclosure는 정보를 3단계로 나누어 **필요할 때만 로드**합니다.

## 3단계 로드 모델

| 단계 | 로드 시점 | 토큰 | 내용 |
|------|----------|------|------|
| 1단계 | 항상 | ~100 | name, description, 트리거 키워드 |
| 2단계 | 활성화 시 | <5000 | 핵심 규칙, 필수 지침 |
| 3단계 | 요청 시 | 무제한 | 예제, 상세 문서, 스크립트 |

## 적용 대상

| 대상 | 1단계 | 2단계 | 3단계 |
|------|-------|-------|-------|
| Skills | frontmatter | SKILL.md 본문 | references/, scripts/ |
| Agents | frontmatter | AGENT.md 본문 | references/, hooks |
| Prompts | 역할 정의 | 핵심 지침 | 예제, 참조 문서 |

## Rule → Skill 변환

> **Rule 대신 Skill 사용을 권장합니다.**

기존 Rule을 Skill로 변환하면 더 유연하고 강력한 기능을 활용할 수 있습니다.

| Rule 사용 의도 | Skill 설정 |
|---------------|-----------|
| 매 세션 자동 적용 | `user-invocable: false` |
| 특정 조건에서만 적용 | description에 트리거 조건 명시 |
| 누락 방지 필요 | core-skills로 그룹화 후 세션 시작 시 트리거 |

**변환 예시:**

```yaml
# Before: Rule (rules/code-style.md)
---
description: 코드 스타일 규칙
paths:
  - "**/*.ts"
---

# After: Skill (skills/code-style/SKILL.md)
---
name: code-style
description: >
  TypeScript 코드 작성 시 적용되는 스타일 가이드.
  코드 작성, 리뷰, 리팩토링 시 자동 참조.
user-invocable: false
---
```

## 표준 디렉토리 구조

```
asset-name/
├── AGENTS.md          # 진입점 - 개요 (Claude 자동 인식)
├── [TYPE].md          # 2단계 - 핵심 지침
├── CLAUDE.md          # AGENTS.md 참조 (선택적, 호환성)
└── references/        # 3단계 - 상세 문서
    └── *.md
```

## 파일별 역할

| 파일 | 역할 | 크기 제한 |
|------|------|----------|
| AGENTS.md | 진입점, Claude 자동 인식 | 최소화 |
| CLAUDE.md | AGENTS.md 참조 (선택적) | 최소화 |
| SKILL.md / RULE.md / AGENT.md | 핵심 지침 | <5000 토큰, <500줄 |
| references/*.md | 상세 문서, 예제 | 무제한 |

## Frontmatter 필수 필드

```yaml
---
name: asset-name          # 1-64자, 소문자/숫자/하이픈
description: >            # 무엇 + 언제 사용하는지
  무엇을 하는지 설명.
  어떤 상황에서 사용하는지 트리거 키워드 포함.
---
```

## 핵심 원칙

### 1. 1단계만으로 판단 가능

description만 읽고 "이 자산이 필요한가?"를 판단할 수 있어야 합니다.

```yaml
# 좋은 예
description: >
  코드 리뷰 시 적용되는 품질 기준.
  PR 리뷰, 코드 검토, 품질 점검 요청 시 활성화.

# 나쁜 예
description: 코드 리뷰 규칙
```

### 2. 2단계는 핵심만

- 500줄 / 5000 토큰 이하
- 하나의 관심사에 집중
- 상세 예제는 references/로 분리

### 3. 3단계는 온디맨드

- 명시적 요청 시에만 로드
- 주제별로 파일 분리
- 깊은 중첩 피하기 (1단계 깊이)

## 체크리스트

자산 작성 시 확인:

```
□ 1단계: description이 무엇+언제를 명확히 설명하는가?
□ 1단계: name이 디렉토리명과 일치하는가?
□ 2단계: 본문이 5000 토큰 이하인가?
□ 2단계: 하나의 관심사에 집중하는가?
□ 3단계: 상세 내용이 references/로 분리되었는가?
□ 3단계: 참조 경로가 1단계 깊이인가?
```

## 상세 가이드

각 자산 유형별 상세 적용 방법:

- [Impact 레벨 정의](references/_index.md)
- [Skills 작성 가이드](references/skills.md)
- [Agents 작성 가이드](references/agents.md)
- [Prompts 구조화 가이드](references/prompts.md)
