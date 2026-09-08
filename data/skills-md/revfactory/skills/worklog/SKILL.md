---
name: worklog
description: "오늘 진행한 모든 Claude Code 세션을 분석하여 주간 워크로그 파일(YYYY-WXX.md)로 정리. 트리거 /worklog, 워크로그, 작업 정리, 오늘 한 거 정리, 작업 기록"
---

# Worklog — 전체 세션 기반 작업 기록 생성기

오늘(00시~현재) 진행한 **모든 Claude Code 세션**의 대화 로그를 분석하여 주간 워크로그 마크다운 파일로 정리한다.

## 데이터 소스

Claude Code는 세션별 전체 대화를 JSONL로 저장한다.

### 전체 대화 로그 (Primary)
```
~/.claude/projects/{경로해시}/{sessionId}.jsonl
```
- 경로 해시 규칙 — cwd의 `/`를 `-`로 치환 (예시 `/home/user/project` → `-home-user-project`)
- 각 줄은 JSON 객체 (type: user | assistant | progress | system)
- **user 엔트리에 `timestamp`, `cwd`, `sessionId` 포함** — 세션 시작 시간과 프로젝트 경로의 신뢰할 수 있는 출처
- assistant 타입에 텍스트 응답, tool_use 포함

### 세션 메타데이터 (Unreliable — 보조용)
```
~/.claude/sessions/{PID}.json
```
- **주의** — 종료된 세션의 파일은 삭제됨. 현재 활성 세션만 존재한다
- 세션 검색의 주 소스로 사용하지 않는다 (JSONL 스캔이 Primary)

## 워크플로우

### Phase 1 — 오늘의 세션 수집

**`~/.claude/projects/*/` 디렉토리에서 JSONL 파일을 직접 스캔한다.** `sessions/`에 의존하지 않는다.

```python
import json, os, glob
from datetime import datetime, timezone, timedelta

# 오늘 00:00 KST의 UTC timestamp
KST = timezone(timedelta(hours=9))
today_local = datetime.now(KST).replace(hour=0, minute=0, second=0, microsecond=0)
today_utc_iso = today_local.astimezone(timezone.utc).isoformat()

# 오늘 00:00의 Unix timestamp (mtime 비교용)
today_unix = today_local.timestamp()

projects_dir = os.path.expanduser("~/.claude/projects/")
sessions = []

for proj_dir in os.listdir(projects_dir):
    dpath = os.path.join(projects_dir, proj_dir)
    if not os.path.isdir(dpath):
        continue
    for jf in glob.glob(os.path.join(dpath, "*.jsonl")):
        # Step 1 — mtime으로 빠른 사전 필터 (오늘 수정된 파일만)
        if os.path.getmtime(jf) < today_unix:
            continue

        # Step 2 — 첫 user/system 엔트리의 timestamp로 실제 시작일 확인
        first_ts = None
        cwd = None
        with open(jf) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("type") in ("user", "system"):
                        first_ts = entry.get("timestamp")
                        cwd = entry.get("cwd")
                        break
                except:
                    pass

        # Step 3 — 오늘 시작된 세션만 포함 (어제 시작 → 오늘 mtime인 세션 제외)
        if first_ts and first_ts >= today_utc_iso:
            sessions.append({
                "path": jf,
                "first_ts": first_ts,
                "cwd": cwd,
                "proj_dir": proj_dir,
                "size": os.path.getsize(jf)
            })

# 시간순 정렬
sessions.sort(key=lambda x: x["first_ts"])
```

**세션 수집 핵심 규칙**
1. `mtime >= 오늘 00:00` 으로 사전 필터 (빠른 I/O)
2. JSONL 첫 엔트리의 `timestamp`로 실제 시작일 확인 (정확성)
3. 어제 시작되어 오늘까지 이어진 세션은 **제외** (mtime 오탐 방지)
4. `sessions/` 디렉토리는 참조하지 않음 (종료된 세션 파일 삭제됨)

### Phase 2 — 세션별 대화 분석

각 세션의 JSONL 파일에서 **작업 요약에 필요한 정보만** 효율적으로 추출한다.

**추출 전략 — 선택적 읽기**

JSONL이 수 MB일 수 있으므로, 모든 줄을 분석하지 않는다.

