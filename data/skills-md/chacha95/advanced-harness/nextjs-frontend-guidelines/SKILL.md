---
name: nextjs-frontend-guidelines
description: Next.js 15 frontend development guidelines for YGS (영영사) React 19/TypeScript application. Modern patterns including App Router, Server/Client Components, shadcn/ui components, Tailwind CSS 4, multi-method authentication (Firebase/Kakao/JWT), admin dashboard patterns, and Korean localization. Use when creating components, pages, API routes, fetching data, styling, or working with frontend code.
---

# Next.js 15 Frontend Development Guidelines for YGS

## Purpose

Comprehensive guide for YGS (영영사) frontend development with Next.js 15, React 19, emphasizing App Router patterns, Server/Client component separation, shadcn/ui components, Tailwind CSS 4 styling, multi-method authentication, and Korean localization.

## When to Use This Skill

- Creating new components or pages
- Building new features with App Router
- Fetching data with Server Components or client-side patterns
- Styling components with shadcn/ui and Tailwind CSS 4
- Setting up API routes or Server Actions
- Authentication flows (Firebase, Kakao, custom JWT)
- Admin dashboard development
- Performance optimization
- Organizing frontend code
- TypeScript best practices

---

## Quick Start

### New Component Checklist

Creating a component? Follow this checklist:

- [ ] Determine if Server or Client Component
- [ ] Use `'use client'` directive only when needed
- [ ] Props type with TypeScript interface
- [ ] Use `@/` import alias for project imports
- [ ] Use shadcn/ui components where applicable
- [ ] Use `cn()` utility for conditional classes
- [ ] Named export for components
- [ ] Async Server Components for data fetching when possible
- [ ] Client Components for interactivity (useState, useEffect, event handlers)
- [ ] Korean text for UI labels

### New Feature Checklist

Creating a feature? Set up this structure:

- [ ] Create `src/components/{feature-name}/` directory
- [ ] Separate Server and Client components
- [ ] Create API route if needed: `src/app/api/{feature}/route.ts`
- [ ] Set up TypeScript types in `src/types/`
- [ ] Create route in `src/app/{feature-name}/page.tsx`
- [ ] Use Server Components by default
- [ ] Add Client Components only for interactivity
- [ ] Use Server Actions for mutations when appropriate
- [ ] Add constants/enums to `src/constants/enums.ts` if needed

---

## Project Structure

Your YGS project structure (import with `@/` alias):

```
src/
├── app/                        # Next.js App Router
│   ├── page.tsx                # Home/Landing page
│   ├── layout.tsx              # Root layout with metadata
│   ├── error.tsx               # Error boundary
│   ├── admin/                  # Admin dashboard (protected)
│   │   ├── page.tsx            # Dashboard stats
│   │   ├── layout.tsx          # Admin layout with auth check
│   │   ├── members/            # Member management
│   │   │   ├── page.tsx        # Member list
│   │   │   └── [id]/page.tsx   # Member detail
│   │   ├── consultations/      # Consultation management
│   │   ├── matching/           # Matching interface
│   │   └── couples/            # Couple management
│   ├── login/                  # Authentication
│   │   ├── page.tsx            # Login page
│   │   └── kakao-callback/     # Kakao OAuth callback
│   ├── form/                   # User profile form
│   ├── match/                  # Matching interface
│   ├── buy/                    # Membership purchase
│   └── api/
│       └── auth/session/       # Token sync endpoint
├── components/                 # React components (~60 total)
│   ├── admin/                  # Admin components (27)
│   │   ├── DashboardStats.tsx
│   │   ├── MemberTable.tsx
│   │   ├── MemberFilters.tsx
│   │   ├── ConsultationFormModal.tsx
│   │   └── modals/             # Edit modals
│   ├── auth/                   # Auth components (4)
│   │   ├── LoginForm.tsx
│   │   ├── SignupForm.tsx
│   │   └── SocialLoginButton.tsx
│   ├── layout/                 # Layout components (2)
│   │   ├── Navbar.tsx
│   │   └── Footer.tsx
│   ├── match/                  # Match components (3)
│   ├── sections/               # Landing page sections (7)
│   ├── seo/                    # SEO schema components (4)
│   └── ui/                     # shadcn/ui components (11)
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       ├── dialog.tsx
│       ├── select.tsx
│       └── ...
├── lib/                        # Core utilities
│   ├── api.ts                  # Main API client (token management)
│   ├── adminApi.ts             # Admin-specific API methods
│   ├── serverAuth.ts           # Server-side auth validation
│   ├── firebaseAuth.ts         # Firebase SDK integration
│   ├── firebase.ts             # Firebase config
│   ├── kakao.ts                # Kakao SDK integration
│   ├── s3Upload.ts             # S3 upload utilities
│   └── utils.ts                # cn() helper
├── providers/                  # Context providers
│   └── AuthProvider.tsx        # Auth state context
├── types/                      # TypeScript definitions
│   ├── index.ts                # Common types
│   ├── admin.ts                # Admin types (362 lines)
│   └── match.ts                # Match types
├── constants/                  # Constants & enums
│   └── enums.ts                # Enum options with Korean labels
└── middleware.ts               # Route protection
```

