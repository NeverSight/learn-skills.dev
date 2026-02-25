---
name: cliproxyapi-statusline
description: Display cliproxyapi proxy multi-account quota usage in Claude Code statusline. cliproxyapi 프록시 서버의 다중 계정 쿼터 사용량을 Claude Code 상태라인에 표시하는 스킬.
user-invocable: true
license: MIT
compatibility: Designed for Claude Code. Requires Node.js and access to a cliproxyapi proxy server.
metadata:
  author: TinycellCorp
  version: "1.0"
---

# cliproxy-statusline

cliproxyapi 프록시 서버의 다중 계정 쿼터 사용량을 Claude Code 상태라인에 표시하는 방법을 안내합니다.

---

## 0. 설정 (Setup)

### 0-1. 설정 파일

이 스킬은 `~/.cliproxy-statusline.json` 파일에서 프록시 서버 정보를 읽습니다.

```json
{
  "proxyUrl": "http://localhost:3000",
  "managementKey": "your-management-key"
}
```

- `proxyUrl`: cliproxyapi 프록시 서버 URL
- `managementKey`: 관리 API 인증 키

### 0-2. 최초 설정 흐름

설정 파일이 없으면 사용자에게 다음을 순서대로 질문합니다:

1. "cliproxyapi 프록시 서버 URL을 입력해주세요 (기본값: http://localhost:3000):"
2. "관리 API 키(management key)를 입력해주세요:"

입력받은 값으로 `~/.cliproxy-statusline.json`을 생성합니다:

```javascript
import { writeFileSync, chmodSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const CONFIG_PATH = join(homedir(), '.cliproxy-statusline.json');

writeFileSync(CONFIG_PATH, JSON.stringify({
  proxyUrl: userInputUrl || 'http://localhost:3000',
  managementKey: userInputKey
}, null, 2));

// Unix: 파일 권한 제한 (소유자만 읽기/쓰기)
try { chmodSync(CONFIG_PATH, 0o600); } catch {}
```

### 0-3. 설정 로드

```javascript
import { readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const CONFIG_PATH = join(homedir(), '.cliproxy-statusline.json');

function loadConfig() {
  try {
    const raw = readFileSync(CONFIG_PATH, 'utf8');
    const config = JSON.parse(raw);
    if (!config.proxyUrl || !config.managementKey) {
      throw new Error('Missing required fields: proxyUrl, managementKey');
    }
    return config;
  } catch {
    return null; // config not found or invalid
  }
}
```

설정이 없으면(`loadConfig()` returns null) 0-2의 설정 흐름을 실행합니다.

---

## 1. 개요

cliproxyapi는 여러 Anthropic 계정의 OAuth 토큰을 관리하는 프록시 서버입니다. 각 계정마다 5시간 및 7일 단위의 사용량 쿼터가 존재하며, fill-first 라우팅 방식으로 가장 많이 채워진 쿼터를 우선 소진합니다.

상태라인에 쿼터를 표시하면 현재 어느 계정이 활성 중인지, 각 계정의 남은 여유를 한눈에 파악할 수 있습니다.

---

## 2. API 엔드포인트

### 2-1. auth-files 목록 조회

```
GET {PROXY_URL}/v0/management/auth-files
Authorization: Bearer {MGMT_KEY}
```

응답: `files` 배열을 포함하는 객체. `provider === "claude"` 항목만 필터링합니다.

```json
{
  "files": [
    { "name": "account1.json", "provider": "claude" },
    { "name": "account2.json", "provider": "claude" }
  ]
}
```

### 2-2. 계정별 토큰 다운로드

```
GET {PROXY_URL}/v0/management/auth-files/download?name={file.name}
Authorization: Bearer {MGMT_KEY}
```

응답에서 `access_token` 필드를 추출합니다.

### 2-3. Anthropic OAuth usage API

```
GET https://api.anthropic.com/api/oauth/usage
Authorization: Bearer {access_token}
anthropic-beta: oauth-2025-04-20
```

### 2-4. 응답 구조

```json
{
  "five_hour": {
    "utilization": 0.52,
    "resets_at": "2026-02-19T15:30:00Z"
  },
  "seven_day": {
    "utilization": 0.07,
    "resets_at": "2026-02-25T12:00:00Z"
  }
}
```

