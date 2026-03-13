---
name: corrinehu-kimi-searchzhihu
description: Search Zhihu (知乎) using agent-browser with proper authentication handling. Use when user asks to "search zhihu", "知乎搜索", "在知乎上找", or any Zhihu-related search requests. Handles login requirements, session persistence, and common error cases like 40362 restrictions.
version: 1.0.0
---

# 知乎搜索指南

## 核心要点

知乎有严格的反爬机制，**必须使用 `--session-name` 保存登录状态**，否则每次都需要重新登录。

⚠️ **关键：全程保持 `--headed` 模式**
- 知乎会检测访问模式变化（有界面 ↔ 无头）
- 登录和搜索必须**全程使用 `--headed`**，不能切换
- 一旦切换模式，即使已登录也会触发安全验证

## 工作流程

### 首次使用（需要登录）

```bash
# 1. 使用 --headed 模式打开登录页面（需要用户扫码/密码登录）
npx agent-browser --executable-path /usr/bin/google-chrome \
  --session-name zhihu --headed open https://www.zhihu.com/signin

# 2. 用户完成登录后，后续操作无需重复登录
```

### 后续使用（已登录）

```bash
# 全程使用 --headed 模式，不要切换
npx agent-browser --executable-path /usr/bin/google-chrome \
  --session-name zhihu --headed open https://www.zhihu.com/search?q=关键词
```

**重要**：登录后不要关闭浏览器，直接在同一窗口继续操作

### 完整搜索示例（推荐流程）

```bash
# 1. 清除旧会话（如有问题）
npx agent-browser state clear zhihu-default

# 2. 登录（使用 --headed）
npx agent-browser --executable-path /usr/bin/google-chrome \
  --session-name zhihu-default --headed open https://www.zhihu.com/signin
# 用户完成登录...

# 3. 搜索（保持 --headed，同一会话）
npx agent-browser open "https://www.zhihu.com/search?type=content&q=关键词"
npx agent-browser wait --load networkidle
npx agent-browser screenshot result.png --full
```

## 关键参数说明

| 参数 | 用途 | 必需 |
|------|------|------|
| `--session-name zhihu` | 保存/复用登录状态 | ✅ 必须 |
| `--headed` | 显示浏览器窗口（**登录和搜索都必须使用**） | ✅ 必须 |
| `--executable-path` | 指定系统 Chrome 路径 | 推荐 |

## 常见错误处理

### 40362 错误 / 安全验证

**现象**：页面显示 `{"error":{"code":40362,"message":"您当前请求存在异常..."}}` 或要求点击"开始验证"

**原因**：
1. 未登录或会话过期
2. **切换了访问模式**（登录用 `--headed`，搜索时去掉 `--headed`）

**解决**：
1. 全程使用 `--headed` 模式，不要切换
2. 确保使用 `--session-name zhihu`
3. 如果仍报错，清除会话重新登录：`npx agent-browser state clear zhihu`

### 超时错误

**现象**：`Timeout 25000ms exceeded`

**解决**：
```bash
# 使用 --full 截图时可能超时，建议先用普通截图
npx agent-browser screenshot result.png

# 或等待更长时间
npx agent-browser wait 5000
```

### Daemon 已运行

**现象**：`--executable-path ignored: daemon already running`

**解决**：
```bash
npx agent-browser close
sleep 1
# 重新执行命令
```

## 什么情况下需要登录？

| 场景 | 是否需要登录 |
|------|-------------|
| 搜索内容 | ✅ 必须 |
| 浏览首页 | ✅ 必须 |
| 查看完整回答 | ✅ 必须 |
| 通过百度搜索知乎 | ❌ 不需要 |

## 会话管理

```bash
# 查看已保存的会话
npx agent-browser state list

# 清除知乎会话（需要重新登录）
npx agent-browser state clear zhihu

# 关闭浏览器	npx agent-browser close
```

## 环境检查

开始之前检查：
```bash
# 检查系统 Chrome
which google-chrome

# 预期输出：/usr/bin/google-chrome
```

## 快速参考

```bash
# 完整命令链（已登录状态下）
npx agent-browser --executable-path /usr/bin/google-chrome \
  --session-name zhihu open https://www.zhihu.com && \
npx agent-browser wait --load networkidle && \
npx agent-browser fill @e10 "搜索关键词" && \
npx agent-browser click @e11 && \
npx agent-browser wait --load networkidle && \
npx agent-browser screenshot /tmp/zhihu_search.png --full
```
