---
name: pptx
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill."
type: orchestrator
---

# PowerPoint 프리젠테이션(PPTX) 처리 스킬

[PPTX 스킬 활성화]

## 목표

PowerPoint 프리젠테이션(.pptx) 생성, 읽기, 편집을 전문 에이전트에 위임하여 사용자 요청을 완수함.

## 활성화 조건

사용자가 `.pptx`, `PowerPoint`, `파워포인트`, `프리젠테이션`, `슬라이드`, `덱` 키워드를 언급하거나 슬라이드 산출물을 요청할 때 활성화.

## 워크플로우

### Phase 1: 작업 유형 판별 (`ulw` 활용)

사용자 요청을 분석하여 생성/편집/분석 작업 유형을 결정함.

| 작업 유형 | 판별 조건 |
|----------|----------|
| 생성 | 새 프리젠테이션 파일 생성 요청 |
| 편집 | 기존 `.pptx` 파일 수정, 슬라이드 추가/삭제/재배치 |
| 분석 | 내용 추출, 구조 파악, 썸네일 생성 |

이 Phase는 `ulw` 매직 키워드를 활용하여 수행함.

### Phase 2-A: 새 프리젠테이션 생성 → Agent: office-editor (`/oh-my-claudecode:ralph` 활용)

- **TASK**: pptxgenjs npm 패키지를 사용하여 새 PowerPoint 생성
- **EXPECTED OUTCOME**: 유효한 OOXML 구조를 가진 `.pptx` 파일 생성. XSD 검증 통과
- **MUST DO**:
  - 디자인 원칙 적용 (색상 팔레트, 타이포그래피, 레이아웃 일관성)
  - 슬라이드마다 시각적 요소 포함 (이미지/차트/아이콘/도형)
  - 생성 후 validate.py로 검증
  - 시각적 검증 (PDF 변환 → 이미지 생성 → 서브에이전트 검사)
- **MUST NOT DO**:
  - 텍스트만 있는 슬라이드 생성하지 않음
  - accent line 장식 사용하지 않음 (AI slop 패턴)
  - 낮은 대비 텍스트/아이콘 사용하지 않음
- **CONTEXT**:
  - PYTHONPATH=gateway/tools 환경변수 설정 필수
  - pptxgenjs API 레퍼런스는 `agents/office-editor/references/pptx-api-reference.md` 참조
  - 디자인 가이드는 `agents/office-editor/references/pptx-design-guide.md` 참조

이 Phase는 `/oh-my-claudecode:ralph`를 활용하여 수행함.

### Phase 2-B: 기존 PPTX 편집 → Agent: office-editor (`/oh-my-claudecode:ralph` 활용)

- **TASK**: unpack → XML 편집 → 검증 → pack 워크플로우로 프리젠테이션 수정
- **EXPECTED OUTCOME**: 수정된 유효 OOXML 프리젠테이션. XSD 검증 통과. 고아 리소스 없음
- **MUST DO**:
  - 슬라이드 마스터/레이아웃 참조 무결성 보존
  - Content_Types.xml과 _rels 파일 동기화
  - pack 전 validate.py + clean.py 실행
- **MUST NOT DO**:
  - XSD 검증 없이 pack 실행 금지
  - 슬라이드 추가 시 add_slide.py 스크립트 활용
- **CONTEXT**:
  - PYTHONPATH=gateway/tools 설정
  - XML 편집 가이드는 `agents/office-editor/references/pptx-editing-guide.md` 참조

이 Phase는 `/oh-my-claudecode:ralph`를 활용하여 수행함.

### Phase 3: 결과 검증 (`ulw` 활용)

생성/편집된 프리젠테이션의 유효성 확인.

| 검증 항목 | 검증 방법 |
|----------|----------|
| OOXML 유효성 | validate.py XSD 스키마 검증 |
| 고아 리소스 | clean.py로 미참조 파일 확인 및 정리 |
| 슬라이드 품질 | thumbnail.py로 썸네일 생성 → 시각적 확인 |
| 내용 반영 | markitdown으로 텍스트 추출 비교 |

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
PYTHONPATH=gateway/tools python gateway/tools/office/unpack.py input.pptx output_dir/
PYTHONPATH=gateway/tools python gateway/tools/office/pack.py input_dir/ output.pptx
PYTHONPATH=gateway/tools python gateway/tools/pptx/add_slide.py input.pptx template_slide_index new_slide_index
PYTHONPATH=gateway/tools python gateway/tools/pptx/clean.py input.pptx
PYTHONPATH=gateway/tools python gateway/tools/pptx/thumbnail.py input.pptx
```

## 완료 조건

| # | 조건 |
|---|------|
| 1 | 생성/편집된 PPTX가 유효한 OOXML 구조를 가짐 |
| 2 | XSD 스키마 검증 통과 |
| 3 | 고아 리소스 없음 (clean.py 검증) |
| 4 | 슬라이드 썸네일 생성 가능 (thumbnail.py 검증) |

## 검증 프로토콜

1. pack.py 실행 시 XSD 검증 자동 수행
2. clean.py로 고아 리소스 확인 및 정리
3. thumbnail.py로 슬라이드 시각적 검증
4. 모든 검증 통과 후에만 완료 선언

## 상태 정리

완료 시 임시 unpack 디렉토리 삭제. `.omc/state/` 에 상태 파일 미사용 (단건 작업).

## 취소

`cancelomc` 또는 `stopomc` 키워드로 즉시 중단. 임시 unpack 디렉토리가 존재하면 삭제.

## 재개

임시 unpack 디렉토리가 남아있으면 해당 상태에서 재개 가능. 원본 파일이 보존되어 있으므로 처음부터 재시작도 가능.

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 원본 PPTX 편집 시 반드시 unpack → XML 편집 → validate → pack 순서 준수 |
| 2 | 슬라이드 마스터/레이아웃 참조 무결성 보존 |
| 3 | 모든 Phase에 오케스트레이션 스킬 활용 필수 명시 |
| 4 | 에이전트 위임 시 5항목 포함 |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 직접 ZIP 파일을 바이너리 수정하지 않음 |
| 2 | XSD 검증 없이 문서 전달 금지 |
| 3 | 에이전트의 내부 절차를 스킬에서 기술하지 않음 |

## 검증 체크리스트

- [ ] frontmatter에 name, description 포함
- [ ] 에이전트 호출 규칙 섹션 포함 (FQN, 프롬프트 조립 4단계, 오케스트레이션 활용)
- [ ] 모든 Phase에 스킬 부스팅 명시
- [ ] 완료 조건, 검증 프로토콜, 상태 정리, 취소/재개 섹션 포함
- [ ] MUST 규칙, MUST NOT 규칙 섹션 포함
- [ ] Agent 위임 단계에 5항목 포함
