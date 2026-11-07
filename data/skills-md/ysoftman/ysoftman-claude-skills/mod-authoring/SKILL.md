---
name: mod-authoring
description: Claude Code mod(함수 hook 플러그인 — pane/패널, 프롬프트 위 band, 단축키 칩, 슬래시 명령)를 만들거나 고칠 때 내장 `plugin-authoring` 스킬과 함께 쓰는 실전 가이드. 패널 탭 표시·전환, keybindings.json `command:` 단축키와 그 안내(프롬프트 아래 힌트 줄 tail), 여러 mod 가 band·힌트 줄을 함께 쓰는 법, 테스트 kit 요령, 수정이 반영되지 않을 때 로드 경로 확인을 다룬다. 사용자가 mod, 모드 만들어, 패널, pane, band, 프롬프트 위 한 줄, 힌트 줄, PromptHint, 단축키 칩, 탭 전환, "reload-plugins 했는데 안 바뀜", `ysoftman-claude-kit/plugins`, `dev-mods`, `register.tsx`, `ui.render`, `$.ui.open` 등을 언급하면 plugin-authoring 과 함께 반드시 사용한다.
---

# Mod Authoring

내장 `plugin-authoring` 스킬이 API·타입·예제를 준다면, 이 스킬은 실제 mod(`summary`, 배포 진행 패널 mod)를 만들며 엔진 코드로 확인한 동작과 거기서 나온 패턴을 담는다. 둘을 같이 로드하고, API 세부는 `plugin-authoring` 의 타입 파일(`claude-code.d.ts`)을 grep 해 확인한다.

재사용 코드(토글, 단축키 읽기, pane 하단 설정 안내, help 명령, 힌트 줄 단축키, 테스트 mock)는 [references/snippets.md](references/snippets.md) 에 있다. 해당 기능을 구현할 때 읽는다.

## 작업 순서

1. `plugin-authoring` 을 로드하고, 쓰려는 이벤트·props 를 타입 파일에서 확인한다.
2. **이 세션이 어느 사본을 로드하는지 먼저 확인한다** (아래 "로드 경로"). 엉뚱한 사본을 고치면 테스트는 통과하는데 화면은 그대로다.
3. 구현한다. TS/TSX 는 `plugin-authoring` 예제 스타일(작은따옴표, 세미콜론 없음, 2-space)을 따르지 않고 처음부터 biome 기본 포맷(tab, 큰따옴표, 세미콜론, 폭 80)으로 쓰고, 플래그 없이 `biome check --write <파일>` 로 맞춘다.
4. 요구 동작마다 테스트를 쓰고, **수정 전 코드에서 그 테스트가 실패하는지** 확인한다: `git stash push <register.tsx>` → `claude plugin test .` → `git stash pop`. 새 코드에서만 통과해야 회귀를 잡는 테스트다.
5. 검증: `claude plugin validate .`, `claude plugin test .`, `bunx -p typescript tsc -p .`. validate·test 는 타입 체크를 하지 않으니 tsc 를 빼먹지 않는다.
6. 로드되는 사본에 반영 → `/reload-plugins` → 사용자에게 화면 확인을 부탁한다. 테스트 kit 은 엔진 동작을 흉내낼 뿐이라 실제 배치·탭·단축키는 화면에서만 확인된다. 확인 전에는 "테스트는 통과, 화면 미확인"으로 보고한다.

## 로드 경로: 고쳤는데 반영이 안 될 때

`/reload-plugins` 는 플러그인을 **로드된 위치에서** 다시 읽을 뿐이다.

| 로드 방식 | 실제로 읽는 위치 |
| --- | --- |
| `CLAUDE_CODE_PLUGIN_DIRS`, `--plugin-dir` | 작업 폴더 그대로 (hot reload) |
| marketplace 설치 플러그인 | `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/` |
| 이 세션에서 만든 mod | `~/.claude/dev-mods/<session>/<mod>/` |

- 설치 경로는 `~/.claude/plugins/installed_plugins.json` 의 `installPath`, 실행 인자는 `ps -ax -o pid,args | rg '[c]laude'` 로 확인한다.
- `diff -rq --exclude=types --exclude=tsconfig.json <작업 저장소 mod> <캐시 mod>` 로 차이를 본다.
- 개발 중에는 `claude --plugin-dir <저장소>` 로 시작하는 게 가장 깔끔하다. 이미 떠 있는 세션이면 바뀐 파일만 캐시 같은 경로로 복사하고 `/reload-plugins` 한다. 캐시 패치는 플러그인 업데이트 때 덮어써진다는 점을 사용자에게 알린다.

