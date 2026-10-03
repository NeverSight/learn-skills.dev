---
name: admin-guide
description: SaaS 어드민 대시보드 개발 가이드 - 관리자 기능 및 필수 로직
triggers:
  - admin
  - 어드민
  - 관리자
  - 대시보드
  - 사용자관리
---

# SaaS 어드민 대시보드 개발 가이드

> SaaS의 핵심 관리 기능 및 필수 비즈니스 로직 구현 가이드

---

## 1. 어드민 대시보드 구조

### 디렉토리 구조

```
src/
├── app/
│   ├── admin/
│   │   ├── layout.tsx          # 어드민 레이아웃
│   │   ├── page.tsx            # 대시보드 메인
│   │   ├── users/
│   │   │   ├── page.tsx        # 사용자 목록
│   │   │   └── [id]/page.tsx   # 사용자 상세
│   │   ├── analytics/
│   │   │   └── page.tsx        # 통계/분석
│   │   ├── subscriptions/
│   │   │   └── page.tsx        # 구독 관리
│   │   ├── content/
│   │   │   └── page.tsx        # 콘텐츠 관리
│   │   └── settings/
│   │       └── page.tsx        # 시스템 설정
│   └── api/
│       └── admin/
│           ├── users/route.ts
│           ├── analytics/route.ts
│           └── settings/route.ts
├── components/
│   └── admin/
│       ├── Sidebar.tsx
│       ├── Header.tsx
│       ├── StatsCard.tsx
│       ├── DataTable.tsx
│       └── Charts/
└── lib/
    └── admin/
        ├── auth.ts             # 어드민 인증
        ├── permissions.ts      # 권한 관리
        └── analytics.ts        # 통계 계산
```

---

## 2. 어드민 레이아웃

### 메인 레이아웃

```typescript
// src/app/admin/layout.tsx
import { redirect } from 'next/navigation';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';
import { AdminSidebar } from '@/components/admin/Sidebar';
import { AdminHeader } from '@/components/admin/Header';

export default async function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await getServerSession(authOptions);

  // 로그인 확인
  if (!session) {
    redirect('/login?callbackUrl=/admin');
  }

  // 어드민 권한 확인
  if (session.user.role !== 'ADMIN' && session.user.role !== 'SUPER_ADMIN') {
    redirect('/dashboard?error=unauthorized');
  }

  return (
    <div className="flex h-screen bg-gray-100">
      <AdminSidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <AdminHeader user={session.user} />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
```

---

## 3. 대시보드 메인

```typescript
// src/app/admin/page.tsx
import { StatsCard } from '@/components/admin/StatsCard';
import { RecentUsers } from '@/components/admin/RecentUsers';
import { RevenueChart } from '@/components/admin/Charts/RevenueChart';
import { getAdminStats } from '@/lib/admin/analytics';

export default async function AdminDashboard() {
  const stats = await getAdminStats();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">대시보드</h1>

      {/* 통계 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatsCard
          title="총 사용자"
          value={stats.totalUsers}
          change={stats.userGrowth}
          icon="users"
        />
        <StatsCard
          title="활성 구독"
          value={stats.activeSubscriptions}
          change={stats.subscriptionGrowth}
          icon="credit-card"
        />
        <StatsCard
          title="월 수익"
          value={`₩${stats.monthlyRevenue.toLocaleString()}`}
          change={stats.revenueGrowth}
          icon="dollar"
        />
        <StatsCard
          title="오늘 방문자"
          value={stats.todayVisitors}
          change={stats.visitorGrowth}
          icon="eye"
        />
      </div>

      {/* 차트 & 최근 활동 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <RevenueChart data={stats.revenueHistory} />
        </div>
        <div>
          <RecentUsers users={stats.recentUsers} />
        </div>
      </div>
    </div>
  );
}
```

---

## 4. 권한 관리 (RBAC)

### 역할 정의

