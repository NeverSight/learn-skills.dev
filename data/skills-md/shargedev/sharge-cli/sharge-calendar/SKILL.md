---
name: sharge-calendar
description: 通过 sharge CLI 按明确月份或时间范围读取、搜索和查看日历资源，并结构化创建、更新、删除事件或修改待办状态。用于用户提到日历事件、待办、重复实例、日历月份、带 offset 的事件时间范围或 Calendar ID 时；不负责解析自然语言时间、管理闪记/录音/日记内容或猜测实例范围。
---

# Sharge Calendar

开始任何 CLI 动作前完整读取 [sharge-core](../sharge-core/SKILL.md)，并继承其中的发现、安全和恢复规则。

## 范围

处理 Calendar 的 month/list/search/get、结构化 create/update/delete 和 todos set-status。所有时间、月份、timezone、重复实例范围和 opaque instance ID 都必须由用户输入或可靠 CLI 结果确定。

## 最短路径

意图和必要时间输入明确时，直接执行稳定读取，不先读取 namespace 或具体命令 help：

```sh
sharge calendar month 2026-08 --json
sharge calendar list --start 2026-08-01T00:00:00+08:00 --end 2026-09-01T00:00:00+08:00 --json
sharge calendar search "项目评审" --json
sharge calendar get 123 --json
```

## 执行

创建、更新、删除或修改待办状态前，只读取对应的具体命令 help，确认 input schema、`dryRun`、`destructive`、`retrySafe` 和 required scopes：

```sh
sharge calendar create --help --json
sharge calendar update --help --json
sharge calendar delete --help --json
sharge calendar todos set-status --help --json
```

按具体 help 生成复杂输入并优先执行零网络 dry run；不要混用业务 flags 与 `--input`。随后按 core 的统一序列执行并解析 envelope。

## 领域规则

- month 必须使用明确 `YYYY-MM`；list 的 start/end 必须是带 offset 的 RFC 3339。不要猜“今天”、月份、timezone 或把自然语言直接传给 v1 CLI。
- create/update 使用具体 help 的当前结构。update 是完整更新；保留字段也要按 input schema 提供，不把它误当 patch。
- instance/future 等重复实例操作只使用 CLI 返回的 opaque instance ID，不拆解或自行构造。
- 真实 delete 先确认目标和作用范围，再加 `--yes`；dry run 可先核对 side effects。todo status 同样属于写操作。
- create/update/delete/todo 写请求若出现 unknown outcome，先用明确 get/list/search 范围核对远端状态，不自动重发。

## Handoff

- 鉴权、scope、配置、envelope 和通用恢复交给 [sharge-core](../sharge-core/SKILL.md)，恢复后回到本 Skill。
- 任务要求从闪记、录音或日记提取内容时，先交给 [sharge-notes](../sharge-notes/SKILL.md)、[sharge-recordings](../sharge-recordings/SKILL.md) 或 [sharge-diary](../sharge-diary/SKILL.md) 获取最小必要结果；回到 Calendar 后重新确认时间、目标和写入风险。
- 过去录音的逐字稿或总结不是日历详情，交给 [sharge-recordings](../sharge-recordings/SKILL.md)。
