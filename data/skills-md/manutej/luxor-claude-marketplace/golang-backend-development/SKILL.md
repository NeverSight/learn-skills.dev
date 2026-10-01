---
name: golang-backend-development
description: Complete guide for Go backend development including concurrency patterns, web servers, database integration, microservices, and production deployment
tags: [golang, go, concurrency, web-servers, microservices, backend, goroutines, channels, grpc, rest-api]
tier: tier-1
---

# Go Backend Development

A comprehensive skill for building production-grade backend systems with Go. Master goroutines, channels, web servers, database integration, microservices architecture, and deployment patterns for scalable, concurrent backend applications.

## When to Use This Skill

Use this skill when:

- Building high-performance web servers and REST APIs
- Developing microservices architectures with gRPC or HTTP
- Implementing concurrent processing with goroutines and channels
- Creating real-time systems requiring high throughput
- Building database-backed applications with connection pooling
- Developing cloud-native applications for containerized deployment
- Writing performance-critical backend services
- Building distributed systems with service discovery
- Implementing event-driven architectures
- Creating CLI tools and system utilities with networking capabilities
- Developing WebSocket servers for real-time communication
- Building data processing pipelines with concurrent workers

**Go excels at:**
- Network programming and HTTP services
- Concurrent processing with lightweight goroutines
- System-level programming with garbage collection
- Cross-platform compilation
- Fast compilation times for rapid development
- Built-in testing and benchmarking

## Core Concepts

### 1. Goroutines: Lightweight Concurrency

Goroutines are lightweight threads managed by the Go runtime. They enable concurrent execution with minimal overhead.

**Key Characteristics:**
- Extremely lightweight (start with ~2KB stack)
- Multiplexed onto OS threads by the runtime
- Thousands or millions can run concurrently
- Scheduled cooperatively with integrated scheduler

**Basic Goroutine Pattern:**

```go
func main() {
    // Launch concurrent computation
    go expensiveComputation(x, y, z)
    anotherExpensiveComputation(a, b, c)
}
```

The `go` keyword launches a new goroutine, allowing `expensiveComputation` to run concurrently with `anotherExpensiveComputation`. This is fundamental to Go's concurrency model.

**Common Use Cases:**
- Background processing
- Concurrent API calls
- Parallel data processing
- Real-time event handling
- Connection handling in servers

### 2. Channels: Safe Communication

Channels provide type-safe communication between goroutines, eliminating the need for explicit locks in many scenarios.

**Channel Types:**

```go
// Unbuffered channel - synchronous communication
ch := make(chan int)

// Buffered channel - asynchronous up to buffer size
ch := make(chan int, 100)

// Read-only channel
func receive(ch <-chan int) { /* ... */ }

// Write-only channel
func send(ch chan<- int) { /* ... */ }
```

**Synchronization with Channels:**

```go
func computeAndSend(ch chan int, x, y, z int) {
    ch <- expensiveComputation(x, y, z)
}

func main() {
    ch := make(chan int)
    go computeAndSend(ch, x, y, z)
    v2 := anotherExpensiveComputation(a, b, c)
    v1 := <-ch  // Block until result available
    fmt.Println(v1, v2)
}
```

This pattern ensures both computations complete before proceeding, with the channel providing both communication and synchronization.

**Channel Patterns:**
- Producer-consumer
- Fan-out/fan-in
- Pipeline stages
- Timeouts and cancellation
- Semaphores and rate limiting

### 3. Select Statement: Multiplexing Channels

The `select` statement enables multiplexing multiple channel operations, similar to a switch for channels.

**Timeout Implementation:**

```go
timeout := make(chan bool, 1)
go func() {
    time.Sleep(1 * time.Second)
    timeout <- true
}()

select {
case <-ch:
    // Read from ch succeeded
case <-timeout:
    // Operation timed out
}
```

**Context-Based Cancellation:**

```go
select {
case result := <-resultCh:
    return result
case <-ctx.Done():
    return ctx.Err()
}
```

