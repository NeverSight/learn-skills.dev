---
name: ppt-design-system
description: "**PPT 한국형 디자인 시스템**: Pretendard + 명조체 조합의 프로페셔널 타이포그라피, 6:3:1 색상 법칙, 한국 비즈니스 PPT 레이아웃 가이드라인을 적용합니다. PptxGenJS 기반 코드 생성 시 네이티브 요소(테이블·차트·이미지·도형·텍스트)를 목적에 맞게 매핑하여 최적 품질의 PPTX를 생성합니다.\n  - MANDATORY TRIGGERS: PPT 디자인, 슬라이드 디자인, 프레젠테이션 디자인, PPT 템플릿, 발표자료, 피치덱, pitch deck, PPT 폰트, 슬라이드 레이아웃"
---

# PPT 한국형 디자인 시스템

## Overview

한국 비즈니스 환경에 최적화된 PPT 디자인 시스템입니다.
Pretendard(고딕) + 조선일보명조(명조) 폰트 조합으로 전문적이고 가독성 높은 슬라이드를 생성합니다.

## ★ PPT 네이티브 요소 매핑 (핵심 원칙)

> **절대 원칙**: 표 형식 데이터는 반드시 `addTable()`을, 수치 비교/추이는 반드시 `addChart()`를 사용한다.
> 도형(`addShape`)과 텍스트(`addText`)로 표/차트를 시뮬레이션하지 않는다.

### 요소 선택 의사결정 트리

```
콘텐츠 유형 판별
├─ 행×열 구조의 데이터인가? ──────────→ addTable()
│   예: 매출표, 일정표, 비교표, 가격표, 스펙표, 예산표
│
├─ 수치의 추이/비교/비율인가? ─────────→ addChart()
│   예: 매출 추이, 점유율, KPI 변화, 분기 비교
│
├─ 외부 이미지/로고/사진인가? ─────────→ addImage()
│   예: 제품 사진, 회사 로고, 스크린샷, 아이콘
│
├─ 단순 텍스트 블록인가? ──────────────→ addText()
│   예: 제목, 본문 단락, 글머리 기호 목록, 인용문
│
├─ 장식/배경/구분선/도형인가? ─────────→ addShape()
│   예: 배경 사각형, 구분선, 강조 바, 아이콘 원형
│
└─ 오디오/비디오인가? ─────────────────→ addMedia()
```

### 요소별 용도 매핑표

| PptxGenJS 메서드 | 용도 | 사용 장면 | 절대 금지 |
|-----------------|------|----------|----------|
| `addTable()` | 구조화된 데이터 | 매출표, 일정표, 비교표, 가격표, 예산표, 스펙표, 커리큘럼표, 인력현황, 체크리스트 | ~~addShape()로 격자 그리기~~ |
| `addChart()` | 데이터 시각화 | 막대차트, 꺾은선, 원형, 도넛, 영역, 방사형, 버블, 산점도 | ~~addShape()로 막대/원 그리기~~ |
| `addImage()` | 외부 이미지 삽입 | 사진, 로고, 스크린샷, SVG→PNG 변환 아이콘 | ~~base64를 addText에 넣기~~ |
| `addText()` | 텍스트 블록 | 제목, 본문, 캡션, 글머리 기호, 인용문, 번호 목록 | ~~표 데이터를 텍스트로 나열~~ |
| `addShape()` | 장식/레이아웃 보조 | 배경 사각형, 구분선, 악센트 바, 카드 배경, 원형 아이콘 배경 | ~~표/차트 시뮬레이션~~ |
| `addNotes()` | 발표자 노트 | 발표 대본, 참고 메모, Q&A 예상 답변 | - |

### ⚠️ 흔한 실수와 교정

```
❌ 잘못된 사용 (표를 도형으로 시뮬레이션)
──────────────────────────────
// 이렇게 하지 말 것!
slide.addShape('rect', { x:1, y:1, w:3, h:0.4, fill:'1A1F36' }); // 헤더 배경
slide.addText('항목', { x:1, y:1, w:1, h:0.4, color:'FFFFFF' }); // 헤더 텍스트
slide.addText('1월', { x:2, y:1, w:1, h:0.4, color:'FFFFFF' });
slide.addShape('line', { x:1, y:1.4, w:3, h:0 });                // 구분선
slide.addText('매출', { x:1, y:1.4, w:1, h:0.4 });               // 데이터 행
slide.addText('100M', { x:2, y:1.4, w:1, h:0.4 });
// ... 수십 줄의 반복 코드

✅ 올바른 사용 (네이티브 테이블)
──────────────────────────────
const rows = [
  [{ text:'항목', options: STYLE.tableHeader },
   { text:'1월',  options: STYLE.tableHeader }],
  [{ text:'매출', options: STYLE.tableCell },
   { text:'100M', options: {...STYLE.tableCellRight} }]
];
slide.addTable(rows, TABLE_OPTIONS);
// 깔끔하고, PowerPoint에서 편집 가능
```

