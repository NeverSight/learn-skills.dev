---
name: python-project
description: 使用 uv 工具管理 Python 项目的依赖、环境和工作流。适用于项目初始化、依赖管理、环境配置和 CI/CD 设置场景。
---

> 代码编写规范参见 [python-coding](../python-coding/SKILL.md) skill。

### 项目初始化
创建新项目：
```bash
uv init myproject --package  # 创建库/包项目
uv init myapp               # 创建应用项目
```

标准项目结构：
```
myproject/
├── pyproject.toml    # 依赖声明的唯一真相源
├── uv.lock          # 锁定文件（必须提交到 git）
├── .python-version  # 固定 Python 版本（可选）
├── src/myproject/   # 源代码
├── tests/           # 测试代码
└── README.md
```

### 依赖管理
添加依赖：
```bash
uv add requests              # 添加生产依赖
uv add --dev pytest ruff     # 添加开发依赖
uv add "fastapi>=0.100"      # 指定版本约束
```

同步与锁定：
```bash
uv lock           # 更新 uv.lock
uv sync           # 同步环境（安装所有依赖）
uv sync --frozen  # CI 中使用：使用现有锁定，不更新
```

移除依赖：
```bash
uv remove requests
```

### Python 版本管理
```bash
uv python install 3.12    # 安装 Python 3.12
uv python pin 3.12        # 固定项目使用 3.12
```

### 虚拟环境
```bash
uv venv    # 创建 .venv
uv sync    # 自动创建并同步环境
```

不要手动激活 - 使用 `uv run` 代替。

### 运行代码
```bash
uv run python script.py         # 自动同步后运行
uv run pytest                   # 运行测试
uv run --no-sync python app.py  # 跳过同步
```

在 pyproject.toml 中定义脚本：
```toml
[project.scripts]
myapp = "myproject.main:cli"

[tool.uv.scripts]
dev = "uvicorn myapp:app --reload"
test = "pytest tests/"
lint = "ruff check ."
```

使用方式：`uv run dev`、`uv run test`、`uv run lint`

### 标准工作流
开发流程：
```bash
# 1. 克隆项目
git clone <repo> && cd myproject

# 2. 同步环境
uv sync

# 3. 开发
uv run python -m myproject

# 4. 添加依赖
uv add newpackage
git add pyproject.toml uv.lock
git commit -m "Add newpackage"
```

CI/CD 模板：
```yaml
# .github/workflows/test.yml
- uses: astral-sh/setup-uv@v1
- run: uv sync --frozen
- run: uv run pytest
```

### 核心规则
1. 单一真相源: `pyproject.toml` 是唯一的依赖声明处
2. 始终提交锁定文件: `uv.lock` 确保可重现性
3. 使用 uv run: 通过 `uv run` 执行所有命令以自动管理环境
4. 固定 Python 版本: 使用 `.python-version` 或 `requires-python`
5. 分离开发依赖: 使用 `--dev` 标志或 `tool.uv.dev-dependencies`

### 常见操作
更新依赖：
```bash
uv lock --upgrade-package requests  # 更新单个包
uv lock --upgrade                   # 更新所有包
```

导出兼容格式：
```bash
uv pip compile pyproject.toml -o requirements.txt
```

安装可选依赖组：
```bash
uv sync --extra dev
```

### 禁止操作
- ❌ 禁止手动编辑 `uv.lock`
- ❌ 禁止在 uv 项目中使用 `pip install`
- ❌ 禁止提交 `.venv/` 目录
- ❌ 禁止在 `pyproject.toml` 外声明依赖
- ❌ 禁止使用 `requirements.txt` 作为主要依赖源

### 决策框架
当被要求：
- 创建项目 → 使用 `uv init`
- 添加依赖 → 使用 `uv add`
- 运行代码 → 使用 `uv run`
- 更新依赖 → 使用 `uv lock --upgrade`
- 配置 CI → 使用 `uv sync --frozen`

始终优先使用 uv 命令而非传统的 pip/virtualenv 工作流。