---
name: cx-design
description: >
  CX 工作流 — 技术设计与 API 契约。当用户提到"技术设计"、"Design Doc"、
  "API 设计"、"接口设计"、"架构设计"、"系统设计"时触发。
  读取 PRD 生成 Design Doc，定义三大强制契约章节：
  API 接口契约、状态枚举对照表、VO/DTO 字段映射。
  保存到本地 .claude/cx/features/{dev_id}-{feature}/design.md。
---

# cx-design: 技术设计与 API 契约

**核心目标**：通过 API 契约（接口路径 + 请求响应 + 状态枚举 + 字段映射）在写代码之前锁死前后端的对齐规范。

## 使用方法

```
/cx-design {功能名}     # 为指定功能生成 Design Doc
/cx-design             # 使用最近的 PRD
```

## 核心步骤

### Step 0: 初始化本地环境

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)
DEVELOPER_ID=$(jq -r '.developer_id' "$PROJECT_ROOT/.claude/cx/config.json" 2>/dev/null || echo "cx")
FEATURE_DIR="$PROJECT_ROOT/.claude/cx/features/${DEVELOPER_ID}-{feature_slug}"
```

### Step 1: 读取 PRD

从本地 `.claude/cx/features/{dev_id}-{feature}/prd.md` 读取需求信息。

### Step 2: 技术栈检测与代码扫描

1. 自动检测技术栈（框架、ORM、API 框架等）
2. 启动 Explore subagent 扫描现有代码：
   - 已有的 API 路由和接口格式
   - 已有的数据模型和命名规范
   - 前端组件结构和状态管理
   - 公共模块和工具函数
   - **与已有 Design Doc 中定义的接口一致性**

3. 扫描接口路径规范（Java `@RequestMapping`、Python `router.get`、TS `api.get` 等）

### Step 3: 生成 Design Doc

**强制性**：包含三大契约章节。

**模板**：

```markdown
# Design Doc: {功能名}

## 关联
- PRD: #{prd_number}
- 相关已有 Design Doc: (如果有)

## 基于现有代码
{代码扫描发现的可复用模块、需要扩展的接口}

## 架构概览
{模块划分、数据流}

## 数据库设计

### 新增/修改表
\`\`\`sql
CREATE TABLE {table_name} (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  {字段} {类型} COMMENT '{说明}',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
\`\`\`

### 字段说明
| 字段 | 类型 | 说明 | 前端对应 |
|------|------|------|---------|
| {field} | {type} | {desc} | {front_field} |

---

## ⚡ API 契约（强制章节）

> **此章节是前后端的对齐合同。exec 阶段必须严格遵守。**

### 接口总览

| # | 方法 | 路径 | 说明 | 认证 |
|---|------|------|------|------|
| 1 | POST | /api/v1/{resource} | {说明} | ✅ |
| 2 | GET | /api/v1/{resource}/{id} | {说明} | ✅ |

### 接口详情

#### 1. {接口名称}

\`\`\`
{METHOD} /api/v1/{path}
Content-Type: application/json
Authorization: Bearer {token}
\`\`\`

**Request Body:**
\`\`\`json
{
  "fieldName": "string",       // 必填
  "anotherField": 0,           // 选填
  "nestedObject": {
    "subField": "string"
  }
}
\`\`\`

**Response (成功):**
\`\`\`json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "fieldName": "string",
    "status": "PENDING",       // → 见状态枚举表
    "createdAt": "2024-01-15T14:30:45"
  }
}
\`\`\`

**Response (失败):**
\`\`\`json
{
  "code": 4001,
  "message": "具体错误说明",
  "data": null
}
\`\`\`

**错误码:**
| code | 含义 | 前端处理 |
|------|------|---------|
| 0 | 成功 | 正常流程 |
| 4001 | {错误1} | {提示方式} |

---

## ⚡ 状态枚举对照表（强制章节）

> **前后端必须使用完全一致的枚举值。此处定义后，exec 阶段不允许修改。**

### {业务领域}状态

| 枚举值 | 后端常量 | API 传输值 | 前端常量 | 显示文本 | 说明 |
|--------|---------|-----------|---------|---------|------|
| 待处理 | PENDING | "PENDING" | 'PENDING' | "待处理" | 初始状态 |
| 处理中 | PROCESSING | "PROCESSING" | 'PROCESSING' | "处理中" | 进行中 |
| 已完成 | COMPLETED | "COMPLETED" | 'COMPLETED' | "已完成" | 最终 |

### 状态流转规则

\`\`\`
PENDING → PROCESSING → COMPLETED
                    ↘ FAILED
\`\`\`

---

## ⚡ VO/DTO 字段映射表（强制章节）

> **此表定义从数据库到前端的完整字段映射链。exec 阶段创建 DTO 和 interface 时必须严格遵循。**

| # | 功能 | 数据库字段 (snake_case) | Java DTO (camelCase) | API JSON | TypeScript | 类型 | 必填 | 说明 |
|---|------|----------------------|--------|-----------|---------|------|------|------|
| 1 | {功能} | {db_field} | {dtoField} | {apiField} | {tsField} | {type} | ✅ | {说明} |

### 命名规范确认
- 数据库: snake_case（`real_name`）
- Java DTO: camelCase（`realName`）
- API JSON: camelCase（Jackson 自动转换）
- TypeScript: camelCase（`realName`）
- 特殊映射: @JsonProperty 或前端转换在此标注

### DTO/VO 类定义

**后端 Java:**
\`\`\`java
@Data
public class {Name}DTO {
  /** {说明} */
  private {Type} {fieldName};
}
\`\`\`

**前端 TypeScript:**
\`\`\`typescript
interface {Name} {
  /** {说明} */
  {fieldName}: {type};
}
\`\`\`

---

## 前端设计
{页面结构、状态管理、关键类型定义}

## 后端设计
{代码路径、关键类、方法签名}

## 影响范围
- 修改的已有文件: {列表}
- 新增文件: {列表}

## 风险点
- {风险1}: {应对方案}
```

