---
name: engineering-onboarding
description: "Create an onboarding guide for an engineer joining a team that consumes the design system. Trigger when someone says: onboard new engineer, developer getting started guide, new engineer guide, engineering onboarding, first day for developers, frontend onboarding, or anything about helping an engineer new to the team get up to speed with the design system."
references:
  - ../../knowledge-notes/design-to-code-contract.md
---

## Context

Engineering onboarding is genuinely different from designer onboarding. The mental model is different (consuming an API vs composing with a library), the first tasks are different (install and import vs connect Figma library), the tooling is different (package manager, TypeScript types, test harness vs Figma, documentation platform). Most importantly, engineers are where component drift originates — wrapping system components in local styled wrappers, hardcoding token values, reimplementing components locally. Proper onboarding from day one is the highest-leverage adoption intervention.

## Key principles

**From design-to-code-contract:** Engineers and designers operate on opposite sides of the contract. Designers compose with a library (Figma, Storybook). Engineers consume an API (imports, props, types). The contract is the component signature: what props it accepts, what slots it exposes, what variants are possible. Component drift begins when an engineer builds a local wrapper because "the system component is close but not quite right" — escalating to designers too late means the system lost control. Onboarding embeds the contract from day one.

**Key principle for engineers:** Do not wrap system components. Do not hardcode values. Do not copy source code. Ask first.

## Configuration

Before writing the guide, gather these inputs:

1. **Framework:** React, Vue, Web Components, Svelte, Angular, etc.
2. **Package manager:** npm, yarn, pnpm (include install command)
3. **Token consumption:** CSS custom properties, JavaScript imports, Tailwind theme config, Sass variables
4. **Component API patterns:** Props, slots, composition style, controlled vs uncontrolled patterns
5. **TypeScript:** Are component types exported? Import pattern for types?
6. **Testing:** Visual regression tool (Chromatic, Percy), unit testing patterns, accessibility testing expectations
7. **Contribution path:** How does an engineer propose a fix or new component? PR process, code review, approval gates
8. **Known rough edges:** Documented workarounds, temporary incompatibilities, or known limitations
9. **Team contacts:** Slack channel, primary system maintainer, office hours schedule

## Steps

**Step 1: Gather system context from the team**

Ask directly: framework, package manager, token consumption method, TypeScript setup, testing tools, contribution expectations. If documentation exists, review it first — you're clarifying, not starting from scratch. Record which information is documented vs tribal knowledge (tribal knowledge is what gets lost in onboarding).

Output: A 5-minute conversation summary or Slack thread capture.

**Step 2: Structure the onboarding guide**

Use this exact section order. Each section builds on prior context. No forward references.

**Step 3: Write the guide introduction**

```
# Getting started with [Design System Name] — for engineers

**For:** Engineers joining [Team Name]  
**Last updated:** [Today's date]  
**Questions:** [Slack channel or contact email]  
**Estimated time:** 30 minutes to first component render

You're consuming a versioned component library and token system. Your job is to use it correctly, not to rebuild it. This guide shows you how.
```

**Step 4: Write "What [System Name] is" section**

One paragraph from engineer perspective. Answer: What am I consuming? What can it do? What shouldn't I do?

Example template:
```
[System Name] is a versioned component library with [X] components and [Y] design tokens. 
It's distributed as an npm package and consumed via import statements in your code. 
The system owns component styling and behavior — your job is to compose components correctly 
and reference tokens instead of hardcoding values. If you need a variant or component that 
doesn't exist, you ask the system team; you don't build a local version.
```

**Step 5: Write "Installation and setup" section**

Copy-pasteable commands. Mark placeholders in brackets, not in the command itself.

```
## Installation and setup

Install the package:
\`\`\`bash
npm install @[org]/[design-system-name]
\`\`\`

Import the CSS (or theme provider for React):
\`\`\`jsx
import '@[org]/[design-system-name]/styles/index.css';
\`\`\`

Verify it works — render a Button in your app:
\`\`\`jsx
import { Button } from '@[org]/[design-system-name]';

export default function App() {
  return <Button>Click me</Button>;
}
\`\`\`

You should see a styled button on the screen. If you see an unstyled button or an error, 
check the [install troubleshooting guide](link).
```

