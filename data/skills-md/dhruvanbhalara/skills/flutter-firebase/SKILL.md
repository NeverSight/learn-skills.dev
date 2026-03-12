---
name: flutter-firebase
description: Firebase Auth, Firestore, FCM, Crashlytics & Analytics Patterns
metadata:
    platforms: "flutter, android, ios"
    languages: "dart"
    category: "backend"
---

# Firebase Setup

-   Use `firebase_core` for initialization — call `Firebase.initializeApp()` before `runApp()`
-   Use `flutterfire configure` for platform-specific setup
-   Use separate Firebase projects per flavor (see `app-config` skill)
-   Register Firebase services via `injectable` for consistent DI

# Authentication

-   Use `firebase_auth` for user management
-   Wrap all auth calls in an `AuthRepository` — no direct `FirebaseAuth` usage in BLoCs or UI
-   Support email/password, Google Sign-In, and Apple Sign-In at minimum
-   Handle auth state changes via `FirebaseAuth.instance.authStateChanges()` stream in `AuthBloc`
-   Store auth tokens via `flutter_secure_storage` — never in `SharedPreferences` or source code
-   Implement proper sign-out: clear local cache, navigate to login, dispose user-specific BLoCs

# Firestore

-   Use `cloud_firestore` for remote data persistence
-   DataSources wrap all Firestore calls (`get`, `set`, `update`, `delete`, `snapshots`)
-   Use typed model classes with `fromFirestore` / `toFirestore` factory methods
-   Prefer `.withConverter<T>()` for type-safe collection references
-   Use batch writes for multi-document operations — never multiple sequential writes
-   Implement offline persistence (enabled by default on mobile)

## Security Rules

-   NEVER rely on client-side validation alone — enforce rules in Firestore Security Rules
-   Default deny: start with `allow read, write: if false;` and open only what's needed
-   Always validate `request.auth != null` for authenticated-only collections
-   Test rules with the Firebase Emulator Suite before deploying

# Push Notifications (FCM)

-   Use `firebase_messaging` for push notifications
-   Request notification permissions early but gracefully (explain value before requesting)
-   Handle foreground, background, and terminated-state messages separately
-   Store FCM token in Firestore user document for server-side targeting
-   Re-register token on `onTokenRefresh` stream

# Crashlytics

-   Use `firebase_crashlytics` for crash reporting
-   Enable in staging and production flavors only — disable in dev
-   Record Flutter errors: `FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError`
-   Catch async errors via `PlatformDispatcher.instance.onError`
-   Add custom keys for user context: `Crashlytics.instance.setCustomKey('userId', id)`

# Analytics

-   Use `firebase_analytics` for user behavior tracking
-   Log meaningful events with descriptive names: `analytics.logEvent(name: 'purchase_completed')`
-   Set user properties for segmentation: `analytics.setUserProperty(name: 'plan', value: 'premium')`
-   Track screen views via `FirebaseAnalyticsObserver` in `GoRouter`
-   NEVER log PII (emails, passwords, phone numbers) in analytics events

# Remote Config

-   Use `firebase_remote_config` for feature flags and A/B testing
-   Set sensible defaults locally — app MUST work without Remote Config fetched
-   Fetch and activate on app start with a timeout fallback
-   Cache values and respect minimum fetch intervals to avoid throttling