### 4. Context Package: Request-Scoped Values

The `context.Context` interface manages deadlines, cancellation signals, and request-scoped values across API boundaries.

**Context Interface:**

```go
type Context interface {
    // Done returns a channel closed when work should be canceled
    Done() <-chan struct{}

    // Err returns why context was canceled
    Err() error

    // Deadline returns when work should be canceled
    Deadline() (deadline time.Time, ok bool)

    // Value returns request-scoped value
    Value(key any) any
}
```

**Creating Contexts:**

```go
// Background context - never canceled
ctx := context.Background()

// With cancellation
ctx, cancel := context.WithCancel(context.Background())
defer cancel()

// With timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

// With deadline
deadline := time.Now().Add(10 * time.Second)
ctx, cancel := context.WithDeadline(context.Background(), deadline)
defer cancel()

// With values
ctx = context.WithValue(parentCtx, key, value)
```

**Best Practices:**
- Always pass context as first parameter: `func DoSomething(ctx context.Context, ...)`
- Call `defer cancel()` immediately after creating cancelable context
- Propagate context through call chain
- Check `ctx.Done()` in long-running operations
- Use context values only for request-scoped data, not optional parameters

### 5. WaitGroup: Coordinating Goroutines

`sync.WaitGroup` waits for a collection of goroutines to finish.

**Basic Pattern:**

```go
var wg sync.WaitGroup

for i := 0; i < 10; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        // Do work
    }(i)
}

wg.Wait()  // Block until all goroutines complete
```

**Common Use Cases:**
- Waiting for parallel tasks
- Coordinating worker pools
- Ensuring cleanup completion
- Synchronizing shutdown

### 6. Mutex: Protecting Shared State

When shared state is necessary, use `sync.Mutex` or `sync.RWMutex` for protection.

**Mutex Pattern:**

```go
var (
    service   map[string]net.Addr
    serviceMu sync.Mutex
)

func RegisterService(name string, addr net.Addr) {
    serviceMu.Lock()
    defer serviceMu.Unlock()
    service[name] = addr
}

func LookupService(name string) net.Addr {
    serviceMu.Lock()
    defer serviceMu.Unlock()
    return service[name]
}
```

**RWMutex for Read-Heavy Workloads:**

```go
var (
    cache   map[string]interface{}
    cacheMu sync.RWMutex
)

func Get(key string) interface{} {
    cacheMu.RLock()
    defer cacheMu.RUnlock()
    return cache[key]
}

func Set(key string, value interface{}) {
    cacheMu.Lock()
    defer cacheMu.Unlock()
    cache[key] = value
}
```

### 7. Concurrent Web Server Pattern

Go's standard pattern for handling concurrent connections:

```go
for {
    rw := l.Accept()
    conn := newConn(rw, handler)
    go conn.serve()  // Handle each connection concurrently
}
```

Each accepted connection is handled in its own goroutine, allowing the server to scale to thousands of concurrent connections efficiently.

## Web Server Development

### HTTP Server Basics

**Simple HTTP Server:**

```go
package main

import (
    "fmt"
    "net/http"
)

func main() {
    http.HandleFunc("/", handler)
    http.ListenAndServe("localhost:8080", nil)
}

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprint(w, "Hello!")
}
```

### Request Handling Patterns

**Handler Functions:**

```go
func handler(w http.ResponseWriter, r *http.Request) {
    // Read request
    method := r.Method
    path := r.URL.Path
    query := r.URL.Query()

    // Write response
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusOK)
    fmt.Fprintf(w, `{"message": "success"}`)
}
```

**Handler Structs:**

```go
type APIHandler struct {
    db *sql.DB
    logger *log.Logger
}

func (h *APIHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    // Access dependencies
    h.logger.Printf("Request: %s %s", r.Method, r.URL.Path)
    // Handle request
}
```

### Middleware Pattern

**Logging Middleware:**

```go
func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        next.ServeHTTP(w, r)
        log.Printf("%s %s %v", r.Method, r.URL.Path, time.Since(start))
    })
}

// Usage
http.Handle("/api/", loggingMiddleware(apiHandler))
```

