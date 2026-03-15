---
name: ionic-skills
description: Ionic Capacitor mobile app development with Angular, React, or Vue. RevenueCat payments, AdMob ads, i18n localization, onboarding flow, paywall, and Ionic Tabs navigation.
---

# Ionic Capacitor Application Development Guide

> **IMPORTANT**: This is a SKILL file, NOT a project. NEVER run npm install in this folder. NEVER create code files here. When creating a new project, ALWAYS ask the user for the project path first or create it in a separate directory (e.g., `~/Projects/app-name`).

This guide covers building production-ready mobile apps with **Ionic Capacitor** using **Angular**, **React**, or **Vue**.

---

## MANDATORY REQUIREMENTS

When creating a new Ionic project, you MUST include ALL of the following:

### Required Pages (ALWAYS CREATE)

- [ ] Onboarding page - Swipe-based onboarding with fullscreen background video and gradient overlay
- [ ] Paywall page - RevenueCat paywall page (shown after onboarding)
- [ ] Settings page - Settings page with language, theme, notifications, and reset onboarding options

### Required Navigation (ALWAYS USE)

- [ ] Use `ion-tabs` with `ion-tab-bar` for tab navigation - NEVER use custom tab implementations or third-party tab libraries

### Required Libraries (ALWAYS INSTALL)

#### Angular

```bash
npm install @capacitor/preferences @capacitor/push-notifications @capacitor/splash-screen @capacitor/status-bar @revenuecat/purchases-capacitor @capacitor-community/admob @ngx-translate/core @ngx-translate/http-loader swiper
```

#### React

```bash
npm install @capacitor/preferences @capacitor/push-notifications @capacitor/splash-screen @capacitor/status-bar @revenuecat/purchases-capacitor @capacitor-community/admob react-i18next i18next i18next-http-backend swiper
```

#### Vue

```bash
npm install @capacitor/preferences @capacitor/push-notifications @capacitor/splash-screen @capacitor/status-bar @revenuecat/purchases-capacitor @capacitor-community/admob vue-i18n swiper
```

### Shared Libraries (All Frameworks)

- `@revenuecat/purchases-capacitor` (RevenueCat)
- `@capacitor-community/admob` (AdMob)
- `@capacitor/push-notifications` (Push Notifications)
- `@capacitor/preferences` (Key-value storage)
- `@capacitor/splash-screen` (Splash screen control)
- `@capacitor/status-bar` (Status bar styling)
- `swiper` (Onboarding slides)

### Framework-Specific i18n Libraries

| Framework | Library | Usage |
|-----------|---------|-------|
| Angular | `@ngx-translate/core` + `@ngx-translate/http-loader` | `translate` pipe |
| React | `react-i18next` + `i18next` | `useTranslation()` hook |
| Vue | `vue-i18n` | `useI18n()` composable / `$t()` |

---

## FORBIDDEN (NEVER USE)

### All Frameworks

- ❌ `localStorage` directly - Use `@capacitor/preferences` instead
- ❌ `@ionic/storage` - Use `@capacitor/preferences` instead
- ❌ Custom tab bars - Use `ion-tabs` + `ion-tab-bar` instead
- ❌ `cordova-plugin-*` plugins - Use Capacitor plugins instead
- ❌ `any` type - Always use proper TypeScript types
- ❌ `ngx-admob-free` or other deprecated ad libraries - ONLY use `@capacitor-community/admob`
- ❌ Synchronous Capacitor calls - Always `await` Capacitor plugin methods

### Angular-Specific

- ❌ NgModules for new pages/components - Use standalone components
- ❌ `IonicModule` in standalone components - Import individual components (`IonButton`, `IonContent`, etc.)
- ❌ Inline `template` or `styles` in `@Component` - Use separate `.html`, `.ts`, `.scss` files with `templateUrl` and `styleUrls`
- ❌ `@angular/http` (deprecated) - Use `@angular/common/http`

### React-Specific

- ❌ Class components - Use functional components with hooks
- ❌ Direct DOM manipulation - Use React refs and state
- ❌ `@ionic/angular` imports - Use `@ionic/react`

### Vue-Specific

- ❌ Options API for new code - Use Composition API with `<script setup>`
- ❌ Direct DOM manipulation - Use Vue refs and reactivity
- ❌ `@ionic/angular` imports - Use `@ionic/vue`

---

## Technology Stack

| Concern | Angular | React | Vue |
|---------|---------|-------|-----|
| Framework | Ionic 8 + Angular 19 | Ionic 8 + React 19 | Ionic 8 + Vue 3.5 |
| Native Runtime | Capacitor 7 | Capacitor 7 | Capacitor 7 |
| Navigation | Angular Router (lazy-loaded) | @ionic/react-router | @ionic/vue-router |
| Tab Navigation | ion-tabs + ion-tab-bar | ion-tabs + ion-tab-bar | ion-tabs + ion-tab-bar |
| State Management | Angular Services (Signals/RxJS) | Custom Hooks / Context | Composables / Pinia |
| Translations | @ngx-translate/core | react-i18next | vue-i18n |
| Purchases | @revenuecat/purchases-capacitor | @revenuecat/purchases-capacitor | @revenuecat/purchases-capacitor |
| Ads | @capacitor-community/admob | @capacitor-community/admob | @capacitor-community/admob |
| Notifications | @capacitor/push-notifications | @capacitor/push-notifications | @capacitor/push-notifications |
| Storage | @capacitor/preferences | @capacitor/preferences | @capacitor/preferences |

> **WARNING**: DO NOT USE `localStorage` directly! Use `@capacitor/preferences` instead for cross-platform persistent storage.

---

## Project Creation

When user asks to create an app, you MUST:

1. FIRST ask for the bundle ID (e.g., "What is the bundle ID? Example: com.company.appname")
2. Create the project in the CURRENT directory
3. Then implement all required pages

### Creating a Project (Angular)

```bash
npm install -g @ionic/cli
ionic start app-name blank --type=angular --capacitor
```

### Creating a Project (React)

```bash
npm install -g @ionic/cli
ionic start app-name blank --type=react --capacitor
```

### Creating a Project (Vue)

```bash
npm install -g @ionic/cli
ionic start app-name blank --type=vue --capacitor
```

### Capacitor Configuration (All Frameworks)

```typescript
// capacitor.config.ts
import type { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.company.appname',
  appName: 'App Name',
  webDir: 'www',
  server: {
    androidScheme: 'https',
  },
};

export default config;
```

> **Note**: For React/Vue projects, `webDir` may be `'dist'` instead of `'www'`. Check your project's build output directory.

### Add Native Platforms

```bash
npx cap add ios
npx cap add android
```

---

## Project Structure

### Angular Project Structure

```
project-root/
├── src/
│   ├── app/
│   │   ├── app.component.ts
│   │   ├── app.component.html
│   │   ├── app.config.ts
│   │   ├── app.routes.ts
│   │   ├── tabs/
│   │   │   ├── tabs.page.ts
│   │   │   ├── tabs.page.html
│   │   │   ├── tabs.page.scss
│   │   │   └── tabs.routes.ts
│   │   ├── home/
│   │   │   ├── home.page.ts
│   │   │   ├── home.page.html
│   │   │   └── home.page.scss
│   │   ├── explore/
│   │   │   ├── explore.page.ts
│   │   │   ├── explore.page.html
│   │   │   └── explore.page.scss
│   │   ├── settings/
│   │   │   ├── settings.page.ts
│   │   │   ├── settings.page.html
│   │   │   └── settings.page.scss
│   │   ├── paywall/
│   │   │   ├── paywall.page.ts
│   │   │   ├── paywall.page.html
│   │   │   └── paywall.page.scss
│   │   ├── onboarding/
│   │   │   ├── onboarding.page.ts
│   │   │   ├── onboarding.page.html
│   │   │   └── onboarding.page.scss
│   │   ├── services/
│   │   │   ├── theme.service.ts
│   │   │   ├── onboarding.service.ts
│   │   │   ├── ads.service.ts
│   │   │   ├── purchases.service.ts
│   │   │   └── notifications.service.ts
│   │   ├── guards/
│   │   │   └── onboarding.guard.ts
│   │   └── utils/
│   │       ├── admob.ts
│   │       ├── purchases.ts
│   │       ├── onboarding.ts
│   │       ├── theme.ts
│   │       └── notifications.ts
│   ├── assets/
│   │   └── i18n/
│   │       ├── en.json
│   │       └── tr.json
│   ├── theme/
│   │   └── variables.scss
│   ├── global.scss
│   ├── index.html
│   └── main.ts
├── ios/
├── android/
├── capacitor.config.ts
├── angular.json
├── package.json
└── tsconfig.json
```

