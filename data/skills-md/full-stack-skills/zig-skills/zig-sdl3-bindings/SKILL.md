---
name: zig-sdl3-bindings
license: Apache-2.0
description: Zig bindings for SDL3 multimedia library. Use for cross-platform game development, graphics, audio, input handling. Covers windowing, rendering, GPU compute, events, gamepads, audio streams, networking. Emphasizes Zig-specific patterns like error handling with try/catch, defer for cleanup, custom allocator integration, callback wrappers, and fromSdl/toSdl type conversions.
---

# Zig SDL3 Bindings Reference

> This skill covers Zig bindings for the SDL3 multimedia library. Use for cross-platform game development, graphics, audio, and input handling.

## Capability Boundaries

### ✅ Strong Suits
1. Cross-platform window management and event handling
2. 2D/3D rendering and GPU compute
3. Audio streams and gamepad input
4. File system and networking
5. Zig-specific binding patterns (try/catch, defer, allocator integration)

### ⚠️ Requirements
1. Requires SDL3 native library (installed via system package manager or compiled)
2. Requires zig-sdl3 dependency

### ❌ Out of Scope (with alternatives)
1. Do not use this for raylib game development → use zig-raylib skill instead
2. Do not use this for Zig language basics → use zig-0.16 skill instead
3. Do not use this for other language SDL3 development → use the corresponding language skill

## When to use

Use this skill when the user needs to write cross-platform games/multimedia applications, handling windows, rendering, audio, or input.

## Data Privacy

This skill does not collect, store, or transmit any user data.

# Zig SDL3 Bindings Reference

## Quick Start

**Example invocations:**
```
Create an SDL3 + Zig window
Handle keyboard events in SDL3
How to use zig-sdl3 GPU rendering
Play audio with SDL3
```

## Workflow

Step 1. **Configure dependencies** — Add zig-sdl3 to build.zig.zon, install SDL3 native library
Step 2. **Initialize SDL3** — Call sdl3.init() to initialize subsystems
Step 3. **Create window** — Use sdl3.Window.create to create the main window
Step 4. **Event loop** — Process events in a while (sdl3.pollEvent()) loop
Step 5. **Render** — Use SDL3 renderer or GPU API for drawing
Step 6. **Clean exit** — Use defer to clean up windows and SDL subsystems

Idiomatic Zig bindings for SDL3, wrapping the C API with Zig patterns: error unions, optionals, slices, and defer-based resource management.

**Version:** 0.1.7+ (SDL 3.4.0+)

## Critical: Build Configuration

### build.zig.zon Dependency

```zig
.dependencies = .{
    .sdl3 = .{
        .url = "git+https://codeberg.org/7Games/zig-sdl3#main",
        .hash = "...",  // Get from build error on first run
    },
},
```

### build.zig Setup

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // Get the SDL3 dependency
    const sdl3_dep = b.dependency("sdl3", .{
        .target = target,
        .optimize = optimize,
        // Build options:
        // .callbacks = true,      // Enable SDL main callbacks pattern
        // .main = true,           // Enable SDL_main
        // .ext_image = true,      // Enable SDL_image extension
        // .ext_ttf = true,        // Enable SDL_ttf extension
        // .ext_net = true,        // Enable SDL_net extension
    });

    const exe = b.addExecutable(.{
        .name = "my-game",
        .root_module = b.createModule(.{
            .root_source_file = b.path("src/main.zig"),
            .target = target,
            .optimize = optimize,
        }),
    });

    // Add SDL3 module and link
    exe.root_module.addImport("sdl3", sdl3_dep.module("sdl3"));

    b.installArtifact(exe);
}
```

### Import in Code

```zig
const sdl3 = @import("sdl3");
```

## Critical: Two Application Patterns

### Pattern 1: Traditional Main Loop (Recommended for most apps)

```zig
const sdl3 = @import("sdl3");

