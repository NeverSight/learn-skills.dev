---
name: git-city-3d-github-visualization
description: Build and extend Git City — a 3D pixel art city where GitHub profiles become interactive buildings using Next.js, Three.js, and Supabase.
triggers:
  - "add a feature to git city"
  - "work on the git city project"
  - "modify the 3d building renderer"
  - "add achievements to git city"
  - "customize git city buildings"
  - "set up git city locally"
  - "add a new building decoration"
  - "extend the github visualization"
---

# Git City — 3D GitHub Profile Visualization

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Git City transforms GitHub profiles into a 3D pixel art city. Each user becomes a unique building: height from contributions, width from repos, window brightness from stars. Built with Next.js 16 (App Router), React Three Fiber, and Supabase.

## Quick Setup

```bash
git clone https://github.com/srizzon/git-city.git
cd git-city
npm install

# Copy env template
cp .env.example .env.local   # Linux/macOS
copy .env.example .env.local  # Windows CMD
Copy-Item .env.example .env.local  # PowerShell

npm run dev
# → http://localhost:3001
```

## Environment Variables

Fill in `.env.local` after copying:

```bash
# Supabase — Project Settings → API
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# GitHub — Settings → Developer settings → Personal access tokens
GITHUB_TOKEN=github_pat_your_token_here

# Optional: comma-separated GitHub logins for /admin/ads access
ADMIN_GITHUB_LOGINS=your_github_login
```

**Finding Supabase values:** Dashboard → Project Settings → API  
**Finding GitHub token:** github.com → Settings → Developer settings → Personal access tokens (fine-grained recommended)

## Project Structure

```
git-city/
├── app/                    # Next.js App Router pages
│   ├── page.tsx            # Main city view
│   ├── [username]/         # User profile pages
│   ├── compare/            # Side-by-side compare mode
│   └── admin/              # Admin panel
├── components/
│   ├── city/               # 3D city scene components
│   │   ├── Building.tsx    # Individual building mesh
│   │   ├── CityScene.tsx   # Main R3F canvas/scene
│   │   └── LODManager.tsx  # Level-of-detail system
│   ├── ui/                 # 2D overlay UI components
│   └── profile/            # Profile page components
├── lib/
│   ├── github.ts           # GitHub API helpers
│   ├── supabase/           # Supabase client + server utils
│   ├── buildings.ts        # Building metric calculations
│   └── achievements.ts     # Achievement logic
├── hooks/                  # Custom React hooks
├── types/                  # TypeScript type definitions
└── public/                 # Static assets
```

## Core Concepts

### Building Metrics Mapping

Buildings are generated from GitHub profile data:

```typescript
// lib/buildings.ts pattern
interface BuildingMetrics {
  height: number;      // Based on total contributions
  width: number;       // Based on public repo count
  windowBrightness: number;  // Based on total stars received
  windowPattern: number[];   // Based on recent activity pattern
}

function calculateBuildingMetrics(profile: GitHubProfile): BuildingMetrics {
  const height = Math.log10(profile.totalContributions + 1) * 10;
  const width = Math.min(Math.ceil(profile.publicRepos / 10), 8);
  const windowBrightness = Math.min(profile.totalStars / 1000, 1);
  
  return { height, width, windowBrightness, windowPattern: [] };
}
```

### 3D Building Component (React Three Fiber)

```tsx
// components/city/Building.tsx pattern
import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface BuildingProps {
  position: [number, number, number];
  metrics: BuildingMetrics;
  username: string;
  isSelected?: boolean;
  onClick?: () => void;
}

export function Building({ position, metrics, username, isSelected, onClick }: BuildingProps) {
  const meshRef = useRef<THREE.Mesh>(null);
  
  // Animate selected building
  useFrame((state) => {
    if (meshRef.current && isSelected) {
      meshRef.current.rotation.y = Math.sin(state.clock.elapsedTime) * 0.05;
    }
  });

  return (
    <group position={position} onClick={onClick}>
      {/* Main building body */}
      <mesh ref={meshRef}>
        <boxGeometry args={[metrics.width, metrics.height, metrics.width]} />
        <meshStandardMaterial color="#1a1a2e" />
      </mesh>
      
      {/* Windows as instanced meshes for performance */}
      <WindowInstances metrics={metrics} />
    </group>
  );
}
```

### Instanced Meshes for Performance

Git City uses instanced rendering for windows — critical for a city with many buildings:

```tsx
// components/city/WindowInstances.tsx pattern
import { useRef, useEffect } from 'react';
import { InstancedMesh, Matrix4, Color } from 'three';

export function WindowInstances({ metrics }: { metrics: BuildingMetrics }) {
  const meshRef = useRef<InstancedMesh>(null);
  
  useEffect(() => {
    if (!meshRef.current) return;
    
    const matrix = new Matrix4();
    const color = new Color();
    let index = 0;
    
    // Calculate window positions based on building dimensions
    for (let floor = 0; floor < metrics.height; floor++) {
      for (let col = 0; col < metrics.width; col++) {
        const isLit = metrics.windowPattern[index] > 0.5;
        
        matrix.setPosition(col * 1.1 - metrics.width / 2, floor * 1.2, 0.51);
        meshRef.current.setMatrixAt(index, matrix);
        meshRef.current.setColorAt(
          index,
          color.set(isLit ? '#FFD700' : '#1a1a2e')
        );
        index++;
      }
    }
    
    meshRef.current.instanceMatrix.needsUpdate = true;
    if (meshRef.current.instanceColor) {
      meshRef.current.instanceColor.needsUpdate = true;
    }
  }, [metrics]);

  const windowCount = Math.floor(metrics.height) * metrics.width;
  
  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, windowCount]}>
      <planeGeometry args={[0.4, 0.5]} />
      <meshBasicMaterial />
    </instancedMesh>
  );
}
```

### GitHub API Integration

```typescript
// lib/github.ts pattern
import { Octokit } from '@octokit/rest';

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

export async function fetchGitHubProfile(username: string) {
  const [userResponse, reposResponse] = await Promise.all([
    octokit.users.getByUsername({ username }),
    octokit.repos.listForUser({ username, per_page: 100, sort: 'updated' }),
  ]);

  const totalStars = reposResponse.data.reduce(
    (sum, repo) => sum + (repo.stargazers_count ?? 0),
    0
  );

  return {
    username: userResponse.data.login,
    avatarUrl: userResponse.data.avatar_url,
    publicRepos: userResponse.data.public_repos,
    followers: userResponse.data.followers,
    totalStars,
  };
}

export async function fetchContributionData(username: string): Promise<number> {
  // Use GitHub GraphQL for contribution calendar data
  const query = `
    query($username: String!) {
      user(login: $username) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
  `;
  
  const response = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query, variables: { username } }),
  });
  
  const data = await response.json();
  return data.data.user.contributionsCollection.contributionCalendar.totalContributions;
}
```

### Supabase Integration

```typescript
// lib/supabase/server.ts pattern — server-side client
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export function createClient() {
  const cookieStore = cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (cookiesToSet) => {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          );
        },
      },
    }
  );
}

// lib/supabase/client.ts — browser client
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

### Achievement System

```typescript
// lib/achievements.ts pattern
export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  condition: (stats: UserStats) => boolean;
}

export const ACHIEVEMENTS: Achievement[] = [
  {
    id: 'first-commit',
    name: 'First Commit',
    description: 'Made your first contribution',
    icon: '🌱',
    condition: (stats) => stats.totalContributions >= 1,
  },
  {
    id: 'thousand-commits',
    name: 'Commit Crusher',
    description: '1,000+ total contributions',
    icon: '⚡',
    condition: (stats) => stats.totalContributions >= 1000,
  },
  {
    id: 'star-collector',
    name: 'Star Collector',
    description: 'Earned 100+ stars across repos',
    icon: '⭐',
    condition: (stats) => stats.totalStars >= 100,
  },
  {
    id: 'open-sourcer',
    name: 'Open Sourcer',
    description: '20+ public repositories',
    icon: '📦',
    condition: (stats) => stats.publicRepos >= 20,
  },
];

export function calculateAchievements(stats: UserStats): Achievement[] {
  return ACHIEVEMENTS.filter((achievement) => achievement.condition(stats));
}
```

### Adding a New Building Decoration

```typescript
// types/decorations.ts
export type DecorationSlot = 'crown' | 'aura' | 'roof' | 'face';

export interface Decoration {
  id: string;
  slot: DecorationSlot;
  name: string;
  price: number;
  component: React.ComponentType<DecorationProps>;
}

// components/city/decorations/Crown.tsx
export function CrownDecoration({ position, buildingWidth }: DecorationProps) {
  return (
    <group position={[position[0], position[1], position[2]]}>
      <mesh>
        <coneGeometry args={[buildingWidth / 3, 2, 4]} />
        <meshStandardMaterial color="#FFD700" metalness={0.8} roughness={0.2} />
      </mesh>
    </group>
  );
}

// Register in decoration registry
export const DECORATIONS: Decoration[] = [
  {
    id: 'golden-crown',
    slot: 'crown',
    name: 'Golden Crown',
    price: 500,
    component: CrownDecoration,
  },
];
```

### Camera / Flight Controls

```tsx
// components/city/CameraController.tsx pattern
import { useThree, useFrame } from '@react-three/fiber';
import { useRef } from 'react';
import * as THREE from 'three';

