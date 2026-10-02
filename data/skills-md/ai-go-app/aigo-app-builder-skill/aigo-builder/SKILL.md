---
name: aigo-builder
description: >
  Use when working on an AI GO Custom App (ai-go.app)：開發前端（React + TypeScript）
  或 Server-Side Action（Python）、部署與驗證、從零規劃新 App（需求盤點、
  Custom App／Hosted App 產品線判斷）、規劃使用者授權架構（角色、app 角色白名單、
  批次邀請內外部人員）、規劃資料架構（資料中心自建表 / Data Reference）、
  接 Webhook 或設定 App 排程、將現有系統或整套專案
  （前端＋後端＋DB；Supabase / Google Sheet / MySQL 等）搬入／遷入 AI GO。
---

# AI GO Custom App Builder

本 Skill 協助 AI Agent 開發 AI GO Custom App。支援 Antigravity / Claude Code / Cursor。

## 設計理念

AI GO Custom App 採用 **TypeScript（前端）+ Python（後端）** 的精選語言組合，
具備低出錯率、靜態型別安全、LLM 生成最佳化等特性，最適合 AI Coding 新手與非技術工作者
開發可靠的公司內部系統。

資料存取統一走 API，不直連資料庫——避免非技術 AI Coder 重複建立類似的表或欄位。
AI GO 預先定義了中小企業通用的資料庫結構（預設表），同時保有**自建表**的擴充彈性。

> 詳見 `references/custom-app-dev-guide.md` §21 架構設計理念。
> **術語先讀 `CONTEXT.md`**——表只有**預設表／自建表**兩大類；
> 「CustomObject / Data Reference / 延伸欄位 / app_domain」是機制詞不是第三類表。
> 六個詞容易混用，混了就會寫錯 code。（舊文件的「SaaS 表」＝預設表，已停用）

## Phase -1：Skill 自我更新（每次觸發時執行，發現新版即強制同步）

> 若已裝 SessionStart hook（見 README「保持更新」），本階段會自動被跳過（節流），
> 不必重複執行。

```bash
python scripts/check_update.py     # macOS / Linux 用 python3
```

- **零相依、不走 uv**——標準函式庫實作，任何專案下都能直接跑。
- **腳本自己動手，不徵詢**：只要遠端 `VERSION` 比本地新，腳本就**直接把本機所有已註冊
  安裝強制同步到遠端 main**——git 安裝 `fetch` + `reset --hard` + `clean`，複製式安裝
  （skills CLI）下載 `main.zip` 鏡像覆蓋。本地修改、分岔的 commit、多出來的檔案一律被
  遠端取代；不問使用者、不等回覆。你不需要也**不可以**替使用者做「要不要更新」的決定。
- **無輸出 = 沒事**：已是最新版、離線、或同一版本差 3 小時內已失敗過一次都靜默結束，
  直接進 Phase 0。（節流只抑制網路抓取與失敗重試；版本比對每次都做，
  所以本機多份安裝共用遠端快取，任一份落後都抓得到。）
- **有輸出 = 已經同步過了（或同步失敗）**，逐行處理：
  - **「已同步」**→ **立刻重新讀取 `SKILL.md` 與相關 `references/`**，讓新版指令在本回合
    就生效；把版本落差與變更摘要**告知**使用者（告知，不是徵詢——更新已完成，
    沒有拒絕的選項）。
  - **「失敗」**→ 把失敗原因與腳本印出的手動指令給使用者，請他們處理完再繼續。
    若同時有「破壞性變更」警語（`--json` 為 `"breaking": true`）：這類版本代表
    **停在舊版就會失敗，且失敗訊息通常不指向真正的原因**（例如 1.7.0 的租戶網址規則，
    症狀是與密碼錯完全同形的 401）——明確告訴使用者「不處理的話會遇到什麼」，
    後續遇到相關錯誤時**優先回頭懷疑版本落差**，不要往其他方向深掘。
  - **「開發副本，略過」**→ 那份是正在改 skill 的工作區（本地版本高於遠端，或 git 不在
    main／master 分支），不是安裝，不用處理也不用提。
- **註冊表只認得執行過 1.17.0+ 檢查的安裝**——使用者若提到其他專案也裝了本 skill
  卻沒被同步到，提醒他們到該專案觸發一次 skill，之後那份就會入列、下次一起被同步。
- **禁止繞過**：不要為了保住本地修改而跳過本階段、改用 `--check-only`、或建議使用者
  這麼做。要改 skill 內容，走 repo 的 PR；裝在本機的副本只能是遠端 main 的鏡像。

## 源頭意圖分流（進入流程前先判讀）

任何工作開始前，先分清用戶的意圖是哪一種——三條線的起手完全不同：

