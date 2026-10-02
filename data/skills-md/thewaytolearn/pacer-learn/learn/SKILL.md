---
name: learn
description: 使用者貼 YouTube 連結或部落格文章網址並要求學習、整理、做筆記、做文字解析時使用。總指揮：先估時間成本與消化積欠，再依序跑 fetch → segment → shot → analyze → digest → notes → render 產出 plan.html、PACER 練習與筆記。
---

> 指令前綴是 `pacer`（本專案的 CLI，裝一次之後任何 agent、任何目錄都能跑）。
> 還沒裝：`uv tool install git+https://github.com/TheWayToLearn/PACER-Learn`（clone 下來的 repo 裡用 `uv tool install -e .`）。
> 只想跑一次：`uvx --from git+https://github.com/TheWayToLearn/PACER-Learn pacer <子指令> …`。

# /learn — 總指揮（10 個步驟）

```
[1/11] estimate  估成本＋消化積欠   [6/11] digest   練習（--digest，預設開）
[2/11] fetch     抓字幕             [8/11] render   產出 plan.html
[3/11] segment   切段               [9/11] atlas    連結各站（≥ 2 站才需要）
[4/11] shot      截圖               [10/11] narrate  產出語音解析（--narrate，預設開）
[5/11] analyze   逐段分析          [11/11] listen   podcast 頁（--listen，預設開）
```
依賴其實是一棵樹：fetch → segment → (shot) → analyze 是主幹；analyze 之後 digest / render / atlas / narrate 只依賴 analyze（digest 排在 render 前是為了讓 plan.html 第一次就有 PACER 標籤；listen 依賴 narrate）。順序固定是為了進度條好讀，多支影片時 atlas / narrate 可以跟 render 平行派 subagent。
每個階段跑完都會印一行 `[N/10] ✔ … ●●●○○○○○○○` 與下一步，**原樣轉給使用者**，讓他隨時知道走到哪。跳過的步驟也要說明（例如「[2/11] fetch 跳過：transcript.json 已存在」）。

用法：
```
/learn <url> [--shots auto|none|many] [--vision true|false|auto] <url> ...
       # 選項只影響前一個 URL；預設 shots=auto、vision=true
/learn <playlist_url> [--playlist-items 1-10] [--playlist-limit N]
       # YouTube 播放清單：展開成清單順序，一支一支跑
/learn <watch?v=…&list=…> [--playlist one|all|from-here]
       # 從清單裡點進來的單支：預設只做那一支，要整串就 all / from-here
/learn input.yaml
/learn --from <stage> <id>        # 從某階段往後重跑：fetch|segment|shot|analyze|digest|render|narrate|listen
/learn --dry-run <url> ...        # 只列各階段會跳過/執行
```

## 來源：YouTube 或部落格文章

非 YouTube 的 `http(s)` 網址一律當**部落格文章**（id 由網址算出，`b_` 開頭）。流程與十個步驟完全相同，差別由 script 自己處理：
- fetch：正文段落當 transcript，`start` 是閱讀秒數，文中圖片列在 `transcript.images`
- shot：不下載影片、不需要 ffmpeg，直接下載 agent 挑到的文中圖片
- narrate：沒有原聲，clip 改成用文章語言的另一個聲音朗讀原文
- plan.html：時間顯示成 ¶段落編號，連結用 text fragment 跳到原文那一段
`--shots` / `--vision` / `--digest` / `--narrate` / `--listen` 對文章同樣有效（`--shots none` = 不取文中圖片）。

## 來源是播放清單時（一支一支照順序跑）

網址分兩種：
- `youtube.com/playlist?list=…`（純清單）＝ **這一串，照順序做**，直接往下走。
- `watch?v=…&list=…&index=N`（從清單裡點進某一支）＝ **有歧義**：可能只想看這一支，也可能想跟著清單往下上。
  先跑 `playlist.py <網址>` 看清單有幾支、使用者點的是第幾支（`index=N`），再用 AskUserQuestion 問一次，三個選項：
  「只做這一支（推薦）」「從第 N 支開始到最後（`--playlist from-here`）」「整份清單 N 支（`--playlist all`）」，
  並附上各自的總時間／token（estimate 的數字）。使用者已經說了（「整個清單」「這一集就好」「從這裡往後」）就照做，不要問。

確定要做整串（或一段）之後：

1. 先展開，看到清單內容再決定做幾支：
   ```
   pacer playlist <url> [--items 1-10] [--limit N]
   ```
   把它印出的編號列表**原樣**給使用者看（清單名、幾支、總時長、每支標題與長度）。列表下方的「跳過：…」是清單裡抓不到的影片（會員限定、私人、已刪除）——**一定要講**，尤其整份清單只剩一兩支能做時，先說清楚再問要不要繼續。
