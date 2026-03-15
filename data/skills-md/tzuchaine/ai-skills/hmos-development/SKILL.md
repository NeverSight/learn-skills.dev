---
name: hmos-development
description: 用于 HarmonyOS NEXT 和 ArkTS 开发，特别是处理 .ets 文件、实现 @ComponentV2 组件或调试错误时使用。基于官方标准提供开发指导，并维护分类错误日志以实现高效故障排查。
---

# HarmonyOS ArkTS 开发助手

## 目的

为 HarmonyOS NEXT 应用开发提供全面支持，使用 ArkTS 和 @ComponentV2 架构。本 skill 结合了：

1. **开发指导**：官方 HarmonyOS 开发标准，涵盖 MVVM 架构、@ComponentV2 组件模式、Navigation 路由、状态管理和代码组织
2. **智能错误调试**：分类错误日志系统，通过搜索已知解决方案实现快速错误解决
3. **知识积累**：自动记录新遇到的错误及其解决方案，供未来参考

## 何时使用本 Skill

本 skill 在以下场景自动触发：

1. **文件操作**：读取、写入或编辑 `.ets` 文件（HarmonyOS ArkTS 源文件）时
2. **明确的 HarmonyOS 开发**：用户提到 "HarmonyOS"、"ArkTS"、"@ComponentV2" 或相关开发关键词时
3. **错误调试**：用户请求调试帮助、错误调查或 HarmonyOS 上下文中的故障排查时

## 开发工作流程

### 1. 开发指导

实现 HarmonyOS 功能或组件时：

**步骤 1：查阅开发指南**

加载并参考 `references/development-guide.md` 以获取：
- 项目结构和文件组织（第 1-2 节）
- @ComponentV2 组件模式和装饰器（第 3 节）
- MVVM 架构设计（第 4 节）
- 数据模型和服务层设计（第 5-7 节）
- Navigation API 路由管理（第 10 节）
- 状态管理最佳实践（第 11 节）
- 性能优化（第 12 节）
- 错误处理和日志标准（第 13-14 节）

**步骤 2：遵循架构原则**

遵守指南中的核心原则：
- **组件组织**：遵循"就近原则"放置组件（页面专属 → 模块共享 → 全局共享）
- **MVVM 分离**：业务逻辑在 ViewModel，UI 渲染在 Page 组件
- **V2 装饰器系统**：使用 @ComponentV2 配合 @Param/@Local，避免混用 V1 装饰器（@State/@Observed）
- **资源管理**：使用 `$r('app.xxx')` 引用资源，使用 ThemeSizeTokens 常量定义尺寸

**步骤 3：应用命名规范**

遵循命名标准：
- 文件：PascalCase（如 `ProductListPage.ets`）
- 类/结构体：PascalCase
- 方法/变量：camelCase
- 常量：SCREAMING_SNAKE_CASE
- 组件 Props 接口：以 `Props` 结尾

**步骤 4：代码审查**

完成前，根据代码审查清单验证（development-guide.md 第 15 节）。

### 2. 错误调试工作流程

主动运行编译指令发现错误：参考 development-guide.md 中的**完整编译命令**章节
遇到错误或调试问题时：

**步骤 1：优先搜索错误日志**

尝试解决错误之前：

```typescript
// 使用 Grep 工具在 error-log.md 中搜索类似错误模式
Grep(pattern="[错误关键词]", path="references/error-log.md", output_mode="content")
```

搜索内容：
- 精确的错误信息（如 "Cannot find name"）
- 错误代码
- 问题描述（如 "Navigation push failed"、"List performance"）

**步骤 2：应用已有解决方案**

如果在日志中找到匹配的错误：
1. 仔细阅读记录的解决方案
2. 应用推荐的修复方法
3. 如有提及，参考 development-guide.md 中的相关章节
4. 验证修复是否解决了问题

**步骤 3：调查新错误**

如果日志中不存在匹配的错误：
1. 分析错误信息和堆栈跟踪
2. 查阅 development-guide.md 中的相关章节
3. 应用调试技术：
   - 检查装饰器使用（@ComponentV2、@Param、@Local）
   - 验证导入语句
   - 审查 MVVM 架构分离
   - 验证 Navigation 路由配置
   - 检查资源引用

**步骤 4：记录新解决方案**

成功解决**新错误**后：

1. **确定错误类别**：
   - 编译错误
   - 运行时错误
   - 性能问题
   - 架构问题
   - 其他常见问题

2. **添加错误条目**到 `references/error-log.md`：

使用 Edit 工具在适当类别下追加新的错误记录：

