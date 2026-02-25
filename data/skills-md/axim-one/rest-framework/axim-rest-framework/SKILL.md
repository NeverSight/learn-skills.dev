---
name: axim-rest-framework
description: Build Spring Boot REST APIs with Axim REST Framework. Use when creating entities, repositories, services, controllers, error handling, or pagination with the axim-rest-framework (Spring Boot + MyBatis). Covers @XEntity, @XRepository, IXRepository, query derivation, save/modify/upsert, XPagination, XPage, error codes, i18n exceptions, and declarative REST client.
---

# Axim REST Framework

Spring Boot + MyBatis lightweight REST framework. Annotation-based entity mapping and repository proxy pattern that minimizes boilerplate while keeping MyBatis SQL control.

**Version:** 1.1.0
**Requirements:** Java 17+, Spring Boot 3.3+, MySQL 5.7+/8.0+, MyBatis 3.0+
**Repository:** https://github.com/Axim-one/rest-framework

## Critical Rules

- SECURITY: `axim.rest.session.secret-key` MUST be set in production. Without it, tokens have NO signature — anyone can forge a session token.
- SECURITY: Set `spring.profiles.active=prod` in production. Non-prod profiles log full request bodies including passwords.
- `@XColumn` is only needed for: primary keys, custom column names, or insert/update control. Regular fields auto-map via camelCase → snake_case — do NOT add `@XColumn` to every field.
- `@XDefaultValue(value="X")` alone does NOT work — `isDBDefaultUsed` defaults to `true`, so the value is ignored. Must set `isDBDefaultUsed=false` for literal values.
- `@XRestServiceScan` is required on the application class when using `@XRestService` declarative REST clients.
- `XWebClient` beans can be registered via `axim.web-client.services.{name}={url}` in properties, then injected with `@Qualifier`.
- Session token format is NOT JWT — it uses custom `Base64(payload).HmacSHA256(signature)`. Do not use JWT libraries.
- JSON date format is `yyyy-MM-dd HH:mm:ss`, not ISO 8601.
- `XSessionResolver` auto-detects `SessionData` subclass parameters — no annotation required on the controller parameter.
- `@XPaginationDefault` defaults: `page=1`, `size=10`, `direction=DESC`. Sort without direction defaults to ASC.
- MANDATORY: Every member variable (Entity, DTO, Request, Response, VO) and every enum item MUST have a detailed Javadoc comment including purpose, example values, format rules, constraints, and allowed values.

## Installation

### Gradle

```gradle
repositories {
    mavenCentral()
    maven { url 'https://jitpack.io' }
}

dependencies {
    implementation 'com.github.Axim-one.rest-framework:core:1.1.0'
    implementation 'com.github.Axim-one.rest-framework:rest-api:1.1.0'
    implementation 'com.github.Axim-one.rest-framework:mybatis:1.1.0'
}
```

### Maven

```xml
<repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>

<dependencies>
    <dependency>
        <groupId>com.github.Axim-one.rest-framework</groupId>
        <artifactId>core</artifactId>
        <version>1.1.0</version>
    </dependency>
    <dependency>
        <groupId>com.github.Axim-one.rest-framework</groupId>
        <artifactId>rest-api</artifactId>
        <version>1.1.0</version>
    </dependency>
    <dependency>
        <groupId>com.github.Axim-one.rest-framework</groupId>
        <artifactId>mybatis</artifactId>
        <version>1.1.0</version>
    </dependency>
</dependencies>
```

## Application Setup

CRITICAL: All annotations below are required. Add `@XRestServiceScan` if using `@XRestService` REST clients.

```java
@ComponentScan({"one.axim.framework.rest", "one.axim.framework.mybatis", "com.myapp"})
@SpringBootApplication
@XRepositoryScan("com.myapp.repository")
@MapperScan({"one.axim.framework.mybatis.mapper", "com.myapp.mapper"})
@XRestServiceScan("com.myapp.client")  // Only if using @XRestService REST clients
public class MyApplication {
    public static void main(String[] args) {
        SpringApplication.run(MyApplication.class, args);
    }
}
```

| Annotation | Required | Purpose |
|---|---|---|
| `@ComponentScan` | **Yes** | Must include `one.axim.framework.rest`, `one.axim.framework.mybatis`, and app packages |
| `@XRepositoryScan` | **Yes** | Scans for `@XRepository` interfaces |
| `@MapperScan` | **Yes** | Must include `one.axim.framework.mybatis.mapper` + app mapper packages |
| `@XRestServiceScan` | If using REST client | Scans for `@XRestService` interfaces, creates JDK proxy beans |

### application.properties — Complete Reference

