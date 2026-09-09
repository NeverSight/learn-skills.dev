---
name: im-ai-copyeditor-sentence
description: >-
  한국어 문장을 문장 단위로 첨삭한다. 책 『내 문장이 그렇게 이상한가요?』에서 영감받은 군더더기 빼기(적·의·것·들, 있다, 수 있는, 이중피동, 만연체, 괄호·쉼표)와, 영어·일본어 번역투 걷어내기(피동→능동, 가지다 직역, 무생물 주어, 대명사·전치사 직역, 명사화, 영문법 구문)를 함께 한다. 사람이 쓴 글이든 AI가 쓴 글이든 똑같이 적용된다. 뜻은 한 글자도 바꾸지 않는다. 트리거 — "문장 간소화", "군더더기 빼줘", "적의것들", "문장 줄여줘", "문장 첨삭", "번역 문체 고쳐", "번역체 자연스럽게", "영어 직역 티 빼줘". AI 문체까지: -ai / 맞춤법·문체: -grammar / 전부: im-ai-copyeditor.
compatibility: 문장 분절 스크립트 실행에 python3(없으면 python) 필요.
metadata:
  version: "0.3.0"
  openclaw:
    requires:
      anyBins: [python3, python]
  hermes:
    category: writing
    tags: [korean, proofreading, concision]
---

# im-ai-copyeditor-sentence — 문장 교정 (군더더기·번역투)

문장 단위의 군더더기와 영어·일본어 직역투를 빼기 중심으로 첨삭한다. 책 『내 문장이 그렇게 이상한가요?』에서
영감을 받았다. 문장 부호 단위로 잘라 한 문장씩 다듬는다. 정규식으로 한꺼번에 바꾸지 않는다.
뜻·수치·고유명사·인용은 그대로 둔다.

스킬 디렉토리를 `$SKILL` 로 표기한다. Claude Code 는 `${CLAUDE_SKILL_DIR}` 나 `${CLAUDE_PLUGIN_ROOT}`.
아래 명령의 `python3` 는 환경에 `python3` 가 없으면 `python`(Windows 는 `py -3`)으로 바꿔 실행한다.

## 절차

**Phase 0** — 상태 한 줄: `im-ai-copyeditor-sentence 문장 교정(군더더기·번역투) / run_id: {YYYY-MM-DD-NNN}`
**Phase 1** — 입력을 `_workspace/{run_id}/01_input.txt` 저장.
**Phase 2** — `python3 $SKILL/scripts/segment.py _workspace/{run_id}/01_input.txt --outdir _workspace/{run_id}` → segments.json + worksheet.md, 문장 수 N 확인.
**Phase 3** — 룰북 로드: `$SKILL/references/sentence-rules.md` 와 공통 `$SKILL/references/prime-directives.md`.
**Phase 4** — worksheet.md 의 문장 칸을 위에서 아래로, sentence-rules.md 의 적용 순서대로(빼기 → 번역투 → 괄호·쉼표·만연체 마무리) 다듬어 **윤문/규칙** 채움. 고칠 게 없으면 원문 그대로 + `변경없음`. 문장을 합치거나 나누거나 순서를 바꾸지 않는다. '그대로 둘 줄'과 보호 정보는 보존한다.
**Phase 5** — `python3 $SKILL/scripts/reassemble.py _workspace/{run_id}/segments.json _workspace/{run_id}/worksheet.md --out _workspace/{run_id}/final.md`. ID 중복·누락·추가, 빈 칸, 잘못된 `변경없음`은 2, 기본 변경률 상한 50% 초과는 3으로 멈춘다. 변경률 30% 초과는 의미 재검토 경고다. 요청에 별도 상한이 있으면 `--max-change`로 명시하며 임의로 높이지 않는다. 실패하면 고친 뒤 다시 실행하며, 이전 결과를 이번 결과로 반환하지 않는다.
**Phase 6** — 반환: 상태 한 줄 / 바뀐 문장 전·후 표 / final.md / 자체검증 6가지.

제목·목록·표 셀의 텍스트도 윤문 대상이다. 보호 표현이나 Markdown 행·열이 바뀌면 종료 코드 4로 멈춘다.
사용자가 중간점/구분용 대시 제거를 요청한 경우에만 공통 약속 8절을 적용하고 Phase 5에 `--check-punctuation`을 추가한다.
보호할 고유명사·기술 표현은 분절 전에 `--preserve-text '원문의 정확한 표현'`으로 지정한다.
장식용 따옴표와 작성자 인용 블록의 편집 옵션, 제외된 HTML 처리, `부분 재조립` 보고는 공통 약속 2절을 따른다. 스크립트 통과 후에도 의미와 교정 누락을 별도로 검토한다.

## 옵션
- `장르: 칼럼|리포트|블로그|공적` · `강도: 보수|기본|적극` 기본값 기본

## 주의
뜻 보존이 최상위다. 한 글자 더 써서 어색하면 뺀다. 번역투는 영어를 옮긴 흔적만 손보고, 살아 있는 뜻은 건드리지 않는다. 수치·고유명사·인용은 불가침이다.
