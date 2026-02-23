---
name: modern-java-backend-playbook
description: Enforces backend Java/Quarkus project standards including architecture layers, design patterns, code reuse, Lombok, TDD, exception handling, and modern Java features. Use this skill when writing, modifying, or reviewing Java backend code with Quarkus, Panache, Hibernate, Jakarta EE, or microservices architecture.
---

# Java Backend - Project Standards & Patterns

You are a senior Java backend developer working on a microservices ecosystem built with **Quarkus** and **Java**. Before writing or modifying code, analyze the project's `pom.xml` or `build.gradle` to identify the exact Java and Quarkus versions in use, then apply the best practices and features available for those versions. You MUST follow all the conventions and patterns described below when writing, modifying, or reviewing code. These are non-negotiable project standards.

---

## 1. Core Principles

### 1.1 Code Reuse
- **NEVER reinvent the wheel.** Before writing new logic, check if a solution already exists in:
  - The current project's utility classes (e.g., `QueryUtils`, `DateUtils`, `FileUtils`, `JwtUtil`)
  - Panache's built-in methods (`findByIdOptional`, `find`, `list`, `persist`, `delete`, `count`, `pageCount`)
  - Libraries already in the project (Apache Commons, MapStruct, Lombok, Jackson, etc.)
  - Java standard library methods (Stream API, `List.of()`, `Map.of()`, `Optional`, `String` methods)
- When a utility or helper already exists, use it. Do not create duplicate logic.

### 1.2 Design Patterns
Apply these patterns consistently:
- **SOLID** - Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion
- **Service Layer** - All business logic lives in Services, NEVER in Resources or Repositories
- **Repository Pattern** - Data access only, SQL/HQL queries here, no business logic
- **DTO Pattern** - DTOs for API input/output, Entities for persistence. Never expose Entities directly
- **Dependency Injection** - Constructor injection via Lombok `@AllArgsConstructor`. NEVER use `@Inject`
- **Facade** - Orchestrate multiple services when needed
- **Factory Method / Builder** - Use Lombok `@Builder` for complex object creation
- **Strategy** - Use when multiple algorithms/behaviors need to be interchangeable
- **Template Method** - Use for shared algorithm structures with varying steps
- **MVC** - Resources (controllers) handle HTTP, Services handle logic, Repositories handle data

### 1.3 Modern Java Features - USE THEM
Always check the Java version in `pom.xml` / `build.gradle` and prefer modern features available for that version:
- **Records** - For immutable DTOs, value objects, and simple data carriers where appropriate
- **Stream API** - For collection transformations. Prefer `stream().map().toList()` over manual loops
- **`List.of()`, `Map.of()`, `Set.of()`** - For immutable collections
- **Type inference (`var`)** - Use in local variables when the type is obvious from the right-hand side
- **Text Blocks (`"""`)** - For multi-line strings, SQL queries, JSON templates
- **Switch Expressions** - Use `->` syntax with yield when appropriate
- **Pattern Matching for `instanceof`** - Use `if (obj instanceof String s)` instead of casting
- **Pattern Matching for `switch`** - Use typed patterns in switch when applicable
- **Sealed classes** - Use for restricted hierarchies when applicable
- **String methods** - Use `.strip()`, `.isBlank()`, `.formatted()`, etc.
- **Virtual Threads** - Use when beneficial for I/O-bound concurrent operations

---

## 2. Architecture & Package Structure

Every microservice follows this package structure:

```
├── resources/              # REST endpoints (JAX-RS Resources)
├── service/                # Service interfaces
│   └── impl/               # Service implementations
├── repository/             # Panache repositories (data access + queries)
├── dto/                    # Data Transfer Objects (request/response)
├── entities/               # JPA entities
│   ├── enums/              # Enum types used by entities
│   └── converters/         # JPA attribute converters
├── exceptions/             # Custom exceptions (BusinessException, etc.)
│   └── providers/          # ExceptionMapper implementations
├── config/                 # Configuration classes
│   ├── interceptors/       # Filters, interceptors (LoggingFilter, TokenHeadersFactory)
│   └── validators/         # Custom constraint validators
├── annotations/            # Custom annotations (@OpComparison, @ValidCNS, etc.)
├── clients/                # REST client interfaces (@RegisterRestClient)
├── mapper/                 # MapStruct mappers (when used)
├── util/                   # Utility classes (QueryUtils, DateUtils, JwtUtil, etc.)
├── health/                 # Health check implementations
├── startup/                # Application startup hooks
└── concurrency/            # Interceptors and listeners for async operations
```

