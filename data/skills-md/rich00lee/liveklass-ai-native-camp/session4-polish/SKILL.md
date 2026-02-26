---
name: session4-polish
description: LiveKlass AI Native Camp 4회차. Session 3에서 만든 Skill을 고도화하고 발표를 준비한다. "4회차", "Session 4", "고도화", "피칭", "발표 준비" 요청에 사용.
---

# Session 4: 고도화 + 발표 준비

이 스킬이 호출되면 아래 **STOP PROTOCOL**을 반드시 따른다.

---

## 용어 정리

| 용어 | 설명 |
|------|------|
| **피칭(pitching)** | 짧은 시간 안에 핵심을 전달하는 발표. "이게 뭐고, 왜 좋은지"를 1분 안에 |
| **리팩토링(refactoring)** | 동작은 그대로 유지하면서 코드/문서의 구조를 개선하는 것 |
| **엣지 케이스(edge case)** | 예상치 못한 극단적인 입력. "데이터가 0개일 때", "100개일 때" 같은 상황 |
| **출력 형식(output format)** | Skill 결과물의 모양. "3줄 요약", "테이블", "Slack 메시지" 등 |
| **SKILL.md** | Skill의 본체 파일. 이 안에 Claude의 행동 규칙을 적는다 |

---

## STOP PROTOCOL — 절대 위반 금지

> 이 프로토콜은 이 스킬의 최우선 규칙이다.
> 아래 규칙을 위반하면 수업이 망가진다.

### 각 블록은 반드시 2턴에 걸쳐 진행한다

```
┌─ Phase A (첫 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 EXPLAIN 섹션을 읽는다    │
│ 2. 기능을 설명한다                                        │
│ 3. references/에서 해당 블록 파일의 EXECUTE 섹션을 읽는다    │
│ 4. "지금 직접 실행해보세요"라고 안내한다                     │
│ 5. ⛔ 여기서 반드시 STOP. 턴을 종료한다.                    │
│                                                          │
│ ❌ 절대 하지 않는 것: 퀴즈 출제, QUIZ 섹션 읽기             │
│ ❌ 절대 하지 않는 것: AskUserQuestion 호출 (Block 0 제외)   │
│ ❌ 절대 하지 않는 것: "실행해봤나요?" 질문                   │
│ ❌ 절대 하지 않는 것: 다음 블록 내용 미리 언급               │
│ ❌ 절대 하지 않는 것: Phase A 종료 문구 이후 추가 텍스트 출력 │
└──────────────────────────────────────────────────────────┘

  ⬇️ 사용자가 돌아와서 "했어", "완료", "다음" 등을 입력한다

┌─ Phase B (두 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 QUIZ 섹션을 읽는다       │
│ 2. AskUserQuestion으로 퀴즈를 출제한다                     │
│ 3. 정답/오답 피드백을 준다                                 │
│ 4. 다음 블록으로 이동할지 AskUserQuestion으로 묻는다         │
│ 5. ⛔ 다음 블록을 시작하면 다시 Phase A부터.                │
└──────────────────────────────────────────────────────────┘
```

### 핵심 금지 사항 (절대 위반 금지)

1. **Phase A에서 AskUserQuestion을 호출하지 않는다 (Block 0 제외)** — Block 0은 개선할 Skill 선택이 필수이므로 예외
2. **Phase A에서 퀴즈를 내지 않는다** — QUIZ 섹션은 Phase B에서만 읽는다
3. **Phase A에서 "실행해봤나요?"를 묻지 않는다** — 사용자가 먼저 말할 때까지 기다린다
4. **한 턴에 EXPLAIN + QUIZ를 동시에 하지 않는다** — 반드시 2턴으로 나눈다
5. **Phase A 종료 문구 이후 어떤 도구 호출이나 추가 텍스트도 출력하지 않는다**

### 공식 문서 URL 출력 (절대 누락 금지)

모든 블록의 Phase A 시작 시, 해당 reference 파일 상단의 `> 공식 문서:` URL을 **반드시 그대로 출력**한다.

```
📖 공식 문서: [URL]
```

- reference 파일에 URL이 여러 개 있으면 전부 출력한다
- URL을 요약하거나 생략하지 않는다

### Phase A 종료 시 필수 문구

Phase A의 마지막에는 반드시 아래 문구를 출력하고 Stop한다:

```
---
👆 위 내용을 직접 실행해보세요.
실행이 끝나면 "완료" 또는 "다음"이라고 입력해주세요.
```

---

## 블록 특수 규칙

- **Block 0 (Review)**: Phase A에서 설명 + AskUserQuestion으로 개선할 Skill/포인트 선택. 선택 결과로 Block 1 개선 방향 확정 → Stop. Phase B에서 문제 진단 확인.
- **Block 1 (Polish)**: Phase A에서 3가지 개선 패턴 설명 + 사용자가 직접 SKILL.md 수정 → Stop. Phase B에서 개선 결과 확인.
- **Block 2 (Pitch)**: Phase A에서 1분 피칭 구조 설명 + 피칭 스크립트 작성 + GitHub 숙제 안내 → Stop. Phase B에서 리허설 (자유 답변 → Claude가 피드백).

### Block 0 예외 규칙

Block 0의 Phase A는 **AskUserQuestion을 사용**한다. 개선할 Skill 선택이 이후 모든 블록의 전제 조건이므로 반드시 사용자 입력을 받아야 한다.

Phase A 진행 순서:
1. `references/block0-review.md`의 EXPLAIN 섹션을 읽고 설명한다
2. AskUserQuestion으로 가장 먼저 개선하고 싶은 포인트를 선택받는다
3. 선택된 포인트의 개선 방향을 정리하여 보여준다
4. Stop한다

---

## References 파일 맵

| 블록 | 파일 | 내용 |
|------|------|------|
| Block 0 | `references/block0-review.md` | Skill 사용 후기 + 문제 진단 |
| Block 1 | `references/block1-polish.md` | 3가지 개선 패턴 적용 |
| Block 2 | `references/block2-pitch.md` | 1분 데모 피칭 준비 + GitHub 숙제 |

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- Session 3에서 만든 Skill을 직접 개선하는 세션
- 이 세션의 목표: **동작하는 Skill → 믿을 수 있는 Skill + 발표 준비**
- 완성도보다 **개선 경험과 발표 자신감** 우선

---

## 시작

아래 테이블을 보여주고 AskUserQuestion으로 어디서 시작할지 물어본다.

| Block | 주제 | 내용 |
|-------|------|------|
| 0 | Review | Session 3 Skill 사용 후기 + 문제 진단 |
| 1 | Polish | 3가지 개선 패턴으로 Skill 고도화 |
| 2 | Pitch | 1분 데모 피칭 준비 + GitHub 숙제 |

```json
AskUserQuestion({
  "questions": [{
    "question": "Session 4: 고도화 + 발표 준비\n\n어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "처음부터 (Block 0: Review)", "description": "Session 3 Skill 점검부터"},
      {"label": "바로 개선 (Block 1: Polish)", "description": "개선할 포인트는 알고 있어"},
      {"label": "발표 준비 (Block 2: Pitch)", "description": "Skill은 완성, 발표 준비부터"}
    ],
    "multiSelect": false
  }]
})
```
