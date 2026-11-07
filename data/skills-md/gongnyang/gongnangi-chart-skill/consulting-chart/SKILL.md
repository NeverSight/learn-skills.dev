---
name: consulting-chart
description: "공냥이 시각 콘텐츠 스킬 — 컨설팅 차트, 인스타 카드뉴스, 애니메이션 영상을 HTML/CSS 코드로 생성. 5가지 카드뉴스 디자인 테마 선택 가능."
allowed-tools: [Bash, Write, Read, Edit]
---

# 공냥이 시각 콘텐츠 스킬

3가지 기능:
- **공냥이 차트** — 컨설팅 스타일 데이터 차트 (960x500 PNG)
- **공냥이 카드뉴스** — 인스타 카드뉴스 5가지 디자인 (1080x1350 PNG)
- **공냥이 영상** — Remotion 애니메이션 차트 (MP4/GIF)

---

## STEP 0: 사전 질문 (반드시 먼저 실행)

**코드를 작성하기 전에 반드시 사용자에게 다음을 질문한다.** 바로 만들지 않는다.

### 공냥이 차트 요청 시

```
1. 어떤 데이터를 차트로 만들까요? (항목명 + 수치)
2. 차트 유형은? (바 차트 / 비교표 / A vs B / 프로세스 / 타임라인)
3. 강조할 항목은? (빨강으로 표시할 것)
4. 제목은? (인사이트 형태 — "매출 추이" X, "Q4 매출 15% 급등" O)
5. 출처(Source)는?
```

### 공냥이 카드뉴스 요청 시

```
1. 주제/내용은 무엇인가요? (텍스트 파일 경로 또는 직접 입력)
2. 몇 장짜리로 만들까요? (4장 / 6장 / 9장)
3. 각 장에 들어갈 핵심 메시지는? (제가 제안할까요, 직접 정해주실 건가요?)
4. 디자인 테마는? (editorial / impact / grid / dark-slim / minimal)
   - 잘 모르겠으면 제가 주제에 맞는 테마를 추천합니다
5. 레퍼런스 스타일이 있나요? (참고할 카드뉴스 URL이나 계정)
6. 핸들/브랜드명은? (하단에 표시할 @이름)
```

**질문 후 기획안을 먼저 텍스트로 제출:**
```
=== 카드뉴스 기획안 ===
테마: impact
장수: 4장
핸들: @gongnangi

[1장 - 커버]
핵심 숫자: 0.25%
제목: 프롬프트 엔지니어링은 끝났다
설명: ...

[2장 - 데이터]
차트 유형: 슬림 바 차트
데이터: 도구출력 80%, 대화기록 5%, ...
인사이트: ...

[3장 - 인용구]
인용: "just the right information..."
저자: Andrej Karpathy

[4장 - 프레임워크]
구조: Write / Select / Compress / Isolate
...
=== 기획안 끝 ===

이대로 만들까요?
```

**사용자가 승인한 후에만 코드 작성 시작.**

### 빈 공간 절대 금지 (최우선 규칙)

**이 규칙은 다른 모든 규칙보다 우선한다.**

- 캔버스의 빈 공간이 20%를 넘으면 안 된다
- 하단에 빈 공간이 보이면 → 폰트를 키우거나 내용을 추가해서 채운다
- margin:auto, flex:1, justify-content:space-between 등으로 요소를 흩뿌리지 않는다
- 모든 요소는 위에서 아래로 빈틈없이 쌓는다 (gap은 24-32px 이내)
- 렌더 후 PNG를 반드시 Read로 열어서 빈 공간을 눈으로 확인한다
- 빈 공간이 보이면 수정 후 재렌더한다 (자동, 최대 3회)

### 공냥이 영상 요청 시

```
1. 어떤 차트를 영상으로 만들까요? (바 차트 / 카운트업 / 프레임워크 순차등장)
2. 데이터는? (기존 차트 재활용 or 새로 만들기)
3. 사이즈는? (960x500 차트용 / 1080x1350 카드뉴스용 / 1920x1080 가로 와이드)
4. 출력 형식은? (MP4 / GIF / 둘 다)
```

---

## 렌더 후 품질 검증 피드백 루프 (필수)

