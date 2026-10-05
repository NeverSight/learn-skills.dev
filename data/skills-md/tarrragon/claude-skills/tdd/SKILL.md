---
name: tdd
description: "TDD 全流程指導工具。Use for: (1) 開始新功能的 TDD 流程（Phase 0-4）, (2) 推進到下一個 TDD 階段, (3) Phase 1 SOLID 原則驅動功能拆分分析, (4) 查看當前 TDD 進度和階段狀態, (5) 評估是否需要 Phase 4 重構以及 3b 拆分評估, (6) 需求文件（Spec/UC）銜接到測試流程, (7) 新專案起手的批量測試設計, (8) 紅燈測試存根策略（靜態語言編譯通過）, (9) 實作 Ticket 拆分邊界判讀（測試變綠驗收點）, (10) 測試↔UseCase 追溯矩陣。Use when: 開始新功能開發、進入任何 TDD Phase、需要 SOLID 拆分指導、需要確認當前所在 TDD 階段、需要做 Phase 4 豁免判斷時、從 spec/UC 開始寫測試、新專案批量測試規劃、紅燈測試編譯不過需要 stub、判斷 ticket 拆分粒度是否合理、確認測試是否覆蓋 UC 場景。Triggers: tdd, 測試, 紅燈, 綠燈, stub, 存根, 拆分粒度, 測試覆蓋, 追溯, traceability, spec 轉測試, UC 轉測試, 批量測試, 新專案測試, 測試變綠, Phase 0, Phase 1, Phase 2, Phase 3, Phase 4, 重構評估, outside-in, 外圈紅燈, on-device, 實機驗證, wip tag。"
metadata:
  version: 2.12.1
  portable: true

---

# /tdd - TDD 全流程指導工具

統一的 TDD 流程入口，涵蓋 Phase 0（架構審查）到 Phase 4（重構評估）的完整指導。

---

## 核心理念

TDD 的價值不只是「測試先寫」，而是**強迫你在實作前想清楚**：

- Phase 0：系統一致性確認（避免重複造輪子）
- Phase 1：功能設計和 SOLID 拆分（設計決策優於實作決策）
- Phase 2：行為規格化（Given-When-Then 驅動實作邊界）；有 runtime surface 的場景**外圈驗收紅燈先行**（on-device / 端對端先紅、單元後紅，outside-in 雙迴圈——詳見 `references/phase2/rules.md`「紅燈層級順序」節）
- Phase 3：實作執行（按規格不走彎路）
- Phase 4：品質反思（發現設計債務）

**粒度原則**：Use Case → 行為單元 → 測試 → 實作，每一層的拆分由上一層決定。單一 Ticket 目標 3-7 分鐘完成。詳見 `references/task-granularity-rules.md`。

**文件連貫性原則**：流程文件鏈（Proposal → Spec/UC → 種子包 → feature-spec → 測試 → traceability）每份文件分三級——活文件（期待最新、必須有機制守著）、scaffold（消費後即過期、要標記）、append-only 記錄（史料不回改）；漂移只發生在「被期待最新卻沒有機制」的錯配格。每類資訊指定唯一權威載體、其他位置引用不複製——行為的權威載體是測試（唯一改壞當下會發聲的載體）。各 Phase 驗收附連貫性檢查點（含 Phase 3/4 的註解判斷標準：先評有沒有解釋到商業邏輯、防護動機轉測試）。詳見 `references/document-coherence.md`。

**設計原則**：Layer 1 內容為通用 TDD 知識，任何專案均可直接使用。Layer 2 為框架整合點，以 blockquote 標記。

---

## 子命令總覽

| 子命令 | 用途 | 適用時機 |
|--------|------|---------|
| `/tdd start` | 開始新 TDD 流程 | 新功能需求進入開發 |
| `/tdd next` | 推進到下一個 Phase | 當前 Phase 完成後 |
| `/tdd split` | Phase 1 SOLID 拆分分析 | Phase 1 設計階段需要拆分功能 |
| `/tdd status` | 查看當前進度和階段 | 確認目前所在 Phase 和轉換條件 |
| `/tdd phase4-exempt` | 評估 Phase 4 豁免條件 | Phase 3b 完成後決定是否豁免 4a/4c |

---

## `/tdd start` - 開始新 TDD 流程

初始化一個新功能的 TDD 流程。

**執行前 Read**：`references/phase0/rules.md`

> **框架整合**：在 Ticket 的 `tdd_stage` 欄位記錄當前 Phase。遷移任務豁免標記跳過的 Phase。

> **Doc 產出物銜接**（條件式）：`/tdd start` 時偵測 doc 產出物路徑（`docs/spec/` + `docs/usecases/` + `docs/proposals/`，詳見 `references/doc-handoff.md`）。有則執行銜接流程，產出 TDD 輸入種子包（GWT 種子 + 功能規格種子 + 整合測試映射）作為 Phase 0/1 的預填輸入。無則走現有流程。

