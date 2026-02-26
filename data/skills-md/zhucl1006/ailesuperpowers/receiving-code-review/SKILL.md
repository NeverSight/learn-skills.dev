---
name: receiving-code-review
description: 在收到程式碼審查回饋時、在實施建議之前使用，特別是當回饋似乎不清楚或技術上有問題時 - 需要技術嚴謹和驗證，而不是執行協議或盲目實施
---

# 代碼審查接待處

## 概述

代碼審查需要技術評估，而不是情感表現。

**核心原則：**實施前先驗證。在假設之前先詢問。技術正確性高於社會舒適度。

## 響應模式

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## 禁止回應

**絕不：**
- “你說得完全正確！”（明顯的 CLAUDE.md 漏洞）
- “說得好！” /“非常好的反饋！” （施行）
- 「讓我現在實施它」（驗證之前）

**反而：**
- 重申技術要求
- 提出澄清問題
- 如果錯誤，用技術推理進行反擊
- 開始工作（行動>言語）

## 處理不明確的回饋

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**範例：**
```
your human partner: "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## 特定源處理

### 來自你的人類夥伴
- **值得信賴** - 瞭解後實施
- **如果範圍不清楚，仍然詢問**
- **無執行協議**
- **跳至操作**或技術確認

### 來自外部審稿人
```
BEFORE implementing:
  1. Check: Technically correct for THIS codebase?
  2. Check: Breaks existing functionality?
  3. Check: Reason for current implementation?
  4. Check: Works on all platforms/versions?
  5. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

**你的人類夥伴的規則：**“外部反饋 - 持懷疑態度，但仔細檢查”

## YAGNI 查看「專業」功能

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

**你的人類夥伴的規則：**“你和審稿人都向我匯報。如果我們不需要這個功能，就不要添加它。”

## 實施令

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (breaks, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactoring, logic)
  3. Test each fix individually
  4. Verify no regressions
```

## 何時延後

在以下情況下推回：
- 建議破壞了現有功能
- 審稿人缺乏完整的背景
- 違反YAGNI（未使用的功能）
- 該堆疊在技術上不正確
- 存在遺留/兼容性原因
- 與人類合作夥伴的架構決策發生衝突

**如何反擊：**
- 使用技術推理，而不是防禦性的
- 詢問具體問題
- 參考工作測試/程式碼
- 如果是建築方面的，請讓您的人類夥伴參與進來

**如果感到不舒服，請大聲喊出：**“Circle K正在發生奇怪的事情”

## 確認正確的反饋

當回饋正確時：
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**為什麼不謝謝：** 行動說話。只要修復它即可。代碼本身表明您聽到了反饋。

**如果你發現自己要寫「謝謝」：**刪除它。請說明修復方法。

## 優雅地糾正你的阻力

如果你反駁並錯了：
```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

如實陳述更正並繼續。

## 常見錯誤

|錯誤|修復 |
|---------|-----|
|執行協議 |國家要求還是行動|
|盲目實作|首先根據程式碼庫進行驗證 |
|批量無需測試|一次一個，逐一測試 |
|假設審查者是正確的 |檢查是否損壞東西 |
|避免阻力 |技術正確 > 舒適度 |
|部分實施 |首先澄清所有項目 |
|無法驗證，仍繼續 |狀態限制，求指點|

## 真實例子

**執行協定（差）：**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
```

**技術驗證（良好）：**
```
Reviewer: "Remove legacy code"
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**亞格尼（好）：**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**不清楚的項目（好）：**
```
your human partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## GitHub 主題回覆

在 GitHub 上覆回內嵌評論評論時，請在評論線程中回覆 (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`），而不是作為頂級公關評論。

## 底線

**外部反饋=評估建議，而不是遵循的命令。 **

核實。問題。然後實施。

沒有執行協議。技術始終嚴謹。
