---
name: nuxt-users
description: Configure and use the nuxt-users module for Nuxt 3 and Nuxt 4. Use when adding authentication, user management, roles, password reset, database setup (SQLite/MySQL/PostgreSQL), or CLI commands (migrate, create-user). Covers nuxt.config (nuxtUsers), composables (useAuthentication, useUsers, usePublicPaths, usePasswordValidation, useNuxtUsersLocale), components (NUsersLoginForm, NUsersLogoutLink, etc.), and authorization (whitelist, permissions).
license: MIT
metadata:
  author: rrd108
  version: "1.0"
---

# Nuxt Users skill

This skill helps you work with the **nuxt-users** module: user authentication, authorization, database setup, and CLI for Nuxt 3 and Nuxt 4 apps.

## When to use this skill

- User asks to add login, register, or logout to a Nuxt app
- User needs to set up or change the database (SQLite, MySQL, PostgreSQL) for nuxt-users
- User wants to run CLI commands: `npx nuxt-users migrate`, `npx nuxt-users create-user`
- User needs to configure permissions, roles, or public routes (whitelist)
- User is customizing password validation, session duration, or mailer (password reset)
- User is using composables like `useAuthentication`, `useUsers`, `usePublicPaths`, or `usePasswordValidation`
- User is styling or integrating components like `NUsersLoginForm`, `NUsersLogoutLink`, `NUsersProfileInfo`, `NUsersResetPasswordForm`, `NUsersList`, `NUsersUserForm`

## Step-by-step: initial setup

1. **Install the module and peer dependencies**
   ```bash
   npm install nuxt-users
   npm install db0 better-sqlite3 bcrypt nodemailer
   ```
   For MySQL or PostgreSQL, install the corresponding driver (`mysql2` or `pg`) instead of or in addition to `better-sqlite3` as required.

2. **Register the module in `nuxt.config.ts`**
   ```ts
   export default defineNuxtConfig({
     modules: ['nuxt-users']
   })
   ```

3. **Run migrations**
   From the project root (where `nuxt.config.ts` lives):
   ```bash
   npx nuxt-users migrate
   ```

4. **Create at least one user**
   ```bash
   npx nuxt-users create-user -e admin@example.com -n "Admin User" -p password123 -r admin
   ```
   Flags: `-e` email, `-n` name, `-p` password, `-r` role (optional).

5. **Configure permissions (required for protected routes)**
   Without `auth.permissions`, authenticated users cannot access protected routes. Prefer early configuration:
   ```ts
   export default defineNuxtConfig({
     modules: ['nuxt-users'],
     nuxtUsers: {
       auth: {
         permissions: {
           admin: ['*'],
           user: ['/profile', '/api/nuxt-users/me']
         }
       }
     }
   })
   ```

6. **Use login in a page**
   - Use the `NUsersLoginForm` component and handle `@success` by calling `login(user)` from `useAuthentication()`.
   - Optionally redirect after login (e.g. `navigateTo('/')`).

## Configuration reference (nuxt.config.ts)

All options live under `nuxtUsers` in `nuxt.config.ts`.

| Area | Key | Notes |
|------|-----|--------|
| Database | `connector.name` | `'sqlite' \| 'mysql' \| 'postgresql'` |
| Database | `connector.options` | `path` (SQLite), or `host`, `port`, `user`, `password`, `database` (MySQL/PostgreSQL) |
| API | `apiBasePath` | Default `'/api/nuxt-users'` |
| Tables | `tables.users`, `tables.personalAccessTokens`, `tables.passwordResetTokens`, `tables.migrations` | Custom table names |
| Mailer | `mailer` | Nodemailer config for password reset emails |
| URLs | `passwordResetUrl`, `emailConfirmationUrl` | Paths for redirects |
| Auth | `auth.whitelist` | Public routes (e.g. `['/register']`); `/login` is always public |
| Auth | `auth.tokenExpiration` | Minutes (default 1440) |
| Auth | `auth.rememberMeExpiration` | Days (default 30) |
| Auth | `auth.permissions` | Role → paths (e.g. `admin: ['*']`, `user: ['/profile']`) |
| Auth | `auth.google` | Google OAuth: `clientId`, `clientSecret`, `callbackUrl`, etc. |
| Password | `passwordValidation` | `minLength`, `requireUppercase`, `requireLowercase`, `requireNumbers`, `requireSpecialChars`, `preventCommonPasswords` |
| Data | `hardDelete` | `true` = hard delete, `false` = soft delete (default) |
| Locale | `locale.default`, `locale.texts`, `locale.fallbackLocale` | Localization |

