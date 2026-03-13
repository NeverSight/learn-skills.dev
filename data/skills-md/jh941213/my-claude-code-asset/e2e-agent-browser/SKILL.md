---
name: e2e-agent-browser
description: >
  agent-browser CLI를 활용한 E2E 테스트 자동화. 스냅샷 기반 접근성 트리와 ref 시스템으로 안정적인 브라우저 테스트를 수행.
  트리거: "E2E", "브라우저 테스트", "agent-browser", "e2e 테스트 작성", "E2E 테스트", "브라우저 자동화"
  안티-트리거: "유닛 테스트", "API 테스트", "pytest", "Jest 테스트만", "Playwright 직접 사용"
user-invocable: false
---

# E2E Testing with agent-browser

AI 에이전트를 위한 헤드리스 브라우저 자동화 CLI `agent-browser`를 활용하여 E2E 테스트를 작성하고 실행하는 종합 가이드입니다.

## 이 스킬을 사용할 때

- 웹 애플리케이션 E2E 테스트 작성
- 로그인/회원가입 플로우 테스트
- 폼 입력 및 제출 테스트
- 네비게이션 및 라우팅 테스트
- UI 상호작용 테스트 (클릭, 호버, 스크롤)
- 시각적 상태 확인 (요소 존재, 텍스트 내용)
- CI/CD 파이프라인에서 브라우저 테스트 실행

## 설치

```bash
# npm으로 설치 (권장)
npm install -g agent-browser

# Chromium 브라우저 다운로드
agent-browser setup

# Linux의 경우 시스템 의존성 추가 설치
agent-browser setup --with-deps
```

## 핵심 개념

### 1. 스냅샷 + Ref 워크플로우

agent-browser의 핵심은 **접근성 트리(Accessibility Tree)**와 **ref 시스템**입니다.

```bash
# 1. 페이지 열기
agent-browser open https://example.com

# 2. 접근성 스냅샷 가져오기 (ref 포함)
agent-browser snapshot -i
# 출력:
# - heading "Example Domain" [ref=e1] [level=1]
# - button "Submit" [ref=e2]
# - textbox "Email" [ref=e3]
# - link "Learn more" [ref=e4]

# 3. ref를 사용하여 요소와 상호작용
agent-browser click @e2        # 버튼 클릭
agent-browser fill @e3 "test@example.com"  # 텍스트 입력
agent-browser text @e1         # 텍스트 가져오기
```

### 2. 스냅샷 옵션

```bash
# 전체 접근성 트리
agent-browser snapshot

# 인터랙티브 요소만 (버튼, 입력, 링크)
agent-browser snapshot -i

# 컴팩트 모드 (빈 구조 요소 제거)
agent-browser snapshot -c

# 깊이 제한
agent-browser snapshot -d 3

# CSS 선택자로 범위 제한
agent-browser snapshot -s "#main"

# 옵션 조합
agent-browser snapshot -i -c -d 5
```

### 3. JSON 모드 (AI 에이전트용)

```bash
# JSON 출력으로 파싱 가능한 결과 반환
agent-browser snapshot --json
# {"success":true,"data":{"snapshot":"...","refs":{"e1":{"role":"heading","name":"Title"},...}}}
```

## E2E 테스트 패턴

### 패턴 1: 기본 페이지 테스트

```bash
#!/bin/bash
# test_homepage.sh

set -e  # 에러 시 즉시 중단

# 페이지 열기
agent-browser open https://myapp.com

# 페이지 타이틀 확인
TITLE=$(agent-browser title)
if [[ "$TITLE" != "My App" ]]; then
  echo "FAIL: Expected title 'My App', got '$TITLE'"
  exit 1
fi

# 주요 요소 존재 확인
agent-browser snapshot -i | grep -q "button.*Login" || {
  echo "FAIL: Login button not found"
  exit 1
}

echo "PASS: Homepage test"
agent-browser close
```

### 패턴 2: 로그인 플로우 테스트

```bash
#!/bin/bash
# test_login.sh

set -e

# 로그인 페이지 열기
agent-browser open https://myapp.com/login

# 스냅샷으로 요소 ref 확인
agent-browser snapshot -i
# - textbox "Email" [ref=e1]
# - textbox "Password" [ref=e2]
# - button "Sign In" [ref=e3]

# 이메일 입력
agent-browser fill @e1 "test@example.com"

# 비밀번호 입력
agent-browser fill @e2 "password123"

# 로그인 버튼 클릭
agent-browser click @e3

# URL 변경 대기
agent-browser wait url "**/dashboard"

# 대시보드 확인
URL=$(agent-browser url)
if [[ "$URL" != *"dashboard"* ]]; then
  echo "FAIL: Not redirected to dashboard"
  exit 1
fi

echo "PASS: Login flow"
agent-browser close
```

### 패턴 3: 폼 입력 및 유효성 검사 테스트

