---
name: fzf-patterns
description: Provides fzf command patterns and configurations. Use when writing fzf commands, interactive filters, or pipeline compositions.
---

# fzf Patterns

fzf 기반 인터랙티브 필터링 스크립트/프로그램 작성을 지원합니다.

**핵심 철학**:
- 파이프라인 조합: `source | fzf [options] | action`
- 프리뷰로 컨텍스트 제공: 선택 전 내용 확인
- 키 바인딩으로 워크플로우 확장: 다양한 액션 연결
- 점진적 복잡도: 단순 → 프리뷰 → 바인딩 → 동적 소스

## Instructions

### 워크플로우 1: 기본 명령어 생성

사용자 요청에서 파악:
1. **소스**: 무엇을 필터링? (파일, 프로세스, git 등)
2. **액션**: 선택 후 무엇을? (열기, 삭제, 체크아웃 등)
3. **컨텍스트**: 프리뷰 필요 여부

기본 패턴:
```bash
<source> | fzf --preview '<cmd> {}' | <action>
```

### 워크플로우 2: 리소스 매칭

요청에 따라 적절한 리소스 로딩:

| 키워드 | 리소스 |
|--------|--------|
| 검색 문법, 필터, 패턴 | `01-search-syntax.md` |
| 옵션, 설정, 플래그 | `02-options.md` |
| 키 바인딩, --bind, 액션 | `03-bindings.md` |
| 프리뷰, preview, bat | `04-preview.md` |
| 쉘 통합, CTRL-R/T, ALT-C | `05-shell-integration.md` |
| 레시피, 함수, git/docker | `06-recipes.md` |
| 고급, 멀티라인, 프로그래밍 | `07-advanced-patterns.md` |

### 워크플로우 3: 함수 작성

함수 요청 시 템플릿 기반 작성:

```bash
my_func() {
  local selected=$(
    SOURCE_CMD |
    fzf --height 40% \
        --layout reverse \
        --preview 'PREVIEW_CMD {}'
  )
  [[ -n "$selected" ]] && ACTION "$selected"
}
```

## Quick Reference

### 검색 문법

| 토큰 | 의미 |
|------|------|
| `word` | fuzzy 매칭 |
| `'word` | 정확히 포함 |
| `^word` | 시작 |
| `word$` | 끝 |
| `!word` | 제외 |
| `a \| b` | OR |

### 필수 옵션

```bash
--height 40%        # 일부 화면
--layout reverse    # 위→아래
--border            # 테두리
--multi             # 다중 선택
--preview 'cmd {}'  # 프리뷰
--bind 'key:action' # 바인딩
--ansi              # 색상 파싱
```

### 자주 쓰는 바인딩

```bash
--bind 'ctrl-/:toggle-preview'
--bind 'ctrl-a:select-all'
--bind 'enter:become(vim {})'
--bind 'change:reload:cmd {q}'
```

### 프리뷰 예시

```bash
# 파일
--preview 'bat --color=always {}'

# Git
--preview 'git log --oneline -20 {}'

# 디렉토리
--preview 'tree -C {} | head -100'
```

## Examples

### 파일 검색 + 열기

**요청**: "파일 찾아서 vim으로"

```bash
fd --type f | fzf --preview 'bat --color=always {}' | xargs vim
```

### Git 브랜치

**요청**: "브랜치 선택해서 체크아웃"

```bash
git branch | fzf --preview 'git log --oneline {-1}' \
    --bind 'enter:become(git checkout {-1})'
```

### ripgrep 통합

**요청**: "코드 검색하면서 프리뷰"

→ `resources/06-recipes.md`의 `rfv` 함수 참조

### 쉘 설정

**요청**: "CTRL-R 커스텀하고 싶어"

→ `resources/05-shell-integration.md`의 `FZF_CTRL_R_OPTS` 참조

## Technical Details

- `REFERENCE.md`: 전체 개요 및 트러블슈팅
- `resources/01-search-syntax.md`: 검색 토큰 상세
- `resources/02-options.md`: 모든 옵션 카테고리별 정리
- `resources/03-bindings.md`: --bind 액션 전체 목록
- `resources/04-preview.md`: 프리뷰 창 설정
- `resources/05-shell-integration.md`: 쉘 통합 (환경변수, 키바인딩)
- `resources/06-recipes.md`: 실용 함수 모음 (git, docker, file 등)
- `resources/07-advanced-patterns.md`: 멀티라인, 프로그래밍 통합