---

## Import Patterns

| Pattern | Usage | Example |
|---------|-------|---------|
| `@/` | Project imports (primary) | `import { api } from '@/lib/api'` |
| Relative | Same directory | `import { Component } from './Component'` |
| `type` | Type-only imports | `import type { User } from '@/types'` |

---

## Common Imports Cheatsheet

```typescript
// Server Component (no 'use client')
import { Suspense } from 'react';
import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { getServerSession } from '@/lib/serverAuth';
import type { Metadata } from 'next';

// Client Component
'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useAuth } from '@/providers/AuthProvider';
import { api } from '@/lib/api';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

// Admin API
import { getMembers, updateMemberBasic, getDashboardStats } from '@/lib/adminApi';

// Types
import type { AdminMember, MemberDetail, MemberFilter } from '@/types/admin';
import type { MatchCard } from '@/types/match';

// Constants
import { USER_STATUS_OPTIONS, GENDER_OPTIONS, getEnumLabel } from '@/constants/enums';
```

---

## Topic Guides

### shadcn/ui Overview

**What is shadcn/ui?**
- Beautifully designed, accessible components built on Radix UI
- Copy/paste components into your project (not a npm package dependency)
- Fully customizable with Tailwind CSS
- TypeScript-first with full type safety

**Key Concepts:**
- Components live in `src/components/ui/`
- Use `cn()` utility for class merging (clsx + tailwind-merge)
- Variants via class-variance-authority (cva)
- Follows Radix UI accessibility patterns

**Available Components in YGS:**
- button, input, textarea, card, dialog, select, checkbox, badge, alert, skeleton, image-upload

**Adding Components:**
```bash
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add dialog
npx shadcn@latest add form
```

---

### Component Patterns

**Server vs Client Components:**
- **Server Components (default)**: Data fetching, static content, no interactivity
- **Client Components ('use client')**: State, effects, event handlers, browser APIs

**Key Concepts:**
- Server Components are async and fetch data directly
- Client Components need 'use client' directive at the top
- Minimize Client Components for better performance
- Pass data from Server to Client Components via props
- Component structure: Props -> Hooks -> Handlers -> Render -> Export

**YGS-Specific Patterns:**
- Most admin components are Client Components (heavy state management)
- Landing page sections are Server Components (static content)
- Forms use manual state management (not react-hook-form)

**[Complete Guide: resources/component-patterns.md](resources/component-patterns.md)**

---

### Authentication (YGS-Specific)

**Multi-Method Authentication:**
1. **Firebase Social Auth**: Google, Apple
2. **Kakao OAuth**: Server-side token validation with Firebase exchange
3. **Custom JWT**: 60-min access token, 30-day refresh token

**AuthProvider Pattern:**
```typescript
'use client';

import { useAuth } from '@/providers/AuthProvider';

export function MyComponent() {
  const {
    user,
    isLoading,
    isAuthenticated,
    signupRequired,
    loginWithKakao,
    loginWithGoogle,
    logout,
    refreshUser,
  } = useAuth();

  if (isLoading) return <Loading />;
  if (!isAuthenticated) return <LoginPrompt />;

  return <div>Welcome, {user?.nickname}</div>;
}
```

**Server-Side Auth Check (Admin Layout):**
```typescript
// app/admin/layout.tsx
import { redirect } from 'next/navigation';
import { getServerSession } from '@/lib/serverAuth';

export default async function AdminLayout({ children }) {
  const session = await getServerSession();

  if (!session.isAuthenticated) {
    redirect('/login');
  }

  // Check admin claim from JWT
  const claims = parseJwtClaims(session.accessToken);
  if (!claims?.is_admin) {
    redirect('/');
  }

  return (
    <div className="flex min-h-screen">
      <AdminSidebar />
      <main className="flex-1">{children}</main>
    </div>
  );
}
```

