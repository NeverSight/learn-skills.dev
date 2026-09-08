---
name: codex-image
description: "OpenAI Codex CLI(`codex exec`)의 내장 `image_generation` 툴로 이미지를 생성하는 스킬. 단일/배치/병렬 생성 지원. 핵심 강점은 **최대 5장 동시 병렬 생성** (실측 직렬 대비 2.4~2.85배 속도). ChatGPT OAuth 로 인증되어 별도 OPENAI_API_KEY 호출 코드가 필요 없다. 사용 시점: 사용자가 'codex 로 이미지', 'codex imagegen', 'codex 이미지 생성', '병렬 이미지 생성', '여러 장 이미지 동시', '이미지 N장 한번에', '배치 이미지 생성', 'imagegen 병렬', 'codex 그림' 등을 언급할 때, 또는 동시에 3장 이상을 빠르게 만들어야 하는 모든 경우. 단, 단순 단일 이미지·고해상도(2K+)·정밀 마스킹 편집·멀티 레퍼런스 합성은 `gpt-image2` 또는 `gemini-3-pro-imagegen` 스킬이 더 적합. ChatGPT 웹/앱이나 직접 OpenAI API 호출은 이 스킬의 범위가 아니다."
---

# Codex Image Generation (병렬)

OpenAI Codex CLI 의 내장 `image_generation` 툴을 활용해 **최대 5장까지 이미지를 동시에 생성**하는 스킬. (codex-cli 0.128 / 2026-05 실측 기준)

## 왜 이 스킬인가

- **병렬 처리**: `codex exec` 를 백그라운드 N개로 띄우면 OpenAI 서버가 N개를 동시 처리. 5장 동시 시 직렬 대비 약 2.85배 빠름 (실측: 직렬 추정 450초 → 병렬 158초).
- **인증 단순화**: codex 가 ChatGPT OAuth 로 이미 로그인돼 있으면 별도 OPENAI_API_KEY · Python SDK · curl 스크립트가 모두 불필요. 단순 자연어 프롬프트 한 줄로 끝.
- **워크스페이스 통합**: 결과 PNG 가 지정 디렉토리에 자동 저장 (codex 가 `~/.codex/generated_images/<session>/` 에서 작업 폴더로 복사).


## 사전 점검

```bash
codex --version           # 0.128+ 권장
codex login status        # "Logged in using ChatGPT" 확인
codex features list | grep image_generation   # stable / true 인지 확인
```

미로그인 시 `codex login` 실행을 사용자에게 요청. 이 스킬 호출 전에 한 번만.

## 핵심 패턴 1 — 단일 이미지 (베이스라인)

```bash
codex exec \
  --sandbox workspace-write \
  --skip-git-repo-check \
  --cd <work_dir> \
  -o /tmp/codex-img-single.md \
  "이미지 생성 도구로 '<프롬프트>' 이미지를 생성하고 ./<출력>.png 로 저장. 파일 경로만 한 줄로 보고."
```

- 평균 소요: 약 **80~110초/장** (모델 응답 분산 큼)
- 기본 해상도: 1254×1254 또는 1536×1024 — codex 가 프롬프트에 따라 자동 결정
- 해상도 강제는 어려움. 정확한 해상도가 필요하면 `gpt-image2` 사용

## 핵심 패턴 2 — N장 병렬 (N ≤ 5)

**Bash `run_in_background: true` 로 동일 명령을 N개 띄운다.** 핵심은 출력 파일명을 다르게 하는 것.

```bash
# 한 메시지 안에서 5개 Bash 도구 호출을 동시에 실행
codex exec --sandbox workspace-write --skip-git-repo-check --cd <work_dir> \
  -o /tmp/codex-img-1.md \
  "이미지 생성 도구로 '<프롬프트1>' 이미지를 생성하고 ./<output1>.png 로 저장. 경로만 한 줄로 보고."
# ... 같은 패턴으로 2~5번째도 run_in_background: true 로 띄움
```

각 작업은 독립 codex 세션이므로 진정한 병렬. 완료 알림은 백그라운드 작업 통지로 자동 수신 — `sleep` 폴링 금지.

### 실측 (2026-05 기준)

