---
name: feishu-bitable
description: 操作飞书多维表格(Bitable)，支持数据表、记录、字段和素材管理。何时使用：当用户说"飞书多维表格"/"飞书表格"/"bitable"，或需要读写表格记录、操作数据表结构、管理字段、上传素材时。
metadata:
  author: "AI Assistant"
  updated: "2026-02-24 12:00:00"
  version: "1.0.0"
---

# 飞书多维表格 API 操作

为 AI 大模型提供处理飞书多维表格的完整能力，支持操作数据表、记录、字段和素材。

## 技能开发者的环境

node --version v24.13.0

## ⚠️ 重要：关于代码混淆

本技能的 `scripts/` 目录下的所有 JavaScript 文件已进行代码混淆处理。

### AI 行为准则

✅ **可以执行**：直接调用和执行这些脚本，使用 `--parameter-file-path` 传递参数

❌ **不要读取**：不要读取或分析 `scripts/` 目录下的 `.js` 文件内容，原因：

- 混淆代码可读性极差，无实际意义
- 避免浪费 token 和时间
- 所有功能说明已在本文档和 `references/` 目录中完整描述

### 遇到问题时

- 参考 `references/` 目录下的文档
- 查看脚本输出的错误信息和错误码
- 不要尝试阅读混淆代码

## 🎯 触发映射：用户说 → AI 做

| 用户输入触发词                   | AI 执行动作                                   | 对应脚本                             |
| -------------------------------- | --------------------------------------------- | ------------------------------------ |
| "查看记录"/"获取记录"/"列出记录" | 运行 `record/get.js` 查询记录列表             | `scripts/record/get.js`              |
| "添加记录"/"创建记录"/"插入记录" | 运行 `record/create.js` 创建单条记录          | `scripts/record/create.js`           |
| "修改记录"/"更新记录"/"编辑记录" | 运行 `record/update.js` 更新单条记录          | `scripts/record/update.js`           |
| "删除记录"/"移除记录"            | 运行 `record/delete.js` 删除单条记录          | `scripts/record/delete.js`           |
| "批量添加记录"/"添加多条记录"    | 运行 `record/batch-create.js` 批量创建记录    | `scripts/record/batch-create.js`     |
| "批量修改记录"/"更新多条记录"    | 运行 `record/batch-update.js` 批量更新记录    | `scripts/record/batch-update.js`     |
| "批量删除记录"/"清空记录"        | 运行 `record/batch-delete.js` 批量删除记录    | `scripts/record/batch-delete.js`     |
| "查看表格"/"数据表列表"          | 运行 `table/list.js` 列出所有数据表           | `scripts/table/list.js`              |
| "创建表格"/"添加数据表"          | 运行 `table/create-single.js` 创建单个数据表  | `scripts/table/create-single.js`     |
| "修改表格名称"/"重命名表格"      | 运行 `table/update.js` 更新数据表名称         | `scripts/table/update.js`            |
| "删除表格"/"移除数据表"          | 运行 `table/delete-one.js` 删除单个数据表     | `scripts/table/delete-one.js`        |
| "查看字段"/"列信息"              | 运行 `field/list.js` 列出所有字段             | `scripts/field/list.js`              |
| "添加字段"/"新列"                | 运行 `field/create.js` 创建字段               | `scripts/field/create.js`            |
| "修改字段"/"修改列"              | 运行 `field/update.js` 更新字段               | `scripts/field/update.js`            |
| "删除字段"/"移除列"              | 运行 `field/delete.js` 删除字段               | `scripts/field/delete.js`            |
| "上传文件"/"上传图片"/"上传附件" | 运行 `media/upload.js` 上传素材               | `scripts/media/upload.js`            |
| "获取下载链接"/"获取直链"        | 运行 `media/file-token-to-url.js` 获取文件URL | `scripts/media/file-token-to-url.js` |

## 决策流程

```
用户请求涉及飞书多维表格？
    │
    ├─ 是 → 检查具体操作类型
    │       │
    │       ├─ 需要访问凭证？
    │       │   └─ 运行 get-tenant-access-token.js
    │       │
    │       ├─ 需要从URL解析信息？
    │       │   └─ 运行 parse-bitable-url.js
    │       │
    │       └─ 执行具体操作
    │           ├─ 数据表操作 → table/ 脚本
    │           ├─ 记录操作 → record/ 脚本
    │           ├─ 字段操作 → field/ 脚本
    │           └─ 素材操作 → media/ 脚本
    │
    └─ 否 → 不使用此 Skill
```

## 如何使用这个 Skill

### 功能概述

本 Skill 提供完整的飞书多维表格 API 操作能力：

