---
name: python-uv-acceleration
description: 在 Python 项目中默认使用 uv 替代 pip 进行依赖管理和虚拟环境创建，提升 10-100x 安装速度。当处理 Python 项目、创建虚拟环境、安装依赖、或用户提到 pip/venv/virtualenv 时使用。
---

# Python uv 加速

使用 [uv](https://github.com/astral-sh/uv) 替代 pip/pip-tools/virtualenv，显著提升 Python 依赖安装速度。

## Instructions（分步说明）

### Step 1：检测项目类型

检查项目是否为 Python 项目：

- `requirements.txt` — 传统依赖文件
- `pyproject.toml` — 现代 Python 项目配置
- `setup.py` / `setup.cfg` — 传统打包配置
- `.py` 文件 — Python 源码

### Step 2：虚拟环境创建

**默认使用 uv 创建虚拟环境**，替代 `python -m venv`：

```bash
# ✅ 推荐：使用 uv（极速）
uv venv

# ❌ 避免：传统方式（较慢）
python -m venv venv
```

默认创建 `.venv/` 目录。如需指定名称：

```bash
uv venv venv  # 创建 venv/ 目录
```

### Step 3：依赖安装

**默认使用 uv pip 安装依赖**，替代 `pip install`：

```bash
# ✅ 推荐：使用 uv（极速，利用全局缓存）
uv pip install -r requirements.txt

# 单个包安装
uv pip install requests

# 开发模式安装
uv pip install -e .

# ❌ 避免：传统方式（较慢）
pip install -r requirements.txt
```

### Step 4：常用命令对照

| 传统命令 | uv 替代命令 | 说明 |
|---------|------------|------|
| `python -m venv venv` | `uv venv` | 创建虚拟环境 |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` | 安装依赖 |
| `pip install package` | `uv pip install package` | 安装单个包 |
| `pip install -e .` | `uv pip install -e .` | 开发模式安装 |
| `pip freeze` | `uv pip freeze` | 导出依赖 |
| `pip list` | `uv pip list` | 列出已安装包 |
| `pip uninstall package` | `uv pip uninstall package` | 卸载包 |

### Step 5：确保 .gitignore 配置

虚拟环境目录应加入 `.gitignore`：

```gitignore
# 虚拟环境（uv 默认创建 .venv/）
.venv/
venv/
env/
ENV/
```

---

## Examples（示例）

### 示例 1：新建 Python 项目

```bash
# 创建虚拟环境
uv venv
source .venv/bin/activate

# 安装依赖
uv pip install flask requests

# 导出依赖
uv pip freeze > requirements.txt
```

### 示例 2：克隆现有项目后初始化

```bash
git clone https://github.com/user/project.git
cd project

# 创建虚拟环境并安装依赖
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 示例 3：使用 pyproject.toml 的项目

```bash
uv venv
source .venv/bin/activate

# 安装项目及其依赖
uv pip install -e ".[dev]"
```

---

## Edge Cases（边界情况）

### uv 未安装

如果系统未安装 uv，先安装：

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip 安装
pip install uv
```

### 需要特定 Python 版本

uv 支持指定 Python 版本：

```bash
uv venv --python 3.11
```

### 私有包源

uv 支持自定义包源：

```bash
uv pip install --index-url https://pypi.example.com/simple/ package
```

### 与 poetry/pdm 项目兼容

uv 可以与 `pyproject.toml` 配合使用，但不替代 poetry/pdm 的完整项目管理功能。对于复杂项目，可以：

- 使用 uv 加速依赖安装部分
- 或继续使用 poetry/pdm 的完整工作流

---

## 参考资料

详细命令和高级用法见 [references/uv-commands.md](references/uv-commands.md)。
