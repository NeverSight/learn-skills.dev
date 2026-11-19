---
name: cap-tiktok-ip-purchase
description: "指导选择和购买 TikTok 业务所需的目标地区 IP：东南亚优先 911Proxy，欧美优先 Miya 或 IPRoyal，并核对静态住宅、ISP、独享、城市和 ASN 等规格。"
---

# IP 购买

## 工作方式

由课前准备入口发起（课前准备上下文）时，先读取 [课前准备流程控制契约](../cap-tiktok-prep/SKILL.md#流程控制契约全局硬规则)，继承当前步骤、状态和待返回位置。跳过、临时答疑、前置阻塞及结束条件按课前准备入口执行；缺少该依赖时不猜测控制规则、不继续顺序陪跑。模块内按现有 SOP 的独立结果建立固定节点编号，不能用“跳过”一次略过整套流程。

单独使用、没有课前上下文时，不套用课程 P 节点流程、跳过规则和结束祝词，只回答IP 选择与购买；本模块以外的问题简短说明不在本模块范围，交回[总入口](../cap-skill/SKILL.md)。

用途仅限让网络环境稳定并与用户合法注册经营的市场一致；不协助绕过封禁或限制、多账号规避限制、伪造身份或规避平台审核。

读取 [references/purchase-specifications.md](references/purchase-specifications.md)。先确认目标国家、城市、产品类型、ASN、数量和周期，再指导用户核对订单页面；IP 质量检测由 `cap-tiktok-ip-diagnostics` 负责。

## 当前业务口径

- 东南亚：优先 `911Proxy`。
- 欧美：优先 `Miya` 或 `IPRoyal`。
- 优先目标地区匹配、长期稳定、独享的静态住宅或 ISP。
- 避免 Hosting、Datacenter、Cloud、VPS，除非目标产品就是该类型。

购买后只确认 Address、Port、Username、Password、协议类型等字段是否齐全，不要求用户把完整参数发给 AI。
