---
name: learn-canvas
description: "[工具] 把某支影片畫成 tldraw 畫布。兩種模式：(1) 逐段圖解 analysis.json，只畫真正重要的角色；(2) `map`：PACER C 類「先畫再對答案」——只丟概念節點不丟線，使用者自己連，連完 /learn-digest do C 對照答案卷。使用者說「畫出來」「用畫的理解」「在 tldraw 畫」「第 N 段」「我要畫地圖」時使用。"
---

> 指令前綴是 `pacer`（本專案的 CLI，裝一次之後任何 agent、任何目錄都能跑）。
> 還沒裝：`uv tool install git+https://github.com/TheWayToLearn/PACER-Learn`（clone 下來的 repo 裡用 `uv tool install -e .`）。
> 只想跑一次：`uvx --from git+https://github.com/TheWayToLearn/PACER-Learn pacer <子指令> …`。

# /learn-canvas　—　把 plan.html 的內容畫成 tldraw 白板（工具，不在 10 步流程內）

不是重新排版 plan.html，是**重新設計**：每段挑 2–5 個真正決定這段在講什麼的角色，砍掉其餘，用方塊＋箭頭＋一句紅字（這段的推論／心態轉折）畫出來。目標是使用者「有理解到重要的角色」，不是畫得完整。

## 前置條件

需要 `tldraw-offline` skill（tldraw Desktop 另一支 app）已裝好且開著。開始前用它列一次文件確認連得上；連不上就請使用者開啟 tldraw Desktop，不要自己猜路徑硬闖。

## 0. 定位來源

使用者可能給 `plan.html` 路徑、影片資料夾、video id 或 URL。一律換算成：
- `folder` = 該影片的 workspace 資料夾（`plan.html` 的所在目錄）
- `folder/analysis.json`（每段的 `builds_on` / `reasoning` / `explanation` / `terms` / `leads_to`）
- `folder/meta.json`（拿 `title` 當畫布/文件命名）

`analysis.json` 才是畫圖的原始素材，不要去解析 `plan.html` 的 HTML。

## 1. 找到或建立對應的 tldraw 文件

用 `api.getDocs()` 找名字是 `<title> 圖解` 的文件；找到就繼續畫在上面，**不要重建**。沒有就用 `/api/docs/create` 建一個。

判斷「畫到第幾段」不靠額外的狀態檔，靠畫布本身：每個形狀的 id 用 `s<segmentId>-<slug>` 命名（例如 `s3-realm`）。要接著畫第 N 段前，先用 `api.getShapes(doc.id)` 看有沒有 `s<N>-` 開頭的 id——有就代表已經畫過，問使用者是要覆蓋重畫還是跳過。

## 2. 一段要畫什麼：先砍，再畫

讀該段的 `builds_on`、`reasoning`、`terms`、`leads_to`（不要整段 `explanation` 照搬，那是給人看文字用的，不是給人看圖用的）。比照 `rules/narrative.md` 的線性推進：**這段的出發點是上一段的 `leads_to`，不要引用還沒畫的段落**。

從中挑：
- **1 個標題**：這段一句話在解決什麼問題（帶段號）
- **2–5 個角色**：能被砍的都砍。判斷準則——拿掉這個角色，使用者還聽得懂這段在講什麼嗎？聽得懂就砍。
- **最多一句紅字**：這段真正的推論或心態轉折（呼應 `reasoning` 或 `explanation` 裡「容易滑過去但很關鍵」的那句），不是每個 term 的 definition 都要搬上去
- **可省的灰字**：刻意不畫的東西可以一句帶過（讓使用者知道「這次不看」≠「不存在」），非必要不加

如果上一段的某個角色在這段被「打開」（例如上一段留了問號，這段給答案），**更新那個舊形狀**（改 `richText`），不要重畫一個新的疊上去——這樣使用者回頭看第一段時看到的是最新答案。

## 3. 版面：先建、量測、再校正——不要相信第一次猜的座標

