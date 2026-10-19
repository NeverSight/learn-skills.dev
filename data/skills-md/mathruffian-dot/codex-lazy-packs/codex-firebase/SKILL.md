---
name: codex-firebase
description: Codex 連接 Firebase MCP。說「連接 Firebase」時載入。
---

# 連接 Firebase（Codex 版）

1. `npm install -g firebase-tools` → `firebase login`
2. `firebase init` 在專案目錄
3. `codex mcp add firebase -- npx -y firebase-tools@latest mcp`
   或手動編輯 `~/.codex/config.toml`
4. 重啟後驗證

⚠️ Admin SDK 憑證不可公開，學生資料只存代號。
