---
name: motion-video-production
description: Plan, build and verify 15–90 second motion graphics, promo and character videos. Take a reference video apart with OpenCV into measured targets, then produce through gated stages (story, character, keyframes, clips, voice and music, assembly) on a bundled engine, Remotion (carry oracle, one-word cut template) or HyperFrames, and judge the rendered mp4 against the targets. Voice via ElevenLabs or Fish Audio through the composio CLI, a procedural score, mix and verify. Use for video production, reference matching, keyframes, character consistency and motion graphics assembly. 모션 그래픽·홍보 영상·캐릭터 영상 제작과 레퍼런스 영상 분석에 사용한다.
---

# 모션 그래픽·영상 제작 스킬 (motion-video-production)

이 스킬은 모션 그래픽과 영상(예: 한 명의 캐릭터가 나오는 30~90초 영상)을 만드는 순서와 점검 기준을 제공합니다.
이 스킬을 따라가면 레퍼런스 분석(`ref/ANALYSIS.md`, `ref/targets.json`), STORY.md, 캐릭터 시트, 키프레임, 장면 영상, 음악·목소리, 최종 mp4를 얻어가십니다. 화면은 스킬에 들어 있는 엔진(Remotion 또는 HyperFrames)으로 만들고, 완성된 mp4를 숫자로 판정합니다.

편집·카메라·질감 용어(매치 컷, 휩 팬, 푸시 인, 얕은 심도 등)는 `references/glossary.md`에 한국어와 영어로 정리돼 있습니다.

모든 답변은 사용자의 언어(기본 한국어)로 합니다. 도구를 대신 로그인하거나 결제하지 않습니다. 로그인·결제·대용량 다운로드가 필요한 시점에서는 사용자에게 먼저 묻습니다.

## 실행 환경과 경로

이 스킬은 Agent Skills 형식의 공통 지침입니다. Codex, Claude Code 및 다른 스킬 지원 런타임에서 같은 폴더를 사용합니다. 특정 모델의 API나 생성 도구 연결을 포함하지 않습니다. 목소리 자동화는 사용자가 연결한 composio CLI 계정이 있을 때만 씁니다.

- 런타임이 알려 준 이 `SKILL.md`의 실제 경로에서 부모 폴더를 `SKILL_ROOT`로 정합니다. `~/.claude/skills` 같은 특정 설치 경로를 가정하지 않습니다. 아래 `references/`, `templates/`, `harness/`, `scripts/`, `engines/`는 모두 이 폴더 기준입니다.
- 산출물 폴더의 절대 경로를 `PROJECT_ROOT`로 정합니다. 두 경로를 구분하고, 스크립트는 `python3 "$SKILL_ROOT/harness/gate.py" <단계> "$PROJECT_ROOT"`처럼 절대 경로로 실행합니다. 보조 스크립트는 산출물 폴더에서 `bash "$SKILL_ROOT/scripts/<파일>.sh" ...`로 실행합니다.
- Python 3, ffmpeg, ffprobe가 필요합니다. `.sh` 스크립트에는 Bash가 필요합니다(macOS/Linux 또는 Windows의 WSL). 엔진에는 Node.js 24 이상이 필요합니다. 레퍼런스 분석에는 `scripts/requirements-ref.txt`의 OpenCV를 가상환경에 설치합니다.
- 엔진(`engines/remotion`, `engines/hyperframes`)은 스킬 폴더 안에서 설치하지 않습니다. 스킬 폴더는 여러 런타임이 함께 쓰는 사본입니다. `cp -R "$SKILL_ROOT/engines/<엔진>" "$PROJECT_ROOT/engine"`으로 복사한 뒤 그 안에서 `npm ci`를 실행합니다.
- 시작할 때 실제로 제공된 파일 읽기·터미널·이미지 보기·생성 도구를 확인합니다. 생성 도구가 없으면 프롬프트와 저장 위치를 제공하고 사용자가 만든 파일을 받아 이어갑니다. 구독만으로 API 접근이나 자동 생성을 할 수 있다고 가정하지 않습니다.
- 이미지를 볼 수 없는 런타임은 사용자의 실제 눈 검수 결과를 요청합니다. 보지 않은 프레임의 검수 기록을 대신 만들지 않습니다. 검사 스크립트 실행이 불가능하면 명령을 전달하고 실제 종료 코드·보고서를 받은 뒤에만 결과를 판단합니다.
- `STORY.md`는 제공된 템플릿의 한국어 항목명과 표 구조를 유지하고, 내용은 사용자 언어로 채웁니다. 게이트가 이 항목명을 읽습니다. 한국어 외의 `character.txt`에는 색 이름과 함께 `#RRGGBB` 색상 코드를 적습니다(현재 색 검사에서 인식 가능).