**Hydration Protection Pattern:**
```typescript
'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/providers/AuthProvider';

export function Navbar() {
  const { user, isLoading, isAuthenticated } = useAuth();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <nav>
      {/* Always render static content */}
      <Logo />

      {/* Auth-dependent content only after mount */}
      {mounted && !isLoading ? (
        isAuthenticated ? <UserMenu user={user} /> : <LoginButton />
      ) : (
        <div className="w-[72px] h-10" /> // Placeholder
      )}
    </nav>
  );
}
```

---

### Data Fetching

**PRIMARY PATTERNS:**

**Server Component Data Fetching (Recommended):**
```typescript
// app/admin/page.tsx
import { getDashboardStats, getRegistrationTrend } from '@/lib/adminApi';

export default async function AdminDashboard() {
  const [stats, trend] = await Promise.all([
    getDashboardStats(),
    getRegistrationTrend(7),
  ]);

  return <DashboardStats stats={stats} trend={trend} />;
}
```

**Client-Side Data Fetching (Admin Pattern):**
```typescript
'use client';

import { useState, useEffect } from 'react';
import { getMembers } from '@/lib/adminApi';
import type { AdminMember, MemberFilter } from '@/types/admin';

export function MemberList() {
  const [members, setMembers] = useState<AdminMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchMembers() {
      try {
        setLoading(true);
        const response = await getMembers({ skip: 0, limit: 20 });
        setMembers(response.items);
      } catch (err) {
        setError(err instanceof Error ? err.message : '데이터를 불러오는데 실패했습니다.');
      } finally {
        setLoading(false);
      }
    }
    fetchMembers();
  }, []);

  if (loading) return <Skeleton />;
  if (error) return <Alert variant="destructive">{error}</Alert>;

  return <MemberTable members={members} />;
}
```

**[Complete Guide: resources/data-fetching.md](resources/data-fetching.md)**

---

### API Client Patterns

**Main API Client (`lib/api.ts`):**
```typescript
import { api } from '@/lib/api';

// Token management
import { getAccessToken, setTokens, clearTokens, hasTokens } from '@/lib/api';

// Auth methods
await api.post('/api/v1/auth/login', { phone, password });
await firebaseLogin(idToken);
await kakaoLogin(code, redirectUri);

// Generic methods
const data = await api.get<ResponseType>('/api/v1/endpoint');
await api.post('/api/v1/endpoint', body);
await api.patch('/api/v1/endpoint', changes);
```

**Admin API Client (`lib/adminApi.ts`):**
```typescript
import {
  // Dashboard
  getDashboardStats,
  getRegistrationTrend,
  getGenderRatio,
  getReferralStats,

  // Member Management
  getMembers,
  getMemberDetail,
  updateMemberBasic,
  updateMemberProfile,
  updateMemberLifestyle,
  updateMemberPreference,
  updateMemberSubscription,
  exportMembersToExcel,

  // Consultations
  getConsultations,
  createConsultation,
  updateConsultation,
  deleteConsultation,

  // Matching
  getCandidates,
  getCompatibilityScore,
} from '@/lib/adminApi';
```

---

### Constants & Enums Pattern

**Define in `constants/enums.ts`:**
```typescript
// constants/enums.ts
export const USER_STATUS_OPTIONS = [
  { value: "draft", label: "상담 전" },
  { value: "pending_review", label: "상담 예정" },
  { value: "active", label: "상담 완료" },
  { value: "suspended", label: "정지" },
  { value: "withdrawn", label: "탈퇴" },
] as const;

export const GENDER_OPTIONS = [
  { value: "male", label: "남성" },
  { value: "female", label: "여성" },
] as const;

// Helper functions
export function getEnumLabel(
  options: readonly { value: string; label: string }[],
  value: string | null | undefined
): string {
  if (!value) return "-";
  return options.find(o => o.value === value)?.label ?? value;
}

export function getUserStatusLabel(value: string | null | undefined): string {
  return getEnumLabel(USER_STATUS_OPTIONS, value);
}
```

