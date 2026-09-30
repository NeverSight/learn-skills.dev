---
name: ai-agents-sdk
description: This skill should be used when the user asks to build or adapt an OpenAI Agents SDK app, create an agent prototype, add tools or handoffs, connect a Codex workflow to an agent, or add focused agent evals. It does not apply to generic prompt writing or ordinary OpenAI API debugging.
metadata:
  source: "Adapted from the installed OpenAI Agents SDK skill"
---

# AI Agents SDK

OpenAI Agents SDK 기반 에이전트 앱을 가장 작은 실행 가능한 형태로 만들고, 실제 경로를 검증한다. 현재 SDK 동작은 공식 문서를 먼저 확인한다.

## 시작 전

- 대상 레포의 README, 의존성, 진입점, 기존 도구와 eval 구조를 확인한다.
- 에이전트 목표, 입력·출력, 도구, 상태, 승인 경계를 한 문장 또는 짧은 계약으로 정리한다.
- 실행·테스트 전에 `OPENAI_API_KEY`가 필요한지 확인하고, 키 값을 읽거나 출력하거나 커밋하지 않는다.
- 현재 Agents SDK 문서와 Agent Evals 문서를 확인한다. 관련 OpenAI 문서 스킬이 있으면 사용하고, 없으면 공식 문서를 직접 확인한다.

## 구현 원칙

- 처음에는 에이전트 하나로 시작한다. 전문가·handoff·다중 에이전트는 실제 요구가 확인된 뒤 추가한다.
- 도구는 결정적이고 범위를 좁게 설계하며 입력 스키마와 부작용을 명확히 한다.
- 파일·셸 접근이 꼭 필요한 경우에만 sandbox를 사용한다.
- 프로젝트의 기존 패키지 매니저와 실행 규칙을 따른다.
- 로컬 smoke 명령, 샘플 입력, 관찰 가능한 기대 결과를 남긴다.
- 배포는 사용자가 명시적으로 요청한 경우에만 진행한다.

## Evals

- mock 응답이 아니라 실제 에이전트 실행 경로를 검증한다.
- 성공 사례뿐 아니라 근거 부족, 도구 호출 경계, 승인 필요, 상태 변경, 회귀 사례를 포함한다.
- 정확한 문장이나 변동하는 ID보다 구조화된 출력, 도구 호출, handoff, guardrail, 상태 변화를 평가한다.
- 비밀키·개인정보·운영 데이터는 fixture에 넣지 않는다.

## 결과

```md
## 구현 요약

- 에이전트 목표와 변경 내용

## 주요 파일

| 파일           | 역할 |
| -------------- | ---- |
| `path/to/file` | ...  |

## 실행·검증

- 실행 명령
- smoke 또는 eval 결과
- 실행하지 못한 항목과 이유
```

- 설명은 한국어로 작성한다.
- API 키 생성·교체·권한 변경은 이 스킬에서 직접 수행하지 않는다.

$ARGUMENTS
