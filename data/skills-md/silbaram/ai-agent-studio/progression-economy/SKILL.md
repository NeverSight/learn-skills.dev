---
name: progression-economy
description: "Keeps items, permanent upgrades, and enemies in single-source JSON/CSV data, shows them in a read-only local viewer, validates them with deterministic scripts (tier inversions, dominated items, pity expectations, upgrade cost chains, enemy threat progression, cross-file drop-table references), and simulates roguelike meta-progression either with an explicit abstract model or from the combat data (permanent upgrade stats and in-run growth added to the combat calculation per stage, with income and purchase order read from the economy plan). Use when designing, adding, or reviewing items, loot, shops, permanent upgrades, enemies, or progression pacing for action roguelikes and other run-based games in any engine."
---

# 아이템·강화·적 데이터와 성장 경제

액션 로그라이크 같은 런 기반 게임의 아이템, 영구 강화, 적 데이터를 한 곳에서 관리하고 스크립트로 검사한다. 엔진에 묶이지 않도록 데이터는 JSON 또는 CSV로 다룬다. 모든 수치 표기는 [numeric-provenance](../numeric-provenance/SKILL.md)를 따른다.

## 도구

모든 도구는 공용 스킬 [studio-data](../studio-data/SKILL.md)의 `studio.py` 하나로 실행한다. 이 스킬과 함께 설치한다. 아래 명령은 게임 프로젝트 폴더에서 Claude Code 설치 기준(`.claude/skills/…`)으로 적었다. Codex는 `.agents/skills/…`, Windows PowerShell은 `python3` 대신 `py`([실행 경로](../studio-data/SKILL.md#실행)).

| 도구 | 답하는 질문 | 답하지 못하는 질문 |
|---|---|---|
| `studio.py view` | 원본 데이터를 종류별 탭과 묶음(부위·트랙·구역)별 표로 보고, 검사 경고가 난 항목을 바로 찾는다 | (읽기 전용 뷰어. 수정은 원본에서) |
| `studio.py check` (아이템) | 상위 티어가 하위보다 약하지 않은가, 아무도 고르지 않을 열위 아이템이 있는가, 드랍 확률과 천장 기대 시도 수는 얼마인가 | 아이템이 재미있는가, 고유 효과의 실제 가치 |
| `studio.py check` (영구 강화) | 선행 조건이 끊기거나 순환하지 않는가, 다음 단계가 더 싸게 책정되지 않았는가, 트랙별 총비용·power는 얼마인가 | 강화가 체감되는가 |
| `studio.py check` (적) | 구역이 오를수록, 등급(일반 → 정예 → 보스)이 오를수록 위협도가 줄지 않는가, 드랍 테이블이 아이템 데이터에 있는가 | 패턴이 공정한가, 실제 난이도 |
| `studio.py simulate` | 정해 둔 모델에서 몇 번째 런에 강화를 사고 보스를 넘는가, 진척이 멈추는 구간이 있는가 | 실제 조작 난이도, 손맛, 재미 |

점수(아이템)와 위협도(적)는 Σ(스탯 × 가중치)다. 가중치는 설계 가정이고, 같은 묶음 안에서만 비교한다. 아이템을 갖춘 플레이어가 적을 몇 번·몇 초에 잡는지처럼 **요소 사이**를 계산하려면 [combat-balance](../combat-balance/SKILL.md)를 쓴다. 같은 원본 데이터를 그대로 참조한다. 티어·구역을 넘어 곡선으로 비교하거나 새 항목을 곡선에서 만들려면 [stat-budget](../stat-budget/SKILL.md)을 쓴다. `stat_weights`·`threat_weights`는 같은 묶음 안 비교용이고, 예산 원가는 그와 따로 `budget.json`에 둔다. 아이템 강화와 합성, 아이템을 얻는 경로는 [crafting-balance](../crafting-balance/SKILL.md)가, 판 안의 수입과 구매 시점은 [economy-flow](../economy-flow/SKILL.md)가 다룬다. 메타 성장 시뮬레이터는 지는 판까지 포함한 판 수를, economy-flow는 매 판을 끝까지 깬 경우의 최소 판 수를 낸다. 시뮬레이터 결과는 **입력 파라미터가 맞다는 가정 아래의 계산값**이다.

## 단일 원본 규칙

- 아이템, 영구 강화, 적의 수치·효과·의도·상태·출처는 **종류별 원본 파일 한 곳**에만 쓴다. 권장 배치는 `data/items.json`, `data/upgrades.json`, `data/enemies.json`. 형식은 [references/data-format.md](references/data-format.md).
- 시뮬레이터 설정(`data/meta.json`)은 강화 목록을 직접 담지 않고 `"upgrades_file": "upgrades.json"`으로 원본을 가리킨다.
- 기획 문서(md)는 항목을 `id`로만 언급한다. 공격력·가격·체력 같은 수치를 md에 옮겨 적지 않는다. 옮겨 적으면 원본을 고칠 때 어긋난다.
- 보기 좋은 정리가 필요하면 문서를 생성하지 않고 뷰어(`python3 .claude/skills/studio-data/scripts/studio.py view .`)로 원본을 본다. 뷰어 사용법은 [studio-data](../studio-data/SKILL.md#뷰어).

## 항목 추가·변경 요청

"이런 아이템(강화, 적)이 있으면 좋겠어" 같은 요청은 다음 순서로 처리한다.

1. 요청을 해당 원본 파일의 항목으로 바꾼다. `status: "proposed"`, `provenance: {"kind": "assumed", "note": "요청 기반 초안"}`로 넣는다. 수치는 에이전트 제안이므로 가정이다.
2. 숫자로 비교할 수 없는 효과는 `effect`에 적는다(아이템은 `unique_effect: true`도 붙인다). 왜 넣는지 `intent`에 한 줄로 적는다.
3. `python3 .claude/skills/studio-data/scripts/studio.py check data/`로 검사한다. 적의 드랍 테이블 참조까지 확인된다. 경고가 나오면 함께 보고한다.
4. 대화에는 **새로 추가되거나 바뀐 행만** 표로 보여 준다. 전체 목록은 뷰어로 안내한다.
5. 사용자가 승인하면 `approved`로 바꾼다. 거절하면 지우지 말고 `cut`으로 두고 `intent`에 뺀 이유를 남긴다. `cut` 항목은 비교, 합계, 시뮬레이션, 게이트에서 빠진다.
6. 사용자 승인 없이 `approved`로 바꾸지 않는다.

## 작업 순서

1. **데이터를 단일 원본으로 둔다.** 게임이 읽는 JSON/CSV 파일을 도구도 그대로 읽는다.
2. **검사한다.**
   ```bash
   python3 .claude/skills/studio-data/scripts/studio.py check data/ --out reports/data-check.json
   ```
   - 폴더를 주면 아이템·강화·적을 한 번에 검사하고, 적의 드랍 테이블은 함께 읽은 아이템 데이터로 확인한다.
   - 오류(형식, 중복 id, 없는 참조, 순환, 삭제된 선행 조건)는 먼저 고친다.
   - 경고(`tier_inversion`, `dominated`, `cost_inversion`, `power_missing`, `zone_inversion`, `rank_inversion`)는 의도인지 판단한다. 의도가 아니면 고친다. 의도라면 해당 항목의 `acknowledged`에 `{경고 코드: 이유}`를 적는다. 그 경고는 "확인한 경고"로 이유와 함께 따로 보이고 경고 수에서 빠져 새 경고를 가리지 않는다. `intent`는 항목이 왜 있는지 적는 곳이며 경고를 끄지 않는다. 사용자가 확인하지 않은 경고를 에이전트가 혼자 `acknowledged`로 돌리지 않는다.
   - 판정할 수 없는 것(고유 효과 아이템의 티어·열위, 아이템 파일 없이 보거나 아이템 파일을 읽지 못한 적의 드랍 테이블)은 "판정 제외" 또는 "미확인"으로 표시된다. 미확인이 남으면 최종 줄이 PASS가 아니라 INCOMPLETE다. 통과로 보고하지 않는다.
   - 확정 판정 전에는 `--fail-on-assumed`를 붙인다. 삭제되지 않은 항목 중 출처가 가정이거나 비어 있는 것이 있으면 실패한다.
3. **메타 성장을 모델링한다.** 모델과 파라미터는 [references/meta-model.md](references/meta-model.md).
   ```bash
   python3 .claude/skills/studio-data/scripts/studio.py simulate data/meta.json --out reports/meta.json --csv reports/meta-curve.csv
   ```
   강화 데이터에 오류가 있거나 활성 강화에 `power`가 없으면 시뮬레이터가 실행을 거부한다. 구매 정책을 비교할 때는 설정 파일을 복사하지 않고 `--compare-policies`를 붙인다.
   전투 계산(`data/combat.json`)이 있으면 추상 "힘" 대신 **전투 계산 모델**(`"model": "combat"`)을 쓴다. 영구 강화의 `stats`와 판 안 성장의 레벨업을 전투 계산에 더해 단계마다 생존을 정하고, 수입·구매 순서를 재화 흐름에서 읽을 수 있다([meta-model](references/meta-model.md#전투-계산-모델)).
   ```bash
   python3 .claude/skills/studio-data/scripts/studio.py simulate data/meta.json --compare-policies --out reports/meta-policies.json
   ```
4. **결과를 문서에 출처와 함께 적는다.** 결과값은 `[계산: reports/meta.json]`처럼 저장한 파일을 출처로 쓴다. 데이터 파일의 수치는 md 태그 대신 각 항목의 `provenance` 필드로 표시한다.
5. **한 번에 하나만 바꾸고 다시 돌린다.** 같은 seed·trials·max_runs로 비교한다. 여러 값을 한꺼번에 바꾸면 어느 변경이 효과를 냈는지 알 수 없다.
6. **플레이 기록이 생기면 보정한다.** 전투 계산 모델은 `calibrate`가 기록의 단계 통과율과 비교해 `slope`·`even_margin`을 제안한다([playtest-verdict](../playtest-verdict/references/calibration.md)). 추상 모델은 실제 런의 도달 방 분포와 `survival_at_base_power`, 마일스톤 분포를 손으로 비교해 `survival.slope`와 `player.skill`을 맞춘다. 보정 근거가 된 파라미터만 `[측정: 기록 출처]`로 올린다.

## 판정 규칙

- 검사기와 시뮬레이터 결과만으로 "난이도 적절", "재미있음"을 판정하지 않는다. 구조적 문제(역전, 끊긴 사슬, 너무 이른 완료, 긴 정체, 도달 불가)를 찾는 데 쓴다.
- 도달률이 100%가 아닌 마일스톤은 중앙값만 보고하지 않는다. `reached_fraction`과 "미도달"을 함께 적는다.
- 구매 정책(`listed_order` / `cheapest_first`)에 따라 결론이 달라지면, 그것 자체를 발견으로 보고한다. 한쪽만 골라 보고하지 않는다. 두 정책은 `--compare-policies`로 한 번에 돌린다.
- 숫자를 손으로 조정해 원하는 결과가 나오게 맞추지 않는다. 조정했다면 무엇을 왜 바꿨는지와 바꾸기 전·후 결과를 함께 남긴다.

## 보고

- 실행한 명령, seed, trials, 설정 파일 해시(`config_sha256`)와 강화 파일 해시(`upgrades_file.sha256`)
- 오류·경고 개수와 의도된 예외의 근거
- 마일스톤과 강화별 도달률, p10 / 중앙값 / p90 런
- 가장 큰 구조적 위험 하나와 그것을 확인할 가장 싼 다음 실험
- 결과가 기대는 `[가정]` 입력 목록

예시 데이터는 `studio-data/assets/sample-project/data/`에 있으며 실제 게임 수치가 아니다.
