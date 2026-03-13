---
name: dragonruby
description: Build games and prototypes with DragonRuby GTK (DRGTK). Use this skill when the user asks to write DragonRuby game code, implement game mechanics, work with the DRGTK API, or debug DragonRuby projects.
---

This skill guides writing idiomatic, performant DragonRuby GTK (DRGTK) game code. DragonRuby uses a 60fps game loop, a bottom-left coordinate origin (1280×720), and flows everything through the `args` object passed to `tick`.

## Sub-skills

For specialised topics, use these companion skills:
- `/dragonruby-rendering` — render targets, cameras, HD/lowrez, pixel arrays, advanced sprites
- `/dragonruby-audio` — spatial audio, procedural synthesis, beat sync, crossfading
- `/dragonruby-3d` — 3D rendering, raycasting, Mode7, matrix math, VR
- `/dragonruby-pathfinding` — A*, BFS, flood fill, quadtrees, spatial queries
- `/dragonruby-ui` — UI controls, menus, scroll views, accessibility, input remapping
- `/dragonruby-platformer` — platformer physics, action states, cameras, level editors

## Project Structure

Each game gets its own unzipped copy of DragonRuby — never share the engine binary across projects.

```
mygame/
  app/
    main.rb       # entry point — defines tick(args)
    player.rb     # require from main.rb
    enemies.rb
  sprites/
  sounds/
  fonts/
  metadata/
    game_metadata.txt   # title, version, itch/steam IDs, orientation
    cvars.txt           # dev server, rendering options
  tmp/    # gitignore
  logs/   # gitignore
```

## .gitignore

The DragonRuby engine binary is large and licensed per-developer — never commit it. Builds and runtime-generated directories should also be excluded.

```gitignore
# DragonRuby engine (download separately — do not commit)
dragonruby
dragonruby.exe
DragonRuby\ GTK.app/

# Runtime-generated directories
tmp/
logs/

# Export builds (large platform-specific archives)
builds/

# OS artifacts
.DS_Store
Thumbs.db

# Solargraph LSP config (optional — commit if whole team uses it)
# .solargraph.yml
```

Place this file at the root of your project (the directory containing `mygame/`). The engine binary lives at the same level and must not be pushed to a public repo due to licensing.

## Core Loop & Lifecycle

```ruby
def boot(args)
  args.state = {}   # initialize state cleanly
end

def tick(args)
  defaults(args)
  input(args)
  calc(args)
  render(args)
end

def shutdown(args)
  # runs before exit
end
```

Keep `tick` as a coordinator that delegates to focused methods. This is the idiomatic DRGTK structure.

## State (`args.state`)

Persistent property bag — values survive between ticks. Use `||=` to initialize once.

```ruby
# Simple values
args.state.score     ||= 0
args.state.enemies   ||= []
args.state.game_over ||= false

# Entity with auto-generated id/timestamps
args.state.player ||= args.state.new_entity(:player) do |p|
  p.x = 640; p.y = 360; p.w = 32; p.h = 32
  p.hp = 3
end

# Spawning into a collection
args.state.enemies << args.state.new_entity(:enemy) do |e|
  e.x = rand(1280); e.y = 720; e.hp = 1
end
```

State entities auto-get: `entity_id`, `entity_type`, `created_at`, `created_at_elapsed`, `global_created_at`.

`GTK.reset` wipes all state. Within tick, use `GTK.reset_next_tick`.

### Serialisation (save/load)
```ruby
GTK.serialize_state('save.txt', args.state)
loaded = GTK.deserialize_state('save.txt')
args.state = loaded if loaded
```

For more control use JSON:
```ruby
GTK.write_file('save.json', { score: args.state.score }.to_json)
data = GTK.parse_json(GTK.read_file('save.json'))
```

