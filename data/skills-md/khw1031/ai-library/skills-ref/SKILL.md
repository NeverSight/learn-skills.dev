---
name: skills-ref
description: >
  스킬 디렉토리를 스캔하여 CLAUDE.md에 Available Skills 섹션을 XML 구조로 생성합니다.
  스킬 등록, 스킬 목록 생성, CLAUDE.md 스킬 섹션, skills ref,
  스킬 인덱스, available skills 작성 요청 시 활성화.
---

# Skills Ref

스킬 디렉토리를 스캔하여 CLAUDE.md에 `<available-skills>` XML 섹션을 생성합니다.

## CRITICAL: 사용자 입력 먼저

**이 스킬은 어떤 분석이나 명령 실행보다 먼저, 반드시 사용자에게 아래 두 가지를 질문해야 합니다. 사용자 응답 없이 절대 진행하지 마세요.**

```
1. 스캔할 스킬 디렉토리는 어디인가요? (예: .claude/skills, skills, 기타 경로)
2. CLAUDE.md 파일 경로는? (예: CLAUDE.md, .claude/CLAUDE.md, 기타)
```

- `skills/` 같은 기본값을 가정하지 마세요. 반드시 사용자에게 물어보세요.
- 레포마다 스킬 디렉토리가 다릅니다:
  - 일반 프로젝트 → `.claude/skills/`
  - 스킬 라이브러리 레포 → `skills/` (배포용), `.claude/skills/` (프로젝트 자체용)
  - 모노레포 → `packages/{pkg}/.claude/skills/`

**사용자가 디렉토리를 알려준 후에만 아래 워크플로우를 진행합니다.**

---

## 워크플로우

### Step 1: uvx 실행 환경 확인

`uvx`로 `skills-ref`를 실행할 수 있는지 확인합니다:

```bash
uvx --from skills-ref agentskills --help 2>/dev/null && echo "사용 가능" || echo "사용 불가"
```

#### uvx가 없는 경우

사용자에게 안내합니다:

```markdown
`uvx` 명령을 사용할 수 없습니다. `uv`를 설치하면 바로 사용할 수 있습니다:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

또는 내장 스크립트로 대체할 수 있습니다 (스킬 검증 기능은 제외).
```

### Step 2: 스킬 스캔

#### uvx 사용 가능한 경우 (권장)

```bash
# 모든 스킬의 프롬프트 XML 생성
uvx --from skills-ref agentskills to-prompt {skills_dir}/*/

# 개별 스킬 검증도 함께 수행
for skill in {skills_dir}/*/; do
  uvx --from skills-ref agentskills validate "$skill"
done
```

`to-prompt` 출력 결과를 CLAUDE.md용 형식으로 변환합니다 (Step 3 참조).

#### uvx 사용 불가한 경우 (대체)

내장 스크립트를 사용합니다:

```bash
bash skills/skills-ref/scripts/generate-skills-xml.sh {skills_dir}
```

### Step 3: XML 생성 및 CLAUDE.md 반영

스캔 결과를 아래 XML 형식으로 변환하여 CLAUDE.md에 작성합니다.

## XML 출력 형식

```xml
## Available Skills

<available-skills>

<skill name="{name}" ref="{skills_dir}/{name}">
  <description>{description 첫 문장 (무엇을 하는지)}</description>
  <trigger>{description 트리거 부분 (언제 활성화되는지)}</trigger>
</skill>

</available-skills>
```

### 필드 설명

| 필드 | 소스 | 설명 |
|------|------|------|
| `name` | frontmatter `name` | 스킬 식별자 |
| `ref` | 디렉토리 상대 경로 | 스킬 SKILL.md 위치 |
| `description` | frontmatter `description` 첫 문장 | 무엇을 하는지 |
| `trigger` | frontmatter `description` 나머지 | 언제 활성화되는지 |

### 실제 예시

```xml
## Available Skills

<available-skills>

<skill name="create-skill" ref=".claude/skills/create-skill">
  <description>Claude Code Skill을 생성합니다.</description>
  <trigger>스킬 생성, SKILL.md 작성, 새 스킬 만들기 요청 시 활성화.</trigger>
</skill>

<skill name="add-rules" ref=".claude/skills/add-rules">
  <description>프로젝트에 규칙을 Skill 기반으로 추가하고 기존 규칙을 Skill로 변환합니다.</description>
  <trigger>규칙 추가, 룰 추가, rule 추가, 새 규칙, 컨벤션 추가, 스타일 가이드 추가, 가이드라인 추가, 규칙 변환, rule 통합 요청 시 활성화.</trigger>
</skill>

<skill name="git-commit" ref=".claude/skills/git-commit">
  <description>Git 변경 사항을 분석하여 커밋 메시지를 생성합니다.</description>
  <trigger>커밋, 커밋 메시지 작성, git commit 요청 시 사용.</trigger>
</skill>

</available-skills>
```

## CLAUDE.md 반영 규칙

### 새 파일인 경우

CLAUDE.md가 없으면 새로 생성합니다:

```markdown
# Project Guide

## Available Skills

<available-skills>
{generated_xml}
</available-skills>
```

### 기존 파일인 경우

CLAUDE.md가 이미 있으면:

1. `<available-skills>` 섹션이 있으면 → **해당 섹션만 교체**
2. `<available-skills>` 섹션이 없으면 → **파일 끝에 추가**

**기존 내용을 절대 삭제하지 않습니다.** Available Skills 섹션만 갱신합니다.

### description 분리 기준

frontmatter description을 `<description>`과 `<trigger>`로 분리합니다:

```yaml
# 원본
description: >
  프로젝트에 규칙을 Skill 기반으로 추가하고 기존 규칙을 Skill로 변환합니다.
  규칙 추가, 룰 추가, rule 추가, 새 규칙, 컨벤션 추가 요청 시 활성화.

# 분리 결과
# description → 첫 문장: "프로젝트에 규칙을 Skill 기반으로 추가하고..."
# trigger → 나머지: "규칙 추가, 룰 추가, rule 추가..."
```

**분리 규칙:**
- 첫 번째 `.` 또는 줄바꿈까지가 description
- 나머지가 trigger
- trigger에 "시 활성화", "시 사용", "요청 시" 등의 패턴이 포함되어 있으면 정확한 분리

## 완료 보고

```markdown
## Available Skills 생성 완료

- **스캔 디렉토리**: `{skills_dir}`
- **발견된 스킬**: {count}개
- **CLAUDE.md 경로**: `{claude_md_path}`
- **동작**: 새로 생성 / 기존 섹션 교체 / 끝에 추가
```

## 상세 가이드

- [XML 형식 상세](references/format.md)
