---
name: migrate-i18next-to-lingui
description: Migrate i18next/react-i18next projects to Lingui. Use when the user wants to replace i18next, react-i18next, useTranslation, i18n.t(), Trans i18nKey, or i18next JSON catalogs with Lingui equivalents. Covers package installation, config setup, code transformation patterns, plural migration, namespace handling, and catalog conversion.
---

# Migrate i18next to Lingui

## Migration Checklist

```
- [ ] Step 1: Install Lingui packages
- [ ] Step 2: Create lingui.config.js
- [ ] Step 3: Set up build tooling (Babel/SWC/Vite)
- [ ] Step 4: Replace i18n initialization
- [ ] Step 5: Migrate React components (useTranslation → useLingui, Trans → Trans)
- [ ] Step 6: Migrate JS/TS strings (t() → t``)
- [ ] Step 7: Migrate plurals
- [ ] Step 8: Migrate namespaces
- [ ] Step 9: Convert existing translation catalogs
- [ ] Step 10: Run lingui extract && lingui compile
- [ ] Step 11: Remove i18next packages
```

## Step 1: Install Lingui

> **Node version gate**: Lingui 6 is ESM-only and requires Node.js ≥ 22.19 (or ≥ 24). On older Node, pin all `@lingui/*` packages to `^5`.

```bash
# Core (always required)
npm install @lingui/core @lingui/react

# CLI (dev)
npm install --save-dev @lingui/cli

# Macro support - pick one based on build tool:
# Babel
npm install --save-dev @lingui/babel-plugin-lingui-macro
# SWC
npm install --save-dev @lingui/swc-plugin
# Vite (also install the Babel macro plugin above — see Step 3)
npm install --save-dev @lingui/vite-plugin
```

## Step 2: Create `lingui.config.js`

```js
import { defineConfig } from "@lingui/cli";

export default defineConfig({
  sourceLocale: "en",
  locales: ["en", "de", "fr"], // match your existing locales
  catalogs: [
    {
      path: "<rootDir>/src/locales/{locale}/messages",
      include: ["src"],
    },
  ],
});
```

## Step 3: Configure Build Tooling

**Vite** (`vite.config.ts`):
```ts
import { lingui } from "@lingui/vite-plugin";
import react from "@vitejs/plugin-react";

export default {
  plugins: [
    react({ babel: { plugins: ["@lingui/babel-plugin-lingui-macro"] } }),
    lingui(),
  ],
};
```

`lingui()` alone does not transform macros — the Babel macro plugin inside `react()` does that (requires `@vitejs/plugin-react@^5`; v6 removed the `babel` option — use the SWC variant instead).

The `lingui()` plugin also compiles `.po` catalogs on the fly, so on Vite the app can import catalogs directly and skip the `lingui compile` step entirely:

```ts
// Dynamic import; the .po extension is mandatory
const { messages } = await import(`./locales/${locale}/messages.po`);
```

For TypeScript, declare the module so `.po` imports type-check:

```ts
// src/vite-env.d.ts
declare module "*.po" {
  import type { Messages } from "@lingui/core";
  export const messages: Messages;
}
```

**Babel** (`.babelrc` or `babel.config.js`):
```json
{ "plugins": ["macros"] }
```

**Next.js with SWC** (`next.config.js`):
```js
module.exports = {
  experimental: {
    swcPlugins: [["@lingui/swc-plugin", {}]],
  },
};
```

**Build-tooling caveats**: `@lingui/swc-plugin` must be version-matched to your SWC runtime, plugin entries must be `[name, options]` tuples (a bare string silently disables macros), and `@vitejs/plugin-react@6` removed Babel support entirely — see the `swc-plugin-compatibility` skill for all three.

## Step 4: Replace i18n Initialization

**Before (i18next):**
```js
import i18next from "i18next";
import { initReactI18next } from "react-i18next";

i18next.use(initReactI18next).init({
  lng: "en",
  resources: { en: { translation: { key: "Hello world" } } },
});
```

**After (Lingui):**
```js
import { i18n } from "@lingui/core";
import { I18nProvider } from "@lingui/react";
import { messages } from "./locales/en/messages";

i18n.load("en", messages);
i18n.activate("en");

function App() {
  return <I18nProvider i18n={i18n}>{/* app */}</I18nProvider>;
}
```

