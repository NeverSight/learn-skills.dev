---
name: session1-onboarding
description: LiveKlass AI Native Camp 1회차 온보딩. Claude Code 설치부터 핵심 기능 체험까지. "1회차", "Session 1", "온보딩", "설치" 요청에 사용.
---

# Session 1: Onboarding — 설치 + 핵심 기능 체험

이 스킬이 호출되면 아래 **STOP PROTOCOL**을 반드시 따른다.

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
│ ❌ 절대 하지 않는 것: AskUserQuestion 호출                  │
│ ❌ 절대 하지 않는 것: "실행해봤나요?" 질문                   │
└──────────────────────────────────────────────────────────┘

  ⬇️ 참가자가 돌아와서 "했어", "완료", "다음" 등을 입력한다

┌─ Phase B (두 번째 턴) ──────────────────────────────┐
│ 1. references/에서 해당 블록 파일의 QUIZ 섹션을 읽는다       │
│ 2. AskUserQuestion으로 퀴즈를 출제한다                     │
│ 3. 정답/오답 피드백을 준다                                 │
│ 4. 다음 블록으로 이동할지 AskUserQuestion으로 묻는다         │
│ 5. ⛔ 다음 블록을 시작하면 다시 Phase A부터.                │
└──────────────────────────────────────────────────────────┘
```

### 핵심 금지 사항

1. **Phase A에서 AskUserQuestion을 호출하지 않는다** — 설명 + 실행 안내 후 바로 Stop
2. **Phase A에서 퀴즈를 내지 않는다** — QUIZ 섹션은 Phase B에서만 읽는다
3. **한 턴에 EXPLAIN + QUIZ를 동시에 하지 않는다** — 반드시 2턴으로 나눈다

### 공식 문서 URL 출력 (절대 누락 금지)

모든 블록의 Phase A 시작 시, 해당 reference 파일 상단의 `> 공식 문서:` URL을 **반드시 그대로 출력**한다.

```
📖 공식 문서: [URL]
```

### Phase A 종료 시 필수 문구

```
---
👆 위 내용을 직접 실행해보세요.
실행이 끝나면 "완료" 또는 "다음"이라고 입력해주세요.
```

### 블록 특수 규칙

- **Block 0 (Setup)**: 퀴즈 없음. Phase A에서 설명+실행 안내 → Stop. Phase B에서 완료 확인만.
- **Block 1 (Experience)**: LiveKlass 실무 예시 3가지 데모. Phase B에서 소감 확인.
- **Block 2 (Features)**: 4개 핵심 기능 각각 독립 블록 (2-1 CLAUDE.md / 2-2 Skill / 2-3 MCP / 2-4 Subagent).

---

## References 파일 맵

| 블록 | 파일 |
|------|------|
| Block 0 | `references/block0-setup.md` |
| Block 1 | `references/block1-experience.md` |
| Block 2-1 | `references/block2-1-claude-md.md` |
| Block 2-2 | `references/block2-2-skill.md` |
| Block 2-3 | `references/block2-3-mcp.md` |
| Block 2-4 | `references/block2-4-subagent.md` |

> 파일 경로는 이 SKILL.md 기준 상대경로다.
> 각 reference 파일은 `## EXPLAIN`, `## EXECUTE`, `## QUIZ` 섹션으로 구성된다.

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- Claude Code 관련 질문이 오면 claude-code-guide 에이전트로 답변한다

---

## 시작

스킬 시작 시 아래 테이블을 보여주고 AskUserQuestion으로 어디서 시작할지 물어본다.

| Block | 주제 | 내용 |
|-------|------|------|
| 0 | Setup | Claude Code 설치 + 첫 대화 |
| 1 | Experience | LiveKlass 실무 예시 3가지 데모 |
| 2 | Features | 4개 핵심 기능 (CLAUDE.md / Skill / MCP / Subagent) |

```json
AskUserQuestion({
  "questions": [{
    "question": "어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "Block 0: Setup", "description": "Claude Code 설치 + 첫 대화"},
      {"label": "Block 1: Experience", "description": "LiveKlass 실무 예시 3가지 데모"},
      {"label": "Block 2: Features", "description": "4개 핵심 기능 소개"}
    ],
    "multiSelect": false
  }]
})
```

> 시작 블록 선택 후 → 해당 블록의 Phase A부터 진행한다.
