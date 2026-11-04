---
name: crafting-balance
description: "Models item enhancement (cost, success rate, and keep/downgrade/destroy on failure per level) and synthesis (fixed recipes and random merges that combine matching items into one of a matching set), computes the expected cost and attempts to reach each level, the value ratio of each recipe against stat budgets, and the expected crafts to get one specific result, and finds item-multiplication loops and items no drop, recipe, or declared source can produce. Use when designing or reviewing upgrade systems, crafting, merging, salvage, or item acquisition paths in any genre and engine."
---

# 강화·합성

아이템 강화(+1, +2 …)와 합성(재료로 만들기, 같은 등급끼리 합치기, 분해)을 데이터로 두고 기대값을 계산한다. 목적은 "강화 +5까지 평균 얼마가 드나", "이 합성은 재료보다 좋은 걸 주나", "합성을 돌면 아이템이 불어나지 않나", "이 아이템은 어디서 얻나"를 감 대신 계산으로 답하는 것이다.

계산은 **기대값**이다. 실제 체감(운이 나쁜 사람의 고통, 천장 필요성)이나 재미를 판정하지 않는다. 분산이 큰 구간은 표를 보고 사람이 판단한다.

## 도구

공용 스킬 [studio-data](../studio-data/SKILL.md)의 `studio.py`로 한다. 이 스킬과 함께 설치한다. 명령은 게임 프로젝트 폴더에서 Claude Code 설치 기준으로 적었다. Codex는 `.agents/skills/…`, Windows PowerShell은 `python3` 대신 `py`([실행 경로](../studio-data/SKILL.md#실행)).

| 명령 | 하는 일 |
|---|---|
| `python3 .claude/skills/studio-data/scripts/studio.py check .` | 형식·참조 검사, 강화 단계별 기대 비용·시도, 합성 가치 비율, 증식 고리, 얻을 수 없는 아이템 |
| `… check . --table crafting` | 강화 표와 합성 표(마크다운) |
| `… view .` | 강화·합성 탭: 강화 단계표, 합성 표(손해 보는 합성 강조), 얻을 수 없는 아이템 |

데이터는 `data/crafting.json` 한 파일이다. 형식은 [references/crafting-format.md](references/crafting-format.md). 아이템과 드랍 테이블은 [progression-economy](../progression-economy/SKILL.md)의 원본을, 가치는 [stat-budget](../stat-budget/SKILL.md)의 원가를 그대로 쓴다. 프로젝트 폴더(`check .`)로 검사해야 참조와 획득 경로를 확인한다. 아이템 데이터가 없으면 `INCOMPLETE`다. 스탯 예산이 없으면 가치 비교를 하지 못해 역시 `INCOMPLETE`다. 가치 비교를 쓰지 않는 게임이면 `crafting.value_check: false`로 끈다.

## 절차

### 1. 강화 단계를 적는다

강화 대상(`applies_to` 조건이나 `items` 목록)마다 단계를 순서대로 적는다.

- `cost`: 한 번 시도하는 비용. 재화 단위는 게임마다 정한다.
- `success`: 성공 확률(기본 1).
- `on_fail`: 실패하면 `keep`(그대로) / `down`(한 단계 하락) / `destroy`(파괴). 파괴가 있으면 `replace_cost`(같은 아이템을 다시 구하는 비용)를 적는다.
- `bonus_pct`: 그 단계에서 오르는 기본 스탯 비율(0.1이면 기본 스탯의 십분의 일). 누적된다.

`check`가 0단계에서 각 단계까지의 **기대 비용과 기대 시도 수**를 낸다. 하락·파괴가 있으면 뒤 단계 비용이 급격히 늘어난다. 이 곡선이 의도와 맞는지 사용자와 본다.

스탯 예산이 있으면 **최고 단계까지 강화한 아이템이 다음 티어의 기대 예산을 넘는지** 본다(`enhance_overtakes_tier`). 강화한 낮은 티어가 새 티어보다 세면 새 아이템을 주울 이유가 사라진다. 의도라면 그 강화의 `acknowledged`에 적는다.

### 2. 합성을 적는다

| 형태 | 적는 법 | 예 |
|---|---|---|
| 레시피 | 재료와 결과를 `item` id로 | 녹슨 검 1 + 숫돌 2 → 철검 |
| 무작위 합성 | 재료나 결과를 `match` 조건으로 | 1티어 무기 아무거나 2개 → 2티어 무기 중 하나 |
| 분해 | 재료 하나, 결과 여러 개 | 쌍단검 1 → 숫돌 3 |

`check`가 내는 것:

- **가치 비율** = 결과 예산 × 성공률 ÷ 재료 예산. "아무거나" 재료는 가장 싼 것으로, 무작위 결과는 평균으로 잰다. 고유 효과 아이템이 끼면 비교하지 않는다. 허용 오차 아래로 낮으면 `recipe_loses_value`. 분해처럼 일부러 손해인 합성은 그 합성의 `acknowledged`에 이유를 적는다.
- **무작위 결과**: 결과 가짓수와, 특정 아이템 하나를 얻기까지의 기대 합성 횟수·재료 수. "원하는 걸 얻으려면 평균 몇 번 돌려야 하나"를 보여 준다.
- **증식 고리**(`value_loop`, 오류): 합성을 돌아 처음 아이템으로 오면 수가 늘어나는 고리. 예: 철검 1 → 녹슨 검 3, 녹슨 검 2 → 철검 1. 무작위 합성을 거치는 고리(1티어 둘 → 2티어 무작위 하나 → 분해해 1티어 셋)도 기대 수율로 찾는다. 재료가 한 종류인 변환만 본다.

### 3. 얻는 경로를 확인한다

드랍 테이블(아이템 id나 희귀도), 합성 결과(재료를 모두 얻을 수 있을 때), `crafting.other_sources`(시작 장비, 상점, 퀘스트 등), [run-growth](../run-growth/SKILL.md)의 아이템을 주는 레벨업 선택지로 얻을 수 있는 아이템을 모은다. 어디에도 없는 활성 아이템은 `unobtainable`로 알린다. 얻는 곳이 있는데 데이터 밖이면(상점 등) `other_sources`에 적는다. 일부러 얻는 곳이 없는 아이템(시즌 보상 등)은 그 아이템의 `acknowledged`에 이유를 적는다.

### 4. 바꾸고 다시 계산한다

한 번에 하나만 바꾼다(성공률, 비용, 수량, 보너스 중 하나). 숫자를 손으로 맞춰 경고를 없애지 않는다. 바꿨다면 무엇을 왜 바꿨는지와 전·후 표를 남긴다. 강화·합성 수치는 기획 판단이라 처음에는 `provenance`가 `assumed`다.

## 다른 스킬과의 연결

[economy-flow](../economy-flow/SKILL.md)가 강화 기대 비용과 합성 비용을 구매 가격으로 가져와 언제 살 수 있는지 계산한다.

## 보고

- 강화 대상별 최고 단계까지의 기대 비용·기대 시도, 비용이 급격히 늘어나는 단계
- 합성별 가치 비율, 무작위 합성의 특정 결과까지 기대 횟수
- 오류(증식 고리, 없는 참조)와 경고(손해 보는 합성, 상위 티어를 넘는 강화, 얻을 수 없는 아이템)
- `INCOMPLETE` 여부, 스탯 예산이 없어 가치 비교를 하지 않았는지
- 사용자가 정해야 할 것: 강화 곡선의 의도, 손해를 감수할 합성, 얻는 경로가 없는 아이템의 처리

## 한계

- 기대값만 낸다. 분산(운이 나쁜 쪽 플레이어가 얼마나 더 쓰는지)과 천장은 아직 계산하지 않는다.
- 가치는 스탯 예산의 선형 합이다. 고유 효과 아이템의 가치는 모른다.
- 증식 고리는 재료가 한 종류인 변환만 본다. 여러 재료가 드는 합성의 고리는 다른 재료의 비용까지 따져야 한다. 무작위 합성이 두 번 이상 겹친 고리는 결과마다 다음 무작위 합성을 평균하지 않고 고정 변환만 따라간다.
- 무작위 합성의 결과는 조건에 맞는 아이템 중 균등하게 하나로 본다(가중치 없음).

예시: `studio-data/assets/sample-project/data/crafting.json` (실제 게임 수치가 아니다).
