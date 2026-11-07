---
name: h2m-config
description: Homenet2MQTT(h2m) 설정에 디바이스 엔티티(climate/light/sensor/fan/switch 등)와 필요한 automation/scripts를 추가하는 방법론. 1순위 근거는 이미 적용된 예제 설정과 벤더 갤러리 프리셋(discovery.match·개수 파라미터·$repeat)이며, 그 둘로 설명되지 않는 디바이스만 원시 RS485 패킷 역산을 폴백으로 쓴다. 갤러리 스니펫의 automation/scripts(주기 폴링·버스 대리응답·벨/엘리베이터 시퀀스·복합 TX 패킷 생성)는 엔티티 동작의 일부이므로 엔티티만 옮기고 끝내지 않는다. 홈넷 버스는 조작할 때만 트래픽이 생기는 경우가 많으므로 사용자에게 월패드·스위치·리모컨 조작을 구체적으로 요청하는 단계를 포함하고, 사용자가 알려준 벤더·모델명은 탐색 우선순위 힌트로 쓰되 이름만으로 예제를 확정하지 않는다. "unmatched 패킷 정리해줘", "이 패킷에 맞는 엔티티 추가해줘", "패킷만 보고 엔티티를 만들어줘", "갤러리 프리셋으로 히터/조명 늘려줘", "설정에 없는 디바이스 붙여줘", "패킷이 안 잡히는데 뭘 조작해야 하나", "상태가 갱신되게 주기 조회를 넣어줘", "현관벨 자동열기/엘리베이터 호출 시퀀스를 붙여줘", "패킷을 직접 보내서 전등이 실제로 켜지는지 확인해줘" 같은 요청에 사용. h2m 주소를 모르거나 Agent API를 어떻게 켜고 토큰을 발급하는지 모르는 사용자에게는 연결부터 안내한다(references/connection-setup.md). h2m은 REST(`/api/v1/agent`)와 MCP(`/api/v1/agent/mcp`)로 같은 도메인 로직을 노출하므로 클라이언트에 MCP 도구가 있으면 MCP로, 셸만 있으면 스크립트로 작업하고 표면별 차이는 references/interfaces.md를 따른다. 패킷 전송 권한이 있으면 생성한 커맨드가 실제 기기를 움직이는지 확인할 때만 미리보기 → 대상·hex·순서·간격을 밝힌 사용자 승인 → 승인된 1회/시퀀스 전송 → 실기기 동작 확인 순서를 지킨다.
argument-hint: [portId]
---

# H2M 엔티티 추가: 예제·갤러리 우선, 패킷 역산은 폴백

## 목적

여기서 "config"는 API로 다루는 브릿지 설정 전반(초기 예제 선택, 포트/브릿지 추가, 엔티티 추가·검증·적용, automation/scripts 반영, 설정 백업·복원, 재시작)을 뜻한다. MQTT 브로커·애드온 옵션·API 토큰·서비스 로그는 API 밖이므로 사용자에게 요청한다(`references/interfaces.md` §6). 기존 설정을 수정하기 전에는 `/backups`로 원본 YAML을 확보해 두고, 필요하면 같은 백업으로 되돌린다.

h2m의 설정은 프레이밍(rx_header/rx_length)·체크섬·디코드·필드 조합이 얽혀 있어 처음부터 손으로 쓰기 어렵다. 그래서 이 스킬의 목적은 **h2m이 이미 가진 프로토콜 자산(적용된 예제 설정 + 벤더 갤러리 프리셋)에 홈네트워크 패킷이 실제로 말하는 디바이스를 엮어 엔티티를 추가하는 것**이다. 새 프로토콜을 발명하는 작업이 아니라, 검증된 프리셋의 어휘 안에서 채널·개수를 늘리는 작업이 기본값이다.

- **기본 경로**: 라이브 설정 → 갤러리 프리셋 → 예제 설정 순으로 근거를 찾아 초안을 만들고 `/entities/*`로 적용
- **폴백 경로**: 위 셋으로 설명되지 않는 디바이스에 한해 원시 패킷을 직접 역산
- **automation/scripts는 엔티티의 일부**: 갤러리 스니펫이 주기 폴링·대리응답·시퀀스·복합 TX를 담고 있으면 같은 초안에 넣는다. 빠뜨리면 상태가 갱신되지 않거나 버스 질의에 응답하지 못한다(`references/automation-scripts.md`)
- 어느 경로든 **홈넷 버스는 조작해야 말한다**. 트래픽이 조용하면 대기하지 말고 사용자에게 피지컬 디바이스 조작을 요청한다

## 우선순위 (이 순서를 지킨다)

1. **라이브 설정** — `/entities --full`의 동일 타입 엔티티(구조·mask·버튼값의 원본)와 포트 `packetDefaults`
2. **갤러리 프리셋** — API `/gallery*`로 읽는 `discovery.match`·`parameters`/`$repeat`·`requirements`와 `automation`/`scripts` 블록
3. **예제 설정** — 예제 파일의 전체 내용(`/setup/examples/<file>`). `/setup/apply`는 serial·packet_defaults만 복사하며, 엔티티·automation·scripts는 절대 가져오지 않는다(엔티티 정의는 오직 조회용 참고 자료임)
4. **직접 패킷 역산** — 위 셋에 정보가 없을 때만. 변동 증거를 확보한 뒤 최소 필드만

4번은 기본이 아니라 최후 수단이다. 갤러리 HIT이 있는데 바이트를 새로 추론하는 것, 예제에 채널 2개가 있는데 4개를 관측한 것을 역산으로 푸는 것은 모두 잘못된 순서다.

## 원칙

1. **프리셋이 1차 증거다.** 필드 조합·mask·디코드는 프리셋/기존 엔티티에서, 구체 바이트는 라이브 설정에서 가져온다. 같은 벤더의 다른 채널이 이미 정상 파싱되고 있다면 그 설정이 해당 버스의 정답이다.
2. **변동은 폴백에서의 유일한 증거다.** 값이 바뀌지 않는 바이트로 새 레이아웃을 확정할 수 없다. 정적 관측만으로 시그니처를 지으면 다른 디바이스를 삼킨다.
3. **추측 시그니처는 미매칭보다 해롭다.** 설명되지 않는 패킷은 억지 엔티티를 만들지 말고 미해결로 보고한다.
4. **홈넷 버스는 조작해야 말한다.** 무트래픽이면 이벤트형(월패드·스위치·리모컨 조작 시에만 송수신)일 수 있다. 조작 요청은 대상·동작·유지시간을 한 번에 묶어 구체적으로 한다.
5. **벤더명은 힌트다.** 사용자가 알려준 벤더·모델은 갤러리·예제 탐색의 시작점으로 **우선 사용**하되, 이름만으로 `/setup/apply`하지 않는다. 내부 프로토콜 세대 차이·파생 모델·혼선 배선으로 어긋날 수 있으므로 수집 바이트의 프레이밍/체크섬/채널 검증이 최종 판정이다.
6. **커맨드는 관측 바이트로 증명한다.** `state` 파싱이 맞아도 `command_*`가 버스에서 실측된 TX hex와 1바이트 차이까지 일치해야(`preview` 대조) 신뢰할 수 있다.
7. **automation은 엔티티가 못 하는 일만 맡는다.** 상태 파싱·단일 커맨드는 엔티티에 두고, 요청/응답·시퀀스·복합 TX 생성만 automation/scripts로 뺀다. 갤러리 스니펫에 해당 블록이 있으면 "이 디바이스가 원래 그렇게 동작한다"는 증거로 취급하되, 사용자 환경에 없는 채널을 위한 폴링은 옮기지 않는다.
8. **실기기 전송은 승인된 계획대로.** 전송 권한(`features.packetSend`)은 허용일 뿐 동의가 아니다. 보낼 패킷 전체(대상·hex·순서·간격)를 `preview`로 확정해 보여주고 한 번에 승인받은 범위 안에서만, 에이전트가 정한 횟수만큼 보낸다. 1회일 수도 있고 "거실→방1→방2 ON 후 1초 뒤 OFF" 같은 시퀀스일 수도 있다. 전송 후 사용자에게 실제 기기 반응을 확인하고, 무반응·부분 실패면 같은 시퀀스를 반복하지 말고 원인을 좁혀 다시 승인받는다.