## 0. 시작하기 전에 정할 것

작업을 시작할 때 아래 6가지를 사용자에게 한 번에 묻고 `STORY.md` 맨 위에 기록합니다.

1. 공개 방식: 비공개 시안인가, 상업적으로 공개하는 최종본인가. (공개 방식이 비용 규칙을 정합니다. `references/cost-rules.md`)
2. 길이와 화면비: 15~90초(기본 30~90초), 16:9.
3. 사용 가능한 도구와 구독 상태: 이미지 생성, 영상 생성, 음악, 목소리 도구 중 어떤 것을 쓸 수 있는지.
4. 금지 사항: 영상에 넣지 않을 요소(예: 로고, 실존 인물, 읽히는 글자).
5. 레퍼런스 영상: "이런 느낌으로" 따라갈 영상이 있는가. 있으면 0단계를 먼저 합니다.
6. 엔진: Remotion 또는 HyperFrames. 정하기 어려우면 아래 "엔진 선택"의 기준으로 추천합니다.

## 제작 6단계

각 단계는 산출물이 있고, 아래 Harness의 게이트가 종료 코드 0으로 끝나야 다음 단계로 넘어갑니다. 작업 전에 아래 Gotchas(함정 목록)를 먼저 읽습니다.

| 단계 | 하는 일 | 쓰는 도구(예시) | 산출물 |
|---|---|---|---|
| 0. 레퍼런스 분석 | 레퍼런스 영상을 OpenCV로 분해해 편집 리듬·움직임·블러·심도·그레인·질감을 숫자로 남기고, 계획이 그 숫자를 인용하게 함 | `scripts/ref-analyze.py` | `ref/ANALYSIS.md`, `ref/targets.json` |
| 1. 스토리·장면 기획 | 한 줄 줄거리, 장면 목록(시간·장소·행동·대사), 음악 싱크 지점 확정 | 현재 에이전트 | `STORY.md`, 장면 목록 |
| 2. 캐릭터 시트 | 정면·측면·표정·의상을 한 장에 고정한 기준 이미지 | 이미지 생성 도구 | 캐릭터 시트 PNG, 외형 고정문 |
| 3. 키프레임 | 장면마다 시작 화면 1장씩 생성 | 이미지 생성 도구 | 키프레임 PNG |
| 4. 영상 변환 | 키프레임을 시작 화면으로 고정하고 3~6초 클립 생성 | 영상 생성 도구 | 장면별 mp4 |
| 5. 음악·목소리 | 음악 1곡, 캐릭터 목소리 1개(ID 고정), 대사 음성 | 음악·음성 도구 | 음악 wav/mp3, 대사 wav |
| 6. 조립 | 박 격자(beat grid)에 맞춰 컷 배치, 자막·타이틀·엔드카드 모션 그래픽, 믹스, mux | 엔진(Remotion 또는 HyperFrames), ffmpeg | 최종 mp4 |

## Gotchas (먼저 읽을 것)

자주 생기는 함정 8가지입니다. 전체 29가지(증상, 원인, 예방, 하네스 검사 ID)는 `references/gotchas.md`에 있습니다.

