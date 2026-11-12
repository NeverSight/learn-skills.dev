---
name: agy-image
description: |
  Generate images via Antigravity CLI (agy) using Gemini's generate_image tool. Google OAuth — no API key needed.
  Antigravity CLI(agy)의 내장 generate_image 도구로 Gemini 이미지 생성. Google OAuth 인증으로 API 키 불필요.
  Usage: /agy-image cherry blossom hanok, /agy-image --out public/images space cat, /agy-image -n 3 seoul night
argument-hint: "[--out <path>] [-n <count>] <image prompt>"
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
---

# agy-image — AI Image Generation via Antigravity CLI (Gemini)

Generate images using Google Gemini's `generate_image` tool through Antigravity CLI (`agy`).
**No API key required** — uses Google OAuth (Gemini Pro subscription) authentication.

Antigravity CLI(`agy`)의 내장 `generate_image` 도구로 Gemini 이미지를 생성한다.
**API 키 불필요** — Google OAuth(Gemini 유료 구독) 인증 사용.

## How it works / 동작 원리

```
User prompt → Claude Code (/agy-image)
  → agy --print (Google OAuth auto-managed)
    → built-in generate_image tool (Gemini)
      → saved to specified path
```

---

## Step 1 — Verify agy CLI / agy CLI 확인

```bash
~/.local/bin/agy --help 2>/dev/null | head -3 || echo "NOT_FOUND"
```

If `NOT_FOUND`, stop:
> "Antigravity CLI 없음. https://antigravity.dev 에서 설치 후 로그인해."

## Step 2 — Parse Arguments / 인자 파싱

Extract from `$ARGUMENTS`:

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--out` | directory path | project root | Save location / 저장 위치 |
| `-n` | 1–4 | `1` | Number of images / 생성 장수 |

Remaining text → image prompt / 나머지 텍스트 → 이미지 프롬프트

If prompt is empty, ask via AskUserQuestion:
> "어떤 이미지를 생성할까? 프롬프트를 입력해줘."

## Step 3 — Determine Save Path / 저장 경로 결정

```bash
_PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
_OUT_DIR="${_PROJECT_ROOT}"
_TIMESTAMP=$(date +%Y%m%d-%H%M%S)
_FILENAME="agy-image-${_TIMESTAMP}"
```

- If `--out` specified, use that path / `--out` 지정 시 해당 경로 사용
- Single image: `agy-image-<timestamp>.png`
- Multiple (`-n > 1`): `agy-image-<timestamp>-1.png`, `-2.png`, ...
- Never overwrite existing files / 기존 파일 덮어쓰기 금지

## Step 4 — Generate Image / 이미지 생성

### Single image (default)

```bash
~/.local/bin/agy --print \
  "Use the generate_image tool to generate an image with this prompt: '${_PROMPT}'. Save the generated image to '${_OUT_DIR}/${_FILENAME}.png'. After saving, print the file path and file size in bytes." \
  --print-timeout 120s \
  2>&1
```

### Multiple images (-n > 1)

```bash
for i in $(seq 1 ${_N}); do
  ~/.local/bin/agy --print \
    "Use the generate_image tool to generate an image with this prompt: '${_PROMPT}'. Save the generated image to '${_OUT_DIR}/${_FILENAME}-${i}.png'. After saving, print the file path and file size in bytes." \
    --print-timeout 120s \
    2>&1
done
```

timeout: 120000ms (2 min) per image

## Step 5 — Verify & Display / 검증 및 표시

```bash
# 파일 존재 + 크기 확인 (1KB 미만이면 실패)
ls -la ${_OUT_DIR}/${_FILENAME}*.png
find ${_OUT_DIR} -name "${_FILENAME}*.png" -size -1k -exec echo "FAILED: {}" \;
```

Output format:
```
═══════════════════════════════════════════════
IMAGE GENERATED (Gemini) / 이미지 생성 완료
═══════════════════════════════════════════════
Prompt: <prompt used>
Count: <n>
Auth: Google OAuth (Gemini)
───────────────────────────────────────────────
<saved file path(s) + size>
═══════════════════════════════════════════════
```

**Always display the generated image using the Read tool.**
**생성된 이미지를 반드시 Read 도구로 표시한다.**

## Step 6 — Follow-up / 후속 안내

- "Run `/agy-image` again to generate another image."
- For Next.js projects: suggest moving to `public/images/` if needed.

## Error Handling / 에러 처리

| Error | Message |
|-------|---------|
| Auth expired | "Google OAuth 만료. 터미널에서 `agy` 실행 후 재로그인." |
| Timeout (>2min) | "생성 시간 초과. 프롬프트를 단순화해서 재시도." |
| Rate limit | "API 호출 제한. 잠시 후 재시도." |
| File < 1KB | "이미지 생성 실패. agy 출력 확인 후 재시도." |
| NOT_FOUND | "agy CLI 없음. ~/.local/bin/agy 확인." |

## Rules / 규칙

- Always use the Read tool to display generated images / 생성된 이미지는 반드시 Read로 표시
- Never overwrite existing files — always use timestamped filenames / 기존 파일 덮어쓰기 금지
- Always use full path `~/.local/bin/agy` to avoid IDE version conflict / IDE 버전 충돌 방지를 위해 항상 풀 경로 사용
- Verify file size after generation (< 1KB = failed) / 생성 후 파일 크기 검증
