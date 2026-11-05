---
name: ux-writing
description: "UX writing rules — universal best practices + language-specific rules (Chinese, English). Use when: creating UI text, writing button labels, form copy, error messages, empty states. Load after language is confirmed in designPreflight."
---

# UI Copy — Interface Text Conventions

UI copy conventions for Figma designs. Universal best practices plus language-specific rules for Chinese and English. Covers buttons, forms, feedback messages, and text length adaptation.

> Extends UI/UX Fundamentals (loaded separately).
> **Scope**: UI text content and copy conventions only.
> Typography rules (font, size, weight, line-height) are in platform skills (`platform-ios`, `platform-android`).

## Skill Boundaries

- Use this skill for **UI text decisions** (button labels, form copy, error messages, empty states).
- Typography (PingFang SC / Noto Sans SC / SF Pro type scale) is in the platform skill — not here.
- If the task is **bulk text replacement or localization**, switch to [text-replace](../text-replace/SKILL.md).

## Design Direction

Design rules are delivered by `_workflow.designPreflight` (from `get_mode`). For detailed rules by category, call `get_design_guidelines(category)`.

---

## Universal Rules (All Languages)

### Buttons
- Verb-first, specific action — "Save changes" not "OK", "Delete account" not "Delete"
- 1–3 words (English) / 2–4 characters (CJK)
- Primary: affirmative verb. Secondary: neutral/negative. Destructive: state consequence explicitly
- Paired buttons should be semantically symmetric ("Save / Discard", not "Save / Cancel maybe")
- NEVER end button text with a period

### Form Labels & Placeholders
- Labels: noun phrase ("Email address", "Phone number")
- Placeholders: show example format ("name@example.com", "(555) 123-4567") — not instructions
- NEVER mismatch label language and placeholder language

### Feedback Messages
- Errors: state what happened + how to fix ("Password is too short. Use at least 8 characters.")
- Success: concise confirmation ("Saved", "Sent", "Account created")
- Empty states: encouraging tone + action CTA ("No projects yet. Create your first project.")
- NEVER use technical jargon ("HTTP 500" → "Something went wrong. Please try again.")
- NEVER use blaming tone ("You entered the wrong password" → "Incorrect password")

### Text Length
- Use padding not fixed width — text length varies across languages
- NEVER set fixed height on text containers — content length varies by language

---

## Chinese — 中文特定规则

### 按钮文案
- 2–4 个汉字，动词优先（「登录」「注册」「提交」「取消」）
- NEVER 冗长文案：「立即注册新账号」→「注册」；「确认并提交表单」→「提交」
- 主操作：肯定动词（「确认」「保存」「发送」「继续」）
- 次操作：中性/否定词（「取消」「返回」「跳过」「稍后再说」）
- 破坏性操作：明确后果（「删除」「退出登录」，而非泛化的「确认」）
- 配对按钮语义对称：「确认 / 取消」「保存 / 放弃」「同意 / 拒绝」

### 表单文案
- 标签：名词性短语（「邮箱地址」「手机号码」「验证码」「收货地址」）
- 占位提示：「请输入…」格式（「请输入邮箱」「请输入密码」「请选择日期」）
- 下拉菜单：「请选择…」格式（「请选择城市」「请选择支付方式」）
- 必填标记：红色星号 * 在标签前
- 帮助文本：简短说明规则（「密码需包含 8 位以上字符」）

### 反馈文案
- 错误提示：问题 + 解决方案（「密码不正确，请重新输入」「网络异常，请稍后重试」）
- 成功提示：简洁确认（「保存成功」「已发送」「注册完成」）
- 空状态：鼓励性语气 + 行动建议（「还没有订单，去逛逛吧」「暂无消息，有新动态会通知你」）
- 加载状态：「加载中…」「正在获取数据…」
- 权限引导：说明用途（「开启通知以便接收订单更新」）

### 导航与标题
- 导航栏标题：≤6 个汉字（超长时截断加省略号）
- Tab 标签：≤4 个汉字（「首页」「发现」「消息」「我的」）
- 页面标题：简洁明确（「订单详情」「账号设置」「帮助中心」）
- 返回按钮：用图标（chevron），不用文字；如需文字用「返回」

### 中英混排
- 英文单词前后加半角空格（「使用 Google 账号登录」「版本 2.0 更新」）
- 数字前后加半角空格（「共 12 条结果」「还剩 3 天」）
- 品牌名保持原文不翻译（Apple、Google、WeChat、GitHub）
- 单位与数字之间加空格（「100 MB」「30 分钟」）
- 中文标点用全角（，。！？：；），英文标点用半角
- 括号内容跟随内容语言（中文内容用中文括号「（）」，英文内容用半角括号）

### 中文文本长度
- 中文比英文紧凑约 30–50%（「Settings」→「设置」，8 字符→2 字符）
- 导航栏标题容器预留 ≤6 个汉字宽度
- Tab 标签预留 ≤4 个汉字宽度

---

## English — 英文特定规则

### Copy Style
- Sentence case for UI labels ("Sign in" not "Sign In"), except proper nouns and acronyms
- Contractions are OK for conversational tone ("Don't have an account?" not "Do not have an account?")
- Active voice preferred ("We couldn't save your changes" not "Your changes could not be saved")

### Placeholders
- Show example format: "name@example.com", "(555) 123-4567", "Search products..."
- NEVER use instructional placeholders ("Enter your email here")

### English Text Length
- English expands ~30–50% vs Chinese — plan wider containers
- Button min-width: accommodate longest reasonable label
- Truncation: ellipsis for overflow, never mid-word
