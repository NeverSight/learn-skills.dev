---
name: emrah-skills
description: Expo React Native mobile app development with expo-iap in-app purchases, AdMob ads, i18n localization, ATT tracking transparency, optional OIDC authentication, onboarding flow, paywall, and NativeTabs navigation
---

# Expo Mobile Application Development Guide

> **IMPORTANT**: This is a SKILL file, NOT a project. NEVER run npm/bun install in this folder. NEVER create code files here. When creating a new project, ALWAYS ask the user for the project path first or create it in a separate directory (e.g., `~/Projects/app-name`).

This guide is created to provide context when working with Expo projects using Claude Code.

## MANDATORY REQUIREMENTS

When creating a new Expo project, you MUST include ALL of the following:

### Required Screens (ALWAYS CREATE)

- [ ] `src/app/att-permission.tsx` - App Tracking Transparency permission screen (**iOS only**, shown BEFORE onboarding)
- [ ] `src/app/onboarding.tsx` - Swipe-based onboarding with fullscreen background video and gradient overlay
- [ ] `src/app/paywall.tsx` - expo-iap paywall screen (shown after onboarding)
- [ ] `src/app/settings.tsx` - Settings screen with language, theme, notifications, and reset onboarding options

### Onboarding Screen Implementation (REQUIRED)

The onboarding screen MUST have a fullscreen background video. Use a **local asset** (`require("@/assets/...")`). The video is looped, muted, and played automatically.

Full implementation of `src/app/onboarding.tsx`:

```tsx
import { useOnboarding } from "@/context/onboarding-context";
import { MaterialIcons } from "@expo/vector-icons";
import { LinearGradient } from "expo-linear-gradient";
import { router } from "expo-router";
import { useVideoPlayer, VideoView } from "expo-video";
import { useRef, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  Dimensions,
  FlatList,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const VIDEO_SOURCE = require("@/assets/onboarding.mp4");

const { width: SCREEN_WIDTH } = Dimensions.get("window");

const SLIDES = [
  {
    key: "1",
    titleKey: "onboarding.slide1.title",
    descKey: "onboarding.slide1.description",
    icon: "access-time",
  },
  {
    key: "2",
    titleKey: "onboarding.slide2.title",
    descKey: "onboarding.slide2.description",
    icon: "explore",
  },
  {
    key: "3",
    titleKey: "onboarding.slide3.title",
    descKey: "onboarding.slide3.description",
    icon: "calendar-today",
  },
  {
    key: "4",
    titleKey: "onboarding.slide4.title",
    descKey: "onboarding.slide4.description",
    icon: "lock",
  },
];

export default function OnboardingScreen() {
  const { t } = useTranslation();
  const { setOnboardingCompleted } = useOnboarding();
  const [activeIndex, setActiveIndex] = useState(0);
  const flatListRef = useRef<FlatList>(null);

  const player = useVideoPlayer(VIDEO_SOURCE, (p) => {
    p.loop = true;
    p.muted = true;
    p.play();
  });

  const handleNext = () => {
    if (activeIndex < SLIDES.length - 1) {
      flatListRef.current?.scrollToIndex({
        index: activeIndex + 1,
        animated: true,
      });
      setActiveIndex(activeIndex + 1);
    } else {
      handleComplete();
    }
  };

  const handleComplete = async () => {
    await setOnboardingCompleted(true);
    router.replace("/paywall");
  };

  const isLast = activeIndex === SLIDES.length - 1;

  return (
    <View style={styles.container}>
      {/* Background video */}
      <VideoView
        player={player}
        style={StyleSheet.absoluteFill}
        contentFit="cover"
        nativeControls={false}
      />
      {/* Gradient overlay */}
      <LinearGradient
        colors={["rgba(0,0,0,0.3)", "rgba(0,0,0,0.7)", "rgba(0,0,0,0.9)"]}
        style={StyleSheet.absoluteFill}
      />

      <SafeAreaView style={styles.safeArea}>
        {/* Skip button */}
        <View style={styles.topBar}>
          <TouchableOpacity onPress={handleComplete} style={styles.skipButton}>
            <Text style={styles.skipButtonText}>{t("onboarding.skip")}</Text>
          </TouchableOpacity>
        </View>

        {/* Slides */}
        <FlatList
          ref={flatListRef}
          data={SLIDES}
          horizontal
          pagingEnabled
          scrollEnabled
          showsHorizontalScrollIndicator={false}
          keyExtractor={(item) => item.key}
          onMomentumScrollEnd={(e) => {
            const index = Math.round(
              e.nativeEvent.contentOffset.x / SCREEN_WIDTH,
            );
            setActiveIndex(index);
          }}
          renderItem={({ item }) => (
            <View style={styles.slide}>
              <View
                style={{
                  width: 96,
                  height: 96,
                  borderRadius: 48,
                  alignItems: "center",
                  justifyContent: "center",
                  marginBottom: 32,
                  backgroundColor: "rgba(65,114,157,0.35)",
                  borderWidth: 1.5,
                  borderColor: "rgba(65,114,157,0.6)",
                }}
              >
                <MaterialIcons
                  name={item.icon as any}
                  size={52}
                  color="#FFFFFF"
                />
              </View>
              <Text style={styles.slideTitle}>{t(item.titleKey)}</Text>
              <Text style={styles.slideDesc}>{t(item.descKey)}</Text>
            </View>
          )}
        />

        {/* Dots */}
        <View style={styles.dotsContainer}>
          {SLIDES.map((_, i) => (
            <View
              key={i}
              style={[
                styles.dot,
                i === activeIndex ? styles.dotActive : styles.dotInactive,
              ]}
            />
          ))}
        </View>

        {/* CTA */}
        <View style={styles.ctaContainer}>
          <TouchableOpacity onPress={handleNext} style={styles.ctaButton}>
            <Text style={styles.ctaButtonText}>
              {isLast ? t("onboarding.getStarted") : t("onboarding.next")}
            </Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#000" },
  safeArea: { flex: 1 },
  topBar: {
    flexDirection: "row",
    justifyContent: "flex-end",
    paddingHorizontal: 20,
    paddingTop: 8,
  },
  slide: {
    width: SCREEN_WIDTH,
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 40,
  },
  skipButton: {
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.25)",
    backgroundColor: "rgba(255,255,255,0.15)",
    borderRadius: 20,
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  skipButtonText: {
    color: "rgba(255,255,255,0.85)",
    fontSize: 13,
    fontWeight: "600",
  },
  slideTitle: {
    fontSize: 36,
    fontWeight: "700",
    color: "#FFFFFF",
    textAlign: "center",
    marginBottom: 16,
  },
  slideDesc: {
    fontSize: 17,
    color: "rgba(255,255,255,0.75)",
    textAlign: "center",
  },
  dotsContainer: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 8,
    marginBottom: 24,
  },
  dot: {
    height: 8,
    borderRadius: 4,
  },
  dotActive: {
    width: 24,
    backgroundColor: "#FFFFFF",
  },
  dotInactive: {
    width: 8,
    backgroundColor: "rgba(255,255,255,0.3)",
  },
  ctaContainer: {
    paddingHorizontal: 24,
    paddingBottom: 40,
  },
  ctaButton: {
    width: "100%",
    backgroundColor: "#6C63FF",
    borderRadius: 16,
    alignItems: "center",
    paddingVertical: 16,
  },
  ctaButtonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "700",
  },
});
```

> **Notes:**
>
> - Place your onboarding video at `assets/onboarding.mp4` (adjust the `require` path to match the actual file)
> - `SafeAreaView` is from `react-native-safe-area-context`, NOT `react-native`
> - Slide icons use `@expo/vector-icons` `MaterialIcons` — adjust icon names per app theme
> - Slides array and icon names should be customized per app
> - Add required i18n keys: `onboarding.slide1.title`, `onboarding.slide1.description`, etc., plus `onboarding.skip`, `onboarding.next`, `onboarding.getStarted`

### Required Navigation (ALWAYS USE)

- [ ] Use `NativeTabs` from `expo-router/unstable-native-tabs` for tab navigation - NEVER use `@react-navigation/bottom-tabs` or `Tabs` from expo-router

### Required Context Providers (ALWAYS WRAP)

```tsx
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { ThemeProvider } from "@/context/theme-context";
import { PurchasesProvider } from "@/context/purchases-context";
import {
  DarkTheme,
  DefaultTheme,
  ThemeProvider as NavigationThemeProvider,
} from "@react-navigation/native";

<GestureHandlerRootView style={{ flex: 1 }}>
  <ThemeProvider>
    <OnboardingProvider>
      <PurchasesProvider>
        <AdsProvider>
          <NavigationThemeProvider
            value={colorScheme === "dark" ? DarkTheme : DefaultTheme}
          >
            <Stack />
          </NavigationThemeProvider>
        </AdsProvider>
      </PurchasesProvider>
    </OnboardingProvider>
  </ThemeProvider>
</GestureHandlerRootView>;
```

### Required Libraries (ALWAYS INSTALL)

Use `npx expo install` to install Expo libraries (NOT npm/yarn/bun install).
Use `bun add` for non-Expo libraries:

```bash
# Expo libraries
npx expo install expo-iap expo-build-properties expo-tracking-transparency react-native-google-mobile-ads expo-notifications i18next react-i18next expo-localization react-native-reanimated expo-video expo-audio expo-sqlite expo-linear-gradient

# Peer dependencies
npx expo install react-native-screens react-native-reanimated react-native-gesture-handler react-native-safe-area-context react-native-svg
```

Libraries:

- `expo-iap` (In-App Purchases)
- `expo-build-properties` (required by expo-iap)
- `expo-tracking-transparency` (ATT — iOS App Tracking Transparency)
- `react-native-google-mobile-ads` (AdMob)
- `expo-notifications`
- `i18next` + `react-i18next` + `expo-localization`
- `react-native-reanimated`
- `expo-video` + `expo-audio`
- `expo-sqlite` (for localStorage)
- `expo-linear-gradient` (for gradient overlays)

### expo-iap Configuration (REQUIRED in app.json)

You MUST add this to `app.json` for expo-iap to work (Expo SDK 53+):

```json
{
  "expo": {
    "plugins": [
      "expo-iap",
      ["expo-build-properties", { "android": { "kotlinVersion": "2.2.0" } }]
    ]
  }
}
```

- Requires Expo SDK 53+ or React Native 0.79+
- iOS 15+ (StoreKit 2), Android API 21+
- Does NOT work in Expo Go — use custom dev client (`eas build --profile development`)

### AdMob Configuration (REQUIRED in app.json)

You MUST add this to `app.json` for AdMob to work:

```json
{
  "expo": {
    "plugins": [
      [
        "react-native-google-mobile-ads",
        {
          "androidAppId": "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy",
          "iosAppId": "ca-app-pub-xxxxxxxxxxxxxxxx~yyyyyyyyyy"
        }
      ]
    ]
  }
}
```

For development/testing, use test App IDs:

- iOS: `ca-app-pub-3940256099942544~1458002511`
- Android: `ca-app-pub-3940256099942544~3347511713`

Do NOT skip this configuration or the app will crash with `GADInvalidInitializationException`.

### Ad Strategy (Revenue-Optimised, UX-Friendly)

Use all five AdMob formats for maximum revenue with minimal UX friction:

| Format           | Trigger                             | Cooldown              | Premium Hidden |
| ---------------- | ----------------------------------- | --------------------- | -------------- |
| **App Open**     | App foreground (after first launch) | 4 hours               | ✅             |
| **Banner**       | Tab bar, always visible             | None                  | ✅             |
| **Native**       | In-feed, every 5 items in FlatList  | None                  | ✅             |
| **Interstitial** | After key user action               | 3 minutes / max 3/day | ✅             |
| **Rewarded**     | User-initiated, for a benefit       | User-triggered        | ✅             |

All ad formats are **hidden for premium users** via `shouldShowAds`.

#### AdsProvider Implementation (REQUIRED)

Create `src/context/ads-context.tsx`:

```tsx
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import { AppState, AppStateStatus } from "react-native";
import {
  AdEventType,
  AppOpenAd,
  InterstitialAd,
  RewardedAd,
  RewardedAdEventType,
  TestIds,
} from "react-native-google-mobile-ads";
import { usePurchases } from "@/context/purchases-context";
import "expo-sqlite/localStorage/install";

// ── Ad Unit IDs ──────────────────────────────────────────────
export const AD_UNITS = {
  banner: __DEV__ ? TestIds.BANNER : "ca-app-pub-xxxxxxxxxxxxxxxx/BANNER_ID",
  interstitial: __DEV__
    ? TestIds.INTERSTITIAL
    : "ca-app-pub-xxxxxxxxxxxxxxxx/INTERSTITIAL_ID",
  rewarded: __DEV__
    ? TestIds.REWARDED
    : "ca-app-pub-xxxxxxxxxxxxxxxx/REWARDED_ID",
  appOpen: __DEV__
    ? TestIds.APP_OPEN
    : "ca-app-pub-xxxxxxxxxxxxxxxx/APP_OPEN_ID",
  native: __DEV__ ? TestIds.NATIVE : "ca-app-pub-xxxxxxxxxxxxxxxx/NATIVE_ID",
};

// ── Constants ────────────────────────────────────────────────
const APP_OPEN_COOLDOWN_MS = 4 * 60 * 60 * 1000; // 4 hours
const INTERSTITIAL_COOLDOWN_MS = 3 * 60 * 1000; // 3 minutes
const INTERSTITIAL_DAILY_CAP = 3;

const LS_APP_OPEN_KEY = "ads_app_open_last_shown";
const LS_INTER_DATE_KEY = "ads_inter_last_date";
const LS_INTER_COUNT_KEY = "ads_inter_count_today";
const LS_INTER_TS_KEY = "ads_inter_last_ts";

function todayDateString() {
  return new Date().toISOString().slice(0, 10);
}

// ── Context ──────────────────────────────────────────────────
interface AdsContextValue {
  shouldShowAds: boolean;
  bannerAdUnitId: string;
  nativeAdUnitId: string;
  showInterstitial: () => void;
  showRewarded: () => Promise<boolean>;
}

const AdsContext = createContext<AdsContextValue>({
  shouldShowAds: true,
  bannerAdUnitId: AD_UNITS.banner,
  nativeAdUnitId: AD_UNITS.native,
  showInterstitial: () => {},
  showRewarded: async () => false,
});

export function AdsProvider({ children }: { children: React.ReactNode }) {
  const { isPremium } = usePurchases();
  const shouldShowAds = !isPremium;

  // ── App Open ─────────────────────────────────────────────
  const appOpenAdRef = useRef<AppOpenAd | null>(null);
  const appOpenLoadedRef = useRef(false);
  const isFirstLaunchRef = useRef(true);

  const loadAppOpen = useCallback(() => {
    if (!shouldShowAds) return;
    const ad = AppOpenAd.createForAdRequest(AD_UNITS.appOpen, {
      requestNonPersonalizedAdsOnly: true,
    });
    ad.addEventHandler(AdEventType.LOADED, () => {
      appOpenLoadedRef.current = true;
    });
    ad.addEventHandler(AdEventType.CLOSED, () => {
      appOpenLoadedRef.current = false;
      appOpenAdRef.current = null;
      loadAppOpen();
    });
    ad.addEventHandler(AdEventType.ERROR, () => {
      appOpenLoadedRef.current = false;
      setTimeout(loadAppOpen, 30_000);
    });
    ad.load();
    appOpenAdRef.current = ad;
  }, [shouldShowAds]);

  const tryShowAppOpen = useCallback(() => {
    if (!shouldShowAds || !appOpenLoadedRef.current || !appOpenAdRef.current)
      return;
    // Skip on first cold launch
    if (isFirstLaunchRef.current) {
      isFirstLaunchRef.current = false;
      return;
    }
    const lastShown = globalThis.localStorage.getItem(LS_APP_OPEN_KEY);
    const now = Date.now();
    if (lastShown && now - parseInt(lastShown, 10) < APP_OPEN_COOLDOWN_MS)
      return;
    globalThis.localStorage.setItem(LS_APP_OPEN_KEY, String(now));
    appOpenAdRef.current.show().catch(() => loadAppOpen());
  }, [shouldShowAds, loadAppOpen]);

  const appStateRef = useRef<AppStateStatus>(AppState.currentState);

  useEffect(() => {
    if (!shouldShowAds) return;
    loadAppOpen();
    const sub = AppState.addEventListener("change", (state) => {
      if (appStateRef.current !== "active" && state === "active") {
        tryShowAppOpen();
      }
      appStateRef.current = state;
    });
    return () => sub.remove();
  }, [shouldShowAds, loadAppOpen, tryShowAppOpen]);

  // ── Interstitial ──────────────────────────────────────────
  const interstitialRef = useRef<InterstitialAd | null>(null);
  const interstitialLoadedRef = useRef(false);

  const loadInterstitial = useCallback(() => {
    if (!shouldShowAds) return;
    const ad = InterstitialAd.createForAdRequest(AD_UNITS.interstitial, {
      requestNonPersonalizedAdsOnly: true,
    });
    ad.addEventHandler(AdEventType.LOADED, () => {
      interstitialLoadedRef.current = true;
    });
    ad.addEventHandler(AdEventType.CLOSED, () => {
      interstitialLoadedRef.current = false;
      interstitialRef.current = null;
      loadInterstitial();
    });
    ad.addEventHandler(AdEventType.ERROR, () => {
      interstitialLoadedRef.current = false;
    });
    ad.load();
    interstitialRef.current = ad;
  }, [shouldShowAds]);

  useEffect(() => {
    if (shouldShowAds) loadInterstitial();
  }, [shouldShowAds, loadInterstitial]);

  const showInterstitial = useCallback(() => {
    if (
      !shouldShowAds ||
      !interstitialLoadedRef.current ||
      !interstitialRef.current
    )
      return;
    const now = Date.now();
    const today = todayDateString();
    const lastDate = globalThis.localStorage.getItem(LS_INTER_DATE_KEY);
    let countToday = parseInt(
      globalThis.localStorage.getItem(LS_INTER_COUNT_KEY) ?? "0",
      10,
    );
    if (lastDate !== today) {
      countToday = 0;
      globalThis.localStorage.setItem(LS_INTER_DATE_KEY, today);
    }
    if (countToday >= INTERSTITIAL_DAILY_CAP) return;
    const lastTs = parseInt(
      globalThis.localStorage.getItem(LS_INTER_TS_KEY) ?? "0",
      10,
    );
    if (now - lastTs < INTERSTITIAL_COOLDOWN_MS) return;
    globalThis.localStorage.setItem(LS_INTER_TS_KEY, String(now));
    globalThis.localStorage.setItem(LS_INTER_COUNT_KEY, String(countToday + 1));
    interstitialRef.current.show().catch(() => loadInterstitial());
  }, [shouldShowAds, loadInterstitial]);

  // ── Rewarded ──────────────────────────────────────────────
  const rewardedRef = useRef<RewardedAd | null>(null);
  const rewardedLoadedRef = useRef(false);

  const loadRewarded = useCallback(() => {
    if (!shouldShowAds) return;
    const ad = RewardedAd.createForAdRequest(AD_UNITS.rewarded, {
      requestNonPersonalizedAdsOnly: true,
    });
    ad.addEventHandler(RewardedAdEventType.LOADED, () => {
      rewardedLoadedRef.current = true;
    });
    ad.addEventHandler(AdEventType.CLOSED, () => {
      rewardedLoadedRef.current = false;
      rewardedRef.current = null;
      loadRewarded();
    });
    ad.addEventHandler(AdEventType.ERROR, () => {
      rewardedLoadedRef.current = false;
    });
    ad.load();
    rewardedRef.current = ad;
  }, [shouldShowAds]);

  useEffect(() => {
    if (shouldShowAds) loadRewarded();
  }, [shouldShowAds, loadRewarded]);

  const showRewarded = useCallback((): Promise<boolean> => {
    return new Promise((resolve) => {
      if (
        !shouldShowAds ||
        !rewardedLoadedRef.current ||
        !rewardedRef.current
      ) {
        resolve(false);
        return;
      }
      const ad = rewardedRef.current!;
      let rewarded = false;
      ad.addEventHandler(RewardedAdEventType.EARNED_REWARD, () => {
        rewarded = true;
      });
      ad.addEventHandler(AdEventType.CLOSED, () => {
        resolve(rewarded);
      });
      ad.show().catch(() => resolve(false));
    });
  }, [shouldShowAds]);

  return (
    <AdsContext.Provider
      value={{
        shouldShowAds,
        bannerAdUnitId: AD_UNITS.banner,
        nativeAdUnitId: AD_UNITS.native,
        showInterstitial,
        showRewarded,
      }}
    >
      {children}
    </AdsContext.Provider>
  );
}

export function useAds() {
  return useContext(AdsContext);
}
```

#### Banner Ad (Tab Layout)

Place the banner below `NativeTabs` in `src/app/(tabs)/_layout.tsx`:

```tsx
import { View, StyleSheet } from "react-native";
import { NativeTabs } from "expo-router/unstable-native-tabs";
import { useTranslation } from "react-i18next";
import { BannerAd, BannerAdSize } from "react-native-google-mobile-ads";
import { useAds } from "@/context/ads-context";

export default function TabLayout() {
  const { t } = useTranslation();
  const { shouldShowAds, bannerAdUnitId } = useAds();

  return (
    <View style={styles.container}>
      <NativeTabs>
        <NativeTabs.Trigger name="index">
          <NativeTabs.Trigger.Label>{t("tabs.home")}</NativeTabs.Trigger.Label>
          <NativeTabs.Trigger.Icon sf="house.fill" md="home" />
        </NativeTabs.Trigger>
        <NativeTabs.Trigger name="settings">
          <NativeTabs.Trigger.Label>
            {t("tabs.settings")}
          </NativeTabs.Trigger.Label>
          <NativeTabs.Trigger.Icon sf="gear" md="settings" />
        </NativeTabs.Trigger>
      </NativeTabs>

      {shouldShowAds && (
        <View style={styles.adContainer}>
          <BannerAd
            unitId={bannerAdUnitId}
            size={BannerAdSize.ANCHORED_ADAPTIVE_BANNER}
            requestOptions={{ requestNonPersonalizedAdsOnly: true }}
          />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  adContainer: { alignItems: "center", paddingBottom: 10 },
});
```

#### App Open Ad

`AdsProvider` handles App Open automatically via `AppState` listener. No extra setup is needed in screens.

```
First cold launch → NO App Open (avoids jarring first impression)
foreground return → App Open shown only if ≥ 4 hours since last shown
```

- The 4-hour timestamp is stored in `localStorage` under `ads_app_open_last_shown`
- `isFirstLaunchRef` ensures the ad never fires on the initial cold open
- After `AdsProvider` mounts, the App Open ad is preloaded silently and auto-reloaded after each show

#### Interstitial Usage Pattern

