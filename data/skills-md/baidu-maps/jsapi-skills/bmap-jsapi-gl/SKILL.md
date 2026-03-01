---
name: bmap-jsapi-gl
description: 百度地图 JSAPI WebGL (BMapGL) 开发指南。在编写、审查或调试使用百度地图 API的代码时应运用此技能。适用于涉及地图初始化、覆盖物渲染、图层管理、事件处理、控件交互或性能优化的任务。当用户提及 BMapGL、百度地图、jsapi-gl或相关地图开发需求时自动触发。
license: MIT
version: 1.0.0
---

# JSAPI GL 开发指南

百度地图 JSAPI WebGL 版本开发指南。包含地图初始化、覆盖物、事件、图层等核心模块的 API 说明和代码示例，旨在帮助开发者快速集成百度地图并遵循正确的使用方式。

## 何时适用

在以下场景中参考这些指南：

- 创建新的地图页面或组件
- 在地图上添加标注、折线、多边形等覆盖物
- 处理地图交互事件（点击、拖拽、缩放等）
- 配置地图样式或切换图层
- 调试地图渲染或性能问题


## 快速参考

### 0. 基础概念

- `references/base-classes.md` - 基础类：Point、Bounds、Size、Pixel、Icon
- `references/constants.md` - 通用常量：搜索状态码、POI 类型

### 1. 地图

- `references/map-init.md` - 地图初始化：资源引入、创建实例、配置选项、交互与视图控制

### 2. 地图覆盖物

- `references/overlay-common.md` - 覆盖物通用操作：添加/移除、显示/隐藏、批量清除
- `references/marker.md` - 点标记：构造参数、位置/图标/旋转/置顶/拖拽方法
- `references/polyline.md` - 折线：构造参数、线条样式、坐标操作、编辑模式
- `references/polygon.md` - 多边形：构造参数、边框/填充样式、带孔多边形、编辑模式
- `references/circle.md` - 圆形：构造参数、中心点/半径、样式设置、编辑模式
- `references/custom-overlay.md` - 自定义覆盖物：DOM 创建、属性传递、事件绑定、旋转控制
- `references/info-window.md` - 信息窗口：构造参数、内容/尺寸设置、最大化、与 Marker 配合使用

### 3. 事件

- `references/map-events.md` - 地图事件：绑定方式、交互事件、视图变化事件、生命周期事件
- `references/overlay-events.md` - 覆盖物事件：通用事件、拖拽事件、矢量图形事件

### 4. 地图样式

- `references/map-style.md` - 个性化地图：自定义地图外观（颜色、显隐），实现深色主题、简洁地图等效果

### 5. 图层服务

- `references/xyz-layer.md` - 第三方图层：加载 XYZ/TMS/WMS/WMTS 标准瓦片
- `references/mvt-layer.md` - 矢量瓦片：加载 MVT/PBF 格式瓦片，支持样式表达式、特征交互、状态管理

### 6. 路径规划

- `references/route-common.md` - 通用配置：构造参数、渲染选项、回调函数、数据结构、状态常量
  - `references/driving-route.md` - 驾车：策略枚举、途经点、路况、收费、拖拽
  - `references/walking-route.md` - 步行：转向类型、拖拽
  - `references/riding-route.md` - 骑行：骑行搜索
  - `references/transit-route.md` - 公交：市内/跨城策略、交通方式、换乘

### 7. 其他LBS服务

- `references/local-search.md` - 本地检索：普通/范围/周边检索、结果处理、翻页、POI 数据结构
- `references/geocoder.md` - 地理编码：正地理编码（地址→坐标）、逆地理编码（坐标→地址）
- `references/convertor.md` - 坐标转换：GPS/高德/谷歌坐标转百度坐标

## 如何使用

请阅读各个参考文件以获取详细说明和代码示例:

```
references/map-init.md
```

每个参考文件包含：

- 功能简要说明
- 完整代码示例及解释
- API 参数说明和注意事项