### Class-based approach (for larger games)
```ruby
class Game
  attr_gtk  # injects args, state, inputs, outputs, audio

  def tick
    state.player ||= { x: 640, y: 360 }
    calc_movement
    render_player
  end
end

$game ||= Game.new
def tick(args)
  $game.args = args
  $game.tick
end
```

## Outputs / Rendering

**Origin: bottom-left.** Screen is 1280×720.

Render order (back → front): `solids → sprites → primitives → labels → lines → borders → debug`

### Sprites
```ruby
args.outputs.sprites << {
  x: 100, y: 100, w: 32, h: 32,
  path: 'sprites/hero.png',
  angle: 45,                          # degrees counter-clockwise
  anchor_x: 0.5, anchor_y: 0.5,      # rotation pivot (0–1)
  flip_horizontally: facing_left,
  r: 255, g: 255, b: 255, a: 255,    # tint + alpha
  # Sprite sheet cropping (source_ uses bottom-left origin):
  source_x: 0, source_y: 0, source_w: 16, source_h: 16
  # OR tile_ (top-left origin):
  # tile_x: 0, tile_y: 0, tile_w: 16, tile_h: 16
}
```

Triangle sprites (three-vertex form):
```ruby
args.outputs.sprites << { x: 0, y: 0, x2: 50, y2: 100, x3: 100, y3: 0, path: 'sprites/tex.png' }
```

### Convenience bang methods
```ruby
rect.merge(r: 255, g: 0, b: 0).solid!    # returns hash with primitive_marker: :solid
rect.merge(r: 255).border!
rect.center.merge(text: "hi").label!
```

### Solids, borders, lines
```ruby
args.outputs.solids   << { x: 0, y: 0, w: 100, h: 100, r: 255, g: 0, b: 0, a: 200 }
args.outputs.borders  << { x: 10, y: 10, w: 200, h: 50, r: 255, g: 255, b: 0 }
args.outputs.lines    << { x: 0, y: 0, x2: 100, y2: 100, r: 255 }
```

Special paths:
```ruby
{ path: :solid }    # filled rect without an image file
{ path: :empty }    # transparent (useful with blendmode: 0 for clipping)
```

### Labels
```ruby
args.outputs.labels << {
  x: 640, y: 360,
  text: "Score: #{args.state.score}",
  size_px: 24,                         # OR size_enum: 2
  alignment_enum: 1,                   # 0=left 1=center 2=right
  vertical_alignment_enum: 1,          # 0=bottom 1=center 2=top
  font: 'fonts/myfont.ttf',
  r: 255, g: 255, b: 255, a: 255
}

# Multi-line text helpers
lines = String.wrapped_lines(long_text, 40)    # array of strings, max 40 chars each
```

### Background color
```ruby
args.outputs.background_color = [30, 30, 40]
```

### Debug output
```ruby
args.outputs.debug << "tick: #{Kernel.tick_count}"
args.outputs.debug.watch(args.state.player)
args.outputs.debug << args.gtk.framerate_diagnostics_primitives
```

### Primitives (manual layering)
```ruby
args.outputs.primitives << { primitive_marker: :sprite, x: 0, y: 0, w: 32, h: 32, path: 'img.png' }
```

## Inputs

### Keyboard
```ruby
args.inputs.keyboard.key_down.space     # true only the tick pressed
args.inputs.keyboard.key_held.left      # true while held
args.inputs.keyboard.key_up.escape      # true the tick released

# Available: .a–.z, .left, .right, .up, .down, .space, .enter,
#            .backspace, .escape, .tab, .shift, .control, .alt,
#            .f1–.f12, number keys, etc.
```

### Mouse
```ruby
args.inputs.mouse.x, args.inputs.mouse.y
args.inputs.mouse.click            # click event object (nil or has .x/.y/.point)
args.inputs.mouse.click.point      # {x:, y:} — useful for inside_rect?
args.inputs.mouse.button_left      # held
args.inputs.mouse.button_right
args.inputs.mouse.held             # any button held
args.inputs.mouse.up               # released this tick
args.inputs.mouse.moved
args.inputs.mouse.wheel            # { x:, y: } scroll delta
args.inputs.mouse.inside_rect?(rect)
args.inputs.mouse.position         # {x:, y:} — always available (no click required)

# Previous click for drag detection:
args.inputs.mouse.previous_click
```

