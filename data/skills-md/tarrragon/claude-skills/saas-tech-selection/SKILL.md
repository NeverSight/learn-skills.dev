---
name: saas-tech-selection
description: "初始化 SaaS repo 時的設計與選型訪談協議：定錨後先過交付形態 gate（託管平台 / 垂直 SaaS / 辦公生態自動化 / BaaS / 半託管 CMS / 自建）、自建成立才從使用者操作（BDD）推導功能與風險、依 SRP / OCP 切分 domain 與 event（DDD）、再把技術維度掛在領域骨架下逐項確認、每個維度附不可沉默跳過的防護底線、產出設計決策記錄與 scaffold 建議。Triggers: 初始化 repo, 新專案, 開新服務, SaaS 選型, 技術選型, tech stack, 要不要自建, 託管平台, Shopify, Wix, Firebase, WordPress, Apps Script, DDD, domain 切分, event 驅動, event storming, BDD, 行為情境, 使用者操作盤點, 選資料庫, 選 queue, 要不要 redis, 要不要 k8s, MVP 架構, repo scaffold, 專案起手, stack 評估, 選型訪談, 架構訪談."
license: MIT
metadata:
  portable: true
  version: 1.4.1
  category: selection-protocol
---

# SaaS Tech Selection

初始化 SaaS repo 時的設計與選型訪談協議。把「使用者開口要建新服務」到「repo 第一個 commit」之間的設計過程結構化：先盤點要提供使用者哪些操作與風險（BDD）、再切分 domain 與 event（DDD、依 SRP / OCP）、然後把技術維度掛在領域骨架下逐項確認、每個維度附防護底線、最後產出設計決策記錄與 scaffold 建議。

協議的核心命題：**開發到一半的設計變更、成本遠高於訪談階段多問十題**。本 skill 的責任是逼迫設計問題在寫第一行程式之前全部浮現 — 使用者沒想清楚的操作、沒切清楚的領域邊界、沒想到的失敗代價、沒被告知的防護缺口。訪談問題的數量沒有上限、問漏才是成本。

---

## Core Pillars（核心支柱）

| 支柱                                            | 意義                                                                                                                                 |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| **Behavior before System** 行為先於系統         | 功能來源是「要提供使用者哪些操作」、不是開發者想建什麼系統；每個操作帶行為情境、誤操作風險與引導設計、從前端一路對應到後端防護       |
| **Domain-Event Backbone** 領域事件骨架          | 先切 domain、再定 event、技術選型掛在骨架下面；transaction 邊界、queue 訊息、授權配置都是領域模型的投影                              |
| **SRP + OCP only** 兩原則切分                   | domain 與 event 依 SRP 切（一個變更理由 / 一個事實）；domain 依 OCP 分公開面與內部面；LSP / ISP / DIP 留給實作階段、此階段刻意不考慮 |
| **Ask Everything** 問漏才是成本                 | 寫不出行為情境的操作、答不出失敗代價的功能、就追問到寫得出來為止；訪談成本永遠低於開發中變更設計的成本                               |
| **Demand before Product** 需求先於產品名        | 使用者點名產品（「我要用 MongoDB」「上 k8s」）時、先回到需求與領域模型確認；產品名是選型的輸出、不是輸入                             |
| **Explicit Baseline + Tripwire** 底線與重評承諾 | 防護底線可延後、不可沉默跳過（記錄「已告知 + 延後理由 + 重評條件」）；每項決策自帶 tripwire、規模撞牆訊號轉成重評承諾                |

---

## 訪談流程

### Stage 0：定錨

問定錨問題建立規模假設：產品形態（B2B / B2C / 內部工具）、租戶模型、預期規模、團隊能力、上線時程。定錨答案決定後面每個階段的預設方向。

定錨的出口是**交付形態 gate**：先判斷「這個產品現在值得自建嗎」。差異化在軟體本身 → 自建成立、走完整訪談；差異化在商品 / 內容 / 服務、需求落在現成平台的標準域（Shopify / Wix / Google Sites / Apps Script / Firebase / WordPress）→ 訪談走縮減流程、決策記錄換成託管縮減記錄（平台選擇 / 可遷出保險 / 升級自建 tripwire / 防護底線總表適用項）。判讀單位是每條業務流程、混合形態（行銷頁託管 + 核心產品自建）是常態。問法與 gate 判讀見 `references/interview-core.md` 的定錨段。

### Stage 1：使用者操作盤點（BDD）

枚舉所有操作主體（含管理者、客服、訪客、機器角色）與其全部操作、每個操作寫行為情境（Given / When / Then 至少一主一失敗）、盤點誤操作風險、設計前端引導與後端防護的成對對應。寫不出行為情境的操作就是還沒想清楚的需求 — 在這裡打斷、而不是開發到一半才發現。協議見 `references/user-operations-bdd.md`。

