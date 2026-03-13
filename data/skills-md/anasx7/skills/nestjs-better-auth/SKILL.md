---
name: nestjs-better-auth
description: Use when integrating Better Auth with NestJS applications - setting up authentication, route protection, guards, decorators, and hooks in NestJS
---

# NestJS Better Auth Integration

**Comprehensive integration of [Better Auth](https://www.better-auth.com/) for NestJS applications using [@thallesp/nestjs-better-auth](https://www.npmjs.com/package/@thallesp/nestjs-better-auth).**

**REQUIRED:** Better Auth >= 1.3.8. Older versions are unsupported.

---

## Quick Reference

| Package      | `@thallesp/nestjs-better-auth`             |
| ------------ | ------------------------------------------ |
| Install      | `npm install @thallesp/nestjs-better-auth` |
| Body Parser  | **MUST disable** in `main.ts`              |
| Global Guard | Enabled by default (all routes protected)  |
| Fastify      | Beta support - may have issues             |

---

## Setup

### 1. Disable Body Parser (Required)

```ts
// main.ts
import { NestFactory } from '@nestjs/core'
import { AppModule } from './app.module'

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    bodyParser: false, // Library re-adds default parsers automatically
  })
  await app.listen(process.env.PORT ?? 3333)
}
bootstrap()
```

### 2. Import AuthModule

```ts
// app.module.ts
import { Module } from '@nestjs/common'
import { AuthModule } from '@thallesp/nestjs-better-auth'
import { auth } from './auth'

@Module({
  imports: [AuthModule.forRoot({ auth })],
})
export class AppModule {}
```

---

## Module Options

```ts
AuthModule.forRoot({
  auth,
  disableTrustedOriginsCors: false, // Disable auto CORS for trustedOrigins
  disableBodyParser: false, // Handle body parsing manually
  disableGlobalAuthGuard: false, // Disable global guard (apply per route)
  disableControllers: false, // Handle routes manually
  middleware: (req, res, next) => {
    // Optional wrapper (e.g., MikroORM)
    RequestContext.create(orm.em, next)
  },
})
```

---

## Route Protection

**Default:** All routes protected globally. Use decorators to override:

| Decorator           | Effect                                              |
| ------------------- | --------------------------------------------------- |
| `@AllowAnonymous()` | No authentication required                          |
| `@OptionalAuth()`   | Auth optional, session may be null                  |

**Apply to class or method:**

```ts
@AllowAnonymous() // All routes in controller are public
@Controller('public')
export class PublicController {}

@Roles(['admin']) // All routes require admin role
@Controller('admin')
export class AdminController {}
```

### WebSocket Protection

Must manually apply `@UseGuards(AuthGuard)` at Gateway or Message level:

```ts
@WebSocketGateway({ path: '/ws', namespace: 'test' })
@UseGuards(AuthGuard)
export class TestGateway {}
```

---

## Decorators

### Session Access

```ts
import { Session, UserSession } from "@thallesp/nestjs-better-auth";

@Get("me")
async getProfile(@Session() session: UserSession) {
  return session;
}
```

### Role-Based Access Control

Use separate decorators for system-level and organization-level authorization:

| Decorator | Checks | Use Case |
| --------- | ------ | -------- |
| `@Roles([...])` | `user.role` only | System-level roles via Better Auth admin plugin |
| `@OrgRoles([...])` | Organization member role only | Org-scoped roles via Better Auth organization plugin |

**IMPORTANT:** These decorators are intentionally separate to prevent privilege escalation.
`@Roles()` checks only `user.role` (system roles) and does not check organization member roles.

#### `@Roles()` - System-Level Roles

Use for system-wide admin protection from Better Auth's admin plugin:

```ts
import { Controller, Get } from '@nestjs/common'
import { Roles } from '@thallesp/nestjs-better-auth'

@Controller('admin')
export class AdminController {
  @Roles(['admin'])
  @Get('dashboard')
  async adminDashboard() {
    // Requires user.role = 'admin'
    // Organization admins cannot access this route unless they are system admins
    return { message: 'System admin dashboard' }
  }
}

// Or as a class decorator
@Roles(['admin'])
@Controller('admin')
export class AdminRoutesController {}
```

#### `@OrgRoles()` - Organization-Level Roles

Use for org-scoped protection. Requires active organization context (`activeOrganizationId`):

```ts
import { Controller, Get } from '@nestjs/common'
import { OrgRoles, Session, UserSession } from '@thallesp/nestjs-better-auth'

@Controller('org')
export class OrgController {
  @OrgRoles(['owner', 'admin'])
  @Get('settings')
  async getOrgSettings(@Session() session: UserSession) {
    // Requires active org + member role owner/admin
    return { orgId: session.session.activeOrganizationId }
  }

  @OrgRoles(['owner'])
  @Get('billing')
  async getOrgBilling() {
    return { message: 'Billing settings' }
  }
}
```

Both decorators accept any role strings you define. Organization defaults are typically
`owner`, `admin`, and `member` unless customized in Better Auth organization plugin config.

### Request Object Access

```ts
@Get("me")
async getProfile(@Request() req: ExpressRequest) {
  return {
    session: req.session,  // Full session object
    user: req.user,        // User from session
  };
}
```

---

## AuthService

Inject to access Better Auth API with type safety:

```ts
import { AuthService } from '@thallesp/nestjs-better-auth'
import { fromNodeHeaders } from 'better-auth/node'
import { auth } from '../auth'

@Controller('users')
export class UsersController {
  constructor(private authService: AuthService<typeof auth>) {}

  @Get('accounts')
  async getAccounts(@Request() req: ExpressRequest) {
    return this.authService.api.listUserAccounts({
      headers: fromNodeHeaders(req.headers),
    })
  }

  @Post('api-keys')
  async createApiKey(@Request() req: ExpressRequest, @Body() body) {
    // Plugin methods (e.g., createApiKey) require AuthService<typeof auth>
    return this.authService.api.createApiKey({
      ...body,
      headers: fromNodeHeaders(req.headers),
    })
  }
}
```

---

## Hooks

**REQUIRED:** Set `hooks: {}` (empty object) in your Better Auth config to enable hook decorators.

```ts
// auth.ts
export const auth = betterAuth({
  basePath: '/api/auth',
  hooks: {}, // Minimum required for @Hook decorators
})
```

**Creating hooks:**

```ts
import { Injectable } from '@nestjs/common'
import {
  Hook,
  BeforeHook,
  AfterHook,
  AuthHookContext,
} from '@thallesp/nestjs-better-auth'

@Hook()
@Injectable()
export class SignUpHook {
  constructor(private readonly signUpService: SignUpService) {}

  @BeforeHook('/sign-up/email')
  async handle(ctx: AuthHookContext) {
    await this.signUpService.execute(ctx)
  }
}
```

**Register in module:**

```ts
@Module({
  imports: [AuthModule.forRoot({ auth })],
  providers: [SignUpHook, SignUpService],
})
export class AppModule {}
```

---

## Common Gotchas

1. **Body parser** - MUST disable in `main.ts` or requests fail
2. **Global guard** - All routes protected by default; use `@AllowAnonymous()` for public routes
3. **Hooks config** - `hooks: {}` required in Better Auth config for hook decorators
4. **WebSocket** - Global guard doesn't apply; manually add `@UseGuards(AuthGuard)`
5. **Plugin types** - Use `AuthService<typeof auth>` for type-safe plugin method access
6. **Fastify** - Beta support only; may have issues
7. **RBAC separation** - Use `@Roles()` for system roles and `@OrgRoles()` for org roles; do not mix assumptions between them

---

## Imports Summary

```ts
// Main imports
import {
  AuthModule,
  AuthService,
  AuthGuard,
} from '@thallesp/nestjs-better-auth'

// Decorators
import {
  Session,
  UserSession,
  AllowAnonymous,
  OptionalAuth,
  Roles,
  OrgRoles,
} from '@thallesp/nestjs-better-auth'

// Hooks
import {
  Hook,
  BeforeHook,
  AfterHook,
  AuthHookContext,
} from '@thallesp/nestjs-better-auth'
```

---

## Resources

- [npm Package](https://www.npmjs.com/package/@thallesp/nestjs-better-auth)
- [Better Auth Docs](https://www.better-auth.com/docs)
- [Better Auth MCP Skill](./better-auth-best-practices/SKILL.md)
