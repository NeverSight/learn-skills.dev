---
name: data-fetching-patterns
description: Explains data fetching strategies including fetch on render, fetch then render, render as you fetch, and server-side data fetching. Use when implementing data loading, optimizing loading performance, or choosing between client and server data fetching.
---

# Data Fetching Patterns

## Overview

Data fetching is how your application retrieves data from APIs or databases. The pattern you choose affects performance, user experience, and code complexity.

## Fetching Locations

| Where | When Executed | Use Case |
|-------|---------------|----------|
| Server (build) | Build time | Static content (SSG) |
| Server (request) | Each request | Dynamic content (SSR) |
| Client (browser) | After hydration | Interactive, real-time |
| Edge | At CDN edge | Personalization, A/B tests |

## Client-Side Patterns

### 1. Fetch on Render (Waterfall)

Components fetch data when they mount.

```jsx
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]);
  
  if (!user) return <Loading />;
  return <Profile user={user} />;
}
```

**Timeline:**

```
Component renders → useEffect runs → Fetch starts → Data arrives → Re-render
                    [-- Waiting --]                 [-- Display --]
```

**Problem: Waterfalls**

```jsx
function Dashboard() {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser().then(setUser);  // Fetch 1
  }, []);
  
  if (!user) return <Loading />;
  
  return (
    <UserPosts userId={user.id} />  // Fetch 2 starts AFTER Fetch 1 completes
  );
}

// Timeline:
// [Fetch User]───────►[Fetch Posts]───────►Display
//                     ↑ Can't start until user loads (waterfall)
```

### 2. Fetch Then Render

Fetch all data before rendering any component.

```jsx
function Dashboard() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    Promise.all([fetchUser(), fetchPosts(), fetchStats()])
      .then(([user, posts, stats]) => setData({ user, posts, stats }));
  }, []);
  
  if (!data) return <Loading />;
  
  return (
    <>
      <UserInfo user={data.user} />
      <Posts posts={data.posts} />
      <Stats stats={data.stats} />
    </>
  );
}
```

**Timeline:**

```
[Fetch User  ]
[Fetch Posts ]──►All Complete───►Render All
[Fetch Stats ]
              ↑ Parallel, but wait for slowest
```

**Problem:** All-or-nothing loading. Fast data waits for slow data.

### 3. Render as You Fetch (Concurrent)

Start fetching immediately, render components as data arrives.

```jsx
// Start fetches immediately (not in useEffect)
const userPromise = fetchUser();
const postsPromise = fetchPosts();

function Dashboard() {
  return (
    <Suspense fallback={<UserSkeleton />}>
      <UserInfo userPromise={userPromise} />
    </Suspense>
    <Suspense fallback={<PostsSkeleton />}>
      <Posts postsPromise={postsPromise} />
    </Suspense>
  );
}

// Each component renders when its data is ready
function UserInfo({ userPromise }) {
  const user = use(userPromise);  // React 19's use() hook
  return <div>{user.name}</div>;
}
```

**Timeline:**

```
[Fetch User  ]───►Render User
[Fetch Posts ]─────────►Render Posts
              ↑ Independent, progressive rendering
```

## Server-Side Patterns

### Server Data Fetching (SSR)

Data fetched on server before sending HTML:

```javascript
// Next.js App Router
async function ProductPage({ params }) {
  const product = await db.products.findById(params.id);  // Runs on server
  return <ProductDetails product={product} />;
}
```

**Benefits:**
- No loading state (data already in HTML)
- SEO-friendly (content in initial HTML)
- Direct database/API access

### Parallel Data Fetching

Fetch multiple resources simultaneously:

```javascript
// Bad: Sequential (waterfall)
const user = await getUser();
const posts = await getPosts(user.id);
const comments = await getComments(posts[0].id);

// Good: Parallel where possible
const [user, stats] = await Promise.all([
  getUser(),
  getStats(),
]);
// Then sequential for dependent data
const posts = await getPosts(user.id);
```

### Streaming and Suspense

Stream HTML to the browser as soon as each part of your UI is ready—even if it's out of order—letting users see content without having to wait for everything.

- **Progressive & Out-of-Order Streaming:** With React's server components and Suspense, the server can send parts of the page (like headers or footers) immediately, even if other parts (like a slow data section) are still loading. This means sections of your UI don't have to stream in their coded order—each streams independently as soon as its data is ready.
- **Suspense Boundaries & Placeholders:** The `<Suspense>` boundary tells React where some data may take longer. While waiting, a fallback component (such as `<Loading />`) is sent as a placeholder in the HTML.
- **Client-Side JS Swapping:** Along with the initial HTML and placeholders, React also sends a small client-side JavaScript "runtime" that listens for streamed content. When the slow component's data arrives from the server, this client JS automatically swaps out the placeholder fallback for the real content—right in place, without a full page reload.

