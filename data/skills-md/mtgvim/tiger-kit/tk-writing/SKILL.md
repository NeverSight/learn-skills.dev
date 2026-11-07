---
name: tk-writing
description: "[user/auto] 글쓰기·설명·HTML 문서 구성 및 표현 기준을 참조할 때 사용합니다. 실제 업무 실행이나 변경 권한을 부여하지 않습니다."
disable-model-invocation: false
metadata:
  tigerkit:
    kind: hybrid
    origin: tigerkit
    relationship: adapted
    role: reference
---

<a id="shared-writing-and-presentation"></a>
# 공통 글쓰기와 표현

아래 조건에 해당하는 참조만 읽고 기준과 공백을 호출자에게 돌려줍니다. 호출자는 범위, 승인과 완료 책임을 유지합니다.
참조는 워크플로를 호출하지 않으며 설치, 변경, 비밀, Git이나 발행 권한을 부여하지 않습니다.

기억, 다른 설치본, 하드코딩한 홈이나 소스 checkout 대체 경로가 아니라 현재 설치된 스킬 모음(`dependencies.json`)에서 소유 스킬을 확인합니다.
소유 스킬이나 자원이 없거나 일치하지 않으면 해당 행동을 중단합니다. 조용히 설치하지 말고 `tk-setup-skills`로 안내합니다.
여기 있는 자원 링크는 `tk-writing`을 기준으로 해석합니다. 명령의 `<tk-writing>`은 현재 설치된 패키지 경로입니다.
이 스킬은 공통 HTML 자산과 조립, 코드 강조, 내보내기와 Chrome 캡처 도우미를 소유하며 런타임 워크플로를 소유하지 않습니다.
호출자가 담당하는 승인과 경로 검사를 마친 뒤 선택한 도우미만 호출합니다. 입력, 출력, 임시 파일과 정리는 설치된 패키지 밖에서 관리합니다.

<a id="conditional-references"></a>
## 조건부 참조

- [HTML 피드백](references/feedback-studio.md): 사람에게 전달하는 HTML의 검증을 마친 뒤 studio를 만들거나 피드백 목록을 반영할 때 읽습니다.

- [차트 설계](references/chart-design.md): 데이터에 차트가 필요하거나 차트 표현을 선택해야 할 때 읽습니다.
- [채팅 전달](references/delivery.md): 사용자에게 결과, 산출물 링크나 여러 속성의 채팅 비교를 반환할 때 읽습니다.
- [명료한 글쓰기](references/clear-writing.md): 제공된 정확한 텍스트를 보존하는 대신 산문을 작성할 때 읽습니다.
- [Diátaxis](references/diataxis.md): 튜토리얼, 방법 안내, 설명이나 참조 구성을 선택할 때 읽습니다.
- [설명 기법](references/explanation-techniques.md): 교육 설명이나 그 표현을 계획할 때 읽습니다.
- [HTML 조립](references/html-assembly.md): 선택한 출력이 공통 reader HTML 조립 경로를 사용할 때 읽습니다.
- [HTML 구성 요소](references/html-components.md): 선택한 HTML 인터페이스에 지원되는 구성 요소가 필요할 때 읽습니다.
- [HTML 도해](references/html-figures.md): 선택한 HTML에 설명 도해가 필요할 때 읽습니다.
- [HTML 출력](references/html-output.md): HTML 산출물을 전달물로 선택했을 때 읽습니다.
- [HTML reader](references/html-reader.md): 공통 reader 수업이나 변경 문서를 조립할 때 읽습니다.
- [HTML 렌더링](references/html-render.md): 선택한 HTML 출력을 빌드, 패키징하거나 검사할 때 읽습니다.
- [대화형 예제](references/interactive-examples.md): 명시적 요청이나 추천 선택에 따라 실시간 대화형 예제를 제공할 때 읽습니다.
- [미디어 선호](references/media-preferences.md): 시각 자료나 미디어 형식/선호를 결정해야 할 때 읽습니다.
- [독자용 서식](references/reader-formatting.md): 설명 문서에 작성한 산문의 서식을 정할 때 읽습니다.
- [렌더러 계약](references/renderer-contract.md): 기존 학습 자료를 바꾸지 않고 지원되는 설명 렌더러를 선택할 때 읽습니다.
- [장면 도해](references/scene-figures.md): 물리적 또는 공간적 관계에 장면 도해가 필요할 때 읽습니다.
- [시각 문법](references/visual-grammar.md): 관계나 설명의 도해 문법을 선택할 때 읽습니다.
