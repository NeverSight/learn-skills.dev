---
name: stimulus-coder
description: Use when creating or refactoring Stimulus controllers. Applies Hotwire conventions, controller design patterns, targets/values usage, action handling, and JavaScript best practices.
allowed-tools: Read Write Edit Grep Glob Bash
---

# Stimulus Coder

**Audience:** Developers building interactive UIs with Stimulus.js and Hotwire.

**Goal:** Write maintainable Stimulus controllers where state lives in HTML and controllers add behavior.

## Core Concepts

- **Controllers** attach behavior to HTML elements
- **Actions** respond to DOM events
- **Targets** reference important elements
- **Values** manage state through data attributes

## Controller Design Principles

### Keep Controllers Small and Reusable

```javascript
// Good: Generic, reusable controller
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["content"]
  static values = { open: Boolean }

  toggle() { this.openValue = !this.openValue }

  openValueChanged() {
    this.contentTarget.classList.toggle("hidden", !this.openValue)
  }
}
```

### Use Data Attributes for Configuration

```javascript
export default class extends Controller {
  static values = {
    delay: { type: Number, default: 300 },
    event: { type: String, default: "input" }
  }

  connect() {
    this.element.addEventListener(this.eventValue, this.submit.bind(this))
  }

  submit() {
    clearTimeout(this.timeout)
    this.timeout = setTimeout(() => this.element.requestSubmit(), this.delayValue)
  }
}
```

```erb
<%= form_with data: { controller: "auto-submit", auto_submit_delay_value: 500 } %>
```

### Compose Multiple Controllers

```erb
<div data-controller="toggle clipboard" data-toggle-open-value="false">
  <button data-action="toggle#toggle">Show</button>
  <div data-toggle-target="content" class="hidden">
    <code data-clipboard-target="source">secret-code</code>
    <button data-action="clipboard#copy">Copy</button>
  </div>
</div>
```

## Targets and Values

### Targets for Element References

```javascript
export default class extends Controller {
  static targets = ["tab", "panel"]
  static values = { index: { type: Number, default: 0 } }

  select(event) { this.indexValue = this.tabTargets.indexOf(event.currentTarget) }

  indexValueChanged() {
    this.panelTargets.forEach((panel, i) => panel.classList.toggle("hidden", i !== this.indexValue))
    this.tabTargets.forEach((tab, i) => tab.setAttribute("aria-selected", i === this.indexValue))
  }
}
```

## Action Handling

```erb
<button data-action="click->toggle#toggle">Toggle</button>
<input data-action="input->search#update focus->search#expand">
<button data-action="modal#open" data-modal-id-param="confirm-dialog">Open</button>
<input data-action="keydown.enter->form#submit keydown.escape->form#cancel">
```

### Action Parameters

```javascript
open(event) {
  const modalId = event.params.id
  document.getElementById(modalId)?.showModal()
}
```

## Common Controller Patterns

### Dropdown Controller

```javascript
export default class extends Controller {
  static targets = ["menu"]
  static values = { open: Boolean }

  toggle() { this.openValue = !this.openValue }

  close(event) {
    if (!this.element.contains(event.target)) this.openValue = false
  }

  openValueChanged() {
    this.menuTarget.classList.toggle("hidden", !this.openValue)
    if (this.openValue) document.addEventListener("click", this.close.bind(this), { once: true })
  }
}
```

### Clipboard Controller

```javascript
export default class extends Controller {
  static targets = ["source", "button"]
  static values = { successMessage: { type: String, default: "Copied!" } }

  async copy() {
    const text = this.sourceTarget.value || this.sourceTarget.textContent
    await navigator.clipboard.writeText(text)
    this.showSuccess()
  }

  showSuccess() {
    const original = this.buttonTarget.textContent
    this.buttonTarget.textContent = this.successMessageValue
    setTimeout(() => this.buttonTarget.textContent = original, 2000)
  }
}
```

## Turbo Integration

```javascript
export default class extends Controller {
  connect() {
    document.addEventListener("turbo:before-visit", this.dismiss.bind(this))
    this.timeout = setTimeout(() => this.dismiss(), 5000)
  }

  disconnect() { clearTimeout(this.timeout) }
  dismiss() { this.element.remove() }
}
```

## Architecture Patterns

### Make Controllers Configurable

Externalize hardcoded values into data attributes. Never embed CSS classes, selectors, or thresholds in controller logic.

```javascript
// Bad: hardcoded
export default class extends Controller {
  toggle() { this.element.classList.toggle("hidden") }
}

// Good: configurable
export default class extends Controller {
  static classes = ["toggle"]
  toggle() { this.element.classList.toggle(this.toggleClass) }
}
```

### Mixins Over Deep Inheritance

Use mixins when behavior is shared but doesn't represent specialization.