---

## 폰트 시스템

### 기본 폰트 (fonts/ 폴더에 포함)

| 폰트 | 용도 | 파일명 | Weight |
|-------|------|--------|--------|
| **Pretendard** | 고딕 (제목/본문/캡션) | Pretendard-{Weight}.otf | 9종: Thin(100)~Black(900) |
| **조선일보명조** | 명조 (인용/강조/격식) | ChosunilboNM.ttf | Regular |

### Pretendard 9종 Weight 가이드

| Weight | 파일명 | 용도 |
|--------|--------|------|
| Thin (100) | Pretendard-Thin.otf | 장식용 대형 텍스트, 워터마크 |
| ExtraLight (200) | Pretendard-ExtraLight.otf | 부제목(라이트 테마), 배경 텍스트 |
| Light (300) | Pretendard-Light.otf | 긴 본문, 설명 텍스트 |
| Regular (400) | Pretendard-Regular.otf | 기본 본문, 캡션 |
| Medium (500) | Pretendard-Medium.otf | 강조 본문, 라벨 |
| SemiBold (600) | Pretendard-SemiBold.otf | 소제목, 카드 제목 |
| Bold (700) | Pretendard-Bold.otf | 섹션 제목, 헤더 |
| ExtraBold (800) | Pretendard-ExtraBold.otf | 메인 제목, 슬라이드 타이틀 |
| Black (900) | Pretendard-Black.otf | KPI 숫자, 히어로 텍스트 |

### 폰트 적용 규칙

```
제목(Title):     Pretendard ExtraBold / Black    36~44pt
소제목(Subtitle): Pretendard SemiBold / Bold      24~28pt
본문(Body):      Pretendard Regular / Medium      16~20pt
캡션(Caption):   Pretendard Light / Regular       12~14pt
인용구(Quote):   조선일보명조 Regular              18~22pt (격식체, 인용문)
숫자강조(KPI):   Pretendard Black                  48~72pt
장식텍스트:      Pretendard Thin / ExtraLight      60~120pt (배경 대형 텍스트)
```

### 자간(Letter Spacing) & 줄간격(Line Height)

| 요소 | 자간 | 줄간격 | PptxGenJS 속성 |
|------|------|--------|----------------|
| 제목 | -0.5pt ~ 0pt | 1.1배 | `charSpacing: -0.5, lineSpacingMultiple: 1.1` |
| 소제목 | 0pt | 1.2배 | `lineSpacingMultiple: 1.2` |
| 본문 | 0.5pt ~ 1pt | 1.4~1.5배 | `charSpacing: 0.5, lineSpacingMultiple: 1.4` |
| 캡션 | 0.5pt | 1.3배 | `charSpacing: 0.5, lineSpacingMultiple: 1.3` |

## 색상 시스템 (6:3:1 법칙)

### 기본 팔레트: "Midnight Executive"

```javascript
const COLORS = {
  // 메인 60% - 배경/여백
  bg_primary:   'FFFFFF',  // 흰 배경
  bg_secondary: 'F5F7FA',  // 연한 회색 배경
  bg_dark:      '1A1F36',  // 다크 네이비 (표지/구분)

  // 보조 30% - 본문/구조
  text_primary:   '1A1F36', // 제목 텍스트 (다크 네이비)
  text_secondary: '4A5568', // 본문 텍스트 (차콜 그레이)
  text_tertiary:  '718096', // 캡션/보조 (미디엄 그레이)
  text_on_dark:   'FFFFFF', // 다크 배경 위 텍스트

  // 강조 10% - 포인트/CTA
  accent_blue:    '4A7BF7', // 메인 블루
  accent_cyan:    '00D4AA', // 시안 그린
  accent_yellow:  'FFB020', // 골드 옐로우
  accent_red:     'FF6B6B', // 경고/주의 레드
  accent_purple:  '8B5CF6', // 보조 퍼플
};
```

### 추가 팔레트 옵션

#### "Warm Corporate" (따뜻한 기업 톤)
```javascript
const WARM = {
  bg_dark: '2D1B4E', accent_blue: 'E8725A', accent_cyan: '4ECDC4',
  accent_yellow: 'F9C74F', accent_purple: '7B68EE'
};
```

#### "Nature Green" (친환경/ESG)
```javascript
const GREEN = {
  bg_dark: '1B3A2D', accent_blue: '2D9CDB', accent_cyan: '27AE60',
  accent_yellow: 'F2C94C', accent_red: 'EB5757'
};
```

#### "Minimal Mono" (미니멀)
```javascript
const MONO = {
  bg_dark: '111111', accent_blue: '333333', accent_cyan: '666666',
  accent_yellow: 'AAAAAA', text_primary: '111111'
};
```

## 레이아웃 시스템