```properties
# ── DataSource ──
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=root
spring.datasource.password=
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
mybatis.config-location=classpath:mybatis-config.xml

# ── Framework: HTTP Client ──
axim.rest.client.pool-size=200                    # Max connection pool (default: 200)
axim.rest.client.connection-request-timeout=30    # seconds (default: 30)
axim.rest.client.response-timeout=30              # seconds (default: 30)
axim.rest.debug=false                             # REST client logging (default: false)

# ── Framework: Gateway ──
axim.rest.gateway.host=http://api-gateway:8080    # Enables gateway mode for @XRestService

# ── Framework: XWebClient Beans ──
axim.web-client.services.userClient=http://user-service:8080    # Named XWebClient bean
axim.web-client.services.orderClient=http://order-service:8080  # Named XWebClient bean

# ── Framework: Session / Token ──
axim.rest.session.secret-key=your-hmac-secret-key # HMAC-SHA256 signing (omit = unsigned)
axim.rest.session.token-expire-days=90            # Token lifetime (default: 90)

# ── Framework: i18n ──
axim.rest.message.default-language=ko-KR          # Default locale (default: ko-KR)
axim.rest.message.language-header=Accept-Language  # Language header (default: Accept-Language)
spring.messages.basename=messages                  # App message files (default: messages)
spring.messages.encoding=UTF-8
```

### mybatis-config.xml

All three elements (objectFactory, plugins, mappers) are **required**.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <settings>
        <setting name="cacheEnabled" value="true"/>
        <setting name="useGeneratedKeys" value="true"/>
        <setting name="defaultExecutorType" value="SIMPLE"/>
        <setting name="defaultStatementTimeout" value="10"/>
        <setting name="callSettersOnNulls" value="true"/>
        <setting name="mapUnderscoreToCamelCase" value="true"/>
    </settings>
    <!-- REQUIRED: Entity instantiation -->
    <objectFactory type="one.axim.framework.mybatis.plugin.XObjectFactory"/>
    <!-- REQUIRED: Pagination + result mapping -->
    <plugins>
        <plugin interceptor="one.axim.framework.mybatis.plugin.XResultInterceptor"/>
    </plugins>
    <!-- REQUIRED: Framework internal CRUD mapper -->
    <mappers>
        <mapper class="one.axim.framework.mybatis.mapper.CommonMapper"/>
    </mappers>
</configuration>
```

## Entity Definition

Use `@XEntity` to map a class to a database table. Fields auto-map using camelCase → snake_case conversion.

```java
@Data
@XEntity("users")
public class User {

    @XColumn(isPrimaryKey = true, isAutoIncrement = true)
    private Long id;

    private String email;
    private String name;

    @XDefaultValue(value = "NOW()", isDBValue = true)
    private LocalDateTime createdAt;

    @XDefaultValue(updateValue = "NOW()", isDBValue = true)
    private LocalDateTime updatedAt;

    @XColumn(insert = false, update = false)
    private String readOnlyField;

    @XIgnoreColumn
    private String transientField;
}
```

### Entity with Schema

```java
@XEntity(value = "orders", schema = "shop")
public class Order { ... }
```

### Entity Inheritance

Parent class fields are automatically included:

```java
public class BaseEntity {
    @XColumn(isPrimaryKey = true, isAutoIncrement = true)
    private Long id;

    @XDefaultValue(value = "NOW()", isDBValue = true)
    private LocalDateTime createdAt;

    @XDefaultValue(updateValue = "NOW()", isDBValue = true)
    private LocalDateTime updatedAt;
}

@Data
@XEntity("partners")
public class Partner extends BaseEntity {
    private String name;
    private String status;
}
```

### @XDefaultValue Patterns

```java
// Pattern 1: Use DB DEFAULT (column omitted from INSERT)
@XDefaultValue(isDBDefaultUsed = true)
private String region;

// Pattern 2: Literal string value on INSERT
@XDefaultValue(value = "ACTIVE", isDBDefaultUsed = false)
private String status;

// Pattern 3: DB expression on INSERT
@XDefaultValue(value = "NOW()", isDBValue = true, isDBDefaultUsed = false)
private LocalDateTime createdAt;

// Pattern 4: Auto-set value on UPDATE
@XDefaultValue(updateValue = "NOW()", isDBValue = true)
private LocalDateTime updatedAt;
```

## Annotations Reference

| Annotation | Target | Description |
|---|---|---|
| `@XEntity(value, schema)` | Class | Maps class to database table |
| `@XColumn(value, isPrimaryKey, isAutoIncrement, insert, update)` | Field | Column mapping with options |
| `@XDefaultValue(value, updateValue, isDBDefaultUsed, isDBValue)` | Field | Default values for INSERT/UPDATE |
| `@XIgnoreColumn` | Field | Excludes field from DB mapping |
| `@XRepository` | Interface | Marks repository for proxy generation |
| `@XRepositoryScan(basePackages)` | Class | Scans for @XRepository interfaces |

## Repository

Extend `IXRepository<K, T>` and annotate with `@XRepository`:

```java
@XRepository
public interface UserRepository extends IXRepository<Long, User> {
    User findByEmail(String email);
    List<User> findByStatus(String status);
    boolean existsByEmail(String email);
    long countByStatus(String status);
    int deleteByStatusAndName(String status, String name);
}
```

### Repository API

| Method | Return | Description |
|---|---|---|
| `save(entity)` | `K` | PK null → INSERT, PK present → Upsert (Composite: all PKs set → upsert) |
| `insert(entity)` | `K` | Plain INSERT with auto-generated ID (Composite: returns key class) |
| `saveAll(List)` | `K` | Batch INSERT IGNORE |
| `update(entity)` | `int` | Full UPDATE (all columns including nulls) |
| `modify(entity)` | `int` | Selective UPDATE (non-null fields only) |
| `findOne(key)` | `T` | Find by primary key |
| `findAll()` | `List<T>` | Find all rows |
| `findAll(pagination)` | `XPage<T>` | Paginated find all |
| `findWhere(Map)` | `List<T>` | Find by conditions |
| `findWhere(pagination, Map)` | `XPage<T>` | Paginated find by conditions |
| `findOneWhere(Map)` | `T` | Find one by conditions |
| `exists(key)` | `boolean` | Check existence by PK |
| `count()` / `count(Map)` | `long` | Total / conditional count |
| `deleteById(key)` | `int` | Delete by primary key |
| `deleteWhere(Map)` | `int` | Delete by conditions |

### CRUD Examples

```java
// save() - Upsert
User user = new User();
user.setName("Alice");
userRepository.save(user);        // INSERT, auto-increment ID set on entity
user.setId(1L);
userRepository.save(user);        // INSERT ... ON DUPLICATE KEY UPDATE

