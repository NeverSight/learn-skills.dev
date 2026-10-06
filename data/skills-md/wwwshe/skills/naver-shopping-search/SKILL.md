---
name: naver-shopping-search
description: 네이버 쇼핑 검색 스킬. 검색은 API sort=sim(또는 최신이면 date); 가격순은 asc/dsc 없이 수신 목록을 에이전트가 정렬. "네이버페이만" 등 필터·후처리 지원.
argument-hint: "[검색키워드] [정렬?] [건수?] [필터?]"
---

# 네이버 쇼핑 검색

사용자가 네이버 쇼핑 상품 검색을 요청하면 [쇼핑 검색 API](https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md)를 호출해 결과를 보여준다. **웹 스크래핑은 하지 않는다.**

## 사전 준비: 클라이언트 ID·시크릿 확인

아래 순서로 자격 증명을 확인한다:

1. 환경변수 `NAVER_CLIENT_ID`, `NAVER_CLIENT_SECRET` 확인
2. 없으면 사용자에게 요청:

```
네이버 쇼핑 검색 API는 클라이언트 ID·시크릿이 필요합니다.

1. https://developers.naver.com/apps 에서 애플리케이션 등록
2. "API 설정"에서 **검색** 사용을 켠다 (쇼핑 검색 포함)
3. 발급된 Client ID / Client Secret을 아래 중 하나로 설정해 주세요.

[방법 A] Claude Code — ~/.claude/settings.json (권장)
  "env": {
    "NAVER_CLIENT_ID": "발급_ID",
    "NAVER_CLIENT_SECRET": "발급_Secret"
  }
  → 저장 후 Claude Code를 재시작합니다.

[방법 B] Cursor — 통합 터미널에 환경변수 넣기
  사용자 settings.json에 추가합니다. (macOS 경로 예: ~/Library/Application Support/Cursor/User/settings.json)
  OS에 맞는 키만 사용: macOS → terminal.integrated.env.osx, Windows → terminal.integrated.env.windows, Linux → terminal.integrated.env.linux

  {
    "terminal.integrated.env.osx": {
      "NAVER_CLIENT_ID": "발급_ID",
      "NAVER_CLIENT_SECRET": "발급_Secret"
    }
  }

  → Cursor를 재시작한 뒤 **새 터미널**을 열어야 적용됩니다. (에이전트 Shell이 이 터미널 환경을 쓰는 경우가 많음)

[방법 C] 에이전트 셸에만 맞추기 — ~/.zshenv 또는 ~/.zshrc
  에이전트가 Cursor `terminal.integrated.env`를 물려받지 않는 경우, **로그인/비대화형 zsh**이 읽는 파일에 `export`를 넣는 방식이 필요할 수 있습니다.

  export NAVER_CLIENT_ID='발급_ID'
  export NAVER_CLIENT_SECRET='발급_Secret'

  - 비대화형에도 항상 넣고 싶으면 ~/.zshenv 권장(다른 도구와 충돌 없는지 확인).
  - 로그인 셸 위주면 ~/.zshrc 또는 ~/.zprofile 등이 읽힐 수 있음. **에이전트가 어떤 셸·어떤 rc를 읽는지에 따라 달라지므로**, 설정 후 에이전트 Shell에서 반드시 확인:

  echo ${#NAVER_CLIENT_ID}

  0이 아니면(길이가 있으면) 변수가 잡힌 것입니다. (값 자체는 로그에 남기지 말 것.)

[방법 D] 대화 중 직접 전달
  "ID는 xxx, 시크릿은 yyy" 처럼 알려주시면 해당 대화에서만 사용합니다.
```

> 네이버 검색 API 일일 호출 한도·이용 약관은 [공식 문서·공지](https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md)를 따른다.

## 입력 파싱

`$ARGUMENTS` 또는 사용자 메시지에서 추출:

| 항목 | 예시 | 기본값 |
|------|------|--------|
| 검색어 | 노트북, 아이폰 케이스 | (필수) |
| 정렬 | 정확도·최신(→API `sim`/`date`), 가격순(→API는 `sim` 또는 `date`만, 순서는 클라이언트) | API `sim` |
| 표시 건수 | 5, 10, 20 | `10` (최대 100) |
| 시작 위치 | 2페이지 등 | `start=1` (`start` 최대 1000) |
| 필터 | 네이버페이만, 중고/렌탈/직구 제외 | 없음 |

### 공식 API가 제공하는 정렬·쿼리 ([문서](https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md))

