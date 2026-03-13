---
name: hytopia-mobile
description: Helps implement mobile support in HYTOPIA SDK games. Use when users need touch controls, mobile UI, device detection, or cross-platform compatibility. Covers mobile controls, touch input, and responsive UI.
---

# HYTOPIA Mobile Support

This skill helps you implement mobile support in HYTOPIA SDK games.

**Documentation:** https://dev.hytopia.com/sdk-guides/mobile

## When to Use This Skill

Use this skill when the user:

- Wants to add mobile controls to their game
- Needs to detect mobile devices
- Asks about touch input handling
- Wants to create responsive UI for mobile
- Needs cross-platform compatibility
- Asks about mobile-specific button layouts

## Mobile Basics

### Automatic Features

HYTOPIA handles automatically:
- Cross-platform play (mobile + desktop together)
- Game state consistency across devices
- Movement joystick (left 40% of screen)
- Camera control (right 60% of screen)
- Landscape orientation enforcement

### What You Must Implement

- Custom action buttons (shoot, jump, interact)
- Mobile-optimized UI sizing
- Touch-friendly button layouts

## Mobile Detection

### CSS Detection

HYTOPIA adds `.mobile` class to `<body>` on mobile devices:

```css
/* Desktop-only styles */
.desktop-controls {
  display: block;
}

/* Hide desktop controls on mobile */
body.mobile .desktop-controls {
  display: none;
}

/* Mobile-only styles */
.mobile-controls {
  display: none;
}

body.mobile .mobile-controls {
  display: flex;
}
```

### JavaScript Detection

```typescript
// Check if running on mobile
if (hytopia.isMobile) {
  setupMobileUI();
} else {
  setupDesktopUI();
}

// Conditional logic
function showControls() {
  if (hytopia.isMobile) {
    showTouchButtons();
  } else {
    showKeyboardHints();
  }
}
```

## Mobile Controls

### Input Simulation

Use `hytopia.pressInput()` to simulate keyboard/mouse input:

```typescript
// Simulate key press
hytopia.pressInput('space', true);   // Key down
hytopia.pressInput('space', false);  // Key up

// Simulate mouse click
hytopia.pressInput('ml', true);   // Left mouse down
hytopia.pressInput('ml', false);  // Left mouse up
hytopia.pressInput('mr', true);   // Right mouse down
```

### Creating Mobile Buttons

```html
<script>
  // Jump button
  const jumpBtn = document.getElementById('jump-btn');

  jumpBtn.addEventListener('touchstart', (e) => {
    e.preventDefault();  // Prevent default touch behavior
    jumpBtn.classList.add('active');
    hytopia.pressInput(' ', true);  // Space key
  });

  jumpBtn.addEventListener('touchend', (e) => {
    e.preventDefault();
    jumpBtn.classList.remove('active');
    hytopia.pressInput(' ', false);
  });

  // Attack button
  const attackBtn = document.getElementById('attack-btn');

  attackBtn.addEventListener('touchstart', (e) => {
    e.preventDefault();
    attackBtn.classList.add('active');
    hytopia.pressInput('ml', true);  // Left click
  });

  attackBtn.addEventListener('touchend', (e) => {
    e.preventDefault();
    attackBtn.classList.remove('active');
    hytopia.pressInput('ml', false);
  });
</script>
```

### Complete Mobile Control Layout

```html
<div class="mobile-controls">
  <a id="interact-btn" class="mobile-button">
    <img src="{{CDN_ASSETS_URL}}/icons/interact.png" />
  </a>

  <a id="jump-btn" class="mobile-button">
    <img src="{{CDN_ASSETS_URL}}/icons/jump.png" />
  </a>

  <a id="attack-btn" class="mobile-button">
    <img src="{{CDN_ASSETS_URL}}/icons/attack.png" />
  </a>
</div>

<style>
  .mobile-controls {
    display: none;
  }

  body.mobile .mobile-controls {
    display: flex;
    gap: 14px;
    position: fixed;
    bottom: 40px;
    right: 40px;
  }

  .mobile-button {
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .mobile-button img {
    width: 24px;
    height: 24px;
    filter: invert(1);
  }

  .mobile-button.active {
    transform: scale(0.92);
    background-color: rgba(0, 0, 0, 0.75);
  }
</style>

<script>
  document.querySelectorAll('.mobile-button').forEach(btn => {
    const input = btn.dataset.input;

    btn.addEventListener('touchstart', (e) => {
      e.preventDefault();
      btn.classList.add('active');
      hytopia.pressInput(input, true);
    });

    btn.addEventListener('touchend', (e) => {
      e.preventDefault();
      btn.classList.remove('active');
      hytopia.pressInput(input, false);
    });
  });
</script>
```

## Responsive UI Design

### Scaling for Mobile

```css
/* Base UI */
.game-hud {
  font-size: 16px;
  padding: 10px;
}

/* Larger touch targets on mobile */
body.mobile .game-hud {
  font-size: 20px;
  padding: 16px;
}

/* Minimum touch target size: 44x44px */
body.mobile button,
body.mobile .touchable {
  min-width: 44px;
  min-height: 44px;
}
```

### Hiding Desktop Elements

```css
/* Keyboard hints - desktop only */
.keyboard-hint {
  display: inline-block;
}

body.mobile .keyboard-hint {
  display: none;
}

/* Simplify mobile UI */
body.mobile .detailed-stats {
  display: none;
}

body.mobile .simple-stats {
  display: block;
}
```

### Safe Areas

```css
/* Account for notches and rounded corners */
body.mobile .mobile-controls {
  padding-bottom: env(safe-area-inset-bottom, 20px);
  padding-right: env(safe-area-inset-right, 20px);
}
```

## Testing Mobile UI

### Browser Developer Tools

1. Open game at play.hytopia.com
2. Open Developer Tools (View → Developer Tools or right-click → Inspect)
3. Click mobile device icon in dev tools toolbar
4. Switch to landscape mode
5. Refresh the page (required for mobile detection)

### Testing Checklist

- [ ] Buttons are large enough (44px minimum)
- [ ] Buttons don't overlap joystick area (left 40%)
- [ ] UI readable in landscape
- [ ] Touch feedback visible (active states)
- [ ] No accidental touches on UI while playing
- [ ] Important info visible above action buttons

## Best Practices

1. **Design desktop first** - Then adapt for mobile
2. **Use e.preventDefault()** - Prevents unwanted browser behavior
3. **Large touch targets** - Minimum 44x44px for buttons
4. **Visual feedback** - Show active/pressed states
5. **Right side placement** - Action buttons on right 60% of screen
6. **Avoid overlapping** - Don't place UI over joystick/camera areas
7. **Test on device** - Browser simulation isn't perfect

## Common Input Keys

| Input | Key |
|-------|-----|
| Space/Jump | `' '` (space) |
| Left Click | `'ml'` |
| Right Click | `'mr'` |
| WASD | `'w'`, `'a'`, `'s'`, `'d'` |
| Interact | `'e'` |
| Reload | `'r'` |
| Sprint | `'shift'` |

## Common Mistakes

- Forgetting `e.preventDefault()` in touch handlers
- Making buttons too small for fingers
- Placing buttons over joystick area
- Not testing on actual mobile devices
- Forgetting to refresh after enabling device simulation
