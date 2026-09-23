---
name: artifact-deck
description: 발표자료를 claude.ai Artifact HTML 덱으로 만든다. 템플릿을 복사해 <slide> 태그로 슬라이드를 채우고, 틀(jsDelivr의 @s-dante/artifact-deck)이 넘기기·전체화면·발표자 노트·발표자와 청중 창 동기화를 맡는다. "발표자료 만들어줘", "슬라이드 만들어", "덱 작성", "프레젠테이션", "발표 준비" 같은 요청에서 로드한다. 사용자가 .pptx 파일을 요구하면 쓰지 않는다.
---

# Artifact 발표 덱

발표자료는 처음부터 쓰지 않고 **이 스킬의 템플릿에서 시작한다.** 슬라이드 내용만 쓰면 되고, 넘기기·전체화면·발표자 노트·창 동기화는 틀 스크립트가 맡는다.

| 파일 | 내용 |
| --- | --- |
| `assets/template.html` | 틀이 쓰는 셸 마크업·CSS와 빈 슬라이드 세 장. 머리 주석에 슬라이드 문법이 있다 |
| `examples/deck-example.html` | 표·흐름도·슬라이더와 슬라이드별 스크립트를 쓴 완성 덱 |

경로는 이 `SKILL.md`가 있는 폴더 기준이다.

## 1. 쓰기 전에

1. `artifact-design` 스킬이 있으면 먼저 로드한다. Artifact 페이지 규칙의 정본은 그 스킬이다.
2. 내용을 정한다: 청중, 발표 시간, 슬라이드별 한 줄 메시지. 사용자가 내용을 주지 않았으면 목차를 먼저 제안하고 확인받는다.
3. `examples/deck-example.html`을 읽어 슬라이드 마크업과 슬라이드 CSS를 어떻게 쓰는지 본다.

## 2. 만드는 순서

1. `assets/template.html`을 작업 위치에 `<짧은-이름>.html`로 복사한다. 사용자가 경로를 정하지 않았으면 현재 프로젝트의 초안 폴더(없으면 스크래치패드)에 둔다.
2. `<title>`과 `<template id="slides">`의 `data-title`에 덱 제목을 쓴다. `<title>`은 2~4단어의 이름으로 짓는다.
3. `<template id="slides">` 안의 `<slide>`를 내용으로 채운다. 문법은 템플릿 머리 주석을 따른다.
   - `id`는 영문 소문자와 하이픈으로 짓는다. `#id` 링크로 그 슬라이드가 바로 열린다.
   - `label`은 하단 목록 이름, `section`은 그 슬라이드에서 시작하는 섹션 이름이다.
   - 표지와 마무리에는 `class="dark cover"`, `class="dark"`를 쓰고, 본문 슬라이드에는 `footer`를 붙인다.
   - 슬라이드마다 `<notes>`에 발표자가 할 말을 쓴다. 발표 노트의 기본값이 된다.
4. 슬라이드 전용 CSS는 `<style>` 끝에 더한다.
5. 조작이 필요한 슬라이드만 `<script type="text/slide">`를 넣는다 (4절).
6. 퍼블리시한다 (5절).

## 3. 슬라이드 쓰기 규칙

- **캔버스는 1920×1080 고정**이고, 틀이 화면 폭에 맞춰 축소한다. 슬라이드 안에서는 반응형 레이아웃을 만들지 않고 px로 쓴다. 본문 글자는 28px 이상, 제목은 템플릿의 `h2`(72px)를 쓴다.
- 기본 여백은 `.slide`의 `padding: 128px`이다. 내용이 1080px 높이를 넘지 않게 한 슬라이드에 메시지 하나만 둔다.
- 색은 템플릿 `:root`의 토큰(`--ink`, `--muted`, `--accent`, `--rule`, `--stage`, `--slide-dark` 등)으로만 쓴다. 새 색이 필요하면 `:root`, 다크 미디어 쿼리, `:root[data-theme="dark"]` 세 곳에 모두 정의한다.
- **틀 부분은 고치지 않는다**: 셸 마크업(`.shell` 이하)과 틀 CSS(`.bar`, `.viewport`, `.canvas`, `.panel`, `.notes`, `.nav`, `.strip` 등)는 `deck.js`와 짝이다.
- **`deck.js`를 로컬에 복사하거나 버전을 바꾸지 않는다.** 마지막 줄의 `<script src="https://cdn.jsdelivr.net/npm/@s-dante/artifact-deck@…/deck.js">`를 그대로 둔다.
- 차트 등 라이브러리가 필요하면 `cdnjs.cloudflare.com`이나 `cdn.jsdelivr.net/npm/`의 공식 UMD 빌드를 버전 고정으로 `deck.js` 앞에 링크한다. 그 밖의 도메인은 CSP에 막힌다.
- 이미지는 `data:` URI로 넣거나, 파일로 두고 퍼블리시 때 `files`로 함께 올린다.
- 페이지 스크립트를 별도 `.js` 파일로 만들지 않는다. 슬라이드 로직은 모두 `<script type="text/slide">`에 둔다.