pub fn main() !void {
    // ALWAYS call shutdown at end, even on error
    defer sdl3.shutdown();

    // Initialize subsystems
    const init_flags = sdl3.InitFlags{ .video = true, .audio = true };
    try sdl3.init(init_flags);
    defer sdl3.quit(init_flags);

    // Create window
    const window = try sdl3.video.Window.init("My Game", 800, 600, .{});
    defer window.deinit();

    // Optional: Create renderer for 2D graphics
    const renderer = try sdl3.render.Renderer.init(window, null);
    defer renderer.deinit();

    // FPS limiter (provided by zig-sdl3)
    var fps_capper = sdl3.extras.FramerateCapper(f32){ .mode = .{ .limited = 60 } };

    var running = true;
    while (running) {
        const dt = fps_capper.delay();  // Delta time in seconds

        // Event handling
        while (sdl3.events.poll()) |event| {
            switch (event) {
                .quit, .terminating => running = false,
                .key_down => |key| {
                    if (key.scancode == .escape) running = false;
                },
                else => {},
            }
        }

        // Update game state using dt...

        // Render
        try renderer.setDrawColor(.{ .r = 0, .g = 0, .b = 0, .a = 255 });
        try renderer.clear();
        // Draw game objects...
        try renderer.present();
    }
}
```

### Pattern 2: App Callbacks (Mobile-friendly, required for some platforms)

Enable with `-Dcallbacks=true` build option:

```zig
const sdl3 = @import("sdl3");
const std = @import("std");

const allocator = std.heap.smp_allocator;

const AppState = struct {
    window: sdl3.video.Window,
    renderer: sdl3.render.Renderer,
    fps_capper: sdl3.extras.FramerateCapper(f32),
};

fn init(app_state: *?*AppState, args: [][*:0]u8) !sdl3.AppResult {
    _ = args;

    const window = try sdl3.video.Window.init("Callback App", 800, 600, .{});
    errdefer window.deinit();

    const renderer = try sdl3.render.Renderer.init(window, null);
    errdefer renderer.deinit();

    const state = try allocator.create(AppState);
    state.* = .{
        .window = window,
        .renderer = renderer,
        .fps_capper = .{ .mode = .{ .limited = 60 } },
    };
    app_state.* = state;

    return .run;  // Continue running
}

fn iterate(app_state: *AppState) !sdl3.AppResult {
    const dt = app_state.fps_capper.delay();
    _ = dt;

    try app_state.renderer.setDrawColor(.{ .r = 100, .g = 50, .b = 200, .a = 255 });
    try app_state.renderer.clear();
    try app_state.renderer.present();

    return .run;
}

fn event(app_state: *AppState, curr_event: sdl3.events.Event) !sdl3.AppResult {
    _ = app_state;
    return switch (curr_event) {
        .quit, .terminating => .success,  // Exit successfully
        else => .run,
    };
}

fn quit(app_state: ?*AppState, result: sdl3.AppResult) void {
    _ = result;
    if (app_state) |state| {
        state.renderer.deinit();
        state.window.deinit();
        allocator.destroy(state);
    }
}

pub fn main() u8 {
    sdl3.main_funcs.setMainReady();
    var args = [_:null]?[*:0]u8{ @constCast("My App") };
    return sdl3.main_funcs.enterAppMainCallbacks(&args, AppState, init, iterate, event, quit);
}
```

## Critical: Error Handling

All SDL functions that can fail return Zig error unions:

```zig
// Functions return !T (error union)
const window = try sdl3.video.Window.init("Title", 800, 600, .{});

// Get error message on failure
const window = sdl3.video.Window.init("Title", 800, 600, .{}) catch |err| {
    std.debug.print("SDL Error: {?s}\n", .{sdl3.errors.get()});
    return err;
};

// Optional: Set thread-local error callback for debugging
sdl3.errors.error_callback = struct {
    fn callback(err: ?[:0]const u8) void {
        std.debug.print("SDL Error: {?s}\n", .{err});
    }
}.callback;
```

### Common Error Type

```zig
pub const Error = error{
    SdlError,  // All SDL errors map to this
};
```

## Critical: Resource Management with Defer

Always use `defer` for cleanup:

```zig
pub fn main() !void {
    defer sdl3.shutdown();  // ALWAYS first

    try sdl3.init(.{ .video = true });
    defer sdl3.quit(.{ .video = true });

    const window = try sdl3.video.Window.init("Title", 800, 600, .{});
    defer window.deinit();

    const renderer = try sdl3.render.Renderer.init(window, null);
    defer renderer.deinit();

    const texture = try renderer.createTexture(.rgba8888, .streaming, 256, 256);
    defer texture.deinit();
}
```

## Critical: Type Conversions (fromSdl/toSdl)

The bindings convert between C and Zig types using consistent patterns:

```zig
// Enum conversions
const zig_theme: sdl3.video.SystemTheme = .dark;
const c_theme = zig_theme.toSdl();                           // Zig -> C
const back_to_zig = sdl3.video.SystemTheme.fromSdl(c_theme); // C -> Zig