保存到 `.claude/cx/features/{dev_id}-{feature}/design.md`。

### Step 4: CLI 确认与调整

显示设计 Doc 摘要，**重点展示三大契约**：

```json
{
  "questions": [
    {
      "question": "Design Doc 和 API 契约是否需要调整？",
      "header": "确认",
      "multiSelect": false,
      "options": [
        {"label": "确认通过", "description": "API 契约无误，创建本地文档"},
        {"label": "调整接口", "description": "接口路径或请求/响应需要修改"},
        {"label": "调整字段", "description": "字段映射或类型需要修改"},
        {"label": "重新生成", "description": "补充信息后重新生成"}
      ]
    }
  ]
}
```

### Step 5: GitHub 同步（可选）

根据 `config.github_sync`：
- **off/local**：仅保存本地
- **collab/full**：创建 GitHub Issue（标签 `doc:design`），记录 Issue 编号

### Step 6: 判断是否需要 ADR

检查 Design Doc 中是否涉及架构决策（新技术、存储方案、通信协议、重大架构变更）。

```json
{
  "questions": [
    {
      "question": "Design Doc 中是否涉及需要记录的架构决策？",
      "header": "ADR",
      "multiSelect": false,
      "options": [
        {"label": "需要 ADR", "description": "有技术选型或架构变更"},
        {"label": "不需要", "description": "没有重大决策"},
        {"label": "稍后补充", "description": "先继续，之后单独创建"}
      ]
    }
  ]
}
```

如果需要，自动触发 `/cx-adr`。

### Step 7: 下一步

```json
{
  "questions": [
    {
      "question": "是否立即创建任务规划？",
      "header": "下一步",
      "multiSelect": false,
      "options": [
        {"label": "立即规划", "description": "运行 /cx-plan"},
        {"label": "稍后处理", "description": "先 review Design Doc"}
      ]
    }
  ]
}
```

如果选择立即规划，自动触发 `/cx-plan {功能名}`。

## 本地文件结构

```
.claude/cx/features/{dev_id}-{feature}/
├── design.md           ← Design Doc
├── design.json         ← Issue 编号、契约元数据
└── ...
```

## Explore Subagent 使用

Step 2 启动代码扫描：

```
Task tool 参数:
  subagent_type: "Explore"
  description: "扫描现有代码结构和接口格式"
  prompt: "列出已有 API 路由、数据模型、组件结构、命名规范"
```

## 三大契约的用处

这三个契约章节在 cx-plan 中会被下沉到各子任务 Issue，使 exec 阶段无需翻阅 Design Doc 即可按契约实现。

## 与其他 Skills 的衔接

- **输入**：prd.md（来自 cx-prd）
- **输出**：design.md（供 cx-adr 和 cx-plan 使用）
- **触发方式**：
  - 来自 cx-prd（M/L 规模自动触发）
  - 用户手动 `/cx-design`
