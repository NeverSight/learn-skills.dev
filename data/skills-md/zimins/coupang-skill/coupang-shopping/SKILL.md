---
name: coupang-shopping
description: "쿠팡에서 상품 검색, 장바구니, 주문/결제를 CLI로 자동화. 사용 시점 - (1) 사용자가 쿠팡에서 물건 사달라고 할 때, (2) 쿠팡 검색, (3) 쿠팡 장바구니 확인, (4) 쿠팡 주문/결제, (5) 쿠팡, coupang, 물건 사줘, 주문해줘, 장바구니 키워드 언급 시."
---

# coupang-shopping

쿠팡에서 상품 검색, 장바구니 담기, 주문/결제를 자동화하는 스킬.

## Triggers

- 사용자가 쿠팡에서 물건 사달라고 할 때
- "쿠팡", "coupang", "물건 사줘", "주문해줘", "장바구니" 키워드 언급 시
- 쿠팡 검색, 장바구니 확인, 주문/결제 요청 시

## Prerequisites

이 스킬을 사용하려면 `coupang-cli`와 브라우저가 설치되어 있어야 합니다.
**에이전트가 아래 순서대로 Bash로 직접 확인/설치합니다.**

### 1. coupang-cli 설치 확인 및 자동 설치

```bash
# 설치 확인
npx coupang-cli --version 2>/dev/null && echo "CLI_OK" || echo "CLI_NOT_FOUND"
```

`CLI_NOT_FOUND`이면 자동 설치:

```bash
npm install -g coupang-cli
```

### 2. 브라우저 확인 및 자동 설치

기본 브라우저는 **Firefox** (Akamai WAF 우회에 유리).

```bash
# Playwright Firefox 설치 확인 + 없으면 자동 설치
npx playwright install firefox
```

- Chrome 사용 시: `COUPANG_BROWSER=chrome npx coupang-cli ...`
- 보통 Firefox가 권장됨 (Chrome CDP는 봇 감지에 취약)

### 2. 계정 정보 확인 (자동 생성)

`~/.coupang-session/credentials.json` 파일이 있어야 합니다.

**파일이 없으면 에이전트가 직접 템플릿을 생성하고 사용자에게 안내합니다:**

1. `~/.coupang-session/` 디렉토리가 없으면 생성
2. 아래 템플릿으로 `~/.coupang-session/credentials.json` 파일 작성:

```json
{
  "email": "여기에_쿠팡_이메일_입력",
  "password": "여기에_비밀번호_입력",
  "paymentPin": "000000"
}
```

3. 사용자에게 다음과 같이 안내:

> `~/.coupang-session/credentials.json` 파일을 생성했습니다.
> 쿠팡 계정 정보를 입력해주세요:
> - `email`: 쿠팡 로그인 이메일
> - `password`: 쿠팡 비밀번호
> - `paymentPin`: 쿠페이 결제 비밀번호 (6자리)
>
> 파일 위치: `~/.coupang-session/credentials.json`

4. 사용자가 정보를 입력했다고 확인할 때까지 다음 단계로 진행하지 않음

### 3. 로그인

```bash
npx coupang-cli login
```

## Important: 에이전트는 브라우저를 직접 조작하지 않는다

- **모든 쿠팡 작업(검색, 로그인, 장바구니, 주문)은 반드시 CLI 명령(`npx coupang-cli ...`)으로만 실행**
- 에이전트가 직접 네이버/쿠팡 웹사이트를 방문하거나, 브라우저 자동화 도구로 조작하면 안 됨
- 로그인, 네이버 경유 접근 등은 CLI 내부에서 자동으로 처리됨
- 에이전트의 역할은 오직: (1) CLI 명령 실행, (2) 키패드 이미지 판독, (3) 결과 보고

## Instructions

### 실행 방식: 서브에이전트로 백그라운드 실행

**이 스킬의 모든 작업은 Agent 도구를 사용하여 서브에이전트에게 위임합니다.**
메인 대화를 블로킹하지 않고, 서브에이전트가 CLI 실행 + 키패드 판독 + 결과 보고를 자율적으로 처리합니다.

#### 서브에이전트 실행 방법

스킬이 트리거되면, 메인 에이전트는 아래와 같이 Agent 도구를 호출합니다:

```
Agent 도구 호출:
  description: "쿠팡 주문/검색/장바구니"
  run_in_background: true
  prompt: |
    아래 규칙을 반드시 따라 쿠팡 작업을 수행하라.

    ## 규칙
    - 모든 쿠팡 작업은 CLI 명령(`npx coupang-cli ...`)으로만 실행
    - 절대 네이버/쿠팡 웹사이트를 직접 방문하거나 브라우저 도구로 조작하지 않는다
    - 로그인, 네이버 경유 접근은 CLI 내부에서 자동 처리됨

    ## 작업 내용
    [사용자 요청 내용을 여기에 전달]

    ## 주문 시 키패드 처리 절차
    1. `rm -f ~/.coupang-session/keypad-ready ~/.coupang-session/keypad-mapping.json`
    2. CLI를 백그라운드로 실행: `npx coupang-cli order-now "상품명" -p card` (run_in_background: true)
    3. 동시에 키패드 신호 폴링 실행 (run_in_background: true):
       `for i in $(seq 1 180); do if [ -f ~/.coupang-session/keypad-ready ]; then echo "KEYPAD_READY"; exit 0; fi; sleep 1; done; echo "TIMEOUT"`
    4. KEYPAD_READY 감지 시, Read 도구로 10개 스크린샷을 모두 동시에 읽기:
       ~/.coupang-session/screenshots/pad-key-0.png ~ pad-key-9.png
    5. 각 이미지에 표시된 숫자를 시각적으로 판독하여 매핑 JSON 작성
    6. Write 도구로 ~/.coupang-session/keypad-mapping.json 에 저장
       예: {"0":"9","1":"3","2":"2","3":"4","4":"0","5":"8","6":"5","7":"6","8":"1","9":"7"}
    7. 키패드가 2회 이상 나올 수 있음 (충전 PIN + 결제 PIN). 각 키패드마다 4-6 반복
    8. TaskOutput으로 CLI 결과 확인 후 주문 성공/실패 보고
```

#### 서브에이전트 프롬프트 예시

**검색:**
```
npx coupang-cli search "검색어" 를 실행하고 결과를 보고하라.
```

**장바구니 담기:**
```
npx coupang-cli cart-add "상품명" 을 백그라운드로 실행하고 결과를 보고하라.
옵션: -n 2 (2번째 검색 결과 선택)
```

**주문:**
```
npx coupang-cli order-now "상품명" -p card 로 주문을 실행하라.
위의 "주문 시 키패드 처리 절차"를 반드시 따를 것.
```

**장바구니 조회:**
```
npx coupang-cli cart 를 실행하고 결과를 보고하라.
```

### 메인 에이전트의 역할

1. 사용자 요청을 파악 (상품명, 결제수단, 옵션 등)
2. 주문의 경우 사용자에게 상품명/결제수단 확인
3. Agent 도구로 서브에이전트 실행 (`run_in_background: true`)
4. 사용자에게 "실행 중입니다" 안내
5. 서브에이전트 완료 알림 수신 후 결과를 사용자에게 보고

### 네이버 경유 쿠팡 이동 (로그인 포함)

네이버 검색 → 쿠팡 링크 클릭 → 쿠팡 진입 + 로그인까지 CLI가 자동 처리:

```bash
npx coupang-cli navigate
```

- 에이전트가 직접 네이버/쿠팡을 방문할 필요 없음. 이 명령 하나로 해결.

## Options

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `-n, --pick <번호>` | 검색 결과에서 선택할 상품 번호 | 1 |
| `-p, --payment <방식>` | 결제 수단 (`coupay` 또는 `card`) | `coupay` |

## Notes

- **키패드 매핑은 DOM 스크래핑 불가** — 반드시 이미지 판독으로 처리
- CLI 명령은 시간이 걸리므로 반드시 백그라운드로 실행
- macOS 전용 (Chrome/Firefox 설치 필요)
- 기본 브라우저는 Firefox (Akamai WAF 우회). Chrome 사용 시: `COUPANG_BROWSER=chrome`
- `order-now`은 확인 없이 바로 결제하므로, 주문 전 사용자에게 상품명/결제 수단 확인 필수
- 키패드가 2회 이상 나올 수 있음 (충전 PIN + 결제 PIN). 각 키패드마다 Step 4-6 반복 필요
