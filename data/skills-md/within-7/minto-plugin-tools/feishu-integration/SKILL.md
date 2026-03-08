---
name: feishu-integration
description: 飞书（Feishu/Lark）API集成指南。当用户要求"创建飞书应用"、"管理多维表格"、"添加协作者"、"生成飞书报表"、"设置飞书权限"或"自动化飞书操作"时使用。优先使用 MCP 工具进行实时交互操作。
---

# 飞书集成技能

飞书（Feishu/Lark）API 集成和自动化综合指南。

## 🚀 工作方式

本项目提供**两种使用方式**：

### 方式一：MCP 工具（推荐）⚡

**实时交互，无需手动运行脚本**

```
用户请求 → MCP 工具调用 → 飞书 API → 返回结果
```

通过 `mcp__feishu__*` 工具直接操作飞书 API。

**优势**：
- ✅ 实时交互式操作
- ✅ 无需切换终端
- ✅ 自动处理认证
- ✅ 支持链式操作

### 方式二：Python 脚本 📜

适合复杂批量操作和自动化流程。

---

## 🔧 MCP 工具列表

### 认证与连接

| 工具 | 功能 | 使用场景 |
|------|------|---------|
| `mcp__feishu__get_tenant_access_token` | 获取访问令牌 | 验证连接状态 |

### 多维表格管理

| 工具 | 功能 | 参数 |
|------|------|------|
| `mcp__feishu__create_bitable` | 创建多维表格 | `name`: 表格名称<br>`folder_token`: 文件夹（可选） |
| `mcp__feishu__get_tables` | 获取数据表列表 | `app_token`: 应用token |
| `mcp__feishu__add_table_field` | 添加字段 | `app_token`, `table_id`, `field_name`, `field_type` |

### 数据操作

| 工具 | 功能 | 参数 |
|------|------|------|
| `mcp__feishu__add_record` | 添加记录 | `app_token`, `table_id`, `fields` (dict) |
| `mcp__feishu__get_records` | 获取记录 | `app_token`, `table_id`, `page_size` (默认20) |

### 权限管理

| 工具 | 功能 | 参数 |
|------|------|------|
| `mcp__feishu__add_collaborator` | 添加协作者 | `app_token`, `member_type`, `member_id`, `perm_type` |
| `mcp__feishu__get_user_by_email` | 通过邮箱查找用户 | `email`: 用户邮箱 |

### 资源

| 资源 URI | 功能 |
|----------|------|
| `feishu://config` | 获取当前配置信息 |

---

## 💡 典型使用场景

### 场景 1: 创建不同类型多维表格

**你是一个多维表格创建专家，需要按照以下步骤完成任务：**

```
用户请求示例：
- "创建一个客户管理系统"
- "帮我做一个项目任务管理表"
- "建立一个库存管理表格"

助手执行流程：

1. 分析用户需求，设计合理的表格结构
   - 识别业务类型（CRM/项目管理/库存/销售等）
   - 确定核心实体和属性
   - 设计字段关系和数据流

2. 调用 create_bitable 创建多维表格

3. 获取返回的 app_token

4. 调用 get_tables(app_token) 获取 table_id

5. 调用 add_table_field() 添加字段：[根据需求动态生成]
   - 主表：核心业务字段
   - 字段类型选择（文本/数字/日期/单选/多选/人员等）
   - 必填字段和默认值设置

6. 设置字段类型、选项、验证规则
   - 单选字段：配置选项列表
   - 数字字段：设置范围限制
   - 日期字段：配置时间格式
   - 关联字段：建立表间关系

7. 添加示例数据

8. 添加用户为协作者

9. 创建关联表（如需要）
   - 子表设计（如订单明细、任务评论）
   - 表间关联配置
   - 数据关系说明
```

**示例：创建客户管理系统**

