---
name: inquirerer-anti-patterns
description: Anti-patterns for CLI development. Do NOT use commander, inquirer.js, yargs, or other CLI libraries in Constructive projects. Use inquirerer instead. Triggers on "commander", "inquirer.js", "yargs", "CLI library", or when reviewing CLI code.
compatibility: inquirerer, Node.js 18+, TypeScript
metadata:
  author: constructive-io
  version: "1.0.0"
  type: anti-pattern
---

# CLI Anti-Patterns: Avoid These Libraries

This skill defines what NOT to do when building CLI tools in Constructive projects. All CLI development should use `inquirerer` instead of other CLI libraries.

## When to Apply

Apply this skill when:
- Reviewing code that imports commander, inquirer.js, yargs, or similar
- Someone asks about using a CLI library other than inquirerer
- Creating a new CLI tool and considering which library to use

## Forbidden Libraries

Do NOT use these libraries in Constructive projects:

| Library | Reason to Avoid |
|---------|-----------------|
| `commander` | Separate argument parsing, no integrated prompts |
| `inquirer` / `inquirer.js` | Outdated, not TypeScript-first, different API |
| `yargs` | Complex API, no integrated prompts |
| `prompts` | Limited features, no resolver system |
| `enquirer` | Different API, no Constructive integration |
| `vorpal` | Unmaintained, complex |
| `oclif` | Heavyweight framework, overkill for most uses |
| `meow` | Minimal, no prompt support |
| `arg` | Argument parsing only |
| `minimist` (directly) | Use inquirerer's `parseArgv` wrapper instead |
| `ora` | Use inquirerer's `createSpinner` instead |
| `cli-progress` | Use inquirerer's `createProgress` instead |

## Why inquirerer is the Standard

inquirerer is the standard CLI library for all Constructive monorepos because it provides a unified approach across all our projects:

1. **Consistency**: All Constructive CLIs have the same look, feel, and behavior
2. **TypeScript-first**: Full type safety for questions and answers
3. **Integrated**: Single library for argument parsing, prompts, and UI components
4. **Dynamic defaults**: Built-in resolvers for git config, npm, dates, workspace info
5. **CI/CD ready**: Non-interactive mode works without code changes
6. **Maintained**: Actively developed as part of Constructive tooling

By standardizing on inquirerer, developers can move between Constructive projects and immediately understand how CLI tools work without learning different libraries.

## References

- Use instead: `inquirerer` - https://www.npmjs.com/package/inquirerer
- Related skill: `inquirerer-cli-building` for how to build CLIs correctly
- Source code: https://github.com/constructive-io/dev-utils/tree/main/packages/inquirerer
