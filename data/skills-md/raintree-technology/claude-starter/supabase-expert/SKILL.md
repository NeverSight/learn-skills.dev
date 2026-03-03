---
name: supabase-expert
description: Comprehensive Supabase expert with access to 2,616 official documentation files covering PostgreSQL database, authentication, real-time subscriptions, storage, edge functions, vector embeddings, and all platform features. Invoke when user mentions Supabase, PostgreSQL, database, auth, real-time, storage, edge functions, backend-as-a-service, or pgvector.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
model: sonnet
---

# Supabase Integration Expert

## Purpose

Provide comprehensive, accurate guidance for building applications with Supabase based on 2,616+ official documentation files. Cover all aspects of database operations, authentication, real-time features, file storage, edge functions, vector search, and platform integrations.

## Documentation Coverage

**Full access to official Supabase documentation (when available):**
- **Location:** `docs/supabase_com/`
- **Files:** 2,616 markdown files
- **Coverage:** Complete guides, API references, client libraries, and platform docs

**Note:** Documentation must be pulled separately:
```bash
pipx install docpull
docpull https://supabase.com/docs -o .claude/skills/supabase/docs
```

**Major Areas:**
- **Database:** PostgreSQL, Row Level Security (RLS), migrations, functions, triggers
- **Authentication:** Email/password, OAuth, magic links, SSO, MFA, phone auth
- **Real-time:** Database changes, broadcast, presence, channels
- **Storage:** File uploads, image transformations, CDN, buckets
- **Edge Functions:** Deno runtime, serverless, global deployment
- **Vector/AI:** pgvector, embeddings, semantic search, RAG
- **Client Libraries:** JavaScript, Python, Dart (Flutter), Swift, Kotlin
- **Platform:** CLI, local development, branching, observability
- **Integrations:** Next.js, React, Vue, Svelte, React Native, Expo

## When to Use

Invoke when user mentions:
- **Database:** PostgreSQL, Postgres, SQL, database, tables, queries, migrations
- **Auth:** authentication, login, signup, OAuth, SSO, multi-factor, magic links
- **Real-time:** real-time, subscriptions, websocket, live data, presence, broadcast
- **Storage:** file upload, file storage, images, S3, CDN, buckets
- **Functions:** edge functions, serverless, API, Deno, cloud functions
- **Security:** Row Level Security, RLS, policies, permissions, access control
- **AI/ML:** vector search, embeddings, pgvector, semantic search, AI, RAG
- **Framework Integration:** Next.js, React, Supabase client, hooks

## How to Use Documentation

When answering questions:

1. **Search for specific topics:**
   ```bash
   # Use Grep to find relevant docs
   grep -r "row level security" docs/supabase_com/ --include="*.md"
   ```

2. **Find guides:**
   ```bash
   # Guides are organized by feature
   ls docs/supabase_com/guides_*
   ```

3. **Check reference docs:**
   ```bash
   # Reference docs for client libraries
   ls docs/supabase_com/reference_*
   ```

## Quick Start

### Installation

```bash
npm install @supabase/supabase-js
```

### Initialize Client

```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

**Environment Variables:**
- `NEXT_PUBLIC_SUPABASE_URL` - Your project URL (safe for client)
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Anonymous/public key (safe for client)
- `SUPABASE_SERVICE_ROLE_KEY` - Admin key (server-side only, bypasses RLS)

## Database Operations

### CRUD Operations

```typescript
// Insert
const { data, error } = await supabase
  .from('posts')
  .insert({
    title: 'Hello World',
    content: 'My first post',
    user_id: user.id,
  })
  .select()
  .single();

// Read (with filters)
const { data: posts } = await supabase
  .from('posts')
  .select('*')
  .eq('published', true)
  .order('created_at', { ascending: false })
  .limit(10);

// Update
const { data, error } = await supabase
  .from('posts')
  .update({ published: true })
  .eq('id', postId)
  .select()
  .single();

// Delete
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId);

// Upsert (insert or update)
const { data, error } = await supabase
  .from('profiles')
  .upsert({
    id: user.id,
    name: 'John Doe',
    updated_at: new Date().toISOString(),
  })
  .select();
```

### Advanced Queries

```typescript
// Joins
const { data } = await supabase
  .from('posts')
  .select(`
    *,
    author:profiles(name, avatar),
    comments(count)
  `)
  .eq('published', true);

// Full-text search
const { data } = await supabase
  .from('posts')
  .select('*')
  .textSearch('title', `'nextjs' & 'supabase'`);

// Range queries
const { data } = await supabase
  .from('posts')
  .select('*')
  .gte('created_at', '2024-01-01')
  .lt('created_at', '2024-12-31');

// JSON queries
const { data } = await supabase
  .from('posts')
  .select('*')
  .contains('metadata', { tags: ['tutorial'] });
```

### Database Functions

```typescript
// Call stored procedure
const { data, error } = await supabase
  .rpc('get_user_stats', {
    user_id: userId,
  });

// Call with filters
const { data } = await supabase
  .rpc('search_posts', { search_term: 'supabase' })
  .limit(10);
```

## Authentication

### Sign Up / Sign In

```typescript
// Email/password signup
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
  options: {
    data: {
      first_name: 'John',
      last_name: 'Doe',
    },
  },
});

// Email/password sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'secure-password',
});

// Magic link (passwordless)
const { data, error } = await supabase.auth.signInWithOtp({
  email: 'user@example.com',
  options: {
    emailRedirectTo: 'https://example.com/auth/callback',
  },
});

