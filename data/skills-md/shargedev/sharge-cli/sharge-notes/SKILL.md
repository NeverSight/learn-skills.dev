---
name: sharge-notes
description: 通过 sharge CLI 读取、搜索、查看、更新、删除 Notes 并下载其媒体。用于用户提到闪记、Quick Note、Live Photo、AI Live Photo、Note ID、标题/正文或相关音频/图片/视频时；不负责创建 Note、管理日历事件或处理录音与日记资源。
---

# Sharge Notes

开始任何 CLI 动作前完整读取 [sharge-core](../sharge-core/SKILL.md)，并继承其中的发现、安全和恢复规则。

## 范围

Notes 是 Quick Note、闪记、Live Photo 和 AI Live Photo 的统一 CLI 领域，规范 namespace 始终是 `notes`。处理单页 list/search、get、部分 update、delete 和 media download。当前不存在 `notes create`；遇到创建请求，直接说明不支持且未执行，不构造未来命令或把相邻产品当作兼容别名。

## 最短路径

意图和必要输入明确时，直接执行稳定读取，不先读取 namespace 或具体命令 help：

```sh
sharge notes list --json
sharge notes search "发布计划" --json
sharge notes get 123 --json
```

## 执行

更新、删除或下载前只读取对应的具体命令 help；不要先读取 namespace help：

```sh
sharge notes update --help --json
sharge notes delete --help --json
sharge notes download --help --json
```

随后按具体 help 和 core 检查 auth/input/risk；支持 dry-run 时可先预演，但预演不代表远端资源已验证。

## 领域规则

- list/search 只读取一页。续页只使用当前响应的精确 cursor，不把大整数 ID 或 cursor 转成 Number。
- update 是现有 Note 的部分更新；业务 flags 与 `--input` 互斥，正文或标题是否清空以具体 help/input schema 为准。
- 真实 delete 必须同时具备明确删除意图和 `--yes`；dry run 不需要 `--yes`。
- download 的媒体类型、是否支持 dry run 和目标 option 以具体 help 为准。未指定显式文件时读取成功结果的绝对 `filePath`；仅在用户明确允许覆盖时添加 `--overwrite`。
- 传输失败若带 unknown outcome，先执行 get/search 核对状态，不直接重发 update/delete。

## Handoff

- 鉴权、scope、配置、envelope 和通用恢复交给 [sharge-core](../sharge-core/SKILL.md)，恢复后回到本 Skill。
- 用户明确要把 Note 内容创建为日程时，先完成最小必要读取，再把内容与 opaque Note ID 交给 [sharge-calendar](../sharge-calendar/SKILL.md)，由 Calendar 重新确认写入风险。
- 录音与日记请求分别交给 [sharge-recordings](../sharge-recordings/SKILL.md)、[sharge-diary](../sharge-diary/SKILL.md)；不要把相似文本内容当作同一资源。