2. 用 AskUserQuestion 問一次要做幾支，選項例如「前 3 支（先試水溫，推薦）」「前 10 支」「全部 N 支」「自己指定範圍」。
   一次做完整份長清單很貴：把 estimate 的總時間／token 當成理由講清楚，**不要**直接全跑。
   使用者已經說了範圍（「前五支」「第 3 到 7 集」）就照做，不要再問。
3. 把選到的影片**依清單順序**寫進 `workspace/input.yaml`（`playlist.py --urls` 可直接拿到網址；既有的 input.yaml 一樣先讀進來去重合併）。
   `--shots` / `--vision` 等選項套用在清單裡每一支。
4. `/learn-estimate` 一次估全部（`estimate.py` 吃播放清單網址會自己展開，也可以直接把展開後的網址列給它），表格原樣轉給使用者。
5. **一支跑完整條流程再跑下一支**，順序就是清單順序：第 1 支 fetch → segment → shot → analyze → digest → render 全部做完、
   把 `plan.html` 路徑交給使用者（他可以先開始讀），再開始第 2 支。不要把十幾支的 fetch 全部先跑掉。
   - 每支開頭報一行「第 k/N 支：<標題>」，跑完報一行結果，讓進度看得見。
   - 某一支失敗（沒有字幕、影片被下架）就**跳過它繼續下一支**，最後一起列出跳過了哪幾支、為什麼，不要整條流程停掉。
   - `atlas` / `listen` 這種 workspace 層級的步驟在**全部跑完之後做一次**就好；`narrate` 可以在每支 render 後派 subagent 背景跑。
6. 播放清單通常是同一主題的系列課：`/learn-atlas` 時把它們連成一條 `next` 鏈（清單順序就是先後順序），並放進同一個 region。

清單裡已經做過的站（workspace 有該 id 的資料夾且 `plan.html` 存在）直接跳過，說一句「第 k 支已經做過，跳過」——所以中途停掉再貼同一個清單網址，就是接著上次的地方繼續。

## 開始前：確認參數

```
pacer options learn [--set k=v ...]
```
1. 使用者在指令裡已指定的參數用 `--set` 傳進去（例如 `--set shots=none`），它們會標成「你已指定」，**不要再問**。
2. 把 script 印出的表**原樣**給使用者看：每個參數的目前值、意義、可選值。
3. 用 AskUserQuestion 問一次「要用預設嗎？」：
   - 第一個選項固定是「用預設，直接開始（推薦）」。
   - 其餘選項是**這支 skill 實際可調且尚未指定**的參數，每個選項寫清楚改成什麼值、會有什麼差別（例如「不截圖 `--shots none`：快很多、省 token，適合畫面沒資訊的影片」）。
   - 使用者選了就照他的選擇跑；選「用預設」就直接進行。
4. 使用者這次已經在對話裡表達過偏好（例如「這支不用截圖」），視同已指定，不要重複問。
5. `/learn` 只在開頭問一次，涵蓋整條流程；後面各階段不要再問。

## 執行位置
- 所有指令都是 `pacer <子指令>`，跟 cwd 與 agent 無關；`pacer paths` 印出程式根目錄（= wheel 裝在哪）。
- 沒有 `pacer` 時：`uv tool install git+https://github.com/TheWayToLearn/PACER-Learn`，或在 clone 的 repo 裡 `uv tool install -e .`；單次用 `uvx --from git+…/PACER-Learn pacer <子指令>`。
- workspace 在使用者目前目錄的 `./workspace/`（或 `$LEARN_WORKSPACE`）。
- **第 0 步之前先跑** `pacer paths`：它印出每個規則檔實際在哪（使用者可用 `./learn.rules/` 覆寫），之後讀規則就讀它印的路徑。

## 流程（每步都用對應的階段 skill，不要自己重做它的工作）

**準備**（不算步驟）：
- 跑 `paths.py` 確認規則檔實際路徑。
- **判定輸出語言**：順序是**使用者這次明說的 > `workspace/settings.json` 的 `output_lang` > 這次下指令用的語言**（中文 → `zh-TW`，英文 → `en`，其他語言用 BCP-47 碼）。寫進 `workspace/input.yaml` 的 `output_lang`，`/learn-fetch` 時帶 `--output-lang`（存進該站 `meta.json`，之後所有階段與 HTML 介面都跟著它）。
  - **`settings.json` 還沒有 `output_lang`（第一次用）時，在「確認參數」那一步順便問一次**：選項給「跟著我的對話語言（推薦）」／「English」／「繁體中文」。使用者選了就跑
    `pacer options learn --save output_lang=<值>`
    記起來，以後這個 workspace 都不用再問。使用者說「以後都用英文」之類的話也是跑這行。
  - 已經產好的站不受影響（各站以自己 `meta.json` 的 `output_lang` 為準）；要整份換語言就改 `settings.json` 後把各站 `meta.json` 的 `output_lang` 一起改，再重跑 render / atlas / listen / digest / notes。