**Rules:**
- Separate files correctly into their packages/modules
- Do NOT mix concerns: a Service does not belong in `resources/`, a query does not belong in `service/`
- One class per file. Name the file exactly as the class name.

---

## 3. Resource Layer (Controllers)

Resources are thin HTTP controllers. They delegate ALL logic to Services.

```java
@AllArgsConstructor
@Authenticated
@Path("/v1/products")
public class ProductResources {

    private ProductService productService;

    @GET
    @Operation(summary = "List all products")
    public Response findByFilters(@BeanParam ProductFilter filter,
                                  @BeanParam Pageable pageable) {
        return Response.ok(productService.findByFilters(filter, pageable)).build();
    }

    @POST
    @Operation(summary = "Create a new product")
    public Response create(@Valid Product product,
                           @Context UriInfo uriInfo) throws BusinessException {
        var created = productService.create(product);
        var uri = uriInfo.getAbsolutePathBuilder().path(created.getId().toString()).build();
        return Response.created(uri).entity(created).build();
    }

    @DELETE
    @Path("{id}")
    @Operation(summary = "Delete a product")
    public Response delete(@PathParam("id") Long id) throws BusinessException {
        productService.deleteById(id);
        return Response.ok().build();
    }
}
```

**Rules:**
- `@AllArgsConstructor` for constructor injection (NEVER `@Inject`)
- `@Authenticated` for secured endpoints
- `@Valid` on request body DTOs for Hibernate Validator constraint validation
- `@BeanParam` for query filters and pagination
- `@Operation(summary = "...")` for OpenAPI documentation
- Resources return `Response` objects
- NO business logic in Resources - only delegation to Services
- Use `@Valid` annotations from Hibernate Validator directly on DTOs to avoid duplicate validation logic

---

## 4. Service Layer

Services contain ALL business logic. They follow the interface + implementation pattern.

### Service Interface
```java
public interface ProductService {
    PageResponse<Product> findByFilters(ProductFilter filter, Pageable pageable);
    List<Product> findByCategoryId(Long categoryId);
    Product create(Product product) throws BusinessException;
    void deleteById(Long id) throws BusinessException;
}
```

### Service Implementation
```java
@AllArgsConstructor
@ApplicationScoped
public class ProductServiceImpl implements ProductService {

    private final ProductRepository productRepository;

    @Override
    @Transactional(rollbackOn = Exception.class)
    public Product create(Product product) throws BusinessException {
        var existingProduct = productRepository.findByCode(product.getCode());
        if (existingProduct.isPresent()) {
            throw new BusinessException("Product already exists with code: " + product.getCode());
        }
        var entity = product.toEntity();
        productRepository.persist(entity);
        return Product.fromEntity(entity);
    }

    @Override
    @Transactional(rollbackOn = Exception.class)
    public void deleteById(Long id) throws BusinessException {
        var entity = this.findByIdInternal(id);
        productRepository.delete(entity);
    }

    protected ProductEntity findByIdInternal(Long id) throws BusinessException {
        return productRepository.findByIdOptional(id)
                .orElseThrow(() -> new BusinessException("Product not found"));
    }
}
```

**Rules:**
- `@AllArgsConstructor` for constructor injection (NEVER `@Inject`)
- `@ApplicationScoped` as the default scope
- `@Transactional(rollbackOn = Exception.class)` for write operations
- ALL business logic lives here, NOT in Resources or Repositories
- NO SQL/HQL in Services - queries belong in Repositories
- Throw `BusinessException` for business rule violations
- Use `findByIdOptional(...).orElseThrow(() -> new BusinessException(...))` for not-found cases
- Use `var` for local variables when the type is obvious
- Use `protected findByIdInternal(...)` for internal entity lookup reused across methods

---

## 5. Repository Layer

Repositories handle ALL data access using Panache.

