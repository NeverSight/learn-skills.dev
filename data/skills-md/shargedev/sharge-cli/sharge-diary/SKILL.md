---
name: sharge-diary
description: 通过 sharge CLI 按明确月份列出和搜索 daily Diary，并按 YYYYMMDD 读取日记与 Open Platform Markdown。用于用户提到日记、AI Daily、日记月份、明确日记日期或日记 Markdown 时；不负责 weekly/monthly 报告、生成、更新、删除日记或管理闪记与录音。
---

# Sharge Diary

开始任何 CLI 动作前完整读取 [sharge-core](../sharge-core/SKILL.md)，并继承其中的发现、安全和恢复规则。

## 范围

处理 daily Diary 的 month list、search 和按真实日期 get。当前不存在 `diary weekly`、`diary monthly`、`diary generate`、`diary update` 或 `diary delete`；遇到这些请求，直接说明当前只公开 daily、不支持且未执行。

## 最短路径

月份、日期或搜索词明确时，直接执行稳定读取，不先读取 namespace 或具体命令 help：

```sh
sharge diary list 2026-08 --json
sharge diary search "上海" --json
sharge diary get 20260730 --json
```

## 执行

Diary 当前只有稳定读操作。Skill 已给出动作和输入格式时直接执行；只有请求未明确分类、参数报错或当前版本疑似漂移时，才读取对应 namespace 或具体命令 help。随后按 core 的统一序列执行并解析 envelope。

## 领域规则

- list 的月份必须是明确、真实的 `YYYY-MM`；get 的 identifier 必须是明确、真实的 `YYYYMMDD`。
- v1 不解析自然语言时间。若用户只说“昨天”或“上个月”，先依据明确 timezone 计算并向用户展示解析结果，不把自然语言直接传给 CLI。
- 保持 Open Platform Markdown 与业务字段原样；不要把 Diary 正文改造成 Notes、Recordings 或内部 schema。
- Diary 是只读领域。遇到生成、更新、删除或 weekly/monthly 请求时说明当前公共能力边界，不构造未来命令。

## Handoff

- 鉴权、scope、配置、envelope 和通用恢复交给 [sharge-core](../sharge-core/SKILL.md)，恢复后回到本 Skill。
- 用户明确要把日记内容用于 Note 或 Calendar 时，只读取和传递任务所需内容到 [sharge-notes](../sharge-notes/SKILL.md) 或 [sharge-calendar](../sharge-calendar/SKILL.md)；目标 Skill 重新确认任何写入风险。
- 逐字稿、说话人和录音音频交给 [sharge-recordings](../sharge-recordings/SKILL.md)。
