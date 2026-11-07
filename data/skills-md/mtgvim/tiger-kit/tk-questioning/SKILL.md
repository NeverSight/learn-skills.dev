---
name: tk-questioning
description: "[user/auto] 질문·승인 라운드와 시각적 질문 기준을 다른 스킬에서 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

<a id="shared-questioning"></a>
# 공통 질문 기준

아래 조건에 해당하는 참조만 읽고 기준과 미확인 사항을 호출자에게 반환합니다. 범위, 승인과 완료 책임은 호출자가 유지합니다. 참조는 워크플로를 호출하지 않으며 설치, 변경, 비밀 접근, Git 또는 발행 권한을 부여하지 않습니다.

소유자는 기억, 다른 설치본, 하드코딩한 홈이나 소스 checkout 대체 경로가 아니라 현재 설치된 스킬 모음(`dependencies.json`)에서 확인합니다. 소유자나 자원이 없거나 일치하지 않으면 해당 행동을 중단합니다. 조용히 설치하지 말고 `tk-setup-skills`를 안내합니다. 자원 링크는 설치된 소유자를 가리킵니다. 시각적 질문의 테마 자산은 `tk-writing`이 소유합니다.

<a id="conditional-references"></a>
## 조건부 참조

- [질문](references/questions.md): 사용자 소유 결정, 누락된 승인이나 선행 조건을 질문·승인 제안·질문 도구 입력으로 제시하기 직전에 읽었는지 확인합니다. 네이티브 도구 우선순위, 결정·승인 분리와 포콕식 채팅 대체 형식의 정본입니다.
- [시각적 질문](references/visual-questions.md): 미해결 레이아웃, 탐색 또는 시각적 선택에 질문 보조 자료가 필요할 때 읽습니다.

HTML을 사람에게 전달할 때는 현재 설치된 `tk-writing`의 [공통 피드백 후처리](../tk-writing/references/feedback-studio.md)를 적용하고 studio를 기본 열람본으로 안내합니다. 원본·기존 전용 인터페이스·검증 의무를 유지합니다.