**Drag and drop pattern:**
```ruby
if args.inputs.mouse.click && target_under_mouse
  args.state.dragging = target_under_mouse.id
  args.state.drag_offset = { x: args.inputs.mouse.x - target.x,
                              y: args.inputs.mouse.y - target.y }
elsif args.inputs.mouse.held && args.state.dragging
  target.x = args.inputs.mouse.x - args.state.drag_offset.x
  target.y = args.inputs.mouse.y - args.state.drag_offset.y
elsif args.inputs.mouse.up
  args.state.dragging = nil
end
```

### Controller
```ruby
c = args.inputs.controller_one   # also controller_two, three, four
c.key_down.a; c.key_held.b; c.key_up.x
c.left_analog_x_perc    # -1.0 to 1.0
c.left_analog_y_perc
c.connected
# Buttons: .a .b .x .y .l1 .r1 .l2 .r2 .l3 .r3 .start .select
```

### Unified input (keyboard + controller)
```ruby
args.inputs.left_right           # -1, 0, or 1
args.inputs.up_down              # -1, 0, or 1
args.inputs.left_right_perc      # -1.0 to 1.0
args.inputs.directional_vector   # {x:, y:} or nil — safe-navigate with &.
args.inputs.last_active          # :keyboard, :mouse, or :controller
```

**Unified movement:**
```ruby
v = args.inputs.directional_vector
player.x += (v&.x || 0) * player_speed
player.y += (v&.y || 0) * player_speed
```

### Touch
```ruby
args.inputs.touch               # hash of active touch points
args.inputs.finger_left.x
args.inputs.finger_right.x
```

## Scene Management

```ruby
def tick(args)
  args.state.scene ||= :title

  case args.state.scene
  when :title then tick_title(args)
  when :game  then tick_game(args)
  when :over  then tick_over(args)
  end

  # Apply queued scene changes atomically at end of tick
  if args.state.next_scene
    args.state.scene = args.state.next_scene
    args.state.next_scene = nil
  end
end
```

Never set `args.state.scene` directly mid-tick; always use `next_scene`.

For fade transitions:
```ruby
args.state.scene_at ||= Kernel.tick_count
a = 255 - (255 * args.state.scene_at.ease(30, :flip))
args.outputs.solids << { x: 0, y: 0, w: 1280, h: 720, r: 0, g: 0, b: 0, a: a }
```

## Geometry

All methods via `Geometry.*` or `args.geometry.*`.

### Collision
```ruby
Geometry.intersect_rect?(a, b)
Geometry.intersect_rect?(a, b, tolerance)
Geometry.inside_rect?(inner, outer)
Geometry.find_intersect_rect(rect, array)         # first hit
Geometry.find_all_intersect_rect(rect, array)     # all hits
Geometry.find_collisions(rects)                   # full collision map

# On objects directly:
player.intersect_rect?(enemy)
array.any_intersect_rect?(player)

# Quad tree (many entities):
qt = Geometry.create_quad_tree(rects)
Geometry.find_all_intersect_rect_quad_tree(rect, qt)

# Circles:
Geometry.intersect_circle?(shape1, shape2)
Geometry.point_inside_circle?(point, center, radius)
```

### Distance & Angles
```ruby
Geometry.distance(a, b)
Geometry.distance_squared(a, b)   # faster for comparisons
Geometry.angle(from, to)          # degrees
Geometry.angle_from(to, from)
Geometry.angle_vec(degrees)       # { x:, y: } unit vector
```

