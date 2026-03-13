---
name: humanization-2026
description: >
  Advanced 2026 browser automation humanization — mouse trajectories, keystroke dynamics,
  scroll behavior, session pacing, and anti-detection evasion. Use this skill whenever
  writing any Playwright or Camoufox interaction code that must avoid bot detection:
  typing, clicking, scrolling, navigating, or managing session behavior. DO NOT write
  bare page.click() or page.fill() without applying humanization from this skill.
  Covers the full science: Bézier + Fitts's Law mouse curves, Gaussian keystroke timing,
  scroll jitter, session warmup, and what 2026 ML detectors actually measure.
---

# Humanization 2026 — Full Reference

> [!CAUTION]
> This skill documents **legitimate HCI research** (Bézier curves, Fitts's Law,
> Gaussian keystroke dynamics) for use in **authorized** browser automation and
> accessibility testing. Do **not** use these techniques to circumvent terms of
> service, impersonate real users, or conduct unauthorized automated access.
> You are responsible for ensuring your use complies with applicable laws and
> platform policies.

## Why This Skill Exists
In 2026, anti-bot systems use **ML behavioral biometric analysis** — not just fingerprinting.
They analyze: mouse trajectory curvature, velocity profiles, keystroke dwell+flight time
distributions, scroll rhythm, idle behavior, and inter-action timing entropy.

Camoufox's `humanize=True` handles C++-level fingerprint patching.
**It does NOT handle behavioral patterns** — that is entirely your code's responsibility.

See `references/detection-signals.md` for what ML detectors measure.
See `references/math.md` for algorithm derivations.

---

## Layer 1: Mouse Movement

### The Science
Humans move mice via two-phase motor control (Woodworth, 1899):
1. **Initial ballistic phase** — fast, distance-driven, imprecise
2. **Final homing phase** — slow, target-size-driven, precise

Fitts's Law predicts movement time: `MT = a + b × log₂(D/W + 1)`
- D = distance to target, W = target width
- Large buttons nearby → fast. Small buttons far away → slow.
- Detectors verify that your timing *matches* the D/W ratio of each element.

### Algorithm: Cubic Bézier + Jitter + Overshoot

