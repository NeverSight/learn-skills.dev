---
name: react-i18next
description: "How to implement internationalization (i18n) in React applications using react-i18next and i18next. Use this skill whenever the user wants to add multi-language support to a React app, translate UI content, set up i18next configuration, use the useTranslation hook, withTranslation HOC, Trans component, handle namespaces, plurals, interpolation, or any localization-related task in React. Also trigger when the user mentions 'i18n', 'i18next', 'react-i18next', 'localization', 'translation', 'multi-language', 'internationalization', 'locale', 'language switcher', or wants to translate strings/JSX in React components — even if they don't explicitly name the library. Trigger for Next.js/Remix/Gatsby i18n questions too, as react-i18next is the underlying solution."
---

# react-i18next Skill

react-i18next is the standard internationalization framework for React / React Native, built on top of i18next. This skill covers setup, configuration, all API surfaces, and common patterns.

> **Key mental model**: i18next is the core translation engine (config, plurals, interpolation, formatting). react-i18next is the React binding layer that connects i18next to your components via hooks, HOCs, render props, and the Trans component.

## Installation

```bash
npm install react-i18next i18next --save

# Common companion packages:
npm install i18next-http-backend i18next-browser-languagedetector --save
```

## i18next Configuration (i18n.js)

Create `i18n.js` beside your entry point. This is the single source of truth for your i18n setup.

### Minimal setup (inline resources)

```js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: {
          "welcome": "Welcome to our app"
        }
      },
      tr: {
        translation: {
          "welcome": "Uygulamamıza hoş geldiniz"
        }
      }
    },
    lng: 'en',              // default language
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false     // React already escapes by default
    }
  });

export default i18n;
```

### Production setup (with backend + language detection)

```js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(Backend)              // loads translations from /public/locales/{lng}/{ns}.json
  .use(LanguageDetector)     // detects user language
  .use(initReactI18next)     // binds i18next to React
  .init({
    fallbackLng: 'en',
    debug: true,             // set false in production
    interpolation: {
      escapeValue: false
    },
    // react-specific options (all optional):
    // react: {
    //   bindI18n: 'languageChanged',
    //   bindI18nStore: '',
    //   transEmptyNodeValue: '',
    //   transSupportBasicHtmlNodes: true,
    //   transKeepBasicHtmlNodesFor: ['br', 'strong', 'i', 'p'],
    //   useSuspense: true,
    // }
  });

export default i18n;
```

Then import in your entry point:

```js
import './i18n';  // must be imported before App
```

### Translation file structure

When using `i18next-http-backend`, place files at:
```
public/
  locales/
    en/
      translation.json    ← default namespace
      common.json          ← additional namespace
    tr/
      translation.json
      common.json
```

## Core APIs

react-i18next provides four ways to access translations. Choose based on your use case:

| Method | Use when |
|--------|----------|
| `useTranslation` hook | Functional components (recommended) |
| `withTranslation` HOC | Class components or wrapping any component |
| `Translation` render prop | Need t function in any component type |
| `Trans` component | Translating JSX trees with embedded HTML/components |

### 1. useTranslation Hook (primary API)

```jsx
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t, i18n } = useTranslation();
  return <h1>{t('welcome')}</h1>;
}
```

**Namespace loading:**
```jsx
const { t } = useTranslation('common');           // single namespace
const { t } = useTranslation(['ns1', 'ns2']);      // multiple (first = default)
t('key');                                          // looks up in default ns
t('key', { ns: 'ns2' });                          // explicit namespace
```

**keyPrefix** (react-i18next >= 11.12.0, i18next >= 20.6.0):
```jsx
// For deeply nested keys: { "very": { "deeply": { "nested": { "key": "value" }}}}
const { t } = useTranslation('translation', { keyPrefix: 'very.deeply.nested' });
t('key');  // → "value"
```

**Fixed language** (react-i18next >= 12.3.1):
```jsx
const { t } = useTranslation('translation', { lng: 'de' });
```

