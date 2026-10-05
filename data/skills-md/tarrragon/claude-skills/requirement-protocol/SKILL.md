---
name: requirement-protocol
description: "從需求確認到實作的對話協議：模糊指令澄清（含篩選類）、可決定 vs 該確認的邊界、失敗 2 次的轉折、覆寫成本告知、revert/checkpoint 處理、漸進驗證、工具切換時機。Triggers: 收到模糊指令, 自決還是確認, 反覆失敗, 換思路, 覆寫成本, 先還原, 先重來, placeholder, 最小範圍, 推理失敗, playwright 切換, 開發前澄清, 需求確認, 排除障礙, 逼近答案, 依 X 篩選, 只看 X, filter 範圍, 呈現決策, 開放問, ABCDE 你選哪個, 反省題, retrospective, 下一步往哪走, 五維度, 需要我繼續嗎, 要做嗎, OK 嗎, yes/no, 二選, 確認嗎."
license: MIT
metadata:
  portable: true
  version: 0.8.4
  category: collaboration-protocol
---

# Requirement Protocol

從需求確認到實作的對話協議。把「使用者下指令 → 執行者實作」之間的溝通流程結構化、避免反覆失敗、避免做出使用者沒要的東西、避免在錯誤方向上累積沉沒成本。

協議的核心命題：**對話成本與重做風險之間有最佳化空間**。全自決對話成本最低、但容易做錯；全確認重做風險最低、但對話爆炸。協議定的是「哪些該攤、哪些自決」、以及「卡住時該怎麼轉彎」。

---

## Core Pillars（核心支柱）

