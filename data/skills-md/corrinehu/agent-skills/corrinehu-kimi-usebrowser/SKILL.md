---
name: corrinehu-kimi-usebrowser
description: Browser automation troubleshooting and best practices for Kimi CLI using agent-browser. Use when encountering issues with browser automation, timeouts, Playwright browser downloads, or when needing to use system Chrome instead of downloading Chromium. Covers common pitfalls like first-time installation timeouts, proxy issues, and executable path configuration.
version: 1.0.0
---

# Kimi 浏览器自动化使用指南

## 概述

本 skill 总结了在 Kimi CLI 环境中使用 `agent-browser` 进行浏览器自动化的经验，特别是针对常见问题和解决方案。

## 核心工作流程

### 基础使用模式

```bash
# 1. 打开网页
npx agent-browser open <url>

# 2. 等待页面加载
npx agent-browser wait --load networkidle

# 3. 获取页面快照（带交互元素引用）
npx agent-browser snapshot -i

# 4. 交互操作（使用 @e1, @e2 等引用）
npx agent-browser fill @e1 "text"
npx agent-browser click @e2

# 5. 截图
npx agent-browser screenshot output.png --full
```

### 命令链式执行

使用 `&&` 连接多个命令提高效率：

```bash
npx agent-browser open https://example.com && \
npx agent-browser wait --load networkidle && \
npx agent-browser snapshot -i
```

## 常见问题与解决方案

### 问题 1：首次安装超时

**现象**：
```bash
npx agent-browser open https://example.com
# Error: Command killed by timeout
```

**原因**：`npx` 首次运行时需要下载安装 `agent-browser` 包及其 184+ 个依赖。

**解决**：
- 手动安装到本地目录：`npm install agent-browser`
- 或使用更长的超时时间
- 安装后再次使用会更快

### 问题 2：Playwright 浏览器下载失败

**现象**：
```bash
npx playwright install chromium
# Error: Proxy connection ended before receiving CONNECT response
```

**原因**：`agent-browser` 基于 Playwright，默认需要下载 Chromium 浏览器，但可能遇到网络/代理问题。

**解决**：使用系统已安装的 Chrome

```bash
# 检查系统 Chrome
which google-chrome  # 或 chromium, chromium-browser

# 使用系统 Chrome 运行
npx agent-browser --executable-path /usr/bin/google-chrome open <url>
```

**重要**：如果 daemon 已在运行，需要先关闭：

```bash
npx agent-browser close
sleep 1
npx agent-browser --executable-path /usr/bin/google-chrome open <url>
```

### 问题 3：会话冲突

**现象**：`--executable-path ignored: daemon already running`

**解决**：关闭现有会话后重新启动：

```bash
npx agent-browser close
npx agent-browser --executable-path /usr/bin/google-chrome open <url>
```

## 实用脚本

使用 `scripts/check-browser-env.sh` 快速检查环境：

```bash
# 检查系统浏览器并输出建议命令
./scripts/check-browser-env.sh
```

输出示例：
```
找到系统浏览器: /usr/bin/google-chrome
建议命令:
  npx agent-browser --executable-path /usr/bin/google-chrome open <url>
```

## 完整示例：搜索并截图

```bash
# 安装依赖（首次）
cd /tmp && npm install agent-browser

# 使用系统 Chrome 执行
npx agent-browser --executable-path /usr/bin/google-chrome open https://www.baidu.com
npx agent-browser wait --load networkidle
npx agent-browser snapshot -i

# 填写搜索框并搜索（假设 @e13 是搜索框，@e14 是按钮）
npx agent-browser fill @e13 "OpenAI"
npx agent-browser click @e14
npx agent-browser wait --load networkidle

# 截图
npx agent-browser screenshot /tmp/search_result.png --full
```

## 快速参考

| 命令 | 用途 |
|------|------|
| `open <url>` | 打开网页 |
| `close` | 关闭浏览器 |
| `snapshot -i` | 获取交互元素快照 |
| `fill @eN "text"` | 填写输入框 |
| `click @eN` | 点击元素 |
| `wait --load networkidle` | 等待网络空闲 |
| `screenshot <path> --full` | 全页截图 |

## 环境检查清单

开始浏览器自动化前，检查：

1. [ ] `agent-browser` 是否已安装（`npm list agent-browser`）
2. [ ] 系统 Chrome/Chromium 路径（`which google-chrome`）
3. [ ] 是否有残留的 daemon（`npx agent-browser close` 清理）
4. [ ] 网络连接是否正常
