---
name: zellij
description: "Zellij 終端多工管理操作指南。Use for: (1) 在 zellij pane 中啟動/停止服務, (2) 讀取其他 pane 的畫面輸出, (3) 多 pane 佈局管理, (4) 從 claude pane 遠端控制其他 pane。Use when: 需要在多個終端中同時運行前後端服務、需要讀取其他 pane 的日誌輸出、需要管理 zellij session 和 pane。"
allowed-tools: Bash, Read
metadata:
  version: 1.0.0
---

# Zellij 終端多工操作指南

從 Claude Code pane 操作其他 zellij pane 的實戰經驗。

## 核心概念

Claude Code 運行在 zellij 的一個 pane 中。所有 `zellij action` 指令都從 claude 的 shell 發出，但操作對象是 **focused pane**。

關鍵限制：`write` / `write-chars` 只能送到 focused pane。從 claude pane 執行 `move-focus` 後，焦點確實會切換，但必須在**同一個 shell 命令鏈**中完成 focus + write。

---

## 操作模式

### 1. 查看佈局和 pane 狀態

```bash
# 查看完整佈局結構（pane 數量、名稱、command）
zellij action dump-layout 2>&1 | head -20

# 查看 tab 名稱
zellij action query-tab-names

# 列出 sessions
zellij list-sessions
```

### 2. 讀取其他 pane 的畫面（最重要的操作）

```bash
# 切到目標 pane → 滾動到底部 → dump 畫面 → 讀取
zellij action move-focus right && \
  zellij action scroll-to-bottom && \
  zellij action dump-screen /tmp/pane-output.txt && \
  tail -30 /tmp/pane-output.txt
```

**重要**：`dump-screen` dump 的是 **當前 focused pane** 的畫面。必須先 `move-focus` 到目標 pane。

### 3. 向其他 pane 送指令

```bash
# 切到目標 pane → 送文字 → 送 Enter → 切回
zellij action move-focus right && \
  zellij action write-chars "go run ." && \
  zellij action write 10 && \
  zellij action move-focus left
```

- `write 10` = 送 Enter（ASCII 10 = LF）
- `write 3` = 送 Ctrl-C（ASCII 3 = ETX）
- 必須在**同一個 `&&` 鏈**中完成，分開的 Bash 呼叫無法保證焦點狀態

### 4. 送指令後必須驗證

**這是最容易犯的錯誤：送出指令後不驗證就假設成功。**

正確流程：
```bash
# Step 1: 送指令
zellij action move-focus right && \
  zellij action write-chars "go run ." && \
  zellij action write 10

# Step 2: 等待執行 + 讀取驗證（分開的命令）
sleep 5 && \
  zellij action move-focus right && \
  zellij action scroll-to-bottom && \
  zellij action dump-screen /tmp/verify.txt && \
  tail -15 /tmp/verify.txt

# Step 3: 切回 claude pane
zellij action move-focus left
```

### 5. Pane 管理

```bash
# 在右側新增 pane
zellij action new-pane --direction right

# 重命名 pane（必須先 focus 到目標 pane）
zellij action move-focus right && \
  zellij action rename-pane "後端"

# 關閉當前 focused pane
zellij action close-pane
```

---

## 常見陷阱

### 陷阱 1：zellij 初始佈局中的 command pane

zellij 佈局可以用 `command="go"` 啟動 pane，這些 pane 的 shell 被包裝在：
```bash
bash -c 'go run . 2>&1; echo "=== EXITED ==="; read'
```

特徵：
- 程序結束後會停在 `read` 等待 Enter
- 直接 `write-chars` 新指令會被 `read` 吃掉
- 需要先送 Enter（`write 10`）結束 `read`，再送新指令

### 陷阱 2：Ctrl-C 送到前台程序

如果 pane 中有前台程序在運行（如 `go run .`），`write 3`（Ctrl-C）會送到該前台程序。如果程序忽略了 signal，可以改用 `kill PID` 從 claude pane 直接殺。

```bash
# 從 claude pane 找到目標 PID
ps aux | grep "go run" | grep -v grep

# 直接殺程序（不需要切 pane）
kill <PID>
```

### 陷阱 3：dump-screen 只顯示可見區域

`dump-screen` 只 dump 終端可見範圍的內容。如果輸出很長，先 `scroll-to-bottom` 確保看到最新內容。

### 陷阱 4：多次 move-focus 的方向計算

pane 佈局是 `[claude | 前端 | 後端]` 時：
- 從 claude 到後端：`move-focus right && move-focus right`
- 從後端到 claude：`move-focus left && move-focus left`
- `focus-next-pane` 也可以，但方向不如 `move-focus` 明確

---

## 典型工作流

### 啟動前後端服務

```bash
# 1. 啟動後端（右側第二個 pane）
zellij action move-focus right && zellij action move-focus right && \
  zellij action write-chars "cd /path/to/server && go run ." && \
  zellij action write 10

# 2. 等待編譯 + 驗證
sleep 10 && \
  zellij action move-focus right && zellij action move-focus right && \
  zellij action scroll-to-bottom && \
  zellij action dump-screen /tmp/backend.txt && \
  tail -10 /tmp/backend.txt

# 3. 啟動前端（右側第一個 pane）
zellij action move-focus right && \
  zellij action write-chars "cd /path/to/ui && flutter run -d macos" && \
  zellij action write 10

# 4. 等待 + 驗證
sleep 30 && \
  zellij action move-focus right && \
  zellij action scroll-to-bottom && \
  zellij action dump-screen /tmp/frontend.txt && \
  tail -15 /tmp/frontend.txt

# 5. 切回 claude pane
zellij action move-focus left
```

### Hot Restart Flutter

```bash
# 切到前端 pane → 送 R → 驗證
zellij action move-focus right && \
  zellij action write-chars "R"

sleep 5 && \
  zellij action move-focus right && \
  zellij action scroll-to-bottom && \
  zellij action dump-screen /tmp/restart.txt && \
  tail -10 /tmp/restart.txt
```

---

## 檢查清單

操作其他 pane 時：

- [ ] 指令和 move-focus 在同一個 `&&` 鏈中？
- [ ] 送出指令後有等待 + dump-screen 驗證？
- [ ] dump-screen 前有 scroll-to-bottom？
- [ ] 操作完成後有切回 claude pane？
- [ ] 目標 pane 是否有前台程序在運行（影響 write 行為）？

---

版本紀錄在同目錄的 `CHANGELOG.md`。