1. 클립은 시작 화면이 같아도 1~2초 뒤에 옷, 안경, 머리가 바뀝니다. 0초만 보고 통과시키지 말고 0, 1.0, 1.5, 2.0, 3.0초를 한 줄에 놓고 봅니다. (G01)
2. SSIM 같은 숫자로는 인물 변형을 잡을 수 없습니다. 정상 클립도 움직이면 값이 떨어집니다. 시작 화면 일치만 숫자로 막고 나머지는 눈으로 봅니다. (G02)
3. 외형 고정문은 파일에서 그대로 붙입니다. 손으로 다시 쓰면 달라집니다. 옷 색을 적습니다. (G03)
4. 컷 길이는 초가 아니라 박의 배수로 정하고, 시작 프레임은 누적 시간에서 한 번만 반올림합니다. (G11, G12)
5. 대사 길이를 먼저 재고 컷 길이를 정합니다. 대사가 컷보다 길면 입이 잘립니다. (G13)
6. 파이프(`| tail`)로 검사 출력을 자르면 종료 코드가 사라집니다. 판정은 하네스의 종료 코드와 보고서 파일로 합니다. (G21)
7. 프레임 수를 읽을 때 `ffprobe -of csv=p=0`을 쓰면 `30,`처럼 읽혀 정상 영상이 막힐 수 있습니다. `-of default=nw=1:nk=1`을 씁니다. (G27)
8. 렌더가 끝난 것은 통과의 근거가 아닙니다. 프레임 수를 세고, 컨택트 시트를 직접 봅니다. (G08, G28)

## Harness (단계 게이트)

단계의 산출물은 `harness/gate.py`가 측정해서 종료 코드로 판정합니다. 게이트가 통과(종료 코드 0)하기 전에는 다음 단계로 넘어가지 않고, 완료라고 보고하지 않습니다.

```
python3 "$SKILL_ROOT/harness/gate.py" <단계> "$PROJECT_ROOT"
```

| 제작 단계 | 게이트 | 하는 검사 |
|---|---|---|
| 0. 레퍼런스 분석 | `ref` | 계획 전: ANALYSIS.md 빈칸, targets.json 형식. 렌더 후: 렌더 분석을 지표마다 목표값과 비교(목표, 값, 차이 %, 허용 범위) |
| 1. 스토리·장면 기획 | `story` | STORY.md 빈칸, BPM, 음악 싱크 지점 표(시간이 숫자인지), 장면 표 |
| 2. 캐릭터 시트 | `character` | character.txt(1개 문단 평문, 색 표현), 시트 이미지 |
| 3. 키프레임 | `keyframes` | 중복 파일, 클립과의 화면비 |
| 4. 영상 변환 | `clips` | 길이, 프레임 수, 시작 화면 일치, 프레임 스트립 생성, 눈 검수 기록과 클립별 판정 |
| 5. 음악·목소리 | `audio` | 음성 ID 1개, 대사 파일 |
| 6. 조립 전 | `edit` | 박 격자(컷 경계), 컷 연결, 반복 컷, 대사 길이, src 클립과 사용 구간 |
| 6. 조립 후 | `final` | 프레임 수, 해상도, fps, 오디오 길이, 라우드니스, true peak, 눈 검수 기록 |

- 프로젝트 폴더 규칙은 `harness/gate.py` 첫머리에 있습니다. (`STORY.md`, `character.txt`, `voices.json`, `edit.json`, `sheet/`, `key/`, `clip/`, `out/final.mp4`, `qa/`) 클립 이름, 키프레임 이름, `edit.json`의 `clip:<이름>@<시작초>`는 같은 이름을 씁니다.
- 게이트는 `qa/gate-<단계>.txt`에 보고서를 남깁니다. 보고할 때는 이 파일의 `BLOCK`, `WARN` 줄을 그대로 인용합니다.
- 눈으로 봐야 하는 검사는 기록 파일을 요구합니다. 에이전트가 프레임 스트립과 컨택트 시트를 실제로 보거나 사용자의 실제 검수 결과를 받은 뒤에만 아래 줄을 씁니다.
  - `qa/clips-review.md`: `REVIEWED: <이름> <YYYY-MM-DD>` 줄과, 클립마다 `<클립 이름>: ok|trim|redo|replace` 줄. `redo`, `replace`가 남아 있으면 통과하지 못합니다. 키프레임이 없는 클립은 `nokey: <클립 이름>` 줄로 허용합니다.
  - `qa/review.md`: `REVIEWED: <이름> <YYYY-MM-DD>` 줄과, 본 결과를 적은 줄. 최종본(`out/final.mp4`)보다 나중에 작성해야 합니다.
