---
name: lint-formatting
description: Run language-specific linters, formatters, and static type checks with full command reference. Use when user asks to lint, format, type-check, check style, or says "린트", "포맷", "타입 체크", "lint", "format", "type check", "biome", "ruff", "pyright", "clippy", "golangci-lint", "gopls", "rumdl", "prettier", "shfmt". Also use when needing detailed command variants (check-only, fix-only, partial scope) beyond the standard fix-everything command.
allowed-tools: Bash, Read, Glob
model: sonnet
effort: low
---

# Lint & Formatting

언어별 lint/format/정적 타입 체크 도구의 명령어 reference. 표준 "수정 + 포맷팅 통합" 명령어와 check-only, 부분 적용 등 변형을 함께 다룬다.

## JavaScript/TypeScript/JSON (Biome)

JSON/JSONC 도 Biome 을 기본으로 사용한다 (prettier 아님). 단 Biome 기본 `indentStyle` 은 tab 이라 2-space JSON 파일이 전부 탭으로 바뀐다 — 2-space 저장소면 repo 루트에 `biome.json` 을 두고 고정한다.

```json
{
  "formatter": {
    "indentStyle": "space",
    "indentWidth": 2
  }
}
```

`biome.json` 이 없는 저장소의 JS/TS 는 기본값(tab, 큰따옴표, 세미콜론, 폭 80) 그대로 포맷한다. 기존 코드나 예제 스타일에 맞추려고 `--indent-style`, `--quote-style`, `--semicolons`, `--line-width` 같은 포맷 플래그를 즉석에서 붙이지 않는다 — 플래그는 어디에도 남지 않아 에디터(conform → biome 기본값)와 결과가 어긋난다.

명령어:

- 린트만: `biome lint .`
- 포맷팅만 (수정): `biome format --write .`
- 포맷팅 검사만: `biome format .`
- 린트 + 포맷팅 통합 수정: `biome check --write .`
- 검사만 (수정 없이): `biome check .`

## Go (golangci-lint + gopls + gofmt)

golangci-lint는 다양한 린터를 통합 실행한다. gopls check 는 golangci-lint 와 go vet 이 잡지 않는 gopls 자체 analyzer 진단(scannererr, modernize 등)을 보여 주므로 Go 코드 수정 후 검증에 함께 포함한다 — 사용자가 에디터에서 gopls diagnostics 를 보고 있다.

- 린트 검사: `golangci-lint run`
- 특정 디렉터리 검사: `golangci-lint run ./...`
- 자동 수정: `golangci-lint run --fix`
- gopls 진단 (warning 이상): `gopls check $(fd -e go)`
- gopls 진단 (modernize 힌트 포함): `gopls check -severity=hint $(fd -e go)`
- 포맷팅: `gofmt -w .`

gopls check 는 진단이 있어도 exit code 가 항상 0 이다 — 출력이 비어 있으면 정상으로 판단한다. `fd .go` 는 regex 라 `.golden`, `logo.png` 도 잡히므로 `fd -e go` 를 쓴다.

modernize 힌트(`-severity=hint`)는 버그가 아닌 스타일 제안이다. 수정한 파일에 돌려 결과를 보고만 하고, 반영은 사용자와 합의 후 진행한다 — 새로 쓴 코드의 힌트도 임의로 고치지 않는다.

## Rust (clippy + rustfmt)

- 린트 검사: `cargo clippy`
- 린트 자동 수정: `cargo clippy --fix`
- 포맷팅: `cargo fmt`
- 포맷팅 검사만: `cargo fmt --check`

## Python (ruff)

- 린트 검사: `ruff check .`
- 린트 자동 수정: `ruff check --fix .`
- 포맷팅: `ruff format .`
- 포맷팅 검사만: `ruff format --check .`

## Python 정적 타입 체크 (pyright)

분류상 lint/format 이 아닌 정적 타입 체크지만, Python 코드 수정 후 검증에는 ruff 와 함께 항상 포함한다 — 사용자가 에디터에서 pyright diagnostics 를 보고 있어서, pyright 에러가 남은 커밋은 미완성 코드로 인식된다.

