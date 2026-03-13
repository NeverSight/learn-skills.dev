---
name: openclaw-install
description: "回答 OpenClaw 的安装、升级、迁移、卸载与环境准备问题。用户提到 docker、nix、node、云平台部署、版本升级或安装故障时使用。"
---

# OpenClaw Install Docs Skill

按下面流程执行：

1. 先确认用户环境（本机/服务器、OS、是否容器化、是否已有旧版本）。
2. 读取英文文档：`references/en/install/*.md`。
3. 若信息不足，继续查阅同目录中与当前环境匹配的安装/升级条目。
4. 输出按“前置检查 -> 安装/升级 -> 验证 -> 回滚/卸载”组织。

回答约束：

- 给出与用户环境匹配的最短落地路径。
- 给出验证命令和成功判据。
- 升级与迁移场景必须提示备份与回滚点。

参考目录：见 `references/sources.md`。