```jsx
// Example: Immediate and slow components streamed out of order

async function Page() {
  return (
    <div>
      <Header /> 
      {/* <Header> streams to client immediately */}
      
      <Suspense fallback={<Loading />}>
        <SlowComponent />
        {/* Placeholder <Loading /> is shown, and client JS
            will replace it with <SlowComponent> content
            as soon as the server streams it */}
      </Suspense>
      
      <Footer />
      {/* <Footer> can stream immediately,
          before or after <SlowComponent>, depending on what finishes first */}
    </div>
  );
}
```

React's streaming SSR means the server sends "islands" of ready UI as soon as they're done, wherever they are in the code. The browser shows the page piecemeal, filling in slow spots later. The React client runtime handles swapping placeholders for finished components when each chunk of streamed content completes, providing a smooth and efficient user experience.

```

## Caching Patterns

### Request Deduplication

Multiple components requesting same data should share request:

```javascript
// Without deduplication
// Component A: fetch('/api/user')
// Component B: fetch('/api/user')
// = 2 requests

// With deduplication (React cache / TanStack Query)
// Component A: useQuery(['user'], fetchUser)
// Component B: useQuery(['user'], fetchUser)
// = 1 request, shared result
```

### Stale-While-Revalidate

Show cached data immediately, update in background:

```javascript
const { data } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts,
  staleTime: 60000,      // Fresh for 60s
  refetchOnMount: true,  // Background refetch
});

// Timeline:
// 1. Show cached data immediately
// 2. Check if stale
// 3. If stale, refetch in background
// 4. Update UI when fresh data arrives
```

### Cache Invalidation

Clear or update cache after mutations:

```javascript
const mutation = useMutation({
  mutationFn: createPost,
  onSuccess: () => {
    // Invalidate and refetch
    queryClient.invalidateQueries(['posts']);
    
    // Or update cache directly
    queryClient.setQueryData(['posts'], (old) => [...old, newPost]);
  },
});
```

## Loading State Patterns

### Skeleton Screens

Show content structure while loading:

```jsx
function ProductCard({ product }) {
  if (!product) {
    return (
      <div className="card">
        <div className="skeleton-image" />
        <div className="skeleton-text" />
        <div className="skeleton-text short" />
      </div>
    );
  }
  return (
    <div className="card">
      <img src={product.image} />
      <h3>{product.name}</h3>
      <p>{product.price}</p>
    </div>
  );
}
```

### Optimistic Updates

Update UI immediately, rollback on error:

```javascript
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries(['todos']);
    
    // Snapshot previous value
    const previous = queryClient.getQueryData(['todos']);
    
    // Optimistically update
    queryClient.setQueryData(['todos'], (old) =>
      old.map(t => t.id === newTodo.id ? newTodo : t)
    );
    
    return { previous };
  },
  onError: (err, newTodo, context) => {
    // Rollback on error
    queryClient.setQueryData(['todos'], context.previous);
  },
});
```

### Placeholder Data

Show estimated/placeholder data while fetching:

```javascript
const { data } = useQuery({
  queryKey: ['product', id],
  queryFn: () => fetchProduct(id),
  placeholderData: {
    name: 'Loading...',
    price: '--',
    image: '/placeholder.jpg',
  },
});
```

## Error Handling

### Error Boundaries

Catch and display errors gracefully:

```jsx
<ErrorBoundary fallback={<ErrorMessage />}>
  <Suspense fallback={<Loading />}>
    <DataComponent />
  </Suspense>
</ErrorBoundary>
```

### Retry Strategies

```javascript
const { data } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts,
  retry: 3,                    // Retry 3 times
  retryDelay: (attempt) => Math.min(1000 * 2 ** attempt, 30000),  // Exponential backoff
});
```

## Pattern Comparison

| Pattern | First Content | Data Freshness | Complexity |
|---------|---------------|----------------|------------|
| Client fetch (useEffect) | Slow | Real-time capable | Low |
| SSR | Fast | Request-time | Medium |
| SSG | Fastest | Build-time | Low |
| ISR | Fastest | Periodic | Medium |
| Streaming | Progressive | Request-time | Medium |

## Decision Framework

```
Is the data static or rarely changes?
├── Yes → SSG or ISR
│
└── No → Does the page need SEO?
          ├── Yes → SSR or Streaming
          │
          └── No → Does it need real-time updates?
                    ├── Yes → Client-side + WebSocket/polling
                    │
                    └── No → Is initial load critical?
                              ├── Yes → SSR + Client hydration
                              └── No → Client-side fetching
