---
name: learn-notes
description: "[步驟 7/11·筆記] 把某一站（或全部站）留給我的觀念／技巧／體悟擷取成 notes.json，彙整成 workspace/notes.html，每條連回 plan.html 的那一段。使用者說「做筆記」「這支我學到什麼」「整理筆記」時使用。"
---

> 指令前綴是 `pacer`（本專案的 CLI，裝一次之後任何 agent、任何目錄都能跑）。
> 還沒裝：`uv tool install git+https://github.com/TheWayToLearn/PACER-Learn`（clone 下來的 repo 裡用 `uv tool install -e .`）。
> 只想跑一次：`uvx --from git+https://github.com/TheWayToLearn/PACER-Learn pacer <子指令> …`。

# /learn-notes　—　步驟 7/11 筆記（`/learn --notes false` 可跳過；也可以隨時單獨跑）

用法：`/learn-notes <video_id|url|all> [--force]`

目的不是摘要影片，是回答「**這一篇留給我什麼**」：3–8 條看完之後才知道的觀念（concept）、明天就能照做的技巧（skill）、改變判斷方式的準則（insight）。全部彙整在 `workspace/notes.html`，新的在上面，每條連回 `plan.html#<vid>-s<seg_id>`。

**語言**：`text` / `detail` 用該站 `meta.json` 的 `output_lang`；術語永遠英文原文。

## 1. 定位站

- `<video_id|url>` → 用 `find_video_dir` 的規則找到 `workspace/<影片標題>/`；`all` = workspace 下所有有 `analysis.json` 的站。
- 該站已有 `notes.json` 且沒 `--force` → 跳過，直接到第 3 步。
- 缺 `analysis.json` → 請使用者先跑 `/learn-analyze`。

## 2. 擷取（agent 做，一站一次）

- 讀 `rules/notes.md`（實際路徑看 `paths.py`，可能被 `./learn.rules/` 覆寫）。
- 讀該站 `analysis.json`（每段 `reasoning` / `explanation` / `terms`）與 `_overview.json`（`takeaways`、`summary`）。
- 寫 `workspace/<影片標題>/notes.json`（格式 `schemas/notes.schema.json`）：
  ```json
  {"video_id": "…", "created": "<ISO 時間>", "notes": [
    {"id": 1, "seg_id": 3, "kind": "concept", "text": "…一句話…", "detail": "…為什麼重要…", "terms": ["LCP"]}
  ]}
  ```
- 驗證：
  ```
  pacer validate notes "workspace/<影片標題>/notes.json"
  ```
  沒過就改到過為止（常見：`seg_id` 不存在、`text` 超過 80 字、超過 12 條）。

## 3. 彙整成網頁（script）

```
pacer notes
pacer listen     # 讓 listen.html 的「📝 筆記」連結出現
```
script 執行完用一行說這站擷取了幾條、各是哪種 kind，並給 `workspace/notes.html` 的絕對路徑。

## 使用者在網頁上做的事

- 每條可按「留」／「刪」，狀態存在瀏覽器；篩選「只看留下的」。
- 「匯出」下載 `notes.keep.json`；使用者把它放到 `workspace/` 後，`notes.py` 會把它當預設狀態（跨裝置、發佈後也一致）。
- 使用者說「第 N 條改成…」「把這條刪掉」→ 直接改 `notes.json` 再跑 `notes.py`，不必重新擷取。
