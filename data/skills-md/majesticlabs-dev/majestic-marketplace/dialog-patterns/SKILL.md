---
name: dialog-patterns
description: Native HTML dialog patterns for Rails with Turbo and Stimulus. Use when building modals, confirmations, alerts, or any overlay UI. Triggers on modal, dialog, popup, confirmation, alert, or toast patterns.
---

# Native Dialog Patterns for Rails

Build accessible, modern dialog UIs using the native HTML `<dialog>` element with Turbo Frames and Stimulus. No JavaScript frameworks or heavy libraries required.

## When to Use This Skill

- Building modal dialogs for forms, confirmations, or content
- Creating toast/alert notifications
- Implementing confirmation dialogs (delete, destructive actions)
- Any overlay UI that needs focus management and accessibility

## Why Native `<dialog>`?

| Feature | Native `<dialog>` | Custom Modal |
|---------|-------------------|--------------|
| Focus trapping | Built-in | Manual implementation |
| ESC to close | Built-in | Manual implementation |
| Backdrop | Built-in (`::backdrop`) | Manual overlay |
| Accessibility | Native `role="dialog"` | Manual ARIA |
| Top layer | Automatic (above all content) | z-index battles |
| Scroll lock | Automatic | Manual `overflow: hidden` |

## Zero-JavaScript Confirmation Dialogs (Recommended)

Modern browsers support the **Invoker Commands API** for declarative dialog control—no JavaScript required. See [references/zero-js-patterns.md](references/zero-js-patterns.md) for complete examples.

### Quick Reference

```erb
<%= button_tag "Delete", commandfor: "delete-#{post.id}", command: "show-modal" %>

<dialog id="delete-<%= post.id %>" closedby="any" role="alertdialog">
  <h3>Delete "<%= post.title %>"?</h3>
  <button commandfor="delete-<%= post.id %>" command="close">Cancel</button>
  <%= button_to "Delete", post, method: :delete %>
</dialog>
```

### Key Attributes

| Attribute | Purpose |
|-----------|---------|
| `commandfor="id"` | References the dialog to control |
| `command="show-modal"` | Opens as modal (backdrop, focus trap) |
| `command="close"` | Closes the dialog |
| `closedby="any"` | Enables backdrop click and ESC to close |

### When to Use Zero-JS vs Stimulus

| Scenario | Approach |
|----------|----------|
| Simple confirmations | Zero-JS (Invoker Commands) |
| Modals with async content | Stimulus + Turbo Frames |
| Complex multi-step dialogs | Stimulus controller |
| Animations | CSS `@starting-style` |

### Additional Patterns (see references/)

- **CSS animations** with `@starting-style` for enter/exit transitions
- **Turbo.config.forms.confirm** to replace ugly browser dialogs
- **Progressive enhancement** for cross-browser compatibility

## Core Pattern: Async Modal with Turbo Frames

The recommended pattern for Rails modals combines three technologies:

1. **Turbo Frame** - Async content loading without page reload
2. **Native `<dialog>`** - Accessible modal presentation
3. **Stimulus controller** - Lifecycle management

### Step 1: Layout Container

Add a modal turbo-frame to your layout:

```erb
<%# app/views/layouts/application.html.erb %>
<body>
  <%= yield %>

  <%# Modal injection point %>
  <%= turbo_frame_tag :modal %>
</body>
```

### Step 2: Trigger Links

Target the modal frame from any link:

```erb
<%# Any view %>
<%= link_to "New Post", new_post_path, data: { turbo_frame: :modal } %>
<%= link_to "Edit", edit_post_path(@post), data: { turbo_frame: :modal } %>
<%= link_to "Confirm Delete", confirm_delete_post_path(@post), data: { turbo_frame: :modal } %>
```

### Step 3: Modal Content View

Wrap modal content in matching turbo-frame with nested inner frame:

```erb
<%# app/views/posts/new.html.erb %>
<%= turbo_frame_tag :modal do %>
  <%# Inner frame prevents flash during form validation %>
  <%= turbo_frame_tag :modal_content do %>
    <dialog data-controller="dialog" data-action="click->dialog#clickOutside" open>
      <article>
        <header>
          <h2>New Post</h2>
          <button data-action="dialog#close" aria-label="Close">&times;</button>
        </header>

        <%= render "form", post: @post %>
      </article>
    </dialog>
  <% end %>
<% end %>
```

### Step 4: Stimulus Controller

Key behaviors: `showModal()` on connect, `replaceChildren()` on disconnect (prevents stale content), `clickOutside` for backdrop close.

See [references/dialog-examples.md](references/dialog-examples.md) for full Stimulus controller, CSS styling, and Tailwind variant.

