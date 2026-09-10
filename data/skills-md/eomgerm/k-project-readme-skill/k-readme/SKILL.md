---
name: k-readme
description: 한국 개발 문화의 "프로젝트 소개서" 형태로 README를 작성한다. 부트캠프형(기술 서사)과 동아리형(서비스 홍보) 두 모드를 지원한다. "README 작성", "리드미 써줘", "readme 만들어줘", "프로젝트 소개 문서", "깃허브 README", "포트폴리오 README", "리드미 보강", "README 다시 써줘", "한국형 리드미" 요청에 사용. 부트캠프·IT 연합동아리(SOPT·디프만·YAPP·넥스터즈·매쉬업·DDD·코테이토·UMC·부스트캠프·우아한테크코스·카카오테크캠퍼스) 프로젝트 저장소가 주 대상이다.
license: MIT
---

# k-readme

한국 개발 문화의 README는 문서가 아니라 **소개서**다. 팀원 사진, 기획 배경, 성과 수치, 데모 GIF —
영미권 README에 없는 것들이 본문의 절반을 차지한다. 이 스킬은 그 형태를 재현한다.

## 절차

### 1. 모드 결정

인자로 받는다: `/k-readme 부트캠프` 또는 `/k-readme 동아리`.
인자가 없으면 `AskUserQuestion`으로 한 번 묻는다. 레포만 보고 추측하지 말 것 — 구분 근거가 없다.

| 모드 | 주인공 | 쓰는 곳 |
| --- | --- | --- |
| **부트캠프형** | 기술적 도전과 성능 개선 서사 | 부스트캠프, 우아한테크코스, 카카오테크캠퍼스, SSAFY, 소마 |
| **동아리형** | 서비스 소개와 화면 | SOPT, 디프만, YAPP, 넥스터즈, 매쉬업, DDD, 코테이토, UMC |

### 2. 기존 README 확인

`README.md`가 이미 있으면 **갱신 모드**로 들어간다. 기존 내용은 보존하고 빈 섹션만 채운다.
전면 재작성은 사용자가 명시적으로 요청할 때만. 남의 글을 지우는 건 사고다.

### 3. 레포 자동 분석

물어보기 전에 캐낼 수 있는 건 전부 캐낸다.

- **기술 스택** — `package.json`, `build.gradle(.kts)`, `Podfile`, `requirements.txt`, `pyproject.toml`, `go.mod`, `Cargo.toml`
- **폴더 구조** — 실제 트리를 읽고 각 디렉터리에 한국어 주석을 단다
- **개발 기간** — `git log --reverse --format=%ad --date=short | head -1` 과 최근 커밋
- **팀원** — `gh api repos/{owner}/{repo}/contributors` 로 로그인 ID·아바타 URL.
  `gh`가 없으면 `git log --format='%an'` 으로 이름만 뽑고 아바타는 비운다
- **컨벤션** — 커밋 메시지 패턴, `.github/PULL_REQUEST_TEMPLATE.md`, 브랜치 목록
- **배포** — `.github/workflows/`, `vercel.json`, `Dockerfile`

마지막에 **블록 조건을 한 번에 확정한다.** 6번에서 조립하다가 파일을 다시 뒤지지 않는다.

