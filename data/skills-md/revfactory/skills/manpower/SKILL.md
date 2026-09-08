---
name: manpower
description: "AI 프롬프팅 스킬 레벨 측정 및 성장 분석. Claude Code 세션 로그에서 사용자 프롬프트를 분석하여 8개 역량 축의 점수를 산출하고, 방사형 그래프와 주간 성장 추이를 시각화한다. 트리거: /manpower, AI 스킬 측정, 프롬프트 분석, AI 역량, 스킬레벨, manpower, AI 실력, 프롬프팅 능력, AI 활용도 분석"
---

# ManPower — AI Skill Level Assessment

Claude Code 세션 로그에서 사용자 프롬프트를 수집·분석하여 **8개 역량 축**의 점수를 산출하고, 방사형 그래프 + 주간 성장 추이로 시각화한다.

## 역량 축 (8개)

| 축 | 코드 | 측정 기준 |
|----|------|----------|
| **명확성** | clarity | 모호한 표현 없이 의도가 명확한가. 대명사("그거", "이것") 남발 대신 구체적 대상을 지칭하는가 |
| **구체성** | specificity | 요구사항에 제약조건, 포맷, 범위를 명시하는가. "대충 만들어줘" vs "A4 단면, 한글, 표 3개 포함" |
| **컨텍스트 제공** | context | 배경 정보, 기존 코드 경로, 기술 스택, 제약사항 등을 선제적으로 제공하는가 |
| **작업 분해** | decomposition | 복잡한 작업을 단계별로 나누어 지시하는가. 한 프롬프트에 10가지를 몰아넣지 않는가 |
| **도구 활용** | tool_usage | 슬래시 커맨드, 스킬, MCP, 에이전트 등 Claude Code 고급 기능을 활용하는가 |
| **반복 개선** | iteration | 결과물에 대해 구체적으로 피드백하고 점진적으로 개선해 나가는가 |
| **창의적 활용** | creativity | AI를 단순 코딩 보조 외에 분석, 설계, 자동화, 리서치 등 다양한 용도로 활용하는가 |
| **효율성** | efficiency | 최소한의 턴으로 원하는 결과를 얻는가. 불필요한 반복 없이 핵심을 짚는가 |

## 데이터 소스

worklog 스킬과 동일한 JSONL 소스를 사용한다.

```
~/.claude/projects/{경로해시}/{sessionId}.jsonl
```

- 경로 해시 규칙: cwd의 `/`를 `-`로 치환
- user 엔트리에 `timestamp`, `cwd`, `sessionId` 포함
- assistant 엔트리에 tool_use, text 포함

## 워크플로우

### Phase 1 — 기간 결정

사용자 입력에서 분석 기간을 결정한다.

| 입력 | 기간 |
|------|------|
| 인자 없음 | 최근 4주 (28일) |
| "이번 주" / "이번주" | 이번 ISO 주 |
| "이번 달" / "한 달" | 최근 30일 |
| "2주" / "최근 2주" | 최근 14일 |
| 특정 날짜 범위 | 해당 범위 |

기간 시작일의 00:00 KST를 UTC로 변환하여 필터링 기준으로 사용한다.

### Phase 2 — 세션 수집

```python
import json, os, glob
from datetime import datetime, timezone, timedelta
from collections import defaultdict

KST = timezone(timedelta(hours=9))
now_kst = datetime.now(KST)

# 기간 시작일 (기본: 28일 전)
start_date = (now_kst - timedelta(days=28)).replace(hour=0, minute=0, second=0, microsecond=0)
start_utc_iso = start_date.astimezone(timezone.utc).isoformat()
start_unix = start_date.timestamp()

projects_dir = os.path.expanduser("~/.claude/projects/")
sessions = []

for proj_dir in os.listdir(projects_dir):
    dpath = os.path.join(projects_dir, proj_dir)
    if not os.path.isdir(dpath):
        continue
    for jf in glob.glob(os.path.join(dpath, "*.jsonl")):
        if os.path.getmtime(jf) < start_unix:
            continue

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

        if first_ts and first_ts >= start_utc_iso:
            sessions.append({
                "path": jf,
                "first_ts": first_ts,
                "cwd": cwd,
                "size": os.path.getsize(jf)
            })

sessions.sort(key=lambda x: x["first_ts"])
```