**Authentication Middleware:**

```go
func authMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")
        if !isValidToken(token) {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }
        next.ServeHTTP(w, r)
    })
}
```

**Chaining Middleware:**

```go
handler := loggingMiddleware(authMiddleware(corsMiddleware(apiHandler)))
http.Handle("/api/", handler)
```

### Context in HTTP Handlers

**HTTP Request with Context:**

```go
func handleSearch(w http.ResponseWriter, req *http.Request) {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    // Check query parameter
    query := req.FormValue("q")
    if query == "" {
        http.Error(w, "missing query", http.StatusBadRequest)
        return
    }

    // Perform search with context
    results, err := performSearch(ctx, query)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // Render results
    renderTemplate(w, results)
}
```

**Context-Aware HTTP Request:**

```go
func httpDo(ctx context.Context, req *http.Request,
            f func(*http.Response, error) error) error {
    c := &http.Client{}

    // Run request in goroutine
    ch := make(chan error, 1)
    go func() {
        ch <- f(c.Do(req))
    }()

    // Wait for completion or cancellation
    select {
    case <-ctx.Done():
        <-ch  // Wait for f to return
        return ctx.Err()
    case err := <-ch:
        return err
    }
}
```

### Routing Patterns

**Custom Router:**

```go
type Router struct {
    routes map[string]http.HandlerFunc
}

func (r *Router) Handle(pattern string, handler http.HandlerFunc) {
    r.routes[pattern] = handler
}

func (r *Router) ServeHTTP(w http.ResponseWriter, req *http.Request) {
    if handler, ok := r.routes[req.URL.Path]; ok {
        handler(w, req)
    } else {
        http.NotFound(w, req)
    }
}
```

**RESTful API Structure:**

```go
// GET /api/users
func listUsers(w http.ResponseWriter, r *http.Request) { /* ... */ }

// GET /api/users/:id
func getUser(w http.ResponseWriter, r *http.Request) { /* ... */ }

// POST /api/users
func createUser(w http.ResponseWriter, r *http.Request) { /* ... */ }

// PUT /api/users/:id
func updateUser(w http.ResponseWriter, r *http.Request) { /* ... */ }

// DELETE /api/users/:id
func deleteUser(w http.ResponseWriter, r *http.Request) { /* ... */ }
```

## Concurrency Patterns

### 1. Pipeline Pattern

Pipelines process data through multiple stages connected by channels.

**Generator Stage:**

```go
func gen(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)
    }()
    return out
}
```

**Processing Stage:**

```go
func sq(in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        for n := range in {
            out <- n * n
        }
        close(out)
    }()
    return out
}
```

**Pipeline Usage:**

```go
func main() {
    // Set up pipeline
    c := gen(2, 3)
    out := sq(c)

    // Consume output
    for n := range out {
        fmt.Println(n)  // 4 then 9
    }
}
```

**Buffered Generator (No Goroutine Needed):**

```go
func gen(nums ...int) <-chan int {
    out := make(chan int, len(nums))
    for _, n := range nums {
        out <- n
    }
    close(out)
    return out
}
```

### 2. Fan-Out/Fan-In Pattern

Distribute work across multiple workers and merge results.

**Fan-Out: Multiple Workers:**

```go
func main() {
    in := gen(2, 3, 4, 5)

    // Fan out: distribute work across two goroutines
    c1 := sq(in)
    c2 := sq(in)

    // Fan in: merge results
    for n := range merge(c1, c2) {
        fmt.Println(n)
    }
}
```

**Merge Function (Fan-In):**

```go
func merge(cs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)

    // Start output goroutine for each input channel
    output := func(c <-chan int) {
        for n := range c {
            out <- n
        }
        wg.Done()
    }

    wg.Add(len(cs))
    for _, c := range cs {
        go output(c)
    }

    // Close out once all outputs are done
    go func() {
        wg.Wait()
        close(out)
    }()
    return out
}
```