- `utilization`: 퍼센트 단위 (예: 37.0 = 37%). 코드에서 0.0~1.0 비율로 정규화 필요
- `resets_at`: ISO 8601 리셋 시각

---

## 3. 상태라인 기본 원리

### 3-1. Claude Code settings.json 등록

`~/.claude/settings.json`의 `statusLine.command`에 실행 파일 경로를 등록합니다.

```json
{
  "statusLine": {
    "command": "node /path/to/proxy-status.mjs"
  }
}
```

### 3-2. One-shot 프로세스 모델

상태라인 프로세스는 매 렌더링마다 독립 실행됩니다.

1. Claude Code가 프로세스를 시작합니다.
2. stdin으로 JSON 컨텍스트를 전송합니다.
3. 프로세스는 stdout에 결과를 출력하고 종료합니다.

```javascript
// stdin 소비
const input = await new Promise(resolve => {
  let data = '';
  process.stdin.on('data', chunk => data += chunk);
  process.stdin.on('end', () => resolve(JSON.parse(data || '{}')));
});

// stdout 출력 후 종료
process.stdout.write(output + '\n');
process.exit(0);
```

### 3-3. stdin 주요 필드

| 필드 | 설명 |
|------|------|
| `context_window` | 현재 컨텍스트 사용량 |
| `model` | 현재 모델 이름 |
| `cwd` | 현재 작업 디렉토리 |
| `transcript_path` | 대화 파일 경로 |

### 3-4. ANSI 색상 코드

| 코드 | 용도 | 조건 |
|------|------|------|
| `\x1b[32m` | 초록 (정상) | utilization < 0.70 |
| `\x1b[33m` | 노랑 (주의) | 0.70 ≤ utilization < 0.90 |
| `\x1b[31m` | 빨강 (위험) | utilization ≥ 0.90 |
| `\x1b[2m` | dim (보조 텍스트) | 리셋 시간, 레이블 등 |
| `\x1b[0m` | reset | 색상 종료 |

### 3-5. 바 차트 형식

```javascript
function makeBar(utilization, width = 8) {
  const filled = Math.round(utilization * width);
  return '█'.repeat(filled) + '░'.repeat(width - filled);
}
```

표시 예시:
```
Q1 5h:[████░░░░]52%(1h17m) wk:[█░░░░░░░]7%(6d20h)
Q2 5h:[██████░░]78%(0h43m) wk:[████░░░░]52%(3d12h)
```

리셋까지 남은 시간 포맷:

```javascript
function formatRemaining(resetsAt) {
  const ms = new Date(resetsAt) - Date.now();
  if (ms <= 0) return '0m';
  const h = Math.floor(ms / 3600000);
  const m = Math.floor((ms % 3600000) / 60000);
  if (h >= 24) {
    const d = Math.floor(h / 24);
    return `${d}d${h % 24}h`;
  }
  return `${h}h${m}m`;
}
```

---

## 4. 구현 패턴

### 4-1. HTTP 조회 (node:http / node:https)

```javascript
import { request } from 'node:https';

function httpGet(url, headers = {}) {
  return new Promise((resolve) => {
    const mod = url.startsWith('https') ? require('node:https') : require('node:http');
    const req = mod.get(url, { headers, timeout: 5000 }, res => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); }
        catch { resolve(null); }
      });
    });
    req.on('error', () => resolve(null));
    req.on('timeout', () => { req.destroy(); resolve(null); });
  });
}
```

### 4-2. 파일 기반 캐싱 (30초 TTL)

이중 임계값 전략:
- **TTL (30s)**: 만료 시 백그라운드 갱신 트리거, 기존 캐시 반환
- **TTL*3 (90s)**: 초과 시 캐시 폐기, null 반환

```javascript
import { readFileSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';

const CACHE_PATH = join(homedir(), '.cliproxy-statusline-cache.json');
const TTL = 30_000;

function readCache() {
  try {
    const { ts, data } = JSON.parse(readFileSync(CACHE_PATH, 'utf8'));
    const age = Date.now() - ts;
    return { data, stale: age > TTL, dead: age > TTL * 3 };
  } catch {
    return { data: null, stale: true, dead: true };
  }
}

function writeCache(data) {
  writeFileSync(CACHE_PATH, JSON.stringify({ ts: Date.now(), data }));
}
```

