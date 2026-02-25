---
name: authgear-integration
description: Integrate Authgear authentication into web, mobile, and backend applications. Use when developers request to "add authentication", "integrate Authgear", "implement login/logout", "validate JWT tokens", "add auth to React/React Native/Vue/Flutter/Android/iOS/backend app", or mention Authgear SDK setup. Supports React SPA, React Native, Android, iOS, Flutter, Vue.js, Next.js, Ionic for frontend, and Python, Node.js, Go, Java, PHP, ASP.NET for backend JWT validation with automatic dependency installation, configuration, authentication flows, protected routes, user profile pages, and API integration patterns.
---

# Authgear Integration

## Overview

This skill helps developers integrate Authgear authentication into their applications quickly and correctly. It provides framework-specific guidance, reusable code templates, and common patterns for:

- **Frontend Applications:** Protected routes, user profiles, API integration, role-based access control for React, React Native, Flutter, Android, iOS, and more
- **Backend Applications:** JWT token validation, API authentication, user verification for Python, Node.js, Go, Java, PHP, and ASP.NET servers

## Integration Workflow

### 1. Detect Project Type

Identify the project type by examining:
- Package files: `package.json`, `pubspec.yaml`, `build.gradle`, `Podfile`, `requirements.txt`, `pom.xml`, `composer.json`, `*.csproj`
- Project structure: presence of `src/`, `android/`, `ios/`, `lib/`, `app/`, `main/` directories
- Configuration files: `vite.config.js`, `next.config.js`, `angular.json`, `go.mod`, `appsettings.json`

Common project types:

**Frontend/Mobile Frameworks:**
- **React SPA**: `package.json` with `react` and `react-dom`, typically with `vite` or `react-scripts`
- **React Native**: `package.json` with `react-native`, `ios/` and `android/` directories
- **Flutter**: `pubspec.yaml` with `flutter` dependency
- **Android**: `build.gradle` files, `AndroidManifest.xml`
- **iOS**: `Podfile`, `.xcodeproj` or `.xcworkspace` files, Swift source files
- **Vue.js**: `package.json` with `vue` dependency
- **Next.js**: `package.json` with `next` dependency

**Backend Frameworks:**
- **Python (Flask/Django/FastAPI)**: `requirements.txt`, `setup.py`, or `pyproject.toml` with Flask/Django/FastAPI
- **Node.js (Express)**: `package.json` with `express` or other Node.js server frameworks
- **Go**: `go.mod` file, `main.go` or `*.go` files
- **Java (Spring Boot)**: `pom.xml` or `build.gradle` with Spring Boot dependencies
- **PHP**: `composer.json` with PHP dependencies
- **ASP.NET Core**: `*.csproj` file with ASP.NET Core packages

### 2. Ask User for Configuration

Use AskUserQuestion to gather required information:

```json
{
  "questions": [
    {
      "question": "Do you have an Authgear project setup? If yes, provide your Client ID.",
      "header": "Client ID",
      "multiSelect": false,
      "options": [
        {
          "label": "I have a Client ID",
          "description": "Provide your Authgear Client ID from the portal"
        },
        {
          "label": "Not yet, help me set it up",
          "description": "Guide me through creating an Authgear project"
        }
      ]
    },
    {
      "question": "What is your Authgear endpoint URL?",
      "header": "Endpoint",
      "multiSelect": false,
      "options": [
        {
          "label": "I have an endpoint",
          "description": "Provide your Authgear endpoint (e.g., https://myapp.authgear.cloud)"
        },
        {
          "label": "Help me find it",
          "description": "Show me where to find my endpoint"
        }
      ]
    }
  ]
}
```

If user doesn't have Client ID or Endpoint, guide them:
- Visit https://portal.authgear.com
- Create a new project or select existing
- Navigate to Applications → Create Application
- Select appropriate application type (Native App for mobile, SPA for web)
- Configure redirect URIs
- Copy Client ID and Endpoint

### 3. Install Dependencies

Based on detected framework:

**React SPA:**
```bash
npm install --save --save-exact @authgear/web
```

**React Native:**
```bash
npm install --exact @authgear/react-native
cd ios && pod install
```

**Flutter:**
```bash
flutter pub add flutter_authgear
```

**Android:**
Add to `build.gradle` - see [references/android.md](references/android.md)

**iOS:**
Via Swift Package Manager: `https://github.com/authgear/authgear-sdk-ios.git`
Or CocoaPods: `pod 'Authgear', :git => 'https://github.com/authgear/authgear-sdk-ios.git'`

### 4. Configure Environment Variables

Create or update `.env` file (or appropriate config for framework):