### Transforms
```ruby
Geometry.rotate_point(point, degrees, pivot)
Geometry.scale_rect(rect, ratio)
Geometry.anchor_rect(rect, anchor_x, anchor_y)
Geometry.center_inside_rect(target, reference)
Geometry.rect_center_point(rect)
Geometry.rect_to_lines(rect)
# UI menu navigation:
Geometry.rect_navigate(rect, rects, left_right, up_down, wrap_x: false, wrap_y: false)
```

### Rect helpers on objects
```ruby
player.shift_rect(dx, dy)       # returns moved rect hash
player.center                   # { x:, y: }
```

## Audio

```ruby
# One-shot sound
args.outputs.sounds << 'sounds/coin.wav'
args.outputs.sounds << { path: 'sounds/hit.wav', gain: 0.5 }

# Persistent / looping
args.audio[:music] = {
  input: 'sounds/theme.ogg',
  looping: true,
  gain: 0.8,
  pitch: 1.0,
  paused: false,
  x: 0.0, y: 0.0, z: 0.0   # spatial: -1 to 1
}
args.audio.delete(:music)         # stop
args.audio.volume = 0.5           # global volume

# Inspect after loading:
args.audio[:music].playtime    # seconds elapsed
args.audio[:music].playlength  # total duration
```

For advanced audio (spatial, synthesis, beat sync, crossfading) → use `/dragonruby-audio`.

## Easing & Animation

### Numeric helpers
```ruby
# Frame animation
frame = start_tick.frame_index(frame_count: 4, hold_each_frame_for: 8, repeat: true)
path  = "sprites/walk_#{frame}.png"

# Timing
start_tick.elapsed_time         # ticks since start_tick
start_tick.elapsed?(120)        # true if 120 ticks have passed

# Lerp & math
current_x = current_x.lerp(target_x, 0.1)
current_x = current_x.towards(target_x, 5)   # move by up to 5 units/tick
val.clamp(0, 100)
val.clamp_wrap(0, 100)
val.remap(0, 100, 0.0, 1.0)
angle.vector_x; angle.vector_y             # cos/sin components
angle.vector_x(distance); angle.vector_y(distance)   # scaled
2.seconds   # => 120 frames

# Simple ease on a tick:
perc = start_tick.ease(duration, :smooth_stop_quint)  # 0.0 to 1.0
x = x_start + (x_end - x_start) * perc
```

### Easing module
```ruby
perc = Easing.ease(start_tick, args.tick_count, duration, :smooth_stop_quint)
# Definitions: :identity, :flip, :quad, :cube, :quart, :quint,
#   :smooth_start_quad/cube/quart/quint, :smooth_stop_quad/cube/quart/quint

perc = Easing.smooth_stop(start_at: start_tick, end_at: start_tick + duration,
                           tick_count: args.tick_count, power: 3)
perc = Easing.spline(start_tick, args.tick_count, duration, [[0, 0.33, 0.66, 1.0]])
```

### Particle / fade queue
```ruby
args.state.particles ||= []
# Spawn:
args.state.particles << { x: x, y: y, w: 8, h: 8,
                            dx: angle.vector_x(3), dy: angle.vector_y(3),
                            a: 255, path: 'sprites/particle.png' }
# Update:
args.state.particles.each { |p| p.x += p.dx; p.y += p.dy; p.dx *= 0.95; p.a -= 8 }
args.state.particles.reject! { |p| p.a <= 0 }
```

## Layout

12×24 grid in landscape. Returns pixel rects for responsive UI.

```ruby
rect = Layout.rect(row: 0, col: 0, w: 6, h: 2)
# => { x:, y:, w:, h:, center: { x:, y: } }

group = Layout.rect_group(row: 10, dcol: 1, w: 1, h: 1, group: items)
args.outputs.debug << Layout.debug_primitives  # visualise the grid
Layout.portrait?; Layout.landscape?
```

## Runtime / GTK Utilities

