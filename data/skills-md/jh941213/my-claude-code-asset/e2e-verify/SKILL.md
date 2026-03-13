---
name: e2e-verify
description: "개발 완료 후 피처 기반 E2E 테스트 작성 및 실행. /verify 이후 실제 사용자 플로우를 검증합니다. Triggers on: e2e 검증, e2e-verify, E2E 테스트, 브라우저 테스트 실행. NOT for: 유닛 테스트, 타입체크, 빌드 검증."
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
---

# E2E 피처 검증

개발 + `/verify` 완료 후, 구현한 피처가 실제 브라우저에서 동작하는지 E2E 테스트로 검증합니다.

## 전제 조건
- `/verify` 통과 완료 (typecheck, lint, test, build)
- 앱이 로컬에서 실행 가능한 상태

## 워크플로우

### 1단계: 피처 분석
구현한 피처의 사용자 플로우를 파악합니다.
```
- 어떤 페이지에서 시작하는가?
- 어떤 인터랙션이 필요한가? (클릭, 입력, 네비게이션)
- 성공 조건은 무엇인가? (URL 변경, 텍스트 표시, 상태 변화)
- 엣지 케이스는? (빈 입력, 에러 응답)
```

### 2단계: 앱 실행
```bash
# package.json에서 dev/start 스크립트 확인
cat package.json | grep -A 5 '"scripts"'

# 앱 실행 (백그라운드)
npm run dev &
sleep 5  # 앱 준비 대기
```

### 3단계: E2E 테스트 작성
`e2e/` 디렉토리에 테스트 파일 생성합니다.

```bash
# 프로젝트에 기존 E2E 설정 확인
ls e2e/ 2>/dev/null || ls tests/e2e/ 2>/dev/null || ls __tests__/e2e/ 2>/dev/null

# 기존 E2E 프레임워크 확인 (Playwright, Cypress, agent-browser)
cat package.json | grep -E "playwright|cypress|agent-browser"
```

#### 프레임워크별 테스트 작성

**agent-browser 사용 시:**
```bash
#!/bin/bash
set -e
cleanup() { agent-browser close 2>/dev/null || true; }
trap cleanup EXIT

agent-browser open http://localhost:3000

# 스냅샷으로 요소 확인
agent-browser snapshot -i

# 피처 플로우 실행
agent-browser fill @email-input "test@example.com"
agent-browser click @submit-btn
agent-browser wait text "Success"

echo "PASS: Feature E2E test"
```

**Playwright 사용 시:**
```typescript
import { test, expect } from '@playwright/test';

test('피처명: 사용자 플로우', async ({ page }) => {
  await page.goto('/');
  await page.fill('[data-testid="email"]', 'test@example.com');
  await page.click('[data-testid="submit"]');
  await expect(page.locator('.success')).toBeVisible();
});
```

**Cypress 사용 시:**
```typescript
describe('피처명', () => {
  it('사용자 플로우를 완료한다', () => {
    cy.visit('/');
    cy.get('[data-testid="email"]').type('test@example.com');
    cy.get('[data-testid="submit"]').click();
    cy.contains('Success').should('be.visible');
  });
});
```

### 4단계: 테스트 실행
```bash
# agent-browser
bash e2e/test_feature.sh

# Playwright
npx playwright test e2e/feature.spec.ts

# Cypress
npx cypress run --spec "cypress/e2e/feature.cy.ts"
```

### 5단계: 실패 시 디버깅
```bash
# 스크린샷 캡처
agent-browser screenshot ./e2e/debug.png

# headed 모드로 재실행
agent-browser open http://localhost:3000 --headed

# 콘솔 에러 확인
agent-browser console --error
```

## 테스트 체크리스트
- [ ] 해피 패스 (정상 플로우) 통과
- [ ] 에러 케이스 (잘못된 입력, 네트워크 에러) 처리 확인
- [ ] 페이지 이동/라우팅 정상 동작
- [ ] UI 상태 변화 (로딩, 성공, 실패) 표시 확인
- [ ] 모바일 뷰포트에서도 동작 (해당 시)

## 검증 루프
각 테스트에서 실패 시:
1. 스크린샷/로그로 원인 파악
2. 코드 수정
3. `/verify` 다시 실행 (회귀 방지)
4. E2E 테스트 재실행
5. 모두 통과할 때까지 반복
