---
name: astrbot-plugin-dev
description: Guide for developing AstrBot plugins. Supports creating commands, filters, hooks, handling messages, integrating with LLMs, and building agents. Use when requested to create or update an AstrBot plugin.
---

# AstrBot Plugin Development

This skill provides the procedural knowledge to develop AstrBot plugins.

## Quick Start: Basic Command Plugin

Create a `main.py` in your plugin directory:

```python
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("helloworld", "YourName", "A simple Hello World plugin", "1.0.0", "https://github.com/user/repo")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        '''A hello world command'''
        user_name = event.get_sender_name()
        message_str = event.message_str
        logger.info("helloworld triggered!")
        yield event.plain_result(f"Hello, {user_name}!")

    async def terminate(self):
        '''Called when the plugin is unloaded/disabled.'''
```

## Core Workflows

### 1. Project Setup and Metadata
A complete plugin requires `metadata.yaml` for identification, `requirements.txt` for dependencies, and optionally `logo.png`, `_conf_schema.json`, and a `README.md`.

- Plugin names should start with `astrbot_plugin_`, be lowercase, have no spaces, and be short.
- See [references/project-structure.md](references/project-structure.md) for mandatory files, dev environment setup, and publishing.

### 2. Registering Commands and Filters
Commands are registered using `@filter.command(name)`. AstrBot auto-parses command parameters by type hints. You can also use command groups, command aliases, and filter by event type, platform, or user permission.

- See [references/core-api.md](references/core-api.md) for full list of filters, hooks, the platform compatibility matrix, and event propagation control.

### 3. Handling Messages and Responses
AstrBot uses a "Message Chain" system. You can respond with plain text, images, or a mix of components. Proactive (bot-initiated) messages are supported via `unified_msg_origin` and `MessageChain`.

- See [references/message-components.md](references/message-components.md) for how to build and send messages.

### 4. Advanced Integrations
- **Configuration**: Use `_conf_schema.json` for user settings (supports `string`, `int`, `bool`, `object`, `list`, `dict`, `file`, `template_list`, and special selectors).
- **LLM Tools**: Register tools via `@filter.llm_tool` decorator or Pydantic `FunctionTool` dataclass.
- **LLM Direct Calls**: Use `self.context.llm_generate()` to call LLMs directly (>= v4.5.7).
- **Agent / Multi-Agent**: Use `self.context.tool_loop_agent()` to run tool-loop agents or compose multi-agent systems.
- **Stateful Interaction**: Use `session_waiter` for multi-step prompts with custom session filters.
- **T2I**: Render text or HTML/Jinja2 templates to images.
- **Conversation & Persona Managers**: Access LLM conversation history and persona settings.

See [references/advanced-features.md](references/advanced-features.md) for examples.

## Elegant Design Patterns
Follow these patterns for robust, user-friendly plugins:
- Use unified logging via `from astrbot.api import logger`.
- Handle errors gracefully to avoid bot crashes.
- Use KV storage (`put_kv_data`/`get_kv_data`) or the `plugin_data` directory for persistence.
- Ensure all IO operations are non-blocking (async).
- Access platform instances, loaded plugins, and protocol-level APIs when needed.

See [references/patterns.md](references/patterns.md) for detailed code patterns.
