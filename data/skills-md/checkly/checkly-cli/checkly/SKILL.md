---
name: checkly
description: Set up, create, test and manage monitoring checks using the Checkly CLI. Use when working with API Checks, Browser Checks, URL Monitors, ICMP Monitors, Playwright Check Suites, Heartbeat Monitors, Alert Channels, Dashboards, or Status Pages.
allowed-tools: Bash(npx:checkly:*) Bash(npm:create:checkly@latest) Bash(npm:install:*)
metadata:
  author: checkly
---

# Checkly

The Checkly CLI provides all the required information via the `npx checkly skills` command.

Use `npx checkly skills` to list all available actions, and `npx checkly skills <action>` to access up-to-date information on how to use the Checkly CLI for each action.

## Progressive Disclosure via `npx checkly skills`

The skill is structured for efficient context usage:

1. **Metadata** (~80 tokens): Name and description in frontmatter
2. **Core Instructions** (~1K tokens): Main SKILL.md content with links to reference commands
3. **Reference Commands** (loaded on demand): Detailed construct documentation with examples

Agents load what they need for each task.

### `npx checkly skills initialize`
Learn how to initialize and set up a new Checkly CLI project from scratch.

### `npx checkly skills configure`
Learn how to create and manage monitoring checks using Checkly constructs and the CLI.

#### `npx checkly skills configure api-checks`
Api Check construct (`ApiCheck`), assertions, and authentication setup scripts

#### `npx checkly skills configure browser-checks`
Browser Check construct (`BrowserCheck`) with Playwright test files

#### `npx checkly skills configure playwright-checks`
Playwright Check Suite construct (`PlaywrightCheck`) for multi-browser test suites

#### `npx checkly skills configure multistep-checks`
Multistep Check construct (`MultiStepCheck`) for complex user flows

#### `npx checkly skills configure tcp-monitors`
TCP Monitor construct (`TcpMonitor`) with assertions

#### `npx checkly skills configure url-monitors`
URL Monitor construct (`UrlMonitor`) with assertions

#### `npx checkly skills configure dns-monitors`
DNS Monitor construct (`DnsMonitor`) with assertions

#### `npx checkly skills configure icmp-monitors`
ICMP Monitor construct (`IcmpMonitor`) with latency and packet loss assertions

#### `npx checkly skills configure heartbeat-monitors`
Heartbeat Monitor construct (`HeartbeatMonitor`)

#### `npx checkly skills configure check-groups`
CheckGroupV2 construct (`CheckGroupV2`) for organizing checks

#### `npx checkly skills configure alert-channels`
Email (`EmailAlertChannel`), Phone (`PhoneCallAlertChannel`), and Slack (`SlackAlertChannel`) alert channels

#### `npx checkly skills configure supporting-constructs`
Status pages (`StatusPage`), dashboards (`Dashboard`), maintenance windows (`MaintenanceWindow`), and private locations (`PrivateLocation`)
