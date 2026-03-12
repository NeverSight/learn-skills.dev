---
name: flutter-dio
description: HTTP Networking with Dio, Retry & Caching Patterns
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "networking"
---

# Networking with Dio

-   Use **Dio** as the primary HTTP client package.
-   Use type-safe model classes with `fromJson` / `toJson` factories for all request/response bodies.
-   Handle all HTTP status codes appropriately with typed exceptions (e.g., `ServerException`, `NetworkException`, `UnauthorizedException`).
-   Use proper request timeouts (`connectTimeout`, `receiveTimeout`, `sendTimeout`).

# Dio Interceptors

-   Use interceptors for cross-cutting concerns:
    -   **Auth Interceptor**: Attach access tokens to headers, handle token refresh on 401.
    -   **Logging Interceptor**: Log requests/responses in debug mode via `AppLogger`.
    -   **Error Interceptor**: Transform `DioException` into domain-specific `Failure` types.
-   Register interceptors centrally via `injectable` for consistent behavior across all API calls.

# Repository Pattern

-   DataSources contain only raw Dio API calls — no business logic or mapping
-   Repositories orchestrate between remote DataSources and local cache for network data

# Retry & Resilience

-   Implement retry logic with exponential backoff for transient failures (e.g., 500, timeout).
-   Set a maximum retry count (default: 3 retries).
-   Cache responses when appropriate to reduce network calls and improve offline UX.

# Performance

-   Parse JSON in background isolates for large responses (> 1MB) using `compute()`
-   Do NOT block the UI thread with synchronous network operations

# Security

-   Store tokens via `flutter_secure_storage` — never in source code or `SharedPreferences`
-   All API communication MUST use HTTPS
