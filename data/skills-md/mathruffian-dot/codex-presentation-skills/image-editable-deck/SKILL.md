---
name: image-editable-deck
description: 使用 Codex 內建生成圖片能力製作無字 AI 投影片背景，再以 PowerPoint 原生文字框疊加精準、可編輯的中文、公式、題目與標籤。當使用者要求 AI 圖片背景、無字背景、圖片型但文字可編輯、正式中文教學簡報、題目簡報或需要後續修改文字時使用。
---

# AI 背景可編輯簡報

## 生圖方式

預設使用 Codex 內建 `image_gen` 工具，不需要 `OPENAI_API_KEY`。

每張背景分別生成。只有使用者明確要求 API／CLI 時，才改走需要 API Key 的替代路線。

## 核心分層

每頁拆成：

1. `background prompt`：無字視覺背景、場景、圖像或裝飾。
2. `editable text`：精確中文、數值、公式、題目、標籤與講者提示。

所有必要資訊都放在 PowerPoint 原生物件中，不依賴圖片裡的文字。

## 工作流

1. 建立頁面表與視覺系統。
2. 為每頁指定文字保留區、背景構圖與可編輯文字內容。
3. 依 `references/background-prompts.md` 建立無字背景提示。
4. 每張背景分別使用內建 `image_gen` 生成。
5. 將選定背景複製到專案 `slides/backgrounds/`。
6. 檢查背景沒有文字、字母、數字、標籤、logo 或浮水印。
7. 建立 `spec.yaml`，格式見 `references/spec-format.md`。
8. 使用 `scripts/pack_pptx.py --mode plate` 疊加可編輯文字。
9. 使用 Presentations 能力或 PowerPoint 渲染全部頁面。
10. 修正對比、文字溢出、背景干擾與裁切問題。

## 背景規則

- 提示必須明確要求：無文字、無字母、無數字、無標籤、無 logo、無浮水印。
- 指定文字安靜區的位置與比例，例如「左側 42% 深色乾淨區」。
- 不要生成假圖表、假公式或需要精準判讀的數據。
- 圖片只負責氣氛、情境與視覺隱喻；內容正確性由可編輯物件承擔。
- 不使用 OCR 抹字作為預設流程。只有轉換既有圖片簡報時才使用 OCR 修復。

## 打包

先安裝：

```powershell
pip install python-pptx Pillow PyYAML
```

再執行：

```powershell
python .\scripts\pack_pptx.py `
  --images-dir .\slides\backgrounds `
  --output .\slides\AI背景可編輯簡報.pptx `
  --mode plate `
  --spec .\slides\spec.yaml
```

## 品質檢查

- 所有重要文字均可編輯。
- 背景未產生偽文字或干擾區塊。
- 文字與背景對比足夠。
- 圖片未拉伸，裁切不影響主體。
- 中文、數學符號、數值與來源正確。
- PPTX 可重新開啟並逐頁渲染。

## 交付

回報背景資料夾、提示檔、`spec.yaml`、PPTX、預覽位置與逐頁檢查結果。
