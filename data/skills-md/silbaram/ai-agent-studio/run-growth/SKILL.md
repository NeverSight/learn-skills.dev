---
name: run-growth
description: "Models in-run growth: level-up choices with stat gains and pick limits, choices offered at random each level, and build policies (priority or spread) that decide what a player takes. Runs a seeded simulation to get each build's expected stats at each combat stage, adds them to the combat calculation, and compares builds by hits to kill and to survive, warning when one build is at least as good everywhere. Use when designing level-up perks, cards, or upgrade choices, checking that builds are distinct, or seeing how in-run growth changes difficulty, in any genre and engine."
---

# 판 안 성장: 레벨업 선택과 빌드

판 안에서 레벨업할 때 고르는 선택지(카드·특성·강화)를 데이터로 두고, "어떤 빌드로 고르면 단계마다 얼마나 강해지나"를 계산한다. 그 스탯을 [combat-balance](../combat-balance/SKILL.md)의 전투 계산에 더해 빌드끼리 처치·버팀을 나란히 비교한다. 목적은 "한 빌드가 모든 상황에서 낫다", "어떤 선택지는 아무도 안 고른다"를 감 대신 계산으로 찾는 것이다.

- 레벨업마다 선택지 중 몇 개(`offers`)가 무작위로 제시되고, 빌드 정책대로 하나를 고른다고 본다.
- 시드를 고정한 반복 시뮬레이션의 평균이다. 같은 설정이면 결과가 같다. 전투는 시행마다 계산해 평균한다.
- 재미나 실제 난이도를 판정하지 않는다. 기대값 계산이며 플레이어의 실력·이동·회피는 없다.

## 도구

