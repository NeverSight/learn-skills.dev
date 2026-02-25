---
name: feishu-bitable
description: 飞书多维表格全能 Skill。覆盖 30+ 项 API：记录 CRUD、字段管理、视图创建、角色权限、公式、关联、统计等。当需要操作飞书多维表格的数据、结构或权限时使用此 Skill。
required_permissions:
  - bitable:app
  - bitable:app:readonly
  - base:app:copy
  - base:dashboard:copy
  - docs:permission.setting:write_only
---

# 飞书多维表格全能手册

你是飞书多维表格自动化专家，负责通过 Bitable API 实现数据操作、结构管理、视图配置和权限控制。

---

## 一、API 基础信息

| 项目 | 值 |
|------|---|
| Base URL | `https://open.feishu.cn/open-apis/bitable/v1` |
| 认证方式 | `Authorization: Bearer {tenant_access_token}` |
| Content-Type | `application/json` |

### 关键参数获取

| 参数 | 获取方式 |
|------|---------|
| `app_token` | 多维表格 URL 中 `/base/` 后面的字符串 |
| `table_id` | 调用列出数据表 API 获取，或从 URL 参数中提取 |

---

## 二、记录操作（CRUD）

### 1. 新增单条记录

```
POST /apps/{app_token}/tables/{table_id}/records
```

```json
{
  "fields": {
    "名称": "测试记录",
    "金额": 100,
    "日期": 1770508800000,
    "状态": "进行中"
  }
}
```

**实测心法**：数值类型不要传字符串，日期必须是 13 位毫秒时间戳。

### 2. 批量新增记录

```
POST /apps/{app_token}/tables/{table_id}/records/batch_create
```

```json
{
  "records": [
    { "fields": { "名称": "记录1" } },
    { "fields": { "名称": "记录2" } }
  ]
}
```

**实测心法**：单次最多 500 条。通过指定唯一索引字段可实现幂等性写入（Upsert）。

### 3. 更新记录

```
PUT /apps/{app_token}/tables/{table_id}/records/{record_id}
```

```json
{
  "fields": { "状态": "已完成" }
}
```

### 4. 批量更新记录

```
POST /apps/{app_token}/tables/{table_id}/records/batch_update
```

**实测心法**：单次请求上限建议控制在 500 条以内。

### 5. 批量删除记录

```
POST /apps/{app_token}/tables/{table_id}/records/batch_delete
```

```json
{ "records": ["rec_1", "rec_2"] }
```

**实测心法**：单次请求上限 500 条。用于自动化清理测试数据或过时流水。

### 6. 查询记录

```
POST /apps/{app_token}/tables/{table_id}/records/search
```

```json
{
  "field_names": ["名称", "金额"],
  "filter": {
    "conjunction": "and",
    "conditions": [
      { "field_name": "状态", "operator": "is", "value": ["进行中"] }
    ]
  },
  "sort": [
    { "field_name": "金额", "desc": true }
  ]
}
```

**实测心法**：Filter 语法较为复杂，建议对照文档调试。

---

## 三、字段类型写入格式（关键）

不同字段类型的数据格式不同，写错格式会导致 API 报错。

### 完整字段类型对照表

| type | ui_type | 中文名 | 写入格式 | 示例 |
|------|---------|--------|---------|------|
| 1 | Text | 多行文本 | 字符串 | `"办公用品"` |
| 1 | Email | 邮箱 | 字符串 | `"test@example.com"` |
| 2 | Number | 数字 | 数值 | `100` |
| 2 | Currency | 货币 | 数值 | `1280.50` |
| 2 | Progress | 进度 | 数值(0~1) | `0.25` |
| 2 | Rating | 评分 | 数值(1~5) | `3` |
| 3 | SingleSelect | 单选 | 字符串 | `"支出"` |
| 4 | MultiSelect | 多选 | 字符串数组 | `["餐饮","交通"]` |
| 5 | DateTime | 日期 | 毫秒时间戳 | `1770508800000` |
| 7 | Checkbox | 复选框 | 布尔值 | `true` |
| 11 | User | 人员 | 对象数组 | `[{"id":"ou_xxx"}]` |
| 13 | Phone | 电话 | 字符串 | `"13800138000"` |
| 15 | Url | 超链接 | 对象 | `{"text":"名称","link":"https://..."}` |
| 17 | Attachment | 附件 | 对象数组 | `[{"file_token":"xxx"}]` |
| 18 | SingleLink | 单向关联 | 字符串数组 | `["recuxxx"]` |
| 21 | DuplexLink | 双向关联 | 字符串数组 | `["recuxxx"]` |
| 22 | Location | 地理位置 | 字符串 | `"116.397,39.903"` |

### 不支持 API 写入的字段类型

以下字段由系统自动维护，**不需要也不能通过 API 写入**：

- 查找引用 (type=19)、公式 (type=20)、创建时间 (type=1001)、最后更新时间 (type=1002)、创建人 (type=1003)、修改人 (type=1004)、自动编号 (type=1005)、按钮 (type=3001)

### 日期字段转换（最常踩坑）

日期必须转为 **13 位毫秒级时间戳**：

```python
import datetime
ts = int(datetime.datetime(2026, 2, 9).timestamp() * 1000)
# → 1770508800000
```

---

## 四、字段管理

### 7. 获取字段列表

```
GET /apps/{app_token}/tables/{table_id}/fields
```

**实测心法**：返回字段的 `type` 和 `ui_name`，是实现"通用适配器"的基础。动态适配不同项目的多维表格结构。