| 功能模块       | 支持的操作                                     |
| -------------- | ---------------------------------------------- |
| **数据表管理** | 创建、更新、删除数据表（支持批量操作）         |
| **记录操作**   | 增删改查记录，支持批量操作（单次最多 1000 条） |
| **字段管理**   | 创建、更新、删除字段，列出所有字段             |
| **素材上传**   | 上传文件、图片等素材，获取临时下载链接         |

### 输出格式

执行完成后，Skill 会输出：

- **成功**：返回操作结果数据（JSON 格式），包含完整的 API 响应
- **失败**：返回错误信息，包含错误码和解决建议

### 前置要求

1. **有效的 `tenant_access_token`**：所有 API 操作都需要
2. **`app_token`**：标识要操作的多维表格
3. **`table_id`**：标识要操作的数据表（部分操作需要）

### 参数传递方式

**注意**：本 Skill 所有脚本均使用 `--parameter-file-path` 参数传递配置，必须通过参数文件方式调用。

**AI 调用规范**：本 Skill 专为 AI 设计，AI 自动处理临时文件的创建和清理，人类用户只需用自然语言描述需求。

### AI 自动处理临时文件流程

AI 调用本 Skill 时，必须遵循以下流程自动管理临时文件：

```javascript
import { createTempParamsFile, cleanupTempFile } from "./scripts/utils";
import { execSync } from "child_process";

// 1. 创建临时参数文件（自动存放在系统临时目录）
const tempFile = createTempParamsFile(
  {
    tenant_access_token: "xxx",
    app_token: "xxx",
    table_id: "xxx"
    // ... 其他参数
  },
  "operation-name"
);

try {
  // 2. 执行脚本
  const result = execSync(`node scripts/xxx.js --parameter-file-path "${tempFile}"`, { encoding: "utf-8" });
  const data = JSON.parse(result);

  // 3. 处理结果并返回给用户
  return formatResultForUser(data);
} finally {
  // 4. 确保清理临时文件（无论成功或失败）
  cleanupTempFile(tempFile);
}
```

**关键原则**：

- ✅ 临时文件必须创建在系统临时目录（`os.tmpdir()`）
- ✅ 脚本执行完成后立即清理临时文件
- ✅ 使用 `try...finally` 确保即使出错也会清理
- ❌ 不要将参数文件创建在技能目录或用户工作目录

### 标准使用流程

**步骤 1：获取访问凭证**

```bash
node scripts/get-tenant-access-token.js --parameter-file-path params.json
```

参数文件示例 (`params.json`):

```json
{
  "appId": "cli_xxx",
  "appSecret": "xxx"
}
```

详细凭证管理规则参见 [认证与凭证管理指南](references/authentication.md)。

**步骤 2：解析多维表格 URL**

从 URL 中提取 `app_token` 和 `table_id`：

```bash
node scripts/parse-bitable-url.js --parameter-file-path params.json
```

**步骤 3：执行具体操作**

根据需求选择对应的脚本：

```bash
# 查询记录
node scripts/record/get.js --parameter-file-path "params.json"

# 创建记录
node scripts/record/create.js --parameter-file-path "params.json"

# 批量创建记录
node scripts/record/batch-create.js --parameter-file-path "params.json"
```

## 核心概念

| 概念                   | 说明                                                     |
| ---------------------- | -------------------------------------------------------- |
| **多维表格 (Bitable)** | 字节跳动的产品，结合电子表格的灵活性和数据库的结构化特性 |
| **数据表 (Table)**     | 多维表格中的单个表格，类似 Excel 工作表                  |
| **记录 (Record)**      | 数据表中的一行数据                                       |
| **字段 (Field)**       | 数据表中的一列的表头，用于设定该列的数据类型             |
| **素材 (Media)**       | 上传的文件、图片、视频等                                 |

## 操作接口速查

### 基础操作

| Action                | 脚本路径                                                         | 说明                                           |
| --------------------- | ---------------------------------------------------------------- | ---------------------------------------------- |
| 获取访问凭证          | [get-tenant-access-token.js](scripts/get-tenant-access-token.js) | 获取 `tenant_access_token`                     |
| 解析飞书多维表格的URL | [parse-bitable-url.js](scripts/parse-bitable-url.js)             | 从 URL 提取 `app_token`、`table_id`、`view_id` |

### 数据表操作

