---
name: py-gui
description: >
  Build and review cross-platform Python desktop applications with tkinter, ttk, CustomTkinter, PySide6, or PyQt6. Use for windows, widgets, layouts, dialogs, system tray, background jobs, event loops, model-view separation, accessibility, high-DPI behavior, settings, packaging with PyInstaller or Nuitka, and fixing unsafe worker-thread UI updates.
compatibility: Agent Skills-compatible. GUI, native packaging, and platform integration require testing on each target operating system.
metadata:
  author: stevenke1981
  version: "2.0.0"
  last-reviewed: "2026-07-30"
---

# Python GUI 桌面應用

## 目標與邊界

用此 skill 建立可維護、不中斷 UI event loop、能正確取消背景工作的桌面應用。先選擇符合授權、平台與功能需求的框架，再設計狀態、執行緒與打包流程。

若只是終端機互動，使用 `py-cli`；若 UI 只是 Web 前端，使用對應 Web 技術，不要為了桌面外殼強行使用 Python GUI。

## 執行流程

1. **定義平台與交付方式**：Windows、macOS、Linux、安裝程式、portable、簽章與自動更新。
2. **選擇框架**：依 widget 複雜度、授權、原生整合、團隊經驗與打包成本決定。
3. **分離狀態與視圖**：domain/model 不 import GUI framework；view 不直接承擔資料存取與長任務。
4. **設計 event loop 邊界**：所有 UI 讀寫在主執行緒；背景工作只透過 queue、signal 或 message 回傳。
5. **加入取消與錯誤回報**：長工作可取消、可逾時，錯誤轉成使用者可理解訊息。
6. **驗證可用性**：鍵盤操作、focus、縮放、字型、深淺色、螢幕閱讀器與多螢幕。
7. **打包與原生測試**：在每個目標 OS 測試啟動、資源、權限、檔案關聯、更新與移除。

## 框架選擇

| 需求 | 優先考慮 | 注意事項 |
|---|---|---|
| 小型內部工具、零額外 GUI 依賴 | tkinter / ttk | 外觀與高階 widget 較有限 |
| 快速做現代化 tkinter UI | CustomTkinter | 仍遵守 Tk 主執行緒規則 |
| 大型桌面產品、model/view、WebEngine、多媒體 | PySide6 | Qt 官方 Python binding；確認 LGPL 義務 |
| 既有 PyQt 團隊或商業授權 | PyQt6 | 確認 GPL／商業授權條件 |
| 終端機全螢幕介面 | Textual | 改讀 `py-cli` 為主 |

不要只根據外觀選框架。原生能力、可測試性、授權與安裝包大小通常更重要。

## 主執行緒規則

- Tk、Qt 與大多數 GUI toolkit 都要求 UI 操作留在主執行緒。
- worker 不直接呼叫 widget method，也不要假設從 worker 呼叫 `after()` 永遠安全。
- worker 只處理計算或 I/O，透過 thread-safe queue 或 Qt signal 回傳事件。
- 關閉視窗時先發出取消，再等待資源安全釋放。
- 不在 click handler 中執行模型下載、網路請求、資料庫 migration 或大型檔案解析。

### tkinter／CustomTkinter queue 模式

```python
from __future__ import annotations

import time
from dataclasses import dataclass
from queue import Empty, Queue
from threading import Event, Thread

import customtkinter as ctk


@dataclass(frozen=True, slots=True)
class ProgressEvent:
    percent: int
    message: str


def run_job(events: Queue[ProgressEvent], cancelled: Event) -> None:
    for percent in range(101):
        if cancelled.is_set():
            events.put(ProgressEvent(percent, "已取消"))
            return
        time.sleep(0.03)
        events.put(ProgressEvent(percent, "處理中"))


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Background Job")
        self.events: Queue[ProgressEvent] = Queue()
        self.cancelled = Event()
        self.worker: Thread | None = None

        self.progress = ctk.CTkProgressBar(self)
        self.progress.pack(padx=20, pady=12)
        self.status = ctk.CTkLabel(self, text="等待中")
        self.status.pack(padx=20, pady=12)
        ctk.CTkButton(self, text="開始", command=self.start_job).pack()
        ctk.CTkButton(self, text="取消", command=self.cancelled.set).pack()

    def start_job(self) -> None:
        if self.worker is not None and self.worker.is_alive():
            return
        self.cancelled.clear()
        self.worker = Thread(
            target=run_job,
            args=(self.events, self.cancelled),
            daemon=True,
        )
        self.worker.start()
        self.after(50, self.poll_events)

    def poll_events(self) -> None:
        try:
            while True:
                event = self.events.get_nowait()
                self.progress.set(event.percent / 100)
                self.status.configure(text=event.message)
        except Empty:
            pass

        if self.worker is not None and self.worker.is_alive():
            self.after(50, self.poll_events)


if __name__ == "__main__":
    App().mainloop()
```

