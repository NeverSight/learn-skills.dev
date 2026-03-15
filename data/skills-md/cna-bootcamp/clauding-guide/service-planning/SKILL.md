---
name: service-planning
description: 비즈니스 도메인만 입력하면 MVP 정의부터 프로토타입까지 전체 서비스 기획 워크플로우를 자동으로 실행합니다. 17개의 전문화된 스킬을 순차적으로 orchestrate하여 완전한 기획 산출물을 생성합니다. (project)
---

# AI 서비스 기획 자동화

비즈니스 도메인만 제공하면 MVP 개념부터 프로토타입 개발까지 완전한 엔드-투-엔드 서비스 기획을 자동으로 수행합니다.

## 사용 시점

- 사용자가 MVP 주제 또는 제품 아이디어를 제공할 때
- 새로운 서비스 기획 프로젝트를 시작할 때
- 처음부터 완전한 기획 워크플로우가 필요할 때
- 사용자가 "서비스 기획", "MVP 만들기", "전체 기획 프로세스"를 언급할 때

## 워크플로우 개요

이 skill은 6개 단계에서 17개의 전문화된 스킬을 orchestrate합니다:

```
1단계: 정의 (MVP + 고객 + 지침)
   ↓
2단계: 문제 발견 및 방향성 (시장 + 고객경험 단계 + 경험 조사 + 여정 맵 + 문제 가설 + 방향성)
   ↓
3단계: 솔루션 (아이디어 발상 + 선정)
   ↓
4단계: 비즈니스 모델 + 발표자료
   ↓
5단계: 제품 설계 (이벤트 스토밍 + 유저스토리 + UI/UX)
   ↓
6단계: 프로토타입
```

## 실행 지침

사용자가 MVP 주제를 제공하면 다음 완전한 워크플로우를 실행합니다:

### 1단계: 주제 정의, 고객 분석 및 지침 작성 (10-15분)

**Step 1.1: MVP 정의**
```
01-mvp-definition skill 호출
입력: 사용자의 MVP 주제/비즈니스 도메인
출력: 명확한 MVP 범위, 도메인, 시장 잠재력
저장: define/MVP정의.md
```

**Step 1.2: 고객 분석**
```
02-customer-analysis skill 호출
입력: MVP 정의 결과 (define/MVP정의.md)
출력: JTBD를 포함한 타겟 고객 페르소나
저장: define/고객분석.md
```

**Step 1.3: 지침 작성**
```
03-guidelines skill 호출
입력: 고객 분석 결과 (define/고객분석.md)
출력: 프로젝트 팀 구성 및 협업 지침 (MVP 주제, 고객 유형, 팀원, 팀 행동원칙, 대화 가이드)
저장: CLAUDE.md (루트)
```

### 2단계: 문제 발견 및 방향성 정의 (25-30분)

**Step 2.1: 시장 조사**
```
04-market-research skill 호출
입력: MVP 주제 + 고객 분석 + 지침 (define/MVP정의.md, define/고객분석.md, CLAUDE.md)
출력: 시장 분석, 경쟁 현황, 트렌드
저장: define/시장조사.md
```

**Step 2.2: 고객경험 단계 정의**
```
05-customer-journey-stages skill 호출
입력: MVP 주제 + 고객 분석 + 시장 조사 + 지침 (CLAUDE.md)
출력: 현재 고객 경험 단계 (5-7단계)
저장: define/고객경험단계.md
```

**Step 2.3: 고객 경험 조사**
```
06-customer-experience skill 호출
입력: 고객 페르소나 + 고객경험 단계 + 지침 (define/고객분석.md, define/고객경험단계.md, CLAUDE.md)
출력: 인터뷰 데이터, 관찰 결과, 고통점 (경험 단계 기반)
저장: define/관찰결과.md, define/체험결과.md, define/고객경험인터뷰결과.md, define/고객경험인터뷰결과취합.md
```

