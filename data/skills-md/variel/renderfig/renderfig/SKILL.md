---
name: renderfig
description: Figma .fig 파일의 프레임을 PNG/JPG로 렌더링합니다. 텍스트, 이미지, 스타일을 오버라이드하여 템플릿 기반 이미지를 생성할 수 있습니다.
---

# renderfig 스킬

당신은 Figma `.fig` 파일을 이미지로 렌더링하는 전문가입니다. `renderfig` CLI 도구를 사용하여 .fig 파일의 특정 프레임을 PNG/JPG로 렌더링하고, 텍스트/이미지/스타일을 프로그래밍적으로 수정할 수 있습니다.

## 설치

renderfig를 사용하려면 먼저 프로젝트에 패키지를 설치하고 Playwright Chromium을 준비해야 합니다.

```bash
npm install -g renderfig
npx playwright install chromium
```

> Playwright가 스크린샷 촬영에 Chromium을 사용하므로, 최초 1회 `npx playwright install chromium`이 필요합니다. 이미 설치되어 있다면 생략 가능합니다.

설치가 되어 있지 않은 상태에서 사용자가 renderfig 작업을 요청하면, 먼저 위 설치를 진행하세요.

## 도구 개요

renderfig는 다음과 같은 파이프라인으로 동작합니다:

```
.fig 파일 → parsefig (파싱) → 노드 트리 + 이미지 추출
  → 오버라이드 적용 → HTML/CSS 생성 → Playwright 스크린샷 → PNG/JPG 출력
```

## 작업 절차

### 1단계: .fig 파일 구조 파악

작업 전 반드시 `inspect` 명령으로 파일 구조를 먼저 확인하세요.

```bash
# 페이지(캔버스) 목록 확인
npx renderfig inspect <파일경로>

# 특정 페이지의 프레임 목록 확인
npx renderfig inspect <파일경로> "페이지 이름"

# 프레임 내부 노드 구조 확인 (depth로 깊이 조절)
npx renderfig inspect <파일경로> "페이지/프레임" --depth 3

# 전체 트리 확인
npx renderfig inspect <파일경로> "페이지/프레임" --depth all
```

inspect 출력에서 다음을 확인합니다:
- **노드 이름**: 오버라이드 `target`으로 사용할 이름
- **노드 타입**: `[TEXT]`는 텍스트 교체 가능, `(image)`는 이미지 교체 가능
- **노드 크기**: 렌더링 결과의 기대 크기
- **mixed styles**: TEXT 노드에 여러 스타일(폰트 크기, 굵기 등)이 혼합된 경우 각 런별 스타일 정보가 표시됩니다

### 2단계: 렌더링

```bash
npx renderfig render <파일경로> "페이지/프레임" -o output.png
```

### 3단계: 오버라이드 적용 (필요한 경우)

#### 텍스트 교체 `--text`

`--text "노드이름=새로운 텍스트"` 형식으로 텍스트 레이어의 내용을 교체합니다. 노드 이름은 1단계 inspect에서 확인한 이름을 사용합니다.

```bash
# 전체 교체
npx renderfig render design.fig "프로필 카드/Channy" \
  --text "Channy (차니)=새이름" \
  --text "Maker=디자이너" \
  -o output.png
```

**부분 교체 (스타일 보존)**: `--text "노드이름//검색텍스트=대체텍스트"` 형식으로 텍스트의 일부만 교체하면서 기존 스타일(폰트 크기, 굵기 등)을 보존합니다. `//`로 노드이름과 검색어를 구분합니다.

```bash
# "진짜 자산관리 시작" 부분만 교체, 나머지 텍스트와 스타일 유지
npx renderfig render design.fig "홈페이지/배너" \
  --text "타이틀//진짜 자산관리 시작=스마트한 돈 관리" \
  -o output.png
```

전체 교체 시에도 줄 수가 같으면 라인별 스타일이 보존됩니다. 예를 들어 원본이 2줄(1줄 Medium, 2줄 Bold)이면 교체 텍스트도 2줄일 때 각 줄의 스타일이 유지됩니다.

#### 이미지 교체 `--image`

`--image "노드이름=이미지파일경로"` 형식으로 이미지 fill을 교체합니다.

```bash
npx renderfig render design.fig "프로필 카드/Channy" \
  --image "사진=./new-photo.jpg" \
  -o output.png
```

#### 스타일 수정 `--style`

`--style "노드이름.속성=값"` 형식으로 스타일 속성을 수정합니다.

```bash
npx renderfig render design.fig "프로필 카드/Channy" \
  --style "Channy (차니).fontSize=40" \
  --style "Channy (차니).color=#ff0000" \
  -o output.png
```

**텍스트 런 단위 스타일 수정**: `--style "노드이름//검색텍스트.속성=값"` 형식으로 mixed text 내 특정 부분의 스타일만 변경합니다. `--text`의 `//` 문법과 동일합니다.

