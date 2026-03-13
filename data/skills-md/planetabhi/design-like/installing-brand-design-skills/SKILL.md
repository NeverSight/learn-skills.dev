---
name: installing-brand-design-skills
description: Helps Claude install and use brand-specific design skills for popular product brands (Apple, Linear, Stripe, Shopify, Notion, Figma, Spotify, Slack, Discord, IBM, Salesforce) by running the design-like CLI to generate Agent Skills and IDE configuration so code and UI match the chosen brand’s design language.
---

# Main Instructions

Use this skill when the user wants code and UI that closely follow the visual language of a specific product brand (for example Apple, Airbnb, Linear, or Stripe) and is working in a project where they can run CLI commands.

This skill centers around the `design-like` CLI, which generates brand-specific Agent Skills and IDE configuration files. These give Claude and other coding agents concrete tokens, components, and guidelines so they can design like the selected brand.

When the user expresses a desire for brand-consistent UI, or mentions one of the supported brands, follow the steps below.

## Step-by-Step Guidance

1. **Confirm context and brand**
   - Ask the user which brand they want to design like (for example: Apple, Airbnb, Linear, Shopify, Stripe, Notion, Figma, Spotify, Slack, Discord, IBM, Salesforce).
   - Ask which IDE or agent environment they are using (for example: Claude Code, Cursor, VS Code, Antigravity).
   - Verify they can run `npx` commands in their project directory.

2. **Guide the user to install the brand design skill**
   - Instruct the user to navigate to their project root in a terminal.
   - Have them run the `design-like` CLI with the chosen brand:

```bash
npx design-like <brand>
```

   - If they are unsure which brand to pick, suggest a few options based on their product style and audience.
   - If they prefer an interactive flow, they can run:

```bash
npx design-like
```

   and select a brand from the prompt.

3. **Explain supported IDEs and where files are generated**
   - Explain that `design-like` detects the IDE or agent environment and writes files into the appropriate folders:
     - Claude Code: `.claude/skills/`
     - Cursor: `.cursor/rules/`
     - VS Code: `.vscode/instructions/`
     - Antigravity: `.agent/skills/`
   - Mention that the tool can also target a specific IDE explicitly using:

```bash
npx design-like <brand> --ide <claude|cursor|vscode|antigravity|all>
```

4. **Help the user choose options and flags**
   - If the user wants to install into a specific directory (for example a monorepo app), suggest:

```bash
npx design-like <brand> --target path/to/app
```

   - Recommend `--force` only when they explicitly want to overwrite any existing design-like files:

```bash
npx design-like <brand> --force
```

   - If they want to preview what will be written without applying changes (if supported), suggest using `--dry-run` or the equivalent option documented in the repository.

5. **Verify installation and explain what was created**
   - After the user runs the command, ask them to confirm that new files were created under their IDE’s configuration directory.
   - Explain that `design-like` typically creates:
     - An Agent Skill file `SKILL.md` describing how to design like the chosen brand.
     - A `tokens.json` (or similar) file containing design tokens (colors, typography, spacing, etc.).
     - IDE-specific rule or instruction files (for example `.mdc` rules for Cursor or `.instructions.md` for VS Code).
   - Encourage the user to keep these files under version control so teammates get the same design guidance.

6. **Use the brand design guidance in your coding session**
   - Once the brand design skill is installed, pay careful attention to its guidance:
     - Follow the brand’s color, typography, spacing, and motion tokens whenever you propose UI.
     - Use the recommended component patterns (buttons, cards, inputs, etc.).
     - Respect the brand’s accessibility, contrast, and layout guidelines.
   - When generating code, reference the specific brand tokens and examples provided by the installed skill instead of inventing your own design system.

7. **Suggest brand-consistent improvements proactively**
   - When reviewing or authoring components, suggest refactors that bring them closer to the installed brand’s patterns.
   - Offer to convert existing generic components to use the brand’s tokens, border radii, shadows, and motion curves.
   - If the user switches brands or wants to compare options, guide them to run the CLI again with a different brand and discuss trade-offs.

## Examples

- **Example 1: Setting up Apple-style UI in a new project**
  - User: “I want this app to look like Apple’s design language.”
  - Claude:
    1. Confirms they can run CLI commands in the project.
    2. Asks which IDE they are using.
    3. Guides them to run:

```bash
npx design-like apple
```

    4. Explains where files were written for their IDE.
    5. Starts generating components and layouts that follow the Apple design skill’s tokens and guidelines.

- **Example 2: Applying Linear’s style in Cursor**
  - User: “I’m using Cursor and I’d love my dashboard to feel like Linear.”
  - Claude:
    1. Asks the user to open a terminal at the project root.
    2. Instructs them to run:

```bash
npx design-like linear --ide cursor
```

    3. Explains that this will create a Cursor rule file under `.cursor/rules/`.
    4. Uses the installed Linear design guidance while proposing React components, Tailwind classes, or CSS.

## Best Practices

- **Clarify the brand and environment early**
  - Always confirm the desired brand and IDE/agent environment before giving installation commands or design recommendations.

- **Align generated UI with installed tokens**
  - After installation, consistently reference the brand’s tokens and component patterns when proposing code.
  - Avoid mixing arbitrary styles that conflict with the installed brand design.

- **Keep the user’s repo structure in mind**
  - When suggesting `--target`, make sure the path matches the user’s actual app directory (for example `apps/web` in a monorepo).

- **Encourage version control**
  - Recommend committing the generated skills and tokens so other collaborators and agents share the same design language.

- **Be transparent about limitations**
  - If the user cannot run CLI commands (for example in a restricted environment), explain that `design-like` works best when it can write files to the project, and offer to approximate the brand style manually using your knowledge of the brand’s design patterns.