```

## Anti-Patterns

### 1. Fetching in useEffect Without Cleanup

```javascript
// Bad: Race condition possible
useEffect(() => {
  fetchData().then(setData);
}, [id]);

// Good: Cleanup or use library
useEffect(() => {
  let cancelled = false;
  fetchData().then(data => {
    if (!cancelled) setData(data);
  });
  return () => { cancelled = true; };
}, [id]);
```

### 2. Not Handling Loading/Error States

```javascript
// Bad: No loading or error handling
const { data } = useQuery(['products'], fetchProducts);
return <ProductList products={data} />;  // data might be undefined

// Good: Handle all states
if (isLoading) return <Loading />;
if (error) return <Error message={error.message} />;
return <ProductList products={data} />;
```

### 3. Over-fetching

```javascript
// Bad: Fetching more than needed
const { data: user } = useQuery(['user'], () => 
  fetch('/api/users/full-profile')  // 50 fields
);
// Only using: user.name, user.avatar

// Good: Fetch only what's needed (or use GraphQL)
const { data: user } = useQuery(['user-summary'], () =>
  fetch('/api/users/summary')  // 3 fields
);
```

---

## Deep Dive: Understanding Data Fetching From First Principles

### The Network Request Lifecycle

Every data fetch involves multiple steps:

```
CLIENT                          NETWORK                         SERVER

1. fetch() called                                               
         │                                                      
2. DNS Lookup ─────────────────► DNS Server                    
         │                       │                              
         │◄──────────────────── IP: 93.184.216.34              
         │                                                      
3. TCP Handshake ─────────────────────────────────────────────► SYN
         │                                                      │
         │◄─────────────────────────────────────────────────── SYN-ACK
         │                                                      
         │───────────────────────────────────────────────────► ACK
         │                                                      
4. TLS Handshake (HTTPS) ─────────────────────────────────────► 
         │◄─────────────────────────────────────────────────── 
         │                                                      
5. HTTP Request ──────────────────────────────────────────────► 
         │                     GET /api/data HTTP/1.1           
         │                     Host: example.com                │
         │                                                      ▼
         │                                              6. Server processes
         │                                                      │
         │                                              7. Query database
         │                                                      │
         │                                              8. Build response
         │                                                      │
         │◄──────────────────────────────────────────────────── 
         │                     HTTP/1.1 200 OK                  
         │                     {"data": [...]}                  
         │                                                      
9. Parse response                                               
         │                                                      
10. Update state                                                
         │                                                      
11. Re-render                                                   
```

**Time breakdown (typical):**

```
DNS Lookup:         10-100ms (cached: 0ms)
TCP Handshake:      50-100ms (1 round trip)
TLS Handshake:      50-150ms (2 round trips)
Request/Response:   50-500ms (depends on server + data size)
Parsing:            1-10ms
Rendering:          5-50ms
────────────────────────────────
TOTAL:              166-910ms
```

### The Waterfall Problem Explained

Waterfalls occur when requests depend on each other:

```javascript
// WATERFALL CODE:
async function loadDashboard() {
  const user = await fetchUser();           // 200ms ─────┐
  const posts = await fetchPosts(user.id);  // 300ms ─────┼─► WAIT
  const comments = await fetchComments(posts[0].id); // 250ms ─┘
}

// TIMELINE (serial):
// |── fetchUser (200ms) ──|── fetchPosts (300ms) ──|── fetchComments (250ms) ──|
// Total: 750ms


// PARALLEL CODE:
async function loadDashboard() {
  // Start all independent fetches simultaneously
  const [user, globalPosts] = await Promise.all([
    fetchUser(),        // 200ms ──┐
    fetchGlobalPosts(), // 300ms ──┤► PARALLEL
  ]);                            // └► Wait for slowest: 300ms
  
  // Dependent fetch still sequential
  const userPosts = await fetchUserPosts(user.id);  // 250ms
}

// TIMELINE (parallel where possible):
// |── fetchUser (200ms) ───|
// |── fetchGlobalPosts (300ms) ──|── fetchUserPosts (250ms) ──|
// Total: 550ms (vs 750ms waterfall)
```

### Why Caching is Essential

Without caching, you make redundant requests:

```javascript
// SCENARIO: Multiple components need user data