| 파라미터 | 값 | 의미 |
|----------|-----|------|
| `sort` | `sim` | 정확도순(기본) |
| `sort` | `date` | 날짜순 내림차순(문서 표현; 사용자에게는 "최신순"에 가깝게 안내 가능) |
| `sort` | `asc` / `dsc` | 문서상 가격 오름/내림차순이나, **이 스킬에서는 사용하지 않는다** (아래「가격순」참고). |
| `filter` | `naverpay` | 네이버페이 연동 상품만 |
| `exclude` | `used` / `rental` / `cbshop` | 중고 / 렌탈 / 해외직구·구매대행 제외 (`used:rental`처럼 `:`로 연결) |

### 이 스킬에서 API에 넣는 `sort`

- **`sim` 또는 `date`만** 사용한다. (`asc` / `dsc`는 호출에 넣지 않는다.)
- 사용자가 **가격 낮은 순·높은 순**을 원하면: API는 **`sim`으로 조회**(또는 이미 최신순이면 `date` 유지)한 뒤, **에이전트가 `items`를 `lprice` 기준으로 정렬**해 표시한다.

### API로 할 수 없는 요청 (솔직히 안내)

- **평점 높은 순·리뷰 많은 순** 등: `sort`에 평점 값이 없고 응답에도 **평점·리뷰 수**가 없다. 불가 이유를 밝히고, **정확도·최신(API)** 또는 **가격 표시 순(클라이언트 정렬)** 중에서 고르도록 제안한다.

### 정렬 — 자연어 매핑 (API + 표시)

| 사용자 표현 | API `sort` | 표시(후처리) |
|------------|------------|----------------|
| 정확도순, 관련순, 그냥 검색(기본) | `sim` | 받은 순서 그대로 |
| 날짜순, 최신순, 최근에 올라온 순 | `date` | 받은 순서 그대로 |
| 가격 낮은 순, 싼 순, 저렴한 순 | `sim`(기본) 또는 사용자가 최신을 고른 상태면 `date` | `items`를 `lprice` **오름차순**으로 정렬 |
| 가격 높은 순, 비싼 순 | 위와 동일 | `lprice` **내림차순**으로 정렬 |

가격순을 쓸 때는 `display`를 필요한 만큼 크게(최대 100) 잡는 것이 좋다. **정렬 대상은 항상 그 요청으로 받은 `items`뿐**임을 사용자에게 짧게 알릴 수 있다.

### 필터 — 자연어 매핑

- "네이버페이만" / "네이버페이 되는 것만" → `filter=naverpay`
- "중고 빼고" → `exclude`에 `used`
- "렌탈 빼고" → `exclude`에 `rental`
- "해외직구 빼고" / "구매대행 빼고" → `exclude`에 `cbshop`
- 여러 개 → `exclude=used:cbshop` 형식

## 사용자와 조건 맞추기 (질문 ↔ 답변)

**가능하다.** `filter` / `exclude` / API `sort`(sim·date)는 쿼리로 반영하고, 가격순은 **후처리 정렬**로 반영한다.

### 언제 질문할지

- 검색어와 **정렬·필터가 한 문장에 모두** 있으면 질문 없이 바로 호출한다.  
  예: "무선 이어폰 가격 낮은 순"(→`sim` 조회 후 `lprice` 오름차순), "노트북 최신순으로 20개", "케이블 중고랑 직구 제외"
- **검색어만** 있거나("키보드 찾아줘"), 정렬이 애매하면:
  - **기본 전략**: `sort=sim`, 필터 없이 **먼저 검색**하고, 결과 아래에 정렬·필터 바꿔 재검색할 수 있다고 짧게 안내한다.
  - **대화형을 원할 때만** 아래 블록처럼 **한 번** 질문한다. (평점순 옵션은 넣지 않고, 원하면 평점은 API 불가라고 안내.)

### 질문 예시 (복붙용)

```
네이버 쇼핑에서 어떤 순서로 볼까요?

1) 정확도순(기본, API sim)  2) 최신순(API date)  3) 가격 낮은 순(sim 조회 후 목록 정렬)  4) 가격 높은 순(sim 조회 후 목록 정렬)

추가로 원하면 같이 말해 주세요:
- 네이버페이 연동만
- 중고 / 렌탈 / 해외직구·구매대행 제외

번호(예: 3)나 자연어(예: "가격 싼 순")로 답해 주세요.
(참고: 평점순 정렬은 이 Open API에서 지원하지 않습니다.)
```

### 답변 파싱

- `1` `①` `정확도` → API `sort=sim`, 가격 후처리 없음
- `2` `최신` `날짜` → API `sort=date`, 가격 후처리 없음
- `3` `싼` `저렴` `낮은` → API `sort=sim`(또는 직전이 최신이면 `date` 유지), 응답 `items`를 **`lprice` 오름차순**으로 정렬해 출력
- `4` `비싼` `높은` 가격 → 위와 동일하게 API는 `sim`/`date`만 쓰고, **`lprice` 내림차순**으로 정렬해 출력
- 이전에 말한 **검색어는 유지**하고, 답만 바뀌었으면 **필요 시** 같은 검색어로 `curl`을 다시 호출하되 **`sort`에는 절대 `asc`/`dsc`를 넣지 않는다.** 이미 같은 검색의 JSON이 맥락에 있으면 **재호출 없이** `jq`로 정렬만 바꿔도 된다.

