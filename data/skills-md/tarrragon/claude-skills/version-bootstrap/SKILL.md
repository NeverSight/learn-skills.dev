---
name: version-bootstrap
description: "版本規劃波 orchestrator：把版本提案展開成可執行的 ticket，中間不漏教學比對。依序走提案清單與依賴檢查、spec、domain map、資料契約、教學比對、UC、地基波（僅 UI 版本）、紅燈測試、匯總建票；每步有 checkpoint，PM 確認才前進。觸發詞：規劃波、版本啟動、bootstrap、提案展開、建票、地基波。Do NOT use for 決定票屬於哪一版（用 version-sequencing）或地基逐維度盤點（用 foundation-design）。"
metadata:
  version: 1.7.6
  category: engineering-workflow
---

# /version-bootstrap — 版本規劃波 Orchestrator

把版本提案展開成可執行的 ticket，中間不漏教學比對。

---

## 全程

九步，由上而下。編號帶小數的是後來插入既有序列之間的步驟，**不是選配**——除了標「僅 UI」者之外每一步都要跑。

| 步 | 做什麼 | 產出 | 適用 |
|----|--------|------|------|
| 1 | 列出提案清單、跑跨提案依賴檢查 | 提案 ID／標題／狀態表 | 全部 |
| 2 | 建 spec 骨架、填 FR；UI 類提案過三項前置檢查 | spec 檔、UI 前置齊備 | 全部 |
| 2.5 | Domain 規劃 | 每個 domain 一份 domain map | 全部 |
| 2.6 | 資料契約產出（兩旗標皆否時合法跳過文件） | 資料契約文件或跳過理由 | 全部 |
| 3 | 教學比對 | 維度 4 無高嚴重度偏移 | 全部 |
| 4 | 建 UC + traceability | UC 場景、映射無 TODO | 全部 |
| 4.5 | 地基波：i18n → design-system → UX 審查 → 元件契約 → 元件庫 | 五塊各自的實作票與依賴 | **僅含 UI 提案的版本** |
| 5 | 紅燈測試設計（5a 外圈、5b 內圈） | 紅燈測試規格 | 全部 |
| 6 | 匯總建票 | W2／W3 實作票、W4 驗收票 | 全部 |

**一條分支不在上表**：決定把某個提案移到別的版本時，走〈按需讀取〉的移版 SOP，跑完回到原本那一步。

## 按需讀取

正文走得完九步。下表是走到特定情況才需要的依據。

| 什麼時候讀 | 檔案 | 涵蓋 |
|-----------|------|------|
| 決定把某個提案移到別的版本（不論理由，含 Step 1 依賴檢查報 `[WARNING]`） | `references/version-shift-sop.md` | 契約掃描、契約鎖定點確認、硬耦合分級、定形票建立、教學比對、交叉標記六步；契約檔案界定三問；硬耦合三類判斷準則 |
| Step 2／4.5／5／6 的判準允許分歧、需要具體範例校準（UI 類判別、三項前置的「存在」判準、地基波依賴編排、兩軸測試交集去重、GREEN 票粒度、並行安全的共用檔案） | `examples/v02-walkthrough.md` | 對應步驟段落的三段鏈式範例（【輸入】【產出】【驗證】），全篇亦可作為九步流程的假想演練 |
| 不確定某件事該由本 skill 還是相鄰資產（`foundation-design`／`version-sequencing`／`ux-design-evaluation`／`component-contract-design`／`dart-style-guardian`）處理 | `references/adjacent-assets-boundary.md` | 被本 skill 呼叫的工具清單；與本 skill 對接的規劃層 skill 交界表 |
| 規劃波過程中發生非 pipeline 內工作（既有測試回歸／Spec 約束邊界發現／流程改善發現） | `references/reactive-work.md` | 三類反應式工作的處理方式對照表 |

---

## 使用方式

```
/version-bootstrap --version <version>
```

**整條 pipeline 不會自己跑完。** 每一步結束都有 checkpoint，PM 確認後才進下一步——這對九個步驟一律成立，沒有例外。

各步標題括號裡的標籤講的是另一件事：**這一步需不需要 PM 填內容**。「無需人工填內容」指跑完指令就有產出，PM 只需在 checkpoint 確認；「需人工填內容」指指令只產骨架，內容要 PM 自己寫。兩個標籤都不影響 checkpoint——**沒有任何一步會自動進入下一步**。