// Phone/SMS
const { data, error } = await supabase.auth.signInWithOtp({
  phone: '+1234567890',
});
```

### OAuth Providers

```typescript
// Google sign in
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: 'http://localhost:3000/auth/callback',
    scopes: 'profile email',
  },
});
```

**Supported providers:**
- Google, GitHub, GitLab, Bitbucket
- Azure, Apple, Discord, Facebook
- Slack, Spotify, Twitch, Twitter/X
- Linear, Notion, Figma, and more

### User Session Management

```typescript
// Get current user
const { data: { user } } = await supabase.auth.getUser();

// Get session
const { data: { session } } = await supabase.auth.getSession();

// Sign out
const { error } = await supabase.auth.signOut();

// Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    console.log('User signed in:', session.user);
  }
  if (event === 'SIGNED_OUT') {
    console.log('User signed out');
  }
  if (event === 'TOKEN_REFRESHED') {
    console.log('Token refreshed');
  }
});
```

### Multi-Factor Authentication (MFA)

```typescript
// Enroll MFA
const { data, error } = await supabase.auth.mfa.enroll({
  factorType: 'totp',
  friendlyName: 'My Authenticator App',
});

// Verify MFA
const { data, error } = await supabase.auth.mfa.challengeAndVerify({
  factorId: data.id,
  code: '123456',
});

// List factors
const { data: factors } = await supabase.auth.mfa.listFactors();
```

## Row Level Security (RLS)

### Enable RLS

```sql
-- Enable RLS on table
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

### Create Policies

```sql
-- Public read access
CREATE POLICY "Posts are viewable by everyone"
  ON posts FOR SELECT
  USING (true);

-- Users can insert their own posts
CREATE POLICY "Users can create posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update only their posts
CREATE POLICY "Users can update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can delete only their posts
CREATE POLICY "Users can delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);

-- Conditional access (e.g., premium users)
CREATE POLICY "Premium content for premium users"
  ON posts FOR SELECT
  USING (
    NOT premium OR
    (auth.uid() IN (
      SELECT user_id FROM subscriptions
      WHERE status = 'active'
    ))
  );
```

### Helper Functions

```sql
-- Get current user ID
auth.uid()

-- Get current JWT
auth.jwt()

-- Access JWT claims
(auth.jwt()->>'role')::text
(auth.jwt()->>'email')::text
```

## Real-time Subscriptions

### Listen to Database Changes

```typescript
const channel = supabase
  .channel('posts-changes')
  .on(
    'postgres_changes',
    {
      event: '*', // or 'INSERT', 'UPDATE', 'DELETE'
      schema: 'public',
      table: 'posts',
    },
    (payload) => {
      console.log('Change received:', payload);
    }
  )
  .subscribe();

// Cleanup
channel.unsubscribe();
```

### Filter Real-time Events

```typescript
// Only listen to specific user's posts
const channel = supabase
  .channel('my-posts')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'posts',
      filter: `user_id=eq.${userId}`,
    },
    (payload) => {
      console.log('New post:', payload.new);
    }
  )
  .subscribe();
```

### Broadcast (Ephemeral Messages)

```typescript
const channel = supabase.channel('chat-room');

// Send message
await channel.send({
  type: 'broadcast',
  event: 'message',
  payload: { text: 'Hello!', user: 'John' },
});

// Receive messages
channel.on('broadcast', { event: 'message' }, (payload) => {
  console.log('Message:', payload.payload);
});

await channel.subscribe();
```

### Presence Tracking

```typescript
const channel = supabase.channel('room-1');

// Track presence
channel
  .on('presence', { event: 'sync' }, () => {
    const state = channel.presenceState();
    console.log('Online users:', Object.keys(state).length);
  })
  .on('presence', { event: 'join' }, ({ key, newPresences }) => {
    console.log('User joined:', newPresences);
  })
  .on('presence', { event: 'leave' }, ({ key, leftPresences }) => {
    console.log('User left:', leftPresences);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.track({
        user_id: userId,
        online_at: new Date().toISOString(),
      });
    }
  });
```

## Storage

### Upload Files

```typescript
const file = event.target.files[0];

const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`public/${userId}/avatar.png`, file, {
    cacheControl: '3600',
    upsert: true,
  });

// Upload from base64
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('file.png', decode(base64String), {
    contentType: 'image/png',
  });
```

### Download Files

```typescript
// Download as blob
const { data, error } = await supabase.storage
  .from('avatars')
  .download('public/avatar.png');

const url = URL.createObjectURL(data);
```

### Public URLs

```typescript
// Get public URL (for public buckets)
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('public/avatar.png');

console.log(data.publicUrl);
```

### Signed URLs (Private Files)

```typescript
// Create temporary access URL
const { data, error } = await supabase.storage
  .from('private-files')
  .createSignedUrl('document.pdf', 3600); // 1 hour

console.log(data.signedUrl);
```

### Image Transformations

```typescript
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('avatar.png', {
    transform: {
      width: 400,
      height: 400,
      resize: 'cover', // 'contain', 'cover', 'fill'
      quality: 80,
    },
  });
```

### List Files

```typescript
const { data, error } = await supabase.storage
  .from('avatars')
  .list('public', {
    limit: 100,
    offset: 0,
    sortBy: { column: 'created_at', order: 'desc' },
  });
```

## Edge Functions

### Create Function

```bash
# Install Supabase CLI
npm install -g supabase

# Initialize project
supabase init

# Create function
supabase functions new my-function
```

### Function Example

```typescript
// supabase/functions/my-function/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  try {
    // Initialize Supabase client
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_ANON_KEY')!,
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization')! },
        },
      }
    );

    // Get authenticated user
    const { data: { user }, error: authError } = await supabase.auth.getUser();

    if (authError || !user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Query database
    const { data: posts, error } = await supabase
      .from('posts')
      .select('*')
      .eq('user_id', user.id);

    if (error) throw error;

    return new Response(JSON.stringify({ posts }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
});
```

