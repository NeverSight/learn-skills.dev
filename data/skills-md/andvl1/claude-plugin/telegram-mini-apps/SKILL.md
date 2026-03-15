---
name: telegram-mini-apps
description: Telegram Mini Apps development - use for building Mini App frontend, WebApp API, initData authentication, and Telegram integration
---

# Telegram Mini Apps Development

## Quick Reference

### WebApp Object (window.Telegram.WebApp)

```javascript
// Initialize app
Telegram.WebApp.ready();
Telegram.WebApp.expand();

// Get user data (UNSAFE - for display only)
const user = Telegram.WebApp.initDataUnsafe.user;
// { id, firstName, lastName, username, languageCode, isPremium }

// Get signed data (send to backend for validation)
const initDataRaw = Telegram.WebApp.initData;
// Send via: Authorization: tma ${initDataRaw}
```

### Key Methods

| Method | Purpose |
|--------|---------|
| `ready()` | Signal app loaded |
| `expand()` | Expand to full height |
| `close()` | Close the app |
| `sendData(data)` | Send data to bot (closes app) |
| `openLink(url)` | Open external URL |
| `openTelegramLink(url)` | Open Telegram link |
| `showAlert(msg)` | Show native alert |
| `showConfirm(msg)` | Show native confirm |
| `showPopup(params)` | Show custom popup |
| `setHeaderColor(color)` | Change header color |
| `setBackgroundColor(color)` | Change background |
| `triggerHapticFeedback(type, style)` | Vibration feedback |

### Main Button Configuration

```javascript
const mainButton = Telegram.WebApp.MainButton;

mainButton.text = 'Save Settings';
mainButton.color = '#5288c1';
mainButton.textColor = '#ffffff';
mainButton.show();

mainButton.onClick(() => {
  // Handle click
  mainButton.showProgress();
  // ... async operation
  mainButton.hideProgress();
});
```

### Back Button

```javascript
const backButton = Telegram.WebApp.BackButton;

backButton.show();
backButton.onClick(() => {
  // Navigate back
});
backButton.hide();
```

### Theme Colors

```javascript
const theme = Telegram.WebApp.themeParams;
// {
//   bg_color, text_color, hint_color, link_color,
//   button_color, button_text_color, secondary_bg_color,
//   header_bg_color, accent_text_color, section_bg_color,
//   section_header_text_color, subtitle_text_color,
//   destructive_text_color
// }

// CSS variables available:
// var(--tg-theme-bg-color)
// var(--tg-theme-text-color)
// etc.
```

### Events

```javascript
// Theme changed
Telegram.WebApp.onEvent('themeChanged', () => {
  const newTheme = Telegram.WebApp.themeParams;
});

// Viewport changed
Telegram.WebApp.onEvent('viewportChanged', () => {
  const height = Telegram.WebApp.viewportHeight;
});

// Main button clicked
Telegram.WebApp.onEvent('mainButtonClicked', () => {
  // Handle
});

// Back button clicked
Telegram.WebApp.onEvent('backButtonClicked', () => {
  // Navigate
});
```

### Storage APIs

```javascript
// Device Storage (5MB per bot)
await Telegram.WebApp.DeviceStorage.setItem('key', 'value');
const value = await Telegram.WebApp.DeviceStorage.getItem('key');

// Secure Storage (encrypted, 10 items max)
await Telegram.WebApp.SecureStorage.setItem('token', 'secret');

// Cloud Storage (synced across devices)
await Telegram.WebApp.CloudStorage.setItem('preference', 'dark');
```

## SDK Usage (@telegram-apps/sdk-react)

### Installation

```bash
npm install @telegram-apps/sdk @telegram-apps/sdk-react
```

### Provider Setup

```tsx
import { SDKProvider, useLaunchParams } from '@telegram-apps/sdk-react';

function App() {
  return (
    <SDKProvider acceptCustomStyles debug>
      <Router>
        <AppContent />
      </Router>
    </SDKProvider>
  );
}
```

### Hooks

```tsx
import {
  useLaunchParams,
  useInitData,
  useInitDataRaw,
  useThemeParams,
  useViewport,
  useMainButton,
  useBackButton,
  useCloudStorage,
} from '@telegram-apps/sdk-react';

function MyComponent() {
  // User data
  const initData = useInitData();
  const user = initData?.user;

  // Raw data for backend
  const initDataRaw = useInitDataRaw();

  // Theme
  const themeParams = useThemeParams();

  // Viewport
  const viewport = useViewport();
  const { height, stableHeight, isExpanded } = viewport;

  // Main button
  const mainButton = useMainButton();
  mainButton.setParams({
    text: 'Save',
    isVisible: true,
  });
  mainButton.on('click', handleSave);
}
```

### Mock Environment (Development)