**Step 2.4: 고객 여정 맵 작성**
```
07-journey-mapping skill 호출
입력: 고객 분석 + 경험 데이터 + 고객경험 단계 + 지침 (CLAUDE.md)
출력: 완전한 고객 여정 맵 (경험 단계를 X축으로 사용)
저장: define/유저저니맵.md, define/유저저니맵.svg
```

**Step 2.5: 문제 가설 정의**
```
08-problem-hypothesis skill 호출
입력: 고객 여정 맵 인사이트 + 지침 (define/유저저니맵.md, CLAUDE.md)
출력: 해결해야 할 핵심 문제 진술
저장: define/문제가설.md, define/문제검증인터뷰결과.md, define/문제검증인터뷰결과취합.md, define/비즈니스가치.md
```

**Step 2.6: 방향성 정의**
```
09-direction-setting skill 호출
입력: 문제 가설 + 고객 고통점 + 지침 (define/문제가설.md, define/고객경험인터뷰결과취합.md, CLAUDE.md)
출력: 킹핀 문제 식별, Needs Statement
저장: think/킹핀문제.md, think/문제해결방향성.md
```

### 3단계: 솔루션 탐색 (10-15분)

**Step 3.1: 아이디어 발상**
```
10-ideation skill 호출
입력: 문제 가설 + 지침 (define/문제가설.md, think/킹핀문제.md, think/문제해결방향성.md, CLAUDE.md)
출력: 다양한 솔루션 아이디어 (10-20개)
저장: think/솔루션탐색.md, think/솔루션후보.md
```

**Step 3.2: 솔루션 선정**
```
11-solution-selection skill 호출
입력: 아이디어 발상 결과 + 지침 (think/솔루션탐색.md, think/솔루션후보.md, CLAUDE.md)
출력: 근거와 함께 선정된 최적 솔루션
저장: think/솔루션평가.md, think/솔루션우선순위평가.svg, think/핵심솔루션.md
```

### 4단계: 비즈니스 모델 및 발표자료 (15-20분)

**Step 4.1: 비즈니스 모델 캔버스**
```
12-business-modeling skill 호출
입력: 선정된 솔루션 + 고객 분석 + 지침 (think/핵심솔루션.md, define/고객분석.md, define/문제가설.md, CLAUDE.md)
출력: 완전한 린 캔버스
저장: think/비즈니스모델.md
```

**Step 4.2: 발표자료 스크립트**
```
13-presentation skill 호출
입력: 비즈니스 모델 + 모든 이전 산출물 + 지침 (CLAUDE.md)
출력: 투자자/임원진용 10-15장 발표 자료 스크립트
저장: think/서비스기획서스크립트.md
```

### 5단계: 제품 설계 (20-25분)

**Step 5.1: 이벤트 스토밍**
```
14-event-storming skill 호출
입력: 선정된 솔루션 + 고객 여정 + 방향성 정의 + 지침 (think/핵심솔루션.md, define/고객분석.md, CLAUDE.md)
출력: 각 유저 플로우에 대한 PlantUML 시퀀스 다이어그램
저장: think/es/userflow.puml, think/es/{순번}-{유저플로우명}.puml
```

**Step 5.2: 유저스토리 작성**
```
15-user-stories skill 호출
입력: 이벤트 스토밍 PlantUML 다이어그램 + 고객 여정 + 지침 (think/핵심솔루션.md, define/고객분석.md, think/es/*.puml, CLAUDE.md)
출력: 인수 기준이 포함된 완전한 유저스토리
저장: design/userstory.md
```

**Step 5.3: UI/UX 설계**
```
16-uiux-design skill 호출
입력: 유저스토리 + 고객 페르소나 + 지침 (design/userstory.md, think/핵심솔루션.md, CLAUDE.md)
출력: UI/UX 명세서 및 와이어프레임
저장: design/uiux/uiux.md, design/uiux/style-guide.md
```

### 6단계: 프로토타입 개발 (15-20분)

