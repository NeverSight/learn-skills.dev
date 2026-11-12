---
name: polish-all
description: 한글 글 한 편을 진단부터 다듬기까지 전과정으로 한 번에 처리하는 윤문 풀코스 오케스트레이터. detect로 입력을 진단(AI글/번역문/장르)해 필요한 단계만 자동 라우팅한 뒤, 교정·교열(proofread) → 번역투 제거(translate-polish) → AI 티 제거(humanize) → 문체·톤 변환(restyle, 목표 지정 시) 순으로 누적 적용하고, 마지막에 detect로 재진단해 개선을 확인한다. 내용은 보존하고(restyle만 register 변경) 단계별 before/after를 보고한다. 다음과 같을 때 사용 — 글을 전체적으로/싹 다듬어 달라, "윤문 풀코스"·"전과정"으로 처리해 달라, 교정부터 윤문까지 한 번에 해 달라는 요청. 한 가지 측면만 원하면 개별 스킬(proofread/translate-polish/humanize/restyle/detect)을 직접 쓴다. 내용 추가·삭제를 동반한 재작성, 번역 작업은 제외한다.
---

# 윤문 풀코스(polish-all) — 진단부터 다듬기까지 전과정

<role>
한글 글 한 편을 **진단 → 교정 → 번역투 제거 → AI 티 제거 → 문체 변환 → 재진단**의 순서로 처리하는
오케스트레이터다. 각 단계는 형제 스킬을 **이름(`plugin:skill`)으로 `Skill` 도구를 통해 호출**해 순차
실행한다 — 형제 스킬의 내부 파일을 상대경로로 직접 참조하지 않는다(내부 구조 변경에 깨지지 않게).
`Skill` 도구는 현재 대화에서 실행되므로 별도 서브에이전트를 띄우지 않는 단일 흐름이다. 앞 단계의
출력이 다음 단계의 입력이 된다. 의미는 보존하고(restyle만 register를 의도적으로 변경) 누적 결과와
단계별 before/after를 보고한다.
</role>

<resources>
순서·라우팅·중복·통합검증은 이 스킬 고유의 `pipeline-guide.md`가 정의한다. 각 단계는 아래 형제 스킬을
`plugin:skill` 이름으로 호출한다(개별 규칙·reference는 각 스킬이 스스로 로드한다).

- `references/pipeline-guide.md` — 단계 순서·근거, 라우팅 매트릭스, translate-polish↔humanize 중복 처리, 강도 전달, 통합 자체검증, 출력 형식. **전 단계의 상위 기준**(이 스킬 고유 파일).
- `yoonmoon:detect` — **Phase 1·6**(진단·재진단).
- `yoonmoon:proofread` — **Phase 2**(교정·교열).
- `yoonmoon:translate-polish` — **Phase 3**(번역투 제거).
- `yoonmoon:humanize` — **Phase 4**(AI 티 제거).
- `yoonmoon:restyle` — **Phase 5**(문체·톤 변환).
  </resources>

<workflow>

<phase n="0" name="입력·옵션 확인">
1. 다듬을 한글 텍스트를 확보한다(붙여넣기 또는 파일). 번역문이면 원문(원천 텍스트)이 있으면 같이 확보.
2. 옵션 파싱: **강도**(`보수|기본|적극`, 기본값 기본), **목표 문체**(restyle용 — 없으면 5단계 skip),
   사용자가 명시한 단계 on/off(라우팅보다 우선).
3. 한 줄 상태 출력: `polish-all 시작 — 강도: {강도} / 목표 문체: {지정/없음}`
</phase>

<phase n="1" name="진단·라우팅 (detect)">
`yoonmoon:detect` 스킬을 호출해 입력을 진단하고, 그 한 줄 판정에서 **AI 가능성 · 번역문 가능성 · 장르**를
읽는다(세 값은 detect의 `<outputFormat>` 1번이 보장한다).
`pipeline-guide.md`의 **라우팅 매트릭스**로 켤 단계를 정한다(proofread 항상, restyle은 목표 지정 시).
두 축은 **각자의 열에 따로** 매핑한다 — 번역문 가능성은 translate-polish 열에, AI 가능성은 humanize 열에.
축마다 **높음**은 ✅, **낮음**은 ⏭ skip, **중간**은 '불확실' 행의 값(번역투·AI 티가 본문에 실제로 보일 때만 ✅)을
쓴다. 한 축이 중간이어도 다른 축은 자기 값을 그대로 쓴다.
판정 결과와 켜진 단계를 기록한다.
</phase>

<phase n="2" name="교정·교열 (proofread)">
`yoonmoon:proofread` 스킬을 호출해 맞춤법·띄어쓰기·표준어·외래어·문장부호·비문 등 **규범 오류만** 고친다.
뜻·문체는 불변. 깨끗한 토대를 만들어 뒤 단계를 돕는다. (항상 실행)
</phase>

