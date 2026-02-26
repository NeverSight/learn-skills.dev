---
name: writing-plans
description: 當您在接觸代碼之前對多步驟任務有規範或要求時使用
---

# 寫作計劃

## 概述

假設工程師對我們的程式碼庫的背景為零且品味有問題，則編寫全面的實施計劃。記錄他們需要知道的一切：每個任務要接觸哪些文件、程式碼、測試、他們可能需要檢查的文檔、如何測試它。將整個計劃作為小任務交給他們。乾燥。亞格尼。時分驅動。頻繁提交。

假設他們是一位熟練的開發人員，但對我們的工具集或問題領域幾乎一無所知。假設他們不太瞭解良好的測試設計。

**開始時宣佈：**“我正在使用寫作計劃技能來創建實施計劃。”

**上下文：** 這應該在專用工作樹中運作（透過腦力激盪技能創建）。

**將計劃保存到：**`docs/plans/YYYY-MM-DD-<feature-name>.md`

## 一口大小的任務粒度

**每一步都是一個動作（2-5 分鐘）：**
- “編寫失敗的測試”-步驟
- 「運行它以確保它失敗」-步驟
- “實現最少的程式碼以使測試通過” - 步驟
- “運行測試並確保它們通過”- 步驟
- “提交”-步驟

## 計劃文檔標題

**每個計劃必須以此標題開頭：**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## 任務結構

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
結果 = 函數（輸入）
斷言結果==預期
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def函數（輸入）：
預期回報
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m“壯舉：新增特定功能”
```
```

## 記住
- 始終精確的文件路徑
- 計劃中的完整代碼（不是“添加驗證”）
- 具有預期輸出的精確命令
- 用@語法參考相關技巧
- DRY、YAGNI、TDD、間隙空間

## 執行交接

保存計劃後，提供執行選擇：

**“計劃完成並保存到`docs/plans/<filename>.md`。兩種執行選項：**

**1.子代理驅動（本次會議）** - 我為每個任務分配新的子代理，在任務之間進行審查，快速迭代

**2.並行會話（單獨）** - 使用執行計劃打開新會話，使用檢查點批量執行

**哪一種方法？ ”**

**如果選擇子代理驅動：**
- **所需的子技能：** 使用超能力：子代理驅動開發
- 留在本次會議
- 每個任務新鮮的子代理+程式碼審查

**如果選擇並行會議：**
- 引導他們在工作樹中打開新會話
- **所需的子技能：** 新會話使用超能力：執行計劃