- 임계값은 환경 변수로 바꿉니다. (`GATE_REF_TOL_SCALE`, `GATE_SSIM_START`, `GATE_LUFS`, `GATE_LUFS_TOL`, `GATE_TP_MAX`)
- 게이트는 엔진을 가리지 않습니다. `ref`와 `final`은 완성된 mp4만 잽니다. `ref/` 폴더가 없으면 `ref` 게이트는 WARN 한 줄을 남기고 건너뜁니다.
- 게이트를 고치거나 새 검사를 더하면 `bash "$SKILL_ROOT/harness/selftest.sh"`가 종료 코드 0으로 끝나야 합니다. 막아야 할 사례를 합성 프로젝트로 실제로 막는지 확인하는 셀프테스트이고, 새 검사에는 막아야 할 사례를 함께 추가합니다.

## 단계별 상세

### 0단계. 레퍼런스 분석
- 사용자가 레퍼런스 영상을 주면 계획 전에 분해합니다. 레퍼런스 파일과 그 프레임은 저장소에 커밋하지 않고 숫자만 남깁니다.
- `python3 -I "$SKILL_ROOT/scripts/ref-analyze.py" <레퍼런스.mp4> -o "$PROJECT_ROOT/ref/analysis.json" --targets "$PROJECT_ROOT/ref/targets.json"` (OpenCV가 설치된 가상환경의 python3로 실행)
- `templates/ANALYSIS.md`를 `ref/ANALYSIS.md`로 복사해 숫자와 그 숫자가 이번 작품에 주는 뜻을 채웁니다. `gate.py ref`가 통과해야 1단계로 넘어갑니다.
- 1단계 이후의 계획(컷 길이, 홀드, 전환, 블러, 질감)은 ANALYSIS.md의 숫자를 인용합니다. 렌더한 뒤에는 같은 스크립트로 최종본을 분석해 `qa/render-analysis.json`에 쓰고 `gate.py ref`로 비교합니다.
- 지표의 뜻, 재는 방법, 다를 때 고칠 것, 실제 예시는 `references/reference-analysis.md`에 있습니다.

### 1단계. 스토리·장면 기획
- `templates/STORY.md`를 복사해 채웁니다. 장면마다 시간대, 장소, 캐릭터 행동 1개, 감정 1개를 적습니다.
- 한 장면에는 행동을 1개만 넣습니다. 영상 생성 모델은 한 클립에 여러 행동이 있으면 손·소품이 변형됩니다.
- 시간대와 장소가 논리적으로 이어지는지 확인합니다. 아침 출근 장면 뒤에 일출 장면이 오면 시간이 거꾸로 갑니다.
- 음악 싱크 지점(드롭, 마지막 히트)은 기획 단계에서 초 단위로 정하고 이후 바꾸지 않습니다.

### 2단계. 캐릭터 시트
- `templates/CHARACTER_SHEET.md`로 시트를 점검합니다. 시트·키프레임·클립 프롬프트 틀은 `templates/PROMPTS.md`에 있습니다.
- 시트가 확정되면 **외형 고정문**(머리, 안경, 의상, 색상을 한 문단으로 쓴 문장)을 `character.txt` 파일로 저장합니다. 이후 모든 프롬프트에 이 파일의 문장을 그대로 붙입니다.

### 3단계. 키프레임
- 모든 키프레임 생성에 같은 캐릭터 시트를 참조 이미지로 넣고, 외형 고정문을 그대로 붙입니다.
- 생성한 이미지는 시트와 나란히 놓고 얼굴·머리·안경·의상을 대조한 뒤 통과한 것만 사용합니다.
- 이미지 생성 도구가 같은 이미지를 두 번 저장하는 경우가 있으므로(G09) 해시(md5)로 중복 파일을 거릅니다.

### 4단계. 영상 변환
- 키프레임을 영상의 **시작 화면**으로 고정하고, 캐릭터 시트를 참조 이미지로 함께 넣습니다.
- 클립 길이는 3~6초로 짧게 잡습니다. 길수록 뒤쪽에서 얼굴이 녹거나 소품이 사라집니다.
- 생성한 클립은 `bash "$SKILL_ROOT/scripts/clipsheet.sh" <클립.mp4>`로 프레임 시트(클립의 모든 프레임, 기본 `qa/sheets/`)를 만들어 눈으로 확인하고, 결함이 있는 구간은 잘라 내고 쓸 수 있는 구간만 사용합니다. (`templates/SCENE_AUDIT.md`에 기록)
- 초록 배경으로 생성한 클립에서 캐릭터만 떼어 합성하는 경우 `scripts/key-plate.sh`를 사용합니다.

