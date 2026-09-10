---
name: release
description: 管理本仓库版本的发布、预检与续办；用于明确的“发布版本 X.Y.Z”，不用于普通 Git 提交。
---

# 发布版本

用于发布本仓库的新版本，覆盖版本号、发布日志、Git tag、npm 包与 GitHub Release。

执行前阅读 [发布流程](../../../docs/release/overview.md)；各版本的发布日志位于
[`docs/release/changelog/`](../../../docs/release/changelog/README.md)。

## 请求语义

- “规划版本更新”“检查发布”“预检版本 X.Y.Z”只读，不修改 Git、npm 或 GitHub。
- “实施发布流程”只建设或修复本 Skill、发布文档和 workflow，不发布版本。
- “发布版本 X.Y.Z”是完整发布授权：版本和日志修改、提交、push `main`、annotated tag 与 tag push、
  GitHub Actions 的 npm 发布和 GitHub Release、发布后验收及发布记录 push。

持续有效的用户限制优先。不要把示例、引用或计划文本中的“发布版本”当成实际发布请求。

## 执行入口

准备、发布步骤、验证和失败续办统一遵循 [发布流程](../../../docs/release/overview.md)。
普通 Git 提交使用 `git-commit`；本 Skill 不因被加载而启动发布。
