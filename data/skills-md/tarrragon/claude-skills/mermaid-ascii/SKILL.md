---
name: mermaid-ascii
description: "Mermaid 圖表 ASCII 渲染工具。Use for: (1) 將 Mermaid 圖表轉為純文字 ASCII, (2) 在不支援圖形的環境中顯示流程圖, (3) 文件中嵌入文字版圖表"
metadata:
  version: 1.0.0
---

# Mermaid ASCII Renderer

純 Python 實現 Mermaid 圖表的 ASCII 渲染工具。

## 功能

- 支援 Mermaid flowchart、state diagram、sequence diagram、class diagram、ER diagram 等圖表類型
- ASCII 和 Unicode 雙輸出格式
- 支援檔案和 stdin 輸入
- 命令列工具和 Python 模組雙介面

## 套件結構

mermaid-ascii 是一個完整的 Python 套件（使用 hatchling 打包系統），包含以下元件：

```
.claude/skills/mermaid-ascii/
├── pyproject.toml                  # 套件配置（PEP 517 標準）
├── SKILL.md                        # 本文件
├── mermaid_ascii/                  # Python 套件
│   ├── __init__.py                 # 套件入口，導出公開 API
│   ├── mermaid_ascii_renderer.py   # 核心渲染引擎
│   └── scripts/
│       ├── __init__.py
│       ├── __main__.py             # 命令列模組入口（python -m mermaid_ascii）
│       └── render.py               # CLI 指令碼（mermaid-ascii 命令）
└── .venv/                          # 虛擬環境
```

## 安裝方式

### 開發環境安裝（推薦）

```bash
# 使用 uv 進行開發安裝
uv pip install -e .

# 之後可直接使用命令列工具
mermaid-ascii --input diagram.mmd --unicode
```

### 使用 uv 直接運行（無需安裝）

```bash
# 使用 uv 直接運行套件
uv run -C /path/to/mermaid-ascii --input diagram.mmd --unicode

# 或使用 stdin
cat diagram.mmd | uv run -C /path/to/mermaid-ascii --ascii
```

### 套件發布後的使用方式

```bash
# 從 PyPI 安裝
uv pip install mermaid-ascii

# 使用 uv run with 選項
uv run --with mermaid-ascii mermaid-ascii --input diagram.mmd --unicode
```

## 支援的圖表類型

目前支援以下 5 種 Mermaid 圖表類型的 ASCII 和 Unicode 渲染：

| 圖表類型 | 描述 | 主要用途 |
|---------|------|--------|
| Flowchart | 流程圖 | 表示系統或過程的流程和決策邏輯 |
| State Diagram | 狀態圖 | 表示對象或系統的不同狀態及其轉移 |
| Sequence Diagram | 序列圖 | 表示參與者之間的時間序列交互 |
| Class Diagram | 類別圖 | 表示系統中的類別結構和關係 |
| ER Diagram | 實體關係圖 | 表示資料庫設計中的實體和關係 |

詳細的圖表類型說明、支援的元素和使用範例請參考 [references/supported-diagrams.md](./references/supported-diagrams.md)。

## 使用方式

### 命令列（已安裝情況下）

```bash
# 從檔案輸入，輸出 Unicode 格式
mermaid-ascii --input diagram.mmd --unicode

# 從檔案輸入，輸出 ASCII 格式
mermaid-ascii --input diagram.mmd --ascii

# 從 stdin（pipe）輸入
cat diagram.mmd | mermaid-ascii --unicode

# 查看版本
mermaid-ascii --version
```

### Python 模組方式

#### 基本用法

```python
from mermaid_ascii import render_mermaid

diagram = """
flowchart TD
    A[開始]
    B[處理]
    C[結束]
    A --> B
    B --> C
"""

# 使用預設的 Unicode 格式渲染
output = render_mermaid(diagram)
print(output)
```

#### 進階用法（使用渲染器類別）

```python
from mermaid_ascii import MermaidAsciiRenderer

diagram = """
flowchart TD
    A[開始]
    B[處理]
    C[結束]
    A --> B
    B --> C
"""

# 建立渲染器實例
renderer = MermaidAsciiRenderer()

# 解析 Mermaid 語法
renderer.parse(diagram)

# 產生 Unicode 格式輸出
output = renderer.render()
print(output)
```

### 使用 Python 模組方式執行命令列

```bash
# 使用 python -m 執行模組（未安裝時）
python -m mermaid_ascii --input diagram.mmd --unicode

# 或管道輸入
cat diagram.mmd | python -m mermaid_ascii --ascii
```

## 命令列選項

### 輸入選項

- `--input FILE`, `-i FILE`
  - 指定輸入 Mermaid 檔案路徑
  - 省略時從標準輸入（stdin）讀取
  - 支援相對和絕對路徑

### 輸出格式選項

- `--ascii`
  - 輸出純 ASCII 字元（無 Unicode 方框字元）
  - 適用於不支援 Unicode 的終端環境
  - 與 `--unicode` 互斥

- `--unicode`
  - 輸出 Unicode 方框字元（預設行為）
  - 提供更好的視覺效果
  - 與 `--ascii` 互斥

### 其他選項

- `--version`
  - 顯示套件版本資訊

---

## 修改 source 後必須重新安裝

> **重要**：本 skill 透過 `uv tool install` 安裝為獨立 CLI，source（本目錄）與 installed（`~/.local/share/uv/tools/<package>/`）是兩份獨立 Python package。修改 source 後若未 reinstall，CLI 仍使用 stale installed 版本，新增的函式會 AttributeError 或被 hasattr 包裝靜默吞掉（W11-037 根因）。

**修復指令**：

```bash
cd .claude/skills/<本 skill 目錄> && uv tool install . --force --reinstall
```

**自動偵測**：每次 SessionStart 由 `uv-tool-staleness-check-hook` 比對 source vs installed SHA256，偵測 stale 時提示修復指令。對應 ticket-skill 本身另有 `ticket-reinstall-hook` 自動 reinstall。

---

版本紀錄在同目錄的 `CHANGELOG.md`。