PNG 렌더 후 반드시 5단계 검증을 실행한다. 하나라도 FAIL이면 수정 후 재렌더 (최대 3회).

### 1단계: 잘림 체크
```bash
# 2배 높이로 렌더하여 하단 잘림 확인
CHROME --screenshot=check.png --window-size=1080,2700 file.html
# check.png 크기가 정상의 1.5배 이상이면 OVERFLOW → FAIL
```

### 2단계: 시각 확인 (Read로 PNG 열기)
- 텍스트가 잘 보이는가 (다크 배경에서 #555 이하는 안 보임 → #999+)
- 하단 빈 공간 20%+ 이면 → FAIL
- 바 차트가 슬림 6px 스타일인가
- border 박스가 없는가
- 미니 프리뷰/스워치가 너무 작아서 깨지지 않는가

### 3단계: OCR 가독성 테스트
Read로 PNG를 열어 모든 텍스트가 눈으로 읽히는지 확인:
- 글자가 깨지거나 잘려서 읽을 수 없으면 → FAIL
- 폰트 14px 미만이 뭉개지면 → FAIL
- 미니 프리뷰 안 텍스트도 읽혀야 함 → 안 읽히면 프리뷰 키우거나 텍스트 제거

### 4단계: 자가 평가 체크리스트
```
□ 빈 공간이 20% 미만인가?
□ 모든 텍스트가 읽히는가? (깨진 글자 없는가?)
□ 각 요소의 특징이 구별되는가? (같은 내용 반복 아닌가?)
□ 색상 대비가 충분한가? (배경 대비 텍스트 명도차 50%+)
□ 바 차트가 슬림 6px 스타일인가?
□ 박스 테두리(border)가 없는가?
□ 하단에 핸들/출처가 있는가?
□ 잘리는 콘텐츠가 없는가?
```

### 5단계: 실패 시 자동 수정
- OVERFLOW → padding 줄이거나 font-size 줄이기
- 텍스트 안 보임 → 색상 올리기 (#555 → #999)
- 글자 깨짐 → font-size 키우기 또는 해당 요소 제거
- 빈 공간 과다 → font-size 키우기 또는 설명 추가
- 특징 구별 안 됨 → 각 항목에 다른 콘텐츠/색상 적용
- 수정 후 재렌더 → 1단계부터 재검증 (최대 3회 반복)

---

## Design Principles

McKinsey/Bain/BCG consulting report standard:

1. **Color**: Default everything grayscale. Accent is **red (#c0392b) only**.
2. **Zero decoration**: No emoji. No icons. No gradients. No rounded corners. No shadows.
3. **Typography**: Title = insight (not description). Numbers large, labels small. Noto Sans KR.
4. **Structure**: Lines thin and precise. Whitespace intentional. Every pixel carries data.
5. **Source**: Always include `Source:` line at the bottom.
6. **Action Title**: Title must pass "So What?" test. Quantify where possible.
7. **Philosophy**: "Everything loud means nothing stands out. One thing catches the eye."

---

## Design Tokens

```json
{
  "color": {
    "title": "#111", "body": "#222", "cell": "#333",
    "secondary": "#555", "label": "#888", "subtitle": "#999",
    "source": "#bbb", "connector": "#ccc", "bar-default": "#d5d5d5",
    "divider": "#eee", "bar-bg": "#f5f5f5", "cell-bg": "#fafafa",
    "warning-bg": "#fdf5f5", "accent": "#c0392b"
  },
  "typography": {
    "chart": { "title": "22px/700", "sub": "11px/400", "source": "9px/300" },
    "cardnews": {
      "hero": "72px/700", "title": "48px/700", "heading": "36px/700",
      "subhead": "28px/400", "body": "24px/400", "label": "18px/400",
      "caption": "14px/300", "source": "12px/300"
    }
  },
  "layout": {
    "chart": "960x500",
    "cardnews": "1080x1350"
  }
}
```

---

## Base CSS (Chart Mode — 960px)

```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Noto Sans KR',sans-serif;background:#fff;padding:28px 36px 20px;width:960px;color:#222}
.title{font-size:22px;font-weight:700;color:#111;margin-bottom:2px}
.sub{font-size:11px;color:#999;margin-bottom:24px}
.source{font-size:9px;color:#bbb;margin-top:18px}
```

## Base CSS (Card News Mode — 1080x1350)

```css
body{width:1080px;height:1350px;padding:80px 72px 60px;display:flex;flex-direction:column}
.slide-num{font-size:14px;color:#ccc;margin-bottom:40px}
.title{font-size:40px;font-weight:700;color:#111;line-height:1.3;margin-bottom:40px}
.body{font-size:24px;color:#555;line-height:1.7}
.highlight{color:#c0392b;font-weight:700}
.bottom{font-size:12px;color:#ccc;margin-top:auto}
```

---

## Chart Types

### 1. Horizontal Bar Chart
- Default bar: `background:#d5d5d5`, Highlight: `background:#c0392b`
- Labels left-aligned, values right. Bar height 18-22px, background #f5f5f5

### 2. Comparison Table
- Header: 10px, #999, bottom 2px solid #111
- Cell: 11px, #333, bottom 1px solid #eee. Highlight: color:#c0392b

### 3. Side-by-Side (A vs B)
- `display:flex;gap:1px;background:#eee` — 1px divider
- Highlight side title in #c0392b

### 4. Process / Flow
- Numbers: 28-32px, bold, #d5d5d5 (highlight: #c0392b). Arrows: `→`, color:#ccc

### 5. Timeline
- Horizontal axis: height:2px, background:#222. Nodes: 14px circles. Current: #c0392b

### 6. Level / Severity
- Color bar tags + description. Scale: #c0392b → #e67e22 → #555 → #999

---

## Card News — 5 Design Themes

Instagram 4:5 portrait (1080x1350). 사용자가 디자인을 선택하면 해당 스타일로 전체 세트 생성.

### 디자인 선택

| # | Theme | Background | Accent | Layout | Feel |
|---|-------|-----------|--------|--------|------|
| 1 | **editorial** | #FAFAFA 라이트 | #FF4444 | 좌측정렬 비대칭 | 매거진 |
| 2 | **impact** | #0A0A0A 다크 | #c0392b | 중앙정렬 | 극적 임팩트 |
| 3 | **grid** | #F0EBE3 + #2C2C2C | #8B6F4E | 좌우 2단 분할 | 구조적 |
| 4 | **dark-slim** | #0A0A0A 다크 | #c0392b | 좌측정렬 | 슬림 차트 |
| 5 | **minimal** | #F5F5F5 라이트 | #c0392b | 중앙정렬 | 흑백 미니멀 |

기본값: `impact` (디자인 미지정 시)

### 공통 타이포그래피 규칙

```
핵심 숫자: 160-200px, weight 900, letter-spacing -6px
제목 핵심: 48-56px, weight 900
제목 연결어: 같은 크기, weight 100-300 (대비)
본문: 22-28px, weight 300-500, line-height * 1.618
라벨: 11-13px, letter-spacing 3-5px, uppercase
```

- 한 줄마다 다른 크기/굵기/색상 (같은 스타일 3줄 연속 금지)
- 콘텐츠가 캔버스의 70%+ 차지
- padding: 상단 100px, 좌우 72px, 하단 72px
- safe zone: 상하 135px (인스타 그리드 잘림 방지)
- 하단: 좌측 시리즈명 + 우측 @핸들

### 공통 바 차트 규칙 (슬림 스타일)

```css
.bar-track{height:6px;background:#f5f5f5}  /* 라이트 */
.bar-track{height:6px;background:#1A1A1A}  /* 다크 */
.bar-accent{background:#c0392b}
.bar-mid{background:#888}
.bar-light{background:#CCC}
```

### 슬라이드 구조 (SCQA + Pyramid)

| Slide | Role | Content |
|-------|------|---------|
| cover | Hook | 핵심 숫자 + 제목 + 설명 |
| data | Complication | 슬림 바 차트 + "왜 한계인가" 설명 |
| quote | Pivot | 핵심 인용구, 줄마다 굵기/색상 대비 |
| framework | Evidence | 프레임워크/축, 번호+이름+설명 계층 |

### 금지사항

- border-radius, box-shadow 금지
- border로 박스 만들기 금지 (구분선 border-top/bottom만 허용)
- margin:auto로 빈 공간 분배 금지
- 같은 스타일 텍스트 3줄 연속 금지

---

## Animation System (Remotion)

React + Remotion으로 spring 물리 기반 애니메이션 → MP4/GIF 렌더.
WSL에서 `LD_LIBRARY_PATH` 설정 필요 (install.sh가 자동 안내).

### Remotion 컴포지션 목록

**차트 애니메이션 (960x500)**
| ID | 설명 | 애니메이션 |
|---|------|----------|
| BarChart | 수평 바 차트 | 바가 0에서 spring으로 올라옴 |
| CountUp | 숫자 카운트업 | 0→목표 숫자 spring 감속 |
| FourAxis | 4축 프레임워크 | 축이 하나씩 슬라이드인 |
| CompareAB | A vs B 양방향 비교 | 양쪽 바가 동시에 성장 |
| ProcessFlow | 프로세스 흐름 | 스텝이 순서대로 등장 + 화살표 |
| QuoteReveal | 인용구 | 줄마다 굵기/색상 다르게 등장 |
| TableReveal | 테이블 | 행이 순서대로 슬라이드인 |
| NumberPulse | 숫자 강조 | 큰 숫자 팝인 + 반복 펄스 |
| Timeline | 타임라인 | 축 그리기 + 노드 순서 등장 |

**카드뉴스 영상화 (1080x1350 / 1920x1080)**
| ID | 설명 | 애니메이션 |
|---|------|----------|
| CardCover | 커버 슬라이드 | 숫자 팝 → 제목 슬라이드인 → 설명 페이드 |
| CardData | 데이터 슬라이드 | 제목 → 바 순차 성장 → 인사이트 등장 |
| BarChart-Card | 바 차트 (카드뉴스 사이즈) | BarChart의 1080x1350 버전 |
| CardCover-Wide | 커버 (와이드) | 1920x1080 가로형 |
| CardData-Wide | 데이터 (와이드) | 1920x1080 가로형 |

**쇼릴 (1920x1080)**
| ID | 설명 |
|---|------|
| SkillIntro | 스킬 소개 (3 in 1) |
| Showreel | 전체 합본 (Intro→Chart→CardNews→Outro) |

### Animation Patterns

```css
/* Bar grow */
@keyframes barGrow{from{width:0}to{width:var(--target)}}
.bar{animation:barGrow 0.8s cubic-bezier(0.25,0.46,0.45,0.94) forwards}

/* Fade in with slide up */
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

/* Scale in (for numbers) */
@keyframes scaleIn{from{transform:scale(0.5)}to{transform:scale(1)}}
```

### Stagger Timing
- Title: 0s
- Subtitle: 0.2s
- Data rows: 0.4s + (index * 0.2s)
- Source line: last animation + 0.5s
- Hold final frame: +1 second

### Capture Pipeline (PowerShell + Windows Chrome)

```powershell
# Frame capture with virtual time
& $chrome --headless=new --disable-gpu --hide-scrollbars `
    --screenshot="$outFile" `
    --window-size=960,500 `
    --virtual-time-budget=$timeMs `
    "file:///$htmlPath"
```

### Encode Pipeline (ffmpeg)

```bash
FFMPEG="path/to/ffmpeg.exe"

# GIF (high quality with palette optimization)
"$FFMPEG" -y -r 15 -i "frames/frame-%04d.png" \
  -vf "fps=15,scale=960:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  output.gif

# MP4 (H.264)
"$FFMPEG" -y -r 15 -i "frames/frame-%04d.png" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 \
  output.mp4

# APNG (animated PNG, infinite loop)
"$FFMPEG" -y -r 15 -i "frames/frame-%04d.png" \
  -plays 0 output.apng
```

---

## PNG Export (Static)

```bash
CHROME="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"

# Chart (960x500)
"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --screenshot="D:\\output\\chart.png" \
    --window-size=960,500 \
    "file:///D:/input/chart.html"

# Card News (1080x1350)
"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --screenshot="D:\\output\\card.png" \
    --window-size=1080,1350 \
    "file:///D:/input/card.html"
```

---

## Prohibited

- Emoji
- Gradients (linear-gradient)
- border-radius (except tables)
- box-shadow
- More than 1 background color on badges/tags
- Any "decorative" element — if it's not data, it doesn't belong
- Description titles ("매출 추이") — always action titles ("Q4 매출 15% 급등")
