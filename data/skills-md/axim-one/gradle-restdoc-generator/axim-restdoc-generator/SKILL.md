---
name: axim-restdoc-generator
description: Auto-generate REST API documentation from Spring Boot controllers using the Axim Gradle RestDoc Generator plugin. Use when configuring restMetaGenerator DSL, writing Javadoc tags (@response, @group, @auth, @error, @header), generating OpenAPI 3.0.3 specs, spec-bundle.json, error code scanning, Postman sync, or troubleshooting the gradle-restdoc-generator plugin.
---

# Axim Gradle RestDoc Generator

A Gradle plugin that auto-generates REST API documentation by scanning Spring Boot `@RestController` classes and their Javadoc comments.

**Version:** 2.0.6
**Requirements:** Java 17+, Gradle 7.0+, Spring Boot
**Repository:** https://github.com/Axim-one/gradle-restdoc-generator

## Installation

### build.gradle (buildscript)

```groovy
buildscript {
    repositories {
        maven { url 'https://jitpack.io' }
    }
    dependencies {
        classpath 'com.github.Axim-one:gradle-restdoc-generator:2.0.6'
    }
}

apply plugin: 'gradle-restdoc-generator'
```

### settings.gradle (Plugin DSL)

```groovy
pluginManagement {
    repositories {
        maven { url 'https://jitpack.io' }
        gradlePluginPortal()
    }
    resolutionStrategy {
        eachPlugin {
            if (requested.id.id == 'gradle-restdoc-generator') {
                useModule("com.github.Axim-one:gradle-restdoc-generator:${requested.version}")
            }
        }
    }
}
```

```groovy
plugins {
    id 'gradle-restdoc-generator' version '2.0.6'
}
```

## Configuration DSL

```groovy
restMetaGenerator {
    // Required
    documentPath = 'build/docs'
    basePackage = 'com.example'
    serviceId = 'my-service'

    // Service info (optional)
    serviceName = 'My Service'
    apiServerUrl = 'https://api.example.com'
    serviceVersion = 'v1.0'
    introductionFile = 'docs/introduction.md'

    // Error code / response class (optional)
    errorCodeClass = 'com.example.exception.ErrorCode'
    errorResponseClass = 'com.example.dto.ApiErrorResponse'    // v2.0.5+

    // Authentication (optional)
    auth {
        type = 'token'
        headerKey = 'Authorization'
        value = 'Bearer {{token}}'
        descriptionFile = 'docs/auth.md'
    }

    // Common headers (optional)
    header('X-Custom-Header', 'default-value', 'Header description')

    // Postman environments (optional)
    environment('DEV') {
        variable('base_url', 'https://dev.api.example.com')
        variable('token', 'dev-token')
    }
    environment('PROD') {
        variable('base_url', 'https://api.example.com')
        variable('token', '')
    }

    // Postman sync (optional)
    postmanApiKey = ''
    postmanWorkSpaceId = ''

    debug = false
}
```

### DSL Property Reference

| Property | Required | Default | Description |
|----------|----------|---------|-------------|
| `documentPath` | **Yes** | — | Output directory (relative to project root) |
| `basePackage` | **Yes** | — | Package(s) to scan (comma-separated for multiple) |
| `serviceId` | **Yes** | — | Service unique ID (used as JSON filename) |
| `serviceName` | No | `""` | Display name (OpenAPI title) |
| `apiServerUrl` | No | `""` | API base URL (OpenAPI servers) |
| `serviceVersion` | No | `"v1.0"` | API version (OpenAPI version) |
| `introductionFile` | No | `""` | Markdown file path for service description |
| `errorCodeClass` | No | `""` | ErrorCode class FQCN (fallback: framework default) |
| `errorResponseClass` | No | `""` | Error Response DTO FQCN (v2.0.5+, fallback: ApiError) |
| `postmanApiKey` | No | `""` | Postman API Key (empty = skip sync) |
| `postmanWorkSpaceId` | No | `""` | Postman Workspace ID |
| `debug` | **Yes** | `false` | Enable debug logging |

## Javadoc Tags

Write Javadoc on controller methods to enrich the generated documentation:

```java
/**
 * 사용자 정보를 조회합니다.
 *
 * @param userId 사용자 ID
 * @return 사용자 정보
 * @response 200 성공
 * @response 404 사용자를 찾을 수 없음
 * @group 사용자 관리
 * @auth true
 * @header X-Request-Id 요청 추적 ID
 * @error UserNotFoundException
 */
@GetMapping("/users/{userId}")
public UserDto getUser(@PathVariable Long userId) { ... }
```

### Tag Reference

| Tag | Description |
|-----|-------------|
| `@param` | Parameter description |
| `@return` | Return value description |
| `@response {code} {desc}` | HTTP response status code and description |
| `@error {ExceptionClass}` | Link error group — auto-populates errors and responseStatus |
| `@throws {ExceptionClass}` | Same as `@error` (standard Javadoc tag) |
| `@group` | API group name (maps to Postman folder) |
| `@auth true` | Mark endpoint as requiring authentication |
| `@header {name} {desc}` | Document a custom header |
| `@className` | Override generated class name |

NOTE: Method signature `throws` clauses are also auto-detected and linked to error groups (no Javadoc tag needed).

## Error Code Documentation

