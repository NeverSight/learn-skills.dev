---
name: claude-code-statusline
description: This skill should be used when configuring or troubleshooting Claude Code's status line using the ccstatusline tool. It provides installation, configuration, and customization guidance for displaying model information, Git status, context usage, and other useful information in the Claude Code status line.
---

# Claude Code Status Line Configuration

## Purpose

This skill provides comprehensive guidance for setting up and customizing Claude Code's status line using the `ccstatusline` tool. It addresses common issues with status line configuration on Windows PowerShell and other environments, and provides step-by-step instructions for installation, configuration, and troubleshooting.

## When to Use This Skill

Use this skill when:
- Claude Code's status line shows raw text (e.g., `"\u@\h:\w\$(git branch...)"`) instead of parsed values
- The status line is not showing any information
- You want to install and configure `ccstatusline` for better status line display
- You need to customize the status line appearance (Powerline style, colors, modules)
- You're experiencing platform-specific issues with status line configuration

## Prerequisites

- Node.js and npm installed (for `ccstatusline` installation)
- Claude Code version supporting `statusLine` configuration
- Git installed (for Git status display)

## Skill Contents

### Scripts (`scripts/`)
- `setup-windows.ps1` - PowerShell script for Windows configuration
- `setup-unix.sh` - Bash script for Unix/Linux/macOS configuration
- `test-statusline.ps1` - PowerShell test script for Windows
- `test-statusline.sh` - Bash test script for Unix/Linux/macOS

### References (`references/`)
- `configuration-guide.md` - Detailed configuration options and examples
- `troubleshooting.md` - Common issues and solutions
- `ccstatusline-customization.md` - Customizing ccstatusline appearance

### Assets (`assets/`)
- `example-config.json` - Example Claude Code configuration with ccstatusline
- `ccstatusline-config.json` - Example ccstatusline configuration with Powerline style enabled

## How to Use This Skill

### Quick Setup

1. **Install ccstatusline**:
   ```bash
   npm install -g ccstatusline
   ```

2. **Test ccstatusline**:
   ```bash
   echo '{"model": {"display_name": "test"}}' | ccstatusline
   ```

3. **Configure Claude Code**:
   Add or update the following in `~/.claude/settings.json` (or project `.claude/settings.json`):
   ```json
   {
     "statusLine": {
       "type": "command",
       "command": "ccstatusline"
     }
   }
   ```

4. **Restart Claude Code**:
   - Completely exit all Claude Code instances
   - Ensure no `claude.exe` processes are running
   - Restart Claude Code

### Platform-Specific Setup

#### Windows PowerShell
Use `scripts/setup-windows.ps1` for automated Windows configuration:
```powershell
.\scripts\setup-windows.ps1
```

Or manually:
1. Install ccstatusline: `npm install -g ccstatusline`
2. Test: `echo '{"model": {"display_name": "test"}}' | ccstatusline`
3. Update configuration in `$env:USERPROFILE\.claude\settings.json`
4. Restart Claude Code

#### Unix/Linux/macOS
Use `scripts/setup-unix.sh` for automated configuration:
```bash
chmod +x scripts/setup-unix.sh
./scripts/setup-unix.sh
```

### Customization

#### Theme-Aware Styling Considerations
When designing status line styles, always consider the user's terminal/interface theme:

1. **Dark Theme Compatibility**:
   - Avoid using `black` or very dark colors for text on dark backgrounds
   - Prefer light text colors (`white`, `brightWhite`, `cyan`, `yellow`) on colored backgrounds
   - Use high-contrast color combinations for readability

2. **Light Theme Compatibility**:
   - Avoid using `white` text on light backgrounds
   - Prefer dark text colors (`black`, `brightBlack`, `blue`, `magenta`) on light backgrounds

3. **Theme Detection**:
   - If the current theme cannot be determined, always ask the user before applying styles
   - Example questions:
     - "您当前使用的是暗黑主题还是亮色主题？"
     - "您的终端背景颜色是深色还是浅色？"

4. **Default Recommendations**:
   - For dark themes: Use light text with colored backgrounds
   - For light themes: Use dark text with light/colored backgrounds
   - Universal: Use moderate contrast and test with both themes

#### Enable Powerline Style
Edit `~/.config/ccstatusline/settings.json` (or `$env:USERPROFILE\.config\ccstatusline\settings.json` on Windows):
```json
{
  "powerline": {
    "enabled": true,
    "separators": [""],
    "separatorInvertBackground": [false]
  }
}
```

#### Custom Module Order
Modify the `lines` array in ccstatusline configuration to rearrange or remove modules:
- `model`: Shows current Claude model
- `context-length`: Shows context window usage
- `git-branch`: Shows current Git branch
- `git-changes`: Shows Git file changes (added/modified/deleted)

### Troubleshooting

#### Status Line Not Showing
1. **Verify ccstatusline installation**: `ccstatusline --help`
2. **Test with sample input**: `echo '{"model": {"display_name": "test"}}' | ccstatusline`
3. **Check Claude Code configuration**: Verify `statusLine.command` is set to `"ccstatusline"`
4. **Restart Claude Code**: Ensure complete restart
5. **Check terminal compatibility**: Try different terminal applications

#### Raw Text Displayed
If status line shows raw text like `"\u@\h:\w\$(git branch...)"`:
1. **Replace custom commands** with `ccstatusline`
2. **Remove any platform-specific** command configurations
3. **Use the scripts** provided in this skill for proper configuration

#### Platform-Specific Issues
- **Windows**: Ensure PowerShell execution policy allows script execution
- **Unix/Linux**: Ensure scripts have execute permissions
- **All platforms**: Verify Node.js and npm are properly installed

## Expected Output

After successful configuration, the status line should display information similar to:
```
Model: Claude 3.5 Sonnet | Context: 85% | ⎇ master | (+2,-1)
```

With Powerline style enabled:
```
 Model: Claude 3.5 Sonnet  Context: 85%  ⎇ master  (+2,-1) 
```

## References

For detailed information, consult:
- `references/configuration-guide.md` - Complete configuration options
- `references/troubleshooting.md` - Advanced troubleshooting steps
- `references/ccstatusline-customization.md` - Customization examples

## Maintenance

This skill should be updated when:
- ccstatusline releases new versions with breaking changes
- Claude Code changes its status line configuration format
- New platforms or environments require specific configuration
- Users report common issues not covered in current documentation