<phase n="3" name="번역투 제거 (translate-polish) — 조건부">
**번역문으로 판정됐을 때만.** `yoonmoon:translate-polish` 스킬을 호출해 번역투 8유형을 교정한다.
원문이 있으면 명시화·간섭을 대조한다. 강도·장르를 전달한다. 재번역 금지.
</phase>

<phase n="4" name="AI 티 제거 (humanize) — 조건부">
**AI 글로 판정됐을 때만.** `yoonmoon:humanize` 스킬을 호출해 AI 티를 다듬는다. 3단계가 실행됐으면
**번역투(카테고리 1·2·6)는 제외하고 AI 고유 티(3·4·5·7·8·9·10·11)에 집중**한다(`pipeline-guide.md`의 중복 처리).
강도·장르를 전달한다.
</phase>

<phase n="5" name="문체·톤 변환 (restyle) — 조건부">
**목표 문체가 지정됐을 때만.** `yoonmoon:restyle` 스킬을 호출해 종결체·격식·매체 톤을 목표에 맞게 바꾼다.
register를 의도적으로 바꾸는 유일한 단계 — 그래서 의미 보존 단계가 끝난 **맨 마지막**에 둔다.
사실·주장·효력 문구는 보존.
</phase>

<phase n="6" name="재진단 (detect QA)">
다듬은 결과를 `yoonmoon:detect` 스킬로 **재진단**해 AI 가능성·번역체 신호가 입력 대비 낮아졌는지 확인한다.
이어 `pipeline-guide.md`의 **통합 자체검증 7항**(사실 보존·의미 동등·단계 충돌·과교정 누적·의미 미달·일관성·재진단 개선)을
수행한다. 위반 시 해당 단계로 돌아가 **1회** 부분 재작업한다. 재작업 후에도 같은 항목이 통과하지 못하면
**무한 반복하지 말고** 최선의 결과물을 내되, 미해결 검증 항목을 결과의 "확인 요망"에 명시한다.
</phase>

<phase n="7" name="결과 반환">
`pipeline-guide.md`의 출력 형식대로 반환한다(`<outputFormat>` 요약). 통합 자체검증에서 걸린 항목이 남았거나 의미 보존이 불안하면
한 줄로 알리고 "특정 단계만 강도를 낮춰 다시 볼까요?"처럼 후속 점검을 제안한다.
</phase>

</workflow>

<outputFormat>
`references/pipeline-guide.md`의 "출력 형식"을 따른다. 요지:

1. **한 줄 상태** — `완료. 실행 단계: {…} / 재진단: AI 가능성 {전}→{후}`
2. **최종 결과물** — 모든 단계를 거친 글.
3. **단계별 요약 표** — 단계 / 실행(✅·skip+사유) / 주요 변경·탐지.
4. **before → after 하이라이트** — 무엇이 왜 달라졌는지 알 만큼만 추린다.
5. (있으면) **확인 요망** — 오역 의심·효력 문구·미해결 검증 항목 등.
   </outputFormat>

<preservationRules>
restyle 단계를 제외한 전 단계에서 어떤 경우에도 보존한다(각 스킬의 보존 원칙 누적):
고유명사·수치·단위·날짜·통화 · 직접 인용·대사 · 전문 용어 · 주장의 방향·강도·인과·수량 · 글의 목적·결론.
restyle은 register(종결체·격식·톤)만 의도적으로 바꾸고 그 외 내용은 보존한다. 누적 과교정을 경계한다.
</preservationRules>

<followupCommands>
| 사용자 신호 | 처리 |
|---|---|
| "특정 단계만 다시" | 해당 단계만 재실행(앞 단계 결과 유지) |
| "교정만" / "~ 단계만" (포함 지정) | 지정한 단계만 실행하고 나머지는 모두 skip |
| "번역투는 빼고" / "~는 빼고" (제외 지정) | 지정 단계만 제외하고 나머지는 라우팅대로 실행 |
| "강도 조정" | 강도를 바꿔 cleaner 단계(2~5)를 재실행 |
| "이 문단만" | 지정 문단만 입력으로 삼아 Phase 0부터 |
| "문체를 ~로 바꿔" | restyle(5단계)을 켜고 목표 문체로 재실행 |
</followupCommands>

<outOfScope>
- 한 가지 측면만 필요 → 개별 스킬: **proofread**(교정) / **translate-polish**(번역투) / **humanize**(AI 티) / **restyle**(문체) / **detect**(진단)
- 내용 추가·삭제·요약·재구성을 동반한 재작성 → 별도 글쓰기
- 다른 언어로 옮기는 번역 → 번역 작업
</outOfScope>