## Pane(패널)과 탭

엔진 동작 (v2.1.29x, 엔진 코드로 확인):

- pane 이 여러 개면 **하나만 보이고 나머지는 탭**이다. 탭 제목은 여백 포함 최대 12칸에서 잘리므로 `title` 은 10칸 이내로 둔다(한글 1자 = 2칸, 예: `배포 패널` 9칸). 본문 제목은 pane 안에서 따로 그린다.
- 이미 열린 id 로 `$.ui.open` 을 다시 부르면 **제목만 바뀌고 앞으로 올라오지 않는다**. 반면 새로 연 pane 은 (키보드를 가진 pane 이 없으면) 보이는 탭이 된다. 그래서 가려진 탭을 앞으로 꺼내려면 close 후 다시 open 한다(대신 탭 순서가 맨 뒤로 간다).
- `focus: true` 는 빈 composer 일 때만 앞으로 올리고 키보드까지 가져간다. 탭 전환 용도로는 쓰지 않는다.
- `$.ui.panes()` 는 **자기 plugin 의 pane 만** 준다. `isShown` = 지금 보이는 탭, `isPlaced: false` = 좁은 터미널에서 대기 중(사람이 요청하지 않은 open 은 144칸, 한 번 연 id 는 110칸 미만이면 대기). 대기 중인 pane 은 `isShown` 도 false 다.
- **가려진 탭의 pane 은 render 되지 않는다.** 그 안의 Button 도 사라진다.
- 탭을 클릭해 전환해도 이벤트가 없다. `$.clock.every` 에서 `$.ui.panes()` 를 폴링해 보임 여부가 바뀔 때만 상태를 갱신하고 다시 그린다.
- 탭 이동은 엔진 action `pane:previous`/`pane:next` 가 한다(2.1.300 확인). 모든 plugin 의 열린 pane 을 순서대로 돌고 끝에서 처음으로 돌아온다. `Global` 문맥에서 pane 이 2개 이상일 때만 동작하고 **기본 키가 없다**. mod 가 다른 plugin 의 탭을 넘길 API 는 없으니(`$.ui.panes()` 는 자기 것만) mod 를 만들지 말고 이 action 을 바인딩한다(아래 "단축키").

토글은 "열림" 이 아니라 "보임" 기준으로 짠다: 보이면 닫고, 열려 있지만 가려졌거나 대기 중이면 닫았다 다시 열고, 없으면 연다. 열림 기준으로 짜면 가려진 탭에서 단축키를 눌렀을 때 앞으로 나오지 않고 닫혀 버린다. 코드는 snippets 의 "보임 기준 토글".

## 단축키

mod 단축키는 **슬래시 명령을 `keybindings.json` 의 `command:` action 에 묶는 방식**으로 만든다. summary·rule-guard 가 이 방식이다(2.1.299 에서 확인).

