---
name: ghostling-libghostty-terminal
description: Build minimal terminal emulators using the libghostty-vt C API with Raylib for windowing and rendering
triggers:
  - build a terminal emulator with libghostty
  - use libghostty-vt C API
  - embed terminal emulation in my app
  - ghostling terminal example
  - integrate ghostty terminal library
  - libghostty render state API
  - minimal terminal emulator in C
  - ghostty libghostty-vt bindings
---

# Ghostling — libghostty Terminal Emulator

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Ghostling is a minimal viable terminal emulator built on **libghostty-vt**, the embeddable C library extracted from [Ghostty](https://ghostty.org). It uses Raylib for windowing/rendering and lives in a single C file. The project demonstrates how to wire libghostty-vt's VT parsing, terminal state, and render-state API to any 2D or GPU renderer.

## What libghostty-vt Provides

- VT sequence parsing (SIMD-optimized)
- Terminal state: cursor, styles, text reflow, scrollback
- Render state management (what cells changed and how to draw them)
- Unicode / multi-codepoint grapheme handling
- Kitty keyboard protocol, mouse tracking, focus reporting
- Zero dependencies (not even libc) — WASM-compatible

**libghostty-vt does NOT provide:** windowing, rendering, PTY management, tabs, splits, or configuration.

## Requirements

| Tool | Version |
|------|---------|
| CMake | 3.19+ |
| Ninja | any |
| C compiler | clang/gcc |
| Zig | 0.15.x (on PATH) |
| macOS | Xcode CLT or Xcode |

## Build & Run

```sh
# Clone
git clone https://github.com/ghostty-org/ghostling.git
cd ghostling

# Debug build (slow — safety checks enabled)
cmake -B build -G Ninja
cmake --build build
./build/ghostling

# Release build (optimized)
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/ghostling
```

After first configure, only the build step is needed:

```sh
cmake --build build
```

> **Warning:** Debug builds are very slow due to Ghostty's safety/correctness assertions. Always benchmark with Release builds.

## Project Structure

```
ghostling/
├── main.c          # Entire terminal implementation (single file)
├── CMakeLists.txt  # Build config; fetches libghostty-vt + Raylib
└── demo.gif
```

## Core libghostty-vt API Patterns

All implementation lives in `main.c`. Below are the key patterns extracted from it.

### 1. Initialize the Terminal

```c
#include "ghostty.h"  // provided by libghostty-vt via CMake

// Create terminal with cols x rows cells
ghostty_terminal_t *terminal = ghostty_terminal_new(
    &(ghostty_terminal_config_t){
        .cols = cols,
        .rows = rows,
    }
);
if (!terminal) { /* handle error */ }
```

### 2. Write Data from PTY into the Terminal

```c
// Read from PTY fd, feed raw bytes to libghostty-vt
ssize_t n = read(pty_fd, buf, sizeof(buf));
if (n > 0) {
    ghostty_terminal_write(terminal, buf, (size_t)n);
}
```

### 3. Send Keyboard Input

```c
// libghostty-vt encodes the correct escape sequences
ghostty_key_event_t ev = {
    .key       = GHOSTTY_KEY_A,          // key enum
    .mods      = GHOSTTY_MODS_CTRL,      // modifier flags
    .action    = GHOSTTY_ACTION_PRESS,
    .composing = false,
};

uint8_t out[64];
size_t  out_len = 0;
ghostty_terminal_key(terminal, &ev, out, sizeof(out), &out_len);

// Write encoded bytes to PTY
if (out_len > 0) write(pty_fd, out, out_len);
```

### 4. Send Mouse Events

```c
ghostty_mouse_event_t mev = {
    .x      = cell_col,   // cell column
    .y      = cell_row,   // cell row
    .button = GHOSTTY_MOUSE_LEFT,
    .action = GHOSTTY_MOUSE_PRESS,
    .mods   = GHOSTTY_MODS_NONE,
};

uint8_t out[64];
size_t  out_len = 0;
ghostty_terminal_mouse(terminal, &mev, out, sizeof(out), &out_len);
if (out_len > 0) write(pty_fd, out, out_len);
```

### 5. Resize the Terminal

```c
ghostty_terminal_resize(terminal, new_cols, new_rows);
// libghostty-vt handles text reflow automatically
// Send SIGWINCH to the child process after this
struct winsize ws = { .ws_col = new_cols, .ws_row = new_rows };
ioctl(pty_fd, TIOCSWINSZ, &ws);
kill(child_pid, SIGWINCH);
```

### 6. Render: Walk the Render State

The render state API tells you exactly which cells changed and how to draw them — no need to redraw everything every frame.

```c
// Get render state handle
ghostty_render_state_t *rs = ghostty_terminal_render_state(terminal);

// Begin a render pass (snapshot current state)
ghostty_render_state_begin(rs);

// Iterate dirty cells
ghostty_render_cell_iter_t iter = {0};
ghostty_render_cell_t      cell;

while (ghostty_render_state_next_cell(rs, &iter, &cell)) {
    // cell.col, cell.row      — grid position
    // cell.codepoint          — Unicode codepoint (0 = empty)
    // cell.fg.r/g/b           — foreground RGB
    // cell.bg.r/g/b           — background RGB
    // cell.attrs.bold         — bold flag
    // cell.attrs.italic       — italic flag
    // cell.attrs.reverse      — reverse video

    // Example: draw with Raylib
    Color fg = { cell.fg.r, cell.fg.g, cell.fg.b, 255 };
    Color bg = { cell.bg.r, cell.bg.g, cell.bg.b, 255 };

    Rectangle rect = {
        .x      = cell.col * cell_width,
        .y      = cell.row * cell_height,
        .width  = cell_width,
        .height = cell_height,
    };
    DrawRectangleRec(rect, bg);

    if (cell.codepoint != 0) {
        char glyph[8] = {0};
        // encode codepoint to UTF-8 yourself or use a helper
        encode_utf8(cell.codepoint, glyph);
        DrawText(glyph, (int)rect.x, (int)rect.y, font_size, fg);
    }
}

// End render pass (marks cells as clean)
ghostty_render_state_end(rs);
```

### 7. Scrollback

```c
// Scroll viewport up/down by N rows
ghostty_terminal_scroll(terminal, -3);  // scroll up 3
ghostty_terminal_scroll(terminal,  3);  // scroll down 3

// Scroll to bottom
ghostty_terminal_scroll_bottom(terminal);
```

### 8. Cursor Position

```c
ghostty_cursor_t cursor;
ghostty_terminal_cursor(terminal, &cursor);
// cursor.col, cursor.row  — cell position
// cursor.visible          — bool
// cursor.shape            — GHOSTTY_CURSOR_BLOCK, _UNDERLINE, _BAR
```

### 9. Cleanup

```c
ghostty_terminal_free(terminal);
```

## PTY Setup (POSIX)

libghostty-vt has no PTY management — you own this:

```c
#include <pty.h>   // openpty
#include <unistd.h>
#include <stdlib.h>

int master_fd, slave_fd;
struct winsize ws = { .ws_row = rows, .ws_col = cols,
                      .ws_xpixel = 0, .ws_ypixel = 0 };
openpty(&master_fd, &slave_fd, NULL, NULL, &ws);

pid_t child = fork();
if (child == 0) {
    // Child: become session leader, attach slave PTY
    setsid();
    ioctl(slave_fd, TIOCSCTTY, 0);
    dup2(slave_fd, STDIN_FILENO);
    dup2(slave_fd, STDOUT_FILENO);
    dup2(slave_fd, STDERR_FILENO);
    close(master_fd);
    close(slave_fd);
    char *shell = getenv("SHELL");
    if (!shell) shell = "/bin/sh";
    execl(shell, shell, NULL);
    _exit(1);
}
// Parent: use master_fd for read/write
close(slave_fd);
```

## CMakeLists.txt Pattern

The project fetches libghostty-vt automatically via CMake FetchContent:

```cmake
cmake_minimum_required(VERSION 3.19)
project(ghostling C)

include(FetchContent)

# libghostty-vt
FetchContent_Declare(
    libghostty
    URL https://release.files.ghostty.org/tip/libghostty-vt-<platform>.tar.gz
)
FetchContent_MakeAvailable(libghostty)

# Raylib
FetchContent_Declare(
    raylib
    GIT_REPOSITORY https://github.com/raysan5/raylib.git
    GIT_TAG 5.0
)
FetchContent_MakeAvailable(raylib)

add_executable(ghostling main.c)
target_link_libraries(ghostling PRIVATE ghostty-vt raylib)
```

## Key Enums & Constants

```c
// Keys
GHOSTTY_KEY_A … GHOSTTY_KEY_Z
GHOSTTY_KEY_UP, GHOSTTY_KEY_DOWN, GHOSTTY_KEY_LEFT, GHOSTTY_KEY_RIGHT
GHOSTTY_KEY_ENTER, GHOSTTY_KEY_BACKSPACE, GHOSTTY_KEY_ESCAPE, GHOSTTY_KEY_TAB
GHOSTTY_KEY_F1 … GHOSTTY_KEY_F12

// Modifiers (bitmask)
GHOSTTY_MODS_NONE
GHOSTTY_MODS_SHIFT
GHOSTTY_MODS_CTRL
GHOSTTY_MODS_ALT
GHOSTTY_MODS_SUPER

// Mouse buttons
GHOSTTY_MOUSE_LEFT, GHOSTTY_MOUSE_RIGHT, GHOSTTY_MOUSE_MIDDLE
GHOSTTY_MOUSE_WHEEL_UP, GHOSTTY_MOUSE_WHEEL_DOWN

// Cursor shapes
GHOSTTY_CURSOR_BLOCK, GHOSTTY_CURSOR_UNDERLINE, GHOSTTY_CURSOR_BAR
```

## Common Patterns

### Non-blocking PTY Read Loop

```c
// Set master_fd non-blocking
fcntl(master_fd, F_SETFL, O_NONBLOCK);

// In your main loop:
uint8_t buf[4096];
ssize_t n;
while ((n = read(master_fd, buf, sizeof(buf))) > 0) {
    ghostty_terminal_write(terminal, buf, (size_t)n);
}
// EAGAIN means no data available — not an error
```

### Raylib Key → ghostty_key_t Mapping

```c
ghostty_key_t raylib_key_to_ghostty(int rl_key) {
    switch (rl_key) {
        case KEY_A: return GHOSTTY_KEY_A;
        case KEY_ENTER: return GHOSTTY_KEY_ENTER;
        case KEY_BACKSPACE: return GHOSTTY_KEY_BACKSPACE;
        case KEY_UP: return GHOSTTY_KEY_UP;
        case KEY_DOWN: return GHOSTTY_KEY_DOWN;
        // ... etc
        default: return GHOSTTY_KEY_INVALID;
    }
}
```

### Scrollbar Rendering

```c
int total_rows    = ghostty_terminal_total_rows(terminal);
int viewport_rows = rows; // your grid height
int scroll_offset = ghostty_terminal_scroll_offset(terminal);

float bar_h      = (float)viewport_rows / total_rows * window_height;
float bar_y      = (float)scroll_offset / total_rows * window_height;
DrawRectangle(window_width - SCROLLBAR_W, (int)bar_y,
              SCROLLBAR_W, (int)bar_h, GRAY);
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Build fails: `zig not found` | Install Zig 0.15.x and ensure it's on `$PATH` |
| Debug build extremely slow | Use Release: `cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release` |
| Terminal renders garbage | Verify you're calling `ghostty_render_state_begin` before iterating cells and `ghostty_render_state_end` after |
| Child process not getting resize | Call `ioctl(pty_fd, TIOCSWINSZ, &ws)` AND `kill(child_pid, SIGWINCH)` after `ghostty_terminal_resize` |
| Kitty keyboard protocol broken | Known upstream Raylib/GLFW limitation — libghostty-vt supports it correctly but needs richer input events |
| Colors look wrong | Check `cell.fg`/`cell.bg` — libghostty-vt resolves palette to RGB, use those values directly |
| `ghostty_terminal_write` crashes | Ensure buffer passed is valid and `len > 0`; never pass NULL |

## What libghostty-vt Will NOT Do For You

You must implement these yourself:
- PTY creation and process management
- Window creation and event loop
- Font loading and glyph rendering
- Clipboard read/write (OSC 52 bytes are provided, handling is yours)
- Tabs, splits, multiple windows
- Configuration UI

## API Reference

Full libghostty-vt C API docs: https://libghostty.tip.ghostty.org/group__render.html
