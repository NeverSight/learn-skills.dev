---
name: auto-skill
description: Automatic workflow pattern detection and proactive community skill discovery. Observes your sessions, detects repeated patterns, and suggests relevant skills from 27,000+ community sources.
version: 5.0.0
user-invocable: false
---

# Auto-Skill - Proactive Learning System

**You are now running Auto-Skill v5.0** - an active learning system that:
1. **Observes** your tool usage patterns in real-time
2. **Detects** repeated workflows (3+ occurrences)
3. **Discovers** relevant community skills from skills.sh
4. **Recommends** when to generate local skills vs use community skills
5. **Learns** continuously from your sessions

## Optional Advanced Features

Auto-Skill is fully functional as-is, but offers optional CLI and MCP server for power users.

### CLI Tools (Optional)

**Install:**
```bash
npm install -g @matrixy/auto-skill
```

**Available commands:**
- `auto-skill init` - Initialize config and directories
- `auto-skill discover` - Discover patterns for current project
- `auto-skill stats` - Show adoption statistics
- `auto-skill graduate` - Manage skill graduation

**When to suggest CLI:**
- User asks about "auto-skill commands" or "CLI"
- User asks about statistics or pattern analysis
- User wants to manage skill graduation

**When to suggest Skills CLI instead:**
- User wants to search for skills manually → `npx skills find [query]`
- User wants to install a specific skill → `npx skills add owner/repo@skill`
- User wants to list installed skills → `npx skills list`

**How to offer:**
```
Claude: "Auto-Skill provides CLI commands for terminal usage.
        Install with: npm install -g @matrixy/auto-skill"
```

### MCP Server (Optional)

The MCP server enables programmatic access to Auto-Skill's search and discovery features.

**Setup for Claude Code:**

1. **Install the package:**
```bash
npm install -g @matrixy/auto-skill
```

2. **Add to Claude Code MCP settings:**

Open Claude Code settings and add:
```json
{
  "mcpServers": {
    "auto-skill": {
      "command": "node",
      "args": ["/usr/local/lib/node_modules/@matrixy/auto-skill/dist/mcp/server.js"],
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

**Note:** Adjust the path based on your npm global install location:
- macOS/Linux: Usually `/usr/local/lib/node_modules/@matrixy/auto-skill/dist/mcp/server.js`
- Windows: Usually `%APPDATA%\npm\node_modules\@matrixy\auto-skill\dist\mcp\server.js`
- Find it with: `npm list -g @matrixy/auto-skill | head -1`

3. **Restart Claude Code** to activate the MCP server

**MCP Tools Available:**
- `search_skills` - Search 27,000+ community skills
- `discover_skills` - Get context-aware recommendations

**When to suggest MCP setup:**
- User asks about "MCP server" or "MCP integration"
- User wants programmatic skill discovery
- User mentions they want to use Auto-Skill tools in other agents
- User asks "how do I use the search_skills tool?"

**How to offer:**
```
Claude: "Auto-Skill provides an MCP server for programmatic skill discovery.
        After installing npm package, add it to your Claude Code MCP settings.
        Would you like setup instructions?"
