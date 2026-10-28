---
name: aicore-sdk-java
description: >
  Generate working Java boilerplate for SAP GenAI Hub using the SAP AI SDK for Java
  (com.sap.ai.sdk). Covers chat completion, streaming, multi-turn conversations,
  prompt templates, content filtering, data masking, embeddings, RAG/grounding,
  prompt registry, and Spring Boot streaming.
  WHEN: user asks for Java or Kotlin code that calls a GenAI Hub model, wants a Java
  starter project, asks how to use com.sap.ai.sdk in their app, or asks how to
  integrate AI Core into a Spring Boot or plain Java application.
  DO NOT USE FOR: JavaScript/TypeScript code — use `aicore-sdk-js`.
compatibility: Requires Java 17+ and Maven or Gradle. Context7 MCP is optional (see Sources & Fallback).
---

## Sources & Fallback

Resolve answers in this priority order:

1. **Assets** (`assets/` directory) — check for a matching template first and serve it
   directly. Assets are always available offline and contain runnable, tested code.
2. **Context7 MCP** — if no asset matches, fetch live docs via Context7:
   `resolve-library-id: SAP/ai-sdk-java`, then `get-library-docs`.
   Context7 returns the most up-to-date API shapes straight from the repo.
   Silently fall back to step 3 if Context7 is not installed.
3. **`references/SDK_JAVA.md`** — offline reference when Context7 is unavailable.
   Use this rather than guessing.

**Do not fabricate class names, method signatures, or config shapes.** If none of the
three sources cover the question, say so and point the user to
https://sap.github.io/ai-sdk/docs/java/ directly.

---

## Rules

