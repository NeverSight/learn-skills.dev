---
name: react-native-naver-map
description: Naver Map SDK React Native wrapper for rendering maps with overlays, markers, clustering, camera control, and location tracking. Use when working with 네이버 지도, naver map, map overlay, marker clustering, path overlay, or NaverMapView.
metadata:
  author: ddocdoc
  version: "1.0.0"
---

# React Native Naver Map

@boostbrothers/react-native-naver-map — 네이버 지도 SDK(NMapsMap)를 React Native에서 사용할 수 있도록 래핑한 라이브러리. 선언적 React 컴포넌트 방식으로 지도를 렌더링합니다.

## When to Apply

Reference this skill when:
- 네이버 지도 컴포넌트를 구현할 때
- 마커, 경로선, 폴리곤 등 오버레이를 추가할 때
- 카메라 애니메이션, 좌표 변환 작업 시
- 마커 클러스터링을 구현할 때
- 위치 추적 모드를 설정할 때

## Component Quick Reference

| Component | Description |
|-----------|-------------|
| NaverMapView | 지도를 렌더링하는 메인 컴포넌트 |
| NaverMapMarkerOverlay | 지도 위에 마커를 표시 |
| NaverMapInfoWindow | 마커 또는 좌표 위에 정보창 표시 |
| NaverMapPathOverlay | 경로선 표시 (진척률 지원) |
| NaverMapPolylineOverlay | 폴리라인 표시 |
| NaverMapPolygonOverlay | 다각형 영역 표시 |
| NaverMapCircleOverlay | 원형 영역 표시 |
| NaverMapArrowheadPathOverlay | 화살표 머리가 있는 경로선 |
| NaverMapMultiPathOverlay | 구간별 색상이 다른 다중 경로선 |
| NaverMapGroundOverlay | 특정 지도 영역에 이미지 표시 |

## NaverMapViewRef Methods

| Method | Description |
|--------|-------------|
| animateCameraTo(params) | 특정 좌표로 카메라 이동 (애니메이션) |
| animateCameraBy(params) | 현재 위치에서 상대적으로 카메라 이동 |
| animateRegionTo(params) | 특정 영역으로 카메라 이동 |
| animateCameraWithTwoCoords(params) | 두 좌표를 기준으로 자동 줌 |
| cancelAnimation() | 진행 중인 카메라 애니메이션 취소 |
| setLocationTrackingMode(mode) | 위치 추적 모드 설정 |
| screenToCoordinate(point) | 화면 좌표 → 위경도 좌표 변환 |
| coordinateToScreen(coord) | 위경도 좌표 → 화면 좌표 변환 |

## Key Types Summary

**MapType**: Basic | Navi | Satellite | Hybrid | Terrain | NaviHybrid

**LocationTrackingMode**: None | NoFollow | Follow | Face

**CameraAnimationEasing**: None | Fly | Linear | EaseIn | EaseOut

**CameraMoveBaseParams**: duration?, easing?, pivot?

**MapImageProp**: 마커 및 오버레이에서 사용하는 이미지 타입

**BaseOverlayProps**: zIndex?, globalZIndex?, isHidden?, minZoom?, maxZoom?, isMinZoomInclusive?, isMaxZoomInclusive?, onTap?

## Main Features

### 지도 유형
NaverMapView의 `mapType` prop으로 설정:
```tsx
<NaverMapView mapType="Navi" style={{ flex: 1 }} />
```

### 레이어 그룹
건물, 교통, 대중교통, 자전거, 등산로, 지적편집도 레이어를 on/off.

### 마커 클러스터링
줌 레벨에 따라 근접 마커들을 자동 클러스터링. `onTapClusterLeaf` 콜백으로 클러스터 내 마커 탭 처리.

### 카메라 제어
ref를 통한 명령형 제어:
```tsx
const mapRef = useRef<NaverMapViewRef>(null);
mapRef.current?.animateCameraTo({
  latitude: 37.5665,
  longitude: 126.9780,
  duration: 1000,
  easing: 'EaseOut',
});
```

### 위치 추적
4가지 모드: None(끔), NoFollow(위치만 표시), Follow(위치+카메라 추적), Face(방향+카메라 추적).

### 좌표 변환
화면 좌표 ↔ 위경도 좌표 변환:
```tsx
const coord = await mapRef.current?.screenToCoordinate({ x: 100, y: 200 });
const point = await mapRef.current?.coordinateToScreen({ latitude: 37.5, longitude: 127.0 });
```

## Architecture

```
React Native JS/TS Layer
  ↓ (JSX Props)
NaverMapView Component
  ↓ (React Native Bridge)
Native Module
  ├── iOS: NMapsMap.framework
  └── Android: naver-map-sdk
```

네이버 지도 API 클라이언트 ID가 반드시 등록되어야 합니다 (iOS Info.plist, Android AndroidManifest.xml).

## How to Use

Read individual reference files for detailed API and troubleshooting:

```
rules/api-components.md   — 10개 컴포넌트 상세 Props
rules/api-types.md        — 모든 타입, 인터페이스, Enum
rules/troubleshooting.md  — iOS/Android 빌드 오류, Expo 이슈
```

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
