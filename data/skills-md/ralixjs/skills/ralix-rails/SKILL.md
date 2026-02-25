---
name: ralix-rails
description: Develop frontend code using Ralix microframework in Ruby on Rails projects. Use when creating controllers, components, helpers, templates, or working with Ralix patterns, route-based controllers, component lifecycle, Ralix helpers (find, findAll, findParent, findParents, on, elem, addClass, removeClass, toggleClass, hasClass, attr, data, style, removeAttr, removeData, insertHTML, sanitize, render, insertTemplate, visit, back, reload, currentUrl, getParam, setParam, get, post, ajax, serialize, submit, currentElement, currentEvent), or integrating Ralix with Rails UJS and Turbolinks/Turbo.
---

# Ralix for Ruby on Rails

Comprehensive guide for mastering Ralix microframework - a lightweight JavaScript framework that enhances server-rendered Rails frontends with route-based controllers, reusable components, and utility helpers.

## When to Use This Skill

- Building frontend features in Rails applications
- Creating route-based page controllers
- Implementing reusable UI components
- Working with Turbolinks/Turbo navigation
- Integrating JavaScript with Rails UJS
- Enhancing server-rendered HTML with minimal JavaScript
- Organizing frontend code in Rails projects
- Migrating from jQuery to modern JavaScript patterns
- Building progressive enhancement features
- Creating modal dialogs, tooltips, and interactive widgets

## Architecture Overview

Ralix organizes frontend code into three main concepts:

1. **Controllers**: Route-based classes that handle page-specific logic
2. **Components**: Reusable UI components with lifecycle hooks
3. **Helpers**: Utility functions for DOM manipulation, events, AJAX, and navigation

Ralix follows a "just enough JavaScript" philosophy - it enhances server-rendered HTML without taking over the entire frontend.

## Installation and Setup

### Installation

```bash
# Using npm
npm install ralix

# Using Yarn
yarn add ralix
```

### Application Setup

Ralix is initialized in `app/javascript/application.js`:

```javascript
// Dependencies
import Rails from '@rails/ujs'
import Turbolinks from 'turbolinks'
import { RalixApp } from 'ralix'

// Controllers
import AppCtrl from './controllers/app'
import PatientsCtrl from './controllers/patients'
import PatientsShowCtrl from './controllers/patients_show'

// Components with auto-start
import FlashMessages from './components/flash_messages'
import ViewportHeight from './components/viewport_height'

// Templates
import * as Templates from './templates'

const App = new RalixApp({
  rails_ujs: Rails,
  routes: {
    '/patients': PatientsCtrl,
    '/patients/([0-9]+)': PatientsShowCtrl,
    '/.*': AppCtrl  // Default/fallback route
  },
  components: [
    FlashMessages,
    ViewportHeight
  ],
  templates: Templates
})

Rails.start()
Turbolinks.start()
App.start()
```

### Minimal Setup (Helpers Only)

If you only need Ralix helpers without controllers or components:

```javascript
import { RalixApp } from 'ralix'

const App = new RalixApp()
App.start()
```

### Global App Access

The `App` object is exposed globally via `window.App`. Access the current controller:

```javascript
// Get current controller instance
const currentCtrl = App.ctrl

// Call controller methods
App.ctrl.goBack()
App.ctrl.toggleMenu()
```

## Controllers

Controllers are route-based classes that handle page-specific logic. They're instantiated when their route matches the current URL.

### 1. Basic Controller Structure

```javascript
// app/javascript/controllers/patients.js

export default class PatientsCtrl {
  constructor() {
    // Initialize on route match
    this.setupEventListeners()
    this.initializeState()
  }

  setupEventListeners() {
    on('.patient-card', 'click', (e) => {
      const patientId = data(e.currentTarget, 'patient-id')
      this.showPatientDetails(patientId)
    })
  }

  initializeState() {
    this.selectedPatient = null
  }

  showPatientDetails(id) {
    visit(`/patients/${id}`)
  }
}
```

### 2. Controller Inheritance

Controllers should inherit from a main controller (AppCtrl, MainCtrl, etc.) to share common functionality:

