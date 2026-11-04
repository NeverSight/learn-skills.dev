---
name: board
description: 任务板——拉取最新进度、领取派给本 lane 的就绪任务、干完标记完成并自动给下游 lane 派活。当用户说"看板/任务板/我该干啥/领任务/同步进度/标记完成"时使用。基于 git + board/ 文件协同，跨 lane 自动交接。
---

# board —— 任务板与自动交接

**lane**: 全部（每个 lane 会话各跑各的）  ·  引擎: `tools/board.py`（确定性，任何模型可用）

三个 lane 不能直接通信，只能靠 **git 仓库 + board/ 任务文件**协同。本 skill 让你：拉取 → 看派给自己的就绪任务 → 干 → 标完成（自动给下游 lane 派活）→ 推送。

## 先确定本机 lane
读仓库根的 `.elec-lane`（未跟踪文件）。若不存在，**问用户本机是哪个 lane**（lead/硬件/控制/算法），写入 `.elec-lane`（一行，如 `控制`）。后续都用它。

## 每次被调用的动作
1. `git pull --rebase`（取别人提交的进度与新派的任务）。
2. `python tools/board.py list --lane <本机lane>` —— 列出**派给我、依赖已全 done** 的就绪任务。
3. 若无就绪任务：`python tools/board.py status` 给全局，告诉用户在等谁（阻塞依赖），结束。
4. 若有：
   - `skill` 类任务 → 调它的 hint 指向的 skill（如 `/interconnect`），按那条流水线干完。
   - `manual` 类任务（连线/整定）→ 把 hint 指的清单/产物摊给用户去做。
5. 干完一个：`python tools/board.py done <id> --by <本机lane>`。这会**自动按 DAG 给下游 lane 派生任务**（写新 board/ 文件）。
6. `git add board/ <你的产物目录> && git commit -m "board: done <id>" && git push`。
7. 告诉用户：完成了什么、自动派给了哪些 lane 什么任务、本 lane 还有无下一个就绪任务。

## 近实时（可选）
让本 lane 会话挂轮询，自动看新派来的任务：
- Claude 原生：`/loop 5m /board`（每 5 分钟 pull+看板）。
- 纯终端：`sh tools/watch.sh <本机lane> 300`。

## 注意
- **只动自己 lane 的产物目录 + board/**（目录归属见 CLAUDE.md），避免 git 冲突。
- 任务板是协作式的：它让交接显式、可审计；但跨机器是 **pull 驱动**，别人要 `git pull` 才看得到你派的活（故有轮询）。
- 流水线 DAG 固定在 `tools/board.py`（read-problem→…→整车联调）；要改交接关系改那里（lead 维护）。
