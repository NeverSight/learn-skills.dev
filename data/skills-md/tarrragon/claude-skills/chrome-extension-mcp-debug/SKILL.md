---
name: chrome-extension-mcp-debug
description: "Chrome Extension 實機測試與 debug 工作流，以 chrome-devtools-mcp 為核心工具。Use when: (1) 完成功能後實機驗證 / manual test / 試看看 / 跑看看 / verify feature, (2) extension debug / popup 不作動 / content script 不注入 / service worker 報錯 / background 出問題, (3) 安裝 unpacked extension / load unpacked / 載入未封裝, (4) 看 console / 看 network / 看 log / view console / inspect requests, (5) 功能更新後重新載入 extension / rebuild reload / reload extension。涵蓋 Manifest V3 service worker / content script / popup / options page 的 chrome-devtools-mcp 工具呼叫流程。不取代 Puppeteer / Playwright 自動化 E2E（CI 用），定位為開發期手動驗證與 LLM-assisted debug。"
license: MIT
metadata:
  version: 1.1.0
  category: chrome-extension-engineering
---

# Chrome Extension Manual Test & Debug with chrome-devtools-mcp

開發 Chrome Extension 時，自動化 E2E（Puppeteer / Playwright）涵蓋迴歸測試，但**功能完成後的實機驗證、popup / content script 行為 debug、network 互動觀察**仍需人工驅動瀏覽器。chrome-devtools-mcp 讓 Claude Code 用 MCP 工具直接驅動 Chrome，把這層工作從「人工 DevTools 操作」變成「LLM 對話式 debug」。

本 SKILL 把五種重複情境變成可呼叫流程：**install / reload / verify / debug-console / debug-network**。

> **前置假設**：`.mcp.json` 已註冊 `chrome-devtools` MCP server（pipe 模式預設，至少含 `--isolated` + `--categoryExtensions`）。若尚未註冊，先做專案級設定（參考各專案的 `docs/` 或 chrome-devtools-mcp 官方 README）。
>
> **不建議**在 `.mcp.json` 設 `--chromeArg=--load-extension=<path>` 預載 extension：(1) 相對路徑在 chrome-devtools-mcp npx 啟動環境不會生效（W1-001.1 / W1-005 實證 `list_extensions` 回空）；(2) 絕對路徑會把開發者本機路徑寫死進 tracked config，跨機器不可移植。改在 Workflow A 用 `install_extension(path="<絕對路徑>")` 動態載入為標準步驟。

---

## Trigger 路由

