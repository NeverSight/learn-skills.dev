---
name: review
description: |
  현재 브랜치의 변경사항 코드 리뷰.
  트리거: "리뷰", "review", "검토", "코드 리뷰", "PR 리뷰", "변경사항 확인"
  안티-트리거: "구현", "코드 작성", "빌드"
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Bash, Grep, Glob
---

# 코드 리뷰

현재 브랜치의 변경사항을 리뷰합니다.

## 변경사항 확인
```bash
git diff main...HEAD --stat
git log main...HEAD --oneline
```

## 리뷰 체크리스트
1. **기능**: 요구사항을 충족하는가?
2. **버그**: 잠재적 버그나 엣지 케이스는 없는가?
3. **보안**: 보안 취약점은 없는가?
4. **성능**: 성능 이슈는 없는가?
5. **가독성**: 코드가 읽기 쉬운가?
6. **테스트**: 테스트가 충분한가?

## 출력 형식
각 파일에 대해 한국어로 리뷰 의견을 작성합니다.
개선이 필요한 부분은 구체적인 제안과 함께 알려줍니다.

## CLAUDE.md 업데이트
리뷰 중 발견한 패턴이나 실수는 CLAUDE.md에 규칙으로 추가합니다.
