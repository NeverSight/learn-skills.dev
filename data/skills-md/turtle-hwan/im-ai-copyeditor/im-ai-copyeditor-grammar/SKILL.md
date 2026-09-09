---
name: im-ai-copyeditor-grammar
description: >-
  한국어 맞춤법과 문체를 문장 단위로 교정한다. 예요/이에요, 되/돼, 안/않, 데/대, 든/던, 로서/로써, 율/률, 띄어쓰기 같은 맞춤법과, 종결문체 일관성·사물존칭·경어법 같은 문체를 국립국어원 기준으로 바로잡는다. 뜻은 한 글자도 바꾸지 않는다. 트리거 — "맞춤법 고쳐", "맞춤법 검사", "문체 통일", "존댓말 통일", "한국어 교정". 문장 교정(번역투·군더더기)까지: -sentence / AI 문체까지: -ai / 전부: im-ai-copyeditor.
compatibility: 문장 분절 스크립트 실행에 python3(없으면 python) 필요.
metadata:
  version: "0.3.0"
  openclaw:
    requires:
      anyBins: [python3, python]
  hermes:
    category: writing
    tags: [korean, proofreading, grammar]
---

# im-ai-copyeditor-grammar — 맞춤법·문체 교정

한국어 맞춤법과 문체를 문장 단위로 바로잡아요. 국립국어원 기준을 따라요. 정규식으로 한꺼번에
바꾸지 않아요. 뜻·수치·고유명사·인용은 그대로 둬요.

스킬 디렉토리를 `$SKILL` 로 표기해요. Claude Code 는 `${CLAUDE_SKILL_DIR}` 나 `${CLAUDE_PLUGIN_ROOT}`.
아래 명령의 `python3` 는 환경에 `python3` 가 없으면 `python`(Windows 는 `py -3`)으로 바꿔 실행해요.

## 절차

**Phase 0** — 상태 한 줄: `im-ai-copyeditor-grammar 맞춤법·문체 / run_id: {YYYY-MM-DD-NNN}`
**Phase 1** — 입력을 `_workspace/{run_id}/01_input.txt` 저장.
**Phase 2** — `python3 $SKILL/scripts/segment.py _workspace/{run_id}/01_input.txt --outdir _workspace/{run_id}` → segments.json + worksheet.md, 문장 수 N 확인.**Phase 3** — 룰북 로드: `$SKILL/references/grammar-rules.md` 와 `$SKILL/references/style-guide.md`, 공통 `$SKILL/references/prime-directives.md`. 먼저 글 전체의 우세 문체를 정해요. 해요체·합니다체·한다체 중 하나로.
**Phase 4** — worksheet.md 의 문장 칸을 위에서 아래로 읽으며 맞춤법 규칙 G-를 먼저 바로잡고 문체 규칙 ST-를 맞춰 **윤문/규칙** 채움. 고칠 게 없으면 원문 그대로 + `변경없음`. 문장을 합치거나 나누거나 순서를 바꾸지 않아요. '그대로 둘 줄'과 보호 정보는 보존해요.
**Phase 5** — `python3 $SKILL/scripts/reassemble.py _workspace/{run_id}/segments.json _workspace/{run_id}/worksheet.md --out _workspace/{run_id}/final.md`. ID 중복·누락·추가, 빈 칸, 잘못된 `변경없음`은 2, 기본 변경률 상한 50% 초과는 3으로 멈춰요. 변경률 30% 초과는 의미 재검토 경고예요. 요청에 별도 상한이 있으면 `--max-change`로 명시하며 임의로 높이지 않아요. 실패하면 고친 뒤 다시 실행하며, 이전 결과를 이번 결과로 반환하지 않아요.
**Phase 6** — 반환: 상태 한 줄 / 바뀐 문장 전·후 표 / final.md / 자체검증 6가지.

제목·목록·표 셀의 텍스트도 교정 대상이에요. 보호 표현이나 Markdown 행·열이 바뀌면 종료 코드 4로 멈춰요.
사용자가 중간점/구분용 대시 제거를 요청한 경우에만 공통 약속 8절을 적용하고 Phase 5에 `--check-punctuation`을 추가해요.
보호할 고유명사·기술 표현은 분절 전에 `--preserve-text '원문의 정확한 표현'`으로 지정해요.
장식용 따옴표와 작성자 인용 블록의 편집 옵션, 제외된 HTML 처리, `부분 재조립` 보고는 공통 약속 2절을 따라요. 스크립트 통과 후에도 의미와 교정 누락을 별도로 검토해요.

## 옵션
- `장르: 칼럼|리포트|블로그|공적` · `강도: 보수|기본|적극` 기본값 기본

## 주의
맞춤법 교정은 뜻을 바꾸지 않아요. 문체는 입력의 격식을 따르되 글 안에서 일관되게 맞춰요. 한쪽으로
통일할 때 글 전체의 격식을 뒤집지 않아요. 사물존칭은 빼되 간접높임은 살려요.