### 3. Explicit Cancellation Pattern

**Cancellation with Done Channel:**

```go
func sq(done <-chan struct{}, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * n:
            case <-done:
                return
            }
        }
    }()
    return out
}
```

**Broadcasting Cancellation:**

```go
func main() {
    done := make(chan struct{})
    defer close(done)  // Broadcast to all goroutines

    in := gen(done, 2, 3, 4)
    c1 := sq(done, in)
    c2 := sq(done, in)

    // Process subset of results
    out := merge(done, c1, c2)
    fmt.Println(<-out)

    // done closed on return, canceling all pipeline stages
}
```

**Merge with Cancellation:**

```go
func merge(done <-chan struct{}, cs ...<-chan int) <-chan int {
    var wg sync.WaitGroup
    out := make(chan int)

    output := func(c <-chan int) {
        defer wg.Done()
        for n := range c {
            select {
            case out <- n:
            case <-done:
                return
            }
        }
    }

    wg.Add(len(cs))
    for _, c := range cs {
        go output(c)
    }

    go func() {
        wg.Wait()
        close(out)
    }()
    return out
}
```

### 4. Worker Pool Pattern

**Fixed Number of Workers:**

```go
func handle(queue chan *Request) {
    for r := range queue {
        process(r)
    }
}

func Serve(clientRequests chan *Request, quit chan bool) {
    // Start handlers
    for i := 0; i < MaxOutstanding; i++ {
        go handle(clientRequests)
    }
    <-quit  // Wait to exit
}
```

**Semaphore Pattern:**

```go
var sem = make(chan int, MaxOutstanding)

func handle(r *Request) {
    sem <- 1        // Acquire
    process(r)
    <-sem           // Release
}

func Serve(queue chan *Request) {
    for req := range queue {
        go handle(req)
    }
}
```

**Limiting Goroutine Creation:**

```go
func Serve(queue chan *Request) {
    for req := range queue {
        sem <- 1  // Acquire before creating goroutine
        go func() {
            process(req)
            <-sem  // Release
        }()
    }
}
```

### 5. Query Racing Pattern

Query multiple sources and return first result:

```go
func Query(conns []Conn, query string) Result {
    ch := make(chan Result)
    for _, conn := range conns {
        go func(c Conn) {
            select {
            case ch <- c.DoQuery(query):
            default:
            }
        }(conn)
    }
    return <-ch
}
```

### 6. Parallel Processing Example

**Serial MD5 Calculation:**

```go
func MD5All(root string) (map[string][md5.Size]byte, error) {
    m := make(map[string][md5.Size]byte)
    err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
        if err != nil {
            return err
        }
        if !info.Mode().IsRegular() {
            return nil
        }
        data, err := ioutil.ReadFile(path)
        if err != nil {
            return err
        }
        m[path] = md5.Sum(data)
        return nil
    })
    return m, err
}
```

**Parallel MD5 with Pipeline:**

```go
type result struct {
    path string
    sum  [md5.Size]byte
    err  error
}

func sumFiles(done <-chan struct{}, root string) (<-chan result, <-chan error) {
    c := make(chan result)
    errc := make(chan error, 1)

    go func() {
        defer close(c)
        err := filepath.Walk(root, func(path string, info os.FileInfo, err error) error {
            if err != nil {
                return err
            }
            if !info.Mode().IsRegular() {
                return nil
            }

            // Start goroutine for each file
            go func() {
                data, err := ioutil.ReadFile(path)
                select {
                case c <- result{path, md5.Sum(data), err}:
                case <-done:
                }
            }()

            // Check for early cancellation
            select {
            case <-done:
                return errors.New("walk canceled")
            default:
                return nil
            }
        })

        select {
        case errc <- err:
        case <-done:
        }
    }()
    return c, errc
}

func MD5All(root string) (map[string][md5.Size]byte, error) {
    done := make(chan struct{})
    defer close(done)

    c, errc := sumFiles(done, root)

    m := make(map[string][md5.Size]byte)
    for r := range c {
        if r.err != nil {
            return nil, r.err
        }
        m[r.path] = r.sum
    }

    if err := <-errc; err != nil {
        return nil, err
    }
    return m, nil
}
```

