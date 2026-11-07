---
name: tk-ui-evidence
description: "[user/auto] UI 문구·진입 경로의 근거 수집 및 전달 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

<a id="shared-ui-evidence"></a>
# 공통 UI 근거

아래 조건이 성립하는 참조만 읽고 기준과 공백을 호출자에게 반환합니다. 호출자는 범위, 승인과 완료에 대한 책임을 유지합니다. 참조는 워크플로를 호출하지 않으며 설치, 변경, 비밀, Git 또는 발행 권한을 부여하지 않습니다.

소유 스킬은 기억, 다른 설치본, 하드코딩한 홈이나 소스 checkout fallback이 아니라 현재 설치된 스킬 모음(`dependencies.json`)에서 확인합니다. 소유 스킬이나 자원이 없거나 식별이 다르면 해당 행동을 중단합니다. `tk-setup-skills`를 안내하며 몰래 설치하지 않습니다. `<package>`, "package-local"과 "this package"는 링크가 다른 소유자를 명시하지 않는 한 호출자의 설치된 패키지를 뜻합니다.

<a id="conditional-references"></a>
## 조건부 참조

- [UI 근거](references/ui-evidence.md): UI label과 진입 경로를 수집, 검증 또는 보고할 때 읽습니다.
