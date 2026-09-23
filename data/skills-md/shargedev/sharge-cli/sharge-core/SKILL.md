---
name: sharge-core
description: 通过 sharge CLI 发现命令、检查登录与 scope、处理配置、诊断、JSON envelope、安全门禁和错误恢复。用于任何 Sharge 任务的公共前置步骤，以及登录、退出、auth、config、doctor 或 logs 请求；不负责 Notes、Calendar、Recordings、Diary 的业务选路和内容决策。
---

# Sharge Core

以可靠完成用户任务为目标，不把 Skill 当作命令目录。Sharge 没有 `schema` 命令；当前安装版本的 `--help --json` 是发生不确定或冲突时的事实源，不是每次调用的固定前置。

## Help 决策

- 领域 Skill 已给出稳定读入口，且意图和输入明确时，直接执行，不读取 root、namespace 或具体命令 help。
- 写入、删除、下载、结构化输入和 dry-run 等风险操作，只读取对应的具体命令 help；不要先遍历 namespace。
- 只有动作未明确、Skill 未明确分类能力边界，或用户要求发现当前能力时，才读取相关 namespace help。
- Skill 已明确排除且校验过的能力，直接说明不支持和未执行；不要用 help 重复确认同一边界。
- 参数错误或 Skill 与当前版本疑似漂移时，按 error envelope 查看对应具体 help，不从 root 重新扫描。

## 统一执行序列

1. 识别用户意图。
2. 选择领域与动作。
3. 读取本 Skill 和领域 Skill 直接链接的条件 reference。
4. 按 Help 决策直接执行，或只读取能消除当前不确定性的 help。
5. 检查鉴权、输入和风险。
6. 只有 JSON help 声明 `dryRun: true` 时才预演，否则执行。
7. 同时解析进程退出码和 envelope。
8. 报告结果，或按结构化恢复提示继续。

用机器可读结果检查当前登录状态：

```sh
sharge auth status --json
```

## 共享安全契约

- 业务命令不会隐式登录。缺凭证时停止业务调用；登录必须是用户明确请求，或是符合原任务的恢复动作。
- 遇到 `SCOPE_REQUIRED` 时读取 `requiredScopes` 和 `nextActions.command`。该登录命令表达完整目标 scope 集合；执行前核对授权范围，不自行删减已有 scope。
- 机器消费显式使用 `--json`，同时检查退出码与 `ok`；不要解析中文 `message` 做逻辑判断。
- 保持 opaque ID、identifier、instance ID 和 cursor 的原始表示，不转换为可能失真的 Number，不重编码或推断内部结构。
- 列表一次只读取一页，不自动翻页。只有任务确实需要后续页时，才使用当前响应返回的 cursor 显式继续。
- 真实删除先确认明确的用户删除意图，再使用 `--yes`；不能把确认错误当成自动授权。
- 只有用户明确允许覆盖指定目标时才使用 `--overwrite`。普通重名让 CLI 选择安全后缀，并采用返回的 `data.filePath`。
- API Key、polling token、settings 全文和签名下载 URL 不得暴露到对话、命令参数、日志摘录、持久化文件或测试快照。
- 写请求出现 `outcome: "unknown"` 时绝不自动重发。先用相应读命令确认远端状态，再决定是否继续。
- `retryable` 是考虑重试的必要条件，不是重试指令。还要确认 help 声明重复执行安全、unknown outcome 已解决，并且重试仍符合用户意图。
- CLI 和 Skill 都不自动重试 network、timeout、429 或 5xx。登录轮询和下载 redirect 是协议步骤，不是业务重试。

## 输入与结果

- 风险操作前读取具体命令的 JSON help；flags 与 `--input` 二选一，只有 `--input -` 读取 stdin。
- `nextActions` 只是候选恢复动作。执行前检查其授权、文件和远端副作用是否仍符合原任务。
- 成功时报告完成的业务结果；失败时报告稳定 `error.type`、是否可恢复和下一步。下载只以返回的绝对 `filePath` 为准。
- 用户询问安装或本机尚无 `sharge` 可执行文件时，转到仓库当前 README/发布说明；发布路径未确定前不得猜安装 URL、包名或执行远端安装脚本。

## Handoff

- 闪记、Quick Note、Live Photo、AI Live Photo 或相关媒体交给 [sharge-notes](../sharge-notes/SKILL.md)。
- 日历事件、待办、日历月份或时间范围交给 [sharge-calendar](../sharge-calendar/SKILL.md)。
- 录音、逐字稿、overview、highlight 或音频交给 [sharge-recordings](../sharge-recordings/SKILL.md)。
- 日记、AI Daily、明确日记月份或 `YYYYMMDD` 交给 [sharge-diary](../sharge-diary/SKILL.md)。仅说“月份”而没有资源领域时先澄清。
- 恢复登录或 scope 后回到原领域和动作；不要把恢复本身误报为用户任务已完成。