## 전제와 범위

- **시리얼 프레이밍과 체크섬은 알려진 상태**에서 시작한다: `/ports`의 `serial`(path/baudRate/parity/stopBits)과 `packetDefaults`(`rx_length`, `rx_checksum`, `rx_header`, `tx_header`, footer), 체크섬 로직(`add` / `xor` / `add_no_header` / `xor_no_header` / `add_final_xor(..)`).
- 범위 밖(확장 예정): 시리얼 주소·보드레이트 자동 탐색(포트 스캔, parity/stop 브루트포스), 물리 `/dev/tty*` 예제별 baud 최적화.
- 작업 표면은 REST(`$H2M_URL/*`, `scripts/h2m.mjs`)와 MCP(`POST $H2M_URL/mcp`, `scripts/mcp.mjs`) 둘이다. 같은 도메인 로직이라 결과·rate limit·`draftHash` 규칙이 같고, 표면별 차이는 `references/interfaces.md`에 정리돼 있다.
- 갤러리·예제가 커버하는 벤더는 여기서 새로 만들지 않는다. 커버되지 않는 프로토콜만 폴백 역산 대상이다.

## 외부 문서 — 필요하면 배포 문서를 읽는다

이 스킬의 `references/`가 1차 자료다. 저장소 체크아웃이 없거나 UI·설치·고급 설정처럼 스킬 범위 밖의 최신 안내가 필요하면 **해당 페이지만** 가져온다(웹 도구가 있을 때).

- 문서 루트: <https://homenet2mqtt-docs.vercel.app/>
- Agent API: <https://homenet2mqtt-docs.vercel.app/guide/agent-api.html>
- 스킬 설치·사용: <https://homenet2mqtt-docs.vercel.app/guide/agent-skills.html>
- 갤러리: <https://homenet2mqtt-docs.vercel.app/guide/gallery.html>
- 설치: <https://homenet2mqtt-docs.vercel.app/guide/install-addon.html> · <https://homenet2mqtt-docs.vercel.app/guide/install-docker.html>

- 문서는 최신 배포(main) 기준일 수 있다. 설치된 h2m 버전과 어긋나면 **라이브 `/capabilities`·API 응답·`/schema`가 우선**이다.
- 위 경로를 그대로 쓴다(`.html` 포함). 사이트 전체를 크롤링하지 말고 필요한 페이지만 읽는다.
- 공개 문서 사이트이므로 토큰·내부 주소를 요청에 담지 않는다.

## 0. 연결 — 사용자가 주소·API를 모를 때

사용자는 보통 **UI 주소만** 알고, Agent API의 존재·포트(기본 3001)·토큰은 모른다. 추측한 URL로 재시도하지 말고 아래 순서로 확인한다(설치 형태별 상세: `references/connection-setup.md`).

1. **한 번에 묻는다**: 설치 형태(HA 애드온 `Homenet2MQTT` / `Homenet2Matter` / Docker / 직접 실행), H2M UI가 열리는 주소, HA·Docker 호스트 IP, `설정 > Agent API` 화면이 보이는지, 토큰을 이미 발급받았는지
2. **Agent API base는 UI 주소가 아니다**: `http://<HOST>:<agentPort>/api/v1/agent`. 기본 3001. 애드온 MQTT는 애드온 **네트워크 탭의 `3001/tcp` 매핑**, Matter(host_network)·Docker는 UI `설정 > Agent API`의 포트. ingress URL에 `/api/v1/agent`를 붙이면 `404`다
3. **API는 API로 켤 수 없다** — 사용자에게 UI 조작을 요청한다: 애드온 구성 탭 `agent_api_enabled` → 네트워크 `3001` 매핑 → 재시작 → UI **설정 > Agent API > 토큰 발급**
4. **토큰 평문은 1회만 표시**된다. 채팅·커밋·로그에 남기지 말고 에이전트 환경변수 `H2M_TOKEN`으로 넣게 안내한다
5. **응답 코드로 원인을 가른다**: 연결 거부=주소/포트/토글, `404`=UI 포트, `401`=토큰, `503 AGENT_API_DISABLED`=토글은 켰지만 토큰·설정 파일이 없음(`reason` 확인)

연결 확인은 토큰 없이 열리는 `GET /openapi.json` → `h2m.mjs info` 순서로 한다. `info`가 포트를 돌려주면 연결은 끝났고, `setupRequired: true`면 API가 아니라 "신규 환경" 절로 넘어간다.

## 인터페이스 — MCP가 있으면 MCP, 없으면 REST

h2m은 같은 `agent/services/*` 로직을 REST와 MCP 두 문으로 노출한다. **지금 쓸 수 있는 문으로 끝까지 간다.**

| 지금 쓸 수 있는 것                                   | 사용                                                       |
| ---------------------------------------------------- | ---------------------------------------------------------- |
| 에이전트 클라이언트에 MCP 도구가 연결됨              | MCP — `scripts/mcp.mjs` `tools` · `call`                   |
| 셸만 있음 / MCP 미지원 클라이언트                    | REST — `scripts/h2m.mjs`                                   |
| 캡처 파일 다운로드·삭제, TX `preview`, SSE `/events` | REST 전용 (MCP에 없음)                                     |
| 설정 스키마 필드 조회(`/schema`)                     | MCP `get_config_schema`(통째) 또는 REST `schema.mjs`(절단) |

- 시작점은 `h2m.mjs info`(= `/capabilities` + `/ports`). `features.packetSend`가 false면 패킷 전송이 꺼진 상태이고, MCP `tools/list`에 `send_packet`이 없는 것과 같은 뜻이다. 권한이 켜져 있어도 전송 전에 사용자 승인이 필요하다(→ "실기기 패킷 전송" 절).
- 기능·엔드포인트·도구 인자 전체 표는 `references/interfaces.md`. 낯선 배포에서는 추측 대신 `/capabilities` → `llms.txt`/`openapi.json` → MCP `tools/list` 순으로 확인한다.
- MCP 도구 실패는 JSON-RPC 오류가 아니라 `isError=true` + `{ error, message }`로 온다. `PACKET_SEND_DISABLED`, `CONFIG_NOT_LOADED`, `DRAFT_STALE`처럼 코드로 원인을 구분한다.
- 두 표면을 섞어도 된다. 단 같은 파일에 대한 초안은 `validate` 직후 받은 `draftHash`로만 `apply`한다(표면이 달라도 동일 규칙).

## 표준 절차 — 설정이 이미 있는 환경 (기본 경로)

`h2m.mjs info`가 연결 오류(`H2M_TOKEN` 없음, 연결 거부, `401`, `503 AGENT_API_DISABLED`)로 멈추면 1단계로 가지 말고 0절로 돌아간다. 1단계는 **연결이 확인된 뒤**의 절차다.

| #   | 할 일                                                                                                                                            | 통과 조건                                                                                  |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| 1   | `h2m.mjs info` · `h2m.mjs entities <portId> --full` · `h2m.mjs automations <portId>` · `h2m.mjs scripts <portId>` · `h2m.mjs unmatched <portId>` | 포트 상태, 적용 예제, 기존 엔티티·automation/script·시그니처, 미매칭 hex 목록 확보         |
| 2   | 사용자에게 힌트 확인(벤더/모델, 월패드에서 조작 가능한 기기 목록, 물리 조작 가능 여부)                                                           | 벤더명·실물 기기 대수 확보 (없으면 `gallery` 전체 목록으로 대체)                           |
| 3   | `h2m.mjs gallery <vendor>` · `gallery-match <portId> <vendor>` · `gallery-expand <file> <params>`                                                | HIT 스니펫 + `params`/채널 상한 + `auto=N scripts=M` 확인. 0건이면 다른 벤더·타입까지 확인 |
| 4   | `gallery-expand` 초안을 라이브 동일 타입 엔티티와 대조·보정(automation/scripts 포함) → `h2m.mjs analyze`                                         | 대표 hex 전부 `MINE=<id>`, `UNMATCHED` 0건. automation이 필요한데 빠뜨리지 않았는지 확인   |
| 5   | `h2m.mjs backups create <portId> before_apply --out backup.yaml`                                                                                 | 기존 설정 원본 YAML과 `filename` 확보(수정 전 필수)                                        |
| 6   | `h2m.mjs validate` → 재시작 고지·승인 → `h2m.mjs apply ... --restart`                                                                            | `valid=true` · `applicable=true` · counts/`draftHash` 확인                                 |
| 7   | 재시작 후 `h2m.mjs unmatched` · `/state` · 이벤트                                                                                                | 0건, 또는 잔여가 요청/하트비트 잡음임을 근거로 설명. 폴링/시퀀스가 실제로 도는지 확인      |
| 8   | (폴백) 3~7로도 설명 안 되는 잔여만 아래 폴백 절의 역산                                                                                           | 변동 증거가 있는 그룹만                                                                    |

