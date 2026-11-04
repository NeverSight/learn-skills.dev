---
name: quotefix
description: Ensures correct quoting and escaping syntax across shells (PowerShell, Bash, CMD). Handles nested command scenarios, cross-shell calls, and Windows-specific PowerShell patterns.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Write
  - Edit
---

# Quotefix

This skill ensures commands are compatible with the user's shell environment by detecting the active shell and adjusting syntax for quoting and escaping.

## When to Use This Skill

- Executing shell commands that may differ between PowerShell, Bash, CMD, and other shells
- Working with file paths containing spaces or special characters
- Writing cross-platform scripts
- Dealing with environment variables and PATH configuration
- Handling nested command scenarios (calling one shell from another)
- Preventing quoting errors in complex command compositions

## Shell Detection Strategy

### 1. Detect the Active Shell

**On Unix/Linux/macOS:**
```bash
# Method 1: Check SHELL environment variable
echo $SHELL  # Shows the user's login shell (e.g., /bin/bash, /usr/bin/zsh)

# Method 2: Check current process
ps -p $$ -o comm=  # Shows the actual running shell

# Method 3: Check shell-specific variables
if [ -n "$BASH_VERSION" ]; then echo "bash"; fi
if [ -n "$ZSH_VERSION" ]; then echo "zsh"; fi
```

**On Windows:**
```powershell
# Method 1: Check environment variable
$env:SHELL  # May not be set on Windows

# Method 2: Check PowerShell version
$PSVersionTable.PSVersion  # PowerShell specific

# Method 3: Check if running in CMD
echo %COMSPEC%  # CMD specific
```

### 2. Platform Detection

```bash
# Detect OS
uname -s  # Linux, Darwin (macOS), MINGW64_NT (Git Bash on Windows)

# Or use Python for cross-platform detection
python -c "import platform; print(platform.system())"  # Linux, Windows, Darwin
```

## Syntax Adjustments by Shell

### Bash/Zsh (Unix/Linux/macOS)

**Quoting:**
- Single quotes: Literal strings, no variable expansion: `'$HOME'` → `$HOME`
- Double quotes: Allow variable expansion: `"$HOME"` → `/home/user`
- Escape special chars: `\"`, `\'`, `\\`, `\$`

**Escape Character:**
- Backslash `\` is the escape character
- Use `\$` for literal dollar sign
- Use `\"` for literal quote inside double-quoted string
- Use `\\` for literal backslash

**Examples:**
```bash
# File with spaces
filename="My Document.txt"
touch "$filename"
cat "$filename"

# Escape special characters
echo "Price: \$100"
echo 'Price: $100'  # Literal (no escaping needed in single quotes)

# Command substitution
current_date=$(date +%Y-%m-%d)

# Escaping in different contexts
echo "He said \"Hello\""
echo 'He said "Hello"'  # Easier in single quotes
```

### PowerShell (Windows)

**Quoting:**
- Single quotes: Literal strings: `'$env:HOME'` → `$env:HOME`
- Double quotes: Variable expansion: `"$env:HOME"` → `C:\Users\username`
- Escape character: Backtick `` ` ``
- Special chars: `` `n`` (newline), `` `t`` (tab), `` `$`` (literal $), `` `"`` (literal quote)

**Escape Character:**
- Backtick `` ` `` is the escape character (NOT backslash!)
- Use `` `$ `` for literal dollar sign
- Use `` `" `` for literal quote inside double-quoted string
- Use `` `` `` for literal backtick

**Here-Strings:**
PowerShell supports here-strings for multi-line text without escaping:

```powershell
# Expandable here-string (with variable expansion)
$message = @"
User: $env:USERNAME
Path: C:\Program Files\App
Quote: "Hello World"
"@

# Literal here-string (no variable expansion)
$message = @'
User: $env:USERNAME (literal, not expanded)
Path: C:\Program Files\App
Quote: "Hello World"
'@
```

**Stop-Parsing Token:**
The `---%` token tells PowerShell to stop parsing and pass everything after it as-is:

```powershell
# Without ---%: PowerShell interprets quotes and special chars
icacls C:\folder /grant Users:(OI)(CI)F  # May fail

# With ---%: Everything passed literally to the executable
icacls ---% C:\folder /grant Users:(OI)(CI)F

# Useful for calling native commands with complex arguments
curl ---% -X POST -H "Content-Type: application/json" -d '{"key":"value"}' http://api.example.com
```

**Common PowerShell Pitfalls:**

1. **Function Call Syntax** - Don't use parentheses like C#:
```powershell
# WRONG - This is treated as passing an array
Get-ChildItem("C:\", "*.txt")

# CORRECT - Space-separated parameters
Get-ChildItem "C:\" -Filter "*.txt"
Get-ChildItem C:\ *.txt

# WRONG - Parentheses group as single argument
Copy-Item($source, $destination)

# CORRECT - Space-separated
Copy-Item $source $destination
```

2. **Comparison Operators** - PowerShell uses different operators:
```powershell
# WRONG - These don't work in PowerShell
if ($x == 5)      # Syntax error
if ($x != 10)     # Syntax error
if ($x > 3)       # Wrong (redirects output!)

# CORRECT - Use PowerShell comparison operators
if ($x -eq 5)     # Equal
if ($x -ne 10)    # Not equal
if ($x -gt 3)     # Greater than
if ($x -ge 3)     # Greater than or equal
if ($x -lt 10)    # Less than
if ($x -le 10)    # Less than or equal
if ($x -like "test*")   # Wildcard matching
if ($x -match "regex")  # Regex matching
```

3. **The $_ Variable in Pipelines:**
```powershell
# $_ represents the current object in the pipeline
Get-ChildItem | Where-Object { $_.Length -gt 1MB }
1..10 | ForEach-Object { $_ * 2 }
Get-Process | Where-Object { $_.Name -like "chrome*" }

# PITFALL: $_ only exists in pipeline contexts
$x = $_  # This won't work outside a pipeline
```

4. **String Expansion:**
```powershell
# Variables expand in double quotes but not single quotes
$name = "World"
Write-Host "Hello $name"   # Outputs: Hello World
Write-Host 'Hello $name'   # Outputs: Hello $name

# Subexpression operator $() for complex expressions
Write-Host "Current date: $(Get-Date -Format 'yyyy-MM-dd')"
Write-Host "Files: $(Get-ChildItem | Measure-Object | Select-Object -ExpandProperty Count)"
```

**Examples:**
```powershell
# File with spaces
$filename = "My Document.txt"
New-Item -Path $filename -ItemType File
Get-Content $filename

# Escape special characters
Write-Host "Price: `$100"
Write-Host 'Price: $100'  # Literal (no escaping needed)

# Command substitution
$currentDate = Get-Date -Format "yyyy-MM-dd"

# Paths with spaces - always quote
$path = "C:\Program Files\My App\data.txt"
Test-Path "$path"

# Backtick for escaping
Write-Host "Line 1`nLine 2`nLine 3"  # Newlines
Write-Host "Column1`tColumn2`tColumn3"  # Tabs
Write-Host "He said `"Hello`""  # Quotes

# Using here-string for complex content
$script = @"
Write-Host "User: $env:USERNAME"
Get-Content "C:\Program Files\file.txt"
"@
Invoke-Expression $script
```

