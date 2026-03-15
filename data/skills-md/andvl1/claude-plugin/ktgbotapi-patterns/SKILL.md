---
name: ktgbotapi-patterns
description: Telegram bot architecture patterns - use for project structure, modular handlers, DI, callback models, keyboards, utilities
---

# KTgBotAPI Architecture Patterns

Patterns for organizing Telegram bot projects with ktgbotapi.

## Project Structure

```
src/main/kotlin/com/example/bot/
├── Application.kt              # Entry point
├── config/
│   ├── BotConfig.kt            # Bot configuration
│   ├── HttpClientConfig.kt     # Ktor client setup
│   └── KoinModules.kt          # DI modules
├── handlers/
│   ├── CommandHandlers.kt      # /start, /help, etc.
│   ├── MessageHandlers.kt      # Text message handlers
│   ├── CallbackHandlers.kt     # Inline button callbacks
│   └── MediaHandlers.kt        # Photo, document, etc.
├── keyboards/
│   ├── InlineKeyboards.kt      # Inline keyboard builders
│   └── ReplyKeyboards.kt       # Reply keyboard builders
├── fsm/
│   ├── States.kt               # FSM state definitions
│   └── StateHandlers.kt        # State transition handlers
├── api/
│   ├── BackendApiService.kt    # HTTP calls to backend (see ktor-client skill)
│   └── ApiModels.kt            # Request/Response DTOs
├── services/
│   ├── UserService.kt          # Business logic
│   └── NotificationService.kt
├── models/
│   ├── User.kt                 # Domain models
│   └── CallbackData.kt         # Callback payload models
└── utils/
    ├── Extensions.kt           # Useful extensions
    └── Formatters.kt           # Text formatting helpers
```

> **Note:** For backend API communication patterns, see the `ktor-client` skill.

## Modular Handler Pattern

### Application Entry Point

```kotlin
// Application.kt
suspend fun main() {
    val bot = telegramBot(System.getenv("BOT_TOKEN"))

    bot.buildBehaviourWithLongPolling(
        defaultExceptionsHandler = { logger.error("Bot error", it) }
    ) {
        setupCommandHandlers()
        setupMessageHandlers()
        setupCallbackHandlers()
        setupMediaHandlers()
    }.join()
}
```

### Handler Modules

```kotlin
// handlers/CommandHandlers.kt
suspend fun BehaviourContext.setupCommandHandlers() {
    onCommand("start") { message ->
        reply(message, "Welcome!", replyMarkup = ReplyKeyboards.main())
    }

    onCommand("help") { message ->
        reply(message, HelpTexts.commands())
    }

    onDeepLink { message, deepLink ->
        handleDeepLink(message, deepLink)
    }
}

// handlers/MessageHandlers.kt
suspend fun BehaviourContext.setupMessageHandlers() {
    onText(initialFilter = { it.content.text == "📋 Menu" }) { showMenu(it) }
    onText(initialFilter = { it.content.text == "⚙️ Settings" }) { showSettings(it) }
}

// handlers/CallbackHandlers.kt
suspend fun BehaviourContext.setupCallbackHandlers() {
    onDataCallbackQuery(Regex("menu:.*")) { handleMenuCallback(it) }
    onDataCallbackQuery(Regex("item:.*")) { handleItemCallback(it) }
    onDataCallbackQuery(Regex("page:.*")) { handlePaginationCallback(it) }
}
```

## Callback Data Models

Type-safe callback data parsing:

