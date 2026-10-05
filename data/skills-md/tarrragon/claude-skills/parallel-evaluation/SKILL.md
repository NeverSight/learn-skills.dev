---
name: parallel-evaluation
description: "多視角審核/code review 工具。派發三人組（含常駐委員 linux）並行掃描程式碼品質、架構設計、重構評估。Use for: 程式碼審查, 架構評估, 重構掃描, 結論審查, 系統設計變更審查, 功能規劃審查。Use when: Phase 3b 完成後 PR 前, Phase 4 重構評估前, 重大架構決策前, ANA Ticket 結論審查, 任何分析報告產出後, 規則/Skill/方法論變更後, Wave 完成審查, 規格設計完成後"
metadata:
  version: 1.3.1
---

# 並行評估工具

> 方法論: .claude/methodologies/parallel-evaluation-methodology.md

## 核心流程

**Phase 1** → 收集標的（確定掃描範圍）
**Phase 2** → 並行視角掃描（2-4 Agent 同時掃描）
> Phase 2 預算檢查: `reference_tokens + (N x avg_target_tokens) + (N x output_tokens) < 100,000`。超過則減少 N 或拆分標的。

**Phase 3** → 彙整 + Worth-It Filter + **建立 Ticket** + **錯誤模式記錄**（決定執行方式，所有發現必須追蹤）
> Phase 3 強制步驟：(1) 彙整發現 → (2) Worth-It Filter 分類 → (3) **對每個「延後執行」項目執行 `ticket create`** → (4) 將 Ticket ID 填入報告表格 → (5) **結構性發現→錯誤模式記錄**（見下方判斷標準）→ (6) 輸出報告。步驟 3-5 不可省略，報告中不可出現沒有 Ticket ID 的「延後追蹤」行。
> Phase 3 步驟 5 判斷標準：發現是否為**結構性模式**（跨專案可重現的錯誤類型，而非單次的專案 bug）？若是，執行 `/error-pattern add` 記錄到 `.claude/error-patterns/`。判斷方式：將發現中的專案名稱和檔案路徑替換為通用描述，如果仍然有意義 → 是結構性模式。
> Phase 3 衝突處理：視角間有衝突時，依衝突分類策略處理（加法vs減法預設減法，linux 品味否決權）。詳見 .claude/methodologies/parallel-evaluation-methodology.md「衝突處理策略」。

## 常駐委員機制

parallel-evaluation 的常駐委員分兩類，加入規則與 opt-out 條件不同：

| 類型 | 代理人 | 加入情境 | 可 opt-out |
|------|--------|---------|-----------|
| `universal_lens` | linux | 所有情境無條件加入（Good Taste / 架構複雜度為所有產出的元維度） | 否 |
| `universal_lens` | basil-writing-critic | 所有情境無條件加入（程式碼註解、docstring、error message、commit message 皆為書面文字） | 否 |

**linux 常駐說明**：linux 評分對應 Worth-It Filter：Garbage = 高幅度、Acceptable = 中幅度、Good taste = 無發現。Wave 完成審查時，除了標準的多視角代理人外，必須額外派發 linux 代理人作為常駐審查委員，與 code-reviewer（Bug/安全）和 code-explorer（架構/設計）組成固定三人組（見 parallel-dispatch.md 多視角審查固定三人組章節）。

**basil 常駐說明**：所有程式碼都包含書面文字（註解、docstring、error message、commit message），文字品質審查在任何情境都有價值。basil 與 linux 同為 `universal_lens`，所有情境無條件加入。

## 情境快速選擇

| 情境 | 適用時機 | 視角 | Agent 數（含常駐 linux + basil） |
|------|---------|------|-------------------------------|
| A: 程式碼審查 | Phase 3b 後、PR 前 | Reuse + Quality + Efficiency | 3+2 |
| B: 重構評估 | Phase 4 前、TD 清理 | Redundancy + Coupling + Complexity | 3+2 |
| C: 架構評估 | SA 審查、新架構決策 | Consistency + Impact + Simplicity | 3+2 |
| D: 功能評估 | Phase 1 後、需求確認 | Overlap + Fit + Scope | 3+2 |
| E: 冗餘偵測 | 版本規劃、系統清理 | Duplication + State + Interface | 3+2 |
| F: 結論審查 | 任何分析報告產出後 | Evidence + Alternatives + Scope | 3+2 |
| G: 系統設計 | 規則/Skill/方法論變更後 | Consistency + Completeness + CogLoad | 3+2 |

> 各視角詳細檢查項目: references/lens-configurations.md
> 各視角 prompt 模板: references/lens-prompts.md

> **跨情境觸發**：標的為防護、守衛、閘門、檢查類產出時（不限上表情境），至少一個視角須附加 `references/lens-prompts.md`「跨情境必問：防護類標的的驗收覆蓋」的四問模板。該問題不可由標的自身的驗收條件回答（PC-BAL-035）。

**語言代理人加入規則**：當審查標的涉及語言/框架專屬的基礎設施或開發流程時，將對應語言代理人作為額外審查委員加入標準三人組：

| 審查標的涉及 | 加入代理人 | 常見場景 |
|-------------|-----------|---------|
| Flutter/Dart | parsley-flutter-developer | Widget 架構、Riverpod 設計、Dart 慣例 |
| Python | thyme-python-developer | Hook 系統、腳本設計、Python 慣例 |
| Go | fennel-go-developer | 後端服務、Go 慣例 |

