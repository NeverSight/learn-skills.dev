---
name: compound
description: 길드 운영 인사이트를 구조화된 문서로 축적하여 조직 지식을 복리로 성장시킨다
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
preconditions:
  - 인사이트가 확인됨 (가설이 아닌 검증된 학습)
  - 해당 인사이트가 재사용 가치가 있음
---

# compound 스킬

**목적:** 길드 운영 과정에서 검증된 인사이트를 즉시 문서화하여, 팀 지식을 복리로 성장시키는 검색 가능한 지식 베이스를 구축한다.

## 개요

이 스킬은 인사이트가 확인되는 즉시 포착하여, YAML frontmatter 기반의 구조화된 문서로 저장한다. 카테고리별 단일 파일 아키텍처를 사용하며, 각 인사이트는 `knowledge/solutions/[category]/[filename].md`에 저장된다.

---

<critical_sequence name="insight-capture" enforce_order="strict">

## 7단계 프로세스

<step number="1" required="true">
### Step 1: 트리거 감지

**자동 감지 문구 (대화에서 인식):**

- "이거 잘 됐다"
- "이 방식이 좋네"
- "다음에도 이렇게 하자"
- "이건 기록해두자"
- "이 포맷이 먹혔다"
- "고객이 좋아했어"
- "이 프레임워크가 통했다"
- "이게 효과가 있었어"
- "이렇게 하니까 됐어"

**OR 수동:** `/compound` 커맨드

**Non-trivial만 (재사용 가치 있는 인사이트):**

- 팀이 반복할 수 있는 패턴
- 다른 상황에도 적용 가능한 교훈
- 시행착오 끝에 발견한 방법
- 파트너/고객이 검증한 접근법
- 조직 운영에 구조적 개선을 가져온 발견

**스킵 기준:**

- 이 상황에서만 통하는 일회성 방법
- 단순 사실 기록 (수치, 날짜 등)
- 이미 문서화된 내용의 반복
- 아직 검증되지 않은 가설
</step>

<step number="2" required="true" depends_on="1">
### Step 2: 컨텍스트 수집

대화 이력에서 추출:

**필수 정보:**

- **domain**: guild / contents / community / business / knowledge
- **insight_type**: 인사이트 유형 (schema.yaml enum 참조)
- **component**: 도메인 내 하위 컴포넌트 (schema.yaml enum 참조)
- **context**: 어떤 상황에서 나온 인사이트인가 (1-3문장)
- **key_learning**: 핵심 교훈 한 문장 (다른 상황에도 일반화 가능하게)
- **impact**: critical / high / medium / low
- **tags**: 검색 키워드 (소문자, 하이픈 구분)

**추가 수집 항목:**

- 배경: 어떤 프로젝트/활동 중이었는가
- 시도한 것들: 효과 없었던 접근들
- 효과 있었던 것: 실제로 작동한 방법
- 작동 이유: 왜 효과적이었는가
- 재현 조건: 언제 이 방법을 쓸 수 있는가

**BLOCKING 요건:** domain, insight_type, 핵심 인사이트가 불분명한 경우 사용자에게 질문하고 응답을 기다린다:

```
문서화를 위해 몇 가지 확인이 필요합니다:

1. 어떤 도메인인가요? (guild/contents/community/business/knowledge)
2. 인사이트 유형은? (예: content_pattern, consulting_pattern, process_improvement...)
3. 핵심 교훈을 한 문장으로 정리하면?

[응답 후 계속 진행]
```
</step>

<step number="3" required="false" depends_on="2">
### Step 3: 기존 문서 검색

`knowledge/solutions/` 에서 유사 인사이트 검색:

```bash
# domain, tags, insight_type 기준으로 병렬 검색
Grep: pattern="domain: [domain]" path=knowledge/solutions/ output_mode=files_with_matches
Grep: pattern="tags:.*[keyword]" path=knowledge/solutions/ output_mode=files_with_matches -i=true
Grep: pattern="insight_type: [type]" path=knowledge/solutions/ output_mode=files_with_matches
```

**유사 문서 발견 시** 사용자에게 선택지 제시 후 대기:

```
유사 문서 발견: knowledge/solutions/[path]

어떻게 할까요?
1. 새 문서 생성 + 교차 참조 추가 (권장)
2. 기존 문서 업데이트 (동일한 인사이트의 보완인 경우)
3. 기타

선택 (1-3): _
```

사용자 응답 대기 후 선택한 액션 실행.

**유사 문서 없으면** Step 4로 바로 진행.
</step>

<step number="4" required="true" depends_on="2">
### Step 4: 파일명 생성

형식: `YYYYMMDD-[sanitized-insight-slug].md`

**Sanitization 규칙:**

- 소문자
- 공백 → 하이픈
- 특수문자 제거 (하이픈 제외)
- 80자 미만으로 truncate

**예시:**