**Dynamic locale switching:**
```js
async function changeLocale(locale) {
  const { messages } = await import(`./locales/${locale}/messages`);
  i18n.load(locale, messages);
  i18n.activate(locale);
}
```

## Step 5: Migrate React Components

### `useTranslation` → `useLingui`

**Before:**
```jsx
import { useTranslation } from "react-i18next";

function MyComponent() {
  const { t } = useTranslation();
  return <p>{t("greeting")}</p>;
}
```

**After:**
```jsx
import { useLingui } from "@lingui/react/macro";

function MyComponent() {
  const { t } = useLingui();
  return <p>{t`Hello World`}</p>;
}
```

### `Trans` component

**Before:**
```jsx
import { Trans } from "react-i18next";

<Trans i18nKey="welcome">Hello World!</Trans>
```

**After:**
```jsx
import { Trans } from "@lingui/react/macro";

<Trans>Hello World!</Trans>
```

For explicit IDs (when preserving i18next keys):
```jsx
<Trans id="welcome">Hello World!</Trans>
```

### `Trans` with interpolation

**Before:**
```jsx
<Trans i18nKey="greeting" values={{ name }}>Hello {{ name }}!</Trans>
```

**After:**
```jsx
<Trans>Hello {name}!</Trans>
```

## Step 6: Migrate JS/TS Strings

### Simple strings

| i18next | Lingui |
|---------|--------|
| `t('key')` | `t\`Message text\`` |
| `t('key', { name })` | `t\`Hello ${name}\`` |
| `t('key', { defaultValue: 'Hi' })` | `t\`Hi\`` |

**Before:**
```js
import i18next from "i18next";

const msg = i18next.t("greeting", { name: "Tom" });
```

**After:**
```jsx
import { useLingui } from "@lingui/react/macro";

function MyComponent() {
  const { t } = useLingui();
  const msg = t`Hello ${name}`;
}
```

**In vanilla JS (outside components):**
```js
import { t } from "@lingui/core/macro";

const msg = t`Hello ${name}`;
```

### Preserving explicit keys from i18next

If you want to keep the i18next message IDs:
```js
import { t } from "@lingui/core/macro";

// i18next: t('navigation.home')
const msg = t({ id: "navigation.home", message: "Home" });
```

### Module-level / lazy strings

**Before (i18next):**
```js
const LABELS = {
  active: "Active",
  inactive: "Inactive",
};
// translated at render time
```

**After (Lingui):**
```js
import { msg } from "@lingui/core/macro";
import { useLingui } from "@lingui/react";

const LABELS = {
  active: msg`Active`,
  inactive: msg`Inactive`,
};

function StatusDisplay({ status }) {
  const { _ } = useLingui();
  return <div>{_(LABELS[status])}</div>;
}
```

## Step 7: Migrate Plurals

i18next uses separate keys per plural form. Lingui uses ICU MessageFormat in a single message.

**Before (i18next):**
```json
{
  "item_one": "{{count}} item",
  "item_other": "{{count}} items"
}
```
```js
t("item", { count });
```

**After (Lingui) - JSX:**
```jsx
import { Plural } from "@lingui/react/macro";

<Plural value={count} one="# item" other="# items" />
```

**After (Lingui) - JS strings:**
```js
import { plural } from "@lingui/core/macro";

const msg = plural(count, {
  one: "# item",
  other: "# items",
});
```

**Exact matches** (i18next `_0`):
```jsx
<Plural
  value={count}
  _0="No items"
  one="# item"
  other="# items"
/>
```

## Step 8: Migrate Namespaces

i18next namespaces (`useTranslation('common')`) map to Lingui **catalog paths**. Two approaches:

**Option A - Single catalog (simplest):**
Remove namespaces and use one unified catalog. Update `lingui.config.js` to include all source directories.

**Option B - Multiple catalogs (preserves namespace separation):**
```js
// lingui.config.js
catalogs: [
  {
    path: "<rootDir>/src/locales/{locale}/common",
    include: ["src/components/common"],
  },
  {
    path: "<rootDir>/src/locales/{locale}/auth",
    include: ["src/components/auth"],
  },
]
```

With multiple catalogs, load them all at startup:
```js
import { messages as commonMessages } from "./locales/en/common";
import { messages as authMessages } from "./locales/en/auth";

i18n.load("en", { ...commonMessages, ...authMessages });
i18n.activate("en");
```