### Phase 3 — 프롬프트 추출

각 세션에서 **사용자 프롬프트만** 추출한다. 분석 대상은 사용자의 지시 능력이므로 assistant 응답은 보조적으로만 참조한다.

```python
def extract_prompts(jsonl_path):
    """세션에서 사용자 프롬프트와 메타데이터를 추출."""
    prompts = []
    tool_uses_by_user = []  # 사용자가 활용한 슬래시 커맨드/스킬
    turn_count = 0
    assistant_corrections = 0  # "아니", "그게 아니라" 등 수정 횟수

    with open(jsonl_path) as f:
        for line in f:
            try:
                entry = json.loads(line)
                t = entry.get("type")

                if t == "user":
                    turn_count += 1
                    msg = entry.get("message", {})
                    content = msg.get("content", "") if isinstance(msg, dict) else ""

                    text = ""
                    if isinstance(content, str):
                        text = content
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                text = block["text"]
                                break

                    if not text.strip():
                        continue

                    # 슬래시 커맨드 감지
                    import re
                    cmd_match = re.search(r"<command-name>(/[\w:-]+)</command-name>", text)
                    if cmd_match:
                        tool_uses_by_user.append(cmd_match.group(1))

                    # 수정/교정 감지
                    correction_patterns = [
                        r"아니[요]?\s", r"그게 아니", r"다시\s", r"잘못",
                        r"that's not", r"no,?\s", r"wrong", r"undo",
                        r"되돌려", r"취소", r"rollback"
                    ]
                    for pat in correction_patterns:
                        if re.search(pat, text, re.IGNORECASE):
                            assistant_corrections += 1
                            break

                    prompts.append({
                        "text": text[:2000],
                        "timestamp": entry.get("timestamp", ""),
                        "turn": turn_count
                    })

            except:
                pass

    return {
        "prompts": prompts,
        "turn_count": turn_count,
        "tool_uses": tool_uses_by_user,
        "corrections": assistant_corrections
    }
```

### Phase 4 — 주간 그룹핑

수집된 프롬프트를 ISO 주차별로 그룹핑한다. 주간 성장 추이를 보기 위함이다.

```python
from datetime import datetime

def get_iso_week(timestamp_str):
    """ISO timestamp에서 'W{주차}' 문자열을 반환."""
    dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    iso = dt.isocalendar()
    return f"W{iso.week:02d}"

weekly_groups = defaultdict(lambda: {
    "prompts": [], "sessions": 0, "tool_uses": [],
    "corrections": 0, "turn_counts": []
})

for session in sessions:
    data = extract_prompts(session["path"])
    week = get_iso_week(session["first_ts"])
    weekly_groups[week]["prompts"].extend(data["prompts"])
    weekly_groups[week]["sessions"] += 1
    weekly_groups[week]["tool_uses"].extend(data["tool_uses"])
    weekly_groups[week]["corrections"] += data["corrections"]
    weekly_groups[week]["turn_counts"].append(data["turn_count"])
```

### Phase 5 — 역량 점수 산출 (하이브리드)

**5개 축은 `scripts/score_calculator.py`로 자동 채점하고, 3개 축만 LLM이 판단한다.** 이 구조로 객관성을 확보한다.

#### Step 1 — 자동 채점 (5축)

`score_calculator.py`를 실행하여 정량 지표 기반 점수를 산출한다.

```bash
python3 ~/.claude/skills/manpower/scripts/score_calculator.py --days 28 --output <workspace>/auto_scores.json
```

자동 채점은 2가지 데이터 소스를 사용한다:
1. **JSONL 프롬프트 분석** — 세션 로그에서 슬래시 커맨드, 키워드, 턴 수 등 추출
2. **프로젝트 환경 스캔** — 실제 프로젝트 디렉토리의 `.claude/` 구성을 직접 스캔 (에이전트, 스킬, CLAUDE.md, 외부 도구 등)

자동 채점 대상 축과 핵심 지표:

| 축 | 핵심 지표 | 데이터 소스 |
|----|----------|-----------|
| **도구활용** | 고유 커맨드 종류, 호출 빈도, 하네스/플러그인/외부도구 사용 여부 | JSONL 커맨드 + 환경 스캔 |
| **컨텍스트** | .claude/ 비율(환경 스캔), CLAUDE.md 수, 파일경로·스크린샷·URL | 환경 스캔 + JSONL 패턴 |
| **창의성** | 활용 도메인 종류(8카테고리), 고유 프로젝트 수, 메타활용 여부 | JSONL 키워드 + 환경 스캔 |
| **효율성** | 세션당 턴 수 중앙값, 수정/교정 비율, 중단 비율 | JSONL 턴 카운트 |
| **작업분해** | Plan→Implement 패턴, 하네스 세션 비율, **에이전트 파일 수, 스킬 파일 수** | JSONL + 환경 스캔 |

**환경 스캔 (`scan_project_environments`)이 포착하는 구조화된 AI 활용:**
- `.claude/agents/*.md` — 에이전트 정의 파일 수 (작업분해 점수에 반영)
- `.claude/skills/*/skill.md` — 커스텀 스킬 수 (작업분해 + 도구활용에 반영)
- `CLAUDE.md` — 프로젝트 컨텍스트 사전 구성 (컨텍스트 점수에 보너스)
- `settings.json` — 훅/퍼미션 설정 여부
- 외부 도구/플러그인 — RIPER-5, SuperPower, OhMyClaudeCode 등 CLAUDE.md 내 언급 감지

**자동 채점 점수는 LLM이 조정할 수 없다.** 공식이 산출한 그대로 사용한다. 공식 자체에 문제가 있으면 `score_calculator.py`를 수정한다.

#### Step 2 — LLM 판단 채점 (3축)

나머지 3축은 프롬프트 텍스트의 질적 분석이 필요하여 LLM이 판단한다. **단, 반드시 근거 프롬프트를 인용해야 한다.**

| 축 | LLM이 판단하는 이유 |
|----|-------------------|
| **명확성** | "의도가 명확한가"는 텍스트의 의미를 이해해야 판단 가능 |
| **구체성** | 제약조건·포맷 명시 여부는 내용 분석 필요 |
| **반복개선** | 피드백의 구체성은 텍스트 질적 분석 필요 |

**LLM 판단 필수 규칙:**
1. 점수와 함께 **근거 프롬프트 3개 이상**을 원문 인용하라 (좋은 예 + 나쁜 예 모두)
2. 인용 없는 점수는 무효다
3. 점수 범위는 자동 채점과 동일한 0~100 스케일을 사용한다

#### LLM 판단 3축 채점 기준

짧은 프롬프트가 반드시 나쁜 것은 아니다. 작업 복잡도에 비례하는 적절한 수준이 정답.

#### 대화 맥락 인식 (Context-Aware Scoring)

**`score_calculator.py`가 각 프롬프트를 대화 역할별로 자동 분류한다.** LLM 판단 시 이 분류를 반드시 참조하라.

| 역할 | 예시 | 채점 방식 |
|------|------|----------|
| `instruction` | "에이전트팀으로 리서치 진행해" | 정상 채점 — 명확성/구체성의 주요 평가 대상 |
| `confirmation` | "동일합니다", "네", "좋아요", "진행" | **채점 제외** — 이전 AI 응답에 대한 동의/확인은 대화 관리 행위이며, 짧은 것이 자연스러움 |
| `refinement` | "거기에 여백 16px 추가", "비율 조정" | 명확성 정상 채점. 구체성은 **증분 지시**로 평가 (이전 맥락이 있으므로 단독 평가 금지) |
| `feedback` | "좌측 바가 좋긴한데 인용문과 헷갈림" | 반복개선 채점 대상. 피드백의 구체성으로 평가 |
| `operational` | "3001 포트로 실행해", "커밋 푸시" | **채점 제외** — 운영 명령은 AI 소통 능력과 무관 |
| `command` | /harness, /skill-creator | **채점 제외** — 도구 호출 (도구활용 축에서 자동 채점됨) |
| `noise` | "Full transcript...", 시스템 출력 | **채점 제외** — 자동 생성 텍스트 |