```java
@ApplicationScoped
public class ProductRepository implements PanacheRepository<ProductEntity> {

    public List<ProductEntity> findByCategoryId(Long categoryId) {
        return list("SELECT p FROM ProductEntity p WHERE p.category.id = ?1", categoryId);
    }

    public Optional<ProductEntity> findByCode(String code) {
        return find("code = ?1", code).firstResultOptional();
    }

    public PanacheQuery<ProductEntity> find(String whereClause, Pageable pageable,
                                             Map<String, Object> params) {
        var baseQuery = "FROM ProductEntity p";
        var fullQuery = whereClause != null && !whereClause.isBlank()
                ? baseQuery + " WHERE " + whereClause
                : baseQuery;
        return find(fullQuery, pageable.getSortOrder(), params);
    }
}
```

**Rules:**
- Extends `PanacheRepository<EntityType>`
- `@ApplicationScoped`
- ALL SQL/HQL queries live here
- Reuse Panache built-in methods whenever possible (`findByIdOptional`, `find`, `list`, `persist`, `delete`)
- Return `Optional<T>` for single-result queries that may not find data
- Return `PanacheQuery<T>` for paginated queries

---

## 6. DTO Layer

DTOs are the bridge between API and Entity layers.

```java
@Data
@Builder(toBuilder = true)
@NoArgsConstructor
@AllArgsConstructor
@RegisterForReflection
public class Product {

    private Long id;

    @NotBlank(message = "Name is required")
    private String name;

    @NotNull(message = "Category is required")
    private Long categoryId;

    private String description;

    public static Product fromEntity(ProductEntity entity) {
        return Product.builder()
                .id(entity.getId())
                .name(entity.getName())
                .categoryId(entity.getCategoryId())
                .description(entity.getDescription())
                .build();
    }

    public ProductEntity toEntity() {
        return ProductEntity.builder()
                .id(this.id)
                .name(this.name)
                .categoryId(this.categoryId)
                .description(this.description)
                .build();
    }

    public static List<Product> toDtoList(List<ProductEntity> entityList) {
        return entityList.stream().map(Product::fromEntity).toList();
    }

    public static List<ProductEntity> toEntityList(List<Product> dtoList) {
        return dtoList.stream().map(Product::toEntity).toList();
    }
}
```

**Rules:**
- Use Lombok: `@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor`
- `@RegisterForReflection` for GraalVM native image support
- `@JsonInclude(JsonInclude.Include.NON_NULL)` when appropriate
- Validation annotations from Hibernate Validator: `@NotNull`, `@NotBlank`, `@NotEmpty`, `@Size`, `@Min`, `@Max`, `@Email`, `@Pattern`, etc.
- Place validation constraints on DTO fields, NOT in Service logic (avoids duplicate validation)
- Static `fromEntity(Entity)` method for entity-to-DTO conversion
- Instance `toEntity()` method for DTO-to-entity conversion
- Static `toDtoList(List<Entity>)` for bulk conversion using streams
- Static `toEntityList(List<DTO>)` for bulk conversion using streams
- Use `@Builder.Default` for fields with default values

### Filter DTOs
```java
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
@RegisterForReflection
public class ProductFilter {

    @QueryParam("name")
    @OpComparison(operator = "LIKE")
    private String name;

    @QueryParam("isActive")
    @OpComparison
    private Boolean isActive;
}
```

### Pagination DTOs
Use the standard `Pageable` and `PageResponse<T>` classes already in the project.

---

## 7. Entity Layer

```java
@Entity
@Table(name = "product")
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class ProductEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id")
    private Long id;

    @Column(name = "name")
    private String name;

    @Column(name = "code")
    private String code;

    @Column(name = "category_id")
    private Long categoryId;

    @Column(name = "description")
    private String description;

    @Column(name = "is_active")
    private Boolean isActive;

    @Column(name = "date_created")
    private LocalDateTime dateCreated;
}
```

**Rules:**
- Use Lombok: `@Data` (or `@Getter`/`@Setter` for entities with relationships to avoid hashCode issues), `@Builder`, `@AllArgsConstructor`, `@NoArgsConstructor`
- `@Entity` and `@Table(name = "table_name")`
- `@Id` with `@GeneratedValue(strategy = GenerationType.IDENTITY)`
- `@Column(name = "column_name")` for all fields
- `@Enumerated(EnumType.STRING)` for enum fields
- Enums go in the `entities.enums` package
- Entity class names end with `Entity` suffix (e.g., `ProductEntity`)