```tsx
import { mockTelegramEnv } from '@telegram-apps/sdk-react';

if (import.meta.env.DEV) {
  mockTelegramEnv({
    themeParams: {
      bgColor: '#17212b',
      textColor: '#f5f5f5',
      buttonColor: '#5288c1',
      buttonTextColor: '#ffffff',
      // ... other params
    },
    initData: {
      user: {
        id: 99281932,
        firstName: 'Test',
        lastName: 'User',
        username: 'testuser',
        languageCode: 'en',
        isPremium: true,
      },
      hash: 'mock-hash',
      authDate: new Date(),
    },
    version: '7.2',
    platform: 'tdesktop',
  });
}
```

## Backend Authentication (Kotlin/Spring)

### InitData Validation

```kotlin
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec

@Service
class TelegramAuthService(
    @Value("\${telegram.bot.token}") private val botToken: String
) {

    fun validateInitData(initDataRaw: String): TelegramUser? {
        val params = parseInitData(initDataRaw)
        val hash = params["hash"] ?: return null
        val dataCheckString = params
            .filterKeys { it != "hash" }
            .toSortedMap()
            .map { "${it.key}=${it.value}" }
            .joinToString("\n")

        val secretKey = hmacSha256("WebAppData".toByteArray(), botToken.toByteArray())
        val calculatedHash = hmacSha256(secretKey, dataCheckString.toByteArray())
            .toHexString()

        if (calculatedHash != hash) return null

        val authDate = params["auth_date"]?.toLongOrNull() ?: return null
        if (System.currentTimeMillis() / 1000 - authDate > 3600) return null

        return parseUser(params["user"] ?: return null)
    }

    private fun hmacSha256(key: ByteArray, data: ByteArray): ByteArray {
        val mac = Mac.getInstance("HmacSHA256")
        mac.init(SecretKeySpec(key, "HmacSHA256"))
        return mac.doFinal(data)
    }
}
```

### REST Controller Pattern

```kotlin
@RestController
@RequestMapping("/api/v1/miniapp")
class MiniAppController(
    private val authService: TelegramAuthService,
    private val settingsService: ChatSettingsService
) {

    @GetMapping("/chats")
    fun getUserChats(
        @RequestHeader("Authorization") authHeader: String
    ): ResponseEntity<List<ChatResponse>> {
        val initData = authHeader.removePrefix("tma ")
        val user = authService.validateInitData(initData)
            ?: throw UnauthorizedException("Invalid initData")

        val chats = settingsService.findChatsWhereAdmin(user.id)
        return ResponseEntity.ok(chats.map { it.toResponse() })
    }

    @PutMapping("/chats/{chatId}/settings")
    fun updateChatSettings(
        @PathVariable chatId: Long,
        @RequestHeader("Authorization") authHeader: String,
        @RequestBody request: UpdateSettingsRequest
    ): ResponseEntity<ChatSettingsResponse> {
        val user = validateAuth(authHeader)

        if (!adminService.isAdmin(user.id, chatId)) {
            throw ForbiddenException("Not admin in this chat")
        }

        val settings = settingsService.update(chatId, request)
        return ResponseEntity.ok(settings.toResponse())
    }
}
```

## Component Library (@telegram-apps/ui)

### Installation

```bash
npm install @telegram-apps/ui
```

### Components

```tsx
import {
  AppRoot,
  Button,
  Cell,
  Section,
  Switch,
  Input,
  Select,
  Slider,
  Spinner,
  Placeholder,
} from '@telegram-apps/ui';

function SettingsPage() {
  return (
    <AppRoot>
      <Section header="Chat Settings">
        <Cell
          after={<Switch checked={isEnabled} onChange={setIsEnabled} />}
          description="Enable message collection"
        >
          Collection
        </Cell>

        <Cell
          after={<Select value={action} onChange={setAction}>
            <option value="WARN">Warn</option>
            <option value="MUTE">Mute</option>
            <option value="BAN">Ban</option>
          </Select>}
          description="Action when warning threshold reached"
        >
          Threshold Action
        </Cell>

        <Cell description="Maximum warnings before action">
          <Slider
            min={1}
            max={10}
            value={maxWarnings}
            onChange={setMaxWarnings}
          />
        </Cell>
      </Section>

      <Button size="large" stretched onClick={handleSave}>
        Save Settings
      </Button>
    </AppRoot>
  );
}
```

## Limitations

1. **HTTPS Required** - Production apps must be served over HTTPS
2. **4KB Data Limit** - `sendData()` limited to 4096 bytes
3. **No Camera/Mic** - Direct access not available
4. **initData Expiry** - Valid for ~1 hour from auth_date
5. **WebView Constraints** - Limited to WebView capabilities
6. **Cross-Client Differences** - Features may vary between iOS/Android/Desktop

## Resources

- [Official Docs](https://core.telegram.org/bots/webapps)
- [Community Docs](https://docs.telegram-mini-apps.com/)
- [@telegram-apps/sdk](https://www.npmjs.com/package/@telegram-apps/sdk)
- [React Template](https://github.com/Telegram-Mini-Apps/reactjs-template)