| 조건 | 판정 근거 |
| --- | --- |
| 서버 레포 | `pom.xml` `nest-cli.json` `manage.py`, 또는 매니페스트 안의 서버 프레임워크 의존성 — `build.gradle(.kts)`·`gradle/libs.versions.toml`·`buildSrc/**/*.gradle.kts`·`requirements*.txt`·`pyproject.toml`의 `spring-boot`(`org.springframework.boot`) `ktor-server` `django` `fastapi` `flask`, `go.mod`의 `gin-gonic` `echo` `fiber` `go-chi` `gorilla/mux` `swaggo`(또는 `main.go`가 `net/http`로 `ListenAndServe`를 부를 때), `Cargo.toml`의 `axum` `actix-web` `rocket`, `Package.swift`의 `vapor`, `package.json`의 `express` `koa` `fastify` `@hapi/hapi` — 단 같은 `package.json`에 `next` `react-dom` `vue`가 함께 있으면 정적·SSR 호스트이므로 서버로 치지 않는다 |
| 앱 레포 | `**/src/main/AndroidManifest.xml`·`**/src/androidMain/AndroidManifest.xml`(모듈명 무관 — KMP는 `androidApp/`, `composeApp/`을 쓴다), `Podfile` `*.xcodeproj`, `Project.swift` `Workspace.swift`(Tuist), `app.json`·`app.config.{js,ts}`의 `expo` 키 또는 `eas.json`(Expo는 android/ios를 prebuild로 만들고 커밋하지 않는다) |
| 실행할 수 있음 | **서버 레포이거나 앱 레포면 항상.** 그 밖에는 `package.json` 의 `scripts`, `gradlew`, `pubspec.yaml`, `manage.py`, `docker-compose*.yml`·`*.yaml`, `compose.yaml`, `Makefile` 중 하나. 마커는 켤지 말지가 아니라 **어떤 명령을 적을지** 고르는 데 쓴다 |
| API 문서 있음 | **서버 레포일 때만.** `springdoc` `springfox` `spring-restdocs` `swagger-ui-express` `swagger-jsdoc` `@nestjs/swagger` `ktor-server-swagger` `ktor-server-openapi` `drf-spectacular` `drf-yasg` `flasgger` `swaggo` `utoipa` 의존성(버전 카탈로그 포함), `docs/**/swagger.json`·`openapi.{yaml,json}`·`**/openapi/*.{yaml,json}`·`src/docs/asciidoc/**/*.adoc`, 또는 `fastapi`(OpenAPI 내장). `swagger-typescript-api` `openapi-typescript` `openapi-fetch` `orval` `openapi3-ts`는 프런트 코드 생성 도구라 근거가 아니다 |
| CI 있음 | `.github/workflows/*.yml` · `*.yaml` |

**파일 이름만으로 판정하지 않는다.** 안드로이드 프로젝트도 루트에 `build.gradle(.kts)`를 두므로
이름만 보면 서버로 걸린다 — 없는 DB의 ERD 섹션이 생긴다. 반대로 요즘
빌드 구성은 마커를 숨긴다: Gradle 컨벤션 플러그인은 `com.android.application`을 문자열로
남기지 않고, Gradle 버전 카탈로그는 의존성 좌표를 `gradle/libs.versions.toml`로 빼내
`build.gradle(.kts)`에 프레임워크 이름이 아예 없으며, Tuist는 `.xcodeproj`를 커밋하지 않고, 파이썬은 `requirements.txt` 대신
`pyproject.toml`을 쓴다. 워크플로와 compose 파일은 `.yml`과 `.yaml`이 섞인다. 위 마커로 판정한다.

**마커는 하위 디렉터리까지 찾는다.** 앱 모듈이 루트에 없고 `Aos/`, `android/`, `modules/app/`
아래 있는 저장소가 흔하다. 서버 마커도 `be/`, `backend/`, `server/` 아래 있을 수 있다.

**둘 다 걸리면 모노레포다 — 배타가 아니라 둘 다 켠다.** 클라이언트와 서버 디렉터리를 각각
적고, A4 ERD는 서버 쪽을 기준으로 쓴다. 부트캠프 저장소에 흔한 형태다.

### 4. 트러블슈팅 후보 발굴 (부트캠프형에서 필수)

이 섹션이 부트캠프형의 주인공인데 재료는 이미 저장소에 있다.

```
git log --format='%h %s' | grep -iE '^\w+ (fix|perf|refactor)'
gh pr list --state merged --limit 40 --json number,title,body
gh issue list --state closed --limit 30 --json number,title,body
```

여기서 **후보 5개를 뽑아 사용자에게 제시하고 고르게 한다.** 코드를 뒤져 최적화 흔적을
추측하지 말 것 — 헛발질이 잦다. 사용자가 나중에 "그 얘기도 넣어줘"라고 하면 그때
해당 커밋·PR을 더 깊이 읽어 섹션을 추가한다.

### 5. 질문은 3개까지

자동 분석으로 못 캐내는 것만 묻는다. 질문이 많은 스킬은 안 쓰게 된다.

1. 이 서비스를 한 줄로 소개하면?
2. 왜 만들었나? (기획 배경)
3. 붙일 링크를 한 번에 — 배포 주소, 스토어 링크, 위키, 노션, 피그마.
   부트캠프형은 여기서 4번 후보 선택도 함께 받는다.

### 6. 블록 조합

섹션을 정해진 순서로 채우는 게 아니라 **블록을 조합한다.** 조건이 켜진 블록만 쓴다.
마크업 실물은 `references/structure.md`, 뱃지는 `references/badges.md`를 읽어서 쓴다.
캡션과 소개 문장의 리듬이 잡히지 않으면 `references/tone-samples.md`로 종결어미 분포를
맞춘다 — 문장을 재사용하지는 않는다(아래 "베끼지 말 것").