---

## 8. Exception Handling

### Custom Exceptions
```java
@RegisterForReflection
public class BusinessException extends Exception {
    public BusinessException(String message) {
        super(message);
    }

    public BusinessException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

### Problem Response Model
```java
@Getter
@RegisterForReflection
public class Problem {

    private final int status;
    private final OffsetDateTime timestamp;
    private final String title;
    private final String detail;
    private final List<ProblemObject> messages;

    public Problem(int status, String title, String detail) {
        this.status = status;
        this.timestamp = OffsetDateTime.now();
        this.title = title;
        this.detail = detail;
        this.messages = new ArrayList<>();
    }

    public void addMessage(String field, String message) {
        this.messages.add(new ProblemObject(field, message));
    }
}
```

### ProblemObject (field-level error detail)
```java
@RegisterForReflection
public record ProblemObject(String name, String message) {
}
```

### ProblemBuilder (centralized Response building)

Use `ProblemBuilder` to avoid repeating `Response.status().entity().type().build()` in every provider:

```java
public final class ProblemBuilder {

    private ProblemBuilder() {}

    public static Response build(int status, String title, String detail) {
        Problem problem = new Problem(status, title, detail);
        return Response.status(status)
                .entity(problem)
                .type(MediaType.APPLICATION_JSON)
                .build();
    }

    public static Response build(Problem problem) {
        return Response.status(problem.getStatus())
                .entity(problem)
                .type(MediaType.APPLICATION_JSON)
                .build();
    }
}
```

### ExceptionMapper Providers

Each provider creates a `Problem` with the appropriate status/title and delegates to `ProblemBuilder`:

```java
@Provider
public class BusinessExceptionProvider implements ExceptionMapper<BusinessException> {
    @Override
    public Response toResponse(BusinessException e) {
        Problem problem = new Problem(422, "Business rule violation", e.getMessage());
        return ProblemBuilder.build(problem);
    }
}
```

```java
@Provider
public class ConstraintViolationExceptionProvider implements ExceptionMapper<ConstraintViolationException> {
    @Override
    public Response toResponse(ConstraintViolationException e) {
        var problem = new Problem(400, "Invalid request data", "One or more fields are invalid.");
        e.getConstraintViolations().forEach(v ->
                problem.addMessage(
                        lastFieldName(v.getPropertyPath().iterator()),
                        v.getMessage()
                )
        );
        return ProblemBuilder.build(problem);
    }

    private String lastFieldName(Iterator<Path.Node> nodes) {
        Path.Node last = null;
        while (nodes.hasNext()) {
            last = nodes.next();
        }
        return last != null ? last.getName() : null;
    }
}
```

### Global Exception Provider (fallback)

Always create a `GlobalExceptionProvider` to catch any unhandled exception:

```java
@Provider
public class GlobalExceptionProvider implements ExceptionMapper<Throwable> {
    @Override
    public Response toResponse(Throwable e) {
        Problem problem = new Problem(500, "Error", e.getMessage());
        return ProblemBuilder.build(problem);
    }
}
```

**Rules:**
- ALWAYS map exceptions properly to return treated errors to the end user
- Use `Problem` with a single generic constructor (`status`, `title`, `detail`) — do NOT create one constructor per exception type
- Use `ProblemBuilder` to centralize Response building — providers should NEVER build the Response manually
- Use `ProblemObject` as a `record` for field-level error details
- Use `Problem.addMessage()` to attach field-level messages (e.g., in `ConstraintViolationExceptionProvider`)
- Use `BusinessException` for business rule violations (status 422)
- ALWAYS create a `GlobalExceptionProvider` for `Throwable` as a fallback for unhandled exceptions
- Create specific `@Provider` classes implementing `ExceptionMapper<T>` in the `exceptions.providers` package for each exception type that needs custom handling
- Verify that exceptions make architectural sense in their context. For example, do NOT throw a `BusinessException` inside a configuration class — use appropriate exception types for the layer
- Handle at minimum: `BusinessException`, `ConstraintViolationException`, `Throwable` (global fallback)

---

## 9. Dependency Injection

```java
// CORRECT - Constructor injection via Lombok
@AllArgsConstructor
@ApplicationScoped
public class MyServiceImpl implements MyService {
    private final MyRepository myRepository;
    private final JwtUtil jwtUtil;
}
```

```java
// WRONG - NEVER do this
@ApplicationScoped
public class MyServiceImpl implements MyService {
    @Inject  // NEVER use @Inject
    MyRepository myRepository;
}
```

**Rules:**
- ALWAYS use constructor injection via `@AllArgsConstructor`
- NEVER use `@Inject` for field injection
- Mark injected fields as `private final` when possible
- This applies to Resources, Services, Repositories, Config classes, and any CDI bean

---

## 10. Validation

Use Hibernate Validator constraint annotations directly on DTO fields:

```java
@Data
@Builder
public class CreateUserRequest {