### Deploy Function

```bash
# Deploy single function
supabase functions deploy my-function

# Deploy all functions
supabase functions deploy
```

### Invoke Function

```typescript
const { data, error } = await supabase.functions.invoke('my-function', {
  body: { name: 'World' },
});

console.log(data);
```

## Vector Search (AI/ML)

### Enable pgvector

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with vector column
CREATE TABLE documents (
  id BIGSERIAL PRIMARY KEY,
  content TEXT,
  embedding VECTOR(1536) -- OpenAI ada-002 dimensions
);

-- Create HNSW index for fast similarity search
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

### Store Embeddings

```typescript
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

// Generate embedding
const response = await openai.embeddings.create({
  model: 'text-embedding-ada-002',
  input: 'Supabase is awesome',
});

const embedding = response.data[0].embedding;

// Store in database
const { data, error } = await supabase
  .from('documents')
  .insert({
    content: 'Supabase is awesome',
    embedding,
  });
```

### Similarity Search

```typescript
// Find similar documents
const { data, error } = await supabase.rpc('match_documents', {
  query_embedding: embedding,
  match_threshold: 0.78,
  match_count: 10,
});
```

**Similarity search function:**
```sql
CREATE FUNCTION match_documents (
  query_embedding VECTOR(1536),
  match_threshold FLOAT,
  match_count INT
)
RETURNS TABLE (
  id BIGINT,
  content TEXT,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

## Next.js Integration

### Server Components

```typescript
// app/posts/page.tsx
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';

export default async function PostsPage() {
  const supabase = createServerComponentClient({ cookies });

  const { data: posts } = await supabase
    .from('posts')
    .select('*')
    .order('created_at', { ascending: false });

  return (
    <div>
      {posts?.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  );
}
```

### Client Components

```typescript
// app/new-post/page.tsx
'use client';

import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';
import { useState } from 'react';

export default function NewPostPage() {
  const supabase = createClientComponentClient();
  const [title, setTitle] = useState('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const { error } = await supabase
      .from('posts')
      .insert({ title });

    if (error) console.error(error);
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

### Middleware (Auth Protection)

```typescript
// middleware.ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const supabase = createMiddlewareClient({ req, res });

  const { data: { session } } = await supabase.auth.getSession();

  // Redirect to login if not authenticated
  if (!session && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  return res;
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

### Route Handlers

```typescript
// app/api/posts/route.ts
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';

export async function GET() {
  const supabase = createRouteHandlerClient({ cookies });

  const { data: posts } = await supabase
    .from('posts')
    .select('*');

  return NextResponse.json({ posts });
}

export async function POST(request: Request) {
  const supabase = createRouteHandlerClient({ cookies });
  const body = await request.json();

  const { data, error } = await supabase
    .from('posts')
    .insert(body)
    .select()
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 400 });
  }

  return NextResponse.json({ post: data });
}
```

## Database Migrations

### Create Migration

```bash
supabase migration new create_posts_table
```

### Migration File Example

```sql
-- supabase/migrations/20241116000000_create_posts_table.sql

-- Create table
CREATE TABLE posts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES auth.users NOT NULL,
  title TEXT NOT NULL,
  content TEXT,
  published BOOLEAN DEFAULT false,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Public posts are viewable by everyone"
  ON posts FOR SELECT
  USING (published = true);

CREATE POLICY "Users can view their own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can create posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id);

-- Create indexes
CREATE INDEX posts_user_id_idx ON posts(user_id);
CREATE INDEX posts_created_at_idx ON posts(created_at DESC);
CREATE INDEX posts_published_idx ON posts(published) WHERE published = true;

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON posts
  FOR EACH ROW
  EXECUTE FUNCTION handle_updated_at();
```

### Run Migrations

```bash
# Apply migrations locally
supabase db reset

# Push to remote (production)
supabase db push
```

## TypeScript Integration

### Database Type Generation

```bash
# Generate types from your database schema
supabase gen types typescript --project-id YOUR_PROJECT_ID > types/supabase.ts

# Or from local development
supabase gen types typescript --local > types/supabase.ts
```

### Type-Safe Client

```typescript
// lib/supabase/types.ts
export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      posts: {
        Row: {
          id: string
          created_at: string
          title: string
          content: string | null
          user_id: string
          published: boolean
        }
        Insert: {
          id?: string
          created_at?: string
          title: string
          content?: string | null
          user_id: string
          published?: boolean
        }
        Update: {
          id?: string
          created_at?: string
          title?: string
          content?: string | null
          user_id?: string
          published?: boolean
        }
      }
      profiles: {
        Row: {
          id: string
          name: string | null
          avatar_url: string | null
          created_at: string
        }
        Insert: {
          id: string
          name?: string | null
          avatar_url?: string | null
          created_at?: string
        }
        Update: {
          id?: string
          name?: string | null
          avatar_url?: string | null
          created_at?: string
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
  }
}

// lib/supabase/client.ts
import { createClient } from '@supabase/supabase-js'
import { Database } from './types'

export const supabase = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Now you get full type safety!
const { data } = await supabase
  .from('posts')  // ✅ TypeScript knows this table exists
  .select('title, content, profiles(name)')  // ✅ TypeScript validates columns
  .eq('published', true)  // ✅ TypeScript validates types

// data is typed as:
// Array<{ title: string; content: string | null; profiles: { name: string | null } }>
```

### Server vs Client Supabase

```typescript
// lib/supabase/client.ts - Client-side (respects RLS)
import { createBrowserClient } from '@supabase/ssr'
import { Database } from './types'

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

