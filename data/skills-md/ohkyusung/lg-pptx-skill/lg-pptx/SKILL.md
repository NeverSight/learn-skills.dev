---
name: lg-pptx
description: 사내 보고서·발표자료 작성 시간을 획기적으로 줄여주는 PPTX 자동 생성 스킬입니다. 에이투지체 폰트와 사내 디자인 컨벤션(액센트 블록, L-브래킷 장식, 컬러 시스템)을 자동 적용하여 직원들이 콘텐츠에만 집중할 수 있게 합니다. 28종 슬라이드 타입(표지, 목차, 내용, 로드맵, 테이블, SWOT, KPI, 타임라인, 프로세스, 간트차트, 조직도, 피라미드, 포지셔닝맵, 키워드강조, 스윔레인, 제언 등)과 matplotlib 차트/이미지 삽입을 지원합니다. "PPT 만들어줘", "발표자료 만들어줘", "보고서 PPT", "주간보고 슬라이드", "제안서 만들어줘", "간트차트 PPT", "조직도 슬라이드", "차트 넣어줘", "이미지 PPT", "SWOT 분석 PPT", "KPI 대시보드", "프로젝트 일정표", "비교 분석 자료", "전략 보고서", "리스크 매트릭스", "스윔레인", "업무 프로세스 다이어그램", "역할별 흐름도", "제언 슬라이드" 같은 요청에 트리거됩니다. 한국어와 영어 프레젠테이션 모두 지원합니다.
---

# 사내 PPTX 자동 생성 스킬 (에이투지체)

사내 디자인 컨벤션을 따르는 프레젠테이션을 자동 생성하여, 직원들의 보고서 작성 시간을 줄이고 일하는 방식을 혁신하는 스킬입니다.

## Quick Reference

| 작업 | 방법 |
|------|------|
| 새 프레젠테이션 생성 | `scripts/lg_pptx_builder.py` 임포트 후 `LGPresentation` 클래스 사용 |
| 디자인 토큰 확인 | `references/design-tokens.md` 참조 |
| 커스텀 레이아웃 | 빌더 메서드 조합으로 자유 구성 |

## 사전 준비: 에이투지체 폰트 설치

이 스킬은 **에이투지체(A2Z)** 폰트가 시스템에 설치되어 있어야 정상 렌더링됩니다.
폰트가 없으면 맑은 고딕으로 대체됩니다.

**다운로드 링크:**
- 공식 배포: https://freesentation.blog/a2z
- 눈누 폰트 플랫폼: https://noonnu.cc/font_page/1778

**설치 방법:**
1. 위 링크에서 폰트 파일(.ttf/.otf)을 다운로드
2. macOS: 다운로드한 파일을 더블클릭 → "서체 설치" 버튼 클릭
3. Windows: 다운로드한 파일 우클릭 → "설치" 또는 "모든 사용자용으로 설치"

**설치 확인 (터미널):**
```bash
# macOS/Linux
fc-list | grep -i "에이투지체"
# 출력 예: /Users/.../에이투지체 4 Regular.ttf: 에이투지체 4 Regular:style=Regular
```

> 라이선스: 에이투지체는 OFL(Open Font License)로 상업적·개인적 용도 모두 무료 사용 가능합니다.

## Workflow

### Step 1: 의존성 확인

```bash
pip install python-pptx Pillow matplotlib
```

### Step 2: 프레젠테이션 생성

빌더 스크립트를 사용해 프레젠테이션을 생성합니다. 아래는 기본 패턴입니다:

```python
import sys
sys.path.insert(0, '<skill-scripts-path>')
from lg_pptx_builder import LGPresentation

# 프레젠테이션 생성
prs = LGPresentation(
    font_name="에이투지체",     # 기본 폰트 (한글+영문 모두)
    font_name_latin="에이투지체",  # 라틴 폰트도 동일
    logo_path=None              # LG 로고 이미지 경로 (선택)
)

# 슬라이드 추가
prs.add_cover("프로젝트 제목", subtitle="팀명", date="2025.01.01")
prs.add_toc([
    ("Summary", []),
    ("시스템 소개", ["항목 1", "항목 2", "항목 3"]),
    ("첨부자료", [])
])
prs.add_content("1.1 시스템 개요", section="Summary", bullets=["내용1", "내용2"])
prs.add_roadmap(
    title="[SPC] 로드맵",
    section="로드맵",
    subtitle="설명 텍스트",
    years=["(2025) Phase 1", "(2026) Phase 2", "(2027) Phase 3"],
    roadmap_items={...},
    table_data={...}
)
prs.save("output.pptx")
```

