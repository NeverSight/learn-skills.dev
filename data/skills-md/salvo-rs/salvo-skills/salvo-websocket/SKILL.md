---
name: salvo-websocket
description: Implement WebSocket connections for real-time bidirectional communication. Use for chat, live updates, gaming, and collaborative features.
---

# Salvo WebSocket

This skill helps implement WebSocket connections in Salvo applications for real-time bidirectional communication.

## What is WebSocket?

WebSocket provides full-duplex communication channels over a single TCP connection, enabling real-time data exchange between client and server.

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["websocket"] }
futures-util = "0.3"
tokio = { version = "1", features = ["full"] }
```

## Basic WebSocket Echo Server

```rust
use salvo::prelude::*;
use salvo::websocket::WebSocketUpgrade;

#[handler]
async fn ws_handler(req: &mut Request, res: &mut Response) -> Result<(), StatusError> {
    WebSocketUpgrade::new()
        .upgrade(req, res, |mut ws| async move {
            // Echo back received messages
            while let Some(msg) = ws.recv().await {
                let msg = match msg {
                    Ok(msg) => msg,
                    Err(_) => return, // Client disconnected
                };

                if ws.send(msg).await.is_err() {
                    return; // Client disconnected
                }
            }
        })
        .await
}

#[handler]
async fn index(res: &mut Response) {
    res.render(Text::Html(r#"
        <!DOCTYPE html>
        <html>
        <body>
            <h1>WebSocket Echo</h1>
            <input type="text" id="msg" />
            <button onclick="send()">Send</button>
            <div id="output"></div>
            <script>
                const ws = new WebSocket(`ws://${location.host}/ws`);
                ws.onmessage = (e) => {
                    document.getElementById('output').innerHTML += `<p>${e.data}</p>`;
                };
                function send() {
                    ws.send(document.getElementById('msg').value);
                }
            </script>
        </body>
        </html>
    "#));
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .get(index)
        .push(Router::with_path("ws").goal(ws_handler));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## WebSocket with Query Parameters

```rust
use salvo::prelude::*;
use salvo::websocket::WebSocketUpgrade;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
struct ConnectParams {
    user_id: usize,
    name: String,
}

#[handler]
async fn connect(req: &mut Request, res: &mut Response) -> Result<(), StatusError> {
    // Parse query parameters before upgrade
    let params = req.parse_queries::<ConnectParams>();

    WebSocketUpgrade::new()
        .upgrade(req, res, |mut ws| async move {
            println!("User connected: {:?}", params);

            while let Some(msg) = ws.recv().await {
                match msg {
                    Ok(msg) => {
                        if ws.send(msg).await.is_err() {
                            break;
                        }
                    }
                    Err(_) => break,
                }
            }

            println!("User disconnected: {:?}", params);
        })
        .await
}
```

## Chat Room Example

```rust
use std::collections::HashMap;
use std::sync::LazyLock;
use std::sync::atomic::{AtomicUsize, Ordering};

use futures_util::{FutureExt, StreamExt};
use salvo::prelude::*;
use salvo::websocket::{Message, WebSocket, WebSocketUpgrade};
use tokio::sync::{RwLock, mpsc};
use tokio_stream::wrappers::UnboundedReceiverStream;

type Users = RwLock<HashMap<usize, mpsc::UnboundedSender<Result<Message, salvo::Error>>>>;

static NEXT_USER_ID: AtomicUsize = AtomicUsize::new(1);
static ONLINE_USERS: LazyLock<Users> = LazyLock::new(Users::default);

#[handler]
async fn chat(req: &mut Request, res: &mut Response) -> Result<(), StatusError> {
    WebSocketUpgrade::new()
        .upgrade(req, res, handle_socket)
        .await
}

async fn handle_socket(ws: WebSocket) {
    let my_id = NEXT_USER_ID.fetch_add(1, Ordering::Relaxed);
    println!("New user connected: {}", my_id);

    // Split socket into sender and receiver
    let (user_ws_tx, mut user_ws_rx) = ws.split();

    // Create channel for this user
    let (tx, rx) = mpsc::unbounded_channel();
    let rx = UnboundedReceiverStream::new(rx);

    // Forward messages from channel to WebSocket
    let send_task = rx.forward(user_ws_tx).map(|result| {
        if let Err(e) = result {
            eprintln!("WebSocket send error: {:?}", e);
        }
    });
    tokio::spawn(send_task);

    // Register user
    ONLINE_USERS.write().await.insert(my_id, tx);

    // Handle incoming messages
    while let Some(result) = user_ws_rx.next().await {
        match result {
            Ok(msg) => {
                if let Ok(text) = msg.as_str() {
                    broadcast_message(my_id, text).await;
                }
            }
            Err(e) => {
                eprintln!("WebSocket error: {:?}", e);
                break;
            }
        }
    }

    // User disconnected
    ONLINE_USERS.write().await.remove(&my_id);
    println!("User {} disconnected", my_id);
}

async fn broadcast_message(sender_id: usize, msg: &str) {
    let formatted = format!("<User#{}>: {}", sender_id, msg);

    for (&uid, tx) in ONLINE_USERS.read().await.iter() {
        if uid != sender_id {
            let _ = tx.send(Ok(Message::text(formatted.clone())));
        }
    }
}

#[handler]
async fn index(res: &mut Response) {
    res.render(Text::Html(CHAT_HTML));
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .get(index)
        .push(Router::with_path("chat").goal(chat));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}

static CHAT_HTML: &str = r#"<!DOCTYPE html>
<html>
<head><title>Chat</title></head>
<body>
    <h1>WebSocket Chat</h1>
    <div id="chat"></div>
    <input type="text" id="msg" />
    <button onclick="send()">Send</button>
    <script>
        const chat = document.getElementById('chat');
        const ws = new WebSocket(`ws://${location.host}/chat`);

        ws.onopen = () => chat.innerHTML = '<p><em>Connected!</em></p>';
        ws.onclose = () => chat.innerHTML += '<p><em>Disconnected</em></p>';
        ws.onmessage = (e) => {
            const p = document.createElement('p');
            p.textContent = e.data;
            chat.appendChild(p);
        };

        function send() {
            const input = document.getElementById('msg');
            ws.send(input.value);
            const p = document.createElement('p');
            p.textContent = '<You>: ' + input.value;
            chat.appendChild(p);
            input.value = '';
        }
    </script>
</body>
</html>"#;
```

## WebSocket with Authentication

```rust
use salvo::prelude::*;
use salvo::websocket::WebSocketUpgrade;
use salvo::jwt_auth::{ConstDecoder, JwtAuth, JwtAuthDepotExt};

#[handler]
async fn ws_authenticated(
    req: &mut Request,
    depot: &mut Depot,
    res: &mut Response,
) -> Result<(), StatusError> {
    // Check JWT token
    let token = depot.jwt_auth_data::<Claims>();
    if token.is_none() {
        return Err(StatusError::unauthorized());
    }

    let user_id = token.unwrap().claims.user_id;

    WebSocketUpgrade::new()
        .upgrade(req, res, move |mut ws| async move {
            println!("Authenticated user {} connected", user_id);

            while let Some(msg) = ws.recv().await {
                match msg {
                    Ok(msg) => {
                        if ws.send(msg).await.is_err() {
                            break;
                        }
                    }
                    Err(_) => break,
                }
            }
        })
        .await
}
```

## Handling Different Message Types

```rust
use salvo::websocket::{Message, WebSocket};

async fn handle_messages(mut ws: WebSocket) {
    while let Some(result) = ws.recv().await {
        let msg = match result {
            Ok(msg) => msg,
            Err(_) => break,
        };

        // Handle different message types
        if msg.is_text() {
            let text = msg.as_str().unwrap();
            println!("Text message: {}", text);

            // Echo back
            ws.send(Message::text(format!("You said: {}", text)))
                .await
                .ok();
        } else if msg.is_binary() {
            let bytes = msg.as_bytes();
            println!("Binary message: {} bytes", bytes.len());

            // Echo back
            ws.send(Message::binary(bytes.to_vec())).await.ok();
        } else if msg.is_ping() {
            // Pong is sent automatically
            println!("Ping received");
        } else if msg.is_close() {
            println!("Close requested");
            break;
        }
    }
}
```

## WebSocket with Room Support

```rust
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use salvo::websocket::Message;
use tokio::sync::mpsc;

type Tx = mpsc::UnboundedSender<Result<Message, salvo::Error>>;
type RoomUsers = HashMap<usize, Tx>;
type Rooms = Arc<RwLock<HashMap<String, RoomUsers>>>;

async fn join_room(rooms: &Rooms, room_name: &str, user_id: usize, tx: Tx) {
    let mut rooms = rooms.write().await;
    rooms
        .entry(room_name.to_string())
        .or_default()
        .insert(user_id, tx);
}

async fn leave_room(rooms: &Rooms, room_name: &str, user_id: usize) {
    let mut rooms = rooms.write().await;
    if let Some(room) = rooms.get_mut(room_name) {
        room.remove(&user_id);
        if room.is_empty() {
            rooms.remove(room_name);
        }
    }
}

async fn broadcast_to_room(
    rooms: &Rooms,
    room_name: &str,
    sender_id: usize,
    message: &str,
) {
    let rooms = rooms.read().await;
    if let Some(room) = rooms.get(room_name) {
        for (&uid, tx) in room.iter() {
            if uid != sender_id {
                let _ = tx.send(Ok(Message::text(message.to_string())));
            }
        }
    }
}
```

## Heartbeat/Keep-Alive

```rust
use std::time::Duration;
use salvo::websocket::{Message, WebSocket};
use tokio::time::interval;

async fn handle_with_heartbeat(ws: WebSocket) {
    let (mut tx, mut rx) = ws.split();

    // Heartbeat task
    let heartbeat = async move {
        let mut interval = interval(Duration::from_secs(30));
        loop {
            interval.tick().await;
            if tx.send(Message::ping(vec![])).await.is_err() {
                break;
            }
        }
    };

    // Message handling task
    let messages = async move {
        while let Some(msg) = rx.next().await {
            match msg {
                Ok(msg) if msg.is_pong() => {
                    println!("Pong received");
                }
                Ok(msg) => {
                    // Handle other messages
                }
                Err(_) => break,
            }
        }
    };

    // Run both tasks concurrently
    tokio::select! {
        _ = heartbeat => {},
        _ = messages => {},
    }
}
```

## WebSocket with JSON Messages

```rust
use salvo::websocket::{Message, WebSocket};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
#[serde(tag = "type")]
enum WsMessage {
    Chat { content: String },
    Join { room: String },
    Leave { room: String },
    Typing { user: String },
}

async fn handle_json_messages(mut ws: WebSocket) {
    while let Some(result) = ws.recv().await {
        let msg = match result {
            Ok(msg) => msg,
            Err(_) => break,
        };

        if let Ok(text) = msg.as_str() {
            if let Ok(ws_msg) = serde_json::from_str::<WsMessage>(text) {
                match ws_msg {
                    WsMessage::Chat { content } => {
                        println!("Chat: {}", content);
                    }
                    WsMessage::Join { room } => {
                        println!("Joining room: {}", room);
                    }
                    WsMessage::Leave { room } => {
                        println!("Leaving room: {}", room);
                    }
                    WsMessage::Typing { user } => {
                        println!("{} is typing...", user);
                    }
                }
            }
        }
    }
}

// Send JSON message
async fn send_json<T: Serialize>(ws: &mut WebSocket, msg: &T) -> Result<(), salvo::Error> {
    let json = serde_json::to_string(msg).unwrap();
    ws.send(Message::text(json)).await
}
```

## Best Practices

1. **Handle disconnections gracefully**: Always check for errors when sending/receiving
2. **Use channels for broadcasting**: Don't hold locks while sending messages
3. **Implement heartbeat**: Detect dead connections with ping/pong
4. **Validate messages**: Don't trust client input
5. **Limit message size**: Prevent memory exhaustion
6. **Use JSON for structured data**: Makes debugging easier
7. **Clean up on disconnect**: Remove users from rooms/lists
8. **Consider backpressure**: Handle slow consumers appropriately
