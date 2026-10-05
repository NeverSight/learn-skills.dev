---
name: case-first-module-workflow
description: "Case-first + Agent team review 五階段流程、寫跨多章節教學模組（5+ 章、有 case 庫）時用。觸發詞：教學模組、case-first、case-driven、stage 1/2/3/4/5、agent team review、polish pass、fact vs derive、reviewer prompt、SSoT 對應、frame 重複、skeleton case vs rich case、case fidelity、自掃描 regex、模組擴章。Trigger when writing teaching modules across multiple chapters with an existing case library."
license: MIT
metadata:
  version: 1.7.2
  category: writing-methodology
---

# Case-First Module Workflow

跨多章節教學模組（5+ 章）撰寫的六階段流程（stage 0 採集 + stage 1-5 audit / write / review / fix / polish）。用真實案例驅動 scope 擴展、用 agent team 平行多輪審查補 LLM 自盲點、用 polish pass 處理系統性殘留。已在 7 個模組驗證、385 個 review issue / case fidelity 70-93% 區間。

Stage 0 是後加入的階段、來自 backend/03-message-queue 模組的 6 vendor case 庫採集經驗 — 既有 stage 1-5 假設「case 庫已存在」、但實作上常碰到 case 庫從零或覆蓋不足、需要先採集再進 audit。

## 適用情境

- **長期累積的教學模組**：5+ 章、跨章引用密集、規範遵循重要
- **有現成 case 庫**：案例庫含 rich case（具體數字 / 設計細節）跟 / 或 skeleton case（方向骨架）
- **品質高於速度**：完整五階段約 4-6 小時 / 模組、適合長期累積的內容、不適合 one-off 文章
- **主 context 容量敏感**：reviewer 平行 background 是節省 context 的關鍵設計

不適用：

