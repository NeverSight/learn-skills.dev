---
name: worktree
description: "Use this skill for managing git worktrees for Ticket-based development. Triggers include: creating a worktree for a new ticket, checking worktree status, viewing all worktrees, or any mention of /worktree, worktree management, feature branches, or setting up development environment."
argument-hint: "<subcommand> [args]"
allowed-tools: Bash, Read, Write, Edit
metadata:
  version: 1.5.1
---

# Worktree Management SKILL

統一 Git Worktree 管理工具 — 簡化並行開發流程。

## 核心功能

管理 git worktree，自動從 Ticket ID 推導分支名和路徑。支援多 Ticket 並行開發時的環境隔離。

---

## Agent isolation worktree（cc 自動建 worktree-agent-*）

> 完整行為說明（機制、base ref 陷阱、dart MCP 洩漏、ticket 狀態 root 分離、殭屍清理、EnterWorktree mid-session 切換）：`references/agent-isolation-worktree.md`（按需讀取）。本節僅速查表，逐項路由。

cc runtime 派發 `isolation: "worktree"` 的 subagent 時自動建立隔離 worktree（`.claude/worktrees/agent-XXXXXXXX`，分支 `worktree-agent-XXXXXXXX`，附 PID lock），與本 SKILL 的人工 `/worktree create` 為不同來源。目的是讓 subagent 檔案改動與主 repo 解耦，避免並行派發互相覆蓋。

| 議題 | 一行結論 | 詳見 references 節 |
|------|---------|-----------------|
| worktree base 落點 | base 取自 `origin/main`（非 local main HEAD），落後時建在 stale 基底；派發前先 push | 〈Base ref 與隔離邊界〉 |
| dart MCP 寫入洩漏 | daemon root 綁主 repo，worktree 內禁用 dart MCP 寫入工具，改 Bash `dart fix`/`dart format` 或 Edit | 〈Base ref 與隔離邊界〉 |
| ticket 狀態該寫哪 | ticket md 讀寫恆落主倉庫（刻意設計，非洩漏）；程式碼提交才走 worktree 分支，`ticket track commit` 需帶 `--worktree` | 〈ticket 狀態統一寫入主倉庫〉 |
| 殭屍累積 | cc 結束不自動 remove，累積佔磁碟；本專案有 SessionStart hook 自動 GC | 〈殭屍問題〉〈手動清理指令〉 |
| 與人工 /worktree create 的區別 | 路徑/分支/生命週期/清理機制皆不同，判別看路徑前綴（`.claude/worktrees/agent-` vs `../ccsession-`） | 〈與人工 /worktree create 的區別〉 |
| EnterWorktree mid-session 切換 | v2.1.157 起可中途切換 worktree；切換後須 `git branch --show-current` + `pwd` 查核再 commit/merge | 〈EnterWorktree mid-session 切換〉 |

**Action**：遇上述議題任一者，先查 references 對應節再處置，不要憑印象操作。

---

## worktree 不含的狀態（0.2.1-W3-274，框架 issue 46）

> **核心概念**：git worktree 是**版本控制層**的隔離機制，只複製 git 追蹤的內容（已 commit 或已 staged 的檔案）。任何 `.gitignore` 排除、或執行期才產生的狀態，都不會隨 worktree 建立而出現在新的工作目錄中。適用於本 SKILL 的人工 `/worktree create` 與 cc runtime 自動建立的 agent isolation worktree 兩者。

### 三類典型非 git 狀態

| 類別 | 說明 | 典型症狀（未補齊時） |
|------|------|---------------------|
| gitignore 排除的產物 | 建置或套件管理工具產生但被 `.gitignore` 排除的檔案或目錄 | 測試/建置找不到對應資源，錯誤訊息通常不直接指向「worktree 缺此目錄」這個根因 |
| 建置快取 | 編譯器/工具鏈的中介快取（非追蹤內容，重建耗時但非必要進 git） | 首次建置變慢，或依賴快取的步驟失敗 |
| 依賴目錄 | 套件管理器安裝的第三方依賴（通常 `.gitignore` 排除，體積大不適合進 git） | 依賴解析/引用失敗 |

**Why**：worktree 共享 git object store，但各自的 working directory 是獨立生成的——`.gitignore` 排除的內容從未進入 git object store，自然不會出現在任何新建立的 worktree 中，與 base 落後 main 幾個 commit 是完全不同的機制（見 `references/agent-isolation-worktree.md`〈Base ref 與隔離邊界〉：該節處理「git 追蹤內容落後多少」，本節處理「git 完全不追蹤的內容從未存在」）。

**Consequence**：未載明補齊方式時，代理人各自在 worktree 內摸索，成功與否取決於個別代理人是否碰巧試出正確命令，同一問題在不同代理人間重複發生而無人留下可複用記錄（框架 issue 46 症狀一實證：四個代理人三個撞牆且回報各異，有解法但不在任何文件或 prompt 中）。

**Action**：具體前置命令屬於 consumer 專案知識（依語言/框架/套件管理器而異），**本 SKILL 不列舉任何專案專屬命令字面**。consumer 專案應：

1. 在專案層文件（`CLAUDE.md` 對應章節或 `scripts/` 下的腳本）記錄本專案 worktree 建立後所需的前置命令
2. 派發需在 worktree 內執行測試/建置的 agent 時，在派發 prompt 引用該文件——見 `.claude/references/agent-dispatch-template.md`「環境前置欄位」

