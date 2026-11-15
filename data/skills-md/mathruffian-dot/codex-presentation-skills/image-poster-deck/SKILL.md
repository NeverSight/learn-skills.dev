---
name: image-poster-deck
description: 使用 Codex 內建生成圖片能力，製作每頁為完整 AI 圖像的海報式、情境式或圖文融合簡報，並可將 PNG 頁面打包成圖片型 PPTX。當使用者要求圖片型簡報、純圖片簡報、AI 生圖簡報、海報式投影片、視覺衝擊簡報或不重視文字後續編輯時使用。
---

# AI 圖片型簡報

## 生圖方式

預設使用 Codex 內建 `image_gen` 工具，不需要 `OPENAI_API_KEY`。

不得為了一般品質、尺寸或批次需求改用 API／CLI。只有使用者明確要求 API、模型參數或 CLI 時，才說明另一路線需要 API Key。

## 適用情境

- 封面、章節頁、直播開場、社群分享。
- 圖像氣氛與視覺敘事比後續文字編輯更重要。
- 每頁文字可以壓縮成標題、短句或少量標籤。

若中文字、公式、題目或數值必須精準且可修改，改用 `image-editable-deck`。

## 工作流

1. 建立內容定位與頁面表。
2. 每頁只保留一個主張，將文字壓縮為適合生圖的短句。
3. 建立統一的風格、色彩、角色、材質與避免事項。
4. 逐頁撰寫圖片提示，規格見 `references/image-prompts.md`。
5. 每張投影片分別呼叫一次內建 `image_gen`。
6. 將選定圖片從 Codex 生成圖片位置複製到專案 `slides/images/`。
7. 逐頁檢查文字、構圖、比例、風格漂移、浮水印與多餘符號。
8. 失敗頁只針對單一問題重新生成。
9. 使用 `scripts/pack_pptx.py --mode baked` 打包圖片型 PPTX。
10. 渲染或開啟 PPTX，確認圖片沒有拉伸、裁切錯誤或順序錯誤。

## 圖片規則

- 預設 16:9 橫式全頁構圖。
- 圖中文字原則上不超過 20 個中文字。
- 不要求生成密集段落、資料表、長公式或小字標籤。
- 每頁提示必須寫明 exact text、文字位置與「不得增加其他文字」。
- 不用本機 CSS、SVG、Pillow 或色塊排版冒充 AI 生成圖片。
- 生成圖片必須複製到專案，不能只留在 Codex 預設生成位置。

## 打包

先安裝：

```powershell
pip install python-pptx Pillow PyYAML
```

再執行：

```powershell
python .\scripts\pack_pptx.py `
  --images-dir .\slides\images `
  --output .\slides\圖片型簡報.pptx `
  --mode baked
```

圖片命名使用 `page_01_*.png`、`page_02_*.png`。

## 交付

回報提示檔、圖片資料夾、PPTX、預覽位置、內建生圖使用狀態及需要重新生成的頁面。