## Why Nested Turbo Frames?

The nested frame pattern (`modal` > `modal_content`) prevents content flashing:

```erb
<%= turbo_frame_tag :modal do %>
  <%= turbo_frame_tag :modal_content do %>
    <dialog>...</dialog>
  <% end %>
<% end %>
```

**Problem without nested frame:**
When a form inside the modal has validation errors and re-renders, the outer frame briefly shows the old content before replacing it.

**Solution with nested frame:**
The inner frame handles form re-renders independently, keeping the modal structure stable.

## Form Handling in Modals

### Successful Submission

Redirect with Turbo to close modal and update page:

```ruby
# app/controllers/posts_controller.rb
def create
  @post = Post.new(post_params)

  if @post.save
    redirect_to posts_path, notice: "Post created!"
  else
    render :new, status: :unprocessable_entity
  end
end
```

The redirect navigates `_top` (full page), effectively closing the modal.

### Validation Errors

Re-render the form with `422` status to keep modal open:

```ruby
render :new, status: :unprocessable_entity
```

### Turbo Stream Response (Stay in Modal)

Use `turbo_stream.update("modal", "")` to clear modal without full redirect. See [references/dialog-examples.md](references/dialog-examples.md) for full example.

## Confirmation Dialog Pattern

For destructive actions: add a `confirm_delete` member route, render a dialog in a turbo frame, trigger via `link_to` with `data: { turbo_frame: :modal }`.

See [references/dialog-examples.md](references/dialog-examples.md) for full confirmation dialog view, route, and trigger.

## Alert/Toast Pattern

For flash messages and notifications. Use `show()` instead of `showModal()` for non-modal presentation. See [references/toast-slideover-patterns.md](references/toast-slideover-patterns.md) for complete implementation.

```erb
<dialog class="toast" data-controller="toast" data-toast-duration-value="5000">
  <p><%= message %></p>
</dialog>
```

Key difference: `show()` opens without backdrop or focus trap (toasts), `showModal()` centers with backdrop (modals).

## Slideover Panel Pattern

For side panels (settings, filters, details). See [references/toast-slideover-patterns.md](references/toast-slideover-patterns.md) for styling and animations.

```erb
<dialog class="slideover" data-controller="dialog" data-action="click->dialog#clickOutside">
  <aside>
    <header><h2>Filters</h2></header>
    <%= render "filters" %>
  </aside>
</dialog>
```

## Accessibility

Native `<dialog>` provides focus trapping, ESC close, background inert, and top layer automatically. Additionally ensure:

- Visible close button (not just ESC)
- `aria-labelledby` / `aria-describedby` for descriptive context
- Focus return to trigger element on close (store `document.activeElement` in `connect()`)

See [references/dialog-examples.md](references/dialog-examples.md) for enhanced accessibility and focus return examples.

## Common Patterns Summary

| Pattern | Container | Stimulus | `show` method |
|---------|-----------|----------|---------------|
| Modal form | `turbo_frame_tag :modal` | `dialog` | `showModal()` |
| Confirmation | `turbo_frame_tag :modal` | `dialog` | `showModal()` |
| Toast/Alert | Fixed position | `toast` | `show()` |
| Slideover | `turbo_frame_tag :modal` | `dialog` | `showModal()` |

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Custom modal without `<dialog>` | No native accessibility | Use native `<dialog>` |
| Missing nested turbo-frame | Content flash on validation | Add inner frame |
| Not clearing frame on close | Stale content on reopen | Clear with `replaceChildren()` in `disconnect()` |
| z-index for stacking | Battles with other elements | `<dialog>` uses top layer |
| Manual focus trap | Complex, error-prone | `showModal()` handles it |
| Inline backdrop div | Extra markup | Use `::backdrop` pseudo-element |

## Testing Dialogs

```ruby
# System test - use `within "dialog"` to scope assertions
within "dialog" do
  fill_in "Title", with: "My Post"
  click_button "Create"
end
expect(page).not_to have_selector("dialog[open]")  # Modal closed
```

## Browser Support

| Pattern | Chrome | Firefox | Safari |
|---------|--------|---------|--------|
| Native `<dialog>` | 37+ | 98+ | 15.4+ |
| Invoker Commands | 135+ | 144+ | 26.2+ |
| `@starting-style` | 117+ | 129+ | 17.5+ |

For older browsers: [dialog polyfill](https://github.com/GoogleChrome/dialog-polyfill), [invokers polyfill](https://github.com/nickshanks/invokers). See [references/zero-js-patterns.md](references/zero-js-patterns.md) for progressive enhancement strategies.