**PowerShell Documentation References:**
- [about_Quoting_Rules](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules)
- [about_Special_Characters](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_special_characters)
- [PowerShell Escape Characters (SS64)](https://ss64.com/ps/syntax-esc.html)

### CMD (Windows Command Prompt)

**Quoting:**
- Double quotes for paths with spaces: `"C:\Program Files\app.exe"`
- Escape character: Caret `^`
- Special chars: `^&`, `^|`, `^<`, `^>`, `^^`, `^%`

**Escape Character:**
- Caret `^` is the escape character
- Use `^&` to escape ampersand
- Use `^^` for literal caret
- Use `^%` to escape percent sign in batch files

**Examples:**
```cmd
REM File with spaces
set filename="My Document.txt"
type %filename%

REM Escape special characters
echo 5 ^& 6
echo Price: ^$100
echo 100^%% complete

REM Use variables
set "PATH_TO_APP=C:\Program Files\MyApp"
"%PATH_TO_APP%\app.exe"

REM Multiline commands
echo Line 1 ^
& echo Line 2 ^
& echo Line 3
```

### Fish Shell

**Quoting:**
- Single quotes: Literal
- Double quotes: Variable expansion
- No escape character in strings (use quotes instead)

**Examples:**
```fish
# File with spaces
set filename "My Document.txt"
touch $filename
cat $filename

# Variables
set current_date (date +%Y-%m-%d)

# No backslash escaping inside strings
# Use different quote types instead
echo "He said 'Hello'"
echo 'He said "Hello"'
```

## Nested Quoting and Command Composition

**This is the most common source of errors and repeated iterations!**

When commands are nested (calling one shell from another, or embedding commands within commands), quoting becomes exponentially complex. Here are the patterns that work:

### PowerShell.exe Called from CMD

**Problem:** Running PowerShell commands from CMD requires careful escaping.

```cmd
REM WRONG - Will fail with quotes
powershell.exe -Command "Get-Content "file.txt""

REM CORRECT - Use single quotes inside PowerShell command
powershell.exe -Command "Get-Content 'file.txt'"

REM CORRECT - For paths with spaces
powershell.exe -Command "Get-Content 'C:\Program Files\file.txt'"

REM CORRECT - Complex nested example
powershell.exe -Command "& {Get-ChildItem | Where-Object {$_.Name -like '*test*'}}"

REM CORRECT - Using here-string approach
powershell.exe -Command "$content = @'
C:\Program Files\file.txt
'@; Get-Content $content"
```

### PowerShell.exe Called from Bash/Zsh

**Problem:** Bash interprets quotes and variables before passing to PowerShell.

```bash
# WRONG - Bash interprets $_ and quotes
powershell.exe -Command "Get-Content 'file.txt' | Where-Object {$_.Length -gt 10}"

# CORRECT - Escape or use single quotes to protect from Bash
powershell.exe -Command 'Get-Content "file.txt" | Where-Object {$_.Length -gt 10}'

# CORRECT - Alternative with escaping
powershell.exe -Command "Get-Content 'file.txt' | Where-Object {\$_.Length -gt 10}"

# CORRECT - For paths with spaces
powershell.exe -Command "Get-Content 'C:\Program Files\My App\file.txt'"

# CORRECT - Complex nested with variable
powershell.exe -Command 'Get-Process | Where-Object {$_.CPU -gt 100} | Select-Object Name, CPU'
```

### Bash/sh Called from PowerShell

**Problem:** PowerShell's quoting and escaping rules differ from Bash.

```powershell
# WRONG - PowerShell interprets the quotes incorrectly
bash -c "echo 'Hello World'"

# CORRECT - Use single quotes in PowerShell, double inside bash
bash -c 'echo "Hello World"'

# CORRECT - Or escape quotes properly with backtick
bash -c "echo `"Hello World`""

# CORRECT - Complex nested example
bash -c 'grep "pattern" /path/to/file.txt | awk ''{print $1}'''

# CORRECT - Even better, use here-string
$command = @'
grep "pattern" /path/to/file.txt | awk '{print $1}'
'@
bash -c $command
```

### Git Commit Messages with Quotes

**Problem:** Commit messages often contain quotes and need proper escaping.

**Bash - Use HEREDOC (BEST PRACTICE):**
```bash
# CORRECT - Heredoc avoids all quoting issues
git commit -m "$(cat <<'EOF'
Add feature: User's "profile" page

- Implemented user's profile view
- Added "Edit Profile" button
- Fixed issue with apostrophes in names like O'Brien
EOF
)"
```

**PowerShell - Use here-string:**
```powershell
# CORRECT - Here-string
$message = @"
Add feature: User's "profile" page

- Implemented user's profile view
- Added "Edit Profile" button
- Fixed issue with apostrophes in names like O'Brien
"@
git commit -m $message
```

**CMD - Escape quotes:**
```cmd
REM CORRECT - Escape with caret (for special chars) or use simple quotes
git commit -m "Add feature: User's profile page"

REM For nested quotes, it's better to use a file
echo Add feature: User's "profile" page > commit_msg.txt
git commit -F commit_msg.txt
del commit_msg.txt
```

### Docker Exec with Nested Commands

**Problem:** Docker exec runs commands inside a container, requiring multiple levels of quoting.

```bash
# WRONG - Quotes not properly nested
docker exec container bash -c "echo 'Hello World'"

