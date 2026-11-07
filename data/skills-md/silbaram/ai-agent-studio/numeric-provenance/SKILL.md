---
name: numeric-provenance
description: "Tags every tunable number in game design documents as assumed, computed, or measured, and checks the tags with a deterministic script before any balance or difficulty verdict. Use when writing or reviewing design numbers such as prices, drop rates, damage, HP, timers, level pacing, or economy values, and before declaring balance final."
---

# 수치 출처 태그

기획 문서의 수치가 어디서 왔는지 표시하고 스크립트로 검사한다. 목적은 **그럴듯한 숫자가 검증된 숫자처럼 취급되는 것을 막는 것**이다. 에이전트가 제안한 수치는 아무리 합리적이어도 처음에는 가정이다.

## 태그

| 태그 | 뜻 | 근거 적기 |
|---|---|---|
| `[가정]` 또는 `[가정: 메모]` | 아직 검증하지 않은 값. 에이전트 제안, 장르 관례, 감 | 선택 |
| `[계산: 출처]` | 스크립트·시뮬레이터·수식으로 산출한 값 | **필수**: 스크립트 경로, 실행 결과 파일, 시뮬레이션 ID |
| `[측정: 출처]` | 실제 플레이나 텔레메트리로 확인한 값 | **필수**: 플레이 기록 세션(`data/playtests.json#세션 id`), 리플레이, 로그 경로 |

영문 별칭 `[assumed]`, `[computed: …]`, `[measured: …]`도 같은 뜻으로 인정한다. 전각 콜론(`：`)도 허용한다.

## 규칙

1. **새 수치는 `[가정]`으로 시작한다.** 에이전트가 제안한 수치를 `[계산]`이나 `[측정]`으로 쓰지 않는다.
2. **태그는 증거로만 올린다.** `[가정]` → `[계산]`은 실제로 스크립트를 실행하고 그 출력을 출처로 적었을 때만 바꾼다. `[측정]`은 사람이 플레이한 기록이나 텔레메트리가 있을 때만 쓴다. 플레이 기록은 [playtest-verdict](../playtest-verdict/SKILL.md)로 남기고 세션 id를 출처로 적는다.
3. **수치 표에는 `출처` 열을 둔다.** 헤더가 정확히 `출처`, `source`, `provenance` 중 하나인 열이 있는 표는 모든 행에 태그가 있어야 한다. 표는 `|`로 시작하는 GFM 형식으로 쓴다. 수치 표가 아닌 표에는 이 헤더 이름을 쓰지 않는다. 헤더에 `출처`가 들어 있지만 정확히 같지 않으면(예: `출처 (근거)`) 그 표는 검사되지 않으므로 검사기가 경고한다.
4. **확정 판정 전 게이트.** "밸런스 확정", "난이도 OK" 같은 판정은 `--fail-on-assumed` 검사를 통과한 뒤에만 한다. 통과하지 못하면 남은 `[가정]` 목록과 함께 "미확정"으로 보고한다.
5. **값을 바꾸면 태그도 다시 본다.** `[계산]`이나 `[측정]` 값을 손으로 고치면 근거가 사라지므로 `[가정]`으로 내린다.
6. **사람의 판단은 `[가정]`이다.** 기획자가 의도적으로 정한 값도 검증 전에는 `[가정: 기획 의도]`로 표시한다. 의도를 존중하되 검증 상태와 섞지 않는다.
7. **본문 수치도 태그한다.** 표 밖 문장의 조정할 수 있는 수치(예: `부화는 6초 [가정]`)에도 태그를 붙인다. 태그는 수치 바로 뒤, 다음 수치 전에 둔다. 검사기는 '숫자 + 단위'(초, %, 배, 개, 명 등)마다 뒤따르는 태그가 있는지 보고, 없으면 경고한다. 한 줄의 태그 하나가 같은 줄의 다른 수치를 통과시키지 않는다(`5분 [가정], 3판 + 2명 [가정]`이면 `3판`을 경고). 태그 안의 숫자는 출처 설명으로 보고 검사하지 않는다. 단위가 없는 숫자는 찾지 못하는 추정 검사라 오류로 막지 않는다.
8. **브리프의 판정 기준도 같다.** 컨셉 브리프(`design/concepts.json`)의 `failure_signal`, `success_criteria` 문장 안 수치에도 같은 태그를 쓴다. `check`가 같은 규칙으로 검사하고, `--fail-on-assumed`는 `[가정]`이 남은 브리프를 실패로 본다.
9. **데이터 파일은 필드로 표시한다.** 아이템·영구 강화·적처럼 JSON/CSV 원본에 있는 수치는 md 태그 대신 항목의 `provenance` 필드(`assumed`/`computed`/`measured`)로 표시하고 `python3 .claude/skills/studio-data/scripts/studio.py check data/ --fail-on-assumed`로 검사한다([progression-economy](../progression-economy/SKILL.md)). 같은 수치를 md에 옮겨 적지 않는다.

## 검사

```bash
python3 .claude/skills/studio-data/scripts/studio.py provenance design/
```

- 기본: 형식 오류(태그 이름 오타 포함), `[계산]`·`[측정]`의 출처 누락, 출처 열의 태그 누락을 찾는다. 오류가 있으면 종료 코드 1. 본문의 태그 없는 수치와 출처로 인식되지 않는 헤더는 경고만 한다.
- md 파일이 하나도 없으면 아무것도 검사하지 않은 것이므로 종료 코드 2로 끝난다. 통과로 보고하지 않는다.
- `--fail-on-assumed`: `[가정]`이 하나라도 남으면 실패한다. 확정 판정 직전에 쓴다.
- `--check-paths`: 출처가 경로처럼 보이면(슬래시 포함, 또는 `.py`/`.json`/`.csv` 등으로 끝남) 문서 폴더나 현재 폴더 기준으로 파일이 실제 있는지 확인한다. 출처가 플레이 기록 파일`#세션 id`이면 그 세션이 기록에 있는지도 확인한다.
- `--json`: 결과를 JSON으로 출력한다.

코드 블록과 인라인 코드 안의 태그는 검사하지 않는다. 검사 도구는 공용 스킬 [studio-data](../studio-data/SKILL.md)에 있으며 이 스킬과 함께 설치한다. 명령은 게임 프로젝트 폴더에서 Claude Code 설치 기준(`.claude/skills/…`)으로 적었다. Codex는 `.agents/skills/…`, Windows PowerShell은 `python3` 대신 `py`([실행 경로](../studio-data/SKILL.md#실행)).

## 보고

수치를 다룬 작업이 끝나면 다음을 함께 보고한다.

- 가정 / 계산 / 측정 개수와 오류 수 (스크립트 출력 그대로)
- 남은 `[가정]` 중 결과에 가장 큰 영향을 주는 것과, 그것을 `[계산]`이나 `[측정]`으로 바꿀 가장 싼 방법
- 검사를 실행하지 못했다면 그 사실. 실행하지 않은 검사를 통과했다고 쓰지 않는다.

예시는 [references/example.md](references/example.md)를 본다.
