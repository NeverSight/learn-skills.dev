---
name: k-skill-korean-ai-tools
description: AI 에이전트를 위한 한국 서비스 자동화 스킬 모음 — SRT/KTX 예매, KBO, 로또, 카카오톡, 지하철, HWP, 우편번호 등
triggers:
  - SRT 기차표 예매해줘
  - KBO 경기 결과 알려줘
  - 로또 당첨번호 확인해줘
  - 카카오톡 메시지 보내줘
  - 서울 지하철 도착정보 조회해줘
  - HWP 파일 변환해줘
  - 우편번호 검색해줘
  - 한국 서비스 자동화 스킬 설치해줘
---

# k-skill

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

한국인을 위한 AI 에이전트 스킬 모음집. Claude Code, Codex, Cursor 등 코딩 에이전트에서 SRT 예매, KBO 조회, 로또 확인, 카카오톡 전송, 서울 지하철 도착정보, HWP 변환, 우편번호 검색 등을 자동화할 수 있습니다.

---

## 설치

### 전체 스킬 설치 (권장)

```bash
# npx로 전체 스킬 설치
npx k-skill install

# 또는 전역 설치
npm install -g k-skill
k-skill install
```

### 선택 설치

```bash
# SRT만 설치
npx k-skill install srt

# KBO + 로또만 설치
npx k-skill install kbo lotto
```

### 설치 후 초기 설정

```bash
# k-skill-setup 스킬 실행 (sops+age 설정, secrets 파일 생성, 런타임 확인)
k-skill-setup
```

초기 설정 순서:
1. `k-skill install` 실행
2. `k-skill-setup` 실행 → `sops + age` 키 생성, 공통 secrets 파일 초기화
3. secrets 값 로컬에 안전하게 등록 (채팅창에 붙여넣기 금지)
4. 각 기능별 문서 확인

---

## 보안 및 시크릿 관리

**절대 금지:**
- 채팅 메시지에 비밀번호/API 키 직접 입력
- `.env` 파일을 git에 커밋
- 코드 내 하드코딩

**표준 환경변수 이름:**

```bash
# SRT
export SRT_USERNAME="your_id"
export SRT_PASSWORD="your_password"

# KTX/Korail
export KORAIL_USERNAME="your_id"
export KORAIL_PASSWORD="your_password"

# 서울 지하철 (공공데이터포털 API 키)
export SEOUL_METRO_API_KEY="your_api_key"
```

**sops + age로 암호화 저장 (권장):**

```bash
# age 키 생성
age-keygen -o ~/.config/sops/age/keys.txt

# secrets 파일 암호화
sops --age $(cat ~/.config/sops/age/keys.txt | grep "public key" | awk '{print $4}') \
  --encrypt secrets.yaml > secrets.enc.yaml

# 복호화하여 환경변수 주입
sops --decrypt secrets.enc.yaml | k-skill env inject
```

---

## 기능별 사용법

### 1. SRT 예매

열차 조회, 예약, 예약 확인, 취소를 지원합니다.

```javascript
const { SRTClient } = require('k-skill/srt');

const client = new SRTClient({
  username: process.env.SRT_USERNAME,
  password: process.env.SRT_PASSWORD,
});

// 로그인
await client.login();

// 열차 조회
const trains = await client.searchTrains({
  departure: '수서',
  arrival: '부산',
  date: '20260401',   // YYYYMMDD
  time: '080000',     // HHmmss
  passengers: 1,
});

console.log(trains);
// [{ trainNo: 'SRT123', departTime: '08:00', arrivalTime: '10:30', price: 59800, seats: 'available' }, ...]

// 예약
const reservation = await client.reserve({
  trainNo: trains[0].trainNo,
  passengers: 1,
  seatType: 'normal', // 'normal' | 'window' | 'aisle'
});

console.log(reservation.reservationId);

// 예약 확인
const myReservations = await client.getReservations();
console.log(myReservations);

// 예약 취소
await client.cancelReservation(reservation.reservationId);
```