export function CameraController() {
  const { camera } = useThree();
  const targetRef = useRef(new THREE.Vector3());
  const velocityRef = useRef(new THREE.Vector3());

  useFrame((_, delta) => {
    // Smooth lerp camera toward target
    camera.position.lerp(targetRef.current, delta * 2);
  });

  // Expose flyTo function via context or ref
  const flyTo = (position: THREE.Vector3) => {
    targetRef.current.copy(position).add(new THREE.Vector3(0, 10, 20));
  };

  return null;
}
```

### Server Actions (Next.js App Router)

```typescript
// app/actions/kudos.ts
'use server';

import { createClient } from '@/lib/supabase/server';
import { revalidatePath } from 'next/cache';

export async function sendKudos(toUsername: string) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  
  if (!user) throw new Error('Must be logged in to send kudos');

  const { error } = await supabase.from('kudos').insert({
    from_user_id: user.id,
    to_username: toUsername,
    created_at: new Date().toISOString(),
  });

  if (error) throw error;
  
  revalidatePath(`/${toUsername}`);
}
```

### Profile Page Route

```tsx
// app/[username]/page.tsx pattern
import { fetchGitHubProfile } from '@/lib/github';
import { createClient } from '@/lib/supabase/server';
import { calculateAchievements } from '@/lib/achievements';
import { BuildingPreview } from '@/components/profile/BuildingPreview';

interface Props {
  params: { username: string };
}

export default async function ProfilePage({ params }: Props) {
  const { username } = params;
  
  const [githubProfile, supabase] = await Promise.all([
    fetchGitHubProfile(username),
    createClient(),
  ]);

  const { data: cityProfile } = await supabase
    .from('profiles')
    .select('*, decorations(*)')
    .eq('username', username)
    .single();

  const achievements = calculateAchievements({
    totalContributions: githubProfile.totalContributions,
    totalStars: githubProfile.totalStars,
    publicRepos: githubProfile.publicRepos,
  });

  return (
    <main>
      <BuildingPreview profile={githubProfile} cityProfile={cityProfile} />
      <AchievementGrid achievements={achievements} />
    </main>
  );
}

export async function generateMetadata({ params }: Props) {
  return {
    title: `${params.username} — Git City`,
    description: `View ${params.username}'s building in Git City`,
    openGraph: {
      images: [`/api/og/${params.username}`],
    },
  };
}
```

## Common Development Patterns

### LOD (Level of Detail) System

```typescript
// Simplified LOD pattern used in the city
import { useThree } from '@react-three/fiber';

export function useLOD(buildingPosition: THREE.Vector3) {
  const { camera } = useThree();
  const distance = camera.position.distanceTo(buildingPosition);
  
  if (distance < 50) return 'high';    // Full detail + animated windows
  if (distance < 150) return 'medium'; // Simplified windows
  return 'low';                        // Box only
}
```

### Fetching with SWR in City View

```tsx
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(r => r.json());

export function useCityBuildings() {
  const { data, error, isLoading } = useSWR('/api/buildings', fetcher, {
    refreshInterval: 30000, // refresh every 30s for live activity feed
  });
  
  return { buildings: data, error, isLoading };
}
```

## Key API Routes

| Route | Purpose |
|-------|---------|
| `GET /api/buildings` | Fetch all city buildings with positions |
| `GET /api/profile/[username]` | GitHub + city profile data |
| `POST /api/kudos` | Send kudos to a user |
| `GET /api/og/[username]` | Generate OG share card image |
| `POST /api/webhook/stripe` | Stripe payment webhook |
| `GET /admin/ads` | Admin panel (requires `ADMIN_GITHUB_LOGINS`) |

## Troubleshooting

**3D scene not rendering**  
Check that `@react-three/fiber` and `three` versions are compatible. The canvas needs a height set on its container div.

**GitHub API rate limits**  
Use a fine-grained token with appropriate scopes. The app caches GitHub responses in Supabase to avoid repeated API calls.

**Supabase auth not working locally**  
Configure the GitHub OAuth provider in your Supabase project and ensure your local callback URL (`http://localhost:3001/auth/callback`) is allowlisted.

**Buildings not appearing**  
Check that Supabase Row Level Security policies allow reads on the `profiles` and `buildings` tables for anonymous users.

**Window shimmer/flicker**  
This is usually a Z-fighting issue. Add a tiny offset (`0.001`) to window mesh positions along the normal axis.

**Performance issues with many buildings**  
Ensure instanced meshes are used for windows and the LOD system is active. Avoid creating new `THREE.Material` instances inside render loops — define them outside components or use `useMemo`.

## Stack Reference

| Layer | Technology |
|-------|-----------|
| Framework | Next.js 16 (App Router, Turbopack) |
| 3D Rendering | Three.js + @react-three/fiber + drei |
| Database | Supabase (PostgreSQL + RLS) |
| Auth | Supabase GitHub OAuth |
| Payments | Stripe |
| Styling | Tailwind CSS v4 + Silkscreen font |
| Hosting | Vercel |
| License | AGPL-3.0 |