// Struct conversions
const zig_rect = sdl3.rect.IRect{ .x = 10, .y = 20, .w = 100, .h = 50 };
const c_rect = zig_rect.toSdl();                       // Zig -> C
const back = sdl3.rect.IRect.fromSdl(c_rect);         // C -> Zig

// Flag struct conversions
const flags = sdl3.InitFlags{ .video = true, .audio = true };
const c_flags = flags.toSdl();                         // Zig -> C bitmask
const back_flags = sdl3.InitFlags.fromSdl(c_flags);    // C bitmask -> Zig

// Nullable conversions (C uses special values for "none")
const format: ?sdl3.pixels.Format = sdl3.pixels.Format.fromSdl(c_format);
const c_format = sdl3.pixels.Format.toSdl(format);  // null -> SDL_PIXELFORMAT_UNKNOWN
```

## Critical: Custom Allocator Integration

Use Zig allocators for SDL memory management:

```zig
const std = @import("std");
const sdl3 = @import("sdl3");

pub fn main() !void {
    // Set up allocator BEFORE any SDL calls
    var debug_allocator = std.heap.DebugAllocator(.{}).init;
    _ = try sdl3.setMemoryFunctionsByAllocator(debug_allocator.allocator());

    // Check for leaks at end
    defer if (debug_allocator.detectLeaks()) @panic("Memory leaks detected!");

    defer sdl3.shutdown();

    // ... rest of app
}
```

## Quick Reference: Initialization Flags

```zig
const sdl3 = @import("sdl3");

// Individual subsystems
try sdl3.init(.{ .video = true });              // Windowing
try sdl3.init(.{ .audio = true });              // Audio playback/recording
try sdl3.init(.{ .events = true });             // Event queue (auto-init by video/audio)
try sdl3.init(.{ .joystick = true });           // Raw joystick access
try sdl3.init(.{ .gamepad = true });            // Controller with standard layout
try sdl3.init(.{ .haptic = true });             // Force feedback
try sdl3.init(.{ .sensor = true });             // Accelerometer, gyro
try sdl3.init(.{ .camera = true });             // Webcam access

// Everything at once
try sdl3.init(sdl3.InitFlags.everything);

// Clean shutdown
defer sdl3.quit(.{ .video = true, .audio = true });  // Quit specific
defer sdl3.shutdown();                                // Quit everything
```

## Quick Reference: Window Creation

```zig
const sdl3 = @import("sdl3");

// Basic window
const window = try sdl3.video.Window.init("Title", 800, 600, .{});
defer window.deinit();

// Window with flags
const window = try sdl3.video.Window.init("Fullscreen", 1920, 1080, .{
    .fullscreen = true,
    .high_pixel_density = true,
});

// Common window flags
.{
    .fullscreen = true,           // Fullscreen exclusive
    .borderless = true,           // No window decorations
    .resizable = true,            // User can resize
    .minimized = true,            // Start minimized
    .maximized = true,            // Start maximized
    .high_pixel_density = true,   // HiDPI support
    .always_on_top = true,        // Stay above other windows
    .hidden = true,               // Create hidden
    .open_gl = true,               // OpenGL context
    .vulkan = true,               // Vulkan surface
    .metal = true,                // Metal layer
}

// Window operations
try window.setTitle("New Title");
try window.setSize(1024, 768);
try window.setPosition(.{ .absolute = 100 }, .{ .absolute = 100 });
try window.show();
try window.hide();
try window.setFullscreen(true);
```

## Quick Reference: 2D Rendering

```zig
const sdl3 = @import("sdl3");

// Create renderer
const renderer = try sdl3.render.Renderer.init(window, null);
defer renderer.deinit();

// Clear screen
try renderer.setDrawColor(.{ .r = 0, .g = 0, .b = 0, .a = 255 });
try renderer.clear();

// Draw filled rectangle
try renderer.setDrawColor(.{ .r = 255, .g = 0, .b = 0, .a = 255 });
try renderer.renderFillRect(.{ .x = 100, .y = 100, .w = 200, .h = 150 });

// Draw outline
try renderer.renderRect(.{ .x = 50, .y = 50, .w = 100, .h = 100 });

// Draw line
try renderer.renderLine(.{ .x = 0, .y = 0 }, .{ .x = 800, .y = 600 });

