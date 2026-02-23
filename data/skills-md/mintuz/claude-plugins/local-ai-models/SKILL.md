---
name: local-ai-models
description: Comprehensive guide for implementing on-device AI models on iOS using Foundation Models and MLX Swift frameworks. Use WHEN building iOS apps with (1) Local LLM inference, (2) Vision Language Models (VLMs), (3) Text embeddings, (4) Image generation, (5) Tool/function calling, (6) Multi-turn conversations, (7) Custom model integration, or (8) Structured generation.
---

# iOS On-Device AI Models

Production-ready guide for implementing on-device AI models in iOS apps using Apple's Foundation Models framework and MLX Swift.

## When to Use This Skill

- Implementing local LLM inference in iOS apps
- Building chat interfaces with Foundation Models
- Integrating Vision Language Models (VLMs)
- Adding text embeddings or image generation
- Implementing tool/function calling with LLMs
- Managing multi-turn conversations
- Optimizing memory usage for on-device models
- Supporting internationalization in AI features

## Core Principles

1. **Availability First** - Always check model availability before initialization
2. **Stream Responses** - Provide progressive UI updates for better UX
3. **Session Persistence** - Reuse LanguageModelSession for multi-turn conversations (Foundation Models)
4. **Memory Awareness** - Use quantized models and monitor memory usage
5. **Async Everything** - Load models asynchronously, never block the main thread
6. **Locale Support** - Use supportsLocale(_:) and locale instructions for Foundation Models

## Quick Reference

### Framework Comparison

| Topic                              | Guide                                                       |
| ---------------------------------- | ----------------------------------------------------------- |
| Framework comparison and selection | [framework-selection.md](references/framework-selection.md) |

### Foundation Models (Apple's Framework)

| Topic                           | Guide                                                                               |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| Setup and configuration         | [foundation-models/setup.md](references/foundation-models/setup.md)                 |
| Chat patterns and conversations | [foundation-models/chat-patterns.md](references/foundation-models/chat-patterns.md) |

### MLX Swift (Advanced Features)

| Topic                                    | Guide                                                                       |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| Setup and configuration                  | [mlx-swift/setup.md](references/mlx-swift/setup.md)                         |
| Chat patterns with custom models         | [mlx-swift/chat-patterns.md](references/mlx-swift/chat-patterns.md)         |
| Vision Language Models (VLMs)            | [mlx-swift/vision-patterns.md](references/mlx-swift/vision-patterns.md)     |
| Tool calling, embeddings, structured gen | [mlx-swift/advanced-patterns.md](references/mlx-swift/advanced-patterns.md) |
| Model quantization with MLX-LM           | [mlx-swift/quantization.md](references/mlx-swift/quantization.md)           |

### Shared (Both Frameworks)

| Topic                           | Guide                                                           |
| ------------------------------- | --------------------------------------------------------------- |
| Best practices and optimization | [shared/best-practices.md](references/shared/best-practices.md) |
| Error handling and recovery     | [shared/error-handling.md](references/shared/error-handling.md) |
| Testing strategies              | [shared/testing.md](references/shared/testing.md)               |

## Quick Decision Trees

### Which framework should I use?

```
Do you need advanced features like:
- Vision Language Models (VLMs)
- Image generation
- Custom models beyond the system model
├── Yes → MLX Swift (references/mlx-swift/)
└── No → Is this a standard chat interface?
    ├── Yes → Foundation Models (simpler, recommended)
    └── No → Check framework-selection.md for guidance
```

### Where should I start?

```
New to on-device AI?
└── Start with Foundation Models:
    1. Read framework-selection.md
    2. Follow foundation-models/setup.md
    3. Implement foundation-models/chat-patterns.md

Need advanced features?
└── Use MLX Swift:
    1. Read framework-selection.md
    2. Follow mlx-swift/setup.md
    3. Choose pattern:
       - Chat: mlx-swift/chat-patterns.md
       - Vision: mlx-swift/vision-patterns.md
       - Advanced: mlx-swift/advanced-patterns.md
```

### Where should my model loading code live?

```
Is this model shared across features?
├── Yes → Create @Observable service in app/services/
└── No → Is it feature-specific?
    ├── Yes → Create @Observable class in feature/
    └── No → Load inline with @State (simple cases only)
```

### How should I handle conversations?

```
Foundation Models:
└── Reuse LanguageModelSession for context
    (references/foundation-models/chat-patterns.md #multi-turn)

MLX Swift:
└── Implement custom context management
    (references/mlx-swift/chat-patterns.md)
```

### What generation parameters should I use?

```
What's the use case?

Factual answers (summaries, facts)
└── temperature: 0.1-0.3

Balanced (chat, Q&A)
└── temperature: 0.6-0.8

Creative (storytelling, ideas)
└── temperature: 0.9-1.2

See references/shared/best-practices.md for details
```

## Resources

- [MLX Swift Examples](https://github.com/ml-explore/mlx-swift-examples)
- [Foundation Models Docs](https://developer.apple.com/documentation/foundationmodels)
- [Hugging Face Model Hub](https://huggingface.co/models)
- [MLX-LM Quantization](https://github.com/ml-explore/mlx-examples/tree/main/llms)
- [MLX Community Models](https://huggingface.co/mlx-community)