| 레이어 | 블록 | 조건 |
| --- | --- | --- |
| **L0 히어로** | H1 배너 | 항상 |
| | H2 링크줄 | 항상 (링크 2개 이하면 생략하고 S1에 녹인다) |
| | H3 스토어 링크 | 앱 레포 |
| | H4 CI 상태 뱃지 | CI 있음 |
| **L1 요약** | S1 소개 + 불릿 | 항상 |
| | S2 개발 기간 | 항상 |
| | S3 목차 | 본문 8KB 초과 |
| | S4 기획 의도 | 5번 2번 질문에 답이 있을 때 |
| **L2 주인공** | T1 기술적 도전 | 부트캠프형 + 전후 수치가 있을 때 |
| | F1 핵심 기능 | 항상 (부트캠프형은 L3 끝으로) |
| **L3 본체** | K1 기술 스택 | 항상 |
| | A1 아키텍처 | 항상 (동아리형은 선택) |
| | A3 폴더 트리 | 부트캠프형 (동아리형은 생략) |
| | A4 ERD | 서버 레포 |
| | R1 실행 방법 | 실행할 수 있음 |
| | R2 API 명세 | API 문서 있음 |
| **L4 사람·규칙** | P1 팀원 | 항상 |
| | C1 컨벤션 | 실제로 지킨 규칙이 있을 때 |
| | C2 CI/CD 표 | 워크플로 2개 이상 |

순서는 레이어 순이다. **L2가 모드 스위치다** — 부트캠프형은 T1이 여기 오고 F1은 L3 끝으로
내려간다. 동아리형은 F1이 여기 오고 T1은 생략한다.

조건이 안 켜진 블록은 자리를 비우지 않고 그냥 빠진다. **부트캠프형인데 전후 수치가 없으면**
L2가 빈다 — T1을 켜지 않고 F1을 원래 자리(L3 끝)에 두고, L3의 K1·A1을 앞으로 당긴다.
재료 없는 주인공을 억지로 세우면 홍보체가 된다.

블록이 길어지면 `<details>`로 접는다. 컨벤션 전문과 50줄 넘는 폴더 트리가 대상이다.

**`H1` `L2` 같은 축약형은 이 문서와 `structure.md` 안에서만 쓰는 식별자다.** 사용자에게
보이는 텍스트에는 넣지 않는다 — 질문, 진행 안내, README 본문, `남은 작업` 주석 전부.
"L2 블록을 채웠습니다"는 아무 정보가 아니다. "기술적 도전 섹션을 채웠습니다"라고 쓴다.

### 7. 이미지 자리

마크업은 완성하고 `src`만 비운다. 깨져 보이는 게 기능이다 — 미완성 README를 그대로
커밋하는 걸 막는다.

```html
<img src="TODO_회원가입_데모_GIF" alt="회원가입 플로우" width="300"/>
```

파일 맨 아래에 남은 작업을 한 곳에 모은다.

```html
<!-- 남은 작업
  - [ ] 배너 이미지 (1200x600)
  - [ ] 회원가입 데모 GIF
  - [ ] 아키텍처 다이어그램
-->
```

