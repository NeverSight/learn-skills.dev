---
name: version-release
description: "版本發布整合工具。Use for: (1) 發布新版本（合併到 main、打 Tag、推送）, (2) 發布前健康檢查（所有 Ticket 完成？CHANGELOG 更新？）, (3) 更新版本文件（worklog 狀態、CHANGELOG）。Use when: 準備發布版本、執行 /version-release check 確認發布前狀態、完成所有 Ticket 後要收尾時。"
metadata:
  version: 2.10.4
---

# Version Release Skill

版本發布整合工具。結合工作日誌檢查、CHANGELOG 更新、Git 操作（合併、Tag、推送、清理）。

## 三步驟發布流程

1. **Pre-flight 檢查** - 驗證 Ticket 完成度、技術債務、版本同步
2. **文件更新** - 清理 todolist、更新 CHANGELOG、確認版本號
3. **Git 操作** - 合併、建立 Tag、推送、清理分支

> 各步驟的完整偽程式碼和檢查邏輯：`references/release-workflow-details.md`

## CLI 使用

```bash
# 啟動新版本
/version-release start --version 0.18.0 --description "測試重寫"

# 啟動新版本（預覽模式）
/version-release start --version 0.18.0 --from 0.17.2 --dry-run

# 完整發布（自動偵測版本）
/version-release release

# 指定版本 + 預覽模式
/version-release release --version 0.19 --dry-run

# 只執行檢查
/version-release check

# 發版收尾：前移非阻擋 pending Ticket 後執行發布流程
/version-release finish --version 0.19

# 只更新文件
/version-release update-docs
```

| 子命令 | 說明 |
|--------|------|
| `start` | 啟動新版本（Options: `--version`(必填)、`--from`、`--description`、`--dry-run`） |
| `release` | 完整發布流程（Options: `--version`、`--dry-run`、`--force`、`--defer-td`） |
| `check` | 只執行 Pre-flight 檢查（發版判準見下方〈發版判準：blocker 阻擋、其餘前移〉） |
| `finish` | 發版收尾：對前移清單逐張 `ticket migrate` 至目標版本，成功後接續 `release` 同一套流程（Options 同 `release`） |
| `update-docs` | 只更新文件 |

### 發版前置關卡：版本必須已凍結

`check`／`finish` 在進入下方 blocker 判準之前，先呼叫 `check_version_frozen`
確認目標版本於 `docs/todolist.yaml` 已標 `scope: frozen`；`finish` 的此關卡
在 Step 0（`migrate_overflow_tickets`）之前，未凍結中止且不產生 migrate 副
作用。未凍結時 exit 非 0 並印：

```
版本 v0.2.0 未凍結，契約 blocker 在凍結前恆為 0，本判定無鑑別力。
請先於 todolist.yaml 標 scope: frozen，並對必要票 set-scope-blocker
```

**Why**：`scope_blocker` 只在凍結後才會被賦值（凍結是「範圍不再開放新收件」
的宣告，blocker 是「凍結範圍內尚未處理」的標記）；凍結前 blocker 恆為 0，
「blocker 清空即可發布」的判準對未凍結版本沒有鑑別力，會恆判可發布。

### 發版判準：blocker 阻擋、其餘前移

`check`／`release`／`finish` 共用同一套判準（`check_worklog_completed` 內部呼叫
`collect_ticket_scope_groups`）：當前版本的 pending／in_progress Ticket 不再以
「池是否清空」為發版判準，改為：

| 分組 | 條件 | 對發版的影響 |
|------|------|-------------|
| 阻擋 | `status: in_progress`（一律） | error，發版中止 |
| 阻擋 | `status: pending` 且 frontmatter 含非空 `scope_blocker` | error，發版中止（訊息含 ticket ID 與 blocker 理由） |
| 前移 | `status: pending` 且無 `scope_blocker` | info，列於「發版時前移」清單，**不阻擋** |

前移清單中每張票依 `compute_overflow_target_version` 計算目標版本：**有已在
`docs/todolist.yaml` 登記且未凍結（`status` 為 `planned` 或 `active`，
`scope` 非 `frozen`）的最近後繼版本時，前移目標一律為該後繼版本**；僅當
無此開放後繼時才回退舊規則（IMP 型別且 `what` 欄位首詞屬新功能動詞
「實作/新增/建立/開發」→ minor+1；其餘 → patch+1）。`finish` 對此清單逐張
執行 `ticket migrate <source_id> <target_id>
--version <target_version>`，任一張失敗即中止、不留半搬狀態。**目標版本
必須已在 `docs/todolist.yaml` 登記**（planned 或 active 皆可），未登記時
整批阻擋並提示先登記，`finish` 不自動登記。

