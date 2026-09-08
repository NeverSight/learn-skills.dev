---
name: a4-print-design
description: Create black and white A4 printable documents (흑백 A4 인쇄물) following professional design guidelines optimized for grayscale printing. Use when creating workshop handouts, educational materials, worksheets, checklists, meeting documents, or any A4 printable materials (워크샵 핸드아웃, 교육 자료, 워크시트, 체크리스트). Automatically applies consistent typography, layout patterns, and print-friendly styling.
---

# 흑백 A4 인쇄물 디자인 스킬

이 스킬은 흑백 프린터로 출력해도 가독성이 좋은 A4 문서를 만들기 위한 전문적인 디자인 가이드라인을 적용합니다.

## 사용 방법

1. **전체 가이드라인 참조**: 작업 시작 전에 `references/design-guidelines.md`를 읽어 전체 디자인 규칙을 파악하세요.

2. **HTML Artifact 생성**: A4 인쇄물은 항상 HTML artifact로 생성하며, 가이드라인의 CSS 스타일을 적용합니다.

3. **파일 생성 옵션**: 사용자가 docx나 PDF 파일을 원하는 경우, HTML을 먼저 생성한 후 변환합니다.

## 핵심 디자인 원칙

### 컬러 제한
- **블랙, 화이트, 그레이만** 사용
- 회색 배경(`#F5F5F5`)은 **문서당 1종류만** - 강조 효과를 위해 아껴서 사용
- 나머지 박스는 흰색 배경 + 테두리로 처리

### 타이포그래피
- **본문**: 10pt (최소 8pt 이상)
- **폰트**: Noto Sans KR, Pretendard, 본고딕
- **line-height**: 1.4~1.6

### 페이지 설정
- **크기**: 210mm x 297mm (A4)
- **여백**: 10~15mm (상하좌우)
- **배율**: 100% 인쇄 기준
- **Page break**: 페이지별로 정확히 나뉘도록 설정

### 레이아웃 패턴
- 2열 그리드 활용
- 섹션 번호는 검정 원 + 흰색 숫자
- 구분선으로 명확한 시각적 계층 구조

## 자주 사용하는 컴포넌트

### 박스 스타일
1. **기본 박스**: 흰색 배경 + 회색 테두리 (대부분 사용)
2. **강조 박스**: 회색 배경 (문서당 1종류만)
3. **팁 박스**: 왼쪽 굵은 검정 선

### 구분선
- **섹션 구분**: 2~3px 검정 실선
- **글쓰기 라인**: 1px 회색 점선

### 체크리스트
- `☐` 기호 사용
- 충분한 행간 확보

## 출력 형식

사용자가 별도 요청하지 않는 한:
- **기본**: HTML artifact (브라우저에서 Ctrl+P로 인쇄 가능)
- **요청 시**: docx, PDF 등으로 변환

## 참고사항

- 모든 스타일은 흑백 인쇄 최적화
- 잉크 절약을 위해 불필요한 배경색 최소화
- 인쇄 후 손으로 작성할 공간 고려
- 배율 100% 기준으로 테스트

---

**상세 가이드라인**: `references/design-guidelines.md` 참조