**Usage in Components:**
```typescript
import { USER_STATUS_OPTIONS, getEnumLabel } from '@/constants/enums';

// In Select component
<Select value={status} onValueChange={setStatus}>
  <SelectTrigger>
    <SelectValue placeholder="상태 선택" />
  </SelectTrigger>
  <SelectContent>
    {USER_STATUS_OPTIONS.map(option => (
      <SelectItem key={option.value} value={option.value}>
        {option.label}
      </SelectItem>
    ))}
  </SelectContent>
</Select>

// Display label
<span>{getEnumLabel(USER_STATUS_OPTIONS, member.status)}</span>
```

---

### Form Patterns (YGS-Specific)

**Pattern 1: Manual State Management (Most Common in YGS):**
```typescript
'use client';

import { useState, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Loader2 } from 'lucide-react';

interface FormData {
  phone: string;
  name: string;
  gender: string;
  birthYear: string;
}

interface FormErrors {
  phone?: string;
  name?: string;
  gender?: string;
  birthYear?: string;
}

export function SignupForm() {
  const [formData, setFormData] = useState<FormData>({
    phone: '', name: '', gender: '', birthYear: ''
  });
  const [errors, setErrors] = useState<FormErrors>({});
  const [loading, setLoading] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};

    if (!/^010-\d{4}-\d{4}$/.test(formData.phone)) {
      newErrors.phone = "올바른 전화번호 형식이 아닙니다.";
    }
    if (formData.name.length < 2) {
      newErrors.name = "이름은 2자 이상이어야 합니다.";
    }
    if (!formData.gender) {
      newErrors.gender = "성별을 선택해주세요.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = useCallback((field: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  }, [errors]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    try {
      await api.post('/signup', formData);
    } catch (err) {
      setErrors({ ...errors, phone: "회원가입에 실패했습니다." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Input
          value={formData.phone}
          onChange={e => handleInputChange('phone', e.target.value)}
          placeholder="전화번호"
          className={cn(errors.phone && "border-red-500")}
        />
        {errors.phone && <p className="text-sm text-red-500">{errors.phone}</p>}
      </div>
      <Button type="submit" disabled={loading} className="w-full">
        {loading ? <Loader2 className="animate-spin mr-2 h-4 w-4" /> : null}
        {loading ? "처리 중..." : "가입하기"}
      </Button>
    </form>
  );
}
```

**Pattern 2: Modal Form (Admin Edit):**
```typescript
'use client';

import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { updateMemberBasic } from '@/lib/adminApi';
import type { MemberDetail } from '@/types/admin';

interface EditModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (member: MemberDetail) => void;
  member: MemberDetail;
}

export function BasicInfoEditModal({ isOpen, onClose, onSuccess, member }: EditModalProps) {
  const [formData, setFormData] = useState({ name: '', status: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (isOpen) {
      setFormData({ name: member.name, status: member.status });
      setError('');
    }
  }, [isOpen, member]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Only send changed fields
      const changes: Record<string, string> = {};
      if (formData.name !== member.name) changes.name = formData.name;
      if (formData.status !== member.status) changes.status = formData.status;

      if (Object.keys(changes).length === 0) {
        onClose();
        return;
      }

      const result = await updateMemberBasic(member.id, changes);
      onSuccess(result);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : '수정에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>기본 정보 수정</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            value={formData.name}
            onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
            placeholder="이름"
          />
          {error && <p className="text-sm text-red-500">{error}</p>}
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>취소</Button>
            <Button type="submit" disabled={loading}>
              {loading ? '저장 중...' : '저장'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
```

---

### URL-Based State Pattern (Pagination/Filtering)

```typescript
'use client';

import { useCallback } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import type { MemberFilter } from '@/types/admin';

export function useMemberFilters() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const filters: MemberFilter = {
    status: searchParams.get('status') || '',
    gender: searchParams.get('gender') || '',
    search: searchParams.get('search') || '',
    skip: Number(searchParams.get('skip')) || 0,
    limit: Number(searchParams.get('limit')) || 20,
  };

  const updateURL = useCallback((newFilters: Partial<MemberFilter>) => {
    const params = new URLSearchParams();
    const merged = { ...filters, ...newFilters };

    if (merged.status) params.set('status', merged.status);
    if (merged.gender) params.set('gender', merged.gender);
    if (merged.search) params.set('search', merged.search);
    if (merged.skip) params.set('skip', String(merged.skip));
    if (merged.limit !== 20) params.set('limit', String(merged.limit));

    router.push(`/admin/members${params.toString() ? `?${params}` : ''}`);
  }, [filters, router]);

  return { filters, updateURL };
}
```