此規則對情境 C（架構評估）和 D（功能評估）尤為重要，因為規劃階段的決策深受語言/框架限制影響。語言代理人可提供框架專業知識，避免產出不符合實際開發慣例的方案。

## Worth-It Filter 快速判斷

**核心原則**：Worth-It Filter 只決定「是否立即執行」，不決定「是否追蹤」。所有發現都必須建 Ticket 或寫入 todolist。發現技術債是一個問題，修復成本是否值得是另一個問題——兩者不在同一時刻決策。

| 改善幅度 | 風險低 | 風險高 | 追蹤方式 |
|---------|--------|--------|---------|
| 高（bug/安全） | 立即執行 | 立即執行 | 建 Ticket（P0/P1） |
| 高（簡化） | 立即執行 | 延後執行 | 建 Ticket（P1） |
| 中（維護性） | 立即執行 | 延後執行 | 建 Ticket（P2） |
| 低（風格） | 延後執行 | 延後執行 | 建 Ticket（P2） |

**Why**：本表的「延後執行」是合法狀態（b）——延後決策必須綁 ticket trigger（見 `.claude/rules/core/decision-trigger-binding.md` 規則 1 / 1.5）。表格右欄的「建 Ticket」就是 trigger 綁定，缺一即退化為無 trigger 延後。

**Consequence**：報告中出現「延後」但 Ticket 欄為空，等同未追蹤；該發現會在「以後」與「永不」之間累積為死議題（PC-093 反模式）。

**Action**：執行有疑慮就延後，但追蹤不可省略。Phase 3 產出報告前，必須對所有延後項目執行 `ticket create`，並在報告表格的 Ticket 欄填入實際 ID。**禁止行為**：報告中出現「延後」但 Ticket 欄為空。

> 量化標準和案例: references/worth-it-filter-details.md

## 執行範例

### 情境 A: 程式碼變更審查

```
Phase 1: git diff --name-only 取得變更檔案
Phase 2: 並行派發 3 Agent
  - Explore: 掃描是否有可重用的既有 utility
  - code-reviewer #1: 掃描冗餘狀態和 copy-paste
  - code-reviewer #2: 掃描不必要的工作和效能問題
Phase 3: 彙整發現 → Worth-It Filter → 行動清單
```

### 情境 F: 結論審查

```
Phase 1: 收集分析報告/結論
Phase 2: 並行派發 3 Agent
  - Explore #1: 驗證結論是否有程式碼佐證
  - Plan: 檢查是否遺漏替代方案
  - Explore #2: 評估影響範圍估計是否合理
Phase 3: 任一視角發現問題 → 回到分析階段補充
```

## 報告格式

```markdown
## 並行評估報告

**標的**: [範圍]  **情境**: [A-G]

### 值得行動

| # | 視角 | 發現 | 幅度 | 風險 | 決策 |
|---|------|------|------|------|------|

### 延後追蹤（建 Ticket，不立即執行）

> **強制**：此表格每一行的 Ticket 欄必須填入實際 Ticket ID（格式如 `{version}-W{wave}-{seq}`）。空白 Ticket 欄 = 未追蹤 = 違反 quality-baseline 規則 5。

| # | 視角 | 發現 | 延後原因 | Ticket |
|---|------|------|---------|--------|

### 結構性錯誤模式（已記錄到 error-patterns/）

> 此區段僅在有結構性發現時出現。判斷標準：將發現中的專案名稱和檔案路徑替換為通用描述，如果仍然有意義 → 記錄。

| # | Pattern ID | 標題 | 來源發現 |
|---|-----------|------|---------|

### 結論
[總結]
```

> **禁止自創「不行動/排除」類別**（0.3.4-W3-004）：報告中所有發現必須歸入「值得行動」或「延後追蹤」，沒有第三類。「評估後不立即執行」= 歸入「延後追蹤」並建 ticket，不是「排除不追蹤」。Why：PM 容易把「不值得立即做」滑坡成「不值得追蹤」，使發現退化為死議題（PC-093）。

## 與 `/bulk-evaluate` 的區別

| 維度 | `/parallel-evaluation` | `/bulk-evaluate` |
|------|----------------------|--------------------|
| 並行軸 | N 個視角 x 1 組標的 | 1 個標準 x N 個單位 |
| 產出物 | 彙整報告（回到主線程） | N 個子 Ticket（不回主線程） |
| 適用 | 多角度快速評估 | 批量處理 + context 卸載 |

**選擇原則**：需要多角度掃描同一標的 → 本工具；需要用同一標準掃描 N 個獨立目標 → `/bulk-evaluate`

## 相關文件

- .claude/methodologies/parallel-evaluation-methodology.md - 完整方法論
- `bulk-evaluate` skill（若專案已採用）- 批量評估（正交工具）
- references/lens-configurations.md - 視角配置
- references/lens-prompts.md - 各情境視角 prompt 模板 + 防護類標的跨情境必問
- references/worth-it-filter-details.md - 過濾標準
- references/integration-guide.md - 整合指南

---

版本紀錄在同目錄的 `CHANGELOG.md`。
