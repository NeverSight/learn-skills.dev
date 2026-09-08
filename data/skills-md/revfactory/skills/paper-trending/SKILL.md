---
name: paper-trending
description: "HuggingFace Daily Papers에서 트렌딩 논문을 수집하여 한줄 요약 리포트를 생성하고, 선택적으로 논문 PDF를 다운로드한다. 트리거: 트렌딩 논문, 인기 논문, paper trending, 최신 논문, 논문 다운로드."
---

# Paper Trending — 트렌딩 논문 한줄 요약 리포트 + 다운로드

HuggingFace Daily Papers API에서 트렌딩 논문을 수집하고 한국어 한줄 요약 테이블로 출력한다.
사용자가 요청하면 논문 PDF를 arxiv에서 다운로드하거나 HTML 버전을 읽어 상세 분석한다.

## 인자 파싱

`/paper-trending` 뒤의 인자를 분석하여 범위를 결정한다:

| 인자 예시 | 해석 | API 파라미터 |
|----------|------|-------------|
| `2026-03-14` | 특정 날짜 | `?date=2026-03-14` |
| `2026-W11` | 특정 주차 | `?week=2026-W11&sort=trending` |
| `이번 주`, `이번주`, `이번 주간`, `this week` | 현재 ISO 주차 | `?week={현재주차}&sort=trending` |
| `최근`, `recent` | 최근 2주 | 현재 주 + 이전 주 각각 호출 |
| (인자 없음), `기본`, `default` | 최근 1개월 | `?month={현재월}&sort=trending` |
| `2026-03` | 특정 월 | `?month=2026-03&sort=trending` |

**추가 액션 인자** (범위 인자와 조합 가능):

| 인자 | 동작 |
|------|------|
| `다운로드`, `download`, `dl` | 트렌딩 리포트 출력 후 상위 N개 논문 PDF 다운로드 |
| `다운로드 5`, `dl 3` | 상위 N개만 다운로드 (기본: 5) |
| `다운로드 all` | 리포트의 모든 논문 다운로드 |
| `읽기 {arxiv_id}`, `read {arxiv_id}` | 특정 논문의 HTML 버전을 읽어 상세 분석 |

예시: `/paper-trending 이번 주 다운로드 3` → 이번 주 트렌딩 리포트 + 상위 3개 PDF 다운로드

**현재 날짜 기준**: 오늘 날짜에서 ISO 주차와 월을 계산한다.

## 워크플로우

### Step 1: 범위 결정

인자를 파싱하여 API 호출 URL을 결정한다.

- ISO 주차 계산이 필요하면 `date +%G-W%V` 또는 Python으로 계산
- "최근"인 경우 현재 주 + 이전 주 2개의 API 호출 필요

### Step 2: API 호출

WebFetch로 HuggingFace API를 호출한다.

**기본 URL**: `https://huggingface.co/api/daily_papers`

**파라미터 (소스 코드 확인된 정확한 사양):**
- `date=YYYY-MM-DD` — 특정 날짜
- `week=YYYY-WNN` — 주간
- `month=YYYY-MM` — 월간
- `sort=trending` — 트렌딩 알고리즘 정렬 (주간/월간에서 권장)
- `sort=publishedAt` — 발행일 정렬 (기본값)
- `p=0,1,2...` — 페이지 번호
- `limit=50` — 페이지당 결과 수 (기본 50)

**호출 예시:**
```
# 이번 주 트렌딩
https://huggingface.co/api/daily_papers?week=2026-W11&sort=trending

# 이번 달
https://huggingface.co/api/daily_papers?month=2026-03&sort=trending

# 특정 날짜
https://huggingface.co/api/daily_papers?date=2026-03-14
```

**"최근" (2주)인 경우** — 두 주차를 병렬로 WebFetch:
```
https://huggingface.co/api/daily_papers?week=2026-W11&sort=trending
https://huggingface.co/api/daily_papers?week=2026-W10&sort=trending
```

결과가 16개 이하이면 `p=1`로 다음 페이지도 호출하여 더 많은 논문 수집.

### Step 3: 데이터 추출

API 응답 JSON에서 각 논문의 다음 정보를 추출:

```
paper.id          → arxiv ID
paper.title       → 제목
paper.upvotes     → upvotes (해당 기간 내 획득분)
paper.ai_summary  → AI 요약 (없으면 paper.summary 사용)
paper.authors[0].name → 첫 번째 저자
paper.organization.fullname → 소속 기관
paper.githubRepo  → GitHub 저장소
paper.githubStars → GitHub 스타 수
```

### Step 4: 출력

upvotes 내림차순으로 정렬하여 마크다운 테이블로 출력한다.

**출력 형식:**