**React (Vite):**
```properties
VITE_AUTHGEAR_CLIENT_ID=<CLIENT_ID>
VITE_AUTHGEAR_ENDPOINT=<ENDPOINT>
VITE_AUTHGEAR_REDIRECT_URL=http://localhost:5173/auth-redirect
```

**React (Create React App):**
```properties
REACT_APP_AUTHGEAR_CLIENT_ID=<CLIENT_ID>
REACT_APP_AUTHGEAR_ENDPOINT=<ENDPOINT>
REACT_APP_AUTHGEAR_REDIRECT_URL=http://localhost:3000/auth-redirect
```

For React Native, Flutter, Android: credentials typically hardcoded in config or stored in platform-specific secure storage.

### 5. Implement Core Authentication

Use framework-specific templates from `assets/` and detailed guides from `references/`:

**For React:**
1. Copy `assets/react/UserProvider.tsx` to `src/`
2. Copy `assets/react/AuthRedirect.tsx` to `src/pages/` or `src/components/`
3. Copy `assets/react/useAuthgear.ts` to `src/hooks/`
4. Update routing to include `/auth-redirect` route
5. Wrap app with `UserContextProvider`

See [references/react.md](references/react.md) for complete implementation details.

**For React Native:**
1. Initialize SDK in `App.tsx`
2. Configure platform-specific redirect handling (AndroidManifest.xml, Info.plist)
3. Implement authentication flow with session state management

See [references/react-native.md](references/react-native.md) for complete implementation details.

**For Flutter:**
1. Add SDK initialization in app state
2. Configure platform-specific URL schemes
3. Implement authentication UI

See [references/flutter.md](references/flutter.md) for complete implementation details.

**For Android:**
1. Add SDK dependency
2. Initialize in MainActivity
3. Configure redirect activity in manifest

See [references/android.md](references/android.md) for complete implementation details.

**For iOS:**
1. Add SDK via Swift Package Manager or CocoaPods
2. Initialize Authgear instance in app
3. Configure custom URI scheme in Info.plist

See [references/ios.md](references/ios.md) for complete implementation details.

### 6. Implement Requested Features

Based on user requirements, implement common patterns from [references/common-patterns.md](references/common-patterns.md):

**Protected Routes:**
- Use `ProtectedRoute` component (React) from `assets/react/ProtectedRoute.tsx`
- Implement navigation guards for React Native/Flutter
- See examples in common-patterns.md

**User Profile Page:**
- Fetch user info using `authgear.fetchUserInfo()`
- Display user details (ID, email, phone)
- Add settings button using `authgear.open(Page.Settings)`

**API Integration:**
- Use `authgear.fetch()` for automatic token handling
- Or manually add Authorization header with `authgear.accessToken`
- Implement token refresh logic

**Role-Based Access:**
- Extract roles/permissions from user info
- Create permission checking hooks/utilities
- Conditionally render UI based on roles

### 7. Add Login/Logout UI

Create UI components for authentication:

**Login Button:**
```tsx
// React
import { useAuthgear } from './hooks/useAuthgear';

const LoginButton = () => {
  const { login } = useAuthgear();
  return <button onClick={login}>Login</button>;
};
```

**Logout Button:**
```tsx
const LogoutButton = () => {
  const { logout } = useAuthgear();
  return <button onClick={logout}>Logout</button>;
};
```

**Settings Button:**
```tsx
const SettingsButton = () => {
  const { openSettings } = useAuthgear();
  return <button onClick={openSettings}>Settings</button>;
};
```

### 8. Test Integration

**For Frontend Applications:**

Guide user to test:
1. Start development server
2. Click login button → should redirect to Authgear
3. Complete authentication
4. Should redirect back to app at `/auth-redirect`
5. Should then navigate to home page as authenticated user
6. Verify protected routes work
7. Test logout functionality

**For Backend Applications:**

Guide user to test:
1. Start backend server
2. Get a test access token from frontend or Auth API
3. Make request to protected endpoint with `Authorization: Bearer <token>` header
4. Should receive successful response with user data
5. Test without token → should receive 401 Unauthorized
6. Test with expired token → should receive 401 Unauthorized
7. Verify user claims are correctly extracted

## Backend Integration Workflow

For backend API applications that need to validate JWT access tokens:

### 1. Ask User for Configuration

Use AskUserQuestion to gather required information:

```json
{
  "questions": [
    {
      "question": "What is your Authgear endpoint URL?",
      "header": "Endpoint",
      "multiSelect": false,
      "options": [
        {
          "label": "I have an endpoint",
          "description": "Provide your Authgear endpoint (e.g., https://myproject.authgear.cloud)"
        },
        {
          "label": "Help me find it",
          "description": "Show me where to find my endpoint in the Portal"
        }
      ]
    },
    {
      "question": "What is your Authgear Client ID?",
      "header": "Client ID",
      "multiSelect": false,
      "options": [
        {
          "label": "I have a Client ID",
          "description": "Provide your application's Client ID from the portal"
        },
        {
          "label": "Help me set it up",
          "description": "Guide me through creating an application"
        }
      ]
    }
  ]
}
```

**Authgear Endpoint Format:**
- Usually looks like: `https://[project-name].authgear.cloud`
- Or custom domain: `https://auth.yourdomain.com`
- Should NOT have trailing slash
- Example: `https://myapp.authgear.cloud`

If user doesn't have endpoint or Client ID, guide them:
1. Visit https://portal.authgear.com
2. Select your project or create a new one
3. Navigate to **Applications** → **Create Application** or select existing
4. Select **"Machine-to-Machine"** or **"Single Page Application"** type (depending on use case)
5. Enable **"Issue JWT as access token"** in application settings
6. Copy the **Client ID** from application details
7. Copy the **Endpoint** from project settings (format: `https://[project-name].authgear.cloud`)

### 2. Verify Prerequisites

- **Enable JWT tokens:** Ensure "Issue JWT as access token" is enabled in Authgear Portal for your application
- **Token-based auth required:** Cookie-based authentication does not support JWT validation
- **Note configuration:** Have your Authgear Endpoint and Client ID ready

### 3. Install Backend Dependencies

Based on detected language:

**Python:**
```bash
pip install PyJWT cryptography requests
```

**Node.js:**
```bash
npm install jwks-rsa jsonwebtoken axios
```

**Go:**
```bash
go get github.com/lestrrat-go/jwx/v2/jwt
go get github.com/lestrrat-go/jwx/v2/jwk
```

**Java (Maven):**
```xml
<dependency>
    <groupId>com.nimbusds</groupId>
    <artifactId>nimbus-jose-jwt</artifactId>
    <version>9.31</version>
</dependency>
```

**PHP:**
```bash
composer require firebase/php-jwt guzzlehttp/guzzle
```

**ASP.NET Core:**
```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

### 4. Implement JWT Validation

Follow language-specific implementation from [references/backend-api.md](references/backend-api.md):

**Key Steps:**
1. Fetch JWKS (JSON Web Key Set) from discovery endpoint
2. Extract token from `Authorization: Bearer <token>` header
3. Decode token header to get Key ID (`kid`)
4. Find matching public key from JWKS
5. Verify signature using RS256 algorithm
6. Validate expiration (`exp`) and audience (`aud`) claims
7. Extract user information from validated claims

**Performance Tip:** Cache JWKS for 10-60 minutes to avoid fetching on every request

### 5. Create Authentication Middleware

Implement middleware/decorator to protect endpoints:

**Python (Flask):**
```python
@require_auth
def protected_endpoint():
    user_id = request.user_id
    return jsonify({"user_id": user_id})
```

**Node.js (Express):**
```javascript
app.get('/api/profile', verifyToken, (req, res) => {
  res.json({ user_id: req.userId });
});
```

**Go:**
```go
http.HandleFunc("/api/profile", verifyTokenMiddleware(profileHandler))
```

**Java (Spring Boot):**
```java
@GetMapping("/api/profile")
public ResponseEntity<?> getProfile(HttpServletRequest request) {
    String userId = (String) request.getAttribute("user_id");
    return ResponseEntity.ok(userId);
}
```

**ASP.NET Core:**
```csharp
[Authorize]
[HttpGet("profile")]
public IActionResult GetProfile() {
    var userId = User.FindFirst("sub")?.Value;
    return Ok(new { user_id = userId });
}
```

### 6. Add Protected Endpoints

Create API endpoints that require authentication:

1. Extract user ID from validated claims (`sub` claim)
2. Use user ID to fetch user-specific data
3. Return appropriate error codes (401 for auth failures)
4. Implement role-based access control if needed

### 7. Test Backend Integration

1. **Using Authgear SDK's Built-in Fetch (Recommended for Frontend Apps):**

If your frontend uses Authgear's JavaScript SDK, use the built-in `fetch` function:

```javascript
// Automatically includes Authorization header and refreshes token
authgear
  .fetch("http://localhost:3000/api/profile")
  .then(response => response.json())
  .then(data => console.log(data));
