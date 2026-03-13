---
name: compact-guide
description: "컨텍스트 윈도우 관리 및 토큰 최적화 가이드. Triggers on: 컨텍스트, 토큰, compact, 메모리 관리. NOT for: 코드 작성, 디버깅."
disable-model-invocation: false
user-invocable: true
---

# 컨텍스트 관리 가이드

컨텍스트는 신선한 우유와 같습니다. 시간이 지나면 상합니다.

## 핵심 규칙
- 토큰 80-100k 넘기 전에 리셋
- 3-5개 작업마다 컨텍스트 정리
- /compact 3번 후 /clear

## 명령어

### /compact
- 대화 내용을 요약해서 압축
- 중요한 정보는 유지, 토큰만 줄임
- 작업 흐름이 끊기지 않음

### /clear
- 완전히 초기화
- HANDOFF.md 없으면 위험!
- 깨끗하게 시작하고 싶을 때

## 권장 패턴

```
작업 시작
    ↓
3-5개 작업 완료
    ↓
/compact (토큰 압축)
    ↓
3-5개 작업 완료
    ↓
/compact
    ↓
3-5개 작업 완료
    ↓
/compact
    ↓
/handoff (HANDOFF.md 생성)
    ↓
/clear (초기화)
    ↓
새 세션에서 HANDOFF.md 읽기
```

## 주의
200k 토큰까지 쓸 수 있지만, 80-100k 넘으면 품질 저하!

## 캐시 관점의 컨텍스트 관리

### /compact가 유리한 이유
- 시스템 프롬프트 + 도구 정의의 prefix 캐시가 유지됨
- 대화 메시지만 요약되므로 매 턴 캐시 히트 가능
- /clear보다 비용이 크게 낮음

### /clear의 숨겨진 비용
- 전체 prefix 캐시 무효화 (시스템 프롬프트 + 도구 + CLAUDE.md + rules/ 재계산)
- HANDOFF.md 로드 시 추가 토큰 발생
- 다음 API 호출부터 캐시 워밍업 필요

### Compaction 타이밍 가이드
- 50-70k 토큰: 첫 /compact (여유 있을 때 미리)
- 80-100k 토큰: 두 번째 /compact 또는 /handoff 준비
- /compact 후에도 80k 이상이면: /handoff → /clear → 새 세션
- 150k 이상에서 compact하지 않기 (buffer 부족 위험)