// lib/supabase/server.ts - Server-side (Next.js App Router)
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { cookies } from 'next/headers'
import { Database } from './types'

export function createClient() {
  const cookieStore = cookies()

  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value, ...options })
          } catch (error) {
            // Called from Server Component - ignore
          }
        },
        remove(name: string, options: CookieOptions) {
          try {
            cookieStore.set({ name, value: '', ...options })
          } catch (error) {
            // Called from Server Component - ignore
          }
        },
      },
    }
  )
}

// lib/supabase/admin.ts - Admin client (bypasses RLS)
import { createClient } from '@supabase/supabase-js'
import { Database } from './types'

export const supabaseAdmin = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,  // ⚠️ Server-side only!
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
)
```

## Next.js App Router Patterns

### Server Components (Recommended)

```typescript
// app/posts/page.tsx
import { createClient } from '@/lib/supabase/server'

export default async function PostsPage() {
  const supabase = createClient()

  // Fetch data on server (no loading state needed!)
  const { data: posts } = await supabase
    .from('posts')
    .select('*, profiles(*)')
    .eq('published', true)
    .order('created_at', { ascending: false })

  return (
    <div>
      {posts?.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>By {post.profiles?.name}</p>
          <div>{post.content}</div>
        </article>
      ))}
    </div>
  )
}
```

### Server Actions for Mutations

```typescript
// app/actions/posts.ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'
import { redirect } from 'next/navigation'

export async function createPost(formData: FormData) {
  const supabase = createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    redirect('/login')
  }

  const title = formData.get('title') as string
  const content = formData.get('content') as string

  const { error } = await supabase
    .from('posts')
    .insert({
      title,
      content,
      user_id: user.id,
    })

  if (error) {
    throw new Error(error.message)
  }

  revalidatePath('/posts')
  redirect('/posts')
}

export async function updatePost(id: string, formData: FormData) {
  const supabase = createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('Unauthorized')

  const { error } = await supabase
    .from('posts')
    .update({
      title: formData.get('title') as string,
      content: formData.get('content') as string,
    })
    .eq('id', id)
    .eq('user_id', user.id)  // Ensure user owns the post

  if (error) throw new Error(error.message)

  revalidatePath('/posts')
}

export async function deletePost(id: string) {
  const supabase = createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('Unauthorized')

  const { error } = await supabase
    .from('posts')
    .delete()
    .eq('id', id)
    .eq('user_id', user.id)

  if (error) throw new Error(error.message)

  revalidatePath('/posts')
}
```

### Client Component with Real-time

```typescript
// app/components/PostsList.tsx
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { Database } from '@/lib/supabase/types'

type Post = Database['public']['Tables']['posts']['Row']

export function PostsList({ initialPosts }: { initialPosts: Post[] }) {
  const [posts, setPosts] = useState(initialPosts)
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase
      .channel('posts-changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'posts',
          filter: 'published=eq.true',
        },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setPosts(prev => [payload.new as Post, ...prev])
          } else if (payload.eventType === 'UPDATE') {
            setPosts(prev =>
              prev.map(post =>
                post.id === payload.new.id ? (payload.new as Post) : post
              )
            )
          } else if (payload.eventType === 'DELETE') {
            setPosts(prev => prev.filter(post => post.id !== payload.old.id))
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase])

  return (
    <div>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </article>
      ))}
    </div>
  )
}
```

### Route Handlers

```typescript
// app/api/posts/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const supabase = createClient()

  const { searchParams } = new URL(request.url)
  const limit = parseInt(searchParams.get('limit') || '10')

  const { data, error } = await supabase
    .from('posts')
    .select('*')
    .eq('published', true)
    .order('created_at', { ascending: false })
    .limit(limit)

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(data)
}

export async function POST(request: NextRequest) {
  const supabase = createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const body = await request.json()

  const { data, error } = await supabase
    .from('posts')
    .insert({
      ...body,
      user_id: user.id,
    })
    .select()
    .single()

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 })
  }

  return NextResponse.json(data)
}
```

## Advanced Authentication

### Email/Password with Email Confirmation

```typescript
// app/actions/auth.ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export async function signUp(formData: FormData) {
  const supabase = createClient()

  const email = formData.get('email') as string
  const password = formData.get('password') as string
  const name = formData.get('name') as string

  const { error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        name,  // Stored in auth.users.raw_user_meta_data
      },
      emailRedirectTo: `${process.env.NEXT_PUBLIC_URL}/auth/callback`,
    },
  })

  if (error) {
    return { error: error.message }
  }

  return { success: true, message: 'Check your email to confirm your account' }
}

export async function signIn(formData: FormData) {
  const supabase = createClient()

  const email = formData.get('email') as string
  const password = formData.get('password') as string

  const { error } = await supabase.auth.signInWithPassword({
    email,
    password,
  })

  if (error) {
    return { error: error.message }
  }

  redirect('/dashboard')
}