- plugin 은 키를 직접 등록할 수 없다. Button 의 `action` 도 엔진 action 이름만 받는다. 대신 `~/.claude/keybindings.json` 의 **`"Chat"` 문맥**에 `"ctrl+x s": "command:summary"` 처럼 슬래시 명령을 묶으면, 그 키가 명령을 입력한 것처럼 실행한다.
- action 은 `^command:[a-zA-Z0-9:\-_]+$` 형식만 받아 **인자를 넣을 수 없다**. 인자 없이 실행했을 때 토글하는 명령을 묶는다: bare `/<명령>` 을 토글로 두고 그대로 묶는다(`command:summary`, `command:rule-guard`). 표 같은 출력은 `list` 같은 인자로 옮긴다. 명령을 하나 더 만드는 `/<mod>-pane` 방식은 명령 목록만 늘린다는 의견이 있어 쓰지 않는다. 명령 이름은 영문·숫자·`_`·`-` 만 된다.
- 토글 명령은 `{}`(text 없음)를 돌려준다. text 를 주면 키를 누를 때마다 대화 기록에 출력이 남는다. `immediate: true` 로 등록해 턴이 도는 중에도 바로 실행되게 한다.
- 키를 받으려고 Button 을 숨겨 둘 필요가 없다. 엔진 action 빌리기(평소 비어 있는 `app:toggleDiffPreSession` 같은 diff 패널 action 을 Button `action` 에 다는 예전 방식)는 쓰지 않는다. diff 패널이 열려 있으면 원래 동작이 우선하고, 그 action 의 엔진 기본 키(`app:cycleDiffBase` 의 `ctrl+x b`)에도 반응하며, 기본 키 없는 빈 action 도 더 남아 있지 않다.
- 안내는 실제로 바인딩한 사람에게만 보인다: `keybindings.json` 을 읽어 `command:<명령>` 에 묶인 키(문맥 무관)를 찾고, 있으면 그 키를 힌트 줄·pane 하단·명령 설명에 표시한다. 없으면 단축키 안내 대신 슬래시 명령 이름을 쓰고, 설정 방법은 아래 "설정 가이드"로 알린다. 키 이름을 코드에 고정하면 설정하지 않은 사람에게 눌러도 안 되는 단축키가 보인다.
- 다시 읽는 시점은 `session.start`, 자기 명령 실행, 관련 스킬 시작 정도면 충분하다(매 프레임 읽지 않는다). 명령 목록의 설명 문구는 등록 시점 값이라 다음 세션에 바뀐다.
- myenv 의 `installclaudecode.sh` 가 mod 단축키(토글 키와 탭 이동 키)를 `keybindings.json` 에 넣는다. action 이 이미 묶여 있으면 그 action 을, 키가 이미 쓰이면 그 키를 건너뛴다. 새 mod 에 단축키를 만들면 거기 `--argjson add` 목록에 `{"context", "action", "keys": [...]}` 한 항목을 추가한다.
- 엔진 기본 `ctrl+x tab` 은 band·pane 에 포커스를 주고, 그 상태에서 Tab·Enter 로 탭을 고를 수 있다. 바인딩과 무관하게 동작하니 pane 하단 안내에 같이 둬도 된다.
- pane 하단 단축키 설명은 **영어로 짧게** 쓴다(`close`, `open/close`, `focus`, `tabs`). help·명령 설명은 mod 의 언어를 따른다.
- **탭 이동 공통 단축키**: `"Global"` 블록에 `"ctrl+<": "pane:previous"`, `"ctrl+>": "pane:next"` 를 묶는다. 터미널이 shift 문장부호를 바뀐 문자(`<`)로 보내면 엔진은 shift 를 빼고 `ctrl+<` 로 맞추고, `,`+shift 로 보내면 `ctrl+shift+,` 로 맞춘다. 그래서 `ctrl+shift+,`/`ctrl+shift+.` 도 함께 묶는다.
- pane 하단 단축키 안내에는 `pane:previous`/`pane:next` 에 묶인 키도 토글 키와 같은 방식(묶였을 때만)으로 읽어 표시한다(summary·rule-guard `tabs`, 배포 진행 패널 `prev tab`/`next tab`). 하단 한 줄에 안내가 넘치면 `flexWrap="wrap"` 과 `columnGap` 으로 다음 줄로 넘긴다(`gap` 은 줄 사이도 벌린다). 코드는 snippets 의 "바인딩된 키 읽기".

### 설정 가이드: 빠뜨리지 않는다

단축키를 쓰는 mod 는 아래를 **모두** 갖춘다. 하나라도 빠지면 공유받은 사람은 단축키가 있다는 것 자체를 모른다(summary mod 가 처음에 그랬다).

- **pane 하단 설정 안내**: 토글 키나 탭 이동 키 중 빠진 게 있으면 pane 하단 단축키 줄 아래에 안내 블록을 그리고, 다 묶이면 블록을 통째로 뺀다. 대부분은 단축키를 직접 넣어야 한다는 걸 모르고, help 는 찾아 실행해야만 보이므로 pane 에서 바로 알린다. 블록은 다음 순서로 그린다.
  - 노란 첫 줄: `⚠ 단축키 미설정 · Claude 에게 "<mod> mod README 대로 단축키 설정해줘" 라고 해도 된다`
  - 흐린 둘째 줄: `직접 넣으려면 ~/.claude/keybindings.json 에 (기존 블록에 합친다):`
  - 빠진 것만 문맥별 JSON 한 줄씩(`"Chat"` 토글, `"Global"` 탭 이동과 `ctrl+shift+,`/`.` 메모)

  Claude 는 pane 내용을 볼 수 없어서 요청 문구는 README 를 가리킨다. 그래서 README 의 바인딩 JSON 에 빠짐없이 넣는다(아래 README 항목). 단축키 설정만 하는 스킬은 따로 만들지 않는다. 문구는 mod 의 언어를 따르고(summary 는 영어), 넣을 줄이 잘리면 안 되니 `wrap="truncate-end"` 를 주지 않는다. 여러 mod 를 한 플러그인에 묶으면 문구를 공용 상수로 둔다(팀 플러그인의 `mods/tab-keys.ts` 의 `KEYS_SETUP`). 코드는 snippets 의 "pane 하단 설정 안내".