```python
def extract_session_summary(jsonl_path, max_user_msgs=50):
    """세션에서 작업 요약에 필요한 핵심 정보만 추출"""
    user_requests = []     # 사용자가 요청한 것
    files_touched = []     # Write/Edit로 생성·수정한 파일
    tools_used = set()     # 사용한 도구 종류
    asst_conclusions = []  # 어시스턴트의 주요 결론 텍스트

    with open(jsonl_path) as f:
        for line in f:
            try:
                entry = json.loads(line)
                t = entry.get("type")

                if t == "user":
                    msg = entry.get("message", {})
                    content = msg.get("content", "") if isinstance(msg, dict) else ""
                    if isinstance(content, str) and content.strip():
                        # command-name 태그에서 슬래시 커맨드 추출
                        if "<command-name>" in content:
                            import re
                            cmd = re.search(r"<command-name>(/\w+)</command-name>", content)
                            if cmd:
                                user_requests.append(cmd.group(1))
                        else:
                            user_requests.append(content[:150])
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                user_requests.append(block["text"][:150])
                                break

                elif t == "assistant":
                    msg = entry.get("message", {})
                    for block in msg.get("content", []):
                        if not isinstance(block, dict):
                            continue
                        if block.get("type") == "tool_use":
                            name = block.get("name", "")
                            tools_used.add(name)
                            inp = block.get("input", {})
                            # Write/Edit → 파일 경로 수집
                            if name in ("Write", "Edit"):
                                fp = inp.get("file_path", "")
                                if fp:
                                    files_touched.append(fp)
                            # Agent → description 수집
                            elif name == "Agent":
                                desc = inp.get("description", "")
                                if desc:
                                    user_requests.append(f"[Agent] {desc}")
                        elif block.get("type") == "text":
                            text = block.get("text", "").strip()
                            # 마지막 몇 개의 어시스턴트 텍스트만 보관 (결론부)
                            if len(text) > 20:
                                asst_conclusions.append(text[:300])
                                if len(asst_conclusions) > 10:
                                    asst_conclusions.pop(0)

                # progress 타입은 스킵 (도구 실행 중간 결과 — 불필요)

            except:
                pass

    return {
        "user_requests": user_requests[:max_user_msgs],
        "files_touched": list(set(files_touched)),
        "tools_used": tools_used,
        "conclusions": asst_conclusions[-5:]  # 마지막 5개만
    }
```

**추출 대상 (우선순위순)**
1. **사용자 요청** — 무엇을 시켰는지 (슬래시 커맨드 포함)
2. **Write/Edit 파일 경로** — 무엇을 만들었는지
3. **Agent 호출** — 서브에이전트/팀 작업 내용
4. **어시스턴트 결론** — 마지막 5개 텍스트 블록 (결과 요약)

**건너뛰는 것**
- `progress` 타입 전체 (도구 실행 중간 로그)
- `tool_result` (도구 출력 — 대부분 대용량)
- `Read`/`Glob`/`Grep` 도구 입력 (탐색일 뿐 결과물 아님)

### Phase 3 — 프로젝트 그룹핑

```python
from collections import defaultdict

projects = defaultdict(lambda: {"sessions": [], "cwd": None})

for s in sessions:
    # cwd에서 프로젝트명 추출 (마지막 디렉토리명)
    cwd = s["cwd"] or ""
    proj_name = os.path.basename(cwd) or s["proj_dir"]
    projects[proj_name]["sessions"].append(s)
    projects[proj_name]["cwd"] = cwd
```

- 같은 `cwd`의 세션은 하나의 프로젝트로 합친다
- 프로젝트명은 cwd 마지막 디렉토리명
- 대화에서 명확한 프로젝트명이 나오면 그것을 우선 사용

### Phase 4 — 범위 결정

사용자 입력에 따라 범위를 결정한다.

| 입력 | 범위 |
|------|------|
| 인자 없음 / "전체" | 오늘의 모든 세션 |
| "오늘 한 거만" | 오늘의 모든 세션 (동일) |
| "방금 한 거" | 현재 대화만 간략히 |
| "이번 주" | 이번 주 모든 세션 (timestamp 필터를 월요일 00:00으로 변경) |

### Phase 5 — ISO 주차 계산 및 파일 처리

1. 오늘 날짜의 ISO 주차를 계산한다

```bash
date +"%G-W%V"
```

2. 워크로그 디렉토리와 파일 경로를 결정한다
   - 디렉토리 — 현재 작업 디렉토리 하위 `worklog/`
   - 파일명 — `{YYYY}-W{XX}.md` (예시 `worklog/2026-W12.md`)

3. 해당 파일이 존재하면 읽고, 없으면 새로 생성한다
   - 새 파일 헤더 — `# YYYY-WXX`

4. 오늘 날짜 섹션(`## YYYY-MM-DD`)이 이미 있는지 확인한다
   - **있으면** — 전체 교체 (세션 전체를 다시 분석하므로 기존 내용 대체)
   - **없으면** — 새 날짜 섹션 생성 (이전 날짜와 `---` 구분선으로 분리)

### Phase 6 — 워크로그 작성

아래 포맷을 **정확히** 따른다. 예외 없음.

#### 포맷 규칙

