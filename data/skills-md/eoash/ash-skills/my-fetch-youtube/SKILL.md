---
name: my-fetch-youtube
description: YouTube URL을 받으면 자막을 추출하고, Web Search로 자동자막 오류를 보정한 뒤, 요약-인사이트-전체 번역을 제공하는 스킬. "유튜브 번역", "영상 정리", "YouTube 요약" 요청에 사용.
triggers:
  - "유튜브 번역"
  - "영상 정리"
  - "YouTube 요약"
---

# my-fetch-youtube

YouTube 영상의 자막을 추출하고, Web Search로 자동자막 오류를 보정한 뒤 요약·인사이트·전체 번역을 제공하는 스킬.

> **환경 참고**: 이 환경에서 yt-dlp는 `python -m yt_dlp` 명령어로 실행한다.

## 자막 추출 및 정제

### 1. 자막 추출 명령어

```bash
python -m yt_dlp --write-auto-sub --sub-lang "ko,en" --skip-download \
  --convert-subs vtt -o "%(title)s" "{URL}"
```

- `--write-auto-sub`: 자동 생성 자막 포함
- `--sub-lang "ko,en"`: 한국어 우선, 영어 차선
- `--skip-download`: 영상 파일 다운로드 안 함
- `--convert-subs vtt`: VTT 형식으로 변환

### 2. VTT → 순수 텍스트 정제

추출된 `.vtt` 파일에서 타임스탬프·태그·번호를 제거하여 순수 텍스트로 만든다:

```bash
cat "파일명.vtt" \
  | sed -E 's/^[0-9]+$//' \
  | sed -E 's/[0-9]{2}:[0-9]{2}:[0-9]{2}.*//g' \
  | sed -E 's/<[^>]+>//g' \
  | tr -s '\n' \
  | grep -v '^$'
```

각 단계:
1. `^[0-9]+$` 제거 → 줄 번호 삭제
2. `HH:MM:SS...` 제거 → 타임스탬프 삭제
3. `<태그>` 제거 → 웹 형식 표시 삭제
4. `tr -s '\n'` → 연속 빈 줄 정리
5. `grep -v '^$'` → 빈 줄 제거

### 3. 자막 언어 우선순위

```
한국어 수동 자막 (ko)
  → 없으면 영어 수동 자막 (en)
  → 없으면 한국어 자동 자막 (ko-auto)
  → 없으면 영어 자동 자막 (en-auto)
```

### 4. 자막 없는 경우

사용 가능한 자막이 없으면:
> "이 영상에는 자막이 없습니다. 자막이 있는 다른 영상을 선택해주세요."

## 메타데이터 추출

### 명령어

```bash
python -m yt_dlp --dump-json --no-download "{URL}"
```

JSON 전체를 출력한다. 영상을 다운로드하지 않고 메타데이터만 가져온다.

### 추출할 주요 필드

| 필드 | 설명 | 활용 |
|------|------|------|
| `title` | 영상 제목 | Web Search 보정 키워드 소스 |
| `description` | 영상 설명 | 고유명사/전문 용어 추출 소스 |
| `channel` | 채널명 | 출처 표시 |
| `duration` | 길이 (초) | 10분 이상이면 Task Agent 사용 판단 |
| `chapters` | 챕터 목록 (있으면) | 번역 시 섹션 구분에 활용 |

### 활용 방법

1. `title` + `description`에서 고유명사·전문 용어를 추출 → Step 4 Web Search 보정에 사용
2. `duration`이 600초(10분) 초과이면 → Task Agent 사용 권장
3. `chapters`가 있으면 → 번역 결과를 챕터별로 구분하여 출력

## Web Search 보정

YouTube 자동 자막은 AI 음성 인식이라 고유명사·전문 용어를 틀리게 인식할 수 있다.
제목·설명의 키워드로 웹 검색하여 올바른 표기를 확인하고 자막을 보정한다.

### Step 1: 키워드 추출 (5-10개)

`title`과 `description`에서 아래 유형의 단어를 추출한다:

- 사람 이름 (발표자, 인터뷰이 등)
- 회사명·제품명·서비스명
- 전문 용어·약어
- 고유명사 (프로젝트명, 논문 제목 등)

### Step 2: WebSearch 병렬 실행

추출한 키워드로 동시에 웹 검색한다:

```
검색 쿼리 예시:
- "{사람 이름} {회사명}"
- "{전문 용어} 정확한 표기"
- "{약어} full name"
- "{제품명} official"
```

### Step 3: 자막 보정 + 내역 기록

검색 결과를 바탕으로 자막 텍스트의 오류를 수정하고, 보정 내역을 기록한다.

**보정 전/후 예시:**

| 보정 전 (자동 자막 오류) | 보정 후 (올바른 표기) |
|--------------------------|----------------------|
| Cloud | Claude |
| 앤트로피 | Anthropic |
| GPT four | GPT-4 |
| 오픈 에이아이 | OpenAI |
| rag | RAG (Retrieval-Augmented Generation) |
| lang chain | LangChain |

**보정 내역 출력 형식:**
```
[Web Search 보정 내역]
- "Cloud" → "Claude" (검색 확인: Anthropic Claude AI)
- "앤트로피" → "Anthropic" (검색 확인: anthropic.com)
총 N개 항목 보정
```

## 번역 파이프라인

자막 추출 + Web Search 보정이 완료된 뒤 아래 3단계 순서로 제공한다.

> **긴 영상 (10분 이상, duration > 600초)**: 자막 텍스트가 방대하므로 Task Agent로 처리한다.
> ```
> Task(description="YouTube 번역", prompt="자막 전체를 읽고 요약-인사이트-아티클로 번역하라")
> ```

### 1단계: 요약 (3-5문장)

- 영상 전체 내용을 한국어로 요약
- 채널명, 영상 제목, 길이 포함
- 핵심 주제와 결론을 중심으로 압축

### 2단계: 인사이트 (3개)

- **핵심 메시지**: 이 영상이 정말 말하고 싶은 것
- **시사점**: 업계/트렌드에서의 의미, 왜 지금 이 내용인지
- **적용점**: 나(시청자)에게 어떤 의미인지, 어떻게 활용할 수 있는지

### 3단계: 전체 번역된 아티클

- 자막 전체를 읽기 쉬운 **아티클 형태**로 번역 (받아쓰기 X, 자연스러운 문장으로)
- 챕터가 있으면 챕터별로 섹션 구분 (`## 챕터명`)
- Web Search 보정된 올바른 용어 사용
- 전문 용어는 원문 병기 (예: "검색 증강 생성(RAG, Retrieval-Augmented Generation)")
