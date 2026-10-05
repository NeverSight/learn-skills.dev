---
name: frontend-with-playwright
description: "框架無關的前端開發協議 + Playwright 驗證 + 跨領域 Stream 操作架構：DOM topology 先於 CSS、CSS / JS 邊界辨識、Playwright 三個位置（假設 / 行為 / 互動驗證）、寫成 layout 測試、framework-managed DOM 共處、Reactive 效能盤點、a11y 三道防線、Filter × Source 層錯位 + 五策略合成（適用前端 / 後端 / 演算法 / DB）。Triggers: 寫 CSS, selector 精準, CSS layers, CSS-only vs JS, class toggle, MutationObserver, observer scope, polling, framework 共處, 外部組件客製, custom UI 邊界外, playwright 驗證, browser_evaluate, layout test, focus management, aria-live, keyboard a11y, reactive 效能, runtime cost, layout reflow, lazy loading, 前端網頁開發, vanilla, vue, react, jquery, filter × source, 層錯位, paginated source, post-filter, 自動續抓, 推進 query, 誠實進度 UX, 演算法 pipeline, middleware filter, materialized view, map-reduce."
license: MIT
metadata:
  portable: true
  version: 0.3.3
  category: frontend-engineering
---

# Frontend with Playwright

框架無關的前端開發協議 + Playwright 驗證。原則適用於 vanilla HTML/CSS/JS、Vue、React、jQuery — 因為核心是「DOM / CSS / JS 三者的本質行為」加上「Playwright 用 live DOM 量測驗證」、不依賴特定框架的渲染機制。

協議的核心命題：**先讀真實狀態、再寫規則；先量再改、不要靠假設**。前端 bug 多半來自「寫 CSS 時假設的 DOM 結構與實際不符」、「JS 改完元素被 framework 還原」、「listener 觸發頻率失控」。Playwright 把這些假設變成可驗證的量測值。

---

## Core Pillars（支柱）

| 支柱                                        | 意義                                                                    |
| ------------------------------------------- | ----------------------------------------------------------------------- |
| **Read Before Write** 先讀真實狀態          | 寫 CSS 前用 playwright/DevTools 量真實 DOM；寫 JS 前確認 framework 邊界 |
| **CSS-First, JS-Augment** CSS 為主、JS 補強 | 能 build-time 算的進 CSS、必須 runtime 量測的進 JS、邊界清楚不混搭      |
| **Measure, Don't Assume** 量測、不要假設    | Layout / 行為 / 互動三層、用 playwright `browser_evaluate` 把假設變已知 |

---

## Principles（原則速查）

讀者在本區塊能完成大方向判斷；具體展開（步驟 / 範例）依下方「觸發路由」進對應 reference。

### 1. 寫 CSS 前先確認 DOM topology

Class name 是約定、不是結構保證。寫 CSS 規則之前、用 playwright `browser_evaluate` 讀目標元素的 ancestor chain — 確認它在 DOM tree 的哪個位置、parent / sibling / 共用的 grid cell 是什麼。

Selector 設計三維度：**起點（document / 元件根 / 函式參數 / closest）+ 範圍（直接子節點 / 子孫）+ 過濾（attribute / 已處理標記）**。預設用最精準的、有證據再放寬。

### 2. CSS / JS 的邊界由「值能否 build-time 定下來」決定

能在 build time 算出來的值（design token、固定 breakpoint、靜態尺寸）→ 寫進 CSS variable / static rule。**必須 runtime 才能知道的值**（form 高度、scroll 位置、container 寬度）→ JS 量測後寫回 CSS variable、CSS 仍然只讀變數。

JS 的職責是 **toggle class / 寫 var**、不是設 inline style。`!important` / inline `display: none` 是 anti-pattern — 改用 class toggle 把樣式留在 CSS。Vendor CSS 用 `@layer` 包起來、自家 unlayered 自動贏 specificity。

### 3. Playwright 在開發循環的三個位置

**位置 1：假設驗證**（寫 CSS 前）— 讀 ancestor chain、確認結構符合假設。
**位置 2：行為驗證**（規則寫完後）— 讀 bounding rect / computed style、確認 layout 結果。
**位置 3：互動驗證**（dispatch event 後讀 state）— 模擬 input / click、量化驗證互動結果。

第 2 次同個版型 bug → 把 query 寫成 playwright 測試固化、CI 防回歸。

### 4. 與 framework-managed DOM 共處的邊界辨識

把 framework 子樹當「禁區」、客製 UI 注入到 framework 邊界外、用 CSS 控制視覺位置（absolute / margin / grid）。框架重渲染時、邊界外的客製 UI 不被 reconcile 清掉。

**JS 操作的邊界穩定性**（從穩到不穩）：reparent 整節點 > 改 inline style > 改 attribute > 改 textContent > 改 innerHTML > 改 framework 子節點。穩定性低的需要 MutationObserver 重做、或乾脆別碰。