---

## 各步驟細節

### Step 1：列出提案清單（無需人工填內容）

**動作**：讀取 `docs/todolist.yaml` 中指定版本的 `proposals` 欄位，列出提案清單和摘要。

```bash
doc list proposals  # 確認提案狀態
```

**輸出**：提案 ID + 標題 + 狀態表格。

**跨提案依賴檢查（強制）**：接著執行依賴檢查腳本，偵測「本版提案依賴的提案排在更晚版本」的排序矛盾。

```bash
uv run .claude/skills/version-bootstrap/scripts/check_proposal_dependencies.py --version <version>
```

腳本讀 `docs/proposals-tracking.yaml` 各提案的 `depends_on` 欄位（選填，list of str，元素為本提案依賴的前置提案 id）比對 `target_version` 排序。欄位格式權威來源（含專案未採用 doc skill 時的腳本行為）與此檢查為何在 Step 1 就位的動機案例，見 `references/step-rationale.md`〈Step 1：跨提案依賴檢查腳本〉。輸出 `[WARNING]` 時，PM 必須在本 Checkpoint 前二擇一處理：(1) 把依賴提案移入本版或更早版本一起排入，(2) 把本提案移至依賴提案完成之後的版本。

**選 (2) 移版時不得整包搬走**：提案在本版可能已留下 schema／DDL／契約級的殘留耦合，必須先盤點並在本版定形，否則兩個提案沒有真正解耦。六步盤點程序見 `references/version-shift-sop.md`。

**Checkpoint**：PM 確認版本範圍——哪些提案納入本版、哪些延後；依賴檢查腳本無 `[WARNING]` 輸出，或警告已處理（移版且已跑完移版 SOP／補前置）。

---

### Step 2：建 Spec 骨架（需人工填內容）

**動作**：用 `/doc batch-init` 批量建立 spec 骨架。

```bash
doc batch-init --proposals PROP-XXX,PROP-YYY --domain <domain>
```

**輸出**：每個提案對應 1 份 spec 骨架檔案。

**PM 工作**：填寫每份 spec 的 FR 列表、介面定義、約束條件。這是規劃波最耗時的人工步驟。

**UI 類判別**：依 FR 產物在哪裡被使用者看到或操作來判定，不以字面關鍵字為準。「畫面」「頁面」「元件」「介面」「UI」只是常見寫法，其涵蓋範圍由下表的呈現通道決定。FR 未寫明呈現通道時，先補寫通道再判定，不以猜測歸類。

| 呈現通道 | 判定 | 動作 |
|---|---|---|
| 圖形介面：由本應用程式渲染的視窗、頁面、彈窗、疊層、應用內提示，含唯讀畫面 | UI 類 | 過下列三項前置檢查 |
| 非圖形的人讀呈現：終端文字輸出與終端互動、匯出文件版面（優先本列）、由作業系統或宿主程式渲染的通知 | 非 UI 類，不過三項前置 | Checkpoint 記錄該提案的呈現通道，交 `foundation-design` UI 維度判改寫產物；不得只記「非 UI 類」 |
| 無人直接觀看：API 回應、供機器讀取的資料格式 | 非 UI 類 | 略過 |

**UI 類提案元件庫前置檢查（強制）**：判為 UI 類者須先確認下列**三項**存在，缺則先補齊才可繼續本提案的 UI 實作票規劃。為什麼這道閘門擋在這裡、為何以通道而非字面判定見 `references/step-rationale.md`〈Step 2 的 UI 前置檢查〉：

| 檢查項 | 對應載體 | 缺失時動作 |
|--------|---------|-----------|
| design token 層 | 專案 design-system 樣式檔（顏色/間距/字體/圓角/陰影參數集中管理） | 先建立 design token 層 |
| L3 元件庫章節 | spec 文件的元件庫章節；僅元件清單 + 原生元件禁用對照表 + 豁免清單三項屬本步驟範圍，契約欄位表與容器條目於 Step 4.5 補齊 | 先建立或補齊 L3 元件庫章節（用 doc skill `component-library-spec-template`） |
| design-system spec 文件 | 用 doc skill `design-system-spec-template` 產出的 design system 專屬 spec（如 `docs/spec/design-system-spec.md`），非混入一般功能 spec | 用 design-system-spec-template 補產 |