### 5단계. 음악·목소리
- 음악 BPM을 먼저 확정하고 `references/beat-grid.md`의 계산으로 컷 길이를 박 단위로 맞춥니다.
- 목소리는 도구에서 음성 1개를 골라 그 ID만 모든 대사에 씁니다. 대사를 합성한 뒤 받아쓰기(whisper)로 대본과 일치하는지 확인합니다.
- 유명인·정치인·저작물 캐릭터의 목소리 복제 모델은 사용하지 않습니다.

### 엔진 선택
화면을 만드는 엔진은 둘 중 하나를 고릅니다. 두 엔진 모두 스킬에 들어 있고, 버전이 고정돼 있습니다. 자세한 비교와 명령은 `references/engines.md`에 있습니다.
- **Remotion** (`engines/remotion/`): React로 프레임마다 값을 계산합니다. 경계마다 무언가가 살아남는지(carry)를 렌더 전에 숫자로 재는 검사, 단어 하나를 한 자리에 두고 장면이 넘겨받는 wordcut 템플릿이 여기에만 있습니다. 직원 4명 이상 영리 조직은 Remotion Company License가 필요합니다.
- **HyperFrames** (`engines/hyperframes/`): 평범한 HTML/CSS 페이지를 GSAP으로 움직여 mp4로 렌더합니다. 재료가 웹페이지·문서일 때, HTML을 아는 사람이 바로 고쳐야 할 때 좋습니다. Apache-2.0입니다. 선언한 track이 없어서 carry 점수는 내지 못하고, 움직임은 `gate.py ref`가 mp4에서 잽니다.
- 정하기 어려우면 Remotion으로 시작하고, 라이선스 조건이 맞지 않으면 HyperFrames를 씁니다.

### 6단계. 조립
- 엔진 폴더를 작업 폴더로 복사하고 `npm ci`로 설치합니다(스킬 폴더 안에서 설치하지 않음).
- **carry가 기본 경계입니다.** carry는 이 스킬의 용어로, 경계를 넘어 살아남는 요소입니다. 비트 경계마다 화면에 있던 요소가 살아남아 다음 비트로 움직이거나 커집니다. 아무것도 남지 않는 장면 교체(하드 컷, 디졸브, 와이프)는 몰아치기(몽타주) 안이나 엔드카드로 갈 때만 씁니다. 어휘는 `references/art-direction.md`에 있습니다.
- Remotion: 모션은 `motions/`의 순수 함수로, 작품별 기하는 순수 `scene(t)`로 씁니다. 화면과 `track.ts`가 같은 `scene(t)`를 읽습니다. 렌더 전에 `node pipeline/probe.mjs productions/<id>`로 carry를 재고(0.5 미만 FAIL), 스틸(`node pipeline/render.mjs <id> --stills 0.5 1.5 3.0`)을 직접 본 뒤 영상을 렌더합니다(`renders/<id>/`). `productions/carry-demo/`가 모든 파일의 예시입니다.
- 비트 시트는 `templates/BEATSHEET.md`로 `timing.ts`와 함께 씁니다. 모든 경계에 살아남는 요소를 적습니다.
- 단어 하나를 여러 장면이 넘겨받는 영상(매치 컷, graphic match cut)은 `productions/wordcut/`의 `data.ts`만 바꿔서 만듭니다. 레퍼런스가 있으면 `node productions/wordcut/plan.mjs "$PROJECT_ROOT/ref/analysis.json" <초>`로 타이밍을 뽑고, `node productions/wordcut/drift.mjs`가 단어가 한 자리에 있는지 픽셀로 잽니다(0.5px 초과면 종료 코드 1). 첫 프레임은 페이지가 아니라 미드숏(medium shot)입니다. 단어가 가운데, 단어 줄만 선명한 초점 띠(얕은 심도, shallow depth of field), 0프레임부터 렌즈 질감(RGB 분리, 그레인, 비네트), 페이지 크롬 없음, 하이라이트만 색. `node productions/wordcut/frame0.mjs --check`가 확인합니다. 첫 프레임만이 아닙니다. 모든 장면에서 단어 하나만 선명하고, 위아래 줄은 단어 줄에서 멀수록 더 흐려집니다. 장면마다 각도(책상 위 종이, 손에 든 휴대폰, 정면), 확대(가까이, 더 가까이, 아주 가까이), 심도, 바닥, 빛과 그레인을 바꾸고, 이웃한 두 장면이 같은 각도+확대+심도 조합을 쓰지 않습니다(`timing.ts`의 `shots`). `node productions/wordcut/focus.mjs --check`가 장면마다 착지 프레임의 초점 비율을 재고 2 미만이면 종료 코드 1을 냅니다.
- 목소리는 대사를 먼저 생성하고 길이를 잰 뒤 타이밍을 정합니다(`pipeline/vo.mjs`, `pipeline/vo-assemble.mjs`, composio CLI. `references/providers.md`). 크레딧이 드므로 생성 전에 사용자에게 알립니다.
- 음악은 `node pipeline/score.mjs productions/<id>`의 기본 스코어로 시작하거나, `templates/MUSIC_BRIEF.md`로 워커에게 맡깁니다.
- 믹스와 mux는 `bash "$SKILL_ROOT/scripts/mix-mux.sh" <picture.mp4> <fps> <초> <music.wav> <vo.wav|-> <out.mp4>`로 합니다. 프레임 수가 맞을 때만 mux하고, 대사가 나올 때 음악을 낮춥니다.
- 최종 확인은 `bash "$SKILL_ROOT/scripts/verify.sh" <mp4>`(`PRODUCTION=productions/<id>`를 주면 carry 검사도 함께)로 하고, 생성된 컨택트 시트를 직접 봅니다. 레퍼런스가 있으면 `gate.py ref`로 비교합니다.

