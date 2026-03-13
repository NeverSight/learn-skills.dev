---
name: ionic-components
description: Use Ionic Framework UI components instead of custom HTML/CSS when building interfaces. Prefer ion- tags, use Ionic CSS variables for colors, use Ionicons for icons, and only fall back to custom styles when no Ionic equivalent exists.
---

# Ionic Components Skill

## Component Priority
When building any UI element, always prefer Ionic components over custom HTML/CSS.

1. **Check Ionic first** — before creating any UI block, verify if an Ionic component
   exists for the use case
2. **Use Ionic component** if available — with proper `ion-` tags and Ionic properties
3. **Custom HTML/CSS only** if Ionic has no equivalent component or lacks required functionality

## Component Properties (Angular)

### String properties — без скобок
```html
<ion-button expand="block" fill="outline" color="primary">Submit</ion-button>
<ion-input type="email" label="Email" placeholder="Enter email"></ion-input>
<ion-icon name="heart-outline" size="large"></ion-icon>
```

### Boolean properties — ALWAYS use square brackets
Boolean without brackets is always treated as `true`, even if the value is `"false"`.

```html
<!-- ✅ Correct -->
<ion-button [disabled]="isLoading">Submit</ion-button>
<ion-input [readonly]="isReadonly" [clearInput]="true"></ion-input>
<ion-checkbox [checked]="isChecked" [indeterminate]="false"></ion-checkbox>
<ion-toggle [checked]="isEnabled" [disabled]="false"></ion-toggle>
<ion-list [inset]="true"></ion-list>

<!-- ❌ Wrong — string "false" is still treated as true -->
<ion-button disabled="false">Submit</ion-button>
<ion-input readonly="false"></ion-input>
```

### Dynamic values — всегда в квадратных скобках
```html
<ion-badge [color]="badgeColor">{{ count }}</ion-badge>
<ion-icon [name]="iconName"></ion-icon>
<ion-button [expand]="isFullWidth ? 'block' : undefined">Click</ion-button>
```

### Events — в круглых скобках
```html
<ion-button (click)="onSubmit()">Submit</ion-button>
<ion-input (ionChange)="onChange($event)" (ionBlur)="onBlur()"></ion-input>
<ion-toggle (ionChange)="onToggle($event)"></ion-toggle>
<ion-refresher (ionRefresh)="doRefresh($event)">
  <ion-refresher-content></ion-refresher-content>
</ion-refresher>
```

### Rule
| Type | Syntax | Example |
|------|--------|---------|
| String (static) | `attr="value"` | `color="primary"` |
| Boolean | `[attr]="value"` | `[disabled]="true"` |
| Number | `[attr]="value"` | `[min]="0"` |
| Dynamic / variable | `[attr]="variable"` | `[color]="myColor"` |
| Event | `(event)="handler()"` | `(ionChange)="fn()"` |

---

## Looking Up Components
When unsure if an Ionic component exists or how to use it:
1. **Context7 first** (if available) — resolve `ionic` and fetch relevant docs
2. **Fallback** — check https://ionicframework.com/docs/components directly

---

## Icons — Ionicons
Always use Ionicons for icons. Browse available icons at https://ionic.io/ionicons

### Setup
If using Ionic Framework — Ionicons is included by default, no setup needed.

Without Ionic Framework, add before closing `</body>`:
```html
<script type="module" src="https://unpkg.com/ionicons@latest/dist/ionicons/ionicons.esm.js"></script>
<script nomodule src="https://unpkg.com/ionicons@latest/dist/ionicons/ionicons.js"></script>
```

### Basic Usage
```html
<ion-icon name="heart"></ion-icon>
```

### Variants
Each icon has three variants:
```html
<ion-icon name="heart"></ion-icon>          <!-- filled (default) -->
<ion-icon name="heart-outline"></ion-icon>  <!-- outline -->
<ion-icon name="heart-sharp"></ion-icon>    <!-- sharp -->
```

Use `outline` for iOS-style, `sharp` for MD/Android-style, or let the platform decide:
```html
<ion-icon ios="heart-outline" md="heart-sharp"></ion-icon>
```

### Size
```html
<ion-icon name="heart" size="small"></ion-icon>
<ion-icon name="heart" size="large"></ion-icon>
```

Or via CSS (use multiples of 8):
```css
ion-icon {
  font-size: 32px;
}
```

### Color
Use Ionic CSS variables:
```css
ion-icon {
  color: var(--ion-color-primary);
}
```

### Stroke Width (outline variant only)
```css
ion-icon {
  --ionicon-stroke-width: 16px; /* default is 32px */
}
```