```
用户: 创建一个客户管理系统

助手执行：

1. 分析需求
   - 业务类型：CRM 客户管理
   - 核心实体：客户、跟进记录
   - 数据流：客户信息 → 跟进互动 → 成交转化

2. 调用 create_bitable(name="客户管理系统")

3. 获取返回的 app_token（例如：app_xxxxxxxxx）

4. 调用 get_tables(app_token) 获取 table_id（例如：tblxxxxxxxx）

5. 调用 add_table_field() 添加字段：
   - 客户名称（field_name="客户名称", field_type=1）文本
   - 联系人姓名（field_name="联系人姓名", field_type=1）文本
   - 联系电话（field_name="联系电话", field_type=11）电话
   - 客户来源（field_name="客户来源", field_type=3）单选
   - 客户阶段（field_name="客户阶段", field_type=3）单选
   - 所属行业（field_name="所属行业", field_type=3）单选
   - 预估成交金额（field_name="预估成交金额", field_type=2）数字
   - 创建时间（field_name="创建时间", field_type=5）日期
   - 备注（field_name="备注", field_type=1）文本

6. 设置字段配置
   - 客户来源选项：网络推广/客户介绍/展会/主动开发
   - 客户阶段选项：潜在客户/意向客户/谈判中/已成交/已流失
   - 所属行业选项：互联网/金融/制造/零售/其他
   - 预估金额：设置最小值为0

7. 添加示例数据
   调用 add_record(app_token, table_id, {
     "客户名称": "示例科技公司",
     "联系人姓名": "张三",
     "联系电话": "13800138000",
     "客户来源": "网络推广",
     "客户阶段": "意向客户",
     "所属行业": "互联网",
     "预估成交金额": 50000,
     "创建时间": 1704067200000,
     "备注": "潜在优质客户"
   })

8. 添加用户为协作者
   调用 get_user_by_email(email="user@example.com") 获取 open_id
   调用 add_collaborator(app_token, "user", open_id, "edit")

9. 创建关联表"跟进记录"
   重复步骤 4-5，创建跟进记录表，包含：
   - 跟进时间（field_type=5）
   - 跟进方式（field_type=3，选项：电话/微信/邮件/面谈）
   - 跟进内容（field_type=1）
   - 下次跟进时间（field_type=5）
   - 客户名称（关联字段，关联到客户信息表）

10. 返回结果
   - 表格链接：https://feishu.cn/base/{app_token}
   - 字段说明文档
   - 使用建议
```

**示例：创建项目任务管理表**

```
用户: 创建一个项目任务管理表

助手执行：

1. 分析需求
   - 业务类型：项目管理
   - 核心实体：项目、任务
   - 数据流：项目分解 → 任务分配 → 执行跟踪

2. 调用 create_bitable(name="项目任务管理系统")

3. 获取返回的 app_token

4. 调用 get_tables(app_token) 获取 table_id

5. 调用 add_table_field() 为"项目列表"表添加字段：
   - 项目名称（field_name="项目名称", field_type=1）
   - 项目编号（field_name="项目编号", field_type=1）
   - 项目状态（field_name="项目状态", field_type=3）选项：未开始/进行中/已完成/已延期
   - 开始日期（field_name="开始日期", field_type=5）
   - 结束日期（field_name="结束日期", field_type=5）
   - 项目优先级（field_name="项目优先级", field_type=3）选项：高/中/低
   - 项目进度（field_name="项目进度", field_type=15）0-100%
   - 项目经理（field_name="项目经理", field_type=1）

6. 添加示例数据
   调用 add_record() 添加 2-3 个示例项目

7. 添加用户为协作者

8. 创建"任务列表"关联表
   - 任务名称（field_type=1）
   - 所属项目（关联字段 → 项目列表）
   - 任务负责人（field_type=1）
   - 任务状态（field_type=3）选项：待办/进行中/已完成/已取消
   - 任务优先级（field_type=3）选项：紧急/高/中/低
   - 开始时间（field_type=5）
   - 截止时间（field_type=5）
   - 预计工时（field_type=2）
   - 实际工时（field_type=2）
   - 任务描述（field_type=1）

9. 返回双表结构说明、关联关系图、使用建议
```

**示例：创建采购订单管理系统**

```
用户: 创建一个采购订单管理系统

助手执行：

1. 分析需求
   - 业务类型：采购管理
   - 核心实体：采购订单
   - 数据流：订单创建 → 审批 → 执行

2. 调用 create_bitable(name="采购订单管理系统")

3. 获取返回的 app_token

4. 调用 get_tables(app_token) 获取 table_id

5. 调用 add_table_field() 添加字段：
   - 采购订单（field_name="采购订单", field_type=1）
   - 采购单价（field_name="采购单价", field_type=2）
   - 采购数量（field_name="采购数量", field_type=2）
   - 采购金额（field_name="采购金额", field_type=2）
   - 采购时间（field_name="采购时间", field_type=5）
   - 采购人（field_name="采购人", field_type=1）

6. 添加示例数据
7. 添加用户为协作者
8. 返回表格链接和使用说明
```

### 场景 2: 批量导入数据

```
用户: 向表格 xyz 添加 10 条采购记录

助手:
1. 调用 get_tables(app_token) 确认 table_id
2. 循环调用 add_record() 添加数据
3. 返回添加结果
```

### 场景 3: 权限管理

