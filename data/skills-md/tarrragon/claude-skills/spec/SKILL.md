---
name: spec
description: "需求完善度品質閘門。Use for: (1) Phase 1 開始時初始化功能規格骨架 (/spec init), (2) 驗證功能規格的需求完善度 (/spec validate), (3) 判斷需求是否足夠清晰可進入實作。Use when: Phase 1 功能設計代理人在進行功能設計時，作為內部工具使用。不是流程入口——/tdd 管流程編排，/spec 管產出物品質。"
metadata:
  portable: true
  version: 1.9.1

---

# /spec - 需求完善度品質閘門

把模糊需求展開成無歧義的行為契約。

---

## 定位與分工

| 工具 | 問的問題 | 階段 | 關係 |
|------|---------|------|------|
| /tdd | 「流程走到哪了？下一步做什麼？」 | Phase 0-4 全流程 | 流程編排器 |
| /spec | 「需求描述得夠不夠清楚？」 | Phase 1 內部 | 產出物品質工具 |
| SA | 「該不該做？和現有系統一致嗎？」 | Phase 0 | 架構守門人 |
| system-design | 「這一版要做哪些決定、哪些延後？」 | 寫規格之前 | 決定範圍與時機；/spec 檢查範圍內的需求寫得夠不夠清楚 |

**/spec 不是流程入口**：lavender 在 Phase 1 內部使用 /spec 產出功能規格。/tdd 不呼叫 /spec，/spec 不呼叫 /tdd。兩者完全解耦。

### 適用範圍限制（防誤用聲明）

`docs/spec/` 下 frontmatter 含 `subdomain: data-contract` 的文件（例：`docs/spec/balance-sheet/SPEC-002-accounts-snapshots-data-contract.md`）**不適用 `/spec validate`**。

| 項目 | /spec validate 假設的 schema | data-contract 文件實際 schema |
|------|------------------------------|-------------------------------|
| 章節結構 | Purpose / Scenarios / Acceptance（Lite）或 6 區段（Full） | 概述 + 可攜性邊界原則 + A 區（邏輯契約）/ B 區（實作綁定） |

**Why**：/spec validate 的 Layer 1 結構檢查針對 Purpose/Scenarios/Acceptance（或 Full 6 區段）比對區段標題，data-contract 文件遵循 `data-layer-contract-methodology.md` 的可攜性兩區（A/B）結構，兩套 schema 不相容。**Consequence**：對 data-contract 文件執行 `/spec validate` 會在 Layer 1 誤報「結構失敗」（找不到 Purpose/Scenarios/Acceptance 區段標題），該結果不反映文件真實品質，若被當真會誤導撰寫者修改成不必要的結構。**Action**：data-contract 文件的機械驗證改由 `doc validate` 子命令承接（`../doc/SKILL.md`， 落地前為人工依 `data-layer-contract-methodology.md` 檢查），禁止對其執行 `/spec validate`；已誤執行者，Layer 1「結構失敗」判定應忽略。<!-- portability-allow: 條件式引用，目標 skill 未必與本 skill 一同安裝 -->

---

## 子命令總覽

| 子命令 | 用途 | 適用時機 |
|--------|------|---------|
| `/spec init` | 初始化功能規格骨架 | Phase 1 開始，lavender 收到 Ticket 後 |
| `/spec validate` | 驗證需求完善度 | 規格撰寫完成後，進入 Phase 2 前 |

---

## `/spec init` - 初始化功能規格骨架

讀取 Ticket frontmatter，自動判斷模式，產出對應模板骨架。

### 輸入

- Ticket ID（必填）：從 frontmatter 讀取 type、where、priority 等欄位

### 模式判斷（自動）

```text
讀取 Ticket frontmatter
    |
    v
符合 Full 任一條件？
    |
    +-- 是 → Full 模式（6 區段）
    |
    +-- 否 → Lite 模式（3 區段）
```

**Full 模式觸發條件**（任一符合）：

| 條件 | 判斷依據 |
|------|---------|
| 新功能開發 | type == IMP 且 how.task_type == "新增" |
| 修改檔案多 | where.files > 5 |
| 明確指定 | 用戶執行 `/spec init --mode full` |

**Lite 模式**：不符合任何 Full 條件，或用戶執行 `/spec init --mode lite`。