### 타임라인 편집기 (조립 뒤 사람이 직접 고칠 때)
- 만든 영상을 사용자가 타임라인으로 보고 고치게 하려면 `node "$SKILL_ROOT/timeline/serve.mjs" "$PROJECT_ROOT"`를 실행합니다. 브라우저에 영상·텍스트·목소리·음악 네 트랙이 뜹니다. Node 표준 라이브러리와 ffmpeg만 씁니다(설치 없음).
- 기준 파일은 `edit.json` 하나입니다. 게이트가 읽는 `cuts`에 선택 트랙 `text`(자막)와 `audio`(목소리·음악: `file`, `t`, `in`, `d`, `gain` dB, `fadeIn`, `fadeOut`, 음악의 `duck`)를 더합니다. 형식은 `timeline/README.md`에 있습니다. 목소리 항목의 `id`는 `voices.json`의 대사 id와 같게 씁니다.
- 에이전트도 같은 코어로 고칩니다: `node "$SKILL_ROOT/timeline/apply.mjs" "$PROJECT_ROOT" ops.json`(인자 없이 실행하면 타임라인과 문제 목록 출력). 열린 편집기는 2초 안에 바뀐 내용을 받습니다. 사용자가 편집기에서 고친 뒤에는 `apply.mjs`로 다시 읽고 이어갑니다.
- 결과물은 `node "$SKILL_ROOT/timeline/build.mjs" "$PROJECT_ROOT"`(편집기의 Build 버튼과 같음)로 `out/final.mp4`를 만듭니다. 컷은 소스에서 프레임 단위로 자르고, 오디오는 항목마다 위치·게인·페이드를 적용해 섞고(음악은 목소리 아래로 낮춤), 텍스트는 화면에 새기고(libass 필요. macOS는 `brew install ffmpeg-full`, 빌드가 자동으로 찾음) `out/captions.srt`도 씁니다. libass가 없거나 `--no-burn`이면 자막 트랙으로만 넣습니다. 그다음 `gate.py edit`, `gate.py final`을 돌립니다.
- 첫 저장 때 원래 `edit.json`을 `qa/timeline/`에 복사해 둡니다.

