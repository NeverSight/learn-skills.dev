---
name: gamekit-multiplayer
description: |
  GameKit real-time and turn-based multiplayer for iOS and visionOS. Use when implementing GKMatch matchmaking, GKLocalPlayer authentication, real-time data sync, or turn-based game logic using Apple's Game Center infrastructure.
---

# GameKit Multiplayer

## Authentication First — Always

Nothing in GameKit works until `GKLocalPlayer` is authenticated. Call this at app launch, before any matchmaking UI:

```swift
import GameKit

func authenticateLocalPlayer() {
    GKLocalPlayer.local.authenticateHandler = { [weak self] viewController, error in
        if let vc = viewController {
            // Present Game Center login UI
            self?.present(vc, animated: true)
        } else if GKLocalPlayer.local.isAuthenticated {
            self?.enableMultiplayerUI()
        } else {
            // Player declined or unavailable — disable multiplayer
            print("GameKit auth failed: \(error?.localizedDescription ?? "unknown")")
        }
    }
}
```

**Common pitfall:** calling `findMatch` before auth completes → silent failure, no error callback.

## GKMatchmaker vs GKMatchmakerViewController

| | GKMatchmaker | GKMatchmakerViewController |
|---|---|---|
| UI | Your own custom UI | Apple's built-in Game Center UI |
| Use when | Full control, invite-only flows | Quick integration |

```swift
// Programmatic (custom UI)
let request = GKMatchRequest()
request.minPlayers = 2
request.maxPlayers = 4

GKMatchmaker.shared().findMatch(for: request) { match, error in
    guard let match, error == nil else { return }
    DispatchQueue.main.async { self.startGame(with: match) }
}

// Built-in Game Center UI
let vc = GKMatchmakerViewController(matchRequest: request)
vc?.matchmakerDelegate = self
present(vc!, animated: true)
```

## Real-time vs Turn-based

**GKMatch (real-time):**
- All players online simultaneously
- Low-latency continuous sync (positions, inputs)
- Action games, racing, shooters

**GKTurnBasedMatch:**
- Players take turns asynchronously (may be hours apart)
- Apple persists game state on their servers
- Strategy games, board games, word games

## Sending & Receiving Data (Real-time)

```swift
// Encode messages with Codable
struct GameMessage: Codable {
    enum Kind: String, Codable { case move, shoot, stateSync }
    let kind: Kind
    let payload: Data
}

func send(_ message: GameMessage, reliable: Bool = true) throws {
    let data = try JSONEncoder().encode(message)
    try match.sendData(toAllPlayers: data, with: reliable ? .reliable : .unreliable)
}
// .reliable   → guaranteed, ordered (use for game state changes)
// .unreliable → fast, may drop (use for position streaming)

// GKMatchDelegate — always dispatch UI work to main thread
func match(_ match: GKMatch, didReceive data: Data, fromRemotePlayer player: GKPlayer) {
    guard let message = try? JSONDecoder().decode(GameMessage.self, from: data) else { return }
    DispatchQueue.main.async { self.apply(message, from: player) }
}
```

## Player Connect / Disconnect

```swift
func match(_ match: GKMatch, player: GKPlayer, didChange state: GKPlayerConnectionState) {
    switch state {
    case .connected:
        // Wait until ALL expected players are connected
        if match.expectedPlayerCount == 0 { startGame() }
    case .disconnected:
        pauseGame()
        // Optionally: GKMatchmaker.shared().addPlayers(to: match, ...) to fill slot
    @unknown default: break
    }
}
```

`match.expectedPlayerCount` starts at (minPlayers - 1) and decrements as players join. Start the game only when it reaches 0.

## Sandbox vs Production

- Test accounts: create sandbox Apple IDs in App Store Connect → Users and Access → Sandbox
- Sandbox and production Game Center are **completely separate** — leaderboards, matches, and friends don't cross
- Enable on device: Settings → Developer → Enable Sandbox Game Center (Xcode scheme also works)
- Always test with two sandbox accounts to catch auth edge cases

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Matchmaking before auth | Set `authenticateHandler` at launch; wait for isAuthenticated callback |
| UI updates in delegate | Wrap all UI in `DispatchQueue.main.async` |
| Starting too early | Wait for `match.expectedPlayerCount == 0` |
| Match object deallocated | Keep strong `var match: GKMatch?` reference |
| `didFailWithError` not implemented | Network errors only surface here — implement it |
| Turn-based state lost | Call `match.saveCurrentTurn(withMatch:completionHandler:)` before ending turn |