// Draw point
try renderer.renderPoint(.{ .x = 400, .y = 300 });

// Load and draw texture
const surface = try sdl3.image.loadFile("sprite.png");  // Requires ext_image
defer surface.deinit();
const texture = try renderer.createTextureFromSurface(surface);
defer texture.deinit();

try renderer.renderTexture(texture, null, .{ .x = 100, .y = 100, .w = 64, .h = 64 });

// Present frame
try renderer.present();
```

## Quick Reference: Event Handling

```zig
const sdl3 = @import("sdl3");

// Poll events
while (sdl3.events.poll()) |event| {
    switch (event) {
        // Application events
        .quit => break,                    // Window close, Alt+F4
        .terminating => break,             // OS killing app
        .low_memory => freeCache(),        // Memory pressure

        // Keyboard
        .key_down => |k| {
            if (k.scancode == .escape) break;
            if (k.key == .space and !k.repeat) jump();
        },
        .key_up => |k| handleKeyUp(k.scancode),
        .text_input => |t| appendText(t.text),

        // Mouse
        .mouse_motion => |m| updateCursor(m.x, m.y),
        .mouse_button_down => |m| {
            if (m.button == .left) onClick(m.x, m.y);
        },
        .mouse_wheel => |w| scroll(w.scroll_y),

        // Gamepad
        .gamepad_button_down => |g| {
            if (g.button == .south) jump();  // A/Cross button
        },
        .gamepad_axis_motion => |g| {
            if (g.axis == .left_x) moveHorizontal(g.value);
        },

        // Window events
        .window_resized => |w| resize(w.width, w.height),
        .window_focus_gained => resumeGame(),
        .window_focus_lost => pauseGame(),

        else => {},
    }
}

// Wait for events (blocks thread)
if (sdl3.events.wait()) |event| {
    // Handle event
}

// Wait with timeout
if (sdl3.events.waitTimeout(1000)) |event| {
    // Handle event
}
```

## Quick Reference: Audio Playback

```zig
const sdl3 = @import("sdl3");

// Load WAV file (returns tuple: Spec + data)
const spec, const audio_buf = try sdl3.audio.loadWav("sound.wav");
defer sdl3.free(audio_buf.ptr);

// Open audio device
const device = try sdl3.audio.Device.default_playback.open(spec);
defer device.close();

// Create stream and bind to device
const stream = try sdl3.audio.Stream.init(spec, spec);
defer stream.deinit();
try device.bindStream(stream);

// Queue audio data
try stream.putData(audio_buf);