### React Project Structure

```
project-root/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   ├── pages/
│   │   ├── OnboardingPage.tsx
│   │   ├── PaywallPage.tsx
│   │   ├── SettingsPage.tsx
│   │   ├── HomePage.tsx
│   │   └── ExplorePage.tsx
│   ├── components/
│   │   ├── TabsLayout.tsx
│   │   └── OnboardingGuard.tsx
│   ├── hooks/
│   │   ├── useTheme.ts
│   │   ├── useOnboarding.ts
│   │   ├── useAds.ts
│   │   ├── usePurchases.ts
│   │   └── useNotifications.ts
│   ├── utils/
│   │   ├── admob.ts
│   │   ├── purchases.ts
│   │   ├── onboarding.ts
│   │   ├── theme.ts
│   │   └── notifications.ts
│   ├── theme/
│   │   └── variables.css
│   └── i18n/
│       ├── index.ts
│       ├── en.json
│       └── tr.json
├── public/
├── ios/
├── android/
├── capacitor.config.ts
├── package.json
└── tsconfig.json
```

### Vue Project Structure

```
project-root/
├── src/
│   ├── App.vue
│   ├── main.ts
│   ├── router/
│   │   └── index.ts
│   ├── views/
│   │   ├── OnboardingPage.vue
│   │   ├── PaywallPage.vue
│   │   ├── SettingsPage.vue
│   │   ├── HomePage.vue
│   │   ├── ExplorePage.vue
│   │   └── TabsLayout.vue
│   ├── composables/
│   │   ├── useTheme.ts
│   │   ├── useOnboarding.ts
│   │   ├── useAds.ts
│   │   ├── usePurchases.ts
│   │   └── useNotifications.ts
│   ├── utils/
│   │   ├── admob.ts
│   │   ├── purchases.ts
│   │   ├── onboarding.ts
│   │   ├── theme.ts
│   │   └── notifications.ts
│   ├── theme/
│   │   └── variables.css
│   └── assets/
│       └── i18n/
│           ├── en.json
│           └── tr.json
├── ios/
├── android/
├── capacitor.config.ts
├── package.json
└── tsconfig.json
```

---

## App Configuration

### App Configuration (Angular)

```typescript
// app.config.ts
import { ApplicationConfig } from '@angular/core';
import { provideRouter, RouteReuseStrategy } from '@angular/router';
import { provideIonicAngular, IonicRouteStrategy } from '@ionic/angular/standalone';
import { provideHttpClient } from '@angular/common/http';
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { HttpClient } from '@angular/common/http';
import { importProvidersFrom } from '@angular/core';
import { routes } from './app.routes';

export function createTranslateLoader(http: HttpClient) {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideIonicAngular({ mode: 'md' }),
    provideHttpClient(),
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    importProvidersFrom(
      TranslateModule.forRoot({
        defaultLanguage: 'en',
        loader: {
          provide: TranslateLoader,
          useFactory: createTranslateLoader,
          deps: [HttpClient],
        },
      })
    ),
  ],
};
```

```html
<!-- app.component.html -->
<ion-app>
  <ion-router-outlet></ion-router-outlet>
</ion-app>
```

```typescript
// app.component.ts
import { Component, OnInit } from '@angular/core';
import { IonApp, IonRouterOutlet } from '@ionic/angular/standalone';
import { AdsService } from './services/ads.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [IonApp, IonRouterOutlet],
  templateUrl: './app.component.html',
})
export class AppComponent implements OnInit {
  constructor(private adsService: AdsService) {}

  async ngOnInit() {
    await this.adsService.initialize();
  }
}
```

### App Configuration (React)

```tsx
// main.tsx
import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';

/* Core CSS required for Ionic components */
import '@ionic/react/css/core.css';
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';

import './theme/variables.css';
import './i18n';

const root = createRoot(document.getElementById('root')!);
root.render(<App />);
```

```tsx
// App.tsx
import { useEffect } from 'react';
import { IonApp, IonRouterOutlet, setupIonicReact } from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { Route, Redirect } from 'react-router-dom';
import OnboardingPage from './pages/OnboardingPage';
import PaywallPage from './pages/PaywallPage';
import TabsLayout from './components/TabsLayout';
import { OnboardingGuard } from './components/OnboardingGuard';
import { initializeAdMob } from './utils/admob';

setupIonicReact({ mode: 'md' });

const App: React.FC = () => {
  useEffect(() => {
    initializeAdMob();
  }, []);

  return (
    <IonApp>
      <IonReactRouter>
        <IonRouterOutlet>
          <Route exact path="/onboarding" component={OnboardingPage} />
          <Route exact path="/paywall" component={PaywallPage} />
          <Route path="/tabs">
            <OnboardingGuard>
              <TabsLayout />
            </OnboardingGuard>
          </Route>
          <Route exact path="/">
            <Redirect to="/tabs" />
          </Route>
        </IonRouterOutlet>
      </IonReactRouter>
    </IonApp>
  );
};

export default App;
```

```typescript
// i18n/index.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './en.json';
import tr from './tr.json';

const browserLang = navigator.language.split('-')[0];

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    tr: { translation: tr },
  },
  lng: ['en', 'tr'].includes(browserLang) ? browserLang : 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
});

export default i18n;
```

### App Configuration (Vue)

```typescript
// main.ts
import { createApp } from 'vue';
import { IonicVue } from '@ionic/vue';
import App from './App.vue';
import router from './router';
import { createI18n } from 'vue-i18n';
import en from './assets/i18n/en.json';
import tr from './assets/i18n/tr.json';

/* Core CSS required for Ionic components */
import '@ionic/vue/css/core.css';
import '@ionic/vue/css/normalize.css';
import '@ionic/vue/css/structure.css';
import '@ionic/vue/css/typography.css';
import '@ionic/vue/css/padding.css';
import '@ionic/vue/css/float-elements.css';
import '@ionic/vue/css/text-alignment.css';
import '@ionic/vue/css/text-transformation.css';
import '@ionic/vue/css/flex-utils.css';
import '@ionic/vue/css/display.css';

import './theme/variables.css';

const browserLang = navigator.language.split('-')[0];

const i18n = createI18n({
  legacy: false,
  locale: ['en', 'tr'].includes(browserLang) ? browserLang : 'en',
  fallbackLocale: 'en',
  messages: { en, tr },
});

const app = createApp(App);
app.use(IonicVue, { mode: 'md' });
app.use(router);
app.use(i18n);
router.isReady().then(() => app.mount('#app'));
```

```vue
<!-- App.vue -->
<template>
  <ion-app>
    <ion-router-outlet />
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { onMounted } from 'vue';
import { initializeAdMob } from './utils/admob';

onMounted(async () => {
  await initializeAdMob();
});
</script>
```

---

## Routing

### Routing (Angular)

```typescript
// app.routes.ts
import { Routes } from '@angular/router';
import { onboardingGuard } from './guards/onboarding.guard';

export const routes: Routes = [
  {
    path: 'onboarding',
    loadComponent: () => import('./onboarding/onboarding.page').then(m => m.OnboardingPage),
  },
  {
    path: 'paywall',
    loadComponent: () => import('./paywall/paywall.page').then(m => m.PaywallPage),
  },
  {
    path: 'tabs',
    loadChildren: () => import('./tabs/tabs.routes').then(m => m.tabsRoutes),
    canActivate: [onboardingGuard],
  },
  {
    path: '',
    redirectTo: 'tabs',
    pathMatch: 'full',
  },
];
```

```typescript
// tabs/tabs.routes.ts
import { Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

export const tabsRoutes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      {
        path: 'home',
        loadComponent: () => import('../home/home.page').then(m => m.HomePage),
      },
      {
        path: 'explore',
        loadComponent: () => import('../explore/explore.page').then(m => m.ExplorePage),
      },
      {
        path: 'settings',
        loadComponent: () => import('../settings/settings.page').then(m => m.SettingsPage),
      },
      {
        path: '',
        redirectTo: 'home',
        pathMatch: 'full',
      },
    ],
  },
];
```

### Routing (React)

Routes are defined in `App.tsx` (see App Configuration above). Tab routes are defined in the `TabsLayout` component:

```tsx
// components/TabsLayout.tsx
import { IonTabs, IonRouterOutlet, IonTabBar, IonTabButton, IonIcon, IonLabel } from '@ionic/react';
import { Route, Redirect } from 'react-router-dom';
import { home, compass, settings } from 'ionicons/icons';
import { useTranslation } from 'react-i18next';
import { useEffect } from 'react';
import HomePage from '../pages/HomePage';
import ExplorePage from '../pages/ExplorePage';
import SettingsPage from '../pages/SettingsPage';
import { showBannerAd, hideBannerAd } from '../utils/admob';
import { isPremiumUser } from '../utils/purchases';

const TabsLayout: React.FC = () => {
  const { t } = useTranslation();

  useEffect(() => {
    isPremiumUser().then((premium) => {
      if (!premium) showBannerAd();
    });
    return () => { hideBannerAd(); };
  }, []);

  return (
    <IonTabs>
      <IonRouterOutlet>
        <Route exact path="/tabs/home" component={HomePage} />
        <Route exact path="/tabs/explore" component={ExplorePage} />
        <Route exact path="/tabs/settings" component={SettingsPage} />
        <Route exact path="/tabs">
          <Redirect to="/tabs/home" />
        </Route>
      </IonRouterOutlet>
      <IonTabBar slot="bottom">
        <IonTabButton tab="home" href="/tabs/home">
          <IonIcon icon={home} />
          <IonLabel>{t('tabs.home')}</IonLabel>
        </IonTabButton>
        <IonTabButton tab="explore" href="/tabs/explore">
          <IonIcon icon={compass} />
          <IonLabel>{t('tabs.explore')}</IonLabel>
        </IonTabButton>
        <IonTabButton tab="settings" href="/tabs/settings">
          <IonIcon icon={settings} />
          <IonLabel>{t('tabs.settings')}</IonLabel>
        </IonTabButton>
      </IonTabBar>
    </IonTabs>
  );
};

export default TabsLayout;
```

### Routing (Vue)

```typescript
// router/index.ts
import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import { isOnboardingCompleted } from '../utils/onboarding';
import TabsLayout from '../views/TabsLayout.vue';

const routes: RouteRecordRaw[] = [
  {
    path: '/onboarding',
    component: () => import('../views/OnboardingPage.vue'),
  },
  {
    path: '/paywall',
    component: () => import('../views/PaywallPage.vue'),
  },
  {
    path: '/tabs/',
    component: TabsLayout,
    children: [
      {
        path: '',
        redirect: '/tabs/home',
      },
      {
        path: 'home',
        component: () => import('../views/HomePage.vue'),
      },
      {
        path: 'explore',
        component: () => import('../views/ExplorePage.vue'),
      },
      {
        path: 'settings',
        component: () => import('../views/SettingsPage.vue'),
      },
    ],
  },
  {
    path: '/',
    redirect: '/tabs/',
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, _from, next) => {
  if (to.path.startsWith('/tabs') || to.path === '/') {
    const completed = await isOnboardingCompleted();
    if (!completed) {
      return next('/onboarding');
    }
  }
  next();
});

export default router;
```

```vue
<!-- views/TabsLayout.vue -->
<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet />
      <ion-tab-bar slot="bottom">
        <ion-tab-button tab="home" href="/tabs/home">
          <ion-icon :icon="home" />
          <ion-label>{{ t('tabs.home') }}</ion-label>
        </ion-tab-button>
        <ion-tab-button tab="explore" href="/tabs/explore">
          <ion-icon :icon="compass" />
          <ion-label>{{ t('tabs.explore') }}</ion-label>
        </ion-tab-button>
        <ion-tab-button tab="settings" href="/tabs/settings">
          <ion-icon :icon="settings" />
          <ion-label>{{ t('tabs.settings') }}</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script setup lang="ts">
import {
  IonPage, IonTabs, IonRouterOutlet, IonTabBar, IonTabButton, IonIcon, IonLabel,
} from '@ionic/vue';
import { home, compass, settings } from 'ionicons/icons';
import { useI18n } from 'vue-i18n';
import { onMounted, onUnmounted } from 'vue';
import { showBannerAd, hideBannerAd } from '../utils/admob';
import { isPremiumUser } from '../utils/purchases';

const { t } = useI18n();

onMounted(async () => {
  const premium = await isPremiumUser();
  if (!premium) await showBannerAd();
});

onUnmounted(async () => {
  await hideBannerAd();
});
</script>
```

---

## Shared Utility Functions (Framework-Agnostic)

These utility files contain pure TypeScript with Capacitor plugin calls. They are used by all frameworks. Each framework wraps them in its own pattern (Angular services, React hooks, Vue composables).

### Storage (All Frameworks)

```typescript
import { Preferences } from '@capacitor/preferences';

// Set a value
await Preferences.set({ key: 'onboardingCompleted', value: 'true' });

// Get a value
const { value } = await Preferences.get({ key: 'onboardingCompleted' });
console.log(value); // 'true'

// Remove a value
await Preferences.remove({ key: 'onboardingCompleted' });
```

### Onboarding State Utility

```typescript
// utils/onboarding.ts
import { Preferences } from '@capacitor/preferences';

const KEY = 'onboardingCompleted';

export async function isOnboardingCompleted(): Promise<boolean> {
  const { value } = await Preferences.get({ key: KEY });
  return value === 'true';
}

export async function setOnboardingCompleted(completed: boolean): Promise<void> {
  await Preferences.set({ key: KEY, value: String(completed) });
}

export async function resetOnboarding(): Promise<void> {
  await Preferences.remove({ key: KEY });
}
```

### Theme Utility

```typescript
// utils/theme.ts
import { Preferences } from '@capacitor/preferences';

export type ThemeMode = 'light' | 'dark' | 'system';

const KEY = 'themeMode';

export async function getTheme(): Promise<ThemeMode> {
  const { value } = await Preferences.get({ key: KEY });
  return (value as ThemeMode) || 'system';
}

export async function setTheme(mode: ThemeMode): Promise<void> {
  await Preferences.set({ key: KEY, value: mode });
  applyTheme(mode);
}

export function applyTheme(mode: ThemeMode): void {
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isDark = mode === 'dark' || (mode === 'system' && prefersDark);
  document.documentElement.classList.toggle('ion-palette-dark', isDark);
}
```

### AdMob Utility

```typescript
// utils/admob.ts
import { AdMob, BannerAdOptions, BannerAdSize, BannerAdPosition } from '@capacitor-community/admob';
import { Capacitor } from '@capacitor/core';

let initialized = false;

export async function initializeAdMob(): Promise<void> {
  if (!Capacitor.isNativePlatform()) return;

  await AdMob.initialize({
    initializeForTesting: true, // Set to false in production
  });
  initialized = true;
}

export async function showBannerAd(): Promise<void> {
  if (!initialized) return;

  const options: BannerAdOptions = {
    adId: 'ca-app-pub-3940256099942544/6300978111', // Test ID - replace in production
    adSize: BannerAdSize.ADAPTIVE_BANNER,
    position: BannerAdPosition.BOTTOM_CENTER,
    isTesting: true, // Set to false in production
  };

  await AdMob.showBanner(options);
}

export async function hideBannerAd(): Promise<void> {
  if (!initialized) return;
  await AdMob.hideBanner();
}
```

For development/testing, use test Ad IDs:

- Banner: `ca-app-pub-3940256099942544/6300978111`

Do NOT skip AdMob initialization or the plugin will not work correctly.

### RevenueCat Utility

```typescript
// utils/purchases.ts
import { Capacitor } from '@capacitor/core';
import { Purchases, LOG_LEVEL, PURCHASES_ERROR_CODE, PurchasesPackage } from '@revenuecat/purchases-capacitor';

let purchasesInitialized = false;

export async function initializePurchases(): Promise<void> {
  if (!Capacitor.isNativePlatform()) return;

  await Purchases.setLogLevel({ level: LOG_LEVEL.DEBUG }); // Use WARN in production

  const apiKey = Capacitor.getPlatform() === 'ios'
    ? 'appl_YOUR_IOS_API_KEY'
    : 'goog_YOUR_ANDROID_API_KEY';

  await Purchases.configure({ apiKey });
  purchasesInitialized = true;
}

export async function isPremiumUser(): Promise<boolean> {
  if (!purchasesInitialized) return false;
  try {
    const { customerInfo } = await Purchases.getCustomerInfo();
    return Object.keys(customerInfo.entitlements.active).length > 0;
  } catch {
    return false;
  }
}

export async function getOfferings(): Promise<PurchasesPackage[]> {
  if (!purchasesInitialized) return [];
  try {
    const { offerings } = await Purchases.getOfferings();
    return offerings?.current?.availablePackages ?? [];
  } catch {
    return [];
  }
}

export async function purchasePackage(pkg: PurchasesPackage): Promise<boolean> {
  try {
    const { customerInfo } = await Purchases.purchasePackage({ aPackage: pkg });
    return Object.keys(customerInfo.entitlements.active).length > 0;
  } catch (error: unknown) {
    if ((error as { code?: string })?.code === PURCHASES_ERROR_CODE.PURCHASE_CANCELLED_ERROR) {
      return false;
    }
    throw error;
  }
}

export async function restorePurchases(): Promise<boolean> {
  try {
    const { customerInfo } = await Purchases.restorePurchases();
    return Object.keys(customerInfo.entitlements.active).length > 0;
  } catch {
    return false;
  }
}
```

