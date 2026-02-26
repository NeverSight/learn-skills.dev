---
name: frontend-internationalization-best-practices
description: Internationalization best practices for React Router framework mode using remix-i18next. Use when setting up locales, middleware, resource routes, or language switching.
---

# Internationalization Best Practices

Guidelines for building a React Router i18n setup with `remix-i18next`. Focuses on middleware detection, locale storage, type safety, and client/server synchronization.

## When to Apply

- Adding i18n to a React Router app
- Wiring `remix-i18next` middleware
- Implementing language switching or locale detection
- Serving locale resources from `/api/locales`

## Rules Summary

### Setup & Middleware (CRITICAL)

#### setup-middleware - @rules/setup-middleware.md

Configure `createI18nextMiddleware` and type-safe resources.

```ts
export const [i18nextMiddleware, getLocale, getInstance] =
  createI18nextMiddleware({
    detection: {
      supportedLanguages: ["es", "en"],
      fallbackLanguage: "en",
      cookie: localeCookie,
    },
    i18next: { resources },
    plugins: [initReactI18next],
  });
```

#### locales-structure - @rules/locales-structure.md

Define locale resources per language and re-export.

```ts
// app/locales/en/translation.ts
export default { title: "Example" };
```

### Namespaces (HIGH)

#### namespaces-strategy - @rules/namespaces-strategy.md

Use a single namespace for small apps; multiple namespaces for large apps.

```ts
// Large app: common + route namespaces
export default { common, home, notFound };
```

### Locale Detection & Persistence (CRITICAL)

#### locale-detection - @rules/locale-detection.md

Prefer cookie/session for speed, with DB as source of truth.

```ts
export const [i18nextMiddleware, getLocale] = createI18nextMiddleware({
  detection: { cookie: localeCookie, fallbackLanguage: "en" },
});
```

#### language-switcher - @rules/language-switcher.md

Store locale in cookie/session and keep it in sync.

```ts
return data(
  { locale },
  { headers: { "Set-Cookie": await localeCookie.serialize(locale) } },
);
```

### Client & Server Integration (CRITICAL)

#### root-locale-sync - @rules/root-locale-sync.md

Send locale to the UI and sync `<html lang dir>`.

```tsx
export async function loader({ context }: Route.LoaderArgs) {
  let locale = getLocale(context);
  return data(
    { locale },
    { headers: { "Set-Cookie": await localeCookie.serialize(locale) } },
  );
}
```

#### entry-client-init - @rules/entry-client-init.md

Initialize i18next client with `htmlTag` detection.

```ts
i18next.init({ detection: { order: ["htmlTag"], caches: [] } });
```

#### entry-server-provider - @rules/entry-server-provider.md

Reuse the middleware instance in SSR with `I18nextProvider`.

```tsx
<I18nextProvider i18n={getInstance(routerContext)}>
  <ServerRouter context={entryContext} url={request.url} />
</I18nextProvider>
```

### Resource Routes & Caching (HIGH)

#### locales-resource-route - @rules/locales-resource-route.md

Serve `/api/locales/:lng/:ns` with validation and cache headers.

```ts
return data(namespaces[ns.data], { headers });
```

### UI Usage (MEDIUM)

#### use-bound-t-in-loader - @rules/use-bound-t-in-loader.md

Use the bound `t()` in loaders and `useTranslation` in components.

```ts
let t = getInstance(context).getFixedT(locale);
```

### Not Found (MEDIUM)

#### not-found-i18n - @rules/not-found-i18n.md

Provide a 404 route so middleware runs and translations load.
