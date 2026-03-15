---
name: collaborating-with-gemini
description: |
  与 Google Gemini CLI 协同开发。将编码任务委托给 Gemini 进行前端原型、UI设计和代码审查。

  触发场景：
  - 需要前端/UI/样式原型设计
  - 需要 CSS/React/Vue 组件设计
  - 需要代码审查和 Bug 分析
  - 用户明确要求使用 Gemini 协作
  - 复杂前端逻辑的原型设计

  触发词：Gemini、协作、多模型、前端原型、UI设计、CSS、样式、gemini协同

  前置要求：
  - 已安装 Gemini CLI (npm install -g @google/gemini-cli)
  - 已配置 Google API Key

  注意：Gemini 对后端逻辑理解有缺陷，后端任务优先使用 Codex。
---

# 与 Gemini CLI 协同开发

> 通过 Python 桥接脚本调用 Gemini CLI，获取前端原型和 UI 设计建议。

## 快速开始

```bash
# 相对路径（推荐，在项目根目录执行）
python .claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py --cd . --PROMPT "Your task"
```

**输出**: JSON 格式，包含 `success`、`SESSION_ID`、`agent_messages` 和可选的 `error`。

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--PROMPT` | str | ✅ | - | 发送给 Gemini 的任务指令（使用英语） |
| `--cd` | Path | ✅ | - | 工作目录根路径 |
| `--sandbox` | bool | ❌ | `False` | 是否启用沙箱模式 |
| `--SESSION_ID` | str | ❌ | `""` | 会话 ID（继续之前的对话） |
| `--return-all-messages` | bool | ❌ | `False` | 返回完整推理信息 |
| `--model` | str | ❌ | `None` | 指定模型（仅用户明确要求时使用） |

## 使用模式

### 1. 基础调用

```bash
python .claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd . \
  --PROMPT "Design a responsive card component for product display"
```

### 2. 多轮会话

**始终保存 SESSION_ID** 用于后续对话：

```bash
# 第一轮：设计 UI
python .claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" \
  --PROMPT "Design a mobile-first login page with form validation"

# 后续轮次：使用 SESSION_ID 继续
python .claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" \
  --SESSION_ID "uuid-from-previous-response" \
  --PROMPT "Add dark mode support to the login page design"
```

### 3. 获取 Unified Diff 补丁

```bash
python .claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" \
  --PROMPT "Generate a unified diff to improve the CSS layout of Home.vue. OUTPUT: Unified Diff Patch ONLY."
```

### 4. 调试模式（返回完整信息）

```bash
python .claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" \
  --PROMPT "Debug this styling issue: elements overflow on mobile" \
  --return-all-messages
```

## 返回值结构

**成功时：**
```json
{
  "success": true,
  "SESSION_ID": "550e8400-e29b-41d4-a716-446655440000",
  "agent_messages": "模型回复内容..."
}
```

**失败时：**
```json
{
  "success": false,
  "error": "错误信息描述"
}
```

## 协作工作流

### 推荐场景

| 场景 | 说明 |
|------|------|
| **前端/UI/UX** | Gemini 擅长 CSS、样式和视觉设计 |
| **组件设计** | React/Vue 组件的原型设计 |
| **响应式布局** | 移动端适配和布局优化 |
| **样式审查** | CSS 代码质量和最佳实践 |

### 重要约束

1. **上下文限制**: Gemini 上下文 < 32k tokens，避免过长输入
2. **英语交互**: 与 Gemini 交互时使用英语，获得更好效果
3. **中文输出强制**: Gemini 倾向于输出英文，必须在每次 PROMPT 末尾追加以下约束：
   ```
   IMPORTANT LANGUAGE RULES:
   - All SQL COMMENT values MUST be in Chinese (e.g., COMMENT '用户名' NOT COMMENT 'username')
   - All Java/code comments (Javadoc, inline //, block /* */) MUST be in Chinese
   - All field descriptions, table descriptions MUST be in Chinese
   - Variable names and class names remain in English (camelCase/PascalCase)
   ```
4. **Diff 输出**: 在 PROMPT 中明确要求 `OUTPUT: Unified Diff Patch ONLY`
5. **后端逻辑**: Gemini 对后端逻辑理解有缺陷，后端任务优先使用 Codex
6. **重构代码**: 将 Gemini 的输出视为"脏原型"，由 Claude 重构为生产代码（**特别检查注释和 COMMENT 是否为中文，不是则修正**）
7. **后台运行**: 对于长时间任务，使用 `Run in the background`

## 与本项目的集成

### 典型用例：后端代码审查

```bash
# 审查后端 Controller 代码
python .claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd . \
  --PROMPT "Review the RESTful API design in ruoyi-modules/ruoyi-system/src/main/java/org/dromara/system/controller/. Focus on path conventions (/list, /{id}) and proper use of @SaCheckPermission."
```

### 典型用例：Service 层代码审查

```bash
# 审查 Service 实现
python .claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" \
  --PROMPT "Review the XxxServiceImpl.java for buildQueryWrapper implementation, MapstructUtils usage, and adherence to three-layer architecture (no DAO layer). OUTPUT: Review comments."
```

### 典型用例：Entity 设计审查

```bash
# 审查 Entity 设计
python .claude/skills/collaborating-with-gemini/scripts/gemini_bridge.py \
  --cd "/project" \
  --PROMPT "Review the Entity classes in ruoyi-modules/ruoyi-demo/src/main/java/org/dromara/demo/domain/ for proper TenantEntity inheritance, @TableLogic usage, and field naming conventions."
```

## 安装前置

```bash
# 安装 Gemini CLI
npm install -g @google/gemini-cli

# 配置 API Key
gemini auth login
```

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| `gemini: command not found` | 确保已安装并添加到 PATH |
| `SESSION_ID` 获取失败 | 检查网络连接和 API Key |
| 输出被截断 | 使用 `--return-all-messages` 获取完整信息 |
| 上下文过长 | 减少输入内容，分批处理 |
| Windows 路径问题 | 使用正斜杠 `/` 或双反斜杠 `\\` |

## Gemini vs Codex 选择指南

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 前端 UI/CSS | Gemini | 视觉设计能力强 |
| 后端逻辑 | Codex | 算法和逻辑分析强 |
| 组件样式 | Gemini | CSS 和布局专长 |
| API 设计 | Codex | 接口设计和架构 |
| 代码审查 | 两者皆可 | 双模型交叉验证更好 |
