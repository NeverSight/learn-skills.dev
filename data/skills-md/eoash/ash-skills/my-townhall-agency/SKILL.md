---
name: my-townhall-agency
description: 타운홀 슬라이드 자동 생성 에이전시. 리서처→요약가→디자이너→개발자 4명의 에이전트가 순차적으로 데이터 수집, 슬라이드 구조화, Apps Script 코드 생성, 실제 Google Slides 삽입까지 자동 실행. "타운홀 만들어줘", "townhall 슬라이드", "/townhall", "타운홀 에이전시" 요청에 사용.
---

# My Townhall Agency

타운홀 자료 제작을 위한 4-Agent 파이프라인.
사용자가 덱 ID와 주제만 주면, 4명의 에이전트가 순차적으로 실행되어 Google Slides에 슬라이드가 삽입된다.

---

## 팀 구성

| 에이전트 | 역할 | 인풋 → 아웃풋 |
|---------|------|--------------|
| 🔍 리서처 | 데이터 수집·분석 | 컨텍스트 소스들 → `townhall/DATA.md` |
| 📝 요약가 | PPT 구조 설계 | `DATA.md` → `townhall/OUTLINE.md` |
| 🎨 디자이너 | Apps Script 코드 생성 | `OUTLINE.md` → `townhall/slides.gs` |
| 💻 개발자 | 실제 덱에 슬라이드 삽입 | `slides.gs` → Google Slides (Chrome 자동화) |

---

## 실행 전 준비

스킬이 트리거되면:

1. 사용자에게 확인:
   - **덱 ID**: 삽입할 Google Slides 파일 ID (URL에서 `/d/` 다음 부분)
   - **주제**: 어떤 섹션 슬라이드를 만들지 (예: "재무 현황", "법인 운영", "연간 목표")
   - **데이터 소스**: 어디서 데이터를 가져올지 (컨텍스트 싱크 파일, 직접 입력 등)

2. `townhall/` 폴더가 없으면 생성

3. 기존 컨텍스트 파일 확인:
   - `.claude/skills/my-context-sync/sync/` 최신 파일
   - `agent/projects/finance/` 파일들
   - `agent/projects/ar_automation/memory/financial_state.md`

---

## 실행 흐름

```
[입력] 덱 ID + 주제 + 데이터 소스
    ↓
[1단계] 리서처 에이전트 → DATA.md 생성
    ↓
[DATA 검증] 필수 섹션 확인 → 실패 시 재실행 (1회)
    ↓
[2단계] 요약가 에이전트 → OUTLINE.md 생성
    ↓
[OUTLINE 검증] 슬라이드 수 확인 (최소 1장) → 실패 시 재실행 (1회)
    ↓
[3단계] 디자이너 에이전트 → slides.gs 생성
    ↓
[코드 검증] 파일 존재 + addSlides 함수 포함 여부 확인
    ↓
[4단계] 개발자 (오케스트레이터) → Chrome 자동화로 실행
    ↓
[최종 보고] 슬라이드 추가 완료 + 덱 URL 출력
```

---

## 각 에이전트 실행 방법

### 🔍 1단계: 리서처 에이전트

```
Task(
  description="리서처: 타운홀 데이터 수집",
  prompt="""
너는 EO Studio 재무·운영 데이터 리서처다.
아래 주제에 맞는 데이터를 수집·정리해서 townhall/DATA.md를 작성하라.

주제: {topic}
데이터 소스:
- .claude/skills/my-context-sync/sync/ 폴더의 최신 컨텍스트 싱크 파일
- agent/projects/ar_automation/memory/financial_state.md (존재 시)
- agent/projects/finance/ 폴더 (존재 시)
- CLAUDE.md의 현재 진행 상태 섹션

DATA.md 형식:
# 타운홀 데이터: {topic}
수집일: {날짜}

## 핵심 수치
- 항목별 수치를 bullet로 정리 (단위 포함)

## 세부 내역
- 카테고리별 상세 데이터

## 현황 및 이슈
- 진행 중인 항목
- 블로커 또는 주요 이슈

## 파이프라인 / 전망
- 예정된 항목, 목표 수치

수집한 모든 관련 데이터를 townhall/DATA.md에 저장하라.
""",
  subagent_type="general-purpose"
)
```

### 📝 2단계: 요약가 에이전트

```
Task(
  description="요약가: 슬라이드 구조 설계",
  prompt="""
너는 EO Studio 타운홀 슬라이드 기획자다.
townhall/DATA.md를 읽고, 발표용 슬라이드 구조를 설계해서 townhall/OUTLINE.md를 작성하라.

규칙:
- 슬라이드는 2~4장으로 구성 (너무 많으면 전달력 저하)
- 각 슬라이드는 하나의 핵심 메시지만 전달
- 수치는 임팩트 있게 배치 (가장 큰 숫자를 헤드라인으로)
- 한국어와 영어를 적절히 혼용 (레이블은 영어, 내용은 한국어)

OUTLINE.md 형식:
# 타운홀 슬라이드 구조: {topic}

## SLIDE 1: {슬라이드 제목}
- 헤드라인 수치: (가장 강조할 숫자)
- 서브 타이틀: (한 줄 설명)
- 좌측 블록:
  - 제목:
  - 항목들: (리스트)
- 우측 블록:
  - 제목:
  - 항목들: (리스트)
- 하단 메시지: (핵심 takeaway 한 줄)

## SLIDE 2: {슬라이드 제목}
(동일 형식)

## 디자인 가이드
- 배경: 블랙 (#0D0D0D)
- 강조색: EO 옐로우 (#E8FF47)
- 폰트 색: 흰색, 회색 (#888888)
- 레이아웃: 좌우 분할 또는 카드형

완성된 OUTLINE을 townhall/OUTLINE.md에 저장하라.
""",
  subagent_type="general-purpose"
)
```