- **`<명령> help`**: 사용법을 보여 주고, 묶인 탭 이동 키가 있으면 그 줄도 넣는다. 토글 키나 탭 이동 키 중 빠진 게 있으면 "단축키는 mod 가 등록하지 않는다. Claude 에게 "<mod> mod README 대로 단축키 설정해줘" 라고 하거나 `~/.claude/keybindings.json` 에 직접 추가한다(기존 블록에 합친다)"는 안내와 빠진 것만 문맥별 JSON 한 줄씩(`"Chat"` 토글, `"Global"` 탭 이동과 `ctrl+shift+,`/`.` 메모) 덧붙인다. 다 묶여 있으면 이 안내를 빼고 `keybindings.json` 도 언급하지 않는다. 실행할 때마다 `keybindings.json` 을 다시 읽어 세션 중에 바인딩해도 바로 반영되게 하고, pane 은 열거나 닫지 않는다.
- **help 로 찾아가는 길**: 명령 설명 끝에 `· help: 사용법` 을 붙이고 `argumentHint: "[help]"` 를 준다. pane 하단 안내에도 `<명령> help` 를 늘 둔다(폭이 좁으면 라벨 없이 keycap 만).
- **키 이름 고정 금지**: `plugin.json` 의 `description` 같은 고정 문구에 키를 쓰지 않는다. 명령 이름(`/<명령>`)을 쓴다.
- **mod 폴더의 README.md**: 다음을 적는다.
  - 설치: `ysoftman-claude-kit` marketplace 의 `/plugin install <mod>@ysoftman-claude-kit`, 개발 중에는 `CLAUDE_CODE_PLUGIN_DIRS` 에 폴더 경로 추가(여러 개면 `:` 구분) 또는 `claude --plugin-dir <폴더>`
  - 사용: `<명령>`, `<명령> help`
  - 단축키: 바인딩 JSON(`"Chat"` 블록의 `"<키>": "command:<명령>"` 과 `"Global"` 블록의 `pane:previous`/`pane:next` 4개 키), "이미 파일이 있으면 덮어쓰지 말고 `Chat`·`Global` 블록의 `bindings` 에 위 줄만 추가(블록이 없으면 추가, 이미 다른 키에 묶은 action 이나 다른 action 에 쓰는 키는 건너뜀)", 다른 키에 묶어도 안내가 그 키를 따른다는 점, 빠진 바인딩이 있으면 pane 하단에 설정 안내가 나오고 Claude 에게 이 README 대로 설정해 달라고 하면 된다는 점. Claude 는 pane 안내의 요청을 받으면 이 JSON 만 보고 넣으므로 여기서 빠진 키는 설정되지 않는다.
  - 확인한 Claude Code 버전
- **README 커밋**: mod 가 `.claude` 처럼 gitignore 된 경로에 있으면 새 README 는 `git status` 에 안 보인다. `git add -f` 로 넣는다.
- **테스트**: `help` 출력과 pane 하단 설정 안내를 바인딩 없음(Claude 요청 문구와 설정 방법 포함, pane 그대로)과 있음(키 표시, 설정 방법 없음) 두 경우로 확인한다. 토글 키만 빠진 경우처럼 일부만 묶였을 때 빠진 줄만 나오는지도 본다. 단축키 동작은 kit 에서 인자 없는 `$.command.run({ command, args: "" })` 로 흉내내고, text 없이 pane 을 열고 닫는지 본다.

코드는 snippets 의 "바인딩된 키 읽기"와 "help 명령".

## 힌트 줄(PromptHint): 단축키 안내 자리

band 에 칩 줄을 두면 할 일이 없을 때도 프롬프트 위 한 줄을 늘 차지한다. 단축키 안내는 프롬프트 아래 힌트 줄(`? for shortcuts` 줄) 끝에 흐린 글씨로 붙인다. summary mod 가 이 방식이다.

- `ui.render` 의 `{ component: "PromptHint" }` 에서 `props.tail` 을 채워 `next` 로 넘긴다. 엔진이 원래 줄(pill 포함)을 그대로 그리고 끝에 ` · ` 와 tail 을 dim 으로 붙이며, 줄 끝에서 자르고 4칸 미만이면 뺀다(v2.1.296 엔진 코드 확인). tail 에 구분자를 직접 넣지 않는다.
- **tail 이어 붙이기 규칙**: 위 hook 이 넘긴 `e.props.tail` 을 지우지 말고 `[e.props.tail, 내 안내].filter(Boolean).join(" · ")` 로 이어 붙인다. 여러 mod 가 끼어도 한 줄로 합쳐진다.
- 자기 pane 이 보이는 동안에는 `return next(e)` 로 빠져도 된다(pane 하단에 같은 안내가 있으므로).
- 바인딩이 없으면 슬래시 명령 이름을 쓰거나 아예 뺀다.

