---
name: inertia-coder
description: Build modern SPAs with Inertia.js and Rails using React, Vue, or Svelte. Use when creating Inertia pages, handling forms with useForm, managing shared props, or implementing client-side routing. Triggers on Inertia.js setup, SPA development, or React/Vue/Svelte with Rails.
---

# Inertia.js + Rails

Build modern single-page applications using Inertia.js with React/Vue/Svelte and Rails backend.

## When to Use This Skill

- Setting up Inertia.js with Rails
- Creating Inertia page components
- Handling forms with useForm hook
- Managing shared props and flash messages
- Client-side routing without API complexity
- File uploads with progress tracking

## What is Inertia.js?

**Inertia.js allows you to build SPAs using classic server-side routing and controllers.**

| Approach | Pros | Cons |
|----------|------|------|
| Traditional Rails Views | Simple, server-rendered | Limited interactivity |
| Rails API + React SPA | Full SPA experience | Duplicated routing, complex state |
| **Inertia.js** | SPA + server routing | Best of both worlds |

## Quick Setup

```ruby
# Gemfile
gem 'inertia_rails'
gem 'vite_rails'
```

```bash
bundle install
rails inertia:install  # Choose: React, Vue, or Svelte
```

```ruby
# config/initializers/inertia_rails.rb
InertiaRails.configure do |config|
  config.version = ViteRuby.digest

  config.share do |controller|
    {
      auth: {
        user: controller.current_user&.as_json(only: [:id, :name, :email])
      },
      flash: controller.flash.to_hash
    }
  end
end
```

## Controller Pattern

```ruby
class ArticlesController < ApplicationController
  def index
    articles = Article.published.order(created_at: :desc)

    render inertia: 'Articles/Index', props: {
      articles: articles.as_json(only: [:id, :title, :excerpt])
    }
  end

  def create
    @article = Article.new(article_params)

    if @article.save
      redirect_to article_path(@article), notice: 'Article created'
    else
      redirect_to new_article_path, inertia: { errors: @article.errors }
    end
  end
end
```

## React Page Component

```jsx
// app/frontend/pages/Articles/Index.jsx
import { Link } from '@inertiajs/react'

export default function Index({ articles }) {
  return (
    <div>
      <h1>Articles</h1>
      {articles.map(article => (
        <Link key={article.id} href={`/articles/${article.id}`}>
          <h2>{article.title}</h2>
        </Link>
      ))}
    </div>
  )
}
```

## Forms with useForm

```jsx
import { useForm } from '@inertiajs/react'

export default function New() {
  const { data, setData, post, processing, errors } = useForm({
    title: '',
    body: ''
  })

  function handleSubmit(e) {
    e.preventDefault()
    post('/articles')
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={data.title}
        onChange={e => setData('title', e.target.value)}
      />
      {errors.title && <div className="error">{errors.title}</div>}

      <textarea
        value={data.body}
        onChange={e => setData('body', e.target.value)}
      />
      {errors.body && <div className="error">{errors.body}</div>}

      <button disabled={processing}>
        {processing ? 'Creating...' : 'Create'}
      </button>
    </form>
  )
}
```

## Shared Layout

```jsx
// app/frontend/layouts/AppLayout.jsx
import { Link, usePage } from '@inertiajs/react'

export default function AppLayout({ children }) {
  const { auth, flash } = usePage().props

  return (
    <div>
      <nav>
        <Link href="/">Home</Link>
        {auth.user ? (
          <Link href="/logout" method="delete">Logout</Link>
        ) : (
          <Link href="/login">Login</Link>
        )}
      </nav>

      {flash.success && <div className="alert-success">{flash.success}</div>}

      <main>{children}</main>
    </div>
  )
}

// Assign layout to page
Index.layout = page => <AppLayout>{page}</AppLayout>
```

## File Upload

```jsx
import { useForm } from '@inertiajs/react'

const { data, setData, post, progress } = useForm({
  avatar: null
})

<input
  type="file"
  onChange={e => setData('avatar', e.target.files[0])}
/>

{progress && <progress value={progress.percentage} max="100" />}

<button onClick={() => post('/profile/avatar', { forceFormData: true })}>
  Upload
</button>
```

## Best Practices

### DO
- Use `<Link>` instead of `<a>` tags
- Share common data via config (auth, flash)
- Validate on server - client is UX only
- Show loading states with `processing`
- Use layouts for consistent navigation

### DON'T
- Don't use `window.location` - breaks SPA
- Don't create REST APIs - Inertia doesn't need them
- Don't fetch data client-side - server provides props
- Don't bypass Inertia router - breaks behavior

## Detailed References

For framework-specific patterns:
- `references/react-patterns.md` - React hooks, TypeScript, advanced patterns
- `references/vue-patterns.md` - Vue 3 Composition API patterns
- `references/svelte-patterns.md` - Svelte stores and reactivity patterns
