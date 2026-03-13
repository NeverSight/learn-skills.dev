---
name: claude-agent-sdk
description: Builds Claude Agent SDK agents in Python. Use when creating custom tools, hooks, sub-agents, or MCP integrations with the Agent SDK. Python 에이전트 구축 시 사용.
---

# Claude Agent SDK

Python 기반 독립 실행형 AI 에이전트 코드 생성.

**vs agent-creator**:
| 항목 | agent-creator | claude-agent-sdk |
|------|---------------|------------------|
| 결과물 | `.claude/agents/*.md` | `*.py` 파일 |
| 실행 환경 | Claude Code 내부 | 독립 Python 앱 |
| 용도 | 작업 위임 | 프로덕션 자동화 |

## Instructions

### 워크플로우 1: 새 에이전트 프로젝트

1. **용도 파악**
   - 무엇을 자동화할 것인가?
   - 어떤 도구가 필요한가? (파일, 명령, 웹, 커스텀)
   - 서브에이전트 필요 여부

2. **템플릿 선택**
   | 용도 | 템플릿 |
   |------|--------|
   | 최소 시작 | `templates/basic-agent.py` |
   | 커스텀 도구 | `templates/tool-agent.py` |
   | 훅 (검증/로깅) | `templates/hook-agent.py` |
   | 서브에이전트 | `templates/multi-agent.py` |
   | 프로덕션 | `templates/production-agent.py` |

3. **프로젝트 구조 생성**
   ```
   {project}/
   ├── pyproject.toml
   ├── agent.py          # 메인 에이전트
   ├── tools.py          # 커스텀 도구 (선택)
   └── hooks.py          # 훅 정의 (선택)
   ```

4. **코드 생성**: 템플릿 기반으로 사용자 요구에 맞게 수정

### 워크플로우 2: 기능 추가

기존 에이전트에 기능 추가 시:

1. **키워드 → 리소스 매칭**
   | 키워드 | 리소스 |
   |--------|--------|
   | 설치, pyproject | `resources/01-setup.md` |
   | query, 기본, 옵션 | `resources/02-query-options.md` |
   | 도구, @tool | `resources/03-custom-tools.md` |
   | 훅, hook, 검증 | `resources/04-hooks.md` |
   | 서브에이전트, 위임 | `resources/05-subagents.md` |
   | 세션, resume | `resources/06-sessions.md` |
   | MCP, playwright | `resources/07-mcp.md` |

2. **리소스 로드 → 패턴 적용**

### 워크플로우 3: 코드 리뷰/개선

기존 에이전트 코드 분석 요청 시:

1. **구조 확인**: 현재 사용 중인 기능 파악
2. **개선점 제안**:
   - 에러 핸들링 추가
   - 훅으로 검증/로깅
   - 서브에이전트로 분리
   - 세션 관리 추가

## 핵심 패턴

### 기본 query()

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for msg in query(
    prompt="작업 지시",
    options=ClaudeAgentOptions(
        allowed_tools=["Read", "Edit", "Bash"],
        cwd="/path/to/project",
        permission_mode="acceptEdits"
    )
):
    if hasattr(msg, "result"):
        print(msg.result)
```

### 커스텀 도구

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("search", "검색 수행", {"query": str})
async def search(args):
    return {"content": [{"type": "text", "text": f"결과: {args['query']}"}]}

server = create_sdk_mcp_server("my-tools", "1.0.0", tools=[search])
```

### 훅

```python
async def validate_bash(input_data, tool_use_id, context):
    cmd = input_data.get("tool_input", {}).get("command", "")
    if "rm -rf" in cmd:
        return {"decision": "block", "reason": "위험한 명령어"}
    return {}

options = ClaudeAgentOptions(
    hooks={"PreToolUse": [HookMatcher(matcher="Bash", hooks=[validate_bash])]}
)
```

## 중요 원칙

1. **allowed_tools 최소화**: 필요한 도구만 허가
2. **permission_mode 신중히**: `bypassPermissions`는 프로덕션 전용
3. **에러 핸들링**: `try/except`로 graceful 처리
4. **세션 활용**: 장기 작업은 session_id 저장 후 resume

## Technical Details

- `REFERENCE.md`: SDK API 전체 개요
- `resources/`: 기능별 상세 패턴
- `templates/`: 완전한 에이전트 코드