// insert() - Plain INSERT
userRepository.insert(user);

// update() vs modify()
userRepository.update(user);      // SET name='Alice', email=NULL, status=NULL
userRepository.modify(user);      // SET name='Alice' (null fields skipped)

// saveAll() - Batch
userRepository.saveAll(List.of(user1, user2, user3));

// Find
User found = userRepository.findOne(1L);
List<User> active = userRepository.findWhere(Map.of("status", "ACTIVE"));
boolean exists = userRepository.exists(1L);
long count = userRepository.count(Map.of("status", "ACTIVE"));

// Delete
userRepository.deleteById(1L);
userRepository.deleteWhere(Map.of("status", "INACTIVE"));
```

## Composite Primary Key

Entities with multiple primary keys use a key class for `IXRepository<K, T>`.

```java
// Key class — field names must match entity PK field names
@Data
public class OrderItemKey {
    private Long orderId;
    private Long itemId;
}

// Entity — multiple @XColumn(isPrimaryKey = true)
@Data
@XEntity("order_items")
public class OrderItem {
    @XColumn(isPrimaryKey = true)
    private Long orderId;
    @XColumn(isPrimaryKey = true)
    private Long itemId;
    private int quantity;
    private BigDecimal price;
}

// Repository
@XRepository
public interface OrderItemRepository extends IXRepository<OrderItemKey, OrderItem> {}
```

```java
// Usage
OrderItemKey key = new OrderItemKey();
key.setOrderId(1L);
key.setItemId(100L);

repository.findOne(key);       // WHERE order_id = ? AND item_id = ?
repository.delete(key);        // WHERE order_id = ? AND item_id = ?
repository.save(orderItem);    // All PKs set → upsert, any null → insert
repository.insert(orderItem);  // Returns OrderItemKey with both PK values
```

## Query Derivation

Declare methods and SQL is auto-generated from the method name.

**Supported Prefixes:** `findBy`, `findAllBy`, `countBy`, `existsBy`, `deleteBy`
**Condition Combinator:** `And`

```java
@XRepository
public interface OrderRepository extends IXRepository<Long, Order> {
    Order findByOrderNo(String orderNo);                           // WHERE order_no = ?
    List<Order> findByUserIdAndStatus(Long userId, String status); // WHERE user_id = ? AND status = ?
    long countByStatus(String status);                             // SELECT COUNT(*) WHERE status = ?
    boolean existsByOrderNo(String orderNo);                       // EXISTS check
    int deleteByUserIdAndStatus(Long userId, String status);       // DELETE WHERE ...
}
```

## Pagination

IMPORTANT: Always use `XPagination` and `XPage` for pagination. NEVER create custom pagination classes (e.g., PageRequest, PageResponse, PaginationDTO). The framework handles COUNT, ORDER BY, and LIMIT automatically.

```java
XPagination pagination = new XPagination();
pagination.setPage(1);       // 1-based
pagination.setSize(20);
pagination.addOrder(new XOrder("createdAt", XDirection.DESC));

XPage<User> result = userRepository.findAll(pagination);
result.getTotalCount();   // total rows
result.getPage();         // current page
result.getPageRows();     // rows in this page
result.getHasNext();      // more pages?

