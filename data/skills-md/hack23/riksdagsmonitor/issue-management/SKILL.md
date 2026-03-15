---
name: issue-management
description: GitHub issue creation, labeling, milestones, agent assignment, and backlog prioritization for product management
license: Apache-2.0
---

# Issue Management

## Purpose

Create well-structured, actionable GitHub issues that facilitate clear communication, efficient triage, and effective task delegation to specialized agents or team members.

## Core Principles

1. **Clarity First**: Issue title and description must be immediately understandable
2. **Actionable**: Clear acceptance criteria and definition of done
3. **Properly Labeled**: Use labels for type, priority, area, and agent assignment
4. **Traceable**: Link to related issues, PRs, and documentation
5. **Evidence-Based**: Include screenshots, logs, or reproduction steps
6. **Agent-Optimized**: Structure issues for Copilot agent assignment

## Issue Structure

### Title Format
```
[Type] Brief, actionable description (50-80 chars)

Examples:
✅ [Bug] Homepage mobile navigation broken on Safari
✅ [Feature] Add voting discipline dashboard
✅ [Security] Update CSP header for CDN resources
✅ [Accessibility] Fix color contrast in party cards
✅ [Documentation] Update ARCHITECTURE.md with C4 diagrams
```

### Body Template
```markdown
## Problem Statement
Clear description of the issue or need (2-3 sentences)

## Current Behavior (for bugs)
What happens now (include error messages, screenshots)

## Expected Behavior
What should happen

## Steps to Reproduce (for bugs)
1. Navigate to...
2. Click on...
3. Observe...

## Acceptance Criteria
- [ ] Criterion 1 (testable, verifiable)
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Context
- Affected files: `index.html`, `styles.css`
- Browser/Device: Chrome 120, Safari 17 on iOS 17
- Related issues: #123, #456

## Evidence
[Screenshots, logs, error messages]

## Suggested Solution (optional)
Brief technical approach if known

## Agent Assignment (if applicable)
Recommend: @security-architect, @frontend-specialist
```

## Label Categories

### Type Labels (Required)
- **bug** 🐛 - Something isn't working
- **feature** ✨ - New functionality
- **enhancement** 🚀 - Improvement to existing feature
- **security** 🔒 - Security-related issue
- **documentation** 📝 - Documentation changes
- **accessibility** ♿ - WCAG 2.1 AA compliance
- **performance** ⚡ - Speed, optimization
- **refactor** 🔧 - Code quality, technical debt

### Priority Labels
- **priority:critical** 🔴 - Blocking, security, data loss
- **priority:high** 🟠 - Major functionality broken
- **priority:medium** 🟡 - Important but not urgent
- **priority:low** 🟢 - Nice to have, future

### Area Labels
- **area:frontend** - HTML/CSS/UI changes
- **area:ci-cd** - GitHub Actions, workflows
- **area:security** - Security controls, ISMS
- **area:accessibility** - WCAG compliance
- **area:i18n** - Multi-language support
- **area:docs** - Documentation

### Agent Labels (for delegation)
- **agent:security-architect** - Security architecture tasks
- **agent:frontend-specialist** - HTML/CSS/UI tasks
- **agent:quality-engineer** - Validation, testing tasks
- **agent:documentation-architect** - Documentation tasks
- **agent:isms-compliance-manager** - Compliance tasks
- **agent:deployment-specialist** - CI/CD tasks
- **agent:intelligence-operative** - Political data analysis
- **agent:task-agent** - Product management, issue creation
- **agent:ui-enhancement-specialist** - UI/UX enhancements

### Status Labels
- **status:triaged** - Reviewed and prioritized
- **status:blocked** - Waiting on dependency
- **status:in-progress** - Actively being worked on
- **status:needs-review** - Ready for review
- **status:wontfix** - Will not be addressed

## When to Use

- **Bug Reports**: User-reported or automated test failures
- **Feature Requests**: New functionality needs
- **Security Issues**: Vulnerabilities, compliance gaps
- **Accessibility Issues**: WCAG violations
- **Technical Debt**: Refactoring, code quality
- **Documentation Needs**: Missing or outdated docs
- **Agent Task Delegation**: Assign specialized agents
- **Product Backlog**: Track feature roadmap

## Examples

### Good Pattern: Bug Report with Evidence
```markdown
# [Bug] Mobile navigation menu not closing on link click (iOS Safari)

## Problem Statement
On iOS Safari, clicking navigation links does not close the mobile menu, forcing users to manually close it or scroll past it.

## Current Behavior
1. Open mobile menu (☰ button)
2. Click any navigation link
3. Page scrolls to section
4. Menu remains open, obscuring content

## Expected Behavior
Menu should auto-close after link click, revealing content immediately.

## Steps to Reproduce
1. Open https://riksdagsmonitor.com on iPhone (iOS 17)
2. Tap hamburger menu (☰)
3. Tap "Overview" link
4. Observe menu stays open

## Acceptance Criteria
- [ ] Menu closes immediately after link click
- [ ] Behavior consistent across all 14 language versions
- [ ] Works on iOS Safari, Chrome mobile, Firefox mobile
- [ ] No JavaScript errors in console
- [ ] Passes manual accessibility test (keyboard nav)

## Technical Context
- Affected files: `index*.html` (all 14 language versions)
- Browser: Safari 17 on iOS 17.2
- Related: Navigation uses CSS-only implementation

## Evidence
![Screenshot showing open menu after link click](screenshot.png)

## Suggested Solution
Add JavaScript event listener for link clicks to toggle menu:
```javascript
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelector('.menu-toggle').checked = false;
  });
});
```

## Agent Assignment
Recommend: @frontend-specialist
```

