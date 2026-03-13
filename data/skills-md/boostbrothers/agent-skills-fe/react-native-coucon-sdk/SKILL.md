---
name: react-native-coucon-sdk
description: Coucon SAS authentication SDK using TurboModule for secure authentication with event-based async results. Use when working with coucon, SAS authentication, SAS 인증, coucon SDK, or TurboModule auth.
metadata:
  author: ddocdoc
  version: "1.0.0"
---

# React Native Coucon SDK

@boostbrothers/react-native-coucon-sdk — Coucon SAS(Security Authentication Service) 인증 엔진을 React Native에서 사용하는 TurboModule 기반 SDK.

## When to Apply

Reference this skill when:
- Coucon SAS 인증을 구현할 때
- TurboModule 기반 네이티브 모듈 연동 시
- NativeEventEmitter 이벤트 기반 비동기 패턴 사용 시

## Architecture

```
앱 (React Native)
  ↓ initialize() / run()
  ↓ addOnSASRunCompletedListener()
CouconSdk (TurboModule)
  ↓ TurboModuleRegistry
iOS/Android 네이티브 SAS 엔진
  ↓ 이벤트 방출
NativeEventEmitter (onSASRunCompleted)
  ↓ { index, outString }
앱
```

## ⚠️ CRITICAL: 리스너 등록 순서

> **반드시 리스너를 먼저 등록한 후 run()을 호출하세요.**
>
> `run()`은 즉시 반환되지만 결과는 `onSASRunCompleted` 이벤트로 비동기 전달됩니다.
> 리스너 없이 run()을 호출하면 결과를 받을 수 없습니다.

## API Reference

### initialize()

SAS 엔진을 초기화합니다. 앱 시작 시 한 번 호출.

```typescript
import { CouconSdk } from '@boostbrothers/react-native-coucon-sdk';

await CouconSdk.initialize();
```

### addOnSASRunCompletedListener(callback)

SAS 실행 완료 이벤트 리스너를 등록합니다.

```typescript
const subscription = CouconSdk.addOnSASRunCompletedListener(
  ({ index, outString }) => {
    console.log(`SAS 완료 - index: ${index}, result: ${outString}`);
  }
);

// 컴포넌트 언마운트 시 정리
return () => subscription.remove();
```

### run(index, input)

SAS 엔진을 실행합니다. 결과는 이벤트로 비동기 전달.

```typescript
// ⚠️ 반드시 리스너 등록 후 호출!
CouconSdk.run(0, 'input-string');
```

## Complete Usage Example

```typescript
import { useEffect } from 'react';
import { CouconSdk } from '@boostbrothers/react-native-coucon-sdk';

function useCouconAuth() {
  useEffect(() => {
    // 1. 초기화
    CouconSdk.initialize();

    // 2. 리스너 등록 (run보다 먼저!)
    const subscription = CouconSdk.addOnSASRunCompletedListener(
      ({ index, outString }) => {
        // 4. 결과 수신
        handleAuthResult(index, outString);
      }
    );

    // 3. 실행
    CouconSdk.run(0, 'auth-input');

    return () => subscription.remove();
  }, []);
}
```

## Event Structure

**onSASRunCompleted** 이벤트 데이터:

| Field | Type | Description |
|-------|------|-------------|
| index | number | run()에 전달한 인덱스 값 |
| outString | string | SAS 엔진 처리 결과 문자열 |

## Troubleshooting

**리스너에 이벤트가 오지 않음**: run() 호출 전에 리스너를 등록했는지 확인. 비동기 초기화 완료 후 run() 호출.

**TurboModule 로드 실패**: React Native New Architecture 설정 확인. android/gradle.properties에 `newArchEnabled=true`.

**initialize() 실패**: 네이티브 SAS 엔진 라이브러리가 프로젝트에 올바르게 링크되었는지 확인.

**이벤트 중복 수신**: subscription.remove()로 이전 리스너를 정리했는지 확인. useEffect cleanup에서 remove() 호출.

## Platform Support

| Platform | Support |
|----------|---------|
| iOS | ✅ |
| Android | ✅ |
| Web | ❌ |
