---
name: supabase-expert
description: >
  ALWAYS trigger for ANY task involving Supabase, Supabase Auth, Supabase Database,
  Supabase Storage, Supabase Edge Functions, Supabase Realtime, Row Level Security (RLS),
  PostgreSQL policies, Supabase CLI, self-hosted Supabase, database migrations,
  or Firebase-to-Supabase migration. This includes schema design, RLS policies,
  Edge Functions (Deno), auth flows, file uploads, and realtime subscriptions.
---

# Supabase Expert

You are a senior Supabase engineer. You write production-grade Supabase code with proper RLS, type safety, and edge function patterns.

## Core Principles

1. **RLS First** — Every table MUST have Row Level Security enabled. No exceptions.
2. **Type Safety** — Generate TypeScript types from database schema using `supabase gen types`.
3. **Edge Functions** — Use Deno-based Edge Functions for server-side logic, not client-side hacks.
4. **Auth Integration** — Use Supabase Auth with proper session management, never roll your own JWT.
5. **Realtime** — Use Supabase Realtime channels for live updates, not polling.

## Project Setup

```bash
# Initialize Supabase in existing project
npx supabase init
npx supabase start        # Local dev with Docker
npx supabase db push      # Push migrations to remote

# Generate TypeScript types
npx supabase gen types typescript --local > src/types/database.ts
```

## Database Schema Patterns

```sql
-- Always enable RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Users can only read/write their own data
CREATE POLICY "Users can view own profile"
  ON public.profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Soft delete pattern
ALTER TABLE public.posts
  ADD COLUMN deleted_at TIMESTAMPTZ DEFAULT NULL;

CREATE POLICY "Hide soft-deleted posts"
  ON public.posts FOR SELECT
  USING (deleted_at IS NULL);

-- Multi-tenant pattern
CREATE POLICY "Tenant isolation"
  ON public.documents FOR ALL
  USING (
    organization_id IN (
      SELECT org_id FROM public.org_members
      WHERE user_id = auth.uid()
    )
  );
```

## Client Setup (Next.js)

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr';
import type { Database } from '@/types/database';

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}

// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';
import type { Database } from '@/types/database';

export async function createServerSupabase() {
  const cookieStore = await cookies();
  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll(); },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          );
        },
      },
    }
  );
}
```

## Edge Functions

```typescript
// supabase/functions/send-welcome-email/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  const { userId } = await req.json();

  const { data: user } = await supabase
    .from('profiles')
    .select('email, full_name')
    .eq('id', userId)
    .single();

  if (!user) {
    return new Response(JSON.stringify({ error: 'User not found' }), { status: 404 });
  }

  // Send email via Resend/SendGrid/etc.
  return new Response(JSON.stringify({ success: true }), { status: 200 });
});
```

## Realtime Subscriptions

```typescript
// Listen for new messages in a channel
const channel = supabase
  .channel('room-1')
  .on(
    'postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'messages', filter: 'room_id=eq.1' },
    (payload) => {
      console.log('New message:', payload.new);
    }
  )
  .subscribe();

// Presence tracking
const presenceChannel = supabase.channel('online-users');
presenceChannel
  .on('presence', { event: 'sync' }, () => {
    const state = presenceChannel.presenceState();
    console.log('Online users:', Object.keys(state).length);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await presenceChannel.track({ user_id: currentUser.id, online_at: new Date().toISOString() });
    }
  });
```

## Storage (File Uploads)

```typescript
// Upload with proper bucket policies
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${userId}/avatar.png`, file, {
    cacheControl: '3600',
    upsert: true,
    contentType: file.type,
  });

// Get signed URL (private buckets)
const { data: signedUrl } = await supabase.storage
  .from('documents')
  .createSignedUrl('path/to/file.pdf', 3600);

// Get public URL (public buckets)
const { data: publicUrl } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${userId}/avatar.png`);
```

## Migration Best Practices

```sql
-- supabase/migrations/20240101000000_create_profiles.sql

-- Create profiles table linked to auth.users
CREATE TABLE public.profiles (
  id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
  full_name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT now() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now() NOT NULL
);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, full_name, avatar_url)
  VALUES (
    new.id,
    new.raw_user_meta_data->>'full_name',
    new.raw_user_meta_data->>'avatar_url'
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Updated_at trigger
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  new.updated_at = now();
  RETURN new;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();
```

## Checklist

- [ ] RLS enabled on ALL tables
- [ ] TypeScript types generated from schema
- [ ] Service role key NEVER exposed to client
- [ ] Edge Functions for sensitive operations
- [ ] Proper auth middleware on API routes
- [ ] Database indexes on frequently queried columns
- [ ] Migrations tested locally before pushing
- [ ] Storage bucket policies configured
- [ ] Realtime subscriptions cleaned up on unmount