### Window & cursor
```ruby
args.gtk.set_window_title("My Game")
args.gtk.toggle_window_fullscreen
args.gtk.set_window_scale(2)
args.gtk.hide_cursor
args.gtk.set_cursor('sprites/cursor.png', 0, 0)
args.gtk.set_mouse_grab(1)   # 0=ungrab, 1=grab, 2=grab+relative
```

### File I/O (sandboxed)
```ruby
args.gtk.write_file('save.json', content)
args.gtk.read_file('save.json')        # returns nil if missing
args.gtk.append_file('log.txt', "line\n")
args.gtk.delete_file('old.txt')
args.gtk.list_files('saves/')
```
Write path: macOS `~/Library/Application Support/[game]`, Windows `AppData\Roaming\[dev]\[game]`, Linux `~/.local/share/[game]`.

### Data parsing
```ruby
args.gtk.parse_json('{"score":42}')
args.gtk.parse_json_file('data/config.json')
args.gtk.parse_xml_file('data/levels.xml')
```

### Sprite utilities
```ruby
args.gtk.calcstringbox("Hello", size_enum, font)   # [w, h]
args.gtk.calcspritebox('sprites/hero.png')          # [w, h]
args.gtk.get_string_rect("text", size_enum, font)   # hash
args.gtk.reset_sprite('sprites/hero.png')
```

### Async HTTP
```ruby
$req ||= args.gtk.http_get('https://example.com/data.json')
if $req && $req[:complete]
  data = args.gtk.parse_json($req[:response_data]) if $req[:http_response_code] == 200
  $req = nil
end
```

### Development helpers
```ruby
GTK.reset            # wipe state (use in console)
GTK.reset_next_tick  # safe to call within tick
GTK.slowmo!(2)       # half-speed debug
args.gtk.notify!("msg")
args.gtk.benchmark(seconds: 1, a: -> { fast }, b: -> { slow })
Kernel.tick_count           # current tick
Kernel.global_tick_count    # never resets
args.gtk.platform?(:macos)  # :win :linux :web :ios :android :touch :desktop
args.gtk.production?
```

### Console (dev tool)
```ruby
# In boot or tick:
GTK.console.set_command "reset_with count: 100"

# Custom console buttons:
class GTK::Console::Menu
  def custom_buttons
    [button(id: :my_btn, row: 2, col: 18, text: "Reset", method: :my_reset)]
  end
  def my_reset
    GTK.reset
  end
end
```

## Array & Numeric Extensions

### Array
```ruby
tiles.map_2d { |row, col, tile| ... }
items.include_any?([:sword, :shield])
rects.any_intersect_rect?(player, 0.1)
list.reject_nil                    # compact alias
list.reject_false                  # removes nil + false
[1,2].product([3,4])               # all combinations
array.push_back(item)              # append
array.pop_front                    # shift
```

### Numeric
```ruby
2.seconds                    # 120 frames
val.lerp(10, 0.1)
val.towards(10, 2)           # move toward 10 by max 2
val.clamp(0, 100)
val.clamp_wrap(0, 100)
val.remap(0, 100, 0.0, 1.0)
val.to_radians; val.to_degrees
val.idiv(32)                 # integer division
val.fdiv(3)                  # float division
val.zmod?(3)                 # val % 3 == 0
tick.elapsed_time
tick.elapsed?(duration)
tick.frame_index(frame_count: 4, hold_each_frame_for: 8, repeat: true)
val.randomize(:ratio)        # random 0..val
val.randomize(:ratio, :sign) # random -val..val
(-1..1).rand                 # random float in range
```

## Common Patterns

### Spawn on interval
```ruby
if Kernel.tick_count.zmod?(120)   # every 2 seconds
  args.state.enemies << { x: 1280, y: rand(720), w: 16, h: 16, hp: 3 }
end
```

### Remove dead entities
```ruby
args.state.enemies.reject! { |e| e[:hp] <= 0 || e[:x] < -32 }
```

