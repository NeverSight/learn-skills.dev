---
name: simplify
description: "코드 단순화 및 리팩토링 — 변경된 코드를 리뷰하고 불필요한 추상화, 중복, 복잡성을 제거합니다. Triggers on: 단순화, simplify, 리팩토링, 코드 정리, 코드 개선. NOT for: 새 기능 추가, 버그 수정."
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Edit, Grep
---

# 코드 단순화

최근 작성한 코드를 리뷰하고 단순화합니다.

## 검토 항목
1. 불필요한 추상화 제거
2. 중복 코드 정리
3. 복잡한 조건문 단순화
4. 변수/함수 이름 개선
5. 불필요한 주석 제거
6. console.log 제거

## 원칙
- 동작은 변경하지 않음 (리팩토링만)
- 테스트가 있다면 테스트 통과 확인
- 과도한 최적화 지양

## 체크리스트
- [ ] 함수 50줄 이하
- [ ] 파일 800줄 이하
- [ ] 중첩 4단계 이하
- [ ] 매직 넘버 제거
- [ ] 명확한 변수명
