---
name: better-auth
description: >
  Better Auth (TypeScript 認証フレームワーク) v1.7 リファレンス。
  認証・認可、サインアップ・サインイン、セッション管理、OAuth、パスキー、二要素認証 (2FA / TOTP)、SSO / SAML、SCIM、
  OAuth Provider (OAuth 2.1 / OIDC)、MCP 認可 (@better-auth/mcp)、Infrastructure (dash / sentinel)、
  プラグイン (organization, admin, magic-link, anonymous 等)。betterAuth, createAuthClient, signUp, signIn, getSession。
  Next.js, Nuxt, SvelteKit, Hono, Express, Expo, TanStack, Effect 統合。
user-invocable: false
---

# Better Auth API リファレンス

Better Auth — TypeScript 向けフレームワーク非依存の認証・認可フレームワーク。
対象 Better Auth v1.7.10（docs: GitHub tag v1.7.10、取得 2026-10-17）。1.6 からの移行は `references/guides/1-7-upgrade-guide.md`。
ユーザーのタスクに応じて適切な README.md を読み、そこから個別ファイルへ辿ること。

## ディレクトリ構成

```text
skills/better-auth/
  SKILL.md
  references/
    getting-started/
      README.md
      installation.md
      basic-usage.md
    concepts/
      README.md
      api.md
      cli.md
      client.md
      cookies.md
      database.md
      dynamic-base-url.md
      email.md
      hooks.md
      oauth.md
      plugins.md
      rate-limit.md
      session-management.md
      typescript.md
      users-accounts.md
    adapters/
      README.md
      community-adapters.md
      drizzle.md
      mongodb.md
      mssql.md
      mysql.md
      other-relational.md
      postgresql.md
      prisma.md
      sqlite.md
    integrations/
      README.md
      astro.md
      convex.md
      electron.md
      elysia.md
      encore.md
      expo.md
      express.md
      fastify.md
      hono.md
      lynx.md
      nestjs.md
      next.md
      nitro.md
      nuxt.md
      react-router.md
      solid-start.md
      svelte-kit.md
      tanstack.md
      waku.md
      effect.md
    examples/
      README.md
      astro.md
      next-js.md
      nuxt.md
      react-router.md
      svelte-kit.md
    authentication/
      README.md
      email-password.md
      social-providers-common.md
      other-social-providers.md
      social-apple.md
      social-atlassian.md
      social-cloudflare.md
      social-cognito.md
      social-discord.md
      social-dropbox.md
      social-facebook.md
      social-figma.md
      social-github.md
      social-gitlab.md
      social-google.md
      social-huggingface.md
      social-kakao.md
      social-kick.md
      social-line.md
      social-linear.md
      social-linkedin.md
      social-microsoft.md
      social-naver.md
      social-notion.md
      social-paybin.md
      social-paypal.md
      social-polar.md
      social-railway.md
      social-reddit.md
      social-roblox.md
      social-salesforce.md
      social-slack.md
      social-spotify.md
      social-tiktok.md
      social-twitch.md
      social-twitter.md
      social-vercel.md
      social-vk.md
      social-wechat.md
      social-zoom.md
    plugins/
      README.md
      admin.md
      agent-auth.md
      anonymous.md
      api-key.md
      api-key-advanced.md
      api-key-reference.md
      autumn.md
      bearer.md
      captcha.md
      chargebee.md
      cimd.md
      commet.md
      community-plugins.md
      creem.md
      device-authorization.md
      dodopayments.md
      dub.md
      email-otp.md
      generic-oauth.md
      have-i-been-pwned.md
      i18n.md
      jwt.md
      last-login-method.md
      magic-link.md
      mcp.md
      multi-session.md
      oauth-provider.md
      oauth-proxy.md
      oidc-provider.md
      one-tap.md
      one-time-token.md
      open-api.md
      organization.md
      passkey.md
      phone-number.md
      polar.md
      scim.md
      scim-groups-and-roles.md
      scim-reference.md
      siwe.md
      sso.md
      stripe.md
      test-utils.md
      two-factor.md
      username.md
    infrastructure/
      README.md
      introduction.md
      getting-started.md
      dashboard.md
      audit-logs.md
      sentinel.md
      email-service.md
      sms-service.md
    reference/
      README.md
      contributing.md
      options.md
      resources.md
      security.md
      faq.md
      instrumentation.md
      telemetry.md
      errors.md
      error-account-already-linked.md
      error-account-not-linked.md
      error-email-doesnt-match.md
      error-email-not-found.md
      error-internal-server-error.md
      error-invalid-callback-request.md
      error-invalid-code.md
      error-no-callback-url.md
      error-no-code.md
      error-oauth-provider-not-found.md
      error-signup-disabled.md
      error-state-invalid.md
      error-state-mismatch.md
      error-state-not-found.md
      error-unable-to-create-session.md
      error-unable-to-create-user.md
      error-unable-to-get-user-info.md
      error-unable-to-link-account.md
      error-unknown.md
    guides/
      README.md
      1-7-upgrade-guide.md
      auth0-migration.md
      browser-extension.md
      clerk-migration.md
      create-a-db-adapter.md
      dynamic-base-url.md
      next-auth-migration.md
      optimizing-for-performance.md
      saml-sso-with-okta.md
      supabase-migration.md
      workos-migration.md
      your-first-plugin.md
  samples/
    README.md
    astro.md
    client-setup.md
    convex.md
    electron.md
    elysia.md
    email-password-auth.md
    email-verification.md
    encore.md
    expo.md
    express.md
    fastify.md
    hono.md
    hooks.md
    lynx.md
    mcp-server.md
    nestjs.md
    next.md
    nitro.md
    nuxt.md
    password-reset.md
    react-router.md
    server-setup.md
    session-management.md
    sign-out.md
    social-sign-in.md
    solid-start.md
    svelte-kit.md
    tanstack.md
    two-factor-auth.md
    user-management.md
    waku.md
  scripts/
    README.md
    cli.md
    generate.md
    install.md
```

