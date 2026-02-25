---
name: docs-search
description: Search and retrieve Toss / Apps-in-Toss documentation using the ax CLI via run-ax.sh. Supports docs, TDS React Native, and TDS Web sources. Use bash to execute run-ax.sh in this skill's directory.
---

# Docs Search

Apps-in-Toss 문서를 검색하고 조회하는 스킬입니다.
이 스킬은 `ax` CLI 바이너리를 `run-ax.sh` 셸 스크립트를 통해 실행합니다.

## How to run

이 스킬 디렉토리 안의 `run-ax.sh`를 bash로 실행합니다.
스크립트가 ax 바이너리를 자동으로 다운로드·캐싱하므로 별도 설치는 필요 없습니다.

```bash
# macOS / Linux
bash skills/docs-search/run-ax.sh <command> [flags]

# Windows (PowerShell)
pwsh skills/docs-search/run-ax.ps1 <command> [flags]
```

## Commands

### 1. search — 문서 검색

세 가지 문서 소스를 검색할 수 있습니다:

| 서브커맨드 | 소스 |
|-----------|------|
| `search docs` | Apps-in-Toss Developer Center |
| `search tds-rn` | TDS React Native |
| `search tds-web` | TDS Web |

**플래그:**
- `--query "검색어"` (필수) — 검색 키워드
- `--limit N` (선택, 기본값 10) — 최대 결과 수

**예시:**

```bash
# 앱인토스 개발 문서에서 "미니앱 개발" 검색 (최대 5건)
bash skills/docs-search/run-ax.sh search docs --query "미니앱 개발" --limit 5

# TDS React Native에서 Button 컴포넌트 검색
bash skills/docs-search/run-ax.sh search tds-rn --query "Button component" --limit 3

# TDS Web에서 Toast 사용법 검색
bash skills/docs-search/run-ax.sh search tds-web --query "Toast usage" --limit 3
```

**출력 형식 (JSON 배열):**

```json
[
  {
    "id": "134c4bc8dc67f01e",
    "title": "미니앱 출시",
    "content": "문서 내용 스니펫...",
    "description": "",
    "url": "https://developers-apps-in-toss.toss.im/development/deploy.md",
    "category": "Table of Contents > 출시 > 출시하기",
    "score": 0.4259
  }
]
```

각 결과의 `id`를 사용하여 문서 전체를 조회할 수 있습니다.

### 2. get — 문서/예제 조회

검색 결과의 `id`로 문서 또는 예제의 전체 내용을 조회합니다.

| 서브커맨드 | 설명 |
|-----------|------|
| `get doc --id "ID"` | Apps-in-Toss 문서 조회 |
| `get tds-rn --id "ID"` | TDS React Native 문서 조회 |
| `get tds-web --id "ID"` | TDS Web 문서 조회 |
| `get example --id "ID"` | 예제 코드 조회 |

**예시:**

```bash
# 검색 결과에서 얻은 id로 문서 전체 조회
bash skills/docs-search/run-ax.sh get doc --id "134c4bc8dc67f01e"

# TDS React Native 문서 조회
bash skills/docs-search/run-ax.sh get tds-rn --id "<id>"

# 예제 코드 조회
bash skills/docs-search/run-ax.sh get example --id "7a4d6538fecee2f4"
```

**출력 형식 (JSON 객체):**

```json
{
  "id": "134c4bc8dc67f01e",
  "title": "미니앱 출시",
  "content": "문서 전체 내용 (마크다운)...",
  "url": "https://developers-apps-in-toss.toss.im/development/deploy.md",
  "category": "Table of Contents > 출시 > 출시하기"
}
```

### 3. list — 리소스 목록

```bash
# 예제 목록 조회
bash skills/docs-search/run-ax.sh list examples
```

## Workflow

사용자가 앱인토스 관련 질문을 하면 아래 순서로 진행합니다:

1. **검색**: `search docs/tds-rn/tds-web`로 관련 문서를 찾고 `id`를 획득
2. **조회**: `get doc/tds-rn/tds-web --id`로 문서 전체 내용을 확인
3. **답변**: 조회한 문서를 바탕으로 사용자에게 답변

예시 워크플로우:

```bash
# Step 1: 검색
bash skills/docs-search/run-ax.sh search docs --query "인앱 결제" --limit 3

# Step 2: 결과에서 id 확인 후 전체 문서 조회
bash skills/docs-search/run-ax.sh get doc --id "<검색결과의-id>"
```

## Version

`run-ax.sh`는 GitHub Releases API를 통해 최신 ax CLI 버전을 자동으로 감지합니다.
버전 정보는 24시간 동안 캐시되며, API 호출 실패 시 캐시된 버전 또는 fallback 버전을 사용합니다.
