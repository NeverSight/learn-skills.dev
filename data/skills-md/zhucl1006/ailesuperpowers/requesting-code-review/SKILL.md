---
name: requesting-code-review
description: 在完成任務、實現主要功能時或在合併之前使用以驗證工作是否符合要求
---

# 請求代碼審查

促進超能力：code-reviewer子代理在問題級聯發生之前發現問題。

**核心原則：**早複習、常複習。

## 何時請求審查

**強迫的：**
- 子代理程式驅動開發中的每個任務之後
- 完成主要功能後
- 合併到主程式之前

**可選但有價值：**
- 當卡住時（新視角）
- 重構前（基線檢查）
- 修復複雜的錯誤後

## 如何請求

**1.獲取git SHA：**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2.調度代碼審閱者子代理：**

使用具有超能力的任務工具：代碼審閱者類型，填寫模板`code-reviewer.md`

**佔位符：**
- `{WHAT_WAS_IMPLEMENTED}`- 你剛剛建造的
- `{PLAN_OR_REQUIREMENTS}`- 它應該做什麼
- `{BASE_SHA}`- 開始提交
- `{HEAD_SHA}`- 結束提交
- `{DESCRIPTION}`- 簡要總結

**3.根據反饋採取行動：**
- 立即修復關鍵問題
- 在繼續之前修復重要問題
- 注意稍後的小問題
- 如果審稿人錯了就退回（有推理）

## 例子

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch superpowers:code-reviewer subagent]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## 與工作流程集成

**子代理驅動的開發：**
- 每項任務後回顧
- 在問題複雜化之前發現問題
- 在進行下一個任務之前修復

**執行計劃：**
- 每批後回顧（3個任務）
- 獲取反饋、申請、繼續

**臨時開發：**
- 合併前審查
- 卡住時回顧

## 危險信號

**絕不：**
- 跳過評論，因為“很簡單”
- 忽略關鍵問題
- 繼續處理未解決的重要問題
- 用有效的技術回饋進行爭論

**如果審稿人錯誤：**
- 用技術推理進行反擊
- 顯示證明其有效的程式碼/測試
- 要求澄清

請參考模板：requesting-code-review/code-reviewer.md