**Labels**: `bug`, `priority:high`, `area:frontend`, `area:i18n`, `agent:frontend-specialist`

### Good Pattern: Feature Request
```markdown
# [Feature] Add voting discipline dashboard for 8 parliamentary parties

## Problem Statement
Users cannot easily visualize voting discipline metrics (party cohesion, rebels, cross-party votes) for the 8 Swedish parliamentary parties, reducing transparency.

## Expected Behavior
New dashboard page showing:
- Party cohesion percentage (progress bars)
- Number of unanimous votes per party
- Number of rebel votes per party
- Heat map of cross-party voting patterns
- Historical trend over current riksmöte

## Acceptance Criteria
- [ ] Dashboard accessible from main navigation
- [ ] Visualizations use CSS-only (no JavaScript charts)
- [ ] WCAG 2.1 AA compliant (4.5:1 contrast, screen reader support)
- [ ] Responsive design (mobile/tablet/desktop)
- [ ] Available in all 14 languages
- [ ] Data sourced from riksdag-regering-mcp
- [ ] Includes data quality disclaimer

## Technical Context
- New files: `voting-discipline.html`, `voting-discipline_sv.html`, etc.
- Data source: `riksdag-regering-mcp` (search_voteringar, get_voting_group)
- Styling: Cyberpunk theme, use existing CSS variables
- Integration: Link from homepage, add to navigation

## Dependencies
- riksdag-regering-mcp MCP server (already configured)
- political-data-visualization skill
- Party color palette (already defined in styles.css)

## Agent Assignment
Recommend: @intelligence-operative (data analysis) → @ui-enhancement-specialist (UI implementation)
```

**Labels**: `feature`, `priority:medium`, `area:frontend`, `agent:intelligence-operative`, `agent:ui-enhancement-specialist`

### Anti-Pattern: Vague Issue
```markdown
# Navigation doesn't work

The menu is broken. Please fix it.
```

**Problems**:
- ❌ No clear problem statement
- ❌ No reproduction steps
- ❌ No acceptance criteria
- ❌ No technical context
- ❌ No evidence (screenshots, logs)
- ❌ No labels or assignment

### Anti-Pattern: Missing Acceptance Criteria
```markdown
# [Feature] Improve dashboard

Make the dashboard better and faster.

## Description
The current dashboard could be improved in various ways.
```

**Problems**:
- ❌ "Better" and "faster" are subjective, not measurable
- ❌ No specific acceptance criteria
- ❌ No technical approach
- ❌ Cannot be tested or verified

## GitHub API for Issue Creation

### Using github-mcp Tool
```javascript
// Create issue with proper structure
const issue = await github_create_issue({
  owner: "Hack23",
  repo: "riksdagsmonitor",
  title: "[Bug] Mobile navigation menu not closing on iOS Safari",
  body: `## Problem Statement
...

## Acceptance Criteria
- [ ] Menu closes on link click
- [ ] Works on iOS Safari
...`,
  labels: ["bug", "priority:high", "area:frontend", "agent:frontend-specialist"],
  assignees: [], // Leave empty for agent assignment
  milestone: 3 // Optional: milestone number
});

console.log(`Issue created: ${issue.html_url}`);
```

### Assigning to Copilot Agent
```javascript
// After creating issue, assign to specialized agent
await assign_copilot_to_issue({
  owner: "Hack23",
  repo: "riksdagsmonitor",
  issue_number: issue.number,
  base_ref: "main",
  custom_instructions: `
    - Fix menu closing behavior on iOS Safari
    - Test on all 14 language versions
    - Ensure WCAG 2.1 AA compliance
    - No breaking changes to existing functionality
  `
});
```

## Issue Triage Workflow

1. **New Issue Created** → Add `status:needs-triage` label
2. **Review Issue** → Verify completeness, request more info if needed
3. **Label** → Add type, priority, area, agent labels
4. **Prioritize** → Assign milestone if time-sensitive
5. **Assign** → Assign to agent or team member
6. **Update Status** → Change to `status:triaged`

## Remember

- **Clear titles** - [Type] actionable description
- **Complete body** - problem, acceptance criteria, context, evidence
- **Proper labels** - type, priority, area, agent
- **Testable criteria** - acceptance criteria must be verifiable
- **Evidence** - screenshots, logs, reproduction steps
- **Link related** - reference related issues, PRs, docs
- **Agent-optimized** - structure for Copilot agent assignment
- **Update status** - keep status labels current
- **Close with context** - explain resolution when closing

## References

- [GitHub Issues Documentation](https://docs.github.com/en/issues)
- [GitHub Issue Templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)
- [Labels Best Practices](https://github.com/joelparkerhenderson/github-special-files-and-paths#labels)
- [Hack23 ISMS - Issue Management](https://github.com/Hack23/ISMS-PUBLIC)

---

**Version**: 1.0  
**Last Updated**: 2026-02-06  
**Maintained by**: Hack23 AB
