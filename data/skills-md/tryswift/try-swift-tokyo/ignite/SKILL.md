---
name: ignite
description: Guidelines for building static sites using the Ignite Swift framework.
---

# Ignite Framework Guidelines

You are an expert in using Ignite, the Swift static site generator.

## 1. DSL Usage

- Use the result builder syntax for HTML generation (`Body`, `Head`, `Div`, `Section`).
- Prefer Ignite's built-in components (`Text`, `Image`, `Link`) over raw HTML strings.
- Use `.style(...)` modifiers for CSS styling rather than inline strings where possible.

## 2. Components

- Break complex UI into reusable `Component` structs.
- Components must implement `var body: some HTML`.

## 3. Themes & Layouts

- Define a `MainTheme` implementing `Theme`.
- Use `Page` protocol for content pages.

## Example

```swift
struct MyPage: Page {
    var title = "Home"

    func body(context: PublishingContext) -> [any HTML] {
        Text("Welcome to my site")
            .font(.title1)
            .margin(.top, 20)

        Section {
            Text("Content goes here")
        }
        .class("container")
    }
}
