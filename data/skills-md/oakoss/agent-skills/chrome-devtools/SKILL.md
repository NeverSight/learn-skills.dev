---
name: chrome-devtools
description: 'Browser automation via Chrome extension and DevTools MCP. Use when controlling a logged-in Chrome browser, automating workflows, filling forms, extracting data, debugging web apps, reading console logs, or running scheduled browser tasks. Use for browser testing, form automation, data extraction, web scraping, authenticated browsing.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
user-invocable: false
---

# Chrome DevTools Skill

Control a real Chrome browser with Claude. The Chrome extension runs inside an authenticated browser session, allowing interaction with sites the user is already logged into -- Gmail, Google Docs, Notion, CRMs, and more.

## Overview

Two integration paths exist: Claude Code + Chrome Extension (terminal-based browser control via `claude --chrome`) and Chrome DevTools MCP (26 browser automation tools via Model Context Protocol). Both operate on a real Chrome instance with existing logins, requiring no re-authentication. The Chrome extension also supports workflow shortcuts, scheduled recurring tasks, and multi-tab coordination independently of Claude Code.

## Quick Reference

| Integration             | Setup                                                                        | Best For                              |
| ----------------------- | ---------------------------------------------------------------------------- | ------------------------------------- |
| Claude Code + Extension | `claude --chrome`                                                            | Terminal-based browser control        |
| Chrome DevTools MCP     | `claude mcp add chrome-devtools --scope user npx chrome-devtools-mcp@latest` | Programmatic automation via MCP tools |

| Capability | Tools/Methods                                                        |
| ---------- | -------------------------------------------------------------------- |
| Navigation | Navigate URLs, create/close/switch tabs, resize windows              |
| Input      | Click, type, fill forms, drag, hover, press keys, upload files       |
| Extraction | Read page content, DOM state, console logs, network requests         |
| Debugging  | Screenshots, DOM snapshots, evaluate JavaScript, performance tracing |
| Emulation  | Device emulation, viewport resizing                                  |
| Recording  | Record browser interactions as GIFs, save workflow shortcuts         |
| Scheduling | Workflow shortcuts with daily/weekly/monthly/annual triggers         |

| Requirement                | Minimum                  |
| -------------------------- | ------------------------ |
| Google Chrome              | Latest stable            |
| Claude in Chrome Extension | 1.0.36+                  |
| Claude Code CLI            | 2.0.73+                  |
| Claude Plan                | Pro, Team, or Enterprise |
| Node.js (DevTools MCP)     | 20.19+                   |

**Not supported**: Other Chromium browsers (Brave, Arc, Edge), WSL, headless mode (extension path only; DevTools MCP supports headless), mobile devices.

## Common Mistakes

| Mistake                                            | Correct Pattern                                                                                          |
| -------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Running browser automation without `--chrome` flag | Start Claude Code with `claude --chrome` or enable Chrome by default via `/chrome` settings              |
| Trying to take over existing tabs                  | Claude opens new tabs for tasks; it does not hijack tabs you already have open                           |
| Not handling CAPTCHAs and modal dialogs manually   | Claude pauses at CAPTCHAs, login prompts, and modals; dismiss them yourself then tell Claude to continue |
| Using ambiguous instructions for form filling      | Be specific about field names, values, and order; ambiguous prompts produce inconsistent results         |
| Requesting all console logs without filtering      | Specify log patterns or error types; requesting everything floods context with noise                     |
| Enabling Chrome by default without need            | Increases context usage since browser tools are always loaded; use `--chrome` flag only when needed      |
| Using DevTools MCP without `--scope user`          | Add `--scope user` to make the MCP server available across all projects                                  |

## Delegation

- **Automate repetitive browser workflows across sites**: Use `Task` agent with Chrome extension to fill forms, extract data, or navigate multi-step flows
- **Debug frontend issues with console and network inspection**: Use `Explore` agent with DevTools MCP to capture console errors, network failures, and DOM state
- **Plan complex multi-tab data extraction pipelines**: Use `Plan` agent to design the workflow steps before executing browser automation
- **Record and schedule recurring browser tasks**: Use Chrome extension shortcuts with scheduling for daily/weekly automation

## References

- [Claude Code Chrome integration](references/claude-code-integration.md) -- setup, capabilities, and how the extension communicates with Claude Code
- [Chrome DevTools MCP tools](references/devtools-mcp.md) -- all 26 MCP tools organized by category with configuration options
- [Browser automation workflows](references/automation-workflows.md) -- common patterns for testing, data extraction, and content management
- [Workflow shortcuts and scheduling](references/shortcuts-scheduling.md) -- creating reusable shortcuts and scheduled recurring tasks
- [Troubleshooting and best practices](references/troubleshooting.md) -- fixing connection issues, handling dialogs, and security considerations
