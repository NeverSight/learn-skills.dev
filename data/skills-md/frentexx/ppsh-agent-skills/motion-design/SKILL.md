---
name: motion-design
description: 動態設計品味規則（HyperFrames 版）— 時間軸、緩動、彈性、節奏、字體（含繁體中文）、配色、質感與場景連貫，全部附具體數字。只要是製作、調整、重新計時或打磨動畫影片、片頭、轉場、motion graphics、HyperFrames composition，就一定要使用此技能。觸發情境包含：「做一支動畫」、「做動態影片」、「做片頭」、「motion design」、「讓這段字動起來」、「調整動畫節奏」等。
---

# Motion design（HyperFrames 版）

HyperFrames 文件教你 API，這份檔案管的是品味。底下的數字來自一支實際上線的作品，請把它們當成預設值：要偏離可以，但必須是刻意的，而不是剛好沒注意。

> 改編自 whaleyxbt/claude-motion 的 `motion-design` skill（MIT，見同資料夾 `LICENSE`）。原版針對 Remotion；本版改寫成 HyperFrames（HTML + GSAP），並加上繁體中文排版規則。標示「（本版新增）」的段落不是原作內容。

## 在 motion-explainer 系列流程裡使用時（本版新增）

`motion-explainer`（以及 `-images`、`-video`、`soil-motion-deck`）用官方 `faceless-explainer` 的流程，下面三件事以那個流程為準，本檔的寫法不適用：

- **時間**：節拍來自 `STORYBOARD.md` 和 `audio_meta.json`（旁白子句的時間），每一格的 `data-start`／`data-duration` 由 `assemble-index` 寫入。**不要另外建 `timeline.js`／`window.TL`**（第 1 節）。
- **建專案**：用 `npx hyperframes init`（見 motion-explainer 第 3 節），不是第「流程」節的做法。
- **字型與顏色**：由專案的 `theme.json` 決定（預設源石黑體粗體、三色主題），`theme.py` 會覆蓋每一格自己寫的字型和色票。第 5、6 節的字族建議只在沒有 `theme.json` 時使用。

其餘的品味規則（緩動、彈性、閱讀停留、構圖、中文排版、強調色只給重點）照常適用。

## 與官方 HyperFrames skills 的分工（本版新增）

本機也裝了 HeyGen 官方的 HyperFrames skills（`hyperframes`、`hyperframes-core`、`hyperframes-animation` 等）。分工如下：

- **官方 skills 管「做法」**：專案結構、`data-*` 屬性、API 寫法、流程路由、registry 現成元件。API 寫法和本檔衝突時，以官方為準。
- **本檔管「品味」**：緩動、節奏、停留時間、字體、配色、中文排版。官方 `hyperframes-animation` 的 rules / blueprints 拿來用時，時間和緩動的數字仍以本檔為預設。
- **檢查**：一律走 `review-loop`，它已經包含官方的 `hyperframes check`。

## 0. HyperFrames 的硬規則（本版新增）

違反這些，畫面會在輸出時閃爍、錯位或每次結果不同：

- 時間由 HTML 決定：每個場景是 `class="clip"` 的元素，用 `data-start`、`data-duration` 放上時間軸。根元素要有 `data-composition-id` 和明確的 `data-duration`。
- 動作由 GSAP 負責：`gsap.timeline({ paused: true })`，註冊到 `window.__timelines["<composition-id>"]`，鍵名必須等於 `data-composition-id`。
- 每個重要的 tween 都給明確位置（第三個參數），兩端都重要時用 `fromTo()`，因為輸出時會跳著 seek。
- 只動 `transform` 和 `opacity`，不要反覆動 `top/left/width/height`。
- 禁止：CSS `transition`／`@keyframes`、`Date.now()`、`requestAnimationFrame`、`setTimeout`、沒有種子的 `Math.random()`、輸出途中才 fetch 的資源。
- 不要用 script 播放、暫停、seek 影音，也不要用 script 依時間顯示或隱藏 clip。這些都交給 data 屬性。要移動影片，就動外層的包裝元素。
- 隨機一律用有種子的函式：

  ```js
  function rand(seed) { let t = (seed += 0x6D2B79F5); t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }
  ```

## 1. 時間集中在一個地方

- 每個節拍都是一個有名字的時間點（秒），按場景分組（`s1`、`s2`…），寫在專案根目錄的 `timeline.js`：

  ```js
  window.TL = {
    s1: { start: 0, title: 0.3, items: [1.2, 1.45, 1.7], exit: 3.6 },
    s2: { start: 3.4, drawOn: 3.5, hook: 5.2, end: 8 },
  };
  ```

  在 `index.html` 裡，所有 composition script 之前先用 `<script src="timeline.js"></script>` 載入。