### 8. 新增字段

```
POST /apps/{app_token}/tables/{table_id}/fields
```

```json
{ "field_name": "新字段", "type": 1 }
```

**实测心法**：新增字段后需要几秒钟索引生效。

### 9. 更新字段配置

```
PUT /apps/{app_token}/tables/{table_id}/fields/{field_id}
```

**实测心法**：修改单选/多选字段时需提供完整的 `property` 结构（包含所有选项）。

### 10. 插入公式字段

```
POST /apps/{app_token}/tables/{table_id}/fields
```

```json
{
  "type": 20,
  "field_name": "利润",
  "property": { "formula_expression": "[营收]-[成本]" }
}
```

**实测心法**：公式语法遵循飞书标准，不支持跨表引用。

### 11. 插入关联字段

```
POST /apps/{app_token}/tables/{table_id}/fields
```

```json
{
  "type": 18,
  "field_name": "关联客户",
  "property": { "table_id": "tblXXX", "multiple": true }
}
```

**实测心法**：实现关系型数据库（RDBMS）能力的核心。

---

## 五、数据表管理

### 12. 创建多维表格

```
POST /open-apis/bitable/v1/apps
```

```json
{ "name": "数据库名称" }
```

**实测心法**：Bitable 属于独立应用，路径与 Docx 不同。

### 13. 获取表级元数据

```
GET /apps/{app_token}/tables/{table_id}
```

**实测心法**：包含记录总数、是否有未同步的外部引用等。用于巡检数据库健康度。

### 14. 数据表重命名

```
PATCH /apps/{app_token}/tables/{table_id}
```

```json
{ "name": "新表名" }
```

### 15. 复制多维表格

```
POST /open-apis/drive/v1/files/{file_token}/copy
```

**实测心法**：虽然是 Drive 接口，但适用于 Bitable 文件的整体克隆。新项目立项时从标准模板快速克隆。

---

## 六、视图管理

### 16. 创建看板视图

```
POST /apps/{app_token}/tables/{table_id}/views
```

```json
{ "view_name": "今日看板", "view_type": "kanban" }
```

### 17. 创建甘特视图

```json
{ "view_name": "项目排期", "view_type": "gantt" }
```

**实测心法**：甘特图需指定开始/结束日期字段。

### 18. 创建表单视图

```json
{ "view_type": "form" }
```

**实测心法**：生成后的 URL 可通过机器人分发，客户填完直达数据库。

### 19. 设置视图筛选条件

```
PATCH /apps/{app_token}/tables/{table_id}/views/{view_id}
```

```json
{
  "property": {
    "filter_info": {
      "conditions": [
        { "field_name": "状态", "operator": "is", "value": ["进行中"] }
      ]
    }
  }
}
```

**实测心法**：非常适合做动态 Dashboard。

### 20. 管理视图显示列

```
POST /apps/{app_token}/tables/{table_id}/views/{view_id}/display_fields
```

**实测心法**：通过配置显隐，提升大表的加载与阅读体验。

### 21. 创建仪表盘

```
POST /apps/{app_token}/dashboards/copy
```

**实测心法**：目前主要支持从模板复制。立项后自动搭建数据大屏。

---

## 七、角色与权限

### 22. 获取角色列表

```
GET /apps/{app_token}/roles
```

**实测心法**：自动化审计谁拥有导出权限。企业级安全管控的基石。

### 23. 创建自定义角色

```
POST /apps/{app_token}/roles
```

**实测心法**：需配合 `role_configuration` 精细设置字段权限。可为供应商动态创建"仅可看自己数据"的权限组。

### 24. 角色成员管理

```
POST /apps/{app_token}/roles/{role_id}/members
```

**实测心法**：支持批量添加，大幅降低运维成本。自动将新入职成员加入特定权限组。

### 25. 管理协作权限

权限：`docs:permission.setting:write_only`

**实测心法**：调用云文档通用权限接口即可。项目完结后自动关闭编辑权限转为只读。

---

## 八、统计与高级

### 26. 获取统计信息

```
GET /apps/{app_token}/tables/{table_id}/statistics
```

**实测心法**：比直接拉取记录更轻量。适合定期播报"昨日新增订单数"。

### 27. 自动化工作流触发

**实测心法**：API 写入记录同样能触发多维表格内部的"自动化助手"（无需额外权限）。

---

## 九、附件上传流程

上传文件到多维表格附件字段，需要两步：

**第 1 步：上传文件获取 file_token**

```
POST https://open.feishu.cn/open-apis/drive/v1/medias/upload_all
Content-Type: multipart/form-data

- file: 文件
- file_name: "invoice.jpg"
- parent_type: "bitable_file"
- parent_node: "{app_token}"
- size: 文件大小（字节）
```

**第 2 步：将 file_token 写入附件字段**

```json
{
  "fields": {
    "附件字段名": [{"file_token": "返回的file_token"}]
  }
}
```

---

## 十、错误处理

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| 0 | 成功 | — |
| 1254043 | 无权限 | 在多维表格中添加应用 |
| 1254044 | app_token 无效 | 检查多维表格 URL 中的 token |
| 1254045 | table_id 无效 | 调用列出数据表 API 重新获取 |
| 1254607 | 字段值格式错误 | 检查字段类型和值的格式是否匹配 |
| 99991663 | token 过期 | 重新获取 tenant_access_token |
| 99991400 | 频率限制 | 等待 1 秒后重试 |
