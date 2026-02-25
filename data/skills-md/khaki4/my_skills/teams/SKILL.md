---
name: teams
description: 문제를 분석하여 Agent Teams를 자동 구성하고, 4가지 조율 패턴(distribute/monitor/discourse/sequence) 중 최적 패턴으로 협업한다. "/teams {문제 설명}"으로 호출한다.
---

# Teams — Agent Teams 자동 구성 및 실행

## Overview

사용자가 제시한 문제를 분석하여 적절한 Agent Teams를 자동으로 구성하고, **4가지 조율 패턴** 중 최적 패턴을 선택하여 결과를 도출하는 편의 스킬이다. 단순 문제는 Agent Teams 없이 직접 해결하고, 복합 문제만 팀을 구성한다.

## When to Use

- 사용자가 `/teams {문제 설명}`을 입력했을 때
- `/teams --pattern {패턴} {문제 설명}`으로 조율 패턴을 지정할 수도 있다
- 멀티 관점 분석, 대규모 구현, 설계 의사결정 등 여러 전문가의 협업이 필요한 문제에 적합

## Prerequisites

- 특별한 전제조건 없음
- 코드 관련 작업 시 해당 프로젝트의 소스 코드 접근 가능 상태

## Error Handling

- 팀 생성 실패 (TeamCreate 에러): 메인 세션에서 단독으로 문제를 해결한다. "Agent Teams 구성에 실패하여 단독으로 처리합니다" 안내
- Lead 생성 실패: 팀 생성 실패와 동일하게 단독 처리
- Teammate 무응답 (10분 이상): 해당 역할을 제외하고 나머지 결과로 진행, 결과에 제외된 역할 명시
- Lead 무응답: 메인 세션에서 단독으로 처리하며 fallback 사유 안내

## Instructions

### 1단계: 문제 분석 및 복잡도 판정

사용자가 제시한 문제를 분석하여 복잡도를 판정한다.

**단순 (Agent Teams 불필요)** — 다음 조건을 **모두** 만족:
- 단일 관점으로 충분 (교차 검증 불필요)
- 변경/분석 범위가 1~2개 파일 이내
- 명확한 정답이 존재 (설계 트레이드오프 없음)

→ 메인 세션에서 직접 해결하고 결과를 출력한다. **이하 단계를 건너뛴다.**

**복합 (Agent Teams 필요)** — 위 조건 중 하나라도 불충족:
- 다관점 분석/교차 검증이 유의미
- 넓은 범위 또는 병렬 작업 가능
- 트레이드오프가 존재하여 토론이 가치 있음

→ 2단계로 진행한다.

### 2단계: 조율 패턴 결정

`--pattern` 옵션이 지정되면 해당 패턴을 사용한다. 미지정 시 문제 유형에서 자동 추론한다.

#### 4가지 조율 패턴

