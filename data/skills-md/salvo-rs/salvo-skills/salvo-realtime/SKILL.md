---
name: salvo-realtime
description: Implement real-time features using WebSocket and Server-Sent Events (SSE). Use for chat applications, live updates, notifications, and bidirectional communication.
---

# Salvo Real-time Communication

This skill provides an overview of real-time communication options in Salvo. For detailed implementations, see the dedicated skills:

- **salvo-websocket**: Full-duplex bidirectional communication
- **salvo-sse**: Server-to-client event streaming

## Choosing Between WebSocket and SSE

| Feature | WebSocket | SSE |
|---------|-----------|-----|
| Direction | Bidirectional | Server → Client only |
| Protocol | Custom protocol | HTTP |
| Reconnection | Manual | Automatic |
| Binary data | Yes | No (text only) |
| Browser support | All modern | All modern |
| Firewall friendly | May have issues | Yes (standard HTTP) |
| Complexity | Higher | Lower |

### When to Use WebSocket

- Chat applications
- Online gaming
- Collaborative editing
- Trading platforms
- Any bidirectional real-time data

### When to Use SSE

- Live notifications
- News feeds
- Stock tickers
- Progress updates
- Server monitoring dashboards

## Quick WebSocket Example

```rust
use salvo::prelude::*;
use salvo::websocket::WebSocketUpgrade;

#[handler]
async fn ws_handler(req: &mut Request, res: &mut Response) -> Result<(), StatusError> {
    WebSocketUpgrade::new()
        .upgrade(req, res, |mut ws| async move {
            while let Some(msg) = ws.recv().await {
                let msg = match msg {
                    Ok(msg) => msg,
                    Err(_) => return,
                };
                if ws.send(msg).await.is_err() {
                    return;
                }
            }
        })
        .await
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(Router::with_path("ws").goal(ws_handler));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Quick SSE Example

```rust
use std::convert::Infallible;
use std::time::Duration;
use futures_util::StreamExt;
use salvo::prelude::*;
use salvo::sse::{self, SseEvent};
use tokio::time::interval;
use tokio_stream::wrappers::IntervalStream;

#[handler]
async fn sse_handler(res: &mut Response) {
    let event_stream = {
        let mut counter: u64 = 0;
        let interval = interval(Duration::from_secs(1));
        let stream = IntervalStream::new(interval);

        stream.map(move |_| {
            counter += 1;
            Ok::<_, Infallible>(SseEvent::default().text(counter.to_string()))
        })
    };

    sse::stream(res, event_stream);
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .push(Router::with_path("events").get(sse_handler));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Real-time Architecture Patterns

### Broadcasting to Multiple Clients

```rust
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::{RwLock, mpsc};
use salvo::websocket::Message;

type Users = Arc<RwLock<HashMap<usize, mpsc::UnboundedSender<Message>>>>;

async fn broadcast(users: &Users, sender_id: usize, message: &str) {
    let formatted = format!("User {}: {}", sender_id, message);
    let users = users.read().await;

    for (&uid, tx) in users.iter() {
        if uid != sender_id {
            let _ = tx.send(Message::text(formatted.clone()));
        }
    }
}
```

### Room-Based Messaging

```rust
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

type Rooms = Arc<RwLock<HashMap<String, Vec<UserId>>>>;

async fn join_room(rooms: &Rooms, room: &str, user_id: UserId) {
    rooms.write().await
        .entry(room.to_string())
        .or_default()
        .push(user_id);
}

async fn leave_room(rooms: &Rooms, room: &str, user_id: UserId) {
    if let Some(users) = rooms.write().await.get_mut(room) {
        users.retain(|&id| id != user_id);
    }
}
```

### Pub/Sub with Broadcast Channels

```rust
use tokio::sync::broadcast;

#[derive(Clone)]
struct PubSub {
    sender: broadcast::Sender<String>,
}

impl PubSub {
    fn new(capacity: usize) -> Self {
        let (sender, _) = broadcast::channel(capacity);
        Self { sender }
    }

    fn publish(&self, message: String) {
        let _ = self.sender.send(message);
    }

    fn subscribe(&self) -> broadcast::Receiver<String> {
        self.sender.subscribe()
    }
}
```

## Client-Side Examples

### WebSocket Client (JavaScript)

```javascript
const ws = new WebSocket('ws://localhost:8080/ws');

ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Received:', e.data);
ws.onclose = () => console.log('Disconnected');
ws.onerror = (e) => console.error('Error:', e);

// Send message
ws.send('Hello, Server!');

// Close connection
ws.close();
```

### SSE Client (JavaScript)

```javascript
const source = new EventSource('http://localhost:8080/events');

source.onopen = () => console.log('Connected');
source.onmessage = (e) => console.log('Message:', e.data);
source.onerror = (e) => console.error('Error:', e);

// Named events
source.addEventListener('notification', (e) => {
    console.log('Notification:', e.data);
});

// Close connection
source.close();
```

## Combining WebSocket and SSE

Some applications benefit from using both:

```rust
let router = Router::new()
    // WebSocket for bidirectional chat
    .push(Router::with_path("chat").goal(ws_chat_handler))
    // SSE for notifications (one-way)
    .push(Router::with_path("notifications").get(sse_notifications))
    // SSE for live data feeds
    .push(Router::with_path("feed").get(sse_feed));
```

## Connection Management

### Track Active Connections

```rust
use std::sync::atomic::{AtomicUsize, Ordering};

static ACTIVE_CONNECTIONS: AtomicUsize = AtomicUsize::new(0);

fn on_connect() {
    let count = ACTIVE_CONNECTIONS.fetch_add(1, Ordering::Relaxed) + 1;
    tracing::info!("Connection opened. Active: {}", count);
}

fn on_disconnect() {
    let count = ACTIVE_CONNECTIONS.fetch_sub(1, Ordering::Relaxed) - 1;
    tracing::info!("Connection closed. Active: {}", count);
}
```

### Heartbeat / Keep-Alive

```rust
use std::time::Duration;
use tokio::time::interval;

async fn heartbeat_task(tx: Sender<Message>) {
    let mut ticker = interval(Duration::from_secs(30));
    loop {
        ticker.tick().await;
        if tx.send(Message::ping(vec![])).await.is_err() {
            break;
        }
    }
}
```

## Best Practices

### WebSocket

1. **Handle disconnections gracefully**: Clean up user state
2. **Implement ping/pong**: Detect dead connections
3. **Use message queues**: Buffer messages for slow clients
4. **Authenticate before upgrade**: Verify tokens in query params or headers
5. **Limit message size**: Prevent memory exhaustion
6. **Use binary for efficiency**: When sending structured data

### SSE

1. **Use keep-alive**: Prevent connection timeout
2. **Include event IDs**: Enable reconnection from last event
3. **Set retry interval**: Guide client reconnection behavior
4. **Use named events**: Organize different message types
5. **Handle client disconnects**: Clean up server resources

### General

1. **Monitor connections**: Track active connection count
2. **Implement rate limiting**: Prevent abuse
3. **Use compression**: For large messages
4. **Log connection events**: Debug connection issues
5. **Test at scale**: Verify behavior with many concurrent connections
6. **Consider horizontal scaling**: Use Redis/message queues for multi-server

## See Also

- **salvo-websocket**: Detailed WebSocket implementation guide
- **salvo-sse**: Detailed SSE implementation guide