**前移順序**：依 ID 階層深度排序，父票先於子票（同深度維持原序）。父票的子樹遷移會
連帶搬走仍為 pending 的子孫，輪到該子孫時來源已不存在：若目標版本有票的
`previous_ids` 含該來源 ID，輸出 `[INFO]` 略過；否則仍判失敗並中止。前移清單中的票
若有 completed／closed 祖先（留在原版本），單獨前移後新版本缺父票，輸出 `[WARNING]`
列出該票與留下的祖先。

**前移清單與 `check` 建議、`release` 前置條件**：前移屬 `finish` 的職責，`release`
不做前移，在前移清單非空時照做會把 pending 票留在已 completed 的版本下成為懸空票。
因此：

- `check` 通過後，結尾建議依前移清單切換：清單非空印 `finish`（並說明前移 N 張），
  清單為空維持印 `release`。
- `release` 在 Step 0 之前計算前移清單，非空即 exit 1，列出清單並提示改用 `finish`；
  清單為空照常執行。`finish` 不受影響。
- **`--force` 不覆蓋此拒絕**。`--force` 的既有語意是略過「可協商的警告」（Pre-flight
  失敗、文件更新失敗、跨大版本推進）；前移清單是資料正確性（懸空票無法事後由發版流程
  自動修復），不是可略過的警告。要略過前移只有一條路：先處理那些 pending 票（完成、
  或加 `scope_blocker` 轉為阻擋），或改用 `finish`。

範例輸出（`check` 命中前移清單）：

```
[OK] 檢查工作日誌完成度...

  發版時前移（2 個，不阻擋）：
    - 0.1.0-W3-700 -> v0.1.1（修復/改善/分析/文件類型歸下一個 patch（相對凍結版本 patch+1））
    - 0.1.0-W3-701 -> v0.2.0（新功能歸下一個小版本（相對凍結版本 minor+1））
[OK] Worklog 目標達成
```

### start 子命令

程式化版本啟動流程，完整生命週期：`start` -> `check` -> `release`。

**執行步驟**：
1. 前版本驗證（檢查 completed 狀態和 git tag）
2. 專案類型偵測（自動或讀取 `.version-release.yaml` 配置）
3. 重複檢查：todolist.yaml 已有該版本條目（狀態為 `active`／`planned`／
   `pending`）時，改走 `ensure_version_activated` 冪等補齊路徑（見下），
   不再視為錯誤；狀態為其他值（如 `completed`）才 FAIL
4. 全新版本：更新 todolist.yaml（插入新版本條目，字串操作保留格式）
5. 全新版本：建立 worklog 目錄結構和主檔案（從模板生成，路徑依專案類型決定）
6. 全新版本：Bump 版本檔案（依專案類型選擇對應的版本源 + sync targets）
7. 輸出摘要報告和下一步建議

**`ensure_version_activated` 冪等補齊**（既有版本走此路徑，`finish` 自動推進下一版本時亦共用同一常式）：逐項檢查 todolist status、worklog 主檔、版本檔版號、CHANGELOG In Development 段落，只補缺的項目並逐項印出 `[OK]`／`[補]`；全部就位時印「無缺漏」且不改動任何檔案（含 mtime）。version status 為 `completed` 時視為不可逆錯誤，不會被本路徑復原。

## 多專案類型支援

工具自動偵測專案類型並調整版本偵測、bump 策略與 worklog 路徑。支援以下專案類型：

> **monorepo 設定前先決定版本模型**：單一版本號（整個 repo 一個 tag）vs 子專案獨立版本，取捨判準（耦合 / 獨立消費者 / 相容性 / 發布節奏）與兩種配置 recipe 見 `references/monorepo-versioning-strategy.md`。註：現行 `monorepo` 類型預設「子專案各自獨立版本」，統一版本 monorepo 需以主版本源子專案的語言類型 + `version_source.primary` 表達。

