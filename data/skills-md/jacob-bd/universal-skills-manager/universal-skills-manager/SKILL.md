---
name: universal-skills-manager
description: "The master coordinator for AI skills. Discovers skills from multiple sources (SkillsMP.com, SkillHub, and ClawHub), manages installation, and synchronization across Claude Code, Gemini CLI, Google Anti-Gravity, OpenCode, and other AI tools. Handles User-level (Global) and Project-level (Local) scopes."
compatibility: "Requires python3, curl, and network access to skillsmp.com, skills.palebluedot.live, clawhub.ai, and github.com"
metadata:
  homepage: https://github.com/jacob-bd/universal-skills-manager
  disable-model-invocation: "true"
  requires-bins: "python3, curl"
  primaryEnv: SKILLSMP_API_KEY
---

<!-- Version: 1.10.0 -->

# Universal Skills Manager

This skill empowers the agent to act as a centralized skill manager for AI capabilities. It discovers skills from multiple sources — SkillsMP.com (curated, AI semantic search), SkillHub (community skills, no API key required), and ClawHub (versioned skills, semantic search, no API key required) — and unifies skill management across multiple AI tools (Claude Code, Gemini, Anti-Gravity, OpenCode, Cline, Cursor, etc.), ensuring consistency and synchronization.

## When to Use This Skill

Activate this skill when the user:
- Wants to **find or search** for new skills.
- Wants to **install** a skill (from a search result or local file).
- Wants to **sync** skills between different AI tools (e.g., "Copy this Gemini skill to OpenCode").
- Asks to **move or copy** skills between scopes (User vs. Project).
- Mentions "Google Anti-Gravity", "OpenCode", or "Gemini" in the context of skills/extensions.
- Wants to **package a skill for claude.ai, Claude Desktop, or ChatGPT** (ZIP upload).

## Supported Ecosystem

This skill manages the following tools and scopes. Always verify these paths exist before acting.

| Tool | User Scope (Global) | Project Scope (Local) |
| :--- | :--- | :--- |
| **Gemini CLI / Codex** | `~/.agents/skills/` | `./.agents/skills/` |
| **Google Anti-Gravity** | `~/.gemini/antigravity/skills/` | `./.antigravity/extensions/` |
| **OpenCode** | `~/.config/opencode/skills/` | `./.opencode/skills/` |
| **OpenClaw** | `~/.openclaw/workspace/skills/` | `./.openclaw/skills/` |
| **CC-Claw** | `~/.cc-claw/workspace/skills/` | N/A (daemon, no project scope) |
| **Claude Code** | `~/.claude/skills/` | `./.claude/skills/` |
| **block/goose** | `~/.config/goose/skills/` | `./.goose/agents/` |
| **Roo Code** | `~/.roo/skills/` | `./.roo/skills/` |
| **Cursor** | `~/.cursor/skills/` | `./.cursor/skills/` |
| **Cline** | `~/.cline/skills/` | `./.cline/skills/` |

*Note: Gemini CLI (v0.30+) and OpenAI Codex both use `~/.agents/skills/` as their skills directory. Gemini CLI also reads `~/.gemini/skills/` but gives `.agents/skills/` higher precedence. To avoid duplicate-skill conflicts, we install to `~/.agents/skills/` only, which serves both tools.*

**Cloud Platforms (ZIP Upload Required):**

| Platform | Installation Method |
| :--- | :--- |
| **claude.ai** | Upload ZIP via Settings → Capabilities → Upload Skill |
| **Claude Desktop** | Upload ZIP via Settings → Capabilities → Upload Skill |
| **ChatGPT** | Upload ZIP via Profile → Skills → New skill → Upload from your computer |

*Note: claude.ai, Claude Desktop, and ChatGPT don't have access to local environment variables. Use the "Package for Cloud Upload" capability (Section 5) to create a ZIP. Embedding an API key is optional — SkillHub and ClawHub search work without one. If you do include a key, do NOT share the ZIP publicly (see Section 5 for credential safety guidance).*

*ChatGPT Skills are currently in beta and available on Business, Enterprise, Edu, Teachers, and Healthcare plans. Skills are off by default for Enterprise/Edu — workspace admins must enable them in Permissions & roles.*

**IMPORTANT - Universal Skills Manager Platform Limitations:**

This skill (Universal Skills Manager) requires network access to call the SkillsMP API, SkillHub API, ClawHub API, and GitHub. Handle these scenarios:

- **If user asks to package/ZIP the Universal Skills Manager itself for claude.ai or ChatGPT:**
  Tell the user: "The Universal Skills Manager won't work on claude.ai or ChatGPT because it requires network access to call the SkillsMP API, SkillHub API, ClawHub API, and GitHub APIs. These platforms' code execution environments don't allow outbound network requests. However, I can package OTHER skills for cloud upload - those will work as long as they don't require network access."

- **If user wants to try the Universal Skills Manager on Claude Desktop:**
  Tell the user: "Claude Desktop has network access capabilities, but there is a **known bug** where custom domains added to the 'Additional allowed domains' setting are not included in the network egress JWT token. This means the skill cannot reach the required APIs even after whitelisting them.

  **Required domains** (for when the bug is fixed):
  - `skillsmp.com` (for SkillsMP skill searches)
  - `skills.palebluedot.live` (for SkillHub skill searches)
  - `clawhub.ai` (for ClawHub skill searches and direct file downloads)
  - `api.github.com` and `raw.githubusercontent.com` (for skill downloads from GitHub)

  **Workaround:** Use Claude Code CLI instead, which has unrestricted network access and works with all three skill sources. You can install via: `curl -fsSL https://raw.githubusercontent.com/jacob-bd/universal-skills-manager/main/install.sh | sh -s -- --tools claude`"

*(Note: If a tool uses a different directory structure, ask the user to confirm the path, then note it for future reference.)*

## Core Capabilities

### 1. Smart Installation & Synchronization
**Trigger:** User asks to install a skill (e.g., "Install the debugging skill" or "Install skill ID xyz").