### 7. Leaky Buffer Pattern

Efficient buffer reuse:

```go
var freeList = make(chan *Buffer, 100)

func server() {
    for {
        b := <-serverChan  // Wait for work
        process(b)

        // Try to reuse buffer
        select {
        case freeList <- b:
            // Buffer on free list
        default:
            // Free list full, GC will reclaim
        }
    }
}
```

## Database Integration

### Connection Management

**Database Connection Pool:**

```go
import "database/sql"

func initDB(dataSourceName string) (*sql.DB, error) {
    db, err := sql.Open("postgres", dataSourceName)
    if err != nil {
        return nil, err
    }

    // Configure connection pool
    db.SetMaxOpenConns(25)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(5 * time.Minute)
    db.SetConnMaxIdleTime(10 * time.Minute)

    // Verify connection
    if err := db.Ping(); err != nil {
        return nil, err
    }

    return db, nil
}
```

### Query Patterns

**Single Row Query:**

```go
func getUser(db *sql.DB, userID int) (*User, error) {
    user := &User{}
    err := db.QueryRow(
        "SELECT id, name, email FROM users WHERE id = $1",
        userID,
    ).Scan(&user.ID, &user.Name, &user.Email)

    if err == sql.ErrNoRows {
        return nil, fmt.Errorf("user not found")
    }
    if err != nil {
        return nil, err
    }

    return user, nil
}
```

**Multiple Row Query:**

```go
func listUsers(db *sql.DB) ([]*User, error) {
    rows, err := db.Query("SELECT id, name, email FROM users")
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    var users []*User
    for rows.Next() {
        user := &User{}
        if err := rows.Scan(&user.ID, &user.Name, &user.Email); err != nil {
            return nil, err
        }
        users = append(users, user)
    }

    if err := rows.Err(); err != nil {
        return nil, err
    }

    return users, nil
}
```

**Insert/Update with Context:**

```go
func createUser(ctx context.Context, db *sql.DB, user *User) error {
    query := "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id"
    err := db.QueryRowContext(ctx, query, user.Name, user.Email).Scan(&user.ID)
    return err
}
```

### Transaction Handling

```go
func transferFunds(ctx context.Context, db *sql.DB, from, to int, amount decimal.Decimal) error {
    tx, err := db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback()  // Rollback if not committed

    // Debit from account
    _, err = tx.ExecContext(ctx,
        "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
        amount, from)
    if err != nil {
        return err
    }

    // Credit to account
    _, err = tx.ExecContext(ctx,
        "UPDATE accounts SET balance = balance + $1 WHERE id = $2",
        amount, to)
    if err != nil {
        return err
    }

    return tx.Commit()
}
```

### Prepared Statements

```go
func insertUsers(db *sql.DB, users []*User) error {
    stmt, err := db.Prepare("INSERT INTO users (name, email) VALUES ($1, $2)")
    if err != nil {
        return err
    }
    defer stmt.Close()

    for _, user := range users {
        _, err := stmt.Exec(user.Name, user.Email)
        if err != nil {
            return err
        }
    }

    return nil
}
```

## Error Handling

### Custom Error Types

```go
type ValidationError struct {
    Field string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

// Usage
if email == "" {
    return &ValidationError{Field: "email", Message: "required"}
}
```

### Error Wrapping

```go
import "fmt"

func processData(data []byte) error {
    err := validateData(data)
    if err != nil {
        return fmt.Errorf("process data: %w", err)
    }
    return nil
}

// Unwrapping
if errors.Is(err, ErrValidation) {
    // Handle validation error
}

if errors.As(err, &validationErr) {
    // Access ValidationError fields
}
```

### Sentinel Errors

```go
var (
    ErrNotFound = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrInvalidInput = errors.New("invalid input")
)

// Usage
if errors.Is(err, ErrNotFound) {
    http.Error(w, "Resource not found", http.StatusNotFound)
}
```

