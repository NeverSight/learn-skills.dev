---
name: tdd
description: 테스트 주도 개발 - 테스트 먼저 작성 후 구현. 트리거: "TDD", "테스트 먼저", "테스트 주도", "RED-GREEN-REFACTOR". 안티-트리거: "구현 먼저", "테스트 나중에".
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Bash
user-invocable: true
---

# TDD (테스트 주도 개발)

테스트를 먼저 작성하고, 코드를 구현하는 TDD 방식을 적용합니다.

## TDD 사이클

```
RED → GREEN → REFACTOR → REPEAT

RED:      실패하는 테스트 작성
GREEN:    테스트 통과하는 최소 코드 작성
REFACTOR: 코드 개선 (테스트 유지)
REPEAT:   다음 기능/시나리오
```

## 진행 순서

1. **인터페이스 정의** (SCAFFOLD)
   - 타입/인터페이스 먼저 정의
   - 함수 시그니처 작성

2. **테스트 작성** (RED)
   - 정상 케이스
   - 엣지 케이스 (빈 값, null, 최대값)
   - 에러 케이스

3. **테스트 실행 - 실패 확인**
   ```bash
   npm test -- path/to/file.test.ts
   ```

4. **최소 구현** (GREEN)
   - 테스트만 통과하는 최소한의 코드

5. **리팩토링** (REFACTOR)
   - 테스트 유지하며 코드 개선

6. **커버리지 확인**
   ```bash
   npm test -- --coverage
   ```
   - 목표: 80% 이상

## 주의사항

- 테스트를 먼저 작성 (구현 전에!)
- 한 번에 하나의 테스트만 작성
- 테스트가 실패하는지 반드시 확인
- 최소한의 코드만 작성
