---
name: ktgbotapi
description: KTgBotAPI reference - use for Telegram Bot API methods, types, triggers, expectations, and library features
---

# KTgBotAPI Reference

Kotlin Multiplatform library for Telegram Bot API. Type-safe, coroutine-based.

## Setup

```kotlin
// build.gradle.kts
dependencies {
    implementation("dev.inmo:tgbotapi:18.2.2")
}
```

## Modules

| Module | Purpose |
|--------|---------|
| `tgbotapi.core` | Core types, requests |
| `tgbotapi.api` | API extension methods |
| `tgbotapi.utils` | Utilities, keyboard builders |
| `tgbotapi.behaviour_builder` | BehaviourBuilder DSL |
| `tgbotapi.behaviour_builder.fsm` | FSM integration |

## Quick Start

```kotlin
suspend fun main() {
    val bot = telegramBot(System.getenv("BOT_TOKEN"))

    bot.buildBehaviourWithLongPolling {
        onCommand("start") { reply(it, "Hello!") }
    }.join()
}
```

## Triggers Reference

### Commands

**CRITICAL: Understanding `requireOnlyCommandInMessage` parameter**

By default, `onCommand` has `requireOnlyCommandInMessage = true`, meaning it ONLY triggers when the message contains JUST the command with no additional text.

```kotlin
// DEFAULT BEHAVIOR - triggers ONLY for "/start" (no extra text)
onCommand("start") { message -> }

// This will NOT trigger for "/start hello" or "/warn @username"!
```

**For commands with arguments, you MUST use one of these approaches:**

```kotlin
// APPROACH 1: Set requireOnlyCommandInMessage = false
// Triggers for "/mute @username reason" - you parse args manually
onCommand("mute", requireOnlyCommandInMessage = false) { message ->
    val text = (message.content as TextContent).text
    val args = text.split(" ").drop(1)  // skip command
}

// APPROACH 2: Use onCommandWithArgs (recommended for simple args)
// Automatically sets requireOnlyCommandInMessage = false and parses args
onCommandWithArgs("echo") { message, args ->
    // args = arrayOf("hello", "world") for "/echo hello world"
    reply(message, args.joinToString(" "))
}

// APPROACH 3: Use onCommandWithNamedArgs for key=value format
onCommandWithNamedArgs("config") { message, args ->
    // args = listOf("key" to "value") for "/config key=value"
}
```

**Common patterns:**

```kotlin
onCommand("start") { message -> }                          // no args expected
onCommand("help", "info") { message -> }                   // multiple commands, no args
onCommand(Regex("set_.*")) { message -> }                  // regex pattern
onCommand("warn", requireOnlyCommandInMessage = false) { } // manual arg parsing
onCommandWithArgs("echo") { message, args -> }             // auto arg parsing
onDeepLink { message, deepLink -> }                        // t.me/bot?start=payload
onUnhandledCommand { message -> }                          // fallback for unknown commands
```

### Text

```kotlin
onText { message -> }
onText(initialFilter = { it.content.text.length > 10 }) { message -> }
onText(Regex("\\d+")) { message -> }
```

### Media

```kotlin
onPhoto { message -> }
onVideo { message -> }
onAudio { message -> }
onDocument { message -> }
onVoice { message -> }
onVideoNote { message -> }
onSticker { message -> }
onAnimation { message -> }
onMediaGroup { messages -> }                       // album
onVisualMediaGroup { messages -> }                 // photos/videos only
```

### Callbacks & Queries

```kotlin
onDataCallbackQuery { query -> }
onDataCallbackQuery(Regex("action:.*")) { query -> }
onInlineQuery { query -> }
onChosenInlineResult { result -> }
```

### Other Updates

```kotlin
onContact { message -> }
onLocation { message -> }
onPoll { poll -> }
onPollAnswer { answer -> }
onChatMemberUpdated { update -> }
onMyChatMemberUpdated { update -> }
onNewChatMembers { message -> }
onLeftChatMember { message -> }
```

## Expectations Reference

Wait for specific user input:

```kotlin
// Wait for text
val text = waitText().first()
val text = waitText { it.chat.id == chatId }.first()

// Wait for media
val photo = waitPhoto().first()
val document = waitDocument().first()

// Wait for callback
val callback = waitDataCallbackQuery().first()
val callback = waitDataCallbackQuery { it.data.startsWith("confirm:") }.first()

// With request (send message and wait)
val photo = waitPhoto(
    SendTextMessage(chatId, "Send me a photo")
).first()
```

