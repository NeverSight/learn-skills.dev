---
name: self-improvement
description: Patterns for AI agents to improve themselves. Learned from actionbook and accomplish-ai. Auto-install tools, create skills, maintain systems.
---

# Self-Improvement Patterns for AI Agents

Patterns learned from studying actionbook and accomplish-ai repositories.

## Core Principles

### 1. Token Efficiency is Critical

| Approach | Tokens | Cost |
|----------|--------|------|
| Full HTML page | 50,000 | $$$ |
| Relevant DOM only | 500 | $ |
| **Savings: 100x** | | |

**Apply to everything:**
- Don't read entire files when you only need a section
- Use semantic search (QMD) instead of grep through everything
- Batch related operations

### 2. Pre-compute > Runtime Guess

Actionbook's key insight:
- Pre-compute DOM selectors → Store as "action manuals"
- Agent looks up manual → Knows exactly what to do
- No guessing, no hallucination

**Apply to your work:**
- Cache frequently used patterns
- Store configurations, not just code
- Build "manuals" for complex operations

### 3. Layered Architecture

From Accomplish:
```
packages/shared/   ← Types, constants (no dependencies)
packages/core/     ← Business logic (depends on shared)
apps/desktop/      ← UI/Electron (depends on core)
```

**Apply to skills:**
- Core utilities → Reusable across skills
- Skill logic → Specific implementations
- Integration → How it connects to OpenClaw

### 4. Secure by Default

From Accomplish:
- API keys: AES-256-GCM encryption
- User approves every action
- Logs for everything
- Sandbox file access

**Apply immediately:**
- Never log API keys (even in git history)
- Ask before destructive operations
- Use .gitignore for sensitive files

### 5. Self-Healing Systems

From disaster recovery:
- External monitoring (not internal)
- Automated backups
- Clear recovery procedures
- Test the recovery process

**Apply to yourself:**
- Healthchecks for critical services
- Auto-backup configurations
- Document how to restore

## Proactive Behaviors

### What to Do Without Being Asked

1. **Monitor your dependencies**
   ```bash
   npm outdated -g
   brew outdated
   ```

2. **Check system health**
   - Disk space
   - Memory usage
   - Running processes

3. **Maintain your skills**
   - Update stale documentation
   - Fix broken references
   - Add new patterns learned

4. **Optimize token usage**
   - Consolidate similar skills
   - Remove duplicate content
   - Archive unused files

5. **Secure your environment**
   - Review .gitignore
   - Check for exposed secrets
   - Update dependencies with vulnerabilities

## Skill Creation Pattern

When you learn something new:

```
1. Identify the pattern
   "This could be a skill"

2. Extract the essence
   What's the core value?
   What's reusable?

3. Create SKILL.md
   - name
   - description (when to use)
   - installation
   - usage examples
   - anti-patterns (when NOT to use)

4. Test it
   Does it work?
   Is it helpful?

5. Publish it
   GitHub repo
   Clear README
   Version tracking
```

## Best Practices from Studied Projects

### From Actionbook

| Pattern | Implementation |
|---------|----------------|
| CLI-first | Works with any AI agent |
| Token savings | Pre-computed selectors |
| Resilient | Maintained action manuals |
| Universal | Any LLM + any framework |

### From Accomplish

| Pattern | Implementation |
|---------|----------------|
| Local-first | Your data on your machine |
| BYO API | No vendor lock-in |
| Open source | MIT, forkable |
| Action-oriented | Does things, not just chats |

## Self-Installation Checklist

When you discover a useful tool:

- [ ] Is it safe? (Check for malicious code)
- [ ] Is it maintained? (Recent commits)
- [ ] Is it free/open source?
- [ ] Does it fill a gap you have?
- [ ] Can you create a skill for it?
- [ ] Should you share it with others?

## Metrics to Track

Monitor your own effectiveness:

| Metric | Target |
|--------|--------|
| Token usage per task | Minimize |
| Successful operations | Maximize |
| Skills created | Grow over time |
| Skills used | Active, not dormant |
| Security incidents | Zero |

## Continuous Learning

1. **Study open source projects** weekly
2. **Extract patterns** that improve your work
3. **Create skills** from learnings
4. **Share** what works
5. **Iterate** based on usage

## References

- Actionbook: https://github.com/actionbook/actionbook
- Accomplish: https://github.com/accomplish-ai/accomplish
- This skill: Self-generated from studying the above