### Notifications Utility

```typescript
// utils/notifications.ts
import { Capacitor } from '@capacitor/core';
import { PushNotifications } from '@capacitor/push-notifications';

export async function requestNotificationPermission(): Promise<boolean> {
  if (!Capacitor.isNativePlatform()) return false;

  const result = await PushNotifications.requestPermissions();
  if (result.receive === 'granted') {
    await PushNotifications.register();
    return true;
  }
  return false;
}

export async function addNotificationListeners(): Promise<void> {
  await PushNotifications.addListener('registration', (token) => {
    console.log('Push registration success, token:', token.value);
  });

  await PushNotifications.addListener('registrationError', (error) => {
    console.error('Push registration error:', error);
  });

  await PushNotifications.addListener('pushNotificationReceived', (notification) => {
    console.log('Push notification received:', notification);
  });

  await PushNotifications.addListener('pushNotificationActionPerformed', (action) => {
    console.log('Push notification action:', action);
  });
}
```

---

## Framework-Specific Service Wrappers

### Angular Services

```typescript
// services/onboarding.service.ts
import { Injectable } from '@angular/core';
import { isOnboardingCompleted, setOnboardingCompleted, resetOnboarding } from '../utils/onboarding';

@Injectable({ providedIn: 'root' })
export class OnboardingService {
  isCompleted = isOnboardingCompleted;
  setCompleted = setOnboardingCompleted;
  reset = resetOnboarding;
}
```

```typescript
// services/theme.service.ts
import { Injectable } from '@angular/core';
import { getTheme, setTheme, applyTheme, ThemeMode } from '../utils/theme';

@Injectable({ providedIn: 'root' })
export class ThemeService {
  async initialize(): Promise<void> {
    const theme = await getTheme();
    applyTheme(theme);
  }

  getTheme = getTheme;
  setTheme = setTheme;
}
```

```typescript
// services/ads.service.ts
import { Injectable } from '@angular/core';
import { initializeAdMob, showBannerAd, hideBannerAd } from '../utils/admob';
import { isPremiumUser } from '../utils/purchases';

@Injectable({ providedIn: 'root' })
export class AdsService {
  async initialize(): Promise<void> {
    await initializeAdMob();
  }

  async showBanner(): Promise<void> {
    if (await isPremiumUser()) return;
    await showBannerAd();
  }

  async hideBanner(): Promise<void> {
    await hideBannerAd();
  }
}
```

```typescript
// services/purchases.service.ts
import { Injectable } from '@angular/core';
import {
  initializePurchases,
  isPremiumUser,
  getOfferings,
  purchasePackage,
  restorePurchases,
} from '../utils/purchases';

@Injectable({ providedIn: 'root' })
export class PurchasesService {
  initialize = initializePurchases;
  isPremium = isPremiumUser;
  getOfferings = getOfferings;
  purchase = purchasePackage;
  restorePurchases = restorePurchases;
}
```

```typescript
// services/notifications.service.ts
import { Injectable } from '@angular/core';
import { requestNotificationPermission, addNotificationListeners } from '../utils/notifications';

@Injectable({ providedIn: 'root' })
export class NotificationsService {
  requestPermission = requestNotificationPermission;
  addListeners = addNotificationListeners;
}
```

### React Hooks

```typescript
// hooks/useOnboarding.ts
import { useCallback } from 'react';
import { isOnboardingCompleted, setOnboardingCompleted, resetOnboarding } from '../utils/onboarding';

export function useOnboarding() {
  const isCompleted = useCallback(() => isOnboardingCompleted(), []);
  const setCompleted = useCallback((v: boolean) => setOnboardingCompleted(v), []);
  const reset = useCallback(() => resetOnboarding(), []);
  return { isCompleted, setCompleted, reset };
}
```

```typescript
// hooks/useTheme.ts
import { useCallback } from 'react';
import { getTheme, setTheme, applyTheme, ThemeMode } from '../utils/theme';

export function useTheme() {
  const initialize = useCallback(async () => {
    const theme = await getTheme();
    applyTheme(theme);
  }, []);

  return {
    initialize,
    getTheme: useCallback(() => getTheme(), []),
    setTheme: useCallback((mode: ThemeMode) => setTheme(mode), []),
  };
}
```

```typescript
// hooks/useAds.ts
import { useCallback } from 'react';
import { initializeAdMob, showBannerAd, hideBannerAd } from '../utils/admob';
import { isPremiumUser } from '../utils/purchases';

export function useAds() {
  const initialize = useCallback(() => initializeAdMob(), []);
  const showBanner = useCallback(async () => {
    if (await isPremiumUser()) return;
    await showBannerAd();
  }, []);
  const hideBanner = useCallback(() => hideBannerAd(), []);
  return { initialize, showBanner, hideBanner };
}
```

```typescript
// hooks/usePurchases.ts
import { useCallback } from 'react';
import {
  initializePurchases,
  isPremiumUser,
  getOfferings,
  purchasePackage,
  restorePurchases,
} from '../utils/purchases';
import { PurchasesPackage } from '@revenuecat/purchases-capacitor';

export function usePurchases() {
  return {
    initialize: useCallback(() => initializePurchases(), []),
    isPremium: useCallback(() => isPremiumUser(), []),
    getOfferings: useCallback(() => getOfferings(), []),
    purchase: useCallback((pkg: PurchasesPackage) => purchasePackage(pkg), []),
    restorePurchases: useCallback(() => restorePurchases(), []),
  };
}
```

```typescript
// hooks/useNotifications.ts
import { useCallback } from 'react';
import { requestNotificationPermission, addNotificationListeners } from '../utils/notifications';

export function useNotifications() {
  return {
    requestPermission: useCallback(() => requestNotificationPermission(), []),
    addListeners: useCallback(() => addNotificationListeners(), []),
  };
}
```

### Vue Composables

```typescript
// composables/useOnboarding.ts
import { isOnboardingCompleted, setOnboardingCompleted, resetOnboarding } from '../utils/onboarding';

export function useOnboarding() {
  return {
    isCompleted: isOnboardingCompleted,
    setCompleted: setOnboardingCompleted,
    reset: resetOnboarding,
  };
}
```

```typescript
// composables/useTheme.ts
import { getTheme, setTheme, applyTheme, ThemeMode } from '../utils/theme';

export function useTheme() {
  const initialize = async () => {
    const theme = await getTheme();
    applyTheme(theme);
  };

  return { initialize, getTheme, setTheme };
}
```

```typescript
// composables/useAds.ts
import { initializeAdMob, showBannerAd, hideBannerAd } from '../utils/admob';
import { isPremiumUser } from '../utils/purchases';

export function useAds() {
  const initialize = () => initializeAdMob();
  const showBanner = async () => {
    if (await isPremiumUser()) return;
    await showBannerAd();
  };
  const hideBanner = () => hideBannerAd();
  return { initialize, showBanner, hideBanner };
}
```

```typescript
// composables/usePurchases.ts
import {
  initializePurchases,
  isPremiumUser,
  getOfferings,
  purchasePackage,
  restorePurchases,
} from '../utils/purchases';

export function usePurchases() {
  return {
    initialize: initializePurchases,
    isPremium: isPremiumUser,
    getOfferings,
    purchase: purchasePackage,
    restorePurchases,
  };
}
```

```typescript
// composables/useNotifications.ts
import { requestNotificationPermission, addNotificationListeners } from '../utils/notifications';

export function useNotifications() {
  return {
    requestPermission: requestNotificationPermission,
    addListeners: addNotificationListeners,
  };
}
```

---

## Onboarding Guard

### Onboarding Guard (Angular)

```typescript
// guards/onboarding.guard.ts
import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { isOnboardingCompleted } from '../utils/onboarding';

export const onboardingGuard: CanActivateFn = async () => {
  const router = inject(Router);

  const completed = await isOnboardingCompleted();

  if (!completed) {
    router.navigateByUrl('/onboarding', { replaceUrl: true });
    return false;
  }

  return true;
};
```

### Onboarding Guard (React)

```tsx
// components/OnboardingGuard.tsx
import { useEffect, useState } from 'react';
import { useIonRouter } from '@ionic/react';
import { isOnboardingCompleted } from '../utils/onboarding';

export const OnboardingGuard: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const router = useIonRouter();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    isOnboardingCompleted().then((completed) => {
      if (!completed) {
        router.push('/onboarding', 'forward', 'replace');
      } else {
        setChecked(true);
      }
    });
  }, []);

  return checked ? <>{children}</> : null;
};
```

