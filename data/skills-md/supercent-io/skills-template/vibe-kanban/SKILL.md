---
name: vibe-kanban
keyword: kanbanview
description: AI 코딩 에이전트를 시각적 Kanban 보드에서 관리. To Do→In Progress→Review→Done 흐름으로 병렬 에이전트 실행, git worktree 자동 격리, GitHub PR 자동 생성.
allowed-tools: [Read, Write, Bash, Grep, Glob]
tags: [vibe-kanban, kanban, kanbanview, multi-agent, git-worktree, github-pr, task-management, claude-code, codex, gemini, open-code, mcp]
platforms: [Claude, Codex, Gemini, OpenCode]
version: 1.2.0
verified: 2026-02-22
verified-with: playwright
source: https://github.com/BloopAI/vibe-kanban
---

## 플랫폼별 적용 상태 (현재 지원 기준)

| 플랫폼 | 현재 지원 방식 | 적용 조건 |
|---|---|---|
| Claude | 네이티브 MCP 연동 | `mcpServers` 등록 |
| Codex | MCP 스크립트 연동 | `scripts/mcp-setup.sh --codex` 또는 동일 설정 |
| Gemini | MCP 등록 | `mcpServers`/브릿지 구성 |
| OpenCode | MCP/브릿지 연동 | `omx`/`ohmg`류 또는 동등 구성 |

`현재 스킬만`으로 가능한지:
- Claude/Gemini: **가능**
- Codex: **가능(스크립트 기반 설정 필요)**
- OpenCode: **가능(오케스트레이션 경유)**

# Vibe Kanban — AI 에이전트 칸반 보드

> 여러 AI 에이전트(Claude/Codex/Gemini)를 하나의 Kanban 보드에서 통합 관리합니다.
> 카드(태스크)를 In Progress로 옮기면 git worktree 생성 + 에이전트 실행이 자동 시작됩니다.

## When to use this skill

- 에픽을 여러 독립 태스크로 분해해 에이전트에게 병렬 할당할 때
- 진행 중인 AI 작업 상태를 시각적으로 추적하고 싶을 때
- 에이전트 결과를 UI에서 diff/로그로 리뷰하고 재시도하고 싶을 때
- GitHub PR 기반 팀 협업과 AI 에이전트 작업을 결합할 때

---

## 전제 조건

```bash
# Node.js 18+ 필요
node --version

# 에이전트 인증 미리 완료
claude --version    # ANTHROPIC_API_KEY 설정
codex --version     # OPENAI_API_KEY 설정 (선택)
gemini --version    # GOOGLE_API_KEY 설정 (선택)
opencode --version  # 별도 설정 없음 (GUI 기반)
```

> **검증된 버전 (2026-02-22 기준)**
> - vibe-kanban: v0.1.17
> - claude (Claude Code): 2.1.50
> - codex: 0.104.0
> - gemini: 0.29.5
> - opencode: 1.2.10

---

## 설치 & 실행

### npx (가장 빠름)

```bash
# 즉시 실행 (설치 불필요)
npx vibe-kanban

# 포트 지정 (기본 포트 3000)
npx vibe-kanban --port 3001

# 포트와 환경 변수 동시 지정
PORT=3001 npx vibe-kanban --port 3001

# 래퍼 스크립트 사용
bash scripts/vibe-kanban-start.sh
```

브라우저에서 `http://localhost:3000` 자동 오픈.

> ⚠️ **포트 충돌 주의**: Next.js 등 다른 개발 서버가 3000 포트를 사용 중이라면
> `PORT=3001 npx vibe-kanban --port 3001`로 실행하세요.
> 시작 로그에서 `Main server on :3001` 확인 후 `http://localhost:3001` 접속.

시작 시 정상 로그:
```
Starting vibe-kanban v0.1.17...
No user profiles.json found, using defaults only
Starting PR monitoring service with interval 60s
Remote client initialized with URL: https://api.vibekanban.com
Main server on :3001, Preview proxy on :XXXXX
Opening browser...
```

### 직접 클론 + 개발 모드

```bash
git clone https://github.com/BloopAI/vibe-kanban.git
cd vibe-kanban
pnpm i
pnpm run dev
```

---

