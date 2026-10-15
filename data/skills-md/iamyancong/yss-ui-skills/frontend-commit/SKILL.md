---
name: frontend-commit
description: 分析并提交 Vue、React、TypeScript、JavaScript、Vite、微前端和前端 monorepo 项目的 Git 改动；当用户要求生成 commit message、检查提交规范、拆分原子提交、暂存并执行 git commit，或修复 commitlint 与 commit-msg hook 拒绝时使用。读取仓库实际规则和 diff，选择业务 scope，生成英文 type/scope 与中文标题和正文，并安全验证提交。
---

# 前端规范提交

## 触发条件

- 用户要求为前端项目生成 commit message、检查提交规范或执行 `git commit`。
- 需要将混合改动拆分为原子提交，或评估当前暂存区是否可以安全提交。
- commitlint、`commit-msg` 或 `pre-commit` hook 拒绝提交，需要按规则修复。
- 适用于 Vue、React、TypeScript、JavaScript、Vite、微前端和前端 monorepo 仓库。

## 不适用场景

- yss-ui 组件库仓库自身的提交与发版：使用 `../commit-linting/SKILL.md`。
- Java、Spring Boot、Maven、Gradle 后端仓库：使用 `../java-backend-commit/SKILL.md`。
- 仅请求代码实现，不涉及提交信息或 `git commit` 操作。
- 无代码改动，或改动内容与提交请求不匹配。
- 合并提交、发布提交和自动依赖机器人提交：遵循仓库专用流程，不套用本技能的常规消息模板。

## 硬约束（禁止/必须）

- 必须把仓库规则视为最高优先级：依次遵循 `AGENTS.md`、`CONTRIBUTING.md`、Git hooks、解析后的 commitlint 配置、本地配置和近期历史；通用规则只作回退。
- 只在用户明确要求提交时执行暂存和 `git commit`；若仅要求提交信息或审查，只输出候选消息与依据。
- 必须保留用户和他人的既有改动。禁止默认使用 `git add -A`、`git add .`、`git commit -a`、`--no-verify`，也不要自动 amend、rebase、push 或改写已发布历史。
- 提交必须是单一逻辑变更。不要用提交信息掩盖混杂的功能、修复、格式化或临时文件。
- 遇到密钥、令牌、私钥、证书、`.env` 实值、账号数据或意外大文件时停止提交并报告具体路径，不要在输出中泄露内容。
- 已有暂存内容视为用户选择，除非用户授权，不要擅自取消暂存或混入其他文件。
- `fixup!` 只用于用户明确要求的评审或 autosquash 工作流，不能作为最终历史的默认提交。
- revert 优先使用 Git 生成的回滚信息并保留被回滚 SHA，再根据仓库规范校验；不要把普通反向修改伪装成 revert。

## 工作流

### 1. 建立仓库契约

1. 确认仓库根目录、当前分支和工作树状态。
2. 搜索并读取仓库级说明、贡献指南、提交模板、commitlint 配置和 `commit-msg`、`pre-commit` hooks。
3. 检测 `package.json`、lockfile、workspace 配置和前端应用或包边界。
4. 如果仓库使用 commitlint，优先使用本地依赖按包管理器读取解析后的配置，例如 `pnpm exec commitlint --print-config json`；不要为了校验联网安装依赖。
5. 查看相关路径近期的非 merge 提交，了解仓库已经形成的 scope 和语言习惯，但不要复制历史中的明显错误。

### 2. 审查真实改动

至少检查：

```bash
git status --short --branch
git diff --cached --name-status
git diff --cached
git diff --name-status
git diff
git ls-files --others --exclude-standard
```

- 同时理解暂存区、未暂存区和未跟踪文件；不要只依据文件名生成消息。
- 将改动按用户可理解的行为和因果关系分组。功能实现、配套测试和为该功能必需的最小配置可以属于同一原子提交。
- lockfile 必须与对应 manifest 一起提交。只提交项目本来就跟踪且由本次意图产生的生成代码；排除构建产物、缓存和临时文件。
- 若无改动、改动与请求不符、多个逻辑变更无法安全拆分，先说明并停止。需要逐行拆分同一文件时，不要靠猜测改写暂存区。

