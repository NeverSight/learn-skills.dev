---
name: anycable-coder
description: Use when implementing real-time features requiring reliability, especially LLM streaming. Applies AnyCable patterns for message delivery guarantees, presence tracking, and Action Cable migration.
allowed-tools: Read Write Edit Grep Glob Bash
---

# AnyCable Coder

## Why AnyCable Over Action Cable

Action Cable provides "at-most once" delivery—messages can be lost on reconnection. For LLM streaming where every chunk matters, this is insufficient.

**AnyCable provides:**
- **At-least once delivery** - Messages are guaranteed to arrive
- **Message ordering** - Chunks arrive in correct sequence
- **Automatic reconnection** - With history recovery
- **Action Cable Extended Protocol** - Enhanced reliability on top of WebSockets

## Installation

```bash
bundle add anycable-rails
bin/rails g anycable:setup
```

```bash
# Client (replace @rails/actioncable)
npm install @anycable/web
```

## Server-Side Channels

### Basic LLM Streaming Channel

```ruby
class LlmStreamChannel < ApplicationCable::Channel
  def subscribed
    stream_for current_user
  end

  def generate(data)
    prompt = data["prompt"]

    llm_client.stream(prompt) do |chunk|
      LlmStreamChannel.broadcast_to(
        current_user,
        { type: "chunk", content: chunk }
      )
    end

    LlmStreamChannel.broadcast_to(
      current_user,
      { type: "complete" }
    )
  end
end
```

### With Presence Tracking

```ruby
class ChatChannel < ApplicationCable::Channel
  include AnyCable::Rails::Channel::Presence

  def subscribed
    stream_from "chat_#{params[:room_id]}"
    presence.join(current_user.id, name: current_user.name)
  end

  def unsubscribed
    presence.leave
  end
end
```

## Client-Side Implementation

### Migration from Action Cable

```javascript
// Before (Action Cable)
import { createConsumer } from "@rails/actioncable"

// After (AnyCable) - same API!
import { createConsumer } from "@anycable/web"

export default createConsumer()
```

### Modern AnyCable Client

```javascript
import { createCable } from "@anycable/web"

const cable = createCable()

// Class-based channel
import { Channel } from "@anycable/web"

class LlmStreamChannel extends Channel {
  static identifier = "LlmStreamChannel"

  async generate(prompt) {
    return this.perform("generate", { prompt })
  }
}

// Subscribe and handle chunks
const channel = new LlmStreamChannel()
cable.subscribe(channel)

await channel.ensureSubscribed()

channel.on("message", (msg) => {
  if (msg.type === "chunk") {
    appendToResponse(msg.content)
  } else if (msg.type === "complete") {
    finishResponse()
  }
})

channel.generate("Explain WebSockets")
```

### Direct Streams (Signed)

```javascript
// Subscribe directly to a stream without channel class
const cable = createCable()
const stream = cable.streamFrom("llm_response/user_123")

stream.on("message", (msg) => console.log(msg))
```

### Presence API

```javascript
const chatChannel = cable.subscribeTo("ChatChannel", { roomId: "42" })

// Join presence
chatChannel.presence.join(user.id, { name: user.name })

// Listen for presence events
chatChannel.presence.on("presence", (event) => {
  if (event.type === "join") {
    console.log("User joined:", event.id, event.info)
  } else if (event.type === "leave") {
    console.log("User left:", event.id)
  }
})

// Get current presence
const users = await chatChannel.presence.info()

// Leave presence
chatChannel.presence.leave()
```

## LLM Streaming Pattern

### Complete Implementation

```ruby
# app/channels/assistant_channel.rb
class AssistantChannel < ApplicationCable::Channel
  def subscribed
    stream_for current_user
  end

  def ask(data)
    conversation_id = data["conversation_id"]
    message = data["message"]

    # Broadcast start
    broadcast_event("start", conversation_id:)

    # Stream LLM response
    response = ""
    llm.chat(message) do |chunk|
      response += chunk
      broadcast_event("chunk", conversation_id:, content: chunk)
    end

    # Save and broadcast completion
    Message.create!(conversation_id:, role: "assistant", content: response)
    broadcast_event("complete", conversation_id:)
  rescue => e
    broadcast_event("error", conversation_id:, message: e.message)
  end

  private

  def broadcast_event(type, **payload)
    AssistantChannel.broadcast_to(current_user, { type:, **payload })
  end

  def llm
    @llm ||= OpenAI::Client.new
  end
end
```

```javascript
// app/javascript/channels/assistant_channel.js
import { Channel } from "@anycable/web"

export default class AssistantChannel extends Channel {
  static identifier = "AssistantChannel"

  constructor() {
    super()
    this.responseBuffer = ""
  }

  async ask(conversationId, message) {
    this.responseBuffer = ""
    return this.perform("ask", { conversation_id: conversationId, message })
  }

  // Override to handle message types
  receive(message) {
    switch (message.type) {
      case "start":
        this.onStart?.(message.conversation_id)
        break
      case "chunk":
        this.responseBuffer += message.content
        this.onChunk?.(message.content, this.responseBuffer)
        break
      case "complete":
        this.onComplete?.(this.responseBuffer, message.conversation_id)
        break
      case "error":
        this.onError?.(message.message)
        break
    }
  }
}
```

## Configuration

### AnyCable Server

```yaml
# config/anycable.yml
production:
  broadcast_adapter: nats
  redis_url: <%= ENV.fetch("REDIS_URL") %>

  # Enable reliable streams
  streams_history_size: 100
  streams_history_ttl: 300
```

### Cable URL

```erb
<!-- app/views/layouts/application.html.erb -->
<%= action_cable_meta_tag %>
```

```javascript
// Auto-detects from meta tag, or specify explicitly
import { createCable } from "@anycable/web"
createCable("wss://cable.example.com/cable")
```

## Deployment

### Procfile

```yaml
web: bundle exec puma -C config/puma.rb
anycable: bundle exec anycable
ws: anycable-go
```

### Docker Compose

```yaml
services:
  web:
    command: bundle exec puma
  anycable:
    command: bundle exec anycable
  ws:
    image: anycable/anycable-go:1.6
    environment:
      ANYCABLE_RPC_HOST: anycable:50051
      ANYCABLE_REDIS_URL: redis://redis:6379
```

## Action Cable vs AnyCable

| Feature | Action Cable | AnyCable |
|---------|--------------|----------|
| Delivery guarantee | At-most once | At-least once |
| Message ordering | Not guaranteed | Guaranteed |
| History on reconnect | No | Yes (configurable) |
| Presence tracking | Manual | Built-in |
| Performance | Ruby threads | Go server |
| LLM streaming | Unreliable | Reliable |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Action Cable for LLM streaming | Lost chunks on reconnect | Use AnyCable |
| Ignoring message ordering | Garbled responses | AnyCable handles automatically |
| Manual reconnection logic | Complex, error-prone | Use AnyCable client |
| No presence tracking | Unknown user state | Use built-in presence API |

## Output Format

When implementing real-time features with AnyCable:

1. **Channel** - Server-side Ruby channel with broadcasting
2. **Client** - JavaScript subscription with message handling
3. **Configuration** - anycable.yml and deployment setup
4. **Error Handling** - Graceful degradation patterns