미매칭이 0이면 엔티티가 이미 충분하다 — 같은 타입 확장을 더 만들지 말고 보고한다. 3→7을 한 번에 끝내려 하지 말고, 타입별(난방 → 조명 → 환기)로 끊어 적용하는 편이 안전하다.

초안 필드명이 기억나지 않으면 `node scripts/schema.mjs fields climate`로 **이 빌드의 스키마**를 확인한다(`GET /schema/homenet-bridge` — MCP 도구면 `get_config_schema`도 같은 문서를 준다). 이는 설정을 읽는 1단계에서도, 초안을 쓰는 4단계에서도 쓰는 조회다.

MCP 클라이언트라면 같은 단계를 도구로 치환한다: `info`→`list_ports`(`/capabilities`는 REST), `entities`→`get_entities`, `automations`→`get_automations`, `scripts`→`get_scripts`, `unmatched`→`get_unmatched_packets`, `history`→`get_packet_history`, `gallery-match`→`match_gallery`, `gallery-expand`→`expand_gallery_snippet`, 백업 생성→`create_backup`, 백업 다운로드→`get_backup`, 복원→`restore_backup`, 브릿지 삭제→`delete_bridge`, 스키마→`list_config_schemas`/`get_config_schema`, `analyze`→`analyze_packet`, `validate`→`validate_entity_draft`, `apply`→`apply_entity_draft`, 전송→`send_packet`(`preview`·사용자 승인 후), 재시작 후 확인→`get_unmatched_packets`. 캡처 파일을 로컬로 받아 `variance.mjs`로 볼 때만 REST(`capture get`)로 내려온다. 스키마는 MCP가 문서 전체(약 120KB)를 주므로, 필드만 빠르게 보려면 REST `schema.mjs fields`가 더 작다.

## 1. 현황 파악 — 설정을 먼저 읽는다

```bash
node scripts/h2m.mjs info                     # 포트/적용 벤더/packetDefaults/엔티티 수
node scripts/h2m.mjs entities <portId> --full # 기존 엔티티 전체 설정(구조·mask·index 원본)
node scripts/h2m.mjs automations <portId>     # 기존 automation 목록(중복 폴러/응답자 확인)
node scripts/h2m.mjs scripts <portId>         # 기존 script 목록(중복 시퀀스 확인)
node scripts/h2m.mjs unmatched <portId>       # 아직 설명되지 않는 원시 프레임
```

- `portId`가 2개 이상이면 모든 호출에 명시한다(`400 PORT_ID_REQUIRED`). 상태가 `error`인 포트는 트래픽이 없으므로 다른 포트를 고른다.
- **가장 강한 템플릿은 같은 파일의 동일 타입 엔티티다.** 여기서 `data`/`mask`/`state_*`/`command_*`/`value_index`를 복사하고 채널 인덱스만 바꾸는 것이 갤러리 스니펫을 맨바닥에서 해석하는 것보다 정확하다.
- **`/entities`는 엔티티만 보여준다.** automation/scripts는 `/automations`·`/scripts`(MCP `get_automations`/`get_scripts`)로 따로 읽는다. 초안 ID가 기존 엔티티·automation·script ID와 겹치지 않는지 세 목록으로 확인한다. 적용된 automation이 실제로 도는지는 `/events`·`/state`·`/packets/history`로 확인한다(`references/interfaces.md` §4).
- `/setup`이 `setupRequired: true`(설정 0개)면 아래 "신규 환경" 절로 먼저 브릿지 설정을 잡는다.

## 2. 사용자 힌트 — 벤더명은 탐색 순서를 정한다

작업 전에 한 번에 묶어 묻는다. 대화가 여러 번 오가면 사용자가 조작 타이밍을 놓친다.

- 벤더/모델명(아는 만큼), 단지·동·호수 규모(디바이스 대수 추정)
- **월패드·벽면 스위치에서 실제로 조작 가능한 기기 목록** — 타입별 대수와 채널 번호(예: 난방 1~3, 조명 1~5, 환기 1). 갤러리·예제의 개수 파라미터는 허용 상한이지 설치 대수가 아니므로, 이 목록이 없으면 없는 기기를 채널 확장으로 찾는 낭비가 생긴다
- 어떤 디바이스가 붙어 있는지: 난방/조명/환기/에어컨/센서 등
- 물리 조작이 가능한지: 월패드 화면, 벽면 스위치, 리모컨, 기기 자체 버튼
- HA에서 이미 보이는 엔티티와 안 보이는 엔티티

실물 목록과 관측 채널이 어긋나면 **실물 목록을 우선**한다. 예제/갤러리가 제시하는 최대 채널(`params` 상한)까지 모두 펼치지 말고, 사용자가 확인한 기기 수 + 실제로 변동이 관측된 채널까지만 확장한다.

벤더명은 **탐색 우선순위**로 쓴다. `gallery <vendor>`와 `setup/examples/<vendor>*`를 먼저 보고, 그 벤더의 스니펫 `discovery.match`로 관측 프레임을 채점한다. 이름이 틀렸을 가능성은 항상 열어 두고, 아래 신호가 나오면 힌트를 버린다.

- 그 벤더 스니펫 전체에 HIT이 0건인데 다른 벤더에는 HIT이 있음
- 사용자가 지목한 예제가 `probe.mjs` 순위에서 2위 이하로 밀림
- 적용 후 미매칭에 다른 벤더 계열 접두가 다수 남음

이때는 "○○로 알고 계시지만 관측 바이트는 △△ 프로토콜과 일치합니다(coverage 82% vs 41%)"처럼 **수치를 붙여** 알리고 확인을 받는다. 반대로 사용자가 모델명을 모르면 이름을 캐묻지 말고 `gallery` 전체 목록과 `discovery.match` 채점으로 바로 넘어간다.

## 3. 갤러리 프리셋으로 미매칭부터 없애기 (1순위 확장 수단)

`/setup/apply`는 예제에서 **설정(serial·packet_defaults)만** 복사하고 엔티티·automation·scripts는 가져오지 않는다(`selectedEntities`·`includeEntities` 전달 엄금). 적용 직후 미매칭이 남는 것은 정상이며, 대부분은 프로토콜을 몰라서가 아니라 아직 엔티티를 펼치지 않았기 때문이다. 갤러리에는 디바이스 타입별 스니펫과 개수 파라미터가 있으므로, 관측 패킷과 대조해 필요한 엔티티를 한 번에 채운다. 예제 파일의 엔티티 정의(`/setup/examples/<file>`)는 갤러리에 없는 벤더의 참고 자료로만 쓰고, 갤러리가 있으면 갤러리를 우선한다.

```bash
node scripts/h2m.mjs gallery                           # 벤더 목록: 스니펫 수/엔티티 타입/requirements
node scripts/h2m.mjs gallery <vendor>                  # 스니펫 인덱스: 파라미터 범위 + discovery.match
node scripts/h2m.mjs gallery-match <portId> <vendor>   # 관측 패킷으로 채점 → HIT + 개수 파라미터 추정치
node scripts/h2m.mjs gallery-show <vendor>/heaters_new.yaml   # 스니펫 원본 YAML
node scripts/h2m.mjs gallery-expand <vendor>/heaters_new.yaml '{"heater_count":4}' --out draft.json   # 초안으로 펼침
```

