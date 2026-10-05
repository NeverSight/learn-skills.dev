---
name: dispatch-strategy-review
description: "派發策略檢討工具. Use for: (1) 失敗數超預期 30% 時的策略檢討, (2) 重複分派失敗的分析, (3) 代理人選擇錯誤的修正"
metadata:
  version: 1.1.0
---

# 派發策略檢討 (Dispatch Strategy Review) SKILL

**版本**: v1.1
**建立日期**: 2026-01-23
**狀態**: 穩定

## 概述

派發策略檢討工具用於檢討和改進代理人派發策略，在派發失敗或效果不佳時進行系統性分析和調整。

## 觸發條件

以下情況應使用此 Skill：

| 情境 | 識別特徵 | 強制性 |
|------|---------|--------|
| 失敗數超預期 | 失敗數超過預期的 30% | 強制 |
| 重複分派失敗 | 同一任務分派 2+ 次仍失敗 | 強制 |
| 代理人選擇錯誤 | 派發後發現代理人不適合 | 建議 |
| 效率低下 | 任務完成時間遠超預期 | 建議 |

## 檢討流程

派發策略檢討遵循 5 個 Stage 的結構化分析流程：

1. **Stage 1: 失敗情況收集** - 收集所有派發失敗的詳細資訊
2. **Stage 2: 失敗模式分析** - 識別失敗的共同模式
3. **Stage 3: 根本原因分析** - 使用 5 Why 分析找出根本原因
4. **Stage 4: 改進策略制定** - 制定短期、中期、長期改進措施
5. **Stage 5: 監控和驗證** - 建立監控指標和驗證檢查點

> **詳細模板**: 見 `references/stage-templates.md` 取得各 Stage 的完整輸出格式模板

## 報告和參考資源

### 完整檢討報告

見 `references/full-report-template.md` 取得完整報告模板，包含所有 5 Stage 的結構化報告格式。

### 常見派發錯誤

見 `references/common-dispatch-errors.md` 取得常見派發錯誤識別和修正方法。

## 與其他 Skill 的關係

| Skill | 關係 |
|-------|------|
| `/ticket track` | 使用 ticket-track 收集失敗任務資訊 |
| `/5w1h-decision` | 改進措施應符合 5W1H 格式 |
| `/pre-fix-eval` | 如果失敗涉及錯誤修復，使用 pre-fix-eval |

---

版本紀錄在同目錄的 `CHANGELOG.md`。
