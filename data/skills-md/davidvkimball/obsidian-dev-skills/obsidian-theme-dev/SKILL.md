---
name: obsidian-theme-dev
description: CSS/SCSS development patterns for Obsidian themes. Load when working with theme.css, SCSS variables, or CSS selectors.
---

# Obsidian Theme Development Skill

This skill provides patterns and rules for developing Obsidian themes, focusing on CSS/SCSS development, styling conventions, and theme-specific coding practices.

## Purpose

To ensure consistent theme development, proper CSS organization, and adherence to Obsidian's theming patterns and CSS variable usage.

## Scope

This skill covers:
- Writing or modifying CSS/SCSS for `theme.css`
- Working with Obsidian's CSS variables and theming system
- Implementing responsive design or dark/light mode support
- Debugging CSS layout or styling issues
- CSS/SCSS coding conventions for Obsidian themes

## Core Rules

- **Use Obsidian CSS Variables**: Always prefer Obsidian's built-in CSS variables over hardcoded values
- **Consistent Naming**: Use a consistent naming convention (BEM, prefixed classes, or other - see conventions file)
- **Mobile-First**: Consider mobile layouts and responsive design
- **Dark/Light Mode Support**: Test themes in both light and dark modes
- **Performance**: Minimize CSS complexity and avoid expensive selectors

## Bundled Resources

- `references/theme-best-practices.md`: Essential CSS patterns and Obsidian variable usage
- `references/theme-coding-conventions.md`: CSS/SCSS style guidelines and naming conventions