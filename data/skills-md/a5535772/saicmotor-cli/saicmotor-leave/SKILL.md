---
name: saicmotor-leave
version: 1.0.0
description: "请假系统：查询年假余额、提交请假申请。当用户需要请假、查年假余额、提交请假申请时使用。不负责：考勤打卡（走 saicmotor-attendance）。"
metadata:
  requires:
    bins: ["saicmotor"]
  cliHelp: "saicmotor leave --help"
---

# 请假 (leave)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../saicmotor-shared/SKILL.md`](../saicmotor-shared/SKILL.md)，其中包含认证、配置处理。**

## Shortcuts

| Shortcut | 说明 |
|----------|------|
| `balance query` | 查询当前用户年假余额 |
| `applications submit` | 提交请假申请（写操作，需要 `--yes`） |

## 编排规则

请年假必须按两步走，不可跳过：

1. **先查余额**：`saicmotor leave balance query`
2. **确认够再提交**：余额充足才执行 `saicmotor leave applications submit`

余额不足时告知用户当前余额，不执行提交。用户未明确说"先帮我查余额"时也要主动先查——**这是硬规则，不允许跳过**。

## 命令详情

### `balance query` — 查年假余额

```bash
saicmotor leave balance query
```

返回：

| 字段 | 类型 | 说明 |
|------|------|------|
| `annual_balance` | integer | 年假总额（天） |
| `used` | integer | 已用天数 |

用法提示：
- 无参数，直接返回当前登录用户的余额。
- 提交请假申请前必须先执行此命令确认余额。

### `applications submit` — 提交请假申请

```bash
saicmotor leave applications submit --start-date <开始日期> --end-date <结束日期> --reason <请假事由> --yes
```

参数：

| 参数 | 必填 | 格式 | 说明 |
|------|------|------|------|
| `--start-date` | 是 | `YYYY-MM-DD` | 请假开始日期 |
| `--end-date` | 是 | `YYYY-MM-DD` | 请假结束日期 |
| `--reason` | 是 | 字符串 | 请假事由 |

返回：

| 字段 | 类型 | 说明 |
|------|------|------|
| `application_id` | string | 申请单号 |
| `status` | string | 状态（`PENDING` = 待审批） |

**⚠️ 重要**：这是写操作（POST），必须加 `--yes` 确认，或加 `--dry-run` 预览请求不发送。

## 写操作确认

所有 `applications submit` 会产生副作用（提交请假申请），默认要求 `--yes`：

```bash
# 正确：加 --yes
saicmotor leave applications submit --start-date 2026-09-21 --end-date 2026-09-22 --reason 年假 --yes

# 预览：只预览不发送
saicmotor leave applications submit --start-date 2026-09-21 --end-date 2026-09-22 --reason 年假 --dry-run

# 错误：不加 --yes 会被拒绝
saicmotor leave applications submit --start-date 2026-09-21 --end-date 2026-09-22 --reason 年假
```

## 输出格式

```bash
# JSON（默认）
saicmotor leave balance query --format json
# > {"ok":true,"data":{"annual_balance":5,"used":3}}

# 表格
saicmotor leave balance query --format table

# 美化
saicmotor leave balance query --format pretty
```

## 术语映射

用户日常说的"请假""休年假""调休""请个假"，实际意图都是对请假系统的操作。自动将口语化的请假意图映射为本 skill 的命令。

## 不在本 skill 范围

- 打卡记录、补卡 → [saicmotor-attendance](../saicmotor-attendance/SKILL.md)
- 登录/登出/配置 → [saicmotor-shared](../saicmotor-shared/SKILL.md)

**注意（强制性）：**
- 日期参数必须使用 `YYYY-MM-DD` 格式。
- 涉及日期计算时，必须显式指定时区，禁止依赖容器默认时区。