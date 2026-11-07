---
name: combat-balance
description: "Connects player, item, upgrade, and enemy data through one stat model and a chosen defense formula (flat, ratio, level-scaled ratio, or capped percent), computes hits and seconds to kill and to die for each stage and enemy, and flags results outside designer target ranges. Use when setting or reviewing combat stats, choosing a defense formula, or checking difficulty per zone, level, or wave in any genre and engine."
---

# 전투 계산: 하나의 스탯 모델로 잇기

플레이어, 아이템, 영구 강화, 적의 스탯을 하나의 공식으로 이어 "이 단계의 기준 장비로 이 적을 몇 번·몇 초에 잡나(처치)", "이 적에게 몇 번·몇 초 맞으면 쓰러지나(버팀)"를 계산한다. 목적은 아이템 점수와 적 위협도를 따로 감으로 매기는 대신, 같은 숫자로 요소 사이의 관계를 확인하는 것이다.

계산은 **기대값**이다. 회피, 이동, 광역 공격, 상태 이상, 조작 실력은 넣지 않는다. 결과로 실제 난이도나 재미를 판정하지 않고, 목표에서 벗어난 곳과 단계 사이의 불연속을 찾는 데 쓴다.

## 도구

검사와 계산은 공용 스킬 [studio-data](../studio-data/SKILL.md)의 `studio.py`로 한다. 이 스킬과 함께 설치한다. 명령은 게임 프로젝트 폴더에서 Claude Code 설치 기준으로 적었다. Codex는 `.agents/skills/…`, Windows PowerShell은 `python3` 대신 `py`([실행 경로](../studio-data/SKILL.md#실행)).

| 명령 | 하는 일 |
|---|---|
| `python3 .claude/skills/studio-data/scripts/studio.py check .` | 전투 설정 형식, 참조(아이템·강화·적 id), 단계·적마다 처치·버팀 계산, 목표 이탈 경고 |
| `… check . --table combat` | 단계 × 적 계산표(마크다운)를 대화에 붙일 수 있게 출력 |
| `… check . --fail-on-assumed` | 공식·목표·단계의 출처가 가정이면 실패 (확정 판정 전) |
| `… view .` | 전투 계산 탭: 공식, 스탯 역할, 목표 범위, 단계별 계산표(목표 이탈 칸 강조) |

데이터는 `data/combat.json` 한 파일이다. 형식은 [references/combat-format.md](references/combat-format.md). 아이템·강화·적 데이터는 [progression-economy](../progression-economy/SKILL.md)의 원본을 그대로 참조하며 수치를 옮겨 적지 않는다. 프로젝트 폴더(`check .`)로 검사해야 참조를 확인한다. 함께 넘기지 않으면 `INCOMPLETE`다.

## 절차

### 1. 방어 공식 형태를 고른다

게임마다 고른다. 장르와 숫자 규모로 고르는 기준은 [references/formula-guide.md](references/formula-guide.md)에 있다. 요약:

| 형태 | `form` | 맞는 경우 |
|---|---|---|
| 고정값 감산 | `flat` | 숫자가 작고 범위가 좁다. 일부러 "방어가 낮으면 못 버티는 구간"을 만든다 |
| 비율 | `ratio` | 성장 폭이 크고 상대가 다양하다. 방어 1의 가치가 일정해 예산을 세우기 쉽다 |
| 레벨 비율 | `level_ratio` | 레벨(구역) 성장이 아주 커서 같은 방어의 효과가 단계마다 줄어야 한다 |
| 직접 퍼센트 | `percent` | 방어 스탯 없이 저항 %만 쓴다. 상한이 필수다 |

사용자가 정하지 않았으면 `ratio`를 제안하고 이유를 한 줄로 말한다. 공식과 상수(k, cap 등)는 기획 판단이므로 `provenance`를 `assumed`로 둔다.

### 2. 스탯 역할을 연결한다

게임마다 스탯 이름이 다르다(`max_hp`, `hp`, `life` …). `combat.stats`에 플레이어와 적 각각 역할(체력·공격·방어·공격 속도·치명 확률·치명 배율) → 그 게임의 스탯 이름을 적는다. 체력과 공격은 필수, 나머지는 선택이다. 없는 역할은 0(방어·치명) 또는 계산 안 함(공격 속도가 없으면 시간 지표를 내지 않는다)으로 둔다.

연결한 이름이 데이터에 없으면 그 역할은 조용히 꺼진다. 비슷한 이름이 데이터에 있으면 `stat_not_found`로 오타를 알리고, 비슷한 이름도 없으면 "값이 있는 데이터가 없는 역할"로 출력한다. 반대로 데이터에 있는데 어느 역할에도 연결하지 않은 스탯도 출력한다. 둘 다 확인한다.

### 3. 단계와 기준 장비를 정한다

단계는 구역·레벨·웨이브·시간 구간 중 그 게임이 난이도를 올리는 단위다. 단계마다 "그 단계에 들어선 평범한 플레이어"를 적는다.

- `base`: 아이템·강화 전 기본 스탯
- `items`, `upgrades`: 그 시점에 흔히 갖춘 아이템과 산 영구 강화의 id (스탯은 원본에서 더한다). 강화한 아이템은 `{"item": id, "enhance": 강화 id, "level": 단계}`로 적으면 [crafting-balance](../crafting-balance/SKILL.md)의 누적 `bonus_pct`만큼 그 아이템 스탯을 키운다
- `enemies` 또는 `zone`: 계산할 적. `zone`을 주면 적 데이터의 `zone`(처음 나오는 구역)이 그 값인 적(삭제 제외)을 모두 쓴다. 앞 구역의 적이 계속 나오는 게임(서바이버라이크 등)은 `"zone_rule": "up_to"`로 그 구역까지 나온 적을 모두 쓴다

기준 장비는 에이전트가 정하면 가정이다. 사용자에게 "이 단계에서 보통 이 정도를 갖췄다"가 맞는지 확인한다. 스탯은 더하기만 한다(곱셈 보너스는 v1에서 지원하지 않는다).

무기 여러 개를 동시에 쓰는 게임(서바이버라이크 등)에서 무기를 모두 기준 장비에 넣으면 피해와 공격 속도가 한 무기처럼 합쳐져 의미 없는 수가 된다. 주무기 하나만 기준 장비에 두고, 보조 무기는 그 무기만 든 단계를 따로 만들어 무기별 처치 시간을 본다. 무기마다 공격을 따로 계산하는 모델은 아직 없다.

### 4. 목표 범위를 정한다

`combat.targets`에 적 등급(일반·정예·보스)별로 지표의 [최소, 최대]를 적는다. 한쪽은 `null`로 비울 수 있다. 예: 일반 적은 처치 1~4타, 버티는 타수 10 이상. 목표는 기획 의도이며 사용자가 정한다. 에이전트가 제안했으면 그렇게 보고한다.

### 5. 계산하고 읽는다

```bash
python3 .claude/skills/studio-data/scripts/studio.py check . --table combat
```

- `target_out_of_range`: 목표를 벗어난 칸. 적 스탯, 기준 장비, 목표 중 무엇을 고칠지는 사용자와 정한다. 의도한 이탈이면 그 단계의 `acknowledged`에 `{"target_out_of_range": "이유"}`를 적는다. 사용자 확인 없이 혼자 적지 않는다.
- `zero_damage`: 피해를 줄 수 없는 조합(고정값 공식에서 방어가 공격보다 큼). 플레이어가 적에게, 적이 플레이어에게 둘 다 본다. 그 행의 타수 목표는 검사할 수 없다.
- `target_unchecked`: 시간 목표를 정했는데 공격 속도가 없어 검사하지 못했다. 통과가 아니다. 공격 속도 역할을 연결하거나 타수 목표로 바꾼다.
- 의도한 이탈을 확인할 때는 적 하나만 덮는 형식 `{"target_out_of_range": {"wraith": "이유"}}`을 먼저 쓴다. 문자열 이유는 그 단계의 그 코드 경고를 모두 덮어, 나중에 생긴 다른 적의 이탈까지 숨긴다.
- `requirement_missing`: 기준 장비의 강화가 선행 조건 없이 들어 있다. 그 단계에서 실제로 살 수 있는 조합으로 고친다.
- 단계가 오를 때 같은 등급의 처치 타수나 버티는 타수가 갑자기 뛰거나 떨어지면, 그 사이의 아이템·강화·적 성장 곡선이 맞지 않는다는 신호다. 경고가 없어도 표로 확인한다.
- 숫자를 손으로 맞춰 목표 안에 넣지 않는다. 바꿨다면 무엇을 왜 바꿨는지와 전·후 표를 함께 남긴다.

### 6. 바꾸고 다시 계산한다

한 번에 하나만 바꾼다(적 스탯, 아이템 스탯, 기준 장비, 공식 상수 중 하나). 여러 개를 함께 바꾸면 어느 변경이 효과를 냈는지 알 수 없다. 계산 결과를 문서에 인용할 때는 `check . --json --out reports/combat.json`으로 저장하고 `[계산: reports/combat.json]`으로 적는다.

## 판 안 성장

[run-growth](../run-growth/SKILL.md)가 레벨업으로 얻는 스탯을 빌드마다 이 계산의 기준 장비에 더해 다시 계산한다. 이 스킬의 목표 범위는 성장 없음 기준이다.

## 스탯 원가 제안

이 공식으로 단계마다 "스탯 1이 공격 1에 비해 얼마나 강해지게 하는가"를 잰다. [stat-budget](../stat-budget/SKILL.md)이 예산 원가를 정할 때 이 값을 제안으로 보여 준다.

## 보고

- 고른 공식 형태와 상수, 그 이유 (가정임을 함께)
- 계산표(`--table`) 또는 목표를 벗어난 행만
- 오류·경고 수, `INCOMPLETE` 여부(함께 검사하지 못한 데이터)
- 가장 큰 불연속 하나와 그것을 고칠 후보(어느 데이터를 바꿀지)
- 사용자가 정해야 할 것: 목표 범위, 의도한 이탈의 확인

## 한계

- 기대값 계산이다. 치명은 확률만큼 섞고, 회피·이동·광역·상태 이상·조작 실력은 없다.
- 플레이어와 적에게 같은 방어 공식을 쓴다.
- 스탯은 더하기만 한다. 퍼센트 보너스와 곱셈 시너지는 아직 없다(강화한 아이템의 `bonus_pct`만 그 아이템 스탯에 곱한다). 런 안의 레벨업은 [run-growth](../run-growth/SKILL.md)가 이 계산에 더한다.
- 무기마다 따로인 공격(무기 여러 개 동시 사용)은 표현하지 못한다. 위 3단계의 대안을 쓴다.
- 비율 공식(`ratio`, `level_ratio`)은 음수 방어를 지원하지 않는다.

예시: `studio-data/assets/sample-project/data/combat.json` (실제 게임 수치가 아니다).
