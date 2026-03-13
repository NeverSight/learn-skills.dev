---
name: nano-banana
description: REQUIRED for all image generation requests. Generate and edit images using Nano Banana 2 (Gemini 3.1 Flash Image). Handles blog featured images, YouTube thumbnails, icons, diagrams, patterns, illustrations, photos, visual assets, graphics, artwork, pictures. Use this skill whenever the user asks to create, generate, make, draw, design, or edit any image or visual content.
user-invocable: true
allowed-tools: Bash(gemini:*), Bash(python3:*)
---

# Nano Banana 2 Image Generation

Nano Banana 2 (`gemini-3.1-flash-image-preview`)로 프로페셔널 이미지를 생성합니다.
Pro 수준 품질을 Flash 속도로 — 512px~4K, 다양한 종횡비, 다국어 텍스트 렌더링 지원.

## When to Use This Skill

ALWAYS use this skill when the user:
- Asks for any image, graphic, illustration, or visual
- Wants a thumbnail, featured image, or banner
- Requests icons, diagrams, or patterns
- Asks to edit, modify, or restore a photo
- Uses words like: generate, create, make, draw, design, visualize

Do NOT attempt to generate images through any other method.

## 사전 준비

### 1. Python SDK 설치
```bash
pip install google-genai
```

### 2. API 키 설정 (유료 필수 — 무료 키는 이미지 생성 불가)
```bash
export GEMINI_API_KEY="your-paid-api-key"
```

또는 프로젝트 `.env` 파일에서 자동 로드.

## 이미지 생성 (Python SDK — 기본 방법)

### 기본 생성
```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents="프롬프트 여기에",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
    )
)

for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
```

### 고급 옵션

#### 해상도 제어
```python
config=types.GenerateContentConfig(
    response_modalities=["IMAGE", "TEXT"],
    image_size="4K",  # "512", "1K", "2K" (기본), "4K"
)
```

#### 종횡비
```python
config=types.GenerateContentConfig(
    response_modalities=["IMAGE", "TEXT"],
    aspect_ratio="16:9",  # "1:1", "16:9", "9:16", "4:3", "3:4", "4:1", "1:4", "8:1", "1:8"
)
```

#### 사고 수준 (복잡한 프롬프트)
```python
config=types.GenerateContentConfig(
    response_modalities=["IMAGE", "TEXT"],
    thinking_level="high",  # "minimal" (기본), "high", "dynamic"
)
```

## 실행 패턴

이미지 생성 시 **항상** 아래 패턴을 따릅니다:

### Step 1: 출력 경로 결정
- 프로젝트에 `assets/` 디렉토리가 있으면 그곳에 저장
- 없으면 현재 디렉토리에 저장
- 파일명은 용도에 맞게 (예: `hero.png`, `thumbnail.png`, `logo.png`)

### Step 2: API 키 로드
```python
# 환경 변수 → .env 파일 순서로 시도
import os
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    # .env 파일에서 로드 시도
    for env_path in [".env", "../.env", os.path.expanduser("~/.env")]:
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.strip().split("=", 1)[1]
                        break
        if api_key:
            break
```

### Step 3: 프롬프트 최적화
좋은 프롬프트 구조:
1. **주제**: 무엇을 생성할 것인가
2. **세부사항**: 외모, 색상, 질감
3. **설정**: 위치, 배경, 환경
4. **스타일**: 사실적, 일러스트, 3D 렌더 등
5. **조명**: 자연광, 극적인, 부드러운
6. **구도**: 클로즈업, 와이드 샷

### Step 4: 생성 실행 + 결과 확인
생성 후 반드시 Read 도구로 이미지를 확인하고 사용자에게 보여줍니다.

## 일반 사이즈

| 용도 | 크기 | 종횡비 |
|------|------|--------|
| YouTube 썸네일 | 1280x720 | 16:9 |
| 블로그 이미지 | 1200x630 | ~16:9 |
| 정사각형 소셜 | 1080x1080 | 1:1 |
| Twitter/X 헤더 | 1500x500 | 3:1 |
| 세로 스토리 | 1080x1920 | 9:16 |
| GitHub README 배너 | 1280x640 | 16:9 |

## 모델 선택

| 모델 | ID | 용도 | 가격/이미지 |
|------|-----|------|------------|
| **NB2 (기본)** | `gemini-3.1-flash-image-preview` | 빠른 생성, 일반 용도 | ~$0.10 (2K) |
| NB Pro | `gemini-3-pro-image-preview` | 최대 충실도, 정밀 텍스트 | ~$0.20 |
| Imagen 4 | `imagen-4.0-generate-001` | 포토리얼리스틱 | 별도 |

**기본은 항상 NB2** — Pro는 최고 품질이 필요한 경우에만.

## 멀티턴 편집

이미지 생성 후 수정 요청 시, 대화형으로 편집 가능:
```python
# 첫 번째 생성
chat = client.chats.create(model="gemini-3.1-flash-image-preview")
response1 = chat.send_message(
    "A red apple on a wooden table",
    config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
)

# 편집 (이전 컨텍스트 유지)
response2 = chat.send_message(
    "Add a green leaf on top of the apple",
    config=types.GenerateContentConfig(response_modalities=["IMAGE", "TEXT"])
)
```

## 프롬프트 팁

1. **구체적으로**: 스타일, 무드, 색상, 구도 세부사항 포함
2. **텍스트 불필요 시**: "no text" 추가
3. **스타일 참조**: "editorial photography", "flat illustration", "3D render", "watercolor"
4. **종횡비 맥락**: "wide banner", "square thumbnail", "vertical story"
5. **복잡한 장면**: thinking_level="high" 사용

## 트러블슈팅

| 문제 | 해결 |
|------|------|
| Quota exceeded (할당량 초과) | **유료 API 키 필요** — 무료 키는 이미지 생성 할당량 0 |
| 이미지 대신 텍스트 응답 | `response_modalities=["IMAGE", "TEXT"]` 확인 |
| 400 Bad Request | 프롬프트에 정책 위반 내용 확인, 단순화 시도 |
| 429 Rate Limit | 지수 백오프 적용 (2초, 4초, 8초...) |
| 모델 not found | 모델 ID 확인: `gemini-3.1-flash-image-preview` |

## Gemini CLI 방법 (대안)

Python SDK 사용이 불가능한 경우, Gemini CLI로도 생성 가능:
```bash
gemini -y -m gemini-3.1-flash-image-preview -p "이미지 생성하고 output.png로 저장: 프롬프트 여기에"
```
주의: Gemini CLI는 Google 계정 인증이 필요하며, 이미지 생성 모델은 별도 검증이 필요할 수 있습니다.