- GSAP 的位置參數一律從 `TL` 取（`TL.s1.title`、`TL.s1.exit + 0.05` 這種相對寫法可以），不要在場景裡寫死秒數。
- 場景外框的 `data-start`／`data-duration` 必須和 `TL` 的場景邊界一致。重新計時時，先改 `timeline.js`，再同步改這兩個屬性。
- 音效和旁白用 `<audio data-start="…">` 放在同一批節拍上。review-loop 的截圖時間也從 `TL` 取，所以畫面、聲音和檢查會一起跟著動。
- 所有畫面都只能由時間決定，見第 0 節。

## 2. 緩動

原作的四條曲線，在 GSAP 裡用 `CustomEase` 精確重建。要多載 `gsap@3/dist/CustomEase.min.js`，再用 `gsap.registerPlugin(CustomEase)` 註冊：

```js
CustomEase.create("enter", "0.16,1,0.3,1");   // easeOut
CustomEase.create("exit",  "0.6,0,0.9,0.35"); // easeIn
CustomEase.create("move",  "0.65,0,0.35,1");  // easeInOut
CustomEase.create("land",  "0.55,0,0.2,1.12"); // overshoot
```

| 曲線 | 用途 | 最接近的內建名稱 |
|---|---|---|
| `enter` = `bezier(0.16, 1, 0.3, 1)` | 進場、揭示，任何「到達」 | `expo.out`（幾乎相同） |
| `exit` = `bezier(0.6, 0, 0.9, 0.35)` | 退場：走得快，不拖泥帶水 | 約 `power3.in` |
| `move` = `bezier(0.65, 0, 0.35, 1)` | 兩個狀態之間的移動（翻面、停靠、變形） | `power2.inOut`（完全相同） |
| `land` = `bezier(0.55, 0, 0.2, 1.12)` | 會「落定」的數值（滑桿爬到某一格） | 沒有好的內建替代，請用 CustomEase |

`ease: "none"`（線性）只用在連續運動：旋轉、漂移、顆粒、秒針。

要讓一個動畫跟著另一個數值走（例如字幕跟著滑桿位置），就用同一個 tween 驅動一個代理物件，在 `onUpdate` 裡衍生，不要給它另一個獨立時鐘。

## 3. 彈性

原作用 Remotion 的物理彈簧，GSAP 沒有彈簧物理。下表是本版挑的近似值（本版新增，不是原作數字），輸出後請用 review-loop 確認手感：

| 手感 | GSAP 設定 | 用在 |
|---|---|---|
| 預設落定 | `back.out(1.2)`，0.6 s | 一般 UI 進場 |
| 厚重、沉穩 | `power3.out`，0.8–1.0 s | 大面板、倒轉 |
| 旋鈕卡格 | `back.out(1.7)`，0.35 s | 控制項跳到某一格 |
| 彈出 | `back.out(2.2)`，0.45 s | 標註、徽章、成功圓點 |
| 彈性重音 | `elastic.out(1, 0.4)`，0.9 s | 每支影片只用一次的高潮時刻 |

有實體感的東西（UI、物件）用彈性，文字和鏡頭感的移動用貝茲曲線。

## 4. 節奏

- **錯開**：英文單字約 0.09 s；中文逐字約 0.04–0.05 s，逐詞約 0.09 s（中文部分為本版新增）；清單項目和標籤約 0.2–0.25 s；圓環和圓點約 0.06 s。
- **文字揭示**約 0.8 s，用遮罩：外層 `overflow: hidden`，內層 `yPercent: 100 → 0` 再加一點旋轉（`rotation: 3 → 0`）。
- **退場約是進場的一半**（0.35–0.55 s 對 0.7–1.25 s），退場用 `exit` 曲線。
- **場景要重疊**：下一場在上一場完全離開前就開始畫入（例如 `s2.drawOn` 4.02 s 早於 `s1.flipEnd` 4.4 s）。硬切出空白，看起來像在「載入中」。
- **打字**每個字元約 0.035 s，閒置時游標以約 2.4 Hz 閃爍（用 `steps` 或 `set` 排在時間軸上，不要用計時器）。
- **閱讀停留**：每個要讓人讀的狀態，落定後都要停住。短句至少 1 s，超過三個詞每多一個詞加約 0.25 s；中文約每多 4 個字加 0.25 s（本版新增）。最後的結尾句至少 2 s。原作的 22 秒版之所以存在，就是因為 15 秒版的字閃太快：拿不準的時候，停久一點、動少一點。

