---
name: ktor-client
description: Ktor HTTP Client - use for backend API calls, REST requests, serialization, authentication, and client-server communication
---

# Ktor HTTP Client

HTTP client for Kotlin. Use when the bot needs to communicate with backend services.

## Setup

```kotlin
// build.gradle.kts
plugins {
    kotlin("plugin.serialization") version "2.0.0"
}

val ktorVersion = "3.1.1"

dependencies {
    implementation("io.ktor:ktor-client-core:$ktorVersion")
    implementation("io.ktor:ktor-client-cio:$ktorVersion")           // Engine (async)
    implementation("io.ktor:ktor-client-content-negotiation:$ktorVersion")
    implementation("io.ktor:ktor-serialization-kotlinx-json:$ktorVersion")
    implementation("io.ktor:ktor-client-logging:$ktorVersion")
    implementation("io.ktor:ktor-client-auth:$ktorVersion")

    // For testing
    testImplementation("io.ktor:ktor-client-mock:$ktorVersion")
}
```

## Client Configuration

```kotlin
import io.ktor.client.*
import io.ktor.client.engine.cio.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.logging.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json

val httpClient = HttpClient(CIO) {
    // JSON serialization
    install(ContentNegotiation) {
        json(Json {
            prettyPrint = true
            isLenient = true
            ignoreUnknownKeys = true
        })
    }

    // Logging
    install(Logging) {
        logger = Logger.DEFAULT
        level = LogLevel.INFO
        filter { request -> request.url.host.contains("api") }
        sanitizeHeader { header -> header == HttpHeaders.Authorization }
    }

    // Timeouts
    install(HttpTimeout) {
        requestTimeoutMillis = 30_000
        connectTimeoutMillis = 10_000
        socketTimeoutMillis = 30_000
    }

    // Default request config
    defaultRequest {
        url("https://api.your-project.example.com/api/v1/")
    }
}
```

## Basic Requests

### GET Request

```kotlin
import io.ktor.client.call.*
import io.ktor.client.request.*

// Simple GET
val response: String = client.get("https://api.example.com/data").body()

// GET with path parameter
val user: User = client.get("users/$userId").body()

// GET with query parameters
val users: List<User> = client.get("users") {
    parameter("page", 1)
    parameter("limit", 20)
    parameter("status", "active")
}.body()

// Alternative: using url builder
val users: List<User> = client.get("users") {
    url {
        parameter("page", 1)
        parameter("limit", 20)
    }
    headers {
        append(HttpHeaders.Accept, ContentType.Application.Json.toString())
    }
}.body()
```

### POST Request

```kotlin
import io.ktor.http.*

// POST with JSON body
@Serializable
data class CreateUserRequest(val name: String, val email: String)

val newUser: User = client.post("users") {
    contentType(ContentType.Application.Json)
    setBody(CreateUserRequest("John", "john@example.com"))
}.body()

// POST form data
val token: TokenResponse = client.post("auth/login") {
    contentType(ContentType.Application.FormUrlEncoded)
    setBody(FormDataContent(Parameters.build {
        append("username", "user")
        append("password", "pass")
    }))
}.body()
```

### PUT / PATCH / DELETE

```kotlin
// PUT
val updated: User = client.put("users/$userId") {
    contentType(ContentType.Application.Json)
    setBody(UpdateUserRequest(name = "New Name"))
}.body()

// PATCH
val patched: User = client.patch("users/$userId") {
    contentType(ContentType.Application.Json)
    setBody(mapOf("status" to "inactive"))
}.body()

// DELETE
client.delete("users/$userId")
```

## Authentication

### Bearer Token

```kotlin
val client = HttpClient(CIO) {
    install(Auth) {
        bearer {
            loadTokens {
                BearerTokens(accessToken = "your-token", refreshToken = "")
            }
        }
    }
}

// Or per-request
client.get("protected/resource") {
    bearerAuth("your-token")
}
```

### API Key Header

```kotlin
val client = HttpClient(CIO) {
    defaultRequest {
        header("X-API-Key", System.getenv("API_KEY"))
    }
}
```

### Custom Auth Interceptor

```kotlin
val client = HttpClient(CIO) {
    install(DefaultRequest) {
        val token = tokenProvider.getToken()
        header(HttpHeaders.Authorization, "Bearer $token")
    }
}
```

## API Service Pattern