中文字容易 `growY`（框自動變高）撐破手排的間距，導致文字重疊。流程固定三步：

1. **建立**：新段落接在畫布目前最低點下面（同一批多段可以左右並排，但標題文字寬度常超過預期，並排前抓寬鬆一點的 x 間距，例如 800–900px 起跳）。
2. **量測**：呼叫一次 `helpers.getLints()`。看到 `growY-on-shape` 或 `overlapping-text` 不算完成。
3. **reflow**：用 `editor.getShapePageBounds(id)` 拿形狀**建立後的實際高度**（不是你原本設的），照實際高度重新排列同一欄/同一組裡後面的形狀（`y += 實際h + 間距`），而不是重新用猜的數字硬改一次。整批（同一批 2 段以上）常見的坑：
   - 兩欄標題文字太長，左右互相撞到——把右欄整欄往右平移，而不是縮標題文字。
   - 同一欄裡框接框，量到的高度比設定的高，下一個框要往下讓。
   `createArrowBetweenShapes` 建的箭頭綁定 shape id，挪動形狀時箭頭自動跟著动，不用手動重連。

排列風格延續既有慣例：不同角色用不同顏色（`geo` 的 `color`），承上啟下用有文字標籤的綁定箭頭（`helpers.createArrowBetweenShapes(from, to, { text: '...' })`），程式碼用 `font: 'mono'`、`verticalAlign: 'start'`。

## 4. 驗證

`helpers.saveDoc()` 存檔，`api.getScreenshot(doc.id, { size: 'large', bounds: {...這段的範圍...} })`，用 Read 工具打開截圖檢查：文字沒被裁切、箭頭方向對、`getLints()` 是空陣列。有問題就回到第 3 步 reflow，不要重寫文字內容硬湊。

## 5. 回報

不超過 5 條列出這段畫了哪些角色（不是每個 term，是圖上實際出現的形狀），一句話說刻意沒畫什麼，結尾給下一步：「說『下一段』或『第 N 段』」。使用者說「一次全部畫完」就依序把剩下的段落都畫完（可以幾段一批處理，每批畫完照第 3–4 步 reflow／驗證一次），最後統一回報整體脈絡（每段一句話串成一條線）與省略掉的細節清單。


## 模式 `map`：概念地圖，先畫再對答案（PACER 的 C）

```
/learn-canvas map <video_id|url>
```
影片的主張：概念性知識是網路，**學習者自己**重建專家腦中的連結才會留下；AI 畫好的圖是消費，不是消化。所以這個模式只給節點、不給線。

1. 讀 `folder/digest.json`（沒有就請先跑 `/learn-digest <id>`），取所有 `kind == "C"` 的 `concept`（`relations` 是答案卷，**這一步不要畫、不要唸出來**）。
2. 文件名 `<title> 地圖`；已存在就不重建（使用者可能畫到一半）。
3. 每個 concept 一個 `geo` 方塊，id 用 `c-<slug>`，**隨機散佈**（不要依 relations 排位置，位置本身就是提示）；同一種顏色；不畫任何箭頭。畫完 `getLints()`、存檔。
4. 對使用者只說一句：「節點都在了，把你認為有關的連起來，箭頭上寫關係；連完說『對答案』。」
5. 使用者說「對答案」→ 走 `/learn-digest do <id> C`：用 `api.getShapes(doc.id)` 讀所有 arrow 的 `start.boundShapeId` / `end.boundShapeId` 與 `text`，換算回 concept 對，跟 `relations` 對照，分三類各一句：**多畫的**（答案卷沒有，未必錯，問使用者理由）、**漏畫的**（答案卷有你沒有）、**方向或關係詞不同的**。然後才把答案卷的線用另一個顏色（例如紅）補到畫布上，id 用 `k-<from>-<to>`，讓兩者並排可比。每個 C 用 `digest.py --mark <vid>:<id> done "<使用者畫的關係>"` 記錄。
