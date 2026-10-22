---
name: ae-things-progress
description: "工作空间事项进展、日报和周报：使用 ae-cli things 采集当前空间、负责人或显式事项集合的周期事实，由当前会话模型归纳并披露数据边界。"
---

# 事项进展汇总

从 aha-links 的事实采集和输出契约适配；先读 [事项操作](../ae-things/SKILL.md) 和 [CLI reference](../ae-things/references/cli.md)。CLI 收事实，当前模型做归纳，不调用独立报告后台。

涉及本轮绑定事项时，先遵循 [执行快照与实时上下文](../ae-things/references/cli.md#执行快照与实时上下文) 读取本次执行快照，再按以下流程采集最新审查或周期事实；两种来源分开表述。无绑定时仅使用用户明确指定的范围。

## 范围和时间

```bash
ae-cli things +digest --agent-space-id <space-id> --from 2026-09-07T00:00:00+08:00 --to 2026-09-14T00:00:00+08:00 --time-zone Asia/Shanghai --format json
ae-cli things +digest --agent-space-id <space-id> --assignee-id <member-id> --format json
ae-cli things +digest --agent-space-id <space-id> --thing-ids <id-a>,<id-b> --format json
```

不猜 ID、不选择个人默认空间；不支持关注清单、群或跨空间汇总。日报按自然日，周报按周一 00:00 到下周一 00:00，默认 Asia/Shanghai。今日／本周的截止点用当前时刻，昨日／上周用完整周期。自定义区间必须明确；命令的 from/to 都必须含时区，区间为左闭右开。

输出时将记录的 ISO 时间转换为报告时区，并在时间窗、采集时间和证据日期旁明确标注时区。例：`2026-09-10T04:50:00Z` 在 Asia/Shanghai 应展示为 `2026-09-10 12:50（Asia/Shanghai）`；不能删除 Z 后直接写成“上海时间 04:50”。无法可靠转换时保留原始 ISO 并标注 UTC，披露尚未转换，不能伪造本地时刻。

## 证据和完整性

核对 `fetchedCount`、`truncated`、`consistency`、`collectedAt`；显式集合再核对 `requestedCount` 和 `unreadable`。字段缺失停止生成全量结论。CLI 自动分页最多每链 100 页／10000 项，异常和上限会标记截断；不能换成单页 list 冒充完整采集。

- `thing` 是当前状态，`entries` 是时间窗内记录，`baseline` 是利用完整业务变更记录倒推的窗口前状态；没有基线或采集发生版本变化时不要补造。
- `lastEffectiveRecordBeforeWindow` 供定位窗口前证据。当前状态不等于周期内变化，周期末状态也不能直接用当前状态代替。
- 输出前比较 `collectedAt` 与窗口 `to`。当 `collectedAt < to`（包括用户指定尚未结束的完整自然周）时，报告必须注明“截至采集时刻的阶段汇总，周期尚未结束”；三态统计标为“采集时状态”，禁止写“周期末状态”或“无后续更新”。例：9月10日采集9月7日至14日的周报，不能断言9月14日状态与当前相同。即使窗口已经结束，也只有完整的窗口后变更证据支持时才能还原周期末状态。
- open/paused/done 分别统计，归档另列；最新进展来自 thing.latestProgress，历史变化读取 progress/status 记录。
- 备注和重复过程描述不算有效进展；`effectiveProgressCount` 是待核查候选，正文没有新信息时排除。
- 没有记录只能说“未记录更新”。此约束同样适用于摘要和下一步建议；open 不能证明尚未开始，只能报告当前状态和未记录事实。附件未读、不可读取、截断及多次请求的非事务采集边界必须披露。`changed_during_collection` 时先重读；仍有变化则保留限制，不声称静态全量。

## 输出与写回

先写范围、时间窗、采集时间及覆盖边界，再给三态和归档统计、周期变化、阻塞、下一步。每个重要判断附事项来源和日期，区分事实、推断与建议。不默认展示内部记录 ID。

默认只输出到会话。明确要求写回时：用 `+detail` 完整读取目标事项的报告记录，检查同范围同周期标题，再用 `ae-cli things entry append --id <target-id> --type note --title "事项周报｜起止日期｜范围" --stdin --command-id <uuid> --format json` 写入最终正文。建议标题为 `事项周报｜起止日期｜范围`（日报同理）。已有同范围同周期报告时提示修订，不静默覆盖或重复追加；用户明确要求追加修订后才写新记录，保留原报告。写回已授权无需再问同一许可。

不自动发送消息、修改状态、指派负责人或建立定时任务。

文件证据：+detail/+digest 自动翻页收集资产关联，availability=missing 或 verification_failed 的文件不算可用交付；即使 available，也只代表引用可用，不代表已读取正文或验收通过。披露未读文件及非事务采集边界。私有会话来源只在当前用户有权时读取，报告引用共享事项事实，不能把私有历史自动公开。
