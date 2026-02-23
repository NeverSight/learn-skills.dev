---
name: mj-download
description: 미드저니 오늘 생성한 이미지를 zip으로 일괄 다운로드합니다. 로그인이 안 되어 있으면 자동으로 로그인을 먼저 처리합니다. 미드저니 이미지 백업이 필요할 때 사용합니다.
---

# 미드저니 작업물 다운로드

## 사전 조건
- Playwright가 설치되어 있지 않으면: `art-repo-package-install`을 먼저 실행하라고 안내 후 중단.

## 스크립트

| 스크립트 | 위치 | 역할 |
|----------|------|------|
| `check_login.ts` | `.agents/skills/mj-login/` | 세션 JSON의 인증 쿠키 유효성 확인 |
| `login.ts` | `.agents/skills/mj-login/` | 브라우저를 열어 수동 로그인, 세션을 JSON으로 저장 |
| `download.ts` | `.agents/skills/mj-download/` | 세션 JSON으로 인증하여 오늘 이미지를 zip으로 다운로드 |

## 실행 흐름

### 1단계: 로그인 확인

```typescript
import { checkLogin } from '../mj_login/check_login.js';

const result = checkLogin("mj_account");
// true: 로그인 정보 존재 → 3단계로 진행
// false: 로그인 정보 없음 → 2단계로 진행
```

또는 CLI 실행:
```bash
pnpm exec tsx .agents/skills/mj-login/check_login.ts ace
# 샌드박스 환경(codex 인터랙티브)에서 IPC 소켓 오류 발생 시:
node --import tsx/esm .agents/skills/mj-login/check_login.ts ace
```

### 2단계: 로그인 (1단계에서 false일 때만)

```typescript
import { login } from '../mj_login/login.js';

const result = await login("mj_account");
// 브라우저가 열린다. 사용자에게 디스코드 계정으로 로그인하라고 안내한다.
// 로그인 완료 시 (/explore 페이지 이동 감지, 최대 2분) 세션이 sessions/mj_{account_name}.json에 저장된다.
// true: 로그인 성공 → 3단계로 진행
// false: 로그인 실패 → 사용자에게 실패를 알리고 중단한다 (3단계 진행하지 않음)
```

또는 CLI 실행:
```bash
pnpm exec tsx .agents/skills/mj-login/login.ts ace
# 샌드박스 환경(codex 인터랙티브)에서 IPC 소켓 오류 발생 시:
node --import tsx/esm .agents/skills/mj-login/login.ts ace
```

### 3단계: 다운로드

```typescript
import { download } from './download.js';

const result = await download("mj_account", "./downloads/mj");
// download_dir 기본값: ./downloads/mj
// true: 다운로드 성공
// false: 다운로드 실패 (세션 파일 없음, 오늘 이미지 없음, 시간 초과 등)
```

또는 CLI 실행:
```bash
pnpm exec tsx .agents/skills/mj-download/download.ts ace
# 샌드박스 환경(codex 인터랙티브)에서 IPC 소켓 오류 발생 시:
node --import tsx/esm .agents/skills/mj-download/download.ts ace
```

## 파라미터 (공통)
- `account_name` (string, 필수): 미드저니 계정명. 세션은 `sessions/mj_{account_name}.json`에 저장된다.
- `download_dir` (string, 선택, download만 해당): 다운로드 파일 저장 디렉토리. 기본값 `./downloads/mj`.

## 결과 보고
각 단계의 콘솔 출력을 확인하여 사용자에게 전달한다.
- `다운로드 완료: {경로}` → 저장된 파일 경로와 파일 크기를 알린다.
- 파일 크기가 0이면 다운로드 실패로 간주하고 사용자에게 알린다.
- `오늘 생성한 이미지가 없습니다` → 해당 내용을 전달한다.
- `[오류]` → 에러 메시지를 전달하고 원인을 분석한다.
