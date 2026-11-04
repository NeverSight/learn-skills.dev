---
name: tk-verification-guidance
description: "[user/auto] 앱·브라우저 검증의 제공자 선택·근거·설정 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

<a id="shared-verification-guidance"></a>
# 공통 검증 지침

아래 조건이 성립하는 참조만 읽고 기준과 공백을 호출자에게 반환합니다. 호출자는 범위, 승인과 완료에 대한 책임을 유지합니다. 참조는 워크플로를 호출하지 않으며 설치, 변경, 비밀, Git 또는 발행 권한을 부여하지 않습니다.

소유 스킬은 기억, 다른 설치본, 하드코딩한 홈이나 소스 checkout fallback이 아니라 현재 설치된 스킬 모음(`dependencies.json`)에서 확인합니다. 소유 스킬이나 자원이 없거나 식별이 다르면 해당 행동을 중단합니다. `tk-setup-skills`를 안내하며 몰래 설치하지 않습니다. [제공자 registry](references/providers.json)와 [선호 설정 도우미](scripts/verify_preferences.py)는 이 패키지가 소유합니다. 명령의 `<tk-verification-guidance>`는 현재 설치된 이 패키지의 경로입니다. 도우미는 호출자가 승인한 선호 설정만 읽고/저장하며 워크플로를 선택하거나 시작하지 않습니다.

<a id="conditional-references"></a>
## 조건부 참조

- [제공자 지식](references/provider-knowledge.md): 호출자가 탐색/상호작용 전에 선택된 제공자의 통합 지식을 필요로 하거나, 진단 후 재검증된 제공자 한계에 제한적인 문제 해결 메모가 필요할 수 있을 때 읽습니다.
- [제공자 선택](references/provider-selection.md): 검증 제공자를 선택하거나 지원되는 선호 설정을 해석할 때 읽습니다.
- [발행 근거](references/publication-evidence.md): 승인된 발행 담당자에게 전달할 검증 근거를 준비할 때 읽습니다.
- [검증](references/verification.md): 검증 범위, 근거와 결과 상태를 정할 때 읽습니다.