Agent API는 갤러리를 **GitHub 우선**으로 읽고, 도달 불가일 때만 컨테이너 동봉 `gallery/`를 폴백으로 쓴다. 출력 마지막 줄 `# source=local`이면 프리셋 리비전이 구버전일 수 있으니 아래 "라이브 설정에서 복사" 규칙으로 교정한다. `gallery-match`은 로그 리텐션이 켜져 있어야 채점되고, 꺼져 있으면 `UNAVAILABLE: …`을 돌려준다(에러가 아니라 안내).

`/gallery`가 없는 구버전 배포(`capabilities.features.gallery` 없음)라면 갤러리 확장을 건너뛰고 4절 폴백으로 간다. `/gallery/expand`가 `404`인 중간 버전이면 `gallery-show` 원문을 직접 펼친다. 스킬은 갤러리를 **서버 API로만** 읽는다(로컬 `gallery/`를 직접 읽는 경로는 없다).

해석 규칙:

- `HIT <file> n=<패킷수>` — `discovery.match`(data/mask)가 관측 프레임을 설명한다 → **초안에 반드시 반영**
- `auto=N scripts=M` — 스니펫이 엔티티 외에 automation/scripts를 함께 담고 있다는 뜻. `N`/`M`이 1 이상이면 `gallery-expand`의 `draft.automations`/`draft.scripts`에 어떻게 펼쳐졌는지 확인하고, 이 디바이스 동작(주기 조회·대리응답·시퀀스·복합 TX)에 필요한지 판단해 같은 초안에 넣는다. `discovery.match`가 없는 automation 전용 스니펫은 HIT에 잡히지 않으므로 이름/설명으로 확인하고, deprecated 표시가 있으면 최신 동등 스니펫을 먼저 찾는다. 판단 기준은 `references/automation-scripts.md`
- `params={"heater_count":4}` / `채널값=0x03,0x04 → max=4 (허용 1..9, 기본 4)` — `$repeat` 인덱스(`dimensions.index`)에서 관측된 최대 채널. **개수 파라미터를 정하는 근거**다
- HIT 없는 프레임은 갤러리 범위 밖 → 폴백 역산 대상
- 폴링형에서는 RX만 보지 말고 **브리지 TX 인덱스**도 채널 상한 증거다. `TX b0 00 03`이 관측되면 3번 채널 실물이 존재한다
- `STATIC n=수백`(수백 프레임 동안 1바이트도 불변, 페이로드 0 채움)은 요청/하트비트 잡음 후보다. 벤더 스니펫 전체와 대조해 HIT이 없으면 미매칭으로 남기는 것이 엔티티를 지어내는 것보다 정확하다

::: warning 새 엔티티의 바이트 원본은 "라이브 설정"에서 복사
같은 벤더라도 예제 파일(`/setup/examples/<file>`)과 갤러리 스니펫(`gallery-expand` 결과)의 프로토콜 리비전이 다를 수 있다. `gallery-expand`로 **구조(필드 조합)**를 잡고, mask/ack/버튼값 같은 **구체 바이트는 `/entities --full`의 기존 동일 타입 엔티티**에서 복사해 채널 인덱스만 바꾼다. 두 소스가 어긋나면 라이브 설정이 정답이다(그 설정으로 이미 다른 채널이 정상 파싱되고 있다).
:::

### 스니펫 → 엔티티·automation 반영 (3단계의 종료 조건)

`/gallery`·`/gallery/snippet`·`/gallery/match`는 **조회 전용**이고, `/gallery/expand`는 설정을 쓰지 않고 **초안만** 만든다. 서버가 `$repeat`/`{{i}}`와 `automation`/`scripts`를 결정적으로 펼치므로, HIT한 스니펫은 `gallery-expand`로 초안을 만들고 `/entities/validate`·`/entities/apply`로 반영한다. 이때 `gallery-match`가 알려준 **관측 채널 수**를 파라미터로 넘겨 빈 채널을 만들지 않는다(빈 채널은 미매칭을 줄이지 않고 경고만 늘린다).

1. **펼침**: `gallery-expand <vendor>/<snippet>.yaml '{"<count_param>":<관측값>}' --out draft.json` — 응답의 `parameterValues`·`counts`로 펼침 결과를 확인하고, 초안 파일을 다음 단계의 입력으로 쓴다. 서버가 없는 구버전이면 `gallery-show` 원문에서 `$repeat` 블록을 지우고 **관측 채널만** 명시 엔티티로 직접 만든다:
   - `{{i}}` → 채널 번호, `0x36` → `54`처럼 hex는 10진으로 옮긴다
   - 단순 산술은 손으로 계산한다: `{{8 + i * 2}}`(i=3 → 14), `{{0x10 + i}}`(i=3 → 19), `{{bitShiftLeft(1, i - 1)}}`(i=3 → 4)
   - folded scalar(`script: >-` 등) 안의 문자열은 hex/수식 변환 대상이 아니다 — 그대로 옮긴다
   - 예: `ezville/heaters_new.yaml` i=3 → `state_temperature_target` 스크립트의 `data[14]`, `state_heat.data/mask` `[4]`, `command_off.data` `[54, 19, 67, 1, 0]`

   결과는 YAML이 아니라 JSON 초안으로 쓴다. 필드 대응은 `references/entity-schema.md`, 형태는 `references/draft-climate-example.json`을 따른다.

2. **automation/scripts 확인**: `gallery-expand`의 `draft.automations`/`draft.scripts`와 `counts`를 먼저 본다. 스니펫의 `automation`/`scripts`가 이미 같은 봉투로 펼쳐져 있으므로 원문을 다시 계산하지 않는다. 서버 펼침이 없는 구버전에서만 `gallery-show`의 `$repeat`/`{{i}}`를 엔티티와 같은 규칙으로 직접 펼친다.
   - 엔티티 동작에 필요한 것(주기 조회, 브리지 대리응답, 상태→시퀀스, 복합 TX 생성)만 옮기고, 사용자 환경에 없는 채널용 폴링은 남기지 않는다. `gallery-expand`가 만든 자동화가 관측 채널 수(`parameterValues`)를 넘는 채널을 폴링하면 파라미터를 줄여 다시 펼친다
   - 옮기기 전에 `/automations`·`/scripts`로 같은 트리거·동작이 이미 있는지 확인한다. 같은 질의에 응답하는 폴러/응답자가 있으면 초안에서 해당 항목을 빼거나 `resolutions`/`renames`로 해결한다
   - 트리거의 `entity_id`가 펼친 엔티티 ID와 정확히 일치하는지 확인한다. 갤러리의 구형 `entity`/`to` 트리거는 현재 런타임이 읽지 않으므로 `entity_id`/`property`/`match`로 고쳐 쓴다
   - `then`과 `actions`를 동시에 쓰지 않는다(`then`이 정본). ID는 엔티티와 별도 네임스페이스이며 전체에서 유일해야 한다
   - 스니펫의 script `mode`처럼 이 빌드의 `ScriptConfig`에 없는 필드는 버린다. 남길지 판단이 서지 않으면 `references/automation-scripts.md`의 패턴 표를 본다

3. **증명**: `analyze <portId> draft.json <OFF hex> <ON hex> <값 변경 hex>` — 전부 `MINE=<new id>`, `UNMATCHED` 0건이어야 통과. `OTHER=<기존 id>`가 뜨면 시그니처가 겹치는 것이니 mask를 넓히거나 ID 중복을 의심한다. `analyze`는 **RX 매칭만** 검증하며 automation 실행은 시뮬레이션하지 않는다.

4. **적용**: `validate` → 사용자에게 재시작 영향(전 디바이스 일시 unavailable) 고지·승인 → `apply <portId> draft.json <방금 받은 draftHash> --restart`.