function Header() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch('/api/user').then(r => r.json()).then(setUser);
  }, []);
  return <span>{user?.name}</span>;
}

function Sidebar() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch('/api/user').then(r => r.json()).then(setUser);  // SAME REQUEST!
  }, []);
  return <img src={user?.avatar} />;
}

function Dashboard() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    fetch('/api/user').then(r => r.json()).then(setUser);  // SAME REQUEST!
  }, []);
  return <span>Welcome, {user?.name}</span>;
}

// RESULT: 3 identical network requests!
// Each takes 200ms, wasting bandwidth and time
```

**Request deduplication:**

```javascript
// WITH TANSTACK QUERY:
function Header() {
  const { data: user } = useQuery(['user'], fetchUser);
  // First component to request starts the fetch
}

function Sidebar() {
  const { data: user } = useQuery(['user'], fetchUser);
  // Same query key = shares the same request/cache
}

function Dashboard() {
  const { data: user } = useQuery(['user'], fetchUser);
  // All three components share ONE network request
}

// RESULT: 1 network request, shared across components
```

### How Cache Invalidation Works

Caches must be invalidated when data changes:

```javascript
// PROBLEM: Stale data after mutation

// User edits their profile
await updateProfile({ name: 'New Name' });

// But cached user data still shows old name!
// Other components display stale data

// SOLUTION 1: Invalidate and refetch
const queryClient = useQueryClient();

async function handleUpdate(newData) {
  await updateProfile(newData);
  
  // Invalidate the cache - next access will refetch
  queryClient.invalidateQueries(['user']);
}


// SOLUTION 2: Optimistic update + invalidate
async function handleUpdate(newData) {
  // Immediately update cache (optimistic)
  queryClient.setQueryData(['user'], (old) => ({
    ...old,
    ...newData,
  }));
  
  // Then persist to server
  try {
    await updateProfile(newData);
    // Invalidate to get any server-side changes
    queryClient.invalidateQueries(['user']);
  } catch (error) {
    // Rollback on failure
    queryClient.setQueryData(['user'], originalData);
  }
}


// SOLUTION 3: Server returns updated data
async function handleUpdate(newData) {
  const updatedUser = await updateProfile(newData);
  
  // Server returns the new state - update cache directly
  queryClient.setQueryData(['user'], updatedUser);
}
```

### Race Conditions in Data Fetching

When fetches can overlap, you get race conditions:

```javascript
// THE BUG:
function SearchResults({ query }) {
  const [results, setResults] = useState([]);
  
  useEffect(() => {
    fetch(`/api/search?q=${query}`)
      .then(r => r.json())
      .then(setResults);
  }, [query]);
  
  return <ResultList items={results} />;
}

// SCENARIO:
// User types "re" - starts fetch A (takes 500ms)
// User types "react" - starts fetch B (takes 200ms)
// Fetch B completes first - shows "react" results
// Fetch A completes second - OVERWRITES with "re" results!
// User sees wrong results!


// THE FIX: Abort previous request
function SearchResults({ query }) {
  const [results, setResults] = useState([]);
  
  useEffect(() => {
    const controller = new AbortController();
    
    fetch(`/api/search?q=${query}`, { signal: controller.signal })
      .then(r => r.json())
      .then(setResults)
      .catch(e => {
        if (e.name === 'AbortError') return; // Expected
        throw e;
      });
    
    // Cleanup: abort if query changes or component unmounts
    return () => controller.abort();
  }, [query]);
  
  return <ResultList items={results} />;
}


// OR use a library that handles this:
function SearchResults({ query }) {
  const { data: results } = useQuery({
    queryKey: ['search', query],
    queryFn: () => fetch(`/api/search?q=${query}`).then(r => r.json()),
    // TanStack Query automatically cancels outdated requests
  });
}
```

### Suspense: A New Data Fetching Paradigm

Traditional approach: component manages its loading state
Suspense approach: component delegates loading to boundary

```javascript
// TRADITIONAL: Each component handles loading
function ProductPage() {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchProduct()
      .then(setProduct)
      .finally(() => setLoading(false));
  }, []);
  
  if (loading) return <Spinner />;  // Loading logic in component
  return <Product data={product} />;
}


// SUSPENSE: Loading delegated to boundary
function ProductPage() {
  const product = use(fetchProduct());  // Suspends if not ready
  return <Product data={product} />;    // Only renders when ready
}