```javascript
// app/javascript/controllers/app.js

export default class AppCtrl {
  goBack() {
    back()
  }

  toggleMenu() {
    toggleClass('#menu', 'hidden')
  }

  displayFlashMessage(type, message) {
    insertHTML('body', render('flashMessage', {
      type,
      message,
      id: Date.now()
    }), 'end')
  }
}
```

```javascript
// app/javascript/controllers/camera.js

import AppCtrl from './app'

export default class CameraCtrl extends AppCtrl {
  constructor() {
    super()
    this.setupCamera()
  }

  setupCamera() {
    // Camera-specific initialization
  }

  // Override parent method
  goBack() {
    visit('/dashboard')
  }
}
```

### 3. Route Patterns

Routes use regular expressions to match URLs:

```javascript
routes: {
  '/dashboard': DashboardCtrl,
  '/users': UsersCtrl,
  '/users/([0-9]+)': UsersShowCtrl,  // Matches /users/123
  '/pages/[a-z0-9]': PagesCtrl,      // Matches /pages/about, /pages/123
  '/.*': AppCtrl                     // Catch-all route
}
```

**Important Notes:**
- Order matters: More specific routes must come before catch-all routes
- First matched route wins
- Use regex patterns for dynamic segments: `([0-9]+)` for numbers, `[a-z0-9]` for alphanumeric

### 4. Calling Controller Methods from HTML

Controller methods are available globally and can be called directly from HTML:

```html
<!-- Methods from current controller are available globally -->
<a href="#" onclick="goBack()">Back</a>
<button onclick="toggleMenu()">Toggle Menu</button>
<input type="text" name="query" onkeyup="search()">
<div onclick="visit('/sign-up')">Sign Up</div>
```

## Components

Components are reusable UI elements that can auto-initialize on page load. They encapsulate widget logic like modals, tooltips, notifications, etc.

### 1. Component with onload Hook

Components with `static onload()` are called automatically on each page load (`turbo:load` event):

```javascript
// app/javascript/components/flash_messages.js

export default class FlashMessages {
  static onload() {
    const flashMessages = findAll('.js-close-snackbar')

    flashMessages.forEach(message => {
      on(message, 'click', () => {
        addClass(message.parentElement, 'hidden')
      })
    })
  }
}
```

### 2. Component with Constructor

Components can also use constructors for instance state:

```javascript
// app/javascript/components/filter_assets.js

export default class FilterAssets {
  constructor() {
    this.assets = findAll('.asset')
    this.searchField = find('.filter-assets-js')
    this.delay = 300
    this.timer = null

    this.setupListeners()
  }

  setupListeners() {
    on(this.searchField, 'keyup', () => {
      if (this.timer) clearTimeout(this.timer)
      this.timer = setTimeout(() => this.filter(), this.delay)
    })
  }

  filter() {
    const query = this.searchField.value.toLowerCase()
    this.assets.forEach(asset => {
      const matches = asset.textContent.toLowerCase().includes(query)
      if (matches) {
        removeClass(asset, 'hide')
      } else {
        addClass(asset, 'hide')
      }
    })
  }
}
```

### 3. Component with Auto-Mount Pattern

Components can auto-mount themselves using `onload()`:

```javascript
// app/javascript/components/modal.js

export default class Modal {
  static onload() {
    findAll('.fire-modal').forEach(el => {
      on(el, 'click', () => {
        const url = data(el, 'url')
        const modal = new Modal(url)
        modal.show()
      })
    })
  }

  constructor(url) {
    this.url = url
  }

  show() {
    const modal = find('#modal')
    const modalBody = find('#modal__body')
    const modalClose = find('#modal__close')

    addClass(document.body, 'disable-scroll')
    addClass(modal, 'open')

    get(this.url).then((result) => {
      insertHTML(modalBody, result)
    })

    on(modalClose, 'click', () => {
      removeClass(document.body, 'disable-scroll')
      removeClass(modal, 'open')
      insertHTML(modalBody, 'Loading ...')
    })
  }
}
```

Then in HTML:

```html
<button class="fire-modal" data-url="/example-modal">Open Remote Modal</button>
```

### 4. Component Best Practices