## Testing

### Unit Tests

```go
func TestGetUser(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()

    user, err := getUser(db, 1)
    if err != nil {
        t.Fatalf("getUser failed: %v", err)
    }

    if user.Name != "John Doe" {
        t.Errorf("expected name John Doe, got %s", user.Name)
    }
}
```

### Table-Driven Tests

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "user@example.com", false},
        {"missing @", "userexample.com", true},
        {"empty string", "", true},
        {"missing domain", "user@", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := validateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("validateEmail(%q) error = %v, wantErr %v",
                    tt.email, err, tt.wantErr)
            }
        })
    }
}
```

### Benchmarks

```go
func BenchmarkConcurrentMap(b *testing.B) {
    m := make(map[string]int)
    var mu sync.Mutex

    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            mu.Lock()
            m["key"]++
            mu.Unlock()
        }
    })
}
```

### HTTP Handler Testing

```go
func TestHandler(t *testing.T) {
    req := httptest.NewRequest("GET", "/api/users", nil)
    w := httptest.NewRecorder()

    handler(w, req)

    resp := w.Result()
    if resp.StatusCode != http.StatusOK {
        t.Errorf("expected status 200, got %d", resp.StatusCode)
    }

    body, _ := ioutil.ReadAll(resp.Body)
    // Assert body content
}
```

## Production Patterns

### Graceful Shutdown

```go
func main() {
    srv := &http.Server{
        Addr:    ":8080",
        Handler: router,
    }

    // Start server in goroutine
    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatalf("listen: %s\n", err)
        }
    }()

    // Wait for interrupt signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    log.Println("Shutting down server...")

    // Graceful shutdown with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        log.Fatal("Server forced to shutdown:", err)
    }

    log.Println("Server exited")
}
```

### Configuration Management

```go
type Config struct {
    ServerPort  int           `env:"PORT" envDefault:"8080"`
    DBHost      string        `env:"DB_HOST" envDefault:"localhost"`
    DBPort      int           `env:"DB_PORT" envDefault:"5432"`
    LogLevel    string        `env:"LOG_LEVEL" envDefault:"info"`
    Timeout     time.Duration `env:"TIMEOUT" envDefault:"30s"`
}

func loadConfig() (*Config, error) {
    cfg := &Config{}
    if err := env.Parse(cfg); err != nil {
        return nil, err
    }
    return cfg, nil
}
```

### Structured Logging

```go
import "log/slog"

func setupLogger() *slog.Logger {
    return slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    }))
}

func handler(w http.ResponseWriter, r *http.Request) {
    logger := slog.With(
        "method", r.Method,
        "path", r.URL.Path,
        "remote", r.RemoteAddr,
    )

    logger.Info("handling request")

    // Process request

    logger.Info("request completed", "status", 200)
}
```

### Health Checks

```go
func healthHandler(db *sql.DB) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // Check database
        if err := db.Ping(); err != nil {
            w.WriteHeader(http.StatusServiceUnavailable)
            json.NewEncoder(w).Encode(map[string]string{
                "status": "unhealthy",
                "error": err.Error(),
            })
            return
        }

        // Check other dependencies...

        w.WriteHeader(http.StatusOK)
        json.NewEncoder(w).Encode(map[string]string{
            "status": "healthy",
        })
    }
}
```

### Rate Limiting

```go
import "golang.org/x/time/rate"

func rateLimitMiddleware(limiter *rate.Limiter) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            if !limiter.Allow() {
                http.Error(w, "Too Many Requests", http.StatusTooManyRequests)
                return
            }
            next.ServeHTTP(w, r)
        })
    }
}

// Usage
limiter := rate.NewLimiter(rate.Limit(10), 20)  // 10 req/sec, burst 20
handler := rateLimitMiddleware(limiter)(apiHandler)
```

### Panic Recovery

```go
func safelyDo(work *Work) {
    defer func() {
        if err := recover(); err != nil {
            log.Println("work failed:", err)
        }
    }()
    do(work)
}