---

## `/tdd next` - 推進到下一個 Phase

在當前 Phase 完成後，確認轉換條件並推進。

**執行前 Read**：當前 Phase 對應的 `references/phase{N}/rules.md`（查看「轉換條件」章節）

> **框架整合**：使用 `scripts/phase_complete.py` 執行 Phase Contract 驗證，確認產出符合要求後執行 `/ticket track complete {id}` 標記完成。Phase 1/2/3a 由執行者自行 commit。

---

## `/tdd split` - Phase 1 SOLID 拆分分析

在 Phase 1 設計階段，使用 SOLID 原則分析功能需求，產出拆分建議。

**執行前 Read**：`references/phase1/rules.md`（「SOLID 拆分進階工具與範本」章節）

CLI 工具位於 `scripts/tdd-phase1-split.py`。

> **框架整合**：使用 `/ticket create --parent {parent_id}` 建立子 Ticket，以 `blockedBy` 標記依賴。

---

## `/tdd status` - 查看當前進度

確認目前所在 TDD 階段、完成情況、下一步行動。

---

## `/tdd phase4-exempt` - Phase 4 豁免評估

Phase 3b 完成後，評估是否符合 Phase 4 豁免條件（跳過 4a/4c，直接執行 4b）。

**執行前 Read**：`references/phase4/rules.md`（「Phase 4 豁免評估」章節）

> **框架整合**：Phase 4a 使用 `/parallel-evaluation B`，Phase 4c 使用 `/parallel-evaluation A`。

---

## 3b 拆分評估（Phase 3a 完成後強制執行）

Phase 3a 策略文件完成後，評估 Phase 3b 是否需要拆分為多個並行子任務。

**執行前 Read**：`references/phase3/rules.md`（「3b 拆分評估」章節）及 專案的 TDD 流程規則

> **框架整合**：拆分時建立子任務，指定修改檔案清單（`where.files`），確保無交集，並行派發。

---

## Layer 1 / Layer 2 設計原則

本 SKILL 的所有內容分為兩層，確保核心 TDD 知識可跨專案複用：

| 層次 | 內容 | 可攜性 |
|------|------|--------|
| Layer 1 | Phase 定義、階段轉換條件、SOLID 檢查、BDD/GWT、品質基準、豁免規則、任務類型豁免 | 通用，任何專案可直接使用 |
| Layer 2 | Ticket 系統、Agent 派發、Hook 自動化、決策樹路由、Commit 管理角色 | 本框架特定，以 blockquote (`>`) 標記 |

### Layer 1 禁止引用

**作用域是全部會被同步出去的內容**——`SKILL.md`、`references/` 底下每一份（含子目錄）、以及 `CHANGELOG.md`。這一條原本寫成「在 `references/phase{N}/rules.md` 的非 blockquote 區域」，而一次可攜性閘門掃描的 20 條違規裡有 18 條落在那個範圍之外，在字面規則下不算違規——**規則的作用域比它的意圖窄，寫下去之後就沒有人再審視它**。

在上述範圍的非 blockquote 區域，禁止出現：

| 禁止項 | 替代方式 |
|--------|---------|
| `/ticket` CLI（如 `/ticket create`） | 「任務系統」「狀態管理」 |
| 具體代理人名稱（lavender/parsley/sage 等） | 「設計者」「實作者」「測試者」 |
| 專案的 hook 系統 | 「驗證機制」「檢查點」 |
| `decision-tree` 路由 | 「階段轉換」「路由決策」 |
| `/parallel-evaluation` 工具 | 「多維度分析」「交叉審查」 |
| 本專案路徑（`.claude/`、`docs/`） | 「規則目錄」「工作目錄」 |
| Wave、Patch 概念 | 「執行批次」「版本」 |

### 三種合規的出路

上面那張表只給「改寫成中性名詞」一條路，而真的需要註明來源的人因此沒有合法選項，於是照寫路徑——**禁令沒有配合規出路時，違規是唯一做得到那件事的寫法**。三種出路各有判斷標準：

| 情形                                                   | 出路                                                              | 判斷標準                                                       |
| ------------------------------------------------------ | ----------------------------------------------------------------- | ---------------------------------------------------------- |
| 規則內容已經寫在句子裡，路徑只說它來自哪               | 行內標 `<!-- portability-allow: 理由 -->`                        | 把路徑整條刪掉，讀者還做得到這件事嗎——做得到就是出處引用 |
| 讀者必須打開那個檔才做得了判定（值、表格、清單不在句內） | 改寫成「該專案自訂」並說明歸屬，本框架的位置放進標記              | 那個值換一個專案會不會不同——會就不該寫死                 |
| 整段在描述本框架的基礎設施（檔名、schema、CLI 名稱）   | 移進 `references/project-integration/`，Layer 1 留語意並標記指過去 | 換一個專案這一段要重寫幾成——過半就移走                   |

