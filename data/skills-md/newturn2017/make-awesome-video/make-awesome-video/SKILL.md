---
name: make-awesome-video
description: Direct pro-level motion-graphics videos with a coding agent (HyperFrames or Remotion code → MP4). Auto-detects the kind of video from the inputs alone — product launch/promo, motion-design/kinetic-typography piece recreated from a reference video, card-news/signage/kiosk loop from static images, or vertical social hook — then runs reference analysis (shot-by-shot decomposition, beat sync), storyboard or shot-list approval, per-shot still frames compared against the reference, render with an independent critic pass, and camera-language director notes. Use when the user wants a launch video, product video, promo, motion graphics, kinetic typography, logo/title sequence, "make one like this video", card news animation, kiosk/signage video, or says "어썸 영상", "런치 영상", "제품 소개 영상", "모션그래픽 영상", "키네틱 타이포", "이 영상처럼 만들어줘", "카드뉴스 애니메이션", "키오스크 영상", "프로모 영상", "모션 쇼릴", "모션 디자이너 실력 보여줘", "make-awesome-video". Not for editing existing footage (video-use) or AI-generated cinematic clips (kie video-creator).
metadata:
  short-description: Reference-driven, gated motion-graphics directing (launch, motion design, info, social)
---

# Make Awesome Video

"한 번의 프롬프트" 영상이 평범한 이유는 모델이 아니라 **컨텍스트 부족** 때문이다. 참조가 없으면 에이전트는 기본값으로 돌아간다: 중앙 정렬 텍스트, 그라데이션 배경, 모든 게 페이드 인. 이 스킬은 에이전트를 **감독의 지시를 받는 모션 디자이너**로 만든다.

핵심 원칙:

1. **스타일은 설명하지 말고 이름을 부른다.** 참조 영상 1–2개를 고르고 "이걸 맞춰"라고 한다.
2. **영상은 코드다.** HyperFrames(기본) 또는 Remotion으로 장면을 코드로 쓰고 MP4로 렌더한다. 수정은 한 줄 고치고 재렌더.
3. **UI는 발명하지 않는다.** 실제 제품 스크린샷, 또는 21st/shadcn 같은 실제 컴포넌트를 쓴다.
4. **방향을 먼저 고르고, 움직임은 나중에.** 스토리보드 3안(`motion` 모드는 참조에서 역설계한 샷 리스트) → 장면별 정지 프레임 → 그다음에 애니메이션.
5. **노트는 카메라 언어로.** "더 좋게"가 아니라 "줌 0.7x로 느리게", "여기 하드 컷", "버튼에 푸시 인".
6. **종류를 묻지 않고 알아낸다.** 입력(참조 영상, 스크린샷, 카드 이미지, 문구)만으로 모드를 판별하고 한 줄로 알린다. "이 영상처럼, 단어는 CLAUDE" 한 줄이면 충분해야 한다.

모든 산출물은 사용자의 현재 작업 폴더(cwd) 아래 프로젝트에 만든다. 스킬 폴더에는 쓰지 않는다.

## 비협상 규칙

1. **사실만.** 후기, 평점, 고객사, 성과 수치, 보증, 확정된 예약을 지어내지 않는다. 브리프에 없는 주장은 화면에 올리지 않는다. 실제 소재가 없는 컨셉 영상은 컨셉이라고 표기하고("Concept film · AI-generated imagery" 등), AI 이미지를 실제 고객·작업·결과처럼 보이게 하지 않는다. 실존 브랜드 스펙 광고는 0단계 인테이크 항목을 따른다.
2. **결정적 모션.** 모든 애니메이션 상태는 타임라인 시간의 순수 함수다. 자유 실행 `requestAnimationFrame`, `Date.now()`, 시드 없는 난수, 물리 이력 금지. 어느 프레임으로 seek해도 같은 픽셀.
3. **만든 사람이 채점하지 않는다.** G4에 렌더를 들고 가기 전에, 맥락을 모르는 새 서브에이전트가 실제 MP4와 측정값으로 판정한다 ([references/critic-loop.md](references/critic-loop.md)). 빌더의 자체 체크만으로 "통과"라고 하지 않는다.
4. **에러 0 ≠ 좋음.** `check` 통과, 매끄러운 움직임은 출발선이다. 깨끗하지만 평범하고 비어 있고 느린 버전도 거절된다. 정지 구간·음량을 재고([references/quality-bar.md](references/quality-bar.md) "측정"), 창의적으로 판정한다.
5. **소리 꺼도 통한다** (`launch`·`social`·`info`). 처음 보는 사람이 끝에서 무엇을 하는 회사인지, 다음 행동 하나가 무엇인지 말할 수 있어야 한다.