**Procedure:**
1.  **Identify Source:**
    *   If from SkillsMP search result: Use the `githubUrl` from the API response
    *   If from SkillHub search result: Fetch skill details via `/api/skills/{id}` to get `skillPath` and `branch`, then construct GitHub tree URL
    *   If from ClawHub search result: Use the `slug` to fetch content via ClawHub's `/file` endpoint (see Section C below)
    *   If from skill name/ID: Search available sources (SkillsMP, SkillHub, and/or ClawHub) to find the skill
    *   If local: Identify the source path
2.  **Verify Repository Structure (CRITICAL):**
    *   Before downloading, browse the GitHub repo to confirm the skill folder location
    *   Use GitHub API to list directory contents: `GET /repos/{owner}/{repo}/contents?ref={branch}`
    *   Look for folders containing `SKILL.md` - this is the actual skill directory
    *   Common patterns: `skill/`, `skills/{name}/`, root level, or custom folder names
    *   Confirm the correct path before generating the download URL
3.  **Download Using Helper Script:**
    *   Use `install_skill.py` (located in this skill's `scripts/` folder):
    ```bash
    python3 ~/.claude/skills/universal-skills-manager/scripts/install_skill.py \
      --url "https://github.com/{owner}/{repo}/tree/{branch}/{skill-folder}" \
      --dest "{target-path}" \
      --dry-run  # Preview first, then remove flag to install
    ```
    *   The script handles: atomic install, validation, subdirectories, safety checks
    *   **Safety feature**: Script will abort (exit code 4) if destination is a root skills directory
    *   **Update detection**: If skill exists, shows diff and prompts for confirmation
    *   **Security scan**: The install script automatically scans downloaded skills for security threats (invisible characters, data exfiltration, prompt injection). Review any findings before proceeding.
4.  **Determine Primary Target:**
    *   Ask: "Should this be installed Globally (User) or Locally (Project)?"
    *   Determine the primary tool (e.g., if user is in Claude Code, Claude is primary)
    *   **If the user specifies claude.ai, Claude Desktop, or ChatGPT as the target**, go to Step 4a instead of Step 5.

    **4a. Cloud Platform Target Flow (claude.ai / Claude Desktop / ChatGPT):**
    If the user wants the skill for claude.ai, Claude Desktop, or ChatGPT:
    1.  **Validate frontmatter** by running `validate_frontmatter.py` against the downloaded SKILL.md:
        ```bash
        python3 scripts/validate_frontmatter.py /path/to/downloaded/SKILL.md
        ```
    2.  **If the skill passes validation**, package it as a ZIP and provide upload instructions (see Step 6a below).
    3.  **If the skill fails validation**, notify the user with the exact issues before doing anything:
        > "This skill isn't formatted correctly for cloud upload. I found these issues:
        > - [list each issue from the validator, e.g., 'Unsupported top-level key: version', 'Description uses a YAML block scalar']
        >
        > I can fix these automatically — unsupported keys will be moved into metadata, block scalars will be converted to inline strings, etc. The skill's functionality won't change.
        >
        > Would you like me to fix it and package it?"
    4.  **If the user agrees**: Run the fix and re-validate:
        ```bash
        python3 scripts/validate_frontmatter.py /path/to/downloaded/SKILL.md --fix
        ```
        Then package as ZIP (Step 6a).
    5.  **If the user declines**: Skip cloud packaging. Offer to install the skill as-is to other locally detected tools instead.

    **6a. Package and deliver ZIP:**
    *   Create a ZIP containing the skill folder (with fixed SKILL.md if applicable)
    *   Provide upload instructions based on the target platform:
        > **For claude.ai / Claude Desktop:**
        > "Your skill is packaged and ready. To install:
        > 1. Go to Settings → Capabilities
        > 2. Click 'Upload skill' in the Skills section
        > 3. Select the ZIP file and upload"
        >
        > **For ChatGPT:**
        > "Your skill is packaged and ready. To install:
        > 1. Click your profile icon and select Skills (or go to chatgpt.com/skills)
        > 2. Click 'New skill'
        > 3. Select 'Upload from your computer'
        > 4. Select the ZIP file and upload"
    *   Continue to Step 5 to offer syncing to other local tools as well.

5.  **The "Sync Check" (CRITICAL):**
    *   **Scan:** Check if other supported tools are installed on the system (look for their config folders)
    *   **Propose:** "I see you also have OpenCode and Cursor installed. Do you want to sync this skill to them as well?"
6.  **Execute:**
    *   For each target location, ensure the parent directory exists: `mkdir -p {target-skills-dir}`
    *   Run the install script for each target location
    *   Ensure the standard structure is maintained
7.  **Report Success:**
    *   Show installed skill name, author, and location(s)
    *   Display GitHub URL and stars count for reference

### 2. The "Updates & Consistency" Check
**Trigger:** User modifies a skill, asks to "sync" skills, or asks about skill consistency across tools.

**Procedure:**
1.  **Run the sync status reporter** (read-only — it never modifies files):
    ```bash
    python3 scripts/sync_skills.py
    ```
    For a specific skill only:
    ```bash
    python3 scripts/sync_skills.py --skill {skill-name}
    ```
    To include project-level skills:
    ```bash
    python3 scripts/sync_skills.py --project-dir /path/to/project
    ```
    For machine-readable output (useful for programmatic decisions):
    ```bash
    python3 scripts/sync_skills.py --json
    ```
2.  **Present the report to the user.** The script outputs a table showing each skill, which tools have it, sync status (in sync / out of sync / single-tool only), and which copy is newest by modification time.
3.  **If out-of-sync skills are found**, ask the user:
    *   Which direction to sync: newest version to all stale locations, or pick a specific source tool.
    *   Which target tools to update (all stale, or a subset).
4.  **On explicit user approval**, copy the chosen source version to each approved target:
    ```bash
    # For each approved target location:
    rm -rf {target_skills_dir}/{skill-name}
    cp -r {source_skills_dir}/{skill-name} {target_skills_dir}/{skill-name}
    ```
    **Never perform this step without user confirmation.**
5.  **Verify** by re-running the sync status reporter to confirm all locations are now in sync:
    ```bash
    python3 scripts/sync_skills.py --skill {skill-name}
    ```

### 3. Skill Discovery (Multi-Source)
**Trigger:** User searches for skills (e.g., "Find a debugging skill" or "Search for React skills").

**Procedure:**
1.  **Discover API Key and Select Source:**
    *   **Step 1 - Environment Variable:** Check `$SKILLSMP_API_KEY`
        ```bash
        printenv SKILLSMP_API_KEY
        ```
        If set and non-empty, use SkillsMP as the primary search source.
        **Note:** Use `printenv` (not `echo $VAR`) — it queries the process environment directly and is more reliable across shell contexts.

    *   **Step 2 - Config File:** Check for `config.json` in this skill's directory
        ```bash
        # Look for config.json in skill directory (path varies by tool)
        cat ~/.claude/skills/universal-skills-manager/config.json 2>/dev/null
        ```
        If `skillsmp_api_key` field has a non-empty value, use SkillsMP as primary source.

    *   **Step 3 - Source Selection:** If no API key found, present the user with a choice:
        > "I don't see a SkillsMP API key configured. You have three options:
        >
        > A) Provide your SkillsMP API key (get one at skillsmp.com) — curated skills with AI semantic search
        >
        > B) Search SkillHub's open catalog — community skills, no API key needed
        >
        > C) Search ClawHub — versioned skills with semantic search, no API key needed
        >
        > Which would you prefer?"

        -   If user chooses **A**: Collect key, **validate it** (see below), store in memory for this session, proceed with SkillsMP
        -   If user chooses **B**: Proceed with SkillHub search (no key needed)
        -   If user chooses **C**: Proceed with ClawHub search (no key needed)

    *   **Key Validation:** SkillsMP API keys always start with `sk_live_skillsmp_`. If the user provides a key that does not match this prefix, reject it immediately:
        > "That doesn't look like a valid SkillsMP API key. Keys start with `sk_live_skillsmp_`. You can get one at https://skillsmp.com — or choose SkillHub/ClawHub search instead (no key needed)."

    *   **Security:** Never log, display, or echo the full API key value.

    **Note for claude.ai/Desktop/ChatGPT users:** Environment variables are not available. Use the "Package for Cloud Upload" capability (Section 5) to create a ZIP with your API key embedded, or provide your key when prompted.

