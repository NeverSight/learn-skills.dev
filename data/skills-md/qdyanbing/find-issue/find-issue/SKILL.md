---
name: find-issue
description: Inspect a local source repository to find real, user-observable bugs. Trace public behavior through runtime code, exclude intended behavior and already-filed GitHub issues or pull requests, build and independently check a minimal public reproduction, and write an issue-ready Markdown draft that remains unverified until a human confirms it. Use when asked to scan code for bugs, find high-value issue candidates, validate a suspected defect, produce issue-ready Markdown with a reproduction link, or record a user-marked non-issue into not-issues.md.
---

# 寻找真实 Issue

从本地源码中寻找已经确认、用户可观察的问题，并产出可直接提交的 Issue 文档。除非用户另行明确要求，否则不要修改目标项目代码、切换分支、提交代码、提交 Issue 或创建 PR。

## 必要条件

- 必须提供环境变量 `FIND_ISSUE_CONFIG_PATH`，指向一份独立配置文件。不要在 skill 中写死项目名或个人路径。只认这一种配置来源，不要使用 `--config`、当前工作目录、用户级配置文件或其他环境变量。
- 复现应使用目标项目真实支持的公开入口和可获取版本。库项目优先验证已发布版本；应用项目验证用户指定或公开可达的版本。
- 需要发布 CodeSandbox 时，从配置文件读取 `csbApiKey`。禁止从环境变量、`~/.zshrc` 或其他位置查找 Token；禁止打印、持久化或把 Token 放进命令参数。
- 没有可用的公开复现时，该候选不能写成 Issue。

## 读取配置

如果当前环境没有 `FIND_ISSUE_CONFIG_PATH`，立即停止，并告诉用户：必须设置 `FIND_ISSUE_CONFIG_PATH` 为 find-issue 配置文件的路径。不要猜测路径，不要回退到其他查找方式。

将当前 `SKILL.md` 所在目录记作 `<skill-directory>`。执行：

```bash
node "<skill-directory>/scripts/resolve-config.mjs"
```

配置格式见 [config.example.json](config.example.json)。配置文件必须包含 `sourceDirectory` 和 `outputDirectory`。`repositoryUrl` 用于对照 GitHub 上已有 Issue 和 PR。发布 CodeSandbox 时还需要 `csbApiKey`。相对路径以配置文件所在目录为基准解析。环境变量未设置、文件不存在或内容无效时停止，并请用户补全配置。

## 工作流程

1. 完整阅读 [references/scanning-guide.md](references/scanning-guide.md)。
2. 读取配置，把 `sourceDirectory` 作为只读扫描仓库，把 `outputDirectory` 作为 Issue 文档目录。确认两个目录不是 skill 自身目录。
3. 若 `outputDirectory/not-issues.md` 存在则完整阅读，其中已记录的现象不得再次写成 Issue。文件不存在时不要创建。同时读取输出目录中的其他 `*.md`，检查重复问题、已提交 Issue、已合并修复和处理中 PR，避免重复产出。
4. 检查源码工作树，但不要切换分支或触碰用户改动。从默认分支、本地稳定基线、对应远端引用或用户指定基线扫描。不要通过线上 Issue 搜索来发现候选；线上检索只用于排除已经存在的 Issue 或 PR。
5. 从公开 API、命令、配置或用户操作一路追踪到运行时。可疑代码看起来是刻意添加时，使用 `git blame`、`git log -S`、`git log -L` 和引入提交还原背景。必须解释功能影响，不能因为写法异常就判定为 Bug。
6. 先通过目标项目现有测试、demo、CLI 或最小本地程序确认候选。本地都无法稳定复现时直接放弃，不要写成 Issue。
7. 配置了 `repositoryUrl` 时，用候选标题和可识别关键词检索已有 Issue 与 PR：

   ```bash
   node "<skill-directory>/scripts/check-existing.mjs" --query 'candidate title keywords'
   ```

   返回 `skipped: true` 表示未配置 `repositoryUrl`，继续后续步骤。匹配结果里若已有同一现象的 Issue 或 PR，无论 open、closed 还是 merged，都放弃该候选。不要为了发现新问题去搜 GitHub。
8. 根据项目类型选择复现载体。浏览器可运行的问题优先使用 CodeSandbox；其他运行时使用能够匿名访问、无需修改目标仓库且适合该生态的公开复现。不要为了使用 CodeSandbox 改变问题成立条件。做不出公开复现时放弃该候选，不能把它当成 Issue。
9. 申请临时输入文件，并把 JSON 写到返回的 `inputPath`。不要把该文件写进 `sourceDirectory`、`outputDirectory` 或 skill 目录：

   ```bash
   node "<skill-directory>/scripts/temp-input.mjs"
   ```

   按 [references/issue-contract.md](references/issue-contract.md) 准备输入 JSON。`slug` 使用英文 kebab-case；发布前将 `status` 设为 `unverified`。候选结束或落盘成功后删除该临时目录。
