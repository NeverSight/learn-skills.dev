---
name: lsp-first
description: "LSP 優先開發策略工具。Use for: (1) 查詢 LSP 操作指令, (2) 配置新語言 LSP 插件, (3) LSP vs MCP 工具選擇決策, (4) 自建 LSP 插件指南。Use when: 需要搜尋符號/定義/引用、想知道 LSP 和 MCP Serena 各自適合什麼場景、新增語言支援需要配置 LSP 時。"
metadata:
  version: 1.0.0
---

# LSP 優先開發策略

---

## 核心原則

**LSP 能解決的問題必須優先使用 LSP**

| 優勢 | 說明 | 效益 |
|------|------|------|
| **效能** | ~50ms vs ~45 秒 | 900x 加速 |
| **Token 效率** | 結構化資料輸出 | 降低 API 成本 |
| **語意精準** | 語言伺服器分析 | 非文字比對 |

詳細效能資料：`references/performance-comparison.md`

---

## LSP 環境自動檢查

**Session 啟動時自動執行 LSP 環境檢查**

### 檢查項目

1. **基本 LSP**（所有專案必備）
   - marksman (Markdown)
   - yaml-language-server (YAML)

2. **語言特定 LSP**（根據專案類型）
   - Flutter/Dart: Dart SDK 內建 LSP
   - TypeScript/JavaScript: vtsls
   - Python: pyright
   - Go: gopls
   - Rust: rust-analyzer

### 相關檔案

- **檢查腳本**: `.claude/hooks/lsp-environment-check.py`
- **配置檔案**: `.claude/hooks/lsp-check-config.json`
- **觸發方式**: `settings.json` 的 SessionStart 事件直接註冊 `lsp-environment-check.py`

> 原記載的整合位置 `.claude/hooks/startup-check-hook.sh`（步驟 6.6）已不存在——LSP 檢查已改為獨立註冊的 SessionStart hook，不再是啟動 shell 腳本中的一個步驟。2026-08-22 文件複查更正。<!-- broken-link-exempt: 本行為更正說明，其內容正是在陳述該腳本已不存在，路徑不存在是預期的 -->

---

## LSP 9 種操作速查

| 操作 | 用途 | 使用場景 |
|------|------|---------|
| goToDefinition | 跳轉符號定義 | 追蹤函式來源、查看類別定義 |
| findReferences | 查找所有引用 | 重構前影響分析、變更評估 |
| hover | 懸停型別資訊 | 查看 API 文件、確認參數型別 |
| documentSymbol | 列出檔案符號 | 快速理解檔案結構 |
| workspaceSymbol | 跨檔案搜尋 | 找出類別定義、模糊查詢 |
| goToImplementation | 實作查找 | 追蹤抽象類別實作 |
| prepareCallHierarchy | 呼叫層級準備 | 準備函式呼叫分析 |
| incomingCalls | 呼叫來源 | 找出誰呼叫了這個函式 |
| outgoingCalls | 呼叫目標 | 找出這個函式呼叫了誰 |

各操作詳解、範例和 Dart MCP 替代方案：`references/lsp-operations.md`

---

## 工具選擇

搜尋工具的完整選擇決策樹和場景對照表，詳見 `/search-tools-guide`。

以下為 LSP 專屬的選擇要點：

### LSP 獨佔能力（無法由其他工具替代）

| 能力 | LSP 操作 |
|------|---------|
| 呼叫層級分析 | incomingCalls / outgoingCalls |
| 介面實作查找 | goToImplementation |
| 精確型別推導 | hover（語意級別） |

### 工具優先順序

1. **優先**: LSP 工具（語意精準、效能最佳）
2. **次選**: Dart MCP / Serena MCP（LSP 功能等效替代）
3. **備援**: 傳統 Grep/Glob 搜尋

Dart MCP 和 Serena MCP 的工具列表與使用建議：`/search-tools-guide`

---

## 三 MCP 工具路由（指向 search-tools-guide）

> 自 W6-001 引入三 MCP（codebase-memory-mcp / codegraph / serena）後，「Serena 是唯一語意工具」的舊敘事已升級為「三刀流互補」。LSP-first 原則仍為精度錨點，但查詢入口擴展至三 MCP。

### 三 MCP 角色定位

| 工具 | 在 LSP-first 流程中的角色 |
|------|--------------------------|
| **LSP / serena** | **精度錨點**：符號定義、引用追蹤、安全重命名、call hierarchy（型別感知不可替代） |
| **codebase-memory-mcp** | **概念查詢入口**：跨檔案語義搜尋、找「處理 X 概念的所有檔案」（BM25 + 向量混合） |
| **codegraph** | **結構查詢入口**：caller / callee / impact 圖譜追蹤，跨語言符號關係 |

### 路由原則

1. **想找符號** → LSP / serena `find_symbol`
2. **想找概念 / 範圍模糊** → cbm `search_graph`（src/、docs/）或 rg（`.claude/`）
3. **想知道修改影響** → codegraph `impact` + serena `find_referencing_symbols` 雙重驗證
4. **想做安全重構** → serena `rename_symbol` / `replace_symbol_body`

完整三刀流決策樹、九維度對照表、命令速查、cbm 對 `.claude/` 不索引的限制：`/search-tools-guide`（含 `references/codebase-memory-tool.md`）

---

## LSP 伺服器配置

自建插件、官方插件市場、跨平台安裝、故障排除：`references/lsp-setup-guide.md`

---

## 相關資源

- `/search-tools-guide` - 搜尋工具選擇指南（含 Dart MCP、Serena、Grep 完整對照）
- `/startup-check` - Session 啟動檢查
- [boostvolt/claude-code-lsps](https://github.com/boostvolt/claude-code-lsps) - 官方 LSP 插件市場
- [Marksman](https://github.com/artempyanykh/marksman) - Markdown LSP
- [yaml-language-server](https://github.com/redhat-developer/yaml-language-server) - YAML LSP

---

版本紀錄在同目錄的 `CHANGELOG.md`。
