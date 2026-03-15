---
name: gh-aw-workflow-authoring
description: Master GitHub Agentic Workflows authoring - markdown syntax, natural language instructions, YAML frontmatter, compilation, and workflow patterns
license: Apache-2.0
version: 1.0.0
last_updated: 2026-02-17
tags: [github-agentic-workflows, workflow-authoring, markdown, natural-language, ai-automation]
---

# ✍️ GitHub Agentic Workflows - Workflow Authoring Skill

## 📋 Purpose

Master the art of authoring **GitHub Agentic Workflows** - creating AI-powered automation using natural language markdown instead of complex YAML. This skill provides comprehensive expertise in workflow design, natural language instructions, configuration, and best practices for effective agentic automation.

## 🎯 Core Concepts

### What Makes Agentic Workflows Different?

**Traditional GitHub Actions:**
```yaml
# Complex conditional logic
if: |
  contains(github.event.issue.labels.*.name, 'bug') &&
  !contains(github.event.issue.labels.*.name, 'wontfix') &&
  github.event.issue.state == 'open'
run: echo "Process bug"
```

**Agentic Workflow:**
```markdown
If this is an open bug that should be fixed, provide helpful triage information.
```

**Key Differences:**

| Traditional Actions | Agentic Workflows |
|-------------------|-------------------|
| ✅ Deterministic | 🤖 AI-driven decisions |
| ⚙️ Complex YAML | 📝 Natural language |
| 🔧 Fixed logic paths | 🧠 Context-aware responses |
| 📊 Explicit conditionals | 💡 Inferred intent |

## 🏗️ Workflow Structure

### File Anatomy

```
.github/
├── workflows/
│   ├── issue-triage.md          # Source (human-authored)
│   └── issue-triage.lock.yml    # Compiled (generated)
```

**Workflow File Structure:**
```markdown
---
# YAML Frontmatter - Configuration
on: issues
permissions: read-all
tools:
  github:
    toolsets: [issues]
  safeoutputs___comment:
engine: copilot
---

# Markdown Body - Natural Language Instructions

Analyze this issue and provide helpful triage information.

Consider:
- Issue content and context
- Related issues and PRs
- Historical patterns
- Repository conventions

Provide actionable recommendations.
```

### YAML Frontmatter

**Required Fields:**
```yaml
on: issues              # Trigger event
permissions: read-all   # Security permissions
tools:                  # Available tools
  github:
engine: copilot         # AI engine
```

**Optional Fields:**
```yaml
name: "Issue Triage"    # Workflow name
description: "Automated issue analysis"
timeout-minutes: 10     # Execution timeout
concurrency:            # Concurrency control
  group: ${{ github.ref }}
  cancel-in-progress: true
```

## 🛠️ Tools Configuration

### GitHub Tools

**Repository Operations:**
```yaml
tools:
  github:
    toolsets:
      - repos         # File operations
      - issues        # Issue management
      - pull_requests # PR operations
      - projects      # GitHub Projects
```

**Examples:**
```markdown
---
tools:
  github:
    toolsets: [repos]
---

Review the repository structure and suggest improvements.
```

### Safe Outputs

**Write Operations:**
```yaml
tools:
  safeoutputs___issue:       # Create/update issues
  safeoutputs___pull_request: # Create PRs
  safeoutputs___comment:      # Add comments
  safeoutputs___file:         # Modify files
    allowed_paths:
      - "docs/**/*.md"
  safeoutputs___label:        # Manage labels
  safeoutputs___noop:         # Read-only mode
```

**Example:**
```markdown
---
tools:
  safeoutputs___comment:
  safeoutputs___label:
---

Analyze this issue, add appropriate labels, and provide feedback.
```

### File Operations

```yaml
tools:
  edit:     # Edit existing files
  view:     # Read file contents
  create:   # Create new files
```

### Shell Commands

```yaml
tools:
  bash:
    allowed-commands:
      - npm
      - git
      - python3
```

**Security Note:** Be restrictive with shell access.

### Web Access

```yaml
tools:
  web-fetch:   # Fetch URLs
  web-search:  # Search the web
```

### Browser Automation

```yaml
tools:
  playwright:
    headless: true
```

### Custom MCP Servers

```yaml
tools:
  custom-mcp:
    url: https://your-mcp-server.com
    headers:
      Authorization: ${{ secrets.API_TOKEN }}
```

## 📝 Natural Language Instructions

