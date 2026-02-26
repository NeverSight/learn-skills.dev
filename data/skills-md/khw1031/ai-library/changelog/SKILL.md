---
name: changelog
description: >
  CHANGELOG.md에 변경 사항과 담당자를 정리하고 package.json 버전을 올립니다.
  changelog 작성, 변경 이력 정리, 버전 올리기, 릴리즈 노트, CHANGELOG 업데이트 요청 시 사용.
argument-hint: "[버전 유형: patch/minor/major]"
---

# Changelog 작성기

CHANGELOG.md에 변경 사항과 변경 담당자(문의담당자)를 정리하고, package.json 버전을 함께 올립니다.

## 활성화 조건

- "changelog 작성해줘", "변경 이력 정리해줘" 요청 시
- "CHANGELOG 업데이트", "릴리즈 노트 작성" 언급 시
- "버전 올리면서 changelog" 관련 작업 요청 시

---

## 실행 단계

### 1단계: 현재 상태 파악

```bash
# 1. 현재 버전 확인
grep -m 1 '"version"' package.json

# 2. 최근 태그 이후 커밋 확인 (태그가 없으면 전체 커밋)
git tag --sort=-v:refname | head -1
git log $(git tag --sort=-v:refname | head -1)..HEAD --oneline --no-merges 2>/dev/null || \
  git log --oneline --no-merges -20

# 3. 기존 CHANGELOG.md 확인
head -30 CHANGELOG.md 2>/dev/null || echo "CHANGELOG.md 없음 - 새로 생성"
```

### 2단계: 버전 유형 선택

사용자에게 버전 유형을 확인합니다.

| 유형 | 변환 | 사용 시점 |
|------|------|----------|
| `patch` | `X.Y.Z` → `X.Y.(Z+1)` | 버그 수정, 작은 변경 |
| `minor` | `X.Y.Z` → `X.(Y+1).0` | 기능 추가 (하위 호환) |
| `major` | `X.Y.Z` → `(X+1).0.0` | 대규모 변경 (하위 호환 X) |

### 3단계: 변경 사항 분석

커밋 로그를 분석하여 카테고리별로 분류합니다.

**커밋 분류 기준:**

| 카테고리 | 커밋 타입 | 아이콘 |
|----------|----------|--------|
| 새 기능 | `feat` | ✨ |
| 버그 수정 | `fix` | 🐛 |
| 리팩토링 | `refactor` | ♻️ |
| 문서 | `docs` | 📝 |
| 스타일 | `style` | 💄 |
| 테스트 | `test` | ✅ |
| 빌드/설정 | `chore`, `build`, `ci` | 🔧 |

**담당자 추출:**

```bash
# 커밋별 작성자 확인
git log $(git tag --sort=-v:refname | head -1)..HEAD --format="%s|%an" --no-merges
```

### 4단계: CHANGELOG.md 작성

아래 형식으로 CHANGELOG.md 상단에 새 버전 섹션을 추가합니다.

**형식:** [CHANGELOG 형식 가이드](references/format-guide.md) 참조

```markdown
## [X.Y.Z] - YYYY-MM-DD

### ✨ 새 기능
- 기능 설명 — @담당자

### 🐛 버그 수정
- 수정 내용 — @담당자

### ♻️ 리팩토링
- 변경 내용 — @담당자
```

**작성 규칙:**
- 각 항목 끝에 `— @담당자이름` 형식으로 문의담당자 표기
- 변경 사항이 없는 카테고리는 생략
- 날짜는 `YYYY-MM-DD` (오늘 날짜)
- 기존 내용 아래로 밀리지 않도록 상단에 삽입

### 5단계: package.json 버전 업데이트

```bash
# package.json의 version 필드를 새 버전으로 수정
# Edit 도구를 사용하여 "version": "이전버전" → "version": "새버전" 변경
```

**모노레포인 경우:** 해당 패키지의 package.json만 수정합니다.

### 6단계: 결과 확인

변경된 파일을 사용자에게 보여줍니다:

```bash
# 변경된 파일 확인
git diff --stat

# CHANGELOG.md 상단 확인
head -30 CHANGELOG.md
```

---

## CHANGELOG.md 초기 구조

CHANGELOG.md가 없거나 비어있으면 아래 헤더로 시작합니다:

```markdown
# Changelog

이 프로젝트의 주요 변경 사항을 기록합니다.
형식은 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/)를 기반으로 합니다.

## [X.Y.Z] - YYYY-MM-DD
...
```

---

## 주의사항

- package.json 수정 전 반드시 사용자 확인
- 커밋 작성자와 실제 담당자가 다를 수 있으므로 사용자에게 확인
- 기존 CHANGELOG.md 내용을 덮어쓰지 않고 상단에 추가
- 담당자 이름은 Git 커밋 author를 기본으로 사용하되, 사용자가 수정 가능