Decision framework:
- **"is a"** → inheritance (class extends BaseController)
- **"acts as"** → mixin (apply behavior at connect)
- **"has a"** → composition (separate controller + outlets)

```javascript
// Mixin pattern
const Sortable = (controller) => {
  const original = controller.prototype.connect
  controller.prototype.connect = function() {
    if (original) original.call(this)
    this.sortable = new Sortable(this.element, this.sortableOptions)
  }
}
```

### Targetless Controllers

If a controller mixes element-level and target-level concerns, split it. Controller acting on `this.element` is one responsibility; acting on targets is another.

Communicate between split controllers via custom events or outlets.

### Namespaced Attributes

For flexible parameter sets without explicitly defining each value:

```javascript
// Read arbitrary data-chart-* attributes
get chartOptions() {
  return Object.entries(this.element.dataset)
    .filter(([key]) => key.startsWith("chart"))
    .reduce((opts, [key, val]) => {
      opts[key.replace("chart", "").toLowerCase()] = val
      return opts
    }, {})
}
```

See [architecture-patterns.md](references/architecture-patterns.md) for SOLID principles applied to Stimulus.

## Controller Communication

Choose pattern based on coupling needs:

| Pattern | Coupling | Direction | Use When |
|---------|----------|-----------|----------|
| Custom events | Loose | Broadcast (1→many) | Sender doesn't know receivers |
| Outlets | Structured | Direct (1→1, 1→few) | Known relationships in layout |
| Callbacks | Read-only | Request/response | Sharing state without triggering actions |

### Custom Events (Preferred Default)

```javascript
// Sender
this.dispatch("submitted", { detail: { id: this.idValue }, bubbles: true })

// Receiver (in HTML)
// data-action="sender:submitted->receiver#handleSubmit"
```

Rules:
- Always set `bubbles: true` for cross-controller events
- Namespace event names: `form:submitted`, `cart:updated`
- Document the `detail` contract

### Outlets (Structured Relationships)

```javascript
export default class extends Controller {
  static outlets = ["result"]

  search() {
    const results = this.performSearch()
    this.resultOutlets.forEach(outlet => outlet.update(results))
  }

  resultOutletConnected(outlet) { /* setup */ }
  resultOutletDisconnected(outlet) { /* cleanup */ }
}
```

## Lifecycle Best Practices

### Don't Overuse `connect()`

`connect()` is for **third-party plugin initialization only**. Not for state setup (use Values API) or event listeners (use `data-action`).

```javascript
// Good: plugin init in connect
connect() {
  this.chart = new Chart(this.canvasTarget, this.chartConfig)
}

disconnect() {
  this.chart.destroy()
  this.chart = null
}
```

### Always Pair connect/disconnect

Every resource acquired in `connect()` must be released in `disconnect()`. Controllers can connect/disconnect multiple times during Turbo navigation.

### Turbo Cache Teardown

Prevent "flash of manipulated content" when cached pages return:

```javascript
connect() {
  document.addEventListener("turbo:before-cache", this.teardown.bind(this))
  this.slider = new Swiper(this.element, this.config)
}

teardown() {
  this.slider?.destroy()
  // Restore original DOM state before caching
}

disconnect() {
  this.teardown()
}
```

## Event Listener Hygiene

### Store Bound References

`.bind()` creates a new function each call. Store the reference for proper removal:

```javascript
connect() {
  this.boundResize = this.resize.bind(this)
  window.addEventListener("resize", this.boundResize, { passive: true })
}

disconnect() {
  window.removeEventListener("resize", this.boundResize)
}
```

### Prefer Declarative Actions

```erb
<%# Good: Stimulus manages lifecycle %>
<div data-controller="search"
     data-action="resize@window->search#layout keydown.escape@window->search#close">

<%# Bad: manual addEventListener in connect() %>
```

Global events use `@window` or `@document` suffix in `data-action`.

See [lifecycle-and-events.md](references/lifecycle-and-events.md) for complete patterns.

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Creating DOM extensively | Fighting Stimulus philosophy | Let server render HTML |
| Storing state in JS | State lost on navigation | Use Values in HTML |
| Over-specific controllers | Not reusable | Design generic behaviors |
| Manual querySelector | Fragile, bypasses Stimulus | Use targets |
| Inline event handlers | Unmaintainable | Use data-action |
| Overloading connect() | Bloated, mixes concerns | Values for state, data-action for events |
| Tight controller coupling | Fragile, hard to test | Custom events or outlets |
| Missing disconnect cleanup | Memory leaks, duplicate listeners | Always pair connect/disconnect |
| Unbound event references | Can't removeEventListener | Store `.bind()` result |

## Output Format

When creating Stimulus controllers, provide:

1. **Controller** - Complete JavaScript implementation
2. **HTML Example** - Sample markup showing usage
3. **Configuration** - Available values and targets
4. **Integration** - How it works with Turbo if applicable