```typescript
// src/lib/admin/permissions.ts
export type Role = 'USER' | 'MODERATOR' | 'ADMIN' | 'SUPER_ADMIN';

export type Permission =
  | 'users:read'
  | 'users:write'
  | 'users:delete'
  | 'subscriptions:read'
  | 'subscriptions:write'
  | 'content:read'
  | 'content:write'
  | 'content:delete'
  | 'analytics:read'
  | 'settings:read'
  | 'settings:write'
  | 'admin:access';

export const rolePermissions: Record<Role, Permission[]> = {
  USER: [],
  MODERATOR: [
    'content:read',
    'content:write',
    'users:read',
    'admin:access',
  ],
  ADMIN: [
    'users:read',
    'users:write',
    'subscriptions:read',
    'subscriptions:write',
    'content:read',
    'content:write',
    'content:delete',
    'analytics:read',
    'settings:read',
    'admin:access',
  ],
  SUPER_ADMIN: [
    'users:read',
    'users:write',
    'users:delete',
    'subscriptions:read',
    'subscriptions:write',
    'content:read',
    'content:write',
    'content:delete',
    'analytics:read',
    'settings:read',
    'settings:write',
    'admin:access',
  ],
};

export function hasPermission(role: Role, permission: Permission): boolean {
  return rolePermissions[role]?.includes(permission) ?? false;
}
```

---

## 5. 필수 비즈니스 로직

### 5.1 인증/인가

```typescript
// src/lib/auth.ts
import { NextAuthOptions } from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';
import CredentialsProvider from 'next-auth/providers/credentials';
import bcrypt from 'bcryptjs';

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        // 인증 로직
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.role = token.role as string;
      }
      return session;
    },
  },
};
```

### 5.2 결제 로직

```typescript
// src/lib/payment.ts
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function createCheckoutSession(
  userId: string,
  priceId: string,
  successUrl: string,
  cancelUrl: string
) {
  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: successUrl,
    cancel_url: cancelUrl,
    metadata: { userId },
  });

  return session;
}
```

### 5.3 Rate Limiting

```typescript
// src/lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

export const rateLimiters = {
  api: new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(60, '1 m'),
    prefix: 'ratelimit:api',
  }),
  login: new Ratelimit({
    redis,
    limiter: Ratelimit.slidingWindow(5, '5 m'),
    prefix: 'ratelimit:login',
  }),
};
```

### 5.4 입력 검증

```typescript
// src/lib/validation.ts
import { z } from 'zod';

export const userSchema = z.object({
  name: z.string().min(2).max(50),
  email: z.string().email(),
  password: z
    .string()
    .min(8)
    .regex(/[A-Z]/)
    .regex(/[0-9]/)
    .regex(/[^A-Za-z0-9]/),
});

export function validate<T>(schema: z.ZodSchema<T>, data: unknown): T {
  return schema.parse(data);
}
```

### 5.5 감사 로그

```typescript
// src/lib/audit.ts
import { prisma } from './prisma';

export async function createAuditLog(data: {
  action: string;
  userId?: string;
  targetId?: string;
  metadata?: Record<string, any>;
}) {
  return prisma.auditLog.create({
    data: {
      ...data,
      createdAt: new Date(),
    },
  });
}
```

---

## 6. 체크리스트

```
┌─────────────────────────────────────────────────────────────┐
│ 📋 어드민 개발 체크리스트                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ 🔐 인증/인가                                                  │
│ □ 어드민 로그인 구현                                         │
│ □ 역할 기반 접근 제어 (RBAC)                                 │
│ □ 권한 체크 미들웨어                                         │
│                                                              │
│ 👥 사용자 관리                                                │
│ □ 사용자 목록 (페이지네이션, 검색)                          │
│ □ 사용자 상세 정보                                           │
│ □ 사용자 생성/수정/삭제                                      │
│                                                              │
│ 💳 구독 관리                                                  │
│ □ 구독 현황 조회                                             │
│ □ 결제 내역                                                  │
│                                                              │
│ 📊 통계/분석                                                  │
│ □ 대시보드 통계 카드                                         │
│ □ 매출 차트                                                  │
│                                                              │
│ 🔒 보안                                                       │
│ □ Rate Limiting                                              │
│ □ 입력 검증                                                  │
│ □ 감사 로그                                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```
