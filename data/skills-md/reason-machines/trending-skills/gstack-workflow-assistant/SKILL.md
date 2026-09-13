---
name: gstack-workflow-assistant
description: Team of specialist AI workflows for Claude Code with CEO review, engineering planning, code review, shipping, QA testing, and browser automation
triggers:
  - "plan this feature like a CEO"
  - "review this code thoroughly"
  - "ship this branch"
  - "test this in browser"
  - "run QA on my app"
  - "do engineering retrospective"
  - "browse and test this page"
  - "setup browser session"
---

# gstack Workflow Assistant

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection

Transform Claude Code from a generic assistant into a team of specialists you can summon on demand. Eight opinionated workflow skills that act as CEO, Engineering Manager, Release Manager, and QA Engineer with slash commands for planning, review, shipping, and testing.

## What It Does

gstack provides specialized AI personas and workflows:
- **CEO Review**: Rethink problems and find the 10-star product hiding in requests
- **Engineering Planning**: Lock in architecture, data flow, and edge cases
- **Code Review**: Paranoid staff engineer-level review that catches production bugs
- **Release Management**: One-command shipping with tests and PR creation
- **QA Testing**: Automated browser testing with screenshots and systematic coverage
- **Browser Automation**: Give AI eyes to click through your app and catch breakage
- **Session Management**: Import real browser cookies for authenticated testing
- **Team Retrospectives**: Engineering manager-style retros with per-person insights

## Installation

### Requirements
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
- [Git](https://git-scm.com/)
- [Bun](https://bun.sh/) v1.0+
- macOS or Linux (x64/arm64) for browser automation

### Global Installation
```bash
git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack
./setup
```

### Project Installation
```bash
cp -Rf ~/.claude/skills/gstack .claude/skills/gstack
rm -rf .claude/skills/gstack/.git
cd .claude/skills/gstack
./setup
```

Add to your `CLAUDE.md`:
```markdown
## gstack
Use /browse skill from gstack for all web browsing. Never use mcp__claude-in-chrome__* tools.

Available skills:
- /plan-ceo-review - Product strategy review
- /plan-eng-review - Technical architecture planning  
- /review - Thorough code review
- /ship - One-command branch shipping
- /browse - Browser automation and testing
- /qa - Systematic QA testing
- /setup-browser-cookies - Session management
- /retro - Engineering retrospectives
```

## Core Commands

### Planning Workflows

#### CEO Product Review
```typescript
// Start with feature description, then review strategy
You: I want to add seller photo upload to the listing app

You: /plan-ceo-review
// AI responds as CEO: challenges assumptions, finds bigger opportunity
// "Photo upload" → "AI-powered listing creation from photos"
```

#### Engineering Architecture Review
```typescript
You: /plan-eng-review
// AI responds as tech lead:
// - Architecture diagrams
// - State machines
// - Async job boundaries  
// - Failure modes
// - Test matrices
```

### Code Quality Workflows

#### Thorough Code Review
```typescript
You: /review
// Paranoid staff engineer review:
// - Race conditions
// - Trust boundaries
// - Missing error handling
// - Production failure modes
```

#### One-Command Shipping
```typescript
You: /ship
// Automated release process:
// 1. Sync main branch
// 2. Run test suite
// 3. Resolve review comments
// 4. Push branch
// 5. Open pull request
```

### QA and Testing Workflows

#### Browser Automation
```typescript
You: /browse https://myapp.com
// AI navigates your app:
// - Takes screenshots
// - Clicks through workflows
// - Identifies breakage
// - Tests responsive design
```

#### Systematic QA Testing
```typescript
You: /qa
// Branch-aware testing:
// - Analyzes git diff
// - Identifies affected pages
// - Tests localhost:3000
// - Full exploration mode
// - Regression testing

You: /qa https://staging.myapp.com --quick
// Quick smoke test: 5 pages in 30 seconds
```

#### Session Management
```typescript
You: /setup-browser-cookies staging.myapp.com
// Imports cookies from real browser (Chrome, Arc, Brave, Edge)
// Enables testing authenticated pages without manual login
```

### Team Workflows

#### Engineering Retrospectives
```typescript
You: /retro
// Engineering manager-style retro:
// - Analyzes git history
// - Per-person contributions
// - Growth opportunities
// - Team dynamics
// - Saves to .context/retros/
```

## Configuration

### Browser Settings
gstack creates isolated browser instances in `.gstack/` directory:
```typescript
// Automatic browser configuration
{
  userDataDir: '.gstack/browser-data',
  headless: false, // for debugging
  viewport: { width: 1280, height: 720 },
  timeout: 30000
}
```

### Project Structure
```
your-project/
├── .claude/
│   └── skills/
│       └── gstack/
│           ├── skills/           # Workflow prompts
│           ├── browse/           # Browser automation
│           └── package.json
├── .gstack/                      # Browser data (gitignored)
│   ├── browser-data/
│   └── screenshots/
└── .context/
    └── retros/                   # Retrospective history
```

## Integration Patterns

### Multi-Session Workflow
Use [Conductor](https://conductor.build) for parallel sessions:
```typescript
// Session 1: Feature development
You: /plan-ceo-review
You: /plan-eng-review
// [implement feature]

// Session 2: Code review
You: /review
// [fix issues]

// Session 3: QA testing  
You: /qa --full

// Session 4: Release
You: /ship
```

### CI/CD Integration
```yaml
# .github/workflows/gstack-qa.yml
name: gstack QA
on: [pull_request]
jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: cd .claude/skills/gstack && ./setup
      - run: echo "/qa --regression" | claude-code
```

### Team Onboarding
```markdown
# Add to team docs
## Development Workflow
1. `/plan-ceo-review` - Validate product direction
2. `/plan-eng-review` - Lock architecture  
3. Implement feature
4. `/review` - Paranoid code review
5. `/qa` - Test branch thoroughly
6. `/ship` - One-command release
7. `/qa staging.app.com` - Staging verification
```

## Advanced Usage

### Custom QA Scenarios
```typescript
// Feature-specific testing
You: /qa --focus=checkout-flow
You: /qa --mobile-only
You: /qa --accessibility

// Performance testing
You: /browse https://app.com
// Then: "Run lighthouse audit on this page"
```

### Cross-Browser Testing
```typescript
// Test in multiple browsers
You: /setup-browser-cookies app.com
You: /browse app.com --browser=chrome
// [switch session]
You: /browse app.com --browser=firefox
```

### Regression Testing
```typescript
// Before major changes
You: /qa --baseline
// [make changes]  
You: /qa --compare-baseline
// AI identifies visual/functional regressions
```

## Troubleshooting

### Binary Issues
```bash
# Rebuild browser automation binary
cd .claude/skills/gstack
rm -rf browse/dist
./setup
```

### Permission Errors
```bash
# Fix executable permissions
cd .claude/skills/gstack
chmod +x setup browse/dist/browse
```

### Missing Dependencies
```bash
# Reinstall Node dependencies
cd .claude/skills/gstack
rm -rf node_modules
bun install
```

### Browser Automation Failures
```typescript
// Debug browser issues
You: /browse --debug
// Runs browser in non-headless mode for inspection

// Clear browser data
rm -rf .gstack/browser-data
```

### Skill Registration Issues
```typescript
// Re-register skills
cd .claude/skills/gstack
./setup

// Verify skills are available
You: /plan-ceo-review --help
```

The skills work by providing specialized prompts and browser automation tools that transform Claude Code into domain experts. Each workflow enforces specific cognitive modes - CEO strategic thinking, engineering rigor, paranoid review, or systematic testing - instead of generic assistance.
