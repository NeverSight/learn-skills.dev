---
name: agent-skill-discovery
description: This skill should be used when the user wants to see all installed plugins, agents, skills, and MCP servers, and also inspect the current repository for local agents, skills, and MCP configuration. Scans the environment and presents a structured catalog of available resources. Works across all AI CLI platforms (Claude Code, GitHub Copilot, Gemini CLI, OpenCode, OpenAI Codex).
license: MIT
---

# agent-skill-discovery

## Purpose

Automated inventory of AI CLI resources across two scopes: resources installed on the system and resources present in the current repository. This skill provides a comprehensive, platform-agnostic catalog of plugins, agents, skills, and MCP servers available in the current environment.

The skill operates in discovery-only mode—it scans, lists, and presents resources without performing analysis, recommendations, or orchestration. It serves as the foundation layer for resource awareness across all supported AI CLI platforms.

## When to Use

Invoke this skill when:

- User wants to know what resources are installed
- Before planning complex tasks (foundation for orchestration)
- Debugging missing resources or capabilities
- Auditing available tools and integrations
- Discovering newly installed plugins or MCP servers
- Verifying skill installation after setup
- Understanding platform capabilities
- Checking whether the current repository contains local agents, skills, or MCP configs

## Platform Support

Works identically on all AI CLI platforms:
- **Claude Code** (`claude`)
- **GitHub Copilot CLI** (`gh copilot`)
- **Gemini CLI** (`gemini`)
- **OpenCode** (`opencode`)
- **OpenAI Codex** (`codex`)

## Progress Tracking

Display a progress gauge before each step to keep the user informed:

```
[████░░░░░░░░░░░░░░░░] 15% — Step 1/6: Scanning Plugins
[████████░░░░░░░░░░░░] 30% — Step 2/6: Scanning Skills
[████████████░░░░░░░░] 45% — Step 3/6: Scanning MCP Servers
[████████████████░░░░] 60% — Step 4/6: Scanning Repository
[██████████████████░░] 75% — Step 5/6: Applying Filters
[████████████████████] 100% — Step 6/6: Generating Catalog
```

## Workflow

### Step 0: Platform Detection

**Objective:** Identify which AI CLI platform is executing the skill.

**Detection Strategy:**

Check for platform-specific base directories in order:

```bash
# Platform detection by directory existence
if [ -d "$HOME/.claude/skills" ] && [ -f "$HOME/.claude/skills/agent-skill-discovery/SKILL.md" ]; then
    PLATFORM="claude"
    BASE_DIR="$HOME/.claude"
elif [ -d "$HOME/.github/skills" ] && [ -f "$HOME/.github/skills/agent-skill-discovery/SKILL.md" ]; then
    PLATFORM="copilot"
    BASE_DIR="$HOME/.github"
elif [ -d "$HOME/.gemini/skills" ] && [ -f "$HOME/.gemini/skills/agent-skill-discovery/SKILL.md" ]; then
    PLATFORM="gemini"
    BASE_DIR="$HOME/.gemini"
elif [ -d "$HOME/.opencode/skills" ] && [ -f "$HOME/.opencode/skills/agent-skill-discovery/SKILL.md" ]; then
    PLATFORM="opencode"
    BASE_DIR="$HOME/.opencode"
elif [ -d "$HOME/.codex/skills" ] && [ -f "$HOME/.codex/skills/agent-skill-discovery/SKILL.md" ]; then
    PLATFORM="codex"
    BASE_DIR="$HOME/.codex"
else
    PLATFORM="unknown"
    BASE_DIR="$HOME"
fi
```

**Platform Configuration:**

Set platform-specific paths dynamically:

```javascript
const PLATFORM_CONFIGS = {
  'claude': {
    name: 'Claude Code',
    baseDir: BASE_DIR,
    pluginsDir: BASE_DIR + '/plugins',
    skillsDir: BASE_DIR + '/skills',
    mcpConfig: BASE_DIR + '/.mcp.json'
  },
  'copilot': {
    name: 'GitHub Copilot CLI',
    baseDir: BASE_DIR,
    pluginsDir: BASE_DIR + '/plugins',
    skillsDir: BASE_DIR + '/skills',
    mcpConfig: BASE_DIR + '/.mcp.json'
  },
  'gemini': {
    name: 'Gemini CLI',
    baseDir: BASE_DIR,
    pluginsDir: BASE_DIR + '/plugins',
    skillsDir: BASE_DIR + '/skills',
    mcpConfig: BASE_DIR + '/.mcp.json'
  },
  'opencode': {
    name: 'OpenCode',
    baseDir: BASE_DIR,
    pluginsDir: BASE_DIR + '/plugins',
    skillsDir: BASE_DIR + '/skills',
    mcpConfig: BASE_DIR + '/.mcp.json'
  },
  'codex': {
    name: 'OpenAI Codex',
    baseDir: BASE_DIR,
    pluginsDir: BASE_DIR + '/plugins',
    skillsDir: BASE_DIR + '/skills',
    mcpConfig: BASE_DIR + '/.mcp.json'
  }
};

const config = PLATFORM_CONFIGS[PLATFORM];
```

### Step 1: Scan for Plugins

**Objective:** Discover all installed plugins and their agents.

**Actions:**

Use Glob to find plugin manifests:

```bash
# Search for plugin.json files
Glob pattern: "{config.pluginsDir}/*/plugin.json"
```

For each plugin found:

1. **Read plugin manifest:**
   ```bash
   Read: {plugin_path}/plugin.json
   ```

2. **Extract metadata:**
   - Plugin name
   - Plugin version
   - Plugin description
   - Agents array

3. **Parse agent details:**
   For each agent in the agents array:
   - Agent name
   - Agent description
   - Available tools (Glob, Grep, Read, Write, Bash, etc.)
   - Agent color/category (if specified)

**Data Structure:**

```json
{
  "name": "feature-dev",
  "version": "1.0.0",
  "description": "Feature development workflow automation",
  "agents": [
    {
      "name": "code-explorer",
      "description": "Deeply analyzes existing codebase features",
      "tools": ["Glob", "Grep", "Read", "Bash"]
    },
    {
      "name": "code-architect",
      "description": "Designs feature architectures",
      "tools": ["Glob", "Grep", "Read", "Write"]
    }
  ]
}
```

**Graceful Handling:**

- If plugins directory doesn't exist: Return empty plugin array
- If plugin.json is malformed: Log warning, skip plugin, continue
- If agents array is missing: Include plugin with 0 agents

### Step 2: Scan for Skills

**Objective:** Discover all installed skills and their metadata.

**Actions:**

Use Glob to find skill definitions:

```bash
# Search for SKILL.md files
Glob pattern: "{config.skillsDir}/*/SKILL.md"
```

For each skill found:

1. **Read skill file:**
   ```bash
   Read: {skill_path}/SKILL.md
   ```

2. **Parse YAML frontmatter:**
   Extract the YAML block between `---` delimiters:
   ```yaml
   ---
   name: skill-creator
   description: "This skill should be used when..."
   triggers:
     - "create a skill"
     - "new skill"
   version: 1.0.0
   category: development
   ---
   ```

3. **Extract metadata:**
   - Skill name
   - Description
   - Triggers (array of phrases)
   - Version
   - Category
   - Tags (if present)

**Data Structure:**

```json
{
  "name": "skill-creator",
  "version": "1.0.0",
  "description": "This skill should be used when the user wants to create a new skill",
  "category": "development",
  "triggers": ["create a skill", "new skill", "build a skill"],
  "tags": ["automation", "scaffolding"]
}
```

**Graceful Handling:**

- If skills directory doesn't exist: Return empty skill array
- If SKILL.md has no YAML frontmatter: Skip skill, continue
- If required fields missing (name, description): Log warning, skip
- If triggers is empty: Include skill with empty triggers array

### Step 3: Scan for MCP Servers

**Objective:** Discover configured MCP servers and their available tools.

**Actions:**

**3.1 Read MCP Configuration:**

```bash
# Check if MCP config exists
Read: {config.mcpConfig}
```

If file exists, parse JSON:

```json
{
  "mcpServers": {
    "claude_ai_Notion": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-notion"]
    },
    "plugin_playwright": {
      "type": "stdio",
      "command": "node",
      "args": ["/path/to/playwright-mcp/index.js"]
    }
  }
}
```

**3.2 Discover Available Tools:**

