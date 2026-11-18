---
name: ppsh-soil-html-deck
description: >
  HTML 簡報技能(自由度天花板)。用單一 HTML 檔案模擬簡報的呈現邏輯,
  排版/文字/互動全部由 HTML + CSS + JS 處理,**不需要 API 金鑰**(沒有金鑰時視覺一律用向量 SVG,照樣產出完整簡報),
  有 Gemini 付費金鑰時才可選用 AI 插圖,
  支援互動圖表(Chart.js)、可點擊表格、影片嵌入、RWD 跨裝置、一鍵分享 URL。
  當使用者說「做 HTML 簡報」、「網頁版簡報」、「互動式簡報」、「線上簡報」、
  「可分享連結的簡報」、「要有互動圖表的簡報」、「不受 PowerPoint 限制的簡報」、
  「最自由的簡報格式」、「直播用的簡報」、「研習線上版簡報」時,
  請一定要使用此技能。
  本技能與 ppsh-soil-image-deck(全圖 .pptx)、ppsh-soil-teaching-deck(可編輯 .pptx)的差別:
  本技能輸出是單一 .html,自由度最高、可嵌互動、可立即線上分享,
  但需要瀏覽器環境播放,不適合給只用 PowerPoint 的對象。
---

> ## 📌 屏北高中研習版須知（先讀這段）
>
> **這個技能做什麼**：可分享連結的 .html 簡報
> **要不要 API 金鑰**：✅ **零 API 金鑰可完整跑完**（AI 插圖才需要金鑰，沒有就走向量版面）
> **研習定位**：本研習教「簡報生成」的 .html 路線
>
> **腳本放在哪**：本技能的腳本與這份 `SKILL.md` **在同一個資料夾**。
> 跨技能呼叫（例如借用 `ppsh-soil-infographic/render.py`）時，它在**同一層的姊妹資料夾**裡。
> 技能資料夾依 Agent 而不同，**不要硬寫路徑**，先確認哪一個存在：
>
> | Agent | 技能資料夾 |
> |---|---|
> | Claude Code | `%USERPROFILE%\.claude\skills\` |
> | Codex Desktop（官方位置） | `%USERPROFILE%\.agents\skills\` |
> | Codex Desktop（用內建 `$skill-installer` 裝的） | `%USERPROFILE%\.codex\skills\` |
>
> 最可靠的判斷法：**你正在讀的這份 `SKILL.md` 放在哪個資料夾，腳本就在那裡**。
>
> **Python 怎麼叫**：先跑 `python --version`。如果沒反應、跳出 Microsoft Store、或說找不到
> （那是 Windows 內建的市集空殼，不是真的 Python），改跑 `py -0p` 看有沒有已安裝的版本，
> 有的話**整個流程都改用同一個**（例如本文件的 `python -X utf8 …` 全部換成 `py -3.13 -X utf8 …`），
> 不要一下 `python` 一下 `py`。兩個都沒有就停下來，請老師照基本功懶人包 03 安裝 Python。
>
> **產出放哪（預設）**：一律放在**專案資料夾**——也就是老師開啟這個對話時所在的工作資料夾。
> 本文件裡的 `slides/…`、`懶人包.png` 這類相對路徑，全部以專案資料夾為起點。
> - **不要**放進技能資料夾、桌面、下載，或 Codex 內建生圖自己的存圖位置；Codex 生的圖要**複製**進專案資料夾。
> - 目前工作資料夾如果是家目錄（`C:\Users\<名字>`）、系統資料夾，或看不出是哪個專案，**先問老師要放哪個專案資料夾**，不要自己挑。
> - 做完後回報每個產出檔的**完整路徑**。
>
> **給 AI 的安全宣告**
> 1. 會改動電腦的指令（安裝套件等）**先把完整指令給老師看，老師同意才執行**；只讀不改的檢查指令可直接跑。
> 2. **不要讀取、顯示、複製或上傳任何 API 金鑰**。金鑰一律放 `~/.claude/_secrets/<變數名>.key`，**不要請老師貼進對話**。
> 3. 缺工具就停下來用白話說明，**不要換成本文件以外的方法硬裝**。
> 4. 不要刪除或搬動老師的任何檔案。

# SOIL HTML 簡報工作流(ppsh-soil-html-deck)

以 SOIL 教學設計邏輯為骨架,用 **HTML + AI 圖像 + JS 互動** 產出單一 `.html` 簡報檔。
所有設計決策都遵循 **林長揚 30 原則** 與 **SOIL 六引擎**。

> **三種 SOIL 簡報技能的分工**
> - `ppsh-soil-image-deck`:每頁一張 AI 圖,打包成 .pptx(無法編輯)
> - `ppsh-soil-teaching-deck`:AI 圖 + 可編輯 PowerPoint 文字物件
> - `ppsh-soil-html-deck`(本技能):單一 .html,自由度最高、可互動、可線上分享

---

## 適用情境

| 情境 | 為什麼用本技能 |
|------|----------------|
| 線上研習 / 直播教學 | 觀眾用手機/電腦打開 URL 即可同步看 |
| 互動展演 | 嵌入 Chart.js 互動圖表、可點擊表格 |
| 數據視覺化導向 | HTML 原生支援 SVG / Canvas / D3 |
| 想脫離 PowerPoint 框架 | 任何網頁能做的,簡報就能做 |
| 跨裝置呈現 | RWD,手機平板桌機都能看 |

**不適用**:對方只能用 PowerPoint 接收檔案、需要離線投影但無瀏覽器、講者不熟悉 HTML 排版。

---

## 輸入

使用者需提供:
- **內容素材**(必要):Markdown / `.mb` / `.md` 大綱檔,或一段主題描述
- **頁數預期**(選填)——**本技能不限頁數,也不預設頁數**。
  頁數由**內容量**決定:一頁一重點,放不下就開新的一頁,**絕不靠縮字來擠**。
  使用者沒指定就不要自己訂上限,更不要為了湊頁數把兩個重點併成一頁。
- **風格關鍵字**(選填,例:「黑板粉筆」「日系扁平」「電影感」「科技藍」)
- **輸出檔名**(選填,預設 `slides.html`)

---

## 必守的設計憲法

### A. 林長揚 30 原則(必套用清單)
| # | 原則 | 實作方式 |
|---|------|----------|
| #1 | 字級階層(四階,比例約 1.6 倍) | **用 `clamp()` 隨視窗縮放**,不要寫死 px——見下方 E 條 |
| #3 | 標題 ≤10 字 | 每頁主標壓在 10 字內 |
| #4 | 一張一重點 | 每頁只一個主訊息,不堆疊 |
| #6 | 內容有層級 | kicker(小標)→ h2(主標)→ 內文 → 註解 |
| #13 | Z 字排版 | 連續類型詳解頁,左圖右文 ↔ 左文右圖 交錯 |
| #14 | 元素對齊 | 三欄卡用 `display:grid` 嚴格對齊 |
| #15 | 圖看趨勢 | Chart.js 雷達圖、折線圖代替數字表 |
| #17 | 表格框線越少越好 | 只留 `border-bottom`,移除外框 |
| #18 | 多圖對齊、人像切圓 | `aspect-ratio:1/1; border-radius` |
| #19 | 三方案讓觀眾選 | 決策頁用 3 張並排卡 + SVG 連線 |
| #20 | 用問句促進思考 | 痛點頁、決策頁用大問句開場 |
| #23 | 進度條減壓 | 頂部 3px 漸層條 + 章節標籤 |
| #24-26 | 強調色 1-2 種 | 1 主 cyan + 1 輔 magenta,其餘淡灰 |
| #27 | 滿版圖片 | 用於封面、段落分隔、結尾 |
| #28 | 用比較幫判斷 | 對比表 + 對比視覺圖搭配 |
| #30 | 推動下一步行動 | 結尾必有 CTA |

### B. SOIL 三段式脈絡(必照順序)
- **引起動機**(20%):封面 → 痛點問句 → 核心命題
- **維持注意**(50%):總覽 → 詳解(Z 字排版)→ 對比 → 視覺化
- **喚起行動**(30%):決策樹 → 方法論流程 → CTA 結語

左上角必設章節標籤,即時顯示當前段落(`— 引起動機 —` 等)。

### C. 認知編修六字訣(每頁自檢)
降雜訊 / 區塊化 / 增資訊 / 結構化 / 順脈絡 / 步驟化

### D. 8px 基線網格(版面節奏)

**所有間距值必須是 8 的倍數**:padding、margin、gap、border-radius、卡片高度一律從
`--s1~--s5`(80/48/24/16/8)與 `--gap`、`--radius` 取值,**不准寫 magic number**
(不要出現 `padding:13px`、`gap:22px`、`margin-top:35px` 這種)。

為什麼:AI 排版最容易出的問題是「每個區塊間距都差一點點」,單看每頁都還好,
連續翻頁時觀眾會感覺畫面在微微晃動。鎖死 8 的倍數,節奏就穩了。

**兩個例外**:
- **字級**不套網格,走四階比例(約 1.6 倍,階層對比才夠),且一律用 `clamp()`——見 E 條
- **1px / 2px / 3px** 的細線(border、進度條)不算間距,照舊

自檢方式:產出 HTML 後 grep 一次,有命中就回頭改成變數。

```bash
grep -oE "(padding|margin|gap|border-radius)[^;]*:[^;]*[0-9]+px" slides.html | grep -vE ":\s*(0|8|16|24|32|40|48|56|64|72|80|96|1|2|3)px"
```

### E. 投影可讀性下限(**比美觀優先**)

本技能用**滿版 responsive**(`inset:0`),不是固定 1920 畫布再縮放。
兩者的差別決定了字級不能寫死:

> **固定畫布**:字跟著畫布一起縮放,寫 13px 到哪都是「畫布的 13/1080」。
> **滿版 responsive**(本技能):寫 13px 就是**螢幕上真的 13 個像素**——
> 螢幕越大,字佔畫面的比例反而越小。

實測換算(內文字高佔畫面高度):

| 內文字級 | 768p 投影 | 1080p 投影 | 教室後排看得到嗎 |
|---|---|---|---|
| 13px(舊值) | 1.69% | **1.20%** | ❌ 大約只有需要量的一半 |
| 20px | 2.60% | 1.85% | ⚠️ 勉強 |
| 24px | 3.13% | **2.22%** | ✅ |

**硬性下限:內文字高 ≥ 畫面高的 2.2%**(10 公尺後排可讀)。
所以字級一律用 `clamp(最小值, vw, 最大值)`,讓它跟著視窗長大:

```css
/* 四階比例維持約 1.6 倍,但基準拉高並隨視窗縮放 */
--t1: clamp(40px, 3.6vw, 68px);   /* 主標 */
--t2: clamp(26px, 2.2vw, 42px);   /* 次標 */
--t3: clamp(18px, 1.4vw, 26px);   /* 小標 / 導言 */
--t4: clamp(15px, 1.1vw, 21px);   /* 內文 —— 這一階最常被寫太小 */
```

1920 寬時約 68 / 42 / 26 / 21,階層比例與林長揚原始比例一致,但**內文大了 60%**。

> **代價要知道**:字變大 → 每頁裝得下的字變少 → **頁數會增加**。
> 這是對的方向,不是缺點——**寧可 30 頁看得清楚,不要 10 頁看不到**。
> 溢出時的處理順序見第 7 步:**先拆頁,不要縮字**。

---

## 執行流程

### 第 1 步:讀懂素材、規劃章節

讀取素材後,先輸出 **章節骨架**給使用者確認,每頁標註:
- 標題(≤10 字)
- 核心訊息(1-2 句)
- 所屬 SOIL 段(動機/注意/行動)
- 是否需要 AI 生圖
- 是否需要互動元件

**等使用者點頭再進下一步。**

### 第 2 步:統一視覺風格(產出 CSS 變數區塊)

```css
:root{
  --bg:#0a0e27; --bg-2:#11163a;
  --ink:#eef3ff; --ink-2:#b8c5e0; --ink-3:#7a8bb8; --ink-4:#4a5680;
  --accent:#00d4ff;   /* 主強調色,僅 1 種 */
  --accent-2:#ff006e; /* 輔強調色,僅 1 種 */
  /* 字級走林長揚階層(比例約 1.6 倍),刻意不套 8px 網格;
     一律 clamp() 隨視窗縮放,不要寫死 px(理由見設計憲法 E) */
  --t1: clamp(40px, 3.6vw, 68px);
  --t2: clamp(26px, 2.2vw, 42px);
  --t3: clamp(18px, 1.4vw, 26px);
  --t4: clamp(15px, 1.1vw, 21px);
  /* 間距一律 8 的倍數:padding / margin / gap / 圓角只能取這幾個值 */
  --s1:80px; --s2:48px; --s3:24px; --s4:16px; --s5:8px;
  --gap:24px; --radius:16px;
}
```

### 第 3 步:批次平行生圖(用 draw 技能) —— **選用,沒有金鑰就跳過**

> **⚠️ 先探金鑰,再決定要不要走這一步。**
> 動手生圖前先跑一次探測,**不要等生到一半才失敗**:
>
> ```powershell
> python -X utf8 "<技能資料夾>\ppsh-draw\draw.py" --probe
> ```
>
> | 結果 | 怎麼做 |
> |---|---|
> | 印出 `gemini`,離開碼 0 | 照本步驟批次生圖 |
> | 印出 `[no-key]`,**離開碼 3** | **跳過整個第 3 步**,改走下方「無生圖版面」。這不是錯誤,不要重試、不要中斷整份工作 |
> | **找不到 draw.py**(沒安裝 `draw` 技能) | **同上,視為沒有金鑰**,直接走無生圖版面。不要去安裝 `draw`,不要找替代生圖工具 |
>
> **無生圖版面(零金鑰預設路徑)**:所有視覺一律改用**向量**——CSS 漸層背景、
> 內嵌 SVG 幾何圖形、圖示字元、色塊分割。第 4 步的 base64 內嵌直接跳過,
> 原本放圖的位置改放 SVG。**成品一樣是完整的一份簡報,只是沒有 AI 插圖。**
> 做完要主動告訴使用者:「本機未設定生圖,已用向量版面完成;要 AI 插圖見懶人包 03 附錄。」

**所有圖像呼叫一次性平行發出**,不要序列等待。呼叫方式:

```powershell
python -X utf8 "<技能資料夾>\ppsh-draw\draw.py" "<提示詞>" --size 1536x1024 --name hero
```

預設參數:
- `--quality low`(99% 場景夠用)
- `--size 1536x1024`(滿版/對比圖)或 `1024x1024`(類型卡)
- 存到專案資料夾的 `slides/generated/`（Codex 內建生圖的成品也複製到這裡）

**Prompt 原則**:
- 風格詞統一(例:`Premium futuristic tech aesthetic, dark navy background, cyan and magenta neon accents`)
- 寫明 `No readable text`(避免亂碼文字)
- 留出文字疊放區域(`with negative space at bottom for text overlay`)
- 比例配合用途(滿版用 16:9,卡片用 1:1)

### 第 4 步:Base64 內嵌圖像(關鍵步驟)

⚠️ **不要用相對路徑**。預覽面板、檔案搬移、跨環境分享都會壞掉。
一律用 Pillow 壓縮 + base64 內嵌成 `data:image/jpeg;base64,...`:

```python
from PIL import Image
import base64, io
img = Image.open(path).convert('RGB')
w, h = img.size
target_w = 1280 if is_full_bleed else 900
if w > target_w:
    img = img.resize((target_w, int(h*target_w/w)), Image.LANCZOS)
