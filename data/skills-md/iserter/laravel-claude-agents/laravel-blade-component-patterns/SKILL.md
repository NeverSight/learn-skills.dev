---
name: laravel-blade-component-patterns
description: Best practices for Laravel Blade components including class-based and anonymous components, slots, attribute bags, and reusable UI patterns.
---

# Blade Component Patterns

## Class-Based Components

```bash
php artisan make:component Alert
```

```php
<?php

namespace App\View\Components;

use Illuminate\Contracts\View\View;
use Illuminate\View\Component;

class Alert extends Component
{
    public function __construct(
        public string $type = 'info',
        public string $message = '',
        public bool $dismissible = false,
    ) {}

    public function alertClasses(): string
    {
        return match ($this->type) {
            'success' => 'bg-green-100 text-green-800 border-green-300',
            'error' => 'bg-red-100 text-red-800 border-red-300',
            'warning' => 'bg-yellow-100 text-yellow-800 border-yellow-300',
            default => 'bg-blue-100 text-blue-800 border-blue-300',
        };
    }

    public function render(): View
    {
        return view('components.alert');
    }
}
```

```blade
{{-- resources/views/components/alert.blade.php --}}
<div {{ $attributes->merge(['class' => 'border rounded-lg p-4 ' . $alertClasses()]) }}
     role="alert">
    <p>{{ $message ?: $slot }}</p>
    @if ($dismissible)
        <button type="button" @click="$el.parentElement.remove()">
            &times;
        </button>
    @endif
</div>
```

```blade
{{-- Usage --}}
<x-alert type="success" message="Profile updated!" />
<x-alert type="error" dismissible>Something went wrong.</x-alert>
```

## Anonymous Components

```blade
{{-- resources/views/components/card.blade.php --}}
@props([
    'title' => null,
    'footer' => null,
])

<div {{ $attributes->merge(['class' => 'bg-white rounded-lg shadow-md overflow-hidden']) }}>
    @if ($title)
        <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900">{{ $title }}</h3>
        </div>
    @endif

    <div class="p-6">
        {{ $slot }}
    </div>

    @if ($footer)
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
            {{ $footer }}
        </div>
    @endif
</div>
```

```blade
{{-- Usage --}}
<x-card title="User Details">
    <p>Name: {{ $user->name }}</p>
    <x-slot:footer>
        <button>Edit</button>
    </x-slot:footer>
</x-card>
```

## The $attributes Bag

### Merging Attributes

```blade
{{-- ✅ Merge classes and other attributes --}}
<div {{ $attributes->merge(['class' => 'base-class', 'role' => 'alert']) }}>
    {{ $slot }}
</div>

{{-- Usage: classes are appended, other attrs are overridden --}}
<x-alert class="extra-class" id="my-alert" />
{{-- Result: class="base-class extra-class" role="alert" id="my-alert" --}}
```

### Class Manipulation

```blade
@props(['variant' => 'primary'])

<button {{ $attributes->class([
    'px-4 py-2 rounded font-medium',
    'bg-blue-600 text-white hover:bg-blue-700' => $variant === 'primary',
    'bg-gray-200 text-gray-800 hover:bg-gray-300' => $variant === 'secondary',
    'bg-red-600 text-white hover:bg-red-700' => $variant === 'danger',
])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```

### Filtering and Checking Attributes

```blade
{{-- Filter attributes --}}
<input {{ $attributes->whereStartsWith('wire:') }} />
<div {{ $attributes->whereDoesntStartWith('wire:') }}>

{{-- Check if attribute exists --}}
@if ($attributes->has('autofocus'))
    <script>document.querySelector('[autofocus]').focus();</script>
@endif

{{-- Get a specific attribute --}}
<input type="{{ $attributes->get('type', 'text') }}" />

{{-- Only / Except --}}
<label {{ $attributes->only(['for', 'class']) }}>
<input {{ $attributes->except(['class']) }} />
```

### Prepending and Appending