// Resume playback (devices start paused)
try device.resumePlayback();
```

## Module Reference

### Core
- **[Getting Started](references/getting-started.md)** - Build setup, project template, dependencies
- **[Init & Lifecycle](references/init-lifecycle.md)** - Initialization, main loop vs callbacks, shutdown
- **[Video & Windows](references/video-windows.md)** - Window creation, displays, surfaces, pixels
- **[Render](references/render.md)** - 2D renderer, textures, drawing primitives
- **[GPU](references/gpu.md)** - Modern GPU API (3D, compute, shaders)
- **[Events](references/events.md)** - Event handling, polling, filtering

### Input
- **[Keyboard](references/keyboard.md)** - Keyboard input, keycodes, scancodes
- **[Mouse](references/mouse.md)** - Mouse input, cursors, relative mode
- **[Gamepad & Joystick](references/gamepad-joystick.md)** - Controllers, haptics, sensors
- **[Touch & Pen](references/touch-pen.md)** - Touch screens, stylus input

### Media
- **[Audio](references/audio.md)** - Audio streams, playback, recording, WAV
- **[Image](references/image.md)** - Image loading (SDL_image extension)
- **[TTF](references/ttf.md)** - Font rendering (SDL_ttf extension)
- **[Camera](references/camera.md)** - Video capture, webcams

### System
- **[Filesystem & I/O](references/filesystem-io.md)** - File I/O, paths, directories, async I/O
- **[Storage](references/storage.md)** - Platform storage, cloud saves
- **[Clipboard](references/clipboard.md)** - Clipboard operations
- **[Networking](references/net.md)** - TCP/UDP (SDL_net extension)
- **[System & Platform](references/system-platform.md)** - Platform detection, CPU info, locale
- **[Threading](references/threading.md)** - Threads, mutexes, atomics

### Configuration
- **[Properties & Hints](references/properties-hints.md)** - Configuration hints, property bags
- **[Log & Errors](references/log-errors.md)** - Logging, error handling patterns
- **[Dialogs & UI](references/dialogs-ui.md)** - Message boxes, file dialogs, tray icons

### Patterns
- **[Binding Patterns](references/binding-patterns.md)** - fromSdl/toSdl, callback wrappers, C interop
- **[Allocator Integration](references/allocator-integration.md)** - Custom Zig allocators with SDL

## Common Type Mappings

| SDL3 C Type | zig-sdl3 Type |
|-------------|---------------|
| `SDL_Window*` | `sdl3.video.Window` |
| `SDL_Renderer*` | `sdl3.render.Renderer` |
| `SDL_Texture*` | `sdl3.render.Texture` |
| `SDL_Surface*` | `sdl3.surface.Surface` |
| `SDL_Event` | `sdl3.events.Event` (tagged union) |
| `SDL_Rect` | `sdl3.rect.IRect` |
| `SDL_FRect` | `sdl3.rect.FRect` |
| `SDL_Point` | `sdl3.rect.IPoint` |
| `SDL_FPoint` | `sdl3.rect.FPoint` |
| `SDL_Color` | `sdl3.pixels.Color` |
| `SDL_Keycode` | `sdl3.keycode.Keycode` |
| `SDL_Scancode` | `sdl3.Scancode` |
| `SDL_AudioDeviceID` | `sdl3.audio.Device` |
| `SDL_AudioStream*` | `sdl3.audio.Stream` |
| `SDL_GPUDevice*` | `sdl3.gpu.Device` |
| `SDL_Gamepad*` | `sdl3.gamepad.Gamepad` |
| `SDL_Joystick*` | `sdl3.joystick.Joystick` |
| `SDL_PropertiesID` | `sdl3.properties.Group` |

## Platform Support

zig-sdl3 supports all SDL3 platforms:
- Windows (x86_64, ARM64)
- macOS (x86_64, ARM64)
- Linux (x86_64, ARM64)
- iOS
- Android
- Emscripten (WebAssembly)

Cross-compilation works via Zig's cross-compilation:
```bash
zig build -Dtarget=x86_64-windows
zig build -Dtarget=aarch64-macos
zig build -Dtarget=wasm32-emscripten
```

## Version Compatibility

| zig-sdl3 | SDL3 | Zig |
|----------|------|-----|
| 0.1.7+ | 3.4.0+ | 0.15.1+ |
| 0.1.0-0.1.6 | 3.2.0+ | 0.14.0+ |

## Raw C Access

For functions not yet wrapped:

```zig
const sdl3 = @import("sdl3");
const c = sdl3.c;  // Raw SDL3 C API

// Use C functions directly
const result = c.SDL_SomeUnwrappedFunction();
```

## Audience

| User Type | Usage |
|-----------|-------|
| **Cross-platform app developers** | Create multimedia applications with SDL3 |
| **Game developers** | Use SDL3 low-level graphics/audio/input |
| **Embedded developers** | Use SDL3's multi-platform abstraction layer |

Customization:
- Specify SDL3 subsystems (video/audio/gamepad/net etc.)
- Specify rendering mode (software / GPU)

## Gotchas

1. **SDL3 native library dependency** — zig-sdl3 depends on the system-installed SDL3 native library (`libSDL3`), not a pure Zig implementation. Use `verify` to check if the library is installed.
2. **build.zig.zon hash** — Dependency hash must be obtained from the compiler's first build error
3. **Extension libraries are optional** — SDL_image, SDL_ttf, SDL_net etc. must be enabled via build options
4. **Defer cleanup** — Windows, renderers, textures must be cleaned up with defer. Use a validation checklist to confirm all resources are released.
5. **Event loop mode** — SDL3 supports both traditional polling and main callback modes. Pick one and stay consistent.

## FAQ

**Q: Do I need to install the SDL3 native library?**
A: Yes. Install the SDL3 development library (e.g. Ubuntu: `libsdl3-dev`, macOS: `brew install sdl3`).

**Q: How does this skill differ from `zig-raylib`?**
A: SDL3 provides a lower-level multimedia abstraction, suitable for projects needing fine-grained control over windows/events/audio. raylib focuses on game development convenience.

**Q: Does SDL3 support Wayland/X11?**
A: SDL3 auto-detects the display backend; no manual configuration is needed.
