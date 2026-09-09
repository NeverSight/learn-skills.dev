---
name: litestar-ai-serving
description: "Auto-activate for Google ADK, LlmAgent, Runner, SQLSpecSessionService, Vertex AI, SSE agent chats, tool calls, or Litestar model workflows. Not for offline ML training."
---

# Litestar AI Serving

Use this skill for HTTP-facing AI agent endpoints, Google ADK integration, session-backed conversations, and Litestar service boundaries around model workflows.

## Code Style Rules

- Keep agent orchestration behind service functions or providers.
- Use typed request and response DTOs at the HTTP boundary.
- Store multi-turn state through the project's database stack.
- Stream only when the client contract needs incremental output.

## Quick Reference

- AI serving patterns: [ai-serving.md](references/ai-serving.md)
- Pair with [sqlspec](../sqlspec/SKILL.md) for ADK session stores.
- Pair with [litestar-realtime](../litestar-realtime/SKILL.md) for streaming or event fan-out.

<workflow>

## Workflow

1. Define the HTTP contract before agent internals.
2. Wire agent runners through DI.
3. Persist session state through the chosen data stack.
4. Test deterministic failure, timeout, and cancellation paths.

</workflow>

<guardrails>

## Guardrails

- Do not expose raw agent internals as the API contract.
- Do not block request workers with unbounded model calls.
- Do not store prompts, tool outputs, or memory without a retention decision.
- Do not skip authorization on agent endpoints.

</guardrails>

<validation>

## Validation Checkpoint

- [ ] Request and response DTOs are explicit.
- [ ] Session persistence is wired.
- [ ] Timeouts and model failures are handled.
- [ ] Auth policy matches the sensitivity of tools and data.

</validation>

<example>

## Example

```python
@get("/chat/{session_id:str}")
async def chat(session_id: str, runner: Runner, body: ChatRequest) -> ChatResponse:
    result = await runner.run_async(session_id=session_id, new_message=body.message)
    return ChatResponse(message=result.final_response)
```

</example>

## References Index

- [ai-serving.md](references/ai-serving.md)

## Official References

- <https://docs.litestar.dev/> - Litestar documentation
- <https://docs.litestar.dev/latest/reference/> - Litestar API reference

## Shared Styleguide Baseline

- [General](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