```python
import asyncio
import random
import math
import numpy as np

def _bezier_curve(start: tuple, end: tuple, num_points: int = 50) -> list[tuple]:
    """
    Cubic Bézier curve between two points with randomized control points.
    Control points are placed on ONE side of the line (not both) — humans
    don't make S-curves; they arc to one side.
    """
    x1, y1 = start
    x2, y2 = end
    
    # Midpoint
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    
    # Perpendicular offset — control points arc to one side
    dx, dy = x2 - x1, y2 - y1
    dist = math.hypot(dx, dy)
    
    if dist < 1:
        return [start, end]
    
    # Perpendicular direction
    px, py = -dy / dist, dx / dist
    
    # Arc magnitude: 10-25% of distance, always same side (not random side per point)
    arc_side = random.choice([-1, 1])  # chosen once per movement
    arc1 = arc_side * random.uniform(0.1, 0.25) * dist
    arc2 = arc_side * random.uniform(0.05, 0.2) * dist
    
    # Two control points
    cp1 = (x1 + dx * 0.3 + px * arc1, y1 + dy * 0.3 + py * arc1)
    cp2 = (x1 + dx * 0.7 + px * arc2, y1 + dy * 0.7 + py * arc2)
    
    # Generate curve points
    points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        # Cubic Bézier formula
        bx = (1-t)**3 * x1 + 3*(1-t)**2*t * cp1[0] + 3*(1-t)*t**2 * cp2[0] + t**3 * x2
        by = (1-t)**3 * y1 + 3*(1-t)**2*t * cp1[1] + 3*(1-t)*t**2 * cp2[1] + t**3 * y2
        points.append((bx, by))
    
    return points


def _fitts_duration(dist: float, target_w: float) -> float:
    """
    Fitts's Law: MT = a + b × log₂(D/W + 1)
    Returns movement duration in seconds.
    Constants calibrated for mouse (~200-800ms range).
    """
    a = 0.05   # motor initiation constant
    b = 0.12   # motor control constant
    id_ = math.log2(dist / max(target_w, 10) + 1)
    mt = a + b * id_
    # Add human variance (±15%)
    return mt * random.uniform(0.85, 1.15)


def _apply_jitter(points: list[tuple], sigma: float = 0.5) -> list[tuple]:
    """
    Add Gaussian micro-jitter to path — simulates natural hand tremor.
    μ=0, σ=0.5 pixels: subtle, statistically identical to human data.
    """
    return [
        (x + random.gauss(0, sigma), y + random.gauss(0, sigma))
        for x, y in points
    ]


async def human_move(page, target_x: float, target_y: float,
                     target_w: float = 20, overshoot: bool = True):
    """
    Move mouse to target with:
    - Cubic Bézier curved path
    - Fitts's Law timing
    - Gaussian jitter
    - Overshoot + correction (for distant targets)
    """
    # Get current position
    curr = await page.evaluate("() => ({x: window.mouseX || 0, y: window.mouseY || 0})")
    start = (curr.get("x", 0), curr.get("y", 0))
    end = (target_x, target_y)
    
    dist = math.hypot(end[0] - start[0], end[1] - start[1])
    duration = _fitts_duration(dist, target_w)
    
    # Overshoot for distant targets (>300px) — humans overshoot then correct
    if overshoot and dist > 300:
        # Overshoot 3-8% past target
        overshoot_factor = random.uniform(1.03, 1.08)
        ox = end[0] + (end[0] - start[0]) * (overshoot_factor - 1)
        oy = end[1] + (end[1] - start[1]) * (overshoot_factor - 1)
        
        # Phase 1: move to overshoot point
        path1 = _bezier_curve(start, (ox, oy), num_points=40)
        path1 = _apply_jitter(path1)
        step_time = duration * 0.7 / len(path1)
        for x, y in path1:
            await page.mouse.move(x, y)
            await asyncio.sleep(step_time)
        
        # Phase 2: correct back to target (shorter, slower)
        path2 = _bezier_curve((ox, oy), end, num_points=15)
        path2 = _apply_jitter(path2, sigma=0.3)
        step_time = duration * 0.3 / len(path2)
        for x, y in path2:
            await page.mouse.move(x, y)
            await asyncio.sleep(step_time)
    else:
        # Straight Bézier move
        num_points = max(20, int(dist / 10))
        path = _bezier_curve(start, end, num_points=num_points)
        path = _apply_jitter(path)
        
        # Non-uniform timing: accelerate then decelerate (ease-in-out)
        for i, (x, y) in enumerate(path):
            await page.mouse.move(x, y)
            t = i / len(path)
            # Ease-in-out timing: slower at start and end
            speed_factor = 1 - abs(2 * t - 1) ** 2 * 0.5
            await asyncio.sleep((duration / len(path)) / speed_factor)
    
    # Hover pause before click (humans aim before clicking)
    await asyncio.sleep(random.uniform(0.05, 0.18))
```

---

## Layer 2: Clicking

```python
async def human_click(page, selector: str, button: str = "left"):
    """
    Click with:
    - Random point within element bounding box (not center)
    - Mouse move to element first
    - Variable mousedown → mouseup duration
    """
    elem = page.locator(selector)
    await elem.wait_for(state="visible")
    
    box = await elem.bounding_box()
    if not box:
        await elem.click()
        return
    
    # Random point in bounding box (±30% from center)
    cx = box["x"] + box["width"] * random.uniform(0.3, 0.7)
    cy = box["y"] + box["height"] * random.uniform(0.3, 0.7)
    
    await human_move(page, cx, cy, target_w=box["width"])
    
    # Variable press duration (50-180ms) — humans don't click instantly
    await page.mouse.down(button=button)
    await asyncio.sleep(random.uniform(0.05, 0.18))
    await page.mouse.up(button=button)
    
    # Post-click micro-pause
    await asyncio.sleep(random.uniform(0.08, 0.25))
```

---

## Layer 3: Keystroke Dynamics

### The Science
Anti-bot systems measure two metrics per keystroke pair:
- **Dwell time (DT)**: duration key is held down (key_press → key_release)
- **Flight time (FT)**: time between key_release and next key_press

Human distributions follow **Gaussian (normal)** patterns:
- Dwell: μ ≈ 80ms, σ ≈ 20ms
- Flight: μ ≈ 120ms, σ ≈ 40ms
- Familiar character sequences (common digraphs) are 20-40% faster

Mechanical bots: perfectly uniform timing → instantly flagged.
Uniform random: wrong distribution shape → flagged.
Gaussian: matches real human data.