**Step 6.1: 프로토타입 가이드**
```
17-prototype-development skill 호출
입력: 모든 이전 산출물 + 지침 (design/uiux/uiux.md, design/uiux/style-guide.md, design/userstory.md, think/핵심솔루션.md, CLAUDE.md)
출력: 기본 HTML/JavaScript 프로토타입 개발 가이드
저장: design/uiux/prototype/{화면순서번호 2자리}-{화면명}.html, common.js, common.css
```

## 실행 가이드라인

### 순차적 처리
- 다음 단계로 넘어가기 전에 각 단계를 완료합니다
- 이전 산출물을 다음 스킬에 컨텍스트로 전달합니다
- 진행하기 전에 산출물을 검증합니다
- 모든 산출물을 해당 디렉토리에 저장합니다 (define/, think/, design/)

### 컨텍스트 누적
각 스킬은 다음을 받습니다:
- 모든 이전 단계 산출물
- 원래 MVP 주제
- 사용자의 추가 입력 또는 설명

### 진행 상황 보고
각 단계 후 보고:
- ✅ 완료된 단계 이름
- 📄 생성된 파일
- ⏭️ 다음 단계 미리보기
- ⏱️ 예상 남은 시간

### 에러 처리
스킬이 실패한 경우:
1. 에러를 명확히 보고합니다
2. 사용자에게 설명/입력을 요청합니다
3. 실패한 스킬을 재시도합니다
4. 중단된 지점부터 계속합니다

## 사용 예시

**사용자 입력:**
> "음식 배달 서비스 MVP를 기획해줘"

**시스템 응답:**
```
🚀 AI 서비스 기획 자동화 시작
프로젝트: 음식 배달 서비스
예상 소요 시간: 100-120분

📋 1단계: 주제, 고객 정의 및 지침 작성 (10-15분)
  ✅ MVP 정의 완료 → define/MVP정의.md
  ✅ 고객 분석 완료 → define/고객분석.md
  ✅ 지침 작성 완료 → CLAUDE.md

📋 2단계: 문제 발견 및 방향성 정의 (25-30분)
  ✅ 시장 조사 완료 → define/시장조사.md
  ✅ 고객경험 단계 정의 완료 → define/고객경험단계.md
  ✅ 고객 경험 조사 완료 → define/관찰결과.md, define/체험결과.md, define/고객경험인터뷰결과.md, define/고객경험인터뷰결과취합.md
  ✅ 고객 여정 맵 완료 → define/유저저니맵.md, define/유저저니맵.svg
  ✅ 문제 가설 정의 완료 → define/문제가설.md, define/문제검증인터뷰결과.md, define/문제검증인터뷰결과취합.md, define/비즈니스가치.md
  ✅ 방향성 정의 완료 → think/킹핀문제.md, think/문제해결방향성.md

📋 3단계: 솔루션 탐색 (10-15분)
  ✅ 아이디어 발상 완료 → think/솔루션탐색.md, think/솔루션후보.md
  ✅ 솔루션 선정 완료 → think/솔루션평가.md, think/솔루션우선순위평가.svg, think/핵심솔루션.md

📋 4단계: 비즈니스 모델 및 발표자료 (15-20분)
  ✅ 비즈니스 모델 완료 → think/비즈니스모델.md
  ✅ 발표자료 스크립트 완료 → think/서비스기획서스크립트.md

📋 5단계: 제품 설계 (20-25분)
  ✅ 이벤트 스토밍 완료 → think/es/userflow.puml, think/es/*.puml
  ✅ 유저스토리 완료 → design/userstory.md
  ✅ UI/UX 설계 완료 → design/uiux/uiux.md, design/uiux/style-guide.md

📋 6단계: 프로토타입 (15-20분)
  ✅ 프로토타입 가이드 완료 → design/uiux/prototype/*.html

🎉 서비스 기획 완료!
📁 모든 산출물: define/ + think/ + design/ 디렉토리
```

## 산출물 구조

