---
name: create-ai-tool
description: >
  사용자 요구사항을 분석하여 Skill 또는 Agent 중 적절한 유형을 결정하고 생성을 위임합니다.
  도구 만들기, 스킬 vs 에이전트, 어떤 걸 만들어야 할지, 도구 유형 선택 요청 시 활성화.
---

# AI Tool Creator

사용자 요구사항을 분석하여 Skill 또는 Agent를 결정하고 해당 생성 스킬로 위임합니다.

## 판단 기준

기본은 **Skill**. 아래 조건에 해당할 때만 **Agent**.

| 조건 | YES → Agent | NO → Skill |
|------|-------------|------------|
| 독립 컨텍스트에서 격리 실행 필요? | 대량 출력, 병렬 처리 | 메인 대화에서 충분 |
| 도구 접근을 제한해야? | 읽기 전용, 특정 도구만 허용 | 제한 불필요 |
| 자동 위임으로 독립 작업 수행? | Claude가 판단해서 태스크 위임 | 사용자/Claude가 직접 호출 |

## 의사결정 흐름

```
[요청 분석]
    │
    ├─ 컨텍스트 격리 또는 도구 제한 필요?
    │       │
    │       ├─ YES → Agent → /create-agent
    │       │
    │       └─ NO
    │           │
    │           └─ Skill → /create-skill
    │
    └─ 규칙/컨벤션/가이드라인?
            │
            └─ Skill (user-invocable: false) → /create-skill
```

## 핵심 차이

| 구분 | Skill | Agent |
|------|-------|-------|
| 컨텍스트 | 메인 대화 공유 | 별도 격리 |
| 목적 | 지식/지침/워크플로우 | 태스크 위임 |
| 호출 | `/skill-name` 또는 Claude 자동 | Claude 자동 위임 |
| 도구 제어 | `allowed-tools` | `tools`, `disallowedTools` |
| 규칙/컨벤션 | `user-invocable: false` | 해당 없음 |

## 사용 사례별 라우팅

| 사용 사례 | 유형 | 핵심 설정 | 위임 |
|----------|------|----------|------|
| 코딩 컨벤션, 스타일 가이드 | Skill | `user-invocable: false` | `/create-skill` |
| 단계별 작업 지침 | Skill | 기본값 | `/create-skill` |
| 배포, DB 작업 (부작용) | Skill | `disable-model-invocation: true` | `/create-skill` |
| 코드 리뷰, 디버깅 (격리) | Agent | `tools`, `disallowedTools` | `/create-agent` |
| 병렬 리서치, 대량 분석 | Agent | `model`, `tools` | `/create-agent` |

## 실행

유형이 결정되면 해당 스킬의 내용을 로드하여 생성을 진행합니다:

- **Skill** → [create-skill](skills/create-skill/SKILL.md) 로드
- **Agent** → [create-agent](skills/create-agent/SKILL.md) 로드

## 상세 판단

복잡한 판단이 필요하면 [의사결정 트리](references/decision-tree.md) 참조.
