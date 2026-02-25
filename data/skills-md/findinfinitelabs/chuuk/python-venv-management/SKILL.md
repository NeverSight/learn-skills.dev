---
name: python-venv-management
description: Automatically manage Python virtual environments (.venv) in terminal commands. Always activate .venv before running Python/pip commands. Supports macOS, Linux, and Windows with shell-aware activation. Use when executing Python scripts, installing packages, or running development servers. Critical for consistent environment management.
---

# Python Virtual Environment Management

## Core Principle

**ALWAYS use the project's .venv when running Python commands in the terminal.**
**NEVER run Python commands without first activating or using the virtual environment.**

## Critical Rules

1. **Check for .venv first** - Always verify .venv exists before running Python commands
2. **Use activation commands** - Activate .venv in every terminal session
3. **Shell-aware** - Detect shell type (Bash, Zsh, PowerShell) and use appropriate commands
4. **No global Python** - Never use system Python when .venv exists
5. **Fail fast** - If .venv doesn't exist, create it or fail clearly
6. **macOS default** - Prefer Bash/Zsh patterns on macOS

## Shell Detection & Commands

### macOS Terminal (Zsh - Default)

```zsh
# Activate .venv
source .venv/bin/activate

# Run Python commands
python app.py
pip install -r requirements.txt

# Check if activated
echo $VIRTUAL_ENV                 # Should show .venv path

# Direct execution (no activation needed)
.venv/bin/python app.py
.venv/bin/pip install package
```

### macOS PowerShell

```powershell
# Activate .venv
./.venv/bin/Activate.ps1

# Run Python commands
python -m <module>
pip install <package>

# Check if activated
$env:VIRTUAL_ENV                  # Should show .venv path
```

### Linux Bash

```bash
# Activate .venv
source .venv/bin/activate

# Run Python commands
python app.py
pip install -r requirements.txt

# Check if activated
echo $VIRTUAL_ENV                 # Should show .venv path
```

### Windows PowerShell

```powershell
# Activate .venv
.\.venv\Scripts\Activate.ps1

# Run Python commands
python -m <module>
pip install <package>

# Check if activated
$env:VIRTUAL_ENV                  # Should show .venv path
```

### Windows Command Prompt

```cmd
# Activate .venv
.venv\Scripts\activate.bat

# Run Python commands
python app.py
pip install -r requirements.txt
```

### Command Patterns

#### Pattern 1: Direct Execution (PREFERRED - No activation needed)

```bash
# macOS/Linux - Most reliable method
.venv/bin/python app.py
.venv/bin/python -m flask run
.venv/bin/pip install package
```

```powershell
# PowerShell
./.venv/bin/python app.py
./.venv/bin/python -m flask run
```

#### Pattern 2: Activation + Command (macOS Zsh)

```zsh
source .venv/bin/activate && python app.py
```

#### Pattern 3: Activation + Command (PowerShell)

```powershell
./.venv/bin/Activate.ps1 ; python app.py
```

## OS-Specific Paths

| OS | Activation Script | Python Executable |
|----|------------------|-------------------|
| macOS (Zsh) | `.venv/bin/activate` | `.venv/bin/python` |
| macOS (PowerShell) | `.venv/bin/Activate.ps1` | `.venv/bin/python` |
| Linux (Bash) | `.venv/bin/activate` | `.venv/bin/python` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` | `.venv\Scripts\python.exe` |
| Windows (CMD) | `.venv\Scripts\activate.bat` | `.venv\Scripts\python.exe` |

## Implementation Checklist

Before running ANY Python command, verify:

- [ ] Is this a Python project? (Check for .venv, requirements.txt, *.py files)
- [ ] Does .venv exist? (Check for .venv directory)
- [ ] What shell am I using? (PowerShell vs Bash/Zsh)
- [ ] Am I using the correct activation syntax?
- [ ] Can I use direct .venv/bin/python instead of activating?

## Standard Workflows

### Workflow 1: Running Python Scripts

**PowerShell:**

```powershell
# Method 1: Activate then run
./.venv/bin/Activate.ps1 ; python app.py

# Method 2: Direct execution (PREFERRED)
./.venv/bin/python app.py
```

**Bash:**

```bash
# Method 1: Activate then run
source .venv/bin/activate && python app.py