    @NotBlank(message = "O nome e obrigatorio")
    private String name;

    @NotNull(message = "O email e obrigatorio")
    @Email(message = "Email invalido")
    private String email;

    @Size(min = 11, max = 11, message = "CPF deve ter 11 digitos")
    private String cpf;
}
```

Then use `@Valid` in the Resource:

```java
@POST
public Response create(@Valid CreateUserRequest request) throws BusinessException {
    return Response.ok(service.create(request)).build();
}
```

**Rules:**
- Place constraints on DTO fields: `@NotNull`, `@NotBlank`, `@NotEmpty`, `@Size`, `@Min`, `@Max`, `@Email`, `@Pattern`
- Use `@Valid` on the request body parameter in the Resource
- Do NOT duplicate validation in the Service that is already handled by constraints
- Create custom validators (in `config.validators`) when built-in constraints are insufficient

---

## 11. Constants

Define constants at the top of the class where they are used:

```java
public class Pageable {
    private static final int DEFAULT_PAGE = 0;
    private static final int DEFAULT_SIZE = 10;
    private static final int MAX_SORT_COLUMNS = 5;
    private static final Pattern SORT_COLUMN_PATTERN = Pattern.compile("^[A-Za-z][A-Za-z0-9_.]{0,63}$");

    // ... rest of the class
}
```

**Rules:**
- Constants go at the TOP of the class, before fields and methods
- Use `private static final` for class-internal constants
- Use `public static final` only when constants need to be shared
- Use `ALL_CAPS_SNAKE_CASE` for naming
- For utility classes with only static methods, add a private constructor to prevent instantiation
- **Evaluate whether constants should live in the class or in a dedicated constants class.** If a class accumulates too many constants or they are shared across multiple classes, consider moving them to a dedicated utility class (e.g., `AppConstants`, `ErrorMessages`) in the `util` package to keep the original class focused and readable

---

## 12. Lombok Usage

Use Lombok to eliminate boilerplate:

| Annotation | Usage |
|---|---|
| `@Data` | DTOs, Entities (generates getters, setters, equals, hashCode, toString) |
| `@Getter` / `@Setter` | Entities with relationships (to avoid hashCode issues) |
| `@Builder` | DTOs, Entities, complex objects |
| `@Builder(toBuilder = true)` | When you need to copy and modify objects |
| `@AllArgsConstructor` | Constructor injection in ALL CDI beans |
| `@NoArgsConstructor` | Required by JPA entities and Jackson deserialization |
| `@RequiredArgsConstructor` | When only `final` fields need injection |

**Rules:**
- ALWAYS use Lombok to avoid boilerplate code
- NEVER write getters/setters/constructors manually if Lombok can generate them
- Use `@Builder` for object construction in DTOs and Entities

---

## 13. Testing (TDD)

Apply TDD: write tests FIRST or alongside implementation to guarantee testability.

### Unit Test Pattern
```java
@QuarkusTest
@TestProfile(NoDatabaseTestProfile.class)
class ProductServiceImplTest {

    @InjectMock
    ProductRepository repository;

    AutoCloseable closeable;
    ProductServiceImpl service;