```kotlin
// models/CallbackData.kt
sealed class CallbackData {
    abstract fun encode(): String

    // Menu actions
    data class Menu(val action: String) : CallbackData() {
        override fun encode() = "m:$action"
    }

    // Item operations
    data class Item(val action: String, val id: String) : CallbackData() {
        override fun encode() = "i:$action:$id"
    }

    // Pagination
    data class Page(val list: String, val page: Int) : CallbackData() {
        override fun encode() = "p:$list:$page"
    }

    // Confirmation
    data class Confirm(val action: String, val id: String) : CallbackData() {
        override fun encode() = "c:$action:$id"
    }

    companion object {
        fun parse(data: String): CallbackData? {
            val parts = data.split(":")
            return when (parts.getOrNull(0)) {
                "m" -> Menu(parts[1])
                "i" -> Item(parts[1], parts[2])
                "p" -> Page(parts[1], parts[2].toInt())
                "c" -> Confirm(parts[1], parts[2])
                else -> null
            }
        }
    }
}

// Usage in handlers
suspend fun BehaviourContext.setupCallbackHandlers() {
    onDataCallbackQuery { query ->
        when (val cb = CallbackData.parse(query.data)) {
            is CallbackData.Menu -> handleMenu(query, cb.action)
            is CallbackData.Item -> handleItem(query, cb.action, cb.id)
            is CallbackData.Page -> handlePage(query, cb.list, cb.page)
            is CallbackData.Confirm -> handleConfirm(query, cb.action, cb.id)
            null -> answer(query, "Unknown action")
        }
    }
}

// Usage in keyboard builders
fun itemKeyboard(itemId: String) = inlineKeyboard {
    row {
        dataButton("✏️ Edit", CallbackData.Item("edit", itemId).encode())
        dataButton("🗑 Delete", CallbackData.Item("delete", itemId).encode())
    }
}
```

## Keyboard Builders

### Inline Keyboards Object

```kotlin
// keyboards/InlineKeyboards.kt
object InlineKeyboards {

    fun mainMenu() = inlineKeyboard {
        row { dataButton("📊 Statistics", "m:stats") }
        row {
            dataButton("👤 Profile", "m:profile")
            dataButton("⚙️ Settings", "m:settings")
        }
        row { urlButton("📖 Help", "https://example.com/help") }
    }

    fun confirmation(action: String, id: String) = inlineKeyboard {
        row {
            dataButton("✅ Confirm", "c:$action:$id")
            dataButton("❌ Cancel", "c:cancel:$id")
        }
    }

    fun pagination(list: String, current: Int, total: Int) = inlineKeyboard {
        row {
            if (current > 1) dataButton("◀️", "p:$list:${current - 1}")
            dataButton("$current / $total", "p:$list:$current")
            if (current < total) dataButton("▶️", "p:$list:${current + 1}")
        }
    }

    fun itemActions(id: String) = inlineKeyboard {
        row {
            dataButton("✏️ Edit", "i:edit:$id")
            dataButton("🗑 Delete", "i:delete:$id")
        }
        row { dataButton("◀️ Back", "m:back") }
    }

    fun backButton(target: String = "back") = inlineKeyboard {
        row { dataButton("◀️ Back", "m:$target") }
    }
}
```

### Reply Keyboards Object

```kotlin
// keyboards/ReplyKeyboards.kt
object ReplyKeyboards {

    fun main() = replyKeyboard(resizeKeyboard = true) {
        row {
            simpleButton("📋 Menu")
            simpleButton("⚙️ Settings")
        }
        row { simpleButton("❓ Help") }
    }

    fun cancel() = replyKeyboard(resizeKeyboard = true, oneTimeKeyboard = true) {
        row { simpleButton("❌ Cancel") }
    }

    fun yesNo() = replyKeyboard(resizeKeyboard = true, oneTimeKeyboard = true) {
        row {
            simpleButton("✅ Yes")
            simpleButton("❌ No")
        }
    }

    fun phoneRequest() = replyKeyboard(resizeKeyboard = true) {
        row { requestContactButton("📱 Share Phone") }
        row { simpleButton("❌ Cancel") }
    }

    fun remove() = ReplyKeyboardRemove()
}
```

## FSM Pattern

### State Definitions

```kotlin
// fsm/States.kt
sealed interface BotState : State {
    override val context: IdChatIdentifier

    // Registration flow
    data class AwaitingName(override val context: IdChatIdentifier) : BotState
    data class AwaitingEmail(override val context: IdChatIdentifier, val name: String) : BotState
    data class AwaitingConfirmation(
        override val context: IdChatIdentifier,
        val name: String,
        val email: String
    ) : BotState

    // Feedback flow
    data class AwaitingFeedback(override val context: IdChatIdentifier) : BotState
    data class AwaitingRating(override val context: IdChatIdentifier, val feedback: String) : BotState
}
```

### State Handlers