// Boundary handles loading
function App() {
  return (
    <Suspense fallback={<Spinner />}>  {/* Loading UI here */}
      <ProductPage />
    </Suspense>
  );
}
```

**How Suspense works internally:**

```javascript
// CONCEPTUAL MECHANISM:

function use(promise) {
  // Check if promise is already resolved
  if (promise.status === 'fulfilled') {
    return promise.value;
  }
  
  if (promise.status === 'rejected') {
    throw promise.reason;
  }
  
  // Not yet resolved - THROW the promise!
  throw promise;
}

// React catches the thrown promise
// Shows nearest Suspense fallback
// When promise resolves, re-renders the component

// This is why Suspense only works with:
// - React's use() hook
// - Libraries that support Suspense (like TanStack Query)
// - Server Components
```

### Streaming: Progressive Data Loading

Streaming sends data as it becomes available:

```javascript
// TRADITIONAL SSR:
// Server must fetch ALL data before sending ANY HTML

async function ProductPage() {
  // These all must complete before response starts
  const product = await getProduct();      // 100ms
  const reviews = await getReviews();       // 500ms  ← SLOW!
  const related = await getRelatedProducts(); // 200ms
  
  // Total wait: 800ms before ANY HTML sent
  return (
    <div>
      <Product data={product} />
      <Reviews data={reviews} />
      <Related data={related} />
    </div>
  );
}


// STREAMING SSR:
// Send what's ready, stream the rest

async function ProductPage() {
  const product = await getProduct();  // 100ms - quick!
  
  return (
    <div>
      <Product data={product} />  {/* Sent immediately */}
      
      <Suspense fallback={<ReviewsSkeleton />}>
        <Reviews />  {/* Streams when ready */}
      </Suspense>
      
      <Suspense fallback={<RelatedSkeleton />}>
        <Related />  {/* Streams when ready */}
      </Suspense>
    </div>
  );
}

// Client receives:
// t=100ms: Product HTML + skeleton placeholders
// t=300ms: Related products stream in
// t=600ms: Reviews stream in

// User sees content progressively!
```

### Optimistic Updates: The UX Advantage

Optimistic updates show expected result before server confirms:

```javascript
// WITHOUT OPTIMISTIC UPDATE:
// User clicks "Like"
// Spinner shows for 200ms
// Heart fills in
// Feels laggy

async function handleLike() {
  setIsLoading(true);
  await api.likePost(postId);  // 200ms
  await refetchPost();          // Another 200ms
  setIsLoading(false);
  // 400ms of waiting!
}


// WITH OPTIMISTIC UPDATE:
// User clicks "Like"
// Heart fills in IMMEDIATELY
// Server confirms in background

async function handleLike() {
  // Immediately update local state
  setIsLiked(true);
  setLikeCount(c => c + 1);
  
  try {
    await api.likePost(postId);
    // Success! State is already correct
  } catch (error) {
    // Failure! Revert the optimistic update
    setIsLiked(false);
    setLikeCount(c => c - 1);
    showError('Failed to like post');
  }
}

// User perceives INSTANT response
// Only 1 in 100 interactions might need rollback
```

### GraphQL vs REST: Data Fetching Implications

Different protocols have different fetching patterns:

```javascript
// REST: Multiple endpoints, potential over/under-fetching

// Need user profile + their posts + comment counts
// Requires 3 requests:
const user = await fetch('/api/users/123');
const posts = await fetch('/api/users/123/posts');
const comments = await fetch('/api/users/123/posts/comments/count');

// Over-fetching: Each endpoint returns all fields
// User endpoint returns 50 fields, you need 3


// GRAPHQL: Single endpoint, precise data

const query = `
  query UserProfile($id: ID!) {
    user(id: $id) {
      name       # Only fields you need
      avatar
      posts {
        title
        commentCount
      }
    }
  }
`;

const { user } = await graphqlFetch(query, { id: '123' });
// One request, exact data shape you need


// TRADEOFFS:

// REST:
// + Simple, well-understood
// + HTTP caching works naturally
// + Each endpoint cacheable independently
// - Over/under-fetching
// - Multiple round trips

// GRAPHQL:
// + Fetch exactly what you need
// + Single request
// + Strongly typed
// - More complex server setup
// - Caching more complex
// - Potential for expensive queries
```

### Error Handling Strategies

Different errors need different handling:

```javascript
// ERROR TYPES:

// 1. Network errors (offline, timeout)
try {
  await fetch('/api/data');
} catch (e) {
  if (!navigator.onLine) {
    showToast('You appear to be offline');
    // Maybe return cached data
    return cache.get('data');
  }
  if (e.name === 'AbortError') {
    // Request was cancelled, ignore
    return;
  }
  throw e;
}

// 2. HTTP errors (4xx, 5xx)
const response = await fetch('/api/data');
if (!response.ok) {
  if (response.status === 401) {
    // Unauthorized - redirect to login
    router.push('/login');
    return;
  }
  if (response.status === 404) {
    // Not found - show not found UI
    setNotFound(true);
    return;
  }
  if (response.status >= 500) {
    // Server error - retry later
    throw new Error('Server error, please try again');
  }
}

// 3. Application errors (in response body)
const data = await response.json();
if (data.error) {
  // Business logic error
  showError(data.error.message);
  return;
}


// ERROR BOUNDARY PATTERN:
<ErrorBoundary
  fallback={<ErrorPage />}
  onError={(error) => logToSentry(error)}
>
  <Suspense fallback={<Loading />}>
    <DataComponent />
  </Suspense>
</ErrorBoundary>
```

### The Request Deduplication Deep Dive

How libraries prevent duplicate requests:

```javascript
// NAIVE IMPLEMENTATION:
const cache = new Map();
const inFlight = new Map();

async function dedupedFetch(key, fetchFn) {
  // Return cached data if fresh
  if (cache.has(key)) {
    const { data, timestamp } = cache.get(key);
    if (Date.now() - timestamp < STALE_TIME) {
      return data;
    }
  }
  
  // If request already in flight, wait for it
  if (inFlight.has(key)) {
    return inFlight.get(key);
  }
  
  // Start new request
  const promise = fetchFn().then(data => {
    cache.set(key, { data, timestamp: Date.now() });
    inFlight.delete(key);
    return data;
  });
  
  inFlight.set(key, promise);
  return promise;
}

// USAGE:
// Both calls share the SAME network request
const data1 = await dedupedFetch('user', () => fetch('/api/user'));
const data2 = await dedupedFetch('user', () => fetch('/api/user'));
```

---

## For Framework Authors: Building Data Fetching Systems

> **Implementation Note**: The patterns and code examples below represent one proven approach to building data fetching systems. Different frameworks take different approaches—Remix uses loaders, React Query focuses on caching, and Next.js integrates with its rendering model. The direction shown here covers core primitives most data systems need. Adapt based on your framework's server/client boundaries, caching strategy, and how you handle loading states.

### Implementing Request Deduplication

```javascript
// REQUEST DEDUPLICATION IMPLEMENTATION

class RequestDeduplicator {
  constructor() {
    this.inflight = new Map();
    this.cache = new Map();
  }
  
  async fetch(key, fetcher, options = {}) {
    const { ttl = 0, forceRefresh = false } = options;
    const keyStr = typeof key === 'string' ? key : JSON.stringify(key);
    
    // Check cache first
    if (!forceRefresh && this.cache.has(keyStr)) {
      const cached = this.cache.get(keyStr);
      if (Date.now() - cached.timestamp < ttl) {
        return cached.data;
      }
    }
    
    // Check if request is already in flight
    if (this.inflight.has(keyStr)) {
      return this.inflight.get(keyStr);
    }
    
    // Create new request
    const promise = fetcher()
      .then(data => {
        this.cache.set(keyStr, { data, timestamp: Date.now() });
        this.inflight.delete(keyStr);
        return data;
      })
      .catch(error => {
        this.inflight.delete(keyStr);
        throw error;
      });
    
    this.inflight.set(keyStr, promise);
    return promise;
  }
  
  invalidate(key) {
    const keyStr = typeof key === 'string' ? key : JSON.stringify(key);
    this.cache.delete(keyStr);
  }
  
  invalidateMatching(predicate) {
    for (const key of this.cache.keys()) {
      if (predicate(key)) {
        this.cache.delete(key);
      }
    }
  }
}

// Per-request deduplication (for SSR)
function createRequestScopedCache() {
  const cache = new Map();
  
  return function cachedFetch(url, options) {
    const key = `${options?.method || 'GET'}:${url}`;
    
    if (cache.has(key)) {
      return cache.get(key);
    }
    
    const promise = fetch(url, options).then(r => r.json());
    cache.set(key, promise);
    
    return promise;
  };
}
```

### Building a Data Loader System

```javascript
// DATA LOADER SYSTEM (Framework Integration)

