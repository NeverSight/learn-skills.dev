---
name: shared-models
description: Shared data models for Kotlin Multiplatform using kotlinx.serialization. Cross-platform domain models with validation and serialization.
---

# Shared Models for KMP

Design and implement data models that work across all platforms in `shared/commonMain`.

## Core Dependencies

```kotlin
// build.gradle.kts (shared module)
sourceSets {
    val commonMain by getting {
        dependencies {
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
            implementation("org.jetbrains.kotlinx:kotlinx-datetime:1.6.0")
        }
    }
}
```

Enable serialization plugin:
```kotlin
plugins {
    kotlin("multiplatform")
    kotlin("plugin.serialization") version "1.9.20"
}
```

## Domain Models

### 1. Immutable Data Classes

```kotlin
// commonMain/kotlin/com/example/shared/model/User.kt
@Serializable
data class User(
    val id: String,
    val name: String,
    val email: String,
    val avatarUrl: String?,
    val createdAt: Instant,
    val lastActiveAt: Instant?
)
```

### 2. Sealed Hierarchies

```kotlin
// commonMain/kotlin/com/example/shared/model/UiState.kt
@Serializable
sealed class UiState<out T> {
    @Serializable
    data object Loading : UiState<Nothing>()

    @Serializable
    data class Success<T>(val data: T) : UiState<T>()

    @Serializable
    data class Error(val message: String, val code: String? = null) : UiState<Nothing>()
}

// Usage with type parameter
@Serializable
sealed class HomeState {
    @Serializable
    data object Loading : HomeState()

    @Serializable
    data class Loaded(val user: User, val items: List<Item>) : HomeState()

    @Serializable
    data class Error(val message: String) : HomeState()
}
```

### 3. Result Wrapper

```kotlin
// commonMain/kotlin/com/example/shared/model/Result.kt
@Serializable
sealed class Result<out T> {
    @Serializable
    data class Success<T>(val data: T) : Result<T>()

    @Serializable
    data class Error(val code: String, val message: String) : Result<Nothing>()
}

// Helper to convert from Kotlin Result
fun <T> Result<T>.toKotlinResult(): kotlin.Result<T> = when (this) {
    is Result.Success -> kotlin.Result.success(data)
    is Result.Error -> kotlin.Result.failure(RuntimeException("$code: $message"))
}
```

### 4. Paginated Response

```kotlin
// commonMain/kotlin/com/example/shared/model/Pagination.kt
@Serializable
data class PaginatedResponse<T>(
    val items: List<T>,
    val page: Int,
    val pageSize: Int,
    val totalPages: Int,
    val totalItems: Long
) {
    val hasMorePages: Boolean get() = page < totalPages
    val nextPage: Int? get() = if (hasMorePages) page + 1 else null
}

// For cursor-based pagination
@Serializable
data class CursorResponse<T>(
    val items: List<T>,
    val nextCursor: String?,
    val hasMore: Boolean
)
```

### 5. Request/Response Models

```kotlin
// commonMain/kotlin/com/example/shared/model/auth/AuthRequests.kt
@Serializable
data class LoginRequest(
    val email: String,
    val password: String
)

@Serializable
data class RegisterRequest(
    val name: String,
    val email: String,
    val password: String
)

// commonMain/kotlin/com/example/shared/model/auth/AuthResponses.kt
@Serializable
data class AuthResponse(
    val user: User,
    val accessToken: String,
    val refreshToken: String,
    val expiresAt: Instant
)

@Serializable
data class RefreshTokenRequest(
    val refreshToken: String
)
```

## Validation

### Inline Validation

```kotlin
// commonMain/kotlin/com/example/shared/model/Validation.kt
@Serializable
data class Email(val value: String) {
    init {
        require(value.contains("@")) { "Invalid email format" }
        require(value.length > 5) { "Email too short" }
    }

    companion object {
        fun of(value: String?): Email? {
            return if (!value.isNullOrBlank()) Email(value) else null
        }
    }
}

@Serializable
data class PhoneNumber(val value: String) {
    init {
        require(value.matches(Regex("^\\+?[1-9]\\d{1,14}$"))) {
            "Invalid phone number format"
        }
    }
}
```

### Validation Result

```kotlin
// commonMain/kotlin/com/example/shared/model/ValidationError.kt
@Serializable
data class ValidationError(
    val field: String,
    val message: String
)

@Serializable
data class ValidationResult(
    val isValid: Boolean,
    val errors: List<ValidationError> = emptyList()
) {
    companion object {
        fun success() = ValidationResult(isValid = true)
        fun failure(errors: List<ValidationError>) = ValidationResult(
            isValid = false,
            errors = errors
        )
    }
}

// Usage in models
@Serializable
data class CreateUserRequest(
    val name: String,
    val email: String,
    val age: Int?
) {
    fun validate(): ValidationResult {
        val errors = buildList {
            if (name.isBlank()) {
                add(ValidationError("name", "Name is required"))
            }
            if (email.isBlank() || !email.contains("@")) {
                add(ValidationError("email", "Invalid email"))
            }
            if (age != null && age < 0) {
                add(ValidationError("age", "Age cannot be negative"))
            }
        }
        return if (errors.isEmpty()) ValidationResult.success()
        else ValidationResult.failure(errors)
    }
}
```

