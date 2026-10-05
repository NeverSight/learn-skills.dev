---
name: cc-release-impact-review
description: "Claude Code release notes 框架影響評估工具。比對 last-reviewed 版本篩出新版本，逐項分類（對框架有幫助 / 需評估 / 無影響 / 不適用），對採用項引導建 ANA + WRAP + spawn 落地。Use when: 執行 /release-notes 看到新版本、定期檢查 CC 更新、評估新功能對專案框架的影響時。Triggers: release notes, release-notes, CC 更新, claude code 更新, 版本更新評估, 新功能評估, 框架影響評估。"
metadata:
  version: 1.0.0
---

# CC Release Impact Review Skill

**定位**：流程引導 skill（仿 `wrap-decision`），把「Claude Code 更新 → 框架影響評估 → spawn 落地」固化為可重複流程。

**核心理念**：CC 平台持續更新，新功能可能改善本專案的派發 / 互動 / 可觀測性規範，也可能與既有規則產生張力。每次更新都應被評估，但只評估「未評估過的新版本」，避免重複勞動。

> **首要原則：去重先於評估**。先讀狀態檔確認 last-reviewed 版本，只評估其後的新版本。重複評估已落地版本是浪費（本 skill 因 W4-028 重複評估 2.1.157 的教訓而生）。

---

## 觸發條件

| 情境 | 識別特徵 |
|------|---------|
| 看到新版本 release notes | 執行 `/release-notes` 後出現未評估的版本號 |
| 定期檢查 | 用戶要求「檢查 CC 更新對框架的影響」 |
| 升級後回顧 | CC 自動更新後想確認新功能是否該納入框架 |

---

## 評估流程（五步）

### Step 1：讀狀態檔，確定起點

讀 `state/last-reviewed.md`，取得 last-reviewed 版本號。**只評估其後的新版本**，已評估版本直接跳過。

### Step 2：取得 release notes

用戶執行 `/release-notes` 並貼上 stdout，或提供版本區間。skill 不自行 fetch 網路（避免外部依賴）。

### Step 3：逐項分類

對每個新版本的每一條，歸入下表四類之一。**禁止漏項**——無影響 / 不適用項也必須顯性標註理由（避免「看似評估完整實則跳過」）。

| 類別 | 判準 | 後續 |
|------|------|------|
| 對框架有幫助 | 可改善既有派發 / 互動 / 可觀測性 / 流程規範 | 進 Step 4 規劃落地 |
| 需評估 | 可能有幫助但需先分析相容性 / 成本 | 建 ANA child 深入 |
| 無影響 | 純 bug fix / 平台內部 / 與本專案無關 | 標註理由，不動作 |
| 不適用 | 針對本專案未用的供應商 / 機制（如三方 Bedrock、plugin） | 標註理由，不動作 |

**特別注意「張力項」**：新功能若與既有規則衝突（如 CC 行為改變 vs 專案強制規則），歸「需評估」並標為高價值，方向交用戶決策（敏感規則改動不擅自落地）。

### Step 4：對採用項建 ANA + WRAP + spawn

採用項（有幫助 / 需評估）依 `quality-baseline` 規則 5 建 ANA ticket：

1. Problem Analysis：逐項評估表（含去重說明 + 無影響標註）
2. Solution：WRAP 四階段（W 擴增採用粒度 / R 現實檢驗 / A 機會成本 / P 絆腳索）+ spawn 規劃表
3. children：以 `--parent` 建立落地 IMP/DOC/ANA（PC-091：ANA 落地用 children 不用 spawned_tickets）
4. 框架文字變更後派 `basil-writing-critic` 審查（三明示 / 禁用詞 / 簡體字）

**範本**：W4-028（worktree/agent/OTEL/plugin 評估）、W4-029（本 skill 的 source ANA）為標準範例，新評估比照其結構。

### Step 5：更新狀態檔

評估完成後，更新 `state/last-reviewed.md` 的 last-reviewed 版本號，並追加本次評估的版本區間 + 對應 ticket ID 到歷史表。

---

## 狀態記錄機制

`state/last-reviewed.md` 記錄：

- **last-reviewed**：已評估的最新版本號（去重依據）
- **評估歷史表**：版本區間 / 評估 ticket ID / 主要結論

下次觸發時讀此檔，從 last-reviewed 之後開始，避免重複（如 W4-029 跳過 W4-028 已評估的 2.1.157）。

---

## 輸出格式

skill 產出：

1. **評估表**：四類分類（含無影響 / 不適用的理由）
2. **建議 ticket 清單**：採用項對應的 ANA / children 規劃
3. **狀態更新**：新的 last-reviewed 版本號

---

## 反模式

| 反模式 | 為何有害 | 正確做法 |
|-------|---------|---------|
| 不讀狀態檔直接評估全部版本 | 重複評估已落地版本（W4-028 重評 2.1.157 的教訓） | Step 1 先讀 last-reviewed，只評估新版本 |
| 只列「有幫助」項，跳過無影響項 | 看似評估完整實則漏項，後人無法判斷是否真評估過 | 四類全標，無影響 / 不適用須附理由 |
| 敏感規則（與平台行為衝突）擅自改 | 影響整個專案互動模式，越權 | 歸「需評估」高價值，方向交用戶決策 |
| 評估後不更新狀態檔 | 下次重複評估同一批版本 | Step 5 必更新 last-reviewed |

---

## 相關文件

- `.claude/rules/core/quality-baseline.md` — 規則 5（所有發現必須追蹤）
- wrap-decision skill（若已安裝）— Step 4 的 WRAP 框架完整方法論；未安裝時仍可依 Step 4 內文已列出的四階段摘要（W 擴增採用粒度 / R 現實檢驗 / A 機會成本 / P 絆腳索）執行，只是不會有該 skill 的完整深度可查
- `.claude/pm-rules/askuserquestion-rules.md` — 敏感項交用戶決策時的提問規範
- W4-028 / W4-029 ticket — 標準評估範例

---

版本紀錄在同目錄的 `CHANGELOG.md`。
