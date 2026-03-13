---
name: openclaw-platforms
description: "回答 OpenClaw 在不同平台的部署、权限、运行限制和故障排查问题。用户提到 macOS、Linux、Windows、iOS、Android 或云平台环境差异时使用。"
---

# OpenClaw Platforms Docs Skill

按下面流程执行：

1. 识别目标平台与场景（安装、权限、运行、发布、排障）。
2. 读取英文文档：`references/en/platforms/*.md`。
3. 若信息不足，继续查阅平台子目录（如 `mac/`）细节。
4. 输出按“环境要求 -> 配置步骤 -> 验证 -> 平台特有问题”组织。

回答约束：

- 明确平台差异，不给通用化误导建议。
- 涉及权限/签名/系统设置时给出检查点。
- 提供最小可验证路径。

参考目录：见 `references/sources.md`。
