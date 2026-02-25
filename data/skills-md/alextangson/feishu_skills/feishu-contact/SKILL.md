---
name: feishu-contact
description: 飞书组织架构与 ID 转换 Skill。搜索成员、获取部门信息、创建部门、ID 互转（OpenID/UserID/UnionID）。当需要查找飞书用户、管理组织架构或在不同 ID 体系间转换时使用此 Skill。
required_permissions:
  - contact:user.base:readonly
  - directory:department:read
  - directory:department:write
  - directory:employee.create:write
  - directory:employee.idconvert:read
  - directory:department.idconvert:read
  - directory:job_title.base:read
  - directory:place.base:read
  - admin:app.user_usable:readonly
---

# 飞书组织架构与 ID 转换

你是飞书通讯录管理专家，负责通过 Contact v3 API 实现成员搜索、部门管理和 ID 转换。

---

## 一、API 基础信息

| 项目 | 值 |
|------|---|
| Base URL | `https://open.feishu.cn/open-apis/contact/v3` |
| 认证方式 | `Authorization: Bearer {tenant_access_token}` |
| Content-Type | `application/json` |

---

## 二、成员查询

### 1. 搜索成员（通过邮箱/手机号获取 OpenID）

```
GET /open-apis/contact/v3/users/batch_get_id
```

**实测心法**：支持邮箱、手机号等多种输入，是对接外部系统的核心桥梁。

### 2. 获取成员职务

```
GET /open-apis/contact/v3/job_titles/{job_title_id}
```

**实测心法**：职务信息需在管理后台预先维护。可基于职级进行自动化审批路由。

---

## 三、部门管理

### 3. 获取部门信息

```
GET /open-apis/contact/v3/departments/{department_id}
```

**实测心法**：`department_id` 有多种格式（OpenID / CustomID），注意区分。

### 4. 创建部门

```
POST /open-apis/contact/v3/departments
```

```json
{ "name": "新部门", "parent_department_id": "0" }
```

**实测心法**：操作敏感，通常需最高管理权限。建议在预发环境多测试。

### 5. 入职成员

```
POST /open-apis/contact/v3/users
```

```json
{ "name": "张三", "mobile": "13800138000", "department_ids": ["od_xxx"] }
```

**实测心法**：合规性操作，建议在预发环境多测试。

---

## 四、ID 转换（核心）

飞书有三种用户 ID 体系，对接外部系统时经常需要互转：

| ID 类型 | 说明 | 使用场景 |
|---------|------|---------|
| `open_id` | 应用内唯一 | 同一应用内识别用户 |
| `user_id` | 企业内唯一 | 企业内部系统对接 |
| `union_id` | 跨应用唯一 | 同一开发者的多个应用间 |

### 6. 用户 ID 转换

```
POST /open-apis/contact/v3/users/batch_get_id
```

**实测心法**：对接外部系统（如微信、钉钉）时的核心桥梁。

### 7. 部门 ID 转换

```
POST /open-apis/contact/v3/departments/batch_get_id
```

**实测心法**：处理跨企业租户合并时的利器。

---

## 五、其他

### 8. 获取办公地点列表

```
GET /open-apis/contact/v3/places
```

**实测心法**：地点 ID 可用于人员地理分布分析，适配多地办公的项目组。

### 9. 管理外部成员访问

```
GET /open-apis/application/v1/applications/{app_id}/user_usable
```

**实测心法**：控制供应商/外包团队对项目的访问权限，合规性管控的核心。

---

## 六、最佳实践

1. **ID 转换先行**：对接外部系统前，先通过 batch_get_id 建立 ID 映射
2. **权限敏感**：创建部门、入职成员等操作需最高权限，谨慎使用
3. **缓存 ID**：频繁查询的用户 ID 建议本地缓存，减少 API 调用
4. **预发测试**：组织架构变更操作务必在预发环境验证