export async function signOut() {
  const supabase = createClient()
  await supabase.auth.signOut()
  redirect('/')
}
```

### OAuth (Google, GitHub, etc.)

```typescript
// app/actions/auth.ts
export async function signInWithGoogle() {
  const supabase = createClient()

  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${process.env.NEXT_PUBLIC_URL}/auth/callback`,
      queryParams: {
        access_type: 'offline',
        prompt: 'consent',
      },
    },
  })

  if (data?.url) {
    redirect(data.url)
  }
}

export async function signInWithGitHub() {
  const supabase = createClient()

  const { data } = await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: {
      redirectTo: `${process.env.NEXT_PUBLIC_URL}/auth/callback`,
      scopes: 'read:user user:email',
    },
  })

  if (data?.url) {
    redirect(data.url)
  }
}
```

### Magic Links

```typescript
export async function sendMagicLink(email: string) {
  const supabase = createClient()

  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: `${process.env.NEXT_PUBLIC_URL}/auth/callback`,
    },
  })

  if (error) {
    return { error: error.message }
  }

  return { success: true, message: 'Check your email for the login link' }
}
```

### Phone Auth (SMS)

```typescript
export async function sendPhoneOTP(phone: string) {
  const supabase = createClient()

  const { error } = await supabase.auth.signInWithOtp({
    phone,
  })

  if (error) {
    return { error: error.message }
  }

  return { success: true }
}

export async function verifyPhoneOTP(phone: string, token: string) {
  const supabase = createClient()

  const { error } = await supabase.auth.verifyOtp({
    phone,
    token,
    type: 'sms',
  })

  if (error) {
    return { error: error.message }
  }

  redirect('/dashboard')
}
```

### Multi-Factor Authentication (MFA)

```typescript
// Enable MFA for user
export async function enableMFA() {
  const supabase = createClient()

  const { data, error } = await supabase.auth.mfa.enroll({
    factorType: 'totp',
    friendlyName: 'Authenticator App',
  })

  if (error) throw error

  // data.totp.qr_code - QR code to scan
  // data.totp.secret - Secret to enter manually
  return data
}

// Verify MFA
export async function verifyMFA(factorId: string, code: string) {
  const supabase = createClient()

  const { data, error } = await supabase.auth.mfa.challengeAndVerify({
    factorId,
    code,
  })

  if (error) throw error
  return data
}
```

### Auth Callback Handler

```typescript
// app/auth/callback/route.ts
import { createClient } from '@/lib/supabase/server'
import { NextRequest, NextResponse } from 'next/server'

export async function GET(request: NextRequest) {
  const requestUrl = new URL(request.url)
  const code = requestUrl.searchParams.get('code')

  if (code) {
    const supabase = createClient()
    await supabase.auth.exchangeCodeForSession(code)
  }

  // Redirect to dashboard or wherever
  return NextResponse.redirect(new URL('/dashboard', request.url))
}
```

### Protected Routes

```typescript
// middleware.ts
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value,
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value,
            ...options,
          })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value: '',
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value: '',
            ...options,
          })
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Protect dashboard routes
  if (request.nextUrl.pathname.startsWith('/dashboard') && !user) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Redirect authenticated users away from auth pages
  if (request.nextUrl.pathname.startsWith('/login') && user) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return response
}

export const config = {
  matcher: ['/dashboard/:path*', '/login', '/signup'],
}
```

## Advanced Row Level Security

### Complex RLS Policies

```sql
-- Users can only see published posts or their own drafts
CREATE POLICY "Users can read appropriate posts"
  ON posts FOR SELECT
  USING (
    published = true
    OR
    auth.uid() = user_id
  );

-- Users can update only their own posts
CREATE POLICY "Users can update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Team-based access
CREATE TABLE teams (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL
);

CREATE TABLE team_members (
  team_id UUID REFERENCES teams,
  user_id UUID REFERENCES auth.users,
  role TEXT CHECK (role IN ('owner', 'admin', 'member')),
  PRIMARY KEY (team_id, user_id)
);

CREATE TABLE team_documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  team_id UUID REFERENCES teams,
  title TEXT,
  content TEXT
);

-- Only team members can see team documents
CREATE POLICY "Team members can view documents"
  ON team_documents FOR SELECT
  USING (
    team_id IN (
      SELECT team_id
      FROM team_members
      WHERE user_id = auth.uid()
    )
  );

-- Only team owners/admins can delete
CREATE POLICY "Team admins can delete documents"
  ON team_documents FOR DELETE
  USING (
    team_id IN (
      SELECT team_id
      FROM team_members
      WHERE user_id = auth.uid()
        AND role IN ('owner', 'admin')
    )
  );
```

### Function-Based RLS

```sql
-- Create helper function
CREATE OR REPLACE FUNCTION is_team_admin(team_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1
    FROM team_members
    WHERE team_members.team_id = is_team_admin.team_id
      AND team_members.user_id = auth.uid()
      AND team_members.role IN ('owner', 'admin')
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Use in policy
CREATE POLICY "Admins can update team settings"
  ON teams FOR UPDATE
  USING (is_team_admin(id))
  WITH CHECK (is_team_admin(id));
```

### RLS with JWT Claims

```sql
-- Access custom JWT claims
CREATE POLICY "Premium users can view premium content"
  ON premium_content FOR SELECT
  USING (
    (auth.jwt() -> 'user_metadata' ->> 'subscription_tier') = 'premium'
  );

-- Role-based access
CREATE POLICY "Admins have full access"
  ON sensitive_data FOR ALL
  USING (
    (auth.jwt() -> 'user_metadata' ->> 'role') = 'admin'
  );
```

## Advanced Real-time Features

### Presence (Who's Online)

```typescript
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export function OnlineUsers() {
  const [onlineUsers, setOnlineUsers] = useState<any[]>([])
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase.channel('online-users')

    channel
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState()
        const users = Object.values(state).flat()
        setOnlineUsers(users)
      })
      .on('presence', { event: 'join' }, ({ newPresences }) => {
        console.log('Users joined:', newPresences)
      })
      .on('presence', { event: 'leave' }, ({ leftPresences }) => {
        console.log('Users left:', leftPresences)
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          // Track this user
          const { data: { user } } = await supabase.auth.getUser()
          if (user) {
            await channel.track({
              user_id: user.id,
              email: user.email,
              online_at: new Date().toISOString(),
            })
          }
        }
      })

    return () => {
      supabase.removeChannel(channel)
    }
  }, [])

  return (
    <div>
      <h3>{onlineUsers.length} users online</h3>
      <ul>
        {onlineUsers.map((user, i) => (
          <li key={i}>{user.email}</li>
        ))}
      </ul>
    </div>
  )
}
```

### Broadcast (Send Messages)

```typescript
// Cursor tracking
export function CollaborativeCanvas() {
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase.channel('canvas')

    channel
      .on('broadcast', { event: 'cursor' }, (payload) => {
        // Update cursor position
        updateCursor(payload.payload)
      })
      .subscribe()

    // Send cursor position
    const handleMouseMove = (e: MouseEvent) => {
      channel.send({
        type: 'broadcast',
        event: 'cursor',
        payload: { x: e.clientX, y: e.clientY },
      })
    }

    window.addEventListener('mousemove', handleMouseMove)

    return () => {
      window.removeEventListener('mousemove', handleMouseMove)
      supabase.removeChannel(channel)
    }
  }, [])

  return <canvas />
}
```

### Postgres Changes (Database Events)

```typescript
// Listen to specific columns
const channel = supabase
  .channel('post-changes')
  .on(
    'postgres_changes',
    {
      event: 'UPDATE',
      schema: 'public',
      table: 'posts',
      filter: 'id=eq.123',  // Specific row
    },
    (payload) => {
      console.log('Post updated:', payload)
    }
  )
  .subscribe()

// Listen to multiple tables
const channel = supabase
  .channel('changes')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    handlePostChange
  )
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'comments' },
    handleCommentChange
  )
  .subscribe()
```

## Advanced Storage

### Image Transformations

```typescript
// Upload with transformation
export async function uploadAvatar(file: File, userId: string) {
  const supabase = createClient()

  const fileExt = file.name.split('.').pop()
  const fileName = `${userId}-${Date.now()}.${fileExt}`
  const filePath = `avatars/${fileName}`

  const { error: uploadError } = await supabase.storage
    .from('avatars')
    .upload(filePath, file, {
      cacheControl: '3600',
      upsert: false,
    })

  if (uploadError) throw uploadError

  // Get transformed image URL
  const { data } = supabase.storage
    .from('avatars')
    .getPublicUrl(filePath, {
      transform: {
        width: 200,
        height: 200,
        resize: 'cover',
        quality: 80,
      },
    })

  return data.publicUrl
}
```

### Signed URLs (Private Files)

```typescript
// Generate signed URL (expires after 1 hour)
export async function getPrivateFileUrl(path: string) {
  const supabase = createClient()

  const { data, error } = await supabase.storage
    .from('private-files')
    .createSignedUrl(path, 3600)  // 1 hour

  if (error) throw error

  return data.signedUrl
}

// Upload to private bucket
export async function uploadPrivateFile(file: File, userId: string) {
  const supabase = createClient()

  const filePath = `${userId}/${file.name}`

  const { error } = await supabase.storage
    .from('private-files')
    .upload(filePath, file)

  if (error) throw error

  return filePath
}
```

### Storage RLS

```sql
-- Enable RLS on storage.objects
CREATE POLICY "Users can upload to their own folder"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'avatars' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Users can view their own files"
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'avatars' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Users can update their own files"
  ON storage.objects FOR UPDATE
  USING (
    bucket_id = 'avatars' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );

CREATE POLICY "Users can delete their own files"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'avatars' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );
```

## Edge Functions

### Basic Edge Function

```typescript
// supabase/functions/hello/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

serve(async (req) => {
  const { name } = await req.json()

  return new Response(
    JSON.stringify({ message: `Hello ${name}!` }),
    {
      headers: { 'Content-Type': 'application/json' },
    },
  )
})
```

### Edge Function with Supabase Client

```typescript
// supabase/functions/create-post/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  try {
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization')! },
        },
      }
    )

    // Get authenticated user
    const { data: { user }, error: userError } = await supabaseClient.auth.getUser()
    if (userError || !user) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
      })
    }

    const { title, content } = await req.json()

    const { data, error } = await supabaseClient
      .from('posts')
      .insert({
        title,
        content,
        user_id: user.id,
      })
      .select()
      .single()

    if (error) throw error

    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
    })
  }
})
```

### Scheduled Edge Function (Cron)

```typescript
// supabase/functions/cleanup-old-data/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // Verify request is from Supabase Cron
  const authHeader = req.headers.get('Authorization')
  if (authHeader !== `Bearer ${Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')}`) {
    return new Response('Unauthorized', { status: 401 })
  }

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // Delete old data
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

  const { error } = await supabase
    .from('temporary_data')
    .delete()
    .lt('created_at', thirtyDaysAgo.toISOString())

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
    })
  }

  return new Response(JSON.stringify({ success: true }))
})