class DataLoader {
  constructor() {
    this.loaders = new Map();
    this.cache = new Map();
  }
  
  // Register a loader for a route
  register(routeId, loader) {
    this.loaders.set(routeId, loader);
  }
  
  // Load data for matched routes (parallel)
  async loadRoute(matches, request) {
    const results = await Promise.all(
      matches.map(async (match) => {
        const loader = this.loaders.get(match.route.id);
        if (!loader) return { routeId: match.route.id, data: null };
        
        const data = await loader({
          params: match.params,
          request,
          context: {},
        });
        
        return { routeId: match.route.id, data };
      })
    );
    
    // Return as map
    return new Map(results.map(r => [r.routeId, r.data]));
  }
  
  // Parallel data loading with dependencies
  async loadWithDeps(loaderGraph, request) {
    const results = new Map();
    const pending = new Set(loaderGraph.keys());
    
    while (pending.size > 0) {
      // Find loaders whose dependencies are satisfied
      const ready = [...pending].filter(id => {
        const deps = loaderGraph.get(id).dependsOn || [];
        return deps.every(d => results.has(d));
      });
      
      if (ready.length === 0 && pending.size > 0) {
        throw new Error('Circular dependency detected');
      }
      
      // Load in parallel
      await Promise.all(
        ready.map(async (id) => {
          const { loader, dependsOn = [] } = loaderGraph.get(id);
          const depData = Object.fromEntries(
            dependsOn.map(d => [d, results.get(d)])
          );
          
          const data = await loader({ request, deps: depData });
          results.set(id, data);
          pending.delete(id);
        })
      );
    }
    
    return results;
  }
}
```

### Implementing Suspense-Compatible Data Fetching

```javascript
// SUSPENSE DATA FETCHING

function createResource(fetcher) {
  let status = 'pending';
  let result;
  
  const promise = fetcher()
    .then(data => {
      status = 'success';
      result = data;
    })
    .catch(error => {
      status = 'error';
      result = error;
    });
  
  return {
    read() {
      switch (status) {
        case 'pending':
          throw promise; // Suspense catches this
        case 'error':
          throw result;  // ErrorBoundary catches this
        case 'success':
          return result;
      }
    },
  };
}

// Cache wrapper for resources
const resourceCache = new Map();

function getResource(key, fetcher) {
  if (!resourceCache.has(key)) {
    resourceCache.set(key, createResource(fetcher));
  }
  return resourceCache.get(key);
}

// Pre-load resources before rendering
function preloadResource(key, fetcher) {
  if (!resourceCache.has(key)) {
    resourceCache.set(key, createResource(fetcher));
  }
}

// Clear resource cache
function invalidateResource(key) {
  resourceCache.delete(key);
}

// Usage pattern
function UserProfile({ userId }) {
  const resource = getResource(
    ['user', userId],
    () => fetch(`/api/users/${userId}`).then(r => r.json())
  );
  
  // Will suspend until data is ready
  const user = resource.read();
  
  return <div>{user.name}</div>;
}
```

### Streaming Data Implementation

```javascript
// STREAMING DATA LOADING

async function* streamJSON(url) {
  const response = await fetch(url);
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    buffer += decoder.decode(value, { stream: true });
    
    // Try to parse complete JSON objects (newline-delimited)
    const lines = buffer.split('\n');
    buffer = lines.pop(); // Keep incomplete line
    
    for (const line of lines) {
      if (line.trim()) {
        yield JSON.parse(line);
      }
    }
  }
  
  // Parse remaining buffer
  if (buffer.trim()) {
    yield JSON.parse(buffer);
  }
}

// Server-Sent Events for real-time data
function createSSEConnection(url) {
  const eventSource = new EventSource(url);
  const listeners = new Set();
  
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    listeners.forEach(l => l(data));
  };
  
  return {
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    close() {
      eventSource.close();
    },
  };
}

// React hook for streaming data
function useStreamingData(url) {
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  useEffect(() => {
    let cancelled = false;
    
    async function stream() {
      for await (const item of streamJSON(url)) {
        if (cancelled) break;
        setItems(prev => [...prev, item]);
      }
      setIsLoading(false);
    }
    
    stream();
    return () => { cancelled = true; };
  }, [url]);
  
  return { items, isLoading };
}
```

### Building an Optimistic Update System

```javascript
// OPTIMISTIC UPDATES IMPLEMENTATION