func server(workChan <-chan *Work) {
    for work := range workChan {
        go safelyDo(work)
    }
}
```

## Microservices Patterns

### Service Structure

```go
type UserService struct {
    db     *sql.DB
    cache  *redis.Client
    logger *slog.Logger
}

func NewUserService(db *sql.DB, cache *redis.Client, logger *slog.Logger) *UserService {
    return &UserService{
        db:     db,
        cache:  cache,
        logger: logger,
    }
}

func (s *UserService) GetUser(ctx context.Context, userID string) (*User, error) {
    // Check cache first
    if user, err := s.getFromCache(ctx, userID); err == nil {
        return user, nil
    }

    // Query database
    user, err := s.getFromDB(ctx, userID)
    if err != nil {
        return nil, err
    }

    // Update cache
    go s.updateCache(context.Background(), user)

    return user, nil
}
```

### gRPC Service

```go
type server struct {
    pb.UnimplementedUserServiceServer
    db *sql.DB
}

func (s *server) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.User, error) {
    user := &pb.User{}
    err := s.db.QueryRowContext(ctx,
        "SELECT id, name, email FROM users WHERE id = $1",
        req.GetId(),
    ).Scan(&user.Id, &user.Name, &user.Email)

    if err != nil {
        return nil, status.Errorf(codes.NotFound, "user not found")
    }

    return user, nil
}
```

### Service Discovery

```go
type ServiceRegistry struct {
    services map[string][]string
    mu       sync.RWMutex
}

func (r *ServiceRegistry) Register(name, addr string) {
    r.mu.Lock()
    defer r.mu.Unlock()
    r.services[name] = append(r.services[name], addr)
}

func (r *ServiceRegistry) Discover(name string) (string, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    addrs := r.services[name]
    if len(addrs) == 0 {
        return "", fmt.Errorf("service %s not found", name)
    }

    // Simple round-robin
    return addrs[rand.Intn(len(addrs))], nil
}
```

### Circuit Breaker

```go
type CircuitBreaker struct {
    maxFailures int
    timeout     time.Duration
    failures    int
    lastFailure time.Time
    state       string  // closed, open, half-open
    mu          sync.Mutex
}

func (cb *CircuitBreaker) Call(fn func() error) error {
    cb.mu.Lock()

    if cb.state == "open" {
        if time.Since(cb.lastFailure) > cb.timeout {
            cb.state = "half-open"
        } else {
            cb.mu.Unlock()
            return errors.New("circuit breaker open")
        }
    }

    cb.mu.Unlock()

    err := fn()

    cb.mu.Lock()
    defer cb.mu.Unlock()

    if err != nil {
        cb.failures++
        cb.lastFailure = time.Now()
        if cb.failures >= cb.maxFailures {
            cb.state = "open"
        }
        return err
    }

    cb.failures = 0
    cb.state = "closed"
    return nil
}
```

## Best Practices

### 1. Goroutine Management

- Always consider goroutine lifecycle and cleanup
- Use contexts for cancellation propagation
- Avoid goroutine leaks by ensuring all goroutines can exit
- Be cautious with closures in loops - pass values explicitly

**Anti-pattern:**
```go
for _, v := range values {
    go func() {
        fmt.Println(v)  // All goroutines share same v
    }()
}
```

**Correct:**
```go
for _, v := range values {
    go func(val string) {
        fmt.Println(val)  // Each goroutine gets its own copy
    }(v)
}
```

### 2. Channel Best Practices

- Close channels from sender, not receiver
- Use buffered channels to prevent goroutine leaks
- Consider using `select` with `default` for non-blocking operations
- Remember: sending on closed channel panics, receiving returns zero value

### 3. Error Handling

- Return errors, don't panic (except for truly exceptional cases)
- Wrap errors with context using `fmt.Errorf("%w", err)`
- Use custom error types for programmatic handling
- Log errors with sufficient context

### 4. Performance

- Use `sync.Pool` for frequently allocated objects
- Profile before optimizing: `go test -bench . -cpuprofile=cpu.prof`
- Consider `sync.Map` for concurrent map access patterns
- Use buffered channels for known capacity
- Avoid unnecessary allocations in hot paths

### 5. Code Organization

```
project/
├── cmd/
│   └── server/
│       └── main.go          # Application entry point
├── internal/
│   ├── api/                 # HTTP handlers
│   ├── service/             # Business logic
│   ├── repository/          # Data access
│   └── middleware/          # HTTP middleware
├── pkg/
│   └── utils/               # Public utilities
├── migrations/              # Database migrations
├── config/                  # Configuration files
└── docker/                  # Docker files
```

### 6. Security

- Validate all inputs
- Use prepared statements for SQL queries
- Implement rate limiting
- Use HTTPS in production
- Sanitize error messages sent to clients
- Use context timeouts to prevent resource exhaustion
- Implement proper authentication and authorization

### 7. Testing

- Write table-driven tests
- Use `t.Helper()` for test helper functions
- Mock external dependencies
- Use `httptest` for HTTP handler testing
- Write benchmarks for performance-critical code
- Aim for >80% test coverage on business logic

## Common Pitfalls

### 1. Race Conditions

**Problem:**
```go
var service map[string]net.Addr