// Controller with auto-binding
@GetMapping
public XPage<User> searchUsers(@XPaginationDefault XPagination pagination) {
    return userRepository.findAll(pagination);
}
// Accepts: ?page=1&size=10&sort=email,asc
```

## Argument Resolvers

Two resolvers are auto-registered via `XWebMvcConfiguration`:

### XPaginationResolver — @XPaginationDefault

Resolves `XPagination` from query parameters. Annotation defaults:

| Attribute | Default | Description |
|---|---|---|
| `page` | `1` | Page number (1-based) |
| `size` | `10` | Rows per page |
| `offset` | `0` | Row offset (alternative to page) |
| `column` | `""` (none) | Default sort column (camelCase) |
| `direction` | `DESC` | Default sort direction |

Sort parsing:
```
?sort=createdAt,DESC          → XOrder("createdAt", DESC)
?sort=name                    → XOrder("name", ASC)   ← omitted direction defaults to ASC
?sort=createdAt,DESC&sort=name,ASC  → multi-sort
```

Priority: `?page=` present → page-based; `?offset=` only → offset-based. Query params override annotation defaults. `"undefined"` and `"null"` strings are treated as absent.

```java
@GetMapping
public XPage<User> listUsers(
        @XPaginationDefault(size = 20, column = "createdAt", direction = XDirection.DESC)
        XPagination pagination) {
    return userRepository.findAll(pagination);
}
```

### XSessionResolver — SessionData Subclass

Resolves any `SessionData` subclass from `Access-Token` HTTP header. **No annotation required** — auto-detected by parameter type.

```java
// UserSession extends SessionData → auto-resolved from Access-Token header
@GetMapping("/me")
public UserProfile getMyProfile(UserSession session) {
    return userService.getProfile(session.getUserId());
}
```

- Requires `XAccessTokenParseHandler` bean (auto-configured or custom `@Component`)
- If `XAccessTokenParseHandler` not registered → returns `null` (no error)
- If token missing → 401 (`NOT_FOUND_ACCESS_TOKEN`)
- If token invalid → 401 (`INVALID_ACCESS_TOKEN`)
- If token expired → 401 (`EXPIRE_ACCESS_TOKEN`)

## Query Strategy: Repository vs Custom Mapper

The framework provides two query approaches. Choosing the right one is critical:

### Use @XRepository (auto-generated SQL) when:
- Exact-match WHERE conditions: `findByStatus("ACTIVE")`
- Single-table CRUD operations
- Simple AND conditions: `findByUserIdAndStatus(id, status)`

### Use @Mapper (custom SQL) when:
- **LIKE / partial match**: `WHERE name LIKE '%keyword%'`
- **BETWEEN / range**: `WHERE created_at BETWEEN ? AND ?`
- **JOIN**: Any query involving multiple tables
- **Subqueries**: `WHERE id IN (SELECT ...)`
- **Aggregation**: `GROUP BY`, `HAVING`, `SUM()`, `COUNT()` per group
- **OR conditions**: `WHERE status = ? OR role = ?`
- **Complex sorting**: Sorting by computed/joined columns
- **UNION**: Combining result sets

**CRITICAL: Query derivation only supports exact-match `=` with `And` combinator. It does NOT support LIKE, BETWEEN, OR, IN, >, <, JOIN, or any other SQL operator. When these are needed, immediately create a @Mapper interface — do not attempt to work around Repository limitations.**

### Custom Mapper with Pagination (XPagination)

Custom @Mapper methods integrate with XPagination seamlessly. The framework's `XResultInterceptor` automatically intercepts the query to handle COUNT, ORDER BY, and LIMIT — you only write the base SELECT.

**Rules for custom mapper pagination:**
1. Add `XPagination` as the **first parameter**
2. Add `Class<?>` as the **last parameter** (pass the entity class — used for result type mapping)
3. Return `XPage<T>` as the return type
4. Write **only the base SELECT** — do NOT add ORDER BY or LIMIT in your SQL

```java
@Mapper
public interface UserMapper {

    // LIKE search with pagination
    @Select("SELECT * FROM users WHERE name LIKE CONCAT('%', #{keyword}, '%')")
    XPage<User> searchByName(XPagination pagination, @Param("keyword") String keyword, Class<?> cls);

    // BETWEEN with pagination
    @Select("SELECT * FROM users WHERE created_at BETWEEN #{from} AND #{to}")
    XPage<User> findByDateRange(XPagination pagination,
                                @Param("from") LocalDateTime from,
                                @Param("to") LocalDateTime to, Class<?> cls);

    // JOIN with pagination
    @Select("SELECT u.*, d.name AS department_name FROM users u " +
            "INNER JOIN departments d ON u.department_id = d.id " +
            "WHERE d.status = #{status}")
    XPage<UserWithDepartment> findUsersWithDepartment(XPagination pagination,
                                                      @Param("status") String status, Class<?> cls);

    // Multiple conditions (OR, IN)
    @Select("<script>" +
            "SELECT * FROM users WHERE status IN " +
            "<foreach item='s' collection='statuses' open='(' separator=',' close=')'>" +
            "#{s}" +
            "</foreach>" +
            "</script>")
    XPage<User> findByStatuses(XPagination pagination,
                               @Param("statuses") List<String> statuses, Class<?> cls);

    // Without pagination — just return List<T> (no XPagination, no Class<?>)
    @Select("SELECT * FROM users WHERE email LIKE CONCAT('%', #{keyword}, '%')")
    List<User> searchByEmail(@Param("keyword") String keyword);