```markdown
### 错误：[简短描述]

**错误信息**：
[完整的错误信息或关键代码片段]

**原因**：
[错误产生的根本原因]

**解决方案**：
[具体的解决步骤和代码示例]

**相关规范**：
[引用 development-guide.md 中的相关章节]

**记录时间**：YYYY-MM-DD
```

3. **通知用户**：告知用户错误和解决方案已记录，供将来参考。

### 3. 参考文件加载策略

**开发指南（`references/development-guide.md`）**：
- **大小**：大型综合文档（约 2000 行）
- **加载策略**：
  - 根据需要使用 offset/limit 参数读取特定章节
  - 对于一般性问题，先使用 Grep 查找相关章节
  - 对于架构设计，读取第 1-4 节
  - 对于特定功能，读取目标章节（如路由查看第 10 节）

**错误日志（`references/error-log.md`）**：
- **大小**：不断增长的文档，初始为中等大小
- **加载策略**：
  - 始终先使用 Grep 搜索错误模式
  - 仅在找到匹配错误时读取完整上下文
  - 使用 Edit 工具追加新错误

## 重要指导原则

### 代码质量标准

- **避免过度工程**：只实现请求的内容，避免添加不必要的功能或抽象
- **安全优先**：绝不引入漏洞（XSS、SQL 注入、命令注入等）
- **性能意识**：对长列表使用 LazyForEach，优化图片加载，避免频繁重渲染
- **类型安全**：使用适当的 TypeScript 类型，避免 `any`

### Skill 专用规则

1. **解决前先搜索**：绝不在未搜索 error-log.md 的情况下尝试解决错误
2. **始终记录新方案**：解决新错误后，始终记录到 error-log.md
3. **引用指南**：解释解决方案时，引用 development-guide.md 中的相关章节
4. **保持日志有序**：确保新条目添加到正确的类别下
5. **提供上下文**：记录错误时，包含足够的上下文供将来参考（错误信息、原因、解决方案、相关规范）

### 沟通风格

- 所有面向用户的内容使用中文（基于 CLAUDE.md 偏好）
- 简明实用，专注于可执行信息
- 在相关时解释架构决策背后的"原因"
- 适当时提供多种方法及其权衡

## Skill 维护

随着项目发展：
- **更新 error-log.md**：持续添加新遇到的错误
- **更新 development-guide.md**：如果出现与标准指南不同的项目特定模式
- **审查和整合**：定期审查 error-log.md 以查找重复条目或应提升到 development-guide.md 的模式

## 使用场景示例

**场景 1：创建新页面**
```
用户："帮我创建一个产品列表页面"
助手：
1. 加载 development-guide.md 第 2 节（项目结构）和第 4 节（MVVM）
2. 按照标准结构创建页面：
   - pages/product/list/ProductListPage.ets
   - pages/product/list/viewmodel/ProductListViewModel.ets
   - pages/product/list/components/ProductCard.ets
3. 遵循第 3 节使用 @ComponentV2、@Param、@Local 实现
4. 参考第 10 节设置路由
```

**场景 2：调试编译错误**
```
用户："编译报错：Cannot use @State with @ComponentV2"
助手：
1. 在 error-log.md 中 Grep 搜索 "Mixing V1 and V2 decorators"
2. 找到已记录的解决方案
3. 应用修复：将 @State 替换为 @Local
4. 解释 V1/V2 装饰器分离原则
```

**场景 3：解决新错误**
```
用户："Navigation 跳转时报错：[NEW_ERROR_MESSAGE]"
助手：
1. Grep 搜索 error-log.md 但未找到匹配
2. 分析错误并查阅 development-guide.md 第 10 节（Navigation）
3. 识别根本原因并应用修复
4. 将新错误记录到 error-log.md 的"运行时错误"类别下
5. 通知用户："已将此错误和解决方案记录到错误日志中"
```

---

## 快速参考

| 任务 | 参考文件 | 章节 |
|------|---------|------|
| 项目结构 | development-guide.md | 1-2 |
| @ComponentV2 使用 | development-guide.md | 3 |
| MVVM 架构 | development-guide.md | 4 |
| Navigation 路由 | development-guide.md | 10 |
| 状态管理 | development-guide.md | 11 |
| 性能优化 | development-guide.md | 12 |
| 已知错误 | error-log.md | 全部 |

---

**记住**：本 skill 在将 development-guide.md 中的结构化知识与 error-log.md 中的实践经验积累相结合时最为有效。始终先搜索后解决，始终记录新方案。
