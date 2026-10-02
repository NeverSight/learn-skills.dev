---
name: learn-digest
description: "[步驟 6/11·練習] PACER：把某一站每一筆資訊標成 P/A/C/E/R 並寫下該做的消化動作（digest.json → workspace/digest.html）；或用對話帶使用者做練習、批判類比、畫地圖、演練證據、回想參考，做完寫進 digest.state.json。使用者說「做練習」「幫我消化這支」「我要練習／演練／回想」「今天該做什麼」時使用。"
---

> 指令前綴是 `pacer`（本專案的 CLI，裝一次之後任何 agent、任何目錄都能跑）。
> 還沒裝：`uv tool install git+https://github.com/TheWayToLearn/PACER-Learn`（clone 下來的 repo 裡用 `uv tool install -e .`）。
> 只想跑一次：`uvx --from git+https://github.com/TheWayToLearn/PACER-Learn pacer <子指令> …`。

# /learn-digest　—　練習（第 6 步；`/learn --digest false` 可跳過。`do` / `today` 模式是工具，隨時可用）

```
/learn-digest <video_id|url|all> [--force]        # 產工作單：標類別、寫動作、產 digest.html
/learn-digest read <video_id>                     # 「讀完了」：這站從消費期進消化期，開始算積欠
/learn-digest do [<video_id>|due] [P|A|C|E|R]     # 對話式消化：帶使用者把未做的做掉，寫 digest.state.json
/learn-digest today                               # 只印今天的積欠，不做事
```

**消費 vs 消化的分界**：跑 `/learn` 產出工作單只是準備，**不算讀過**。使用者讀完 plan.html（或聽完 lesson.mp3）才按「📖 讀完了」（digest.html 每站一顆，或 `digest.py --mark <vid> read`），那一站的筆才開始算積欠、進 `--pending`；E 的「隔一天」也從讀完那天起算。沒讀的站在積欠行顯示「未讀 N 站不計」。使用者說「這支我看完了／讀完了／聽完了」就是 `read`。

出處：Justin Sung「How to Remember Everything You Read」。讀完只是 **consumption**，留下來靠 **digestion**；每筆資訊依 PACER 分類，各有專屬流程：P 程序→練習、A 類比→批判、C 概念→自己畫地圖、E 證據→存＋演練、R 參考→存＋回想。兩期要平衡：積欠太多就別再吸收。

**語言**：內文用該站 `meta.json` 的 `output_lang`；`concept`、`terms`、`relations[].to` 永遠英文原文。

## 模式一：產工作單（`<id|url|all>`）

1. 定位站：`find_video_dir` 規則找 `workspace/<影片標題>/`；`all` = 所有有 `analysis.json` 的站。已有 `digest.json` 且沒 `--force` → 跳過（重產會讓使用者已做的進度對不上 id）。缺 `analysis.json` → 請先跑 `/learn-analyze`。
2. 讀 `rules/digest.md`（實際路徑看 `paths.py`，可能被 `./learn.rules/` 覆寫）、該站 `analysis.json`、`_overview.json`。
3. 寫 `workspace/<影片標題>/digest.json`（`schemas/digest.schema.json`）。分類單位是**一筆資訊**，一段 2–5 筆、一站 10–40 筆。每類必填見 rules；範例：`tests/fixtures/ws/測試影片 C/digest.json`。
4. 驗證，沒過就改到過：
   ```
   pacer validate digest "workspace/<影片標題>/digest.json"
   ```
   常見錯：`relations[].to` 指到不存在的 concept（先確認同站有那筆 C，或它是 analysis 的 term）、E 的 `supports` 指到 term 而不是 C、同一 concept 開了兩筆。
5. 產頁：
   ```
   pacer digest
   ```
   該站**已經有 `plan.html`** 時再重 render 一次讓每段長出 PACER 標籤（`scripts/render.py <video_id>`）；還沒 render 過就不用，第 7 步會做。
6. 回報：`digest.py` 印的積欠行與 `[6/10] ✔ …` 兩行原樣照抄，再一行說五類各幾筆、`digest.html` 絕對路徑。最後一句固定是**現在就能做的一件事**（通常是第一筆 P 的 `practice_task`）。

## 模式 read：標「讀完了」

```
pacer digest --mark <vid> read      # 標回未讀：unread
```
回報 `digest.py` 印的積欠行（這站的筆現在算進去了），再一句「現在就能做的一件事」= 這站第一筆 P 的 `practice_task`。

## 模式二：對話式消化（`do`）

網頁適合 R 卡與勾做完；P／A／C／E 需要來回，這裡由 agent 當陪練。原則：**使用者動手，agent 只出題與回饋**——不代寫答案、不先給答案卷。

