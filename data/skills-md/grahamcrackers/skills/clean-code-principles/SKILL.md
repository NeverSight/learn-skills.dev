---
name: clean-code-principles
description: Clean code principles for readable, maintainable TypeScript and React codebases. Covers naming, functions, abstraction, composition, error handling, comments, and code smells. Use when writing new code, refactoring, reviewing code quality, or when the user asks about clean code, readability, or maintainability.
---

# Clean Code Principles

Practical guidelines for writing readable, maintainable code in TypeScript and React.

## Naming

### Be Descriptive and Specific

Names should reveal intent. A reader should understand what a variable holds or what a function does without reading its implementation.

```typescript
// Vague
const d = new Date();
const list = getItems();
function process(data: unknown) {}

// Clear
const registrationDate = new Date();
const activeUsers = getActiveUsers();
function validatePaymentInput(input: PaymentInput) {}
```

### Use Consistent Vocabulary

Pick one word per concept and stick with it across the codebase.

```typescript
// Inconsistent — uses fetch, get, retrieve interchangeably
fetchUsers();
getProducts();
retrieveOrders();

// Consistent
getUsers();
getProducts();
getOrders();
```

### Booleans Should Read as Yes/No Questions

```typescript
const isLoading = true;
const hasPermission = user.role === "admin";
const canEdit = hasPermission && !isArchived;
const shouldAutoSave = settings.autoSave && isDirty;
```

### Event Handlers

Prefix handlers with `handle`, prefix callback props with `on`:

```tsx
function SearchForm({ onSubmit }: { onSubmit: (query: string) => void }) {
    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        onSubmit(query);
    };
    return <form onSubmit={handleSubmit}>...</form>;
}
```

### Avoid Encodings and Abbreviations

```typescript
// Avoid
const usrLst: IUser[] = [];
const btnRef = useRef<HTMLButtonElement>(null);
const tmpVal = calculate();

// Prefer
const users: User[] = [];
const buttonRef = useRef<HTMLButtonElement>(null);
const discountedPrice = calculate();
```

Exception: widely understood abbreviations like `e` for events, `i` for loop indices, `ref` for React refs, and `ctx` for context are fine.

## Functions

### Keep Functions Small and Focused

Each function should do one thing. If you can describe what it does with "and," it's doing too much.

```typescript
// Too much — fetches, transforms, and saves
async function syncUserData(userId: string) {
    const response = await api.get(`/users/${userId}`);
    const user = {
        ...response.data,
        fullName: `${response.data.firstName} ${response.data.lastName}`,
        isActive: response.data.status === "active",
    };
    await db.users.upsert(user);
    await cache.invalidate(`user:${userId}`);
}

// Split by responsibility
async function fetchUser(userId: string): Promise<ApiUser> {
    const response = await api.get(`/users/${userId}`);
    return response.data;
}

function toUser(data: ApiUser): User {
    return {
        ...data,
        fullName: `${data.firstName} ${data.lastName}`,
        isActive: data.status === "active",
    };
}

async function syncUser(userId: string) {
    const data = await fetchUser(userId);
    const user = toUser(data);
    await db.users.upsert(user);
    await cache.invalidate(`user:${userId}`);
}
```

### Limit Parameters

More than 3 parameters signals the function is doing too much or needs an options object.

```typescript
// Too many positional args
function createUser(name: string, email: string, role: string, teamId: string, notify: boolean) {}

// Use an object
function createUser(input: CreateUserInput) {}
```

### Avoid Flag Arguments

A boolean parameter usually means the function does two things. Split it.

```typescript
// Flag decides behavior
function renderList(items: Item[], isCompact: boolean) {}

// Two functions with clear intent
function renderList(items: Item[]) {}
function renderCompactList(items: Item[]) {}
```

### Prefer Pure Functions

Functions without side effects are easier to test, reason about, and reuse.

```typescript
// Impure — mutates external state
let total = 0;
function addToTotal(amount: number) {
    total += amount;
}

// Pure — returns a new value
function add(a: number, b: number): number {
    return a + b;
}
```

### Return Early

Reduce nesting by handling edge cases first.

```typescript
// Deeply nested
function getDiscount(user: User) {
    if (user) {
        if (user.subscription) {
            if (user.subscription.isActive) {
                return user.subscription.discount;
            }
        }
    }
    return 0;
}

// Early returns
function getDiscount(user: User) {
    if (!user?.subscription?.isActive) return 0;
    return user.subscription.discount;
}
```