**핵심 원칙:**
- `confirmation`을 "모호한 프롬프트"로 감점하지 마라. "동일합니다"는 이전 제안에 동의하는 완전한 의사 표현이다.
- `refinement`은 이전 결과가 전제되므로, 프롬프트 단독으로 정보가 부족해 보여도 감점하지 마라.
- `operational`("3000포트로 실행해")은 환경 조작이며, 짧은 것이 효율적이다.
- **채점 대상은 `instruction` + `refinement` + `feedback`뿐이다.** 나머지는 분모에서도 제외한다.

#### LLM 판단 3축 채점 기준

**명확성 (clarity)** — 프롬프트를 읽고 의도를 바로 파악할 수 있는가 (채점 대상 프롬프트만 평가)
- 90~100: 작업 복잡도에 맞는 적절한 지시. 단순 작업은 짧게, 복잡한 작업은 상세하게
- 80~89: 대부분 추가 질문 없이 실행 가능. 가끔 모호한 지칭이 있지만 맥락에서 추론 가능
- 65~79: 절반 이상 명확하지만, 기대 결과 누락으로 AI가 추측하는 경우 종종 있음
- 50~64: "고쳐줘", "이상해" 등 증상만 제시하고 기대 상태 미설명
- 0~49: 대부분 AI가 의도를 추측해야 함

**구체성 (specificity)** — 필요한 제약/포맷/범위를 명시하는가 (채점 대상 프롬프트만 평가)
- 90~100: 필요할 때 정밀한 제약 + 단순 작업에서는 의도적 위임 (적절한 위임도 구체성)
- 80~89: 주요 요구사항 명시. URL, 경로, 에러 등 구체적 근거 제공
- 65~79: 큰 방향은 제시하지만 포맷이나 제약이 빠지는 경우 있음
- 50~64: "만들어줘" 수준 포괄적 지시 다수
- 0~49: 거의 모든 프롬프트가 한 줄짜리 포괄적 지시

**반복 개선 (iteration)** — 결과물에 구체적 피드백을 주고 점진적으로 개선하는가 (feedback + refinement 평가)
- 90~100: 구체적 피드백 ("3번째 줄의 변수명을 X로") 또는 환경 설정을 체계적으로 반복 개선
- 80~89: 구체적 수정 지시를 주고 2~3회 반복으로 품질 도달
- 65~79: 피드백을 주지만 가끔 포괄적. 한 번에 완성되면 그대로 수용
- 50~64: 불만만 표현하고 개선 방향 미제시
- 0~49: 피드백 없이 수용하거나 포기

#### LLM 판단 출력 형식

각 축에 대해 점수 + 근거 프롬프트 인용을 포함한다:

```
**명확성: 80점 (A)**
- 좋은 예: "cover_01_dawn_walk.png 하단 이름을 '황민호 지음'" → 대상+행동이 한 문장에 명확
- 좋은 예: "README 요구사항에 Claude Code CLI 제거하고 에이전트 팀 활성화에 참고 링크 추가" → 삭제+추가 액션이 구체적
- 나쁜 예: "사이트가 이상해졌어" → 어떻게 이상한지 미기술
- 나쁜 예: "어색한 표현과 문체 수정" → 어떤 부분이 어색한지 미지정
```

### Phase 6 — 시각화

`scripts/radar_chart.py`를 사용하여 방사형 그래프와 주간 추이 차트를 생성한다.

1. 채점 결과를 JSON으로 정리한다:

```json
{
  "overall": {
    "labels": ["명확성", "구체성", "컨텍스트", "작업분해", "도구활용", "반복개선", "창의성", "효율성"],
    "scores": [85, 72, 78, 65, 90, 70, 82, 75],
    "max_score": 100
  },
  "weekly": [
    {"week": "W10", "scores": [80, 68, 75, 60, 85, 65, 78, 70], "total": 72.6},
    {"week": "W11", "scores": [82, 70, 76, 62, 88, 68, 80, 73], "total": 74.9},
    {"week": "W12", "scores": [85, 72, 78, 65, 90, 70, 82, 75], "total": 77.1}
  ]
}
```

2. 차트 생성 실행:

```bash
python3 ~/.claude/skills/manpower/scripts/radar_chart.py \
  "<output_dir>/manpower_chart.png" \
  "<workspace>/chart_data.json"
```