class OptimisticUpdateManager {
  constructor(queryClient) {
    this.queryClient = queryClient;
    this.pendingUpdates = new Map();
  }
  
  async mutate(key, mutationFn, options = {}) {
    const { 
      optimisticUpdate, 
      rollback = true,
      invalidateKeys = [],
    } = options;
    
    const keyStr = JSON.stringify(key);
    
    // Snapshot current state
    const previousData = this.queryClient.getQueryData(key);
    const mutationId = Date.now().toString();
    
    try {
      // Apply optimistic update
      if (optimisticUpdate) {
        const optimisticData = optimisticUpdate(previousData);
        this.queryClient.setQueryData(key, optimisticData);
        this.pendingUpdates.set(mutationId, { key, previousData });
      }
      
      // Execute actual mutation
      const result = await mutationFn();
      
      // Update with server result
      if (result !== undefined) {
        this.queryClient.setQueryData(key, result);
      }
      
      // Invalidate related queries
      for (const invalidateKey of invalidateKeys) {
        this.queryClient.invalidateQueries(invalidateKey);
      }
      
      this.pendingUpdates.delete(mutationId);
      return result;
      
    } catch (error) {
      // Rollback on error
      if (rollback && this.pendingUpdates.has(mutationId)) {
        const { previousData } = this.pendingUpdates.get(mutationId);
        this.queryClient.setQueryData(key, previousData);
        this.pendingUpdates.delete(mutationId);
      }
      
      throw error;
    }
  }
  
  // Batch multiple optimistic updates
  async batchMutate(mutations) {
    const snapshots = mutations.map(m => ({
      key: m.key,
      previous: this.queryClient.getQueryData(m.key),
    }));
    
    // Apply all optimistic updates
    mutations.forEach((m, i) => {
      if (m.optimisticUpdate) {
        const data = m.optimisticUpdate(snapshots[i].previous);
        this.queryClient.setQueryData(m.key, data);
      }
    });
    
    try {
      // Execute all mutations in parallel
      const results = await Promise.all(
        mutations.map(m => m.mutationFn())
      );
      return results;
      
    } catch (error) {
      // Rollback all
      snapshots.forEach(s => {
        this.queryClient.setQueryData(s.key, s.previous);
      });
      throw error;
    }
  }
}
```

### Cache Invalidation Strategies

```javascript
// CACHE INVALIDATION PATTERNS

class CacheInvalidator {
  constructor(cache) {
    this.cache = cache;
    this.tags = new Map(); // tag -> Set of keys
  }
  
  // Associate cache entry with tags
  setWithTags(key, value, tags = []) {
    this.cache.set(key, value);
    
    for (const tag of tags) {
      if (!this.tags.has(tag)) {
        this.tags.set(tag, new Set());
      }
      this.tags.get(tag).add(key);
    }
  }
  
  // Invalidate by exact key
  invalidateKey(key) {
    this.cache.delete(key);
  }
  
  // Invalidate by tag
  invalidateTag(tag) {
    const keys = this.tags.get(tag);
    if (keys) {
      for (const key of keys) {
        this.cache.delete(key);
      }
      this.tags.delete(tag);
    }
  }
  
  // Invalidate by pattern
  invalidatePattern(pattern) {
    const regex = new RegExp(pattern);
    for (const key of this.cache.keys()) {
      if (regex.test(key)) {
        this.cache.delete(key);
      }
    }
  }
  
  // Time-based invalidation
  setWithTTL(key, value, ttlMs) {
    this.cache.set(key, {
      value,
      expiresAt: Date.now() + ttlMs,
    });
    
    // Schedule cleanup
    setTimeout(() => this.cache.delete(key), ttlMs);
  }
}

// Webhook-based invalidation (for ISR)
async function handleRevalidationWebhook(request) {
  const { type, id, tags } = await request.json();
  
  // Verify webhook signature
  const signature = request.headers.get('x-webhook-signature');
  if (!verifySignature(signature, request.body)) {
    return new Response('Unauthorized', { status: 401 });
  }
  
  // Invalidate based on payload
  if (id) {
    await revalidatePath(`/${type}/${id}`);
  }
  
  if (tags) {
    for (const tag of tags) {
      await revalidateTag(tag);
    }
  }
  
  return new Response('OK');
}
```

## Related Skills

- See [rendering-patterns](../rendering-patterns/SKILL.md) for SSR/SSG context
- See [state-management-patterns](../state-management-patterns/SKILL.md) for caching
- See [hydration-patterns](../hydration-patterns/SKILL.md) for client-side hydration
