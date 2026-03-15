---
name: loki-log-query
description: |
  通过 Grafana Loki 查询线上日志，支持多环境切换、traceId 链路追踪、接口路径查询、关键词搜索。

  触发场景：
  - 需要查看线上日志排查问题
  - 通过 traceId 查询完整请求链路
  - 通过接口路径查询该接口的所有日志
  - 搜索特定错误日志或异常堆栈
  - 切换不同日志服务环境

  触发词：查日志、traceId、链路追踪、Loki、日志查询、线上日志、生产日志、错误日志、异常堆栈、日志排查、切换环境、monitor
---

# Loki 日志查询技能

## 概述

通过 Grafana Loki API 查询线上日志。支持：
1. **多环境管理**：5 个 Grafana 日志服务，按需切换
2. **traceId 查询**：通过日志ID获取完整请求链路
3. **接口路径查询**：通过 API 接口路径查询相关日志
4. **关键词搜索**：错误信息、类名、自定义关键词

## 多环境配置

配置文件：`.claude/skills/loki-log-query/environments.json`

### 环境列表

| 环境别名 | 名称 | URL | 快捷词 |
|----------|------|-----|--------|
| `test13` | 测试13（主测试环境） | `https://test13.xnzn.net/grafana` | test13, 13 |
| `monitor-test` | Monitor 测试环境 | `https://monitor-test.xnzn.net/grafana` | mtest |
| `monitor-dev` | Monitor 开发环境 | `https://monitor-dev.xnzn.net/grafana` | mdev, dev |
| `monitor02-dev` | Monitor02 开发环境 | `https://monitor02-dev.xnzn.net/grafana` | m02, monitor02 |
| `monitor-tyy-dev` | Monitor 体验园开发环境 | `https://monitor-tyy-dev.xnzn.net/grafana` | tyy, 体验园 |

### 环境匹配规则

用户说的话 → 匹配环境：
- "查 test13 的日志" → `test13`
- "去 monitor-dev 查" → `monitor-dev`
- "切到体验园" → `monitor-tyy-dev`
- "去 m02 查一下" → `monitor02-dev`
- 未指定环境 → 使用 `active` 字段指定的默认环境

### 读取配置

```bash
SKILL_DIR="$CLAUDE_PROJECT_DIR/.claude/skills/loki-log-query"
ENV_FILE="${SKILL_DIR}/environments.json"

# 读取指定环境（参数: 环境别名）
read_env() {
  local ENV_KEY="${1:-$(python3 -c "import json; print(json.load(open('${ENV_FILE}'))['active'])")}"
  GRAFANA_URL=$(python3 -c "import json; print(json.load(open('${ENV_FILE}'))['environments']['${ENV_KEY}']['url'])")
  TOKEN=$(python3 -c "import json; print(json.load(open('${ENV_FILE}'))['environments']['${ENV_KEY}']['token'])")
  API="${GRAFANA_URL}/api/datasources/proxy/uid/loki/loki/api/v1"
  echo "Environment: ${ENV_KEY} → ${GRAFANA_URL}"
}

# 通过别名查找环境 key
find_env() {
  python3 -c "
import json
data = json.load(open('${ENV_FILE}'))
alias = '${1}'.lower()
for key, env in data['environments'].items():
    if alias == key or alias in env.get('aliases', []):
        print(key)
        break
else:
    print(data['active'])
"
}
```

### 切换活跃环境

```bash
# 切换默认环境为 monitor-dev
python3 -c "
import json
data = json.load(open('${ENV_FILE}'))
data['active'] = 'monitor-dev'
json.dump(data, open('${ENV_FILE}', 'w'), indent=2, ensure_ascii=False)
print('Switched to:', data['active'])
"
```

### 更新 Token

```bash
# 为某个环境设置 Token
python3 -c "
import json
data = json.load(open('${ENV_FILE}'))
data['environments']['monitor-dev']['token'] = 'glsa_新的token值'
json.dump(data, open('${ENV_FILE}', 'w'), indent=2, ensure_ascii=False)
print('Token updated for monitor-dev')
"
```

## API 基础

| 项目 | 值 |
|------|-----|
| 数据源 | Loki（uid: `loki`） |
| **API 路径** | `{GRAFANA_URL}/api/datasources/proxy/uid/loki/loki/api/v1/query_range` |
| 认证 | `Authorization: Bearer {TOKEN}` |
| 默认标签 | `app="yunshitang"` |

> **重要**：Loki API 必须通过 Grafana datasource proxy 访问，直接 `/loki/api/v1/` 会返回 404。
> 查询时不限 project 标签（`{app="yunshitang"}`），可覆盖该 Grafana 下所有环境。

## 日志格式

```
2026-03-07 09:16:53.039,bcf6d955-fa26-45a5-9628-748f7ac4eed2,,,  INFO 1 --- [线程名] 类名 : 行号 : 消息内容
```

