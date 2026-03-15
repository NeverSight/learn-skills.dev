---
name: salvo-sse
description: Implement Server-Sent Events for real-time server-to-client updates. Use for live feeds, notifications, and streaming data.
---

# Salvo Server-Sent Events (SSE)

This skill helps implement Server-Sent Events in Salvo applications for real-time server-to-client communication.

## What is SSE?

Server-Sent Events (SSE) is a standard for pushing updates from server to client over HTTP. Unlike WebSocket, SSE is:

- **Unidirectional**: Server to client only
- **Simple**: Uses standard HTTP
- **Auto-reconnecting**: Browsers handle reconnection
- **Text-based**: Sends text/event-stream

## When to Use SSE vs WebSocket

| Use Case | SSE | WebSocket |
|----------|-----|-----------|
| Live notifications | ✓ | ✓ |
| Real-time feeds | ✓ | ✓ |
| Chat messages | | ✓ |
| Gaming | | ✓ |
| Bidirectional needed | | ✓ |
| Simple implementation | ✓ | |

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["sse"] }
futures-util = "0.3"
tokio = { version = "1", features = ["full"] }
tokio-stream = "0.1"
```

## Basic SSE Counter

```rust
use std::convert::Infallible;
use std::time::Duration;

use futures_util::StreamExt;
use salvo::prelude::*;
use salvo::sse::{self, SseEvent};
use tokio::time::interval;
use tokio_stream::wrappers::IntervalStream;

