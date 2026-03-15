---
name: slack-to-gcal
description: Slack 이모지 반응자를 Google Calendar 이벤트에 자동 초대. "슬랙 캘린더", "이모지 반응 초대", "slack to gcal", "/slack-gcal" 요청에 사용.
---

# slack-to-gcal

Slack 메시지에 이모지 반응한 사람들을 Google Calendar 이벤트에 자동 초대하는 스킬.

## Step 1: 링크 수집

사용자에게 두 가지 링크를 받는다.

- **Slack 메시지 링크**: 이모지 반응을 받은 메시지의 링크
  - Slack에서 메시지 우클릭 → "링크 복사"
  - 예: `https://eo2019.slack.com/archives/C01N15328HG/p1772186298231169`
- **Google Calendar 이벤트 링크**: 초대할 이벤트의 편집 URL
  - 캘린더에서 이벤트 클릭 → 연필(편집) 아이콘 → 주소창 URL 복사
  - 예: `https://calendar.google.com/calendar/u/0/r/eventedit/NGhwY3Y4...`

아직 두 링크를 받지 않은 경우 AskUserQuestion으로 요청한다:

```json
AskUserQuestion({
  "questions": [
    {
      "question": "이모지 반응을 받은 Slack 메시지 링크를 붙여넣으세요.",
      "header": "Slack 링크",
      "options": [
        {"label": "링크 준비됨", "description": "다음 단계로 진행"},
        {"label": "링크 찾는 중", "description": "메시지 우클릭 → 링크 복사"}
      ],
      "multiSelect": false
    }
  ]
})
```

## Step 2: 스크립트 실행

두 링크를 받으면 아래 명령어를 실행한다.

```bash
cd C:\Users\ash\ash
printf 'y\n' | PYTHONIOENCODING=utf-8 python scripts/tools/slack_to_gcal.py \
  --slack "[SLACK_링크]" \
  --cal "[CALENDAR_링크]"
```

- `[SLACK_링크]`와 `[CALENDAR_링크]`를 사용자가 제공한 실제 링크로 교체
- `token_calendar.json`이 있으면 Google 로그인 없이 바로 실행됨

## Step 3: 결과 요약

스크립트 출력 결과를 보기 좋게 정리해서 보여준다:

```
✅ 완료!

이벤트: [이벤트 제목]
일시: [날짜/시간]

이모지 반응자 총 N명
├── 새로 초대됨 (N명): 이름, 이름, 이름
└── 이미 초대됨 (N명): 이름, 이름
```

---

## 참고

- 스크립트 위치: `scripts/tools/slack_to_gcal.py`
- Google Calendar 토큰: `token_calendar.json` (최초 1회 브라우저 로그인 필요)
- Slack 봇 토큰: `.env`의 `SLACK_BOT_TOKEN`
- 필요 스코프: `reactions:read`, `users:read`, `users:read.email`
