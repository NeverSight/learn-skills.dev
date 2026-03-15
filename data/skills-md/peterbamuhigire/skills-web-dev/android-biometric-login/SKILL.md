---
name: android-biometric-login
description: "Optional biometric (fingerprint/face) gate on Android app launch using AndroidX Biometric API. Covers BiometricHelper utility, splash screen integration, settings toggle with verification, EncryptedSharedPreferences storage, and graceful fallback. Use when adding biometric authentication to any Android app."
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Android Biometric Login

Add optional fingerprint/face authentication as a gate on app launch. Uses the AndroidX Biometric library (`BIOMETRIC_STRONG` — Class 3 biometrics only). The feature is opt-in: users enable it in Settings, and it triggers on every app launch from the splash screen.

## Overview

**Flow:** App launch → Splash → Check biometric pref → Show system biometric prompt → Success (Dashboard) or Failure (Login screen).

**Key principles:**
- **Optional, not mandatory** — users choose to enable via a Settings toggle
- **Verify before enabling** — require biometric auth to turn the feature ON (prevents unauthorized enabling)
- **Graceful degradation** — if device has no biometric hardware, hide the toggle entirely
- **Survive logout** — biometric preference persists across logout/re-login
- **No custom UI** — use the system `BiometricPrompt` dialog (consistent UX, handles retries)

## Dependencies

```toml
# libs.versions.toml
[versions]
biometric = "1.1.0"

[libraries]
biometric = { group = "androidx.biometric", name = "biometric", version.ref = "biometric" }
```

```kotlin
// build.gradle.kts
implementation(libs.biometric)
```

No manifest permissions needed — `BiometricPrompt` API on Android 10+ (minSdk 29) handles everything.

## Architecture

```
core/auth/
  BiometricHelper.kt    — Static utility: canAuthenticate() + authenticate()
  AuthManager.kt        — Stores biometric preference in EncryptedSharedPreferences

feature/splash/ui/
  SplashScreen.kt       — Checks pref + triggers prompt on app launch

feature/settings/ui/
  SettingsScreen.kt     — Toggle switch with verify-before-enable
  SettingsViewModel.kt  — Delegates to AuthManager
```

## Step 1: BiometricHelper Utility

A stateless `object` with two functions. No DI needed — takes `FragmentActivity` as parameter.

```kotlin
package com.example.app.core.auth

import androidx.biometric.BiometricManager
import androidx.biometric.BiometricPrompt
import androidx.core.content.ContextCompat
import androidx.fragment.app.FragmentActivity

object BiometricHelper {

    /**
     * Returns true if device has enrolled Class 3 biometrics (fingerprint or face).
     */
    fun canAuthenticate(activity: FragmentActivity): Boolean {
        val bm = BiometricManager.from(activity)
        return bm.canAuthenticate(BiometricManager.Authenticators.BIOMETRIC_STRONG) ==
                BiometricManager.BIOMETRIC_SUCCESS
    }

    /**
     * Shows the system biometric prompt. Calls onSuccess or onFailure on completion.
     * onAuthenticationFailed() is intentionally not overridden — the system dialog
     * shows its own retry UI (e.g., "Try again" for bad fingerprint).
     */
    fun authenticate(
        activity: FragmentActivity,
        title: String,
        subtitle: String,
        negativeButtonText: String,
        onSuccess: () -> Unit,
        onFailure: () -> Unit
    ) {
        val executor = ContextCompat.getMainExecutor(activity)

        val callback = object : BiometricPrompt.AuthenticationCallback() {
            override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
                onSuccess()
            }
            override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
                // Cancel pressed, lockout, or no biometrics enrolled
                onFailure()
            }
        }

        val prompt = BiometricPrompt(activity, executor, callback)
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle(title)
            .setSubtitle(subtitle)
            .setNegativeButtonText(negativeButtonText)
            .build()

        prompt.authenticate(promptInfo)
    }
}
```

### Key Decisions

- **`BIOMETRIC_STRONG` only** — no `DEVICE_CREDENTIAL` fallback (PIN/pattern). The negative button sends user to the login screen instead.
- **`onAuthenticationFailed` not overridden** — the system UI handles retry. Only `onAuthenticationError` (cancel/lockout) triggers `onFailure`.
- **`FragmentActivity` required** — `BiometricPrompt` needs a `FragmentActivity`. Compose activities extend `ComponentActivity`, which extends `FragmentActivity`, so this works out of the box.

## Step 2: AuthManager Storage

Store the biometric preference in EncryptedSharedPreferences alongside auth tokens. The key insight: **preserve biometric preference on logout**. **IMPORTANT:** The EncryptedSharedPreferences init MUST be wrapped in try-catch with fallback to regular SharedPreferences — Samsung Knox throws `KeyStoreException` during `MasterKey` creation (see `android-development` security skill).

