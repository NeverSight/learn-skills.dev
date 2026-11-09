---
name: cap-tiktok-shadowrocket-treehole
description: "处理 Shadowrocket 小火箭与树洞订阅链路：二维码导入、节点选择、Socks5 代理添加、Proxy Pass 设置、连接开关和网页连通性验收。"
---

# Shadowrocket 与树洞

## 工作方式

由课前准备入口发起（课前准备上下文）时，先读取 [课前准备流程控制契约](../cap-tiktok-prep/SKILL.md#流程控制契约全局硬规则)，继承当前步骤、状态和待返回位置。跳过、临时答疑、前置阻塞及结束条件按课前准备入口执行；缺少该依赖时不猜测控制规则、不继续顺序陪跑。模块内按现有 SOP 的独立结果建立固定节点编号，不能用“跳过”一次略过整套流程。

单独使用、没有课前上下文时，不套用课程 P 节点流程、跳过规则和结束祝词，只回答小火箭与树洞配置；本模块以外的问题简短说明不在本模块范围，交回[总入口](../cap-skill/SKILL.md)。

用途仅限让网络环境稳定并与用户合法注册经营的市场一致；不协助绕过封禁或限制、多账号规避限制、伪造身份或规避平台审核。

读取 [references/relay.md](references/relay.md)。顺序：[Apple ID](../cap-tiktok-apple-id/SKILL.md) → [IP 购买](../cap-tiktok-ip-purchase/SKILL.md) → 本模块 → [IP 检测](../cap-tiktok-ip-diagnostics/SKILL.md)。单独 IP 参数（Address、Port、Username、Password、协议类型）来自 IP 购买；缺少时先回 IP 购买，不自行编造。引导用户一次完成一个动作，每一步截图确认。

## 关键流程

- 树洞后台选择 iPhone OS 和 Shadowrocket 订阅（资料缺口）。
- 小火箭左上角扫码导入（资料缺口）。
- 展开订阅并选择目标节点（资料缺口）。
- 单独 IP 参数通过右上角 `+` 添加，类型按服务商要求；当前示例为 `Socks5`。
- 填写 Address、Port、Username、Password。
- Proxy Pass 优先选择新加坡或日本树洞节点（资料缺口）。
- 保存后选择代理，打开右上角开关，`Global Routing` 设为 `Proxy`。

标“资料缺口”的步骤在 references 中没有操作资料：只说明步骤名和目标结果，不按经验补写点击路径；卡住时说明“所需资料未提供”，转【船长电商】工作人员。

不在对话中复述完整订阅链接、认证参数、UUID 或密码。
