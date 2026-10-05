---
name: content-extension-evaluation
description: "寫完核心章節 / 教學模組後評估「該補哪些延伸內容」的標準流程。產出 6 軸候選 + ROI 矩陣 + 立即補 / backlog 排序、避免完美主義 collapse 跟覆蓋率不足兩種反向誤判。觸發詞：延伸評估、補章節、章節後續、評估缺口、規模成長後續、extension 候選、內容後續、模組完成評估、長期維護、知識卡缺口、跨章整合、vendor 深入。Trigger when evaluating what extensions to add after completing a batch of teaching chapters."
license: MIT
metadata:
  version: 1.1.2
  category: writing-methodology
---

# Content Extension Evaluation

寫完核心章節 / 教學模組後、評估「該補哪些延伸內容」的標準流程。產出 6 軸候選 + ROI 矩陣 + 立即補 / backlog 排序、避免「完美主義 collapse」跟「覆蓋率不足」兩種反向誤判。已在 backend 模組驗證、評估 5 章 + 1 report 卡的延伸潛力、產出 3 章高 ROI 延伸 + 8 個跨章整合段。

## 適用情境

- **核心章節已完成**：3+ 章新章節寫完、想知道接下來補什麼
- **多輪 review 已修完**：[`multi-round-review`](../multi-round-review/SKILL.md) 跑完、章節品質穩定、可以評估延伸
- **時間 / context 有限**：不能全寫、需要排優先序
- **長期累積場景**：教學模組、規範文件、需要持續演進的內容

不適用：

- **單篇文章**：無「延伸」概念、修完就結束
- **快速迭代原型**：延伸評估的固定成本（盤點 6 軸 + 排優先序）對原型 ROI 低
- **核心章節未寫完**：先寫核心、再做延伸評估

## 評估的 6 個軸

每軸代表一種「該不該補」的不同角度。批量評估時不是選一條軸、是 6 軸都盤過、再整合排序。

### 軸 A：讀者旅程覆蓋

已開出的學習路線（如「規模成長」「API 到資料流」）是否都被新章節覆蓋？既有路線是否需要更新章節清單以納入新章節？

判讀問題：

- 新章節進入哪幾條既有路線的「建議順序」？
- 既有路線是否仍能順讀完？章節之間有沒有銜接斷層？
- 是否需要新開一條路線？

### 軸 B：Module-level 結構一致性

各模組（00 / 01 / 02 / ...）的章節數、深度、子分類是否一致？

判讀問題：

- 哪個模組章節數超過 20、可能需要 sub-cluster 化？
- 新章節編號跟既有章節順序是否合理？
- 模組 _index.md 章節清單、學習路線、跨模組路由有沒有遺漏？

### 軸 C：Skill / 方法論抽取

寫作過程累積的方法論（reviewer workflow、評估流程、特殊寫作技巧）是否值得抽成正式 skill？

判讀問題：

- 哪些工作流跨越多個 batch、可重用？
- 哪些原則目前散落在多張 report 卡、可以包成 skill 集中觸發？
- 是否需要建 sibling skill（如多輪 review、延伸評估）？

### 軸 D：Knowledge card 剩餘缺口

新章節提到但無對應卡片的概念清單。

判讀問題：

- 哪些概念在多章使用、缺卡造成讀者重複看內聯解釋？
- 哪些概念複雜到值得獨立卡、不適合內聯？
- 卡片建立優先序：高頻 + 跨章 + 概念穩定（不易過時）

### 軸 E：Vendor / Deep article 缺口

新章節提到的具體工具 / vendor 是否有對應 deep article？

判讀問題：

- 哪些 vendor / 工具被多個章節引用、缺 deep article 造成讀者跳出？
- 哪些 vendor 對照已寫、deep article 是延伸？
- Vendor deep article 是長期 backlog、優先序通常低於知識卡

### 軸 F：長期維護風險

新章節有哪些內容會隨時間過時？

判讀問題：

- 哪些 vendor 名稱 / 服務 / 規格會變？半衰期多久？
- 哪些性能數字 / 計價 / 配額會更新？
- 是否需要設「定期 audit」mechanism、誰負責、用什麼訊號觸發？

## 標準流程

### Step 1：6 軸盤點

對每個軸、列出候選清單：

