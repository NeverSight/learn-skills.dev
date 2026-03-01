---
name: copilot-coding-agent
keyword: copilotview
description: GitHub Copilot Coding Agent 자동화. 이슈에 ai-copilot 라벨 부착 → GitHub Actions가 GraphQL로 Copilot에 자동 할당 → Copilot이 Draft PR 생성. 원클릭 이슈-to-PR 파이프라인.
allowed-tools: [Read, Write, Bash, Grep, Glob]
tags: [copilot, copilotview, github-actions, issue-to-pr, draft-pr, graphql, automation, ai-agent]
platforms: [Claude, Codex, Gemini]
version: 1.0.0
source: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent
---

# GitHub Copilot Coding Agent — Issue → Draft PR 자동화

> 이슈에 `ai-copilot` 라벨을 붙이면 GitHub Actions가 자동으로 Copilot에 할당하고,
> Copilot이 브랜치 생성 → 코드 작성 → Draft PR 생성까지 수행합니다.

## When to use this skill

- PM/디자이너가 이슈 작성 → 개발자 없이 Copilot이 자동 구현 시작할 때
- 백로그 이슈(리팩터링/문서화/테스트 추가)를 Copilot에게 offload할 때
- Vibe Kanban / Conductor로 생성된 후속 작업을 Copilot에게 위임할 때
- Jira 등 외부 시스템 → GitHub Issue → Copilot PR 자동화 파이프라인

---

## 전제 조건

- **GitHub 플랜**: Copilot Pro+, Business, 또는 Enterprise
- **Copilot Coding Agent 활성화**: 레포 설정에서 활성화 필요
- **gh CLI**: 인증 완료
- **PAT**: `repo` scope를 가진 Personal Access Token

---

## 최초 1회 셋업

```bash
# 원클릭 셋업 (토큰 등록 + 워크플로 배포 + 라벨 생성)
bash scripts/copilot-setup-workflow.sh
```

이 스크립트가 수행하는 작업:
1. `COPILOT_ASSIGN_TOKEN` 레포 시크릿 등록
2. `.github/workflows/assign-to-copilot.yml` 배포
3. `ai-copilot` 라벨 생성

---

## 사용 방법

### 방법 1: GitHub Actions 자동 (권장)

```bash
# 이슈 생성 + ai-copilot 라벨 → Copilot 자동 할당
gh issue create \
  --label ai-copilot \
  --title "Add user authentication" \
  --body "Implement JWT-based auth with refresh tokens. Include login, logout, refresh endpoints."
```

### 방법 2: 기존 이슈에 라벨 추가

```bash
# 이슈 번호 42에 라벨 추가 → Actions 트리거
gh issue edit 42 --add-label ai-copilot
```

### 방법 3: 스크립트로 직접 할당

```bash
export COPILOT_ASSIGN_TOKEN=<your-pat>
bash scripts/copilot-assign-issue.sh 42
```

---

## 동작 원리 (기술)

```
이슈 생성/라벨링
    ↓
GitHub Actions 트리거 (assign-to-copilot.yml)
    ↓
GraphQL로 Copilot bot ID 조회
    ↓
replaceActorsForAssignable → Copilot을 assignee로 설정
    ↓
Copilot Coding Agent 이슈 처리 시작
    ↓
브랜치 생성 → 코드 작성 → Draft PR 오픈
    ↓
당신을 PR 리뷰어로 자동 지정
```

필수 GraphQL 헤더:
```
GraphQL-Features: issues_copilot_assignment_api_support,coding_agent_model_selection
```

---

## GitHub Actions 워크플로우

| 워크플로 | 트리거 | 목적 |
|---------|--------|------|
| `assign-to-copilot.yml` | 이슈에 `ai-copilot` 라벨 | Copilot에 자동 할당 |
| `copilot-pr-ci.yml` | PR 오픈/업데이트 | CI (빌드 + 테스트) 실행 |

---

## Copilot PR 제약 사항

> Copilot은 **외부 기여자**처럼 취급됩니다.

- PR은 기본적으로 Draft 상태로 생성
- 첫 번째 Actions 실행 전 write 권한자의 **수동 승인** 필요
- 승인 후 `copilot-pr-ci.yml` CI가 정상 실행

```bash
# 수동 승인 후 CI 확인
gh pr list --search 'head:copilot/'
gh pr view <pr-number>
```

---

## planno(plannotator) 통합 — 선택사항

Copilot에 할당 전 이슈 스펙을 planno로 검토 (독립 스킬, 필수 아님):

```text
planno로 이 이슈 스펙을 검토하고 승인해줘
```

승인 후 `ai-copilot` 라벨 부착 → Actions 트리거.

---

## 대표 사용 케이스

### 1. 라벨 기반 Copilot 큐

```
PM이 이슈 작성 → ai-copilot 라벨 부착
→ Actions 자동 할당 → Copilot Draft PR 생성
→ 팀이 PR 리뷰만 수행
```

### 2. Vibe Kanban / Conductor와 결합

```
Vibe Kanban으로 생성된 후속 이슈:
  리팩터링/문서 정리/테스트 추가
  → ai-copilot 라벨 → Copilot 처리
→ 팀은 메인 기능 개발에 집중
```

### 3. 외부 시스템 연동

```
Jira 이슈 → Zapier/웹훅 → GitHub Issue 자동 생성
→ ai-copilot 라벨 → Copilot PR
→ 완전 자동화 파이프라인
```

### 4. 리팩터링 백로그 처리

```bash
# 백로그 이슈들에 라벨 일괄 추가
gh issue list --label "tech-debt" --json number \
  | jq '.[].number' \
  | xargs -I{} gh issue edit {} --add-label ai-copilot
```

---

## 결과 확인

```bash
# Copilot이 생성한 PR 목록
gh pr list --search 'head:copilot/'

# 특정 이슈 상태
gh issue view 42

# PR CI 상태
gh pr checks <pr-number>
```

---

## 참고 레퍼런스

- [GitHub Copilot Coding Agent 개요](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [Copilot에게 PR 생성 요청 (GraphQL 예제)](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-a-pr)
- [이슈 Copilot 할당 공식 문서](https://docs.github.com/copilot/using-github-copilot/coding-agent/asking-copilot-to-create-a-pull-request)
- [Copilot PR 권한/제약 사항](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [GitHub Copilot coding agent (VSCode 문서)](https://code.visualstudio.com/docs/copilot/copilot-coding-agent)

---

## Quick Reference

```
=== 셋업 ===
bash scripts/copilot-setup-workflow.sh   최초 1회 설정

=== 이슈 할당 ===
gh issue create --label ai-copilot ...  새 이슈 + 자동 할당
gh issue edit <num> --add-label ai-copilot  기존 이슈
bash scripts/copilot-assign-issue.sh <num>  직접 할당

=== 결과 확인 ===
gh pr list --search 'head:copilot/'    Copilot PR 목록
gh pr view <num>                        PR 상세
gh pr checks <num>                      CI 상태

=== 제약 ===
Copilot Pro+/Business/Enterprise 필요
첫 PR은 수동 승인 필요 (외부 기여자 취급)
PAT: repo scope 필요
```
