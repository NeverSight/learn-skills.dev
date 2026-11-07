---
name: level-design
description: "Lays out each level as an ordered list of encounters (rooms, waves, packs), scores every encounter's threat from the same enemy stats used by combat and stat budgets, compares it with a threat budget curve per stage and role, and cross-checks placed enemies against combat stages and kill counts against the economy. Use when composing levels, waves or rooms, sizing encounters, or checking that a level agrees with combat and economy assumptions, in any genre and engine."
---

# 레벨 구성

레벨을 조우의 순서로 적고, 조우마다 위협도가 의도한 크기인지 계산으로 본다. 목적은 "이 방은 앞 방보다 얼마나 센가", "이 구역의 보스 방은 예산 안인가", "레벨에 놓은 적이 전투 계산과 재화 흐름의 가정과 같은가"를 감 대신 계산으로 답하는 것이다.

조우는 그 게임이 플레이어를 적과 맞붙이는 단위다. 방, 웨이브, 무리, 시간 구간 어느 것이든 된다.

위협도는 스탯으로 낸 **설계 가정**이다. 적을 더한 값이므로 적의 조합, 지형, 동시에 몰리는 정도는 반영하지 않는다. 실제 난이도나 재미를 판정하지 않는다.

## 도구

공용 스킬 [studio-data](../studio-data/SKILL.md)의 `studio.py`로 한다. 이 스킬과 함께 설치한다. 명령은 게임 프로젝트 폴더에서 Claude Code 설치 기준으로 적었다. Codex는 `.agents/skills/…`, Windows PowerShell은 `python3` 대신 `py`([실행 경로](../studio-data/SKILL.md#실행)).

| 명령 | 하는 일 |
|---|---|
| `python3 .claude/skills/studio-data/scripts/studio.py check .` | 형식·참조 검사, 조우의 위협도와 예산, 전투 단계의 적, 재화 흐름의 처치 수 |
| `… check . --table levels` | 조우 표(마크다운) |
| `… view .` | 레벨 구성 탭: 레벨별 조우, 위협도와 예산 범위 |

데이터는 `data/levels.json` 한 파일이다. 형식은 [references/levels-format.md](references/levels-format.md). 적은 [progression-economy](../progression-economy/SKILL.md)의 원본에서, 위협도의 가중치는 [stat-budget](../stat-budget/SKILL.md)의 적 원가에서(없으면 `threat_weights`), 단계는 [combat-balance](../combat-balance/SKILL.md)에서 가져온다. 프로젝트 폴더(`check .`)로 검사해야 참조를 확인한다. 적이나 전투 계산을 함께 넘기지 않으면 `INCOMPLETE`다.

## 절차

### 1. 레벨을 전투 단계에 잇는다

레벨은 플레이어가 지나가는 한 덩어리다. 구역, 스테이지, 맵이 여기에 해당한다. 전투 계산의 단계와 id가 다르면 `combat_stage`에 그 단계를 적는다. 한 단계에 레벨이 여럿이면 한 판에 모두 지나는 것으로 센다. 대체 맵(한 판에 그중 하나만 나옴)은 조우의 `repeat`를 나오는 확률로 나눠 적는다. 레벨이 없는 전투 단계가 남으면 `INCOMPLETE`다.

### 2. 예산을 정한다

조우를 하나씩 감으로 채우기 전에 `threat_budget`을 정한다.

- `curve`: 단계가 오를수록 평범한 조우가 얼마나 세지는가. 전투 단계의 순서(1부터)를 기준으로 읽는다. 스탯 예산과 같은 `linear`, `exponential`을 쓰고, `table`이면 단계 id별 값을 적는다.
- `roles`: 조우의 역할과 배수. 예를 들어 평범한 방 1, 정예 방 1.2, 쉬어 가는 방 0.5. 역할 이름은 게임마다 정한다.
- `tolerance`: 허용 오차(기본 0.2).

처음에는 지금 적으로 "평범한 조우" 하나를 만들어 위협도를 재고, 그 값을 곡선의 시작점으로 삼는다. 이 값은 가정이다. 사용자에게 확인한다.

### 3. 조우를 놓는다

판에서 지나는 순서대로 `encounters`에 적는다.

- `enemies`: 한 번 만날 때 나오는 적 `{id: 수}`. 무작위로 나오면 평균을 소수로 적는다.
- `repeat`: 한 판에서 평범하게 이 조우를 만나는 횟수(기본 1). 무작위 방은 평균을 적는다. 위협도에는 곱하지 않고 처치 수와 한 판 위협도에만 곱한다.
- `role`: 예산의 역할.
- `intent`: 이 조우가 플레이어에게 무엇을 시험하는가. 수치로 설명되지 않는 의도를 남긴다.

### 4. 계산하고 읽는다

```bash
python3 .claude/skills/studio-data/scripts/studio.py check . --table levels
```

- `over_budget`·`under_budget`: 조우의 위협도가 곡선 × 역할 배수에서 허용 오차를 넘게 벗어났다. 의도한 조우면 역할을 바꾸거나 이유를 `acknowledged`에 적는다.
- `enemy_not_in_stage`: 전투 계산이 그 단계에서 재지 않는 적을 놓았다. 앞 구역의 적이 계속 나오는 게임이면 전투 단계에 `zone_rule: "up_to"`를 적는다.
- `enemy_unplaced`: 전투 계산은 세는데 어떤 조우에도 없는 적이다. 조우 밖에서만 나오는 적이면 그 단계의 레벨 하나의 `acknowledged`에 이유를 적는다.
- `kills_differ`: 조우로 센 처치 수(적 수 × 횟수)가 재화 흐름의 처치 가정과 허용 오차를 넘게 다르다. 어느 쪽이 맞는지 사용자와 정해 한쪽을 고친다.
- `kills_not_linked`: 재화 흐름의 처치 수가 어떤 레벨과도 이어지지 않아 비교하지 못했다. 재화 흐름 단계에 `combat_stage`를 적거나 전투 단계와 같은 id로 둔다.
- 숫자를 손으로 맞춰 경고를 없애지 않는다. 한 번에 하나만 바꾸고 전·후 표를 남긴다.

## 보고

- 레벨별 조우 표: 역할, 횟수, 구성, 위협도, 예산 범위
- 예산을 벗어난 조우와 이유
- 전투 단계·재화 흐름과 어긋난 적과 처치 수
- 오류·경고 수, `INCOMPLETE` 여부
- 사용자가 정해야 할 것: 곡선, 역할 배수, 조우의 구성과 횟수

## 한계

- 위협도는 적의 합이다. 조합의 시너지, 지형, 등장 간격은 넣지 않는다.
- 쉬는 곳과 보상의 배치, 조우 사이의 흐름은 아직 보지 않는다.
- 재화 흐름 단계에 처치 수가 없으면 그 단계는 맞춰 보지 않는다.

예시: `studio-data/assets/sample-project/data/levels.json` (실제 게임 수치가 아니다).