---

### Styling

**shadcn/ui + Tailwind CSS 4:**
- Primary: shadcn/ui pre-built components with Tailwind
- Customization: Override with Tailwind utility classes
- Class merging: Use `cn()` utility for conditional classes

**cn() Utility (IMPORTANT):**
```typescript
import { cn } from '@/lib/utils';

// Conditional classes
<div className={cn(
  "flex items-center gap-2",
  isActive && "bg-primary text-white",
  isScrolled && "shadow-sm",
  className
)}>

// Status-based styling
const statusColors: Record<string, string> = {
  draft: "bg-slate-100 text-slate-600",
  active: "bg-green-100 text-green-700",
  suspended: "bg-red-100 text-red-600",
};

<Badge className={cn(statusColors[status] || "bg-gray-100")}>
  {getStatusLabel(status)}
</Badge>
```

**YGS Color System:**
```typescript
// Primary brand color (Coral/Orange)
className="bg-primary text-white"
className="hover:bg-primary-dark"
className="text-primary"

// Gradients
className="bg-gradient-to-r from-amber-500 to-orange-500"

// Status colors
className="text-red-500"     // Errors, destructive
className="bg-green-50"      // Success
className="text-gray-500"    // Muted
```

**Responsive Patterns:**
```typescript
// Grid
className="grid grid-cols-1 lg:grid-cols-4 gap-4"
className="grid grid-cols-2 lg:grid-cols-4 gap-4"

// Text
className="text-xl sm:text-2xl md:text-3xl lg:text-4xl"

// Display
className="hidden md:flex"   // Hidden on mobile
className="md:hidden"        // Mobile only

// Padding
className="px-4 sm:px-6 md:px-12"
```

**[Complete Guide: resources/styling-guide.md](resources/styling-guide.md)**

---

### File Organization

**App Router Structure:**
```
src/
  app/
    page.tsx              # Home page (/)
    layout.tsx            # Root layout
    {route}/
      page.tsx            # Route page
      layout.tsx          # Route layout (optional)
      loading.tsx         # Route loading
      error.tsx           # Route error
    api/
      {route}/
        route.ts          # API route handler
  components/
    ui/                   # shadcn/ui components
      button.tsx
      card.tsx
      input.tsx
    admin/                # Admin-specific components
      DashboardStats.tsx
      MemberTable.tsx
      modals/             # Edit modals
    {feature}/            # Feature-specific components
      Component.tsx
```

**Component Organization:**
- shadcn/ui components in `src/components/ui/`
- Feature components in `src/components/{feature}/`
- Admin components in `src/components/admin/`
- Keep Server and Client components separate

**[Complete Guide: resources/file-organization.md](resources/file-organization.md)**

---

### Loading & Error States

**App Router Conventions:**

**Loading:**
```typescript
// loading.tsx (route-level)
import { Skeleton } from '@/components/ui/skeleton';

export default function Loading() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-8 w-48" />
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <Skeleton key={i} className="h-24" />
        ))}
      </div>
    </div>
  );
}
```

**Error Handling (Korean):**
```typescript
// error.tsx (route-level)
'use client';

import { Button } from '@/components/ui/button';
import { AlertCircle } from 'lucide-react';

export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <AlertCircle className="h-12 w-12 text-destructive mb-4" />
      <h2 className="text-xl font-bold mb-2">오류가 발생했습니다</h2>
      <p className="text-muted-foreground mb-4">페이지를 불러오는 중 문제가 발생했습니다.</p>
      <Button onClick={reset}>다시 시도</Button>
    </div>
  );
}
```

**[Complete Guide: resources/loading-and-error-states.md](resources/loading-and-error-states.md)**

---

### Performance

**Next.js 15 Optimizations:**
- Server Components by default (zero JS to client)
- Dynamic imports: `const Heavy = dynamic(() => import('./Heavy'))`
- Image optimization: `next/image` component
- Font optimization: Built-in font loading
- Turbopack: Faster dev builds (already enabled)

**React 19 Patterns:**
- `useMemo`: Expensive computations
- `useCallback`: Event handlers passed to children
- `React.memo`: Prevent unnecessary re-renders

**[Complete Guide: resources/performance.md](resources/performance.md)**

---

### TypeScript

**Standards:**
- Strict mode enabled
- Explicit return types on functions
- Type imports: `import type { User } from '@/types'`
- Component prop interfaces with JSDoc
- No `any` type (use `unknown` if needed)