### 4-3. Fill-first 정렬

weekly utilization 내림차순 정렬 → 가장 높은 계정이 현재 활성(fill-first 소진 중).

```javascript
accounts.sort((a, b) => b.seven_day.utilization - a.seven_day.utilization);
```

### 4-4. 프록시 활성 판별

현재 세션이 프록시를 경유하는지 판별합니다. `ANTHROPIC_BASE_URL` 환경변수가 설정되어 있고, 그 값이 설정 파일의 `proxyUrl`과 동일한 호스트를 가리킬 때만 프록시 세션으로 간주합니다.

```javascript
function isProxySession(config) {
  const baseUrl = process.env.ANTHROPIC_BASE_URL;
  if (!baseUrl) return false;
  try {
    const proxyHost = new URL(config.proxyUrl).host;
    const sessionHost = new URL(baseUrl).host;
    return proxyHost === sessionHost;
  } catch {
    return false;
  }
}
```

### 4-5. 전체 조회 함수

```javascript
const config = loadConfig();
if (!config || !isProxySession(config)) {
  // 설정 없음 또는 프록시 비경유 세션 -- 쿼터 라인 생략
  process.stdout.write('\n');
  process.exit(0);
}

async function fetchProxyUsage(proxyUrl, mgmtKey) {
  const authHeader = { Authorization: `Bearer ${mgmtKey}` };

  // 1. auth-files 목록 (응답이 {files:[...]} 객체)
  const resp = await httpGet(`${proxyUrl}/v0/management/auth-files`, authHeader);
  const files = resp.files || [];
  const claudeFiles = files.filter(f => f.provider === 'claude');

  // 2. 각 파일에서 토큰 다운로드
  const tokens = await Promise.all(
    claudeFiles.map(f =>
      httpGet(`${proxyUrl}/v0/management/auth-files/download?name=${encodeURIComponent(f.name)}`, authHeader)
        .then(d => d.access_token)
    )
  );

  // 3. Anthropic usage API 조회
  const usages = await Promise.all(
    tokens.map(token =>
      httpGet('https://api.anthropic.com/api/oauth/usage', {
        Authorization: `Bearer ${token}`,
        'anthropic-beta': 'oauth-2025-04-20',
      })
    )
  );

  return usages;
}

const usages = await fetchProxyUsage(config.proxyUrl, config.managementKey);
```

### 4-6. utilization 정규화

Anthropic API는 utilization을 퍼센트 단위(예: 37.0 = 37%)로 반환합니다. 내부적으로 0.0~1.0 비율로 정규화합니다.

```javascript
function normalizeUtil(val) {
  return val > 1 ? val / 100 : val;
}
```

### 4-7. 표시 렌더링