Exception classes with `public static final ErrorCode` fields are auto-scanned:

```java
public class UserNotFoundException extends RuntimeException {
    public static final ErrorCode USER_NOT_FOUND =
        new ErrorCode("USER_001", "error.user.notfound");
    public static final ErrorCode USER_DELETED =
        new ErrorCode("USER_002", "error.user.deleted");

    public UserNotFoundException(ErrorCode errorCode) {
        super(HttpStatus.NOT_FOUND, errorCode);
    }
}
```

### Error Code/Response Class Resolution (2-level priority)

1. **DSL explicit** — `errorCodeClass` / `errorResponseClass` in build.gradle
2. **Framework default** — `one.axim.framework.rest.exception.ErrorCode` / `one.axim.framework.rest.model.ApiError`

### Linking Errors to APIs

Use `@error` / `@throws` Javadoc tags or method `throws` clause:

```java
/**
 * 사용자 상세 조회
 * @error UserNotFoundException
 */
@GetMapping("/users/{id}")
public UserDto getUser(@PathVariable Long id) { ... }

// Or: auto-detected from throws clause
@GetMapping("/users/{id}/status")
public UserStatus getUserStatus(@PathVariable Long id) throws AuthException { ... }
```

## Pagination Support

Spring Data `Pageable`/`Page<T>` are auto-recognized:

```java
@GetMapping(name = "사용자 페이징 조회", value = "/paged")
public Page<UserDto> getUsers(Pageable pageable) { ... }
```

Auto-generated:
- **Query params:** `page` (default: 0), `size` (default: 20), `sort`
- **Response model:** `content`, `totalElements`, `totalPages`, `size`, `number`, `numberOfElements`, `first`, `last`, `empty`, `sort`
- **API JSON:** `isPaging: true`, `pagingType: "spring"`

## ApiResult Wrapper Unwrapping

`ApiResult<T>` wrapper types are auto-unwrapped:

```java
// Single → returnClass: "UserDto"
public ApiResult<UserDto> getUser() { ... }

// List → returnClass: "UserDto", isArrayReturn: true
public ApiResult<List<UserDto>> getUsers() { ... }

// Paging → returnClass: "UserDto", isPaging: true, pagingType: "spring"
public ApiResult<Page<UserDto>> getUsersPaged(Pageable pageable) { ... }
```

## Running the Plugin

```bash
./gradlew restMetaGenerator
```

## Output Structure

```
build/docs/
├── {serviceId}.json          # Service definition
├── openapi.json              # OpenAPI 3.0.3 spec
├── spec-bundle.json          # Integrated bundle (service + APIs + models + errors)
├── api/
│   └── {ControllerName}.json # Per-controller API definitions
├── model/
│   └── {ClassName}.json      # Model/DTO definitions
└── error/
    ├── errors.json           # Error code groups
    └── error-response.json   # Error response model structure
```

## spec-bundle.json Structure

The bundle JSON combines all outputs into a single file for UI consumption:

```json
{
  "service": {
    "serviceId": "my-service",
    "name": "My Service",
    "apiServerUrl": "https://api.example.com",
    "version": "v1.0",
    "introduction": "...",
    "auth": { "type": "token", "headerKey": "Authorization", ... },
    "headers": [...]
  },
  "apis": [
    {
      "id": "getUser",
      "name": "사용자 조회",
      "method": "GET",
      "urlMapping": "/users/{id}",
      "returnClass": "com.example.dto.UserDto",
      "parameters": [...],
      "responseStatus": { "200": "성공", "404": "사용자를 찾을 수 없음" },
      "errors": [{ "exception": "UserNotFoundException", "status": 404, "codes": [...] }]
    }
  ],
  "models": {
    "com.example.dto.UserDto": {
      "name": "UserDto",
      "type": "Object",
      "fields": [{ "name": "id", "type": "Long" }, ...]
    }
  },
  "errors": [
    {
      "group": "User Not Found",
      "exception": "UserNotFoundException",
      "status": 404,
      "codes": [{ "code": "USER_001", "name": "USER_NOT_FOUND", "message": "..." }]
    }
  ],
  "errorResponse": {
    "name": "ApiErrorResponse",
    "type": "Object",
    "fields": [...]
  }
}
```

## Execution Pipeline

The `restMetaGenerator` task runs in this order:

1. **Error Code Scan** — Collect ErrorCode fields from Exception classes
2. **API Document Generation** — Scan `@RestController` → generate per-controller/model JSON
3. **Error JSON Write** — Output `errors.json` + `error-response.json`
4. **OpenAPI Spec** — Generate `openapi.json` (OpenAPI 3.0.3)
5. **Spec Bundle** — Generate `spec-bundle.json`
6. **Postman Sync** — Sync Collection/Environment (if configured)

## Changelog

- **v2.0.6** — Fixed empty version causing `//path`, fixed ArrayIndexOutOfBoundsException for path-less mappings
- **v2.0.5** — Added `errorResponseClass` DSL property
- **v2.0.4** — OpenAPI 3.0.3, spec-bundle.json, error code scanning, @error/@throws tags
- **v2.0.3** — Fixed inner class enum ClassNotFoundException
- **v2.0.2** — Spring Pageable/Page<T> recognition, ApiResult<T> unwrapping