- 沒有 `input.yaml` 就依參數寫一份到 `workspace/input.yaml`（格式見 `input.example.yaml`）；**已經有就先讀進來、依 `url` 去重後合併再寫回**，不要整份覆蓋（同一個 workspace 可能有另一個 /learn 正在跑）。

**選項**
- `--shots`：`auto`（預設，只截看了才懂的畫面）｜`none`（完全不截圖，也不下載影片，步驟 4 直接跳過）｜`many`（投影片型影片，每段至少一張）。使用者說「畫面沒什麼東西」「重點都在講的內容」「不用截圖」就用 `none`。
- `--vision`：AI 要不要逐張讀截圖，預設 `true`；`--shots none` 時自動失效。
- `--narrate`：要不要順便產出語音解析（第 10 步），**預設 `true`**。使用者說「不用聲音」「只要網頁」就用 `false`。
- `--digest`：要不要做 PACER 練習（第 6 步），**預設 `true`**。使用者說「只要規劃」「不用工作單」就用 `false`。
- `--notes`：要不要擷取筆記（第 7 步），**預設 `true`**。使用者說「不用筆記」就用 `false`。
- `--force`：消化積欠超過 `config/estimate.yaml` 的 `balance.max_backlog` 時 estimate 會警告並建議先消化；使用者堅持就加 `--force` 往下跑。
- `--listen`：要不要重產 podcast 頁 listen.html（第 11 步），**預設 `true`**。`--narrate false` 且 workspace 裡還沒有任何語音解析時自動跳過。
- `--shots` / `--vision` 寫進 `workspace/input.yaml` 該支影片底下，並由 `/learn-segment` 寫進 `segments.json` 的 `shots_mode` / `vision`。

**[1/11] estimate**：跑 `/learn-estimate`（帶上 `--shots` / `--vision`），把分階段 + 總和的表格原樣給使用者看。`--shots none` 會明顯降低時間與 token，值得在確認時指出。使用者未明說「直接跑」時，等確認再繼續。
- **消化平衡閥**：estimate 最後會印「消化積欠：…（共 N，上限 M）」。N > M 且沒 `--force` → **停在這裡**，說明「沒消化的東西會忘掉九成」，建議先 `/learn-digest do due`；使用者說「還是要看」就當 `--force` 繼續。N ≤ M 或沒有任何工作單就照常往下。
  - 積欠只算**已標「讀完了」的站**（digest.html 每站的 📖 按鈕，或 `digest.py --mark <vid> read`）；產出工作單本身不算讀過，所以剛跑完 `/learn` 的站不會立刻變成積欠。積欠行末的「未讀 N 站不計」是提醒有多少站產了還沒讀。

**[2/11]–[4/11]**：每支影片依序 `/learn-fetch` → `/learn-segment` → `/learn-shot`。
- 每階段先看輸出檔是否已存在，存在就跳過（除非 `--force` 或 `--from` 指定要重做）；跳過也要說「[N/10] X 跳過：<檔案> 已存在」。
- agent 產的 JSON 一定要過 `pacer validate <kind> <file>`，不過就修到過。

**[5/11] analyze：一定用 subagent 跑，不要在主對話裡做。**
逐段分析會把整份 transcript 片段、所有截圖、每段的 analysis 累積進 context（實測 150–200k tokens），
留在主對話裡會讓後面的 render / atlas / narrate 每一輪都重送一次。丟進 subagent 就只有結果會回來。

- 用 Agent（Task）tool 開一個 `general-purpose` subagent，一支影片一個；多支影片可以同時開。
- prompt 至少要寫清楚：
  1. 「照 `skills/learn-analyze/SKILL.md` 做」＋ 影片資料夾絕對路徑 ＋ `pacer paths` 印出的程式根目錄。
  2. `--vision` / `--force` 這次的值。
  3. 「自己讀 `rules/narrative.md`、`schemas/analysis.schema.json`、`segments.json`、`meta.json`，不要問我」。
  4. 「寫完跑 validate.py，不過就自己修到過」。
  5. **回傳格式**：只回三樣 —— `progress.py analyze` 印出的那兩行、一句話結果（幾段、vision 用了幾張圖）、
     validate 的最後狀態。**不要把 analysis.json 的內容貼回來。**