```blade
{{-- Prepend to existing attribute values --}}
<div {{ $attributes->prepend('class', 'base-') }}>

{{-- Useful for conditional attribute defaults --}}
<input {{ $attributes->merge([
    'type' => 'text',
    'class' => 'form-input',
]) }} />
```

## Named Slots

```blade
{{-- resources/views/components/modal.blade.php --}}
@props(['title'])

<div {{ $attributes->merge(['class' => 'modal']) }}>
    <div class="modal-header">
        <h2>{{ $title }}</h2>
        {{ $headerActions ?? '' }}
    </div>

    <div class="modal-body">
        {{ $slot }}
    </div>

    @if (isset($footer))
        <div class="modal-footer">
            {{ $footer }}
        </div>
    @endif
</div>
```

```blade
{{-- Usage --}}
<x-modal title="Confirm Delete">
    <x-slot:headerActions>
        <button @click="close">&times;</button>
    </x-slot:headerActions>

    <p>Are you sure you want to delete this item?</p>

    <x-slot:footer>
        <button @click="close">Cancel</button>
        <button @click="confirm" class="btn-danger">Delete</button>
    </x-slot:footer>
</x-modal>
```

### Slot Attributes

```blade
{{-- Component definition --}}
<ul>
    @foreach ($items as $item)
        {{ $slot->withAttributes(['class' => 'text-sm']) }}
    @endforeach
</ul>

{{-- Scoped slots --}}
@props(['items'])

@foreach ($items as $item)
    <li>{{ $slot }}</li>
@endforeach
```

## Dynamic Components

```blade
{{-- ✅ Render components dynamically --}}
<x-dynamic-component :component="'alert'" type="success" message="Done!" />

{{-- Useful for form field rendering --}}
@foreach ($fields as $field)
    <x-dynamic-component
        :component="'forms.' . $field->type"
        :name="$field->name"
        :label="$field->label"
        :value="old($field->name)"
    />
@endforeach
```

## Layouts with Component Approach

```blade
{{-- resources/views/components/layouts/app.blade.php --}}
@props(['title' => config('app.name')])

<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ $title }}</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
    @stack('styles')
</head>
<body class="antialiased">
    {{ $header ?? '' }}

    <main>
        {{ $slot }}
    </main>

    {{ $footer ?? '' }}

    @stack('scripts')
</body>
</html>
```

```blade
{{-- resources/views/dashboard.blade.php --}}
<x-layouts.app title="Dashboard">
    <x-slot:header>
        <x-navbar />
    </x-slot:header>

    <h1>Dashboard</h1>
    <p>Welcome back!</p>
</x-layouts.app>
```

## Conditional Classes and Styles

```blade
{{-- @class directive --}}
<div @class([
    'p-4 rounded-lg',
    'bg-green-100 text-green-800' => $status === 'active',
    'bg-red-100 text-red-800' => $status === 'inactive',
    'opacity-50' => $disabled,
])>
    {{ $label }}
</div>

{{-- @style directive --}}
<div @style([
    'background-color: ' . $color,
    'font-weight: bold' => $isImportant,
    'display: none' => $hidden,
])>
    {{ $content }}
</div>
```

## Stacks

```blade
{{-- In layout --}}
<head>
    @stack('styles')
</head>
<body>
    {{ $slot }}
    @stack('scripts')
</body>

{{-- In child views / components --}}
@push('styles')
    <link rel="stylesheet" href="{{ asset('css/datepicker.css') }}">
@endpush

@push('scripts')
    <script src="{{ asset('js/datepicker.js') }}"></script>
@endpush

{{-- Prepend to stack (added before other pushes) --}}
@prepend('scripts')
    <script src="{{ asset('js/jquery.min.js') }}"></script>
@endprepend

{{-- Push once (prevents duplicates) --}}
@pushOnce('scripts')
    <script src="{{ asset('js/chart.js') }}"></script>
@endPushOnce
```

## View Fragments for HTMX / Turbo