For each MCP server, use ToolSearch to find available tools:

```bash
# Search for MCP tools by server prefix
ToolSearch query: "mcp__{server_name}__*"
```

Example results:
- `mcp__claude_ai_Notion__notion-search`
- `mcp__claude_ai_Notion__notion-create-pages`
- `mcp__plugin_playwright__browser_navigate`
- `mcp__plugin_playwright__browser_click`

**3.3 Build MCP Server Inventory:**

```json
{
  "name": "claude_ai_Notion",
  "type": "stdio",
  "command": "npx -y @anthropic-ai/mcp-server-notion",
  "tools": [
    {
      "name": "notion-search",
      "fullName": "mcp__claude_ai_Notion__notion-search",
      "description": "Search Notion pages and databases"
    },
    {
      "name": "notion-create-pages",
      "fullName": "mcp__claude_ai_Notion__notion-create-pages",
      "description": "Create new Notion pages"
    }
  ],
  "toolCount": 5
}
```

**Graceful Handling:**

- If .mcp.json doesn't exist: Return empty MCP array
- If .mcp.json is malformed: Log warning, return empty array
- If ToolSearch fails: Continue with server info, mark tools as "unavailable"
- If no tools found for server: Include server with toolCount = 0

### Step 4: Scan Current Repository

**Objective:** Discover local resources inside the repository where the user is currently working.

**Scope:**

Scan from current working directory (repository root when available). Do not use hardcoded absolute paths.

**4.1 Discover Local Agents:**

Search for agent manifests in common conventions:
- `**/plugin.json` files containing `agents` arrays
- `**/agents/*.md` and `**/agents/*.json`
- `**/.claude/agents/*` and similar platform-local agent folders

For each candidate:
- Parse safely (JSON/YAML/Markdown metadata)
- Extract agent name, description, and source path
- Mark resource scope as `local`

**4.2 Discover Local Skills:**

Search for skill definitions in common conventions:
- `**/skills/*/SKILL.md`
- `**/.*/skills/*/SKILL.md` (hidden platform folders in repo)

Parse YAML frontmatter using same validation rules as installed skills.

**4.3 Discover Local MCP Configurations:**

Search for MCP configuration files in common conventions:
- `./.mcp.json`
- `./mcp.json`
- `./.config/mcp.json`
- `**/.mcp.json` (nested workspace folders)

If multiple files exist:
- Parse all valid configs
- Merge by server name
- Deduplicate with installed scope by server name + command

**4.4 Deduplication Rules:**

- Keep installed and local inventories in separate sections
- Inside each section, deduplicate by normalized name
- If same resource appears in both scopes, keep both entries and label scope explicitly

**Graceful Handling:**

- If repository has no local resources: Return empty local arrays
- If a local file is malformed: Skip file, continue scan
- If repository root cannot be determined: Fallback to current working directory

### Step 5: Apply Filters (Optional)

**Objective:** Filter results based on user-specified criteria.

**Filter Types:**

**5.1 By Resource Type:**

```bash
# User request: "list only plugins"
# Filter: Show only plugins, hide skills and MCPs

# User request: "show MCP servers"
# Filter: Show only MCP servers, hide plugins and skills
```

**5.2 By Category:**

```bash
# User request: "show development skills"
# Filter: skills.filter(s => s.category === 'development')

# User request: "list content tools"
# Filter: skills.filter(s => s.category === 'content')
```

**5.3 By Keyword Search:**

```bash
# User request: "find resources related to Notion"
# Search in: plugin names, descriptions, agent names, skill names, triggers, MCP server names

function searchResources(keyword) {
  const lowerKeyword = keyword.toLowerCase();

  return {
    plugins: plugins.filter(p =>
      p.name.includes(lowerKeyword) ||
      p.description.toLowerCase().includes(lowerKeyword)
    ),
    skills: skills.filter(s =>
      s.name.includes(lowerKeyword) ||
      s.description.toLowerCase().includes(lowerKeyword) ||
      s.triggers.some(t => t.includes(lowerKeyword))
    ),
    mcpServers: mcpServers.filter(m =>
      m.name.includes(lowerKeyword) ||
      m.tools.some(t => t.name.includes(lowerKeyword))
    )
  };
}
```

**Filter Detection:**

