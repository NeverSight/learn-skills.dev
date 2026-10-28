---
name: pokeclaw-android-ai-agent
description: PokeClaw (PocketClaw) — on-device Android AI phone agent using Gemma 4 via LiteRT-LM with tool calling, accessibility automation, and optional cloud models.
triggers:
  - "set up PokeClaw on Android"
  - "build on-device AI phone agent"
  - "add tool calling to LiteRT LLM"
  - "automate Android with local LLM"
  - "implement accessibility agent Kotlin"
  - "create auto-reply bot with on-device AI"
  - "integrate Gemma 4 Android automation"
  - "write PokeClaw skill or tool"
---

# PokeClaw Android AI Agent

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

PokeClaw is an open-source Android app that runs Gemma 4 entirely on-device via [LiteRT-LM](https://ai.google.dev/edge/litert/llm/overview) with native tool calling. The LLM reads the screen as a UI tree, selects tools (tap, swipe, type, open app, send message, etc.), executes them through Android Accessibility Services, observes the result, and loops until the task is complete — no cloud, no API key required for local mode.

---

## Architecture Overview

```
User prompt
    │
    ▼
TaskOrchestrator          ← manages task lifecycle & session history
    │
    ▼
LLMEngine (LiteRT-LM)     ← Gemma 4 on-device, tool-call aware
    │  tool_calls[]
    ▼
ToolDispatcher            ← routes to concrete tool implementations
    │
    ├── AccessibilityTool  ← tap / swipe / long_press / input_text
    ├── AppLaunchTool      ← open_app
    ├── ScreenReaderTool   ← get_screen_info / take_screenshot
    ├── MessagingTool      ← send_message / auto_reply
    └── FinishTool         ← finish (signals task done)
         │
         ▼
    Android Accessibility Service / UI Automator
```

---

## Installation / Setup

### 1. Clone the repo

```bash
git clone https://github.com/agents-io/PokeClaw.git
cd PokeClaw
```

### 2. Open in Android Studio

- Android Studio Hedgehog or newer recommended
- SDK: Android 9+ (API 28), target API 34+
- Kotlin 1.9+

### 3. Add LiteRT-LM dependency

In `app/build.gradle.kts`:

```kotlin
dependencies {
    // LiteRT-LM for on-device LLM inference with tool calling
    implementation("com.google.ai.edge.litert:litert-lm:1.0.0")

    // Coroutines for async inference
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3")

    // JSON for tool-call serialization
    implementation("org.json:json:20231013")
}
```

### 4. AndroidManifest.xml permissions

```xml
<!-- Required: accessibility for UI control -->
<uses-permission android:name="android.permission.BIND_ACCESSIBILITY_SERVICE" />

<!-- Required: read notifications for auto-reply -->
<uses-permission android:name="android.permission.BIND_NOTIFICATION_LISTENER_SERVICE" />

<!-- Optional: foreground service for background tasks -->
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />

<!-- Accessibility service declaration -->
<service
    android:name=".accessibility.PokeAccessibilityService"
    android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE"
    android:exported="false">
    <intent-filter>
        <action android:name="android.accessibilityservice.AccessibilityService" />
    </intent-filter>
    <meta-data
        android:name="android.accessibilityservice"
        android:resource="@xml/accessibility_service_config" />
</service>
```

`res/xml/accessibility_service_config.xml`:

```xml
<accessibility-service xmlns:android="http://schemas.android.com/apk/res/android"
    android:accessibilityEventTypes="typeAllMask"
    android:accessibilityFeedbackType="feedbackGeneric"
    android:accessibilityFlags="flagDefault|flagRetrieveInteractiveWindows|flagRequestEnhancedWebAccessibility"
    android:canRetrieveWindowContent="true"
    android:canPerformGestures="true"
    android:notificationTimeout="100"
    android:description="@string/accessibility_service_description" />
```

### 5. Build & install APK

```bash
./gradlew assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk
```

Or download the [latest release APK](https://github.com/agents-io/PokeClaw/releases/latest).

---

## Core Concepts

### Tool Definition

Tools are declared as JSON schemas that LiteRT-LM uses for structured output. Define a tool:

```kotlin
// domain/tools/ToolDefinition.kt
data class ToolDefinition(
    val name: String,
    val description: String,
    val parameters: ToolParameters
)

data class ToolParameters(
    val type: String = "object",
    val properties: Map<String, ToolProperty>,
    val required: List<String>
)

data class ToolProperty(
    val type: String,
    val description: String,
    val enum: List<String>? = null
)
```

### Registering Tools with LiteRT-LM

```kotlin
// llm/LLMEngine.kt
import com.google.ai.edge.litert.lm.LiteRtLm
import com.google.ai.edge.litert.lm.InferenceOptions
import com.google.ai.edge.litert.lm.ToolConfig

class LLMEngine(private val context: Context) {

    private lateinit var lm: LiteRtLm

    suspend fun initialize(modelPath: String) {
        lm = LiteRtLm.create(
            context = context,
            modelPath = modelPath,
            inferenceOptions = InferenceOptions.builder()
                .setMaxTokens(2048)
                .setTemperature(0.1f)   // low temp for reliable tool calls
                .setTopK(40)
                .build()
        )
    }

    fun buildToolConfigs(): List<ToolConfig> {
        return listOf(
            ToolConfig.fromJson(tapToolJson()),
            ToolConfig.fromJson(inputTextToolJson()),
            ToolConfig.fromJson(openAppToolJson()),
            ToolConfig.fromJson(getScreenInfoToolJson()),
            ToolConfig.fromJson(sendMessageToolJson()),
            ToolConfig.fromJson(finishToolJson())
        )
    }

    private fun tapToolJson() = """
    {
      "name": "tap",
      "description": "Tap a UI element by its resource ID, content description, or screen coordinates.",
      "parameters": {
        "type": "object",
        "properties": {
          "target": {
            "type": "string",
            "description": "Resource ID, content-desc, or visible text of the element to tap."
          },
          "x": { "type": "number", "description": "Screen X coordinate (optional)." },
          "y": { "type": "number", "description": "Screen Y coordinate (optional)." }
        },
        "required": ["target"]
      }
    }
    """.trimIndent()

    private fun inputTextToolJson() = """
    {
      "name": "input_text",
      "description": "Type text into the currently focused or specified text field.",
      "parameters": {
        "type": "object",
        "properties": {
          "text": { "type": "string", "description": "Text to type." },
          "target": { "type": "string", "description": "Optional: resource ID of the target field." }
        },
        "required": ["text"]
      }
    }
    """.trimIndent()

    private fun openAppToolJson() = """
    {
      "name": "open_app",
      "description": "Launch an installed app by its name or package name.",
      "parameters": {
        "type": "object",
        "properties": {
          "app_name": { "type": "string", "description": "Human-readable app name, e.g. 'WhatsApp'." },
          "package_name": { "type": "string", "description": "Optional explicit package, e.g. 'com.whatsapp'." }
        },
        "required": ["app_name"]
      }
    }
    """.trimIndent()

    private fun getScreenInfoToolJson() = """
    {
      "name": "get_screen_info",
      "description": "Return a text representation of all interactive UI elements on the current screen.",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
    """.trimIndent()

    private fun sendMessageToolJson() = """
    {
      "name": "send_message",
      "description": "Send a chat/SMS message to a contact. Handles: open app, find contact, type, send.",
      "parameters": {
        "type": "object",
        "properties": {
          "app": { "type": "string", "description": "Messaging app name, e.g. 'WhatsApp'." },
          "contact": { "type": "string", "description": "Contact name or phone number." },
          "message": { "type": "string", "description": "Message body to send." }
        },
        "required": ["app", "contact", "message"]
      }
    }
    """.trimIndent()

    private fun finishToolJson() = """
    {
      "name": "finish",
      "description": "Signal that the task is complete. Include a summary of what was done.",
      "parameters": {
        "type": "object",
        "properties": {
          "summary": { "type": "string", "description": "Brief summary of completed actions." }
        },
        "required": ["summary"]
      }
    }
    """.trimIndent()
}
```

---

## Accessibility Service Implementation

```kotlin
// accessibility/PokeAccessibilityService.kt
class PokeAccessibilityService : AccessibilityService() {

    companion object {
        var instance: PokeAccessibilityService? = null
            private set
    }

    override fun onServiceConnected() {
        super.onServiceConnected()
        instance = this
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent?) { /* optional monitoring */ }
    override fun onInterrupt() {}

    // ── Screen reading ──────────────────────────────────────────────

    fun getScreenInfo(): String {
        val root = rootInActiveWindow ?: return "Screen unavailable"
        return buildString {
            appendNode(root, 0)
        }
    }

    private fun StringBuilder.appendNode(node: AccessibilityNodeInfo, depth: Int) {
        val indent = "  ".repeat(depth)
        val text = node.text?.toString()?.trim()
        val desc = node.contentDescription?.toString()?.trim()
        val resId = node.viewIdResourceName
        val cls = node.className?.toString()?.substringAfterLast('.')

        if (!text.isNullOrEmpty() || !desc.isNullOrEmpty()) {
            append("$indent[$cls")
            if (!resId.isNullOrEmpty()) append(" id=$resId")
            if (!text.isNullOrEmpty()) append(" text=\"$text\"")
            if (!desc.isNullOrEmpty()) append(" desc=\"$desc\"")
            if (node.isClickable) append(" clickable=true")
            if (node.isEditable) append(" editable=true")
            appendLine("]")
        }

        for (i in 0 until node.childCount) {
            node.getChild(i)?.let { appendNode(it, depth + 1) }
        }
    }

    // ── Tap ─────────────────────────────────────────────────────────

    fun tap(target: String?, x: Float? = null, y: Float? = null): Boolean {
        if (x != null && y != null) {
            return performTapGesture(x, y)
        }
        val root = rootInActiveWindow ?: return false
        val node = findNode(root, target ?: return false)
        return node?.performAction(AccessibilityNodeInfo.ACTION_CLICK) ?: false
    }

    private fun performTapGesture(x: Float, y: Float): Boolean {
        val path = Path().apply { moveTo(x, y) }
        val stroke = GestureDescription.StrokeDescription(path, 0, 50)
        val gesture = GestureDescription.Builder().addStroke(stroke).build()
        return dispatchGesture(gesture, null, null)
    }

    private fun findNode(root: AccessibilityNodeInfo, target: String): AccessibilityNodeInfo? {
        // Try by text
        root.findAccessibilityNodeInfosByText(target).firstOrNull()?.let { return it }
        // Try by viewId
        root.findAccessibilityNodeInfosByViewId(target).firstOrNull()?.let { return it }
        // Try by content-desc (recursive)
        return findByContentDesc(root, target)
    }

    private fun findByContentDesc(node: AccessibilityNodeInfo, target: String): AccessibilityNodeInfo? {
        if (node.contentDescription?.toString()?.contains(target, ignoreCase = true) == true) return node
        for (i in 0 until node.childCount) {
            node.getChild(i)?.let { findByContentDesc(it, target) }?.let { return it }
        }
        return null
    }

    // ── Swipe ───────────────────────────────────────────────────────

    fun swipe(startX: Float, startY: Float, endX: Float, endY: Float, durationMs: Long = 300): Boolean {
        val path = Path().apply {
            moveTo(startX, startY)
            lineTo(endX, endY)
        }
        val stroke = GestureDescription.StrokeDescription(path, 0, durationMs)
        val gesture = GestureDescription.Builder().addStroke(stroke).build()
        return dispatchGesture(gesture, null, null)
    }

    // ── Type text ───────────────────────────────────────────────────

    fun inputText(text: String, targetResId: String? = null): Boolean {
        val root = rootInActiveWindow ?: return false
        val node = if (targetResId != null) {
            root.findAccessibilityNodeInfosByViewId(targetResId).firstOrNull()
        } else {
            findFocusedEditText(root)
        } ?: return false

        node.performAction(AccessibilityNodeInfo.ACTION_FOCUS)
        val args = Bundle().apply {
            putString(AccessibilityNodeInfo.ACTION_ARGUMENT_SET_TEXT_CHARSEQUENCE, text)
        }
        return node.performAction(AccessibilityNodeInfo.ACTION_SET_TEXT, args)
    }

    private fun findFocusedEditText(node: AccessibilityNodeInfo): AccessibilityNodeInfo? {
        if (node.isEditable && node.isFocused) return node
        if (node.isEditable) return node   // fallback: first editable
        for (i in 0 until node.childCount) {
            node.getChild(i)?.let { findFocusedEditText(it) }?.let { return it }
        }
        return null
    }
}
```

---

## Task Orchestrator

```kotlin
// agent/TaskOrchestrator.kt
class TaskOrchestrator(
    private val llmEngine: LLMEngine,
    private val toolDispatcher: ToolDispatcher,
    private val screenReader: ScreenReaderTool
) {

    data class Message(val role: String, val content: String)

    private val history = mutableListOf<Message>()
    private val maxSteps = 20

    suspend fun runTask(userPrompt: String): String = withContext(Dispatchers.IO) {
        history.clear()
        history.add(Message("system", buildSystemPrompt()))
        history.add(Message("user", userPrompt))

        for (step in 1..maxSteps) {
            val response = llmEngine.chat(history, toolConfigs = llmEngine.buildToolConfigs())

            // No tool call → plain text reply, done
            if (response.toolCalls.isEmpty()) {
                return@withContext response.text ?: "Task complete."
            }

            // Execute each tool call
            val toolResults = mutableListOf<String>()
            for (call in response.toolCalls) {
                val result = toolDispatcher.dispatch(call.name, call.arguments)
                toolResults.add("Tool ${call.name} → $result")

                if (call.name == "finish") {
                    return@withContext call.arguments.optString("summary", "Done.")
                }
            }

            // Feed results back as assistant + tool turn
            history.add(Message("assistant", response.text ?: "(tool calls)"))
            history.add(Message("tool", toolResults.joinToString("\n")))
        }

        "Task stopped: max steps ($maxSteps) reached."
    }

    private fun buildSystemPrompt() = """
        You are PokeClaw, an AI agent that controls an Android phone.
        You have access to tools: tap, swipe, input_text, open_app, get_screen_info, send_message, finish.
        
        Workflow:
        1. Call get_screen_info to understand the current screen before acting.
        2. Pick the most direct tool to make progress.
        3. After each action, verify with get_screen_info if needed.
        4. Call finish when the task is complete with a brief summary.
        
        Rules:
        - Never guess coordinates; use element IDs or text labels when possible.
        - If an action fails, read the screen and adapt.
        - Do not loop more than 3 times on the same element.
        - Keep responses concise; the phone has limited memory.
    """.trimIndent()
}
```

---

## Tool Dispatcher

```kotlin
// agent/ToolDispatcher.kt
class ToolDispatcher(
    private val accessibilityService: PokeAccessibilityService,
    private val context: Context
) {

    fun dispatch(toolName: String, args: JSONObject): String {
        return try {
            when (toolName) {
                "tap" -> handleTap(args)
                "swipe" -> handleSwipe(args)
                "input_text" -> handleInputText(args)
                "open_app" -> handleOpenApp(args)
                "get_screen_info" -> accessibilityService.getScreenInfo()
                "send_message" -> handleSendMessage(args)
                "finish" -> "FINISH: ${args.optString("summary")}"
                else -> "Unknown tool: $toolName"
            }
        } catch (e: Exception) {
            "Error in $toolName: ${e.message}"
        }
    }

    private fun handleTap(args: JSONObject): String {
        val target = args.optString("target").takeIf { it.isNotEmpty() }
        val x = args.optDouble("x").takeIf { !it.isNaN() }?.toFloat()
        val y = args.optDouble("y").takeIf { !it.isNaN() }?.toFloat()
        val success = accessibilityService.tap(target, x, y)
        return if (success) "Tapped '$target'" else "Tap failed for '$target'"
    }

    private fun handleSwipe(args: JSONObject): String {
        val sx = args.getDouble("start_x").toFloat()
        val sy = args.getDouble("start_y").toFloat()
        val ex = args.getDouble("end_x").toFloat()
        val ey = args.getDouble("end_y").toFloat()
        val success = accessibilityService.swipe(sx, sy, ex, ey)
        return if (success) "Swiped ($sx,$sy)→($ex,$ey)" else "Swipe failed"
    }

    private fun handleInputText(args: JSONObject): String {
        val text = args.getString("text")
        val target = args.optString("target").takeIf { it.isNotEmpty() }
        val success = accessibilityService.inputText(text, target)
        return if (success) "Typed: \"$text\"" else "Input failed"
    }

    private fun handleOpenApp(args: JSONObject): String {
        val appName = args.getString("app_name")
        val pkgName = args.optString("package_name").takeIf { it.isNotEmpty() }
            ?: resolvePackageName(appName)
            ?: return "App '$appName' not found"

        val intent = context.packageManager.getLaunchIntentForPackage(pkgName)
            ?: return "Cannot launch '$pkgName'"
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        context.startActivity(intent)
        return "Launched $appName ($pkgName)"
    }

    private fun handleSendMessage(args: JSONObject): String {
        val app = args.getString("app")
        val contact = args.getString("contact")
        val message = args.getString("message")
        // Delegates to MessagingSkill which orchestrates the multi-step flow
        return MessagingSkill(accessibilityService, context)
            .sendMessage(app, contact, message)
    }

    private fun resolvePackageName(appName: String): String? {
        val pm = context.packageManager
        val packages = pm.getInstalledApplications(PackageManager.GET_META_DATA)
        return packages.firstOrNull {
            pm.getApplicationLabel(it).toString().equals(appName, ignoreCase = true)
        }?.packageName
    }
}
```

---

## Skills System

Skills are reusable multi-step workflows. Write a skill as a Kotlin class or (upcoming) a plain-text `.skill` file.

### Built-in skill example: Auto-Reply

```kotlin
// skills/AutoReplySkill.kt
class AutoReplySkill(
    private val accessibility: PokeAccessibilityService,
    private val llmEngine: LLMEngine,
    private val contact: String,
    private val app: String = "WhatsApp"
) {

    // Called when a new message notification arrives from `contact`
    suspend fun handleIncomingMessage(notificationText: String): String {
        // Step 1: Open the chat
        val dispatcher = ToolDispatcher(accessibility, accessibility)
        dispatcher.dispatch("open_app", JSONObject().put("app_name", app))
        delay(1500)

        // Step 2: Read the full conversation visible on screen
        val screenInfo = accessibility.getScreenInfo()

        // Step 3: Generate a context-aware reply using the LLM
        val reply = llmEngine.generateReply(
            systemPrompt = "You are replying on behalf of the user. Be brief and natural.",
            context = "Conversation visible on screen:\n$screenInfo\n\nLatest message: $notificationText",
            instruction = "Write a short, friendly reply."
        )

        // Step 4: Send the reply
        dispatcher.dispatch(
            "send_message",
            JSONObject()
                .put("app", app)
                .put("contact", contact)
                .put("message", reply)
        )

        return "Auto-replied to $contact: \"$reply\""
    }
}
```

### Skill as a text recipe (upcoming format)

```
# morning-briefing.skill
name: Morning Briefing
description: Summarize weather, calendar, and email every morning.

steps:
  1. open_app(app_name="Weather")
  2. get_screen_info() -> weather_info
  3. open_app(app_name="Calendar")
  4. get_screen_info() -> calendar_info
  5. open_app(app_name="Gmail")
  6. get_screen_info() -> email_info
  7. finish(summary="Weather: {weather_info}\nCalendar: {calendar_info}\nEmail: {email_info}")
```

---

## Cloud Mode (Optional)

When stronger reasoning is needed, swap the LLM backend. The tool interface stays identical.

```kotlin
// llm/CloudLLMEngine.kt — example with OpenAI-compatible endpoint
class CloudLLMEngine(
    private val apiKey: String = System.getenv("POKECLAW_CLOUD_API_KEY") ?: "",
    private val endpoint: String = System.getenv("POKECLAW_CLOUD_ENDPOINT")
        ?: "https://api.openai.com/v1"
) : LLMBackend {

    override suspend fun chat(
        messages: List<TaskOrchestrator.Message>,
        toolConfigs: List<ToolConfig>
    ): LLMResponse {
        // Build request body with tool schemas, call endpoint, parse response
        // The ToolDispatcher and orchestrator are unchanged
        TODO("Implement HTTP call with OkHttp or Ktor")
    }
}
```

Switch backends in your DI setup — everything else is identical because `ToolDispatcher` is backend-agnostic.

---

## Model Download (Local Mode)

```kotlin
// model/ModelManager.kt
class ModelManager(private val context: Context) {

    // Default model: Gemma 4 E2B LiteRT (~2.6 GB)
    private val modelUrl = "https://huggingface.co/google/gemma-4-e2b-it-litert/resolve/main/model.litertlm"
    private val modelFile get() = File(context.filesDir, "gemma4_e2b.litertlm")

    val isDownloaded get() = modelFile.exists() && modelFile.length() > 1_000_000_000L

    suspend fun downloadModel(onProgress: (Float) -> Unit) = withContext(Dispatchers.IO) {
        val connection = URL(modelUrl).openConnection() as HttpURLConnection
        val total = connection.contentLengthLong
        var downloaded = 0L

        connection.inputStream.use { input ->
            modelFile.outputStream().use { output ->
                val buffer = ByteArray(8192)
                var bytes: Int
                while (input.read(buffer).also { bytes = it } != -1) {
                    output.write(buffer, 0, bytes)
                    downloaded += bytes
                    onProgress(downloaded.toFloat() / total)
                }
            }
        }
    }

    fun getModelPath(): String = modelFile.absolutePath
}
```

To use a custom `.litertlm` model, place it in `context.filesDir` and call `llmEngine.initialize(customPath)`.

---

## ViewModel Integration

```kotlin
// ui/TaskViewModel.kt
@HiltViewModel
class TaskViewModel @Inject constructor(
    private val orchestrator: TaskOrchestrator
) : ViewModel() {

    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages.asStateFlow()

    private val _isRunning = MutableStateFlow(false)
    val isRunning: StateFlow<Boolean> = _isRunning.asStateFlow()

    fun submitTask(prompt: String) {
        viewModelScope.launch {
            _isRunning.value = true
            _messages.update { it + ChatMessage("user", prompt) }

            val result = try {
                orchestrator.runTask(prompt)
            } catch (e: Exception) {
                "Error: ${e.message}"
            }

            _messages.update { it + ChatMessage("agent", result) }
            _isRunning.value = false
        }
    }
}

data class ChatMessage(val role: String, val text: String)
```

---

## Quick-Task Cards

Surface pre-built tasks in the UI:

```kotlin
// ui/QuickTaskCard.kt
val quickTasks = listOf(
    QuickTask("📋 Summarize notifications", "Read my recent notifications and summarize them."),
    QuickTask("🔋 Battery report", "Check battery level, temperature, and charging state."),
    QuickTask("💾 Storage analysis", "Analyze storage usage and suggest apps to clean up."),
    QuickTask("📱 Installed apps", "List all installed apps grouped by category."),
    QuickTask("🔵 Bluetooth state", "Check if Bluetooth is on and list paired devices.")
)

data class QuickTask(val label: String, val prompt: String)

// In your composable:
@Composable
fun QuickTaskRow(onSelect: (String) -> Unit) {
    LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        items(quickTasks) { task ->
            AssistChip(
                onClick = { onSelect(task.prompt) },
                label = { Text(task.label) }
            )
        }
    }
}
```

---

## Common Patterns

### Pattern: Read screen → act → verify

```kotlin
// Always read screen state before acting on unknown screens
suspend fun navigateToContact(contact: String): Boolean {
    // 1. Understand current state
    val screen = accessibilityService.getScreenInfo()
    
    // 2. If already in the right place, proceed
    if (screen.contains(contact)) return true
    
    // 3. Otherwise search
    accessibilityService.tap("search")
    delay(500)
    accessibilityService.inputText(contact)
    delay(1000)
    
    // 4. Verify
    val updated = accessibilityService.getScreenInfo()
    return updated.contains(contact)
}
```

### Pattern: Retry with backoff

```kotlin
suspend fun <T> retryWithBackoff(
    times: Int = 3,
    initialDelay: Long = 500,
    block: suspend () -> T
): T {
    var currentDelay = initialDelay
    repeat(times - 1) {
        try { return block() } catch (e: Exception) { /* continue */ }
        delay(currentDelay)
        currentDelay *= 2
    }
    return block() // last attempt, let exception propagate
}

// Usage
retryWithBackoff { accessibilityService.tap("Send") }
```

### Pattern: Wait for UI element

```kotlin
suspend fun waitForElement(
    target: String,
    timeoutMs: Long = 5000,
    pollMs: Long = 200
): Boolean {
    val deadline = System.currentTimeMillis() + timeoutMs
    while (System.currentTimeMillis() < deadline) {
        if (accessibilityService.getScreenInfo().contains(target)) return true
        delay(pollMs)
    }
    return false
}
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `Screen unavailable` from `getScreenInfo()` | Accessibility service not connected | Check Settings → Accessibility → PokeClaw is enabled |
| Tap does nothing | Element not in view or ID mismatch | Call `getScreenInfo()` first; scroll if needed |
| Model OOM crash | Not enough free RAM | Close background apps; need ≥8 GB device RAM |
| Model download
