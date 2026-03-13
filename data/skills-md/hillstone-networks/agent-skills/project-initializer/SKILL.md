---
name: project-initializer
description: "Scaffolds new projects with README.md, AGENTS.md, and CI/CD (GitLab CI, GitHub Actions). Handles project type (generic / Flask backend / React frontend / Taro miniapp), tech stack, coding standards, quality level, and SDD (OpenSpec, SpecKit, GSD). All init flows (Flask, React, Taro) and conventions (backend-python-cicd, frontend-codegen, flask-backend-codegen, QA/testing, agent-roles/subagents) are built-in; no separate skills. Docs default to Chinese. Use when creating a project, initializing a repo, or setting up CI/CD/SDD."
---

# Project Initializer

A skill for scaffolding new projects with consistent README.md, AGENTS.md, and CI/CD pipelines — all wired together with an SDD (Spec-Driven Development) framework.

## Overview

The skill does five things:

1. **Interview** — Understand the project's goals, tech stack, coding standards, quality requirements, CI platform(s), and preferred SDD workflow.
2. **Generate** — Create README.md, AGENTS.md, and CI pipeline file(s) from templates.
3. **Integrate** — Install SDD framework tools and initialize project structure; wire coding standards and quality checks into the CI pipeline.
4. **Tag** — Embed a machine-readable project identity tag in AGENTS.md so server-side CI can verify the project was properly initialized.
5. **Verify consistency** — Make sure all generated files agree with each other (same tech stack, same quality gates, same SDD expectations).

---

## Phase 1: Interview

使用 `AskUserQuestion` 与用户进行访谈，了解项目情况。逐个问题与用户交互 — 不要跳过问题或代表用户做出决定。在进入第2阶段（文件生成）前，总结他们的答案并确认理解。

根据已有的上下文信息，可以一次性提出所有问题，也可以在自然对话中分散提问 — 根据情况自行判断。

**必需信息：**

对于以下每个问题，使用 `AskUserQuestion` 与用户交互式提问。不要跳过问题，不要代替用户做决定。当提供建议或默认值时，请通过 `AskUserQuestion` 确认用户同意后再继续。

1. **项目名称和一句话描述** — 使用 `AskUserQuestion`。这个项目是什么？它解决了什么问题？

2. **项目类型** — 使用 `AskUserQuestion` 确认项目属于哪一类，以便在 Phase 2 执行对应的初始化流程（见下方「按项目类型生成」）：
   - *通用* — 仅生成 README、AGENTS.md、CI 与 SDD，不生成框架骨架
   - *Flask 后端* — 在本技能内直接生成 Flask API 项目骨架（应用工厂、Blueprint、Service/Model 分层、uv、测试等），参考 `references/flask-backend.md` 与 `assets/flask-backend/`
   - *React 前端* — 在本技能内直接生成 React 前端骨架（Vite + Rolldown、React + TypeScript、Ant Design、Vitest、目录与配置等），见下方「React 前端初始化」
   - *Taro 小程序* — 在本技能内按 Taro 官方 CLI 初始化、目录、代理、README/AGENTS，见下方「Taro 小程序初始化」
   - *其他* — 仅通用文件
   选择后，Phase 2 在生成通用文件之外，按类型执行对应骨架生成，**不引用、不调用**任何独立 init-* 技能。

3. **技术栈** — 编程语言、框架、包管理工具、数据库、部署目标等。使用 `AskUserQuestion` 提示用户。用户表示不确定或要求建议时，根据问题领域提供合理的默认值 — 但通过 `AskUserQuestion` 获得用户确认后再继续。

4. **质量等级** — 使用 `AskUserQuestion` 提问：这是演示/原型项目还是生产项目？
   - *演示*：最小化CI、无覆盖率门槛、无安全扫描、轻量级SDD
   - *生产*：完整CI、覆盖率门槛、安全扫描、严格的SDD对齐检查

5. **SDD框架** — 使用 `AskUserQuestion` 展示所有三个选项，询问团队将使用哪一个。包括下面的描述以帮助他们做出决定。

   | 框架 | 风格 | 适用于 |
   |------|------|--------|
   | **OpenSpec** | 流畅、棕地优先、增量规范 | 现有代码库、个人开发者、迭代工作 |
   | **SpecKit** | 宪法强制、分阶段 | 团队、企业、严格的质量标准 |
   | **GSD** | 基于阶段的路线图、上下文工程 | 想让AI做主力工作的个人开发者 |

   > 选择后，阅读相应的参考文件了解更多细节：
   > - OpenSpec → `references/openspec.md`
   > - SpecKit → `references/speckit.md`
   > - GSD → `references/gsd.md`

6. **CI平台** — 使用 `AskUserQuestion` 提问：应该配置哪些CI系统？
   - *GitLab CI* — 生成 `.gitlab-ci.yml`
   - *GitHub Actions* — 生成 `.github/workflows/ci.yml`
   - *两者* — 生成两个文件，保持一致

