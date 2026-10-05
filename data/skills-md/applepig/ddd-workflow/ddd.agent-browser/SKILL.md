---
name: ddd.agent-browser
description: >
  E2E 除錯：用 agent-browser CLI 重現場景、觀察狀態、定位前端問題根因。
  E2E 測試失敗、需要視覺驗證 UI 行為、或追蹤前端問題時使用，通常在 /ddd.work 中觸發。
  Trigger: "debug E2E", "check the page", "why is the test failing",
  "open the browser", "take a screenshot", "inspect the DOM",
  "E2E 失敗", "測試壞了", "檢查頁面", /ddd.agent-browser。
---

# ddd.agent-browser — E2E 除錯說明書

在 DDD 工作流的開發階段（`/ddd.work`），當 Playwright E2E 測試失敗或需要視覺驗證時，用 `agent-browser` CLI 直接操作瀏覽器來定位問題。

這份說明書不是完整指令手冊，而是從「測試掛了」走到「找到根因」的流程速查。指令細節以目前安裝版本內建說明為準：`agent-browser skills get core --full`。

## 核心循環

```
測試失敗 → 重現場景 → 觀察狀態 → 定位根因 → 修正 → 驗證
```

先讀 Playwright 錯誤訊息提出假設，再用 `agent-browser` 驗證。不要盲目連續嘗試；連續 3 次假設被推翻時，暫停並回報已排除項目。

## Step 1：重現場景

把瀏覽器帶到測試失敗的頁面。新版 `tab` 使用穩定 id（`t1`、`t2`）或自訂 label，不接受數字 index；多 tab 除錯時優先用 label。

```bash
# 單頁除錯：在目前作用中的 tab 導航
agent-browser tab
agent-browser open http://localhost:3000/target-page

# 多頁除錯：建立有 label 的 tab，之後用 label 切換
agent-browser tab new --label app http://localhost:3000/target-page
agent-browser tab app
```

導航後等頁面穩定，再拿互動元素 refs：

```bash
agent-browser wait --load networkidle
agent-browser snapshot -i
```

需要登入狀態時，用 session 持久化避免重複登入：

```bash
agent-browser --session-name debug open http://localhost:3000/login
agent-browser snapshot -i
agent-browser fill @e1 "test@example.com"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"

agent-browser --session-name debug open http://localhost:3000/target-page
```

## Step 2：觀察狀態

根據失敗類型選擇最小觀察手段。

### DOM 或互動狀態

```bash
agent-browser snapshot -i
agent-browser snapshot -s "#form-container"
agent-browser get text @e1
agent-browser get html @e1
agent-browser is visible @e1
agent-browser is enabled @e2
agent-browser is checked @e3
```

### 視覺呈現

```bash
agent-browser screenshot
agent-browser screenshot --full
agent-browser screenshot --annotate
agent-browser diff url http://localhost:3000/page http://staging.example.com/page
```

### JavaScript 錯誤

```bash
agent-browser console
agent-browser errors
agent-browser eval 'document.querySelectorAll(".error-message").length'
```

複雜 JS 用 stdin，避免 shell 跳脫問題：

```bash
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify({
  url: location.href,
  errors: document.querySelectorAll(".error").length,
})
EVALEOF
```

### 網路請求

```bash
agent-browser network requests
agent-browser network requests --filter "/api/"
agent-browser network route "/api/submit" --abort
agent-browser network route "/api/data" --body '{"error": "mocked failure"}'
agent-browser network unroute "/api/submit"
```

`network route` 會改變流量，只能在 dev server 或使用者明確同意的環境使用。

## Step 3：互動重現

用 snapshot refs 模擬失敗路徑；頁面變動後一定要重新 snapshot。

```bash
agent-browser fill @e1 "test input"
agent-browser select @e2 "option-value"
agent-browser check @e3
agent-browser press Tab
agent-browser keyboard type "search query"
agent-browser click @e5
agent-browser wait --load networkidle
agent-browser snapshot -i
```

`@e1`、`@e2` 這些 ref 在導航、表單送出、Modal 開啟、AJAX 更新後可能失效。

```bash
agent-browser click @e5
agent-browser snapshot -i
agent-browser click @e1
```

## Step 4：備用定位器

當 snapshot ref 不穩定或元素沒有好的 selector 時，用語義定位器。

```bash
agent-browser find text "送出" click
agent-browser find label "電子郵件" fill "test@example.com"
agent-browser find role button click --name "Submit"
agent-browser find placeholder "搜尋" type "query"
agent-browser find testid "submit-btn" click
```

## 常見場景

元素找不到：先 `wait --load networkidle`，再 `snapshot -i`；若不在互動快照中，改用 `snapshot`、`get text` 或檢查 iframe。

點擊沒反應：檢查 `is visible`、`is enabled`，必要時 `scrollintoview`，再用 `screenshot --annotate` 看是否被 overlay 擋住。

表單驗證失敗：送出後截圖，並用 `eval --stdin` 查錯誤訊息與欄位 validity。

API 回應異常：用 `network requests --filter "/api/"` 看請求；只在 dev server 用 `network route` 模擬失敗或空資料。

RWD 問題：用 `set viewport 375 812` 或 `set device "iPhone 14"` 重現，再截圖比對。

Auth 問題：用 `cookies`、`storage local`、`storage session` 檢查狀態；不要把 token 或 cookie 值貼進對話或文件。

## 進階工具

錄影（`record`）、Chrome DevTools Trace（`trace`）、效能分析（`profiler`）、元素高亮（`highlight`）詳見 `references/agent-browser-advanced.md`。

## DDD 收尾

在 `/ddd.work` 中使用時，把除錯發現同步到 `works.md`：記錄失敗現象、驗證過的假設、根因、修正方式與驗證結果。
