---
name: playtest-verdict
description: "Records prototype playtest sessions as data, has a read-only judge propose a verdict (holds, refuted, unknown) for each concept hypothesis from those records, promotes measured numbers from assumed to measured with a checkable source, and calibrates assumptions from recorded stage statistics: compares assumed levels, durations, kills, and income with the records, compares simulated stage clear rates with measured ones, and suggests survival curve values. Use after playing a prototype, when deciding whether a concept's hypotheses survived, before turning an assumed number into a measured one, or when checking balance assumptions against real runs."
---

# 플레이 기록과 가설 판정

프로토타입을 플레이한 기록을 데이터로 남기고, 브리프의 가설이 버텼는지 **기록만 보고** 판정한다. 목적은 "해 보니 재미있었다"가 증거처럼 쓰이는 것을 막는 것이다. 재미를 점수로 매기지 않는다.

## 원칙

- **기록이 증거다.** 판정은 `data/playtests.json`에 적힌 관찰값만 근거로 쓴다. 대화에서 들은 인상, 만든 쪽의 설명, 에이전트의 추측은 증거가 아니다.
- **관찰과 선호를 나눈다.** "3판부터 예고를 안 보고 거리만 벌렸다"는 관찰이다. "재미있다", "소리가 좋다"는 선호다. 선호는 `notes`에 `preference`로 남기되 판정 근거로 쓰지 않는다.
- **모르면 unknown이다.** 표본이 계획보다 적거나, 신호가 나왔는지 기록으로 가릴 수 없으면 `unknown`이다. unknown은 실패가 아니다.
- **값을 지어내지 않는다.** 관찰값은 플레이한 사람이 말한 것이나 로그 파일에서 읽은 것만 적는다. 에이전트가 짐작한 값을 관찰값으로 적지 않는다.
- **판정은 따로, 확정은 사용자가.** 판정 에이전트(읽기 전용)가 제안하고, 메인 에이전트가 `proposed`로 기록하고, 사용자가 확인하면 `approved`로 바꾼다.

## 도구

