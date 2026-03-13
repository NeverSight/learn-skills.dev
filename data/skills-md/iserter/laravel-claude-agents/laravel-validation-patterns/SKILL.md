---
name: laravel-validation-patterns
description: Best practices for Laravel validation including Form Requests, custom rules, conditional validation, and input sanitization.
---

# Laravel Validation Patterns

## Form Request Classes (Standard Approach)

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StoreOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Order::class);
    }

    public function rules(): array
    {
        return [
            'customer_id' => ['required', 'exists:customers,id'],
            'items' => ['required', 'array', 'min:1'],
            'items.*.product_id' => ['required', 'exists:products,id'],
            'items.*.quantity' => ['required', 'integer', 'min:1'],
            'notes' => ['nullable', 'string', 'max:500'],
        ];
    }

    public function messages(): array
    {
        return [
            'items.required' => 'At least one item is required.',
            'items.*.product_id.exists' => 'Product #:position does not exist.',
        ];
    }

    protected function prepareForValidation(): void
    {
        $this->merge([
            'notes' => strip_tags($this->notes),
            'email' => strtolower($this->email),
        ]);
    }

    public function after(): array
    {
        return [
            function (\Illuminate\Validation\Validator $validator) {
                if ($this->hasExceededOrderLimit()) {
                    $validator->errors()->add('items', 'You have exceeded the daily order limit.');
                }
            },
        ];
    }
}
```

## Custom Rule Objects

```php
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class StrongPassword implements ValidationRule
{
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (! preg_match('/[A-Z]/', $value)) {
            $fail('The :attribute must contain at least one uppercase letter.');
        }

        if (! preg_match('/[0-9]/', $value)) {
            $fail('The :attribute must contain at least one number.');
        }
    }
}

// Usage in rules
'password' => ['required', 'string', 'min:8', new StrongPassword],
```

## Conditional Validation

```php
public function rules(): array
{
    return [
        'type' => ['required', Rule::in(['individual', 'company'])],

        // Required only when type is company
        'company_name' => ['required_if:type,company', 'string', 'max:255'],

        // Excluded when type is individual (not present in validated data)
        'tax_id' => ['exclude_if:type,individual', 'required', 'string'],

        // Dynamic conditional rule
        'billing_address' => [
            Rule::when($this->boolean('different_billing'), ['required', 'string']),
        ],

        // Conditional with sometimes (only validates if field is present)
        'coupon_code' => ['sometimes', 'string', 'exists:coupons,code'],
    ];
}
```

## Array and Nested Validation

```php
public function rules(): array
{
    return [
        'tags' => ['required', 'array', 'min:1', 'max:10'],
        'tags.*' => ['string', 'max:50'],

        'items' => ['required', 'array'],
        'items.*.name' => ['required', 'string'],
        'items.*.options' => ['sometimes', 'array'],
        'items.*.options.*.key' => ['required_with:items.*.options', 'string'],
    ];
}
```

## Database Rules

```php
public function rules(): array
{
    return [
        // Unique with ignore (for updates)
        'email' => [
            'required',
            'email',
            Rule::unique('users')->ignore($this->user()),
        ],

        // Unique with scoping
        'slug' => [
            'required',
            Rule::unique('posts')->where('tenant_id', $this->user()->tenant_id),
        ],

        // Exists with additional constraints
        'category_id' => [
            'required',
            Rule::exists('categories', 'id')->where('active', true),
        ],
    ];
}
```

## Enum Validation

```php
use App\Enums\OrderStatus;

public function rules(): array
{
    return [
        'status' => ['required', Rule::enum(OrderStatus::class)],

        // Only allow specific enum values
        'priority' => [
            'required',
            Rule::enum(Priority::class)->only([Priority::High, Priority::Critical]),
        ],
    ];
}
```

## Working with Validated Data

```php
// In controller
public function store(StoreOrderRequest $request)
{
    // ✅ Use validated data only
    $validated = $request->validated();

    // ✅ Use safe() for partial access
    $orderData = $request->safe()->only(['customer_id', 'notes']);
    $items = $request->safe()->except(['notes']);

    // ✅ Merge additional trusted data
    $order = Order::create(
        $request->safe()->merge(['user_id' => $request->user()->id])->all()
    );

    // ❌ Never use unvalidated input
    $order = Order::create($request->all());

    // ❌ Never bypass validation
    $order = Order::create($request->input());
}
```

## Common Pitfalls

```php
// ❌ Validating inline in controllers
public function store(Request $request)
{
    $request->validate(['title' => 'required']);
    // Hard to test, not reusable
}

// ✅ Use Form Request classes
public function store(StorePostRequest $request)
{
    Post::create($request->validated());
}

// ❌ Missing bail - continues validating after first failure
'email' => ['email', 'unique:users', 'dns_check'],

// ✅ Use bail to stop on first failure
'email' => ['bail', 'email', 'unique:users'],

// ❌ Using $request->all() instead of validated data
Order::create($request->all());

// ✅ Only validated and safe data
Order::create($request->validated());
```

## Checklist

- [ ] Validation logic lives in Form Request classes, not controllers
- [ ] authorize() method properly checks permissions
- [ ] Custom Rule objects used for reusable complex validation
- [ ] prepareForValidation() sanitizes input before validation
- [ ] after() used for cross-field or business logic validation
- [ ] Array and nested fields validated with wildcard notation
- [ ] Database rules use proper scoping and ignore patterns
- [ ] Only validated/safe data used when creating or updating models
- [ ] bail used where early termination is desired
- [ ] Custom error messages provided for user-facing fields