**GIF 만들기**: 웹·CLI는 [demo-gif](https://github.com/conorbronsdon/demo-gif-skill) 스킬로 넘긴다
(`npx skills add conorbronsdon/demo-gif-skill`). 모바일 앱은 그 스킬이 다루지 않으니
`references/mobile-demo.md`를 읽어 직접 처리한다.

## 어투

한국 부트캠프·동아리 README 16개를 실측한 결과를 그대로 따른다.

### 문체

- **기본은 합쇼체** (`~합니다` / `~했습니다`). 실측 104회 대 17회로 압도적이다
- **서비스 소개와 기능 캡션은 해요체 허용** — "한 게임방에서 200명까지 플레이할 수 있어요!"
- **기술적 도전은 합쇼체 고정** — 여기서 해요체를 쓰면 가벼워진다
- **`~이다` / `~한다` 평서체 금지** — 16개 중 0회다. README에 쓰는 문체가 아니다
- **한 파일 안에서 섞어도 된다.** 통일하려 들면 오히려 AI 티가 난다. 실제 README는
  섹션마다 톤이 튄다. 동아리형은 해요체 비중을 높이고, 부트캠프형은 합쇼체로 간다

### 금지 표현

16개 레퍼런스에서 **거의 안 나온** 말들이다. 나오면 AI가 쓴 문장이라고 봐도 된다
(`~에 대해`만 한 저장소에서 2회 나왔고 나머지 일곱은 0회다).

`뿐만 아니라` `~에 대해` `원활하게` `혁신` `완벽한` `핵심적인` `경험을 제공` `최적화하였`

반대로 `~을/를 통해`(31회), `다양한`(3회), `효율적으로`(4회)는 실제로 쓰인다. 금지하면
문장이 뒤틀린다.

### 금지 마크업

레퍼런스 25개에서 **0회**다. 전부 프로필 README 관용구고 프로젝트 레포에는 안 쓴다.

`skillicons.dev` `devicon` `badgen.net` `forthebadge` `capsule-render` `readme-typing-svg`
`star-history` `mermaid`

뱃지는 shields.io만 쓴다. slug와 색은 `references/badges.md`에 있다 — 추측한 slug는
오류를 내지 않고 조용히 로고 없는 뱃지로 렌더되니 표를 확인한다.

### 구조 규칙

진짜 AI 티는 어휘가 아니라 구조다. 어휘 블랙리스트보다 이쪽이 효과가 크다.

- **3항 병렬 금지** — 모든 불릿이 3개면 티가 난다. 내용에 따라 2~5개로
- **길이 균일 금지** — 한 줄 불릿과 세 줄 불릿이 섞여야 사람이 쓴 것처럼 읽힌다
- **형용사 2개 겹치기 금지** — "빠르고 안정적인 실시간 동기화" 대신 "실시간 동기화"
- **한 문장 3절 금지** — `~하고, ~하며, ~하여` 로 잇지 말고 끊는다

### 과장의 기준

**구체적 수치**이거나 **팀이 실제로 쓸 말**이거나, 둘 중 하나여야 한다.
어느 쪽도 아닌 형용사는 지운다.

- 좋음: "목록 첫 렌더가 `2.41초`에서 `0.83초`로 줄었습니다" (소수점을 버리지 않는다)
- 좋음: "이거 모잇! 왤케 편해잇!" (팀 개성이 드러나는 표현)
- 나쁨: "혁신적인 사용자 경험을 제공합니다" (중간지대의 홍보체 — 아무도 안 쓴다)

### 이모지

- **헤딩에만 1개.** 문장 속에는 넣지 않는다. 실측이 거의 이 모양이다(헤딩 120개, 본문은
  캐치프레이즈와 컨벤션 체크표시 정도가 예외)
- **프로젝트 도메인에서 고른다.** 야구 서비스면 `⚾`, 독서 기록이면 `📖`.
  AI 티가 나는 이유는 개수가 아니라 `🚀✨💡` 같은 범용 이모지를 반복하기 때문이다

### 마무리

윤문이 더 필요하면 `humanize-korean` 스킬을 이어서 돌리라고 **제안만** 한다.
자동으로 부르지 않는다 — 의미가 드리프트할 수 있다.

제안할 때 **헤딩 이모지 1개와 합쇼체·해요체 혼용은 윤문 대상에서 빼라고 함께 알린다.**
그 스킬은 헤딩 이모지를 최고 심각도로 잡아 지우는데, 여기서는 실측으로 세운 규칙이다.

## 베끼지 말 것

`references/tone-samples.md`의 발췌는 **종결어미와 리듬을 재는 용도**다. 문장을 재사용하면
출처가 드러난다. 다음은 특히 눈에 띄는 것들이다.

- 트러블슈팅 라벨 `동기 / 행동 / 결과` — **구조는 훌륭하니 쓰되 라벨을 갈아쓴다.**
  `왜 했나 / 뭘 했나 / 어떻게 됐나`, `문제 / 시도 / 결과`, `상황 / 해결 / 성과` 등
- 모든 항목 끝에 같은 더보기 유도 문구를 반복하는 패턴 — 항목마다 다르게 쓰거나 링크만 남긴다
- 특정 팀의 팀명·캐치프레이즈·헤딩 문구 전체

### 프로젝트마다 달라지게 하는 장치

1. **헤딩에 프로젝트 고유 사실을 넣는다 (필수).** 이게 가장 강력하다.
   `## 🔥 기술적 도전` 대신 `## 🔥 200명이 한 방에 들어가기까지` 처럼 쓴다.
   헤딩만 고유어로 바뀌면 같은 골격이라도 다른 문서로 읽힌다
2. **이모지를 도메인에서 고른다 (필수)**
3. **불릿 개수를 내용에 맞춰 바꾼다 (필수)**
4. 레이어 안에서 블록 순서를 프로젝트 성격에 따라 조정한다 (선택)
5. 캡션 문체를 프로젝트 톤에 맞춘다 (선택)
