---
name: mysql-debug
description: |
  MySQL 数据库查询调试技能。通过 mysql CLI 直接查询本地 MySQL 数据库，配合日志进行 Bug 排查。
  Bug 修复时自动评估是否需要查库，从日志中提取数据库名（租户ID），支持手动指定数据库。

  触发场景：
  - 结合日志排查 Bug 时需要查询数据库验证数据
  - 检查数据库中某条记录的实际值
  - 验证 SQL 执行结果是否符合预期
  - 排查数据不一致、数据丢失、数据异常问题
  - 需要查看表结构、索引、数据分布

  触发词：查数据库、查表、执行SQL、查记录、mysql查询、数据库排查、验证数据、查数据、db查询、数据库调试
---

# MySQL 数据库查询调试技能

## 概述

本技能用于在 Bug 排查过程中直接查询 MySQL 数据库，验证数据状态。配合日志分析定位问题根因。

**核心能力**：
1. 智能判断 Bug 是否需要查库（明显代码错误跳过）
2. 从日志自动提取数据库名（租户 ID = 数据库名）
3. 只读查询，安全排查

---

## 连接信息获取（三级降级，自动查找）

当本技能被激活时，**按以下优先级获取数据库连接信息**：

### 优先级 1：用户对话中指定（最高优先级）

用户直接给出连接信息，或指定环境名：
- "连 dev 环境查一下" → 使用 `.claude/mysql-config.json` 中 dev 环境的配置
- 直接给出 host/port/user/password → 直接使用

### 优先级 2：`.claude/mysql-config.json`（显式配置，可选）

如果文件存在且当前环境的 password 不是占位符 `YOUR_PASSWORD`，使用该配置。
**此文件为可选**，主要用于连接非本地环境（dev/prod 远程数据库）。

### 优先级 3：工程配置文件（零配置，本地开发默认）

从项目的 `bootstrap-dev.yml` 中自动提取连接信息：

**搜索路径**：
```
**/bootstrap-dev.yml
**/bootstrap*.yml（降级）
```

**解析位置**：`spring.dataset.system.master` 节点

**解析规则**：
```yaml
# 从以下字段提取：
jdbcUrl: jdbc:mysql://127.0.0.1:3306/system_xxx
username: root
password: xxx
```

**提取结果**：
- host = `127.0.0.1`（从 jdbcUrl 解析）
- port = `3306`（从 jdbcUrl 解析）
- user = `root`（username 字段）
- password = `xxx`（password 字段）
- 注意：jdbcUrl 中的数据库名（`system_xxx`）为系统库，**不作为查询目标数据库**。查询目标数据库 = 租户ID（从日志提取或用户指定）

### mysql CLI 查找（多路径）

按顺序查找 mysql 客户端：

```bash
which mysql \
  || ls /usr/local/mysql/bin/mysql \
  || ls /opt/homebrew/bin/mysql \
  || ls /opt/homebrew/opt/mysql-client/bin/mysql
```

找到任一即可使用。如果全部不存在，输出安装提示：
```
brew install mysql-client
```

### 引导提示（仅当连接信息和 mysql CLI 都无法获取时）

```
⚠️ 数据库查询功能需要先完成配置：

1. 连接信息获取失败：
   - 未找到 bootstrap-dev.yml 工程配置文件
   - 未找到 .claude/mysql-config.json 配置文件
   → 请创建 .claude/mysql-config.json 或确保项目中存在 bootstrap-dev.yml

2. 安装 MySQL 客户端：
   brew install mysql-client

完成后重新触发即可使用数据库查询辅助排查。
```

> 引导提示输出后，Bug 排查仍可继续（走 bug-detective 纯代码分析路径），只是跳过数据库查询环节。

---

## 多环境支持

### 配置文件结构

`.claude/mysql-config.json` 支持多环境配置：

```json
{
  "environments": {
    "local": { "host": "127.0.0.1", "port": 3306, "user": "root", "password": "xxx" },
    "dev":   { "host": "dev-db.example.com", "port": 3306, "user": "dev_user", "password": "xxx" },
    "prod":  { "host": "prod-db.example.com", "port": 3306, "user": "readonly", "password": "xxx" }
  },
  "default": "local"
}
```

### 环境选择规则

| 优先级 | 来源 | 示例 |
|--------|------|------|
| 1（最高） | 用户对话中指定 | "连 dev 环境查一下"、"用生产库看看" |
| 2 | 配置文件 `default` 字段 | `"default": "local"` |

### 环境关键词映射

用户说的话 → 对应环境名：

