---
name: teaching-sync
description: "Repo ↔ 教學文章雙向同步。實作撞牆或設計階段發現教學缺口時建 challenge 記錄；回補教學章節；教學新章節產生實作需求時建 issue 追蹤。觸發詞：teaching-sync、教學同步、撞牆記錄、回補教學、challenge、教學回補、blog sync、知識同步、設計缺口、教學缺口、gap 分析。Use when: 實作遇到挑戰需記錄、設計階段發現教學覆蓋不足、需要回補教學章節、教學章節需要實作驗證、schema/transport 變更需同步教學文件。"
license: MIT
metadata:
  version: 2.0.0
  category: knowledge-management
---

# Teaching Sync — Repo ↔ 教學文章雙向同步

管理 monitor repo（實作端）和 [blog monitoring 教學系列](https://tarrragon.github.io/blog/monitoring/)（教學端）之間的知識同步。

## 前置條件：`BLOG_REPO`

本 skill 的命令會對 blog repo 執行 `checkout` / `commit` / `merge` / `push`，需要知道它在**你這台**的位置。該位置由 `BLOG_REPO` 提供，本檔不寫死任何路徑。

執行任何 blog 操作前先確認：

```bash
git -C "${BLOG_REPO:?請先在 .claude/settings.local.json 的 env 區塊定義 BLOG_REPO}" rev-parse --show-toplevel
```

未定義時此行以非零狀態中止並指出缺什麼，後續命令不會執行。這比讓路徑靜默解析到不存在的位置安全——後者的失敗點會落在 `git commit` 或 `push`，屆時已有部分副作用。

定義位置（`.claude/settings.local.json`，該檔在 gitignore 範圍內，故每台各自持有自己的值、不會互相覆蓋）：

```json
{
  "env": {
    "BLOG_REPO": "<你這台的 blog repo 絕對路徑>"
  }
}
```

**為何不寫死路徑**：同一個 blog repo 在不同 working copy 下的位置不一致（曾出現 `~/Projects/blog` 與 `~/project/blog` 兩種佈局並行）。`~` 只消去使用者名那一段，消不掉 HOME 之下的佈局差異，任一寫法都會在另一側失效。判準見 `.claude/references/reference-stability-rules.md` 規則 9。

## 核心原則

教學和實作是互補關係，兩者各自承擔不同的知識生產責任：

| 方向 | 觸發 | 動作 |
|------|------|------|
| 實作 → 教學 | 實作撞牆（bug / 效能 / 設計困難） | `challenge` — 記錄 → 標記回補點 |
| 設計 → 教學 | UC / spec 設計時發現教學覆蓋不足 | `design-gap` — 比對分析 → 記錄 → 標記回補點 |
| 記錄 → 教學 | challenge / gap 記錄待回補到 blog | `backfill` — 切 blog branch → 修改教學章節 → 更新 sync-pending |
| 教學 → 實作 | 教學新章節需要實作驗證 | `need-impl` — 建 issue 追蹤 |
| 雙向 | schema / transport 變更 | `schema-change` — 同步更新兩端 |

## 指令

### `/teaching-sync challenge` — 記錄實作撞牆

當實作遇到挑戰時執行。建立 `docs/challenges/<name>.md` 記錄，並標記應回補的教學模組。

**流程**：

1. 詢問撞牆場景（輸入規模、症狀、嘗試方案）
2. 建立 challenge 記錄檔（格式見 `docs/challenges/README.md`）
3. 判斷對應教學模組（mapping 表見下方）
4. 在 challenge 記錄的「結論與教學回補」欄位標記回補目標和類型
5. 新增項目到 `docs/sync-pending.md`

### `/teaching-sync design-gap` — 設計階段教學缺口分析

UC / spec / proposal 設計過程中，比對教學內容發現覆蓋不足時執行。和 `challenge` 的差異：gap 在設計階段發現（尚未實作），不是撞牆後的回顧。

**流程**：

1. 讀取待分析的 UC / spec 檔案
2. 對照每個描述、例外場景、邊界條件，讀取 blog 對應教學章節
3. 逐項比對覆蓋度，找出：
   - UC 中的行為/場景，blog 無對應設計指引
   - UC 的例外場景，blog 未討論
   - UC 中自行推導的設計決策（非直接從 blog 引用）
4. 產出 gap 分析表格：

   | UC | UC 中的描述 | 對應 blog 章節 | Gap 描述 | 建議回補方向 |

5. 建立 challenge 記錄檔（`docs/challenges/NNN-*.md`），含完整 gap 清單和優先序
6. 新增項目到 `docs/sync-pending.md`，標記優先級（P0 / P1 / P2）

**只列真正的 gap**。教學已充分覆蓋的部分不列入，避免噪音。

### `/teaching-sync backfill` — 執行教學回補

將 challenge / gap 記錄中的待回補項目實際寫入 blog 教學文章。

**前置條件**：`docs/sync-pending.md` 中有未完成的回補項目。

**流程**：

1. 讀取 `docs/sync-pending.md`，列出待回補項目
2. 按優先級選擇要回補的項目（可指定，如 `/teaching-sync backfill P0`）
3. 讀取對應的 challenge 記錄，理解 gap 的完整背景
4. **切 blog repo feature branch**：
   ```
   git -C "$BLOG_REPO" checkout -b feat/monitor-teaching-backfill-NNN
   ```
5. 讀取目標教學章節，理解現有內容結構
6. **直接修改 blog 教學文章**——在適當位置新增或補充內容
7. **字句層審查**（commit 前強制執行）：
   對修改過的檔案執行 blog multi-round-review Round 1-A 字句層 grep，keyword bank 來自 blog 的 `compositional-writing` skill：
   ```bash
   FILES="<modified-file-paths>"
   # 以下 grep 全部用子 shell，不裸 cd
   (cd "$BLOG_REPO" && rg "不[行可是要能該支對符夠必]|無法|沒[做有]|而非|而不是" $FILES)      # 否定起手
   (cd "$BLOG_REPO" && rg "其實|實務上|真的|碰巧|立刻撞牆|沒事" $FILES)                      # 口語修辭
   (cd "$BLOG_REPO" && rg "集群|默認|質量|視頻|函數|文件夾|接口" $FILES)                      # 地區用語
   (cd "$BLOG_REPO" && rg "值得注意的是|需要說明的是|實際上|基本上|事實上" $FILES)              # 廢話前綴
   (cd "$BLOG_REPO" && rg "✅|❌|⚠️|🚨|🟡|🟢|⭐|📌|✓|✗" $FILES)                           # 裝飾符號
   (cd "$BLOG_REPO" && rg "很多人|大家|不少人|你天天|你會|你可能|先讀懂|先釐清|別搞混" $FILES)  # 對讀者喊話
   (cd "$BLOG_REPO" && rg "教科書級|堪稱|可謂|完美|經典|範本級|最佳實踐|best practice" $FILES)  # 自評誇飾
   (cd "$BLOG_REPO" && rg "天生|與生俱來|本質就是|本來就是|必然|唯一|註定|理所當然" $FILES)      # 必然性框架
   ```
   **命中是候選、不是判決**——每個命中逐一做語意判定：
   - 否定起手：核心概念在句首正面出場 → 合規；被推到「而是/不如」之後 → 修正為概念前置
   - 必然性框架：技術事實（物理/數學限制）→ 合規；設計選擇被講成自然法則 → 修正
   - 其他維度：依 compositional-writing keyword bank 判準

   判定結果記錄為表格（維度 / 命中數 / 判定），違規項立即修正後 commit。
8. **commit + merge + push**：
   ```bash
   git -C "$BLOG_REPO" add <changed-files>

   git -C "$BLOG_REPO" commit -m "docs(monitoring): 回補教學缺口 — <摘要>

   來源：docs/challenges/<NNN>.md (<Gap-ID>)

   Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"

   git -C "$BLOG_REPO" checkout main
   git -C "$BLOG_REPO" merge feat/monitor-teaching-backfill-NNN
   git -C "$BLOG_REPO" push origin main
   git -C "$BLOG_REPO" branch -d feat/monitor-teaching-backfill-NNN
   ```
   審查修正如有額外 commit，同樣走 feature branch → merge → push 流程。
9. 更新 `docs/sync-pending.md`，將完成項目標記 `[x]` 並附 commit hash

**寫作原則**：

- 教學文章面向讀者（非開發者自己），用「為什麼這樣設計」的語氣
- 新增章節放在既有章節的語意流中（不是附錄式貼尾巴）
- 引用其他教學章節用相對連結
- 不在教學文章中提及 monitor repo 的實作細節（那是 repo README 的責任）

**品質閘門**：

- 字句層審查（step 7）是 commit 前的強制步驟，不可跳過
- 審查範圍是 blog 的 `multi-round-review` + `compositional-writing` 規範
- 回補內容量小（嵌入既有章節的 1-2 段）時，Round 1-A 字句層 grep 足夠
- 回補內容量大（新增完整章節 / 3+ 篇同時回補）時，應跑完整 multi-round-review 3 輪流程

### `/teaching-sync need-impl` — 教學需要實作驗證

當教學章節撰寫中發現需要實作驗證時執行。

**流程**：

1. 指定教學模組和章節
2. 描述需要驗證的問題（如「JSONL 查詢在 1 萬筆時真的會慢嗎？」）
3. 建立 monitor repo 的 GitHub issue（標籤 `teaching-driven`）
4. 在教學章節標記 `> 待實作驗證：monitor#<issue-number>`

### `/teaching-sync schema-change` — Schema 變更同步

當 `schema/event.schema.json` 或 `docs/transport.md` 變更時執行。

**流程**：

1. 列出本次 schema/transport 變更差異
2. 檢查教學模組需同步的位置：
   - `monitoring/02-log-schema/` 的欄位解說
   - `monitoring/03-sdk-design/` 的 SDK API 設計
   - `monitoring/04-collector/` 的驗證邏輯
3. **直接修改 blog 教學文章**同步變更（流程同 `backfill` 的 step 4-8：切 branch → 修改 → commit → merge → push）
4. 若變更範圍大（新增欄位 / 移除欄位 / 改型別），記錄到 `docs/sync-pending.md` 追蹤

### `/teaching-sync status` — 同步狀態總覽

列出當前同步狀態：

1. `docs/challenges/` 中未標記教學回補的記錄
2. `docs/sync-pending.md` 中待同步項目（已完成 / 未完成分開列）
3. 教學模組 `_index.md` 中待寫章節 checklist 的完成狀態（需讀 blog repo）

## 模組 mapping 表

| 挑戰類型 | 對應教學模組 |
|---------|------------|
| 高併發寫入 / 儲存效能 / 查詢效能 | [04 Collector](/monitoring/04-collector/) |
| SDK 離線 buffer / 攢批策略 / 生命週期 | [03 SDK 設計](/monitoring/03-sdk-design/) |
| 平台特異行為（CORS / isolate / GIL / 短生命週期） | [05 平台適配](/monitoring/05-platform-adaptation/) |
| Secret 洩漏 / redaction / access control | [07 資安與隱私](/monitoring/07-security-privacy/) |
| 事件分類困難 / 命名規範 | [01 心智模型](/monitoring/01-mental-model/) |
| Schema 版本演進 / 欄位設計 | [02 Log Schema](/monitoring/02-log-schema/) |
| 自架 vs 商業取捨 | [06 商業方案對照](/monitoring/06-commercial-comparison/) |
| funnel / cohort / attribution 實作 | [08 商業利用](/monitoring/08-business-analytics/) |

## 跨 Repo 操作

教學文章位於 blog repo 的 `content/monitoring/`。本 skill **直接修改 blog 教學文章**，完成 commit、merge、push 全流程。

| 操作 | 在哪個 repo 做 | 分支要求 |
|------|---------------|---------|
| 記錄 challenge / gap | monitor repo | 無（docs/ 在 main 可寫） |
| 回補教學章節 | blog repo（直接修改） | feature branch → merge main → push → 刪 branch |
| schema 變更同步 | monitor repo 先改 → blog repo 直接同步 | 同上 |
| 教學需要驗證 | blog repo 發現 → monitor repo 建 issue | 無 |

### Git 操作規範

blog repo 的所有修改遵循固定流程：

1. **切 feature branch**（blog main 是保護分支，Edit 會被 hook 擋）
2. **修改教學文章**
3. **commit**（訊息前綴 `docs(monitoring):`，body 含 challenge 來源引用）
4. **checkout main → merge → push**（fast-forward merge，不開 PR）
5. **刪除 feature branch**

branch 命名：`feat/monitor-teaching-backfill-NNN`（NNN = challenge 編號）

## 同步紀律

1. **Challenge 必填**：`docs/challenges/` 的記錄是強制的——發現不記錄等於知識丟失
2. **教學回補標記必填**：每個 challenge / gap 必須標記對應教學模組和優先級
3. **Schema 變更必同步**：schema/transport 變更後直接同步 blog 教學文章
4. **sync-pending 是 SOT**：所有待回補和已回補項目都記錄在 `docs/sync-pending.md`，不靠記憶
5. **回補完成即推送**：blog 修改完成後立即 merge + push，不留 stale feature branch

## 相關文件

- `docs/challenges/README.md` — challenge 記錄格式
- `docs/sync-pending.md` — 待同步到教學端的變更清單（本 skill 維護）
- `CLAUDE.md` §3「教學 × 實作互補」— 教學模組對應表和雙向工作流
- blog repo: `content/monitoring/` — 教學文章
- blog repo: `content/monitoring/cases/` — 由 challenge 教學化後產生的 case

---

版本紀錄在同目錄的 `CHANGELOG.md`。
