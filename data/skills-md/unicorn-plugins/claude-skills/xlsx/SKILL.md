---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
type: orchestrator
---

# Excel 스프레드시트(XLSX) 처리 스킬

[XLSX 스킬 활성화]

## 목표

Excel 스프레드시트(.xlsx) 생성, 읽기, 편집, 분석을 전문 에이전트에 위임하여 사용자 요청을 완수함.

## 활성화 조건

사용자가 `.xlsx`, `Excel`, `엑셀`, `스프레드시트` 키워드를 언급하거나 표 형식 데이터 파일 산출물을 요청할 때 활성화.

## 워크플로우

### Phase 1: 작업 유형 판별 (`ulw` 활용)

사용자 요청을 분석하여 생성/읽기/편집/수식 재계산 작업 유형을 결정함.

| 작업 유형 | 판별 조건 |
|----------|----------|
| 생성/편집 | openpyxl로 Excel 파일 생성 또는 기존 파일 수정 |
| 읽기/분석 | pandas로 데이터 읽기, 통계 분석, 시각화 |
| 수식 재계산 | LibreOffice 매크로로 수식 값 업데이트 |

이 Phase는 `ulw` 매직 키워드를 활용하여 수행함.

### Phase 2-A: 생성/편집 → Agent: office-editor (`/oh-my-claudecode:ralph` 활용)

