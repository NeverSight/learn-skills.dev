---
name: ppsh-word-writer
description: 寫 Word 檔 — 用 python-docx 新建 Word（批閱結果、考卷、計畫草稿、會議紀錄），或照老師確認過的修訂內容另存一份修訂稿；原檔一律不動。當使用者要你「寫成 Word」「產出 docx」「做成 Word 檔」「把修改寫進 Word」時使用。
---

# 寫 Word 檔（屏北高中版）

讀 Word 用 `ppsh-office-reader`；**寫** Word 用這個技能。

## 先分清楚是哪一種

| 情況 | 做法 |
|---|---|
| **新建**：批閱結果、考卷、會議紀錄、計畫草稿 | 用 python-docx 直接產生新檔（第 2 節） |
| **改既有的 Word**：計畫書、公文、別人給的表件 | **預設不寫回。** 產出「修訂對照表」（位置｜原文｜修改後｜理由），請老師自己貼回 Word。<br>老師**明確要求**時，才另存一份修訂稿（第 3 節），原檔不動 |

既有文件常有合併儲存格、隱藏格式、核章欄。程式改寫可能動到看不見的排版，而送出去的正式文件要由老師負責，所以預設交給老師貼。

## 1. 確認套件

```powershell
python -X utf8 -c "import docx; print('python-docx OK')"
```

- 出現 `python-docx OK` → 繼續。
- `ModuleNotFoundError` → **先把下面這行指令給老師看、經同意後**再執行：
  ```powershell
  python -X utf8 -m pip install python-docx
  ```
- `python` 跳出 Microsoft Store 或沒反應 → 那是市集空殼。用 `py -0p` 看有哪個版本，把上面的 `python` 換成 `py -3.13`（換成列出的版本）。

## 2. 新建 Word

- 程式寫成 `.py` 檔，放在專案的 `_scripts\` 資料夾再執行。不要把長程式塞進一行指令。
- 成品存在專案資料夾裡（例如 `研習成果\`），中文檔名沒問題。
- 標題用 Word 內建的「標題」樣式，老師在 Word 的導覽窗格才看得到章節。
- 表格用 `Table Grid` 樣式，印出來才有框線。

```python
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

doc = Document()
# 中文字型：英文字型和東亞字型都要設，只設一個的話，中文會被 Word 換成新細明體
st = doc.styles["Normal"]
st.font.name = "標楷體"
st.font.size = Pt(12)
st.element.get_or_add_rPr().get_or_add_rFonts().set(qn("w:eastAsia"), "標楷體")

doc.add_heading("批閱結果", level=1)
t = doc.add_table(rows=1, cols=3)
t.style = "Table Grid"
for c, h in zip(t.rows[0].cells, ["作品", "評分依據", "結果"]):
    c.text = h
doc.save(r"研習成果\批閱結果.docx")
```

## 3. 另存修訂稿（老師明確要求才做）

1. 先把原檔**複製**成 `<原檔名>_修訂稿.docx`，只改這份副本。
2. 只換文字，不重建表格：改儲存格時，把新文字放進該格第一個 run，其餘 run 清空，原本的字型、粗體就會保留。
3. 這些地方**不碰**，列在回報裡請老師自己處理：合併儲存格的結構、文字方塊、追蹤修訂、核章欄、頁首頁尾。
4. 改完用 `ppsh-office-reader` 把修訂稿轉成文字，逐條比對修訂對照表，回報「改成功幾處、哪幾處沒改到」。

## 4. 驗收（每次都要做）

- 用 `ppsh-office-reader` 讀回產出的檔案，確認段落和表格欄位都在。
- 有數字（分數、金額、人數）就讀回來**再加總一次**，跟對照表或原始資料比對。
- 提醒老師：「請用 Word 打開看一次排版，再送出或列印。」

## 不要做的事

- 不覆蓋、不搬動原檔；老師沒要求時，不把修改寫回既有文件。
- 不用 Word 的 COM 自動化：它會直接操作老師正在開的 Word 視窗。
- 檔案含學生姓名、成績、輔導資料時，比照 `ppsh-office-reader` 的個資提醒。

## 相關技能

- 讀 Word／PDF／簡報／Excel：`ppsh-office-reader`