공용 스킬 [studio-data](../studio-data/SKILL.md)의 `studio.py`로 한다. 이 스킬과 함께 설치한다. 명령은 게임 프로젝트 폴더에서 Claude Code 설치 기준으로 적었다. Codex는 `.agents/skills/…`, Windows PowerShell은 `python3` 대신 `py`([실행 경로](../studio-data/SKILL.md#실행)).

| 명령 | 하는 일 |
|---|---|
| `python3 .claude/skills/studio-data/scripts/studio.py check .` | 형식·참조 검사, 빌드별 단계마다 얻는 스탯, 전투 계산에 더한 처치·버팀, 밀리는 빌드 경고 |
| `… check . --table growth` | 빌드 비교표(마크다운): 성장 없음과 빌드별 처치·버팀 |
| `… view .` | 판 안 성장 탭: 빌드별 성장, 빌드 비교표 |

데이터는 `data/growth.json` 한 파일이다. 형식은 [references/growth-format.md](references/growth-format.md). 전투 계산(`data/combat.json`)과 그 참조 데이터를 그대로 쓴다. 프로젝트 폴더(`check .`)로 검사해야 계산한다. 전투 계산이 없거나 그 검사에 오류·미확인이 있으면 `INCOMPLETE`다.

## 절차

### 1. 단계별 레벨을 정한다

`growth.level_at`에 전투 계산의 단계마다 "그 단계에 들어설 때 보통 몇 레벨인가"를 적는다. 전투 계산의 단계가 "그 단계에 들어선 평범한 플레이어"이므로 같은 시점으로 맞춘다(첫 단계는 보통 1). 레벨 1에서 시작해 그 레벨까지 레벨업한다. 이 값은 경험치 곡선과 적 수에서 나오는 추정이라 처음에는 가정이다. 플레이 기록이 있으면 그 값으로 바꾼다. 전투 계산의 단계를 빼먹으면 `level_missing`이고, 일부러 뺄 단계는 `null`로 적는다.

### 2. 선택지를 적는다

`choices`마다 오르는 스탯(`stats`, 플레이어 스탯 이름 그대로)과 최대 선택 횟수(`max_picks`, 없으면 무제한)를 적는다. 레벨업마다 제시하는 개수는 `offers`다. 고르면 아이템을 얻는 선택지는 `item`(아이템 id)으로 적으면 그 아이템의 스탯을 원본에서 가져온다(스탯을 옮겨 적지 않는다).

### 3. 빌드를 적는다

빌드는 "플레이어가 어떻게 고르나"다. 전형적인 플레이 방식을 두세 가지 적는다.

- `priority`: 원하는 선택지를 순서대로. 제시된 것 중 가장 앞의 것을 고른다(최대 횟수에 닿은 것은 건너뜀).
- `pick: "spread"`: 목록 중 지금까지 가장 적게 고른 것을 고른다(고르게 키우는 빌드).
- 원하는 것이 하나도 제시되지 않으면 제시된 것 중 첫째를 고른다.
- 경험치·수집 선택지로 레벨을 빨리 올리는 빌드는 그 빌드의 `level_at`에 가정한 레벨을 적는다. 적지 않으면 모든 빌드가 같은 레벨로 계산된다.

### 4. 계산하고 읽는다

```bash
python3 .claude/skills/studio-data/scripts/studio.py check . --table growth
```

- `build_dominated`: 한 빌드가 다른 빌드보다 전투 계산상 모든 단계·적·지표에서 같거나 낫다. 선택지 수치를 바꾸거나 빌드 정의를 확인한다. 진 빌드가 전투 밖 선택지(줍기·이동·경험치)를 골랐다면 그 가치는 계산에 없다. 그 선택지의 `stat_not_in_combat`을 확인하면 경고 대신 "전투 계산상 밀림"으로 보이고, 전투 밖 가치는 사용자와 따로 판단한다. 의도라면 그 빌드의 `acknowledged`에 적는다.
- 어느 빌드도 고르지 않은 선택지가 출력되면 그 선택지가 약하거나 빌드 정의에 빠져 있다.
- `stat_not_in_combat`: 선택지 스탯을 전투 계산이 쓰지 않는다. 오타면 고치고, 이동 속도처럼 전투 밖 효과면 그 선택지의 `acknowledged`에 적는다.
- `build_invalid`: 성장이 쌓이면 스탯이 계산에 쓸 수 없는 값이 된다(치명 확률이 1을 넘는 등). `max_picks`나 수치를 고친다.
- 성장 없음과 빌드별 숫자의 차이가 판 안 성장의 크기다. 성장이 너무 커서 후반 적이 한두 대에 죽거나, 너무 작아 레벨업이 체감되지 않는지 본다. 전투 계산의 목표 범위(성장 없음 기준)와 함께 본다.
- 숫자를 손으로 맞춰 경고를 없애지 않는다. 한 번에 하나만 바꾸고 전·후 표를 남긴다.

## 보고

- 빌드별 단계마다 얻는 스탯, 성장 없음 대비 처치·버팀 변화
- 밀리는 빌드와 이기는 빌드, 아무도 고르지 않는 선택지
- 오류·경고 수, `INCOMPLETE` 여부, 시행 수와 seed
- 사용자가 정해야 할 것: 단계별 레벨, 빌드 정의, 밀리는 빌드를 살릴지

## 한계

- 스탯은 더하기만 한다. 곱셈 보너스와 선택지끼리의 시너지는 없다. 아이템을 주는 선택지는 그 아이템 스탯을 더할 뿐이라, 무기를 하나 더 얻는 선택지는 전투 계산의 한계(무기마다 따로인 공격이 없다)를 그대로 따른다.
- 빌드는 정해진 규칙으로 고른다. 상황을 보고 바꾸는 플레이어는 모델에 없다.
- 단계별 레벨은 입력이다. 경험치 곡선에서 레벨을 계산하지 않는다. 경험치·수집 선택지의 가치는 모른다(빌드의 `level_at`에 가정으로 적는 것까지만).
- 메타 성장 시뮬레이터의 전투 계산 모델(`simulate`, `"model": "combat"`)은 빌드 하나를 골라 판마다 레벨업을 새로 뽑아 영구 강화와 함께 계산한다([meta-model](../progression-economy/references/meta-model.md#전투-계산-모델)). 이 스킬은 영구 강화 없는 한 판의 빌드 비교다.

예시: `studio-data/assets/sample-project/data/growth.json` (실제 게임 수치가 아니다).
