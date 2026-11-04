---
name: tk-artifacts
description: "[user/auto] 파일 산출물 경로·비밀 입력·인증 보존 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

<a id="shared-artifact-safety"></a>
# 공통 산출물 안전 기준

아래 조건을 충족하는 참조만 읽고 기준과 부족한 사항을 호출자에게 반환합니다. 범위, 승인과 완료에 대한 책임은 호출자에게 있습니다. 참조는 워크플로를 호출하지 않으며 설치, 변경, 비밀 접근, Git 또는 발행 권한을 부여하지 않습니다.

소유 스킬은 현재 설치된 스킬 모음(`dependencies.json`)에서 확인합니다. 기억, 다른 설치본, 하드코딩된 홈 경로나 소스 checkout 대체 경로를 사용하지 않습니다. 소유 스킬이나 자원이 없거나 식별이 다르면 해당 행동을 중단하고 `tk-setup-skills`를 안내하며, 말없이 설치하지 않습니다.
`<package>`, "package-local", "this package"는 링크가 다른 소유자를 명시하지 않는 한 호출자의 설치된 패키지를 뜻합니다.

<a id="conditional-references"></a>
## 조건부 참조

- [산출물 경로](references/artifact-paths.md): 승인된 산출물이나 임시 입력을 쓰기 전에 읽습니다.
- [인증](references/authentication.md): 승인된 애플리케이션 인증 입력이나 갱신이 필요할 때 읽습니다.