buf = io.BytesIO()
img.save(buf, 'JPEG', quality=78, optimize=True)
b64 = base64.b64encode(buf.getvalue()).decode()
data_uri = f"data:image/jpeg;base64,{b64}"
```

5 張圖內嵌後 HTML 約 1.3-1.6 MB,完全可攜。

### 第 5 步:產出單一 HTML(架構模板)

**整體結構**:
```html
<body>
  <div id="progress"></div>          <!-- 頂部進度條 #23 -->
  <div id="section-tag"></div>       <!-- 左上 SOIL 章節標籤 -->
  <div id="pageInfo"></div>          <!-- 右下頁碼 -->
  <div id="hint"></div>              <!-- 左下快捷鍵提示 -->

  <section class="slide active" data-slide="1" data-section="引起動機">...</section>
  <section class="slide" data-slide="2" data-section="引起動機">...</section>
  ...

  <script>切頁 / 排序 / Chart.js 邏輯</script>
</body>
```

**slide 容器(滿版,不要做 1920×1080 縮放)**:
```css
.slide{
  position:absolute; inset:0;
  display:flex; align-items:center; justify-content:center;
  padding:var(--s1) 96px;   /* 8 的倍數,不寫 100px */
  opacity:0; pointer-events:none;
  transition:opacity .55s ease, transform .55s ease;
  transform:translateY(16px);
  overflow:hidden;
}
.slide.active{ opacity:1; pointer-events:auto; transform:translateY(0); }
.slide-inner{ width:100%; max-width:1320px; }
```

⚠️ **不要使用固定 1920×1080 + scale 縮放舞台的架構**。
理由:在小型預覽面板(如 Claude Code 的 Launch preview)會被縮成極小,字會擠成一團,觀感極差。
直接用 `position:absolute; inset:0` 滿版,讓內容跟著視窗大小撐滿就好。

**必備 UI 功能**:
1. **左右鍵 / 空白鍵切頁**(JS keydown)
2. **點擊畫面左右側切頁**(`x > 0.7*innerWidth → next`)
3. **F 鍵全螢幕**
4. **頁碼顯示**(右下角 `當前 / 總數`)
5. **頂部進度條**(切頁時動畫)
6. **章節標籤**(左上,讀 `data-section` 即時切換)
7. **每頁淡入動畫**
8. **E 鍵匯出當前頁 PNG**(見第 8 步)

### 第 5.5 步:數學式、物理公式、化學式(有公式的單元必做)

用 **KaTeX + mhchem 擴充**:排版品質等同方程式編輯器／LaTeX,速度比 MathJax 快,而且不用安裝任何東西(CDN 載入)。
**不要**用 Unicode 硬拼上下標(v₀²、H₂O)、**不要**把公式截圖、**不要**手刻 `<sup>`/`<sub>`:分數、根號、向量箭頭都會排壞。

`<head>` 加這四行(版本號固定,不要寫 `@latest`):
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/mhchem.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
```

