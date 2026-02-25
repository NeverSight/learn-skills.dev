---
name: feishu-approval
description: 飞书审批流管理 Skill。获取审批定义、提交审批实例、添加评论、转办、撤回。当需要自动化提交审批或管理审批流程时使用此 Skill。
required_permissions:
  - approval:definition
  - approval:approval
  - docs:permission.member:transfer
---

# 飞书审批流管理

你是飞书审批自动化专家，负责通过 Approval v4 API 实现审批的提交、监控、评论与数据检索。

---

## 一、API 基础信息

| 项目 | 值 |
|------|---|
| Base URL | `https://open.feishu.cn/open-apis/approval/v4` |
| 认证方式 | `Authorization: Bearer {tenant_access_token}` |
| Content-Type | `application/json` |

---

## 二、 审批流开发核心指南 (New)

### 1. 消息驱动协作 (Bot Messages)
机器人不仅可以发起审批，还能发送/更新审批相关的卡片消息，实现异步处理：
- **发送审批机器人消息**：`POST /open-apis/approval/v4/messages`
- **更新审批机器人消息**：`PUT /open-apis/approval/v4/messages/{message_id}`
  - *场景*：当审批状态改变时，动态更新用户收到的卡片状态（如“已通过”），减少干扰。

### 2. 高级数据检索与审计 (Audit & Search)
针对大规模审批数据的管理能力：
- **搜索审批定义**：`POST /open-apis/approval/v4/approvals/search`
- **批量获取审批实例**：`POST /open-apis/approval/v4/instances/query`
- **查询抄送列表**：`POST /open-apis/approval/v4/instances/search_cc`
- **查看审批详情 (专用)**：`POST /open-apis/approval/v4/instances/query` (支持通过 ID 定位)
- **精准搜索审批实例**：`POST /open-apis/approval/v4/instances/search` (支持状态、发起人、时间范围等多维审计)

### 3. 事件实时监听 (Events)
订阅以下事件实现自动化闭环：
- `approval.instance.status_changed_v4`：全量感知实例状态变化。
- `approval.task.status_changed_v4`：感知具体节点任务的状态流转。

---

## 三、 典型业务操作

### 1. 获取审批定义
```
GET /open-apis/approval/v4/approvals/{approval_code}
```
**实测心法**：`approval_code` 在管理后台导出。必须先解析表单控件 ID（如 `widget177...`），提交时必须精准匹配。

### 2. 提交审批实例
```
POST /open-apis/approval/v4/instances?user_id_type=user_id
```
```json
{
  "approval_code": "xxx",
  "user_id": "ou_xxx",
  "form": "[{\"id\":\"widget1\",\"type\":\"input\",\"value\":\"说明\"}]"
}
```
**注意**：`user_id` 类型建议优先使用 `user_id`（企业内唯一码）。

### 3. 审批实例检索与审计
```
POST /open-apis/approval/v4/instances/search
```
**Payload 示例**：
```json
{
  "user_id": "ou_xxx",
  "approval_code": "7CC60280...",
  "instance_start_time_from": "1770259200",
  "instance_start_time_to": "1770739200"
}
```

---

## 四、最佳实践

1. **写后必审 (AI Audit)**：机器人发起审批后，应紧随一条评论说明 AI 自动核验的结果，增强审批人的信任感。
2. **状态全链路追踪**：结合 Search 接口定期巡检 P0 级审批，若超时未处理，通过 IM 技能加急提醒。
3. **表单扁平化**：控件 ID 极其冗长（如 `widget177...`），建议在 Skill 配置中硬编码 ID 映射表，提高代码可读性。


---


# feishu-approval 技能总结 (教程脱敏版)

### 一、 核心功能清单

| 功能维度 | 具体能力 | 说明 |
| :--- | :--- | :--- |
| **实例自动发起** | 零代码填单提交 | 支持通过 API 自动填充复杂的审批表单控件（文本、数字、日期等）并一键发起流程。 |
| **高级审计检索** | 多维实例搜索 | 支持按时间范围、状态（审批中/通过/拒绝）、发起人等多维度批量检索审批记录，实现自动化审计。 |
| **动态消息管理** | 审批卡片更新 | 支持发送审批通知并动态更新已有消息卡片的状态，确保审批流状态与用户通知实时同步。 |
| **审计留痕** | AI 决策评论 | 支持在审批单下自动追加 AI 审计评论，提供核验建议，增强人工审批的决策信心。 |
| **全链路监听** | 事件实时感知 | 通过订阅实例状态变更事件，实现从发起、审批到反馈的自动化全闭环。 |

---

### 二、 典型业务场景

**差旅/费用自动审计与报销：**
*   **场景**：员工发送报销指令后，AI 自动生成审批单。同时，AI 利用**高级检索接口**查询该员工当月已有的报销总额，若超过阈值，自动在审批单下添加“超额预警”评论。
*   **价值**：将报销从“被动接收”变为“主动预审”，极大降低了财务部的初审工作量。

**自动化权限巡检与回收：**
*   **场景**：IT 管理员定期触发任务，AI 通过**审批搜索接口**拉取所有已过期的“临时权限申请单”，自动发起对应的权限回收流程。
*   **价值**：确保公司数字资产的访问安全性，实现权限生命周期的闭环管理。

**项目预算动态追踪：**
*   **场景**：当新项目立项审批通过时，AI 自动监听**状态变更事件**，实时同步该项目的预算配额到多维表格看板。
*   **价值**：消除跨部门信息不对称，实现预算执行进度的实时可视化。

---

### 三、 实测注意事项（教程必写 · 尽量详细）

**控件 ID 的“唯一标识” (Critical)：**
*   **风险**：审批表单的控件 ID（如 `widget177...`）是随机生成的。禁止在自动化逻辑中硬编码 ID。
*   **对策**：教程必须强调「定义先行」原则。开发时应先调用 `get_approval_definition` 接口动态获取 Widget ID 列表。

**消息 ID 的“生命周期管理”：**
*   **坑点**：在执行“更新机器人消息卡片”时，必须缓存发送时的 `message_id`。
*   **建议**：建议在数据库或多维表格中建立 `Instance_Code <-> Message_ID` 的映射表，以便后续状态更新时能够精准定位卡片。

**时间戳的“精确审计”：**
*   **注意**：在调用高级搜索接口（`instances/search`）时，时间范围参数需使用**秒级时间戳**。
*   **技巧**：在教程中建议用户在搜索时预留 5-10 分钟的冗余量，以应对服务器间可能存在的同步延迟。

**ID 类型的“全局一致性”：**
*   **注意**：飞书审批对 `user_id` 类型极其挑剔。在调用所有搜索、提交接口时，务必显式声明 `user_id_type`（推荐优先使用企业内唯一的 `user_id`）。

---
*注：以上内容已脱敏。已保存至：`opensource/feishu-skills/feishu-approval/SUMMARY.md`*
