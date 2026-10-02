---
name: learn-listen
description: "[步驟 11/11·podcast 頁] 把 workspace 裡所有語音解析（lesson.mp3）列成一集一集，新產出的在上面，置底播放器、字幕（講稿 karaoke）、原聲／翻譯切換、記住聽到哪裡，每集連到 plan.html。使用者說「podcast 頁」「聽的清單」「重產 listen.html」時使用。"
---

> 指令前綴是 `pacer`（本專案的 CLI，裝一次之後任何 agent、任何目錄都能跑）。
> 還沒裝：`uv tool install git+https://github.com/TheWayToLearn/PACER-Learn`（clone 下來的 repo 裡用 `uv tool install -e .`）。
> 只想跑一次：`uvx --from git+https://github.com/TheWayToLearn/PACER-Learn pacer <子指令> …`。

# /learn-listen　—　Podcast 頁（第 11 步；`/learn --listen false` 可跳過）

```
pacer listen
```

- 產 `workspace/listen.html`，以及每站的 `captions.js`（講稿精簡版，播到才載入；用 `<script>` 載所以 `file://` 直接開也有字幕）。
- 步驟 9 `/learn-narrate` 跑完會自動重產一次；`/learn` 最後再跑一次收尾。單獨跑的時機：手動改了 `lesson.json`、或單獨做完 `/learn-notes` 讓「📝 筆記」連結出現。
- 發佈（`/learn-publish`）時 `index.html` 就是這一頁。
- script 執行完會自己印 `[10/10] ✔ … 全部完成` 兩行，把它原樣回報給使用者，不要改寫；再給 `workspace/listen.html` 的絕對路徑與集數。

## 頁面能做的事（回答使用者問題時用）

- 點封面或「▶ 播放」開始播；置底播放器有 ⏮ −15 ▶ +15 ⏭、語速、`CC` 字幕（快捷鍵 C）、`🗣 翻譯`／`🎙 原聲`（快捷鍵 D，該集有 `lesson.dub.mp3` 才出現）。
- 字幕面板就是講稿 karaoke：唸過＝一般色、目前＝強調、未唸＝灰、原聲＝斜體；點任一句從那裡播。
- 每集記住上次聽到哪裡（瀏覽器 localStorage），播完標「✓ 聽完了」並自動接下一集；封面下緣有進度條。
- 網址 `listen.html#<video_id>` 直接打開那一集（不自動播）。
- 鎖定畫面／耳機按鍵可用（Media Session API）。