### 슬라이드 크기
- **발표용**: 16:9 (기본값, 가로 13.33" x 세로 7.5")
- **인쇄/보고서용**: A4 (가로 11.69" x 세로 8.27")

### 여백 가이드 (16:9 기준)

```
+-------------------------------------+
|  0.6"                         0.6"  |
|  +-------------------------------+  |
|  |  콘텐츠 영역                  |  |  상단: 0.5"
|  |  가로: 12.13" / 세로: 6.5"   |  |
|  |                               |  |
|  +-------------------------------+  |
|                                0.5" |  하단: 0.5"
+-------------------------------------+
```

| 영역 | 위치(x, y) | 크기(w, h) |
|------|-----------|-----------|
| 좌측 여백 | x=0.6" | - |
| 우측 여백 | - | w=12.13" (13.33-0.6-0.6) |
| 상단 여백 | y=0.5" | - |
| 하단 여백 | - | h=6.5" (7.5-0.5-0.5) |
| 페이지 번호 | x=12.3", y=7.1" | fontSize: 9pt |

### 핵심 레이아웃 패턴

#### 1. 표지 (Title Slide)
```
[다크 배경 전체]
  중앙: 과정명 (44pt ExtraBold, 흰색)
  중앙 아래: 부제목 (20pt Regular, 70% 흰색)
  하단: 발표자/날짜 (14pt, 50% 흰색)
```

#### 2. 섹션 구분 (Section Divider)
```
[좌측 40% 다크 배경 | 우측 60% 밝은 배경]
  좌측: 섹션 번호 (72pt Black, accent_cyan)
  우측: 섹션 제목 (36pt Bold) + 설명 (16pt Regular)
```

#### 3. 2단 콘텐츠 (Two Column)
```
[상단: 제목 바]
[좌측 50% | 우측 50%]
  각 컬럼: 소제목 (24pt Bold) + 본문 (16pt Regular)
  컬럼 간격: 0.4"
```

#### 4. 카드 그리드 (Card Grid)
```
[상단: 제목 바]
[2x2 또는 2x3 카드 그리드]
  카드: 둥근 모서리 (rectRadius=0.1)
  카드 간격: 0.3"
  카드 헤더: accent 색상 바 (높이 0.08")
```

#### 5. 타임라인 (Timeline)
```
[상단: 제목 바]
[좌측 색상 바 | 우측 항목 리스트]
  각 항목: 시간 (Bold) + 내용 (Regular) + 구분선
```

#### 6. KPI 대시보드 (Data Dashboard)
```
[상단: 제목 바]
[3~4열 KPI 카드]
  숫자: Pretendard Black 48pt (accent 색상)
  라벨: Regular 14pt (text_tertiary)
[하단: 차트/그래프 영역] → addChart() 사용
```

#### 7. 데이터 테이블 (Data Table) — NEW
```
[상단: 제목 바]
[네이티브 테이블] → addTable() 사용
  헤더: 다크 배경 + 흰색 텍스트
  짝수행: 연한 회색 배경 (zebra stripe)
  합계행: bold + 상단 border 강조
```

#### 8. 차트+설명 (Chart & Insight) — NEW
```
[상단: 제목 바]
[좌측 60%: addChart() | 우측 40%: 핵심 인사이트 텍스트]
  인사이트: 숫자 강조 (KPI 스타일) + 짧은 설명
```

---

## PptxGenJS 네이티브 요소 상세 가이드

### 1. addTable() — 테이블

표 형식 데이터는 **반드시** `addTable()`을 사용합니다.

#### 테이블 스타일 상수

```javascript
// ===== 테이블 공통 스타일 =====
const TABLE_STYLE = {
  // 헤더 셀 (다크 배경)
  header: {
    bold: true,
    fill: { color: COLORS.bg_dark },
    color: COLORS.text_on_dark,
    fontFace: 'Pretendard',
    fontSize: 11,
    align: 'center',
    valign: 'middle'
  },
  // 일반 셀
  cell: {
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_secondary,
    valign: 'middle'
  },
  // 숫자 셀 (우측 정렬)
  cellRight: {
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_secondary,
    align: 'right',
    valign: 'middle'
  },
  // 짝수행 배경 (zebra stripe)
  cellAlt: {
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_secondary,
    fill: { color: COLORS.bg_secondary },
    valign: 'middle'
  },
  // 합계/소계 행
  cellTotal: {
    bold: true,
    fontFace: 'Pretendard',
    fontSize: 11,
    color: COLORS.text_primary,
    border: [{ type: 'solid', pt: 1.5, color: COLORS.text_primary }, null, null, null],
    valign: 'middle'
  }
};

// 테이블 공통 옵션
const TABLE_OPTIONS = {
  x: 0.6,
  y: 1.8,  // 제목 바 아래
  w: 12.13,
  border: { type: 'solid', pt: 0.5, color: 'E2E8F0' },
  autoPage: false,
  margin: [5, 8, 5, 8]  // 셀 내부 여백 [top, right, bottom, left] pt
};
```