# CORRECT - Single quotes around the bash command
docker exec container bash -c 'echo "Hello World"'

# CORRECT - Complex example with variables
docker exec container bash -c 'grep "error" /var/log/app.log | tail -n 10'

# CORRECT - With file paths containing spaces
docker exec container bash -c 'cat "/app/My Files/config.txt"'
```

**From PowerShell:**
```powershell
# CORRECT - Use single quotes in PowerShell
docker exec container bash -c 'echo "Hello World"'

# CORRECT - Complex nested
docker exec container bash -c 'mysql -e "SELECT * FROM users WHERE name=''John''"'

# CORRECT - Using here-string for very complex commands
$dockerCmd = @'
bash -c 'grep "error" /var/log/app.log | awk "{print $1}"'
'@
docker exec container $dockerCmd
```

### SSH Commands with Nested Quotes

**Problem:** SSH executes commands on remote hosts, requiring quote preservation.

```bash
# WRONG - Quotes interpreted locally
ssh user@host "grep 'pattern' /var/log/syslog"

# CORRECT - Escape quotes for remote execution
ssh user@host 'grep "pattern" /var/log/syslog'

# CORRECT - Complex nested example
ssh user@host 'docker exec container bash -c "echo \"Hello\""'

# CORRECT - With variables (use backslash escaping)
local_var="pattern"
ssh user@host "grep '$local_var' /var/log/syslog"
```

### JSON Strings as Command Arguments

**Problem:** JSON contains quotes and braces that conflict with shell syntax.

**Bash:**
```bash
# WRONG - Unescaped quotes and braces
curl -X POST -d {"name": "value"} http://api.example.com

# CORRECT - Single quotes protect JSON
curl -X POST -d '{"name": "value", "nested": {"key": "val"}}' http://api.example.com

# CORRECT - With variables, use heredoc
json=$(cat <<EOF
{
  "name": "value",
  "path": "/home/user/My Files"
}
EOF
)
curl -X POST -d "$json" http://api.example.com
```

**PowerShell:**
```powershell
# CORRECT - Use here-string for JSON
$json = @'
{
  "name": "value",
  "nested": {
    "key": "val"
  }
}
'@
Invoke-RestMethod -Method Post -Body $json -Uri 'http://api.example.com'

# CORRECT - Or use ConvertTo-Json (BEST PRACTICE)
$data = @{
    name = "value"
    path = "C:\Program Files\App"
}
$json = $data | ConvertTo-Json
Invoke-RestMethod -Method Post -Body $json -Uri 'http://api.example.com'

# CORRECT - Inline JSON with proper escaping
$json = "{`"name`": `"value`", `"path`": `"C:\\Program Files\\App`"}"
Invoke-RestMethod -Method Post -Body $json -Uri 'http://api.example.com'
```

### Multiple Levels of Nesting

**Problem:** Commands within commands within commands...

```bash
# Example: SSH to host, run docker, execute bash inside container
# Level 1: Local Bash
# Level 2: SSH command
# Level 3: Docker exec
# Level 4: Bash inside container

# WRONG - Quotes completely broken
ssh user@host "docker exec container bash -c "echo 'Hello'""

# CORRECT - Progressive escaping
ssh user@host 'docker exec container bash -c "echo \"Hello\""'

# CORRECT - For very complex cases, use intermediate scripts
# Create script on remote host first, then execute it
cat > /tmp/script.sh << 'EOF'
docker exec container bash -c 'echo "Hello from container"'
EOF

ssh user@host 'bash /tmp/script.sh'
```

### Heredoc and Here-String Patterns (BEST PRACTICE)

**Use heredocs to avoid quoting hell entirely:**

**Bash Heredoc:**
```bash
# CORRECT - No escaping needed inside heredoc
cat > script.sh << 'EOF'
#!/bin/bash
echo "User's name: O'Brien"
grep "pattern" 'file with spaces.txt'
docker exec container bash -c 'echo "nested command"'
EOF

chmod +x script.sh
./script.sh
```

