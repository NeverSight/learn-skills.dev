---
name: instrument-llm-analytics
description: >-
  Add PostHog AI Observability to trace AI model usage. Use after implementing
  LLM features or reviewing PRs to ensure all generations are captured with
  token counts, latency, and costs. Also handles initial PostHog SDK setup if
  not yet installed.
metadata:
  author: PostHog
---

# Add PostHog AI Observability

Use this skill to add PostHog AI Observability that traces AI model usage in new or changed code. Use it after implementing LLM features or reviewing PRs to ensure all generations are captured with token counts, latency, and costs. If PostHog is not yet installed, this skill also covers initial SDK setup. Supports any provider or framework.

Supported providers: OpenAI, Azure OpenAI, Anthropic, Google, Cohere, Mistral, Perplexity, DeepSeek, Groq, Together AI, Fireworks AI, xAI, Cerebras, Hugging Face, Ollama, OpenRouter.

Supported frameworks: LangChain, LlamaIndex, CrewAI, AutoGen, DSPy, LangGraph, Pydantic AI, Vercel AI, LiteLLM, Instructor, Semantic Kernel, Mirascope, Mastra, SmolAgents, OpenAI Agents.

Proxy/gateway: Portkey, Helicone.

## Instructions

Before you edit anything, read `references/COMMANDMENTS.md`. It lists the rules every PostHog install follows: how to install the SDK, where to create the client, how to identify users, Content Security Policy and multi-platform apps, plus the rules for this framework.

Follow these steps IN ORDER:

STEP 1: Analyze the codebase and detect the LLM stack.
  - Look for LLM provider SDKs (openai, anthropic, google-generativeai, etc.) and AI frameworks (langchain, llamaindex, crewai, etc.) in dependency files and imports.
  - Look for lockfiles to determine the package manager.
  - Check for existing PostHog or observability setup. If PostHog is already installed and LLM tracing is configured, skip to STEP 4 to add tracing for any new LLM calls.

STEP 2: Research instrumentation. (Skip if PostHog LLM tracing is already set up.)
  2.1. Find the reference file below that matches the detected provider or framework — it is the source of truth for callback setup, middleware configuration, and event capture. Read it now.
  2.2. If no reference matches, use manual-capture.md as a fallback — it covers the generic event capture approach that works with any provider.

STEP 3: Install the PostHog SDK. (Skip if PostHog is already set up.)
  - Add the PostHog SDK and any required callback/integration packages.
  - Do not manually edit dependency files — use the package manager's install command.
  - If the project keeps more than one lockfile for the same manifest, such as a second Gemfile lock for another bundle, update each one.

STEP 4: Add LLM tracing.
  - Instrument LLM calls to capture input tokens, output tokens, model name, latency, and costs for every generation.
  - Follow the provider-specific reference for the exact callback/middleware setup.
  - Do not alter the fundamental architecture of existing files. Make additions minimal and targeted.
  - You must read a file immediately before attempting to write it.

STEP 5: Link to users.
  - Associate LLM generations with identified users via distinct IDs when possible.

STEP 6: Set up environment variables.
  - Check if the project already has PostHog environment variables configured (e.g. in `.env`, `.env.local`, or framework-specific env files). If valid values already exist, skip this step.
  - If the PostHog project token is missing, use the project token that the tool or CLI which started this setup already gave you (for example in its output or instructions).
  - If it gave you none, use the PostHog MCP server's `projects-get` tool to retrieve the project's `api_token`. If multiple projects are returned, ask the user which project to use. If the MCP server is not connected or not authenticated, ask the user for their PostHog project token instead.
  - For the PostHog host URL: use the host that the tool or CLI which started this setup already gave you. If it gave you none, check the `projects-get` MCP response for a `region` field — `US` maps to `https://us.i.posthog.com`, `EU` maps to `https://eu.i.posthog.com`. If you still have no host from the calling tool, the MCP response, or existing project configuration, ask the user: "Are you on PostHog US Cloud or EU Cloud?" Do not assume US Cloud.
  - Write these values to the appropriate env file using the framework's naming convention.
  - Reference these environment variables in code instead of hardcoding them.
  - List the key names in `.env.example`, or the env template the project already uses, with placeholder values, so the next developer knows what to set. Create `.env.example` if the project has none. Never put real values in it.
  - Read the keys as optional: a missing key must never break the build or boot. Follow the missing-configuration rule in `references/COMMANDMENTS.md`.

## Reference files

- `references/openai.md` - Openai observability installation
- `references/azure-openai.md` - Azure openai observability installation
- `references/README.md` - PostHog.ai for .net
- `references/anthropic.md` - Anthropic ai observability installation
- `references/google.md` - Google ai observability installation
- `references/cohere.md` - Cohere ai observability installation
- `references/mistral.md` - Mistral ai observability installation
- `references/perplexity.md` - Perplexity ai observability installation
- `references/deepseek.md` - Deepseek ai observability installation
- `references/groq.md` - Groq ai observability installation
- `references/together-ai.md` - Together ai observability installation
- `references/fireworks-ai.md` - Fireworks ai observability installation
- `references/xai.md` - Xai observability installation
- `references/cerebras.md` - Cerebras ai observability installation
- `references/hugging-face.md` - Hugging face ai observability installation
- `references/ollama.md` - Ollama ai observability installation
- `references/openrouter.md` - Openrouter ai observability installation
- `references/langchain.md` - Langchain ai observability installation
- `references/llamaindex.md` - Llamaindex ai observability installation
- `references/crewai.md` - Crewai observability installation
- `references/autogen.md` - Autogen ai observability installation
- `references/dspy.md` - Dspy ai observability installation
- `references/langgraph.md` - Langgraph ai observability installation
- `references/pydantic-ai.md` - Pydantic ai observability installation
- `references/vercel-ai.md` - Vercel ai SDK observability installation
- `references/litellm.md` - Litellm ai observability installation
- `references/instructor.md` - Instructor ai observability installation
- `references/semantic-kernel.md` - Semantic kernel ai observability installation
- `references/mirascope.md` - Mirascope ai observability installation
- `references/mastra.md` - Mastra ai observability installation
- `references/smolagents.md` - Smolagents ai observability installation
- `references/openai-agents.md` - Openai agents SDK observability installation
- `references/portkey.md` - Portkey ai observability installation
- `references/helicone.md` - Helicone ai observability installation
- `references/manual-capture.md` - Manual capture ai observability installation
- `references/basics.md` - Ai observability basics
- `references/traces.md` - Traces
- `references/calculating-costs.md` - Calculating llm costs
- `references/COMMANDMENTS.md` - Framework-specific rules the integration must follow

Each provider reference contains installation instructions, SDK setup, and code examples specific to that provider or framework. Find the reference that matches the user's stack.

If the user's provider isn't listed, use `manual-capture.md` as a fallback — it covers the generic event capture approach that works with any provider.

## Key principles

- **Environment variables**: Always use environment variables for PostHog and LLM provider keys. Never hardcode them.
- **Minimal changes**: Add LLM analytics alongside existing LLM calls. Don't replace or restructure existing code.
- **Trace all generations**: Capture input tokens, output tokens, model name, latency, and costs for every LLM call.
- **Link to users**: Associate LLM generations with identified users via distinct IDs when possible.
- **One provider at a time**: Only instrument the provider(s) the user is actually using. Don't add instrumentation for providers not present in the codebase.