| 意圖 | 走法 |
|------|------|
| **開發新 App**（從零做新功能） | 走主流程（Phase 0 →），**但建 app 之前必先完成 Phase 1.5 §1.0 的需求盤點**（四問＋Custom App 能力邊界核對，對稱遷入線的 §2.0）——用戶開場的一句話是題目不是需求；產品線判斷（Custom／Hosted／混合）與授權架構（誰能開、掛什麼角色）在 Phase 1.5 定案後才建 app |
| **現有 App 遷入**（有既存系統／repo／DB 要搬進 AI GO） | **先讀 `references/migration-workflow.md`，從 §2.0 的 stack 盤點做起**（架構師視角：先盤前端／後端／資料的結構，再分流產品線），之後才回主流程 |
| **資料操作，不開發 app**（查、改、批次、匯出自己有權限的資料） | **走 `references/data-operations.md` 的短流程**：`aigo_auth.py status` → `aigo_data.py me` → `perm-check` → 路由查該檔 §4 → `call`／`export`。不進 Phase 0 的 VFS review、不建 app、不走 proxy——用登入者自己的 token 與權限。**寫入前必過該檔 §3.5 的寫入閘門**——這條線打的是唯一一份正式資料，沒有沙箱也沒有還原路徑 |
| **成員／角色管理，不開發 app**（批次邀請、建連結、開角色、改權限、設 app 角色白名單） | **走 `references/member-admin.md`**（§2 端點、§4 邀請流程、§5 角色 CRUD）：登入者本人的 JWT，不建 app、不走 `/open/*`；寫入同樣過 `data-operations.md` §3.5 閘門（邀請與改角色都是不可逆的正式資料） |

**資料操作意圖的偵測訊號**：用戶要「查一下／改一批／匯出／灌資料」而沒有提到畫面、功能、
app；或問「我有沒有權限看某表」。這條線的權限是使用者在平台介面上的權限：預設表依模組
角色（`sale.read` 等），自建表需 `builder.access`——先跟用戶說清楚再動手，寫入前必經用戶確認。

**遷入意圖的偵測訊號**（出現任一就主動確認，不要等用戶自己說「遷移」）：
用戶提到現有系統、既有網站、某個 repo、Supabase／Google Sheet／MySQL 等資料來源、
「搬過來」「轉移」「改用 AI GO」等字樣；或 Phase 0 時發現工作目錄是一個
非 AI GO 結構的完整專案。判成遷入後，多系統（≥2 個）再疊加 Phase 1.25 的全局盤點。

## Phase 0：Review 現有 Code（★ 強制步驟）

> **每次開始任何開發工作前，必須先執行此步驟。**

### 九步（★ 完整版與每步的端點、報告內容 → `references/review-workflow.md`）

```bash
uv run --project scripts python scripts/aigo_auth.py status   # 1. 找工作區、定目標
# 2. get_token() 自動取 JWT——★ 不要向用戶要密碼、不代填、不放進指令列
# 3-5. review_app() 一次做完：取 VFS → 檔案清單與 [SDK]/[INJ] 標記 → 路由與頁面 → legacy 偵測
#      → builder.access 破口偵測 → webhook 宣告 → Data Reference 盤點 → CSS 相容性
```

**三道不可跳過的盤點**（跳過的代價都是事後才發現、且要重做）：

| 盤什麼 | 為什麼 | 怎麼盤 |
|---|---|---|
| **租戶既有自建表**（★ 強制） | 自建表是**租戶級**、不在 VFS 裡——兩個 app 各建一張「客戶」表＝資料分裂成兩份 | `GET /data-center/tables`；順手掃命名（`^tbl(_\d+)?$` 等保底名，規則 18.5），**只盤不動手** |
| **既有排程** | republish 或改 action 名稱會把排程觸發到自動暫停 | `GET /builder/apps/{app_id}/crons` |
| **對外呼叫與 Egress** | 舊 code 能跑不代表新 slug 也通；靠平台代灌金鑰的與 raw `httpx` 的都**必改** | 撈出 action 裡所有 `ctx.http.call` slug 與對外網域 |

- **Data Reference 一律用 `GET /api/v1/refs/apps/{app_id}`**，不要讀 `src/db.json`（實測恆為 `{}`）
- ⚠️ 自建表清單取不到時回**空清單**——空清單不等於「租戶沒有表，可以放心建新的」
- **步驟 9：確認已完全理解現有結構，才可進入開發**
## Phase 1：環境設定

### 三條硬規則（★ 不可違反；完整說明見 `references/environment.md`）

1. **所有 API 一律打租戶空間 `https://[tenant].ai-go.app/*`**。apex `https://ai-go.app` 推不出租戶，
   ★ 實測回 `401 帳號或密碼錯誤`——**與密碼真的打錯完全同形**，會把你帶去查錯方向。
   `*.apps.ai-go.app` 是 app 執行期網域，不是 API host
2. **憑證由用戶自己填**：`~/.aigo/.env`（機器級）或 `<工作區>/.aigo/.env`（覆寫）。
   agent 不得代填密碼、不得把 token 印出來、不得寫進 repo
3. **工作區不能放在 skill 安裝目錄裡**——更新會整個資料夾重建，憑證與登錄表會被清光

### 最短設定路徑

```bash
uv run --project scripts python scripts/aigo_auth.py setup                 # 建 ~/.aigo/.env 範本（用戶自己填）
uv run --project scripts python scripts/aigo_auth.py setup-workspace <目錄>  # 建工作區 .aigo/config.json
uv run --project scripts python scripts/aigo_auth.py status                # 確認實際生效的租戶空間與憑證
uv run --project scripts python scripts/aigo_auth.py login                 # 驗證憑證（不印 token）
uv run --project scripts python scripts/aigo_auth.py app add <alias> --id <uuid>   # 登錄 app
```

- **三層模型**：裝置（skill 一份）→ 工作區（一個租戶一個目錄，`base_url` 在 `config.json`）→
  app（工作區的 `apps` 登錄表，多 app 未指定會報錯列出 alias、不猜）