#### 테이블 헬퍼 함수

```javascript
/**
 * 디자인 시스템 적용된 테이블 추가
 * @param {Slide} slide
 * @param {string[]} headers - 헤더 텍스트 배열
 * @param {Array<Array<string|{text,options}>>} dataRows - 데이터 행 배열
 * @param {object} opts - 추가 옵션 (x, y, w, colW, rowH 등)
 */
function addStyledTable(slide, headers, dataRows, opts = {}) {
  const rows = [];

  // 헤더 행
  rows.push(headers.map(h => ({
    text: h,
    options: { ...TABLE_STYLE.header }
  })));

  // 데이터 행 (zebra stripe 자동 적용)
  dataRows.forEach((row, i) => {
    const isAlt = i % 2 === 1;
    const baseStyle = isAlt ? TABLE_STYLE.cellAlt : TABLE_STYLE.cell;
    rows.push(row.map(cell => {
      if (typeof cell === 'string') {
        return { text: cell, options: { ...baseStyle } };
      }
      // {text, options} 객체인 경우 스타일 병합
      return { text: cell.text, options: { ...baseStyle, ...cell.options } };
    }));
  });

  slide.addTable(rows, {
    ...TABLE_OPTIONS,
    ...opts
  });
}

/**
 * colspan을 활용한 제목 행 포함 테이블
 */
function addTitledTable(slide, tableTitle, headers, dataRows, opts = {}) {
  const colCount = headers.length;
  const rows = [];

  // 테이블 제목 행 (colspan 병합)
  rows.push([{
    text: tableTitle,
    options: {
      colspan: colCount,
      bold: true,
      fill: { color: COLORS.bg_dark },
      color: COLORS.text_on_dark,
      fontFace: 'Pretendard',
      fontSize: 13,
      align: 'center',
      valign: 'middle'
    }
  }]);

  // 헤더 행
  rows.push(headers.map(h => ({
    text: h,
    options: {
      bold: true,
      fill: { color: COLORS.bg_secondary },
      color: COLORS.text_primary,
      fontFace: 'Pretendard',
      fontSize: 11,
      align: 'center',
      valign: 'middle'
    }
  })));

  // 데이터 행
  dataRows.forEach((row, i) => {
    const isAlt = i % 2 === 1;
    rows.push(row.map(cell => {
      const base = isAlt
        ? { ...TABLE_STYLE.cellAlt }
        : { ...TABLE_STYLE.cell };
      if (typeof cell === 'string') return { text: cell, options: base };
      return { text: cell.text, options: { ...base, ...cell.options } };
    }));
  });

  slide.addTable(rows, { ...TABLE_OPTIONS, ...opts });
}
```

#### 테이블 사용 예시

```javascript
// ===== 매출 계획표 =====
addTitledTable(slide, '2026년 매출 계획표',
  ['구분', 'Q1', 'Q2', 'Q3', 'Q4', '연간 합계'],
  [
    ['온라인',
     { text: '120M', options: { align: 'right' } },
     { text: '150M', options: { align: 'right' } },
     { text: '180M', options: { align: 'right' } },
     { text: '200M', options: { align: 'right' } },
     { text: '650M', options: { align: 'right', bold: true } }],
    ['오프라인',
     { text: '80M', options: { align: 'right' } },
     { text: '90M', options: { align: 'right' } },
     { text: '100M', options: { align: 'right' } },
     { text: '110M', options: { align: 'right' } },
     { text: '380M', options: { align: 'right', bold: true } }],
  ],
  { colW: [2, 1.8, 1.8, 1.8, 1.8, 2.5] }
);

// ===== 일정표/시간표 =====
addStyledTable(slide,
  ['교시', '시간', '과목', '내용', '비고'],
  [
    ['1', '09:00~09:50', 'Excel 기초', '데이터 정리 자동화', '이론'],
    ['2', '10:00~10:50', 'Excel 분석', 'KPI 대시보드 설계', '이론+실습'],
    ['3', '11:00~11:50', 'PPT 생성', '슬라이드 자동 변환', '이론'],
  ],
  { colW: [1, 2.2, 2.5, 4, 1.8], rowH: [0.45, 0.4, 0.4, 0.4] }
);

// ===== 비교표 (스펙/기능 비교) =====
addStyledTable(slide,
  ['기능', 'Free', 'Pro', 'Enterprise'],
  [
    ['스킬 수', '12개', { text: '24개', options: { bold: true, color: COLORS.accent_blue } }, '무제한'],
    ['지원', '커뮤니티', '이메일', { text: '전담 매니저', options: { bold: true } }],
    ['가격', '무료', '월 9,900원', '문의'],
  ]
);
```

### 2. addChart() — 차트

수치 데이터의 추이/비교/비율은 **반드시** `addChart()`를 사용합니다.

#### 차트 스타일 상수