```javascript
function colorize(utilization, text) {
  const color = utilization >= 0.9 ? '\x1b[31m'
              : utilization >= 0.7 ? '\x1b[33m'
              : '\x1b[32m';
  return `${color}${text}\x1b[0m`;
}

function renderQuota(usages) {
  return usages.map((u, i) => {
    const fh = { utilization: normalizeUtil(u.five_hour.utilization), resets_at: u.five_hour.resets_at };
    const wk = { utilization: normalizeUtil(u.seven_day.utilization), resets_at: u.seven_day.resets_at };
    const fhPct = Math.round(fh.utilization * 100);
    const wkPct = Math.round(wk.utilization * 100);
    return (
      `\x1b[2mQ${i + 1}\x1b[0m ` +
      `\x1b[2m5h:\x1b[0m[${colorize(fh.utilization, makeBar(fh.utilization))}]` +
      `${colorize(fh.utilization, `${fhPct}%`)}` +
      `\x1b[2m(${formatRemaining(fh.resets_at)})\x1b[0m ` +
      `\x1b[2mwk:\x1b[0m[${colorize(wk.utilization, makeBar(wk.utilization))}]` +
      `${colorize(wk.utilization, `${wkPct}%`)}` +
      `\x1b[2m(${formatRemaining(wk.resets_at)})\x1b[0m`
    );
  }).join('\n');
}
```

---

## 5. OMC HUD 연동 (선택 사항)

oh-my-claudecode(OMC) HUD를 사용하는 경우, 별도 statusLine 커맨드 없이 HUD 출력에 쿼터 라인을 통합할 수 있습니다. OMC 없이 standalone 모드를 사용하는 경우 이 섹션을 건너뛰세요.

상세 구현은 [references/omc-hud.md](references/omc-hud.md)를 참조하세요.

---

## 6. 트러블슈팅

### 프록시 서버 미응답

**증상**: 쿼터 라인이 표시되지 않거나 빈 상태.

**동작**:
- TTL 이내 캐시가 있으면 캐시 데이터 표시 (stale 마킹)
- TTL*3 초과 시 null 반환 → 쿼터 라인 생략

**해결**: 프록시 서버 실행 상태 확인. `curl {PROXY_URL}/v0/management/auth-files -H "Authorization: Bearer {KEY}"` 로 직접 테스트.

### 설정 파일을 찾을 수 없음

**증상**: 쿼터 라인이 표시되지 않음.

**확인**: `~/.cliproxy-statusline.json` 파일이 존재하는지 확인합니다.

```bash
cat ~/.cliproxy-statusline.json
```

**해결**: 파일이 없으면 수동으로 생성합니다:

```bash
echo '{"proxyUrl":"http://localhost:3000","managementKey":"YOUR_KEY"}' > ~/.cliproxy-statusline.json
```

또는 스킬을 다시 호출하여 설정 흐름을 실행합니다.

### settings.json의 env가 상태라인에 전달되지 않음

**증상**: `settings.json`의 `env` 섹션에 설정한 환경변수가 statusLine 프로세스에서 읽히지 않음.

**해결**: `~/.cliproxy-statusline.json` 설정 파일을 사용합니다 (Section 0 참조). 환경변수 대신, `loadConfig()`로 설정을 읽습니다.

```javascript
const config = loadConfig(); // ~/.cliproxy-statusline.json
const { proxyUrl, managementKey } = config;
```

### 프록시 경유인데 쿼터가 표시되지 않음

**증상**: 프록시를 통해 접속했는데 쿼터 라인이 표시되지 않음.

**원인**: `isProxySession()`은 `process.env.ANTHROPIC_BASE_URL`을 확인합니다. 이 환경변수가 셸 레벨에서 설정되어야 statusLine 프로세스가 상속받을 수 있습니다. `settings.json`의 `env` 섹션에만 설정된 경우 statusLine 프로세스에는 전달되지 않습니다.

**해결**: 프록시 실행 래퍼(예: `ccs` alias)에서 `ANTHROPIC_BASE_URL`을 셸 환경변수로 export합니다:

```bash
export ANTHROPIC_BASE_URL="http://localhost:3000"
claude  # 이 프로세스와 statusLine이 환경변수를 상속받음
```

### OMC non-breaking space 변환으로 문자열 매칭 실패

**증상**: OMC HUD가 출력 문자열 내 일반 공백을 `\u00A0`(non-breaking space)으로 변환하여 정규식이나 문자열 비교가 실패함.

**해결**: 공백 비교 시 `\u00A0`도 함께 처리:

```javascript
const normalized = str.replace(/\u00A0/g, ' ');
```

### 첫 실행 시 캐시 없음

**증상**: 최초 실행 시 쿼터 라인이 표시되지 않음.

**동작 (정상)**: 캐시 파일이 없으면 fetch를 await하여 캐시를 생성하고, 결과를 표시합니다.

```javascript
const config = loadConfig();
if (!config || !isProxySession(config)) {
  process.stdout.write('\n');
  process.exit(0);
}

const { data, stale, dead } = readCache();

if (!dead && data) {
  output = renderQuota(data);
  if (stale) {
    // stale: 기존 캐시 표시 후 백그라운드 갱신 (fire-and-forget OK)
    fetchProxyUsage(config.proxyUrl, config.managementKey)
      .then(writeCache)
      .catch(() => {});
  }
} else {
  // dead 또는 캐시 없음: await로 fetch 완료 대기
  try {
    const fresh = await fetchProxyUsage(config.proxyUrl, config.managementKey);
    writeCache(fresh);
    output = renderQuota(fresh);
  } catch {
    output = '';
  }
}
```
