---
name: init
description: 初始化项目 AI 开发规范，当用户需要创建项目协作准则、同步多 AI 上下文时使用。
---

## 技能定义：init

**描述：** 自动化生成项目“AI 宪法”文件，确保所有协作 AI 对项目背景、技术栈和规范达成 100% 共识。

### 执行工作流

1. **扫描 (Scan)**：自动读取根目录配置文件（`package.json`, `pyproject.toml`, `go.mod` 等）识别技术栈。
   - 扩展支持：Cargo.toml, composer.json, Makefile, Dockerfile
   - 冲突处理：多配置文件共存时按优先级识别核心技术栈
2. **建模 (Model)**：分析目录结构，确定核心业务逻辑存放路径。
3. **生成 (Generate)**：填充下方的 `AGENTS.md` 模板。
   - 自动填充：技术栈、常用命令、目录结构、更新日期
   - 提示补充：项目名称、核心目标、业务逻辑等描述性内容
   - 精简模式：小型项目自动生成 3 章节精简版模板
4. **同步 (Sync)**：创建软链接，将 `GEMINI.md` 和 `CLAUDE.md` 指向 `AGENTS.md`。
   - 冲突处理：检测到现有文件时默认备份，支持跳过/覆盖选项

---

## AGENTS.md 规范模板

```markdown
# Agents Instruction

> **AI 指令级别**：项目全局上下文与行为准则
> **交流语言**：用户交互始终使用 **简体中文**
> **更新日期**：{当前日期}

## 1. 项目概览 (Project Overview)
{*简要描述项目，帮助 AI 理解“为什么”要做这个项目。*}

- **项目名称**：[输入项目名称]
- **核心目标**：[例如：基于 FastAPI 的分布式任务调度系统，解决高并发下的延迟问题。]
- **业务逻辑**：[简述核心链路，例如：用户提交任务 -> 消息队列 -> 节点竞争执行]

## 2. 技术选型 (Tech Stack)
{*明确工具链，防止 AI 生成不兼容的代码。*}

- **语言/环境**：[例如：Python 3.11, Bun v1.0]
- **框架/库**：[例如：Tailwind CSS, Prisma, Pydantic v2]
- **存储/基础设施**：[例如：Redis, PostgreSQL, Docker]

## 3. 常用命令 (Common Commands)
{*AI 辅助开发时可直接调用的指令。*}

| 任务 | 命令 |
| :--- | :--- |
| **安装依赖** | `npm install` 或 `uv sync` |
| **启动开发环境** | `npm run dev` 或 `python main.py` |
| **执行测试** | `pytest` 或 `npm test` |
| **构建发布** | `npm run build` |

## 4. 项目架构 (Architecture)
{*指导 AI 理解文件摆放逻辑。*}

- `src/`：源代码根目录
- `src/core/`：核心算法与配置
- `src/api/`：接口层规范
- **禁止项**：严禁在 `dist/` 或 `build/` 目录下进行任何手动代码修改。

## 5. 编码规范与约束 (Constraints)
{*AI 必须遵守的“硬红线”。*}

- **规范**：遵循 [例如：Google Python Style Guide / Standard JS]。
- **安全**：禁止在代码中包含硬编码的密钥，使用 `.env`。
- **注释**：所有 Public 接口必须包含中文 JSDoc/Docstring 描述。

## 6. AI 交互规范（可选）
- 输出语言：与用户交流默认使用简体中文，代码注释使用英文
- 代码风格：遵循项目 eslint/ruff/prettier 配置
- 输出格式：优先使用代码块展示可执行内容，关键步骤添加简要说明
```

### 如何完成“软链接”操作？

```bash
# 在 Linux/macOS 环境下
ln -s AGENTS.md GEMINI.md
ln -s AGENTS.md CLAUDE.md

# 在 Windows (PowerShell 管理员模式)
New-Item -ItemType SymbolicLink -Path "GEMINI.md" -Target "AGENTS.md"
New-Item -ItemType SymbolicLink -Path "CLAUDE.md" -Target "AGENTS.md"
```