```kotlin
// services/BackendApiService.kt
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.request.*
import io.ktor.http.*

class BackendApiService(
    private val client: HttpClient,
    private val baseUrl: String = System.getenv("BACKEND_URL")
) {

    // User operations
    suspend fun getUser(telegramId: Long): User? {
        return runCatching {
            client.get("$baseUrl/users/telegram/$telegramId").body<User>()
        }.getOrNull()
    }

    suspend fun createUser(telegramId: Long, name: String): User {
        return client.post("$baseUrl/users") {
            contentType(ContentType.Application.Json)
            setBody(CreateUserRequest(telegramId, name))
        }.body()
    }

    suspend fun updateUserSettings(userId: Long, settings: UserSettings): User {
        return client.put("$baseUrl/users/$userId/settings") {
            contentType(ContentType.Application.Json)
            setBody(settings)
        }.body()
    }

    // Chat/Message operations
    suspend fun saveMessage(chatId: Long, message: SaveMessageRequest): SavedMessage {
        return client.post("$baseUrl/chats/$chatId/messages") {
            contentType(ContentType.Application.Json)
            setBody(message)
        }.body()
    }

    suspend fun getMessages(chatId: Long, page: Int = 1): PaginatedResponse<SavedMessage> {
        return client.get("$baseUrl/chats/$chatId/messages") {
            parameter("page", page)
            parameter("limit", 20)
        }.body()
    }

    // Health check
    suspend fun healthCheck(): Boolean {
        return runCatching {
            client.get("$baseUrl/health").status.isSuccess()
        }.getOrDefault(false)
    }
}
```

## DTOs (Data Transfer Objects)

```kotlin
// models/ApiModels.kt
import kotlinx.serialization.Serializable

@Serializable
data class User(
    val id: Long,
    val telegramId: Long,
    val name: String,
    val settings: UserSettings? = null,
    val createdAt: String
)

@Serializable
data class CreateUserRequest(
    val telegramId: Long,
    val name: String
)

@Serializable
data class UserSettings(
    val notifications: Boolean = true,
    val language: String = "ru"
)

@Serializable
data class SaveMessageRequest(
    val telegramMessageId: Long,
    val text: String,
    val fromUserId: Long
)

@Serializable
data class SavedMessage(
    val id: Long,
    val text: String,
    val savedAt: String
)

@Serializable
data class PaginatedResponse<T>(
    val data: List<T>,
    val page: Int,
    val totalPages: Int,
    val totalItems: Int
)

@Serializable
data class ApiError(
    val code: String,
    val message: String
)
```

## Error Handling

### HttpResponseValidator (Recommended)

```kotlin
import io.ktor.client.plugins.*

val client = HttpClient(CIO) {
    install(ContentNegotiation) { json() }

    HttpResponseValidator {
        validateResponse { response ->
            when (response.status.value) {
                in 300..399 -> throw RedirectResponseException(response, "Redirect")
                in 400..499 -> throw ClientRequestException(response, "Client error: ${response.status}")
                in 500..599 -> throw ServerResponseException(response, "Server error: ${response.status}")
            }
        }

        handleResponseExceptionWithRequest { exception, request ->
            when (exception) {
                is ClientRequestException -> {
                    logger.warn("Client error for ${request.url}: ${exception.message}")
                }
                is ServerResponseException -> {
                    logger.error("Server error for ${request.url}: ${exception.message}")
                }
            }
        }
    }
}
```

### Custom Exception Pattern

```kotlin
import io.ktor.client.call.*
import io.ktor.client.statement.*
import io.ktor.http.*

class ApiException(
    val statusCode: HttpStatusCode,
    val errorBody: ApiError?
) : Exception("API error: $statusCode - ${errorBody?.message}")

// Extension for safe API calls
suspend inline fun <reified T> HttpResponse.bodyOrThrow(): T {
    if (status.isSuccess()) {
        return body<T>()
    }

    val error = runCatching { body<ApiError>() }.getOrNull()
    throw ApiException(status, error)
}

// Usage with error handling
class BackendApiService(private val client: HttpClient) {

    suspend fun getUser(telegramId: Long): Result<User> = runCatching {
        client.get("users/telegram/$telegramId").bodyOrThrow<User>()
    }

    suspend fun createUser(request: CreateUserRequest): Result<User> = runCatching {
        client.post("users") {
            contentType(ContentType.Application.Json)
            setBody(request)
        }.bodyOrThrow<User>()
    }
}

// In bot handler
onCommand("profile") { message ->
    val userId = message.from?.id?.chatId ?: return@onCommand

    when (val result = apiService.getUser(userId)) {
        is Result.Success -> reply(message, "Profile: ${result.value.name}")
        is Result.Failure -> {
            val error = result.exception
            if (error is ApiException && error.statusCode == HttpStatusCode.NotFound) {
                reply(message, "Profile not found. Use /start to register.")
            } else {
                reply(message, "Error loading profile. Try again later.")
                logger.error("API error", error)
            }
        }
    }
}
```

## Retry Logic

### Global Retry Configuration