| 位置 | 字段 | 示例 |
|------|------|------|
| 第1段 | 时间戳 | `2026-03-07 09:16:53.039` |
| 第2段 | traceId | `bcf6d955-fa26-45a5-9628-748f7ac4eed2` 或 `a53dd0b0cc62bf4a79a63e77444f6f3f` |
| 第3段 | 商户ID | `553722740746489856` |
| 第4段 | 用户ID | `553723188689768448` |
| 第5段 | 日志内容 | `INFO 1 --- [thread] Class : 123 : msg` |

> traceId 可能是 UUID 格式（带横线）或 32位hex（不带横线），都支持。

## 查询场景

### 场景 1：按 traceId 查完整链路（最常用）

用户说："用 `a53dd0b0cc62bf4a79a63e77444f6f3f` 查日志"

```bash
TRACE_ID="a53dd0b0cc62bf4a79a63e77444f6f3f"
END=$(date +%s)000000000
START=$(( $(date +%s) - 21600 ))000000000  # 最近6小时

curl -s "${API}/query_range" \
  -H "Authorization: Bearer ${TOKEN}" \
  --data-urlencode "query={app=\"yunshitang\"} |= \"${TRACE_ID}\"" \
  --data-urlencode "start=${START}" \
  --data-urlencode "end=${END}" \
  --data-urlencode "limit=500" \
  --data-urlencode "direction=forward" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('status') == 'success':
    for stream in data['data']['result']:
        labels = stream.get('stream', {})
        print(f'--- {labels.get(\"app\",\"?\")}/{labels.get(\"project\",\"?\")} ---')
        for ts, line in stream['values']:
            print(line)
else:
    print('Error:', data)
"
```

### 场景 2：按接口路径查日志

用户说："查 `/security/summary/order/mealtime/classify/page` 这个接口的日志"

接口路径出现在请求日志的 `RequestLoggingFilter` 中（`>>> POST /xxx` 或 `>>> GET /xxx`）。

```bash
API_PATH="/security/summary/order/mealtime/classify/page"
END=$(date +%s)000000000
START=$(( $(date +%s) - 21600 ))000000000  # 最近6小时

curl -s "${API}/query_range" \
  -H "Authorization: Bearer ${TOKEN}" \
  --data-urlencode "query={app=\"yunshitang\"} |= \"${API_PATH}\"" \
  --data-urlencode "start=${START}" \
  --data-urlencode "end=${END}" \
  --data-urlencode "limit=200" \
  --data-urlencode "direction=forward" \
  | python3 -c "
import sys, json, re
data = json.load(sys.stdin)
if data.get('status') != 'success':
    print('Error:', data); sys.exit()

# 从匹配的请求日志中提取 traceId
trace_ids = set()
all_lines = []
for stream in data['data']['result']:
    for ts, line in stream['values']:
        all_lines.append(line)
        # 提取 traceId（第2个逗号分隔字段）
        parts = line.split(',')
        if len(parts) >= 2:
            tid = parts[1].strip()
            if len(tid) >= 32:
                trace_ids.add(tid)

print(f'Found {len(all_lines)} lines, {len(trace_ids)} unique traceIds')
print()
for tid in list(trace_ids)[:10]:
    print(f'  traceId: {tid}')
print()
for line in all_lines[:30]:
    print(line)
if len(all_lines) > 30:
    print(f'... and {len(all_lines)-30} more lines')
"
```

**进阶**：找到 traceId 后，再用场景 1 查该 traceId 的完整链路。

### 场景 3：关键词搜索

用户说："搜一下 LeException" 或 "查 ERROR 日志"

```bash
KEYWORD="LeException"
END=$(date +%s)000000000
START=$(( $(date +%s) - 21600 ))000000000  # 最近6小时

curl -s "${API}/query_range" \
  -H "Authorization: Bearer ${TOKEN}" \
  --data-urlencode "query={app=\"yunshitang\"} |= \"${KEYWORD}\"" \
  --data-urlencode "start=${START}" \
  --data-urlencode "end=${END}" \
  --data-urlencode "limit=100" \
  --data-urlencode "direction=backward"
```

**常用关键词组合**：

```logql
# 所有 ERROR 日志
{app="yunshitang"} |= "ERROR"

# 业务异常
{app="yunshitang"} |= "LeException"

# SQL 错误
{app="yunshitang"} |~ "SQLSyntaxError|DataAccessException|BadSqlGrammar"

# 空指针
{app="yunshitang"} |= "NullPointerException"

# 按类名搜索
{app="yunshitang"} |= "OrderInfoService"

# 组合：ERROR + 特定类
{app="yunshitang"} |= "ERROR" |= "OrderInfoService"

# 排除健康检查噪音
{app="yunshitang"} |= "ERROR" != "health" != "actuator"
```

### 场景 4：按接口查完整链路（组合查询）

