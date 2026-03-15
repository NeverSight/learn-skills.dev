---
name: react-typescript-frontend
description: Build React TypeScript frontends with Mantine UI v8, Vite, and type-safe API integrations. Use when creating or modifying the Chuuk Dictionary frontend, building React components, or working with TypeScript in the frontend.
---

# React TypeScript Frontend

## Overview

Build and maintain the Chuuk Dictionary React frontend using TypeScript, Mantine UI v8, and Vite. Focuses on type-safe development, component patterns, and proper Chuukese text handling.

## Tech Stack

- **React 19**: Latest React with hooks and concurrent features
- **TypeScript 5.9**: Strict type checking
- **Mantine v8**: UI component library with dark mode
- **Vite 7**: Fast build tool and dev server
- **React Router v7**: Client-side routing
- **Axios**: HTTP client for API calls

## Project Structure

```text
frontend/
├── src/
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point with providers
│   ├── theme.ts             # Mantine theme configuration
│   ├── components/          # Reusable components
│   │   ├── Footer.tsx
│   │   └── GrammarLearning.tsx
│   ├── contexts/            # React contexts
│   ├── hooks/               # Custom hooks
│   ├── pages/               # Page components
│   ├── data/                # Static data
│   └── assets/              # Images, fonts
├── public/                  # Static assets
├── index.html               # HTML template
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript config
└── package.json
```

## Configuration

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### vite.config.ts

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5002',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});
```

## Component Patterns

### 1. Page Component

```tsx
// src/pages/DictionaryPage.tsx
import { useState, useEffect } from 'react';
import { Container, Title, TextInput, Stack, Loader, Alert } from '@mantine/core';
import { IconSearch, IconAlertCircle } from '@tabler/icons-react';
import { useDictionary } from '@/hooks/useDictionary';
import { DictionaryEntry } from '@/components/DictionaryEntry';

interface DictionaryPageProps {
  initialQuery?: string;
}

export function DictionaryPage({ initialQuery = '' }: DictionaryPageProps) {
  const [query, setQuery] = useState(initialQuery);
  const { entries, loading, error, search } = useDictionary();

  useEffect(() => {
    if (query.length >= 2) {
      search(query);
    }
  }, [query, search]);

  return (
    <Container size="lg" py="xl">
      <Title order={1} mb="lg">Chuukese Dictionary</Title>
      
      <TextInput
        placeholder="Search Chuukese or English..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        leftSection={<IconSearch size={16} />}
        size="lg"
        mb="xl"
        styles={{
          input: {
            fontFamily: "'Noto Sans', sans-serif",
          }
        }}
      />

      {error && (
        <Alert icon={<IconAlertCircle />} color="red" mb="md">
          {error}
        </Alert>
      )}

      {loading ? (
        <Loader />
      ) : (
        <Stack gap="md">
          {entries.map((entry) => (
            <DictionaryEntry key={entry._id} entry={entry} />
          ))}
        </Stack>
      )}
    </Container>
  );
}
```

### 2. Reusable Component

```tsx
// src/components/DictionaryEntry.tsx
import { Card, Text, Badge, Group, Stack } from '@mantine/core';

interface DictionaryEntryData {
  _id: string;
  chuukese_word: string;
  english_definition: string;
  part_of_speech?: string;
  grammar_type?: string;
  pronunciation?: string;
}

interface DictionaryEntryProps {
  entry: DictionaryEntryData;
  onClick?: (entry: DictionaryEntryData) => void;
}

export function DictionaryEntry({ entry, onClick }: DictionaryEntryProps) {
  return (
    <Card
      shadow="sm"
      padding="lg"
      radius="md"
      withBorder
      onClick={() => onClick?.(entry)}
      style={{ cursor: onClick ? 'pointer' : 'default' }}
    >
      <Group justify="space-between" mb="xs">
        <Text
          fw={600}
          size="xl"
          style={{ fontFeatureSettings: "'kern' 1" }}
        >
          {entry.chuukese_word}
        </Text>
        {entry.part_of_speech && (
          <Badge color="blue" variant="light">
            {entry.part_of_speech}
          </Badge>
        )}
      </Group>

      <Text c="dimmed" size="md">
        {entry.english_definition}
      </Text>

      {entry.pronunciation && (
        <Text size="sm" c="dimmed" mt="xs" fs="italic">
          /{entry.pronunciation}/
        </Text>
      )}
    </Card>
  );
}
```

### 3. Custom Hook

```tsx
// src/hooks/useDictionary.ts
import { useState, useCallback } from 'react';
import axios from 'axios';

interface DictionaryEntry {
  _id: string;
  chuukese_word: string;
  english_definition: string;
  part_of_speech?: string;
  grammar_type?: string;
}

interface UseDictionaryResult {
  entries: DictionaryEntry[];
  loading: boolean;
  error: string | null;
  search: (query: string) => Promise<void>;
  getEntry: (word: string) => Promise<DictionaryEntry | null>;
}

