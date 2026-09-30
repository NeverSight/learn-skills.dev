---
name: git-workflow
description: This skill should be used when the user asks to create or rename a branch, choose a branch name, write or validate a commit message, commit changes, prepare or open a pull request, or check branch, commit, or PR conventions. It applies Korean commit messages, conventional type-scope-subject commits, branch naming, and the [branch-name] - summary PR format.
---

# Git Workflow

브랜치, 커밋, PR 작성과 검증을 일관된 형식으로 처리한다.

## 작업 전 확인

- `git status`, 현재 브랜치, 변경 파일과 diff를 확인한다.
- 사용자가 요청하지 않은 코드 수정, 커밋, 푸시, PR 생성을 하지 않는다.
- 프로젝트의 `AGENTS.md`와 기존 PR 템플릿 규칙을 우선한다.

## 브랜치

- 기본 형식은 `type/short-description`이다.
- 예: `feat/login-page`, `fix/header-style`, `refactor/api-client`, `docs/pr-template`.
- 프로젝트나 실행 환경에 별도 prefix가 있으면 그것을 우선한다.
- 브랜치를 실제로 만들거나 이름을 바꾸는 작업은 사용자의 명시적 요청이 있을 때만 한다.

## 커밋 메시지

- 커밋 메시지는 한국어로 작성한다.
- 반드시 `type(scope): subject` 형식을 사용한다.
- `scope`는 변경된 기능 또는 폴더를 기준으로 짧게 작성한다.
- `subject`는 짧고 명확하게 작성한다.

예시:

```text
feat(button): 버튼 UI 추가
fix(tooltip): 툴팁 위치 오류 수정
refactor(api): API 클라이언트 구조 개선
docs(readme): PR 작성 규칙 추가
chore(page): 미사용 import 제거
```

## PR

- 제목은 `[브랜치명] - 변경 사항 요약` 형식을 사용한다.
- 본문에는 `요약`, `주요 변경 파일`, `변경 추가 이유`를 포함한다.
- 저장소에 `.github/pull_request_template.md`가 있으면 그 형식을 우선한다.

```md
## 요약

1. 변경 사항 요약

---

## 주요 변경 파일

| 파일 | 설명 |
|---|---|
| `파일 경로` | 변경 내용 |

---

## 변경 추가 이유

- 변경한 이유
```

## 결과

요청 종류에 따라 제안한 브랜치명, 커밋 메시지, PR 제목과 본문을 구분해 보여준다.
실제 변경을 수행했다면 변경 전후 상태와 실행한 검증도 함께 정리한다.