```bash
#!/bin/bash
# test_form_validation.sh

set -e

agent-browser open https://myapp.com/register

# 스냅샷으로 폼 요소 확인
agent-browser snapshot -i

# 빈 폼 제출 시도
agent-browser click @submit-btn

# 에러 메시지 대기
agent-browser wait text "Email is required"

# 에러 메시지 확인
agent-browser snapshot -i | grep -q "Email is required" || {
  echo "FAIL: Validation error not shown"
  exit 1
}

# 유효한 이메일 입력
agent-browser fill @email "valid@example.com"

# 이메일 에러 메시지 사라짐 확인
agent-browser snapshot -i | grep -q "Email is required" && {
  echo "FAIL: Email error should be gone"
  exit 1
}

echo "PASS: Form validation"
agent-browser close
```

### 패턴 4: 네비게이션 테스트

```bash
#!/bin/bash
# test_navigation.sh

set -e

agent-browser open https://myapp.com

# 네비게이션 메뉴 클릭
agent-browser click role:link "About"
agent-browser wait url "**/about"

# 뒤로 가기
agent-browser back
agent-browser wait url "**/home"

# 앞으로 가기
agent-browser forward
agent-browser wait url "**/about"

echo "PASS: Navigation test"
agent-browser close
```

### 패턴 5: 모달/다이얼로그 테스트

```bash
#!/bin/bash
# test_modal.sh

set -e

agent-browser open https://myapp.com

# 모달 트리거 버튼 클릭
agent-browser click @open-modal-btn

# 모달 나타날 때까지 대기
agent-browser wait @modal-dialog

# 모달 내용 확인
agent-browser snapshot -s "[role=dialog]" -i

# 모달 닫기
agent-browser click @close-modal-btn

# 모달 사라짐 확인 (isvisible 사용)
VISIBLE=$(agent-browser isvisible @modal-dialog 2>/dev/null || echo "false")
if [[ "$VISIBLE" == "true" ]]; then
  echo "FAIL: Modal should be closed"
  exit 1
fi

echo "PASS: Modal test"
agent-browser close
```

### 패턴 6: 드래그 앤 드롭 테스트

```bash
#!/bin/bash
# test_dnd.sh

set -e

agent-browser open https://myapp.com/kanban

# 드래그 앤 드롭 실행
agent-browser drag @task-1 @column-done

# 결과 확인
agent-browser snapshot -s "#column-done" | grep -q "Task 1" || {
  echo "FAIL: Task not moved"
  exit 1
}

echo "PASS: Drag and drop test"
agent-browser close
```

### 패턴 7: 파일 업로드 테스트

```bash
#!/bin/bash
# test_upload.sh

set -e

agent-browser open https://myapp.com/upload

# 파일 업로드
agent-browser upload @file-input "./test-file.pdf"

# 업로드 완료 대기
agent-browser wait text "Upload complete"

echo "PASS: File upload test"
agent-browser close
```

## 고급 기능

### 인증 세션 유지

```bash
# 프로필 디렉토리로 로그인 상태 유지
agent-browser open https://myapp.com --profile ~/.browser-profile/myapp

# 환경 변수로 설정
export AGENT_BROWSER_PROFILE=~/.browser-profile/myapp
agent-browser open https://myapp.com
```

### 세션 분리

```bash
# 독립된 세션으로 병렬 테스트
AGENT_BROWSER_SESSION=test1 agent-browser open https://myapp.com &
AGENT_BROWSER_SESSION=test2 agent-browser open https://myapp.com &
wait

# 세션 목록 확인
agent-browser sessions
```

### 네트워크 인터셉트

```bash
# 특정 요청 차단
agent-browser block "*.png"
agent-browser block "*analytics*"

# API 응답 모킹
agent-browser mock "/api/users" '{"users": [{"id": 1, "name": "Test"}]}'

# 네트워크 요청 모니터링
agent-browser requests
```

### 스크린샷 및 PDF

```bash
# 현재 화면 스크린샷
agent-browser screenshot ./screenshot.png

# 전체 페이지 스크린샷
agent-browser screenshot ./full.png --full

# PDF로 저장
agent-browser pdf ./page.pdf
```

### JavaScript 실행

```bash
# JS 코드 실행
agent-browser eval "document.title"
agent-browser eval "window.localStorage.getItem('token')"

# 복잡한 스크립트
agent-browser eval "
  const items = document.querySelectorAll('.item');
  return items.length;
"
```

## 테스트 러너 스크립트

### Node.js 테스트 러너

