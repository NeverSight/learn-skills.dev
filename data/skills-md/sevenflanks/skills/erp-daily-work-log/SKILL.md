---
name: erp-daily-work-log
description: 使用者要求將每日工作證據填寫、補新增或替換到 SoftLeader ERP 本人工作日誌時使用；含請假、個人偏好與獨立授權的共用 repo mapping 維護。
license: MIT
metadata:
  author: sevenflankse
  version: 0.4.2
---

# ERP Daily Work Log

以 `daily-work-log` 證據填寫本人指定日期日誌；一般摘要使用上游 skill。回報採短句與條列，先交代具體結果；只列新發現、必要選擇、結果、實際缺口及待決事項，合併同輪問題並省略重複的流程敘述。

**只維護共用 mapping**：直接讀 [mapping-save.md](references/mapping-save.md)，不進日誌／請假／collector 步驟。同時有日誌任務時，其 deadline、全天假或未知請假 gate 只控制日誌分支，獨立授權的合法維護仍可進行。

## 1. 固定日期與操作

1. 固定 `reportDate`（預設今天、`Asia/Taipei`），context、collector、mapping、options 及讀回均用該日。補報不改今天。
2. 從 runtime 發現並載入外部 `erp` skill，依其 access 指引解析 config root、認證及 resolved base URL。每次新執行先讀部署官方 OpenAPI：context、submit／replace、必要 options／resolver 的 operation、security、參數、回應及 `$ref`；能力以部署為準。[helper 契約](references/helper.md) 不是部署宣告。認證失敗、未知 state、context／必要 schema 缺口停止，不猜欄位或部署、不修改外部 readonly guard。ERP 查詢一律用該 skill 的唯讀工具。
3. GET 本人同日完整 context（可取代 exists），核對日期、existing details、snapshot、PROCESS/PASS 每日實際假時、打卡及服務端 `+08:00` 時間／次日 10:00 期限。**已知整日請假先 stop**，不 collect、不寫 LEAVE 或工作日誌。
4. 按意圖分流：
   - **首次填寫／補新增用 append**：官方 `POST /api/v2/daily-reports` 可用時，已有日誌仍追加，只送新列。10 點與 `canReplace=false` 不阻擋 append。相同 project＋module／RD 立案書與 existing 或新列衝突時先問；不得默默合併、改歸屬或覆寫 existing。
   - **明確替換意圖才 replace**：官方 `/replace` 可用且在期限內才進行；已有列的覆蓋授權獨立保留。「直接提交」不等於覆蓋。只有當次明確「直接覆蓋並提交」等完整授權才略過覆蓋詢問。
   - **所需 operation 不可用，或 replace 已逾期則 output_only**：直接到第 3 步，不問覆蓋／未知工時／branch／模組，不產生 rows 或 preview。不能為繞期限把替換意圖改成追加。若部署只有 replace 且未逾期，先確認替換意圖及必要覆蓋授權；只有 replace 且已逾期也走 output_only。

同任務、同日已核對的唯讀準備，在契約／options／選擇未漂移時沿用；handoff 或使用者簡稱不等官方 label 本身不構成重查理由。

