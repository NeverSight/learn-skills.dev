---
name: jpushare
description: JPUShare(share.jedutools.io)에 사용자 대신 GPU 작업을 제출하고 상태·로그·결과를 받으며, 연구실 저장 공간에 파일을 올리고 내려받는다. 키 발급·연구실 가입·관리자 기능은 다루지 않는다. 사용자가 "JPUShare에 작업 올려줘", "GPU 작업 결과 받아줘", "JPUShare 저장 공간에 업로드해 줘", "GPU 서버 상황 알려줘"처럼 JPUShare 작업·저장 공간·GPU 서버·대기열을 부탁할 때 쓴다. 사용자가 웹에서 발급한 API 키(환경 변수 JPUSHARE_API_KEY)가 필요하다.
---

# JPUShare

JPUShare는 여러 연구실이 GPU 서버를 함께 쓰는 서비스다. 연구실마다 구성원과 저장 공간을 따로 두고, GPU 서버와 실행 순서는 모든 연구실이 함께 쓴다. 제출한 작업은 다른 연구실의 작업과 함께 순서를 기다린다.

- 허용 범위별 경로, 저장 위치 조합, 멀티파트 업로드, 전체 오류 표: [references/api.md](references/api.md)
- 사람용 안내(이 스킬과 어긋나면 이쪽이 맞다): 에이전트 연결하기 https://jhelper.jedutools.io/JPUShare/2Agent/1Connect , API 사용법 https://jhelper.jedutools.io/JPUShare/2Agent/2API

## 1. 시작 전 확인

```bash
: "${JPUSHARE_API_KEY:?JPUSHARE_API_KEY 가 비어 있습니다 — 사람에게 키를 받는다}"   # 키는 덮어쓰지 않는다
export BASE=https://share.jedutools.io
```

`JPUSHARE_API_KEY`가 비어 있으면 작업을 시작하지 말고 사람에게 안내한다.