判準與分層依據（L1/L2/L3 分層、狀態綁定判準、流程整合點）見 `.claude/methodologies/component-library-bidirectional-constraint-methodology.md`。非 UI 類提案略過本檢查。

**Checkpoint**：所有 spec FR 填寫完成；UI 類提案已完成元件庫前置檢查（design token 層、L3 元件庫章節、design-system spec 三者存在或已補齊），非 UI 類提案略過本項；第二類（非圖形的人讀呈現）提案已記錄呈現通道並交 foundation-design。

---

### Step 2.5：Domain 規劃（需人工填內容）

**時機**：spec FR 填完後、測試設計前。為什麼這一步不能省見 `references/step-rationale.md`〈Step 2.5〉。

**動作**：用 doc skill 的 domain-map-template 為每個 domain 產出 domain map（多 domain 專案放 domain 子目錄，單 domain 專案放 `docs/` 根層）：

```bash
# 多 domain 專案：放對應 domain 子目錄
cp .claude/skills/doc/templates/domain-map-template.md docs/spec/{domain}/domain-map.md
# 單 domain 專案：放 docs/ 根層
cp .claude/skills/doc/templates/domain-map-template.md docs/domain-map.md
```

**PM 工作**：依模板從 spec FR 反推 bundle 邊界（切分判準見 `.claude/methodologies/domain-bundle-mapping-methodology.md`）——界定 aggregate / kernel / read-model 分類、依賴方向 DAG（**用實際 import 鏈驗證，不憑心智模型宣告**——如 `grep -rn "import.*<lower_layer>" lib/<domain_dir>/` 或 codegraph callers，確認 import 集合不含被禁層）、每 bundle 的目標路徑與測試層、FR→bundle 全覆蓋表。

**產出或更新語意**：saas 起手的版本，saas Stage 1/2 的 DDD 切分已餵入 domain map 的產出端，本步驟將其精修為層/依賴/測試 map；非 saas 起手（提案 / handoff 起手）則從模板新建。此語意消除「domain 規劃綁死 saas 起手」——標準化為所有規劃波的通用步驟。

**被誰消費**：Step 5 測試設計依 domain map 逐 bundle 決定測試層（domain unit / data repository / presentation widget）；Step 6 建票依 domain / data / presentation 分層切分。

**Checkpoint**：每個 domain 有 domain map；依賴方向底線經 import 鏈驗證；spec 全部 FR 在 FR→bundle 覆蓋表有歸屬（含標為非 domain 的 presentation / data FR）。

---

### Step 2.6：資料契約產出（需人工填內容）

**時機**：spec FR 與 domain map 完成後、紅燈測試設計前。為什麼這一步不能省見 `references/step-rationale.md`〈Step 2.6〉。

**動作**：先依 `.claude/methodologies/data-layer-contract-methodology.md` 第 2 節兩正交旗標（契約文件 / migration 治理）判定（本步驟不複寫判準內容，僅引用）。**兩旗標皆否時，僅維持 schema 約束 + DDL 註解即為合法終態，本步驟到此結束**（合法跳過文件產出，非偷懶）。任一旗標為要時，cp 模板產出：

```bash
# 沿用 SPEC-NNN 編號體系，subdomain 固定為 data-contract
cp .claude/skills/doc/templates/data-contract-template.md docs/spec/{domain}/{name}-data-contract.md
```

**消費來源**：spec FR 列表（欄位語意/值域）+ domain map data 層（§3 Bundle 界定表 Infrastructure/data 列的「資料契約文件引用連結」欄）。

**PM 工作**：依模板填寫 A 區（邏輯契約，DB-agnostic）與 B 區（實作綁定，DB-specific），完成後執行 `doc query <SPEC-ID>` 做 doc CLI 驗證——確認 frontmatter 有效、文件可被查詢發現。

**被誰消費（feed Step 5）**：每條契約條目（不變式/欄位語意/邊界行為）登錄至 `docs/traceability.yaml` 第三軸 `data_contract_tests`；Step 5 派發 sage 時一併帶入此軸，供測試設計逐條盤點覆蓋缺口，避免資料層規則只靠「剛好被某測試涵蓋」被動覆蓋。

