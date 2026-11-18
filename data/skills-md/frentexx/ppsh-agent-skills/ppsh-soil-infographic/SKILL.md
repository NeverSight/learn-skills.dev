---
name: ppsh-soil-infographic
description: >
  單頁資訊圖表（懶人包）技能。把要點、辦法、流程、統計整理成「一張圖看完」的 PNG，
  用 HTML + CSS + SVG 排版，再以 headless Chrome 渲染成高 DPI 圖檔。
  文字與數字 100% 精準可控，改一個字只要 3 秒重算，不會像 AI 生圖那樣糊掉或亂碼。
  當使用者說「做懶人包」、「做資訊圖表」、「做一張圖說明」、「做圖卡」、
  「一張圖看懂」、「做成 PNG」、「做張圖發 LINE 群」、「公告用的圖」、
  「把這份要點做成一張圖」、「infographic」時，請一定要使用此技能。
  **預設不呼叫 ppsh-draw 技能**：裝飾一律用向量 SVG，除非使用者明確說要 AI 插圖或精美圖卡。
  本技能與 ppsh-soil-html-deck 的差別：那是多頁簡報（要翻頁、深色、投影用），
  本技能是單頁圖檔（不翻頁、淺色、發出去給人看）。兩者不可互相代用。
---

> ## 📌 屏北高中研習版須知（先讀這段）
>
> **這個技能做什麼**：單頁資訊圖表（PNG）
> **要不要 API 金鑰**：✅ **零 API 金鑰**，只要 Chrome ＋ Python
> **研習定位**：本研習的主實作技能
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

# SOIL 單頁資訊圖表（ppsh-soil-infographic）

把「一份文件」壓成「一張圖」。輸出是 PNG，不是簡報。

> **與姊妹技能的分工（選錯就整份重做，務必先分清）**
> | 技能 | 產出 | 頁數 | 用途 |
> |------|------|------|------|
> | `ppsh-soil-infographic`（本技能） | **.png** | **1 頁** | 發出去讓人自己看 |
> | `ppsh-soil-html-deck` | .html | 10 頁 | 站在台上講 |
> | `ppsh-soil-teaching-deck` | .pptx | 多頁 | 對方要能編輯 |
> | `ppsh-soil-image-deck` | .pptx | 多頁 | 每頁一張 AI 圖 |

---

## 🚦 第 0 步：先問清楚，這一關不准跳

動工前**必須**先確認兩件事，用一到兩句問完，等使用者回答：

1. **單頁還是多頁？** 「一張圖看完」→ 本技能；「要一頁一頁講」→ `ppsh-soil-html-deck`。
2. **要不要 AI 插圖？** 預設**不要**（純 SVG）。使用者明講要精美圖卡、要插畫、要氛圍背景時，才搭配 `ppsh-draw`。

> **為什麼這一關是硬性的**：實測踩過——使用者說「資訊圖表」，被誤讀成「圖表（chart）」，
> 結果做出一份 10 頁深色簡報加 Chart.js 長條圖，方向全錯、三張生圖白花。
> **「資訊圖表」= infographic = 單張圖；「圖表」= chart = 長條圖圓餅圖。兩個不同的詞。**
> 只要問一句就能擋掉整份重做。

---

## 為什麼預設不用 ppsh-draw

| | 純 SVG（本技能預設） | ppsh-draw（AI 生圖，要付費金鑰） |
|---|---|---|
| 中文字 | 100% 正確 | 會糊、會亂碼 |
| 數字精準度 | 就是你寫的數字 | 不可信 |
| 改一個字 | 改一行、3 秒重算，其餘不動 | 整張重生，構圖還會變 |
| 成本 | 0 | 每張要錢 |
| 可重現 | 完全一致 | 每次都不一樣 |
| 放大 | 向量，印 A4 邊緣銳利 | 點陣，會糊 |

**判準：畫面上有「不能錯的字或數字」→ 純 SVG。** 要點、辦法、法規、流程、統計全屬此類——
字錯了是行政事故，不能交給生成模型。

