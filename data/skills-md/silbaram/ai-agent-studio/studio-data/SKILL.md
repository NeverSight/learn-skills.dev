---
name: studio-data
description: "Shared tooling for the game-design skills: one entry script (studio.py) and one Python package that validate concept records, items, permanent upgrades, enemies, combat calculations, in-run growth builds, stat budgets, enhancement and crafting, currency flow, and playtest records, draft items and enemies from budget curves, simulate roguelike meta-progression, check numeric provenance tags in design docs, serve a read-only browser viewer that shows all of a project's design data with validation results, and install a read-only judge agent and data-check hooks for Claude Code. Use when viewing, checking, or simulating game design data, when setting up Claude Code hooks for a game project, or when another skill in this repository tells you to run a check."
---

# 게임 설계 데이터 공용 도구

다른 스킬([concept-exploration](../concept-exploration/SKILL.md), [progression-economy](../progression-economy/SKILL.md), [numeric-provenance](../numeric-provenance/SKILL.md), [combat-balance](../combat-balance/SKILL.md), [run-growth](../run-growth/SKILL.md), [stat-budget](../stat-budget/SKILL.md), [crafting-balance](../crafting-balance/SKILL.md), [economy-flow](../economy-flow/SKILL.md), [level-design](../level-design/SKILL.md), [playtest-verdict](../playtest-verdict/SKILL.md))은 절차만 담고, 실행하는 도구는 모두 이 스킬에 있다. 이 스킬을 다른 스킬과 같은 부모 폴더에 함께 설치한다.

## 실행

실행 파일은 `scripts/studio.py` 하나다. Python 3.9 이상, 추가 설치는 필요 없다. **게임 프로젝트 폴더에서** 설치 위치의 경로로 실행한다.

| 설치 | 실행 파일 경로 (게임 프로젝트 기준) |
|---|---|
| Claude Code | `.claude/skills/studio-data/scripts/studio.py` |
| Codex | `.agents/skills/studio-data/scripts/studio.py` |
| 이 저장소에서 직접 | `skills/studio-data/scripts/studio.py` |

- 어느 경우든 이 SKILL.md가 있는 폴더의 `scripts/studio.py`다. 다른 스킬 문서 기준으로는 `../studio-data/scripts/studio.py`.
- 모든 스킬 문서의 명령은 Claude Code 설치 기준(`.claude/skills/…`)으로 적는다. Codex는 `.agents/skills/…`로 바꾼다.
- Python 명령은 `python3`로 적는다. Windows PowerShell에서는 `py`를 쓴다. `python`만 있는 환경이면 `python`.

