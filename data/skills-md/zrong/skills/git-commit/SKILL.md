---
name: git-commit
description: Git 提交并打 CalVer 标签。当用户说"提交"、"commit"、"打标签"、"tag"、"发版"时使用。
---

# Git Commit with CalVer Tag

将当前更改提交到 git 并按 CalVer 规则打 tag。

## 工作流程

1. **更新 CLAUDE.md**：将本次更新的摘要写入项目根目录的 `CLAUDE.md` 文件（如不存在则创建）。
2. **检查文档**：如果项目中存在 `docs/` 目录，检查是否需要同步更新文档。不存在则跳过。
3. **Git 提交**：执行 `git add` 和 `git commit`。如果 `$ARGUMENTS` 非空，将其作为 commit message；否则根据变更内容自动生成。
4. **计算版本号**：运行以下命令获取下一个 CalVer 版本号（**禁止手动计算，必须使用此脚本**）：
   ```bash
   python3 scripts/calver.py
   ```
5. **打 Tag**：使用脚本输出的版本号执行 `git tag <版本号>`。
6. **展示结果**：显示 commit 和 tag 信息，提示用户如需推送可执行：
   ```bash
   git push && git push --tags
   ```

## CalVer 规则

- 格式：`YY.WW.MICRO`
- `YY`：ISO 年份后两位，无前导 0
- `WW`：ISO 周数，无前导 0
- `MICRO`：从 1 开始的全局递增序号，跨年不重置

## 注意事项

- 不自动执行 `git push`，推送是不可逆操作，需用户明确要求
- 版本号计算完全依赖 `scripts/calver.py` 脚本，确保准确性
