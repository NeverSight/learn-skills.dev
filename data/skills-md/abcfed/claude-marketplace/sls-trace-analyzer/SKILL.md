---
name: sls-trace-analyzer
description: 根据 traceId 或 URL（带时间戳）查询阿里云日志服务 (SLS) 获取日志，分析日志内容，定位代码中的问题。
---

# SLS Trace Analyzer Skill

根据 traceId 或 URL（带时间戳）查询阿里云日志服务 (SLS) 获取日志，分析日志内容，定位代码中的问题。

## Usage

```
/sls-trace <traceId | URL> [--env <environment>] [--region <region>] [--from <date>] [--to <date>]
```

### Parameters
- `traceId`: 要查询的 traceId，或带时间戳的 URL（如 `https://dev.abczs.cn/api-weapp/pe/registration?t=1769398080665`）
- `--env`: 可选，环境名称：dev/test/prod（默认 prod，URL 模式下自动从域名解析）
- `--region`: 可选，地域：shanghai/hangzhou（默认 shanghai，URL 模式下自动从域名解析）
- `--from`: 可选，开始日期，格式 YYYY-MM-DD 或 YYYY-MM-DD HH:mm:ss（默认 3 天前）
- `--to`: 可选，结束日期，格式 YYYY-MM-DD 或 YYYY-MM-DD HH:mm:ss（默认当前时间）
- `--longtime`: 可选，仅查询 longtime logstore（默认同时查询普通和 longtime 两个 logstore）

### LogStore 查询策略

**默认行为**：同时查询两个 logstore 以获取完整日志
- 普通存储 (`prod`/`test`/`dev`): 常规业务日志
- 长期存储 (`prod_longtime`/`test_longtime`/`dev_longtime`): 带 `@LogReqAndRsp(longTimeLog = true)` 注解的接口请求/响应详情

**为什么需要同时查询**：
- 普通存储包含 MQ 消息、网关日志等
- 长期存储包含详细的请求入参和响应数据
- 只查询单个 logstore 可能遗漏关键信息，导致问题分析不完整

### URL 模式说明
当输入为 URL 时，skill 会自动：
1. 从域名解析环境和地域
2. 从 `t` 参数提取时间戳
3. 先查询 gateway access-log 获取 X-B3-TraceId
4. 再用 traceId 查询详细日志

## Configuration

### Python 运行环境（按需自动初始化）

`sls-query.py`、`requirements.txt`、`.venv/` 均位于**本 SKILL.md 同级目录**。

**调用规则**：
1. 直接用同目录下的 `.venv/bin/python` 执行 `sls-query.py`，无需前置检查
2. 仅当执行失败（`No such file or directory`、`ModuleNotFoundError`）时，在同目录下执行 `python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt` 初始化后重试
3. 不要使用系统 `python3` 直接运行 `sls-query.py`，否则缺少依赖

### 上海 Region (默认)
- Endpoint: `cn-shanghai.log.aliyuncs.com`
- Project: `abc-cis-log`
- Credentials: loaded from `~/.config/sls-query/credentials.json`

### 杭州 Region
- Endpoint: `cn-hangzhou.log.aliyuncs.com`
- Project: `abc-cis-log-hangzhou`
- Credentials: loaded from `~/.config/sls-query/credentials.json`

### LogStore 命名规则
- 开发环境: `dev` 或 `dev_longtime`
- 测试环境: `test` 或 `test_longtime`
- 生产环境: `prod` 或 `prod_longtime`

### 域名到环境映射
| 域名 | 环境 | 地域 |
|------|------|------|
| `dev.abczs.cn` | dev | shanghai |
| `test.abczs.cn` | test | shanghai |
| `abcyun.cn` | prod | shanghai |
| `region2.abcyun.cn` | prod | hangzhou |

## Instructions

当用户调用此 skill 时，按以下步骤执行：

### Step 0: 判断输入类型（URL 或 TraceId）

首先判断用户输入是 URL 还是直接的 traceId：

