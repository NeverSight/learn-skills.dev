---
name: note-writer
description: >
  Obsidian 호환 학습 노트를 Skill 형식으로 작성합니다.
  레퍼런스, 키워드, 개념 정리, 노트 작성, 지식 정리 요청 시 사용.
  텍스트, URL, 이미지, 영상 등 다양한 입력 지원.
argument-hint: "[컨텐츠 - 텍스트/URL/파일 등]"
---

# Obsidian 노트 작성기

노트를 **Skill 형식**으로 작성하여 AI가 관련 개념을 쉽게 탐색하고 로드할 수 있게 합니다.

## 핵심 원칙

> 생성되는 노트 = Skill 구조 + Progressive Disclosure

| 단계 | 내용 | AI 활용 |
|------|------|--------|
| 1단계 | frontmatter (name, description, keywords) | 관련성 판단 |
| 2단계 | SKILL.md 본문 (요약, 쉬운 설명) | 핵심 파악 |
| 3단계 | references/ (상세, 예시) | 필요시 로드 |

## 워크플로우

### 1. 입력 컨텐츠 분석

| 입력 유형 | 처리 방법 |
|----------|----------|
| 텍스트/키워드 | 주제 추출 및 개념 정리 |
| URL (문서) | WebFetch로 내용 분석 |
| URL (영상) | 제목/설명 기반 주제 파악 |
| 이미지 | 이미지 내용 분석 및 설명 |
| 파일 경로 | 파일 읽어서 내용 분석 |

### 2. 기존 노트 탐색

**PageIndex 우선 사용**, fallback으로 grep/glob:

```bash
# Fallback: 키워드로 기존 노트 검색
grep -rl "keywords:.*검색어" . --include="SKILL.md"
grep -rl "related:.*검색어" . --include="SKILL.md"
```

### 3. 카테고리 매칭

[카테고리 관리](references/categories.md) 참조.

| 조건 | 액션 |
|------|------|
| 유사 노트 존재 | 기존 노트에 링크 추가 (양방향) |
| 유사 카테고리 존재 | 해당 카테고리에 노트 생성 |
| 신규 주제 | 새 카테고리/노트 생성 |

### 4. 노트 생성

1. `notes/[category]/[topic]/SKILL.md` 생성
2. 필요시 `references/` 하위에 상세 문서 생성
3. `.claude/skills/[topic]` symlink 생성
4. 관련 기존 노트에 역링크 추가

## 생성 구조

```
notes/
└── [category]/
    └── [topic]/
        ├── SKILL.md          # 노트 본문 (Skill 형식)
        └── references/       # 상세 내용 (필요시)
            └── examples.md

.claude/skills/
└── [topic] -> ../../notes/[category]/[topic]/  # symlink
```

## 필수 요소

모든 노트에 반드시 포함:

1. **Skill frontmatter** - name, description, keywords, related
2. **요약** - 핵심 내용 2-3문장
3. **쉬운 설명** - 비전문가용 설명
4. **관련 개념 링크** - Obsidian 형식 `[[노트명]]`
5. **태그** - 계층적 태그

## 링크 전략

- **기존 노트 없음** → 빈 링크 `[[미작성 개념]]` 생성
- **기존 노트 있음** → 양방향 링크 업데이트
- 상세: [링크 전략](references/linking.md)

## 상세 가이드

- [노트 템플릿](references/templates.md)
- [카테고리 관리](references/categories.md)
- [링크 전략](references/linking.md)