### 輸出

- 功能規格骨架檔案：`{ticket-id}-feature-spec.md`
- 存放位置：Ticket 所在目錄（`docs/work-logs/v{version}/tickets/`）
- **Spec 文件即 Phase 1 設計文件**（同一檔案，非額外產物）

**生命週期（scaffold 文件）**：feature-spec 的消費者是 Phase 2 測試設計；Phase 3 綠燈後，行為的權威轉移到測試與程式碼，本文件頂部標記 `status: archived (superseded by tests)`、之後讀它是讀當時的設計快照。引用 domain spec 的內容用指涉（SPEC-ID + 章節）、不整段複寫——只有本 ticket 對 spec 的增量決策是這份文件的固有資訊。多份文件同時被期待最新必然漂移；本段的三個規定（archived 標記、指涉不複寫、增量決策才是固有資訊）已自足。同專案若也安裝 tdd skill，完整的文件分級與資訊住址原則見其 `references/document-coherence.md`——那是選讀的延伸、不是本段的前置依賴。

### Lite 模式骨架（3 區段）

```markdown
# {Ticket ID} 功能規格

## 1. Purpose（目的）
<!-- 用一句話回答：這個功能解決什麼問題？為誰解決？ -->

## 2. Scenarios（行為場景）
<!-- 用 GWT 格式描述每個行為場景 -->
### 場景 1: {場景名稱}
- **Given**: {前置條件}
- **When**: {觸發動作}
- **Then**: {預期結果}

## 3. Acceptance（驗收條件）
<!-- 可直接驗證的條件清單 -->
- [ ] {條件 1}
```

### Full 模式骨架（6 區段）

```markdown
# {Ticket ID} 功能規格

## 1. Purpose（目的）
<!-- 問題背景、目標用戶、核心價值 -->

## 2. API Signatures（介面定義）
<!-- 函式簽名、輸入輸出型別、回傳值語義 -->

## 3. GWT Scenarios（行為場景）
<!-- Given-When-Then 格式，含正常流程和異常流程 -->

## 4. Error Handling（錯誤處理）
<!-- 每個錯誤情境的處理策略和回傳值 -->

## 5. Dependencies（依賴）
<!-- 外部依賴、前置條件、環境假設 -->

## 6. Acceptance（驗收條件）
<!-- 可直接驗證的條件清單，含效能指標（如適用） -->
```

> 完整模板含填寫指引和範例：`references/spec-template-lite.md`、`references/spec-template-full.md`

---

## `/spec validate` - 驗證需求完善度

兩層驗證：結構檢查（機械性）+ AI 語義推演（深度分析）。

### 輸入

- Spec 文件路徑（必填）：`{ticket-id}-feature-spec.md`

### Layer 1：結構檢查（自動，秒級）

檢查模板區段的存在性和非空性。

| 模式 | 必須存在的區段 | 檢查內容 |
|------|--------------|---------|
| Lite | Purpose, Scenarios, Acceptance | 區段標題存在且內容非空 |
| Full | 全部 6 區段 | 區段標題存在且內容非空 |

**額外結構檢查**：

| 檢查項 | 規則 |
|--------|------|
| GWT 格式 | Scenarios 區段至少 1 個 Given-When-Then 完整三元組 |
| Acceptance 可驗證性 | 每個條件以 `- [ ]` 開頭 |
| Purpose 簡潔性 | 不超過 200 字（Lite）/ 500 字（Full） |
| API surface 完整性（Full only） | 每個 `### FR-XX:` 段落若提及 HTTP API 行為（`GET`/`POST`/`PUT`/`DELETE`/`endpoint`/`API 回`/`status code` 類訊號），須有對應 `/v1/...` endpoint 路徑定義；缺者列為提醒 |
| domain-map 覆蓋（規劃波 domain spec） | spec 每個 `### FR-XX:` 須在對應 domain map 的 FR→bundle 覆蓋表歸屬；domain map 缺失、或有未覆蓋 FR，列為提醒 |
| 事件流標定（可選，`--check-event-flow-labeling`） | spec 每個 `### FR-XX:` 段落若命中事件流訊號詞（清單見下，與 Layer 2 維度 5 共用同一份），須在 domain map「通道與協調圖」節之「到達類別與級別實例」子表找到對應 FR 引用；缺者列為提醒 |

