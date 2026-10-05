---
name: ux-design-evaluation
description: "UX / UI 設計的系統性評估：把「使用者被困住」類缺口從實機測試提前到設計階段。六維度各有可機械執行的表格——畫面狀態矩陣、gate fallback、輸入機制、錯誤恢復、導航、互動回饋，空白格即缺口。觸發詞：UX 設計、狀態矩陣、退出路徑、死胡同、gate、IME、錯誤訊息、retry、降級、deep link、back 行為、spinner、SnackBar、選中態、溢出。Do NOT use for 元件級契約（用 component-contract-design）。"
license: MIT
metadata:
  portable: true
  version: 1.11.14
  category: ux-design
---

# UX Design Evaluation

UX / UI 設計的系統性評估方法。這個 skill 的出發點是一類反覆出現的事故：功能邏輯完整、實機測試才發現使用者被困在畫面裡出不去、按鈕按了沒有任何回饋、Face ID 失敗後沒有替代路徑。加一顆 back 按鈕是 5 分鐘的事，問題在設計階段沒有工具強制回答「每個狀態怎麼離開、每道關卡失敗怎麼辦、每個動作使用者怎麼知道系統收到了」。

本 skill 把 UX 設計從「靠經驗想到」變成「靠方法查到」：每個評估維度都有可機械執行的表格或提問清單，填完表格、空白格自動暴露缺口。適用於任何前端 surface（mobile app、web、桌面），範例以 mobile 為主。

**兩件事不在本 skill，但各有去處**——寫明去處是因為「不涵蓋」若沒有下一句，讀者會停在這裡：視覺風格（品牌色、字型階、間距階）屬 design token 體系，走 `foundation-design` skill 的 UI 維度，其執法層在 Dart 專案是 `dart-style-guardian` skill；使用者研究方法（訪談、可用性測試、問卷）本框架目前無承接者，需自行取用外部方法。**可讀性對比（WCAG）是例外，它屬本 skill 的互動回饋檢查範圍**，不要因為它看起來像視覺風格就轉出去。

---

## Core Pillars（核心支柱）

| 支柱                                               | 意義                                                                               |
| -------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Every state has an exit** 每個狀態都有退出路徑   | 畫面的每個狀態至少一條使用者可自行觸發的離開路徑；退出路徑為空 = UX 死胡同         |
| **Every gate has a fallback** 每道關卡都有替代路徑 | 使用者過不了關卡（認證失敗、斷網、權限被拒）時仍有路可走，而非被擋死               |
| **Every action gets honest feedback** 回饋即時誠實 | 每個使用者動作都有與等待時長相稱的系統回應；沒有回饋的按鈕等同壞掉的按鈕           |
| **Design decisions are artifacts** 設計決策成品化  | 狀態矩陣、gate 設計表、輸入決策表在企劃階段產出、可被 review、可直接轉成 test case |

---

## 評估流程

### 設計新畫面 / 新流程時（事前）

1. 從操作盤點（BDD 情境或功能規格）列出所有畫面與狀態
2. 每個畫面填**畫面狀態矩陣**（四欄：顯示 / 可用操作 / 進入條件 / 退出路徑）— 空白格就是設計缺口
3. 每道 gate 回答成功 / 失敗 / 不確定必答問題、產出 gate 設計表
4. 每個輸入框過輸入機制決策（keyboard type / submit model / IME policy / special keys）
5. 每個非同步操作標時間門檻帶、決定回饋形式
6. 每個導航操作回答「使用者按 back 期望回到哪裡」

畫面狀態矩陣填完、進入元件級實作前：每個元件契約欄位表齊全、容器排列不變式的填寫由 `component-contract-design` skill 承接（本 skill 只到畫面級狀態，不含元件層契約）。

### 審查既有 UI / UX review 時（事後）

依症狀路由到對應 reference（見下表），用該 reference 的檢查清單逐項掃。跨維度的快速掃描順序：先掃退出路徑（被困住的代價最高）、再掃 gate fallback、再掃回饋完整性。

---

## 觸發路由

