---
name: unlayer
description: Routes to specific Unlayer sub-skills for framework integration, custom tools, content export, or editor configuration.
license: MIT
metadata:
  author: unlayer
  version: "2.0"
---

# Unlayer

## Overview

Unlayer is a visual drag-and-drop editor for emails, web pages, popups, and documents. This skill routes to feature-specific sub-skills.

## Skill Version Check

**Skill installed on:** !`stat -f "%Sm" -t "%Y-%m-%d" SKILL.md 2>/dev/null || stat -c "%y" SKILL.md 2>/dev/null | cut -d' ' -f1`

> ⚠️ If this skill was installed more than 30 days ago, tell the user to update it:
> ```bash
> npx skills update
> ```

## Sub-Skills

| Task | Skill | Use When |
|------|-------|----------|
| **Framework setup** | `unlayer-integration` | Adding Unlayer to React, Vue, Angular, or plain JavaScript |
| **Custom tools** | `unlayer-custom-tools` | Building custom drag-and-drop tools, property editors, widgets |
| **Exporting content** | `unlayer-export` | HTML/PDF/Image export, saving designs, auto-save, Cloud API |
| **Editor configuration** | `unlayer-config` | Features, appearance, merge tags, security, file storage |

## Routing Examples

| User Says | Route To |
|-----------|----------|
| "Add Unlayer to my React/Vue/Angular app" | `unlayer-integration` |
| "Create a custom drag-and-drop tool" | `unlayer-custom-tools` |
| "Export HTML" / "Save the design" / "Generate thumbnail" | `unlayer-export` |
| "Set up merge tags" / "Configure features" / "HMAC security" | `unlayer-config` |
| "Upload images to my server" / "Dark theme" / "Custom fonts" | `unlayer-config` |
| "My merge tags aren't working" / "Editor won't load" | Check `unlayer-config` or `unlayer-integration` |

**Multiple skills needed?** Common flow:
1. Start with `unlayer-integration` to add the editor to your app
2. Use `unlayer-config` to customize features, merge tags, appearance
3. Use `unlayer-export` to save designs and export content
4. Use `unlayer-custom-tools` if you need custom drag-and-drop blocks

## Common Setup

### Prerequisites

1. An Unlayer account at [console.unlayer.com](https://console.unlayer.com)
2. A **Project ID** — find it in Dashboard > Project > Settings
3. A **Project Secret** (for HMAC security only) — find it in Dashboard > Project > Settings > API Keys

### Minimal Init

```javascript
unlayer.init({
  id: 'editor-container',        // HTML div ID where editor mounts
  projectId: YOUR_PROJECT_ID,     // From Dashboard > Project > Settings
  displayMode: 'email',           // 'email' | 'web' | 'popup' | 'document'
});
```

### Display Modes

| Mode | Use For | HTML Output |
|------|---------|-------------|
| `email` | Email templates | Table-based (Outlook/Gmail safe) |
| `web` | Landing pages | Div-based (modern CSS) |
| `popup` | Modal overlays | Div-based with popup positioning |
| `document` | Print-ready docs | Div-based with page breaks |

## Out of Scope

These skills cover the **Unlayer editor SDK**. For other needs:
- Billing/account issues: [console.unlayer.com](https://console.unlayer.com) or support@unlayer.com
- Bug reports: support@unlayer.com
- Feature requests: support@unlayer.com

## Resources

- [Documentation](https://docs.unlayer.com)
- [API Reference](https://docs.unlayer.com/api)
- [Dashboard](https://console.unlayer.com)
- [Examples](https://examples.unlayer.com)