- `20260224-linkedin-hook-pattern.md`
- `20260224-workshop-icebreaker-framework.md`
- `20260224-weekly-sync-standup-format.md`
- `20260224-upstage-consulting-onboarding.md`
- `20260224-meetup-networking-structure.md`
</step>

<step number="5" required="true" depends_on="4" blocking="true">
### Step 5: YAML 검증 (BLOCKING)

**schema.yaml 기반으로 모든 필수 필드 검증.**

<validation_gate name="yaml-schema" blocking="true">

**검증 항목:**

- `domain`: schema.yaml의 enum 값 중 하나
- `date`: YYYY-MM-DD 형식
- `insight_type`: schema.yaml의 enum 값 중 하나
- `component`: 해당 domain에 매핑된 enum 값 중 하나 (`domain_component_mapping` 확인)
- `context`: 20-300자, 구체적 상황 서술
- `key_learning`: 10-200자, 일반화 가능한 교훈
- `impact`: critical / high / medium / low
- `tags`: 1-8개, 소문자 하이픈 구분

**검증 실패 시 Step 6 차단:**

```
YAML 검증 실패

오류:
- domain: 허용된 값이 아님: "marketing" → guild, contents, community, business, knowledge 중 하나
- component: domain 'guild'에는 허용되지 않는 컴포넌트: "linkedin" → operations, culture, hiring, sync, decision-making, season-planning 중 하나
- tags: 대문자 포함 → 소문자로 변환 필요

수정된 값을 제공해주세요.
```

**GATE 강제:** 모든 검증 통과 전까지 Step 6 진행 금지.

</validation_gate>
</step>

<step number="6" required="true" depends_on="5">
### Step 6: 문서 작성

**카테고리 디렉토리 결정:** schema.yaml의 `category_mapping`으로 insight_type → 저장 경로 매핑.

**문서 생성:**

```bash
INSIGHT_TYPE="[검증된 YAML에서]"
CATEGORY_DIR="[category_mapping에서 매핑]"
FILENAME="[Step 4에서 생성]"
DOC_PATH="${CATEGORY_DIR}${FILENAME}"

# 디렉토리 없으면 생성
mkdir -p "${CATEGORY_DIR}"

# assets/resolution-template.md 기반으로 문서 작성
# (Step 2에서 수집한 컨텍스트 + Step 5에서 검증한 YAML frontmatter)
```

**결과:**

- 카테고리 디렉토리에 단일 파일 생성
- Enum 검증으로 일관된 분류 보장
</step>

<step number="7" required="false" depends_on="6">
### Step 7: 교차 참조 & 패턴 감지

**Step 3에서 유사 문서 발견된 경우:**

```bash
# 기존 문서에 Related 섹션 추가
# 새 문서에도 기존 문서 링크 추가
```

**패턴 후보 감지:**

동일 카테고리에 유사 인사이트 3개 이상 존재하면:

```
패턴 문서 후보 감지: [카테고리]에 유사 인사이트 X개
→ patterns/ 문서로 종합하시겠습니까?
```

**Critical Pattern 승격 조건 (자동 승격 금지, 사용자 결정):**

- impact가 `critical`인 경우
- 여러 도메인에 횡단 적용 가능한 경우
- 팀 전체가 반드시 알아야 하는 경우

이 경우 Decision Menu에서 "2. 크리티컬 패턴에 추가" 옵션에 주석 추가:

```
💡 이 인사이트는 크리티컬 패턴 승격을 고려해볼 만합니다
```

</step>

</critical_sequence>

---

<decision_gate name="post-documentation" wait_for_user="true">

## Decision Menu After Capture

문서화 성공 후 선택지 제시 및 사용자 응답 대기:

```
인사이트가 기록되었습니다.

파일 생성:
- knowledge/solutions/[category]/[filename].md

다음 작업:
1. 계속 진행 (권장)
2. 크리티컬 패턴에 추가 - critical-patterns.md에 승격
3. 관련 문서 연결 - 유사 인사이트와 교차 참조
4. 기존 스킬에 추가 - .claude/skills/에 연결
5. 문서 확인 - 생성된 내용 보기

선택: _
```

**각 옵션 처리:**

**Option 1: 계속 진행**

- 현재 작업/워크플로우로 복귀
- 문서화 완료

**Option 2: 크리티컬 패턴에 추가**

사용자가 선택하는 경우:
- 팀 전체에 반복 적용되는 패턴
- 절대 잊어서는 안 되는 교훈
- 비직관적이지만 필수적인 규칙

액션:
1. 문서에서 패턴 추출
2. assets/critical-pattern-template.md 형식으로 구조화
3. `knowledge/solutions/patterns/critical-patterns.md`에 추가 (순번 유지)
4. 해당 문서에 교차 참조 추가
5. 확인: "크리티컬 패턴에 추가되었습니다. 이후 learnings-researcher가 항상 이 패턴을 확인합니다."

