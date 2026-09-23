---
name: html-in-canvas
description: HTML-in-Canvas API(drawElementImage)로 살아있는 DOM을 canvas/WebGL/three.js에 그리는 작업 전반. "HTML in canvas", "drawElementImage", "DOM을 canvas에 그리기", "canvas 속 input", "DOM을 텍스처로", CanvasUI 라이브러리 관련 요청 시 사용. 실검증된 함정 회피 규칙과 표준 골격 코드를 제공한다.
---

# HTML-in-Canvas 스킬

살아있는 DOM(`<input>`, `<video>`, CSS 애니메이션 포함)을 canvas 픽셀로 촬영해 자유 변형·상호작용하는 실험 API를 다루는 지식 패키지.

> **검증일 2026-08-20** — Chrome Canary, `chrome://flags/#canvas-draw-element` Enabled 기준.
> 실험 API라 빌드마다 이름·시그니처·동작이 다르다. 아래 규칙은 전부 **실제 빈 화면/예외를 디버깅해서 얻은 것**이므로 생략하면 같은 함정을 다시 밟는다.

## 절대 규칙 (위반 시 증상 병기)

| # | 규칙 | 위반 시 증상 |
|---|---|---|
| 1 | **촬영은 소스 canvas의 `paint` 이벤트 핸들러 안에서만.** rAF에서는 `src.requestPaint?.()`로 요청만 | `InvalidStateError: No cached paint record for element` — 매 프레임 거부되어 영원히 빈 화면 |
| 2 | 시그니처 3종 `(el,x,y)` → `(el,x,y,w,h)` → `(el)` 순차 try + **실패 시 세 에러 전부 나열** | 마지막 시도의 "3 arguments required"가 진짜 원인을 가림 |
| 3 | 소스 canvas 숨김은 `position:absolute; z-index:-1` 겹침만. `display:none`·`visibility:hidden`·`left:-9999px` 금지 | 페인트 생략 → 투명(빈) 촬영 |
| 4 | rAF 루프 전체 try/catch + 예외는 **페이지 내 빨간 에러 박스**에 표시, 루프는 계속 | 첫 프레임 예외로 루프가 조용히 죽어 "그냥 빈 화면" |
| 5 | `getImageData`/`toDataURL` 금지 (촬영한 canvas는 오염됨) | `SecurityError` |
| 6 | 소스 요소는 **소유 canvas(`layoutsubtree` 속성)의 자식**이어야 함. 효과는 버퍼 패턴: 소스에 촬영 → `drawImage`로 표시 canvas에 변형 복사 | 형제/외부 요소는 촬영 불가 또는 paint 기록 미보장 |
| 7 | 모든 실험 API 호출은 감지 가드 뒤에. 미지원 시 데모 대신 **요구 사항 안내만 표시** (Chromium 146 이상 + 플래그, DOM 폴백 금지) | 일반 브라우저에서 즉사 |
| 8 | 첫 90프레임(~1.5초)은 실패해도 에러 표시 유보 (초기 레이스) | 정상 동작인데 오탐 에러 |

## 표준 골격 (복사해서 시작)

```js
var drawFn = ['drawElementImage','drawElement'].find(n => typeof sctx[n] === 'function');
var lastErrs = null, captureOk = false, paintSeen = false, failStreak = 0;

function drawCompat() {
  var tries = [['(el,x,y)', () => sctx[drawFn](root, 0, 0)],
               ['(el,x,y,w,h)', () => sctx[drawFn](root, 0, 0, W, H)],
               ['(el)', () => sctx[drawFn](root)]];
  var errs = [];
  for (var [sig, run] of tries) {
    try { run(); return true; } catch (e) { errs.push(sig + ' → ' + e.name + ': ' + e.message); }
  }
  lastErrs = errs; return false;
}
function snap() {
  sctx.reset ? sctx.reset() : sctx.clearRect(0, 0, W, H);
  if (drawCompat()) { captureOk = true; failStreak = 0; return true; }
  if (!captureOk && ++failStreak === 90) showErrorBox(lastErrs.join('\n')); // 규칙 4·8
  return false;
}
src.addEventListener('paint', () => { paintSeen = true; snap(); }); // 규칙 1
function tick(t) {
  try {
    if (typeof src.requestPaint === 'function') src.requestPaint();
    if (!paintSeen) snap(); // paint 이벤트 없는 빌드 폴백
    effect(ctx, src, t);    // 마지막 성공 촬영본으로 효과 렌더
  } catch (e) { showErrorBox(e.name + ': ' + e.message); }
  requestAnimationFrame(tick); // 규칙 4: 예외가 나도 루프는 계속
}
```

## 상호작용 — 3가지 경로

1. **공식 정공법**: `drawElementImage()`가 반환하는 transform을 `el.style.transform`에 되적용 → 브라우저가 네이티브로 히트테스트·포커스·접근성 처리. 평면 배치에서만 성립(왜곡·원근 불가).
2. **`setHitTestRegions()` / `fireOnEveryPaint`**: 스펙에 있으나 빌드에 없을 수 있음 — `typeof` 감지 후 3번으로 폴백.
3. **수동 포워딩** (변형된 화면에서 유일한 방법):
   - 좌표: 포인터 → `getBoundingClientRect` 비율 보정 → fx 버퍼 좌표 → (효과의 역변환) → root 로컬 좌표
   - 히트테스트: root 하위 전 요소의 offset 누적 rect 중 가장 깊은 요소 (`elementFromPoint`는 canvas 위라 무용)
   - `pointerdown`에서 `e.preventDefault()` (canvas가 포커스를 뺏지 않게) 후:

| 대상 | 포워딩 | 비고 |
|---|---|---|
| input/textarea/select | `focus()` + `setSelectionRange(끝)` | 이후 타이핑·**한글 IME**는 브라우저가 처리, 다음 촬영에 자동 반영 |
| checkbox/radio | `click()` | focus만으론 토글 안 됨 |
| select/date/color/file | `showPicker()` (실패 시 focus) | **열린 팝업은 OS 레이어라 캡처에 안 찍힘** — 실제 화면 위에 뜸 |
| button/a/summary | `click()` + active 클래스 잠깐 토글 | |
| contenteditable | `focus()` | 기본 포워딩 대상 아님 — 직접 처리 |
| 스크롤 컨테이너 | fx의 `wheel` → `scrollTop += deltaY` | 스크롤 위치도 캡처됨 |
| dialog | `show()` 사용 | `showModal()`은 top layer → 캡처 밖 |

- `:hover`는 canvas 위라 안 걸림 → hover 클래스(.cui-hover 등)를 hit 결과로 토글하고 CSS에 `:hover, .cui-hover` 쌍선언, `style.cursor`도 직접 지정.
- 캐럿(커서) 깜빡임은 촬영에 안 보일 수 있음(구현차). 글자 반영은 확실.

## three.js / WebGL 통합

- 파이프라인: 소스 canvas(paint 모델로 촬영) → `THREE.CanvasTexture(src)` → 매 프레임 `texture.needsUpdate = true`.
- NPOT 텍스처: `minFilter = LinearFilter`, `generateMipmaps = false` 필수.
- 클릭 포워딩: Raycaster → `intersectObject(mesh)[0].uv` → `(uv.x*W, (1-uv.y)*H)` → 수동 히트테스트. 메시 명중 시 상호작용, 빗나가면 카메라 드래그로 구분.
- three.js는 **UMD 빌드를 vendor로 로컬 동봉** — `file://`에서 ES 모듈은 CORS로 차단됨. CDN 로드 금지.
- WebGL 직접 업로드는 `texElementImage2D`(신형→구형 시그니처 폴백) 감지 후 사용, 미지원 시 2D 캡처 → `texImage2D` 폴백.
- DOM→3D 역방향 제어(체크박스로 조명 토글 등)는 그냥 DOM 이벤트 리스너로 하면 됨 — DOM은 진짜니까.

## 흔한 실수 (이 세션에서 실제 발생)

- `var frame = mesh` + `function frame(t)` 같은 **var/function 이름 충돌** → rAF에 Mesh가 넘어가 "parameter 1 is not of type 'Function'". 파일 저장 전 동명 선언 검사.
- 문자열 치환 패치 시 **부분 문자열 오염** (들여쓰기만 다른 동일 코드가 여럿일 때) → 고유 앵커 포함해서 치환.
- 다크 테마 페이지에 흰 배경 콘텐츠 이식 시 글자색 상속 → white-on-white. 이식 콘텐츠에 `color` 명시.
- DOM 라벨이 컨테이너보다 넓어져 줄바꿈되면 배치 계산 전체가 틀어짐 → `white-space: nowrap` + 폰트 축소.
- 카드가 canvas 버퍼보다 커지면 아래가 잘림 → 최대 상태(아코디언 전부 펼침 등) 기준으로 높이 산정.

## CanvasUI 코어 (이 레포의 라이브러리)

위 규칙 전부를 캡슐화한 `core/canvas-ui.js` + 토큰 CSS. 새 데모는 직접 구현하지 말고 이걸 쓴다:

```js
var api = CanvasUI.create({
  mount: el, html: '<div>…진짜 DOM…</div>', width: 640, height: 400,
  effect(ctx, src, t, api) {},   // 생략 시 src 중앙 표시. 버퍼 패턴으로 자유 변형
  onFrame(t, api) {},            // 물리/파티클 갱신 (effect 앞)
  onHit(el, ev, api) {},         // true 반환 시 기본 포워딩 생략
});
// api: fx·ctx·src·sctx·root·center·toLocal(x,y)·hit(x,y)·requestRender()·destroy()·state{}
```

문서 사이트(`index.html`)는 `CUIDocs.register({ id, section: 'basics|official|components', name, oneLiner(한 문장·45자), code, mount(el)→api, knobs(el,api)?, renderDoc? })` 계약으로 페이지를 등록한다. 라우팅 이탈 시 셸이 `api.destroy()`를 호출하므로 window 리스너는 destroy를 래핑해 해제한다.

## 스타일 원칙

- 설명문은 페이지당 한 문장. 외부 CDN 금지(전부 로컬). 금액·숫자에 M/B/K 약어 금지(콤마 또는 만/억).
- 검증 데모(비디오 캡처 여부, iframe/:visited 프라이버시 등)는 **결과가 어느 쪽이든 화면에 표시**하고 이 문서에 실측 결과를 추가한다.
