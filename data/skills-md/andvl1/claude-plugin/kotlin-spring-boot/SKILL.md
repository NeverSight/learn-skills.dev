---
name: kotlin-spring-boot
description: Kotlin/Spring Boot 3.x patterns - use for backend services, REST APIs, dependency injection, controllers, and service layers
---

# Kotlin Spring Boot Patterns

## Project Configuration

```kotlin
// build.gradle.kts
plugins {
    kotlin("jvm") version "2.2.21"
    kotlin("plugin.spring") version "2.2.21"
    id("org.springframework.boot") version "3.5.7"
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.springframework.boot:spring-boot-starter-data-jdbc")
    implementation("org.springframework.boot:spring-boot-starter-validation")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
}
```

## Entity Pattern

```kotlin
data class Environment(
    val id: UUID,
    val name: String,
    val status: EnvironmentStatus,
    val createdAt: Instant,
    val updatedAt: Instant?
)

enum class EnvironmentStatus {
    PENDING, RUNNING, STOPPED, FAILED
}
```

## Service Pattern

```kotlin
@Service
class EnvironmentService(
    private val repository: EnvironmentRepository,
    private val computeClient: ComputeClient
) {
    // Use NEVER propagation - let caller control transaction
    @Transactional(propagation = Propagation.NEVER)
    fun create(request: CreateEnvironmentRequest): Pair<EnvironmentResponse, Boolean> {
        // Check for existing (idempotency)
        repository.findByName(request.name)?.let {
            return Pair(it.toResponse(), false) // existing
        }

        // Create new
        val environment = Environment(
            id = UUID.randomUUID(),
            name = request.name,
            status = EnvironmentStatus.PENDING,
            createdAt = Instant.now(),
            updatedAt = null
        )

        val saved = repository.save(environment)
        return Pair(saved.toResponse(), true) // created
    }

    fun findById(id: UUID): Environment =
        repository.findById(id)
            ?: throw ResourceNotFoundRestException("Environment", id)

    fun findAll(): List<Environment> =
        repository.findAll()
}
```

## Controller Pattern

```kotlin
@RestController
class EnvironmentController(
    private val service: EnvironmentService
) : EnvironmentApi {

    override fun create(request: CreateEnvironmentRequest): ResponseEntity<EnvironmentResponse> {
        val (result, isNew) = service.create(request)
        return if (isNew) {
            ResponseEntity.status(HttpStatus.CREATED).body(result)
        } else {
            ResponseEntity.ok(result)
        }
    }

    override fun getById(id: UUID): ResponseEntity<EnvironmentResponse> =
        ResponseEntity.ok(service.findById(id).toResponse())

    override fun list(): ResponseEntity<List<EnvironmentResponse>> =
        ResponseEntity.ok(service.findAll().map { it.toResponse() })
}
```

## API Interface Pattern (OpenAPI)

```kotlin
@Tag(name = "Environments", description = "Environment management")
interface EnvironmentApi {

    @Operation(summary = "Create environment")
    @ApiResponses(
        ApiResponse(responseCode = "201", description = "Created"),
        ApiResponse(responseCode = "200", description = "Already exists"),
        ApiResponse(responseCode = "400", description = "Validation error")
    )
    @PostMapping("/api/v1/environments")
    fun create(
        @RequestBody @Valid request: CreateEnvironmentRequest
    ): ResponseEntity<EnvironmentResponse>

    @Operation(summary = "Get environment by ID")
    @GetMapping("/api/v1/environments/{id}")
    fun getById(@PathVariable id: UUID): ResponseEntity<EnvironmentResponse>

    @Operation(summary = "List all environments")
    @GetMapping("/api/v1/environments")
    fun list(): ResponseEntity<List<EnvironmentResponse>>
}
```

## DTO Pattern

```kotlin
data class CreateEnvironmentRequest(
    @field:NotBlank(message = "Name is required")
    @field:Size(max = 100, message = "Name must be <= 100 chars")
    val name: String,

    @field:Size(max = 500)
    val description: String? = null
)

data class EnvironmentResponse(
    val id: UUID,
    val name: String,
    val status: String,
    val createdAt: Instant
)

// Extension function for mapping
fun Environment.toResponse() = EnvironmentResponse(
    id = id,
    name = name,
    status = status.name,
    createdAt = createdAt
)
```

## Exception Handling

```kotlin
// Typed exceptions
throw ResourceNotFoundRestException("Environment", id)
throw ValidationRestException("Name cannot be empty")
throw ConflictRestException("Environment already exists")

// Global handler
@RestControllerAdvice
class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundRestException::class)
    fun handleNotFound(ex: ResourceNotFoundRestException): ResponseEntity<ErrorResponse> =
        ResponseEntity.status(HttpStatus.NOT_FOUND)
            .body(ErrorResponse(ex.message ?: "Not found"))

    @ExceptionHandler(MethodArgumentNotValidException::class)
    fun handleValidation(ex: MethodArgumentNotValidException): ResponseEntity<ErrorResponse> {
        val errors = ex.bindingResult.fieldErrors.map { "${it.field}: ${it.defaultMessage}" }
        return ResponseEntity.badRequest()
            .body(ErrorResponse("Validation failed", errors))
    }
}
```

## Kotlin Idioms

```kotlin
// Use ?.let for optional operations
user?.let { repository.save(it) }

// Use when for exhaustive matching
when (status) {
    EnvironmentStatus.PENDING -> startEnvironment()
    EnvironmentStatus.RUNNING -> return // already running
    EnvironmentStatus.STOPPED -> restartEnvironment()
    EnvironmentStatus.FAILED -> throw IllegalStateException("Cannot start failed env")
}

// Avoid !! operator, prefer these alternatives:
repository.findById(id).single()      // throws if not exactly one
repository.findById(id).firstOrNull() // returns null if none

// Data class copy for immutable updates
val updated = environment.copy(
    status = EnvironmentStatus.RUNNING,
    updatedAt = Instant.now()
)
```

## Configuration Properties

```kotlin
@ConfigurationProperties(prefix = "your-project")
data class AppProperties(
    val bot: BotProperties,
    val backend: BackendProperties
) {
    data class BotProperties(
        val token: String,
        val adminIds: List<Long> = emptyList()
    )

    data class BackendProperties(
        val url: String,
        val apiKey: String,
        val timeout: Duration = Duration.ofSeconds(30)
    )
}
```
