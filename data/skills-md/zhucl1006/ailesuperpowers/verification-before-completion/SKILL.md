---
name: verification-before-completion
description: 在提交或建立 PR 之前，報表工作已完成、修復或即將使用時 - 需要在做出任何成功報表之前運行驗證命令並確認輸出；證據總是先於斷言
---

# 完成前驗證

## 概述

在沒有驗證的情況下聲稱工作已經完成是不誠實的，而不是效率。

**核心原則：** 證據先於主張，始終如此。

**違反本規則的字面意義即違反本規則的精神。 **

## 鐵律

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

如果您沒有運行此訊息中的驗證命令，則不能聲稱它通過了。

## 門功能

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## 常見故障

|索賠 |需要 |還不夠|
|-------|----------|----------------|
|測試通過 |測試命令輸出：0 次失敗 |上一次運行，“應該通過” |
| 棉絨清潔 | Linter 輸出：0 個錯誤 |部分研究、推斷 |
|建置成功 |建置指令：exit 0 | Linter 通過，日誌看起來不錯 |
|錯誤已修復 |測試原始症狀：通過 |代碼已更改，假設已修復 |
|回歸測試有效 |紅綠循環驗證 |測試一次通過 |
|代理完成| VCS diff 顯示更改 |代理報告“成功”|
|滿足要求 |逐行檢查表 |測試通過 |

## 危險信號 - 停止

- 使用“應該”、“可能”、“似乎”
- 在驗證之前表達滿意（“太棒了！”、“完美！”、“完成！”等）
- 即將工作/勞力/PR，消耗驗證
- 信任代理成功報告
- 依賴部分驗證
- 想著“就這一次”
- 累了並且想要結束工作
- **任何暗示成功但未運行驗證的措辭**

## 合理化預防

|對不起|現實|
|--------|---------|
| “現在應該工作了” |運行驗證 |
| 「我有信心」 |信心≠證據|
| 「就這一次」|無一例外 |
| “Linter 通過”| Linter ≠ 編譯器 |
| 《代理說成功》|獨立驗證 |
| “我累了” |疲憊≠藉口|
| 「部分檢查就夠了」|部分證明不了什麼|
| 「不同的詞語，因此規則不適用」 |精神重於文字|

## 關鍵模式

**測試：**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**回歸測試（TDD紅-綠）：**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**建造：**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**要求：**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**代理委託：**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## 為什麼這很重要

24次失敗記憶：
- 你的人類伴侶說“我不相信你”——信任被打破
- 未定義的函數已發布 - 會崩潰
- 缺少已交付的需求 - 功能不完整
- 時間浪費在錯誤完成→重定向→返工上
- 違規：“誠實是核心價值觀。如果你撒謊，你就會被取代。”

## 何時申請

**總是在：**之前
- 成功/完成聲明的任何變化
- 任何滿意的表達
- 關於工作狀態的任何積極陳述
- 承諾、公關創建、任務完成
- 移至下一個任務
- 委託給代理人

**規則適用於：**
- 準確的短語
- 釋義和同義詞
- 成功的影響
- 任何表明完成/正確性的通信

## 底線

**驗證沒有捷徑。 **

運行命令。讀取輸出。然後領取結果。

這是沒有商量餘地的。
