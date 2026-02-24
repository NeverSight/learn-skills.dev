---
name: 104-sourcing
description: 自動登入 104 招募管理平台，依據人資需求搜尋並篩選合適候選人。使用時機：當人資需要在 104 平台搜尋求職者、篩選條件、查看 Candidate 資料時。
compatibility: 需要 agent-browser 已全域安裝（npm install -g agent-browser && agent-browser install）
metadata:
  author: orangeapple
  version: "5.0"
---

# 104 HR 人才搜尋

## 概覽

本 Skill 使用 **agent-browser** CLI 控制瀏覽器，自動登入 104 招募管理平台並搜尋合適人選。執行流程分三個階段：**需求訪談 → 登入 → 純 API 搜尋篩選**。

> **依賴工具**：本 Skill 需要 `agent-browser` CLI，安裝方式見 frontmatter 的 `compatibility` 欄位。
> **指令參考**：[references/agent-browser.md](references/agent-browser.md)

### 架構原則（重要）

- **登入用 browser，其餘全用 API**：瀏覽器只用來建立 session cookie，搜尋/篩選/評估全部走 API，速度快 100 倍以上
- **所有 fetch 必須在主 session（104-sourcing）內呼叫**：Subagent 的獨立 session 無法共用登入 cookie
- **eval 只能用 ES5 語法**：`var` 不能用 `const/let`，不能用 arrow function，否則 eval 會報錯

---

## 第一階段：需求訪談

在開啟瀏覽器前，**必須先透過訪談了解招募需求**，不得假設或跳過。訪談分兩層：

### 基本條件（硬性篩選用）

1. **職位名稱**：要搜尋什麼職務？（例：電銷、業務、工程師）
2. **工作地點**：候選人可接受的工作地點？（例：台北市、新北市板橋區）
3. **硬性要求**：有哪些必要條件？（例：工作年資、學歷、特定技能或證照）
4. **待業狀況**：是否只看特定就業狀態的求職者？（預設不限）
   - 不限：`empStatus=0`
   - 在職中（想跳槽）：`empStatus=1`
   - 待業中（即可上班）：`empStatus=2`

### 質性條件（篩選後評估用）

4. **理想候選人樣貌**：這個職位最重視什麼特質或背景？有哪些過往經歷特別加分？
5. **地雷**：有哪些狀況要排除？（例：頻繁換工作、特定產業背景、工作空窗過長）
6. **加分項目**：其他 nice-to-have？（例：具備特定軟體操作經驗、語言能力）

訪談結束後，整理並回覆「搜尋策略確認」：
- **搜尋關鍵字**：用於 API 的 `kws` 參數
- **硬性篩選條件**：JS 過濾邏輯的依據
- **質性評估標準**：看完候選人資料後打分的依據

用戶確認後，再進入第二階段。

---

## 第二階段：啟動瀏覽器並確認登入狀態

瀏覽器**只需登入**，不需要用 UI 操作搜尋或篩選條件。

### 步驟

1. **直接開啟招募管理平台**（帶現有 session，看是否已登入）
   ```bash
   agent-browser --session-name 104-sourcing open https://vip.104.com.tw/rms/index
   ```

2. **取得目前狀態**
   ```bash
   agent-browser --session-name 104-sourcing snapshot -i
   ```
   解讀 snapshot 輸出，判斷目前頁面狀態：

3. **若已在 vip.104.com.tw**（招募管理平台）→ 直接進入第三階段，不需要登入

4. **若被導向登入頁** → 向用戶索取帳號密碼，注意兩種情況：
   - **完整登入**（snapshot 有 email + password 兩個輸入欄）：輸入帳號與密碼
   - **密碼重新驗證**（snapshot 只有 password 輸入欄，無 email 欄）：104 在 session 過期時有時只要求再輸入密碼，不需重新輸入 email
   ```bash
   agent-browser --session-name 104-sourcing fill @eX "{用戶提供的 email}"  # 僅完整登入時
   agent-browser --session-name 104-sourcing fill @eX "{用戶提供的密碼}"
   agent-browser --session-name 104-sourcing click @eX   # 登入按鈕
   agent-browser --session-name 104-sourcing snapshot -i
   ```

