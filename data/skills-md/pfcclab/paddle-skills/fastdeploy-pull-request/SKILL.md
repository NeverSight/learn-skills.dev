---
name: fastdeploy-pull-request
description: |
  自动创建或更新 GitHub Pull Request。
  当需要为 FastDeploy 仓库创建 PR 时，优先使用本 skill。
---

# FastDeploy 仓库 PR 创建与更新

## 流程

### 1. 检查分支状态

- 检查当前分支是否已经推送到远端；如果没有，执行 `git push -u origin HEAD`。
- 如果当前分支名是 `develop` 或 `main`，在继续之前先向用户确认是否真的要在该分支上直接提 PR。
- FastDeploy 默认分支是 `develop`，PR 通常应该合入 `develop` 分支。

### 2. 按逻辑主题整理改动

- 不要机械地罗列每一次 commit。
- 按照「功能 / 目的」对改动进行分组，回答：
  - 为什么需要这次改动？
  - 解决了什么问题？
  - 大致改了哪些模块？

### 3. 使用 FastDeploy 官方 PR 模板

- PR 内容必须遵循 FastDeploy 官方 PR 模板：
  - 模板链接：`https://github.com/PaddlePaddle/FastDeploy/blob/develop/.github/pull_request_template.md`
  - **CI 会自动检查以下必填章节，缺失将导致 CI 失败**：

```markdown
## Motivation

<!-- 描述本 PR 的目的和目标 -->

## Modifications

<!-- 详细说明本 PR 中所做的改动 -->

## Usage or Command

<!-- 如果是新功能，提供使用方法 -->
<!-- 如果是性能优化或 bug 修复，提供运行命令 -->

## Accuracy Tests

<!-- 如果本 PR 影响模型输出（如修改 kernel 或模型前向代码），提供精度测试结果 -->

## Checklist

- [ ] Add at least a tag in the PR title.
- [ ] Format your code, run `pre-commit` before commit.
- [ ] Add unit tests. Please write the reason in this PR if no unit tests.
- [ ] Provide accuracy results.
- [ ] If the current PR is submitting to the `release` branch, make sure the PR has been submitted to the `develop` branch, then cherry-pick it to the `release` branch with the `[Cherry-Pick]` PR tag.
```

### 4. PR 标题规范

标题必须包含至少一个标签，格式为 `[TAG] 简要说明`。

#### 可用标签列表

| 类别 | 标签 |
|-----|------|
| **模块** | `[FDConfig]` `[APIServer]` `[Engine]` `[Scheduler]` `[PD Disaggregation]` `[Executor]` `[Graph Optimization]` `[Speculative Decoding]` `[RL]` `[Models]` `[Quantization]` `[Loader]` `[OP]` `[KVCache]` `[DataProcessor]` |
| **类型** | `[BugFix]` `[Docs]` `[CI]` `[Optimization]` `[Feature]` `[Benchmark]` `[Others]` |
| **硬件** | `[XPU]` `[HPU]` `[GCU]` `[DCU]` `[Iluvatar]` `[Metax]` |

#### 标题示例

- `[BugFix] Fix memory leak in data processor`
- `[Feature][APIServer] Add streaming response support`
- `[Optimization][KVCache] Improve cache eviction strategy`
- `[XPU][OP] Add flash attention kernel for XPU`

#### 避免的标题

- `fix bug` / `update code` / `test` / `temp` / `WIP`

### 5. 使用 gh 命令创建 PR

示例命令（根据实际情况替换标题和正文）：

```bash
gh pr create --base develop --title "[BugFix] Fix xxx issue" --body "$(cat <<'EOF'
## Motivation

简要说明为什么需要这个 PR，解决什么问题。

## Modifications

- 修改了 xxx 文件
- 新增了 xxx 功能
- 删除了 xxx 代码

## Usage or Command

```bash
python -m fastdeploy.entrypoints.openai.api_server --model xxx
```

## Accuracy Tests

| Model | Before | After |
|-------|--------|-------|
| xxx   | xxx    | xxx   |

## Checklist

- [x] Add at least a tag in the PR title.
- [x] Format your code, run `pre-commit` before commit.
- [x] Add unit tests. Please write the reason in this PR if no unit tests.
- [x] Provide accuracy results.
- [ ] If the current PR is submitting to the `release` branch, make sure the PR has been submitted to the `develop` branch, then cherry-pick it to the `release` branch with the `[Cherry-Pick]` PR tag.

EOF
)"
```

### 6. Cherry-Pick PR 规范

如果是 Cherry-Pick 到 release 分支：
- 标题格式：`[Cherry-Pick][原标签] 原标题(#原PR号)`
- 示例：`[Cherry-Pick][CI] Add check trigger and logic(#5191)`

## 注意事项

- **所有章节必填**：CI 会检查 Motivation、Modifications、Usage or Command、Accuracy Tests、Checklist 五个章节，任一缺失将导致 CI 失败。
- **Checklist 必须勾选**：CI 会检查 Checklist 中的项目是否已勾选。
- **代码风格检查**：提交前需运行 `pre-commit`，CI 会自动检查代码风格。
  ```bash
  pip install pre-commit==4.2.0
  pre-commit install
  pre-commit run --all-files
  ```
- 如果业务或背景信息不清楚，应先向用户提问澄清，再生成 PR 描述。
- 成功创建或更新 PR 后，应返回 PR URL，方便用户查看。
