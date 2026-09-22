---
name: ldm-session-handoff
description: >
  导出会话原文、生成任务路由器和重启提示语，帮助长任务跨会话恢复。用户说“会话存档”“保存聊天记录”“导出对话全记录”“生成路由器”“准备退出重启”或“给我重启提示语”时使用；普通文件归档不使用。
  Export raw conversation transcripts, generate task routers and restart prompts to help long-running tasks resume across sessions. Triggered when the user says "session archive," "save chat log," "export full transcript," "generate router," "prepare to exit and restart," or "give me a restart prompt"; not used for ordinary file archiving.
---

# 会话交接

目标是让下一次会话能核对原始记录，并快速恢复决定、产出、进度和待办。

## 按用户请求选择产物

- 完整交接：对话全记录、路由器、重启提示语。
- 用户明确说“只导出原文”时：只生成对话全记录。
- 用户明确说“只更新路由器”时：读取现有记录和产出后更新路由器。
- 用户明确说“只要重启提示语”“不用导出”或“不要创建文件”时：只给提示语；若缺少可靠上下文，明确哪些信息待补。

用户说“加载交接 Skill”“使用交接 Skill”“会话存档”“保存对话”或“准备退出重启”时，默认做完整交接；即使同一句还提到“给我重启提示语”，也不能因此跳过对话全记录和路由器。只有用户用“只”“仅”“不用导出”“不要创建文件”等明确措辞缩小范围时，才改为单项产物。

## 完整交接流程

1. 确认当前会话、主题和保存目录。优先使用用户已配置的存档根目录；否则使用当前工作区中的明确目录。
2. 通过平台原生导出能力或本 Skill 的脚本读取 user/assistant 原文。不要凭记忆生成“全记录”。
3. 生成路由器，只保留恢复任务需要的决定、产出、进度、待办和新教训。
4. 核对文件存在、消息数量级合理、来源标记准确。
5. 报告所有产物的绝对路径，最后直接给出可复制的重启提示语。

格式见 [references/formats.md](references/formats.md)。只有需要选择或排查导出后端时才读 [references/export-backends.md](references/export-backends.md)。

## 原文真实性

- “对话全记录”必须来自可核查的会话数据源。
- 默认保留 user/assistant 可见文本，过滤工具调用、工具输出、推理记录、环境注入和空占位。
- 不把摘要、路由器或模型回忆标成原文。
- 导出不完整时写明已获得的范围和“待补存”，不要声称数据必然永久存在。
- 单条截断会损失原文；只有用户要求控制体积或平台限制无法避免时才截断，并在文件头记录阈值和数量。

## 路由器

路由器是恢复上下文的主力，重启提示语只是入口；原文负责回查，路由器负责恢复。它是导航，不复述整段对话。至少写清：

- 关键决策及其理由。
- 存档点：按时间顺序列出做完并确认过的关卡及其凭据，让新会话一眼看到做到哪了。
- 已完成产物的绝对路径与状态。
- 资源版本：只写恢复时用错版本就会做错的依赖及其版本（skill、素材库、模板、工具）；还没定的状态、还没做的事，写进待办或下一步。
- 正在进行的工作、下一步及其前置条件（动手之前必须先具备或确认什么）。
- 尚未解决的问题和明确待办。
- 只有本次新出现且可复用的经验教训。

外部链接只记录需要继续使用的最终入口。敏感凭证不写入路由器。

## 导出工具

- Hermes SQLite：`scripts/export_transcript.py`
- Claude Code / Codex JSONL：`scripts/export_jsonl_transcript.py`

脚本只负责导出原文，不负责生成路由器。先用 `--list` 找到会话，再指定会话和输出路径；本机存在多个后端时不要猜测。

**当前活跃会话**不会出现在 `--list` 中。导出步骤：`session_search` 搜当前对话关键词 → 从结果提取 `session_id` → `export_transcript.py --session <id> --output <绝对路径>`。此路径对活跃会话和已结束会话同样有效。

## 完成检查

- 交付内容与用户请求的产物范围一致。
- 全记录文件头写明数据源、会话标识、时间范围、消息数和导出方式。
- 完整交接时，两个文件均已报告绝对路径，重启提示语已直接发给用户。
- 失败和截断情况如实标注，没有用摘要冒充原文。

## Pitfalls

### 1. 永远不要声称"导不出来"（2026-09-04/09-08 实战教训）

用户明确要求导出时，不得以"当前活跃session"为由放弃。导出路径：`session_search` 提取 session_id → `export_transcript.py --session <id>`。这招对活跃会话和已结束会话都有效。

此错误已导致用户暴怒两次。如果 `--list` 找不到，换 `session_search`；如果 `session_search` 也找不到，如实报告，但先试完两条路再说。

### 2. 重启提示语和路由器中必须使用绝对路径（2026-09-04/09-08 实战教训）

- ❌ `~/Documents/Hermes_Workspace/...`（`~` 不是绝对路径，用户会暴怒）
- ✅ `/Users/likai/Documents/Hermes_Workspace/...`

所有文件路径一律用 `/Users/likai/` 开头。包括重启提示语、路由器产出清单、用户给的指引。用户已多次纠正此问题。

### 3. 导出全记录不要按 `active = 1` 过滤（2026-09-11 实战教训）

上下文压缩会把已压缩的老消息标成 `active = 0`，但那些**仍是被压缩前的真实原文**，全记录必须保留。按 `active = 1` 过滤会把长会话导成十分之一（实测某会话只导出 34 条，实际原文 162 条）——丢掉的正好是最早、最需要回查的那部分。

只排除 `_compressed_summary = 1` 的行：那是压缩生成给模型看的 AI 摘要，不是原文。`export_transcript.py` 已修（commit 5844ac6）；确需只看当前活跃上下文时用 `--active-only`。
上下文重建还会把历史整块重复入库（同一消息以 [Note: ...] 前缀变体反复重插），脚本已内置去重：块重放（连续3条以上同序同文）整块剔除、助手重复长文只留首次，用户消息不做全局去重（连发「1」是真实对话）。文件头会写明两类剔除条数。

导出后必须核对条数：文件头写的消息数应与「用户条数 + 助手条数」一致，并与库里的实际条数量级相符。

### 4. 本 skill 是软链，`skill_manage` 改不动（2026-09-11 实战教训）

`skill_manage` 会报 `not found in active profile`，因为真源在 ldm-skill 仓库里。改这个 skill 直接用 `patch` 工具改真源路径：

`/Users/likai/Documents/Hermes_Workspace/ldm-skill/skills/ldm-session-handoff/SKILL.md`

改完从软链路径（`/Users/likai/.hermes/skills/ldm-session-handoff/SKILL.md`）读回验证。