2.  **Execute Search Based on Selected Source:**

    **If using SkillsMP (primary, curated):**
    -   **Choose method:**
        -   **Keyword Search** (`/api/v1/skills/search`): For specific terms, exact matches
        -   **AI Semantic Search** (`/api/v1/skills/ai-search`): For natural language queries (e.g., "help me debug code")
    -   **IMPORTANT:** Always capture the API key into a local variable first, then use it. Direct `$SKILLSMP_API_KEY` expansion in curl can fail in some shell contexts.
    -   **IMPORTANT:** Always include a `User-Agent` header. SkillsMP is behind Cloudflare, which blocks bare curl requests (403 Forbidden).
        ```bash
        # Step 1: Capture key (do this once per session)
        API_KEY=$(printenv SKILLSMP_API_KEY)

        # Step 2: Use ${API_KEY} in curl commands (User-Agent required)
        # Keyword Search
        curl -X GET "https://skillsmp.com/api/v1/skills/search?q={query}&limit=20&sortBy=recent" \
          -H "Authorization: Bearer ${API_KEY}" \
          -H "User-Agent: Universal-Skills-Manager"

        # AI Semantic Search (for natural language queries)
        curl -X GET "https://skillsmp.com/api/v1/skills/ai-search?q={query}" \
          -H "Authorization: Bearer ${API_KEY}" \
          -H "User-Agent: Universal-Skills-Manager"
        ```
    -   **Parse:** Extract from `data.skills[]` (keyword) or `data.data[]` (AI search)
    -   Available fields: `id`, `name`, `author`, `description`, `githubUrl`, `skillUrl`, `stars`, `updatedAt`
    -   **Note:** SkillsMP requires a `q` parameter — there is no browse/list endpoint. However, `q=*` works as a wildcard to surface top skills (combine with `sortBy=stars` for popularity). For dedicated browsing, use SkillHub or ClawHub instead (both support browsing by stars/downloads).

    **If using SkillHub (open catalog, no auth):**
    -   **Execute:**
        ```bash
        # SkillHub Search (no authentication required)
        curl -X GET "https://skills.palebluedot.live/api/skills?q={query}&limit=20" \
          -H "User-Agent: Universal-Skills-Manager"
        ```
    -   **Parse:** Extract from `skills[]` array
    -   Available fields: `id`, `name`, `description`, `githubOwner`, `githubRepo`, `githubStars`, `downloadCount`, `securityScore`
    -   **Note:** SkillHub does not have an AI semantic search — keyword search only

    **If using ClawHub (versioned skills, semantic search, no auth):**
    -   **Choose method:**
        -   **Semantic Search** (`/api/v1/search`): For natural language queries — returns results ranked by vector similarity `score`
        -   **Browse/List** (`/api/v1/skills`): For browsing by popularity, stars, or recency
    -   **Execute:**
        ```bash
        # Semantic Search (vector/similarity search)
        curl -X GET "https://clawhub.ai/api/v1/search?q={query}&limit=20" \
          -H "User-Agent: Universal-Skills-Manager"

        # Browse by stars, downloads, or trending
        curl -X GET "https://clawhub.ai/api/v1/skills?limit=20&sort=stars" \
          -H "User-Agent: Universal-Skills-Manager"
        # Other sort options: sort=downloads, sort=trending, sort=updated
        ```
    -   **Parse:**
        -   Semantic search: Extract from `results[]` array — each has `score`, `slug`, `displayName`, `summary`, `version`, `updatedAt`
        -   Browse: Extract from `items[]` array — each has `slug`, `displayName`, `summary`, `version`, `stats.stars`, `stats.downloads`
    -   **Note:** ClawHub hosts skill files directly (not on GitHub). Use the `slug` field when installing — see Section C.