5. **若出現 MFA**（snapshot 中有 OTP 輸入）
   - 向用戶索取 6 位數 Email 驗證碼
   - `agent-browser --session-name 104-sourcing fill @eX "驗證碼"`
   - `agent-browser --session-name 104-sourcing press Enter`

6. **確認已進入 vip.104.com.tw**
   - 若出現重複登入對話框：snapshot 找「將目前帳號登出」→ click
   - 若出現廣告彈窗（screenshot 中看到「加強曝光」等促銷文字）：snapshot 找關閉按鈕 → click

---

## 第三階段：純 API 搜尋與篩選

登入完成後，**全程用 eval + fetch API**，不再操作瀏覽器 UI。

### 已知 API 端點

| 用途 | 端點 |
|------|------|
| 搜尋候選人列表（含工作經歷） | `GET https://auth.vip.104.com.tw/api/search/searchResult` |
| 取得單一候選人完整履歷 | `GET https://auth.vip.104.com.tw/vipapi/resume/search/{idNo}?path_for_log=list_search` |
| 取得儲存資料夾列表（含 folderNo） | `GET https://auth.vip.104.com.tw/api/resumeTools/getFolderList?source=search&ec=105` |
| 儲存候選人到資料夾（支援批次） | `POST https://auth.vip.104.com.tw/api/resumeTools/saveResume` |

### 就業狀態代碼（empStatus 參數）

| 值 | 說明 |
|----|------|
| `0` | 不限 |
| `1` | 在職中（想跳槽；`expJobArr[0].expEndDesc` 通常為「仍在職」） |
| `2` | 待業中（已離職，即可上班；`expEndDesc` 顯示離職時長） |

### 城市代碼

完整代碼清單見 [references/area.json](references/area.json)，支援台灣、大陸、海外地區。縣市層代碼末三位為 `000`，行政區層末三位為流水號。

常用縣市快查：

| 地點 | city 參數值 |
|------|------------|
| 台北市 | `6001001000` |
| 新北市 | `6001002000` |
| 基隆市 | `6001004000` |
| 桃園市 | `6001005000` |
| 新竹縣市 | `6001006000` |
| 台中市 | `6001008000` |
| 台南市 | `6001014000` |
| 高雄市 | `6001016000` |

### 步驟 1：呼叫搜尋 API 第 1 頁，取得總頁數與 fixedUpdateDate

```bash
agent-browser --session-name 104-sourcing eval "
fetch('https://auth.vip.104.com.tw/api/search/searchResult?contactPrivacy=0&kws=%E9%9B%BB%E9%8A%B7%E4%BA%BA%E6%89%8D&city=6001001000&workExpTimeType=all&sex=2&empStatus={0|1|2}&updateDateType=1&sortType=RANK&readStatus=all&plastActionDateType=1&page=1&ec=105', {credentials:'include'})
  .then(function(r){return r.json()})
  .then(function(d){
    window._fixedDate = d.result.fixedUpdateDate;
    window._totalPages = d.result.pageInfo.total_page;
    window._allCandidates = d.result.data;
    window._p1done = true;
  });
'fetching page 1...'
"
```

等待後確認：
```bash
sleep 3 && agent-browser --session-name 104-sourcing eval "JSON.stringify({done:window._p1done, fixedDate:window._fixedDate, totalPages:window._totalPages, count:window._allCandidates&&window._allCandidates.length})"
```

> **重要**：`fixedUpdateDate` 必須從第 1 頁回應取得，後續所有分頁都要帶這個值，確保結果一致性。

### 步驟 2：並發抓取所有剩餘頁