5. **재확인**: 재시작 후 `unmatched`. 0건이면 종료, 남으면 다른 타입 스니펫으로 1~4를 반복하고, 갤러리로도 설명 안 되는 프레임만 폴백 절로 넘긴다. automation을 넣었다면 폴링 주기·대리응답·시퀀스가 실제로 도는지 `/events`·`/state`·`/packets/history`로 확인한다.

## 4. 초안 규칙 (프리셋을 옮길 때)

- 필드명은 라이브 스키마(`node scripts/schema.mjs fields climate`, 설명까지 `--desc`)로 확인한다. `references/entity-schema.md`는 요약이며, `/schema`가 없는 구버전에서만 정본 역할을 한다. 형태는 `references/draft-climate-example.json`을 본다(YAML이 아니라 숫자 JSON 초안).
- **같은 파일의 동일 타입 엔티티를 템플릿으로 삼는다.** `state`/`command`의 필드 조합은 그대로, `data`/`mask`의 채널 인덱스만 바꾼다.
- `state`를 비우지 말 것 — `{}`는 절대 매칭되지 않는다(미매칭의 흔한 원인).
- ID는 `^[A-Za-z0-9_-]+$`, 기존과 구별되는 접두(예: `draft_`)를 붙인다.
- 타입 선택: 온도/모드 2개 이상 → `climate`, 단일 수치 → `sensor`, ON/OFF 2값 → `light`/`switch`.
- mask는 **관측된 값보다 좁게** 잡지 말 것 — ack 패킷까지 같은 엔티티로 흡수하는 벤더 프리셋 관례를 따른다(`references/heuristics.md` §3).
- `$repeat`/`{{i}}`/YAML 앵커는 초안에 남길 수 없다. 관측 채널만큼 명시적으로 펼친다.
- **초안 봉투는 `entities`(필수) + `automations`(선택) + `scripts`(선택) + `packetDefaults`(선택)** 이다. API 요청 본문은 `automations`(복수)만 받고, 설정 파일에는 `automation` 키로 기록된다(`scripts/h2m.mjs`는 로컬 초안의 `automation` 별칭도 변환해 준다). `validate`/`apply`는 이 네 필드만 본다(`references/entity-schema.md`).
- automation/scripts도 **ID가 전체에서 유일**해야 한다. 같은 ID가 이미 있으면 엔티티처럼 `resolutions`/`renames`로 해결한다. 라이브 목록은 `/automations`·`/scripts`로 먼저 확인하고, 같은 동작을 하는 automation이 다른 ID로 이미 있는지도 본다.
- automation을 넣을 때는 **엔티티 필드로 표현 가능한 일을 중복 구현하지 않는다.** 단일 상태 파싱·단일 커맨드는 엔티티에 두고, 여러 엔티티 갱신·요청/응답 시퀀스·스케줄·복합 TX만 automation/scripts로 뺀다. 패턴·금지 사례는 `references/automation-scripts.md`.
- `validate`는 automation/scripts의 **정적 스키마**(ID·필수 필드·`then`/`actions` 동시 정의·script `actions` 비어 있음)만 검사하고, script 참조가 실제로 존재하는지나 실행 결과는 검증하지 않는다. 트리거가 실제로 발화하는지는 적용 후 관측으로만 확인한다.

## 5. 증명과 적용 (모든 경로 공통)

```bash
node scripts/h2m.mjs analyze <portId> <draft.json> <hex> <hex> ...
node scripts/h2m.mjs preview <portId> <txHex> [--header] [--footer] [--no-checksum]
node scripts/h2m.mjs validate <portId> <draft.json>
```

| 출력                                    | 뜻                            | 행동                                            |
| --------------------------------------- | ----------------------------- | ----------------------------------------------- |
| `MINE=<id>={...}` 값이 관측 사실과 일치 | 초안 통과                     | 다음 hex로 확장                                 |
| `MINE=NONE OTHER=<기존id>`              | 시그니처가 기존 설정보다 좁음 | mask/index 재조정                               |
| `MINE=... OTHER=<기존id>`               | 시그니처가 겹침               | 중복 등록 여부·ID 충돌 판단                     |
| `UNMATCHED <hex>`                       | 초안으로 설명 불가            | 추측 금지. 폴백 절로 넘어가 변동 확보           |
| `preview` 결과가 실측 TX와 다름         | 커맨드 오도출                 | `data` 접두/`value_index`/`value_encode` 재검토 |

- `validate`는 `valid`/`applicable`/`errors`/`conflicts`/`discoveryPreview`와 `draftHash`, `counts`(`entities`/`automations`/`scripts`)를 준다. **counts가 의도한 개수와 맞는지 확인**한다 — `scripts`가 0인데 엔티티 `command_*`가 script를 참조하거나, `automations`가 빠진 채 적용하면 이후 동작이 조용히 실패한다.
- `analyze`는 RX 패킷이 초안 엔티티에 매칭되는지만 본다. automation/scripts는 **실행 시뮬레이션이 없으므로** `valid=true`가 곧 동작 보장이 아니다. 스케줄·상태 트리거·시퀀스는 적용 후 `/events`·`/state`·`/packets/history`로 확인한다.
- `/entities/apply`는 YAML 기록 + 백업 + **서비스 재시작**을 수행하고, 재시작 전까지 라이브 등록이 안 된다. 반드시 방금 받은 `draftHash`로만 호출하며(바뀌면 `409 DRAFT_STALE`), 재시작 영향과 `restart: false` 대안을 알리고 승인받는다. ID 충돌은 `resolutions`(`overwrite`/`skip`) 또는 `renames`로 해결한다. 적용 전에 `backups create`로 원본을 따로 확보해 두면, 결과가 기대와 다를 때 `backups restore <filename>`로 되돌릴 수 있다(복원도 재시작).
- 브릿지(YAML) 삭제는 `POST /bridges/delete`(스크립트 `delete-bridge`, MCP `delete_bridge`)만 쓴다. 삭제 전에 `backups create`로 현재 YAML을 백업하고 그 `filename`을 `backupFilename`으로 넘겨야 하며, 백업 이후 YAML이 바뀌었으면 `409 BACKUP_STALE`로 거부된다. `confirm: true`와 서비스 재시작·설정 유실 영향을 사용자에게 알리고 승인받는다. 마지막 설정을 지우면 초기 설정 마법사가 다시 열린다. 설정 파일을 직접 삭제하지 않는다.
- `/packets/send`는 실제 버스에 트래픽을 흘리는 옵트인 기능이다. `features.packetSend`가 켜져 있어도 보낼 패킷 전체(순서·간격 포함)를 `preview`로 확정해 사용자에게 보여주고 명시적 승인을 받은 뒤 승인 범위 안에서만 보낸다. 1회든 여러 패킷 시퀀스든 동일하다. 절차는 아래 "실기기 패킷 전송" 절을 따른다.

## 실기기 패킷 전송 — 미리보기 → 명시적 동의 → 승인된 시퀀스 전송 → 동작 확인

생성한 커맨드가 **실제 기기를 움직이는지** 확인할 때만 쓴다. `features.packetSend`/`send_packet` 권한은 전송을 _가능하게_ 할 뿐, 지금 보내도 된다는 동의가 아니다. `analyze`·`validate`를 대체하지도 않는다.

전송 횟수는 검증 목적에 따라 에이전트가 정한다. 한 패킷일 수도 있고, "거실→방1→방2 순서로 켠 뒤 1초 뒤 모두 끄기"처럼 여러 패킷을 순서·간격까지 정한 시퀀스일 수도 있다. 중요한 것은 **보낼 패킷 전체와 순서·간격을 미리 사용자에게 보여주고 한 번에 승인받는 것**이다.