3.  **Display Results (Unified Format):**
    Display results in a consistent table format regardless of source. Include the **Source** column to indicate origin:

    ```
    | # | Skill | Author | Stars | Source | Description |
    |---|-------|--------|-------|--------|-------------|
    | 1 | debugging-strategies | wshobson | 27,021 | SkillHub | Master systematic debugging... |
    | 2 | code-debugging | AuthorX | 15 | SkillsMP | Systematic debugging methodology... |
    | 3 | self-improving-agent | clawhub-user | 42 | ClawHub | Agent that improves itself... |
    ```

    -   For SkillsMP AI search: Also show relevance score
    -   For SkillHub: Show `securityScore` if available
    -   For ClawHub semantic search: Show similarity `score` if available
    -   Limit to top 10-15 results for readability

4.  **Search More Sources:**
    After displaying results from any source, offer to search the remaining unsearched sources:

    -   **If 2 sources remain:** "Want to also search {source1} or {source2}? Or both?"
    -   **If 1 source remains:** "Want to also search {source}?"

    Available sources: SkillsMP (requires API key), SkillHub (no key), ClawHub (no key)

    If yes:
    -   Query the selected source(s) with the same search terms
    -   **Deduplicate:** Compare results across sources:
        -   SkillsMP ↔ SkillHub: By full skill ID (`{owner}/{repo}/{path}`)
        -   ClawHub ↔ others: By skill name (ClawHub uses slugs, not GitHub paths)
    -   Append unique results to the display, labeled with their source tag

5.  **Offer Installation:**
    -   After displaying results, ask: "Which skill would you like to install?"
    -   For SkillsMP results: Note the skill's `githubUrl` for content fetching
    -   For SkillHub results: Note the skill's `id` for detail fetching (needed to get `skillPath` and `branch`)
    -   For ClawHub results: Note the skill's `slug` for direct file fetching via ClawHub's `/file` endpoint

### 4. Skill Matrix Report
**Trigger:** User asks for skill report/overview (e.g., "Show my skills", "What skills do I have?", "Skill report", "Compare my tools").

**Procedure:**
1.  **Detect Installed Tools:**
    Check which AI tools are installed by verifying their user-level skills directories exist:
    ```bash
    # Check each tool's skills directory
    ls -d ~/.claude/skills 2>/dev/null && echo "Claude: ✓"
    ls -d ~/.agents/skills 2>/dev/null && echo "Gemini CLI / Codex: ✓"
    ls -d ~/.gemini/antigravity/skills 2>/dev/null && echo "Antigravity: ✓"
    ls -d ~/.openclaw/workspace/skills 2>/dev/null && echo "OpenClaw: ✓"
    ls -d ~/.cc-claw/workspace/skills 2>/dev/null && echo "CC-Claw: ✓"
    ls -d ~/.cursor/skills 2>/dev/null && echo "Cursor: ✓"
    ls -d ~/.config/opencode/skills 2>/dev/null && echo "OpenCode: ✓"
    ls -d ~/.roo/skills 2>/dev/null && echo "Roo: ✓"
    ls -d ~/.config/goose/skills 2>/dev/null && echo "Goose: ✓"
    ls -d ~/.cline/skills 2>/dev/null && echo "Cline: ✓"
    ```

2.  **Collect All Skills:**
    For each detected tool, list skill folders:
    ```bash
    find ~/.{claude,agents,gemini/antigravity,openclaw/workspace,cc-claw/workspace,cursor,config/opencode,config/goose,roo,cline}/skills -maxdepth 1 -type d 2>/dev/null | \
      xargs -I{} basename {} | sort -u
    ```

3.  **Generate Matrix Table:**
    Create a markdown table where:
    - **Rows** = skill names (deduplicated across all tools)
    - **Columns** = only tools that are installed on the system
    - **Cells** = ✅ (installed) or ❌ (not installed)

    Example output:
    ```
    | Skill | Claude | Gemini/Codex | Cursor |
    |-------|--------|--------------|--------|
    | humanizer | ✅ | ❌ | ✅ |
    | skill-creator | ❌ | ✅ | ❌ |
    | using-superpowers | ✅ | ✅ | ✅ |
    ```

4.  **Show Summary:**
    - Total skills across all tools
    - Skills unique to one tool
    - Skills installed everywhere

### 5. Package for Cloud Upload (claude.ai / Claude Desktop / ChatGPT)

**Trigger:** User wants to use this skill in claude.ai, Claude Desktop, or ChatGPT (e.g., "Package this for claude.ai", "Create a ZIP for Claude Desktop", "Package for ChatGPT", "I want to upload this skill to claude.ai", "Prepare skill for web upload", "Package this for chatgpt.com").

**Procedure:**
1.  **Explain the Process:**
    "I'll create a ZIP file with this skill ready for upload to claude.ai, Claude Desktop, or ChatGPT. Since cloud environments don't have access to your local environment variables, I can optionally embed your API key in the package. Note: the API key is optional — SkillHub and ClawHub search work without one."

2.  **Validate Frontmatter Compatibility (CRITICAL — do this BEFORE packaging):**
    Run `validate_frontmatter.py` to check the SKILL.md against the Agent Skills spec (used by both claude.ai/Claude Desktop and ChatGPT):
    ```bash
    # Validate only (report issues)
    python3 scripts/validate_frontmatter.py /path/to/SKILL.md

    # Validate and auto-fix (overwrites file)
    python3 scripts/validate_frontmatter.py /path/to/SKILL.md --fix

    # Validate a ZIP file
    python3 scripts/validate_frontmatter.py /path/to/skill.zip --fix
    ```
    The script checks for unsupported top-level keys, nested metadata, non-string metadata values, and field length violations. With `--fix`, it automatically moves unsupported keys into `metadata`, flattens nested objects, and converts values to strings. Tell the user what was fixed. See Operational Rule 5 for the full spec.