### 🎨 3단계: 디자이너 에이전트

```
Task(
  description="디자이너: Apps Script 코드 생성",
  prompt="""
너는 Google Apps Script 전문 개발자다.
townhall/OUTLINE.md를 읽고, 기존 Google Slides 덱에 슬라이드를 추가하는 Apps Script 코드를 작성하라.

덱 ID: {deck_id}

반드시 지켜야 할 규칙:
1. SlidesApp.openById(DECK_ID)로 기존 덱 열기 (create 절대 금지)
2. presentation.appendSlide()로 슬라이드 추가
3. SlidesApp.getUi()는 사용 금지 (에러 발생)
4. Logger.log()로 완료 메시지와 URL 출력
5. 함수명은 반드시 addSlides()로 통일

색상 팔레트 (반드시 사용):
- BLACK: "#0D0D0D"
- WHITE: "#FFFFFF"
- GRAY_DARK: "#1E1E1E"
- GRAY_MID: "#2E2E2E"
- ACCENT: "#E8FF47" (EO 시그니처 옐로우)
- TEXT_MUTED: "#888888"
- GREEN: "#4CAF50"

유틸 함수 패턴 (반드시 포함):
function addText(slide, text, x, y, w, h, opts) { ... }
function addRect(slide, x, y, w, h, color, opacity) { ... }
function addLine(slide, x, y, length, color) { ... }

슬라이드 사이즈: W=720, H=405 (16:9 기준 pt)

각 슬라이드 상단 공통 헤더:
- 좌: "FINANCE · {날짜}" (9pt, TEXT_MUTED)
- 우: "{날짜}" (9pt, TEXT_MUTED, right-align)
- 구분선: addLine(slide, 40, 46, W-80, GRAY_MID)

OUTLINE.md의 내용을 정확히 코드로 구현하라.
완성된 코드를 townhall/slides.gs 파일로 저장하라.
""",
  subagent_type="general-purpose"
)
```

### 💻 4단계: 개발자 (오케스트레이터 직접 실행)

4단계는 Chrome 자동화가 필요하므로 오케스트레이터(메인 Claude)가 직접 실행한다.

실행 순서:
1. `townhall/slides.gs` 파일 읽기
2. Chrome에서 Apps Script 에디터 열기 (work 계정)
3. Monaco 에디터에 코드 삽입
4. 저장 → `addSlides` 함수 선택 → 실행
5. 실행 로그 확인 → 완료 메시지 캡처
6. 덱으로 이동해서 결과 스크린샷

---

## 검증 로직

### DATA 검증
`townhall/DATA.md`를 읽어서:
- `핵심 수치` 섹션 존재 여부
- 실제 수치 데이터(숫자) 포함 여부

### OUTLINE 검증
`townhall/OUTLINE.md`를 읽어서:
- `SLIDE` 키워드 최소 1회 이상
- `헤드라인` 또는 `블록` 섹션 존재 여부

### 코드 검증
`townhall/slides.gs`를 읽어서:
- `addSlides` 함수 존재 여부
- `openById` 사용 여부 (create 사용 시 재생성)
- `getUi` 미사용 여부

---

## 최종 보고 형식

```
✅ 타운홀 슬라이드 생성 완료!

📁 생성 파일:
  townhall/DATA.md     — 수집 데이터
  townhall/OUTLINE.md  — 슬라이드 구조
  townhall/slides.gs   — Apps Script 코드

🖼️ 추가된 슬라이드: N장
🔗 덱 URL: https://docs.google.com/presentation/d/{DECK_ID}/edit
```

---

## 사용 예시

- `"재무 현황 타운홀 슬라이드 만들어줘"` → `/townhall` 트리거
- `"이번 달 타운홀 에이전시로 만들어줘"`
- `"법인 운영 현황 슬라이드 에이전시팀으로 추가해줘"`

---

## 주의사항

- 에이전트 간 소통은 **파일**을 통해서만 (DATA.md → OUTLINE.md → slides.gs)
- 4단계(개발자)는 Chrome 자동화로 오케스트레이터가 직접 실행
- `slides.gs`에 `getUi()`가 있으면 런타임 오류 → 디자이너 에이전트 재실행
- 같은 덱에 중복 실행 시 슬라이드가 누적됨 → 실행 전 사용자에게 확인
- `townhall/` 폴더는 작업 루트(`C:\Users\ash\ash\`)에 생성