**Without Suspense:**
```jsx
const { t, i18n, ready } = useTranslation('ns1', { useSuspense: false });
if (!ready) return <Loading />;  // must handle loading state yourself
```

**Suspense behavior**: By default, useTranslation triggers React Suspense while translations load. Wrap your app (or relevant subtree) in `<Suspense fallback="loading">`.

### 2. withTranslation HOC

```jsx
import { withTranslation } from 'react-i18next';

function MyComponent({ t, i18n }) {
  return <p>{t('greeting')}</p>;
}
export default withTranslation()(MyComponent);           // default ns
export default withTranslation('common')(MyComponent);    // specific ns
export default withTranslation(['ns1', 'ns2'])(MyComponent); // multiple
```

Without Suspense: pass `useSuspense={false}` as a prop, then check `props.tReady`.

### 3. Translation Render Prop

```jsx
import { Translation } from 'react-i18next';

function MyComponent() {
  return (
    <Translation ns="common">
      {(t, { i18n }) => <p>{t('hello')}</p>}
    </Translation>
  );
}
```

### 4. Trans Component

Use Trans **only** when you need to embed React elements (links, bold text, components) within a translated string. For plain text, use `t()` instead.

```jsx
import { Trans, useTranslation } from 'react-i18next';

function Welcome({ name, count }) {
  const { t } = useTranslation();
  return (
    <Trans i18nKey="userMessages" count={count}>
      Hello <strong title={t('nameTitle')}>{{name}}</strong>,
      you have {{count}} unread message.
      <Link to="/msgs">Go to messages</Link>.
    </Trans>
  );
}
```

Translation JSON:
```json
{
  "userMessages_one": "Hello <1>{{name}}</1>, you have {{count}} unread message. <5>Go to messages</5>.",
  "userMessages_other": "Hello <1>{{name}}</1>, you have {{count}} unread messages. <5>Go to messages</5>."
}
```

**Named components (v11.6.0+)** — cleaner than indexed tags:
```jsx
<Trans
  i18nKey="myKey"
  defaults="hello <italic>beautiful</italic> <bold>{{what}}</bold>"
  values={{ what: 'world' }}
  components={{ italic: <i />, bold: <strong /> }}
/>
```
JSON: `"myKey": "hello <italic>beautiful</italic> <bold>{{what}}</bold>"`

**Simple HTML elements** (v10.4.0+):
By default, `<br/>`, `<strong>`, `<i>`, `<p>` are kept as-is in translation strings (controlled by `transSupportBasicHtmlNodes` and `transKeepBasicHtmlNodesFor` options).

**Index numbering rules**: Children of Trans are numbered by their position in the children array. Strings and interpolation objects get indices but aren't wrapped in tags. Elements get `<N>...</N>` tags.

For a full reference of Trans component props and advanced patterns, read `references/trans-component.md`.

## Common Patterns

### Language Switching

```jsx
function LanguageSwitcher() {
  const { i18n } = useTranslation();
  return (
    <select value={i18n.language} onChange={e => i18n.changeLanguage(e.target.value)}>
      <option value="en">English</option>
      <option value="tr">Türkçe</option>
    </select>
  );
}
```

### Using t() Outside Components

Import the configured i18n instance directly:
```js
import i18n from './i18n';
i18n.t('my.key');
```

### I18nextProvider (Multiple Instances)

Only needed if you support multiple i18next instances (e.g., component libraries) or SSR:
```jsx
import { I18nextProvider } from 'react-i18next';
import i18n from './i18n';

<I18nextProvider i18n={i18n} defaultNS="translation">
  <App />
</I18nextProvider>
```

### Namespaces (Multiple Translation Files)

Namespaces let you split translations into separate files and lazy-load them:
```jsx
const { t } = useTranslation(['page1', 'common']);
t('key');                      // from 'page1' (first namespace)
t('key', { ns: 'common' });   // from 'common'
```

Components using `useTranslation`, `withTranslation`, or `Translation` will automatically Suspense until their requested namespaces are loaded — no need to load all translations upfront.

### Interpolation