| 觸發情境 / 症狀                                                                                                                                                                                                 | 讀哪份 reference                     |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| 設計多狀態畫面（連線 / 配對 / 同步）、使用者被困在畫面出不去、畫面剛開啟就顯示離線、審查導航缺口、路由存在但入口找不到                                                                                          | `references/screen-state-matrix.md`  |
| 設計認證 / 網路 / 權限 / 硬體條件關卡、生物辨識失敗沒退路、權限被拒後的處理、覆蓋 / 清空既有資料的操作確認、模擬器上測不到的 gate                                                                               | `references/gate-fallback.md`        |
| 設計輸入框 / 表單 / 搜尋框 / CLI 輸入、鍵盤自動校正破壞輸入、密碼或 secret 欄位、驗證時機選擇                                                                                                                   | `references/input-mechanism.md`      |
| 撰寫錯誤訊息、設計重試機制、使用者卡在錯誤迴圈、錯誤畫面的行動過重（重載 / 重裝）、部分功能不可用的降級呈現                                                                                                     | `references/error-recovery.md`       |
| 選擇導航模式（stack / tab / drawer）、go vs push 的選擇、back 行為不符預期、hash SPA 的頁面辨識、deep link 設計                                                                                                 | `references/navigation-patterns.md`  |
| 按鈕按了沒反應、重複提交、佔位 handler 假按鈕、宣告完成但資料不全、loading 該不該顯示、spinner vs skeleton、通知該用 SnackBar 還是 Dialog | `references/interaction-feedback.md`（按鈕流程與狀態）+ `references/interaction-feedback-waiting-and-notification.md`（時間門檻、spinner/skeleton、通知形式） |
| 點到的是狀態圖示卻沒反應、切換鈕標籤被讀成現態、選中看不到字、文字被壓成省略號、水平清單溢出無捲動提示 | `references/interaction-feedback-component-semantics.md` |

每份 reference 自包含：不讀 SKILL.md 與其他 reference 也能獨立套用；`interaction-feedback` 家族四檔互相具名指路，見各檔檔頭。

---

## 跨維度快速自檢

任何 UX / UI 變更提交前的最小檢查（細項在各 reference 內）：

- [ ] 新增或修改的畫面：每個狀態都有至少一條退出路徑？
- [ ] 涉及 gate（認證 / 網路 / 權限）：失敗與不確定路徑都有設計？
- [ ] 涉及輸入框：keyboard type 與 IME policy 是明確決策而非預設值？secret 類欄位過了 IME 安全清單？
- [ ] 涉及非同步操作：按鈕有 loading + disabled + 恢復？結果有通知？
- [ ] 涉及錯誤畫面：除了重試還有第二條路（返回 / 替代方案）？
- [ ] 涉及導航：go / push 的選擇對照過「按 back 期望回哪裡」？
- [ ] 通知形式對照過「是否需要使用者操作 × 干擾程度」二軸？
- [ ] 畫面查詢的對象有獨立生命週期（service worker / 遠端服務）：initializing 與離線分開建模？
- [ ] 批次 / 遍歷操作的完成宣告有窮盡證據？
- [ ] 跨 context 的結果通知有端對端驗證？
- [ ] 覆蓋 / 清空既有資料的操作：有後果確認 + 確認機制故障時的安全預設？
- [ ] 切換元件標籤是動作語意（或已拆成狀態顯示 + 動作按鈕）？
- [ ] 非互動指示與按鈕形態可區分、選中態對比成對設計？
- [ ] 關鍵回饋文字有版面保障（窄幕驗收）？
- [ ] 靠顏色區分的語意，顏色之外另有訊號或文字？
- [ ] 無佔位 handler（dev toast / log-only）殘留？

---

## Directory Index

```text
ux-design-evaluation/
├── SKILL.md                              # 本檔：支柱 + 評估流程 + 觸發路由
└── references/
    ├── screen-state-matrix.md            # 畫面狀態矩陣：四欄定義、填寫、BDD 展開、路由可達性、happy-path 反模式（入口，同組見下）
    ├── screen-state-matrix-selection-prestate.md  # 選取類前置呈現：獨立成列與判定條件
    ├── gate-fallback.md                  # Gate 分類、成功/失敗/不確定必答問題、biometric/network/permission、dev vs 真機差異
    ├── input-mechanism.md                # 輸入機制四維決策、表單/搜尋/CLI 場景、IME 安全清單
    ├── error-recovery.md                 # 錯誤訊息兩職責、retry 策略、error loop 逃生口、degraded mode
    ├── navigation-patterns.md            # 導航模式分類、go/push/pushReplacement 語意、平台慣例差異、deep link
    ├── interaction-feedback.md           # 回饋三層模型、按鈕級回饋（按鈕流程與狀態）（入口，同組見下）
    ├── interaction-feedback-waiting-and-notification.md  # 時間門檻、畫面級回饋、spinner vs skeleton、通知形式選擇
    ├── interaction-feedback-component-semantics.md        # 元件語意與版面：切換標籤、可點性、選中態、溢出、版面保障
    └── interaction-feedback-checklist.md                  # 互動回饋反模式速查、檢查清單、參考來源（三檔共用）
```