```python
if input.startswith('http://') or input.startswith('https://'):
    # URL 模式 - 执行 Step 0.1 ~ 0.3
    pass
else:
    # TraceId 模式 - 跳到 Step 1
    trace_id = input
```

#### Step 0.1: 解析 URL

```python
from urllib.parse import urlparse, parse_qs

parsed = urlparse(url)
domain = parsed.netloc  # e.g., "dev.abczs.cn"
path = parsed.path      # e.g., "/api-weapp/pe/registration"
query = parsed.query    # e.g., "t=1769398080665" 或 "1769398080665"

# 提取时间戳（支持两种格式）
if '=' in query:
    params = parse_qs(query)
    timestamp = params.get('t', [None])[0]
else:
    timestamp = query  # 直接是时间戳
```

#### Step 0.2: 从域名解析环境和地域

```python
DOMAIN_MAPPING = {
    "dev.abczs.cn": {"env": "dev", "region": "shanghai"},
    "test.abczs.cn": {"env": "test", "region": "shanghai"},
    "abcyun.cn": {"env": "prod", "region": "shanghai"},
    "region2.abcyun.cn": {"env": "prod", "region": "hangzhou"},
}
config = DOMAIN_MAPPING.get(domain, {"env": "prod", "region": "shanghai"})
```

#### Step 0.3: 查询 Gateway Access Log 获取 TraceId

使用时间戳和 path 查询 gateway 日志，提取 `X-B3-TraceId`：

```bash
.venv/bin/python sls-query.py \
  --mode access-log \
  --timestamp "<timestamp>" \
  --path "<path>" \
  --region "<region>" \
  --env "<env>"
```

**【重要】Gateway 日志 Topic 说明**
- **`abc-cis-gateway-service`**: 业务请求 API 网关入口，用于查询 access-log 获取 TraceId
- **`abc-invoke-gateway-service`**: 跨 region 调用网关入口，用于判断是否需要跨 region 查询

**【查询技巧】**
1. 时间范围：默认查询时间戳前后 **10 分钟**（不是 30 秒，太窄容易漏掉）
2. 路径匹配：使用路径的**关键词**而非完整路径，例如用 `registration` 而非 `/api-weapp/pe/registration`
3. 如果 access-log 模式查不到，可以直接用 gateway topic 查询：
   ```bash
   # 备用查询方式：直接查 gateway 日志
   query = '__topic__: abc-cis-gateway-service and <path关键词>'
   ```

从返回日志中提取 `X-B3-TraceId` 字段，然后继续 Step 1。

### Step 1: 解析参数并确定配置

从用户输入中解析 traceId 和可选参数，确定：

```python
# 根据 region 选择配置
if region == "hangzhou":
    endpoint = "cn-hangzhou.log.aliyuncs.com"
    project = "abc-cis-log-hangzhou"
else:  # 默认上海
    endpoint = "cn-shanghai.log.aliyuncs.com"
    project = "abc-cis-log"

# 根据 env 和 longtime 确定 logstore
logstore = env  # dev/test/prod
if longtime:
    logstore = f"{env}_longtime"

# Credentials loaded from ~/.config/sls-query/credentials.json
# (or SLS_ACCESS_KEY_ID / SLS_ACCESS_KEY_SECRET env vars)

# 时间范围（默认最近 3 天）
from_time = from_date or (now - 3 days)
to_time = to_date or now
```

### Step 2: 查询 SLS 日志

使用 Python 脚本查询日志：

```bash
.venv/bin/python sls-query.py \
  --trace-id "<traceId>" \
  --region "<region>" \
  --env "<env>" \
  --from "<from_time>" \
  --to "<to_time>"
```

如果使用 longtime logstore，添加 `--longtime` 参数。

### Step 2.5: 跨 Region 日志追踪

首次查询默认使用上海 region，需判断是否需要查询其他 region。

**【判断逻辑】**

1. **先检查上海日志是否已包含完整错误信息**
   - 如果已有目标服务（如 `abc-his-xxx-service`）的 ERROR 日志和异常堆栈 → **无需跨 region 查询**
   - 如果只有 `abc-cis-monitor-service` 或 `abc-cis-gateway-service` 的日志 → 继续下一步