用户说："查 `/api/v2/web/order/list` 接口的全链路日志"

**两步走**：
1. 先按接口路径搜索，拿到 traceId
2. 再按 traceId 查完整链路

```bash
# Step 1: 找 traceId
API_PATH="/api/v2/web/order/list"
END=$(date +%s)000000000
START=$(( $(date +%s) - 21600 ))000000000  # 最近6小时

TRACE_IDS=$(curl -s "${API}/query_range" \
  -H "Authorization: Bearer ${TOKEN}" \
  --data-urlencode "query={app=\"yunshitang\"} |= \"${API_PATH}\" |= \">>>\"" \
  --data-urlencode "start=${START}" \
  --data-urlencode "end=${END}" \
  --data-urlencode "limit=10" \
  --data-urlencode "direction=backward" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for stream in data.get('data',{}).get('result',[]):
    for ts, line in stream['values']:
        parts = line.split(',')
        if len(parts) >= 2 and len(parts[1].strip()) >= 32:
            print(parts[1].strip())
")

echo "Found traceIds:"
echo "${TRACE_IDS}" | head -5

# Step 2: 用第一个 traceId 查完整链路
FIRST_TID=$(echo "${TRACE_IDS}" | head -1)
if [ -n "${FIRST_TID}" ]; then
  curl -s "${API}/query_range" \
    -H "Authorization: Bearer ${TOKEN}" \
    --data-urlencode "query={app=\"yunshitang\"} |= \"${FIRST_TID}\"" \
    --data-urlencode "start=${START}" \
    --data-urlencode "end=${END}" \
    --data-urlencode "limit=500" \
    --data-urlencode "direction=forward" \
    | python3 -c "
import sys, json
data = json.load(sys.stdin)
for stream in data.get('data',{}).get('result',[]):
    for ts, line in stream['values']:
        print(line)
"
fi
```

### 场景 5：指定 project 环境查询

如果用户指定了具体的 project（如 test20）：

```logql
{app="yunshitang",project="test20"} |= "traceId值"
```

## LogQL 语法速查

### 流选择器

| 操作 | 语法 | 示例 |
|------|------|------|
| 精确匹配 | `=` | `{app="yunshitang"}` |
| 不等于 | `!=` | `{app!="test"}` |
| 正则匹配 | `=~` | `{project=~"test2.*"}` |

### 行过滤

| 操作 | 语法 | 示例 |
|------|------|------|
| 包含 | `\|=` | `\|= "ERROR"` |
| 不包含 | `!=` | `!= "DEBUG"` |
| 正则匹配 | `\|~` | `\|~ "Exception\|Error"` |
| 正则排除 | `!~` | `!~ "health\|ping"` |

### 查看可用标签值

```bash
# 列出所有 project
curl -s "${API}/label/project/values" -H "Authorization: Bearer ${TOKEN}"

# 列出所有 app
curl -s "${API}/label/app/values" -H "Authorization: Bearer ${TOKEN}"
```

## Bug 修复工作流

```
1. 获取线索（traceId / 接口路径 / 错误关键词）
   ↓
2. 确定环境（哪个 Grafana？读取 environments.json）
   ↓
3. 查询日志（场景 1-4 选择合适的查询方式）
   ↓
4. 分析日志（ERROR/异常堆栈/SQL 错误/耗时）
   ↓
5. 定位代码（类名:行号 → 项目搜索）
   ↓
6. 修复 + 更新云效任务状态
```

### 日志分析重点

1. **ERROR 级别日志** — 异常根因
2. **异常堆栈** — `at net.xnzn.core.xxx` 开头的行
3. **SQL 错误** — `SQLSyntaxErrorException`、`DataAccessException`
4. **业务异常** — `LeException` 抛出的位置
5. **耗时** — `Completed xxx in Nms`，识别慢请求
6. **请求/响应** — `RequestLoggingFilter` 的 `>>>` 和 `<<<` 日志

### 联动技能

| 场景 | 联动技能 |
|------|---------|
| 排查 Bug | `bug-detective` |
| 查询云效任务 | `yunxiao-task-management` |
| 查数据库 | `mysql-debug` |
| 性能问题 | `performance-doctor` |

## Grafana Service Account Token 创建

每个 Grafana 环境需要独立创建 Token：

1. 登录对应 Grafana URL
2. 左侧菜单 → Administration → Service accounts
3. Add service account（名称：`claude-loki-reader`），角色：`Viewer`
4. Add service account token → 复制
5. 更新 `environments.json` 中对应环境的 `token` 字段

## 注意

- 如果 Token 为空会报 `invalid API key`，需要先为该环境创建 Token
- 查询默认不限 project，可覆盖该 Grafana 下所有项目环境
- `direction=forward` 按时间正序，`direction=backward` 按时间倒序（最新优先）
- 如果是 Bug 排查完整流程，同时使用 `bug-detective`
