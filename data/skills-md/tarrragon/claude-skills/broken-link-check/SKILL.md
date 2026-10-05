---
name: broken-link-check
description: "broken-link 偵測工具。掃描 .claude/ 目錄所有 Markdown 文件中的路徑引用，偵測失效連結。Use for: (1) 一次性掃描所有 broken links, (2) 搭配 /loop 定期監控, (3) 修改規則/方法論/代理人文件後驗證路徑完整性。Use when: user runs /broken-link-check, 或搭配 /loop 定期執行, 或發現 broken link 錯誤後。"
metadata:
  portable: true
  version: 2.5.1
---

# broken-link-check

掃描 `.claude/` 目錄下所有 Markdown 文件中的路徑引用，偵測失效連結。

## 背景

`.claude/` 目錄中的規則、方法論、代理人定義文件大量交叉引用彼此。
當文件被重命名或移動時，舊的引用路徑會變成 broken link。

此工具用於定期偵測此類問題，防止 broken links 長期未被發現。

---

## 權威 gate：scan_links.py CLI

broken-link 計數的唯一權威來源是 `scan_links.py` 確定性 CLI，不是 LLM 手動判讀。LLM 手動 Glob/Grep 流程對同一 repo 會產出浮動計數（實測顯示相同專案產出 258 vs 155 的差異），無法作為跨框架完成 gate。CLI 以固定排除規則與穩定排序保證同一 repo 連續執行 byte-for-byte 一致，因此作為權威 gate。

### 立即掃描（權威）

```
python3 .claude/skills/broken-link-check/scan_links.py .  # portability-allow: consumer 共通安裝位置
```

- 位置參數為 repo root（預設 cwd），預設掃描 `<root>/.claude/**/*.md`
- `--scan-root SUBTREE`（可重複指定）疊加額外子樹（如 `docs`），使規劃文件（ticket body、spec、usecases、proposals）一併納入偵測；不帶此 flag 時行為與擴充前逐字一致（向後相容，既有 gate 用法不受影響）
- exit code：`0`=零 broken（gate pass）/ `1`=偵測到 broken（gate fail）/ `2`=執行錯誤（root 不存在、I/O 失敗）
- gate 用途可直接接 `&&` 或 CI：broken>0 即非零 exit，與工具自身錯誤（exit 2）區隔

```
# 擴充掃描 docs/ 下規劃文件（疊加於預設 .claude/，不取代）
python3 .claude/skills/broken-link-check/scan_links.py . --scan-root docs  # portability-allow: consumer 共通安裝位置
```

### 輸出格式

| flag | 用途 |
|------|------|
| `--format text`（預設） | 人類可讀：摘要 + 分組 broken 清單 |
| `--format json` | 穩定 schema，供下游清理工具消費（含 `source_file/line/raw_ref/resolved_path/category` + `categories` 分類計數） |

### 四排除旋鈕（預設皆排除，flag 顯式覆寫納入）

| 旋鈕 | 預設 | 覆寫 flag |
|------|------|-----------|
| 程式碼區塊內引用 | 排除 | `--include-code-block` |
| migration-backups / hook-logs 下路徑 | 排除（歸 `excluded_backup`） | `--include-migration-backups` |
| placeholder 範例路徑（如 `path/file.md`） | 排除（歸 `placeholder`） | `--include-placeholder` |
| documented-error 豁免 marker 行 | 排除（歸 `excluded_documented`） | `--include-documented` |

覆寫旋鈕用於 triage/debug，gate 預設一律不加 flag。

### documented-error 豁免 marker

error-pattern 案例表會刻意記錄不存在的路徑——例如 confabulation 案例的「錯誤參照」欄、或已遷移/刪除檔案的歷史軌跡。這些路徑的文獻價值正在於保留原貌，redirect/刪除會毀損案例資料。在含該引用的行尾（或同 table cell 內）加上行內 marker，scanner 即將該行所有引用歸 `excluded_documented` 不計 broken：

```
<!-- broken-link-exempt: documented-error -->
```

- 顯式 opt-in（per-occurrence），無 marker 的真實 broken 不受影響。
- marker 僅作用於所在行（PC-146 放置精確性），不會誤豁免他行。
- 僅取消「不存在」引用的 broken 計列；該行若有存在的引用仍歸 `ok`，不遮蔽存在事實。
- `--include-documented` 可在 triage 時顯式納入計數。

### opt-in fence 稽核模式（非 gate）

`--include-code-block` 預設維持 `False` 是刻意判定：fence（程式碼區塊）內
broken 引用大量為歷史實作報告與教學/語法示範，翻預設會使多數變成誤報，淹
沒真實 drift。但維持預設不代表放棄偵測——`--fence-audit` 開一條獨立稽核
通道，讓 fence 內失效引用能被人定期複查，防止 drift 在無人偵測的射程外
累積。

```
python3 .claude/skills/broken-link-check/scan_links.py . --fence-audit  # portability-allow: consumer 共通安裝位置
```

