---
name: desktop-automation
description: 桌面自动化 — 通过 AppleScript 控制 macOS 应用（Atlas、Chrome、Finder 等）。
triggers:
  intent_patterns:
    - "applescript|桌面自动化|desktop|macos|打开应用|切换窗口"
  context_signals:
    keywords: ["applescript", "desktop", "macos", "自动化", "窗口"]
  confidence_threshold: 0.7
priority: 6
requires_tools: [bash]
max_tokens: 200
cooldown: 60
---

# desktop-automation

macOS 桌面自动化：运行 AppleScript 控制应用程序。

## 调用

```bash
python3 skills/desktop-automation/run.py run --script 'tell application "Finder" to activate'
python3 skills/desktop-automation/run.py open_app --app Safari
```