`</body>` 前加:
```html
<script>
  // $...$ 行內公式、$$...$$ 獨立一行置中;寫法和 ppsh-soil-teaching-deck 的 pptx 公式工具一致
  document.addEventListener("DOMContentLoaded", () => {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false }
      ],
      throwOnError: false   // 單一公式寫錯只會顯示紅字,不會整頁壞掉
    });
  });
</script>
```

CSS 加一行讓公式和中文一樣大、跟著主題色:`.katex{font-size:1.1em;color:inherit}`

**寫法速查**(直接寫在 HTML 文字裡):

| 要的效果 | 寫法 |
|---|---|
| 分數、平方 | `$K=\frac{1}{2}mv^2$` |
| 文字下標 | `$W_{\text{net}}$` |
| 希臘字母 | `$\Delta K$`、`$\theta$`、`$\lambda$` |
| 向量、根號、積分 | `$\vec{F}=m\vec{a}$`、`$v=\sqrt{2gh}$`、`$W=\int_{x_1}^{x_2}F\,dx$` |
| 化學反應式 | `$\ce{2H2 + O2 -> 2H2O}$`、`$\ce{N2 + 3H2 <=> 2NH3}$` |
| 離子、狀態 | `$\ce{Fe^{3+}}$`、`$\ce{CaCO3(s)}$`、`$\ce{SO4^2-}$` |
| 獨立一行的大公式 | `$$x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$$` |

