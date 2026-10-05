---
name: continuous-learning
description: "Extracts reusable patterns from Claude Code sessions and captures knowledge with capture-time triage: framework-relevant learnings (still true after swapping project names/paths) go straight to the canonical framework layer (error-patterns/rules/methodologies/references), project-relevant learnings go to docs/CLAUDE.md, and session-only findings are not recorded. Claude Code's native memory is excluded as a destination — this framework's error-patterns layer replaces it for cross-project reuse. Use when session ends (Stop hook), when recording technical decisions, implementation insights, or lessons learned. Handles automatic pattern detection and structured knowledge capture with interconnected links, preventing cross-project principles from being trapped in single-project storage."
metadata:
  version: 4.1.0
---

# Continuous Learning

從 Claude Code 工作過程中自動提取可復用模式，並將洞察、決策和經驗依三分流正規化為結構化的原子知識記錄。

---

## 兩大功能

### 1. Session Pattern Extraction（自動）

透過 Stop hook 在 session 結束時自動執行：

1. **Session 評估**：檢查 session 訊息量是否足夠（預設 10+）
2. **模式偵測**：識別可提取的可復用模式
3. **Skill 產出**：將有用模式儲存到 `.claude/skills/learned/`

### 2. Knowledge Capture（按需）

將重要技術決策、實作方案和經驗教訓正規化為文件：

1. **提取核心結論**：從工作過程中識別值得記錄的結論
2. **捕獲時三分流**（記錄前必答；判別問句「另一個專案的 session 讀到這段，能用嗎」）：框架相關（能用）+ 錯誤學習類 + 根因已過 Two-Phase Reflection → **直接 `/error-pattern add`**（canonical 層，隨 sync 跨專案傳播），流程結束；框架相關 + 錯誤學習類 + 根因未熟 → 暫不記錄，續觀察同主題是否再現；框架相關 + 非錯誤學習類 → 依升級路徑表選 `rules/` `methodologies/` `references/` `pm-rules/` `agents/` `skills/` 之一；專案相關（不能用但本專案未來會用）→ `docs/` 或 `CLAUDE.md`；兩者皆非（僅本次 session 成立）→ 不記錄
3. **分類和結構化**：依目的地的既有格式規範撰寫（error-pattern 用 PC/IMP/ARCH 範本、規則用 rules/core 速查 stub 或 references 全文、方法論用 methodology 範本）
4. **建立連結**：識別與既有知識的關聯，補上交叉引用

> **重要**：分流判斷在**寫入前**執行，不是寫入後補救。「寫入後補評估」的事後閉環經量化證明不執行（130 檔 feedback memory 標註率 4%，PC-061 模式的規模化實證）。memory 不是任何分支的目的地。
>
> - 分流判準權威來源：`.claude/pm-rules/pm-quality-baseline.md` 規則 7
> - 錯誤模式參考：`.claude/error-patterns/process-compliance/PC-061-memory-upgrade-blindness.md`
> - 完整決策樹：`references/upgrade-decision-tree.md`

**適用時機**：

| 時機 | 說明 |
|------|------|
| 重要技術決策完成 | 方案選擇後建立決策記錄 |
| 實作方案確定 | 新的實作模式或解決方案誕生 |
| 學習機會 | 測試失敗、問題排除、重構完成後的經驗總結 |
| Phase 4 完成 | 重構後進行知識沉澱 |
| 版本發布前 | 總結主要決策和經驗 |

### 根因型知識記錄特殊處理（Two-Phase Reflection）

當記錄的核心是**根因分析**（error-pattern、代理人失敗歸因、用戶質疑「分析太表層」），必須套用兩階段深度反思：

1. **Phase 1 多假設 Reality Test**：列 5+ 候選動機、逐個自我觀察驗證、至少挖 2 層深因
2. **Phase 2 WRAP 檢驗**：結論產出後過 WRAP（Widen/Reality/Attain/Premortem）避免第一直覺陷阱

禁止只列 1-2 個假設就下結論，或跳過 Phase 2 直接落地。

> 完整方法論：`.claude/methodologies/three-phase-reflection-methodology.md`
> 案例：PC-087（表層版）→ PC-088（Phase 1+2 後的抽象層）

---

## Pattern Types

| Pattern | Description |
|---------|-------------|
| `error_resolution` | How specific errors were resolved |
| `user_corrections` | Patterns from user corrections |
| `workarounds` | Solutions to framework/library quirks |
| `debugging_techniques` | Effective debugging approaches |
| `project_specific` | Project-specific conventions |

---

## Configuration

Edit `config.json` to customize:

```json
{
  "min_session_length": 10,
  "extraction_threshold": "medium",
  "auto_approve": false,
  "learned_skills_path": ".claude/skills/learned/",
  "patterns_to_detect": [
    "error_resolution",
    "user_corrections",
    "workarounds",
    "debugging_techniques",
    "project_specific"
  ],
  "ignore_patterns": ["simple_typos", "one_time_fixes", "external_api_issues"]
}
```

---

## Hook Setup

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/skills/continuous-learning/evaluate-session.py"
          }
        ]
      }
    ]
  }
}
```

---

## 知識記錄撰寫指引

依三分流判定的目的地選用對應撰寫規範，不再有單一共用的記憶檔案格式：

| 目的地 | 撰寫規範 |
|--------|---------|
| `.claude/error-patterns/` | `/error-pattern add` 內建範本（PC/IMP/ARCH 分類、Why/Consequence/Action 三明示） |
| `.claude/rules/` `.claude/methodologies/` `.claude/references/` `.claude/pm-rules/` `.claude/agents/` `.claude/skills/` | `.claude/rules/core/document-writing-style.md` 三明示規範；方法論另依 methodology-writing skill（若已安裝）的撰寫規範，未安裝時仍可依三明示規範直接撰寫，只是少了該 skill 提供的方法論專屬範本 |
| `docs/` `CLAUDE.md` | 專案既有文件格式慣例 |

> 若專案已採用 compositional-writing skill，原子性（一則記錄一個結論）等**跨載體通用**的撰寫原則可參考該 skill，不綁定任何特定儲存格式；若未採用，仍可依「一則記錄一個結論」的原子性原則自行撰寫，只是不會有該 skill 提供的完整跨載體寫作原則清單可查。標題應表達具體結論而非主題，此原則綁定「原子記憶檔案」這個已排除的形態，未跨載體抽取；各目的地已有自己的標題慣例（error-pattern 用現象 slug、ticket 用 what 欄位、規則用「規則 N：主題」）。

**為什麼分流在寫入前**：

捕獲時三分流讓每筆知識寫入時態即確定去向（canonical 層 / docs 或 CLAUDE.md / 不記錄），不會產生「已記下待評估」這種不可觀測、無限積壓的中間態（PC-061「Memory upgrade blindness」的結構性解——量化證據為 130 檔事後標註率僅 4%）。

**參考資源**：

- 強制規則：`.claude/pm-rules/pm-quality-baseline.md` 規則 7「知識捕獲時分流」
- 錯誤模式：`.claude/error-patterns/process-compliance/PC-061-memory-upgrade-blindness.md`
- 完整決策樹：`references/upgrade-decision-tree.md`

---

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Section on continuous learning
- `/learn` command - Manual pattern extraction mid-session

---

版本紀錄在同目錄的 `CHANGELOG.md`。