## 환경 변수

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `PORT` | 서버 포트 | `3000` |
| `HOST` | 서버 호스트 | `127.0.0.1` |
| `VIBE_KANBAN_REMOTE` | 원격 연결 허용 | `false` |
| `VK_ALLOWED_ORIGINS` | CORS 허용 출처 | 미설정 |
| `DISABLE_WORKTREE_CLEANUP` | worktree 정리 비활성화 | 미설정 |
| `ANTHROPIC_API_KEY` | Claude Code 에이전트용 | — |
| `OPENAI_API_KEY` | Codex/GPT 에이전트용 | — |
| `GOOGLE_API_KEY` | Gemini 에이전트용 | — |

`.env` 파일에 설정 후 서버 시작.

> **에이전트별 API 키 설정 위치 (Settings → Agents → Environment variables)**
> - Claude Code: `ANTHROPIC_API_KEY`
> - Codex: `OPENAI_API_KEY`
> - Gemini: `GOOGLE_API_KEY`
> - Opencode: 별도 설정 없음 (내장 인증)

---

## MCP 설정

Vibe Kanban은 MCP(Model Context Protocol) 서버로 동작하여 에이전트가 직접 보드를 제어할 수 있습니다.

### Claude Code MCP 설정

`~/.claude/settings.json` 또는 프로젝트의 `.mcp.json`:

```json
{
  "mcpServers": {
    "vibe-kanban": {
      "command": "npx",
      "args": ["vibe-kanban", "--mcp"],
      "env": {
        "MCP_HOST": "127.0.0.1",
        "MCP_PORT": "3001"
      }
    }
  }
}
```

### OpenCode MCP 설정

`~/.config/opencode/opencode.json`에 추가:

```json
{
  "mcp": {
    "vibe-kanban": {
      "command": "npx",
      "args": ["vibe-kanban", "--mcp"],
      "env": {
        "MCP_HOST": "127.0.0.1",
        "MCP_PORT": "3001"
      }
    }
  }
}
```

재시작 후 `vk_*` 도구가 OpenCode 세션에서 바로 사용 가능합니다.


### MCP 도구 목록

| 도구 | 설명 |
|------|------|
| `vk_list_cards` | 모든 카드(워크스페이스) 조회 |
| `vk_create_card` | 새 카드 생성 |
| `vk_move_card` | 카드 상태 변경 |
| `vk_get_diff` | 카드 diff 조회 |
| `vk_retry_card` | 카드 재실행 |

> ⚠️ **이전 버전 도구명과 변경**: `vk_list_tasks` → `vk_list_cards`, `vk_create_task` → `vk_create_card`
> v0.1.17 기준 실제 MCP API에서 확인된 도구명입니다.

### Codex MCP 적용

Codex에서 Vibe Kanban을 연동하려면 프로젝트 루트에서 다음을 실행합니다.

```bash
bash scripts/mcp-setup.sh --codex
```

이 명령은 `~/.codex/config.toml`에 `vibe-kanban` MCP 서버 설정을 추가합니다.  
훅 기반 자동 반복은 Codex 기본 동작이 아니므로, 재시도/반복 운영은 보드 카드 진행 상태 또는 상위 오케스트레이션으로 관리합니다.

---

## 워크스페이스 → 병렬 에이전트 → PR 워크플로우

> **v0.1.17 실제 UI 구조**: Vibe Kanban은 Kanban 보드 형태이지만,
> 실제 작업 단위는 **Workspace** (워크스페이스)입니다.
> 각 워크스페이스가 하나의 태스크를 독립적으로 처리합니다.

### 1. 서버 시작

```bash
# 기본 실행
npx vibe-kanban
# → http://localhost:3000

# 포트 충돌 시 (Next.js 등)
PORT=3001 npx vibe-kanban --port 3001
# → http://localhost:3001
```

### 2. (선택) planno로 에픽 계획 검토

```text
planno로 이 기능의 구현 계획을 검토해줘
```

planno(plannotator)는 독립 스킬 — Vibe Kanban 없이도 사용 가능.

### 3. 워크스페이스 생성 (Create Workspace)

1. UI 접속 → **"+ Create Workspace"** 또는 왼쪽 사이드바 `+` 버튼 클릭
2. **Which repositories?** 화면:
   - **Browse** → 파일 시스템에서 git 레포 선택 (경로 수동 입력 가능)
   - **Recent** → 이전에 사용한 레포
   - 레포 선택 후 브랜치 선택 (기본: `main`)
   - **Continue** 클릭