| Action         | 脚本路径                                           | 说明                                |
| -------------- | -------------------------------------------------- | ----------------------------------- |
| 新增一个数据表 | [create-single.js](scripts/table/create-single.js) | 支持指定名称、视图和字段            |
| 新增多个数据表 | [batch-create.js](scripts/table/batch-create.js)   | 仅可指定数据表名称                  |
| 更新数据表名称 | [update.js](scripts/table/update.js)               | 更新指定数据表的名称                |
| 列出数据表     | [list.js](scripts/table/list.js)                   | 获取所有数据表的 ID、版本号和名称   |
| 删除一个数据表 | [delete-one.js](scripts/table/delete-one.js)       | 通过 `app_token` 和 `table_id` 删除 |
| 删除多个数据表 | [batch-delete.js](scripts/table/batch-delete.js)   | 批量删除多个数据表                  |

详细参数参见 [table 参考文档](references/table/) 目录。

### 记录操作

| Action       | 脚本路径                                          | 说明                          |
| ------------ | ------------------------------------------------- | ----------------------------- |
| 新增记录     | [create.js](scripts/record/create.js)             | 在数据表中新增一条记录        |
| 更新记录     | [update.js](scripts/record/update.js)             | 更新数据表中的一条记录        |
| 查询记录     | [get.js](scripts/record/get.js)                   | 单次最多查询 500 行，支持分页 |
| 删除记录     | [delete.js](scripts/record/delete.js)             | 删除数据表中的一条记录        |
| 新增多条记录 | [batch-create.js](scripts/record/batch-create.js) | 单次最多新增 1,000 条         |
| 更新多条记录 | [batch-update.js](scripts/record/batch-update.js) | 单次最多更新 1,000 条         |
| 批量获取记录 | [batch-get.js](scripts/record/batch-get.js)       | 通过记录 ID 查询，最多 100 条 |
| 删除多条记录 | [batch-delete.js](scripts/record/batch-delete.js) | 批量删除多条记录              |

详细参数参见 [record 参考文档](references/record/) 目录。

### 字段操作

| Action   | 脚本路径                             | 说明                              |
| -------- | ------------------------------------ | --------------------------------- |
| 新增字段 | [create.js](scripts/field/create.js) | 在数据表中新增一个字段            |
| 更新字段 | [update.js](scripts/field/update.js) | 全量更新字段（property 会被覆盖） |
| 列出字段 | [list.js](scripts/field/list.js)     | 获取数据表中的所有字段            |
| 删除字段 | [delete.js](scripts/field/delete.js) | 删除数据表中的一个字段            |

详细参数参见 [field 参考文档](references/field/) 目录。

### 素材/文件操作

| Action   | 脚本路径                                                   | 说明                                      |
| -------- | ---------------------------------------------------------- | ----------------------------------------- |
| 素材上传 | [upload.js](scripts/media/upload.js)                       | 上传文件、图片、视频等素材                |
| 获取直链 | [file-token-to-url.js](scripts/media/file-token-to-url.js) | `file_token` 转临时下载链接（24小时有效） |

详细参数参见 [media 参考文档](references/media/) 目录。

## 文件和目录使用说明

| 项目     | 说明                                                            |
| -------- | --------------------------------------------------------------- |
| 文档位置 | `references/` 目录下的文档，有具体的 API 调用命令或脚本执行方式 |
| 脚本位置 | `scripts/` 目录下的 Node.js 脚本直接使用                        |
| 临时文件 | **系统临时目录** (`%TEMP%` 或 `/tmp`)，操作完成后自动删除       |
| 参数文件 | **系统临时目录**，使用绝对路径引用                              |
| 上传记录 | **系统临时目录** (`feishu-bitable-upload-records.json`)         |

### 临时文件管理最佳实践

本技能所有临时文件（参数文件、上传记录）均存放在系统临时目录，避免污染用户主目录和技能目录：

**Windows 示例**：

```
C:\Users\xxx\AppData\Local\Temp\feishu-create-record-1740374400000-a7x9k2.json
C:\Users\xxx\AppData\Local\Temp\feishu-bitable-upload-records.json
```

**Linux/Mac 示例**：

```
/tmp/feishu-create-record-1740374400000-a7x9k2.json
/tmp/feishu-bitable-upload-records.json
```

### 工具函数使用示例

```javascript
import { createTempParamsFile, cleanupTempFile, cleanupAllTempFiles } from './utils';

// 1. 创建临时参数文件（自动存放在系统临时目录）
const params = {
  tenant_access_token: 'xxx',
  app_token: 'xxx',
  table_id: 'xxx',
  fields: { ... }
};
const tempFilePath = createTempParamsFile(params, 'create-record');

// 2. 执行脚本
const result = await executeScript(tempFilePath);

// 3. 立即清理临时文件
cleanupTempFile(tempFilePath);

// 4. 清理所有过期的临时文件（24小时前的）
cleanupAllTempFiles();
```

**临时文件命名规范**：

- 格式：`feishu-{operation}-{timestamp}-{random}.json`
- 示例：`feishu-batch-create-1740374400000-a7x9k2.json`

