---
name: generate-tech-proposal
description: |
  生成标准化的技术设计方案文档，包含数据库设计、架构设计、接口设计、业务流程等完整章节。
  使用 Mermaid 绘制 ER 图和流程图。适用于：(1) 创建新功能的技术方案，(2) 规范化现有技术文档，
  (3) 生成符合团队标准的设计文档。触发词：技术方案、设计文档、数据库设计、接口设计、技术设计。
---

# 技术设计方案生成器

生成标准化、结构完整的技术设计方案文档，确保团队技术文档的一致性和完整性。

**重要：默认使用详细格式的 ER 图**，包含完整的表结构、字段类型、约束和注释。

## 快速开始

生成一个完整的技术方案文档，包含以下标准章节：

1. **数据库设计** - 表清单、ER 图、建表 SQL、表关系说明
2. **架构设计** - 系统架构图、技术栈说明
3. **数据模型** - 实体关系、数据权限、多租户隔离
4. **接口设计** - Controller/Service/Mapper 接口规范
5. **核心业务流程** - 业务流程图和说明
6. **功能权限配置** - 权限规则和配置说明

## 文档结构

标准技术方案文档应包含以下章节（按顺序）：

```
# [功能名称] - 技术方案

## 1. 数据库设计
### 1.1 表清单
### 1.2 ER 图
### 1.3 表关系说明
### 1.4 建表 SQL

## 2. 架构设计
### 2.1 系统架构图
### 2.2 技术栈说明

## 3. 数据模型
### 3.1 表关系图
### 3.2 数据权限
### 3.3 多租户隔离
### 3.4 软删除

## 4. 组件接口设计
### 4.1 Controller 接口
### 4.2 Service 接口
### 4.3 Mapper 接口
### 4.4 多语言字段设计（如需要）

## 5. 核心业务流程
### 5.1 [流程1名称]
### 5.2 [流程2名称]
### 5.3 [流程3名称]

## 6. 功能权限配置
```

## 使用流程

### 创建新技术方案

1. **确定功能范围** - 明确要设计的功能模块
2. **设计数据库** - 参考 [references/database-design.md](references/database-design.md)
3. **设计接口** - 参考 [references/api-design.md](references/api-design.md)
4. **设计业务流程** - 参考 [references/business-flow.md](references/business-flow.md)
5. **完善权限配置** - 定义数据权限和操作权限

### 规范化现有文档

1. **检查章节完整性** - 对照标准结构检查缺失章节
2. **统一格式** - 参考 [references/template-overview.md](references/template-overview.md)
3. **补充缺失内容** - 根据各 reference 文件补充标准内容

## 当前业务模块范围约束（强制）

生成技术文档时，必须遵循以下范围规则：

1. 仅对**当前业务模块**进行完整技术设计（数据库、接口、流程、权限）。
2. 非当前业务模块（含外部系统、上下游服务、其他业务域）不在当前文档中体现，不生成“跨模块协作”“外部依赖”“协作边界”等章节或表格。
3. 禁止输出非当前模块的数据库表结构、Service/Mapper 细节、完整业务流程和权限定义。
4. 如输入包含非当前模块背景信息，直接忽略并从文档中移除，不输出任何说明性语句。

## 何时查看 Reference 文件

- **template-overview.md** - 需要了解完整文档结构和各章节作用时
- **database-design.md** - 设计数据库表结构、ER 图、SQL 时
- **api-design.md** - 设计 Controller/Service/Mapper 接口时
- **business-flow.md** - 绘制业务流程图、描述业务逻辑时

## 图表绘制

所有流程图和 ER 图使用 **Mermaid** 语法：

### ER 图格式

**默认使用详细格式**，包含完整表结构、字段类型、约束和注释。

提供两种 ER 图格式，根据场景选择：

#### 1. 详细 ER 图（默认格式，推荐使用）

适用于详细设计文档、代码评审、数据库迁移：