### Step 3: QA 검증

생성된 PPTX를 검증합니다:
1. `markitdown` 으로 텍스트 추출하여 내용 확인
2. 가능하면 `soffice` → `pdftoppm` 으로 이미지 변환하여 시각적 확인

## Design System Overview

LG 그룹 프레젠테이션의 핵심 디자인 요소입니다. 상세 토큰은 `references/design-tokens.md`를 참조하세요.

### Color Palette

| 역할 | 색상 | HEX | 용도 |
|------|------|-----|------|
| Primary | LG RED | `#A50034` | 브래킷, 액센트 바, TOC 번호, 강조 |
| Text Primary | Black | `#000000` | 제목, 본문 |
| Text Secondary | Dark Gray | `#333333` | 부제목, 보조 텍스트 |
| Text Tertiary | Medium Gray | `#666666` | 섹션명, 캡션 |
| Background | White | `#FFFFFF` | 슬라이드 배경 |
| Surface | Light Gray | `#F2F2F2` | 콘텐츠 박스 배경 |
| Header Bar | Charcoal | `#3C3C3C` | 타임라인 헤더, 테이블 헤더 |
| Accent Green | Green | `#2E7D32` | 미래/계획 항목 |
| Accent Orange | Orange | `#D4760A` | 하이라이트 항목 |

### Typography

- **폰트**: 에이투지체 — 한글+영문 모두 동일 폰트 적용
- 시스템에 폰트가 없는 경우 "맑은 고딕" 또는 "Malgun Gothic" 사용
- East Asian 폰트 설정 필수 (python-pptx에서 `<a:ea>` XML 요소 직접 설정)

| 용도 | 크기 | 굵기 | 색상 |
|------|------|------|------|
| 표지 제목 | 32pt | Bold | Black |
| 표지 부제 | 14pt | Regular | Dark Gray |
| 섹션 제목 | 28pt | Bold | Black |
| 본문 제목 | 16pt | Bold | Black |
| 본문 | 12pt | Regular | Black/Dark Gray |
| 표 헤더 | 10pt | Bold | White |
| 표 본문 | 9pt | Regular | Black |
| 캡션/주석 | 8pt | Regular | Medium Gray |

### Slide Types

#### 1. Cover (표지)
- 흰 배경
- **좌상단 L-브래킷**: LG RED, 두께 ~0.4cm, 팔 길이 ~2.5cm
- **우하단 L-브래킷**: LG RED, 180도 회전 (대칭)
- 중앙: 제목 (Bold, 32pt, Black)
- 하단 중앙: 부제 + 날짜 (14pt, Dark Gray)
- 우하단 (브래킷 안): LG 로고 (선택)

#### 2. Table of Contents (목차)
- 흰 배경
- 상단: 얇은 회색 가로선
- 좌측: "Contents" 텍스트 (28pt, Black) + 짧은 빨간 밑줄 바 (~3cm)
- 아래: 회색 구분선
- 목차 항목: 로마 숫자 (LG RED, Bold) + 항목명
- 하위 항목: 들여쓰기 + dash prefix (Black)

#### 3. Content (내용 슬라이드)
- 흰 배경
- **좌상단 액센트 블록**: LG RED 작은 사각형 (0.5cm x 1.4cm), 제목 왼쪽에 위치
- 제목: 액센트 블록 오른쪽에 번호+제목 (Bold, 24pt, Black) — 예: "1.1 공정 DX 서비스"
- 우상단: 섹션명 (12pt, Medium Gray) + 빨간 원형 인디케이터
- 본문 영역: 자유 구성 (텍스트, 박스, 표 등)