**Step 6: Write "Using components" section**

Import pattern. Prop API conventions. One complete code example. TypeScript types if applicable.

```
## Using components

All components are named exports. Import what you need:
\`\`\`jsx
import { Button, Input, Card } from '@[org]/[design-system-name]';
\`\`\`

Read prop documentation in Storybook: [link to component docs]. 
Every prop is listed with type and default value.

Example — a login form using system components:
\`\`\`jsx
import { Button, Input, Card, Text } from '@[org]/[design-system-name]';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  
  return (
    <Card padding="large">
      <Text variant="heading">Sign in</Text>
      <Input 
        type="email" 
        placeholder="Email" 
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <Button variant="primary">Sign in</Button>
    </Card>
  );
}
\`\`\`

For TypeScript, component types are exported from the package:
\`\`\`tsx
import type { ButtonProps } from '@[org]/[design-system-name]';
\`\`\`
```

**Step 7: Write "Using tokens" section**

Include before/after example showing wrong vs right.

```
## Using tokens

Tokens are design decisions (spacing, color, typography) managed by the system team. 
Always reference tokens, never hardcode values.

**Access tokens via CSS variables:**
\`\`\`css
.my-component {
  padding: var(--ds-spacing-medium);
  color: var(--ds-color-text-primary);
}
\`\`\`

**or JavaScript imports (if available):**
\`\`\`js
import { spacing, colors } from '@[org]/[design-system-name]/tokens';

const styles = {
  padding: spacing.medium,
  color: colors.text.primary,
};
\`\`\`

**Wrong — hardcoded value:**
\`\`\`jsx
<div style={{ padding: '16px', color: '#222222' }}>
  Content
</div>
\`\`\`

**Right — uses tokens:**
\`\`\`jsx
import { spacing, colors } from '@[org]/[design-system-name]/tokens';

<div style={{ padding: spacing.medium, color: colors.text.primary }}>
  Content
</div>
\`\`\`

Use semantic tokens (e.g., `colors.text.primary`), never primitives directly 
(e.g., never reach for `colors.blue[500]`). Semantic tokens survive theme changes; 
primitives break in dark mode or custom themes.
```

**Step 8: Write "When the system doesn't have what you need" section**

Escalation path. Contribution path. Temporary workarounds.

```
## When the system doesn't have what you need

**First:** Check Storybook [link] and the component API docs.  
**Second:** Ask in #[design-system-slack-channel].  
**Third:** File a feature request in [issue tracker].  

Don't copy component source. Don't build a local wrapper. Both create drift 
and make the system lose visibility into what you actually need.

**Temporary workarounds** (max 1-2 sprint): It's okay to style a system component 
locally while waiting for a system variant — use a class wrapper, not !important 
overrides. Document the workaround in a comment with a link to the tracking issue. 
Plan to remove it when the system delivers the variant.

**Contributing a fix** (bugs in system components): 
1. Fork [system repo]
2. Fix the issue
3. Add a test
4. Open a PR against the [main/release branch]
5. System team reviews and merges

[Link to contribution guide]
```

**Step 9: Write "Testing with system components" section**

Unit testing, visual regression, accessibility expectations.

```
## Testing with system components

**Unit tests:** Mock system components if needed:
\`\`\`jsx
jest.mock('@[org]/[design-system-name]', () => ({
  Button: ({ children, ...props }) => <button {...props}>{children}</button>,
}));
\`\`\`

Test your component's logic, not the system component's rendering 
(that's the system team's job).

**Visual regression:** We use [Chromatic/Percy]. Your PR will automatically 
compare visual changes against the baseline. Review differences in the PR check 
before merging. If you update a component's appearance intentionally, 
approve the diff.

**Accessibility testing:** System components are WCAG AA by default. Test your 
composition for proper heading hierarchy, alt text on images, and focus management. 
[Link to a11y guide]
```

**Step 10: Write "Common mistakes" section**

Seven anti-patterns specific to engineers.