```kotlin
// fsm/StateHandlers.kt
suspend fun BehaviourContextWithFSM<BotState>.setupRegistrationFlow() {

    onCommand("register") { startChain(BotState.AwaitingName(it.chat.id)) }

    strictlyOn<BotState.AwaitingName> { state ->
        send(state.context, "Enter your name:", replyMarkup = ReplyKeyboards.cancel())

        val response = waitTextOrCancel(state.context) ?: return@strictlyOn null
        if (response.length < 2) {
            send(state.context, "Name too short. Try again:")
            return@strictlyOn state
        }

        BotState.AwaitingEmail(state.context, response)
    }

    strictlyOn<BotState.AwaitingEmail> { state ->
        send(state.context, "Enter your email:")

        val response = waitTextOrCancel(state.context) ?: return@strictlyOn null
        if (!response.contains("@")) {
            send(state.context, "Invalid email. Try again:")
            return@strictlyOn state
        }

        BotState.AwaitingConfirmation(state.context, state.name, response)
    }

    strictlyOn<BotState.AwaitingConfirmation> { state ->
        send(state.context, buildEntities {
            +"Confirm registration:\n\n"
            bold("Name: ") + state.name + "\n"
            bold("Email: ") + state.email
        }, replyMarkup = ReplyKeyboards.yesNo())

        val response = waitTextOrCancel(state.context) ?: return@strictlyOn null
        when (response) {
            "✅ Yes" -> {
                userService.register(state.name, state.email)
                send(state.context, "✅ Registered!", replyMarkup = ReplyKeyboards.main())
            }
            else -> send(state.context, "❌ Cancelled", replyMarkup = ReplyKeyboards.main())
        }
        null
    }
}

// Helper function
private suspend fun BehaviourContextWithFSM<BotState>.waitTextOrCancel(
    chatId: IdChatIdentifier
): String? {
    val message = waitText { it.chat.id == chatId }.first()
    return if (message.content.text == "❌ Cancel") {
        send(chatId, "Cancelled", replyMarkup = ReplyKeyboards.main())
        null
    } else {
        message.content.text
    }
}
```

## Dependency Injection with Koin

```kotlin
// config/KoinModules.kt
val botModule = module {
    single { telegramBot(getProperty("BOT_TOKEN")) }
}

// HTTP client for backend communication (see ktor-client skill)
val httpModule = module {
    single {
        HttpClient(CIO) {
            install(ContentNegotiation) { json() }
            install(HttpTimeout) { requestTimeoutMillis = 30_000 }
            defaultRequest {
                url(getProperty("BACKEND_URL"))
                header("X-API-Key", getProperty("API_KEY"))
            }
        }
    }
    singleOf(::BackendApiService)
}

val serviceModule = module {
    singleOf(::UserService)
    singleOf(::NotificationService)
}

// Application.kt
suspend fun main() {
    startKoin {
        properties(mapOf(
            "BOT_TOKEN" to System.getenv("BOT_TOKEN"),
            "BACKEND_URL" to System.getenv("BACKEND_URL"),
            "API_KEY" to System.getenv("API_KEY")
        ))
        modules(botModule, httpModule, serviceModule)
    }

    val bot: TelegramBot = get()
    val apiService: BackendApiService = get()

    bot.buildBehaviourWithLongPolling {
        setupCommandHandlers(apiService)
        setupCallbackHandlers(apiService)
    }.join()
}

// Pass dependencies to handlers
suspend fun BehaviourContext.setupCommandHandlers(api: BackendApiService) {
    onCommand("profile") { message ->
        val user = api.getUser(message.chat.id.chatId)
        reply(message, user?.let { "Name: ${it.name}" } ?: "Not registered")
    }
}
```

## Useful Extensions

```kotlin
// utils/Extensions.kt

// User display name
val CommonMessage<*>.userDisplayName: String
    get() = chat.asPrivateChat()?.let {
        listOfNotNull(it.firstName, it.lastName).joinToString(" ").ifEmpty { "User" }
    } ?: "User"

// Safe callback answer
suspend fun BehaviourContext.safeAnswer(
    query: CallbackQuery,
    text: String? = null,
    showAlert: Boolean = false
) = runCatching { answer(query, text, showAlert) }

// Edit or send new
suspend fun BehaviourContext.editOrSend(
    query: DataCallbackQuery,
    text: String,
    replyMarkup: InlineKeyboardMarkup? = null
) {
    runCatching {
        edit(query.message!!, text, replyMarkup = replyMarkup)
    }.onFailure {
        send(query.message!!.chat, text, replyMarkup = replyMarkup)
    }
}

// Chunked message sending
suspend fun BehaviourContext.sendLongMessage(
    chatId: IdChatIdentifier,
    text: String,
    chunkSize: Int = 4000
) {
    text.chunked(chunkSize).forEach { chunk ->
        sendMessage(chatId, chunk)
        delay(50)
    }
}

// Admin check
suspend fun BehaviourContext.isAdmin(chatId: IdChatIdentifier, userId: UserId): Boolean {
    return runCatching {
        val member = getChatMember(chatId, userId)
        member is Administrator || member is Creator
    }.getOrDefault(false)
}
```

