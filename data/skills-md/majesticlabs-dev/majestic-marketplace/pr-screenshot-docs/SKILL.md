---
name: pr-screenshot-docs
description: Capture and document UI changes with before/after screenshots for pull requests. Use when creating PRs that include visual changes to ensure reviewers can assess design modifications.
disable-model-invocation: true
---

# PR Screenshot Documentation

Guidance for capturing and documenting UI changes with before/after screenshots when creating pull requests.

## When to Use This Skill

- Creating PRs with frontend/UI modifications
- Documenting visual changes for code review
- Building a visual record of design evolution
- Enabling async design review without running the app

## Screenshot Workflow

### 1. Before Making Changes

Capture the current state before implementing UI modifications:

```
1. browser_resize(width: 320, height: 568)  # Mobile-first
2. browser_navigate to the target page
3. browser_snapshot to identify elements
4. browser_take_screenshot(element: "Target component", ref: "E123")
```

Save or note the screenshot for later comparison.

### 2. After Implementing Changes

Capture the same view after your modifications:

```
1. Refresh or navigate to the updated page
2. browser_snapshot to get updated refs
3. browser_take_screenshot(element: "Target component", ref: "E123")
```

### 3. Upload Screenshots (Optional)

For persistent URLs in PR descriptions, upload to an image hosting service:

```bash
# Using curl with 0x0.st (ephemeral hosting)
curl -F 'file=@screenshot.png' https://0x0.st

# Or use project-specific image storage
```

**Note:** 0x0.st URLs expire. For permanent records, use GitHub's drag-and-drop image upload in PR descriptions or project documentation storage.

## PR Description Template

Include a visual comparison section in your PR description:

```markdown
## Visual Changes

| Before | After |
|--------|-------|
| ![Before](url-or-path) | ![After](url-or-path) |

### What Changed
- [Specific visual change 1]
- [Specific visual change 2]
```

## Viewport Recommendations

Choose viewport size based on what you're documenting:

| Target | Width | Height | Use Case |
|--------|-------|--------|----------|
| Mobile | 320 | 568 | Mobile-first responsive |
| Tablet | 768 | 1024 | Tablet layouts |
| Desktop | 1280 | 800 | Standard desktop |
| Wide | 1440 | 900 | Wide desktop layouts |

**Default to mobile (320px)** for documentation - if it looks good on mobile, it usually scales up well.

## Best Practices

### Capture Strategy

- **Focus on the changed component** - don't capture full pages unless layout changed
- **Use consistent viewports** - same size for before and after
- **Capture interactive states** - hover, focus, active when relevant
- **Include error states** - if you changed error handling UI

### Documentation Quality

- **Describe what changed** - don't make reviewers guess
- **Explain why** - connect visual changes to user benefit
- **Note accessibility** - mention contrast, focus indicators if relevant

### When NOT to Capture

- Pure backend changes with no UI impact
- Code refactoring without visual changes
- Test-only changes
- Configuration updates

## Integration with PR Workflow

This skill complements the `/majestic-engineer:git:create-pr` command. Before creating a PR with UI changes:

1. Take before screenshots (if you didn't already)
2. Implement your changes
3. Take after screenshots
4. Include comparison in PR description
5. Run the create-pr command

## Example PR Section

```markdown
## Visual Changes

| Before | After |
|--------|-------|
| ![Before - Button styling](./docs/screenshots/button-before.png) | ![After - Button styling](./docs/screenshots/button-after.png) |

### Changes Made
- Increased button padding from 8px to 12px for better touch targets
- Added subtle shadow for depth
- Improved contrast ratio from 3.5:1 to 4.8:1 (now WCAG AA compliant)

### Tested Viewports
- [x] Mobile (320px)
- [x] Tablet (768px)
- [x] Desktop (1280px)
```

## Related Tools

- `visual-validator` agent - For rigorous visual QA after changes
- `ui-ux-designer` agent - For iterative design refinement
