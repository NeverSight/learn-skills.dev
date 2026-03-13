---
name: caiyun-weather
description: "Get weather data via Caiyun (彩云天气) API through MCP. Use when: user asks about weather, temperature, forecasts, air quality, or weather alerts for any location in China. Supports realtime, hourly (72h), daily (7d), historical (24h), and alerts. Triggers: '天气', 'weather', '气温', '空气质量', 'AQI', '降水', '预报'. NOT for: locations outside China (use weather skill instead)."
---

# 彩云天气 Skill

通过 MCP server (`caiyun-weather`) 调用彩云天气 v2.6 API，获取高精度天气数据（1km 分辨率，分钟级降水预报）。

## 前置条件

- 在你的 `mcporter.json` 里加入 server 配置（合并到 `mcpServers` 下即可）：

  ```json
  "caiyun-weather": {
    "command": "uvx",
    "args": ["mcp-caiyun-weather"],
    "env": {
      "CAIYUN_WEATHER_API_TOKEN": "YOUR_CAIYUN_API_TOKEN"
    }
  }
  ```

- 需要彩云天气 API token（环境变量 `CAIYUN_WEATHER_API_TOKEN`）

## 常用坐标

- 杭州萧山：`lng=120.26 lat=30.27`

如需其他城市坐标，用 web_search 查询或从用户获取。

## 可用工具

通过 `mcporter call` 调用，所有工具参数均为 `lng`（经度）和 `lat`（纬度）：

### 实时天气
```bash
mcporter call caiyun-weather.get_realtime_weather lng=120.26 lat=30.27
```
返回：温度、湿度、风速风向、降水强度、空气质量（PM2.5/PM10/O3/AQI）、生活指数（紫外线/舒适度）。

### 小时级预报（72h）
```bash
mcporter call caiyun-weather.get_hourly_forecast lng=120.26 lat=30.27
```
返回：逐小时温度、天气现象、降水概率、风速风向。

### 天级预报（7天）
```bash
mcporter call caiyun-weather.get_weekly_forecast lng=120.26 lat=30.27
```
返回：每日温度范围、天气现象、降水概率。

### 历史天气（24h）
```bash
mcporter call caiyun-weather.get_historical_weather lng=120.26 lat=30.27
```

### 天气预警
```bash
mcporter call caiyun-weather.get_weather_alerts lng=120.26 lat=30.27
```
返回：预警标题、代码、状态、描述。

## 天气现象代码（skycon）

| 代码 | 含义 |
|------|------|
| CLEAR_DAY/NIGHT | 晴 |
| PARTLY_CLOUDY_DAY/NIGHT | 多云 |
| CLOUDY | 阴 |
| LIGHT_RAIN | 小雨 |
| MODERATE_RAIN | 中雨 |
| HEAVY_RAIN | 大雨 |
| STORM_RAIN | 暴雨 |
| LIGHT_SNOW | 小雪 |
| MODERATE_SNOW | 中雪 |
| HEAVY_SNOW | 大雪 |
| STORM_SNOW | 暴雪 |
| FOG | 雾 |
| DUST/SAND/WIND | 浮尘/沙尘/大风 |
| HAZE | 霾 |

## 使用建议

- 心跳天气检查优先用 `get_realtime_weather`（一次调用，数据全面）
- 需要判断是否带伞时用 `get_hourly_forecast` 看未来几小时降水概率
- 天气预警用 `get_weather_alerts`，有预警时主动提醒用户
- 彩云 API 有调用频率限制，避免短时间内重复请求