func RegisterService(name string, addr net.Addr) {
    service[name] = addr  // RACE CONDITION
}

func LookupService(name string) net.Addr {
    return service[name]  // RACE CONDITION
}
```

**Solution:**
```go
var (
    service   map[string]net.Addr
    serviceMu sync.Mutex
)

func RegisterService(name string, addr net.Addr) {
    serviceMu.Lock()
    defer serviceMu.Unlock()
    service[name] = addr
}
```

### 2. Goroutine Leaks

**Problem:**
```go
func process() {
    ch := make(chan int)
    go func() {
        ch <- expensive()  // Blocks forever if no receiver
    }()
    // Returns without reading from ch
}
```

**Solution:**
```go
func process() {
    ch := make(chan int, 1)  // Buffered channel
    go func() {
        ch <- expensive()  // Won't block
    }()
}
```

### 3. Not Closing Channels

Receivers need to know when no more values are coming:

```go
func gen(nums ...int) <-chan int {
    out := make(chan int)
    go func() {
        for _, n := range nums {
            out <- n
        }
        close(out)  // IMPORTANT: close when done
    }()
    return out
}
```

### 4. Blocking on Unbuffered Channels

```go
// This will deadlock
ch := make(chan int)
ch <- 1  // Blocks forever - no receiver
v := <-ch
```

Use buffered channels or separate goroutines.

### 5. Unsynchronized Channel Operations

```go
c := make(chan struct{})

// RACE CONDITION
go func() { c <- struct{}{} }()
close(c)
```

Ensure happens-before relationship with proper synchronization.

## Resources and References

### Official Documentation
- Go Documentation: https://go.dev/doc/
- Effective Go: https://go.dev/doc/effective_go
- Go Blog: https://go.dev/blog/
- Go by Example: https://gobyexample.com/

### Concurrency Resources
- Go Concurrency Patterns: https://go.dev/blog/pipelines
- Context Package: https://go.dev/blog/context
- Share Memory By Communicating: https://go.dev/blog/codelab-share

### Standard Library
- net/http: https://pkg.go.dev/net/http
- database/sql: https://pkg.go.dev/database/sql
- context: https://pkg.go.dev/context
- sync: https://pkg.go.dev/sync

### Tools
- Race Detector: `go test -race`
- Profiler: `go tool pprof`
- Benchmarking: `go test -bench`
- Static Analysis: `go vet`, `staticcheck`

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: Backend Development, Systems Programming, Concurrent Programming
**Prerequisites**: Basic programming knowledge, understanding of HTTP, familiarity with command line
**Recommended Next Skills**: docker-deployment, kubernetes-orchestration, grpc-microservices