Call `showInterstitial()` from `useAds()` **after** a meaningful user action. Cooldown (3 min) and daily cap (3/day) are enforced automatically — just call it freely at good breakpoints.

```tsx
import { useAds } from "@/context/ads-context";

function SomeScreen() {
  const { showInterstitial } = useAds();

  const handleActionComplete = async () => {
    await doSomething();
    showInterstitial(); // fire-and-forget, respects cooldown + cap
  };
}
```

**Good trigger points:** after completing a level / generating content / sharing a result

**Avoid:** on screen mount, during navigation, mid-form, or on back press

#### Native Ad (In-Feed)

Create `src/components/ads/NativeAdCard.tsx`:

```tsx
import { View, Text, StyleSheet } from "react-native";
import {
  NativeAd,
  NativeAdView,
  HeadlineView,
  BodyView,
  CallToActionView,
  AdvertiserView,
} from "react-native-google-mobile-ads";
import { useEffect, useState } from "react";
import { useAds } from "@/context/ads-context";

export function NativeAdCard() {
  const { nativeAdUnitId, shouldShowAds } = useAds();
  const [nativeAd, setNativeAd] = useState<NativeAd | null>(null);

  useEffect(() => {
    if (!shouldShowAds) return;
    const ad = new NativeAd(nativeAdUnitId);
    ad.load()
      .then(() => setNativeAd(ad))
      .catch(() => {});
    return () => ad.destroy();
  }, [shouldShowAds, nativeAdUnitId]);

  if (!nativeAd || !shouldShowAds) return null;

  return (
    <NativeAdView nativeAd={nativeAd} style={styles.container}>
      <View style={styles.badge}>
        <Text style={styles.badgeText}>Ad</Text>
      </View>
      <AdvertiserView style={styles.advertiser} />
      <HeadlineView style={styles.headline} />
      <BodyView style={styles.body} />
      <CallToActionView style={styles.cta} />
    </NativeAdView>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: "rgba(255,255,255,0.05)",
    borderRadius: 12,
    padding: 14,
    marginHorizontal: 16,
    marginVertical: 4,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.08)",
  },
  badge: {
    alignSelf: "flex-start",
    backgroundColor: "#F59E0B",
    borderRadius: 4,
    paddingHorizontal: 6,
    paddingVertical: 2,
    marginBottom: 6,
  },
  badgeText: { color: "#000", fontSize: 10, fontWeight: "700" },
  advertiser: { color: "rgba(255,255,255,0.4)", fontSize: 11 },
  headline: {
    color: "#FFFFFF",
    fontSize: 15,
    fontWeight: "700",
    marginVertical: 4,
  },
  body: { color: "rgba(255,255,255,0.65)", fontSize: 13 },
  cta: {
    marginTop: 10,
    backgroundColor: "#2563EB",
    borderRadius: 8,
    paddingHorizontal: 14,
    paddingVertical: 8,
    alignSelf: "flex-start",
    overflow: "hidden",
  },
});
```

**Inject into FlatList every 5 items:**

```tsx
import { NativeAdCard } from "@/components/ads/NativeAdCard";
import { useAds } from "@/context/ads-context";
import { useMemo } from "react";

const NATIVE_AD_INTERVAL = 5;

function MyListScreen() {
  const { shouldShowAds } = useAds();

  const listData = useMemo(() => {
    if (!shouldShowAds)
      return items.map((item) => ({ type: "item" as const, item }));
    return items.flatMap((item, i) => {
      const result: any[] = [{ type: "item", item }];
      if ((i + 1) % NATIVE_AD_INTERVAL === 0) {
        result.push({ type: "native_ad", key: `ad_${i}` });
      }
      return result;
    });
  }, [items, shouldShowAds]);

  return (
    <FlatList
      data={listData}
      keyExtractor={(entry) =>
        entry.type === "item" ? entry.item.id : entry.key
      }
      renderItem={({ item: entry }) =>
        entry.type === "native_ad" ? (
          <NativeAdCard />
        ) : (
          <MyItemComponent item={entry.item} />
        )
      }
    />
  );
}
```

#### Rewarded Ad Usage Pattern

```tsx
import { useAds } from "@/context/ads-context";

function SomeScreen() {
  const { showRewarded } = useAds();

  const handleWatchAd = async () => {
    const earned = await showRewarded();
    if (earned) {
      unlockPremiumContent(); // grant the reward
    }
  };
}
```

**Good use-cases:** skip a waiting period, unlock a single feature temporarily, grant extra credits/attempts

#### Ad Unit ID Configuration

Replace the placeholder IDs in `AD_UNITS` inside `src/context/ads-context.tsx`:

| Format       | Constant                | AdMob Console Location            |
| ------------ | ----------------------- | --------------------------------- |
| Banner       | `AD_UNITS.banner`       | Apps → Ad units → Banner          |
| Interstitial | `AD_UNITS.interstitial` | Apps → Ad units → Interstitial    |
| Rewarded     | `AD_UNITS.rewarded`     | Apps → Ad units → Rewarded        |
| App Open     | `AD_UNITS.appOpen`      | Apps → Ad units → App open        |
| Native       | `AD_UNITS.native`       | Apps → Ad units → Native advanced |

- ALWAYS use `TestIds.*` in `__DEV__` to avoid policy violations
- `shouldShowAds = !isPremium` — all formats hidden for premium users
- `AdsProvider` must be nested **inside** `PurchasesProvider`

### TURKISH LOCALIZATION (IMPORTANT)

When writing `tr.json`, you MUST use correct Turkish characters:

- ı (lowercase dotless i) - NOT i
- İ (uppercase dotted I) - NOT I
- ü, Ü, ö, Ö, ç, Ç, ş, Ş, ğ, Ğ

Example:

- ✅ "Ayarlar", "Giriş", "Çıkış", "Başla", "İleri", "Güncelle"
- ❌ "Ayarlar", "Giris", "Cikis", "Basla", "Ileri", "Guncelle"

### FORBIDDEN (NEVER USE)

- ❌ AsyncStorage - Use `expo-sqlite/localStorage/install` instead
- ❌ lineHeight style - Use padding/margin instead
- ❌ `Tabs` from expo-router - Use `NativeTabs` instead
- ❌ `@react-navigation/bottom-tabs` - Use `NativeTabs` instead
- ❌ `expo-av` - Use `expo-video` for video, `expo-audio` for audio instead
- ❌ `expo-ads-admob` - Use `react-native-google-mobile-ads` instead
- ❌ Any other ads library - ONLY use `react-native-google-mobile-ads`
- ❌ Reanimated hooks inside callbacks - Call at component top level
- ❌ `SafeAreaView` from `react-native` - Use `import { SafeAreaView } from 'react-native-safe-area-context'` instead

### Reanimated Usage (IMPORTANT)

NEVER call `useAnimatedStyle`, `useSharedValue`, or other reanimated hooks inside callbacks, loops, or conditions.

❌ WRONG:

```tsx
const renderItem = () => {
  const animatedStyle = useAnimatedStyle(() => ({ opacity: 1 })); // ERROR!
  return <Animated.View style={animatedStyle} />;
};
```

✅ CORRECT:

```tsx
function MyComponent() {
  const animatedStyle = useAnimatedStyle(() => ({ opacity: 1 })); // Top level
  return <Animated.View style={animatedStyle} />;
}
```

For lists, create a separate component for each item:

```tsx
function AnimatedItem({ item }) {
  const animatedStyle = useAnimatedStyle(() => ({ opacity: 1 }));
  return <Animated.View style={animatedStyle}>{item.name}</Animated.View>;
}

// In FlatList:
renderItem={({ item }) => <AnimatedItem item={item} />}
```

### POST-CREATION CLEANUP (ALWAYS DO)

After creating a new Expo project, you MUST:

1. If using `(tabs)` folder, DELETE `src/app/index.tsx` to avoid route conflicts:

```bash
rm src/app/index.tsx
```

2. Check and remove `lineHeight` from these files:

- `src/components/themed-text.tsx` (comes with lineHeight by default - REMOVE IT)
- Any other component using `lineHeight`

Search and remove all `lineHeight` occurrences:

```bash
grep -r "lineHeight" src/
```

Replace with padding or margin instead.

### AFTER BUILDING A SCREEN (ALWAYS DO)

For EVERY screen you create or modify, you MUST also create or update the corresponding Maestro test flow in `.maestro/`:

| Screen                       | Flow file                                                              |
| ---------------------------- | ---------------------------------------------------------------------- |
| `src/app/att-permission.tsx` | `.maestro/01_att_permission.yaml`                                      |
| `src/app/onboarding.tsx`     | `.maestro/02_onboarding.yaml`                                          |
| `src/app/paywall.tsx`        | `.maestro/03_paywall_skip.yaml` + `.maestro/04_paywall_subscribe.yaml` |
| `src/app/(tabs)/index.tsx`   | `.maestro/05_main_tabs.yaml`                                           |
| `src/app/settings.tsx`       | `.maestro/06_settings.yaml`                                            |
| Any new tab/screen           | `.maestro/0N_<screen_name>.yaml`                                       |

When creating a **new project**, also create the GitHub Actions workflows:

| File                                    | Purpose                          |
| --------------------------------------- | -------------------------------- |
| `.github/workflows/maestro-android.yml` | Android emulator E2E (ubuntu)    |
| `.github/workflows/maestro-ios.yml`     | iOS simulator E2E (macos runner) |

Always add `testID` props to key interactive elements:

```tsx
<TouchableOpacity testID="skip-button" onPress={handleSkip}>
<TouchableOpacity testID="close-button" onPress={handleClose}>
<TouchableOpacity testID="subscribe-button" onPress={handleSubscribe}>
<TouchableOpacity testID="get-started-button" onPress={handleComplete}>
```

Never skip this step. Screen code and its Maestro flow are delivered together.

### AFTER COMPLETING CODE (ALWAYS RUN)

When you finish writing/modifying code, you MUST run these commands in order:

```bash
npx expo install --fix
npx expo prebuild --clean
```

1. `install --fix` fixes dependency version mismatches
2. `prebuild --clean` recreates ios and android folders

Do NOT skip these steps.

---

## Project Creation

When user asks to create an app, you MUST:

1. FIRST ask for the bundle ID (e.g., "What is the bundle ID? Example: com.company.appname")
2. **SECOND ask: "Does the app require user login/authentication (OIDC)?"**
   - If **YES** → follow the [Authentication (OIDC)](#authentication-oidc--optional) section after project setup
   - If **NO** → skip auth entirely
3. Create the project in the CURRENT directory using:

```bash
bunx create-expo -t default@next app-name
```

3. Update `app.json` with the bundle ID:

```json
{
  "expo": {
    "ios": {
      "bundleIdentifier": "com.company.appname"
    },
    "android": {
      "package": "com.company.appname"
    }
  }
}
```

4. Then cd into the project and start implementing all required screens
5. Do NOT ask for project path - always use current directory

## Technology Stack

- **Framework**: Expo, React Native
- **Navigation**: Expo Router (file-based routing), NativeTabs
- **State Management**: React Context API
- **Translations**: i18next, react-i18next
- **Purchases**: expo-iap (expo-iap)
- **Advertisements**: Google AdMob (react-native-google-mobile-ads)
- **Notifications**: expo-notifications
- **Animations**: react-native-reanimated
- **Storage**: localStorage via expo-sqlite polyfill
- **Authentication** _(optional)_: OIDC via expo-auth-session + expo-secure-store + zustand

> **WARNING**: DO NOT USE AsyncStorage! Use expo-sqlite polyfill instead.

- Example usage

```js
import "expo-sqlite/localStorage/install";

globalThis.localStorage.setItem("key", "value");
console.log(globalThis.localStorage.getItem("key")); // 'value'
```

> **WARNING**: NEVER USE `lineHeight`! It causes layout issues in React Native. Use padding or margin instead.

## Project Structure

```
project-root/
├── src/
│   ├── app/
│   │   ├── _layout.tsx
│   │   ├── index.tsx
│   │   ├── explore.tsx
│   │   ├── settings.tsx
│   │   ├── paywall.tsx
│   │   ├── onboarding.tsx
│   │   └── att-permission.tsx
│   ├── components/
│   │   ├── ui/
│   │   ├── themed-text.tsx
│   │   └── themed-view.tsx
│   ├── constants/
│   │   ├── theme.ts
│   │   └── [data-files].ts
│   ├── context/
│   │   ├── onboarding-context.tsx
│   │   ├── purchases-context.tsx
│   │   └── ads-context.tsx
│   ├── store/                        # (if auth enabled)
│   │   ├── authStore.ts
│   │   └── useIntegratedAuth.ts
│   ├── hooks/
│   │   ├── use-notifications.ts
│   │   └── use-color-scheme.ts
│   ├── lib/
│   │   ├── notifications.ts
│   │   ├── purchases.ts
│   │   ├── ads.ts
│   │   └── i18n.ts
│   ├── services/                     # (if auth enabled)
│   │   └── identity/
│   │       ├── index.ts
│   │       ├── types.ts
│   │       └── hooks/
│   └── locales/
│       ├── tr.json
│       └── en.json
├── .github/
│   └── workflows/
│       ├── maestro-android.yml       # Android E2E (ubuntu, free)
│       └── maestro-ios.yml           # iOS E2E (macos runner)
├── .maestro/
│   ├── 00_app_launch.yaml
│   ├── 01_att_permission.yaml
│   ├── 02_onboarding.yaml
│   ├── 03_paywall_skip.yaml
│   ├── 04_paywall_subscribe.yaml
│   ├── 05_main_tabs.yaml
│   ├── 06_settings.yaml
│   └── 07_full_flow.yaml
├── assets/
│   └── images/
├── ios/
├── android/
├── app.json
├── eas.json
├── package.json
└── tsconfig.json
```

## Tab Navigation (NativeTabs)

Expo Router uses NativeTabs for native tab navigation:

```tsx
import { NativeTabs } from "expo-router/unstable-native-tabs";

export default function TabLayout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="index">
        <NativeTabs.Trigger.Label>Home</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="house.fill" md="home" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="explore">
        <NativeTabs.Trigger.Label>Explore</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="compass.fill" md="explore" />
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="settings">
        <NativeTabs.Trigger.Label>Settings</NativeTabs.Trigger.Label>
        <NativeTabs.Trigger.Icon sf="gear" md="settings" />
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
```

### NativeTabs Properties

- **sf**: SF Symbols icon name (iOS)
- **md**: Material Design icon name (Android)
- **name**: Route file name
- Tab order follows trigger order

### Common Icons

| Purpose       | SF Symbol       | Material Icon |
| ------------- | --------------- | ------------- |
| Home          | house.fill      | home          |
| Explore       | compass.fill    | explore       |
| Settings      | gear            | settings      |
| Profile       | person.fill     | person        |
| Search        | magnifyingglass | search        |
| Favorites     | heart.fill      | favorite      |
| Notifications | bell.fill       | notifications |

## Development Commands

```bash
bun install
bun start
bun ios
bun android
bun lint
npx expo install --fix
npx expo prebuild --clean
```

## EAS Build Commands

```bash
eas build --profile development --platform ios
eas build --profile development --platform android
eas build --profile production --platform ios
eas build --profile production --platform android
eas submit --platform ios
eas submit --platform android
```

## Important Modules

### expo-iap

- File: `src/context/purchases-context.tsx`
- Wraps `useIAP` hook and checks subscription status **on app startup**
- Product SKUs: weekly (`weekly_premium`) and yearly (`yearly_premium`)
- Paywall: `app/paywall.tsx`
- Exposes `usePurchases()` → `{ isPremium, loading, premiumExpiryDate, premiumProductId, refreshPremiumStatus }`
- `refreshPremiumStatus()` must be called after a successful purchase
- `drainPendingTransactions()` runs on startup to acknowledge stuck transactions
- Use `getAvailablePurchases()` for restore purchases flow
- Always call `finishTransaction` after a successful purchase

#### PurchasesProvider Implementation (REQUIRED)

Create `src/context/purchases-context.tsx`:

```tsx
import { finishTransaction, getAvailablePurchases, useIAP } from "expo-iap";
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

// Replace these SKUs with the app's actual product IDs
const SUBSCRIPTION_SKUS = [
  "com.company.appname.monthly",
  "com.company.appname.yearly",
];

interface PurchasesContextValue {
  isPremium: boolean;
  loading: boolean;
  premiumExpiryDate: Date | null;
  premiumProductId: string | null;
  refreshPremiumStatus: () => Promise<void>;
}

const PurchasesContext = createContext<PurchasesContextValue>({
  isPremium: false,
  loading: true,
  premiumExpiryDate: null,
  premiumProductId: null,
  refreshPremiumStatus: async () => {},
});

export function PurchasesProvider({ children }: { children: React.ReactNode }) {
  const { hasActiveSubscriptions } = useIAP();
  const [isPremium, setIsPremium] = useState(false);
  const [loading, setLoading] = useState(true);
  const [premiumExpiryDate, setPremiumExpiryDate] = useState<Date | null>(null);
  const [premiumProductId, setPremiumProductId] = useState<string | null>(null);

  /** Acknowledge any transactions left unfinished (e.g. app killed mid-purchase). */
  const drainPendingTransactions = async () => {
    try {
      const purchases = await getAvailablePurchases();
      for (const purchase of purchases) {
        try {
          await finishTransaction({ purchase, isConsumable: false });
        } catch {
          // already acknowledged — safe to ignore
        }
      }
    } catch {
      // IAP unavailable (simulator, no network, etc.)
    }
  };

  const refreshPremiumStatus = useCallback(async () => {
    try {
      await drainPendingTransactions();
      const hasPremium = await hasActiveSubscriptions(SUBSCRIPTION_SKUS);
      setIsPremium(hasPremium);

      if (hasPremium) {
        // Find the active subscription with the latest expiry date
        const purchases = await getAvailablePurchases();
        const activeSubs = purchases.filter((p) =>
          SUBSCRIPTION_SKUS.includes(p.productId),
        );
        // Pick the one with the furthest expiry (expirationDateIOS is ms epoch, iOS only)
        let bestExpiry: Date | null = null;
        let bestProductId: string | null = null;
        for (const p of activeSubs) {
          const expMs = (p as { expirationDateIOS?: number | null })
            .expirationDateIOS;
          if (expMs) {
            const d = new Date(expMs);
            if (!bestExpiry || d > bestExpiry) {
              bestExpiry = d;
              bestProductId = p.productId;
            }
          } else if (!bestProductId) {
            // Android: no expirationDate field – record productId at least
            bestProductId = p.productId;
          }
        }
        setPremiumExpiryDate(bestExpiry);
        setPremiumProductId(bestProductId);
      } else {
        setPremiumExpiryDate(null);
        setPremiumProductId(null);
      }
    } catch (error) {
      console.error("Failed to check subscription status:", error);
    } finally {
      setLoading(false);
    }
  }, [hasActiveSubscriptions]);

  // ✅ App açıldığında otomatik olarak satın alma durumu kontrol edilir
  useEffect(() => {
    refreshPremiumStatus();
  }, [refreshPremiumStatus]);

  return (
    <PurchasesContext.Provider
      value={{
        isPremium,
        loading,
        premiumExpiryDate,
        premiumProductId,
        refreshPremiumStatus,
      }}
    >
      {children}
    </PurchasesContext.Provider>
  );
}

export function usePurchases() {
  return useContext(PurchasesContext);
}
```

> **Notes:**
>
> - `drainPendingTransactions` acknowledges unfinished transactions on startup (prevents stuck purchases)
> - `premiumExpiryDate` is iOS only (`expirationDateIOS`); Android doesn't expose this field
> - `premiumProductId` lets you know which plan (monthly/yearly) is active
> - Replace `SUBSCRIPTION_SKUS` with the app's actual App Store / Play Store product IDs

After a successful purchase in `paywall.tsx`, always call `refreshPremiumStatus()`:

```tsx
const { refreshPremiumStatus } = usePurchases();

// In onPurchaseSuccess callback:
await finishTransaction({ purchase, isConsumable: false });
await refreshPremiumStatus(); // Update global premium state
router.replace("/(tabs)");
```

### AdMob

- File: `src/context/ads-context.tsx`
- Manages all 5 ad formats: App Open, Banner, Native, Interstitial, Rewarded
- App Open fires on foreground return with 4-hour cooldown (skipped on first cold launch)
- Interstitial: 3-minute cooldown, max 3/day — enforced automatically via `localStorage`
- Rewarded: resolves `Promise<boolean>` — `true` if user earned the reward
- All ads hidden for premium users via `shouldShowAds = !isPremium`
- Always use `TestIds.*` in `__DEV__` to avoid policy violations
- `AdsProvider` must be nested **inside** `PurchasesProvider` in `_layout.tsx`

### ATT / Tracking Transparency (iOS Only)

- File: `src/app/att-permission.tsx`
- **iOS only** — skipped entirely on Android
- Must be shown **before onboarding**, on first launch
- Uses `requestTrackingPermissionsAsync` from `expo-tracking-transparency`
- Required by Apple for AdMob personalized ads on iOS 14.5+
- App will be **rejected by App Store** without this

#### app.json Configuration (REQUIRED)

```json
{
  "expo": {
    "plugins": [
      [
        "expo-tracking-transparency",
        {
          "userTrackingPermission": "This identifier will be used to deliver personalized ads to you."
        }
      ]
    ]
  }
}
```

#### ATT Screen Implementation (REQUIRED)

Create `src/app/att-permission.tsx` — a full-screen custom UI that explains tracking **before** triggering the system dialog:

```tsx
import { useEffect } from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Platform,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { router } from "expo-router";
import { requestTrackingPermissionsAsync } from "expo-tracking-transparency";
import { LinearGradient } from "expo-linear-gradient";
import { useTranslation } from "react-i18next";
import "expo-sqlite/localStorage/install";

// Redirect Android away immediately (this screen is iOS only)
export function unstable_settings() {
  return {};
}

export default function ATTPermissionScreen() {
  const { t } = useTranslation();

  useEffect(() => {
    // Safety: if somehow opened on Android, redirect
    if (Platform.OS !== "ios") {
      router.replace("/onboarding");
    }
  }, []);

  const handleAllow = async () => {
    await requestTrackingPermissionsAsync(); // Triggers iOS system dialog
    globalThis.localStorage.setItem("att_shown", "true");
    router.replace("/onboarding");
  };

  const handleSkip = async () => {
    globalThis.localStorage.setItem("att_shown", "true");
    router.replace("/onboarding");
  };

  return (
    <LinearGradient
      colors={["#0F0F1A", "#1A1A2E", "#16213E"]}
      style={styles.container}
    >
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.content}>
          {/* Icon */}
          <View style={styles.iconContainer}>
            <Text style={styles.icon}>🔒</Text>
          </View>

          {/* Title */}
          <Text style={styles.title}>{t("att.title")}</Text>

          {/* Description */}
          <Text style={styles.description}>{t("att.description")}</Text>

          {/* Benefits list */}
          <View style={styles.benefitsList}>
            <BenefitItem icon="🎯" text={t("att.benefit1")} />
            <BenefitItem icon="🛡️" text={t("att.benefit2")} />
            <BenefitItem icon="🚫" text={t("att.benefit3")} />
          </View>

          {/* Privacy note */}
          <Text style={styles.privacyNote}>{t("att.privacyNote")}</Text>
        </View>

        {/* Buttons */}
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.allowButton} onPress={handleAllow}>
            <Text style={styles.allowButtonText}>{t("att.allow")}</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.skipButton} onPress={handleSkip}>
            <Text style={styles.skipButtonText}>{t("att.skip")}</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
}

function BenefitItem({ icon, text }: { icon: string; text: string }) {
  return (
    <View style={styles.benefitItem}>
      <Text style={styles.benefitIcon}>{icon}</Text>
      <Text style={styles.benefitText}>{text}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
    justifyContent: "space-between",
  },
  content: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 32,
  },
  iconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: "rgba(255,255,255,0.1)",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 32,
  },
  icon: {
    fontSize: 48,
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    color: "#FFFFFF",
    textAlign: "center",
    marginBottom: 16,
  },
  description: {
    fontSize: 16,
    color: "rgba(255,255,255,0.75)",
    textAlign: "center",
    marginBottom: 32,
    paddingVertical: 4,
  },
  benefitsList: {
    width: "100%",
    gap: 12,
    marginBottom: 24,
  },
  benefitItem: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(255,255,255,0.08)",
    borderRadius: 12,
    padding: 14,
    gap: 12,
  },
  benefitIcon: {
    fontSize: 22,
  },
  benefitText: {
    flex: 1,
    fontSize: 14,
    color: "rgba(255,255,255,0.85)",
  },
  privacyNote: {
    fontSize: 12,
    color: "rgba(255,255,255,0.45)",
    textAlign: "center",
  },
  buttonContainer: {
    padding: 24,
    gap: 12,
  },
  allowButton: {
    backgroundColor: "#6C63FF",
    borderRadius: 16,
    padding: 18,
    alignItems: "center",
  },
  allowButtonText: {
    color: "#FFFFFF",
    fontSize: 17,
    fontWeight: "700",
  },
  skipButton: {
    alignItems: "center",
    padding: 12,
  },
  skipButtonText: {
    color: "rgba(255,255,255,0.5)",
    fontSize: 15,
  },
});
```

#### ATT Localization Keys (add to tr.json and en.json)

`en.json`:

```json
"att": {
  "title": "Help Us Improve Your Experience",
  "description": "We use your data to show you relevant ads and improve app performance. Your privacy is important to us.",
  "benefit1": "See ads that are relevant to you",
  "benefit2": "Your data is never sold to third parties",
  "benefit3": "You can change this anytime in Settings",
  "privacyNote": "Tapping \"Allow\" will show Apple's permission dialog.",
  "allow": "Allow Tracking",
  "skip": "No Thanks"
}
```

`tr.json`:

```json
"att": {
  "title": "Deneyiminizi Geliştirmemize Yardım Edin",
  "description": "Verilerinizi size uygun reklamlar göstermek ve uygulama performansını artırmak için kullanıyoruz. Gizliliğiniz bizim için önemlidir.",
  "benefit1": "Size ilgili reklamlar görün",
  "benefit2": "Verileriniz asla üçüncü taraflara satılmaz",
  "benefit3": "Bunu Ayarlar'dan istediğiniz zaman değiştirebilirsiniz",
  "privacyNote": "\"İzin Ver\" tuşuna basınca Apple'ın izin diyaloğu görünecektir.",
  "allow": "Takibe İzin Ver",
  "skip": "Hayır, Teşekkürler"
}
```

### Notifications

- Files: `src/lib/notifications.ts`, `src/hooks/use-notifications.ts`
- iOS requires push notification entitlement

### App Flow (CRITICAL — ALWAYS FOLLOW THIS ORDER)

```
iOS:     ATT Permission → Onboarding → Paywall → Main App (tabs)
Android:               Onboarding → Paywall → Main App (tabs)
```

- ATT screen is **iOS only** — Android skips it entirely
- ATT screen shows once; result is stored in `localStorage` (`att_shown`)
- After ATT (grant or deny), navigate to onboarding
- After onboarding completes, navigate to paywall
- After paywall (purchase or skip), navigate to main app

```tsx
// In att-permission.tsx - after permission result:
const handleContinue = async () => {
  await requestTrackingPermissionsAsync(); // request system dialog
  globalThis.localStorage.setItem("att_shown", "true");
  router.replace("/onboarding");
};
```

```tsx
// In onboarding.tsx - when user completes onboarding:
const handleComplete = async () => {
  await setOnboardingCompleted(true);
  router.replace("/paywall"); // Navigate to paywall immediately
};
```

```tsx
// In paywall.tsx - after purchase or skip:
const handleContinue = () => {
  router.replace("/(tabs)"); // Navigate to main app
};
```

#### \_layout.tsx Routing Logic (iOS ATT check)

In the root `_layout.tsx`, determine the initial route on app start:

```tsx
import { Platform } from "react-native";
import { useEffect } from "react";
import { router } from "expo-router";
import { useOnboarding } from "@/context/onboarding-context";
import "expo-sqlite/localStorage/install";

export default function RootLayout() {
  const { hasCompletedOnboarding } = useOnboarding();

  useEffect(() => {
    if (hasCompletedOnboarding === null) return; // still loading

    if (hasCompletedOnboarding) {
      router.replace("/(tabs)");
      return;
    }

    // Show ATT only on iOS and only once
    const attShown = globalThis.localStorage.getItem("att_shown");
    if (Platform.OS === "ios" && !attShown) {
      router.replace("/att-permission");
    } else {
      router.replace("/onboarding");
    }
  }, [hasCompletedOnboarding]);

  return <Stack screenOptions={{ headerShown: false }} />;
}
```

### Paywall Screen Implementation (REQUIRED)

Full implementation of `src/app/paywall.tsx`:

```tsx
import { usePurchases } from "@/context/purchases-context";
import { MaterialIcons } from "@expo/vector-icons";
import type { Purchase } from "expo-iap";
import { useIAP } from "expo-iap";
import { LinearGradient } from "expo-linear-gradient";
import { router } from "expo-router";
import * as WebBrowser from "expo-web-browser";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  ActivityIndicator,
  Alert,
  Platform,
  Pressable,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

// Replace with actual product IDs
const SKUS = {
  monthly: "com.company.appname.monthly",
  yearly: "com.company.appname.yearly",
};

// Replace with actual URLs
const TERMS_URL = "https://example.com/terms.html";
const PRIVACY_URL = "https://example.com/privacy.html";

interface Feature {
  key: string;
  icon: keyof typeof MaterialIcons.glyphMap;
}

const FEATURES: Feature[] = [
  { key: "paywall.feature1", icon: "block" },
  { key: "paywall.feature2", icon: "notifications-active" },
  { key: "paywall.feature3", icon: "cloud-off" },
];

export default function PaywallScreen() {
  const { t } = useTranslation();
  const { refreshPremiumStatus, isPremium } = usePurchases();

  const [selectedPlan, setSelectedPlan] = useState<"monthly" | "yearly">(
    "yearly",
  );
  const [purchasing, setPurchasing] = useState(false);
  const [restoring, setRestoring] = useState(false);

  const {
    connected,
    subscriptions,
    fetchProducts,
    requestPurchase,
    finishTransaction,
    restorePurchases,
  } = useIAP({
    onPurchaseSuccess: async (purchase: Purchase) => {
      try {
        await finishTransaction({ purchase, isConsumable: false });
        await refreshPremiumStatus();
        router.replace("/(tabs)");
      } catch (err) {
        console.error("Finish transaction error:", err);
      } finally {
        setPurchasing(false);
      }
    },
    onPurchaseError: (error) => {
      setPurchasing(false);
      if ((error as any)?.code !== "E_USER_CANCELLED") {
        Alert.alert("Error", t("errors.purchaseFailed"));
      }
    },
  });

  useEffect(() => {
    if (connected) {
      fetchProducts({ skus: [SKUS.monthly, SKUS.yearly], type: "subs" });
    }
  }, [connected]);

  const handleClose = () => {
    if (router.canGoBack()) {
      router.back();
    } else {
      router.replace("/(tabs)");
    }
  };

  const handleSubscribe = async () => {
    if (purchasing) return;
    setPurchasing(true);
    try {
      const sku = selectedPlan === "monthly" ? SKUS.monthly : SKUS.yearly;
      await requestPurchase(
        Platform.OS === "ios"
          ? { request: { apple: { sku } }, type: "subs" }
          : { request: { google: { skus: [sku] } }, type: "subs" },
      );
    } catch {
      setPurchasing(false);
    }
  };

  const handleRestore = async () => {
    if (restoring) return;
    setRestoring(true);
    try {
      await restorePurchases();
      await refreshPremiumStatus();
      if (isPremium) {
        router.replace("/(tabs)");
      } else {
        Alert.alert("", t("errors.noActivePurchases"));
      }
    } catch {
      Alert.alert("Error", t("errors.restoreFailed"));
    } finally {
      setRestoring(false);
    }
  };

  const monthlyProduct = subscriptions?.find((p) => p.id === SKUS.monthly);
  const yearlyProduct = subscriptions?.find((p) => p.id === SKUS.yearly);

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" />
      <LinearGradient
        colors={["#0A0F1E", "#111827", "#0F172A"]}
        style={StyleSheet.absoluteFill}
      />

      <SafeAreaView style={styles.safeArea}>
        {/* Top bar — close button */}
        <View style={styles.topBar}>
          <TouchableOpacity
            onPress={handleClose}
            testID="close-button"
            style={styles.closeButton}
          >
            <MaterialIcons
              name="close"
              size={18}
              color="rgba(255,255,255,0.7)"
            />
          </TouchableOpacity>
        </View>

        {/* Scrollable content */}
        <ScrollView
          contentContainerStyle={styles.scroll}
          showsVerticalScrollIndicator={false}
          bounces={false}
        >
          {/* Hero icon */}
          <View style={styles.heroWrap}>
            <LinearGradient
              colors={["#2563EB", "#1D4ED8"]}
              style={styles.heroGradient}
            >
              <MaterialIcons name="workspace-premium" size={40} color="#fff" />
            </LinearGradient>
            <View style={styles.heroBadge}>
              <MaterialIcons name="verified" size={14} color="#34D399" />
            </View>
          </View>

          <Text style={styles.title}>{t("paywall.title")}</Text>
          <Text style={styles.subtitle}>{t("paywall.subtitle")}</Text>

          {/* Features */}
          <View style={styles.featuresCard}>
            {FEATURES.map(({ key, icon }, i) => (
              <View key={key}>
                <View style={styles.featureRow}>
                  <View style={styles.featureIconWrap}>
                    <MaterialIcons name={icon} size={18} color="#60A5FA" />
                  </View>
                  <Text style={styles.featureText}>{t(key)}</Text>
                  <MaterialIcons name="check" size={16} color="#34D399" />
                </View>
                {i < FEATURES.length - 1 && <View style={styles.separator} />}
              </View>
            ))}
          </View>

          {/* Plan selector — side by side */}
          <View style={styles.plansRow}>
            {/* Monthly */}
            <TouchableOpacity
              onPress={() => setSelectedPlan("monthly")}
              style={[
                styles.planCard,
                selectedPlan === "monthly"
                  ? styles.planCardSelected
                  : styles.planCardIdle,
              ]}
            >
              {selectedPlan === "monthly" && <View style={styles.planDot} />}
              <Text style={styles.planLabel}>{t("paywall.monthly")}</Text>
              <Text style={styles.planPrice}>
                {monthlyProduct?.displayPrice ?? t("paywall.monthlyPrice")}
              </Text>
            </TouchableOpacity>

            {/* Yearly */}
            <View style={styles.planCardWrap}>
              <View style={styles.badgeWrap}>
                <Text style={styles.badgeText}>{t("paywall.yearlyBadge")}</Text>
              </View>
              <TouchableOpacity
                onPress={() => setSelectedPlan("yearly")}
                style={[
                  styles.planCard,
                  selectedPlan === "yearly"
                    ? styles.planCardSelected
                    : styles.planCardIdle,
                ]}
              >
                {selectedPlan === "yearly" && <View style={styles.planDot} />}
                <Text style={styles.planLabel}>{t("paywall.yearly")}</Text>
                <Text style={styles.planPrice}>
                  {yearlyProduct?.displayPrice ?? t("paywall.yearlyPrice")}
                </Text>
                <Text style={styles.planPerWeek}>
                  {t("paywall.yearlyPerWeek")}
                </Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>

        {/* Sticky bottom CTA */}
        <View style={styles.footer} className="px-6 pb-4 pt-3">
          {/* Gradient subscribe button — kept as Pressable for custom gradient */}
          <Pressable
            onPress={handleSubscribe}
            disabled={purchasing}
            style={styles.subscribeTouchable}
          >
            <LinearGradient
              colors={
                purchasing ? ["#374151", "#374151"] : ["#2563EB", "#1D4ED8"]
              }
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 0 }}
              style={styles.subscribeButton}
            >
              {purchasing ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text className="text-white text-lg font-bold tracking-wide">
                  {t("paywall.subscribe")}
                </Text>
              )}
            </LinearGradient>
          </Pressable>

          <Text style={styles.autoRenewText}>{t("paywall.autoRenew")}</Text>

          <View style={styles.linksRow}>
            <TouchableOpacity onPress={handleRestore} disabled={restoring}>
              {restoring ? (
                <ActivityIndicator size="small" color="rgba(255,255,255,0.4)" />
              ) : (
                <Text style={styles.linkText}>{t("paywall.restore")}</Text>
              )}
            </TouchableOpacity>
            <Text style={styles.linkDot}>·</Text>
            <TouchableOpacity
              onPress={() => WebBrowser.openBrowserAsync(TERMS_URL)}
            >
              <Text style={styles.linkText}>{t("paywall.terms")}</Text>
            </TouchableOpacity>
            <Text style={styles.linkDot}>·</Text>
            <TouchableOpacity
              onPress={() => WebBrowser.openBrowserAsync(PRIVACY_URL)}
            >
              <Text style={styles.linkText}>{t("paywall.privacy")}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </SafeAreaView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  safeArea: { flex: 1 },
  topBar: {
    flexDirection: "row",
    justifyContent: "flex-end",
    paddingHorizontal: 16,
    paddingTop: 8,
    paddingBottom: 4,
  },
  closeButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: "rgba(255,255,255,0.1)",
    alignItems: "center",
    justifyContent: "center",
  },
  scroll: {
    paddingHorizontal: 24,
    paddingBottom: 24,
    alignItems: "center",
  },
  featuresCard: {
    width: "100%",
    backgroundColor: "rgba(255,255,255,0.05)",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.08)",
    borderRadius: 14,
    marginBottom: 20,
    overflow: "hidden",
  },
  featureRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  featureIconWrap: {
    width: 32,
    height: 32,
    borderRadius: 8,
    backgroundColor: "rgba(37,99,235,0.2)",
    alignItems: "center",
    justifyContent: "center",
  },
  featureText: {
    flex: 1,
    color: "rgba(255,255,255,0.85)",
    fontSize: 14,
    fontWeight: "500",
  },
  separator: {
    height: StyleSheet.hairlineWidth,
    backgroundColor: "rgba(255,255,255,0.08)",
    marginHorizontal: 16,
  },
  plansRow: {
    flexDirection: "row",
    width: "100%",
    gap: 12,
  },
  planCardWrap: {
    flex: 1,
    position: "relative",
    marginTop: 12,
  },
  badgeWrap: {
    position: "absolute",
    top: -12,
    alignSelf: "center",
    backgroundColor: "#F59E0B",
    borderRadius: 10,
    paddingHorizontal: 10,
    paddingVertical: 3,
    zIndex: 1,
  },
  badgeText: {
    color: "#000",
    fontSize: 11,
    fontWeight: "800",
  },
  planCard: {
    flex: 1,
    alignItems: "center",
    paddingVertical: 16,
    paddingHorizontal: 8,
    borderRadius: 12,
  },
  planCardSelected: {
    borderWidth: 2,
    borderColor: "#2563EB",
    backgroundColor: "rgba(37,99,235,0.12)",
  },
  planCardIdle: {
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.12)",
    backgroundColor: "rgba(255,255,255,0.04)",
  },
  planDot: {
    position: "absolute",
    top: 8,
    right: 8,
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: "#2563EB",
  },
  planLabel: {
    color: "rgba(255,255,255,0.55)",
    fontSize: 11,
    fontWeight: "600",
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  planPrice: {
    color: "#FFFFFF",
    fontSize: 15,
    fontWeight: "700",
    textAlign: "center",
  },
  planPerWeek: {
    color: "rgba(255,255,255,0.4)",
    fontSize: 11,
    textAlign: "center",
  },
  footer: {
    borderTopWidth: StyleSheet.hairlineWidth,
    borderTopColor: "rgba(255,255,255,0.07)",
  },
  subscribeTouchable: {
    borderRadius: 14,
    overflow: "hidden",
    marginBottom: 10,
  },
  subscribeButton: {
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 16,
  },
  autoRenewText: {
    color: "rgba(255,255,255,0.3)",
    fontSize: 11,
    textAlign: "center",
    marginBottom: 10,
  },
  linksRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    gap: 6,
  },
  linkText: {
    color: "rgba(255,255,255,0.4)",
    fontSize: 13,
  },
  linkDot: {
    color: "rgba(255,255,255,0.2)",
    fontSize: 14,
  },
});
```

> **Notes:**
>
> - Replace `SKUS` with the app's actual App Store / Play Store product IDs
> - Replace `TERMS_URL` and `PRIVACY_URL` with actual links
> - Default selected plan is **yearly** — adjust `FEATURES` array per app
> - `displayPrice` from `subscriptions` shows the real localized price; fallback strings are used while products load
> - Add i18n keys: `paywall.title`, `paywall.subtitle`, `paywall.monthly`, `paywall.yearly`, `paywall.monthlyPrice`, `paywall.yearlyPrice`, `paywall.yearlyBadge`, `paywall.yearlyPerWeek`, `paywall.subscribe`, `paywall.autoRenew`, `paywall.restore`, `paywall.terms`, `paywall.privacy`, `paywall.feature1-3`, `errors.purchaseFailed`, `errors.noActivePurchases`, `errors.restoreFailed`

### Settings Screen Options (REQUIRED)

Settings screen MUST include:

1. **Language** - Change app language
2. **Theme** - Light/Dark/System
3. **Notifications** - Enable/disable notifications
4. **Remove Ads** - Navigate to paywall (hidden if already premium)
5. **Reset Onboarding** - Restart onboarding flow (for testing/demo)

```tsx
import { usePurchases } from "@/context/purchases-context";

const { isPremium } = usePurchases(); // Global premium state (checked on app startup)

// Remove Ads - navigates to paywall
const handleRemoveAds = () => {
  router.push("/paywall");
};

// Reset onboarding
const handleResetOnboarding = async () => {
  await setOnboardingCompleted(false);
  router.replace("/onboarding");
};

// In settings list:
{
  !isPremium && (
    <SettingsItem
      title={t("settings.removeAds")}
      icon="crown.fill"
      onPress={handleRemoveAds}
    />
  );
}

<SettingsItem
  title={t("settings.resetOnboarding")}
  icon="arrow.counterclockwise"
  onPress={handleResetOnboarding}
/>;
```

## Localization

- File: `lib/i18n.ts`
- Languages stored in `locales/`
- App restarts on language change

## Coding Standards

- Use functional components
- Strict TypeScript
- Avoid hardcoded strings
- Use padding instead of lineHeight
- Use memoization when necessary

## Context Providers

```tsx
<GestureHandlerRootView style={{ flex: 1 }}>
  <ThemeProvider>
    <OnboardingProvider>
      <PurchasesProvider>
        {/* ✅ App açılışında isPremium kontrol eder */}
        <AdsProvider>
          {/* AdsProvider, isPremium'u PurchasesProvider'dan okur */}
          <Stack />
        </AdsProvider>
      </PurchasesProvider>
    </OnboardingProvider>
  </ThemeProvider>
</GestureHandlerRootView>
```

## useColorScheme Hook

File: `src/hooks/use-color-scheme.ts`

```tsx
import { useThemeContext } from "@/context/theme-context";

export function useColorScheme(): "light" | "dark" | "unspecified" {
  const { isDark } = useThemeContext();
  return isDark ? "dark" : "light";
}
```

## Important Notes

1. iOS permissions are defined in `app.json`
2. Android permissions are defined in `app.json`
3. Enable new architecture via `newArchEnabled: true`
4. Enable typed routes via `experiments.typedRoutes`

## App Store & Play Store Notes

- iOS ATT permission required
- Restore purchases must work correctly
- Target SDK must be up to date

---

## Authentication (OIDC — Optional)

> **Only implement this section if the user answered YES to "Does the app need login/authentication?"**

This project uses **OpenID Connect (OIDC)** with OAuth 2.0 Authorization Code Flow + PKCE.

### Architecture

```
UI (useIntegratedAuth hook)
        │
        ├── authStore (Zustand) ── SecureStore (tokens)
        │       │
        │       └── Identity Server (OIDC)
        │               ├── /authorize
        │               ├── /token
        │               └── /userinfo
        │
        └── services/identity/ ── Authenticated Axios instance
```

### Install Auth Libraries

```bash
npx expo install expo-auth-session expo-secure-store expo-web-browser
bunx expo install zustand @tanstack/react-query
```

### Environment Variables (`.env`)

```env
EXPO_PUBLIC_IDENTITY_SERVER_AUTHORITY=https://identity.appaflytech.com
EXPO_PUBLIC_OIDC_CLIENT_ID=wap-mobile-app
EXPO_PUBLIC_APP_SCHEME=anatoli
EXPO_PUBLIC_APP=anatoli
```

### `app.json` — Scheme (REQUIRED for redirect URI)

```json
{
  "expo": {
    "scheme": "anatoli"
  }
}
```

### `src/utils/constants.ts`

```typescript
export const AppConfig = {
  identityServerAuthority:
    process.env.EXPO_PUBLIC_IDENTITY_SERVER_AUTHORITY ||
    "https://identity.appaflytech.com",
  oidcClientId: process.env.EXPO_PUBLIC_OIDC_CLIENT_ID || "wap-mobile-app",
  appScheme: process.env.EXPO_PUBLIC_APP_SCHEME || "anatoli",
  app: process.env.EXPO_PUBLIC_APP || "anatoli",
};
```

### `src/store/authStore.ts`

```typescript
import * as AuthSession from "expo-auth-session";
import * as SecureStore from "expo-secure-store";
import * as WebBrowser from "expo-web-browser";
import { create } from "zustand";
import { AppConfig } from "@/utils/constants";

WebBrowser.maybeCompleteAuthSession();

export const OIDC_CONFIG = {
  issuer: AppConfig.identityServerAuthority,
  clientId: AppConfig.oidcClientId,
  scopes: ["openid", "profile", "offline_access"],
};

const STORAGE_KEY = "auth_tokens";
const redirectUri = AuthSession.makeRedirectUri({
  scheme: AppConfig.appScheme,
});

type TokenResponse = {
  access_token: string;
  refresh_token?: string;
  expires_in?: number;
  id_token?: string;
  token_type?: string;
  issued_at?: number;
};

type UserModel = {
  sub: string;
  name?: string;
  given_name?: string;
  family_name?: string;
  preferred_username?: string;
  picture?: string;
  email?: string;
  email_verified?: boolean;
};

type AuthState = {
  tokens: TokenResponse | null;
  user: UserModel | null;
  discovery: AuthSession.DiscoveryDocument | null;
  ready: boolean;
  isLoggingIn: boolean;

  init: () => Promise<void>;
  login: () => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<TokenResponse>;
  loadUserInfo: () => Promise<void>;
  getValidAccessToken: () => Promise<string | null>;
  isAuthenticated: () => boolean;
};

export const useAuthStore = create<AuthState>((set, get) => ({
  tokens: null,
  user: null,
  discovery: null,
  ready: false,
  isLoggingIn: false,

  init: async () => {
    try {
      // Load discovery document
      const discovery = await AuthSession.fetchDiscoveryAsync(
        OIDC_CONFIG.issuer,
      );
      set({ discovery });

      // Restore saved tokens
      const raw = await SecureStore.getItemAsync(STORAGE_KEY);
      if (raw) {
        const tokens: TokenResponse = JSON.parse(raw);
        set({ tokens });
        await get().loadUserInfo();
      }
    } catch (e) {
      console.warn("Auth init error:", e);
    } finally {
      set({ ready: true });
    }
  },

  login: async () => {
    const { discovery } = get();
    if (!discovery) throw new Error("Discovery not loaded");

    set({ isLoggingIn: true });
    try {
      const request = new AuthSession.AuthRequest({
        clientId: OIDC_CONFIG.clientId,
        redirectUri,
        scopes: OIDC_CONFIG.scopes,
        responseType: AuthSession.ResponseType.Code,
        usePKCE: true,
      });

      const authUrl = await request.makeAuthUrlAsync(discovery);
      const authUrlFull = `${authUrl}&app=${AppConfig.app}&lang=tr`;

      const result = await WebBrowser.openAuthSessionAsync(
        authUrlFull,
        redirectUri,
        { preferEphemeralSession: true },
      );

      if (result.type !== "success") throw new Error("Login cancelled");

      const code = new URL(result.url).searchParams.get("code");
      if (!code) throw new Error("No code returned");

      const tokenResult = await AuthSession.exchangeCodeAsync(
        {
          code,
          clientId: OIDC_CONFIG.clientId,
          redirectUri,
          codeVerifier: request.codeVerifier!,
        },
        discovery,
      );

      const payload: TokenResponse = {
        access_token: tokenResult.accessToken,
        refresh_token: tokenResult.refreshToken ?? undefined,
        expires_in: tokenResult.expiresIn ?? undefined,
        id_token: tokenResult.idToken ?? undefined,
        issued_at: Math.floor(Date.now() / 1000),
      };

      await SecureStore.setItemAsync(STORAGE_KEY, JSON.stringify(payload));
      set({ tokens: payload });
      await get().loadUserInfo();
    } finally {
      set({ isLoggingIn: false });
    }
  },

  logout: async () => {
    const { tokens, discovery } = get();
    try {
      if (tokens?.id_token && discovery?.endSessionEndpoint) {
        const logoutUrl = `${discovery.endSessionEndpoint}?id_token_hint=${tokens.id_token}&post_logout_redirect_uri=${encodeURIComponent(redirectUri)}`;
        await WebBrowser.openAuthSessionAsync(logoutUrl, redirectUri, {
          preferEphemeralSession: true,
        });
      }
    } finally {
      await SecureStore.deleteItemAsync(STORAGE_KEY);
      set({ tokens: null, user: null });
    }
  },

  refresh: async () => {
    const { tokens, discovery } = get();
    if (!tokens?.refresh_token || !discovery) throw new Error("Cannot refresh");

    const result = await AuthSession.refreshAsync(
      { clientId: OIDC_CONFIG.clientId, refreshToken: tokens.refresh_token },
      discovery,
    );

    const payload: TokenResponse = {
      access_token: result.accessToken,
      refresh_token: result.refreshToken ?? tokens.refresh_token,
      expires_in: result.expiresIn ?? undefined,
      issued_at: Math.floor(Date.now() / 1000),
    };

    await SecureStore.setItemAsync(STORAGE_KEY, JSON.stringify(payload));
    set({ tokens: payload });
    return payload;
  },

  loadUserInfo: async () => {
    const { tokens, discovery } = get();
    if (!tokens?.access_token || !discovery?.userInfoEndpoint) return;

    const res = await fetch(discovery.userInfoEndpoint, {
      headers: { Authorization: `Bearer ${tokens.access_token}` },
    });
    const user: UserModel = await res.json();
    set({ user });
  },

  getValidAccessToken: async () => {
    const { tokens, refresh } = get();
    if (!tokens) return null;

    const isExpired = (() => {
      if (!tokens.expires_in || !tokens.issued_at) return false;
      return (
        Math.floor(Date.now() / 1000) >=
        tokens.issued_at + tokens.expires_in - 30
      );
    })();

    if (isExpired) {
      try {
        const refreshed = await refresh();
        return refreshed.access_token;
      } catch {
        set({ tokens: null, user: null });
        return null;
      }
    }
    return tokens.access_token;
  },

  isAuthenticated: () => {
    return !!get().tokens?.access_token;
  },
}));
```

### `src/store/useIntegratedAuth.ts`

```typescript
import { useEffect } from "react";
import { useAuthStore } from "./authStore";

export interface AppUser {
  id?: string;
  name?: string;
  surname?: string;
  email?: string;
  avatar?: string;
  isLoggedIn: boolean;
}

// Minimal app-level user state — wire into your own store/context as needed
let _appUser: AppUser = { isLoggedIn: false };
const _listeners = new Set<() => void>();

function setAppUser(u: AppUser) {
  _appUser = u;
  _listeners.forEach((l) => l());
}

export function useIntegratedAuth() {
  const authStore = useAuthStore();

  // Sync OIDC state → app user state
  useEffect(() => {
    if (!authStore.ready) return;

    const oidcLoggedIn = authStore.isAuthenticated();

    if (oidcLoggedIn && authStore.user && !_appUser.isLoggedIn) {
      setAppUser({
        id: authStore.user.sub,
        name: authStore.user.given_name || authStore.user.name,
        surname: authStore.user.family_name,
        email: authStore.user.email,
        avatar: authStore.user.picture,
        isLoggedIn: true,
      });
    } else if (!oidcLoggedIn && _appUser.isLoggedIn) {
      setAppUser({ isLoggedIn: false });
    }
  }, [authStore.ready, authStore.tokens, authStore.user]);

  const login = async () => {
    await authStore.login();
  };

  const logout = async () => {
    await authStore.logout();
    setAppUser({ isLoggedIn: false });
  };

  const getAccessToken = () => authStore.getValidAccessToken();

  return {
    isAuthenticated: authStore.isAuthenticated(),
    isLoggingIn: authStore.isLoggingIn,
    ready: authStore.ready,
    user: authStore.user,
    appUser: _appUser,
    login,
    logout,
    getAccessToken,
  };
}
```

### Initialize Auth in `_layout.tsx`

```tsx
import { useEffect } from "react";
import { useAuthStore } from "@/store/authStore";

export default function RootLayout() {
  const initAuth = useAuthStore((s) => s.init);

  useEffect(() => {
    initAuth(); // Load tokens + discovery on app start
  }, []);

  // ... rest of your layout
}
```

### Flow with Auth Enabled

```
iOS:     ATT → Onboarding → Paywall → Main App
Android:        Onboarding → Paywall → Main App

Login screen is accessible from Settings or any protected screen.
Authenticated state is checked via useIntegratedAuth().isAuthenticated.
```

### `src/app/auth/oidc-login.tsx` — Login Screen

```tsx
import {
  View,
  Text,
  TouchableOpacity,
  ActivityIndicator,
  StyleSheet,
} from "react-native";
import { useIntegratedAuth } from "@/store/useIntegratedAuth";

export default function OIDCLoginScreen() {
  const { login, isLoggingIn, ready } = useIntegratedAuth();

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Giriş Yap</Text>

      <TouchableOpacity
        style={[
          styles.button,
          (!ready || isLoggingIn) && styles.buttonDisabled,
        ]}
        onPress={login}
        disabled={!ready || isLoggingIn}
      >
        {isLoggingIn ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.buttonText}>Hesabınla Giriş Yap</Text>
        )}
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 32,
  },
  title: { fontSize: 28, fontWeight: "700", marginBottom: 40 },
  button: {
    backgroundColor: "#6C63FF",
    borderRadius: 16,
    padding: 18,
    width: "100%",
    alignItems: "center",
  },
  buttonDisabled: { opacity: 0.5 },
  buttonText: { color: "#fff", fontSize: 17, fontWeight: "700" },
});
```

### `src/services/identity/index.ts` — Authenticated Axios

```typescript
import axios from "axios";
import { AppConfig } from "@/utils/constants";
import { useAuthStore } from "@/store/authStore";

export const identityAxios = axios.create({
  baseURL: AppConfig.identityServerAuthority,
});

identityAxios.interceptors.request.use(async (config) => {
  const token = await useAuthStore.getState().getValidAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### Auth Usage Examples

```tsx
// Check auth state
import { useIntegratedAuth } from "@/store/useIntegratedAuth";

function ProfileScreen() {
  const { isAuthenticated, user, logout } = useIntegratedAuth();

  if (!isAuthenticated) return <LoginPrompt />;

  return (
    <View>
      <Text>Hoş geldin, {user?.given_name}!</Text>
      <Button title="Çıkış Yap" onPress={logout} />
    </View>
  );
}
```

```typescript
// Authenticated API call
async function fetchProtectedData() {
  const token = await useAuthStore.getState().getValidAccessToken();
  if (!token) throw new Error("Not authenticated");

  const res = await fetch("https://api.appaflytech.com/data", {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.json();
}
```

### Security Features

| Feature                | Detail                                                   |
| ---------------------- | -------------------------------------------------------- |
| **PKCE**               | Authorization Code Flow with Proof Key for Code Exchange |
| **SecureStore**        | Tokens stored in iOS Keychain / Android Keystore         |
| **Ephemeral Session**  | WebBrowser doesn't share cookies; every login is fresh   |
| **Auto Token Refresh** | Token renewed 30s before expiry automatically            |
| **Token Cleanup**      | On refresh failure, tokens cleared and user logged out   |

---

## Maestro E2E Tests (ALWAYS GENERATE AFTER BUILDING SCREENS)

Maestro is an open-source mobile UI testing framework using YAML flow files. After building each screen, **automatically generate the corresponding Maestro flow**.

### Installation

```bash
curl -fsSL "https://get.maestro.mobile.dev" | bash
maestro --version   # requires Java 17+
```

### Project Structure

```
project-root/
└── .maestro/
    ├── 00_app_launch.yaml
    ├── 01_att_permission.yaml       # iOS only
    ├── 02_onboarding.yaml
    ├── 03_paywall_skip.yaml
    ├── 04_paywall_subscribe.yaml
    ├── 05_main_tabs.yaml
    ├── 06_settings.yaml
    └── 07_full_flow.yaml
```

### Run Tests

```bash
maestro test .maestro/02_onboarding.yaml   # single flow
maestro test .maestro/                     # all flows
```

### Key Commands

| Command                       | Description                    |
| ----------------------------- | ------------------------------ |
| `launchApp: clearState: true` | Fresh launch, clears all data  |
| `tapOn: "Text"`               | Tap by visible text            |
| `tapOn: {id: "testID"}`       | Tap by testID prop             |
| `assertVisible: "Text"`       | Assert element visible         |
| `assertNotVisible: "Text"`    | Assert element NOT visible     |
| `inputText: "value"`          | Type into focused input        |
| `swipe: {direction: LEFT}`    | Swipe gesture                  |
| `back`                        | Android back button            |
| `takeScreenshot: name`        | Capture screenshot             |
| `runFlow: path/to/flow.yaml`  | Reuse another flow             |
| `optional: true`              | Skip step if element not found |

---

### Flow Templates

Adapt `appId` and all text strings to the app's actual English i18n values.

#### 00 — App Launch

```yaml
# .maestro/00_app_launch.yaml
appId: com.company.appname
---
- launchApp:
    clearState: true
- takeScreenshot: app_launch
```

#### 01 — ATT Permission (iOS only)

```yaml
# .maestro/01_att_permission.yaml
appId: com.company.appname
---
- launchApp:
    clearState: true
- assertVisible: "Allow Tracking"
- takeScreenshot: att_screen
- tapOn: "Allow Tracking"
- tapOn:
    text: "Allow"
    optional: true
- takeScreenshot: att_after
```

#### 02 — Onboarding

```yaml
# .maestro/02_onboarding.yaml
appId: com.company.appname
---
- launchApp:
    clearState: true
# Dismiss ATT if present (iOS)
- tapOn:
    text: "Allow Tracking"
    optional: true
- tapOn:
    text: "Allow"
    optional: true
# Swipe through slides
- takeScreenshot: onboarding_slide_1
- swipe:
    direction: LEFT
    duration: 400
- takeScreenshot: onboarding_slide_2
- swipe:
    direction: LEFT
    duration: 400
- takeScreenshot: onboarding_slide_3
- swipe:
    direction: LEFT
    duration: 400
- takeScreenshot: onboarding_slide_4
- tapOn: "Get Started"
- takeScreenshot: onboarding_complete
```

#### 03 — Paywall Skip

```yaml
# .maestro/03_paywall_skip.yaml
appId: com.company.appname
---
- runFlow: 02_onboarding.yaml
- assertVisible: "Yearly"
- assertVisible: "Monthly"
- takeScreenshot: paywall_screen
- tapOn:
    id: "close-button"
    optional: true
- tapOn:
    text: "×"
    optional: true
- takeScreenshot: paywall_closed
```

#### 04 — Paywall Plan Selection

```yaml
# .maestro/04_paywall_subscribe.yaml
appId: com.company.appname
---
- runFlow: 02_onboarding.yaml
- tapOn: "Yearly"
- takeScreenshot: paywall_yearly_selected
- tapOn: "Monthly"
- takeScreenshot: paywall_monthly_selected
# Opens store sheet — cannot complete purchase in automated test
- tapOn: "Subscribe"
- takeScreenshot: paywall_subscribe_tapped
```

#### 05 — Main Tabs Navigation

```yaml
# .maestro/05_main_tabs.yaml
appId: com.company.appname
---
- runFlow: 02_onboarding.yaml
- runFlow: 03_paywall_skip.yaml
- takeScreenshot: main_home
- tapOn: "Settings"
- takeScreenshot: main_settings
- tapOn: "Home"
- takeScreenshot: main_home_again
```

#### 06 — Settings Screen

```yaml
# .maestro/06_settings.yaml
appId: com.company.appname
---
- runFlow: 02_onboarding.yaml
- runFlow: 03_paywall_skip.yaml
- tapOn: "Settings"
- assertVisible: "Language"
- assertVisible: "Theme"
- assertVisible: "Notifications"
- takeScreenshot: settings_screen
```

#### 07 — Full End-to-End Flow

```yaml
# .maestro/07_full_flow.yaml
appId: com.company.appname
---
- launchApp:
    clearState: true
- runFlow: 01_att_permission.yaml
- runFlow: 02_onboarding.yaml
- runFlow: 03_paywall_skip.yaml
- runFlow: 05_main_tabs.yaml
- runFlow: 06_settings.yaml
- takeScreenshot: full_flow_complete
```

### Notes

- `01_att_permission.yaml` — **iOS only**, skip on Android builds
- System dialogs use `optional: true` (vary by OS/device)
- Android: `- back` simulates hardware back button
- iOS simulator: `maestro --device booted test .maestro/`
- Use `runFlow` to chain — no duplicate setup steps

---

### GitHub Actions CI/CD (ALWAYS CREATE)

After generating `.maestro/` flows, you MUST also create the GitHub Actions workflow so tests run automatically on every push and pull request.

#### Project Structure (add these files)

```
project-root/
├── .github/
│   └── workflows/
│       ├── maestro-android.yml   # Android emulator tests (free, ubuntu)
│       └── maestro-ios.yml       # iOS simulator tests (macOS runner)
└── .maestro/
    └── ...
```

#### `.github/workflows/maestro-android.yml`

```yaml
name: Maestro E2E — Android

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  e2e-android:
    runs-on: ubuntu-latest
    timeout-minutes: 60

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Java 17
        uses: actions/setup-java@v4
        with:
          java-version: "17"
          distribution: "temurin"

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install dependencies
        run: npm install

      - name: Install Maestro
        run: |
          curl -fsSL "https://get.maestro.mobile.dev" | bash
          echo "$HOME/.maestro/bin" >> $GITHUB_PATH

      - name: Enable KVM (Android emulator acceleration)
        run: |
          echo 'KERNEL=="kvm", GROUP="kvm", MODE="0666", OPTIONS+="static_node=kvm"' | sudo tee /etc/udev/rules.d/99-kvm4all.rules
          sudo udevadm control --reload-rules
          sudo udevadm trigger --name-match=kvm

      - name: Expo Prebuild
        run: npx expo prebuild --platform android --non-interactive

      - name: Run Android E2E Tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          arch: x86_64
          profile: pixel_6
          avd-name: maestro_test
          emulator-options: -no-snapshot-save -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim
          disable-animations: true
          script: |
            cd android && ./gradlew assembleDebug --no-daemon && cd ..
            adb install -r android/app/build/outputs/apk/debug/app-debug.apk
            maestro test .maestro/ --format junit --output test-results.xml

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: maestro-android-results
          path: |
            test-results.xml
            ~/.maestro/tests/

      - name: Upload screenshots
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: maestro-android-screenshots
          path: ~/.maestro/tests/**/*.png
```

#### `.github/workflows/maestro-ios.yml`

```yaml
name: Maestro E2E — iOS

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  e2e-ios:
    runs-on: macos-15
    timeout-minutes: 90

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Java 17 (required by Maestro)
        uses: actions/setup-java@v4
        with:
          java-version: "17"
          distribution: "temurin"

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install dependencies
        run: npm install

      - name: Install Maestro
        run: |
          curl -fsSL "https://get.maestro.mobile.dev" | bash
          echo "$HOME/.maestro/bin" >> $GITHUB_PATH

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_16.2.app

      - name: Expo Prebuild
        run: npx expo prebuild --platform ios --non-interactive

      - name: Install CocoaPods dependencies
        run: cd ios && pod install

      - name: Boot iOS Simulator
        run: |
          UDID=$(xcrun simctl create "MaestroTest" "iPhone 16" "iOS-18-2")
          xcrun simctl boot $UDID
          echo "SIM_UDID=$UDID" >> $GITHUB_ENV

      - name: Build app for simulator
        run: |
          SCHEME=$(ls ios/*.xcworkspace | head -1 | xargs basename | sed 's/.xcworkspace//')
          xcodebuild \
            -workspace ios/$SCHEME.xcworkspace \
            -scheme $SCHEME \
            -configuration Debug \
            -sdk iphonesimulator \
            -derivedDataPath build \
            -quiet
          APP_PATH=$(find build -name "*.app" | head -1)
          xcrun simctl install ${{ env.SIM_UDID }} "$APP_PATH"

      - name: Run iOS E2E Tests
        run: maestro --device ${{ env.SIM_UDID }} test .maestro/ --format junit --output test-results.xml
        env:
          MAESTRO_DRIVER_STARTUP_TIMEOUT: "60000"

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: maestro-ios-results
          path: |
            test-results.xml
            ~/.maestro/tests/

      - name: Upload screenshots
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: maestro-ios-screenshots
          path: ~/.maestro/tests/**/*.png

      - name: Cleanup simulator
        if: always()
        run: xcrun simctl delete ${{ env.SIM_UDID }}
```

#### No GitHub Secrets Required

Both workflows build the app **locally on the CI runner** — no EAS account, no Maestro Cloud, no secrets needed.

**Android** uses Gradle directly:

```yaml
- name: Expo Prebuild
  run: npx expo prebuild --platform android --non-interactive
# Then inside android-emulator-runner script:
# cd android && ./gradlew assembleDebug --no-daemon
# adb install -r app/build/outputs/apk/debug/app-debug.apk
```

**iOS** uses `xcodebuild` directly:

```yaml
- name: Expo Prebuild
  run: npx expo prebuild --platform ios --non-interactive

- name: Install CocoaPods
  run: cd ios && pod install

- name: Build for simulator
  run: |
    SCHEME=$(ls ios/*.xcworkspace | head -1 | xargs basename | sed 's/.xcworkspace//')
    xcodebuild \
      -workspace ios/$SCHEME.xcworkspace \
      -scheme $SCHEME \
      -configuration Debug \
      -sdk iphonesimulator \
      -derivedDataPath build \
      -quiet
    APP_PATH=$(find build -name "*.app" | head -1)
    xcrun simctl install ${{ env.SIM_UDID }} "$APP_PATH"
```

The complete final workflows with local builds are provided above (`maestro-android.yml` / `maestro-ios.yml`). Replace the `# install APK` comment lines in those templates with the Gradle/xcodebuild steps shown here.

#### CI-Friendly Maestro Flow Tips

```yaml
# Use env variables for appId in CI
appId: ${APP_ID:-com.company.appname}
---
# Add retries for flaky steps
- tapOn:
    text: "Get Started"
    retryTapIfNoChange: true

# Increase timeouts for slow CI environments
- tapOn:
    text: "Subscribe"
    waitToSettleTimeoutMs: 5000

# Skip ATT on Android / CI
- runFlow:
    when:
      platform: iOS
    file: 01_att_permission.yaml
```

---

## Testing Checklist

- [ ] `maestro test .maestro/` — all flows pass on iOS and Android
- [ ] Login/logout flow (if auth enabled)
- [ ] UI tested in all languages (tr / en)
- [ ] Dark / Light mode
- [ ] Notifications
- [ ] Premium flow
- [ ] Restore purchases
- [ ] Offline support
- [ ] Multiple screen sizes

## After Development

```bash
npx expo prebuild --clean
bun ios
bun android
```

> NOTE: `prebuild --clean` recreates ios and android folders. Run it after modifying native modules or app.json.