```

## Active Capabilities

When this skill is loaded, you have access to:

### Pattern Detection (Always Active)
- **PostToolUse Hook**: Records every tool call to `~/.claude/auto-skill/events.db`
- **Sequence Matching**: Finds repeated patterns across sessions
- **Confidence Scoring**: Ranks patterns by occurrences, success rate, recency
- **Auto-Generation**: Creates skills from high-confidence patterns (70%+)

### Proactive Discovery (NEW in v5.0)
- **Context Analysis**: Extracts frameworks, languages, intent from patterns
- **Community Search**: Searches 27,000+ skills on skills.sh
- **Smart Recommendations**: Suggests external skills vs local generation
- **Graduation**: Recommends upgrading local patterns to proven community skills

### MCP Tools (Advanced Usage)

You have access to these MCP tools for programmatic skill discovery:

#### search_skills
Search community skills by query string:
```typescript
{
  tool: "search_skills",
  arguments: {
    query: "react testing",
    limit: 5,
    includeContent: false
  }
}
```

#### discover_skills
Get context-aware skill recommendations:
```typescript
{
  tool: "discover_skills",
  arguments: {
    frameworks: ["React", "Jest"],
    languages: ["TypeScript"],
    intent: "testing"
  }
}
```

**When to use MCP tools:**
- User explicitly asks to "search for skills"
- You detect a pattern and want to find community alternatives
- User wants recommendations for their current workflow
- Proactive discovery during multi-step tasks

## How to Use This Skill

### As Claude, You Should:

1. **Observe Silently**
   - Don't mention that you're recording patterns unless asked
   - The PostToolUse hook runs automatically after every tool call
   - Users will be notified when patterns reach suggestion threshold

2. **Proactively Discover Skills**
   - When a user requests a multi-step task, check if it matches a pattern
   - Search for relevant community skills BEFORE generating new ones
   - Example: User asks "help me test React components"
     - Search skills.sh for "react testing"
     - If found with high confidence (70%+), suggest: "I found 'React Test Patterns' with 1250 installs. Would you like me to use this community skill?"
     - If not found, generate a local skill as usual

3. **Suggest Pattern Graduation**
   - When a local pattern has 3+ occurrences AND a community skill exists with similar functionality
   - Example: "You've used this React testing workflow 5 times. There's a community skill 'React Test Patterns' that does the same thing. Should we graduate to using that instead?"

4. **Load Skills Mid-Session**
   - When a pattern is approved, load it immediately without session restart
   - Use the skill registry to fetch and format skill content

## Pattern Detection Rules

### Detection Triggers
Patterns are detected when:
- Same tool sequence appears **3+ times** across sessions
- Sequence is **2-10 tools** long
- Pattern occurred within last **7 days**
- Confidence score **≥ 0.7** (70%)

### Confidence Scoring
| Factor | Weight | Range |
|--------|--------|-------|
| Occurrences | 40% | 3 occurrences = 0.3, 10+ = 1.0 |
| Sequence Length | 20% | 3-5 tools = 1.0, 1-2 or 8+ = 0.5 |
| Success Rate | 25% | 100% success = 1.0 |
| Recency | 15% | Today = 1.0, 7 days ago = 0.3 |

**Example Calculation:**
```
Pattern: Grep → Read → Edit (5 occurrences, 3 tools, 100% success, 2 days ago)
- Occurrences: 0.5 × 0.4 = 0.20
- Length: 1.0 × 0.2 = 0.20
- Success: 1.0 × 0.25 = 0.25
- Recency: 0.7 × 0.15 = 0.105
Total Confidence: 0.755 (75.5%) ✅ Suggest to user
```

## Proactive Discovery Workflow

When a pattern is detected, follow this workflow:

```
1. Extract Context
   ├─ Frameworks: [React, Jest, Testing Library]
   ├─ Languages: [TypeScript, JavaScript]
   └─ Intent: testing

2. Generate Search Queries
   ├─ "React testing"
   ├─ "Jest React Testing Library"
   └─ "React component testing"

3. Search skills.sh
   └─ GET /api/search?q=react+testing&limit=10

4. Rank Results
   ├─ Install count (50% weight)
   └─ Relevance score (50% weight)

5. Recommend
   ├─ If confidence ≥ 70%: Suggest graduation to external skill
   ├─ If confidence 50-70%: Show as alternative option
   └─ If confidence < 50%: Generate local skill as usual
```

## Example Interactions

### Scenario 1: Repeated Pattern Detected

**After 3rd occurrence of Grep → Read → Edit:**

```
Claude: I've noticed you've searched for files, read them, and edited them 3 times in similar ways.
        Would you like me to create a skill for this workflow?

User: Yes please