## Abstraction

### Don't Repeat Yourself (Wisely)

Duplication is cheaper than the wrong abstraction. Wait until you see the same pattern 3 times before abstracting. When you do abstract, make sure the shared code represents a genuine concept, not just coincidental similarity.

```typescript
// Two functions that look similar but serve different purposes — don't merge
function formatUserDisplayName(user: User) {
    return `${user.firstName} ${user.lastName}`;
}

function formatAuthorByline(author: Author) {
    return `${author.firstName} ${author.lastName}`;
}

// When they genuinely share a concept — abstract
function formatFullName(person: { firstName: string; lastName: string }) {
    return `${person.firstName} ${person.lastName}`;
}
```

### Prefer Composition Over Inheritance

Build behavior by combining small, focused pieces.

```tsx
// Instead of a monolithic component with many props
<Card variant="user" showAvatar showBadge showActions />

// Compose smaller components
<Card>
    <Card.Header>
        <Avatar src={user.avatar} />
        <Badge status={user.status} />
    </Card.Header>
    <Card.Body>{user.bio}</Card.Body>
    <Card.Actions>
        <EditButton />
    </Card.Actions>
</Card>
```

### Keep Abstractions at One Level

Each function should operate at a single level of abstraction. Don't mix high-level orchestration with low-level details.

```typescript
// Mixed levels
async function onboardUser(input: OnboardInput) {
    const hashedPassword = await bcrypt.hash(input.password, 12);
    const user = await db.users.create({ ...input, password: hashedPassword });
    const token = jwt.sign({ userId: user.id }, SECRET, { expiresIn: "7d" });
    await sendgrid.send({
        to: user.email,
        subject: "Welcome!",
        html: `<h1>Hello ${user.name}</h1>`,
    });
    return { user, token };
}

// Single level
async function onboardUser(input: OnboardInput) {
    const user = await createUser(input);
    const token = generateAuthToken(user);
    await sendWelcomeEmail(user);
    return { user, token };
}
```

## Error Handling

### Throw Meaningful Errors

```typescript
// Unhelpful
throw new Error("Invalid input");

// Helpful
throw new Error(`User with email "${email}" already exists. Use a different email or log in.`);
```

### Use Typed Error Classes

```typescript
class NotFoundError extends Error {
    constructor(resource: string, id: string) {
        super(`${resource} with id "${id}" not found`);
        this.name = "NotFoundError";
    }
}

class ValidationError extends Error {
    constructor(
        public readonly field: string,
        message: string,
    ) {
        super(message);
        this.name = "ValidationError";
    }
}
```

### Don't Swallow Errors

```typescript
// Silent failure — hides bugs
try {
    await saveData(data);
} catch {
    // do nothing
}

// Handle or propagate
try {
    await saveData(data);
} catch (error) {
    logger.error("Failed to save data", { error, data });
    throw error;
}
```

### Use Result Types for Expected Failures

For operations that can fail as part of normal flow, return results instead of throwing:

```typescript
type Result<T, E = Error> = { success: true; data: T } | { success: false; error: E };

function parseConfig(raw: string): Result<Config> {
    try {
        const parsed = JSON.parse(raw);
        return { success: true, data: configSchema.parse(parsed) };
    } catch (error) {
        return { success: false, error: new Error("Invalid config format") };
    }
}
```

## Comments

### Code Should Be Self-Documenting

If you need a comment to explain what code does, the code should be rewritten to be clearer.

```typescript
// Bad — comment restates the code
// Check if user is active
if (user.status === "active") {
}

// Good — no comment needed
const isActive = user.status === "active";
if (isActive) {
}
```

### Comment Why, Not What

Comments should explain intent, trade-offs, or constraints that the code cannot convey.

```typescript
// Debounce to 300ms because the search API rate-limits at 10 req/s
const debouncedSearch = useDebouncedCallback(search, 300);

// Must match the order defined in the payment provider's webhook spec
const WEBHOOK_EVENTS = ["payment.created", "payment.updated", "payment.failed"] as const;
```

### Delete Commented-Out Code

Version control exists. Don't leave dead code behind.

## Code Smells

### Large Files