```bash
agent-browser --session-name 104-sourcing eval "
var baseUrl = 'https://auth.vip.104.com.tw/api/search/searchResult?contactPrivacy=0&kws=%E9%9B%BB%E9%8A%B7%E4%BA%BA%E6%89%8D&city=6001001000&workExpTimeType=all&sex=2&empStatus={0|1|2}&updateDateType=1&sortType=RANK&readStatus=all&plastActionDateType=1&ec=105&fixed_update_date=';
var pages = [];
for(var i=2; i<=window._totalPages; i++) pages.push(i);
Promise.all(pages.map(function(p){
  return fetch(baseUrl+window._fixedDate+'&page='+p, {credentials:'include'})
    .then(function(r){return r.json()})
    .then(function(d){ window._allCandidates = window._allCandidates.concat(d.result.data); });
})).then(function(){ window._allDone = true; });
'fetching remaining pages...'
"
```

等待後確認：
```bash
sleep 8 && agent-browser --session-name 104-sourcing eval "JSON.stringify({done:window._allDone, total:window._allCandidates.length})"
```

### 步驟 3：在 JS 中直接篩選，不需要呼叫個別履歷 API

搜尋結果的每筆資料已包含完整 `expJobArr`，可直接在記憶體中篩選：

```bash
agent-browser --session-name 104-sourcing eval "
# 範例：篩選職稱含「電銷」且年資 >= 1 年的候選人
var qualified = window._allCandidates.filter(function(c){
  return c.expJobArr && c.expJobArr.some(function(e){
    if((e.expTitle||'').indexOf('電銷') === -1) return false;
    var desc = e.expEndDesc || '';
    if(desc.indexOf('仍在職') > -1) return true;
    var yr = desc.match(/(\d+)年/);
    return yr && parseInt(yr[1]) >= 1;
  });
});
window._qualified = qualified;
JSON.stringify({
  totalSearched: window._allCandidates.length,
  qualified: qualified.length,
  list: qualified.map(function(c){
    return {
      idNo: c.idNo,
      name: c.userName,
      age: c.age,
      edu: c.eduDesc.split(' ')[0],
      city: c.wcityNoDesc,
      totalExp: c.expPeriodDesc,
      teleSalesJobs: c.expJobArr.filter(function(e){
        return (e.expTitle||'').indexOf('電銷')>-1;
      }).map(function(e){ return e.expTitle+'@'+e.expFirm+'('+e.expEndDesc+')'; })
    };
  })
})"
```

### 搜尋 API 回傳的候選人欄位參考

| 欄位 | 說明 |
|------|------|
| `idNo` | 候選人 ID（用於呼叫個別履歷 API） |
| `userName` | 姓名 |
| `age` | 年齡 |
| `sexDesc` | 性別 |
| `eduDesc` | 學歷（含學校名，可用 `.split(' ')[0]` 取簡稱） |
| `wcityNoDesc` | 希望工作地點（多個以「、」分隔） |
| `expPeriodDesc` | 總工作年資描述 |
| `titleCatDesc` | 希望職稱類別 |
| `expJobArr` | 工作經歷陣列（含 `expTitle`, `expFirm`, `expJobNote`, `expEndDesc`, `expPeriod`） |

### 步驟 4：批次儲存合格候選人到資料夾

篩選完成後，**一次 API 呼叫**即可批次儲存所有合格候選人，不需要 UI 操作。

#### 先取得資料夾列表，讓用戶選擇

```bash
agent-browser --session-name 104-sourcing eval "fetch('https://auth.vip.104.com.tw/api/resumeTools/getFolderList?source=search&ec=105',{credentials:'include'}).then(function(r){return r.json()}).then(function(d){window._folders=JSON.stringify(d.result.folderList.map(function(f){return {name:f.name,folderNo:f.folderNo}}))});'fetching'"
sleep 2 && agent-browser --session-name 104-sourcing eval "window._folders"
```

取得結果後，以表格呈現給用戶：

| # | 資料夾名稱 | folderNo |
|---|------------|----------|
| 1 | （依 API 回應填入） | ... |

**詢問用戶**：「請問要將 N 位候選人存入哪個資料夾？」，等用戶選擇後，以選定的 `folderNo` 執行下一步。

#### 批次儲存所有合格候選人

> **重要**：每次 API 呼叫最多成功儲存 **50 筆**，超過的會靜默失敗（在 `params.fail` 中）。
> 必須以 50 筆為單位分批送出，並使用**同步 XHR** 取得即時結果（async fetch + window 變數在頁面導航後會消失）。