- **用 JS 字串動態塞公式時**(例如互動題、Chart.js 標籤)反斜線要寫兩次(`"\\frac"`),或用 `` String.raw`...` ``;
  塞完要再呼叫一次 `renderMathInElement(那個元素, 同樣的設定)`。
- 文字裡真的要顯示錢字號時寫 `\$`,不然會被當成公式開頭。
- **沒網路的場地**:KaTeX 要從 CDN 載字型。上課場地可能沒網路時,把公式多的頁面用 `ppsh-soil-infographic` 的
  `render.py --transparent` 拍成透明 PNG,照第 4 步 base64 內嵌(不能再改,但離線也一樣漂亮)。
- 驗收:第 7 步逐頁檢查時,確認畫面上**沒有殘留的 `$` 符號或紅字**(那代表公式沒轉成功)。

### 第 6 步:加入互動元件(這就是本技能的價值)

依章節骨架,在對應頁加入:

| 元件 | 適用頁型 | 實作 |
|------|----------|------|
| **三欄卡片** | 總覽頁、決策頁 | `display:grid; grid-template-columns:repeat(3,1fr)` + AI 圖嵌入卡內 |
| **左右並排圖文** | 類型詳解頁 | `display:grid; grid-template-columns:1fr 1fr` + Z 字翻轉 |
| **可排序表格** | 對比頁 | 點 `<th>` 觸發 sort,搭配 AI 對比視覺圖 |
| **Chart.js 雷達 / 折線圖** | 數據頁 | lazy render(切到該頁才初始化) |
| **SVG 決策樹** | 決策頁 | 中央問句 + SVG `<line>` 連到三張結果卡 |
| **滿版背景圖** | 封面、結尾 | 圖層 `position:absolute;inset:0` + 漸層遮罩 |
| **流程卡 2×3 grid** | 方法論頁 | 不要用 1×6,會太擠 |