### Writing Effective Prompts

**1. Be Specific and Clear:**

❌ **Bad:**
```markdown
Do something with this issue.
```

✅ **Good:**
```markdown
Analyze this issue and:
1. Determine if it's a bug, feature request, or question
2. Check for duplicates in existing issues
3. Suggest appropriate labels
4. Add a helpful comment with next steps
```

**2. Provide Context:**

❌ **Bad:**
```markdown
Fix the code.
```

✅ **Good:**
```markdown
Review the changed files in this PR and:
- Check for common security issues (SQL injection, XSS)
- Verify error handling is comprehensive
- Ensure tests cover new functionality
- Suggest improvements following our style guide
```

**3. Structure with Lists:**

```markdown
Perform code review with focus on:

**Security:**
- Input validation
- Authentication checks
- Data sanitization

**Quality:**
- Code duplication
- Function complexity
- Test coverage

**Documentation:**
- API documentation
- Inline comments
- README updates
```

**4. Use Examples:**

```markdown
Analyze this pull request and provide feedback similar to:

"## Code Review

### Security Concerns
- Line 45: User input not validated

### Performance
- Line 78: Consider caching this result

### Style
- Follows project conventions ✓"
```

### Prompt Engineering Patterns

**Pattern 1: Analyze → Decide → Act**
```markdown
1. Analyze the issue description and comments
2. Decide if it's a duplicate or new issue
3. If duplicate: Close with reference to original
4. If new: Add labels and assign to appropriate team
```

**Pattern 2: Conditional Instructions**
```markdown
If this is a security issue:
- Add 'security' label
- Mark as high priority
- Notify security team

If this is a feature request:
- Add 'enhancement' label
- Ask for use case details
- Add to product backlog
```

**Pattern 3: Multi-Step Workflow**
```markdown
Step 1: Review all changed files
Step 2: Identify potential issues
Step 3: For each issue found:
  - Note the file and line number
  - Explain the problem
  - Suggest a solution
Step 4: Summarize findings in a comment
```

## 🎯 Workflow Examples

### Example 1: Issue Triage

```markdown
---
name: "Issue Triage"
on: issues
permissions: read-all

tools:
  github:
    toolsets: [issues]
  safeoutputs___label:
  safeoutputs___comment:
---

# Automated Issue Triage

Analyze this new issue and provide comprehensive triage:

## Classification
Determine if this is:
- 🐛 **Bug**: Something isn't working
- ✨ **Feature**: New functionality request
- ❓ **Question**: Help or clarification needed
- 📚 **Documentation**: Documentation improvement

## Duplicate Check
Search for similar issues using keywords from the title and description.
If a duplicate is found, note the issue number.

## Priority Assessment
Based on:
- Impact (how many users affected)
- Severity (how critical)
- Workaround availability

Suggest priority: high, medium, or low

## Actions
Using safeoutputs___label, add appropriate labels:
- Type: bug/feature/question/docs
- Priority: high/medium/low
- Component: affected area

Using safeoutputs___comment, provide:
- Classification explanation
- Duplicate status (if any)
- Recommended priority with reasoning
- Suggested assignee or team
- Next steps for the reporter
```

### Example 2: PR Code Review

```markdown
---
name: "Code Review Assistant"
on: pull_request
permissions: read-all

tools:
  github:
    toolsets: [pull_requests, repos]
  bash:
    allowed-commands: [git, npm]
  safeoutputs___comment:
---

# Automated Code Review

Perform a comprehensive code review of this pull request:

## Files Changed
Review each changed file for:

### Security
- Input validation
- SQL injection risks
- XSS vulnerabilities
- Authentication/authorization
- Sensitive data exposure

### Code Quality
- Function complexity
- Code duplication
- Error handling
- Edge cases

### Testing
- Test coverage
- Test quality
- Missing test cases

### Performance
- Inefficient algorithms
- Memory leaks
- Database query optimization

### Style
- Follows project conventions
- Naming consistency
- Documentation completeness

## Summary
Provide:
- Overall assessment (approve/needs work/concerns)
- Count of issues by severity
- Most critical items to address
- Positive feedback on good practices

Use safeoutputs___comment to post the review.
```

### Example 3: Documentation Updates

