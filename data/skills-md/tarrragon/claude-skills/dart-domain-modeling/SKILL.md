---
name: dart-domain-modeling
description: "Dart/Flutter copyWith 收窄判準與 entity 不變式設計。Use when designing or reviewing copyWith, entity classes, value objects, freezed models, domain invariants, or state transition methods (markAsX/completeY)."
metadata:
  version: 1.0.0
---

# Dart Domain Modeling Skill

判斷 `copyWith` 在特定型別上是正確工具還是繞過不變式的逃生口，並提供收窄與審查判準。

## 核心判準：識別測試

先問一個問題，決定整個型別的 `copyWith` 策略：

> **此型別有沒有「不允許任意組合的欄位」？**

| 回答 | 結論 |
|------|------|
| 沒有（純資料載體：DTO / API model / UI state / 小型 value object） | `copyWith` 是正當的便利工具，欄位逐一覆寫語意清晰、無代價，保留全欄位 public `copyWith` |
| 有（entity：帶著一組**有意圖的狀態轉換方法**，如 `startX()` / `completeX()` / `markAsY()`，且這些方法會記錄稽核歷史或強制轉換順序） | `copyWith` 對該型別是逃生口，必須收窄（見下表） |

**判斷依據**：freezed 之類的程式碼生成工具會替每個 model 自動產生全欄位 `copyWith`，這是 Dart 生態的預設路徑，對純資料載體完全合理；問題不在 `copyWith` 本身，而在「public 全欄位 `copyWith` 掛在 entity 上」——它讓每個具意圖的狀態轉換方法從「唯一路徑」降級成「建議路徑」。

## 三層收窄表

| 對象 | 處置 |
|------|------|
| value object / DTO / UI state | 保留 `copyWith`，這裡它是正確工具 |
| 有領域方法的 entity | `copyWith` 改為 private，僅供內部領域方法呼叫；或至少從參數列移除「必須經由領域方法變更」的欄位（如狀態欄位、歷史紀錄欄位） |
| 測試建構 | 讓測試工廠（`createForTest` 之類）接受完整的建構參數，消除「用 `copyWith` 拼裝再撈預設值」的動機——修工廠的表達力，不是修每一個拼裝點 |

## 逃生口機制：為什麼繞過會自然發生

`copyWith` 作為逃生口的危險之處：**它總是有辦法把物件拼出來，所以呼叫端永遠不會被迫去修那個表達力不足的工廠或補齊缺的領域方法。** 建構路徑或工廠的表達力缺陷被逃生口吸收掉，然後以語意錯誤的形式在別處復發。

一旦發現「呼叫端繞過領域方法直接用 `copyWith` 改狀態」，正確修法不是禁止那一個呼叫點，而是回頭問：呼叫端為什麼繞？通常是工廠或介面給不了它要的表達力。修表達力，而非修拼裝點。

## 兩種違規形態（審查時 grep 得到）

### 形態一：直接改受保護欄位，繞過狀態轉換方法

```dart
// 違規：直接改 status，繞過 markAsAvailable() / completeEnrichment()
final result = draft.copyWith(status: EntityStatus.available);

// 正確：透過領域方法，狀態轉換連帶記錄稽核歷史
final result = draft.markAsAvailable();
```

**後果**：狀態轉換沒有進入稽核歷史（`modificationHistory` 之類的欄位）。稽核軌跡有洞，而且是靜默的——沒有任何錯誤、警告或測試失敗會提示。

**Grep 訊號**：`.copyWith(status:` 或 `.copyWith(<受保護欄位>:` 出現在領域方法定義之外。

### 形態二：註解宣稱約束，實作零檢查

```dart
/// 約束：只能從 enriching 狀態轉換，確保狀態流程正確
Entity completeEnrichment() {
  final newHistory = _modificationHistory.addChange('...');
  return copyWith(status: EntityStatus.enriched, modificationHistory: newHistory);
  // 內部沒有任何 if / assert / throw 檢查前置狀態
}
```

**後果**：這比「沒有約束」更糟——註解讓讀者以為有防護。而且就算方法內部加了檢查，若 `copyWith(status: ...)` 對外仍是 public，逃生口還是繞得過去；約束要成立，逃生口就得先關上。

**Grep 訊號**：方法註解含「約束」「只能」「必須」等字樣，但方法本體 grep 不到 `if` / `assert` / `throw`。

## Examples

**輸入**：審查一個 entity 類別，發現 `copyWith` 參數列包含 `status` 且為 public。

**動作**：

1. 套用識別測試——此型別有無狀態轉換方法（`markAsX()` / `completeY()` 之類）？有 -> 進入收窄流程。
2. Grep 全專案 `.copyWith(status:` 或對應受保護欄位，列出所有繞過點。
3. 對每個繞過點，回頭檢查呼叫端為什麼不走領域方法——通常是工廠或介面缺這個組合的建構能力。
4. 修法優先序：先修工廠/介面表達力，再移除繞過呼叫，最後把 `copyWith` 收窄為 private 或移除受保護欄位。

**輸出**：受保護欄位不再出現在 public `copyWith` 參數列；狀態轉換全數經過領域方法；稽核歷史無缺口。

## 相關文件

- `.claude/error-patterns/implementation/IMP-APP-003-fresh-checkout-missing-gitignored-generated-artifacts.md` —— 「單張 ticket 裡的觀察若未升格，下一個執行者不會讀到它」，本 skill 存在的理由（跨情境的通用教訓，非該篇技術主題本身）
- 「介面隔離 + 語意化方法優先於直接操作狀態」是本 skill 判準的上位原則。狀態管理層曾有對應的 `dart-provider-architecture` skill，因其參考範例綁定單一專案的檔案路徑而移除；需要 Riverpod 層規範時，以所在專案 `lib/core/providers`（或等價目錄）的既有慣例為準，不套用他專案的範例

---

版本紀錄在同目錄的 `CHANGELOG.md`。
