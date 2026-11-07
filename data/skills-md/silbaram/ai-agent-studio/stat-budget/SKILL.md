---
name: stat-budget
description: "Sets stat budget curves per tier, zone, or level with per-stat costs and multipliers (rank, rarity, slot), checks every item and enemy against its expected budget, drafts new items and enemies from archetypes that split the budget across stats, and suggests stat costs from the combat formula. Use when designing tier or zone progression, adding items or enemies so they fit a curve, finding over- or under-budget entries, or deciding how much one stat point is worth, in any genre and engine."
---

# 스탯 예산: 곡선에서 표로

아이템과 적의 수치를 하나씩 감으로 정하지 않는다. 티어·구역마다 "스탯 예산 총량"이 어떻게 오르는지 곡선으로 정하고, 원형(아키타입)으로 그 예산을 스탯에 나눠 표를 만든다. 이미 있는 항목은 곡선과 비교해 넘치거나 모자란 것을 찾는다.

- **예산** = Σ(스탯 × 스탯 원가). 원가는 "그 스탯 1이 예산 몇 점인가"다.
- **기대 예산** = 곡선(기준 값) × 배수(등급·희귀도·부위 등).
- 재미나 실제 난이도를 판정하지 않는다. 곡선과 원가는 기획 가정이며, 결과는 그 가정 아래의 계산이다.

## 도구