    @BeforeEach
    void initMocks() {
        closeable = MockitoAnnotations.openMocks(this);
        service = new ProductServiceImpl(repository);
    }

    @AfterEach
    void tearDown() throws Exception {
        closeable.close();
    }

    @Test
    void givenValidProduct_WhenCreate_ThenReturnCreatedProduct() {
        // GIVEN
        var product = MockProduct.newProduct();
        doAnswer(invocation -> {
            ProductEntity entity = invocation.getArgument(0);
            entity.setId(1L);
            return entity;
        }).when(repository).persist(any(ProductEntity.class));

        // WHEN
        var result = service.create(product);

        // THEN
        assertNotNull(result);
        assertEquals(1L, result.getId());
        verify(repository).persist(any(ProductEntity.class));
    }

    @Test
    void givenNonExistentId_WhenFindById_ThenThrowBusinessException() {
        // GIVEN
        when(repository.findByIdOptional(1L)).thenReturn(Optional.empty());

        // THEN
        var exception = assertThrows(BusinessException.class, () -> service.findById(1L));
        assertEquals("Product not found", exception.getMessage());
    }
}
```

### Integration Test Pattern
```java
@QuarkusTest
@TestHTTPResource
class ProductResourcesIT {

    @Test
    void givenValidRequest_WhenCreateProduct_ThenReturn201() {
        given()
            .contentType(ContentType.JSON)
            .body(/* request body */)
        .when()
            .post("/v1/products")
        .then()
            .statusCode(201);
    }
}
```

**Rules:**
- Test naming: `givenContext_WhenAction_ThenExpectedResult`
- Use GIVEN / WHEN / THEN comments to structure tests
- `@QuarkusTest` for all tests
- `@TestProfile(NoDatabaseTestProfile.class)` for unit tests that don't need a database
- `@InjectMock` or `@InjectSpy` for mocking Panache repositories
- Use `MockitoAnnotations.openMocks(this)` in `@BeforeEach`
- Close mocks in `@AfterEach`
- Create mock factory classes (e.g., `MockField.newField()`) for test data
- Use `rest-assured` for integration tests
- Use `TestContainers` for database integration tests
- Test both success and failure paths

---

## 14. Technology Stack Reference

Always check the project's `pom.xml` or `build.gradle` to identify the exact versions in use. Apply best practices for those versions.

| Technology | Purpose |
|---|---|
| Java | Language (check `pom.xml` / `build.gradle` for version) |
| Quarkus | Framework (check `pom.xml` / `build.gradle` for version) |
| Hibernate ORM + Panache | ORM / Data Access |
| Flyway | Database Migrations |
| SQL Server (MSSQL) | Database |
| Keycloak / OIDC | Authentication |
| Lombok | Code Generation |
| MapStruct | Object Mapping (when used) |
| Jackson | JSON Serialization |
| Hibernate Validator | Bean Validation |
| SmallRye OpenAPI | API Documentation |
| OpenTelemetry | Distributed Tracing |
| SmallRye Health | Health Checks |
| SmallRye Fault Tolerance | Resilience |
| AWS S3 | Object Storage |
| JUnit 5 + Mockito | Testing |
| TestContainers | Integration Testing |
| REST Assured | API Testing |
| JaCoCo | Code Coverage |

---

## 15. File Formatting

- Leave exactly ONE blank line at the end of every file
- Use 4 spaces for indentation (no tabs)
- Follow Java standard formatting conventions
- Organize imports: java.*, jakarta.*, third-party, project-internal

---

## 16. REST Client Pattern

Use `configKey` to decouple the configuration from the fully qualified class name:

```java
@RegisterRestClient(configKey = "user-api")
@Path("/v1/users")
public interface UserClient {

    @GET
    @Path("/{id}")
    UserResponse findById(@PathParam("id") Long id);
}
```

Configuration in `application.properties`:
```properties
quarkus.rest-client.user-api.url=${BACKEND_USER_URL}
```

**Rules:**
- Always use `configKey` in `@RegisterRestClient(configKey = "...")` instead of referencing the full class path
- The `configKey` should be a short, descriptive kebab-case name (e.g., `user-api`, `product-api`, `notification-api`)

---

## 17. Configuration Pattern

```properties
# Use environment variables with defaults
quarkus.datasource.username=${DATASOURCE_USERNAME}
quarkus.datasource.password=${DATASOURCE_PASSWORD}
quarkus.datasource.jdbc.url=jdbc:sqlserver://${DATASOURCE_HOST:localhost}:1433;databaseName=${DATASOURCE_DB_NAME}

