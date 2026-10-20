---
name: tinyship-auth
description: >-
  Configure authentication providers for TinyShip: Google OAuth, GitHub OAuth,
  WeChat login, SMS OTP, and email/password with verification. Use when the user
  asks to "add google login", "configure github auth", "set up wechat login",
  "add SMS login", "configure authentication", "add OAuth", or "add social login".
---

# TinyShip Auth Provider Setup

Guide for configuring authentication methods in TinyShip. Built on [Better Auth](https://www.better-auth.com/).

## Available Auth Methods

| Method | Difficulty | Requirements |
|--------|-----------|--------------|
| **Email/Password** | Simple | Already works after setup |
| **Google OAuth** | Medium | Google Cloud Console project |
| **GitHub OAuth** | Medium | GitHub OAuth App |
| **WeChat Login** | Complex | WeChat Open Platform + business license |
| **SMS OTP** | Complex | Twilio or Aliyun SMS account |

Ask the user which method(s) they want to configure, then follow the relevant section.

## Email/Password (Default)

Already functional after basic setup. To enable email verification and password reset emails,
configure an email provider:

1. Set up Resend (simplest): get API key from [resend.com](https://resend.com)
2. Add to `.env`:

```
RESEND_API_KEY="re_xxxxx"
EMAIL_DEFAULT_FROM="noreply@yourdomain.com"
```

Read `docs/user-guide/auth/email.md` for detailed email auth configuration.

## Google OAuth

For detailed setup steps, read [references/google-oauth.md](references/google-oauth.md).

Summary:
1. Create project in Google Cloud Console
2. Configure OAuth consent screen
3. Create OAuth 2.0 credentials with redirect URI: `{APP_BASE_URL}/api/auth/callback/google`
4. Add to `.env`:

```
GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET="GOCSPX-xxxxx"
```

## GitHub OAuth

For detailed setup steps, read [references/github-oauth.md](references/github-oauth.md).

Summary:
1. Go to GitHub Settings > Developer settings > OAuth Apps > New
2. Set callback URL: `{APP_BASE_URL}/api/auth/callback/github`
3. Add to `.env`:

```
GITHUB_CLIENT_ID="Ov23xxxxxxxxxx"
GITHUB_CLIENT_SECRET="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## WeChat Login

For detailed setup steps, read [references/wechat-login.md](references/wechat-login.md).

Summary:
1. Register on WeChat Open Platform (requires business license)
2. Create a web application
3. Add to `.env`:

```
NEXT_PUBLIC_WECHAT_APP_ID="wx_xxxxx"
VITE_WECHAT_APP_ID="wx_xxxxx"
WECHAT_APP_SECRET="xxxxx"
```

## SMS OTP Login

For detailed setup steps, read [references/sms-login.md](references/sms-login.md).

Summary (Twilio):
1. Create Twilio account and get credentials
2. Add to `.env`:

```
TWILIO_ACCOUNT_SID="ACxxxxx"
TWILIO_AUTH_TOKEN="xxxxx"
TWILIO_DEFAULT_FROM="+1234567890"
```

Summary (Aliyun):
1. Enable Aliyun SMS service, create sign and template
2. Add to `.env`:

```
ALIYUN_ACCESS_KEY_ID="xxxxx"
ALIYUN_ACCESS_KEY_SECRET="xxxxx"
ALIYUN_SMS_SIGN_NAME="YourSign"
ALIYUN_SMS_TEMPLATE_CODE="SMS_000000000"
```

## Frontend: Configure Login Buttons

After adding providers, update the social auth buttons to show/hide them:

**Next.js**:
Edit `apps/next-app/components/social-auth.tsx`:

```typescript
const defaultProviders: SocialProvider[] = ['google', 'github'];
// Add or remove: 'google', 'github', 'wechat', 'phone'
```

**Nuxt.js**:
Edit `apps/nuxt-app/components/SocialAuth.vue`:

```typescript
providers: () => ['google', 'github']
// Add or remove: 'google', 'github', 'wechat', 'phone'
```

**TanStack Start**:
Edit `apps/tanstack-app/src/components/social-auth.tsx` (same pattern as Next.js).

## Verify

1. Restart the dev server after `.env` changes
2. Visit `/signin` and check that configured providers appear
3. Test the login flow for each provider
4. Verify the user appears in admin panel at `/admin/users`

## Reference Files in TinyShip Repo

- `config/auth.ts` — auth provider configuration
- `libs/auth/AGENTS.md` — auth library architecture
- `docs/user-guide/auth/overview.md` — auth documentation index
- `apps/next-app/components/social-auth.tsx` — Next.js social auth buttons
- `apps/tanstack-app/src/components/social-auth.tsx` — TanStack Start social auth buttons
- `apps/nuxt-app/components/SocialAuth.vue` — Nuxt.js social auth buttons