**結構檢查失敗**：輸出缺失清單，不進入 Layer 2。

**API surface 完整性檢查**（動機：SPEC-014 FR-04 曾寫「analytics API 回 501」卻無 endpoint 路徑定義，缺口到派發實作才暴露）：以 `scripts/check_api_surface.py` 機械掃描每個 FR 段落，比對「描述 API 行為的訊號」與「同段落內是否已有對應主題的 `/v1/...` 路徑定義」。命令：

```bash
python3 .claude/skills/spec/scripts/check_api_surface.py {spec-file-path}  # portability-allow: consumer 共通安裝位置
```

輸出缺口清單（`[FR-XX] {行內容}`）或「檢核通過」；exit code 0 = 通過、1 = 有缺口。**性質為啟發式提醒**（依訊號詞比對，非語意理解），可能有少量誤判（如籠統的架構流程敘述），不構成強制阻擋，僅供撰寫者複核。

**domain-map 覆蓋檢核**（動機：domain map 曾漏覆蓋部分 FR，靠人工四視角審查才抓出）：驗證 version-bootstrap Step 2.5 產出的 domain map 是否覆蓋 spec 全部 FR。適用於規劃波的 domain spec（`docs/spec/{domain}/`），非 ticket 級 feature-spec。命令：

```bash
python3 .claude/skills/spec/scripts/check_domain_coverage.py {spec-file-path} [--domain-map {path}]  # portability-allow: consumer 共通安裝位置
```

domain map 定位：省略 `--domain-map` 時自動找 spec 同目錄 `domain-map.md`，退化找 `docs/domain-map.md`。輸出：domain map 缺失（提示先走 Step 2.5 產出）、未覆蓋 FR 清單（`FR-NN`，請於 domain map §7 補歸屬）、或「檢核通過」。exit code 0 = 通過、1 = 缺失或有未覆蓋 FR。FR token 展開支援逗號續列（`FR-01,02,03`）與範圍（`FR-13~17`）。

**事件流標定檢核**（可選，動機：Layer 2 維度 5「資源競爭」需要規格逐條標定事件流的到達類別與級別，靠 AI 語意判讀成本高，本檢核先以機械掃描做第一輪篩選）：以同一支 `check_domain_coverage.py` 加 `--check-event-flow-labeling` 執行，掃描 spec 每個 `### FR-XX:` 段落是否命中事件流訊號詞（`事件`、`通知`、`提示`、`背景`、`排程`、`佇列`、`推送`、`webhook`、`isolate`——與上方 Layer 2 維度 5 掃描說明共用同一份清單，程式碼側集中於 `check_domain_coverage.py` 的 `EVENT_FLOW_SIGNAL_WORDS` 常數，避免兩處各自維護而漂移）。命中的 FR 須在 domain map「通道與協調圖」節（**以標題文字定位，不依編號**——章節編號在既有專案可能已被其他內容佔用）之「到達類別與級別實例」子表找到對應 FR 引用，缺者列為提醒。命令：

```bash
python3 .claude/skills/spec/scripts/check_domain_coverage.py {spec-file-path} [--domain-map {path}] --check-event-flow-labeling  # portability-allow: consumer 共通安裝位置
```

輸出：命中訊號詞但未見通道標定的 FR 清單（`FR-NN`，請於「通道與協調圖」節之「到達類別與級別實例」子表補上標定），或「檢核通過」。**性質為啟發式提醒**（依訊號詞比對，非語意理解），不構成強制阻擋，僅供撰寫者複核；無事件流訊號的 spec 不受影響（與 Layer 2 維度 5 同形的條件式觸發）。

### Layer 2：AI 語義推演（深度，需思考）

沿 3 個核心維度掃描規格文件，找出**未被展開的需求假設**。每個維度產出一組「未回答問題」。Full 模式額外提示情境相關問題（不產出清單、不進入迭代）。

#### 掃描維度

