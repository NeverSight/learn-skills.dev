---
name: stitch-design-md
description: "Stitch 프로젝트를 분석하여 DESIGN.md 파일을 생성합니다 — 디자인 시스템을 시맨틱하고 자연스러운 언어로 문서화하여 일관된 UI 생성을 지원합니다. Triggers on: Stitch, 디자인 시스템, DESIGN.md, Stitch 디자인 분석. NOT for: React 컴포넌트 변환, 코드 구현."
user-invocable: true
allowed-tools:
  - "stitch*:*"
  - "mcp__stitch*"
  - "Read"
  - "Write"
  - "mcp__tavily__tavily_extract"
---

# Stitch DESIGN.md 스킬

당신은 전문 디자인 시스템 리더입니다. Stitch 프로젝트의 기술 자산을 분석하고, `DESIGN.md` 파일로 시맨틱 디자인 시스템을 합성하는 것이 목표입니다.

## 개요

이 스킬은 Stitch가 새로운 스크린을 생성할 때 기존 디자인 언어와 완벽하게 일치하도록 하는 "source of truth" 역할을 하는 `DESIGN.md` 파일을 생성합니다.

Stitch는 특정 색상 값으로 뒷받침되는 "시각적 설명"을 통해 디자인을 해석합니다.

## 사전 요구사항

- Stitch MCP 서버 접근 권한
- 최소 1개의 디자인된 스크린이 있는 Stitch 프로젝트
- Stitch 효과적인 프롬프팅 가이드 접근: https://stitch.withgoogle.com/docs/learn/prompting/

## 검색 및 네트워킹

Stitch 프로젝트를 분석하려면 Stitch MCP 서버 도구를 사용하여 스크린 메타데이터와 디자인 자산을 검색해야 합니다:

### 1. 네임스페이스 탐색

```bash
# list_tools를 실행하여 Stitch MCP 접두사 찾기
# 이 접두사(예: mcp_stitch:)를 모든 후속 호출에 사용
```

### 2. 프로젝트 조회 (Project ID가 없는 경우)

```
[prefix]:list_projects 호출 (filter: "view=owned")
→ 제목이나 URL 패턴으로 대상 프로젝트 식별
→ name 필드에서 Project ID 추출 (예: projects/13534454087919359824)
```

### 3. 스크린 조회 (Screen ID가 없는 경우)

```
[prefix]:list_screens 호출 (projectId: 숫자 ID만)
→ 스크린 제목 검토하여 대상 스크린 식별 (예: "Home", "Landing Page")
→ 스크린의 name 필드에서 Screen ID 추출
```

### 4. 메타데이터 가져오기

```
[prefix]:get_screen 호출 (projectId, screenId: 둘 다 숫자 ID만)
반환되는 정보:
- screenshot.downloadUrl: 디자인의 시각적 참조
- htmlCode.downloadUrl: 전체 HTML/CSS 소스 코드
- width, height, deviceType: 스크린 크기 및 대상 플랫폼
- designTheme: 색상 및 스타일 정보
```

### 5. 자산 다운로드

```
web_fetch 또는 read_url_content로 htmlCode.downloadUrl에서 HTML 코드 다운로드
선택적으로 screenshot.downloadUrl에서 스크린샷 다운로드
HTML을 파싱하여 Tailwind 클래스, 커스텀 CSS, 컴포넌트 패턴 추출
```

## 분석 및 합성 지침

### 1. 프로젝트 아이덴티티 추출

- 프로젝트 제목 찾기
- 특정 Project ID 찾기 (JSON의 `name` 필드에서)

### 2. 분위기 정의

스크린샷과 HTML 구조를 평가하여 전체적인 "분위기"를 포착합니다.
분위기를 설명하는 형용사 사용:
- "Airy" (공기처럼 가벼운)
- "Dense" (밀집된)
- "Minimalist" (미니멀리스트)
- "Utilitarian" (실용주의적)

### 3. 색상 팔레트 매핑

시스템의 핵심 색상을 식별합니다. 각 색상에 대해 제공:

| 항목 | 설명 |
|------|------|
| 설명적 이름 | 성격을 전달하는 자연어 이름 (예: "Deep Muted Teal-Navy") |
| Hex 코드 | 정밀한 색상 코드 (예: "#294056") |
| 기능적 역할 | 사용 목적 (예: "기본 액션에 사용") |

### 4. 기하학 및 형태 번역

기술적 `border-radius` 값을 물리적 설명으로 변환:

| Tailwind 클래스 | 설명 |
|----------------|------|
| `rounded-full` | 알약 모양 (Pill-shaped) |
| `rounded-lg` | 미묘하게 둥근 모서리 |
| `rounded-xl` | 넉넉하게 둥근 모서리 |
| `rounded-none` | 날카로운 직각 모서리 |

