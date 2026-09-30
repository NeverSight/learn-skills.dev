---
name: skill-router
description: This skill should be used when the user asks to "관련 스킬 찾아줘", "어떤 스킬을 써야 해?", "스킬 후보 보여줘", "이 작업에 맞는 스킬 추천해줘", "스킬 조합을 골라줘", "find relevant skills", "show skill candidates", or "which skills should I use", or asks for a multi-domain implementation such as backend API and frontend integration. It presents up to three skill candidates with their roles and recommended order, then waits for the user's choice. Do not use for simple single-file changes.
---

# Skill Router

복합 작업의 구현 전에 적절한 스킬을 고르는 라우터로 동작한다.

## 절차

1. 현재 Codex 컨텍스트에 표시된 스킬 목록을 확인한다.
2. `scripts/list_skills.py --json`을 실행할 수 있으면 프로젝트와 사용자 스킬의
   `name`·`description`도 확인한다.
3. 요청과 실제 description이 맞는 스킬을 최대 3개 후보로 고른다. 이름만 보고
   역할을 추측하거나 존재하지 않는 스킬을 만들지 않는다.
4. 각 후보의 역할, 적용 이유, 적용하지 않는 범위를 설명한다.
5. 여러 스킬이 필요하면 추천 실행 순서를 제시한다.
6. 사용자가 선택하기 전에는 파일을 수정하거나 구현을 시작하지 않는다.
7. `1`, `1+2`, `전부`, `직접 진행`처럼 선택할 수 있도록 묻고 멈춘다.

## 복합 작업 후보 규칙

- 요청이 백엔드·프론트엔드·API·인프라처럼 두 개 이상의 영역을 포함하면, 현재 컨텍스트에 `orchestration`, `routing`, `coordination`, `multi-agent` 역할의 스킬이 있는지 먼저 확인한다.
- 그런 스킬이 있으면 최대 1개를 후보에 포함하고, 구현 스킬이 아니라 작업 분해·실행 순서·리스크 점검 담당이라고 설명한다.
- 나머지 후보는 실제 도메인 스킬에서 고른다. orchestration 스킬이 현재 목록에 없으면 만들어 내거나 설치된 것으로 추정하지 않는다.
- `Sol Advisor`처럼 설치된 Plugin 스킬은 레포에 복사하지 않아도 현재 컨텍스트에 보이는 경우 후보로 제시할 수 있다.

## 후보 응답 형식

```md
관련 스킬 후보 3개를 찾았습니다.

1. <skill-name>
   역할: <무엇을 하는 스킬인지>
   이유: <현재 요청과 맞는 이유>

2. <skill-name>
   역할: <무엇을 하는 스킬인지>
   이유: <현재 요청과 맞는 이유>

추천 순서: 1 → 2

어떤 조합으로 진행할까요? (`1`, `1+2`, `전부`, `직접 진행`)
```

## 선택 후

- 사용자가 고른 스킬의 `SKILL.md`만 읽고 해당 절차를 적용한다.
- 여러 스킬을 고르면 경계를 유지하고 추천 순서대로 진행한다.
- 후보에 없는 작업은 일반 Codex 절차로 처리한다고 알린다.
- 사용자가 `직접 진행`을 고르면 라우터를 중단하고 일반 작업으로 전환한다.