### 브랜드 소개 영상과 홈페이지 (레시피)
"우리 가게 소개 영상을 홈페이지에 넣고 싶다"는 요청은 이 순서로 만듭니다. 새 엔진 없이 wordcut 템플릿과 `templates/homepage-intro.html`을 씁니다. 자세한 순서와 예시는 `references/brand-intro.md`에 있습니다.
1. 레퍼런스를 읽고(있으면 0단계) 장면 목록을 4줄 이하로 씁니다. 한 줄 = 프레임 범위, 화면, 빌려 오는 레퍼런스.
2. 이미지 프롬프트와 마무리를 정하는 키워드 3~6개를 고릅니다. 하나는 wordcut의 단어가 됩니다.
3. 마무리 이미지를 생성합니다. 화면비는 영상과 같게, 단어 자리는 비워 둡니다.
4. wordcut으로 컷을 만듭니다. `data.ts`의 `closing`에 마무리 이미지를 넣으면 마지막 비트가 그 이미지에서 멈춥니다.
5. 홈페이지 한 장: 히어로는 t=0 프레임이 영상의 마무리 이미지인 Three.js 장면입니다. 9:16 영상은 휴대폰에서만 짧은 카드로 보여 주고 데스크톱에서는 숨깁니다. 유튜브 오프닝에서 영상 끝을 사이트 첫 프레임으로 잇는 매치 컷은 페이지가 아니라 영상 편집에서 만듭니다. 출발점은 `templates/homepage-intro.html`이고, reduced motion이나 WebGL이 없으면 포스터(마지막 프레임)와 일반 페이지만 보여 줍니다. 간격, 섹션 배치, 외부 라이브러리 규칙도 `references/brand-intro.md`에 있습니다.

## 캐릭터 일관성 7가지

캐릭터 시트, 외형 고정문, 키프레임 시작 화면, 목소리 고정(같은 음성 ID), 대사와 입 모양 타이밍, 음악 박자, 품질 검수가 모두 맞물려야 장면이 바뀌어도 얼굴과 목소리가 같습니다. 항목별 문제와 맞추는 방법은 `references/consistency-7.md`에 있습니다.

## 비용 분기 규칙

무료 플랜으로 시안을 만들고, 상업 공개용 최종본의 음악·목소리만 유료 플랜에서 다시 생성합니다. 유료 대량 생성 전에는 예상 크레딧을 알리고 승인을 받습니다. 전체 규칙은 `references/cost-rules.md`, 현재 약관은 `references/licensing.md`에 있습니다.

## 검수 원칙

- 눈으로 보지 않은 것을 통과로 보고하지 않습니다. "렌더가 끝났다"는 통과의 근거가 아닙니다.
- 측정할 수 있는 것은 측정합니다: 프레임 수, 길이, 라우드니스(LUFS), true peak, 받아쓰기 일치 여부. 하네스가 있는 단계는 하네스의 종료 코드로 판정합니다.
- 직접 들어 보지 않은 오디오를 들었다고 보고하지 않습니다. 받아쓰기와 라우드니스로 확인했다고 보고합니다.
- 결과 보고에는 측정 수치, 고친 것, 남은 결함, 산출물 위치를 포함합니다.

하네스 검사가 없는 실수는 `references/pitfalls.md`, 도구별 사용법은 `references/providers.md`를 참고합니다.

## 스크립트 (모두 `scripts/` 아래, 프로젝트 폴더에서 실행)

| 파일 | 용도 |
|---|---|
| `ref-analyze.py` | 레퍼런스(또는 렌더) 영상을 OpenCV로 분해해 JSON 하나로 (`requirements-ref.txt`) |
| `dupcheck.py` | 같은 키프레임을 쓰는 반복 컷 검출 |
| `clipsheet.sh` | 프레임 시트(클립의 모든 프레임을 6x5 칸으로 배치) |
| `key-plate.sh` | 초록 배경 -> 투명 PNG |
| `mix-mux.sh` | 음악·대사 믹스와 프레임 수 게이트 mux |
| `verify.sh` | 영상 측정, 반복 프레임, 가장자리 색, 컨택트 시트, 받아쓰기, 선택적 carry 검사 |
| `beat-grid.py` | BPM 기준 박 길이·스냅 계산 |
| `../harness/gate.py` | 단계별 통과 여부를 종료 코드로 판정 |
| `../timeline/serve.mjs`, `apply.mjs`, `build.mjs` | 타임라인 편집기, 에이전트용 편집 CLI, edit.json → mp4 빌드 |

엔진 폴더의 스크립트(`pipeline/render.mjs`, `probe.mjs`, `score.mjs`, `vo.mjs`, `vo-assemble.mjs`, `productions/wordcut/*.mjs`)는 `references/engines.md`에 정리돼 있습니다.
