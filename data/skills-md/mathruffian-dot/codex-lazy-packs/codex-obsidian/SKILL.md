---
name: codex-obsidian
description: Codex 連接 Obsidian。說「連接 Obsidian」時載入。
---

# 連接 Obsidian（Codex 版）

## 方式一：資料夾授權（推薦）
在 Codex 設定中授權 vault 資料夾讀寫，不需 MCP。

## 方式二：MCPVault
1. 找 vault 路徑（搜尋 `.obsidian` 子目錄）
2. `npm install -g @bitbonsai/mcpvault`
3. `codex mcp add obsidian -- npx @bitbonsai/mcpvault <VAULT_PATH>`
   或手動編輯 `~/.codex/config.toml`
4. 重啟後驗證

## 進階
全文檢索：安裝 Obsidian Local REST API plugin + `cli-hub install obsidian`

回報：授權方式、vault 路徑、讀取/寫入測試結果。