3. 차트 파일을 Read로 열어 사용자에게 보여준다.

### Phase 7 — 리포트 출력

분석 결과를 아래 포맷으로 사용자에게 보여준다.

```markdown
## ManPower — AI Skill Assessment

**분석 기간**: YYYY-MM-DD ~ YYYY-MM-DD (N개 세션, M개 프롬프트)
**종합 등급**: {등급} ({평균점수}점)

### 역량별 점수

| 역량 | 점수 | 등급 | 한줄 평가 |
|------|------|------|----------|
| 명확성 | 85 | A | 지시 대상과 행동이 거의 항상 명확함 |
| ... | ... | ... | ... |

### 강점 (상위 3개)
- **도구 활용** (90점) — 슬래시 커맨드, 스킬, 에이전트 팀 등 고급 기능을 적극 활용
- ...

### 성장 기회 (하위 3개)
- **작업 분해** (65점) — 복잡한 작업을 한 프롬프트에 담는 경향. 단계별 분리 추천
- ...

### 주간 성장 추이

| 주차 | 종합 | 변화 | 주요 변화 |
|------|------|------|----------|
| W10 | 72.6 | — | 기준점 |
| W11 | 74.9 | +2.3 | 구체성, 도구활용 향상 |
| W12 | 77.1 | +2.2 | 명확성, 창의성 향상 |

### AI와 더 잘 소통하는 팁
(하위 역량 기반으로 맞춤 제안 3~5개)
```

**차트 이미지**를 리포트 앞에 Read로 표시한다.

### Phase 8 — 결과 저장

분석 결과를 `manpower/` 디렉토리에 저장한다.

- `manpower/YYYY-MM-DD_report.md` — 마크다운 리포트
- `manpower/YYYY-MM-DD_chart.png` — 방사형 그래프 이미지
- `manpower/_data/YYYY-MM-DD.json` — 원본 채점 데이터 (추후 비교용)

이전 분석 결과가 있으면 `_data/` 디렉토리의 JSON을 참조하여 장기 추이도 반영한다.

## 등급 체계

| 점수 구간 | 등급 | 설명 |
|----------|------|------|
| 90~100 | S | AI 마스터. 프롬프트 엔지니어링 전문가 수준 |
| 80~89 | A | 숙련자. AI와의 협업이 자연스럽고 효율적 |
| 70~79 | B | 중급자. 핵심을 알고 있으나 개선 여지 있음 |
| 60~69 | C | 초중급. 기본기는 있으나 효율성 부족 |
| 50~59 | D | 입문자. AI 활용의 기본기를 다져야 함 |
| 0~49 | F | 시작 단계. 체계적 학습 권장 |

## 에러 핸들링

| 상황 | 처리 |
|------|------|
| 세션이 0개 | "분석할 세션이 없습니다. 기간을 확인해주세요" 안내 |
| 특정 주차 프롬프트 < 5개 | 해당 주 "데이터 부족" 표시, 채점 생략 |
| JSONL 파싱 실패 | 해당 세션 스킵, 나머지로 진행 |
| matplotlib 없음 | `pip install matplotlib` 안내 후 텍스트 테이블로 폴백 |
| 차트 생성 실패 | 텍스트 리포트만 출력 (차트 없이 진행) |
| 이전 분석 데이터 없음 | 장기 추이 생략, 현재 분석만 표시 |

## 테스트 시나리오

**정상 흐름**
1. 사용자가 `/manpower` 실행
2. 최근 4주간 세션 30개, 프롬프트 250개 수집
3. 3주차로 그룹핑 (1주차 데이터 부족으로 제외)
4. 주차별 채점 → 종합 점수 산출
5. 방사형 그래프 + 주간 추이 차트 생성
6. 마크다운 리포트 + 차트 이미지 표시
7. `manpower/` 디렉토리에 저장

**데이터 부족 흐름**
1. 사용자가 `/manpower 이번 주` 실행
2. 이번 주 세션 2개, 프롬프트 3개 수집
3. "데이터 부족 — 최소 5개 프롬프트 필요" 안내
4. 기간 확대 제안 ("최근 2주로 확대할까요?")