3. **What would you like to work on?** 화면:
   - 에이전트 선택 (Opencode, Claude Code, Codex, Gemini, Amp, Qwen Code, Copilot, Droid, Cursor Agent)
   - 태스크 설명 입력 (Markdown 지원)
   - 모드 선택 (Default, Build 등)
   - **Create** 클릭

### 4. 에이전트 자동 실행

워크스페이스 생성 시:
- `vk/<hash>-<slug>` 브랜치 자동 생성 (예: `vk/3816-add-a-comment-to`)
- git worktree 자동 생성 (에이전트별 완전 격리)
- 선택한 에이전트 CLI 실행 + 로그 스트리밍

워크스페이스 상태:
- **Running**: 에이전트 실행 중 (왼쪽 사이드바)
- **Idle**: 대기 중
- **Needs Attention**: 에이전트 완료 또는 입력 필요

### 5. 결과 확인

- **Changes 패널**: 파일 diff 확인
- **Logs 패널**: 에이전트 실행 로그
- **Preview 패널**: 웹앱 미리보기
- **Terminal**: 직접 명령 실행
- **Notes**: 메모 작성

### 6. PR 생성 & 완료

- 워크스페이스 상세 → **"Open pull request"** 버튼
- PR merge → 워크스페이스 Archive로 이동
- worktree 자동 정리

---

## Git Worktree 격리 구조

워크스페이스 디렉토리 (Settings → General → Workspace Directory에서 변경 가능):
```
~/.vibe-kanban-workspaces/          ← 기본 위치 (홈 디렉토리 하위)
├── <workspace-uuid-1>/             ← 워크스페이스1 격리 환경
├── <workspace-uuid-2>/             ← 워크스페이스2 격리 환경
└── <workspace-uuid-3>/             ← 워크스페이스3 격리 환경
```

브랜치 네이밍 (Settings → General → Git → Branch Prefix에서 변경):
```
vk/<4자 ID>-<task-slug>
예: vk/3816-add-a-comment-to-readme
```

내부 동작:
```bash
git worktree add <workspace-dir> -b vk/<hash>-<task-slug> main
<agent-cli> -p "<task-description>" --cwd <workspace-dir>
```

> **.gitignore 권장 항목 추가:**
> ```
> .vibe-kanban-workspaces/
> .vibe-kanban/
> ```

---

## 원격 배포

### Docker

```bash
# 공식 이미지
docker run -p 3000:3000 vibekanban/vibe-kanban

# 환경 변수 전달
docker run -p 3000:3000 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e VK_ALLOWED_ORIGINS=https://vk.example.com \
  vibekanban/vibe-kanban
```

### 리버스 프록시 (Nginx/Caddy)

```bash
# CORS 허용 필수
VK_ALLOWED_ORIGINS=https://vk.example.com

# 또는 다중 출처
VK_ALLOWED_ORIGINS=https://a.example.com,https://b.example.com
```

### SSH 원격 열기

VSCode Remote-SSH와 통합:
```
vscode://vscode-remote/ssh-remote+user@host/path/to/.vk/trees/<task-slug>
```

---

## 트러블슈팅

### Worktree 충돌 / 고아 worktree

```bash
# 고아 worktree 정리
git worktree prune

# 현재 worktree 목록 확인
git worktree list

# 특정 worktree 강제 삭제
git worktree remove .vk/trees/<slug> --force
```

### 403 Forbidden (CORS 오류)

```bash
# 원격 접속 시 CORS 설정 필요
VK_ALLOWED_ORIGINS=https://your-domain.com npx vibe-kanban
```

### 에이전트가 시작되지 않음

```bash
# CLI 직접 테스트
claude --version
codex --version

# API 키 확인
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
```

### 포트 충돌

```bash
# 다른 포트 사용
npx vibe-kanban --port 3001

# 또는 환경 변수
PORT=3001 npx vibe-kanban
```

### SQLite 락 오류

```bash
# worktree 정리 비활성화 후 재시작
DISABLE_WORKTREE_CLEANUP=1 npx vibe-kanban
```

---

## UI vs CLI 선택 기준