**에이전트 프롬프트 예시:**
```
"4월 1일 수서→부산 SRT 08시 이후 첫 열차 창가석으로 예약해줘"
```

---

### 2. KTX 예매

> ⚠️ 현재 작동하지 않습니다. 향후 지원 예정.

```javascript
const { KTXClient } = require('k-skill/ktx');
// KTX/Korail 열차 조회, 예약, 예약 확인, 취소 지원 목표
// 현재 개발 중 — 사용 불가
```

---

### 3. 카카오톡 Mac CLI

macOS에서 `kakaocli`를 사용한 대화 조회, 검색, 메시지 전송. 인증 불필요.

```javascript
const { KakaoTalkMac } = require('k-skill/kakaotalk-mac');

const kakao = new KakaoTalkMac();

// 대화 목록 조회
const conversations = await kakao.listConversations();
console.log(conversations);
// [{ name: '홍길동', lastMessage: '안녕', unread: 2 }, ...]

// 특정 대화 검색
const results = await kakao.searchConversations('개발팀');

// 테스트 전송 (실제 전송 전 확인)
const preview = await kakao.previewSend({
  to: '홍길동',
  message: '안녕하세요!',
});
console.log(preview); // { to: '홍길동', message: '안녕하세요!', confirmed: false }

// 실제 전송 (사용자 확인 후)
await kakao.send({
  to: '홍길동',
  message: '안녕하세요!',
  confirmed: true, // 반드시 사용자 동의 후 true
});
```

> **중요:** 에이전트는 사용자가 명시적으로 확인한 경우에만 `confirmed: true`로 실제 전송합니다.

**CLI 직접 사용:**

```bash
# 대화 목록
kakaocli list

# 메시지 전송
kakaocli send --to "홍길동" --message "테스트 메시지"

# 대화 내용 조회
kakaocli read --name "홍길동" --count 20
```

---

### 4. 서울 지하철 도착정보 조회

공공데이터포털 API 키 필요.

```javascript
const { SeoulSubway } = require('k-skill/seoul-subway');

const subway = new SeoulSubway({
  apiKey: process.env.SEOUL_METRO_API_KEY,
});

// 역 이름으로 실시간 도착정보 조회
const arrivals = await subway.getArrivals('강남');

console.log(arrivals);
/*
[
  {
    line: '2호선',
    station: '강남',
    direction: '성수방면',
    nextTrain: '1분 후',
    followingTrain: '5분 후',
    trainNo: '2234'
  },
  ...
]
*/

// 특정 노선 필터링
const line2 = await subway.getArrivals('강남', { line: '2호선' });

// 역 코드로 조회
const byCode = await subway.getArrivalsByCode('0222');
```

**에이전트 프롬프트 예시:**
```
"지금 강남역 2호선 외선순환 다음 열차 언제 와?"
```

---

### 5. KBO 경기 결과 조회

인증 불필요.

```javascript
const { KBOClient } = require('k-skill/kbo');

const kbo = new KBOClient();

// 오늘 경기 일정/결과
const today = await kbo.getGames();
console.log(today);

// 특정 날짜
const games = await kbo.getGames({ date: '20260401' }); // YYYYMMDD

// 팀별 필터링
const lgGames = await kbo.getGames({
  date: '20260401',
  team: 'LG',
});

console.log(lgGames);
/*
[
  {
    homeTeam: 'LG',
    awayTeam: 'KIA',
    homeScore: 5,
    awayScore: 3,
    status: 'final',   // 'scheduled' | 'live' | 'final'
    stadium: '잠실',
    startTime: '18:30'
  }
]
*/

// 팀 목록
const teams = kbo.getTeamList();
// ['LG', 'KIA', 'SSG', 'NC', 'KT', '두산', '한화', '롯데', '삼성', '키움']
```

---

### 6. 로또 당첨 확인

인증 불필요.