---

## 與相鄰資產的交界

執行時不需要先讀本節。不確定某件事該由本 skill 還是相鄰資產處理時再查。

| 相鄰資產 | 它管什麼 | 交界落在哪 |
|---------|---------|-----------|
| `component-contract-design` skill | 元件級契約：元件契約欄位表、容器排列不變式 | 本 skill 只到**畫面級狀態**。同一類失效在那邊寫成契約欄位（內容政策、空間不足策略）而非審查項。**本 skill 判定的回饋時間門檻與通知形式，是它填回饋契約時的輸入**——它不重新判斷門檻，所以本 skill 的產出必須是可被引用的具體值，不能只寫「要有回饋」 |
| `foundation-design` skill | 地基入口與路由；design token 體系是它 UI 維度的產物 | 品牌色、字型階、間距階在那裡定義。本 skill 的 `interaction-feedback-component-semantics.md` 談對比與版面保障時**消費那些階，不新增階**——需要一個不存在的色階或字級時，那是地基缺口，回去建票而不是在畫面設計裡就地決定 |
| `dart-style-guardian` skill（Dart／Flutter 的執法工具） | 掃裸色碼、裸間距、裸字級、寫死文字 | 它只看程式碼字面。**「按鈕沒有 loading 態」「選中態對比不足」它掃不到**——那些是本 skill 的檢查項，執法工具全綠不代表本 skill 的自檢清單過了 |
| `version-bootstrap` skill 地基波 | 編排 i18n → design-system → UX 審查 → 元件庫四塊的順序 | 本 skill 是第 3 塊。**它的輸入是前兩塊（i18n 與 design-system）已完成**——token 與文案 key 還沒有時，本 skill 產出的回饋設計會指向不存在的值 |

### 三段鏈式範例：本 skill 的產出必須是可被引用的具體值

情境：一個非同步操作，`component-contract-design` skill 填元件契約〈回饋契約〉欄時需要一個明確的時間門檻與回饋形式，而非本 skill 自行留白讓對方猜。驗證段的判定屬「設計產出物」（判定規則：產出物能在執行期被啟動、看得到它運作的屬執行期行為，驗證段寫 Given/When/Then；契約表、判定結果這類靜態文件屬設計產出物，驗證段寫檢驗問句加預期答案）。

【輸入】

```
SPEC 片段：一個非同步查詢操作，由按鈕觸發，實測延遲 p90 為 600ms
```

【產出】

```
形態：決策表
判斷依據                       | 結果
600ms 落在 `interaction-feedback-waiting-and-notification.md`〈時間門檻與回饋策略〉哪個帶 | 400ms-1s（短暫等待）
該帶對應的回饋策略             | Spinner／按鈕 loading 狀態
結論                           | 回饋契約表「等待與結果」列：時間門檻欄填「p90 600ms
                                 （400ms-1s 帶）」，選用的統計量隨值標明；反應欄的等待段
                                 填「按鈕 loading 狀態」。反應欄須同格涵蓋的成功／失敗／
                                 逾時／服務不可用四段，由 `interaction-feedback-waiting-
                                 and-notification.md`〈結果通知的形式選擇〉產出，不在本例
                                 範圍；回饋通道欄由規格撰寫者填，本 skill 不填
```

【驗證】

```
檢驗問句
Q 本 skill 產出的「反應欄等待段」是否為封閉列舉中的具體值？
  預期：是——「按鈕 loading 狀態」是 `interaction-feedback-waiting-and-notification.md`〈時間門檻與回饋策略〉表已定義的策略之一，
  `component-contract-design` 可直接引用，不需要再判斷一次門檻
Q 產出是否停留在「要有回饋」這類抽象敘述？
  預期：否——停在抽象敘述等於把門檻判斷丟回給填寫元件契約的人，
  兩位不同的填寫者可能各自選出不同的回饋形式，產出分岔
```

---

**Last Updated**: 2026-09-16

版本紀錄在同目錄的 `CHANGELOG.md`。