**例外：可自動補齊的 gitignore 排除產物**——當缺漏檔案內容為固定樣板（無機器相依內容，可用固定字串重建，非真正的本機產物）時，`worktree_manager.py` 的 `create` 子命令會直接寫入補齊，不需 agent 手動介入。目前涵蓋：macOS 平台的 `macos/Flutter/Flutter-Debug.xcconfig`、`Flutter-Release.xcconfig`（僅 `#include` 相對路徑，Flutter 官方樣板固定內容）。此類補齊僅在 worktree 內偵測到對應平台目錄（如 `macos/Flutter/`）時才動作，對不含該平台的專案為無操作（no-op），不違反上述「不列舉專案專屬命令」原則——此為程式碼層的 opinionated default，非文件字面列舉。CocoaPods（`Pods/` 目錄）因需網路且耗時，不自動執行 `pod install`，`create` 完成時僅輸出提示指令。

---

## 快速開始

### 建立 Worktree

```bash
/worktree create 1.0.0-W9-002.1
```

自動建立：
- 分支：`feat/1.0.0-W9-002.1`
- Worktree：`../ccsession-1.0.0-W9-002.1`

建立完成後輸出 `cd` 指令，一鍵切換工作環境。

### 查看 Worktree 狀態

```bash
# 查看所有 worktree
/worktree status

# 查看特定 Ticket 的 worktree
/worktree status 1.0.0-W9-002.1
```

顯示：
- 路徑和分支
- 相對於 main 的 commit 領先/落後情況
- 未 commit 的變更數

---

## 子命令詳細說明

> 完整參數表、推導規則、成功範例與錯誤情境：`references/subcommands.md`（按需讀取）。本節保留於〈快速開始〉的最小指令示範已足夠日常使用；需要查特定參數或錯誤訊息時才讀該檔。

- `create`：建立 worktree，見 `references/subcommands.md`〈create — 建立 Worktree〉
- `status`：查看 worktree 狀態，見 `references/subcommands.md`〈status — 查看 Worktree 狀態〉

---

## 使用場景

### 場景 1：新 Ticket 開發

```bash
# 1. 收到 Ticket 1.0.0-W9-002.1
# 2. 建立 worktree（自動推導名稱）
/worktree create 1.0.0-W9-002.1

# 3. 一鍵切換環境
cd /path/to/project-1.0.0-W9-002.1

# 4. 開始開發...
```

### 場景 2：多 Ticket 並行開發

```bash
# 建立多個 worktree（隔離環境）
/worktree create 1.0.0-W9-002.1
/worktree create 1.0.0-W9-002.2
/worktree create 1.0.0-W9-002.3

# 查看整體狀態
/worktree status

# 查看特定 Ticket 進度
/worktree status 1.0.0-W9-002.1
```

### 場景 3：檢查進度

```bash
# 在任何 worktree 中執行，檢查全局狀態
/worktree status

# 確認該 Ticket 有多少未提交變更
/worktree status 1.0.0-W9-002.1
```

---

## 與 Hook 系統的整合

### branch-verify-hook

在保護分支（main）上編輯時：
- **允許**：`.claude/`、`docs/` 路徑的編輯（規則更新、文件維護）
- **阻止**：程式碼路徑編輯（如 `ui/lib/main.dart`）
- **建議**：使用 `/worktree create <ticket-id>` 建立隔離環境

### branch-status-reminder

Session 啟動時：
- **正確環境**（在 worktree + allowed 分支）→ 靜默
- **異常環境**（主倉庫保護分支）→ 警告 + 建議使用 `/worktree create`

---

## 常見問題

### Q: Worktree 與分支的對應關係是什麼？

**A**: 一個 worktree = 一個獨立的分支 + 隔離的檔案系統。

- 建立 worktree 時同時建立分支
- 多個 worktree 間檔案變更隔離
- 每個 worktree 有獨立的 git working directory

### Q: 能否指定 base 分支？

**A**: 支援。使用 `--base` 參數：

```bash
/worktree create 1.0.0-W9-002.1 --base develop
```

### Q: Dry-run 模式有什麼用？

**A**: 檢查將要執行的 git 命令，不實際建立分支和 worktree。適合驗證操作是否正確。

```bash
/worktree create 1.0.0-W9-002.1 --dry-run
```

### Q: 如何刪除 Worktree？

**A**: 使用 git 命令（本 SKILL 暫不支援刪除）：

```bash
# 刪除 worktree（保留分支）
git worktree remove ../ccsession-1.0.0-W9-002.1

# 刪除分支
git branch -d feat/1.0.0-W9-002.1
```

---

## 參考資料

- Git Worktree 官方文件：https://git-scm.com/docs/git-worktree

---

## 修改 source 後無需重新安裝（shim 化）

> **重要**：本 skill 已改用 cwd-resolving shim（ARCH-APP-002 / framework issue #12），不再走 `uv tool install`。shim 每次執行都 `uv run --directory .claude/skills/worktree` 當前專案源碼，修改 source 後改動即時生效，無 stale installed 問題（取代舊 `uv-tool-staleness-check-hook` 機制）。

**檢查 / 安裝指令**：

```bash
# 安裝 / 更新 shim（一次安裝 ticket / doc / worktree）
python3 .claude/scripts/install-skill-clis.py

# 檢查是否已 shim 化（exit 0/1）
python3 .claude/scripts/install-skill-clis.py --check
```

---

版本紀錄在同目錄的 `CHANGELOG.md`。
