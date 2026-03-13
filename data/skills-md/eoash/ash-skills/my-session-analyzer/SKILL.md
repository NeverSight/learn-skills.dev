---
name: my-session-analyzer
description: 스킬 실행 기록을 SKILL.md 설계도와 비교해서 PASS/FAIL 검증 리포트를 생성하는 스킬. "/session-analyzer", "세션 검증", "스킬 분석", "실행 검증" 요청에 사용.
---

# my-session-analyzer

SKILL.md(설계도)와 실제 세션 실행 기록을 비교해서 스킬이 의도대로 동작했는지 검증한다.
"레시피대로 요리했는지 감독관이 확인하는 것"과 같은 역할.

## Execution Flow

```
┌─────────────────────────────────────────────┐
│  Step 1. 분석 대상 스킬 선택                   │
│  (어떤 스킬의 실행을 검증할지)                  │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│  Step 2. SKILL.md 파싱                        │
│  설계도에서 "기대 동작" 추출                    │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│  Step 3. 세션 기록 분석                        │
│  가장 최근 세션에서 "실제 동작" 추출             │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│  Step 4. Expected vs Actual 비교              │
│  PASS / FAIL 판정                             │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│  Step 5. 검증 리포트 출력                      │
│  + FAIL 항목 개선 제안                         │
└─────────────────────────────────────────────┘
```

---

## Step 1: 분석 대상 스킬 선택

AskUserQuestion으로 어떤 스킬의 실행을 검증할지 선택받는다:

```json
AskUserQuestion({
  "questions": [{
    "question": "어떤 스킬의 실행을 검증할까요?",
    "header": "검증 대상",
    "options": [
      {"label": "my-session-wrap", "description": "세션 정리 스킬 검증"},
      {"label": "my-context-sync", "description": "컨텍스트 싱크 스킬 검증"},
      {"label": "my-history-insight", "description": "히스토리 분석 스킬 검증"},
      {"label": "직접 입력", "description": "다른 스킬 이름 직접 입력"}
    ],
    "multiSelect": false
  }]
})
```

---

## Step 2: SKILL.md 파싱 — 기대 동작 추출

선택된 스킬의 SKILL.md를 읽어서 아래 항목을 추출한다:

- **에이전트 목록**: 어떤 에이전트가 정의되어 있는지
- **실행 순서**: 병렬/순차 구조가 어떻게 설계됐는지
- **출력 형식**: 어떤 결과물을 만들어야 하는지
- **필수 단계**: 반드시 실행해야 하는 Step들

추출한 항목을 "기대 동작 체크리스트"로 정리한다.

예시:
```
기대 동작 체크리스트 (my-session-wrap 기준)
□ git status 실행 (Step 1)
□ doc-updater 에이전트 실행 (Phase 1, 병렬)
□ automation-scout 에이전트 실행 (Phase 1, 병렬)
□ learning-extractor 에이전트 실행 (Phase 1, 병렬)
□ followup-suggester 에이전트 실행 (Phase 1, 병렬)
□ duplicate-checker 실행 (Phase 2, Phase 1 완료 후)
□ AskUserQuestion으로 사용자 선택 받기 (Step 4)
□ 선택된 작업 실행 (Step 5)
```

---

## Step 3: 세션 기록 분석 — 실제 동작 추출

`~/.claude/projects/` 에서 해당 스킬이 실행된 가장 최근 세션 파일을 찾는다.

- 세션 파일의 assistant 메시지에서 Tool 호출 기록 확인
- Task(서브에이전트) 호출 횟수와 이름 확인
- AskUserQuestion 호출 여부 확인
- Bash/Read/Write/Edit 등 도구 사용 패턴 확인
- 최종 출력물(파일 생성, 커밋 등) 확인

추출한 항목을 "실제 동작 기록"으로 정리한다.

---

## Step 4: Expected vs Actual 비교

기대 동작과 실제 동작을 표로 비교해서 PASS/FAIL 판정한다.

```
| 구성요소            | 기대한 것          | 실제 결과          | 판정  |
|--------------------|-------------------|-------------------|-------|
| git status 실행    | Step 1에서 실행   | Bash로 실행됨     | PASS  |
| doc-updater        | 병렬 실행         | Task로 병렬 실행  | PASS  |
| automation-scout   | 병렬 실행         | Task로 병렬 실행  | PASS  |
| learning-extractor | 병렬 실행         | Task로 병렬 실행  | PASS  |
| followup-suggester | 병렬 실행         | Task로 병렬 실행  | PASS  |
| duplicate-checker  | Phase 1 완료 후   | Phase 1 후 실행   | PASS  |
| 사용자 선택        | AskUserQuestion   | AskUserQuestion   | PASS  |
| 선택 작업 실행     | 조건부 실행       | 실행됨            | PASS  |
```

**판정 기준:**
- **PASS**: 설계도대로 동작함
- **FAIL**: 설계도와 다르게 동작하거나 생략됨
- **PARTIAL**: 일부만 실행됨

---

## Step 5: 검증 리포트 출력

```
🔍 session-analyzer 검증 리포트
대상 스킬: [스킬명]
분석 세션: [세션 ID 앞 8자리]
실행 시각: YYYY-MM-DD HH:MM

━━━━━━━━━━━━━━━━━━━━━━━━

📋 Expected vs Actual

[비교 테이블]

━━━━━━━━━━━━━━━━━━━━━━━━

📊 전체 판정
✅ PASS: X개 / ❌ FAIL: Y개 / ⚠️ PARTIAL: Z개

최종 결과: [PASS / FAIL / PARTIAL]

━━━━━━━━━━━━━━━━━━━━━━━━

🔧 개선 제안 (FAIL 항목이 있을 때만)
- [FAIL 항목]: [구체적인 SKILL.md 수정 방법]

━━━━━━━━━━━━━━━━━━━━━━━━

💡 총평
[스킬이 전반적으로 의도대로 동작했는지 한 줄 평가]
```

FAIL 항목이 있으면 바로 수정 여부를 물어본다:

```json
AskUserQuestion({
  "questions": [{
    "question": "FAIL 항목을 발견했습니다. 어떻게 할까요?",
    "header": "다음 단계",
    "options": [
      {"label": "SKILL.md 바로 수정", "description": "FAIL 항목 기반으로 스킬 개선"},
      {"label": "나중에 수정", "description": "현재는 리포트만 확인하고 넘어감"},
      {"label": "무시", "description": "핵심 기능은 동작하므로 그대로 사용"}
    ],
    "multiSelect": false
  }]
})
```

---

## Quick Reference

- 언제: 스킬을 새로 만들거나 수정한 직후
- 소요 시간: ~1분
- 핵심 원칙: **만들기 → 실행 → 검증 → 수정의 반복**이 좋은 스킬을 만든다