### Collision response
```ruby
args.state.enemies.each do |e|
  next unless Geometry.intersect_rect?(args.state.player, e)
  e[:hp] -= 1
  # push-back:
  angle = Geometry.angle(e, args.state.player)
  e[:x] += angle.vector_x * 3
  e[:y] += angle.vector_y * 3
end
```

### Snap to grid
```ruby
grid_x = mouse_x.idiv(32) * 32
grid_y = mouse_y.idiv(32) * 32
```

### Screen center
```ruby
cx = args.grid.w / 2   # 640
cy = args.grid.h / 2   # 360
```

### Smooth camera follow
```ruby
args.state.cam_x = args.state.cam_x.lerp(player.x - 640, 0.08)
args.state.cam_y = args.state.cam_y.lerp(player.y - 360, 0.08)
```

### Camera shake (trauma-based)
```ruby
args.state.trauma = (args.state.trauma + 0.3).clamp(0, 1)
offset = 20.0 * args.state.trauma ** 2
cam.x_off = offset.randomize(:ratio, :sign)
cam.y_off = offset.randomize(:ratio, :sign)
args.state.trauma *= 0.92   # decay each tick
```

### Timed flash effect
```ruby
args.state.flash_at ||= -999
args.state.flash_at = Kernel.tick_count if hit
if args.state.flash_at.elapsed_time < 30
  a = 255 * args.state.flash_at.ease(30, :flip)
  args.outputs.solids << { x: 0, y: 0, w: 1280, h: 720, r: 255, g: 255, b: 255, a: a }
end
```

### Floating damage numbers
```ruby
args.state.floaters ||= []
args.state.floaters << { x: e.x, y: e.y, text: "-#{dmg}", a: 255, dy: 2 }
args.state.floaters.each { |f| f.y += f.dy; f.a -= 5 }
args.state.floaters.reject! { |f| f.a <= 0 }
args.outputs.labels << args.state.floaters.map { |f| f.merge(r: 255, g: 0, b: 0) }
```

### Frame animation (sprite sheet)
```ruby
col = args.state.anim_start.frame_index(frame_count: 6, hold_each_frame_for: 5, repeat: true)
args.outputs.sprites << { x: p.x, y: p.y, w: 32, h: 32,
                           path: 'sprites/run.png',
                           source_x: col * 32, source_y: 0, source_w: 32, source_h: 32 }
```

### Directional sprite flipping
```ruby
path: "sprites/hero.png",
flip_horizontally: player.dx < 0
```

### Wave difficulty scaling
```ruby
args.state.spawn_rate = (args.state.spawn_rate * 0.95).to_i.clamp(20, 300)
```

### Seeded RNG for reproducibility
```ruby
@rng = Random.new(seed)
val = @rng.rand(0...10)
```

## Performance Tips

- Prefer Hash or class primitives over Array form in hot code paths
- `args.outputs.static_sprites` — holds references instead of clearing each tick; update in place
- Implement `draw_override(ffi_draw)` + `attr_sprite` for maximum render throughput
- Use `Geometry.create_quad_tree` for collision with many entities
- Use `Geometry.distance_squared` instead of `distance` when comparing distances
- Avoid allocating new arrays every tick — mutate in place (`reject!`, `map!`, `push`)
- Use render targets (`:symbol`) to cache complex scenes; only redraw when content changes
- Viewport culling: only transform/render entities inside the camera rect
- One-time initialization guard: `return if Kernel.tick_count != 0`
- `args.gtk.warn_array_primitives!` — audits array-form output usage

```ruby
# Static sprites (fastest for large numbers of mostly-static objects)
if Kernel.tick_count == 0
  args.state.stars = 500.map { Star.new(args.grid) }
  args.outputs.static_sprites << args.state.stars
end
# Stars mutate in place; no need to re-add each tick

# draw_override (maximum speed):
class Star
  attr_sprite
  def draw_override(ffi_draw)
    ffi_draw.draw_sprite @x, @y, @w, @h, @path
  end
end
```