### 第 7 步:版面溢出檢查(逐頁驗收)

每頁打開後檢查:
- [ ] 內容是否在標準 1920×1080 / 1366×768 視窗下完整顯示
- [ ] 沒有元素被視窗高度截掉
- [ ] 字級階層清楚(主標明顯大於內文)
- [ ] 圖文比例舒適(不擠不空)
- [ ] 章節標籤、頁碼、進度條都正常更新

如果某頁溢出,**優先做的事**(依序試,不要跳過前面直接改字級):
1. **把內容拆成兩頁** —— 本技能不限頁數,**這永遠是第一選擇**
2. 換成 2×N grid(避免 1×N 一字排開太擠)
3. 刪掉可有可無的句子(一頁一重點,其餘都是雜訊)
4. 縮短 padding(96px → 56px,仍守 8 的倍數)
5. 圖片改成 `aspect-ratio:1/1` 縮成正方形

⚠️ **絕對不要調小 `--t1`~`--t4` 來救溢出**。
那會同時破壞階層、又讓投影看不清楚——**兩個問題換一個問題,不划算**。
字級是可讀性的底線,頁數不是。

### 第 8 步:PNG 匯出(頁內 E 鍵 + 批次腳本)

簡報做完常常還要「發一張預告圖到 LINE 群」「把某頁貼進公文或研習手冊」。
所以每份 HTML 都要**內建把當前頁轉成 2× PNG 的能力**,不要事後再用手機拍螢幕。

