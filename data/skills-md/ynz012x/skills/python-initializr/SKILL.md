---
name: python-initializr
description: 初始化一个规范的 Python 项目，包含依赖管理、代码规范检查、测试框架、版本管理等。当用户需要创建新的 Python 项目时触发此 skill。
---

# Python 项目初始化

## 流程概述

1. 确认项目信息 - 与用户交互确认项目名称和 Python 版本
2. 初始化项目 - 使用 uv init 创建项目，启用 git 版本控制
3. 配置代码规范检查 - 使用 pre-commit 管理并初始化代码规范检查 hooks，并应用相应的规范配置
4. 配置测试框架 - 添加 pytest、pytest-cov 开发依赖
5. 配置版本管理工具 - 配置 .gitignore 优化VCS管理，配置版本元信息，配置 bumpversion 进行语义化版本管理
6. 添加常用开发工具 - 添加 ipython 用于本地调试
7. 安装并验证 - 安装所有依赖并验证配置
8. 更新README - 创建并更新README文件，添加项目使用说明
9. 完成初始提交

---

## Step 1: 确认项目信息

与用户确认以下信息：

- **项目名称 project_name**: 默认使用当前目录名称
- **项目描述 project_description**: 简短的项目描述信息，用于快速理解项目功能和定位
- **Python 版本 python_version**: 推荐使用官方支持的版本（3.10及以上）

## Step 2: 初始化项目

使用 uv 初始化项目，启用 git 版本控制：

```bash
uv init \
    # 项目名称
    --name=<project_name> \
    # 项目描述
    --description="<project_description>" \
    # 初始化 src/<project_name> 包目录
    --package \
    # 初始化 git
    --vcs=git \
    # Python 最低支持版本
    --python=<python_version>
```

## Step 3: 配置代码规范检查

添加 pre-commit 及代码格式化工具：

```bash
uv add --dev pre-commit black flake8 flake8-import-order ruff
```

将 [assets/pre-commit-config.yaml](assets/pre-commit-config.yaml) 内容写入项目根目录的 `.pre-commit-config.yaml` 文件

将 [assets/flake8.j2](assets/flake8.j2) 模板应用到项目根目录的 `.flake8` 文件，替换变量 `{{ project_name }}` 为项目名称

安装 pre-commit hooks：

```bash
uv run pre-commit install
```

## Step 4: 配置测试框架

添加 pytest 和 pytest-cov 开发依赖：

```bash
uv add --dev pytest pytest-cov
```

创建 tests 目录和初始测试文件：

```bash
mkdir -p tests
touch tests/__init__.py
```

在 `pyproject.toml` 中添加 pytest 配置：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*", "*Test"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--cov=src/<project_name>",
    "--cov-report=term-missing",
    "--tb=short",
]

[tool.coverage.run]
source = ["src/<project_name>"]
branch = true
omit = ["tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
]
```


## Step 5: 配置版本管理工具

添加 .gitignore

```bash
curl https://raw.githubusercontent.com/github/gitignore/refs/heads/main/Python.gitignore -o .gitignore
```

添加 bumpversion 依赖：

```bash
uv add --dev bumpversion
```

配置版本元信息

1) 新建 `src/<project_name>/_version.py` 文件用于保存项目版本元信息

    ```python:src/<project_name>/_version.py
    __version__ = "0.1.0"
    ```

2) 将版本信息导出到项目包命名空间，调整 `src/<project_name>/__init__.py`

    ```python:src/<project_name>/__init__.py
    """<project_name> package."""

    from ._version import __version__  # noqa: F401
    ```

3) 添加测试用例用于验证版本元信息获取

    ```python:tests/test_version.py
    from <project_name> import __version__

    def test_version():
        assert __version__
    ```

将 [assets/bumpversion.cfg.j2](assets/bumpversion.cfg.j2) 模板应用到项目根目录的 `.bumpversion.cfg` 文件，替换变量 `{{ project_name }}` 为项目名称

## Step 6: 添加常用开发工具

```bash
uv add --dev ipython
```

## Step 7: 安装并验证

安装所有依赖：

```bash
uv sync
```

验证配置：

```bash
# 验证 pytest
uv run pytest

# 验证 pre-commit
uv run pre-commit run --all-files

# 验证 bumpversion
uv run bumpversion --help

# 验证版本元信息
uv run python -c 'from <project_name> import __version__; print(__version__)'
```

## Step 8: 更新README

使用模板 [assets/README.md.j2](assets/README.md.j2) 生成项目 README 文件，替换以下变量：
- `{{ project_name }}` - 项目名称
- `{{ project_description }}` - 项目描述

将生成的内容写入项目根目录的 `README.md` 文件。

## Step 9: 完成初始提交

```bash
git add .
git commit -m "Initial project setup"
```
