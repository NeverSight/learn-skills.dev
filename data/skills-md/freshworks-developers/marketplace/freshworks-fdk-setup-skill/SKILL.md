---
name: freshworks-fdk-setup-skill
description: Complete FDK management for macOS and Windows - install, upgrade, downgrade, and uninstall. Use when the user needs to install/configure/upgrade/downgrade/uninstall the Freshworks Development Kit, set up FDK on a new machine, asks about FDK installation on Mac or Windows, wants to change FDK version, or encounters FDK/CLI setup issues.
argument-hint: "[install|upgrade|downgrade|uninstall] [version]"
allowed-tools: ["shell", "read", "write", "task"]
---

# FDK Setup Skill

Complete automated FDK lifecycle management for macOS and Windows using subagents for complex multi-step operations.

## Usage

```bash
/fdk-setup install          # Install FDK with Node.js 18
/fdk-setup upgrade          # Upgrade to latest
/fdk-setup downgrade 9.6.0  # Downgrade to specific version
/fdk-setup uninstall        # Remove FDK completely
/fdk-setup                  # Check FDK status
```

## Execution Mode: SUBAGENT-BASED

**When invoked, spawn specialized subagents for each operation:**

1. Parse command arguments (`$ARGUMENTS`)
2. Launch appropriate subagent with Task tool
3. Subagent handles the complete operation autonomously
4. Report results when subagent completes

**Why Subagents:**
- Complex multi-step operations (nvm + Node.js 18 + FDK setup)
- Parallel execution of independent checks
- Isolated error handling per operation
- Better progress tracking and logging
- Autonomous execution without context pollution

**How to Invoke:**

When user requests FDK setup, immediately call the Task tool:

```javascript
// Example for install operation
Task({
  subagent_type: "shell",
  model: "fast",
  description: "Install FDK with Node.js 18",
  prompt: "..." // See operation-specific prompts below
})
```

The subagent will:
1. Execute all shell commands autonomously
2. Handle errors and retries
3. Report progress via terminal output
4. Return final status and summary

**DO NOT:**
- Execute shell commands directly from the main agent
- Ask for confirmation before spawning subagent
- Provide manual instructions instead of automation

**DO:**
- Spawn subagent immediately when skill is invoked
- Let subagent handle all complexity
- Report subagent results to user when complete

## Argument Parsing and Routing

**Parse `$ARGUMENTS` to determine operation:**

```javascript
// Extract operation and version from arguments
const args = $ARGUMENTS.trim().split(/\s+/);
const operation = args[0] || 'status';  // Default to status check
const version = args[1];                 // Optional version for downgrade

// Route to appropriate subagent
switch(operation) {
  case 'install':
    // Spawn install subagent (see Operation 1)
    break;
  case 'upgrade':
    // Spawn upgrade subagent (see Operation 2)
    break;
  case 'downgrade':
    // Spawn downgrade subagent with version (see Operation 3)
    if (!version) {
      // Ask user for version before spawning
      return "Please specify version: /fdk-setup downgrade 9.6.0";
    }
    break;
  case 'uninstall':
    // Spawn uninstall subagent (see Operation 4)
    break;
  case 'status':
  default:
    // Spawn status check subagent (see Operation 5)
    break;
}
```

## Operations

### 1. Install (`/fdk-setup install`)

**Launch subagent with Task tool:**

```javascript
Task({
  subagent_type: "shell",
  model: "fast",
  description: "Install FDK with Node.js 18",
  prompt: `Install Freshworks Development Kit (FDK) with complete Node.js 18 setup.

REQUIREMENTS:
1. Install nvm (Node Version Manager) if not present
2. Install Node.js 18 (latest 18.x version) via nvm
3. Set Node.js 18 as default for FDK (keep other versions intact)
4. Install FDK CLI via npm
5. Configure PATH and shell environment
6. Verify installation

STEPS TO EXECUTE:

1. CHECK EXISTING SETUP (parallel):
   - Check if nvm exists: command -v nvm
   - Check current Node.js: node --version
   - Check if FDK installed: fdk version
   - Detect OS: uname
   - Detect shell: echo $SHELL