코드는 snippets 의 "힌트 줄 단축키".

## Band(AbovePrompt) 함께 쓰기

진행 상태처럼 정말 보여 줄 정보가 있을 때만 band 를 쓴다.

- band 는 여러 plugin 의 hook 이 위에서 아래로 감싸는 chain 이다. 위 hook 은 `next(e)` 결과(아래가 그린 tree)를 자기 tree 에 넣는다. 그릴 게 없으면 `return next(e)` 하고, `e.props.hasSurvey` 면 양보한다. `next(e)` 결과를 빠뜨리면 아래 mod 가 화면에서 사라진다.
- plugin tree 가 하나라도 있으면 엔진이 `[-]` 를 붙여 band 한 줄을 차지한다. 그래서 단축키 안내는 band 가 아니라 힌트 줄에 둔다.
- 자기 pane 이 보이는 동안에는 band 를 그리지 않는다(같은 정보가 pane 에 있으므로).
- 예전 규칙(단축키 칩을 key `band-chips` Box 에 넣고 위 hook 이 `takeChips` 로 모아 한 줄로 그림)은 기존 mod 모두 힌트 줄로 옮겨 더 쓰지 않는다.
- `next(e)` 결과는 plain-data tree(`{ type, props, children }`)다. Box·Button 의 key 는 `props.key` 에 있다. 다른 mod 의 Button 을 옮겨 그려도 그대로 눌린다(테스트로 확인).

## 다시 그리기와 상태

- 모듈 변수는 reload 때마다 초기화된다. 스피너 프레임, 보임 여부처럼 다시 계산할 수 있는 그리기용 값에만 쓴다.
- `$.state` atom 은 세션 동안 유지되고, 값을 쓰면 그 값을 읽은 render 가 다시 그려진다. 계약은 `types/index.d.ts` 의 `PluginState` 에 선언하고, 키 이름을 바꾸면 계약도 같이 바꾼다.
- 값이 바뀔 때만 쓴다(`read` 후 비교하고 `update`). 매 tick 쓰면 불필요하게 다시 그려지고, write 횟수를 검사하는 테스트도 깨진다.
- 애니메이션은 필요할 때만: 작업 중일 때 10fps, 그 밖엔 느리게 또는 멈춤. `$.ui.invalidate("ui.render")` 를 무조건 돌리지 않는다.

## 테스트 kit 요령

자세한 mock 코드는 snippets 의 "테스트 mock".

- kit 에는 엔진 bottom 이 없다. `ui.open`/`ui.close`/`ui.panes` 를 메모리로 흉내내고, `isShown` 은 실제처럼(대기 중이면 false, 새로 연 pane 은 보이는 탭) 계산한다. 흉내가 실제와 다르면 테스트가 엉뚱한 동작을 승인한다.
- `$.session.start` 를 부르려면 `session.start`·`command.register` 응답 hook 이 필요하다. `$.clock.every` 는 보통 `session.start` 에서 걸리므로, 타이머를 테스트하려면 세션을 시작해야 한다.
- 모든 `on(...)` 은 테스트에서 `$` 를 처음 부르기 전에 등록한다.
- `mock.clock(on)` 이 준 clock 의 `advance(ms)` 로 타이머를 돌린다.
- `find`/`findAll` 에서 Text 의 key 는 남지 않으니 문구로 찾는다. `findAll` 결과의 `children` 에서 key 는 `props.key` 다.
- 다른 mod 를 흉내낸 test hook 의 Button 은 `ui.press({ key, plugin: "test" })` 로 누른다.
- `keybindings.json` 읽기는 `env.get`(HOME), `fs.read` 를 mock 한다. mock 이 없으면 읽기가 실패하므로 "바인딩 없음" 시나리오가 된다.
- UI 테스트는 `["terminal", "desktop"]` 두 surface 를 모두 돈다.

## 문서에 없는 엔진 동작 확인

타입 파일의 doc comment 를 먼저 본다. 그래도 모르면(예: 탭 폭, 이미 열린 id 의 open 동작) 엔진 코드를 직접 확인한다.

```bash
strings -n 8 "$(readlink -f "$(command -v claude)")" | rg -o '.{0,200}shownId.{0,200}' | head
```

엔진 코드는 버전마다 바뀌고 이름이 축약돼 있다. 확인한 사실과 추정을 구분해 보고하고, 확인한 버전을 함께 적는다.