```kotlin
// In AuthManager.kt

companion object {
    private const val KEY_BIOMETRIC_ENABLED = "biometric_enabled"
}

fun isBiometricEnabled(): Boolean =
    securePreferences.getBoolean(KEY_BIOMETRIC_ENABLED)

fun setBiometricEnabled(enabled: Boolean) {
    securePreferences.putBoolean(KEY_BIOMETRIC_ENABLED, enabled)
}

fun clearAuth() {
    // Save preferences that survive logout
    val savedBiometric = isBiometricEnabled()
    val savedLanguage = getLanguage()
    securePreferences.clear()
    // Restore
    if (savedBiometric) securePreferences.putBoolean(KEY_BIOMETRIC_ENABLED, true)
    if (savedLanguage != null) securePreferences.putString(KEY_LANGUAGE, savedLanguage)
}
```

## Step 3: Splash Screen Integration

The splash screen is the single integration point. Uses `CompletableDeferred` to bridge the callback-based `BiometricPrompt` into coroutine-based `LaunchedEffect`.

```kotlin
@Composable
fun SplashScreen(
    authManager: AuthManager,
    onNavigateToLogin: () -> Unit,
    onNavigateToMain: () -> Unit,
    onNavigateToChangePassword: () -> Unit
) {
    val context = LocalContext.current
    val activity = context as? FragmentActivity

    // Pre-resolve string resources outside the coroutine
    val biometricTitle = stringResource(R.string.biometric_prompt_title)
    val biometricSubtitle = stringResource(R.string.biometric_prompt_subtitle)
    val biometricCancel = stringResource(R.string.biometric_prompt_cancel)

    LaunchedEffect(Unit) {
        delay(1500) // Splash display time

        if (!authManager.isLoggedIn()) {
            onNavigateToLogin()
            return@LaunchedEffect
        }

        val biometricPref = authManager.isBiometricEnabled()
        val canAuth = activity != null && BiometricHelper.canAuthenticate(activity)

        if (biometricPref && canAuth) {
            // Bridge callback → coroutine
            val result = CompletableDeferred<Boolean>()
            BiometricHelper.authenticate(
                activity = activity!!,
                title = biometricTitle,
                subtitle = biometricSubtitle,
                negativeButtonText = biometricCancel,
                onSuccess = { result.complete(true) },
                onFailure = { result.complete(false) }
            )
            if (result.await()) {
                // Biometric passed — check force password change then go to main
                if (authManager.isForcePasswordChange()) {
                    onNavigateToChangePassword()
                } else {
                    onNavigateToMain()
                }
            } else {
                // Biometric failed/cancelled — send to login
                onNavigateToLogin()
            }
        } else {
            // No biometric — go straight through
            if (authManager.isForcePasswordChange()) {
                onNavigateToChangePassword()
            } else {
                onNavigateToMain()
            }
        }
    }

    // Splash UI (logo, brand name, etc.)
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Image(
            painter = painterResource(R.mipmap.ic_launcher_foreground),
            contentDescription = null,
            modifier = Modifier.size(150.dp)
        )
    }
}
```

### Navigation Setup

The splash screen pops itself from the back stack when navigating:

```kotlin
composable(Screen.Splash.route) {
    SplashScreen(
        authManager = authManager,
        onNavigateToLogin = {
            navController.navigate(Screen.Login.route) {
                popUpTo(Screen.Splash.route) { inclusive = true }
            }
        },
        onNavigateToMain = {
            navController.navigate(Screen.Dashboard.route) {
                popUpTo(Screen.Splash.route) { inclusive = true }
            }
        },
        onNavigateToChangePassword = {
            navController.navigate(Screen.ChangePassword.route) {
                popUpTo(Screen.Splash.route) { inclusive = true }
            }
        }
    )
}
```

## Step 4: Settings Toggle

The toggle is **conditionally rendered** — only shown if the device supports biometrics. Enabling requires biometric verification first.