**定位：這不是 gate。** `--fence-audit` 恆 `exit 0`，不參與既有命令的 exit
code 語意，也不接 CI 阻擋——即使找到大量發現，指令本身不失敗。用途是產出
「供人判讀的清單」，不是「必須降為零的計數」。

**不做的事**：不嘗試自動判定「語法示範」vs「操作指引」。兩者差別是語氣
（「例如」「格式如下」vs「執行以下步驟」），機器判不了；全量逐筆分類的實
測結果與抽樣外推值有數倍落差（詳見
`docs/work-logs/v0/v0.2/v0.2.1/fence-ref-triage.md`），印證語意分類不可
靠。稽核模式只輸出機器可靠取得的分組訊號：

| 欄位 | 說明 |
|------|------|
| `carrier_nature` | 依來源檔路徑段判定的載體性質：`可執行指令載體`（`commands/`）、`案例敘事載體`（`error-patterns/`）、`歷史報告載體`（`hook-specs/`）、`未分類`（其餘目錄，性質混雜不構成可靠訊號） |
| `has_marker` | 該行是否已有 `broken-link-exempt` / `portability-allow` 豁免 marker（`category` 對應 `excluded_documented`），供人複核既有 marker 是否仍合法 |
| `merge_successor` | 沿用既有合併型遷移反查索引，有值者為高信心可直接改指 |

彙總層另提供 `by_carrier_nature` 與 `marker_counts` 兩組計數，取代語意
三分類統計（「歷史報告 / 語法示範 / 真實 drift」機器判不了，改以可靠訊號
分組呈現）。

`--format json` 輸出額外欄位：`scanned_files` / `fence_entries_count` /
`by_carrier_nature` / `marker_counts` / `entries`（每筆含
`source_file`/`line`/`raw_ref`/`resolved_path`/`category`/`carrier_nature`/
`has_marker`/`merge_successor`）。與既有 gate 路徑（無 `--fence-audit`
時）完全不共用輸出 schema，不影響原有 `--format json` 欄位。

`--scan-root` 對 `--fence-audit` 同樣生效（疊加額外子樹）。

### 搭配 /loop 定期掃描

```
/loop 1h python3 .claude/skills/broken-link-check/scan_links.py .  # portability-allow: consumer 共通安裝位置
```

---

## 偵測規則（CLI 內建，供理解輸出用）

CLI 已內建以下規則，本節僅供閱讀輸出時對照，非需手動執行的步驟。

偵測的路徑格式：

| 格式 | 範例 | 解析基準 |
|------|------|------|
| `@.claude/path/file.md` | `@.claude/pm-rules/decision-tree.md` | repo root |<!-- broken-link-exempt: 格式示範範例路徑，非真實引用（A 類） -->
| `.claude/path/file.md` | `.claude/agents/incident-responder.md` | repo root |<!-- broken-link-exempt: 格式示範範例路徑，非真實引用（A 類） -->
| `../path/file.md` | `../agents/lavender-interface-designer.md` | 引用文件所在目錄 <!-- broken-link-exempt: 格式示範範例路徑，非真實引用（A 類） --> |
| `./path/file.md` | `./references/detail.md` | 引用文件所在目錄 <!-- broken-link-exempt: 格式示範範例路徑，非真實引用（A 類） --> |

排除：`http(s)://`（外部 URL）、`#section`（錨點）、預設四旋鈕涵蓋的程式碼區塊 / 備份目錄 / placeholder 範例 / documented-error marker 行。

---

## Fallback：手動流程（非權威，僅 CLI 不可用時參考）

以下手動 Glob/Grep 流程為 `scan_links.py` 無法執行時（如環境缺 Python）的降級參考，計數可能浮動，不可作為完成 gate。權威結果一律以 CLI 輸出為準。

1. Glob 找出 `.claude/**/*.md`，排除 `.claude/hook-logs/`<!-- portability-allow: 掃描對象目錄，存不存在由各專案決定 -->
2. Grep 找出上述四種前綴的路徑引用，排除 URL / 錨點 / 程式碼區塊
3. 依解析基準轉為實際路徑
4. Read/Glob 確認路徑存在，不存在者記為 broken link（含文件名與行號）
5. 輸出 broken 清單

---

## 修復建議

發現 broken link 時，建議的修復步驟：

1. 搜尋相似文件名（文件可能被重命名）
2. 確認文件是否已移至其他目錄
3. 更新引用路徑（使用 Edit 工具）
4. 如文件確實已刪除，移除引用或更新為替代文件

---

## 注意事項

- 此工具預設只掃描 `.claude/` 目錄；`--scan-root docs` 可疊加 `docs/`，其他目錄（`ui/`、`server/` 等）仍不在掃描範圍
- 只偵測文件引用，不偵測 URL 有效性
- 相對路徑解析基於文件所在目錄，需正確計算層級
- 大型 `.claude/` 目錄（100+ 文件）掃描可能需要數分鐘

---

版本紀錄在同目錄的 `CHANGELOG.md`。