**요약 (callout 바깥)**
```markdown
## YYYY-MM-DD

**프로젝트명** — 핵심 내용을 쉼표로 나열
**프로젝트명2** — 핵심 내용을 쉼표로 나열
다음 → 후속 작업 내용
```

- 한 날짜 = 하나의 `##` 섹션
- 프로젝트별 한 줄 요약 — `**프로젝트명** — 핵심만 쉼표로 나열`
- 다음 할 일은 `다음 →` 한 줄로
- 요약 부분은 **최대 6~7줄**

**상세 (옵시디언 callout 접기)**
```markdown
> [!note]- 상세
> **프로젝트명**
> - 구체적 작업 내용 1
> - 구체적 작업 내용 2
> - → 결과물 경로나 산출물
>
> **프로젝트명2**
> - 구체적 작업 내용
> - → 결과물
```

- `> [!note]- 상세` 형태 (마이너스로 접힌 상태 시작)
- callout 안에서 `**프로젝트명**`으로 구분
- 불릿 포인트로 구체적 내용 (모든 줄 앞에 `> ` 필수)
- 결과물은 각 프로젝트 마지막에 `→` 로 표시
- callout 내 빈 줄은 `>` 만 있는 줄로 표현

**공통 규칙**
- 한국어 반말
- 콜론(`:`) 사용 금지 — 절대 쓰지 않는다
- 날짜 사이에 `---` 구분선

#### 완성 예시

```markdown
# 2026-W12

## 2026-03-16

**하네스** — agent-research 스킬 리팩토링, 팀 모드 기본값 변경
**프론트엔드** — 대시보드 차트 컴포넌트 추가
다음 → 리서치 팀 테스트 시나리오 작성

> [!note]- 상세
> **하네스**
> - agent-research 스킬에서 서브에이전트 → 에이전트 팀 모드로 전환
> - orchestrator-template.md에 팀 모드 Phase 추가
> - references/team-examples.md에 리서치 팀 예시 추가
> - → `.claude/skills/harness/SKILL.md` 업데이트 완료
>
> **프론트엔드**
> - 대시보드에 일별 활성 사용자 차트 추가
> - recharts 라이브러리 도입
> - → `src/components/DailyActiveChart.tsx` 생성

---

## 2026-03-17

**하네스** — worklog 스킬 생성
다음 → 실제 사용 테스트

> [!note]- 상세
> **하네스**
> - 대화 기반 작업 기록을 주간 마크다운으로 정리하는 스킬 생성
> - 옵시디언 callout 접기 포맷 적용
> - → `.claude/skills/worklog/skill.md` 생성
```

### Phase 7 — 파일 저장

1. `worklog/` 디렉토리가 없으면 생성한다
2. 주차 파일에 작성한 내용을 저장한다
3. 오늘 날짜 섹션이 이미 있으면 교체, 없으면 추가
4. 다른 날짜의 기존 내용은 절대 건드리지 않는다
5. 날짜 순서를 유지한다 (오래된 날짜가 위)

### Phase 8 — 사용자에게 요약 표시

파일 저장 후, **요약 부분만** 사용자에게 보여준다 (상세 callout 제외).
파일 저장 경로도 함께 안내한다.
분석한 세션 수와 프로젝트 수도 언급한다.

## 에러 핸들링

| 상황 | 처리 |
|------|------|
| 오늘 세션이 없음 | "오늘 진행한 세션이 없습니다" 안내 |
| JSONL 파일 읽기 실패 | 해당 세션 스킵, 나머지 세션으로 진행 |
| 주차 파일 쓰기 실패 | 에러 메시지와 함께 내용을 텍스트로 출력 |
| 프로젝트명 판단 불가 | 경로 해시 디렉토리명에서 마지막 세그먼트 사용 |
| JSONL 파싱 에러 | 해당 줄 스킵, 나머지 줄로 진행 |
| 첫 엔트리에 timestamp 없음 | mtime 기반으로 폴백 (경고 포함) |

## 테스트 시나리오

**정상 흐름**
1. 오늘 5개 프로젝트에서 9개 세션 진행 (일부 종료됨)
2. `/worklog` 실행
3. `~/.claude/projects/*/` 스캔으로 9개 세션 발견
4. 첫 엔트리 timestamp로 어제 시작 세션 2개 제외 → 7개 확정
5. 5개 프로젝트로 그룹핑
6. `worklog/2026-WXX.md` 파일 생성
7. 요약만 사용자에게 표시

**교체 흐름**
1. 이미 오늘 날짜 워크로그가 있는 상태에서 추가 작업 후 `/worklog` 실행
2. 오늘의 모든 세션을 다시 분석
3. 기존 오늘 날짜 섹션을 새 내용으로 교체
4. 다른 날짜 내용은 유지