**外部組件客製的合作層次**（穩定性梯度）：CSS variable / API > class hook > boundary DOM > 內部結構。離公共介面越近、升級越穩。

### 5. Reactive 監聽器的頻率盤點

MutationObserver 三維度：**root（最窄）、options（最少）、debounce（最長可接受）**。預設 `observer.observe(scope, { childList: true })`、不寫 `subtree: true` 除非有 case。

Polling（`setTimeout` / `setInterval`）有事件可監聽就替換成 MutationObserver — 0 latency / 0 idle CPU。Reactive perf debug 從 `console.count(callbackName)` 起、確認觸發頻率符合預期。

效能風險點四面向：**iteration 成本（500 results × regex test）、reflow 成本（>16ms 觸發 jank）、listener 頻率（如上）、resource 載入時序（lazy chunk vs critical path）**。

### 6. A11y 三道防線

**鍵盤可達性**：visible focus indicator、邏輯 tab 順序、modal 有 escape 路徑。三者缺一不可。
**動態 a11y**：JS reparent / hide 時保存並還原 focus；變動內容用 `aria-live="polite"` 廣播給 screen reader。
**Native > ARIA**：能用 `<button>` / `<fieldset>` / `<dialog>` 就不要自己組 ARIA role — native HTML 自帶 keyboard / focus / a11y tree、ARIA 是補強不是替代。

---

## When to Consult This Skill（觸發路由）

| 觸發情境                                                              | 讀哪份 reference                                                 |
| --------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 要寫 CSS 規則、需要先確認 DOM 結構 / selector 該怎麼寫                | `references/dom-topology-first.md`                               |
| 不確定 selector 該多寬、命中其他元素                                  | `references/dom-topology-first.md`                               |
| 不確定值該寫進 CSS 還是 JS、CSS layers / variable / class toggle 取捨 | `references/css-js-boundary.md`                                  |
| 用 `!important` / inline style 解 specificity                         | `references/css-js-boundary.md`                                  |
| 要用 playwright 驗證 layout / 假設 / 互動                             | `references/playwright-in-loop.md`                               |
| Layout bug 第 2 次出現、想寫成測試                                    | `references/playwright-in-loop.md`                               |
| 客製 UI 被 framework 還原、不知道該注入到哪                           | `references/framework-coexistence.md`                            |
| 要客製外部組件（pagefind / vendor library）                           | `references/framework-coexistence.md`                            |
| 使用者反映卡頓、CPU 100%、scroll lag、resize jank                     | `references/reactive-performance.md`                             |
| 要設計 MutationObserver / event listener 範圍                         | `references/reactive-performance.md`                             |
| 要驗收鍵盤 / screen reader / motor / 視覺 a11y                        | `references/accessibility-and-focus.md`                          |
| JS reparent 後 focus 跑掉、aria-live 沒朗讀                           | `references/accessibility-and-focus.md`                          |
| 設計 filter / sort / count 操作、source 是分批 / streaming            | `references/data-flow-and-filter-composition.md`                 |
| 「Load more 後畫面閃但內容沒變」的 silent 缺口                        | `references/data-flow-and-filter-composition.md`（層錯位）       |
| Backend / 演算法 / map-reduce 的 post-filter 漏項                     | `references/data-flow-and-filter-composition.md`（跨領域同結構） |

每份 reference 自包含：以該情境為核心、把六大原則翻譯成可直接套用的協議步驟與範例。閱讀任一 reference 不需要回來看其他 reference。

---

## Success Criteria（M1-M2 認知負擔類）

| Metric | 定義                                                  | 目標 |
| ------ | ----------------------------------------------------- | ---- |
| **M1** | 從 SKILL.md 出發、解決一個觸發情境需要開幾個檔案      | ≤ 2  |
| **M2** | 隨機抽一份 reference、不讀其他 reference 能否獨立套用 | 100% |

---

## Directory Index

```text
frontend-with-playwright/
├── SKILL.md                                    # 本檔：六大原則速查 + 觸發路由
└── references/
    ├── dom-topology-first.md                   # 情境 1：寫 CSS 前用 playwright/DevTools 量真實 DOM、selector 設計
    ├── css-js-boundary.md                      # 情境 2：CSS-only vs JS-assisted、class toggle、layers、variable 單一位置、檔案拆分
    ├── playwright-in-loop.md                   # 情境 3：playwright 三個位置（假設 / 行為 / 互動驗證）+ 寫成 layout test
    ├── framework-coexistence.md                # 情境 4：custom UI 留 framework 邊界外、外部組件四層合作、JS 操作邊界辨識
    ├── reactive-performance.md                 # 情境 5：observer scope、polling→observer、頻率盤點、iteration / regex / reflow
    ├── accessibility-and-focus.md              # 情境 6：focus on DOM move、keyboard 三要素、aria-live、native HTML > ARIA
    └── data-flow-and-filter-composition.md     # 情境 7：Filter × Source 層錯位 + 五策略 + 跨領域（前端 / 後端 / 演算法 / DB）
```