2. **检查 region 字段确定请求实际路由**
   ```
   his-region1 / region1 → 上海 (已查询，无需再查)
   his-region2 / region2 → 杭州 (需要查询)
   ```

3. **需要跨 Region 查询的条件**（同时满足）
   - 日志显示 `region: his-region2` 或 `region2`
   - 上海日志中**缺少**目标服务的详细错误堆栈

**【执行跨 Region 查询】**

满足上述条件时，立即执行杭州查询（无需询问用户）：
```bash
.venv/bin/python sls-query.py \
  --trace-id "<traceId>" \
  --region "hangzhou" \
  --env "<env>"
```

**【架构说明】**
- `abc-cis-monitor-service` 全局只部署在上海，记录所有 region 的 HTTP 请求概要
- 上海日志：monitor 层（请求/响应概要）
- 杭州日志：业务服务详细日志、ERROR 堆栈

### Step 3: 分析日志内容

拿到日志后，进行以下分析：

1. **识别错误和异常**
   - 查找 ERROR、WARN 级别的日志
   - 识别 Java 异常堆栈（Exception、Caused by）
   - 提取错误消息和错误码

2. **追踪请求链路**
   - 按时间排序日志条目
   - 识别请求入口（Controller）和出口
   - 标记 RPC/Feign 调用和响应
   - 识别数据库操作

3. **提取关键信息**
   - 请求 URL 和方法
   - 请求参数
   - 响应结果
   - 耗时信息
   - 服务调用链

### Step 4: 定位代码问题

基于日志分析结果：

1. **从 URL Path 定位服务**
   - 从日志中提取请求的 URL path（如 `/api/v2/healthlink/xxx`）
   - 查看 Config 工程中的 Gateway 路由配置：`/Users/wxd/IdeaProjects/AbcCisConfig`
   - 路由配置格式示例：
     ```yaml
     routes:
       - id: abc-cis-healthlink-service
         uri: http://abc-cis-healthlink-service
         predicates:
           - Path=/api/v2/healthlink/**
     ```
   - `id` 字段即为服务名称
   - 根据服务名称在 `~/IdeaProjects/` 目录下找到对应的服务代码
   - 例如：`/api/v2/healthlink/**` 对应服务 `abc-cis-healthlink-service`，代码位于 `~/IdeaProjects/AbcCisHealthlinkService`

2. **【重要】确保代码分支与线上环境一致**

   #### 2.1 确定目标环境

   按以下优先级从多个来源提取环境信息：

   **来源 A：用户输入的描述文本**
   - 格式示例：`【重要】[region1][灰度环境][primary]异常请求`
   - 关键词映射：
     | 关键词 | 环境 |
     |--------|------|
     | `灰度环境` | gray |
     | `预发布环境` | pre |
     | `正式环境` | prod |
     | `测试环境` | test |
     | `开发环境` | dev |

   **来源 B：Gateway access-log 的 `env` 字段**
   - 从 `__topic__: abc-cis-gateway-service` 的日志中提取 `env` 字段
   - 示例：`env: gray`、`env: pre`、`env: prod`、`env: dev`、`env: test`

   **来源 C：SLS 查询使用的 logstore 环境**
   - 如果以上来源都没有，则根据 Step 1 中确定的 `--env` 参数推断

   #### 2.2 环境到分支映射

   | 环境 (env) | Git 分支 |
   |-----------|----------|
   | dev | `dev-joint` |
   | test | `test-joint` |
   | pre | `rc` |
   | gray | `gray` |
   | prod | `master` |

   #### 2.3 分支使用策略（分场景）

   **场景 A：当前工作目录已在目标服务工程内**
   - **优先使用当前分支**，直接在当前分支上查找代码、定位问题
   - 只有当在当前分支上**找不到对应的类/方法**，或者**代码行号与堆栈不匹配**时，才切换到环境对应的目标分支

   **场景 B：当前工作目录不在目标服务工程内**
   - 进入目标服务代码目录后，直接切换到环境对应的目标分支

   ```bash
   # 场景 B 或场景 A 回退时的切换流程：
   cd ~/IdeaProjects/<ServiceProject>
   git fetch origin <target_branch>
   git checkout <target_branch>
   git pull origin <target_branch>
   ```

   **【注意事项】**
   - 切换分支前先检查工作区是否干净（`git status`），如有未提交的修改需要先 `git stash`
   - 如果目标分支不存在，回退使用 `master` 分支
   - 对于依赖库（abc-cis-core、abc-cis-commons、abc-bis-rpc-sdk）**不需要切换分支**，只需在当前分支上 `git pull` 拉取最新代码即可