| 상황 | 모드 |
|------|------|
| 팀 공유 보드, 시각적 진행 추적 | UI (`npx vibe-kanban`) |
| CI/CD 파이프라인, 스크립트 자동화 | CLI (`scripts/pipeline.sh`) |
| 빠른 로컬 실험 | CLI (`scripts/conductor.sh`) |
| 브라우저 diff/로그 리뷰 | UI |

---

## 지원 에이전트 목록 (v0.1.17 검증)

Settings → Agents에서 각 에이전트별 상세 설정 가능:

| 에이전트 | 명령 | API 키 |
|----------|------|--------|
| **Opencode** | `opencode` | 내장 (기본값) |
| **Claude Code** | `claude` | `ANTHROPIC_API_KEY` |
| **Codex** | `codex` | `OPENAI_API_KEY` |
| **Gemini** | `gemini` | `GOOGLE_API_KEY` |
| **Amp** | `amp` | 별도 |
| **Qwen Code** | `qwen-coder` | 별도 |
| **Copilot** | `copilot` | GitHub 계정 |
| **Droid** | `droid` | 별도 |
| **Cursor Agent** | `cursor` | Cursor 구독 |

에이전트별 설정 가능 항목:
- **Append prompt**: 에이전트 실행 시 추가 지시문
- **Model**: 사용할 모델명 (예: `claude-opus-4-6`)
- **Variant**: 모델 변형
- **Auto Approve**: 에이전트 액션 자동 승인 (기본: ON)
- **Auto Compact**: 컨텍스트 자동 압축 (기본: ON)
- **Environment variables**: API 키 등 환경변수

## 대표 사용 케이스

### 1. 에픽 병렬 분해 처리

```
"결제 플로우 v2" 에픽
  ├── 워크스페이스1: 프론트엔드 UI  → Claude Code
  ├── 워크스페이스2: 백엔드 API     → Codex
  └── 워크스페이스3: 통합 테스트    → Opencode
→ 3개 워크스페이스 동시 Running → 병렬 구현
```

### 2. 역할별 전문 에이전트 배치

```
Claude Code  → 설계/도메인 heavy 기능
Codex        → 타입/테스트/리팩터링
Gemini       → 문서/스토리북 작성
Opencode     → 범용 작업 (기본값)
```

### 3. GitHub PR 기반 팀 협업

```
VIBE_KANBAN_REMOTE=true 설정
→ 팀원이 보드에서 상태 확인
→ GitHub PR에서만 리뷰/승인
→ 에이전트 병렬 + 전통 PR 프로세스 결합
```

### 4. 구현 비교

```
동일 태스크, 두 개 워크스페이스:
  워크스페이스A → Claude Code (UI 구조 중심)
  워크스페이스B → Codex (성능 최적화 중심)
→ PR 비교 후 best-of-both 선택
```

### 5. OpenCode + ulw 병렬 위임

OpenCode의 ulw(ultrawork) 모드와 결합해 에이전트를 에픽 단위로 병렬 실행:

```python
# ulw 키워드 → ultrawork 병렬 실행 레이어 활성화
# Vibe Kanban 보드: npx vibe-kanban (별도 터미널에서 실행)

task(category="visual-engineering", run_in_background=True,
     load_skills=["frontend-ui-ux", "vibe-kanban"],
     description="[Kanban WS1] 프론트엔드 UI",
     prompt="결제 플로우 UI 구현 — src/components/payment/ 내 카드 입력, 주문 확인, 완료 화면")

task(category="unspecified-high", run_in_background=True,
     load_skills=["vibe-kanban"],
     description="[Kanban WS2] 백엔드 API",
     prompt="결제 플로우 API 구현 — POST /charge, POST /refund, GET /status/:id")

task(category="unspecified-low", run_in_background=True,
     load_skills=["vibe-kanban"],
     description="[Kanban WS3] 통합 테스트",
     prompt="결제 E2E 테스트 작성 — 성공/실패/환불 시나리오")

# → 3개 워크스페이스가 Running 상태로 Kanban 보드에 동시 표시
# → 각 완료 시: Needs Attention → PR 생성 → Archive
```

---

## 팁

- 카드 범위를 좁게 유지 (1카드 = 1커밋 단위)
- 2개 파일 이상 변경 시 planno로 먼저 계획 검토
- `VIBE_KANBAN_REMOTE=true`는 신뢰 네트워크에서만 사용
- 에이전트 스탈 시 → 재할당 또는 카드 분할

---

## 아키텍처 개요