검사는 공용 스킬 [studio-data](../studio-data/SKILL.md)의 `studio.py`로 한다. 이 스킬과 함께 설치한다. 명령은 게임 프로젝트 폴더에서 Claude Code 설치 기준으로 적었다. Codex는 `.agents/skills/…`, Windows PowerShell은 `python3` 대신 `py`([실행 경로](../studio-data/SKILL.md#실행)).

| 명령 | 확인하는 것 | 확인하지 않는 것 |
|---|---|---|
| `python3 .claude/skills/studio-data/scripts/studio.py check .` | 판정이 근거 세션을 가리키는가, 그 세션이 있고 그 가설을 관찰했는가, 가설·컨셉 id가 맞는가, 세션의 판 수·사람 수 | 관찰값이 정말 틀렸다는 신호에 해당하는가 |
| `… check . --fail-on-assumed` | 선택한 컨셉의 가설 중 확정된 버팀·틀림이 아닌 것이 남았는가 | 가설이 좋은 가설인가 |
| `… provenance design/ --check-paths` | `[측정: data/playtests.json#세션 id]`의 세션이 실제 기록에 있는가 | 측정값을 옮겨 적을 때 틀리지 않았는가 |
| `… runlog playtests/세션/runs.csv` | 판별 로그를 세션의 단계 기록으로 모아 출력(강화 상태별 묶음). 파일에 쓰지 않는다 | 로그가 맞는가 |
| `… calibrate data/meta_combat.json` | 가정값과 기록의 차이, 단계 통과율의 예측과 실측, 기록에 맞는 생존 곡선 값 제안 | 재미, 실제 난이도. 파일을 고치지 않는다 |

Claude Code에서는 한 번 `python3 .claude/skills/studio-data/scripts/studio.py setup claude .`를 실행해 판정 에이전트와 훅을 설치한다([setup](../studio-data/SKILL.md#claude-code-연결)). 스킬을 다시 설치한 뒤에도 다시 실행한다.

## 절차

### 1. 플레이 전: 가설에 id를 단다

`design/concepts.json`에서 시험할 컨셉의 `brief.hypotheses`마다 `id`를 넣는다(소문자·숫자·밑줄, 예: `density_timing`). 기록과 판정은 이 id로 가설을 가리킨다. 문장을 바꿔도 id는 그대로 둔다.

시험 전에 가설의 `test`에 적은 표본(사람 수, 판 수)과 기록할 값을 사용자와 확인한다. 프로토타입이 그 값을 로그로 남기게 하면 옮겨 적는 실수가 줄어든다.

### 2. 플레이한 뒤: 세션을 기록한다

한 번 모여 플레이할 때마다 `data/playtests.json`의 `playtests`에 세션 하나를 넣는다. 형식은 [references/playtest-record.md](references/playtest-record.md).

- 날짜, 플레이한 사람, 빌드(커밋 해시), 판 수
- 가설별 관찰값(`observations`): 가설의 `failure_signal`을 판단하는 데 필요한 값. 로그에서 읽었으면 `source`에 파일을 적는다
- 그 밖의 관찰과 선호(`notes`)

사용자에게 묻지 않고 채운 값이 있으면 그 사실을 보고한다. 로그 파일이 있으면 `logs`에 경로를 적는다. 기록 파일을 지우지 않는다.

### 3. 판정한다

- **Claude Code**: 판정 에이전트 `studio-judge`에게 맡긴다. 예: "studio-judge로 ripening_gems의 가설을 판정해 줘". 판정 에이전트는 파일을 고치지 못하고(훅이 막는다), 가설별 제안과 `verdicts`에 넣을 JSON을 돌려준다.
- **Codex 등 판정 에이전트가 없는 환경**: 같은 절차를 직접 따른다. 판정 기준은 [references/playtest-record.md](references/playtest-record.md#판정)이다. 만드는 쪽과 판정하는 쪽이 분리되지 않았다는 사실을 보고에 적는다.

받은 제안을 `verdicts`에 `"status": "proposed"`로 넣고 사용자에게 보여 준다. 사용자가 확인하면 `approved`로 바꾼다. 다시 판정할 때는 지난 판정을 지우지 않고 `status`를 `cut`으로 둔 뒤 새 판정을 넣는다.

### 4. 측정값을 올린다

관찰값을 **그대로** 옮긴 수치만 `[가정]`에서 `[측정: data/playtests.json#세션 id]`로 바꾼다. 데이터 파일(아이템·강화·적)은 `provenance`를 `{"kind": "measured", "source": "data/playtests.json#세션 id"}`로 둔다.

- 평균·비율을 새로 계산한 값은 `[계산: 스크립트 또는 결과 파일]`이다. 계산한 스크립트가 없으면 올리지 않는다.
- 판정 기준의 문턱값(예: `80% [가정]`)은 측정값이 아니다. 기획 판단이므로 `[가정]`으로 둔다.
- 올린 뒤 `provenance design/ --check-paths`로 세션이 실제로 있는지 확인한다.

### 5. 가정값을 보정한다

세션에 단계 기록과 그때 가진 영구 강화를 적었으면 `calibrate`로 기획의 가정값과 비교한다. 평균을 손으로 내지 않는다. 프로토타입의 판별 로그(CSV)를 `runlog`로 모아 세션에 합친다(판 사이에 강화를 사서 상태가 바뀌어도 상태별 묶음으로 나온다). 형식과 읽는 법은 [references/calibration.md](references/calibration.md).

```bash
python3 .claude/skills/studio-data/scripts/studio.py runlog playtests/pt_20261112_1/runs.csv
python3 .claude/skills/studio-data/scripts/studio.py calibrate data/meta_combat.json --out reports/calibrate.json
```

- 가정값 비교: 판 안 성장의 단계별 레벨, 재화 흐름의 길이·처치 수·수입을 기록의 평균과 나란히 놓는다. 시뮬레이터 설정 없이 폴더(`calibrate .`)만 넘겨도 된다.
- 통과율 비교: 그 세션의 강화·레벨로 다시 계산한 예측이 실측의 95% 구간 안인지 본다. 구간이 넓으면 표본이 적은 것이다.
- 생존 곡선 제안: 기록이 지금 값과 구분될 때만 `slope`·`even_margin`을 범위와 함께 제안한다. "제안 없음"이면 바꿀 근거가 없는 것이다. 근거가 모자란 값은 제안하지 않고 이유를 남긴다.
- 제안은 자동으로 적용하지 않는다. 사용자에게 보여 주고 어느 값을 옮길지 정한다. 레벨을 먼저 옮기고 생존 곡선을 옮긴다. 옮긴 값에는 출처를 남긴다(기록을 그대로 옮기면 측정, 평균이나 제안이면 `reports/calibrate.json`을 출처로 한 계산). 기획 목표 범위는 의도이므로 바꾸지 않는다.

### 6. 틀렸으면 되돌아간다

`refuted`가 확정되면 다음 중 하나를 사용자에게 제안한다. 결정은 사용자가 한다.

- 가설이 기대는 규칙 하나를 바꿔 다시 시험한다(브리프의 `prototype`과 가설을 고친다).
- 컨셉을 `proposed`로 되돌리고, 탈락 사유가 증명되었으면 `hard_reject`와 함께 `cut`으로 둔다. 다른 후보를 고르려면 [concept-exploration](../concept-exploration/SKILL.md)의 선택 단계로 돌아간다.
- `unknown`이면 무엇이 부족했는지(표본, 기록하지 못한 값)를 다음 세션 계획으로 남긴다.

## 보고

- `check` 결과 그대로: 판정별 버팀·틀림·모름, 근거 세션 수·판 수·사람 수, 오류·경고 수, `INCOMPLETE` 여부
- 확정되지 않은 가설 목록(`--fail-on-assumed`의 gate 줄)
- 이번에 `[측정]`으로 올린 수치와 그 출처
- `calibrate`를 돌렸으면: 쓴 세션과 표본, 표시된 차이, 구간을 벗어난 단계, 제안과 옮긴 값
- 사용자 확인이 필요한 것: 제안 판정의 확정, 틀린 가설 이후의 방향
- 실행하지 못한 검사가 있으면 그 사실

## 한계

- 검사기는 판정이 **증거를 가리키는지**만 본다. 관찰값이 틀렸다는 신호에 해당하는지는 판정 에이전트와 사용자가 본다.
- 표본이 충분한지 숫자로 막지 않는다. 판 수·사람 수를 보여 줄 뿐이고, 가설의 `test`에 적은 계획과 비교하는 것은 판정 에이전트가 한다.
- 보정 값은 기록한 빌드와 플레이어에서 나온 값이다. 보정해도 시뮬레이션 결과로 재미나 실제 난이도를 판정하지 않는다.
- 판정 에이전트와 훅은 Claude Code 전용이다. 훅 입력의 에이전트 이름(`agent_type`)으로 판정 에이전트를 구분한다(Claude Code 2.1.316, WSL에서 확인. Windows는 미확인).

예시: `studio-data/assets/sample-project/data/playtests.json` (실제 플레이 기록이 아니다).