```javascript
const { LottoClient } = require('k-skill/lotto');

const lotto = new LottoClient();

// 최신 회차 당첨번호
const latest = await lotto.getLatestResult();
console.log(latest);
/*
{
  round: 1162,
  date: '2026-03-28',
  numbers: [3, 14, 22, 31, 40, 43],
  bonusNumber: 7,
  prizes: {
    first: { winners: 12, amount: 2500000000 },
    ...
  }
}
*/

// 특정 회차
const specific = await lotto.getResult(1100);

// 내 번호 대조
const myNumbers = [3, 14, 22, 31, 40, 43];
const check = await lotto.checkNumbers(myNumbers);

console.log(check);
/*
{
  round: 1162,
  myNumbers: [3, 14, 22, 31, 40, 43],
  matched: [3, 14, 22, 31, 40, 43],
  bonusMatched: false,
  rank: 1,  // 1~5등 또는 null
  prize: 2500000000
}
*/
```

---

### 7. HWP 문서 처리

`.hwp` 파일을 JSON/Markdown/HTML로 변환, 이미지 추출, 배치 처리 지원. 인증 불필요.

```javascript
const { HWPProcessor } = require('k-skill/hwp');

const hwp = new HWPProcessor();

// HWP → Markdown 변환
const markdown = await hwp.toMarkdown('./document.hwp');
console.log(markdown);

// HWP → JSON 변환
const json = await hwp.toJSON('./document.hwp');
console.log(json.paragraphs);

// HWP → HTML 변환
const html = await hwp.toHTML('./document.hwp');

// 이미지 추출
const images = await hwp.extractImages('./document.hwp', {
  outputDir: './extracted-images',
});
console.log(images); // ['./extracted-images/image_001.png', ...]

// 배치 처리 (디렉토리 내 전체 HWP 파일)
const results = await hwp.batchConvert('./hwp-files/', {
  format: 'markdown',
  outputDir: './converted/',
});

// Windows 직접 제어 (한글과컴퓨터 앱 설치된 경우)
const winHwp = new HWPProcessor({ useWindowsApp: true });
const nativeResult = await winHwp.toMarkdown('./document.hwp');
```

**CLI 사용:**

```bash
# 단일 파일 변환
k-skill hwp convert document.hwp --format markdown

# 배치 변환
k-skill hwp batch ./hwp-folder/ --format json --output ./output/

# 이미지 추출
k-skill hwp extract-images document.hwp --output ./images/
```

---

### 8. 우편번호 검색

공식 우체국 우편번호 API 사용. 인증 불필요.

```javascript
const { ZipcodeClient } = require('k-skill/zipcode');

const zipcode = new ZipcodeClient();

// 주소 키워드로 검색
const results = await zipcode.search('강남구 테헤란로');

console.log(results);
/*
[
  {
    zipcode: '06236',
    roadAddress: '서울특별시 강남구 테헤란로 152',
    jibunAddress: '서울특별시 강남구 역삼동 736',
    building: '강남파이낸스센터'
  },
  ...
]
*/

// 정확한 건물명으로 검색
const exact = await zipcode.search('롯데월드타워');

// 우편번호로 역조회
const byZip = await zipcode.getByZipcode('05510');
```

---

## 공통 패턴

### 에러 핸들링

```javascript
const { SRTClient, SRTError, SRTAuthError } = require('k-skill/srt');

try {
  const client = new SRTClient({
    username: process.env.SRT_USERNAME,
    password: process.env.SRT_PASSWORD,
  });
  await client.login();
  const trains = await client.searchTrains({ ... });
} catch (err) {
  if (err instanceof SRTAuthError) {
    console.error('로그인 실패. 아이디/비밀번호를 확인하세요.');
  } else if (err instanceof SRTError) {
    console.error('SRT 오류:', err.message, err.code);
  } else {
    throw err;
  }
}
```

### 환경변수 로드 패턴