> 이 패턴은 BF Workflow의 Lead 스킬들과 공유한다. Canonical definition: [CLAUDE.md — 조율 패턴](../../CLAUDE.md#조율-패턴)

| 패턴 | 핵심 동작 | 적합한 문제 유형 | BF Lead |
|------|----------|-----------------|---------|
| **distribute** | Lead가 작업을 분배 → 각 agent가 독립 수행 → Lead가 취합 | 병렬 구현, 대규모 리서치, 문서 생성 | bf-lead-plan |
| **monitor** | Lead가 agent를 스폰하고 진행 상황 모니터링 + 에스컬레이션 처리 | TDD 구현, 장시간 작업, 단계적 빌드 | bf-lead-implement |
| **discourse** | 독립 분석 → 교차 검증 → 합의/미합의 분리 | 코드 리뷰, 설계 의사결정, 아키텍처 분석 | bf-lead-review |
| **sequence** | Lead가 단계별로 순차 트리거, 분기만 수행 | 멀티 페이즈 파이프라인, 의존성 체인 | bf-lead-orchestrate |

**자동 추론 규칙:**

| 문제 유형 | 기본 패턴 |
|-----------|----------|
| 코드 리뷰/분석 | discourse |
| 설계 의사결정 | discourse |
| 디버깅/조사 | discourse |
| 구현 (대규모, 병렬 가능) | distribute |
| 구현 (순차 의존성 있음) | monitor |
| 리서치/비교 | distribute |
| 멀티 페이즈 작업 | sequence |

### 3단계: 팀 구성 결정

조율 패턴과 문제 유형에 따라 역할, 인원, 모델을 결정한다. 아래 테이블은 가이드라인이며, 문제 특성에 따라 조정한다.

| 유형 | 인원 | 모델 배당 | 역할 예시 |
|------|------|-----------|-----------|
| 코드 리뷰/분석 | 2~3명 | 전원 opus | Reviewer-A, Reviewer-B, (Convention Guard) |
| 설계 의사결정 | 2~3명 | 전원 opus | Architect-A, Architect-B, (Domain Expert) |
| 디버깅/조사 | 2~3명 | opus + sonnet | Investigator(sonnet), Analyst(opus), (Reproducer(sonnet)) |
| 구현 (대규모) | 3~4명 | Lead opus, Impl sonnet | Lead, Implementer-A, Implementer-B, (Integrator) |
| 리서치/비교 | 2~4명 | 조사 sonnet, 종합 opus | Researcher-A(sonnet), Researcher-B(sonnet), Synthesizer(opus) |

**제약:**
- 최대 teammate 수: **5명** (Lead 포함)
- 분석/리뷰/설계 유형은 교차 검증 품질을 위해 **opus 우선**
- 구현/리서치 유형은 비용 효율을 위해 **sonnet 작업자 + opus 종합자** 패턴

### 4단계: 팀 생성 및 작업 배분

1. **TeamCreate**로 팀을 생성한다 (team_name: `teams-{timestamp}` 형식).

2. **Lead 에이전트를 생성**한다:
   - Task tool로 Lead 생성 (`model: opus`, `subagent_type: general-purpose`)
   - `team_name` 파라미터로 팀에 합류시킨다
   - Lead에게 전달할 정보:
     - 원본 문제 설명
     - 결정된 팀 구성 (역할, 인원, 모델)
     - 각 teammate에게 할당할 작업 내용
     - Discourse 진행 지침 (아래 4단계 참조)

3. **Lead가 teammate를 생성**한다:
   - 각 역할에 맞는 모델로 teammate 생성 (Task tool의 `model` 파라미터 사용)
   - 모든 teammate에게 `team_name` 파라미터로 동일 팀에 합류시킨다
   - TaskCreate로 각 teammate에게 작업을 할당한다

4. 메인 세션은 Lead의 최종 결과만 수신한다 (컨텍스트 보존).

### 5단계: 조율 패턴 실행

선택된 조율 패턴에 따라 Lead가 다른 절차로 진행한다.

#### Discourse 패턴 (리뷰, 설계, 분석)

1. **독립 작업**: 각 teammate가 자신의 할당 작업을 독립적으로 수행한다.
2. **결과 공유**: Lead가 각 teammate의 결과를 수집한다.
3. **교차 검증**: Lead가 결과를 종합하여 teammate들에게 공유하고, teammate끼리 SendMessage로 직접 challenge/agree/보완한다.
4. **합의 판정**: Lead가 합의된 사항과 미합의 쟁점을 분리한다.
5. **최종 종합**: Lead가 결과를 정리하여 메인 세션에 전달한다.

#### Distribute 패턴 (병렬 구현, 리서치)

1. **작업 분배**: Lead가 문제를 독립 단위로 분할하여 각 teammate에게 할당한다.
2. **병렬 실행**: 각 teammate가 독립적으로 작업을 수행한다. (파일 겹침이 없도록 분배)
3. **"done" 수집**: Lead가 각 teammate로부터 완료 신호를 수신한다.
4. **취합 및 통합**: Lead가 결과를 통합하고 불일치가 있으면 조정한다.
5. **최종 결과**: Lead가 통합 결과를 메인 세션에 전달한다.

#### Monitor 패턴 (TDD 구현, 장시간 작업)

1. **agent 스폰**: Lead가 작업 agent를 스폰한다.
2. **진행 모니터링**: 각 agent로부터 "done" 또는 "stuck" 신호를 수신한다.
3. **에스컬레이션 처리**: "stuck" 수신 시 Lead가 판단하여 재시도 또는 접근 전환을 지시한다.
4. **상태 업데이트**: Lead가 진행 상태를 관리한다.
5. **최종 보고**: 모든 agent 완료 후 결과를 메인 세션에 전달한다.

#### Sequence 패턴 (멀티 페이즈 파이프라인)

1. **단계 정의**: Lead가 전체 작업을 순차 단계로 분해한다.
2. **순차 트리거**: 각 단계의 agent를 순서대로 스폰한다.
3. **분기 판단**: 각 단계 완료 신호에 따라 다음 단계를 결정한다.
4. **파이프라인 완료**: 모든 단계 완료 후 결과를 메인 세션에 전달한다.

#### 공통: 쟁점 해소 프로토콜

모든 패턴에서 teammate 간 의견 충돌 시 동일한 프로토콜을 따른다:
1. **Teammate 직접 대화**: SendMessage로 직접 challenge/agree/보완 → 합의 시 Lead에 결론만 보고
2. **미합의 시 Lead 중재**: 프로젝트 방향성 기준으로 판단 → Lead 결정으로 확정
3. **그래도 미합의 → 버린다 (기록)**: 최종 결과에 "미합의 쟁점"으로 포함, 더 이상 토큰을 쓰지 않음

### 6단계: 결과 제시

메인 세션은 Lead로부터 받은 결과를 다음 구조로 사용자에게 출력한다:

```
## 결과 요약

{문제에 대한 핵심 결론 1~3줄}

## 합의 사항

- {팀원 전원이 동의한 결론/권장사항}
- ...

## 미합의 쟁점 (있는 경우)

| 쟁점 | 입장 A | 입장 B | 근거 |
|------|--------|--------|------|
| ... | ... | ... | ... |

## 권장 액션

1. {사용자가 취해야 할 구체적 다음 단계}
2. ...
```

- 합의 사항이 명확하면 미합의 섹션은 생략한다.
- 구현 유형인 경우 코드 변경 사항을 직접 포함한다.

### 7단계: 정리

1. Lead에게 shutdown_request를 보낸다 (Lead가 teammate들을 먼저 shutdown한 뒤 자신도 종료).
2. 모든 teammate 종료를 확인한 뒤 **TeamDelete**로 팀을 삭제한다.

## Fallback

- **팀 생성 실패** (TeamCreate 또는 Lead 생성 에러): 메인 세션에서 단독으로 문제를 해결한다. 사용자에게 "Agent Teams 구성에 실패하여 단독으로 처리합니다"를 알린다.
- **Teammate 무응답** (10분 이상 미응답): 해당 역할을 제외하고 나머지 teammate 결과로 진행한다. 결과에 제외된 역할을 명시한다.
- **Lead 무응답**: 메인 세션에서 단독으로 처리하며 fallback 사유를 알린다.

## Output Format

대화 출력만 생성한다. 별도 파일을 생성하지 않는다.