// Configure in Dashboard: Database > Cron Jobs
// Schedule: 0 2 * * * (2am daily)
// HTTP Request: https://your-project.supabase.co/functions/v1/cleanup-old-data
```

### Invoke Edge Function from Client

```typescript
// Client-side
const { data, error } = await supabase.functions.invoke('hello', {
  body: { name: 'World' },
})

// With auth headers automatically included
const { data: { session } } = await supabase.auth.getSession()

const { data, error } = await supabase.functions.invoke('create-post', {
  body: {
    title: 'My Post',
    content: 'Content here',
  },
  headers: {
    Authorization: `Bearer ${session?.access_token}`,
  },
})
```

## Vector Search (AI/RAG)

### Enable pgvector

```sql
-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with embedding column
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  content TEXT NOT NULL,
  metadata JSONB,
  embedding vector(1536),  -- For OpenAI ada-002 (1536 dimensions)
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for fast similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Or use HNSW for better performance (Postgres 15+)
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

### Generate and Store Embeddings

```typescript
// lib/embeddings.ts
import { OpenAI } from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!,
})

export async function generateEmbedding(text: string): Promise<number[]> {
  const response = await openai.embeddings.create({
    model: 'text-embedding-ada-002',
    input: text,
  })

  return response.data[0].embedding
}

// Store document with embedding
export async function storeDocument(content: string, metadata: any) {
  const supabase = createClient()

  const embedding = await generateEmbedding(content)

  const { data, error } = await supabase
    .from('documents')
    .insert({
      content,
      metadata,
      embedding,
    })
    .select()
    .single()

  if (error) throw error

  return data
}
```