# Method 2: Direct execution (PREFERRED)
.venv/bin/python app.py
```

### Workflow 2: Installing Packages

**PowerShell:**

```powershell
./.venv/bin/Activate.ps1 ; pip install <package>
# OR
./.venv/bin/python -m pip install <package>
```

**Bash:**

```bash
source .venv/bin/activate && pip install <package>
# OR
.venv/bin/python -m pip install <package>
```

### Workflow 3: Running Flask/Django

**PowerShell:**

```powershell
./.venv/bin/Activate.ps1 ; python app.py
# OR
./.venv/bin/python app.py
```

**Bash:**

```bash
source .venv/bin/activate && python app.py
# OR
.venv/bin/python app.py
```

## Virtual Environment Setup

### Check if .venv Exists

```powershell
# PowerShell
Test-Path .venv

# Bash
test -d .venv && echo "exists" || echo "missing"
```

### Create .venv if Missing

```powershell
# PowerShell
python -m venv .venv

# Bash
python3 -m venv .venv
```

### Verify Activation

```powershell
# PowerShell - Should show .venv path
$env:VIRTUAL_ENV

# Bash - Should show .venv path
echo $VIRTUAL_ENV
```

## Common Errors & Solutions

### Error: "Activate.ps1 cannot be loaded"

**Solution:** Set PowerShell execution policy

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "python: command not found"

**Solution:** Use python3 or direct .venv path

```powershell
# Use python3
python3 -m venv .venv

# Or use .venv directly
./.venv/bin/python app.py
```

### Error: "No module named 'flask'"

**Solution:** Ensure .venv is activated and packages installed

```powershell
./.venv/bin/Activate.ps1 ; pip install -r requirements.txt
```

## Best Practices

1. **Always use .venv/bin/python directly** - Most reliable method
2. **Never assume system Python** - Always check for .venv
3. **Detect shell type** - Use appropriate activation syntax
4. **Fail gracefully** - If .venv missing, create it first
5. **Document requirements** - Keep requirements.txt updated
6. **Use python -m** - More reliable than calling pip/flask directly

## Terminal Command Template

Use this template for ALL Python-related terminal commands:

```python
# Step 1: Detect shell
shell_type = "powershell" if on_windows or using_pwsh else "bash"

# Step 2: Check .venv exists
if not exists(".venv"):
    create_venv()

# Step 3: Build command with activation
if shell_type == "powershell":
    command = "./.venv/bin/Activate.ps1 ; <your_command>"
else:
    command = "source .venv/bin/activate && <your_command>"

# Step 4: Execute
run_in_terminal(command)
```

## Quick Reference

| Task | PowerShell | Bash |
|------|-----------|------|
| Activate | `./.venv/bin/Activate.ps1` | `source .venv/bin/activate` |
| Run Python | `./.venv/bin/python app.py` | `.venv/bin/python app.py` |
| Install package | `./.venv/bin/pip install pkg` | `.venv/bin/pip install pkg` |
| Check activation | `$env:VIRTUAL_ENV` | `echo $VIRTUAL_ENV` |
| Deactivate | `deactivate` | `deactivate` |

## Integration with Other Skills

- **git-workflow-management**: Activate .venv before running git hooks with Python
- **code-documentation-standards**: Ensure .venv active when generating docs
- **ai-training-data-generation**: Activate .venv before training scripts

## Example Commands

### Starting Flask App

```powershell
# PowerShell (PREFERRED)
./.venv/bin/python app.py

# Or with activation
./.venv/bin/Activate.ps1 ; python app.py
```

### Installing Requirements

```powershell
# PowerShell (PREFERRED)
./.venv/bin/python -m pip install -r requirements.txt

# Or with activation
./.venv/bin/Activate.ps1 ; pip install -r requirements.txt
```

### Running Tests

```powershell
# PowerShell (PREFERRED)
./.venv/bin/python -m pytest tests/

# Or with activation
./.venv/bin/Activate.ps1 ; pytest tests/
```

### Multiple Commands

```powershell
# PowerShell
./.venv/bin/Activate.ps1 ; pip install flask ; python app.py

# Bash
source .venv/bin/activate && pip install flask && python app.py
```

## Validation

Before completing any Python task, verify:

1. ✅ .venv exists in project root
2. ✅ Correct shell syntax used (PowerShell vs Bash)
3. ✅ Virtual environment activated in command
4. ✅ No system Python used accidentally
5. ✅ Command tested and working

## Time Savings

Using this skill saves time by:

- ❌ No more "python: command not found" errors
- ❌ No more "No module named X" errors
- ❌ No more debugging which Python is running
- ✅ Consistent environment every time
- ✅ One command that always works
- ✅ No manual activation needed

## Remember

> **The most important rule: If you're running Python code, you MUST use .venv. No exceptions.**
