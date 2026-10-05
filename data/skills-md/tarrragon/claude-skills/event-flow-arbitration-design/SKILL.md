---
name: event-flow-arbitration-design
description: "落實事件流負載仲裁方法論的執行流程、訪談問題、套用範例與產出物範本（通道清單表、九格卸載順序表）。方法論管判準，本 skill 管怎麼問、怎麼套、產出長什麼樣。Use when: 事件流仲裁、負載仲裁、load shedding、卸載順序、backpressure、通道清單、九格表、isolate 仲裁、worker pool 競爭、connection pool 競爭、佔用量閾值設計、到達類別標定、級別標定時。"
metadata:
  version: 1.2.0
---

# Event Flow Arbitration Design

把《事件流負載仲裁方法論》的判準轉成可執行的訪談流程與各步的產出物範本。

## 定位（與方法論的分工）

| 載體 | 管什麼 |
|------|-------|
| 事件流負載仲裁方法論 | 判準——每條規則附「它回答的問題」與「為何這樣定」 |
| 本 skill | 流程——怎麼問、怎麼套用到具體系統、產出物長什麼樣 |

本 skill 不重述方法論的判準本身，只在 `references/templates.md` 的欄位名上與其保持一致。

## 觸發條件

以下情境出現任一項即觸發：

- 系統中有多個事件流競爭同一個稀缺通道（DB 連線池、worker pool、單一 isolate 事件迴圈、訊息佇列 partition、使用者注意力載體）
- 已完成 `saas-tech-selection` 的 async-queue／capacity-performance／observability 維度訪談，發現有「不可丟」或「須留痕」的 event，需要決定它與其他事件流在同一通道上的取捨順序
- 使用者提到：backpressure、load shedding、卸載順序、通道競爭、佔用量閾值、isolate 仲裁、connection pool 打滿、訊息混流不同級別

## 執行流程

各步逐一對應方法論〈執行步驟〉的清單，步數以該清單為準；每步的訪談問題在 `references/interview-questions.md`、產出物範本在 `references/templates.md`。

| 步驟 | 要做的事 | 對應方法論章節 | 產出物 |
|------|---------|--------------|-------|
| 1. 列通道 | 找出每個「一次只能服務有限請求」的資源，確認真持有者與仲裁器落點；並記下哪些 domain 會對同一通道發出請求 | 〈通道與仲裁器〉 | 通道清單表、協調圖 |
| 2. 標類別與級別 | 對每條事件流的每種觸發路徑逐跳標到達類別；級別在邊界或發起點標定 | 〈到達類別〉〈級別〉 | 到達類別與級別標定表 |
| 3. 定佔用量 | 選佔用量單位，兩種計法（請求數／資源單位）給出不同裁決時分池；定進入與離開卸載的兩個閾值 | 〈競爭與佔用量〉〈資源成本異質〉 | 佔用量與卸載閾值表 |
| 4. 填卸載順序表 | 九格（到達類別 × 級別）各填動作；推送型定緩衝上限，不可棄的推送型定持久佇列 | 〈讓步與卸載順序〉 | 九格卸載順序表 |
| 5. 定 deadline 來源 | 三類到達類別各自的 deadline 來源與逾期動作；自發型分狀態驅動與窗口驅動 | 〈Deadline 傳播〉 | Deadline 來源表 |
| 6. 定可觀測事件與最小指標集 | 定義仲裁決策事件的欄位、留痕粒度與載體、告警綁定的狀態變遷 | 〈可觀測性〉 | 可觀測事件欄位範本 |

**執行順序不可跳步**：第 4 步依賴第 2、3 步的分類與閾值結果，第 6 步的指標欄位（佔用量分解、卸載計數）依賴第 1-4 步已定義的通道與級別。訪談時仍可按需求先問使用者熟悉的部分，但填範本時依此順序回填。

## 與既有骨架範本的分工

| 載體 | 管什麼 | 與本 skill 的介面 |
|------|-------|------------------|
| `saas-tech-selection` 的 async-queue／capacity-performance／observability 維度 | 機制選型（用什麼佇列送）、容量假設與高峰 readiness、訊號源的 day-one 底線 | 這些維度訪談發現「不可丟」事件或「同一佇列混流不同級別」時，路由到本 skill 做仲裁設計；本 skill 的容量失敗訊號（不可棄請求無法服務）路由回 capacity-performance 的 tripwire 表 |
| `foundation-design` | 地基波的整體定位與各維度權威指名 | 本 skill 是其事件流仲裁維度的執行入口，不重複 foundation-design 的路由邏輯 |
| `doc` 的 domain-map 範本（`.claude/skills/doc/templates/domain-map-template.md` 的通道與協調圖節） | domain 邊界與依賴方向；該節是協調圖的結構載體 | 依賴方向描述資料流向；方法論〈通道與仲裁器〉的協調圖與之正交（互不呼叫的兩個 domain 仍可能競爭同一通道），兩者不互相取代。判準的權威在方法論，DAG 的權威在 `domain-bundle-mapping-methodology.md`，本表只說分工 |

## 何時讀哪份 reference

| 情境 | 讀 | 涵蓋內容 |
|------|-----|---------|
| 執行〈執行流程〉任一步的訪談，需要具體問句 | `references/interview-questions.md` | 各步數題，每題附「為什麼問」 |
| 需要參考已套用過的案例，理解判準如何落地到具體系統 | `references/worked-examples.md` | 三個場景（HTTP API 共用連線池、多 isolate 應用程式、訊息消費者混流），各含套用結果、易誤套形態、方法論對應判準；末節另有三個不繫於特定場景的常見誤解 |
| 需要填產出物，要現成表格骨架 | `references/templates.md` | 〈執行流程〉各步對應的範本表格，欄位與方法論條文一致 |

## Example

系統有一個 HTTP API 共用的 DB 連線池，另有 cron 對帳與 webhook 消費者也搶這個池。第 1 步列通道：連線池是通道、DB 是真持有者、仲裁器掛在借出連線之前。第 2 步標到達類別：HTTP 請求屬等待型；cron 屬自發型；webhook 逐跳標——送達跳等待型（未回 2xx 前發送方在等）、確認收訖後的處理跳自發型。第 3 步定佔用量：以「已借出連線數＋等待者數＋最老等待者年齡」實例化。第 4 步填九格表時，webhook 的付款完成事件落「等待型 × 不可棄」格，該格不由仲裁器卸載，無法服務即觸發容量失敗訊號，路由回 `capacity-performance` 的 tripwire 表。完整案例見 `references/worked-examples.md` 場景 (a)。
