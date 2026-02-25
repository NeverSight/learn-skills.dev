---
name: bf-update-conventions
description: 스프린트 중 코드 리뷰에서 발견된 반복 패턴을 conventions.md에 반영한다. Convention Guard의 규칙 소스를 축적하여 다음 스프린트의 리뷰 품질을 높인다.
---

# Update Conventions

## Overview

스프린트 완료 후, 코드 리뷰에서 발견된 패턴과 교훈을 docs/conventions.md에 축적한다. conventions.md는 Convention Guard (Open Code Review 기반 리뷰)의 단일 규칙 소스이다.

## When to Use

- 사용자가 `/bf-update-conventions`를 입력했을 때
- `/bf-archive-sprint` 완료 후

## Prerequisites

- 아카이브된 스프린트 존재: `docs/archive/{TICKET}/`
- 아카이브 내 stories, tech-specs 디렉토리 존재
- `docs/archive/{TICKET}/reviews/` 디렉토리 존재 (리뷰 결과 파일) — 미존재 시 git log에서 리뷰 관련 커밋 히스토리를 대안으로 분석
- docs/conventions.md (없으면 신규 생성 — `/bf-spec`이 초기 seed를 생성했어야 하나, 미생성 시 이 스킬이 빈 템플릿으로 생성)
- **권장 실행 순서**: `/bf-archive-sprint` → `/bf-metrics` (선택) → `/bf-update-conventions`. 아카이빙 후 실행해야 리뷰 결과에 접근 가능

## Error Handling

- 아카이브 디렉토리 미존재: "`docs/archive/`가 없습니다. `/bf-archive-sprint`를 먼저 실행하세요." 안내
- 리뷰 파일도 git log도 분석할 데이터가 없으면: "분석할 리뷰 데이터가 없습니다. 스프린트 리뷰 이력이 없으면 건너뛰어도 됩니다." 안내

## Instructions

1. 아카이브된 스프린트의 리뷰 이력을 분석한다:
   - **1차 소스**: `docs/archive/{TICKET}/reviews/*.md` 파일들을 읽는다
   - **2차 소스** (리뷰 파일 미존재 시): `git log`에서 커밋 메시지와 변경 패턴을 분석하여 반복 지적 패턴을 추론한다
   - 반복적으로 지적된 패턴 추출
   - 블로커로 분류된 이슈 유형 정리
   - Convention Guard가 놓친 패턴 식별

2. 사용자에게 발견된 패턴을 제시한다:
   - 각 패턴의 발생 빈도
   - 대표 사례
   - 제안하는 룰 내용

3. 사용자 승인 후 다음을 업데이트한다:
   - **docs/conventions.md**: 새 컨벤션 룰을 **적절한 섹션에** 추가한다. 이 파일이 Convention Guard(OCR 리뷰)의 단일 규칙 소스이므로, 새 체크 항목도 이 파일에 추가한다. **기존 룰은 삭제하지 않는다** (append-only). 기존 룰 보완·구체화만 허용한다.
     **섹션 분류 규칙:**
     - Core 섹션(아키텍처, 네이밍, 테스트, 코드 스타일)에 해당하면 해당 섹션에 추가
     - 기술 특화 패턴이면 concern-area 섹션(UI 패턴, API 패턴, DB 패턴, 보안 패턴, 인프라 패턴)에 추가
     - concern-area 섹션이 아직 없으면 해당 섹션 헤딩(`## {Name} 패턴`)을 새로 생성하여 추가
     - 어느 섹션에도 맞지 않으면 가장 관련 높은 Core 섹션에 추가
   - **CLAUDE.md**: Changelog 섹션에 컨벤션 업데이트 이력을 기록한다. 본문(설계 원칙, 핵심 개념 등)은 수정하지 않는다

4. git commit을 수행한다:
   - 메시지: `[{TICKET}] 컨벤션 업데이트`

## Output Format

- docs/conventions.md 업데이트 (Convention Guard 규칙 포함)
- CLAUDE.md 업데이트 (필요 시)
- git commit