```markdown
---
name: "Documentation Sync"
on: push
paths:
  - 'src/**/*.ts'

permissions: read-all

tools:
  github:
    toolsets: [repos]
  bash:
    allowed-commands: [git]
  safeoutputs___file:
    allowed_paths:
      - "docs/**/*.md"
      - "README.md"
---

# Keep Documentation Current

When code changes, ensure documentation stays synchronized:

## Changed Files Analysis
1. Identify which source files changed
2. Determine if they have corresponding documentation
3. Review the nature of changes (new features, API changes, deprecations)

## Documentation Updates
For each relevant change:

### API Documentation
- Update function signatures
- Add new method documentation
- Mark deprecated features
- Update examples

### README
- Add new feature descriptions
- Update installation if needed
- Refresh examples
- Update version compatibility

### Changelog
- Add entry for this change
- Include breaking changes prominently
- Link to PR/issue

## Implementation
Use safeoutputs___file to update documentation files.
Ensure:
- Examples are tested and work
- Links are valid
- Formatting is consistent
- Version numbers are current
```

### Example 4: Dependency Management

```markdown
---
name: "Dependency Update Review"
on: pull_request
paths:
  - 'package.json'
  - 'package-lock.json'

permissions: read-all

tools:
  github:
    toolsets: [pull_requests]
  bash:
    allowed-commands: [npm]
  web-fetch:
  safeoutputs___comment:
---

# Dependency Update Analysis

When dependencies are updated, provide security and compatibility review:

## Changed Dependencies
Identify all dependency changes:
- New dependencies added
- Updated versions
- Removed dependencies

## Security Check
For each changed dependency:
1. Check npm audit for known vulnerabilities
2. Review GitHub advisory database
3. Check Snyk or similar databases
4. Note any security warnings

## Compatibility Check
- Review changelog for breaking changes
- Check if major version bump
- Verify Node.js version compatibility
- Check for deprecated features used

## License Check
- Verify license compatibility
- Flag any license changes
- Note GPL or other copyleft licenses

## Recommendation
Provide:
- ✅ Safe to merge
- ⚠️ Review required
- ❌ Security concerns

Include:
- Specific issues found
- Recommended actions
- Links to relevant documentation

Use safeoutputs___comment to post the analysis.
```

### Example 5: Scheduled Maintenance

```markdown
---
name: "Weekly Repository Health Check"
on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday

permissions: read-all

tools:
  github:
    toolsets: [issues, pull_requests, repos]
  safeoutputs___issue:
---

# Weekly Repository Health Report

Generate a comprehensive repository health report:

## Open Issues Analysis
- Total open issues
- Issues by label
- Stale issues (30+ days)
- High priority unassigned
- Trends (increasing/decreasing)

## Pull Requests Review
- Open PRs count
- Average PR age
- PRs awaiting review
- Stale PRs (14+ days)
- Merge rate trend

## Code Quality Metrics
- Test coverage
- Recent build failures
- Security vulnerabilities
- Dependency updates needed

## Community Health
- New contributors this week
- First-time contributors
- Response times
- Merge frequency

## Recommendations
Based on the analysis:
1. Issues to prioritize
2. PRs needing attention
3. Maintenance tasks
4. Community engagement opportunities

Use safeoutputs___issue to create:
- Weekly health report issue
- Label it 'maintenance' and 'automated'
- Assign to repository maintainers
```

## ⚙️ Advanced Configuration

### Concurrency Control

```yaml
---
on: issues

concurrency:
  group: issue-${{ github.event.issue.number }}
  cancel-in-progress: true
---
```

**Use Cases:**
- Prevent duplicate processing
- Cancel outdated runs
- Resource management

### Conditional Execution

```yaml
---
on: pull_request

if: |
  github.event.pull_request.draft == false &&
  !contains(github.event.pull_request.labels.*.name, 'skip-review')
---
```

### Timeouts

```yaml
---
timeout-minutes: 5  # Cancel if exceeds 5 minutes
---
```

### Environment Variables

```yaml
---
env:
  NODE_VERSION: '24'
  DEBUG: 'true'
---
```

## 🔄 Compilation Process

### Manual Compilation

```bash
# Install compiler
npm install -g @github/agentic-workflows-compiler

# Compile workflow
aw-compile .github/workflows/issue-triage.md

# Output: .github/workflows/issue-triage.lock.yml
```

### Automatic Compilation