- **Auto-mounted components**: Only components in the `components` array get `onload()` called automatically
- **Manual components**: Components not in the array can be imported manually in specific controllers
- **Use `onload()` for simple DOM initialization**: No instance state needed
- **Use `constructor()` for components with state**: Need to track instance data
- **Components reinitialize on Turbolinks/Turbo navigation**: `onload()` runs on each `turbo:load` event

## Templates

Templates are functions that return HTML strings using template literals. They help DRY up repetitive HTML generation.

### 1. Template Structure

```javascript
// app/javascript/templates/index.js

export const flashMessage = ({ type, message, icon_name, dissmisable, side, id, native }) => `
  <div class="snackbar snackbar--${type} snackbar--${side}" id="snackbar-${id}" data-native="${native}">
    ${icon_name ? icon(icon_name, 'snackbar__icon') : ''}
    <span>${message}</span>
    ${dissmisable ? `<span class="snackbar__close" onclick="closeAlert('${id}')">${icon("cross", "snackbar__close-icon")}</span>` : ''}
  </div>
`

export const icon = (type, css_classes = '') => `
  <svg class="icon icon_${type} ${css_classes}"><use xlink:href="#icon_${type}"></use></svg>
`

export const itemCard = ({ title, description, id }) => `
  <div class="item-card" data-item-id="${id}">
    <h2>${title}</h2>
    <p>${description}</p>
  </div>
`
```

### 2. Using Templates

```javascript
// Render template function
const html = render('flashMessage', {
  type: 'success',
  message: 'Saved successfully',
  id: Date.now(),
  dissmisable: true
})

// Insert rendered HTML manually
insertHTML('body', html, 'end')

// Or use insertTemplate helper (combines render + insertHTML)
insertTemplate(
  '.container',
  'itemCard',
  { title: 'Item 1', description: 'Description', id: 1 },
  'end'  // 'end' or 'start'
)
```

### 3. Template Best Practices

- Keep templates as pure functions
- Use template literals for multi-line HTML
- Escape user input to prevent XSS
- Compose templates from smaller templates
- Use descriptive parameter names

## Ralix Helpers

Ralix provides global helper functions inspired by jQuery for common DOM operations.

### 1. DOM Selection

```javascript
// Single element (returns Element or undefined)
// Accepts selector string or Element
const button = find('.submit-btn')
const form = find('#user-form')

// Multiple elements (returns NodeList or array)
// Accepts selector string or Element
const inputs = findAll('input[type="text"]')
const cards = findAll('.card')

// Find parent (returns first matching ancestor or parentNode)
const form = findParent(button, 'form')           // First ancestor matching 'form'
const parent = findParent(button, null)           // Direct parent (queryParent null/undefined)

// Find all parents (returns array of matching ancestors)
const parents = findParents('.card', '.card-grid') // All ancestors matching '.card-grid'

// Always check for existence
if (button) {
  // Element exists
}
```

### 2. Event Handling

```javascript
// Single element
on(button, 'click', (e) => {
  e.preventDefault()
  // Handle click
})

// Multiple elements (delegation)
on('.card', 'click', (e) => {
  // Handles clicks on any .card element
  const cardId = data(e.currentTarget, 'card-id')
  console.log(cardId)
})

// Multiple events (space-separated)
on('.btn', 'click focus', handleInteraction)

// With selector string
on('.submit-btn', 'click', handleSubmit)

// Event delegation for dynamic content
on('[data-action="delete"]', 'click', (e) => {
  e.stopPropagation()
  const id = e.currentTarget.getAttribute('data-id')
  deleteItem(id)
})

// Event context (inside callbacks)
on('.btn', 'click', (e) => {
  const el = currentElement()   // Element that triggered the event
  const ev = currentEvent()     // Native event object
})
```

### 3. DOM Manipulation

