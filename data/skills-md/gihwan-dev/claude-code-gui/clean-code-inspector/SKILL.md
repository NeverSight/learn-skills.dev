---
name: clean-code-inspector
description: React 코드 품질 분석. git diff 기반으로 변경된 코드의 클린 코드 점수 평가. "코드 리뷰", "품질 검사" 등의 요청 시 사용
disable-model-invocation: false
---

1. **Identify Changes**:
   - Run `git status` to see the current state.
   - Run `git diff --name-only` (or `git diff --cached --name-only` if changes are staged) to get the list of modified files.
   - Focus on React components and logic files (`.tsx`, `.ts`, `.jsx`, `.js`).

2. **Analyze Code** (adaptive parallelism):

   **변경 파일 수에 따른 분석 전략:**

   #### 3개 이하: 순차 분석 (기존 방식)

   각 파일을 직접 `git diff`로 검사하고 Scorecard 프레임워크에 따라 평가합니다.

   #### 4개 이상: 병렬 분석

   **2-A: 파일 그룹화**
   변경된 파일들을 디렉토리/기능 영역별로 그룹화합니다:
   - 같은 디렉토리의 파일들 → 하나의 그룹
   - 관련 컴포넌트 + 훅 + 타입 → 하나의 그룹
   - 독립적인 파일 → 개별 그룹

   **2-B: 병렬 분석**
   각 그룹을 Task sub-agent로 동시 분석합니다:

   ```
   Task call:
     subagent_type: "general-purpose"
     model: "sonnet"
     description: "Analyze code quality for [그룹명]"
     run_in_background: true
     prompt: |
       You are a React Clean Code Inspector. Analyze the following files
       for code quality using the React Clean Code Scorecard framework.

       Files to analyze: [파일 목록]

       Run `git diff -- [파일]` for each file to see the changes.

       Evaluate strictly based on these metrics:
       - Cyclomatic Complexity (CC): branch count in JSX, nested ternaries
       - Component Responsibility Score (CRS): LoC + CC + State Count + Dependency Count
       - Cohesion (LCOM4): hook and state connectivity
       - Interface Quality: props count, boolean props, naming conventions
       - State Architecture: colocation, global state density

       For each file, provide:
       1. Per-metric scores with measured values
       2. Status (양호/주의/위험) for each metric
       3. Specific recommendations

       Output as structured markdown with the Scorecard table format.
   ```

   모든 그룹 분석 Task가 완료될 때까지 대기한 후 결과를 수집합니다.

   **2-C: 결과 통합**
   오케스트레이터가 모든 그룹의 분석 결과를 통합하여 전체 Scorecard를 생성합니다:
   - 그룹별 결과를 병합
   - 크로스-파일 이슈 식별 (그룹 간 결합도, 공통 패턴 위반 등)
   - 전체 종합 점수 산출

   **CRITICAL**: You must evaluate the code strictly based on the **"React Clean Code Scorecard"** framework provided below. Do not use generic "clean code" advice; use these specific metrics.

   <FRAMEWORK_START>

   # 리액트 애플리케이션의 아키텍처 건전성 및 클린 코드 품질 평가를 위한 정량적 지표 프레임워크

   ## 1. 서론

   주관적인 "클린 코드"가 아닌, 정량적이고 객관적인 엔지니어링 지표로 평가합니다.

   ## 2. 구조적 복잡도 (Structural Complexity)
   - **순환 복잡도 (CC)**: 조건부 렌더링 경로, 분기 수 측정.
     - JSX 내 삼항 연산자 중첩 등 분기 폭발 확인.
     - 점수: 1~10(안전), 11~20(주의), 21~50(위험), >50(불가).
   - **인지 복잡도**: 중첩된 훅/콜백, JSX 깊이(max-depth > 3~4 주의), 의존성 배열 크기(>5 위험).

   ## 3. 컴포넌트 책임 점수 (CRS)
   - CRS = w1(LoC) + w2(CC) + w3(SC) + w4(DC)
   - **Line of Code (LoC)**: >200줄 위험, 100줄 이내 권장.
   - **State Count (SC)**: useState 개수. 0~3(건강), 4~6(주의), >6(위험).
   - **Dependency Count (DC)**: import 개수. >10개 주의.
   - CRS 결과: <50(Atomic), 50-100(Boundary), >100(God Component - Refactor Alert).

   ## 4. 응집도(Cohesion)와 결합도(Coupling)
   - **Props Drilling**: Depth > 3 이면 불필요한 결합.
   - **LCOM4 (React Hook Cohesion)**: 내부 상태와 메서드(Effect/Callback)간의 연결 그래프 분석.
     - LCOM4 > 1 이면 로직 분리 필요 (커스텀 훅 등으로).

   ## 5. 컴포넌트 인터페이스 품질
   - **Props 개수**: <5(이상적), 5~7(허용), >7(Code Smell).
   - **Boolean Props**: 다수의 boolean 대신 Enum/Status 문자열 사용 권장.
   - **Naming**: `on` 접두사(Props) / `handle` 접두사(Implementation) 일관성.

   ## 6. 정적 분석 지표 (ESLint)
   - `react-hooks/rules-of-hooks`: 0 위반
   - `max-lines-per-function`: < 100
   - `no-console`: 0 위반
   - `TypeScript noImplicitAny`: 0%

   ## 7. 테스트 가능성 (Mutation Score)
   - 비즈니스 로직 훅/유틸리티의 경우 Mutation Score > 80% 목표.

   ## 8. 상태 아키텍처
   - **State Colocation**: 상태가 사용되는 곳과 얼마나 가까운가.
   - **Global State Density**: 꼭 필요한 전역 상태인지 확인.

   ## 9. 종합 스코어카드

   평가 결과는 아래 표 형식을 포함하여 정리해야 합니다.

   | 카테고리   | 평가 항목         | 측정/관찰 값 | 상태 (양호/주의/위험) | 비고 |
   | ---------- | ----------------- | ------------ | --------------------- | ---- |
   | 복잡도     | 순환 복잡도 (CC)  | ...          | ...                   | ...  |
   | 규모       | 라인 수 (LoC)     | ...          | ...                   | ...  |
   | 인터페이스 | Props 개수        | ...          | ...                   | ...  |
   | 결합도     | Props 드릴링 깊이 | ...          | ...                   | ...  |
   | 응집도     | LCOM4 (추정)      | ...          | ...                   | ...  |
   | 위생       | 훅 의존성 준수    | ...          | ...                   | ...  |

   <FRAMEWORK_END>

3. **Generate Report**:
   - Create a file named `clean-code-inspect-result.md` in the project root.
   - **Language**: Korean (한국어). All analysis, summaries, and recommendations must be written in Korean.
   - Format: Markdown.
   - Content:
     - **Summary**: High-level assessment of the changes.
     - **Detailed Analysis**: For each modified component, provide the CRS breakdown, complexity analysis, and specific metric violations.
     - **Scorecard**: The table defined in Section 9 of the framework.
     - **Recommendations**: Specific refactoring actions based on the "Quality Impact" guidance.
     - (병렬 분석 시) **분석 방식**: 그룹 구성과 병렬 분석 결과 요약 포함.