1. If no deployment exists, check the SAP AI Core console or contact your admin to list or create one before generating code.
2. Always include credential guidance in generated code comments; link to [Connecting to AI Core](https://sap.github.io/ai-sdk/docs/java/connecting-to-ai-core) for setup details.
3. Use `OrchestrationAiModel` constants (e.g. `OrchestrationAiModel.GPT_4O_MINI`) — never raw model name strings.
4. Always use `OrchestrationClient` as the primary client for chat, streaming, embeddings, grounding, and filtering. `OpenAiClient` (`openai` artifact) is only for direct OpenAI proxy use cases — do not recommend it for general chat.
5. Streaming has two distinct APIs — use each correctly:
   - **`OrchestrationClient.streamChatCompletion()` in a Spring Boot controller**: always use `ResponseBodyEmitter` + `ThreadContextExecutors.getExecutor().execute()` to forward deltas. Never use `SseEmitter`, `Thread.ofVirtual()`, or expose a raw `Flux` from the controller.
   - **Spring AI `ChatModel.stream()` (`OrchestrationChatModel` / `OpenAiChatModel`)**: this method is part of the Spring AI `ChatModel` interface and legitimately returns `Flux<ChatResponse>`. Composing the `Flux` directly (e.g. `.doOnNext(…).blockLast()`) is correct — do not replace it with `ResponseBodyEmitter`.
6. Gather these details before generating code — ask only for what the user hasn't provided:
   - **Use case**: chat / streaming / multi-turn / embeddings / grounding / filtering?
   - **Model**: check the SAP AI Core console or the [SAP GenAI Hub documentation](https://help.sap.com/docs/sap-ai-core) for available models
   - **Build tool**: Maven or Gradle?
   - **Framework**: plain Java / Spring Boot?
7. For SDK bugs or unexpected runtime behavior: acknowledge the issue, share only verified workarounds from the assets or reference docs, and direct the user to https://github.com/SAP/ai-sdk-java/issues. Do not speculate about SDK internals or diagnose bugs not covered by a source above.

---

## Asset Map

| Use case                               | Template                                  | Dependency                                 |
| -------------------------------------- | ----------------------------------------- | ------------------------------------------ |
| Chat via `OrchestrationClient`         | `assets/ChatOrchestration.java`           | `com.sap.ai.sdk:orchestration`             |
| Streaming via `OrchestrationClient`    | `assets/StreamingOrchestration.java`      | `com.sap.ai.sdk:orchestration`             |
| Multi-turn conversation                | `assets/MultiTurnOrchestration.java`      | `com.sap.ai.sdk:orchestration`             |
| Text embeddings                        | `assets/EmbeddingsOrchestration.java`     | `com.sap.ai.sdk:orchestration`             |
| RAG / vector store grounding           | `assets/GroundingOrchestration.java`      | `com.sap.ai.sdk:orchestration`             |
| Prompt Registry templates              | `assets/PromptRegistryOrchestration.java` | `com.sap.ai.sdk:orchestration`             |
| Spring AI + Orchestration              | `assets/SpringAiOrchestration.java`       | `com.sap.ai.sdk:orchestration`             |
| Spring AI + OpenAI client              | `assets/SpringAiOpenAi.java`              | `com.sap.ai.sdk:openai`                    |
| LLM batch processing                   | `assets/BatchOrchestration.java`          | `com.sap.ai.sdk:batch` + `openai` + `core` |
| Native OpenAI Responses API            | `assets/OpenAiNative.java`                | `com.sap.ai.sdk:openai`                    |
| RPT table completion (SAP RPT model)   | `assets/RptOrchestration.java`            | `com.sap.ai.sdk:sap-rpt`                   |
| Content filtering (Azure + LlamaGuard) | `assets/FilteringOrchestration.java`      | `com.sap.ai.sdk:orchestration`             |
| Data masking (DPI anonymization)       | `assets/MaskingOrchestration.java`        | `com.sap.ai.sdk:orchestration`             |

---

## Install Options

```xml
<!-- Maven — orchestration only (default resource group) -->
<dependency>
    <groupId>com.sap.ai.sdk</groupId>
    <artifactId>orchestration</artifactId>
    <version>1.22.0</version>
</dependency>

<!-- Add core if using AiCoreService (custom resource groups) -->
<dependency>
    <groupId>com.sap.ai.sdk</groupId>
    <artifactId>core</artifactId>
    <version>1.22.0</version>
</dependency>
```

```groovy
// Gradle
implementation 'com.sap.ai.sdk:orchestration:1.22.0'
// Add core if using AiCoreService (custom resource groups):
implementation 'com.sap.ai.sdk:core:1.22.0'
```

Check [Maven Central](https://central.sonatype.com/artifact/com.sap.ai.sdk/orchestration) for the latest version.

---

## Quick Start (OrchestrationClient)

```java
import com.sap.ai.sdk.orchestration.OrchestrationClient;
import com.sap.ai.sdk.orchestration.OrchestrationModuleConfig;
import com.sap.ai.sdk.orchestration.OrchestrationPrompt;
import com.sap.ai.sdk.orchestration.OrchestrationAiModel;

// Credentials auto-loaded from AICORE_SERVICE_KEY env var or VCAP_SERVICES
var client = new OrchestrationClient();

var config = new OrchestrationModuleConfig()
    .withLlmConfig(OrchestrationAiModel.GPT_4O_MINI);

var response = client.chatCompletion(
    new OrchestrationPrompt("What is SAP AI Core?"), config);

System.out.println(response.getContent());
```

---

## Credential Setup

Set the `AICORE_SERVICE_KEY` environment variable to the JSON service key from SAP AI Core:

```bash
export AICORE_SERVICE_KEY='{"clientid":"...","clientsecret":"...","url":"...","serviceurls":{"AI_API_URL":"..."}}'
```

Or run `aicore configure` (Python CLI) to store credentials in `~/.aicore/config.json`.
See: https://sap.github.io/ai-sdk/docs/java/connecting-to-ai-core

---

## Handoffs

- **Want JS/TS code instead?** → invoke `aicore-sdk-js`
- **SDK bug or unexpected behavior?** → https://github.com/SAP/ai-sdk-java/issues

---

## When to Load Reference Files

| Trigger                                                                                                                        | Action                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- |
| Use case matches an asset (chat, streaming, multi-turn, embeddings, grounding, prompt registry, Spring AI, filtering, masking) | Serve the matching asset from `assets/`                                                             |
| Use case not covered by an asset (reasoning, structured output, Spring Boot streaming)                                         | Use Context7 (`SAP/ai-sdk-java`) for API usage patterns if available, else `references/SDK_JAVA.md` |
| Any code generation                                                                                                            | Always verify class names and method signatures against a source above                              |