```javascript
// ===== 차트 공통 스타일 =====
const CHART_STYLE = {
  // 공통 기본값
  base: {
    showTitle: true,
    titleFontFace: 'Pretendard',
    titleFontSize: 14,
    titleColor: COLORS.text_primary,
    showLegend: true,
    legendFontFace: 'Pretendard',
    legendFontSize: 9,
    legendColor: COLORS.text_secondary,
    catAxisLabelFontFace: 'Pretendard',
    catAxisLabelFontSize: 10,
    catAxisLabelColor: COLORS.text_tertiary,
    valAxisLabelFontFace: 'Pretendard',
    valAxisLabelFontSize: 10,
    valAxisLabelColor: COLORS.text_tertiary,
  },
  // 차트 색상 팔레트 (최대 6색)
  colors: [
    COLORS.accent_blue,     // 4A7BF7
    COLORS.accent_cyan,     // 00D4AA
    COLORS.accent_yellow,   // FFB020
    COLORS.accent_red,      // FF6B6B
    COLORS.accent_purple,   // 8B5CF6
    '38BDF8'                // 라이트 블루 (6번째)
  ]
};
```

#### 차트 유형별 사용 기준

| 데이터 유형 | 차트 유형 | PptxGenJS 상수 |
|------------|----------|---------------|
| 항목별 크기 비교 | 세로 막대 | `pptx.charts.BAR` |
| 시계열 추이/변화 | 꺾은선 | `pptx.charts.LINE` |
| 전체 대비 비율 (5개 이하) | 원형 | `pptx.charts.PIE` |
| 전체 대비 비율 (중앙 KPI) | 도넛 | `pptx.charts.DOUGHNUT` |
| 추이 + 누적량 | 영역 | `pptx.charts.AREA` |
| 다차원 항목 비교 | 방사형 | `pptx.charts.RADAR` |
| 두 변수 간 관계 | 산점도 | `pptx.charts.SCATTER` |
| 세 변수 관계 | 버블 | `pptx.charts.BUBBLE` |

#### 차트 헬퍼 함수

```javascript
/**
 * 디자인 시스템 적용된 차트 추가
 * @param {Slide} slide
 * @param {object} pptx - PptxGenJS 인스턴스 (charts 참조용)
 * @param {string} type - 'BAR'|'LINE'|'PIE'|'DOUGHNUT'|'AREA'|'RADAR'|'SCATTER'
 * @param {Array} chartData - [{name, labels, values}]
 * @param {object} opts - 위치/크기/추가 옵션
 */
function addStyledChart(slide, pptx, type, chartData, opts = {}) {
  const typeMap = {
    BAR: pptx.charts.BAR,
    LINE: pptx.charts.LINE,
    PIE: pptx.charts.PIE,
    DOUGHNUT: pptx.charts.DOUGHNUT,
    AREA: pptx.charts.AREA,
    RADAR: pptx.charts.RADAR,
    SCATTER: pptx.charts.SCATTER,
    BUBBLE: pptx.charts.BUBBLE
  };

  const defaults = {
    x: 0.6, y: 1.8, w: 12.13, h: 5.0,
    ...CHART_STYLE.base,
    chartColors: CHART_STYLE.colors.slice(0, chartData.length || 6),
    ...opts
  };

  // 차트 유형별 기본값 추가
  if (type === 'BAR') {
    defaults.barGapWidthPct = 80;
    defaults.catAxisOrientation = 'minMax';
    defaults.valAxisOrientation = 'minMax';
  }
  if (type === 'LINE') {
    defaults.lineDataSymbol = 'circle';
    defaults.lineDataSymbolSize = 8;
    defaults.lineSmooth = false;
  }
  if (type === 'PIE' || type === 'DOUGHNUT') {
    defaults.showPercent = true;
    defaults.showLegend = true;
    defaults.legendPos = 'b';
    defaults.chartColors = CHART_STYLE.colors.slice(0, chartData[0]?.values?.length || 6);
  }

  slide.addChart(typeMap[type], chartData, defaults);
}
```

#### 차트 사용 예시

```javascript
// ===== 매출 추이 (꺾은선) =====
addStyledChart(slide, pptx, 'LINE',
  [{ name: '매출(억)', labels: ['1월','2월','3월','4월','5월','6월'],
     values: [12, 15, 18, 22, 25, 30] }],
  { x: 0.6, y: 1.8, w: 7, h: 4.5, title: '2026 상반기 매출 추이' }
);

// ===== 부서별 비교 (막대) =====
addStyledChart(slide, pptx, 'BAR',
  [
    { name: '목표', labels: ['영업','마케팅','개발','인사'], values: [100, 80, 120, 50] },
    { name: '실적', labels: ['영업','마케팅','개발','인사'], values: [95, 85, 110, 48] }
  ],
  { x: 0.6, y: 1.8, w: 12.13, h: 5, title: '부서별 목표 대비 실적' }
);

// ===== 구성비 (원형) =====
addStyledChart(slide, pptx, 'PIE',
  [{ name: '점유율', labels: ['제품A','제품B','제품C','기타'],
     values: [45, 25, 20, 10] }],
  { x: 3, y: 1.5, w: 7, h: 5, title: '제품별 매출 구성비' }
);

// ===== 진행률 (도넛) =====
addStyledChart(slide, pptx, 'DOUGHNUT',
  [{ name: '진행률', labels: ['완료','잔여'], values: [75, 25] }],
  { x: 4, y: 2, w: 5, h: 4, title: '프로젝트 진행률',
    chartColors: [COLORS.accent_cyan, 'E2E8F0'] }
);
```

