---
name: abc-apifox
description: ABC 医疗云 API 文档查询工具。读取和查询 ABC API 的 OpenAPI 规范文档（5000+ 接口），支持按模块、路径、方法搜索，自动解析 $ref 引用。采用按模块拆分的缓存结构，查询速度快。使用场景：(1) 查询 API 接口定义 (2) 搜索特定功能接口 (3) 查询 Schema 定义 (4) 查看接口统计信息
---

# ABC Apifox Skill

本 skill 提供 ABC 医疗云 API 文档查询功能。

## 环境配置

### 必需的环境变量

```bash
# 设置 Apifox Access Token（必需）
export APIFOX_ACCESS_TOKEN="你的 Apifox Access Token"

# 设置项目 ID（可选，默认为 4105462）
export APIFOX_PROJECT_ID="4105462"
```

获取 Token：登录 [Apifox](https://apifox.com) > 账号设置 > API 访问令牌

### 依赖安装

```bash
pip3 install requests
```

### 首次使用：初始化缓存

首次使用前需要初始化缓存（只需执行一次），执行以下命令：

```bash
# 初始化环境（自动安装依赖、检查配置、下载缓存）
python3 scripts/apifox.py init
```

初始化过程会自动：
1. 检查并安装 Python 依赖（requests）
2. 运行环境检查（验证 APIFOX_ACCESS_TOKEN 配置）
3. 从 Apifox 下载最新 API 文档并构建缓存

缓存初始化后，后续查询直接从本地读取，无需重复初始化。如需更新缓存，可使用 `refresh_oas` 命令。

### 工作原理

**缓存架构**：按模块拆分的缓存结构

1. **智能拆分**：接口按模块拆分，Schema 按首字母分组
2. **按需加载**：查询时只加载相关模块文件
3. **缓存持久**：缓存永久有效，需要手动刷新获取最新文档
4. **自动保护**：查询时内部自动检查缓存状态

## 使用方式

```bash
python3 scripts/apifox.py <command> [参数]
```

所有命令默认返回 JSON 格式输出。

## 命令列表

### 接口查询

| 命令 | 说明 |
|------|------|
| `get_path` | 获取接口详情（自动推断模块） |
| `get_schema` | 获取 Schema 定义 |
| `search_paths` | 搜索接口（关键词匹配） |
| `list_modules` | 列出所有模块 |
| `get_module` | 获取模块的所有接口 |

### 文档管理

| 命令 | 说明 |
|------|------|
| `init` | 初始化环境（安装依赖、检查配置、下载缓存） |
| `refresh_oas` | 刷新 OpenAPI 文档 |
| `status` | 查看缓存状态 |
| `clear_cache` | 清除本地缓存（需要 `--force`） |

## 查询注意事项

### 1. 查询前先搜索

**获取接口详情前，必须先用 `search_paths` 确认接口存在**：

```bash
# 错误做法：直接查询可能不存在的接口
python3 scripts/apifox.py get_path --path "/rpc/xxx/yyy" --method POST

# 正确做法：先搜索确认存在
python3 scripts/apifox.py search_paths --keyword "xxx"
# 然后根据搜索结果获取详情
python3 scripts/apifox.py get_path --path "/rpc/xxx/yyy" --method GET
```

### 2. HTTP 方法判断

根据路径特征判断 HTTP 方法：

| 路径特征 | 常见方法 | 示例 |
|---------|---------|------|
| `/page`、`/list`、`/query` | GET | 分页查询、列表查询 |
| `/create`、`/add` | POST | 创建资源 |
| `/update`、`/modify` | PUT/POST | 更新资源 |
| `/delete`、`/remove` | DELETE | 删除资源 |
| `/xxx/{id}` | GET | 获取单个资源 |

## 使用示例

### 获取接口详情

```bash
# 获取接口详情（自动推断模块）
python3 scripts/apifox.py get_path \
    --path "/api/v3/goods/stocks/check/orders" \
    --method POST

# 获取接口并解析 $ref 引用
python3 scripts/apifox.py get_path \
    --path "/api/v3/goods/stocks/check/orders" \
    --method POST \
    --include_refs true
```

### 获取 Schema 定义

```bash
# 获取 Schema 定义
python3 scripts/apifox.py get_schema --name CreateGoodsStockCheckOrderReq
```

### 搜索接口

```bash
# 搜索盘点相关接口
python3 scripts/apifox.py search_paths --keyword "盘点"

# 搜索特定模块的接口
python3 scripts/apifox.py search_paths --keyword "库存" --module api.stocks

# 按方法过滤
python3 scripts/apifox.py search_paths --keyword "order" --method POST --limit 10
```

### 模块查询

```bash
# 列出所有模块
python3 scripts/apifox.py list_modules

# 获取特定模块的所有接口
python3 scripts/apifox.py get_module --module api.stocks
```

### 文档管理

```bash
# 初始化环境（首次使用前必须执行）
python3 scripts/apifox.py init

# 查看缓存状态
python3 scripts/apifox.py status

# 刷新文档（从 Apifox 获取最新数据）
python3 scripts/apifox.py refresh_oas

# 清除缓存
python3 scripts/apifox.py clear_cache --force
```

## 输出格式

所有命令返回 JSON 格式：

```json
{
  "success": true,
  "data": "返回的数据"
}
```

错误时返回：

```json
{
  "success": false,
  "error": "错误信息"
}
```

## 缓存结构

```
cache/
├── meta.json              # 元数据 + 全局索引
├── modules/               # 按模块拆分的接口数据
│   ├── api.stocks.json    # 库存相关接口
│   ├── rpc.advice.json    # 医嘱相关接口
│   └── ...
└── schemas/               # Schema 定义缓存（按首字母分组）
    ├── a.json             # A 开头的 Schema
    ├── b.json
    ├── ...
    └── _.json             # 非字母开头的 Schema（中文、数字等）
```

## 模块命名规则

| 路径格式 | 模块名 | 示例 |
|---------|-------|------|
| `/api/v3/goods/stocks/xxx` | `api.stocks` | 库存模块 |
| `/rpc/advice/xxx` | `rpc.advice` | 医嘱模块 |
| `/api/global-auth/xxx` | `api.global-auth` | 认证模块 |

## 文件结构

```
scripts/
├── apifox.py           # Python CLI 实现（命令行入口）
├── apifox_client.py    # 客户端
├── cache_manager.py    # 缓存管理器
├── requirements.txt    # Python 依赖
├── check_env.py        # 环境检查脚本
└── test_apifox.py      # 功能测试脚本
```

## 开发工具

### 环境检查 (`check_env.py`)

检查环境配置和 API 连接状态：

```bash
python3 scripts/check_env.py
```

**检查项目**：
- 环境变量是否配置
- Python 依赖是否安装
- 缓存状态
- API 连接测试

**使用场景**：
- 首次配置后验证环境
- API 连接异常时诊断
- 修改环境变量后确认生效

### 功能测试 (`test_apifox.py`)

冒烟测试套件，验证核心功能正常：

```bash
python3 scripts/test_apifox.py
```

**测试内容**：
- 缓存加载
- 搜索性能（平均应 < 100ms）
- 模块过滤
- 方法过滤
- 接口详情获取
- Schema 获取
- 模块列表

**使用场景**：
- **修改代码后必须运行**，确保功能正常
- 部署前的回归测试
- 性能退化检测

### 依赖安装 (`requirements.txt`)

```bash
# 安装依赖
pip3 install -r scripts/requirements.txt
```

## 开发工作流

修改功能后必须执行冒烟测试：

```bash
# 1. 修改代码
vim scripts/cache_manager.py

# 2. 运行测试（必须）
python3 scripts/test_apifox.py

# 3. 测试通过后提交
git add scripts/cache_manager.py
git commit -m "fix: ..."
```

**测试失败时**：
- 检查修改是否破坏了现有功能
- 运行 `check_env.py` 诊断环境问题
- 修复后重新测试直到通过
