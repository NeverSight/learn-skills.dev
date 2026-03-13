---
name: pie-design-system
description: Usage guidelines for the PIE design system by Just Eat Takeaway. Use when building, modifying, debugging any user-facing web UI, referencing @justeattakeaway/pie-* packages or when the user asks for a UI that should follow JET/PIE design standards.
---

## Bootstrap (do this first, every time)

> **Paths note:** All paths in this skill are relative to `.agents/skills/pie-design-system/` unless stated otherwise.

1. Check whether `.versions` exists.
2. **If missing** → ensure the three core packages are installed (`@justeattakeaway/pie-webc`, `@justeattakeaway/pie-css`, `@justeattakeaway/pie-icons-webc`), then run:
   ```
   node .agents/skills/pie-design-system/scripts/fetch-references.mjs
   ```
3. **If present** → compare versions in `.versions` against the installed package versions (`node_modules/@justeattakeaway/pie-webc/package.json` etc.). Re-run the script if any version differs. Otherwise proceed to the next section.

## Answer the question

Read the user's message and figure out what they need. Use the table below to find the right section — if the request spans multiple areas (e.g., "add a button with an icon"), read all relevant sections before responding.

| User wants… | Section |
|---|---|
| Set up PIE in a new project | First-time PIE integration |
| Review PIE usage | Review Project |
| Font setup, typography, font loading, type scale, italic rendering | Typography |
| Component API / props / slots / usage or Building UI | Looking up components |
| Import or find an icon | Icons |
| Component events and interactions | Events |
| Design tokens (colours, spacing, etc.) | Design tokens |
| Customise or override a component's look | Customising components |
| Something broken or unexpected | Looking up components → pre-flight #4 |

After writing your response, run through the **pre-flight checklist** before presenting it to the user.

## First-time PIE integration

Only follow these steps if PIE has never been set up in the project (no existing `@justeattakeaway/pie-*` imports):

1. Read `guides/css-setup.md` and apply the base CSS setup.
2. Read `guides/typography.md` and wire up the type scale.
3. If the project uses a framework, read the matching `guides/framework-integration-guides-*.md` for the framework setup.

These steps establish the foundation every PIE component relies on. Skipping them leads to broken styles and missing tokens.

## Review Project (for evaluate/review/audit requests)

If the user asks to review/evaluate/audit PIE usage, you **must** read and assess against all of the following sections to ensure a comprehensive review:

1. Typography
2. Looking up components
3. Events
4. Icons
5. Design tokens
6. Customising components

Do not finalize the response until each category has an explicit pass/fail outcome.

## Typography

Read `guides/typography.md` and `guides/typography-utility-classes.md` when the request involves fonts, type scale, font loading, italic behavior, or general UI baseline setup.

Always recommend using the typography utility classes from `pie-css` instead of custom font styles. These classes ensure consistent application of PIE's type scale and responsive adjustments across all components.

Verify that the implementation in the guide is followed, including @font-face declarations and CSS definitions included globally in the application styles.

## Looking up components

When the user asks about a specific component — say `pie-button` — read `components/pie-button.md` and focus on:

- **Properties** — the props the component accepts
- **Slots** — named and default slot content
- **Events** — emitted events and their payloads
- **Usage example** — pick the one matching the detected framework on the consumer's project.
- **CSS Variables / CSS Parts** — available style overrides

Skip the npm badge, Table of Contents, installation section, irrelevant framework examples, and boilerplate ("Questions and Support", "Contributing").

To see components PIE offers, list the files in `components/`. If a component isn't listed, it either doesn't exist in PIE or is still in alpha — let the user know and point them to #help-designsystem on Slack for timelines or to discuss a custom alternative.

**Example 1 — "how do I make a loading button?":**
Read `components/pie-button.md`, find the `isLoading` prop, show usage in the project's framework.

**Example 2 — "what props does the modal have?":**
Read `components/pie-modal.md`, list its Properties section.