### 3. addImage() — 이미지

```javascript
// 파일 경로로 삽입
slide.addImage({
  path: '/path/to/image.png',
  x: 0.6, y: 1.8, w: 5, h: 3.5
});

// SVG → PNG 변환 후 삽입 (sharp 라이브러리)
const sharp = require('sharp');
const svgBuffer = Buffer.from(svgString);
const pngBuffer = await sharp(svgBuffer).png().toBuffer();
const base64 = pngBuffer.toString('base64');
slide.addImage({
  data: 'image/png;base64,' + base64,
  x: 0.6, y: 1.8, w: 5, h: 3.5
});

// 로고 삽입 (우측 하단)
slide.addImage({
  path: '/path/to/logo.png',
  x: 11.5, y: 6.8, w: 1.2, h: 0.5
});
```

### 4. addText() — 텍스트

```javascript
// 제목
slide.addText('슬라이드 제목', {
  x: 0.6, y: 0.65, w: 10, h: 0.6,
  fontSize: 28, fontFace: 'Pretendard', bold: true,
  color: COLORS.text_primary, charSpacing: -0.3
});

// 글머리 기호 목록 (bullet: true)
slide.addText([
  { text: '첫 번째 항목', options: { bullet: true, indentLevel: 0 } },
  { text: '두 번째 항목', options: { bullet: true, indentLevel: 0 } },
  { text: '하위 항목', options: { bullet: true, indentLevel: 1 } },
], {
  x: 0.6, y: 1.8, w: 12.13, h: 4,
  fontSize: 16, fontFace: 'Pretendard',
  color: COLORS.text_secondary,
  lineSpacingMultiple: 1.5,
  paraSpaceAfter: 6
});

// 번호 목록 (bullet: {type:'number'})
slide.addText([
  { text: '첫 번째 단계', options: { bullet: { type: 'number' } } },
  { text: '두 번째 단계', options: { bullet: { type: 'number' } } },
], {
  x: 0.6, y: 1.8, w: 12.13, h: 3,
  fontSize: 16, fontFace: 'Pretendard',
  color: COLORS.text_secondary
});

// 인용문 (명조체)
slide.addText('\u201C변화를 두려워하지 마세요\u201D', {
  x: 2, y: 3, w: 9, h: 1,
  fontSize: 22, fontFace: 'ChosunilboNM', italic: true,
  color: COLORS.text_tertiary, align: 'center'
});
```

### 5. addShape() — 장식/레이아웃 보조만

```javascript
// ✅ 올바른 사용: 배경 영역
slide.addShape('rect', {
  x: 0, y: 0, w: '100%', h: '100%',
  fill: { color: COLORS.bg_dark }
});

// ✅ 올바른 사용: 악센트 라인
slide.addShape('rect', {
  x: 0.6, y: 0.5, w: 1.2, h: 0.06,
  fill: { color: COLORS.accent_blue }
});

// ✅ 올바른 사용: 카드 배경 (둥근 모서리)
slide.addShape('roundRect', {
  x: 0.6, y: 1.8, w: 5.5, h: 3,
  rectRadius: 0.1,
  fill: { color: 'FFFFFF' },
  shadow: { type: 'outer', blur: 6, offset: 2, color: '00000015' }
});

// ✅ 올바른 사용: 구분선
slide.addShape('line', {
  x: 0.6, y: 4, w: 12.13, h: 0,
  line: { color: 'E2E8F0', width: 0.5 }
});

// ❌ 금지: 표 격자를 도형으로 그리기
// ❌ 금지: 막대 차트를 사각형으로 그리기
```

### 6. addNotes() — 발표자 노트

```javascript
slide.addNotes('이 슬라이드에서는 매출 추이를 설명합니다.\n핵심 포인트: Q3 성장률 40% 강조');
```

---

## PptxGenJS 코드 컨벤션

### 폰트 임베딩