```kotlin
// In SettingsScreen.kt, inside the Security section

val activity = context as? FragmentActivity
if (activity != null && BiometricHelper.canAuthenticate(activity)) {
    HorizontalDivider()

    var biometricEnabled by remember { mutableStateOf(viewModel.isBiometricEnabled()) }
    val verifyTitle = stringResource(R.string.biometric_verify_title)
    val verifySubtitle = stringResource(R.string.biometric_verify_subtitle)
    val verifyCancel = stringResource(R.string.biometric_prompt_cancel)

    ListItem(
        headlineContent = { Text(stringResource(R.string.biometric_login_title)) },
        supportingContent = { Text(stringResource(R.string.biometric_login_subtitle)) },
        leadingContent = {
            Icon(Icons.Default.Fingerprint, contentDescription = null,
                tint = MaterialTheme.colorScheme.primary)
        },
        trailingContent = {
            Switch(
                checked = biometricEnabled,
                onCheckedChange = { enabled ->
                    if (enabled) {
                        // Verify identity before enabling
                        BiometricHelper.authenticate(
                            activity = activity,
                            title = verifyTitle,
                            subtitle = verifySubtitle,
                            negativeButtonText = verifyCancel,
                            onSuccess = {
                                viewModel.setBiometricEnabled(true)
                                biometricEnabled = true
                            },
                            onFailure = { /* Verification failed — don't enable */ }
                        )
                    } else {
                        // Disabling doesn't require verification
                        viewModel.setBiometricEnabled(false)
                        biometricEnabled = false
                    }
                }
            )
        }
    )
}
```

## Step 5: String Resources

```xml
<!-- Biometric (7 strings, translate all) -->
<string name="biometric_login_title">Biometric Login</string>
<string name="biometric_login_subtitle">Use fingerprint or face to unlock</string>
<string name="biometric_prompt_title">Biometric Login</string>
<string name="biometric_prompt_subtitle">Verify your identity to access the app</string>
<string name="biometric_prompt_cancel">Use Password</string>
<string name="biometric_verify_title">Verify Identity</string>
<string name="biometric_verify_subtitle">Authenticate to enable biometric login</string>
```

## Flow Diagram

```
App Launch
  ↓
[Splash Screen] — 1.5s delay
  ↓
isLoggedIn()?
  ├─ NO → Login Screen
  └─ YES
      ↓
      isBiometricEnabled() && canAuthenticate()?
        ├─ YES → System BiometricPrompt
        │   ├─ Success → forcePasswordChange? → Dashboard / ChangePassword
        │   └─ Failure/Cancel → Login Screen
        └─ NO → forcePasswordChange? → Dashboard / ChangePassword
```

## Patterns & Anti-Patterns

### DO
- Use `BIOMETRIC_STRONG` (Class 3) for security-sensitive apps
- Require biometric verification when the user turns the feature ON
- Preserve biometric preference across logout (`clearAuth()` saves + restores it)
- Use `CompletableDeferred` to bridge BiometricPrompt callbacks into coroutines
- Hide the toggle entirely on devices without biometric hardware
- Use `context as? FragmentActivity` safely (never force-cast)
- Pre-resolve string resources before entering `LaunchedEffect` (Compose rule)

### DON'T
- Don't add `DEVICE_CREDENTIAL` as a fallback — it defeats the purpose of biometric gate
- Don't override `onAuthenticationFailed()` — the system handles retry UI
- Don't store biometric data yourself — the system handles enrollment and matching
- Don't show biometric prompt on login screen — only on splash (user is already authenticated)
- Don't require biometric for disabling the feature — that traps users who can't authenticate
- Don't declare manifest permissions — `BiometricPrompt` on API 29+ doesn't need them
- Don't use `KeyguardManager` or deprecated `FingerprintManager` — use `BiometricPrompt` only

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| No biometric hardware | Settings toggle hidden, splash skips biometric |
| Biometrics enrolled then removed | `canAuthenticate()` returns false, splash skips |
| User cancels prompt | `onFailure()` → navigate to Login |
| Too many failed attempts (lockout) | System shows lockout message, then `onFailure()` |
| Force password change + biometric | Biometric first, then redirect to ChangePassword |
| App killed during prompt | Next launch starts fresh from splash |
| Multiple accounts on device | Biometric pref is per-app, not per-user |

## Integration with Other Skills

```
android-biometric-login
  ├── android-development     (project structure, Hilt, EncryptedSharedPreferences)
  ├── dual-auth-rbac          (JWT auth, AuthManager, token storage)
  └── jetpack-compose-ui      (Settings ListItem, Switch, Material 3 theming)
```

**Key integrations:**
- `dual-auth-rbac`: BiometricHelper works alongside JWT auth — biometric gates app access, JWT gates API access
- `android-development`: Follows MVVM pattern — ViewModel delegates to AuthManager, UI observes state
- `jetpack-compose-ui`: Settings toggle uses Material 3 `ListItem` + `Switch` pattern

## Checklist

- [ ] Add `androidx.biometric:biometric:1.1.0` dependency
- [ ] Create `BiometricHelper` object with `canAuthenticate()` + `authenticate()`
- [ ] Add biometric preference to AuthManager (persists across logout)
- [ ] Integrate biometric check in Splash screen with `CompletableDeferred`
- [ ] Add Settings toggle with verify-before-enable
- [ ] Add 7 string resources (translate to all supported languages)
- [ ] Test on device with biometrics, device without, and emulator