Runtime config is also supported: use `runtimeConfig.nuxtUsers` for env-based or server-only settings; the CLI (e.g. `npx nuxt-users migrate`) reads from the same config when run from the project root.

## CLI commands

Run from the project root so `nuxt.config.ts` (and optionally `.env`) are found.

- **Migrations**
  ```bash
  npx nuxt-users migrate
  ```

- **Create user**
  ```bash
  npx nuxt-users create-user -e <email> -n "<name>" -p <password> [-r <role>]
  ```

- **Legacy/table creation** (if needed for older setups)
  ```bash
  npx nuxt-users create-users-table
  npx nuxt-users create-personal-access-tokens-table
  npx nuxt-users create-password-reset-tokens-table
  npx nuxt-users create-migrations-table
  ```

## Composables (auto-imported)

- **useAuthentication()** — `user`, `isAuthenticated`, `login(user, rememberMe?)`, `logout()`, `fetchUser(useSSR?)`, `initializeUser()`
- **useUsers()** — Admin: `users`, `pagination`, `loading`, `error`, `fetchUsers(page?, limit?)`, `updateUser`, `addUser`, `removeUser(userId)`
- **usePublicPaths()** — `getPublicPaths()`, `getAccessiblePaths()`, `isPublicPath(path)`, `isAccessiblePath(path, method?)`
- **usePasswordValidation(moduleOptions?, options?)** — `validate(password)`, `isValid`, `errors`, `strength`, `score`, `clearValidation()`
- **useNuxtUsersLocale()** — `t(key, params?)`, `currentLocale`, `fallbackLocale`

## Components

- `NUsersLoginForm` — Login form; use `@success` to call `login(user)` from `useAuthentication()`
- `NUsersLogoutLink` — Logout link/button
- `NUsersProfileInfo` — Display profile
- `NUsersResetPasswordForm` — Password reset form
- `NUsersList` — List users (admin)
- `NUsersUserForm` — Create/edit user form

## Common edge cases

1. **Users get redirected to login on protected routes**  
   Configure `nuxtUsers.auth.permissions` so each role has access to the routes they need (e.g. `admin: ['*']`, `user: ['/profile']`).

2. **CLI says config not found**  
   Run CLI from the directory that contains `nuxt.config.ts`. For runtime-only options, ensure env vars or `runtimeConfig.nuxtUsers` are set as documented.

3. **Migrations table missing**  
   Run `npx nuxt-users migrate` once from the project root. The module will warn at runtime if the migrations table is missing.

4. **Password validation too strict**  
   Adjust `nuxtUsers.passwordValidation` (e.g. lower `minLength`, set `requireUppercase`/`requireNumbers`/`requireSpecialChars` to `false`). Do not disable all checks in production without good reason.

5. **Database driver errors**  
   Install the correct peer: SQLite → `better-sqlite3`, MySQL → `mysql2`, PostgreSQL → `pg`. Ensure `connector.name` and `connector.options` match the driver and environment (e.g. correct host, port, credentials).

6. **Google OAuth**  
   Set `nuxtUsers.auth.google` with `clientId`, `clientSecret`, and optionally `callbackUrl`, `successRedirect`, `errorRedirect`, `scopes`, `allowAutoRegistration`.

## File references

- Project LLM context and config types: [llms.txt](../../llms.txt) in the repo root
- Full docs: [https://nuxt-users.webmania.cc/](https://nuxt-users.webmania.cc/)
- Getting started and examples: `../../docs/user-guide/getting-started.md`, `../../docs/examples/basic-setup.md`
- Authorization: `../../docs/user-guide/authorization.md`
- Configuration details: `../../docs/user-guide/configuration.md`

Keep `nuxtUsers` config and permissions in sync with the app’s roles and routes; use guard clauses and early returns when implementing custom auth logic.
