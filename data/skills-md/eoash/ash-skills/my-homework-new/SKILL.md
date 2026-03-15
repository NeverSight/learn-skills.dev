---
name: my-homework-new
description: AI Native Camp 숙제 파일을 자동 생성하는 스킬. "homework Day N", "숙제 파일 만들어줘", "/homework-new" 요청에 사용.
---

# my-homework-new

AI Native Camp 숙제 파일을 올바른 형식으로 자동 생성한다.
"빈 문서를 열어서 형식을 기억해내는" 수고를 없애는 역할.

## Execution Flow

```
┌─────────────────────────────────────────────┐
│  Step 1. Day 번호 확인                        │
│  (어떤 날의 숙제 파일을 만들지)                │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│  Step 2. 숙제 내용 입력                        │
│  (과제 지시문 또는 주제 입력받기)               │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│  Step 3. 파일 생성                            │
│  docs/camp/ai_native_camp_dayN_homework.md  │
└─────────────────────────────────────────────┘
```

---

## Step 1: Day 번호 확인

AskUserQuestion으로 어떤 날의 숙제인지 확인한다:

```json
AskUserQuestion({
  "questions": [{
    "question": "몇 일차 숙제 파일을 만들까요?",
    "header": "Day 번호",
    "options": [
      {"label": "Day 3", "description": "clarify 스킬 실습"},
      {"label": "Day 4", "description": "session-wrap / multi-agent 실습"},
      {"label": "Day 5", "description": "다음 수업"},
      {"label": "직접 입력", "description": "다른 번호 입력"}
    ],
    "multiSelect": false
  }]
})
```

---

## Step 2: 숙제 지시문 확인

숙제 지시문을 사용자에게 붙여넣으라고 안내하거나,
주제 키워드만 있으면 기본 형식으로 생성한다.

---

## Step 3: 파일 생성

아래 템플릿으로 `docs/camp/ai_native_camp_dayN_homework.md` 를 생성한다:

```markdown
# AI Native Camp Day N 과제 - 안서현

## 과제: [과제 제목]

[과제 지시문]

---

## Claude가 던진 질문들

### Q1. [질문]

**내 답변:**

---

## 💡 가장 의외였던 질문

**질문:**

**이 질문이 의외였던 이유:**

---

## 📝 전후 요구사항 변화

### Before

### After

---

## 💭 오늘의 배움

---

*생성: Claude Code + [사용한 스킬]*
*날짜: YYYY-MM-DD*
```

파일 생성 후 "파일이 준비됐습니다. 이제 내용을 채워보세요"라고 안내한다.

---

## Quick Reference

- 언제: 수업 직후, 숙제 파일 작성 시작 전
- 소요 시간: ~30초
- 위치: `docs/camp/ai_native_camp_dayN_homework.md`