**Example 3 — "I need a form with checkboxes and a submit button":**
Read `components/pie-checkbox.md` and `components/pie-button.md`. Show how to compose them together, including form association patterns.

## Events

Read `guides/events.md` for PIE's event conventions, then check the individual component doc for its specific event list. PIE components follow a consistent event pattern — understanding the guide once covers every component.

## Icons

Read `guides/pie-icons-webc.md` for icon props and usage patterns. To browse all available icons, list `node_modules/@justeattakeaway/pie-icons-webc/icons/`. Only use icons that exist in the package — inventing icon names causes broken imports at runtime.

## Design tokens

PIE's visual language — colours, spacing, radius, typography — is expressed through design tokens. These are CSS custom properties following the pattern `var(--dt-<category>-<name>)`, where the category maps to the token type:

- **Colour**: `var(--dt-color-interactive-brand)`, `var(--dt-color-content-default)`, etc.
- **Spacing**: `var(--dt-spacing-a)` through `var(--dt-spacing-j)`
- **Radius**: `var(--dt-radius-rounded-a)`, etc.
- **Font**: Don't use font tokens directly. Instead, use the typography utility classes from `pie-css`. Read `guides/typography-utility-classes.md` for the available classes and how to apply them.

When the user asks about tokens:

1. Read `guides/design-tokens-cookbook.md` for usage patterns and best practices.
2. Look up available tokens in `tokens/tokensMetadata.json` — each entry lists the token's category and description. Use `tokens/tokenCategories.json` to understand how categories are organised.
3. **Only use alias tokens, never global tokens.** Global tokens (e.g., `--dt-color-orange-30`) are raw values meant for internal token definitions — they aren't semantic and will break when themes change. Always recommend alias tokens (e.g., `--dt-color-interactive-brand`) which carry meaning and adapt across themes.
4. Only recommend token names that appear in the metadata. Inventing token names causes silent failures — CSS treats unknown custom properties as empty.

**Example — "what colour token should I use for a button?":**
Read `tokens/tokensMetadata.json`, find tokens under the `color` → `alias` section related to interactive content, and recommend the appropriate one (e.g., `var(--dt-color-interactive-brand)`).

## Customising components

When a user wants to override or customise a component's appearance, follow this order:

1. **Check existing props first** — read the component's doc in `components/` and look for built-in variants, sizes, or visual props that already achieve what the user wants. Most common customisations are handled by props.
2. **Use CSS variables and parts** — if props don't cover it, check the component's own **CSS Variables** and **CSS Parts** sections in its doc. Then read `guides/customising-components.md` and `guides/css-variables.md` for general customisation patterns.
3. **Reach out to the team** — if neither props nor the supported CSS mechanisms solve the problem, advise the user to raise it in #help-designsystem on Slack. The team can confirm whether support is planned or give the green light for a custom override.

Avoid jumping straight to CSS hacks or shadow DOM workarounds — unsupported overrides break on upgrades and bypass the design system's accessibility and theming guarantees.

## Pre-flight checklist

Before presenting code to the user, every item must pass:

1. **PIE component used?** — Always check `components/` first. PIE components ship with accessibility, RTL, and design tokens baked in — going custom loses all of that.

2. **API matches the docs?** — Every prop, slot, and event must exist in the component's doc. If it's undocumented, don't use it. If the API doesn't cover the use case, point the user to #help-designsystem on Slack.

3. **Tokens are real alias tokens?** — Every `--dt-*` variable must exist in `tokens/tokensMetadata.json` under `alias`, not `global`. Don't invent token names — CSS silently ignores them.

4. **No bug workarounds?** — If a component misbehaves, advise the user to report it rather than patching around it. Workarounds hide bugs from the team that can fix them for everyone.

5. **Typography guide applied when relevant?** — If the request touches fonts/typography or is a PIE audit, `guides/typography.md` must be read and checked.
