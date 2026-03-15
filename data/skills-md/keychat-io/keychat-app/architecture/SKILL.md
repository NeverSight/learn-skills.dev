---
name: architecture
description: Explains the Keychat app architecture and key components
user-invocable: true
disable-model-invocation: false
---

Keychat is a secure messaging app with a unique architecture. When explaining or working with the codebase, understand these key components:

## Core Technologies

| Technology | Purpose | Implementation |
|------------|---------|----------------|
| **Nostr Protocol** | Message delivery/storage | `lib/nostr-core/`, WebSocket connections |
| **Signal Protocol** | 1:1 E2E encryption | `api_signal.rs` via FFI |
| **MLS Protocol** | Group E2E encryption | `api_mls.rs` via FFI |
| **Bitcoin Ecash** | Micropayments to relays | `api_cashu.rs`, `keychat_ecash/` |

## Package Structure

```
packages/
├── app/                    # Main Flutter app
├── keychat_ecash/          # Ecash wallet functionality
└── keychat_rust_ffi_plugin/ # Native crypto via Rust
```

## Key Services (packages/app/lib/service/)

- **signal_chat.service.dart** - Signal protocol session management
- **mls_group.service.dart** - MLS group key operations
- **websocket.service.dart** - Nostr relay connections
- **chat.service.dart** - High-level message routing
- **relay.service.dart** - Relay management
- **identity.service.dart** - User identity management

## State Management

Uses **GetX** pattern:
- Controllers in `lib/controller/`
- Services are singleton instances
- Reactive state with `.obs` observables

## Database

Uses **Isar** (NoSQL for Flutter):
- Models in `lib/models/`
- Models use `@collection` annotation
- Generated code via build_runner (*.g.dart, *.isar.dart)

## Rust FFI Bridge

Native crypto operations use flutter_rust_bridge:
- Rust code: `packages/keychat_rust_ffi_plugin/rust/src/`
- Generated Dart bindings: `packages/keychat_rust_ffi_plugin/lib/`
- Key APIs: Cashu, Nostr, Signal, MLS

## Message Flow

1. User composes message
2. Signal/MLS encrypts content
3. Message wrapped in Nostr event
4. Ecash stamp attached (if relay requires payment)
5. Sent via WebSocket to Nostr relay
6. Recipient receives, decrypts, displays