    // Aggregation (non-paginated, returns custom projection)
    @Select("SELECT department_id, COUNT(*) as user_count FROM users GROUP BY department_id")
    List<Map<String, Object>> countByDepartment();
}
```

### Controller Pattern: Repository + Mapper Together

A typical controller uses Repository for simple operations and Mapper for complex queries:

```java
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserRepository userRepository;  // simple CRUD
    private final UserMapper userMapper;           // complex queries

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userRepository.findOne(id);
    }

    @GetMapping
    public XPage<User> searchUsers(@XPaginationDefault XPagination pagination,
                                   @RequestParam(required = false) String keyword) {
        if (keyword != null) {
            return userMapper.searchByName(pagination, keyword, User.class);
        }
        return userRepository.findAll(pagination);
    }

    @PostMapping
    public User createUser(@RequestBody User user) {
        userRepository.save(user);
        return user;
    }
}
```

## Error Code System

### ErrorCode Record

```java
public record ErrorCode(String code, String messageKey) {}
```

### Built-in Exceptions

| Code | Exception | HTTP | Description |
|---|---|---|---|
| `1` | `UnAuthorizedException` | 401 | Authentication required |
| `2` | `UnAuthorizedException` | 401 | Invalid credentials |
| `3` | `UnAuthorizedException` | 401 | Token expired |
| `11` | `InvalidRequestParameterException` | 400 | Invalid parameter |
| `12` | `InvalidRequestParameterException` | 400 | Request body not found |
| `13` | `InvalidRequestParameterException` | 400 | Method not supported |
| `100` | `NotFoundException` | 404 | Not found |
| `900` | `UnavailableServerException` | 504 | Server unavailable |
| `999` | `UnknownServerException` | 500 | Unknown error |

### Custom Exception

```java
public class UserException extends XRestException {
    public static final ErrorCode DUPLICATE_EMAIL = new ErrorCode("2001", "user.error.duplicate-email");
    public static final ErrorCode INACTIVE_ACCOUNT = new ErrorCode("2002", "user.error.inactive-account");

    public UserException(ErrorCode error) {
        super(HttpStatus.BAD_REQUEST, error);
    }

    public UserException(ErrorCode error, String description) {
        super(HttpStatus.BAD_REQUEST, error, description);
    }
}

// Usage
throw new UserException(UserException.DUPLICATE_EMAIL, "alice@example.com already exists");
```

### i18n Messages

```properties
# messages.properties
user.error.duplicate-email=Email already exists.

# messages_ko.properties
user.error.duplicate-email=이미 존재하는 이메일입니다.
```

### Error Response Format

```json
{
    "code": "2001",
    "message": "Email already exists.",
    "description": "alice@example.com already exists",
    "data": null
}
```

## Declarative REST Client

Requires `@XRestServiceScan` on application class.

### Direct Mode vs Gateway Mode

```java
// Direct Mode — host specified → URL: {host}{path}
@XRestService(value = "user-service", host = "${USER_SERVICE_HOST:http://localhost:8081}")
public interface UserServiceClient { ... }

// Gateway Mode — host omitted → URL: {gatewayHost}/{serviceName}/{version}{path}
@XRestService(value = "user-service", version = "v1")
public interface UserServiceClient { ... }
```

### Parameter Annotations

```java
@XRestService(value = "order-service", host = "${ORDER_SERVICE_HOST}")
public interface OrderServiceClient {

    @XRestAPI(value = "/orders/{id}", method = XHttpMethod.GET)
    Order getOrder(@PathVariable("id") Long id);

    @XRestAPI(value = "/orders", method = XHttpMethod.POST)
    Order createOrder(@RequestBody OrderCreateRequest request);

    @XRestAPI(value = "/orders", method = XHttpMethod.GET)
    List<Order> search(@RequestParam("status") String status,
                       @RequestParam("keyword") String keyword);

    @XRestAPI(value = "/orders", method = XHttpMethod.GET)
    List<Order> getOrders(@RequestHeader("X-Tenant-Id") String tenantId);

    // XPagination auto-converted → ?page=1&size=20&sort=createdAt,DESC
    @XRestAPI(value = "/orders", method = XHttpMethod.GET)
    XPage<Order> listOrders(XPagination pagination);

    @XRestAPI(value = "/orders/{id}", method = XHttpMethod.PUT)
    Order updateOrder(@PathVariable("id") Long id,
                      @RequestBody OrderUpdateRequest request,
                      @RequestHeader("Access-Token") String token);
}
```

### Error Handling

```java
try {
    Order order = orderClient.getOrder(id);
} catch (XRestException e) {
    e.getStatus();       // Original HTTP status (400, 404, 500, etc.)
    e.getCode();         // Error code from ApiError
    e.getMessage();      // Error message
    e.getDescription();  // Additional description
}
```

### JSON Date Format

The framework ObjectMapper uses `yyyy-MM-dd HH:mm:ss` (NOT ISO 8601):
```java
// ✓ "2024-01-15 14:30:00"
// ✗ "2024-01-15T14:30:00Z"
```

## XWebClient (RestClient-based Alternative)

For programmatic HTTP calls (not declarative proxy). Two registration options:

### Option 1: Declarative Bean Registration via Properties

```properties
# application.properties — each entry creates a named XWebClient bean
axim.web-client.services.userClient=http://user-service:8080
axim.web-client.services.orderClient=http://order-service:8080
```

```java
@Service
@RequiredArgsConstructor
public class ExternalApiService {

    @Qualifier("userClient")
    private final XWebClient userClient;

    public User getUser(Long id) {
        return userClient.get("/users/{id}", User.class, id);
    }
}
```

### Option 2: Programmatic via XWebClientFactory

```java
@Service
@RequiredArgsConstructor
public class ExternalApiService {