日誌主題選定後、ERP preview 前，依 [`daily-work-log` issue-state 補證規則](../daily-work-log/SKILL.md#workflow) 核對會影響成果／待辦的明確引用 issue；只刷新因新證據或失效而受影響的查詢。若補證改變日誌內容／意圖，依第 5 節直接呈現同 plan 的 `--preview` 全文並重新取得授權，不以摘要取代授權稿；輸出未變時沿用原 preview／授權，不重問。取得本次有效授權並準備實際 write 時，才重新讀 fresh context 與必要 options／snapshot；單純重 preview 不提前重查未受影響的 context／options。每次 write 都須 fresh 核對並保留 snapshot／intent guards，不沿用過時授權 snapshot。

完成條件：日誌 `stop` 已終止，`output_only` 轉第 3 步，或 append／replace 意圖與可用官方契約確定。

## 2. 核對工時與偏好

- 總工時預設 8 小時，含請假；僅使用者明確覆寫才改。PROCESS／PASS 計當日實際分攤，駁回／取消排除，不平均跨日假單、不重複計入非出勤打卡。請假等於總數 stop；超額、重疊或來源衝突先問。
- 無可用假單且無打卡、只有非出勤或混合打卡缺時數時，詢問實際請假時數；非出勤不證明全天假，也不推定 0h。工作預算＝總數−請假。
- append 以 **existing＋new** 核對工作／請假合計。已有 LEAVE 不再新增 LEAVE；其時數不符先釐清。部分假且尚無 LEAVE 時新增實際假時，主旨「請假」，保留原因隱私。不調整舊列或虛構工時以湊數。
- 逾期 append 仍遵守官方工作日、遲報與豁免規則：非豁免工作日當日合計（含 existing）須達 8h。context 若未提供官方 holiday／exemption 資訊，不能猜放行；揭露仍須滿足的條件並交 server validation，不能把自訂 total 當遲報豁免。
- 個人偏好啟用、讀取或更新時先讀 [preferences.md](references/preferences.md)，namespace／API 以該文為準。啟用只確認一次；已啟用後 preview 的新選擇預設覆蓋相同作用範圍，明說「僅本次」不存。偏好不取代當日 options／可靠 branch 核對；共用 mapping 儲存另取確認。

完成條件：工作／請假及 existing＋new 的預算可核對；未知資料已釐清或停止。`output_only` 跳過此步。

## 3. Probe → 來源預告 → Collect

載入 [`daily-work-log`](../daily-work-log/SKILL.md)；分開安裝時從 runtime 發現同名 skill，沿其實際 script 位置呼叫。

1. 沿用上游 recall/preferences 與來源參數，固定日期 From／To／Timezone，先 `-ProbeOnly`。
2. 預告可用來源、略過理由及缺口，再以相同參數 collect；兩來源可用均納入。遵守 DB fallback、Codex 有界日期分區，不擴大／重跑湊證據。
3. 保留全部來源及 coverage 停止條件：無來源、讀取全失敗、無活動、`canGenerateLog=false` 停止；`gh` 不可用／未認證預設停止，只有使用者強烈要求降級才揭露缺口繼續。partial 如實揭露。

沿用上游依 repo 分組的條列摘要，保留證據主題與交付狀態，不把 session 標題當完成；ERP row 的 description 到第 4 節核對歸屬後才合併。

Model 在**已確認工作總預算內自行提出合理主題分配**，不逐項問分時，不把 elapsed、commit 數或比例當 actual 測量。

完成條件：可靠證據與缺口可辨識；不足依上游停止。`output_only` 只輸出證據摘要及未知工時／參照缺口，請使用者到 ERP 處理後完成，不填未知時數；其他路徑續行。

## 4. 解析分類、參照與可選 mapping

1. 以 collector 的 canonical `githubRepo`＋**可靠當日 branch**＋固定 `reportDate` 呼叫官方 resolver。資料夾名不代表 repo；session／commit／PR 可補當日 branch 證據，補報不能用現在 checkout 代替。缺證據或多義先問。resolver `400`／http_error 原因未明時只報解析失敗，不稱缺 mapping、不換 branch 重試、不據此新增永久 mapping。
2. 先用官方回報 project 選項驗證當日合法 project，再查 `GET /api/v2/daily-reports/options/projects/{projectId}/modules`。非法 project 的空 list 不代表無模組；modules 可帶日期但不是歷史快照。使用者簡稱可由已讀 ID／code 唯一辨識，preview 用官方 label，多義才問。
3. singleton 可選；多 modules 按 topic／PR／issue 選唯一有依據的候選並於 preview 列依據。多義／泛稱／未知時列 API 候選與推薦（無依據明說）詢問，不取 first／OTHER／虛構 ID。有 modules 的 PROJECT 每列（含 0h）必填該 project 的 module ID；僅合法 project 確認無 modules 才 null。一個 repo 可分多 modules，不把 module 存入共用 mapping。
4. RD 每次新任務先核對部署官方 spec 與當日立案書 options。API 的 `mandateCharterId` 可選，不代表忽略參照：user 指定 code 時必須用官方 options 找到正確 ID；查無、多義或查詢失敗先修正／詢問，不能以 null 繞過。未指定時，唯一明確適用候選優先選用；只有確認無適用立案書才選 null。不能要求所有 RD 一律由 user 指定，也不能填固定預設 ID。分類／適用性不明先問。agent 在私有 plan 的 local `row.expectedMandateCharterId` 記錄已選 ID 或經核實的 null，由 helper 比對送出內容；合法性仍由 agent 按官方 options 核對。
5. **先核對歸屬，再合描述**：逐一將證據主題（repo＋topic／PR／issue）對回本次已確認的分類及 project／module／立案書，確定所屬 row 後才在該 row 合併 description。使用者已確認的歸屬直接沿用，其他依上述 options／證據規則釐清。沿用已有證據與 plan，不另建歸屬 schema。逐列回看每個主題均在已確認列，且未漏掉；共用 repo、工具性質或相似主旨本身不改變已確認歸屬。一個 repo 可依已確認選擇分到多 modules 或不同分類；不同 repo 同一 RD 立案書可在新工作組稿時合成一列，保留各 repo 群組。未確定的主題先釐清，已授權原文保持不變。
6. append 若同 project＋module 或同立案書撞到 existing／其他新列，先問，不默默合併、刪改或換歸屬。本次 project 選擇與個人偏好不授權共用 mapping；需要永久維護時按 [mapping-save.md](references/mapping-save.md) 完整 list、權限、期間、modifiedTime、差異預覽及獨立儲存確認執行。拒存／缺維護 API 不擋合法日誌。

**實際寫入的 `detail.description` 本身**以 repo 名稱作群組行、`- ` 開頭的短行純文字列出具體成果；保留相關 PR／issue 編號、已核實的 OPEN／MERGED／CLOSED／待交付狀態、實際缺口與待決事項。同一 RD 立案書合成一列時，description 內仍保留各 repo 群組；preview 外框的條列不能取代欄位內的條列。主旨描述工作範圍，內容成果在前、相關編號句尾；不放 Markdown 標題、表格或 HTML，省略流程重述與低訊號細節。超出欄位長度時先精簡再完整預覽，不能送出前截斷。已授權原文保持不變；使用者明確採用合法非條列描述時照原文送出，helper 不做排版改寫。格式示例見 [helper.md](references/helper.md#description-欄位範例)。

完成條件：每條分類、參照、內容與時數合法且可核對；必要選項缺失先解決，`output_only` 跳過此步。

## 5. 預覽、送出與讀回

- **直接展示同 plan 的 helper `--preview` 完整輸出**（可放 code block）：保留 `action`、`mode`、`reportDate`、`expectedSnapshot`、`intent`、`details` 全部業務欄位及 null、`impact.scope`／`preserved`／`replaced` 全文與 `hours` 全部工時。append 的 existing 保留／新增及日合計、replace 的全日替換範圍均須可見；送出前逐欄核對展示內容與 helper 輸出相同。已核對的官方 label／選擇依據可在輸出外補充，不能取代 ID、改寫原輸出或另做一份手工縮略授權稿。取得正向授權後才提交，不先給縮略版再送不同文字。只有**當次明確直接提交**才略 preview；否定、引文、歷史 log、技能說明及含糊「先看看」皆不授權。日期／內容（含 todos）／歸屬／mode／snapshot 改變須重 preview／確認相應意圖，送出前核對與原 dry-run intent 相同。
- 寫前 fresh GET 同日 context、必要 project／module／RD options，重核日期、假時、工時、唯一性與 preview snapshot；已知全天假 stop，unknown／衝突先釐清。僅 replace 重核期限；append 不套 replace deadline。選項失效重新列候選問，不能默換 ID 或 snapshot。
- 依 [helper.md](references/helper.md) 在 repo 外產生私有 task-local plan，context 放完整官方 `AjaxResponse.data`，保留預覽的 `expectedSnapshot`，先 dry-run。append 明填 `mode=append`、只送無 id／modifiedTime 的新 detail；POST body **不含 expectedSnapshot**，本地 snapshot 比對只保護 preview 意圖，不是 server CAS，也不保證寫入當下仍空日。replace 才將 snapshot 送 `/replace` 做全日原子替換。僅契約與當次授權完成才用 `--authorized --contract-verified`，replace existing 另需 `--overwrite-confirmed`。
- 沿用外部 access 的 config root 與 resolved base URL，API key 不進 CLI；本地配置／驗證失敗是 `not_sent`，修正後可續作。傳輸後任何 2xx、應用拒絕、500、timeout 都先用 `erp` 完整讀回同日日誌，再依 [helper.md](references/helper.md#本地-preview-與-readback) 以原送出 plan＋官方 data 執行 `--readback`：核對日期、分類、project／module／立案書、主旨、description 全文、todos 及工時；append 還核對既有列 ID 與原業務內容未變。列順序不影響比對。差異／缺欄位先回報待確認；2xx 本身不代表完成。
- 已生效就 stop。**可信證據確認未生效**且日期、全文、歸屬、context snapshot 與原 dry-run intent 相同時，原授權最多涵蓋一次受控 retry；按 helper 的 `plan.retry` 帶證據、原 intent、沿用 `retriesUsed`，每次 execute 最多一個 request。unknown／timeout／單次空讀回只標待讀回，不重送；空白不證明在途請求永不提交。內容變更或額度用完先重新 preview／授權，不能重設 count 沿用舊授權。

完成條件：完整讀回與提交內容一致才說「已填寫」；缺口如實標待確認。mapping／report 分別回報，已存 mapping 而 report 失敗則保留、不宣稱跨端點 atomic。清理私有暫存 plan，不把 ERP 個資存入 repo，不輸出 secrets、原始反射 error body 或內部路徑。