- **TASK**: openpyxl을 사용하여 Excel 생성 또는 편집
- **EXPECTED OUTCOME**: 유효한 Excel 파일 생성. 수식이 있는 경우 recalc.py로 재계산 완료. 오류 0개
- **MUST DO**:
  - 계산 로직은 Excel 수식으로 작성 (Python에서 계산 후 하드코딩 금지)
  - 재무 모델링 시 색상 코딩 표준 준수 (blue=입력, black=수식, green=워크시트 링크)
  - 숫자 서식 표준화 (연도는 텍스트, 통화는 $#,##0, 0은 "-")
  - 모든 가정은 별도 셀에 배치하고 수식에서 참조
  - 생성 후 recalc.py로 수식 재계산 (필수)
  - 재계산 결과에서 오류 발견 시 수정 후 재실행
- **MUST NOT DO**:
  - 수식을 하드코딩된 값으로 대체하지 않음
  - #REF!, #DIV/0!, #VALUE! 등 수식 오류를 남기지 않음
- **CONTEXT**:
  - PYTHONPATH=gateway/tools 환경변수 설정 필수
  - openpyxl/pandas API 레퍼런스는 `agents/office-editor/references/xlsx-api-reference.md` 참조
  - 재무 모델링 표준은 `agents/office-editor/references/financial-modeling.md` 참조

이 Phase는 `/oh-my-claudecode:ralph`를 활용하여 수행함.

### Phase 2-B: 읽기/분석 → Agent: office-editor (`ulw` 활용)

- **TASK**: pandas로 Excel 데이터 읽기 및 분석
- **EXPECTED OUTCOME**: 데이터 추출, 통계 분석, 시각화 결과
- **MUST DO**:
  - 적절한 dtype 지정하여 타입 추론 오류 방지
  - 대용량 파일은 usecols로 필요 컬럼만 읽기
  - 날짜 컬럼은 parse_dates 사용
- **MUST NOT DO**: 분석 결과를 하드코딩된 값으로 Excel에 저장 금지 (수식 사용)
- **CONTEXT**: pandas API는 `agents/office-editor/references/xlsx-api-reference.md` 참조

이 Phase는 `ulw` 매직 키워드를 활용하여 수행함.

### Phase 2-C: 수식 재계산 → Agent: office-editor (`ulw` 활용)

- **TASK**: LibreOffice 매크로 실행으로 Excel 수식 재계산
- **EXPECTED OUTCOME**: 모든 수식 값이 최신 상태로 업데이트됨. 오류 0개
- **MUST DO**:
  - recalc.py 스크립트 실행
  - 반환된 JSON에서 오류 확인
  - 오류가 발견되면 (#REF!, #DIV/0! 등) 해당 셀 수정 후 재실행
- **MUST NOT DO**: 오류가 있는 상태에서 완료 선언하지 않음
- **CONTEXT**: recalc.py는 자동으로 LibreOffice 매크로 설정. 샌드박스 환경 지원

이 Phase는 `ulw` 매직 키워드를 활용하여 수행함.

### Phase 3: 결과 검증 (`ulw` 활용)

생성/편집된 Excel 파일의 무결성 확인.

| 검증 항목 | 검증 방법 |
|----------|----------|
| 파일 로드 가능 | openpyxl로 정상 로드 확인 |
| 수식 재계산 완료 | recalc.py 실행 결과 status: success 확인 |
| 오류 0개 | recalc.py 반환 JSON에서 total_errors: 0 확인 |
| 데이터 무결성 | 셀 값, 서식, 수식 보존 확인 |

이 Phase는 `ulw` 매직 키워드를 활용하여 수행함.

## 에이전트 호출 규칙

### 에이전트 FQN

| 에이전트 | FQN | 티어 |
|----------|-----|------|
| office-editor | `claude-skills:office-editor:office-editor` | MEDIUM |

### 프롬프트 조립 절차

1. `agents/office-editor/` 에서 3파일 로드 (AGENT.md + agentcard.yaml + tools.yaml)
2. `gateway/runtime-mapping.yaml` 참조하여 구체화:
   - **모델 구체화**: agentcard.yaml의 `tier: MEDIUM` → `tier_mapping.default.MEDIUM` → `claude-sonnet-4-5`
   - **툴 구체화**: tools.yaml의 추상 도구 → `tool_mapping`에서 실제 도구 결정
   - **금지액션 구체화**: `forbidden_actions: [user_interact, agent_delegate]` → `action_mapping`에서 `[AskUserQuestion, Task]` 제외
   - **최종 도구** = (구체화된 도구) - (제외 도구)
3. 프롬프트 조립: 3파일을 합쳐 하나의 프롬프트로 구성
   - **구성 순서**: 공통 정적(runtime-mapping) → 에이전트별 정적(3파일) → 동적(작업 지시)
4. `Task(subagent_type="claude-skills:office-editor:office-editor", model="claude-sonnet-4-5", prompt=조립된 프롬프트)` 호출

### 오케스트레이션 스킬 활용

| 워크플로우 Phase | 추천 스킬 | 적용 |
|-----------------|----------|:----:|
| Phase 1 (작업 유형 판별) | `ulw` 매직 키워드 | **필수** |
| Phase 2 (생성/편집 실행) | `/oh-my-claudecode:ralph` | **필수** |
| Phase 3 (결과 검증) | `ulw` 매직 키워드 | **필수** |

### 스크립트 호출 패턴

모든 커스텀 도구 호출 시 PYTHONPATH 환경변수를 설정:

```bash
PYTHONPATH=gateway/tools python gateway/tools/xlsx/recalc.py output.xlsx
```

## 완료 조건

| # | 조건 |
|---|------|
| 1 | 생성/편집된 Excel이 openpyxl로 정상 로드됨 |
| 2 | 수식이 있는 경우 recalc.py로 재계산 완료 |
| 3 | 데이터 무결성 확인 (셀 값, 서식, 수식 보존) |
| 4 | 수식 오류 0개 (total_errors: 0) |

## 검증 프로토콜

1. openpyxl로 결과 파일 로드하여 무결성 확인
2. 수식이 포함된 경우 recalc.py로 재계산 후 결과 JSON 확인
3. JSON의 status가 "errors_found"이면 error_summary 참조하여 수정 후 재실행
4. 모든 검증 통과 후에만 완료 선언

## 상태 정리

상태 파일 미사용 (단건 작업). 임시 파일 없음.

## 취소

`cancelomc` 또는 `stopomc` 키워드로 즉시 중단.

## 재개

원본 파일이 보존되어 있으므로 처음부터 재시작 가능.

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 수식이 포함된 셀은 값이 아닌 수식을 보존 |
| 2 | 재무 모델링 시 financial-modeling.md 가이드 준수 |
| 3 | 모든 Phase에 오케스트레이션 스킬 활용 필수 명시 |
| 4 | 에이전트 위임 시 5항목 포함 |
| 5 | 수식이 있는 Excel 생성/편집 시 반드시 recalc.py 실행 |
| 6 | recalc.py 반환 JSON에서 오류 발견 시 수정 후 재실행 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 수식을 하드코딩된 값으로 대체하지 않음 |
| 2 | 에이전트의 내부 절차를 스킬에서 기술하지 않음 |
| 3 | 수식 오류(#REF!, #DIV/0! 등)를 남기지 않음 |

## 검증 체크리스트

- [ ] frontmatter에 name, description 포함
- [ ] 에이전트 호출 규칙 섹션 포함 (FQN, 프롬프트 조립 4단계, 오케스트레이션 활용)
- [ ] 모든 Phase에 스킬 부스팅 명시
- [ ] 완료 조건, 검증 프로토콜, 상태 정리, 취소/재개 섹션 포함
- [ ] MUST 규칙, MUST NOT 규칙 섹션 포함
- [ ] Agent 위임 단계에 5항목 포함