If a file exceeds ~300 lines, look for opportunities to extract. Components, hooks, utilities, and types can often be split.

### Deep Nesting

More than 2–3 levels of nesting hurts readability. Flatten with early returns, extracted functions, or guard clauses.

### Long Parameter Lists

More than 3 parameters signals the need for an options object or decomposition.

### Feature Envy

A function that accesses another object's data more than its own should probably live on (or closer to) that object.

### Magic Numbers and Strings

Extract to named constants:

```typescript
// Magic
if (password.length < 8) {
}
if (retries > 3) {
}

// Named
const MIN_PASSWORD_LENGTH = 8;
const MAX_RETRIES = 3;

if (password.length < MIN_PASSWORD_LENGTH) {
}
if (retries > MAX_RETRIES) {
}
```

### Primitive Obsession

Use types and branded types instead of raw primitives for domain concepts:

```typescript
// Primitives everywhere — easy to mix up
function createOrder(userId: string, productId: string, quantity: number) {}

// Domain types
type UserId = string & { readonly __brand: "UserId" };
type ProductId = string & { readonly __brand: "ProductId" };

function createOrder(userId: UserId, productId: ProductId, quantity: number) {}
```

## React-Specific Clean Code

### Components Should Do One Thing

If a component handles data fetching, business logic, and rendering, split it:

```tsx
// Data layer
function UserProfile({ userId }: { userId: string }) {
    const { data: user } = useUser(userId);
    if (!user) return <UserProfileSkeleton />;
    return <UserProfileView user={user} />;
}

// Presentation layer
function UserProfileView({ user }: { user: User }) {
    return (
        <div>
            <Avatar src={user.avatar} />
            <h2>{user.name}</h2>
        </div>
    );
}
```

### Custom Hooks for Reusable Logic

Extract shared logic into hooks — not shared state, shared logic:

```typescript
function useToggle(initial = false) {
    const [value, setValue] = useState(initial);
    const toggle = useCallback(() => setValue((v) => !v), []);
    const setTrue = useCallback(() => setValue(true), []);
    const setFalse = useCallback(() => setValue(false), []);
    return { value, toggle, setTrue, setFalse } as const;
}
```

### Avoid Prop Drilling

If props pass through 3+ levels, use composition (children/slots), Context, or a state library.

### Colocate Related Code

Keep components, hooks, types, and tests close to where they're used. Don't scatter related code across the file tree.

## Design Patterns

