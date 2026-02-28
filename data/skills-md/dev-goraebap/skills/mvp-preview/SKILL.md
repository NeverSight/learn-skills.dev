---
name: mvp-preview
description: "빠른 MVP·프로토타입 제작과 링크 공유. Actions: MVP 만들기, 프로토타입, 빠르게 구현, 데모 페이지, 기능 시연, prototype, demo, quick build, 아이디어 구체화, 클라이언트 공유, 팀 공유, 링크 공유, 기획 검토. Phases: 토론, 발견, 범위 확정, discovery, 핵심 가치, 핵심 기능, 스택 선택. Share: vercel, surge, cloudflared, tunnel, 배포, deploy, 공유 링크."
allowed-tools: Bash Read Write Edit
metadata:
  author: dev-goraebap
---

# MVP Preview

AI와 함께 핵심 기능을 빠르게 만들고 링크로 공유하는 워크플로우.

아이디어가 구체적이지 않아도 괜찮다. 토론하면서 범위를 좁히고, 최소한의 코드로 가치를 보여준 뒤, 링크 하나로 팀이나 클라이언트에게 전달한다.

## 언제 적용하나

- 아이디어나 기능을 빠르게 눈으로 확인하고 싶을 때
- 클라이언트·팀원에게 기획을 링크로 공유하고 싶을 때
- 완성도보다 방향성 검증이 목적일 때
- "이런 거 만들면 어떨까요?" 를 말 대신 코드로 보여주고 싶을 때

## 카테고리

| 카테고리 | 적용 상황 | 참조 파일 |
|----------|-----------|-----------|
| **제품 맥락** | 세션 간 맥락 유지, 요구사항·정책·도메인 정보 축적 | [brief.md](references/brief.md) |
| **토론** | 아이디어가 막연할 때, 범위를 좁히고 싶을 때, 무엇을 만들지 결정할 때 | [discovery.md](references/discovery.md) |
| **구현** | 스택 선택, MVP 빌드 원칙, 목업 데이터, 빠른 프로토타입 | [build.md](references/build.md) |
| **공유** | 로컬 서버 링크 공유, 빌드 배포, 브라우저 플레이그라운드 | [share.md](references/share.md) |

## 핵심 원칙

- **하나만**: 핵심 기능 하나를 완벽하게. 여러 기능을 어설프게 X
- **목업 데이터**: 실제 API 연결 불필요. 하드코딩된 데이터로 충분
- **해피 패스만**: 에러 처리·예외·엣지 케이스는 나중에
- **링크로 공유**: 노트북을 들고 가지 않아도 된다
- **매 작업 후 커밋**: 작업이 끝나면 바로 커밋 + `vN` 태그. 언제든 되돌릴 수 있어야 한다

## 실행 방법

### Step 0: 환경 확인

두 가지를 확인한다.

1. **git 설치 여부**: `git --version` 실행. 없으면 설치를 제안하고 진행한다
   - macOS: `brew install git`
   - Ubuntu/Debian: `sudo apt install git`
   - Windows: https://git-scm.com/download/win
2. **brief.md 확인**: 내용이 있으면 이전 맥락을 이어간다. 없으면 Step 1부터 시작한다

### Step 1: 토론

막연한 아이디어도 괜찮다. `discovery.md`의 질문 흐름으로 범위를 확정한다.

> "어떤 제품을 만들고 있나요? 이 MVP로 무엇을 보여주고 싶으세요?"

범위가 확정되면 `brief.md`를 업데이트하고 구현으로 넘어간다.

> **UI/UX를 더 잘 만들고 싶다면**
> `ui-ux-pro-max` 스킬이 설치되어 있으면 구현 전에 활용할 수 있다.
> 설치가 안 되어 있다면 아래 명령어로 설치할 수 있다:
> ```
> npx skills add https://github.com/nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max
> ```
> 설치 후 "이 MVP에 어울리는 디자인 추천해줘" 또는 원하는 스타일을 말하면 도움을 받을 수 있다.

### Step 2: 스택 확인 → 구현

구현에 들어가기 전 **반드시** 스택을 먼저 확인한다.

1. 현재 디렉토리에 `package.json`이 있으면 어떤 프레임워크인지 파악한다
2. 없으면 사용자에게 묻는다:
   > "어떤 방식으로 만들까요? (1) 단일 HTML 파일 — 빌드 없이 바로 공유 가능, (2) 사용 중인 프레임워크가 있으면 알려주세요"

스택이 확정되면 `build.md`의 방식에 따라 구현한다.

**단일 HTML 방식을 선택한 경우:**
- Tailwind CDN + Alpine.js를 사용한다. Vanilla JS로 DOM을 직접 조작하지 않는다
- 화면이 2개 이상이면 하나의 파일에 몰아넣지 않는다. HTML 파일을 화면별로 분리하고 `<a href>`로 연결한다

**프레임워크 방식을 선택한 경우:**
- 기존 프로젝트 구조에 새 페이지/컴포넌트를 추가한다. 별도 설정 없이 진행한다

구현이 끝나면 **즉시 커밋 + 태그**를 단다:

```bash
git add .
git commit -m "feat: MVP [한 줄 요약]"
git tag v1   # 다음 이터레이션은 v2, v3 ...
```

### Step 3: 결과 확인

구현한 화면을 사용자가 직접 브라우저에서 볼 수 있도록 안내한다. 개발 경험 유무에 따라 설명 방식을 조정한다.

**단일 HTML 파일인 경우 — 브라우저로 바로 열기**

> 파일 탐색기(Windows) 또는 Finder(macOS)에서 `index.html` 파일을 더블 클릭하세요. 브라우저가 자동으로 열립니다.

브라우저가 이미 열려 있다면:
> 브라우저 주소창에 파일을 드래그해서 놓으면 바로 열립니다.

**프레임워크 방식인 경우 — 개발 서버 실행**

`package.json`의 `scripts`를 확인해 실행 명령어를 파악한다. 프레임워크마다 다르다.

```bash
# 예시: Next.js, SvelteKit, Vite 계열
npm run dev

# 예시: Create React App
npm start

# 예시: 그 외 — package.json scripts 확인 후 적절한 명령어 안내
```

사용자에게는 확인한 명령어를 직접 알려준다:

> 터미널에 `[명령어]`를 입력하고 엔터를 누르세요. 터미널에 표시되는 주소(예: `http://localhost:3000`)를 브라우저 주소창에 입력하면 됩니다. 서버를 종료하려면 터미널에서 `Ctrl + C`를 누르세요.

**결과가 마음에 들지 않는 경우 — 이전 버전으로 되돌리기**

사용자가 "이전 버전이 나았어요" 또는 "v1로 돌아가 주세요"라고 하면 해당 태그로 되돌린다.

```bash
# 태그 목록 확인
git tag

# 특정 버전으로 되돌리기
git checkout v1
```

되돌린 뒤에는 현재 어느 버전인지 사용자에게 알려준다:
> "v1 버전으로 돌아왔습니다. 이 상태에서 다시 수정을 이어갈까요?"

### Step 4: 공유

`share.md`의 상황별 옵션을 골라 링크를 만든다.

| 상황 | 방법 |
|------|------|
| 지금 바로 링크 필요 (로컬 서버) | `cloudflared tunnel --url localhost:PORT` |
| 안정적인 URL 필요 (빌드 완료) | `surge ./dist my-name.surge.sh` |
| 프레임워크 프로젝트 자동 빌드 배포 | `npx vercel` |
| 단일 HTML 파일 | CodePen에 붙여넣기 |
