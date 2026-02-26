---
name: note-search
description: >
  notes/ 디렉토리의 학습 노트를 검색합니다.
  노트 검색, 개념 찾기, 관련 노트, 키워드 검색, 태그 검색 요청 시 사용.
argument-hint: "[검색어 또는 옵션]"
---

# 노트 검색

note-writer로 생성된 학습 노트를 효과적으로 검색합니다.

## 검색 전략

### 1단계: 빠른 매칭 (frontmatter)

```bash
# 키워드 검색 (가장 정확)
grep -rl "keywords:.*검색어" notes/ --include="SKILL.md"

# name/description 검색
grep -l "name: .*검색어" notes/ --include="SKILL.md"
grep -l "description:.*검색어" notes/ --include="SKILL.md"
```

### 2단계: 관련성 확장

```bash
# related 필드 검색
grep -rl "related:.*검색어" notes/ --include="SKILL.md"

# aliases 검색
grep -rl "aliases:.*검색어" notes/ --include="SKILL.md"

# Obsidian 링크 검색
grep -rl "\[\[.*검색어.*\]\]" notes/ --include="SKILL.md"
```

### 3단계: 본문 검색

```bash
# 요약/핵심 내용에서 검색
grep -rl "검색어" notes/ --include="SKILL.md"
```

## 검색 옵션

| 옵션 | 사용법 | 설명 |
|------|--------|------|
| 기본 | `/note-search 검색어` | 전체 필드 검색 |
| 카테고리 | `/note-search --category react 검색어` | 특정 카테고리만 |
| 태그 | `/note-search --tag type/concept` | 태그 기반 검색 |
| 관련 | `/note-search --related 노트명` | 연결된 노트 탐색 |

## 출력 형식

### 기본 출력 (요약)

```
## 검색 결과: "검색어"

### 1. 노트명 (notes/category/topic/)
- **키워드**: keyword1, keyword2
- **요약**: 핵심 내용 1-2문장

### 2. 다른노트 (notes/category/topic2/)
- **키워드**: keyword3
- **요약**: 핵심 내용 1-2문장

---
총 N개 노트 발견. 상세 내용은 해당 노트 참조.
```

### 상세 출력 요청 시

```
### 노트명 (notes/category/topic/)
- **키워드**: keyword1, keyword2

> [!summary]
> 요약 내용 전체

**핵심 내용 미리보기:**
- 포인트 1 요약
- 포인트 2 요약

[전체 내용 보기](notes/category/topic/SKILL.md)
```

## 검색 워크플로우

```
[검색어 입력]
    │
    ├─ 1. keywords 필드 검색 ──→ 정확한 매칭
    │
    ├─ 2. name/description 검색 ──→ 제목/설명 매칭
    │
    ├─ 3. related/aliases 검색 ──→ 관련 개념 매칭
    │
    ├─ 4. 본문 검색 ──→ 전체 텍스트 매칭
    │
    └─ 5. 결과 병합 및 중복 제거
            │
            └─ 관련성 순 정렬하여 출력
```

## 관련 노트 탐색

특정 노트의 연결 관계를 탐색:

```bash
# 해당 노트의 related 필드 읽기
grep -A5 "related:" notes/category/topic/SKILL.md

# 역방향 링크 찾기 (이 노트를 참조하는 다른 노트)
grep -rl "\[\[topic\]\]" notes/ --include="SKILL.md"
```

## 카테고리 목록 조회

```bash
# 모든 카테고리 확인
ls notes/

# 특정 카테고리의 노트 목록
ls notes/category/
```

## 실행 예시

```
/note-search useState

→ keywords에 "useState" 포함된 노트 우선
→ related에 "useState" 있는 노트 추가
→ 본문에 "useState" 언급된 노트 추가
→ 결과 출력
```

## 결과 없을 때

```
"검색어"에 대한 노트를 찾을 수 없습니다.

추천:
- 다른 키워드로 검색해 보세요
- /note-writer로 새 노트를 생성할 수 있습니다
- 카테고리 목록: ls notes/
```
