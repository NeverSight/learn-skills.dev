---
name: fivem-dui-optimization
description: Optimization techniques for DUI to minimize VRAM usage and CPU overhead.
---

# DUI Optimization Best Practices

### 1. JS vs. Lua Performance Gap
- **Benchmark**: NUI/DUI callbacks in **JavaScript are up to 9x slower** than in Lua when handling heavy data (e.g., base64 encoded images).
- **Guideline**: Use **Lua** for high-frequency data handling or critical interaction logic. Reserve JS for browser-side UI logic.

### 2. Proximity-Based Lifecycle
- Only initialize and render DUI objects when the player is nearby.
- **Tip**: Use the Lua distance-squared operator (`# (vectorA - vectorB)`) for distance checks—it is significantly faster than `GetDistanceBetweenCoords`.

### 3. Resource Cleanup
- **Critical**: Orphaned DUI instances continue to consume CPU cycles and VRAM even if not visible.
- **Procedure**: On resource stop, set the URL to `about:blank` first to terminate media decoders/JS loops, then call `DESTROY_DUI`.

### 4. Resolution and Refresh Rates
- Use the **minimum required resolution** for small objects (keypads, ATMs) to save VRAM.
- For background displays, decouple updates from the game's frame rate by using timers to refresh at 15–30 FPS instead of every frame.
- If content is static, prefer `CREATE_RUNTIME_TEXTURE_FROM_IMAGE` or a `.ytd` file over a live browser.