---
name: instrument-product-analytics
description: >-
  Add PostHog product analytics events to track user behavior. Use after
  implementing new features or reviewing PRs to ensure meaningful user actions
  are captured. Also handles initial PostHog SDK setup if not yet installed.
metadata:
  author: PostHog
---

# Add PostHog product analytics events

Use this skill to add product analytics events (capture calls) that track meaningful user actions in new or changed code. Use it after implementing features or reviewing PRs to ensure key user behaviors are captured. If PostHog is not yet installed, this skill also covers initial SDK setup. Supports any framework or language.

Supported frameworks and languages: Next.js, React Router, Nuxt, Vue, TanStack Start, SvelteKit, Astro, Angular, Django, Flask, FastAPI, Laravel, PHP, Ruby on Rails, Go, Elixir, Android, iOS, Flutter, React Native, Expo, and more.

## Instructions

Follow these steps IN ORDER:

STEP 1: Analyze the codebase and detect the platform.
  -
 Look for dependency files (package.json, pubspec.yaml, Podfile, Package.swift, requirements.txt, Gemfile, composer.json, go.mod, mix.exs, etc.) to determine the framework and language.
  -
 Look for lockfiles (pnpm-lock.yaml, package-lock.json, yarn.lock, bun.lockb, go.sum, pubspec.lock, Podfile.lock, Package.resolved, mix.lock) to determine the package manager.
  - Check for existing PostHog setup. If PostHog is already installed and initialized, skip to STEP 5.

STEP 2: Research integration. (Skip if PostHog is already set up.)
  2.1. Find the reference file below that matches the detected framework — it is the source of truth for SDK initialization, provider setup, and event capture patterns. Read it now.
  2.2. If no reference matches, fall back to your general knowledge and web search. Use posthog.com/docs as the primary search source.

STEP 3: Install the PostHog SDK. (Skip if PostHog is already set up.)
  - Add the PostHog SDK package for the detected platform. Do not manually edit package.json — use the package manager's install command.

STEP 4: Initialize PostHog. (Skip if PostHog is already set up.)
  - Follow the framework reference for where and how to initialize. This varies significantly by framework (e.g., instrumentation-client.ts for Next.js 15.3+, AppConfig.ready() for Django, create_app() for Flask).

STEP 5: Plan event tracking.
  - From the project's file list, select between 10 and 15 files that might have interesting business value for event tracking, especially conversion and churn events.
  - Also look for files related to login that could be used for identifying users, along with error handling.
  - Find any existing `posthog.capture()` code. Make note of event name formatting. Don't duplicate existing events; supplement them.
  - Track actions only, not pageviews (those can be captured automatically). Exceptions can be made for "viewed"-type events at the top of a conversion funnel.
  - **Server-side events are REQUIRED** if the project includes any instrumentable server-side code (API routes, server actions, webhook handlers, payment/checkout completion, authentication endpoints).

STEP 6: Implement event capture.
  - For each planned event, add `posthog.capture()` calls with useful properties.
  - If a file already has existing integration code for other tools or services, don't overwrite or remove that code. Place PostHog code below it.
  - Do not alter the fundamental architecture of existing files. Make additions minimal and targeted.
  - You must read a file immediately before attempting to write it.

STEP 7: Identify users.
  - Add PostHog `identify()` calls on the client side during login and signup events. Use the contents of login and signup forms to identify users on submit.
  - If both frontend and backend exist, pass the client-side session and distinct ID using `X-POSTHOG-DISTINCT-ID` and `X-POSTHOG-SESSION-ID` headers to the server-side code. On the server side, make sure events have a matching distinct ID.

STEP 8: Add error tracking.
  - Add PostHog exception capture error tracking to relevant files, particularly around critical user flows and API boundaries.

STEP 9: Set up environment variables.
  - Check if the project already has PostHog environment variables configured (e.g. in `.env`, `.env.local`, or framework-specific env files). If valid values already exist, skip this step.
  - If the PostHog project token is missing, use the PostHog MCP server's `projects-get` tool to retrieve the project's `api_token`. If multiple projects are returned, ask the user which project to use. If the MCP server is not connected or not authenticated, ask the user for their PostHog project token instead.
  - For the PostHog host URL: check the `projects-get` MCP response for a `region` field — `US` maps to `https://us.i.posthog.com`, `EU` maps to `https://eu.i.posthog.com`. If the region is not available from the MCP response or from existing project configuration, ask the user: "Are you on PostHog US Cloud or EU Cloud?" Do not assume US Cloud.
  - Write these values to the appropriate env file using the framework's naming convention.
  - Reference these environment variables in code instead of hardcoding them.