7. **主分支名称** — 使用 `AskUserQuestion` 提问哪个分支会触发发布流程。建议用 `main` 作为默认值，但要向用户确认。

8. **编码规范** — 使用 `AskUserQuestion` 提问：团队是否有现有的编码规范、风格指南或代码检查配置？
   - *直接粘贴内容* — 用户将规范粘贴到对话中
   - *文件路径* — 用户提供现有文件的路径（如 `docs/coding-standards.md`、`.eslintrc.json`）
   - *无* — 如果没有，使用技术栈的合理默认值
   
   如果提供了规范，请阅读并总结。规范将被注入到AGENTS.md中，并用于配置CI代码检查命令。

9. **额外质量要求**（生产项目）— 使用 `AskUserQuestion` 提问：
   - 最小测试覆盖率百分比（如 80%）
   - 静态分析工具（如 ESLint、Pylint、SonarQube）— 可能已被编码规范涵盖
   - 安全扫描（Trivy、Semgrep、Bandit等）

10. **文档语言** — 使用 `AskUserQuestion` 提问：README.md和AGENTS.md应该用什么语言编写？默认为中文（中文），除非用户指定其他语言。

11. **Python + GitLab CI 规范**（仅当技术栈含 Python 且选择了 GitLab CI 时）— 使用 `AskUserQuestion` 询问：是否采用 **backend-python-cicd** 规范？若选是，则生成/校验 `.gitlab-ci.yml`、Dockerfile、部署脚本时须遵循本技能 `references/backend-python-cicd.md` 与 `assets/backend-python-cicd/`（私有镜像源、多阶段构建、分支 develop/bugfix/hotfix/master、dev→prod K8s 部署、先本地 Docker 构建再 Git 推送）。

12. **QA/测试规范** — 使用 `AskUserQuestion` 询问：是否在 AGENTS.md 中引用 **QA/测试规范**（测试计划、用例、自动化与报告、缺陷根因分析）？若选是，在 AGENTS 中增加「测试与根因分析」说明或引用本技能 `references/qa-testing.md`。

