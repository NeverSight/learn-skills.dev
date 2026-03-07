---
name: error-boundary-creator
description: Create error boundaries, error handling, and fallback UIs for React applications. Use when implementing error handling, creating fallback components, or setting up error reporting.
---

# Error Boundary Creator

## Instructions

When implementing error handling:

1. **Identify error-prone areas** (async operations, third-party integrations)
2. **Create appropriate error boundaries**
3. **Design fallback UIs**
4. **Set up error reporting**

## Basic Error Boundary

```tsx
'use client';

import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Send to error reporting service
    // reportError(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || <DefaultErrorFallback error={this.state.error} />;
    }

    return this.props.children;
  }
}

function DefaultErrorFallback({ error }: { error?: Error }) {
  return (
    <div role="alert" className="p-4 bg-red-50 border border-red-200 rounded-lg">
      <h2 className="text-lg font-semibold text-red-800">Something went wrong</h2>
      <p className="text-red-600 mt-1">{error?.message || 'An unexpected error occurred'}</p>
      <button
        onClick={() => window.location.reload()}
        className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
      >
        Reload page
      </button>
    </div>
  );
}
```

## Error Boundary with Reset

```tsx
'use client';

import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  onReset?: () => void;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ResettableErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  reset = () => {
    this.props.onReset?.();
    this.setState({ hasError: false, error: undefined });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div role="alert" className="p-6 text-center">
          <h2 className="text-xl font-bold">Oops!</h2>
          <p className="text-gray-600 mt-2">{this.state.error?.message}</p>
          <button
            onClick={this.reset}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
          >
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## react-error-boundary Library

```tsx
import { ErrorBoundary, FallbackProps } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }: FallbackProps) {
  return (
    <div role="alert" className="p-4 bg-red-50 rounded-lg">
      <p className="font-medium">Something went wrong:</p>
      <pre className="text-sm text-red-600 mt-2">{error.message}</pre>
      <button onClick={resetErrorBoundary} className="mt-4 btn-primary">
        Try again
      </button>
    </div>
  );
}

// Usage
function App() {
  return (
    <ErrorBoundary
      FallbackComponent={ErrorFallback}
      onReset={() => {
        // Reset app state here
      }}
      onError={(error, info) => {
        // Log to error reporting service
        console.error(error, info);
      }}
    >
      <MyComponent />
    </ErrorBoundary>
  );
}
```

## Next.js Error Handling

### App Router error.tsx

```tsx
// app/error.tsx (or any route segment)
'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log error to reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px]">
      <h2 className="text-2xl font-bold">Something went wrong!</h2>
      <button
        onClick={reset}
        className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg"
      >
        Try again
      </button>
    </div>
  );
}
```

### Global Error (app/global-error.tsx)

```tsx
'use client';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <html>
      <body>
        <div className="flex flex-col items-center justify-center min-h-screen">
          <h2 className="text-2xl font-bold">Something went wrong!</h2>
          <button onClick={reset} className="mt-4 btn-primary">
            Try again
          </button>
        </div>
      </body>
    </html>
  );
}
```

### Not Found (app/not-found.tsx)

```tsx
import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px]">
      <h2 className="text-4xl font-bold">404</h2>
      <p className="text-gray-600 mt-2">Page not found</p>
      <Link href="/" className="mt-4 text-blue-600 hover:underline">
        Go home
      </Link>
    </div>
  );
}
```

## Async Error Handling

```tsx
'use client';

import { useState } from 'react';

interface AsyncState<T> {
  data: T | null;
  error: Error | null;
  isLoading: boolean;
}

function useAsync<T>() {
  const [state, setState] = useState<AsyncState<T>>({
    data: null,
    error: null,
    isLoading: false,
  });

  const execute = async (promise: Promise<T>) => {
    setState({ data: null, error: null, isLoading: true });
    try {
      const data = await promise;
      setState({ data, error: null, isLoading: false });
      return data;
    } catch (error) {
      setState({ data: null, error: error as Error, isLoading: false });
      throw error;
    }
  };

  return { ...state, execute };
}

// Usage
function DataComponent() {
  const { data, error, isLoading, execute } = useAsync<User[]>();

  const loadData = () => execute(fetchUsers());

  if (isLoading) return <Spinner />;
  if (error) return <ErrorMessage error={error} onRetry={loadData} />;
  if (!data) return <button onClick={loadData}>Load</button>;

  return <UserList users={data} />;
}
```

## Error Reporting Integration

```typescript
// lib/error-reporting.ts
export function reportError(error: Error, context?: Record<string, unknown>) {
  // Sentry
  // Sentry.captureException(error, { extra: context });

  // LogRocket
  // LogRocket.captureException(error);

  // Custom endpoint
  fetch('/api/errors', {
    method: 'POST',
    body: JSON.stringify({
      message: error.message,
      stack: error.stack,
      context,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      userAgent: navigator.userAgent,
    }),
  }).catch(console.error);
}
```

## Best Practices

1. **Wrap at route level** for page-level isolation
2. **Wrap third-party components** separately
3. **Provide meaningful fallbacks** with recovery options
4. **Log errors** to monitoring service
5. **Don't catch errors you can't handle**
6. **Test error states** in development