```blade
{{-- resources/views/posts/index.blade.php --}}
<x-layouts.app>
    <h1>Posts</h1>

    @fragment('post-list')
    <div id="post-list">
        @foreach ($posts as $post)
            @fragment('post-' . $post->id)
            <div id="post-{{ $post->id }}">
                <h2>{{ $post->title }}</h2>
                <p>{{ $post->excerpt }}</p>
            </div>
            @endfragment
        @endforeach

        {{ $posts->links() }}
    </div>
    @endfragment
</x-layouts.app>
```

```php
// Controller returning just a fragment
public function index(Request $request)
{
    $posts = Post::paginate(15);

    if ($request->header('HX-Request')) {
        return view('posts.index', compact('posts'))->fragment('post-list');
    }

    return view('posts.index', compact('posts'));
}
```

## Reusable Form Component Patterns

### Text Input

```blade
{{-- resources/views/components/forms/input.blade.php --}}
@props([
    'name',
    'label' => null,
    'type' => 'text',
    'value' => null,
])

<div class="mb-4">
    @if ($label)
        <label for="{{ $name }}" class="block text-sm font-medium text-gray-700 mb-1">
            {{ $label }}
        </label>
    @endif

    <input
        {{ $attributes->class([
            'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'border-red-500' => $errors->has($name),
        ])->merge([
            'type' => $type,
            'name' => $name,
            'id' => $name,
            'value' => old($name, $value),
        ]) }}
    />

    @error($name)
        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
    @enderror
</div>
```

### Select

```blade
{{-- resources/views/components/forms/select.blade.php --}}
@props([
    'name',
    'label' => null,
    'options' => [],
    'selected' => null,
    'placeholder' => 'Select an option...',
])

<div class="mb-4">
    @if ($label)
        <label for="{{ $name }}" class="block text-sm font-medium text-gray-700 mb-1">
            {{ $label }}
        </label>
    @endif

    <select
        {{ $attributes->class([
            'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
            'border-red-500' => $errors->has($name),
        ])->merge(['name' => $name, 'id' => $name]) }}
    >
        @if ($placeholder)
            <option value="">{{ $placeholder }}</option>
        @endif
        @foreach ($options as $value => $text)
            <option value="{{ $value }}" @selected(old($name, $selected) == $value)>
                {{ $text }}
            </option>
        @endforeach
    </select>

    @error($name)
        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
    @enderror
</div>
```

### Form Usage

```blade
<form method="POST" action="{{ route('users.store') }}">
    @csrf

    <x-forms.input name="name" label="Full Name" required />
    <x-forms.input name="email" label="Email" type="email" required />
    <x-forms.select
        name="role"
        label="Role"
        :options="['admin' => 'Admin', 'editor' => 'Editor', 'viewer' => 'Viewer']"
    />

    <button type="submit" class="btn-primary">Create User</button>
</form>
```

## Subdirectory Components

```blade
{{-- resources/views/components/forms/input.blade.php --}}
{{-- Usage: --}}
<x-forms.input name="email" />

{{-- resources/views/components/navigation/menu-item.blade.php --}}
{{-- Usage: --}}
<x-navigation.menu-item href="/about">About</x-navigation.menu-item>
```

## Inline Components

```php
// For very simple components without a template
use Illuminate\View\Component;

class ColorPicker extends Component
{
    public function __construct(
        public string $color = '#000000',
    ) {}

    public function render(): string
    {
        return <<<'blade'
            <div>
                <input type="color" {{ $attributes->merge(['value' => $color]) }}>
            </div>
        blade;
    }
}
```

## Checklist

- [ ] Components have a single, clear purpose
- [ ] `@props` declared for all expected data in anonymous components
- [ ] `$attributes` bag used to allow consumer customization
- [ ] Default classes set via `merge()` or `class()`
- [ ] Named slots used for flexible content sections
- [ ] Form components display validation errors via `@error`
- [ ] Layouts use `@stack` for page-specific CSS/JS
- [ ] `@pushOnce` used to prevent duplicate asset includes
- [ ] Dynamic components used for configurable rendering
- [ ] Components organized in subdirectories by domain
- [ ] `@class` and `@style` used for conditional styling
- [ ] Fragments used for partial page updates (HTMX/Turbo)
