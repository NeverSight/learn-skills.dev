---
name: my-fetch-tweet
description: X/Twitter URL을 받으면 트윗 원문을 가져와서 요약-인사이트-전체 번역을 제공하는 스킬. "트윗 번역", "트윗 가져와", "X 게시글" 요청에 사용.
triggers:
  - "트윗 번역"
  - "트윗 가져와"
  - "X 게시글"
---

# my-fetch-tweet

X/Twitter 트윗을 가져와서 요약·인사이트·전체 번역을 제공하는 스킬.

## API 연동 방법

### 지원 URL 형식

| 입력 URL | 변환 후 |
|----------|---------|
| `https://x.com/{screen_name}/status/{id}` | `https://api.fxtwitter.com/{screen_name}/status/{id}` |
| `https://twitter.com/{screen_name}/status/{id}` | `https://api.fxtwitter.com/{screen_name}/status/{id}` |
| `https://fxtwitter.com/{screen_name}/status/{id}` | 도메인만 `api.fxtwitter.com`으로 교체 |
| `https://fixupx.com/{screen_name}/status/{id}` | 도메인만 `api.fxtwitter.com`으로 교체 |

### 변환 규칙

1. URL에서 `screen_name`과 `status_id` 추출
2. 도메인을 `api.fxtwitter.com`으로 교체
3. WebFetch로 JSON 데이터 호출

```
변환 예시:
https://x.com/garrytan/status/1234567890
→ https://api.fxtwitter.com/garrytan/status/1234567890
```

### 응답 JSON 주요 필드

| 필드 | 설명 |
|------|------|
| `tweet.text` | 트윗 본문 전체 |
| `tweet.author.name` | 작성자 이름 |
| `tweet.author.screen_name` | 작성자 @핸들 |
| `tweet.likes` | 좋아요 수 |
| `tweet.retweets` | 리트윗 수 |
| `tweet.views` | 조회수 |
| `tweet.quote` | 인용 트윗 (있는 경우) |

## 번역 파이프라인

트윗 데이터를 가져온 뒤 아래 3단계 순서로 제공한다.
전체 번역을 바로 보여주지 않고 단계적으로 제공하여 핵심 파악 → 의미 이해 → 전문 독해 순서를 따른다.

### 1단계: 요약 (3-5문장)

- 트윗의 핵심 주장을 한국어로 요약
- 작성자 정보(@핸들, 이름) 포함
- 인게이지먼트 수치 포함 (좋아요 N / 리트윗 N / 조회 N)
- 스레드 트윗이면 전체 흐름을 한 문단으로 압축

### 2단계: 인사이트 (3개)

- **핵심 메시지**: 이 트윗이 정말 말하고 싶은 것
- **시사점**: 업계/트렌드에서의 의미, 왜 지금 이 말을 하는지
- **적용점**: 나(독자)에게 어떤 의미인지, 어떻게 활용할 수 있는지

### 3단계: 전체 번역

- 원문 전체를 자연스러운 한국어로 번역
- 인용 트윗이 있으면 함께 번역 (들여쓰기로 구분)
- 전문 용어는 원문 병기 (예: "에이전트(Agent)", "프롬프트(Prompt)")
- 줄바꿈·이모지·링크 등 원문 서식 유지

## WebFetch Fallback

스크립트 실행이 어려울 때 WebFetch 도구로 직접 API를 호출한다.

### 사용 방법

1. 입력 URL에서 `screen_name`과 `status_id` 추출
2. 아래 형식으로 WebFetch 호출:

```
URL: https://api.fxtwitter.com/{screen_name}/status/{status_id}
Prompt: "Extract the full tweet text, author name, and engagement metrics"
```

### 예시

```
입력: https://x.com/garrytan/status/1234567890
WebFetch URL: https://api.fxtwitter.com/garrytan/status/1234567890
```

응답에서 `tweet.text`, `tweet.author`, `tweet.likes`, `tweet.retweets`, `tweet.views` 값을 추출하여 번역 파이프라인(요약 → 인사이트 → 전체 번역)에 사용한다.