Detect filter intent from user request:
- "only", "just", "show me" → Type filter
- "related to", "about", "for" → Keyword search
- Category names (development, content, analysis) → Category filter

### Step 6: Generate Catalog

**Objective:** Present discovered resources in clean, structured markdown.

**Output Format:**

```markdown
# 📦 Resource Discovery Report

**Platform:** {platform_name}
**Scan Date:** {YYYY-MM-DD HH:MM:SS}

---

# 📦 Installed Resources

## 🔌 Plugins ({count})

### {plugin_name} v{version}
**Description:** {description}

**Agents ({count}):**
- `{agent_name}` - {description}
  - **Tools:** {tool1}, {tool2}, {tool3}

---

## 🛠️ Skills ({count})

### {skill_name} v{version}
**Description:** {description}
**Category:** {category}
**Triggers:** `{trigger1}`, `{trigger2}`, `{trigger3}`

---

## 🌐 MCP Servers ({count})

### {server_name} ({type})
**Status:** {✅ Connected | ⚠️ Disconnected}
**Command:** `{command} {args}`

**Tools ({count}):**
- `{tool_name}` - {description}

---

# 📁 Current Repository Resources

**Repository Path:** {cwd}

## 🔌 Local Agents ({count})

### {agent_name}
**Description:** {description}
**Source:** `{relative_path}`

## 🛠️ Local Skills ({count})

### {skill_name} v{version}
**Description:** {description}
**Source:** `{relative_path}`

## 🌐 Local MCP Servers ({count})

### {server_name} ({type|unknown})
**Source Config:** `{relative_path}`
**Command:** `{command_or_unknown}`

---

## 📊 Summary

- **Installed Plugins:** {count}
- **Installed Agents:** {count}
- **Installed Skills:** {count}
- **Installed MCP Servers:** {count}
- **Installed MCP Tools:** {count}
- **Local Agents:** {count}
- **Local Skills:** {count}
- **Local MCP Servers:** {count}
```

**Presentation Rules:**

1. **Resource Counts:**
   - Always show counts in section headers
   - Include summary at bottom

2. **Sorting:**
   - Plugins/Agents/Skills/MCPs: Alphabetical by name

3. **Empty Sections:**
   - If no installed resources found: Display "None installed"
   - If no local repository resources found: Display "None found in current repository"
   - Example: `## 🔌 Plugins (0)\n\nNone installed.`

4. **Tool Lists:**
   - For agents: Comma-separated tool names
   - For MCP servers: Bulleted list with descriptions

5. **Status Indicators:**
   - MCP Connected: ✅
   - MCP Disconnected: ⚠️
   - Unknown status: ❓

## Critical Rules

### **NEVER:**

- ❌ Hardcode platform names or paths (always detect dynamically)
- ❌ Assume directory structure exists (check first, handle gracefully)
- ❌ Execute any resource (only read and list)
- ❌ Analyze or recommend resources (that's orchestrator's job)
- ❌ Skip platform detection step
- ❌ Use platform-specific tool names without detection context
- ❌ Fail if a single resource is malformed (skip and continue)
- ❌ Make assumptions about missing metadata (use defaults or skip)
- ❌ Omit repository scope when user asks for full discovery

### **ALWAYS:**

- ✅ Detect platform automatically at runtime
- ✅ Scan for resources dynamically (fresh discovery each time)
- ✅ Use Glob for file discovery (not hardcoded ls or find)
- ✅ Use Read to parse JSON/YAML (not cat or grep)
- ✅ Handle missing directories/files gracefully (empty arrays, not errors)
- ✅ Present clean, structured markdown output
- ✅ Include resource counts in all sections
- ✅ Show platform name and timestamp in header
- ✅ Scan current repository in addition to installed scope
- ✅ Show installed and repository resources in separate sections
- ✅ Sort resources alphabetically within each section
- ✅ Validate JSON/YAML before parsing (try-catch)

### **DISCOVERY PRINCIPLES:**

- **Zero-Config:** Discover paths at runtime, never hardcode
- **Fail-Safe:** Missing resources return empty arrays, not errors
- **Platform-Agnostic:** Same output format on all 5 platforms
- **Dual-Scope:** Always inspect installed scope and current repository scope
- **Read-Only:** Never modify, execute, or recommend resources
- **Fresh Scan:** No caching, always scan fresh on invocation