1. **권한 확인** — `h2m.mjs info`의 `features.packetSend`가 `false`면 전송 API가 꺼진 상태다. MCP `tools/list`에 `send_packet`이 없는 것도 같다. 사용자에게 UI **설정 > Agent API > 패킷 전송 허용**을 켜 달라고 요청하고, 켜지기 전에는 `preview`까지만 한다(`references/interfaces.md` §6).
2. **hex 확정** — 보낼 `hex`는 **프레임을 제외한 payload**다. 엔티티 `command_*`에서 만든다: 정적 `{ data: [...] }`는 그 배열을 그대로, CEL 문자열 커맨드는 목표 값(`x`)과 현재 state로 평가한 바이트 배열을 쓴다. CEL을 확신 있게 평가할 수 없으면 추측하지 말고 정적 ON/OFF 커맨드부터 검증한다. 이미 관측된 TX를 그대로 재현할 때는 **프레임 전체 hex**를 header/footer 플래그 없이 `--no-checksum`으로 넘기면 바이트가 변형되지 않는다. 프레이밍은 `packetDefaults`에 맞춰 `--header`/`--footer`/`--no-checksum`을 고르고, **시퀀스의 각 패킷마다** `preview`를 돌려 최종 hex 목록을 만든다. `data` 접두·`value_index`·`value_encode`가 의심되면 §5의 preview 대조를 먼저 끝낸다.
3. **동의 요청** — 전송 전에 계획 **전체**를 보여준다: ① 포트 ② 각 대상 기기·채널 ③ 각 최종 hex ④ 전송 순서와 간격(예: ON 3개를 1초 간격 → 마지막 ON 후 1초 → OFF 3개) ⑤ 기대 동작 ⑥ 실패 시 영향(일부 기기가 켜진 채 남거나 다른 기기가 오동작할 가능성). **"이 순서와 간격으로 전송해도 될까요?"**라고 명시적으로 묻는다. 승인은 **그 계획에만** 유효하다 — 패킷·순서·간격·횟수가 바뀌면 다시 승인받는다. 대상이 불명확한 "해봐"나 이전 작업의 포괄 승인은 새 계획의 동의로 쓰지 않는다. 승인 전에는 `send`를 호출하지 않는다.
4. **승인된 시퀀스 전송** — 승인 직후 계획대로 보낸다.
   - 서로 다른 패킷: `h2m.mjs send <portId> <hex1> <hex2> ... --confirm --delay <ms>`로 승인된 순서대로 1회씩 보낸다. 중간 간격이 다르면 `sleep`으로 나눠 호출한다(예: ON 3개를 `--delay 1000`으로 보낸 뒤 `sleep 1`, OFF 3개 전송). 승인 한 건이 여러 `send` 호출을 커버할 수 있다.
   - 같은 패킷 반복: `--count N --interval <ms>`(API 상한 10). 단, toggle형 커맨드는 반복하면 상태가 뒤집히므로 쓰지 않는다.
   - 스크립트는 `--confirm` 없이는 거부하고 한 호출에 최대 10패킷만 보낸다. 전송 중 하나라도 실패하면 즉시 멈추며, 남은 패킷을 임의로 이어 보내지 않는다.
   - 전송 API에는 명령 레이트 리밋(10초당 20회)이 있다. 10패킷 시퀀스를 연달아 두 번 보내지 말고, `RATE_LIMITED`(429)가 나면 재시도로 넘기지 말고 남은 단계에서 멈춘 뒤 간격을 두고 다시 승인받는다.
5. **동작 확인 요청** — 전송 후 사용자에게 시퀀스 **전체**를 확인한다: **"거실→방1→방2 순서로 켜졌고, 1초 뒤 모두 꺼졌나요? 반응하지 않은 단계가 있나요?"** 동시에 send 응답의 `packet`/`sentCount`, `/state`의 엔티티 값 변화, `/packets/history`의 ACK/RX를 확인한다. 에이전트가 보낸 TX 자체는 history에 남지 않을 수 있으므로, 프레임을 확인해야 하면 전송 전에 `capture start`를 켠다. 결과를 구분해 보고한다: ① **기기는 움직였는데 HA 상태가 안 바뀜** = RX 파싱/mask 문제 ② **TX는 나갔는데 기기 무반응** = 프레이밍/체크섬/채널 값 문제 ③ **전송 실패** = `PORT_NOT_READY`·`PACKET_BUILD_FAILED` 등 API 오류.
6. **무반응·부분 실패면 재전송 금지** — 시퀀스 전체를 습관적으로 다시 보내지 않는다. 어느 단계에서 멈췄는지(사용자 확인 + 캡처/ACK) 좁힌 뒤 `preview`/전송 응답의 hex와 실제 프레임을 대조해 header/footer/checksum 플래그, `data` 접두, `value_index`, 채널 바이트, `value_encode`(BCD/bit)를 고친다. 수정한 계획으로 3~5단계를 다시 밟는다. 같은 hex의 반복 전송이나 채널을 훑는 브루트포스는 하지 않는다. 승인된 계획에 OFF가 포함돼 있는데 일부 기기가 켜진 채 남았다면 원상복구용 OFF를 먼저 보낸다.
7. **탐색 목적 전송 금지** — 미지의 바이트·채널을 알아내려고 `send`를 쓰지 않는다. 전송 횟수·순서도 검증 계획에 근거해야 하며, 이미 확정된 커맨드의 실기기 검증에만 쓴다. 트래픽이 필요하면 "트래픽 확보" 절의 사용자 조작 요청으로 돌아간다.

```bash
node scripts/h2m.mjs preview <portId> <hex> [--header] [--footer] [--no-checksum]
node scripts/h2m.mjs send <portId> <hex> --confirm [--header] [--footer] [--no-checksum] [--count N] [--interval ms]
node scripts/h2m.mjs send <portId> <hex1> <hex2> ... --confirm [--header] [--footer] [--no-checksum] [--delay ms]
```

승인 요청 예시(시퀀스):

> "거실→방1→방2 전등을 1초 간격으로 켠 뒤, 마지막 ON에서 1초 후 모두 끄는 6개 패킷을 보내도 될까요? 최종 hex는 각각 `…`, `…`, … 이고, 실패하면 일부 전등이 켜진 채 남을 수 있습니다. 전송 후 단계별로 실제 반응을 알려 주세요."

전송 후 확인 요청 예시:

> "승인된 순서로 6개 패킷을 전송했습니다. 거실→방1→방2 순서로 켜졌고, 1초 뒤 모두 꺼졌나요? 반응하지 않은 단계가 있으면 알려 주세요. 확인되면 결과를 정리하겠습니다."

## 신규 환경(설정 0개) — 예제 매칭도 힌트에서 시작

`/setup`의 `setupRequired: true`라면 엔티티 추가 전에 브릿지 설정을 잡는다. 사용자에게 **시리얼 주소(TCP `ip:port` 또는 `/dev/tty*`)**와 함께 벤더/모델 힌트를 받아 두면 탐색 순서를 정할 수 있다.

```bash
node scripts/probe.mjs <serialPath> [--baud 9600] [--parity none] [--stop 1] [--rounds 3]
```

`probe.mjs`의 판정 원리:

1. `POST /setup/test-serial`을 `example:"__empty__"` + 명시적 `serialConfig`으로 호출해 **벤더 편향 없는 raw 바이트**를 수집한다
2. `GET /setup/examples/<file>`로 예제의 `rx_header`/`rx_footer`/`rx_length`/`rx_checksum`을 읽고
3. 수집 바이트에 대해 예제별 프레이밍 + 체크섬 검증을 자체 수행해 **coverage(설명된 바이트 비율)**로 순위화한다
4. 체크섬을 검증할 수 없는 예제(`none`, `bestin_sum`, `samsung_xor`, crc8 계열)은 순위에서 분리해 "판정 불가"로 표시한다 — 길이 무제약 예제는 아무 바이트에서도 100%가 나오므로 추천 근거가 될 수 없다

사용자가 지목한 벤더의 예제가 상위권이면 그 예제를 우선 적용 후보로 본다. 다만 coverage 60%↑ + 2위와 30%p↑를 만족하지 못하면 적용하지 말고 수치를 보여주며 확인을 받는다. `--rounds`를 늘리거나 상태 변동을 만든 뒤 재시행한다.

