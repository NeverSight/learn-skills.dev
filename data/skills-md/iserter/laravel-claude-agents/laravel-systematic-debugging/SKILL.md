---
name: laravel-systematic-debugging
description: Systematic debugging process for Laravel applications - ensures root cause investigation before attempting fixes. Use for any Laravel issue (test failures, bugs, unexpected behavior, performance problems).
---

# Systematic Debugging for Laravel

## Overview

Random fixes waste time and create new bugs in Laravel applications. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY Laravel technical issue:
- Test failures
- Eloquent query issues
- Authentication/authorization bugs
- Validation failures
- Queue job failures
- Route errors
- Migration issues
- N+1 query problems
- Performance issues

**Use this ESPECIALLY when:**
- Under time pressure
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

## The Four Phases

You MUST complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully**
   ```
   SQLSTATE[23000]: Integrity constraint violation
   → Check foreign key constraints, not a code bug
   
   Class 'App\Models\Post' not found
   → Check namespace, run composer dump-autoload
   
   Method Illuminate\Database\Eloquent\Collection::save does not exist
   → get() returns Collection, not Model. Use first() or update()
   ```

2. **Check Laravel Logs**
   ```bash
   # Main Laravel log
   tail -f storage/logs/laravel.log
   
   # Check for specific errors
   grep "SQLSTATE" storage/logs/laravel.log
   
   # Clear logs if too large
   > storage/logs/laravel.log
   ```

3. **Enable Debug Mode (Local Only)**
   ```env
   APP_DEBUG=true
   APP_ENV=local
   ```

4. **Use Laravel Telescope**
   ```bash
   composer require laravel/telescope --dev
   php artisan telescope:install
   php artisan migrate
   
   # Access at /telescope
   # View: Requests, Queries, Jobs, Events, Exceptions
   ```

5. **Check Recent Changes**
   ```bash
   # What changed that could cause this?
   git log --oneline -10
   git diff HEAD~5
   
   # Check if migrations ran
   php artisan migrate:status
   
   # Check if config cached
   php artisan config:show
   ```

6. **Reproduce Consistently**
   ```bash
   # Can you trigger it every time?
   php artisan tinker
   >>> App\Models\Post::first();
   
   # Try in different environments
   APP_ENV=testing php artisan test
   ```

7. **Trace Data Flow for Eloquent Issues**
   ```php
   // Enable query logging
   DB::listen(function ($query) {
       Log::debug('Query executed', [
           'sql' => $query->sql,
           'bindings' => $query->bindings,
           'time' => $query->time,
       ]);
   });
   
   // Or in specific code
   DB::enableQueryLog();
   $posts = Post::with('user')->get();
   dd(DB::getQueryLog());
   ```

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples in Laravel**
   ```bash
   # Search for similar working code
   grep -r "belongsTo" app/Models/
   grep -r "middleware" app/Http/
   
   # Check Laravel docs for the pattern
   # Check other models that work correctly
   ```

2. **Compare Against Laravel Conventions**
   ```php
   // ❌ What you have
   class Post extends Model {
       public function author() {
           return $this->hasOne(User::class, 'id', 'user_id');
       }
   }
   
   // ✅ Laravel convention
   class Post extends Model {
       public function user(): BelongsTo {
           return $this->belongsTo(User::class);
       }
   }
   ```

3. **Check Laravel Documentation**
   - Read the COMPLETE section, don't skim
   - Follow examples exactly first
   - Customize only after understanding

4. **Identify Differences**
   ```php
   // Working model
   class User extends Model {
       protected $fillable = ['name', 'email'];
   }
   
   // Broken model - difference: missing mass assignment protection
   class Post extends Model {
       // No $fillable or $guarded defined
   }
   ```

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   ```
   Hypothesis: "Posts aren't saving because mass assignment 
   protection is blocking the 'user_id' field"
   
   Expected: Adding 'user_id' to $fillable will fix it
   ```

2. **Test Minimally**
   ```php
   // Before (broken)
   protected $fillable = ['title', 'content'];
   
   // Test change (ONE variable)
   protected $fillable = ['title', 'content', 'user_id'];
   
   // Don't change multiple things at once
   ```

3. **Verify in Tinker**
   ```bash
   php artisan tinker
   >>> $post = Post::create(['title' => 'Test', 'content' => 'Test', 'user_id' => 1]);
   >>> $post->user_id; // Should be 1
   ```

4. **When You Don't Know**
   - Say "I don't understand why X is happening"
   - Check Laravel GitHub issues for similar problems
   - Ask in Laravel Discord/Forums with specifics
   - Don't pretend to know

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

1. **Create Failing Test Case**
   ```php
   use Illuminate\Foundation\Testing\RefreshDatabase;
   
   test('user can create post', function () {
       $user = User::factory()->create();
       
       $response = $this->actingAs($user)
           ->post('/posts', [
               'title' => 'Test Post',
               'content' => 'Test content',
           ]);
       
       $response->assertRedirect();
       
       expect(Post::where('title', 'Test Post')->exists())->toBeTrue();
       expect(Post::first()->user_id)->toBe($user->id);
   });
   
   // Run and watch it FAIL first
   php artisan test --filter=user_can_create_post
   ```