## Example Usage

### Example 1: Full Inventory

**User Request:**
```
"What do I have installed?"
```

**Output:**
```markdown
# 📦 Installed Resources

**Platform:** Claude Code
**Scan Date:** 2026-02-07 14:32:15

---

## 🔌 Plugins (3)

### commit-commands v1.0.0
**Description:** Git commit workflow automation

**Agents (3):**
- `commit` - Create git commits with best practices
  - **Tools:** Bash, Read, Grep
- `commit-push-pr` - Commit, push, and open pull request
  - **Tools:** Bash, Read, Grep
- `clean_gone` - Clean up deleted remote branches
  - **Tools:** Bash

### feature-dev v1.2.0
**Description:** Feature development workflow automation

**Agents (3):**
- `code-explorer` - Deeply analyzes existing codebase
  - **Tools:** Glob, Grep, Read, Bash
- `code-architect` - Designs feature architectures
  - **Tools:** Glob, Grep, Read, Write, Bash
- `code-reviewer` - Reviews code for quality issues
  - **Tools:** Glob, Grep, Read, Bash

### plugin-dev v1.0.0
**Description:** Claude Code plugin development tools

**Agents (5):**
- `create-plugin` - Guided plugin creation workflow
  - **Tools:** Read, Write, Bash
- `skill-development` - Skill creation and optimization
  - **Tools:** Read, Write, Grep
- `command-development` - Slash command development
  - **Tools:** Read, Write
- `hook-development` - Plugin hook development
  - **Tools:** Read, Write, Grep
- `agent-development` - Agent creation and configuration
  - **Tools:** Read, Write

---

## 🛠️ Skills (8)

### agent-skill-discovery v1.0.0
**Description:** This skill should be used when the user wants to see all installed resources
**Category:** discovery
**Triggers:** `what do I have installed`, `list available resources`, `show my agents`

### audio-transcriber v1.0.0
**Description:** Transform audio recordings into professional Markdown documentation
**Category:** content
**Triggers:** `transcribe audio`, `convert audio to text`

### prompt-engineer v1.0.0
**Description:** Transforms user prompts into optimized prompts using frameworks
**Category:** optimization
**Triggers:** `improve this prompt`, `optimize prompt`, `enhance prompt`

### skill-creator v1.0.0
**Description:** This skill should be used when the user asks to create a new skill
**Category:** development
**Triggers:** `create a skill`, `new skill`, `build a skill`

### youtube-summarizer v1.0.0
**Description:** Extract transcripts from YouTube videos and generate summaries
**Category:** content
**Triggers:** `summarize youtube`, `youtube summary`, `analyze video`

(... 3 more skills)

---

## 🌐 MCP Servers (2)

### claude_ai_Notion (stdio)
**Status:** ✅ Connected
**Command:** `npx -y @anthropic-ai/mcp-server-notion`

**Tools (5):**
- `notion-search` - Search Notion pages and databases
- `notion-create-pages` - Create new Notion pages
- `notion-fetch` - Fetch Notion page content
- `notion-update-page` - Update existing Notion pages
- `notion-get-users` - Get Notion workspace users

### plugin_playwright (stdio)
**Status:** ✅ Connected
**Command:** `node /Users/user/.claude/plugins/playwright/index.js`

**Tools (15):**
- `browser_navigate` - Navigate to URL
- `browser_click` - Click element
- `browser_type` - Type text into element
- `browser_screenshot` - Take screenshot
- `browser_evaluate` - Run JavaScript in browser
(... 10 more tools)

---

## 📊 Summary

- **Total Plugins:** 3
- **Total Agents:** 11
- **Total Skills:** 8
- **Total MCP Servers:** 2
- **Total MCP Tools:** 20
```

### Example 2: Filtered by Type

**User Request:**
```
"List only MCP servers"
```

**Output:**
```markdown
# 📦 MCP Servers (2)

**Platform:** GitHub Copilot CLI
**Scan Date:** 2026-02-07 14:35:42

---

### claude_ai_Notion (stdio)
**Status:** ✅ Connected
**Tools (5):**
- notion-search
- notion-create-pages
- notion-fetch
- notion-update-page
- notion-get-users

### plugin_playwright (stdio)
**Status:** ✅ Connected
**Tools (15):**
- browser_navigate
- browser_click
- browser_type
- browser_screenshot
(... 11 more)
```