**什麼時候才加 ppsh-draw**（使用者明確要求時）：
- 封面級的氛圍背景、情境插畫、寫實質感
- 作法：`ppsh-draw` 生**沒有文字**的底圖（prompt 寫明 `No readable text`）→ base64 內嵌當背景 →
  文字仍然用 HTML 排在上層。**絕不讓 AI 產生任何要被閱讀的字。**

---

## 執行流程

### 第 1 步：抽出素材（用程式，不要用 LLM 讀）

| 來源 | 用什麼 |
|------|--------|
| PDF | `python -X utf8 -c "import fitz; ..."`（PyMuPDF，本機已裝） |
| docx / pptx | officecli 的 `get` / `query`（**只讀不寫**） |
| xlsx | Python 直讀 |

程式解析 100% 保真且 0 token，LLM 讀反而會漏字。

### 第 2 步：擬內容骨架，給使用者確認

一張圖最多裝：**1 個標題 + 3 個大數字 + 4 張卡 + 1 行頁尾**。裝不下就是要砍，不是要縮字級。

列出你打算放的：
- 主標（≤12 字）＋ 一句副標
- 三個大數字（各要一個「這數字是什麼」的說明）
- 四張卡的標籤與結論句
- 頁尾依據與免責

**等使用者點頭再排版。**

### 第 3 步：複製 template.html 改內容

```bash
cp "<技能資料夾>\ppsh-soil-infographic\template.html" ./infographic.html
```

版型與配色已固定在 template，改內容就好。**不要重寫 CSS**，除非使用者要求換主題。

**版式尺寸**（body 的 width/height 要和 `render.py --size` 一致）：

| 用途 | 尺寸 | 輸出（2×） |
|------|------|-----------|
| 預設橫式（LINE 群、公告、A4 橫印） | 1536×1024 | 3072×2048 |
| 直式（IG 限動、小紅書） | 1080×1440 | 2160×2880 |
| 方形（FB／IG 貼文） | 1080×1080 | 2160×2160 |
| A4 直印（300dpi） | 1240×1754，`--scale 2` | 2480×3508 |

**有數學式、物理公式、化學式時**：用 KaTeX + mhchem，排出來和方程式編輯器一樣。不用另外安裝套件，`render.py` 渲染時會從 CDN 載入。
**不要**用 Unicode 硬拼上下標（v₀²、H₂O），也不要手刻 `<sup>`。`<head>` 加：

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/mhchem.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>.katex{font-size:1.1em;color:inherit}</style>
```

`</body>` 前加：

```html
<script>
  document.addEventListener("DOMContentLoaded", () => renderMathInElement(document.body, {
    delimiters: [{ left: "$$", right: "$$", display: true }, { left: "$", right: "$", display: false }],
    throwOnError: false
  }));