## 探索手順

タスクからカテゴリを引き、カテゴリの README.md で目的のページを特定する:

1. 下記マッピング表でタスクに対応するカテゴリを探す
2. そのカテゴリの `references/{category}/README.md` を参照して目的のページを特定する
3. 該当ページの `.md` を Read して詳細を確認する

## タスク → カテゴリ マッピング

| タスク | カテゴリ | 参照 README |
|--------|---------|------------|
| インストール・初期設定・auth インスタンス作成 | getting-started | [references/getting-started/README.md](references/getting-started/README.md) |
| 基本的な認証パターン・メール/パスワード・セッション取得の概要 | getting-started | [references/getting-started/README.md](references/getting-started/README.md) |
| auth.api・クライアント・セッション管理・Cookie・DB・フック・レートリミット | concepts | [references/concepts/README.md](references/concepts/README.md) |
| OAuth フロー・型安全性・プラグイン概念・動的ベース URL | concepts | [references/concepts/README.md](references/concepts/README.md) |
| Prisma / Drizzle / MongoDB / SQLite / PostgreSQL / MySQL 等の DB アダプター | adapters | [references/adapters/README.md](references/adapters/README.md) |
| コミュニティ製サードパーティ DB アダプター | adapters | [references/adapters/README.md](references/adapters/README.md) |
| Next.js / Nuxt / SvelteKit / Hono / Express / Fastify / Expo 等フレームワーク統合 | integrations | [references/integrations/README.md](references/integrations/README.md) |
| Astro / React Router / TanStack / Convex / Electron / NestJS 等の統合手順 | integrations | [references/integrations/README.md](references/integrations/README.md) |
| 公式ウォークスルー実例 (Astro, Next.js, Nuxt, React Router, SvelteKit) | examples | [references/examples/README.md](references/examples/README.md) |
| Email/Password 認証・ソーシャルログイン (GitHub, Google, Apple 等) | authentication | [references/authentication/README.md](references/authentication/README.md) |
| 特定ソーシャルプロバイダー (Discord, Microsoft, LINE, Twitter 等) の設定 | authentication | [references/authentication/README.md](references/authentication/README.md) |
| 2FA (TOTP)・パスキー・マジックリンク・SMS OTP・匿名認証 | plugins | [references/plugins/README.md](references/plugins/README.md) |
| Organization・Admin・SSO・SCIM・API Key・JWT・Bearer トークン | plugins | [references/plugins/README.md](references/plugins/README.md) |
| Stripe / Chargebee / Polar / Autumn 等の課金・サブスクリプション統合 | plugins | [references/plugins/README.md](references/plugins/README.md) |
| MCP 認証・エージェント認証・SIWE・キャプチャ・パスワード漏洩チェック | plugins | [references/plugins/README.md](references/plugins/README.md) |
| コミュニティ製プラグイン一覧を確認したい | plugins | [references/plugins/README.md](references/plugins/README.md) |
| OAuth 2.1 / OIDC プロバイダー構築・CIMD・DPoP | plugins | [references/plugins/README.md](references/plugins/README.md) |
| SCIM の groups・roles・reference | plugins | [references/plugins/README.md](references/plugins/README.md) |
| Effect HTTP server 統合 | integrations | [references/integrations/README.md](references/integrations/README.md) |
| Better Auth Infrastructure（有料。@better-auth/infra の dash / sentinel、audit logs、managed email / SMS） | infrastructure | [references/infrastructure/README.md](references/infrastructure/README.md) |
| 設定オプション一覧・セキュリティガイド・FAQ | reference | [references/reference/README.md](references/reference/README.md) |
| エラーコード調査・OpenTelemetry・テレメトリー | reference | [references/reference/README.md](references/reference/README.md) |
| コントリビューションガイド・コミュニティ動画/ブログ等のリソース集 | reference | [references/reference/README.md](references/reference/README.md) |
| 1.6 → 1.7 アップグレード・破壊的変更（npx auth upgrade） | guides | [references/guides/README.md](references/guides/README.md) |
| Auth.js (NextAuth) / Auth0 / Clerk / Supabase / WorkOS からの移行 | guides | [references/guides/README.md](references/guides/README.md) |
| カスタムプラグイン作成・カスタム DB アダプター作成・パフォーマンス最適化 | guides | [references/guides/README.md](references/guides/README.md) |
| SAML SSO (Okta)・ブラウザ拡張機能統合・動的ベース URL 詳細 | guides | [references/guides/README.md](references/guides/README.md) |
| 典型的な使い方・動作するコード例・フレームワーク別セットアップ断片 | samples | [samples/README.md](samples/README.md) |
| インストールコマンド・CLI コマンド・スキーマ生成を知りたい | scripts | [scripts/README.md](scripts/README.md) |