## Error Handling Pattern

```kotlin
// utils/ErrorHandling.kt
class BotException(message: String, val userMessage: String = message) : Exception(message)
class ValidationException(message: String) : BotException(message)
class NotFoundException(message: String) : BotException(message, "Not found")

suspend fun BehaviourContext.withErrorHandling(
    message: CommonMessage<*>,
    block: suspend () -> Unit
) {
    try {
        block()
    } catch (e: ValidationException) {
        reply(message, "⚠️ ${e.userMessage}")
    } catch (e: NotFoundException) {
        reply(message, "❌ ${e.userMessage}")
    } catch (e: BotException) {
        reply(message, "❌ ${e.userMessage}")
    } catch (e: Exception) {
        logger.error("Unexpected error", e)
        reply(message, "❌ Something went wrong")
    }
}

// Usage
onCommand("action") { message ->
    withErrorHandling(message) {
        val result = service.performAction()
        reply(message, "✅ Done: $result")
    }
}
```

## Rate Limiter

```kotlin
// utils/RateLimiter.kt
class RateLimiter(private val maxRequests: Int = 30) {
    private val semaphore = Semaphore(maxRequests)

    suspend fun <T> withLimit(block: suspend () -> T): T {
        return semaphore.withPermit { block() }
    }
}

// Broadcast helper
suspend fun BehaviourContext.broadcast(
    userIds: List<Long>,
    text: String,
    rateLimiter: RateLimiter = RateLimiter(25)
): BroadcastResult {
    var success = 0
    var failed = 0

    userIds.forEach { userId ->
        rateLimiter.withLimit {
            runCatching {
                sendMessage(ChatId(userId), text)
                success++
            }.onFailure { failed++ }
        }
    }

    return BroadcastResult(success, failed)
}

data class BroadcastResult(val success: Int, val failed: Int)
```

## Testing Pattern

```kotlin
// Test with MockK
class CommandHandlersTest {
    private val mockBot = mockk<TelegramBot>(relaxed = true)

    @Test
    fun `start command sends welcome`() = runTest {
        val message = createTestMessage("/start")

        coEvery { mockBot.execute(any<SendTextMessage>()) } returns mockk()

        testBehaviourContext(mockBot) {
            setupCommandHandlers()
            // trigger handler
        }

        coVerify {
            mockBot.execute(match<SendTextMessage> {
                it.text.contains("Welcome")
            })
        }
    }
}

// Test helper
suspend fun testBehaviourContext(
    bot: TelegramBot,
    block: suspend BehaviourContext.() -> Unit
) {
    bot.buildBehaviour { block() }
}
```

## Spring Boot Integration

```kotlin
// config/TelegramBotConfig.kt
@ConfigurationProperties(prefix = "telegram")
data class TelegramProperties(
    val token: String,
    val adminIds: List<Long> = emptyList()
)

@Configuration
@EnableConfigurationProperties(TelegramProperties::class)
class TelegramBotConfig(private val props: TelegramProperties) {

    @Bean
    fun telegramBot(): TelegramBot = telegramBot(props.token)

    @Bean
    fun adminIds(): List<Long> = props.adminIds
}

// BotService.kt
@Service
class BotService(
    private val bot: TelegramBot,
    private val userService: UserService,
    private val adminIds: List<Long>
) {
    private val scope = CoroutineScope(Dispatchers.Default + SupervisorJob())

    @PostConstruct
    fun start() {
        scope.launch {
            bot.buildBehaviourWithLongPolling {
                setupCommandHandlers(userService, adminIds)
            }.join()
        }
    }

    @PreDestroy
    fun stop() {
        scope.cancel()
    }

    suspend fun sendNotification(chatId: Long, text: String) {
        bot.sendMessage(ChatId(chatId), text)
    }
}
```