| # | 維度 | 核心問題 | 適用模式 |
|---|------|---------|---------|
| 1 | 邊界完整性 | 極端值、空值、上限下限的行為定義了嗎？ | Lite + Full |
| 2 | 錯誤路徑 | 每個操作失敗時，系統如何回應？ | Lite + Full |
| 3a | 狀態轉換完整性 | 所有狀態和轉換都定義了嗎？有不可達狀態嗎？ | Lite + Full |
| 3b | 約束條件違反行為 | 每條約束條件的前提被違反時，行為定義了嗎？ | Lite + Full |
| 4 | 教學一致性 | spec 的設計決策是否與 blog 教學對應模組一致？ | Full only |
| 5 | 資源競爭 | 本功能發出或接收的每條事件流，到達類別（等待型／自發型／推送型，逐跳）與級別（不可棄／須留痕／可棄）標定了嗎？它與哪些既有事件流共用同一通道？通道進入卸載時，本功能的行為定義了嗎？ | Lite + Full（條件式，見下） |

**Lite 模式只掃描維度 1-3、5**，降低小型任務的認知負擔（維度 5 為條件式觸發，無事件流訊號時不計入）。**Full 模式額外掃描維度 4**。

#### 維度 4 教學一致性掃描說明（Full 模式）

比對 spec 設計決策與 blog 教學對應模組是否一致：

1. 從 spec 的 domain 定位對應教學模組（CLAUDE.md「教學模組對應表」）
2. 讀取 blog 對應章節
3. 逐項比對設計決策面向（API 路徑 / 資料模型 / response format / 行為語意 / 儲存架構）
4. 產出偏移清單

嚴重度：高（API 路徑/response format，影響 SDK 實作）、中（資料模型欄位）、低（行為策略，不影響介面契約）。教學缺口（spec 有但教學無）不算偏移，標記為缺口建議先在 blog 補完。

**降級條款（無教學模組對應表時）**：步驟 1 依賴專案 CLAUDE.md 存在「教學模組對應表」章節才能定位對應教學模組。**Why**：並非所有專案都維護 blog 教學內容（如本專案 flutter_balance），CLAUDE.md 無此表時維度 4 無源可比。**Consequence**：若強行執行，會因找不到對應章節而卡住或產出誤導性的空比對結果，且不應被計入 validate 失敗。**Action**：執行維度 4 前先確認專案 CLAUDE.md 是否含「教學模組對應表」章節；不存在時跳過維度 4，於 validate 輸出標註「維度 4 skipped：無教學模組對應表」，不得視為失敗（不計入未回答問題數、不阻擋迭代上限判定）。

#### 維度 5 資源競爭掃描說明（條件式觸發）

**觸發條件**：spec 內文含事件流訊號詞之一才掃描。訊號詞（一行列舉，供 Layer 1 腳本共用）：事件、通知、提示、背景、排程、佇列、推送、webhook、isolate。無訊號時跳過維度 5，於輸出標註「維度 5 skipped：無事件流訊號」，不計入未回答問題數、不阻擋迭代上限判定（與維度 4 降級條款同形）。

**Why**：現有維度 1-4 都不問「本功能發出或接收的事件流會與誰搶同一通道、卸載時本功能怎麼辦」。未在 spec 階段標定，到達類別與級別會在實作期由工程師憑印象補，違反〈事件流負載仲裁方法論〉〈級別〉一節「級別在邊界標定、仲裁器不推導」的原則。**Consequence**：級別標定延後到實作期，會使同一查詢在不同呼叫情境下被賦予不一致的級別（無業務脈絡可依），且卸載發生時本功能行為未定義，只能臨場決定。**Action**：spec 命中訊號詞時，逐條事件流回答：(1) 到達類別（等待型／自發型／推送型，逐跳判定）與級別（不可棄／須留痕／可棄）是否已標定；(2) 與哪些既有事件流共用同一通道；(3) 通道進入卸載狀態時本功能的行為（依〈讓步與卸載順序〉）是否已定義。三問的判斷標準定義見〈事件流負載仲裁方法論〉的〈到達類別〉、〈級別〉、〈讓步與卸載順序〉三節，本節不重述。

#### 情境相關提問（Full 模式額外提示）

Full 模式下，validate 完成維度 1-3 掃描後，**額外提示**以下問題供撰寫者自行考慮。這些不產出未回答問題清單，不進入迭代：