## Platform-Specific Fields

### Using Serial Names

```kotlin
// commonMain/kotlin/com/example/shared/model/PlatformData.kt
@Serializable
data class PlatformData(
    val platform: Platform,
    val deviceInfo: DeviceInfo
)

@Serializable
enum class Platform {
    ANDROID,
    IOS,
    DESKTOP,
    WEB
}

@Serializable
data class DeviceInfo(
    val model: String,
    val osVersion: String,
    val appVersion: String,
    // Platform-specific optional fields
    val pushToken: String? = null,
    val advertisingId: String? = null
)
```

### Custom Serializers

```kotlin
// commonMain/kotlin/com/example/shared/model/InstantSerializer.kt
object InstantSerializer : KSerializer<Instant> {
    override val descriptor: SerialDescriptor =
        PrimitiveSerialDescriptor("Instant", PrimitiveKind.LONG)

    override fun serialize(encoder: Encoder, value: Instant) {
        encoder.encodeLong(value.toEpochMilliseconds())
    }

    override fun deserialize(decoder: Decoder): Instant {
        return Instant.fromEpochMilliseconds(decoder.decodeLong())
    }
}

@Serializable
data class Event(
    val id: String,
    @Serializable(with = InstantSerializer::class)
    val timestamp: Instant
)
```

## JSON Configuration

```kotlin
// commonMain/kotlin/com/example/shared/serialization/JsonFactory.kt
object JsonFactory {
    val Default = Json {
        ignoreUnknownKeys = true
        isLenient = true
        encodeDefaults = false
        coerceInputValues = true
    }

    // Pretty printing for debug
    val Pretty = Json {
        ignoreUnknownKeys = true
        isLenient = true
        prettyPrint = true
        indent = "  "
    }

    // Strict parsing for API responses
    val Strict = Json {
        ignoreUnknownKeys = false
        isLenient = false
        encodeDefaults = false
        coerceInputValues = false
    }
}
```

## File Organization

```
shared/commonMain/kotlin/com/example/shared/
├── model/
│   ├── User.kt
│   ├── Item.kt
│   ├── Pagination.kt
│   ├── UiState.kt
│   └── Result.kt
├── model/auth/
│   ├── AuthRequests.kt
│   ├── AuthResponses.kt
│   └── UserProfile.kt
├── serialization/
│   ├── JsonFactory.kt
│   └── InstantSerializer.kt
└── validation/
    ├── ValidationResult.kt
    └── Validators.kt
```

## Best Practices

### ✅ DO

```kotlin
// ✅ Use immutable data classes
@Serializable
data class User(val id: String, val name: String)

// ✅ Use sealed classes for fixed types
@Serializable
sealed class Result

// ✅ Provide default values for optional fields
@Serializable
data class Item(
    val id: String,
    val description: String? = null
)

// ✅ Use value classes for type safety
@JvmInline
@Serializable
value class UserId(val value: String)

// ✅ Group related models in packages
model/
  auth/
  payment/
  social/
```

### ❌ DON'T

```kotlin
// ❌ Don't use platform-specific types
@Serializable
data class Event(val date: Date)  // Date is platform-specific
// Use Instant or LocalDateTime instead

// ❌ Don't include complex logic in models
@Serializable
data class User(val id: String) {
    // Heavy business logic doesn't belong here
    fun calculateSomethingComplex(): Int { ... }
}

// ❌ Don't make everything nullable
@Serializable
data class Item(
    val id: String?,
    val name: String?,
    val price: Double?
)  // Use Optional pattern or separate fields

// ❌ Don't use var in data classes
@Serializable
data class User(var name: String)  // Use val for immutability
```

## Testing

```kotlin
// commonTest/kotlin/ModelTest.kt
class ModelTest {
    @Test
    fun `serialize and deserialize user`() {
        val user = User(
            id = "123",
            name = "John Doe",
            email = "john@example.com",
            avatarUrl = null,
            createdAt = Clock.System.now(),
            lastActiveAt = null
        )

        val json = JsonFactory.Default.encodeToString(user)
        val restored = JsonFactory.Default.decodeFromString<User>(json)

        assertEquals(user, restored)
    }

    @Test
    fun `validation catches invalid email`() {
        val result = CreateUserRequest(
            name = "John",
            email = "not-an-email",
            age = null
        ).validate()

        assertFalse(result.isValid)
        assertTrue(result.errors.any { it.field == "email" })
    }
}
```

---

**Remember**: Shared models are your contract between platforms. Keep them simple, immutable, and focused on data.
