---
name: framework-issue
description: "Manages framework issues on tarrragon/claude: dedup, create, comment-as-section init/update/observe/check, fix-matrix close, folding tickets into issues. Use for: framework issue, 框架 issue, canonical issue, ticket 收束, 跨 consumer 修復追蹤, curator 派發."
metadata:
  version: 2.6.0
---

# Framework Issue

框架問題的知識載體是 canonical repo（`tarrragon/claude`）上的 issue，本地 ticket 只記執行。本檔是入口：先定位你在做哪一種事，再依路由表讀對應的一份 reference。

## 定位：ticket 記執行，issue 記問題

| | ticket | issue |
|---|---|---|
| 一張對應什麼 | 一個執行單位（本專案這一階段做什麼） | 一個問題領域（問題是什麼、為何這樣解） |
| 狀態可逆 | 否 | 是（close 可 reopen，close 只代表當前結論暫時穩定） |
| 可見範圍 | 單一 consumer | 所有 consumer |
| 增長語意 | 池增長是負債 | open 數增長不是失效，同領域裂成多張才是 |

工作流四階段：發現問題 → 分析票（ticket）；分析與方案 → issue 區段；實作 → 實作票（依階段裁票）；同步 → `sync-push`。分析 context 留在 ticket 時對其他 consumer 不可見，同一問題會被重複發現、已解的問題後續票不知情。

## 決策入口

先答這一問：**這個問題替換掉本專案名稱與路徑後還成立、且根源在 `.claude/` 通用資產嗎？** 兩者皆是才是框架問題；否則走 `ticket` skill。

| 你要做的事 | 動作 |
|-----------|------|
| 記錄一個新框架問題 | `dedup` 查重 → 逐一判定命中的關係（重複／切分／引用）→ 依關係處置 |
| 對既有 issue 補實測、反證、疑慮 | `observe`，任何 session 隨時可加，不需 owner |
| 更新自己擁有的區段 | `update <comment-id>`，以 comment id 精準編輯 |
| 把一群本地 ticket 的分析收進 issue | 收束流程五步（見下節） |
| 一個壞 change 多個 consumer 各自修 | fix-matrix 命令（`fix-status` / `fix-version` / `close`） |
| ticket 執行中發現框架問題，決定接不接 | 兩條路徑（先記錄不接手 / 當下接手）與關閉協定 |

**查重命中不等於重複**：全文檢索涵蓋 comment 內文，互相引用的 issue 會同時命中彼此。三種關係的判定與處置見按需讀取表的協定檔。

## 命令總表

全部命令住在 `scripts/`，以 `python3 .claude/skills/framework-issue/scripts/<檔名> ...` 執行。`<issue-ref>` 支援 `owner/repo#N`（限框架 repo）、`#N`、純數字。

| 命令 | 檔名 | 用途 |
|------|------|------|
| `dedup` | `section_comment.py` | 唯讀查重，含空白的關鍵字組拆單詞聯集查詢 |
| `init` | `section_comment.py` | 查重後建全部區段 comment、與既有索引列合併回填一次 body 索引；**issue 已有區段時拒絕**（exit 3，`--force` 可覆蓋並合併） |
| `add` | `section_comment.py` | 對已 init 過的 issue 追加單一區段，併入既有索引列 |
| `update` | `section_comment.py` | 以 comment id 更新自己擁有的區段 |
| `transfer-owner` | `section_comment.py` | PATCH 區段首行標記的 owner 欄，內容不變 |
| `observe` | `section_comment.py` | 附加觀測 comment |
| `show` | `section_comment.py` | 以 body 索引為入口，區分區段與觀測流 |
| `check` | `section_comment.py` | 三項警訊：當前結論落後最新觀測（主）、comment 數、索引一致性 |
| `todo` | `section_comment.py` | 唯讀，跨 open issue 聚合「待辦與來源*」表格列；預設本 consumer 擁有的 open issue，`--all`／`--issue N` 改範圍，`--status`／`--stage`／`--priority`／`--consumer`／`--json` 可用 |
| `create` | `create_issue.py` | 建 issue，body 自動附環境資訊 |
| `list` | `list_issues.py` | 列 issue，`--search` 作粗篩 |
| `link` | `link_issue.py` | 把 issue ref stamp 進本地 error-pattern 的分類資訊表 |
| `fix-status` | `fix_status.py` | 查或標記本 consumer 的修復狀態（body 內 fix-matrix 表） |
| `fix-version` | `fix_version.py` | 追加修復版本號（body 內 fix-versions 表），close 前置 |
| `close`（issue） | `close_issue.py` | 關 issue，缺版本號註記即拒（exit 3）；與收束流程的 ticket close 是不同對象 |

