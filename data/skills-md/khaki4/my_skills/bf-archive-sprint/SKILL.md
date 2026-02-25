---
name: bf-archive-sprint
description: 스프린트 내 모든 에픽이 완료된 후 스프린트 문서를 아카이빙한다. 문서 이동, git commit을 자동으로 수행한다.
---

# Archive Sprint

## Overview

스프린트가 완료되면 관련 문서를 아카이빙하고, git commit을 수행한다.

## When to Use

- 사용자가 `/bf-archive-sprint`를 입력했을 때
- 스프린트 내 모든 에픽의 E2E가 통과한 후

## Prerequisites

- sprint-status.yaml 존재 및 모든 에픽의 e2e가 terminal state (`passed` | `escalated` | `max-regression-cycles` | `skipped`), 모든 Story `review: approved` (skipped Story 포함 — bf-execute/bf-resume가 사람 "진행" 선택 시 자동 설정)
- `docs/stories/`, `docs/tech-specs/` 디렉토리 존재

## Error Handling

- sprint-status.yaml 미존재: "sprint-status.yaml이 없습니다. `/bf-execute`로 워크플로우를 먼저 실행하세요." 안내
- 미완료 에픽 존재 (e2e가 `pending`): "미완료 에픽이 있습니다: {에픽 목록}. `/bf-execute` 또는 `/bf-resume`으로 먼저 완료하세요." 안내
- Story review가 `approved`가 아닌 경우: "{Story} 리뷰가 미승인입니다. `/bf-execute`에서 에픽 결과를 확인하고 '진행'을 선택하세요." 안내

## Instructions

1. sprint-status.yaml을 확인한다:
   - 모든 에픽의 e2e가 terminal state인지 검증 (`passed` | `escalated` | `max-regression-cycles` | `skipped`). `pending`이면 실행 중단
   - 모든 Story의 review가 `approved`인지 검증
   - 미완료 에픽이 있으면 실행 중단 및 안내

2. 문서를 아카이브 디렉토리로 이동한다:
   - `docs/stories/` → `docs/archive/{TICKET}/stories/`
   - `docs/tech-specs/` → `docs/archive/{TICKET}/tech-specs/`
   - `docs/reviews/` → `docs/archive/{TICKET}/reviews/` (존재하는 경우)
   - `docs/sprint-status.yaml` → `docs/archive/{TICKET}/sprint-status.yaml`
   - `docs/conventions.md` → `docs/archive/{TICKET}/conventions.md` (복사, 이동 아님 — 시점 스냅샷 보존용)

3. git commit을 수행한다:
   - 메시지: `[{TICKET}] 스프린트 아카이빙`
   - 포함 대상: `docs/archive/{TICKET}/` + `docs/conventions.md`
   - **이 커밋이 docs/ 산출물의 최초 git 커밋이다** — Phase 1-3에서는 docs/ 파일을 git에 커밋하지 않으며, 아카이브 시점에 일괄 커밋한다.

4. 완료 후 다음 순서로 후속 스킬 실행을 안내한다:
   - **먼저** `/bf-metrics` (선택 사항): 스프린트 메트릭 분석 → 모델 배당/난이도 태깅 최적화 제안
   - **그 후** `/bf-update-conventions`: 리뷰 패턴 분석 → conventions.md 업데이트
   - 순서가 중요함: bf-metrics 분석 결과가 bf-update-conventions의 개선 방향에 참고될 수 있음

## Output Format

- `docs/archive/{TICKET}/` — 아카이브 디렉토리
- git commit