## API 호출

**Bash tool + curl + jq 로 호출한다.**

한글·공백 검색어는 반드시 `--data-urlencode`로 전달한다. API `sort`에는 **`sim` 또는 `date`만** 넣는다. `filter`, `exclude`는 위에서 파싱한 값으로 치환한다. `exclude`가 여러 개면 **한 파라미터**에 `used:rental` 형태로 넣는다.

### 기본 호출

```bash
curl -s -G "https://openapi.naver.com/v1/search/shop.json" \
  --data-urlencode "query={검색어}" \
  --data-urlencode "display={표시건수}" \
  --data-urlencode "start={시작위치}" \
  --data-urlencode "sort={sim|date}" \
  -H "X-Naver-Client-Id: ${NAVER_CLIENT_ID}" \
  -H "X-Naver-Client-Secret: ${NAVER_CLIENT_SECRET}" \
  | jq '{
    lastBuildDate,
    total: .total,
    start: .start,
    display: .display,
    items: [.items[]? | {
      title: (.title | gsub("<[^>]*>"; "")),
      link,
      image,
      lprice,
      hprice,
      mallName,
      productId,
      brand,
      maker,
      category1,
      category2,
      category3,
      category4
    }]
  }'
```

`filter` / `exclude`가 필요하면 같은 방식으로 `--data-urlencode`로 추가한다.

### 가격순 표시 (`asc` / `dsc` API 미사용)

`curl`으로 받은 객체의 `items` 배열에 대해 **에이전트가 `jq`로 정렬**한다. `title`의 HTML 태그는 정렬 전에 제거해 두는 편이 안전하다.

- **가격 낮은 순**: `sort_by(.lprice | tonumber)` — `tonumber` 실패 행은 `select`로 빼거나 `try/catch`로 끝으로 보낼 정책을 정한다.
- **가격 높은 순**: `sort_by(.lprice | tonumber) | reverse`

예시(추출 필드 유지한 채 낮은 가격순):

```bash
curl -s -G "https://openapi.naver.com/v1/search/shop.json" ... \
  | jq '.items |= (map(.title |= gsub("<[^>]*>"; "")) | sort_by(.lprice | tonumber)) | {
      lastBuildDate, total, start, display,
      items: [.items[] | {title, link, image, lprice, hprice, mallName, productId, brand, maker, category1, category2, category3, category4}]
    }'
```

출력 상단에 `API 정렬: sim(또는 date) · 표시 순서: 가격 낮은 순(클라이언트)`처럼 **구분해서** 적는다.

### 오류 처리

- HTTP 401 / 403: Client ID·Secret 오류 또는 개발자센터에서 검색 API 미사용
- `errorMessage` 필드가 있으면 그 내용을 사용자에게 그대로 요약한다
- `total`이 0이면 "검색 결과 없음" 안내

## 검색 결과 후처리 (에이전트 필터)

**가능하다.** API로 받은 JSON의 `items[]`에 대해, **에이전트가 jq 등으로 조건을 걸어** 목록을 줄인 뒤 사용자에게 보여준다. (재호출 없이 한 번에 처리하거나, 조건이 복잡하면 `curl` 결과를 변수·파이프로 넘겨 두 단계 `jq`를 써도 된다.)

### 할 수 있는 예 (응답 필드에 의존)

