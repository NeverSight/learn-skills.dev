---
name: spritekit-ios
description: |
  SpriteKit 2D game development for iOS and visionOS. Use when building games with scenes, sprites, physics, tile maps, or particle systems using Apple's SpriteKit framework.
---

# SpriteKit iOS Game Development

## Scene Graph & Coordinate System

- **Y-up** coordinate system — origin (0,0) at bottom-left by default
- `SKScene.anchorPoint` defaults to (0.5, 0.5) — center of screen
- `zPosition` controls draw order — higher = in front; siblings draw in add order if equal
- Every node inherits parent's transform — build hierarchy intentionally

```swift
class GameScene: SKScene {
    override func didMove(to view: SKView) {
        backgroundColor = .black
        scaleMode = .resizeFill   // or .aspectFit for fixed-resolution games
    }
}
```

## Physics

```swift
// Dynamic body (moves with physics)
let sprite = SKSpriteNode(imageNamed: "player")
sprite.physicsBody = SKPhysicsBody(circleOfRadius: sprite.size.width / 2)
sprite.physicsBody?.categoryBitMask    = PhysicsCategory.player   // what am I
sprite.physicsBody?.contactTestBitMask = PhysicsCategory.enemy    // notify on contact
sprite.physicsBody?.collisionBitMask   = PhysicsCategory.wall     // physically bounce off

// Static body (immovable)
let wall = SKSpriteNode(color: .white, size: CGSize(width: 10, height: 300))
wall.physicsBody = SKPhysicsBody(rectangleOf: wall.size)
wall.physicsBody?.isDynamic = false

// Category constants — UInt32, max 32 unique categories (bits 0–31)
struct PhysicsCategory {
    static let none:   UInt32 = 0
    static let player: UInt32 = 0b0001   // 1
    static let enemy:  UInt32 = 0b0010   // 2
    static let wall:   UInt32 = 0b0100   // 4
    // Never exceed bit 31 — UInt32 overflow will crash
}

// Contact delegate
class GameScene: SKScene, SKPhysicsContactDelegate {
    override func didMove(to view: SKView) {
        physicsWorld.contactDelegate = self
    }
    func didBegin(_ contact: SKPhysicsContact) {
        // Order of bodyA/bodyB is not guaranteed — always sort
        let maskA = contact.bodyA.categoryBitMask
        let maskB = contact.bodyB.categoryBitMask
        if (maskA | maskB) == (PhysicsCategory.player | PhysicsCategory.enemy) {
            handlePlayerEnemyContact(contact)
        }
    }
}
```

## Actions

```swift
// Sequence — runs in order
let seq = SKAction.sequence([
    SKAction.move(to: target, duration: 0.3),
    SKAction.run { self.spawnEffect() },
    SKAction.removeFromParent()
])

// Group — runs simultaneously
let combo = SKAction.group([
    SKAction.scale(to: 1.5, duration: 0.2),
    SKAction.fadeOut(withDuration: 0.2)
])

// Repeat forever
sprite.run(SKAction.repeatForever(
    SKAction.rotate(byAngle: .pi * 2, duration: 1.0)
))

// Custom timing
let eased = SKAction.move(by: CGVector(dx: 100, dy: 0), duration: 0.5)
eased.timingMode = .easeInEaseOut
```

## Texture Atlases & Animation

```swift
// Add a MyCharacter.atlas folder to your Xcode target with numbered frames
let atlas = SKTextureAtlas(named: "MyCharacter")
let frames = (1...8).map { atlas.textureNamed("run_\($0)") }

let anim = SKAction.animate(with: frames, timePerFrame: 0.08, resize: false, restore: true)
sprite.run(SKAction.repeatForever(anim))
```

Atlases batch all sprites into one draw call — **always use them** for animated sprites in production.

## SKTileMapNode

```swift
// Usually configured in the Xcode scene editor; access in code:
if let tileMap = childNode(withName: "Ground") as? SKTileMapNode {
    // Read tile at position
    let col = tileMap.tileColumnIndex(fromPosition: point)
    let row = tileMap.tileRowIndex(fromPosition: point)
    let def = tileMap.tileDefinition(atColumn: col, row: row)
    let isWall = def?.userData?["solid"] as? Bool ?? false
}
```

## Game Loop — What Goes Where

| Method | Use for |
|---|---|
| `update(_ currentTime:)` | Input handling, AI decisions, manual velocity changes |
| `didEvaluateActions()` | State checks after actions complete (e.g., did animation finish?) |
| `didSimulatePhysics()` | Camera follow, enforcing constraints after physics step |

## Performance

- **Node count targets:** < 500 for 60 fps on older devices; < 1500 on modern hardware
- **Debug overlay:** `view.showsFPS = true; view.showsNodeCount = true; view.showsDrawCount = true`
- Prefer `SKSpriteNode` over `SKShapeNode` — shape nodes regenerate geometry every frame
- Avoid `SKEffectNode` unless you need blur/filters — triggers expensive offscreen render pass
- Pool and reuse frequently spawned nodes (bullets, particles) instead of add/remove

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| `presentScene` crash | Must be called on main thread |
| Physics bitmask > bit 31 | UInt32 overflow → crash; cap at 32 categories |
| `removeFromParent()` off main thread | All node graph operations: main thread only |
| Memory leak on scene transition | Nil out delegate refs; use `view.presentScene(_:transition:)` |
| anchorPoint confusion | Set explicitly; docs show (0,0) examples but default SKScene is (0.5, 0.5) |
| Contact firing twice | Both `didBegin` and `didEnd` fire per pair — guard with a "contacted" flag if needed |