#[handler]
async fn sse_counter(res: &mut Response) {
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

#[handler]
async fn index(res: &mut Response) {
    res.render(Text::Html(r#"
        <!DOCTYPE html>
        <html>
        <body>
            <h1>SSE Counter</h1>
            <div id="count">0</div>
            <script>
                const source = new EventSource('/events');
                source.onmessage = (e) => {
                    document.getElementById('count').textContent = e.data;
                };
            </script>
        </body>
        </html>
    "#));
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .get(index)
        .push(Router::with_path("events").get(sse_counter));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## SSE Event Types

```rust
use salvo::sse::SseEvent;

// Simple text event
let event = SseEvent::default().text("Hello, World!");

// Named event
let event = SseEvent::default()
    .name("notification")
    .text("New message received");

// JSON data
let event = SseEvent::default()
    .name("update")
    .json(&serde_json::json!({"count": 42}))?;

// With event ID (for reconnection)
let event = SseEvent::default()
    .id("msg-123")
    .text("Message content");

// With retry suggestion (milliseconds)
let event = SseEvent::default()
    .retry(Duration::from_secs(5))
    .text("Reconnect in 5 seconds");

// Comment (keep-alive)
let event = SseEvent::default().comment("keep-alive");
```

## SSE with Keep-Alive

```rust
use salvo::sse::{SseEvent, SseKeepAlive};

#[handler]
async fn sse_with_keepalive(res: &mut Response) {
    let stream = create_event_stream();

    // Wrap stream with keep-alive (sends comments periodically)
    SseKeepAlive::new(stream)
        .interval(Duration::from_secs(15))  // Keep-alive interval
        .text("ping")                        // Keep-alive message
        .stream(res);
}
```

## Chat Room with SSE

```rust
use std::collections::HashMap;
use std::sync::LazyLock;
use std::sync::atomic::{AtomicUsize, Ordering};

use futures_util::StreamExt;
use parking_lot::Mutex;
use salvo::prelude::*;
use salvo::sse::{SseEvent, SseKeepAlive};
use tokio::sync::mpsc;
use tokio_stream::wrappers::UnboundedReceiverStream;

#[derive(Debug)]
enum Message {
    UserId(usize),
    Reply(String),
}

type Users = Mutex<HashMap<usize, mpsc::UnboundedSender<Message>>>;

static NEXT_USER_ID: AtomicUsize = AtomicUsize::new(1);
static ONLINE_USERS: LazyLock<Users> = LazyLock::new(Users::default);

#[handler]
async fn sse_connect(res: &mut Response) {
    let my_id = NEXT_USER_ID.fetch_add(1, Ordering::Relaxed);
    println!("User {} connected", my_id);

    let (tx, rx) = mpsc::unbounded_channel();
    let rx = UnboundedReceiverStream::new(rx);

    // Send user their ID
    tx.send(Message::UserId(my_id)).unwrap();

    // Register user
    ONLINE_USERS.lock().insert(my_id, tx);

    // Convert messages to SSE events
    let stream = rx.map(|msg| match msg {
        Message::UserId(id) => {
            Ok::<_, salvo::Error>(SseEvent::default().name("user").text(id.to_string()))
        }
        Message::Reply(text) => {
            Ok(SseEvent::default().text(text))
        }
    });

    SseKeepAlive::new(stream).stream(res);
}

#[handler]
async fn send_message(req: &mut Request, res: &mut Response) {
    let my_id: usize = req.param("id").unwrap();
    let msg = std::str::from_utf8(req.payload().await.unwrap()).unwrap();

    let formatted = format!("<User#{}>: {}", my_id, msg);

    // Broadcast to all users except sender
    ONLINE_USERS.lock().retain(|uid, tx| {
        if *uid == my_id {
            true
        } else {
            tx.send(Message::Reply(formatted.clone())).is_ok()
        }
    });

    res.status_code(StatusCode::OK);
}

#[handler]
async fn index(res: &mut Response) {
    res.render(Text::Html(CHAT_HTML));
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .get(index)
        .push(
            Router::with_path("chat")
                .get(sse_connect)
                .push(Router::with_path("{id}").post(send_message))
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}

static CHAT_HTML: &str = r#"<!DOCTYPE html>
<html>
<body>
    <h1>SSE Chat</h1>
    <div id="chat"><em>Connecting...</em></div>
    <input type="text" id="msg" />
    <button onclick="send()">Send</button>
    <script>
        let userId;
        const chat = document.getElementById('chat');
        const sse = new EventSource('/chat');

        sse.onopen = () => chat.innerHTML = '<em>Connected!</em>';

        sse.addEventListener('user', (e) => {
            userId = e.data;
            console.log('My ID:', userId);
        });

        sse.onmessage = (e) => {
            const p = document.createElement('p');
            p.textContent = e.data;
            chat.appendChild(p);
        };

        function send() {
            const input = document.getElementById('msg');
            fetch(`/chat/${userId}`, {
                method: 'POST',
                body: input.value
            });
            const p = document.createElement('p');
            p.textContent = '<You>: ' + input.value;
            chat.appendChild(p);
            input.value = '';
        }
    </script>
</body>
</html>"#;
```

## Live Data Feed

```rust
use salvo::sse::SseEvent;
use serde::Serialize;

#[derive(Serialize)]
struct StockPrice {
    symbol: String,
    price: f64,
    change: f64,
}

#[handler]
async fn stock_feed(res: &mut Response) {
    let stream = async_stream::stream! {
        let symbols = vec!["AAPL", "GOOGL", "MSFT"];
        let mut prices: HashMap<&str, f64> = HashMap::new();
        prices.insert("AAPL", 150.0);
        prices.insert("GOOGL", 140.0);
        prices.insert("MSFT", 380.0);

        loop {
            tokio::time::sleep(Duration::from_secs(1)).await;

            for symbol in &symbols {
                // Simulate price change
                let change = (rand::random::<f64>() - 0.5) * 2.0;
                let price = prices.get_mut(symbol).unwrap();
                *price += change;

                let stock = StockPrice {
                    symbol: symbol.to_string(),
                    price: *price,
                    change,
                };

                yield Ok::<_, Infallible>(
                    SseEvent::default()
                        .name("price")
                        .json(&stock)
                        .unwrap()
                );
            }
        }
    };

    sse::stream(res, stream);
}
```

## Notification System

```rust
use std::sync::Arc;
use tokio::sync::broadcast;
use salvo::sse::{SseEvent, SseKeepAlive};

#[derive(Clone)]
struct NotificationService {
    sender: broadcast::Sender<Notification>,
}

#[derive(Clone, Serialize)]
struct Notification {
    id: u64,
    title: String,
    message: String,
    timestamp: i64,
}

impl NotificationService {
    fn new() -> Self {
        let (sender, _) = broadcast::channel(100);
        Self { sender }
    }

    fn subscribe(&self) -> broadcast::Receiver<Notification> {
        self.sender.subscribe()
    }

    fn send(&self, notification: Notification) {
        let _ = self.sender.send(notification);
    }
}

#[handler]
async fn notifications(depot: &mut Depot, res: &mut Response) {
    let service = depot.obtain::<NotificationService>().unwrap();
    let mut receiver = service.subscribe();

    let stream = async_stream::stream! {
        while let Ok(notification) = receiver.recv().await {
            yield Ok::<_, salvo::Error>(
                SseEvent::default()
                    .name("notification")
                    .id(notification.id.to_string())
                    .json(&notification)
                    .unwrap()
            );
        }
    };

    SseKeepAlive::new(stream)
        .interval(Duration::from_secs(30))
        .stream(res);
}

#[handler]
async fn send_notification(depot: &mut Depot, res: &mut Response) {
    let service = depot.obtain::<NotificationService>().unwrap();

    service.send(Notification {
        id: 1,
        title: "New Alert".to_string(),
        message: "Something happened!".to_string(),
        timestamp: chrono::Utc::now().timestamp(),
    });

    res.render("Notification sent");
}
```

## SSE with Event ID for Reconnection

```rust
use std::sync::atomic::{AtomicU64, Ordering};

static EVENT_ID: AtomicU64 = AtomicU64::new(0);

#[handler]
async fn sse_with_ids(req: &mut Request, res: &mut Response) {
    // Get last event ID from client (for reconnection)
    let last_id: u64 = req
        .header("Last-Event-ID")
        .and_then(|s| s.parse().ok())
        .unwrap_or(0);

    println!("Client reconnecting from event ID: {}", last_id);

    let stream = async_stream::stream! {
        loop {
            tokio::time::sleep(Duration::from_secs(1)).await;

            let id = EVENT_ID.fetch_add(1, Ordering::Relaxed);

            // Skip events client already has
            if id <= last_id {
                continue;
            }

            yield Ok::<_, Infallible>(
                SseEvent::default()
                    .id(id.to_string())
                    .text(format!("Event {}", id))
            );
        }
    };

    sse::stream(res, stream);
}
```

## Client-Side JavaScript

```javascript
// Basic SSE connection
const source = new EventSource('/events');

// Handle generic messages
source.onmessage = (event) => {
    console.log('Message:', event.data);
};

// Handle named events
source.addEventListener('notification', (event) => {
    const data = JSON.parse(event.data);
    console.log('Notification:', data);
});

// Handle connection open
source.onopen = () => {
    console.log('Connected');
};

// Handle errors
source.onerror = (error) => {
    console.error('SSE Error:', error);
    if (source.readyState === EventSource.CLOSED) {
        console.log('Connection closed');
    }
};

// Close connection
source.close();
```

## Best Practices

1. **Use keep-alive**: Prevent connection timeout with periodic comments
2. **Include event IDs**: Enable reconnection from last received event
3. **Set retry intervals**: Guide client reconnection behavior
4. **Use named events**: Organize different message types
5. **Handle disconnections**: Clients auto-reconnect, but clean up server-side
6. **Consider CORS**: SSE follows same-origin policy
7. **Limit connections**: Each client uses a connection; consider connection limits
8. **Use broadcast channels**: Efficiently send same data to multiple clients