- **新 app 用 API 建，不必走 UI**：`POST /api/v1/builder/apps`，`name` + `template_slug` 必填；
  ★ **access_mode 由模板決定、建立後不可改**，且**建 app 只在 Phase 1.5 計畫確認後**
  （`starter-internal` 是預設；`starter-external` 只在分配表明寫時用）→ `custom-app-dev-guide.md` §26
- `config.json` 欄位、`base_url` 的三層來源與優先序、登入 401 的排查 → `references/environment.md`
- **Hosted App 用 `aigo` CLI 時**：先過 `hosted-apps.md` §3.3 版本閘門（`scripts/aigo_cli_check.py`）；
  既有 app 只部署 → 用戶放 Deploy Token；建新 app／session-only → 用戶自己 `aigo login --workspace`（§3.1）
## Phase 1.25：多系統遷入盤點（條件觸發）

> **觸發條件**：用戶有 **2 個以上外部系統**（各自帶 Supabase / Google Sheet / MySQL
> 等 DB）要遷入 AI GO。僅遷入 1 個系統或純新建 App → 跳過，直接進 Phase 1.5
> （純新建從 §1.0 需求盤點起手）。

> 觸發時 → 讀 `references/migration-workflow.md` §1。目的是在任何單一 App 開始
> Phase 1.5 之前建立**全局視圖**，避免各 App 各自為政導致資料架構混亂；
> 產出的「遷入全景表」會在後續各 App 的 Phase 1.5 持續參照。

## Phase 1.5：需求盤點與實作計畫（★ 強制步驟）

> **在任何開發工作開始前（包含建立 app、從模板建立），必須先完成需求盤點、提出實作計畫
> 並獲得用戶確認。禁止跳過此步驟直接進入 Phase 2 寫 code；也禁止在 §1.0 盤點與計畫確認前
> 建立 app**——模板＝`access_mode`，建立後不可改。

### 1.0 需求盤點 → 四問（★ 缺一不進 1.5）

用戶開場的一句話**是題目不是需求**。一輪問完四問，資訊不足就問、不猜；
已在對話中講過的不重問；遷入情景這四問由 `migration-workflow.md` §2.0 盤點推導，不另問。

| # | 問什麼 |
|---|---|
| 一 | **誰在用**——列出使用者群，以及有沒有不登入就要能看的頁 |
| 二 | **做什麼**——功能清單、使用場景與流程、涉及哪些資料實體 |
| 三 | **對外面向**——需不需要自有網域、SEO、匿名瀏覽整站 |
| 四 | **機制需求**——逐條核 `product-line-decision.md` §2 的 Custom App 能力邊界表 |

另外順帶盤（餵計畫第 4.5–4.7 項）：第三方 API、外部 webhook、定時工作、檔案上傳。

**產出「需求形狀結論」**（照 `resources/new_app_requirements_template.md` 填）。
四問的理由、答不出時給的選項、結論格式 → `references/planning.md` §1.0。

### 計畫內容必須包含（★ 逐項展開在 `references/planning.md`）

| # | 項目 | SSOT |
|---|---|---|
| 1 | 需求分析：功能清單、使用場景、使用者流程 | §1.0 問題二 |
| 1.5 | **產品線與模式判斷**（結果不可逆）→ 產出 **app 分配表** | `product-line-decision.md` |
| 1.7 | **授權架構選型**（角色、`access_role_ids`、邀請）→ 產出 **授權架構表** | `member-admin.md` §1 |
| 2 | 功能群拆分（2 群以上不同目的才拆 app） | `product-line-decision.md` §7 |
| 3 | **資料架構雙軌分流** → 產出 **資料承載表**（每張自建表都要「已對照的預設表／不採用理由」） | `custom-app-dev-guide.md` §19、`default-table-lookup.md` |
| 4 | 頁面與元件規劃、路由結構 | — |
| 4.5–4.7 | 外部 API（egress）、webhook、排程、檔案 | `event-triggers.md`、`custom-app-dev-guide.md` §25 |
| 5 | 驗證方式與里程碑 | `verification-details.md` |

**常駐（`always_on`）兩條線都要有結論，預設都是 `false`**——Hosted 過 `hosted-apps.md` §3.0 三問；
Custom 過 `custom-app-dev-guide.md` §28.1（答案幾乎一律是「關」，沒命中即時互動訊號不必問 owner）。

### 計畫閘門（★ 五條，缺一不得進 Phase 2）

1. 四問未齊，或計畫缺「需求形狀結論」「app 分配表」「授權架構表」「資料承載表」任一張 → 不算完成
2. app 分配表任何一列**沒有常駐結論** → 不算完成（寫「開」要帶「理由 X；退場條件 Y」＋確認付費方案）
3. 資料承載表任何一張自建表缺「已對照的預設表／不採用理由」 → 不算完成
   （issue #53：少了它，46 張表的遷入案第一版判 40 張自建表，對照後只剩 13 張）
4. **必須等用戶明確回覆「同意」**才進 Phase 2；用戶改需求 → 更新計畫再確認
5. 確認後的固定動作：依 app 分配表建 app（**建 app 的唯一時點**）並 `aigo_auth.py app add` 登錄、
   記 `app_domain`、依授權架構表建角色與發邀請（`member-admin.md` §3–§5，每步過
   `data-operations.md` §3.5 寫入閘門）；判走 Hosted 的轉 `hosted-apps.md`

閘門每一條的理由與踩過的坑 → `references/planning.md`。
## Phase 2：專案腳手架

基於 Phase 0 Review 結果決定策略：

