---
name: google-styleguides-skills
description: Complete collection of Google's official style guides for 17 languages. Includes TypeScript, JavaScript, Python, Java, Go, C++, C#, Swift, Objective-C, HTML/CSS, AngularJS, Shell, R, Common Lisp, Vim Script, JSON, and Markdown. Production-ready coding standards used across Google's engineering organization, formatted for AI agent consumption.
---

# Google Style Guides

> Official Google style guides for 17 languages — packaged for AI coding agents.

This skill pack includes all 17 official Google style guides from https://google.github.io/styleguide/

## Included Style Guides

### Frontend
- **TypeScript** - Types, interfaces, naming, null handling, enums, imports
- **JavaScript** - ES6+, modules, naming, formatting, JSDoc
- **HTML/CSS** - Formatting, naming, semantics, accessibility
- **AngularJS** - Controllers, services, directives, modules

### Backend
- **Python** - PEP 8, type hints, docstrings, imports, comprehensions
- **Java** - Naming, formatting, Javadoc, exceptions, best practices
- **Go** - Formatting, naming, comments, error handling, concurrency
- **C++** - Headers, naming, formatting, classes, memory management
- **C#** - Naming, formatting, LINQ, async/await, XML docs

### Mobile
- **Swift** - Naming, optionals, protocols, error handling, formatting
- **Objective-C** - Naming, formatting, memory management, protocols

### Other
- **Shell** - Bash scripting, naming, error handling, portability
- **R** - Naming, formatting, functions, documentation
- **Common Lisp** - Naming, formatting, macros, documentation
- **Vim Script** - Plugin structure, naming, portability
- **JSON** - Formatting, naming, structure, comments
- **Markdown** - Formatting, structure, links, lists

## Installation Options

### Install Everything (This Skill)
```bash
npx skills add testdino-hq/google-styleguides-skills
```

### Install Individual Languages
```bash
# Frontend
npx skills add testdino-hq/google-styleguides-skills/typescript
npx skills add testdino-hq/google-styleguides-skills/javascript
npx skills add testdino-hq/google-styleguides-skills/html-css
npx skills add testdino-hq/google-styleguides-skills/angularjs

# Backend
npx skills add testdino-hq/google-styleguides-skills/python
npx skills add testdino-hq/google-styleguides-skills/java
npx skills add testdino-hq/google-styleguides-skills/go
npx skills add testdino-hq/google-styleguides-skills/cpp
npx skills add testdino-hq/google-styleguides-skills/csharp

# Mobile
npx skills add testdino-hq/google-styleguides-skills/swift
npx skills add testdino-hq/google-styleguides-skills/objective-c

# Other
npx skills add testdino-hq/google-styleguides-skills/shell
npx skills add testdino-hq/google-styleguides-skills/r
npx skills add testdino-hq/google-styleguides-skills/common-lisp
npx skills add testdino-hq/google-styleguides-skills/vim-script
npx skills add testdino-hq/google-styleguides-skills/json
npx skills add testdino-hq/google-styleguides-skills/markdown
```

## Golden Rules Across All Languages

### Naming
- **Be consistent** - Follow language conventions
- **Be descriptive** - Clarity over brevity
- **Be conventional** - Use established patterns

### Formatting
- **Automate it** - Use language-specific formatters
- **Be consistent** - Same style across the codebase
- **Follow standards** - Don't reinvent formatting rules

### Documentation
- **Document public APIs** - Help users understand interfaces
- **Explain why, not what** - Code shows what, comments explain why
- **Keep it updated** - Outdated docs are worse than no docs

### Code Quality
- **Prefer clarity** - Readable code over clever code
- **Handle errors** - Don't ignore error conditions
- **Test your code** - Automated tests catch regressions

## How It Works

When you install this skill:
1. The style guides are copied to `.kiro/skills/` in your project
2. Your AI coding agent reads them when generating code
3. Generated code follows Google's official style conventions automatically

## License

This project is licensed under the [MIT License](LICENSE).

Copyright (c) 2026 TestDino

## Source

All content derived from Google's official style guides:  
https://google.github.io/styleguide/
