---
name: tk-engineering
description: "[user/auto] 테스트·진단·리뷰·SDD의 공통 기준을 다른 스킬에서 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

<a id="shared-engineering-guidance"></a>
# 공통 엔지니어링 기준

아래 조건에 해당하는 참조만 읽고 기준과 누락 사항을 호출자에게 반환합니다.
범위, 승인과 완료 책임은 호출자가 유지합니다. 참조는 워크플로를 호출하지 않으며
설치, 변경, 비밀, Git 또는 발행 권한을 부여하지 않습니다.

소유자는 현재 설치된 스킬 모음(`dependencies.json`)에서 찾습니다. 기억, 다른 설치본,
하드코딩한 홈이나 소스 checkout 대체 경로에서 찾지 않습니다. 소유자나 자원이 없거나
일치하지 않으면 해당 행동을 차단하고 `tk-setup-skills`를 안내하며, 조용히 설치하지 않습니다.
`<package>`, "package-local"과 "this package"는 링크가 다른 소유자를 명시하지 않는 한 호출자의 설치된 패키지를 뜻합니다.

<a id="conditional-references"></a>
## 조건부 참조

- [진단](references/diagnosis.md): 어렵거나 간헐적이거나 성능과 관련된 버그를 진단해야 하거나 최초 재현에 실패했을 때 읽습니다.
- [발견 사항 품질](references/finding-quality.md): 정확한 범위의 리뷰 발견 사항을 걸러내고 근거를 뒷받침할 때 읽습니다.
- [프로젝트 규칙](references/project-rules.md): 저장소나 작업이 프로젝트 규칙 묶음을 지정할 때 읽습니다.
- [React](references/react.md): 정확히 해당하는 코드 리뷰에 React 코드가 포함될 때 읽습니다.
- [리뷰 프로토콜](references/review-protocol.md): 직접 리뷰, SDD Unit 리뷰 또는 전체 변경의 독립 리뷰를 수행할 때 읽습니다.
- [SDD 상호작용](references/sdd-interaction.md): 승인된 SDD 실행이 사용자 상호작용 지점에 도달했을 때 읽습니다.
- [SDD 복구](references/sdd-recovery.md): 승인되었으나 중단된 SDD 실행을 재개할 때 읽습니다.
- [SDD 전달](references/sdd-transport.md): 승인된 SDD 단위나 리뷰 brief를 작업자에게 전달할 때 읽습니다.
- [SDD](references/sdd.md): 준비 담당자가 이미 SDD를 선택했을 때 읽습니다.
- [보안 경계](references/security-boundaries.md): 엔지니어링 또는 감사 조사가 안전이나 권한 경계에 도달했을 때 읽습니다.
- [보안](references/security.md): 정확히 해당하는 코드 리뷰에 보안상 민감한 영역이 포함될 때 읽습니다.
- [선택 인계](references/selection-handoff.md): 선택한 prototype이나 비교 결과를 구현에 반영해야 할 때 읽습니다.
- [테스트 대역](references/test-doubles.md): 변경된 테스트가 mock, fake, stub 또는 spy를 사용할 때 읽습니다.
- [테스트](references/testing.md): 소스 변경에 테스트가 필요한 관찰 가능한 동작이 있을 때 읽습니다.
- [TypeScript](references/typescript.md): 정확히 해당하는 코드 리뷰에 TypeScript 코드가 포함될 때 읽습니다.
- [의미적 리뷰 계획](references/review-planning.md): 최종 로컬 구현 승인 전에 Seed나 현재 직접 작업에 리뷰 의무를 보존할 때 읽습니다.