**帶法是提示式，不是考試式**（記住靠的是使用者腦子出力那一下，但純出題等答太乾）：
- **一次只問一格**：A 的像／不像／失效分三次問，C 的關係一條一條問，E 先問「證明了哪個概念」再問「怎麼用」。
- **用填空題問，不用開放題**：每一格都寫成「JSON mode 是逐字生出來、每步限制能選哪些字；Jev 是 ______。」這種一句話留一個空格，使用者只要填那個空。開放式的「哪裡不像？」對使用者來說看不出要幹嘛。R 卡也一樣：`q` 改寫成填空句再問。
- **空格附 3 個選項**：正確答案混在兩個**同站的鄰近概念**裡（例如問 logits 時給「機率／logits／token」），順序打亂、不固定放第一個，不出「以上皆非」。這樣是辨識而不是回想，強度低一點，但使用者卡在「不知道要填什麼」的時間遠比想不起來多。選錯就照下一條給引導問題，不直接公布。
- **卡住先給引導問題，不給答案**：使用者說「不知道」→ 空格再縮小，或給一個更小的問題讓他自己推到（例如問 TS 類比時：「TS 檢查完，程式還能不能算出錯的值？」）；還是不行才丟「是不是 ○○？對或不對」讓他判斷。連這樣都不行才貼答案卷那一格，並標成「跳過」而不是 done。
- **答得不完整也標 done**：標的是「試過」，不是「答對」；把使用者原話記進 `--mark`，漏掉的點由 agent 補一句。
- 底線：使用者還沒開口前，不貼 `critique_key` / `relations` / `a`。

1. 取未做的筆（只會列**已標讀完**的站；使用者要做的站還沒標，先問「這支讀完了嗎？」，是就先 `--mark <vid> read`）：
   ```
   pacer digest --pending [<video_id>|due]
   ```
   輸出 JSON，含答案卷欄位（`relations` / `critique_key` / `a`）——那是給你對照用的，**不要先貼給使用者**。有指定類別就只挑那類；沒指定依 P → E → A → C → R 順序（P 最怕拖，R 網頁自己翻就好）。一次只做一筆，做完問要不要下一筆；使用者說停就停。
2. 每類怎麼帶：
   | kind | 出題 | 使用者回答後 | 記錄 |
   |---|---|---|---|
   | P | 貼 `practice_task`，問「現在做得到嗎？做不到就換去讀別的，不要硬背」 | 問做了什麼、結果如何；一句回饋 | `--mark <key> done "<使用者說的結果>"` |
   | A | 貼 `new` ⇄ `known`，請使用者依序回答「哪裡像／哪裡不像／什麼情況失效」 | 逐格跟 `critique_key` 對照，指出漏掉的那一點；不重述整份答案卷 | `--mark <key> alike=…`、`unlike=…`、`breaks=…`，最後 `done` |
   | C | 貼 `concept`，請使用者**先說**它連到哪些概念、關係是什麼；想用畫的就 `/learn-canvas map <id>`（只給節點，使用者自己連線），連完回來對 | 跟 `relations` 對照：多畫的、漏畫的、方向或關係詞不同的各一句；tldraw 上再用另一色把答案卷的線補上 | `--mark <key> done "<使用者畫的關係>"` |
   | E | 貼 `detail` 與 `rehearse_q` | 判斷有沒有講到「它證明了哪個概念」與「怎麼用」；缺哪個就追問一次 | `--mark <key> rehearsed "<使用者的回答>"` |
   | R | 貼 `q`，等使用者回答再貼 `a` | 問「忘了／難／會」 | `--mark <key> grade 0|3|5` |
3. 記錄用：
   ```
   pacer digest --mark <vid>:<id> <動作> [值]
   ```
   它會寫 `workspace/digest.state.json`（有檔案鎖）並重產 `digest.html`，網頁與 CLI 看同一份；使用者在網頁上做的要按「匯出進度」放到 `workspace/` 才會被這裡看到。
4. 一輪結束回報：做了哪幾筆、`digest.py` 印的積欠行原樣照抄。`--mark` 每次都會順便重匯 `workspace/brain/`（Obsidian vault），不用另外跑。

## second brain（Obsidian）

`digest.py` 每次跑完都會把所有站的工作單＋進度匯成 `workspace/brain/`：`stations/<站>.md`、`concepts/<概念>.md`（同名概念跨站合併，E 證據掛在它證明的概念下，`[[wikilink]]` 互連）。用 Obsidian 開 `workspace/brain/` 這個資料夾，graph view 就是 knowledge network。要另外放就 `scripts/brain.py --out <dir>`。內容改 `digest.json` 再重跑，vault 會被覆蓋。

## `today`

```
pacer digest --backlog
```
原樣印出，再加一句：積欠 > 0 就建議 `/learn-digest do due` 先消化；為 0 才建議吸收新的（`/learn <url>`）。

## 使用者在網頁上做的事（digest.html）

- 頂部「今天」：到期 R 卡、待演練 E、P·A·C 未做；「開始回想」翻卡（空白翻面、1/2/3 = 忘了/難/會）。
- 每筆是該類的動作 UI，做完灰掉；預設只看未做。
- 「匯出進度」→ `digest.state.json` 放到 `workspace/`；「匯出 Anki」→ R 卡 tsv。
- 使用者說「第 N 筆改成…」→ 直接改 `digest.json` 再跑 `digest.py`，不必重新分類；改 `id` 會讓進度對不上。