### Example 3: Keyword Search

**User Request:**
```
"Show skills related to content"
```

**Output:**
```markdown
# 📦 Skills - Search Results for "content" (2)

**Platform:** Gemini CLI
**Scan Date:** 2026-02-07 14:38:10

---

### audio-transcriber v1.0.0
**Description:** Transform audio recordings into professional Markdown documentation
**Category:** content
**Triggers:** `transcribe audio`, `convert audio to text`

### youtube-summarizer v1.0.0
**Description:** Extract transcripts from YouTube videos and generate summaries
**Category:** content
**Triggers:** `summarize youtube`, `youtube summary`
```

### Example 4: Empty Results

**User Request:**
```
"What do I have installed?"
```

**Output (fresh installation):**
```markdown
# 📦 Installed Resources

**Platform:** OpenCode
**Scan Date:** 2026-02-07 14:40:33

---

## 🔌 Plugins (0)

None installed.

---

## 🛠️ Skills (1)

### agent-skill-discovery v1.0.0
**Description:** Scans and lists all installed resources
**Category:** discovery
**Triggers:** `what do I have installed`

---

## 🌐 MCP Servers (0)

None configured.

---

## 📊 Summary

- **Total Plugins:** 0
- **Total Agents:** 0
- **Total Skills:** 1
- **Total MCP Servers:** 0
- **Total MCP Tools:** 0
```

## Technical Implementation Notes

### Platform Detection Algorithm

```javascript
function detectPlatform() {
  const platformChecks = [
    { path: '~/.claude/skills/agent-skill-discovery/SKILL.md', platform: 'claude' },
    { path: '~/.github/skills/agent-skill-discovery/SKILL.md', platform: 'copilot' },
    { path: '~/.gemini/skills/agent-skill-discovery/SKILL.md', platform: 'gemini' },
    { path: '~/.opencode/skills/agent-skill-discovery/SKILL.md', platform: 'opencode' },
    { path: '~/.codex/skills/agent-skill-discovery/SKILL.md', platform: 'codex' }
  ];

  for (const check of platformChecks) {
    if (fileExists(expandPath(check.path))) {
      return check.platform;
    }
  }

  return 'unknown';
}
```

### YAML Frontmatter Parsing

```javascript
function parseSkillFrontmatter(content) {
  const yamlMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!yamlMatch) return null;

  try {
    return parseYAML(yamlMatch[1]);
  } catch (error) {
    console.warn('Failed to parse YAML:', error);
    return null;
  }
}
```

### MCP Tool Discovery

```javascript
function discoverMCPTools(serverName) {
  try {
    const searchPattern = `mcp__${serverName}__*`;
    const toolResults = toolSearch(searchPattern);

    return toolResults.map(tool => ({
      name: tool.name.replace(`mcp__${serverName}__`, ''),
      fullName: tool.name,
      description: tool.description || 'No description'
    }));
  } catch (error) {
    console.warn(`Failed to discover tools for ${serverName}:`, error);
    return [];
  }
}
```

## Performance Considerations

- **Glob Optimization:** Use specific patterns (e.g., `*/plugin.json` not `**/*`)
- **Parallel Scanning:** Read plugins, skills, and MCPs concurrently when possible
- **Lazy Parsing:** Only parse YAML/JSON when displaying results
- **Caching:** No caching—always fresh scan (prioritize accuracy over speed)

## Error Recovery

- **Malformed JSON:** Skip resource, log warning, continue
- **Missing Directories:** Return empty array, no error
- **Permission Denied:** Log warning, continue with accessible resources
- **Network Timeout (MCP):** Mark as disconnected, continue

## Future Enhancements

Potential features for future versions:
- Export to JSON/CSV format
- Compare resources between platforms
- Historical tracking (what changed since last scan)
- Resource health checks (validate plugins/skills work)
- Auto-update detection (check for newer versions)

## Related Skills

- **agent-skill-orchestrator** - Uses this skill to discover resources before planning
- **skill-creator** - Creates new skills that will appear in discovery results
- **plugin-dev** - Creates plugins that will appear in discovery results