---

## Reading Order（建議閱讀順序）

1. 第一次接觸 → 從本 SKILL.md 的「三大支柱 + 六大原則」讀起
2. 進入實際情境 → 依觸發路由讀對應 reference（只讀一份）
3. 想驗證自己有沒有套用對 → 用該 reference 結尾的 self-check checklist 自評

---

## 跟 requirement-protocol 的關係

`requirement-protocol` 是上層的「對話協議」（澄清需求、失敗轉折、覆寫成本、工具切換時機）；本 skill 是下層的「前端執行協議」（DOM / CSS / JS / Playwright 的具體做法）。

當情境是「不確定該怎麼跟使用者溝通」 → 讀 requirement-protocol。
當情境是「知道要做什麼、不確定前端該怎麼實作驗證」 → 讀本 skill。
兩個 skill 的 `playwright` 段落互補：`requirement-protocol/tool-switching-timing` 講「何時切」、本 skill 的 `playwright-in-loop` 講「切了之後具體寫什麼 query」。

`requirement-protocol/clarifying-ambiguous-instructions` 的「類型 5：篩選類」跟本 skill 的 `data-flow-and-filter-composition` 互補：上層講「該怎麼澄清」、本層講「澄清完該怎麼實作」。

---

## 相關抽象層原則

本 skill 的協議建立在幾條抽象層原則上（檔案位置：`references/principles/`）：

- [#42 2 次門檻](references/principles/two-occurrence-threshold.md) — 第 1 次失敗是運氣、第 2 次是訊號（playwright 切換時機的根據）
- [#43 最小必要範圍](references/principles/minimum-necessary-scope-is-sanity-defense.md) — selector / observer / 操作邊界從窄起（DOM 設計、Reactive 效能的根據）
- [#44 SSOT](references/principles/single-source-of-truth.md) — 值的住址只能一處（CSS 變數、量測一致性的根據）
- [#45 外部組件合作四層](references/principles/external-component-collaboration-layers.md) — 離公共介面越近越穩（framework 共處的根據）
- [#64 同層合成](references/principles/compose-feature-at-source-layer.md) — Stream 操作必須跟 materialization 同層（Filter × Source 的本質）
- [#67 寫作便利度跟意圖對齊反相關](references/principles/ease-of-writing-vs-intent-alignment.md) — 容易寫的位置通常是錯位的位置（meta-principle、解釋為什麼層錯位 / 寬 selector / inline style 等便利寫法都會出問題）
- [#68 驗收的時間軸：四個 checkpoint](references/principles/verification-timeline-checkpoints.md) — Layout test 屬 Ship 前 checkpoint 的具體做法
- [#69 Test-First：先看到 RED 才相信 GREEN](references/principles/test-first-red-before-green.md) — Playwright 測試的驗證協議：寫完測試 + 第一次跑就 GREEN 是警訊、要先在 buggy code 上看到 RED 才相信測試 catch 到該 catch 的東西
- [#70 URL 是 stateful UI 的儲存層](references/principles/url-as-state-container.md) — 互動式 UI 的可分享 / 可恢復 / 可導航 state 該寫進 URL（搜尋 / filter / tab / sort / pagination 都該檢視）
- [#71 Tab Order = DOM Order = Mental Model 三者對齊](references/principles/tab-order-mental-model-alignment.md) — DOM 順序預設 = tab 順序、不對齊時優先重排 DOM、tabindex > 0 是反模式
- [#72 高 ROI 無外部觸發的工作會被結構性跳過](references/principles/external-trigger-for-high-roi-work.md) — meta-原則：寫測試 / refactor / a11y review / Ship 前 case 設計都需要外部觸發（CI / pre-commit / PR template）、不是靠紀律
- [#73 搜尋引擎的匹配模式跟使用者預期的對齊](references/principles/search-engine-matching-mode-mismatch.md) — Search feature 的 capability 維度：prefix vs substring vs fuzzy vs semantic 各自取捨、預設多為 prefix（為 index size）、跟使用者預期不對齊 = silent 失敗
- [#79 決策對話的五維度](references/principles/decision-dialogue-dimensions.md) — 設計取捨呈現給使用者時的 meta-框架（呈現 / 策略疊加 / 批次 / 時間 / 選項類型）— 「設計取捨段落」常用的五策略表 + 推薦 + 「先 ship X、Y 下輪」就是這五維度的展現
- [#82 字面攔截 vs 行為精煉](references/principles/literal-interception-vs-behavioral-refinement.md) — playwright 測試是字面驗證（input → output 比對）、抓不到「為什麼這個 selector 設計錯」這類行為錯誤、需要 multi-pass review 配合

---

**Last Updated**: 2026-04-26

版本紀錄在同目錄的 `CHANGELOG.md`。