### Semantic Search

```typescript
// Search similar documents
export async function searchSimilarDocuments(query: string, limit = 5) {
  const supabase = createClient()

  // Generate embedding for query
  const queryEmbedding = await generateEmbedding(query)

  // Search with RPC function
  const { data, error } = await supabase.rpc('match_documents', {
    query_embedding: queryEmbedding,
    match_threshold: 0.78,  // Minimum similarity
    match_count: limit,
  })

  if (error) throw error

  return data
}

// Create the RPC function
```

```sql
CREATE OR REPLACE FUNCTION match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  metadata JSONB,
  similarity float
)
LANGUAGE SQL STABLE
AS $$
  SELECT
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
$$;
```

### RAG (Retrieval Augmented Generation)

```typescript
export async function ragQuery(question: string) {
  // 1. Search for relevant documents
  const relevantDocs = await searchSimilarDocuments(question, 5)

  // 2. Build context from relevant documents
  const context = relevantDocs
    .map(doc => doc.content)
    .join('\n\n')

  // 3. Generate answer with GPT
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      {
        role: 'system',
        content: 'You are a helpful assistant. Answer questions based on the provided context.',
      },
      {
        role: 'user',
        content: `Context:\n${context}\n\nQuestion: ${question}`,
      },
    ],
  })

  return {
    answer: completion.choices[0].message.content,
    sources: relevantDocs,
  }
}
```

## Database Functions & Triggers

### Custom Functions

```sql
-- Get user's post count
CREATE OR REPLACE FUNCTION get_user_post_count(user_id UUID)
RETURNS INTEGER AS $$
  SELECT COUNT(*)::INTEGER
  FROM posts
  WHERE posts.user_id = get_user_post_count.user_id;
$$ LANGUAGE SQL STABLE;

-- Call from TypeScript
const { data, error } = await supabase.rpc('get_user_post_count', {
  user_id: userId,
})
```

### Triggers

```sql
-- Auto-update updated_at column
CREATE OR REPLACE FUNCTION handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON posts
  FOR EACH ROW
  EXECUTE FUNCTION handle_updated_at();

-- Update post count when post is created/deleted
CREATE OR REPLACE FUNCTION update_post_count()
RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    UPDATE profiles
    SET post_count = post_count + 1
    WHERE id = NEW.user_id;
    RETURN NEW;
  ELSIF TG_OP = 'DELETE' THEN
    UPDATE profiles
    SET post_count = post_count - 1
    WHERE id = OLD.user_id;
    RETURN OLD;
  END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_post_count_trigger
  AFTER INSERT OR DELETE ON posts
  FOR EACH ROW
  EXECUTE FUNCTION update_post_count();
```

## Performance Optimization

### Query Optimization

```typescript
// Bad: N+1 query problem
const { data: posts } = await supabase.from('posts').select('*')
for (const post of posts) {
  const { data: author } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', post.user_id)
    .single()
}

// Good: Join in single query
const { data: posts } = await supabase
  .from('posts')
  .select(`
    *,
    profiles (
      id,
      name,
      avatar_url
    )
  `)

// Good: Use specific columns
const { data: posts } = await supabase
  .from('posts')
  .select('id, title, created_at, profiles(name)')  // Only what you need
  .eq('published', true)
  .order('created_at', { ascending: false })
  .limit(20)
```

### Indexes

```sql
-- Index on frequently filtered columns
CREATE INDEX posts_user_id_idx ON posts(user_id);
CREATE INDEX posts_created_at_idx ON posts(created_at DESC);

-- Partial index (filtered)
CREATE INDEX posts_published_idx ON posts(published)
WHERE published = true;

-- Composite index
CREATE INDEX posts_user_published_idx ON posts(user_id, published, created_at DESC);

-- Full-text search index
CREATE INDEX posts_content_idx ON posts
USING GIN (to_tsvector('english', content));
```

### Connection Pooling

```typescript
// Use connection pooler for serverless (Supavisor)
// Connection string: postgresql://postgres.[project-ref]:[password]@aws-0-us-east-1.pooler.supabase.com:6543/postgres

import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!,
  {
    db: {
      schema: 'public',
    },
    global: {
      headers: { 'x-my-custom-header': 'my-app-name' },
    },
  }
)
```

### Caching

```typescript
// Next.js cache with revalidation
import { unstable_cache } from 'next/cache'
import { createClient } from '@/lib/supabase/server'

export const getCachedPosts = unstable_cache(
  async () => {
    const supabase = createClient()
    const { data } = await supabase
      .from('posts')
      .select('*')
      .eq('published', true)
    return data
  },
  ['posts'],
  {
    revalidate: 300,  // 5 minutes
    tags: ['posts'],
  }
)

// Revalidate on mutation
import { revalidateTag } from 'next/cache'

export async function createPost(data: any) {
  const supabase = createClient()
  await supabase.from('posts').insert(data)
  revalidateTag('posts')
}
```

