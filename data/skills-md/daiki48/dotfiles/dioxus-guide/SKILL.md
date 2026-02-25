---
name: dioxus-guide
description: Dioxus v0.7.x desktop app guide. Components, Signal state, rsx! macro, hooks, events, Context API, async.
---

# Dioxus v0.7.x Development Guide

## Breaking Changes (from 0.6)

Deprecated in 0.7:
- `cx` / `Scope` → Not needed
- `use_state` → `use_signal`
- `use_ref` → `use_signal`

## Basic Setup

```rust
use dioxus::prelude::*;

fn main() { dioxus::launch(App); }

#[component]
fn App() -> Element {
    rsx! { "Hello, Dioxus!" }
}
```

```toml
[dependencies]
dioxus = { version = "0.7.2", features = ["router"] }

[features]
default = ["desktop"]
web = ["dioxus/web"]
desktop = ["dioxus/desktop"]
```

## RSX Macro

```rust
rsx! {
    div { class: "container", color: "red",
        width: if condition { "100%" },  // Conditional attr
        "Hello!"
    }

    for i in 0..5 { div { "{i}" } }      // Loop (prefer for over iter)

    if condition { div { "True!" } }      // Conditional

    {children}                            // Expressions in braces
}
```

## Components

```rust
#[component]
fn MyComponent(
    title: String,
    #[prop(optional)] class: Option<String>,
    #[prop(default = 10)] limit: usize,
    children: Element,
) -> Element {
    rsx! {
        div { class: class.unwrap_or_default(),
            h1 { "{title}" }
            {children}
        }
    }
}
```

**Props**: Must be owned types (`String`, not `&str`), implement `PartialEq` + `Clone`

## State: use_signal

```rust
#[component]
fn Counter() -> Element {
    let mut count = use_signal(|| 0);

    rsx! {
        h1 { "Count: {count}" }
        button { onclick: move |_| *count.write() += 1, "+" }
    }
}

// Read
count()        // Clone value
count.read()   // Reference (&T)

// Write
count.set(10)
*count.write() = 10
count.with_mut(|c| *c += 1)
```

## Derived State: use_memo

```rust
let doubled = use_memo(move || count() * 2);
```

## Context API

```rust
// Provider
#[component]
fn App() -> Element {
    let theme = use_signal(|| "light".to_string());
    use_context_provider(|| theme);
    rsx! { Child {} }
}

// Consumer
#[component]
fn Child() -> Element {
    let theme = use_context::<Signal<String>>();
    rsx! { div { "Theme: {theme}" } }
}
```

## Async: use_resource

```rust
let data = use_resource(move || async move { fetch_data().await });

match data() {
    Some(result) => rsx! { div { "{result}" } },
    None => rsx! { "Loading..." },
}

// With dependency
let user = use_resource(move || {
    let id = user_id();  // Re-runs when this changes
    async move { fetch_user(id).await }
});
```

## Routing

```rust
#[derive(Routable, Clone, PartialEq)]
enum Route {
    #[layout(NavBar)]
        #[route("/")]
        Home {},
        #[route("/blog/:id")]
        BlogPost { id: i32 },
}

#[component]
fn NavBar() -> Element {
    rsx! {
        nav { a { href: "/", "Home" } }
        Outlet::<Route> {}
    }
}

#[component]
fn App() -> Element {
    rsx! { Router::<Route> {} }
}
```

## Events

```rust
rsx! {
    button { onclick: move |_| { /* click */ }, "Click" }

    input {
        oninput: move |e| set_value(e.value()),
        prop:value: value,
    }

    input { onkeydown: move |e| {
        if e.key() == Key::Enter { /* enter pressed */ }
    }}

    form { onsubmit: move |e| {
        e.prevent_default();
        // submit
    }}
}
```

## Desktop Config (Dioxus.toml)

```toml
[desktop.window]
title = "MyApp"
width = 1200
height = 800
```

## Commands

```bash
curl -sSL http://dioxus.dev/install.sh | sh  # Install dx CLI
dx serve        # Dev server
dx build --release
dx bundle --release  # Create .deb etc.
```

## Dioxus vs Leptos

| Item | Dioxus 0.7 | Leptos 0.8 |
|------|------------|------------|
| Signal | `use_signal` (Copy-like) | `signal()` (may need clone) |
| Macro | `rsx! {}` | `view! {}` |
| Desktop | Native support | Needs Tauri |
