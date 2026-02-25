---
name: storybook-stories
description: 'Writes and maintains Storybook stories and interaction tests using CSF3 format. Covers component stories, play functions, visual regression testing with Chromatic, and accessibility testing. Use when creating component documentation, writing interaction tests, debugging test failures, configuring visual snapshots, or updating story structure. Use for CSF3, play functions, userEvent, Testing Library queries, Chromatic configuration, autodocs, MDX.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: https://storybook.js.org/docs
user-invocable: false
---

# Storybook Stories

## Overview

Storybook is a frontend workshop for building UI components in isolation. Stories are written in Component Story Format 3 (CSF3), which uses object syntax with `args` for type-safe component documentation and testing.

**When to use:** Component documentation with live examples, interaction testing with play functions, visual regression testing, accessibility validation, design system maintenance, isolated component development.

**When NOT to use:** End-to-end testing (use Playwright/Cypress), API integration testing (use Vitest/Jest), full application testing (use browser automation), performance testing (use Lighthouse/WebPageTest).

## Quick Reference

| Pattern                | API                                                    | Key Points                             |
| ---------------------- | ------------------------------------------------------ | -------------------------------------- |
| Basic story            | `export const Default: Story = { args }`               | Use args for simple single components  |
| Complex story          | `export const Example: Story = { render }`             | Use render for multi-component layouts |
| Meta configuration     | `const meta = { component, args } satisfies Meta`      | Define defaults and argTypes           |
| Interaction test       | `play: async ({ canvas, userEvent, args })`            | canvas and userEvent provided directly |
| User interaction       | `await userEvent.click(element)`                       | Always await userEvent methods         |
| Query elements         | `canvas.getByRole('button')`                           | Prefer getByRole over other queries    |
| Assertions             | `await expect(args.onPress).toHaveBeenCalled()`        | Use storybook/test assertions          |
| beforeEach hook        | `beforeEach: async ({ args }) => {}`                   | Setup mocks before story renders       |
| Play composition       | `await OtherStory.play?.(context)`                     | Reuse setup across stories             |
| Autodocs               | `tags: ['autodocs']`                                   | Enable automatic documentation         |
| Controls customization | `argTypes: { variant: { control: 'select' } }`         | Configure control panel                |
| Decorators             | `decorators: [withTheme]`                              | Add wrappers or context providers      |
| Parameters             | `parameters: { layout: 'centered' }`                   | Configure addon behavior per story     |
| Chromatic snapshot     | `parameters: { chromatic: { delay: 300 } }`            | Control visual regression captures     |
| Disable snapshot       | `parameters: { chromatic: { disableSnapshot: true } }` | Skip story in visual tests             |
| A11y testing           | `await expect(button).toHaveAccessibleName()`          | Validate accessible labels             |

## Common Mistakes

| Mistake                                    | Correct Pattern                                          |
| ------------------------------------------ | -------------------------------------------------------- |
| Using args with multi-component layouts    | Use render for complex compositions                      |
| Not awaiting userEvent methods             | Always await: `await userEvent.click(button)`            |
| Using within(canvasElement) manually       | Destructure `canvas` from play context directly          |
| Using getByTestId first                    | Prefer getByRole, getByLabelText, getByText              |
| Missing default args at meta level         | Add args to meta to prevent placeholder controls         |
| Exposing non-serializable props            | Disable className, ref, style in argTypes                |
| Not composing play functions               | Reuse setup with `await BaseStory.play?.(context)`       |
| Forgetting to mock callbacks               | Use `fn()` for event handlers: `args: { onPress: fn() }` |
| Missing accessible names for icon buttons  | Add aria-label or use aria-labelledby                    |
| Not scoping queries for portal content     | Use `within(canvasElement.ownerDocument.body)`           |
| Using boolean && for conditional rendering | Use ternary in stories for consistent snapshots          |
| Not waiting for animations                 | Wrap assertions in waitFor for async state               |

## Common Fixes

| Problem                    | Solution                                        |
| -------------------------- | ----------------------------------------------- |
| Controls show placeholders | Add `args` at meta level with default values    |
| Serialization error        | Disable `className`, `ref`, `style` in argTypes |
| Portal element not found   | Search `body` instead of `canvas`               |
| Animation timing issues    | Wrap assertions in `waitFor`                    |
| Multiple buttons found     | Add `{ name: '...' }` to getByRole              |
| A11y test failing          | Add `label` prop or `aria-label`                |

## Delegation

- **Story structure review**: Use `code-reviewer` skill for CSF3 pattern validation
- **Accessibility audit**: Use `Explore` agent to discover ARIA patterns across stories
- **Visual regression analysis**: Use `Task` agent to investigate Chromatic failures

## References

- [Story writing patterns and CSF3 syntax](references/story-writing.md)
- [Interaction tests with play functions](references/interaction-tests.md)
- [Component documentation and controls](references/component-documentation.md)
- [Visual testing with Chromatic](references/visual-testing.md)