- **VFS 為空**：生成全新專案結構
  - 單頁／多頁依 Phase 1.5 計畫第 4 項的頁面架構，**不另問**；計畫沒寫就是計畫不完整，回 1.5 補
  - 單頁：直接渲染，不使用 Router
  - 多頁：HashRouter + Sidebar 導航
  - 可用 `scripts/aigo_scaffold.py` 的 `scaffold_new_project()`

- **VFS 有內容**：下載到本地進行增量開發
  - 將雲端 VFS 下載為本地檔案結構
  - 保留現有所有程式碼
  - 可用 `scripts/aigo_scaffold.py` 的 `download_vfs_to_local()`

## Phase 3：開發指引

### 核心規則（必須嚴格遵守）

1. **框架**：React 18 + TypeScript
2. **路由**：多頁用 `HashRouter`（禁用 `BrowserRouter`）；單頁可不用 Router
3. **CSS**：全域 `App.css`，不支援 CSS Modules / Tailwind
4. **CSS 變數**：必須用 `:host, :root { }` 雙選擇器
5. **HTML 重設**：必須用 `html, :host { }` 雙選擇器
6. **入口點**：必須是 `src/main.tsx`，且 `import "./App.css"`
7. **Layout**：最外層容器必須 `height: 100vh; overflow-y: auto`
8. **Runtime 模組**：react, react-dom, lucide-react, react-router-dom, react-hot-toast 由 Runtime 提供，不可自行安裝
9. **SDK 不可修改**：api.ts, db.ts, action.ts, data.json, db.json, actions.json
10. **Server-Side Actions**：Python，放在 `actions/` 目錄，定義 `execute(ctx)` 函式
11. **Shadow DOM 限制**：`confirm()` / `alert()` / `prompt()` 不可用 → 改用 React state 或 react-hot-toast
12. **前端 `db.ts` 的 db.update() Bug**：需用 `{"data": {...}}` 包裝 payload（直接 fetch，不走 SDK）
    - ⚠️ **2026-09-01 前注入的 `db.ts` 送的是 `PUT`，資料代理只收 `PATCH`——`update()` 恆回 405、
      更新從未生效**（#1416 修正 SDK 模板）。既有 app 若 `src/db.ts` 仍是 `method: 'PUT'` 版本，
      要換成平台最新模板（Builder 重新注入）或直接 fetch 用 `PATCH`；不要把 405 當成權限問題查
13. **前端 `db.ts` 的 db.insert() Bug**：同上，需用 `{"data": {...}}` 包裝
    - ⚠️ **只適用前端**。Server Action 的 `ctx.db.insert(table, data)` 收**扁平 dict**，
      包裝反而會被濾光並回 400。自建表的 `insert_row` / `update_row` 同樣收扁平 dict
14. **開發限制**：取得 App ID 後先用 `scripts/aigo_limits.py` 的 `get_limits(base_url, token, app_id)` 查詢目標平台的 VFS、Action 與 egress 限制，以回應為準。404／503 或連線失敗代表未知，不使用文件中的歷史數值推定當前額度。
    ——單檔超限仍會略過；必須查看 `skipped_files`，不可把 `success: true` 當成完整納入。
    數值以平台為準，見 `references/custom-app-dev-guide.md` §4
15. **完整程式碼原則**：每次更新 VFS 檔案必須提供 100% 完整內容，禁止 `// ...省略` 佔位符
16. **不支援動態 import**：`import()` 語法不支援（lazy loading 除外，esbuild 支援 code splitting）
17. **不支援 Node.js 原生模組**：fs, path, crypto 等無法使用
**規則 18–34（資料、事件、權限、時間、網址、渲染、UAT、撤權）速查——完整版在 `references/dev-rules.md`，**
**動手前逐條核；標 ★ 的違反即停，標 ⚠️ 的違反不會報錯只會算錯：**

| # | 規則 | 標記 |
|---|---|---|
| 18 | **資料承載體：雙軌分流** | ★ 強制 |
| 18.5 | **自建表命名規範：實體名一律英文** | ★ 強制 |
| 19 | **app_domain 標籤規範** | ★ 強制 |
| 20 | **Webhook / 排程 action 必須冪等** | ★ 強制 |
| 21 | **Webhook 宣告只在發布後生效** |  |
| 22 | **排程的四個硬限制** |  |
| 23 | **角色／權限沿用平台，不要自建一套** | ★ 強制 |
| 24 | **預設表寫入可能被簽核攔截** | ★ 強制 |
| 25 | **表沒有 `tenant_id` 不等於沒保護** | ★ 強制 |
| 26 | **`offset` 分頁一律帶唯一鍵排序** | ★ 強制；⚠️ 靜默出錯 |
| 27 | **`ctx.erp.validate_picking` 的冪等要看明細，不能看單據 state** | ★ 強制 |
| 28 | **原生 TIMESTAMP／DATE 是 offset-naive 的 UTC，解析前必須補 `Z`** | ★ 強制；⚠️ 靜默出錯 |
| 29 | **所有 API 一律走租戶空間 `https://[tenant].ai-go.app/*`** | ★ 強制 |
| 30 | **啟動先渲染 skeleton，不要讓長 API 擋住首次渲染** | ★ 強制 |
| 31 | **Internal app 前端禁止直呼自建表 SDK** | ★ 強制 |
| 32 | **禁止以 Hosted App 承載資料庫或 storage** | ★ 強制 |
| 33 | **每支要上正式的 app 都要有一個「UAT 結論」** | ★ 強制 |
| 34 | **沿用 AI GO 登入、同時保留自家認證後端的 app，必須做「即時撤權」** | ★ 強制 |