```markdown
# {범위} 트렌딩 논문 ({날짜 범위})

| # | 논문 | UP | 한줄 요약 |
|---|------|---:|---------|
| 1 | **{제목}** ({기관}) | {upvotes} | {ai_summary를 한국어 1문장으로 요약} |
| 2 | ... | | |
| ... | | | |

**키워드**: {전체 논문에서 추출한 주요 트렌드 키워드 3-5개}
```

**규칙:**
- 한줄 요약은 **한국어**로, ai_summary 또는 summary를 1문장으로 압축
- 기관명이 있으면 제목 옆에 괄호로 표시
- 기본적으로 상위 15개까지 표시. 사용자가 더 요청하면 추가
- upvotes가 0인 논문은 제외
- "최근" 모드에서 두 주차 결과가 합쳐지면 중복 제거 (arxiv ID 기준)

### Step 5: 논문 다운로드 (선택적 — `다운로드`/`download` 인자가 있을 때)

arxiv 논문은 인증 없이 자유롭게 다운로드 가능하다.

**다운로드 URL 패턴:**

| 형식 | URL | 용도 |
|------|-----|------|
| PDF | `https://arxiv.org/pdf/{arxiv_id}` | 원본 논문 다운로드 |
| HTML | `https://arxiv.org/html/{arxiv_id}` | 브라우저 읽기용 (모든 논문에 있지는 않음) |
| Abstract | `https://arxiv.org/abs/{arxiv_id}` | 메타데이터 + 초록 페이지 |

**다운로드 절차:**

1. 작업 디렉토리에 `papers/` 폴더 생성 (없으면)
2. 대상 논문 목록 결정:
   - `다운로드 N` → 리포트 상위 N개
   - `다운로드 all` → 리포트 전체
   - `다운로드` → 기본 상위 5개
3. 각 논문을 Bash `curl`로 다운로드:
   ```bash
   curl -L "https://arxiv.org/pdf/{arxiv_id}" -o "papers/{arxiv_id}.pdf"
   ```
4. 다운로드 완료 후 결과 테이블 출력:
   ```markdown
   ## 다운로드 완료

   | 논문 | 파일 | 크기 |
   |------|------|------|
   | {제목} | papers/{arxiv_id}.pdf | {size} |
   ```

**주의사항:**
- PDF 파일은 수~수십 MB 가능. 대량 다운로드 시 사용자에게 확인
- arxiv에 과도한 요청을 보내지 않도록 다운로드 간 1초 간격 유지
- 다운로드 실패 시 해당 논문 스킵하고 보고

### Step 6: 논문 읽기 (선택적 — `읽기`/`read` 인자가 있을 때)

특정 논문의 내용을 상세 분석한다.

**절차:**

1. 논문이 이미 `papers/{arxiv_id}.pdf`로 다운로드되어 있으면 Read 도구로 PDF 읽기
2. 없으면 HTML 버전을 시도: WebFetch로 `https://arxiv.org/html/{arxiv_id}` 호출
3. HTML도 없으면 PDF 다운로드 후 Read 도구로 읽기
4. 논문 내용을 한국어로 요약:
   - 연구 목적/동기
   - 핵심 방법론
   - 주요 실험 결과
   - 한계점/향후 연구
   - 실용적 시사점

## 에러 핸들링

| 상황 | 대응 |
|------|------|
| API 응답 실패 | 1회 재시도. 실패 시 사용자에게 알림 |
| 빈 응답 | "해당 기간에 트렌딩 논문이 없습니다" 출력 |
| 잘못된 인자 | 인자 형식 안내 후 기본값(1개월)으로 진행할지 확인 |
| PDF 다운로드 실패 | 해당 논문 스킵, 나머지 계속. 실패 목록 보고 |
| HTML 버전 없음 (404) | PDF 다운로드 후 Read 도구로 대체 |
| PDF 용량 과대 (>50MB) | 사용자에게 알리고 다운로드 여부 확인 |

## 사용 예시

```
/paper-trending                          → 이번 달 트렌딩
/paper-trending 이번 주                   → 이번 주 트렌딩
/paper-trending 최근                     → 최근 2주 트렌딩
/paper-trending 2026-03-14               → 특정 날짜
/paper-trending 2026-W11                 → 특정 주차
/paper-trending 2026-03                  → 특정 월
/paper-trending 이번 주 다운로드           → 이번 주 트렌딩 + 상위 5개 PDF 다운로드
/paper-trending 이번 주 다운로드 3         → 이번 주 트렌딩 + 상위 3개 PDF 다운로드
/paper-trending 이번 주 dl all            → 이번 주 트렌딩 + 전체 PDF 다운로드
/paper-trending 읽기 2603.03143           → 특정 논문 상세 분석
```
