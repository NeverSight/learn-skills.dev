---
name: sharge-recordings
description: 通过 sharge CLI 单页列出和搜索录音、读取逐字稿/overview/highlight 等富详情，并安全下载录音音频。用于用户提到录音、Recording ID、录音说话人/逐字稿/总结/高亮或录音音频时；不负责上传、修改、删除、重新转写录音或管理日历和日记。
---

# Sharge Recordings

开始任何 CLI 动作前完整读取 [sharge-core](../sharge-core/SKILL.md)，并继承其中的发现、安全和恢复规则。

## 范围

处理 Recordings 的单页 list、search、富详情 get 和 audio download。当前不存在 `recordings upload`、`recordings update`、`recordings delete`、`recordings transcribe` 或 `recordings regenerate`；遇到这些请求，直接说明只读、不支持且未执行。

## 最短路径

意图和必要输入明确时，直接执行稳定读取，不先读取 namespace 或具体命令 help：

```sh
sharge recordings list --json
sharge recordings search "项目复盘" --json
sharge recordings get 456 --json
```

## 执行

下载前只读取具体命令 help，确认 dry-run、目标文件和覆盖契约；不要先读取 namespace help：

```sh
sharge recordings download --help --json
```

随后按具体 help 和 core 的统一序列执行；支持时可用零网络 dry run 计划路径。

## 领域规则

- list 一次只读取一页。需要更多结果时使用响应的 next/prev cursor 和 direction，不猜 cursor，也不自动拉全量。
- get 返回的 transcript、overviews、speaker map 和 highlights 可能包含动态字典；保持业务字段和键原样，不递归改名。
- download 不把二进制写到 stdout。未指定显式目标时采用返回的绝对 `filePath`；仅在用户明确允许覆盖指定路径时使用 `--overwrite`。
- 读取失败只在 `retryable: true` 且仍符合任务时考虑重试；CLI 不提供重新转写或重新总结作为恢复动作。

## Handoff

- 鉴权、scope、配置、envelope 和通用恢复交给 [sharge-core](../sharge-core/SKILL.md)，恢复后回到本 Skill。
- 用户明确要求把录音结论写入 Note 或 Calendar 时，先完成读取，再把最小必要内容与原始 Recording ID 交给 [sharge-notes](../sharge-notes/SKILL.md) 或 [sharge-calendar](../sharge-calendar/SKILL.md)；目标 Skill 重新确认写入意图。
- 日记内容交给 [sharge-diary](../sharge-diary/SKILL.md)，不要因为两者都有总结文本就混用资源。