> 這 17 條的完整說明、判準與實測佐證在 `references/dev-rules.md`（含目錄）。
> 只看表不足以動手的情況：規則 18 的雙軌分流、18.5 的命名兩步法、23 的角色沿用——這三條必讀原文。
### Server-Side Action 撰寫（★ 四條硬規則；`ctx` 清單見 `custom-app-dev-guide.md` §7）

```python
def execute(ctx):
    data = ctx.params.get("key", "default")          # webhook / cron 事件也走 ctx.params
    ctx.response.json({"result": data})
```

1. **對外呼叫一律走 `ctx.http.call(<egress-slug>, <path>)`**——runner 是 default-deny egress，
   raw `import httpx / requests / urllib.request` 連不出去（實測 20 秒 timeout）。
   ⚠️ 這些套件 **import 得進來**（語言級沙箱已拆，2026-09-13 實打）——擋的是**網路層**，
   別把「能 import」當成能用
2. **slug 必須先在 Builder 建同名「外部服務」並授權給本 app**，否則連不出去。
   這是設定問題，改 code 改不掉；服務被停用也一樣擋（發布 409 `service_inactive`）
3. **金鑰由 app 自帶**：閘道只驗域名、不注入憑證（ADR 0010）——存 `ctx.secrets`，
   action 自組 `Authorization` header
4. **`ctx.db` 沒有結構操作**：執行期不能建表改欄，這是刻意的能力邊界
5. **★ 人工設定政策**：在 AI 開發流程中，外部服務的建立／修改／啟停／刪除與 App 授權，以及
   secrets 的新增／更新／刪除，**由使用者或具權限的管理員在 Builder 手動完成**——外部服務到
   `/builder/{app_id}` 的「外部服務」tab，金鑰到「服務」tab。這是刻意的安全設計：讓人理解並決定
   連線目的地、用途與可能送出的資料。AI 可整理設定需求、做唯讀檢查（`available-egress-services`、
   發布預檢），但**不得透過 API、腳本或代操作 UI 完成上述設定**；持有可用 token 不代表允許代設。
   設定缺口＝「等待人工設定」，**不是 bug**（→ 錯誤處理、`issue-reporting.md`；dev-guide §25.2）

> 逾時有兩道且原文同形：manifest `timeout_ms`（1000～120000，舊 app 要 republish 才換上新值）
> 與 egress 閘道的服務 `timeout_ms`（預設 10000、硬上限 30000）。走 `ctx.http.call` 的 action
> 提早被切是後者，**不是 manifest 沒生效**。閘道另有請求 8 MiB／回應 5 MiB／每分鐘 120 次上限
> → `custom-app-dev-guide.md` §25.4。資料層 403 帶 `reason`／`rule_id` 是租戶資料存取規則擋的，
> 改 code 無解 → dev-guide §27。

### 前端呼叫 Action

```typescript
import { runAction, downloadFile } from "../action";
const { data, file } = await runAction("my_action", { key: "value" });
if (file) downloadFile(file);
```
## Phase 4：部署 + 自動驗證（★ 每次 code 變更後必須執行）

> **原則：每次 code 變更後，都必須完成「同步 → 編譯 → 驗證」循環。**
> 只有通過驗證閘門，才可進入發布或繼續下一輪開發。
> 極小變更（如僅修改文字、CSS 微調）可跳過 Custom Data 和 Action 測試，但編譯驗證不可跳過。

### 4.1 標準部署流程

0. **定目標並印出來**：`app = resolve_app(root, alias)` → `print(app.describe())`
   → GET app 後 `assert_remote_matches(app, info)`。工作區有多個 app 而本次沒指定 →
   `resolve_app` 會報錯列出 alias，**問用戶，不要猜**。`full_deploy()` 自己也會印目標行
1. **同步 VFS**：讀取本地檔案 → PATCH `/api/v1/builder/apps/{id}/source/files`
   - 腳本：`scripts/aigo_sync.py` 的 `sync_to_cloud()`
   - ★ 內建二次驗證：PATCH 後自動 GET 確認 vfs_version 遞增 + 檔案確實寫入
1.5. **語意檢查**（★ 前端有實質修改時必跑）：`uv run --project scripts python scripts/aigo_typecheck.py <專案目錄>`
   - **compile 走 esbuild，只轉譯不驗型別**：`const` 宣告前被使用（TDZ）、找不到名稱、重複宣告
     這類錯誤 compile 全綠、發布後 runtime 白畫面，且堆疊只有 minified 名稱與 esm.sh 的
     React 呼叫鏈（`troubleshooting.md` 白畫面列）。這一步是唯一能在發布前抓到它們的閘
   - 腳本只**阻擋會炸 runtime 的語意錯誤**（TS2448／2454／2451／2300／2304…），
     缺型別套件的噪音只列不擋；本機沒有 Node 會印提示並略過——此時要**告知用戶**
     這道閘沒跑，或請用戶在 Builder AI 用 `check_types` 補跑（平台有此工具但無 REST 端點）
