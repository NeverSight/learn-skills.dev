---
name: react-native-kms-module
description: AWS KMS native module for secure data encryption and decryption using envelope encryption pattern. Use when working with KMS encrypt, KMS decrypt, AWS KMS, data encryption, or react-native-aws-kms.
metadata:
  author: ddocdoc
  version: "1.0.0"
---

# React Native KMS Module

@boostbrothers/react-native-aws-kms — AWS Key Management Service(KMS)를 사용하여 민감한 데이터를 안전하게 암호화하고 복호화하는 React Native 네이티브 모듈. Expo Modules API 기반.

## When to Apply

Reference this skill when:
- AWS KMS를 사용한 데이터 암호화/복호화 구현 시
- 엔벨로프 암호화 패턴을 이해해야 할 때
- KMS 자격증명 관리 관련 작업 시

## Architecture: Envelope Encryption

AWS KMS는 엔벨로프 암호화를 사용합니다. 데이터를 KMS에 직접 전송하지 않고, KMS에서 생성한 데이터 키(DEK)로 로컬에서 암호화합니다.

```
앱 (React Native)
  ↓ init() / encrypt() / decrypt()
KMS Module (Expo NativeModule)
  ↓
네이티브 레이어 (iOS Swift / Android Kotlin)
  ↓ AWS KMS API 호출
AWS KMS → 데이터 키 반환
  ↓
네이티브 레이어: AES-256-ECB 로컬 암호화
  ↓
Base64 문자열 반환
```

## API Reference

### init(config)

KMS 클라이언트를 초기화합니다.

```typescript
import { init } from '@boostbrothers/react-native-aws-kms';

await init({
  region: 'ap-northeast-2',
  keyId: 'arn:aws:kms:ap-northeast-2:123456:key/abcd-1234',
  accessKey: credentials.accessKeyId,
  secretKey: credentials.secretAccessKey,
  sessionToken: credentials.sessionToken,
});
```

> ⚠️ **SECURITY WARNING**: `accessKey`, `secretKey`, `sessionToken`을 소스 코드에 하드코딩하지 마세요. 환경 변수, AWS Cognito Identity Pool, 또는 STS를 통해 동적으로 자격증명을 획득하세요.

### encrypt(plainText)

데이터를 암호화합니다. KMS에서 데이터 키를 생성하고 로컬에서 AES-256-ECB로 암호화.

```typescript
const encrypted = await encrypt('민감한 데이터');
// encrypted: Base64 인코딩된 암호문
```

### decrypt(cipherText)

암호화된 데이터를 복호화합니다.

```typescript
const decrypted = await decrypt(encrypted);
// decrypted: 원본 평문
```

## AWS KMS 특징

- **FIPS 140-2 인증 HSM** 사용
- **CloudTrail** 감사 로그
- **IAM** 기반 세밀한 접근 제어
- **자동 키 교체** (Key Rotation) 지원

## Usage Example

```typescript
import { init, encrypt, decrypt } from '@boostbrothers/react-native-aws-kms';

// 1. STS에서 임시 자격증명 획득
const credentials = await getTemporaryCredentials();

// 2. KMS 초기화
await init({
  region: 'ap-northeast-2',
  keyId: 'arn:aws:kms:...',
  ...credentials,
});

// 3. 암호화
const cipherText = await encrypt('주민등록번호: 123456-1234567');

// 4. 복호화
const plainText = await decrypt(cipherText);
```

## Troubleshooting

**자격증명 오류**: accessKey/secretKey/sessionToken이 유효한지 확인. STS 토큰의 만료 시간 체크.

**네트워크 오류**: AWS KMS 엔드포인트 접근 가능 여부 확인. VPN 또는 프록시 설정 검토.

**키 권한 오류**: IAM 정책에서 해당 KMS 키에 대한 encrypt/decrypt 권한이 있는지 확인.

**Base64 디코딩 오류**: encrypt() 반환값은 Base64 문자열. 추가 인코딩 없이 그대로 decrypt()에 전달.

## Platform Support

| Platform | Support |
|----------|---------|
| iOS | ✅ |
| Android | ✅ |
| Web | ❌ |