| Category                  | Description                                                          | Reference                                                               |
| ------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| GoF Patterns (TypeScript) | Classic 22 design patterns with TypeScript examples                  | [Refactoring Guru](https://refactoring.guru/design-patterns/typescript) |
| React Patterns            | Compound components, render props, hooks, providers, slots, and more | [react-patterns](references/react-patterns.md)                          |

### GoF Patterns (TypeScript)

Classic design patterns with TypeScript implementations. Full catalog and examples at [Refactoring Guru — Design Patterns in TypeScript](https://refactoring.guru/design-patterns/typescript).

### Creational Patterns

| Pattern          | Purpose                                        | Reference                                                          |
| ---------------- | ---------------------------------------------- | ------------------------------------------------------------------ |
| Factory Method   | Create objects without specifying exact class  | [pattern-factory-method](references/pattern-factory-method.md)     |
| Abstract Factory | Produce families of related objects            | [pattern-abstract-factory](references/pattern-abstract-factory.md) |
| Builder          | Construct complex objects step by step         | [pattern-builder](references/pattern-builder.md)                   |
| Singleton        | Ensure a class has only one instance           | [pattern-singleton](references/pattern-singleton.md)               |
| Prototype        | Copy existing objects without class dependency | [pattern-prototype](references/pattern-prototype.md)               |

### Structural Patterns

| Pattern   | Purpose                                            | Reference                                            |
| --------- | -------------------------------------------------- | ---------------------------------------------------- |
| Adapter   | Make incompatible interfaces work together         | [pattern-adapter](references/pattern-adapter.md)     |
| Decorator | Attach new behaviors via wrapper objects           | [pattern-decorator](references/pattern-decorator.md) |
| Facade    | Simplified interface to a complex subsystem        | [pattern-facade](references/pattern-facade.md)       |
| Proxy     | Placeholder that controls access to another object | [pattern-proxy](references/pattern-proxy.md)         |
| Composite | Compose objects into tree structures               | [pattern-composite](references/pattern-composite.md) |
| Bridge    | Split abstraction from implementation              | [pattern-bridge](references/pattern-bridge.md)       |
| Flyweight | Share state between many similar objects           | [pattern-flyweight](references/pattern-flyweight.md) |

### Behavioral Patterns

| Pattern                 | Purpose                                                  | Reference                                                                        |
| ----------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Strategy                | Swap algorithms at runtime                               | [pattern-strategy](references/pattern-strategy.md)                               |
| Observer                | Notify subscribers of state changes                      | [pattern-observer](references/pattern-observer.md)                               |
| Command                 | Turn requests into stand-alone objects                   | [pattern-command](references/pattern-command.md)                                 |
| State                   | Alter behavior when internal state changes               | [pattern-state](references/pattern-state.md)                                     |
| Chain of Responsibility | Pass requests along a handler chain                      | [pattern-chain-of-responsibility](references/pattern-chain-of-responsibility.md) |
| Mediator                | Reduce direct dependencies between objects               | [pattern-mediator](references/pattern-mediator.md)                               |
| Iterator                | Traverse a collection without exposing internals         | [pattern-iterator](references/pattern-iterator.md)                               |
| Template Method         | Define algorithm skeleton, let subclasses override steps | [pattern-template-method](references/pattern-template-method.md)                 |
| Visitor                 | Separate algorithms from the objects they operate on     | [pattern-visitor](references/pattern-visitor.md)                                 |
| Memento                 | Save and restore object state                            | [pattern-memento](references/pattern-memento.md)                                 |

### Most Useful GoF Patterns in Frontend/React

- **Strategy** — swappable validation, sorting, or formatting logic
- **Observer** — event emitters, pub/sub, store subscriptions
- **Adapter** — wrapping 3rd party APIs to your interface
- **Facade** — simplified API client or service layer
- **Builder** — constructing complex query objects, form schemas, or configs
- **Decorator** — higher-order components, middleware, extending behavior
- **State** — XState machines, status-driven UI
- **Command** — undo/redo, action queues, optimistic updates
- **Composite** — recursive tree rendering (menus, file explorers, org charts)

### React-Specific Patterns

Patterns born from React's component model that don't exist in the GoF catalog. See [react-patterns](references/react-patterns.md) for full examples.

| Pattern                    | Purpose                                                               |
| -------------------------- | --------------------------------------------------------------------- |
| Compound Components        | Multiple components sharing implicit state (`<Tabs>`, `<Tabs.Panel>`) |
| Render Props               | Pass a function as prop to delegate rendering                         |
| Custom Hook                | Extract reusable stateful logic into `use*` functions                 |
| Provider                   | Context-based dependency injection across the tree                    |
| Container / Presentational | Separate data fetching from pure UI rendering                         |
| Controlled / Uncontrolled  | Who owns the state — parent or component?                             |
| Polymorphic Components     | `as` / `asChild` prop for flexible element rendering                  |
| Slot Pattern               | Pass components as named props for layout composition                 |
| State Reducer              | Let consumers customize internal state transitions                    |
| Forwarded Refs             | Expose imperative API to parent via `useImperativeHandle`             |
| Higher-Order Components    | Wrap a component with cross-cutting behavior                          |
| Error Boundary             | Declarative error catching in the component tree                      |
| Optimistic Updates         | Update UI before server confirms, rollback on failure                 |
| Portal                     | Render outside the DOM hierarchy (modals, tooltips)                   |

## Key Principles

1. **Readability over cleverness** — code is read far more than it is written.
2. **Delete code you don't need** — less code means fewer bugs and easier maintenance.
3. **Make the right thing easy and the wrong thing hard** — design APIs that guide correct usage.
4. **Leave the code better than you found it** — the Boy Scout Rule applies to every change.
5. **Optimize for change** — code will be modified. Structure it to make future changes safe and easy.

## References

- [Refactoring Guru — Design Patterns](https://refactoring.guru/design-patterns) — full catalog with TypeScript examples
- [Refactoring Guru — Code Smells](https://refactoring.guru/refactoring/smells) — catalog of code smells and refactoring techniques
- [The Twelve-Factor App](https://12factor.net/) — methodology for building modern, scalable, maintainable software-as-a-service apps ([reference](references/twelve-factor-app.md))
