---
name: accessibility-review
description: This skill should be used when the user asks to "접근성 리뷰해줘", "a11y 검토해줘", "accessibility review", "웹 접근성 확인해줘", "스크린리더 지원 확인해줘", or any request to review code for accessibility issues.
---

# Accessibility Review

웹 접근성 문제를 근거와 함께 찾아 우선순위가 있는 리뷰 결과로 정리한다.

## 원칙

- 리뷰 요청에서는 먼저 결과를 작성하고 코드를 수정하지 않는다.
- 관련 컴포넌트, 템플릿, 스타일, 테스트와 사용 흐름을 함께 확인한다.
- 실행 가능한 앱이면 실제 키보드·화면·스크린리더 관련 상태를 확인한다.
- 실행할 수 없으면 정적 분석만 했다고 명시한다.
- 네이티브 HTML 의미론을 우선하고, ARIA는 필요한 경우에만 사용한다.
- 근거 없이 WCAG 준수나 스크린리더 지원을 보장한다고 말하지 않는다.

## 확인 항목

- 의미 있는 HTML 요소, landmark, 제목 계층
- 이미지 대체 텍스트, 아이콘의 이름과 장식 처리
- 키보드 접근, 탭 순서, 포커스 표시, 포커스 손실과 포커스 트랩
- 폼 label, 오류 메시지, 필수 상태, 입력값 안내
- 버튼·링크의 accessible name, role, state, value
- 색상 대비, 색상만으로 전달되는 정보, 확대·반응형 상태
- 동적 콘텐츠, 모달, 알림, live region, 로딩·오류 상태
- 애니메이션, 깜빡임, `prefers-reduced-motion` 지원
- 표, 미디어 자막·대체 수단, 터치 조작과 충분한 대상 크기

## 결과 형식

```md
## Findings

- [P1] <문제 요약>
  - 위치: `path/to/file.tsx:10`
  - 영향: <어떤 사용자가 어떤 작업을 하기 어려운지>
  - 근거: <코드 또는 실행 결과>
  - 수정 방향: <최소 수정 방향>
  - 관련 기준: <알 수 있을 때만 WCAG 기준>

## 확인 범위

## 확인하지 못한 부분
```

심각도는 핵심 사용 흐름 차단 여부와 영향 범위를 기준으로 `P0`, `P1`, `P2`를 사용한다.
발견 사항이 없으면 확인한 범위와 남은 검증 한계를 함께 작성한다.
