---
name: update-hwpx-differences
description: Updates the HWPX-Markdown differences documentation when a new conversion issue is found or a new handling method is implemented. Use this skill when fixing HWPX parsing issues, adding new format handling, or discovering incompatibilities between HWPX and Markdown.
allowed-tools: Read, Edit, Write, Grep, Glob
user-invocable: true
---

# HWPX-Markdown 차이점 문서 업데이트

이 스킬은 HWPX와 Markdown 간의 차이점 문서(`docs/hwpx-markdown-differences.md`)를 자동으로 업데이트합니다.

## 사용 시점

다음과 같은 경우에 이 스킬을 사용하세요:

1. **새로운 변환 문제 발견**: HWPX 파싱 중 Markdown으로 표현할 수 없는 새로운 요소 발견
2. **새로운 처리 방법 구현**: 기존 차이점에 대한 새로운 변환 로직 추가
3. **기존 문서 개선**: 더 나은 설명이나 예시 추가 필요

## 실행 단계

### 1. 현재 문서 확인

```
docs/hwpx-markdown-differences.md
```

파일을 읽어 현재 문서화된 차이점 목록을 확인합니다.

### 2. 새로운 차이점 추가

다음 형식으로 새 항목을 추가합니다:

```markdown
### N. [차이점 이름]

| 항목 | 설명 |
|------|------|
| **HWPX** | [HWPX에서의 동작/기능] |
| **Markdown** | [Markdown의 제한사항] |
| **변환 방식** | [hwp2markdown의 처리 방법] |

**예시:**
- HWPX: [원본 예시]
- Markdown: [변환된 결과 예시]

**관련 코드:** `[파일 경로]` - `[함수명]` 함수

---
```

### 3. 번호 재정렬

새 항목 추가 후 전체 번호가 순차적인지 확인합니다.

### 4. 날짜 업데이트

문서 하단의 마지막 업데이트 날짜를 오늘 날짜로 변경합니다:

```markdown
*마지막 업데이트: YYYY-MM-DD*
```

## 차이점 카테고리

문서에 포함할 수 있는 차이점 유형:

| 카테고리 | 설명 |
|----------|------|
| 레이아웃 | 페이지, 여백, 단 나누기 등 |
| 테이블 | 병합, 중첩, 스타일 등 |
| 텍스트 | 글꼴, 색상, 특수 문자 등 |
| 객체 | 이미지, OLE, 수식 등 |
| 구조 | 각주, 목차, 참조 등 |

## 예시: 새 차이점 추가

**상황**: `<hp:tab/>` 요소가 Markdown에서 지원되지 않음을 발견

**추가할 내용**:

```markdown
### 11. 탭 문자 (Tab Character)

| 항목 | 설명 |
|------|------|
| **HWPX** | `<hp:tab/>` 요소로 탭 정렬 지원 |
| **Markdown** | 탭은 코드 블록 들여쓰기로만 사용 |
| **변환 방식** | 탭을 공백 4개로 변환 |

**예시:**
- HWPX: `이름<hp:tab/>홍길동`
- Markdown: `이름    홍길동`

**관련 코드:** `internal/parser/hwpx/parser.go` - `readElementText()` 함수

---
```

## 주의사항

- 기존 항목의 번호나 구조를 변경할 때는 다른 문서의 참조도 확인
- 코드 변경과 문서 업데이트는 같은 커밋에 포함
- 예시는 실제 테스트 파일(`testdata/한글 테스트.hwpx`)에서 가져오는 것이 좋음