### Onboarding Guard (Vue)

The Vue onboarding guard is implemented as a `router.beforeEach` hook. See the Routing (Vue) section above.

---

## Onboarding Page

### Shared Video CSS (All Frameworks)

```css
.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}
.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.7));
  z-index: 1;
}
.onboarding-slides {
  position: relative;
  z-index: 2;
  height: 100%;
}
```

Do NOT just reference the video without actually rendering the `<video>` element. Use native HTML5 `<video>` - NOT canvas, NOT animated GIFs, NOT external players.

### Onboarding Page (Angular)

```html
<!-- onboarding/onboarding.page.html -->
<ion-content [fullscreen]="true" class="onboarding-content">
  <video
    #bgVideo
    [src]="videoUrl"
    autoplay
    loop
    muted
    playsinline
    class="background-video"
  ></video>
  <div class="gradient-overlay"></div>
  <div class="onboarding-slides">
    <!-- Swiper slides content here -->
  </div>
</ion-content>
```

```scss
// onboarding/onboarding.page.scss
.background-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.7));
  z-index: 1;
}

.onboarding-slides {
  position: relative;
  z-index: 2;
  height: 100%;
}
```

```typescript
// onboarding/onboarding.page.ts
import { Component } from '@angular/core';
import { IonContent, IonButton, IonIcon } from '@ionic/angular/standalone';
import { Router } from '@angular/router';
import { OnboardingService } from '../services/onboarding.service';

const VIDEO_URL =
  'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';

@Component({
  selector: 'app-onboarding',
  standalone: true,
  imports: [IonContent, IonButton, IonIcon],
  templateUrl: './onboarding.page.html',
  styleUrls: ['./onboarding.page.scss'],
})
export class OnboardingPage {
  videoUrl = VIDEO_URL;

  constructor(
    private router: Router,
    private onboardingService: OnboardingService
  ) {}

  async completeOnboarding() {
    await this.onboardingService.setCompleted(true);
    this.router.navigateByUrl('/paywall', { replaceUrl: true });
  }
}
```

### Onboarding Page (React)

```tsx
// pages/OnboardingPage.tsx
import { IonContent, IonButton, IonIcon, useIonRouter } from '@ionic/react';
import { useOnboarding } from '../hooks/useOnboarding';
import './OnboardingPage.css';

const VIDEO_URL =
  'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';

const OnboardingPage: React.FC = () => {
  const router = useIonRouter();
  const { setCompleted } = useOnboarding();

  const completeOnboarding = async () => {
    await setCompleted(true);
    router.push('/paywall', 'forward', 'replace');
  };

  return (
    <IonContent fullscreen className="onboarding-content">
      <video
        src={VIDEO_URL}
        autoPlay
        loop
        muted
        playsInline
        className="background-video"
      />
      <div className="gradient-overlay" />
      <div className="onboarding-slides">
        {/* Swiper slides content here */}
      </div>
    </IonContent>
  );
};

export default OnboardingPage;
```

### Onboarding Page (Vue)

```vue
<!-- views/OnboardingPage.vue -->
<template>
  <ion-content :fullscreen="true" class="onboarding-content">
    <video
      :src="videoUrl"
      autoplay
      loop
      muted
      playsinline
      class="background-video"
    />
    <div class="gradient-overlay" />
    <div class="onboarding-slides">
      <!-- Swiper slides content here -->
    </div>
  </ion-content>
</template>

<script setup lang="ts">
import { IonContent, IonButton, IonIcon } from '@ionic/vue';
import { useRouter } from 'vue-router';
import { useOnboarding } from '../composables/useOnboarding';

const VIDEO_URL =
  'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4';

const videoUrl = VIDEO_URL;
const router = useRouter();
const { setCompleted } = useOnboarding();

async function completeOnboarding() {
  await setCompleted(true);
  router.replace('/paywall');
}
</script>

<style scoped>
.background-video {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  z-index: 0;
}
.gradient-overlay {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.7));
  z-index: 1;
}
.onboarding-slides {
  position: relative;
  z-index: 2;
  height: 100%;
}
</style>
```

---

## Paywall Page

**IMPORTANT**: Paywall MUST appear immediately after onboarding completes.

Paywall MUST have two subscription options:

1. **Weekly** - Default option
2. **Yearly** - With "50% OFF" badge (recommended, should be highlighted)

Three buttons: Subscribe, Continue with ads, Restore Purchases.

Flow: `Onboarding -> Paywall -> Main App (tabs)`

### Paywall Page (Angular)

```html
<!-- paywall/paywall.page.html -->
<ion-content [fullscreen]="true">
  <div class="paywall-container">
    <h1>{{ 'paywall.title' | translate }}</h1>

    <div class="subscription-options">
      <div
        *ngFor="let option of subscriptionOptions"
        class="option-card"
        [class.selected]="selectedPlan === option.id"
        (click)="selectedPlan = option.id"
      >
        <ion-badge *ngIf="option.badge" color="danger">{{ option.badge }}</ion-badge>
        <h3>{{ option.title | translate }}</h3>
        <p>{{ option.price }}</p>
      </div>
    </div>

    <ion-button expand="block" (click)="subscribe()">
      {{ 'paywall.subscribe' | translate }}
    </ion-button>

    <ion-button fill="clear" (click)="skip()">
      {{ 'paywall.skip' | translate }}
    </ion-button>

    <ion-button fill="clear" size="small" (click)="restore()">
      {{ 'paywall.restore' | translate }}
    </ion-button>
  </div>
</ion-content>
```

```scss
// paywall/paywall.page.scss
.paywall-container {
  // Add your paywall styles here
}

.subscription-options {
  // Add your subscription options styles here
}

.option-card {
  // Add your option card styles here

  &.selected {
    // Selected state styles
  }
}
```

```typescript
// paywall/paywall.page.ts
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {
  IonContent, IonButton, IonIcon, IonBadge,
} from '@ionic/angular/standalone';
import { NgFor, NgIf, NgClass } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { PurchasesService } from '../services/purchases.service';

@Component({
  selector: 'app-paywall',
  standalone: true,
  imports: [
    IonContent, IonButton, IonIcon, IonBadge,
    NgFor, NgIf, NgClass, TranslateModule,
  ],
  templateUrl: './paywall.page.html',
  styleUrls: ['./paywall.page.scss'],
})
export class PaywallPage {
  selectedPlan = 'weekly';

  subscriptionOptions = [
    { id: 'weekly', title: 'paywall.weekly', price: '$4.99/week', badge: null },
    { id: 'yearly', title: 'paywall.yearly', price: '$129.99/year', badge: '50% OFF' },
  ];

  constructor(
    private router: Router,
    private purchasesService: PurchasesService,
  ) {}

  async subscribe() {
    // Use RevenueCat to process purchase
    this.router.navigateByUrl('/tabs', { replaceUrl: true });
  }

  skip() {
    this.router.navigateByUrl('/tabs', { replaceUrl: true });
  }

  async restore() {
    const restored = await this.purchasesService.restorePurchases();
    if (restored) {
      this.router.navigateByUrl('/tabs', { replaceUrl: true });
    }
  }
}
```

### Paywall Page (React)

```tsx
// pages/PaywallPage.tsx
import { useState } from 'react';
import {
  IonContent, IonButton, IonBadge, useIonRouter,
} from '@ionic/react';
import { useTranslation } from 'react-i18next';
import { usePurchases } from '../hooks/usePurchases';

const subscriptionOptions = [
  { id: 'weekly', title: 'paywall.weekly', price: '$4.99/week', badge: null },
  { id: 'yearly', title: 'paywall.yearly', price: '$129.99/year', badge: '50% OFF' },
];

const PaywallPage: React.FC = () => {
  const { t } = useTranslation();
  const router = useIonRouter();
  const { restorePurchases } = usePurchases();
  const [selectedPlan, setSelectedPlan] = useState('weekly');

  const subscribe = async () => {
    // Use RevenueCat to process purchase
    router.push('/tabs', 'forward', 'replace');
  };

  const skip = () => {
    router.push('/tabs', 'forward', 'replace');
  };

  const restore = async () => {
    const restored = await restorePurchases();
    if (restored) {
      router.push('/tabs', 'forward', 'replace');
    }
  };

  return (
    <IonContent fullscreen>
      <div className="paywall-container">
        <h1>{t('paywall.title')}</h1>

        <div className="subscription-options">
          {subscriptionOptions.map((option) => (
            <div
              key={option.id}
              className={`option-card ${selectedPlan === option.id ? 'selected' : ''}`}
              onClick={() => setSelectedPlan(option.id)}
            >
              {option.badge && <IonBadge color="danger">{option.badge}</IonBadge>}
              <h3>{t(option.title)}</h3>
              <p>{option.price}</p>
            </div>
          ))}
        </div>

        <IonButton expand="block" onClick={subscribe}>
          {t('paywall.subscribe')}
        </IonButton>

        <IonButton fill="clear" onClick={skip}>
          {t('paywall.skip')}
        </IonButton>

        <IonButton fill="clear" size="small" onClick={restore}>
          {t('paywall.restore')}
        </IonButton>
      </div>
    </IonContent>
  );
};

export default PaywallPage;
```

