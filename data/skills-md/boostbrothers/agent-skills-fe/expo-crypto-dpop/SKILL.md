---
name: expo-crypto-dpop
description: RFC 9449 DPoP authentication crypto module for EC P-256 key generation, DPoP proof JWT creation, and secure token binding. Use when working with DPoP, dpop proof, RFC 9449, token binding, OAuth, or expo-crypto-dpop.
metadata:
  author: ddocdoc
  version: "1.0.0"
---

# Expo Crypto DPoP

RFC 9449 표준 기반 DPoP(Demonstrating Proof-of-Possession) 인증 모듈. EC P-256 키 쌍을 안전하게 생성·보관하고, OAuth 2.0 액세스 토큰에 암호학적으로 바인딩된 DPoP 증명 JWT를 생성합니다.

## When to Apply

Reference this skill when:
- DPoP 인증을 구현할 때
- OAuth 2.0 토큰 바인딩이 필요할 때
- RFC 9449 관련 작업 시
- Axios 인터셉터에 DPoP 헤더를 추가할 때
- 앱 재설치 후 키 관리가 필요할 때

## DPoP 개요

Bearer 토큰의 보안 취약점을 해결하는 RFC 9449 확장 메커니즘:
- 요청마다 개인 키로 서명된 DPoP 증명 JWT 전송
- 서버가 공개 키로 서명 검증하여 정당한 클라이언트 확인
- 탈취된 토큰도 개인 키 없이는 사용 불가

## API Reference

### ensureKeyPair()

앱 시작 시 호출하여 키 쌍을 확보. 앱 재설치 시 구 키 삭제 후 새 키 자동 생성.

```typescript
import { ensureKeyPair } from 'expo-crypto-dpop';

// 앱 초기화 시
await ensureKeyPair();
```

### createProof(params)

매 API 요청마다 호출하여 DPoP 증명 JWT를 생성.

```typescript
import { createProof } from 'expo-crypto-dpop';

const proof = await createProof({
  htm: 'POST',           // HTTP 메서드
  htu: 'https://api.example.com/token',  // HTTP URI (쿼리 파라미터 제외!)
  accessToken: 'eyJ...',  // 선택: 액세스 토큰 바인딩 (ath 클레임)
  nonce: 'server-nonce',  // 선택: 서버 제공 nonce
});
```

> ⚠️ **CRITICAL**: `htu`는 RFC 9449에 따라 쿼리 파라미터와 프래그먼트를 포함하지 않아야 합니다. URL 객체의 `origin + pathname`만 사용하세요.

### deleteKeyPair()

로그아웃 시 DPoP 키 삭제 (선택사항, 보안 정책에 따라 결정).

```typescript
import { deleteKeyPair } from 'expo-crypto-dpop';
await deleteKeyPair();
```

## DPoP JWT 구조

**Header:**
```json
{
  "typ": "dpop+jwt",
  "alg": "ES256",
  "jwk": { "kty": "EC", "crv": "P-256", "x": "...", "y": "..." }
}
```

**Payload:**
```json
{
  "jti": "unique-id",
  "htm": "POST",
  "htu": "https://api.example.com/token",
  "iat": 1234567890,
  "ath": "base64url(sha256(access_token))",
  "nonce": "server-provided-nonce"
}
```

## Architecture

```
앱 → expo-crypto-dpop → expo-secure-store →
  ├── iOS: Security.framework (Keychain)
  └── Android: KeyStore
→ OAuth 서버
```

**주요 기능:**
- EC P-256 키 쌍 생성 (네이티브 암호화 라이브러리)
- DPoP 증명 JWT 생성 (ES256)
- expo-secure-store를 통한 보안 키 저장
- 앱 재설치 감지 (iOS Keychain 영속성 처리)
- Nonce 지원 (DPoP-Nonce 헤더)
- 토큰 바인딩 (ath 클레임)

## Troubleshooting

**KEY_GENERATION_FAILED**: 네이티브 암호화 라이브러리 접근 실패. expo-secure-store 설정 확인.

**KEY_NOT_FOUND**: 키 쌍이 존재하지 않음. ensureKeyPair()를 먼저 호출했는지 확인.

**SIGNING_FAILED**: JWT 서명 실패. 키 쌍 무결성 확인. 재설치 후 발생 시 ensureKeyPair()로 키 재생성.

**INVALID_INPUT**: htm, htu 파라미터 확인. htu에 쿼리 파라미터가 포함되지 않았는지 확인.

**앱 재설치 후 인증 실패**: iOS Keychain은 앱 삭제 후에도 데이터가 남을 수 있음. ensureKeyPair()가 이를 자동 처리하지만, 서버 측에서도 키 갱신을 지원해야 함.

## How to Use

Read the integration patterns file for Axios interceptor setup:

```
rules/integration-patterns.md  — Axios 인터셉터, Nonce 처리, 토큰 갱신 흐름
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