**GitHub Actions:**
```yaml
name: Compile Agentic Workflows

on:
  pull_request:
    paths:
      - '.github/workflows/*.md'

jobs:
  compile:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Compile Workflows
        run: |
          npm install -g @github/agentic-workflows-compiler
          aw-compile .github/workflows/*.md
      
      - name: Commit Compiled Files
        run: |
          git add .github/workflows/*.lock.yml
          git commit -m "Compile agentic workflows"
          git push
```

### Validation

```bash
# Validate syntax
aw-validate .github/workflows/issue-triage.md

# Check for common issues
aw-lint .github/workflows/issue-triage.md
```

## 🎨 Best Practices

### 1. Single Responsibility

❌ **Bad: Multiple tasks in one workflow**
```markdown
Triage issues, review PRs, update documentation, and manage dependencies.
```

✅ **Good: Focused workflow**
```markdown
Triage new issues by analyzing content, checking for duplicates, and applying appropriate labels.
```

### 2. Clear Success Criteria

❌ **Bad: Vague instructions**
```markdown
Make this better.
```

✅ **Good: Specific criteria**
```markdown
Improve this code by:
- Reducing cyclomatic complexity to <10
- Adding error handling for edge cases
- Including unit tests with 80%+ coverage
```

### 3. Tool Minimalism

❌ **Bad: Grant all tools**
```yaml
tools:
  github:
    toolsets: ['*']
  bash:
  safeoutputs___*:
```

✅ **Good: Only required tools**
```yaml
tools:
  github:
    toolsets: [issues]
  safeoutputs___comment:
```

### 4. Error Guidance

```markdown
If you encounter issues:
1. Check for existing similar issues first
2. If API rate limit reached, note it and suggest trying later
3. If insufficient permissions, explain what's needed
4. Always provide fallback recommendations
```

### 5. Testing Instructions

```markdown
Before implementation:
1. Validate file paths exist
2. Check for required permissions
3. Verify tool availability
4. Test with dry-run if possible

Use safeoutputs___noop to report findings if validation fails.
```

## 🚨 Common Pitfalls

### Pitfall 1: Overly Complex Instructions

❌ **Don't:**
```markdown
Analyze code considering 27 different quality metrics, cross-reference with 15 different documentation sources, generate detailed reports with statistical analysis, create visualization dashboards, and...
```

✅ **Do:**
```markdown
Focus on 3 key areas:
1. Security vulnerabilities
2. Test coverage
3. Code complexity

Provide actionable feedback for each.
```

### Pitfall 2: Assuming Tool Availability

❌ **Don't:**
```markdown
Use bash to run npm install...
```

✅ **Do:**
```yaml
---
tools:
  bash:
    allowed-commands: [npm]
---

If npm is available, run npm install to verify dependencies.
```

### Pitfall 3: Ignoring Rate Limits

❌ **Don't:**
```markdown
Search all 10,000 issues for duplicates.
```

✅ **Do:**
```markdown
Search recent issues (last 90 days) for duplicates.
If none found, note that older issues weren't checked due to performance.
```

### Pitfall 4: Not Handling Failures

❌ **Don't:**
```markdown
Update the file with new content.
```

✅ **Do:**
```markdown
Attempt to update the file.
If it fails (permissions, file doesn't exist, etc.):
- Use safeoutputs___noop to explain the issue
- Suggest manual resolution steps
```

## 🔗 Related Skills

- **gh-aw-safe-outputs** - Understanding write operations
- **gh-aw-tools-ecosystem** - Available tools and capabilities
- **gh-aw-mcp-gateway** - MCP server integration
- **gh-aw-continuous-ai-patterns** - Workflow patterns and strategies
- **gh-aw-github-actions-integration** - Deployment and CI/CD

## 📚 References

- [GitHub Agentic Workflows Documentation](https://github.github.com/gh-aw/)
- [Quick Start Guide](https://github.github.com/gh-aw/setup/quick-start/)
- [How They Work](https://github.github.com/gh-aw/introduction/how-they-work/)
- [Workflow Examples](https://github.github.com/gh-aw/examples/)
- [Best Practices](https://github.github.com/gh-aw/guides/best-practices/)

## ✅ Remember

- ✅ Write in natural language, not code
- ✅ Be specific and provide context
- ✅ Use tool minimalism (least privilege)
- ✅ Structure with clear sections
- ✅ Provide examples in instructions
- ✅ Handle errors gracefully
- ✅ Test before deploying
- ✅ Focus on single responsibility
- ✅ Compile generates .lock.yml
- ✅ Natural language beats complex YAML

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-17  
**Maintained by**: Hack23 AB
