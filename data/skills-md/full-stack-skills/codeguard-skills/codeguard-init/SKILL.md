---
name: codeguard-init
description: 为已有仓库规划并受控接入 Codeguard，包括语言检测、linter 配置、pre-commit、AGENTS.md 规则和 CI 门禁；当用户说 /init、接入规范检查、添加 pre-commit 或 CI 时使用。必须先盘点现有配置并输出合并计划，不覆盖用户文件。
license: Apache-2.0
compatibility: 需要可读的 Git 仓库；创建/合并配置前必须确认作用域，不自动安装 hook、依赖或覆盖现有规则。
---

# 初始化项目接入 codeguard

## 工作流

### 步骤 1：检测项目语言

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/detect_lang.py" .
```

### 步骤 2：拷贝对应 linter 配置文件

| 检测到语言 | 拷贝到项目根 |
|---|---|
| Java | `linters/checkstyle/p3c-javadoc-enforced.xml` → `checkstyle.xml` |
| Java | `linters/checkstyle/checkstyle-suppressions.xml` → `checkstyle-suppressions.xml` |
| Rust | `linters/clippy/strict.toml` → `clippy.toml` |
| TypeScript | `linters/eslint/recommended.cjs` → `eslint.config.js` |
| Python | 追加 `linters/ruff/pyproject-snippet.toml` 的 `[tool.ruff]` 块到 `pyproject.toml` |

### 步骤 3：写 .pre-commit-config.yaml

如果项目根**没有** `.pre-commit-config.yaml`，从 `linters/pre-commit/.pre-commit-config.template.yaml` 拷贝并按本项目语言**裁剪**（删掉不适用的语言块）。

如果**已有** `.pre-commit-config.yaml`，询问用户：「检测到已有 pre-commit 配置，是否合并 codeguard 项？」

### 步骤 4：增量更新 AGENTS.md

如果没有 `AGENTS.md`，创建并写入：

```markdown
# AGENTS.md

## 代码规范（由 codeguard 插件管理）

- 项目使用 [codeguard](https://github.com/partme-ai/partme-codeguard-plugin)
- 检测到的语言：<从步骤 1 输出>
- Linter：checkstyle (Java) / clippy (Rust) / eslint (TS) / ruff (Python)
- **AI 写代码会被 PostToolUse 钩子强制 lint**；失败会阻塞继续
- **用户要求「提交/push」时** UserPromptSubmit 钩子会再次确认全部通过
```

如果已有 `AGENTS.md`，**追加**上述章节，不要覆盖已有内容。

### 步骤 5：写 GitHub Actions CI（可选）

如果项目根**没有** `.github/workflows/`，询问用户：「是否生成 GitHub Actions 工作流？」

如果是，写 `.github/workflows/lint.yml`：

```yaml
name: lint
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4   # Java 项目需要
        with: { distribution: temurin, java-version: 17 }
      - uses: actions/setup-python@v5  # Python 项目需要
        with: { python-version: '3.10' }
      - uses: actions/setup-node@v4    # TS 项目需要
        with: { node-version: '20' }
      - uses: arduino/setup-protoc@v1  # 仅 Rust 需要（如适用）
      - run: pip install pre-commit
      - run: pre-commit run --all-files
```

### 步骤 6：询问用户

输出安装指令（不自动执行）：
```bash
pip install pre-commit
pre-commit install
```

并提醒：「pre-commit 已配置好。现在每次 git commit 时会自动跑 linter。」

## 边界

- 不要删除或覆盖项目已有 `.pre-commit-config.yaml` / `checkstyle.xml` / `eslint.config.js`
- 不要覆盖已有 `AGENTS.md` 内容（只追加章节）
- 不要自动执行 `pre-commit install`（让用户决定）

## 不适用范围（什么时候不该用）

- 用户只要一次性 lint 检查，不想修改仓库配置。
- 仓库已有另一套受管质量门禁，但尚未确定是合并还是保留。
- 要求全局安装 CLI、修改开发者本机 hook 或发布 CI，却没有明确授权。

## 数据与安全

初始化应在本地完成，不收集、上传或记录仓库代码和凭据。生成 CI 时不得将 token、密码或内网地址写入工作流；使用 secret name 占位并说明所需的最小权限。

## 受控 Workflow

### Step 1：读取仓库指令

确认 Git 根、分支、未提交改动、AGENTS/CLAUDE 指令和现有 CI/规格文档。

### Step 2：只读盘点

列出已有 linter、formatter、pre-commit、CI、ignore、suppression 和生成文件规则，对每个文件标注 create/merge/skip。

### Step 3：检测语言并核对能力

将 `codeguard detect` 结果与仓库实际构建文件交叉验证；对 `planned` 语言不生成伪门禁。

### Step 4：生成合并计划

在写文件前展示将创建、修改、保留的目标和风险。已有配置冲突时停止并请用户决定。

### Step 5：执行最小接入

只对已批准文件做增量修改；保留既有版本、自定义规则和用户注释。

### Step 6：验证配置

运行配置 parser、Codeguard detect/check dry-run 和 CI 语法检查；工具不可用时报告 `UNVERIFIED`。

### Step 7：交付手动动作

清晰列出需用户安装的工具、hook 启用、secret 配置和首次 CI 验证，不冒充已完成。

## Rules

1. 任何已有配置先 merge，不直接覆盖。
2. 不为了开启 Codeguard 删除团队自定义规则。
3. 不自动安装全局工具、Git hook 或 CI secret。
4. 只有实际执行并通过的门禁才能报告已接入。
5. 配置改动必须带 diff 摘要和回退方法。

## 输出模板

```text
Codeguard init 结果
- 仓库/模块：<scope>
- 语言：<detected + evidence>
- 现有门禁：<inventory>
- 文件处理：<create/merge/skip>
- 已验证：<commands and exits>
- 未验证：<missing tools/CI/secrets>
- 用户待执行：<hook/install/publish actions>
```

## Gotchas

1. **YAML 合并不是文本追加**：重复 key 可让 CI 配置静默覆盖。
2. **pre-commit hook 与 CI 不是同一证据**：本地 hook 已安装不代表远程 workflow 可运行。
3. **工具版本漂移**：应尽可能复用仓库既有版本锁定。
4. **monorepo 作用域**：根配置可能不适用每个子包，需明确 working-directory。
5. **现有未提交文件**：重叠修改不得用生成模板覆盖。
6. **只生成文件不等于接入完成**：还需实际 parser、check 和 CI 运行证据。

## 按需加载资源

- 进行现有配置盘点时读取 `references/rules/merge-policy.md`。
- 设计接入顺序和回退时读取 `references/operations/adoption-playbook.md`。
- 根据仓库现状只读取 `examples/` 中的对应示例。