| 專案類型 | 識別方式 | 主版本源 | bump 格式 |
|---------|---------|---------|----------|
| `flutter` | `pubspec.yaml` 存在 | `pubspec.yaml` | YAML（支援 `X.Y.Z+build` 自動遞增 build number） |
| `go` | `go.mod` 存在 | git tag | 無檔案 bump（版本由 git tag 管理） |
| `chrome-ext` | `package.json` + `manifest.json` 同時存在 | `package.json` | JSON（自動同步 `manifest.json`） |
| `php` | `composer.json` 存在 | `composer.json` | JSON |
| `npm` | 僅 `package.json` 存在（無 `manifest.json`） | `package.json` | JSON |
| `python` | `pyproject.toml` 存在 | `pyproject.toml` | TOML（支援單引號和雙引號） |
| `monorepo` | 根目錄無版本檔但子目錄（depth=1）含版本檔 | 依子專案 | 依子專案類型 |
| `unknown` | 無任何已知標記檔 | git tag | 無檔案 bump |

### 自動偵測優先序

偵測按以下順序進行，**第一個命中即停止**：

1. `pubspec.yaml` → `flutter`
2. `go.mod` → `go`
3. `package.json` + `manifest.json` → `chrome-ext`
4. `composer.json` → `php`
5. 僅 `package.json` → `npm`
6. `pyproject.toml` → `python`
7. 子目錄含版本檔 → `monorepo`
8. 全無 → `unknown`

若自動偵測不正確，在 `.version-release.yaml` 中明確指定 `project_type` 覆蓋。

### 版本源解析優先序

`resolve_version_source` 依以下優先序決定版本源：

1. `.version-release.yaml` 指定 `version_source.primary` → 使用指定檔案
2. 無配置 → 依 `VERSION_FILE_CANDIDATES` 順序掃描（`pubspec.yaml` > `package.json` > `manifest.json` > `composer.json` > `pyproject.toml`）
3. 全無版本檔但有 `go.mod` → fallback 到 `git-tag`（不 bump 檔案，版本由 tag 管理）

## 版本偵測

偵測優先順序：`--version 參數` -> `git branch (feature/vX.Y)` -> 版本檔案（依語言） -> `git tag`

## 版本策略

### Chrome Extension 雙版本來源

| 來源 | 檔案 | 說明 |
|------|------|------|
| NPM 版本 | `package.json` | 專案主版本，Ticket/Wave 以此為準 |
| Chrome 版本 | `manifest.json` | Chrome Web Store 發布版本 |

`check` 子命令驗證兩者一致，不一致視為錯誤。

### 其他專案類型

| 專案類型 | 版本策略 |
|---------|---------|
| `flutter` | `pubspec.yaml` 為唯一版本源；含 `+build` 後綴時 bump 自動遞增 build number |
| `go` | 無版本檔，版本完全由 git tag 管理；`start` 階段不 bump 檔案 |
| `php` / `npm` / `python` | 單一版本源（`composer.json` / `package.json` / `pyproject.toml`） |
| `monorepo` | 依 `subprojects` 配置各別管理（見 `.version-release.yaml` schema） |

## 前置條件

- Python 3.10+、Git 2.0+、`pyyaml`
- 完成 Phase 4 重構評估，技術債務已分類
- 版本檔案已存在（或使用 git-tag 策略）

## 使用流程檢查清單

- [ ] 所有 Ticket 已完成（無 pending/in_progress）
- [ ] 技術債務已分類到 todolist.yaml
- [ ] 三分流語意分類（框架相關／專案相關／兩者皆非）人工抽查已完成：本版 ticket 標記「發現」的內容皆已依三分流落地（見 `.claude/pm-rules/pm-quality-baseline.md` 規則 7；此項無自動化輔助，須人工逐一確認）
- [ ] 權限需求變更檢查已完成（依專案類型，見「權限需求變更檢查」章節）
- [ ] 運行 `check` 確認所有檢查通過
- [ ] on-device 驗收套件全綠（若專案有 on-device 測試層，如 Flutter `integration_test/`——於驗證環境釘住裝置執行，見「實機冒煙驗證」章節）
- [ ] 實機冒煙清單已執行（若專案有 `docs/release-smoke-checklist.md`，見「實機冒煙驗證」章節）
- [ ] 運行 `release --dry-run` 預覽
- [ ] 運行 `release` 完成發布
- [ ] 驗證 main 分支已更新、Tag 已建立、feature 分支已清理

## 實機冒煙驗證（行動/桌面 APP 專案）

