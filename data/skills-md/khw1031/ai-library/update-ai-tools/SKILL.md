---
name: update-ai-tools
description: >
  AI 도구(Skill, Agent) 추가/변경 후 모든 README.md를 재귀적으로 업데이트하고 CHANGELOG에 반영합니다.
  update-ai-tools, README 업데이트, 도구 문서 갱신, 문서 동기화 요청 시 사용.
disable-model-invocation: true
---

# AI 도구 문서 업데이트

Skill, Agent 등 AI 도구를 추가/변경한 후, 모든 README.md를 재귀적으로 업데이트하고 CHANGELOG에 반영합니다.

## 활성화 조건

- `/update-ai-tools` 명령어 입력 시
- "도구 문서 갱신", "README 업데이트", "문서 동기화" 요청 시

---

## 실행 흐름

```
1. 변경 감지 → 2. 개별 도구 README → 3. 디렉토리 README → 4. 루트 README → 5. CHANGELOG
```

### 1단계: 변경 사항 감지

```bash
# 최근 변경된 AI 도구 파일 확인 (git 기준)
git diff --name-only HEAD
git diff --cached --name-only
git status --short

# skills/ 및 agents/ 하위 변경 파일 필터링
git diff --name-only HEAD -- skills/ agents/
```

**감지 대상:**
- 새로 추가된 도구 (`SKILL.md`, `AGENT.md` 신규)
- 수정된 도구 (`SKILL.md`, `AGENT.md` 변경)
- 삭제된 도구 (디렉토리 삭제)

변경이 없으면 사용자에게 알리고 종료합니다.

### 2단계: 개별 도구 README.md 업데이트

변경된 각 도구 디렉토리의 README.md를 업데이트합니다.

**대상:** `skills/{name}/README.md`, `agents/{name}/README.md`

각 README.md 작성 내용:
- 스킬/에이전트 이름, 설명 (SKILL.md/AGENT.md frontmatter 기반)
- 주요 기능 (본문에서 추출)
- 사용 방법 (호출 커맨드, 트리거 키워드)
- 디렉토리 구조 (실제 파일 목록)

**새 도구:** README.md 신규 생성
**수정된 도구:** 기존 README.md를 최신 SKILL.md/AGENT.md 기준으로 재작성
**삭제된 도구:** 해당 README.md도 함께 삭제됨 (디렉토리 삭제 시 자동)

> 변경된 도구가 3개 이상이면 에이전트 팀으로 병렬 처리를 권장합니다.

### 3단계: 디렉토리 README.md 업데이트

`skills/README.md`와 `agents/README.md`를 업데이트합니다.

**skills/README.md:**
1. 모든 `skills/*/SKILL.md`를 스캔
2. frontmatter에서 name, description 추출
3. 카테고리별로 그룹화 (기존 카테고리 구조 유지)
4. 요약 테이블 + 카테고리별 상세 섹션 재작성

**agents/README.md:**
1. 모든 `agents/*/AGENT.md`를 스캔
2. 요약 테이블 + 개별 상세 섹션 재작성

**카테고리 분류 기준:** [카테고리 가이드](references/categories.md) 참조. 없는 카테고리는 제안 후 생성 가능.

### 4단계: 루트 README.md 업데이트

`README.md`의 아래 섹션만 업데이트합니다 (나머지 섹션은 유지):

| 업데이트 대상 | 내용 |
|--------------|------|
| 리소스 목록 > Skills | 전체 스킬 테이블 (Name, Description) + 개수 |
| 리소스 목록 > Agents | 전체 에이전트 테이블 (Name, Description) + 개수 |
| 디렉토리 구조 | 실제 디렉토리 트리 반영 |

**유지할 섹션:** 설치 방법, 지원 에이전트, 설치 경로, 기여 방법

### 5단계: CHANGELOG 반영

`/changelog` 스킬을 호출하여 변경 내용을 CHANGELOG.md에 기록합니다.

changelog 스킬에 전달할 정보:
- 추가/수정/삭제된 도구 목록
- 변경 유형 (feat: 새 도구 추가, docs: 문서 업데이트 등)
- 담당자 (git author 기반)

---

## 병렬 처리 가이드

변경된 도구 수에 따라 실행 전략을 조절합니다:

| 변경 도구 수 | 전략 |
|-------------|------|
| 1~2개 | 순차 처리 |
| 3개 이상 | 에이전트 팀 구성 (배치별 병렬) |

병렬 처리 시 구성:
- 개별 도구 README 업데이트 에이전트 (배치별)
- 디렉토리 + 루트 README 업데이트 에이전트 (개별 완료 후)

---

## 주의사항

- 기존 README.md의 사용자 커스텀 내용이 있으면 보존 여부 확인
- 삭제된 도구는 디렉토리 README와 루트 README에서 자동 제거
- CHANGELOG 반영 시 버전 유형(patch/minor/major)은 사용자에게 확인
- 이 스킬은 `disable-model-invocation: true`로 사용자만 호출 가능