2. **編譯**：POST `/api/v1/compile/compile/{slug}?dev=true`
   - 腳本：`scripts/aigo_compile.py` 的 `compile_app()`
   - 成功或失敗都讀 `skipped_files` 並告知用戶每個 path／UTF-8 bytes／reason；`[]` 才代表未略過，缺欄位或 null 代表舊服務或本次未編譯，不能當成完整納入。發布回應同樣檢查此欄位。
   - ⚠️ `success: true` 且 `compile_errors: []` 只代表**轉譯成功**，不代表程式語意正確（見 1.5）
   - 要讓用戶**在瀏覽器看草稿**：internal 開 `{tenant}.ai-go.app/runtime/version-test/{識別碼}`
     （需 `builder.access`）；external 的測試網址還要 `?preview_token=`（Builder 工具列「預覽」會自動帶），
     形狀表與識別碼規則見 `references/platform-behaviors.md` §6.2——**不要自己拼**
3. **編譯失敗**：解析錯誤 → 嘗試自動修復 → 重新同步 → 重新編譯（最多 5 次）
4. **編譯成功 → 進入驗證閘門**（Phase 4.2）

### 4.2 驗證閘門（Verification Gate）

每次編譯成功後，根據**變更範圍**自動決定需要執行的驗證項目：

#### 變更範圍判斷規則

