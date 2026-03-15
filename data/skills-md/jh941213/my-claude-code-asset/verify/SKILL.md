---
name: verify
description: "작업 완료 후 코드 검증 (타입체크, 린트, 테스트, 빌드). Triggers on: 검증, verify, 테스트 돌려, 빌드 확인, 타입체크. NOT for: E2E 테스트, 코드 작성, 구현."
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Bash, Grep
---

# 코드 검증

작업 완료 후 코드를 검증합니다.

## 검증 순서
1. TypeScript 타입 체크 (있는 경우)
2. 린트 실행
3. 테스트 실행
4. 빌드 실행

## 실행 명령어
```bash
# package.json scripts 확인
cat package.json | grep -A 20 '"scripts"'

# 일반적인 검증 순서
npm run typecheck || npx tsc --noEmit
npm run lint
npm test
npm run build
```

## 검증 루프
각 단계에서 에러가 발생하면:
1. 즉시 수정
2. 다시 검증
3. 모두 통과할 때까지 반복