```javascript
// e2e/runner.js
const { execSync } = require('child_process');

const tests = [
  'test_homepage.sh',
  'test_login.sh',
  'test_form_validation.sh',
  'test_navigation.sh',
];

let passed = 0;
let failed = 0;

for (const test of tests) {
  console.log(`Running ${test}...`);
  try {
    execSync(`bash e2e/${test}`, { stdio: 'inherit' });
    passed++;
  } catch (error) {
    failed++;
    console.error(`FAILED: ${test}`);
  }
}

console.log(`\nResults: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
```

### npm 스크립트

```json
{
  "scripts": {
    "test:e2e": "node e2e/runner.js",
    "test:e2e:headed": "AGENT_BROWSER_HEADED=1 npm run test:e2e"
  }
}
```

## CI/CD 통합

### GitHub Actions

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install agent-browser
        run: |
          npm install -g agent-browser
          agent-browser setup --with-deps

      - name: Start app
        run: |
          npm run build
          npm run start &
          sleep 5

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload screenshots on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: e2e-screenshots
          path: e2e/screenshots/
```

### 클라우드 브라우저 사용 (Browserbase)

```yaml
# .github/workflows/e2e-cloud.yml
jobs:
  e2e:
    runs-on: ubuntu-latest
    env:
      AGENT_BROWSER_PROVIDER: browserbase
      BROWSERBASE_API_KEY: ${{ secrets.BROWSERBASE_API_KEY }}
      BROWSERBASE_PROJECT_ID: ${{ secrets.BROWSERBASE_PROJECT_ID }}

    steps:
      - uses: actions/checkout@v4
      - run: npm run test:e2e
```

## 디버깅

### headed 모드

```bash
# 브라우저 창 표시
agent-browser open https://myapp.com --headed
```

### 요소 하이라이트

```bash
# 요소 강조 표시
agent-browser highlight @button
```

### 콘솔 로그 확인

```bash
# 브라우저 콘솔 로그 보기
agent-browser console

# 에러 로그만
agent-browser console --error
```

### 트레이스 녹화

```bash
# 트레이스 시작
agent-browser trace start

# 테스트 실행
agent-browser open https://myapp.com
agent-browser click @button
# ...

# 트레이스 저장
agent-browser trace stop ./trace.zip
```

## 셀렉터 가이드

### Ref 기반 (권장)

```bash
# 스냅샷에서 얻은 ref 사용
agent-browser click @e1
agent-browser fill @e2 "text"
```

### CSS 셀렉터

```bash
agent-browser click "#submit-btn"
agent-browser fill ".email-input" "test@example.com"
agent-browser click "div > button.primary"
```

### 시맨틱 로케이터

```bash
# Role 기반
agent-browser click role:button "Submit"
agent-browser fill role:textbox "Email" "test@example.com"

# 텍스트 기반
agent-browser click text:label "Remember me"
agent-browser click text: "Sign Up"

# data-testid 기반
agent-browser click testid:submit-form
```

## 대기 전략

```bash
# 요소 대기
agent-browser wait @element

# 텍스트 대기
agent-browser wait text "Success"

# URL 패턴 대기
agent-browser wait url "**/dashboard"

# 시간 대기 (ms)
agent-browser wait 2000

# 로드 상태 대기
agent-browser wait load          # load 이벤트
agent-browser wait domcontentloaded
agent-browser wait networkidle   # 네트워크 안정화

# JS 조건 대기
agent-browser wait js "window.appReady === true"
```

## 모범 사례

### 1. 스냅샷 우선 접근

```bash
# 항상 스냅샷으로 현재 상태 파악
agent-browser snapshot -i

# 그 다음 ref로 상호작용
agent-browser click @e1
```

### 2. 안정적인 대기

```bash
# 하드코딩된 sleep 대신 조건 대기 사용
# BAD: agent-browser wait 5000
# GOOD:
agent-browser wait @loading-spinner
agent-browser wait text "Data loaded"
```

### 3. 에러 핸들링

```bash
#!/bin/bash
cleanup() {
  agent-browser close 2>/dev/null || true
}
trap cleanup EXIT

set -e
# 테스트 코드...
```

### 4. 환경별 설정

```bash
# .env.test
AGENT_BROWSER_PROFILE=~/.browser-test
AGENT_BROWSER_HEADED=0
BASE_URL=http://localhost:3000
```

### 5. 테스트 격리

```bash
# 각 테스트 전 쿠키/스토리지 초기화
agent-browser cookies clear
agent-browser local clear
agent-browser session clear
```

## 유용한 명령어 요약

| 명령어 | 설명 |
|--------|------|
| `agent-browser open <url>` | 페이지 열기 |
| `agent-browser snapshot -i` | 인터랙티브 요소 스냅샷 |
| `agent-browser click @ref` | 클릭 |
| `agent-browser fill @ref "text"` | 텍스트 입력 |
| `agent-browser text @ref` | 텍스트 가져오기 |
| `agent-browser wait text "msg"` | 텍스트 대기 |
| `agent-browser wait url "**/path"` | URL 대기 |
| `agent-browser screenshot ./ss.png` | 스크린샷 |
| `agent-browser isvisible @ref` | 가시성 확인 |
| `agent-browser close` | 브라우저 닫기 |

## 리소스

- **agent-browser 문서**: https://agent-browser.dev
- **GitHub**: https://github.com/vercel-labs/agent-browser
- **Playwright (내부 사용)**: https://playwright.dev
