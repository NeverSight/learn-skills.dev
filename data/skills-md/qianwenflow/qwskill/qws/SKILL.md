---
name: qws
description: QWS AI 采访统一入口。Use when the user says /qws, qws, 调取QWS, 想接受AI采访，或希望通过连续提问把经历、想法或判断说清。
---

# QWS

这是公开包的统一入口。当前公开包包含 `qws-interview`，用于通过连续、非诱导式采访把用户尚未说清的经历、想法和判断整理成显性知识。

执行时：

1. 读取同一安装中的 `qws-interview/SKILL.md` 全文及它要求的必要资源。
2. 按 `qws-interview` 的入口、流程、权限和交付规则继续；本入口不复制、改写或缩减采访规则。
3. 如果 `qws-interview` 未安装或不可读，明确报告缺少依赖，并请用户重新安装完整公开包；不要凭记忆模拟。

当前公开包没有发布其他 QWSkill。对非采访任务，不得声称可以调用未安装的内部 Skill。