### 3. 选择 type、scope 与正文

先读取 `./references/scope-and-examples.md`，再按「标准代码骨架」的格式生成。

- type 默认从 `feat/fix/docs/style/refactor/perf/test/chore/revert/build/ci` 中选择，但仓库枚举优先。
- scope 优先级为：仓库枚举 → monorepo 包或应用 → 业务模块 → 共享能力。使用小写 kebab-case；不要机械地以 `views`、`hooks` 或文件名作为 scope。
- 标题使用英文 type/scope、ASCII `:` 和中文摘要；描述行为或价值，不写“修改文件”“更新代码”或单个文件名。
- 默认将完整 header 控制在 72 个字符内；仓库存在更严格限制时服从仓库。标题末尾不加句号，不用 emoji 或全角冒号。
- 简单单文件变更可以没有 body；多文件、非显然修复、重要功能或行为变化使用 body 解释做了什么、为什么以及如何验证。
- 仅对真实不兼容变更使用 `!` 和 `BREAKING CHANGE:`；仅在已知编号或仓库要求时加入工单、DCO、`Signed-off-by` 等 footer，禁止编造。

### 4. 验证并提交

1. 根据变更范围运行仓库已有的最小充分检查，例如相关单元测试、类型检查、lint 和构建检查；优先使用仓库脚本与当前包管理器。
2. 通过 stdin 校验完整候选消息，而不只校验 header。使用仓库本地 commitlint 命令；退出码为 0 才继续。
3. 仅暂存属于当前原子提交的明确路径或安全 hunks，再重新检查 `git diff --cached --check`、`--name-status` 和完整 staged diff。
4. 执行正常 `git commit`，允许 hooks 运行。
5. hook 若格式化或修改文件，重新检查 staged 与 working tree，确认实际提交内容没有漂移。
6. 提交成功后检查 `git show --stat --oneline --decorate HEAD` 和 `git status --short`，向用户报告 commit hash、消息、已运行检查以及剩余未提交改动。

## 标准代码骨架

```text
type(scope)!: 中文行为摘要

- 说明关键行为或原因
- 说明兼容性、测试或必要约束

BREAKING CHANGE: 说明不兼容影响和迁移方式
Refs: 已知工单号
```

示例：

```text
feat(data-push): 优化推送任务数据源与调度规则展示

- 将英文星期转换为中文调度描述
- 按数据源目录映射业务名称并补充单元测试
```

## 交付检查清单

- [ ] type 与 scope 通过仓库 resolved commitlint 校验，完整消息经 stdin 校验退出码为 0。
- [ ] scope 来自仓库枚举、包名或业务模块，未使用 `views`、`hooks`、`utils` 或文件名兜底。
- [ ] 标题为英文 type/scope + ASCII 冒号 + 中文摘要，完整 header 不超过 72 字符。
- [ ] 暂存区只包含当前原子提交的文件；lockfile 与对应 manifest 同提交。
- [ ] 已运行与变更范围匹配的最小充分检查（相关测试、类型检查、lint）。
- [ ] 提交后已核对 `git show --stat` 与 `git status --short`，并向用户报告 hash 与剩余改动。

## 失败兜底策略

- 无法区分 `feat`、`fix`、`refactor` 时继续检查需求和行为；仍有高影响歧义则询问用户，不自动降级为 `chore`。
- hook 拒绝时按输出中的规则修正并重新校验，绝不使用 `--no-verify`。
- 仓库 parser 或 hook 不支持标准破坏性标记时，不要绕过校验或静默删掉标记；报告规则冲突，并采用仓库明确批准的兼容方案。
- 多个逻辑变更无法安全拆分时，先给出拆分方案并停止，不强行生成“大杂烩”提交。
- 发现密钥或意外大文件时停止提交，报告具体路径并等待用户处理。