```javascript
// Add/remove/toggle classes
addClass(element, 'active')
removeClass(element, 'hidden')
toggleClass(element, 'visible')

// Toggle with forced value (add if true, remove if false)
toggleClass(element, 'visible', true)   // add
toggleClass(element, 'visible', false)  // remove

// Multiple classes (array)
addClass('.menu', ['open', 'visible'])
removeClass('#modal', ['hidden', 'inactive'])

// Check if element has class
if (hasClass(element, 'active')) {
  // ...
}

// With selector strings
addClass('.menu', 'open')
removeClass('#modal', 'hidden')

// Insert HTML
// position: 'inner' (replace content), 'prepend' (sibling before element), 'begin' (first child), 'end' (last child), 'append' (sibling after element)
// sanitize: true (default) - XSS protection via DOMPurify
insertHTML('.container', '<div>Content</div>', 'end')
insertHTML('#modal-body', html, 'begin')
insertHTML('.container', userHtml, { position: 'end', sanitize: true })

// Create elements
const form = elem('form', { action: '/submit', method: 'post' })
const input = elem('input', { type: 'text', name: 'email', class: 'form-control' })
form.append(input)
document.body.appendChild(form)
```

### 4. Attributes and Data

```javascript
// Get attribute
const id = attr(element, 'id')
const href = attr(link, 'href')

// Set attribute
attr(element, 'id', 'my-id')
attr(element, { 'aria-label': 'Close', 'role': 'button' })

// Remove attribute(s)
removeAttr(element, 'disabled')
removeAttr(element, ['disabled', 'data-temp'])

// Get/set data attributes (converts kebab-case to camelCase)
const userId = data(element, 'user-id')        // Reads data-user-id
data(element, 'user-id', '123')                // Set
data(element, { 'user-id': '123', 'role': 'admin' })  // Set multiple

// Remove data attribute(s)
removeData(element, 'temp-id')
removeData(element, ['temp-id', 'cache'])      // Remove multiple
removeData(element, null)                      // Remove all data attributes

// Style (get computed or set inline)
const styles = style(element)                  // Get computed styles (null)
style(element, 'color: red; font-size: 16px')   // Set via string
style(element, { color: 'red', fontSize: '16px' })  // Set via object (camelCase)
```

### 5. Navigation Helpers

```javascript
// Navigate to URL (works with Turbolinks/Turbo)
visit('/dashboard')
visit('/users/123')

// Browser back (with optional fallback URL)
back()                    // history.back()
back('/dashboard')        // If no referrer or external referrer, visit fallback

// Reload page
reload()

// Current URL
const url = currentUrl()

// URL params (get/set without full reload)
const allParams = getParam()                    // Object with all params
const singleParam = getParam('id')              // Single param
const arrayParam = getParam('ids[]')            // Array param (ids[])

setParam('page', 2)                             // Set single param
setParam({ page: 2, sort: 'name' })             // Set multiple
setParam('filter', null)                        // Remove param

// Example usage
on('.back-button', 'click', () => {
  back()
})

on('.next-button', 'click', () => {
  visit('/next-page')
})
```

### 6. AJAX and Forms

```javascript
// Simple GET request (returns HTML/text)
const html = await get('/users/123')
insertHTML('.container', html)

// GET with params
const data = await get('/api/search', { params: { q: 'term', limit: 10 } })

// POST request
const result = await post('/api/items', {
  params: { name: 'Item', quantity: 10 },
  options: { format: 'json' }
})

// Full AJAX request
const response = await ajax('/api/endpoint', {
  params: { id: 1 },           // Query string for GET, body for POST/PUT/PATCH
  options: {
    method: 'POST',
    format: 'json',            // 'json' or 'text'
    headers: {
      'Content-Type': 'application/json',
      'X-CSRF-Token': find('meta[name="csrf-token"]').content
    }
  }
})

// Form submission (works with Rails UJS)
submit(formElement)
submit('.search-form')  // Also accepts selector strings

// Serialize form data
const formData = serialize('.my-form')           // Form element or selector
const queryString = serialize({ id: 1, q: 'x' }) // Object to query string
```

### 7. DOM Utilities

```javascript
// Find parent element
const form = findParent(button, 'form')
const card = findParent(element, '.card')

// Sanitize HTML (XSS protection via DOMPurify)
const safeHtml = sanitize(userInput)
insertHTML('.container', sanitize(userHtml), { sanitize: false })  // Pre-sanitized

// Check element existence
if (find('.element')) {
  // Element exists
}
```

### 8. Templates