## Step 9: Convert Existing Translation Catalogs

See [catalog-conversion.md](references/catalog-conversion.md) for and patterns.

**Key concept:** i18next uses JSON with dotted keys; Lingui uses `.po` files with the message as the ID (or an explicit ID you provide).

## Step 10: Build & Verify

Run the full verification loop in this order — each stage catches what the previous one can't:

```bash
npx lingui extract --clean   # extracts all messages → .po files, drops obsolete entries
npx lingui compile           # compiles .po → runtime message catalogs
npx tsc --noEmit             # type errors from changed imports/APIs
npm run build                # macro transform actually runs in the real build
```

On Vite with `@lingui/vite-plugin` importing `.po` catalogs directly (Step 3), skip `lingui compile` — the plugin compiles at dev/build time and there are no compiled catalog files to manage.

Add to `package.json`:
```json
{
  "scripts": {
    "i18n:extract": "lingui extract",
    "i18n:compile": "lingui compile"
  }
}
```

For TypeScript:
```bash
npx lingui compile --typescript
```

### Recall Check: Find Strings the Migration Missed

A green build only proves the migrated strings work — not that all strings were migrated. Two checks:

**1. No i18next remnants.** All of these should return nothing:

```bash
grep -rn "from ['\"]i18next\|from ['\"]react-i18next" src/
grep -rn "useTranslation\|i18nKey\|i18next.t(" src/
```

**2. No unwrapped user-facing strings.** Run `eslint-plugin-lingui`'s `no-unlocalized-strings` rule over the tree — it catches hardcoded strings that were never in i18next to begin with, plus any `defaultValue` text left behind as plain strings:

```js
// eslint.config.js
import pluginLingui from "eslint-plugin-lingui";

export default [
  {
    plugins: { lingui: pluginLingui },
    rules: {
      "lingui/no-unlocalized-strings": ["warn", {
        ignore: ["^[A-Z0-9_-]+$"],                    // enums, constants
        ignoreNames: ["className", "src", "data-testid"],
        ignoreFunctions: ["console.*", "cn", "cva"],
      }],
    },
  },
];
```

The scan is deliberately over-inclusive — review each hit and either wrap it or confirm it's a non-UI string (class names, keys, URLs). Keep the plugin installed afterwards as a permanent guardrail. Report any strings you deliberately leave unwrapped rather than silently skipping them.

For the full audit loop — tuned scanner config, bounded fix rounds, residual reporting — use the **find-unwrapped-strings** skill. The check above is its migration-scoped subset.

## Step 11: Remove i18next

```bash
npm uninstall i18next react-i18next
```

## Common Patterns Reference

### Date/Number Formatting

**Before (i18next):**
```js
t("intlDateTime", { val: new Date() });
```

**After (Lingui):**
```jsx
import { useLingui } from "@lingui/react/macro";

function Component() {
  const { i18n } = useLingui();
  return <span>{new Intl.DateTimeFormat(i18n.locale).format(date)}</span>;
}
```

### Context (disambiguation)

**Before (i18next):**
```js
t("right", { context: "direction" });
```

**After (Lingui):**
```jsx
<Trans context="direction">right</Trans>
// or
t({ message: "right", context: "direction" });
```

### Gender / Select

**Before (i18next):**
```json
{ "pronoun_male": "He", "pronoun_female": "She", "pronoun_other": "They" }
```

**After (Lingui):**
```js
import { select } from "@lingui/core/macro";

const pronoun = select(gender, {
  male: "He",
  female: "She",
  other: "They",
});
```

## Pitfalls

- **Don't call `t\`...\`` at module level.** Use `msg\`...\`` instead and translate with `_(descriptor)` at render time.
- **After locale change**, call both `i18n.load(locale, messages)` and `i18n.activate(locale)`.
- **Wrap the entire app** in `<I18nProvider i18n={i18n}>` before any component uses `useLingui` or `Trans`.
- **Always run `lingui compile`** before building for production; the app imports compiled `.js` catalogs, not `.po` files.
- **Generated IDs change if message text changes.** If stability matters, use explicit `id` props.

## Additional Resources

- [Detailed migration patterns](references/migration-patterns.md)
- [Catalog conversion guide](references/catalog-conversion.md)
- [Lingui docs](https://lingui.dev)
- [Lingui vs i18next comparison](https://lingui.dev/misc/i18next)