- 主對話**不要**讀 `frames/*.jpg`，也不要讀回 `analysis.json`；需要它的是 [6/11]，那時再讀。
- subagent 失敗或 validate 過不了時，它會回報錯誤；再開一個 subagent 修，不要自己接手做完。
- 把 subagent 回傳的那兩行進度原樣轉給使用者。

**[6/11] digest**：`--digest true`（預設）就對每支影片跑 `/learn-digest <id>`（agent 依 `rules/digest.md` 把每筆資訊標 P/A/C/E/R 並寫消化動作 → `validate.py digest` → `digest.py`；這一步**不要**跑 skill 裡的 `render.py`，那是第 8 步）。`false` 則跳過，並提一句「想要工作單可以跑 /pacer:learn-digest <id>」。
- 只讀 `analysis.json` 與 `_overview.json`（`_overview.json` 還沒有就先由 `/learn-render` 的第 1 步產它，或直接讀 analysis），不讀截圖，留在主對話做即可；多支影片可各開一個 subagent（同 [5/11] 的回傳規則）。

**[7/11] notes**：`--notes true`（預設）就對每支影片跑 `/learn-notes <id>`（agent 依 `rules/notes.md` 從 analysis 挑 3–8 條「看完才知道的」→ `validate.py notes` → `notes.py`）。`false` 則跳過，並提一句「想要筆記可以跑 /pacer:learn-notes <id>」。

**[8/11] render**：
- 若 `--narrate true`，**render 之前**先跑一次
  `pacer narrate <id> --mark-pending`，
  這樣產出的 `plan.html` 會顯示「🎧 語音解析產生中…」，並在完成後自動偵測、自動重新整理。
- 每支影片各自 `/learn-render`（每支一份 `plan.html`，在自己的資料夾）。使用者明確要合併時才用 `--combined`。
- **render 完成後立刻把 `plan.html` 路徑給使用者**，告訴他可以先開始讀，語音解析還在做。

**[9/11] atlas**：workspace 下有 ≥ 2 支影片時跑 `/learn-atlas`，把新站跟既有站連起來（route / region）。只有一站就說「[9/11] atlas 跳過：只有一站」。

**[10/11] narrate**：`--narrate true`（預設）就跑 `/learn-narrate`；`false` 則跳過，並提一句「想用聽的可以跑 /pacer:learn-narrate」。
完成後**再跑一次 `/learn-render`**，讓 `plan.html` 換成正式的播放器與講稿（使用者若還開著頁面，它也會自己重新整理）。

**[11/11] listen**：`--listen true`（預設）就跑 `/learn-listen`（`listen.py`，把新的語音解析列進 podcast 頁並掛上 digest / notes 連結）。跳過的情形：`--listen false`，或 `--narrate false` 且 workspace 裡沒有任何 `lesson.mp3`（說「[11/11] listen 跳過：沒有語音解析」）。

**收尾回報**：`plan.html` 路徑、每支影片 vision 模式、estimate vs 實際耗時（`timings.json`）、atlas 上的新 route、工作單五類各幾筆與 `digest.html` / `listen.html` 路徑（有做才列）。提醒一句：**讀完（或聽完）再到 digest.html 按這站的「📖 讀完了」**，工作單才開始算積欠。最後一句固定是**現在就能做的一件事**：第一筆 P 的 `practice_task`——讀完只是消費，做了才算。

## 規則檔（改行為就改這些，不改程式）
- `rules/segment.md`（實際路徑看 `paths.py`，可能被 `./learn.rules/` 覆寫）、`rules/narrative.md`、`rules/overview.md`、`rules/digest.md`、`rules/output.md`
- `config/estimate.yaml`（估算係數）
- `schemas/*.json`（agent 輸出格式）

## 工作目錄
```
workspace/<影片標題>/               # 一站（waypoint）
  estimate.json  transcript.json  meta.json  segments.json  frames/  analysis.json  timings.json
  digest.json                      # [6/11] PACER 工作單：每筆資訊的類別與消化動作（/learn-digest）
  _overview.json  plan.html        # 每支影片各自一份
workspace/atlas.json               # 站與站的 route、主題區（agent 維護）
workspace/listen.html              # [11/11] podcast 頁：所有語音解析新到舊，置底播放器（/learn-listen）
workspace/digest.html              # [6/11] 練習：今天到期、每站五類、做完灰掉（digest.py）
workspace/digest.state.json        # 消化進度（網頁匯出或 /learn-digest do 寫入）
workspace/notes.html               # 筆記（第 7 步，--notes false 可跳過）
workspace/atlas.html               # 影片解析：所有站的卡片、分類、搜尋、相鄰站
```