## Sending Messages

```kotlin
// Text
sendMessage(chatId, "Hello")
sendTextMessage(chatId, "Hello", parseMode = ParseMode.HTML)
reply(message, "Reply text")

// With entities
send(chatId, buildEntities {
    bold("Bold") + " and " + italic("italic")
})

// Media
sendPhoto(chatId, InputFile.fromFile(File("photo.jpg")))
sendPhoto(chatId, InputFile.fromUrl("https://..."))
sendDocument(chatId, InputFile.fromFile(File("doc.pdf")))
sendVideo(chatId, InputFile.fromFile(File("video.mp4")))
sendAudio(chatId, InputFile.fromFile(File("audio.mp3")))
sendVoice(chatId, InputFile.fromFile(File("voice.ogg")))
sendSticker(chatId, InputFile.fromId(stickerFileId))

// Media group
sendMediaGroup(chatId, listOf(
    TelegramMediaPhoto(InputFile.fromFile(File("1.jpg"))),
    TelegramMediaPhoto(InputFile.fromFile(File("2.jpg")))
))

// Location
sendLocation(chatId, latitude = 55.75, longitude = 37.62)

// Contact
sendContact(chatId, phoneNumber = "+123456789", firstName = "John")
```

## Text Formatting

### buildEntities DSL

```kotlin
val text = buildEntities {
    bold("Bold") + "\n"
    italic("Italic") + "\n"
    underline("Underline") + "\n"
    strikethrough("Strike") + "\n"
    spoiler("Spoiler") + "\n"
    code("inline code") + "\n"
    pre("code block", language = "kotlin")
    link("Link", "https://example.com") + "\n"
    mention("username")
    textMention("User", userId)
    botCommand("start")
    hashtag("tag")
    cashtag("USD")
    email("test@example.com")
    phoneNumber("+123456789")
    regular("Plain text")
}
```

### Parse Modes

```kotlin
// HTML
sendTextMessage(chatId, """
    <b>Bold</b>, <i>italic</i>, <u>underline</u>
    <s>strikethrough</s>, <tg-spoiler>spoiler</tg-spoiler>
    <code>code</code>, <pre>block</pre>
    <a href="https://...">link</a>
""".trimIndent(), parseMode = ParseMode.HTML)

// MarkdownV2 (escape special chars: _*[]()~`>#+-=|{}.!)
sendTextMessage(chatId, """
    *bold*, _italic_, __underline__
    ~strikethrough~, ||spoiler||
    `code`, ```block```
    [link](https://...)
""".trimIndent(), parseMode = ParseMode.MarkdownV2)
```

## Reply Keyboard

```kotlin
val keyboard = replyKeyboard(
    resizeKeyboard = true,
    oneTimeKeyboard = true,
    inputFieldPlaceholder = "Choose option"
) {
    row {
        simpleButton("Button 1")
        simpleButton("Button 2")
    }
    row {
        requestContactButton("Share Contact")
        requestLocationButton("Share Location")
    }
    row {
        requestPollButton("Create Poll", type = RegularPoll)
        webAppButton("Web App", WebAppInfo("https://..."))
    }
}

sendMessage(chatId, "Menu:", replyMarkup = keyboard)

// Remove keyboard
sendMessage(chatId, "Done", replyMarkup = ReplyKeyboardRemove())
```

## Inline Keyboard

```kotlin
val keyboard = inlineKeyboard {
    row {
        dataButton("Action", "callback_data")
        urlButton("Link", "https://example.com")
    }
    row {
        webAppButton("Web App", WebAppInfo("https://..."))
        loginButton("Login", LoginUrl("https://..."))
    }
    row {
        inlineQueryInCurrentChatButton("Search", "query")
        inlineQueryInChosenChatButton("Search chat", "query")
    }
    row {
        payButton("Pay")
        gameButton("Play")
    }
}