**Option 3: 관련 문서 연결**

- 프롬프트: "어떤 문서와 연결할까요? (파일명 또는 주제 설명)"
- `knowledge/solutions/`에서 대상 문서 검색
- 양방향 교차 참조 추가
- 확인: "교차 참조가 추가되었습니다"

**Option 4: 기존 스킬에 추가**

- 프롬프트: "어떤 스킬에 추가할까요?"
- `.claude/skills/[skill-name]/`의 적절한 파일에 링크와 설명 추가
- 확인: "[skill-name] 스킬에 추가되었습니다"

**Option 5: 문서 확인**

- 생성된 문서 내용 표시
- Decision Menu 다시 제시

</decision_gate>

---

<integration_protocol>

## 통합 지점

**호출 트리거:**
- `/compound` 커맨드 (주 인터페이스)
- 대화 중 확인 문구 자동 감지
- 워크플로우 완료 후 수동 호출

**호출하는 스킬/에이전트:**
- 없음 (terminal 스킬 - 다른 스킬에 위임하지 않음)

**Handoff 조건:**
호출 전 대화 이력에 충분한 컨텍스트가 있어야 함.

</integration_protocol>

---

<success_criteria>

## 성공 기준

다음 모든 조건이 충족될 때 문서화 성공:

- YAML frontmatter 검증 통과 (모든 필수 필드, 올바른 형식, 유효한 enum 값)
- `knowledge/solutions/[category]/[filename].md`에 파일 생성됨
- domain-component 매핑이 schema.yaml과 일치
- Context, What Worked, Why This Works 섹션이 구체적으로 작성됨
- 유사 문서 발견 시 교차 참조 추가됨
- 사용자에게 Decision Menu 제시 및 액션 확인됨

</success_criteria>

---

## 에러 처리

**컨텍스트 부족:**

- 사용자에게 누락된 정보 질문
- 필수 정보 확보 전 진행 금지

**YAML 검증 실패:**

- 구체적인 오류 항목 표시
- 수정된 값으로 재시도
- 통과할 때까지 차단

**유사 인사이트 모호함:**

- 여러 후보 모두 표시
- 사용자 선택: 새 문서 / 기존 업데이트 / 별도 연결

**카테고리 매핑 불확실:**

- 가장 근접한 카테고리 제안
- 사용자 확인 후 진행

---

## 실행 가이드라인

**반드시 해야 하는 것:**
- YAML frontmatter 검증 (Step 5 validation gate는 blocking)
- domain-component 매핑 유효성 확인
- 파일 작성 전 `mkdir -p`로 디렉토리 생성
- 컨텍스트 누락 시 사용자에게 묻고 대기
- key_learning은 다른 상황에도 적용 가능하게 일반화

**절대 하지 말아야 하는 것:**
- YAML 검증 건너뛰기 (validation gate는 blocking)
- 모호한 설명으로 문서화 (검색 불가)
- 가설이나 미검증 내용 문서화
- critical pattern 자동 승격 (사용자 결정 필요)

---

## 예시 시나리오

**사용자:** "업스테이지 워크샵에서 아이스브레이커로 'AI 사용 경험 공유'를 먼저 했더니 참여도가 확 올라갔어. 다음에도 이렇게 하자."

**스킬 활성화:**

1. **트리거 감지:** "다음에도 이렇게 하자" → 자동 활성화
2. **컨텍스트 수집:**
   - domain: business
   - insight_type: consulting_pattern
   - component: consulting
   - context: "업스테이지 AI 워크샵에서 기술 실습 전 아이스브레이커로 'AI 사용 경험 공유' 세션을 진행했을 때 참여도와 분위기가 크게 개선됨"
   - key_learning: "B2B 워크샵에서 실습 전 개인 경험 공유 아이스브레이커가 참여자의 심리적 안전감과 참여도를 높인다"
   - impact: high
   - tags: [workshop, icebreaker, consulting, engagement, upstage]
3. **기존 문서 검색:** knowledge/solutions/consulting-patterns/ 검색
4. **파일명 생성:** `20260224-workshop-icebreaker-experience-sharing.md`
5. **YAML 검증:** ✅ 통과
6. **문서 작성:** `knowledge/solutions/consulting-patterns/20260224-workshop-icebreaker-experience-sharing.md`
7. **교차 참조:** 없음 (유사 문서 없음)

**출력:**

```
인사이트가 기록되었습니다.

파일 생성:
- knowledge/solutions/consulting-patterns/20260224-workshop-icebreaker-experience-sharing.md

다음 작업:
1. 계속 진행 (권장)
2. 크리티컬 패턴에 추가 - critical-patterns.md에 승격
3. 관련 문서 연결 - 유사 인사이트와 교차 참조
4. 기존 스킬에 추가 - .claude/skills/에 연결
5. 문서 확인 - 생성된 내용 보기
```