### Stage 1.5：畫面狀態矩陣展開（條件式、產品有 UI 元件才執行）

操作清單的「前端引導」欄只描述顯示，容易漏掉操作和退出路徑。產品有 UI 元件時，把操作清單展開成畫面狀態矩陣 — 每個畫面的每個狀態四欄（顯示 / 可用操作 / 進入條件 / 退出路徑）。退出路徑欄為空 = UX 死胡同。每個 gate 用三問展開（成功 / 失敗 / 不確定）。展開原則見 `references/principles/screen-state-matrix-expansion.md`、操作步驟在 `references/user-operations-bdd.md` 的「畫面狀態矩陣展開」段。

### Stage 2：Domain / Event 切分（DDD）

把操作清單轉成 domain map 與 event catalog：操作 → command → 唯一歸屬 domain → event。Domain 依 SRP 切（一個變更理由）、依 OCP 分公開面（別的 domain 需要知道的：event schema、查詢介面）與內部面（不需要知道的：表結構、狀態機）；event 依 SRP 定（一個事實、過去式命名）。切完 domain map 後逐 domain 過 **commodity domain check**：認證、金流、表單、搜尋、通知、物件儲存、後台 CRUD 這類非差異化能力、現成 feature SaaS 已做完的就標「外包 + 整合邊界」、整塊移出 build scope、不模內部 event。命中後用該能力自己的買 vs 建問題集追（每塊的判斷標準形狀不同 —— 認證問 hash 可攜與企業 SSO、搜尋問計費模型與規模拐點、金流問 PCI 與 orchestration、表單問資料怎麼接回來、後台問 per-seat 計費與客製天花板）。協議與逐能力問題集見 `references/domain-event-modeling.md`、深度判讀見 `references/principles/capability-outsourcing-depth.md`。

### Stage 3：核心問題（技術需求判讀）

以操作盤點與 domain / event 切分的產物為輸入、依序確認需求類型、流量形狀、資料生命週期、失敗代價、成本模型、定位與備援、安全邊界。每問附判讀路由：答案訊號決定維度展開階段要進哪些技術維度。問法與路由見 `references/interview-core.md`。

### Stage 4：技術維度展開

維度分兩層進入：

- **必展開**（任何 SaaS 都逃不掉）：state-storage、deployment-platform、security、observability 底線、reliability 底線、verification-surface（實機驗證環境——改動在哪台裝置 / 哪個瀏覽器 / 哪個 runtime 被驅動與觀察；交付形態決定問哪一節，答案下游固化為專案 verify 配方）。
- **觸發展開**（操作盤點 / domain / event 切分 / 核心問題的訊號命中才進）：cache、async-queue、capacity-performance。event catalog 中存在不可丟 event 時、async-queue 直接升級為必展開。

每個維度的 reference 自帶訪談問題、候選類型差異、防護底線與 tripwire；展開時把該維度的問題錨在 domain map 與操作清單上（「Order domain 的不可丟 event 用什麼機制送」、不是抽象的「要不要 queue」）。

每個維度的選型還帶一個 **外包深度** 判斷（self-host / managed 基礎設施 / feature SaaS / 折進跨能力 bundle、見 `references/principles/capability-outsourcing-depth.md`）：交付形態 gate 判「自建」的流程、不等於每個維度都自己跑機器 —— 維度的 day-one 託管預設與領域層的 commodity 買掉是 gate 之外的另一層外包判讀。候選若是跨能力 bundle（一個 vendor 同時給資料庫 + 認證 + 物件儲存 + 即時推送）、逐維度判斷哪幾塊用它、收進同一筆 bundle 決策、整包遷出代價記進 tripwire。

### Stage 5：決策收斂（決策記錄 + scaffold 建議）

依 `references/decision-record-template.md` 產出設計決策記錄：操作風險表、domain map、event catalog、每項技術選型（理由 / 防護狀態 / tripwire）、防護底線總表、規模 tripwire 總表、驗證環境節（格式見 `references/dimensions/verification-surface.md`「決策記錄要記什麼」節）。決策記錄經使用者確認後、才產出 scaffold 建議；scaffold 是決策的下游、修改決策時 scaffold 跟著重生。scaffold 建議包含專案 verify 配方種子（`.claude/skills/verify/SKILL.md` 的 Build & Launch / Observe 骨架，由驗證環境節生成；配方屬專案特化資產、不隨框架 sync 推送）。<!-- portability-allow: 約定位置，指各專案自有的驗證配方安裝點 -->