## 모드 (먼저 판별)

| 모드 | 입력 신호 | 방향 게이트(G2) |
|---|---|---|
| `launch` | 제품 URL, 스크린샷, 기능 설명 | 스토리보드 3안 |
| `motion` | **참조 영상 + 문구 하나** (제품 소재 없음) — 키네틱 타이포, 모션 쇼릴, 로고/타이틀 시퀀스. 참조 없이 "실력 보여줘"·"쇼릴처럼"만 있어도 `motion` (참조는 prompt-motion에서) | **샷 리스트 승인** (참조가 곧 방향) |
| `info` | 카드뉴스·포스터 등 정적 이미지 여러 장 → 사이니지/키오스크/안내 루프 | 스토리보드 3안 |
| `social` | 9:16, 20초 이하, SNS | 훅 3안 |

판별표 전체, 모드별 인테이크·기본값·게이트 차이: [references/modes.md](references/modes.md). 판별은 질문하지 않고 알린다 ("참조 영상 + 단어 하나 → 모션 디자인 모드로 진행합니다").

## 절대 규칙: 게이트

브리프에서 바로 렌더로 가지 않는다. 그것이 이 스킬이 막으려는 "원프롬프트 = 그저 그런 영상" 실패다. 아래 네 게이트에서는 **반드시 멈추고 사용자의 선택/승인을 기다린다.** 사용자가 명시적으로 "게이트 건너뛰고 끝까지 가"라고 하면 그때만 스스로 고르고, 무엇을 골랐는지 기록한다.

| 게이트 | 멈추는 지점 | 사용자가 하는 일 |
|---|---|---|
| G1 | 참조 후보 제시 후 (`motion`: 주어진 참조가 있으면 분석 결과 제시로 대체하고 멈추지 않음, 없으면 prompt-motion 후보 제시) | 참조 영상 1–2개 선택 |
| G2 | 스토리보드 3안 (`motion`: 샷 리스트) 제시 후 | 방향 선택 / 샷 리스트 승인 |
| G3 | 정지 프레임 제시 후 (`motion`: 참조 동일 시점과 나란히) | 프레임 승인 또는 수정 지시 |
| G4 | 첫 렌더 후 (`motion`: 참조 대비 차이 목록을 먼저 제시) | 감독 노트 (반복) |

## 워크플로

### 0단계 — 모드 판별 + 인테이크 (브리프 수집)

먼저 [references/modes.md](references/modes.md) 판별표로 모드를 정하고, 셋업 확인(2단계 스크립트)을 병행한다. 인테이크는 모드별로 다르다. 아래 목록은 `launch` 기준이다. `motion`은 참조 영상 + 문구만 받고 나머지(색, 폰트 계열, 길이, 비율, 리듬, 음악 유무)는 참조에서 추론한다. 묻는 건 최대 2개(문구 배치, 음원). `info`는 원본 자료 + 설치 환경(화면 물리 크기, 시청 거리)이다.

한 번에 묻고, 이미 받은 건 다시 묻지 않는다. 없는 항목은 합리적인 기본값을 제안한다.