```
## Common mistakes

1. **Wrapping system components in local styled wrappers**
   Don't: Create a `StyledButton = styled(Button)`. Request a variant from the system instead.

2. **Hardcoding hex values instead of referencing tokens**
   Don't: `color: '#FF4444'`. Use `color: var(--ds-color-error)`.

3. **Using primitive tokens directly**
   Don't: `colors.blue[500]`. Use `colors.primary` (semantic tier).

4. **Copying component source instead of importing**
   Don't: Copy the Button JSX into your repo. That breaks updates forever.

5. **Overriding component styles with !important**
   Don't: `.my-button { color: red !important; }`. Request the system variant.

6. **Pinning to a specific version and never updating**
   Don't: Lock `@[org]/[design-system-name]` to 1.2.0 for a year. 
   Update monthly. Bug fixes and security patches matter.

7. **Building local variants instead of requesting them**
   Don't: Create a custom "success with icon" button variant locally. 
   Tell the system team. It probably belongs in the system.
```

**Step 11: Write "Your first two weeks" section**

Checkbox path with concrete tasks.

```
## Your first two weeks

**Week 1:**
- [ ] Install the package and render your first component (today)
- [ ] Read the [components overview](link) — understand what exists
- [ ] Use tokens in a feature you're working on — don't hardcode values
- [ ] Post a question in #[design-system-channel] — introduce yourself

**Week 2:**
- [ ] Review a PR that touches system components — spot common mistakes
- [ ] File a bug or feature request based on something you hit — 
  show you understand the escalation path
- [ ] Pair with a system team member for 30 min — ask your hardest questions
- [ ] Read [design-to-code-contract](link) — understand why things work this way
```

**Step 12: Write "Quick reference card" section**

Compact, printable.

```
## Quick reference card

**Install:**
\`\`\`bash
npm install @[org]/[design-system-name]
\`\`\`

**Import components:**
\`\`\`jsx
import { Button, Input } from '@[org]/[design-system-name]';
\`\`\`

**Access tokens:**
\`\`\`jsx
import { spacing, colors } from '@[org]/[design-system-name]/tokens';
\`\`\`

**Documentation:** [Storybook link]  
**Questions:** [#slack-channel](slack link)  
**Contribute:** [GitHub repo link]  
**Escalate:** Post in Slack first, then file an issue  

**Remember:** Use it correctly. Don't wrap it. Don't copy it. Ask first.
```

**Step 13: Write "Common questions" section**

Four to five engineer-specific Q&As.

```
## Common questions

**Q: Can I override component styles with CSS?**
A: Not with !important. If you need a visual change, request a variant from the system. 
Temporary workarounds are okay (one sprint max) — use a class wrapper and comment with the issue link.

**Q: What if I need a component that doesn't exist?**
A: Ask in #[design-system-channel] first. The component might be planned or in another team's code. 
If it's genuinely new, file a feature request. Don't build it locally.

**Q: Do I have to use TypeScript types?**
A: No, but they're available if you use TypeScript. Prop validation happens at runtime for non-TS users.

**Q: How often do I need to update the design system package?**
A: Update at least monthly. We backport security fixes to the last two minor versions. 
Major version updates are documented in a migration guide.

**Q: What's the difference between tokens and component props?**
A: Tokens are values (colors, spacing). Props are component options (size, variant). 
Use both together: a Button's variant sets its colors via tokens internally.
```

## Quality Checks

1. **Completeness for new engineers:** Can someone with zero prior design system experience follow this and render a component by Step 5?
2. **Copy-paste commands:** All install and import commands are directly executable — no placeholders in the command itself. Placeholders are in brackets and marked.
3. **Runnable code examples:** Every code example is complete and renders something visible (not fragments).
4. **Anti-patterns are specific:** Each mistake references an actual pattern, not generic advice. Includes "don't" and "do instead" for each.
5. **Token usage shows wrong vs right:** Before/after code example demonstrates the impact of the mistake.
6. **Testing coverage:** Unit testing, visual regression, and accessibility testing are all mentioned with enough detail to get started.
7. **No forward references:** Each section stands alone. No "see Step X" or "we'll explain later."

## Small-system note

For systems with fewer than 5 components, compress the onboarding:

- Compress "Using components" into a single example (install → import → render one component).
- Name every component in the overview so nothing is left implicit.
- Collapse "Installation and setup" + "Using components" into one section if the system is very small.
- Shorten "Your first two weeks" to "Your first week" with 3-4 tasks.
- Remove the quick reference card (too little to reference).