| 동시 작업 수 | 가장 느린 작업 wall-clock | 직렬 대비 |
|---|---|---|
| 1장 | 89.7초 | 1.00× |
| 3장 | 110.9초 | 2.43× |
| 5장 | 158.5초 | 2.84× |

5장이 3장보다 가장 느린 작업이 ~47초 늘어남. 큐잉 흔적이지만 명확한 직렬화는 없음.

## 핵심 패턴 3 — N > 5 배치 처리

ChatGPT 플랜의 동시 요청 한도와 안정적 응답 시간을 고려해 **5개씩 묶어 순차 배치**를 권장.

```bash
# 12장 = 5 + 5 + 2 의 3배치
# 배치1: 5개 동시 → 완료 대기
# 배치2: 다음 5개 동시 → 완료 대기
# 배치3: 마지막 2개 동시
```

배치 헬퍼 스크립트는 `scripts/codex_imagegen_batch.sh` 참고.

## 헬퍼 스크립트

`scripts/codex_imagegen_batch.sh` — 최대 5개씩 묶어 자동 배치 실행.

```bash
# 사용법
~/.claude/skills/codex-image/scripts/codex_imagegen_batch.sh <work_dir> \
  "프롬프트1::output1.png" \
  "프롬프트2::output2.png" \
  "프롬프트3::output3.png" \
  ... 임의 개수
```

- 입력 N개를 받아 **5개씩 동시 실행**, 한 배치가 끝나면 다음 배치 시작
- 모든 출력 PNG 가 `<work_dir>/` 에 저장됨
- 각 작업의 codex 최종 메시지는 `<work_dir>/.codex-imagegen-logs/` 에 보관

## 결과 검증

생성 후 항상 파일을 확인.

```bash
file <work_dir>/*.png
ls -la <work_dir>/*.png
```

- 0 바이트 / 손상 PNG 가 나오면 그 작업만 재시도
- codex 가 "이미지 생성 도구를 못 찾음" 류 응답을 내면 `image_generation` 피처가 비활성화된 것 — `codex features list` 확인

## 비용·플랜 주의

- 각 호출은 독립 codex 세션 → 토큰 사용량은 N배.
- ChatGPT Plus/Pro 플랜의 시간당 메시지 한도가 N개씩 차감.
- 헤비 배치(20장+) 전에는 `codex login status` 로 플랜 확인.
- 세션은 `~/.codex/sessions/` 에 저장. 일회성·민감 데이터는 `--ephemeral` 추가.

## 안티패턴

- **`codex exec` 에 `--ask-for-approval` 부착** — 비대화형이라 즉시 에러 종료.
- **포그라운드로 N개 직렬 실행** — 병렬 효과를 얻지 못함. 항상 `run_in_background: true`.
- **`sleep` 으로 완료 대기** — 백그라운드 통지가 자동으로 옴. 폴링 금지.
- **6개 이상 한 배치** — 큐잉으로 응답 시간 분산이 커지고 일부 작업이 비정상 길어질 수 있음.
- **출력 파일명 충돌** — 같은 디렉토리에서 `./output.png` 같은 동일 경로를 N개 작업이 쓰면 마지막만 살아남음. 반드시 N개 이름이 모두 달라야 함.
- **Git 리포 안 작업 시 `--skip-git-repo-check` 누락** — codex 가 워크스페이스 검증에서 멈춤.

## 트러블슈팅

| 증상 | 원인 / 조치 |
|------|------------|
| 일부 PNG 가 0 바이트 | codex 세션이 도구 호출 실패. 해당 작업만 재시도 |
| 모든 작업이 직렬화된 듯 느림 (450초+) | 플랜 한도 초과 또는 네트워크 문제. `codex login status`, 플랜 확인 |
| "image_generation tool not available" | `codex features list` 확인. `--enable image_generation` 명시 가능 |
| 파일이 작업 폴더에 없고 `~/.codex/generated_images/` 에만 있음 | codex 가 복사를 안 한 경우. 프롬프트에 "./<파일> 로 저장" 명시 강화 |
| 해상도가 들쭉날쭉 | 정상. 정확한 해상도 필요 시 `gpt-image2` 사용 |