```text
軸 A 讀者旅程：
  - [候選 1] 路線 X 缺新章節 Y
  - [候選 2] 路線 Z 銜接斷層

軸 B 模組結構：
  - [候選 3] 模組 N 章節數 22、考慮 sub-cluster

軸 C Skill 抽取：
  - [候選 4] 方法論 P 已驗證、可抽 skill

軸 D Knowledge cards：
  - [候選 5-12] 8 個缺卡概念

軸 E Vendor deep articles：
  - [候選 13-17] 5 個 vendor deep article 候選

軸 F 維護風險：
  - [候選 18-20] 3 個半衰期 < 12 個月的內容
```

### 附帶檢查：兜底資料夾主題浮現

6 軸盤點同時掃兜底資料夾（如 `other/`）：有沒有 3+ 篇同主題文章、且文章之間有相互引用？有的話、建立新分類列入延伸候選。分類是內容累積到臨界量後的自然產物、不是事先規劃的空架子。詳見 [category-emerges-from-depth](references/principles/category-emerges-from-depth.md)。

### Step 2：每個候選評估「成本 × 價值」

| 候選   | 成本 | 價值 | 急迫度 |
| ------ | ---- | ---- | ------ |
| 候選 1 | 中   | 高   | 立即   |
| 候選 2 | 低   | 中   | 短期   |
| ...    | ...  | ...  | ...    |

- **成本**：寫作 / 修改 / 維護成本（低 / 中 / 高）
- **價值**：補完後對讀者的影響（低 / 中 / 高）
- **急迫度**：立即補 / 短期 backlog / 長期 backlog / 不補

### Step 3：用 AskUserQuestion 跟用戶確認方向

不要直接全部做。延伸內容範圍可能很大、需要用戶決策。

問法範例：

```text
評估完 N 個候選、按 ROI 矩陣排序：

最高 ROI：[3-5 個]
短期 backlog：[5-8 個]
長期 backlog：[多個]

要怎麼處理？
A. 推薦高 ROI 立即補
B. 只補跨章整合段（低成本）
C. 全部補
D. 全部留 backlog
```

### Step 4：執行 + 整合 + commit

依照用戶選擇執行。每類延伸可獨立 commit：

- 新章節：1 commit / 章
- 跨章整合段：合 1 commit
- Knowledge card：合 1 commit
- Skill：1 commit / skill

每個 commit 帶清楚的 ROI 理由。

## 避免兩種反向誤判

### 誤判 1：覆蓋率不足（提早收尾）

- 「核心章節寫完就好」、不評估延伸
- 結果：讀者撞到「框架已給、執行缺位」、要自己 google
- 防範：強制走 6 軸盤點、確認沒有 systemic 缺位

### 誤判 2：完美主義 collapse（無止境疊代）

- 全 6 軸所有候選都做、ROI 邊際遞減
- 結果：時間 / context 用光、後續核心章節無法開工
- 防範：用「修法成本反轉訊號」判讀（per [`multi-round-review` 的停止訊號](../multi-round-review/references/principles/cross-round-stopping-signal.md)）— 修一個延伸的成本超過讀者實際感受價值、就停

兩個誤判的本質是 collapse 在反向。延伸評估的價值在「主動規劃延伸範圍、不交給直覺」。

## 跟其他 skill 的關係

- [`multi-round-review`](../multi-round-review/SKILL.md)：在 multi-round-review 完成後啟動本 skill。Review 抓「現有章節有什麼問題」、延伸評估抓「應該還補什麼」。
- [`case-first-module-workflow`](../case-first-module-workflow/SKILL.md)：本 skill 接在 case-first Stage 5 polish pass 之後、作為「模組視為完成前的最後評估」步驟。
- [`compositional-writing`](../compositional-writing/SKILL.md)：本 skill 不重複其原則、評估結果中的「新章節候選」會回到 compositional-writing 規範寫。

## 反模式

- **直接寫延伸不評估**：看到一個 idea 就寫、沒走 6 軸盤點、容易補了低 ROI 的東西、漏了高 ROI 的東西
- **評估完不問用戶**：自己決定全寫、用戶可能只想補一小部分
- **把延伸當「強制要做」**：6 軸盤點是「有候選」、不是「必須補」。多數 backlog 就是 backlog、不該逼自己做完
- **跳過 ROI 矩陣**：列出 N 個候選但沒分立即 / backlog、結果用「先做最容易的」直覺執行

---

版本紀錄在同目錄的 `CHANGELOG.md`。
