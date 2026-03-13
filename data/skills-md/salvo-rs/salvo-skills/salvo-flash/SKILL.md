---
name: salvo-flash
description: Implement flash messages for one-time notifications across redirects. Use for success/error messages after form submissions.
---

# Salvo Flash Messages

This skill helps implement flash messages in Salvo applications for displaying one-time notifications that survive redirects.

## What are Flash Messages?

Flash messages are temporary messages stored between requests, typically used to show feedback after form submissions or actions. They're automatically deleted after being displayed once.

Common use cases:
- "Successfully logged in!"
- "Item added to cart"
- "Error: Invalid email format"
- "Profile updated successfully"

## Setup

```toml
[dependencies]
salvo = { version = "0.89.0", features = ["flash"] }
```

## Basic Flash Messages with Cookie Store

```rust
use std::fmt::Write;
use salvo::flash::{CookieStore, FlashDepotExt};
use salvo::prelude::*;

#[handler]
async fn set_flash(depot: &mut Depot, res: &mut Response) {
    // Get outgoing flash and add messages
    let flash = depot.outgoing_flash_mut();
    flash.info("Operation completed successfully!");
    flash.debug("Debug information here");

    // Redirect to show the message
    res.render(Redirect::other("/show"));
}

#[handler]
async fn show_flash(depot: &mut Depot, res: &mut Response) {
    let mut output = String::new();

    // Read incoming flash messages
    if let Some(flash) = depot.incoming_flash() {
        for message in flash.iter() {
            writeln!(output, "[{}] {}", message.level, message.value).unwrap();
        }
    }

    if output.is_empty() {
        output = "No flash messages".to_string();
    }

    res.render(Text::Plain(output));
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .hoop(CookieStore::new().into_handler())
        .push(Router::with_path("set").get(set_flash))
        .push(Router::with_path("show").get(show_flash));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Flash Message Levels

```rust
use salvo::flash::FlashDepotExt;

#[handler]
async fn add_messages(depot: &mut Depot, res: &mut Response) {
    let flash = depot.outgoing_flash_mut();

    // Different message levels
    flash.debug("Debug message");     // For debugging
    flash.info("Info message");       // General information
    flash.success("Success message"); // Success notifications
    flash.warning("Warning message"); // Warnings
    flash.error("Error message");     // Error notifications

    res.render(Redirect::other("/"));
}
```

## Flash with Session Store

For larger messages or when cookies aren't suitable:

```rust
use salvo::flash::{SessionStore, FlashDepotExt};
use salvo::session::{CookieStore as SessionCookieStore, SessionHandler};
use salvo::prelude::*;