```javascript
// Render template (requires App.templates)
const html = render('flashMessage', { type: 'success', message: 'Done' })

// Insert template (render + insertHTML, sanitize: false)
insertTemplate('.container', 'itemCard', { title: 'Item', id: 1 })
insertTemplate('.container', 'itemCard', { title: 'Item', id: 1 }, 'end')  // position
```

## Integration with Rails

### 1. Rails UJS Integration

Ralix integrates with Rails UJS for form submissions and AJAX:

```javascript
const App = new RalixApp({
  rails_ujs: Rails,
  // ...
})

Rails.start()
```

This enables:
- CSRF token handling
- Rails AJAX helpers
- Form submission with Rails conventions

### 2. Turbolinks/Turbo Integration

Ralix works seamlessly with Turbolinks and Turbo:

```javascript
Turbolinks.start()  // or Turbo.start()
App.start()
```

**Behavior:**
- Controllers reinitialize on Turbolinks/Turbo navigation
- Components with `onload()` run on each page load (`turbo:load` event)
- Use Turbolinks/Turbo events for cleanup:

```javascript
document.addEventListener('turbo:before-cache', () => {
  // Cleanup before page cache
  // Remove event listeners, clear timers, etc.
})

document.addEventListener('turbo:load', () => {
  // Page loaded, initialize if needed
})
```

### 3. CSRF Token Handling

Always include CSRF tokens in AJAX requests:

```javascript
_getCsrfToken() {
  return find('meta[name="csrf-token"]')?.content
}

_getFetchHeaders() {
  return {
    'X-CSRF-Token': this._getCsrfToken(),
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
}

async _deleteAsset(id) {
  const response = await ajax(`/assets/${id}`, {
    method: 'DELETE',
    headers: this._getFetchHeaders()
  })
  return response
}
```

### 4. Rails Helpers in Templates

Pass data from Rails to JavaScript via data attributes:

```erb
<div data-user-id="<%= user.id %>"
     data-tags='<%= user.tags.to_json %>'
     data-config='<%= config.to_json.html_safe %>'>
```

Access in JavaScript:

```javascript
const userId = data(element, 'user-id')
const tags = JSON.parse(data(element, 'tags'))
const config = JSON.parse(data(element, 'config'))
```

## Common Patterns

### 1. Form Validation

```javascript
validateForm(button) {
  const form = findParent(button, 'form')
  const inputs = form.querySelectorAll('.validate-input-submit-js')
  let error = false

  inputs.forEach(input => {
    if (validateInput(input)) error = true
  })

  if (!error) {
    form.requestSubmit()  // submit(form) doesn't validate required fields
  }
}

validateInput(input) {
  switch (input.type) {
    case 'checkbox':
      if (!input.checked) {
        removeClass(`#${input.id}_error`, 'hide')
        return true
      } else {
        addClass(`#${input.id}_error`, 'hide')
      }
      break
    default:
      console.warn(`No validation defined for ${input.type}`)
  }
  return false
}
```

### 2. Event Delegation for Dynamic Content

```javascript
// Use delegation for dynamically added elements
on('[data-action="delete"]', 'click', (e) => {
  e.stopPropagation()
  const assetId = e.currentTarget.getAttribute('data-asset-id')
  this._deleteAsset(assetId)
})

// Works even if elements are added after page load
```

### 3. Component State Management

```javascript
export default class AssetSelector {
  constructor() {
    this.assets = []
    this.selectedAssetId = null
    this._listenersSetup = false
  }

  _setupEventListeners() {
    if (!this._listenersSetup) {
      on('[data-action="upload"]', 'click', () => {
        find('[data-file-input]')?.click()
      })
      this._listenersSetup = true
    }
  }
}
```

### 4. Debouncing and Throttling

```javascript
// Debounce search input
constructor() {
  this.searchField = find('.search-input')
  this.delay = 300
  this.timer = null

  on(this.searchField, 'keyup', () => {
    if (this.timer) clearTimeout(this.timer)
    this.timer = setTimeout(() => this.search(), this.delay)
  })
}