### Stage 6：銜接 doc 需求文件系統（條件式、專案有 doc skill 才執行）

決策記錄產出後、偵測專案是否載入 doc skill（檢查 `.claude/skills/doc/` 是否存在）<!-- portability-allow: 執行期偵測指令，路徑是所有 consumer 共通的 skill 安裝位置，非特定專案的檔案 -->：

- **有 doc skill** — 決策記錄不只進 `docs/tech-decisions.md`、還移交 doc 系統長成需求文件：操作風險表（BDD）轉 usecase、domain map + 介面契約（DDD）轉 spec、定錨 + 交付形態 gate + 技術決策轉 proposal。移交前先過閘門：§1 / §2 任一為空即回補 Stage 1 / 2、不可硬生半成品。映射細節與移交步驟見 `references/decision-record-template.md` 的「銜接 doc 系統」節。
- **無 doc skill** — 維持現狀、決策記錄獨立產出（saas 單獨運作、不依賴 doc）。

這一步是「需求確認（saas）」到「需求文件化（doc）」的接點：saas 已產出 doc 需要的全部原料、此處只做格式移交、不重新訪談。

---

## 訪談互動原則

1. **問題總量不設限、節奏分輪推進**：每輪 3-5 題讓使用者好消化、但輪數沒有上限；覆蓋率優先於對話成本。發現使用者沒想清楚的操作、持續追問到能寫出行為情境為止。
2. **產品名攔截**：使用者開口指定產品時、先用一句話確認背後需求（「指定 MongoDB 是因為 schema 變動頻繁、還是團隊熟悉度？」）、需求確認後產品可以直接採納。
3. **每階段帶反向問**：使用者描述的是想要的功能、沒想到的東西藏在失敗面 — 「使用者做完馬上後悔怎麼辦」「這批資料外洩的代價」「凌晨三點誰起床」「Order 的表加欄位要通知誰」。反向問是「確認使用者沒想到的東西」的主要工具。
4. **底線告知協議**：防護底線逐項過、使用者可延後但要記錄；「先跳過、之後再說」轉寫成「延後 + 具體重評條件」、見 `references/baseline-protections.md`。
5. **行為情境是收斂條件**：任何功能爭論回到「使用者在什麼情境做什麼、預期看到什麼」收斂；情境寫得出來才進下一階段。
6. **訪談問句去重**：同一個風險在操作盤點風險表、核心問題、維度訪談各出現一次 — 這是宣告層的雙重核對設計、保留；訪談問句層要去重 — 語意重複的問句、後出現者改用「引用前答確認」句式（「操作盤點時提過重複扣款不可接受 — 佇列重試的情境下這仍成立嗎」）、不重新開放問同一題。

---

## 觸發路由

| 訊號                                                                                        | 讀哪份 reference                                                                                                            |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 使用者的需求看起來用託管平台 / BaaS 就能解決（電商、表單流程、內容站、app 後端）            | `references/interview-core.md`（定錨段的交付形態 gate）                                                                     |
| 產品是開源自架工具（開發者工具 / CLI 工具 / 自架服務、源碼公開）                            | `references/interview-core.md`（開源自架工具中間流程 + 開源替代品 check）                                                   |
| 開始盤點功能、使用者說「我要做一個 X 的服務」                                               | `references/user-operations-bdd.md`（操作盤點）                                                                             |
| 操作清單完成、產品有 UI 元件、要展開畫面狀態矩陣                                            | `references/user-operations-bdd.md`（Stage 1.5 畫面狀態矩陣展開）+ `references/principles/screen-state-matrix-expansion.md` |
| 操作清單完成、要切 domain / 定 event                                                        | `references/domain-event-modeling.md`（domain / event 切分）                                                                |
| 判斷一塊 domain / 維度該自建還是買、或候選 vendor 一次 cover 多維度（跨能力 bundle / BaaS） | `references/principles/capability-outsourcing-depth.md`（外包深度三分層）                                                   |
| 領域模型完成、要判讀技術需求                                                                | `references/interview-core.md`（定錨 + 核心問題）                                                                           |
| 正式狀態保存（帳號、訂單、合約、金流）                                                      | `references/dimensions/state-storage.md`（必）                                                                              |
| 任何對外服務                                                                                | `references/dimensions/deployment-platform.md`（必）+ `references/dimensions/security.md`（必）                             |
| 任何 production 服務                                                                        | `references/dimensions/observability.md`（必）+ `references/dimensions/reliability.md`（必）                                |
| 任何有可執行產出的專案（app / 網站 / 服務 / CLI）、要定實機驗證環境                         | `references/dimensions/verification-surface.md`（必）                                                                       |
| event catalog 有不可丟 event、或 request 外的可靠工作                                       | `references/dimensions/async-queue.md`                                                                                      |
| 同一資料高頻重複讀、昂貴計算共用、session / presence                                        | `references/dimensions/cache.md`                                                                                            |
| 產品有 client-side 元件（mobile app / SPA / desktop app）                                   | `references/dimensions/observability.md`（client-side 觸發展開段）+ `references/principles/client-side-observability.md`    |
| 明確高峰活動、成本敏感、規模假設首年破十萬用戶                                              | `references/dimensions/capacity-performance.md`                                                                             |
| 使用者問「之後長大怎麼辦」、或要寫 tripwire 總表                                            | `references/scale-stage-triggers.md`                                                                                        |
| 防護底線逐項確認、或使用者要求跳過某條底線                                                  | `references/baseline-protections.md`                                                                                        |
| 訪談收斂、要產出決策文件與 scaffold 建議                                                    | `references/decision-record-template.md`                                                                                    |
| 決策記錄產出後、專案有 doc skill、要移交需求文件                                            | `references/decision-record-template.md`（銜接 doc 系統節）                                                                 |