```bash
# 以每批 50 筆為單位，用同步 XHR 儲存，直接取得結果
agent-browser --session-name 104-sourcing eval "
var folderNo = '{用戶選擇的 folderNo}';
var batch = window._qualified.slice(0, 50).map(function(c){return c.idNo});
var body = 'rc=11012313&docNo='+folderNo+'&pageSource=search&isDuplicate=0&contentInfo%5Bsnapshot%5D=&contentInfo%5BsearchEngine%5D='+batch.join('%2C');
var xhr = new XMLHttpRequest();
xhr.open('POST','https://auth.vip.104.com.tw/api/resumeTools/saveResume',false);
xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
xhr.withCredentials = true;
xhr.send(body);
xhr.responseText;
"
```

將 `slice(0, 50)` 改為 `slice(50, 100)`、`slice(100, 150)`... 依此類推完成所有批次。

**回應格式說明：**
- `code: 0` → 全部儲存成功
- `code: 6, type: dataDuplicated` → **使用 isDuplicate=-1 時才會出現**；`params.id` 是成功儲存的 ID（非重複），其餘全被帳號層級的重複檢查跳過
- `code: 7, type: partialFail` → 部分失敗；`params.success.searchEngine[]` 是成功的，`params.fail.searchEngine[]` 是失敗的
- `code: 4, type: overStorage` → 資料夾已滿（上限 300 筆）
- `code: 5, type: overView` → 單次請求候選人數量超過平台上限

**saveResume POST 參數說明：**

| 參數 | 值 | 說明 |
|------|-----|------|
| `rc` | `11012313` | 操作類型碼（搜尋頁儲存，固定值） |
| `docNo` | `{folderNo}` | 目標資料夾 ID |
| `pageSource` | `search` | 來源頁面（固定值） |
| `isDuplicate` | `0` | **務必用 0**；`-1` 會跳過帳號內任何資料夾已存過的候選人，導致大量漏存 |
| `contentInfo[searchEngine]` | `{idNo1},{idNo2},...` | 候選人 idNo，逗號分隔，**每批最多 50 筆** |
| `contentInfo[snapshot]` | 空 | 快照 ID（搜尋頁固定留空） |

### 候選人評估報告格式（基本版）

```
## 篩選結果（共 N 位符合條件）

| # | 姓名 | 年齡 | 學歷 | 希望地點 | 工作年資 | 相關經歷 |
|---|------|------|------|----------|----------|----------|
| 1 | 王小明 | 35 | 大學 | 台北市 | 8~9年 | 電銷主管@XX公司(3年) |
...

**建議聯絡**：#1 王小明、#3 ...
**建議略過**：#2 ...（原因：地點不符）
```

### 步驟 3.5（選用）：深度履歷分析

顯示基本篩選結果後，**詢問用戶是否進行深度分析**：

> 「目前根據搜尋列表資料篩出 N 位候選人。是否進行**深度履歷分析**？（額外讀取自我介紹、希望薪資、產業年資，耗時較長但評估更精準）」

用戶選擇「是」後，依序執行：

#### 分批 fetch 個別履歷（每批 50 筆）

以 50 筆為一批，批次間 sleep 5 秒，避免 rate limit。主 session 收集每批 JSON：

```bash
# 第 1 批（idNo 0~49）
agent-browser --session-name 104-sourcing eval "
var ids = window._qualified.slice(0, 50).map(function(c){return c.idNo});
var results = {};
Promise.all(ids.map(function(id){
  return fetch('https://auth.vip.104.com.tw/vipapi/resume/search/'+id+'?path_for_log=list_search',{credentials:'include'})
    .then(function(r){return r.json()})
    .then(function(d){
      var res = d.data ? d.data.resume : null;
      if(!res) return;
      results[id] = {
        intro: res.intro ? res.intro.replace(/<[^>]+>/g,'') : '',
        hopeSalary: res.hopeSalaryDesc || '',
        expCats: res.expCatTimeDesc ? res.expCatTimeDesc.map(function(e){return e.expCatDesc+':'+e.expTimeDesc}).join(', ') : ''
      };
    });
})).then(function(){ window._resumeBatch = JSON.stringify(results); });
'fetching batch 1...'
"
sleep 10 && agent-browser --session-name 104-sourcing eval "window._resumeBatch"
```

