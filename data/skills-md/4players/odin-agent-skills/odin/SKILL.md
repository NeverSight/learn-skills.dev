---
name: odin
description: "ODIN platform by 4Players - real-time voice chat SDKs, game server hosting, and video conferencing. Use when: building applications with voice chat (Unity, Unreal, Web, Swift, Node.js, C/C++), deploying game servers with ODIN Fleet, or integrating video conferencing with ODIN Rooms."
license: MIT
---

# ODIN Platform

ODIN is a real-time communication and game server infrastructure platform by 4Players. It provides voice chat SDKs for all major platforms, game server hosting, and browser-based video conferencing.

## Quick Reference

Use this guide to find the right reference for your task:

| Task | Reference |
|------|-----------|
| Unity voice chat | [references/voice-unity.md](references/voice-unity.md) |
| Unreal Engine voice chat | [references/voice-unreal.md](references/voice-unreal.md) |
| Web/browser voice chat | [references/voice-web.md](references/voice-web.md) |
| iOS/macOS voice chat | [references/voice-swift.md](references/voice-swift.md) |
| Node.js server-side voice | [references/voice-nodejs.md](references/voice-nodejs.md) |
| C/C++ native SDK | [references/voice-core.md](references/voice-core.md) |
| Game server deployment | [references/fleet.md](references/fleet.md) |
| Fleet CLI tool | [references/fleet-cli.md](references/fleet-cli.md) |
| Video conferencing rooms | [references/rooms.md](references/rooms.md) |
| Platform concepts & auth | [references/fundamentals.md](references/fundamentals.md) |
| Pricing details | [references/pricing.md](references/pricing.md) |

---

## ODIN Voice

Cross-platform real-time voice chat SDK for games and applications.

**Key Features:** 3D spatial audio, noise suppression, echo cancellation, low latency, cross-platform (mobile, web, desktop in same room), data channels for custom game data.

> **Version Note:** ODIN Voice 1.x and 2.x are **not interoperable**. All participants in a room must use the same major version.

### Unity SDK

Real-time voice chat for Unity games and XR experiences. Supports v1.x (stable, Unity 2019.4+) and v2.x (beta, Unity 2021.4+).

- **Reference**: [references/voice-unity.md](references/voice-unity.md)
- **v1.x docs**: [references/voice-unity-v1.md](references/voice-unity-v1.md)
- **v2.x docs**: [references/voice-unity-v2.md](references/voice-unity-v2.md)
- **Troubleshooting**: [references/voice-unity-troubleshooting.md](references/voice-unity-troubleshooting.md)

### Unreal Engine SDK

Voice chat plugin for Unreal Engine. Supports v1.x (UE 4.26+) and v2.x (UE 5.3+).

- **Reference**: [references/voice-unreal.md](references/voice-unreal.md)
- **v1.x docs**: [references/voice-unreal-v1.md](references/voice-unreal-v1.md)
- **v2.x docs**: [references/voice-unreal-v2.md](references/voice-unreal-v2.md)
- **Troubleshooting**: [references/voice-unreal-troubleshooting.md](references/voice-unreal-troubleshooting.md)

### Web/JavaScript SDK

Browser SDK for real-time voice chat with WebTransport/HTTP3. Supports NPM and CDN.

- **Reference**: [references/voice-web.md](references/voice-web.md)
- **Advanced patterns**: [references/voice-web-advanced.md](references/voice-web-advanced.md)
- **Audio processing**: [references/voice-web-audio-processing.md](references/voice-web-audio-processing.md)
- **Framework integration** (React, Vue, Angular): [references/voice-web-frameworks.md](references/voice-web-frameworks.md)

### Swift SDK (OdinKit)

Voice chat for iOS and macOS apps. Requires iOS 9+/macOS 10.15+, Swift 5.0+.

- **Reference**: [references/voice-swift.md](references/voice-swift.md)

### Node.js SDK

Server-side voice chat with native C++ bindings. For recording bots, AI voice assistants, server-side audio processing, and content moderation.

- **Reference**: [references/voice-nodejs.md](references/voice-nodejs.md)
- **Audio patterns**: [references/voice-nodejs-audio.md](references/voice-nodejs-audio.md)

### Core SDK (C/C++)

Low-level C API foundation for all ODIN Voice SDKs. For custom platform integrations or language bindings.

- **Reference**: [references/voice-core.md](references/voice-core.md)
- **v1.x docs**: [references/voice-core-v1.md](references/voice-core-v1.md)
- **v2.x docs**: [references/voice-core-v2.md](references/voice-core-v2.md)

---

## ODIN Fleet

Game server hosting and deployment platform with global infrastructure.

**Key Features:** Engine-agnostic architecture, automatic scaling, Docker and Steamworks image support, REST API and CLI for deployment automation, dashboard for monitoring/logging/backups.

- **Reference**: [references/fleet.md](references/fleet.md)
- **Deployment patterns**: [references/fleet-deployment.md](references/fleet-deployment.md)
- **Matchmaking**: [references/fleet-matchmaking.md](references/fleet-matchmaking.md)

### Fleet CLI

Command-line tool for managing Fleet resources. Supports automation, CI/CD pipelines, and scripted deployments.

- **Reference**: [references/fleet-cli.md](references/fleet-cli.md)
- **Advanced patterns**: [references/fleet-cli-advanced.md](references/fleet-cli-advanced.md)
- **CI/CD integration**: [references/fleet-cli-cicd.md](references/fleet-cli-cicd.md)

---

## ODIN Rooms

Browser-based, decentralized video conferencing with end-to-end encryption. GDPR compliant.

**Key Features:** Audio/video calls, text chat, screen sharing, whiteboard, custom branding, self-hosted or cloud-hosted.

- **Reference**: [references/rooms.md](references/rooms.md)

---

## Platform Fundamentals

Core concepts, authentication, pricing, and architecture that apply across all ODIN products.

- **Fundamentals**: [references/fundamentals.md](references/fundamentals.md)
- **Integration patterns**: [references/integration-patterns.md](references/integration-patterns.md)
- **Pricing details**: [references/pricing.md](references/pricing.md)

### Authentication

ODIN uses a two-level authentication system:

1. **Access Key** — API credential for generating tokens (server-side only, never expose to clients)
2. **Room Token** — JWT signed with Ed25519, used by clients to join rooms

> **CRITICAL**: Never embed access keys in client code in production. Generate room tokens on a server.

### Core Concepts

- **Rooms** — Virtual spaces where peers communicate
- **Peers** — Participants in a room, each with a unique peer ID
- **Media Streams** — Audio channels (microphone input/output)
- **Data Channels** — Custom binary/text data between peers

## Documentation

- **Main Docs**: https://docs.4players.io/
- **Voice SDK**: https://docs.4players.io/voice/
- **Fleet**: https://docs.4players.io/fleet/
- **Rooms**: https://docs.4players.io/rooms/
- **Discord**: https://4np.de/discord