- **제품**: 이름, 한 줄 설명, 영상이 보여줄 핵심 기능 1–3개
- **브랜드**: 로고 파일(SVG 우선), 색상 HEX, 폰트 이름/파일. 없으면 사이트 URL을 받아 추출
- **실제 제품 스크린샷/화면 녹화**: 가장 중요. 없으면 사이트 URL → `npx hyperframes capture <url>`로 캡처
- **브레인덤프**: 사용자가 머릿속에 그리는 영상 (거칠어도 됨)
- **포맷**: 길이(기본 20–40초), 비율(landscape 1920x1080 / portrait 1080x1920 / square), 사운드(음악 파일 유무)
- **채널**: X, 유튜브, 랜딩 히어로 등 (비율과 길이 결정에 영향)
- **실존 브랜드 스펙 광고**(의뢰 없이 만드는 브랜드 영상): 로고·슬로건은 상표라 개인 포트폴리오·비공식 용도로만 쓴다고 알리고, 락업에 "Unofficial fan film" 같은 소형 표기를 넣을지 묻는다. 카피는 연도·출처(캠페인명)를 확인할 수 있는 것만 쓴다.
- **스크린샷이 없는 소재**(브랜드 매니페스토 등): 사진·음원은 생성 도구로 만든다. 이미지는 방향(G2)이 정해진 뒤 필요한 수만큼 생성하고(안마다 필요 수가 크게 다르다), 음원은 스토리보드 전에 만들어 비트 지도부터 뽑는다. 생성 요령: [references/gotchas.md](references/gotchas.md) "소재 준비" 섹션.

결과를 프로젝트 루트의 `brief.md`로 저장한다. 템플릿은 [references/storyboard-template.md](references/storyboard-template.md) 의 "brief.md" 섹션.

### 1단계 — 참조 영상 고르기·분석 (G1)

사용자가 참조 영상을 줬으면 후보 탐색을 건너뛰고 바로 분석한다. 없으면 두 갤러리에서 후보를 찾는다: whatships.com(X에 올라온 스타트업 런치 영상 큐레이션 디렉터리)과 prompt-motion.com(Claude가 만든 모션 영상 + 그 영상을 만든 프롬프트 원문).

```bash
python3 {baseDir}/scripts/find_refs.py "devtool terminal" --category "Developer tools" --limit 8 --details
python3 {baseDir}/scripts/find_refs.py --list-categories
```

- 제품 카테고리 + 원하는 느낌(키네틱 타이포, UI 워크스루, 3D, 미니멀 등) 키워드로 6–10개 후보를 뽑아 제목·회사·길이·원본 X 링크·포스터와 함께 제시한다.
- whatships는 스타트업 런치 영상 위주라 스포츠·패션 같은 **브랜드 광고 참조는 거의 없다**. "kinetic typography" 같은 키워드도 결과가 비기 쉽다. 브랜드 매니페스토·프로모는 `--category Motion`(쇼릴, 브랜드 릴, 매니페스토 필름)에서 고르고, 사용자에게 실제 브랜드 광고 링크/mp4를 주면 그걸 우선한다고 함께 알린다.
- **prompt-motion:** 영상마다 그걸 만든 프롬프트가 붙어 있어 "어떤 지시가 이 결과를 냈나"까지 참조가 된다. 참조 없는 `motion` 요청("모션 디자이너 실력 보여줘", "쇼릴처럼 전력으로")은 여기서 서로 다른 방향의 후보 3–4개를 뽑아 G1에 제시한다. 영상 URL은 `analyze_ref.sh`에 그대로 넣으면 된다. 프롬프트 원문은 방향과 금지 목록을 읽는 데만 쓰고 결과물에 옮기지 않는다. 갤러리 232편에서 뽑은 패턴: [references/prompt-motion-patterns.md](references/prompt-motion-patterns.md).
  ```bash
  python3 {baseDir}/scripts/find_motion_refs.py "launch" --structured --details --limit 6
  python3 {baseDir}/scripts/find_motion_refs.py kinetic type --aspect square
  python3 {baseDir}/scripts/find_motion_refs.py --show <slug>     # 프롬프트 원문 읽기
  ```
