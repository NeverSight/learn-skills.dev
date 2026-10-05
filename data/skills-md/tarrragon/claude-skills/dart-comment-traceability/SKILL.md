---
name: dart-comment-traceability
description: "Dart 事件處理函式與 UseCase/Domain 層的註解追溯品質檢查。用於：(1) Write/Edit 後自動掃描缺少追溯註解的事件處理函式與獨立 Widget，(2) 產出含建議註解範本的品質報告，(3) 支援 Dart 為主、JavaScript/TypeScript 為輔的多語言註解檢查。觸發場景：PostToolUse Hook（matcher: Write|Edit），事件驅動架構下的程式碼審查。"
metadata:
  version: 1.0.0
---

# Dart Comment Traceability

Dart 事件處理函式與 Domain 層公開函式的註解追溯守護者——確保關鍵函式的註解能回答
「這段程式碼的需求來源、規格文件、修改約束是什麼」，而非只描述做了什麼。

## 定位與沿革

本 skill 承接原屬 `compositional-writing` 的 `comment-qa-hook.py`：該 hook 檢查的是
特定架構風格（事件驅動）下 Dart 事件處理函式的追溯規範，主題屬 Dart/事件驅動架構，
不屬 `compositional-writing` 的一般寫作規範範疇。命名依既有 `dart-style-guardian`／
`dart-test-async-guardian` 的 `dart-` 前綴慣例；hook 檔名維持 `comment-qa-hook.py`
不變——skill 名與 hook 名不一致是刻意的，下游 consumer 以逐字路徑
`dart-comment-traceability/hooks/comment-qa-hook.py` 作為遷移前提。

通用的註解撰寫規範（「為什麼」而非「做什麼」等原則）仍由 `compositional-writing` 的
`references/writing-code-comments.md` 持有，本 skill 的報告以跨 skill 引用方式指向它，
不重複維護。

## 檢查策略

| 分類 | 規則 |
|------|------|
| 必須註解 | Dart 事件處理函式（`handle*`／`on*`／`process*`／`emit*`／`dispatch*`）、獨立 Widget（`StatefulWidget`／`ConsumerWidget`／`StreamBuilder`／`FutureBuilder`）、JS/TS 匯出函式與類別方法、所有語言的 UseCase/Domain 層公開函式 |
| 可豁免 | `_` 開頭的私有輔助函式（`isValid`／`format`／`parse` 等命名模式）、測試檔案、生成檔案（`.g.dart`／`.freezed.dart`） |

完整判斷邏輯（事件處理函式命名模式、輔助函式豁免清單、Widget 分類）見
`hooks/comment-qa-hook.py` 內 `is_event_handler_function()`／`is_auxiliary_function()`。

## 註解完整性判準

註解需同時包含「需求來源」類關鍵字（`需求來源`／`需求:`／`UC-`／`BR-`）與「規格文件」
類關鍵字（`規格文件`／`工作日誌`／`docs/`）才視為完整；缺一即被列入建議清單。

## 架構文件引用為可選

`docs/event-driven-architecture-design.md` 是選用性參考：hook 執行時以
`PROJECT_ROOT`（`get_project_root()`，worktree 感知）為基準檢查該文件是否存在，
不存在時報告直接省略該列引用，其餘檢查（事件處理函式掃描、Widget 掃描、註解範本
產出）照常執行，不報錯、不降級。本專案與 `flutter_balance` 目前皆無此文件。

## 配置

`.claude/hooks/comment-qa-config.yaml`（可選）。缺檔時使用內建預設配置（Dart/JS/TS
皆啟用、排除 `test/`、`*.g.dart`、`*.freezed.dart` 等生成檔案）。

## Hook 模式

已整合為 PostToolUse Hook，`Write`／`Edit` 成功執行後自動觸發。輸出為建議模式
（不阻擋開發），報告存於 `.claude/hook-logs/comment-qa-reports/`，並以
`audience="pm_only"` 過濾，僅主線程可見（避免 subagent 執行時被觸發，PC-V1-004）。

## Resources

### hooks/

- `comment-qa-hook.py` - PostToolUse Hook 入口腳本，含多語言 Parser 整合、
  事件處理函式/Widget 掃描、註解範本產出

---

版本紀錄在同目錄的 `CHANGELOG.md`。
