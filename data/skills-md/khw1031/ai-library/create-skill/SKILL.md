---
name: create-skill
description: >
  Claude Code Skill을 생성하거나 기존 스킬을 개선합니다.
  스킬 생성, 스킬 수정, SKILL.md 작성, 새 스킬 만들기, 스킬 개선, 스킬 업데이트 요청 시 활성화.
---

# Skill 생성

Claude Code Skill을 생성하는 가이드입니다.

## Progressive Disclosure 핵심

> **컨텍스트 윈도우는 공공재입니다.** Claude는 이미 충분히 똑똑합니다. Claude가 모르는 정보만 추가하세요.

스킬은 3단계로 정보를 로드합니다. 생성 시 각 단계의 역할을 명확히 분리하세요.

| 단계 | 내용 | 토큰 예산 | 위치 |
|------|------|----------|------|
| 1단계 Discovery | name + description | ~100 | frontmatter |
| 2단계 Activation | 핵심 지침, 사용 방법 | <5000 (<500줄) | SKILL.md 본문 |
| 3단계 Execution | 상세 문서, 스크립트, 리소스 | 무제한 | references/, scripts/, assets/ |

**원칙:** 1단계만으로 "이 스킬이 필요한가?" 판단 가능해야 하고, 2단계만으로 작업 수행이 가능해야 합니다. 3단계는 필요 시에만 로드합니다.

## 디렉토리 구조

```
skill-name/
├── SKILL.md          # Stage 2: 핵심 지침 (필수, <500줄)
├── references/       # Stage 3: 상세 문서 (*.md)
│   └── detail.md
├── scripts/          # Stage 3: 실행 가능한 코드
│   └── main.py
└── assets/           # Stage 3: 템플릿, 설정, 리소스
    └── template.json
```

| 디렉토리 | 역할 | 예시 |
|----------|------|------|
| `references/` | 상세 가이드, 예제, 스키마 문서 | `options.md`, `examples.md` |
| `scripts/` | 스킬이 실행하는 코드 (자체 완결적) | `lint.sh`, `analyze.py` |
| `assets/` | 정적 리소스, 템플릿 파일 | `template.json`, `config.yaml` |

## 필수 요소

| 필드 | 설명 | 제약 |
|------|------|------|
| `name` | 스킬 식별자 | 1-64자, 소문자/숫자/하이픈만, 디렉토리명과 일치 |
| `description` | 무엇 + 언제 | 1-1024자, 트리거 키워드 포함 |

## description 작성 패턴

```yaml
description: >
  [무엇을 하는지 1-2문장]
  [언제/어떤 키워드에 사용하는지]
```

**예시:**
```yaml
description: >
  PDF 파일에서 텍스트와 테이블을 추출합니다.
  PDF 작업, 문서 추출, 폼 처리 요청 시 사용.
```

## 생성 단계

### 1단계: 디렉토리 생성

```bash
mkdir -p skills/{name}/references
# 필요 시 추가
mkdir -p skills/{name}/scripts
mkdir -p skills/{name}/assets
```

### 2단계: Frontmatter 작성

```yaml
---
name: skill-name
description: >
  무엇을 하는지 설명.
  언제 사용하는지 트리거 키워드 포함.
---
```

상세 필드는 [Frontmatter 스키마](references/schema.md) 참조.

### 3단계: 본문 작성

본문은 Stage 2입니다. <500줄, <5000 토큰을 유지하며 핵심만 포함합니다.

**기본 구조:**

```markdown
# 스킬 제목

## 개요
핵심 기능 2-3문장

## 사용 방법
단계별 지침 (핵심만)

## 상세 정보
- [참조 문서](references/detail.md)
```

**판단 기준:** 본문에 넣을지, references/로 분리할지:
- 본문: 매번 참조해야 하는 핵심 규칙, 필수 워크플로우
- references: 예제 모음, 상세 옵션, 엣지 케이스, 배경 설명

상세 가이드는 [본문 작성 가이드](references/body-guide.md) 참조.

### 4단계: 검증

```
□ name이 1-64자, 소문자/숫자/하이픈만 사용하는가?
□ name이 디렉토리명과 일치하는가?
□ description이 무엇+언제를 명확히 설명하는가?
□ SKILL.md 본문이 500줄 이하인가?
□ 본문이 핵심만 포함하고 상세는 references/로 분리되었는가?
□ 파일 참조가 상대 경로이며 1단계 깊이인가?
```

상세 검증/보안 가이드는 [검증 및 보안](references/validation.md) 참조.

## 파일 참조 규칙

스킬 내부 파일을 참조할 때:

- **상대 경로** 사용 (절대 경로 금지)
- **1단계 깊이**만 참조 (`references/file.md` O, `references/sub/file.md` X)
- Markdown 링크 형식: `[표시 텍스트](references/file.md)`

```markdown
# 좋은 예
- [상세 가이드](references/guide.md)
- [스크립트](scripts/analyze.py)

# 나쁜 예
- [가이드](/absolute/path/guide.md)       # 절대 경로
- [가이드](references/sub/deep/guide.md)  # 깊은 중첩
```

## 선택 필드

| 필드 | 용도 | 예시 |
|------|------|------|
| `argument-hint` | 인자 힌트 | `[파일경로]` |
| `disable-model-invocation` | 사용자만 호출 | `true` (부작용 있는 작업) |
| `user-invocable` | Claude만 호출 | `false` (내부 지식) |
| `context` | 서브에이전트 실행 | `fork` |
| `agent` | 서브에이전트 유형 | `Explore`, `Plan`, `general-purpose` |
| `allowed-tools` | 도구 제한 | `Read, Grep` |

## 사용 패턴

| 패턴 | 설정 | 용도 |
|------|------|------|
| 일반 스킬 | 기본값 | 사용자/Claude 모두 호출 |
| 사용자 전용 | `disable-model-invocation: true` | 배포, DB 작업 등 부작용 |
| Claude 전용 | `user-invocable: false` | 내부 컨벤션, 배경 지식 |
| 격리 실행 | `context: fork` | 무거운 분석 작업 |

## 상세 가이드

- [Frontmatter 스키마](references/schema.md)
- [템플릿 모음](references/templates.md)
- [본문 작성 가이드](references/body-guide.md)
- [검증 및 보안](references/validation.md)