#[tokio::main]
async fn main() {
    // Session handler is required for session-based flash
    let session_handler = SessionHandler::builder(
        SessionCookieStore::new(),
        b"secretabsecretabsecretabsecretabsecretabsecretabsecretabsecretab",
    )
    .build()
    .unwrap();

    // Flash store using sessions
    let flash_handler = SessionStore::new().into_handler();

    let router = Router::new()
        .hoop(session_handler)   // Session first
        .hoop(flash_handler)     // Then flash
        .push(Router::with_path("set").get(set_flash))
        .push(Router::with_path("show").get(show_flash));

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Form Submission with Flash

```rust
use salvo::flash::{CookieStore, FlashDepotExt};
use salvo::prelude::*;
use serde::Deserialize;

#[derive(Deserialize)]
struct ContactForm {
    name: String,
    email: String,
    message: String,
}

#[handler]
async fn show_form(depot: &mut Depot, res: &mut Response) {
    // Check for flash messages
    let mut flash_html = String::new();
    if let Some(flash) = depot.incoming_flash() {
        for msg in flash.iter() {
            let class = match msg.level.as_str() {
                "success" => "alert-success",
                "error" => "alert-error",
                "warning" => "alert-warning",
                _ => "alert-info",
            };
            flash_html.push_str(&format!(
                r#"<div class="{}">{}</div>"#,
                class, msg.value
            ));
        }
    }

    res.render(Text::Html(format!(r#"
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .alert-success {{ background: #d4edda; padding: 10px; margin: 10px 0; }}
                .alert-error {{ background: #f8d7da; padding: 10px; margin: 10px 0; }}
                .alert-warning {{ background: #fff3cd; padding: 10px; margin: 10px 0; }}
                .alert-info {{ background: #d1ecf1; padding: 10px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            {flash_html}
            <h1>Contact Us</h1>
            <form method="post" action="/contact">
                <p><input type="text" name="name" placeholder="Name" required /></p>
                <p><input type="email" name="email" placeholder="Email" required /></p>
                <p><textarea name="message" placeholder="Message" required></textarea></p>
                <button type="submit">Send</button>
            </form>
        </body>
        </html>
    "#)));
}

#[handler]
async fn handle_form(req: &mut Request, depot: &mut Depot, res: &mut Response) {
    match req.parse_form::<ContactForm>().await {
        Ok(form) => {
            // Process the form...
            println!("Received message from: {} <{}>", form.name, form.email);

            // Success flash
            depot.outgoing_flash_mut()
                .success("Thank you! Your message has been sent.");
        }
        Err(e) => {
            // Error flash
            depot.outgoing_flash_mut()
                .error(format!("Error: {}", e));
        }
    }

    res.render(Redirect::other("/contact"));
}

#[tokio::main]
async fn main() {
    let router = Router::new()
        .hoop(CookieStore::new().into_handler())
        .push(
            Router::with_path("contact")
                .get(show_form)
                .post(handle_form)
        );

    let acceptor = TcpListener::new("0.0.0.0:8080").bind().await;
    Server::new(acceptor).serve(router).await;
}
```

## Multiple Flash Messages

```rust
#[handler]
async fn process_action(depot: &mut Depot, res: &mut Response) {
    let flash = depot.outgoing_flash_mut();

    // Add multiple messages
    flash.info("Processing started...");
    flash.success("Step 1 completed");
    flash.success("Step 2 completed");
    flash.warning("Step 3 had minor issues but continued");
    flash.success("All steps completed!");

    res.render(Redirect::other("/results"));
}

#[handler]
async fn show_results(depot: &mut Depot, res: &mut Response) {
    let mut html = String::from("<h1>Results</h1><ul>");

    if let Some(flash) = depot.incoming_flash() {
        for msg in flash.iter() {
            html.push_str(&format!(
                "<li><strong>{}:</strong> {}</li>",
                msg.level, msg.value
            ));
        }
    }

    html.push_str("</ul>");
    res.render(Text::Html(html));
}
```

## Flash with CRUD Operations

```rust
use salvo::flash::FlashDepotExt;
use salvo::prelude::*;

#[handler]
async fn create_item(depot: &mut Depot, res: &mut Response) {
    // Create item logic...
    let item_id = 123;

    depot.outgoing_flash_mut()
        .success(format!("Item #{} created successfully!", item_id));

    res.render(Redirect::other("/items"));
}

#[handler]
async fn update_item(depot: &mut Depot, res: &mut Response) {
    // Update item logic...

    depot.outgoing_flash_mut()
        .success("Item updated successfully!");

    res.render(Redirect::other("/items"));
}

#[handler]
async fn delete_item(depot: &mut Depot, res: &mut Response) {
    // Delete item logic...

    depot.outgoing_flash_mut()
        .info("Item has been deleted.");

    res.render(Redirect::other("/items"));
}

#[handler]
async fn list_items(depot: &mut Depot, res: &mut Response) {
    let mut flash_messages = Vec::new();

    if let Some(flash) = depot.incoming_flash() {
        for msg in flash.iter() {
            flash_messages.push(format!("[{}] {}", msg.level, msg.value));
        }
    }

    // Render list with flash messages...
    res.render(Json(serde_json::json!({
        "flash": flash_messages,
        "items": []
    })));
}
```

## Flash with JSON API

For API responses that need flash-like behavior:

```rust
use salvo::flash::FlashDepotExt;
use salvo::prelude::*;
use serde::Serialize;

#[derive(Serialize)]
struct ApiResponse<T> {
    success: bool,
    data: Option<T>,
    messages: Vec<FlashMessage>,
}

#[derive(Serialize)]
struct FlashMessage {
    level: String,
    text: String,
}

#[handler]
async fn api_create(depot: &mut Depot, res: &mut Response) {
    // Store flash for potential redirect
    depot.outgoing_flash_mut()
        .success("Created successfully");

    // Also return in JSON for AJAX requests
    res.render(Json(ApiResponse {
        success: true,
        data: Some(serde_json::json!({"id": 1})),
        messages: vec![
            FlashMessage {
                level: "success".to_string(),
                text: "Created successfully".to_string(),
            }
        ],
    }));
}
```

## Rendering Flash Messages

### As HTML Alerts

```rust
fn render_flash_html(depot: &Depot) -> String {
    let mut html = String::new();

    if let Some(flash) = depot.incoming_flash() {
        html.push_str("<div class=\"flash-container\">");
        for msg in flash.iter() {
            let (class, icon) = match msg.level.as_str() {
                "success" => ("flash-success", "✓"),
                "error" => ("flash-error", "✗"),
                "warning" => ("flash-warning", "⚠"),
                "info" => ("flash-info", "ℹ"),
                _ => ("flash-debug", "🔧"),
            };
            html.push_str(&format!(
                r#"<div class="flash {}"><span>{}</span> {}</div>"#,
                class, icon, msg.value
            ));
        }
        html.push_str("</div>");
    }

    html
}
```

### As JSON

```rust
fn flash_to_json(depot: &Depot) -> serde_json::Value {
    let messages: Vec<_> = depot
        .incoming_flash()
        .map(|flash| {
            flash.iter()
                .map(|msg| {
                    serde_json::json!({
                        "level": msg.level,
                        "message": msg.value
                    })
                })
                .collect()
        })
        .unwrap_or_default();

    serde_json::json!({ "flash": messages })
}
```

## Best Practices

1. **Use appropriate levels**: Match message importance to level (success, error, warning, info)
2. **Keep messages brief**: Flash messages should be short and clear
3. **Redirect after POST**: Use Post-Redirect-Get pattern with flash messages
4. **Style by level**: Use different colors/icons for different message levels
5. **Cookie store for simple cases**: Session store for larger/sensitive messages
6. **Clear after display**: Flash messages auto-clear, don't display twice
7. **Handle empty flash**: Check if flash exists before rendering
8. **Escape HTML**: Sanitize message content if it includes user input
