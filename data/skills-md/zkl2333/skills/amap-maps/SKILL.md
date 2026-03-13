---
name: amap-maps
description: "高德地图 API（通过 MCP）。地理编码（地址↔坐标）、IP 定位、天气、POI 搜索、路线规划（骑行/步行/驾车/公交）、距离测量。Triggers: '高德', 'amap', '地理编码', 'geocoding', '经纬度', 'POI', '路线规划', '导航'. NOT for: 高德 JSAPI 前端开发（用 AMap-Web/amap-skills）."
---

# 高德地图 Skill

通过 MCP server (`amap-maps`) 调用高德 Web Service API。

## 前置条件

- 在你的 `mcporter.json` 里加入 server 配置（合并到 `mcpServers` 下即可）：

  ```json
  "amap-maps": {
    "command": "npx",
    "args": ["-y", "@amap/amap-maps-mcp-server"],
    "env": {
      "AMAP_MAPS_API_KEY": "YOUR_AMAP_API_KEY"
    }
  }
  ```

- 需要高德 Web Service API Key（环境变量 `AMAP_MAPS_API_KEY`）

## 可用工具

所有工具通过 `mcporter call amap-maps.<tool>` 调用。

### 地理编码
```bash
# 地址 → 坐标
mcporter call amap-maps.maps_geo address="杭州市萧山区"

# 坐标 → 地址（逆地理编码）
mcporter call amap-maps.maps_regeocode location="120.26,30.27"
```

### IP 定位
```bash
mcporter call amap-maps.maps_ip_location ip="114.247.50.2"
```

### 天气
```bash
mcporter call amap-maps.maps_weather city="杭州"
```

### POI 搜索
```bash
# 关键词搜索
mcporter call amap-maps.maps_search_text keywords="咖啡" city="杭州"

# 周边搜索
mcporter call amap-maps.maps_search_around keywords="餐厅" location="120.26,30.27"

# POI 详情
mcporter call amap-maps.maps_search_detail id="B0FFH3V5BN"
```

### 路线规划
```bash
# 驾车
mcporter call amap-maps.maps_direction_driving origin="120.26,30.27" destination="121.47,31.23"

# 步行
mcporter call amap-maps.maps_direction_walking origin="120.26,30.27" destination="120.28,30.29"

# 骑行
mcporter call amap-maps.maps_bicycling origin="120.26,30.27" destination="120.28,30.29"

# 公交（跨城需传 city/cityd）
mcporter call amap-maps.maps_direction_transit_integrated origin="120.26,30.27" destination="121.47,31.23" city="杭州" cityd="上海"
```

### 距离测量
```bash
mcporter call amap-maps.maps_distance origins="120.26,30.27" destination="121.47,31.23"
```

## 坐标格式

高德使用 GCJ-02 坐标系，格式为 `经度,纬度`（注意：经度在前）。

## 使用建议

- 需要坐标时先用 `maps_geo` 把地址转成经纬度
- 配合 `caiyun-weather` skill 使用：先用高德 geocoding 获取坐标，再传给彩云天气
- 高德 API 有 QPS 限制，避免短时间大量请求
