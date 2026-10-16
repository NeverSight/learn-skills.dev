---
name: agri-branch
description: Creates a Git branch for the current task when branch creation is requested.
metadata:
  author: Lucas Yang
  version: "2026.10.16"
---

# agri-branch

## 工作流程

1. 用 `git branch --show-current` 確認目前分支；不在 `main` 或 `develop` 就維持原分支並結束。
2. 用 `git status --long` 查看工作區變更，作為命名的補充資訊；以使用者描述的工作內容為主要依據。
3. 依工作內容取簡短、具體的分支名稱：新功能用 `feat/<branch-name>`，修正問題用 `fix/<branch-name>`，雜項調整用 `chore/<branch-name>`。使用者指定名稱就沿用；資訊不足以判斷時先詢問。確定名稱後執行 `git switch -c <名稱>`；指令失敗就回報，不能宣稱已開好分支。
4. 用 `git branch --show-current` 確認目前分支名稱與預期名稱相同。

## 注意事項

- 只負責開分支；提交、推送與建立 PR 由各自流程處理。
- 團隊 Gitflow 為 `feat/*`／`fix/*`／`chore/*` → `develop` → `main`（正式發佈）。