| 用戶語句訊號 | 進入工作流 |
|------------|----------|
| 「實機跑看看」「驗證看看」「試看看」「manual test」「verify feature」 | [Workflow C: Verify completed feature](#workflow-c-verify-completed-feature) |
| 「popup 不作動」「點 popup 沒反應」「popup 報錯」 | [Workflow D-popup: Debug popup](#workflow-d-popup-debug-popup) |
| 「content script 不注入」「頁面腳本沒跑」「injection failed」 | [Workflow D-cs: Debug content script](#workflow-d-cs-debug-content-script) |
| 「service worker 沒跑」「background 報錯」「SW lifecycle」 | [Workflow D-sw: Debug service worker](#workflow-d-sw-debug-service-worker) |
| 「看 console」「console 有什麼錯」「讀 log」「view log」 | [Workflow E-console: Inspect console](#workflow-e-console-inspect-console) |
| 「看 network」「看 request」「看 fetch」「inspect requests」 | [Workflow E-network: Inspect network](#workflow-e-network-inspect-network) |
| 「載入 unpacked」「install unpacked」「載入未封裝」「load extension」 | [Workflow A: Install unpacked](#workflow-a-install-unpacked) |
| 「重新載入 extension」「reload extension」「rebuild reload」 | [Workflow B: Reload after rebuild](#workflow-b-reload-after-rebuild) |

---

## 三個前置概念

讀懂以下三個概念可大幅降低 chrome-devtools-mcp 操作的試錯成本。未理解三者時最常見的失敗模式：(1) 用 attach 模式找 extension 卻發現 `list_extensions` 工具不可用，誤以為設定錯；(2) 在 host page console 找 service worker log 永遠找不到；(3) 沒有 extension ID 卻嘗試 navigate `chrome-extension://`。下方分別說明判別準則與避雷做法。

### 概念 1：pipe vs attach 兩種啟動模式

| 模式 | 適用 | `categoryExtensions` 工具集 |
|------|------|---------------------------|
| pipe（chrome-devtools-mcp 自啟動 Chrome） | 開發中 unpacked extension | [可用] 完整 |
| attach（連接 `--remote-debugging-port=9222` 既有 Chrome） | debug installed extension | [限制] Chrome 149 前不支援（基礎 console / network 工具仍可用） |

**判別**：若你要看「Chrome Web Store 安裝版」或「使用者已載入 unpacked 的實際 profile」→ attach；若是「我剛 build 完想測一下」→ pipe。**為何不能單一模式涵蓋兩者**：attach 模式接到既有 Chrome 時 `categoryExtensions` 工具集未隨之掛載（Chrome 149 stable 前不支援），pipe 模式則綁定 chrome-devtools-mcp 自啟動的隔離 Chrome 實例，無法看使用者原本的 profile。

### 概念 2：Manifest V3 三個執行情境

| 情境 | 在哪 console 顯示 | chrome-devtools-mcp 工具 |
|------|----------------|------------------------|
| Popup（`action.default_popup`） | 開 popup 後 DevTools 的 console | navigate `chrome-extension://<id>/popup.html` + list_console_messages |
| Content script | host page 的 console（與該頁面 console 共用） | navigate `<target-host>` + list_console_messages |
| Service worker（background） | `chrome://extensions` → 「Service worker」inspector | select_page 選取 SW target + list_console_messages（pipe 模式）/ 手開 inspector（attach 模式） |

**常見誤判**：看 host page console 找不到 service worker 的 log → 三個 console 是分開的，要去對應 inspector 看。**為何分開**：Manifest V3 把 popup、content script、service worker 各跑在不同 V8 isolate，DevTools 也對應分隔上下文（chrome-devtools-mcp 一次只 attach 一個 context），不會自動聚合。

### 概念 3：extension ID 取得方式

Extension ID（如 `abcdefghijklmnopabcdefghijklmnop`）是訪問 `chrome-extension://<id>/...` 必需。取得：

| 方法 | 適用情境 |
|------|---------|
| `chrome-devtools__list_extensions` | pipe 模式自動載入後 |
| 導航到 `chrome://extensions/` 截圖看 | 任何模式 |
| 從專案 `manifest.json` 的 key 欄位 + 公開 key 推算 | 不推薦（複雜，直接看更快） |

---

## Workflow A: Install unpacked

完成 build 後第一次載入 unpacked extension 並確認載入成功。

### 前置

```bash
# 各專案的 dev build 命令，例：
npm run build:dev    # 或 npm run build / yarn dev / pnpm build 等，產出 unpacked extension 目錄
```

### 步驟

1. 在 Claude Code 中：「用 chrome-devtools-mcp 載入 `<unpacked-path>` extension 並列出」
2. Claude Code 呼叫 `chrome-devtools__install_extension(path="<絕對路徑>")`（**必須是絕對路徑**——相對路徑 / `.mcp.json` 預載均不可靠）
3. Claude Code 呼叫 `chrome-devtools__list_extensions`，回傳 extension 清單（含 ID）
4. 確認目標 extension 在清單中 Enabled

### 為何不在 `.mcp.json` 用 `--chromeArg=--load-extension` 預載

**Why**：W1-001.1 / W1-005 實證 chrome-devtools-mcp npx 啟動環境下 `--load-extension=<相對路徑>` 不會生效（`list_extensions` 初次回空）；改絕對路徑雖可載入但會把開發者本機路徑寫進 tracked config 不可移植。

**Action**：所有專案統一改用 `install_extension(path="<絕對路徑>")` 動態載入；`.mcp.json` 只保留 `--isolated` + `--categoryExtensions` 等模式類旗標。

### 預期輸出

```
Extension ID: abcdefghijklmnopabcdefghijklmnop
Name: <YourExtensionName>
Version: x.y.z
Service Worker: <SW URL>
```

### 失敗排除

| 症狀 | 可能原因 |
|------|---------|
| 清單空 | `install_extension` 未呼叫，或 path 非絕對路徑，或路徑指向非 unpacked 結構（缺 `manifest.json`） |
| `install_extension` 報路徑錯 | 傳入相對路徑（必須絕對），或 build 輸出目錄不存在（先跑 `npm run build:dev`） |
| 載入但 manifest 報錯 | manifest.json schema 問題，看 `chrome-devtools__list_console_messages` |
| Permission 缺失 | manifest 缺 host_permissions / permissions，補後重 build → Workflow B |

---

## Workflow B: Reload after rebuild

`npm run build:dev` 重 build 後，extension 不會自動 reload，必須觸發重載。

### 步驟

1. `npm run build:dev`（或專案對應命令）
2. 在 Claude Code 中：「重新載入 extension」
3. Claude Code 兩種做法：
   - 重啟 chrome-devtools-mcp Chrome instance（pipe 模式最乾淨，但會丟失 page state）
   - 導航到 `chrome://extensions/`，找到 extension reload 按鈕點擊
4. 重新執行 `list_extensions` 確認 version / SW URL 更新

### 何時必須 reload

| 變更 | 必須 reload？ |
|------|------------|
| popup HTML / CSS / JS | 不必（重開 popup 即可） |
| Content script | 必須（已注入頁面的舊版仍在記憶體，新 build 不會替換） |
| Service worker / manifest | 必須 |
| Static assets（圖片等） | 不必（瀏覽器直接讀新檔） |

### 預期輸出

reload 後 `list_extensions` 顯示新 version 號或 SW 重啟時間。

---

## Workflow C: Verify completed feature

完成一個功能後實機驗證行為符合 acceptance。

### 適用場景

- 「我剛改完 popup 的搜尋功能，看看跑不跑」
- 「content script 加了一個 banner，看看出現了嗎」
- 「verify the feature works on real page」

### 步驟

1. 確認 extension 已 install + 必要時已 reload（Workflow A/B）
2. 在 Claude Code 中描述「要驗證什麼」+ 「在哪個頁面」+ 「期望什麼結果」
3. Claude Code 呼叫：
   - `chrome-devtools__navigate` 到目標頁面
   - `chrome-devtools__take_snapshot` 取 accessibility tree 看 DOM 結構
   - `chrome-devtools__list_console_messages` 看注入是否成功（content script 有印 init log？）
   - `chrome-devtools__take_screenshot` 視覺確認
   - 若要互動：`chrome-devtools__click` / `chrome-devtools__fill_form` 驅動 UI
4. Claude Code 對照預期結果回報「符合 / 不符合 / 部分符合」

### 預期輸出

| 項目 | 內容 |
|------|------|
| Snapshot diff | extension 注入的 DOM 元素是否存在 |
| Console init log | content script / popup 初始化 log 是否符合 |
| Interactive result | 點擊 / 輸入後行為是否符合 |
| Screenshot | 視覺上是否如預期 |

### 反模式

- [反模式] 只截圖不看 console — 視覺正常但 console 有 error 是常見「半失敗」狀態
- [反模式] 直接 navigate 不等 content script 初始化 — 加 `chrome-devtools__wait_for` 等預期 DOM 出現
- [建議] 三件套：take_snapshot + list_console_messages + take_screenshot 一起看

### 書庫類專案：套用既有 checklist 模板

提取書目的 Extension 專案通常含多步驟流程（登入 → 觸發提取 → storage 寫入 → overview 顯示 → 匯出）。本 SKILL 不重複每書城具體步驟，改引用專案 reference：

| 書城 | Reference 路徑 | 狀態 |
|------|--------------|------|
| Readmoo | `docs/bookstores/readmoo.md` 含「MCP E2E 驗證 Checklist」7 步驟 | 已實作 |
| 博客來 / Kindle / Kobo | — | 未實作 |

**新書城擴充流程**：依 `docs/bookstores/README.md` 模板新增 `<bookstore>.md`，含基本資訊 / 測試 URL / 登入流程 / Content Script 注入點 / debug 觀察點五章節。

**Workflow C 在書庫類專案的標準呼叫**：書庫類專案不另發明步驟，固定按對應 reference 走 4 步驟：

1. 讀對應書城 reference 取得測試 URL、登入需求、SPA 觀察點
2. 依該 reference 的「MCP E2E Checklist」7 步驟跑（install → navigate → 登入 → 瀑布流 → popup → storage 驗證 → overview）
3. 失敗時對照 reference 的 Common pitfalls 表診斷
4. 結果寫入 ticket Solution 或 worklog

---

## Workflow D-popup: Debug popup

Popup 不作動 / 點了沒反應 / 顯示異常。

### 步驟

1. 取 extension ID（Workflow A）
2. Claude Code 呼叫 `chrome-devtools__navigate` 到 `chrome-extension://<id>/popup.html`
3. `chrome-devtools__list_console_messages` 看 popup 載入時的 error
4. `chrome-devtools__take_snapshot` 看 popup DOM 結構是否完整
5. `chrome-devtools__take_screenshot` 看渲染是否正常
6. 若要測點擊：`chrome-devtools__click` 對應元素 → 再 `list_console_messages` 看反應

### 常見問題對照

| 症狀 | 檢查方向 |
|------|---------|
| popup 空白 | console 有 manifest 路徑錯誤？CSS 載入失敗？ |
| 點按鈕沒反應 | event listener 綁定錯誤；popup 重開後 listener 重設 |
| 資料載不到 | popup ↔ background 通訊（chrome.runtime.sendMessage）失敗，看 SW 端 log |

---

## Workflow D-cs: Debug content script

Content script 不注入 / host page 看不到效果。

### 步驟

1. 確認 manifest `content_scripts.matches` 涵蓋目標頁
2. Claude Code 呼叫 `chrome-devtools__navigate` 到目標 host page
3. `chrome-devtools__list_console_messages` 看 content script 是否印初始化 log（建議專案在 content script 開頭加 `console.log('[my-ext] cs loaded')` 便於 debug）
4. `chrome-devtools__take_snapshot` 看 host DOM 是否有 extension 注入的元素
5. `chrome-devtools__evaluate_script`（若可用）執行 `chrome.runtime.id` 確認在 extension 上下文

### 常見問題對照

| 症狀 | 檢查方向 |
|------|---------|
| console 完全沒有 cs log | matches 沒命中（檢查正則、protocol）/ rebuild 後沒 reload |
| log 出現但功能沒跑 | DOM 未 ready 時就跑（加 `DOMContentLoaded` 監聽或 `run_at: document_idle`） |
| 跨 origin 抓不到資料 | host_permissions 缺；CORS 限制 |

---

## Workflow D-sw: Debug service worker

Service worker 沒跑 / background 任務失效。

### 步驟（pipe 模式）

舊版取 SW log 的專用工具已不存在於現行 chrome-devtools MCP 工具集，SW log 改用「切換 target 頁面 + 讀 console」流程取得：

1. Claude Code 呼叫 `chrome-devtools__list_extensions` 取 extension ID 與 SW URL
2. `chrome-devtools__list_pages` 列出所有頁面/背景 target，找到對應 service worker 的 target（`chrome-extension://<id>` 的 background/service worker context）
3. `chrome-devtools__select_page` 選取該 SW target，把後續操作 focus 切到 service worker context
4. `chrome-devtools__list_console_messages` 取 SW console log（此時讀取的是已 select 的 SW context）
5. 對照預期看 init log / 事件處理 log

### 步驟（attach 模式或 categoryExtensions 不可用時）

1. 導航到 `chrome://extensions/`
2. 截圖找目標 extension 的 「Inspect service worker」連結
3. 提示用戶手動點開 SW inspector 觀察（chrome-devtools-mcp 暫無法直接 attach SW inspector context）

### 常見問題對照

| 症狀 | 檢查方向 |
|------|---------|
| SW 啟動後立即 inactive | Manifest V3 SW 是 event-driven，無事件就會睡眠（正常） |
| 重 build 後 SW 不更新 | 必 reload extension（Workflow B） |
| `chrome.alarms` / `chrome.tabs` 監聽不觸發 | manifest permissions 缺；handler 寫在 async function 但沒 keep-alive |

---

## Workflow E-console: Inspect console

只想看 console（不一定 debug 特定問題）。

### 步驟

1. Claude Code 呼叫 `chrome-devtools__navigate` 到目標頁
2. `chrome-devtools__list_console_messages` 取 console 訊息
3. 可選參數：`--level error` / `--level warning` 過濾嚴重度
4. 結果回報含 timestamp / level / source / message

### 三個 console 對照（再次強調）

| 你想看 | 在哪 |
|--------|------|
| content script log | host page 的 console（先 navigate 到 host page） |
| popup log | popup 開啟後 popup 自身 console（navigate 到 `chrome-extension://<id>/popup.html`） |
| service worker log | SW inspector（`select_page` 切到 SW target 後 `list_console_messages`，或手開 SW inspector） |

### 常見誤判

| 症狀 | 根因 | 修正 |
|------|------|------|
| 沒看到 content script log | navigate 早於 cs 注入 / cs 內 console 被 framework 攔截 | 加 `wait_for` DOM 元素出現再 `list_console_messages` |
| log 不完整 | console.log 在 page lifecycle 早於 mcp attach | 重新 navigate 該頁觸發 cs 再讀 |
| 看到 log 但時間錯亂 | 多個 page tab 並存，console 來源混淆 | 用 `--source <url-pattern>` 篩選或先關不相關 tab |

---

## Workflow E-network: Inspect network

看 fetch / XHR / extension 資源載入。

### 步驟

1. Claude Code 呼叫 `chrome-devtools__navigate` 到目標頁
2. 觸發感興趣的操作（點擊 / 等待 polling）
3. `chrome-devtools__list_network_requests` 取網路請求清單
4. 篩選關鍵字（URL pattern / status code / resourceType）

### 篩選技巧

| 想看 | 篩選方式 |
|------|---------|
| API 呼叫 | URL contains `/api/` 或 method=POST |
| extension 自身載入的 asset | URL prefix `chrome-extension://` |
| 失敗請求 | status >= 400 |
| 跨 origin | initiator vs final URL 比對 |

### 配合 console 使用

network 看到 4xx/5xx 後，回頭看對應時間點的 console log 確認應用層錯誤訊息。

### 常見誤判

| 症狀 | 根因 | 修正 |
|------|------|------|
| 看不到 extension 發起的 request | request 來自 service worker，但 attach 模式下未追蹤 SW context | 改 pipe 模式或人工開 SW inspector |
| 看到 request 但缺 response body | chrome-devtools-mcp 預設不存 body（成本高） | 明示需 response body 時請 LLM 用 evaluate 直接 fetch 重發 |
| Pre-flight CORS 看不到 | CORS pre-flight OPTIONS 在某些版本被過濾 | 用 `--all` 參數或檢查 host_permissions 是否齊備 |

---

## 專案測試目標（書城 / 站點特定 URL）

本 SKILL 提供**通用**工作流；具體要測哪些 URL、是否需登入、書城特有的 DOM / API 觀察點屬**專案特定知識**，分離存放：

| 內容 | 位置 |
|------|------|
| 通用 install / reload / verify / debug 流程（本 SKILL） | `.claude/skills/chrome-extension-mcp-debug/SKILL.md` |
| 專案測試 URL、書城登入流程、特定 debug 觀察點 | 各專案 `docs/bookstores/<bookstore>.md`（書庫類專案）或 `docs/test-targets/<site>.md`（其他擴充情境） |

**書庫類 Extension 專案的擴充模式**：一書城一檔（如 `docs/bookstores/readmoo.md` / `books-com-tw.md` / `kindle.md` / `kobo.md`），各檔遵循統一模板（基本資訊 / 測試 URL / 登入流程 / Content Script 注入點 / debug 觀察點）。本專案範例：`docs/bookstores/README.md`（含模板與擴充指引）。

**忽略書城 reference 的後果**：直接套用書城官方首頁 URL 啟動 Workflow C 時，content script 雖能注入但目標頁面不含書目 DOM，`chrome-devtools__evaluate_script` 取不到資料，會被誤判為 content script 注入失敗或 selector 過時，浪費 debug 時間。

**Workflow C 開始驗證前**：先讀對應書城 reference 確認測試 URL 正確。例：Readmoo 書目資料在 `https://read.readmoo.com/#/library` 而非首頁 `https://readmoo.com/`。

---

## 與其他工具的邊界

| 工具 | 定位 | 何時用 |
|------|------|--------|
| chrome-devtools-mcp | 開發期 LLM 驅動 debug | manual test、互動探索、看 console / network |
| Puppeteer / Playwright | 自動化 E2E | CI 迴歸測試、可重複跑、機械 pass/fail |
| Chrome DevTools（手動） | 細節調試 | 設斷點、profile、coverage（MCP 不擅長） |

**判別**：要寫一次跑很多次 → Puppeteer / Playwright；要邊看邊問 → chrome-devtools-mcp；要設斷點 step → 手動 DevTools。

---

## 設定缺失 fallback

`.mcp.json` 未註冊或 `chrome-devtools__*` 工具不可呼叫時：

1. 確認 Claude Code 已重啟（MCP server 設定變更需重啟）
2. 確認 `npx chrome-devtools-mcp --help` 能執行
3. 確認 `.mcp.json` JSON 合法（`python3 -m json.tool .mcp.json`）
4. 若仍失敗，提示用戶以 `npm run build:dev && open -a "Google Chrome" --args --load-extension=<path>` 手動載入後人工 DevTools debug，本 SKILL 流程暫不可用

---

## 反模式速查

| 反模式 | 為何錯 | 改 |
|--------|------|-----|
| 用 chrome-devtools-mcp 跑 CI E2E | MCP server 需 LLM 即時驅動，無機械 pass/fail | 改 Puppeteer / Playwright |
| Content script 改完不 reload extension 就驗證 | 舊版仍在頁面記憶體，新版不會生效 | Workflow B reload |
| Popup 看 host page 的 console 找 popup log | 三個 console 分開 | 開 popup 對應 console |
| Service worker 沒 log 就以為「SW 沒跑」 | MV3 SW event-driven 會睡眠，無事件就無 log | 觸發事件再看 / 看 lifecycle log |
| 只看截圖驗證功能 | console 有 error 但視覺正常 = 半失敗 | 三件套 take_snapshot + list_console_messages + take_screenshot |

---

## 相關文件

- 各專案 `docs/chrome-devtools-mcp-usage.md`（若有）— 專案級設定範例與專屬工作流補充
- chrome-devtools-mcp 官方 README — 完整工具清單與最新限制
- `.mcp.json`（專案根）— MCP server 註冊設定

---

版本紀錄在同目錄的 `CHANGELOG.md`。