### Icon Slots
`ion-icon` uses the `slot` attribute to position itself **inside** a parent component.

| Slot | Parent | Effect |
|------|--------|--------|
| `slot="start"` | `ion-button`, `ion-item`, `ion-input`, `ion-select` | Icon on the left side |
| `slot="end"` | `ion-button`, `ion-item`, `ion-input`, `ion-select` | Icon on the right side |
| `slot="icon-only"` | `ion-button` | Icon fills the button — no text, larger tap target, adjusted sizing |

#### slot="start" and slot="end"
```html
<!-- ion-button -->
<ion-button>
  <ion-icon slot="start" name="log-in-outline" aria-hidden="true"></ion-icon>
  Login
</ion-button>

<ion-button>
  Next
  <ion-icon slot="end" name="arrow-forward-outline" aria-hidden="true"></ion-icon>
</ion-button>

<!-- ion-input -->
<ion-input label="Search" placeholder="Type to search...">
  <ion-icon slot="start" name="search-outline" aria-hidden="true"></ion-icon>
</ion-input>

<!-- ion-select -->
<ion-select label="Country">
  <ion-icon slot="start" name="globe-outline" aria-hidden="true"></ion-icon>
  <ion-select-option value="us">United States</ion-select-option>
  <ion-select-option value="uk">United Kingdom</ion-select-option>
</ion-select>
```

#### slot="icon-only"
Use when the button contains only an icon and no text. Ionic automatically applies correct sizing and padding.
```html
<!-- Correct: icon-only button in toolbar -->
<ion-buttons slot="end">
  <ion-button aria-label="Search">
    <ion-icon slot="icon-only" name="search-outline"></ion-icon>
  </ion-button>
  <ion-button aria-label="More options">
    <ion-icon slot="icon-only" name="ellipsis-vertical"></ion-icon>
  </ion-button>
</ion-buttons>
```

❌ Don't use `slot="icon-only"` without text when there's text next to the icon — use `slot="start"` or `slot="end"` instead.
```html
<!-- Wrong -->
<ion-button>
  <ion-icon slot="icon-only" name="add-outline"></ion-icon>
  Add Item
</ion-button>

<!-- Correct -->
<ion-button>
  <ion-icon slot="start" name="add-outline" aria-hidden="true"></ion-icon>
  Add Item
</ion-button>
```

### Accessibility
Decorative icons — hide from assistive technology:
```html
<ion-icon name="heart" aria-hidden="true"></ion-icon>
```

Interactive icons — add a label:
```html
<ion-icon name="heart" aria-label="Favorite"></ion-icon>
```

Icon inside a button — label the button, hide the icon:
```html
<ion-button aria-label="Favorite">
  <ion-icon name="heart" aria-hidden="true"></ion-icon>
</ion-button>
```

### Icon in ion-item
```html
<ion-item>
  <ion-icon name="person-outline" slot="start" aria-hidden="true"></ion-icon>
  <ion-label>Profile</ion-label>
</ion-item>
```

---

## Slots
Slots are used to position content inside Ionic components. Always use the correct slot for the component context.

### Universal Slots (most components)
| Slot | Position |
|------|----------|
| `start` | Left side in LTR, right side in RTL |
| `end` | Right side in LTR, left side in RTL |

### ion-button Slots
| Slot | Usage |
|------|-------|
| *(default)* | Button label text |
| `start` | Icon or content before text |
| `end` | Icon or content after text |
| `icon-only` | Icon with no text — adjusts sizing automatically |

```html
<!-- Icon before text -->
<ion-button>
  <ion-icon slot="start" name="arrow-back-outline" aria-hidden="true"></ion-icon>
  Back
</ion-button>

<!-- Icon after text -->
<ion-button>
  Continue
  <ion-icon slot="end" name="arrow-forward-outline" aria-hidden="true"></ion-icon>
</ion-button>

<!-- Icon only — no text -->
<ion-button aria-label="Search">
  <ion-icon slot="icon-only" name="search-outline"></ion-icon>
</ion-button>
```

### ion-item Slots
| Slot | Usage |
|------|-------|
| *(default)* | Main content (label, input, etc.) |
| `start` | Decorative visuals — icon, avatar, thumbnail |
| `end` | Actions or metadata — toggle, badge, timestamp |

