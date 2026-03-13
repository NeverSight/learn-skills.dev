---
name: stitch-loop
description: "Stitch를 사용하여 자율적으로 멀티 페이지 웹사이트를 생성하는 반복 빌드 루프 패턴 — 바통 시스템으로 지속적 웹사이트 개발. Triggers on: Stitch 루프, 웹사이트 생성, 멀티 페이지, 빌드 루프. NOT for: 단일 페이지, React 앱."
user-invocable: true
allowed-tools:
  - "stitch*:*"
  - "mcp__stitch*"
  - "chrome*:*"
  - "Read"
  - "Write"
  - "Bash"
---

# Stitch Build Loop

당신은 반복적인 사이트 빌드 루프에 참여하는 **자율 프론트엔드 빌더**입니다. Stitch를 사용하여 페이지를 생성하고, 사이트에 통합하며, 다음 반복을 위한 지침을 준비하는 것이 목표입니다.

## 개요

Build Loop 패턴은 "바통" 시스템을 통해 지속적이고 자율적인 웹사이트 개발을 가능하게 합니다.

각 반복 과정:
1. 바통 파일(`next-prompt.md`)에서 현재 작업 읽기
2. Stitch MCP 도구를 사용하여 페이지 생성
3. 페이지를 사이트 구조에 통합
4. 다음 반복을 위해 바통 파일에 다음 작업 작성

## 사전 요구사항

**필수:**
- Stitch MCP 서버 접근 권한
- Stitch 프로젝트 (기존 또는 새로 생성)
- `DESIGN.md` 파일 (없으면 `stitch-design-md` 스킬로 생성)
- `SITE.md` 파일 (사이트 비전 및 로드맵 문서)

**선택:**
- Chrome DevTools MCP 서버 — 생성된 페이지의 시각적 검증 가능

## 바통 시스템

`next-prompt.md` 파일은 반복 간의 릴레이 바통 역할을 합니다:

```markdown
---
page: about
---

Jules.top 추적 방식을 설명하는 페이지입니다.

**디자인 시스템 (필수):**
[DESIGN.md 섹션 6에서 복사]

**페이지 구조:**
1. 네비게이션이 있는 헤더
2. 추적 방법론 설명
3. 링크가 있는 푸터
```

**중요 규칙:**
- YAML frontmatter의 `page` 필드가 출력 파일명 결정
- 프롬프트 내용에 `DESIGN.md`의 디자인 시스템 블록 포함 필수
- 작업 완료 전 이 파일을 업데이트하여 루프 지속

## 실행 프로토콜

### Step 1: 바통 읽기

`next-prompt.md`를 파싱하여 추출:
- `page` frontmatter 필드에서 **페이지 이름**
- markdown 본문에서 **프롬프트 내용**

### Step 2: 컨텍스트 파일 참조

생성 전에 다음 파일 읽기:

| 파일 | 목적 |
|------|------|
| `SITE.md` | 사이트 비전, **Stitch Project ID**, 기존 페이지(사이트맵), 로드맵 |
| `DESIGN.md` | Stitch 프롬프트에 필요한 시각적 스타일 |

**중요 확인사항:**
- 섹션 4 (사이트맵) — 이미 존재하는 페이지를 다시 만들지 마세요
- 섹션 5 (로드맵) — 백로그가 있으면 여기서 작업 선택
- 섹션 6 (크리에이티브 프리덤) — 로드맵이 비어있으면 새 페이지 아이디어

### Step 3: Stitch로 생성

Stitch MCP 도구를 사용하여 페이지 생성:

```bash
# 1. 네임스페이스 탐색
list_tools 실행하여 Stitch MCP 접두사 찾기

# 2. 프로젝트 가져오기 또는 생성
- stitch.json이 있으면 projectId 사용
- 없으면 [prefix]:create_project 호출 후 stitch.json에 ID 저장

# 3. 스크린 생성
[prefix]:generate_screen_from_text 호출:
- projectId: 프로젝트 ID
- prompt: 바통의 전체 프롬프트 (디자인 시스템 블록 포함)
- deviceType: DESKTOP (또는 지정된 대로)

# 4. 자산 검색
[prefix]:get_screen 호출하여:
- htmlCode.downloadUrl → queue/{page}.html로 다운로드 및 저장
- screenshot.downloadUrl → queue/{page}.png로 다운로드 및 저장
```

### Step 4: 사이트에 통합

1. 생성된 HTML을 `queue/{page}.html`에서 `site/public/{page}.html`로 이동
2. 자산 경로를 public 폴더 기준 상대 경로로 수정
3. 네비게이션 업데이트:
   - 기존 플레이스홀더 링크 (예: `href="#"`)를 새 페이지로 연결
   - 적절한 경우 전역 네비게이션에 새 페이지 추가
4. 모든 페이지에서 일관된 헤더/푸터 보장

### Step 4.5: 시각적 검증 (선택)

**Chrome DevTools MCP 서버**가 사용 가능한 경우:

```bash
# 1. 가용성 확인
list_tools로 chrome* 도구 존재 확인

# 2. 개발 서버 시작
Bash로 로컬 서버 시작 (예: npx serve site/public)

# 3. 페이지 이동
[chrome_prefix]:navigate로 http://localhost:3000/{page}.html 열기

# 4. 스크린샷 캡처
[chrome_prefix]:screenshot으로 렌더링된 페이지 캡처

# 5. 시각적 비교
Stitch 스크린샷(queue/{page}.png)과 비교하여 충실도 확인

# 6. 서버 중지
개발 서버 프로세스 종료
```

> **참고:** Chrome DevTools MCP가 설치되지 않은 경우 Step 5로 건너뛰세요.

### Step 5: 사이트 문서 업데이트

`SITE.md` 수정:
- 섹션 4 (사이트맵)에 새 페이지를 `[x]`로 추가
- 섹션 6 (크리에이티브 프리덤)에서 사용한 아이디어 제거
- 백로그 항목 완료 시 섹션 5 (로드맵) 업데이트

### Step 6: 다음 바통 준비 (중요!)

**완료 전에 반드시 `next-prompt.md`를 업데이트해야 합니다.** 이것이 루프를 유지합니다.

1. **다음 페이지 결정:**
   - `SITE.md` 섹션 5 (로드맵)에서 대기 항목 확인
   - 비어있으면 섹션 6 (크리에이티브 프리덤)에서 선택
   - 또는 사이트 비전에 맞는 새로운 것 창작

2. **바통 작성** (적절한 YAML frontmatter 포함):

```markdown
---
page: achievements
---

개발자 배지와 마일스톤을 보여주는 경쟁적 성취 페이지입니다.

**디자인 시스템 (필수):**
[DESIGN.md에서 전체 디자인 시스템 블록 복사]

**페이지 구조:**
1. 제목과 네비게이션이 있는 헤더
2. 잠금 해제/잠금 상태를 보여주는 배지 그리드
3. 마일스톤 추적을 위한 진행 바
```

## 파일 구조 참조

```
project/
├── next-prompt.md          # 바통 — 현재 작업
├── stitch.json             # Stitch 프로젝트 ID (유지 필수!)
├── DESIGN.md               # 시각적 디자인 시스템 (design-md 스킬에서)
├── SITE.md                 # 사이트 비전, 사이트맵, 로드맵
├── queue/                  # Stitch 출력 스테이징 영역
│   ├── {page}.html
│   └── {page}.png
└── site/public/            # 프로덕션 페이지
    ├── index.html
    └── {page}.html
```

## 오케스트레이션 옵션

루프는 다양한 오케스트레이션 레이어로 구동될 수 있습니다:

| 방법 | 작동 방식 |
|------|----------|
| **CI/CD** | `next-prompt.md` 변경 시 GitHub Actions 트리거 |
| **Human-in-loop** | 개발자가 각 반복을 검토 후 계속 |
| **Agent chains** | 한 에이전트가 다른 에이전트에 디스패치 |
| **Manual** | 개발자가 동일한 레포에서 에이전트를 반복 실행 |

이 스킬은 오케스트레이션에 독립적입니다 — 트리거 메커니즘이 아닌 패턴에 집중하세요.

## 디자인 시스템 통합

이 스킬은 `stitch-design-md` 스킬과 함께 사용하면 최상의 효과:

1. **최초 설정**: 기존 Stitch 스크린에서 `stitch-design-md` 스킬로 `DESIGN.md` 생성
2. **매 반복**: 섹션 6 ("Stitch 생성을 위한 디자인 시스템 노트")을 바통 프롬프트에 복사
3. **일관성**: 생성된 모든 페이지가 동일한 시각적 언어 공유

## 일반적인 함정

| 문제 | 설명 |
|------|------|
| ❌ `next-prompt.md` 업데이트 누락 | 루프가 중단됨 |
| ❌ 사이트맵에 이미 있는 페이지 재생성 | 중복 페이지 발생 |
| ❌ 프롬프트에 디자인 시스템 블록 미포함 | 일관성 없는 스타일 |
| ❌ 플레이스홀더 링크(`href="#"`) 방치 | 네비게이션 작동 안 함 |
| ❌ 새 프로젝트 생성 후 `stitch.json` 저장 누락 | 프로젝트 추적 불가 |

## 문제 해결

| 문제 | 해결책 |
|------|--------|
| Stitch 생성 실패 | 프롬프트에 디자인 시스템 블록 포함 확인 |
| 일관성 없는 스타일 | DESIGN.md가 최신인지 확인하고 올바르게 복사 |
| 루프 중단 | `next-prompt.md`가 유효한 frontmatter로 업데이트되었는지 확인 |
| 네비게이션 깨짐 | 모든 내부 링크가 올바른 상대 경로 사용 확인 |

## SITE.md 템플릿

```markdown
# [사이트 이름]

**Stitch Project ID:** [프로젝트 ID]

## 1. 비전

[사이트의 목적과 목표 사용자에 대한 설명]

## 2. 기술 스택

- Stitch 생성 HTML
- Tailwind CSS
- 정적 호스팅

## 3. 디자인 참조

DESIGN.md 참조

## 4. 사이트맵 (완료된 페이지)

- [x] index.html - 랜딩 페이지
- [x] about.html - 소개 페이지
- [ ] contact.html - 연락처 페이지

## 5. 로드맵 (다음 작업)

1. 연락처 페이지 생성
2. 블로그 목록 페이지
3. 개별 블로그 포스트 템플릿

## 6. 크리에이티브 프리덤 (아이디어)

- FAQ 페이지
- 팀 소개 페이지
- 포트폴리오 갤러리
```

## 워크플로우 예시

```bash
# 1. 초기 설정
stitch-design-md 스킬로 DESIGN.md 생성
SITE.md 작성

# 2. 첫 번째 바통 작성
echo '---
page: index
---
메인 랜딩 페이지...
**디자인 시스템:** ...' > next-prompt.md

# 3. 루프 실행
# 에이전트가 자동으로:
# - next-prompt.md 읽기
# - Stitch로 페이지 생성
# - site/public/에 통합
# - SITE.md 업데이트
# - next-prompt.md 업데이트 (다음 작업)

# 4. 반복
# 다음 에이전트 세션에서 동일한 레포로 계속
```

## 리소스

- **Stitch 공식 문서**: https://stitch.withgoogle.com/docs/
- **Stitch MCP 설정**: https://stitch.withgoogle.com/docs/mcp/setup
- **stitch-skills 레포**: https://github.com/google-labs-code/stitch-skills
