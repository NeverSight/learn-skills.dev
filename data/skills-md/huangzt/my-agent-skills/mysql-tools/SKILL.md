---
name: mysql-tools
description: "MySQL 数据库工具集，用于连接数据库实例、列出所有表、查看表结构、执行 SQL 查询等操作。当需要操作 MySQL 数据库、查询数据、分析表结构时使用此技能。支持通过命令行参数指定 host、port、user、password、database 等连接信息，可代替 mysql mcp 服务使用。支持 Windows、macOS 和 Linux 平台。"
---

# MySQL 工具 Skill

用于操作 MySQL 数据库的工具集，提供连接测试、表管理和 SQL 执行功能。

## 快速开始

### 前置要求

```bash
pip install pymysql
```

### 平台兼容性

- ✅ Windows
- ✅ macOS
- ✅ Linux

### 连接参数

所有脚本支持以下参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host` | 数据库主机地址 | localhost |
| `--port` | 数据库端口 | 3306 |
| `--user` | 数据库用户名 | root |
| `--password` | 数据库密码 | 必填 |
| `--database` | 数据库名称 | 必填 |

## 可用脚本

### 1. 测试数据库连接

验证数据库连接参数是否正确：

```bash
python scripts/mysql_connect.py --host 127.0.0.1 --port 3306 --user root --password YOUR_PASSWORD --database YOUR_DB
```

### 2. 列出所有表

获取数据库中的所有表名：

```bash
python scripts/mysql_tables.py --host 127.0.0.1 --user root --password YOUR_PASSWORD --database YOUR_DB
```

输出格式：表名列表，包含表类型（BASE TABLE / VIEW）

### 3. 查看表结构

显示指定表的字段信息：

```bash
python scripts/mysql_schema.py --host 127.0.0.1 --user root --password YOUR_PASSWORD --database YOUR_DB --table TABLE_NAME
```

输出格式：字段名、类型、是否可空、键类型、默认值、额外信息

### 4. 执行 SQL 查询

运行任意 SQL 语句：

```bash
python scripts/mysql_query.py --host 127.0.0.1 --user root --password YOUR_PASSWORD --database YOUR_DB --query "SELECT * FROM users LIMIT 10"
```

支持 SELECT、INSERT、UPDATE、DELETE 等所有 SQL 语句。

### 5. 查看数据库信息

获取数据库版本、大小等信息：

```bash
python scripts/mysql_info.py --host 127.0.0.1 --user root --password YOUR_PASSWORD --database YOUR_DB
```

## 输出格式

所有脚本输出 JSON 格式数据，便于解析：

```json
{
  "success": true,
  "data": [...],
  "message": "操作成功"
}
```

错误时返回：

```json
{
  "success": false,
  "error": "错误信息",
  "message": "操作失败"
}
```

## 常见用例

### 探索新数据库

1. 测试连接：`mysql_connect.py`
2. 列出所有表：`mysql_tables.py`
3. 查看关键表结构：`mysql_schema.py --table TABLE_NAME`
4. 查询示例数据：`mysql_query.py --query "SELECT * FROM TABLE_NAME LIMIT 5"`

### 数据分析

1. 获取表记录数：`mysql_query.py --query "SELECT COUNT(*) FROM TABLE_NAME"`
2. 分析数据分布：`mysql_query.py --query "SELECT column, COUNT(*) FROM TABLE_NAME GROUP BY column"`

### 参考更多 SQL 示例

查看 `references/common_queries.md` 获取常用 SQL 查询模板。
