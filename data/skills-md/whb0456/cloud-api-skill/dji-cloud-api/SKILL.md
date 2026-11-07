---
name: dji-cloud-api
description: 大疆上云API（DJI Cloud API）离线全量知识库，抓取自 developer.dji.com 官网 v1.16.1。涵盖基础概念、MQTT Topic、物模型属性与字段枚举、HTTP/WebSocket 接口、DJI WPML 航线格式、DRC 指令飞行、错误码、HMS 告警等全部 145 页官方文档。凡项目涉及大疆机场（Dock 1/2/3）、DJI Pilot 2 接入第三方云、无人机云平台开发、机场任务/航线/直播/媒体/设备管理/固件升级/远程调试/自定义飞行区/一键起飞等问题，直接从本知识库查数据回答，无需访问官网。
---

# DJI 上云API 离线知识库

本 skill 内置大疆上云API官方文档的完整离线快照（v1.16.1，2026-09 抓取自 developer.dji.com，共 145 页，目录在 `references/INDEX.md`）。回答问题时**不要访问官网**，以本库内容为准；仅当本库确实缺少时才告知用户并考虑联网。

## 安装约定

本仓库根目录就是可分发的 skill 包。安装时必须将 `SKILL.md` 与同级的 `references/` 一起复制到 Codex 的 skill 目录，例如项目级 `.agents/skills/dji-cloud-api/` 或用户级 `~/.agents/skills/dji-cloud-api/`。`references/` 中的路径均相对于本文件解析；不要单独复制 `SKILL.md`。

## 查询协议

1. **先定位，再阅读。** 读取 `references/INDEX.md`（总目录：每页列出标题、文件路径、MQTT topic、HTTP 端点、小节名），据此选择 1~3 个最相关文件。
2. **文件太大时用 Grep 缩小范围。** 引用文件按官网目录树组织，路径即可预测：
   - 设备物模型属性 → `references/api-reference/dock-to-cloud/mqtt/aircraft/m30|m3d|m4d-properties.md`（机场侧 OSD）；`references/api-reference/pilot-to-cloud/mqtt/...`（遥控器/飞行器侧 OSD）
   - 机场 MQTT 模块（直播/航线/调试/固件/HMS…）→ `references/api-reference/dock-to-cloud/mqtt/dock/dock1|dock2|dock3/<模块>.md`
   - 云端 HTTP 接口 → `references/api-reference/pilot-to-cloud/https/<域>/<操作>.md`
   - 航线文件格式 → `references/api-reference/dji-wpml/*.md`
3. **回答时注明出处**：给出 md 文件路径；需要时引用文件 frontmatter 中的 `source`（官网 URL）与 `version`。

常用 Grep 锚点：

```bash
# 查某个 MQTT topic / 字段 / 枚举 / 错误码
grep -rn "thing/product/{gateway_sn}/services" references/api-reference/dock-to-cloud/mqtt/
grep -rn "wayline_type\|exec_id\|flighttask_prepare" references/api-reference/dock-to-cloud/mqtt/dock/dock2/
grep -n "319001\|飞行资源不足" references/error-code.md
grep -n "rc_signal_lost_action\|return_to_home" references/api-reference/dock-to-cloud/mqtt/aircraft/m30-properties.md
```

## 目录结构

```
references/
├── INDEX.md                     # 总目录与查询路由（先读这个）
├── overview/                    # 产品介绍/架构/机型支持(枚举)/基础概念(MQTT/物模型/HTTPS/WebSocket/JSBridge)
├── quick-start/                 # 官方 Demo 部署（源码/Docker）
├── feature-set/
│   ├── pilot-feature-set/       # Pilot 上云/态势/直播/地图元素/媒体/航线/日志/DRC/三方App
│   └── dock-feature-set/        # 机场接入/设备管理/直播/媒体/航线/HMS/远程调试/固件/远程日志/DRC/自定义飞行区/多机场/AI识别
├── api-reference/
│   ├── dji-wpml/                # 航线文件格式：template KML + waylines WPML + 公共元素
│   ├── pilot-to-cloud/          # Pilot侧：mqtt(topic+各机型properties)、https(地图元素/航线库/媒体/态势)、websocket推送、jsbridge
│   └── dock-to-cloud/           # 机场侧：mqtt topic定义、飞行器属性(m30/m3d/m4d)、dock1/dock2/dock3各模块
├── debug/                       # Pilot Webview 调试、日志导出、MQTTX 调试
├── error-code.md                # 全量错误码表
├── faq.md                       # 官方 FAQ
├── flight-safety-notification.md
├── tutorial-map.md              # 官方文档阅读指引
└── release-notes.md             # 版本发布记录（v1.16.1 起全部版本）
```

## 查询路由速查

| 用户问什么 | 去哪查 |
| --- | --- |
| 某协议/某概念是什么（物模型、TS/UDP、DRC…） | `overview/basic-concept/*`；专有名词在 `proper-noun.md` |
| 支持哪些机型/负载/枚举（domain、type-subtype-gimbalindex） | `overview/product-support.md` |
| 机场/飞机 OSD 上报哪些字段、怎么设置属性 | `api-reference/dock-to-cloud/mqtt/aircraft/*-properties.md`（机场侧）；`pilot-to-cloud/mqtt/<机型>/properties.md` |
| 某业务怎么实现（直播/航线/媒体/调试流程） | `feature-set/<pilot|dock>-feature-set/*.md`（含 mermaid 时序图） |
| Topic 定义、消息收发模式（services/events/requests/osd/state/drc） | `api-reference/*/mqtt/topic-definition.md` |
| 具体接口的请求/响应 JSON 结构 | 对应模块 md（dock 模块在 `dock1|2|3/`，HTTP 在 `pilot-to-cloud/https/`） |
| 航线 KML/WPML 元素、动作（takeoff_to_safe_point、on_search_task 等） | `api-reference/dji-wpml/*.md` |
| 飞控指令（flyto、一键起飞、云台控制、POI…） | `dock*/drc.md`（DRC）、`pilot-to-cloud/mqtt/<机型>/drc.md` |
| 接口报错码含义 | `error-code.md`（数字 grep）；HMS 告警码在各机场 `hms.md`，告警文案用 `api-reference/dock-to-cloud/mqtt/dock/hms.json`（拼接规则见 `feature-set/dock-feature-set/hms.md`） |
| 某版本新增了什么 | `release-notes.md` |

## 注意事项

- **机型差异大**：dock1/dock2/dock3 与 m30/m3d/m4d 的同名模块内容不同（如 dock3 才有 `media.md`、dock2/3 才有 `remote-control.md`）。回答时确认用户机型，引用对应目录；不明确时列出差异。
- **Topic 变量**：`{gateway_sn}`（网关=机场或遥控器）、`{aircraft_sn}`（飞行器 OSD）、`{device_sn}`、`{workspace_id}` 为占位符，需按实际设备替换。
- 枚举值/属性带"支持产品"标注时以表格行为准；官方标注"已废弃/待废弃"的接口不要推荐（如 `创建航线任务` 已废弃，改用 `下发任务`+`执行任务`）。
- 交互时序图以 ```mermaid 代码块内联保存，可直接展示或转图。
- 快照为 v1.16.1（2026-09）。若用户质疑时效性，可对比 `release-notes.md` 中最新版本条目判断是否需要更新本库。