```
CLAUDE.md (루트: 프로젝트 지침)

define/
├── MVP정의.md
├── 고객분석.md
├── 시장조사.md
├── 고객경험단계.md
├── 관찰결과.md
├── 체험결과.md
├── 고객경험인터뷰결과.md
├── 고객경험인터뷰결과취합.md
├── 유저저니맵.md
├── 유저저니맵.svg
├── 문제가설.md
├── 문제검증인터뷰결과.md
├── 문제검증인터뷰결과취합.md
└── 비즈니스가치.md

think/
├── 킹핀문제.md
├── 문제해결방향성.md
├── 솔루션탐색.md
├── 솔루션후보.md
├── 솔루션평가.md
├── 솔루션우선순위평가.svg
├── 핵심솔루션.md
├── 비즈니스모델.md
├── 서비스기획서스크립트.md
└── es/
    ├── userflow.puml
    ├── 01-{유저플로우명}.puml
    ├── 02-{유저플로우명}.puml
    └── ...

design/
├── userstory.md
└── uiux/
    ├── uiux.md
    ├── style-guide.md
    └── prototype/
        ├── common.js
        ├── common.css
        ├── 01-{화면명}.html
        ├── 02-{화면명}.html
        └── ...
```

## 최상의 결과를 위한 팁

1. **구체적으로**: 상세한 MVP 주제 제공 (도메인, 타겟 사용자, 핵심 기능)
2. **작업 저장**: 모든 산출물이 증분적으로 저장됨

## 대안 사용법

### 부분 워크플로우
특정 단계만 실행:
- "1-2단계만 실행해줘" (정의 + 문제 발견)
- "5단계부터 시작해줘" (제품 설계부터 시작)

### 단일 스킬
개별 스킬을 직접 실행:
- "고객 여정 맵만 그려줘" → journey-mapping skill만 사용
- "이벤트 스토밍만 해줘" → event-storming skill만 사용

### 워크플로우 재개
이전 작업에서 계속:
- "이전 기획에서 4단계부터 계속해줘"
- 이전 산출물 위치 제공

## 실행 프롬프트 예시

사용자는 간단히 다음과 같이 입력할 수 있습니다:

```
"음식 배달 서비스 MVP 기획해줘"
"온라인 교육 플랫폼 서비스 기획"
"헬스케어 앱 전체 기획 프로세스 실행"
"중고차 거래 플랫폼 MVP부터 프로토타입까지"
```

시스템은 자동으로:
1. 비즈니스 도메인을 파악합니다
2. 16개 스킬을 순차적으로 실행합니다
3. 각 단계의 산출물을 저장합니다
4. 진행 상황을 보고합니다
5. 최종 완전한 기획 산출물을 생성합니다

## 주의사항

- 전체 프로세스는 약 100-120분 소요됩니다
- 모든 산출물은 자동으로 저장되며 작업 내용이 보존됩니다
- 워크플로우는 자동으로 진행되며 각 단계를 순차적으로 완료합니다
- CLAUDE.md는 프로젝트 루트에 생성되며, 이후 모든 스킬에서 참조합니다

## 스킬 참조

이 오케스트레이션 스킬은 다음 17개의 전문화된 스킬을 사용합니다:

1. `01-mvp-definition`: MVP 주제 정의
2. `02-customer-analysis`: 타겟 고객 분석
3. `03-guidelines`: 프로젝트 지침 작성 (팀 구성, 협업 가이드)
4. `04-market-research`: 시장 조사 및 경쟁 분석
5. `05-customer-journey-stages`: 고객경험 단계 정의
6. `06-customer-experience`: 고객 경험 조사
7. `07-journey-mapping`: 고객 여정 맵 작성
8. `08-problem-hypothesis`: 문제 가설 정의
9. `09-direction-setting`: 킹핀 문제 및 방향성 정의
10. `10-ideation`: 아이디어 발상
11. `11-solution-selection`: 솔루션 선정
12. `12-business-modeling`: 비즈니스 모델 캔버스
13. `13-presentation`: 발표자료 스크립트
14. `14-event-storming`: 이벤트 스토밍 (PlantUML)
15. `15-user-stories`: 유저스토리 작성
16. `16-uiux-design`: UI/UX 설계
17. `17-prototype-development`: 프로토타입 개발