| 用户说法 | 环境 |
|---------|------|
| "本地"、"local"、"本地环境" | `local` |
| "开发"、"dev"、"测试环境"、"开发环境" | `dev` |
| "生产"、"prod"、"线上"、"正式环境" | `prod` |

### 连接示例

```bash
# 用户说"连 dev 环境查一下 order_info"
# → 读取 environments.dev 的连接信息 + 日志提取的数据库名
mysql -h dev-db.example.com -P 3306 -u dev_user -p'xxx' 546198574447230976 -e "SELECT ..."
```

---

## 核心流程：是否需要查库？

### 决策树（Bug 修复时必须先评估）

```
用户报告 Bug / 提供日志
  │
  ├─ 明显的代码错误？ ──→ ✅ 不需要查库，直接修复
  │   - NPE 且代码中未做空判断
  │   - 语法错误、拼写错误
  │   - 类型转换错误（ClassCastException）
  │   - 缺少 import、注解遗漏
  │   - 方法签名不匹配
  │
  ├─ 数据相关的问题？ ──→ 🔍 需要查库
  │   - "查不到数据"、"数据为空"
  │   - "数量不对"、"金额不对"
  │   - SQL 相关异常（DataIntegrityViolation、DuplicateKey）
  │   - 关联查询结果异常
  │   - 状态流转异常（订单状态不对等）
  │
  ├─ 不确定是代码还是数据？ ──→ 🔍 需要查库确认
  │   - 逻辑正确但结果错误
  │   - 特定租户/特定数据才出现的 Bug
  │   - 生产有问题但本地无法复现
  │
  └─ 配置/环境问题？ ──→ ✅ 不需要查库
      - 启动失败、Bean 创建异常
      - 配置文件错误
      - 依赖版本冲突
```

### 评估输出格式

在 Bug 修复响应中，先输出评估结论：

```
📊 数据库查询评估：需要查库
理由：日志显示 order_info 查询返回空，需要确认数据是否存在
数据库：546198574447230976（从日志提取）
```

或：

```
📊 数据库查询评估：不需要查库
理由：明显的 NPE，代码中 getUserInfo() 返回值未做空判断
```

---

## 从日志提取数据库名

### 日志格式说明

本项目的日志格式：

```
2026-03-04 10:21:40.902,-,546198574447230976,, DEBUG 94396 --- [  XNIO-1 task-3] n.x.f.c.request.RequestLoggingFilter : 47  : >>> GET /api/v2/web/xxx
```

各字段含义：

```
时间戳                    ,-,租户ID（=数据库名）,, 日志级别 PID --- [线程名] 类名 : 行号 : 日志内容
```

### 提取规则

1. **自动提取**：从日志行中匹配 `,-,(\d{15,19}),,` 模式，提取的数字即为数据库名
2. **手动指定**：用户直接说"查 546198574447230976 库"或"数据库名是 xxx"
3. **优先级**：手动指定 > 日志提取 > 配置文件 default

### 提取示例

```
日志：2026-03-04 10:21:40.902,-,546198574447230976,, DEBUG ...
                                ↑
                          数据库名 = 546198574447230976
```

连接时使用：
```bash
mysql -h 127.0.0.1 -P 3306 -u root -p'password' 546198574447230976 -e "SELECT ..."
```

---

## 查询执行

### 连接方式

按"连接信息获取"章节的优先级获取 host/port/user/password，数据库名从日志提取或用户指定：

```bash
# 连接信息来源：用户指定 > mysql-config.json > bootstrap-dev.yml 自动提取
# 数据库名来源：用户指定 > 日志提取的租户ID
mysql -h {host} -P {port} -u {user} -p'{password}' {database_from_log_or_user} -e "{SQL}"

# mysql 路径：如果 which mysql 失败，尝试绝对路径
/opt/homebrew/opt/mysql-client/bin/mysql -h {host} ...
```

### 常用排查查询模板

#### 查看表结构
```sql
DESCRIBE table_name;
SHOW CREATE TABLE table_name;
```

#### 按 ID 查记录
```sql
SELECT * FROM table_name WHERE id = {id} AND del_flag = 2;
```

#### 查看最近修改的数据
```sql
SELECT * FROM table_name
WHERE uptime >= '{log_timestamp}'
ORDER BY uptime DESC
LIMIT 20;
```

#### 检查关联数据一致性
```sql
SELECT a.id, b.id AS related_id
FROM table_a a
LEFT JOIN table_b b ON a.related_id = b.id
WHERE a.id = {id} AND b.id IS NULL;
```

#### 统计数据分布
```sql
SELECT status, COUNT(*) as cnt
FROM table_name
WHERE del_flag = 2
GROUP BY status;
```