::: warning `test-serial`은 벤더 판별 능력이 없다
`testSerial`은 예제의 serial 설정으로 포트만 열어 **data 이벤트 hex를 그대로** 돌려준다(`collectSerialPackets`는 `rx_checksum`/`rx_length`를 보지 않는다). TCP 브리지(`ip:port`)에서는 baud/parity가 socket에 영향 없는 경우가 많아 응답이 예제마다 동일하니, 판별은 반드시 `probe.mjs` 같은 자체 스코어링으로 해야 한다. 실제 물리 `/dev/tty*`에서는 baud/parity가 응답 자체를 바꾸므로 예제별 결과가 달라질 수 있다.
:::

> [!CRITICAL] 초기 설정(`/setup/apply` 또는 `apply_initial_setup`) 시 주의사항
> - **`selectedEntities` (또는 `includeEntities`)를 절대 넘기지 마십시오.**
> - 초기 설정의 유일한 목적은 시리얼 포트를 열어 버스 트래픽을 수신하는 것입니다.
> - 예제에 있는 엔티티를 미리 넣으면 버스에 실존하지 않는 가짜 엔티티가 생성됩니다. 모든 엔티티는 반드시 **3절 갤러리 매칭(`gallery-match`)**을 통해 실제 패킷으로 증명된 것만 추가해야 합니다.

```bash
node scripts/h2m.mjs post "/setup/apply" '{"mode":"init","example":"<winner>.homenet_bridge.yaml","serialPath":"<path>","portId":"<portId>","restart":true}'
```

- `mode:"init"`은 설정이 0개일 때만(`409 SETUP_NOT_REQUIRED` 방지). 이미 로드된 환경의 신규 포트는 `mode:"add"` + 미사용 `portId`
- **`/setup/apply`는 오직 설정(serial·packet_defaults)만 복사해야 한다.** `selectedEntities`나 `includeEntities`는 절대 넘기지 않는다. 예제의 엔티티·automation·scripts는 들어가지 않으므로, 적용 직후 미매칭이 남는 것은 정상이다. 재시작 후 3절 갤러리 확장으로 엔티티를 채운다.
- 재시작 후 `/ports`(status=started), `/state`, `/packets/history`, `/packets/unmatched`를 확인한다
- **예제 수는 실제 디바이스 수와 무관하다.** 갤러리 `params` 상한과 관측 채널을 근거로 필요한 만큼만 펼친다 → 3절 갤러리 확장으로 넘어간다
- MCP에서는 `get_setup_state` → `get_setup_example` → `test_setup_serial` → `apply_initial_setup`(`mode:"init"|"add"`)으로 같은 흐름을 만든다(`includeEntities`/`selectedEntities` 절대 금지). 설정 0개 판정과 `loadedPortIds` 확인도 이 도구들로 끝난다
- MQTT 접속 정보(브로커 주소/계정)는 config가 아니라 환경변수/애드온 옵션이므로 API로 설정 불가

## 트래픽 확보 — 홈넷은 조작해야 말한다

엔티티 확장(3절)은 이미 들어오는 프레임으로 대부분 끝난다. 하지만 채널 상한 판단이나 폴백 역산에는 **변동이 있는 트래픽**이 필요하다. 관측을 위해 `send`로 트래픽을 만들지 않는다 — 전송은 확정된 커맨드의 실기기 검증 전용이다. 먼저 이 버스가 폴링형인지 이벤트형인지 가른다(캡처를 직접 켜지 않아도 된다):

```bash
node scripts/h2m.mjs capture wait <portId> 60 5
```

- `TRAFFIC +N패킷` — 폴링형. 방치해도 프레임이 쌓인다
- `NO_TRAFFIC`(exit 3) — **조작 시에만 오가는 버스**일 가능성이 높다. 여기서 기다리지 말고 즉시 사용자에게 요청한다:

  > "월패드에서 **실제로 조작 가능한 기기 목록**을 먼저 알려 주세요(예: 조명 3개, 난방 2개, 환기 1개). 그다음 ① 1번 전등 ON → 5초 → OFF ② 난방 목표온도를 2~3단계 바꿔 주세요 ③ 환기팬 모드를 한 번 바꿔 주세요. 조작 전에 말씀해 주시면 제가 캡처를 켜겠습니다."

  목록은 확장 범위를 정하고, 조작 요청은 그 목록 안의 기기로만 한다(없는 기기를 조작하려다 왕복이 늘어난다). 요청은 대상·동작·순서·유지시간을 명시하고, 여러 개를 동시에 켜지 않게 한다(어느 채널인지 구분 불가).

`NO_TRAFFIC`과 `무배선`은 다르다. `capture wait`이 0건이면 RX뿐 아니라 TX도 한 프레임 없는 상태다. `/ports` status가 `started`인데도 아무것도 안 오가면 배선/브릿지 경로(터미널 서버 대역폭, 포트 충돌)를 먼저 의심하고, `error`/`stopped`면 시리얼 주소·프레이밍 단계로 되돌아간다. 둘 다 아니어야 이벤트형으로 취급한다.

::: warning 무트래픽 판정은 원시 프레임 기준
`/packets/history`는 **엔티티에 매칭된 패킷만** 담는다. 설정이 아직 없는 환경에서 history로 "트래픽 없음"을 판단하면, 미매칭 프레임이 계속 들어오는데도 조용한 버스로 오인한다. `capture wait`은 `/capture`의 `packetCount`(원시 프레임)를 본다.
:::

변동이 필요한 경우 캡처를 열고 조작 전후를 대조한다:

```bash
node scripts/h2m.mjs capture start <portId> all
# 사용자 조작 (또는 폴링 대기)
node scripts/h2m.mjs capture stop <portId>
node scripts/h2m.mjs capture files
node scripts/h2m.mjs capture get <filename> cap1.txt
node scripts/variance.mjs cap1.txt --length <rx_length>
# 2차 캡처 후
node scripts/variance.mjs cap2.txt --base cap1.txt --length <rx_length>
```

- `uniq=N varyBytes=[i,j]` — 변하는 바이트가 데이터 필드 후보, 접두는 디바이스/타입 식별자 후보
- `STATIC n=…` — 필드 의미 확정 불가 신호. 이 항목이 많을수록 조작 요청이 필수다
- 이벤트형 버스는 사용자 조작 1회가 1차·2차 캡처를 겸한다. 조작 직전에 캡처를 켜고 조작 순서를 메모해 두면 `--base` 없이도 시간순으로 필드가 전개된다
- **캡처는 서비스 전역 1개다.** `capture start <portId>`의 `portId`는 서버가 무시하므로(파일 메타에는 첫 포트 serial만 기록) 포트별로 나눠 찍을 수 없다. 멀티포트에서는 다른 포트의 프레임도 같은 파일에 섮인다 — 원하는 포트의 트래픽만 변동했는지는 `variance.mjs`의 접두 그룹으로 가른다

## 폴백 — 예제·갤러리에도 없는 디바이스만 직접 역산

3~4절로 설명되지 않는 프레임(갤러리 HIT 0건 + 동일 타입 기존 엔티티와 접두가 다름)에만 적용한다. 이 절차는 **변동 증거가 전제**다.

### 1) 기준선과 상태 변동

```bash
node scripts/h2m.mjs capture wait <portId> 60 5   # 폴링형/이벤트형 판정
node scripts/h2m.mjs capture start <portId> all
# (이벤트형이면 사용자 조작 요청) 60~120초
node scripts/h2m.mjs capture stop <portId>
```

STATIC만 나오면 추측하지 말고 위 "트래픽 확보" 절의 조작 요청으로 돌아간다. 폴링형이라도 폴링은 *현재값*만 반복하므로, 조작이 없으면 모드/액션 비트는 존재 자체가 관측되지 않는다.

요청 예시(한 번에 묶어서, 순서와 유지 시간 명시):

- 히터/에어컨: 전원 ON → 목표 온도 2~3단계 변경(각 5초 유지) → OFF
- 조명: 1번만 ON → 5초 → OFF, 그 다음 2번 (여러 개 동시 조작 금지)
- 센서: 값이 실제로 변하도록 환기/냉방
- 미상 계열(`0f`/`8f` 등): 해당 장치를 직접 조작 가능하면 요청

### 2) 레이아웃·인코딩 확정

