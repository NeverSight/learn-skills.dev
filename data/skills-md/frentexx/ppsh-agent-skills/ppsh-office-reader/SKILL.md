---
name: ppsh-office-reader
description: 讀取 Office 與 PDF 文件 — 把 PDF、Word（docx）、PowerPoint（pptx）、Excel（xlsx）轉成文字後再閱讀、摘要或整理。當使用者要你「讀／看／摘要／整理」這類檔案，或給你 .pdf .docx .pptx .xlsx 的路徑時使用。只讀不改原檔。
---

# 讀取 Office 與 PDF 文件（屏北高中版）

AI 不能直接「看懂」Word、PowerPoint、Excel 的檔案格式。這個技能先把檔案轉成純文字，再交給你閱讀。轉檔工具有兩個，**依檔案類型挑**：

| 檔案 | 先用 | 第一個失敗時改用 | 讀不到 |
|---|---|---|---|
| Word `.docx`、舊版 `.doc`、`.odt`、`.rtf` | **anydoc** | MarkItDown（只限 `.docx`） | 文字方塊內的部分排版 |
| PowerPoint `.pptx`、舊版 `.ppt` | **anydoc** | MarkItDown（只限 `.pptx`） | 圖片裡的字 |
| PDF（文字版） | **MarkItDown** | anydoc | 掃描版 PDF 的文字（那其實是圖片） |
| Excel `.xlsx` | **MarkItDown** | — | **公式本身**（只看得到算出來的結果） |
| 舊版 `.xls` | — | — | 請老師先用 Excel 另存成 `.xlsx` |

**為什麼 Word 要先用 anydoc**：計畫書、經費表常有合併儲存格。MarkItDown 遇到合併儲存格會**少算一欄**，後面的金額全部往左錯一格；儲存格裡的分行也會被接成同一行（本校國教署計畫書實測）。anydoc 會保留空欄位與分行。

## 1. 確認工具在不在

```powershell
anydoc --version
markitdown --version
```

**anydoc 找不到指令** → 先檢查 `node --version`：
- 有版本號（20 以上）→ **先把下面這行指令給老師看、經同意後**再執行：
  ```powershell
  npm install -g @firecrawl/anydoc
  ```
  PowerShell 回「已停用指令碼執行」→ 改用 `npm.cmd install -g @firecrawl/anydoc`，並改用 `anydoc.cmd` 執行。
- 沒有 Node.js → 這次先只用 MarkItDown 讀，並告訴老師：「合併儲存格多的表格可能錯欄，數字請對照原檔。」

**MarkItDown 有顯示版本號**（例：`markitdown 0.1.7`）→ 繼續第 2 步。
**MarkItDown 找不到指令** → 先檢查 `uv --version`：
  - 有 uv → **先把下面這行指令給老師看、經同意後**再執行：
    ```powershell
    uv tool install "markitdown[pdf,docx,pptx,xlsx]"
    ```
    裝完若仍找不到指令，執行 `uv tool update-shell`，並請老師**重開 AI Agent 視窗**。
  - 沒有 uv → 停下來，告訴老師先照「屏北高中 Agent 基本功懶人包」的 **01-Office文件讀取工具** 安裝，不要自己亂找其他工具。

## 2. 轉檔（不改原檔）

輸出到專案資料夾裡的 `_轉文字` 資料夾，檔名沿用原檔：

```powershell
New-Item -ItemType Directory -Force "_轉文字" | Out-Null
# Word、PowerPoint：
anydoc "<原始檔案完整路徑>" -o "_轉文字\<原檔名>.md"
# PDF、Excel：
markitdown "<原始檔案完整路徑>" -o "_轉文字\<原檔名>.md"
```

macOS／Linux：

```bash
mkdir -p _轉文字
anydoc "<原始檔案完整路徑>" -o "_轉文字/<原檔名>.md"      # Word、PowerPoint
markitdown "<原始檔案完整路徑>" -o "_轉文字/<原檔名>.md"  # PDF、Excel
```

- 路徑有空格或中文，一定要用雙引號包起來。
- **絕對不要覆蓋或修改原始檔案。**
- **anydoc 絕對不要加 `--ocr hosted`**：這個選項會把整份檔案上傳到外部雲端服務（Firecrawl）做文字辨識。公文、計畫書、學生資料一律不准。
- anydoc 結束碼是 `3`＝這是掃描檔、需要 OCR，照第 5 節處理，不要改用 `--ocr hosted`。

## 3. 讀轉出來的文字

- 檔案很長時分段讀，不要一次塞進對話。
- 回答老師時，說明你是從哪一頁／哪一個工作表讀到的。

## 4. Excel 的兩個陷阱（實測過，回報時要主動提醒）

| 現象 | 原因 | 怎麼處理 |
|---|---|---|
| **座號 `01` 變成 `1`** | 轉檔時把文字當成數字，前導 0 被吃掉 | 以原始 Excel 為準；比對名單時不要只靠轉出來的座號 |
| 公式格顯示 `NaN` | 這個檔案沒有在 Excel 裡存過，沒有算好的結果可讀 | 請老師用 Excel 打開、存檔一次再轉 |

## 5. 讀不到內容時，老實說

轉出來幾乎是空的（常見於掃描版 PDF、拍照的講義）：

> 「這份檔案看起來是圖片，我讀不到文字內容。需要先做文字辨識（OCR），或請你提供文字版。」

**絕對不要在讀不到內容的情況下，照檔名或猜測寫出摘要。** 那份摘要會是編的。

## 6. 個資提醒

檔案若含學生姓名、學號、成績、輔導或健康資料：
- 先提醒老師：內容讀出來後會送到 AI 模型端處理
- 建議先去識別化（班級＋座號）再讀
- `_轉文字` 資料夾裡的副本同樣含個資，用完提醒老師刪除

## 不要做的事

- 不要修改、覆蓋、搬動原始檔案
- 不要把轉出來的內容上傳到其他網站或服務
- 讀不到時不要編造內容

## 相關技能

- 要寫成 Word 檔：`ppsh-word-writer`
- 初始化：`ppsh-project-init`
- 開工：`ppsh-startup`
- 收工：`ppsh-shutdown`