**Checkpoint**：兩旗標已判定並記錄理由（含合法跳過情形）；旗標=要時，資料契約文件已產出且 `doc query` 查詢成功；`traceability.yaml` 第三軸 `data_contract_tests` 已初始化，每條契約條目的 `contract_ref`／`description`（schema 必要欄位）皆已填齊。`tests` 依 `tracking_schema.py` 的 `data_contract_entry_optional` 屬選填欄位，測試設計要到 Step 5 才進行，本步驟合法留空，不視為 TODO 佔位——測試對應是否補齊的判準移至 Step 5 Checkpoint。

---

### Step 3：教學比對（需人工填內容）

**動作**：對每份完成的 spec 執行 `/spec validate`（Full 模式，含維度 4 教學一致性）。

**前置**：確認 CLAUDE.md 是否含「教學模組對應表」章節。
- 有此表且列出對應模組 → 依下方 PM 工作處理維度 4 掃描結果
- 無此表（專案未採用教學對應慣例，或本版無 blog 教學內容）→ `/spec validate` 依其既有降級條款（`spec` skill〈維度 4 教學一致性掃描說明〉）自動跳過維度 4，輸出「維度 4 skipped：無教學模組對應表」，不計入失敗；本步驟以該輸出作為 Checkpoint 通過依據，不需額外處理

**PM 工作**（CLAUDE.md 有教學模組對應表時）：
- 偏移（高/中）：對齊教學設計或先在 blog 補完
- 教學缺口：在 blog 對應模組補完後再回來；無法立即補完時登記到 `docs/sync-pending.md`（`teaching-sync` skill 維護的 SOT，見該 skill〈sync-pending 是 SOT〉），標記優先級（P0/P1/P2），不以口頭記憶取代

**Checkpoint**：CLAUDE.md 有教學模組對應表時，維度 4 無高嚴重度偏移，教學缺口已處理或已登記於 `docs/sync-pending.md`；CLAUDE.md 無教學模組對應表時，`/spec validate` 已輸出「維度 4 skipped：無教學模組對應表」。

---

### Step 4：建 UC + traceability（需人工填內容）

**動作**：Step 2 的 `batch-init` 已同時建立 UC 骨架和 traceability 映射佔位。

**PM 工作**：填寫每份 UC 的 GWT 場景、更新 traceability 映射（spec FR → UC scenario）。

**Checkpoint**：所有 UC 場景填寫完成，traceability 映射無 TODO 佔位。

---

### Step 4.5：地基波（需人工填內容；僅含 UI 提案的版本）

**時機**：含 UI 提案的版本，於測試設計前。為什麼這一步不能省見 `references/step-rationale.md`〈Step 4.5〉。

**動作**：依 `.claude/methodologies/component-library-bidirectional-constraint-methodology.md`〈地基波 build 順序〉為權威（與 Step 2 UI 前置檢查同一份方法論），編排四塊地基實作，外加一個介於第 3 塊與第 4 塊之間、不計入四塊的元件契約銜接步驟：

| 順序 | 地基塊／銜接步驟 | 產出 |
|------|--------|------|
| 1 | i18n 系統 | 多語系資源檔 + 產生器（元件文字取 i18n key，測試可驗 zh/en overflow） |
| 2 | design-system 實作 | design token 集中檔（消費 Step 2 的 design-system spec） |
| 3 | UX 審查 | 每個互動元件的反應/動畫/提示 + 頁面跳轉/退出/生命週期完整性審查（產出反應規格供元件庫與測試點） |
| 3.5（銜接，不計入四塊） | 元件契約 | L3 元件庫章節補齊逐元件元件契約欄位表與容器條目（程序見 `component-contract-design` skill，判準見方法論〈元件契約判準〉）；checkpoint 為該 skill 的〈契約齊全的定義〉 |
| 4 | 元件庫實作 | 集中元件庫（套 token + i18n + UX 反應，依契約實作），barrel 匯出 |

**PM 工作**：為四塊各建實作票，另為元件契約銜接步驟建 DOC 票——唯 i18n 與 design-system 可並行，其餘依順序表預設相依（UX 審查因此以兩者為 `blockedBy`）；元件契約依賴 UX 審查，經此鏈已含 i18n／design-system（見 `references/step-rationale.md`〈元件契約遞移依賴〉）；元件庫依賴前三塊與元件契約為 `blockedBy`。順序與依賴依方法論〈地基波 build 順序〉，本 skill 不重複判準只做 orchestration。