- **新主題沒案例庫**：要先建案例庫、不能直接套這流程
- **單篇短文**：流程的固定成本（讀案例 + 跑 reviewer）對短文 ROI 低
- **快速迭代原型**：流程偏向 *寫一次寫好*、不是 *快速修改*
- **Routing layer / 導讀性質章節**：已含完整 threat scope + 引用標準 + 問題節點表、case 庫不對應或缺位、應跳過本流程、用標準引用 + 通用工程知識補充承接
- **Standard framework 比 case 庫成熟的領域**（07 LLM 章節驗證）：當該領域的 *標準框架*（如 OWASP LLM Top 10 / NIST AI RMF / MITRE ATLAS）已涵蓋 threat 分類、且 case 維護半衰期短於 standard（領域演進快、6 個月可能過時）、章節應 *用 standard-driven 取代 case-driven*、加 `Last reviewed: YYYY-MM-DD` cadence。Standard-driven 跟 case-driven 是平行選項、沒有退化 / 進階關係。詳見 [standard-driven 取代 case-driven](#standard-driven-vs-case-driven) 段。

## Standard-driven vs case-driven

判斷該用哪種策略、看領域的兩個性質：

| 領域性質        | Case-driven 適用              | Standard-driven 適用            |
| --------------- | ----------------------------- | ------------------------------- |
| 議題穩定度      | 高（5+ 年穩定）               | 低（< 1 年快速演進）            |
| Case 公開度     | 高（充分的事故公告）          | 中或低（vendor 偏 marketing）   |
| Standard 成熟度 | 中（多用 case 而非 standard） | 高（standard framework 已成型） |
| 維護半衰期      | 長                            | 短（6 個月過時）                |

典型 case-driven 領域：分散式系統 / 安全控制面 / 可靠性 / 訊息佇列。
典型 standard-driven 領域：LLM 安全（OWASP LLM Top 10）、新興 compliance（NIST AI RMF）、cloud-native 標準（CNCF baseline）。

Standard-driven 章節的寫作策略：

1. **章節對齊 standard framework 分類**、用 framework 章節 ID 標明（如 OWASP LLM01 / NIST AI-1.1）
2. **加 Last reviewed cadence**：每 quarter 重評估 standard 版本跟章節對應
3. **「案例觸發參考」段標明「公開案例累積中、值得追蹤的方向」**、不寫「對應 [case] 揭露」斷言
4. **引用標準時用版本號**（OWASP LLM Top 10 2025 / NIST AI RMF 1.0）、framework 改版要 trigger 章節重審

何時要從 standard-driven 轉回 case-driven：

- 該領域累積 5+ 個高可信度 case（vendor disclosure + academic + CVE 三來源交叉）
- 跨章 frame 重複出現、case-driven mechanism 深化能解 SSoT 衝突
- 出現「等級類似 SolarWinds」的 incident、案例本身夠重、單一 case 即可支撐章節擴章

實證：07 batch 2 LLM 安全 5 章驗證此策略 — 章節 113-137 行、含完整 threat scope + 問題節點表 + 風險邊界、引用 OWASP LLM Top 10 + NIST AI RMF + MITRE ATLAS 取代個別 case 引用、加 `Last reviewed: 2026-05-12` cadence、完全不寫「對應 [case] —」斷言。scope 涵蓋真實 production 議題（KV cache 跨租戶、shared prefix optimization、batch 推論順序敏感）、品質跟 case-driven 章節同等。

## 三大支柱

| 支柱                     | 意義                                                               |
| ------------------------ | ------------------------------------------------------------------ |
| **Case-driven scope**    | 用真實案例 findings 驅動「該寫什麼」、不是 LLM 從訓練資料自生      |
| **Agent team review**    | 3 個專責 reviewer 平行 background 跑、各維度獨立、不污染主 context |
| **Pattern-aware polish** | 系統性 pattern（負向骨架、模板化）跨檔批次處理、不一個個改         |

## 六階段流程

### Stage 0：案例採集（從零或補強建 case 庫）

當 case 庫從零、或既有 case 庫覆蓋不足某些章節 / vendor / 主題時、走 stage 0 採集流程。

關鍵紀律：

- **平行 agent 採集**：spawn N 個 `subagent_type: general-purpose`、`run_in_background: true` agent、每個負責一個 vendor / 主題、各自跑 WebSearch + WebFetch
- **WebFetch 驗證硬閘門**：每個 URL 都要 WebFetch 確認可訪 + 內容真的提到目標 vendor / 主題、不能編造
- **採集目標 5-10 case per vendor**：含 anchor（1-3 個、覆蓋多議題）+ 邊緣（3-6 個）+ 反例（1-2 個）
- **薄殼形態**：採集只寫薄殼（觀察 + 判讀 + 對應大綱 + 引用源、~15-20 行）、不寫策略 / 詳細路由、後續 stage 1 audit 可升 rich
- **誠實標明缺口**：採集後在 `_index.md` 加「案例覆蓋缺口」段、明示哪些章節公開 case 稀薄

詳見 [stage-0-case-collection](./references/stage-0-case-collection.md) 跟 [stage-0-collection-checklist](./references/stage-0-collection-checklist.md)。對應 [principles/case-collection-coverage-gap](./references/principles/case-collection-coverage-gap.md)。

### Stage 1：案例庫 audit + findings 抽取

完整讀 case（不只 title + description）、邊際遞減判斷停止點、findings 帶 *case 來源* + *對應章節* + *case 類型* 標明。

關鍵紀律：**Skeleton / Medium / Rich case 三類分類** + **Fact vs Derive 分層**。詳見 [stage-1-case-audit](./references/stage-1-case-audit.md) 跟 [principles/case-type-discrimination](./references/principles/case-type-discrimination.md) + [principles/fact-vs-derive-layering](./references/principles/fact-vs-derive-layering.md)。

### Stage 2：基於 findings 建立內容

**寫作前 30 分鐘做 SSoT 對應**（這步不做必踩 frame 重複坑）：列出 cross-chapter findings、每個 frame 指定唯一主寫章節、其他章節只 link。跨模組層級概念 → 模組索引（module index、本 blog Hugo 結構下為 `_index.md`、其他靜態網站可能是 `README.md` 或 `index.md`）。

**承重論點先 steelman 再寫**（分析 / 合成型模組尤其）：模組若架在一個承重論點上——錯了會讓多章作廢或大改的核心宣稱（方法論主張、跨 case 合成 frame、核心分類假設）——在動筆寫依賴它的章節前，先對它跑一次對抗性挑戰（獨立 reviewer 或「預設它錯、逐條枚舉反例」的自我步驟）。承重論點常是「只有一組 X」「所有 Y 都 Z」的全稱 / 唯一性宣稱，別把「還沒找到反例」當「不存在反例」。這個 steelman 是生產閘門、跟 Stage 3 的收尾 steelman 不是同一件——只在 Stage 3 才挑戰承重論點＝太晚，錯誤已寫進 N 章、跨章回改成本 N 倍（同 cadence 抽樣「別等 reviewer」的邏輯）。同源自審對自己的地基有盲區、挑戰要交對抗 / 異源。

寫作時主動防範以下反覆陷阱（完整清單見「反覆陷阱」段、本段給寫作當下必須意識的核心條目）：

1. **負向陳述骨架**：避免「不是 X、是 Y」推進論證、避免「核心責任不是 X、而是 Y」變體段首
2. **模板化**：L1/L2/L3 三層、三選一表格、四步驟流程出現前先問「真的對等嗎？」
3. **首句結構**：每段首句先寫「這個概念是什麼、承擔什麼責任」、不是「對應 [case] 揭露 X」
4. **Case 引用三段式**（06 模組強化）：每處 case 引用要走「概念定義 → case 引用 → 通用展開」三段、case 引用不能取代段首概念定義。詳見 [principles/case-citation-three-part](./references/principles/case-citation-three-part.md)
5. **跨 case 合成 frame 必須標明**（07 模組新發現）：當段落把多個 case 的失效訊號抽象為更高層 frame（如「跨工具回查壓力」「平台責任切分」）、要 explicit 標為「本章合成、非 case 原文」、避免把章節 derive 包裝成 case 揭露。詳見 [principles/fact-vs-derive-layering](./references/principles/fact-vs-derive-layering.md)
6. **批量寫作 cadence 抽樣**（07 vendor batch 新發現）：寫 ≥ 5 個同類檔時、第 1-3 篇刻意產出 3 種 framing 變體（pilot phase）、進度 10-20% 跑跨檔抽樣（段首句 / 段末收尾語 / 過渡詞密度）、發現 cadence 同質化立即回頭加變體；不要等 Stage 3 reviewer 才發現連讀預期化、修正成本 N 倍。詳見 [principles/cadence-sampling-in-batch-writing](./references/principles/cadence-sampling-in-batch-writing.md)
7. **合成章只寫「一句話案例 + link」**（11 模組新發現）：合成型框架章（無專屬 case、從全庫推導）會把 anchor 案例的機制 / 清單 / 時序吸進來當例證、靜默反轉 SSoT map 的主寫方向；合成章引用案例只允許一句話結論 + 數字 + link 主寫章、初稿可最後寫或回頭壓縮。詳見 [principles/ssot-correspondence](./references/principles/ssot-correspondence.md) 的合成章硬規則段

寫完每章後 commit 一次或合併 commit。全部主章完成後、跑一輪 **回填輪**：大綱案例支撐欄、case 檔對應大綱欄、跟正文實際引用三方對照、機械性同步（詳見 [principles/ssot-correspondence](./references/principles/ssot-correspondence.md) 的寫後回填輪段）。

### Stage 3：Agent team 平行多輪審查

Stage 2 commit 後、平行 spawn 3 個 reviewer（`subagent_type: general-purpose`、`run_in_background: true`）：

- **Reviewer A**：寫作規範（AGENTS.md 八原則）— prompt 見 [reviewer-prompts/reviewer-a-standards](./references/reviewer-prompts/reviewer-a-standards.md)
- **Reviewer B**：案例引用準確性（對照原始 case、含 fact vs derive 分層）— prompt 見 [reviewer-prompts/reviewer-b-case-fidelity](./references/reviewer-prompts/reviewer-b-case-fidelity.md)
- **Reviewer C**：跨章一致性（重複 frame / cross-link / 邊界）— prompt 見 [reviewer-prompts/reviewer-c-consistency](./references/reviewer-prompts/reviewer-c-consistency.md)

**Review 七軸對照**（07 vendor batch 新發現）：Reviewer A/B/C 三個 instance 已 cover Frame / Instance / Granularity 主軸跟部分 Surface / Scope；**Cadence 軸 + Timing 軸** 不靠 reviewer 補、是靠 Stage 2 寫作流程內抽樣（pilot phase 變體 + 進度 10-20% 抽樣）。設計新 reviewer 維度時先列七軸對照表、看哪些軸由 reviewer 覆蓋、哪些由 Stage 2 補。詳見 [principles/review-multi-axis-completeness](./references/principles/review-multi-axis-completeness.md)。

**為什麼 background**：reviewer 要讀完整 commit + 案例 + 章節、自身 context 會被佔滿；用 background 把 reviewer context 跟主 context 分開、主 context 只接收精煉摘要、節省 ~80% context。

預期 issue baseline：

| Reviewer 維度          | 範圍            | 備註                                                                                                                                                                    |
| ---------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Standards reviewer     | 20-45 issue     | 規範八原則、含「不是 X 而是 Y」變體段首、06 揭露「case 引用段首」、07 揭露「case 引用句構同質化」新 pattern                                                             |
| Case fidelity reviewer | 6-20 issue      | 準確率 70-93%、skeleton case 多會擴 over-extrapolation、medium case 多會擴實作層、rich case 多會混淆 fact vs derive、跨 case 合成 frame 易升級成 case 揭露（07 新發現） |
| Consistency reviewer   | 13-18 issue     | 跟章節數 / 跨模組密度成正比                                                                                                                                             |
| **總計**               | **47-71 issue** | 7 模組範圍（baseline 隨 standards reviewer 抓的 pattern 變多而擴大）                                                                                                    |

### Stage 4：修正循環

按嚴重度修：critical 編造 → high frame 重複 / fact-derive 錯位 → medium 規範 / 路由 → low polish。

按 *檔案批次* 修、不是按 issue 編號順序。每個檔案修完跑一次 `mdtools fmt --fix` + `mdtools cards` + `mdtools lint`、確認該檔內部一致、再進下一檔。最後跑跨檔驗證、確認 cross-link 全部對齊。

**每個 issue 修完之後，掃的是那一類、不是清單上的那幾行**（per [principles/fix-the-class-not-the-cited-instances](./references/principles/fix-the-class-not-the-cited-instances.md)）。reviewer 列出的是它抽樣到的位置，而清單的形式（位置、原文、嚴重度、建議修法）在暗示完整性，於是「按嚴重度修完清單」被讀成「處理完問題」。修完用該 issue 的特徵字串掃整批章節——命中歸零、或剩下的都逐處判定合規，才算這一條處理完；掃描指令先拿一個已知會命中的字串驗過管道。沒有穩定關鍵詞的類別（frame 重複、fact-derive 錯位、論元結構）掃不出來，改派一輪限定 scope 的複掃、指令只說「找出這一類的全部位置」而不給已知的那幾處。**留下的舊實例比新引入的變體難抓**：新變體下一輪近 frame 撞得到，舊實例因為這一類已經回報過、後續輪次不再掃它。

預期成本 1.5-2.5 小時 / 模組。

### Stage 5：Polish pass

Stage 4 後仍會殘留 ~30-40% low / medium issue（負向骨架、編號漂移、cross-link 缺漏、模板化）— 屬系統性 pattern、跨檔批次處理。

詳細工序見 [stage-5-polish-pass](./references/stage-5-polish-pass.md) 跟自掃描 regex 集合 [self-scan-regex](./references/self-scan-regex.md)。

關鍵限制：

- **不重寫章節結構**：polish pass 是修得更貼合規範、不是重新組織
- **不擴大 scope**：polish pass 邊界 = stage 4 修改過的章節集合
- **不追求 0 issue**：保留 ~15 個 low 為下次擴章節時自然處理

預期成本 30-45 分鐘 / 模組。

## 模組執行的觸發路由

當使用者要寫跨章節教學模組時：

1. **先判讀領域該走 case-driven 還是 standard-driven**：對照「Standard-driven vs case-driven」段四維度（議題穩定度 / case 公開度 / standard 成熟度 / 維護半衰期）— standard-driven 領域不建 case 庫、直接用 standard framework 寫章節 + Last reviewed cadence
2. **確認 case 庫狀態**（case-driven 領域）：
   - 既有案例 5+ 篇且覆蓋目標章節 → 跳到 stage 1 audit
   - 案例 < 5 篇或部分章節缺案例 → **走 stage 0 採集**、補到 5-10 per vendor / 主題
   - 整個領域是 standard-driven → 跳過 case 庫、直接走章節寫作
3. 確認模組規模 5+ 章節 — 單篇文章用 [compositional-writing](../compositional-writing/SKILL.md) 即可
4. （case-driven 領域）按 stage 0 → 1 → 2 → 3 → 4 → 5 順序執行、不跳階段
5. 每個 stage 完成 commit 一次、保留可追溯歷史
6. 模組完成後做 retrospective、把新浮現 pattern 寫回方法論

## 反覆陷阱（必須主動防範）

7 個模組驗證後、以下陷阱在 *多數模組重複出現*、要在 stage 1-2 就防範、不能依賴 stage 3 reviewer 補救：

1. **Skeleton case 擴寫成 case 事實** — 詳見 [principles/case-type-discrimination](./references/principles/case-type-discrimination.md)
2. **Frame 重複展開（SSoT 不清）** — 詳見 [principles/ssot-correspondence](./references/principles/ssot-correspondence.md)
3. **負向陳述 + 模板化** — 詳見 [self-scan-regex](./references/self-scan-regex.md)
4. **Rich case 判讀層被當 case fact 引用** — 詳見 [principles/fact-vs-derive-layering](./references/principles/fact-vs-derive-layering.md)
5. **自掃描盲點累積** — 每個模組 reviewer 抓出新 pattern 後、回頭更新 self-scan regex
6. **Case 引用段首取代核心概念句**（06 模組新發現）— 詳見 [principles/case-citation-three-part](./references/principles/case-citation-three-part.md)
7. **Medium case 實作層擴寫過頭**（06 模組新發現）— 用 mechanism 名稱精準引用、不擴寫到 case 沒提的具體實作細節、詳見 [principles/case-type-discrimination](./references/principles/case-type-discrimination.md)
8. **跨 case 合成 frame 升級成 case 揭露**（07 模組新發現）— 當段落把多個 case 失效訊號抽象為更高層 frame（如「跨工具回查壓力」「平台責任切分」）、要 explicit 標為「本章合成、非 case 原文」。07 batch 1 reviewer B 的 2 個 high issue 都屬此類、發生在跨 case 合成場景。詳見 [principles/fact-vs-derive-layering](./references/principles/fact-vs-derive-layering.md)
9. **Case 引用句構同質化**（07 模組新發現）— 跨章 13+ 段 case 引用用同一句構（「揭露 N 層失效控制面 — A、B、C。案例『可落地檢查點』標明 mechanism 為 X、前提是 Y」）會讓讀者把 case 引用當儀式而非論證、stage 5 polish pass 要主動分流。詳見 [principles/case-citation-three-part](./references/principles/case-citation-three-part.md)
10. **採集階段編造案例**（backend/03 模組新發現）— LLM 會把訓練資料 + 真實公司名混合成不存在的案例、單純串行採集無法擋。Stage 0 必須 WebFetch 驗證 URL + 內容、agent 採集 prompt 要明示「不能編造、URL 失效要列入捨棄候選」。詳見 [stage-0-case-collection](./references/stage-0-case-collection.md)
11. **採集階段跨網域引用觸發 anti-phishing**（backend/03 模組新發現）— 第三方平台（Synadia 寫 NATS、CloudAMQP 寫 RabbitMQ）的 customer case 引用時、link display 含 vendor TLD 字樣會觸發 markdown lint anti-phishing 規則。採集 checklist 要驗證 display 跟 href domain 一致。詳見 [stage-0-collection-checklist](./references/stage-0-collection-checklist.md)
12. **採集階段全是正例、缺反例**（backend/03 模組新發現）— 採集容易偏向 success story（vendor 客戶 story、規模化案例）、忽略反例 / 退場 / 誤配案例。反例教學價值高於正例、每個 vendor 案例庫至少要有 1 個反例。詳見 [principles/case-type-discrimination](./references/principles/case-type-discrimination.md) 的「教學功能」維度
13. **跨檔 cadence 同質化**（07 vendor batch 新發現）— 寫 ≥ 5 個同類檔時、找到一個「都過 lint + 章節齊 + 表格深化」的 framing 後、批量會複製到所有檔；單篇合規、連讀預期化；屬 *emergence 違規*、規則化不了、不能丟給 Stage 3 reviewer 才發現（修正成本 N 倍）。Stage 2 進度 10-20% 必須抽樣 catch。詳見 [principles/cadence-sampling-in-batch-writing](./references/principles/cadence-sampling-in-batch-writing.md)
14. **Review 設計 collapse 到單軸**（07 vendor batch 新發現）— 「找一個 reviewer 跑就好」「跑一輪就好」「body review 就夠」這類便利選擇會 collapse 掉七軸中的某幾條（Cadence / Timing / Surface / Scope）、對應違規 systematic miss；設計新 reviewer 維度時要 enumerate 七軸覆蓋狀況、不是直接寫 prompt。詳見 [principles/review-multi-axis-completeness](./references/principles/review-multi-axis-completeness.md)
15. **外部分析文章被誤當 case fact** — analyst article / investor memo / industry commentary 是 source，不是 case 本體。Stage 0 若採集到這類材料，先用 compositional-writing 的 [source-to-teaching-analysis](../compositional-writing/references/source-to-teaching-analysis.md) 拆成事實、原作者判讀、本文推導；只有可驗證事實能進 case findings，原作者判讀只能當 hypothesis prior 或對照 frame。
16. **合成章的引力**（11 模組新發現）— 合成型框架章把下游主寫章的案例細節吸走、SSoT map 主寫方向被靜默反轉；實測 6 個 High 重複展開 issue 有 4 個同此根因。修法是合成章硬規則（一句話 + link）、詳見 [principles/ssot-correspondence](./references/principles/ssot-correspondence.md)
17. **預測性索引未回填**（11 模組新發現）— 大綱案例支撐欄與 case 檔對應大綱欄是 stage 0/1 的預測、正文完成後不回填就雙向失真、實測佔一致性 review 近半 issue（22 中 10）。正文完成後跑機械性回填輪、跟 lint 同級、詳見 [principles/ssot-correspondence](./references/principles/ssot-correspondence.md) 的寫後回填輪段

## 跟其他 skill 的關係

本 skill 跟 [compositional-writing](../compositional-writing/SKILL.md) skill 互補：

- compositional-writing 管 *單篇* 寫作的原子化跟意圖
- compositional-writing 的 [source-to-teaching-analysis](../compositional-writing/references/source-to-teaching-analysis.md) 管 *外部分析材料 → 教學文章* 的 source 分層與讀者降層；case-first 遇到 analyst source 時先跑這個前處理
- case-first-module-workflow 管 *跨章模組* 的 scope 跟一致性

跟 [requirement-protocol](../requirement-protocol/SKILL.md) skill 互補：

- requirement-protocol 管 *對話協議*（澄清需求、確認方向）
- case-first-module-workflow 管 *內容生產*（5 階段執行）

---

版本紀錄在同目錄的 `CHANGELOG.md`。
