---
name: python-env
description: Python environment management with venv, Poetry, Pipenv, pyenv, and conda. Use when user asks to "create virtual environment", "set up Poetry", "manage Python versions", "fix pip issues", "install dependencies", "create requirements.txt", or any Python environment tasks.
---

# Python Environment Management

Virtual environments, dependency management, and Python version control.

## venv (Built-in)

```bash
# Create virtual environment
python -m venv .venv
python3 -m venv .venv

# Activate
source .venv/bin/activate          # Linux/macOS
.venv\Scripts\activate             # Windows

# Deactivate
deactivate

# Install packages
pip install requests flask
pip install -r requirements.txt

# Freeze dependencies
pip freeze > requirements.txt

# Upgrade pip
pip install --upgrade pip
```

### requirements.txt

```
# Pinned versions (production)
flask==3.0.0
requests==2.31.0
sqlalchemy==2.0.23

# Ranges (library development)
flask>=3.0,<4.0
requests~=2.31            # Compatible release (>=2.31, <3.0)

# With extras
fastapi[all]==0.104.0

# From git
git+https://github.com/user/repo.git@main#egg=package
```

```bash
# Separate dev dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Poetry

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Create new project
poetry new my-project
poetry init  # In existing project

# Add dependencies
poetry add requests flask
poetry add pytest --group dev
poetry add "sqlalchemy>=2.0,<3.0"

# Remove dependency
poetry remove requests

# Install all dependencies
poetry install
poetry install --without dev

# Update dependencies
poetry update
poetry update requests      # Single package

# Show dependencies
poetry show
poetry show --tree

# Run command in virtualenv
poetry run python main.py
poetry run pytest

# Activate shell
poetry shell

# Build & publish
poetry build
poetry publish

# Export to requirements.txt
poetry export -f requirements.txt --output requirements.txt
poetry export -f requirements.txt --without-hashes
```

### pyproject.toml (Poetry)

```toml
[tool.poetry]
name = "my-project"
version = "1.0.0"
description = "My project"
authors = ["Name <email@example.com>"]
python = "^3.11"

[tool.poetry.dependencies]
python = "^3.11"
flask = "^3.0"
sqlalchemy = "^2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
ruff = "^0.1"
mypy = "^1.7"

[tool.poetry.scripts]
serve = "my_project.main:app"
```

## uv (Fast Python Package Manager)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Install packages (10-100x faster than pip)
uv pip install requests flask
uv pip install -r requirements.txt

# Sync from lock file
uv pip sync requirements.txt

# Compile requirements (resolve + lock)
uv pip compile requirements.in -o requirements.txt

# Create project
uv init my-project

# Add dependency
uv add requests
uv add pytest --dev

# Run
uv run python main.py
```

## pyenv (Python Version Management)

```bash
# Install pyenv
curl https://pyenv.run | bash

# List available versions
pyenv install --list | grep "3\."

# Install Python version
pyenv install 3.12.1
pyenv install 3.11.7

# Set global default
pyenv global 3.12.1

# Set local version (per directory)
pyenv local 3.11.7    # Creates .python-version

# List installed
pyenv versions

# Uninstall
pyenv uninstall 3.10.0
```

## Pipenv

```bash
# Install
pip install pipenv

# Create environment + install
pipenv install
pipenv install requests
pipenv install pytest --dev

# Run in environment
pipenv run python main.py
pipenv shell

# Lock dependencies
pipenv lock

# Install from lock file
pipenv install --deploy

# Show dependency graph
pipenv graph
```

## conda

```bash
# Create environment
conda create -n myenv python=3.12
conda create -n myenv python=3.12 numpy pandas

# Activate/deactivate
conda activate myenv
conda deactivate

# Install packages
conda install numpy pandas
conda install -c conda-forge package-name

# List environments
conda env list

# Export environment
conda env export > environment.yml

# Create from file
conda env create -f environment.yml

# Remove environment
conda env remove -n myenv
```

## Common Issues

```bash
# "pip not found" after creating venv
python -m pip install --upgrade pip

# Permission errors
pip install --user package-name

# Conflicting versions
pip install --force-reinstall package==1.0

# Clear pip cache
pip cache purge

# Check what's outdated
pip list --outdated

# Verify installation
python -c "import package; print(package.__version__)"
```

## Reference

For comparison and migration guides: `references/tools.md`
