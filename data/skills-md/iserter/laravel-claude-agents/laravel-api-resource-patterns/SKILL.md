---
name: laravel-api-resource-patterns
description: Best practices for Laravel API Resources including resource transformation, collection handling, conditional attributes, and relationship loading.
---

# API Resource Patterns

## Basic Resource Structure

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class PostResource extends JsonResource
{
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'content' => $this->content,
            'created_at' => $this->created_at->toISOString(),
            'updated_at' => $this->updated_at->toISOString(),
        ];
    }
}
```

## Conditional Attributes

```php
public function toArray($request): array
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        
        // Only include if loaded
        'author' => new UserResource($this->whenLoaded('user')),
        
        // Only include if condition is true
        'content' => $this->when($request->user()?->can('view', $this->resource), $this->content),
        
        // Only include if not null
        'comments_count' => $this->when($this->comments_count !== null, $this->comments_count),
        
        // Merge conditionally
        $this->mergeWhen($request->user()?->isAdmin(), [
            'internal_notes' => $this->internal_notes,
        ]),
    ];
}
```

## Nested Relationships

```php
public function toArray($request): array
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        
        // Single relationship
        'author' => new UserResource($this->whenLoaded('user')),
        
        // Collection relationship
        'comments' => CommentResource::collection($this->whenLoaded('comments')),
        
        // Nested relationships
        'category' => new CategoryResource($this->whenLoaded('category')),
    ];
}
```

## Resource Collections

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class PostCollection extends ResourceCollection
{
    public function toArray($request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total' => $this->total(),
                'count' => $this->count(),
                'per_page' => $this->perPage(),
                'current_page' => $this->currentPage(),
                'total_pages' => $this->lastPage(),
            ],
            'links' => [
                'self' => $request->url(),
                'first' => $this->url(1),
                'last' => $this->url($this->lastPage()),
                'prev' => $this->previousPageUrl(),
                'next' => $this->nextPageUrl(),
            ],
        ];
    }
}
```

## Adding Links

```php
public function toArray($request): array
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        'links' => [
            'self' => route('posts.show', $this->id),
            'author' => route('users.show', $this->user_id),
            'comments' => route('posts.comments.index', $this->id),
        ],
    ];
}
```

## Resource Response Customization

```php
// In controller
public function store(Request $request)
{
    $post = Post::create($request->validated());
    
    return (new PostResource($post))
        ->response()
        ->setStatusCode(201)
        ->header('Location', route('posts.show', $post));
}
```

## Pivot Data in Resources

```php
public function toArray($request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'assigned_at' => $this->whenPivotLoaded('role_user', function () {
            return $this->pivot->created_at;
        }),
        'expires_at' => $this->whenPivotLoadedAs('assignment', 'role_user', function () {
            return $this->assignment->expires_at;
        }),
    ];
}
```

## Wrapping and Unwrapping

```php
// Disable wrapping in AppServiceProvider
use Illuminate\Http\Resources\Json\JsonResource;

public function boot()
{
    JsonResource::withoutWrapping();
}

// Or per resource
public static $wrap = 'post';
```

## With Additional Data

```php
public function with($request): array
{
    return [
        'version' => '1.0.0',
        'timestamp' => now()->toISOString(),
    ];
}

public function withResponse($request, $response)
{
    $response->header('X-Value', 'True');
}
```

## Best Practices

### Always Use whenLoaded for Relationships

```php
// ✅ Prevents N+1 queries
'author' => new UserResource($this->whenLoaded('user')),

// ❌ Will cause N+1 queries
'author' => new UserResource($this->user),
```

### Use Type Hints

```php
use Illuminate\Http\Request;

public function toArray(Request $request): array
{
    // ...
}
```

### Keep Resources Focused

```php
// ✅ Create separate resources for different contexts
class PostResource extends JsonResource { }
class PostListResource extends JsonResource { }
class PostDetailResource extends JsonResource { }

// ❌ Don't make one resource do everything
```

### Use Resource Collections

```php
// ✅ Use collection class
return new PostCollection(Post::paginate());

// ✅ Or collection method
return PostResource::collection(Post::all());
```

## Controller Usage

```php
class PostController extends Controller
{
    public function index()
    {
        $posts = Post::with(['user', 'category'])
            ->withCount('comments')
            ->paginate(15);
        
        return new PostCollection($posts);
    }
    
    public function show(Post $post)
    {
        $post->load(['user', 'comments.user', 'tags']);
        
        return new PostResource($post);
    }
    
    public function store(StorePostRequest $request)
    {
        $post = Post::create($request->validated());
        
        return (new PostResource($post))
            ->response()
            ->setStatusCode(201);
    }
}
```

## Checklist

- [ ] Resources transform models consistently
- [ ] Relationships loaded with whenLoaded()
- [ ] Conditional attributes use when()
- [ ] Collections include pagination metadata
- [ ] Links included for HATEOAS
- [ ] Type hints used
- [ ] Proper HTTP status codes
- [ ] No N+1 queries
- [ ] Consistent date formatting
- [ ] Appropriate wrapping strategy