- 사용자가 이미 참조 영상(X 링크, mp4, 유튜브)을 갖고 있으면 그걸 우선한다.
- whatships 결과가 약하거나 특정 전환 메커니즘(전경 플라이스루, 결과 물질화, 분해 레이어, 요청 → 선택 → 확인 등)을 보여줄 참조가 필요하면 [references/motion-grammar.md](references/motion-grammar.md)의 "참조 28편"에서 메커니즘이 맞는 순간을 시각까지 지정해 함께 제시한다.
- **G1: 사용자가 1–2개를 고를 때까지 멈춘다.**

선택되면 참조를 분석해 **스타일 스펙**을 만든다:

```bash
bash {baseDir}/scripts/analyze_ref.sh "<X post URL 또는 로컬 mp4>" refs/<slug>
```

컷 타임스탬프, 평균 샷 길이, 컨택트 시트, 대표 팔레트를 뽑는다. 모션 그래픽 참조는 `--fps 4`를 붙여 타임스탬프가 찍힌 밀도 높은 시트(`contact_dense.png`)를 만들고, 그걸 보며 [references/shot-decomposition.md](references/shot-decomposition.md) 대로 **샷 리스트**를 역설계한다. 참조에 음악이 있으면 음원을 프로젝트에 넣고 `npx hyperframes beats <project>`로 비트를 뽑아 컷이 비트 동기인지 확인한다. 이것과 프레임을 직접 보고 [references/reference-analysis.md](references/reference-analysis.md) 형식으로 `refs/style-spec.md`를 쓴다. 다운로드가 실패하면(X 로그인 벽 등) 사용자에게 mp4를 받거나, 포스터 + 원본 영상 시청 기반으로 스펙을 쓰고 그 한계를 밝힌다. 참조 영상은 스타일 학습용으로만 쓰고 결과물에 그대로 넣지 않는다.

### 2단계 — 빌드 도구 셋업

**워크플로를 시작할 때 가장 먼저** 설치 상태를 확인하고, 빠진 게 있으면 바로 설치한다. 인테이크(0단계) 질문을 보내면서 병행해도 된다.

```bash
bash {baseDir}/scripts/setup.sh --check     # 상태만 확인
bash {baseDir}/scripts/setup.sh             # 빠진 것 설치 (HyperFrames + Remotion)
bash {baseDir}/scripts/setup.sh --engine hyperframes   # 한쪽만
```

설치 대상: Node.js 22+, ffmpeg/ffprobe, yt-dlp, HyperFrames CLI(`npm i -g hyperframes`) + 렌더용 Chrome + 공식 에이전트 스킬(`hyperframes`, `product-launch-video`, `motion-graphics` 등), Remotion 공식 에이전트 스킬(`remotion-best-practices` 등) + `create-video` 스캐폴더. 시스템 패키지는 brew, 또는 비밀번호 없는 sudo가 가능할 때 apt/dnf/pacman으로 설치한다. 불가능하면 스크립트가 수동 명령을 출력하니 그대로 사용자에게 전달한다.

- 새로 설치된 에이전트 스킬은 **세션을 재시작해야 로드된다.** 재시작 전에는 init이 만드는 프로젝트의 `CLAUDE.md`와 `npx hyperframes docs`로 작성 규칙을 확인한다.
- **HyperFrames (기본)** vs **Remotion**: 사용자가 Remotion을 원하거나, 이미 React 디자인 시스템/컴포넌트를 재사용해야 하면 Remotion. Remotion 프로젝트는 `npx create-video@latest --yes --blank <name>`로 만들고 `remotion-best-practices` 스킬을 따른다. 3인 초과 회사는 유료 라이선스가 필요하니 상업용이면 알린다.
- **21st (UI 컴포넌트)**: 스크립트는 확인만 한다. 없으면 설치 명령과 `API_KEY_21ST` 필요를 사용자에게 알린다. Claude 설정과 API 키가 걸린 일이라 자동 설치하지 않는다. 없으면 실제 스크린샷 → shadcn/ui → HyperFrames UI 블록 순서로 대체.

세부 명령표: [references/setup.md](references/setup.md)

프로젝트 초기화:

```bash
npx hyperframes init <project-name> --non-interactive --resolution landscape
```