### Paywall Page (Vue)

```vue
<!-- views/PaywallPage.vue -->
<template>
  <ion-content :fullscreen="true">
    <div class="paywall-container">
      <h1>{{ t('paywall.title') }}</h1>

      <div class="subscription-options">
        <div
          v-for="option in subscriptionOptions"
          :key="option.id"
          class="option-card"
          :class="{ selected: selectedPlan === option.id }"
          @click="selectedPlan = option.id"
        >
          <ion-badge v-if="option.badge" color="danger">{{ option.badge }}</ion-badge>
          <h3>{{ t(option.title) }}</h3>
          <p>{{ option.price }}</p>
        </div>
      </div>

      <ion-button expand="block" @click="subscribe">
        {{ t('paywall.subscribe') }}
      </ion-button>

      <ion-button fill="clear" @click="skip">
        {{ t('paywall.skip') }}
      </ion-button>

      <ion-button fill="clear" size="small" @click="restore">
        {{ t('paywall.restore') }}
      </ion-button>
    </div>
  </ion-content>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { IonContent, IonButton, IonBadge } from '@ionic/vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { usePurchases } from '../composables/usePurchases';

const { t } = useI18n();
const router = useRouter();
const { restorePurchases } = usePurchases();
const selectedPlan = ref('weekly');

const subscriptionOptions = [
  { id: 'weekly', title: 'paywall.weekly', price: '$4.99/week', badge: null },
  { id: 'yearly', title: 'paywall.yearly', price: '$129.99/year', badge: '50% OFF' },
];

async function subscribe() {
  // Use RevenueCat to process purchase
  router.replace('/tabs');
}

function skip() {
  router.replace('/tabs');
}

async function restore() {
  const restored = await restorePurchases();
  if (restored) {
    router.replace('/tabs');
  }
}
</script>
```

---

## Tab Navigation

### Common Ionicons

| Purpose       | Ionicon Name  |
|---------------|---------------|
| Home          | home          |
| Explore       | compass       |
| Settings      | settings      |
| Profile       | person        |
| Search        | search        |
| Favorites     | heart         |
| Notifications | notifications |

### Tab Navigation (Angular)

```html
<!-- tabs/tabs.page.html -->
<ion-tabs>
  <ion-tab-bar slot="bottom">
    <ion-tab-button tab="home">
      <ion-icon name="home"></ion-icon>
      <ion-label>{{ 'tabs.home' | translate }}</ion-label>
    </ion-tab-button>

    <ion-tab-button tab="explore">
      <ion-icon name="compass"></ion-icon>
      <ion-label>{{ 'tabs.explore' | translate }}</ion-label>
    </ion-tab-button>

    <ion-tab-button tab="settings">
      <ion-icon name="settings"></ion-icon>
      <ion-label>{{ 'tabs.settings' | translate }}</ion-label>
    </ion-tab-button>
  </ion-tab-bar>
</ion-tabs>
```

```typescript
// tabs/tabs.page.ts
import { Component, OnInit, OnDestroy } from '@angular/core';
import { IonTabs, IonTabBar, IonTabButton, IonIcon, IonLabel } from '@ionic/angular/standalone';
import { addIcons } from 'ionicons';
import { home, compass, settings } from 'ionicons/icons';
import { TranslateModule } from '@ngx-translate/core';
import { AdsService } from '../services/ads.service';

@Component({
  selector: 'app-tabs',
  standalone: true,
  imports: [IonTabs, IonTabBar, IonTabButton, IonIcon, IonLabel, TranslateModule],
  templateUrl: './tabs.page.html',
  styleUrls: ['./tabs.page.scss'],
})
export class TabsPage implements OnInit, OnDestroy {
  constructor(private adsService: AdsService) {
    addIcons({ home, compass, settings });
  }

  async ngOnInit() {
    await this.adsService.showBanner();
  }

  async ngOnDestroy() {
    await this.adsService.hideBanner();
  }
}
```

### Tab Navigation (React)

See the `TabsLayout` component in the Routing (React) section above.

### Tab Navigation (Vue)

See the `TabsLayout.vue` component in the Routing (Vue) section above.

---

## Settings Page

Settings page MUST include:

1. **Language** - Change app language
2. **Theme** - Light/Dark/System
3. **Notifications** - Enable/disable notifications
4. **Remove Ads** - Navigate to paywall (hidden if already premium)
5. **Reset Onboarding** - Restart onboarding flow (for testing/demo)

### Settings Page (Angular)

```html
<!-- settings/settings.page.html -->
<ion-header>
  <ion-toolbar>
    <ion-title>{{ 'settings.title' | translate }}</ion-title>
  </ion-toolbar>
</ion-header>
<ion-content>
  <ion-list>
    <ion-item>
      <ion-icon name="language" slot="start"></ion-icon>
      <ion-label>{{ 'settings.language' | translate }}</ion-label>
      <ion-select [value]="currentLang" (ionChange)="changeLanguage($event)">
        <ion-select-option value="en">English</ion-select-option>
        <ion-select-option value="tr">Türkçe</ion-select-option>
      </ion-select>
    </ion-item>

    <ion-item>
      <ion-icon name="color-palette" slot="start"></ion-icon>
      <ion-label>{{ 'settings.theme' | translate }}</ion-label>
      <ion-select [value]="currentTheme" (ionChange)="changeTheme($event)">
        <ion-select-option value="system">{{ 'settings.system' | translate }}</ion-select-option>
        <ion-select-option value="light">{{ 'settings.light' | translate }}</ion-select-option>
        <ion-select-option value="dark">{{ 'settings.dark' | translate }}</ion-select-option>
      </ion-select>
    </ion-item>

    <ion-item>
      <ion-icon name="notifications" slot="start"></ion-icon>
      <ion-label>{{ 'settings.notifications' | translate }}</ion-label>
      <ion-toggle [checked]="notificationsEnabled" (ionChange)="toggleNotifications($event)"></ion-toggle>
    </ion-item>

    <ion-item *ngIf="!isPremium" button (click)="removeAds()">
      <ion-icon name="star" slot="start"></ion-icon>
      <ion-label>{{ 'settings.removeAds' | translate }}</ion-label>
    </ion-item>

    <ion-item button (click)="resetOnboarding()">
      <ion-icon name="refresh" slot="start"></ion-icon>
      <ion-label>{{ 'settings.resetOnboarding' | translate }}</ion-label>
    </ion-item>
  </ion-list>
</ion-content>
```

```scss
// settings/settings.page.scss
// Add your settings page styles here
```

```typescript
// settings/settings.page.ts
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {
  IonContent, IonHeader, IonTitle, IonToolbar,
  IonList, IonItem, IonLabel, IonIcon, IonToggle, IonSelect, IonSelectOption,
} from '@ionic/angular/standalone';
import { NgIf } from '@angular/common';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { Preferences } from '@capacitor/preferences';
import { ThemeService } from '../services/theme.service';
import { OnboardingService } from '../services/onboarding.service';
import { PurchasesService } from '../services/purchases.service';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [
    IonContent, IonHeader, IonTitle, IonToolbar,
    IonList, IonItem, IonLabel, IonIcon, IonToggle, IonSelect, IonSelectOption,
    NgIf, TranslateModule,
  ],
  templateUrl: './settings.page.html',
  styleUrls: ['./settings.page.scss'],
})
export class SettingsPage implements OnInit {
  currentLang = 'en';
  currentTheme = 'system';
  notificationsEnabled = false;
  isPremium = false;

  constructor(
    private router: Router,
    private themeService: ThemeService,
    private onboardingService: OnboardingService,
    private purchasesService: PurchasesService,
    private translate: TranslateService,
  ) {}

  async ngOnInit() {
    this.currentLang = this.translate.currentLang || 'en';
    this.currentTheme = await this.themeService.getTheme();
    this.isPremium = await this.purchasesService.isPremium();
  }

  changeLanguage(event: CustomEvent) {
    const lang = event.detail.value;
    this.translate.use(lang);
    Preferences.set({ key: 'language', value: lang });
  }

  changeTheme(event: CustomEvent) {
    this.themeService.setTheme(event.detail.value);
  }

  toggleNotifications(event: CustomEvent) {
    this.notificationsEnabled = event.detail.checked;
  }

  removeAds() {
    this.router.navigateByUrl('/paywall');
  }

  async resetOnboarding() {
    await this.onboardingService.reset();
    this.router.navigateByUrl('/onboarding', { replaceUrl: true });
  }
}
```

