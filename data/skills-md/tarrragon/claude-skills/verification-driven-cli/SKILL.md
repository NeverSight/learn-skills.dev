---
name: verification-driven-cli
description: "CLI 工具教學文章的驗證導向生產流程：分類決定驗證分工（非互動 vs 全螢幕 TUI）、Docker 可拋棄 fixture、三層標註（驗過 / caveat / 移除）、實跑 gotcha 回寫。官方 docs fact-check 會放過版本差異與實作落差、只有實機跑過才能抓到。觸發詞：CLI 工具文章、工具教學、驗證流程、Docker fixture、實機驗證、gotcha、tool article、CLI tutorial、verification workflow。Trigger when writing CLI tool tutorial / tool comparison articles."
license: MIT
metadata:
  version: 1.2.2
  category: writing-methodology
---

# Verification-Driven CLI Tool Articles

CLI 工具教學文章的驗證導向生產流程 — 在寫下每一條 install 與操作指令前、先在本機實際跑過、確認正確才寫進去。

## 為什麼需要這個流程

官方文件查核會放過三類落差：

1. **旗標名 / 設定鍵在版本間變動**：文件常落後於 binary
2. **隱含前提未寫明**：需要特定 schema prefix、需要特定 driver 參數
3. **平台特定行為**：macOS 裝得起來但特定功能 segfault

這些落差的共通點：讀者照文件走會撞牆、卻在文件裡找不到答案。實機跑一次就現形。

## 適用情境

- 寫 CLI 工具教學文章（安裝、配置、操作指引）
- 寫工具比較文章（多工具同場景對照）
- 已有 Docker / OrbStack 環境可起可拋棄容器

不適用：

- 純概念文章（不含操作指令）
- 雲端服務操作（無法本機模擬）
- 需真實網域 / 叢集 / 特定 OS 的操作（標 caveat、不用此流程）

## 流程

### Step 1：列候選工具、分兩類

| 類別       | 特徵                                                           | 驗證方式            |
| ---------- | -------------------------------------------------------------- | ------------------- |
| 非互動工具 | 一次呼叫印出結果就結束（`--version`、`--help`、`-c` 執行模式） | 自動化跑、看輸出    |
| 全螢幕 TUI | 接管終端機（`lazygit`、`btop`、`harlequin`）                   | 人工互動操作 + 截圖 |

判斷標準：先 grep `--help` 找有沒有非互動模式。有就自動驗（最可靠、零人力）、沒有才走人工互動。很多 TUI 工具附帶 snapshot / ci / execute 旗標、優先用這些縮小「需要人」的範圍。

### Step 2：安裝

`brew` 優先、不在 core 的用 `cargo install` 或 `go install` 備案。`go install` 還能繞過從源碼 build 撞到的 Xcode 版本問題。

### Step 3：造 Docker fixture

用 Docker 起可拋棄的測試環境。紀律三條：

1. **獨立命名 + 非標準 port**：容器名加 prefix（`sqltest-pg`）、port 用 55432 等非標準值、避免撞到使用者既有服務
2. **只動自己造的**：不碰使用者既有容器 / 資料庫 / 檔案
3. **測完自己清理**：`docker stop` / `rm` 自己的容器、刪自己的暫存檔；image 可留著重用

資料庫工具的標準 fixture：

```bash
docker run -d --name sqltest-pg \
  -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=testdb \
  -p 55432:5432 postgres:alpine
# 等 ready 再 seed
docker exec sqltest-pg psql -U test -d testdb \
  -c "CREATE TABLE products(id serial primary key, name text, price numeric);
      INSERT INTO products(name,price) VALUES('widget',9.99),('gadget',19.50);"
```

容器監控工具：起常駐容器給 `ctop` 看即時資源、pull 多層 image 給 `dive --ci` 分析。
檔案 / SQLite 工具：用 `sqlite3` 造小 db。

### Step 4：驗證

非互動工具自己跑（版本 / `--help` 旗標 / 非互動模式輸出）。TUI 交人互動操作、截圖回報、對照文章宣稱逐項判讀。

### Step 5：三層標註

| 狀態                             | 處理                                                        |
| -------------------------------- | ----------------------------------------------------------- |
| 驗過                             | 寫進文章、當正式內容、記實機觀察                            |
| 本機驗不了但工具有效             | 保留、加 blockquote caveat 標「依官方文件、本機未實機驗證」 |
| 裝得起但操作無法驗證且無保留價值 | 移除、不寫進去                                              |

已驗部分和未驗部分在同一段時要明確標示、讓讀者分得出哪些經實測。

### Step 6：gotcha 回寫

實跑抓到的「文件沒寫的真實行為」寫進對應工具段落、標「實測」。這些一句話提醒省下讀者各自撞一次的時間。

### Step 7：收尾

`mdtools lint` / `cards` 過、清理自己造的 fixture、commit。

## 反覆陷阱

1. **跳過 Step 3 直接寫**：沒跑就寫的指令錯誤率最高、尤其是連線字串跟旗標名
2. **漏清理 fixture**：使用者下次 `docker ps` 看到一堆 `sqltest-*` 容器
3. **驗過但沒標**：讀者分不出哪些經實測、哪些是文件依據
4. **caveat 沒寫具體原因**：「未驗證」不夠、要寫「需真實 k8s cluster、本機無法模擬」
5. **把 verifier 當成不會錯的**：你寫的驗證腳本 / 檢查本身也是一隻會讀錯層的眼睛 — 一個 naive 判斷（如「這 leaf 檔是不是 symlink」對上 GNU stow 的目錄摺疊）會給假陰性、讓你誤判部署壞了。verifier 也要被驗：拿一個「已知正確」的環境跑一次、確認它報 pass，再信它的 fail。
6. **模擬架構的 fixture 不可信**：Docker fixture 跑在 CPU 模擬下（qemu，如 arm64 host 上跑 amd64 image）會給假通過 / 假失敗 — sandbox、seccomp、LSM、syscall 相關行為在模擬層跟原生不同。架構敏感的驗證要在目標架構的原生環境跑，別信模擬 fixture 的綠燈或紅燈。

## 跟其他 skill 的關係

- [compositional-writing](../compositional-writing/SKILL.md)：寫作 atomic 原則、適用所有寫作
- [migration-playbook-methodology](../migration-playbook-methodology/SKILL.md)：sibling、處理 cross-vendor process content
- [golden-path-validation](../golden-path-validation/SKILL.md)：本 skill 是「作者自己用 Docker fixture 逐工具驗」；golden-path-validation 是「派陌生人冷讀代理人端到端驗一整份 setup 指引」。兩者共享「執行勝過審讀」與「模擬環境不可信」的紀律（本 skill 反覆陷阱 #5/#6 是那組原則的濃縮版）。

---

版本紀錄在同目錄的 `CHANGELOG.md`。