    private final XWebClientFactory webClientFactory;

    public User getUser(Long id) {
        XWebClient client = webClientFactory.create("http://external-api.com");
        return client.get("/users/{id}", User.class, id);
    }
}
```

### API Reference

```java
// Simple API
client.get("/users/{id}", User.class, id);
client.post("/users", body, User.class);
client.put("/users/{id}", body, User.class, id);
client.delete("/users/{id}", Void.class, id);

// Generic types
client.get("/users", new ParameterizedTypeReference<List<User>>() {});

// Builder API
client.spec()
        .get("/users?keyword=" + keyword)
        .header("X-API-Key", "my-key")
        .body(requestBody)
        .retrieve(new ParameterizedTypeReference<List<User>>() {});
```

| Feature | `@XRestService` | `XWebClient` |
|---|---|---|
| Style | Interface + annotations | Direct method calls |
| Bean creation | `@XRestServiceScan` | Properties or `XWebClientFactory` |
| Best for | Internal microservice calls | External API, dynamic URLs |
| Pagination | Auto XPagination → query params | Manual query string |
```

## Session / Token Authentication

The framework provides a built-in token system. **This is NOT JWT** — uses custom `Base64(payload).HmacSHA256(signature)` format.

### Custom Session Data

```java
@Data
public class UserSession extends SessionData {
    /** 사용자 고유 ID */
    private Long userId;
    /** 사용자 이름 */
    private String userName;
    /** 사용자 권한 목록 (예시: ["ADMIN", "USER"]) */
    private List<String> roles;
}
```

`SessionData` base fields (auto-managed): `sessionId`, `createDate` (format: `yyyyMMddHHmmss`)

### Generating Tokens (Login)

```java
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/auth")
public class AuthController {

    private final XAccessTokenParseHandler tokenHandler;

    @PostMapping("/login")
    public Map<String, String> login(@RequestBody LoginRequest request) {
        // Authenticate user...
        UserSession session = new UserSession();
        session.setSessionId(UUID.randomUUID().toString());
        session.setUserId(authenticatedUser.getId());
        session.setUserName(authenticatedUser.getName());
        session.setRoles(authenticatedUser.getRoles());

        String token = tokenHandler.generateAccessToken(session);
        return Map.of("accessToken", token);
    }
}
```

### Using Session in Controllers

Session auto-resolved from `Access-Token` HTTP header:

```java
@GetMapping("/me")
public UserProfile getMyProfile(UserSession session) {
    // If token missing → 401 (NOT_FOUND_ACCESS_TOKEN)
    // If token invalid → 401 (INVALID_ACCESS_TOKEN)
    // If token expired → 401 (EXPIRE_ACCESS_TOKEN)
    return userService.getProfile(session.getUserId());
}
```

### Session Configuration

```properties
# MUST be set in production — without it, tokens can be forged
axim.rest.session.secret-key=your-secret-key
axim.rest.session.token-expire-days=90         # Expiration in days (default: 90)
```

**SECURITY WARNING:** If `secret-key` is omitted, tokens have NO signature verification — anyone can forge a valid session token by crafting Base64-encoded JSON. ALWAYS set a strong secret key in production.

## i18n Message Source

Hierarchical message resolution: Application messages override framework defaults.

```
messages.properties (your app)  →  overrides  →  framework-messages.properties (built-in)
```

Built-in framework messages:
```properties
server.http.error.invalid-parameter=Invalid request parameter.
server.http.error.required-auth=Authentication required.
server.http.error.invalid-auth=Invalid authentication credentials.
server.http.error.expire-auth=Authentication expired.
server.http.error.notfound-api=API not found.
server.http.error.server-error=Internal server error.
```

If key not found in any source, the key string itself is returned (no exception).

## Security Warnings

### 1. Session Secret Key — Token Forgery Risk

Without `axim.rest.session.secret-key`, token payload is Base64-decoded without integrity check. **Anyone can forge a valid session token.**

```properties
# ✗ DANGEROUS — attacker creates Base64({"userId":1}) → valid token
# axim.rest.session.secret-key=

# ✓ REQUIRED for production
axim.rest.session.secret-key=a-strong-random-secret-key-at-least-32-chars
```

Rules: Always set in production. Minimum 32 chars. Never commit to source control — use environment variables.

### 2. Request Body Logging in Non-prod Profile

`XRequestFilter` logs full request bodies when profile is NOT `prod`. **Passwords and sensitive fields are logged as-is** (no field-level masking). HTTP headers like `Authorization` are masked, but request body fields are NOT.

```properties
# ✗ Non-prod → logs plaintext passwords from login endpoints
spring.profiles.active=dev

# ✓ Prod → disables body logging and stack traces in errors
spring.profiles.active=prod
```

### 3. Demo Credentials

Demo module contains hardcoded DB credentials for local development only. NEVER copy into production config.

## Complete Service Layer Example

