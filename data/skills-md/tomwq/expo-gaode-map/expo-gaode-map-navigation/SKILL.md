---
name: expo-gaode-map-navigation
description: 高德导航全功能一体化方案：集成完整地图能力（MapView/全部覆盖物/离线地图/定位/几何计算，无需核心包），提供官方 NaviView 导航 UI（语音/事件/路况/指南针）；支持多模式路径规划（驾车/步行/骑行/货车/摩托车/电动车）及策略/限行/途经点；具备高级独立算路能力（预估/路线预览/选择/启动）；包含 Config Plugin 自动配置；与 expo-gaode-map 存在 SDK 冲突，项目仅需安装此包。
---

# Expo Gaode Map Navigation

## 描述
`expo-gaode-map-navigation` 是高德导航 SDK 的 React Native 封装。它提供了完整的导航解决方案，包括嵌入式导航 UI (`NaviView`)、多模式路径规划 API 以及高级的独立算路功能。

## 使用场景
- **应用内导航**：直接在 App 内部显示导航界面，无需跳转第三方 App。
- **路径规划**：计算两点间的距离、耗时、路线详情（支持驾车、步行、骑行）。
- **特殊车辆导航**：支持货车（限高/限重）、摩托车、电动车导航。
- **行前选路**：在开始导航前预览多条路线方案并进行选择。

## 开发指令

### 1. 基础集成 (NaviView)
- 使用 `<ExpoGaodeMapNaviView>` 组件嵌入导航界面。
- 通过 `ref` 调用 `startNavigation` 和 `stopNavigation`。
- 必须设置 `style` (通常是 `flex: 1`)。

### 2. 路径规划 (Routing)
- **驾车**: `calculateDriveRoute`
- **步行**: `calculateWalkRoute`
- **骑行**: `calculateRideRoute`
- **货车**: `calculateTruckRoute` (需设置 `TruckSize`, `height`, `load` 等)

### 3. 高级功能 (Advanced)
- **独立算路**: 使用 `independentDriveRoute` + `selectIndependentRoute` 实现行前路线预览与选择。
- **UI 定制**: 使用 `showMode`, `naviMode`, `showTrafficBar` 等属性深度定制导航界面。

## 快速模式

### ✅ 场景 1：嵌入式导航 UI
```tsx
import { ExpoGaodeMapNaviView } from 'expo-gaode-map-navigation';

// 必须使用 ref 来控制导航开始/结束
const naviRef = useRef(null);

<ExpoGaodeMapNaviView
  ref={naviRef}
  style={{ flex: 1 }}
  naviType={0} // 0: GPS, 1: 模拟
  showTrafficButton={true}
  onArrive={() => console.log('到达目的地')}
/>

// 发起导航
naviRef.current?.startNavigation(null, { latitude: 39.9, longitude: 116.4 }, 0);
```

### ✅ 场景 2：驾车路径规划
```ts
import { calculateDriveRoute, DriveStrategy } from 'expo-gaode-map-navigation';

const result = await calculateDriveRoute({
  from: { latitude: 39.9, longitude: 116.4 },
  to: { latitude: 39.95, longitude: 116.45 },
  strategy: DriveStrategy.AVOID_CONGESTION
});
console.log(`距离: ${result.routes[0].distance}米`);
```

## 🛡️ 类型安全最佳实践
本库提供了完整的 TypeScript 定义，请参考 [类型定义文档](./resources/types.md) 了解详情。

**核心原则**：
1. **请勿使用 `any`**，始终导入并使用正确的类型（如 `DriveRouteOptions`, `NaviInfo`, `DriveStrategy` 等）。
2. **优先使用原生计算**：涉及到路径相关的计算（如距离、时间、吸附、抽稀等），**必须优先使用 `expo-gaode-map` (Core) 包中 `ExpoGaodeMapModule` 提供的原生几何方法**。严禁在 JS 层手写地理算法。

## 参考文档
- [导航 API 详解 (NaviView & Routing)](./resources/navigation-api.md)
- [核心导航指南 (Navigation Core)](./resources/navigation.md)