**장면 HTML을 쓰기 전에 `<project>/CLAUDE.md`(또는 `AGENTS.md`)를 반드시 읽는다.** init이 만들어 주는 이 파일이 HyperFrames 작성 규칙(`window.__timelines` 등록, `data-*` 속성, seek 가능한 애니메이션)과 공식 스킬 라우팅을 담고 있다. GSAP/HyperFrames 코드를 기억에 의존해 쓰지 않는다.

- 작성은 HyperFrames 공식 스킬에 맡긴다: `/hyperframes`(라우터), `/product-launch-video`, `/motion-graphics`, `/hyperframes-animation`, `/hyperframes-registry`(블록 설치). 없으면 `npx hyperframes skills update` 후 세션 재시작이 필요하다고 사용자에게 알린다.
- **역할 분담:** 공식 스킬은 "어떻게 코드로 만드나", 이 스킬은 "무엇을 만들지와 언제 멈출지"를 맡는다. 공식 워크플로가 브리프에서 곧장 렌더로 가려 해도 이 스킬의 G1–G4 게이트가 우선한다.
- 미리보기는 에이전트에서 막히지 않는 `npx hyperframes preview --background`(종료: `--stop`)를 쓴다.

### 3단계 — 스토리보드 3안 또는 샷 리스트 (G2)

**`motion` 모드:** 3안을 쓰지 않는다. 참조가 곧 방향이다. `shots.md`(샷 리스트: 참조 시간 / 우리 시간 / 기법 / 이징 / 모티프 / 구현 / 우리 내용)를 [references/shot-decomposition.md](references/shot-decomposition.md) 형식으로 쓰고 승인받는다. 쓰기 전에 [references/motion-craft.md](references/motion-craft.md)(모티프 연속성, 페이싱 곡선, 비트 동기, 이징 사전)를 읽는다. 구현 열에는 매핑표에 있는 블록·룰·kit 이름만 쓴다.

**그 외 모드:**

쓰기 전에 [references/motion-grammar.md](references/motion-grammar.md)(여섯 규칙, 구도 규칙, 메커니즘 카탈로그)를 읽는다. 브리프 + 스타일 스펙 + 스크린샷을 모두 넣고 **방향이 서로 다른** 3안을 쓴다. 같은 안을 세 번 다듬은 것이 아니어야 한다. 예:

- A: 참조를 가장 충실히 따르는 안
- B: 제품 UI가 주인공인 안 (스크린샷 속으로 푸시 인하며 기능을 보여줌)
- C: 타이포/메시지가 주인공인 안 (키네틱 타이포, 하드 컷 리듬)

각 안은 장면 표(시간·화면 텍스트·비주얼·비트의 역할·카메라/모션·트랜지션 아웃과 넘겨지는 물체·사용할 HyperFrames 블록), 한 줄 로그라인, 효과 이름 없이 설명하는 **시그니처 변형 3개**, 장면을 관통하는 **연속 모티프 하나**, 그 안에서 쓰지 않을 **금지 목록**(6–10개, [references/prompt-motion-patterns.md](references/prompt-motion-patterns.md) "금지 목록" 섹션에서 고름)을 갖는다. 음악이 있으면 시간 열을 박 단위로도 적는다. 기능 비트의 주 피사체는 화면의 60–85%, 움직임 없는 구간은 0.6초 이하로 설계한다. 형식: [references/storyboard-template.md](references/storyboard-template.md). `storyboards/A.md`, `B.md`, `C.md`로 저장.

30초 이상 `launch`이거나 브리프에 사실 주장이 많으면, 제시 전에 새 서브에이전트로 스토리보드 크리틱을 돌려(사실성, 필러 비트, 음소거 CTA) 걸린 것을 고친다. 프롬프트: [references/critic-loop.md](references/critic-loop.md).

**G2: 사용자가 방향을 고를 때까지 멈춘다.** "A의 오프닝 + B의 중반"처럼 섞는 것도 받는다.

승인되면 brief + 스타일 스펙 + 선택안(또는 샷 리스트)을 `film-spec.md` 한 장으로 합친다 (입력 / 방향·금지 / 박 단위 구조 / 빌드 / 함정 / 멈춤 지점). 이후 장면 코드와 서브에이전트는 이 파일을 기준으로 삼는다. 형식: [references/film-spec-template.md](references/film-spec-template.md).