- **체크섬**: 마지막 바이트가 앞 바이트 합(`add`)인지 xor인지 검증. 어긋나면 `_no_header` 변형, `rx_checksum2`(2바이트), footer 포함 여부를 순서대로 의심
- **index 좌표계**: `rx_header`가 비어 있으면 패킷 절대 바이트 위치, 있으면 헤더 이후 상대 위치
- **BCD**: `0x25`→25, `0x13`→13처럼 hex 표기가 곧 10진으로 읽히면 `decode: bcd`
- **채널 바이트**: 접두가 같은 그룹에서 한 바이트만 `01..0N`으로 도는 패턴은 디바이스 인덱스
- **RX/TX 쌍**: `RX 30 0i` 쿼리에 곧바로 `TX b0 00 i`가 따라오면 자동화/브리지 응답이지 엔티티 상태가 아니다

### 3) 최소 초안 → 증명

4~5절과 동일하게 `analyze` → `preview` → `validate` → 승인 → `apply`. 프리셋이 없는 영역이므로 필드를 최소로 잡고, 관측되지 않은 하위 상태(action/heating 등)는 아예 정의하지 않는다(unknown으로 보이는 편이 오매칭보다 안전).

## 보고

| 패킷 그룹   | 근거(프리셋/예제/역산) | 변동                | 도출 필드               | 상태 파싱 | TX preview | automation/scripts      | validate   |
| ----------- | ---------------------- | ------------------- | ----------------------- | --------- | ---------- | ----------------------- | ---------- |
| 예시 그룹   | gallery heaters_new    | byte1 bit0, byte3/4 | `state_off`, 온도 `bcd` | 일치      | 일치       | 주기 조회 1개(`auto=1`) | applicable |
| 미해결 그룹 | 없음(STATIC)           | 없음                | 확정 불가               | -         | -          | 해당 없음               | -          |

미해결 항목을 성공 항목과 섞어 보고하지 말 것. 어떤 근거(프리셋/예제/역산)로 만든 엔티티인지도 함께 적는다. automation/scripts를 추가했다면 **무엇을 왜 넣었는지**(예: "상태가 스스로 갱신되지 않아 30초 주기 조회 추가", "현관벨 상태 → 3초 지연 후 문 열기")와 적용 후 실제 발화 여부를 함께 적는다. 실기기 전송으로 검증했다면 승인받은 계획(패킷·순서·간격)과 실제 전송 횟수, 사용자 확인 결과(동작함/무반응/부분 실패)를 적고, 무반응이면 재전송하지 않고 교정 계획을 보고한다.

## 도구

```bash
export H2M_URL="http://<H2M-HOST>:3001/api/v1/agent"   # Agent API 전용 포트 (UI 포트 아님) — 주소를 모르면 0절
export H2M_TOKEN="<설정 > Agent API에서 발급한 토큰>"   # 채팅·커밋·로그에 남기지 않는다
cd <skill-dir>   # 이 SKILL.md가 있는 디렉터리
node scripts/h2m.mjs info
node scripts/mcp.mjs tools   # MCP 도구 목록 = 이 배포에서 가능한 작업
```

- `scripts/h2m.mjs` — REST 래퍼. `info|setup|get|post|entities|automations|scripts|unmatched|history|capture(start|stop|status|wait|files|get|delete)|gallery|gallery-show|gallery-match|gallery-expand|backups(list|create|get|restore)|delete-bridge|analyze|validate|apply|preview|send`. `preview <portId> <hex> [--header] [--footer] [--no-checksum]`는 최종 프레임을 보여주고, `send <portId> <hex> [<hex> ...] --confirm ...`는 실제 전송이다. 단일 hex는 `--count N --interval ms`로 같은 패킷을 반복하고, 여러 hex는 `--delay ms` 간격으로 승인된 순서대로 1회씩 보낸다(한 호출 최대 10패킷, `--confirm` 필수 — 미리보기·사용자 승인 없이는 쓰지 않는다). `automations`/`scripts`는 기존 automation/script 목록과 config를 읽는다. `gallery-expand <file> [paramsJson] [--out draft.json] [--port portId]`는 서버에서 `$repeat`/`{{i}}`와 automation/scripts를 펼쳐 초안을 만든다. `backups create [portId|-] [reason] [--out file.yaml]`는 수정 전 원본 YAML을 확보하고, `backups get <filename> [outfile]`·`backups restore <filename> [--no-restart]`로 내려받거나 되돌린다(복원은 `confirm=true`를 자동 포함). `delete-bridge <portId|-> --backup <filename> --confirm [--config-file <file>]`는 백업이 현재 YAML과 일치할 때만 YAML을 삭제하고 재시작한다. `analyze`/`validate`/`apply`는 초안의 `entities`·`automations`(`automation` 별칭 포함)·`scripts`·`packetDefaults`를 그대로 전달한다. `gallery <vendor>` 출력의 `auto=N scripts=M`으로 automation/scripts 보유 여부를 먼저 거른다
- `scripts/schema.mjs` — 이 빌드의 설정 JSON 스키마 조회(Agent API `GET /schema/homenet-bridge`, Bearer 토큰; MCP `get_config_schema`가 같은 문서). `list` · `types` · `fields <type|Def> [--desc|--json]` · `def <Def>`. 120KB 전체를 덤프하지 않고 정의 단위로 잘라 본다 — 필드명·enum·required의 정본
- `scripts/mcp.mjs` — MCP JSON-RPC 클라이언트(stateless). `tools`(도구+필수 인자) · `call <tool> [json|@file] [--max N]`(기본 전체 출력) · `raw <method> [json]` · `init`. 도구 인자 표는 `references/interfaces.md`
  - MCP에 없는 기능(캡처 파일 다운로드·삭제, TX `preview`, SSE `/events`)은 같은 토큰으로 `h2m.mjs`(REST)를 쓴다
- `scripts/probe.mjs` — 신규 환경 예제 자동 매칭. raw 수집 → 예제별 프레이밍/체크섬 자체 검증 → coverage 순위화
- `scripts/variance.mjs` — 캡처 로그 그룹별 변동 분석(`--base`, `--length`, `--prefix`, `--show`)
- 순수 ESM, 외부 의존성 없음, node 18+ 필요(`fetch` 내장). `node`가 PATH에 없는 환경에선 해당 런타임 경로를 직접 지정한다
- rate limit 분당 120회 — `capture wait`의 폴링 간격은 5초 이상 유지하고 `capture status`를 난사하지 말 것

## Resources

- `references/connection-setup.md` — 주소·토큰을 모르는 사용자용 안내(설치 형태별 주소, Agent API 활성화·토큰 발급, 연결 확인, 증상별 진단)
- `references/entity-schema.md` — 타입별 필드 요약(정본은 라이브 `/schema`), 매칭 로직, YAML→JSON 변환
- `references/automation-scripts.md` — 갤러리에서 automation/scripts가 쓰이는 패턴(주기 폴링·대리응답·상태 시퀀스·복합 TX), 초안 봉투, 트리거/액션 의미론, 구형 트리거·`low_priority`·`update_state` 함정
- `references/heuristics.md` — 프리셋 우선 규칙, 체크섬·mask·ack·BCD·정적 버스·glued 패킷·API 제약에 대한 실측 판정 규칙과 함정
- `references/draft-climate-example.json` — `analyze`/`validate` 통과가 검증된 climate 초안 샘플(형태 참고용)
- API 규약: `GET /openapi.json`(API 스펙), `GET /llms.txt`(요약), 설정 스키마는 `GET /schema/homenet-bridge`(`scripts/schema.mjs`)
- 배포 문서: <https://homenet2mqtt-docs.vercel.app/> — 스킬 범위 밖(UI·설치·고급 설정)의 최신 안내가 필요할 때 해당 페이지만 읽는다. 버전이 어긋나면 라이브 API가 우선
- `references/interfaces.md` — 시스템 지도(core/service/ui/simulator/gallery), REST 엔드포인트·MCP 도구 전체 표, MCP에 없어 REST로 내려와야 하는 기능, API로 불가능해 사용자에게 요청할 것