3.  **Collect API Key (Optional):**
    *   Ask: "Would you like to include your SkillsMP API key for curated search? This is optional — SkillHub and ClawHub work without a key. If you skip this, the packaged skill will still work for SkillHub and ClawHub searches."
    *   If user wants to include a key:
        -   Ask: "Please provide your SkillsMP API key. You can get one at https://skillsmp.com"
        -   Wait for user to provide the key
        -   **Validate:** Key must start with `sk_live_skillsmp_`. If invalid, reject and re-prompt or offer to skip.
        -   **Security:** Do not echo or display the key back to the user
    *   If user skips, create the ZIP without `config.json`
    *   **Credential safety warning (IMPORTANT — always display this if a key is included):**
        > "**Security note:** This ZIP will contain your API key in plain text. Please follow these precautions:
        > - **Do NOT share** this ZIP publicly, post it online, or commit it to version control
        > - **Do NOT distribute** this ZIP to others — each user should package their own
        > - **Use a scoped/least-privilege key** if your provider supports it
        > - **Rotate your key** if you suspect the ZIP was exposed
        > - The key is stored locally in `config.json` inside the ZIP and is only used at runtime to authenticate with the SkillsMP API"

4.  **Create Package Contents:**
    *   Create a temporary directory structure:
        ```
        universal-skills-manager/
        ├── SKILL.md          # Copy from current skill
        ├── config.json       # Create with embedded API key
        └── scripts/
            └── install_skill.py  # Copy from current skill
        ```
    *   Generate `config.json` with the user's API key:
        ```json
        {
          "skillsmp_api_key": "USER_PROVIDED_KEY_HERE"
        }
        ```

5.  **Create ZIP File:**
    *   Use Python to create the ZIP:
        ```python
        import zipfile
        import json
        import tempfile
        from pathlib import Path
        
        # Create ZIP in user's Downloads or current directory
        zip_path = Path.home() / "Downloads" / "universal-skills-manager.zip"
        skill_dir = Path("~/.claude/skills/universal-skills-manager").expanduser()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Copy skill files
            for file_path in skill_dir.rglob('*'):
                if file_path.is_file() and file_path.name != 'config.json':
                    rel_path = file_path.relative_to(skill_dir)
                    dest = temp_path / rel_path
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(file_path.read_bytes())
            
            # Create config.json with API key
            config = {"skillsmp_api_key": "USER_API_KEY"}
            (temp_path / "config.json").write_text(json.dumps(config, indent=2))
            
            # Create ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path in temp_path.rglob('*'):
                    if file_path.is_file():
                        arcname = f"universal-skills-manager/{file_path.relative_to(temp_path)}"
                        zf.write(file_path, arcname)
        ```
    *   Alternatively, provide the ZIP as a downloadable artifact

6.  **Provide Upload Instructions:**
    *   "Your skill package is ready! To use it:"
    *   **For claude.ai / Claude Desktop:**
        *   "1. Download the ZIP file"
        *   "2. Go to Settings → Capabilities"
        *   "3. Click 'Upload skill' in the Skills section"
        *   "4. Select the ZIP file and upload"
        *   "5. Enable the skill and start using it!"
    *   **For ChatGPT:**
        *   "1. Download the ZIP file"
        *   "2. Click your profile icon and select Skills (or go to chatgpt.com/skills)"
        *   "3. Click 'New skill'"
        *   "4. Select 'Upload from your computer'"
        *   "5. Select the ZIP file and upload"
        *   "6. The skill is now installed and ChatGPT will use it when relevant!"

7.  **Security Reminder:**
    *   If a key was embedded: "This ZIP contains your API key. Do NOT share it publicly, distribute it to others, or commit it to version control. If you need to share the skill, create a key-free version (without `config.json`) and let each user add their own key."
    *   If no key was embedded: "This ZIP is safe to share — it contains no credentials. Recipients can add their own API key later, or use SkillHub/ClawHub search which requires no key."

## Operational Rules

1.  **Structure Integrity:** When installing, always ensure the skill has its own folder (e.g., `.../skills/my-skill/`). Do not dump loose files into the root skills directory. Always run `mkdir -p` on the target path before copying files.
2.  **Conflict Safety:** If a skill already exists at a target location, **always** ask before overwriting, unless the user explicitly requested a "Force Sync."
3.  **Sync Safety:** The `sync_skills.py` script is read-only — it only reports status and never modifies files. All write operations (copy, overwrite, deploy, delete) are performed by the agent and require explicit user approval before execution. No sync action is ever taken autonomously.
4.  **User-Agent Required:** Always include `-H "User-Agent: Universal-Skills-Manager"` in all curl requests. APIs behind Cloudflare (like SkillsMP) return 403 Forbidden for bare curl requests without a User-Agent header.
5.  **OpenClaw Note:** OpenClaw may require a restart to pick up new skills if `skills.load.watch` is not enabled in `openclaw.json`. Warn the user of this after installation.
6.  **Cross-Platform Adaptation:**
    *   Gemini uses `SKILL.md`.
    *   Cline uses the same `SKILL.md` format with `name` and `description` frontmatter. The `name` field must match the directory name. No manifest generation required. Note: Cline also reads `.claude/skills/` at the project level, so Claude Code project skills work in Cline automatically.
    *   If OpenCode or Anti-Gravity require a specific manifest (e.g., `manifest.json`), generate a basic one based on the `SKILL.md` frontmatter during installation.