3. **从异常堆栈定位**
   - 提取堆栈中的类名和行号
   - 优先关注 `cn.abcyun` 包下的代码
   - 使用 codebase-retrieval 或 Grep 工具查找对应代码
   - 分析代码逻辑找出可能的问题原因

3. **从错误消息定位**
   - 搜索错误消息在代码中的位置
   - 分析错误抛出的条件
   - 追踪调用链

4. **检查相关依赖代码**
   - 如果涉及 abc-cis-core，查看 `/Users/wxd/IdeaProjects/AbcCisCore`
   - 如果涉及 abc-cis-commons，查看 `/Users/wxd/IdeaProjects/AbcCisCommons`
   - 如果涉及 abc-bis-rpc-sdk，查看 `/Users/wxd/IdeaProjects/AbcBisRpcSDK`

5. **【重要】下游服务代码分析**

   当日志显示错误来自 RPC/Feign 调用的下游服务时，**必须**查看下游服务的具体实现：

   - **识别下游服务**: 从 FeignClient 类名识别目标服务
     | FeignClient 类名 | 对应服务 | 代码位置 |
     |-----------------|---------|---------|
     | `AbcCisCrmFeignClient` | CRM 服务 | `~/IdeaProjects/AbcCisCrmService` |
     | `AbcCisGoodsFeignClient` | ScGoods 服务 | `~/IdeaProjects/AbcCisScGoodsService` |
     | `AbcCis{Xxx}FeignClient` | 对应 Xxx 服务 | `~/IdeaProjects/AbcCis{Xxx}Service` |

   - **定位接口实现**:
     1. 从堆栈中找到 FeignClient 调用的方法名（如 `tryLockingGoodsStockBatch`）
     2. 在 RPC SDK 中找到 FeignClient 接口定义：`~/IdeaProjects/AbcBisRpcSDK`
     3. 根据 `@PostMapping`/`@GetMapping` 注解找到 URL path
     4. 在下游服务中搜索对应的 Controller 和 Service 实现

   - **分析实现逻辑**:
     1. 阅读 Controller 层代码，理解入参处理
     2. 阅读 Service 层代码，理解业务逻辑
     3. 特别关注：事务边界、锁机制、数据库操作顺序
     4. 对于死锁问题：分析 SQL 执行顺序和锁获取顺序

### Step 4.5: 上下游日志综合分析（深度根因定位）

**【关键】** 仅看异常堆栈不足以定位根因，必须结合上下游日志和代码逻辑综合分析：

1. **识别调用链中的所有服务**
   - 从日志的 `__topic__` 字段识别涉及的服务
   - 常见服务对应关系：
     | __topic__ | 服务名 | 代码位置 |
     |-----------|--------|---------|
     | `abc-cis-dispensing-service` | 发药服务 | `~/IdeaProjects/AbcCisDispensingService` |
     | `abc-cis-sc-goods-service` | 商品库存服务 | `~/IdeaProjects/AbcCisScGoodsService` |
     | `abc-cis-charge-service` | 收费服务 | `~/IdeaProjects/AbcCisChargeService` |
     | `abc-cis-crm-service` | CRM服务 | `~/IdeaProjects/AbcCisCrmService` |

2. **按服务分组分析日志**
   - 将同一 TraceId 的日志按 `__topic__` 分组
   - 每个服务单独分析其内部流程
   - 重点关注 ERROR 级别日志和异常堆栈

3. **分析上游服务（调用方）**
   - 查看调用参数是否正确
   - 检查调用时机和并发情况
   - 分析重试逻辑是否合理

