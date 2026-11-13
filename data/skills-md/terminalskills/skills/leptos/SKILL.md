---
name: leptos
description: >-
  Leptos is a Rust web framework that builds reactive user interfaces compiled
  to WebAssembly, either as a client-side app or as a full-stack app with
  server-side rendering, hydration and server functions on Axum or Actix. Use
  when a user asks to "build a web app in Rust", "start a Leptos project",
  "add a server function", "use signals and resources in Leptos", "set up
  cargo-leptos", "fix Leptos code that no longer compiles after 0.7", or
  "deploy a Leptos SSR app". Covers Leptos 0.8: signals, the view macro,
  resources and Suspense, server functions and actions, routing, islands,
  Trunk and cargo-leptos.
license: Apache-2.0
compatibility: "Rust stable with the wasm32-unknown-unknown target. Client-side apps need Trunk; full-stack apps need cargo-leptos and Axum 0.8 or Actix. Compiled against leptos 0.8.21 on Rust 1.99."
metadata:
  author: terminal-skills
  version: 1.1.0
  category: development
  repository: https://github.com/leptos-rs/leptos
  tags: "rust, wasm, full-stack, reactive, ssr"
---

# Leptos — Full-Stack Rust Web Framework

## Overview

Leptos renders HTML from Rust components written with the `view!` macro and updates the page through fine-grained signals: when a signal changes, only the DOM nodes that read it are touched. It runs in two modes:

- **Client-side rendering (CSR)** — the app compiles to WebAssembly and is served as static files by Trunk. Fast builds, any backend.
- **Server-side rendering (SSR) with hydration** — one crate compiles twice: a native server binary (feature `ssr`) that renders HTML, and a WebAssembly bundle (feature `hydrate`) that makes it interactive. `cargo-leptos` coordinates both builds, and server functions let client code call server code directly.

Leptos 0.7 rewrote the API, and 0.8 keeps it. Code from older tutorials (`use leptos::*`, `create_signal`, `create_resource`, `.into_view()` on every branch) fails or warns: the current forms are `use leptos::prelude::*`, `signal()`, `Resource::new()`, `.into_any()`.

## Instructions

### 1. Set up the toolchain

