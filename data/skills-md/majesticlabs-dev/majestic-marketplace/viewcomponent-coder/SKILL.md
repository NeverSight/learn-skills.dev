---
name: viewcomponent-coder
description: Build component-based UIs with ViewComponent and view_component-contrib. Use when creating reusable UI components, implementing slots and style variants, or building component previews. Triggers on ViewComponent creation, component patterns, Lookbook previews, or UI component architecture.
---

# ViewComponent Patterns

Build modern, component-based UIs with ViewComponent using Evil Martians' [view_component-contrib](https://github.com/palkan/view_component-contrib) patterns.

## When to Use This Skill

- Creating ViewComponent classes
- Implementing slots and style variants
- Building Lookbook previews
- Testing components in isolation
- Refactoring partials to components

## Core Principle: Components Over Partials

**Prefer ViewComponents over partials** for reusable UI.

### Why ViewComponents?

- Better encapsulation than partials
- Testable in isolation
- Object-oriented approach with explicit contracts
- IDE support and type safety
- Performance benefits (compiled templates)

## Setup

```ruby
# Gemfile
gem "view_component"
gem "view_component-contrib"  # Evil Martians patterns
gem "dry-initializer"         # Declarative initialization
gem "lookbook"                # Component previews
gem "inline_svg"              # SVG icons
```

Install with Rails template:
```bash
rails app:template LOCATION="https://railsbytes.com/script/zJosO5"
```

## Base Classes

```ruby
# app/components/application_view_component.rb
class ApplicationViewComponent < ViewComponentContrib::Base
  extend Dry::Initializer
end

# spec/components/previews/application_view_component_preview.rb
class ApplicationViewComponentPreview < ViewComponentContrib::Preview::Base
  self.abstract_class = true
end
```

## Basic Component with dry-initializer

```ruby
# app/components/button_component.rb
class ButtonComponent < ApplicationViewComponent
  option :text
  option :variant, default: -> { :primary }
  option :size, default: -> { :md }
end
```

```erb
<%# app/components/button_component.html.erb %>
<button class="btn btn-<%= variant %> btn-<%= size %>">
  <%= text %>
</button>
```

## Style Variants DSL

Replace manual VARIANTS hashes with the Style Variants DSL:

```ruby
class ButtonComponent < ApplicationViewComponent
  include ViewComponentContrib::StyleVariants

  option :text
  option :color, default: -> { :primary }
  option :size, default: -> { :md }

  style do
    base { %w[font-medium rounded-full] }

    variants {
      color {
        primary { %w[bg-blue-500 text-white] }
        secondary { %w[bg-gray-500 text-white] }
        danger { %w[bg-red-500 text-white] }
      }
      size {
        sm { "text-sm px-2 py-1" }
        md { "text-base px-4 py-2" }
        lg { "text-lg px-6 py-3" }
      }
    }

    # Apply when multiple conditions match
    compound(size: :lg, color: :primary) { "uppercase" }

    defaults { { color: :primary, size: :md } }
  end
end
```

```erb
<button class="<%= style(color:, size:) %>">
  <%= text %>
</button>
```

## Component with Slots

```ruby
class CardComponent < ApplicationViewComponent
  renders_one :header
  renders_one :footer
  renders_many :actions
end
```

```erb
<%= render CardComponent.new do |card| %>
  <% card.with_header do %>
    <h3>Title</h3>
  <% end %>

  <p>Body content</p>

  <% card.with_action do %>
    <%= helpers.link_to "Edit", edit_path %>
  <% end %>
<% end %>
```

## Important Rules

**1. Prefix Rails helpers with `helpers.`**

```erb
<%# CORRECT %>
<%= helpers.link_to "Home", root_path %>
<%= helpers.image_tag "logo.png" %>
<%= helpers.inline_svg_tag "icons/user.svg" %>

<%# WRONG - will fail in component context %>
<%= link_to "Home", root_path %>
```

**Exception**: `t()` i18n helper does NOT need prefix:

```erb
<%= t('.title') %>
```

**2. SVG Icons as Separate Files**

Store SVGs in `app/assets/images/icons/` and render with `inline_svg` gem:

```erb
<%= helpers.inline_svg_tag "icons/user.svg", class: "w-5 h-5" %>
```

**Don't inline SVG markup in Ruby code** - use separate files instead.

## Conditional Rendering

```ruby
class AlertComponent < ApplicationViewComponent
  option :message
  option :type, default: -> { :info }
  option :dismissible, default: -> { true }

  # Skip rendering if no message
  def render?
    message.present?
  end
end
```

## Lookbook Previews

```ruby
# spec/components/previews/button_component_preview.rb
class ButtonComponentPreview < ApplicationViewComponentPreview
  def default
    render ButtonComponent.new(text: "Click me")
  end

  def primary
    render ButtonComponent.new(text: "Primary", color: :primary)
  end

  def all_sizes
    render_with(wrapper: :flex_row) do
      safe_join([
        render(ButtonComponent.new(text: "Small", size: :sm)),
        render(ButtonComponent.new(text: "Medium", size: :md)),
        render(ButtonComponent.new(text: "Large", size: :lg))
      ])
    end
  end
end
```

Access at: `http://localhost:3000/lookbook`

## Testing Components

```ruby
RSpec.describe ButtonComponent, type: :component do
  it "renders button text" do
    render_inline(ButtonComponent.new(text: "Click me"))
    expect(page).to have_button("Click me")
  end

  it "applies style variant classes" do
    render_inline(ButtonComponent.new(text: "Save", color: :primary, size: :lg))
    expect(page).to have_css("button.bg-blue-500.text-lg")
  end
end
```

## Detailed References

For advanced patterns and examples:
- `references/patterns.md` - Slots, collections, polymorphic components, Turbo integration
- `references/style-variants.md` - Full Style Variants DSL, compound variants, TailwindMerge