| 變更類型 | 影響範圍 | 需執行的驗證 |
|---------|---------|------------|
| **CSS 微調**（僅 App.css 變動） | 極小 | ✅ Compile 產物 |
| **文案/UI 修改**（僅 TSX 變動，無新 import） | 小 | ✅ Compile 產物 |
| **元件新增/重構**（新增 TSX、修改路由） | 中 | ✅ Compile 產物 + ✅ Publish 一致性 |
| **Custom Data 相關**（修改了使用 api.ts/db.ts 的程式碼） | 中 | ✅ Compile 產物 + ✅ Custom Data CRUD |
| **Server Action 變更**（actions/*.py 修改） | 中 | ✅ Compile 產物 + ✅ Server Action 呼叫 |
| **多個範圍同時變動** | 大 | ✅ 全部 4 項驗證 |
| **首次部署或架構變更** | 大 | ✅ 全部 4 項驗證 |

> 要**實際執行**這四項驗證 → `references/verification-details.md` §1
> 有每一項的完整檢查條目與函式簽名。

### 4.3 驗證後決策

| 驗證結果 | 下一步 |
|---------|--------|
| ✅ 全部通過 | 可進入發布（4.4）或繼續開發 |
| ❌ Compile 失敗 | 回到 Phase 3 修復程式碼 |
| ❌ CRUD/Action 失敗 | 檢查 API 使用方式、表結構、Action 邏輯 |
| ❌ Publish 一致性失敗 | 重新 sync → compile → publish |

> 任何一項失敗 → 先查 `references/troubleshooting.md` 對症狀，再動手改。
> ⚠️ CRUD 驗證打預設表時，回傳 `approval_status: "pending"` 或「需要簽核審批」例外
> **不算驗證失敗**——那是租戶簽核流程攔截（核心規則 24），不要當成 bug 去改程式。

### 4.4 發布

只有通過驗證閘門後才可發布：

1. POST `/api/v1/builder/apps/{id}/publish`
   - 腳本：`scripts/aigo_publish.py` 的 `publish_app()`
   - ★ 內建二次驗證：POST 後自動 GET 確認 status == "published"
   - ★ POST 前內建 `egress_preflight()`：比對 `_template.json` 的 `required_egress` 宣告、`actions/*.py` 的
     字面 `ctx.http.call` slug 與本 App 已授權的外部服務——起手式殘留的 `openai` 在這裡就會被指出來，
     不用等 409（`troubleshooting.md` EGRESS_NOT_READY 列；起手式要清的兩個檔見 dev-guide §26.2）
   - 三個 query 參數預設都不帶，**409 回來先讀 `code` 再決定**（dev-guide §8 分流表）：
     `confirm_removal=true` 只在用戶確認要移除該 action；`confirm_egress_gaps=true` 只在確定用不到那個
     slug；`auto_rollback=true` 是發布後自動編譯驗證、失敗退回上一版並回 422——要開得讓用戶知道會退版
2. 發布後執行 Publish 一致性驗證；**發布後立刻呼叫 action 回 503 是 runner 冷啟動**，等 `Retry-After`
   再試，不是發布失敗（`troubleshooting.md` 503 列）

### 樂觀鎖

- GET App 時記錄 `vfs_version`
- PATCH 時帶入 `expected_version`
- 409 → 重新 GET → 合併 → 重試

### 自動修復策略

| 偵測問題 | 自動修復 |
|---------|--------|
| `:root {` 無 `:host` | → `:host, :root {` |
| `html {` 無 `:host` | → `html, :host {` |
| BrowserRouter | → HashRouter |
| 缺少 `import "./App.css"` | → 在 main.tsx 頂部加入 |

可使用 `scripts/aigo_sync.py`、`aigo_compile.py`、`aigo_publish.py`。

## Phase 5：完整 E2E 驗證（里程碑驗證）

> Phase 4 的驗證閘門每次迭代自動執行；Phase 5 是**開發里程碑完成**
> （功能全部完成、準備交付）時的完整驗證。

> 要執行時 → `references/verification-details.md` §2 有完整清單與呼叫範例。

## 驗證流程快速參照

```
每次 code 變更：
  sync → compile → ✅ Compile 產物驗證
                   └─ (若涉及 Data) → ✅ Custom Data CRUD
                   └─ (若涉及 Action) → ✅ Server Action 呼叫
                   └─ (若涉及路由/元件) → publish → ✅ Publish 一致性

里程碑交付：
  上述全部 + 角色白名單實測（用不在 `access_role_ids` 內的帳號開 app 應 404）+ 匿名存取（僅判進 external 的 app）
  + 常駐狀態對帳（dev-guide §28.1）：用 `GET /builder/apps` **列表**讀回 `always_on`＋`has_messaging_trigger`
    （Builder 線沒有 `GET /runtime-settings`），必須等於計畫那列的結論；寫「開」才在 publish 後
    `PATCH .../runtime-settings {"always_on": true}` 並確認回 `effective_mode: "always_on"`
  + 交付連結實開（照 `platform-behaviors.md` §6.2 組**正式版**網址，用非開發者帳號／external 使用者開一次；`verification-details.md` 第 8 項）
  + UAT 結論對帳（`dev-rules.md` 規則 33）：計畫寫「有」的，`uat-environment.md` §4 驗證表要全過；寫「無」的，理由與風險要在交付說明裡

Hosted App 線（不走 Phase 2–4）：
  任何 `aigo` 指令前 → ✅ hosted-apps.md §3.3 版本閘門（`aigo_cli_check.py` 非零＝瀏覽器登入不可用，先重裝；找不到 `aigo` 時連 token 部署也不行）
  deploy/redeploy → ✅ hosted-apps.md §3.4 部署後驗證閘門（含讀回 `always_on`＝§3.0 決策；未通過不得對外交付）

資料操作線（不開發 app）：
  寫入前 → ✅ data-operations.md §3.5 寫入閘門（估影響面 → 備份 → 試一筆 → 用戶確認）
```

## 錯誤處理

> 任何一步失敗、或收到非預期狀態碼 → **先查 `references/troubleshooting.md`，不要自行推測修法**。
> 查無此症、或照表處理仍卡死 → **自動**進入下方「問題回報」五步，不要反覆重試、不要繞道硬改。

狀態碼語義分野：**403** 權限（結構操作 `datacenter.schema_write`／`system.admin` 與記錄 `builder.access` 降級動作不同；body 帶
`reason`／`rule_id` 是租戶資料存取規則 → dev-guide §27）｜**409** 配額或衝突｜**422** 輸入不合法｜
**400** 業務規則拒絕｜**503 「app runner 暫時不可用」** 三種成因同形：先問有沒有 publish
（`status: draft` 重試不會好）→ 剛發布的冷啟動（等 `Retry-After`）→ body 帶 `quota_hint` 是租戶
運算配額（**不是 code 問題**，把原文轉給用戶）｜**`aigo login` 瀏覽器登入 401「帳號或密碼錯誤」**
先跑 `aigo_cli_check.py` 看版本，再看登入頁網址是不是租戶子網域，最後才查帳密（`troubleshooting.md`）。

**★ Action 對外呼叫失敗時別急著改 code**：先完整讀出 status 與 error message。
timeout／連不出去＝raw `httpx` 直連（改 `ctx.http.call`）或 slug 沒有同名外部服務／未授權；
401＝action 自己的 header 或 `ctx.secrets` 金鑰不對（閘道不注入也不剝除憑證）。
**指向 Egress 或權限就立刻停止改程式**——那是設定問題，改幾次結果都一樣。確認是外部服務未建立／
停用／未授權或金鑰缺少（發布 409 `gaps[].kind` ∈ `service_missing`／`service_inactive`／`unauthorized`／
`secret_missing`，或呼叫期的 `egress_service_not_found`／`egress_service_inactive`／`egress_not_authorized`）→ 判定為**「等待人工設定」**：告訴用戶這一步是刻意的安全設計，
請到 Builder「外部服務」／「服務」tab 手動完成；列出具體缺項、停止相關重試，設定生效後再驗證。
**不要把這個設定缺口當成平台 bug 回報**，也不要為了「證明」它去打設定寫入 API
（`custom-app-dev-guide.md` §25.2 人工設定政策、§25.3）。
## 問題回報（平台問題 → 開發團隊）

> ★ **預設平台必定正確；開發或使用失敗，預設是自己的操作有誤。不確定就不報。**

**只有一條管道**：`scripts/report_issue.py submit`（開發團隊 Scrum Board 的卡），平台缺陷與**文件缺口**
都走這條，不用問用戶要發到哪；不要替用戶到 GitHub（含本 skill repo）開 issue。用戶或其他說明文件裡的
「意見卡」「回報卡」「開發團隊的卡」都是這條（`references/issue-reporting.md` 開頭）。

**何時自動進入**（任一成立，不必等用戶要求、不反覆重試、不繞道硬改）：
`troubleshooting.md` 查無此症、照表處理仍卡死、實測與 `references/` 明文不符、端點 5xx／流程被硬阻斷。
**優先排除**：等待人工完成 egress／secrets 設定（上段「錯誤處理」）不屬於「照表仍卡死」或「流程被
硬阻斷」，不進回報流程；只有人工操作 Builder 本身失敗、或設定完成後回讀／發布結果與設定矛盾才算。

**五步固定**：自動觸發 → 走完 `references/pre-report-self-grill.md` 六輪自審（每個分支都要有
指令＋輸出當證據）→ 判定（不是平台問題就直接修、前沿還有待查就不報）→ **主動問用戶要不要送**
（給非技術語言的摘要，**不得替用戶決定**）→ 同意才 `submit`。

**三個硬條件**（缺一即拒收，CLI 會擋）：
1. 內容寫**行為不寫解法**——「情境 → 操作 → 結果 → 預期」四段，出現「建議改／根因是」等開藥方措辭拒收
2. `--ruled-out`：自審濃縮的已排除清單，每行一項、至少三項
3. `--user-confirmed`：代表第 4 步已問過用戶且用戶說了送——**沒問過就帶是本節最嚴重的違規**

指令、參數、附截圖、追蹤進度、preflight 查既有卡 → `references/issue-reporting.md`。
## 參考文件

| 檔案 | 內容 |
|------|------|
| `CONTEXT.md` | ★ 術語表——預設表／自建表兩大類＋四個機制詞（含稱謂對照與禁用詞：舊稱 SaaS 表與外部產品名都不出現） |
| `references/dev-rules.md` | **Phase 3 規則 18–34 的完整版**（資料雙軌分流、自建表命名、app_domain、冪等、排程限制、角色沿用、簽核攔截、分頁排序、時間、租戶網址、skeleton、builder.access 破口、Hosted 不承載 DB 與外接庫的唯一例外、UAT 結論、即時撤權）——主檔只有速查表，動手前讀原文 |
| `references/planning.md` | **Phase 1.5 的完整版**：§1.0 四問的理由與選項、計畫九項逐項展開、閘門每一條的踩坑紀錄 |
| `references/environment.md` | **Phase 1 的完整版**：租戶網址規則的推導與 401 同形成因、三層模型、`config.json` schema 2 與 `base_url` 三層來源、設定六步、憑證規則 |
| `references/review-workflow.md` | **Phase 0 的完整版**：九步各自打哪個端點、Review 報告要列什麼、哪些情況標「必改」 |
| `references/custom-app-dev-guide.md` | 核心 API 規格與架構理念；**§6.0 SDK 依模式分流表**、**§29 四條存取通道端點總表（internal／external／匿名／open）**、**§15.1 匿名存取的平台核可三態**、§12 Storage 坑表、**§27 租戶資料存取規則（Auth gate：403 帶 `reason` 的來源）**、§28 冷啟動／常駐（`always_on`）＋**§28.1 Custom 線常駐決策閘（預設關）** |
| `references/data-center.md` | 自建表完整規格（型別、配額、權限、SDK）＋ 延伸欄位（§10） |
| `references/default-table-lookup.md` | **判「平台有沒有同語意實體」時（Phase 1.5 第 3 項、遷入 §2.4 每張表必查）**：業務語言→預設表速查、表名前綴讀法、Meta 面↔引用面對照、必填欄與唯讀表、遷入常見誤判 |
| `references/event-triggers.md` | Webhook 與 App 排程（冪等要求、宣告、限制） |
| `references/product-line-decision.md` | **Phase 1.5 判產品線與模式時（兩條路共用 SSOT）**：預設 Custom App 與偏離訊號、Custom App 能力邊界核對表、兩問四象限（登入者一律 internal）、混合方案分工（含 Hosted 當 Custom 後端）、不可逆前提、app 分配表 |
| `references/member-admin.md` | **Phase 1.5 第 1.7 項授權架構選型的 SSOT ＋ 成員／角色管理 playbook**：內外人員共用帳號體系的立場、三問與授權架構表、邀請／角色端點與權限、`access_role_ids`（兩條線）、批次邀請流程與四個邊界、Hosted internal 身分取得（header＋members context）、既有系統使用者搬遷、403 解讀 |
| `references/migration-workflow.md` | **有現存系統要遷入時**：stack 盤點（§2.0，最先做；**四種 stack 形狀**，含「BaaS 為後端、瀏覽器直連」；原雲端拓撲與本機／外部微服務、排程的落點）、產品線判斷的遷入輸入（§2.1）、專案解構、Schema 映射、使用者與登入的落點（§2.4.5）、資料遷移 |
| `references/uat-environment.md` | **規則 33 的做法**：UAT 結論怎麼下、`version-test` 為何不算、鏡像拓撲、`-uat` 命名、獨立資料庫與憑證、clone Hosted 的正式設定窗口與可見度重設、egress／secrets／Open Proxy 引用、只補測試者、驗證表、維運與退場 |
| `references/verification-details.md` | **要執行驗證時**：四項驗證的完整定義、Phase 5 里程碑 |
| `references/troubleshooting.md` | **出錯時**：錯誤速查表 |
| `references/pre-report-self-grill.md` | **回報平台問題前（必走）**：預設平台正確、六輪自審排除樹、送出條件、已排除清單 |
| `references/issue-reporting.md` | **回報平台問題時**：BDD 撰寫規範、指令、進度追蹤 |
| `references/platform-behaviors.md` | **實測行為補遺**：DB Proxy 分頁與筆數上限、`custom_data` 不可伺服器端過濾、TIMESTAMP 格式、seed 表唯讀、`ctx.erp` 白名單、**app 執行期網址總表（§6.2：internal／external × 正式／測試）**、深連結與「找不到此應用」三層（§6.2）、空渲染偵測、API 權限閘（app 軸；人軸見 dev-guide §27） |
| `references/hosted-apps.md` | **Hosted App（「自訂 App」）產品線**：與 Custom App 的邊界、應用形狀硬規則、部署 API、**部署後驗證閘門（§3.4＝Phase 4.2 的等價物）**、env 規則、錯誤碼對照——Phase 1.5 判斷走這條線或混合方案時讀 |
| `references/data-operations.md` | **資料操作模式（不開發 app）**：四條使用者身分資料面與權限閘、**寫入閘門（§3.5，正式資料不可逆）**、模組 REST 慣例、匯出白名單、Meta 值域、出錯與回報出口（§7）——源頭意圖判成「資料操作」時讀 |