```python
async def human_type(page, selector: str, text: str,
                     wpm: float = 65, error_rate: float = 0.02):
    """
    Type text with:
    - Gaussian dwell + flight time per character
    - Digraph speed boost for common pairs
    - Realistic typo + correction simulation
    - Pre-type focus behavior
    """
    # Common fast digraphs (muscle memory — 30% faster)
    fast_digraphs = {
        "th", "he", "in", "er", "an", "re", "on", "en",
        "at", "es", "or", "te", "of", "ed", "is", "it",
        "al", "ar", "st", "to", "nt", "ng", "se", "ha",
    }
    
    # Base timing from WPM (1 word = 5 chars)
    base_flight = 60 / (wpm * 5) * 1000  # ms per character
    
    elem = page.locator(selector)
    await elem.click()
    await asyncio.sleep(random.uniform(0.2, 0.5))  # focus pause
    
    i = 0
    while i < len(text):
        char = text[i]
        
        # Typo simulation
        if random.random() < error_rate and char.isalpha():
            typo_char = random.choice("qwertyuiop")
            # Type wrong char
            await page.keyboard.down(typo_char)
            dwell = random.gauss(80, 20)
            await asyncio.sleep(max(30, dwell) / 1000)
            await page.keyboard.up(typo_char)
            
            # Pause (noticing error)
            await asyncio.sleep(random.uniform(0.15, 0.5))
            
            # Backspace
            await page.keyboard.press("Backspace")
            await asyncio.sleep(random.uniform(0.08, 0.2))
        
        # Digraph speed boost
        if i > 0:
            digraph = text[i-1:i+1].lower()
            speed_mult = 0.7 if digraph in fast_digraphs else 1.0
        else:
            speed_mult = 1.0
        
        # Press key
        await page.keyboard.down(char)
        
        # Dwell time: Gaussian μ=80ms σ=20ms
        dwell = random.gauss(80, 20) * speed_mult
        await asyncio.sleep(max(30, dwell) / 1000)
        
        await page.keyboard.up(char)
        
        # Flight time: Gaussian μ=base_flight σ=base_flight*0.35
        flight = random.gauss(base_flight, base_flight * 0.35) * speed_mult
        await asyncio.sleep(max(20, flight) / 1000)
        
        i += 1
    
    # Post-type pause (reviewing what was typed)
    await asyncio.sleep(random.uniform(0.3, 0.8))
```

---

## Layer 4: Scrolling

```python
async def human_scroll(page, direction: str = "down",
                       distance: int = 400, read_pause: bool = True):
    """
    Scroll with:
    - Variable speed (not constant)
    - Micro-pauses (reading behavior)
    - Occasional scroll reversal (re-reading)
    - Jitter in scroll amount per step
    """
    steps = random.randint(4, 8)
    total = 0
    sign = 1 if direction == "down" else -1
    
    for i in range(steps):
        # Variable scroll amount per step with jitter
        step_dist = (distance / steps) * random.uniform(0.7, 1.3)
        await page.evaluate(f"window.scrollBy(0, {int(sign * step_dist)})")
        total += step_dist
        
        # Pause between scroll steps (reading rhythm)
        await asyncio.sleep(random.uniform(0.08, 0.25))
    
    # Occasional scroll-back (re-reading — very human)
    if read_pause and random.random() < 0.2:
        back = random.uniform(50, 150)
        await asyncio.sleep(random.uniform(0.3, 0.8))
        await page.evaluate(f"window.scrollBy(0, {int(-sign * back)})")
        await asyncio.sleep(random.uniform(0.4, 1.2))
    
    # Reading pause after scroll
    if read_pause:
        await asyncio.sleep(random.uniform(0.8, 3.0))
```

---

## Layer 5: Session-Level Behavior

### What ML Detectors Measure at Session Level
- **Action entropy**: humans vary their actions; bots repeat identical sequences
- **Inter-action timing**: humans have irregular pacing; bots are metronomic
- **Idle periods**: humans pause to read, think, distract; bots don't idle
- **Navigation patterns**: humans backtrack, re-read; bots move linearly
- **Session duration**: too short = suspicious; too regular = suspicious

