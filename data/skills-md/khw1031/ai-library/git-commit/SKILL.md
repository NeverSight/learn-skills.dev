---
name: git-commit
description: >
  Git 변경 사항을 분석하여 의미있는 커밋 메시지를 자동 생성합니다.
  커밋, 커밋 메시지 작성, 변경사항 커밋, git commit 요청 시 사용.
argument-hint: "[커밋 범위 - 전체/스테이징/파일명]"
---

# Git 커밋 메시지 생성기

변경 사항을 분석하여 의미있는 커밋 메시지를 자동으로 생성합니다.

## 워크플로우

### 1단계: 변경 사항 파악

```bash
# 스테이징된 변경 확인
git diff --cached --stat

# 스테이징된 상세 변경 내용
git diff --cached

# 전체 변경 확인 (스테이징 전)
git status --short
```

### 2단계: 변경 분석

| 분석 항목 | 확인 내용 |
|----------|----------|
| 파일 유형 | 소스 코드, 설정, 문서, 테스트 등 |
| 변경 유형 | 추가, 수정, 삭제, 리팩토링 |
| 영향 범위 | 단일 기능, 여러 모듈, 전체 시스템 |
| 핵심 키워드 | 함수명, 클래스명, 모듈명 |

### 3단계: 메시지 생성

**Conventional Commits 형식:**

```
<type>(<scope>): <subject>

<body>
```

**타입 선택 기준:**

| 타입 | 사용 시점 |
|------|----------|
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 변경 |
| `style` | 포맷팅, 세미콜론 등 (코드 변경 없음) |
| `refactor` | 리팩토링 (기능 변경 없음) |
| `test` | 테스트 추가/수정 |
| `chore` | 빌드, 설정 파일 변경 |

### 4단계: 커밋 실행

```bash
# 메시지와 함께 커밋
git commit -m "type(scope): subject" -m "body"

# 또는 에디터로 상세 메시지 작성
git commit
```

## 메시지 작성 규칙

### Subject (제목)

- 50자 이내
- 명령형 현재 시제 ("Add", "Fix", "Update")
- 마침표 없음
- 핵심 변경 내용 요약

### Body (본문)

- 72자마다 줄바꿈
- **무엇**을 변경했는지
- **왜** 변경했는지
- 주요 키워드/함수명 포함

## 예제

### 단일 기능 추가

```
feat(auth): add JWT token refresh endpoint

- Add /api/auth/refresh endpoint
- Implement token rotation logic
- Add 7-day refresh token expiry
```

### 버그 수정

```
fix(payment): resolve duplicate charge issue

- Add idempotency key validation
- Prevent concurrent payment requests
- Fix race condition in transaction handler
```

### 여러 파일 변경

```
refactor(api): reorganize route handlers

Affected modules:
- userController: extract validation logic
- authMiddleware: simplify token check
- errorHandler: add custom error types

Breaking changes: None
```

## 주의사항

- 스테이징되지 않은 파일은 커밋되지 않음
- 큰 변경은 논리적 단위로 분리 커밋 권장
- 민감한 정보(API 키 등) 포함 여부 확인