공용 스킬 [studio-data](../studio-data/SKILL.md)의 `studio.py`로 한다. 이 스킬과 함께 설치한다. 명령은 게임 프로젝트 폴더에서 Claude Code 설치 기준으로 적었다. Codex는 `.agents/skills/…`, Windows PowerShell은 `python3` 대신 `py`([실행 경로](../studio-data/SKILL.md#실행)).

| 명령 | 하는 일 |
|---|---|
| `python3 .claude/skills/studio-data/scripts/studio.py check .` | 곡선·원가·원형 형식 검사, 모든 아이템·적의 예산 비교(넘침·모자람), 원가 제안 |
| `… check . --table budget` | 항목별 예산 비교표(마크다운) |
| `… draft . --archetype <원형> --at <기준 값> [--set 필드=값] [--id 새_id]` | 곡선과 원형으로 초안 하나를 JSON으로 출력. **파일에 쓰지 않는다** |
| `… view .` | 스탯 예산 탭: 원가와 제안, 곡선의 기대 예산, 비교표(넘침·모자람 강조), 원형 |

데이터는 `data/budget.json` 한 파일이다. 형식은 [references/budget-format.md](references/budget-format.md). 아이템·적은 [progression-economy](../progression-economy/SKILL.md)의 원본을 그대로 읽는다. 프로젝트 폴더(`check .`)로 검사해야 비교한다. 함께 넘기지 않으면 그쪽은 `INCOMPLETE`다.

## 절차

### 1. 원가를 정한다

쪽(아이템·적)마다 스탯 원가를 정한다. 기준 스탯 하나(보통 공격)를 1로 두고 나머지를 그에 맞춘다.

- [combat-balance](../combat-balance/SKILL.md)의 `data/combat.json`이 있으면 `check`가 **원가 제안**을 보여 준다. 전투 공식으로 단계마다 "그 스탯 1이 공격 1에 비해 얼마나 강해지게 하는가"를 잰 값이다. 단계마다 다르다(방어는 적이 셀수록 값어치가 오르는 식).
- 제안은 자동으로 적용하지 않는다. 기획자가 정한 원가와 크게 다르면 사용자에게 보여 주고 어느 쪽을 쓸지 묻는다.
- 전투 공식에 없는 스탯(이동 속도, 획득 반경 등)은 제안이 없다. 사용자와 정한다.
- 전투 계산에 오류가 있거나 기준 장비를 계산하지 못한 단계는 제안이 빠진다. 빠진 단계와 이유는 "원가 제안 미확인" 줄로 나온다.
- 이 원가가 아이템·적 데이터의 "예산"의 원본이다. `budget.json`이 있으면 아이템 검사(티어 역전·열위)와 적 검사(위협도)도 `stat_weights`·`threat_weights` 대신 이 원가를 쓴다. 두 값을 따로 적어 두면 판정이 엇갈리므로, 비율이 다르면 `weights_ignored`로 알린다. 옛 가중치는 지우거나 같은 비율로 맞춘다.

### 2. 곡선을 정한다

- `by`: 곡선의 기준이 되는 필드(아이템은 보통 `tier`, 적은 `zone`·`level`).
- `growth`: `linear`(일정하게 증가), `exponential`(비율로 증가), `table`(값을 직접 적음).
- `multiplier`: 같은 기준 안에서 크기를 나누는 필드와 배수(적의 `rank`: 일반 1 · 정예 2.7 · 보스 8.5, 아이템의 `slot`이나 `rarity`).
- `tolerance`: 허용 오차 비율(기본 0.2).

처음 곡선은 지금 데이터에서 시작하면 좋다. `check --table`의 예산 열을 보고, 곡선이 대부분의 항목을 지나도록 잡은 뒤, 벗어난 항목을 고칠지 곡선을 고칠지 사용자와 정한다.

### 3. 벗어난 항목을 읽는다

- `over_budget` / `under_budget`: 기대 예산의 허용 범위를 벗어났다. 의도한 예외(초반 함정 아이템, 특수한 정예)면 **그 항목의** `acknowledged`에 `{"over_budget": "이유"}`를 적는다. 사용자 확인 없이 혼자 적지 않는다.
- `stat_without_cost`: 원가가 없는 스탯이 있어 비교하지 못했다. 원가를 정하거나, 예산 밖 효과라면 그 항목에 `unique_effect: true`를 붙인다.
- `unique_effect` 아이템은 비교에서 빠진다("판정 제외").
- 숫자를 손으로 맞춰 곡선 안에 넣지 않는다. 바꿨다면 무엇을 왜 바꿨는지와 전·후 비율을 남긴다.

### 4. 새 항목은 초안에서 시작한다

"티어 3 무기 하나", "구역 4 정예 탱커 하나" 같은 요청은 `draft`로 시작한다.

```bash
python3 .claude/skills/studio-data/scripts/studio.py draft . --archetype quick_blade --at 3 --id gale_blade
python3 .claude/skills/studio-data/scripts/studio.py draft . --archetype tank --at 4 --set rank=elite --id frost_warden
```

1. 출력된 JSON을 해당 원본 파일(`items.json`, `enemies.json`)에 넣는다. `status`는 `proposed`, `provenance`는 `computed`(출처 `data/budget.json#원형`)다. 이 값이 기대는 곡선과 원가는 가정이라는 사실을 보고에 함께 적는다.
2. 이름, 효과, 의도(`intent`)를 채우고, 원형에 없는 필드(희귀도 등)를 정한다.
3. `check .`로 예산 비교와 다른 검사(티어 역전, 위협도, 전투 계산)를 함께 본다.
4. 대화에는 새 행만 보여 주고, 승인은 사용자가 한다.

원형에 맞는 것이 없으면 `archetypes`에 새 원형을 제안한다. 원형도 기획 판단이라 `provenance`는 `assumed`다.

## 다른 스킬과의 연결

[crafting-balance](../crafting-balance/SKILL.md)가 이 원가로 합성의 가치 비율과 강화한 아이템이 다음 티어를 넘는지 계산한다.

## 보고

- 곡선(기준, 형태, 값)과 원가, 그 출처 (가정임을 함께)
- 벗어난 항목 목록과 비율, 원가 제안과 기획 원가의 큰 차이
- 초안을 만들었다면 그 행과 기대 예산
- 오류·경고 수, `INCOMPLETE` 여부
- 사용자가 정해야 할 것: 곡선과 배수, 원가, 벗어난 항목의 처리

## 한계

- 예산은 스탯의 선형 합이다. 스탯끼리의 시너지(치명 확률 × 치명 배율 등)는 원가 제안에만 반영되고 예산 합에는 없다.
- 원가 제안은 전투 계산의 기대값 모델에서 잰다. 회피·이동·광역 같은 효과의 값어치는 모른다.
- 영구 강화는 비교하지 않는다(비용 사슬은 progression-economy가 검사한다).

예시: `studio-data/assets/sample-project/data/budget.json` (실제 게임 수치가 아니다).