13. **多角色/子代理** — 使用 `AskUserQuestion` 询问：是否需要 **多角色规划与子代理**（.cursor/agents/*.md）？若选是，在 Phase 2 后按本技能 `references/agent-roles.md` 与 `assets/agent-roles/` 执行角色规划与子代理文件生成。

---

## Phase 2: File Generation

> **CRITICAL — Template Fidelity:** Reproduce every CI pipeline template verbatim. Substitute only the `{{PLACEHOLDER}}` tokens. Do **not** remove, merge, rename, or omit any stages, jobs, or comment blocks. The complete job set in each template is the minimum viable pipeline; dropping any job will break SDD checks, project-tag validation, or coverage gates. For demo projects, dial down strictness through placeholder values (e.g., set `{{COVERAGE_THRESHOLD}}` to `0`, `{{SECURITY_SCAN_CMD}}` to `echo "skipped"`) — never by removing jobs.

After gathering information, generate files. Use the templates in `assets/templates/` as starting points and fill in the placeholders.

> **Path resolution — read this before running any script:**
> - `<skill_dir>` = the directory that contains this SKILL.md file (e.g. `.agents/skills/project-initializer`). All script paths below are relative to `<skill_dir>`.
> - `<project_root>` = the root of the project being initialized — pass `.` if you are already inside it, or the absolute path if not. **Never pass a path outside the project the user is working on.**

**File locations:**
- `README.md` — project root
- `AGENTS.md` — project root
- `.gitlab-ci.yml` — project root (if GitLab CI selected)
- `.github/workflows/ci.yml` — project root (if GitHub Actions selected)

**Placeholder convention** used in templates: `{{VARIABLE_NAME}}`

After creating all files, do a consistency pass:
- The tech stack in README.md must match AGENTS.md and the CI environment images
- Quality gates in CI files must reflect what's specified in AGENTS.md
- The SDD check script path must match the framework chosen
- Both CI files (if both selected) must use the same quality thresholds, check scripts, and branch names

### README.md

Read `assets/templates/README.template.md`. Fill in:
- `{{PROJECT_NAME}}` — project name
- `{{PROJECT_DESCRIPTION}}` — one-paragraph description
- `{{TECH_STACK_LIST}}` — bulleted list of stack components
- `{{SDD_FRAMEWORK}}` — name of chosen SDD framework
- `{{SDD_DOCS_PATH}}` — where SDD documents live (see framework reference)
- `{{GETTING_STARTED_STEPS}}` — installation and run steps appropriate for the tech stack

**Language**: Generate this file in the language chosen in Phase 1 (default: Chinese/中文).

### AGENTS.md

Read `assets/templates/AGENTS.template.md`. Fill in:
- `{{PROJECT_NAME}}` — project name
- `{{PROJECT_DESCRIPTION}}` — concise single-sentence summary
- `{{TECH_STACK_DETAILS}}` — structured tech stack list with versions if known
- `{{SDD_FRAMEWORK}}` — framework display name (e.g., "OpenSpec")
- `{{SDD_FRAMEWORK_ID}}` — framework lowercase id: `openspec`, `speckit`, or `gsd`
- `{{SDD_WORKFLOW_SUMMARY}}` — 3-5 bullet points describing the team's SDD workflow from the reference doc
- `{{QUALITY_LEVEL}}` — "demo" or "production" (display)
- `{{QUALITY_LEVEL_ID}}` — "demo" or "production" (machine-readable, same as display)
- `{{CI_PLATFORMS_ID}}` — `gitlab`, `github`, or `gitlab,github` (no spaces)
- `{{COVERAGE_THRESHOLD}}` — number (e.g., "80") or "N/A" for demo
- `{{LINT_TOOL}}` — linter/formatter names (from coding standards or tech stack defaults)
- `{{SECURITY_TOOLS}}` — security scan tools or "N/A"
- `{{IGNORE_TAG_DOCS}}` — the git commit ignore tag reference for the chosen framework (see reference docs)
- `{{CODING_STANDARDS_SUMMARY}}` — see Coding Standards Composition section above
- `{{INITIALIZED_DATE}}` — today's date in `YYYY-MM-DD` format
- `{{MAIN_BRANCH}}` — release branch name

**Language**: Generate this file in the language chosen in Phase 1 (default: Chinese/中文).

**Important**: AGENTS.md is a living document. Keep it minimal at creation time. Agents should append to it during development but never remove existing entries. The initial version is just the skeleton — it will grow.

### Coding Standards Composition

If the user provided coding standards:

1. Read the content (from the pasted text or the file path).
2. Extract the key rules relevant to: naming conventions, file structure, formatting, forbidden patterns, and required patterns.
3. Summarize them into the `## Coding Standards` section of AGENTS.md (concise bullet-point form — the full doc lives separately).
4. If the standards specify a linter/formatter config, reference it in the `{{LINT_CMD}}` for CI (e.g., `eslint --config .eslintrc.json`, `ruff check --config pyproject.toml`).
5. If the user provided a file path, also add a reference to that file in AGENTS.md so agents know where the canonical source is.

If no standards were provided, write a minimal placeholder in the Coding Standards section appropriate for the tech stack (e.g., "Follow PEP 8" for Python, "Follow Airbnb JavaScript Style Guide" for JS).

### 按项目类型生成（Flask 后端 / React 前端 / Taro 小程序）

以下流程**内置于本技能**，不调用、不引用任何独立 init-* 技能。

---

#### 当项目类型 = Flask 后端

在生成 README、AGENTS、CI 等通用文件之后，在 `<project_root>` 下按本技能 `references/flask-backend.md` 与 `assets/flask-backend/` 生成完整 Flask API 骨架。

1. **目录结构**  
   按 `assets/flask-backend/project-structure.txt` 创建目录树：`app/`（含 `__init__.py`、`config.py`、`extensions.py`）、`app/routes/`（`main_api.py` 及至少一个业务模块如 `user_api.py`）、`app/models/`、`app/service/`、`app/schemas/`、`app/utils/`（含 `api_util.py`）、可选 `app/permission/`、`tests/`（含 `conftest.py`）、`scripts/`、`docs/` 或 `context/`，根目录 `.env.example`、`pyproject.toml`。

2. **核心文件要点**  
   - **app/__init__.py**：`create_app(config_name)` 应用工厂；初始化扩展、加载配置、注册 Blueprint（可调用 `register_all_blueprints(app)`）；注册 `before_request`/`after_request`/`teardown_request`/`teardown_appcontext` 及全局 `errorhandler`。可参考 `assets/flask-backend/create_app_snippet.py`。  
   - **app/config.py**：按环境（development/test/production）加载配置，敏感项从环境变量读取。  
   - **app/extensions.py**：集中定义 Flask-SQLAlchemy、Redis、JWT、Casbin 等扩展实例（在 create_app 中 init_app）。  
   - **app/utils/api_util.py**：统一响应格式（如 `AppResponse`、`{code, message, data}`）、自定义 Api、统一异常处理。  
   - **app/routes/main_api.py**：健康检查等通用接口；Blueprint 命名与 `*_api.py` 约定一致，导出 `*_app`（如 `main_app`）供自动注册。  
   - **业务路由**：至少一个示例模块（如 `user_api.py`），Blueprint + Api，Resource 仅做「解析参数 → 调 Service → 返回 AppResponse/字典」。  
   - **register_all_blueprints**：扫描 `app/routes` 下 `*_api.py`，导出变量名为文件名去 `_api` 加 `_app`，实现见 `create_app_snippet.py`。

3. **依赖与配置**  
   - 使用 **uv**：以 `pyproject.toml` + `uv.lock` 为准；参考 `assets/flask-backend/pyproject-uv.example.toml` 填写依赖（flask、flask-restful、flask-sqlalchemy、python-dotenv、pytest 等）。  
   - `.env.example` 参考 `assets/flask-backend/env-example.txt`。  
   - README 中可纳入或引用「用户如何使用 uv」：见 `assets/flask-backend/uv-usage.md`。

4. **交付物**  
   完整目录与占位 `__init__.py`；`app/__init__.py`（create_app + register_all_blueprints + 钩子）；`app/config.py`、`app/extensions.py`；`app/utils/api_util.py`；`app/routes/main_api.py` 及至少一个业务模块示例；占位或示例的 `app/models/`、`app/service/`、`app/schemas/`；`.env.example`、`pyproject.toml`；`tests/conftest.py` 及至少一个 API 测试示例。可选：`scripts/validate_flask_structure.py` 可从本技能复制为 `scripts/validate_flask_structure.py` 供用户校验结构。

5. **与通用 Phase 2 的衔接**  
   若选择了 CI，`.gitlab-ci.yml` / GitHub Actions 中的 `{{DOCKER_IMAGE}}`、`{{INSTALL_CMD}}` 等按 Python/Flask 填写（如 `uv sync`、`uv run pytest`）。README 的 `{{GETTING_STARTED_STEPS}}` 写入 uv 安装与 `uv sync`、`uv run flask run` 等步骤。  
   **后续开发**：在 AGENTS 或开发约定中注明「新增 API/资源时按本技能 `references/flask-backend-codegen.md` 与 `assets/flask-backend-codegen/`（路由、Service、Model、Schema、权限、测试、.env.example）」。

---

#### 当项目类型 = React 前端

在生成通用文件之后，在 `<project_root>` 下生成 React 前端骨架；**不**调用外部 init-react-frontend 技能。

1. **脚手架**  
   使用官方 Vite 创建项目：在目标目录执行 `npm create vite@latest <project-name> -- --template react-ts`（或当前 create-vite 支持时选择 Rolldown、React、TypeScript）。若未提供 Rolldown 选项，则在生成 `package.json` 时在 devDependencies 中设置 `"vite": "npm:rolldown-vite@<resolved-latest-version>"`，并在 Vite 配置中启用 React Compiler。

2. **默认技术栈**  
   React、React Compiler（在 Vite 中启用）、TypeScript、Ant Design、react-router-dom、Zustand、Vitest + jsdom、Tailwind CSS、Axios、Vite（Rolldown）。依赖版本在生成时解析为当时最新稳定版，并写入 `package.json` 精确版本（不用 `^`/`~`）。

3. **目录结构**  
   在 `src/` 下创建：`src/utils/`、`src/consts/`、`src/route/`（路由配置，与 consts 分离）、`src/components/`、`src/pages/`、`src/store/`、`src/api/` 或 `src/services/`；以及 `test/` 或 `src/test/`（Vitest 全局 setup、fixtures、mocks）。单元测试可放在源码旁 `**/*.test.{ts,tsx}`。

4. **文件清单**  
   - `package.json`：scripts（dev、build、preview、test）；依赖为解析后的精确版本；Vite 使用 Rolldown 时 devDependencies 中 `"vite": "npm:rolldown-vite@<version>"`。  
   - `vite.config.ts`：React 插件、React Compiler、path alias（如 `@/` → `src/`）、build 输出；**dev proxy**：`server.proxy` 将 `/api` 等转发到后端，默认 target 端口 5000。  
   - `tsconfig.json` / `tsconfig.node.json`、`tailwind.config.js` + `postcss.config.js`、`index.html`（入口为 `src/main.tsx`）。  
   - `src/main.tsx`：React 根入口、Ant Design 样式、mount。  
   - `src/App.tsx`：BrowserRouter 与最小路由列表。  
   - `src/utils/`、`src/consts/`、`src/route/`、`src/components/`、`src/pages/`、`src/store/`、`src/api/` 或 `src/services/` 的占位或示例。  
   - `vitest.config.ts`：Vitest + jsdom，匹配 `**/*.test.{ts,tsx}`。  
   - 至少一个示例测试 `src/**/*.test.tsx`。  
   - `.gitignore`（Node、dist、env、IDE）。  
   - **AGENTS.md**：使用本技能模板 `assets/templates/AGENTS.react.template.md` 填充 `{{PROJECT_NAME}}`、`{{PROJECT_DESCRIPTION}}`、`{{TECH_STACK_TABLE}}`、`{{DIR_STRUCTURE}}`、`{{SCRIPTS}}`、`{{INITIALIZED_DATE}}`；语言与项目约定一致（默认中文）。

5. **与通用 Phase 2 的衔接**  
   若选择了 CI，CI 中的 `{{INSTALL_CMD}}` 为 `npm ci`，`{{TEST_CMD}}` 为 `npm run test` 等。README 的 `{{GETTING_STARTED_STEPS}}` 写入 `npm install`、`npm run dev`、后端端口与 dev proxy 说明。  
   生成完成后提示用户执行 `npm install`（或所选包管理器），并可选择执行 `npm run build`、`npm run test` 做验证。  
   **后续开发**：在 AGENTS 或开发规范中注明「功能/页面/组件开发按本技能 `references/frontend-codegen.md`（复用优先、UI/业务分层、数据化路由、测试先行、函数组件）」。

---

#### 当项目类型 = Taro 小程序

在生成通用文件之后，在 `<project_root>` 下按 Taro 官方方式初始化并做**仅允许**的后续操作；**不**调用外部 init-taro-miniapp 技能。

1. **初始化（必须）**  
   在项目所在父目录执行：`npx @tarojs/cli init <projectName>`。仅用此命令创建项目；交互中可选择框架（React/Vue3）、TypeScript、CSS 预处理器、打包工具、包管理器。不得用其他脚手架替代。

2. **安装依赖（必须）**  
   进入项目根目录执行 `npm install`（若 init 时选了 pnpm/yarn 则用 `pnpm install` 或 `yarn`）。不可省略。

3. **在 src 下创建目录**  
   仅新增以下目录（缺失则创建，不修改已有文件）：`src/apis`（API 封装）、`src/utils`、`src/components`、`src/consts`；可选 `src/hooks`、`src/services`。目录可为空，不强制添加文件。

4. **配置 H5 开发代理**  
   仅修改项目配置中的 H5 dev proxy，使前端能请求后端。配置文件一般为 `config/index.js` 或 `config/dev.js`。在 **h5** → **devServer** 下增加或合并 **proxy**，例如将 `/api` 转发到后端（默认端口 5000）：
   ```javascript
   h5: { devServer: { proxy: { '/api': { target: 'http://localhost:5000', changeOrigin: true, pathRewrite: { '^/api': '/api' } } } } }
   ```
   后端端口非 5000 时修改 `target`；除 proxy 外不修改配置其他项。

5. **README 与 AGENTS.md**  
   使用本技能模板 `assets/templates/AGENTS.taro.template.md` 在项目根目录生成或覆盖 `AGENTS.md`，填充 `{{PROJECT_NAME}}`、`{{PROJECT_DESCRIPTION}}`、`{{TECH_STACK_TABLE}}`、`{{DIR_STRUCTURE}}`（含 src/apis、utils、components、consts 及 config/、dist/）、`{{SCRIPTS}}`、`{{INITIALIZED_DATE}}`。可酌情新增或更新 README（项目名、运行方式、代理/端口说明），保持简洁。

6. **禁止**  
   不修改 `package.json`、依赖或脚本（仅允许执行上述 install）；不修改已有源码、应用入口或其他配置（如 `app.config.ts`、`babel.config.js`），仅允许上述 proxy 配置块。

---

### .gitlab-ci.yml

Read `assets/templates/gitlab-ci.template.yml`. Fill in:
- `{{DOCKER_IMAGE}}` — appropriate base image for the tech stack
- `{{INSTALL_CMD}}` — dependency install command (e.g., `npm ci`, `pip install -r requirements.txt`)
- `{{LINT_CMD}}` — lint/format check command
- `{{TEST_CMD}}` — test run command
- `{{COVERAGE_CMD}}` — coverage report command
- `{{COVERAGE_THRESHOLD}}` — minimum coverage (skip/set to 0 for demo)
- `{{SECURITY_SCAN_CMD}}` — security scan command or `echo "skipped"` for demo
- `{{SDD_CHECK_SCRIPT}}` — path to framework check script: one of:
  - `scripts/check_sdd_openspec.sh`
  - `scripts/check_sdd_speckit.sh`
  - `scripts/check_sdd_gsd.sh`
- `{{MAIN_BRANCH}}` — release branch name (default: `main`)

**当用户选择 Python + GitLab CI + backend-python-cicd 规范时**：生成或校验 `.gitlab-ci.yml`、Dockerfile、部署脚本与分支文档时，须遵循本技能 `references/backend-python-cicd.md` 与 `assets/backend-python-cicd/`。要点：先本地 Docker 构建测试再 Git 推送；私有镜像 `docker.dic.hillstonenet.com/library/python:3.12-slim` 与 pip/uv 镜像源（见 `assets/backend-python-cicd/dockerfile-python-base.md`）；多阶段构建（requirement + project）；分支 develop/bugfix/hotfix/master；dev→prod K8s 部署（dev_deploy.sh、prod_deploy.sh）；私有镜像仓库 registry.dic.hillstonenet.com；Runner tags `grunner`。可生成 Dockerfile、`scripts/dev_deploy.sh`、`scripts/prod_deploy.sh`、`k8s/dev_deployment.yaml.tpl`、`docs/GITLAB-CICD.md` 及 Git 操作说明（见 `assets/backend-python-cicd/git-operations.md`）。

Run the install script to copy all required check scripts into the project:

    python <skill_dir>/scripts/install_scripts.py <project_root> --framework <fw>

This installs the appropriate runtime variant (`.sh` on Linux/macOS, `.js` as fallback, `.ps1` on Windows) of `check_project_tag` and `check_sdd_<framework>` into `<project_root>/scripts/`. **Do not manually recreate or copy-paste script files** — the install script guarantees the exact asset versions are used without modification. Pass `--dry-run` first to verify what will be copied.

### .github/workflows/ci.yml (if GitHub Actions selected)

Read `assets/templates/github-actions.template.yml`. Fill in the same placeholders as the GitLab template — the values must be identical to ensure both pipelines enforce the same standards.

### 当用户选择 QA/测试规范（Phase 1 问题 12）

在 AGENTS.md 中增加「测试与根因分析」小节，或引用本技能 `references/qa-testing.md`：测试计划、用例格式、自动化约定、测试报告；缺陷与测试失败时采用系统性排错与根因分析（先根因、后修复，禁止只治标）。可摘录要点或写「详见项目所用 project-initializer 技能之 references/qa-testing.md」。

### 当用户选择多角色/子代理（Phase 1 问题 13）

在 Phase 2 生成与 Phase 3 SDD 之后，按本技能 `references/agent-roles.md` 与 `assets/agent-roles/` 执行：(1) 确认场景与约束（系统开发、数据分析、运维等；串行/并行；规模与规定）；(2) 规划角色清单（从 `references/agent-roles.md` 常见场景与角色映射选取并裁剪）；(3) 为每个角色填规范（使用 `assets/agent-roles/role-template.json` 结构，产出 `roles/<role-id>.md` 或 `roles/<role-id>.json`）；(4) 若用户要求创建子代理，从角色定义生成 `.cursor/agents/<name>.md`（YAML frontmatter：name、description、model 等；正文：scope、inputExpectation、constraints、outputSpec、handoff），格式参考 `assets/agent-roles/subagent-cursor-template.md`。子代理目录默认项目级 `.cursor/agents/`。可选：将 `scripts/validate_roles.py` 复制到项目中用于校验角色 JSON。

---

## Phase 3: SDD Framework Installation

> **MANDATORY — do not skip or substitute manually.**
> You MUST run the script below. Do NOT create SDD framework directories or documents by hand. Manually created files will be incomplete, wrongly structured, and will fail CI checks. If the script encounters an error, report it to the user — do not work around it by creating files yourself.

Resolve `<skill_dir>` (the directory containing this SKILL.md) and run:

    python <skill_dir>/scripts/initialize_sdd.py <project_root> --framework <fw> --ai-provider <agent> [--script-shell sh|ps]

If you are already inside the project directory, `<project_root>` is `.`.

**Determining the `--ai-provider` value:** Use the name of the AI agent currently running this skill (e.g. `claude`, `copilot`, `gemini`, `opencode`, `codex`). You know this from your own identity — pass it as-is.

**For SpecKit only — `--script-shell` parameter:** Choose the shell for generated scripts:
- `sh` (default): Unix/shell scripts — use for Linux/macOS CI runners
- `ps`: PowerShell scripts — use for Windows CI runners

This script runs all frameworks **non-interactively**:
- **OpenSpec**: `openspec init --tools <tool_id>` — `--ai-provider` mapped to OpenSpec's tool ID: `claude`, `opencode`, `codex`, `gemini`, `windsurf`, `qwen`, `codebuddy`, `kilocode` use the same name; `copilot`→`github-copilot`; `cursor-agent`→`cursor`; `roo`→`roocode`; all others→`all`
- **SpecKit**: `specify init . --ai <provider> --here --force --script <shell>` — passes the provider name and shell choice directly
- **GSD**: `npx -y get-shit-done-cc@latest --<runtime> --local` — `--ai-provider` is mapped to a runtime flag: `claude`→`--claude`, `opencode`→`--opencode`, `codex`→`--codex`, all others→`--claude`

The script also:
- Installs the framework CLI tool (`npm`, `uv`, or `npx` as appropriate) if not found
- Initializes framework-specific directories
- For **OpenSpec**: initializes `openspec/specs/` and `openspec/changes/`
- For **SpecKit**: initializes `specs/` (auto-numbered) and `memory/constitution.md`
- For **GSD**: initializes `.planning/` with PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, config.json

SpecKit `--ai-provider` supported values: claude, gemini, copilot, cursor-agent, windsurf, opencode, codex, qwen, amp, shai, agy, bob, qodercli, roo, codebuddy, jules, kilocode, generic.

Pass `--dry-run` to preview without installing.

### Prerequisites

| Framework | Requires |
|-----------|----------|
| OpenSpec | `npm` (Node.js) |
| SpecKit | `uv` (Python tool installer) + `git` |
| GSD | `npx` + Node.js ≥18 |

If a required tool is not installed, the script will exit with an error message indicating what needs to be installed.

---

## Phase 4: SDD Check Script

The check script reads the latest git commit message and the project's SDD documents. It enforces documentation consistency.

### Ignore Tag System

Agents and developers can place structured tags in commit messages to suppress specific checks:

```
feat: implement user login [ignore:spec_sync]
fix: typo in variable name [ignore:all_sdd]
```

**Universal tags (all frameworks):**

| Tag | What it suppresses |
|-----|-------------------|
| `[ignore:all_sdd]` | All SDD process checks |

**Framework-specific tags** — see the relevant reference file for the complete list. They follow the pattern `[ignore:<check_name>]`.

### When checks fail

The script exits non-zero and prints a message explaining:
1. What was found (e.g., "3 tasks incomplete in openspec/changes/add-auth/tasks.md")
2. What the developer should do (e.g., `Run /opsx:sync add-auth to sync delta specs`)
3. How to suppress the check if appropriate (e.g., `Add [ignore:spec_sync] to commit message if this is a bug fix not tied to a feature`)

---

## Phase 5: Project Identity Tag

Every project initialized by this skill must have a machine-readable identity tag embedded at the top of `AGENTS.md`. This tag allows server-side CI to:
- Confirm the project was properly initialized (not just a hand-crafted AGENTS.md)
- Know which SDD framework and CI platforms are in use
- Enforce version-specific checks appropriate for the project's configuration

The tag takes the form of a structured HTML comment block (the first thing in the file, before any Markdown):

```
<!-- @project-initializer
version: 1
initialized_at: YYYY-MM-DD
sdd_framework: openspec|speckit|gsd
quality_level: demo|production
ci_platforms: gitlab|github|gitlab,github
project_initializer_version: 1.0.0
-->
```

Rules:
- Always place it as the very first content in `AGENTS.md` (before the `#` heading)
- Use the actual initialization date (today)
- `sdd_framework` — lowercase identifier: `openspec`, `speckit`, or `gsd`
- `ci_platforms` — comma-separated, no spaces: `gitlab`, `github`, or `gitlab,github`
- Do not modify this block after creation except through a deliberate re-initialization