```javascript
// .env 파일 사용 시
require('dotenv').config();

// sops 복호화 후 환경변수 주입 시
// sops --decrypt secrets.enc.yaml | k-skill env inject 실행 후 자동 주입됨

const { SRTClient } = require('k-skill/srt');
const client = new SRTClient({
  username: process.env.SRT_USERNAME,   // 환경변수 참조
  password: process.env.SRT_PASSWORD,
});
```

---

## CLI 전체 명령어 요약

```bash
# 설치 및 설정
k-skill install                    # 전체 스킬 설치
k-skill install srt kbo lotto      # 선택 설치
k-skill-setup                      # sops+age 설정, secrets 초기화
k-skill env inject                 # 환경변수 주입

# SRT
k-skill srt search --from 수서 --to 부산 --date 20260401 --time 080000
k-skill srt reserve --train SRT123 --passengers 1
k-skill srt list                   # 예약 목록
k-skill srt cancel --id RES456     # 예약 취소

# KBO
k-skill kbo today                  # 오늘 경기
k-skill kbo games --date 20260401
k-skill kbo games --team LG

# 로또
k-skill lotto latest               # 최신 회차
k-skill lotto result --round 1100
k-skill lotto check --numbers 3,14,22,31,40,43

# 지하철
k-skill subway arrivals --station 강남
k-skill subway arrivals --station 강남 --line 2호선

# HWP
k-skill hwp convert doc.hwp --format markdown
k-skill hwp batch ./folder/ --format json
k-skill hwp extract-images doc.hwp

# 우편번호
k-skill zipcode search "강남구 테헤란로"
k-skill zipcode lookup 06236

# 카카오톡 (macOS)
k-skill kakao list
k-skill kakao send --to "홍길동" --message "메시지"
```

---

## 트러블슈팅

### `SRT_USERNAME` 환경변수가 없다는 오류

```bash
# 환경변수 확인
echo $SRT_USERNAME

# .env 파일에 등록
echo 'SRT_USERNAME=your_id' >> .env
echo 'SRT_PASSWORD=your_password' >> .env

# sops로 암호화 관리 권장
k-skill-setup  # 다시 실행하여 secrets 등록
```

### HWP 변환 실패

```bash
# 의존 패키지 확인
npm install -g hwp.js

# Python 백엔드 사용 시
pip install python-hwp

# Windows에서 한컴 앱 직접 제어 시
k-skill hwp convert doc.hwp --use-native
```

### 카카오톡 CLI (macOS) 실행 안 됨

```bash
# kakaocli 설치 확인
which kakaocli

# 없으면 설치
brew install kakaocli
# 또는
npm install -g kakaocli
```

### 서울 지하철 API 키 오류

```bash
# 공공데이터포털에서 API 키 발급
# https://data.seoul.go.kr → 서울시 지하철 실시간 도착정보

export SEOUL_METRO_API_KEY="발급받은_키"
```

### Node.js 버전 오류

```bash
node --version  # v18 이상 권장

# nvm으로 버전 변경
nvm install 20
nvm use 20
```

---

## 로드맵

현재 포함:
- ✅ SRT 예매
- ⚠️ KTX 예매 (개발 중, 현재 미작동)
- ✅ 카카오톡 Mac CLI
- ✅ 서울 지하철 도착정보
- ✅ KBO 경기 결과
- ✅ 로또 당첨 확인
- ✅ HWP 문서 처리
- ✅ 우편번호 검색

다음 후보:
- 쿠팡 주문 조회
- 다나와 가격 비교
- 네이버 스토어 주문 확인
- 당근마켓 매물 조회
- 정부24 민원 조회
- 홈택스 세금 조회

---

## 참고 링크

- [GitHub 저장소](https://github.com/NomaDamas/k-skill)
- [설치 가이드](https://github.com/NomaDamas/k-skill/blob/main/docs/install.md)
- [보안/시크릿 정책](https://github.com/NomaDamas/k-skill/blob/main/docs/security-and-secrets.md)
- [전체 로드맵](https://github.com/NomaDamas/k-skill/blob/main/docs/roadmap.md)