## 4. 슬라이드별 스크립트

슬라이드가 화면에 붙을 때마다 실행되고 `slide`를 받는다.

| API | 설명 |
| --- | --- |
| `slide.root` | 이 슬라이드의 DOM (`.slide`) |
| `slide.values` | 덱 전체가 공유하는 조작 값 |
| `slide.interactive` | 이 화면에서 조작할 수 있는가. 목록 미리보기와 권한 없는 청중은 `false` |
| `slide.set(patch, { debounce })` | 조작 값을 바꾼다. 발표자와 청중 창에 양방향으로 동기화된다 |
| `slide.onUpdate(fn)` | 조작 값이 바뀔 때마다 `fn(values)`. 붙은 직후에도 한 번 불린다 |

- 요소는 `id`가 아니라 `data-*` 속성으로 찾는다. 하단 목록 미리보기에서는 `id`가 지워진다.
- 화면은 `onUpdate` 안에서만 그린다. 입력 이벤트에서는 `slide.set()`만 부른다. 그래야 다른 창의 조작도 똑같이 반영된다.
- `slide.values`의 키 이름은 덱 전체에서 겹치지 않게 짓는다. 모든 슬라이드가 한 객체를 공유한다.
- 기본값은 스크립트 안에 두고 `{ ...defaults, ...values }`로 합친다. 조작 값은 처음에 비어 있다.
- `slide.interactive`가 `false`인 화면에서는 틀이 입력 요소를 `disabled`로 만들고 `slide.set()`을 무시한다. 따로 처리하지 않는다.
- 인라인 이벤트 속성(`onclick="…"`)은 쓰지 않고 `addEventListener`로 건다.

## 5. 퍼블리시

로컬 스크립트가 없으므로 **HTML 파일을 빌드 없이 그대로** Artifact 도구의 `file_path`로 넘긴다.

1. 첫 퍼블리시에는 `icon: "slides"`, 한 문장 `description`과 아래 `capabilities`를 넣는다. 발표자·청중 동기화와 개인 노트에 필요하다. 현재 위치(`presentation`)는 편집 권한자만, 조작 값(`presentation/controls`)은 참여자 모두가 쓸 수 있다.
   ```json
   { "db": { "rules": [ { "path": "presentation", "write": "admin" },
                        { "path": "presentation/controls", "write": "interact" } ] },
     "user": {} }
   ```
2. 받은 아티팩트 주소를 `<template id="slides">`의 `data-url`에 적고, 같은 파일 경로로 다시 퍼블리시한다. 발표자 패널의 "청중 창 새로 열기"가 이 주소에 `#audience`를 붙여 연다.
3. 이후 수정도 같은 파일 경로로 다시 퍼블리시해 같은 URL을 유지한다. 다른 대화에서 고칠 때는 기존 `url`을 넘긴다.
4. 사용자에게 쓰는 법을 한 줄로 알린다: 발표자는 **발표자** 모드에서 노트를 보며 넘기고, 청중에게는 주소 끝에 `#audience`를 붙인 링크를 준다.

## 6. 확인

- 퍼블리시 전에 브라우저로 볼 수 있으면 본다. 파일에는 Artifact 스켈레톤이 없으므로 `<meta charset="utf-8">`를 앞에 붙인 임시 사본을 로컬 서버로 연다. `deck.js`는 CDN에서 받는다. 로컬에서는 아티팩트 db가 없어 동기화가 같은 브라우저의 탭끼리만(BroadcastChannel) 된다.
- 확인할 것: 슬라이드가 모두 하단 목록에 뜨는가, 넘치는 슬라이드가 없는가, 라이트·다크 둘 다 읽히는가, 폭 400px에서 셸이 깨지지 않는가, 콘솔 오류가 없는가.