## 5. 字體

- 最多三種字族：展示用襯線、介面無襯線、等寬（用於標籤、提示詞、數字）。
  - 英文（原作）：Instrument Serif／Inter／JetBrains Mono。
  - 繁體中文（本版新增）：Noto Serif TC／Noto Sans TC，數字和標籤搭 JetBrains Mono。字型檔放在專案的 `assets/fonts/`，用 `@font-face` 載入，不要依賴系統字型（換台電腦就不一樣）。
- 英文展示字要大（1080 寬的畫布上約 138 px），字距收緊（`-0.02em`），`line-height: 1`。
- 中文展示字（本版新增）：1080 寬約 96–120 px，一行不超過約 12 個字，字距 `0` 到 `0.02em`（中文不要負字距），`line-height: 1.15–1.25`。
- 每行一個重點：英文用一個斜體字配強調色；中文沒有真斜體，用強調色加粗重來扛重點（本版新增）。
- 等寬標籤：大寫，`letter-spacing: 0.2–0.24em`，顏色調淡。它們只是裝飾；觀眾一定要讀的東西就做大。
- 手機測試：在 360 px 寬（社群動態裡實際看到的大小）時，關鍵訊息仍要讀得清楚。用 contact sheet 檢查。

## 6. 配色

- （本版新增）整支片用**三個顏色定調**，像簡報版型一樣由使用者決定：背景色 `bg`、主色 `fg`（文字與線稿）、強調色 `accent`，寫在專案的 `theme.json`，用 `motion-explainer` 系列技能的 `theme.py` 套用。強調色只給「答案、結論、關鍵數字、章節卡」。
- 色票定義成 `:root` 的 CSS 變數（`--bg`、`--ink`、`--muted`、`--accent`…），場景裡不要再冒出新的色碼。
- 只有一個強調色，而且它有意義：改變的那個東西、答案、勝出者。如果什麼都是強調色，就等於沒有強調。
- 光暈由狀態驅動而不是時間（`glow = effort`）：光線要能說明故事。

## 7. 質感：沒有東西是完全靜止的

- 底片顆粒：SVG `feTurbulence` 濾鏡疊一層，opacity 約 0.09，每兩格換一次 `seed`（在時間軸上用 `set` 排定，種子由幀號算出）。
- 暗角 + 點狀網格，每秒漂移幾 px：`radial-gradient` 暗角，網格用一條跨整支片的線性 tween。
- 手繪「線條抖動」（`feTurbulence` + `feDisplacementMap`，同樣每兩格換種子）：用在草稿感、低完成度的狀態，品質提升時淡出。
- 閒置元素要呼吸：會走的時鐘、閃爍的游標、緩慢的旋轉。

## 8. 連貫與轉場

- 寧可讓物件延續，也不要硬切。原作的提示列、火花和滑桿會穿越場景並改變角色，這就是「有設計過」和「拼湊出來」的差別。在 HyperFrames 裡，跨場景的物件放在根 composition，不要放在某個場景裡面。
- 每個轉場都要由畫面上的物件帶出來（五個結果圓點合成一個，再變成光圈）。不用制式的擦除轉場。
- 用速度：拖影、擠壓從「這一格和上一格的數值差」推出來，不要硬做假的。
- 每支影片一個高潮時刻（光圈 + 衝擊）。一路鋪陳到它，不要太早用掉。

## 9. 反模式

- 所有東西同時淡入，或所有東西都用同一個時長。
- 有起停的東西用線性緩動。
- 文字在該被閱讀的時候還在動。
- 一格畫面裡有超過一個焦點。
- 內容距離畫面邊緣不到約 60 px（安全區），除非是刻意裁切。
- 第 0 格是空白或全黑：社群平台靜音自動播放時，第一格就是縮圖。
- （本版新增）在 script 裡控制影音播放或 clip 顯示、用 CSS 動畫、用沒有種子的隨機，見第 0 節。

## 流程

1. 先把節拍寫進 `timeline.js`（用數字寫的分鏡），向使用者確認節奏再動手。
2. 用 `npx hyperframes init <專案資料夾>` 建專案；每個場景是 `compositions/` 裡的一個 composition，共用元件和跨場景物件放在 `index.html`。
3. 每次有意義的修改後，都跑 `review-loop` 技能。
4. 畫面時間鎖定後再處理聲音：音效和配樂用 `<audio data-start>` 對上 `TL` 的節拍。中文旁白的口音和情緒交給使用者用耳朵判斷，不要拿 ASR 或相似度分數代替（本版新增）。