7.  **Cloud Platform Frontmatter Compatibility Check (claude.ai / Claude Desktop / ChatGPT):**
    When a user wants to upload or package a skill for **claude.ai**, **Claude Desktop**, or **ChatGPT**, validate the SKILL.md frontmatter against the [Agent Skills specification](https://agentskills.io/specification). All three platforms use strict frontmatter validation that rejects ambiguous YAML constructs like block scalars. Non-compliant skills will be rejected with "malformed YAML frontmatter" or "unexpected key" errors.

    **Allowed top-level frontmatter fields (Agent Skills spec):**

    | Field | Required | Constraints |
    | :--- | :--- | :--- |
    | `name` | Yes | Max 64 chars, lowercase letters/numbers/hyphens only, must match directory name |
    | `description` | Yes | Max 1024 chars. No angle brackets (`<` or `>`). Avoid literal block scalars (`\|`) — known to fail with blank lines. Folded scalars (`>`) work but inline strings are safest |
    | `license` | No | License name or reference to bundled file |
    | `compatibility` | No | Max 500 chars, environment requirements |
    | `metadata` | No | Flat key-value pairs only (string keys to string values — no nested objects, no arrays) |
    | `allowed-tools` | No | Space-delimited list of pre-approved tools (experimental) |

    **Use the validation script (preferred — avoids manual YAML errors):**
    ```bash
    # Validate a SKILL.md
    python3 scripts/validate_frontmatter.py /path/to/SKILL.md

    # Validate and auto-fix in place
    python3 scripts/validate_frontmatter.py /path/to/SKILL.md --fix

    # Validate and fix a ZIP file (rewrites SKILL.md inside the ZIP)
    python3 scripts/validate_frontmatter.py /path/to/skill.zip --fix
    ```
    The script (`scripts/validate_frontmatter.py`) is zero-dependency Python 3. It checks all constraints and with `--fix` automatically applies these corrections:
    -   Moves unsupported top-level keys (e.g., `version`, `author`, `homepage`, `category`) into `metadata` as string values
    -   Flattens nested `metadata` objects (e.g., `metadata.clawdbot.requires.bins: [x, y]` → `metadata.clawdbot-requires-bins: "x, y"`)
    -   Converts non-string metadata values to quoted strings (e.g., `true` → `"true"`)
    -   Collapses literal block scalar (`|`) descriptions to inline quoted strings (known to fail with blank lines). Folded scalars (`>`) trigger a warning but work in current Claude Desktop
    -   Strips angle brackets (`<` `>`) from description (Anthropic's validator rejects them)
    -   Converts YAML list-format `allowed-tools` to space-delimited string
    -   Truncates `description` if over 1024 chars
    -   Validates the fix and reports if any issues remain

    **If the script is not available**, do the validation manually:
    1.  Read the SKILL.md frontmatter
    2.  Check all top-level keys are in the allowed set: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`
    3.  If `metadata` is present, verify all values are strings (no nested objects or arrays)
    4.  Verify `name` is lowercase with hyphens only, max 64 chars
    5.  Verify `description` is max 1024 chars

    **If validation fails**, tell the user exactly what's wrong and offer to fix it (run the script with `--fix`, or apply the fixes manually).

## Available Tools
- `bash` (curl): Make API calls to SkillsMP.com, SkillHub (skills.palebluedot.live), and ClawHub (clawhub.ai); fetch skill content from GitHub or ClawHub directly.
- `web_fetch`: Fetch skill content from GitHub raw URLs, SkillHub API, or ClawHub API (alternative to curl).
- `read_file` / `write_file`: Manage local skill files.
- `glob`: Find existing skills in local directories.

## Implementation Details

### Skill Structure
Skills typically contain:
- **SKILL.md** (required): Main instructions with frontmatter.
- **Reference docs**: Additional documentation files.
- **Scripts**: Helper scripts (Python, shell, etc.).
- **Config files**: JSON, YAML configurations.

### Installation Logic

#### A. Installing from SkillsMP API
1.  **Fetch Skill Content:**
    -   Convert `githubUrl` to raw content URL:
        ```
        Input:  https://github.com/{user}/{repo}/tree/{branch}/{path}
        Output: https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}/SKILL.md
        ```
    -   Fetch the SKILL.md content using curl or web_fetch

2.  **Create Directory:**
    -   Use skill `name` from API response for directory: `.../skills/{skill-name}/`
    -   Example: `.../skills/code-debugging/`

3.  **Save SKILL.md:**
    -   Write the fetched content to `SKILL.md` in the new directory
    -   Preserve the original YAML frontmatter and content

4.  **Handle Additional Files (Optional):**
    -   Check if GitHub repo has additional files (reference docs, scripts)
    -   Optionally fetch and save them to maintain complete skill package

5.  **Confirm:**
    -   Report: "Installed '{name}' by {author} to {path}"
    -   Show GitHub URL and stars count
    -   Offer sync to other AI tools

#### B. Installing from SkillHub
1.  **Fetch Skill Details:**
    -   Use the skill's `id` from the search result to get full details:
        ```bash
        curl -X GET "https://skills.palebluedot.live/api/skills/{id}"
        ```
    -   **IMPORTANT:** The `id` field (e.g., `wshobson/agents/debugging-strategies`) does NOT map to the file path within the repo. You MUST use the detail endpoint to get the actual `skillPath` and `branch`.
    -   Extract from response: `githubOwner`, `githubRepo`, `branch`, `skillPath`

2.  **Construct GitHub URL:**
    -   Build the GitHub tree URL from the detail response:
        ```
        https://github.com/{githubOwner}/{githubRepo}/tree/{branch}/{skillPath}
        ```
    -   Example: `https://github.com/wshobson/agents/tree/main/plugins/developer-essentials/skills/debugging-strategies`

3.  **Download Using Helper Script:**
    -   From this point, the flow is identical to SkillsMP installation:
        ```bash
        python3 ~/.claude/skills/universal-skills-manager/scripts/install_skill.py \
          --url "https://github.com/{githubOwner}/{githubRepo}/tree/{branch}/{skillPath}" \
          --dest "{target-path}"
        ```

4.  **Confirm:**
    -   Report: "Installed '{name}' from SkillHub to {path}"
    -   Show GitHub URL and stars count
    -   Offer sync to other AI tools

#### C. Installing from ClawHub
ClawHub hosts skill files directly (not on GitHub), so the install flow bypasses `install_skill.py` and fetches content via ClawHub's API.

1.  **Fetch SKILL.md Content:**
    -   Use ClawHub's file endpoint to get the raw SKILL.md:
        ```bash
        curl -s "https://clawhub.ai/api/v1/skills/{slug}/file?path=SKILL.md" \
          -H "User-Agent: Universal-Skills-Manager" \
          -o /tmp/clawhub-{slug}/SKILL.md
        ```
    -   **IMPORTANT:** This endpoint returns raw `text/plain` content, NOT JSON. Save the response body directly as the file.
    -   The `x-content-sha256` response header can be used to verify file integrity.

2.  **Handle Multi-File Skills (if applicable):**
    -   If the skill has additional files (scripts, configs), use ClawHub's download endpoint:
        ```bash
        curl -s "https://clawhub.ai/api/v1/download?slug={slug}" \
          -H "User-Agent: Universal-Skills-Manager" \
          -o /tmp/clawhub-{slug}.zip
        unzip -o /tmp/clawhub-{slug}.zip -d /tmp/clawhub-{slug}/
        ```
    -   To check if a skill has multiple files, inspect the detail response from `GET /api/v1/skills/{slug}` — the `latestVersion` object may indicate file count.

3.  **Run Security Scan:**
    -   Since `install_skill.py` is bypassed, run the security scanner manually:
        ```bash
        python3 ~/.claude/skills/universal-skills-manager/scripts/scan_skill.py /tmp/clawhub-{slug}/
        ```
    -   Review any findings before proceeding. ClawHub has VirusTotal integration but our scan provides an additional layer.

4.  **Validate YAML Frontmatter:**
    -   Verify the SKILL.md has valid YAML frontmatter (name, description fields).
    -   If invalid, warn the user and ask whether to proceed.

5.  **Create Directory and Install:**
    -   Create the target directory: `.../skills/{slug}/`
    -   Copy all files from the temp directory to the destination:
        ```bash
        mkdir -p {target-path}/{slug}
        cp -r /tmp/clawhub-{slug}/* {target-path}/{slug}/
        ```

6.  **Confirm:**
    -   Report: "Installed '{displayName}' (v{version}) from ClawHub to {path}"
    -   Show version info and stars count
    -   Offer sync to other AI tools

7.  **Cleanup:**
    -   Remove the temporary directory:
        ```bash
        rm -rf /tmp/clawhub-{slug}/ /tmp/clawhub-{slug}.zip
        ```

#### D. Installing from Local Source (Sync/Copy)
This flow applies when syncing a skill from one local tool directory to another (e.g., after the sync status reporter identifies out-of-sync locations).

1.  **Identify source and targets:** Use the sync status report (`python3 scripts/sync_skills.py`) to determine which tool has the newest version and which are stale or missing the skill.
2.  **Confirm with the user:** Present the proposed copy operations and get explicit approval. Example: "Copy 'code-review' from Claude Code (~/.claude/skills/code-review) to Gemini CLI / Codex (~/.agents/skills/code-review) and OpenCode (~/.config/opencode/skills/code-review)?"
3.  **Create directory:** `mkdir -p {target_skills_dir}/{skill-name}`
4.  **Copy all files** from the source to the target, preserving filenames:
    ```bash
    rm -rf {target_skills_dir}/{skill-name}
    cp -r {source_skills_dir}/{skill-name} {target_skills_dir}/{skill-name}
    ```
5.  **Verify:** Re-run `python3 scripts/sync_skills.py --skill {skill-name}` to confirm all locations are now in sync.
6.  **Handle missing skills:** If a skill exists in some tools but not others, ask the user whether to deploy it to additional tools or leave it as-is.

### SkillsMP API Configuration

**Base URL:** `https://skillsmp.com/api/v1`

**Authentication:**
```bash
Authorization: Bearer $SKILLSMP_API_KEY
```

**Available Endpoints:**
- `GET /api/v1/skills/search?q={query}&page={1}&limit={20}&sortBy={recent|stars}`
- `GET /api/v1/skills/ai-search?q={query}`

**Response Format (Keyword Search):**
```json
{
  "success": true,
  "data": {
    "skills": [
      {
        "id": "...",
        "name": "skill-name",
        "author": "AuthorName",
        "description": "...",
        "githubUrl": "https://github.com/user/repo/tree/main/path",
        "skillUrl": "https://skillsmp.com/skills/...",
        "stars": 10,
        "updatedAt": 1768838561
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 3601,
      "totalPages": 1801,
      "hasNext": true
    }
  }
}
```

**Response Format (AI Search):**
```json
{
  "success": true,
  "data": {
    "search_query": "...",
    "data": [
      {
        "file_id": "...",
        "filename": "...",
        "score": 0.656,
        "skill": {
          "id": "...",
          "name": "...",
          "author": "...",
          "description": "...",
          "githubUrl": "...",
          "skillUrl": "...",
          "stars": 0,
          "updatedAt": 1769542668
        }
      }
    ]
  }
}
```

**Error Handling:**
- `401`: Invalid or missing API key
- `400`: Missing required query parameter
- `500`: Internal server error

### SkillHub API Configuration

**Base URL:** `https://skills.palebluedot.live/api`

**Authentication:** None required (open API)

**Available Endpoints:**
- `GET /api/skills?q={query}&limit={20}` — Search skills by keyword
- `GET /api/skills/{id}` — Get full skill details (includes `skillPath`, `branch`, `rawContent`)
- `GET /api/categories` — List skill categories
- `GET /api/health` — Health check

**Search Response Format:**
```json
{
  "skills": [
    {
      "id": "wshobson/agents/debugging-strategies",
      "name": "debugging-strategies",
      "description": "Master systematic debugging...",
      "githubOwner": "wshobson",
      "githubRepo": "agents",
      "githubStars": 27021,
      "downloadCount": 0,
      "securityScore": 100,
      "securityStatus": null,
      "rating": 0,
      "isVerified": false,
      "compatibility": { "platforms": [] }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 1000,
    "totalPages": 50
  },
  "searchEngine": "meilisearch",
  "processingTimeMs": 10
}
```

**Detail Response Format (GET /api/skills/{id}):**
```json
{
  "id": "wshobson/agents/debugging-strategies",
  "name": "debugging-strategies",
  "description": "...",
  "githubOwner": "wshobson",
  "githubRepo": "agents",
  "skillPath": "plugins/developer-essentials/skills/debugging-strategies",
  "branch": "main",
  "githubStars": 27021,
  "rawContent": "---\nname: debugging-strategies\n..."
}
```

**Key Fields for Installation:**
- `skillPath`: The actual directory path within the GitHub repo (CRITICAL — the `id` does NOT match the file path)
- `branch`: The branch name (e.g., `main`)
- `githubOwner` + `githubRepo`: Used to construct the GitHub URL
- `rawContent`: Full SKILL.md content (can be used as fallback if GitHub is unreachable)

**Error Handling:**
- `404`: Skill not found
- `500`: Internal server error

### ClawHub API Configuration

**Base URL:** `https://clawhub.ai/api/v1`

**Authentication:** None required (open API)

**Rate Limits:** 120 reads/min per IP (shown in `x-ratelimit-remaining` and `x-ratelimit-reset` response headers)

**Available Endpoints:**
- `GET /api/v1/search?q={query}&limit={20}` — Semantic/vector search (ranked by similarity score)
- `GET /api/v1/skills?limit={20}&sort={stars|downloads|updated|trending}&cursor={cursor}` — Browse/list with cursor pagination
- `GET /api/v1/skills/{slug}` — Get full skill details (owner, version, moderation status)
- `GET /api/v1/skills/{slug}/file?path={filepath}&version={ver}` — Get raw file content (text/plain, NOT JSON)
- `GET /api/v1/download?slug={slug}&version={ver}` — Download full skill as ZIP

**Search Response Format (GET /api/v1/search):**
```json
{
  "results": [
    {
      "score": 0.82,
      "slug": "self-improving-agent",
      "displayName": "Self-Improving Agent",
      "summary": "An agent that iteratively improves itself...",
      "version": "1.0.0",
      "updatedAt": "2026-01-15T10:30:00Z"
    }
  ]
}
```

**Browse Response Format (GET /api/v1/skills):**
```json
{
  "items": [
    {
      "slug": "self-improving-agent",
      "displayName": "Self-Improving Agent",
      "summary": "...",
      "version": "1.0.0",
      "stats": {
        "stars": 42,
        "downloads": 150
      }
    }
  ],
  "nextCursor": "eyJ..."
}
```

**Detail Response Format (GET /api/v1/skills/{slug}):**
```json
{
  "skill": {
    "slug": "self-improving-agent",
    "displayName": "Self-Improving Agent",
    "summary": "...",
    "version": "1.0.0"
  },
  "owner": {
    "handle": "username",
    "displayName": "User Name"
  },
  "latestVersion": "1.0.0",
  "moderation": "approved"
}
```

**File Endpoint (GET /api/v1/skills/{slug}/file?path=SKILL.md):**
- Returns raw `text/plain` content (NOT JSON)
- Response headers include `x-content-sha256` (integrity hash) and `x-content-size` (byte count)
- Use `version` query param to fetch a specific version (defaults to latest)

**Key Differences from SkillsMP/SkillHub:**
- **Direct hosting:** ClawHub hosts skill files directly — no GitHub URL construction needed
- **Versioned skills:** Each skill has explicit version numbers; use `version` param to pin
- **Slug-based IDs:** Skills are identified by `slug` (e.g., `self-improving-agent`), not GitHub paths
- **Semantic search built-in:** The `/search` endpoint uses vector similarity, not keyword matching
- **VirusTotal integration:** ClawHub scans skills via VirusTotal partnership; `moderation` field indicates status

**Error Handling:**
- `404`: Skill or file not found
- `429`: Rate limit exceeded (120 reads/min)
- `500`: Internal server error

### Guidelines
-   **Multi-Source Search:** Use SkillsMP as the primary source when an API key is available. Offer SkillHub and ClawHub as alternative or additional sources.
-   **Prefer AI/Semantic Search:** For natural language queries, use SkillsMP `/ai-search` or ClawHub `/search` (both support semantic matching). SkillHub only supports keyword search.
-   **Source Labeling:** Always label results with their source (`[SkillsMP]`, `[SkillHub]`, or `[ClawHub]`) so users can distinguish between sources.
-   **SkillHub Detail Lookup:** When installing from SkillHub, always fetch the detail endpoint first to get the correct `skillPath` and `branch`. Never try to parse the `id` field as a file path.
-   **ClawHub Direct Hosting:** ClawHub hosts skill files directly — use the `/file` endpoint to fetch content. No GitHub URL construction is needed. Use the `slug` field as the skill identifier.
-   **ClawHub Versioning:** ClawHub skills have explicit version numbers. Show the version in install confirmations. Use the `version` query param to pin a specific version if needed.
-   **Deduplication:** When showing results from multiple sources, deduplicate: SkillsMP ↔ SkillHub by full skill ID (`{owner}/{repo}/{path}`); ClawHub ↔ others by skill name (since ClawHub uses slugs, not GitHub paths).
-   **Verify Content:** After fetching from any source, verify the SKILL.md has valid YAML frontmatter.
-   **Structure Integrity:** Maintain the `.../skills/{skill-name}/SKILL.md` structure.
-   **Syncing:** After installing a skill, offer to sync (copy) it to other detected AI tools.
-   **GitHub URLs:** For SkillsMP/SkillHub installs, always convert tree URLs to raw.githubusercontent.com URLs for content fetching.
-   **Security:** Security scanning runs on all installs regardless of source (SkillsMP, SkillHub, or ClawHub). SkillHub's `securityScore` and ClawHub's VirusTotal `moderation` status are informational only — our own `scan_skill.py` at install time is authoritative.