每批取回 JSON 後，累積到主 session 的物件中（`let allDetails = {...allDetails, ...JSON.parse(batchJson)}`）。
將 `slice(0,50)` 改為 `slice(50,100)`, `slice(100,150)` ... 完成所有批次。

> 批次數量 = `Math.ceil(qualified.length / 50)`，每批 sleep 10 秒。

#### 合併資料並寫入暫存檔

所有批次完成後，將 `window._qualified`（基本資料）與累積的個別履歷合併，寫入暫存檔：

```bash
# 主 session 中取出 _qualified 基本資料
agent-browser --session-name 104-sourcing eval "JSON.stringify(window._qualified)"
```

將兩份資料合併為：
```json
[
  {
    "idNo": "...",
    "name": "...",
    "age": 28,
    "expJobArr": [...],
    "intro": "...",
    "hopeSalary": "35,000~45,000",
    "expCats": "教育業:2年, 金融業:1年"
  },
  ...
]
```

寫入 `/tmp/104_resumes.json`。

#### 並發啟動 Sub-agents 分析

將候選人分組，每組 50 筆，用 Task tool **同時**啟動多個 sub-agents（subagent_type: `general-purpose`）：

```
Task prompt 範例（每個 sub-agent）：

請讀取 /tmp/104_resumes.json，分析第 {start} 到第 {end} 筆候選人（0-indexed）。

招募條件：
- 職位：{職位}
- 硬性要求：{條件}
- 理想候選人：{描述}
- 地雷：{排除條件}
- 加分：{nice-to-have}

請針對每位候選人：
1. 評分（1-5）
2. 推薦原因（一句話）
3. 疑慮（若有）

回傳格式（JSON array）：
[{"idNo":"...","score":4,"reason":"...","concern":"..."}]
```

主 session 等所有 sub-agents 回傳後，彙整所有評分結果，以分數排序後呈現深度版評估報告：

```
## 深度篩選結果（共 N 位，按推薦分數排序）

| # | 姓名 | 評分 | 年齡 | 希望薪資 | 產業背景 | 推薦原因 | 疑慮 |
|---|------|------|------|----------|----------|----------|------|
| 1 | 王小明 | ★★★★★ | 28 | 4~5萬 | 教育業2年 | 符合理想背景 | 無 |
...
```

---

## 注意事項

- **eval 只能用 ES5**：不可用 `const/let`、arrow function、template literal，否則報 SyntaxError
- **API fetch 必須在主 session（104-sourcing）內呼叫**：Subagent 的獨立 session 沒有登入 cookie
- `expJobNote` 含 HTML 標籤，分析前用 `.replace(/<[^>]+>/g, '')` 清除
- `fixedUpdateDate` 必須從第 1 頁回應取得後，用於所有後續分頁請求
- 若 session 失效（fetch 回傳「尚未登入」），重新執行第二階段登入流程
- **搜尋關鍵字不要加「人才」兩字**：104 搜尋機制不夠精準，加了「人才」後容易搜到「人才專員」「人才顧問」等人資職缺，反而干擾結果。直接用職位名稱即可（例如：電銷、業務、工程師）
- **saveResume 必須用 isDuplicate=0**：`-1` 是帳號層級的重複檢查（只要曾存過任何資料夾就算重複），會導致大量候選人被靜默跳過；`0` 才會強制儲存到目標資料夾
- **每批最多 50 筆**：saveResume 每次請求實際成功儲存上限為 50 筆，超過的會列在 `params.fail` 但不報錯，務必以 50 為單位分批
- **saveResume 用同步 XHR，不用 async fetch**：async fetch 需要額外的 sleep + 讀取 window 變數，一旦中間導航頁面就會遺失；同步 XHR 直接回傳結果，更可靠
- **頁面導航會清空所有 window 變數**：只要執行 `open` 切換頁面，`window._qualified`、`window._allCandidates` 等全部消失，需重新抓取篩選