### 4단계 — 장면별 정지 프레임 (G3)

움직이기 전에 장면마다 **대표 정지 프레임 1장**을 만든다. 스토리보드를 고치는 게 렌더를 고치는 것보다 훨씬 싸다.

1. 각 장면을 레이아웃만 먼저 구현한다 (애니메이션은 최종 상태에 멈춘 상태, 즉 "hero frame").
2. 장면 중간 시점에서 캡처:
   ```bash
   npx hyperframes snapshot <project> --at 1.5,5,9.5,14 --no-end
   npx hyperframes snapshot <project> --at 2,6 --against refs/<slug>/ref.mp4   # 참조와 나란히 비교
   ```
   스냅샷은 `<project>/snapshots/`에 저장되고 `contact-sheet.jpg`도 함께 생긴다. 이 단계에서는 타임라인이 정지 상태라 `check`가 "Timeline did not advance under seek"로 실패하는데, 정상이다. `check` 게이트는 5단계에서 적용한다.
3. 프레임을 직접 열어 보고 [references/quality-bar.md](references/quality-bar.md) 체크리스트로 자체 검수한다. 장면이 5개 이상이거나 3D·커스텀 컴포넌트가 있으면 새 서브에이전트에 정지 프레임 크리틱을 맡기고(권장), 지적을 고친 뒤 사용자에게 보여준다. `motion` 모드는 `--against` 쌍 이미지를 보여주며 샷마다 참조와 다른 점을 먼저 밝힌다.
4. 3D 장면이나 커스텀 컴포넌트는 먼저 단독 랩 컴포지션으로 만들어 컴포넌트 크리틱의 KEEP을 받은 뒤 합류시킨다 ([references/three-d.md](references/three-d.md)).

**G3: 승인 전에는 애니메이션을 붙이지 않는다.** 정지 프레임 수정은 초 단위다.

### 5단계 — 애니메이션 & 렌더

승인된 프레임에 스타일 스펙의 페이싱·이징·트랜지션을 입힌다.

**모션 킷:** 검증된 헬퍼를 프로젝트로 복사해 쓴다 (`{baseDir}/assets/motion-kit/kit.js`, `kit.css` → `<project>/assets/motion-kit/`). `const K = MAK(tl)` 한 줄로 화면 폭 맞춤(`fitWidth`), 등장(`up`, `pop`, `maskRise`, `typeOn`, `slam`), 가변 폰트 축(`axis`), 카메라(`pushIn`, `whipIn/Out`), 패널(`panelWipe`), 브랜드 링 아이리스(`ringWipe`, 루프 이음새 포함), 단어 벽(`wordWall`, `gridStagger`), CSS 3D 돌출(`depthText`, `extrude`), 노이즈 필드(`noiseField`), 비트 스냅(`snap`, `strong`)을 쓴다. 실제 작업 예: [references/examples/claude-motion-shots.md](references/examples/claude-motion-shots.md) (15초 키네틱 타이포 쇼릴 재현 샷 리스트와 구현 메모). 블록이 더 맞으면 `npx hyperframes add <block>`. 어느 쪽인지는 샷 리스트의 구현 열을 따른다.

```bash
npx hyperframes check <project>          # lint + 런타임 검증 + 레이아웃 검사
npx hyperframes preview --background     # 스튜디오 미리보기 (선택, 끝나면 --stop)
npx hyperframes render <project> --quality draft --output <project>/renders/draft.mp4   # --output은 cwd 기준
```