**清理策略**：

- 成功或失败都立即尝试删除参数文件
- 删除失败不影响主流程
- 系统临时目录自动定期清理
- 运行 `cleanupAllTempFiles()` 批量清理过期文件（24小时前）

## AI 处理示例

**用户说**："帮我在飞书表格 https://xxx.feishu.cn/wiki/xxx 里添加一条记录，任务名称是'完成报告'，进度50%"

**AI 执行步骤**：

| 步骤 | 执行动作                            | 脚本/命令                                         |
| ---- | ----------------------------------- | ------------------------------------------------- |
| 1    | 检查 tenant_access_token            | 如无则运行 `get-tenant-access-token.js`           |
| 2    | 解析 URL 获取 app_token 和 table_id | 运行 `parse-bitable-url.js`                       |
| 3    | 创建临时参数文件                    | 运行 `createTempParamsFile()`，存放在系统临时目录 |
| 4    | 创建记录                            | 运行 `record/create.js`                           |
| 5    | 清理临时参数文件                    | 运行 `cleanupTempFile()`                          |
| 6    | 返回结果                            | 向用户返回："已成功创建记录！记录ID: recxxx"      |

**用户感知**：完全不需要知道临时文件的存在，只需自然语言交互。

## 错误处理

| 错误场景         | 错误表现                                                     | 处理方式                                               |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------ |
| 缺少访问凭证     | API 返回 401/403 错误                                        | 运行 `get-tenant-access-token.js` 获取凭证             |
| 访问凭证过期     | API 返回 错误代码: 99991663, 错误信息: Invalid access token for authorization | 运行 `get-tenant-access-token.js` 获取凭证             |
| URL 解析失败     | 无法提取 app_token/table_id                                  | 检查 URL 格式是否正确，或手动提供参数                  |
| 记录不存在       | API 返回 404 错误                                            | 检查 record_id 是否正确，或先运行 `record/get.js` 查询 |
| 字段类型不匹配   | API 返回 400 错误                                            | 运行 `field/list.js` 查看字段类型，调整参数后重试      |
| 文本字段格式错误 | `TextFieldConvFail` 错误                                     | 文本字段使用字符串格式，不要用富文本数组格式           |
| 字段更新缺少参数 | `field validation failed`                                    | 更新字段时必须提供 `type` 参数                         |
| 文件token格式错  | `Cannot read properties`                                     | 使用 `file_tokens`（数组）而非 `file_token`（字符串）  |
| 批量操作超限     | API 返回 422 错误                                            | 减少单次操作数量（记录最多1000条，批量获取最多100条）  |
| 临时文件创建失败 | 磁盘空间不足或权限问题                                       | 检查系统临时目录权限和磁盘空间                         |
| 网络超时         | 请求无响应                                                   | 检查网络连接，稍后重试                                 |

### 常见错误详解

#### 1. 文本字段格式错误 (TextFieldConvFail)

**错误信息**：`the value of 'Multiline' must be a string`

**原因**：创建/更新记录时，文本字段使用了查询返回的富文本数组格式

**解决**：

- ❌ 错误：`"字段名": [{"text": "内容", "type": "text"}]`
- ✅ 正确：`"字段名": "内容"`

#### 2. 字段更新缺少 type 参数

**错误信息**：`field validation failed - type is required`

**原因**：更新字段时未提供 `type` 参数

**解决**：更新字段时必须包含 `type`，如 `"type": 1`（1=文本, 2=数字）

#### 3. 获取文件下载链接参数错误

**错误信息**：`Cannot read properties of undefined (reading 'map')`

**原因**：使用了 `file_token` 而不是 `file_tokens`

**解决**：

- ❌ 错误：`"file_token": "xxx"`
- ✅ 正确：`"file_tokens": ["xxx"]`

## 参考文档

| 文档                                                      | 说明                                                                              |
| --------------------------------------------------------- | --------------------------------------------------------------------------------- |
| [认证与凭证管理指南](references/authentication.md)        | 详细的凭证管理说明，包括 App ID/App Secret 获取、tenant_access_token 自动获取流程 |
| [获取访问凭证 API](references/get_tenant_access_token.md) | 获取 tenant_access_token 的具体 API 调用说明和脚本使用方法                        |
| [解析飞书 URL 工具](references/parse_bitable_url.md)      | 从飞书多维表格 URL 中提取 app_token、table_id、view_id 的工具使用说明             |
| [常见错误及解决方案](references/errors.md)                | API 调用常见错误码及排查方法                                                      |
| [参数配置示例与最佳实践](references/examples.md)          | 各种操作场景的参数配置示例                                                        |
