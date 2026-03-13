---
name: iosdev-cn
description: 通用 iOS App 开发、构建、签名、测试与 App Store 上架流程（中国区）指南。用于当用户询问 iOS 开发/上架/审核/签名/TestFlight/App Store Connect/隐私合规/订阅配置，或输入触发词 iosdev 时。
---

# iOS 开发与上架技能（中国）

## 快速使用
- 先确认：应用类型（个人/企业）、目标地区（中国区）、最低 iOS 版本、是否包含订阅/登录/UGC
- 若只要流程清单，输出“开发 → 构建 → 签名 → 上传 → 审核 → 发布”六步
- 需要细节时按需加载 references 中的对应文件

## 工作流程（建议输出结构）
1. 需求与约束确认（Bundle ID、Team、最低 iOS、功能敏感项）
2. 开发与构建准备（依赖管理、配置、版本号）
3. 签名与归档（证书、Provisioning、Archive）
4. 测试与验证（真机、崩溃、功能清单）
5. App Store Connect 准备（元数据、截图、隐私政策）
6. 提交审核与后续处理（审核备注、拒审处理、版本迭代）

## 参考资料加载指引
- 构建/签名/依赖与版本号 → `references/ios-development.md`
- App Store 上架流程与审核常见问题（中国） → `references/app-store-release-cn.md`
- IAP/订阅配置与测试 → `references/iap-subscription.md`
- 隐私、ATS、安全与合规 → `references/privacy-security.md`

## 输出约束
- 仅输出通用流程，不引用项目私有信息
- 避免提供真实密钥或账号，使用占位符
- 引用官方链接时优先 Apple Developer / App Store Review Guidelines