**(a) 頁內 E 鍵匯出(必做)**

用 `html-to-image` UMD 版,配合本技能「圖片一律 base64 內嵌」的設計——
因為沒有外部圖片,不會踩到 canvas 的跨域污染問題,截圖一定成功。

```html
<script src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.min.js"></script>
<script>
async function exportPNG(){
  const el = document.querySelector('.slide.active');
  const n  = el.dataset.slide;
  const url = await htmlToImage.toPng(el, {
    pixelRatio: 2,                                   // 2× 高 DPI,社群平台夠用
    backgroundColor: getComputedStyle(document.body).backgroundColor
  });
  const a = document.createElement('a');
  a.href = url; a.download = `slide-${String(n).padStart(2,'0')}.png`; a.click();
}
document.addEventListener('keydown', e => {
  if (e.key === 'e' || e.key === 'E') exportPNG();
});
</script>
```

左下角快捷鍵提示要一起加上 `E 匯出本頁 PNG`。

⚠️ 三個已知限制,產出時要注意:
- `backdrop-filter`(玻璃擬態)在部分瀏覽器截不出來 → 卡片同時給一個半透明 `background`
  當保底,截圖才不會變全透明
- 這條 CDN 需要網路。若簡報要在**沒網路的場地**播,或要發成 Artifact
  (Artifact 的 CSP 只放行 Google Fonts,擋掉其他 CDN)→ 把整包 JS 內嵌進 `<script>`
- Chart.js 是 canvas,截得到;但要先切到該頁讓它 render 完再按 E

**(b) 批次匯出全部頁(選用)**

要一次出整份講義圖時才做,需要 Playwright(`pip install playwright && playwright install chromium`)。
環境沒裝就跳過,別為了截圖硬裝一包東西——**先問使用者要不要**。

```python
# export_slides.py — 逐頁截圖到 slides/exports/
from playwright.sync_api import sync_playwright
from pathlib import Path

OUT = Path('slides/exports'); OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width':1920,'height':1080}, device_scale_factor=2)
    pg.goto(Path('slides.html').resolve().as_uri())
    total = pg.eval_on_selector_all('.slide', 'els => els.length')
    for i in range(total):
        if i: pg.keyboard.press('ArrowRight')
        pg.wait_for_timeout(800)          # 等淡入動畫與 Chart.js render
        pg.locator('.slide.active').screenshot(path=OUT / f'slide-{i+1:02d}.png')
    b.close()
print(f'已匯出 {total} 頁 → slides/exports/')
```

### 第 9 步:驗收與輸出