- **並發安全**：多個使用者/執行緒同時操作會怎樣？
- **效能約束**：資料量增長 10x/100x 時行為如何？有回應時間要求嗎？
- **安全性**：誰可以執行此操作？敏感資料如何保護？
- **依賴明確性**：外部依賴的契約是否明確？依賴不可用時的降級策略？

#### 語義推演輸出格式

```markdown
## /spec validate 結果

### 結構檢查：通過/未通過
{缺失清單，如有}

### 語義推演：{N} 個未回答問題

#### 維度 1: 邊界完整性
- Q1: 當 {參數} 為空值時，預期行為是什麼？
- Q2: {集合} 的上限是多少？超過上限時如何處理？

#### 維度 2: 錯誤路徑
- Q3: {操作} 失敗時，是否需要回滾已完成的步驟？

#### 維度 3a: 狀態轉換完整性
（無未回答問題）

#### 維度 3b: 約束條件違反行為
對「約束條件」區段每一條，三問法掃描：
1. 約束的前提是什麼？（例：「init 呼叫一次」→ 前提 = 只能呼叫一次）
2. 前提被違反時（第二次呼叫 init），行為定義了嗎？
3. 約束覆蓋部分 API 時，同類別未列舉的 API 是否也需定義？

#### 維度 4: 教學一致性（Full 模式）

CLAUDE.md 有「教學模組對應表」時：

| 偏移面向 | Spec 值 | 教學值 | 嚴重度 |
|---------|---------|--------|--------|
| {面向} | {spec 描述} | {教學描述} | 高/中/低 |

教學缺口（spec 有定義但教學未涵蓋）：
- {設計決策描述} → 建議先在 blog 補完

CLAUDE.md 無「教學模組對應表」時（降級條款，見上）：

```text
維度 4 skipped：無教學模組對應表
```

#### 維度 5: 資源競爭（條件式，見上）

spec 含事件流訊號詞時：
- Q4: {事件流名稱} 的到達類別（等待型／自發型／推送型）與級別（不可棄／須留痕／可棄）標定了嗎？
- Q5: {事件流名稱} 與哪些既有事件流共用同一通道？通道進入卸載時，本功能的行為定義了嗎？

無事件流訊號時：

```text
維度 5 skipped：無事件流訊號
```

### 建議
- 必須回答：Q1, Q3（影響 GWT 設計）
- 建議回答：Q2（影響效能設計）
- 教學偏移（高）：必須對齊後再進入 Phase 2
- 教學缺口：建議先補教學再落實 spec
- 可延後：無
```

---

## 迭代機制

/spec validate 可多次執行。回答問題後再次 validate，直到無新問題或達上限。

### 迭代上限（安全閥）

| 模式 | 上限 | 理由 |
|------|------|------|
| Lite | 2 次 | 小型任務不應花費過多時間在規格上 |
| Full | 3 次 | 第 3 次仍有大量問題表示需求本身不成熟，應升級 PM |

達上限時輸出警告，剩餘問題標記為 Phase 2 待解決。

---

## 使用流程

Phase 1 中 lavender 如何使用 /spec 的完整流程，詳見該代理人定義的「/spec 工具整合」章節。

/spec 只負責「發現問題」（產出骨架和未回答問題清單），不負責「解決問題」（由 lavender 決定如何回答和組織）。

---

## 相關文件

- `../tdd/SKILL.md` - TDD 流程工具（流程編排；同專案若也安裝 tdd）
- Phase 1 功能設計代理人的定義 - /spec 的使用者（各專案自有）
- 專案的 TDD 流程定義文件
- references/spec-template-lite.md - Lite 模板（3 區段）
- references/spec-template-full.md - Full 模板（6 區段）
- `data-layer-contract-methodology` - data-contract 文件的 A/B 兩區結構定義（`/spec validate` 不適用對象）
- `../doc/SKILL.md` - data-contract 文件機械驗證的承接者（`doc validate`）<!-- portability-allow: 條件式引用，目標 skill 未必與本 skill 一同安裝 -->
- `事件流負載仲裁方法論` - 維度 5「資源競爭」的判斷標準來源（〈到達類別〉〈級別〉〈讓步與卸載順序〉三節）<!-- portability-allow: 條件式引用，目標方法論未必與本 skill 一同安裝 -->

---

版本紀錄在同目錄的 `CHANGELOG.md`。
