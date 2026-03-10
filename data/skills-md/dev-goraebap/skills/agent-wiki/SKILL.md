---
name: agent-wiki
description: >
  어떤 정보 공간이든 git 기반 위키 워크스페이스로 만들고 관리하는 인터페이스 스킬.
  문서 내용이나 형식에 상관없이 작업 영역을 git 워크스페이스로 초기화하고,
  AGENTS.md를 동적으로 생성하여 에이전트가 효율적으로 읽고 작업하도록 안내한다.
  소스코드 프로젝트에서는 기존 위키를 git submodule로 연결하여 에이전트 컨텍스트를 제공한다.
  트리거: "위키 만들어줘", "워크스페이스 만들어줘", "이 폴더를 위키로", "서브모듈 연결해줘",
  "위키 연결해줘", "위키 내용 파악해줘", "위키 업데이트", "위키 읽어줘",
  "agent-wiki", "에이전트 위키", "submodule 추가", "위키 초기화"
metadata:
  author: dev-goraebap
  version: "4.0"
---

# agent-wiki

어떤 정보 공간이든 **git 기반 워크스페이스 인터페이스**로 만들고 관리한다.
문서 유형(애자일, IA, 기술 문서 등)에 구애받지 않는다.
이 스킬의 핵심은 **AGENTS.md** — 에이전트가 워크스페이스를 읽고 작업할 때 따르는 동적 길잡이.

## 모드 감지

실행 전 아래 순서로 모드를 결정하고, 해당 workflow 파일을 Read하여 절차를 따른다.

| 조건 | 모드 | workflow 파일 |
|------|------|--------------|
| "help"/"사용법"/"뭐야"/"어떤 걸 할 수 있어" 등 스킬 자체 질문 | GUIDE | `workflow/guide-mode.md` |
| URL 인수 + "연결"/"서브모듈"/"connect" 키워드 | CONNECT | `workflow/connect-mode.md` |
| "read"/"읽어줘"/"내용 파악"/"분석해줘" 단독 요청 | READ | `workflow/read-mode.md` |
| "update"/"업데이트"/"수정"/"추가" 요청 또는 CWD에 `AGENTS.md` 있음 | UPDATE | `workflow/update-mode.md` |
| "create"/"새로 만들어줘"/"위키 만들어줘"/"초기화" 또는 그 외 | CREATE | `workflow/create-mode.md` |

## 워크스페이스 구조

agent-wiki는 내용 구조를 강제하지 않는다. 최소 공통 파일만 생성한다:

```
[project]-wiki/
├── AGENTS.md       ← 워크스페이스 길잡이 (동적 생성, 읽기 순서 + 구조 설명)
├── README.md       ← 워크스페이스 소개
├── .gitignore      ← 에이전트 캐시 등 제외
└── ...             ← 실제 문서 (유형 자유)
```

**AGENTS.md 원칙:**
- 짧게 — 내용을 담는 곳이 아니라 **길잡이**
- 읽기 순서 명시 — 에이전트가 어디서 시작할지 바로 알 수 있어야 함
- 구조 설명 — 각 파일/폴더의 역할을 한 줄씩
- 작업 안내 — 이 워크스페이스의 규칙·패턴 (있다면)

## 참고 파일

### Workflow

| 파일 | 역할 |
|------|------|
| `workflow/guide-mode.md` | 스킬 안내 (GUIDE) |
| `workflow/create-mode.md` | 워크스페이스 초기화 (CREATE) |
| `workflow/connect-mode.md` | 서브모듈 연결 (CONNECT) |
| `workflow/read-mode.md` | 위키 내용 파악 (READ) |
| `workflow/update-mode.md` | 문서 변경 (UPDATE) |

### Templates

| 파일 | 역할 |
|------|------|
| `templates/agents-md.md` | AGENTS.md 구조 가이드 |
| `templates/README.md` | README 구조 가이드 |
| `templates/.gitignore` | 기본 .gitignore |

### References

| 파일 | 역할 |
|------|------|
| `references/wiki-agents-guide.md` | 워크스페이스 이름 규칙 + 기반 파일 작성 규칙 |