The CI check script (`assets/scripts/check_project_tag.sh`) reads this tag and exits non-zero if it is missing or malformed. It is installed automatically by the `install_scripts.py` step described in Phase 2 — `check_project_tag` is always included regardless of the chosen SDD framework. The framework's initialize script (Phase 3) must complete successfully before this tag is validated.

---

## Phase 6: Consistency Verification

After generating all files, perform this checklist:

- [ ] `AGENTS.md` starts with a valid `<!-- @project-initializer` tag
- [ ] `sdd_framework` in tag matches chosen framework
- [ ] `ci_platforms` in tag matches files actually generated
- [ ] Docker/runner image in CI file(s) matches tech stack
- [ ] `AGENTS.md` tech stack section matches `README.md`
- [ ] Coverage threshold in CI file(s) matches `AGENTS.md` → Quality Standards
- [ ] SDD framework name consistent across all generated files
- [ ] The correct SDD check script is referenced (OpenSpec/SpecKit/GSD)
- [ ] Both CI platform files (if both generated) use identical quality thresholds
- [ ] Branch name in CI rules matches the stated main branch
- [ ] SDD framework initialized successfully (Phase 3)
  - OpenSpec: `openspec/specs/` and `openspec/changes/` exist
  - SpecKit: `specs/` and `memory/constitution.md` exist
  - GSD: `.planning/` contains PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md, config.json