2. INSTALL NVM (if missing):
   
   macOS/Linux:
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
   
   Then source the nvm script:
   export NVM_DIR="$HOME/.nvm"
   [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
   
   Windows (PowerShell as Administrator):
   # Download nvm-windows installer
   # Note: Cannot be automated via script, must inform user
   If Windows detected and nvm not found:
   Report: "Please install nvm-windows manually from: https://github.com/coreybutler/nvm-windows/releases"
   Report: "Download nvm-setup.exe, run as Administrator, then retry /fdk-setup install"
   Exit with instructions

3. INSTALL NODE.JS 18:
   nvm install 18
   nvm alias fdk 18
   nvm use 18
   
   Verify: node --version (should show v18.x.x)

4. CONFIGURE NVM FOR FDK:
   Create/update ~/.nvmrc in the FDK project directories with:
   18
   
   Add to shell config (~/.zshrc or ~/.bash_profile):
   # FDK uses Node.js 18
   export FDK_NODE_VERSION=18
   alias fdk-env='nvm use $FDK_NODE_VERSION'

5. INSTALL FDK:
   npm install https://cdn.freshdev.io/fdk/latest.tgz -g
   
   If using Homebrew (macOS only):
   brew tap freshworks-developers/homebrew-tap
   brew install fdk
   echo 'source "$(brew --repository freshworks-developers/homebrew-tap)/path.bash.inc"' >> ~/.zshrc

6. VERIFY INSTALLATION:
   fdk version
   node --version
   npm --version
   nvm current

7. OUTPUT SUMMARY:
   Report installed versions, paths, and next steps.

ERROR HANDLING:
- If nvm install fails, provide manual installation URL
- If Node.js 18 install fails, check disk space and network
- If FDK install fails, try alternative method (Homebrew vs npm)
- If PATH issues, provide manual PATH configuration

Execute all steps autonomously. Report progress and final status.`
})
```

### 2. Upgrade (`/fdk-setup upgrade`)

**Launch subagent with Task tool:**

```javascript
Task({
  subagent_type: "shell",
  model: "fast",
  description: "Upgrade FDK to latest",
  prompt: `Upgrade Freshworks Development Kit (FDK) to the latest version.

REQUIREMENTS:
1. Check current FDK version
2. Detect installation method (Homebrew vs npm)
3. Ensure Node.js 18 is active
4. Upgrade FDK
5. Verify upgrade success

STEPS TO EXECUTE:

1. CHECK CURRENT STATE (parallel):
   - fdk version
   - brew list fdk 2>/dev/null (check if Homebrew install)
   - node --version (ensure 18.x)
   - nvm current (check active Node version)

2. ENSURE NODE.JS 18 ACTIVE:
   If not on Node 18:
   nvm use 18 || nvm use fdk

3. UPGRADE FDK:
   If Homebrew installation:
   brew upgrade fdk
   
   If npm installation:
   npm install https://cdn.freshdev.io/fdk/latest.tgz -g

4. VERIFY UPGRADE:
   fdk version
   
5. OUTPUT SUMMARY:
   Report: Old version → New version
   Confirm Node.js version used

ERROR HANDLING:
- If upgrade fails, try uninstall + reinstall
- If network error, retry once
- If permission error, suggest sudo (macOS) or Administrator (Windows)

Execute autonomously. Report old and new versions.`
})
```

### 3. Downgrade (`/fdk-setup downgrade <version>`)

**Arguments:** Version number required (e.g., `9.6.0`, `9.7.4`)

**Launch subagent with Task tool:**

```javascript
Task({
  subagent_type: "shell",
  model: "fast",
  description: "Downgrade FDK to version X",
  prompt: `Downgrade Freshworks Development Kit (FDK) to version ${VERSION}.

REQUIREMENTS:
1. Parse target version from arguments
2. Check current FDK version
3. Ensure Node.js 18 is active
4. Uninstall current FDK
5. Install target version
6. Verify downgrade success

STEPS TO EXECUTE:

1. PARSE VERSION:
   Target version: ${VERSION}
   If no version provided, ask user for version number

2. CHECK CURRENT STATE (parallel):
   - fdk version (get current)
   - node --version (ensure 18.x)
   - nvm current (check active Node)

3. ENSURE NODE.JS 18 ACTIVE:
   nvm use 18 || nvm use fdk

4. UNINSTALL CURRENT FDK:
   Detect method and uninstall:
   brew uninstall fdk 2>/dev/null || npm uninstall fdk -g

5. INSTALL TARGET VERSION:
   IMPORTANT: CDN URL requires 'v' prefix
   npm install https://cdn.freshdev.io/fdk/v${VERSION}.tgz -g
   
   Example: For version 9.6.0, use:
   npm install https://cdn.freshdev.io/fdk/v9.6.0.tgz -g

6. VERIFY DOWNGRADE:
   fdk version
   Should show: ${VERSION}

7. OUTPUT SUMMARY:
   Report: Old version → ${VERSION}
   Confirm Node.js version

ERROR HANDLING:
- If version not found (404), list available versions
- If network error, retry once
- If permission error, suggest sudo

Execute autonomously. Report version change.`
})
```

**Important:** CDN URL requires `v` prefix: `https://cdn.freshdev.io/fdk/v9.7.4.tgz`

### 4. Uninstall (`/fdk-setup uninstall`)

**Launch subagent with Task tool:**

```javascript
Task({
  subagent_type: "shell",
  model: "fast",
  description: "Uninstall FDK completely",
  prompt: `Uninstall Freshworks Development Kit (FDK) completely from the system.

REQUIREMENTS:
1. Check if FDK is installed
2. Detect installation method
3. Remove FDK
4. Clean up shell configurations
5. Verify removal
6. Keep Node.js and nvm intact

STEPS TO EXECUTE:

1. CHECK IF INSTALLED:
   fdk version
   If not found, report "FDK not installed" and exit

2. DETECT INSTALLATION METHOD:
   brew list fdk 2>/dev/null && METHOD="homebrew" || METHOD="npm"

3. UNINSTALL FDK:
   
   If Homebrew:
   brew uninstall fdk
   brew untap freshworks-developers/homebrew-tap
   
   # Clean shell configs (create backups)
   sed -i.bak '/freshworks-developers\/homebrew-tap\/path.bash.inc/d' ~/.zshrc
   sed -i.bak '/freshworks-developers\/homebrew-tap\/path.bash.inc/d' ~/.bash_profile
   
   If npm:
   npm uninstall fdk -g

4. CLEAN UP FDK ALIASES (optional):
   Remove FDK-related aliases from shell config:
   sed -i.bak '/FDK_NODE_VERSION/d' ~/.zshrc
   sed -i.bak '/fdk-env/d' ~/.zshrc

5. VERIFY REMOVAL:
   fdk version
   Should output: command not found

6. OUTPUT SUMMARY:
   Report: FDK uninstalled successfully
   Note: Node.js 18 and nvm remain installed

ERROR HANDLING:
- If permission denied, suggest sudo
- If files locked, check for running FDK processes

Execute autonomously. Report completion status.`
})
```

### 5. Status Check (`/fdk-setup`)

**Launch subagent with Task tool:**

```javascript
Task({
  subagent_type: "shell",
  model: "fast",
  description: "Check FDK installation status",
  prompt: `Check Freshworks Development Kit (FDK) installation status and environment.

REQUIREMENTS:
1. Check if FDK is installed and version
2. Check Node.js version and nvm status
3. Check PATH configuration
4. Verify FDK can run basic commands
5. Report any issues or recommendations

STEPS TO EXECUTE:

1. CHECK VERSIONS (parallel):
   - fdk version
   - node --version
   - npm --version
   - nvm current
   - nvm list
   - which fdk
   - which node

2. CHECK ENVIRONMENT:
   - echo $PATH | grep -o '[^:]*node[^:]*'
   - echo $NVM_DIR
   - cat ~/.nvmrc 2>/dev/null || echo "No .nvmrc"

3. TEST FDK FUNCTIONALITY:
   fdk --help

4. ANALYZE AND REPORT:
   ✓ FDK: version X.X.X
   ✓ Node.js: vX.X.X (via nvm)
   ✓ Active nvm alias: fdk → 18.x.x
   ✓ PATH configured correctly
   
   Or report issues:
   ✗ FDK not found
   ✗ Node.js version < 18.13.0
   ⚠ Multiple Node versions but no nvm
   
5. RECOMMENDATIONS:
   If issues found, suggest:
   - Run /fdk-setup install
   - Upgrade Node.js to 18.x
   - Configure nvm

Execute autonomously. Report comprehensive status.`
})
```

## Template Variables

Use Maestro template variables for context:

- `{{CWD}}` - Current working directory
- `{{DATE}}` - Current date
- `{{AGENT_PATH}}` - Project path
- `{{GIT_BRANCH}}` - Current git branch

Example: `/fdk-setup install` in project at `{{AGENT_PATH}}`

## Node.js 18 and nvm Strategy

**Why nvm:**
- FDK requires Node.js 18.13.0 or later
- Users may have other Node versions for different projects
- nvm allows switching between versions seamlessly
- Keeps existing Node installations intact

**Implementation:**
1. Install nvm if not present
2. Install Node.js 18 (latest 18.x) via nvm
3. Create nvm alias `fdk` pointing to Node 18
4. Set Node 18 as default when working with FDK
5. Keep other Node versions available (20, 22, etc.)

**Usage after setup:**
```bash
nvm use fdk          # Switch to Node 18 for FDK work
nvm use 20           # Switch to Node 20 for other projects
nvm use default      # Switch to system default
```

**Shell Configuration:**
Add to `~/.zshrc` or `~/.bash_profile`:
```bash
# FDK uses Node.js 18
export FDK_NODE_VERSION=18
alias fdk-env='nvm use $FDK_NODE_VERSION'
```

## Error Handling

| Error | Action |
|-------|--------|
| nvm not installed | Install nvm automatically via curl script |
| Node.js < 18.13.0 | Install Node 18 via nvm |
| FDK already installed | Report version, ask if upgrade needed |
| Permission denied | Suggest: `sudo` (macOS) or Administrator (Windows) |
| Network error | Retry once, then report |
| Invalid version | List common versions: 9.7.4, 9.6.0, 9.4.1 |
| nvm install fails | Provide manual installation URL |

## Success Output

```
✓ Detected: macOS (darwin)
✓ nvm installed: v0.40.1
✓ Node.js 18 installed: v18.20.8
✓ nvm alias 'fdk' → 18.20.8
✓ FDK installed via npm: 9.7.4
✓ Configured PATH in ~/.zshrc
✓ Environment variables set

FDK Setup Complete!

Node.js versions available:
  → v18.20.8 (default for FDK)
    v20.11.0
    v22.1.0

Ready to use: fdk create, fdk run, fdk validate

To switch to FDK environment: nvm use fdk
To switch to other Node versions: nvm use 20
```

## Subagent Execution Pattern

Each operation spawns a dedicated shell subagent using the Task tool:

**Benefits:**
- **Isolation** - Each operation runs in its own context
- **Parallel checks** - Multiple commands run simultaneously
- **Error recovery** - Subagent can retry and handle failures
- **Progress tracking** - Clear status updates throughout
- **Autonomy** - No user intervention required

**Pattern:**
```javascript
Task({
  subagent_type: "shell",      // Shell specialist for command execution
  model: "fast",               // Fast model for straightforward tasks
  description: "Brief summary", // 3-5 words
  prompt: `Detailed instructions with:
    - Requirements
    - Step-by-step workflow
    - Error handling
    - Output format
  `
})
```

## Important Notes

### Node.js 18 Requirement

- **FDK requires Node.js 18.13.0 or later**
- Node.js 18 is LTS (Long Term Support) until April 2025
- Recommended: Use latest 18.x version (18.20.x as of 2024)

### nvm Benefits

- **Version isolation** - Keep Node 18 for FDK, other versions for other projects
- **Easy switching** - `nvm use 18` vs `nvm use 20`
- **No conflicts** - Each version has its own global npm packages
- **Project-specific** - `.nvmrc` files auto-switch versions per project

### PATH and Environment

After nvm + Node 18 + FDK installation:

**macOS/Linux:**
- nvm manages Node.js binaries in `~/.nvm/versions/node/v18.x.x/bin/`
- npm global packages in `~/.nvm/versions/node/v18.x.x/lib/node_modules/`
- FDK binary at `~/.nvm/versions/node/v18.x.x/bin/fdk`

**Windows:**
- nvm-windows manages Node.js in `C:\Users\<User>\AppData\Roaming\nvm\v18.x.x\`
- npm global packages in `%APPDATA%\npm\`
- FDK binary at `%APPDATA%\npm\fdk.cmd`

### Keeping Other Node Versions

The subagent will:
- **Never remove** existing Node installations
- **Never change** default Node version (unless user has no default)
- **Create alias** `fdk` pointing to Node 18
- **Keep** Node 20, 22, or any other versions intact

Users can switch anytime:
```bash
nvm use fdk    # Node 18 for FDK
nvm use 20     # Node 20 for other work
nvm use 22     # Node 22 for cutting-edge projects
```

## References

- [macOS Setup](references/macos.md) - Homebrew and npm installation with nvm
- [Windows Setup](references/windows.md) - npm and PATH configuration with nvm-windows
- [nvm Documentation](https://github.com/nvm-sh/nvm) - Node Version Manager for macOS/Linux
- [nvm-windows](https://github.com/coreybutler/nvm-windows) - Node Version Manager for Windows