每份 reference 自包含：以該階段或維度為核心、把訪談問題、判斷標準、防護底線與 tripwire 收在同一檔。閱讀任一 reference 不需要回來看其他 reference。

---

## Success Criteria

| Metric | 定義                                                              | 目標 |
| ------ | ----------------------------------------------------------------- | ---- |
| **M1** | 從 SKILL.md 出發、完成一個階段或維度的訪談需要開幾個檔案          | ≤ 2  |
| **M2** | 隨機抽一份 reference、不讀其他 reference 能否獨立完成該段訪談     | 100% |
| **M3** | 決策記錄每項選型「理由 / 防護狀態 / tripwire」三欄齊備率          | 100% |
| **M4** | 操作清單中每個操作「行為情境 / 風險 / 引導 / 後端防護」四欄齊備率 | 100% |
| **M5** | event catalog 中每個跨 domain 協作都有對應 event 或公開查詢介面   | 100% |

---

## Directory Index

```text
saas-tech-selection/
├── SKILL.md                              # 本檔：核心支柱 + 訪談流程 + 觸發路由
└── references/
    ├── user-operations-bdd.md            # Stage 1：操作主體枚舉、行為情境寫法、誤操作風險、前端引導與後端防護成對
    ├── domain-event-modeling.md          # Stage 2：operation → command → domain → event、SRP 切分判斷標準、OCP 公開面 / 內部面
    ├── interview-core.md                 # 定錨 + 核心問題：問法、為什麼問、答案判讀路由
    ├── scale-stage-triggers.md           # 規模成長撞牆訊號 → 決策文件 tripwire 總表寫法
    ├── baseline-protections.md           # 跨維度防護底線清單 + 延後記錄協議
    ├── decision-record-template.md       # 設計決策記錄模板（操作風險表 / domain map / event catalog / 維度決策）+ scaffold 格式
    ├── principles/
    │   ├── capability-outsourcing-depth.md  # 外包深度三分層（managed 基礎設施 / feature SaaS / 跨能力 bundle）+ commodity domain / 接縫成本判讀
    │   ├── screen-state-matrix-expansion.md # Stage 1.5：操作清單 → 畫面狀態矩陣展開、退出路徑檢查、gate 三問
    │   ├── three-layer-test-strategy.md     # 三層測試策略（unit / protocol integration / screen state）、mock 遮蔽意識
    │   └── client-side-observability.md     # Client-side 觸發展開：四類事件分類、自架 vs 商業、SDK 設計
    └── dimensions/
        ├── state-storage.md              # 正式狀態與資料儲存：DB 類型、多租戶資料模型、migration / 備份底線
        ├── cache.md                      # 快取：何時需要、失效策略先行、不可當 source of truth
        ├── async-queue.md                # 非同步交接：event catalog 的執行層、idempotency 底線
        ├── observability.md              # 觀測底線：structured log、錯誤分類、alert 路由、PII 邊界
        ├── deployment-platform.md        # 部署與入口：PaaS / VM / container / k8s 進入條件、回滾底線
        ├── security.md                   # 身份、租戶隔離、secret、資料保護、audit、合規
        ├── reliability.md                # CI gate、測試層次、備份演練、第三方依賴降級
        ├── capacity-performance.md       # 容量假設、連線池、成本監控、高峰 readiness
        └── verification-surface.md       # 實機驗證環境：模擬器/實機、瀏覽器/URL、runtime/容器/入口層，答案固化為專案 verify 配方
```

---

**Last Updated**: 2026-08-08

版本紀錄在同目錄的 `CHANGELOG.md`。