```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository userRepository;

    public User create(User user) {
        userRepository.save(user);
        return user;
    }

    public User partialUpdate(Long id, UserUpdateRequest req) {
        User user = new User();
        user.setId(id);
        user.setName(req.getName());
        userRepository.modify(user);    // selective UPDATE
        return userRepository.findOne(id);
    }

    public XPage<User> list(int page, int size) {
        XPagination pagination = new XPagination();
        pagination.setPage(page);
        pagination.setSize(size);
        pagination.addOrder(new XOrder("createdAt", XDirection.DESC));
        return userRepository.findAll(pagination);
    }
}
```

## Coding Conventions

### MANDATORY: Document All Member Variables and Enum Items

Every member variable in Entity, DTO, Request, Response, VO classes and every enum item MUST have a detailed Javadoc comment. Include: purpose, example values, format/pattern rules, constraints, and allowed values.

#### Entity Example

```java
@Data
@XEntity("orders")
public class Order {

    /** 주문 고유 식별자 (Auto Increment) */
    @XColumn(isPrimaryKey = true, isAutoIncrement = true)
    private Long id;

    /**
     * 주문 번호
     * - 형식: "ORD-{yyyyMMdd}-{6자리 시퀀스}"
     * - 예시: "ORD-20240115-000001"
     * - UNIQUE 제약조건 적용
     */
    private String orderNo;

    /**
     * 주문 상태
     * - "PENDING": 결제 대기
     * - "PAID": 결제 완료
     * - "SHIPPED": 배송 중
     * - "DELIVERED": 배송 완료
     * - "CANCELLED": 주문 취소
     * @see OrderStatus
     */
    private String status;

    /**
     * 주문 총 금액 (단위: 원, KRW)
     * - 소수점 2자리까지 허용
     * - 음수 불가
     * - 예시: 15000.00
     */
    private BigDecimal totalAmount;

    /**
     * 주문자 ID (users 테이블 FK)
     * - NULL 불가
     */
    private Long userId;

    /** 주문 생성 일시 (INSERT 시 자동 설정) */
    @XDefaultValue(value = "NOW()", isDBValue = true)
    private LocalDateTime createdAt;

    /** 주문 수정 일시 (UPDATE 시 자동 갱신) */
    @XDefaultValue(updateValue = "NOW()", isDBValue = true)
    private LocalDateTime updatedAt;
}
```

#### DTO / Request Example

```java
@Data
public class OrderCreateRequest {

    /**
     * 주문할 상품 ID 목록
     * - 최소 1개 이상 필수
     * - 예시: [1, 2, 3]
     */
    @NotEmpty
    private List<Long> productIds;

    /**
     * 배송지 주소
     * - 전체 도로명 주소 (우편번호 제외)
     * - 예시: "서울특별시 강남구 테헤란로 123 4층"
     * - 최대 200자
     */
    @NotBlank
    @Size(max = 200)
    private String shippingAddress;

    /**
     * 배송 메모 (선택사항)
     * - 예시: "부재 시 경비실에 맡겨주세요"
     * - 최대 500자, NULL 허용
     */
    @Size(max = 500)
    private String deliveryNote;

    /**
     * 결제 수단 코드
     * - "CARD": 신용/체크카드
     * - "BANK": 무통장입금
     * - "KAKAO": 카카오페이
     * - "NAVER": 네이버페이
     */
    @NotBlank
    private String paymentMethod;
}
```

#### Enum Example

```java
public enum OrderStatus {

    /** 결제 대기 — 주문이 생성되었으나 결제가 완료되지 않은 상태 */
    PENDING,

    /** 결제 완료 — 결제가 확인되어 상품 준비 중인 상태 */
    PAID,

    /** 배송 중 — 택배사에 인계되어 배송이 진행 중인 상태 */
    SHIPPED,

    /** 배송 완료 — 수령인이 상품을 수령한 상태 */
    DELIVERED,

    /** 주문 취소 — 고객 요청 또는 시스템에 의해 취소된 상태. 환불 처리 필요 */
    CANCELLED
}
```

#### Comment Rules

| Rule | Description |
|---|---|
| All member variables | Must have `/** */` Javadoc comment describing purpose |
| Example values | Include concrete examples with `예시:` or `e.g.` prefix |
| Format/Pattern | Document format rules (e.g., `"ORD-{yyyyMMdd}-{seq}"`) |
| Allowed values | List all valid values for string-coded fields |
| Constraints | Note NOT NULL, UNIQUE, max length, range limits |
| Enum items | Each item must have a comment explaining the state/meaning |
| FK references | Note the referenced table (e.g., "users 테이블 FK") |
| Units | Specify units for numeric fields (e.g., 원, KRW, %, 초) |

### @XColumn Usage Rules

`@XColumn` is NOT required on every field. The framework auto-maps fields using camelCase → snake_case. Only use `@XColumn` when you need to set specific options.

```java
@Data
@XEntity("users")
public class User {

    @XColumn(isPrimaryKey = true, isAutoIncrement = true)
    private Long id;           // ✓ @XColumn needed — primary key

    private String email;      // ✓ auto-mapped to "email" — NO @XColumn needed
    private String userName;   // ✓ auto-mapped to "user_name" — NO @XColumn needed
    private Integer loginCount; // ✓ auto-mapped to "login_count" — NO @XColumn needed

    @XColumn("usr_email_addr")
    private String emailAddr;  // ✓ @XColumn needed — custom column name

    @XColumn(insert = false, update = false)
    private String readOnly;   // ✓ @XColumn needed — read-only field

    @XColumn(update = false)
    private String createdBy;  // ✓ @XColumn needed — immutable after creation
}
```

