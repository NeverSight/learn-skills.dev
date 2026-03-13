---
name: opentelemetry
description: OpenTelemetry observability - use for distributed tracing, metrics, instrumentation, Sentry integration, and monitoring
---

# OpenTelemetry Patterns

## Spring Boot Configuration

```kotlin
// build.gradle.kts
dependencies {
    implementation(platform("io.opentelemetry.instrumentation:opentelemetry-instrumentation-bom:2.15.0"))
    implementation("io.opentelemetry.instrumentation:opentelemetry-spring-boot-starter")
    implementation("io.micrometer:micrometer-tracing-bridge-otel")
    implementation("io.opentelemetry:opentelemetry-exporter-zipkin")

    // Sentry integration
    implementation("io.sentry:sentry-spring-boot-starter-jakarta:8.26.0")
    implementation("io.sentry:sentry-logback:8.26.0")
}
```

```yaml
# application.yaml
spring:
  application:
    name: your-project

management:
  tracing:
    sampling:
      probability: 1.0  # 100% in dev, lower in prod
  otlp:
    tracing:
      endpoint: http://localhost:4318/v1/traces

otel:
  exporter:
    otlp:
      endpoint: http://otel-collector:4317
  service:
    name: your-project
  resource:
    attributes:
      deployment.environment: ${ENVIRONMENT:dev}
      service.version: ${APP_VERSION:unknown}

sentry:
  dsn: ${SENTRY_DSN:}
  environment: ${ENVIRONMENT:dev}
  traces-sample-rate: 1.0
```

## Custom Span Creation

```kotlin
import io.opentelemetry.api.trace.Span
import io.opentelemetry.api.trace.Tracer
import io.opentelemetry.context.Context
import org.springframework.stereotype.Component

@Component
class TracingService(
    private val tracer: Tracer
) {

    fun <T> withSpan(
        spanName: String,
        attributes: Map<String, String> = emptyMap(),
        block: () -> T
    ): T {
        val span = tracer.spanBuilder(spanName)
            .setParent(Context.current())
            .startSpan()

        attributes.forEach { (key, value) ->
            span.setAttribute(key, value)
        }

        return try {
            span.makeCurrent().use {
                block()
            }
        } catch (e: Exception) {
            span.recordException(e)
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.message ?: "Error")
            throw e
        } finally {
            span.end()
        }
    }
}

// Usage for Telegram bot
@Service
class CommandService(
    private val tracingService: TracingService,
    private val userRepository: UserRepository
) {

    suspend fun handleCommand(message: CommonMessage<*>, command: String) {
        tracingService.withSpan(
            "CommandService.handleCommand",
            mapOf(
                "telegram.command" to command,
                "telegram.chat_id" to message.chat.id.chatId.toString(),
                "telegram.user_id" to (message.from?.id?.chatId?.toString() ?: "unknown")
            )
        ) {
            Span.current().addEvent("Processing command: $command")

            when (command) {
                "start" -> handleStart(message)
                "help" -> handleHelp(message)
                else -> handleUnknown(message)
            }
        }
    }
}
```

## Annotation-Based Tracing

```kotlin
import io.micrometer.tracing.annotation.NewSpan
import io.micrometer.tracing.annotation.SpanTag

@Service
class MessageService {

    @NewSpan("bot.sendMessage")
    suspend fun sendMessage(
        @SpanTag("telegram.chat_id") chatId: Long,
        @SpanTag("message.type") type: String
    ): Message {
        // Automatically traced
        return bot.sendMessage(ChatId(chatId), text)
    }

    @NewSpan("bot.handleCallback")
    suspend fun handleCallback(
        @SpanTag("callback.data") data: String,
        @SpanTag("telegram.user_id") userId: Long
    ) {
        // Process callback query
    }
}
```

## Baggage Propagation

```kotlin
import io.opentelemetry.api.baggage.Baggage

// Set baggage (propagates across services)
fun setUserContext(userId: String, tenantId: String) {
    Baggage.current()
        .toBuilder()
        .put("user.id", userId)
        .put("tenant.id", tenantId)
        .build()
        .makeCurrent()
}

// Read baggage
fun getCurrentUserId(): String? {
    return Baggage.current().getEntryValue("user.id")
}
```

## Metrics

```kotlin
// Kotlin/Spring Boot
import io.micrometer.core.instrument.MeterRegistry
import io.micrometer.core.instrument.Timer

@Component
class BotMetricsService(
    private val registry: MeterRegistry
) {

    private val commandCounter = registry.counter(
        "your-project.bot.commands",
        "command", "unknown"
    )

    private val messageProcessingTimer = Timer.builder("your-project.bot.message.duration")
        .description("Time to process a message")
        .register(registry)

    fun recordCommand(command: String) {
        registry.counter("your-project.bot.commands", "command", command).increment()
    }

    fun recordCallback(action: String) {
        registry.counter("your-project.bot.callbacks", "action", action).increment()
    }

    fun <T> timeMessageProcessing(block: () -> T): T {
        return messageProcessingTimer.recordCallable(block)!!
    }
}
```

## Sentry Integration

```kotlin
// Error reporting with Sentry for Telegram bot
import io.sentry.Sentry
import io.sentry.SentryLevel

class BotErrorHandler {

    fun handleBotException(e: Exception, chatId: Long?, command: String?) {
        Sentry.withScope { scope ->
            scope.setTag("error.type", e.javaClass.simpleName)
            scope.setTag("bot.command", command ?: "unknown")
            scope.setLevel(SentryLevel.ERROR)
            scope.setContexts("telegram", mapOf(
                "chat_id" to (chatId?.toString() ?: "unknown"),
                "command" to (command ?: "none")
            ))
            Sentry.captureException(e)
        }
    }
}

// Usage in bot handler
bot.buildBehaviourWithLongPolling(
    defaultExceptionsHandler = { e ->
        errorHandler.handleBotException(e, null, null)
        logger.error("Bot error", e)
    }
) {
    // handlers
}
```

## OpenTelemetry Collector Config

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  zipkin:
    endpoint: http://zipkin:9411/api/v2/spans
  prometheus:
    endpoint: 0.0.0.0:8889
  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [zipkin, logging]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```