#### 4. Roadmap (로드맵)
- Content 슬라이드 기본 구조 유지 (좌측 레드 바, 제목, 섹션명)
- 부제: 설명 텍스트 (14pt, Dark Gray)
- **타임라인 헤더**: 다크 차콜 (#3C3C3C) 쉐브론/화살표, 연도 + 설명 (White, Bold)
- **좌측 라벨 블록**: 다크 레드 (#A50034) 세로 블록, 라벨 텍스트 (White, Bold)
- **콘텐츠 그리드**: 연도별 컬럼, 라이트 그레이 배경 셀
- 텍스트 색상: 검정(기본), 초록(미래 계획), 주황(하이라이트)
- **하단 테이블** (선택): 비교 표

#### 5. Comparison Table (비교 테이블)
- Content 슬라이드 기본 구조
- 다크 차콜 헤더 행 (White Bold 텍스트)
- 얇은 회색 테두리
- 교대 행 배경 (White / Light Gray)

#### 6. Summary Matrix (요약 매트릭스)
- Content 슬라이드 기본 구조 (액센트 블록 + 제목)
- **좌측 2열**: 카테고리(세로 병합) + 서브라벨 (회색 배경)
- **상단 헤더**: 다크 차콜 배경, 흰색 텍스트 (계열사/항목명)
- 셀 내용: 좌측 정렬, 연도별 불릿 텍스트
- 얇은 회색 테두리

#### 7. Two Column (2단 레이아웃)
- Content 슬라이드 기본 구조
- 좌우 2개 컬럼, 각각 제목 + 불릿 포인트
- 비교, Before/After, 장단점 분석에 적합

#### 8. KPI Cards (핵심 지표)
- Content 슬라이드 기본 구조
- 가로 나란히 배치된 카드들 (Light Gray 배경)
- 큰 숫자 (40pt, 색상 커스텀 가능) + 라벨 텍스트
- 경영진 보고, 성과 요약에 적합

#### 9. Timeline (타임라인)
- Content 슬라이드 기본 구조
- 가로 타임라인 선 + 빨간 원형 마커
- 날짜 (상단, LG RED) + 제목/설명 (하단)
- 프로젝트 일정, 마일스톤 표현

#### 10. Process Flow (프로세스 흐름)
- Content 슬라이드 기본 구조
- 가로 정렬된 단계 박스 (차콜 헤더 + 라이트 그레이 본문)
- 단계 사이 화살표 연결
- 워크플로우, 시스템 아키텍처 개요

#### 11. SWOT Analysis (SWOT 분석)
- Content 슬라이드 기본 구조
- 2x2 그리드: 강점(RED), 약점(CHARCOAL), 기회(GREEN), 위협(ORANGE)
- 각 사분면: 컬러 헤더 + 라이트 그레이 본문 + 불릿

#### 12. Gantt Chart (간트 차트)
- Content 슬라이드 기본 구조
- 좌측: 태스크명 + 담당자 목록, 우측: 월별 타임라인 그리드
- 바 차트: 태스크별 컬러 바 (시작~종료), 완료율 표시
- 마일스톤 마커 (빨간 다이아몬드)
- 프로젝트 일정 관리, WBS 표현에 적합

#### 13. Org Chart (조직도)
- Content 슬라이드 기본 구조
- 최상위 노드 (LG RED 배경) → 하위 노드 (차콜 배경) 계층 구조
- 수직 커넥터 라인으로 연결
- 각 노드: 직책/이름 + 부서/역할 텍스트
- 조직 구조, 보고 체계 시각화

#### 14. Pyramid (피라미드 다이어그램)
- Content 슬라이드 기본 구조
- 위에서 아래로 넓어지는 사다리꼴 레이어
- 각 레이어: 컬러 배경 + 제목/설명 텍스트
- 전략 계층, 가치 피라미드, 우선순위 표현

#### 15. Positioning Map (포지셔닝 맵)
- Content 슬라이드 기본 구조
- X/Y 축 교차 2D 맵 + 사분면 라벨
- 항목별 원형 마커 (크기/색상 커스텀)
- 경쟁사 분석, 시장 포지셔닝, BCG 매트릭스

#### 16. Keyword Highlight (키워드 강조)
- Content 슬라이드 기본 구조
- 태그 클라우드 스타일: 키워드별 크기/색상/굵기 차등
- 하단 설명 텍스트
- 핵심 메시지, 비전/미션, 키워드 요약

#### 17. Swimlane (스윔레인 프로세스)
- Content 슬라이드 기본 구조
- 역할/부서별 수평 레인 (수영장 레인 스타일)
- 레인 내 프로세스 단계 박스 배치 (라운드 사각형)
- 같은 레인 이동: 수평 화살표, 다른 레인 이동: L자형 커넥터
- 레인별 고유 색상 (RED, CHARCOAL, BLUE, GREEN, ORANGE, PURPLE)
- 업무 프로세스, R&R 구분, 시스템 간 연동 흐름 표현

#### 18. Recommendation (제언)
- Content 슬라이드 기본 구조
- 번호 원형 (LG RED) + 제목 + 상세 설명
- 클로징 직전 배치, 핵심 제언/권고사항 정리
- 문자열 리스트 또는 {title, detail} 딕셔너리 리스트 지원

#### 19. Chart Slide (차트 이미지)
- Content 슬라이드 기본 구조
- 외부 차트 이미지 파일(.png/.jpg) 중앙 배치
- 하단 캡션 텍스트
- matplotlib/seaborn 등으로 생성한 차트 삽입

#### 18. Image Slide (이미지 배치)
- Content 슬라이드 기본 구조
- 1~4장 이미지 자동 레이아웃 (1장=전체, 2장=좌우, 3장+=그리드)
- 이미지별 캡션 텍스트
- 스크린샷, 사진, 다이어그램 배치

#### 19. Matplotlib Chart (직접 삽입)
- Content 슬라이드 기본 구조
- matplotlib Figure 객체를 직접 전달 → 자동 렌더링
- 임시 파일 생성 후 삽입, 자동 정리
- 데이터 분석 결과 즉시 슬라이드화

## Key Design Rules

1. **일관성**: 모든 내용 슬라이드에 좌상단 빨간 액센트 블록 적용
2. **밀도 우선**: 보고서/리서치용 빡빡한 레이아웃 — 상하 0.5cm, 좌측 1.5cm, 우측 0.5cm 최소 여백
3. **색상 절제**: LG RED는 강조에만 사용, 과용 금지
4. **계층 구조**: 제목 → 부제 → 본문 크기/굵기 차이로 시각적 계층 표현
5. **박스 스타일**: 둥근 모서리 없음 (직각 사각형), 라이트 그레이 배경
6. **라벨 뱃지**: 카테고리 라벨은 LG RED 배경 + White 텍스트의 작은 사각형
7. **표 스타일**: 헤더는 다크 차콜 배경, 테두리는 얇은 회색
8. **차트/이미지**: matplotlib Figure 직접 삽입 또는 이미지 파일 배치 지원

## Builder API Reference

`scripts/lg_pptx_builder.py`의 `LGPresentation` 클래스는 다음 메서드를 제공합니다:

### 생성자
```python
LGPresentation(font_name="에이투지체", font_name_latin="에이투지체", logo_path=None)
```

### 슬라이드 메서드

| 메서드 | 설명 |
|--------|------|
| `add_cover(title, subtitle, date, logo_path)` | 표지 슬라이드 |
| `add_toc(items)` | 목차 슬라이드 |
| `add_section_divider(number, title)` | 섹션 구분 슬라이드 |
| `add_content(title, section, body, bullets)` | 일반 내용 슬라이드 |
| `add_roadmap(title, section, subtitle, years, roadmap_items, table_data)` | 로드맵 슬라이드 |
| `add_table(title, section, headers, rows)` | 테이블 슬라이드 |
| `add_summary_matrix(title, section, headers, row_groups)` | 요약 매트릭스 (카테고리 병합 테이블) |
| `add_two_column(title, section, left_title, left_bullets, right_title, right_bullets)` | 2단 레이아웃 |
| `add_kpi_cards(title, section, kpis)` | KPI/핵심 지표 카드 |
| `add_timeline(title, section, milestones)` | 타임라인 슬라이드 |
| `add_process_flow(title, section, steps)` | 프로세스 흐름도 |
| `add_swot(title, section, strengths, weaknesses, opportunities, threats)` | SWOT 분석 |
| `add_architecture(title, section, subtitle, columns, rows)` | 멀티컬럼 아키텍처/시스템 구조도 |
| `add_strategy_pillars(title, section, subtitle, pillars)` | 전략 필러 (3~5개 수직 컬럼) |
| `add_risk_matrix(title, section, subtitle, risks)` | 3x3 리스크 평가 매트릭스 |
| `add_financial_summary(title, section, subtitle, categories)` | 투자/예산 요약 테이블 (소계+합계) |
| `add_milestone_tracker(title, section, subtitle, phases)` | 마일스톤 추적 (상태별 색상) |
| `add_comparison_cards(title, section, subtitle, cards)` | 솔루션/옵션 비교 카드 |
| `add_gantt_chart(title, section, subtitle, tasks, start_date, months)` | 간트 차트 (프로젝트 일정) |
| `add_org_chart(title, section, subtitle, org_data)` | 조직도 (계층 구조) |
| `add_pyramid(title, section, subtitle, levels)` | 피라미드 다이어그램 |
| `add_positioning_map(title, section, subtitle, x_label, y_label, items, quadrant_labels)` | 2D 포지셔닝 맵 |
| `add_keyword_highlight(title, section, subtitle, keywords, description)` | 키워드 강조/태그 클라우드 |
| `add_swimlane(title, section, subtitle, lanes, steps, connections)` | 스윔레인 프로세스 다이어그램 |
| `add_recommendation(title, section, subtitle, recommendations)` | 제언/권고사항 (클로징 전) |
| `add_chart_slide(title, section, subtitle, chart_path, caption)` | 차트 이미지 삽입 |
| `add_image_slide(title, section, subtitle, images)` | 이미지 배치 (1~4장 자동 레이아웃) |
| `add_matplotlib_chart(title, section, subtitle, fig, caption)` | matplotlib Figure 직접 삽입 |
| `save(filename)` | PPTX 파일 저장 |

### 헬퍼 메서드 (내부)

| 메서드 | 설명 |
|--------|------|
| `_set_font(run)` | Latin + EA 폰트 동시 설정 |
| `_add_l_bracket(slide, corner, arm_len, thickness, color)` | L-브래킷 장식 |
| `_add_accent_bar(slide)` | 좌측 빨간 액센트 바 |
| `_add_section_indicator(slide, section_name)` | 우상단 섹션명 + 빨간 점 |
| `_add_slide_title(slide, title)` | 제목 텍스트 추가 |

## Common Patterns

### 내용이 많은 슬라이드

콘텐츠가 한 슬라이드에 다 안 들어갈 때:
- 같은 섹션 제목으로 여러 슬라이드 분할
- 제목에 "(1/2)", "(2/2)" 등 페이지 표시
- 각 슬라이드에 동일한 액센트 바 + 섹션 인디케이터 유지

### 다이어그램/아키텍처 슬라이드

복잡한 다이어그램은 python-pptx의 기본 도형으로 구성:
- 사각형 (`add_shape`) + 텍스트로 블록 구성
- 화살표/커넥터로 연결
- 카테고리 라벨: LG RED 배경 소형 사각형
- 콘텐츠 블록: Light Gray 배경 사각형

### 로드맵 구성

로드맵 슬라이드의 `roadmap_items` 파라미터 구조:
```python
roadmap_items = {
    "label": "시스템 로드맵",  # 좌측 라벨
    "rows": [
        {
            "items_by_year": [
                # Year 1 items
                [{"text": "항목 1", "tag": "LGES", "tag_color": "#1565C0"}],
                # Year 2 items
                [{"text": "항목 2", "color": "green"}],
                # Year 3 items
                [{"text": "항목 3", "color": "orange"}]
            ]
        }
    ]
}
```

### 간트 차트 구성

```python
prs.add_gantt_chart(
    title="프로젝트 일정표", section="일정",
    subtitle="2025년 상반기",
    start_date="2025-01",
    months=6,
    tasks=[
        {"name": "요구사항 분석", "owner": "김팀장", "start": 0, "duration": 2, "progress": 100, "color": "#A50034"},
        {"name": "설계", "owner": "이과장", "start": 1, "duration": 3, "progress": 60},
        {"name": "개발", "owner": "박대리", "start": 3, "duration": 4, "progress": 0},
        {"name": "Go-Live", "owner": "", "start": 5, "duration": 0, "milestone": True},
    ]
)
```

### 조직도 구성

```python
prs.add_org_chart(
    title="조직 구조", section="조직",
    org_data={
        "name": "CEO", "title": "대표이사",
        "children": [
            {"name": "CTO", "title": "기술총괄", "children": [
                {"name": "개발팀", "title": "팀장 김OO"},
                {"name": "인프라팀", "title": "팀장 이OO"},
            ]},
            {"name": "CFO", "title": "재무총괄"},
        ]
    }
)
```

### 피라미드 다이어그램

```python
prs.add_pyramid(
    title="전략 계층 구조", section="전략",
    levels=[
        {"label": "비전", "description": "글로벌 No.1", "color": "#A50034"},
        {"label": "전략", "description": "디지털 전환 가속화"},
        {"label": "실행 과제", "description": "AI·데이터·클라우드 역량 강화"},
        {"label": "기반", "description": "인재·문화·인프라"},
    ]
)
```

### 포지셔닝 맵

```python
prs.add_positioning_map(
    title="경쟁사 포지셔닝", section="분석",
    x_label="가격 경쟁력", y_label="기술력",
    quadrant_labels=["고가·고기술", "저가·고기술", "고가·저기술", "저가·저기술"],
    items=[
        {"label": "자사", "x": 0.7, "y": 0.8, "size": 1.5, "color": "#A50034"},
        {"label": "경쟁사A", "x": 0.3, "y": 0.6, "size": 1.0},
        {"label": "경쟁사B", "x": 0.5, "y": 0.4, "size": 1.2, "color": "#2E7D32"},
    ]
)
```

### 키워드 강조

```python
prs.add_keyword_highlight(
    title="핵심 키워드", section="요약",
    description="2025년 전략 방향의 핵심 키워드입니다.",
    keywords=[
        {"text": "디지털 전환", "size": 36, "color": "#A50034", "bold": True},
        {"text": "AI", "size": 32, "color": "#1565C0", "bold": True},
        {"text": "클라우드", "size": 28},
        {"text": "자동화", "size": 24, "color": "#2E7D32"},
        {"text": "데이터", "size": 26, "bold": True},
    ]
)
```

### matplotlib 차트 삽입

```python
import matplotlib.pyplot as plt

# 방법 1: Figure 객체 직접 전달
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(["Q1", "Q2", "Q3", "Q4"], [120, 145, 160, 180])
ax.set_title("분기별 매출")
prs.add_matplotlib_chart(title="매출 추이", section="실적", fig=fig, caption="단위: 억원")
plt.close(fig)

# 방법 2: 이미지 파일로 저장 후 삽입
fig.savefig("/tmp/chart.png", dpi=150, bbox_inches="tight")
prs.add_chart_slide(title="매출 차트", section="실적", chart_path="/tmp/chart.png", caption="2025년 실적")
```

### 이미지 배치

```python
prs.add_image_slide(
    title="현장 사진", section="현황",
    images=[
        {"path": "/tmp/photo1.jpg", "caption": "공장 전경"},
        {"path": "/tmp/photo2.jpg", "caption": "생산라인"},
    ]
)
```

### 스윔레인 프로세스

```python
prs.add_swimlane(
    title="도입 업무 프로세스", section="프로세스",
    lanes=["고객사", "PM", "개발팀", "QA팀"],
    steps=[
        {"lane": 0, "col": 0, "text": "요구사항 전달", "color": "#A50034"},
        {"lane": 1, "col": 1, "text": "분석/설계"},
        {"lane": 2, "col": 2, "text": "개발", "color": "#1565C0"},
        {"lane": 3, "col": 3, "text": "테스트", "color": "#2E7D32"},
        {"lane": 0, "col": 4, "text": "최종 승인", "color": "#A50034"},
    ],
    connections=[(0,1), (1,2), (2,3), (3,4)],
)
```

### 제언 (클로징 전 권고사항)

```python
# 방법 1: 간단한 문자열 리스트
prs.add_recommendation(
    title="제언", section="제언",
    recommendations=["데이터 품질 확보 최우선", "단계적 도입 전략 수립"]
)

# 방법 2: 제목 + 상세 설명
prs.add_recommendation(
    title="제언", section="제언",
    recommendations=[
        {"title": "데이터 품질 확보", "detail": "입력 데이터 정합성 검증 체계를 초기부터 확립"},
        {"title": "단계적 도입", "detail": "파일럿 → 확대 적용 → 전사 확산 순서로 진행"},
    ]
)
```
