---
name: hap-api-doc-updater
description: 专门用于维护和更新明道云 HAP 接口文档的技能。当用户需要在 HAP API 文档中新增、修改、删除接口,或需要同步中英文版本文档时使用此技能。支持组织授权 API (en/zh-Hans) 和应用 API (application) 两种文档类型。
---

# HAP API 文档更新器

此技能专门用于维护和更新明道云 HAP (Host Application Platform) 的 OpenAPI 3.0 接口文档,支持中英文双语文档的同步管理。

## 使用场景

在以下情况下使用此技能:
- 用户需要在 HAP 文档中新增接口
- 用户需要修改现有接口的定义、参数或响应结构
- 用户需要删除废弃的接口
- 用户需要确保中英文文档保持同步
- 用户提到"HAP API 文档"、"接口文档"、"OpenAPI"、"新增接口"、"更新接口"等关键词

## 文档结构

HAP API 文档项目包含两类文档:

### 1. 组织授权 API 文档
位于项目根目录:
- `en/` - 英文版组织授权接口文档
- `zh-Hans/` - 中文版组织授权接口文档

### 2. 应用 API 文档 (v3-beta)
位于 application 目录:
- `application/en/` - 英文版应用接口文档
- `application/zh-Hans/` - 中文版应用接口文档

每个文档目录包含:
```
openapi.yaml         # 主文件,定义 tags、paths 路由
description.md       # 文档描述
index.html          # Redoc 预览页面
paths/              # 接口定义目录
  ├── user/         # 按功能模块分类
  ├── department/
  └── ...
schemas/            # 数据模型目录
  ├── base/         # 基础模型
  ├── user/         # 用户相关模型
  └── ...
```

## 工作流程

### 新增接口

1. **确定接口类型和位置**
   - 询问用户接口属于哪个模块 (user/department/app 等)
   - 确定是组织 API 还是应用 API
   - 确定 HTTP 方法 (GET/POST/PUT/DELETE 等)

2. **收集接口信息**
   - 接口路径 (如 `/v2/user/getExternalPortalUsers`)
   - 接口摘要和描述
   - 请求参数 (query/body/path parameters)
   - 响应结构
   - 是否需要鉴权参数 (appKey, sign, timestamp 等)

3. **创建文件结构**

   对于每个语言版本 (en 和 zh-Hans),执行以下操作:

   a. **创建 path 定义文件**
      - 位置: `paths/{module}/{operationName}.yaml`
      - 包含: HTTP 方法、tags、summary、description、parameters/requestBody、responses
      - 参考 `references/path_template.yaml` 中的模板

   b. **创建 schema 文件** (如需要)
      - 请求 schema: `schemas/{module}/{operationName}Request.yaml`
      - 响应 schema: `schemas/{module}/{operationName}Response.yaml`
      - 数据对象: `schemas/{module}/{objectName}.yaml`
      - 参考 `references/schema_template.yaml` 中的模板

   c. **更新 openapi.yaml**
      - 在 paths 部分添加新路由
      - 如果有特殊的 server 配置,添加 servers 字段
      - 确保按模块分组,保持文件整洁

4. **验证一致性**
   - 确保中英文版本结构一致
   - 检查所有 $ref 引用路径正确
   - 验证必填字段在 required 数组中

### 修改接口

1. **定位文件**
   - 使用 Grep 工具搜索接口路径或 operationId
   - 找到对应的 path 文件和相关 schema 文件

2. **同步修改**
   - 同时修改中英文版本的对应文件
   - 保持字段结构一致,仅翻译 description 和 example

3. **更新关联文件**
   - 如果修改了 schema 引用,检查其他使用该 schema 的接口
   - 如果修改了路径,同步更新 openapi.yaml

### 删除接口

1. **从 openapi.yaml 中移除路由**
   - 同时删除中英文版本

2. **删除相关文件**
   - 删除 paths 文件
   - 检查 schemas 是否被其他接口使用,如果没有则删除

3. **验证引用**
   - 确保没有其他地方引用已删除的文件

### 同步中英文文档

1. **对比结构**
   - 检查 openapi.yaml 中的 paths 是否一致
   - 对比文件目录结构

2. **同步差异**
   - 复制缺失的文件
   - 翻译描述性文本
   - 保持技术字段 (type, format, required 等) 完全一致

## 重要规范

### 命名规范
- **文件命名**: 使用驼峰命名法,如 `getExternalPortalUsers.yaml`
- **operationId**: 与文件名保持一致
- **schema 文件**: 使用描述性名称,如 `externalPortalUser.yaml`

### 路径引用规范
- 从 openapi.yaml 引用 paths: `'./paths/{module}/{file}.yaml'`
- 从 paths 引用 schemas: `'../../schemas/{module}/{file}.yaml'`
- 从 schemas 引用其他 schemas: `'./{file}.yaml'`

### 请求/响应规范

**GET 请求**: 使用 parameters 定义查询参数
```yaml
parameters:
  - name: pageIndex
    in: query
    required: true
    schema:
      type: integer
```

**POST 请求**: 使用 requestBody 定义请求体
```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        $ref: '../../schemas/user/requestSchema.yaml'
```

### 鉴权参数
组织 API 通常需要以下基础参数:
- `appKey` - 应用密钥
- `sign` - 签名
- `timestamp` - 时间戳
- `projectId` - 项目 ID

可以引用基础 schema: `$ref: ../../schemas/base/request/baseQueryAppkey.yaml`

### 响应结构
标准响应格式:
```yaml
type: object
properties:
  code:
    type: integer
    description: 状态码,1表示成功
  message:
    type: string
    description: 状态描述
  data:
    type: object/array
    description: 返回数据
```

## 工作检查清单

在完成文档更新后,执行以下检查:

- [ ] 中英文版本都已更新
- [ ] openapi.yaml 中的路由已添加/修改/删除
- [ ] paths 文件已创建/修改/删除
- [ ] 必要的 schemas 文件已创建
- [ ] 所有 $ref 引用路径正确
- [ ] 必填参数在 required 数组中声明
- [ ] description 提供了清晰的说明
- [ ] example 提供了有效的示例值
- [ ] 中英文字段结构完全一致 (仅描述不同)

## 参考资料

详细的模板和示例请查看:
- `references/path_templates.md` - 接口定义模板
- `references/schema_templates.md` - 数据模型模板
- `references/common_patterns.md` - 常见模式参考

## 预览文档

修改完成后,可以使用 Live Server 预览:
1. 在 VS Code 中右键点击 `zh-Hans/index.html` 或 `en/index.html`
2. 选择 "Open With Live Server"
3. 浏览器将自动打开并显示 Redoc 渲染的文档