**Checkpoint**：UI 版本的 i18n / design-system / UX 審查 / 元件庫四塊實作完成並測試綠（元件契約銜接步驟以 `component-contract-design` skill 的〈契約齊全的定義〉為完成判準，是元件庫實作的前置條件）；非 UI 版本略過本步驟（比照 Step 2 UI 判別）。

---

### Step 5：紅燈測試設計（需人工填內容；可並行）

**動作**：對每份 spec 派發 sage-test-architect 做 Phase 2 紅燈測試設計，依紅燈層級順序分兩段產出：

- **5a 外圈驗收紅燈（先）**：對 `runtime_surface: yes` 的 UC 場景產出整合層測試描述，含 on-device / 端對端層級；外圈定義「什麼叫做完」，以 wip tag 與 gate 隔離。`runtime_surface: no` 的場景豁免本段（豁免判準見權威節，此處不複寫）。
- **5b 內圈單元紅燈（後）**：規格分解的單元測試設計，驅動實作紅綠循環。

順序規則、豁免判準與 wip tag 共存機制的權威定義見 `/tdd` skill `references/phase2/rules.md`「紅燈層級順序」節，此處不複寫。

多 spec 可並行派發（每個 spec 1 張子票）。派發時使用 `/tdd` Phase 2 流程，sage 產出紅燈測試規格（5a + 5b 兩段皆屬同一 Phase 2 產出）。

**消費 Step 2.5 domain map（兩軸測試設計）**：

1. **層軸**：依 domain map 逐 bundle 決定測試層——domain bundle 走純函式 unit test、data 走 repository test、presentation 走 widget test（分層測試策略見 `.claude/methodologies/hybrid-testing-strategy-methodology.md`）。
2. **不變式軸**：依 domain map 的「Bundle 不變式清單」節逐 bundle 列舉 domain 行為不變式測試（例：某項缺漏沿用前值、比率分母為 0 的定義值、依賴方向不成環等**各專案自己的** domain 不變式），**與 UC 場景測試並存去重**——UC 場景測試涵蓋垂直使用者行為，不變式測試涵蓋水平 domain 規則，兩軸交集去重、聯集為完整覆蓋。避免 domain 規則只靠「剛好出現於某 UC 場景」被動覆蓋。

> sage 派發 prompt 應同時帶 spec FR / UC 場景（既有）與 domain map 的 bundle 不變式清單（新增），使兩軸都被系統列舉。traceability 的 domain-bundle→test 軸（見下）記錄不變式軸覆蓋。

**PM 工作**：驗收 sage 產出——確認 FR↔AC 覆蓋矩陣（Q12）無空行。

**Checkpoint**：所有 spec 的 Phase 2 完成，紅燈測試規格已提交；`traceability.yaml` 第三軸 `data_contract_tests` 每條契約條目已補上 `tests` 或標記 `no_test_needed`＋`reason`，不留缺口（Step 2.6 合法留空的欄位在此軸收斂）。

---

### Step 6：匯總建票（需人工填內容）

**動作**：根據 Step 2-5 的產出，建立 W2/W3/W4 的 IMP ticket。

- W2/W3：GREEN 實作票（每個 spec FR 或功能模組 1 張，分組依據見 `references/step-rationale.md`〈GREEN 票分組依據〉）
- W4：驗收票（E2E + Phase 4）

**建票來源**：
- spec FR 列表 → IMP ticket
- Phase 2 紅燈規格 → 確認 ticket 粒度（每張 ticket 的紅燈數）
- UC 場景 → 整合測試 ticket
- domain map bundle 分層 → 按 domain / data / presentation 切分實作票，並依 domain map §5「對實作票切分指引」對齊各票的層歸屬與依賴方向底線

**PM 工作**：確認 Wave 分配、並行安全（共用檔案需整合票，歸屬後其餘票不得直接修改，見 `.claude/pm-rules/task-splitting.md`〈拆分後檢查清單〉B 檔案所有權）。

**Checkpoint**：所有 ticket 建立完成，Wave 分配確認。

---

規劃波過程中可能發生但不屬於 bootstrap pipeline 的反應式工作，見〈按需讀取〉`references/reactive-work.md`。

---

版本紀錄在同目錄的 `CHANGELOG.md`。