- 초안은 `--quality draft`로 빠르게. 최종은 기본(`looks`) 또는 `--quality delivery`.
- 렌더 후 측정한다: `bash {baseDir}/scripts/frozen_time.sh <mp4> --ignore-tail <락업 길이>`, 단일 프레임 팝 `python3 {baseDir}/scripts/frame_pops.py <mp4> --allow <의도한 하드 컷 시각들>`, 오디오가 있으면 `bash {baseDir}/scripts/loudness.sh <mp4>`, 검수용 `bash {baseDir}/scripts/contact_sheet.sh <mp4> <project>/review/sheet.jpg 0.25 8 6`.
- **G4로 가기 전에 전체 영상 크리틱을 돌린다 (필수).** 새 서브에이전트에 MP4 경로, `brief.md`, 스타일 스펙만 주고 [references/critic-loop.md](references/critic-loop.md)의 프롬프트로 판정받는다. 내가 고친 목록이나 의도는 주지 않는다. 상위 지적 중 명백한 결함(충돌, 잘림, 빈 프레임, 0.6초 넘는 정지)은 고쳐 재렌더하고, 취향이 걸린 항목은 6단계 노트 초안으로 넘긴다. 결과를 `<project>/review/ledger.md`에 한 줄 남긴다.
- 음악·효과음·믹스는 [references/audio.md](references/audio.md)를 따른다. 효과음 후보는 `python3 {baseDir}/scripts/sfx_candidates.py`로 먼저 거르고, 오디오가 있으면 음악 전용 폴백도 렌더한다.
- 음악이 있으면 `npx hyperframes beats`로 비트를 뽑아 컷을 비트에 맞춘다 (도착 시점을 비트에: `at = beat - duration`).
- 루프 영상(`info` 사이니지 등)은 렌더 후 `python3 {baseDir}/scripts/loop_seam.py <mp4>`로 첫/끝 프레임 일치를 검증한다.
- 실전 함정(배경 제거 모델 한계, 마스크 오버레이 오탐, 대비 실패 등): [references/gotchas.md](references/gotchas.md)

### 6단계 — 감독 노트 루프 (G4)

첫 렌더는 보통 80%다. 마지막 20%는 정확한 노트에서 나온다.

- 사용자 노트를 [references/director-notes.md](references/director-notes.md) 의 카메라 어휘로 해석해 **구체적인 파라미터 변경**으로 바꾸고, 무엇을 바꿨는지 장면·줄 단위로 보고한다.
- "더 좋게", "더 역동적으로" 같은 모호한 노트가 오면 추측으로 랜덤 수정하지 말고, 카메라 어휘로 된 2–3개 해석을 제시해 고르게 한다.
- 노트가 필요한데 사용자가 막막해하면 에이전트가 먼저 감독 노트 초안 3–5개를 제안한다 (예: "장면 2→3 크로스페이드를 하드 컷으로", "CTA 버튼에 1.0→1.08 푸시 인"). 초안의 근거는 5단계 전체 영상 크리틱의 상위 지적이다. 사용자 노트와 크리틱이 다르면 사용자가 우선이다.
- 노트를 반영해 재렌더할 때마다 **또 다른 새 서브에이전트**로 검증 크리틱을 돌려 이전 지적과 노트를 FIXED / PARTLY / STILL PRESENT로 확인하고 회귀를 찾는다. 원장에 한 줄 추가.
- 수정은 해당 장면만 고치고 재렌더한다. 전체를 다시 쓰지 않는다.
- `motion` 모드는 렌더 후 `snapshot --against`로 샷별 참조 대비 차이를 카메라 어휘로 정리해 **노트 초안으로 먼저 제시**한다 (예: "4번 패널 닫힘이 참조보다 2배 느림 → 0.3s로").

## 완료 보고

다음을 구분해 보고한다: 최종 MP4 경로, 포스터 프레임, 컨택트 시트, 선택된 참조/스토리보드, 적용된 노트 목록, 실행한 검증(`check`, `snapshot`, `frozen_time.sh`, `frame_pops.py`, `loudness.sh`)과 그 수치, 크리틱 원장(`review/ledger.md`: 라운드별 지적 → 변경 → 측정 전/후), 오디오가 있으면 음악 전용 폴백, 미해결 항목. 측정한 것과 실제로 듣거나 본 것, 샘플링 검수와 전수 검수를 구분한다. 실행하지 않은 검사를 통과했다고 말하지 않는다.

## 참고 파일

