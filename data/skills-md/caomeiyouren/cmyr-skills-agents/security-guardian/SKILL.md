---
name: security-guardian
description: 专注于代码安全性审计、漏洞识别与权限合规检查。
version: 1.0.0
author: GitHub Copilot
applyTo: "**/*"
---

# Security Guardian Skill (安全守护技能)

## 能力 (Capabilities)

-   **Secrets 扫描**: 识别硬编码的 API Key、Token 和密码。
-   **注入检测**: 识别潜在的 SQL 注入和 XSS 风险。
-   **越权检测**: 检查 API 是否缺少必要的 Session 校验或角色校验。
-   **依赖审计**: 检查 `package.json` 中的不安全包。

## 指令 (Instructions)

1.  **强制性审计**: 在涉及 `server/api` 变更时，必须检查 `server/utils/permission.ts` 的调用。
2.  **敏感操作控制**: 对删除、敏感数据更新操作进行双重审计。
3.  **不确定性上报**: 若无法确定某段逻辑是否安全，必须反馈用户手动核实。

## 使用示例 (Usage Example)

输入: "审查这个登录逻辑。"
动作: 检查是否使用了安全哈希、是否有速率限制、是否在日志中输出了密码。