**PowerShell Here-String:**
```powershell
# CORRECT - No escaping needed inside here-string
$script = @'
Write-Host "User's name: O'Brien"
Get-Content "file with spaces.txt" | Select-String "pattern"
docker exec container bash -c 'echo "nested command"'
'@

$script | Out-File script.ps1
& .\script.ps1

# CORRECT - Expandable here-string (with variables)
$user = "O'Brien"
$script = @"
Write-Host "User's name: $user"
Get-Content "file with spaces.txt"
"@
```

### Quick Decision Tree for Nested Quoting

```
Is the command nested?
├─ No → Use normal quoting rules
└─ Yes → How many levels?
    ├─ 1 level (e.g., bash -c "...")
    │   └─ Use opposite quotes: outer double, inner single (or vice versa)
    ├─ 2 levels (e.g., ssh ... docker exec ...)
    │   └─ Use: outer single, middle double, inner escaped double
    └─ 3+ levels or contains JSON/complex strings
        └─ Use heredoc/here-string and avoid inline quoting entirely
```

### Common Nested Quoting Patterns Reference

| Scenario | Shell | Pattern | Example |
|----------|-------|---------|---------|
| Call PowerShell from Bash | Bash | Single quotes around entire command | `powershell.exe -Command 'Get-Content "file.txt"'` |
| Call Bash from PowerShell | PowerShell | Single quotes in PS, double in bash | `bash -c 'echo "Hello"'` |
| Git commit with quotes | Bash | Heredoc | `git commit -m "$(cat <<'EOF'...)"` |
| Git commit with quotes | PowerShell | Here-string | `$msg = @"..."@; git commit -m $msg` |
| Docker exec | Bash | Single outer, double inner | `docker exec c bash -c 'echo "Hi"'` |
| SSH command | Bash | Single quotes | `ssh host 'command "with quotes"'` |
| JSON in curl | Bash | Single quotes | `curl -d '{"key":"val"}' url` |
| JSON in PowerShell | PowerShell | ConvertTo-Json | `$obj | ConvertTo-Json` |

### Anti-Patterns to AVOID

```bash
# ❌ NEVER: Mix quotes without planning nesting
powershell.exe -Command "Get-Content "file.txt""

# ❌ NEVER: Forget to escape $ in bash when calling PowerShell
powershell.exe -Command "Get-Process | Where {$_.Name -eq 'foo'}"
# Should be: '\$_' or use single quotes

# ❌ NEVER: Use parentheses for PowerShell function calls from other shells
powershell.exe -Command "Get-ChildItem('C:\')"
# Should be: Get-ChildItem C:\

# ❌ NEVER: Use complex inline JSON
curl -d "{\"key\":\"value with spaces\",\"nested\":{\"key2\":\"val\"}}"
# Use heredoc or file instead

# ❌ NEVER: Chain multiple levels without testing each level
ssh host "docker exec c bash -c "mysql -e "SELECT * FROM t"""
# Build up from innermost to outermost

# ❌ NEVER: Use == in PowerShell conditions
powershell.exe -Command "if ($x == 5) { Write-Host 'Five' }"
# Should be: -eq instead of ==
```

### Best Practices for Avoiding Quoting Issues

1. **Use heredoc/here-string for anything complex** (3+ lines or 2+ nesting levels)
2. **Test each nesting level separately** before combining
3. **Prefer opposite quote types** at each level (outer double, inner single)
4. **Use intermediate files/scripts** for very complex cases
5. **Escape $ and ` in bash when passing to other shells**
6. **Use ConvertTo-Json in PowerShell** instead of manual JSON strings
7. **Document the nesting levels** with comments when unavoidable
8. **Remember PowerShell's unique syntax** (backtick, -eq vs ==, no parentheses for function calls)

## Cross-Platform Command Translation

### Common Operations

| Operation | Bash/Zsh | PowerShell | CMD |
|-----------|-----------|------------|-----|
| List files | `ls -la` | `Get-ChildItem` or `ls` | `dir` |
| Copy file | `cp src dst` | `Copy-Item src dst` | `copy src dst` |
| Move file | `mv src dst` | `Move-Item src dst` | `move src dst` |
| Delete file | `rm file` | `Remove-Item file` | `del file` |
| Echo | `echo "text"` | `Write-Host "text"` | `echo text` |
| Environment var | `$HOME` | `$env:HOME` | `%USERPROFILE%` |
| Path separator | `/` | `\` or `/` | `\` |
| Line continuation | `\` | `` ` `` | `^` |
| Escape character | `\` | `` ` `` | `^` |