- [ ] `scripts/` directory was populated by running `install_scripts.py` (not manually recreated or copy-pasted)
- [ ] The correct single variant (`.sh` on Linux/macOS, `.ps1` on Windows, `.js` as fallback) is present in `scripts/`
- [ ] `.gitlab-ci.yml` (if generated) contains **all** required jobs: `lint`, `unit-tests`, `commit-format`, `full-test-suite`, `coverage-gate`, `security-scan`, `project-tag-check`, `sdd-process-check`, `deploy`
- [ ] `.github/workflows/ci.yml` (if generated) contains **all** required jobs: `lint`, `unit-tests`, `commit-format`, `full-test-suite`, `security-scan`, `project-tag-check`, `sdd-process-check`
- [ ] No jobs were removed or merged compared to the template; only `{{PLACEHOLDER}}` tokens were substituted
- [ ] `AGENTS.md` starts with a valid `<!-- @project-initializer` tag
- [ ] First commit includes: README.md, AGENTS.md, CI files, scripts/, and framework directories

Report any inconsistencies to the user before finishing.

---

## Reference files

- `references/openspec.md` — OpenSpec document structure, sync workflow, ignore tags
- `references/speckit.md` — SpecKit spec lifecycle, constitution, phase gates, ignore tags
- `references/gsd.md` — GSD phase workflow, document set, planning structure, ignore tags
- `references/flask-backend.md` — Flask 后端目录结构、分层、Blueprint、UV、钩子（项目类型 = Flask 后端时使用）
- `references/backend-python-cicd.md` — Python + GitLab CI：多阶段 Docker、分支、K8s、私有镜像（用户选择该规范时使用）
- `references/frontend-codegen.md` — React 功能/页面/组件开发：复用优先、UI/业务分层、数据化路由、测试先行（React 项目后续开发）
- `references/flask-backend-codegen.md` — Flask 新增 API/资源：路由、Service、Model、Schema、权限、测试（Flask 项目后续开发）
- `references/qa-testing.md` — 测试计划、用例、自动化、报告与系统性根因分析（用户选择引用 QA 时使用）
- `references/agent-roles.md` — 多角色规划与 Cursor 子代理（.cursor/agents/*.md）（用户选择多角色/子代理时使用）

## Installation scripts

All script paths are relative to `<skill_dir>` (the directory containing this SKILL.md). `<project_root>` is the project's root — use `.` if already inside it.

- `scripts/install_scripts.py` — copies check scripts into `<project_root>/scripts/`

  Usage: `python <skill_dir>/scripts/install_scripts.py <project_root> --framework <openspec|speckit|gsd>`

  Always run this instead of manually copying scripts. Add `--dry-run` to preview.

- `scripts/initialize_sdd.py` — installs SDD framework tools and initializes project structure

  Usage: `python <skill_dir>/scripts/initialize_sdd.py <project_root> --framework <openspec|speckit|gsd> --ai-provider <agent>`

  **Must be run — do not manually create SDD directories.** Installs the framework CLI non-interactively, sets up directories. Add `--dry-run` to preview.

## Template files

- `assets/templates/README.template.md`
- `assets/templates/AGENTS.template.md` — 通用项目；项目类型 = React 前端时改用 `assets/templates/AGENTS.react.template.md`
- `assets/templates/AGENTS.react.template.md` — React 前端项目 AGENTS 模板
- `assets/templates/AGENTS.taro.template.md` — Taro 小程序项目 AGENTS 模板
- `assets/templates/gitlab-ci.template.yml`
- `assets/templates/github-actions.template.yml`
- Flask 后端：`assets/flask-backend/`（project-structure.txt、create_app_snippet.py、env-example.txt、pyproject-uv.example.toml、uv-usage.md）
- Python GitLab CI/K8s：`assets/backend-python-cicd/`（dockerfile-python-base.md、docker-build-commands.md、git-operations.md、k8s/、scripts/、gitlab-ci-example.yml、pipeline-overview.md）
- Flask 代码生成：`assets/flask-backend-codegen/`（response-format.json、code-snippets.md）；可选 `scripts/check_route_layer.py`
- 角色与子代理：`assets/agent-roles/`（role-template.json、scenario-roles-example.json、subagent-cursor-template.md、config-template.json）；可选 `scripts/validate_roles.py`

## Check scripts

Each check is available in three runtime variants, stored in the skill's `assets/scripts/` directory. The install_scripts.py command copies these into the target project's `scripts/` directory — which variant gets invoked in CI depends on the runner OS and what's available.

| Script | Shell (Linux/macOS) | PowerShell (Windows/cross-platform) | Node.js (any platform) |
|--------|--------------------|------------------------------------|------------------------|
| Project tag | `check_project_tag.sh` | `check_project_tag.ps1` | `check_project_tag.js` |
| OpenSpec | `check_sdd_openspec.sh` | `check_sdd_openspec.ps1` | `check_sdd_openspec.js` |
| SpecKit | `check_sdd_speckit.sh` | `check_sdd_speckit.ps1` | `check_sdd_speckit.js` |
| GSD | `check_sdd_gsd.sh` | `check_sdd_gsd.ps1` | `check_sdd_gsd.js` |

### Selecting which variant to use in CI

When generating CI pipeline files, choose the invocation command based on the project's runner environment:

| Runner environment | CI invocation |
|--------------------|--------------|
| Linux / macOS (bash available) | `bash scripts/check_sdd_<fw>.sh` |
| Windows (PowerShell 7+ available) | `pwsh scripts/check_sdd_<fw>.ps1` |
| Any (Node.js ≥ 18 available) | `node scripts/check_sdd_<fw>.js` |
| Unknown / mixed | Use Node.js — it works everywhere Node.js is installed |

The Node.js variants are the most portable choice if the runner environment is uncertain. They require no npm dependencies — only the Node.js built-in modules (`fs`, `path`, `child_process`).

The GitLab CI and GitHub Actions templates default to the shell variant. If the user's CI runners are Windows-based or they prefer Node.js, update the `script:` / `run:` lines accordingly. All three variants implement identical logic and exit codes.
````
