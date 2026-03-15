---
name: ui-validator
description: 负责所有 UI 变更后的浏览器自动化验证，确保实际渲染效果符合预期。
version: 1.0.0
author: GitHub Copilot
appliesTo: "components/**/*.vue, pages/**/*.vue, assets/styles/**/*.scss"
---

# UI Validator Skill (UI 验证专家技能)

## 概述 (Overview)

本技能专注于所有涉及 UI（用户界面）改动的闭环验证。它通过驱动真实的浏览器环境，确保代码层面的修改在不同主题模式、屏幕尺寸及交互状态下均能正确呈现。

## 核心职责 (Core Responsibilities)

### 1. 开发环境自检 (Dev Server Pre-check)
在进行任何页面访问前，必须确保开发服务器 (`localhost:3000`) 已处于活跃状态。
- **端口检查**：执行 `Test-NetConnection -ComputerName localhost -Port 3000` (Windows) 或 `lsof -i:3000` (POSIX) 检查端口。
- **自动启动**：若端口未启动，则异步执行 `pnpm dev`（设置 `isBackground: true`）并等待约 5-10 秒直至就绪。
- **避免重复**：若端口已占用，严禁再次启动服务器。

### 2. 浏览器自动化验证 (Browser Automation)
使用浏览器工具（如 Chrome MCP）进行多维检查。
- **页面访问**：导航至受影响组件所在的路由路径。
- **暗色模式切换**：通过执行脚本修改 `html` 元素的 `class`（添加/删除 `dark`）来切换暗色模式。
- **状态捕获**：
    - **视觉捕捉**：获取页面截图 (`browser_take_screenshot`)。
    - **逻辑分析**：获取 a11y 树快照 (`take_snapshot`) 或执行 JavaScript 获取计算后的样式 (`evaluate_script`，检查 `getComputedStyle`)。
- **交互验证**：模拟用户悬停、点击等操作，验证交互反馈。

### 3. 改动对比与修复 (Comparison & Remediation)
- **视觉对比**：确认改动是否修复了原本存在的问题，或者新功能是否美观、符合 BEM 规范及样式变量。
- **回归修复**：若在浏览器中观察到样式冲突、覆盖不生效或对比度不足，必须回退至代码编辑阶段进行针对性修复。

## 指令 (Instructions)

1. **先启动，后访问**：永远先校验 3000 端口，不要假设服务器永远运行着。
2. **多模式检查**：对于所有 UI 修改，必须分别在 `light` 和 `dark` 模式下检查。
3. **关键数据导向**：比起模糊的“看起来不错”，优先提供 `getComputedStyle` 的具体颜色值、尺寸信息或截图作为证据。
4. **证据闭环**：在任务总结中，应包含对 UI 实际表现的简短描述，必要时引用截图路径。

## 使用示例 (Usage Example)

输入: "修改了文章卡片的圆角，并在暗色模式下加深背景。"
动作:
1. 运行 `Test-NetConnection` 确认服务器。
2. 调用 `browser_navigate` 访问演示页面。
3. 执行脚本添加 `.dark` 类。
4. 通过 `evaluate_script` 检查卡片的 `border-radius` 和 `background-color`。
5. 截图并反馈给用户。