### 5. 깊이 및 고도 설명

UI가 레이어를 처리하는 방식을 설명합니다:

- "Flat" (평면적)
- "Whisper-soft diffused shadows" (속삭이듯 부드러운 확산 그림자)
- "Heavy, high-contrast drop shadows" (무거운 고대비 드롭 섀도우)

## 출력 가이드라인

- **언어**: 설명적 디자인 용어와 자연어 사용
- **형식**: 아래 구조를 따르는 깨끗한 Markdown 파일 생성
- **정밀도**: 설명적 이름과 함께 정확한 hex 코드 포함
- **맥락**: "무엇"뿐만 아니라 "왜"에 대해 설명

## 출력 형식 (DESIGN.md 구조)

```markdown
# Design System: [프로젝트 제목]

**Project ID:** [프로젝트 ID]

## 1. 시각적 테마 및 분위기

(분위기, 밀도, 미학적 철학에 대한 설명)

## 2. 색상 팔레트 및 역할

| 이름 | Hex 코드 | 역할 |
|------|----------|------|
| Deep Ocean Blue | #0077B6 | 기본 액션 버튼 |
| Whisper Gray | #F5F5F5 | 배경 색상 |
| Midnight Text | #1A1A1A | 본문 텍스트 |

## 3. 타이포그래피 규칙

(폰트 패밀리, 헤더 vs 본문의 굵기 사용, 자간 특성에 대한 설명)

## 4. 컴포넌트 스타일링

### 버튼
- 형태: 알약 모양, 넉넉한 패딩
- 색상: 기본 - Deep Ocean Blue, 호버 시 밝아짐
- 동작: 미묘한 고도 상승 효과

### 카드/컨테이너
- 모서리: 부드럽게 둥근 (8px)
- 배경: 순백색
- 그림자: 속삭이듯 부드러운 확산 그림자

### 입력/폼
- 테두리: 1px Whisper Gray
- 배경: 순백색
- 포커스: Deep Ocean Blue 테두리

## 5. 레이아웃 원칙

(여백 전략, 마진, 그리드 정렬에 대한 설명)

## 6. Stitch 생성을 위한 디자인 시스템 노트

**[이 섹션을 stitch-loop 스킬의 프롬프트에 복사하세요]**

```
비주얼 스타일: [분위기 설명]
기본 색상: [이름] (#hex) - [역할]
보조 색상: [이름] (#hex) - [역할]
배경: [이름] (#hex)
텍스트: [이름] (#hex)
버튼 스타일: [형태, 색상, 동작]
카드 스타일: [모서리, 그림자]
전체적인 느낌: [2-3문장 요약]
```
```

## 사용 예시

### 1. 프로젝트 정보 검색

```
Stitch MCP 서버를 사용하여 "My App" 프로젝트 가져오기
```

### 2. 홈 페이지 스크린 상세 정보 가져오기

```
홈 페이지 스크린의 코드, 이미지, 스크린 객체 정보 검색
```

### 3. 모범 사례 참조

```
Stitch 효과적인 프롬프팅 가이드 검토:
https://stitch.withgoogle.com/docs/learn/prompting/
```

### 4. 분석 및 합성

- 스크린에서 모든 관련 디자인 토큰 추출
- 기술적 값을 설명적 언어로 번역
- DESIGN.md 구조에 따라 정보 구성

### 5. 파일 생성

- 프로젝트 디렉토리에 `DESIGN.md` 생성
- 지정된 형식을 정확히 따르기
- 모든 색상 코드가 정확한지 확인
- 디자이너 친화적인 감성적 언어 사용

## 모범 사례

| 원칙 | 설명 |
|------|------|
| 설명적으로 | "blue" 대신 "Ocean-deep Cerulean (#0077B6)" 사용 |
| 기능적으로 | 각 디자인 요소의 용도 항상 설명 |
| 일관되게 | 문서 전체에서 동일한 용어 사용 |
| 시각적으로 | 설명을 통해 독자가 디자인을 시각화할 수 있게 |
| 정밀하게 | 자연어 설명 뒤에 정확한 값 포함 |

## 피해야 할 함정

- ❌ 번역 없이 기술 용어 사용 (예: "rounded-xl" 대신 "넉넉하게 둥근 모서리")
- ❌ 색상 코드 누락 또는 설명적 이름만 사용
- ❌ 디자인 요소의 기능적 역할 설명 누락
- ❌ 분위기 설명이 너무 모호함
- ❌ 그림자나 간격 패턴 같은 미묘한 디자인 세부사항 무시

## 리소스

- **Stitch 공식 문서**: https://stitch.withgoogle.com/docs/
- **효과적인 프롬프팅 가이드**: https://stitch.withgoogle.com/docs/learn/prompting/
- **Stitch MCP 서버**: https://github.com/google-labs-code/stitch-skills
