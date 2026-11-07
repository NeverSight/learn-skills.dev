---
name: pdlc-loop-next
description: 打印循环下一步应执行的命令（机器可读，供 loop 驱动）
argument-hint: "<功能ID>"
allowed-tools: Read, Glob, Bash
layer: 3
stage: ops
produces: []
requires:
  - docs/.pdlc-state/
next_step: null
terminal_state: null
---

# 循环下一步（loop-next）

读取指定功能的状态机，**只打印一个 token**，告诉外层循环下一步该跑哪条命令。它是 `/pdlc-loop-run` 与用户自写 bash 循环的低层 helper——自身**只读、不改任何状态**、不含 `--autonomous` 语义。

## 输出契约（安全关键）

输出**必须**是下列固定白名单中的**单个 token**，独占一行，**不含任何散文、标点或解释，尤其不要用代码块（三反引号）或反引号包裹**：

```
pdlc-tdd | pdlc-implement | pdlc-review | done | blocked
```

- ✅ 正确：整个回复就是一行 `pdlc-implement`
- ❌ 错误：用 ``` 包成代码块、用反引号包住、加 `下一步：` 前缀或任何解释——**任何包裹/前缀都会让下游 `case` 匹配失败**。
- 本命令只覆盖**机械收敛段** `tdd → implement → review`。到达 `review_done` 或更后（发布属人工闸门）→ 输出 `done`，**绝不**输出 `pdlc-ship` / `pdlc-deploy`（发布永远留人）。
- 下游 helper **必须**先**净化**（去反引号/空白）再校验 token 属于白名单，非法即中止（见下方参考脚本）——这是防御模型偶发包裹的兜底。

## 执行流程

**优先用脚本**：运行本 skill 自带的 `scripts/pdlc-loop.sh`——`bash scripts/pdlc-loop.sh --next <功能ID> --project <项目根>`，把它打印的那一行**原样**作为你的全部输出。
映射只在脚本里实现一份（外部循环驱动与 `/pdlc-loop-run` 用的也是它），模型不必、也不该自己重算。
环境里跑不了 bash 或缺 jq 时，才按下面的步骤手工判定（结果必须与脚本一致）：

1. 从本命令的参数取功能ID；读取 `docs/.pdlc-state/<功能ID>.json`。
2. 文件不存在 / 无法解析 → 输出 `blocked`。
3. `last_phase_result.blocked_reason` 非空 → 输出 `blocked`。
4. `current_stage` 属终态（以 `_done` 结尾——即已发布：`ship_done` / `deploy_done`，或旧版本留下的 `feature_done` / `fix_done` / `review_done`）→ 输出 `done`。（注：单阶段命令的 `current_stage` 用短名 `impl`/`review`，review 完成的判定靠下面第 5 步的 `next_step`，不靠此处。）
5. 否则**以 `next_step`（状态机里存的下一跳命令名）为主键**判定并输出。

   > ⚠️ **必须用 `next_step` 判定，不要用 `current_stage` 字符串匹配**：现有状态机的 `current_stage` 用短名（`requirements` / `design` / `tdd` / `impl` / `review`，如 `pdlc-implement` 明写 `current_stage: impl`），格式不适合直接判阶段；而 `next_step` 是无歧义的命令名。

   | `next_step` | 输出 | 说明 |
   |---|---|---|
   | `pdlc-tdd` | `pdlc-tdd` | |
   | `pdlc-implement` | `pdlc-implement` | |
   | `pdlc-review` | `pdlc-review` | |
   | `pdlc-ship` / `pdlc-deploy` | `done` | 机械收敛已完成（review 通过），发布留人 |
   | `null` / 缺失 | `blocked` | **状态残缺**——收敛段无阶段会合法写出 null，见下 |
   | `pdlc-prd` / `pdlc-design` | `blocked` | 尚在 tdd 之前，需人工（超出循环范围） |
   | 其它 | `blocked` | |

   > ⛔ **`null` 判 `blocked` 而不是 `done`**：机械收敛段里没有任何阶段会合法写出
   > `next_step: null`——`pdlc-implement` 与 `pdlc-fix` 写 `pdlc-review`，`pdlc-review`
   > 写 `pdlc-ship`（即 `pdlc-fix` 写 `pdlc-review`：修复也要先过评审）。**收敛完成的信号是 `next_step=pdlc-ship`**（上表已单独映射到
   > `done`），不是 `null`。所以 `null` 只可能是状态残缺，判 `done` 等于把「什么都
   > 没发生」报成「机械阶段已完成」——上层会以为可以进发布评估了。
   >
   > 注意这类输入**逃得过「无法解析 → blocked」的兜底**：`{}` 是合法 JSON，
   > 解析得了、只是什么都没有。展示层早有同一结论（`bin/pdlc-statusline.sh` 的
   > `is_terminal`：`/pdlc-task` 的 `next` 恒为 `null` 却未必完成，误判会显示「✅ done」）。

6. 不写文件、不产任何 artifact。

<!-- adapter:claude-only-start -->
## 参考 helper（供 usage-guide / 外层循环使用，含白名单校验）

```bash
# 净化：把输出切成 token（去反引号、按空白分行）再用 grep -x 整 token 匹配白名单——
# 容忍空白/代码块包裹，又避免从 done_at / blocked_reason 等子串里误抽 done/blocked
RAW=$(claude -p "/pdlc-loop-next $ID")
CMD=$(printf '%s' "$RAW" | tr '`' ' ' | tr -s ' \t' '\n' | grep -xE '(pdlc-tdd|pdlc-implement|pdlc-review|done|blocked)' | head -1)
case "$CMD" in
  pdlc-tdd|pdlc-implement|pdlc-review)
    claude -p "/$CMD $ID --autonomous" ;;
  done)    echo "✅ 已到 review_done，交人工决定是否 /pdlc-ship"; break ;;
  blocked) echo "⛔ 需人工介入"; break ;;
  *)       echo "❌ 非法命令（原始输出：$RAW）"; exit 1 ;;
esac
```
<!-- adapter:claude-only-end -->

功能ID: $ARGUMENTS