```mermaid
erDiagram
    lead_brand {
        bigint id PK "雪花算法"
        varchar brand_name "品牌名称(区分大小写)"
        varchar brand_country "品牌国家/地区编码"
        varchar brand_status "品牌状态:NORMAL/REVIEWING/REJECTED"
        varchar creator "创建者"
        datetime create_time "创建时间"
        varchar updater "更新者"
        datetime update_time "更新时间"
        tinyint deleted "是否删除:0-否,1-是"
        bigint tenant_id "租户编号"
    }

    lead_customer {
        bigint id PK "雪花算法"
        varchar customer_no UK "客户编号"
        varchar customer_name "客户名称"
        bigint brand_id FK "主关联品牌ID"
        bigint owner_id FK "归属人ID"
        bigint tenant_id "租户编号"
        tinyint deleted "是否删除:0-否,1-是"
    }

    lead_brand ||--o{ lead_customer : "1:N 一品牌关联多客户"
```

**详细 ER 图要点**：
- 字段顺序：主键 → 业务字段 → 标准字段
- 约束标记：PK（主键）、FK（外键）、UK（唯一键）
- 字段注释：枚举值列出所有可能值，外键说明关联表
- 关系定义：在所有表定义后统一定义

#### 2. 简化 ER 图（仅在特殊场景使用）

仅在技术方案初稿、架构讨论等需要快速展示表关系时使用：

```mermaid
erDiagram
    USER ||--o{ ORDER : "1:N 一个用户多个订单"
    ORDER ||--|{ ORDER_ITEM : "1:N 一个订单多个明细"
    PRODUCT ||--o{ ORDER_ITEM : "1:N 一个产品多个订单明细"
```

### 流程图示例

根据技术方案类型选择合适的流程图格式：

**后端业务流程（推荐使用时序图）**：

```mermaid
sequenceDiagram
    participant 用户
    participant Controller
    participant Service
    participant Mapper
    participant DB as 数据库

    用户->>Controller: 发起请求
    Controller->>Service: 调用业务逻辑
    Service->>Mapper: 查询数据
    Mapper->>DB: SQL 查询
    DB-->>Mapper: 返回结果
    Mapper-->>Service: 返回 DO
    Service-->>Controller: 返回 VO
    Controller-->>用户: 返回响应
```

**前端交互流程（推荐使用 flowchart）**：

```mermaid
flowchart TD
    A([用户打开页面]) --> B[输入表单数据]
    B --> C[点击提交]
    C --> D{前端校验}
    D -->|失败| E[显示错误提示]
    E --> B
    D -->|通过| F[调用 API]
    F --> G{请求结果}
    G -->|成功| H[显示成功提示]
    G -->|失败| I[显示错误消息]
    H --> J([结束])
    I --> B
```

## 输出格式

生成的技术方案文档应：

1. **使用 Markdown 格式**
2. **标题层级清晰** - 使用 # ## ### 标记层级
3. **表格规范** - 使用 Markdown 表格语法
4. **代码块标注语言** - SQL 代码使用 ```sql，Java 代码使用 ```java
5. **图表使用 Mermaid** - 所有流程图和 ER 图使用 ```mermaid 代码块
6. **Service/Mapper 接口方法必须带注释** - 每个方法前都要有 `//` 单行注释，禁止输出无注释的方法签名
7. **严格遵守模块边界** - 仅展开当前模块设计，不输出跨模块或外部依赖定义

## 接口注释规范（强制）

在 `4.2 Service 接口` 与 `4.3 Mapper 接口` 章节中，必须满足：

1. 每个方法签名前必须有 `//` 单行注释
2. 注释首行需明确方法业务动作（如：分页查询、详情查询、导出、统计、唯一性校验）
3. 若方法有明显业务约束（如分布式锁、数据权限过滤、状态过滤），应在注释中简要说明
4. 不允许出现“仅方法签名、无注释”的 Service/Mapper 接口代码块

## 质量检查清单

生成文档后，检查以下项目：

- [ ] 所有标准章节都已包含
- [ ] 表清单完整，包含序号、表名、说明
- [ ] ER 图使用 Mermaid 绘制
- [ ] 建表 SQL 完整可执行
- [ ] 接口设计包含请求/响应示例
- [ ] Service 与 Mapper 接口方法均包含 `//` 单行注释
- [ ] 文档仅覆盖当前模块，未展开其他模块内部实现
- [ ] 文档中不存在跨模块协作、外部依赖、协作边界等非当前模块定义
- [ ] 业务流程图清晰易懂
- [ ] 权限配置说明完整

## 示例

参考各 reference 文件中的完整示例。