</script>
```

文字裡直接寫：`$K=\frac{1}{2}mv^2$`、`$W_{\text{net}}=\Delta K$`、`$\vec{F}=m\vec{a}$`、`$\ce{2H2 + O2 -> 2H2O}$`、`$\ce{Fe^{3+}}$`；
獨立一行的大公式寫 `$$...$$`；要顯示錢字號寫 `\$`。寫法和 `ppsh-soil-teaching-deck`／`ppsh-soil-html-deck` 相同。
第 5 步看圖時，確認畫面上**沒有殘留的 `$` 或紅字**（那代表公式沒轉成功）。

**只要一張透明背景的公式圖**（例如插進 pptx 或 html 簡報）：只放公式的小 HTML，`body{margin:0;background:transparent}`，
用 `render.py --size 寬x高 --transparent` 輸出。

### 第 4 步：渲染成 PNG

```bash
python -X utf8 "<技能資料夾>\ppsh-soil-infographic
ender.py" infographic.html --out 懶人包.png
```

換版式時加 `--size 1080x1440`。腳本會自動找 Chrome／Edge、處理中文路徑、
等字體載完才快門，並在最後驗收輸出尺寸。

### 第 5 步：**一定要親眼看過再交件**

**先做一次零成本的文字檢查**——確認範本的佔位符全部填掉了：

```bash
grep -o "【[^】]*】" infographic.html
```

**有任何輸出就是還沒填完**，回去補。最常漏掉的是**頁尾右側那一格**，
它在版面最角落，眼睛掃版面時很容易跳過去。（這一條是實測漏掉一次才補上的。）

接著看圖：

```bash
python -X utf8 -c "from PIL import Image; im=Image.open('懶人包.png'); im.resize((1152,768), Image.LANCZOS).save('_check.png')"
```

用 Read 工具開 `_check.png` 檢查，交件前刪掉。**不看就交等於沒做**——
版面問題（文字被裝飾壓住、圖示畫壞、溢出）只有看圖才抓得到，程式檢查抓不出來。

逐項確認：
- [ ] 頁尾左右兩段文字**沒有被角落裝飾壓住**
- [ ] 每個 SVG 圖示都畫成該有的樣子（不是奇怪的線團）
- [ ] 沒有文字溢出卡片或被裁掉
- [ ] 主標一眼看到，三個大數字清楚
- [ ] 強調色只有紅、金兩種，其餘是墨綠與灰

### 第 6 步：交件

交**PNG**（那才是使用者要的東西），同時保留 `infographic.html` 供日後改字。
告知檔案路徑與尺寸。

---

## 版面規則

### 8px 基線網格
間距（padding／margin／gap／border-radius）一律取 `--s1~--s5`（64/32/24/16/8）與
`--gap`、`--radius`，**不准寫 magic number**。字級不套網格。

```bash
grep -oE "(padding|margin|gap|border-radius|height|width)[^;{]*:[^;}]*[0-9]+px" infographic.html | grep -vE ":\s*(0|8|16|24|32|40|48|56|64|72|80|96|1|2|3)px"
```

（版面尺寸 1536/1024、圖示尺寸這類本來就不是間距的值，命中可忽略。）

### 資訊密度
- 一張卡最多 **4 條**，每條最多 **1 行半**
- 大數字最多 **3 個**，多了就沒有一個突出
- 標籤（`.tag`）2–4 字，不要寫成句子

### 顏色
只有兩個強調色：**磚紅 `--red` 用於數字與警示**、**金褐 `--gold` 用於裝飾與項目點**。
墨綠 `--green` 是結構色（標籤底、圖示），不算強調色。其餘一律灰階。

---

## 踩坑紀錄

| 坑 | 解法 |
|----|------|
| 「資訊圖表」被讀成「圖表」，做成 10 頁簡報 | 第 0 步強制問「單頁還是多頁」 |
| 左下角織紋壓住頁尾文字 | **左下角永遠留白**，`.foot` 設 `z-index:2` |
| 自己手寫的 SVG 圖示路徑畫出怪東西 | 渲染後一定要開圖檢查；圖示寧可簡單也不要複雜 |
| 中文路徑餵給 Chrome 打不開 | `render.py` 用 `Path.as_uri()` 自動編碼 |
| 截圖拍到字體還沒載完的版本 | `--virtual-time-budget=12000` |
| html-to-image 匯出噴 SecurityError | Google Fonts 跨網域讀不到 cssRules → `skipFonts:true`，改用本機字體 |
| 頁面上的「下載 PNG」按鈕被拍進圖裡 | `render.py` 帶 `?shot=1`，頁面自己移除 `.ui-only` |
| 內容塞不下就縮字級 | 錯。要砍內容，不要縮字級 |

---

## 兩條匯出路徑（不要搞混）

| 路徑 | 誰在跑 | 用途 |
|------|--------|------|
| `render.py`（headless Chrome） | 我在後台跑 | 直接產出檔案交給使用者，字體尺寸完全受控 |
| 頁面右上「下載 PNG」（html-to-image） | 使用者的瀏覽器 | 使用者自己改完字後重新匯出 |

**html-to-image 不是生圖工具**，它只是把已渲染的 DOM 重畫成 PNG，
跟 AI 生圖那種「憑描述想像出一張圖」是完全不同的東西。

---

## 給其他 Agent 的呼叫提示

1. 輸出是 **單一 PNG**，HTML 只是中間產物
2. 裝飾用 **inline SVG**，預設不呼叫任何生圖 API
3. 所有文字寫在 HTML 裡，**不准讓 AI 產生要被閱讀的字**
4. 交件前必須把 PNG 縮圖讀進來親眼確認版面
5. 間距守 8 的倍數，強調色只有兩種