```html
<!-- Icon on the left, toggle on the right -->
<ion-item>
  <ion-icon name="notifications-outline" slot="start" aria-hidden="true"></ion-icon>
  <ion-label>Notifications</ion-label>
  <ion-toggle slot="end"></ion-toggle>
</ion-item>

<!-- Avatar on the left, badge on the right -->
<ion-item>
  <ion-avatar slot="start">
    <img src="avatar.jpg" alt="User" />
  </ion-avatar>
  <ion-label>John Doe</ion-label>
  <ion-badge slot="end" color="primary">3</ion-badge>
</ion-item>
```

### ion-toolbar Slots
| Slot | Position | iOS | MD |
|------|----------|-----|----|
| `start` | Left | Left | Left |
| `end` | Right | Right | Right |
| `primary` | Action side | Right | Right |
| `secondary` | Secondary side | Left | Right (after primary) |
| `content` | Center | Center | Center |

```html
<ion-toolbar>
  <ion-buttons slot="start">
    <ion-back-button></ion-back-button>
  </ion-buttons>

  <ion-title>Page Title</ion-title>

  <ion-buttons slot="end">
    <ion-button aria-label="Search">
      <ion-icon slot="icon-only" name="search-outline"></ion-icon>
    </ion-button>
  </ion-buttons>
</ion-toolbar>
```

### ion-fab-button Slots
| Slot | Usage |
|------|-------|
| *(default)* | Icon inside the FAB button |

```html
<ion-fab slot="fixed" vertical="bottom" horizontal="end">
  <ion-fab-button>
    <ion-icon name="add-outline"></ion-icon>
  </ion-fab-button>
</ion-fab>
```

### Common Mistakes
❌ Using `slot="icon-only"` outside of a button
❌ Using `slot="start"` on text content in `ion-item` (use default slot)
❌ Placing `ion-buttons` directly in `ion-toolbar` without a slot
❌ Using `slot="fixed"` anywhere other than `ion-content`

---

## Ionic CSS Variables
Never use hardcoded colors. Always use Ionic CSS variables:

Common variables:
- `--ion-color-primary`, `--ion-color-secondary`, `--ion-color-tertiary`
- `--ion-color-success`, `--ion-color-warning`, `--ion-color-danger`
- `--ion-color-light`, `--ion-color-medium`, `--ion-color-dark`
- `--ion-background-color`, `--ion-text-color`
- `--ion-font-family`

## Custom Styles
If custom styles are needed:
- Use Ionic CSS variables for all colors and typography
- Follow Ionic's spacing scale where possible
- Scope styles to component to avoid conflicts

---

## Examples

### Button
✅ Correct:
```html
<ion-button expand="block" color="primary">Submit</ion-button>
<ion-button fill="outline" color="danger">Delete</ion-button>
```
❌ Incorrect:
```html
<button style="background: #3880ff; color: white; width: 100%">Submit</button>
```

### Input
✅ Correct:
```html
<ion-input label="Email" type="email" placeholder="Enter email"></ion-input>
<ion-textarea label="Message" rows="4"></ion-textarea>
```
❌ Incorrect:
```html
<input type="email" placeholder="Email" class="my-input" />
```

### List
✅ Correct:
```html
<ion-list>
  <ion-item>
    <ion-label>Item 1</ion-label>
  </ion-item>
  <ion-item>
    <ion-icon name="person-outline" slot="start" aria-hidden="true"></ion-icon>
    <ion-label>Item with icon</ion-label>
  </ion-item>
</ion-list>
```
❌ Incorrect:
```html
<ul class="my-list">
  <li>Item 1</li>
</ul>
```

### Card
✅ Correct:
```html
<ion-card>
  <ion-card-header>
    <ion-card-title>Title</ion-card-title>
    <ion-card-subtitle>Subtitle</ion-card-subtitle>
  </ion-card-header>
  <ion-card-content>
    Content goes here
  </ion-card-content>
</ion-card>
```
❌ Incorrect:
```html
<div class="card" style="border-radius: 8px; box-shadow: ...">
  <div class="card-title">Title</div>
</div>
```

### Colors
✅ Correct:
```css
color: var(--ion-color-primary);
background: var(--ion-color-light);
border-color: var(--ion-color-medium);
```
❌ Incorrect:
```css
color: #3880ff;
background: #f4f5f8;
border-color: #92949c;
```

### Icons
✅ Correct:
```html
<!-- Decorative -->
<ion-icon name="star-outline" aria-hidden="true"></ion-icon>

<!-- Interactive -->
<ion-icon name="close" aria-label="Close dialog"></ion-icon>

<!-- In button -->
<ion-button aria-label="Add item">
  <ion-icon name="add-outline" aria-hidden="true"></ion-icon>
</ion-button>
```
❌ Incorrect:
```html
<img src="./icons/star.png" />
<i class="fa fa-star"></i>
```
