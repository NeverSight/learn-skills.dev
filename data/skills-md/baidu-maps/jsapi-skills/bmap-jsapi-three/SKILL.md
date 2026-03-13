---
name: bmap-jsapi-three
description: 使用 MapV-Three 构建专业的 3D 地图和 GIS 应用 - 基于 Z-up 坐标系的 3D 地图库，支持地图编辑、测量工具、要素绘制、数据管理等地理可视化功能。适用于创建地图编辑器、测量工具、空间数据可视化等 Web-GIS 应用。
license: MIT
version: 1.1.0
---

# MapV-Three 开发指南

使用 MapV-Three 构建高性能的 3D 地图和 GIS 应用 - 一个采用 Z-up 坐标系的跨浏览器 WebGL 库。

## 何时适用

在以下场景中参考这些指南：

- 3D 地图编辑和要素绘制
- 地图测量工具开发
- 建筑物、区域等 3D 可视化
- 实时交通数据展示
- 路径追踪动画开发

## 快速参考

### 0. 核心引擎

- `reference/engine.md` - Engine 引擎核心：初始化、场景管理、渲染控制
- `reference/initialization.md` - 引擎初始化、资源配置、百度地图适配器

### 1. 数据管理

- `reference/datasource.md` - DataSource 数据源基类
- `reference/datasource/geojson-datasource.md` - GeoJSON 数据源
- `reference/datasource/json-datasource.md` - JSON 数据源
- `reference/datasource/csv-datasource.md` - CSV 数据源
- `reference/datasource/dataitem.md` - DataItem 数据项

### 2. 点对象与标签

- `reference/simple-point.md` - SimplePoint 简单点
- `reference/effect-point.md` - EffectPoint 特效点（Fan、Bubble、Wave、Breath、Radar 等）
- `reference/marker-types.md` - 标记类型（Icon、BallonPoint、DOMPoint、EffectModelPoint）
- `reference/circle.md` - Circle 圆形（屏幕空间渲染）
- `reference/label.md` - Label 文本/图标标签（功能最丰富）
- `reference/text.md` - Text 文本组件
- `reference/cluster.md` - ClusterPoint 点聚合

### 3. 线与面

- `reference/polyline.md` - Polyline 折线（flat 参数控制渲染模式）
- `reference/simple-line.md` - SimpleLine 简单线
- `reference/wall.md` - Wall 墙体/围栏
- `reference/polygon.md` - Polygon 多边形
- `reference/pillar.md` - Pillar 柱体/椎体

### 4. DOM覆盖物

- `reference/marker.md` - Marker 标记
- `reference/popup.md` - Popup 弹出窗口
- `reference/dom-overlay.md` - DOMOverlay DOM 覆盖物

### 5. 追踪器

- `reference/tracker.md` - 追踪器总览与生命周期
- `reference/path-tracker.md` - PathTracker 路径追踪
- `reference/object-tracker.md` - ObjectTracker 对象追踪
- `reference/orbit-tracker.md` - OrbitTracker 轨道追踪

### 6. 编辑与测量

- `reference/editor.md` - Editor 编辑器（支持点、线、面、圆、矩形绘制和编辑）
- `reference/measure.md` - Measure 测量工具（支持点、线、面测量）

### 7. 3D 模型

- `reference/model.md` - 3D 模型加载（SimpleModel/AnimationModel/LODModel）

### 8. 材质与特效

- `reference/materials.md` - 材质系统（WaterMaterial、ExtendMeshStandardMaterial 等）
- `reference/easing-function.md` - 缓动函数（LINEAR、QUINTIC_IN_OUT、CUBIC_OUT）

### 9. 天空与天气

- `reference/sky-weather.md` - 天空系统（EmptySky/DynamicSky/StaticSky）和天气

### 10. 热力图

- `reference/heatmap.md` - Heatmap 热力图

### 11. 地图图层加载

- `reference/imagery-tile-provider.md` - 影像瓦片加载（Baidu、Tianditu、Bing、OSM、Stadia）
- `reference/vector-tile-provider.md` - 矢量瓦片加载（Baidu、Mapbox）
- `reference/third-party-imagery.md` - 第三方图层接入（WMS、WMTS、XYZ 标准协议）
- `reference/terrain-tile-provider.md` - 地形瓦片加载（Cesium、平面地形）

### 12. LBS 位置服务

- `reference/services.md` - 位置基础服务（地理编码、搜索、路线规划、行政区划等）

### 13. 3DTiles 加载

- `reference/3dtiles-loading.md` - 3D Tiles 加载（Default3DTiles、HDMap3DTiles）

### 14. 基础概念

- `reference/common/coordinate-system.md` - 坐标系：Z-up、投影方式
- `reference/common/event-binding.md` - 事件绑定模式（地图事件绑定和可视化组件事件绑定）

## 关键注意事项

- **引擎初始化**：`new mapvthree.Engine(container, { map: { center: [lng, lat], range: meters } })`
- **坐标系**：Z-up（X-东、Y-北、Z-上），与 Three.js 默认 Y-up 不同
- **视野控制**：使用 `range`（相机距离，米）而非 zoom
- **属性赋值**：使用属性代理 `obj.color = value`，而非 `obj.setColor(value)`
- **MeasureType**：使用 `mapvthree.Measure.MeasureType`
- **图层设置**：通过 `MapView` 设置影像/矢量/地形提供者，而非 `engine.map`