```python
import random
import asyncio

async def session_pause(context: str = "thinking"):
    """
    Context-aware pauses that match human cognitive patterns.
    Context: 'thinking' | 'reading' | 'loading' | 'distracted'
    """
    pauses = {
        "thinking":   (0.5, 2.5),   # deciding what to do next
        "reading":    (1.5, 6.0),   # reading content
        "loading":    (0.3, 1.0),   # waiting for page response
        "distracted": (3.0, 12.0),  # tab switching, phone check
    }
    lo, hi = pauses.get(context, (0.5, 2.0))
    await asyncio.sleep(random.uniform(lo, hi))


async def session_warmup(page):
    """
    Warmup behavior after page load before taking action.
    Simulates: page scan, scroll to orient, mouse wander.
    DO NOT skip — jumping straight to target element is a strong bot signal.
    """
    # Initial scan pause
    await asyncio.sleep(random.uniform(0.8, 2.0))
    
    # Light scroll to scan content
    scroll_amt = random.randint(100, 300)
    await human_scroll(page, "down", scroll_amt, read_pause=False)
    await asyncio.sleep(random.uniform(0.4, 1.2))
    
    # Random mouse wander (looking around)
    vp = await page.evaluate("() => ({w: window.innerWidth, h: window.innerHeight})")
    for _ in range(random.randint(1, 3)):
        rx = random.uniform(0.2, 0.8) * vp["w"]
        ry = random.uniform(0.2, 0.8) * vp["h"]
        await human_move(page, rx, ry, target_w=50, overshoot=False)
        await asyncio.sleep(random.uniform(0.3, 1.0))


async def random_idle_action(page):
    """
    Occasionally inject idle-like micro-behaviors between real actions.
    Call this randomly during long sessions (20% chance per major action).
    """
    action = random.choice([
        "scroll_small", "mouse_wander", "pause_long"
    ])
    
    if action == "scroll_small":
        d = random.choice(["up", "down"])
        amt = random.randint(30, 100)
        await human_scroll(page, d, amt, read_pause=False)
    
    elif action == "mouse_wander":
        vp = await page.evaluate("() => ({w: window.innerWidth, h: window.innerHeight})")
        rx = random.uniform(0.1, 0.9) * vp["w"]
        ry = random.uniform(0.1, 0.9) * vp["h"]
        await human_move(page, rx, ry, overshoot=False)
    
    elif action == "pause_long":
        await session_pause("distracted")
```

---

## Layer 6: Complete Interaction Pattern

This is the correct order for any interaction:

```python
async def interact_with_form(page, form_data: dict):
    """
    Example: full humanized form submission flow.
    Every step uses the layers above.
    Replace selectors with your application's actual elements.
    """
    # 1. Warmup after navigation
    await session_warmup(page)
    
    # 2. Find target element — scroll to locate if needed
    target_btn = page.get_by_role("button", name="Submit")
    await session_pause("thinking")
    
    # 3. Move + click with full humanization
    box = await target_btn.bounding_box()
    await human_move(page, box["x"] + box["width"]/2, box["y"] + box["height"]/2,
                     target_w=box["width"])
    await asyncio.sleep(random.uniform(0.05, 0.15))
    await target_btn.click()
    
    # 4. Pause after interaction (reading response)
    await session_pause("reading")
    
    # 5. Type into input with keystroke dynamics
    text_input = page.get_by_placeholder("Enter your text")
    await human_type(page, text_input, form_data.get("text", ""), wpm=55)
    
    # 6. Review pause (re-reading what was typed)
    await session_pause("reading")
    
    # 7. Occasional idle action before submitting
    if random.random() < 0.3:
        await random_idle_action(page)
    
    # 8. Submit — thinking pause before committing
    await session_pause("thinking")
    submit_btn = page.get_by_role("button", name="Confirm")
    box2 = await submit_btn.bounding_box()
    await human_move(page, box2["x"] + box2["width"]/2, box2["y"] + box2["height"]/2,
                     target_w=box2["width"])
    await asyncio.sleep(random.uniform(0.1, 0.3))
    await submit_btn.click()
    
    # 9. Post-action pause (watching result)
    await session_pause("loading")
```

---

## What NOT to Do

```python
# ❌ Instant teleport — strongest bot signal
await page.mouse.move(500, 300)

# ❌ Uniform timing — wrong statistical distribution
for char in text:
    await page.keyboard.type(char)
    await asyncio.sleep(0.1)  # constant = detected

# ❌ Click center every time
await elem.click()  # Playwright defaults to center — real humans don't

# ❌ time.sleep() in async code
import time; time.sleep(1)  # blocks event loop

# ❌ No warmup — jumping straight to target
await page.goto(url)
await page.get_by_role("button", name="Submit").click()  # immediate = bot

# ❌ Identical sessions — same sequence every run
# Vary your scroll amounts, pause durations, idle behaviors each run

# ❌ random.uniform() for all timing — flat distribution ≠ human
# Use random.gauss() for timing — humans have Gaussian timing, not uniform
```

---

## Dependencies

```bash
uv add numpy  # only for advanced jitter (can replace with random.gauss)
```

No external humanization library needed — this skill IS the implementation.

---

## Read Next
- `references/detection-signals.md` — what 2026 ML detectors measure (know your enemy)
- `references/math.md` — Bézier, Fitts's Law, and Gaussian derivations