```javascript
// Pretendard OTF 경로 (스킬 폴더 기준)
const FONT_DIR = path.join(__dirname, 'fonts');

// PptxGenJS에서 폰트 등록은 지원하지 않으므로
// 시스템에 Pretendard가 설치된 환경에서 다음과 같이 사용:
const FONTS = {
  title:    { fontFace: 'Pretendard', bold: true },   // ExtraBold/Black
  subtitle: { fontFace: 'Pretendard', bold: true },   // SemiBold/Bold
  body:     { fontFace: 'Pretendard', bold: false },   // Regular/Medium
  caption:  { fontFace: 'Pretendard', bold: false },   // Light/Regular
  serif:    { fontFace: 'ChosunilboNM', bold: false }, // 조선일보명조
  kpi:      { fontFace: 'Pretendard', bold: true },    // Black
  deco:     { fontFace: 'Pretendard', bold: false },   // Thin/ExtraLight (장식용)
};
```

### 슬라이드 생성 헬퍼

```javascript
// 표준 제목 바 추가 함수
function addTitleBar(slide, title, subtitle = '') {
  // 얇은 accent 라인
  slide.addShape('rect', {
    x: 0.6, y: 0.5, w: 1.2, h: 0.06,
    fill: { color: COLORS.accent_blue }
  });
  // 제목
  slide.addText(title, {
    x: 0.6, y: 0.65, w: 10, h: 0.6,
    fontSize: 28, fontFace: 'Pretendard', bold: true,
    color: COLORS.text_primary, charSpacing: -0.3
  });
  // 부제목 (있을 경우)
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.6, y: 1.25, w: 10, h: 0.4,
      fontSize: 16, fontFace: 'Pretendard',
      color: COLORS.text_tertiary
    });
  }
}

// 카드 생성 함수 (장식용 - 데이터 표시 아님)
function addCard(slide, { x, y, w, h, title, body, accentColor }) {
  // 카드 배경
  slide.addShape('roundRect', {
    x, y, w, h, rectRadius: 0.1,
    fill: { color: 'FFFFFF' },
    shadow: { type: 'outer', blur: 6, offset: 2, color: '00000015' }
  });
  // 상단 accent 바
  slide.addShape('rect', {
    x: x + 0.02, y, w: w - 0.04, h: 0.06,
    fill: { color: accentColor || COLORS.accent_blue }
  });
  // 카드 제목
  slide.addText(title, {
    x: x + 0.2, y: y + 0.2, w: w - 0.4, h: 0.35,
    fontSize: 16, fontFace: 'Pretendard', bold: true,
    color: COLORS.text_primary
  });
  // 카드 본문
  slide.addText(body, {
    x: x + 0.2, y: y + 0.55, w: w - 0.4, h: h - 0.75,
    fontSize: 13, fontFace: 'Pretendard',
    color: COLORS.text_secondary,
    lineSpacingMultiple: 1.4, valign: 'top'
  });
}

// 페이지 번호 추가
function addPageNumber(slide, num, total) {
  slide.addText(`${num} / ${total}`, {
    x: 12.0, y: 7.05, w: 1.0, h: 0.3,
    fontSize: 9, fontFace: 'Pretendard',
    color: COLORS.text_tertiary, align: 'right'
  });
}
```

## 실전 슬라이드 구성 패턴

### 패턴 A: 매출 보고 슬라이드

```javascript
const slide = pptx.addSlide();
addTitleBar(slide, '월별 매출 실적', '2026년 상반기');

// 상단: KPI 카드 3개 (addText + addShape)
// → KPI 숫자는 카드 형태 = addShape(배경) + addText(숫자)
['매출 합계|₩3.2B', '전년 대비|+18%', '목표 달성률|94%'].forEach((item, i) => {
  const [label, value] = item.split('|');
  addCard(slide, {
    x: 0.6 + i * 4.1, y: 1.6, w: 3.8, h: 1.2,
    title: label, body: value, accentColor: CHART_STYLE.colors[i]
  });
});

// 중단: 데이터 테이블 (addTable)
addStyledTable(slide, ['월','매출','비용','영업이익','이익률'], [...data],
  { y: 3.1, rowH: [0.4, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35] });
```

### 패턴 B: 비교 분석 슬라이드

```javascript
const slide = pptx.addSlide();
addTitleBar(slide, '경쟁사 비교 분석');

// 좌측: 비교 차트 (addChart)
addStyledChart(slide, pptx, 'BAR',
  [
    { name: '자사', labels: ['가격','품질','서비스','인지도'], values: [85, 92, 88, 70] },
    { name: '경쟁A', labels: ['가격','품질','서비스','인지도'], values: [90, 80, 75, 85] }
  ],
  { x: 0.6, y: 1.6, w: 6.5, h: 5.2, title: '' }
);

// 우측: 비교표 (addTable)
addStyledTable(slide, ['항목','자사','경쟁A'],
  [['가격', '85', '90'], ['품질', '92', '80'], ['서비스', '88', '75']],
  { x: 7.5, y: 1.6, w: 5.2 }
);
```

### 패턴 C: 프로젝트 현황 대시보드