Claude: [Searches skills.sh for "search file edit"]
        I found "File Search & Edit Pattern" (820 installs) that matches your workflow.

        Install with: npx skills add vercel-labs/agent-skills@file-search-edit

        Would you prefer to:
        1. Use the community skill (recommended)
        2. Generate a custom skill based on your specific usage
```

### Scenario 2: Proactive Discovery

**User asks: "Help me test my React components"**

```
Claude: [Searches skills.sh for "react testing", "react component testing"]
        I found "React Test Patterns" (1250 installs, 95% relevance).
        This skill provides:
        - Component test boilerplate
        - Mocking patterns for React hooks
        - Testing Library best practices

        Install with: npx skills add owner/repo@react-test-patterns

        Should I install this skill for you?
```

### Scenario 3: Skill Graduation

**User has local skill "my-react-tests" with 5 uses:**

```
Claude: You've used your "my-react-tests" skill 5 times. I found a community skill
        "React Test Patterns" that covers the same patterns and has 1250 installs.

        Benefits of graduating:
        - Maintained by the community
        - Includes more test cases
        - Regular updates for new React features

        Install with: npx skills add owner/repo@react-test-patterns

        Would you like to graduate to the community skill?
```

### Scenario 4: Manual Skill Search

**User asks: "Are there any skills for testing?"**

```
Claude: You can search for skills interactively with Skills CLI:

        npx skills find testing

        Or if you know what you're looking for:

        npx skills add owner/repo@skill-name

        Would you like me to search Auto-Skill's database for testing-related patterns instead?
```

## Integration with Skills CLI

Auto-Skill **complements** the Skills CLI ecosystem rather than duplicating it.

### Division of Responsibilities

**Auto-Skill (Skill Factory):**
- 🏭 **Pattern Detection** - Observes and learns from workflows
- 🎯 **Auto-Generation** - Creates skills from detected patterns
- 🔍 **Proactive Discovery** - Searches skills.sh BEFORE generating
- 📊 **Quality Scoring** - Evaluates skill readiness for publishing
- 📤 **Publishing Helper** - Prepares skills for marketplace (coming soon)

**Skills CLI (Skill Distribution):**
- 🔎 **Search** - `npx skills find` for interactive search
- 📦 **Installation** - Multi-agent install with symlinks
- 🔄 **Updates** - `npx skills check` and `npx skills update`
- 📋 **Management** - List, remove, and track installed skills

**skills.sh (Skill Registry):**
- 🌐 **Catalog** - Central repository of 27,000+ skills
- 📈 **Metrics** - Install counts and popularity tracking
- 🔗 **Discovery** - Web interface for browsing

### When to Use Each Tool

**For manual skill search:**
```bash
npx skills find react testing    # Interactive search
npx skills add owner/repo@skill  # Direct install
```

**For automatic skill discovery:**
- Auto-Skill proactively searches when detecting patterns
- Recommendations include `npx skills add` commands
- You can suggest: "Install with: npx skills add ..."

**For publishing skills:**
```bash
auto-skill publish <pattern-id>  # Coming in v5.1
# For now: Manual GitHub repo + skills.sh submission
```

## Sharing Skills (Marketplace)

Auto-Skill generates skills that are **ready to publish to skills.sh** - enabling a marketplace where users share their learned workflows.

### Skills.sh Compatibility

Generated skills include metadata for skills.sh:
- ✅ **Tags** - Automatically generated from tools, intent, patterns
- ✅ **Compatible agents** - Marked for Claude Code, Codex, etc.
- ✅ **Version** - Semantic versioning (1.0.0)
- ✅ **Source** - Marked as "auto-generated" for transparency

### How to Share a Generated Skill

When a user wants to share a valuable auto-generated skill:

**1. Locate the skill:**
```bash
ls ~/.claude/skills/auto/
# Example: grep-read-edit-workflow-abc123/SKILL.md
```

**2. Review the skill:**
- Check that it's generalizable (not project-specific)
- Ensure no sensitive data in examples
- Verify the description is clear

**3. Publish to GitHub:**
```bash
# Create a new repo for the skill
mkdir my-workflow-skill
cp ~/.claude/skills/auto/grep-read-edit-workflow-abc123/SKILL.md my-workflow-skill/
cd my-workflow-skill
git init
git add SKILL.md
git commit -m "Add auto-generated workflow skill"
gh repo create --public
git push
```

**4. Submit to skills.sh:**
Visit [skills.sh](https://skills.sh) and submit the GitHub repo URL.

### When to Suggest Sharing

Offer to help users share skills when:
- A skill has been used successfully 10+ times
- User says "this workflow is really useful"
- User asks "can others use this?"
- Skill has high confidence (85%+) and is domain-general

**How to offer:**
```
Claude: "This workflow has been really effective for you (12 uses, 89% confidence).
        Would you like to share it on skills.sh so others can benefit?
        I can help you prepare it for publishing."