## Implementation Guidelines

### Before Executing Commands

1. **Detect the shell:**
   ```bash
   # In Bash
   CURRENT_SHELL=$(basename "$SHELL")

   # Or check specific shell
   if [ -n "$BASH_VERSION" ]; then
       SHELL_TYPE="bash"
   elif [ -n "$ZSH_VERSION" ]; then
       SHELL_TYPE="zsh"
   fi
   ```

2. **Detect the platform:**
   ```bash
   case "$(uname -s)" in
       Linux*)     PLATFORM=linux;;
       Darwin*)    PLATFORM=mac;;
       MINGW*)     PLATFORM=windows;;
       *)          PLATFORM=unknown;;
   esac
   ```

3. **Apply appropriate syntax:**
   - Use proper quoting for the detected shell
   - Escape special characters correctly
   - Use correct path separators

## Complete Example: Cross-Platform Script

```bash
#!/usr/bin/env bash

# Detect shell and platform
detect_environment() {
    # Detect shell
    if [ -n "$BASH_VERSION" ]; then
        SHELL_TYPE="bash"
    elif [ -n "$ZSH_VERSION" ]; then
        SHELL_TYPE="zsh"
    elif [ -n "$FISH_VERSION" ]; then
        SHELL_TYPE="fish"
    else
        SHELL_TYPE="unknown"
    fi

    # Detect platform
    case "$(uname -s 2>/dev/null || echo Windows)" in
        Linux*)     PLATFORM="linux";;
        Darwin*)    PLATFORM="mac";;
        MINGW*|CYGWIN*|MSYS*)  PLATFORM="windows";;
        Windows*)   PLATFORM="windows";;
        *)          PLATFORM="unknown";;
    esac

    echo "Detected: $SHELL_TYPE on $PLATFORM"
}

# Create file with proper quoting
create_file() {
    local filename="My Document.txt"

    if [ "$SHELL_TYPE" = "bash" ] || [ "$SHELL_TYPE" = "zsh" ]; then
        # Bash/Zsh quoting
        touch "$filename"
        echo "Size: 100 MB" > "$filename"
    fi
}

# Main execution
detect_environment
create_file
```

## Quick Reference

### Quoting Rules
- **Bash/Zsh**: Use `"$var"` for expansion, `'literal'` for literal
- **PowerShell**: Use `"$var"` for expansion, `'literal'` for literal
- **CMD**: Use `%var%` for variables, `"path with spaces"`
- **Fish**: Use `"$var"` for expansion, `'literal'` for literal

### Escape Characters
- **Bash/Zsh**: `\` (backslash)
- **PowerShell**: `` ` `` (backtick) - NOT backslash!
- **CMD**: `^` (caret)
- **Fish**: No escape character (use different quote types)

### Path Separators
- **Unix/Linux/macOS**: `/`
- **Windows**: `\` (but PowerShell accepts both `/` and `\`)

### Special PowerShell Operators
- **Comparison**: `-eq`, `-ne`, `-gt`, `-ge`, `-lt`, `-le`, `-like`, `-match`
- **Pipeline variable**: `$_` (current object)
- **Stop-parsing**: `---%` (pass arguments literally)
- **Subexpression**: `$(...)` (embed expressions in strings)

## Best Practices

1. **Always detect before executing** - Never assume the shell type
2. **Quote all variables** - Prevents word splitting and globbing
3. **Test on target platform** - Cross-platform issues are common
4. **Provide fallbacks** - Handle unknown shells gracefully
5. **Document shell requirements** - Make dependencies clear
6. **Avoid shell-specific features** - When portability is needed
7. **Check command availability** - Use `command -v` before execution
8. **Remember PowerShell is different** - Backtick escaping, -eq operators, no function parentheses
9. **Use here-strings/heredocs for complex content** - Avoid escaping hell
10. **Build nested commands incrementally** - Test each level before combining