# Profile-specific configuration
%dev.quarkus.log.level=INFO
%prod.quarkus.datasource.jdbc.min-size=${DATASOURCE_MIN_SIZE:2}
%prod.quarkus.datasource.jdbc.max-size=${DATASOURCE_MAX_SIZE:10}
```

**Rules:**
- Use environment variable placeholders `${VAR_NAME}` with sensible defaults `${VAR_NAME:default}`
- Use Quarkus profiles (`%dev.`, `%test.`, `%prod.`) for environment-specific config
- NEVER hardcode secrets or credentials

---

## 18. Explicit `this` Keyword Usage

Use `this.` explicitly in specific contexts to improve code readability, especially in **void methods** where there is no return value to guide the reader through the flow.

### When to use `this.`

**In void methods calling other methods of the same class:**
```java
@Override
public void updateStatusAndOverview(Long productSolicitationId, Long statusId,
                                     Long requestSummaryId) throws BusinessException {
    this.updateStatus(productSolicitationId, statusId, requestSummaryId, true);
}

@Override
public void deleteById(Long id) throws BusinessException {
    var entity = this.findByIdInternal(id);
    productRepository.delete(entity);
}
```

**In void update methods on DTOs/Requests — accessing own fields with `this.`:**
```java
public void updateUserEntity(UserEntity entity) {
    Optional.ofNullable(this.getName()).ifPresent(entity::setName);
    Optional.ofNullable(this.getEmail()).ifPresent(entity::setEmail);
    Optional.ofNullable(this.getPhone()).ifPresent(entity::setPhone);
    Optional.ofNullable(this.getDateOfBirth()).ifPresent(entity::setDateOfBirth);

    if (this.getRole() != null) {
        entity.setRole(RoleType.fromString(this.getRole()));
    }
}
```

**In constructors — field assignment (already standard in the project):**
```java
public Problem(BusinessException e) {
    this.status = 422;
    this.timestamp = OffsetDateTime.now();
    this.title = "Business";
    this.detail = e.getLocalizedMessage();
}
```

**In `toEntity()` and copy methods — accessing own fields in builders:**
```java
public ProductEntity toEntity() {
    return ProductEntity.builder()
            .id(this.id)
            .name(this.name)
            .categoryId(this.categoryId)
            .description(this.description)
            .build();
}
```

### When NOT to use `this.`

- In methods that return a value and the flow is already self-explanatory
- In simple one-liner delegations where the context is obvious
- Avoid adding `this.` everywhere indiscriminately — use it only where it genuinely improves readability

**Rules:**
- Use `this.` in void methods when calling other methods of the same class
- Use `this.` in void update methods on DTOs when accessing own fields/getters
- Use `this.` in constructors for field assignment
- Use `this.` in `toEntity()` and copy methods when building from own fields
- Do NOT apply `this.` blindly to all code — the goal is readability, not ceremony

---

## Summary Checklist

Before submitting any code, verify:
- [ ] Business logic is in the Service layer only
- [ ] SQL/HQL queries are in the Repository layer only
- [ ] Constructor injection via `@AllArgsConstructor` (no `@Inject`)
- [ ] Validation constraints are on DTO fields with `@Valid` in Resource
- [ ] Exceptions are mapped with ExceptionMapper providers
- [ ] Exceptions make architectural sense in their context
- [ ] Lombok is used to avoid boilerplate
- [ ] DTOs have `fromEntity()`, `toEntity()`, `toDtoList()` methods
- [ ] Modern Java features for the project's version are used (var, streams, records, switch expressions, pattern matching, etc.)
- [ ] Tests follow GIVEN/WHEN/THEN pattern
- [ ] Constants are at the top of the class
- [ ] Files are in the correct package
- [ ] Exactly one blank line at end of file
- [ ] Existing code and utilities are reused
- [ ] `this.` is used in void methods, constructors, `toEntity()`, and update methods for readability
