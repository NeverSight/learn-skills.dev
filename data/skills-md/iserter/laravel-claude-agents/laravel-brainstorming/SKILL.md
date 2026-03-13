---
name: laravel-brainstorming
description: Use when creating or developing Laravel features, before writing code or implementation plans - refines rough ideas into fully-formed Laravel designs through collaborative questioning, alternative exploration, and incremental validation.
---

# Brainstorming Laravel Ideas Into Designs

## Overview

Help turn Laravel feature ideas into fully formed designs and specs through natural collaborative dialogue, focusing on Laravel best practices and ecosystem patterns.

Start by understanding the current Laravel project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

## The Process

**Understanding the idea:**
- Check out the current Laravel project state first (routes, models, migrations, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, Laravel patterns, constraints, success criteria

**Example Questions:**
- "Should this be a queue job or run synchronously?"
- "Which authentication approach: Sanctum, Passport, or custom?"
- "Will this need real-time updates via broadcasting?"
- "Should we use Eloquent events or explicit service calls?"

**Exploring approaches:**
- Propose 2-3 different Laravel approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Example:**
```
For the notification system, I see three approaches:

1. Laravel Notifications with database channel (recommended)
   - Built-in, follows Laravel conventions
   - Easy to add email/Slack later
   - Simple to mark as read
   Trade-off: Less flexible for complex notification logic

2. Custom Event/Listener system
   - Maximum flexibility
   - Can add complex rules
   Trade-off: More code to maintain

3. Third-party package (like Laravel Echo)
   - Real-time out of the box
   Trade-off: External dependency, overkill if not needed

I'd recommend #1 for most cases - start simple, Laravel's notification system is excellent and you can always extend it later if needed.

Which approach feels right for your use case?
```

**Presenting the design:**
- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: database schema, models & relationships, routes & controllers, services/actions, queues/events, API resources, validation, testing
- Be ready to go back and clarify if something doesn't make sense

## Laravel-Specific Design Sections

### 1. Database Schema
```
First, let's look at the database design:

We'll need three tables:
1. `posts` - title, slug, content, status, published_at
2. `tags` - name, slug
3. `post_tag` - pivot table for many-to-many

The posts table will have a foreign key to users, indexed on status and published_at for common queries. We'll use an enum for status (draft, published, archived) to keep it clean.

Does this schema structure make sense for what we're building?
```

### 2. Models & Relationships
```
For the models, we'll have:

Post model with:
- belongsTo relationship to User
- belongsToMany relationship to Tag
- Scopes: published(), draft(), recent()
- Casts: published_at as datetime, metadata as array
- Factory for testing

Tag model with:
- belongsToMany relationship to Post
- Slug auto-generation on save

Should we add soft deletes to posts, or will hard deletes work?
```

### 3. API Design
```
For the API endpoints, following RESTful conventions:

GET    /api/posts           - List posts (paginated)
POST   /api/posts           - Create post
GET    /api/posts/{post}    - Show post
PUT    /api/posts/{post}    - Update post
DELETE /api/posts/{post}    - Delete post

Authentication via Sanctum, rate limited to 60 requests/minute.
API resources will transform the output, hiding sensitive data.

Does this API structure cover your needs?
```

### 4. Business Logic
```
The posting workflow:

When a post is published:
1. PostService validates the post is ready (has title, content)
2. Sets published_at timestamp
3. Dispatches NotifySubscribers job to queue
4. Fires PostPublished event for other listeners
5. Clears related caches

We'll use a service class to keep controllers thin, and queues for email notifications so publishing is fast.

Is this flow what you had in mind?
```

## After the Design

**Documentation:**
- Write the validated design to `docs/designs/YYYY-MM-DD-<feature>-design.md`
- Include: feature overview, database schema, API endpoints, business logic flow
- Commit the design document to git

**Implementation (if continuing):**
- Ask: "Ready to set up for implementation?"
- Create implementation checklist
- Consider using test-driven development approach

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features, keep it simple
- **Laravel conventions first** - Use built-in Laravel features before custom solutions
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense

## Laravel-Specific Considerations

When brainstorming Laravel features, consider:

**Architecture:**
- Will this be a monolith or need microservices?
- What design patterns fit best (repository, service layer, actions)?
- How will this scale?

**Database:**
- What relationships are needed?
- What indexes for performance?
- Should we use polymorphic relationships?

**Performance:**
- Should this use queues?
- What caching strategy?
- Eager loading requirements?

**Testing:**
- What factories are needed?
- Feature tests vs unit tests?
- How to test jobs/events?

**Security:**
- Authorization via policies or gates?
- What validation rules?
- Rate limiting needs?

## Example Brainstorming Session

```
Claude: I see you want to add a comment system. Let me understand the requirements.

First question: Should comments be nested (replies to replies) or just one level deep (replies to posts only)?

User: Just one level - comments on posts.

Claude: Got it. And for moderation, which approach:
A) All comments published immediately
B) Comments from new users require approval
C) All comments require approval

User: B - new users need approval.

Claude: Perfect. For notifications when someone comments:
A) Real-time via Laravel Echo and WebSockets
B) Email only
C) In-app notifications (database)

User: In-app notifications.

Claude: Excellent. Let me present the design...

[Design sections follow]
```

## Common Laravel Brainstorming Topics

- Authentication flow (SPA vs traditional)
- API design (REST vs GraphQL)
- Real-time features (Pusher vs Socket.io vs Reverb)
- File upload strategy (local vs S3)
- Multi-tenancy approach
- Payment integration (Stripe, Paddle, Cashier)
- Search implementation (Scout, Elasticsearch)
- Admin panel (Nova, Filament, custom)

## Remember

The goal is to arrive at a clear, actionable Laravel design that:
- Follows Laravel conventions
- Uses appropriate Laravel ecosystem packages
- Is testable and maintainable
- Solves the actual problem without over-engineering
- Can be implemented incrementally

Ask questions until you understand, then design in small validatable chunks.
