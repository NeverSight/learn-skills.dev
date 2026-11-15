---
name: instrument-feature-flags
description: >-
  Add PostHog feature flags to gate new functionality. Use after implementing
  features or reviewing PRs to ensure safe rollouts with feature flag controls.
  Also handles initial PostHog SDK setup if not yet installed.
metadata:
  author: PostHog
---

# Add PostHog feature flags

Use this skill to add PostHog feature flags that gate new or changed functionality. Use it after implementing features or reviewing PRs to ensure safe rollouts with feature flag controls. If PostHog is not yet installed, this skill also covers initial SDK setup. Supports any platform or language.

Supported platforms: React, Next.js, React Native, Web (JavaScript), Node.js, Python, PHP, Ruby, Go, Java, Rust, .NET, Elixir, Android, iOS, Flutter, and the REST API.

## Instructions

Before you edit anything, read `references/COMMANDMENTS.md`. It lists the rules every PostHog install follows: how to install the SDK, where to create the client, how to identify users, Content Security Policy and multi-platform apps, plus the rules for this framework.

Follow these steps IN ORDER:

STEP 1: Analyze the codebase and detect the platform.
  -
 Look for dependency files (package.json, pubspec.yaml, Podfile, Package.swift, requirements.txt, go.mod, Gemfile, composer.json, mix.exs, etc.) to determine the language and framework.
  -
 Look for lockfiles (pnpm-lock.yaml, package-lock.json, yarn.lock, bun.lockb, go.sum, pubspec.lock, Podfile.lock, Package.resolved, mix.lock) to determine the package manager.
  - Check for existing PostHog setup (SDK initialization, env vars, etc.). If PostHog is already installed and initialized, skip to STEP 3.

STEP 2: Research instrumentation. (Skip if PostHog is already set up.)
  2.1. Find the reference file below that matches the detected platform — it is the source of truth for SDK initialization, flag evaluation methods, and framework-specific patterns. Read it now.
  2.2. If no reference matches, fall back to your general knowledge and web search. Use posthog.com/docs as the primary search source.

STEP 3: Create or find the feature flag.
  - Check if a PostHog MCP server is connected. If available, use its tools to search for an existing feature flag the user wants to instrument, or create a new one.
  - If no MCP server is available, instruct the user to create the flag in the PostHog dashboard.

STEP 4: Plan release conditions.
  - Determine the rollout strategy (percentage rollout, user targeting, group targeting, etc.).
  - Plan how the feature flag will gate the new functionality in code.

STEP 5: Instrument the feature.
  - Add the feature flag code following the platform-specific reference patterns.
  - Use server-side evaluation when possible to avoid UI flicker.
  - Do not alter the fundamental architecture of existing files. Make additions minimal and targeted.
  - You must read a file immediately before attempting to write it.

STEP 6: Set up environment variables.
  - Check if the project already has PostHog environment variables configured (e.g. in `.env`, `.env.local`, or framework-specific env files). If valid values already exist, skip this step.
  - If the PostHog project token is missing, use the project token that the tool or CLI which started this setup already gave you (for example in its output or instructions).
  - If it gave you none, use the PostHog MCP server's `projects-get` tool to retrieve the project's `api_token`. If multiple projects are returned, ask the user which project to use. If the MCP server is not connected or not authenticated, ask the user for their PostHog project token instead.
  - For the PostHog host URL: use the host that the tool or CLI which started this setup already gave you. If it gave you none, check the `projects-get` MCP response for a `region` field — `US` maps to `https://us.i.posthog.com`, `EU` maps to `https://eu.i.posthog.com`. If you still have no host from the calling tool, the MCP response, or existing project configuration, ask the user: "Are you on PostHog US Cloud or EU Cloud?" Do not assume US Cloud.
  - Write these values to the appropriate env file using the framework's naming convention.
  - Reference these environment variables in code instead of hardcoding them.
  - List the key names in `.env.example`, or the env template the project already uses, with placeholder values, so the next developer knows what to set. Create `.env.example` if the project has none. Never put real values in it.
  - Read the keys as optional: a missing key must never break the build or boot. Follow the missing-configuration rule in `references/COMMANDMENTS.md`.

## Reference files

- `references/react.md` - React feature flags installation
- `references/react-native.md` - React native feature flags installation
- `references/web.md` - Web feature flags installation
- `references/nodejs.md` - Node.js feature flags installation
- `references/python.md` - Python feature flags installation
- `references/django.md` - Django
- `references/flask.md` - Flask
- `references/php.md` - Php feature flags installation
- `references/laravel.md` - Laravel
- `references/ruby.md` - Ruby feature flags installation
- `references/ruby-on-rails.md` - Ruby on rails
- `references/go.md` - Go feature flags installation
- `references/java.md` - Java feature flags installation
- `references/rust.md` - Rust feature flags installation
- `references/dotnet.md` - .net feature flags installation
- `references/dotnet.md` - .net
- `references/elixir.md` - Elixir feature flags installation
- `references/android.md` - Android feature flags installation
- `references/ios.md` - Ios feature flags installation
- `references/usage.md` - Ios SDK usage
- `references/flutter.md` - Flutter feature flags installation
- `references/api.md` - API feature flags installation
- `references/next-js.md` - Next.js
- `references/adding-feature-flag-code.md` - Adding feature flag code
- `references/best-practices.md` - Best practices for production-ready flags
- `references/COMMANDMENTS.md` - Framework-specific rules the integration must follow

Each platform reference contains SDK-specific installation, flag evaluation, and code examples. Find the one matching the user's stack. If unlisted, use the API reference as a fallback.

## Key principles

- **Environment variables**: Always use environment variables for PostHog keys. Never hardcode them.
- **Minimal changes**: Add feature flag code alongside existing logic. Don't replace or restructure existing code.
- **Boolean flags first**: Default to boolean flag checks unless the user specifically asks for multivariate flags.
- **Server-side when possible**: Prefer server-side flag evaluation to avoid UI flicker.