| 명령 | 하는 일 |
|---|---|
| `python3 .claude/skills/studio-data/scripts/studio.py view .` | 프로젝트의 설계 데이터를 브라우저에서 본다 (읽기 전용, 자동 갱신) |
| `python3 .claude/skills/studio-data/scripts/studio.py check .` | 컨셉·아이템·영구 강화·적·전투 계산·판 안 성장·스탯 예산·강화·합성·재화 흐름·레벨 구성·플레이 기록을 한 번에 검사한다 |
| `python3 .claude/skills/studio-data/scripts/studio.py simulate data/meta.json` | 메타 성장을 시뮬레이션한다(추상 모델, 또는 `"model": "combat"`이면 전투 계산 데이터로) |
| `python3 .claude/skills/studio-data/scripts/studio.py calibrate data/meta_combat.json` | 플레이 기록의 단계 기록으로 가정값을 비교하고 생존 곡선 값을 제안한다. 파일을 고치지 않는다([calibration](../playtest-verdict/references/calibration.md)) |
| `python3 .claude/skills/studio-data/scripts/studio.py runlog runs.csv` | 판별 로그(CSV)를 세션의 단계 기록으로 모아 출력한다. 파일에 쓰지 않는다 |
| `python3 .claude/skills/studio-data/scripts/studio.py provenance design/` | 기획 문서(md)의 수치 출처 태그를 검사한다 |
| `python3 .claude/skills/studio-data/scripts/studio.py draft . --archetype <원형> --at <기준 값>` | 스탯 예산의 곡선과 원형으로 아이템·적 초안을 JSON으로 출력한다 (파일에 쓰지 않음) |
| `python3 .claude/skills/studio-data/scripts/studio.py setup claude .` | 판정 에이전트와 훅을 게임 프로젝트에 설치한다 (Claude Code, [아래](#claude-code-연결)) |

옵션은 `studio.py <명령> --help`로 본다. 종료 코드는 0 통과, 1 오류(또는 `--strict` 경고, `--fail-on-assumed` 가정), 2 사용법 오류(경로 없음, 읽을 수 없는 파일, `check`할 데이터 없음, `provenance`할 md 없음, `calibrate`로 비교할 기록 없음, 설정 오류)다. `check --fail-on-assumed`는 출처가 가정이거나 비어 있거나 읽을 수 없는 시뮬레이터 설정도 실패시킨다.

- **미확인은 통과가 아니다.** `check`에서 함께 검사할 데이터가 없어 확인하지 못한 참조가 남으면 최종 줄이 `INCOMPLETE`다(종료 코드 0, `--strict`나 `--fail-on-assumed`를 붙이면 1). 계산 파일(전투 계산·판 안 성장·재화 흐름·레벨 구성)에 오류 없이 계산한 것이 하나도 없을 때(빈 배열, 모두 삭제)도, 강화·합성의 가치 비교를 스탯 예산이 없어 하지 못했을 때도 같다. `provenance`에 md 파일이 하나도 없으면 종료 코드 2다.
- **확인한 경고.** 의도를 확인한 경고는 그 항목의 `acknowledged`에 `{경고 코드: 이유}`로 적는다. 경고 수와 `--strict`에서 빠지고 "확인한 경고"로 이유와 함께 따로 보인다. 오류는 확인으로 끌 수 없다. 한 항목에 대상이 여럿인 경고(전투 단계의 적별 행)는 `{경고 코드: {대상 id: 이유}}`로 그 대상만 확인한다. 문자열 이유는 그 항목의 그 코드 경고를 모두 덮어 나중에 생기는 경고도 숨긴다.
- `check --table`: 컨셉 비교표, 전투 계산표(단계 × 적), 빌드 비교표, 예산 비교표, 강화·합성 표, 재화 흐름 표, 조우 표를 마크다운으로 출력한다. `--table combat,growth`처럼 종류(`concepts`, `combat`, `growth`, `budget`, `crafting`, `economy`, `levels`)를 쉼표로 고르면 그 표만 낸다. 검사할 경로는 `--table` 앞에 적는다. `--ids a,b,c`는 컨셉 비교표에 고른 후보만 그 순서로 보인다.
- `simulate --policy cheapest_first` / `--compare-policies`: 설정 파일을 고치지 않고 구매 정책을 바꾸거나 정책들을 나란히 비교한다. 설정에 재화 흐름 연결(`economy`)이 있으면 `economy`(그 구매 계획 순서)도 쓰고 비교에 넣는다.

## 프로젝트 배치

```
<게임 프로젝트>/
├─ design/
│  └─ concepts.json   컨셉 후보와 선택한 컨셉의 브리프
└─ data/
   ├─ items.json      아이템, 드랍 테이블
   ├─ upgrades.json   영구 강화
   ├─ enemies.json    적
   ├─ combat.json     전투 계산: 스탯 역할, 방어 공식, 목표 범위, 단계별 기준 장비
   ├─ growth.json     판 안 성장: 단계별 레벨, 레벨업 선택지, 빌드
   ├─ budget.json     스탯 예산: 원가, 곡선, 배수, 원형
   ├─ crafting.json   강화 단계와 합성(레시피·무작위 합성·분해)
   ├─ economy.json    재화 흐름: 재화, 단계별 수입, 구매 계획
   ├─ playtests.json  플레이 기록과 가설 판정
   └─ meta.json       시뮬레이터 설정 (upgrades.json을 가리킴)
```

`view`와 `check`에 폴더를 주면 그 폴더와 바로 아래 `design/`, `data/`에서 데이터 파일을 찾는다. 종류는 JSON 최상위 키(`concepts` / `items` / `upgrades` / `enemies` / `combat` / `growth` / `budget` / `crafting` / `economy` / `playtests`)로 판단한다. 키의 형식이 틀려도 그 종류로 보고 형식 오류를 보고한다(건너뛰지 않는다). 파일 이름이 `concepts.json`처럼 종류 이름인데 그 키가 없으면 읽기 오류로 알린다. 항목이 아직 없으면 `"concepts": []`처럼 빈 배열을 넣는다. 시뮬레이터 설정과 관계없는 JSON은 건너뛴다. 파일을 직접 줄 수도 있다. 적의 드랍 테이블은 함께 읽은 아이템 데이터로, 전투 계산은 함께 읽은 아이템·영구 강화·적 데이터로, 판 안 성장은 전투 계산으로, 스탯 예산은 아이템·적 데이터(원가 제안은 전투 계산)로, 강화·합성은 아이템·드랍 테이블(가치는 스탯 예산)로, 재화 흐름은 적 보상·드랍·아이템 가격·영구 강화·강화·합성 비용으로, 플레이 기록의 컨셉·가설 참조는 함께 읽은 컨셉 데이터로 확인한다.

예시 프로젝트: `assets/sample-project/` (실제 기획이 아니다).

## 뷰어

- **서버 모드(기본)**: `studio.py view <폴더>`. 화면이 1.5초마다 원본을 다시 읽고, 내용이 바뀌었을 때만 다시 검사한다. 한 파일의 형식 때문에 검사기가 처리하지 못해도 그 파일만 오류로 표시되고 나머지는 계속 보인다. 탭은 컨셉, 아이템, 영구 강화, 적, 전투 계산, 판 안 성장, 스탯 예산, 강화·합성, 재화 흐름, 플레이 기록. 컨셉 탭은 제약, 선택한 컨셉의 브리프, 후보 비교표를 보여 준다. 전투 계산 탭은 공식·스탯 역할·목표 범위와 단계별 계산표(목표 이탈 칸 강조)를, 판 안 성장 탭은 빌드별 성장과 빌드 비교표를, 스탯 예산 탭은 원가와 원가 제안·곡선·비교표·원형을, 강화·합성 탭은 강화 단계표·합성 표·얻을 수 없는 아이템을, 재화 흐름 탭은 단계별 수입·구매 계획·남는 재화를, 플레이 기록 탭은 가설별 판정과 세션을 보여 준다. 문서를 생성하지 않으므로 동기화할 것이 없다. 기본으로 127.0.0.1에서만 열린다. 터미널을 닫으면 뷰어도 꺼진다. 데이터 파일이 아직 없어도 열리며, 지켜보는 위치를 안내하고 파일이 생기면 자동으로 보여 준다.
- **파일 모드(보조)**: `assets/viewer.html`을 직접 열고 '불러오기'로 JSON을 고른다. 원본에 적힌 값만 보여 주며 검사·점수·확률 계산은 하지 않는다. 검사 규칙은 파이썬에만 있고 JavaScript로 복제하지 않는다.

## Claude Code 연결

```bash
python3 .claude/skills/studio-data/scripts/studio.py setup claude .
```

게임 프로젝트 폴더에서 한 번 실행한다. 스킬을 다시 설치(`npx skills add …`)한 뒤에도 다시 실행한다. 쓰는 파일은 게임 프로젝트 안의 둘뿐이다.

| 파일 | 내용 |
|---|---|
| `.claude/agents/studio-judge.md` | 읽기 전용 판정 에이전트. 원본은 `assets/claude/studio-judge.md` |
| `.claude/settings.json`의 `hooks` | 아래 두 훅. 사용자의 다른 훅과 설정은 그대로 둔다 |

- **PostToolUse(Write·Edit)**: `design/`·`data/` 아래 파일을 고치면 데이터는 `check`, md는 `provenance`를 돌린다. 오류는 에이전트에게 바로 보이고(종료 코드 2), 경고는 참고 정보로 붙는다. 편집을 되돌리지는 않는다.
- **PreToolUse**: 판정 에이전트(`studio-judge`)가 파일을 쓰거나(Write·Edit·MultiEdit·NotebookEdit) `studio.py check`·`provenance` 밖의 명령을 실행하면 막는다. `--out`(파일 쓰기)과 셸 연결(`;`, `&&`, `|`, `>`, `$` 등)도 막는다. 다른 에이전트에는 관여하지 않는다.

다시 실행하면 이 도구가 넣은 훅만 바꾼다. `settings.json`이 JSON이 아니거나, `studio-judge.md`가 이미 있는데 setup이 만든 파일이 아니면 아무것도 바꾸지 않고 종료 코드 2로 끝난다. 훅이 쓸 파이썬은 `--python`으로 바꾼다(기본: Windows `py`, 그 밖 `python3`).

확인 범위: Claude Code 2.1.316, WSL(Linux)에서 실제 세션으로 확인했다. 판정 에이전트의 `check`는 통과하고 셸 리다이렉트 쓰기는 막혔으며, 메인 에이전트의 데이터 오류 편집은 오류로 되돌아왔고 메인 에이전트는 막히지 않았다. Windows에서의 훅 명령 실행은 아직 확인하지 않았다. Codex에는 같은 장치가 없다.

## 코드 구조

모든 파이썬 코드는 `scripts/studio_data/` 패키지에 있다.

| 모듈 | 역할 |
|---|---|
| `common` | 읽기, 종류 판별, 공통 필드(id·상태·출처) 검사 |
| `datasets` | 파일 찾기(각 파일은 한 번만 읽음) → 종류별 검사, 파일 간 참조 확인, 검사기 예외를 파일 단위로 격리 |
| `concepts`, `items`, `upgrades`, `enemies`, `combat`, `growth`, `budget`, `crafting`, `economy`, `playtests` | 종류별 검사 규칙 (`growth`는 빌드 시뮬레이션과 비교, `combat`은 전투 계산과 스탯 원가 제안, `budget`은 예산 비교와 초안, `crafting`은 강화 기대 비용과 합성 가치, `economy`는 수입과 구매 시점도 한다) |
| `meta_sim` | 메타 성장 시뮬레이터 |
| `provenance` | md 수치 출처 태그 검사 |
| `viewer` | 뷰어 서버 (내용이 바뀔 때만 다시 검사) |
| `claude` | Claude Code 연결: `setup`과 `hook` 처리기 |
| `cli` | `studio.py`의 하위 명령 |

새 데이터 종류를 추가할 때는 `common.DATASET_KINDS`, `datasets.VALIDATORS`, `assets/viewer.html`의 `KINDS`에 함께 등록한다.