4. **分析下游服务（被调用方）**
   - **必须阅读下游服务的代码实现**
   - 查看接口入参处理逻辑
   - 分析业务处理流程
   - 检查事务和锁的使用方式

5. **特定问题类型的深度分析**

   **死锁问题 (Deadlock)**:
   - 查看下游服务的 SQL 执行顺序
   - 分析是否存在锁顺序不一致
   - 检查事务范围是否过大
   - 查看是否有并发请求操作相同数据

   **超时问题 (Timeout)**:
   - 分析各阶段耗时
   - 检查是否有慢 SQL
   - 查看是否有外部依赖阻塞

   **空指针问题 (NullPointer)**:
   - 定位具体代码行
   - 分析数据来源
   - 检查上游传参是否完整

6. **综合分析输出**
   - 结合代码逻辑解释为什么会出现这个错误
   - 给出具体的代码修复位置和方案

### Step 5: 输出分析报告

生成结构化的分析报告：

```markdown
## 日志分析报告

### 基本信息
- TraceId: xxx
- 环境: prod/test/dev
- 地域: shanghai/hangzhou
- 时间范围: xxx ~ xxx
- 日志条目数: xxx
- 涉及服务: xxx, xxx

### 错误摘要
- 错误类型: xxx
- 错误消息: xxx
- 发生时间: xxx
- 发生服务: xxx
```

### 调用链路
```markdown
1. [入口] POST /api/xxx → DispensingService
2. [Service] DispensingService.dispense()
3. [RPC] → ScGoodsService.lockingGoodsStock()
4. [DB] SQL 执行
5. [Error] Deadlock / NullPointer / Timeout
```

### 上下游日志分析
```markdown
#### 上游服务 (xxx-service)
- 调用参数: ...
- 调用时间: ...
- 关键日志: ...

#### 下游服务 (xxx-service)
- 接收参数: ...
- 处理流程: ...
- 错误日志: ...
- 异常堆栈: ...
```

### 根因分析（重点）
```markdown
#### 问题现象
简述观察到的错误现象

#### 代码分析
- **上游调用代码**: `文件路径:行号`
  ```java
  // 关键代码片段
  ```
- **下游实现代码**: `文件路径:行号`
  ```java
  // 关键代码片段
  ```

#### 根本原因
结合代码逻辑，解释为什么会出现这个错误：
1. xxx
2. xxx

#### 修复建议
1. 具体修复方案
2. 代码修改位置
```

## Examples

```bash
# 查询生产环境上海 region 的日志（默认最近 3 天）
/sls-trace abc123def456

# 查询测试环境的日志
/sls-trace abc123def456 --env test

# 查询杭州 region 生产环境的日志
/sls-trace abc123def456 --region hangzhou

# 指定日期范围查询
/sls-trace abc123def456 --from 2025-01-20 --to 2025-01-24

# 指定精确时间范围
/sls-trace abc123def456 --from "2025-01-20 10:00:00" --to "2025-01-20 12:00:00"

# 查询 longtime logstore（历史日志）
/sls-trace abc123def456 --env prod --longtime

# 组合使用
/sls-trace abc123def456 --env test --region hangzhou --from 2025-01-20

# ========== URL 模式示例 ==========

# 通过 URL 自动查询（带 t= 参数）
/sls-trace https://dev.abczs.cn/api-weapp/pe/registration?t=1769398080665
# 自动解析: env=dev, region=shanghai, timestamp=1769398080665

# 通过 URL 自动查询（时间戳直接作为参数）
/sls-trace https://test.abczs.cn/api/v2/charge/sheets?1769398080665
# 自动解析: env=test, region=shanghai, timestamp=1769398080665

# 生产环境 URL
/sls-trace https://abcyun.cn/api/v2/crm/patients?t=1769398080665
# 自动解析: env=prod, region=shanghai

# 杭州 region 生产环境 URL
/sls-trace https://region2.abcyun.cn/api/v2/his/emr?t=1769398080665
# 自动解析: env=prod, region=hangzhou
```