export function useDictionary(): UseDictionaryResult {
  const [entries, setEntries] = useState<DictionaryEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = useCallback(async (query: string) => {
    if (!query.trim()) {
      setEntries([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.get<{ entries: DictionaryEntry[] }>(
        `/api/dictionary/search`,
        { params: { query } }
      );
      setEntries(response.data.entries);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed');
      setEntries([]);
    } finally {
      setLoading(false);
    }
  }, []);

  const getEntry = useCallback(async (word: string): Promise<DictionaryEntry | null> => {
    try {
      const response = await axios.get<DictionaryEntry>(
        `/api/dictionary/entry/${encodeURIComponent(word)}`
      );
      return response.data;
    } catch {
      return null;
    }
  }, []);

  return { entries, loading, error, search, getEntry };
}
```

### 4. Context Provider

```tsx
// src/contexts/AuthContext.tsx
import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';

interface User {
  email: string;
  name: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (email: string) => Promise<void>;
  logout: () => Promise<void>;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await axios.get<User>('/api/auth/me');
      setUser(response.data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string) => {
    await axios.post('/api/auth/magic-link', { email });
  };

  const logout = async () => {
    await axios.post('/api/auth/logout');
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
```

## API Integration

### Axios Setup

```tsx
// src/api/client.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// Request interceptor
apiClient.interceptors.request.use((config) => {
  // Add any auth headers if needed
  return config;
});

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### Type-Safe API Calls

```tsx
// src/api/translation.ts
import apiClient from './client';

interface TranslationRequest {
  text: string;
  direction: 'chk_to_en' | 'en_to_chk';
}

interface TranslationResponse {
  original: string;
  translated: string;
  confidence: number;
  model_used: string;
}

export async function translate(request: TranslationRequest): Promise<TranslationResponse> {
  const response = await apiClient.post<TranslationResponse>('/translate', request);
  return response.data;
}

export async function translateBatch(
  texts: string[],
  direction: 'chk_to_en' | 'en_to_chk'
): Promise<TranslationResponse[]> {
  const response = await apiClient.post<TranslationResponse[]>('/translate/batch', {
    texts,
    direction,
  });
  return response.data;
}
```

## Chuukese Text Handling

### Font Configuration

```css
/* src/index.css */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&display=swap');

:root {
  font-family: 'Noto Sans', 'Arial Unicode MS', sans-serif;
}

/* Chuukese text styling */
.chuukese-text {
  font-family: 'Noto Sans', 'Arial Unicode MS', sans-serif;
  font-feature-settings: 'kern' 1, 'liga' 1;
  line-height: 1.6;
}
```

### Text Component with Accent Support

```tsx
// src/components/ChuukeseText.tsx
import { Text, TextProps } from '@mantine/core';

interface ChuukeseTextProps extends TextProps {
  children: React.ReactNode;
}

export function ChuukeseText({ children, ...props }: ChuukeseTextProps) {
  return (
    <Text
      {...props}
      style={{
        fontFamily: "'Noto Sans', 'Arial Unicode MS', sans-serif",
        fontFeatureSettings: "'kern' 1, 'liga' 1",
        ...props.style,
      }}
    >
      {children}
    </Text>
  );
}
```

## Routing

### Router Setup

```tsx
// src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { DictionaryPage } from './pages/DictionaryPage';
import { TranslationPage } from './pages/TranslationPage';
import { GrammarPage } from './pages/GrammarPage';
import { LoginPage } from './pages/LoginPage';
import { useAuth } from './contexts/AuthContext';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <LoadingScreen />;
  if (!isAuthenticated) return <Navigate to="/login" />;

  return <>{children}</>;
}

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<DictionaryPage />} />
          <Route path="translate" element={<TranslationPage />} />
          <Route path="grammar" element={<GrammarPage />} />
          <Route
            path="admin/*"
            element={
              <ProtectedRoute>
                <AdminRoutes />
              </ProtectedRoute>
            }
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

## Development Commands

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Type check
npx tsc --noEmit
```

## Best Practices

### TypeScript

1. **Enable strict mode**: Catch more errors at compile time
2. **Define interfaces**: Type all API responses and component props
3. **Avoid `any`**: Use proper types or `unknown`
4. **Use type guards**: Narrow types safely

### React

1. **Use functional components**: Hooks for all state management
2. **Memoize expensive operations**: `useMemo`, `useCallback`
3. **Split components**: Keep components focused and reusable
4. **Handle loading and error states**: Always show feedback

### Mantine

1. **Use theme tokens**: Don't hardcode colors or spacing
2. **Leverage built-in components**: Avoid custom implementations
3. **Use compound components**: Group related components logically
4. **Dark mode first**: Test in both color schemes

## Dependencies

```json
{
  "dependencies": {
    "@mantine/core": "^8.3.10",
    "@mantine/hooks": "^8.3.10",
    "@mantine/notifications": "^8.3.10",
    "@mantine/modals": "^8.3.10",
    "@tabler/icons-react": "^3.35.0",
    "axios": "^1.13.2",
    "react": "^19.2.0",
    "react-dom": "^19.2.0",
    "react-router-dom": "^7.10.1"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^5.1.1",
    "typescript": "~5.9.3",
    "vite": "^7.2.4"
  }
}
```