1. JPUShare(https://share.jedutools.io) → **내 정보/설정** → **API 키 발급**에서 필요한 허용 범위만 골라 발급한다. 연결 확인에는 `account:read`, 작업 제출·결과 받기에는 `platform:read`·`jobs:read`·`jobs:submit`이 필요하다. 권한이 큰 범위는 **키 허용 범위 확인** 창에서 **확인 후 발급**을 누른다.
2. 터미널에서 `export JPUSHARE_API_KEY='jpk_...'`를 실행하고 **그 터미널에서 에이전트를 다시 시작**한다.

키는 에이전트가 만들 수 없다(`/v1/api-keys`는 웹 로그인 전용). 사람이 키를 채팅에 붙여 넣으면 "대화 기록에 남으니 export 뒤 다시 시작하는 편이 안전합니다"라고 한 번 권하고, 그대로 진행하라고 하면 명령에만 넣어 쓴다.

연결을 확인한다. 모든 호출에 `Authorization: Bearer $JPUSHARE_API_KEY`를 붙인다.

<!-- doc-exec: C01 expect=200 -->

```bash
curl --fail-with-body "$BASE/v1/me" -H "Authorization: Bearer $JPUSHARE_API_KEY"
```

- 200: `username`, `lab`, `actions`(이 키로 할 수 있는 동작)를 사람에게 짧게 알린다. `lab`이 비어 있으면 연구실 소속이 없어 작업을 낼 수 없다 → 웹에서 참가를 신청하고 책임교수 또는 연구실 관리자의 승인을 받게 한다.
- 401: 키가 만료·폐기됐거나 잘못 복사됐다 → 새 키를 요청한다.
- 403 `API_KEY_SCOPE_REQUIRED`: `account:read`가 없다 → 그 범위를 넣은 새 키를 요청한다.

## 2. 작업 제출 워크플로

아래 체크리스트를 응답에 옮겨 적고 단계마다 표시한다.

```
- [ ] 1. GPU 서버와 실행 환경 고르기
- [ ] 2. 입력 데이터 올리기(필요할 때만)
- [ ] 3. 코드 ZIP 만들고 제출하기
- [ ] 4. 종료 상태까지 기다리기
- [ ] 5. 로그와 결과 받기
```

### 1단계 — GPU 서버와 실행 환경

`GET /v1/tiers`로 GPU 서버(`name`, `compute_capability`)를, `GET /v1/workspace-profiles`로 실행 환경(`current_snapshot_id`, `supported_compute_caps`)을 받는다. `supported_compute_caps` 중 GPU 서버의 `compute_capability`와 점 앞 숫자가 같고 점 뒤 숫자가 그 이하인 값이 있는 환경만 쓴다. 둘 중 하나라도 `null`이면 서버가 판정하지 않고 받아 준다.

출력: `TIER`(고른 GPU 서버의 `name`), `SNAPSHOT_ID`(그 환경의 `current_snapshot_id`). 3단계 예제의 `jpu-60`·`$SNAPSHOT_ID` 자리에 이 값을 넣는다.

### 2단계 — 입력 데이터 업로드 (storage:write)

위치는 `scope`(`shared`=연구실 공유, `private`=내 폴더)와 `folder`(`data`·`result`) 조합으로 정한다. 256 MiB 이하는 주소 발급 + PUT 두 단계다. `content_length`는 정확한 바이트 수다.

<!-- doc-exec: C03 expect=200 -->

```bash
curl --fail-with-body "$BASE/v1/storage/upload-url" \
  -H "Authorization: Bearer $JPUSHARE_API_KEY" -H 'Content-Type: application/json' \
  -d '{"scope":"shared","folder":"data","key":"train/sample.csv","content_length":1234}' \
  -o upload.json
UPLOAD_URL=$(jq -r .url upload.json)
UPLOAD_TAGGING=$(jq -r '.headers["x-amz-tagging"]' upload.json)
```

응답 `headers`의 모든 항목을 PUT에 빠짐없이 붙인다.

<!-- doc-exec: C04 expect=200 -->

```bash
curl --fail-with-body -X PUT "$UPLOAD_URL" -H "x-amz-tagging: $UPLOAD_TAGGING" --data-binary @sample.csv
```

헤더를 빠뜨리면 저장소가 XML 403으로 거절한다.

<!-- doc-exec: C05 expect=403 -->

```bash
curl -sS -X PUT "$UPLOAD_URL" --data-binary @sample.csv   # 잘못된 예 → 403 SignatureDoesNotMatch|AccessDenied
```

256 MiB를 넘으면 `upload-url`이 400 `MUST_USE_MULTIPART`를 준다 → [references/api.md](references/api.md)의 멀티파트 절차를 따른다.

### 3단계 — 제출 (jobs:submit)

`POST /v1/jobs`는 `multipart/form-data`다. 코드는 `artifact`(ZIP, 500 MiB 이하)와 `git_url`(+`git_ref`) 중 하나만 준다.

<!-- doc-exec: C07 expect=200 -->

```bash
curl --fail-with-body "$BASE/v1/jobs" \
  -H "Authorization: Bearer $JPUSHARE_API_KEY" \
  -F 'artifact=@code.zip' \
  -F 'command=python' \
  -F 'args=["main.py"]' \
  -F 'name=에이전트 제출 예제' \
  -F 'work_type=training' \
  -F 'description=jpushare 스킬 예제' \
  -F 'tier=jpu-60' \
  -F "workspace_snapshot_id=$SNAPSHOT_ID" \
  -F 'timeout_seconds=3600' \
  -F 'result_location=private' \
  -F 'channels=[{"name":"train","scope":"shared","folder":"data","prefix":"train/","size_gb":1}]' \
  -o job.json
JOB_ID=$(jq -r .job_id job.json)
```

- `description`(작업 목적, 500자 이내)은 필수다. 사람이 말한 목적을 한 줄로 적는다.
- `args`·`channels`는 JSON 문자열이다. `channels[].name`은 코드에서 `JOB_CHANNEL_<이름>` 환경 변수로 읽는다.
- `result_location`은 `shared` 또는 `private`다. 코드는 결과를 `/output` 아래에 써야 회수된다.
- `timeout_seconds`는 60~259200이다. GPU 수는 GPU 서버가 정한다.

### 4단계 — 종료 상태까지 기다리기 (jobs:read)

`GET /v1/jobs/{id}`를 5~10초 간격으로 불러 `state`를 본다. 대기가 길어도 실패가 아니다 — 다른 연구실의 작업과 함께 순서를 기다리는 중이다.

<!-- doc-exec: C08 expect=200 -->

```bash
curl --fail-with-body "$BASE/v1/jobs/$JOB_ID" -H "Authorization: Bearer $JPUSHARE_API_KEY"
```

- 진행 중: `USER_QUEUE_WAIT`·`GLOBAL_QUEUE_WAIT`·`ESCALATION_WAIT`(대기), `ASSIGNED`, `RUNNING`, `CANCEL_REQUESTED`.
- 종료 상태(10개, 이후 바뀌지 않음): `SUCCEEDED`, `FAILED_RUNTIME`, `FAILED_ENV`, `FAILED_OOM_CONFIRMED`, `FAILED_OOM_SUSPECT`, `TIMED_OUT`, `CANCELLED`, `KILLED_BY_ADMIN`, `FAILED_SUBMISSION`, `UPLOAD_FAILED`.
- `SUCCEEDED`가 아니면 `last_error_code`와 `last_error_message`(콘솔의 "실패 사유")를 사람에게 전하고 stderr 로그를 읽어 원인을 설명한다. 준비 단계에서 실패한 작업(`FAILED_ENV` 등)은 로그가 없을 수 있다(404 `NO_ATTEMPT`) → `last_error_message`만 전한다.

### 5단계 — 로그와 결과

<!-- doc-exec: C10 expect=200 -->

```bash
curl --fail-with-body "$BASE/v1/jobs/$JOB_ID/results" -H "Authorization: Bearer $JPUSHARE_API_KEY"   # objects[].url = 임시 주소
```

```bash
curl --fail-with-body "$BASE/v1/jobs/$JOB_ID/results-zip" -H "Authorization: Bearer $JPUSHARE_API_KEY" -o results.zip   # 완료된 작업, 2 GiB까지
curl --fail-with-body "$BASE/v1/jobs/$JOB_ID/log?stream=stderr" -H "Authorization: Bearer $JPUSHARE_API_KEY"         # stdout 은 stream=stdout
```

결과에는 `/output` 아래 파일과 `logs/stdout.log`·`logs/stderr.log`·`exit_code.txt`가 있다. `url`은 만료되므로 필요할 때 목록을 다시 받는다. 결과는 작업이 끝나고 30일 뒤 정리된다.

## 3. 그 밖의 호출

- GPU 서버 현황: `GET /v1/tiers`, `GET /v1/workers`. 내 대기열: `GET /v1/queue`(`queue:read`). 점검 상태: `GET /v1/maintenance/status`(인증 불필요).
- 파일 목록: `GET /v1/storage/objects?scope=…&folder=…&prefix=…`. 다운로드 주소: `GET /v1/storage/objects/{key}/url?scope=…&folder=…`(둘 다 `storage:read`).
- 취소: `POST /v1/jobs/{id}/cancel`(`jobs:cancel`) — 사람이 확인한 뒤에만 부른다.

## 4. 오류가 나면

HTTP 상태와 본문을 함께 보고 분기한다. 일반 오류는 `code`, 제출 검증 오류는 `status:"VALIDATION_FAILED"`와 `errors[].code`, 점검 중 503은 `error` 값을 본다. 자주 만나는 것만 적는다. 전체 표는 [references/api.md](references/api.md)에 있다.

| 상태·코드 | 대응 |
|---|---|
| 401 | 새 키를 요청한다 |
| 403 `API_KEY_SCOPE_REQUIRED` | 필요한 범위를 넣은 새 키를 요청한다 |
| 403 `JWT_REQUIRED` | 키로 부를 수 없는 경로다. 키로 다시 시도하지 않는다 |
| 403 `NO_LAB` | 연구실 소속이 없다 → 웹에서 참가 승인부터 받게 한다 |
| 400 `VALIDATION_FAILED` + `WORKSPACE_GPU_INCOMPATIBLE` | 1단계 호환 조건에 맞는 실행 환경이나 GPU 서버로 바꾼다 |
| 400 `VALIDATION_FAILED` + `WORKER_ACCOUNT_MISSING` | 다른 GPU 서버로 내거나 잠시 뒤 다시 낸다. 반복되면 운영자 확인을 요청한다 |
| 400 `DESCRIPTION_REQUIRED` | 작업 목적을 `description`에 적어 다시 낸다 |
| 429 | `Retry-After` 헤더만큼 기다린다. 전역 제한의 본문은 평문이라 JSON으로 파싱하지 않는다 |
| 503 `SERVICE_MAINTENANCE` | `GET /v1/maintenance/status`로 끝난 것을 확인한 뒤 다시 한다 |

범위가 모자란 키의 거절 예:

<!-- doc-exec: C11 expect=403 -->

```bash
# READONLY_API_KEY = account:read 만 가진 다른 키(설명용 — 이런 키로 제출하면) → 403 API_KEY_SCOPE_REQUIRED
curl -sS "$BASE/v1/jobs" -H "Authorization: Bearer $READONLY_API_KEY" -F 'command=python' -F 'tier=jpu-60'
```

## 5. 판단 규칙

- 키 발급·폐기는 사람이 한다. 만료되거나 범위가 모자라면 사람에게 요청한다.
- 필요한 범위만 요청한다. 읽기만 할 거면 쓰기 범위를 달라고 하지 않는다.
- 삭제·취소·대기열 순서 변경은 사람이 확인한 뒤에만 한다. 삭제·이동·복사 전에는 짝이 되는 `*-preview` 경로([references/api.md](references/api.md)의 범위 표)로 영향 범위를 먼저 보여 준다.
- 키 원문을 파일·로그·보고·커밋에 쓰지 않는다.
- `/v1/llm/*`는 부르지 않는다(503 `LLM_DISABLED`).