sendMessage(chatId, "Actions:", replyMarkup = keyboard)
```

## Callback Queries

```kotlin
onDataCallbackQuery { query ->
    val data = query.data        // callback data string
    val message = query.message  // original message (nullable)
    val user = query.user        // user who clicked

    // Answer callback (removes loading indicator)
    answer(query)
    answer(query, "Notification text")
    answer(query, "Alert!", showAlert = true)

    // Edit original message
    edit(query.message!!, "New text")
    edit(query.message!!, replyMarkup = newKeyboard)

    // Delete original message
    delete(query.message!!)
}
```

## Inline Mode

```kotlin
onInlineQuery { query ->
    val searchQuery = query.query

    val results = listOf(
        InlineQueryResultArticle(
            id = "1",
            title = "Result Title",
            description = "Description",
            inputMessageContent = InputTextMessageContent("Selected: Result 1"),
            replyMarkup = inlineKeyboard { row { dataButton("Details", "d:1") } }
        ),
        InlineQueryResultPhoto(
            id = "2",
            photoUrl = "https://example.com/photo.jpg",
            thumbnailUrl = "https://example.com/thumb.jpg"
        ),
        InlineQueryResultGif(
            id = "3",
            gifUrl = "https://example.com/animation.gif",
            thumbnailUrl = "https://example.com/thumb.gif"
        )
    )

    answerInlineQuery(
        query,
        results,
        cacheTime = 300,
        isPersonal = false,
        button = InlineQueryResultsButton("Open Bot", StartParameter("param"))
    )
}

onChosenInlineResult { result ->
    val resultId = result.resultId
    val query = result.query
}
```

## FSM (Finite State Machine)

```kotlin
// Define states
sealed interface BotState : State {
    override val context: IdChatIdentifier
    data class WaitingName(override val context: IdChatIdentifier) : BotState
    data class WaitingAge(override val context: IdChatIdentifier, val name: String) : BotState
}

// Bot with FSM
bot.buildBehaviourWithFSMAndStartLongPolling<BotState> {

    onCommand("start") { message ->
        startChain(BotState.WaitingName(message.chat.id))
    }

    strictlyOn<BotState.WaitingName> { state ->
        send(state.context, "Enter your name:")
        val name = waitText { it.chat.id == state.context }.first().content.text
        BotState.WaitingAge(state.context, name)  // transition
    }

    strictlyOn<BotState.WaitingAge> { state ->
        send(state.context, "Enter your age:")
        val age = waitText { it.chat.id == state.context }.first().content.text
        send(state.context, "Name: ${state.name}, Age: $age")
        null  // end chain
    }
}.second.join()
```

## Chat Management

```kotlin
// Get chat info
val chat = getChat(chatId)

// Get chat member
val member = getChatMember(chatId, userId)

// Kick/ban
banChatMember(chatId, userId)
banChatMember(chatId, userId, untilDate = Instant.now() + 1.hours)

// Unban
unbanChatMember(chatId, userId)

// Restrict
restrictChatMember(chatId, userId, ChatPermissions(
    canSendMessages = false,
    canSendMediaMessages = false
))

// Promote
promoteChatMember(chatId, userId,
    canDeleteMessages = true,
    canPinMessages = true
)

// Set title
setChatAdministratorCustomTitle(chatId, userId, "Custom Title")
```

## File Operations

```kotlin
// Download file
val file = bot.downloadFile(fileId)
val bytes = bot.downloadFileToByteArray(fileId)

// Get file info
val fileInfo = getFile(fileId)
val filePath = fileInfo.filePath
```

## Bot Settings

```kotlin
// Get bot info
val me = getMe()

// Set commands
setMyCommands(listOf(
    BotCommand("start", "Start the bot"),
    BotCommand("help", "Show help")
))

// Set commands for specific scope
setMyCommands(
    commands = listOf(BotCommand("admin", "Admin panel")),
    scope = BotCommandScopeChat(adminChatId)
)

// Delete commands
deleteMyCommands()

// Set description
setMyDescription("Bot description")
setMyShortDescription("Short description")
```

## Error Handling

```kotlin
bot.buildBehaviourWithLongPolling(
    defaultExceptionsHandler = { throwable ->
        when (throwable) {
            is CommonBotException -> println("API error: ${throwable.message}")
            is CancellationException -> { /* ignore */ }
            else -> throwable.printStackTrace()
        }
    }
) {
    // handlers
}
```

## Types Quick Reference

| Type | Description |
|------|-------------|
| `ChatId` | Chat identifier (Long wrapper) |
| `UserId` | User identifier |
| `MessageId` | Message identifier |
| `FileId` | File identifier |
| `IdChatIdentifier` | Union of ChatId/UserId |
| `CommonMessage<T>` | Message with content type T |
| `TextContent` | Text message content |
| `PhotoContent` | Photo message content |
| `DocumentContent` | Document message content |
| `PrivateChat` | Private chat type |
| `GroupChat` | Group chat type |
| `SupergroupChat` | Supergroup chat type |
| `ChannelChat` | Channel chat type |