// Throttle scroll events
constructor() {
  this.lastScroll = 0
  this.throttleDelay = 100

  on(window, 'scroll', () => {
    const now = Date.now()
    if (now - this.lastScroll >= this.throttleDelay) {
      this.handleScroll()
      this.lastScroll = now
    }
  })
}
```

### 5. Loading States

```javascript
showLoading() {
  addClass('.spinner', 'visible')
  removeClass('.content', 'visible')
}

hideLoading() {
  removeClass('.spinner', 'visible')
  addClass('.content', 'visible')
}

async fetchData() {
  this.showLoading()
  try {
    const data = await get('/api/data')
    this.renderData(data)
  } finally {
    this.hideLoading()
  }
}
```

## File Organization

```
app/javascript/
├── application.js          # RalixApp initialization
├── controllers/            # Route-based controllers
│   ├── app.js             # Main/base controller
│   ├── patients.js
│   ├── patients_show.js
│   └── camera.js
├── components/             # Reusable components
│   ├── flash_messages.js   # Auto-mounted
│   ├── modal.js            # Auto-mounted
│   ├── filter_assets.js    # Manual import
│   └── viewport_height.js  # Auto-mounted
├── helpers/                # Utility functions
│   ├── media_utils.js
│   └── device_utils.js
└── templates/              # HTML template functions
    └── index.js
```

## Best Practices

1. **Keep controllers thin**: Move reusable logic to components or helpers
2. **Use components for reusable UI**: Components with `onload()` are simplest
3. **Template functions for dynamic HTML**: Keep templates pure functions
4. **Event delegation**: Use selectors with `on()` for dynamic content
5. **Type safety**: Use optional chaining (`?.`) when accessing elements
6. **CSRF tokens**: Always include CSRF tokens in AJAX requests
7. **Error handling**: Check for `undefined` elements before use
8. **Controller inheritance**: Define common methods in main controller (AppCtrl), override in child controllers
9. **Route order**: More specific routes before catch-all (`/.*`)
10. **Component organization**: Auto-mounted components in `components` array, manual imports for page-specific components
11. **Cleanup**: Remove event listeners and clear timers on page unload
12. **Progressive enhancement**: Enhance server-rendered HTML, don't replace it

## Common Mistakes to Avoid

❌ **Don't use jQuery**: Ralix provides all needed DOM helpers
❌ **Don't use document.querySelector directly**: Use `find()` and `findAll()`
❌ **Don't forget CSRF tokens**: Always include in AJAX requests
❌ **Don't mix vanilla JS event listeners**: Use Ralix's `on()` helper
❌ **Don't create components without lifecycle**: Use `onload()` or `constructor()`
❌ **Don't forget route order**: More specific routes must come before catch-all
❌ **Don't assume all components auto-mount**: Only components in the `components` array get `onload()` called
❌ **Don't use `fetch()` directly**: Use Ralix's `get()` or `ajax()` helpers for consistency
❌ **Don't mutate DOM directly**: Use Ralix helpers for consistency
❌ **Don't forget to check element existence**: Always verify `find()` returns a value

## Philosophy

Ralix follows a "just enough JavaScript" philosophy:

- **Enhances server-rendered HTML**, doesn't replace it
- **Lightweight**: ~500 lines of code total
- **Flat learning curve**: Understand the whole framework in minutes
- **Composable**: Works well with Stimulus, Alpine.js, or any other framework
- **Rails-inspired**: Controller hierarchy inspired by Rails controllers
- **jQuery-inspired helpers**: Familiar API for DOM manipulation
- **Progressive enhancement**: Start with HTML, enhance with JavaScript

## Resources

### Official Documentation

- **Main Repository**: https://github.com/ralixjs/ralix
- **Rails Integration Guide**: https://github.com/ralixjs/ralix/blob/master/docs/RAILS_INTEGRATION.md
- **Design Philosophy**: https://github.com/ralixjs/ralix/blob/master/docs/DESIGN.md
- **Helpers API**: https://github.com/ralixjs/ralix/blob/master/docs/HELPERS_API.md
- **NPM Package**: https://www.npmjs.com/package/ralix

## References

- **ralix-rails** skill: Full Ralix helper API, installation, setup
- [Ralix Documentation](https://github.com/ralixjs/ralix)
- [Turbo Documentation](https://turbo.hotwired.dev/)