`check` 的自動佔位掃描（preflight 步驟 1.7）只能攔截靜態可查的佔位實作（ComingSoon 路由、UnimplementedError provider、空 callback）；平台 API 語意差異與框架初始化警告只有在目標平台實際執行才會暴露。**Consequence**：缺實機驗證 gate 時，單元測試全綠 + 自動掃描通過的版本仍可能在用戶裝置上功能不可用。**Action**：APP 類專案應維護發版前實機冒煙清單（建議路徑 `docs/release-smoke-checklist.md`，三層結構：啟動健康 / 用例 happy path 走查 / 平台敏感點），`check` 通過後、打 tag 前執行一次，結果記入版本 worklog。非 APP 專案（純 CLI / library）無實機層，此項不適用。

**on-device 驗收套件（存在時先於冒煙清單執行）**：專案有 on-device 測試層（如 Flutter `integration_test/`，測試編譯進真實 app 於裝置執行、零結構替身）時，發版前於驗證環境釘住裝置執行全套並要求全綠（例：`flutter test integration_test -d <device>`）。開發中的外圈紅燈以 wip tag 隔離（dart_test.yaml skip），不影響本 gate；wip tag 於發版時仍存活（即將跨版本）即為異味。若專案已採用 `tdd` skill，處置方式見該 skill 的「紅燈層級順序」節（若已安裝）；若未採用，仍應視為異味並自行決定移除 wip tag 或延後發版，只是不會有現成的分級處置指引可查。on-device 全綠後，手動冒煙清單聚焦自動化涵蓋不了的部分（硬體功能、觀感、探索性走查），兩者互補不重複。

## `.version-release.yaml` 配置檔

配置檔為可選，放置於專案根目錄（`<root>/.version-release.yaml`）或 `.claude/` 目錄下（`<root>/.claude/.version-release.yaml`，後者在 branch-verify hook 豁免路徑內，適用 all-on-main 工作流）。不存在時使用內建預設值。

### Schema

| 欄位 | 型別 | 預設值 | 說明 |
|------|------|--------|------|
| `project_type` | `string \| null` | `null` | 專案類型，`null` 時自動偵測。可選值：`chrome-ext` / `flutter` / `go` / `php` / `python` / `npm` / `monorepo` |
| `version_source` | `object \| null` | `null` | 版本源配置（見下方子欄位）。`null` 時依 `VERSION_FILE_CANDIDATES` 自動偵測 |
| `version_source.primary` | `string` | — | 主版本源檔案相對路徑（如 `package.json`、`pubspec.yaml`） |
| `version_source.parser` | `string \| null` | 依副檔名推斷 | 版本源 parser 類型：`json` / `yaml` / `toml` / `git-tag` |
| `version_source.key` | `string` | `"version"` | 版本 key（json/yaml/toml 用） |
| `version_source.sync_targets` | `list[object]` | `[]` | 版本 bump 時一併更新的檔案清單，每項含 `path` 和 `parser` |
| `subprojects` | `list[object] \| null` | `null` | monorepo 子專案配置，每項含 `path` 和 `version_source` 子配置 |
| `release_workflow` | `string` | `"trunk"` | 發布工作流模式：`trunk`（all-on-main）或 `feature-branch`（merge + 分支清理） |
| `tag_format` | `string` | `"v{version}"` | Tag 命名範本，支援 `{version}` 和 `{major_minor}` 佔位符 |
| `worklog_path_pattern` | `string` | 依專案類型 | Worklog 目錄路徑範本，支援 `{version}` / `{major_minor}` / `{major}` 佔位符 |
| `versions` | `object` | 內建 Chrome Extension 配置 | 版本源定義（`package` / `manifest` 子配置） |
| `sync_rules` | `object` | 內建同步規則 | 版本同步規則（`on_release` / `on_development` / `conflict_detection`） |
| `preflight_checks` | `object` | 內建檢查配置 | Pre-flight 檢查配置 |

### Worklog 路徑預設值

未明確設定 `worklog_path_pattern` 時，依專案類型決定預設值：

| 專案類型 | 預設路徑範本 | 範例（v0.19.0） |
|---------|------------|----------------|
| `flutter` | `docs/work-logs/v{major}/v{major_minor}/v{version}` | `docs/work-logs/v0/v0.19/v0.19.0` |
| 其餘所有類型 | `docs/work-logs/v{version}` | `docs/work-logs/v0.19.0` |