STEP 10: Verify and clean up.
  - Check the project for errors. Look for type checking or build scripts in package.json.
  - Ensure any components created were actually used.
  - Run any linter or prettier-like scripts found in the package.json, but ONLY on the files you have edited or created during this session. Never run formatting or linting across the entire project's codebase.

## Reference files

- `references/EXAMPLE-next-app-router.md` - next-app-router example project code
- `references/EXAMPLE-next-pages-router.md` - next-pages-router example project code
- `references/EXAMPLE-react-react-router-6.md` - react-react-router-6 example project code
- `references/EXAMPLE-react-react-router-7-framework.md` - react-react-router-7-framework example project code
- `references/EXAMPLE-react-react-router-7-data.md` - react-react-router-7-data example project code
- `references/EXAMPLE-react-react-router-7-declarative.md` - react-react-router-7-declarative example project code
- `references/EXAMPLE-nuxt-3-6.md` - nuxt-3-6 example project code
- `references/EXAMPLE-nuxt-4.md` - nuxt-4 example project code
- `references/EXAMPLE-vue-3.md` - vue-3 example project code
- `references/EXAMPLE-react-tanstack-router-file-based.md` - react-tanstack-router-file-based example project code
- `references/EXAMPLE-react-tanstack-router-code-based.md` - react-tanstack-router-code-based example project code
- `references/EXAMPLE-tanstack-start.md` - tanstack-start example project code
- `references/EXAMPLE-sveltekit.md` - sveltekit example project code
- `references/EXAMPLE-astro-static.md` - astro-static example project code
- `references/EXAMPLE-astro-view-transitions.md` - astro-view-transitions example project code
- `references/EXAMPLE-astro-ssr.md` - astro-ssr example project code
- `references/EXAMPLE-astro-hybrid.md` - astro-hybrid example project code
- `references/EXAMPLE-angular.md` - angular example project code
- `references/EXAMPLE-django.md` - django example project code
- `references/EXAMPLE-flask.md` - flask example project code
- `references/EXAMPLE-fastapi.md` - fastapi example project code
- `references/EXAMPLE-python.md` - python example project code
- `references/EXAMPLE-laravel.md` - laravel example project code
- `references/EXAMPLE-php.md` - php example project code
- `references/EXAMPLE-ruby-on-rails.md` - ruby-on-rails example project code
- `references/EXAMPLE-ruby.md` - ruby example project code
- `references/EXAMPLE-android.md` - android example project code
- `references/EXAMPLE-swift.md` - swift example project code
- `references/EXAMPLE-react-native.md` - react-native example project code
- `references/EXAMPLE-expo.md` - expo example project code
- `references/next-js.md` - Next.js
- `references/react-router-v6.md` - React router v6
- `references/react-router-v7-framework-mode.md` - React router v7 framework mode (remix v3)
- `references/react-router-v7-data-mode.md` - React router v7 data mode
- `references/react-router-v7-declarative-mode.md` - React router v7 declarative mode
- `references/nuxt-js-3-6.md` - Nuxt.js (v3.0 to v3.6)
- `references/nuxt-js.md` - Nuxt.js
- `references/vue-js.md` - Vue.js
- `references/tanstack-start.md` - Tanstack start
- `references/svelte.md` - Svelte
- `references/astro.md` - Astro
- `references/angular.md` - Angular
- `references/django.md` - Django
- `references/flask.md` - Flask
- `references/python.md` - Python
- `references/posthog-python.md` - PostHog python SDK
- `references/dotnet.md` - .net
- `references/elixir.md` - Elixir
- `references/go.md` - Go
- `references/laravel.md` - Laravel
- `references/php.md` - Php
- `references/ruby-on-rails.md` - Ruby on rails
- `references/ruby.md` - Ruby
- `references/android.md` - Android
- `references/ios.md` - Ios
- `references/usage.md` - Ios SDK usage
- `references/configuration.md` - Ios SDK configuration
- `references/flutter.md` - Flutter
- `references/react-native.md` - React native
- `references/identify-users.md` - Identify users
- `references/COMMANDMENTS.md` - Framework-specific rules the integration must follow

Each framework reference contains SDK-specific installation, initialization, and usage patterns. Find the one matching the user's stack.

## Key principles

- **Environment variables**: Always use environment variables for PostHog keys. Never hardcode them.
- **Minimal changes**: Add PostHog code alongside existing integrations. Don't replace or restructure existing code.
- **Match the docs**: Follow the framework reference's initialization and capture patterns exactly.