```javascript
const slide = pptx.addSlide();
addTitleBar(slide, '프로젝트 현황 대시보드', '2026년 2월 기준');

// 좌측 상단: 진행률 도넛 (addChart)
addStyledChart(slide, pptx, 'DOUGHNUT',
  [{ name: '진행', labels: ['완료','잔여'], values: [72, 28] }],
  { x: 0.6, y: 1.6, w: 4, h: 3, showTitle: false,
    chartColors: [COLORS.accent_cyan, 'E2E8F0'] }
);

// 우측 상단: 주간 이슈 테이블 (addTable)
addStyledTable(slide, ['이슈','담당','상태','기한'],
  [['서버 지연', '김개발', '진행중', '2/20'],
   ['UI 버그', '박디자', '완료', '2/18']],
  { x: 5, y: 1.6, w: 7.7, rowH: [0.4, 0.35, 0.35] }
);

// 하단: 마일스톤 타임라인 (addTable로 구현 가능)
addStyledTable(slide, ['마일스톤','시작일','종료일','진행률','상태'],
  [['기획', '1/15', '2/10', '100%', '\u2705'],
   ['개발', '2/11', '4/30', '45%', '\uD83D\uDD27'],
   ['테스트', '5/1', '5/31', '0%', '\u23F3']],
  { x: 0.6, y: 5.0, w: 12.13, rowH: [0.4, 0.35, 0.35, 0.35] }
);
```

---

## 6x6 콘텐츠 규칙

- 슬라이드 당 **글머리 기호 최대 6개**
- 글머리 당 **단어 6개 이내** (한글 기준 15~18자)
- 한 슬라이드에 **핵심 메시지 1개**
- 텍스트가 많으면 **2장으로 분할**

## 이미지 & 아이콘 가이드

### SVG 아이콘 사용
- 별도 `svg-diagram` 스킬을 활용하여 테마 색상에 맞는 SVG 아이콘/다이어그램 생성
- SVG → PNG 변환 후 삽입 (sharp 라이브러리 활용)

### Hero Image 규칙
- 한 슬라이드에 핵심 이미지 1개만 사용
- 이미지 선택 기준: 주제, 분위기, 해상도, 색상, 여백

## 2025-2026 한국형 PPT 디자인 트렌드

### 기능적 미니멀리즘
- 불필요한 장식 요소 배제, 콘텐츠 중심 디자인
- 넓은 여백(White Space) 적극 활용
- 한 슬라이드 = 한 메시지 원칙 강화
- 배경: 순백(#FFFFFF) 또는 연한 회색(#F5F7FA~#F8FAFC) 기본

### 모듈형 레이아웃
- 카드 기반 그리드 시스템 (2x2, 2x3, 1+2 변형)
- 각 모듈에 독립적 정보 단위 배치
- 모듈 간 일관된 간격(0.3"~0.4") 유지
- 반복 가능한 레이아웃 패턴으로 일관성 확보

### 포인트 컬러 전략
- 배경: 라이트 그레이 (#F5F7FA)
- 포인트: 네이비(#1A1F36) + 1~2가지 악센트 컬러
- 6:3:1 법칙: 배경 60% + 텍스트 30% + 강조 10%
- 그라데이션보다 단색(Flat) 선호

### 타이포그래피
- **Pretendard** -- 한국 비즈니스 PPT 표준 폰트로 자리매김
- 가변폰트(Variable Font) 활용으로 세밀한 두께 조절
- 제목은 ExtraBold~Black, 본문은 Regular~Medium
- 자간: 제목 타이트(-0.5pt), 본문 약간 넓게(+0.5pt)
- 명조체(조선일보명조)는 인용구/강조에만 포인트 사용

### 데이터 시각화 강화
- 숫자 중심 KPI 카드 레이아웃 인기
- 복잡한 3D 차트 대신 2D 플랫 차트 (addChart 활용)
- 아이콘 + 숫자 조합의 인포그래픽 스타일
- SVG 도식화 연계 (svg-diagram 스킬 활용)

## 체크리스트 (QA)

문서 생성 후 다음을 확인:
- [ ] 제목 36~44pt / 소제목 24~28pt / 본문 16~20pt 범위 내
- [ ] 자간: 제목 -0.5~0pt / 본문 0.5~1pt
- [ ] 줄간격: 본문 1.4배 이상
- [ ] 색상 6:3:1 비율 준수
- [ ] 여백: 좌우 0.6" / 상하 0.5" 이상
- [ ] 한 슬라이드 1 메시지 원칙
- [ ] 폰트 2종 이내 (Pretendard + 명조)
- [ ] 한글 깨짐 없음 (Pretendard 폰트 확인)
- [ ] **표 데이터 → addTable() 사용 확인** (도형 시뮬레이션 금지)
- [ ] **수치 비교/추이 → addChart() 사용 확인** (도형 시뮬레이션 금지)
- [ ] **이미지/로고 → addImage() 사용 확인**
- [ ] **글머리 기호 → addText({ bullet: true }) 사용 확인**
