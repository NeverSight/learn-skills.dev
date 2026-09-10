---
name: codex-ppt-style-expanded
description: Create multi-style PowerPoint decks with AI-generated backgrounds and independently editable text. Use for audience-aware slide planning, Image 2 style expansion, up to five comparable style samples, editable draw.io flowcharts, and PPTX production.
---

# SlideWeave｜圖敘簡報

衍生自 ningzimu/codex-ppt-skill 的內容、大綱、樣張、逐頁檢查流程，結合 freestylefly/awesome-gpt-image-2 的風格與提示詞索引。這是獨立衍生版；不需要先安裝兩個上游 Skill。來源版本與授權見 [SOURCES.md](SOURCES.md)。

## 核心契約

- 預設產出「AI 背景 + 原生 PowerPoint 文字」；標題、內文、引用、頁碼、圖表標籤不烘焙進圖片。使用者明確要求整頁圖片模式時才改用該模式，並說明其文字不可單獨編輯。
- 背景由可用的圖片生成工具製作。使用者指定 Image 2 時，核實工具是否公開模型資訊；工具未揭露模型便記錄「內建生圖，模型未公開」，不得宣稱已驗證為 gpt-image-2。如使用者要求精確型號，取得可指定該型號的後端後才生圖。
- 本 Skill 採用原始風格檔的視覺描述，不採用其中「所有文字由生圖完成」「full-slide image」等製作要求。這項分層契約優先於內附風格素材。
- 樣張就是可編輯 PPT 的實際渲染預覽；不得拿整頁生成圖冒充最終分層效果。
- 數據與證據來自來源資料；AI 圖只作視覺素材。論文圖、Logo、截圖等指定素材以原始檔置入，避免透過生圖重繪改變內容。

## 工作流程

### 1. 理解任務
先依 [references/conversation-intake.md](references/conversation-intake.md) 做輕量需求訪談：沿用已知答案，先釐清用途、受眾、時間、素材與真實身份背景，再給內容判斷與風格建議。此流程參考 ppt-image-first 的提問方法，不沿用其全頁圖片或強制確認關卡。
讀取 [references/presentation-modes.md](references/presentation-modes.md)，將使用情境、時間格式與視覺風格分開設定。研究模式與 PechaKucha 可以組合；樣張不冒充完整限時簡報。
讀取來源，整理主題、受眾、先備知識、溝通目標、時間/頁數、投影或閱讀、語言、品牌限制、必須保留的素材。沿用已知答案；每輪最多三個必要問題，避免每個階段重複要求確認。使用者只有主題時，先給合理假設與初步大綱。

在專案內保存 `brief.md` 和 `outline.md`。逐頁記錄主張、內容、來源、頁面角色、必要素材。受眾決定解釋深度；風格不能取代內容準確性。

### 2. 搜尋與收斂風格
先查閱 [references/style-catalog.json](references/style-catalog.json) 的 27 種完整圖例索引。目錄封面 kind 為 generated-cover-reference，是繁中點陣示意圖，不能冒充可編輯 PPT 預覽。實際樣張仍需無字背景與原生文字分層。圖片為線上預覽連結或儲存庫根目錄相對路徑；獨立安裝 Skill 時可至 GitHub README 查看圖片。
讀取 [references/style-expansion.md](references/style-expansion.md)。優先採用使用者明確指定的風格或參考圖；本系列預設以 codex-ppt 上游的原始風格與實際圖片為視覺基準，尤其手繪技術解釋、科研及創意雜誌。新增配方作為可選延伸，不能取代使用者喜歡的原始美學。沒有指定時推薦三種，最多五種。每種附配色、圖像語言、密度、適用原因。五種是每輪比較上限，不是風格庫容量上限。

用 `python scripts/search_styles.py --query "醫療 教學 illustration" --limit 5` 查詢；原始資料與衍生配方皆可离線讀取。詞彙搜尋只作檢索，不把分數當作美學判斷。

### 3. 直接製作可比較樣張
有足夠的內容與 1–5 個合理候選後，使用同一份代表性內容、相同比例與大致相同資訊量，但各風格需有適合自己的構圖、文字層級與圖文關係。不要把同內容誤解成同版型，不以換配色或右側裝飾圖冒充風格差異。為每種候選生成一張無字背景，組裝原生文字，渲染成樣張供討論。不要先額外要求使用者從風格名稱選出唯一一種才能看圖。

一般先做內容頁，縮小到一至兩種後可补封面、資料密集頁。已指定唯一風格時只做該風格。實際生圖前確認可用工具並說明後端，不要求使用者重複授權已指定的工具。若工具不可用，保存提示詞與規格並指出缺項，不用本機假背景冒充 AI 產物。

保存 `samples/<style-id>/` 下的背景、PPTX、渲染圖與 prompt。展示預覽，請使用者選擇或描述調整；此時尚未授權的整套製作等待回覆。若使用者已明確授權自選風格完成整套，直接選擇並記錄理由。

### 4. 鎖定規格與逐頁製作
內容含流程、分支、泳道或系統架構時，讀取 [references/flowcharts.md](references/flowcharts.md)，使用內建 `vendor/drawio-skill/` 產出可編輯 `.drawio`。依需求選擇 PPT 圖片置入或原生節點重建，清楚記錄可編輯層級；不要用 AI 圖生成正式流程標籤。
讀取 [references/production.md](references/production.md)。把選定配色、字體、版型、背景材質、文字安全區、樣張路径及實際生圖後端記入 `design-spec.json`。記錄混搭的具體規則，例如只採 B 的插畫，不把多個完整風格隨機混用。

依每頁角色改變版型，保持同一視覺語言。背景與文字共用座標規劃，先規劃整頁的圖文敘事、流程或比較，再生圖並加入原生文字。插畫、箭頭與標籤應共同解釋內容，文字可散佈於對應節點，不強制左側留白。單頁修改只重製受影響的素材或文字；不要重生整份簡報。

### 5. 檢查與交付
檢查每頁來源對應、文字可編輯性、字級、溢出、遮擋、背景對比、版型變化與跨頁一致性。渲染每頁實際 PPTX 並檢視；若無渲染工具，明示「結構已檢查、視覺尚未驗證」，不能宣稱完整 QA。

交付 PPTX、原始背景、預覽、內容大綱、設計規格、逐頁提示詞、可重建的程式/資料，以及有需要時寫入備註的講稿。風格保存於本次專案；使用者要求跨專案保存時才複製到其指定的個人風格位置。

## 工具

- `scripts/search_styles.py`：查原始 11 種 PPT 風格、衍生配方和 Image 2 模板；支援 `--list`、`--show ID`。
- `scripts/assemble_editable.py`：基本原生文字/形狀/圖片/備註組裝器，輸入規格見 production.md。需 Python 與 python-pptx。資料圖表等超出此組裝器的頁面，使用環境既有 PPT 工具建立原生物件，不轉成圖片冒充可編輯。
- 生圖、參考圖片檢視和 PPT 渲染使用當前環境可用工具；遵循該環境的工具與 Skill 要求。沒有生圖或渲染能力時準確報告限制。

- 內建 draw.io：`vendor/drawio-skill/scripts/diagramctl.py`（環境檢查、IR、同步等）與 `validate.py`（結構檢查）。匯出需要 draw.io CLI；未自動註冊 MCP。