```bash
# 첫째 줄은 ExtraBold, 둘째 줄은 Light
npx renderfig render design.fig "홈페이지/배너" \
  --style "타이틀//진짜 자산관리 시작.fontWeight=ExtraBold" \
  --style "타이틀//위스키캣 가계부.fontWeight=Light" \
  -o output.png
```

지원하는 스타일 속성:

**위치 & 크기**: `x`, `y`, `width`, `height`

**색상 & 외관**: `color` (hex), `backgroundColor` (hex), `opacity` (0-1), `visible` (true/false)

**Border**: `cornerRadius`, `borderRadiusTopLeft`, `borderRadiusTopRight`, `borderRadiusBottomLeft`, `borderRadiusBottomRight`, `strokeColor` (hex), `strokeWeight`

**Typography** (TEXT 노드): `fontSize`, `fontFamily`, `fontWeight` (Bold 등), `textAlign` (LEFT/CENTER/RIGHT), `textAlignVertical` (TOP/CENTER/BOTTOM), `lineHeight` (px), `lineHeightPercent` (%), `letterSpacing` (px), `textDecoration` (UNDERLINE/STRIKETHROUGH)

**Auto Layout** (FRAME 노드): `gap`, `padding`, `paddingHorizontal`, `paddingVertical`, `paddingTop`, `paddingRight`, `paddingBottom`, `paddingLeft`, `alignItems` (MIN/CENTER/MAX), `justifyContent` (MIN/CENTER/MAX/SPACE_BETWEEN)

#### 폰트 지정 `--font`

`--font "폰트패밀리=폰트파일경로"` 형식으로 로컬 폰트를 지정합니다. 지정하지 않은 폰트는 Google Fonts에서 자동 로딩을 시도하고, Google Fonts에도 없으면 시스템 폰트로 폴백합니다.

```bash
npx renderfig render design.fig "프로필 카드/Channy" \
  --font "Pretendard=./fonts/Pretendard-Regular.woff2" \
  -o output.png
```

### 출력 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `-o, --output <path>` | 출력 파일 경로 (필수) | - |
| `--format png\|jpeg` | 출력 포맷 | 확장자에서 자동 감지 |
| `--quality <n>` | JPEG 품질 (0-100) | - |
| `--scale <n>` | 디바이스 스케일 팩터 | 1 |

## Programmatic API

Node.js 코드에서 직접 사용할 수도 있습니다:

```typescript
import { renderFrame } from 'renderfig';

const buffer = await renderFrame({
  figFile: './design.fig',
  frameName: '프로필 카드/Channy',
  output: './output.png',
  scale: 2,
  overrides: [
    // 전체 교체
    { type: 'text', target: 'Channy (차니)', value: '새이름' },
    // 부분 교체 (search로 해당 부분만 교체, 스타일 보존)
    { type: 'text', target: '타이틀', search: '원래텍스트', value: '새텍스트' },
    { type: 'image', target: '사진', src: './photo.jpg' },
    { type: 'style', target: 'Maker', props: { fontSize: 24, color: '#0066ff' } },
    // 텍스트 런 단위 스타일 변경
    { type: 'style', target: '타이틀', search: '위스키캣 가계부', props: { fontWeight: 'Light' } },
    // 동일 이름 노드 구분: 인덱스 문법
    { type: 'text', target: '이메일[1]', value: 'second@email.com' },
  ],
  fonts: [
    { family: 'Pretendard', src: './fonts/Pretendard-Regular.woff2' },
  ],
});
```

## 작업 지침

- **항상 inspect 먼저**: 렌더링 전 반드시 `inspect`로 구조를 파악하세요. 노드 이름을 정확히 알아야 오버라이드가 동작합니다.
- **target 매칭**: 노드 이름 그대로 사용하거나 `/` 구분 경로 (예: `기본 정보/Channy (차니)`)로 지정합니다. 같은 이름의 노드가 여러 개면 경로를 사용하거나 `이름[n]` 인덱스 문법 (0-based)으로 구분합니다 (예: `이메일[0]`, `이메일[1]`).
- **대량 생성**: 같은 템플릿으로 여러 이미지를 만들 때는 Programmatic API를 사용하는 스크립트를 작성하세요.
- **폰트 주의**: 한국어 폰트(Pretendard, SUIT 등)는 Google Fonts에 없는 경우가 많으므로 `--font`로 직접 지정해야 정확합니다.
- **벡터 지원**: VECTOR, BOOLEAN_OPERATION 등 벡터 노드는 fillGeometry blob을 SVG `<path>`로 디코딩하여 렌더링합니다. blob이 없는 경우 색상 채우기 사각형으로 폴백합니다.
- **Mixed text styles**: 하나의 TEXT 노드 내에서 여러 스타일(폰트 크기, 굵기 등)이 혼합된 경우 자동 감지하여 `<span>` 단위로 올바르게 렌더링합니다.
- **Hug sizing**: Auto Layout 프레임의 Hug Contents(자동 크기 조절) 설정이 올바르게 반영됩니다.
- **렌더링 결과 확인**: 렌더링 후 출력 이미지를 열어 결과를 확인하고, 필요하면 오버라이드를 조정하세요.