### 各專案類型範例

#### Chrome Extension

```yaml
# .version-release.yaml
project_type: chrome-ext
release_workflow: trunk
tag_format: "v{version}"
version_source:
  primary: package.json
  parser: json
  sync_targets:
    - path: manifest.json
      parser: json
```

#### Flutter

```yaml
# .version-release.yaml
project_type: flutter
release_workflow: feature-branch
tag_format: "v{version}"
worklog_path_pattern: "docs/work-logs/v{major}/v{major_minor}/v{version}"
version_source:
  primary: pubspec.yaml
  parser: yaml
```

#### Go

```yaml
# .version-release.yaml
project_type: go
release_workflow: feature-branch
tag_format: "v{version}"
version_source:
  parser: git-tag
```

#### PHP

```yaml
# .version-release.yaml
project_type: php
release_workflow: trunk
version_source:
  primary: composer.json
  parser: json
```

#### Monorepo

```yaml
# .version-release.yaml
project_type: monorepo
release_workflow: feature-branch
subprojects:
  - path: packages/frontend
    version_source:
      primary: package.json
      parser: json
  - path: packages/backend
    version_source:
      primary: pyproject.toml
      parser: toml
```

## 參考資料

| 資料 | 說明 |
|------|------|
| `references/release-workflow-details.md` | 三步驟完整偽程式碼和檢查邏輯 |
| `references/cli-output-examples.md` | CLI 輸出範例和版本偵測說明 |
| `references/troubleshooting.md` | 常見問題和恢復指引 |
| `references/monorepo-versioning-strategy.md` | monorepo 單一版本 vs 子專案獨立版本的取捨判準與配置 recipe |

## 權限需求變更檢查

版本發布或推進時，若專案有面向使用者的權限宣告，須檢查權限是否較上一發布版本變更；有變更則同步更新權限說明文件與上架頁的權限聲明。**Why**：應用程式商店（Chrome Web Store、Google Play、App Store）審核會比對上架頁的權限聲明與專案實際的權限宣告檔，兩者不符是審核卡關的常見原因。**Consequence**：權限說明 drift 後，審核退件需重新提交，延誤發布。**Action**：發布前依下方專案類型對照表，檢查權限宣告檔差異並同步更新。

### 各專案類型處理方式

不同專案類型的權限宣告位置與更新對象不同，後端服務則無此需求：

| 專案類型 | 是否需檢查 | 權限宣告位置 | 同步更新對象 |
|---------|-----------|-------------|-------------|
| Chrome Extension | 是 | `manifest.json` 的 `permissions` / `host_permissions` | README 權限說明、隱私權政策文件、Chrome Web Store 開發者後台 |
| 行動 APP（Android / iOS） | 是 | Android `AndroidManifest.xml`；iOS `Info.plist` 的 usage description | 權限說明文件、Google Play / App Store 上架頁的權限與隱私聲明 |
| 後端服務 | 否 | 無使用者端權限宣告 | N/A |

### 檢查步驟（適用「需檢查」的專案類型）

1. 比對權限宣告位置的內容與上一發布版本（git tag 或上一 release commit）的差異。
2. 若有新增或移除權限，同步更新上表「同步更新對象」欄列出的所有文件與上架頁。
3. 若無變更，於該版本 worklog 的技術筆記章節標註「權限無變更」。

**相關 Skill**: `tech-debt-capture`（Phase 4 技術債務提取）

---

## 修改 source 後必須重新安裝

> **重要**：本 skill 透過 `uv tool install` 安裝為獨立 CLI，source（本目錄）與 installed（`~/.local/share/uv/tools/<package>/`）是兩份獨立 Python package。修改 source 後若未 reinstall，CLI 仍使用 stale installed 版本，新增的函式會 AttributeError 或被 hasattr 包裝靜默吞掉（W11-037 根因）。

**修復指令**：

```bash
cd .claude/skills/<本 skill 目錄> && uv tool install . --force --reinstall
```

**自動偵測**：每次 SessionStart 由 `uv-tool-staleness-check-hook` 比對 source vs installed SHA256，偵測 stale 時提示修復指令。對應 ticket-skill 本身另有 `ticket-reinstall-hook` 自動 reinstall。

---

版本紀錄在同目錄的 `CHANGELOG.md`。
