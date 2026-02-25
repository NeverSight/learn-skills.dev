---
name: skill-finder
description: Proactively discover, install, and create Claude skills for specialized tasks. AUTOMATICALLY activates when encountering niche domains, unfamiliar APIs, specialized knowledge areas, or when user expresses wanting to learn/know something new. Searches the community registry at claude-plugins.dev and auto-installs matching skills. Creates new skills when no match exists. Use when user says "I want to know...", "help me with [specialized domain]", or when you recognize a task requires specialized expertise you don't have.
---

# Skill Finder

Dynamically discover, install, and create skills to expand Claude's capabilities on-demand.

## When to Activate

**PROACTIVELY** use this skill when:

1. **User requests new capability**
   - "I want to know kung-fu"
   - "Help me learn about [topic]"
   - "I need to work with [unfamiliar technology]"

2. **Specialized domain encountered**
   - Niche APIs (NFT marketplaces, proprietary systems)
   - Domain-specific formats/protocols
   - Industry-specific tooling

3. **Knowledge gap recognized**
   - Task requires expertise you're uncertain about
   - Unfamiliar tools, frameworks, or services
   - User asks about something highly specialized

4. **Recurring specialized need**
   - Pattern suggests ongoing work in specialized area
   - Multiple related requests in same domain

**DO NOT activate for:**
- General programming tasks (algorithms, data structures)
- Common frameworks (React, Express, Django) - base model handles these
- One-off simple queries
- Tasks you can handle confidently

## Instructions

### Phase 1: Extract Search Keywords

Interpret the user's request and extract relevant search terms:

- "I want to know kung-fu" → search: `martial arts combat self-defense`
- "Help with Stripe billing" → search: `stripe payments billing api`
- "Work with NFTs on OpenSea" → search: `opensea nft marketplace api`

Use multiple related keywords to maximize match potential.

### Phase 2: Search the Registry

Query the skills API:

```
https://claude-plugins.dev/api/skills?q=<keywords>
```

Use WebFetch to retrieve results. The API returns:

```json
{
  "skills": [{
    "name": "skill-name",
    "namespace": "@author/repo/skill-name",
    "description": "What the skill does...",
    "stars": 12345,
    "installs": 678,
    "metadata": {
      "rawFileUrl": "https://raw.githubusercontent.com/..."
    }
  }],
  "total": 100
}
```

### Phase 3: Evaluate Results

Rank by:
1. **Relevance** - Does description match the actual need?
2. **Quality** - Star count as credibility signal:
   - > 1000 stars: High confidence
   - > 100 stars: Moderate confidence
   - < 100 stars: Review carefully
3. **Specificity** - Prefer targeted skills over broad ones

**Credible match criteria:**
- Description clearly addresses the task
- AND (stars > 500 OR installs > 50)
- No obvious security concerns

### Phase 4a: Auto-Install (if credible match found)

Run the install command:

```bash
npx claude-plugins skills install <namespace> --local
```

Where `<namespace>` is the full namespace from the API (e.g., `@anthropics/claude-code/frontend-design`).

The `--local` flag installs to the project's `.claude/skills/` directory.

After installation, inform the user:

> I've learned `<skill-name>` - [brief description of capability]. Let me apply this to your task.

Then immediately use the new skill to address the user's original request.

### Phase 4b: Create Skill (if no credible match)

**Only create a skill if:**
- No good matches in the registry
- Task is genuinely specialized (not just complex)
- Would provide reusable capability for this domain
- Base Claude genuinely needs augmentation

**Do NOT create if:**
- Task is complex but not specialized
- One-off operation unlikely to recur
- Base model can handle it reasonably
- Similar capability already exists locally

**Creation process:**

1. **Research the domain**
   - Use WebSearch to understand the technology/domain
   - Read official documentation
   - Identify key concepts, APIs, patterns

2. **Design the skill**
   - Determine what instructions Claude needs
   - Identify any scripts or references required
   - Plan the skill structure

3. **Create the skill files**

   Create directory: `.claude/skills/<skill-name>/`

   Create `SKILL.md` with:
   ```yaml
   ---
   name: skill-name
   description: Clear description of what it does and when to use it.
   ---
   ```

   Add body with:
   - When to use
   - Step-by-step instructions
   - Examples
   - Any required setup

4. **Add supporting files if needed**
   - `scripts/` for automation
   - `references/` for documentation
   - `templates/` for boilerplate

5. **Inform the user**

> I've created a custom skill for [domain] based on my research. I can now [list capabilities]. Let me help with your task.

## Examples

### Example 1: Skill exists in registry

```
User: "I want to build beautiful frontend interfaces"

Claude thinking:
- This is a specialized design skill request
- Search: "frontend design ui interface"
- Found: frontend-design with 45k stars
- High relevance + high quality = credible match

Claude action:
npx claude-plugins skills install @anthropics/claude-code/frontend-design --local

Claude response:
"I've learned frontend-design - expertise in creating distinctive, production-grade interfaces. Let me help you build something beautiful..."
```

### Example 2: Proactive discovery

```
User: "Help me integrate OpenSea's API to list NFTs"

Claude thinking:
- NFT marketplace API = specialized domain
- I should check for existing skills
- Search: "opensea nft api marketplace"
- Found: opensea-api with good ratings

Claude action:
npx claude-plugins skills install @creator/skills/opensea-api --local

Claude response:
"I've equipped myself with OpenSea API expertise. I can now help you authenticate, list items, fetch collections, and handle marketplace transactions. Let's set up your NFT listing..."
```

### Example 3: No match - create skill

```
User: "I need to work with Acme Corp's proprietary data format"

Claude thinking:
- Very specialized/proprietary domain
- Search: "acme corp data format"
- No credible matches found
- This is genuinely specialized, not just complex
- User likely needs this repeatedly
- I should create a skill

Claude action:
1. WebSearch for Acme Corp documentation
2. Research the data format specification
3. Create .claude/skills/acme-data-handler/SKILL.md

Claude response:
"I've created a custom skill for Acme Corp data formats based on their documentation. I can now parse, validate, and transform Acme data files. Let me help with your specific task..."
```

### Example 4: Don't over-activate

```
User: "Write a binary search implementation"

Claude thinking:
- This is a standard algorithm
- Base model handles this perfectly
- Not specialized, just programming
- No skill needed

Claude action:
Proceed directly with the task without skill search.
```

## Troubleshooting

### npx command fails

If `npx claude-plugins` isn't available, fall back to manual installation:

1. Fetch the skill's `rawFileUrl` from the API response
2. Use WebFetch to get the SKILL.md content
3. Check for references to scripts/ or other files
4. Manually create the skill directory and files in `.claude/skills/`

### No search results

1. Try broader keywords
2. Try synonyms or related terms
3. If still no results, consider creating a custom skill

### Multiple good matches

Prefer:
1. Higher star count
2. More specific description
3. More recent updates (check `updatedAt`)

Install the best match and mention alternatives exist if user wants different approach.

## Quality Checklist

Before auto-installing, verify:
- [ ] Description clearly matches user's need
- [ ] No security red flags in description
- [ ] Reasonable popularity (stars/installs)
- [ ] Source is from GitHub (trusted platform)

Before creating a skill, verify:
- [ ] No existing skill covers this
- [ ] Task is genuinely specialized
- [ ] Skill would be reusable
- [ ] I have enough information to create useful instructions