| Situation | @XColumn | Example |
|---|---|---|
| Primary Key | **Required** | `@XColumn(isPrimaryKey = true, isAutoIncrement = true)` |
| Composite PK field | **Required** | `@XColumn(isPrimaryKey = true)` |
| Regular field (camelCase→snake_case) | **Omit** | `private String userName;` → `user_name` |
| Custom column name | **Required** | `@XColumn("usr_nm")` |
| Read-only / insert-only / update-only | **Required** | `@XColumn(insert = false, update = false)` |
| Exclude from DB entirely | Use `@XIgnoreColumn` | `@XIgnoreColumn private String temp;` |

### @XDefaultValue Pitfall: isDBDefaultUsed Defaults to true

CRITICAL: `isDBDefaultUsed` defaults to `true`. This means `@XDefaultValue(value = "ACTIVE")` will **omit the column from INSERT** and use DB DEFAULT — the `value` is silently ignored!

```java
// ✗ WRONG — "ACTIVE" is IGNORED because isDBDefaultUsed defaults to true
@XDefaultValue(value = "ACTIVE")
private String status;

// ✓ CORRECT — must set isDBDefaultUsed = false for literal values
@XDefaultValue(value = "ACTIVE", isDBDefaultUsed = false)
private String status;

// ✓ CORRECT — DB expression
@XDefaultValue(value = "NOW()", isDBValue = true)
private LocalDateTime createdAt;

// ✓ CORRECT — intentionally use DB DEFAULT
@XDefaultValue(isDBDefaultUsed = true)
private String region;

// ✓ CORRECT — auto-set on UPDATE only
@XDefaultValue(updateValue = "NOW()", isDBValue = true)
private LocalDateTime updatedAt;
```

## Common Pitfalls

### 1. Column Names vs Field Names

Query derivation and `findWhere()` use **Java field names** (camelCase), NOT column names (snake_case).

```java
// ✗ WRONG
User findByUser_name(String name);
userRepository.findWhere(Map.of("user_name", "Alice"));

// ✓ CORRECT
User findByUserName(String name);
userRepository.findWhere(Map.of("userName", "Alice"));
```

### 2. findBy Return Type Determines Behavior

```java
User findByEmail(String email);       // → LIMIT 1 (single result)
List<User> findByEmail(String email); // → no LIMIT (all matches)
```

### 3. update() Overwrites with NULL

```java
User user = new User();
user.setId(1L);
user.setName("Alice");
// email and status are null

userRepository.update(user);  // ✗ Sets email=NULL, status=NULL in DB!
userRepository.modify(user);  // ✓ Only sets name='Alice', others preserved
```

### 4. ORDER BY / LIMIT in Custom Mapper SQL

XResultInterceptor handles pagination SQL automatically. Never add ORDER BY or LIMIT.

```java
// ✗ WRONG
@Select("SELECT * FROM users WHERE status = #{status} ORDER BY created_at DESC LIMIT 20")
XPage<User> findByStatus(XPagination pagination, @Param("status") String status, Class<?> cls);

// ✓ CORRECT — only the base SELECT
@Select("SELECT * FROM users WHERE status = #{status}")
XPage<User> findByStatus(XPagination pagination, @Param("status") String status, Class<?> cls);
```

### 5. Never Create Custom Pagination Classes

```java
// ✗ WRONG
public class PageRequest { int page; int size; }
public class PageResponse<T> { List<T> items; long total; }

// ✓ CORRECT — always use framework classes
XPagination pagination = new XPagination();
XPage<User> result = userRepository.findAll(pagination);
```

### 6. Empty Map in findWhere()

```java
userRepository.findWhere(Map.of());                    // ✗ Throws exception
userRepository.findAll();                               // ✓ Use findAll() instead
userRepository.findWhere(Map.of("status", "ACTIVE"));  // ✓ Non-empty map
```

### 7. Query Derivation Method Name Parsing

`And` only splits when preceded by lowercase and followed by uppercase.

```java
User findByBrandName(String brandName);                       // → single field "brandName"
List<User> findByStatusAndName(String status, String name);   // → two fields "status", "name"

// ✗ Parameter count must match parsed field count
List<User> findByStatusAndName(String status);  // WRONG — 2 fields but 1 param
```

## Architecture

```
Application Code                    Framework Internals
────────────────                    ───────────────────
@XRepository                        XRepositoryBeanScanner
UserRepository                           ↓
  extends IXRepository<K, T>        XRepositoryProxyFactoryBean
       ↓                                 ↓
  (JDK Dynamic Proxy)              XRepositoryProxy (InvocationHandler)
       ↓                                 ↓
                                    CommonMapper (@Mapper)
                                         ↓
                                    CrudSqlProvider (SQL Generation + Cache)
                                         ↓
                                    XResultInterceptor (Pagination, Result Mapping)
```