### Settings Page (React)

```tsx
// pages/SettingsPage.tsx
import { useState, useEffect } from 'react';
import {
  IonContent, IonHeader, IonTitle, IonToolbar, IonPage,
  IonList, IonItem, IonLabel, IonIcon, IonToggle, IonSelect, IonSelectOption,
  useIonRouter,
} from '@ionic/react';
import { language, colorPalette, notifications, star, refresh } from 'ionicons/icons';
import { useTranslation } from 'react-i18next';
import { Preferences } from '@capacitor/preferences';
import { useTheme } from '../hooks/useTheme';
import { useOnboarding } from '../hooks/useOnboarding';
import { usePurchases } from '../hooks/usePurchases';
import { ThemeMode } from '../utils/theme';

const SettingsPage: React.FC = () => {
  const { t, i18n } = useTranslation();
  const router = useIonRouter();
  const { getTheme, setTheme } = useTheme();
  const { reset } = useOnboarding();
  const { isPremium } = usePurchases();

  const [currentLang, setCurrentLang] = useState('en');
  const [currentTheme, setCurrentTheme] = useState<ThemeMode>('system');
  const [notificationsEnabled, setNotificationsEnabled] = useState(false);
  const [premium, setPremium] = useState(false);

  useEffect(() => {
    setCurrentLang(i18n.language || 'en');
    getTheme().then(setCurrentTheme);
    isPremium().then(setPremium);
  }, []);

  const changeLanguage = (lang: string) => {
    setCurrentLang(lang);
    i18n.changeLanguage(lang);
    Preferences.set({ key: 'language', value: lang });
  };

  const changeTheme = (mode: ThemeMode) => {
    setCurrentTheme(mode);
    setTheme(mode);
  };

  const resetOnboarding = async () => {
    await reset();
    router.push('/onboarding', 'forward', 'replace');
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>{t('settings.title')}</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent>
        <IonList>
          <IonItem>
            <IonIcon icon={language} slot="start" />
            <IonLabel>{t('settings.language')}</IonLabel>
            <IonSelect value={currentLang} onIonChange={(e) => changeLanguage(e.detail.value)}>
              <IonSelectOption value="en">English</IonSelectOption>
              <IonSelectOption value="tr">Türkçe</IonSelectOption>
            </IonSelect>
          </IonItem>

          <IonItem>
            <IonIcon icon={colorPalette} slot="start" />
            <IonLabel>{t('settings.theme')}</IonLabel>
            <IonSelect value={currentTheme} onIonChange={(e) => changeTheme(e.detail.value)}>
              <IonSelectOption value="system">{t('settings.system')}</IonSelectOption>
              <IonSelectOption value="light">{t('settings.light')}</IonSelectOption>
              <IonSelectOption value="dark">{t('settings.dark')}</IonSelectOption>
            </IonSelect>
          </IonItem>

          <IonItem>
            <IonIcon icon={notifications} slot="start" />
            <IonLabel>{t('settings.notifications')}</IonLabel>
            <IonToggle
              checked={notificationsEnabled}
              onIonChange={(e) => setNotificationsEnabled(e.detail.checked)}
            />
          </IonItem>

          {!premium && (
            <IonItem button onClick={() => router.push('/paywall')}>
              <IonIcon icon={star} slot="start" />
              <IonLabel>{t('settings.removeAds')}</IonLabel>
            </IonItem>
          )}

          <IonItem button onClick={resetOnboarding}>
            <IonIcon icon={refresh} slot="start" />
            <IonLabel>{t('settings.resetOnboarding')}</IonLabel>
          </IonItem>
        </IonList>
      </IonContent>
    </IonPage>
  );
};

export default SettingsPage;
```

### Settings Page (Vue)

```vue
<!-- views/SettingsPage.vue -->
<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>{{ t('settings.title') }}</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <ion-list>
        <ion-item>
          <ion-icon name="language" slot="start" />
          <ion-label>{{ t('settings.language') }}</ion-label>
          <ion-select :value="currentLang" @ion-change="changeLanguage($event)">
            <ion-select-option value="en">English</ion-select-option>
            <ion-select-option value="tr">Türkçe</ion-select-option>
          </ion-select>
        </ion-item>

        <ion-item>
          <ion-icon name="color-palette" slot="start" />
          <ion-label>{{ t('settings.theme') }}</ion-label>
          <ion-select :value="currentTheme" @ion-change="changeTheme($event)">
            <ion-select-option value="system">{{ t('settings.system') }}</ion-select-option>
            <ion-select-option value="light">{{ t('settings.light') }}</ion-select-option>
            <ion-select-option value="dark">{{ t('settings.dark') }}</ion-select-option>
          </ion-select>
        </ion-item>

        <ion-item>
          <ion-icon name="notifications" slot="start" />
          <ion-label>{{ t('settings.notifications') }}</ion-label>
          <ion-toggle :checked="notificationsEnabled" @ion-change="toggleNotifications($event)" />
        </ion-item>

        <ion-item v-if="!premium" button @click="removeAds">
          <ion-icon name="star" slot="start" />
          <ion-label>{{ t('settings.removeAds') }}</ion-label>
        </ion-item>

        <ion-item button @click="resetOnboardingFlow">
          <ion-icon name="refresh" slot="start" />
          <ion-label>{{ t('settings.resetOnboarding') }}</ion-label>
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import {
  IonPage, IonHeader, IonToolbar, IonTitle, IonContent,
  IonList, IonItem, IonLabel, IonIcon, IonToggle, IonSelect, IonSelectOption,
} from '@ionic/vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { Preferences } from '@capacitor/preferences';
import { useTheme } from '../composables/useTheme';
import { useOnboarding } from '../composables/useOnboarding';
import { usePurchases } from '../composables/usePurchases';
import type { ThemeMode } from '../utils/theme';

const { t, locale } = useI18n();
const router = useRouter();
const { getTheme, setTheme } = useTheme();
const { reset } = useOnboarding();
const { isPremium } = usePurchases();

const currentLang = ref('en');
const currentTheme = ref<ThemeMode>('system');
const notificationsEnabled = ref(false);
const premium = ref(false);

onMounted(async () => {
  currentLang.value = locale.value || 'en';
  currentTheme.value = await getTheme();
  premium.value = await isPremium();
});

function changeLanguage(event: CustomEvent) {
  const lang = event.detail.value;
  currentLang.value = lang;
  locale.value = lang;
  Preferences.set({ key: 'language', value: lang });
}

function changeTheme(event: CustomEvent) {
  const mode = event.detail.value as ThemeMode;
  currentTheme.value = mode;
  setTheme(mode);
}

function toggleNotifications(event: CustomEvent) {
  notificationsEnabled.value = event.detail.checked;
}

function removeAds() {
  router.push('/paywall');
}

async function resetOnboardingFlow() {
  await reset();
  router.replace('/onboarding');
}
</script>
```

---

## Localization

### Translation Files (Shared - All Frameworks)

```json
// en.json
{
  "tabs": {
    "home": "Home",
    "explore": "Explore",
    "settings": "Settings"
  },
  "onboarding": {
    "next": "Next",
    "start": "Get Started",
    "skip": "Skip"
  },
  "paywall": {
    "title": "Go Premium",
    "weekly": "Weekly",
    "yearly": "Yearly",
    "subscribe": "Subscribe",
    "skip": "Continue with ads",
    "restore": "Restore Purchases"
  },
  "settings": {
    "title": "Settings",
    "language": "Language",
    "theme": "Theme",
    "system": "System",
    "light": "Light",
    "dark": "Dark",
    "notifications": "Notifications",
    "removeAds": "Remove Ads",
    "resetOnboarding": "Reset Onboarding"
  }
}
```

```json
// tr.json
{
  "tabs": {
    "home": "Ana Sayfa",
    "explore": "Keşfet",
    "settings": "Ayarlar"
  },
  "onboarding": {
    "next": "İleri",
    "start": "Başla",
    "skip": "Atla"
  },
  "paywall": {
    "title": "Premium'a Geç",
    "weekly": "Haftalık",
    "yearly": "Yıllık",
    "subscribe": "Abone Ol",
    "skip": "Reklamlı devam et",
    "restore": "Satın Alımları Geri Yükle"
  },
  "settings": {
    "title": "Ayarlar",
    "language": "Dil",
    "theme": "Tema",
    "system": "Sistem",
    "light": "Açık",
    "dark": "Koyu",
    "notifications": "Bildirimler",
    "removeAds": "Reklamları Kaldır",
    "resetOnboarding": "Tanıtımı Sıfırla"
  }
}
```