```

**Benefits:**
- Automatic Authorization header injection
- Automatic token refresh handling
- No manual token management needed

**Note:** JavaScript/Web SDK only. Mobile platforms (iOS, Android) must manually call `refreshAccessTokenIfNeeded()` and construct headers.

2. **Using cURL (Manual Testing):**

Get test token and make request:
```bash
# Get token from frontend or use OAuth password grant
curl http://localhost:3000/api/profile \
  -H "Authorization: Bearer <VALID_TOKEN>"
```

3. **Test error cases:**
   - No token → 401 Unauthorized
   - Invalid token → 401 Unauthorized
   - Expired token → 401 Unauthorized

4. **Verify claims extraction:**
   - Check that user ID and email are correctly extracted
   - Verify custom claims are accessible

See [references/backend-api.md](references/backend-api.md) for complete implementation details, code examples, security best practices, and troubleshooting guides for all supported languages.

## Framework-Specific Guides

For detailed implementation instructions, consult these framework-specific references:

**Frontend/Mobile:**
- **React SPA**: [references/react.md](references/react.md)
- **React Native**: [references/react-native.md](references/react-native.md)
- **Android**: [references/android.md](references/android.md)
- **iOS**: [references/ios.md](references/ios.md)
- **Flutter**: [references/flutter.md](references/flutter.md)

**Backend:**
- **Backend API (Python, Node.js, Go, Java, PHP, ASP.NET)**: [references/backend-api.md](references/backend-api.md)

## Common Patterns

For implementing specific features, see [references/common-patterns.md](references/common-patterns.md):

- Protected routes and navigation guards
- User profile pages with settings
- API integration with automatic token handling
- Role-based access control

## Quick Setup Examples

### React SPA - Minimal Setup

```tsx
// 1. Install
npm install --save --save-exact @authgear/web react-router-dom

// 2. Wrap app with provider (App.tsx)
import { UserContextProvider } from './UserProvider';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AuthRedirect from './AuthRedirect';
import Home from './Home';

function App() {
  return (
    <UserContextProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/auth-redirect" element={<AuthRedirect />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </BrowserRouter>
    </UserContextProvider>
  );
}

// 3. Add login button (Home.tsx)
import { useAuthgear } from './hooks/useAuthgear';
import { useUser } from './UserProvider';

function Home() {
  const { login, logout } = useAuthgear();
  const { isLoggedIn } = useUser();

  return (
    <div>
      {isLoggedIn ? (
        <button onClick={logout}>Logout</button>
      ) : (
        <button onClick={login}>Login</button>
      )}
    </div>
  );
}
```

### React Native - Minimal Setup

```tsx
// 1. Install
npm install --exact @authgear/react-native
cd ios && pod install

// 2. Initialize in App.tsx
import authgear, { SessionState } from '@authgear/react-native';
import { useEffect, useState } from 'react';
import { Button, Text, View } from 'react-native';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    authgear.configure({
      clientID: '<CLIENT_ID>',
      endpoint: '<ENDPOINT>',
    }).then(() => {
      authgear.delegate = {
        onSessionStateChange: (container) => {
          setIsLoggedIn(container.sessionState === SessionState.Authenticated);
        },
      };
    });
  }, []);

  const handleLogin = () => {
    authgear.authenticate({ redirectURI: 'com.myapp://host/path' });
  };

  const handleLogout = () => {
    authgear.logout();
  };

  return (
    <View>
      {isLoggedIn ? (
        <Button title="Logout" onPress={handleLogout} />
      ) : (
        <Button title="Login" onPress={handleLogin} />
      )}
    </View>
  );
}

// 3. Configure AndroidManifest.xml and Info.plist (see references/react-native.md)
```

## Resources

- **assets/react/**: Ready-to-use React components (UserProvider, AuthRedirect, ProtectedRoute, useAuthgear hook)
- **references/**: Detailed framework-specific integration guides
- **Authgear Documentation**: https://docs.authgear.com
- **Authgear Portal**: https://portal.authgear.com

## Important Notes

**Frontend Applications:**
- Always use environment variables for Client ID and Endpoint (never hardcode in React web apps)
- For mobile apps, configure platform-specific URL schemes in AndroidManifest.xml and Info.plist
- Use `useRef` in React 18+ to prevent duplicate authentication in StrictMode
- Call `refreshAccessTokenIfNeeded()` before using access tokens
- Use `authgear.fetch()` for automatic token handling in API calls

**Backend Applications:**
- Enable "Issue JWT as access token" in Authgear Portal settings
- Cache JWKS for 10-60 minutes to improve performance
- Always validate signature, expiration, audience, and issuer claims
- Use HTTPS only - never transmit tokens over HTTP
- Token-based authentication required (cookie-based auth not supported for JWT validation)
- Implement proper error handling for expired and invalid tokens