```kotlin
import io.ktor.client.plugins.*

val client = HttpClient(CIO) {
    install(HttpRequestRetry) {
        retryOnServerErrors(maxRetries = 3)
        retryOnExceptionIf(maxRetries = 3) { _, cause ->
            cause is java.io.IOException
        }
        exponentialDelay()

        // Custom retry condition
        retryIf { request, response ->
            response.status == HttpStatusCode.TooManyRequests
        }

        // Custom delay
        delayMillis { retry ->
            retry * 2000L  // 2s, 4s, 6s...
        }
    }
}
```

### Per-Request Retry

```kotlin
val client = HttpClient(CIO) {
    install(HttpRequestRetry) {
        noRetry()  // Disable global retry
    }
}

// Override for specific request
client.get("https://api.example.com/data") {
    retry {
        retryOnServerErrors(maxRetries = 5)
        constantDelay(millis = 500)
    }
}
```

### Manual Retry Helper

```kotlin
suspend fun <T> retryable(
    times: Int = 3,
    delayMs: Long = 1000,
    block: suspend () -> T
): T {
    repeat(times - 1) { attempt ->
        runCatching { return block() }
            .onFailure { logger.warn("Attempt ${attempt + 1} failed: ${it.message}") }
        kotlinx.coroutines.delay(delayMs * (attempt + 1))
    }
    return block()
}
```

## Integration with Bot

```kotlin
// config/Dependencies.kt
val httpClient = HttpClient(CIO) {
    install(ContentNegotiation) { json() }
    install(HttpTimeout) {
        requestTimeoutMillis = 30_000
    }
    defaultRequest {
        url(System.getenv("BACKEND_URL"))
        header("X-API-Key", System.getenv("API_KEY"))
    }
}

val apiService = BackendApiService(httpClient)

// handlers/CommandHandlers.kt
suspend fun BehaviourContext.setupCommandHandlers(api: BackendApiService) {

    onCommand("start") { message ->
        val telegramId = message.from?.id?.chatId ?: return@onCommand
        val name = message.from?.firstName ?: "User"

        val user = api.getUser(telegramId) ?: api.createUser(telegramId, name)
        reply(message, "Welcome, ${user.name}!")
    }

    onCommand("save") { message ->
        val replyTo = message.replyTo ?: run {
            reply(message, "Reply to a message to save it")
            return@onCommand
        }

        val saved = api.saveMessage(
            chatId = message.chat.id.chatId,
            message = SaveMessageRequest(
                telegramMessageId = replyTo.messageId,
                text = (replyTo.content as? TextContent)?.text ?: "",
                fromUserId = replyTo.from?.id?.chatId ?: 0
            )
        )

        reply(message, "Message saved! ID: ${saved.id}")
    }

    onCommand("history") { message ->
        val messages = api.getMessages(message.chat.id.chatId)

        if (messages.data.isEmpty()) {
            reply(message, "No saved messages yet")
            return@onCommand
        }

        val text = messages.data.joinToString("\n\n") { msg ->
            "• ${msg.text.take(100)}..."
        }

        reply(message, "Saved messages:\n\n$text")
    }
}
```

## Testing

```kotlin
import io.ktor.client.engine.mock.*
import io.ktor.http.*

@Test
fun `getUser returns user when exists`() = runTest {
    val mockEngine = MockEngine { request ->
        respond(
            content = """{"id":1,"telegramId":123,"name":"Test","createdAt":"2024-01-01"}""",
            status = HttpStatusCode.OK,
            headers = headersOf(HttpHeaders.ContentType, "application/json")
        )
    }

    val client = HttpClient(mockEngine) {
        install(ContentNegotiation) { json() }
    }

    val api = BackendApiService(client, "https://api.test")
    val user = api.getUser(123)

    assertNotNull(user)
    assertEquals("Test", user?.name)
}

@Test
fun `getUser returns null when not found`() = runTest {
    val mockEngine = MockEngine {
        respond(
            content = """{"code":"NOT_FOUND","message":"User not found"}""",
            status = HttpStatusCode.NotFound,
            headers = headersOf(HttpHeaders.ContentType, "application/json")
        )
    }

    val client = HttpClient(mockEngine) {
        install(ContentNegotiation) { json() }
    }

    val api = BackendApiService(client, "https://api.test")
    val user = api.getUser(999)

    assertNull(user)
}
```

## Client Lifecycle

```kotlin
// Proper client shutdown
class BotApplication : AutoCloseable {
    private val httpClient = HttpClient(CIO) { /* config */ }
    private val apiService = BackendApiService(httpClient)

    suspend fun start() {
        val bot = telegramBot(System.getenv("BOT_TOKEN"))
        bot.buildBehaviourWithLongPolling {
            setupCommandHandlers(apiService)
        }.join()
    }

    override fun close() {
        httpClient.close()
    }
}

// Main
fun main() = runBlocking {
    BotApplication().use { app ->
        app.start()
    }
}
```