10. 仅当复现使用 CodeSandbox 时，在没有网络副作用的情况下校验请求内容：

   ```bash
   node "<skill-directory>/scripts/create-reproduction.mjs" --input /absolute/path/from-temp-input/input.json --dry-run
   ```

   不使用 CodeSandbox 时跳过本步和下一步，不要因为缺少 `csbApiKey` 而停止整个流程。
11. 仅当复现使用 CodeSandbox 时创建独立、公开的 Sandbox：

   ```bash
   node "<skill-directory>/scripts/create-reproduction.mjs" --input /absolute/path/from-temp-input/input.json
   ```

   此时配置中必须有 `csbApiKey`；没有就停止，并请用户写入配置。脚本只从 `FIND_ISSUE_CONFIG_PATH` 指向的配置文件读取密钥；不得把 Token 展开进命令文本。
12. 匿名打开公开复现。等待运行环境就绪，检查页面、日志或控制台，执行文档中的操作步骤，并确认实际结果与描述一致。这个步骤只验证复现本身可用，不构成人工核验。没有可用的公开复现链接时不要调用 `write-issue.mjs`。
13. 复现检查失败时先修正或放弃候选；在修正本地输入前不要反复发布替代复现。复现检查成功后，将链接写入 `reproductionUrl`，但 `status` 仍保持 `unverified`。
14. 先预览再按配置落盘：

   ```bash
   node "<skill-directory>/scripts/write-issue.mjs" --input /absolute/path/from-temp-input/input.json --dry-run
   node "<skill-directory>/scripts/write-issue.mjs" --input /absolute/path/from-temp-input/input.json
   ```

15. 重新阅读生成的 Markdown，确认 frontmatter 为 `status: unverified`，并包含标题、问题描述、在线复现、最小代码或配置、编号步骤、期望结果、实际结果和环境信息。
16. 只有用户明确表示已经人工核验该问题，并要求或同意标记为已验证后，才能执行：

   ```bash
   node "<skill-directory>/scripts/mark-verified.mjs" --issue /absolute/path/to/issue.md
   ```

   模型、子代理、自动化测试、浏览器操作或公开复现检查均不算人工核验，不得据此把状态改为 `verified`。
17. 只有用户明确把某条候选或已有文档判定为非问题时，才把现象总结成一行，写入临时 JSON 并执行：

   ```bash
   node "<skill-directory>/scripts/temp-input.mjs"
   node "<skill-directory>/scripts/record-not-issue.mjs" --input /absolute/path/from-temp-input/input.json
   ```

   JSON 必须包含 `summary`。若输出目录里已经有对应 Issue 文档，同时写入 `slug`，脚本会删除该文件。不要在扫描阶段或用户未判定时写入。文件不存在时脚本会在 `outputDirectory` 创建 `not-issues.md`。条目格式见 [references/issue-contract.md](references/issue-contract.md)。完成后删除临时目录。

## 完成标准

- 每个已确认问题只生成一个新的 Markdown 文件，文件名与英文 kebab-case 的 `slug` 一致。
- 新生成的 Issue 文档必须为 `status: unverified`，即使模型已经独立运行并确认公开复现。
- 只有收到用户明确的人工核验结论后，才允许把已有文档改为 `status: verified`；不得自行推断用户已经核验。
- 最小复现只证明一个故障点，不构建结果面板或演示页面；同一根因影响多个相邻 API 时，选最短的一条路径复现，其余影响写入问题描述。
- 没有公开复现的候选不得写成 Issue。
- 排除合理设计选择、仅文档或命名问题、无用户影响的内部实现差异、无法稳定复现的理论缺陷，GitHub 上已有的相同 Issue 或 PR，以及 `not-issues.md` 中已记录的现象。
- 用户明确判定为非问题后，必须通过 `record-not-issue.mjs` 追加一行；若已有对应 Issue 文档，必须一并删除。不得用手写方式改该文件，也不得在用户未判定时创建它。
- 输入 JSON 只允许写在 `temp-input.mjs` 给出的临时路径，用完删除。
- 除非用户明确要求更新并使用 `--force`，否则不得覆盖已有文档。
- 不得在日志、Markdown、浏览器 URL 或最终回复中暴露任何 Token。
- 最终报告生成的 Markdown 路径、`status` 和公开复现 URL，回复保持简洁。

## CodeSandbox Token

只有复现适合 CodeSandbox 时才需要 Token。把具备 `sandbox_create` 和 `sandbox_read` 权限的密钥写入配置文件的 `csbApiKey`；只有后续需要更新 Sandbox 时才增加 `sandbox_edit_code`。创建脚本调用官方 `https://api.codesandbox.io/sandbox` 接口，并且自身没有 npm 依赖。缺少该密钥时，不要把其他类型的复现流程一并停掉。
