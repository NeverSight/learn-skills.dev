---
name: react-native-device-data-module
description: Cross-platform native storage access module providing unified interface to iOS UserDefaults and Android SharedPreferences. Use when working with device data, UserDefaults, SharedPreferences, native storage, device storage, or platform key mapping.
metadata:
  author: ddocdoc
  version: "1.0.0"
---

# React Native Device Data Module

@boostbrothers/react-native-device-data-module — iOS UserDefaults와 Android SharedPreferences에 대한 통합 인터페이스를 제공하는 네이티브 스토리지 모듈. 플랫폼별 스토리지 키 차이를 단일 통합 키 시스템으로 추상화합니다.

## When to Apply

Reference this skill when:
- 네이티브 스토리지(UserDefaults/SharedPreferences)에 접근할 때
- 플랫폼 간 키 매핑이 필요할 때
- 동적 키(userId 기반) 사용 시
- 토큰, 디바이스 ID 등 저장된 값을 읽을 때

## Architecture

```
App Code
  ↓
UnifiedDeviceDataModule
  ↓
Platform Key Mapping
  ↓ Platform Detection
  ├── iOS → UserDefaults
  └── Android → SharedPreferences
        ↓ Value Transform (JSON 파싱)
        ↓ Timestamp 통일
```

> **중요**: 모든 통합 키(UnifiedKey)는 내부적으로 현재 플랫폼에 맞는 실제 스토리지 키로 변환됩니다. 플랫폼별 키 이름을 직접 사용할 필요가 없습니다.

## Key Features

| Feature | Description |
|---------|-------------|
| Unified Key System | iOS/Android 단일 키 이름 |
| Platform Key Mapping | 레거시 키 완전 호환 |
| Dynamic Key Support | 런타임 파라미터(userId 등) |
| Value Transform | Android JSON 자동 파싱 |
| Timestamp Unification | 플랫폼 간 시간 표준화 |

## Key Mapping Summary

| Unified Key | 용도 |
|-------------|------|
| requirePermissionSuccessScreen | 권한 요청 성공 화면 |
| deviceId | 기기 고유 ID |
| userSSN | 주민번호 (동적 키: userId 필요) |
| familyReceiptPopUp | 가족 접수 팝업 |
| kidsGrowthOverAgePopUp | 아이 성장 나이 초과 |
| appReviewPopUp | 앱 리뷰 유도 |
| accessToken | 액세스 토큰 |
| refreshToken | 리프레시 토큰 |
| expiresTimestamp | 토큰 만료 시각 |
| fcmRegisterId | FCM ID (Android 전용) |
| familyEditAuthPopUp | 가족 수정 인증 |
| noLoginADPushAllowed | 광고 푸시 허용 (JSON 변환) |
| noLoginADPushAllowedTime | 광고 푸시 변경 시각 (JSON 변환) |

> 전체 플랫폼 매핑 테이블: `rules/platform-key-mapping.md`

## Critical Edge Cases

### 1. 동적 키: userSSN
Android에서 `userId` 파라미터로 키 생성:
```typescript
// userId='12345' → Android 키: 'USER_SSN_12345'
const ssn = await getDeviceData('userSSN', { userId: '12345' });
```
> ⚠️ params 없으면 `USER_SSN_undefined` 생성됨

### 2. Android 전용: fcmRegisterId
iOS에서 호출하면 빈 문자열 반환:
```typescript
import { Platform } from 'react-native';
if (Platform.OS === 'android') {
  const fcmId = await getDeviceData('fcmRegisterId');
}
```

### 3. JSON 변환 키: noLoginADPushAllowed / noLoginADPushAllowedTime
Android 저장 형식:
```json
{ "enablePush": true, "changedDate": "2024-01-15T10:30:00.000Z" }
```
- `noLoginADPushAllowed` → `enablePush` 필드 추출 (boolean)
- `noLoginADPushAllowedTime` → `changedDate` 밀리초 변환 (number)
> ⚠️ iOS는 개별 값으로 저장, Android는 JSON 객체로 저장 — 모듈이 자동 변환

### 4. 타임스탬프 통일
모든 타임스탬프를 밀리초 단위로 정규화:
- 밀리초 숫자 (>1,000,000,000,000): 그대로
- 초 단위: ×1000
- ISO 문자열: `new Date(value).getTime()`

## Troubleshooting

**키를 찾을 수 없음**: UnifiedKey 이름이 올바른지 확인. 플랫폼별 실제 키 이름은 rules/platform-key-mapping.md 참조.

**타입 불일치**: iOS/Android에서 같은 키가 다른 타입을 반환할 수 있음 (예: noLoginADPushAllowed — iOS: string, Android: boolean). 모듈의 Value Transform이 이를 처리하지만, 타입 단언 주의.

**동적 키 undefined**: params 객체에 필수 파라미터를 전달했는지 확인. userSSN은 { userId } 필수.

**Android JSON 파싱 실패**: SharedPreferences에 저장된 값이 유효한 JSON인지 확인.

## How to Use

Read the platform key mapping file for full mapping details:

```
rules/platform-key-mapping.md  — iOS/Android 키 매핑 전체 테이블, 엣지 케이스 상세
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
