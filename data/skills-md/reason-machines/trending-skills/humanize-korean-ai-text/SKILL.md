---
name: humanize-korean-ai-text
description: AI가 쓴 한글 글을 사람이 쓴 것처럼 윤문해주는 Claude Code 스킬 — 번역투·관용구·구조적 AI 패턴 40+ 서브 패턴 탐지 및 수술적 수정
triggers:
  - "AI 티 없애줘"
  - "GPT 문체 제거해줘"
  - "사람이 쓴 것처럼 윤문해줘"
  - "번역투 제거"
  - "한글 AI 윤문"
  - "AI가 쓴 글 자연스럽게 고쳐줘"
  - "ChatGPT 문체 사람처럼 바꿔줘"
  - "한국어 AI 탐지 우회 윤문"
---

# Humanize KR — 한글 AI 티 제거기 (im-not-ai)

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

AI(ChatGPT · Claude · Gemini 등)가 생성한 한글 텍스트를 **내용은 그대로 유지하면서** 문체·리듬·표현만 자연스러운 한국어로 변환하는 Claude Code 스킬입니다. 번역투, 기계적 병렬 구조, AI 특유 관용구, 피동태 남용 등 10대 카테고리 × 40+ 패턴을 탐지·수정합니다.

---

## 설치

```bash
git clone https://github.com/epoko77-ai/im-not-ai.git
cd im-not-ai
claude
```

> **반드시 `im-not-ai` 폴더 안에서** `claude`를 실행해야 스킬이 로드됩니다. 다른 경로에서 실행하면 일반 Claude Code로 동작합니다.