| 사용자 요청 예 | 후처리 아이디어 |
|----------------|-----------------|
| N원 이하/이상만 | `lprice`를 숫자로 보고 `select` (없거나 0이면 규칙 정하기) |
| 특정 브랜드·제조사만 | `brand`, `maker` 문자열 포함/일치 |
| 제목에 단어 포함 | `title`에서 HTML 제거 후 `test` |
| 특정 몰 제외·만 | `mallName` |
| 카테고리 안에서만 | `category1`~`category4` 중 하나에 키워드 포함 |
| 상품 타입(중고 등) | [문서의 `productType`](https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md#상품군-타입) 코드로 `select` (API `exclude`와 겹치면 API를 우선해도 됨) |
| 가격 낮은/높은 순(표시만) | API `asc`/`dsc` 없이 `items`를 `lprice` 기준 jq 정렬(위「가격순 표시」절) |

`productType` 등은 기본 `jq` 추출 블록에 없으면 후처리용으로 **원본 `items`에서 필드를 추가**해 쓴다.

### jq 예시 (가격 상한 + 브랜드 포함)

`curl` 응답에 이어 붙이거나, `.items`만 떼어 두 번째 `jq`로 처리한다:

```bash
curl -s -G "https://openapi.naver.com/v1/search/shop.json" ... \
  | jq '
    .items
    | map(.title |= gsub("<[^>]*>"; ""))
    | map(select((.lprice | try tonumber catch 0) <= 50000))
    | map(select((.brand // "") | test("삼성"; "i")))
  '
```

`lprice`는 문자열로 올 수 있어 `tonumber`를 쓴다. 변환 실패 시 `catch 0` 등으로 정책을 정한다.

### 꼭 짚을 한계

1. **이번에 받은 페이지 안에서만** 걸러지거나 정렬된다. API `display`는 최대 100이므로, "전체 검색 10만 건 중 최저가" 같은 **전역 순위**는 이 방식만으로는 보장할 수 없다. 필요하면 `start`를 바꿔 **여러 번 호출해 `items`를 합친 뒤** 클라이언트에서 정렬·필터하거나, `display`를 100으로 맞추는 등 **데이터를 더 모은 뒤** 같은 방식으로 처리한다. (**API `asc`/`dsc`는 쓰지 않는다.**)
2. **평점·리뷰 수**는 응답에 없으면 후처리로도 불가능하다.

### 출력 시

- 결과 상단에 **"API 정렬/필터"**와 별도로 **"표시 목록에 적용한 조건"**을 한 줄 적는다.  
  예: `표시: 수신 {display}건 중, 가격 5만 원 이하 · 브랜드 'OO' 포함만 표시`

## 결과 출력 형식

```
## "{검색어}" 네이버 쇼핑 검색

전체 약 {total}건 · 표시 {display}건 · API 정렬: {sim 또는 date} · 표시 순서: {정확도/최신 그대로 또는 가격 낮은/높은 순(클라이언트)} · 출처: 네이버 쇼핑 검색 API

---

### 1. {제목(HTML 제거)}

![{제목 짧게, alt용}]({image})

- 최저가: {lprice}원 (최고가 hprice가 의미 있으면 함께 표기)
- 판매처: {mallName}
- 브랜드/제조사: {brand} / {maker} (없으면 생략)
- 분류: {category1} > {category2} > … (있는 만큼)
- 상품: [바로가기]({link})

---

### 2. ...
```

### 썸네일(상품 이미지)

- API `image` 필드는 **썸네일 URL**이다. 채팅/마크다운 UI에서 보이게 하려면 **표준 이미지 문법**을 쓴다: `![대체텍스트](이미지URL)`
- `image`가 비어 있거나 잘못된 경우 해당 줄은 생략한다.
- `alt`에는 제목 일부(특수문자·`]` 이스케이프)를 넣어 접근성을 맞춘다.
- 사용자가 **"썸네일 빼고"** "텍스트만"이라고 하면 이미지 줄 없이 링크·가격만 출력한다.
- 한 화면에 이미지가 너무 많으면(예: 20건 전부) 렌더링이 무거울 수 있으니, 사용자가 건수를 크게 요청했을 때는 **상위 N개만 이미지**·나머지는 링크만 같은 식으로 조절해도 된다.

- `title`에 남은 HTML 엔티티는 필요 시 짧게 정리한다
- 최대 표시 건수는 API `display` 상한(100) 이내로 맞춘다
- 가격은 천 단위 구분 없이 숫자만 나와도 되고, 보기 좋게 콤마를 넣어도 된다

## 결과 제공 후 추가 제안

```
더 찾아볼까요?
- 최신순 → API `sort=date`로 다시 검색
- 가격순 → API는 `sim`(또는 유지)로 두고 **목록만 `lprice`로 정렬** (`asc`/`dsc` 쿼리는 쓰지 않음)
- 방금 목록만 좁히기 → "5만 원 이하만 보여줘" / "삼성만" (같은 JSON에 `jq` 후처리)
- 다음 페이지 → "다음 페이지" (start = 이전 start + display)
- 네이버페이만 → "네이버페이 연동 상품만"
- 중고·렌탈·해외직구 제외 → "중고랑 직구 빼고 검색해줘"
- 평점순은 이 API에서 불가 → 정렬·필터 중에서 다시 선택
- 썸네일 끄기 → "썸네일 빼고 보여줘" (이미지 줄 생략)
```

## 주의

- API 응답의 `link`·이미지 URL은 네이버 정책에 따른 것이므로 **재가공·재판매용 DB 적재** 등은 [이용약관](https://developers.naver.com/products/terms/)을 확인한다.
- 키를 스킬 파일이나 로그에 하드코딩하지 않는다.