| 支柱                                       | 意義                                                                 |
| ------------------------------------------ | -------------------------------------------------------------------- |
| **Visibility-Based Confirmation** 可見性確認 | 使用者會看到的決定（數字 / 順序 / 文字）攤開確認、純技術細節自決     |
| **Two-Occurrence Threshold** 2 次門檻        | 第 1 次是運氣、第 2 次是訊號；同方向失敗 2 次就停、不沿同方向加碼到 3 |
| **Cost Transparency** 成本透明              | 覆寫深度、revert 影響、最小必要範圍 — 把成本攤開讓使用者參與決策     |
| **Multi-pass Refinement** 多輪精煉           | 第 1 輪實作不追求完美、預期會有未發現問題；設計第 2 / 3 輪用不同 frame 收斂、不是「再仔細一次」、是換角度看（[#82](references/principles/literal-interception-vs-behavioral-refinement.md) / [#85](references/principles/methodology-multi-pass-embedding.md)） |

---

## Core Principles（核心原則速查）

讀者在本區塊能完成大方向判斷；具體情境的展開（步驟 / 模板 / 反例）依下方「觸發路由」進對應 reference。

### 1. 可決定 vs 該確認的邊界

純技術實作（grid / flex、ResizeObserver / setInterval、selector 寫法）可自決；使用者會看到的決定（breakpoint、預設尺寸、filter 順序、UI 文字、配色）先列選項給使用者點頭。

判斷標準三問：**UI 上會不會產生使用者感知的差異？選不同會不會影響體驗？寫進 commit 後改動成本高不高？** 任一個「是」 → 該確認。確認時給「選項 + 推薦 + 開放修改」、不要開放問。

### 2. 同方向失敗 2 次 = 停下驗證假設

第 1 次失敗多半是執行細節（typo、cache、syntax）— 修了再試。第 2 次同方向失敗、不要再試一次更小心、用工具驗證底層假設（DOM tree、computed style、framework 行為）。

驗證後分兩條路：**假設對 → 繼續修；假設錯 → 換方向、不為前面的努力買單**。第 3 次同方向加碼（更複雜的 selector、加 `!important`、再寫一層 polyfill）會放大原本的問題、產生脆弱的 patchwork。

### 3. 推理失敗 2 次切到量測工具

靜態 CSS 推理 + 視覺截圖溝通的迴圈在第 1 次假設錯了之後成本就爆炸。第 2 次失敗主動提：**起 server、用 playwright `browser_evaluate` 讀 live DOM**。

工具切換 ROI 在第 1 次失敗後就轉正、不要等到第 5 次。簡單一次性確認用 DevTools、複雜或反覆 debug 用 playwright（可重跑、可寫成測試）。

### 4. 覆寫成本攤開、不偷偷對抗

當客製需求看似簡單但會對抗多層（UA stylesheet、framework CSS、browser default）— 在開始寫之前先報成本：**「會打到哪幾層、要寫幾條規則、剩下什麼風險（升級會壞？瀏覽器差異？）」**、讓使用者決定值不值。

不在使用者不知情的情況下堆 `!important` / specificity 戰 / 多層 polyfill — 沉默對抗會讓使用者驚訝於後續的維護負擔。

### 5. Revert 含 checkpoint、不直接清空

收到「先還原」「先重來」「換個方向」時、先確認：**還原到哪個狀態？要不要先 commit 當前進度當 checkpoint（標「explored, not adopted」）？** 再執行 reset。

探索的成果即使沒採用、也是「為什麼不採用」的證據 — 直接清空會丟掉「下次別再走這條路」的判斷依據。

### 6. 漸進驗證、最小必要範圍

UI debug 從色塊 placeholder 起步（沒文字、沒樣式、單純色塊）→ 確認位置 / 尺寸 / grid 對 → 再加文字 → 再加樣式 → 再加互動。每階段只引入一個變數。

Selector / MutationObserver root / JS 操作邊界：**從最小開始、有證據再擴張**。「先寬後縮」分不出哪個寬度是刻意的；「先窄後寬」每次擴張都有原因。

### 7. Multi-pass Refinement：第 1 輪不追求完美、設計第 2 / 3 輪用不同 frame

第 1 輪實作預期會有未發現問題、不要追求 perfect — 跑得到結尾、看實際結果比寫得漂亮重要。第 2 輪用「對需求 / 邊界 case」frame、第 3 輪用「dogfood / 反向自查」frame、第 N 輪換「上層原則」frame。每輪不同 frame 才能 catch 上一輪 miss 的東西。

呈現決策時的「五維度展開」（[`references/decision-dialogue.md`](references/decision-dialogue.md)）就是 multi-pass 在「決策呈現」場景的具體實現：每維度等於一輪 self-check。**「再仔細一次」≠ multi-pass — 同 frame 重看 catch 不到不同層的錯**。L4 review / pair / dogfood 才是行為錯誤的解、不是再寫一條 hook（[#82](references/principles/literal-interception-vs-behavioral-refinement.md)）。

---

## When to Consult This Skill（觸發路由）

| 觸發情境                                                        | 讀哪份 reference                              |
| --------------------------------------------------------------- | --------------------------------------------- |
| 收到模糊指令（含「對齊」「靠近」「隔離」「不要動」「分開」等）  | `references/clarifying-ambiguous-instructions.md` |
| 不確定某個決定該自決還是該先問使用者                            | `references/clarifying-ambiguous-instructions.md` |
| 收到「依 X 篩選 / 只看 X / 過濾 Y」類指令、source 是分批的       | `references/clarifying-ambiguous-instructions.md`（類型 5：篩選三問） |
| 同方向失敗 ≥ 2 次、想再試一次更小心                              | `references/failure-pivot-protocol.md`        |
| 推理 + 視覺截圖溝通迴圈卡住、不知道該不該換工具                  | `references/tool-switching-timing.md`         |
| 客製需求要對抗多層（vendor CSS、framework、browser default）     | `references/cost-and-checkpoint.md`           |
| 收到「先還原 / 先重來 / 換個方向」類指令                         | `references/cost-and-checkpoint.md`           |
| 開始 UI layout debug、不知道從哪一步起                           | `references/progressive-verification.md`      |
| 設計 selector / MutationObserver root / JS 操作範圍              | `references/progressive-verification.md`      |
| 準備呈現決策給使用者選擇（A 還是 B、要不要做 X）                  | `references/decision-dialogue.md`             |
| 寫到「你想怎麼做？」「ABCDE 你選哪個？」這類開放問                | `references/decision-dialogue.md`             |
| 反省題 / retrospective / 「下一步往哪走」類問題                   | `references/decision-dialogue.md`             |

每份 reference 自包含：以該情境為核心、把核心原則翻譯成可直接套用的協議步驟與模板。閱讀任一 reference 不需要回來看其他 reference。

**與 `wrap-decision` 的邊界**：本 skill 處理「使用者**指令**是否明確可執行」（模糊指令澄清）。若卡點是「決策諮詢的當事人條件不足」或「要 premortem 的計畫輪廓不清」而非指令模糊，那屬 `wrap-decision` 的資料充足度閘門（Step 0）與 premortem context 閘門——先讀 `../wrap-decision/SKILL.md`。三者互為前置、不重複問同一組問題（分工對照表見該檔 Step 0「與 requirement-protocol 的分工邊界」）。

---

## Success Criteria（M1-M2 認知負擔類）

| Metric | 定義                                                                  | 目標 |
| ------ | --------------------------------------------------------------------- | ---- |
| **M1** | 從 SKILL.md 出發、解決一個觸發情境需要開幾個檔案                     | ≤ 2  |
| **M2** | 隨機抽一份 reference、不讀其他 reference 能否獨立套用                 | 100% |

---

## Directory Index

```text
requirement-protocol/
├── SKILL.md                                       # 本檔：核心支柱 + 核心原則速查 + 觸發路由
└── references/
    ├── clarifying-ambiguous-instructions.md       # 情境 1：模糊指令的澄清協議（spatial / relative / isolation / decision-authority）
    ├── failure-pivot-protocol.md                  # 情境 2：失敗 2 次的轉折協議（停下、驗證假設、換方向）
    ├── cost-and-checkpoint.md                     # 情境 3：覆寫成本告知 + revert 含 checkpoint
    ├── progressive-verification.md                # 情境 4：placeholder 漸進 + measurement 完整性 + 最小必要範圍
    ├── tool-switching-timing.md                   # 情境 5：推理 / DevTools / playwright 之間的切換時機
    └── decision-dialogue.md                       # 情境 6：呈現決策的五維度協議（呈現 / 策略 / 批次 / 時間 / 選項類型）
```

---

## Reading Order（建議閱讀順序）

1. 第一次接觸 → 從本 SKILL.md 的「核心支柱 + 核心原則」讀起
2. 進入實際情境 → 依觸發路由讀對應 reference（只讀一份）
3. 想驗證自己有沒有套用對 → 用該 reference 結尾的 self-check checklist 自評

---

## 相關抽象層原則

本 skill 的協議建立在幾條抽象層原則上、實作協議時可背景引用（檔案位置：`references/principles/`）：

- [#42 2 次門檻](references/principles/two-occurrence-threshold.md) — 第 1 次失敗是運氣、第 2 次是訊號（「同方向失敗 2 次」與「推理失敗 2 次切到量測工具」兩條原則的根據）
- [#43 最小必要範圍](references/principles/minimum-necessary-scope-is-sanity-defense.md) — 範圍從窄起、有證據再擴張（原則 6 的根據）
- [#44 SSOT](references/principles/single-source-of-truth.md) — 值的住址只能一處（成本告知與澄清的共骨）
- [#45 外部組件合作四層](references/principles/external-component-collaboration-layers.md) — 離公共介面越近越穩
- [#67 寫作便利度跟意圖對齊反相關](references/principles/ease-of-writing-vs-intent-alignment.md) — 容易寫的位置通常是錯位的位置（meta-principle、解釋為什麼澄清協議能 catch 到便利驅動的錯誤）
- [#68 驗收的時間軸：四個 checkpoint](references/principles/verification-timeline-checkpoints.md) — 寫之前 / 開發中 / ship 前 / ship 後分散驗收（原則 6 的展開）
- [#69 Test-First：先看到 RED 才相信 GREEN](references/principles/test-first-red-before-green.md) — 「需求確認」最重要的一環：使用者意圖落實成測試 → 在 buggy code 上跑出 RED 才證明測試 catch 到該意圖、再修到 GREEN — 跳過 RED 等於跳過「測試對應到使用者意圖」的驗證
- [#70 URL 是 stateful UI 的儲存層](references/principles/url-as-state-container.md) — 列「使用者意圖完整集合」要包含 URL 維度：分享 / reload / back-forward 該不該保留 state
- [#71 Tab Order = DOM Order = Mental Model 三者對齊](references/principles/tab-order-mental-model-alignment.md) — A11y 維度的需求澄清：使用者預期「先做 X 再做 Y」、tab 順序該對齊 mental model
- [#72 高 ROI 無外部觸發的工作會被結構性跳過](references/principles/external-trigger-for-high-roi-work.md) — meta-原則：澄清 / Checkpoint 1 / RED phase 都是「沒便利路徑」工作、修法是 L3-L5 結構性對策（PR template / CI / pair）、不是「下次記得」
- [#73 搜尋引擎的匹配模式跟使用者預期的對齊](references/principles/search-engine-matching-mode-mismatch.md) — Checkpoint 1 列「使用者意圖完整集」要包含「使用者打字行為的預期」：工具預設 matching mode（prefix）跟使用者預期（substring，被 Google 訓練）對齊嗎？
- [#74 決策呈現：選項 + 推薦 + 開放修改](references/principles/decision-presentation-options-recommendation.md) — 不要開放問、給結構表 + 推薦、把整理問題的成本攤在 agent 而非 user
- [#75 主策略 + 補強：選擇不必互斥](references/principles/main-strategy-plus-supplementary.md) — 多策略可疊加（structural + UX）、預設「五選一」會放掉互補可能
- [#76 分批 ship：可見性 + 風險 + 驗證三軸切分](references/principles/incremental-shipping-criteria.md) — 「ship 順序 ≠ 重要程度」、低風險可見價值先 ship
- [#77 「現在不決定」是合法選項](references/principles/decide-later-as-valid-option.md) — 決策表加「延後 + 條件」欄、區分逃避決策 vs 結構性延後
- [#78 反省任務預設複選](references/principles/retrospective-multi-select-default.md) — 互斥要證明、不互斥是預設、反省題用 radio = 結構性 collapse
- [#79 決策對話的五維度](references/principles/decision-dialogue-dimensions.md) — meta-#74-#78、五個獨立維度的鬆綁、預設都選窄格 = 把使用者塞進最少自由度的盒子
- [#80 Yes/No 二選是隱式 collapse](references/principles/yes-no-binary-collapse.md) — 「需要 X 嗎？」「OK 嗎？」最常見最隱形的 collapse、修法是翻成多選表
- [#81 卡片系統的迭代浮現](references/principles/cards-as-living-system-iteration.md) — 本 skill 的 reference 是 spiral 浮現、不是線性寫成、process-level 元原則
- [#82 字面攔截 vs 行為精煉](references/principles/literal-interception-vs-behavioral-refinement.md) — 驗證手段跟錯誤層次對齊、行為錯誤（如 collapse）靠 multi-pass spiral 收斂、不是「補一條 hook 規則」、本 skill 的 reference + dogfood examples + self-check 就是 multi-pass 設計

---

**Last Updated**: 2026-07-05

版本紀錄在同目錄的 `CHANGELOG.md`。
