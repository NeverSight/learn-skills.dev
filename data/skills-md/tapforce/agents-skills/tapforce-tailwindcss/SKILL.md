---
name: tapforce-tailwindcss
description: Best practices for setting up and developing UX/UI for projects using Tailwind CSS ^4. Use when setting up new projects with Tailwind CSS support or when projects have Tailwind CSS installed.
license: ISC
metadata:
  author: tapforce
  version: "1.0"
compatibility: Requires Node.js ^20.0.0, Tailwind CSS ^4.0.0, pnpm ^10.0.0
allowed-tools: Bash Read Write
---

# Tapforce Tailwind CSS Skill

This skill provides best practices for setting up and developing UX/UI for projects using Tailwind CSS ^4.

## When to Use

Use this skill when:
- Setting up a new project that needs Tailwind CSS support
- Working with projects that have Tailwind CSS installed
- Configuring Tailwind CSS ^4 for different project types
- Implementing UI components with Tailwind CSS utilities

## Requirements

- Project uses Tailwind CSS ^4 or needs to start with Tailwind CSS
- Project must be supported by Tailwind CSS (see installation guides)
- Node.js ^20.0.0 environment
- Prefer pnpm ^10.0.0 as package manager

## Project Validation

### Check Existing Installation

If the project already has Tailwind CSS installed:

1. **Check version**: Verify Tailwind CSS version is ^4.0.0
2. **Compatibility**: Ensure project type supports Tailwind CSS ^4
3. **Configuration**: Check for proper Tailwind CSS setup

If version doesn't match ^4.0.0, refuse to continue and recommend upgrade.

### Project Type Support

Verify project type compatibility from official documentation:
- Vite: https://tailwindcss.com/docs/installation/using-vite
- PostCSS: https://tailwindcss.com/docs/installation/using-postcss
- Tailwind CLI: https://tailwindcss.com/docs/installation/tailwind-cli
- Framework guides: https://tailwindcss.com/docs/installation/framework-guides
- Play CDN: https://tailwindcss.com/docs/installation/play-cdn

## Installation Setup

### Preferred Project Setup

For best practices, projects should:
- Use Node.js as base
- Use pnpm as package manager
- Use popular JS frameworks (SvelteKit, Next.js, Nuxt.js, etc.)
- Default to SvelteKit if framework not decided

### Installation by Project Type

See [installation guide](references/installation.md) for detailed setup instructions based on project type.

## Tailwind CSS ^4 Compatibility

Tailwind CSS ^4 has breaking changes compared to ^3. See [compatibility guide](references/compatibility.md) for detailed information.

## Core Concepts

### Styling with Utility Classes

Use utility classes for styling instead of custom CSS. See [styling guide](references/styling.md) for comprehensive examples.

### Hover, Focus, and Other States

Implement interactive states using Tailwind's state variants. See [states guide](references/states.md) for patterns and examples.

### Responsive Design

Create responsive layouts using Tailwind's breakpoint system. See [responsive guide](references/responsive.md) for implementation patterns.

### Dark Mode

Implement dark mode support using Tailwind's dark mode utilities. See [dark mode guide](references/dark-mode.md) for setup strategies.

### Theme and Colors

Customize themes and work with colors effectively. See [theme guide](references/theme.md) for customization patterns.

### Adding Custom Styles

Add custom CSS when utilities aren't sufficient. See [custom styles guide](references/custom-styles.md) for best practices.

### Detecting Classes in Source Files

Understand how Tailwind detects classes in your source files. See [detection guide](references/detection.md) for configuration.

### Functions and Directives

Use Tailwind's CSS functions and directives. See [functions guide](references/functions.md) for advanced usage.

## Rules

This skill includes the following rules:

### Utility-First Approach
- **Rule**: [utility-first](rules/utility-first.md)
- **Description**: Rules for preferring Tailwind utilities over custom CSS

### Arbitrary Values
- **Rule**: [arbitrary-values](rules/arbitrary-values.md)
- **Description**: Rules for using arbitrary values when built-in utilities are insufficient

### CSS Organization
- **Rule**: [css-organization](rules/css-organization.md)
- **Description**: Rules for organizing CSS files and custom styles

### Utility Directives
- **Rule**: [utility-directives](rules/utility-directives.md)
- **Description**: Rules for defining custom utilities with @utility directive

### Color Consistency
- **Rule**: [color-consistency](rules/color-consistency.md)
- **Description**: Rules for maintaining consistent color value formats

### Version Validation
- **Rule**: [version-validation](rules/version-validation.md)
- **Description**: Rules for validating Tailwind CSS ^4 installation and compatibility

## Best Practices

- Always prefer Tailwind ^4 utility classes over custom CSS
- Use arbitrary values for custom styling when built-in classes are insufficient
- Centralize custom CSS variables in the root CSS file
- Use @utility directive for shared custom styles
- Maintain consistent color value formats (hsl() by default, oklch() for shadcn-svelte)
- Reference official documentation for framework-specific setup
- Test responsive designs across all breakpoints
- Implement proper dark mode support
- Use semantic HTML with Tailwind utilities for accessibility