```json
{ "greeting": "Hello {{name}}, you are {{age}} years old" }
```
```jsx
t('greeting', { name: 'Ali', age: 28 })
```

### Plurals

i18next uses ICU-like plural suffixes. For English:
```json
{
  "item_one": "{{count}} item",
  "item_other": "{{count}} items"
}
```
```jsx
t('item', { count: 5 })  // → "5 items"
```

### Context

```json
{
  "friend_male": "A boyfriend",
  "friend_female": "A girlfriend"
}
```
```jsx
t('friend', { context: 'male' })
```

### Nesting

```json
{
  "app": { "name": "MyApp" },
  "intro": "Welcome to $t(app.name)"
}
```

## TypeScript Support

Requires react-i18next >= 13.0.0 and i18next >= 23.0.1.

Follow the official guide at https://www.i18next.com/overview/typescript for setting up type-safe translations. The key steps are:

1. Create a resources type definition file
2. Augment the `i18next` module with your resource types
3. The `t` function then uses accessor syntax: `t($ => $.my.key)`

## SSR (Next.js, Remix, Gatsby)

- **Next.js (App Router)**: Use i18next directly with the App Router pattern — see references/ssr.md
- **Next.js (Pages Router)**: Use `next-i18next` which wraps react-i18next
- **Remix**: Use `remix-i18next`
- **Gatsby**: Use `gatsby-plugin-react-i18next`

For custom SSR, use `useSSR` hook or `withSSR` HOC to pass initial translations and language from server to client:
```jsx
import { useSSR } from 'react-i18next';
function InitSSR({ initialI18nStore, initialLanguage }) {
  useSSR(initialI18nStore, initialLanguage);
  return <App />;
}
```

For more details, read `references/ssr.md`.

## Testing

Three approaches, from simplest to most thorough:

**1. Mock the hook (Jest):**
```js
jest.mock('react-i18next', () => ({
  useTranslation: () => ({
    t: (key) => key,
    i18n: { changeLanguage: () => new Promise(() => {}) },
  }),
  initReactI18next: { type: '3rdParty', init: () => {} },
}));
```

**2. Export bare component + pass t as prop:**
```js
export { MyComponent };                              // for testing
export default withTranslation('ns')(MyComponent);   // for app
// In test: <MyComponent t={key => key} />
```

**3. Full i18next setup in tests** (no mocking):
```js
import i18n from 'i18next';
import { initReactI18next, I18nextProvider } from 'react-i18next';
i18n.use(initReactI18next).init({
  lng: 'en', fallbackLng: 'en',
  resources: { en: { translationsNS: {} } },
});
// Wrap component: <I18nextProvider i18n={i18n}><MyComponent /></I18nextProvider>
```

For a detailed testing guide with spy examples, read `references/testing.md`.

## React Options Reference

Options under `i18next.init({ react: { ... } })`:

| Option | Default | Description |
|--------|---------|-------------|
| `bindI18n` | `'languageChanged'` | Events triggering rerender |
| `bindI18nStore` | `''` | Store events triggering rerender |
| `transEmptyNodeValue` | `''` | Value for failed lookups in Trans |
| `transSupportBasicHtmlNodes` | `true` | Keep `<br/>` etc. in translation strings |
| `transKeepBasicHtmlNodesFor` | `['br','strong','i','p']` | Which HTML tags to keep |
| `transWrapTextNodes` | `''` | Wrap text nodes (e.g. `'span'` for Google Translate fix) |
| `useSuspense` | `true` | Enable/disable Suspense |
| `keyPrefix` | `undefined` | Auto-prefix for useTranslation's t function |

## Reference Files

For detailed documentation on specific topics, read these files in the `references/` directory:

- `references/trans-component.md` — Full Trans component API, props, index numbering, named components, overriding props, lists, ICU format usage
- `references/testing.md` — Detailed testing patterns with Jest mocks, spies, and full i18next setup
- `references/ssr.md` — SSR patterns for Next.js, Remix, Gatsby, and custom SSR with useSSR/withSSR