正式應用需再處理視窗關閉時的取消、worker join、例外事件與重複啟動。

## Qt Signal／Slot 規則

- 長工作使用 `QThread`, `QThreadPool`/`QRunnable` 或 async integration，不把工作塞進主 event loop。
- worker 透過 typed signal 傳送不可變資料。
- QObject 的 thread affinity 必須清楚；不要任意在執行後移動有 parent 的物件。
- view model 保留可測試狀態；signal handler 只做短操作。
- 大量更新要節流或批次，避免每筆資料都 repaint。

## 佈局與狀態

### tkinter

- `pack`、`grid` 可在不同 parent 使用，但不要在同一 parent 混用。
- 混用通常造成 geometry manager 錯誤，而不是所謂「無限迴圈」。
- 表單優先 `grid`，簡單線性區塊可用 `pack`。
- 不以 `place` 固定所有像素；需考慮 DPI、字型與翻譯後長度。

### 狀態管理

- domain model 不依賴 GUI import。
- 設定與 session state 使用 dataclass/Pydantic 等明確結構。
- view 只保存呈現需要的狀態。
- 儲存前驗證，使用 atomic write，避免程式中斷造成設定檔損壞。
- 不在 UI state 內保存裸 API key；使用 OS credential store 或安全 secret 來源。

## 錯誤與使用者體驗

- 技術例外寫入 log，對使用者顯示可行動訊息。
- 非致命錯誤不要讓主 event loop 崩潰。
- 需要時間的操作顯示 progress、可取消與明確完成狀態。
- 防止 double-click 重複提交；disable/enable 按鈕與 operation state 一致。
- 對破壞性操作提供確認與可回復機制。
- 所有主要操作可使用鍵盤，focus order 合理。

## 打包與發布

1. 先用一般 venv 執行完整 smoke test。
2. 明確列出動態 import、Qt plugin、圖示、翻譯與資料檔。
3. 先測 one-folder，再決定是否 one-file；one-file 常有較慢啟動與防毒誤判成本。
4. 在乾淨 VM 或實體機測試，不只在開發機。
5. 分別驗證 Windows code signing、macOS signing/notarization 與 Linux desktop integration。
6. 記錄 log/cache/config 位置與升級遷移策略。
7. 若有自動更新，更新包必須簽章並可回復。

## 測試策略

- domain/model 使用一般單元測試。
- controller/view model 使用 fake view 或 signal spy。
- 對 thread/queue 測試完成、取消、例外與 shutdown。
- UI smoke test 覆蓋啟動、主要流程與視窗關閉。
- 在 CI 或 release pipeline 執行每個 OS 的打包與啟動測試。
- screenshot test 只作輔助；不要以像素完全相同取代可用性測試。

## 交付標準

- UI 操作只在主執行緒，worker 透過 queue/signal 回傳。
- 長工作可取消，關閉時不留下 thread、process、socket 或暫存檔。
- domain/model 不依賴 GUI framework，可獨立測試。
- 佈局支援 DPI、字型與文字長度變化。
- 錯誤、進度、重複操作與破壞性動作有清楚 UX。
- 每個目標 OS 都有打包與乾淨環境 smoke test。
- 授權、簽章、更新與設定儲存策略已記錄。

## 延伸閱讀

- [完整範例](references/examples.md)
- [速查表](references/cheatsheet.md)
- [常見陷阱](references/pitfalls.md)

## 版本相容性

| 環境 | 建議 |
|---|---|
| Python 3.14 | 穩定維護基準；確認 GUI framework 與 bundler wheel |
| Python 3.10–3.13 | 支援；依目標框架的官方支援矩陣 |
| Windows/macOS/Linux | 必須分別打包與 smoke test |
| PySide6/PyQt6 | Qt plugin、授權與部署規則需依實際版本確認 |
| Preview Python | 不作發行預設，除非 bundler 與 native wheels 已驗證 |