Rust comes from rustup (use your distribution's `rustup` package, or download `rustup-init` and check it against the `.sha256` published next to it). Then:

```bash
rustup target add wasm32-unknown-unknown
cargo install --locked trunk            # CSR apps
cargo install --locked cargo-leptos     # full-stack apps
```

Stable Rust is enough. The `nightly` feature of `leptos` only adds function-call syntax for signals (`count()` instead of `count.get()`).

### 2. Client-side app with Trunk

```bash
cargo init reading-timer && cd reading-timer
cargo add leptos --features=csr
cargo add console_error_panic_hook
printf '<!DOCTYPE html>\n<html>\n  <head></head>\n  <body></body>\n</html>\n' > index.html
trunk serve --open                      # rebuilds and reloads on save
trunk build --release                   # static site in dist/
```

```rust
// src/main.rs
use leptos::prelude::*;

#[component]
fn Counter(#[prop(default = 0)] initial: i32, #[prop(into)] label: String) -> impl IntoView {
    let (count, set_count) = signal(initial);
    let doubled = Memo::new(move |_| count.get() * 2);
    Effect::new(move |_| leptos::logging::log!("count is {}", count.get()));

    view! {
        <button on:click=move |_| set_count.update(|n| *n -= 1)>"-"</button>
        <span class:negative=move || count.get() < 0>{label} ": " {count} " (doubled: " {doubled} ")"</span>
        <button on:click=move |_| *set_count.write() += 1>"+"</button>
        <Show when=move || { count.get() > 9 } fallback=|| view! { <p>"Keep going"</p> }>
            <p>"Double digits"</p>
        </Show>
    }
}

fn main() {
    console_error_panic_hook::set_once();
    leptos::mount::mount_to_body(|| view! { <Counter initial=3 label="Clicks"/> });
}
```

What to know about signals and the view macro:

- `signal(v)` returns a `(ReadSignal, WriteSignal)` pair; `RwSignal::new(v)` is one handle for both. Read with `.get()` (clones) or `.read()` (borrows); write with `.set(v)`, `.update(|v| ...)` or `*sig.write() = v`. All are `Copy`, so `move` closures can capture them freely.
- A value is reactive in the view only if it is a signal or a closure: `{count}` and `{move || count.get() * 2}` update, `{count.get()}` is evaluated once.
- `Memo::new` caches a derived value; `Effect::new` runs side effects in the browser after render and never on the server.
- Text nodes are string literals in quotes. Attributes: `on:click=`, `class:name=`, `style:color=`, `prop:value=`, and `bind:value=signal` for two-way input binding.
- Branches of an `if`/`match` inside `view!` must have one type: end each branch with `.into_any()` or use `<Show>`. Lists use `<For each=... key=... children=.../>` with a stable key.

### 3. Full-stack project with cargo-leptos

```bash
cargo leptos new --git https://github.com/leptos-rs/start-axum --name reading-list   # or .../start-actix
cd reading-list
cargo leptos watch                      # http://127.0.0.1:3000, rebuilds server and client
cargo leptos build --release            # target/release/reading-list + target/site/
```

`cargo leptos new` is a wizard: it asks "Use nightly features?" (answer No) and stops with `IO error: not a terminal` in a script or agent session. There, run `cargo generate --git https://github.com/leptos-rs/start-axum --name reading-list -d nightly=No` instead (`cargo install --locked cargo-generate`). The template's `Cargo.toml` wires the two builds. Keep this shape when adding dependencies: server-only crates are `optional` and listed under `ssr`.

```toml
[dependencies]
leptos = { version = "0.8" }
leptos_router = { version = "0.8" }
leptos_meta = { version = "0.8" }
serde = { version = "1", features = ["derive"] }                                        # added
axum = { version = "0.8", optional = true }
leptos_axum = { version = "0.8", optional = true }
tokio = { version = "1", features = ["rt-multi-thread"], optional = true }
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres"], optional = true }   # added
console_error_panic_hook = { version = "0.1", optional = true }
wasm-bindgen = { version = "0.2", optional = true }

[features]
hydrate = ["leptos/hydrate", "dep:console_error_panic_hook", "dep:wasm-bindgen"]
ssr = ["dep:axum", "dep:tokio", "dep:leptos_axum", "dep:sqlx", "leptos/ssr", "leptos_meta/ssr", "leptos_router/ssr"]
```

`[package.metadata.leptos]` in the same file sets `site-root`, `site-addr` (default `127.0.0.1:3000`), `bin-features = ["ssr"]` and `lib-features = ["hydrate"]`.

`src/lib.rs` exports `hydrate()`, which calls `leptos::mount::hydrate_body(App)`; `src/app.rs` holds `shell()` (the HTML document with `<HydrationScripts options/>`) and the `App` component; `src/main.rs` is the server. To give server functions a database pool, pass it as context when registering routes:

```rust
// src/main.rs (inside #[cfg(feature = "ssr")] #[tokio::main] async fn main)
use axum::Router;
use leptos::prelude::*;
use leptos_axum::{generate_route_list, LeptosRoutes};
use reading_list::app::{shell, App};

let database_url = std::env::var("DATABASE_URL").expect("DATABASE_URL is not set");
let pool = sqlx::postgres::PgPoolOptions::new().max_connections(5).connect(&database_url).await.expect("database");

let conf = get_configuration(None).unwrap();
let addr = conf.leptos_options.site_addr;
let leptos_options = conf.leptos_options;
let routes = generate_route_list(App);

let app = Router::new()
    .leptos_routes_with_context(
        &leptos_options,
        routes,
        move || provide_context(pool.clone()),          // visible to components and server functions
        {
            let leptos_options = leptos_options.clone();
            move || shell(leptos_options.clone())
        },
    )
    .fallback(leptos_axum::file_and_error_handler(shell))
    .with_state(leptos_options);

let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
axum::serve(listener, app.into_make_service()).await.unwrap();
```

### 4. Server functions, resources and actions

```rust
// src/app.rs
use leptos::prelude::*;
use leptos_router::{components::{Route, Router, Routes, A}, hooks::use_params_map, path};
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[cfg_attr(feature = "ssr", derive(sqlx::FromRow))]
pub struct Book {
    pub id: i64,
    pub title: String,
    pub author: String,
}

#[server]
pub async fn list_books() -> Result<Vec<Book>, ServerFnError> {
    let pool = expect_context::<sqlx::PgPool>();
    let books = sqlx::query_as::<_, Book>("SELECT id, title, author FROM books ORDER BY id DESC LIMIT 50")
        .fetch_all(&pool)
        .await?;
    Ok(books)
}

#[server]
pub async fn add_book(title: String, author: String) -> Result<(), ServerFnError> {
    if title.trim().is_empty() {
        return Err(ServerFnError::new("title is required"));
    }
    let pool = expect_context::<sqlx::PgPool>();
    sqlx::query("INSERT INTO books (title, author) VALUES ($1, $2)")
        .bind(title)
        .bind(author)
        .execute(&pool)
        .await?;
    Ok(())
}

#[component]
fn BookList() -> impl IntoView {
    let add = ServerAction::<AddBook>::new();
    // Refetches whenever the action finishes
    let books = Resource::new(move || add.version().get(), |_| list_books());

    view! {
        <ActionForm action=add>
            <input type="text" name="title" placeholder="Title"/>
            <input type="text" name="author" placeholder="Author"/>
            <button type="submit">"Add"</button>
        </ActionForm>
        <Suspense fallback=|| view! { <p>"Loading..."</p> }>
            <ErrorBoundary fallback=|errors| view! { <p class="error">{move || format!("{:?}", errors.get())}</p> }>
                <ul>
                    {move || Suspend::new(async move {
                        books.await.map(|books| {
                            books
                                .into_iter()
                                .map(|b| view! { <li><A href=format!("/books/{}", b.id)>{b.title}</A> " by " {b.author}</li> })
                                .collect_view()
                        })
                    })}
                </ul>
            </ErrorBoundary>
        </Suspense>
    }
}

#[component]
fn BookPage() -> impl IntoView {
    let params = use_params_map();
    let id = move || params.read().get("id").unwrap_or_default();
    view! { <h1>"Book #" {id}</h1> }
}
```

`#[server]` keeps the function body out of the WebAssembly build and generates an HTTP endpoint plus a client stub with the same signature. The macro also creates a struct named after the function in PascalCase (`AddBook`), which `ServerAction` and `<ActionForm>` use; the form's input `name`s must match the argument names, and it works without JavaScript. Arguments and return values must implement `Serialize` and `Deserialize`. Routes go inside `App` (`HomePage` is the template's start page):