`references/project-integration/` 不隨同步傳遞，由各專案自備；Layer 1 指向它的那一句要寫明這件事，讓消費端知道那個目錄是他們自己的。

`portability-allow` 寫在哪一行就只豁免那一行，而它同時關掉可攜性閘門與失連掃描兩道檢查，所以標記的理由要寫得讓後來的人判得出該不該信——**理由寫成類型標籤（「這是必要的」）等於關機鍵**。

### 自己查，不要等閘門擋

同步工具若有可攜性閘門，推送前用不執行的方式讀它一次，逐條看而不是只看有沒有通過：

```bash
echo n | skill-sync push tdd -m "x"   # 讀 [Portability] 段，n 讓它不會真的推出去
```

<!-- portability-allow: skill-sync 是本庫的同步工具，其餘專案換成自己的 -->

一次全庫盤點的結果：這條禁令寫在 SKILL.md 裡、每次叫用都會被讀到，而 20 條違規照樣長出來。**規則被讀到不等於規則被執行**，差的是一道會擋下來的檢查。

### Layer 2 整合點

Layer 2 內容以 blockquote 標記，提供本框架的具體實現方式：

| 整合點 | Layer 1 描述 | Layer 2 實現 |
|--------|-------------|-------------|
| 任務管理 | 「任務轉換條件」 | `/ticket track complete` |
| 角色派發 | 「Phase 1 由設計者執行」 | 「派發給 lavender-interface-designer」 |
| 自治提交 | 「完成後自行提交」 | `feat({id}): Phase X - {摘要}` |
| 多視角分析 | 「多維度交叉審查」 | `/parallel-evaluation` |

---

## 案例集

真實案例記錄 TDD 各階段踩過的坑，供設計和審查時參考：

| 案例 | 對應 Phase | 主要教訓 |
|------|-----------|---------|
| [跨模組共用策略缺失](references/cases/cross-module-shared-strategy-gaps.md) | Phase 1 | 規格未標注跨模組驗證重複、ID 碰撞、欄位映射缺失、零日誌 |
| [測試資料與可觀測性盲點](references/cases/test-data-and-observability-blind-spots.md) | Phase 2 | 測試資料殘留 v1 欄位碰巧通過、catch 區塊零日誌未測 |
| [印表機測試覆蓋深度不足](references/cases/printer-test-coverage-depth-failure.md) | Phase 2 | 28 個測試全過但 4 個 Bug 上線，路徑深度不足、try-catch 吞錯誤 |
| [並行實作重複與 Lint](references/cases/parallel-impl-duplication-and-lint.md) | Phase 3 | 並行 worktree 各自實作驗證框架、dead import、版本號硬編碼 |
| [多視角審查發現總結](references/cases/multi-perspective-review-findings-v0170.md) | Phase 4 | 完整審查報告：規格盲點 36%、測試盲點 27%、實作品質 36% |
| [Chrome Storage API 效能延遲](references/cases/storage-api-performance-latency.md) | Phase 1 | 規格應定義效能目標數值，批次參數屬規格範疇 |
| [批次寫入失敗處理策略](references/cases/storage-write-failure-handling.md) | Phase 1 | 回滾/孤立/預防中止三策略選擇，規格須定義失敗策略 |
| [私有方法測試覆蓋缺口](references/cases/private-method-test-coverage-gap.md) | Phase 2 | 合併邏輯和快取鍵的私有方法無獨立斷言，邊界條件未覆蓋 |
| [異常路徑測試覆蓋缺口](references/cases/error-path-test-coverage-gap.md) | Phase 2 | 180 錯誤碼中 49% 生產路徑未測，引用 != 測試 |
| [Phase 4 豁免判斷邊界](references/cases/phase4-exemption-doc-task.md) | Phase 4 | DOC 標籤不等於低風險，豁免條件應改為 AND 邏輯 |
| [SA 審查 Tag-based Book Model](references/cases/sa-review-tag-based-book-model.md) | Phase 0 | 跨 3 子域變更必須 Phase 0，重複實作只能在系統層級識別 |

---

## 相關資源

- 文件連貫性紀律（分級 / 住址 / 各 Phase 檢查點）：`references/document-coherence.md`
- Phase 2 測試設計時，若需要從規格推導「要測哪些對象」並定義每個對象的契約完整度，見 `references/test-object-catalogue.md`（doc-handoff 回答 spec→測試映射、layered-test-strategy 回答該層怎麼測，本檔回答要測哪些對象）
- TDD 流程規則：專案的 TDD 流程規則
- 任務拆分指南：專案的任務拆分指南
- 並行派發指南：專案的並行派發規則
- 認知負擔原則：專案的認知負擔規則

---

**Last Updated**: 2026-09-16

版本紀錄在同目錄的 `CHANGELOG.md`。