**사전 요건:** [Claude Code](https://claude.com/claude-code) CLI 설치 필요

```bash
claude --version  # 설치 확인
```

---

## 기본 사용법

### 방법 A — 자연어 (가장 쉬움)

```
이 AI 글 자연스럽게 윤문해줘:

[ChatGPT / Claude / Gemini 초안 붙여넣기]
```

아래 표현 중 아무거나 써도 스킬이 자동 발동합니다:
- `"AI 티 없애줘"`
- `"GPT 문체 제거해줘"`
- `"사람이 쓴 것처럼 윤문해줘"`
- `"번역투 제거"`
- `"한글 AI 윤문"`

### 방법 B — 슬래시 커맨드

```bash
/humanize [텍스트 또는 파일 경로]

# 옵션 예시
/humanize ./draft.txt 장르: 칼럼
/humanize ./report.md 강도: 적극 최소심각도: S1
/humanize ./essay.txt 원문 톤을 더 살려줘

# 결과가 맘에 안 들면 재실행
/humanize-redo "번역투만 다시"
/humanize-redo "관용구만 재처리"
```

### 방법 C — Plugin 설치 (포크 버전)

```bash
# gaebalai 포크 — Claude Code Plugin 규격
/plugin install humanize-korean@epoko77-ai-plugins

# 또는 스크립트로 다른 프로젝트에 설치
./scripts/install.sh --target ~/my-project
```

---

## 처리 모드

### Fast 모드 (디폴트 — 5,000자 이하)

`humanize-monolith` 에이전트 단일 호출로 탐지·윤문·자체검증을 한 번에 처리합니다.

- **소요 시간:** 약 2~3분
- **도구 호출:** 4~5회 캡 (Read 입력 → Read 룰북 → Write final → Write summary)
- **자동 선택 조건:** 입력 5,000자 이하

```
입력 텍스트
    ↓
[humanize-monolith]  ← 탐지 + 윤문 + 자체검증 일괄
    ↓
_workspace/{날짜-번호}/final.md
_workspace/{날짜-번호}/summary.md
```

### Strict 모드 (`--strict` 또는 8,000자+)

5인 파이프라인이 단계별로 처리하며 각 단계 결과물을 별도 파일로 저장합니다.

```bash
/humanize ./long-report.md --strict
```

```
입력 텍스트
    ↓
[ai-tell-detector]          → 02_detection.json
    ↓
[korean-style-rewriter]     → 03_rewrite.md
    ↓
[content-fidelity-auditor]  → 04_fidelity_audit.json  (병렬)
[naturalness-reviewer]      → 05_naturalness_review.json (병렬)
    ↓
[오케스트레이터 종합]
    ↓
final.md + summary.md
```

---

## 출력 파일 구조

```
_workspace/
└── 20260426-001/          # 실행마다 새 폴더 생성
    ├── 01_input.txt       # 원문 그대로
    ├── final.md           # 윤문 결과
    └── summary.md         # 메트릭 · 탐지 결과 · 등급 · 주요 변경

# Strict 모드 추가 파일
    ├── 02_detection.json          # span 단위 AI 티 탐지 리포트
    ├── 03_rewrite.md              # 윤문본 초안
    ├── 04_fidelity_audit.json     # 의미 동등성 감사 (13항 체크리스트)
    └── 05_naturalness_review.json # 자연도 재측정 결과
```

---

## AI 티 분류 체계 — 10대 카테고리

| ID | 대분류 | 주요 패턴 예시 |
|----|--------|--------------|
| **A** | 번역투 | `~를 통해`, `~에 있어서`, `~되어진다` (이중 피동), `가지고 있다` |
| **B** | 영어 인용 과다 | 번역 가능한 영어 그대로 사용, 과도한 괄호 병기 |
| **C** | 구조적 AI 패턴 | 기계적 `첫째/둘째/셋째`, 과도한 불릿·헤딩·이모지 |
| **D** | AI 특유 관용구 | `결론적으로`, `시사하는 바가 크다`, `주목할 만하다`, `혁신적인` |
| **E** | 리듬 균일성 | 문장 길이 표준편차 낮음, 동일 종결어미 반복 |
| **F** | 수식·중복 | `매우`, `정말`, 동의어 이중 수식, `~적/~성/~화` 남발 |
| **G** | Hedging 남용 | `~할 수 있을 것으로 보인다` 다중 완곡 |
| **H** | 접속사 남발 | 문두 `또한/따라서/즉/나아가` 연속 |
| **I** | 형식명사 과다 | `것이다`, `점`, `수`, `바`, `~할 필요가 있다` |
| **J** | 시각 장식 남용 | 과도한 **볼드**, `"따옴표"`, 대시(`—`) 남발 |

전체 40+ 서브 패턴: `.claude/skills/humanize-korean/references/ai-tell-taxonomy.md`

---

## 심각도 기준

| 등급 | 기준 | 처리 |
|------|------|------|
| **S1 결정적** | 한 번만 나와도 AI 확신 | 무조건 제거 |
| **S2 강함** | 1~2회 허용, 3회+ 반복 | 반복 시 제거 |
| **S3 약함** | 단독으로는 무해 | 다른 패턴 중첩 시만 제거 |

---

## 품질 등급 (윤문 후 summary.md 확인)

| 등급 | 기준 | 후속 조치 |
|------|------|----------|
| **A** | S1 0건, S2 ≤2건, 점수 개선 70%+ | 완료 |
| **B** | S1 0건, S2 ≤4건, 개선 50%+ | 완료 |
| **C** | S1 1~2건 or 과윤문 시그널 2개 | 2차 윤문 자동 시작 |
| **D** | S1 3건+ or 심각한 과윤문 | 사람 검토 권고 |

---

## 4대 철칙 (에이전트가 항상 따르는 규칙)

1. **의미 불변** — 사실·주장·수치·고유명사·직접 인용 100% 원문 보존
2. **근거 기반** — 탐지된 span에만 수술적 수정, 탐지 없는 구간 불변
3. **장르 유지** — 칼럼→문학, 리포트→에세이 변환 금지
4. **과윤문 금지** — 변경률 30% 초과 시 경고, 50% 초과 시 강제 중단

---

## 탐지·윤문 제외 대상

다음 항목은 절대 수정하지 않습니다:

- 수치·단위·날짜
- 고유명사·인명·제품명·모델명
- 큰따옴표 내부 직접 인용
- 법률·규정 조문
- 학술 개념어 (불가피한 경우)

---

## 실제 변환 예시

### 번역투 (카테고리 A)

```
Before: AI 기술을 통해 효율을 높일 수 있다.
After:  AI로 효율을 높인다.

Before: 이에 있어서 중요한 점은
After:  여기서 중요한 건

Before: ~에 의해 생성된
After:  ~가 만든

Before: 가지고 있다
After:  있다
```

### AI 관용구 (카테고리 D)

```
Before: 결론적으로, 이는 시사하는 바가 크다.
After:  (삭제 또는 문맥에 맞게 구체화)

Before: 이는 주목할 만한 혁신적인 접근법이다.
After:  이 방식은 눈길을 끈다.
```

### Hedging 남용 (카테고리 G)

```
Before: 이는 효과적일 수 있을 것으로 보인다.
After:  이 방식은 효과적이다. (또는 문맥에 따라 적절히 완곡화)
```

### 기계적 병렬 (카테고리 C)

```
Before:
첫째, 비용이 절감된다.
둘째, 시간이 단축된다.
셋째, 품질이 향상된다.

After:
비용과 시간이 줄고 품질도 오른다.
```

---

## 재실행 · 수정 명령

결과가 마음에 안 들면 자연어로 말씀하시면 됩니다:

```
"이 문단만 다시 윤문해줘"          → 해당 구간만 재시도
"번역투만 더 손봐줘"               → 카테고리 A만 재처리
"관용구만 다시"                    → 카테고리 D만 재처리
"윤문 강도 낮춰줘"                 → S1 결정적 패턴만 제거
"원문 톤을 더 살려줘"              → 변경률 상한 낮춤
"2차 윤문해줘"                     → 현재 결과를 한 번 더 다듬기
```

부분 재실행 명령은 자동으로 Strict 모드로 전환됩니다.

---

## 에이전트 구성 (참고)

| 에이전트 | 모드 | 역할 |
|---------|------|------|
| `humanize-monolith` | Fast (디폴트) | 탐지·윤문·자체검증 일괄 처리 |
| `ai-tell-detector` | Strict | span 단위 JSON 탐지 리포트 |
| `korean-style-rewriter` | Strict | finding 기반 수술적 윤문, 변경률 모니터링 |
| `content-fidelity-auditor` | Strict | 의미 동등성 감사 (13항 체크리스트) |
| `naturalness-reviewer` | Strict | 잔존 AI 티·과윤문·자연도 판정, 등급 A~D |
| `korean-ai-tell-taxonomist` | 별도 명령 | 분류 체계(SSOT) 관리, 신규 패턴 심사 |
| `humanize-web-architect` | 옵션 | Next.js 15 + Vercel 웹 서비스 확장 설계 |

---

## 핵심 참조 파일

```
.claude/skills/humanize-korean/
├── references/
│   ├── ai-tell-taxonomy.md      # 40+ 서브 패턴 전체 목록 및 처방
│   ├── rewriting-playbook.md    # 카테고리별 윤문 규칙
│   ├── quick-rules.md           # Fast 모드용 슬림 룰북 (~150줄)
│   └── web-service-spec.md      # 웹 서비스 확장 설계
└── commands/
    ├── humanize                 # /humanize 커맨드 정의
    └── humanize-redo            # /humanize-redo 커맨드 정의
```

---

## 자주 묻는 문제

**Q: 스킬이 로드되지 않고 일반 Claude처럼 동작해요**  
→ `im-not-ai` 폴더 안에서 `claude`를 실행했는지 확인하세요.

```bash
pwd  # /path/to/im-not-ai 이어야 함
claude
```

**Q: 처리가 너무 오래 걸려요 (25분+)**  
→ v1.5 이전 버전 문제입니다. `git pull`로 최신 버전을 받으세요. Fast 모드는 2~3분 내 완료됩니다.

**Q: 변경률이 50%를 넘어 강제 중단됐어요**  
→ 과윤문 방지 안전장치입니다. `"윤문 강도 낮춰줘"` 또는 `"S1만 제거해줘"`로 재실행하세요.

**Q: 수치나 고유명사가 바뀌었어요**  
→ 버그입니다. `_workspace/{날짜-번호}/01_input.txt`와 `final.md`를 비교해 신고해 주세요: [Issues](https://github.com/epoko77-ai/im-not-ai/issues)

**Q: 웹 버전이나 API로도 쓸 수 있나요?**  
→ 현재는 Claude Code CLI 전용입니다. 웹 서비스는 v1.6 로드맵에 있습니다 (`humanize-web-architect` 에이전트로 설계 중).

**Q: 일본어·중국어도 되나요?**  
→ 현재는 한국어 전용입니다. v4 로드맵에 일본어·중국어 확장이 포함되어 있습니다.

---

## 버전 히스토리 요약

| 버전 | 주요 변경 |
|------|----------|
| v1.5 | Monolith Fast Path 신설, v1.2~v1.4 롤백, `quick-rules.md` 추가 |
| v1.4 | 역할별 모델 분산 (성능 문제로 폐기) |
| v1.3 | Candidate pool 도입 (폐기) |
| v1.2 | Voice profile 도입 (폐기) |
| v1.1 | 5인 에이전트 파이프라인 (Strict 모드로 보존) |
