---
name: session3-automation
description: LiveKlass AI Native Camp 3회차. 나만의 업무 자동화 Skill 기획 → 제작 → 테스트. "3회차", "Session 3", "자동화 만들기", "스킬 만들기" 요청에 사용.
---

# Session 3: 나만의 업무 자동화 만들기

이 스킬이 호출되면 아래 **STOP PROTOCOL**을 반드시 따른다.

---

## 용어 정리

| 용어 | 설명 |
|------|------|
| **Skill** | Claude Code에게 특정 작업 방법을 가르치는 문서. Session 1에서 체험, Session 2에서 직접 만든 것 |
| **SKILL.md** | Skill의 본체 파일. 이 안에 Claude의 행동 규칙을 적는다 |
| **frontmatter** | SKILL.md 맨 위 `---` 사이에 적는 메타 정보 (name, description) |
| **description** | frontmatter 안에서 "이 Skill을 언제 쓸지" 정의하는 한 줄 설명 |
| **references** | SKILL.md가 참조하는 교안 파일들. EXPLAIN/EXECUTE/QUIZ 3섹션 구조 |

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

1. **Phase A에서 AskUserQuestion을 호출하지 않는다 (Block 0 제외)** — Block 0은 아이디어 선택이 필수이므로 예외
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

- **Block 0 (Design)**: Phase A에서 설명 + AskUserQuestion으로 자동화 아이디어 선택. 선택 결과로 SKILL.md 설계 방향 확정 → Stop. Phase B에서 입력/출력 명확성 확인.
- **Block 1 (Build)**: Phase A에서 SKILL.md 작성 원칙 설명 + **Claude가 사용자 프로젝트에 직접 스킬 파일을 생성** → Stop. Phase B에서 실행 결과 확인.
- **Block 2 (Test)**: Phase A에서 3가지 테스트 시나리오 설명 + 테스트 실행 + 중간 발표 30초 피칭 문구 작성 → Stop. Phase B에서 피칭 문구 다듬기 (자유 답변).

### Block 0 예외 규칙

Block 0의 Phase A는 **AskUserQuestion을 사용**한다. 아이디어 선택이 이후 모든 블록의 전제 조건이므로 반드시 사용자 입력을 받아야 한다.

Phase A 진행 순서:
1. `references/block0-design.md`의 EXPLAIN 섹션을 읽고 설명한다
2. AskUserQuestion으로 자동화 아이디어를 선택받는다
3. 선택된 아이디어의 입력/출력 구조를 정리하여 보여준다
4. Stop한다

---

## References 파일 맵

| 블록 | 파일 | 내용 |
|------|------|------|
| Block 0 | `references/block0-design.md` | 자동화 아이디어 구체화 + SKILL.md 설계 방향 |
| Block 1 | `references/block1-build.md` | SKILL.md 작성 원칙 + Claude가 직접 스킬 파일 생성 |
| Block 2 | `references/block2-test.md` | 3가지 테스트 시나리오 + 중간 발표 30초 피칭 준비 |

---

## 진행 규칙

- 한 번에 한 블록씩 진행한다
- "다음", "skip", 블록 번호/이름으로 이동한다
- Session 2에서 만든 /my-context-sync 경험을 기반으로, 이번에는 나만의 Skill을 처음부터 만든다
- 참가자마다 만드는 Skill이 다르므로 개별 맞춤 진행
- 이 세션은 **실습 중심** — 설명보다 만드는 시간이 더 많다
- 막히면 "뭘 만들려고 하는지" 다시 물어보고 작게 쪼개서 도움
- 완성도보다 **동작하는 결과물** 우선

---

## 시작

아래 테이블을 보여주고 AskUserQuestion으로 어디서 시작할지 물어본다.

| Block | 주제 | 내용 |
|-------|------|------|
| 0 | Design | 자동화 아이디어 구체화 + SKILL.md 설계 |
| 1 | Build | SKILL.md 작성 + 실제 Skill 제작 |
| 2 | Test | 테스트 + 개선 + 중간 발표 준비 |

```json
AskUserQuestion({
  "questions": [{
    "question": "Session 3: 나만의 업무 자동화 만들기\n\n어디서부터 시작할까요?",
    "header": "시작 블록",
    "options": [
      {"label": "처음부터 (Block 0: Design)", "description": "자동화 아이디어 구체화 → SKILL.md 설계"},
      {"label": "바로 제작 (Block 1: Build)", "description": "아이디어는 있고, Skill 제작부터"},
      {"label": "테스트 (Block 2: Test)", "description": "만든 Skill 테스트 + 개선 + 중간 발표 준비"}
    ],
    "multiSelect": false
  }]
})
```
