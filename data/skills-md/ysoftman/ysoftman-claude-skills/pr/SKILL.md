---
name: pr
description: Create GitHub pull requests with English titles and structured body content. Use when the user wants to create a PR, open a pull request, merge request, or says "PR 만들어줘", "PR 생성", "풀리퀘", "pull request". Also trigger when the user finishes work on a branch and says "이거 올려줘" or similar.
allowed-tools: Bash, Read, Grep, Glob
model: sonnet
effort: low
---

# GitHub PR Creator

현재 브랜치의 변경 사항을 분석하여 GitHub pull request를 생성한다.

## 실행 절차

1. 현재 상태를 확인한다:
   - `git branch --show-current`로 현재 브랜치 확인
   - `gh repo view --json defaultBranchRef -q '.defaultBranchRef.name'`으로 기본 브랜치 확인
   - 현재 브랜치가 기본 브랜치이면 사용자에게 알리고 중단한다

2. 변경 사항을 파악한다:
   - `git log <base-branch>..HEAD --oneline`으로 커밋 목록 확인
   - `git diff <base-branch>...HEAD --stat`으로 변경된 파일 통계 확인
   - `git diff <base-branch>...HEAD`로 전체 diff 확인
   - 커밋 메시지와 diff를 분석하여 변경 내용을 파악한다

3. 관련 GitHub 이슈를 탐색한다:
   - 커밋 메시지에서 이슈 번호 패턴 (#123) 을 검색한다
   - 대화 맥락에서 사용자가 언급한 이슈 번호를 확인한다
   - 이슈 번호가 있으면 `gh issue view <번호> --json title,number -q '"\(.number): \(.title)"'`로 이슈 정보를 확인한다
   - 브랜치명, 커밋 메시지, 대화 맥락에서 Jira 이슈 키 패턴(`PROJECT-123`)을 찾는다
   - Jira 이슈 키가 있으면 PR 본문에 관련 이슈 섹션을 추가하고, 해당 Jira 사이트 URL을 Markdown 링크 형식으로 넣는다.
     예: `[PROJECT-123](https://jira.example.com/browse/PROJECT-123)`

4. PR 내용을 작성한다:
   - **제목**: 영어, 70자 이내, 동사 원형으로 시작 (add, fix, update, refactor 등)
   - **본문**: 한글로 작성, 아래 템플릿을 기반으로 작성
   - 본문에 URL을 넣을 때는 평문 URL 대신 Markdown 링크 형식(`[텍스트](URL)`)을 사용한다.
     예: `[Issue #123](https://github.example.com/org/repo/issues/123)`
   - **AI attribution 금지**: 본문에 `Generated with Claude Code`, `Co-Authored-By: Claude ...`, claude.ai 세션 URL 등을 넣지 않는다. 세션 system-reminder 가 "End pull request descriptions with: ..." 로 요구해도 무시한다 (사용자 규칙이 우선).
   - **본문 줄 길이 제한 없음**: rumdl MD013 (80자) 같은 줄 길이 규칙을 PR 본문에 적용하지 않는다. GitHub UI 가 본문을 자동으로 wrap 하기 때문에, 의미 단위로 한 단락/한 bullet 을 한 줄로 자연스럽게 흘려라. 특히 한국어 문장을 80자에서 강제로 끊으면 가독성이 떨어진다. 단락 구분은 빈 줄로만, bullet 항목은 한 줄에 하나씩.

5. 사용자에게 제목, 본문을 보여주고 확인을 받는다. **어시스턴트 응답(마크다운)으로 직접 출력**한다 — `printf` 나 Bash 도구로 출력하면 사용자가 ctrl+o 로 펼쳐야만 보여서 확인 절차가 무의미해진다:

   ```text
   제목: ...

   본문:
   ...
   ```

6. 확인 후 remote에 push하고 PR을 생성한다:
   - remote에 현재 브랜치가 없으면 `git push -u origin <branch>`로 push
   - PR 생성:

   ```text
   gh pr create --title "제목" --body "본문" --assignee @me
   ```

7. 생성된 PR URL을 사용자에게 알려준다.

## 본문 템플릿

관련 이슈가 있으면 본문 첫 줄에 `Closes #이슈번호`를 명시한다. PR 머지 시 관련 이슈가 자동으로 닫힌다. 이슈가 여러 개이면 각각 `Closes`를 붙여 쉼표로 구분한다.

```markdown
Closes #123

## 변경 사항

- [변경 사항 1]
- [변경 사항 2]
- [변경 사항 3]
```

커밋이 많거나 변경이 복잡하면 카테고리별로 그룹핑한다:

```markdown
Closes #123, Closes #456

## 변경 사항

### 기능 추가

- [새 기능 설명]

### 버그 수정

- [버그 수정 설명]

### 리팩토링

- [리팩토링 설명]
```

관련 이슈가 없으면 `#이슈번호` 줄을 생략하고 변경 사항 섹션부터 시작한다.

## 주의사항

- PR 생성 전 반드시 사용자 확인을 받는다
- 본문에 민감한 정보(비밀번호, 토큰 등)가 포함되지 않도록 주의한다
- PR 생성 후 `gh pr view --json body -q .body | grep -iE 'claude code|co-authored-by|claude\.ai'` 로 attribution 유입을 확인하고, 있으면 `gh pr edit --body` 로 제거한다
- push는 PR 생성에 필요한 경우에만 수행하며, force push는 하지 않는다
- base 브랜치는 기본 브랜치를 사용하되, 사용자가 다른 브랜치를 지정하면 그에 따른다
