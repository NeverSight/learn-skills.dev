---
name: release
description: Automates versioning and release notes generation for hwp2md. Use this skill when preparing a new release, creating version tags, or generating changelogs from git history.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
user-invocable: true
---

# Release Automation Skill

이 스킬은 hwp2md의 버저닝과 릴리즈를 자동화합니다.

## 사용법

```
/release [version] [options]
```

**예시:**
- `/release` - 다음 버전 자동 결정 및 릴리즈 준비
- `/release v0.2.0` - 특정 버전으로 릴리즈
- `/release patch` - 패치 버전 증가 (v0.1.0 → v0.1.1)
- `/release minor` - 마이너 버전 증가 (v0.1.0 → v0.2.0)
- `/release major` - 메이저 버전 증가 (v0.1.0 → v1.0.0)

## 릴리즈 프로세스

### 1. 버전 결정

현재 태그 확인:
```bash
git tag -l 'v*' --sort=-version:refname | head -5
```

버전 형식: `vMAJOR.MINOR.PATCH` (Semantic Versioning)

**버전 증가 기준:**
- **MAJOR**: 하위 호환성이 깨지는 변경
- **MINOR**: 새로운 기능 추가 (하위 호환)
- **PATCH**: 버그 수정, 문서 수정

### 2. 변경사항 분석

마지막 태그 이후 커밋 분석:
```bash
# 마지막 태그 찾기
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

# 커밋 로그 (태그 이후 또는 전체)
if [ -n "$LAST_TAG" ]; then
  git log $LAST_TAG..HEAD --oneline
else
  git log --oneline
fi
```

### 3. 릴리즈 태그 생성

```bash
# 태그 생성 (annotated tag)
git tag -a v0.2.0 -m "Release v0.2.0

주요 변경사항:
- 기능 1
- 기능 2
- 버그 수정
"

# 원격에 푸시
git push origin v0.2.0
```

### 4. GitHub Release

goreleaser를 사용한 릴리즈:
```bash
# 로컬 테스트 (실제 릴리즈 없이)
goreleaser release --snapshot --clean

# 실제 릴리즈 (CI에서 자동 실행)
goreleaser release --clean
```

## 릴리즈 체크리스트

릴리즈 전 확인사항:

- [ ] 모든 테스트 통과 (`make test`)
- [ ] 린트 검사 통과 (`make lint`)
- [ ] README.md 버전 정보 확인
- [ ] main 브랜치에 모든 변경사항 병합
- [ ] 이전 릴리즈 이후 breaking change 확인

## 예시: 전체 릴리즈 워크플로우

```bash
# 1. 현재 상태 확인
git status
make test

# 2. 마지막 태그 확인
git describe --tags --abbrev=0

# 3. 변경사항 확인
git log $(git describe --tags --abbrev=0)..HEAD --oneline

# 4. 태그 생성 및 푸시
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin main
git push origin v0.2.0

# 5. GitHub Actions가 자동으로 goreleaser 실행
```

## GitHub Actions 자동 릴리즈

태그를 푸시하면 GitHub Actions가 자동으로 릴리즈를 생성합니다.

### 워크플로우 (.github/workflows/release.yml)

1. `v*` 태그 푸시 시 트리거
2. goreleaser가 자동 실행
3. 크로스 플랫폼 바이너리 빌드 (Linux, macOS, Windows)
4. GitHub Release 페이지에 자동 게시
5. 릴리즈 노트 자동 생성 (커밋 메시지 기반)

### 릴리즈 노트 구조

goreleaser가 커밋 메시지를 분석하여 카테고리별로 정리:

- **New Features**: Add, Implement, Create, feat 접두사
- **Bug Fixes**: Fix, Resolve, Correct 접두사
- **Improvements**: Update, Change, Refactor, Improve 접두사
- **Documentation**: docs 접두사

### 릴리즈 실행 방법

```bash
# 1. 태그 생성
git tag -a v0.2.0 -m "Release v0.2.0"

# 2. main과 태그 푸시
git push origin main
git push origin v0.2.0

# 3. GitHub Actions가 자동으로:
#    - 바이너리 빌드
#    - 릴리즈 페이지 생성
#    - 릴리즈 노트 생성
```

### 릴리즈 페이지 내용

자동 생성되는 릴리즈 페이지:
- 설치 방법 (바이너리 다운로드, go install)
- 주요 기능 소개
- 변경 내역 (커밋 기반)
- 전체 변경 로그 링크
- 플랫폼별 바이너리 다운로드

## 긴급 패치 릴리즈

핫픽스가 필요한 경우:

```bash
# 1. 핫픽스 브랜치 생성
git checkout -b hotfix/v0.1.1 v0.1.0

# 2. 수정 적용
# ... 코드 수정 ...

# 3. 커밋 및 태그
git commit -m "Fix: Critical bug description"
git tag -a v0.1.1 -m "Hotfix release v0.1.1"

# 4. main에 병합 및 푸시
git checkout main
git merge hotfix/v0.1.1
git push origin main
git push origin v0.1.1
```