### TURKISH LOCALIZATION (IMPORTANT)

When writing `tr.json`, you MUST use correct Turkish characters:

- ı (lowercase dotless i) - NOT i
- İ (uppercase dotted I) - NOT I
- ü, Ü, ö, Ö, ç, Ç, ş, Ş, ğ, Ğ

Example:

- ✅ "Ayarlar", "Giriş", "Çıkış", "Başla", "İleri", "Güncelle"
- ❌ "Ayarlar", "Giris", "Cikis", "Basla", "Ileri", "Guncelle"

### i18n Setup (Angular)

i18n is configured in `app.config.ts` using `@ngx-translate/core`. See the App Configuration (Angular) section.

Usage in `.html` template files:

```html
{{ 'settings.title' | translate }}
```

Detect language in `app.component.ts`:

```typescript
import { TranslateService } from '@ngx-translate/core';

constructor(private translate: TranslateService) {
  const browserLang = navigator.language.split('-')[0];
  translate.setDefaultLang('en');
  translate.use(['en', 'tr'].includes(browserLang) ? browserLang : 'en');
}
```

### i18n Setup (React)

i18n is configured in `i18n/index.ts`. See the App Configuration (React) section.

Usage in components:

```tsx
import { useTranslation } from 'react-i18next';

const MyComponent: React.FC = () => {
  const { t } = useTranslation();
  return <h1>{t('settings.title')}</h1>;
};
```

### i18n Setup (Vue)

i18n is configured in `main.ts` using `vue-i18n`. See the App Configuration (Vue) section.

Usage in templates:

```vue
<template>
  <h1>{{ t('settings.title') }}</h1>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
</script>
```

---

## Framework Best Practices

### Angular Best Practices

ALWAYS use standalone components with separate HTML, TS, and SCSS files:

❌ WRONG (NgModules + IonicModule):

```typescript
// home.module.ts
@NgModule({
  imports: [CommonModule, IonicModule],
  declarations: [HomePage],
})
export class HomePageModule {}
```

❌ WRONG (inline templates):

```typescript
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [IonContent, IonHeader, IonTitle, IonToolbar, TranslateModule],
  template: `
    <ion-header>
      <ion-toolbar>
        <ion-title>{{ 'home.title' | translate }}</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <!-- content -->
    </ion-content>
  `,
})
export class HomePage {}
```

✅ CORRECT (separate .html, .ts, .scss files):

```html
<!-- home/home.page.html -->
<ion-header>
  <ion-toolbar>
    <ion-title>{{ 'home.title' | translate }}</ion-title>
  </ion-toolbar>
</ion-header>
<ion-content>
  <!-- content -->
</ion-content>
```

```scss
// home/home.page.scss
// Page-specific styles here
```

```typescript
// home/home.page.ts
@Component({
  selector: 'app-home',
  standalone: true,
  imports: [IonContent, IonHeader, IonTitle, IonToolbar, TranslateModule],
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
})
export class HomePage {}
```

Import individual Ionic components (e.g., `IonContent`, `IonButton`) - NEVER import `IonicModule` in standalone components.
ALWAYS use `templateUrl` + `styleUrls` - NEVER use inline `template` or `styles`.

### React Best Practices

ALWAYS use functional components with hooks:

❌ WRONG:

```tsx
class HomePage extends React.Component {
  render() {
    return <IonContent>...</IonContent>;
  }
}
```

✅ CORRECT:

```tsx
import { IonContent, IonHeader, IonTitle, IonToolbar, IonPage } from '@ionic/react';
import { useTranslation } from 'react-i18next';

const HomePage: React.FC = () => {
  const { t } = useTranslation();

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>{t('home.title')}</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent>
        {/* content */}
      </IonContent>
    </IonPage>
  );
};

export default HomePage;
```

Always wrap page content in `<IonPage>` for proper Ionic page transitions and lifecycle.

### Vue Best Practices

ALWAYS use Composition API with `<script setup>`:

❌ WRONG:

```vue
<script>
export default {
  data() {
    return { title: 'Home' };
  },
};
</script>
```

✅ CORRECT:

```vue
<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>{{ t('home.title') }}</ion-title>
      </ion-toolbar>
    </ion-header>
    <ion-content>
      <!-- content -->
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent } from '@ionic/vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
</script>
```

Always wrap page content in `<ion-page>` for proper Ionic page transitions and lifecycle.

---

## POST-CREATION CLEANUP (ALWAYS DO)

After creating a new Ionic project, you MUST:

1. Remove default generated pages that conflict with your structure
2. Ensure the build configuration has the correct output directory
3. Verify `capacitor.config.ts` has the correct `appId` and `appName`
4. Check that all Ionic imports use the correct framework-specific package

---

## AFTER COMPLETING CODE (ALWAYS RUN)

### Angular

```bash
npm install
npx ng build
npx cap sync
```

### React

```bash
npm install
npm run build
npx cap sync
```

### Vue

```bash
npm install
npm run build
npx cap sync
```

1. `npm install` installs any new dependencies
2. Build compiles the project
3. `cap sync` syncs web assets and plugins to native projects

Do NOT skip these steps.

---

## Development Commands

### Angular

```bash
npm install
ionic serve          # Run in browser
ionic build          # Build for production
npx cap sync         # Sync web assets to native
npx cap open ios     # Open in Xcode
npx cap open android # Open in Android Studio
npx cap run ios      # Build and run on iOS device/simulator
npx cap run android  # Build and run on Android device/emulator
```

### React

```bash
npm install
ionic serve          # Run in browser
ionic build          # Build for production
npx cap sync         # Sync web assets to native
npx cap open ios     # Open in Xcode
npx cap open android # Open in Android Studio
npx cap run ios      # Build and run on iOS
npx cap run android  # Build and run on Android
```

### Vue

```bash
npm install
ionic serve          # Run in browser
ionic build          # Build for production
npx cap sync         # Sync web assets to native
npx cap open ios     # Open in Xcode
npx cap open android # Open in Android Studio
npx cap run ios      # Build and run on iOS
npx cap run android  # Build and run on Android
```

---

## Coding Standards

### All Frameworks

- Strict TypeScript - no `any` types
- Avoid hardcoded strings - use translation keys
- Use `@capacitor/preferences` for persistent storage
- Lazy-load all pages
- Use `Capacitor.isNativePlatform()` to guard native-only code
- Always `await` Capacitor plugin methods

### Angular-Specific

- Use standalone components (NEVER NgModules for pages/components)
- ALWAYS use separate `.html`, `.ts`, `.scss` files - NEVER inline `template` or `styles`
- Use `templateUrl` and `styleUrls` in `@Component` decorator
- Use Angular's `inject()` function or constructor injection
- Lazy-load via `loadComponent` in routes
- Use Angular Signals for reactive state when possible
- Import individual Ionic components - NEVER `IonicModule`
- Use `addIcons()` from `ionicons` to register icons

### React-Specific

- Use functional components with hooks
- Wrap pages in `<IonPage>`
- Use `useIonRouter()` for navigation
- Use `useTranslation()` for i18n
- Import icons directly from `ionicons/icons`

### Vue-Specific

- Use Composition API with `<script setup lang="ts">`
- Wrap pages in `<ion-page>`
- Use `useRouter()` from `vue-router` for navigation
- Use `useI18n()` for i18n
- Import icons from `ionicons/icons` and pass via `:icon` prop

---

## Important Notes

1. iOS permissions are defined in `Info.plist` (added via Capacitor plugins)
2. Android permissions are defined in `AndroidManifest.xml` (added via Capacitor plugins)
3. Always run `npx cap sync` after installing new Capacitor plugins
4. Use `Capacitor.isNativePlatform()` to guard native-only code
5. Test in browser with `ionic serve` for rapid development, then test on devices

## App Store & Play Store Notes

- iOS ATT permission required for personalized ads
- Restore purchases must work correctly
- Target SDK must be up to date
- Use `npx cap sync` before each native build

## Testing Checklist

- UI tested in all languages
- Dark / Light mode
- Notifications
- Premium flow
- Restore purchases
- Offline support
- Multiple screen sizes
- Browser (ionic serve) and native platforms

## After Development

```bash
npm run build
npx cap sync
npx cap open ios
npx cap open android
```

> NOTE: `cap sync` copies the built web app to native projects and syncs plugins. Run it after every build before testing on native platforms.