```
┌─────────────────────────────────────────────────────────┐
│                    Vibe Kanban UI                       │
│   ┌──────────┬──────────┬──────────┬──────────┐        │
│   │  To Do   │In Progress│  Review  │   Done   │        │
│   └──────────┴──────────┴──────────┴──────────┘        │
└───────────────────────────┬─────────────────────────────┘
                            │ REST API
┌───────────────────────────▼─────────────────────────────┐
│                    Rust Backend                         │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐  │
│  │ server  │  │executors │  │   git   │  │ services │  │
│  └─────────┘  └──────────┘  └─────────┘  └──────────┘  │
│                   │                                     │
│             ┌─────▼─────┐                               │
│             │  SQLite   │                               │
│             └───────────┘                               │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌─────▼─────┐       ┌────▼────┐
   │ Claude  │        │   Codex   │       │ Gemini  │
   │worktree1│        │ worktree2 │       │worktree3│
   └─────────┘        └───────────┘       └─────────┘
```

---

## 참고 레퍼런스

- [GitHub 리포: BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban)
- [공식 랜딩 페이지: vibekanban.com](https://vibekanban.online)
- [아키텍처 분석: vibe-kanban – a Kanban board for AI agents](https://virtuslab.com/blog/ai/vibe-kanban/)
- [한국어 도입기](https://bluedreamer-twenty.tistory.com/7)
- [데모: Run Multiple Claude Code Agents Without Git Conflicts](https://www.youtube.com/watch?v=W45XJWZiwPM)
- [데모: Claude Code Just Got Way Better | Auto Claude Kanban Boards](https://www.youtube.com/watch?v=vPPAhTYoCdA)

---

## 스킬 파일 구조

```
.agent-skills/vibe-kanban/
├── SKILL.md              # 메인 스킬 문서
├── SKILL.toon            # TOON 형식 (압축)
├── scripts/
│   ├── start.sh          # 서버 시작 래퍼
│   ├── cleanup.sh        # Worktree 정리
│   ├── mcp-setup.sh      # MCP 설정 자동화
│   └── health-check.sh   # 서버 상태 확인
├── references/
│   ├── environment-variables.md  # 환경 변수 레퍼런스
│   └── mcp-api.md                # MCP API 레퍼런스
└── templates/
    ├── claude-mcp-config.json    # Claude Code MCP 설정
    ├── docker-compose.yml        # Docker 배포 템플릿
    └── .env.example              # 환경 변수 예시
```

### 스크립트 사용법

```bash
# 서버 시작
bash scripts/start.sh --port 3001

# Worktree 정리
bash scripts/cleanup.sh --dry-run  # 미리보기
bash scripts/cleanup.sh --all       # 모든 VK worktree 삭제

# MCP 설정
bash scripts/mcp-setup.sh --claude  # Claude Code 설정
bash scripts/mcp-setup.sh --all     # 모든 에이전트 설정

# 상태 확인
bash scripts/health-check.sh
bash scripts/health-check.sh --json  # JSON 출력
```

---

## Quick Reference

```
=== 서버 실행 ===
npx vibe-kanban                       즉시 실행 (포트 3000)
PORT=3001 npx vibe-kanban --port 3001 포트 충돌 시 (Next.js 등)
http://localhost:3000                  보드 UI

=== 환경 변수 ===
PORT=3001                        포트 변경
VK_ALLOWED_ORIGINS=https://...   CORS 허용
ANTHROPIC_API_KEY=...            Claude Code 인증
OPENAI_API_KEY=...               Codex 인증
GOOGLE_API_KEY=...               Gemini 인증

=== MCP 연동 ===
npx vibe-kanban --mcp            MCP 모드
vk_list_cards                    카드(워크스페이스) 조회
vk_create_card                   카드 생성
vk_move_card                     상태 변경

=== 워크스페이스 흐름 ===
Create → Running → Needs Attention → Archive
Running: worktree 생성 + 에이전트 시작
Needs Attention: 완료 또는 입력 필요
Archive: PR merge 완료

=== MCP 설정 파일 위치 ===
Opencode: ~/.config/opencode/opencode.json
Claude Code: ~/.claude/settings.json 또는 .mcp.json

=== worktree 정리 ===
git worktree prune               고아 정리
git worktree list                목록 확인
git worktree remove <path>       강제 삭제
```