2. **Implement Single Fix**
   ```php
   // ONE fix for the root cause
   protected $fillable = ['title', 'content', 'user_id'];
   
   // NO bundled improvements like:
   // - Adding casts
   // - Refactoring methods
   // - Changing other code
   ```

3. **Verify Fix**
   ```bash
   # Test passes now
   php artisan test --filter=user_can_create_post
   
   # All tests still pass
   php artisan test
   
   # Manual verification
   php artisan tinker
   >>> $post = Post::create([...]);
   ```

4. **If Fix Doesn't Work**
   - STOP
   - Count: How many fixes have you tried?
   - If < 3: Return to Phase 1 with new information
   - **If ≥ 3: STOP and question the approach**

5. **If 3+ Fixes Failed: Question Architecture**
   ```
   Pattern indicating architectural problem:
   - Each fix reveals new shared state/coupling
   - Fixes require "massive refactoring"
   - Each fix creates new symptoms elsewhere
   
   STOP and question fundamentals:
   - Is this Laravel pattern correct?
   - Should we use a different approach (repository/service)?
   - Are we fighting the framework?
   
   Discuss with team before attempting more fixes.
   ```

## Laravel-Specific Debug Techniques

### Eloquent Debugging
```php
// See actual SQL
$posts = Post::where('status', 'published');
dd($posts->toSql(), $posts->getBindings());

// Check relationship loading
$post = Post::first();
$post->relationLoaded('user'); // false
$post->load('user');
$post->relationLoaded('user'); // true

// Prevent lazy loading (catch N+1)
Model::preventLazyLoading(!app()->isProduction());
```

### Route Debugging
```bash
# List all routes
php artisan route:list

# Find specific route
php artisan route:list --name=posts

# Check route exists
php artisan tinker
>>> route('posts.show', 1);
```

### Queue Debugging
```bash
# See failed jobs
php artisan queue:failed

# Retry failed job
php artisan queue:retry <id>

# Work queue with verbose output
php artisan queue:work --verbose

# Check job payload
php artisan tinker
>>> DB::table('jobs')->first();
```

### Validation Debugging
```php
// See exact validation errors
protected function failedValidation(Validator $validator)
{
    Log::debug('Validation failed', [
        'errors' => $validator->errors()->toArray(),
        'input' => $this->all(),
    ]);
    
    parent::failedValidation($validator);
}
```

## Red Flags - STOP and Follow Process

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add protected $guarded = [] to see if that helps"
- "Skip the test, I'll manually verify"
- "It's probably the relationship definition"
- "I don't fully understand Eloquent but this might work"
- "The docs say X but I'll adapt it differently"
- **"One more fix attempt" (when already tried 2+)**

**ALL of these mean: STOP. Return to Phase 1.**

## Common Laravel Debugging Scenarios

### Scenario 1: N+1 Query Problem
```
Phase 1: Detect it
- Enable Model::preventLazyLoading()
- Exception thrown showing the problem

Phase 2: Find the pattern
- Check working code that uses with()
- Identify which relationship is lazy loading

Phase 3: Hypothesis
- "Adding with('user') will prevent the N+1"

Phase 4: Fix
- Add test that counts queries
- Add with('user') to the query
- Verify query count reduced
```

### Scenario 2: Route Model Binding Not Working
```
Phase 1: Investigate
- Check route definition: /posts/{post}
- Check controller parameter: Post $post
- Check if using custom key

Phase 2: Pattern
- Compare with working route binding
- Check Post model for getRouteKeyName()

Phase 3: Hypothesis
- "Parameter name doesn't match or model not found"

Phase 4: Fix
- Ensure route parameter matches method parameter
- Or customize: public function getRouteKeyName() { return 'slug'; }
```

### Scenario 3: Mass Assignment Exception
```
Phase 1: Error says "Add [field] to fillable property"
Phase 2: Check other models' $fillable arrays
Phase 3: Hypothesis: "Field not in $fillable"
Phase 4: Add field to $fillable, test
```

## Integration with Laravel Agents

- Use **laravel-debugger** for Laravel-specific debugging help
- Use **laravel-testing-expert** for creating failing tests (Phase 4)
- Use **eloquent-specialist** for relationship debugging
- Use **laravel-performance-optimizer** for performance issues

## Quick Reference

| Phase | Laravel-Specific Activities | Success Criteria |
|-------|----------------------------|------------------|
| **1. Root Cause** | Check logs, Telescope, Tinker, recent changes | Understand WHAT and WHY |
| **2. Pattern** | Find working Laravel examples, check docs | Identify differences |
| **3. Hypothesis** | Form theory, test in Tinker | Confirmed or new hypothesis |
| **4. Implementation** | Create Pest test, fix, verify | Bug resolved, tests pass |

## Remember

- Laravel has excellent error messages - read them fully
- Use Telescope for comprehensive debugging
- Tinker is your friend for testing hypotheses
- Follow Laravel conventions - fighting the framework causes bugs
- 95% of "weird Laravel behavior" is misunderstanding the framework

Always investigate systematically, understand the root cause, then fix once correctly.