**YGS Type Patterns:**
```typescript
// types/admin.ts
interface AdminMember {
  id: string;
  name: string;
  gender: "male" | "female";
  phone: string;
  status: string;
  birth_year: number | null;
  created_at: string;
}

interface MemberDetail extends AdminMember {
  profile: UserProfile | null;
  lifestyle: UserLifestyle | null;
  preference: UserPreference | null;
  subscription: UserSubscription | null;
  documents: UserDocument[];
  photos: UserPhoto[];
}

// Update request types (partial)
interface BasicInfoUpdateRequest {
  name?: string;
  status?: string;
  is_admin?: boolean;
  birth_year?: number;
  gender?: "male" | "female";
}
```

**[Complete Guide: resources/typescript-standards.md](resources/typescript-standards.md)**

---

## Navigation Guide

| Need to... | Read this resource |
|------------|-------------------|
| Create a component | [component-patterns.md](resources/component-patterns.md) |
| Fetch data | [data-fetching.md](resources/data-fetching.md) |
| Organize files/folders | [file-organization.md](resources/file-organization.md) |
| Style components | [styling-guide.md](resources/styling-guide.md) |
| Set up routing | [routing-guide.md](resources/routing-guide.md) |
| Handle loading/errors | [loading-and-error-states.md](resources/loading-and-error-states.md) |
| Optimize performance | [performance.md](resources/performance.md) |
| TypeScript types | [typescript-standards.md](resources/typescript-standards.md) |
| Forms/Auth/API Routes | [common-patterns.md](resources/common-patterns.md) |
| See full examples | [complete-examples.md](resources/complete-examples.md) |

---

## Core Principles

1. **Server Components First**: Use Server Components by default, Client Components only for interactivity
2. **Async Data Fetching**: Fetch data directly in Server Components
3. **Minimize Client JS**: Less JavaScript sent to the browser = better performance
4. **App Router Conventions**: Use loading.tsx, error.tsx, layout.tsx appropriately
5. **shadcn/ui Components**: Use pre-built accessible components from `@/components/ui/`
6. **cn() for Classes**: Always use `cn()` for conditional/merged class names
7. **Import with @/ alias**: Consistent import paths across the project
8. **Type Safety**: Strict TypeScript with explicit types
9. **Korean Localization**: All user-facing text in Korean
10. **AuthProvider**: Use `useAuth()` hook for client-side auth state

---

## Quick Reference: Templates

### Server Component Template

```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { getDashboardStats } from '@/lib/adminApi';
import type { DashboardStats } from '@/types/admin';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: '대시보드 | YGS 관리자',
};

export default async function DashboardPage() {
  const stats: DashboardStats = await getDashboardStats();

  return (
    <div className="container py-8">
      <h1 className="text-2xl font-bold mb-6">대시보드</h1>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader>
            <CardTitle>전체 회원</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{stats.total_members}</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

### Client Component Template

```typescript
'use client';

import { useState, useCallback, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Skeleton } from '@/components/ui/skeleton';
import { getMembers } from '@/lib/adminApi';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';
import type { AdminMember } from '@/types/admin';

interface MemberListProps {
  className?: string;
}

export function MemberList({ className }: MemberListProps) {
  const [members, setMembers] = useState<AdminMember[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchMembers = useCallback(async () => {
    try {
      setLoading(true);
      const response = await getMembers({ skip: 0, limit: 20 });
      setMembers(response.items);
    } catch (err) {
      setError(err instanceof Error ? err.message : '데이터를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchMembers();
  }, [fetchMembers]);

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <Skeleton key={i} className="h-16 w-full" />
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500 mb-4">{error}</p>
        <Button onClick={fetchMembers}>다시 시도</Button>
      </div>
    );
  }

  return (
    <div className={cn("space-y-4", className)}>
      {members.map(member => (
        <div key={member.id} className="p-4 border rounded-lg">
          <p className="font-medium">{member.name}</p>
          <p className="text-sm text-muted-foreground">{member.phone}</p>
        </div>
      ))}
    </div>
  );
}
```

For complete examples, see [resources/complete-examples.md](resources/complete-examples.md)

---

## Related Skills

- **error-tracking**: Error tracking with Sentry (applies to frontend too)
- **fastapi-backend-guidelines**: Backend API patterns that frontend consumes

---

**Skill Status**: Updated for YGS project with comprehensive coverage of actual codebase patterns