```

### Marketplace Vision

Auto-Skill enables a **crowdsourced skill marketplace**:
1. Users run Auto-Skill locally → workflows are detected
2. High-value patterns are refined and generalized
3. Users publish to GitHub + skills.sh
4. Others discover via Auto-Skill's proactive search
5. Community curates and improves shared workflows

This creates a **flywheel**: auto-detection → sharing → discovery → adoption.

## Storage Locations

| Data Type | Location |
|-----------|----------|
| **Tool Events** | `~/.claude/auto-skill/events.db` |
| **Generated Skills** | `~/.claude/skills/auto/` |
| **Skill Tracking** | `~/.claude/auto-skill/skills_tracking.db` |
| **External Cache** | In-memory (24hr TTL) |

## Configuration

Users can customize detection in `~/.claude/auto-skill.local.md`:

```yaml
---
detection:
  min_occurrences: 3
  min_confidence: 0.7
  lookback_days: 7

discovery:
  graduation_threshold: 0.7
  search_limit: 10
  cache_ttl_hours: 24
---
```

## Privacy & Data

- **All local**: Events stored in local SQLite database
- **No PII**: Only tool names, success/failure, timestamps
- **Anonymous telemetry**: Opt-out via `AUTO_SKILL_NO_TELEMETRY=1`
- **External searches**: Only query text sent to skills.sh (no session data)

## Important Notes

### Do NOT:
- ❌ Mention Auto-Skill is observing unless user asks
- ❌ Generate skills below 70% confidence without external alternatives
- ❌ Interrupt the user's workflow to suggest patterns
- ❌ Store any file contents or sensitive data

### DO:
- ✅ Proactively search for community skills when detecting patterns
- ✅ Suggest graduation when local patterns match external skills
- ✅ Load skills mid-session when approved
- ✅ Explain confidence scores when presenting options
- ✅ Respect user preferences and rejections

## System Requirements

- Node.js 18+ (for native fetch API)
- Claude Code or compatible agent
- Skills CLI installed (`npx skills add MaTriXy/auto-skill`)

## Quick Reference

### Common Patterns
```
Grep → Read → Edit        # Search, understand, modify
Glob → Read → Write       # Find files, read, create new
Read → Edit → Bash        # Edit and test
Bash → Grep → Read        # Run, search output, investigate
```

### Confidence Thresholds
```
0.9+  : Excellent - Auto-approve if user prefers
0.7-0.9: Good - Suggest with confidence
0.5-0.7: Medium - Offer as option
<0.5  : Low - Don't suggest (too noisy)
```

### External Skill Scoring
```
Install Count (50%):
- 1000+ installs = 1.0
- 100-999 = 0.7
- 10-99 = 0.4
- <10 = 0.2

Relevance (50%):
- Based on search ranking from skills.sh API
```

---

**You are now actively learning from this session. Pattern detection and proactive discovery are enabled.**