```rust
<Router>
    <Routes fallback=|| "Page not found.">
        <Route path=path!("/") view=HomePage/>
        <Route path=path!("/books") view=BookList/>
        <Route path=path!("/books/:id") view=BookPage/>
    </Routes>
</Router>
```

### 5. Islands and release builds

Islands mode ships no WebAssembly for static components. Enable the `islands` feature on `leptos`, mark interactive components with `#[island]` instead of `#[component]`, call `leptos::mount::hydrate_islands()` in `hydrate()`, and write `<HydrationScripts options islands=true/>` in the shell.

The templates already build the WebAssembly bundle with a size-optimised profile (`[profile.wasm-release]` with `opt-level = "z"`, LTO and one codegen unit, selected by `lib-profile-release = "wasm-release"`); keep it when editing `Cargo.toml`.

To deploy, copy the binary from `target/release/` and the `target/site/` directory to the server and set `LEPTOS_SITE_ROOT=site` and `LEPTOS_SITE_ADDR=0.0.0.0:8080` (the address defaults to `127.0.0.1:3000`, which is unreachable from outside a container).

## Examples

### Example 1: A counter page without a backend

**User request:**

```
I want to try Leptos. Make me a small page with a counter that I can open in the browser, no server.
```

The agent uses the commands and `src/main.rs` from section 2, then runs `trunk serve --open`. Trunk prints the address it serves (`http://127.0.0.1:8080/` by default) and opens the page: `Clicks: 3 (doubled: 6)` with two buttons. Pressing "+" seven times shows `Clicks: 10 (doubled: 20)` and replaces "Keep going" with "Double digits"; the browser console logs `count is 10`. `trunk build --release` writes `index.html`, a `.js` loader and a `.wasm` file to `dist/` for any static host.

### Example 2: Add a database-backed page to a full-stack app

**User request:**

```
My start-axum project is called reading-list. Add a /books page that lists rows from Postgres and has a form to add one.
```

The agent adds `serde` and optional `sqlx` to `Cargo.toml` as in section 3, creates the pool in `main.rs` and passes it through `leptos_routes_with_context`, puts the `Book` struct, the two server functions and `BookList` from section 4 into `src/app.rs`, registers the `/books` routes, and verifies both halves compile:

```bash
cargo check --features ssr
cargo check --lib --features hydrate --target wasm32-unknown-unknown
DATABASE_URL="$READING_LIST_DATABASE_URL" cargo leptos watch
```

Both checks end with `Finished`. At `http://127.0.0.1:3000/books` the list is rendered into the HTML on the server; submitting the form calls `add_book`, the action's version changes, and the resource refetches the list without a page reload.

## Guidelines

1. **Pin the minor version** — 0.6, 0.7/0.8 and the 0.9 beta are not source-compatible; keep `leptos`, `leptos_router`, `leptos_meta` and the server integration on the same line and check which version a tutorial targets.
2. **Wrap comparisons in braces inside `view!`** — `when=move || count.get() > 9` does not parse because `>` closes the tag; write `when=move || { count.get() > 9 }`.
3. **Server-only code must not reach the client build** — make such dependencies `optional`, enable them in the `ssr` feature, and touch them only inside `#[server]` bodies or `#[cfg(feature = "ssr")]` items.
4. **Server functions are public HTTP endpoints** — validate input and check authentication inside every one; the client stub is not the only caller.
5. **Hydration needs identical output** — the server and the browser must render the same HTML; reading `window`, random values or the clock during render causes hydration errors. Do that work in `Effect::new`.
6. **Context is typed** — `expect_context::<T>()` panics when no value of that exact type was provided; `use_context::<T>()` returns an `Option`.
7. **Load data with resources, mutate with actions** — a `Resource` under `<Suspense>` streams in during SSR; make it depend on `action.version()` to refresh after writes.
8. **Run both `cargo check` commands in CI** — the `ssr` and `hydrate` builds fail independently.
9. **Compile times are the cost** — a full-stack rebuild compiles two targets; use CSR with Trunk when no server rendering is needed.
