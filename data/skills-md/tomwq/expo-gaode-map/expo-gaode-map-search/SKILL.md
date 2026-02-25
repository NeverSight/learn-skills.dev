---
name: expo-gaode-map-search
description: 高德原生搜索高性能方案：基于原生 SDK 实现，无 Web 配额限制；提供全场景 POI 搜索（关键字/周边/沿途/多边形/ID详情）；支持输入提示（Autocomplete）与逆地理编码（坐标转地址）；提供完整 TypeScript 定义；需依赖核心包或导航包初始化。
---

# 原生搜索开发 (Search)

## 描述
协助开发者使用 `expo-gaode-map-search` 包进行原生搜索功能的开发。该包直接调用高德原生 SDK 接口，相比 Web API 具有更优的性能且不消耗 Web 服务配额。

## 使用场景
- 需要搜索 POI（兴趣点），如“附近的加油站”。
- 需要实现搜索框的自动补全（输入提示）。
- 需要将坐标转换为地址（逆地理编码）。
- 需要高性能搜索，无额外网络请求开销。

## 开发指令
1. **依赖**：确保已安装任一基础包 (`core` 或 `navigation`) 并初始化。
2. **POI 搜索**：
   - 关键字搜索：`searchPOI`
   - 周边搜索：`searchNearby`
   - 沿途搜索：`searchAlong`
3. **辅助功能**：
   - 输入提示：`getInputTips`
   - 逆地理：`reGeocode`

## 快速模式

### ✅ 正确：在搜索前初始化
```ts
import { initSearch } from 'expo-gaode-map-search';

// 可选：提前调用以检测 API Key 配置问题
initSearch();
```

### ✅ 正确：使用城市编码提高准确性
```ts
// 相比使用 "北京"，使用 "010" 能更准确地锁定区域
const result = await searchPOI({
  keyword: '银行',
  city: '010'
});
```

### ❌ 错误：不处理搜索空结果
搜索可能返回 0 个结果或抛出异常（如网络问题、API Key 无效），务必使用 try-catch 并检查 `result.pois.length`。

## 🛡️ 类型安全最佳实践
本库提供了完整的 TypeScript 定义，请参考 [类型定义文档](./resources/types.md) 了解详情。

**核心原则：请勿使用 `any`**，始终导入并使用正确的类型（如 `PoiSearchOptions`, `Poi`, `InputTip` 等）。

## 参考文档
- [原生搜索 API 参考 (Search API)](./resources/search-api.md)
- [原生搜索 API 详解 (Search)](./resources/search.md)
- [类型定义参考 (Types)](./resources/types.md)
