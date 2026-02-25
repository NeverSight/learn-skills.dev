---
name: expo-gaode-map-web-api
description: 高德 Web 服务纯 JS 完整封装：提供 V5 路径规划（驾车/新能源/步行/骑行/跨城公交）、地理编码（正/逆）、POI 搜索（关键字/周边/多边形）及输入提示；内置 LRU 缓存、自动重试与请求取消机制；全 TypeScript 类型定义；适用于跨平台逻辑层，需配合核心包或导航包配置 Key。
---

# Web API 开发 (Web API)

## 描述
协助开发者使用 `expo-gaode-map-web-api` 包。该包是纯 JavaScript 实现，封装了高德 Web 服务 API，支持跨平台使用。

## 使用场景
- 需要使用高德最新的 **V5 版路径规划**（支持更多策略、新能源车等）。
- 需要**跨城**公交路径规划。
- 需要在非原生环境（如纯 JS 逻辑层）进行地理编码或算路。
- 原生搜索包无法满足特定的 API 需求时。

## 开发指令
1. **Key 配置**：在基础包初始化时传入 `webKey`，或构造时传入。
2. **实例化**：创建 `GaodeWebAPI` 实例。
3. **调用服务**：
   - 路径规划：`api.route.driving/walking/transit`
   - 地理编码：`api.geocode.geocode/regeocode`

## ⚠️ 性能优化提示
当处理 API 返回的 `polyline` 数据时，**强烈建议**结合 `ExpoGaodeMapModule` 的原生计算能力：
- **解析**：使用 `ExpoGaodeMapModule.parsePolyline(str)` 解析坐标串，比 JS 手动 split 快得多。
- **优化**：使用 `ExpoGaodeMapModule.simplifyPolyline(points, tolerance)` 进行 RDP 抽稀，显著减少地图渲染压力。

## 🛡️ 类型安全与稳定性
本库提供了完整的 TypeScript 定义，请参考 [类型定义文档](./resources/types.md) 了解详情。

**核心原则：请勿使用 `any`**，始终导入并使用正确的类型（如 `DrivingRouteResponse`, `Step`, `Path` 等）。

### 稳定性特性
- **自动重试**：网络波动或限流时自动重试（默认 3 次）。
- **LRU 缓存**：可开启内存缓存，减少重复请求，提升性能。
- **请求取消**：支持 `AbortSignal`，防止输入提示等场景下的竞态问题。

## 快速模式

### ✅ 正确：全局下发 Web Key
```ts
// 推荐做法：在 Core 或 Navigation 初始化时一并传入
ExpoGaodeMapModule.initSDK({
  androidKey: '...',
  iosKey: '...',
  webKey: 'YOUR_WEB_KEY'
});

// 之后随处可用，可开启缓存
const api = new GaodeWebAPI({ enableCache: true });
```

### ✅ 正确：处理 API 错误
```ts
try {
  await api.route.driving(...);
} catch (e) {
  if (e instanceof GaodeAPIError) {
    console.log('高德服务报错:', e.info);
  }
}
```

## 参考文档
- [Web API 详解 (Web API)](./resources/web-api.md)
- [类型定义参考 (Types)](./resources/types.md)