exit code：`0` 成功、`3` 降級（gh 未安裝／未登入／Issues 停用／執行例外，stderr 給提示不拋 traceback）。

## 收束流程速覽

把一群本地 ticket 壓成 issue 的當前結論，完整配方在 `references/ticket-intake.md`。五步不可跳：

1. **分群**：以主題為單位，一主題一 issue；先與並行 session 對齊誰認領哪個主題。
2. **查重**：`dedup` 單詞 token；主題已有 open issue 一律附加，不新開。
3. **改寫**：ticket 是時序累積（後段修正前段），區段是狀態呈現（只含現在成立的）。逐段問「這是現在的結論，還是通往結論的過程？」，被推翻的中間版本刪除、只留一句撤回記錄。
4. **建段**：「當前結論」（讀者入口）必有；「問題與方案」「待辦與來源」有內容才建，不寫空殼。
5. **收票**：ANA／DOC／IMP 一律 close，知識住址寫進 reason-note；依賴範圍票的外部票以 `set-why` 補 issue ref。命令、範圍規則與 reason-note 禁詞見 `references/ticket-intake.md` 步驟五。

## Owner 與派發

區段 owner 是實際執行該工作的 session，他方以 `observe` 附加或 `add` 自己的區段。`init`／`add` 預設自行推導 owner（不需指定），推導值為 `<專案目錄 kebab-case>-<session uuid 前 8 碼十六進位>`；`--owner` 降為覆寫確認用途，給值不符或推導失敗一律 exit 3，無靜默降級路徑；理由見協定檔〈owner 識別格式〉。

收束與區段撰寫派 `framework-issue-curator`（opus、effort medium）；一個主題一個 curator 並行，派發票列明範圍內的 ticket ID，curator 只對這些票 close。純 `observe`／`check` 類輕量操作不需派發。

## 按需讀取

涵蓋章節欄與目標檔的 `##` 標題逐字相同、雙向齊全。

| 何時讀 | 檔案 | 涵蓋章節 |
|--------|------|---------|
| 要 init／add／update／transfer-owner／observe／show／check，或判定查重關係、解讀 check 警訊、查 owner 格式 | `references/comment-as-section-protocol.md` | 〈操作一覽〉〈CLI 語法〉〈區段與觀測標記格式〉〈init 前查重：三種關係處置〉〈check 的三項警訊〉〈增長語意與 close 語意〉〈已知限制〉 |
| 要用 create／list／link／fix-status／fix-version／close | `references/fix-matrix-commands.md` | 〈create 與 list〉〈link〉〈fix-status〉〈fix-version〉〈close〉〈Graceful Degradation〉 |
| ticket 執行中辨識到框架問題，決定接不接與怎麼關；或發現當下要判斷能否直接寫定修法；或收束時要判斷某個修法能否寫進「當前結論」區段 | `references/escalation-flow.md` | 〈介入判斷：框架問題 vs 專案問題〉〈兩條路徑〉〈修法時點分離：發現票何時能寫定修法〉〈Issue 關閉協定〉〈回報前查重 SOP〉 |
| 要把一群 ticket 收束成 issue，或派 curator 做這件事 | `references/ticket-intake.md` | 〈前提與分工〉〈步驟一：分群〉〈步驟二：查重與落點〉〈步驟三：時序改狀態〉〈步驟四：區段範本〉〈步驟五：ticket 處置〉〈步驟六：驗證與交接〉〈派發 curator〉 |
| 想看一張 issue 從 dedup 到 check 的完整走查 | `references/worked-example.md` | 〈情境〉〈查重輸出與關係判定〉〈sections.json〉〈init 與索引〉〈ticket close〉〈check 與 owner 更新〉 |

## Testing

```bash
uv run --project .claude/hooks pytest .claude/skills/framework-issue/tests/ -v
```

測試以 mock 攔截 gh subprocess，不真打 GitHub API。

---

版本紀錄在同目錄的 `CHANGELOG.md`。