- [references/modes.md](references/modes.md) — 모드 판별표, 모드별 인테이크·게이트·기본값
- [references/shot-decomposition.md](references/shot-decomposition.md) — 참조 → 샷 리스트, 기법 → 블록/룰/kit 매핑표, 참조 대비 검증
- [references/motion-craft.md](references/motion-craft.md) — 모티프 연속성, 페이싱 곡선, 비트 동기, 이징 사전, 가변 폰트, 3D·셰이더 원칙
- [references/motion-grammar.md](references/motion-grammar.md) — 장면 사이를 잇는 여섯 규칙, 구도·페이싱 수치, 메커니즘 카탈로그, 런치 영상 참조 28편
- [references/prompt-motion-patterns.md](references/prompt-motion-patterns.md) — prompt-motion 갤러리 232편에서 뽑은 패턴: 참조 없는 쇼릴 대응, 연속 모티프, 금지 목록, 비트 그리드 구조, 카메라·커서, 닫힌 형태 스프링, 효과음 피크 정렬, 구현 함정
- [references/film-spec-template.md](references/film-spec-template.md) — G2 후 `film-spec.md` 6블록 형식 (입력 / 방향·금지 / 구조 / 빌드 / 함정 / 멈춤 지점)
- [references/critic-loop.md](references/critic-loop.md) — 빌더 ≠ 판정자, 게이트별 크리틱 라운드, 크리틱 프롬프트, 원장
- [references/audio.md](references/audio.md) — 음악 선택·편집, 효과음 규칙, 대역별 레벨, 믹스 목표
- [references/three-d.md](references/three-d.md) — 결정적 Three.js 렌더 계약, 랩 먼저, 히어로 모션 실측, 모션 블러, 사실감 체크리스트
- [references/gotchas.md](references/gotchas.md) — 실전 함정과 해결 (소재 누끼, check 오탐, 루프 이음새)
- [references/setup.md](references/setup.md) — HyperFrames / Remotion / 21st 설치·확인
- [references/reference-analysis.md](references/reference-analysis.md) — 참조 영상을 스타일 스펙으로 바꾸는 법
- [references/storyboard-template.md](references/storyboard-template.md) — brief.md, 스토리보드 3안 형식
- [references/director-notes.md](references/director-notes.md) — 카메라 어휘 → 파라미터 변경표, HyperFrames 블록 매핑
- [references/quality-bar.md](references/quality-bar.md) — 측정 기준 + "싸구려로 읽히는" 신호 체크리스트 + 클라이언트 거절 문구
- `scripts/setup.sh` — HyperFrames / Remotion / ffmpeg / yt-dlp 확인 및 자동 설치
- `scripts/find_refs.py` — whatships.com 카탈로그 검색
- `scripts/find_motion_refs.py` — prompt-motion.com 갤러리 검색 (영상 URL + 프롬프트, `--structured`, `--aspect`, `--stack`, `--show`)
- `scripts/analyze_ref.sh` — 참조 영상 다운로드 + 컷/변화 피크 검출 + 컨택트 시트(`--fps 4`로 타임스탬프 밀도 시트) + 팔레트
- `scripts/loop_seam.py` — 루프 영상 첫/끝 프레임 일치 검증
- `scripts/frozen_time.sh` — 렌더의 정지 구간·최장 홀드 측정 (0.6초 초과 홀드가 있으면 exit 1)
- `scripts/frame_pops.py` — 이웃 대비 3배 넘게 튀는 단일 프레임 팝 검출 (`--allow`, `--allow-range`로 의도한 컷 제외, 발견 시 exit 1)
- `scripts/loudness.sh` — 통합 LUFS, LRA, true peak, 초당 short-term 음량
- `scripts/contact_sheet.sh` — 렌더 검수·크리틱용 컨택트 시트 (전환 밀도 창 포함)
- `scripts/sfx_candidates.py` — 효과음 후보의 저역·고역 비율, 길이로 사전 거르기 (numpy 필요)
- `assets/motion-kit/` — 검증된 GSAP 헬퍼 (`kit.js`, `kit.css`)