```
用户: 添加 user@example.com 为表格管理员

助手:
1. 调用 get_user_by_email(email="user@example.com") 获取 open_id
2. 调用 add_collaborator(
   app_token="...",
   member_type="user",
   member_id="<open_id>",
   perm_type="full_access"
)
```

---

## 🤖 智能表格类型识别

支持识别以下业务类型：

| 业务类型 | 关键词 | 预设字段 |
|---------|--------|---------|
| 客户管理 | CRM、客户、销售、客户管理 | 客户名称、联系人、阶段、金额 |
| 项目管理 | 项目、任务、项目任务 | 项目名称、状态、负责人、进度 |
| 采购管理 | 采购、订单、供应商 | 订单号、单价、数量、金额 |
| 库存管理 | 库存、仓库、商品 | 商品名称、SKU、库存量、位置 |
| 人事管理 | 员工、考勤、招聘 | 姓名、部门、职位、状态 |
| 费用管理 | 报销、费用、审批 | 报销人、金额、类型、日期 |

---

## 📋 字段类型说明

| 类型值 | 类型名称 | 说明 |
|--------|----------|------|
| 1 | text | 文本 |
| 2 | number | 数字 |
| 3 | select | 单选 |
| 4 | multiSelect | 多选 |
| 5 | dateTime | 日期 |
| 7 | attachment | 附件 |
| 11 | phone | 电话 |
| 12 | email | 邮箱 |
| 13 | url | 网址 |
| 15 | progress | 进度 |

---

## 🔐 权限类型说明

- `view` - 仅查看
- `edit` - 编辑权限
- `full_access` - 完全管理权限

---

## 📁 项目结构

```
feishu-integration/
├── plugin.json              # 插件清单
├── SKILL.md                 # 本文档
├── mcp-server/              # MCP 服务器
│   ├── index.py             # FastMCP 实现
│   ├── requirements.txt     # Python 依赖
│   └── README.md            # MCP 文档
├── scripts/                 # Python 脚本（备用）
│   ├── create_feishu_app.py
│   ├── create_purchase_order_bitable.py
│   ├── add_feishu_collaborator.py
│   └── ...
└── .mcp.json                # MCP 配置
```

---

## 🛠️ 配置说明

### MCP 服务器配置

确保 `~/.minto/config/mcp.json` 包含：

```json
{
  "mcpServers": {
    "feishu": {
      "command": "python3.11",
      "args": ["/path/to/mcp-server/index.py"],
      "env": {
        "FEISHU_APP_ID": "your_app_id",
        "FEISHU_APP_SECRET": "your_app_secret"
      }
    }
  }
}
```

### 环境变量

- `FEISHU_APP_ID`: 飞书应用ID
- `FEISHU_APP_SECRET`: 飞书应用密钥

获取方式：
1. 访问 https://open.feishu.cn
2. 创建应用或选择已有应用
3. 在"凭证与基础信息"页面获取

---

## 🔍 故障排查

### MCP 工具不可用

1. 检查 MCP 服务器是否启动：
   ```bash
   minto mcp list
   ```

2. 检查环境变量是否配置：
   ```bash
   minto mcp get feishu
   ```

3. 查看 MCP 配置文件：
   ```bash
   cat ~/.minto/config/mcp.json
   ```

### API 返回 404

- 确保在飞书开放平台启用了相关权限
- 重新发布应用并等待权限生效（约10分钟）

### 添加协作者失败

应用需要以下权限：
- `permission:permission.member.create`
- 或权限包："分享云文档"

---

## 📚 Python 脚本使用（备用）

如果需要使用脚本方式：

```bash
cd scripts
python3 create_feishu_app.py
python3 add_feishu_collaborator.py
```

依赖安装：
```bash
pip install requests lark-oapi
```

---

## ✅ 最佳实践

1. **优先使用 MCP 工具**进行交互式操作
2. **批量操作使用脚本**提高效率
3. 创建表格后**及时添加自己为协作者**
4. **验证权限**：先用 `get_tenant_access_token` 测试连接
5. **保存 app_token**：创建的表格 token 需保存以便后续操作

---

## 🔗 参考文档

- [飞书开放平台](https://open.feishu.cn/document)
- [多维表格 API](https://open.feishu.cn/document/server-docs/docs/bitable-v1/app-list)
- [权限管理 API](https://open.feishu.cn/document/server-docs/docs/permission-v2/permission/add_member)

---

## 💻 开发者

- GitHub: https://github.com/Within-7/minto-plugin-tools
- MCP 服务器: FastMCP 2.12.2
- Python: 3.11+