- 검사: `bunx pyright <수정한 파일...>` (pyright 글로벌 미설치 — bunx 로 실행)
- **수정한 파일만 검사한다.** repo 전체를 0 error 게이트로 걸지 않는다 — pyright 미도입 프로젝트는 기존 부채(특히 동적 스텁 패턴이 많은 테스트 파일)만으로 에러가 수십~수백 건일 수 있다.
- 기존 부채 에러는 범위 외 — 수정/추가한 코드에서 나온 에러만 0 으로 만든다. 기존 부채 일괄 정리나 pyrightconfig 도입은 사용자와 별도 합의 후 진행한다.
- 자주 걸리는 패턴과 해법:
  - closure 가 캡처한 변수는 바깥 `if` 의 narrowing 이 함수 안으로 전파되지 않는다 → 함수 본문에서 재검사
  - `.get()` 결과를 isinstance 로 거른 뒤 `["key"]` 로 재접근하면 narrowing 이 안 붙는다 → walrus(`:=`) 또는 로컬 변수로 바인딩
  - try/except import fallback stub 은 실함수와 파라미터 이름까지 일치시킨다 (이름 불일치도 시그니처 비호환)

## HTML (Prettier)

Biome가 HTML을 미지원하므로 Prettier를 사용한다.

- 포맷팅: `bunx prettier --write <파일>`
- 검사만: `bunx prettier --check <파일>`
- `tidy`는 HTML 포맷터로 사용하지 않는다. 사용자가 명시적으로 요청하거나
  프로젝트 스크립트가 `tidy`를 요구하는 경우에만 예외로 다룬다.

## Shell (shfmt)

- 포맷팅: `shfmt -i 4 -ci -w <file.sh>`
- 검사만: `shfmt -d <file.sh>`

## Markdown (rumdl)

**필수: rumdl 을 실행할 때는 항상 `--extend-disable MD013` 플래그를 붙인다.** 플래그 없는 `rumdl check .` / `rumdl fmt .` 형태는 이 환경에서 사용하지 않는다. MD013(line-length) 은 한국어 본문 가독성 때문에 의도적으로 끈 정책이며, `--extend-disable` 은 프로젝트 `.rumdl.toml` 의 disable 목록에 더해지는 형태라 기존 설정과 충돌하지 않는다.

- 검사만 (수정 없이): `rumdl check --extend-disable MD013 .`
- 자동 수정: `rumdl fmt --extend-disable MD013 .`
- 추가 규칙 끄기: `--extend-disable MD013,MD024` 처럼 콤마로 나열한다 (MD013 은 항상 포함).

## TOML (taplo)

`taplo` 는 PATH 에 없다. mason 경로로 실행한다 — `~/.local/share/nvim/mason/bin/taplo` (이하 `$TAPLO`).

- 린트 검사: `$TAPLO lint <파일...>`
- 포맷팅: `$TAPLO format <파일...>`
- 포맷팅 검사만: `$TAPLO format --check <파일...>`
- 변경 내용만 보기: `$TAPLO format --diff <파일...>`

파일 인자를 생략하면 cwd 이하를 재귀 탐색한다. `format` 은 인자 없이 실행하면 하위 모든 `.toml` 을 그 자리에서 수정하므로, 범위를 확인하려면 먼저 `--check` 나 `--diff` 로 돌린다.

## 실행 절차

1. 사용자 요청에서 대상 언어와 작업(검사 vs 수정)을 파악한다. 명시되지 않으면 `git status`로 변경된 파일의 확장자를 확인하여 추론한다.
2. 위 reference와 프로젝트 스크립트(`package.json`, `Makefile`, CI 설정 등)를 확인해 명령어를 선택한다. reference와 프로젝트 스크립트가 충돌하면 사용자에게 확인한다.
3. 명령어를 추측하거나 설치된 도구 이름만 보고 대체하지 않는다.
4. 결과를 사용자에게 보고한다. 에러가 있으면 파일 경로와 라인 번호를 함께 제시한다.

## 주의사항

- 표준 "수정 후 자동 수정" 워크플로우는 `commit` 스킬이 자체적으로 처리한다. 이 스킬은 명시적 lint/format 요청 또는 변형 명령어가 필요할 때 사용한다.
- HTML과 Shell의 `<파일>` 부분은 실제 파일 경로로 치환한다. 전체 디렉터리 일괄 적용 시에는 `fd`와 조합한다 (예: `fd -e sh -x shfmt -i 4 -ci -w {}`).