#### 查看某时间段的操作记录
```sql
SELECT * FROM table_name
WHERE crtime BETWEEN '{start}' AND '{end}'
ORDER BY crtime DESC
LIMIT 50;
```

---

## 安全规范（强制执行，违反即终止）

### 允许执行的 SQL（白名单）

**只允许以下语句类型**：
- `SELECT` — 查询数据
- `DESCRIBE` / `DESC` — 查看表结构
- `SHOW` — 查看建表语句、索引、状态等
- `EXPLAIN` — 分析执行计划

### 禁止执行的 SQL（黑名单）

**DDL 操作 — 全部禁止**：
- `CREATE TABLE / VIEW / INDEX / DATABASE`
- `ALTER TABLE / COLUMN`
- `DROP TABLE / VIEW / INDEX / DATABASE`
- `TRUNCATE TABLE`
- `RENAME TABLE`

**DML 写操作 — 全部禁止**：
- `INSERT` — 禁止插入数据
- `UPDATE` — 禁止更新数据
- `DELETE` — 禁止删除数据
- `REPLACE` — 禁止替换数据

**权限/管理操作 — 全部禁止**：
- `GRANT / REVOKE`
- `SET GLOBAL`
- `FLUSH`

### 敏感 SQL 拦截（执行前必须分析）

在执行任何 SQL 之前，必须进行安全分析。遇到以下情况时，**不执行 SQL，改为输出分析结果并询问用户**：

| 风险类型 | 检测规则 | 处理方式 |
|---------|---------|---------|
| 无 WHERE 全表扫描 | `SELECT * FROM xxx` 无 WHERE 子句 | 提醒用户加条件，或自动加 `LIMIT 10` |
| 大范围查询 | WHERE 条件覆盖范围过大（如 `del_flag = 2`） | 提醒加更精确条件，强制 `LIMIT 50` |
| 多表 JOIN 无条件 | JOIN 无 ON 条件（笛卡尔积） | 拒绝执行，提示补充 JOIN 条件 |
| 子查询嵌套过深 | 超过 3 层嵌套子查询 | 输出 SQL 让用户确认后再执行 |
| 敏感表查询 | 涉及用户密码表、密钥表 | 输出脱敏后的 SQL 分析，不直接查询 |

### 执行前检查流程

```
收到/构造 SQL
  │
  ├─ 是否在白名单内？ ──→ 否 → 拒绝执行，输出原因
  │
  ├─ 是否命中敏感规则？ ──→ 是 → 输出风险分析，询问用户
  │
  ├─ 是否包含 LIMIT？ ──→ 否 → 自动追加 LIMIT 50
  │
  └─ 通过所有检查 → 执行 SQL
```

### 查询结果安全

- 查询必须加 `LIMIT`（默认 LIMIT 50）防止返回过多数据
- 不在输出中暴露密码、手机号（phone）、身份证（id_card）等敏感字段
- 查询结果中的敏感字段用 `***` 脱敏展示
- 如需修改数据，**只输出 SQL 语句让用户手动执行**，不代为执行

### 配置文件安全

- `.claude/mysql-config.json` 已加入 `.gitignore`，禁止提交到版本库

---

## 与 bug-detective 配合

本技能是 `bug-detective` 的数据层扩展。当 bug-detective 被触发时，会自动评估是否需要同时激活 mysql-debug：

| 步骤 | bug-detective | mysql-debug |
|------|--------------|-------------|
| 1 | 分析日志、定位异常层 | 评估是否需要查库 |
| 2 | 识别涉及的表和查询 | 从日志提取数据库名 |
| 3 | 推断可能原因 | 执行 SQL 验证数据 |
| 4 | 给出修复方案 | 用数据证实/排除假设 |

典型联合使用：
```
用户："订单查询接口返回空数据，日志如下..."
日志：2026-03-04 10:21:40.902,-,546198574447230976,, ERROR ...

→ 评估：需要查库（数据返回空，需确认数据是否存在）
→ 提取数据库：546198574447230976
→ 执行：SELECT * FROM order_info WHERE id = xxx AND del_flag = 2
→ 发现：del_flag = 1（已删除），用户操作了删除但不知情
→ 修复方案：恢复数据 / 检查前端删除按钮权限
```

---

## 注意

- 本技能专注于**查询数据库辅助排查**，不涉及建表、迁移等操作（请使用 `database-ops`）
- 如果是纯代码错误（NPE、语法错误等）不需要查库，请使用 `bug-detective`
- 如果是 SQL 性能问题（慢查询），请使用 `performance-doctor`