1. 用 Bash 開啟產出的 HTML(`start slides.html`)
2. 切完每一頁,確認互動元件都正常
3. 隨手按一次 E,確認 PNG 匯得出來且沒有透明破圖
4. 跑一次第 D 條的 8px 網格 grep,有漏網的 magic number 就修掉
5. 報告檔案路徑與功能清單給使用者

---

## 輸出規範

```
專案資料夾/
├── slides.html              ← 單一 HTML(base64 內嵌圖,~1.5 MB)
├── slides/
│   ├── generated/           ← AI 生成圖原始 PNG(備份用)
│   │   ├── slide-1-cover.png
│   │   └── ...
│   └── exports/             ← (選用)批次截圖的每頁 PNG
│       ├── slide-01.png
│       └── ...
├── export_slides.py         ← (選用)Playwright 批次截圖腳本
└── README.md                ← 使用說明 + 鍵盤快捷鍵
```

---

## 風格範本(預設「現代深色 + 霓虹點綴」)

| 項目 | 值 |
|------|----|
| 背景 | `#0a0e27`(深藍黑) |
| 主色 | `#00d4ff`(霓虹青) |
| 輔色 | `#ff006e`(亮粉) |
| 警示 | `#ffb800` / `#ff4466` |
| 標題字體 | `Noto Sans TC` 700/900 |
| 內文字體 | `Noto Sans TC` 400 |
| Mono 字體 | `JetBrains Mono`(用於 kicker、頁碼、tag) |
| 卡片 | 玻璃擬態(`backdrop-filter: blur(10px)`) |

---

## 與其他技能的串接

- **draw**(**選用**):平行批次生成所有頁面的 AI 圖。**沒有金鑰就跳過,改走向量版面**(見第 3 步)——本技能在零金鑰狀態下仍能產出完整簡報
- **ppsh-office-reader**(選用):素材是 Word／PDF／簡報／Excel 時,先轉成文字再進引擎一
- **ppsh-soil-teaching-deck**(姊妹):同時要產 .pptx 版本可平行呼叫

---

## 給其他 Agent 的呼叫提示

如本技能被其他 agent(如 GPT Codex)讀取使用,請遵守:
1. 每頁的 HTML 結構必須一致(`<section class="slide" data-slide="N" data-section="...">`)
2. 圖像一律 base64 內嵌,**不用相對路徑**
3. 所有 JS / CSS 內嵌或用 CDN(Chart.js / Google Fonts / html-to-image),不要產生需要 build 的 React/Vue 專案
4. 預設輸出單一 `.html`,使用者要的是「打開即用」,不是 dev server
5. 不要用固定 1920×1080 + transform scale 的架構,直接用 `position:absolute; inset:0` 滿版
6. 每頁要遵守林長揚 30 原則 + SOIL 三段式脈絡
7. 數學、物理、化學式一律用 KaTeX + mhchem(見第 5.5 步),不用 Unicode 上下標或截圖

---

## 踩坑紀錄(2026-05-02 直播 demo 累積)

| 坑 | 解法 |
|----|------|
| 預覽面板看不到圖(中文路徑或沙箱) | base64 內嵌,**不用** 相對路徑 |
| AI 圖只當背景太可惜 | 用 grid 把圖跟內容區塊**並排融合**,圖片要切圓角 + 加角標 |
| 1920×1080 scale 在小視窗變超小 | 改用滿版 `inset:0`,內容跟視窗撐滿 |
| 決策樹用 ASCII 字符不夠視覺 | 改成中央問句 + SVG 連線 + 三張顏色不同的結果卡 |
| 6 引擎排成 1×6 太擠 | 改 2×3 grid,搭配左側 AI 視覺圖 |
| 對比頁只有表格太枯燥 | 左側放「左舊右新」對比視覺圖,右側放可排序表 |
| 標題太長破版 | 嚴守 ≤10 字原則 |
| 強調色超過 2 種畫面亂 | 主 cyan + 輔 magenta + 警示色,其餘一律淡灰 |
| **投影出來內文看不清**(2026-09-16) | 固定 13px 配滿版 responsive,在 1080p 只佔畫面高 1.2%,不到可讀門檻的一半。改用 `clamp()` 見設計憲法 E |
| **為了不超過頁數上限而硬擠** | 本技能**不限頁數**。擠成一頁的代價是沒人看得清楚 |