## Local Development

### Setup Local Supabase

```bash
# Install Supabase CLI
brew install supabase/tap/supabase

# Initialize project
supabase init

# Start local Supabase (Docker required)
supabase start

# This starts:
# - PostgreSQL
# - GoTrue (Auth)
# - Realtime
# - Storage
# - Kong (API Gateway)
# - Studio (Dashboard)
```

### Local Development URLs

```bash
# After supabase start:
API URL: http://localhost:54321
Studio URL: http://localhost:54323
Inbucket URL: http://localhost:54324  # Email testing
```

### Migration Workflow

```bash
# Create migration
supabase migration new add_posts_table

# Edit migration file in supabase/migrations/

# Apply migration locally
supabase db reset

# Push to production
supabase db push

# Pull remote schema
supabase db pull
```

### Generate Types from Local DB

```bash
# Generate TypeScript types
supabase gen types typescript --local > types/database.ts
```

## Testing

### Testing RLS Policies

```sql
-- Test as specific user
SET LOCAL ROLE authenticated;
SET LOCAL "request.jwt.claims" TO '{"sub": "user-uuid-here"}';

-- Test query
SELECT * FROM posts;

-- Reset
RESET ROLE;
```

### Testing with Supabase Test Helpers

```typescript
// tests/posts.test.ts
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!  // For testing
)

describe('Posts', () => {
  beforeEach(async () => {
    // Clean up
    await supabase.from('posts').delete().neq('id', '00000000-0000-0000-0000-000000000000')
  })

  it('should create post', async () => {
    const { data, error } = await supabase
      .from('posts')
      .insert({ title: 'Test', content: 'Test' })
      .select()
      .single()

    expect(error).toBeNull()
    expect(data.title).toBe('Test')
  })
})
```

## Error Handling

### Comprehensive Error Handler

```typescript
import { PostgrestError } from '@supabase/supabase-js'

export function handleSupabaseError(error: PostgrestError | null) {
  if (!error) return null

  // Common error codes
  const errorMessages: Record<string, string> = {
    '23505': 'This record already exists',  // Unique violation
    '23503': 'Related record not found',    // Foreign key violation
    '42P01': 'Table does not exist',
    '42501': 'Permission denied',
    'PGRST116': 'No rows found',
  }

  const userMessage = errorMessages[error.code] || error.message

  console.error('Supabase error:', {
    code: error.code,
    message: error.message,
    details: error.details,
    hint: error.hint,
  })

  return userMessage
}

// Usage
const { data, error } = await supabase.from('posts').insert(postData)

if (error) {
  const message = handleSupabaseError(error)
  toast.error(message)
  return
}
```

## Best Practices

1. **Row Level Security:**
   - Enable RLS on ALL tables
   - Never rely on client-side checks alone
   - Test policies thoroughly
   - Use service role key sparingly (server-side only)

2. **Query Optimization:**
   - Use `.select()` to specify needed columns
   - Add database indexes for filtered/sorted columns
   - Use `.limit()` to cap results
   - Consider pagination for large datasets

3. **Real-time Subscriptions:**
   - Always unsubscribe when component unmounts
   - Use RLS policies to filter events
   - Use broadcast for ephemeral data
   - Limit number of simultaneous subscriptions

4. **Authentication:**
   - Store JWT in httpOnly cookies when possible
   - Refresh tokens before expiry
   - Handle auth state changes
   - Validate user on server-side

5. **Storage:**
   - Set appropriate bucket policies
   - Use image transformations for optimization
   - Consider storage limits
   - Clean up unused files

6. **Error Handling:**
   - Always check `error` object
   - Provide user-friendly error messages
   - Log errors for debugging
   - Handle network failures gracefully

## Common Patterns

### Auto-create Profile on Signup

```sql
-- Create profiles table
CREATE TABLE profiles (
  id UUID REFERENCES auth.users PRIMARY KEY,
  name TEXT,
  avatar_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trigger function
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, name, avatar_url)
  VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'name',
    NEW.raw_user_meta_data->>'avatar_url'
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

## Documentation Quick Reference

**Need to find something specific?**

Search the 2,616 documentation files:

```bash
# Search all docs
grep -r "search term" docs/supabase_com/

# Find guides
ls docs/supabase_com/guides_*

# Find API reference
ls docs/supabase_com/reference_*
```

**Common doc locations:**
- Guides: `docs/supabase_com/guides_*`
- JavaScript Reference: `docs/supabase_com/reference_javascript_*`
- Database: `docs/supabase_com/guides_database_*`
- Auth: `docs/supabase_com/guides_auth_*`
- Storage: `docs/supabase_com/guides_storage_*`

## Resources

- **Dashboard:** https://supabase.com/dashboard
- **Docs:** https://supabase.com/docs
- **Status:** https://status.supabase.com
- **CLI Docs:** https://supabase.com/docs/guides/cli

## Implementation Checklist

- [ ] Create Supabase project
- [ ] Install: `npm install @supabase/supabase-js`
- [ ] Set environment variables
- [ ] Design database schema
- [ ] Create migrations
- [ ] Enable RLS and create policies
- [ ] Set up authentication
- [ ] Implement auth state management
- [ ] Create CRUD operations
- [ ] Add real-time subscriptions (if needed)
- [ ] Configure storage buckets (if needed)
- [ ] Test RLS policies
- [ ] Add database indexes
- [ ] Deploy edge functions (if needed)
- [ ] Test in production
